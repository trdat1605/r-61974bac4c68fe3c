"""Check product records and PR traceability. Consistency is not product acceptance."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPRedirectHandler


LIMITS = ('Consistency only: no reviewer identity or execution-truth attestation, '
          'product acceptance, security certification or merge enforcement')
NAME = r'[A-Za-z0-9_.-]+'
SHA = r'[0-9a-f]{40}'


class ProductError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ProductError(message)


def text_field(value, label):
    require(isinstance(value, str) and value.strip(), 'Missing ' + label)
    return value


def repository(value):
    """Only public GitHub URL syntax; never fetch a caller-supplied URL."""
    require(isinstance(value, str), 'Invalid repository URL')
    match = re.fullmatch(r'https://github\.com/(' + NAME + '/' + NAME + r')(?:/)?', value)
    require(match is not None, 'Invalid credential-free GitHub repository URL')
    slug = match[1]
    if slug.endswith('.git'):
        slug = slug[:-4]
    require(all(part not in ('', '.', '..') for part in slug.split('/')), 'Invalid repository name')
    return slug.casefold()


def issue_identity(value):
    require(isinstance(value, str), 'Invalid issue URL')
    match = re.fullmatch(r'https://github\.com/(' + NAME + '/' + NAME + r')/issues/([1-9][0-9]*)', value)
    require(match is not None, 'Expected full GitHub issue URL, not a pull request')
    return repository('https://github.com/' + match[1]), int(match[2])


def relative_path(value):
    require(isinstance(value, str) and value, 'Missing artifact path')
    require('\\' not in value and ':' not in value and
            not any(part in ('', '.', '..', '.git') for part in value.split('/')) and
            not any(c in value for c in '*?[]'), 'Unsafe artifact path')
    require(not any(part.casefold() == '.env' or part.casefold().startswith('.env.')
                    for part in value.split('/')), 'Secret artifact path')
    return value


def local_file(root, name):
    target = Path(root) / relative_path(name)
    require(target.resolve().is_relative_to(Path(root).resolve()), 'Artifact escapes checkout')
    require(not any(p.is_symlink() for p in [target, *target.parents]
                    if p != Path(root).resolve().parent), 'Symlink artifact is unsupported')
    require(target.is_file(), 'Missing artifact')
    return target


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def validate_plan(record):
    require(isinstance(record, dict) and record.get('schema_version') == 1, 'Unsupported product schema')
    require(isinstance(record.get('task_id'), str) and re.fullmatch(NAME, record['task_id']) and
            record['task_id'] not in ('.', '..'), 'Invalid task ID')
    issue_identity(record.get('issue'))
    source = record.get('source')
    require(isinstance(source, dict), 'Missing source')
    repository(source.get('repository'))
    require(isinstance(source.get('base_commit'), str) and re.fullmatch(SHA, source['base_commit']), 'Pin source base commit')
    criteria = record.get('criteria')
    require(isinstance(criteria, list) and criteria, 'Missing acceptance criteria')
    ids = set()
    for criterion in criteria:
        require(isinstance(criterion, dict), 'Invalid acceptance criterion')
        cid = criterion.get('id')
        require(isinstance(cid, str) and re.fullmatch(NAME, cid) and cid not in ids, 'Invalid or duplicate acceptance ID')
        ids.add(cid)
        text_field(criterion.get('description'), 'acceptance description')
        checks = criterion.get('checks')
        require(isinstance(checks, list) and checks and all(isinstance(c, str) and re.fullmatch(NAME, c) for c in checks), 'Missing criterion checks')
        require(len(checks) == len(set(checks)), 'Duplicate criterion checks')
    for key in ('environment', 'risk', 'rollback'):
        text_field(record.get(key), key)
    return {'status': 'PLAN_VALID', 'task_id': record['task_id'], 'limits': LIMITS}


def git_environment():
    # A foreign checkout must never inherit hook index/dir/config overrides.
    # No network Git command is used here, so omit all Git-specific overrides.
    return {key: value for key, value in os.environ.items() if not key.upper().startswith('GIT_')}


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], env=git_environment(),
                            capture_output=True, text=True, encoding='utf-8')
    require(result.returncode == 0, 'Source Git command failed')
    return result.stdout.strip()


def committed_artifact(root, name):
    """Handoff evidence must survive a fresh checkout, with identical bytes."""
    data = local_file(root, name).read_bytes()
    result = subprocess.run(['git', '-C', str(root), 'show', 'HEAD:' + name],
                            env=git_environment(), capture_output=True)
    require(result.returncode == 0, 'Evidence is not committed at control HEAD')
    require(result.stdout == data, 'Evidence differs from committed control HEAD')
    return data


def remote_identity(value):
    if value.startswith('git@github.com:'):
        value = 'https://github.com/' + value[len('git@github.com:'):]
    return repository(value)


def require_full_index(root):
    """Status cannot attest files whose index flags suppress working-tree checks."""
    # git-ls-files -v documents lowercase tags for assume-unchanged and S for
    # skip-worktree. NUL boundaries prevent unusual filenames becoming tags.
    for entry in git(root, 'ls-files', '-v', '-z').split('\0'):
        if entry:
            require(not entry[0].islower() and entry[0] != 'S',
                    'Application index has assume-unchanged or skip-worktree files')
    for key in ('core.sparseCheckout', 'index.sparse'):
        require(git(root, 'config', '--type=bool', '--default=false', '--get', key) == 'false',
                'Sparse application checkouts are unsupported')


def verify(record, source_repo, root):
    validate_plan(record)
    require(source_repo is not None, 'verify requires --source-repo')
    source_repo, root = Path(source_repo).resolve(), Path(root).resolve()
    require(source_repo != root, 'Application source must be a separate checkout')
    require(Path(git(source_repo, 'rev-parse', '--show-toplevel')).resolve() == source_repo, 'Use the application checkout root')
    source = record['source']
    require(repository(source['repository']) != remote_identity(git(root, 'remote', 'get-url', 'origin')),
            'Application repository cannot be the control repository')
    require(remote_identity(git(source_repo, 'remote', 'get-url', 'origin')) == repository(source['repository']), 'Application repository identity mismatch')
    implementation = record.get('implementation')
    require(isinstance(implementation, dict), 'Missing implementation')
    subject = implementation.get('subject_commit')
    require(isinstance(subject, str) and re.fullmatch(SHA, subject), 'Pin application subject commit')
    implementer = text_field(implementation.get('implementer'), 'implementer')
    for commit in (source['base_commit'], subject):
        require(git(source_repo, 'rev-parse', '--verify', commit + '^{commit}') == commit, 'Application commit mismatch')
    git(source_repo, 'merge-base', '--is-ancestor', source['base_commit'], subject)
    require(git(source_repo, 'rev-parse', 'HEAD') == subject, 'Application checkout HEAD differs from subject')
    require_full_index(source_repo)
    require(not git(source_repo, 'status', '--porcelain', '--untracked-files=no'), 'Application tracked files are dirty')
    review = record.get('review')
    require(isinstance(review, dict), 'Missing application review')
    reviewer = text_field(review.get('reviewer'), 'reviewer')
    require(reviewer != implementer, 'Implementer cannot independently review')
    require(review.get('reviewed_commit') == subject and review.get('result') == 'PASS' and
            review.get('blocking_findings') == [], 'Application review is stale or blocked')
    text_field(review.get('limits'), 'review limits')
    records = record.get('checks')
    require(isinstance(records, list) and all(isinstance(c, dict) for c in records), 'Missing check records')
    names = [c.get('name') for c in records]
    require(all(isinstance(n, str) for n in names) and len(names) == len(set(names)), 'Invalid or duplicate check records')
    required = {name for criterion in record['criteria'] for name in criterion['checks']}
    require(set(names) == required, 'Required check coverage mismatch')
    by_name = {c['name']: c for c in records}
    for criterion in record['criteria']:
        for name in criterion['checks']:
            check = by_name[name]
            require(check.get('status') == 'PASS' and check.get('exit_code') == 0, 'Required check is FAIL or NOT_RUN')
            evidence = check.get('evidence')
            relative_path(evidence)
            require(evidence.startswith('tasks/' + record['task_id'] + '/evidence/'), 'Evidence outside task')
            data = committed_artifact(root, evidence)
            require(hashlib.sha256(data).hexdigest() == check.get('sha256'), 'Evidence hash mismatch')
            receipt = json.loads(data.decode('utf-8-sig'))
            require(isinstance(receipt, dict), 'Invalid check receipt')
            require(repository(receipt.get('source_repository')) == repository(source['repository']), 'Receipt application repository mismatch')
            require(receipt.get('subject_commit') == subject, 'Receipt application subject mismatch')
            require(receipt.get('status') == 'PASS' and receipt.get('exit_code') == 0, 'Receipt is FAIL or NOT_RUN')
            text_field(receipt.get('command'), 'check command or steps')
            require(isinstance(receipt.get('criteria'), list) and criterion['id'] in receipt['criteria'], 'Missing criterion evidence')
    return {'status': 'PRODUCT_RECORD_VERIFIED', 'task_id': record['task_id'],
            'subject_commit': subject, 'mode': 'current-checkout', 'limits': LIMITS}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_issue(slug, number, token, opener=None):
    require(bool(token), 'Read-only issue check requires GH_TOKEN or GITHUB_TOKEN')
    # slug has passed the GitHub-only parser. Redirects cannot forward credentials.
    request = Request('https://api.github.com/repos/' + slug + '/issues/' + str(number),
                      headers={'Accept': 'application/vnd.github+json',
                               'Authorization': 'Bearer ' + token,
                               'X-GitHub-Api-Version': '2022-11-28'}, method='GET')
    try:
        with (opener or build_opener(NoRedirect())).open(request, timeout=20) as response:
            data = json.load(response)
    except HTTPError as error:
        raise ProductError('GitHub issue API denied or unavailable (HTTP ' + str(error.code) + ')') from None
    except (URLError, OSError, ValueError):
        raise ProductError('GitHub issue API unavailable or invalid response') from None
    require(isinstance(data, dict) and 'pull_request' not in data, 'Issue reference is a pull request or invalid object')
    require(data.get('number') == number, 'GitHub issue number mismatch')
    require(issue_identity(data.get('html_url')) == (slug, number), 'GitHub issue repository mismatch')
    return True


def check_pr(event, expected_repository, root, token, opener=None):
    expected = repository('https://github.com/' + expected_repository)
    require(isinstance(event, dict), 'Invalid GitHub event')
    repo = event.get('repository')
    require(isinstance(repo, dict) and isinstance(repo.get('full_name'), str) and
            repo['full_name'].casefold() == expected, 'PR event repository mismatch')
    pr = event.get('pull_request')
    require(isinstance(pr, dict), 'Expected a pull_request event')
    body = pr.get('body')
    require(isinstance(body, str), 'Missing PR body')
    task_matches = re.findall(r'^Task: (tasks/(' + NAME + r')/task\.json)\s*$', body, re.MULTILINE)
    require(len(task_matches) == 1, 'PR requires one Task: tasks/ID/task.json line')
    task_path, task_id = task_matches[0]
    task = load(local_file(root, task_path))
    require(isinstance(task, dict) and task.get('id') == task_id, 'PR task ID mismatch')
    require(repository(task.get('repository')) == expected, 'PR task repository mismatch')
    task_issue = issue_identity(task.get('issue_url'))
    require(task_issue[0] == expected, 'PR task issue repository mismatch')
    issue_urls = re.findall(r'https://github\.com/' + NAME + '/' + NAME + r'/issues/[1-9][0-9]*(?![0-9])[^\s<>)]*', body)
    require(issue_urls, 'PR requires full GitHub issue URL')
    issues = set()
    for url in issue_urls:
        slug, number = issue_identity(url)
        require(slug == expected, 'PR issue must belong to expected repository')
        issues.add((slug, number))
    require(task_issue in issues, 'PR body does not reference the task issue')
    for slug, number in sorted(issues):
        read_issue(slug, number, token, opener)
    return {'status': 'PR_TRACEABILITY_VALID', 'task_id': task_id,
            'issues_checked': len(issues), 'limits': LIMITS}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ProductError('Invalid command arguments; see --help')


def main(argv=None):
    parser = Parser(description=__doc__)
    parser.add_argument('mode', choices=['plan', 'verify', 'pr'])
    parser.add_argument('--record')
    parser.add_argument('--source-repo')
    parser.add_argument('--repo', default='.')
    parser.add_argument('--event')
    parser.add_argument('--expected-repository')
    try:
        args = parser.parse_args(argv)
        if args.mode == 'pr':
            event = args.event or os.environ.get('GITHUB_EVENT_PATH')
            require(event and args.expected_repository, 'PR mode requires event and expected repository')
            result = check_pr(load(event), args.expected_repository, args.repo,
                              os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN'))
        else:
            require(args.record, 'Plan and verify require --record')
            record = load(args.record)
            result = validate_plan(record) if args.mode == 'plan' else verify(record, args.source_repo, args.repo)
        print(json.dumps(result))
        return 0
    except ProductError as error:
        print(json.dumps({'status': 'BLOCKED', 'error': str(error), 'limits': LIMITS}))
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({'status': 'BLOCKED', 'error': 'Unreadable or malformed input', 'limits': LIMITS}))
    return 2


if __name__ == '__main__':
    sys.exit(main())
