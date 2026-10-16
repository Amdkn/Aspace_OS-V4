#!/usr/bin/env python3
"""Compose the canonical S3/A3/B2/B3/A2 view from source registries.

Read-only: this module never dispatches agents, creates claims, or mutates a
mission. It exposes a machine-readable matrix and a mission-scoped projection.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSS_OS = ROOT / "architecture" / "cross_os_collaboration.json"
BUSINESS = ROOT / "business" / "holons" / "registry.json"
LIFE = ROOT / "life" / "registry.json"
AGENTS = ROOT / "agents" / "registry.json"
SCHEMA = "aspace.s3_a3_b2_b3_matrix.v1"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _one(items, field, value, label):
    found = [item for item in items if item.get(field) == value]
    if len(found) != 1:
        raise ValueError(f"expected one {label} for {value!r}; found {len(found)}")
    return found[0]


def build_matrix(cross, business, life, agents):
    """Build an integrity-checked view without promoting source statuses."""
    historic = {row["life_domain"]: row for row in cross["historic"]}
    directions = {row["life_domain"]: row for row in business["directions"]}
    life_domains = {row["id"]: row for row in life["domains"]}
    managers = business["managers"]
    squads = business["squads"]
    tech_relations = cross["tech_to_a3"]
    profiles = agents["profiles"]

    expected = [f"LD{i:02d}" for i in range(1, 9)]
    if sorted(historic) != expected or sorted(directions) != expected:
        raise ValueError("cross-OS and Business registries must cover LD01-LD08 exactly")
    if sorted(life_domains) != expected:
        raise ValueError("Life registry must cover LD01-LD08 exactly")
    if len(tech_relations) != 9:
        raise ValueError("expected the canonical nine S3 collaboration records")
    frameworks = cross["frameworks"]
    if len(frameworks) != 6:
        raise ValueError("expected the six canonical Life OS frameworks")

    doctors = {
        key: {
            "id": key,
            "name": profile["name"],
            "class": profile["authority_class"],
            "responsibility": profile["primary_responsibility"],
        }
        for key, profile in profiles.items()
        if key.startswith("doctor-")
    }

    s3_catalog = []
    for relation in tech_relations:
        profile_key = relation["tech_holon_id"].rsplit(":", 1)[-1]
        profile = _one([{"id": k, **v} for k, v in profiles.items()],
                       "id", profile_key, "agent profile")
        if profile.get("authority_class") != "S3":
            raise ValueError(f"{profile_key} is not registered as S3")
        if relation["doctor"] != profile.get("doctor"):
            raise ValueError(f"Doctor mismatch for {profile_key}")
        _one(list(doctors.values()), "id", relation["doctor"], "supervising Doctor")
        s3_catalog.append({
            "relation_id": relation["id"],
            "holon_id": relation["tech_holon_id"],
            "name": profile["name"],
            "supervising_doctor": relation["doctor"],
            "capabilities": relation["capabilities"],
            "preferred_life_a3_id": (
                relation["life_a3_id"]
                if relation["life_a3_id"] != "ANY_A3_AS_NEEDED" else None
            ),
            "scope": "NON_EXCLUSIVE" if relation["life_a3_id"] == "ANY_A3_AS_NEEDED"
                     else "PREFERRED_A3_NON_EXCLUSIVE",
            "relationship_status": relation["status"],
            "authority": relation["authority"],
            "purpose": relation["purpose"],
        })

    result_domains = []
    for ld in expected:
        anchor = historic[ld]
        direction = directions[ld]
        life_domain = life_domains[ld]
        if direction["life_a3_id"] != anchor["life_a3_id"]:
            raise ValueError(f"A3 owner mismatch for {ld}")
        if direction["id"] != anchor["jerry_id"]:
            raise ValueError(f"Jerry mismatch for {ld}")

        functions = []
        owned_managers = [m for m in managers if m["parent"] == direction["id"]]
        if len(owned_managers) != 8:
            raise ValueError(f"{ld} must expose eight contextual B2 functions")
        for manager in sorted(owned_managers, key=lambda m: m["id"]):
            squad = _one(squads, "id", manager["child"], "B3 squad")
            if squad["parent"] != manager["id"]:
                raise ValueError(f"B2/B3 parent mismatch for {manager['id']}")
            function = manager["id"].rsplit(":", 1)[-1]
            functions.append({
                "function": function,
                "b2_id": manager["id"],
                "b2_home": manager["home"],
                "dc_manager": manager["vp"],
                "playbook": manager["playbook"],
                "b3_id": squad["id"],
                "b3_home": squad["home"],
                "marvel_squad": squad["name"],
                "runbook": squad["runbook"],
                "relation_to_a3": manager["relation_to_a3"],
                "dispatch_status": "NOT_SELECTED",
            })

        if len({f["function"] for f in functions}) != 8:
            raise ValueError(f"{ld} does not have eight distinct B2 functions")
        anchor_manager = _one(managers, "id", anchor["historic_anchor_manager_id"],
                              "historical B2 anchor")
        anchor_squad = _one(squads, "id", anchor["historic_anchor_squad_id"],
                            "historical B3 anchor")
        if anchor_manager["child"] != anchor_squad["id"]:
            raise ValueError(f"historical B2/B3 anchor mismatch for {ld}")

        a3_id = direction["life_a3_id"]
        domain_tech_relations = []
        for relation in tech_relations:
            if relation["life_a3_id"] == a3_id:
                association = "PREFERRED_A3"
            elif relation["life_a3_id"] == "ANY_A3_AS_NEEDED":
                association = "CROSS_DOMAIN_CANDIDATE"
            else:
                continue
            domain_tech_relations.append({
                "holon_id": relation["tech_holon_id"],
                "relation_id": relation["id"],
                "association": association,
                "relationship_status": relation["status"],
                "capabilities": relation["capabilities"],
                "supervising_doctor": relation["doctor"],
                "dispatch_status": "NOT_SELECTED",
            })

        # Frameworks remain cross-cutting A2 systems. This list is an explicit
        # composition view, not a forced workflow sequence or runtime assignment.
        framework_view = [{
            "id": framework["id"],
            "a2_id": framework["a2_id"],
            "contribution": framework["contribution"],
            "a3_specialist": direction["owner"] in framework["a3_specialists"],
            "dispatch_status": "NOT_SELECTED",
        } for framework in frameworks]

        result_domains.append({
            "life_domain": ld,
            "life_domain_name": life_domain["name"],
            "a3": {
                "id": direction["life_a3_id"],
                "steward": direction["owner"],
                "ownerbook": direction["ownerbook"],
            },
            "jerry": {
                "id": direction["id"],
                "name": direction["name"],
                "ownerbook": direction["ownerbook"],
                "linear_issue": direction["issue"],
            },
            "historical_anchor": {
                "relation_id": anchor["relation_id"],
                "status": anchor["ratification"],
                "b2_id": anchor_manager["id"],
                "b2": anchor["dc_manager"],
                "b3_id": anchor_squad["id"],
                "b3": anchor["marvel_squad"],
                "framework_at_source": anchor["framework_at_source"],
            },
            "additional_business_contributions": {
                "items": anchor["linear_associations_2026_10_08"],
                "status": anchor["linear_associations_status"],
            },
            "functions_b2_b3": functions,
            "s3_candidates": domain_tech_relations,
            "a2_frameworks": framework_view,
            "owner_decision": "A3_STEWARD",
        })

    return {
        "schema": SCHEMA,
        "as_of": cross["as_of"],
        "source_files": [
            "architecture/cross_os_collaboration.json",
            "business/holons/registry.json",
            "life/registry.json",
            "agents/registry.json",
        ],
        "semantics": {
            "historical_anchor": "Provenance only; never auto-selected as mission assignment.",
            "contextual_b2_b3": "Eight available function pairs per Jerry; choose per mission.",
            "s3": "Capability catalog filtered by domain preference and non-exclusive scope; choose only for a mission.",
            "frameworks": "Cross-cutting A2 contribution; composable, not a mandatory sequence.",
            "execution": "This resolver is read-only and never dispatches agents or claims completion.",
        },
        "doctors": doctors,
        "s3_capability_catalog": s3_catalog,
        "domains": result_domains,
    }


def resolve_cooperation(matrix, life_domain, business_function=None,
                        tech_holon_id=None, required_capability=None,
                        framework_ids=None):
    """Return a domain composition and optional mission-scoped selections."""
    domain = _one(matrix["domains"], "life_domain", life_domain, "Life domain")
    result = {
        "schema": "aspace.mission_cooperation_projection.v1",
        "life_domain": life_domain,
        "a3_owner": domain["a3"],
        "jerry": domain["jerry"],
        "historical_anchor": domain["historical_anchor"],
        "additional_business_contributions": domain["additional_business_contributions"],
        "business_assignment": None,
        "s3_assignment": None,
        "frameworks": [],
        "runtime_status": "NOT_DISPATCHED",
    }
    if business_function:
        function = _one(domain["functions_b2_b3"], "function",
                        business_function.upper(), "B2/B3 business function")
        result["business_assignment"] = {
            **function,
            "dispatch_status": "PROPOSED_NOT_DISPATCHED",
        }
    if tech_holon_id or required_capability:
        candidates = [
            candidate for candidate in domain["s3_candidates"]
            if (not tech_holon_id or candidate["holon_id"] == tech_holon_id)
            and (not required_capability
                 or required_capability in candidate["capabilities"])
        ]
        if len(candidates) != 1:
            raise ValueError(
                "S3 selection must resolve to exactly one domain-compatible "
                f"candidate; found {len(candidates)}"
            )
        result["s3_assignment"] = {
            **candidates[0],
            "dispatch_status": "CAPABILITY_MATCH_NOT_DISPATCHED",
        }
    for framework_id in framework_ids or []:
        framework = _one(domain["a2_frameworks"], "id", framework_id,
                         "A2 framework")
        result["frameworks"].append({
            **framework,
            "dispatch_status": "CONTRIBUTION_SELECTED_NOT_DISPATCHED",
        })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true",
                        help="print the complete S3/A3/B2/B3/A2 matrix")
    parser.add_argument("--domain", choices=[f"LD{i:02d}" for i in range(1, 9)])
    parser.add_argument("--business-function", help="mission-specific B2/B3 function")
    parser.add_argument("--tech-holon-id", help="mission-specific S3 holon ID")
    parser.add_argument("--capability", help="mission-specific S3 capability")
    parser.add_argument("--framework", action="append", default=[],
                        help="select an A2 contribution; may be repeated")
    args = parser.parse_args()

    matrix = build_matrix(_load(CROSS_OS), _load(BUSINESS), _load(LIFE), _load(AGENTS))
    if args.domain:
        print(json.dumps(resolve_cooperation(
            matrix, args.domain, args.business_function, args.tech_holon_id,
            args.capability, args.framework), ensure_ascii=False, indent=2))
    elif args.json:
        print(json.dumps(matrix, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            "schema": matrix["schema"],
            "domains": len(matrix["domains"]),
            "b2_b3_function_pairs": sum(
                len(row["functions_b2_b3"]) for row in matrix["domains"]),
            "s3_capabilities": len(matrix["s3_capability_catalog"]),
            "a2_frameworks": len(matrix["domains"][0]["a2_frameworks"]),
            "validation": "PASS",
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
