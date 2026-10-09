import copy
import json
import tempfile
import unittest
from pathlib import Path
from aspace.journal import Journal
from aspace.life import review
from tools.heritage import load, verify

ROOT = Path(__file__).resolve().parents[1]
AT = '2026-10-05T18:00:00+00:00'


def claim(identity, value='recovery', **changes):
    c = {'schema': 'aspace.temporal-claim.v1', 'claim_id': identity,
         'subject': 'LD03', 'predicate': 'fixture', 'scope': 'life',
         'source_authority': 'test:culber', 'source_ref': 'test:fixture',
         'observed_at': '2026-10-05T17:00:00+00:00', 'recorded_at': '2026-10-05T17:01:00+00:00',
         'assertion': value, 'evidence_refs': ['test:fixture'], 'temporal_state': 'CURRENT'}
    c.update(changes)
    return c


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.journal = Journal(self.home / 'source.sqlite')
        self.addCleanup(self.journal.close)

    def put(self, c):
        return self.journal.append('claim', c, expected_authority=c['source_authority'])

    def context(self, journal):
        return journal.context(holon_id='LD03', mission_id='fixture:continuity',
                               correlation_id='fixture:one', scope='life',
                               authority_envelope={'owner': 'Doctor11', 'effect': 'test'},
                               workgraph_neighborhood={}, evidence_head=['test:fixture'],
                               return_to={'doctor': 'Doctor11', 'mission': 'fixture:continuity'}, t=AT)

    def test_relocation_replays_identical_context_and_deduplicates(self):
        c = claim('first')
        self.put(c)
        self.put(c)
        self.assertEqual(self.journal.db.execute('select count(*) from event').fetchone()[0], 1)
        expected = self.context(self.journal)
        self.journal.backup(self.home / 'second-host/state.sqlite')
        recovered = Journal(self.home / 'second-host/state.sqlite')
        try:
            self.assertEqual(expected, self.context(recovered))
            self.assertEqual(expected['return_to']['doctor'], 'Doctor11')
        finally:
            recovered.close()

    def test_immutable_identity_cannot_be_overwritten(self):
        self.put(claim('first'))
        with self.assertRaises(ValueError):
            self.put(claim('first', 'different'))
        self.assertEqual(len(self.journal.graph().claims), 1)

    def test_historical_import_does_not_become_live(self):
        self.put(claim('old', 'GREEN', temporal_state='HISTORICAL'))
        self.assertEqual(self.context(self.journal)['canon_slice'], [])
        self.assertEqual(review('LD03', AT, self.journal)['aggregate_life_state'], 'UNKNOWN')

    def test_late_ingestion_respects_knowledge_cutoff(self):
        self.put(claim('late', recorded_at='2026-10-06T00:00:00Z'))
        self.assertEqual(self.context(self.journal)['canon_slice'], [])
        self.assertEqual(len(self.journal.graph().claims), 1)

    def test_contradiction_survives_replay(self):
        self.put(claim('one', 'A'))
        self.put(claim('two', 'B', source_authority='test:rory'))
        capsule = self.context(self.journal)
        self.assertEqual(set(capsule['contradictions']), {'one', 'two'})

    def test_older_observation_does_not_replace_newer(self):
        self.put(claim('new', 'new'))
        self.put(claim('old', 'old', observed_at='2026-10-04T17:00:00Z'))
        self.assertEqual(self.context(self.journal)['canon_slice'], ['new'])

    def test_explicit_reconciliation_preserves_old_claims(self):
        self.put(claim('one', 'A'))
        self.put(claim('two', 'B', source_authority='test:rory'))
        transition = {'schema': 'aspace.canon-transition.v1', 'transition_id': 'resolution',
                      'subject': 'LD03', 'predicate': 'fixture', 'scope': 'life',
                      'from_claims': ['one'], 'to_claims': ['two'], 'resulting_canon_heads': ['two'],
                      'recorded_at': AT, 'effective_at': AT, 'reason': 'Test explicit decision',
                      'evidence_refs': ['test:decision'], 'resolution_authority': 'rory',
                      'resolution_scope': 'life'}
        self.journal.append('transition', transition, expected_authority='rory')
        self.assertEqual(self.context(self.journal)['canon_slice'], ['two'])
        self.assertEqual(len(self.journal.graph().claims), 2)
        transition['transition_id'] = 'bad'
        transition['scope'] = 'business'
        with self.assertRaises(ValueError):
            self.journal.append('transition', transition, expected_authority='rory')

    def test_unknown_authority_and_cross_scope_relations_rejected(self):
        with self.assertRaises(ValueError):
            self.journal.append('claim', claim('first'), expected_authority='other')
        self.put(claim('one'))
        with self.assertRaises(ValueError):
            self.put(claim('other', subject='LD02', supersedes=['one']))

    def test_expired_claim_not_current(self):
        self.put(claim('expired', valid_to='2026-10-05T17:30:00Z'))
        self.assertEqual(self.context(self.journal)['canon_slice'], [])

    def test_intrusion_deletion(self):
        # Intrusion: delete the row directly using sqlite3
        import sqlite3
        self.put(claim('c1'))
        self.put(claim('c1b'))

        conn = sqlite3.connect(self.home / 'source.sqlite')
        conn.execute("DELETE FROM event WHERE identity='c1'")
        conn.commit()
        conn.close()

        # Re-initialize journal (simulate fresh startup) or just call graph()
        journal2 = Journal(self.home / 'source.sqlite')
        with self.assertRaises(ValueError) as context:
            journal2.graph()
        self.assertIn("Journal integrity failure", str(context.exception))
        journal2.close()

    def test_intrusion_insertion(self):
        # Intrusion: insert a fake row bypassing append() logic
        import sqlite3
        import hashlib
        from aspace.journal import canonical

        c1 = claim('c1')
        self.put(c1)

        fake_claim = dict(c1)
        fake_claim["claim_id"] = "c2"
        fake_claim["assertion"] = "forged"

        encoded = canonical(fake_claim)
        digest = hashlib.sha256(encoded.encode()).hexdigest()

        conn = sqlite3.connect(self.home / 'source.sqlite')
        conn.execute(
            "INSERT INTO event(kind,identity,payload,digest) VALUES(?,?,?,?)",
            ("claim", "c2", encoded, digest)
        )
        conn.commit()
        conn.close()

        journal2 = Journal(self.home / 'source.sqlite')
        with self.assertRaises(ValueError) as context:
            journal2.graph()

        self.assertIn("Journal integrity failure", str(context.exception))

        try:
            state = journal2.graph().state_at("LD03", "fixture", AT, "life")
            self.assertFalse(any(c["claim_id"] == "c2" for c in state), "Forged claim should not be returned by state_at")
        except ValueError:
            pass # graph() failing is expected and good

        journal2.close()


class HeritageTests(unittest.TestCase):
    def test_all_source_bytes_and_inventory_are_preserved(self):
        self.assertEqual(verify(ROOT), [])
        inventory = json.loads((ROOT / 'migration/v3-inventory.json').read_text())['entries']
        self.assertEqual(len(inventory), 9339)
        corpus = load(ROOT)['sources']
        self.assertEqual(sum(p.startswith('40_Memory_Wiki_OKF/') for p in corpus), 100)

    def test_eight_domains_six_frameworks_have_resolvable_sources(self):
        corpus = load(ROOT)['sources']
        registry = json.loads((ROOT / 'life/registry.json').read_text())
        self.assertEqual([d['id'] for d in registry['domains']], [f'LD{i:02}' for i in range(1,9)])
        self.assertEqual(len(registry['frameworks']), 6)
        for entry in registry['domains'] + registry['frameworks']:
            self.assertTrue(entry['source_paths'])
            self.assertTrue(all(p in corpus for p in entry['source_paths']))


if __name__ == '__main__':
    unittest.main()
