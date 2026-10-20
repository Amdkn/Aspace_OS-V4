# D-N021 / M-05 — Cube Farm d'abord : la factory DANS le monde 3D

**Mission :** M-05 (`REGISTRE-INSPIRATIONS.md`) — dispatch D-N021 (Nardole). **Plan :** 12e Doctor.
**Objectif :** le monde 3D est le véhicule de livraison ; la factory s'y branche, pas l'inverse.
**Thèse :** Cube Farm (3D) prime sur la mécanique factory (mémoire 2026-10-08).

## État actuel
- Cube Farm : control-plane `swarm` à `/workspaces/aspace/state/cubefarm`, app à `/workspaces/aspace/apps/cubefarm`, port **4417** (devcontainer).
- FreeLLMAPI : design existant `control-plane/README-freellmapi.md` ; fichiers stagés `~/workspace/v4-factory/control-plane/` (`setup-freellmapi.sh` idempotent, `devcontainer-3001.patch`, README) — D-N006.
- Grant GitHub App accordé (All repositories) → push débloqué.

## Bornes
**IN :** push des fichiers FreeLLMAPI dans le repo (PR, merge autorité 12e) ; exécution `setup-freellmapi.sh` dans le Codespace ; migration des clés (export JSON app desktop → import auto) ; clés factory en secrets GitHub Actions, clé dev en secrets Codespaces ; cohabitation Cube Farm (:4417) + FreeLLMAPI (:3001) + Claude Code + Codex ; runbook opérateur à jour.
**OUT :** le contenu 3D lui-même ; exposer :3001 publiquement pour Actions (**interdit** — local-only) ; toute modification de Cube Farm.

## Phases (séquentielles)
| Phase | Action | Gate |
|---|---|---|
| **P0 — Repo** | PR : `setup-freellmapi.sh` + `devcontainer-3001.patch` (+ README si absent) → merge 12e | PR mergée |
| **P1 — Codespace** | Appliquer le patch devcontainer (rebuild si besoin) ; lancer `setup-freellmapi.sh` ; migrer les clés ; récupérer la clé unifiée ; brancher Claude Code + Codex (`setup-claude` / `setup-codex`) | H-M05-1/2/3 |
| **P2 — Durcissement** | Port 3001 = private (vérifié) ; secrets hors git (vérifié) ; runbook à jour | H-M05-4/5/6 |

## Tests hold-out (définis avant exécution)
| ID | Vérifie | Seuil |
|---|---|---|
| **H-M05-1** | FreeLLMAPI sert | `curl -s http://localhost:3001/v1/models` → 200, liste non vide (depuis le Codespace) |
| **H-M05-2** | Cohabitation | :4417 (Cube Farm) ET :3001 répondent simultanément |
| **H-M05-3** | Routeur fonctionnel | requête smoke avec `ANTHROPIC_BASE_URL=http://localhost:3001` + clé unifiée → 200 (zéro clé Anthropic/OpenAI directe) |
| **H-M05-4** | Aucun secret en git | `git log --all -p` sur les nouveaux commits : aucun `freellmapi-…` ni `sk-…` ; sensibles sous `/workspaces/aspace/state/freellmapi/` (hors git), `.env` 0600 |
| **H-M05-5** | Local-only | port 3001 = **private** dans la config du Codespace (jamais public) |
| **H-M05-6** | Runbook vrai | `README-freellmapi.md` reflète l'état réel (script dans le repo, port forwardé, procédure clés) |

**Reçu (mission) :** le Codespace V4 sert Cube Farm et FreeLLMAPI sur :3001 ; runbook opérateur à jour.
**Contrainte capacité :** P1 s'exécute dans le terminal du Codespace (compte Capitaine) — route préférée : browser task ; sinon handoff documenté. C'est une capacité-compte, pas un gate.
