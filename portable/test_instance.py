import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import instance


class InstanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.item = {'repository': 'example/repo', 'path': 'core/repo', 'commit': 'a' * 40}

    def test_manifest_pins_and_paths(self):
        instance.validate(json.loads(Path('instance.lock.json').read_text()))
        for path in ['../outside', '/absolute', 'x/../../outside', 'C:\\foo']:
            item = dict(self.item, path=path)
            with self.assertRaises(ValueError):
                instance.validate({'schema_version': 1, 'repositories': [item]})
        with self.assertRaises(ValueError):
            instance.validate({'schema_version': 1, 'repositories': [dict(self.item, commit='main')]})

    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            instance.validate({'schema_version': 1, 'repositories': [self.item, dict(self.item, repository='other/repo', path='core/repo/sub')]})

    def test_symlink_escape_rejected(self):
        (self.root / 'core').symlink_to(self.root.parent)
        with self.assertRaises(ValueError):
            instance.inspect(self.root, self.item)

    def test_missing_and_occupied(self):
        self.assertEqual(instance.inspect(self.root, self.item), 'MISSING')
        dest = self.root / self.item['path']
        dest.mkdir(parents=True)
        self.assertEqual(instance.inspect(self.root, self.item), 'OCCUPIED')
        with self.assertRaises(RuntimeError):
            instance.hydrate(self.root, self.item)

    def test_real_git_identity_dirty_and_revision(self):
        dest = self.root / self.item['path']
        dest.mkdir(parents=True)
        instance.git('init', dest)
        instance.git('-C', dest, 'config', 'user.email', 'test@example.invalid')
        instance.git('-C', dest, 'config', 'user.name', 'test')
        instance.git('-C', dest, 'commit', '--allow-empty', '-m', 'fixture')
        instance.git('-C', dest, 'remote', 'add', 'origin', 'https://github.com/example/repo.git')
        self.item['commit'] = instance.git('-C', dest, 'rev-parse', 'HEAD')
        self.assertEqual(instance.hydrate(self.root, self.item), 'READY')
        (dest / 'uncommitted.txt').write_text('preserve me')
        self.assertEqual(instance.inspect(self.root, self.item), 'DIRTY')
        with self.assertRaises(RuntimeError):
            instance.hydrate(self.root, self.item)
        self.assertEqual((dest / 'uncommitted.txt').read_text(), 'preserve me')
        (dest / 'uncommitted.txt').unlink()
        self.assertEqual(instance.inspect(self.root, dict(self.item, commit='b' * 40)), 'REVISION_MISMATCH')
        instance.git('-C', dest, 'remote', 'set-url', 'origin', 'https://github.com/wrong/repo.git')
        self.assertEqual(instance.inspect(self.root, self.item), 'ORIGIN_MISMATCH')

    def test_hydrate_pinned_commit_and_replay(self):
        source = self.root / 'source'
        instance.git('init', source)
        instance.git('-C', source, 'config', 'user.email', 'test@example.invalid')
        instance.git('-C', source, 'config', 'user.name', 'test')
        (source / 'data.txt').write_text('pinned')
        instance.git('-C', source, 'add', '.')
        instance.git('-C', source, 'commit', '-m', 'pinned')
        self.item['commit'] = instance.git('-C', source, 'rev-parse', 'HEAD')
        (source / 'data.txt').write_text('newer')
        instance.git('-C', source, 'commit', '-am', 'newer')
        original = instance.git
        def transport(*args):
            # Only replace network transport; exercise real git checkout/verification.
            if 'clone' in args or 'fetch' in args:
                return original('-c', 'url.' + str(source) + '.insteadOf=https://github.com/example/repo.git', *args)
            return original(*args)
        with patch.object(instance, 'git', side_effect=transport):
            self.assertEqual(instance.hydrate(self.root, self.item), 'READY')
            self.assertEqual(instance.hydrate(self.root, self.item), 'READY')
        self.assertEqual((self.root / self.item['path'] / 'data.txt').read_text(), 'pinned')


if __name__ == '__main__':
    unittest.main()
