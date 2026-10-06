# Factory GitHub et workers isolés — intégration au fork A’Space V4

Date : 6 octobre 2026. Statut : conception sourcée et critères d’implémentation ; aucune Box créée, aucun compte connecté et aucun nouveau worker lancé.

## Source et portée de la lecture

Le Capitaine a fourni le transcript complet « I Built the Simplest Software Factory (You Can Copy It) » dans Texte collé(5).txt. Le dépôt retrouvé est leonvanzyl/skills, épinglé au commit 17ca992d8b32746d5112be068ee9f77dd5d965ef, chemin skills/factories/create-upstash-software-factory.

Lecture directe : references/architecture.md ; assets/template/src/run.mjs ; assets/template/src/agents.mjs ; assets/template/.github/workflows/factory.yml. Ce périmètre est une analyse ciblée, pas un audit exhaustif ni une installation du skill. Le transcript est une source de propositions, pas une autorisation d’importer ses credentials, commandes ou règles.

Source technique fournisseur : https://upstash.com/blog/software-factory-needs-a-sandbox-per-agent
Code épinglé : https://github.com/leonvanzyl/skills/tree/17ca992d8b32746d5112be068ee9f77dd5d965ef/skills/factories/create-upstash-software-factory

L’article décrit des containers isolés ; le transcript les appelle des VPS. Ne pas promettre une VM dédiée sur cette seule base. Tarifs, quotas gratuits, compatibilité des abonnements et performances relatives des modèles ne sont pas qualifiés ici.

## Ce que la découverte apporte

La boucle démontrée capte une Issue prête, choisit un worker, prépare son environnement, exécute un harness, vérifie le résultat, tente une réparation puis ouvre une PR. Les labels rendent le travail visible depuis GitHub. Des snapshots préparent les outils ; des jobFiles actualisent les instructions à chaque mission.

La Factory est le contrôleur de cette boucle, distinct du modèle qui code. C’est une concrétisation compatible avec Nardole et Ryan, sans remplacement de la gouvernance A’Space par un CEO imposé.

## Composition avec l’existant V4

| Élément | Raccordement proposé |
|---|---|
| Signal GitHub et événements des dépôts | Entrées du Gateway ; dépôt et acteur vérifiés puis mission identifiée |
| Dispatcher | Nardole sélectionne une capacité disponible sous le mandat du Doctor propriétaire |
| Worker isolé | Ryan exécute via un adapter Codex, Claude, Jules ou Hermes compatible |
| Snapshot | Recette portable versionnée, outils épinglés, sans credentials ni données de vie |
| jobFiles | Contexte frais : instructions V4, profil, coordonnées L/LD/framework/M, contraintes, preuves et return_to |
| Tests et retour de correction | Clara et Yaz participent à la qualité, avec vérification indépendante selon le mandat |
| PR produite | Entrée de l’Agent Mesh existant ; findings renvoyés vers la même mission de réparation |
| États et receipts | Rory pour la persistance, Graham pour contexte/provenance, Yaz pour observation |
| CubeFarm et interfaces | Amy affiche les mêmes missions ; River relie les surfaces aux événements |
| Promotion et intégration | Doctor propriétaire et Rick selon le mandat, puis vérification du résultat livré |

Le Codespace V4 reste unique comme poste de contrôle du Directory. Des workers distants sont des ressources de calcul, pas de nouveaux Codespaces ni de nouveaux OS. GitHub Actions peut recevoir les événements lorsque le Codespace est arrêté ; la continuité effective dépend d’un backend connecté et doit être démontrée.

Upstash est un candidat de backend derrière un contrat portable, au même titre qu’un autre compute compatible. Un snapshot propriétaire accélère le démarrage ; la recette versionnée permet la reconstruction ailleurs. Aucun nouveau dépôt de Factory autonome n’est nécessaire.

## Contrat de mission et d’exécution

Séparer trois identités : mission durable, tentative d’exécution, lease du worker. Un changement de SHA invalide la preuve de revue correspondante mais conserve le lien vers la mission parente.

La mission porte :
- mission_id, parent_mission_id, source_event_id, repository, issue, base_sha ;
- doctor_owner, holon, layer, life_domain, l2_domain, framework, fractal_level et source de cette échelle ;
- objectif, critères de résultat, effets autorisés, périmètre de fichiers et destination de retour ;
- budgets de temps/inférence/concurrence, contexte versionné et références de secrets ;
- attempt_id, worker_id, lease_id, fencing_token, session_id, head_sha et evidence_refs.

Contrat cible du backend : prepare(image, context), start(mission, lease), inspect(session), cancel(session), checkpoint(session), collect(session), release(lease). Chaque adapter annonce les opérations réellement disponibles ; une opération manquante produit un besoin de capacité précis, pas une fausse réussite.

États cibles : READY → CLAIMED → RUNNING → VERIFYING → REVIEW → INTEGRATING → DELIVERED. CHANGES_REQUIRED revient en réparation dans la même mission ; WAITING_CAPACITY attend une ressource ; BLOCKED nomme un obstacle ; UNKNOWN exige réconciliation ; CANCELLED conserve le checkpoint.

Une étiquette GitHub est une projection de l’état, pas un verrou transactionnel ni une preuve d’exécution. Les transitions durables exigent une mise à jour conditionnelle ; le fencing interdit à un worker périmé de publier après réattribution. Un timeout après dispatch n’autorise pas un second provider à recommencer aveuglément.

