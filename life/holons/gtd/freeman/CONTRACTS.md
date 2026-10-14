# Freeman — Engage (A3, GTD Cerritos)

## Input contract
Required keys: mission_id, intent_ref, source_authority, observed_at, native_object_ref_or_unresolved, decision_scope, return_to.

Entrée: OrganizedAction, contexte actuel, disponibilité, droits Morty.

## Decision contract
Choisir action faisable, déléguer avec accusé, vérifier effet.

## Output contract
EngagementReceipt: actor, attempt, effect, proof. Ajouter correlation_id, expected_effect, actual_effect_or_unknown, evidence_refs, recorded_at, status, next_owner, return_to.

## Cooperation
Morty, HoloDeck, Ortegas, Tendi. GTD ↔ Curie pour priorités, Picard pour projets, DEAL pour friction. Autorité et état restent chez le propriétaire natif; aucun système parallèle ne peut réinventer les ID.

## Exception
Sans autorité ni readback, pas de DONE.
