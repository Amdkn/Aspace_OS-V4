# V4 : nouvelle architecture, acquis sélectionnés

Décision utilisateur du 5 octobre 2026. Remplace les interprétations « V3 reste la
cible » et « V4 est la prochaine version de V3 ». V2 renseigne l'histoire ; V3
fournit des actifs et des expériences ; V4 possède ses propres contrats.

## L0, L1, L2 : conserver la profondeur

Le même fondamental BedRock L0 soutient Life OS L1 et ses huit domaines. Cette
continuité conceptuelle ne signifie pas importer le runtime ou les restrictions
de V3. Graham maintient la mémoire partagée ; un classement de mémoire
ne doit pas être confondu avec un rang d'agent S1/S2/S3 ou B1/B2/B3.

| LD | Domaine | Reprise de référence V3 | Résultat attendu dans V4 |
|---|---|---|---|
| LD01 | Carrière et Business | Business / Book | Développement professionnel et Business OS |
| LD02 | Finance | Finance / Saru | Visibilité et pilotage financier |
| LD03 | Santé | Health / Culber | Continuité de la santé et récupération |
| LD04 | Cognition | Cognition / Tilly | Apprentissage et développement cognitif |
| LD05 | Social | Social / Stamets | Relations et participation sociale |
| LD06 | Famille | Family / Burnham | Engagements et liens familiaux |
| LD07 | Créativité | Creativity / Reno | Création et expression |
| LD08 | Impact | Impact / Georgiou | Contribution et trajectoire Solarpunk |

Noms de domaines vérifiés dans `20_Life_OS/22_Wheel_Discovery` de V3. Les intitulés
de résultats sont une proposition d'implémentation, pas une mesure de vie actuelle.
Chaque LD porte ses objectifs, projets, responsabilités, ressources, observations
et cycles de développement. Business OS est le développement de LD01 ; les sept
autres LD ont une existence autonome. Les méthodes d'exécution sont réutilisables
sans transformer chaque domaine en activité commerciale.

Les six frameworks Ikigai, Wheel, 12WY/Curie, PARA, GTD et DEAL traversent les LD.
Équilibre ne signifie pas allocation identique : rendre visibles engagement,
attention, besoins et évolution pour les huit domaines, sans inventer des seuils.
Une victoire de la Factory ne prouve pas une amélioration de LD03 ou LD06.

## Doctors, Compagnons, Apps et harness

Le 11e Doctor porte Life Core : Amy (interfaces), Rory (persistance), River
(flux et intégration) rendent les surfaces et les frameworks utilisables.
Ryan, Yaz, Graham restent indispensables à fabrication, observabilité et mémoire,
mais leur quickstart ne doit pas devenir un prérequis infini à toute vie utile.
Bill commence par WATCH, capacité perceptive transversale aux huit LD.

Les Doctors possèdent le cycle des branches : création de mission, allocation de
worktree, intégration, checkpoint, clôture et génération quotidienne. Un harness
est un moyen d'exécution interchangeable, pas l'identité du Doctor. Les autorités
Gateway/Sandbox, A0, S1, S2, S3 sont orthogonales aux trois Doctors.

Proposition de références : `spaces/{gateway,a0,s1,s2,s3}` et
`runs/<app>/<doctor>/<jour>/<mission>/<cellule>`. Les relations parent/enfant et
return_to sont explicites dans le registre de mission ; les slashs Git ne créent
pas une hiérarchie d'autorité. Les permissions GitHub App sont au niveau dépôt :
préfixes seuls insuffisants ; rulesets et médiation d'accès restent à déployer.

Les branches sont renouvelables, les identités et connaissances sont durables.
Au changement de journée : réconcilier PR/commits/checkpoints/sessions, retirer le
travail intégré, sauvegarder et vérifier le travail unique, puis renouveler les
espaces. Une mission active garde son identité. Un échec de sauvegarde suspend
le reset concerné. Aucun reset ni ordonnanceur destructif n'est livré ici.

## Réseau de Discussions, inspiré de Moltbook

Les agents ont des identités, des contributions sourcées, des échanges entre pairs
et des retours d'expérience. La popularité d'un post ne lui donne aucun droit de
mutation. Pas de publication automatique de messages de remplissage ; déclencher
sur une découverte, une question réelle, une décision ou une preuve nouvelle.

| Catégorie / slug | Usage |
|---|---|
| Agora / agora | Intentions, exploration et composition sans dette d'Issues |
| Observatoire / observatoire | WATCH, découvertes de Bill et signaux sourcés |
| Life Core / life-core | Équilibre des huit LD et expériences Amy/Rory/River |
| Atelier / atelier | Collaborations de mission et demandes de capacité |
| Decisions / decisions | Arbitrages, alternatives, raisons et supersession |
| Memoire / memoire | Synthèses de Graham, contradictions et leçons réutilisables |
| Preuves / preuves | Démonstrations, résultats, incidents et réparation |

Le format porte : auteur institutionnel, mission/LD concernés, sources, statut de
preuve, RACI et retour attendu. Pour une exploration sans décision, RACI peut
indiquer « sans objet » ; un responsable de décision reste unique lorsque A est
nécessaire. RACI accompagne l'autonomie et n'exige pas une approbation à chaque geste.

