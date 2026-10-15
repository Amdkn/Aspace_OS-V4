# Ortegas — Execution et Time Use (A3, 12WY Curie)

## Input contract
Required keys: mission_id, intent_ref, source_authority, observed_at, native_object_ref_or_unresolved, decision_scope, return_to.

Entrée: Tactiques acceptées Una, disponibilité, carnet de vol.

## Decision contract
Préparer créneaux si mandat, observer effets, consigner blocages.

## Output contract
FlightLog: slot, actual_effect, evidence, return_to. Ajouter correlation_id, expected_effect, actual_effect_or_unknown, evidence_refs, recorded_at, status, next_owner, return_to.

## Cooperation
Curie, Una, Freeman, Chapel, Morty. Ikigai/Discovery → Curie, Picard/Summers, Jerry; GTD actions et DEAL friction. Autorité et état restent chez le propriétaire natif; aucun système parallèle ne peut réinventer les ID.

## Exception
Calendar lu ≠ autorisation d'inviter ou d'exécuter.


## Résidence constitutionnelle V4 — life/holons/A3/Curie/Ortegas
**Relation 1 — rattachement institutionnel.** Ortegas est A3; manager [Curie A2](https://github.com/Amdkn/Aspace_OS-V4/tree/main/life/holons/A2/Curie). Chemin stable source `wy/ortegas` = alias historique, non seconde institution. Ce contrat appartient exclusivement à `life/holons/A3/Curie/Ortegas`.

**Relation 2 — coopération de pairs.** Pike, Una, M'Benga, Chapel. Les A3 conservent leur manager Curie lors d'une contribution GTD ou DEAL; coopération réentrante sans pipeline rigide.

**Relation 3 — engagement transversal.** exécution hebdomadaire, temps réel, signaler blocages vers GTD/DEAL. Un même `mission_id/correlation_id` peut être observé par Curie (Rock), HoloDeck/GTD (action/attente), HoloJaneway/DEAL (friction/gain net). Chacun conserve son rôle, ne fabrique pas d'ID natif ni d'engagement non ratifié. GTD peut faire réviser le cycle; DEAL peut retirer l'action avant exécution et renvoyer sa capacité libérée.

**Références.** [Projet Linear Curie](https://linear.app/aspace-os/project/a2-curie-12-week-year-4cc3d3c89481) · [Issue institution SOH-93](https://linear.app/aspace-os/issue/SOH-93) · [Index des résidences](https://github.com/Amdkn/Aspace_OS-V4/blob/main/life/holons/README.md) · [SOH-143](https://linear.app/aspace-os/issue/SOH-143). Conservation du Drive indiqué dans le README existant. `effect_status=NOT_CERTIFIED` tant que le receipt natif n'est pas relu.
