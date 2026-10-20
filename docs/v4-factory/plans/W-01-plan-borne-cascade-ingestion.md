# W-01 — Plan borné : Cascade d'ingestion vidéo autonome

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-19
**Source :** mission Rick (S1) W-01/02/03 ; Discover Bill (`~/workspace/architecture-compagnons/discover-ingestion-youtube-autonome.md`) ; preuve persistée (`~/workspace/watch-reports/GQatuTWSRqY-gemini-url-2026-10-19.md` — la vidéo Cole Medin qui avait échoué au bot-wall ce matin, ingérée en 26–41 s en autonomie complète)
**Mandat :** « tant que Bill ne saura pas récupérer mes vidéos YouTube, je serai un babysitter » — critère de sortie : une vidéo sans sous-titres traitée de bout en bout, **zéro action du Capitaine**.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Cascade fixe : V2 → V1 → V3 → dégradation honnête étiquetée.**
   - **V2 — Sous-titres yt-dlp d'abord** (verbatim horodaté, coût zéro) : quand la piste existe et passe, elle sert.
   - **V1 — Gemini URL en fallback** (`fileData.fileUri` — Google récupère la vidéo, l'IP de la VM ne touche jamais YouTube) : compréhension + citations quand il n'y a pas de sous-titres ou que V2 est bloquée. **Percée prouvée** (2 exécutions reproductibles).
   - **V3 — Navigateur en secours 429 uniquement** (session du Capitaine) : ne résout pas le sans-sous-titres ; dernier recours avant dégradation.
   - **Dégradation honnête étiquetée** : métadonnées seules, **dites comme telles** — jamais de transcription inventée, jamais d'échec silencieux.
2. **Label de voie obligatoire sur chaque rapport** : `verbatim` (V2) / `compréhension` (V1) / `secours` (V3) / `dégradé` (métadonnées). Les citations V1 sont **near-verbatim et marquées comme telles** — jamais présentées comme des sous-titres ou du verbatim.
3. **Rework, pas rewrite.** `watch.py` orchestre les voies ; le prototype `youtube-via-gemini.py` (déjà écrit et testé par Bill, clé via Secure Vault) est l'implémentation V1 ; yt-dlp n'est pas réécrit. V4 (audio+ASR) et V5 (ASR local) restent **écartées** (download = maillon faible ; VM insuffisante) ; V6 (tiers) non recommandée (vie privée).
4. **Vidéos privées/non-répertoriées → échec explicite.** V1 est publiques-uniquement : l'échec est **documenté**, jamais contourné, jamais silencieux. L'accès aux privées = le compte du Capitaine, son choix (hors design).
5. **Journal de cascade** : chaque ingestion journalise la voie qui a servi + le motif d'échec des voies précédentes. La voie empruntée fait partie du rapport.
6. **Limites V1 assumées** : ~2 h max (500 intermittents sur très longues, rapportés comme tels) ; coût ~258 tok/s → budget = W-02 (le garde-fou est la précondition des runs non supervisés).

## 1. Bornes

**IN :** cascade V2→V1→V3 + labels + journal + rework `watch.py` + prototype V1 intégré.
**OUT :** contourner un bot-wall/CAPTCHA (interdit par construction) ; ASR local ; services tiers en primaire ; accès aux vidéos privées.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Cascade** : V2 (verbatim, gratuit) → V1 (compréhension, budgétée) → V3 (secours 429) → dégradé étiqueté.
**Système 2 — Étiquetage** : label de voie + citations near-verbatim marquées + journal de cascade.
**Système 3 — Honnêteté** : échec explicite (privées), dégradation dite, 0 invention.

**Flux :** P0 (cascade + prototype intégré) → P1 (étiquetage + journal) → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Cascade** | Rework `watch.py` : V2 → V1 (prototype intégré) → V3 ; garde-fou W-02 câblé avant tout run non supervisé | H-W01-1, H-W01-3 |
| **P1 — Étiquetage** | Label de voie sur chaque rapport ; journal de cascade | H-W01-4, H-W01-5 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-W01-1 | **Critère de sortie du mandat** | une vidéo publique sans sous-titres est ingérée de bout en bout via V1, **zéro action du Capitaine** |
| H-W01-2 | Vidéos privées | vidéo privée/non-répertoriée → **échec explicite documenté** ; 0 tentative de contournement |
| H-W01-3 | Discipline de cascade | vidéo avec sous-titres → V2 sert le verbatim, **V1 n'est pas appelée** (vérifié au journal) |
| H-W01-4 | Étiquetage | chaque rapport porte son label de voie ; les citations V1 sont marquées near-verbatim |
| H-W01-5 | Journal | chaque ingestion journalise voie servie + motifs d'échec des voies précédentes |
| H-W01-6 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Quota free-tier V1.** → W-02 (garde-fou) ; la cascade dégrade sans brûler en silence.
- **R2 — Très longues vidéos (>2 h).** → 500 intermittents rapportés honnêtement ; pas de promesse au-delà de la limite documentée.
- **R3 — V3 fragile (UI).** → Secours uniquement, jamais primaire.

*Fin du plan W-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*
