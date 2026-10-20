# [Discussion] [MISSION-S2] Qualifier capabilities.json (18/19 sans preuve) + statuer Supabase

> Source : Audit Aspace_OS-V4 — 9 octobre 2026, §3.8 et §3.9
> Pour : Sessions Workers et Doctors (S2/S3)

## Mission typée (S1)

**Objectif :** chaque capacité a une preuve runtime ou est retirée ; le statut Supabase est tranché et documenté.

**Périmètre :**
- INCLUS :
  - pour chaque capacité `to_qualify_from_sources` (18/19, `source_revision: null`, `runtime_evidence: null`) : fournir la preuve runtime OU la retirer du registre ;
  - mettre à jour `architecture/SUPABASE_RUNTIME.md` (Agent OS Backend `biyecksylqonuovqmbtz` = INACTIVE : reconnecter ou acter l'abandon) ;
  - MCP Supabase non authentifiés (`Unauthorized. Please provide a valid access token`) : authentifier ou retirer la configuration.
- EXCLUS : ajouter de nouvelles capacités.

**Critères de reçu (R10) :**
1. Zéro capacité `to_qualify_from_sources` sans plan de qualification daté.
2. `SUPABASE_RUNTIME.md` reflète l'état réel et vérifiable.

**Gate humain :** aucun pour la qualification. **DÉCISION VISION** si abandon Supabase (connecteur, coût, stratégie data) → remonte au Capitaine, seul point vision du lot.

## Prise en charge (Workers / Doctors)

Pour prendre cette mission : commentez `CLAIMED <session>` ci-dessous. À la fin : PR vers `main` + reçus (capabilities.json vérifié, doc runtime à jour). R10 : pas de statut « actif » sans reçu.
