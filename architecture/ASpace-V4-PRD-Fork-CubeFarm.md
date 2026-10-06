# A’Space V4 — PRD de fondation du fork CubeFarm

Version de travail 0.1 — 6 octobre 2026. Proposition de vision et exigences produit, pas déclaration de déploiement. Aucun changement de dépôt, de permission ou de runtime effectué pour produire ce PRD.

## 1. Promesse produit

Depuis un seul environnement cloud V4, le Capitaine doit pouvoir formuler une intention, explorer plusieurs architectures, engager les capacités appropriées et retrouver un résultat utilisable dans sa vie. Il ne doit plus reconstruire le contexte entre conversations, assurer les relais entre agents, ou attendre que toute l’infrastructure soit achevée pour utiliser Life OS.

Le fork CubeFarm devient une surface vivante d’A’Space : représentation, interaction et supervision des missions. Le Gateway porte l’exécution inter-harness ; les connaissances et états restent exportables indépendamment de cette surface. Les interfaces Agent OS, Life OS, Business OS, Mobile OS, Starnet et WorkAdventure appartiennent au même périmètre de composition.

La mesure directrice est le temps humain effectivement libéré avec des résultats utiles et une continuité vérifiée. Nombre d’agents, tokens consommés, tickets et animations ne sont pas des résultats de vie.

## 2. Diagnostic fondé sur les sources

Lecture du 6 octobre : AGENTS.md et architecture/REFONDATION.md de V4 reconnaissent explicitement les huit LD, les six frameworks et le Life Core du Doctor 11. Le problème ne se résume donc pas à leur omission textuelle. agents/registry.json contient surtout des responsabilités résumées ; son automatic_task est review et max_new_missions_per_run vaut 1. Ces paramètres décrivent la boucle GitHub actuelle, pas une limite constitutionnelle souhaitable de tout A’Space.

L’écart est entre la richesse annoncée et les missions que le système sait réellement prendre en charge. Un nom de compagnon, une responsabilité en une phrase et une liste de providers ne constituent pas un mandat opérationnel.

La contribution Gemini décrit des holons fonctionnels pour Curie, une articulation macro/méso/micro et des développements propres à chaque domaine. Ses références narratives, commandes et contraintes techniques restent des propositions à qualifier. Les tables aspace.* proposées ne sont pas considérées déployées. Le présent PRD ne prétend pas avoir relu intégralement V3 ni ses variantes de Codex Web.

## 3. Étendue du Life Core

| Domaine | Développement autonome attendu | Exemple de résultat observable |
|---|---|---|
| LD01 Carrière / Business | Business OS, offres, opérations, huit fonctions métier de la proposition Gemini | Une offre livrée et son fonctionnement suivi |
| LD02 Finance | Engagements, visibilité, scénarios et arbitrages personnels | Une vue financière compréhensible et actualisable |
| LD03 Santé | Récupération, sommeil, habitudes et organisation personnelle | Des périodes de récupération effectivement protégées |
| LD04 Cognition | Apprentissage, corpus, pratique et transmission | Une compétence pratiquée avec retour utile |
| LD05 Social | Relations, participation, réciprocité et engagements | Un engagement relationnel suivi sans automatisation intrusive |
| LD06 Famille | Liens, responsabilités et organisation du foyer | Un engagement familial respecté |
| LD07 Créativité | Exploration, prototypes, expression et œuvres | Une création consultable ou utilisable |
| LD08 Impact | Contribution, communs et trajectoire Solarpunk | Un effet documenté pour ses bénéficiaires |

Les archétypes Book, Saru, Culber, Tilly, Stamets, Burnham, Reno et Georgiou conservent leur place de responsables de domaine. Ils ne sont ni des modèles imposés ni nécessairement huit processus permanents.

Life OS ne commercialise pas les sept domaines non-business. Les méthodes de développement peuvent circuler ; leur finalité reste propre au domaine. Équilibre ne signifie ni huit budgets égaux ni huit agents toujours réveillés. L’attention, les engagements, les tensions et les domaines délaissés doivent être visibles et arbitrables.

LD06 Famille dans V4 et ld06_habitat observé dans Supabase restent deux significations à réconcilier. Ne pas les fusionner sur une simple ressemblance. Le rattachement IT/Infra dans le Business OS de Gemini décrit une fonction métier ; il ne doit pas rendre Bedrock L0 dépendant de LD01.

