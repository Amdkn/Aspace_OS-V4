# Chantier 1 — Qualification du corpus des principes transférables

**Mission :** Bill (holon DISCOVER) — qualification préalable, « Finalisation des Fondations Aspace ».
**Date :** 2026-10-17 ~02:20 EDT · **Statut :** CORPUS QUALIFIÉ — l'exécution attendra le salvage complet.
**Contraintes :** lecture seule partout (Drive inclus) ; chaque affirmation d'état = preuve (fichier + ligne, ou commande + sortie).

---

## 1 — État exact du salvage ChatGPT (`~/workspace/chatgpt-extraction/`)

| Lot | État vérifié | Preuve |
|---|---|---|
| A — Réparation Vague 3 | **TERMINÉ** | `MANIFESTE.md` § Vague 3 : fichiers 01 et 03 « complet (vérifié 2026-10-17 — Lot A…) » |
| B1 + B2-bis — Items manquants | **TERMINÉ** | `items-recuperes.md` : « Bilan cumulé des 16 items — FINAL (2026-10-17, recalculé sur le réel après B1 + B2-bis) » → 10/16 texte intégral, 0/16 localisés, 6/16 non récupérables |
| C — Vague 4 (11 conversations) | **EN COURS (partiel)** | `MANIFESTE.md` § Vague 4 : « Conversations 1–6 : en cours d'extraction » ; `vague-4/` = 5 fichiers : 07 non transcrit (conversation introuvable), 08 partiel (décalage titre/contenu), 09 partiel (décalage titre/contenu), 10 non transcrit (probablement supprimée), 11 non transcrit (pas une conversation, c'est un .md) |
| D — Registre 4 états | **En design** | Mission D-01 typée par Bill, transmise à Clara par S1 Rick (état réel : 82/10/0/6 = 98) |
| E — IPBD | **En design** | Mission E-01 typée par Bill, transmise à Clara par S1 Rick ; `ipbd-qualification-matiere.md` (159 lignes) : 33 transcriptions exploitables, 9 fortes, 80–140 entrées plausibles ; pas de dossier `ipbd/` (non exécuté) |

**Volumes constatés** (commande `du -sh`, 2026-10-17) : vague-1/ 24 fichiers (700 K), vague-2/ 2 (12 K), vague-3/ 5 (100 K), vague-4/ 5 (60 K). `elements-enregistres.md` : 98 items (référence honnête = bilan FINAL 82/10/0/6, **pas** les nombres périmés du PRD-D 82/1/3/12 ni du brief S1 82/1/3/6). `items-recuperes.md` : 1 682 lignes. `MANIFESTE.md` : 85 lignes.

---

## 2 — Takeout Gemini : localisation et qualification

**Le Takeout n'est PAS dans le workspace.** Localisation établie par recherche Drive (lecture seule) :

| Élément | Localisation | Preuve |
|---|---|---|
| « Gemini Takeout 11 Oct 2026 » | Drive, dossier id `1n9CEkreJhXTmo7wPa7SL7CmI1j_PCIIt`, déposé 2026-10-12 (export manuel du Capitaine) | `gws drive files list` q=`name contains 'takeout'`, 2026-10-17 |
| 20 fichiers mensuels | Même dossier : `Gemini_Historique_2025-04.md` → `Gemini_Historique_2026-10.md` (text/markdown prétraités), **~23 Mo** cumulés | listing dossier, 2026-10-17 |
| `INDEX_MENSUEL.md` | Même dossier (1 999 o) | idem |
| `RAPPORT_ANALYSE_TAKEOUT.md` | Même dossier (4 933 o) — analyse Antigravity/Gemini du 2026-10-12 | lu via `drive files get`, 2026-10-17 |
| `MonActivite.html` | Même dossier (28,5 Mo, 4 054 entrées d'activité) | idem |
| Zips bruts | **PC du Capitaine** `C:\Users\amado\Downloads\takeout-20261012T172532Z-*.zip` (1,05 Go compressé → **1,68 Go décompressé, 1 641 fichiers**) | RAPPORT_ANALYSE_TAKEOUT.md §1 |
| « Youtube Takeout » | Drive, dossier séparé id `1P0Sgc9XInyHGzb1uW6U9OgM8me19xwug` | recherche Drive, 2026-10-17 |

**Contenu brut** (d'après RAPPORT_ANALYSE_TAKEOUT.md §1) : 1 410 images (~950 Mo), 77 enregistrements vocaux .wav (~35 Mo — dictées de prompts du Capitaine), 11 vidéos .mp4 (~280 Mo — masterclasses, architecture), 3 .mp3, 47 specs .md (SDD-000 → SDD-009 : constitution Rick's-Verse, bootstrap agents, aspace-core, solarpunk-kernel, harness Rick, protocole TARDIS, gouvernance…), 34 PDF (livres/canons : *Sovereign Codex*, *Architect Codex*…), 10 code/SQLite, 36 dossiers légaux/administratifs, 11 archives code.

**État d'exploitation :** prétraité (mensuels .md + index + rapport d'analyse thématique) mais **non intégré au workspace** ; Drive = lecture seule pour A0 (décision Capitaine 2026-10-13) ; **médias non transcrits** (images, 77 .wav, 11 .mp4) ; zips bruts inaccessibles depuis la VM (PC du Capitaine).

