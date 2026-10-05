"""Isolated synthetic continuity proof; never writes real Life observations."""
import hashlib
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aspace.journal import Journal, canonical
from aspace.life import review
from tools.heritage import verify


def run():
    root = Path(__file__).resolve().parents[1]
    at = '2026-10-05T18:00:00+00:00'
    claim = {'schema': 'aspace.temporal-claim.v1', 'claim_id': 'fixture:one',
             'subject': 'LD03', 'predicate': 'test_continuity', 'scope': 'life',
             'source_authority': 'fixture', 'source_ref': 'fixture:synthetic',
             'observed_at': at, 'recorded_at': at, 'assertion': {'synthetic': True},
             'evidence_refs': ['fixture:synthetic'], 'temporal_state': 'CURRENT'}
    request = dict(holon_id='LD03', mission_id='fixture:continuity', correlation_id='fixture:continuity',
                   scope='life', authority_envelope={'scope': 'fixture'}, workgraph_neighborhood={},
                   evidence_head=['fixture:synthetic'], return_to={'doctor': 'Doctor11'}, t=at)
    with tempfile.TemporaryDirectory() as folder:
        a = Journal(Path(folder) / 'a/state.sqlite')
        b = None
        try:
            a.append('claim', claim, expected_authority='fixture')
            a.append('claim', claim, expected_authority='fixture')
            first = a.context(**request)
            a.backup(Path(folder) / 'b/state.sqlite')
            b = Journal(Path(folder) / 'b/state.sqlite')
            second = b.context(**request)
            result = {'kind': 'isolated-synthetic-canary', 'same_context_after_relocation': first == second,
                      'capsule_sha256': hashlib.sha256(canonical(second).encode()).hexdigest(),
                      'claims_after_duplicate_delivery': len(b.graph().claims),
                      'return_to': second['return_to'], 'heritage_errors': verify(root),
                      'life_aggregate': review('LD03', at, b)['aggregate_life_state'],
                      'not_verified': ['two VPS hosts', 'GWS effects', 'live Doctors', 'Gateway auth',
                                       'Supabase/WorkGraph synchronization', 'real Life state']}
            if not result['same_context_after_relocation'] or result['heritage_errors']:
                raise ValueError(result)
            return result
        finally:
            a.close()
            if b:
                b.close()


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
