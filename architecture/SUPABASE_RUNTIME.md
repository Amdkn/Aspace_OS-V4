# Supabase dans la refondation V4

## Observation du 6 octobre 2026
Life OS (hjweyhpmrxqsxfbibsnc) : ACTIVE_HEALTHY. Agent OS Backend (biyecksylqonuovqmbtz) : ABANDON_PROPOSE (proposition worker — décision vision : Capitaine, cf. issue #33 ; le Conseil S2 n'avalise pas). Verification par list_projects et information_schema.tables ; aucune donnee personnelle exportee, aucune migration executee.

Tables Life OS : fw_12wy, fw_deal, fw_gtd, fw_ikigai, fw_life_wheel, fw_para, ikigai_visions, life_wheel_ambitions, ld01_business, ld02_finance, ld03_health, ld04_cognition, ld05_relations, ld06_habitat, ld07_creativity, ld08_impact, symphony_state, sys_agent_veto, sys_shell_routing, user_profiles, wrappers_fdw_stats.

## Observation du 21 octobre 2026 — Agent OS Backend reconnecte (acte D-N036, decision #33)
Etat actuel : Agent OS Backend (biyecksylqonuovqmbtz) : RECONNECTE. L'etat ABANDON_PROPOSE consigne dans l'observation du 6 octobre 2026 est supplee par le present acte : les actes materiels du Capitaine du 21 octobre 2026 (restauration du projet + depot de la cle au Vault) repondent « reconnecter » a la decision #33 — decision vision du Capitaine ; le Conseil S2 n'avait pas avalise l'abandon. Preuve du jour : sonde authentifiee d'A0 — reponse 200 sur Agent OS Backend.

Cadrage du Capitaine, verse tel quel au dossier : « le projet Supabase OMK n'est qu'un Business en L2 » ; un nouveau Business client sera cree plus tard ; sequence : Setup du BedRock d'abord.

Garde-fou : cette reconnexion ne fait pas de Supabase une dependance operationnelle du substrat. Le BedRock n'en depend pas pour operer ; la qualification du stockage du substrat (Phase 0 du Noyau A1 : voie locale embarquee qualifiee en premiere, Supabase tenue comme dependance nommee) reste inchangee. Le projet reconnecte vit au niveau L2 (un Business), pas au L0.

## Repartition pour les brainstormings
- Bedrock L0 : constitution versionnee dans Git ; les tables ne definissent pas seules la constitution V4.
- Life Core L1 / Doctor 11 : huit domaines en equilibre. Life OS est un patrimoine vivant ; LD01 Business ne remplace pas les sept autres domaines.
- Graham / memoire L2 : Git et OpenWiki portent les connaissances revues et leur provenance ; Supabase peut porter les etats structures et relations. Un index vectoriel reste derive et reconstructible.
- GitHub : Directory, missions, discussions, decisions, PR, preuves et promotion. Conserver les identifiants GitHub sans dupliquer les backlogs.
- Gateway : route les missions vers les harness. Supabase ne devient ni routeur de modeles ni identite de holon.
- CubeFarm : surface et execution dans le Codespace V4. Etat actuellement sur disque cloud ; aucune synchronisation Supabase implementee.

## Decisions ouvertes
LD05 Social et ld05_relations demandent une correspondance explicite. LD06 Famille et ld06_habitat ne sont pas synonymes : conserver les deux intentions. Inspecter colonnes, dependances et RLS avant toute migration. Agent OS Backend reconnecte (2026-10-21) ne doit pas etre presente comme dependance operationnelle du substrat (cf. observation du 21 octobre 2026).

Avant un brainstorming : lire REFONDATION.md, le Directory, ce document et les contrats de memoire. Comparer reutilisation avec adaptateurs et schema V4 distinct avec migration reversible. Montrer les consequences sur les huit LD, les six frameworks et les surfaces. Distinguer observation, proposition et preuve.

## Contrat cible des effets (non deploye)
Chaque effet distribue porte mission_id, correlation_id, effect_id, provenance et return_to. Une outbox transactionnelle et un consommateur idempotent pourront relier les changements aux receipts GitHub ; Realtime seul ne prouve pas la livraison. Definir proprietaire, retention, RLS et recuperation avant activation. Ni service-role dans le navigateur, ni secrets dans Git.

## Connexion
Le MCP Life OS prepare dans .codex/config.toml sert a la decouverte en lecture seule. OAuth dans le Codespace reste necessaire ; le connecteur ChatGPT ne transmet pas ses credentials au harness. Les futures missions d ecriture auront des migrations versionnees et des capacites temporaires/permanentes organisees au Gateway.

Source : https://supabase.com/docs/guides/ai-tools/mcp
