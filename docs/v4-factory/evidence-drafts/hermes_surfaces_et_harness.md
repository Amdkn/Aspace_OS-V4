# Fiche preuve — Hermes surfaces et harness (batch 1/3, M-16/D-N019)

- **verdict** : NOT_PROVEN
- **proof_level** : documented
- **capability** : Hermes surfaces et harness — `architecture/capabilities.json` → statut `qualification_planned`, cible `evidence/hermes_surfaces_et_harness._qualification.json`

## Checks

| Check | Résultat | Preuve |
|---|---|---|
| Mention doctrine | ✅ pass | `agents/CONTRACT.md:19-20` : « Codex et Hermes produisent le même résultat typé » ; `:41` : « connexion Hermes sur runner cloud éphémère » |
| Slot provider | ✅ pass | `agents/registry.json` → `providers: ["codex", "jules", "hermes"]` — **noms seuls, aucun objet de configuration** (pas d'endpoint, pas de credentials, pas de paramètres) |
| Mentions repo | ✅ pass | 15 occurrences (`AGENTS.md`, `README.md`, `agents/README.md`, `control-plane/README.md`, `architecture/*`, `migration/v3-inventory.json`, `os/agent/*`) — toutes nominatives/doctrinales |
| Code harness Hermes | ❌ fail | Aucun fichier d'implémentation trouvé : pas de client, pas d'adaptateur, pas de skill, pas de config sous `harness/`, `agents/`, `control-plane/`, `tools/` |
| Surfaces Hermes | ❌ fail | Aucune « surface » (UI/API) attribuable à Hermes dans le repo |
| Connexion live | ❌ fail | Aucune connexion établissable : rien à quoi se connecter (pas d'URL, pas de credential) |

## Artefacts
- `agents/CONTRACT.md` (lignes 19-20, 41) — description doctrinale du rôle Hermes
- `agents/registry.json` — slot `hermes` dans `providers` (sans config)

## not_verified
- Existence d'un service Hermes externe (aucune URL connue dans le repo)
- Toute exécution via Hermes (aucune trace : pas de logs, pas de reçus, pas de runs)

## live_checks_needed
- Si un runner Hermes existe hors repo : URL + credential requis pour tester une connexion ; à défaut, la capacité reste indémontrable depuis la factory.

## Note de périmètre
Hermes est aujourd'hui un **nom de provider dans la doctrine du plan de contrôle**, pas une capacité runtime. Le PRD-Fork-CubeFarm le dit explicitement : « Aucun nom de framework n'est assimilé à une capacité prouvée. » Sans endpoint ni exécution, le statut honnête est NOT_PROVEN → retour devant le Conseil S2 à l'échéance (retrait éventuel : décision S2 + validation S1, jamais unilatéral — M-08).