## 4. Frameworks composables

Ikigai éclaire le sens ; Wheel rend les domaines visibles ; Curie/12WY cadence les engagements choisis ; PARA organise projets et responsabilités ; GTD traite les entrées ; DEAL aide à éliminer, déléguer et libérer du temps. Ils partagent des objets et se renvoient des observations, sans imposer une chaîne obligatoire à chaque action.

Curie peut reprendre les cinq fonctions proposées : Pike/Vision, Una/Planning, M’Benga/Process Control, Chapel/Measurement et Uhura/Time Use. Leurs noms facilitent l’incarnation ; les fonctions doivent être exécutables et indépendantes d’un provider.

Corrections proposées au texte Gemini :

- Un projet peut dépasser un cycle 12WY ; chaque cycle porte alors une contribution explicite au projet.
- Une tactique n’est pas automatiquement un projet PARA.
- Le score d’exécution informe la revue ; il ne certifie pas à lui seul la valeur d’un cycle ni l’équilibre humain.
- Une modification de cap doit être possible quand le contexte change, avec sa raison conservée.
- La preuve est adaptée à l’effet : un test et un commit pour du code, une confirmation humaine pour un engagement vécu. La cryptographie ne prouve pas la qualité d’une relation.
- Les blocs de concentration restent compatibles avec le travail cloud ; leur protection vise les interruptions, pas une coupure réseau universelle.
- Les fonctions Curie peuvent être instanciées par domaine sans multiplier mécaniquement les sessions et leurs coûts.

## 5. S1, S2, S3 : mandats complets

| Instance | Responsabilité produit | Compagnons et résultats |
|---|---|---|
| S1 Rick | Vérifier la cohérence, le risque, la qualité et la possibilité de reprise ; aider à résoudre les blocages | Revue adaptée à l’effet et chemin de résolution exploitable |
| S2 Doctor 11 | Rendre le Life Core utilisable dans les huit LD | Amy : interfaces ; Rory : persistance ; River : flux et intégration |
| S2 Doctor 12 | Étendre les capacités par recherche, conception et composition | Bill : découvertes ; Clara : architectures ; Nardole : dispatch et continuité |
| S2 Doctor 13 | Produire, observer et améliorer les réalisations | Ryan : Factory ; Yaz : observation et critique ; Graham : mémoire et contexte |

Le rattachement organise la responsabilité, pas un monopole de service : Graham sert aussi le Life Core, Amy la Factory et Bill tous les domaines. Nardole coordonne une topologie réentrante ; Bill → Clara → Nardole → Ryan n’est pas une cascade unique. Ryan peut expérimenter pendant que Clara compare ; Yaz peut rouvrir une hypothèse ; Graham restitue les acquis à tous.

Chaque mandat doit préciser : finalité, périmètre, engagements envers les autres, capacités accessibles, déclencheurs, décisions autonomes, limites d’autorité, entrées/sorties, mémoire à consulter et à produire, critères de résultat, budget, reprise et return_to. Les fichiers AGENTS.md restent des index lisibles de ces contrats ; leur longueur n’est pas un indicateur de richesse.

L’identité S1/S2/S3, le rôle de domaine, le rôle B1/B2/B3, le framework et le moteur d’exécution sont des axes distincts. Un changement de modèle ne change pas la responsabilité. Les cinq GitHub Apps portent les autorités effectives d’accès ; elles ne remplacent pas ces mandats.

## 6. Expérience du véritable fork

1. **Life Core accessible dès l’entrée.** Huit domaines, engagements, tensions et résultats, avec navigation vers les surfaces spécialisées.
2. **War Room.** Exploration des intentions, sources, capacités du Directory, alternatives et conséquences. Une idée peut rester une connaissance sans devenir une Issue.
3. **Atelier des missions.** Composition et réaffectation des capacités, dépendances visibles, travail parallèle lorsque pertinent, reprise à la dernière preuve.
4. **Factory.** Fabrication et intégration des logiciels, documents, expériences et automatisations nécessaires aux domaines.
5. **Mémoire et observatoire.** Sources, contradictions, décisions, état réel, coûts et effets consultables depuis l’objet concerné.

