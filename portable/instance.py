#!/usr/bin/env python3
"""Rehydrate pinned A'Space repositories on remote Linux; never launch agents."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile


def git(*args):
    return subprocess.check_output(['git', *map(str, args)], text=True).strip()


def validate(manifest):
    if manifest.get('schema_version') != 1:
        raise ValueError('Unsupported manifest version')
    paths = []
    repositories = set()
    for item in manifest['repositories']:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', item['repository']):
            raise ValueError('Invalid GitHub repository')
        if not re.fullmatch(r'[0-9a-f]{40}', item['commit']):
            raise ValueError('Every repository requires an immutable commit')
        path = PurePosixPath(item['path'])
        if path.is_absolute() or '..' in path.parts or not path.parts or '\\' in item['path']:
            raise ValueError('Unsafe destination path')
        if any(path == p or path in p.parents or p in path.parents for p in paths):
            raise ValueError('Overlapping destinations')
        if item['repository'] in repositories:
            raise ValueError('Duplicate repository')
        paths.append(path)
        repositories.add(item['repository'])


def destination(root, item):
    dest = root / item['path']
    if not dest.resolve().is_relative_to(root.resolve()):
        raise ValueError('Destination escapes instance root')
    return dest


def inspect(root, item):
    dest = destination(root, item)
    if not dest.exists():
        return 'MISSING'
    if dest.is_symlink() or not (dest / '.git').is_dir():
        return 'OCCUPIED'
    expected = 'https://github.com/' + item['repository'] + '.git'
    if git('-C', dest, 'remote', 'get-url', 'origin') != expected:
        return 'ORIGIN_MISMATCH'
    if git('-C', dest, 'status', '--porcelain'):
        return 'DIRTY'
    if git('-C', dest, 'rev-parse', 'HEAD') != item['commit']:
        return 'REVISION_MISMATCH'
    return 'READY'


def hydrate(root, item):
    state = inspect(root, item)
    if state == 'READY':
        return state
    if state != 'MISSING':
        raise RuntimeError(f"{item['path']}: {state}; preserve existing work")
    dest = destination(root, item)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.hydrate-', dir=dest.parent) as staging:
        checkout = Path(staging) / 'repo'
        git('clone', '--filter=blob:none', '--no-checkout',
            'https://github.com/' + item['repository'] + '.git', checkout)
        git('-C', checkout, 'fetch', 'origin', item['commit'])
        git('-C', checkout, 'checkout', '--detach', item['commit'])
        if git('-C', checkout, 'rev-parse', 'HEAD') != item['commit']:
            raise RuntimeError('Checkout verification failed')
        if dest.exists() or dest.is_symlink():
            raise RuntimeError('Destination changed during hydration')
        os.rename(checkout, dest)
    return inspect(root, item)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'hydrate', 'verify'])
    parser.add_argument('--manifest', type=Path, default=Path(__file__).with_name('instance.lock.json'))
    parser.add_argument('--root', type=Path, default=Path(os.environ.get('ASPACE_INSTANCE_ROOT', '/workspaces/aspace')))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    validate(manifest)
    if args.command == 'plan':
        print(json.dumps(manifest, indent=2))
        return 0
    root = args.root.resolve()
    if not args.root.is_absolute() or root == Path('/'):
        raise ValueError('Use a dedicated absolute remote instance root')
    if args.command == 'hydrate':
        root.mkdir(parents=True, exist_ok=True)
    results = []
    def collect():
        for item in manifest['repositories']:
            try:
                state = hydrate(root, item) if args.command == 'hydrate' else inspect(root, item)
            except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
                state = 'FAILED: ' + type(exc).__name__
            results.append({'repository': item['repository'], 'commit': item['commit'], 'state': state})
    if args.command == 'hydrate':
        with (root / '.hydrate.lock').open('w') as lock:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            collect()
    else:
        collect()
    report = {'repositories': results, 'runtime': 'NOT_ACTIVATED',
              'unresolved': manifest.get('unresolved', [])}
    print(json.dumps(report, indent=2))
    if args.command == 'hydrate':
        receipt = root / 'hydration-receipt.json'
        temporary = root / '.hydration-receipt.tmp'
        temporary.write_text(json.dumps(report, indent=2) + '\n')
        temporary.replace(receipt)
    return 0 if all(r['state'] == 'READY' for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
