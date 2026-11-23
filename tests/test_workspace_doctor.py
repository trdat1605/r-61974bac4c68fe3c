import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).resolve().parents[1] / "tools/agents/workspace_doctor.py"
SPEC = importlib.util.spec_from_file_location("workspace_doctor", SCRIPT)
doctor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(doctor)
PROFILE = {
    "distribution": "Ubuntu-22.04", "source_root": "/root/code/runtime",
    "source_branch": "codex/runtime", "source_commit": "a" * 40,
    "engine_id": "expected-engine", "engine_os": "Docker Desktop",
    "compose_project": "cwlab-test", "runtime_access": "read-only",
    "app_services": ["rails", "vite", "sidekiq"],
}


def responses():
    values = [PROFILE["source_root"], PROFILE["source_commit"], PROFILE["source_branch"],
              "2096:123", json.dumps({"id": "expected-engine", "os": "Docker Desktop"})]
    for service in PROFILE["app_services"]:
        mount_source = PROFILE["source_root"]
        if service == "vite":
            mount_source = ("/run/desktop/mnt/host/wsl/docker-desktop-bind-mounts/"
                            "Ubuntu-22.04/" + "f" * 64)
        values.extend(["b" * 12, json.dumps({
            "project": "cwlab-test", "service": service,
            "app_mounts": [{"type": "bind", "source": mount_source, "target": "/app"}, None],
        }), "2096:123"])
    return values


def fake_runner(values):
    return Mock(side_effect=[subprocess.CompletedProcess([], 0, value, "") for value in values])


