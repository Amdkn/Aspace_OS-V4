#!/usr/bin/env python3
"""Deterministic read-only cross-OS mission composer (no workers, no side effects).

Historical anchorage != functional assignment. Advice != ownership.
A mission descriptor is untrusted input, not a grant of authority.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

if __package__:
    from .s3_a3_b2_b3_matrix import build_matrix, resolve_cooperation
else:  # Direct invocation: python tools/holon_route.py
    from s3_a3_b2_b3_matrix import build_matrix, resolve_cooperation

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "architecture" / "cross_os_collaboration.json"
BUSINESS = ROOT / "business" / "holons" / "registry.json"
LIFE_REGISTRY = ROOT / "life" / "registry.json"
AGENTS_REGISTRY = ROOT / "agents" / "registry.json"


def _present(x):
    return isinstance(x, str) and bool(x.strip())


def _utc(s):
    if not _present(s):
        raise ValueError("timestamp required")
    value = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("timestamp must be timezone aware")
    return value.astimezone(timezone.utc)


def verify_grant(mission, grant_registry=None, now=None):
    """A caller-controlled string/object never certifies permission.

    grant_registry must be a separate trusted, verified snapshot of grants from
    the authorising system; this module cannot authenticate its origin. No such
    snapshot is connected in production, so default is fail-closed.
    """
    requested = mission.get("authority_ref")
    if not isinstance(requested, dict) or not _present(requested.get("grant_id")):
        return "AUTHORITY_UNVERIFIED", "No structured external grant reference"
    grants = (grant_registry or {}).get("grants", {})
    if not isinstance(grants, dict):
        return "AUTHORITY_UNVERIFIED", "External grant registry unavailable"
    grant = grants.get(requested["grant_id"])
    if not isinstance(grant, dict) or not grant_registry.get("source_verified", False):
        return "AUTHORITY_UNVERIFIED", "Grant absent from independently verified authority snapshot"
    if grant.get("revoked_at") or grant.get("status") != "active":
        return "AUTHORITY_REVOKED", "Grant has been revoked or is not active"
    if not _present(grant.get("issuer")) or not _present(grant.get("evidence_ref")):
        return "AUTHORITY_UNVERIFIED", "Issuer or independent evidence absent"
    action = mission.get("requested_action", "research.read")
    if action not in grant.get("actions", []):
        return "AUTHORITY_SCOPE_MISMATCH", "Requested action is not permitted"
    if mission["mission_id"] != grant.get("mission_id") or mission["life_domain"] != grant.get("life_domain"):
        return "AUTHORITY_SCOPE_MISMATCH", "Mission/domain outside grant scope"
    if grant.get("native_ref") != mission.get("native_ref"):
        return "AUTHORITY_SCOPE_MISMATCH", "Object reference outside grant scope"
    clock = now or datetime.now(timezone.utc)
    try:
        if _utc(grant["not_before"]) > clock or _utc(grant["expires_at"]) <= clock:
            return "AUTHORITY_EXPIRED", "Grant validity interval excludes execution time"
    except (ValueError, KeyError, TypeError):
        return "AUTHORITY_UNVERIFIED", "Grant validity is malformed"
    return "AUTHORITY_VERIFIED_FOR_ROUTE_ONLY", "Scope, expiry and revocation checked against supplied verified snapshot"


def _capability(mission, registry, anchor):
    tech_id = mission.get("requested_tech_holon_id")
    if not tech_id:
        return None
    items = [e for e in registry["tech_to_a3"] if e["tech_holon_id"] == tech_id]
    if len(items) != 1:
        raise ValueError("unknown tech collaborator")
    edge = items[0]
    caps = edge.get("capabilities", [])
    requested = mission.get("requested_capability")
    if requested and requested not in caps:
        raise ValueError("tech collaborator does not offer requested capability")
    return {
        "id": tech_id, "capability": requested or (caps[0] if caps else "UNDECLARED"),
        "doctor": edge["doctor"], "preference": edge.get("life_a3_id"),
        "preferred_relation": anchor["life_a3_id"] == edge.get("life_a3_id"),
        "nonexclusive": True, "status": "CAPABILITY_MATCH_NOT_DISPATCHED"
    }


def _assignment(mission, registry, business_registry, anchor):
    available = [m for m in business_registry["managers"] if m["parent"] == anchor["jerry_id"]]
    by_function = {m["id"].rsplit(":", 1)[-1]: m for m in available}
    if len(by_function) != 8:
        raise ValueError("expected eight distinct existing functions per Jerry")
    requested = mission.get("business_function")
    if requested is not None and requested not in by_function:
        raise ValueError("business function not available in this Jerry")
    selected = by_function.get(requested) if requested else None
    return {
        "historical_manager": anchor["historic_anchor_manager_id"],
        "historical_squad": anchor["historic_anchor_squad_id"],
        "available_functions": sorted(by_function),
        "selected_function": requested,
        "selected_manager": selected["id"] if selected else None,
        "selected_squad": selected["child"] if selected else None,
        "assignment_status": "PROPOSED_NOT_DISPATCHED" if selected else "NO_FUNCTION_SELECTED",
        "not_executed": True
    }


def _frameworks(mission, registry):
    names = mission.get("framework_contributions", [])
    if not isinstance(names, list) or len(set(names)) != len(names):
        raise ValueError("framework_contributions must be a unique list")
    available = {f["id"]: f for f in registry["frameworks"]}
    missing = set(names).difference(available)
    if missing:
        raise ValueError("unknown framework(s): " + ", ".join(sorted(missing)))
    return [{
        "framework": n, "a2": available[n]["a2_id"],
        "discipline": available[n]["contribution"],
        "a3_specialists": available[n]["a3_specialists"],
        "authority": "ADVISORY_ONLY_UNLESS_LOCAL_OWNER_ACCEPTS",
        "status": "REQUESTED_NOT_EXECUTED", "return_to": available[n]["a2_id"]
    } for n in names]


def _council(mission, tech, unavailable):
    doctors = [tech["doctor"]] if tech else []
    doctors += mission.get("additional_doctors", [])
    valid = {"doctor-11", "doctor-12", "doctor-13"}
    if not isinstance(doctors, list) or any(x not in valid for x in doctors):
        raise ValueError("invalid Doctor participant")
    participants = sorted(set(doctors))
    if not participants:
        return {"status": "NEEDS_DOCTOR_IDENTIFICATION", "participants": [], "next_decision_owner": None}
    active = [d for d in participants if "aspace:tech:" + d not in unavailable]
    if not active:
        return {"status": "DOCTORS_UNAVAILABLE", "participants": participants, "next_decision_owner": None}
    if len(participants) == 1:
        return {"status": "DOCTOR_REVIEW", "participants": participants, "next_decision_owner": "aspace:tech:" + active[0],
                "return_to": "aspace:tech:rick"}
    return {"status": "S2_COUNCIL_REVIEW", "participants": participants,
            "available_participants": active, "chair_for_systemic_review": "aspace:tech:rick",
            "next_decision_owner": None, "decision_rule": "record each Doctor position; no unilateral mandate override",
            "persistent_disagreement": "Rick reviews systemic failure; A0 only for constitutional change"}


def resolve(mission, registry, business_registry=None, grant_registry=None, now=None):
    for key in ("mission_id", "correlation_id", "life_domain"):
        if not _present(mission.get(key)):
            raise ValueError("required mission field: " + key)
    anchors = [e for e in registry["historic"] if e["life_domain"] == mission["life_domain"]]
    if len(anchors) != 1:
        raise ValueError("domain must have one existing historical anchor")
    anchor = anchors[0]
    business_registry = business_registry or json.loads(BUSINESS.read_text(encoding="utf-8"))
    tech = _capability(mission, registry, anchor)
    assign = _assignment(mission, registry, business_registry, anchor)
    fw = _frameworks(mission, registry)
    matrix = build_matrix(
        registry,
        business_registry,
        json.loads(LIFE_REGISTRY.read_text(encoding="utf-8")),
        json.loads(AGENTS_REGISTRY.read_text(encoding="utf-8")),
    )
    matrix_domain = next(
        row for row in matrix["domains"] if row["life_domain"] == anchor["life_domain"]
    )
    mission_selection = resolve_cooperation(
        matrix,
        anchor["life_domain"],
        business_function=mission.get("business_function"),
        tech_holon_id=mission.get("requested_tech_holon_id"),
        required_capability=mission.get("requested_capability"),
        framework_ids=mission.get("framework_contributions", []),
    )
    unavailable = mission.get("unavailable_ids", [])
    if not isinstance(unavailable, list) or any(not _present(x) for x in unavailable):
        raise ValueError("unavailable_ids must contain valid IDs")
    auth_status, auth_reason = verify_grant(mission, grant_registry, now)
    result = {
        "mission_id": mission["mission_id"], "correlation_id": mission["correlation_id"],
        "life_domain": anchor["life_domain"], "life_result_owner": anchor["life_a3_id"],
        "jerry_standard_owner": anchor["jerry_id"], "historical_anchor_only": True,
        "historical_anchor_manager_id": assign["historical_manager"],
        "historical_anchor_squad_id": assign["historical_squad"],
        "business": assign, "framework_contributions": fw, "tech_contribution": tech,
        "cooperation": {
            "matrix_schema": matrix["schema"],
            "institutional_relations": matrix["institutional_relations"],
            "governance_procedure": matrix["governance_procedure"],
            "available_business_functions": matrix_domain["functions_b2_b3"],
            "available_s3_candidates": matrix_domain["s3_candidates"],
            "a2_framework_contributions": matrix_domain["a2_frameworks"],
            "mission_selection": mission_selection,
        },
        "tech_advisor": tech["id"] if tech else None,
        "tech_supervisor": tech["doctor"] if tech else None,
        "manager_delivery_owner": assign["selected_manager"],
        "squad_executor": assign["selected_squad"],
        "native_ref": mission.get("native_ref"), "authority_status": auth_status,
        "authority_diagnostic": auth_reason,
        "observed_effect": "UNKNOWN", "runtime_status": "NOT_VERIFIED",
        "return_to": mission.get("return_to") or anchor["life_a3_id"],
        "delegated_execution": False, "next_decision_owner": None,
        "decision_record": {"proposal": mission.get("proposal"), "objection": mission.get("disagreement"),
                            "response": mission.get("objection_response"), "revision": mission.get("revision_ref"),
                            "appeal": mission.get("appeal_ref")},
    }
    owner = anchor["life_a3_id"]
    morty = "aspace:life:a1:morty"
    beth = "aspace:life:a1:beth"
    if owner in unavailable:
        if morty not in unavailable:
            result.update(status="OWNER_UNAVAILABLE", next_decision_owner=morty,
                          next_decision="Morty verifies durable succession and leases; no substitution without mandate")
        elif beth not in unavailable:
            result.update(status="SUCCESSION_REVIEW_REQUIRED", next_decision_owner=beth,
                          next_decision="Beth can adjudicate continuity/values; operational successor remains unassigned")
        else:
            result.update(status="WAIT_NO_AUTHORIZED_SUCCESSOR",
                          next_decision="A0 constitutional exception channel only; all effects paused")
    elif mission.get("disagreement"):
        conflict = mission["disagreement"]
        if not isinstance(conflict, dict):
            raise ValueError("disagreement must be an object")
        axis = conflict.get("axis")
        decision = {
            "life_value": beth, "area_standard": anchor["jerry_id"], "jurisdiction": morty,
            "tech_capacity": None,
        }
        if axis not in decision:
            raise ValueError("unknown disagreement axis")
        if axis == "tech_capacity":
            council = _council(mission, tech, unavailable)
            result.update(council=council, next_decision_owner=council["next_decision_owner"])
        else:
            candidate = decision[axis]
            if candidate not in unavailable:
                result["next_decision_owner"] = candidate
        result.update(status="OBJECTION_AWAITING_MOTIVATED_RESPONSE" if not mission.get("objection_response") else "REVISION_OR_APPEAL_REVIEW",
                      next_decision="Objection -> situated motivated response -> revision -> appeal if unresolved; no effect")
        if not result["next_decision_owner"] and axis != "tech_capacity":
            result["status"] = "WAIT_UNAVAILABLE_ARBITER"
        if mission.get("appeal_ref"):
            result["appeal_status"] = "PENDING_REVIEW_NOT_SELF_RATIFIED"
    elif not mission.get("native_ref"):
        result.update(status="NATIVE_REF_UNRESOLVED", next_decision_owner=owner)
    elif auth_status != "AUTHORITY_VERIFIED_FOR_ROUTE_ONLY":
        result.update(status=auth_status, next_decision_owner=owner)
    else:
        result.update(status="OWNER_REVIEW_READY_NOT_EXECUTED", next_decision_owner=owner)
    return result


def sample_cases():
    common = {
        "mission_id": "SOH-148", "correlation_id": "CORR-BILL-TILLY-20261014",
        "life_domain": "LD04", "requested_tech_holon_id": "aspace:tech:bill",
        "requested_capability": "research",
        "business_function": "PRD", "framework_contributions": ["Discovery", "PARA"],
        "native_ref": "https://linear.app/aspace-os/issue/SOH-148",
        "authority_ref": {"grant_id": "NOT_ISSUED_SAMPLE"},
        "return_to": "aspace:life:a3:discovery:tilly",
    }
    return [
        dict(common),
        dict(common, disagreement={"axis": "life_value", "reason": "Learning goal conflicts with LD06"}),
        dict(common, unavailable_ids=["aspace:life:a3:discovery:tilly", "aspace:life:a1:morty"]),
    ]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases", action="store_true")
    p.add_argument("--mission-json", type=Path)
    args = p.parse_args()
    if not args.cases and not args.mission_json:
        p.error("pass --cases or --mission-json")
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cases = sample_cases() if args.cases else [json.loads(args.mission_json.read_text(encoding="utf-8"))]
    print(json.dumps([resolve(case, reg) for case in cases], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
