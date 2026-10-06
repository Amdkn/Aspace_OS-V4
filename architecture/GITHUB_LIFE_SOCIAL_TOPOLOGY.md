# GitHub V4 — trois Cores, six frameworks, huit domaines

Analyse et décisions du 6 octobre 2026. V3 est une source, V4 la destination. Analyse statique ciblée, pas certification des anciens runtimes.

## État vérifié
PR V4 #7, #8, #9, #10 et #11 fusionnées. #11 fusionnée à 8868ec9cb4c1bc8b6d3eaa66846c904de2ac5f94, sans conflit ; contrôle V4 réussi, revue automatique Rick indisponible. Les cinq branches de mission avaient exactement les têtes de leurs PR fusionnées : aucun nouveau commit de tête à intégrer. Elles peuvent être retirées après conservation de la provenance ; leur présence n'est pas un conflit.
Le Codespace a été observé en cours d'arrêt et n'a pas été redémarré.

## Diagnostic Tech OS V3
Les trois CORE.md sont générés par un même template ; ils organisent Kernel/Doctor13, Life/Doctor11, Buzz/Doctor12 et partagent les organes du kernel. Leurs interdictions absolues de lecture/écriture inter-couches contredisent le routeur Tech OS et shared_surface_fabric.json, qui autorisent explicitement la composition inter-Core par capacité. Reprendre les responsabilités et le mécanisme de génération, pas ces interdictions obsolètes.
mandat_docteur.py impose spec/build/spawn selon L0/L1/L2, choisit un pending par priorité/ancienneté et produit une commande Hermes. Ce fichier seul ne constitue ni routage agnostique ni sélection des dépendances ; le claim est délégué au travailleur. La règle « critère = commande avec rc » ne couvre pas les résultats humains Life OS. Son absence de candidat doit rester un état sans inference, pas un réveil périodique coûteux.
shared_surface_fabric.json distingue identité, surface, harness et capacité. GitHub, GWS, Supabase, Linear, Herdr et observabilité y sont partagés : les stewards répondent du service sans en interdire l'usage aux autres compagnons.
Les journaux D4 citent d'anciens schedulers et résultats locaux. Ils restent historiques, sans réactivation ni assimilation à des preuves V4.

## Analyse des six Issues CubeFarm initiales
Créées le 3 octobre sous la signature « A0 Amadeus, cubefarm CEO ». Cette signature prouve la provenance déclarée du texte, pas une autorité constitutionnelle. Les six décrivent une Factory TypeScript générique. Elles n'instancient ni Life Core, ni les frameworks, ni les huit LD.

| Issue | Acquis à conserver | Requalification V4 |
|---|---|---|
| #1 Scaffolding | Installation reproductible et CI | Remplacée par le socle Python/Node intégré ; ancienne prescription TS globale abandonnée, pas déclarée exécutée |
| #2 Authority | Identités, lease, fencing, budgets, return_to | Contrat inter-harness et cinq Apps, promotion temporaire/permanente ; aucune réécriture TS imposée |
| #3 WorkGraph | Reprise, traces et idempotence | Étudier les acquis V3 et Supabase ; mémoire/connaissances distinctes du journal d'exécution ; gérer UNKNOWN et réconciliation |
| #4 GitHub | PR, CI, intégrité de contenu | Adapter à la stratégie réelle de merge, pas imposer rebase ; merge distinct du déploiement et de la clôture du besoin |
| #5 Loop | Délégation, reprise et refill | Topologie réentrante, dépendances, interruption et budgets ; arrêter quand aucun travail éligible, jamais refill infini |
| #6 Canary | Preuve réelle et récupération | Scénario explicitement autorisé, environnement de test, résultat de vie hors LD01 ; pas mutation de production à chaque merge |

Les bodies historiques sont conservés dans chaque Issue après la directive de reprise. Les Issues #2–#6 restent du travail à réaliser, pas une flotte active.

## Axes indépendants
| Axe | Coordonnées |
|---|---|
| Responsabilité principale | Kernel / Doctor13 / Ryan-Yaz-Graham ; Life / Doctor11 / Amy-Rory-River ; Buzz / Doctor12 / Bill-Clara-Nardole |
| Bénéficiaires | LD01 Carrière-Business, LD02 Finance, LD03 Santé, LD04 Cognition, LD05 Social, LD06 Famille, LD07 Créativité, LD08 Impact |
| Méthodes composées | Ikigai, Wheel, Curie-12WY, PARA, GTD, DEAL |
| Nature de contribution | découverte, conception, fabrication, observation, mémoire, interface, persistance, flux, dispatch |
| Autorité | A0, S1, S2, S3 et enveloppe d'effet ; distinctes du provider |
| Exécution | harness/provider/compute, dépendances, budget, reprise |

Un item peut concerner plusieurs domaines et frameworks avec un seul responsable de résultat. Aucun produit cartésien de 3 × 6 × 8 Issues vides. Aucun domaine ne disparaît parce qu'aucune mission n'y est active.

