#!/usr/bin/env python3
"""Qualify existing A'Space Issue Factory for the Bill–Tilly life-benefit question.

Single mission, read-only source audit; no provider request, worker, git push,
Linear state change, WorkGraph claim or personal outcome inferred.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.holon_route import resolve
from tools.handoff_compiler import capsule, validate

ROOT = Path(__file__).resolve().parents[1]
CORRELATION = "CORR-BILL-TILLY-20261014"
MISSION = "SOH-148"
SOURCES = (
    "tools/issue_factory.py",
    ".github/workflows/auto-label-factory-ready.yml",
    ".github/workflows/issue-factory.yml",
    "tests/test_issue_factory.py",
    "research/bill_tilly/video_manifest.json",
)

def qualify(root=ROOT):
    content = {p: (root / p).read_text(encoding="utf-8") for p in SOURCES}
    manifest = json.loads(content["research/bill_tilly/video_manifest.json"])
    registry = json.loads((root / "architecture/cross_os_collaboration.json").read_text(encoding="utf-8"))
    if manifest.get("mission_correlation_id") != CORRELATION:
        raise ValueError("mission source correlation changed; refuse blind rescope")
    if manifest["sources"][0].get("video_id") != "ZHOmBeMNbnc":
        raise ValueError("VIDEO-01 provenance changed")
    if any(s.get("transcript_ref") for s in manifest["sources"]):
        raise ValueError("Transcript state changed; review source before qualification")
    code = content["tools/issue_factory.py"]
    wf = content[".github/workflows/auto-label-factory-ready.yml"]
    gate = content[".github/workflows/issue-factory.yml"]
    if "trusted_receipt" not in code or "CLAIMED" not in code or "UNKNOWN" not in code:
        raise ValueError("Factory receipt/replay safety missing")
    if "factory:opt-in" not in wf or "no-factory" not in wf:
        raise ValueError("Factory new-issue opt-in gate not present")
    if "concurrency:" not in gate or "cancel-in-progress: false" not in gate:
        raise ValueError("Single controller concurrency absent")
    route = resolve({
        "mission_id": MISSION, "correlation_id": CORRELATION, "life_domain": "LD04",
        "requested_tech_holon_id": "aspace:tech:bill", "requested_capability": "research",
        "business_function": None, "framework_contributions": ["Discovery","PARA","DEAL"],
        "native_ref": "https://linear.app/aspace-os/issue/SOH-148",
        "requested_action": "research.read",
        "authority_ref": {"grant_id": "UNVERIFIED_NO_PROVIDER_GRANT"},
        "return_to": "aspace:life:a3:discovery:tilly",
    }, registry)
    if route["delegated_execution"] or route["authority_status"] == "AUTHORITY_VERIFIED_FOR_ROUTE_ONLY":
        raise ValueError("Source qualification must never dispatch an effect")
    return {
      "schema": "aspace.factory_qualification.v1", "mission_id": MISSION,
      "correlation_id": CORRELATION, "question_owner": route["life_result_owner"],
      "research_owner": route["tech_advisor"], "doctor": route["tech_supervisor"],
      "candidate": "existing GitHub Issue Factory / Jules with the installed receipts",
      "video_context": "VIDEO-01 David Ondrej, METADATA_AND_PARTIAL_SECONDARY_TIMECODES; not a runtime proof",
      "decision": "REJECT_UNSCOPED_AUTO_DISPATCH_ACCEPT_EXPLICIT_OPT_IN_REUSE",
      "decision_type": "TECHNICAL_SAFETY_RECOMMENDATION_PENDING_LIFE_ACCEPTANCE",
      "observations": [
        "Factory code records claimed/unknown states and avoids blind Jules redispatch",
        "Actions workflow serializes controller with cancel-in-progress=false",
        "New issue auto-label now gated by factory:opt-in; previous open factory:ready issues are not cleared",
        "No independently verified grant for live Jules spend/effect or Life acceptance on this canary",
      ],
      "criteria_not_proven": [
        "provider credentials and available quotas", "real Jules session creates accepted result",
        "two independent sessions resume with no A0 instruction",
        "net A0 time saved minus maintenance", "Tilly acceptance of cognitive outcome"
      ],
      "selected_business_function": None,
      "historical_business_anchor": route["historical_anchor_manager_id"],
      "route_status": route["status"],
      "authority_status": route["authority_status"],
      "no_external_effects": True,
      "source_sha256": {p: hashlib.sha256(v.encode("utf-8")).hexdigest() for p,v in content.items()},
      "source_refs": [
        "https://github.com/Amdkn/Aspace_OS-V4/blob/main/tools/issue_factory.py",
        "https://github.com/Amdkn/Aspace_OS-V4/blob/main/.github/workflows/auto-label-factory-ready.yml",
        "https://github.com/Amdkn/Aspace_OS-V4/blob/main/research/bill_tilly/video_manifest.json",
        "https://linear.app/aspace-os/issue/SOH-148",
      ],
      "return_to": "aspace:life:a3:discovery:tilly"
    }


def to_handoff(qual):
    return {
      "mission_id": qual["mission_id"], "correlation_id": qual["correlation_id"],
      "owner": qual["question_owner"], "observed_at": datetime.now(timezone.utc).isoformat(),
      "last_verified_effect": "Code and six-source manifest inspected, opt-in gate and no-blind-retry logic verified by source checks; no execution performed",
      "latest_native_refs": qual["source_refs"],
      "pending_authority": "Independent permission snapshot for Jules spend/effect, plus scope owner approval; neither is assumed",
      "blocked_outcome": "No verified runtime/cognitive benefit; no WorkGraph claim",
      "next_executable_action": "Re-read GitHub HEAD and existing Issue Factory receipts; locate one explicit opt-in bounded real issue, verify current grant/quota, run one reversible worker canary or issue a reasoned rejection",
      "return_to": qual["return_to"], "effect_status": "OBSERVED_SOURCE_ONLY",
      "evidence_refs": qual["source_refs"], "decision": qual["decision"],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=Path("factory-out"))
    args = p.parse_args()
    qual = qualify()
    handoff = to_handoff(qual)
    validate(handoff)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "qualification.json").write_text(json.dumps(qual, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out / "handoff.json").write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("QUALIFIED READ-ONLY: " + qual["decision"])
    print("Independent resume capsule:\n" + capsule(handoff))


if __name__ == "__main__":
    main()
