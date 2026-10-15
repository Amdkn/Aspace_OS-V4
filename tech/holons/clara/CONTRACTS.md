# Interfaces et délégation — Clara

Doctor/manager: doctor-12. Pairs: bill, nardole. Les appels entre collègues conservent owner, correlation et return_to.

## Input
`mission_id`, `correlation_id`, `owner`, `scope`, `authority_ref`, `source_refs`, `observed_at`, `expected_effect`, `return_to`; `head_sha` pour GitHub.

## Decision
développement sur branche isolée et PR selon mandat; pas d'autorisation automatique merge. Autorisation du mandat ≠ transport réellement implémenté; review Agent Mesh est vérifiable séparément du build/fix/push/merge. 

## Output
`actual_effect_or_unknown`, `effect_id_or_unresolved`, `evidence_refs`, `status`, `next_owner`, `recorded_at`, `return_to`. Une PR, un statut ou un commentaire seul ne vaut pas livraison. En reprise: même clé de corrélation, aucune mutation répétée tant que l'effet précédent est incertain.

## Pairs
bill, nardole ; jamais réassigner une identity pour consommer une capacité d'un pair.


## CROSS-OS-20261014 — coopération S3↔A3, non exclusive

A3 exprimant besoin + manager DC porteur du DoD: transforme en architecture, tests, sécurité, maintenabilité et passation au build; l'A3 conserve l'acceptation de vie.

S3 reste sous Doctor d'origine, indépendamment du domaine servi. Demande entrante: `intent_ref, life_a3_id, jerry_id_or_null, mission_id, correlation_id, need, acceptance_method, authority_ref, return_to`. Retour: `artifact_ref, observed_effect_or_unknown, evidence_refs, exception, next_owner, return_to`. Une permission pour chaque clic est inutile si le mandat/scopes couvrent l'effet; arbitrage requis sur dépassement réel d'autorité. [A3 relations](https://github.com/Amdkn/Aspace_OS-V4/blob/main/architecture/cross_os_collaboration.json).
