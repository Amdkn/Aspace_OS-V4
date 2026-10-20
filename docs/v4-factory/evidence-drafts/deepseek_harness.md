# Dossier de preuve — DeepSeek Harness
**Mission :** M-16 / D-N019 · **Échéance :** 2026-11-01 · **Clone :** `~/workspace/v4-capabilities` (main @ 2554e0f)
**Verdict : NOT_PROVEN** · **proof_level : installed** (wrapper UI en code, harnais lui-même jamais exécuté ; la sonde du registre a mesuré son absence)

## Checks

| # | Check | Résultat | Preuve |
|---|---|---|---|
| 1 | Entrée registre harnais | ✅ PASS (déclarée) | `os/business/_runtime/bridge/harnesses.json` → id `dsh`, `statut: "suppose"`, `mesure_le: null` |
| 2 | Sonde de joignabilité | ❌ FAIL (mesuré absent) | même fichier : `sonde.joignable: false`, « absent du PATH et des repertoires connus (68 repertoires sondes) », sonde du 2026-08-24 ; note : « PISTE NON VERIFIEE… A confirmer contre la doc Cordis/DSH » |
| 3 | Code wrapper UI | ✅ PASS | `os/agent/src/apps/DeepSeekHarness/index.tsx` (23 lignes : `DeepSeekHarnessApp` = `Cadre` iframe vers `http://127.0.0.1:3080`, remède « `dsh web --port 3080` ou cliquer sur Lancer ») |
| 4 | Entrée routeur | ✅ PASS (déclarée) | `os/agent/tools/routeurs-api.ts:105-111` (cle `deepseek`, port 3080, lanceur `C:/Users/amado/agent-os/desktop/lancer_dsh.cmd` — chemin Windows) |
| 5 | Lanceur | ✅ PASS (fichier) | `os/agent/lancer_dsh.cmd` présent |
| 6 | Binaire `dsh` présent | ❌ FAIL | absent du PATH et des répertoires connus sur cette VM (recherche système : 0 résultat) |
| 7 | Serveur `:3080` joignable | ❌ FAIL | `curl http://127.0.0.1:3080/` : pas de réponse (000) |
| 8 | Dépendance package | ❌ FAIL | aucune mention `dsh`/`deepseek` dans `os/agent/package.json` ni `package.json` racine |
| 9 | Tests | ❌ FAIL | aucun test ne référence deepseek/dsh (`os/agent/src` : 0 fichier `*.test.*`) |
| 10 | Issues/PRs GitHub | — | 0 issue, 0 PR mentionnant deepseek sur Amdkn/Aspace_OS-V4 |

## Artefacts
- `os/agent/src/apps/DeepSeekHarness/index.tsx` (wrapper UI)
- `os/agent/tools/routeurs-api.ts` (entrée routeur, chemins Windows)
- `os/agent/lancer_dsh.cmd`
- `os/business/_runtime/bridge/harnesses.json` (entrée `dsh`, statut `suppose`, sonde négative du 2026-08-24)

## not_verified
- Installation de `dsh` (binaire introuvable, source d'installation non documentée dans le repo)
- `dsh web --port 3080` démarré et servant l'UI — jamais observé
- Plugin ACP supposé (`dsh-plugin-acp`) — piste non vérifiée contre la doc Cordis/DSH
- Capacités annoncées (`tool_call`, `file_edit`, `shell`, `mcp`) — jamais exercées

## live_checks_needed
1. Installer `dsh` depuis sa source officielle (à identifier — absente du repo), `dsh --version`
2. `dsh web --port 3080`, `curl -s http://127.0.0.1:3080/` → 200 + capture d'écran du rendu
3. Exercer une capacité (ex. `tool_call`) et conserver le reçu

## Note de périmètre (honnête)
Le **périphérique** existe (app UI + routeur + lanceur), mais le **harnais** n'a jamais été mesuré : la sonde du registre elle-même a constaté son absence le 2026-08-24. Wrapper ≠ capacité prouvée. Sans preuve au 2026-11-01, retour devant le Conseil (condition S2) ; aucun retrait unilatéral (M-08).
