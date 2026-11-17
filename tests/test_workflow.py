import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/agents'))

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools/agents' / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

workflow = module('workflow')
ownership = module('ownership')
repository_check = module('repository_check')


class ContentChecks(unittest.TestCase):
    def test_generated_secret_markers_and_credentials_are_blocked(self):
        cases = [
            ('ghp_' + 'x' * 30, 'github_token'),
            ('-----BEGIN ' + 'PRIVATE KEY-----', 'private_key'),
            ('https://' + 'fixture:placeholder@invalid.test/', 'credential_url'),
        ]
        for value, expected in cases:
            with self.subTest(check=expected):
                self.assertIn(expected, repository_check.scan_file('fixture.md', value.encode()))

    def test_sensitive_data_files_block_and_normal_task_is_clean(self):
        self.assertIn('sensitive_file_type', repository_check.scan_file('.env', b'fixture'))
        self.assertIn('sensitive_file_type', repository_check.scan_file('.env.production', b'fixture'))
        self.assertIn('sensitive_file_type', repository_check.scan_file('nested/.ENV.local', b'fixture'))
        self.assertEqual(repository_check.scan_file('.env.example', b'PUBLIC_SETTING=placeholder'), [])
        self.assertIn('sensitive_file_type', repository_check.scan_file('fixture.dump', b'fixture'))
        self.assertEqual(repository_check.scan_file('task.json', b'{"status":"NOT_RUN"}'), [])


class Contracts(unittest.TestCase):
    def setUp(self):
        self.task = workflow.load(ROOT / 'tasks/AGENT-001/task.json')

    def test_real_task_has_required_context(self):
        self.assertEqual(workflow.validate_task(self.task)['id'], 'AGENT-001')

    def test_vietnamese_brief_survives_windows_pipe_encoding(self):
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'cp1252'
        result = subprocess.run(
            [sys.executable, '-B', str(ROOT / 'tools/agents/workflow.py'), 'brief',
             '--repo', str(ROOT), '--task', str(ROOT / 'tasks/AGENT-001/task.json'), '--role', 'reviewer'],
            env=env, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Ngăn', result.stdout)

    def test_missing_acceptance_and_done_claim_block(self):
        for field in ['goal', 'acceptance', 'permissions', 'stop_conditions', 'receiver']:
            value = copy.deepcopy(self.task)
            value.pop(field)
            with self.subTest(field=field), self.assertRaises(workflow.WorkflowError):
                workflow.validate_task(value)
        for value in ['Done', 'done', 'accepted', 'unknown']:
            self.task['status'] = value
            with self.subTest(status=value), self.assertRaises(workflow.WorkflowError):
                workflow.validate_task(self.task)

    def test_escape_credentials_and_ambiguous_scope_block(self):
        for path in ['../x', '/tmp/x', 'C:/x', r'a\b', '.GIT/config', '.env', 'a//b', '**/*.py']:
            with self.subTest(path=path), self.assertRaises(workflow.WorkflowError):
                workflow.relative_file(path)


class GitFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.git('init', '-b', 'fixture')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@localhost')
        self.git('config', 'core.autocrlf', 'false')
        self.write('code.py', 'print(1)\n')
        self.write('profile.json', '{"revision":1}\n')
        self.git('add', '--', 'code.py', 'profile.json')
        self.git('commit', '-m', 'fixture base')
        self.base = self.git('rev-parse', 'HEAD').strip()

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True, stderr=subprocess.PIPE)

    def write(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value, encoding='utf-8')


