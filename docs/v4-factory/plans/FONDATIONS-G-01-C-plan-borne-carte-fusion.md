# G-01-C — Plan borné : Carte de fusion opposable

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne lore : Bill → Clara → Nardole → validation Doctors → exécution) — 2026-10-17
**Source :** mission Rick (S1) ; découverte Bill G-01 (`fusion/CARTE-FUSION.md`, `g-01a-drive-v3-history.md`, `g-01b-github-linear.md`)
**Arbitrage Capitaine intégré :** Drive = PARA (lecture seule) ; Takeout = archive lecture seule, pas de miroir ; Clara crée les systèmes **depuis** les archives ; le routage capacitaire multi-dimensions = Nardole.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **Le registre vit dans V4** : `fusion/REGISTRE-FUSION.md`, versionné par git (PR + validation Doctors). C'est la référence opposable : statut + pointeur + preuve par surface.
2. **4 statuts, définitions fermées** : `vivant` (V4 = référence vivante, reçoit les écritures) / `figé-archive` (pointé, jamais modifié) / `fantôme` (référencé mais non localisé — état légitime, pas un défaut) / `coquille` (vide, en attente de remplissage — pas un manque à « réparer »).
3. **M7 tranché EN PREMIER** (avant toute cartographie) : V3 reçoit encore des écritures (PR #576, sessions Jules) alors que la doctrine dit « héritage sélectif ». Décision datée : **gel** de V3 OU **périmètre d'écriture documenté** (qui écrit, quoi, jusqu'à quand). Pas de troisième voie floue.
4. **La carte casse si une archive reçoit un push** (C2) : `tools/fusion-watch` + job planifié — compare les empreintes enregistrées (HEAD SHA des repos figés GitHub ; `modifiedTime` des dossiers Drive en listing lecture seule). Écart → échec visible + entrée d'anomalie au registre. Une archive qui bouge sans décision = anomalie, pas une mise à jour silencieuse.
5. **Préambule V3 obligatoire** (ordre Capitaine) : le registre s'ouvre sur l'historique V3 (Bill §0 — « V3 ne s'est pas effondré : il a été consommé », 6 leçons). Enforcement procédural : **aucun design d'agents Tech/Life/Business sur V4 sans l'avoir lu** — le gate de dispatch Nardole le vérifie (le plan cite le préambule, le reviewer le contrôle).
6. **Règle de non-duplication (opposable)** : V4 = référence vivante ; les archives se pointent, ne se modifient jamais ; Drive = PARA lecture seule ; Takeout = archive lecture seule. Chaque surface du registre porte sa règle d'écriture (où s'écrit quoi).
7. **Contrat de récupération lisible (C4)** : le Doc est illisible (connecteur `google_docs` non connecté ; la règle Drive interdit l'export de contournement). P0 : A0 connecte le connecteur OU le Capitaine fournit le contenu. Le design ne l'invente pas ; en attendant, le blocage est documenté avec propriétaire et échéance.
8. **M6 : « non localisé » est un état légitime.** Le heartbeat du fork Moltbot est cherché sur les pistes (infra Capitaine, Drive) ; s'il n'est pas trouvé → statut `fantôme` documenté. **Inventer un heartbeat est hors bornes** (pas de faux binaire « trouvé / inventé » : l'enquête tranche, avec un état honnête possible).
9. **M4 : pas d'écriture Linear sans instruction explicite du Capitaine** (contrainte inviolable) : le design propose le spec du projet miroir ; l'exécution est gatée sur son instruction, documentée comme telle.

## 1. Bornes

**IN :** `fusion/REGISTRE-FUSION.md` (statut + pointeur + preuve par surface) ; `tools/fusion-watch` + job planifié (C2) ; traitement M1–M7 avec décision documentée chacun (M7 en premier) ; contrat de récupération rendu lisible (ou blocage documenté) ; préambule V3 + gate de dispatch.
**OUT :** modifier une archive ; miroir workspace du Takeout ; transfert des principes vers V4.1 (F-01) ; inventer M6 ; écrire dans Linear sans instruction explicite.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — `fusion/REGISTRE-FUSION.md` (référence opposable)**
- Schéma fixe par surface : id, type (repo / Drive / Linear / back-office), statut (4 valeurs §0.2), pointeur (id Drive / URL repo / preuve), règle d'écriture, preuve.
- Sections : préambule V3 (obligatoire) → surfaces vivantes → archives figées → coquille V4.1 → recouvrements (règle §0.6) → décisions M1–M7 (datées) → gaps déclarés.

**Système 2 — `tools/fusion-watch` + job planifié (la carte qui casse)**
- Empreintes enregistrées au registre ; comparaison périodique ; écart sur une surface `figé-archive` → échec visible + anomalie tracée.

**Système 3 — Gate de dispatch Nardole (préambule V3)**
- Tout design d'agents Tech/Life/Business cite le préambule ; le reviewer le contrôle avant dispatch.

**Flux :** P0 (M7 + contrat) → registre → watch → décisions M1–M6 → validation Doctors.

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — M7 + contrat (OBLIGATOIRE, en premier)** | Trancher M7 (gel V3 ou périmètre d'écriture documenté : qui/quoi/jusqu'à quand), daté. Lancer la résolution du contrat de récupération (connecteur ou Capitaine) | H-G01-3 ; H-G01-5 |
| **P1 — Registre** | `fusion/REGISTRE-FUSION.md` : préambule V3 + toutes les surfaces (statut + pointeur + preuve) + règle de non-duplication | H-G01-1, H-G01-6 |
| **P2 — Watch** | `tools/fusion-watch` + job planifié ; empreintes enregistrées | H-G01-2 |
| **P3 — M1–M6** | Décision documentée chacun : M1 archiver la coquille `Agent-OS` (paramètre repo, pas de suppression — exécution propriétaire tracée) ; M2 `coquille` en attente F-01 ; M3 créer les catégories Discussions manquantes (autorité Doctor) ; M4 spec du miroir Linear **proposé, gaté sur instruction explicite du Capitaine** ; M5 vérifier puis dédupliquer #8/#12 ; M6 enquêter puis statuer (`fantôme` si non localisé) | H-G01-4 |
| **P4 — Validation** | Revue Doctors → Nardole dispatche la validation | Tous verts |

**Règle d'exécution :** séquentiel, un seul exécutant. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-G01-1 | Registre opposable | `fusion/REGISTRE-FUSION.md` versionné dans V4 ; chaque surface a statut + pointeur + preuve ; 0 surface sans statut |
| H-G01-2 | La carte casse | modification simulée d'une empreinte d'archive figée → le watch échoue visiblement + anomalie tracée |
| H-G01-3 | M7 tranché en premier, daté | gel OU périmètre (qui/quoi/jusqu'à quand) — décision datée avant P1 |
| H-G01-4 | M1–M6 décidés | 6 décisions documentées et datées ; M4 explicitement gaté sur instruction du Capitaine (non exécuté sans) ; M6 non inventé |
| H-G01-5 | Contrat de récupération | lisible et référencé — OU blocage documenté (propriétaire + échéance), jamais contourné par export |
| H-G01-6 | Préambule V3 obligatoire | présent en tête du registre ; le gate de dispatch le référence (design sans citation du préambule = rejeté) |
| H-G01-7 | Aucune archive modifiée | empreintes inchangées en fin de mission |
| H-G01-8 | R10 | reçu au ledger |

## 5. Risques

- **R1 — Écritures V3 pendant la cartographie (Jules).** → M7 en P0 : le périmètre ou le gel s'applique avant P1.
- **R2 — Contrat de récupération illisible.** → P0 : propriétaire (A0/connecteur ou Capitaine) + échéance ; pas d'invention, pas de contournement.
- **R3 — PC Capitaine inaccessible (Life OS vivant V3).** → La carte documente l'inaccessible (pointeur + preuve d'inaccessibilité), ne l'invente pas.
- **R4 — 35 branches orphelines V4 (écho du sprint V3).** → La référence est `main` ; les branches ne sont pas des surfaces du registre.
- **R5 — Tentation d'inventer M6.** → Hors bornes explicite (H-G01-4).

*Fin du plan G-01-C. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors.*
