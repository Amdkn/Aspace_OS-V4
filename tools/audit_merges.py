#!/usr/bin/env python3
"""Non-bypass audit — L04 (F-02 BedRock).

For each recent merge on `main` (sliding window), verify that the required
checks were green BEFORE the merge (check-run timestamps vs merged_at).

Tier D: pure code, timestamp comparison, zero model. No network writes.

Verdicts per merge:
  OK       — every required check completed with success before merged_at.
  BYPASS   — a required check was not green before merged_at
             (pending / failing / absent while CI ran). Traced with who/when.
  NO_DATA  — no check runs at all for the head SHA (pre-CI history).
             Reported, not counted as bypass.

Exit 0: no BYPASS in window. Exit 1: at least one BYPASS (visible alert).
The JSON report is the trace (H-L04-2).

Usage:
  GH_TOKEN=... python tools/audit_merges.py [--window 20]
      [--required "verify (ubuntu-latest),verify (windows-latest)"]
      [--report audit-report.json] [--repo Amdkn/Aspace_OS-V4]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

API = "https://api.github.com"


def api_get(path, token):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"API error {e.code} on {path}", file=sys.stderr)
        raise SystemExit(2)


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=20)
    ap.add_argument("--required", default="verify (ubuntu-latest),verify (windows-latest)")
    ap.add_argument("--report", default="audit-report.json")
    ap.add_argument("--repo", default="Amdkn/Aspace_OS-V4")
    args = ap.parse_args()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    required = [r.strip() for r in args.required.split(",") if r.strip()]

    prs = api_get(
        f"/repos/{args.repo}/pulls?state=closed&base=main&per_page={min(args.window, 100)}"
        f"&sort=updated&direction=desc", token)
    merged = [p for p in prs if p.get("merged_at")][:args.window]

    results = []
    bypasses = 0
    for pr in merged:
        num = pr["number"]
        head = pr["head"]["sha"]
        merged_at = parse_ts(pr["merged_at"])
        by = (pr.get("merged_by") or {}).get("login", "?")
        runs = api_get(
            f"/repos/{args.repo}/commits/{head}/check-runs?per_page=100", token
        ).get("check_runs", [])

        by_name = {}
        for cr in runs:
            n = cr["name"]
            if cr["status"] == "completed" and cr.get("completed_at"):
                ts = parse_ts(cr["completed_at"])
                prev = by_name.get(n)
                if prev is None or ts > prev[0]:
                    by_name[n] = (ts, cr["conclusion"])

        checks = {}
        verdict = "OK"
        if not runs:
            verdict = "NO_DATA"
        for req_name in required:
            hit = by_name.get(req_name)
            if hit and hit[0] < merged_at and hit[1] == "success":
                checks[req_name] = {"verdict": "OK",
                                   "completed_at": hit[0].isoformat()}
            else:
                checks[req_name] = {"verdict": "BYPASS",
                                   "detail": ("no successful completion before merge"
                                              if not hit else
                                              f"last={hit[1]}@{hit[0].isoformat()}")}
                verdict = "BYPASS"
        if verdict == "BYPASS":
            bypasses += 1
        results.append({
            "pr": num, "title": pr["title"][:80], "head": head[:7],
            "merged_at": pr["merged_at"], "merged_by": by,
            "verdict": verdict, "checks": checks,
        })

    report = {
        "repo": args.repo, "window": args.window,
        "required_checks": required,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bypasses": bypasses, "merges": results,
    }
    with open(args.report, "w") as f:
        json.dump(report, f, indent=2)

    for r in results:
        flag = {"OK": "✓", "BYPASS": "✗ BYPASS", "NO_DATA": "? NO_DATA"}[r["verdict"]]
        print(f"#{r['pr']} {r['head']} merged_by={r['merged_by']} "
              f"at={r['merged_at']} → {flag}")
        if r["verdict"] == "BYPASS":
            for name, c in r["checks"].items():
                if c["verdict"] == "BYPASS":
                    print(f"    {name}: {c['detail']}")
    print(f"\n{bypasses} bypass(es) in window of {len(results)}. "
          f"Report: {args.report}")
    return 1 if bypasses else 0


if __name__ == "__main__":
    sys.exit(main())
