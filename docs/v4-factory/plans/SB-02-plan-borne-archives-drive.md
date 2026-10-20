# SB-02 — Plan borné : Lot 2 — archives → Drive PARA (~2,1 Go)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; inventaire Bill (`~/workspace/sandbox-extraction/inventaire-sandbox.md`)
**Contraintes inviolables :** Drive = PARA du Capitaine (lecture seule par défaut — **écriture = autorisation ponctuelle du Capitaine**, précédent : extraction ChatGPT 2026-10-16) ; manifeste SHA par lot ; **transcription des médias hors périmètre** (arbitrage A1 en attente) ; Takeout Gemini = mission suivante.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Contenu** : `video-tests/pieces/life-os-evolution/` (vrai projet : brief.md, LOG.md, piece.json, `src/`, `renders/` 190 Mo, `frames/` 1,6 Go) · `your_files/` (180 Mo : ~25 MP3 livrées, docs, `animate-history-of-ai-60s.mp4` 97 Mo) · `goals/.../life-os-v3-v4-60s.mp4` (79 Mo) · `watch-reports/` · `reports/` · `rapports/` · **complément chatgpt-extraction** (miroir Drive incomplet).
2. **Frames 1,6 Go — décision tranchée (déléguée par Rick)** : **exclues de l'archive** — régénérables depuis `src/` (rendu procédural). L'archive garde `src/` + `renders/` + docs + brief/LOG/piece.json ; la **commande de régénération** (extraite de LOG.md/`src/`) est consignée dans le manifeste du lot. Économie : 1,6 Go. Si la régénération s'avère impossible à l'exécution → repli documenté : archiver les frames (décision tracée, pas silencieuse).
3. **Gros fichiers (< 100 Mo) → Drive, jamais GitHub** : `final.mp4` / `final-1920x1080.mp4` (79 Mo ×2), `animate-history-of-ai-60s.mp4` (97 Mo), `life-os-v3-v4-60s.mp4` (79 Mo). Le seul fichier > 100 Mo de la sandbox (pack git 120 Mo) est une métadonnée — pas à extraire.
4. **Complément chatgpt-extraction — procédure SHA** : (a) uploader les 4 manquants (`elements-enregistres.md`, `ipbd-qualification-matiere.md`, `prd/`, `BEFORE-YOU-BUILD.md`) ; (b) **comparaison SHA** `items-recuperes.md` : SHA-256 local (89 Ko, 17 oct. 05:44) vs SHA-256 Drive (90 548 octets) + mtimes + diff de contenu. **Règle** : fait foi la version la plus récente **dont l'intégrité est vérifiée** (98 items attendus — compter) ; les deux SHAs et la décision sont consignés ; en cas d'ambiguïté → conserver les deux, marquer le miroir « à vérifier », **jamais d'écrasement aveugle**.
5. **Gate autorisation d'écriture Drive** : écriture ponctuelle autorisée par le Capitaine (précédent 2026-10-16) — **à escalader via A0 avec les 4 arbitrages** (nouveau point 5). Aucun upload avant.
6. **Quota et transfert** : vérifier l'espace Drive disponible avant transfert ; envois par batch avec manifeste par batch ; reprise sur échec (pas de re-upload aveugle — comparer SHA avant de réémettre).
7. **Arborescence Drive** : dossiers d'archive datés, pattern de l'extraction ChatGPT 2026-10-16 (dossier racine « Sandbox — Extraction 2026-10-17 » sous le PARA, sous-dossiers par lot).
8. **`user/media_library/` — hors lots (arbitrage Capitaine)** : reste dans Drive (5 To = son équivalent S3) — **reste où c'est**, non inclus dans les lots d'extraction. Le design ne le déplace ni ne le duplique.

## 1. Bornes

**IN :** archives §0.1 + manifeste SHA par lot/batch + décision frames + procédure SHA items-recuperes.md + gate autorisation Drive.
**OUT :** transcription des médias (arbitrage A1) ; Takeout Gemini (mission suivante) ; écriture Drive sans autorisation ponctuelle ; `user/`, `memory/`, runtime.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Arborescence Drive** : dossier racine daté + sous-dossiers par lot (pattern extraction 2026-10-16).
**Système 2 — Manifestes SHA par batch** : par fichier — chemin, SHA-256, octets ; vérification avant réémission.
**Système 3 — Procédure SHA items-recuperes.md** : double SHA + mtimes + diff + règle d'autorité §0.4, décision consignée.

**Flux :** P0 (gate autorisation + quota) → P1 (batches + manifestes) → P2 (complément chatgpt-extraction + SHA) → vérification.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Gate autorisation** | Autorisation ponctuelle d'écriture Drive (via A0) ; vérification quota Drive | H-SB02-5 |
| **P1 — Batches** | Upload par batch (pieces sans frames, your_files, vidéos, watch-reports, reports, rapports) + manifeste SHA par batch | H-SB02-1, H-SB02-2, H-SB02-4 |
| **P2 — Complément** | Upload des 4 manquants ; procédure SHA items-recuperes.md ; décision consignée | H-SB02-3 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-SB02-1 | Manifeste par batch | chaque fichier uploadé a une entrée (chemin, SHA-256, octets) ; échantillon re-téléchargé conforme |
| H-SB02-2 | Décision frames appliquée | l'archive contient `src/`+`renders/`+docs, **0 frame** ; commande de régénération consignée (ou repli tracé si impossible) |
| H-SB02-3 | Miroir complété | les 4 manquants présents en Drive ; items-recuperes.md : les deux SHAs + la décision d'autorité consignés |
| H-SB02-4 | Gros fichiers → Drive | aucun fichier > 25 Mo dans les lots GitHub (SB-01/SB-03) ; les 4 vidéos < 100 Mo en Drive |
| H-SB02-5 | Autorisation Drive | autorisation ponctuelle du Capitaine enregistrée avant tout upload (précédent 2026-10-16) |
| H-SB02-6 | R10 | reçu au ledger |

## 5. Risques

- **R1 — 2,1 Go : quota/temps.** → P0 : quota vérifié ; batches avec reprise sur SHA.
- **R2 — Delta SHA items-recuperes.md.** → Procédure §0.4 : règle d'autorité + décision consignée, jamais d'écrasement aveugle.
- **R3 — Frames : régénération impossible.** → Repli §0.2 : archiver les frames, décision tracée.
- **R4 — Écriture Drive sans autorisation.** → Gate P0 inviolable (doctrine lecture seule 2026-10-13, exception ponctuelle uniquement).

*Fin du plan SB-02. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors (upload après gate autorisation).*
