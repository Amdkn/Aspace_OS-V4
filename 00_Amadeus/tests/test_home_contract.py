"""A0 documentary smoke test, not a runtime acceptance test."""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
class TestA0Home(unittest.TestCase):
    def test_core_files_present(self):
        for name in ("README.md","AGENT.md","AGENTS.md","SOUL.md","IDENTITY.md","MISSION.md","DESIGN.md","IPBD.md","VISION.md","GOVERNANCE.md","RELATIONS.md","CAPABILITIES.md","MEMORY.md","STATE.md","DECISIONS.md","HANDOFF.md"):
            self.assertTrue((ROOT/name).is_file(),name)
    def test_one_identity(self):
        text=(ROOT/"IDENTITY.md").read_text(encoding="utf-8")
        self.assertIn("aspace:a0:amadeus",text)
    def test_ipbd_integrity(self):
        obj=json.loads((ROOT/"register/ipbd.public.json").read_text(encoding="utf-8"))
        records=obj["records"]; ids=[x["id"] for x in records]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(obj["holon_id"],"aspace:a0:amadeus")
        self.assertTrue(all(x["source_refs"] and x["links"]["return_to"] for x in records))
        self.assertTrue(all(x["privacy"]=="PUBLIC_ABSTRACT_ONLY" for x in records))
if __name__=="__main__": unittest.main()