## Projects : définition cible
Les Projects utilisateur V3 #8 Universal Constructor, #9 Foundation et #10 Agent OS sont des références du setup V3 #569, pas une preuve d'inventaire actuel. Ne pas copier leurs tâches aveuglément ni créer des doublons avant réconciliation de leurs IDs.

Un portefeuille V4 « A’Space — Directory & compositions » rassemble les dépôts, possibilités et missions. Trois vues de responsabilité Kernel/Life/Buzz, une vue huit LD, une vue frameworks et une vue dépendances exposent les mêmes items. Les projets métier autonomes peuvent garder leur propre Project relié au portefeuille.
Champs : Core responsable, Doctor, capacité/compagnon responsable, bénéficiaires LD (multi-valeurs via labels ou relation), frameworks (idem), maturité, statut, source V3, dépôt de réalisation, milestone, effet attendu, preuve, return_to. Les champs GitHub mono-sélection ne doivent pas transformer les relations multiples en choix exclusifs.
Le statut d'une Issue décrit son exécution ; la maturité d'une capacité et l'état de son résultat de vie sont distincts. Un item exploratoire peut rester un brouillon Project lié à une Discussion.

## Milestones : définition cible, non créées par ce document
| Convergence | Responsable | Critère de sortie |
|---|---|---|
| Instance V4 portable et harness utilisable | Doctor13 | Une mission réelle exécutée, checkpoint et reprise vérifiés sur compute autorisé |
| Life Core : revue des huit LD et premier effet | Doctor11 | Huit domaines examinés, arbitrages conservés, résultat utilisable hors LD01 |
| Buzz : découverte jusqu'à un usage | Doctor12 | Source Bill, alternatives Clara, dispatch Nardole, réalisation et retour au bénéficiaire |
| Continuite inter-Core | Doctor de la mission | Changement de harness et interruption sans perte de mission ni double effet |

Ces convergences peuvent avancer simultanément. Pas de date inventée. Un cycle Curie peut référencer plusieurs milestones ; toute tactique n'est pas un projet PARA.

## Discussions : réseau social de travail
Kernel Core, Life Core et Buzz Core portent les communautés de responsabilité. Frameworks porte les compositions des six méthodes dans les huit LD. Agora accueille intentions et alternatives ; Observatoire les sources ; Atelier les collaborations ; Decisions les arbitrages ; Memoire les connaissances ; Preuves les démonstrations et reprises.
Ne pas créer huit copies du même débat : une conversation a un lieu principal et des coordonnées LD/frameworks/Core, avec liens vers les autres. RACI : R réalise, A répond de la décision, C contribue, I suit ; dans l'exploration A peut rester sans objet. Les auteurs institutionnels sont explicités sans prétendre que leur compte GitHub est un autre utilisateur.
Une contribution indique source, objet, périmètre, hypothèse/observation/décision, retour attendu. Les réponses apportent contradiction, expérience ou composition. Les réactions ne confèrent aucun droit d'exécution. Les faits privés de santé/famille restent dans leur stockage approprié, seuls les éléments nécessaires sont projetés.
Une découverte n'engendre une Issue que lorsqu'un effet ou un obstacle concret existe. La synthèse retourne à la Discussion et à la mémoire. Pas de bots qui publient du remplissage pour simuler une communauté vivante.

## Définition d'une Issue V4
Intention et résultat entier ; cellule réalisable ou obstacle nommé ; Core/Doctor responsable et collaborateurs ; LD bénéficiaires ; frameworks pertinents ; sources existantes à réutiliser ; effets autorisés ; dépendances ; critères d'usage et preuves adaptées ; reprise FAILED/UNKNOWN et return_to. Une cellule bornée ne réduit pas la portée de l'intention parente. Les labels swarm:* historiques sont retirés des cellules requalifiées pour ne pas fournir une consigne de dispatch obsolète ; ceci ne prouve pas l'arrêt d'une session déjà engagée.

## Sources consultées
V3 : 10_Tech_OS/AGENTS.md ; les trois CORE.md ; kernel/shared_surface_fabric.json ; kernel/mandat_docteur.py ; .github/ISSUE_TEMPLATE/executable-cell.yml et gateway-cell.yml ; docs/governance/ASPACE_GITHUB_V4_CONTROL_PLANE_SETUP.md au SHA e332181fcaca2e26db60d1af4f5c60d3e061faae (PR #569 encore ouverte).
Issues/PR ouvertes V3 observées : #542–#546 Gateway, #555 Apps, #562 Jules, #567 Automaton, #568/#569 documentation, #484 réflexes, #485 recovery, #318 incarnation, #207 et #222 recherche, #570 vérification Kernel. Les milestones associés sont des observations des métadonnées d'Issues ; l'inventaire des Projects et milestones n'est pas déclaré exhaustif.
V4 : Issues #1–#6 intégralement, PR #7–#11 et branches, AGENTS.md, agents/CONTRACT.md, REFONDATION et analyse du transfert. Catégories de Discussions inspectées dans GitHub. Aucun merge ni mutation sur V3.
