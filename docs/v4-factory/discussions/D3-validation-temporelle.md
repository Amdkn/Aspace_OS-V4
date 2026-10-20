# [Discussion] [MISSION-S2] Validation temporelle honnête : schéma, dates, corrélation chronologique

> Source : Audit Aspace_OS-V4 — 9 octobre 2026, §2.2 à §2.7
> Pour : Sessions Workers et Doctors (S2/S3)

## Mission typée (S1)

**Objectif :** le schéma rejette ce qu'il prétend rejeter ; la corrélation est chronologique (instants réels, pas chaînes) ; les états épistémiques sont dérivés, pas auto-déclarés.

**Périmètre :**
- INCLUS :
  - aligner le draft JSON-Schema (fichier déclare draft-2020-12, code en dur draft-07) ;
  - activer `FormatChecker` pour `format: date-time` ;
  - valider les dates à la lecture (`ingest_claim()`), pas seulement à l'écriture ;
  - trier par instant (`datetime` aware) dans `state_at()` / `replay_history()`, pas par chaîne ;
  - même instant + même autorité + valeurs conflictuelles → un seul CURRENT (règle explicite à définir) ;
  - `freshness` dérivé de `age_seconds` (au lieu du littéral `"UNKNOWN"`) ;
  - `replay_history()` signale le contenu tronqué, pas seulement `truncated: true` ;
  - `CONTRADICTED` exclu de CURRENT.
- EXCLUS : refonte du modèle de graphe.

**Critères de reçu (R10) :**
1. La matrice de l'audit devient verte : `observed_at: "NOT-A-DATE"` rejeté, `recorded_at: "also not"` rejeté, `assertion: {nested dict}` rejeté, `format: date-time` appliqué.
2. Test fuseaux : `2026-10-05T19:00:00+02:00` et `2026-10-05T17:00:00+00:00` reconnus comme le même instant (plus de verdict opposé selon le fuseau).
3. `observed_at: "a"` → rejeté à l'ingestion.

**Gate humain :** aucun (gate supprimé par PR #24 — décision owner 2026-10-09).

## Prise en charge (Workers / Doctors)

Pour prendre cette mission : commentez `CLAIMED <session>` ci-dessous. À la fin : PR vers `main` + reçus (matrice de validation verte + tests fuseaux). R10 : pas de statut « actif » sans reçu.
