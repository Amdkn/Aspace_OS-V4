# DESIGN — aspace:business:H1

Flux: aspace:life:a3:discovery:reno → aspace:business:H1 → 8 DC B2 (DoD) → B3 (effets) → preuves/readback → A3. J1 ne reçoit que dépendances entre Jerry. Historique Gemini 30 juin: H2/IT et H3/IT. Fonctions contextuelles: huit B2 et huit B3 intactes.

Entrées: intent_ref, mission_id, correlation_id, authority_ref, expected_effect, acceptance, source_ref, return_to. Sorties: observed_effect_or_unknown, evidence_refs, decision_ref, next_owner, return_to.

Vérité des rôles et statuts: https://github.com/Amdkn/Aspace_OS-V4/blob/main/business/holons/registry.json ; ancrages/contributions: https://github.com/Amdkn/Aspace_OS-V4/blob/main/architecture/cross_os_collaboration.json . En cas d'état UNKNOWN, réconcilier les objets natifs avant retry. Absence de résultat personnel ≠ succès technique.

