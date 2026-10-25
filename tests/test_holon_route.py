import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tools.holon_route import resolve, sample_cases, verify_grant

ROOT = Path(__file__).resolve().parents[1]
REG = json.loads((ROOT / "architecture/cross_os_collaboration.json").read_text(encoding="utf-8"))
BIZ = json.loads((ROOT / "business/holons/registry.json").read_text(encoding="utf-8"))
NOW = datetime(2026, 10, 15, tzinfo=timezone.utc)


class TestCrossOSDecisionCanary(unittest.TestCase):
    def mission(self, **updates):
        m = copy.deepcopy(sample_cases()[0])
        m.update(updates)
        return m

    def test_historical_anchor_not_forced_as_assignment(self):
        r = resolve(self.mission(business_function=None), REG, BIZ)
        self.assertEqual(r["historical_anchor_manager_id"], "aspace:business:E2:PRD")
        self.assertIsNone(r["manager_delivery_owner"])
        self.assertIsNone(r["squad_executor"])
        self.assertEqual(r["business"]["assignment_status"], "NO_FUNCTION_SELECTED")

    def test_select_other_function_without_destroying_anchor(self):
        r = resolve(self.mission(business_function="IT"), REG, BIZ)
        self.assertEqual(r["manager_delivery_owner"], "aspace:business:E2:IT")
        self.assertEqual(r["squad_executor"], "aspace:business:E3:IT")
        self.assertEqual(r["historical_anchor_manager_id"], "aspace:business:E2:PRD")
        self.assertEqual(len(r["business"]["available_functions"]), 8)
        self.assertFalse(r["delegated_execution"])
        self.assertEqual(r["business"]["assignment_status"], "PROPOSED_NOT_DISPATCHED")

    def test_core_router_emits_composed_cross_holon_matrix(self):
        r = resolve(self.mission(
            business_function="PRD",
            requested_tech_holon_id="aspace:tech:bill",
            requested_capability="research",
            framework_contributions=["Discovery", "GTD"],
        ), REG, BIZ)
        cooperation = r["cooperation"]
        self.assertEqual(cooperation["matrix_schema"], "aspace.s3_a3_b2_b3_matrix.v1")
        self.assertEqual(len(cooperation["available_business_functions"]), 8)
        self.assertEqual(len(cooperation["available_s3_candidates"]), 9)
        self.assertEqual(len(cooperation["a2_framework_contributions"]), 6)
        selection = cooperation["mission_selection"]
        self.assertEqual(selection["a3_owner"]["steward"], "Tilly")
        self.assertEqual(selection["business_assignment"]["b2_id"], "aspace:business:E2:PRD")
        self.assertEqual(selection["business_assignment"]["b3_id"], "aspace:business:E3:PRD")
        self.assertEqual(selection["s3_assignment"]["holon_id"], "aspace:tech:bill")
        self.assertEqual([x["id"] for x in selection["frameworks"]], ["Discovery", "GTD"])
        self.assertEqual(selection["runtime_status"], "NOT_DISPATCHED")

    def test_all_eight_domains_historical_anchors_preserved(self):
        for h in REG["historic"]:
            with self.subTest(h["life_domain"]):
                r = resolve(self.mission(life_domain=h["life_domain"], business_function=None,
                                         requested_tech_holon_id=None), REG, BIZ)
                self.assertEqual(r["life_result_owner"], h["life_a3_id"])
                self.assertEqual(r["jerry_standard_owner"], h["jerry_id"])
                self.assertEqual(r["historical_anchor_manager_id"], h["historic_anchor_manager_id"])
                self.assertEqual(len(r["business"]["available_functions"]), 8)

    def test_nonexclusive_graham_and_bill_across_domains(self):
        for tech, capability in [("graham", "memory"), ("bill", "research")]:
            r = resolve(self.mission(life_domain="LD06", business_function=None,
                                     requested_tech_holon_id="aspace:tech:" + tech,
                                     requested_capability=capability), REG, BIZ)
            self.assertEqual(r["tech_contribution"]["capability"], capability)
            self.assertFalse(r["tech_contribution"]["preferred_relation"])
            self.assertTrue(r["tech_contribution"]["nonexclusive"])
            self.assertEqual(r["tech_contribution"]["doctor"], "doctor-13" if tech == "graham" else "doctor-12")
            self.assertEqual(
                r["cooperation"]["mission_selection"]["s3_assignment"]["association"],
                "CROSS_DOMAIN_NON_EXCLUSIVE",
            )
            self.assertFalse(
                r["cooperation"]["mission_selection"]["s3_assignment"]["preferred_a3_match"]
            )

    def test_only_requested_frameworks_contribute(self):
        r = resolve(self.mission(framework_contributions=["PARA", "DEAL", "12WY"]), REG, BIZ)
        self.assertEqual([x["framework"] for x in r["framework_contributions"]], ["PARA", "DEAL", "12WY"])
        self.assertEqual(len(next(x for x in r["framework_contributions"] if x["framework"] == "PARA")["a3_specialists"]), 4)
        self.assertNotIn("GTD", [x["framework"] for x in r["framework_contributions"]])
        self.assertEqual([x["status"] for x in r["framework_contributions"]], ["REQUESTED_NOT_EXECUTED"] * 3)

    def test_mission_without_framework_still_routable(self):
        r = resolve(self.mission(framework_contributions=[]), REG, BIZ)
        self.assertEqual(r["framework_contributions"], [])

    def test_unavailable_owner_then_morty_then_beth(self):
        owner = "aspace:life:a3:discovery:tilly"
        morty = "aspace:life:a1:morty"
        beth = "aspace:life:a1:beth"
        a = resolve(self.mission(unavailable_ids=[owner]), REG, BIZ)
        b = resolve(self.mission(unavailable_ids=[owner, morty]), REG, BIZ)
        c = resolve(self.mission(unavailable_ids=[owner, morty, beth]), REG, BIZ)
        self.assertEqual((a["status"], a["next_decision_owner"]), ("OWNER_UNAVAILABLE", morty))
        self.assertEqual((b["status"], b["next_decision_owner"]), ("SUCCESSION_REVIEW_REQUIRED", beth))
        self.assertEqual(c["status"], "WAIT_NO_AUTHORIZED_SUCCESSOR")
        self.assertIsNone(c["next_decision_owner"])
        self.assertTrue(all(not x["delegated_execution"] for x in [a, b, c]))

    def test_doctor_11_language_not_hardcoded_to_12(self):
        r = resolve(self.mission(requested_tech_holon_id="aspace:tech:amy",
                                 requested_capability="interfaces",
                                 disagreement={"axis": "tech_capacity"}), REG, BIZ)
        self.assertEqual(r["council"]["next_decision_owner"], "aspace:tech:doctor-11")
        self.assertEqual(r["council"]["participants"], ["doctor-11"])

    def test_cross_core_goes_to_council_not_single_doctor(self):
        r = resolve(self.mission(disagreement={"axis": "tech_capacity"},
                                 additional_doctors=["doctor-11", "doctor-13"]), REG, BIZ)
        self.assertEqual(r["council"]["status"], "S2_COUNCIL_REVIEW")
        self.assertIsNone(r["next_decision_owner"])
        self.assertEqual(len(r["council"]["participants"]), 3)
        self.assertEqual(r["council"]["chair_for_systemic_review"], "aspace:tech:rick")

    def test_objection_response_revision_and_appeal(self):
        a = resolve(self.mission(disagreement={"axis": "life_value", "reason": "Value conflict"}), REG, BIZ)
        b = resolve(self.mission(disagreement={"axis": "life_value"}, objection_response="Reasoned response",
                                 revision_ref="issue:amendment", appeal_ref="issue:appeal"), REG, BIZ)
        self.assertEqual(a["status"], "OBJECTION_AWAITING_MOTIVATED_RESPONSE")
        self.assertEqual(a["next_decision_owner"], "aspace:life:a1:beth")
        self.assertEqual(b["status"], "REVISION_OR_APPEAL_REVIEW")
        self.assertEqual(b["appeal_status"], "PENDING_REVIEW_NOT_SELF_RATIFIED")

    def test_fake_grant_never_satisfies_authority(self):
        for ref in ["SOH-148:read-only-research", "{}", {"grant_id": "invented"}]:
            with self.subTest(ref=ref):
                r = resolve(self.mission(authority_ref=ref), REG, BIZ)
                self.assertEqual(r["status"], "AUTHORITY_UNVERIFIED")

    def test_external_verified_snapshot_scopes_and_revoke(self):
        ref = "https://linear.app/aspace-os/issue/SOH-148"
        grant = {"status": "active", "issuer": "Morty", "evidence_ref": "signed-or-sourced-external-grant",
                 "mission_id": "SOH-148", "life_domain": "LD04", "native_ref": ref,
                 "actions": ["research.read"],
                 "not_before": "2026-10-14T00:00:00Z", "expires_at": "2026-10-17T00:00:00Z"}
        registry = {"source_verified": True, "grants": {"g1": grant}}
        m = self.mission(authority_ref={"grant_id": "g1"}, requested_action="research.read")
        r = resolve(m, REG, BIZ, registry, NOW)
        self.assertEqual(r["status"], "OWNER_REVIEW_READY_NOT_EXECUTED")
        self.assertFalse(r["delegated_execution"])
        self.assertEqual(resolve(self.mission(authority_ref={"grant_id": "g1"}, requested_action="deploy"),
                                 REG, BIZ, registry, NOW)["status"], "AUTHORITY_SCOPE_MISMATCH")
        revoked = copy.deepcopy(registry)
        revoked["grants"]["g1"]["revoked_at"] = "2026-10-15T01:00:00Z"
        self.assertEqual(resolve(m, REG, BIZ, revoked, NOW)["status"], "AUTHORITY_REVOKED")
        self.assertEqual(resolve(m, REG, BIZ, registry, datetime(2026, 10, 18, tzinfo=timezone.utc))["status"],
                         "AUTHORITY_EXPIRED")
        self.assertEqual(verify_grant(m, {"source_verified": False, "grants": {"g1": grant}}, NOW)[0],
                         "AUTHORITY_UNVERIFIED")

    def test_invalid_tech_and_function_are_rejected(self):
        with self.assertRaises(ValueError):
            resolve(self.mission(requested_tech_holon_id="aspace:tech:nope"), REG, BIZ)
        with self.assertRaises(ValueError):
            resolve(self.mission(requested_tech_holon_id="aspace:tech:amy",
                                 requested_capability="research"), REG, BIZ)
        with self.assertRaises(ValueError):
            resolve(self.mission(business_function="UNKNOWN"), REG, BIZ)
        with self.assertRaises(ValueError):
            resolve(self.mission(framework_contributions=["DEAL", "DEAL"]), REG, BIZ)
        with self.assertRaises(ValueError):
            resolve(self.mission(life_domain="LD09"), REG, BIZ)

    def test_evidence_never_becomes_external_effect(self):
        for m in sample_cases():
            r = resolve(m, REG, BIZ)
            self.assertFalse(r["delegated_execution"])
            self.assertEqual(r["observed_effect"], "UNKNOWN")
            self.assertEqual(r["runtime_status"], "NOT_VERIFIED")



    def test_multi_core_council_exists_without_objection_but_does_not_execute(self):
        r = resolve(self.mission(disagreement=None,
                                 additional_doctors=["doctor-11", "doctor-13"]), REG, BIZ)
        self.assertEqual(r["council"]["status"], "S2_COUNCIL_REVIEW")
        self.assertEqual(r["coordination_status"], "S2_REVIEW_REQUESTED_NOT_EXECUTED")
        self.assertEqual(r["council"]["participants"], ["doctor-11", "doctor-12", "doctor-13"])
        self.assertFalse(r["delegated_execution"])
        self.assertEqual(r["runtime_status"], "NOT_VERIFIED")

    def test_single_core_routing_has_no_unnecessary_council(self):
        r = resolve(self.mission(disagreement=None, additional_doctors=[]), REG, BIZ)
        self.assertNotIn("council", r)
        self.assertNotIn("coordination_status", r)

    def test_malformed_additional_doctors_rejected(self):
        with self.assertRaises(ValueError):
            resolve(self.mission(additional_doctors="doctor-11"), REG, BIZ)

if __name__ == "__main__":
    unittest.main()