class WorkspaceDoctorTests(unittest.TestCase):
    def test_healthy_windows_argv_is_read_only_and_never_shell(self):
        runner = fake_runner(responses())
        result, code = doctor.diagnose(PROFILE, runner=runner, windows=True)
        self.assertEqual((result["status"], code), ("HEALTHY", 0))
        self.assertEqual(len(runner.call_args_list), 14)
        for call in runner.call_args_list:
            self.assertEqual(call.args[0][:4], ["wsl.exe", "-d", "Ubuntu-22.04", "--exec"])
            self.assertFalse(call.kwargs["shell"])
            self.assertTrue(call.kwargs["capture_output"])
            self.assertEqual(call.kwargs["timeout"], 15)
        commands = [call.args[0][4:] for call in runner.call_args_list]
        self.assertEqual(commands[0], ["git", "-C", PROFILE["source_root"], "rev-parse", "--show-toplevel"])
        for command in commands:
            self.assertIn(command[0], ["git", "stat", "docker"])
            if command[0] == "docker":
                self.assertIn(command[1], ["info", "ps", "inspect", "exec"])
                if command[1] == "inspect":
                    self.assertEqual(command[2:5], ["--type", "container", "--format"])
                    self.assertNotIn("Env", command[5])
                    self.assertNotIn("json .Config", command[5])
                if command[1] == "exec":
                    self.assertEqual(command[3:], ["stat", "-Lc", "%d:%i", "/app"])

    def test_linux_runs_direct_and_explicit_correct_root(self):
        runner = fake_runner(responses())
        _, code = doctor.diagnose(PROFILE, PROFILE["source_root"], runner=runner, windows=False)
        self.assertEqual(code, 0)
        self.assertEqual(runner.call_args_list[0].args[0][0], "git")

    def test_wrong_windows_or_linux_path_blocks_before_any_command(self):
        for root in [r"C:\old\chatwoot", "/root/code/copy", PROFILE["source_root"] + "/"]:
            with self.subTest(root=root):
                runner = Mock()
                result, code = doctor.diagnose(PROFILE, root, runner=runner)
                self.assertEqual(code, 2)
                self.assertEqual(result["checks"][-1]["check"], "source_path")
                runner.assert_not_called()

    def test_wrong_git_root_pin_or_branch(self):
        for index, value, check in [(0, "/other", "git_root"), (1, "0" * 40, "git_commit"),
                                    (2, "main", "git_branch")]:
            values = responses()
            values[index] = value
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual((code, result["checks"][-1]["check"]), (2, check))

    def test_wrong_engine_id_or_os(self):
        for key in ["id", "os"]:
            values = responses()
            engine = json.loads(values[4])
            engine[key] = "wrong"
            values[4] = json.dumps(engine)
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual((code, result["checks"][-1]["check"]), (2, "engine_" + key))

    def test_service_not_running_multiple_or_invalid_ids(self):
        for value in ["", "b" * 12 + "\n" + "c" * 12, "unsafe --option"]:
            values = responses()
            values[5] = value
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual((code, result["checks"][-1]["check"]), (2, "service_rails_running"))

    def test_project_or_service_label_mismatch(self):
        for key, check in [("project", "project"), ("service", "label")]:
            values = responses()
            container = json.loads(values[6])
            container[key] = "wrong"
            values[6] = json.dumps(container)
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual((code, result["checks"][-1]["check"]), (2, "service_rails_" + check))

    def test_wrong_mount_type_source_target_missing_or_duplicate(self):
        original = json.loads(responses()[6])["app_mounts"][0]
        bad_mounts = [[], [None], [original, original]]
        for key, value in [("type", "volume"), ("source", "/other"), ("target", "/other")]:
            mount = dict(original)
            mount[key] = value
            bad_mounts.append([mount])
        for mounts in bad_mounts:
            values = responses()
            container = json.loads(values[6])
            container["app_mounts"] = mounts
            values[6] = json.dumps(container)
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual((code, result["checks"][-1]["check"]), (2, "service_rails_mount"))

    def test_desktop_alias_requires_expected_distribution_and_hash(self):
        for source in ["/run/desktop/anything", "/run/desktop/mnt/host/wsl/docker-desktop-bind-mounts/Other/" + "f" * 64,
                       "/run/desktop/mnt/host/wsl/docker-desktop-bind-mounts/Ubuntu-22.04/../copy"]:
            values = responses()
            container = json.loads(values[9])
            container["app_mounts"][0]["source"] = source
            container["working_dir"] = PROFILE["source_root"]
            values[9] = json.dumps(container)
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual((code, result["checks"][-1]["check"]), (2, "service_vite_mount"))

    def test_copy_or_alias_inode_mismatch_cannot_pass_via_labels(self):
        for index, service in [(7, "rails"), (10, "vite"), (13, "sidekiq")]:
            values = responses()
            values[index] = "2096:999"
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual((code, result["checks"][-1]["check"]), (2, "service_" + service + "_directory"))

    def test_malformed_selected_output_fails_closed_without_echo(self):
        for index in [3, 4, 6, 7, 9]:
            values = responses()
            values[index] = "secret-customer-data"
            result, code = doctor.diagnose(PROFILE, runner=fake_runner(values))
            self.assertEqual(code, 2)
            self.assertNotIn("secret", json.dumps(result))

    def test_each_command_failure_timeout_or_unavailable_is_sanitized(self):
        for index in range(14):
            for failure in [subprocess.CompletedProcess([], 1, "secret-output", "secret-error"),
                            subprocess.TimeoutExpired("secret-command", 15, output="secret-output", stderr="secret-error"),
                            FileNotFoundError("secret-path")]:
                values = [subprocess.CompletedProcess([], 0, value, "") for value in responses()[:index]]
                values.append(failure)
                runner = Mock(side_effect=values)
                result, code = doctor.diagnose(PROFILE, runner=runner)
                self.assertEqual(code, 2)
                self.assertNotIn("secret", json.dumps(result))

    def test_invalid_profile_never_invokes_runtime(self):
        for key, value in [("source_root", "C:\\old"), ("source_root", "/root/../copy"),
                           ("source_commit", "not-pin"), ("app_services", ["postgres"]),
                           ("runtime_access", "write"), ("distribution", "--bad")]:
            profile = copy.deepcopy(PROFILE)
            profile[key] = value
            runner = Mock()
            result, code = doctor.diagnose(profile, runner=runner)
            self.assertEqual((code, result["checks"][-1]["check"]), (2, "profile"))
            runner.assert_not_called()

    def test_cli_invalid_profile_returns_only_generic_json(self):
        output = io.StringIO()
        with patch.object(Path, "read_text", side_effect=OSError("secret-path")), redirect_stdout(output):
            code = doctor.main(["--profile", "missing"])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "BLOCKED")
        self.assertNotIn("secret", output.getvalue())

    def test_cli_invalid_arguments_return_sanitized_json(self):
        for args in [[], ["--secret-token"], ["--profile"]]:
            output = io.StringIO()
            with redirect_stdout(output):
                code = doctor.main(args)
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(output.getvalue())["checks"][-1]["check"], "arguments")
            self.assertNotIn("secret", output.getvalue())


if __name__ == "__main__":
    unittest.main()
