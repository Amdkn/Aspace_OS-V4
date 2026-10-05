import copy
import unittest
from datetime import datetime, timezone

from aspace.temporal_truth.packets import ContradictionPacket
from aspace.temporal_truth.reconciliation import (
    ReconciliationBoundaryError,
    transition_from_explicit_decision,
)
from aspace.temporal_truth.temporal_truth import TemporalCanonGraph


class TestRoryTemporalReconciliation(unittest.TestCase):
    def setUp(self):
        self.graph = TemporalCanonGraph()
        now = datetime.now(timezone.utc).isoformat()
        self.now = now
        self.claim_a = {
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "claim-a",
            "subject": "service",
            "predicate": "release_state",
            "scope": "production",
            "source_authority": "github",
            "observed_at": now,
            "assertion": "READY",
            "evidence_refs": ["github:pr:1"],
        }
        self.claim_b = {
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "claim-b",
            "subject": "service",
            "predicate": "release_state",
            "scope": "production",
            "source_authority": "runtime",
            "observed_at": now,
            "assertion": "BLOCKED",
            "evidence_refs": ["runtime:receipt:2"],
        }
        self.graph.ingest_claim(copy.deepcopy(self.claim_a))
        self.graph.ingest_claim(copy.deepcopy(self.claim_b))
        self.before_a = copy.deepcopy(self.graph.claims["claim-a"])
        self.before_b = copy.deepcopy(self.graph.claims["claim-b"])
        self.packet = ContradictionPacket(
            packet_id="contradiction-494",
            detected_at=now,
            subject="service",
            predicate="release_state",
            scope="production",
            claims=["claim-a", "claim-b"],
            detector_authority="graham",
            correlation_id="corr-494",
            return_to={"issue": 448, "gate": "G4"},
        )

    def decision(self, **updates):
        value = {
            "resolution_authority": "rory",
            "resolution_scope": "production",
            "selected_claims": ["claim-b"],
            "reason": "Runtime receipt is authoritative for deployed release_state.",
            "evidence_refs": ["rory:review:494", "runtime:receipt:2"],
            "effective_at": self.now,
            "correlation_id": "corr-494",
            "return_to": {"issue": 448, "gate": "G4"},
        }
        value.update(updates)
        return value

    def test_explicit_rory_decision_records_transition_without_rewriting_history(self):
        transition = transition_from_explicit_decision(
            self.graph, self.packet, self.decision()
        )

        self.assertEqual(transition.from_claims, ["claim-a"])
        self.assertEqual(transition.to_claims, ["claim-b"])
        self.assertEqual(transition.resolution_authority, "rory")
        self.assertEqual(transition.resolution_scope, "production")
        self.assertEqual(transition.contradiction_refs, ["contradiction-494"])
        self.assertEqual(transition.correlation_id, "corr-494")
        self.assertEqual(transition.return_to, {"issue": 448, "gate": "G4"})

        # Original claims remain byte-for-byte equivalent to their post-ingest
        # historical records. G3 records a transition; it never rewrites claims.
        self.assertEqual(self.graph.claims["claim-a"], self.before_a)
        self.assertEqual(self.graph.claims["claim-b"], self.before_b)

        states = self.graph.state_at(
            "service",
            "release_state",
            self.now,
            "production",
        )
        by_id = {item["claim_id"]: item for item in states}
        self.assertEqual(by_id["claim-a"]["temporal_state"], "SUPERSEDED")
        self.assertEqual(by_id["claim-b"]["temporal_state"], "CURRENT")

    def test_missing_explicit_decision_fields_fail_closed(self):
        for field in (
            "resolution_authority",
            "resolution_scope",
            "selected_claims",
            "reason",
            "evidence_refs",
            "effective_at",
        ):
            with self.subTest(field=field):
                decision = self.decision()
                decision.pop(field)
                with self.assertRaises(ReconciliationBoundaryError):
                    transition_from_explicit_decision(
                        self.graph, self.packet, decision
                    )
                self.assertEqual(self.graph.transitions, {})

    def test_unknown_selected_claim_fails_closed(self):
        with self.assertRaises(ReconciliationBoundaryError):
            transition_from_explicit_decision(
                self.graph,
                self.packet,
                self.decision(selected_claims=["claim-does-not-exist"]),
            )
        self.assertEqual(self.graph.transitions, {})

    def test_scope_widening_fails_closed(self):
        with self.assertRaises(ReconciliationBoundaryError):
            transition_from_explicit_decision(
                self.graph,
                self.packet,
                self.decision(resolution_scope="global"),
            )
        self.assertEqual(self.graph.transitions, {})

    def test_wrong_resolution_authority_fails_closed(self):
        with self.assertRaises(ReconciliationBoundaryError):
            transition_from_explicit_decision(
                self.graph,
                self.packet,
                self.decision(resolution_authority="graham"),
            )
        self.assertEqual(self.graph.transitions, {})

    def test_empty_evidence_fails_closed(self):
        with self.assertRaises(ReconciliationBoundaryError):
            transition_from_explicit_decision(
                self.graph,
                self.packet,
                self.decision(evidence_refs=[]),
            )
        self.assertEqual(self.graph.transitions, {})

    def test_correlation_or_return_path_drift_fails_closed(self):
        for updates in (
            {"correlation_id": "corr-other"},
            {"return_to": {"issue": 999}},
        ):
            with self.subTest(updates=updates):
                with self.assertRaises(ReconciliationBoundaryError):
                    transition_from_explicit_decision(
                        self.graph,
                        self.packet,
                        self.decision(**updates),
                    )
                self.assertEqual(self.graph.transitions, {})

    def test_packet_claim_dimension_mismatch_fails_closed(self):
        bad_packet = copy.deepcopy(self.packet)
        bad_packet.predicate = "different_predicate"
        with self.assertRaises(ReconciliationBoundaryError):
            transition_from_explicit_decision(
                self.graph,
                bad_packet,
                self.decision(),
            )
        self.assertEqual(self.graph.transitions, {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
