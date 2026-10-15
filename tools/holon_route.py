#!/usr/bin/env python3
"""Read-only mission routing against the existing CROSS_OS collaboration registry."""
import argparse
import json
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "architecture" / "cross_os_collaboration.json"


def resolve(mission, registry):
    for key in ("mission_id", "correlation_id", "life_domain"):
        if not isinstance(mission.get(key), str) or not mission[key].strip():
            raise ValueError("required mission field: " + key)
    anchors = [entry for entry in registry["historic"] if entry["life_domain"] == mission["life_domain"]]
    if len(anchors) != 1:
        raise ValueError("life_domain must resolve exactly one historical domain anchor")
    anchor = anchors[0]
    tech_id = mission.get("requested_tech_holon_id")
    tech = None
    if tech_id is not None:
        eligible = [e for e in registry["tech_to_a3"]
                    if e["tech_holon_id"] == tech_id and
                    e["life_a3_id"] in (anchor["life_a3_id"], "ANY_A3_AS_NEEDED")]
        if len(eligible) != 1:
            raise ValueError("tech collaborator not supported for mission domain")
        tech = eligible[0]
    result = {
        "mission_id": mission["mission_id"], "correlation_id": mission["correlation_id"],
        "life_domain": anchor["life_domain"],
        "life_result_owner": anchor["life_a3_id"],
        "jerry_standard_owner": anchor["jerry_id"],
        "manager_delivery_owner": anchor["historic_anchor_manager_id"],
        "squad_executor": anchor["historic_anchor_squad_id"],
        "historical_anchor_only": True,
        "tech_advisor": tech_id,
        "tech_supervisor": tech["doctor"] if tech else None,
        "native_ref": mission.get("native_ref"),
        "authority_ref": mission.get("authority_ref"),
        "observed_effect": "UNKNOWN", "runtime_status": "NOT_VERIFIED",
        "return_to": mission.get("return_to") or anchor["life_a3_id"],
        "delegated_execution": False,
    }
    unavailable = mission.get("unavailable_ids", [])
    if not isinstance(unavailable, list) or not all(isinstance(v, str) for v in unavailable):
        raise ValueError("unavailable_ids must be a list of IDs")
    if anchor["life_a3_id"] in unavailable:
        result.update(status="OWNER_UNAVAILABLE", next_decision_owner="aspace:life:a1:morty",
                      next_decision="Verify durable ownership and authorised succession; Nardole may coordinate the lease, but no worker may self-promote. Pause effects.")
    elif mission.get("disagreement"):
        conflict = mission["disagreement"]
        if not isinstance(conflict, dict):
            raise ValueError("disagreement must be an object")
        authorities = {
            "life_value": ("aspace:life:a1:beth", "Arbitrate values and LD acceptance with A3; tech cannot override life outcome."),
            "area_standard": (anchor["jerry_id"], "Jerry arbitrates Area standard, A3 keeps human acceptance; Morty mediates unresolved scope."),
            "tech_capacity": (tech["tech_holon_id"].replace(":bill", ":doctor-12") if tech else "aspace:tech:doctor-12", "Doctor 12 raises cross-Core conflict to existing S2 council; Rick observes systemic failures."),
            "jurisdiction": ("aspace:life:a1:morty", "Reconcile overlapping mandates without reparenting any holon; escalate constitutional change to A0."),
        }
        axis = conflict.get("axis")
        if axis not in authorities:
            raise ValueError("unknown disagreement axis")
        owner, decision = authorities[axis]
        result.update(status="DISAGREEMENT_REQUIRES_DECISION", next_decision_owner=owner,
                      next_decision=decision, objection=conflict.get("reason", "UNSPECIFIED"))
    elif not mission.get("native_ref"):
        result.update(status="NATIVE_REF_UNRESOLVED", next_decision_owner=anchor["life_a3_id"],
                      next_decision="Identify existing native project/issue and actual mission instance before an effect.")
    elif not mission.get("authority_ref"):
        result.update(status="AUTHORITY_UNRESOLVED", next_decision_owner=anchor["life_a3_id"],
                      next_decision="Resolve required authority for the requested effect; read-only observation may continue.")
    else:
        result.update(status="OWNER_REVIEW_READY_NOT_EXECUTED", next_decision_owner=anchor["life_a3_id"],
                      next_decision="A3 confirms expected life effect and acceptance; Jerry/B2/B3 and S3 perform only separately authorised work; return receipt to A3.")
    return result


def sample_cases():
    common = {
        "mission_id": "SOH-148", "correlation_id": "CORR-BILL-TILLY-20261014",
        "life_domain": "LD04", "requested_tech_holon_id": "aspace:tech:bill",
        "native_ref": "https://linear.app/aspace-os/issue/SOH-148",
        "authority_ref": "SOH-148:read-only-research",
        "return_to": "aspace:life:a3:discovery:tilly",
    }
    return [
        dict(common),
        dict(common, disagreement={"axis": "life_value", "reason": "video advice would displace a family or learning priority"}),
        dict(common, unavailable_ids=["aspace:life:a3:discovery:tilly"]),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", action="store_true", help="Show three read-only Bill/Tilly governance scenarios")
    parser.add_argument("--mission-json", type=Path, help="Read JSON mission descriptor; no network or mutations")
    args = parser.parse_args()
    if not args.cases and not args.mission_json:
        parser.error("pass --cases or --mission-json")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    missions = sample_cases() if args.cases else [json.loads(args.mission_json.read_text(encoding="utf-8"))]
    print(json.dumps([resolve(m, registry) for m in missions], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
