"""Structural regression for sourced Tech and Business OS institutions.

These checks certify repository constitution, NOT runtime agents or business outcomes.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TECH = ROOT / "tech" / "holons"
BIZ = ROOT / "business" / "holons"
REQUIRED = ("README.md", "IDENTITY.md", "SOUL.md", "AGENTS.md",
            "MISSION.md", "CONTRACTS.md", "CAPABILITIES.md",
            "RUNBOOK.md", "MEMORY.md", "STATE.md")
CODES = {"GRO", "SAL", "PRD", "OPS", "IT", "FIN", "PPL", "LEG"}
DIRECTIONS = "BCDEFGHI"


class InstitutionalHolonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tech = json.loads((ROOT / "agents" / "registry.json").read_text(encoding="utf-8"))
        cls.bindings = json.loads((TECH / "bindings.json").read_text(encoding="utf-8"))
        cls.business = json.loads((BIZ / "registry.json").read_text(encoding="utf-8"))

    def assert_home(self, home):
        self.assertTrue(home.is_dir(), str(home))
        for filename in REQUIRED:
            self.assertTrue((home / filename).is_file(), str(home / filename))
            self.assertGreater((home / filename).stat().st_size, 80, str(home / filename))

    def test_tech_13_unique_homes_and_existing_registry(self):
        names = set(self.tech["profiles"])
        self.assertEqual(len(names), 13)
        refs = self.bindings["records"]
        self.assertEqual({x["registry_key"] for x in refs}, names)
        self.assertEqual(len({x["id"] for x in refs}), 13)
        for item in refs:
            key = item["registry_key"]
            with self.subTest(key=key):
                self.assert_home(TECH / key)
                self.assertEqual(item["id"], f"aspace:tech:{key}")
                self.assertIn("drive.google.com/drive/folders/", item["drive_folder"])
                self.assertEqual(item["session_active"], "NOT_VERIFIED")
                self.assertEqual(item["context_loaded"], "NOT_VERIFIED")
                profile = ROOT / item["github_profile"]
                self.assertTrue(profile.is_file(), profile)
                self.assertIn(f"tech/holons/{key}", profile.read_text(encoding="utf-8"))
                contract = (TECH / key / "CONTRACTS.md").read_text(encoding="utf-8")
                for field in ("mission_id", "correlation_id", "return_to"):
                    self.assertIn(field, contract)

    def test_business_137_unique_homes_and_canonical_ownership(self):
        r = self.business
        self.assertEqual(len(r["directions"]), 8)
        self.assertEqual(len(r["managers"]), 64)
        self.assertEqual(len(r["squads"]), 64)
        self.assertEqual(r["j1"]["role"], "aggregator_not_LD09")
        all_items = r["directions"] + r["managers"] + r["squads"] + [r["j1"]]
        self.assertEqual(len(all_items), 137)
        self.assertEqual(len({x["id"] for x in all_items}), 137)
        self.assertEqual(len({x["home"] for x in all_items}), 137)
        for item in all_items:
            with self.subTest(home=item["home"]):
                self.assert_home(BIZ / item["home"])
        self.assertEqual({x["home"] for x in r["directions"]},
                         {f"B1/{c}1" for c in DIRECTIONS})
        self.assertEqual({x["home"] for x in r["managers"]},
                         {f"B2/{c}2/{code}" for c in DIRECTIONS for code in CODES})
        self.assertEqual({x["home"] for x in r["squads"]},
                         {f"B3/{c}3/{code}" for c in DIRECTIONS for code in CODES})
        dirs = {x["id"] for x in r["directions"]}
        managers = {x["id"] for x in r["managers"]}
        for x in r["managers"]:
            self.assertIn(x["parent"], dirs)
            self.assertTrue(x["playbook"].startswith("https://"))
            self.assertIn(x["child"], {z["id"] for z in r["squads"]})
        for x in r["squads"]:
            self.assertIn(x["parent"], managers)
            self.assertTrue(x["runbook"].startswith("https://"))
            self.assertTrue(x["physical_folder"].startswith("https://"))
            contract = (BIZ / x["home"] / "CONTRACTS.md").read_text(encoding="utf-8")
            self.assertIn("mission_id", contract)
            self.assertIn("correlation_id", contract)
            self.assertIn("return_to", contract)

    def test_original_drive_reference_counts(self):
        r = self.business
        c_to_i = [x for x in r["squads"] if not x["home"].startswith("B3/B3/")]
        self.assertEqual(len(c_to_i), 56)
        self.assertEqual(len({x["runbook"] for x in c_to_i}), 56)
        self.assertEqual(len({x["physical_folder"] for x in c_to_i}), 56)
        self.assertTrue(all("docs.google.com/document/d/" in x["runbook"] for x in c_to_i))
        ld01 = [x for x in r["squads"] if x["home"].startswith("B3/B3/")]
        self.assertEqual(len(ld01), 8)
        self.assertTrue(all("drive.google.com/file/d/" in x["runbook"] for x in ld01))
        self.assertTrue((BIZ / "J1" / "README.md").is_file())

    def test_provider_authority_separate_from_workflow(self):
        contract = (ROOT / "agents" / "CONTRACT.md").read_text(encoding="utf-8")
        implementation = (ROOT / "agents" / "README.md").read_text(encoding="utf-8")
        for text in (contract, implementation):
            self.assertIn("tech/holons", text)
        self.assertIn("auto-merge", contract.lower())
        self.assertIn("Issue Factory", implementation)

    def test_no_fake_running_status_or_private_details_in_registries(self):
        self.assertEqual(self.business["runtime_status"], "NOT_VERIFIED")
        self.assertEqual(self.bindings["runtime_deployment"], "NOT_VERIFIED")
        self.assertEqual(len(self.bindings["records"]), 13)


if __name__ == "__main__":
    unittest.main()
