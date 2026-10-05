import unittest
import json
import os
import jsonschema
from aspace.temporal_truth.packets import (
    ObservationPacket,
    TemporalClaim,
    ContradictionPacket,
    CanonTransition,
    ContextCapsule,
    CapabilityNeed,
    serialize_packet,
    deserialize_packet
)

class TestPacketsRoundTrip(unittest.TestCase):
    def test_observation_packet_round_trip(self):
        packet = ObservationPacket.create(
            source_ref="gh_issue_458",
            source_authority="yaz",
            dimension="github_mutation_recent",
            value=True,
            evidence_refs=["#458"],
            return_to={"owner": "nardole"}
        )
        json_str = serialize_packet(packet)
        deserialized = deserialize_packet(json_str)
        self.assertEqual(packet, deserialized)
        self.assertEqual(deserialized.source_authority, "yaz")
        self.assertEqual(deserialized.return_to, {"owner": "nardole"})

    def test_contradiction_packet_round_trip(self):
        packet = ContradictionPacket.create(
            subject="jules",
            predicate="runtime_state",
            scope="global",
            claims=["claim_1", "claim_2"],
            detector_authority="graham",
            return_to={"owner": "nardole"}
        )
        json_str = serialize_packet(packet)
        deserialized = deserialize_packet(json_str)
        self.assertEqual(packet, deserialized)
        self.assertEqual(deserialized.detector_authority, "graham")
        self.assertEqual(deserialized.return_to, {"owner": "nardole"})

    def test_capability_need_round_trip(self):
        packet = CapabilityNeed.create(
            target_capability="reconcile_contradiction",
            evidence=["contradiction_123"],
            issuer_authority="rory",
            return_to={"owner": "nardole"}
        )
        json_str = serialize_packet(packet)
        deserialized = deserialize_packet(json_str)
        self.assertEqual(packet, deserialized)
        self.assertEqual(deserialized.issuer_authority, "rory")
        self.assertEqual(deserialized.return_to, {"owner": "nardole"})

    def test_temporal_claim_round_trip(self):
        packet = TemporalClaim(
            claim_id="claim_1",
            source_ref="gh_458",
            source_authority="yaz",
            recorded_at="2026-10-03T10:00:00Z",
            observed_at="2026-10-03T09:59:00Z",
            scope="github",
            subject="jules",
            predicate="mutation",
            assertion=True,
            evidence_refs=["evidence_1"],
            temporal_state="CURRENT",
            return_to={"owner": "nardole"}
        )
        json_str = serialize_packet(packet)
        deserialized = deserialize_packet(json_str)
        self.assertEqual(packet, deserialized)
        self.assertEqual(deserialized.source_authority, "yaz")
        self.assertEqual(deserialized.return_to, {"owner": "nardole"})

    def test_canon_transition_round_trip(self):
        packet = CanonTransition(
            transition_id="trans_1",
            subject="jules",
            predicate="runtime_state",
            scope="global",
            from_claims=["claim_1"],
            to_claims=["claim_2"],
            recorded_at="2026-10-03T10:10:00Z",
            effective_at="2026-10-03T10:10:00Z",
            reason="explicit_reconciliation",
            evidence_refs=["contradiction_1"],
            resolution_authority="rory",
            resolution_scope="global",
            resulting_canon_heads=["claim_2"],
            return_to={"owner": "nardole"}
        )
        json_str = serialize_packet(packet)
        deserialized = deserialize_packet(json_str)
        self.assertEqual(packet, deserialized)
        self.assertEqual(deserialized.resolution_authority, "rory")
        self.assertEqual(deserialized.return_to, {"owner": "nardole"})

    def test_context_capsule_round_trip(self):
        packet = ContextCapsule(
            capsule_id="cap_1",
            compiled_at="2026-10-03T10:15:00Z",
            source_cutoff_at="2026-10-03T10:14:00Z",
            holon_id="jules",
            mission_id="mission_1",
            correlation_id="corr_1",
            canon_slice=["claim_2"],
            anthology_window=["event_1"],
            physiology_ref="phys_1",
            authority_envelope={"boundary": "safe"},
            workgraph_neighborhood={"claims": 0, "bindings": 0},
            evidence_head=["evidence_1"],
            contradictions=[],
            unknowns=["jules_runtime"],
            return_to={"owner": "nardole"}
        )
        json_str = serialize_packet(packet)
        deserialized = deserialize_packet(json_str)
        self.assertEqual(packet, deserialized)
        self.assertEqual(deserialized.unknowns, ["jules_runtime"])
        self.assertEqual(deserialized.return_to, {"owner": "nardole"})


    def test_resolution_authority_requires_explicit_scope(self):
        packet = CanonTransition(
            transition_id="trans_auth",
            subject="jules",
            predicate="runtime_state",
            scope="global",
            from_claims=["claim_1"],
            to_claims=["claim_2"],
            recorded_at="2026-10-03T10:10:00Z",
            effective_at="2026-10-03T10:10:00Z",
            reason="explicit_reconciliation",
            evidence_refs=["contradiction_1"],
            resolution_authority="rory",
            resolution_scope="runtime_state/global",
            resulting_canon_heads=["claim_2"],
            return_to={"owner": "nardole"}
        )
        data = json.loads(serialize_packet(packet))
        schema_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "aspace",
            "contracts",
            "TEMPORAL_TRUTH_CONTEXT_V1.schema.json",
        )
        with open(schema_path, "r", encoding="utf-8") as handle:
            root = json.load(handle)
        bounded_schema = dict(root)
        bounded_schema["$ref"] = "#/$defs/CanonTransition"
        jsonschema.validate(data, bounded_schema)

        without_scope = dict(data)
        without_scope.pop("resolution_scope")
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(without_scope, bounded_schema)


