# Fiche preuve — BMAD (batch 1/3, M-16/D-N019)

- **verdict** : QUALIFIED
- **proof_level** : executed
- **capability** : BMAD — `architecture/capabilities.json` → statut `qualification_planned`, cible `evidence/bmad._qualification.json`

## Checks

| Check | Résultat | Preuve |
|---|---|---|
| Installation | ✅ pass | **52 skills** `bmad-*` dans `os/business/.claude/skills/` (ex. `bmad-agent-dev/SKILL.md` : agent « Amelia », contenu réel, conventions `{skill-root}`/`{project-root}`) |
| Installation (2) | ✅ pass | `os/business/_bmad/` : `_config`, `bmm/` (config.yaml, module-help.csv, v6-shims), `core/`, `custom/`, `scripts/` (config_utils.py, context.py, memlog.py, render_skill.py, resolve_config.py), `config.toml`, `config.user.toml` |
| Exécution — specs | ✅ pass | `os/business/_bmad-output/specs/` : SPEC.md + stories.yaml + stories détaillées (ex. `spec-couche-ontologie/`, `spec-themes-par-app/`) — sorties réelles d'un workflow BMAD |
| Exécution — build-auto | ✅ pass | `os/business/_bmad-output/implementation-artifacts/bmad-build-auto-result-story2-2026-08-05.md` : résultat d'un run build-auto **avec statut honnête `blocked`** et motif réel (worktree basé sur `03fd40d` antérieur à l'implémentation sur `main`) — trace d'exécution authentique, pas une fixture |
| Exécution — artefacts | ✅ pass | `deferred-work.md`, `spec-people-personas-memoire-codex.md` dans `implementation-artifacts/` |
| Mentions doctrine | ✅ pass | `architecture/ASpace-V4-PRD-Fork-CubeFarm.md`, `REFONDATION.md`, `migration/README.md`, `portable/README.md` (« exploration BMAD/Gstack/CEO Bench ») |

## Artefacts
- `os/business/.claude/skills/bmad-*/` (52 skills)
- `os/business/_bmad/` (installation complète)
- `os/business/_bmad-output/` (specs, stories, résultats de runs)

## not_verified
- Version exacte de la méthode BMAD installée (bmm/config.yaml non comparé à l'upstream)
- Rejouabilité d'un run complet ici (nécessiterait Claude Code ; les traces existantes font foi de l'exécution passée)
- Couverture : les 52 skills n'ont pas toutes des traces d'usage individuel

## Note de périmètre
BMAD est **installé et a réellement tourné** dans l'historique du projet (specs, stories, build-auto avec reçus honnêtes y compris `blocked`). Le périmètre asserté : méthode BMAD opérationnelle dans `os/business`, pas « toutes les 52 skills utilisées en production ».
