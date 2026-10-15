import json
import unittest
from pathlib import Path
from tools.holon_route import resolve, sample_cases

ROOT = Path(__file__).resolve().parents[1]
REG = json.loads((ROOT / "architecture/cross_os_collaboration.json").read_text(encoding="utf-8"))


class TestCrossOSDecisionCanary(unittest.TestCase):
    def test_normal_bill_tilly_mission(self):
        r = resolve(sample_cases()[0], REG)
        self.assertEqual(r["status"], "OWNER_REVIEW_READY_NOT_EXECUTED")
        self.assertEqual(r["life_result_owner"], "aspace:life:a3:discovery:tilly")
        self.assertEqual(r["jerry_standard_owner"], "aspace:business:E1")
        self.assertEqual(r["manager_delivery_owner"], "aspace:business:E2:PRD")
        self.assertEqual(r["squad_executor"], "aspace:business:E3:PRD")
        self.assertEqual(r["tech_supervisor"], "doctor-12")
        self.assertEqual(r["runtime_status"], "NOT_VERIFIED")
        self.assertFalse(r["delegated_execution"])

    def test_life_value_disagreement(self):
        r = resolve(sample_cases()[1], REG)
        self.assertEqual(r["status"], "DISAGREEMENT_REQUIRES_DECISION")
        self.assertEqual(r["next_decision_owner"], "aspace:life:a1:beth")
        self.assertEqual(r["life_result_owner"], "aspace:life:a3:discovery:tilly")
        self.assertFalse(r["delegated_execution"])

    def test_omitted_owner_is_not_silently_replaced(self):
        r = resolve(sample_cases()[2], REG)
        self.assertEqual(r["status"], "OWNER_UNAVAILABLE")
        self.assertEqual(r["next_decision_owner"], "aspace:life:a1:morty")
        self.assertEqual(r["observed_effect"], "UNKNOWN")
        self.assertFalse(r["delegated_execution"])

    def test_area_and_tech_disputes_keep_jurisdictions(self):
        common = sample_cases()[0]
        for axis, expected in [
            ("area_standard", "aspace:business:E1"),
            ("tech_capacity", "aspace:tech:doctors:council"),
            ("jurisdiction", "aspace:life:a1:morty"),
        ]:
            with self.subTest(axis=axis):
                r = resolve(dict(common, disagreement={"axis": axis}), REG)
                self.assertEqual(r["next_decision_owner"], expected)

    def test_all_eight_historical_domains_are_preserved(self):
        for e in REG["historic"]:
            with self.subTest(ld=e["life_domain"]):
                m = dict(sample_cases()[0], life_domain=e["life_domain"])
                m.pop("requested_tech_holon_id")
                r = resolve(m, REG)
                self.assertEqual(r["life_result_owner"], e["life_a3_id"])
                self.assertEqual(r["jerry_standard_owner"], e["jerry_id"])
                self.assertEqual(r["manager_delivery_owner"], e["historic_anchor_manager_id"])
                self.assertEqual(r["squad_executor"], e["historic_anchor_squad_id"])

    def test_read_only_routing_refuses_unknown_or_unbound_scope(self):
        with self.assertRaises(ValueError):
            resolve(dict(sample_cases()[0], requested_tech_holon_id="aspace:tech:fake"), REG)
        with self.assertRaises(ValueError):
            resolve(dict(sample_cases()[0], life_domain="LD09"), REG)
        self.assertEqual(resolve(dict(sample_cases()[0], authority_ref=None), REG)["status"], "AUTHORITY_UNRESOLVED")
        self.assertEqual(resolve(dict(sample_cases()[0], native_ref=None), REG)["status"], "NATIVE_REF_UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
