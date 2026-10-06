# Univers Life L2 et coordonnées fractales

Statut : principe d’imbrication demandé par le Capitaine le 6 octobre 2026 ; découpage détaillé des 64 domaines proposé à discussion. Ce document ne déclare aucun nouvel agent ou runtime exécuté.

## Vision commune aux holons

L0 est le BedRock Tech OS au service de la vie. Ses trois Cores sont Kernel (Doctor 13 : Ryan, Yaz, Graham), Life (Doctor 11 : Amy, Rory, River) et Buzz (Doctor 12 : Bill, Clara, Nardole), sous la gouvernance technique S1 Rick. La gestion des branches relève des Doctors. Ces responsabilités ne sont pas des frontières de cognition ou des silos exclusifs.

L1 est Life OS, ses huit domaines LD et ses six frameworks transversaux : Ikigai, Wheel, Curie/12WY, PARA, GTD, DEAL. Chaque LD porte son univers opérationnel L2 avec huit domaines propres. Business OS est celui de LD01 ; il n’est pas l’unique L2 et ses indicateurs ne remplacent pas les résultats des sept autres LD.

Les Cores et leurs compagnons rendent leurs capacités disponibles à tous les LD et L2. Une surface CubeFarm, un provider ou un harness ne définit ni un OS ni l’identité d’un holon. Une extension à 64 domaines ne commande pas de lancer 64 processus ni de recopier mécaniquement les rôles Business partout.

## M est une coordonnée locale, L une imbrication

Les fractales Tech OS M0/M1/M2 et Curie/12WY M0/M1/M2/M3 coexistent. Un numéro M sans framework, instance et parent ne permet aucune comparaison. Leur décalage d’imbrication ne constitue pas une incohérence. Ne pas convertir M0 en L0, M1 en L1 ou M2 en L2 ; ne pas tronquer M3 parce que Tech OS s’arrête à M2.

Décrire un contexte avec : `os_instance`, `parent_instance`, `layer`, `life_domain`, `framework`, `fractal_level`, `scope`, `source`. Exemple de forme : `{layer:L2, life_domain:LD03, framework:12WY, fractal_level:M1, parent_instance:<instance Life>, scope:<périmètre explicite>}`. Cet exemple ne ratifie pas une sémantique de M1.

L’échelle M doit conserver la définition de sa source. La convention « M0 fédérer / M1 composer / M2 évoluer » de la première proposition CubeFarm ne définit pas les fractales historiques et ne doit plus être utilisée comme équivalence universelle. L’autorité S1/S2/S3 et les rôles A/B restent des axes distincts.

## Proposition des huit univers L2

Chaque ligne propose huit domaines internes, identifiables LDxx.D01 à LDxx.D08 dans l’ordre indiqué. Ces identifiants sont locaux à leur parent : Finance d’entreprise (LD01) et Finance personnelle (LD02) ont des interfaces, sans être fusionnées.

| Parent L1 | Steward | Univers L2 proposé | Huit domaines internes proposés |
|---|---|---|---|
| LD01 Carrière & Business | Book | Business OS | Growth ; Sales ; Product ; Operations ; IT/Infra ; Finance ; People ; Legal |
| LD02 Finance | Saru | Finance personnelle OS | Revenus personnels ; Budget et dépenses ; Trésorerie et épargne ; Dettes et engagements ; Patrimoine et actifs ; Investissement ; Protection et fiscalité ; Transmission et liberté financière |
| LD03 Santé, sommeil & énergie | Culber | Santé & vitalité OS | Sommeil et récupération ; Nutrition et hydratation ; Mouvement et force ; Santé préventive et suivi ; Santé mentale et émotions ; Énergie et rythmes ; Environnement de santé ; Adaptation et autonomie |
| LD04 Cognition | Tilly | Cognition & apprentissage OS | Attention et concentration ; Apprentissage ; Mémoire et connaissance ; Raisonnement critique ; Métacognition ; Compétences et pratique ; Langages et expression ; Recherche et synthèse |
| LD05 Social | Stamets | Relations & communautés OS | Amitiés ; Réseaux et rencontres ; Communautés ; Communication et écoute ; Coopération et entraide ; Limites et résolution des conflits ; Hospitalité et activités partagées ; Réciprocité et continuité des liens |
| LD06 Famille | Burnham | Famille & foyer OS | Lien conjugal et intime ; Parentalité et éducation ; Liens intergénérationnels ; Habitat et foyer ; Organisation domestique ; Temps partagé et rituels ; Soin des proches ; Histoire et transmission familiale |
| LD07 Créativité | Reno | Création & exploration OS | Inspiration et curiosité ; Arts visuels et design ; Écriture et narration ; Musique et expression sonore ; Fabrication et prototypes ; Jeu et expérimentation ; Pratiques et projets créatifs ; Partage et patrimoine créatif |
| LD08 Impact | Georgiou | Contribution & impact OS | Écologie et régénération ; Solidarité et inclusion ; Engagement civique ; Communs et open source ; Éducation et transmission publique ; Coopératives et économie sociale ; Action territoriale ; Évaluation et pérennité de l’impact |

Les huit LD et leurs stewards proviennent de `life/registry.json`. LD01 reprend les huit familles Business évoquées dans le travail de conception ; les formulations des 56 domaines LD02–LD08 sont des propositions nouvelles à arbitrer, pas un héritage V3 prétendument ratifié. Les catégories doivent rester adaptables à la vie réelle du Capitaine.

## Composition des six frameworks

Chaque univers conserve : sens et horizons (Ikigai), équilibre avec les autres LD (Wheel), vision/planification/contrôle/mesure/temps (Curie/12WY), projets et responsabilités durables (PARA), capture et engagements (GTD), définition/élimination/automatisation/libération (DEAL). Ces frameworks se composent au niveau Life et dans les instances de domaine, sans duplication automatique de données ou d’engagements.

Un objectif de sommeil en LD03 peut mobiliser LD01 pour protéger le temps et LD06 pour organiser le foyer. L’objectif, son propriétaire et sa mesure restent liés ; une contribution transversale ne recrée pas trois objectifs concurrents. Le résultat recherché est de vie, pas nécessairement une livraison logicielle.

## Arbitrage et continuité

Discussion Life Core : préciser pour chaque univers les frontières, huit domaines, besoins, résultats et liens avec les autres univers. RACI de conception proposé : R = contribution Codex avec coordination Doctor 11 ; A = Capitaine pour le découpage de sa vie ; C = stewards des huit LD, trois Doctors, compagnons et responsables des six frameworks ; I = Rick et Directory. Ce RACI décrit la cible institutionnelle, pas des agents consultés ou actifs.

Une décision ratifiée alimente le registre et les profils ; une expérience exécutable devient une Issue liée si nécessaire. Garder la discussion comme lieu d’exploration, avec provenance et raisons des révisions. Ne pas ouvrir automatiquement 64 Issues.
