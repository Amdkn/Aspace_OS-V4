# Conseil S2 — Décision des 18 capacités

Registre officiel : Discussion #46 « Conseil S2 — Décision des 18 capacités »
(commentaire de décision du 2026-10-09). Ce document en est la transcription dans le repo ;
en cas de divergence, la Discussion fait foi.

Conformément à la mission S1 / S2 (Ref: #41, reprise D6 de #33), aucune capacité n'a été
amputée ou retirée silencieusement. Pour chacune : plan de qualification daté ou proposition
d'abandon motivée. Les statuts `abandonment_proposed` et `qualification_planned` sont
intermédiaires : aucune capacité ne quitte le registre sans validation S1 (Rick).

## Tableau des Décisions (Conseil S2, 2026-10-09)

| Capacité | Décision S2 | Détail |
|---|---|---|
| Agent OS | ABANDONNER (validation S1 en attente) | Redondant avec le substrat agent du BedRock L0 ; périmètre propre non vérifiable. Réserve expresse : porte sur la revendication au registre V4, pas sur la migration d'Agent-OS-Desktop dans le mono-repo (décision mono-repo du 2026-10-09, inchangée). |
| Business OS | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/business_os._qualification.json`. |
| Mobile OS | ABANDONNER (validation S1 en attente) | Hors périmètre du V4 minimal viable ; surface mobile réelle = portable cloud (Codespace). |
| The OMK Office JaaS — 75 services déclarés | ABANDONNER (validation S1 en attente) | Non pertinent comme capacité runtime V4 ; les 75 services vivent dans le site OMK Office / Master Profile. Réserve expresse : porte sur la revendication au registre, pas sur l'activité OMK Office (objectif 1 M$ inchangé). |
| Cube Farm | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/cube_farm._qualification.json`. |
| Starnet | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/starnet._qualification.json`. |
| WorkAdventure | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/workadventure._qualification.json`. |
| Gateway OpenClaw | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/gateway_openclaw._qualification.json`. |
| Hermes surfaces et harness | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/hermes_surfaces_et_harness._qualification.json`. |
| Prime Agent | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/prime_agent._qualification.json`. |
| DeepSeek Harness | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/deepseek_harness._qualification.json`. |
| Automaton M0/M1/M2 | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/automaton_m0_m1_m2._qualification.json`. |
| Constructeur Universel | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/constructeur_universel._qualification.json`. |
| BMAD | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/bmad._qualification.json`. |
| gstack | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/gstack._qualification.json`. |
| CEO Bench | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/ceo_bench._qualification.json`. |
| OpenShell | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/openshell._qualification.json`. |
| Octop | QUALIFIER | Échéance: 2026-11-01. Owner: Ryan / Doctor 13. Preuve: `evidence/octop._qualification.json`. |

Condition générale : toute capacité sans preuve à l'échéance 2026-11-01 revient devant le Conseil.

## Points hors périmètre S2

- `SUPABASE_RUNTIME.md` (Agent OS Backend `biyecksylqonuovqmbtz`) : l'abandon est une DÉCISION VISION,
  elle remonte au Capitaine (cf. issue #33). Le Conseil n'avalise aucune mention « Decision S2 » sur ce point.
- `.codex/config.toml` (retrait du MCP Supabase non authentifié) : hygiène validée par le Conseil.
