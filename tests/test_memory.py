import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('memory', Path(__file__).parents[1] / 'tools/memory.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'memory'
        self.source = self.base / 'source.txt'
        self.source.write_bytes(b'original\r\nsource\n')

    def test_capture_idempotent_and_exact(self):
        key = m.capture(self.root, self.source, 'test:input')
        self.assertEqual(key, m.capture(self.root, self.source, 'test:input'))
        self.assertEqual((self.root / 'raw' / key).read_bytes(), self.source.read_bytes())
        self.assertEqual(len(m.read_manifest(self.root)[key]['origins']), 1)

    def test_tampering_is_reported(self):
        key = m.capture(self.root, self.source, 'test:input')
        (self.root / 'raw' / key).write_text('changed')
        self.assertTrue(m.check(self.root))
        with self.assertRaises(ValueError):
            m.capture(self.root, self.source, 'test:input')

    def test_citation_validation_and_catalog(self):
        key = m.capture(self.root, self.source, 'test:input')
        wiki = self.root / 'wiki'
        wiki.mkdir()
        page = wiki / 'note.md'
        page.write_text('No citation')
        self.assertTrue(m.check(self.root))
        page.write_text('source:' + '0' * 64)
        self.assertTrue(m.check(self.root))
        page.write_text('source:' + key)
        self.assertEqual(m.check(self.root), [])
        self.assertEqual(m.catalog(self.root)[0]['sources'], [key])

    def test_concurrent_writer_refused(self):
        self.root.mkdir()
        (self.root / '.capture.lock').touch()
        with self.assertRaises(FileExistsError):
            m.capture(self.root, self.source, 'test:input')

    def test_raw_traversal_refused(self):
        key = m.capture(self.root, self.source, 'test:input')
        records = m.read_manifest(self.root)
        records[key]['path'] = '../source.txt'
        m.write_json(self.root / 'sources.json', records)
        self.assertIn('invalid source path', m.check(self.root)[0])


if __name__ == '__main__':
    unittest.main()
