# Coach OS

A desktop-web OS for solo premium coaches — 13 apps (Dashboard, People/Agents,
Operations, IT/R&D, Clients, Tasks, Marketplace, Product, Growth, Sales, Finance,
Legal, Settings), each with its own collapsible sidebar and CMS-driven content
(collections → repeater lists → dynamic detail pages, in the spirit of a
Wix-CMS-style content model).

Forked from the A'Space Life OS window shell (draggable/resizable windows,
Zustand-backed layout persistence, glass design system) and re-skinned in a
PostHog-light palette with a paper-garden wallpaper.

## Stack

- Vite + React 19 + TypeScript
- Zustand (shell/window state + CMS collections store)
- Tailwind v4
- Supabase (Postgres, RLS-scoped multi-tenant backend — see `MIGRATION_SUPABASE.md`)

## Local development

Full step-by-step setup (clone to first `--sante` check) lives in
[`INSTALL.md`](./INSTALL.md) — it documents two already-paid traps (a
false-positive `tsc` command, and a flaky default `vitest` pool) so nobody
re-discovers them. Short version:

```bash
npm install
cp .env.example .env.local   # fill in your Supabase keys
npm run dev
```

Node version is pinned in [`.nvmrc`](./.nvmrc).

## Verify / CI

```bash
npm run verify
```

Runs, in order: `typecheck` (`tsc -b` — the only command that actually
type-checks; `npx tsc --noEmit -p tsconfig.json` alone is a silent
false-positive), `typecheck:api`, `test` (vitest with `--pool=threads`),
`build`, and the four runtime benches (`_runtime/kernel.mjs`,
`_runtime/bridge/{bridge,adapters,rbac-test}.mjs`). This is exactly what
[`.github/workflows/ci.yml`](./.github/workflows/ci.yml) runs on every push
and pull request.

## Docs

- [`INSTALL.md`](./INSTALL.md) — full local setup, verification, and known traps
- [`MIGRATION_SUPABASE.md`](./MIGRATION_SUPABASE.md) — data-layer migration plan, 3-stage tenancy model
- [`PHASE0_RECEIPT.md`](./PHASE0_RECEIPT.md) — Supabase Phase 0 provisioning receipt


<!-- ASPACE-WORLD-FEDERATION:BEGIN -->
## A'Space World Federation

This repository is a sovereign world/member of one A'Space V3 federation, not a monorepo subtree.

- **Astra** — [Amdkn/Aspace_OS_V3](https://github.com/Amdkn/Aspace_OS_V3): unified system / Design-of-Design / registry.
- **Sol** — [Amdkn/Agent-OS-Desktop](https://github.com/Amdkn/Agent-OS-Desktop): Agent OS interface & observability; local desktop `127.0.0.1:5555`.
- **Terra** — [Amdkn/Life-OS-2026](https://github.com/Amdkn/Life-OS-2026): Life OS 2026.
- **Luna** — Business federation: [BusinessOS](https://github.com/Amdkn/BusinessOS), [Business-Office-3-OS](https://github.com/Amdkn/Business-Office-3-OS), [01-OMK-Business-OS](https://github.com/Amdkn/01-OMK-Business-OS), [The-OMK-Office1.0-JaaS](https://github.com/Amdkn/The-OMK-Office1.0-JaaS), [Mobile Back Office](https://github.com/Amdkn/The-OMK-Mobile-Back-Office), [OMK Desktop Web OS](https://github.com/omk-services/OMK-DESKTOP-WEB-OS), [OMK SaaS OS](https://github.com/omk-services/00-omk-saas-os), and the private OMK landing repository.

Filesystem junctions/symlinks are navigation projections only. Every member keeps its own Git history, remote, CI and release boundary. Canonical location mapping lives in Astra's `ASPACE_WORKSPACE_REGISTRY.json`.
<!-- ASPACE-WORLD-FEDERATION:END -->
