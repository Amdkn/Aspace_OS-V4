"""Inspect immutable V3 sources; never execute their historical instructions."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def load(root):
    with gzip.open(Path(root) / 'migration/v3-corpus.json.gz', 'rt', encoding='utf-8') as f:
        return json.load(f)


def verify(root):
    root = Path(root)
    lock = json.loads((root / 'migration/v3-transfer.json').read_text())
    data = (root / 'migration/v3-corpus.json.gz').read_bytes()
    errors = []
    if hashlib.sha256(data).hexdigest() != lock['corpus_sha256']:
        errors.append('corpus digest mismatch')
    corpus = load(root)
    for path, entry in corpus['sources'].items():
        raw = entry['content'].encode('utf-8')
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if blob != entry['git_blob_sha'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
            errors.append('source altered: ' + path)
    if len(corpus['sources']) != lock['imported_text_sources']:
        errors.append('source count mismatch')
    return errors


def search(root, text):
    c = load(root)
    return [{'path': p, 'source_ref': e['source_ref'], 'status': 'HISTORICAL_SOURCE',
             'sha256': e['sha256']}
            for p, e in c['sources'].items()
            if text.casefold() in (p + '\n' + e['content']).casefold()]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['verify', 'search', 'read'])
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--text')
    p.add_argument('--path')
    a = p.parse_args()
    if a.command == 'verify':
        errors = verify(a.root)
        print(json.dumps({'ok': not errors, 'errors': errors}))
        return bool(errors)
    if a.command == 'read':
        if not a.path:
            p.error('--path required')
        print(load(a.root)['sources'][a.path]['content'], end='')
    else:
        if not a.text:
            p.error('--text required')
        print(json.dumps(search(a.root, a.text), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
