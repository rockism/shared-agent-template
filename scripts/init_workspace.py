#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path
from validate import validate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    target = args.destination.expanduser().absolute()
    if target.exists() or target.is_symlink() or target.resolve().is_relative_to(source):
        parser.error('Destination must be new and outside the template.')
    if validate(source, 'template'):
        parser.error('Template validation failed; inspect it before initializing.')
    target.mkdir(mode=0o700, parents=True, exist_ok=False)
    # A failed copy is retained for inspection, never silently removed or overwritten.
    shutil.copytree(source / 'examples/workspace', target, dirs_exist_ok=True)
    errors = validate(target, 'workspace')
    if errors:
        parser.error('Created workspace needs inspection: ' + '; '.join(errors))
    print('Created example workspace. Validate and review policy before use.')


if __name__ == '__main__':
    main()
