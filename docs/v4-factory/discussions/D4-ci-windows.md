# [Discussion] [MISSION-S3] CI portable Windows : fcntl, sqlite verrouillé, memory-check

> Source : Audit Aspace_OS-V4 — 9 octobre 2026, §3.2, §3.4, §3.5
> Pour : Sessions Workers et Doctors (S2/S3)

## Mission typée (S1)

**Objectif :** `v4-checks.yml` verte sur runner `windows-latest` (sans désactiver de tests).

**Périmètre :**
- INCLUS :
  - remplacer `import fcntl` dans `portable/test_instance.py` (Unix-only) par une abstraction portable ;
  - fermer proprement la connexion sqlite3 dans `Journal.backup()` — ne pas compter sur le context manager de `sqlite3.connect()` (ne ferme pas sur Windows → `PermissionError` au cleanup) ;
  - régénérer `evidence/continuity-canary.json` après correction (le fichier actuel est obsolète : `continuity_canary.py` ne peut pas le produire).
- EXCLUS : désactiver des tests ou des steps CI pour « faire passer ».

**Critères de reçu (R10) :**
1. CI verte sur `windows-latest` ET `ubuntu-latest`.
2. `evidence/continuity-canary.json` frais : `capsule_sha256` et `heritage_errors` cohérents avec l'arbre courant.

**Gate humain :** aucun (gate supprimé par PR #24 — décision owner 2026-10-09).

## Prise en charge (Workers / Doctors)

Pour prendre cette mission : commentez `CLAIMED <session>` ci-dessous. À la fin : PR vers `main` + reçus (runs CI verts sur les deux OS). R10 : pas de statut « actif » sans reçu.
