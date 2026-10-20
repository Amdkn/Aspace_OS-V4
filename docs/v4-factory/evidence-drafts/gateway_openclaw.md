# Gateway OpenClaw — draft de preuve (M-16/D-N019, batch 2/3)

- **verdict** : NEEDS_LIVE_CHECK
- **proof_level** : executed (périmètre : harnais CLI mesuré — voir note)
- **date d'enquête** : 2026-10-09 · **clone** : `~/workspace/v4-capabilities` @ `2554e0f`

## Checks

| Check | Résultat | Preuve |
|---|---|---|
| Harnais `openclaw` mesuré | ✅ PASS | `os/business/_runtime/bridge/harnesses.json` : `statut: "mesure"`, `mesure_le: "2026-08-24"`, invocation `cli` → cible `openclaw` |
| Sonde d'exécution (joignable) | ✅ PASS | `sonde: {joignable: true, chemin: "C:\\Users\\amado\\AppData\\Roaming\\npm\\openclaw", motif: "trouve dans …\\npm"}` — note : « OpenClaw 2026.5.18, detecte par omniroute status » |
| Audit indépendant | ✅ PASS | `os/business/_audit/AUDIT_BRIDGE.md` : `openclaw | mesure | OUI — OpenClaw 2026.5.18 (50a2481) | Honnête` |
| Code de service Gateway dans V4 | ❌ FAIL | Aucun : seuls `os/life/openspec/changes/TOTAL_Spec/{ADR,DDD,PRD}/…FleetGateway.md` (specs) et `os/business/tools/watchdog-agentgateway.ps1` |
| `VITE_OPENCLAW_URL` configuré | ❌ FAIL | `os/life/.env.example` : `VITE_OPENCLAW_URL=<REPLACE_WITH_YOUR_VALUE>` (placeholder) |
| Auth du gateway | ❌ NON VÉRIFIÉ | Diagnostic V4 (2026-10-06) : « Gateway without auth » = risque résiduel connu |

## Artefacts
- `os/business/_runtime/bridge/harnesses.json` (entrée `openclaw`, statut `mesure`)
- `os/business/_audit/AUDIT_BRIDGE.md` (confirmation « Honnête », version `2026.5.18 (50a2481)`)

## not_verified
- Service gateway en cours d'exécution (URL, port)
- Authentification du gateway
- Routage réel de missions via le gateway

## live_checks_needed
1. Clarification de périmètre (Conseil) : la capacité vise-t-elle le **harnais** (mesuré le 2026-08-24 → qualifiable) ou un **service gateway** V4 (non prouvé) ?
2. Si gateway : URL du service en cours d'exécution + statut de l'authentification.

## Note de périmètre (honnête)
Le **harnais OpenClaw est réellement mesuré** : sonde exécutée le 2026-08-24, version identifiée, audit indépendant « Honnête » — c'est une preuve d'exécution avec artefacts. En revanche, aucun service « Gateway » OpenClaw n'existe dans le repo (specs seulement, URL non configurée, auth non prouvée). Recommandation : NEEDS_LIVE_CHECK — si le périmètre = harnais → QUALIFIED sur la mesure du 2026-08-24 ; si périmètre = service gateway → NOT_PROVEN en l'état.