class Handoffs(GitFixture):
    def setUp(self):
        super().setUp()
        self.write('code.py', 'print(2)\n')
        self.git('add', '--', 'code.py')
        self.git('commit', '-m', 'fixture subject')
        self.subject = self.git('rev-parse', 'HEAD').strip()
        self.task = workflow.load(ROOT / 'tasks/AGENT-001/task.json')
        self.task.update(baseline_commit=self.base, write_scope=['code.py'], bound_inputs=['profile.json'], checks=['unit'])
        self.receipt = {'subject_commit': self.subject, 'status': 'PASS', 'exit_code': 0}
        self.evidence = 'tasks/AGENT-001/evidence/unit.json'
        self.write(self.evidence, json.dumps(self.receipt))
        digest = hashlib.sha256((self.root / self.evidence).read_bytes()).hexdigest()
        self.handoff = {'task_id': 'AGENT-001', 'implementer': self.task['implementer'],
                        'implementation_base': self.base, 'subject_commit': self.subject,
                        'changed_files': ['code.py'], 'next_step': 'owner review', 'open_issues': [],
                        'checks': [{'name': 'unit', 'status': 'PASS', 'exit_code': 0,
                                    'evidence': self.evidence, 'sha256': digest}]}
        self.handoff['input_hashes'] = {'profile.json': hashlib.sha256((self.root / 'profile.json').read_bytes()).hexdigest()}
        self.review = {'task_id': 'AGENT-001', 'reviewer': 'different-reviewer',
                       'reviewed_commit': self.subject, 'result': 'PASS', 'blocking_findings': [],
                       'limits': ['Synthetic receipt does not attest execution truth']}
        self.review['input_hashes'] = self.handoff['input_hashes'].copy()

    def verify(self):
        for name, value in [('task.json', self.task), ('handoff.json', self.handoff), ('review.json', self.review)]:
            self.write(name, json.dumps(value))
        return workflow.verify_handoff(self.root, self.root / 'task.json', self.root / 'handoff.json', self.root / 'review.json')

    def test_consistent_handoff_ready_not_owner_accepted(self):
        self.assertEqual(self.verify()['status'], 'READY_FOR_OWNER')

    def test_stale_review_blocked(self):
        self.review['reviewed_commit'] = self.base
        with self.assertRaises(workflow.WorkflowError):
            self.verify()

    def test_self_review_and_blocking_finding_blocked(self):
        self.review['reviewer'] = self.handoff['implementer']
        with self.assertRaises(workflow.WorkflowError):
            self.verify()
        self.review['reviewer'] = 'different-reviewer'
        self.review['blocking_findings'] = ['reproducible defect']
        with self.assertRaises(workflow.WorkflowError):
            self.verify()

    def test_scope_violation_blocked(self):
        self.task['write_scope'] = ['another.py']
        with self.assertRaises(workflow.WorkflowError):
            self.verify()

    def test_changed_evidence_blocked(self):
        self.write(self.evidence, '{"status":"PASS","changed":true}')
        with self.assertRaises(workflow.WorkflowError):
            self.verify()

    def test_not_run_or_failing_test_blocked(self):
        for value in ['NOT_RUN', 'FAIL']:
            self.handoff['checks'][0]['status'] = value
            with self.subTest(value=value), self.assertRaises(workflow.WorkflowError):
                self.verify()

    def test_post_review_code_change_blocked(self):
        self.write('code.py', 'print(3)\n')
        with self.assertRaises(workflow.WorkflowError):
            self.verify()

    def test_changed_bound_profile_requires_new_review(self):
        self.write('profile.json', '{"revision":2}\n')
        self.git('add', '--', 'profile.json')
        self.git('commit', '-m', 'unreviewed profile change')
        with self.assertRaises(workflow.WorkflowError):
            self.verify()

    def test_historical_review_and_later_reviewed_edit_can_coexist(self):
        self.verify()
        self.write('code.py', 'print(3)\n')
        self.git('add', '--', 'code.py')
        self.git('commit', '-m', 'second task subject')
        subject2 = self.git('rev-parse', 'HEAD').strip()
        task2 = copy.deepcopy(self.task)
        task2.update(id='AGENT-002', evidence_location='tasks/AGENT-002/evidence/')
        handoff2 = copy.deepcopy(self.handoff)
        handoff2.update(task_id='AGENT-002', implementation_base=self.subject, subject_commit=subject2)
        review2 = copy.deepcopy(self.review)
        review2.update(task_id='AGENT-002', reviewed_commit=subject2)
        path2 = 'tasks/AGENT-002/evidence/unit.json'
        self.write(path2, json.dumps({'subject_commit': subject2, 'status': 'PASS', 'exit_code': 0}))
        handoff2['checks'][0].update(evidence=path2, sha256=hashlib.sha256((self.root / path2).read_bytes()).hexdigest())
        for name, data in [('task.json', task2), ('handoff.json', handoff2), ('review.json', review2)]:
            self.write('second/' + name, json.dumps(data))
        paths = [self.root / 'task.json', self.root / 'second/task.json']
        result = workflow.verify_task_set(self.root, paths, require_handoffs=True)
        self.assertEqual(result['tasks_validated'], 2)
        historical = workflow.verify_handoff(self.root, paths[0], self.root / 'handoff.json', self.root / 'review.json', check_current=False)
        self.assertEqual(historical['status'], 'REVIEW_RECORD_VALID')
        self.write('code.py', 'print(4)\n')
        with self.assertRaises(workflow.WorkflowError):
            workflow.verify_task_set(self.root, paths, require_handoffs=True)


