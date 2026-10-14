#!/usr/bin/env python3
"""A'Space handoff contract: reduce manual session re-explanation.

No credentials, network calls, automation scheduler or implicit effects.
Inputs are durable receipt JSON files with explicit truth status.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ("mission_id", "last_verified_effect", "latest_native_refs",
            "pending_authority", "blocked_outcome", "next_executable_action",
            "owner", "return_to", "observed_at", "correlation_id")

def validate(receipt: dict) -> None:
    if not isinstance(receipt, dict):
        raise ValueError("receipt must be an object")
    missing = [k for k in REQUIRED if k not in receipt]
    if missing:
        raise ValueError("missing fields: " + ", ".join(missing))
    if not isinstance(receipt["latest_native_refs"], list):
        raise ValueError("latest_native_refs must be a list")
    for k in ("mission_id", "owner", "return_to", "observed_at", "correlation_id"):
        if not isinstance(receipt[k], str) or not receipt[k].strip():
            raise ValueError(k + " must be a nonempty string")
    if receipt.get("effect_status") == "VERIFIED" and not receipt.get("evidence_refs"):
        raise ValueError("VERIFIED requires evidence_refs")

def capsule(receipt: dict) -> str:
    validate(receipt)
    status = receipt.get("effect_status", "UNKNOWN")
    refs = "\n".join("- " + str(ref) for ref in receipt["latest_native_refs"]) or "- UNRESOLVED"
    return (
        f"# Mission resume: {receipt['mission_id']}\n"
        f"Correlation: {receipt['correlation_id']}\n"
        f"Owner: {receipt['owner']}\n"
        f"Observed: {receipt['observed_at']}\n"
        f"Effect status: {status}\n"
        f"Verified effect: {receipt['last_verified_effect']}\n"
        f"Refs:\n{refs}\n"
        f"Pending authority: {receipt['pending_authority']}\n"
        f"Blocked outcome: {receipt['blocked_outcome']}\n"
        f"NEXT: {receipt['next_executable_action']}\n"
        f"Return to: {receipt['return_to']}\n"
        "On resumption: re-read native refs and receipt, check authority and "
        "correlation before effects. If ambiguous, UNKNOWN; no blind retry.\n"
    )

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("receipt", type=Path)
    args = p.parse_args(argv)
    try:
        obj = json.loads(args.receipt.read_text(encoding="utf-8"))
        print(capsule(obj))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print("INVALID RECEIPT: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
