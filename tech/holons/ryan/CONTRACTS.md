# Interfaces et délégation — Ryan

Doctor/manager: doctor-13. Pairs: yaz, graham. Les appels entre collègues conservent owner, correlation et return_to.

## Input
`mission_id`, `correlation_id`, `owner`, `scope`, `authority_ref`, `source_refs`, `observed_at`, `expected_effect`, `return_to`; `head_sha` pour GitHub.

## Decision
mutation code sous mandat et permission du repo, pas de merge implicite. Autorisation du mandat ≠ transport réellement implémenté; review Agent Mesh est vérifiable séparément du build/fix/push/merge. 

## Output
`actual_effect_or_unknown`, `effect_id_or_unresolved`, `evidence_refs`, `status`, `next_owner`, `recorded_at`, `return_to`. Une PR, un statut ou un commentaire seul ne vaut pas livraison. En reprise: même clé de corrélation, aucune mutation répétée tant que l'effet précédent est incertain.

## Pairs
yaz, graham ; jamais réassigner une identity pour consommer une capacité d'un pair.


## CROSS-OS-20261014 — coopération S3↔A3, non exclusive

A3 bénéficiaire, Jerry/DC/squad concernés: fabrique/répare une capacité bornée avec tests/receipts, rend le résultat observable au propriétaire du besoin.

S3 reste sous Doctor d'origine, indépendamment du domaine servi. Demande entrante: `intent_ref, life_a3_id, jerry_id_or_null, mission_id, correlation_id, need, acceptance_method, authority_ref, return_to`. Retour: `artifact_ref, observed_effect_or_unknown, evidence_refs, exception, next_owner, return_to`. Une permission pour chaque clic est inutile si le mandat/scopes couvrent l'effet; arbitrage requis sur dépassement réel d'autorité. [A3 relations](https://github.com/Amdkn/Aspace_OS-V4/blob/main/architecture/cross_os_collaboration.json).
