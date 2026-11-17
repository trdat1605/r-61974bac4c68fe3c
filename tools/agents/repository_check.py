"""Run repository checks without changing application/runtime or Git settings."""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from workflow import WorkflowError, verify_task_set


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def test_environment(root, source=None):
    """Foreign Git fixtures must not inherit the caller hook's repository/index/config."""
    environment = dict(os.environ if source is None else source)
    names = git(root, 'rev-parse', '--local-env-vars').decode().splitlines()
    for name in names:
        environment.pop(name, None)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    return environment


def scan_file(path, data):
    issues = []
    parts = [x.casefold() for x in path.split('/')]
    if any(p == '.env' or (p.startswith('.env.') and p != '.env.example') for p in parts) or Path(path).suffix.casefold() in ['.dump', '.rdb', '.sqlite', '.sqlite3', '.vhdx']:
        issues.append('sensitive_file_type')
    text = data.decode('utf-8-sig', errors='replace')
    patterns = {
        'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        'github_token': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
        'credential_url': r'https?://[^\s/<>]+:[^\s/<>]+@',
        'provider_key': r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}',
    }
    for name, pattern in patterns.items():
        if re.search(pattern, text):
            issues.append(name)
    return issues


def index_snapshot(root):
    """Checks the full index against the working files used by Python/tests, including deletions."""
    paths = git(root, 'ls-files', '-z').decode().split('\0')
    paths = [p for p in paths if p]
    findings = []
    for path in paths:
        target = Path(root) / path
        if not target.is_file() or target.read_bytes() != git(root, 'show', ':' + path):
            findings.append({'path': path, 'check': 'staged_working_mismatch'})
    removed = git(root, 'diff', '--cached', '--name-only', '--diff-filter=D', '-z').decode().split('\0')
    for path in filter(None, removed):
        if (Path(root) / path).exists():
            findings.append({'path': path, 'check': 'staged_deleted_but_working_exists'})
    return paths, findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true')
    parser.add_argument('--require-handoffs', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    try:
        if args.staged:
            paths, findings = index_snapshot(root)
        else:
            paths = [p for p in git(root, 'ls-files', '-z').decode().split('\0') if p]
            findings = []
        if findings:
            print(json.dumps({'status': 'BLOCKED', 'findings': findings}))
            return 2
        for path in paths:
            data = git(root, 'show', ':' + path) if args.staged else (root / path).read_bytes()
            findings.extend({'path': path, 'check': issue} for issue in scan_file(path, data))
        if findings:
            print(json.dumps({'status': 'BLOCKED', 'findings': findings}))
            return 2
        tasks = [root / p for p in paths if re.fullmatch(r'tasks/[^/]+/task\.json', p)]
        task_result = verify_task_set(root, tasks, args.require_handoffs, allowed_artifacts=set(paths))
        environment = test_environment(root)
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=root, env=environment)
        if result.returncode:
            return result.returncode
        print(json.dumps({'status': 'PASS', 'files_scanned': len(paths), **task_result,
                          'limits': 'Pattern scan and contract checks do not attest all secrets, execution truth, reviewer identity or product acceptance'}))
        return 0
    except (WorkflowError, OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({'status': 'BLOCKED', 'error': str(error)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
