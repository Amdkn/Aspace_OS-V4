import unittest
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
import sys
import os

# Add 10_Tech_OS to sys.path to allow import

import importlib
temporal_truth = importlib.import_module("aspace.temporal_truth.temporal_truth")
compiler = importlib.import_module("aspace.temporal_truth.compiler")

TemporalCanonGraph = temporal_truth.TemporalCanonGraph
ContextCompiler = compiler.ContextCompiler

class TestTemporalTruthG0(unittest.TestCase):
    def setUp(self):
        self.graph = TemporalCanonGraph()

    def test_g0_validation(self):
        claim = {
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "c1",
            "subject": "jules",
            "predicate": "active_slots",
            "scope": "runtime",
            "source_authority": "yaz",
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "assertion": "0 active",
            "evidence_refs": ["ev_1"]
        }
        self.graph.ingest_claim(claim)
        self.assertIn("c1", self.graph.claims)

        # Missing required field
        invalid_claim = claim.copy()
        del invalid_claim["subject"]
        with self.assertRaises(Exception): # jsonschema.exceptions.ValidationError
            self.graph.ingest_claim(invalid_claim)


class TestTemporalTruthG1(unittest.TestCase):
    def setUp(self):
        self.graph = TemporalCanonGraph()

    def test_g1_canary(self):
        # Jules sequence: 0 active -> 15 slots -> 12 IN_PROGRESS -> 12 PR open -> 7 PR open
        base_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

        claims_data = [
            ("c1", "0 active", base_time),
            ("c2", "15 slots", base_time + timedelta(minutes=10)),
            ("c3", "12 IN_PROGRESS", base_time + timedelta(minutes=20)),
            ("c4", "12 PR open", base_time + timedelta(minutes=30)),
            ("c5", "7 PR open", base_time + timedelta(minutes=40))
        ]

        for cid, val, t in claims_data:
            self.graph.ingest_claim({
                "schema": "aspace.temporal-claim.v1",
                "claim_id": cid,
                "subject": "jules",
                "predicate": "status",
                "scope": "workgraph",
                "source_authority": "system",
                "observed_at": t.isoformat(),
                "assertion": val,
                "evidence_refs": [f"ev_{cid}"]
            })

        # state_at tests
        t_15m = (base_time + timedelta(minutes=15)).isoformat()
        states = self.graph.state_at("jules", "status", t_15m, "workgraph")
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0]["assertion"], "15 slots")
        self.assertEqual(states[0]["temporal_state"], "CURRENT")

        # history preserved
        t_5m = (base_time + timedelta(minutes=5)).isoformat()
        states_old = self.graph.state_at("jules", "status", t_5m, "workgraph")
        self.assertEqual(states_old[0]["assertion"], "0 active")

        # reinject old 0 active
        self.graph.ingest_claim({
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "c1_re",
            "subject": "jules",
            "predicate": "status",
            "scope": "workgraph",
            "source_authority": "system",
            "observed_at": base_time.isoformat(), # same old observed_at
            "assertion": "0 active",
            "evidence_refs": ["ev_1"]
        })

        # It should NOT make it current
        t_now = (base_time + timedelta(minutes=50)).isoformat()
        states_now = self.graph.state_at("jules", "status", t_now, "workgraph")
        self.assertEqual(states_now[0]["assertion"], "7 PR open")

