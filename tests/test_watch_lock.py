import hashlib
import json
import unittest
from pathlib import Path


class WatchLockTest(unittest.TestCase):
    def test_vendored_files_match_pinned_lock(self):
        root = Path(__file__).parents[1]
        lock = json.loads((root / 'architecture/watch.lock.json').read_text())
        for name, sha in lock['files'].items():
            with self.subTest(name=name):
                path = root / '.agents/skills/watch' / name
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), sha)
