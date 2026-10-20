# os/life — Life-OS-2026 (réduit)

Import fidèle de **Amdkn/Life-OS-2026@f9d6f27** (5/5 PRs mergées), réduit via le
manifeste Phase 1 (494 chemins supprimés, 5 ancrages).

**Contenu (minimum) :** shell web OS + PARA + serveur Blackboard + persistance
IndexedDB → Supabase. Système de capabilities protégé (voir
`os/capabilities.registry.json`).

**Commandes** (dans `os/life/`) :
- `npm ci && npm run build` — build production (vite)
- `npm run gate` — gate complet (a3-validation-gate + tsc + build)
- `npm run dev` — shell web (`:4444`)
- `npm run server` — serveur Blackboard (`:4445`, `PORT` overridable)

**Règle persistance :** pas de mock Supabase silencieux — fail-fast au boot sans
`VITE_SUPABASE_URL`/`VITE_SUPABASE_ANON_KEY`, sauf `VITE_LIFE_LOCAL_ONLY=true`
(bannière visible, shell sans compte).
