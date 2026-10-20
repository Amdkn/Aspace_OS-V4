# Fiche preuve — Automaton M0/M1/M2 (batch 1/3, M-16/D-N019)

- **verdict** : NOT_PROVEN
- **proof_level** : documented
- **capability** : Automaton M0/M1/M2 — `architecture/capabilities.json` → statut `qualification_planned`, cible `evidence/automaton_m0_m1_m2._qualification.json`

## Checks

| Check | Résultat | Preuve |
|---|---|---|
| Mentions V4 | ✅ pass | `architecture/ASpace-V4-PRD-Fork-CubeFarm.md:111`, `architecture/REFONDATION.md:134-137`, `architecture/Conseil_S2_Decision_18_capacites.md`, `architecture/GITHUB_LIFE_SOCIAL_TOPOLOGY.md`, `presentations/v3-v4/Analyse-transfert-V3-V4.md` |
| Héritage V3 | ✅ pass | `migration/v3-inventory.json` : `_INBOX/handoffs/HANDOVER-2026-10-05-AUDIT-GATEWAY-AUTOMATON.md` et `docs/architecture/AUTOMATON_GATEWAY_M0_M1_M2_PROPOSAL.md` (V3 @ `ad5e68e`), disposition `REFERENCE_PENDING_QUALIFICATION` |
| Code V4 | ❌ fail | Aucun module, service, test ou config `automaton` dans le repo V4 (hors docs et inventaire) |
| Exécution M0/M1/M2 | ❌ fail | Aucune trace d'exécution des échelles M0/M1/M2 dans V4 |
| Référence externe | ⚠️ hors périmètre | https://github.com/Conway-Research/automaton — référence de recherche (triptyque), pas une capacité runtime V4 ; non vérifiée live dans cette passe |

## Artefacts
- `migration/v3-inventory.json` (entrées AUTOMATON, disposition `REFERENCE_PENDING_QUALIFICATION`)
- `architecture/ASpace-V4-PRD-Fork-CubeFarm.md:109-111` — doctrine : « BMAD, gstack, CEO Bench, Automaton, OpenClaw, Hermes, Prime Agent et DeepSeek Harness restent des candidats présents dans le périmètre historique. […] Aucun nom de framework n'est assimilé à une capacité prouvée. »

## not_verified
- Contenu réel des docs V3 (non lus en détail — héritage, pas runtime V4)
- Repo externe Conway-Research/automaton (référence, pas preuve V4)

## Note de périmètre
Automaton M0/M1/M2 est un **candidat du périmètre historique** (proposition d'architecture V3), sans implémentation ni exécution dans V4. Statut honnête : NOT_PROVEN → retour devant le Conseil S2 à l'échéance. Si le Conseil veut le qualifier, la voie serait : implémenter ou démontrer M0/M1/M2 contre des usages Life/Business observables (cf. REFONDATION.md:134-137).
