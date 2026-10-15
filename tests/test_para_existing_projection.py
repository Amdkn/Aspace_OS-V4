"""PARA is the sixth existing framework, not a new institutional topology."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIFE = ROOT / "life" / "holons"

class TestPARAExistingInstitution(unittest.TestCase):
    def test_a2_and_four_a3_drive_residences(self):
        homes = {
          "A2/Computer": "1Ie2Qo205NLE2DWvua8ieLbGuBUKYKQHp",
          "A3/Enterprise/Picard": "17SuVx4Ld0tpYsgL-7l1EWu_O7H81W2ce",
          "A3/Enterprise/Spock": "1KAJ1XJ5nNpkeohmz-g9Z4_wpEMlbY7tP",
          "A3/Enterprise/Geordi": "1xjvsr-NMvCyLnQq9DjbEyKkK6XiICZIz",
          "A3/Enterprise/Data": "1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM",
        }
        for rel, drive_id in homes.items():
            with self.subTest(rel=rel):
                home = LIFE / rel
                for name in ("README.md", "IDENTITY.md", "CONTRACTS.md"):
                    self.assertTrue((home/name).is_file(), str(home/name))
                text = (home/"IDENTITY.md").read_text(encoding="utf-8")
                self.assertIn(drive_id, text)
                self.assertIn("20_Life_OS/24_PARA_Enterprise", text)
                self.assertIn("NOT_CERTIFIED", text)

    def test_six_frameworks_and_existing_parent_relation(self):
        j = json.loads((ROOT/"architecture/cross_os_collaboration.json").read_text(encoding="utf8"))
        self.assertEqual(len(j["frameworks"]), 6)
        self.assertEqual(len(set(x["id"] for x in j["frameworks"])), 6)
        para = next(x for x in j["frameworks"] if x["id"]=="PARA")
        self.assertEqual(para["a2_id"], "aspace:life:a2:computer")
        self.assertEqual(set(para["a3_specialists"]), {"Picard","Spock","Geordi","Data"})
        self.assertEqual(len(j["historic"]), 8)
        self.assertEqual(len(j["tech_to_a3"]), 9)

    def test_no_second_para_home(self):
        self.assertFalse((LIFE/"para"/"Computer"/"AGENTS.md").exists())
        self.assertFalse((LIFE/"A2"/"Picard").exists())
        self.assertTrue((LIFE/"A2"/"Orville").is_dir())
        self.assertTrue((LIFE/"A2"/"Zora").is_dir())


if __name__=="__main__":
    unittest.main()
