#!/usr/bin/env python3
"""Temporary PR metadata guard against auto-closing Life-outcome issues.

A Linear workflow may link GitHub PRs and auto-move statuses. This only
guards title/body on new PRs; it does not inspect Linear workspace settings,
commits, or prove the integration's internal root cause.
"""
import json
import os
from pathlib import Path
import re
import sys

LIFE_OUTCOME_IDS = {f"SOH-{n}" for n in range(145, 153)}
ISSUE_RE = re.compile(r"\bSOH-1(?:4[5-9]|5[0-2])\b", re.IGNORECASE)


def inspect(title, body):
    raw = f"{title or ''}\n{body or ''}"
    found = sorted({k.upper() for k in ISSUE_RE.findall(raw)})
    return [k for k in found if k in LIFE_OUTCOME_IDS]


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("NOT_PR_EVENT: metadata check skipped")
        return 0
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    pr = event.get("pull_request")
    if not pr:
        print("NOT_PR_EVENT: metadata check skipped")
        return 0
    matches = inspect(pr.get("title"), pr.get("body"))
    if matches:
        print("BLOCKING_DIRECT_LIFE_ISSUE_REFERENCE: " + ", ".join(matches), file=sys.stderr)
        print("Technical PRs must be connected through the existing Linear technical work item. "
              "Attach evidence to the Life-outcome issue from Linear after human-result acceptance. "
              "This is a temporary mitigation, NOT a fix to integration settings.", file=sys.stderr)
        return 2
    print("NO_DIRECT_LIFE_OUTCOME_REFERENCE_IN_PR_METADATA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
