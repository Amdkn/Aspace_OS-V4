"""Life Core source navigation and evidence review across all eight LD."""
import argparse
import json
from pathlib import Path
from .journal import Journal, timestamp

ROOT = Path(__file__).resolve().parents[1]


def review(domain, at, db=None, root=ROOT):
    registry = json.loads((root / 'life/registry.json').read_text())
    entry = next(d for d in registry['domains'] if d['id'] == domain)
    observations = []
    if db is not None:
        graph = db.graph(as_known_at=at)
        predicates = sorted({c['predicate'] for c in graph.claims.values()
                             if c['subject'] == domain and c['scope'] == 'life'})
        for predicate in predicates:
            observations.extend(graph.state_at(domain, predicate, at, 'life'))
    return {'domain': entry, 'review_at': timestamp(at), 'doctor': registry['doctor'],
            'observations': observations, 'aggregate_life_state': 'UNKNOWN',
            'reason': 'No inferred health/balance score from source files or technical tests',
            'frameworks': [f['id'] for f in registry['frameworks']],
            'return_to': {'domain': domain, 'doctor': 'Doctor11'}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['list', 'review', 'record'])
    p.add_argument('--domain', choices=[f'LD{i:02}' for i in range(1, 9)])
    p.add_argument('--at')
    p.add_argument('--db', type=Path)
    p.add_argument('--claim', type=Path)
    p.add_argument('--authority')
    a = p.parse_args()
    if a.command == 'list':
        print((ROOT / 'life/registry.json').read_text())
        return
    if a.command == 'record' and (not a.db or not a.claim or not a.authority):
        p.error('record requires --db --claim --authority')
    if a.command == 'review' and (not a.domain or not a.at):
        p.error('review requires --domain --at')
    if a.command == 'review' and a.db and not a.db.is_file():
        p.error('review database does not exist')
    journal = Journal(a.db) if a.db else None
    try:
        if a.command == 'record':
            item = json.loads(a.claim.read_text())
            if item['subject'] not in [f'LD{i:02}' for i in range(1, 9)] or item['scope'] != 'life':
                raise ValueError('Claim must target one Life domain in scope life')
            result = {'claim_id': journal.append('claim', item, expected_authority=a.authority)}
        else:
            result = review(a.domain, a.at, journal)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        if journal:
            journal.close()


if __name__ == '__main__':
    main()
