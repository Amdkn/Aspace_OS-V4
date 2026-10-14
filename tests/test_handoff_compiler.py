import json
import unittest
from tools.handoff_compiler import capsule, validate

class HandoffCompilerTest(unittest.TestCase):
    def setUp(self):
        self.receipt = dict(
            mission_id="SOH-153", correlation_id="gtd-book-20261014",
            owner="HoloDeck/Boimler", observed_at="2026-10-14",
            latest_native_refs=["https://linear.app/aspace-os/issue/SOH-153",
              "https://drive.google.com/file/d/15iWY1w0FtiJpU9_YNUJngnv6tSL_YOwk/view"],
            last_verified_effect="Book LD01 doc read; PR #22 referenced; no task completed",
            pending_authority="Offer and beneficiary not ratified",
            blocked_outcome="Google Tasks write not certified",
            next_executable_action="Inspect Book LD01 PR #22, identify owner and first service deliverable",
            return_to="Curie/Una; Picard/Book",
            effect_status="OBSERVED")
    def test_capsule(self):
        value = capsule(self.receipt)
        self.assertIn("SOH-153", value)
        self.assertIn("NEXT:", value)
        self.assertIn("no blind retry", value)
    def test_missing_field_fails(self):
        self.receipt.pop("return_to")
        with self.assertRaises(ValueError): validate(self.receipt)
    def test_verified_requires_evidence(self):
        self.receipt["effect_status"] = "VERIFIED"
        with self.assertRaises(ValueError): validate(self.receipt)

if __name__ == "__main__":
    unittest.main()
