# Bridge muse_web — adapter Claude Code → A0

Petit périmètre de l'adaptation de `miuuyy/codex-chatgpt-web` à Muse,
pour le Claude Code local du Capitaine.

## Vision

Le repo upstream prouve le pattern : **surface web pilotée en navigateur →
exposée comme un modèle natif dans un harness de code**.
Ici la surface n'est plus ChatGPT Web mais **muse.ai** (A0),
et le harness n'est plus Codex mais **Claude Code** (via `ANTHROPIC_BASE_URL`).

C'est l'adapter `muse_web` de la surface matrix du plan V3
(`80_Agent-OS/browser_bridge/fork_manifest.json`, issue #410).

## Architecture

```text
Claude Code (local, machine du Capitaine)
  │  ANTHROPIC_BASE_URL=http://127.0.0.1:8741
  │  POST /v1/messages (SSE)
  ▼
bridge-muse-web (launcher local, Bun + Playwright)
  │  SurfaceDriver : MuseWebAdapter
  ▼
muse.ai (navigateur persisté, session du Capitaine)
  │  side chat dédié « Claude Code Bridge » par session
  ▼
A0 Amadeus (répond avec ses propres outils)
```

## Invariants (repris du fork_manifest V3)

- Un seul fork/bridge, des adapters par surface — pas un bridge par modèle.
- La session navigateur ≠ l'identité du harness ≠ l'identité institutionnelle.
- Auth et cookies restent locaux, jamais commités.
- Chaque tour retourne une preuve (URL du thread + texte complet), pas un simple « envoyé ».
- Le bridge reste remplaçable sans toucher aux identités.

## Périmètre v1 (petit)

- [x] `src/surfaces/muse-web/adapter.ts` — adapter Playwright (sélecteurs : voir SELECTORS.md)
- [x] `src/server.ts` — serveur minimal compatible API Anthropic (`POST /v1/messages`, SSE)
- [ ] Renseigner SELECTORS.md depuis l'inspection DOM réelle
- [ ] Tester `ANTHROPIC_BASE_URL=http://127.0.0.1:8741 claude "dis bonjour"`
- [ ] v2 : tool-calls retour vers le filesystem Claude Code (full harness MCP)

## Hors périmètre v1

- Le packaging 3 OS (reprendre celui de l'upstream au moment du fork).
- Les autres surfaces (qwen, deepseek…) — YAGNI.
- L'auth automatisée : le login muse.ai se fait une fois à la main dans le profil persisté.
