# Agents GitHub — incarnation et exécution

Le workflow **Aspace Agent Mesh** prend une PR interne non-draft, lui affecte un
holon et appelle un adaptateur connecté. Déclenchements : CI V4 terminée,
configuration modifiée, lancement manuel, réconciliation deux fois par heure.
Aucun appel modèle si la file est vide ou la mission déjà prise. Un nouveau
travail par run borne la consommation sans supprimer le périmètre.

Treize profils `.github/agents` : Rick ; Doctors 11/12/13 ; Amy/Rory/River ;
Bill/Clara/Nardole ; Ryan/Yaz/Graham. Sélectionnables par les surfaces GitHub
compatibles, lus directement par les trois adaptateurs. Le support natif dépend
aussi de l’activation du produit agent sur le compte.

| Runtime | Connexion | Exécution / preuve |
|---|---|---|
| Codex | Secret Actions OPENAI_API_KEY | Action OpenAI épinglée, CLI 0.160.1, résultat JSON validé |
| Jules | Secret Actions JULES_API_KEY + App Jules connectée à ce dépôt | Sources API, session, plan automatique du mandat, polling des activités |
| Hermes | Runner cloud éphémère labellisé aspace-hermes-ephemeral, CLI/provider configurés ; variable ASPACE_HERMES_EPHEMERAL_READY=true | hermes chat --oneshot --query-file --format stream-json ; résultat terminal |

Routage automatique : disponibilité Codex, Jules, Hermes. L’entrée provider
permet un choix explicite. Après dispatch ambigu, aucun fallback ne duplique
l’effet. Présence d’un secret ≠ connexion certifiée. Ne pas déclarer Hermes
READY avant l’enregistrement et la configuration effective du runner éphémère.

Actions → Aspace Agent Mesh → Run workflow : PR, agent, provider. Les statuts du
commit affichent CLAIMED, session, READY, CHANGES_REQUIRED, BLOCKED, UNKNOWN ou
STALE. Artifacts : mesh-mission, mesh-result, mesh-jules, mesh-receipt.
Après ajout d’une connexion, BLOCKED:unavailable reprend si la disponibilité a
changé. Après UNKNOWN/CLAIMED interrompu, vérifier la session externe et conserver
l’historique avant reprise ; pas de relance automatique d’un effet incertain.

La première automation est la revue réentrante, pas la Factory complète. Les
findings ne sont pas encore routés automatiquement vers une mission de réparation.
Pas d’auto-merge, pas de nouvelles autorisations pour les cinq Apps. Les profils
restent aptes aux missions de fabrication dans les harnesses. Gateway, promotion
et archivage externe restent des connexions distinctes.

## Sources

- https://docs.github.com/en/copilot/reference/custom-agents-configuration
- https://developers.openai.com/codex/github-action
- https://developers.openai.com/codex/noninteractive
- https://jules.google/docs/api/reference/sessions
- https://jules.google/docs/api/reference/activities
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands

Tests de contrat : tests/test_agent_mesh.py. Les transports simulés ne certifient
pas une session LLM réelle. Les artifacts de disponibilité donnent les blockers.

## Reprendre une session Jules ambiguë

Run workflow avec PR explicite, même agent, et `recover_jules_session=sessions/id`.
Le contrôleur vérifie que le prompt original contient le même mission_id et SHA
avant de réattacher et suivre la session. Il ne crée pas une nouvelle session.
