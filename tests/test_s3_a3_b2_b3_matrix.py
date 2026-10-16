import json
import unittest
from pathlib import Path

from tools.s3_a3_b2_b3_matrix import (
    AGENTS, BUSINESS, CROSS_OS, LIFE, build_matrix, resolve_cooperation,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


MATRIX = build_matrix(load(CROSS_OS), load(BUSINESS), load(LIFE), load(AGENTS))


class TestS3A3B2B3Matrix(unittest.TestCase):
    def test_complete_eight_domain_composition(self):
        self.assertEqual(
            [row["life_domain"] for row in MATRIX["domains"]],
            [f"LD{i:02d}" for i in range(1, 9)],
        )
        self.assertEqual(
            sum(len(row["functions_b2_b3"]) for row in MATRIX["domains"]), 64
        )
        for row in MATRIX["domains"]:
            self.assertEqual(len(row["functions_b2_b3"]), 8)
            self.assertEqual(
                len({f["function"] for f in row["functions_b2_b3"]}), 8
            )
            for pair in row["functions_b2_b3"]:
                self.assertTrue(pair["b2_id"])
                self.assertTrue(pair["b3_id"])
                self.assertEqual(pair["dispatch_status"], "NOT_SELECTED")

    def test_historical_anchor_is_separate_from_selectable_function(self):
        for row in MATRIX["domains"]:
            anchor = row["historical_anchor"]
            self.assertTrue(anchor["relation_id"].startswith("LIFE-BIZ-HIST-"))
            self.assertIn(
                anchor["b2_id"], {pair["b2_id"] for pair in row["functions_b2_b3"]}
            )
            self.assertIn(
                anchor["b3_id"], {pair["b3_id"] for pair in row["functions_b2_b3"]}
            )
            self.assertEqual(
                row["jerry"]["id"], load(BUSINESS)["directions"][
                    int(row["life_domain"][-2:]) - 1
                ]["id"]
            )

    def test_s3_catalog_preserves_doctor_and_relationship_status(self):
        self.assertEqual(len(MATRIX["s3_capability_catalog"]), 9)
        self.assertEqual(set(MATRIX["doctors"]), {
            "doctor-11", "doctor-12", "doctor-13"
        })
        for candidate in MATRIX["s3_capability_catalog"]:
            self.assertTrue(candidate["supervising_doctor"])
            self.assertIn(
                candidate["relationship_status"],
                {"USER_EXPLICIT", "PROPOSED_FUNCTIONAL", "PROPOSED_NON_EXCLUSIVE"},
            )
        ld04 = next(row for row in MATRIX["domains"] if row["life_domain"] == "LD04")
        ids = {x["holon_id"]: x for x in ld04["s3_candidates"]}
        self.assertEqual(ids["aspace:tech:bill"]["relationship_status"], "USER_EXPLICIT")
        self.assertEqual(ids["aspace:tech:graham"]["relationship_status"], "PROPOSED_FUNCTIONAL")
        ld01_candidates = {
            x["holon_id"]: x
            for x in MATRIX["domains"][0]["s3_candidates"]
        }
        self.assertIn("aspace:tech:bill", ld01_candidates)
        self.assertEqual(
            ld01_candidates["aspace:tech:bill"]["association"],
            "CROSS_DOMAIN_NON_EXCLUSIVE",
        )
        self.assertFalse(
            ld01_candidates["aspace:tech:bill"]["preferred_a3_match"]
        )

    def test_a2_frameworks_are_composable_across_domains(self):
        self.assertEqual(len(MATRIX["domains"][0]["a2_frameworks"]), 6)
        self.assertEqual(
            {item["id"] for item in MATRIX["domains"][0]["a2_frameworks"]},
            {"Ikigai", "Discovery", "PARA", "12WY", "GTD", "DEAL"},
        )
        ld04 = next(row for row in MATRIX["domains"] if row["life_domain"] == "LD04")
        selected = resolve_cooperation(
            MATRIX, "LD04", business_function="PRD",
            tech_holon_id="aspace:tech:bill", required_capability="research",
            framework_ids=["Discovery", "GTD"],
        )
        self.assertEqual(selected["a3_owner"]["steward"], "Tilly")
        self.assertEqual(selected["business_assignment"]["b2_id"], "aspace:business:E2:PRD")
        self.assertEqual(selected["business_assignment"]["b3_id"], "aspace:business:E3:PRD")
        self.assertEqual(
            selected["s3_assignment"]["dispatch_status"],
            "CAPABILITY_MATCH_NOT_DISPATCHED",
        )
        self.assertEqual(
            [framework["id"] for framework in selected["frameworks"]],
            ["Discovery", "GTD"],
        )
        self.assertEqual(selected["runtime_status"], "NOT_DISPATCHED")
        self.assertEqual(ld04["owner_decision"], "A3_STEWARD")

    def test_invalid_domain_function_or_capability_fails_closed(self):
        with self.assertRaises(ValueError):
            resolve_cooperation(MATRIX, "LD09")
        with self.assertRaises(ValueError):
            resolve_cooperation(MATRIX, "LD04", business_function="NOPE")
        with self.assertRaises(ValueError):
            resolve_cooperation(MATRIX, "LD04", required_capability="unregistered")


if __name__ == "__main__":
    unittest.main()
