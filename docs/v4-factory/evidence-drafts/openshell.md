# Dossier de preuve — OpenShell
**Mission :** M-16 / D-N019 · **Échéance :** 2026-11-01 · **Clone :** `~/workspace/v4-capabilities` (main @ 2554e0f)
**Verdict : NOT_PROVEN** · **proof_level : documented** (3 mentions en docs, zéro code, zéro test, zéro exécution)

## Checks

| # | Check | Résultat | Preuve |
|---|---|---|---|
| 1 | Mention registre V4 | ✅ PASS (déclarée) | `architecture/capabilities.json` → statut `qualification_planned`, preuve cible `evidence/openshell._qualification.json` |
| 2 | Décision S2 | ✅ PASS (décidée) | `architecture/Conseil_S2_Decision_18_capacites.md` → QUALIFIER, échéance 2026-11-01 |
| 3 | Autres mentions docs | ⚠️ PARTIEL (listes) | `migration/README.md:77` : cité dans une énumération (« OpenShell/Octop ») parmi les éléments « rest[ant] dans architecture/capabilities.json » — aucune spec |
| 4 | Code | ❌ FAIL | 0 référence dans tout le code (`*.mjs`/`*.ts`/`*.tsx`/`*.py`/`*.sh` : 0 hit hors `.git`) |
| 5 | Fichiers dédiés | ❌ FAIL | aucun fichier `*openshell*` dans le repo |
| 6 | Tests | ❌ FAIL | 0 hit dans `tests/` |
| 7 | Exécution / endpoint / service | ❌ FAIL | rien d'exécutable, aucun port, aucun binaire, aucune config |
| 8 | Issues/PRs GitHub | — | 0 issue, 0 PR mentionnant « openshell » sur Amdkn/Aspace_OS-V4 |

## Artefacts
- `architecture/capabilities.json` (entrée, `qualification_planned`)
- `architecture/Conseil_S2_Decision_18_capacites.md` (décision S2 QUALIFIER)
- `migration/README.md` (mention en liste)

## not_verified
- Tout : aucune définition fonctionnelle d'OpenShell comme capacité runtime (ni spec, ni interface, ni implémentation)

## live_checks_needed
1. Définir la capacité : spec minimale (entrées/sorties, interface) — à défaut, il n'y a rien à prouver
2. Si une implémentation existe hors repo : la localiser, l'exécuter, capturer un output observable

## Note de périmètre (honnête)
OpenShell est un **nom au registre**, pas une capacité observable : 3 mentions documentaires, zéro substance exécutable. Sans preuve au 2026-11-01, retour devant le Conseil (condition S2) ; aucun retrait unilatéral (M-08).
