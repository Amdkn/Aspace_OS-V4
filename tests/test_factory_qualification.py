import json
import tempfile
import unittest
from pathlib import Path

from tools.factory_qualify import qualify, to_handoff, ROOT
from tools.handoff_compiler import capsule, validate


class FactoryQualificationTest(unittest.TestCase):
    def test_source_qualification_without_worker(self):
        obj = qualify()
        self.assertEqual(obj["mission_id"], "SOH-148")
        self.assertEqual(obj["correlation_id"], "CORR-BILL-TILLY-20261014")
        self.assertEqual(obj["decision"], "REJECT_UNSCOPED_AUTO_DISPATCH_ACCEPT_EXPLICIT_OPT_IN_REUSE")
        self.assertTrue(obj["no_external_effects"])
        self.assertEqual(obj["authority_status"], "AUTHORITY_UNVERIFIED")
        self.assertIsNone(obj["selected_business_function"])
        self.assertEqual(obj["historical_business_anchor"], "aspace:business:E2:PRD")
        self.assertEqual(len(obj["source_sha256"]), 5)

    def test_new_issue_requires_explicit_opt_in(self):
        text = (ROOT/".github/workflows/auto-label-factory-ready.yml").read_text()
        self.assertIn("factory:opt-in", text)
        self.assertIn("no-factory", text)
        self.assertNotIn("!contains(join(github.event.issue.labels", text)

    def test_second_process_can_resume_from_native_receipt(self):
        obj = qualify()
        receipt = to_handoff(obj)
        validate(receipt)
        with tempfile.TemporaryDirectory() as d:
            f = Path(d)/"receipt.json"
            f.write_text(json.dumps(receipt), encoding="utf-8")
            independent = json.loads(f.read_text(encoding="utf-8"))
            text = capsule(independent)
        self.assertIn("CORR-BILL-TILLY-20261014", text)
        self.assertIn("NEXT:", text)
        self.assertIn("SOH-148", text)
        self.assertIn("no blind retry", text)

    def test_qualification_has_no_provider_side_effects(self):
        source = (ROOT/"tools/factory_qualify.py").read_text(encoding="utf-8")
        self.assertNotIn("urlopen(", source)
        self.assertNotIn("subprocess.", source)
        self.assertNotIn("gh issue edit", source)
        self.assertNotIn("post_to_jules", source)


if __name__=="__main__":
    unittest.main()
