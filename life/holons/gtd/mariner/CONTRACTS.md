# Mariner — Capture (A3, GTD Cerritos)

## Input contract
Required keys: mission_id, intent_ref, source_authority, observed_at, native_object_ref_or_unresolved, decision_scope, return_to.

Entrée: Demandes autorisées, sources datées, intentions A0.

## Decision contract
Capturer sans interpréter ni perdre la provenance, dédupliquer.

## Output contract
CaptureRecord: source, text, observed_at, receipt. Ajouter correlation_id, expected_effect, actual_effect_or_unknown, evidence_refs, recorded_at, status, next_owner, return_to.

## Cooperation
Boimler, HoloDeck, Morty. GTD ↔ Curie pour priorités, Picard pour projets, DEAL pour friction. Autorité et état restent chez le propriétaire natif; aucun système parallèle ne peut réinventer les ID.

## Exception
Si Tasks n'est pas disponible, proposer seulement.
