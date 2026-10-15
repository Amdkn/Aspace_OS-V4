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


if __name__ == "__main__":
    unittest.main()