---

## 3 — Complétude : ce qui manque pour un corpus complet

1. **Lot C — 6 conversations en cours** (Debug URLs 21 sept., Gestion IA multimodale 10 janv., Salutations en français, Weekly 12WY, Cadrage IKIGAI 5 déc. 2025, Avoir des OS sur Windows) + 2 partielles à qualifier (08, 09) + 3 non-transcrites documentées (07, 10, 11).
2. **Lots D et E — en design chez Clara**, non exécutés (registre 4 états + IPBD 80–140 entrées).
3. **Relais A0/B2 éventuel** — items 64–71 : si un relais ultérieur récupère un item, D et E se rouvrent (PRD-D §8, PRD-E §9).
4. **Takeout — médias non transcrits** (1 410 images, 77 .wav, 11 .mp4) : une partie des principes (dictées, masterclasses) est inaccessible sans pipeline de transcription ; zips bruts sur PC du Capitaine uniquement.
5. **Export natif ChatGPT (3e tentative)** — statut inconnu depuis le 2026-10-16 (en attente à l'époque) ; s'il arrive, il peut compléter/corriger (troncations vague-1, messages manquants).

---

## 4 — Structure cible du corpus de principes

Principe : **zéro duplication** — le salvage reste où il est, le Takeout reste en Drive (lecture seule) ; le corpus de principes **pointe**, il ne recopie pas.

```
~/workspace/fondations-aspace/
  BEFORE-YOU-BUILD.md                  ← cadre (existe)
  chantier-1-qualification-corpus.md   ← ce livrable
  corpus/                              ← MATIÈRE (pointers, lecture seule)
    chatgpt/                           → ~/workspace/chatgpt-extraction/ (ne pas déplacer)
      registre.md                      → elements-enregistres.md (4 états, réf. 82/10/0/6)
      recuperes.md                     → items-recuperes.md (bilan FINAL)
      ipbd/                            → sorties du lot E (à venir : README + <theme>.md)
    gemini/
      drive/                           → dossier « Gemini Takeout 11 Oct 2026 » (id Drive, lecture seule)
      mensuels-index.md                → INDEX_MENSUEL.md (miroir lecture seule si besoin traitement)
      analyse-takeout.md               → RAPPORT_ANALYSE_TAKEOUT.md
      brut-manifestes/                 ← inventaires des zips (PAS les zips : restent sur PC Capitaine)
  principes/                           ← PRODUIT (extraction, nouveau)
    REGISTRE-PRINCIPES.md              ← index : id, énoncé court, statut, sources
    <domaine>/
      PRINCIPE-XXX.md                  ← 1 fichier/principe : énoncé, statut, sources, traçabilité
  preuves/                             ← traçabilité principe→source (citations exactes + liens)
```

---

## 5 — Critères de « transférable » (vers V4.1)

Un principe est **TRANSFÉRABLE** si et seulement si :
- **T1 — Paternité :** formulé ou explicitement validé par le Capitaine (pas une proposition IA non reprise). Source : IPBD ou citation transcription.
- **T2 — Récurrence :** apparaît dans ≥ 2 contextes, ou survit à une reformulation/correction (non annulé).
- **T3 — Actionnabilité :** exprime une règle, une décision ou une contrainte applicable à V4.1 (pas une anecdote).
- **T4 — Non-contradiction :** aucune correction ultérieure du Capitaine ne l'annule (traçabilité bidirectionnelle IPBD : le dernier état fait foi).
- **T5 — Preuve d'application :** a guidé au moins une décision ou un artefact réel — sinon statut « À éprouver », jamais « Transférable » par défaut.

**Statuts :** `TRANSFÉRABLE` (T1–T5) · `ARCHIVE` (contexte historique, pas de transfert) · `À ÉPROUVER` (candidat, preuve manquante) · `ÉCARTÉ` (contradit — motif + source de la contradiction obligatoires).

---

## 6 — Méthode d'extraction (transcriptions + IPBD)

1. **Repérage** — balayer le corpus priorisé : les 9 conversations ChatGPT fortes d'abord (`ipbd-qualification-matiere.md` §1 : vague-1/01, 02, 18, 19, 20, 21, 22 + vague-3/01 + vague-4/09), puis les 7 moyennes, puis les mensuels Gemini via `INDEX_MENSUEL.md`. Marqueurs : I/P/B/D explicites + doux (« je vais », « je reprends », « il faut ») + directives impératives.
2. **Découpage** — 1 énoncé = 1 principe candidat (les directives impératives longues — 5 à 15 intentions implicites par message — se découpent, elles ne se collectent pas en bloc).
3. **Citation exacte** — les mots du Capitaine entre guillemets ; toute reformulation marquée « reformulation », jamais présentée comme citation.
4. **Attribution** — Capitaine vs IA vs tiers cité ; incertain → « attribution incertaine », jamais tranché silencieusement (cas : v4/08 conversation collée, traces d'autres sessions en v1/02 et v1/18).
5. **Déduplication inter-sources** — même principe en ChatGPT et en Gemini → **1** principe, 2+ sources (renforce T2, pas de doublon).
6. **Test de transférabilité** — appliquer T1–T5, attribuer le statut.
7. **Traçabilité** — chaque principe pointe ses sources exactes (fichier + message # + date + URL) ; `REGISTRE-PRINCIPES.md` comme index unique.
8. **Contre-vérification** — un second passage sur échantillon (≥ 10 %) avant validation du lot ; pas d'auto-validation aveugle.

**Garde-fous honnêteté :** pas d'invention ; en cas de doute → `ARCHIVE` ou `À ÉPROUVER`, jamais `TRANSFÉRABLE` par défaut ; les corrections ultérieures du Capitaine priment ; P quasi absent du corpus explicite (0 marqueur — cf. `ipbd-qualification-matiere.md`) → constater la rareté, ne pas forcer.

---

## 7 — Risques

| # | Risque | Mitigation |
|---|---|---|
| R1 | Lot C incomplet (6 conversations en cours) → corpus ChatGPT non clos | L'extraction démarre sur corpus partiel **scopé explicitement**, ou attend la fin du lot C — trancher avant (cf. mission E-01, R1) |
| R2 | Lots D/E en design → registre 4 états et IPBD non livrés | L'extraction des principes **dépend de l'IPBD** (E-01) : séquencer après, ou avancer sur les 9 conversations fortes en marquant « IPBD à confirmer » |
| R3 | Takeout en Drive lecture seule + brut sur PC du Capitaine | Définir le pipeline d'ingestion avec le Capitaine (miroir workspace ? fourniture des zips ?) — **c'est un arbitrage vision via A0**, pas une décision technique |
| R4 | Médias non transcrits (1 410 images, 77 .wav, 11 .mp4) | Pipeline de transcription dédié (lot séparé) ou exclusion scopée et documentée |
| R5 | Biais de source : ChatGPT dense en gouvernance/factory (sept–oct 2026), Takeout sur 19 mois | Échantillonnage stratifié par période ; ne pas sur-pondérer le récent |
| R6 | Export natif ChatGPT pendant | S'il arrive : compléter/corriger (troncations, messages manquants), puis re-jouer la déduplication (étape 5) |
| R7 | Relais A0/B2 ultérieur (items 64–71) | D et E se rouvrent (PRD-D §8, PRD-E §9) → le corpus de principes aussi, de façon tracée |

---

**Prochaine étape (chaîne lore) :** Clara designe l'extraction (plan borné + tests hold-out écrits avant exécution) sur la base de cette qualification ; Nardole dispatche ; les Doctors valident avant toute exécution.
