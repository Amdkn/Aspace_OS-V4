"""Reproducible, offline import from a pinned sparse Git checkout. No source execution."""
import argparse
import gzip
import hashlib
import json
import subprocess
from pathlib import Path

REV = 'ad5e68e2867854ad952495cf1fcd37d76acbd33e'
REPO = 'Amdkn/Aspace_OS_V3'
ROOTS = ('40_Memory_Wiki_OKF/', '50_Distillation/',
         '60_Implementation_Méthodologiques/', '70_Onthologies/', '20_Life_OS/')
ARCHIVE = '20_Life_OS/24_PARA_Enterprise/04_Archives_Data/'


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run(source, dest):
    actual = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != REV:
        raise ValueError('Source HEAD differs from pinned revision')
    tree = subprocess.check_output(['git', '-C', str(source), 'ls-tree', '-rz', '--full-tree', REV])
    sources, inventory = {}, []
    for record in tree.split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, sha = meta.decode().split()
        path = name.decode('utf-8')
        ref = f'https://github.com/{REPO}/blob/{REV}/{path}'
        row = {'source_path': path, 'git_sha': sha, 'mode': mode, 'type': kind,
               'source_ref': ref, 'disposition': 'REFERENCE_PENDING_QUALIFICATION'}
        selected = path.startswith(ROOTS) and not path.startswith(ARCHIVE)
        if kind == 'commit':
            row['disposition'] = 'EXTERNAL_GITLINK_REQUIRES_ORIGIN'
        elif path.startswith(ARCHIVE):
            row['disposition'] = 'ARCHIVE_REFERENCE_PRESERVED'
        elif selected:
            f = source / path
            if f.is_symlink():
                raise ValueError('Selected symlink requires explicit handling: ' + path)
            raw = f.read_bytes()
            blob_sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            if blob_sha != sha:
                raise ValueError('Dirty or altered source: ' + path)
            try:
                content = raw.decode('utf-8')
                if '\0' in content:
                    raise UnicodeError('binary')
            except UnicodeError:
                row['disposition'] = 'BINARY_REFERENCE_PRESERVED'
            else:
                sources[path] = {'content': content, 'git_blob_sha': sha,
                                 'sha256': hashlib.sha256(raw).hexdigest(), 'source_ref': ref}
                row['disposition'] = 'IMPORTED_HISTORICAL_SOURCE'
        inventory.append(row)
    corpus = {'repository': REPO, 'revision': REV, 'instruction_authority': False,
              'sources': dict(sorted(sources.items()))}
    packed = gzip.compress(json.dumps(corpus, ensure_ascii=False, sort_keys=True).encode(), mtime=0)
    (dest / 'migration').mkdir(exist_ok=True)
    (dest / 'migration/v3-corpus.json.gz').write_bytes(packed)
    dump(dest / 'migration/v3-inventory.json', {'repository': REPO, 'revision': REV, 'entries': inventory})
    dump(dest / 'migration/v3-transfer.json', {
        'repository': REPO, 'revision': REV, 'schema': 'aspace.heritage-transfer.v1',
        'source_entries': len(inventory), 'imported_text_sources': len(sources),
        'corpus_sha256': hashlib.sha256(packed).hexdigest(),
        'dispositions': {d: sum(x['disposition'] == d for x in inventory)
                         for d in sorted({x['disposition'] for x in inventory})},
        'meaning': 'Historical evidence; no automatic V4 canon or runtime activation',
        'return_to': {'repository': 'Amdkn/Aspace_OS-V4', 'pull_request': 8}})
    domains = []
    names = ['Carrière et Business', 'Finance', 'Santé, sommeil et énergie', 'Cognition',
             'Social', 'Famille', 'Créativité', 'Impact']
    wheel = '20_Life_OS/22_Wheel_Discovery/'
    for i, name in enumerate(names, 1):
        domain_id = f'LD{i:02}'
        domain_sources = [p for p in sources if p.startswith(wheel + domain_id + '_')]
        if not domain_sources:
            raise ValueError('Missing domain sources: ' + domain_id)
        domains.append({'id': domain_id, 'name': name,
                        'steward': domain_sources[0].split('/')[2].split('_')[-1],
                        'source_paths': domain_sources, 'runtime_state': 'UNKNOWN',
                        'source_state': 'HISTORICAL', 'business_os': i == 1})
    frameworks = [{'id': n, 'source_paths': [p for p in sources if p.startswith('20_Life_OS/' + prefix)]}
                  for n, prefix in [('Ikigai', '21_'), ('Wheel', '22_'), ('12WY', '23_'),
                                    ('PARA', '24_'), ('GTD', '25_'), ('DEAL', '26_')]]
    dump(dest / 'life/registry.json', {'schema': 'aspace.life-registry.v1', 'layer': 'L1',
         'doctor': 'Doctor11', 'companions': ['Amy', 'Rory', 'River'],
         'domains': domains, 'frameworks': frameworks,
         'frameworks_cross_domains': True, 'twelve_week_vessel': 'Curie',
         'historical_path_alias': '23_12WY_SNW',
         'business_parent': 'LD01', 'source_revision': REV})
    print(json.dumps({'entries': len(inventory), 'sources': len(sources), 'bytes': len(packed)}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('--dest', type=Path, default=Path(__file__).resolve().parents[1])
    a = p.parse_args()
    run(a.source.resolve(), a.dest.resolve())
