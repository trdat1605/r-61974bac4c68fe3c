"""Run repository checks without changing application/runtime or Git settings."""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from workflow import WorkflowError, load, validate_task, verify_handoff


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def scan_file(path, data):
    issues = []
    parts = [x.casefold() for x in path.split('/')]
    if '.env' in parts or Path(path).suffix.casefold() in ['.dump', '.rdb', '.sqlite', '.sqlite3', '.vhdx']:
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true')
    parser.add_argument('--require-handoffs', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    try:
        if args.staged:
            paths = git(root, 'diff', '--cached', '--name-only', '--diff-filter=ACMR').decode().splitlines()
        else:
            paths = git(root, 'ls-files').decode().splitlines()
        findings = []
        for path in paths:
            data = git(root, 'show', ':' + path) if args.staged else (root / path).read_bytes()
            if args.staged and (root / path).read_bytes() != data:
                findings.append({'path': path, 'check': 'staged_working_mismatch'})
            findings.extend({'path': path, 'check': issue} for issue in scan_file(path, data))
        if findings:
            print(json.dumps({'status': 'BLOCKED', 'findings': findings}))
            return 2
        tasks = list((root / 'tasks').glob('*/task.json'))
        for task_path in tasks:
            validate_task(load(task_path))
            handoff, review = task_path.parent / 'handoff.json', task_path.parent / 'review.json'
            if handoff.exists() and review.exists():
                verify_handoff(root, task_path, handoff, review)
            elif args.require_handoffs:
                raise WorkflowError('Task lacks handoff/review: ' + task_path.parent.name)
        environment = os.environ.copy()
        environment['PYTHONDONTWRITEBYTECODE'] = '1'
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=root, env=environment)
        if result.returncode:
            return result.returncode
        print(json.dumps({'status': 'PASS', 'files_scanned': len(paths), 'tasks_validated': len(tasks),
                          'limits': 'Pattern scan and contract checks do not attest all secrets, execution truth, reviewer identity or product acceptance'}))
        return 0
    except (WorkflowError, OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({'status': 'BLOCKED', 'error': str(error)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
