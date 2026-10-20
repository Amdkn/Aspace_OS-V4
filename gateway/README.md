# Gateway V4 — frontal d'authentification

Capacité V4 native (plan D-N015, méthode H-04 : **extraction-composition**).
Le serveur compose trois briques qualifiées de Business OS — `garde.ts`
(auth), `agp.ts` (contrôle d'accès des routes), `adapt.ts` (forme Web vers
Node) — extraites avec provenance dans leurs en-têtes. Aucune
réimplémentation de la posture.

## Ce qu'il fait

- Écoute sur **127.0.0.1, port 4440** (voir `os/PORTS.md`) — rien d'autre.
- Proxe uniquement les routes nommées `/api/blackboard/*` vers le
  blackboard interne (127.0.0.1:4445, chemin préservé). Toute autre route
  est refusée, même avec un jeton valide (refus par défaut, brique AGP).
- `/health` ouvert, réponse limitée à `status` et `time` — aucune donnée
  métier.
- Log d'accès minimal (horodatage, méthode, route, statut). Aucun secret,
  aucun corps de requête.

## Modèle d'auth

- Jeton bearer, lu **uniquement** dans la variable d'environnement
  `GATEWAY_TOKEN` (voir `.env.example`). Jamais en repo, jamais en UI.
- Requis sur **toutes** les routes `/api/*`, dans tous les modes :
  fail-closed — si la variable est absente, le service refuse tout
  (503 muet) plutôt que de s'ouvrir.
- Comparaison en temps constant (empreintes SHA-256, `timingSafeEqual`).
- Refus 401 strictement identique pour jeton absent ou invalide : la
  réponse ne dit jamais ce qui manque ou ce qui cloche.
- Le jeton n'est **pas** transmis au blackboard : l'en-tête d'autorisation
  est retiré avant le proxy. Le blackboard est derrière le frontal.
- CORS restreint : origines explicites via `GATEWAY_CORS_ORIGINS`
  (séparées par des virgules). Aucune origine générique ; une origine non
  listée ne reçoit aucun en-tête CORS.

## Machine de confiance uniquement (W03-H04)

Le bind 127.0.0.1 fait du gateway un service de **machine de confiance**.
L'identité tenant (W03) n'est pas fermée (H-H04-3) : **toute exposition
au-delà de 127.0.0.1 est interdite** tant que cette fermeture n'est pas
verte. Le blackboard direct sur 127.0.0.1 reste possible pour le debug
local — documenté, pas contourné.

## Rotation du jeton

1. Générer un nouveau jeton (gestionnaire de secrets du poste).
2. Mettre à jour la variable d'environnement dans l'environnement
   d'exécution — jamais dans un fichier du repo.
3. Redémarrer le gateway. L'ancien jeton cesse de fonctionner dès le
   redémarrage (aucune période de grâce).
4. Rotation recommandée à chaque session sensible (risque R1 du plan :
   le jeton vit en clair dans l'environnement d'exécution).

## Lancer

Poser les variables d'environnement (voir `.env.example`), puis :

```sh
node server.ts
```

Node >= 22 (TypeScript natif), zéro dépendance. Le blackboard doit écouter
sur 127.0.0.1:4445 pour que le proxy réponde (sinon 502 explicite).
