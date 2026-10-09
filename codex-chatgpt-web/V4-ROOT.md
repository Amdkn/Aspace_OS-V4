# codex-chatgpt-web — à la racine de Aspace OS V4

> Décision Capitaine, 2026-10-09 : le projet codex-chatgpt-web (fork
> `Amdkn/codex-chatgpt-web` de `miuuyy/codex-chatgpt-web`) vit à la racine
> du mono-repo V4, pas comme repo isolé.

## Contenu

| Chemin | Origine |
|---|---|
| `src/adapters/chatgpt-web/` | surface ChatGPT Web (upstream) |
| `src/adapters/base.ts` | contrat d'adapter (upstream) |
| `launcher/`, `src/`, `docs/`… | fork tel quel (vendored) |
| `bridge-muse-web/` | **surface `muse_web`** — adaptation à Muse pour Claude Code local (travail A0, nouveau) |

## bridge-muse-web en bref

```
Claude Code local (ANTHROPIC_BASE_URL=http://127.0.0.1:8741)
  → bridge-muse-web (API Anthropic / SSE)
  → Playwright → muse.ai (side chat « Claude Code Bridge »)
  → A0 Amadeus
```

- `bridge-muse-web/src/server.ts` — serveur Bun `:8741`, `POST /v1/messages`, SSE.
- `bridge-muse-web/src/surfaces/muse-web/adapter.ts` — pilote Playwright.
- `bridge-muse-web/src/surfaces/muse-web/selectors.json` — 7 sélecteurs DOM
  stables (attributs `data-hatch-*`, `aria-label`), relevés sur navigateur réel
  le 2026-10-09. Si un sélecteur dérive : échec explicite, jamais de bascule
  silencieuse (règle upstream).
- `bridge-muse-web/INSTALL.md` — installation et test local (Windows PowerShell inclus).

## Test local (machine du Capitaine)

```powershell
cd codex-chatgpt-web/bridge-muse-web
bun install; bunx playwright install chromium
$env:BRIDGE_PROFILE_DIR="./.bridge-profile"; bun src/server.ts   # login muse.ai une fois
# autre terminal :
$env:ANTHROPIC_BASE_URL="http://127.0.0.1:8741"; $env:ANTHROPIC_AUTH_TOKEN="bridge-local"
claude "dis bonjour"
```

## Évolutions prévues

- V1 : A0 répond avec ses propres outils (prouver `muse_web` d'abord — doctrine Ponytail).
- V2 : porter l'adapter vers le contrat `src/adapters/base.ts` (full harness MCP).
- Surfaces suivantes (Qwen, DeepSeek, Gemini…) : uniquement après preuve V1.