class TestTemporalTruthG2(unittest.TestCase):
    def setUp(self):
        self.graph = TemporalCanonGraph()
        self.compiler = ContextCompiler(self.graph)

    def test_g2_split_brain(self):
        t_now = datetime.now(timezone.utc)

        self.graph.ingest_claim({
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "mut1",
            "subject": "repo",
            "predicate": "mutation",
            "scope": "github",
            "source_authority": "gh",
            "observed_at": t_now.isoformat(),
            "assertion": "recent",
            "evidence_refs": ["ev_gh"]
        })

        self.graph.ingest_claim({
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "wg1",
            "subject": "jules",
            "predicate": "claims",
            "scope": "workgraph",
            "source_authority": "wg",
            "observed_at": t_now.isoformat(),
            "assertion": 0,
            "evidence_refs": ["ev_wg"]
        })

        self.graph.ingest_claim({
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "wg2",
            "subject": "jules",
            "predicate": "bindings",
            "scope": "workgraph",
            "source_authority": "wg",
            "observed_at": t_now.isoformat(),
            "assertion": 0,
            "evidence_refs": ["ev_wg2"]
        })

        # Derive snapshot for Jules, scope global/aggregate
        # The split brain test says we look at these facts and Jules runtime is UNKNOWN

        snap_gh = self.compiler.derive_physiology_snapshot("repo", "github")
        self.assertEqual(snap_gh["dimensions"][0]["epistemic_state"], "KNOWN")

        snap_wg = self.compiler.derive_physiology_snapshot("jules", "workgraph")
        known_dims = [d for d in snap_wg["dimensions"] if d["epistemic_state"] == "KNOWN"]
        self.assertEqual(len(known_dims), 2)

        snap_rt = self.compiler.derive_physiology_snapshot("jules", "runtime", requested_predicates=["status"])
        self.assertEqual(snap_rt["dimensions"][0]["epistemic_state"], "UNKNOWN")

class TestTemporalTruthG3(unittest.TestCase):
    def setUp(self):
        self.graph = TemporalCanonGraph()

    def test_g3_reconciliation(self):
        t = datetime.now(timezone.utc)

        # Two conflicting claims
        self.graph.ingest_claim({
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "c_a",
            "subject": "system",
            "predicate": "mode",
            "scope": "global",
            "source_authority": "A",
            "observed_at": t.isoformat(),
            "assertion": "X",
            "evidence_refs": ["ev_a"]
        })

        self.graph.ingest_claim({
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "c_b",
            "subject": "system",
            "predicate": "mode",
            "scope": "global",
            "source_authority": "B",
            "observed_at": t.isoformat(),
            "assertion": "Y",
            "evidence_refs": ["ev_b"]
        })

        # Explicit reconciliation -> Transition
        self.graph.record_transition({
            "schema": "aspace.canon-transition.v1",
            "transition_id": "t1",
            "subject": "system",
            "predicate": "mode",
            "scope": "global",
            "from_claims": ["c_a"],
            "to_claims": ["c_b"], # Resolving to B
            "effective_at": t.isoformat(),
            "reason": "Rory decided B is authoritative",
            "evidence_refs": ["ev_rory"],
            "resolution_authority": "rory",
            "resolution_scope": "global",
            "resulting_canon_heads": ["c_b"]
        })

        states = self.graph.state_at("system", "mode", (t + timedelta(minutes=1)).isoformat(), "global")
        # c_a should be SUPERSEDED, c_b should be CURRENT
        c_a_res = next(s for s in states if s["claim_id"] == "c_a")
        c_b_res = next(s for s in states if s["claim_id"] == "c_b")

        self.assertEqual(c_a_res["temporal_state"], "SUPERSEDED")
        self.assertEqual(c_b_res["temporal_state"], "CURRENT")

class TestTemporalTruthG4G5(unittest.TestCase):
    def setUp(self):
        self.graph = TemporalCanonGraph()
        self.compiler = ContextCompiler(self.graph)

    def test_g4_context_compiler(self):
        t = datetime.now(timezone.utc)
        self.graph.ingest_claim({
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "c_ctx",
            "subject": "ryan",
            "predicate": "role",
            "scope": "mission_1",
            "source_authority": "system",
            "observed_at": t.isoformat(),
            "assertion": "builder",
            "evidence_refs": ["ev_1"]
        })

        capsule = self.compiler.compile_context_capsule(
            holon_id="ryan",
            mission_id="m1",
            correlation_id="corr1",
            scope="mission_1",
            authority_envelope={"type": "standard"},
            workgraph_neighborhood={"nodes": []},
            evidence_head=["ev_1"],
            return_to={"topic": "done"}
        )

        self.assertEqual(capsule["holon_id"], "ryan")
        self.assertIn("c_ctx", capsule["canon_slice"])
        self.assertNotIn("giant_role_prompt", str(capsule))

if __name__ == '__main__':
    unittest.main()
