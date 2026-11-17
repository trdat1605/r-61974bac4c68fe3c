"""Validate task contracts and version-bound handoffs. No model call or runtime write."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


class WorkflowError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise WorkflowError(message)


def relative_file(value):
    require(isinstance(value, str) and value, 'Expected a relative file path')
    require(chr(92) not in value and ':' not in value, 'Ambiguous or absolute path')
    require(not any(p.casefold() in ('', '.', '..', '.git') for p in value.split('/')), 'Unsafe path')
    require(not any(c in value for c in '*?[]'), 'Exact file paths are required')
    name = Path(value).name.casefold()
    require(name not in ('.env', 'auth.json', 'credentials.json') and
            not (name.startswith('.env.') and name != '.env.example'), 'Secret file path is forbidden')
    return value


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def resolve_commit(root, value):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{7,40}', value), 'Use a Git commit ID, not a mutable branch name')
    return git(root, 'rev-parse', '--verify', value + '^{commit}').decode().strip()


def validate_task(task):
    require(isinstance(task, dict), 'Task must be an object')
    for key in ['id', 'goal', 'repository', 'branch', 'baseline_commit', 'evidence_location', 'implementer', 'reviewer', 'receiver', 'role_brief']:
        require(isinstance(task.get(key), str) and task[key].strip(), 'Missing task field: ' + key)
    require(re.fullmatch(r'[A-Za-z0-9_.-]+', task['id']), 'Invalid task ID')
    require(task['repository'].startswith('https://github.com/') and '@' not in task['repository'], 'Expected a credential-free GitHub repository URL')
    for key in ['acceptance', 'write_scope', 'affected', 'dependencies', 'start_conditions', 'permissions', 'checks', 'stop_conditions']:
        require(isinstance(task.get(key), list) and task[key] and all(isinstance(x, str) and x.strip() for x in task[key]), 'Missing task list: ' + key)
        require(len(set(task[key])) == len(task[key]), 'Duplicate entries: ' + key)
    for path in task['write_scope']:
        relative_file(path)
    require(isinstance(task.get('bound_inputs'), list), 'Declare bound_inputs, empty only when no file input affects the result')
    require(len(set(task['bound_inputs'])) == len(task['bound_inputs']), 'Duplicate bound inputs')
    for path in task['bound_inputs']:
        relative_file(path)
    relative_file(task['role_brief'])
    relative_file(task['evidence_location'].rstrip('/') + '/placeholder.json')
    require(isinstance(task.get('environment'), dict) and task['environment'].get('runtime_access') in ['read-only', 'exclusive-write'], 'Declare runtime access')
    require(isinstance(task.get('application'), dict) and re.fullmatch(r'[0-9a-f]{40}', task['application'].get('commit', '')), 'Pin application commit')
    require(re.fullmatch(r'[0-9a-f]{7,40}', task['baseline_commit']), 'Pin baseline commit')
    require(task.get('status') in ['specified', 'in_progress', 'handed_off', 'awaiting_product_owner', 'blocked'],
            'Unknown status; technical workflow cannot record product acceptance')
    return task


def require_indexed_artifact(root, path, allowed_artifacts):
    if allowed_artifacts is not None:
        name = Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
        require(name in allowed_artifacts, 'Consumed artifact is not in index: ' + name)


def checked_artifact(root, task, path, allowed_artifacts=None):
    relative_file(path)
    require(path.startswith(task['evidence_location'].rstrip('/') + '/'), 'Evidence outside task evidence directory')
    target = Path(root) / path
    require_indexed_artifact(root, target, allowed_artifacts)
    require(not any(p.is_symlink() for p in [target, *target.parents] if p != Path(root).parent), 'Symlink evidence is unsupported')
    require(target.resolve().is_relative_to(Path(root).resolve()) and target.is_file(), 'Missing evidence file')
    return target.read_bytes()


def file_at(root, commit, path):
    relative_file(path)
    entries = git(root, 'ls-tree', '-z', commit, '--', path)
    if not entries:
        return None
    return git(root, 'show', commit + ':' + path)


def current_matches(root, commit, path):
    expected = file_at(root, commit, path)
    require(file_at(root, 'HEAD', path) == expected, 'Reviewed code/input differs from current HEAD: ' + path)
    target = Path(root) / path
    actual = target.read_bytes() if target.is_file() else None
    require(actual == expected, 'Working file differs from reviewed code/input: ' + path)


def verify_handoff(root, task_path, handoff_path, review_path, check_current=True, allowed_artifacts=None):
    for path in [task_path, handoff_path, review_path]:
        require_indexed_artifact(root, path, allowed_artifacts)
    task = validate_task(load(task_path))
    handoff, review = load(handoff_path), load(review_path)
    require(isinstance(handoff, dict) and isinstance(review, dict), 'Handoff and review must be objects')
    require(handoff.get('task_id') == task['id'] == review.get('task_id'), 'Task IDs disagree')
    require(handoff.get('implementer') == task['implementer'], 'Unexpected implementer')
    base = resolve_commit(root, handoff.get('implementation_base', ''))
    subject = resolve_commit(root, handoff.get('subject_commit', ''))
    baseline = resolve_commit(root, task['baseline_commit'])
    require(subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', baseline, base], capture_output=True).returncode == 0, 'Implementation base does not descend from task baseline')
    require(subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', base, subject], capture_output=True).returncode == 0, 'Subject does not descend from implementation base')
    paths = [p for p in git(root, 'diff', '--name-only', '-z', base, subject).decode().split('\0') if p]
    require(paths and set(paths).issubset(task['write_scope']), 'Committed change outside task write scope')
    require(set(handoff.get('changed_files', [])) == set(paths), 'Handoff changed files disagree with Git')
    require(review.get('reviewed_commit') == subject, 'Review refers to stale/wrong commit')
    require(review.get('reviewer') and review['reviewer'] != handoff['implementer'], 'Implementer cannot be independent reviewer')
    require(review.get('result') == 'PASS' and review.get('blocking_findings') == [], 'Review is not clear of blocking findings')
    require(review.get('limits'), 'Review must state its limits')
    inputs = handoff.get('input_hashes')
    require(isinstance(inputs, dict) and set(inputs) == set(task['bound_inputs']), 'Bound input hashes disagree with task')
    require(review.get('input_hashes') == inputs, 'Review input hashes disagree with handoff')
    for path, digest in inputs.items():
        data = file_at(root, subject, path)
        require(data is not None and hashlib.sha256(data).hexdigest() == digest, 'Input differs from reviewed subject: ' + path)
    if check_current:
        for path in set(paths) | set(inputs):
            current_matches(root, subject, path)
    records = handoff.get('checks', [])
    require(isinstance(records, list) and all(isinstance(r, dict) for r in records), 'Checks must be object records')
    require(len({r.get('name') for r in records}) == len(records), 'Duplicate check names')
    by_name = {r.get('name'): r for r in records}
    for name in task['checks']:
        require(name in by_name, 'Missing required check: ' + name)
        record = by_name[name]
        require(record.get('status') == 'PASS' and record.get('exit_code') == 0, 'Required check did not pass: ' + name)
        data = checked_artifact(root, task, record.get('evidence', ''), allowed_artifacts)
        require(hashlib.sha256(data).hexdigest() == record.get('sha256'), 'Evidence bytes changed after handoff: ' + name)
        artifact = json.loads(data.decode('utf-8-sig'))
        require(isinstance(artifact, dict), 'Evidence receipt must be an object')
        require(artifact.get('subject_commit') == subject, 'Evidence refers to a different code commit')
        require(artifact.get('status') == 'PASS' and artifact.get('exit_code') == 0, 'Receipt does not record a passing check')
    require(handoff.get('next_step') and handoff.get('open_issues') is not None, 'Missing handoff continuation')
    return {'status': 'READY_FOR_OWNER' if check_current else 'REVIEW_RECORD_VALID', 'task_id': task['id'], 'subject_commit': subject,
            'reviewer': review['reviewer'], 'changed_files': paths, 'bound_inputs': sorted(inputs),
            'limits': 'Version/scope/receipt consistency only; no identity attestation, test truth guarantee or product acceptance'}


def verify_task_set(root, task_paths, require_handoffs=False, allowed_artifacts=None):
    """Keep historical reviews valid; current bytes must match the latest reviewed owner per path."""
    owners = {}
    for task_path in task_paths:
        task = validate_task(load(task_path))
        handoff, review = task_path.parent / 'handoff.json', task_path.parent / 'review.json'
        if not (handoff.is_file() and review.is_file()):
            require(not require_handoffs, 'Task lacks handoff/review: ' + task['id'])
            continue
        result = verify_handoff(root, task_path, handoff, review, check_current=False, allowed_artifacts=allowed_artifacts)
        subject = result['subject_commit']
        require(subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', subject, 'HEAD'], capture_output=True).returncode == 0,
                'Reviewed subject is not integrated in HEAD: ' + task['id'])
        for path in result['changed_files'] + result['bound_inputs']:
            owners.setdefault(path, set()).add(subject)
    for path, commits in owners.items():
        latest = [candidate for candidate in commits if all(
            subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', earlier, candidate], capture_output=True).returncode == 0
            for earlier in commits)]
        require(len(latest) == 1, 'Ambiguous overlapping reviewed owners: ' + path)
        current_matches(root, latest[0], path)
    return {'tasks_validated': len(task_paths), 'current_review_bound_paths': len(owners)}


def render_brief(root, role, task_path):
    task = validate_task(load(task_path))
    roles = load(Path(root) / 'agents/codex/roles.json')
    require(role in roles, 'Unknown configured role')
    path = relative_file(roles[role]['brief'])
    return ('Read repository AGENTS.md first, then this role brief and the exact task. '
            'These are explicit Codex briefs, not auto-discovered Claude definitions.\n\n'
            + (Path(root) / path).read_text(encoding='utf-8') + '\n'
            + json.dumps(task, ensure_ascii=False, indent=2))


def main():
    # Windows pipes can default to cp1252; task briefs are Vietnamese UTF-8.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'brief', 'handoff'])
    parser.add_argument('--repo', default='.')
    parser.add_argument('--task', required=True)
    parser.add_argument('--role', choices=['coordinator', 'implementer', 'reviewer'])
    parser.add_argument('--handoff')
    parser.add_argument('--review')
    parser.add_argument('--historical', action='store_true', help='Validate a historical record, without declaring current HEAD ready')
    args = parser.parse_args()
    try:
        if args.action == 'validate':
            task = validate_task(load(args.task))
            print(json.dumps({'status': 'VALID', 'task_id': task['id']}))
        elif args.action == 'brief':
            require(args.role, '--role is required')
            print(render_brief(args.repo, args.role, args.task))
        else:
            require(args.handoff and args.review, '--handoff and --review are required')
            print(json.dumps(verify_handoff(args.repo, args.task, args.handoff, args.review, check_current=not args.historical), ensure_ascii=False))
        return 0
    except (WorkflowError, OSError, subprocess.SubprocessError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'BLOCKED', 'error': str(error)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
