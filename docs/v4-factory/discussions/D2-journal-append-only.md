# [Discussion] [MISSION-S2] Journal append-only réel : détecter toute mutation hors append()

> Source : Audit Aspace_OS-V4 — 9 octobre 2026, §2.1 (« P4 : l'instrument qui ment »)
> Pour : Sessions Workers et Doctors (S2/S3)

## Mission typée (S1)

**Objectif :** toute suppression ou insertion directe en SQL est détectée ; aucun claim forgé ne devient CURRENT.

**Périmètre :**
- INCLUS : verrouillage et/ou checksum de la base SQLite ; vérification d'intégrité à la lecture (`graph()`, `ingest_claim()`, `state_at()`), pas seulement à l'écriture ; journalisation des accès.
- EXCLUS : changement du format des claims.

**Critères de reçu (R10) :**
1. Test d'intrusion automatisé : suppression d'une ligne en SQL direct → `graph()` lève une erreur d'intégrité (pas de disparition silencieuse).
2. Insertion d'un claim forgé en SQL direct → rejeté ; `state_at()` ne le renvoie jamais comme CURRENT.

**Gate humain :** aucun (gate supprimé par PR #24 — décision owner 2026-10-09).

## Prise en charge (Workers / Doctors)

Pour prendre cette mission : commentez `CLAIMED <session>` ci-dessous. À la fin : PR vers `main` + reçus (test d'intrusion vert). R10 : pas de statut « actif » sans reçu.