| Travail | R — réalise | A — répond du résultat | C — consulté | I — informé |
|---|---|---|---|---|
| Observation WATCH | Bill | Doctor de la mission | Graham, expert du LD | Participants abonnés |
| Usage Life Core | Amy/Rory/River selon effet | 11e Doctor | Responsables des LD concernés | A0 via résultat utile |
| Compilation mémoire | Graham | Doctor du périmètre | Auteur et personnes concernées | Consommateurs concernés |
| Branches et intégration | Doctor ou délégataire | Doctor de la mission | Clara, auteurs en conflit | Participants de mission |
| Évolution des fondamentaux | Architecte mandaté | A0 | Doctors et responsables des LD | Communauté concernée |

Les catégories ne correspondent pas une à une à des tâches. Une Discussion peut
aboutir à une expérience, un Project, un Milestone, une Issue ou rien. Une Issue
exécutable peut produire une PR, une Action et une Release. Le Wiki conserve les
connaissances réutilisables ; les surfaces Desktop/Mobile/3D présentent les mêmes
identités et états avec des interactions adaptées.

État vérifié dans l'interface GitHub le 5 octobre 2026 : Discussions activé ;
les sept catégories ci-dessus créées, en format conversation ouverte. Les slugs
correspondent aux sept formulaires de cette PR. Les catégories natives GitHub
sont conservées. Les formulaires RACI nécessitent encore leur fusion sur main.

Le Wiki natif est désactivé et son contrôle est indisponible : GitHub demande
une mise à niveau ou un dépôt public. Aucun abonnement ni changement de visibilité
n'a été effectué. La mémoire versionnée 40_Memory reste indépendante de ce blocage.

## Mémoire cumulative et perception

Capture GTD → source immuable → observation WATCH → compilation sourcée →
liens/conflits → connaissance Graham → restitution adaptée au domaine → résultat
→ nouvelle preuve. Une capture peut rester une référence sans engendrer une Issue.

Reprendre le principe `40_Memory` de V3, ses connaissances pertinentes et leur
provenance. Ne pas copier en bloc les anciens journaux d'exécution comme des
instructions V4. Les deux sont consultables, avec leur date et leur statut.

- LLM Wiki : raw, wiki et schéma d'entretien ; maintenir les contradictions.
- OpenWiki : moteur de documentation et recherche, avec espaces inter-dépôts.
  Le mode agent intégré documente le code ; le mode personal traite d'autres
  sources. Il ne suffit pas d'installer le mode code pour couvrir toute la vie.
- DOX : instructions et index locaux, pas une nouvelle base de faits ni une
  frontière de sécurité. Une règle écrite ne remplace pas son mécanisme effectif.
- Wiki GitHub : projection lisible de connaissances publiables. Le brut privé,
  les états d'exécution et les secrets conservent leur stockage adapté.

## Surfaces et acquis : aucun effacement de périmètre

Agent OS, Life OS, Business OS, Mobile OS, les 75 services déclarés de The OMK
Office JaaS, Cube Farm, Starnet et WorkAdventure sont au registre de reprise.
Pour chaque actif : source/version, contrat, domaine servi, données et permissions,
surface, adaptation nécessaire, preuve d'exécution. « Mentionné » ne signifie ni
déployé ni abandonné. `capabilities.json` conserve les éléments encore à qualifier.

Gateway/OpenClaw et surfaces Hermes, Prime Agent, DeepSeek Harness, Automaton
M0/M1/M2, Constructeur Universel, BMAD, gstack et CEO Bench restent dans ce
périmètre. Leur répartition finale doit répondre à des usages Life/Business
observables, pas à la seule multiplication des composants.

## Génération de modèles et défense

L'objectif inspiré de Gemini/Astra/Mythos est l'autonomie prolongée avec mémoire,
organisation et capacité de réparation. V4 choisit un provider par capacité,
disponibilité, qualité mesurée, coût et contraintes de données. Aucun modèle
annoncé ou restreint n'est une dépendance obligatoire du démarrage.

Glasswing inspire une boucle défensive sur les actifs autorisés : découverte,
reproduction isolée, correction, test de régression, revue indépendante et preuve
de déploiement. Ce n'est pas une autorisation de sonder des tiers. Les annonces
de performances ne sont pas des résultats obtenus par V4.

## Sources

- Instructions utilisateur et cinq transcripts capturés dans `40_Memory/sources.json`.
- V3 : `40_Memory_Wiki_OKF/index.md` et `20_Life_OS/22_Wheel_Discovery/` au commit
  `ad5e68e2867854ad952495cf1fcd37d76acbd33e` (source, pas dépendance runtime).
- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- https://github.com/langchain-ai/openwiki
- https://github.com/agent0ai/dox
- https://github.com/bradautomates/claude-video
- https://www.moltbook.com/
- https://www.anthropic.com/glasswing
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/

## Transfert sourcé

Voir `migration/README.md` et `life/registry.json` : corpus V3 conservé, huit LD,
six frameworks, journal temporel et revue Life exécutables. Les preuves de reprise
sont techniques ; elles ne déclarent pas des Doctors ou des connexions GWS actifs.
