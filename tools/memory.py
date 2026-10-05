"""Capture immutable source bytes and maintain a rebuildable wiki catalog.

No inference, scheduler, remote publication or source execution.
"""
import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_manifest(root):
    path = root / 'sources.json'
    return json.loads(path.read_text()) if path.exists() else {}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.pending-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def capture(root, source, origin):
    """Single-writer command. Preserve exact bytes; repeated capture is idempotent."""
    root.mkdir(parents=True, exist_ok=True)
    lock = root / '.capture.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        data = source.read_bytes()
        key = digest(data)
        sources = read_manifest(root)
        raw = root / 'raw' / key
        raw.parent.mkdir(exist_ok=True)
        if raw.exists():
            if raw.read_bytes() != data:
                raise ValueError('Existing raw source differs from its digest')
        else:
            with raw.open('xb') as stream:
                stream.write(data)
        entry = sources.setdefault(key, {'path': f'raw/{key}', 'origins': []})
        if entry['path'] != f'raw/{key}':
            raise ValueError('Invalid source path')
        record = {'name': source.name, 'origin': origin}
        if record not in entry['origins']:
            entry['origins'].append(record)
        write_json(root / 'sources.json', sources)
        return key
    finally:
        os.close(fd)
        lock.unlink()


def catalog(root):
    rows = []
    for path in sorted((root / 'wiki').rglob('*.md')):
        if path.is_symlink():
            raise ValueError('Wiki symlink not accepted')
        text = path.read_text(encoding='utf-8')
        rows.append({'path': path.relative_to(root).as_posix(),
                     'sha256': digest(path.read_bytes()),
                     'sources': sorted(set(re.findall(r'source:([a-f0-9]{64})', text)))})
    return rows


def check(root):
    errors = []
    sources = read_manifest(root)
    for key, record in sources.items():
        if not re.fullmatch('[a-f0-9]{64}', key) or record['path'] != f'raw/{key}':
            errors.append(f'invalid source path: {key}')
            continue
        path = root / record['path']
        if path.is_symlink() or not path.is_file() or digest(path.read_bytes()) != key:
            errors.append(f'missing or changed source: {key}')
    for row in catalog(root):
        if not row['sources']:
            errors.append(f'uncited page: {row["path"]}')
        for key in row['sources']:
            if key not in sources:
                errors.append(f'unknown citation: {row["path"]}: {key}')
    if (root.parent / 'migration/v3-transfer.json').exists():
        try:
            from tools.heritage import verify
        except ModuleNotFoundError:
            from heritage import verify
        errors.extend(verify(root.parent))
    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['capture', 'index', 'check', 'query'])
    p.add_argument('--root', type=Path, default=Path('40_Memory'))
    p.add_argument('--file', type=Path)
    p.add_argument('--origin')
    p.add_argument('--text')
    a = p.parse_args()
    if a.command == 'capture':
        if not a.file or not a.origin:
            p.error('capture needs --file and --origin')
        print(capture(a.root, a.file, a.origin))
    elif a.command == 'check':
        errors = check(a.root)
        print(json.dumps({'ok': not errors, 'errors': errors}, ensure_ascii=False))
        return bool(errors)
    elif a.command == 'index':
        errors = check(a.root)
        if errors:
            raise ValueError(errors)
        rows = catalog(a.root)
        write_json(a.root / 'catalog.json', rows)
        print(json.dumps({'pages': len(rows)}))
    else:
        if not a.text:
            p.error('query needs --text')
        matches = []
        for row in catalog(a.root):
            text = (a.root / row['path']).read_text(encoding='utf-8')
            if a.text.casefold() in text.casefold():
                matches.append(row)
        if (a.root.parent / 'migration/v3-transfer.json').exists():
            try:
                from tools.heritage import search
            except ModuleNotFoundError:
                from heritage import search
            matches.extend(search(a.root.parent, a.text))
        print(json.dumps(matches, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
