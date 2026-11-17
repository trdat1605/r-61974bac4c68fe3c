"""Read-only identity checks for the shared local Chatwoot runtime.

This checks an expected path and shared-WSL-kernel directory identity. It is not
a symlink security sandbox, a portable cross-kernel inode check, or an app test.
Only fixed check names reach stdout; subprocess output/errors never do.
"""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess


TIMEOUT_SECONDS = 15
INFO_FORMAT = '{"id":{{json .ID}},"os":{{json .OperatingSystem}}}'
INSPECT_FORMAT = (
    '{"project":{{json (index .Config.Labels "com.docker.compose.project")}},'
    '"service":{{json (index .Config.Labels "com.docker.compose.service")}},'
    '"app_mounts":[{{range .Mounts}}{{if eq .Destination "/app"}}'
    '{"type":{{json .Type}},"source":{{json .Source}},'
    '"target":{{json .Destination}}},{{end}}{{end}}null]}'
)


class Blocked(Exception):
    """Carry a fixed category, never a command's raw error."""


class DoctorParser(argparse.ArgumentParser):
    def error(self, message):
        raise Blocked("arguments")


def valid_profile(profile):
    if not isinstance(profile, dict):
        return False
    required = ("distribution", "source_root", "source_branch", "source_commit",
                "engine_id", "engine_os", "compose_project")
    if any(not isinstance(profile.get(key), str) or not profile[key] or "\0" in profile[key]
           for key in required):
        return False
    root = profile["source_root"]
    return (
        root.startswith("/") and "\\" not in root and "\0" not in root
        and str(PurePosixPath(root)) == root
        and ".." not in PurePosixPath(root).parts
        and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", profile["distribution"]) is not None
        and re.fullmatch(r"[0-9a-f]{40}", profile["source_commit"]) is not None
        and re.fullmatch(r"[a-z0-9][a-z0-9_-]*", profile["compose_project"]) is not None
        and profile.get("runtime_access") == "read-only"
        and profile.get("app_services") == ["rails", "vite", "sidekiq"]
    )


def diagnose(profile, source_root=None, *, runner=None, windows=None):
    """Return (sanitized result, exit code); runner injection never runs Docker in tests."""
    checks = []
    runner = runner or subprocess.run
    windows = os.name == "nt" if windows is None else windows

    def record(name):
        checks.append({"check": name, "status": "PASS"})

    def command(category, argv):
        if windows:
            argv = ["wsl.exe", "-d", profile["distribution"], "--exec", *argv]
        try:
            result = runner(argv, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=TIMEOUT_SECONDS, check=False,
                            shell=False)
        except (OSError, subprocess.SubprocessError):
            raise Blocked(category + "_command") from None
        if result.returncode != 0:
            raise Blocked(category + "_command")
        return result.stdout.strip()

    def json_command(category, argv):
        try:
            return json.loads(command(category, argv))
        except (ValueError, TypeError):
            raise Blocked(category + "_response") from None

    def directory_identity(category, argv):
        value = command(category, argv)
        if re.fullmatch(r"[0-9]+:[0-9]+", value) is None:
            raise Blocked(category + "_response")
        return value

    try:
        if not valid_profile(profile):
            raise Blocked("profile")
        record("profile")
        expected_root = profile["source_root"]
        # Reject Windows/alternate checkouts before invoking Git or runtime tools.
        if source_root is not None and source_root != expected_root:
            raise Blocked("source_path")
        record("source_path")
        git = ["git", "-C", expected_root]
        if command("git", [*git, "rev-parse", "--show-toplevel"]) != expected_root:
            raise Blocked("git_root")
        if command("git", [*git, "rev-parse", "HEAD"]) != profile["source_commit"]:
            raise Blocked("git_commit")
        if command("git", [*git, "symbolic-ref", "--short", "HEAD"]) != profile["source_branch"]:
            raise Blocked("git_branch")
        record("git_identity")
        host_identity = directory_identity("source_stat", ["stat", "-Lc", "%d:%i", expected_root])
        record("source_directory")
        engine = json_command("engine", ["docker", "info", "--format", INFO_FORMAT])
        if not isinstance(engine, dict) or engine.get("id") != profile["engine_id"]:
            raise Blocked("engine_id")
        if engine.get("os") != profile["engine_os"]:
            raise Blocked("engine_os")
        record("engine_identity")
        for service in profile["app_services"]:
            category = "service_" + service
            ids = command(category, ["docker", "ps", "--filter",
                          "label=com.docker.compose.project=" + profile["compose_project"],
                          "--filter", "label=com.docker.compose.service=" + service,
                          "--format", "{{.ID}}"])
            if re.fullmatch(r"[0-9a-f]{12,64}", ids) is None:
                raise Blocked(category + "_running")
            container = json_command(category, ["docker", "inspect", "--type", "container",
                                                "--format", INSPECT_FORMAT, ids])
            if not isinstance(container, dict):
                raise Blocked(category + "_response")
            if container.get("project") != profile["compose_project"]:
                raise Blocked(category + "_project")
            if container.get("service") != service:
                raise Blocked(category + "_label")
            mounts = container.get("app_mounts")
            if not isinstance(mounts, list):
                raise Blocked(category + "_mount")
            mounts = [mount for mount in mounts if mount is not None]
            if len(mounts) != 1 or not isinstance(mounts[0], dict):
                raise Blocked(category + "_mount")
            mount = mounts[0]
            source = mount.get("source")
            alias_prefix = ("/run/desktop/mnt/host/wsl/docker-desktop-bind-mounts/"
                            + profile["distribution"] + "/")
            is_alias = (isinstance(source, str) and source.startswith(alias_prefix)
                        and re.fullmatch(r"[0-9a-f]{64}", source[len(alias_prefix):]) is not None)
            if (mount.get("type") != "bind" or mount.get("target") != "/app"
                    or not (source == expected_root or is_alias)):
                raise Blocked(category + "_mount")
            # Desktop aliases cannot be proven by Compose working_dir labels.
            # This local runtime shares the WSL kernel: require the same directory.
            actual_identity = directory_identity(category, ["docker", "exec", ids,
                                                            "stat", "-Lc", "%d:%i", "/app"])
            if actual_identity != host_identity:
                raise Blocked(category + "_directory")
            record(category)
    except Blocked as error:
        checks.append({"check": str(error), "status": "FAIL"})
        return {"status": "BLOCKED", "checks": checks}, 2
    return {"status": "HEALTHY", "checks": checks}, 0


def main(argv=None):
    parser = DoctorParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--source-root", help="Must exactly equal the profile Linux source root")
    try:
        args = parser.parse_args(argv)
        profile = json.loads(Path(args.profile).read_text(encoding="utf-8"))
    except Blocked:
        result, code = {"status": "BLOCKED", "checks": [{"check": "arguments", "status": "FAIL"}]}, 2
    except (OSError, ValueError):
        result, code = {"status": "BLOCKED", "checks": [{"check": "profile", "status": "FAIL"}]}, 2
    else:
        result, code = diagnose(profile, args.source_root)
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
