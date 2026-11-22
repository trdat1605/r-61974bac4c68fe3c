import copy
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/agents'))
import product_check as product


def plan():
    return {'schema_version': 1, 'task_id': 'PRODUCT-001',
            'issue': 'https://github.com/example/control/issues/7',
            'source': {'repository': 'https://github.com/example/app', 'base_commit': 'a' * 40},
            'criteria': [{'id': 'AC-1', 'description': 'Expected user behaviour', 'checks': ['focused']}],
            'environment': 'Isolated test environment', 'risk': 'Limited to one view',
            'rollback': 'Revert the application commit'}


class Plans(unittest.TestCase):
    def test_plan_valid_is_not_product_verified(self):
        self.assertEqual(product.validate_plan(plan())['status'], 'PLAN_VALID')

    def test_missing_issue_pull_url_credentials_and_missing_criteria_block(self):
        for key, value in [('issue', None), ('issue', 'https://github.com/example/control/pull/7'),
                           ('issue', 'https://token@github.com/example/control/issues/7'),
                           ('criteria', []), ('environment', ''), ('risk', ''), ('rollback', '')]:
            record = plan()
            record[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(product.ProductError):
                product.validate_plan(record)

    def test_duplicate_criteria_and_missing_check_block(self):
        record = plan()
        record['criteria'] *= 2
        with self.assertRaises(product.ProductError):
            product.validate_plan(record)
        record = plan()
        record['criteria'][0]['checks'] = []
        with self.assertRaises(product.ProductError):
            product.validate_plan(record)

    def test_cli_errors_are_sanitized_json(self):
        for args in [['verify'], ['unknown'], ['plan', '--record', 'secret-input-does-not-exist']]:
            output = io.StringIO()
            with patch('sys.stdout', output):
                code = product.main(args)
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(output.getvalue())['status'], 'BLOCKED')
            self.assertNotIn('secret-input', output.getvalue())


class SourceFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.control = Path(self.temp.name) / 'control'
        self.app = Path(self.temp.name) / 'app'
        for root, remote in [(self.control, 'control'), (self.app, 'app')]:
            root.mkdir()
            self.git(root, 'init', '-b', 'fixture')
            self.git(root, 'config', 'user.name', 'Fixture')
            self.git(root, 'config', 'user.email', 'fixture@localhost')
            self.git(root, 'config', 'core.autocrlf', 'false')
            self.git(root, 'remote', 'add', 'origin', 'https://github.com/example/' + remote + '.git')
            (root / 'code.txt').write_text('before\n', encoding='utf-8')
            self.git(root, 'add', '--', 'code.txt')
            self.git(root, 'commit', '-m', 'base')
        self.base = self.git(self.app, 'rev-parse', 'HEAD')
        (self.app / 'code.txt').write_text('after\n', encoding='utf-8')
        self.git(self.app, 'add', '--', 'code.txt')
        self.git(self.app, 'commit', '-m', 'subject')
        self.subject = self.git(self.app, 'rev-parse', 'HEAD')
        self.record = plan()
        self.record['source']['base_commit'] = self.base
        self.record['implementation'] = {'subject_commit': self.subject, 'implementer': 'worker'}
        self.record['review'] = {'reviewer': 'reviewer', 'reviewed_commit': self.subject,
                                 'result': 'PASS', 'blocking_findings': [], 'limits': 'Fixture only'}
        self.receipt = {'source_repository': 'https://github.com/example/app',
                        'subject_commit': self.subject, 'command': 'synthetic fixture; no app test run',
                        'criteria': ['AC-1'], 'status': 'PASS', 'exit_code': 0}
        self.evidence = 'tasks/PRODUCT-001/evidence/focused.json'
        self.path = self.control / self.evidence
        self.path.parent.mkdir(parents=True)
        self.record['checks'] = [{'name': 'focused', 'status': 'PASS', 'exit_code': 0,
                                  'evidence': self.evidence}]
        self.save_receipt()
        self.commit_receipt()

    def git(self, root, *args):
        return subprocess.check_output(['git', '-C', str(root), *args], env=product.git_environment(),
                                       text=True, stderr=subprocess.PIPE).strip()

    def save_receipt(self):
        data = json.dumps(self.receipt).encode()
        self.path.write_bytes(data)
        self.record['checks'][0]['sha256'] = hashlib.sha256(data).hexdigest()

    def commit_receipt(self):
        self.git(self.control, 'add', '--', self.evidence)
        self.git(self.control, 'commit', '--allow-empty', '-m', 'fixture evidence')

    def verify(self):
        return product.verify(self.record, self.app, self.control)

    def test_real_git_fixture_positive_is_consistency_only(self):
        result = self.verify()
        self.assertEqual(result['status'], 'PRODUCT_RECORD_VERIFIED')
        self.assertEqual(result['subject_commit'], self.subject)
        self.assertEqual(result['mode'], 'current-checkout')

    def test_source_checkout_required_and_control_checkout_rejected(self):
        for source in (None, self.control):
            with self.subTest(source=source), self.assertRaises(product.ProductError):
                product.verify(self.record, source, self.control)

    def test_wrong_remote_and_credentials_block(self):
        for remote in ('https://github.com/example/other', 'https://token@github.com/example/app'):
            self.git(self.app, 'remote', 'set-url', 'origin', remote)
            with self.subTest(remote=remote), self.assertRaises(product.ProductError):
                self.verify()

    def test_separate_control_clone_cannot_masquerade_as_app(self):
        self.record['source']['repository'] = 'https://github.com/example/control'
        self.git(self.app, 'remote', 'set-url', 'origin', 'https://github.com/example/control')
        with self.assertRaises(product.ProductError):
            self.verify()

    def test_stale_checkout_dirty_tracked_source_and_non_ancestor_block(self):
        self.git(self.app, 'checkout', '--detach', self.base)
        with self.assertRaises(product.ProductError):
            self.verify()
        self.git(self.app, 'checkout', '--detach', self.subject)
        (self.app / 'code.txt').write_text('unreviewed\n', encoding='utf-8')
        with self.assertRaises(product.ProductError):
            self.verify()
        self.git(self.app, 'checkout', '--', 'code.txt')
        self.git(self.app, 'checkout', '--orphan', 'unrelated')
        self.git(self.app, 'commit', '-m', 'unrelated')
        self.record['source']['base_commit'] = self.git(self.app, 'rev-parse', 'HEAD')
        self.git(self.app, 'checkout', '--detach', self.subject)
        with self.assertRaises(product.ProductError):
            self.verify()

    def test_missing_criteria_check_evidence_and_modified_bytes_block(self):
        original = copy.deepcopy(self.record)
        self.record['checks'] = []
        with self.assertRaises(product.ProductError):
            self.verify()
        self.record = original
        self.receipt['criteria'] = []
        self.save_receipt()
        self.commit_receipt()
        with self.assertRaises(product.ProductError):
            self.verify()
        self.receipt['criteria'] = ['AC-1']
        self.save_receipt()
        self.commit_receipt()
        self.path.write_text('{}', encoding='utf-8')
        with self.assertRaises(product.ProductError):
            self.verify()

    def test_receipt_wrong_repo_control_subject_missing_command_and_not_run_block(self):
        for key, value in [('source_repository', 'https://github.com/example/control'),
                           ('subject_commit', self.git(self.control, 'rev-parse', 'HEAD')),
                           ('command', ''), ('status', 'NOT_RUN'), ('status', 'FAIL')]:
            previous = self.receipt[key]
            self.receipt[key] = value
            self.save_receipt()
            self.commit_receipt()
            with self.subTest(key=key, value=value), self.assertRaises(product.ProductError):
                self.verify()
            self.receipt[key] = previous

    def test_untracked_and_working_modified_receipts_block(self):
        self.git(self.control, 'rm', '--cached', '--', self.evidence)
        self.git(self.control, 'commit', '-m', 'fixture untracked evidence')
        with self.assertRaisesRegex(product.ProductError, 'not committed'):
            self.verify()
        self.commit_receipt()
        self.receipt['command'] = 'changed command'
        self.save_receipt()
        with self.assertRaisesRegex(product.ProductError, 'differs from committed'):
            self.verify()

    def test_required_check_fail_not_run_and_escaping_evidence_block(self):
        for key, value in [('status', 'FAIL'), ('status', 'NOT_RUN'),
                           ('evidence', '../receipt.json'), ('evidence', 'tasks/OTHER/evidence/x.json')]:
            previous = self.record['checks'][0][key]
            self.record['checks'][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(product.ProductError):
                self.verify()
            self.record['checks'][0][key] = previous

    def test_stale_self_and_blocked_reviews_block(self):
        for key, value in [('reviewer', 'worker'), ('reviewed_commit', self.base),
                           ('blocking_findings', ['defect']), ('limits', '')]:
            previous = self.record['review'][key]
            self.record['review'][key] = value
            with self.subTest(key=key), self.assertRaises(product.ProductError):
                self.verify()
            self.record['review'][key] = previous

    def test_git_hook_environment_cannot_redirect_source_commands(self):
        before = (self.control / '.git/config').read_bytes()
        # patch.dict(os.environ) clears/restores native Windows variables. Empty
        # values can disappear from native child environments while remaining in
        # Python's mapping. Replace only the mapping read by our explicit-env helper.
        probe = [sys.executable, '-B', '-c', 'import os,json; print(json.dumps(dict(os.environ)))']
        native_before = json.loads(subprocess.check_output(probe, text=True))
        contaminated = dict(os.environ)
        contaminated.update({'GIT_DIR': str(self.control / '.git'),
                             'GIT_WORK_TREE': str(self.control),
                             'GIT_INDEX_FILE': str(self.control / '.git/index'),
                             'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'remote.origin.url',
                             'GIT_CONFIG_VALUE_0': 'https://github.com/example/evil'})
        with patch.object(product.os, 'environ', contaminated):
            self.assertEqual(self.verify()['subject_commit'], self.subject)
        self.assertEqual((self.control / '.git/config').read_bytes(), before)
        self.assertTrue(json.loads(subprocess.check_output(probe, text=True)) == native_before,
                        'Test must preserve native child environment without exposing its values')


class FakeOpener:
    def __init__(self, payload):
        self.payload = payload
        self.requests = []

    def open(self, request, timeout):
        self.requests.append(request)
        return io.BytesIO(json.dumps(self.payload).encode())


class PullRequests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        path = self.root / 'tasks/FLOW-001/task.json'
        path.parent.mkdir(parents=True)
        self.task = {'id': 'FLOW-001', 'repository': 'https://github.com/example/control',
                     'issue_url': 'https://github.com/example/control/issues/7'}
        path.write_text(json.dumps(self.task), encoding='utf-8')
        self.event = {'repository': {'full_name': 'example/control'},
                      'pull_request': {'body': 'Issue: https://github.com/example/control/issues/7\nTask: tasks/FLOW-001/task.json\n'}}
        self.opener = FakeOpener({'number': 7, 'html_url': 'https://github.com/example/control/issues/7'})

    def check(self):
        return product.check_pr(self.event, 'example/control', self.root, 'test-token', self.opener)

    def test_fixed_host_read_only_issue_check_and_task_link(self):
        self.assertEqual(self.check()['status'], 'PR_TRACEABILITY_VALID')
        request = self.opener.requests[0]
        self.assertEqual(request.full_url, 'https://api.github.com/repos/example/control/issues/7')
        self.assertEqual(request.get_method(), 'GET')

    def test_missing_issue_pull_url_other_repo_or_missing_task_block(self):
        for body in ['Task: tasks/FLOW-001/task.json',
                     'https://github.com/example/control/pull/7\nTask: tasks/FLOW-001/task.json',
                     'https://github.com/example/other/issues/7\nTask: tasks/FLOW-001/task.json',
                     'https://github.com/example/control/issues/7\nTask: tasks/MISSING/task.json']:
            self.event['pull_request']['body'] = body
            with self.subTest(body=body), self.assertRaises(product.ProductError):
                self.check()

    def test_api_pull_request_object_wrong_identity_and_no_token_block(self):
        for payload in [{'number': 7, 'pull_request': {}},
                        {'number': 8, 'html_url': 'https://github.com/example/control/issues/8'},
                        {'number': 7, 'html_url': 'https://github.com/example/other/issues/7'}]:
            self.opener.payload = payload
            with self.subTest(payload=payload), self.assertRaises(product.ProductError):
                self.check()
        with self.assertRaises(product.ProductError):
            product.check_pr(self.event, 'example/control', self.root, None, self.opener)

    def test_wrong_event_repository_and_task_identity_block(self):
        self.event['repository']['full_name'] = 'example/other'
        with self.assertRaises(product.ProductError):
            self.check()
        self.event['repository']['full_name'] = 'example/control'
        (self.root / 'tasks/FLOW-001/task.json').write_text('{"id":"OTHER"}', encoding='utf-8')
        with self.assertRaises(product.ProductError):
            self.check()

    def test_body_issue_must_match_task_issue_and_task_repository(self):
        for key, value in [('issue_url', 'https://github.com/example/control/issues/8'),
                           ('repository', 'https://github.com/example/other'),
                           ('issue_url', 'https://github.com/example/control/pull/7')]:
            task = dict(self.task)
            task[key] = value
            (self.root / 'tasks/FLOW-001/task.json').write_text(json.dumps(task), encoding='utf-8')
            with self.subTest(key=key, value=value), self.assertRaises(product.ProductError):
                self.check()
    def test_api_error_never_exposes_token_or_response_body(self):
        with patch.object(self.opener, 'open', side_effect=HTTPError(
                'https://api.github.com', 403, 'test-token secret body', {}, None)):
            with self.assertRaises(product.ProductError) as raised:
                self.check()
        self.assertNotIn('test-token', str(raised.exception))
        self.assertIn('403', str(raised.exception))

    def test_redirects_cannot_forward_authorization(self):
        self.assertIsNone(product.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.example'))


if __name__ == '__main__':
    unittest.main()
