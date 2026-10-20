# W-03 — Plan borné : Verbatim sans sous-titres, phase 2 (mission conditionnelle)

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-19
**Source :** mission Rick (S1) W-01/02/03 ; Discover Bill (`~/workspace/architecture-compagnons/discover-ingestion-youtube-autonome.md`, §4)
**Principe : mission dormante par design.** Elle ne s'ouvre que si un canal de téléchargement propre est **prouvé** ET avec le consentement explicite du Capitaine. Dormant = état valide, pas un échec.
**Statut :** plan livré — **SIGNÉ Clara** (le design est signé ; **l'exécution est gatée** sur les deux conditions §0.1).

---

## 0. Décisions design (autorité Clara)

1. **Deux gates d'exécution, documentées :**
   - **Gate 1 — canal prouvé** : un canal de téléchargement propre (ex. cookies du profil navigateur du Capitaine) **démontré** sur une vidéo test — pas supposé, pas promis.
   - **Gate 2 — consentement** : consentement **explicite** du Capitaine pour l'usage de sa session/cookies.
   - Sans les deux gates documentées → la mission **reste dormante** (état enregistré, pas une erreur, pas un retard).
2. **Périmètre = strictement le download.** L'ASR est résolue (V1) : canal ouvert → audio → ASR (Gemini Files API audio ou agrégateur Whisper) → verbatim horodaté. Rien d'autre n'est à builder.
3. **Jamais de contournement CAPTCHA/bot-check.** Règle du skill, maintenue : tout design ou étape exigeant un contournement = **rejeté par construction** — l'exécution s'arrête et le rapporte, elle ne le contourne pas.
4. **Ne pas builder avant que le canal soit prouvé.** Le download reste le maillon faible (V4 écartée pour cette raison) — aucun code écrit sur une promesse de canal.

## 1. Bornes

**IN :** design du canal + gates documentées + ASR via V1/Whisper une fois le canal ouvert.
**OUT :** tout contournement (CAPTCHA, bot-check, session détournée) ; builder avant canal prouvé ; accès sans consentement.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Gates** : canal prouvé + consentement explicite, documentés avant exécution.
**Système 2 — Périmètre** : download uniquement ; ASR = V1.
**Système 3 — Interdit** : contournement = arrêt + rapport.

**Flux :** P0 (gates documentées) → P1 (canal → ASR → verbatim) → validation Doctors. **P0 avant tout.**

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Gates** | Canal démontré + consentement explicite documentés | H-W03-1 |
| **P1 — Verbatim** | Audio → ASR → verbatim horodaté (si P0 vert) | H-W03-3 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-W03-1 | Mission conditionnelle | sans canal prouvé + consentement documenté → mission **dormante enregistrée**, ni erreur ni exécution |
| H-W03-2 | Interdit de contournement | étape exigeant un contournement → exécution **arrêtée et rapportée**, jamais contournée |
| H-W03-3 | Verbatim (phase d'exécution) | vidéo sans sous-titres → verbatim horodaté via le canal |
| H-W03-4 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Canal jamais prouvé.** → La mission reste dormante : c'est un état valide, W-01 couvre déjà le besoin (compréhension).
- **R2 — Tentation de contournement.** → §0.3 : rejeté par construction, pas par vigilance.
- **R3 — Consentement ambigu.** → Explicite ou rien ; un consentement supposé ne compte pas.

*Fin du plan W-03. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors (exécution gatée §0.1).*
