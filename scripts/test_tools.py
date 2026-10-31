#!/usr/bin/env python3
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from validate import validate

ROOT = Path(__file__).resolve().parents[1]


class ToolsTest(unittest.TestCase):
    def test_init_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'workspace with spaces'
            cmd = [sys.executable, str(ROOT / 'scripts/init_workspace.py'), str(dest)]
            first = subprocess.run(cmd, cwd=tmp, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertFalse(validate(dest, 'workspace'))
            original = (dest / 'policy.md').read_bytes()
            self.assertNotEqual(subprocess.run(cmd, cwd=tmp, capture_output=True).returncode, 0)
            self.assertEqual(original, (dest / 'policy.md').read_bytes())
            (dest / 'policy.md').unlink()
            self.assertTrue(validate(dest, 'workspace'))

    def test_refuse_inside_template(self):
        cmd = [sys.executable, str(ROOT / 'scripts/init_workspace.py'), str(ROOT / 'local/test')]
        self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.assertFalse((ROOT / 'local/test').exists())

    def test_tampering_links_and_unlisted_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp) / 'template'
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns('__pycache__'))
            self.assertFalse(validate(clone, 'template'))
            with (clone / 'README.md').open('a') as f:
                f.write('\n[broken](missing.md)\n')
            (clone / 'unexpected.txt').write_text('unlisted')
            errors = validate(clone, 'template')
            self.assertTrue(any('hash' in e for e in errors))
            self.assertTrue(any('relative link' in e for e in errors))
            self.assertTrue(any('membership' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
