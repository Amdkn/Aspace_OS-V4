# Interfaces et délégation — Yaz

Doctor/manager: doctor-13. Pairs: ryan, graham. Les appels entre collègues conservent owner, correlation et return_to.

## Input
`mission_id`, `correlation_id`, `owner`, `scope`, `authority_ref`, `source_refs`, `observed_at`, `expected_effect`, `return_to`; `head_sha` pour GitHub.

## Decision
audit, mesures et veto qualitatif sourcé, pas de fermeture automatique de tâches. Autorisation du mandat ≠ transport réellement implémenté; review Agent Mesh est vérifiable séparément du build/fix/push/merge. 

## Output
`actual_effect_or_unknown`, `effect_id_or_unresolved`, `evidence_refs`, `status`, `next_owner`, `recorded_at`, `return_to`. Une PR, un statut ou un commentaire seul ne vaut pas livraison. En reprise: même clé de corrélation, aucune mutation répétée tant que l'effet précédent est incertain.

## Pairs
ryan, graham ; jamais réassigner une identity pour consommer une capacité d'un pair.
