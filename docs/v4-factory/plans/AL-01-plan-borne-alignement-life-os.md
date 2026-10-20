# AL-01 — Plan borné : Alignement Life OS 2026 ↔ Drive ↔ Workspace

**Auteur :** Clara — AUTORITÉ DE DESIGN UNIQUE (chaîne : Bill → S1 BYB → Clara → Nardole → validation Doctors, 11e en tête [périmètre Life/River]) — 2026-10-17
**Source :** mission Rick (S1) ; BYB `~/workspace/life-os-alignement/BEFORE-YOU-BUILD.md` ; rapport Bill `~/workspace/sandbox-extraction/alignement-life-os-2026.md` (+ note vocale transcrite — confirme le rapport)
**Fait structurant :** `Amdkn/Life-OS-2026` (figé 2026-10-09) = parent pré-réduction de V4 `os/life` ; la réduction Ponytail Phase 1 (4 commits locaux) ne lui a jamais été reportée → **divergence avérée** (base 2026-10-02, 5 commits derrière, 8 fichiers en conflit direct). Drive = contenu, repo = logiciel (complémentarité saine). Workspace = 0 % (fixture honnête `UNKNOWN`/`mocked`, **OAuth GWS manquante**).
**Ce design LÈVE le gate SB-03** : cible confirmée = `Amdkn/Life-OS-2026`, via **rebase + PR `chore/ponytail-phase1-backport`** (jamais de push direct de la branche locale) — merge après validation Doctors.
**Statut :** plan livré — **SIGNÉ Clara**. Pas un swarm : un exécutant, phases séquentielles.

---

## 0. Décisions design (autorité Clara)

