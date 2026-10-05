# A’Space — présentation du transfert intelligent V3 → V4

[Lecteur interactif](ASpace-V3-V4.html) · [Vidéo](ASpace-V3-V4.mp4) · [Analyse source](Analyse-transfert-V3-V4.md)

GitHub affiche le HTML comme code : l’ouvrir dans un navigateur depuis le compute
(Codespaces ou VPS), ou consulter la version jointe à la conversation ChatGPT.
Aucun hébergement public ni installation sur le PC personnel n’est requis.

Présentation silencieuse, 1600 × 1000, 24 fps, 90 secondes, six transformations.
Le format, le rythme et la direction graphique sont des choix de réalisation.
Public : Capitaine et collaborateurs connaissant A’Space. Pas de capture Figma.

## Sources factuelles
Analyse-transfert-V3-V4.md du 5 octobre 2026 (jointe) et livraison PR #8 :
https://github.com/Amdkn/Aspace_OS-V4/pull/8
Commit V4 : 69bca772e61185e67d446775288a6e288147f65e
Snapshot V3 : ad5e68e2867854ad952495cf1fcd37d76acbd33e
L’analyse jointe précède la livraison ; le film ajoute explicitement son état.
Les nombres de fichiers ne représentent pas un taux de fonctionnement.

## Réalisation et licences
Anidoodle : https://github.com/alexgreensh/anidoodle
SHA f649db6eb823562ae41608119beb53f04d9d7c05, Apache-2.0, Alex Greenshpun.
Blueprint Animation : https://github.com/moguzbulbul/blueprint-animation
SHA 29aa30b83db4632daf586420c52a251e7dac2d92, Oğuz, CC BY-NC 4.0.
Adaptation de phases()/tw()/lerp et de la chorégraphie en Canvas dans Anidoodle.
Le moteur animations_v3 de Claude Design n’est pas utilisé : absent du dépôt.
Usage non commercial pour cette présentation dérivée. Le dépôt Blueprint demande
une permission écrite de son auteur pour un usage commercial. Licences jointes.

## Reconstruction
Cloner Anidoodle au SHA ci-dessus. Exécuter son scaffold.mjs avec --film aspace
--size 1600x1000 --duration 90 --fps 24. Copier aspace.ts dans src/canvas-core et
page-aspace.ts dans src/hosts. Dans src/hosts/page.ts, retirer le bloc final à
partir de « // ---- the player: » en conservant la fermeture de mountFilm.
Cette modification remplace le lecteur de base par les contrôles de présentation.
Installer les dépendances esbuild et playwright-core, ainsi qu’un Chromium compatible.
node tools/build-page.mjs aspace
node tools/render.mjs aspace --out out/ASpace-V3-V4.mp4
Le HTML dist/aspace.html est autonome, sans téléchargement au moment de la lecture.
Le rendu testé utilise Chromium Headless Shell 134 / build 1161, fontes du compute.
Les pixels peuvent varier avec les fontes et la version Chromium d’un autre hôte.

## Storyboard et registre des affirmations
0–6 s : unité de transfert complète ; analyse, introduction et critères.
6–18 s : 9339 entrées, 1341 importées ; migration/v3-transfer.json et inventaire V4.
18–30 s : Life 3630 / archives 3249, 8 LD et 6 frameworks ; analyse + life/registry.json.
30–42 s : mémoire historique et journal durable ; aspace/journal.py, tests de continuité.
42–54 s : holons, Doctors, Apps ; architecture cible issue des sources utilisateur.
54–66 s : forge et preuves ; primitives existantes/cibles, intégration partielle.
66–78 s : portabilité ; canary isolé, pas de preuve entre deux VPS.
78–90 s : bilan livré / restant ; PR #8 et CI 37354690805.
Chaque phase utilise focus, scan blueprint, construction, révélation et temps de lecture.
La simplification visuelle est une matrice de six axes, pas la topologie 10D complète.

## Vérifications
Images clés rendues deux fois avec empreintes identiques ; contrôle 2x.
Lecteur testé hors réseau : lecture/pause, avant/après, chapitres et déterminisme.
Le film contient des pauses de lecture intentionnelles ; aucune certification
« dead air » Anidoodle n’est revendiquée. Pas de piste sonore.