class IndexSnapshot(GitFixture):
    def test_staged_deletion_with_working_file_remaining_is_blocked(self):
        self.git('rm', '--cached', '--', 'code.py')
        paths, findings = repository_check.index_snapshot(self.root)
        self.assertNotIn('code.py', paths)
        self.assertIn({'path': 'code.py', 'check': 'staged_deleted_but_working_exists'}, findings)

    def test_unstaged_working_code_cannot_supply_passing_tests_for_other_index(self):
        self.write('code.py', 'print(999)\n')
        _, findings = repository_check.index_snapshot(self.root)
        self.assertIn({'path': 'code.py', 'check': 'staged_working_mismatch'}, findings)


class Claims(GitFixture):
    @unittest.skipUnless(os.name == 'nt', 'Windows case-insensitive file claims')
    def test_windows_case_alias_cannot_claim_same_file_twice(self):
        ownership.claim(self.root, 'first', ['file:code.py'])
        with self.assertRaises(ownership.ClaimError):
            ownership.claim(self.root, 'second', ['file:CODE.py'])
        ownership.release(self.root, 'first', ['file:code.py'])

    def test_conflict_wrong_release_and_parallel_runtime_block(self):
        resources = ['file:code.py', 'runtime:shared-lab']
        ownership.claim(self.root, 'first', resources)
        with self.assertRaises(ownership.ClaimError):
            ownership.claim(self.root, 'second', ['runtime:shared-lab'])
        with self.assertRaises(ownership.ClaimError):
            ownership.release(self.root, 'second', resources)
        with self.assertRaises(ownership.ClaimError):
            ownership.release(self.root, 'first', ['file:code.py', 'file:code.py'])
        self.assertEqual(len(ownership.status(self.root)), 2)
        ownership.release(self.root, 'first', resources)
        self.assertEqual(ownership.status(self.root), [])

    def test_atomic_competing_claims(self):
        def attempt(owner):
            try:
                ownership.claim(self.root, owner, ['file:code.py'])
                return owner
            except ownership.ClaimError:
                return None
        with ThreadPoolExecutor(max_workers=2) as pool:
            winners = [x for x in pool.map(attempt, ['one', 'two']) if x]
        self.assertEqual(len(winners), 1)
        ownership.release(self.root, winners[0], ['file:code.py'])

    def test_claims_shared_between_git_worktrees(self):
        other = Path(self.temp.name) / 'other'
        self.git('worktree', 'add', '-b', 'other', str(other), self.base)
        ownership.claim(self.root, 'first', ['file:code.py'])
        with self.assertRaises(ownership.ClaimError):
            ownership.claim(other, 'second', ['file:code.py'])
        ownership.release(other, 'first', ['file:code.py'])

    def test_partial_acquisition_rolls_back_only_own_claims(self):
        ownership.claim(self.root, 'first', ['file:z.py'])
        with self.assertRaises(ownership.ClaimError):
            ownership.claim(self.root, 'second', ['file:a.py', 'file:z.py'])
        self.assertEqual(ownership.status(self.root), [{'owner': 'first', 'resource': 'file:z.py'}])
        ownership.release(self.root, 'first', ['file:z.py'])


if __name__ == '__main__':
    unittest.main()
