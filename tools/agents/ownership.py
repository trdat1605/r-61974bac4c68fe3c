"""Cooperative atomic claims across Git worktrees; not an OS permission boundary."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


class ClaimError(ValueError):
    pass


def common_dir(root):
    value = subprocess.check_output(
        ['git', '-C', str(root), 'rev-parse', '--path-format=absolute', '--git-common-dir'],
        text=True, stderr=subprocess.PIPE).strip()
    return Path(value)


def validate_resource(resource):
    if resource.startswith('file:'):
        path = resource[5:]
        parts = path.split('/')
        if not path or chr(92) in path or ':' in path or any(p.casefold() in ('', '.', '..', '.git') for p in parts):
            raise ClaimError('File resource must be a normalized repository-relative file path')
        if any(c in path for c in '*?[]'):
            raise ClaimError('Claims use exact file paths; subtree/glob claims are unsupported')
    elif not re.fullmatch(r'runtime:[A-Za-z0-9_.-]+', resource):
        raise ClaimError('Expected file:<path> or runtime:<project>')


def resource_key(resource):
    # Windows file paths are case-insensitive; task/runtime IDs remain explicit.
    import os
    value = resource.casefold() if os.name == 'nt' and resource.startswith('file:') else resource
    return hashlib.sha256(value.encode()).hexdigest()


def claim(root, owner, resources):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', owner):
        raise ClaimError('Invalid owner/task ID')
    if not resources or len(resources) != len(set(resources)):
        raise ClaimError('Provide unique nonempty resources')
    for resource in resources:
        validate_resource(resource)
    base = common_dir(root) / 'agent-claims'
    base.mkdir(exist_ok=True)
    acquired = []
    try:
        for resource in sorted(resources):
            directory = base / resource_key(resource)
            try:
                directory.mkdir()
            except FileExistsError:
                raise ClaimError('Resource already claimed: ' + resource)
            acquired.append(directory)
            (directory / 'claim.json').write_text(json.dumps({'owner': owner, 'resource': resource}), encoding='utf-8')
    except Exception:
        for directory in reversed(acquired):
            record = directory / 'claim.json'
            if record.exists():
                record.unlink()
            directory.rmdir()
        raise
    return {'owner': owner, 'resources': sorted(resources), 'status': 'CLAIMED'}


def release(root, owner, resources):
    if not resources or len(resources) != len(set(resources)):
        raise ClaimError('Provide unique nonempty resources')
    base = common_dir(root) / 'agent-claims'
    records = []
    for resource in resources:
        validate_resource(resource)
        directory = base / resource_key(resource)
        record = directory / 'claim.json'
        if not record.exists():
            raise ClaimError('Missing or incomplete claim; coordinator must inspect: ' + resource)
        value = json.loads(record.read_text(encoding='utf-8'))
        if value != {'owner': owner, 'resource': resource}:
            raise ClaimError('Claim belongs to a different owner: ' + resource)
        records.append((directory, record))
    for directory, record in records:
        record.unlink()
        directory.rmdir()
    return {'owner': owner, 'resources': resources, 'status': 'RELEASED'}


def status(root):
    base = common_dir(root) / 'agent-claims'
    return [json.loads(p.read_text(encoding='utf-8')) for p in sorted(base.glob('*/claim.json'))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['claim', 'release', 'status'])
    parser.add_argument('--repo', default='.')
    parser.add_argument('--owner')
    parser.add_argument('--resource', action='append', default=[])
    args = parser.parse_args()
    try:
        if args.action == 'status':
            result = status(args.repo)
        else:
            if not args.owner:
                raise ClaimError('--owner is required')
            result = (claim if args.action == 'claim' else release)(args.repo, args.owner, args.resource)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ClaimError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(json.dumps({'status': 'BLOCKED', 'error': str(error)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