La 3D doit expliquer une situation et permettre une action. Un personnage en mouvement ne signifie pas qu’un modèle travaille. La surface distingue prêt, en exécution, en attente, interrompu, résultat produit et résultat vérifié. Un mode compact accessible expose les mêmes opérations sans rendre la 3D obligatoire.

Le fork doit extraire l’hypothèse « CEO = Claude » derrière un contrat d’orchestration interchangeable. La vue ne choisit pas implicitement le provider. Aucun nouveau nom A’Space affiché dans le lobby ne suffit à démontrer cette transformation.

## 7. Gateway, Codex, FreeLLMApi et enveloppe 1B

Topologie cible : surface A’Space → mission et autorité → Gateway/Nardole → adapter de harness → provider → résultat et receipt → mission d’origine. Les flux de mémoire et d’observation sont présents pendant l’exécution.

Codex dans le Codespace est un premier moteur. FreeLLMApi est une route candidate demandée par le Capitaine ; ce PRD ne présume ni son endpoint, ni ses garanties, ni sa compatibilité avec les versions actuelles. La connexion doit qualifier : protocole, streaming, outils, annulation, reprise, modèles, contexte accepté, quotas, données transmises et erreurs. Un simple ping n’est pas une preuve de compatibilité de harness.

« 1B tokens » reste une cible à caractériser : crédit/budget d’inférence, taille d’un corpus ou capacité de contexte sont trois choses différentes. Le système doit enregistrer la nature du droit réel, sa période, sa consommation et sa portabilité. Exporter une configuration ne transfère pas un abonnement ni les droits d’un provider.

Trois ensembles exportables sont requis :

- **Configuration déclarative** : versions, routes, modèles, adapters, capacités, règles de budget et références de secrets.
- **Continuité** : missions, relations, décisions, index des connaissances, checkpoints et provenance, avec filtres de confidentialité.
- **Accès** : procédure de réauthentification ou récupération depuis un coffre autorisé, séparée du paquet partageable.

La preuve de portabilité sera la reprise d’une mission sur un compute neuf sans reconstituer les instructions à la main. Le Codespace unique est le poste de contrôle ; il peut déléguer à des computes autorisés. Sa fermeture interrompt ses propres processus : les missions autonomes nécessitent un runtime durable distinct lorsqu’elles doivent continuer.

Les variantes Codex/ChatGPT Web mentionnées dans V3 doivent être inventoriées avec leurs sources avant toute décision de fork. Comparer d’abord extension d’interface, adapter de protocole et fork du moteur. Préserver les comportements utiles plutôt que dupliquer tous les composants par défaut.

## 8. Composition M0 / M1 / M2

Convention proposée pour ce PRD uniquement, à rapprocher des définitions exactes d’Automaton et du Constructeur Universel avant adoption. Ces modes sont par capacité et peuvent coexister ; ils ne réduisent pas l’ambition fonctionnelle à trois petits lots.

| Mode proposé | Transformation | Preuve attendue |
|---|---|---|
| M0 — fédérer | Rendre un acquis accessible avec son contexte et son identité | Un usage réel, des entrées/sorties connues et une provenance |
| M1 — composer | Connecter plusieurs capacités sous une mission et une continuité communes | Relais sans ressaisie, interruption/reprise, résultat exploitable |
| M2 — faire évoluer | Modifier une composition à partir de l’observation et d’expériences | Comparaison avec référence, amélioration mesurée, rollback possible |

BMAD, gstack, CEO Bench, Automaton, OpenClaw, Hermes, Prime Agent et DeepSeek Harness restent des candidats présents dans le périmètre historique. Leurs fonctions exactes et versions doivent être qualifiées avant attribution. Aucun nom de framework n’est assimilé à une capacité prouvée. Bill apporte les sources ; Clara compare contrats et redondances ; Ryan démontre ; Yaz mesure ; Graham conserve les alternatives écartées et leurs raisons.

## 9. Supabase et mémoire

Observation antérieure de cette session : Life OS actif, Agent OS Backend inactif. Ce PRD n’exécute aucune migration. Life OS contient déjà des tables des huit domaines et des six frameworks : elles entrent dans le design comme patrimoine à comprendre.