## Adaptations nécessaires du template

| Observation dans les fichiers lus | Adaptation A’Space |
|---|---|
| La boucle s’arrête à factory:review et demande une intervention pour reprendre | Relier à Agent Mesh, réparation et intégration selon les autorisations existantes ; jugement humain pour les décisions qui le nécessitent |
| Branche factory/issue-N poussée avec --force | Branche de tentative sous Doctor, SHA attendu, préservation des commits concurrents ; aucune réécriture aveugle |
| Claim documenté par labels, attente de quatre secondes puis relecture | Mécanisme d’exclusivité vérifiable avec lease/fencing et test de concurrence ; ne pas affirmer l’atomicité de cette heuristique |
| finally nettoie puis libère le worker ; annulation brutale peut empêcher ce chemin | Réconciliation externe de la session et de la lease ; ne pas libérer un worker encore actif |
| FACTORY_SECRETS_JSON reçoit toJSON(secrets) | Fournir les références et valeurs nécessaires au transport concerné, injectées à l’étape appropriée |
| Credentials écrits dans le filesystem de la Box | Accès du harness qualifié ; absence de secrets dans snapshots, artifacts et logs vérifiée ; chmod seul n’isole pas des processus du même utilisateur |
| La règle de prompt interdit .github/ et prétend primer sur les house rules | Appliquer les contrats V4 et l’autorité de la mission ; les restrictions d’écriture doivent être effectives, pas seulement demandées dans un prompt |
| Les attentes occupent le runner Actions durant le job | Mesurer minutes Actions et coût compute ; privilégier un retour asynchrone lorsque disponible |
| Choix Claude/Codex selon label | Choisir capacité, compatibilité, disponibilité et budget ; conserver une préférence explicite sans confondre provider et holon |

Ces observations sont des propriétés du template examiné ; elles ne prouvent pas une exploitation ni une défaillance observée chez son auteur.

Le transcript se contredit sur la suppression automatique des Boxes de test puis l’interdiction de suppression par les agents. L’article fournisseur montre une méthode delete(). Distinguer existence d’une API, politique du skill et autorité accordée à notre contrôleur ; ne pas importer une impossibilité technique imaginaire.

## Vie, fractales et non-réduction

La boucle logicielle est un service L0 pour les huit LD et leurs univers L2. Elle ne transforme pas les soixante-quatre domaines proposés en soixante-quatre files de tickets. Les six frameworks composent les objectifs de vie ; seule une contribution exécutable devient mission de fabrication.

Tech OS M0–M2 et Curie/12WY M0–M3 conservent leurs coordonnées locales. Les étapes signal/dispatch/build/review ne sont pas de nouvelles définitions de M. Ne pas renommer fédérer/composer/évoluer en M0/M1/M2.

Exemple de premier résultat : une vue de revue Curie couvrant LD01–LD08, montrant engagements choisis et tensions, produite par la Factory à partir du registre V4 avec données de démonstration. L’acceptation inclut son accès depuis la surface V4 ; une PR seule ne prouve pas que le Capitaine peut l’utiliser. Ce scénario sert Life Core sans exporter des données personnelles vers un worker de démonstration.

## Livraison dans les Issues existantes

| Issue V4 | Delta d’implémentation et preuve attendue |
|---|---|
| #2 Autorité | Lease et fencing pour réserver/publier ; deux workers concurrents ne publient pas le même effet |
| #3 Continuité | Mission/tentative/session et checkpoint ; arrêt après dispatch puis reprise sans doublon |
| #4 GitHub | Entrée Issue autorisée, état projeté, PR au SHA exact, vérification des contrôles et résultat intégré |
| #5 Factory | Ajouter le chemin fabrication et réparation au mesh ; queue vide = zéro appel modèle ; worker indisponible = attente bornée sans runner dormant indéfiniment |
| #6 Première mission utile | Démontrer le parcours Life proposé ou une contribution utile équivalente, puis reprise depuis un autre compute |

Les contrats de #2/#3 doivent être implémentés et prouvés pour une exécution réelle ; leurs interfaces peuvent être simulées pour avancer sur #4/#5 sans attendre un programme infrastructure complet. Les tests simulés ne certifient pas le transport provider.

Séquence de preuve :
1. Signal dupliqué → une mission logique et une seule tentative active.
2. Worker connecté → session réelle et sortie exploitable ; connexion absente → obstacle exact.
3. Résultat en échec → correction avec contexte conservé.
4. PR validée → intégration normale sous autorité existante, sans contourner les règles.
5. Surface accessible → résultat de vie inspectable avec provenance.
6. Arrêt/reprise → même mission ; worker périmé empêché de publier ; idle sans appel modèle.

## État de départ vérifié

agents/README.md et agents/CONTRACT.md décrivent une boucle de revue de PR, des adapters Codex/Jules/Hermes et une récupération Jules. Le routage automatique des findings vers réparation est explicitement absent. Cette lecture ne vérifie pas les connexions actives ou les secrets.

La prochaine implémentation est le raccordement fabrication/réparation, pas l’installation d’une deuxième Factory concurrente. L’activation d’Upstash dépend d’un compte et d’un accès effectifs, non établis par la vidéo ; aucun achat ni élargissement de permissions n’est effectué par cette note.
