#!/usr/bin/env python3
"""Supabase live probe — L02 (F-02 BedRock).

Read-only proof that a live Supabase instance answers. NEVER writes:
the probe only performs HTTP GET requests. Secrets come from the
environment only (SUPABASE_URL, SUPABASE_ANON_KEY) — never from the repo,
never hardcoded.

Modes:
  liveness  (default, no key needed) — proves the instance answers:
            GET {url}/auth/v1/health and GET {url}/rest/v1/.
            Exit 0 = a Supabase component answers (live).
            Exit 1 = unreachable / down.
  full      (needs SUPABASE_ANON_KEY) — liveness + authenticated check:
            GET {url}/rest/v1/ with the anon key.
            Exit 0 = key valid, API answers (optionally + table read).
            Exit 2 = key missing (explicit skip, traced — escalate).
            Exit 1 = key invalid or API error.

Optional: --table <name> adds a read-only row probe in full mode:
  GET {url}/rest/v1/<table>?select=*&limit=1
  (200 = readable, 401 = RLS denies anon — connectivity still proven,
   404 = table missing — recorded, not fatal).

A timestamped JSON report is written with --report. Exit code is the
verdict; nothing here is a mock.

Usage:
  SUPABASE_URL=https://<ref>.supabase.co python tools/supabase_probe.py
  SUPABASE_URL=... SUPABASE_ANON_KEY=... python tools/supabase_probe.py --mode full --table organizations
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone


def get(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(200)
    except urllib.error.HTTPError as e:
        return e.code, e.read(200)
    except Exception as e:  # unreachable, DNS, TLS, timeout
        return None, str(e)[:120]


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["liveness", "full"], default="liveness")
    ap.add_argument("--table", default=None,
                    help="read-only table probe in full mode")
    ap.add_argument("--report", default="supabase-probe-report.json")
    args = ap.parse_args()

    base = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_ANON_KEY", "")
    report = {"observed_at": now_iso(), "mode": args.mode,
              "url_host": base.split("://", 1)[-1] if base else None,
              "tiers": {}}

    if not base:
        print("SKIP: SUPABASE_URL not set (env only, never hardcoded).")
        report["verdict"] = "skip-no-url"
        json.dump(report, open(args.report, "w"), indent=2)
        return 2

    # Tier (a): infrastructure liveness — no key needed.
    health = get(f"{base}/auth/v1/health")
    rest = get(f"{base}/rest/v1/")
    live = (health[0] in (200, 401)) or (rest[0] in (200, 401))
    report["tiers"]["liveness"] = {
        "auth_health": health[0], "rest_root": rest[0],
        "verdict": "LIVE" if live else "DOWN",
    }
    if args.mode == "liveness":
        print(f"LIVENESS: {'LIVE' if live else 'DOWN'} "
              f"(auth={health[0]}, rest={rest[0]}) @ {report['observed_at']}")
        report["verdict"] = "live" if live else "down"
        json.dump(report, open(args.report, "w"), indent=2)
        return 0 if live else 1

    # Tier (b): authenticated read-only check — key required.
    if not key:
        print("SKIP: SUPABASE_ANON_KEY not set — authenticated check cannot "
              "run. Escalation path: A0 (capacity). This is traced, not green.")
        report["verdict"] = "skip-no-key"
        json.dump(report, open(args.report, "w"), indent=2)
        return 2

    status, _ = get(f"{base}/rest/v1/",
                    headers={"apikey": key,
                             "Authorization": f"Bearer {key}"})
    key_valid = status in (200, 404)
    report["tiers"]["authenticated"] = {
        "rest_root_with_key": status,
        "key_valid": key_valid,
    }
    table_result = None
    if args.table and key_valid:
        tstatus, _ = get(f"{base}/rest/v1/{args.table}?select=*&limit=1",
                         headers={"apikey": key,
                                  "Authorization": f"Bearer {key}"})
        table_result = {200: "readable",
                        401: "rls-denied-anon",
                        404: "table-missing"}.get(tstatus, f"http-{tstatus}")
        report["tiers"]["table"] = {"table": args.table,
                                    "status": tstatus,
                                    "read": table_result}

    ok = key_valid
    verdict = "full-green" if ok else "auth-failed"
    print(f"FULL: key_valid={key_valid} (rest={status}"
          + (f", table {args.table}={table_result}" if args.table else "")
          + f") @ {report['observed_at']}")
    report["verdict"] = verdict
    json.dump(report, open(args.report, "w"), indent=2)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