Rory définit les états structurés et les correspondances de domaine ; Graham définit connaissance, provenance et restitution ; River définit la circulation des événements. Git conserve code et décisions versionnées ; GitHub porte les primitives d’ingénierie ; Supabase peut porter les états relationnels et leur contrôle d’accès ; les médias volumineux ont un stockage adapté. Les fichiers temporaires du Codespace ne doivent pas devenir l’unique mémoire.

Avant d’adopter tape/work/claim/prediction/evidence : réconcilier les contrats V3, le schéma existant et les usages V4. Distinguer temps d’observation et d’enregistrement ; gérer idempotence, effets inconnus et reprise. Les connaissances de vie ne se réduisent pas aux logs de la Factory.

## 10. Dark Factory au service de la vie

La Factory sait fabriquer des résultats à partir de mandats suffisamment définis, proposer des corrections et revenir vers le bon interlocuteur quand le problème change. Elle réduit les interventions du Capitaine sans exiger une autorité illimitée.

Chaque délégation porte un objectif, un espace de modification, des moyens disponibles, un budget, un critère de sortie et une destination de retour. Les permissions permanentes et promotions temporaires suivent les effets autorisés. Si une capacité manque, Nardole expose le besoin exact et reprend la même mission après résolution.

Rick indisponible ne devient ni validation implicite ni abandon silencieux : conserver le checkpoint et orienter vers une voie de revue déjà autorisée, sinon rendre la décision humaine précise et minimale. Les activités indépendantes continuent lorsque leurs dépendances le permettent.

## 11. Scénarios d’acceptation du produit

| Scénario | Réussite observable |
|---|---|
| Préparer un cycle de vie | Les huit LD sont examinés ; les engagements retenus et les arbitrages sont visibles |
| Découverte de Bill | Une source sert une expérience dans le LD approprié, avec retour vers la découverte |
| Livraison de la Factory | Le résultat atteint une surface utile ; merge et tests seuls ne clôturent pas l’usage |
| Changement de harness | La mission reprend avec identité, contexte et état conservés, sans double effet |
| Fermeture du Codespace | Les checkpoints sont conservés ; la différence entre arrêté et délégué reste visible |
| Migration de compute | Configuration restaurée, accès reconnectés et mission reprise sans recopier le système manuellement |
| Indisponibilité d’un reviewer | Blocage précis, alternative autorisée ou décision humaine bornée, continuité conservée |
| Valeur non-business | Au moins un parcours complet sert un LD non commercial sans le transformer en pipeline de revenus |

Mesurer : interventions de coordination du Capitaine, ressaisies, temps jusqu’au résultat utile, reprises réussies, erreurs/doubles effets, coût par résultat et domaines laissés sans attention. Les objectifs chiffrés seront fixés à partir d’une mesure de départ, pas inventés dans le PRD.

## 12. Ordre de conception recommandé

Conserver d’abord cette vision et le patrimoine Gemini ; établir les mandats complets et les parcours de vie ; qualifier la configuration réelle à exporter et les variantes V3 ; concevoir les contrats du fork et du Gateway ; choisir une première composition démontrant simultanément Life Core, Factory, mémoire et reprise. Une expérience bornée prouve la fondation sans amputer les capacités restantes du registre.

Premier parcours proposé : préparer un cycle Curie en protégeant récupération et engagements personnels, pendant que la Factory livre une capacité utile choisie dans LD01 ou un autre domaine. Le Capitaine doit pouvoir voir où son attention est requise et où le système avance seul.

## Sources et limites

- Texte collé(4).txt fourni par le Capitaine : proposition Gemini, lue intégralement.
- Capture image(20261006-083939).png : montre le quota et le lobby ; ne prouve pas l’exécution d’un agent.
- https://github.com/Amdkn/Aspace_OS-V4/blob/main/AGENTS.md — lecture du 6 octobre 2026.
- https://github.com/Amdkn/Aspace_OS-V4/blob/main/agents/registry.json — même lecture.
- https://github.com/Amdkn/Aspace_OS-V4/blob/main/architecture/REFONDATION.md — même lecture.
- Diagnostics et inspections techniques antérieurs de cette conversation, distingués des nouveaux faits observés.

Non vérifiés dans ce travail : configuration FreeLLMApi réelle, signification contractuelle de 1B tokens, contenu complet des variantes Codex Web de V3, références narratives Gemini et capacités courantes des frameworks cités. Ils constituent des besoins de qualification ciblée, pas des faits inventés ni des exclusions du périmètre.
