# Supabase dans la refondation V4

## Observation du 6 octobre 2026
Life OS (hjweyhpmrxqsxfbibsnc) : ACTIVE_HEALTHY. Agent OS Backend (biyecksylqonuovqmbtz) : INACTIVE. Verification par list_projects et information_schema.tables ; aucune donnee personnelle exportee, aucune migration executee.

Tables Life OS : fw_12wy, fw_deal, fw_gtd, fw_ikigai, fw_life_wheel, fw_para, ikigai_visions, life_wheel_ambitions, ld01_business, ld02_finance, ld03_health, ld04_cognition, ld05_relations, ld06_habitat, ld07_creativity, ld08_impact, symphony_state, sys_agent_veto, sys_shell_routing, user_profiles, wrappers_fdw_stats.

## Repartition pour les brainstormings
- Bedrock L0 : constitution versionnee dans Git ; les tables ne definissent pas seules la constitution V4.
- Life Core L1 / Doctor 11 : huit domaines en equilibre. Life OS est un patrimoine vivant ; LD01 Business ne remplace pas les sept autres domaines.
- Graham / memoire L2 : Git et OpenWiki portent les connaissances revues et leur provenance ; Supabase peut porter les etats structures et relations. Un index vectoriel reste derive et reconstructible.
- GitHub : Directory, missions, discussions, decisions, PR, preuves et promotion. Conserver les identifiants GitHub sans dupliquer les backlogs.
- Gateway : route les missions vers les harness. Supabase ne devient ni routeur de modeles ni identite de holon.
- CubeFarm : surface et execution dans le Codespace V4. Etat actuellement sur disque cloud ; aucune synchronisation Supabase implementee.

## Decisions ouvertes
LD05 Social et ld05_relations demandent une correspondance explicite. LD06 Famille et ld06_habitat ne sont pas synonymes : conserver les deux intentions. Inspecter colonnes, dependances et RLS avant toute migration. Agent OS inactif est acté comme abandonné et retiré du registre (conformément à l'audit M3 de qualification).

Avant un brainstorming : lire REFONDATION.md, le Directory, ce document et les contrats de memoire. Comparer reutilisation avec adaptateurs et schema V4 distinct avec migration reversible. Montrer les consequences sur les huit LD, les six frameworks et les surfaces. Distinguer observation, proposition et preuve.

## Contrat cible des effets (non deploye)
Chaque effet distribue porte mission_id, correlation_id, effect_id, provenance et return_to. Une outbox transactionnelle et un consommateur idempotent pourront relier les changements aux receipts GitHub ; Realtime seul ne prouve pas la livraison. Definir proprietaire, retention, RLS et recuperation avant activation. Ni service-role dans le navigateur, ni secrets dans Git.

## Connexion
Le MCP Life OS prepare dans .codex/config.toml sert a la decouverte en lecture seule. OAuth dans le Codespace reste necessaire ; le connecteur ChatGPT ne transmet pas ses credentials au harness. Les futures missions d ecriture auront des migrations versionnees et des capacites temporaires/permanentes organisees au Gateway.

Source : https://supabase.com/docs/guides/ai-tools/mcp
