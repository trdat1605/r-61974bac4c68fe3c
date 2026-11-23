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


def identity_map():
    return {'schema_version': 1, 'repositories': [
        {'id': 101, 'repository': 'https://github.com/example/control',
         'aliases': ['https://github.com/example/control-legacy']},
        {'id': 202, 'repository': 'https://github.com/example/app',
         'aliases': ['https://github.com/example/app-legacy']}]}


def save_identity_map(root, document=None):
    path = root / 'config/agents/repositories.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(identity_map() if document is None else document), encoding='utf-8')


class RepositoryIdentities(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_missing_map_keeps_unknown_names_strict_and_known_aliases_are_explicit(self):
        self.assertEqual(product.repository_identities(self.root), {})
        save_identity_map(self.root)
        identities = product.repository_identities(self.root)
        self.assertEqual(product.canonical_repository('https://github.com/example/app-legacy', identities),
                         'example/app')
        self.assertEqual(identities['example/app-legacy']['id'], 202)
        self.assertEqual(product.canonical_repository('https://github.com/example/unlisted', identities),
                         'example/unlisted')

    def test_malformed_schema_entries_ids_and_alias_lists_block(self):
        documents = [[], {}, {'schema_version': True, 'repositories': []},
                     {'schema_version': 2, 'repositories': []},
                     {'schema_version': 1, 'repositories': []}]
        for key, values in [('id', [None, True, 0, -1, '101', 101.0]),
                            ('aliases', [None, 'https://github.com/example/old', {}])]:
            for value in values:
                document = identity_map()
                document['repositories'][0][key] = value
                documents.append(document)
        for field in ('id', 'repository', 'aliases'):
            document = identity_map()
            del document['repositories'][0][field]
            documents.append(document)
        for document in documents:
            with self.subTest(document=document):
                save_identity_map(self.root, document)
                with self.assertRaises(product.ProductError):
                    product.repository_identities(self.root)

    def test_duplicate_ids_names_and_cross_repository_aliases_block(self):
        changes = [('id', 101), ('repository', 'https://github.com/example/control'),
                   ('aliases', ['https://github.com/example/control-legacy']),
                   ('aliases', ['https://github.com/example/control']),
                   ('aliases', ['https://github.com/example/app']),
                   ('aliases', ['https://github.com/example/old', 'https://github.com/example/old'])]
        for key, value in changes:
            document = identity_map()
            document['repositories'][1][key] = value
            save_identity_map(self.root, document)
            with self.subTest(key=key, value=value), self.assertRaises(product.ProductError):
                product.repository_identities(self.root)

    def test_unsafe_or_noncanonical_map_urls_block(self):
        for value in [None, 'example/control', 'http://github.com/example/control',
                      'https://token@github.com/example/control', 'https://evil.example/example/control',
                      'https://github.com/example/control?token=secret',
                      'https://github.com/example/control#fragment',
                      'https://github.com/example/control.git', 'https://github.com/example/control/',
                      'https://github.com/example/../control', 'https://github.com/example/.',
                      'https://github.com/Example/Control']:
            for key in ('repository', 'aliases'):
                document = identity_map()
                document['repositories'][0][key] = [value] if key == 'aliases' else value
                save_identity_map(self.root, document)
                with self.subTest(key=key, value=value), self.assertRaises(product.ProductError):
                    product.repository_identities(self.root)


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

    def test_legacy_record_remote_and_committed_receipt_compare_as_known_identity(self):
        save_identity_map(self.control)
        for record_name, remote_name, receipt_name in [
                ('app-legacy', 'app', 'app-legacy'), ('app', 'app-legacy', 'app'),
                ('app-legacy', 'app', 'app'), ('app', 'app', 'app-legacy')]:
            self.record['source']['repository'] = 'https://github.com/example/' + record_name
            self.git(self.app, 'remote', 'set-url', 'origin', 'git@github.com:example/' + remote_name + '.git')
            self.receipt['source_repository'] = 'https://github.com/example/' + receipt_name
            self.save_receipt()
            self.commit_receipt()
            before = self.path.read_bytes()
            with self.subTest(record=record_name, remote=remote_name, receipt=receipt_name):
                self.assertEqual(self.verify()['status'], 'PRODUCT_RECORD_VERIFIED')
                self.assertEqual(self.path.read_bytes(), before)

    def test_no_map_does_not_accept_a_legacy_application_remote(self):
        self.git(self.app, 'remote', 'set-url', 'origin', 'https://github.com/example/app-legacy')
        with self.assertRaisesRegex(product.ProductError, 'identity mismatch'):
            self.verify()

    def test_map_does_not_accept_unlisted_source_remote_or_receipt(self):
        save_identity_map(self.control)
        self.git(self.app, 'remote', 'set-url', 'origin', 'https://github.com/example/unlisted')
        with self.assertRaisesRegex(product.ProductError, 'identity mismatch'):
            self.verify()
        self.git(self.app, 'remote', 'set-url', 'origin', 'https://github.com/example/app')
        self.record['source']['repository'] = 'https://github.com/example/unlisted'
        with self.assertRaisesRegex(product.ProductError, 'identity mismatch'):
            self.verify()
        self.record['source']['repository'] = 'https://github.com/example/app'
        self.receipt['source_repository'] = 'https://github.com/example/unlisted'
        self.save_receipt()
        self.commit_receipt()
        with self.assertRaisesRegex(product.ProductError, 'Receipt application repository mismatch'):
            self.verify()

    def test_renamed_control_clone_still_cannot_masquerade_as_app(self):
        save_identity_map(self.control)
        self.record['source']['repository'] = 'https://github.com/example/control-legacy'
        self.git(self.app, 'remote', 'set-url', 'origin', 'https://github.com/example/control-legacy')
        with self.assertRaisesRegex(product.ProductError, 'cannot be the control'):
            self.verify()

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

    def test_assume_unchanged_cannot_hide_modified_application_bytes(self):
        self.git(self.app, 'update-index', '--assume-unchanged', '--', 'code.txt')
        (self.app / 'code.txt').write_text('hidden unreviewed change\n', encoding='utf-8')
        self.assertEqual(self.git(self.app, 'status', '--porcelain', '--untracked-files=no'), '')
        with self.assertRaisesRegex(product.ProductError, 'assume-unchanged or skip-worktree'):
            self.verify()

    def test_skip_worktree_cannot_hide_modified_application_bytes(self):
        self.git(self.app, 'update-index', '--skip-worktree', '--', 'code.txt')
        (self.app / 'code.txt').write_text('hidden unreviewed change\n', encoding='utf-8')
        self.assertEqual(self.git(self.app, 'status', '--porcelain', '--untracked-files=no'), '')
        with self.assertRaisesRegex(product.ProductError, 'assume-unchanged or skip-worktree'):
            self.verify()

    def test_sparse_configuration_is_explicitly_unsupported_even_with_clean_files(self):
        for key in ('core.sparseCheckout', 'index.sparse'):
            self.git(self.app, 'config', key, 'true')
            with self.subTest(key=key), self.assertRaisesRegex(product.ProductError, 'Sparse application'):
                self.verify()
            self.git(self.app, 'config', key, 'false')

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

    def legacy_task_with_map(self):
        save_identity_map(self.root)
        self.task['repository'] = 'https://github.com/example/control-legacy'
        self.task['issue_url'] = 'https://github.com/example/control-legacy/issues/7'
        path = self.root / 'tasks/FLOW-001/task.json'
        path.write_text(json.dumps(self.task), encoding='utf-8')
        self.event['repository']['id'] = 101
        self.event['pull_request']['body'] = (
            'Legacy: https://github.com/example/control-legacy/issues/7\n'
            'Current: https://github.com/example/control/issues/7\n'
            'Task: tasks/FLOW-001/task.json\n')
        return path

    def test_historical_urls_request_canonical_api_directly_without_redirect(self):
        path = self.legacy_task_with_map()
        before = path.read_bytes()
        with patch.object(product, 'build_opener', return_value=self.opener) as build:
            result = product.check_pr(self.event, 'example/control', self.root, 'test-token')
        self.assertIsInstance(build.call_args.args[0], product.NoRedirect)
        self.assertEqual(result['issues_checked'], 1)
        self.assertEqual(len(self.opener.requests), 1)
        request = self.opener.requests[0]
        self.assertEqual(request.full_url, 'https://api.github.com/repos/example/control/issues/7')
        self.assertEqual(request.get_method(), 'GET')
        self.assertEqual(path.read_bytes(), before)

    def test_known_event_and_expected_aliases_require_same_pinned_id(self):
        self.legacy_task_with_map()
        self.event['repository']['full_name'] = 'example/control-legacy'
        result = product.check_pr(self.event, 'example/control-legacy', self.root, 'test-token', self.opener)
        self.assertEqual(result['status'], 'PR_TRACEABILITY_VALID')
        for value in [None, True, '101', 101.0, 202, 999]:
            self.event['repository']['id'] = value
            with self.subTest(value=value), self.assertRaisesRegex(product.ProductError, 'ID mismatch'):
                self.check()
        self.assertEqual(len(self.opener.requests), 1)

    def test_canonical_event_also_requires_map_id_and_unknown_event_alias_blocks(self):
        self.legacy_task_with_map()
        del self.event['repository']['id']
        with self.assertRaisesRegex(product.ProductError, 'ID mismatch'):
            self.check()
        self.event['repository'] = {'full_name': 'example/unlisted', 'id': 101}
        with self.assertRaisesRegex(product.ProductError, 'repository mismatch'):
            self.check()
        self.assertEqual(self.opener.requests, [])

    def test_event_full_name_remains_strict_even_when_map_exists(self):
        self.legacy_task_with_map()
        for name in ['example/control/', 'example/control.git',
                     'example/control-legacy/', 'https://github.com/example/control']:
            self.event['repository']['full_name'] = name
            with self.subTest(name=name), self.assertRaisesRegex(product.ProductError, 'repository mismatch'):
                self.check()
        self.assertEqual(self.opener.requests, [])

    def test_map_does_not_accept_unlisted_task_or_body_alias(self):
        self.legacy_task_with_map()
        path = self.root / 'tasks/FLOW-001/task.json'
        for key, value in [('repository', 'https://github.com/example/unlisted'),
                           ('issue_url', 'https://github.com/example/unlisted/issues/7')]:
            task = dict(self.task)
            task[key] = value
            path.write_text(json.dumps(task), encoding='utf-8')
            with self.subTest(key=key), self.assertRaises(product.ProductError):
                self.check()
        path.write_text(json.dumps(self.task), encoding='utf-8')
        self.event['pull_request']['body'] += 'https://github.com/example/unlisted/issues/7\n'
        with self.assertRaises(product.ProductError):
            self.check()
        self.assertEqual(self.opener.requests, [])

    def test_missing_map_keeps_legacy_task_urls_strict(self):
        self.legacy_task_with_map()
        (self.root / 'config/agents/repositories.json').unlink()
        with self.assertRaises(product.ProductError):
            self.check()
        self.assertEqual(self.opener.requests, [])

    def test_canonical_api_redirect_or_alias_response_remains_blocked(self):
        self.legacy_task_with_map()
        for status in (301, 302, 307, 308):
            with patch.object(self.opener, 'open', side_effect=HTTPError(
                    'https://api.github.com', status, 'redirect',
                    {'Location': 'https://evil.example'}, None)):
                with self.subTest(status=status), self.assertRaisesRegex(product.ProductError, 'HTTP ' + str(status)):
                    self.check()
        self.opener.payload['html_url'] = 'https://github.com/example/control-legacy/issues/7'
        with self.assertRaisesRegex(product.ProductError, 'GitHub issue repository mismatch'):
            self.check()

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
