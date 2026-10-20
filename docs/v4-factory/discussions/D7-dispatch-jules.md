# [Discussion] [MISSION-S2/S3] Diagnostic dispatcher Jules : file vide + santé du tuyau — RÉSOLU 2026-10-09

> Source : diagnostic S1 — 2026-10-09 (~11:15 EDT), complété ~11:25 EDT via navigateur.
> Pour : Sessions Workers et Doctors (S2/S3)

## Résolution (ne plus prendre cette mission)

- **Cause racine confirmée : file `factory:ready` vide.** Seule #5 l'a portée (consommée le 07-10 via PR #22). Le run #142 du 09-10 le dit lui-même : « No eligible issue; no model call ».
- **Dispatcher sain :** 25+ derniers runs de `Aspace Issue Factory` tous verts, cron 11,41 actif. L'épisode des 38 runs en échec (07-08/10) est clos.
- **Correctif appliqué :** `.github/workflows/auto-label-factory-ready.yml` créé sur `main` (commit `656022d`, 09-10 11:22 EDT) — toute nouvelle issue reçoit automatiquement `factory:ready` (opt-out : label `no-factory`).

## Mission typée (S1) — archivée pour traçabilité

## Mission typée (S1)

**Objectif :** établir pourquoi Jules ne reçoit plus de missions, et remettre un run vert du dispatcher.

**Périmètre :**
- INCLUS :
  - état des runs récents de `Aspace Issue Factory` (onglet Actions) : verts ou rouges ? Si rouges, cause racine (`JULES_API_KEY`, bug `tools/issue_factory.py`, etc.) ;
  - vérifier que le cron `11,41 * * * *` tourne et réconcilie la file ;
  - confirmer que la file `factory:ready` est vide (constat S1 : seule #5 l'a portée, consommée le 07-10 via PR #22) ;
  - produire un run vert **vérifié depuis son log** (pas depuis l'absence d'emails d'échec).
- EXCLUS : labelliser de nouvelles issues (décision S1/Capitaine, pas du diagnostic).

**Critères de reçu (R10) :**
1. Diagnostic écrit : cause de l'inactivité (file vide / dispatcher cassé / les deux), avec preuves (liens vers runs).
2. Un run `Aspace Issue Factory` vert, vérifié depuis son log.

**Gate humain :** aucun.

## Prise en charge (Workers / Doctors)

Pour prendre cette mission : commentez `CLAIMED <session>` ci-dessous. À la fin : reçu écrit + lien du run vert. R10 : pas de statut « actif » sans reçu.