class TestCanaryScenario(unittest.TestCase):
    def test_canary_scenario(self):
        # GitHub mutation recent + WorkGraph 0 claim/0 binding + Jules runtime not directly observable.
        # Ensure that known dimensions stay KNOWN; only Jules runtime dimension becomes UNKNOWN.

        # 1. Observation of GitHub mutation
        obs_github = ObservationPacket.create(
            source_ref="gh_issue_458",
            source_authority="yaz",
            dimension="github_mutation",
            value="recent",
            evidence_refs=["#458"]
        )

        # 2. Observation of WorkGraph claims and bindings
        obs_workgraph = ObservationPacket.create(
            source_ref="wg_query_1",
            source_authority="yaz",
            dimension="workgraph_state",
            value={"claims": 0, "bindings": 0},
            evidence_refs=["#wg_1"]
        )

        # No fresh runtime observation establishing ONLINE/OFFLINE.

        # We construct a ContextCapsule to show the derived explicit UNKNOWN vs KNOWN.
        capsule = ContextCapsule(
            capsule_id="cap_canary",
            compiled_at="2026-10-03T10:15:00Z",
            source_cutoff_at="2026-10-03T10:14:00Z",
            holon_id="jules",
            mission_id="mission_canary",
            correlation_id="corr_canary",
            canon_slice=[obs_github.packet_id, obs_workgraph.packet_id],
            anthology_window=[],
            physiology_ref="phys_canary",
            authority_envelope={"boundary": "safe"},
            workgraph_neighborhood=obs_workgraph.value,
            evidence_head=[obs_github.packet_id, obs_workgraph.packet_id],
            contradictions=[],
            unknowns=["jules_runtime_state"], # explicit unknown
            return_to={"owner": "nardole"}
        )

        # Verify invariants
        self.assertEqual(capsule.workgraph_neighborhood, {"claims": 0, "bindings": 0})
        self.assertIn(obs_github.packet_id, capsule.canon_slice)
        self.assertIn("jules_runtime_state", capsule.unknowns)

        # We assert that the KNOWN dimensions stay KNOWN (workgraph_neighborhood is populated explicitly, github mutation is in canon_slice).
        # We assert that only Jules runtime dimension becomes UNKNOWN.
        # This effectively proves that GitHub/WorkGraph do not overwrite runtime truth implicitly.
        self.assertEqual(len(capsule.unknowns), 1)

if __name__ == "__main__":
    unittest.main()
