# F-01 — Plan borné : Chantier 1 — Corpus des principes transférables

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne lore : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** dispatch Rick (S1) « Finalisation des Fondations Aspace » ; découverte Bill C1–C6 (`chantier-1-qualification-corpus.md`) ; cadre `BEFORE-YOU-BUILD.md`
**Arbitrage Rick intégré (A1, tranché puis ARBITRÉ PAR LE CAPITAINE 2026-10-17 ~04:35 EDT) :** Takeout Gemini → **PAS de miroir workspace.** Drive est son PARA ; Bill archive le Takeout **en lecture seule** dans Life OS Data (`1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM`), exactement comme l'extraction ChatGPT. Le corpus **pointe** vers ces archives (zéro duplication). Le routage capacitaire multi-dimensions (horizons vertical, diagonal, orthogonal) est le domaine de Nardole (Hyper Dispatcher, Router de l'Infini) — Clara crée les systèmes **depuis** ces archives. Structure cible C4 confirmée (pointeurs).
**Séquencement : exécution APRÈS salvage complet** (lot C partie 1/2 en cours, puis D, E). Design maintenant.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara — tranchées ici, ne remontent pas)

1. **Zéro duplication.** Le salvage reste où il est (`~/workspace/chatgpt-extraction/`), le Takeout reste en Drive (lecture seule) ; le corpus de principes **pointe**, il ne recopie pas. Tout pointeur est vérifié (résolu + hash) — un pointeur cassé = anomalie bloquante, pas un avertissement ignoré.
2. **Takeout : pointeurs uniquement (arbitrage Capitaine A1).** `corpus/gemini/` pointe vers les archives Takeout en lecture seule dans Life OS Data (`1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM`) — archivées par Bill comme l'extraction ChatGPT. **Aucun miroir workspace.** Le routage capacitaire multi-dimensions est le domaine de Nardole (Hyper Dispatcher) : le design crée les systèmes *depuis* ces archives, il ne route pas.
3. **Schéma fixe PRINCIPE-XXX.md** : Énoncé (citation exacte entre guillemets ; reformulation marquée « reformulation », jamais sous guillemets) / Statut (4 valeurs) / Sources (fichier + message # + date + URL) / Test T1–T5 (chacun : verdict + preuve) / Corrections (bidirectionnel) / Domaine.
4. **Statuts à 4 valeurs, transitions versionnées** : `TRANSFÉRABLE` (T1–T5 tous verts, preuves) / `ARCHIVE` (contexte historique) / `À ÉPROUVER` (candidat, preuve manquante) / `ÉCARTÉ` (contradit — motif + source de la contradiction obligatoires). Un changement de statut = décision datée + preuve, jamais une édition silencieuse. En cas de doute, le statut ne peut pas être `TRANSFÉRABLE` : le motif du doute détermine le statut (contexte historique → `ARCHIVE`, preuve manquante → `À ÉPROUVER`), documenté dans l'entrée.
5. **REGISTRE-PRINCIPES.md = index unique.** Tout principe y figure ; aucun principe hors index ; aucun doublon inter-sources (même principe en ChatGPT et Gemini → **1** principe, 2+ sources — renforce T2).
6. **Gate de complétude du salvage** : l'exécution ne démarre que sur checklist datée — lot C 1/2 terminé, D livré, E livré, Takeout arbitré (A1). Démarrage anticipé = hors bornes.
7. **Médias scopés, pas abandonnés** (OUT Rick) : `corpus/gemini/medias/` marqué `EN ATTENTE ARBITRAGE A1` (transcription : images, 77 .wav, 11 .mp4) — ni transcrits sans arbitrage, ni effacés silencieusement.
8. **P quasi absent : constat, pas invention** (garde-fou Bill) : si P reste quasi absent, le livrable le constate.

## 1. Bornes (scope strict)

**IN :**
- Structure cible C4 (pointers, zéro duplication) : `corpus/chatgpt/` → chatgpt-extraction/ (registre.md → elements-enregistres.md 4 états ; recuperes.md → items-recuperes.md FINAL ; ipbd/ → sorties lot E) ; `corpus/gemini/` → Drive (drive/ + mensuels-index.md + analyse-takeout.md + brut-manifestes/ — PAS les zips) ; `principes/` (REGISTRE-PRINCIPES.md + PRINCIPE-XXX.md) ; `preuves/` (traçabilité).
- Critères T1–T5, statuts à 4 valeurs.
- Méthode 8 étapes (C6) : repérage priorisé (9 fortes ChatGPT d'abord, puis 7 moyennes, puis mensuels Gemini via INDEX_MENSUEL.md) → découpage (1 énoncé = 1 candidat) → citation exacte → attribution marquée → déduplication inter-sources → test T1–T5 → traçabilité → contre-vérification ≥ 10 %.
- Compteur : principes extraits avec critères explicites.

**OUT :**
- Exécution avant salvage complet (gate §0.6).
- Transcription des médias (attente arbitrage A1 — scopé §0.7).
- Transfert V4.1 (mission suivante, sur ordre du Capitaine uniquement).

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — `corpus/` (matière, pointeurs lecture seule)**
- `corpus/chatgpt/` : pointeurs vers `~/workspace/chatgpt-extraction/` (registre.md → elements-enregistres.md ; recuperes.md → items-recuperes.md ; ipbd/ → sorties lot E à venir). Vérifiés (résolution + hash).
- `corpus/gemini/` : pointeurs vers les archives Takeout **en lecture seule** dans Life OS Data (`1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM`, archivées par Bill comme l'extraction ChatGPT) — `drive/` (archives), `mensuels-index.md` → INDEX_MENSUEL.md, `analyse-takeout.md` → RAPPORT_ANALYSE_TAKEOUT.md, `brut-manifestes/` → inventaires des zips (jamais les zips eux-mêmes, restent sur PC Capitaine), `medias/` → marqué `EN ATTENTE ARBITRAGE` (transcription : images, 77 .wav, 11 .mp4). **Aucun miroir workspace** (arbitrage Capitaine A1).
- Règle : aucun contenu recopié ; tout pointeur cassé bloque.

**Système 2 — `principes/` (produit, nouveau)**
- `REGISTRE-PRINCIPES.md` : index unique — id, énoncé court, statut, sources, domaine.
- `<domaine>/PRINCIPE-XXX.md` : schéma fixe §0.3.
- Transitions de statut versionnées (§0.4).

**Système 3 — `preuves/` (traçabilité)**
- Chaque principe pointe ses sources exactes (fichier + message # + date + URL) ; citations exactes + liens ; corrections bidirectionnelles.

**Système 4 — Gate de complétude (checklist datée)**
- Lot C 1/2 ✓, D ✓, E ✓, Takeout arbitré (A1) ✓ — l'exécution ne démarre que sur 4/4.

**Flux de données :** salvage complet (gate) → repérage priorisé (C6.1) → découpage → citation/attribution → déduplication → T1–T5 → traçabilité → contre-vérification ≥10 % → REGISTRE-PRINCIPES.md → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Gate salvage (OBLIGATOIRE, première étape d'exécution)** | Vérifier la checklist : lot C 1/2 terminé, D livré, E livré, Takeout arbitré (A1). Si incomplet → BLOQUÉ, pas d'extraction partielle | 4/4 cochés et datés |
| **P1 — Structure** | Créer `corpus/`, `principes/`, `preuves/` selon C4 ; déclarer la branche Takeout dans `SOURCE.md` (post-A1) ; marquer `medias/` en attente | H-F01-1, H-F01-2 |
| **P2 — Repérage** | 9 fortes ChatGPT → 7 moyennes → mensuels Gemini (marqueurs I/P/B/D + doux + impératifs) | — |
| **P3 — Extraction** | Découpage 1=1, citation exacte, attribution marquée, déduplication inter-sources | H-F01-3 |
| **P4 — Qualification** | Test T1–T5 par principe, statuts attribués (transitions datées) | H-F01-4 |
| **P5 — Traçabilité** | `preuves/`, REGISTRE-PRINCIPES.md, corrections bidirectionnelles | H-F01-5 |
| **P6 — Contre-vérification** | Second passage ≥ 10 % (exécutant ou méthode différent), écarts résolus | H-F01-6 |
| **P7 — Validation** | Revue Doctors → Nardole dispatche la validation | Tous verts |

**Règle d'exécution :** phases séquentielles, un seul exécutant. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Tests hold-out (définis AVANT exécution — validation aveugle)

| ID | Vérifie | Seuil |
|---|---|---|
| **H-F01-1** | Structure C4, zéro duplication | tous les pointeurs résolus (0 cassé) ; aucun contenu recopié (comparaison hash : 0 duplication) |
| **H-F01-2** | Pointeurs Takeout (arbitrage A1) | tous les pointeurs `corpus/gemini/` résolus vers les archives Life OS Data en lecture seule ; 0 miroir workspace ; 0 duplication |
| **H-F01-3** | Schéma des principes | chaque PRINCIPE-XXX.md a les 6 sections (§0.3) ; citations entre guillemets = mots exacts (échantillon revérifié) ; reformulations marquées |
| **H-F01-4** | T1–T5 appliqués honnêtement | tout `TRANSFÉRABLE` a T1–T5 verts avec preuves ; tout `ÉCARTÉ` a motif + source de contradiction ; 0 `TRANSFÉRABLE` par défaut |
| **H-F01-5** | Index unique | chaque principe dans REGISTRE-PRINCIPES.md ; 0 orphelin ; 0 doublon inter-sources |
| **H-F01-6** | Contre-vérification ≥ 10 % | second passage documenté, écarts résolus avant validation |
| **H-F01-7** | Gate salvage respecté | l'exécution n'a pas démarré avant 4/4 (C 1/2, D, E, A1) — checklist datée |
| **H-F01-8** | Médias scopés | `medias/` marqué en attente A1 : ni transcrits sans arbitrage, ni effacés |
| **H-F01-9** | Traçabilité R10 | reçu (mission_id F-01 + SHA) au ledger |

## 5. Risques (Bill R1–R7 → réponses design)

- **R1 — Lot C incomplet.** → Gate P0 : pas d'extraction partielle (H-F01-7).
- **R2 — D/E en design.** → Séquencement : F-01 exécute après D et E livrés (l'IPBD est une source) ; le design n'attend pas.
- **R3 — Takeout : pipeline d'ingestion.** → Tranché par arbitrage Capitaine A1 : pointeurs vers les archives Life OS Data en lecture seule, aucun miroir workspace. Le routage capacitaire est le domaine de Nardole.
- **R4 — Médias non transcrits.** → Scopé §0.7/§1 OUT ; lot séparé ultérieur.
- **R5 — Biais de source.** → Échantillonnage stratifié par période dans la méthode (C6.1) ; ne pas sur-pondérer le récent.
- **R6 — Export natif ChatGPT pendant.** → S'il arrive : compléter/corriger puis rejouer la déduplication (étape 5) — tracé, pas silencieux.
- **R7 — Relais A0/B2 ultérieur.** → D, E et le corpus se rouvrent de façon tracée (PRD-D §8, PRD-E §9).

## 6. Séquence d'exécution (pas un swarm)

```
[salvage complet : C 1/2 + D + E] → P0 (gate — OBLIGATOIRE) → H-F01-7 → P1 (structure) → H-F01-1/H-F01-2
  → P2 (repérage) → P3 (extraction) → H-F01-3 → P4 (T1–T5) → H-F01-4 → P5 (traçabilité) → H-F01-5
  → P6 (contre-vérif ≥10 %) → H-F01-6 → H-F01-8 → P7 (revue Doctors → validation Nardole) → H-F01-9
```

Tout écart → **BLOQUÉ** avec raison + qui débloque. Pas de contournement silencieux.

*Fin du plan F-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors (exécution après salvage complet).*
