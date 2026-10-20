# CI Integrity — receipts, not locks (L04 · F-02 BedRock)

This document states the repository's CI integrity doctrine explicitly.
It is normative for `main`.

## 1. Bypass is a deliberate capability, not a vulnerability

- **`enforce_admins` is `false`** (Capitaine arbitration A2, 2026-10-17).
  The repository owner can bypass branch protection. This is **by design**.
- Owner bypass = **deliberate capability** under the *maximum-capacity*
  doctrine (the inverse of least privilege): control comes from the
  org chart plus the receipts, not from locking.
- This document **never** claims "no bypass is possible". Any claim of
  that form is a documentation bug — report it.

## 2. Where integrity actually comes from

1. **Required checks** — `V4 checks / verify (ubuntu-latest)` and
   `V4 checks / verify (windows-latest)` are required on `main`.
   A merge without green checks is blocked for everyone except the owner
   (see §1).
2. **Receipt check (`r10-receipt`)** — every merge on `main` requires an
   R10 receipt referencing the PR (mission_id + SHA + observed_at /
   recorded_at + proof links + emitter). Status: enforcement lands with
   L01; this phase (L04) prepares it.
3. **Non-bypass audit** — `.github/workflows/audit-nonbypass.yml`
   (daily + on demand) replays recent merges on `main` and verifies that
   the required checks were green *before* each merge (check-run
   timestamps vs `merged_at`). A detected bypass fails the run visibly
   and is recorded in the uploaded `audit-report.json` artifact
   (who merged, when, which check was not green). The audit is
   **transparency of the trail**, not a step toward locking.

## 3. Reading the audit

- `✓ OK` — all required checks green before the merge.
- `✗ BYPASS` — a required check was not green before the merge.
  The report names the PR, the merger, and the timestamp: that **is**
  the trace. No silent circumvention.
- `? NO_DATA` — no check runs at all (pre-CI history). Reported,
  not counted as bypass.

Bypass detected → visible red run + named trace. That is the whole
mechanism. There is no lock to add.