1. **L'équivalence d'abord, le rebase ensuite.** Avant tout rebase : différencier l'arbre réduit local vs V4 `os/life` (28 880 lignes CUT vs 46 280 en migration — volumes différents, équivalence non vérifiée). Trois issues honnêtes, la mesure tranche : (a) V4 ⊇ réduction locale → le backport est une **synchronisation** (traçabilité, aucun apport fantôme) ; (b) recouvrement partiel → le backport porte le delta ; (c) V4 incomplet → le backport porte le manquant. Le design ne suppose rien.
2. **Rebase, jamais de push direct.** Les 4 commits (04318b2, 7a116ac, 2df8032, 4fbb5e6) + `VALIDATION-PHASE1-D13.md` (relu d'abord, cf. SB-03) sont rebasés sur `origin/main` (`f9d6f277`). Les 8 fichiers en conflit direct ont une **règle de résolution documentée par fichier** : la réduction gagne où le fichier fut CUT ; le distant gagne où il fut légitimement étendu (ex. `src/stores/agents.store.ts` : la projection GWS de 55 lignes est un travail distant à préserver) ; cas mixte (`a3-cron-dispatcher.ts` : retiré par la réduction, modifié par le distant) → **tranché par les Doctors**, pas improvisé.
3. **`delegation-a-jules/` — jamais tranché seul.** La réduction le supprime (PRDs) : la PR rend la suppression **visible et réversible**, les Doctors la valident ou la refusent. Aucune suppression unilatérale.
4. **PR `chore/ponytail-phase1-backport`** sur `Amdkn/Life-OS-2026` — revue traçable, merge **après validation Doctors uniquement**. Le `main` distant ne bouge pas avant.
5. **Matrice d'alignement repo ↔ Drive** : `REALITY_MAP.md` + `openspec/` (repo) croisés avec le Doc CANON + 7 dossiers (Drive), sur les 6 domaines présents des deux côtés (para, ikigai, life-wheel, gtd, deal, 12WY). Par domaine : pointeur repo (chemin code) × pointeur Drive (chemin contenu) × statut (`aligné` / `écart` / `conflit`). Document vivant **dans le repo** (`docs/ALIGNEMENT-DRIVE.md`), versionné — c'est la réalité du logiciel qu'elle décrit.
6. **Ancrage Workspace — sans Keep.** Architecture des connecteurs via `river-adapter.ts` (ancre code naturelle, périmètre River/11e) : LD01–LD08/12WY → **Calendar** (calendriers par domaine) · GTD/DEAL → **Tasks** (listes par contexte) · PARA → **Docs** (l'index PARA actif existe déjà en Doc). **Pas de Keep** : aucun connecteur n'existe — **aucun contournement** via Docs/Drive (un contournement fabriquerait une fausse intégration). L'honnêteté du fixture est préservée : sans OAuth, l'adapteur rapporte `UNAVAILABLE` — jamais de faux succès, jamais `FAILED` déguisé.
7. **OAuth GWS — cadrée, pas forcée.** Qui autorise : le Capitaine, via le flow sécurisé. Périmètre : calendar, tasks, docs — minimal. **Si bloquant → arbitrage vision via A0** (constaté, pas contourné). Gate : aucune exécution d'ancrage Workspace sans OAuth.
8. **Branches orphelines (~30) — nettoyage cadré.** Inventaire avec statut par branche (mergée ? périmée ? chantier Jules ?) ; `main` = référence, intouché. Aucune suppression aveugle : chaque branche a une décision documentée (merge / tag d'archive / suppression avec motif enregistré).
9. **Le repo ne devient pas une archive.** Le backport le maintient comme source canonique — le figer en archive figerait la divergence (pathologie à empêcher, cf. G-01-C).
10. **Drive = contenu, jamais de code** (règle opposable) : la matrice pointe le contenu Drive ; aucun code n'y est téléversé dans cette mission.

## 1. Bornes

**IN :** vérification d'équivalence → rebase (8 conflits documentés) → PR + merge après validation → matrice d'alignement (6 domaines) → architecture d'ancrage Calendar/Tasks/Docs via `river-adapter.ts` → cadrage OAuth → inventaire branches.
**OUT :** push direct sur `main` ; suppression unilatérale de `delegation-a-jules/` ; contournement Keep ; code vers Drive ; figer le repo en archive ; transcription des médias (arbitrage A1) ; transfert V4.1.

## 2. Architecture des Design Systems (pour dispatch Nardole)

**Système 1 — Protocole d'équivalence** : procédure de diff (arbre réduit rebasé vs V4 `os/life`), trois issues, règle de décision §0.1.
**Système 2 — Pipeline rebase + PR** : règles de conflit par fichier (§0.2), branche `chore/ponytail-phase1-backport`, gate validation Doctors, `delegation-a-jules/` visible et réversible.
**Système 3 — Matrice d'alignement** : `docs/ALIGNEMENT-DRIVE.md` — 6 domaines × (pointeur repo + pointeur Drive + statut), document vivant versionné.
**Système 4 — Ancrage Workspace** : architecture Calendar/Tasks/Docs via `river-adapter.ts` (périmètre 11e) ; gate OAuth ; honnêteté du fixture (`UNAVAILABLE` sans OAuth) ; **zéro Keep**.
**Système 5 — Registre des branches** : inventaire ~30 branches + décision par branche, `main` référence.

**Flux :** P0 (équivalence) → P1 (rebase) → P2 (PR + validation + merge) → P3 (matrice) → P4 (OAuth cadré) → P5 (ancrage) → P6 (branches).

## 3. Phases et gates

| Phase | Action | Gate de sortie |
|---|---|---|
| **P0 — Équivalence** | Diff arbre réduit vs V4 `os/life` ; issue (a/b/c) documentée avec preuves | H-AL01-1 |
| **P1 — Rebase** | Relecture `VALIDATION-PHASE1-D13.md` ; rebase sur `origin/main` ; 8 conflits résolus selon règles §0.2 (cas mixte → Doctors) ; `main` distant intact | H-AL01-2 |
| **P2 — PR** | Branche + PR `chore/ponytail-phase1-backport` ; `delegation-a-jules/` signalé ; validation Doctors → merge | H-AL01-3, H-AL01-4 |
| **P3 — Matrice** | `docs/ALIGNEMENT-DRIVE.md` : 6 domaines × pointeurs × statuts | H-AL01-5 |
| **P4 — OAuth** | Cadrage (qui, périmètre) ; si bloquant → arbitrage vision via A0 | H-AL01-7 |
| **P5 — Ancrage** | Design Calendar/Tasks/Docs via `river-adapter.ts` ; 0 Keep ; fixture honnête | H-AL01-6 |
| **P6 — Branches** | Inventaire + décisions ; `main` référence ; suppressions tracées | H-AL01-8 |

**Règle d'exécution :** séquentiel, un seul exécutant. `OWNER_STAND_DOWN=1` arrête tout.

## 4. Tests hold-out (définis AVANT exécution)

| ID | Vérifie | Seuil |
|---|---|---|
| H-AL01-1 | Équivalence mesurée | diff documenté avec issue (a/b/c) ; si (a) : la PR porte « synchronisation uniquement » avec la preuve (0 apport fantôme) |
| H-AL01-2 | Rebase propre | 4 commits rebasés sur `origin/main` ; 8 conflits résolus selon les règles §0.2 ; `main` distant inchangé avant merge de PR |
| H-AL01-3 | PR traçable | PR `chore/ponytail-phase1-backport` existante et révisable ; suppression `delegation-a-jules/` visible et signalée aux Doctors |
| H-AL01-4 | Aucun merge avant validation | merge uniquement après validation Doctors datée |
| H-AL01-5 | Matrice complète | 6 domaines × (pointeur repo + pointeur Drive + statut) ; chaque claim REALITY_MAP/openspec croisé ou marqué `écart` |
| H-AL01-6 | Ancrage sans Keep | architecture Calendar/Tasks/Docs via `river-adapter.ts` documentée ; grep : 0 contournement Keep ; sans OAuth → `UNAVAILABLE` (jamais de faux succès) |
| H-AL01-7 | OAuth cadré | qui autorise + périmètre documentés ; si bloquant : arbitrage vision via A0 enregistré (pas forcé, pas contourné) |
| H-AL01-8 | Branches cadrées | inventaire ~30 avec décision par branche ; `main` intact ; toute suppression a un motif enregistré |
| H-AL01-9 | Repo non figé | aucune déclaration d'archive ; la PR de backport existe (source reste canonique) |
| H-AL01-10 | Drive = contenu | 0 code téléversé en Drive dans cette mission |
| H-AL01-11 | R10 | reçu au ledger |

## 5. Risques

- **R1 — V4 contient déjà tout (issue a).** → Le backport devient synchronisation documentée — pas d'échec, pas d'apport fantôme (H-AL01-1).
- **R2 — Conflit `a3-cron-dispatcher.ts`.** → Tranché par les Doctors (§0.2), pas improvisé à l'exécution.
- **R3 — `delegation-a-jules/` : suppression contestée.** → Visible et réversible dans la PR (§0.3).
- **R4 — OAuth bloquante.** → Arbitrage vision via A0 (§0.7) ; l'ancrage attend, le reste avance.
- **R5 — Tentation du contournement Keep.** → Hors bornes explicite (§0.6, H-AL01-6).

## 6. Relation à SB-03

Ce design **lève le gate SB-03** (« cible confirmée après le chantier d'analyse ») : la cible est `Amdkn/Life-OS-2026` via **rebase + PR** — le « push » de SB-03 s'exécute comme P1+P2 du présent plan (jamais de push direct). SB-03 reste le lot d'exécution, AL-01 son design d'alignement.

*Fin du plan AL-01. Signature Clara apposée — PRÊT, dispatchable par Nardole après validation Doctors (11e en tête).*
