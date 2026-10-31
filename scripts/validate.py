#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path


def validate(root, mode):
    root = root.resolve()
    errors = []
    required = ['README.md', 'policy.md', 'knowledge/project.md', 'memory/README.md', 'candidates/README.md'] if mode == 'workspace' else ['README.md', 'manifest.json', 'scripts/init_workspace.py', 'scripts/validate.py', 'examples/workspace/policy.md']
    for name in required:
        if not (root / name).is_file():
            errors.append('missing: ' + name)
    files = {}
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append('symlink: ' + name)
            continue
        if '.git' in path.relative_to(root).parts or '__pycache__' in path.relative_to(root).parts:
            continue
        if path.is_file():
            files[name] = path
    if mode == 'template' and (root / 'manifest.json').is_file():
        try:
            manifest = json.loads((root / 'manifest.json').read_text())
            actual = set(files) - {'manifest.json'}
            for name in sorted(actual ^ set(manifest)):
                errors.append('manifest membership: ' + name)
            for name in actual & set(manifest):
                if hashlib.sha256(files[name].read_bytes()).hexdigest() != manifest[name]:
                    errors.append('manifest hash: ' + name)
        except (ValueError, TypeError):
            errors.append('invalid manifest')
    for name, path in files.items():
        if path.suffix != '.md':
            continue
        text = path.read_text(encoding='utf-8')
        head = '\n'.join(text.splitlines()[:12])
        for field in ['Version', 'Last Update', 'Purpose']:
            if field not in head:
                errors.append('metadata ' + field + ': ' + name)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.split('#')[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            dest = (path.parent / target).resolve()
            if not dest.is_relative_to(root) or not dest.exists():
                errors.append('invalid relative link: ' + name)
        if mode == 'template':
            patterns = [r'/Users/[^/\s]+/', r'192\.168\.\d+\.\d+', r'-----BEGIN .*PRIVATE KEY-----', r'\b(?:sk|ghp)_[A-Za-z0-9]{20,}']
            if any(re.search(p, text) for p in patterns):
                errors.append('review sensitive marker: ' + name)
    return errors


def main():
    parser = argparse.ArgumentParser(description='Read-only structural validation; not a complete secret audit.')
    parser.add_argument('mode', choices=['template', 'workspace'])
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    errors = validate(args.root, args.mode)
    print('\n'.join(errors) if errors else 'PASS: structure and declared checks only')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
