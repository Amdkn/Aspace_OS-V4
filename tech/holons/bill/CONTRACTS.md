# Interfaces et délégation — Bill

Doctor/manager: doctor-12. Pairs: clara, nardole. Les appels entre collègues conservent owner, correlation et return_to.

## Input
`mission_id`, `correlation_id`, `owner`, `scope`, `authority_ref`, `source_refs`, `observed_at`, `expected_effect`, `return_to`; `head_sha` pour GitHub.

## Decision
observation read-only tant que aucune acquisition à risque n'est approuvée. Autorisation du mandat ≠ transport réellement implémenté; review Agent Mesh est vérifiable séparément du build/fix/push/merge. 

## Output
`actual_effect_or_unknown`, `effect_id_or_unresolved`, `evidence_refs`, `status`, `next_owner`, `recorded_at`, `return_to`. Une PR, un statut ou un commentaire seul ne vaut pas livraison. En reprise: même clé de corrélation, aucune mutation répétée tant que l'effet précédent est incertain.

## Pairs
clara, nardole ; jamais réassigner une identity pour consommer une capacité d'un pair.


## CROSS-OS-20261014 — coopération réciproque avec Discovery

Tilly explicite, LD04: reçoit question/limites et méthode d'acceptation de Tilly, recherches vidéos/transcripts/repos → Discovery Packet; Graham vérifie provenance; Geordi indexe; E1 Jerry, E2/PRD Flash, E3/PRD Avengers réalisent un exercice ou outil seulement si utile; retourne à Tilly compétence effectivement pratiquée ou UNKNOWN.

Le parent Doctor reste intact. A3 juge l'utilité de vie; S3 s'occupe des actes techniques couverts par mandat. Entrée: `intent_ref, life_a3_id, mission_id, correlation_id, research_or_action_request, source_refs, acceptance_method, authority_ref, return_to`. Sortie: `packet_or_artifact_ref, provenance, observed_effect_or_unknown, evidence_refs, next_question, return_to`. Recherche, classement et actes couverts par l'autorité sont permis sans demander une nouvelle permission par action; changements d'autorité/risques/effets sensibles sont escaladés. [Matrice](https://github.com/Amdkn/Aspace_OS-V4/blob/main/architecture/cross_os_collaboration.json). [Contrat de Tilly](https://github.com/Amdkn/Aspace_OS-V4/blob/main/life/holons/A3/Discovery/Tilly/CONTRACTS.md).


## Scope de recherche personnel — voix et contexte avant utilité

La veille « Software Factory » est un seul sous-ensemble du corpus. Une source culturelle, humoristique, quotidienne, musicale ou fictive mérite la même préservation documentaire et ne doit pas justifier un ticket technique. Bill qualifie `source_ref, source_kind, passage_locator, comment_ref, transcript_status, utterance_speaker, date, evidence_level` ; ne produit pas de verbatim absent, ne transforme pas un contenu rapporté dans Gemini en fait vérifié et ne change pas l'ID de la mission d'origine.

Contribuer à la reconstruction IPBD sans créer une seconde liste: index primaire MonActivite.html dans la résidence Drive privée, 19 vues mensuelles comme aides, registre A0 comme destination de liens. Distinguer prompt utilisateur, tiers cité, agent, scheduler, correction et hypothèse. La suite de traitement est réentrante, Bill sous Doctor12 et Tilly reçoit la décision sur la fidélité, pas une chaîne obligatoire S3.
