# [Discussion] [MISSION-S2] Implémenter aspace/memory.py (module vide, 0 octet)

> Source : Audit Aspace_OS-V4 — 9 octobre 2026, §3.1
> Pour : Sessions Workers et Doctors (S2/S3)

## Mission typée (S1)

**Objectif :** `python -m aspace.memory` fonctionne comme documenté (README, AGENTS.md) — la primitive de mémoire durable existe réellement.

**Périmètre :**
- INCLUS : module CLI avec `--db`, écriture/lecture du journal durable, conforme à la documentation existante.
- EXCLUS : refonte du journal (voir mission D2 « Journal append-only réel »).

**Critères de reçu (R10) :**
1. Les commandes documentées dans README/AGENTS.md s'exécutent sans erreur.
2. Round-trip écriture → lecture vérifié par test automatisé.

**Gate humain :** aucun (gate supprimé par PR #24 — décision owner 2026-10-09).

## Prise en charge (Workers / Doctors)

Pour prendre cette mission : commentez `CLAIMED <session>` ci-dessous. À la fin : PR vers `main` + reçus (test round-trip vert). R10 : pas de statut « actif » sans reçu.
