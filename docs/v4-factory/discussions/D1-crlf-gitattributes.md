# [Discussion] [MISSION-S2] Corriger la racine CRLF : .gitattributes + renormalisation (tests 69/69)

> Source : Audit Aspace_OS-V4 — 9 octobre 2026, §1 et §3.3
> Pour : Sessions Workers et Doctors (S2/S3)

## Mission typée (S1)

**Objectif :** 69/69 tests verts sur checkout Windows et Linux ; `tools/memory.py check --root 40_Memory` → `ok: true`.

**Périmètre :**
- INCLUS : créer `.gitattributes` (`* text=auto`, `*.py text eol=lf`), `git add --renormalize`, commit. Vérifier `watch.lock.json` (SHA-256 LF) et `40_Memory/raw/`.
- EXCLUS : toute modification de code métier. Aucune.

**Critères de reçu (R10) :**
1. `python -m unittest` : 69 pass, 0 fail, sur runner `windows-latest` ET `ubuntu-latest`.
2. `python heritage.py verify` → `ok: true` (corpus V3 intègre, 1 341 sources).
3. `python tools/memory.py check --root 40_Memory` → `{"ok": true, …}`.

**Gate humain :** aucun (gate supprimé par PR #24 — décision owner 2026-10-09).

## Prise en charge (Workers / Doctors)

Pour prendre cette mission : commentez `CLAIMED <session>` ci-dessous. À la fin : PR vers `main` + reçus (logs des 3 commandes ci-dessus sur les deux OS). R10 : pas de statut « actif » sans reçu.
