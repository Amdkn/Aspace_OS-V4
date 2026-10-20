# Supabase Probe — L02 (F-02 BedRock)

Read-only proof that a live Supabase instance answers. The probe
(`tools/supabase_probe.py`) only performs HTTP **GET** requests —
zero writes, by construction and by audit.

## Modes and exit codes

| Mode | Needs | Proves | Exit |
|---|---|---|---|
| `liveness` (default) | `SUPABASE_URL` | the instance answers (auth health / REST root) | 0 = live, 1 = down |
| `full` | `SUPABASE_URL` + `SUPABASE_ANON_KEY` | the anon key is valid and the API answers; optional `--table` read | 0 = green, 1 = auth/API failure, **2 = key missing (traced skip, not green)** |

Secrets are read from the environment only. Never in the repo, never
hardcoded. The CI workflow (`.github/workflows/supabase-probe.yml`)
feeds them from the repo variable `SUPABASE_URL` and the repo secret
`SUPABASE_ANON_KEY`.

## A4 secret inventory (run 2026-10-20)

1. **Secure Vault metadata** — no Supabase entry. ✗
2. **Codespace secrets** — Codespace stopped (budget exhausted,
   2026-10-19); secrets not readable from here. Unverified.
3. **Documented project** — `os/business/okf/securite/projets-supabase.md`
   documents two projects:
   - `sgzbkhqqkqdwhakkyzzm` (OMK Services — internal): **LIVE** —
     `/auth/v1/health` and `/rest/v1/` answer 401 (Supabase up,
     key required), liveness probe exit 0 on 2026-10-20.
   - `qjrwcdzaebyqponqkiqs` (Coach OS): **DOWN** — unreachable
     (connection fails; likely paused/deleted), liveness exit 1.

No real key appears anywhere in the repo (`.env.example` files carry
placeholders only; secret-pattern grep is empty — H-L02-3).

## Open item — escalation A0 (capacity)

H-L02-2 (green authenticated probe on a live instance) requires the
**anon key** of project `sgzbkhqqkqdwhakkyzzm`. It exists nowhere the
probe can reach (see inventory above). Escalation goes through A0 —
no demand is made to the Capitaine (plan §L02, decision 3). Until the
key lands (repo secret `SUPABASE_ANON_KEY` + variable `SUPABASE_URL`),
the `probe` CI job fails explicitly with exit 2: the degraded state
is traced and loud, never silently green.

## Non-regression

The Life fail-fast client (`os/life/src/lib/supabase.ts`) and the
`VITE_LIFE_LOCAL_ONLY` mode are untouched by this phase (H-L02-4).
