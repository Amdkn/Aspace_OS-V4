import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('issue_factory', Path(__file__).resolve().parents[1] / 'tools/issue_factory.py')
factory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(factory)


class IssueFactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = patch.dict(os.environ, {'GITHUB_REPOSITORY': 'owner/repo', 'JULES_API_KEY': 'test'}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.out = patch.object(factory, 'OUT', Path(self.temp.name))
        self.out.start()
        self.addCleanup(self.out.stop)
        self.issue = {'number': 5, 'title': 'Build', 'body': 'Implement', 'state': 'open',
                      'html_url': 'https://github.com/owner/repo/issues/5', 'labels': [{'name': 'factory:ready'}]}
        self.comments = []
        self.pr = {'head': {'repo': {'full_name': 'owner/repo'}, 'sha': 'head'},
                   'html_url': 'https://github.com/owner/repo/pull/20', 'state': 'open', 'merged': False}

    def github(self, path, data=None, method=None):
        if path == 'issues/5/comments' and data:
            self.comments.append({'id': 1, 'user': {'login': 'github-actions[bot]'}, 'body': data['body']})
            return self.comments[-1]
        if path == 'issues/8/comments' and data:
            self.comments.append({'id': 2, 'user': {'login': 'github-actions[bot]'}, 'body': data['body']})
            return self.comments[-1]
        if path == 'issues/comments/1' and data:
            self.comments[0]['body'] = data['body']
            return self.comments[0]
        if path == 'issues/comments/2' and data:
            for comment in self.comments:
                if comment['id'] == 2:
                    comment['body'] = data['body']
                    return comment
        if path == '':
            return {'default_branch': 'main'}
        if path == 'git/ref/heads/main':
            return {'object': {'sha': 'base'}}
        if path == 'pulls/20':
            return self.pr
        raise AssertionError(path)

    def setup_transport(self):
        for target, replacement in [('gh', self.github), ('pages', lambda _: self.comments),
            ('sources', lambda: [{'name': 'sources/repo', 'githubRepo': {'owner': 'owner', 'repo': 'repo'}}]),
            ('prompt_for', lambda *args: 'bounded mission')]:
            p = patch.object(factory, target, replacement)
            p.start()
            self.addCleanup(p.stop)

    def test_missing_key_fails_without_dispatch_and_does_not_spam(self):
        self.setup_transport()
        os.environ.pop('JULES_API_KEY')
        with patch.object(factory, 'jules') as runtime:
            self.assertEqual(factory.process(self.issue, Path('.')), 'BLOCKED')
            self.assertEqual(factory.process(self.issue, Path('.')), 'BLOCKED')
            runtime.assert_not_called()
        self.assertEqual(len(self.comments), 1)

    def test_dispatch_claim_precedes_post_and_restart_polls(self):
        self.setup_transport()
        def runtime(path, data=None):
            record, _ = factory.trusted_receipt(self.comments, factory.identity('owner/repo', 5))
            self.assertTrue(record['dispatch_started'])
            if data:
                self.assertEqual(record['state'], 'CLAIMED')
                self.assertEqual(data['automationMode'], 'AUTO_CREATE_PR')
                return {'name': 'sessions/abc'}
            return {'state': 'IN_PROGRESS'}
        with patch.object(factory, 'jules', side_effect=runtime) as transport:
            self.assertEqual(factory.process(self.issue, Path('.')), 'RUNNING')
            self.assertEqual(factory.process(self.issue, Path('.')), 'RUNNING')
            self.assertEqual(sum(c.args[0] == 'sessions' for c in transport.call_args_list), 1)

    def test_ambiguous_post_is_never_repeated(self):
        self.setup_transport()
        with patch.object(factory, 'jules', side_effect=TimeoutError) as runtime:
            with self.assertRaises(TimeoutError):
                factory.process(self.issue, Path('.'))
            self.assertEqual(factory.process(self.issue, Path('.')), 'UNKNOWN')
            self.assertEqual(runtime.call_count, 1)

    def test_untrusted_comment_cannot_forge_controller_receipt(self):
        record = {'mission_id': 'x', 'state': 'RUNNING'}
        comment = {'id': 1, 'user': {'login': 'outsider'},
                   'body': factory.MARKER + '\n```json\n' + json.dumps(record) + '\n```'}
        self.assertEqual(factory.trusted_receipt([comment], 'x'), (None, None))

    def test_build_pr_then_integration_without_closing_parent(self):
        self.setup_transport()
        with patch.object(factory, 'jules', return_value={'name': 'sessions/abc'}):
            factory.process(self.issue, Path('.'))
        with patch.object(factory, 'jules', return_value={'state': 'COMPLETED', 'outputs': [
            {'pullRequest': {'url': 'https://github.com/owner/repo/pull/20'}}]}):
            self.assertEqual(factory.process(self.issue, Path('.')), 'REVIEW')
        self.pr['merged'] = True
        self.assertEqual(factory.process(self.issue, Path('.')), 'INTEGRATED')
        self.assertEqual(self.issue['state'], 'open')

    def test_wrong_repository_output_is_not_accepted(self):
        self.assertIsNone(factory.session_pr({'outputs': [{'pullRequest': {
            'url': 'https://github.com/other/repo/pull/20'}}]}, 'owner/repo'))

    def test_recovery_rejects_unrelated_session(self):
        self.setup_transport()
        with patch.object(factory, 'jules', return_value={'title': 'other', 'prompt': 'other'}):
            with self.assertRaises(ValueError):
                factory.process(self.issue, Path('.'), 'sessions/other')

    def test_idle_queue_never_calls_provider(self):
        event = Path(self.temp.name) / 'event.json'
        event.write_text('{}')
        os.environ.update(GITHUB_EVENT_NAME='schedule', GITHUB_EVENT_PATH=str(event))
        with patch.object(factory, 'pages', return_value=[]), patch.object(factory, 'jules') as runtime:
            factory.main()
            runtime.assert_not_called()
        self.assertTrue(json.loads((factory.OUT / 'run.json').read_text())['idle'])

    def test_main_exits_nonzero_when_provider_missing(self):
        self.setup_transport()
        os.environ.pop('JULES_API_KEY')
        event = Path(self.temp.name) / 'event.json'
        event.write_text('{}')
        os.environ.update(GITHUB_EVENT_NAME='schedule', GITHUB_EVENT_PATH=str(event))
        with patch.object(factory, 'pages', side_effect=lambda p: [self.issue] if p.startswith('issues?') else self.comments):
            with self.assertRaises(SystemExit) as exc:
                factory.main()
            self.assertEqual(exc.exception.code, 1)

    def test_eligible_checks_dependencies(self):
        issue_with_open_dep = {
            'number': 6,
            'state': 'open',
            'labels': [{'name': 'factory:ready'}],
            'body': 'Dépendances fonctionnelles : #2/#3'
        }
        issue_with_closed_deps = {
            'number': 7,
            'state': 'open',
            'labels': [{'name': 'factory:ready'}],
            'body': 'Dépendances fonctionnelles : #2'
        }

        def mock_gh(path):
            if path == 'issues/2':
                return {'state': 'closed'}
            if path == 'issues/3':
                return {'state': 'open'}
            raise AssertionError(path)

        with patch.object(factory, 'gh', side_effect=mock_gh):
            self.assertFalse(factory.eligible(issue_with_open_dep))
            self.assertTrue(factory.eligible(issue_with_closed_deps))

    def test_process_parses_doctor_and_holon(self):
        self.setup_transport()
        issue_with_roles = {
            'number': 8,
            'state': 'open',
            'html_url': 'https://github.com/owner/repo/issues/8',
            'labels': [{'name': 'factory:ready'}],
            'body': 'A : Doctor11 ; R : Amy\nSome other text.'
        }
        with patch.object(factory, 'jules', return_value={'name': 'sessions/xyz'}):
            factory.process(issue_with_roles, Path('.'))
        record = json.loads((Path(self.temp.name) / 'receipt.json').read_text())
        self.assertEqual(record['doctor'], 'doctor11')
        self.assertEqual(record['holon'], 'amy')


if __name__ == '__main__':
    unittest.main()
