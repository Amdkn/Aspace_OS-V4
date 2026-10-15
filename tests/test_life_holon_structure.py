"""Verify A'Space Life OS has exactly one A2/A3 constitutional home per 12WY/GTD/DEAL identity."""
from __future__ import annotations

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIFE = ROOT / "life" / "holons"

MAPPING = {
    "wy/curie": "A2/Curie",
    "wy/pike": "A3/Curie/Pike",
    "wy/una": "A3/Curie/Una",
    "wy/mbenga": "A3/Curie/MBenga",
    "wy/chapel": "A3/Curie/Chapel",
    "wy/ortegas": "A3/Curie/Ortegas",
    "gtd/holodeck": "A2/HoloDeck",
    "gtd/mariner": "A3/Cerritos/Mariner",
    "gtd/boimler": "A3/Cerritos/Boimler",
    "gtd/rutherford": "A3/Cerritos/Rutherford",
    "gtd/tendi": "A3/Cerritos/Tendi",
    "gtd/freeman": "A3/Cerritos/Freeman",
    "deal/holojaneway": "A2/HoloJaneway",
    "deal/dal": "A3/Protostar/Dal",
    "deal/roktahk": "A3/Protostar/RokTahk",
    "deal/zero": "A3/Protostar/Zero",
    "deal/gwyn": "A3/Protostar/Gwyn",
}
REQUIRED = ("README.md", "SOUL.md", "AGENTS.md", "CONTRACTS.md",
            "CAPABILITIES.md", "RUNBOOK.md", "STATE.md", "MEMORY.md")
MANAGERS = {
    "Curie": ["Pike", "Una", "MBenga", "Chapel", "Ortegas"],
    "HoloDeck": ["Mariner", "Boimler", "Rutherford", "Tendi", "Freeman"],
    "HoloJaneway": ["Dal", "RokTahk", "Zero", "Gwyn"],
}
A3_PARENT = {"Curie": "Curie", "Cerritos": "HoloDeck", "Protostar": "HoloJaneway"}


class LifeHolonLayoutTest(unittest.TestCase):
    def test_17_unique_canonical_homes_all_eight_files(self):
        self.assertEqual(len(MAPPING), 17)
        self.assertEqual(len(set(MAPPING.values())), 17)
        for old, new in MAPPING.items():
            with self.subTest(new=new):
                home = LIFE / new
                self.assertTrue(home.is_dir(), home)
                for filename in REQUIRED:
                    self.assertTrue((home / filename).is_file(), home / filename)
                self.assertIn(old, (home / "README.md").read_text(encoding="utf-8"))
                self.assertIn(new, (home / "CONTRACTS.md").read_text(encoding="utf-8"))

    def test_legacy_paths_are_only_non_agent_aliases(self):
        for old, new in MAPPING.items():
            with self.subTest(old=old):
                historical = LIFE / old
                self.assertEqual({p.name for p in historical.iterdir()}, {"README.md"})
                body = (historical / "README.md").read_text(encoding="utf-8")
                self.assertIn(new, body)
                self.assertIn("alias", body.lower())

    def test_three_relationships_each_holon(self):
        for new in MAPPING.values():
            with self.subTest(home=new):
                contract = (LIFE / new / "CONTRACTS.md").read_text(encoding="utf-8")
                for k in ("Relation 1", "Relation 2", "Relation 3",
                          "mission_id", "correlation_id", "SOH-"):
                    self.assertIn(k, contract)
                self.assertIn("Rattachement", contract.lower().title())

    def test_ownership_manager_and_framework_indices(self):
        self.assertTrue((LIFE / "FRAMEWORKS.md").is_file())
        self.assertEqual(sum(len(v) for v in MANAGERS.values()), 14)
        for manager, specialists in MANAGERS.items():
            with self.subTest(manager=manager):
                idx = (LIFE / "A2" / manager / "FRAMEWORK_INDEX.md").read_text(encoding="utf-8")
                self.assertIn("Rattachement", idx)
                self.assertIn("Coopération", idx)
                self.assertIn("Contribution", idx)
                for n in specialists:
                    self.assertIn(n, idx)
        for branch, manager in A3_PARENT.items():
            for child in (LIFE / "A3" / branch).iterdir():
                if child.is_dir():
                    self.assertIn(manager, (child / "CONTRACTS.md").read_text(encoding="utf-8"))

    def test_preexisting_21_homes_preserved(self):
        for folder in ("A1/Beth", "A1/Morty", "A2/Orville", "A2/Zora",
                       "A3/Discovery/Book", "A3/Discovery/Georgiou",
                       "A3/Orville/Ed_Mercer", "A3/Orville/H1_Isaac"):
            self.assertTrue((LIFE / folder / "AGENTS.md").is_file(), folder)
        self.assertTrue((LIFE / "deal" / "handoff_example_SOH-153.json").is_file())

    def test_framework_links_resolve_locally(self):
        for manager in MANAGERS:
            idx_path = LIFE / "A2" / manager / "FRAMEWORK_INDEX.md"
            data = idx_path.read_text(encoding="utf-8")
            for rel in re.findall(r"\]\((\.{1,2}/[^)#]+\.md)\)", data):
                target = (idx_path.parent / rel).resolve()
                self.assertTrue(target.is_file(), (manager, rel))


if __name__ == "__main__":
    unittest.main()
