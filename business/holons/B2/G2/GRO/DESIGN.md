# DESIGN — aspace:business:G2:GRO

Réseau: A3 correspondant au Jerry → aspace:business:G1 → aspace:business:G2:GRO → aspace:business:G3:GRO → receipt → Jerry/A3. Type de rattachement historique: CURRENT_JERRY_FUNCTION. Chaque Jerry conserve les huit fonctions B2, indépendamment de l'ancrage de juin.

Entrées: source_ref, mission_id, correlation_id, JTBD, constraints, DoD, authority_ref, return_to. Sorties: artifact_ref, observed_effect_or_unknown, evidence_refs, cost, next_owner, return_to.

Principes: une mission = un propriétaire de résultat, S3 Tech coopère sous son propre Doctor sans rattachement exclusif. En cas de timeout, état UNKNOWN avant toute duplication. Registre source https://github.com/Amdkn/Aspace_OS-V4/blob/main/architecture/cross_os_collaboration.json
