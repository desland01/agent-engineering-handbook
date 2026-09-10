"""Source layout behaves the same in Git checkouts and deployment archives."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


class ArchiveLayoutTest(unittest.TestCase):
    def test_generated_files_are_ignored_but_source_violations_are_rejected(self):
        spec = importlib.util.spec_from_file_location('handbook_check', Path(__file__).with_name('check.py'))
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        with tempfile.TemporaryDirectory() as directory:
            checker.ROOT = Path(directory)
            for name in ['.vercel/project.json', '.build-deps/markdown/core.py',
                         'control/plan-20260910.md', 'unexpected.txt', 'guides/test.md']:
                target = checker.ROOT / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('fixture')
            with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, ['git'])):
                files = {str(path) for path in checker.tracked_files()}
                checker.layout()
            self.assertEqual(files, {'control/plan-20260910.md', 'unexpected.txt', 'guides/test.md'})
            self.assertTrue(any('unexpected entry' in failure for failure in checker.failures))
            self.assertTrue(any('a date, version' in failure for failure in checker.failures))
            self.assertFalse(any('guides/test.md' in failure for failure in checker.failures))


if __name__ == '__main__':
    unittest.main()
