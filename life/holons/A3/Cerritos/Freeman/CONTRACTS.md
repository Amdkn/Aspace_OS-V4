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


## Résidence constitutionnelle V4 — life/holons/A3/Cerritos/Freeman
**Relation 1 — rattachement institutionnel.** Freeman est A3; manager [HoloDeck A2](https://github.com/Amdkn/Aspace_OS-V4/tree/main/life/holons/A2/HoloDeck). Chemin stable source `gtd/freeman` = alias historique, non seconde institution. Ce contrat appartient exclusivement à `life/holons/A3/Cerritos/Freeman`.

**Relation 2 — coopération de pairs.** Mariner, Boimler, Rutherford, Tendi. Les A3 conservent leur manager HoloDeck lorsqu'ils utilisent un engagement Curie ou consultent DEAL; coopération latérale et réentrante.

**Relation 3 — engagement transversal.** engager une action autorisée, preuve d'effet et retour, sans claim automatique. Même `mission_id/correlation_id` signifie vues distinctes : Curie (engagement de cycle), HoloDeck (action ou attente), DEAL (friction et charge nette). Les effets natifs restent chez leur propriétaire, jamais dans un deuxième WorkGraph. Une revue GTD peut réviser Curie; une suppression DEAL peut annuler une action avant son exécution.

**Références.** [Projet Linear GTD](https://linear.app/aspace-os/project/a2-holo-deck-cerritos-gtd-0521907c1942) · [Issue institution SOH-88](https://linear.app/aspace-os/issue/SOH-88) · [SOH-153 action Book](https://linear.app/aspace-os/issue/SOH-153) · [Index V4](https://github.com/Amdkn/Aspace_OS-V4/blob/main/life/holons/README.md). Drive existant préservé dans README. Statut sans preuve native : NOT_CERTIFIED.
