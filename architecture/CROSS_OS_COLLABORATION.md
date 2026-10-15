# Collaboration Tech × Life × Business — sources et contrat

La source primaire du 30 juin (Gemini échange #1615) contient huit *ancrages historiques* **distincts** des 8 fonctions modernes par Jerry et des contributions additionnelles Linear. Cet ancrage n'est pas une délégation exclusive de domaine. Source: https://gemini.google.com/app/85cbd978eb6302c1 ; archive: https://drive.google.com/file/d/14pMHAhr28KgAa3l-aFWsZv9yA-XT1q_B/view. La V3 #415 (https://github.com/Amdkn/Aspace_OS_V3/issues/415) demande une parité technique sans coloniser les résultats personnels avec des KPI métier.

## Matrice historique avec les contrats actuels

| A3 Life | Jerry permanent | Ancrage 30 juin | Contributions Oct 8 Linear | Statut |
|---|---|---|---|---|
| LD01 book | aspace:business:B1 | OPS Batman/Fantastic Four | Product, Sales | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |
| LD02 saru | aspace:business:C1 | FIN Wonder Woman/Thunderbolts | Finance | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |
| LD03 culber | aspace:business:D1 | LEG Aquaman/Eternals | aucune déclarée | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |
| LD04 tilly | aspace:business:E1 | PRD Flash/Avengers | IT, OPS | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |
| LD05 stamets | aspace:business:F1 | SAL JohnJones / Martian Manhunter/Illuminati | People, Growth | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |
| LD06 burnham | aspace:business:G1 | PPL Green Lantern/X-Men | aucune déclarée | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |
| LD07 reno | aspace:business:H1 | IT Cyborg/Kang Dynasty | Product | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |
| LD08 georgiou | aspace:business:I1 | GRO Superman/Guardians | Growth, Legal | HISTORICAL_ANCHOR; liens Oct=ADDITIONAL_CONTRIBUTION |

## Responsabilités réciproques

A3 choisit le but de vie, le contexte, les limites et l'acceptation; Jerry B1 entretient le standard de l'Area; manager DC B2 formule DoD; squad B3 effectue avec preuves et liberté tactique. Le S3 Tech, sous **son Doctor original**, propose une capacité transversale, exécute des effets techniques permis et renvoie evidence/observed_effect. Aucun échange ne change le parent du S3 ni ne délègue à la Tech le choix de santé, famille, finances ou relations. Les projets Summers Picard sont des *instances*, pas les Jerry Area.

Échange typé: `intent_ref, life_a3_id, jerry_id, manager_id, squad_id, tech_holon_id, mission_id, correlation_id, request, scope, authority_ref, expected_effect, acceptance_by_a3, source_refs, evidence_refs, observed_effect_or_unknown, return_to`. Idempotence et readback avant promotion; `source_research` n'est pas `demonstrated_skill` ni `real_world_effect`. S3 peut prospecter/collecter/lire/transformer dans son mandat; une demande nouvelle à A0 est réservée aux droits absents, effets sensibles ou irréversibles, dépenses non bornées ou changement constitutionnel — pas à chaque appel d'outil déjà autorisé.

## Ancrage Bill ↔ Tilly et Geordi

Entrée: question de cognition inscrite à [Tilly](../life/holons/A3/Discovery/Tilly/CONTRACTS.md) et acceptation LD04. Bill [S3](../tech/holons/bill/CONTRACTS.md) cherche/sélectionne sources (WATCH/last30days), extrait métadonnées, transcripts et preuves d'incertitude. Graham protège provenance et comparaison aux connaissances; Geordi maintient les références réutilisables; **E1 Jerry → E2/PRD Flash → E3/PRD Avengers** transforme une possibilité choisie par Tilly en exercice ou outil. Seul Tilly accepte l'utilité sur une pratique/apprentissage réellement observé. Clara/Ryan/River en appui si construction nécessaire et autorisée. Retour: `research_packet_ref, knowledge_question, source_refs, confidence, geordi_resource_ref_or_unknown, memory_delta_ref_or_unknown, E1/E2/E3 work_ref_or_unknown, observed_practice_or_unknown, next_question, return_to=Tilly`. **La boucle n'est pas un processus autonome attesté** tant que les receipts de mission ne sont pas vérifiés.

## Huit autres Compagnons

- aspace:tech:graham → Continuité de décisions, connaissances et provenance pour tous A3; avec Tilly relier Bill/Geordi et apprentissages sans décider du programme cognitif. [PROPOSED_FUNCTIONAL], supervisé par doctor-13
- aspace:tech:amy → A3 bénéficiaire définit usage et acceptation; Amy conçoit interface, teste l'accessibilité et retourne le résultat au même A3. [PROPOSED_NON_EXCLUSIVE], supervisé par doctor-11
- aspace:tech:rory → A3 responsable des engagements; Rory préserve Linear↔GWS↔WorkGraph et signale les divergences à l'owner. [PROPOSED_NON_EXCLUSIVE], supervisé par doctor-11
- aspace:tech:river → A3 responsable du processus; River intègre API/événements selon effet autorisé et readback. [PROPOSED_NON_EXCLUSIVE], supervisé par doctor-11
- aspace:tech:clara → A3 porteur du besoin et DC concernés; Clara spécifie options, contrats/tests, maintenabilité; renvoie au résultat humain. [PROPOSED_NON_EXCLUSIVE], supervisé par doctor-12
- aspace:tech:ryan → A3 bénéficiaire et DC/Marvel concernés; Ryan fabrique/répare puis remet effet vérifié à son owner. [PROPOSED_NON_EXCLUSIVE], supervisé par doctor-13
- aspace:tech:yaz → A3 définit critères d'utilité, limites de charge et de coût; Yaz mesure sans inventer de santé ou impact. [PROPOSED_NON_EXCLUSIVE], supervisé par doctor-13
- aspace:tech:nardole → A3 concernés par dépendances; Nardole coordonne claims/return_to sans A0 routeur et sans agir comme steward Life. [PROPOSED_NON_EXCLUSIVE], supervisé par doctor-12

## Burnham et incohérences reconnues

LD06 demeure Famille/Présence et conserve son ancrage People/X-Men d'origine. G1 Solarpunk Habitat est une Area de services/habitat **au profit de la famille**, pas le remplacement du domaine ni l'identité du foyer. LD03 conserve souveraineté santé même si LEG/Eternals historique est une fonction de consentement/protection. Les mentions Linear du 8 octobre ne remplacent pas l'historique. Les associations supplémentaires restent contributrices sauf décision explicite versionnée.


## Épreuve exécutable de décision inter-holons (2026-10-15)

Commande **sans effet externe** : `python tools/holon_route.py --cases`. Elle lit **ce même** `architecture/cross_os_collaboration.json` (8 ancrages LD et 9 collaborations S3), sans recopier les holons ni imposer six validations à chaque action.

- **Mission normale (SOH-148 / Bill–Tilly)** : Tilly garde le résultat LD04 et l'acceptation; E1 garde son standard, E2/PRD et E3/PRD leurs responsabilités propres; Bill reste chez Doctor 12. Sortie `OWNER_REVIEW_READY_NOT_EXECUTED`, jamais `DONE` et jamais un claim runtime fabriqué.
- **Désaccord** : valeurs/effet Life → Beth avec Tilly; standard de l'Area → Jerry E1; capacité traversant plusieurs Cores → conseil S2 des Doctors, Rick observe les défaillances communes; conflit de juridiction → Morty, A0 uniquement si constitution modifiée. La contestation n'efface pas le propriétaire du résultat.
- **Responsable LD04 absent** : `OWNER_UNAVAILABLE`, décision de continuité à Morty; Nardole peut organiser une reprise/lease autorisée mais Bill, E1 ou E2 ne s'auto-nomment pas A3. L'effet reste `UNKNOWN` et l'exécution en pause.
- **Autorité ou référence native absente** : `AUTHORITY_UNRESOLVED` ou `NATIVE_REF_UNRESOLVED`, sans effet. Un résultat de test CI démontre le routeur, pas la disponibilité réelle des personnes, des agents ou des outils.

Les tests `tests/test_holon_route.py` vérifient ces décisions, les 8 ancrages et l'immutabilité des relations de supervision. Le routeur est un **contrôle déterministe de cohérence de mission**, pas une nouvelle résidence institutionnelle, un workflow de production, ni un substitut aux DoD, consentements ou receipts de WorkGraph.


## Composition hyperalignée v2 (15 octobre 2026) — corrections sur les maisons existantes

**Lire cette section après le registre historique.** L'ancien exemple Bill–Tilly → E2/PRD et E3/PRD décrit le **point d'ancrage du 30 juin**, pas une affectation permanente ni une chaîne obligatoire. Pour une mission LD04 donnée, `business_function` peut être `PRD, IT, OPS, ...`, une des huit fonctions réellement enregistrées dans `business/holons/registry.json`, ou `null` tant que la fonction n'est pas déterminée. Les managers/squads proposés ne sont **jamais exécutés** par le routeur. Une sélection vaut `PROPOSED_NOT_DISPATCHED`.

Le registre `cross_os_collaboration.json` dispose désormais de six contributions A2: Orville/Ikigai, Zora/Discovery, Computer/PARA, Curie/12WY, HoloDeck/GTD, HoloJaneway/DEAL. Un même `mission_id` peut invoquer zéro, une ou plusieurs de leurs disciplines par `framework_contributions`, sans changer d'identité ni imposer six approbations. Le retour porte chaque A2 et ses A3. Computer/Picard/Spock/Geordi/Data sont des projections des résidences V3 et Drive existantes, intégrées sous `life/holons/A2` et `A3/Enterprise`, avec [l'institution Linear existante](https://linear.app/aspace-os/project/a2-computer-enterprise-para-76871e5f81e0).

Les neuf S3 sont appelés selon **capacité + mandat** (`requested_capability`), sous leur Doctor original. Le lien Bill↔Tilly est privilégié, pas exclusif ; Graham peut contribuer à LD06 sur la mémoire et Bill peut rechercher sur LD07 sans devenir le A3 du domaine. Les S3 conçoivent et entretiennent la capacité de Beth/Morty, mais seuls A1/A3 délibèrent du sens et acceptent la valeur Life.

**Démocratie ouverte** : chaque pair peut `proposer → objecter → demander réponse motivée → proposer révision → exercer recours`. Le propriétaire situé du périmètre doit répondre; le droit de contestation ne fournit pas l'autorité d'exécuter. Valeurs → Beth; standards → Jerry; juridiction → Morty; capacité monodomaine → Doctor responsable; conflit entre Cores → Conseil S2 réunissant Doctors concernés, Rick examine les défaillances systémiques. A0 traite seulement une exception de constitution/valeur non délégable, pas chaque absence ou appel routinier. L'absence cumulée de Tilly/Morty/Beth laisse `WAIT_NO_AUTHORIZED_SUCCESSOR`.

**Autorité séparée** : l'entrée de mission n'est jamais une permission. `authority_ref` doit pointer vers un grant structuré et corroboré par un registre de droits indépendant, avec issuer, statut non révoqué, native_ref, action, scope, date de début et expiration; ce contrôle est seulement `AUTHORITY_VERIFIED_FOR_ROUTE_ONLY`. Le code accepte un snapshot de test injecté, mais aucun service production d'autorité n'est branché aujourd'hui : **fail-closed, aucun exécuteur**, pas de WorkGraph claim fabriqué. Les effets sensibles exigent toujours permission native et readback. Test: `python tools/holon_route.py --cases`; `python -m unittest tests.test_holon_route -v`.

**Mesure orientée vie :** Billy/Graham/Geordi qualifient une capacité Factory pour le bénéfice Tilly; un résultat exploitable exige la décision E1/Area, l'expérimentation E2/E3 qui peut être une autre fonction que PRD, puis le retour d'efficacité réelle. Une PR verte ne clôt pas SOH-148, voir `architecture/CROSS_OS_COLLABORATION.md` et Linear. Aucun artefact privé des Takeout n'est recopié sur GitHub.
