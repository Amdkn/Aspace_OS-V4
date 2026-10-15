import copy
import unittest

from tools.factory_qualify import qualify, to_handoff
from tools.factory_resume import replay


class IndependentFactoryReplayTests(unittest.TestCase):
    def setUp(self):
        self.q = qualify()
        self.receipt = to_handoff(self.q)

    def test_replay_from_existing_receipt_no_external_effect(self):
        result = replay(self.q, self.receipt)
        self.assertTrue(result["source_fingerprints_match"])
        self.assertTrue(result["context_reconstructed_without_A0"])
        self.assertEqual(result["external_effect"], "NOT_EXECUTED")
        self.assertEqual(result["independent_companion_agent"], "NOT_PROVEN")
        self.assertEqual(result["return_to"], "aspace:life:a3:discovery:tilly")

    def test_tampered_source_or_decision_fails_closed(self):
        tampered = copy.deepcopy(self.q)
        tampered["source_sha256"]["tools/issue_factory.py"] = "bad"
        with self.assertRaises(ValueError):
            replay(tampered, self.receipt)
        t2 = copy.deepcopy(self.receipt)
        t2["return_to"] = "unrelated"
        with self.assertRaises(ValueError):
            replay(self.q, t2)
        t3 = copy.deepcopy(self.receipt)
        t3["effect_status"] = "VERIFIED"
        with self.assertRaises(ValueError):
            replay(self.q, t3)



    def test_next_executable_action_cannot_be_substituted(self):
        tampered = copy.deepcopy(self.receipt)
        tampered["next_executable_action"] = "AUDIT: arbitrary substituted instruction"
        with self.assertRaisesRegex(ValueError, "next_executable_action"):
            replay(self.q, tampered)

    def test_authority_and_semantic_receipt_fields_cannot_drift(self):
        for field, value in (
            ("pending_authority", "permission granted without proof"),
            ("blocked_outcome", "human outcome done"),
            ("latest_native_refs", ["https://example.invalid/other"]),
            ("owner", "different owner"),
            ("last_verified_effect", "published externally"),
            ("evidence_refs", ["https://example.invalid/fake"]),
        ):
            with self.subTest(field=field):
                tampered = copy.deepcopy(self.receipt)
                tampered[field] = value
                with self.assertRaises(ValueError):
                    replay(self.q, tampered)

    def test_qualification_semantic_field_cannot_drift(self):
        tampered = copy.deepcopy(self.q)
        tampered["authority_status"] = "AUTHORITY_VERIFIED_FOR_ROUTE_ONLY"
        with self.assertRaisesRegex(ValueError, "authority_status"):
            replay(tampered, self.receipt)

    def test_observed_at_must_be_timezone_aware(self):
        tampered = copy.deepcopy(self.receipt)
        tampered["observed_at"] = "2026-10-15T15:00:00"
        with self.assertRaisesRegex(ValueError, "observed_at"):
            replay(self.q, tampered)

if __name__ == "__main__":
    unittest.main()
