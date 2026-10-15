# HoloDeck — Système GTD (A2, GTD Cerritos)

## Input contract
Required keys: mission_id, intent_ref, source_authority, observed_at, native_object_ref_or_unresolved, decision_scope, return_to.

Entrée: Entrées, attentes, projets PARA et engagements Curie.

## Decision contract
Assurer capture, clarification, organisation, revue, engagement sans seconde hiérarchie.

## Output contract
GTDDisposition: captured_ref, class, next_action, owner, evidence. Ajouter correlation_id, expected_effect, actual_effect_or_unknown, evidence_refs, recorded_at, status, next_owner, return_to.

## Cooperation
Mariner, Boimler, Rutherford, Tendi, Freeman, Morty, Picard. GTD ↔ Curie pour priorités, Picard pour projets, DEAL pour friction. Autorité et état restent chez le propriétaire natif; aucun système parallèle ne peut réinventer les ID.

## Exception
Tasks API non certifiée; ne pas fabriquer des tâches.


## Résidence constitutionnelle V4 — life/holons/A2/HoloDeck
**Relation 1 — rattachement institutionnel.** HoloDeck est A2; manager A0 Amadeus + A1 Beth/Morty (autorité humaine préservée). Chemin stable source `gtd/holodeck` = alias historique, non seconde institution. Ce contrat appartient exclusivement à `life/holons/A2/HoloDeck`.

**Relation 2 — coopération de pairs.** Mariner, Boimler, Rutherford, Tendi, Freeman. Les A3 conservent leur manager HoloDeck lorsqu'ils utilisent un engagement Curie ou consultent DEAL; coopération latérale et réentrante.

**Relation 3 — engagement transversal.** cohérence GTD des actions, attentes et projets; aligne demandes quotidiennes avec priorités Curie. Même `mission_id/correlation_id` signifie vues distinctes : Curie (engagement de cycle), HoloDeck (action ou attente), DEAL (friction et charge nette). Les effets natifs restent chez leur propriétaire, jamais dans un deuxième WorkGraph. Une revue GTD peut réviser Curie; une suppression DEAL peut annuler une action avant son exécution.

**Références.** [Projet Linear GTD](https://linear.app/aspace-os/project/a2-holo-deck-cerritos-gtd-0521907c1942) · [Issue institution SOH-65](https://linear.app/aspace-os/issue/SOH-65) · [SOH-153 action Book](https://linear.app/aspace-os/issue/SOH-153) · [Index V4](https://github.com/Amdkn/Aspace_OS-V4/blob/main/life/holons/README.md). Drive existant préservé dans README. Statut sans preuve native : NOT_CERTIFIED.
