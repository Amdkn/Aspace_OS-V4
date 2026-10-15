#!/usr/bin/env python3
"""Independent runner verification of a durable qualification artifact.

No network; compare Linux-produced artifact with independently checked-out
source on this runner. This proves cross-runner continuity, not a second S3.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.factory_qualify import qualify
from tools.handoff_compiler import validate, capsule


def replay(qualification, receipt):
    fresh = qualify()
    for key in ("schema", "mission_id", "correlation_id", "source_sha256", "decision", "no_external_effects"):
        if qualification.get(key) != fresh.get(key):
            raise ValueError("Source or decision drift at independent runner: " + key)
    validate(receipt)
    if receipt.get("mission_id") != fresh["mission_id"] or receipt.get("correlation_id") != fresh["correlation_id"]:
        raise ValueError("Receipt does not belong to this bounded mission")
    if receipt.get("decision") != fresh["decision"]:
        raise ValueError("Receipt decision disagrees with source")
    if receipt.get("return_to") != fresh["return_to"]:
        raise ValueError("Receipt return_to changed")
    if receipt.get("effect_status") == "VERIFIED":
        raise ValueError("A read-only qualification may not claim a verified external effect")
    capsule_text = capsule(receipt)
    if "no blind retry" not in capsule_text or "NEXT:" not in capsule_text:
        raise ValueError("No independent next action")
    return {
        "schema": "aspace.factory_replay.v1",
        "mission_id": fresh["mission_id"], "correlation_id": fresh["correlation_id"],
        "verified": True, "verification_type": "INDEPENDENT_RUNNER_SOURCE_AND_RECEIPT_REPLAY",
        "source_fingerprints_match": True, "context_reconstructed_without_A0": True,
        "next_action_recovered": receipt["next_executable_action"],
        "return_to": receipt["return_to"],
        "external_effect": "NOT_EXECUTED",
        "independent_companion_agent": "NOT_PROVEN",
        "human_time_saved": "NOT_MEASURED"
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("qualification", type=Path)
    p.add_argument("receipt", type=Path)
    p.add_argument("--out", type=Path, default=Path("replay-out"))
    args = p.parse_args()
    a = json.loads(args.qualification.read_text(encoding="utf8"))
    b = json.loads(args.receipt.read_text(encoding="utf8"))
    result = replay(a, b)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"replay.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf8")
    print("INDEPENDENT_RUNNER_REPLAY_OK: " + result["mission_id"] + ", return_to=" + result["return_to"])


if __name__ == "__main__":
    main()
