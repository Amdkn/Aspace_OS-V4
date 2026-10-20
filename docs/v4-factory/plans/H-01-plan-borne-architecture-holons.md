# H-01 — Plan borné : Architecture des 9 Holons + capacités multiples

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) « Mission 1 : Architecture des 9 Compagnons » ; Discover Bill (`~/workspace/architecture-compagnons/qualif-holons-9.md` — les 9 Holons existent, complets, différenciés, 12 fichiers chacun, maintenus 2026-10-15)
**Principe : réactivation, pas (re)création.** État réel : 1/9 actif (Bill), 1/9 interrupted (Yaz), 7/9 dormants. Aucun trou de définition.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Aucune (re)création de Holon.** Les 9 existent (profils `.github/agents/`, résidences `tech/holons/<nom>/` 12 fichiers, `agents/registry.json` conforme au lore, doctrine S3). Le design porte sur l'architecture (fiches + namespace) et la réactivation.
2. **Fiche par Compagnon (schéma fixe)** : identité (namespacée §0.4) + Holon (profil + résidence) + **capacités multiples : déclarées vs prouvées** (états du pattern d'honnêteté : DECLARED / CONNECTED / EXECUTED / VERIFIED — jamais de capacité supposée sur la seule présence d'un provider) + preuves (liens) + mapping Doctor/lore + dette éventuelle. Les données Bill = baseline pré-remplie.
3. **Plan de réactivation : référence F-02 L06, pas de duplication.** Le plan F-02/L06 (SIGNÉ) couvre déjà : diagnostic Yaz-first (H-L06-2), ping 9/9 (H-L06-3), rituel d'activité tracé (H-L06-4), « dormant-mais-tracé = état valide ». H-01 y **réfère** ; il y ajoute les fiches comme baseline de réactivation (chaque ping met à jour la colonne PROVEN de la fiche).
4. **Namespace tranché : par cœur, pas aplati.** `aspace:kernel:*` (Ryan, Yaz, Graham) / `aspace:life:*` (Amy, Rory, River) / `aspace:buzz:*` (Bill, Clara, Nardole). Rationnel : les trois cœurs sont des **frontières de sécurité/responsabilité** (cf. amendement D-N017 : pas des paliers LLM) — l'aplatissement `aspace:tech:*` les efface. `aspace:tech:*` est enregistré comme **alias déprécié** (pas de rupture silencieuse).
5. **Correction factuelle (base du plan) :** le verdict « Clara = goulot, 0 design en 8 jours » mesurait la **circulation**, pas la production — 18+ plans signés existent dans `~/workspace/v4-factory/plans/` (2026-10-17) ; le chaînon manquant est le protocole d'atterrissage (H-02) + les designs accessibles (H-05). La fiche Clara enregistre ses capacités prouvées **avec preuves** (le répertoire des plans) — pas de défensive, des faits vérifiables.
6. **Dette REGISTRE-INSPIRATIONS.md** : non tenu depuis le 09 alors que Bill a produit toute la chaîne du 17 — dette tracée, soldée à l'exécution (Bill met à jour ; la fiche Bill porte le check).

## 1. Bornes

**IN :** 9 fiches (schéma §0.2, baseline Bill) + namespace tranché + plan de réactivation (référence F-02 L06) + dette registre soldée.
**OUT :** (re)créer des Holons ; dupliquer F-02 L06 ; trancher seul au-delà du namespace.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Fiches** (`docs/holons/<nom>.md` ou registre) : schéma fixe, baseline pré-remplie, colonne PROVEN mise à jour par le rituel.
**Système 2 — Namespace** : identités par cœur + alias déprécié `aspace:tech:*` documenté.
**Système 3 — Réactivation** : pointeur normatif vers F-02 L06 (pas de copie).

**Flux :** P0 (fiches baseline) → P1 (namespace) → P2 (réactivation via F-02 L06) → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Fiches** | 9 fiches au schéma §0.2, baseline Bill, preuves liées | H-H01-1, H-H01-4 |
| **P1 — Namespace** | Identités par cœur ; alias `aspace:tech:*` documenté | H-H01-2 |
| **P2 — Réactivation** | Exécution via F-02 L06 (Yaz-first, ping 9/9, rituel) ; fiches mises à jour | H-H01-3 |
| **P3 — Dette** | REGISTRE-INSPIRATIONS.md à jour | H-H01-5 |

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-H01-1 | 9 fiches | chacune au schéma §0.2 (identité + déclarées vs prouvées + preuves) ; 0 capacité supposée sans preuve |
| H-H01-2 | Namespace | les 9 identités par cœur ; `aspace:tech:*` présent uniquement comme alias déprécié documenté |
| H-H01-3 | Zéro doublon F-02 L06 | la section réactivation **réfère** F-02 L06 (pas de contenu normatif dupliqué — diff contrôlé) |
| H-H01-4 | Fiche Clara factuelle | capacités prouvées = artefacts vérifiables (répertoire des plans) |
| H-H01-5 | Dette soldée | REGISTRE-INSPIRATIONS.md couvre la chaîne du 17 |
| H-H01-6 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Clara goulot de sa propre mission.** → Traité §0.5 : le goulot était la circulation (H-02/H-05), pas la production.
- **R2 — Yaz interrupted.** → F-02 L06 H-L06-2 (diagnostic d'abord), référencé pas dupliqué.
- **R3 — Réinvention.** → §0.1 : tout existe ; le design n'écrit que fiches + namespace.

*Fin du plan H-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*
