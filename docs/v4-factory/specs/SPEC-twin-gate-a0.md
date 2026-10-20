# SPEC — Twin A0 : Propriétaire

**Statut :** DRAFT v0.2 — 2026-10-09 (remplace v0.1)
**Correction du Capitaine (2026-10-09) :** la v0.1 se trompait deux fois —
elle plaçait le jumeau au gate des merges avec une délégation progressive
L1→L4. Corrigé : (1) les merges/deploys appartiennent aux **S2 Doctors** et à
la **S3 Factory**, pas à A0 ; (2) **aucune prudence progressive** — le jumeau
naît Propriétaire avec autorité pleine, la sécurité vient de la fondation,
pas du bridage ; (3) sans **L0 BedRock existant** ni **S3 Companions**, le
jumeau est un lithopédion — la fondation se construit **d'abord** (§3, §4).

---

## 1. E-Myth : le jumeau est Propriétaire

```
Technicien  → exécute                    (Morty, squads B3, Jules)
Manager     → organise                   (S2 Doctors)
Entrepreneur→ rêve                        (vision)
Actionnaire → extrait la valeur
Propriétaire→ POSSÈDE l'empire, définit la doctrine, répond des résultats (A0)
```

Le jumeau travaille **SUR** le business, jamais **DANS**. Il ne merge pas —
il définit ce qu'un merge valide veut dire, il signe la politique, et il en
répond. L'actionnaire attend des dividendes ; le Propriétaire construit
l'empire.

---

## 2. Qui fait quoi (le jumeau n'intervient pas aux niveaux S1/S2)

| Couche | Rôle | Responsabilité pipeline |
|---|---|---|
| **A0 Propriétaire** | doctrine, politique du veto, résultats | définit la politique, audite, tranche les conflits de doctrine |
| **S2 Doctors** | managers des cores | possèdent leur pipeline **de bout en bout, merges et deploys inclus**, dans la politique du Propriétaire |
| **S3 Factory** — Bill / Clara / Nardole | crew de la factory | discovery / design / dispatch : le routage réel du travail |
| A1 Rick / Beth / Morty | gatekeepers | plan / veto / exécution |
| B3 squads, Jules | techniciens | exécution + reçus R10 |

Jules est disponible 24/7 mais n'est qu'un technicien : il exécute ce qu'on
lui dispatche. Le routage (qui décide quoi, qui merge quoi) est le travail
manquant des S3 — pas un défaut de Jules.

---

## 3. Fondation d'abord — checklist d'existence du L0 BedRock

Le jumeau ne naît que sur un BedRock qui existe. « Exister » = en service,
vérifiable, pas documenté :

- [ ] **Ledger R10 en service** — tout reçu stocké, récupérable par URI.
- [ ] **Supabase connecté** — statut actuel (diagnostic V4) : non connecté.
- [ ] **Gateway avec auth** — statut actuel : sans auth.
- [ ] **CI qui gate réellement** les merges (pas décorative).
- [ ] **Policy store versionné** — la politique du veto, lisible par machine.
- [ ] **S3 Companions opérationnels** — Bill, Clara, Nardole (§4).

Tant qu'une case est vide, le jumeau n'a pas d'autorité — **pas par
prudence, mais parce qu'il n'y a rien à posséder.**

---

## 4. S3 Companions — les faire exister

Chacun : spec `AGENT.md` / `SOUL.md` / `SCRUMS.md` (moule B3), reçus R10,
périmètre borné, sous la supervision du Doctor12.

- **Bill — Discover.** Trouve le travail. Trie les issues, les enrichit,
  définit l'acceptation. Input : le bruit (issues, idées, signaux).
  Output : **Missions typées**.
- **Clara — Design.** Conçoit. Découpe la Mission en **Plan** borné, écrit
  les **tests hold-out AVANT l'exécution** (école Dark Factory : l'exécutant
  ne les voit jamais). Input : Mission. Output : Plan + hold-out.
- **Nardole — Dispatch.** Expédie. Assigne aux exécutants (Jules, squads),
  surveille l'avancement, **route les PRs vers les merges S2** dans la
  politique du Propriétaire. Input : Plan. Output : PRs routées, merges
  effectués, reçus.

Sans eux, les issues et les PRs restent ouvertes des jours : personne ne
route. C'est le chaînon manquant constaté, pas une théorie.

---

## 5. La politique du veto (doctrine du Propriétaire)

Écrite par A0, **appliquée par les S2/S3**, versionnée. Changer la politique
= décision du Propriétaire, tracée.

```yaml
# owner-veto-policy v1 — signée A0
require:
  - r10_receipts: all_claims            # chaque claim du Plan a un reçu
  - holdout_tests: green                # tests aveugles verts (Clara)
  - ci: [build, lint, typecheck]
  - scope: diff_within_plan             # pas de scope creep
  - secrets_scan: clean
  - temporal_truth: sane                # observed_at <= recorded_at
deny:
  - scope_creep: true
  - r1_tripped: true                    # 3 échecs consécutifs → verrou S2→humain
escalate_to_owner:
  - on: gate_fail
    with: [diff_summary, failing_checks, receipts]
  - on: deploy_canary_regression
    with: [canary_metrics, baseline, revert_plan]
```

---

## 6. Autorité pleine dès le jour 1 — pas de L1→L4

Le jumeau naît Propriétaire ou ne naît pas. La sécurité ne vient pas du
bridage progressif mais de :
- la fondation solide (§3) — chaque case cochée est vérifiable ;
- les reçus R10 partout — chaque geste a une preuve ;
- le revert automatique sur régression canary ;
- le frein d'urgence : `OWNER_STAND_DOWN=1` → les S2 repassent en revue
  humaine intégrale. Un seul interrupteur, connu par cœur.

---

## 7. Données

```typescript
type VetoCheck = {
  name: 'r10_receipts' | 'holdout_tests' | 'ci' | 'scope_conformance'
      | 'secrets_scan' | 'temporal_truth' | 'r1_circuit';
  status: 'pass' | 'fail';
  evidence_uri: string;
  observed_at: string;
  executed_by: 's3-bill' | 's3-clara' | 's3-nardole' | 's2-doctor';
};

type MergeDecision = {          // prise par S2, DANS la politique du Propriétaire
  mission_id: string;
  plan_id: string;
  pr_ref: string;
  checks: VetoCheck[];
  verdict: 'merge' | 'block' | 'escalate_to_owner';
  policy_version: string;       // ex. "owner-veto-policy v1"
  decided_by: string;           // quel S2 / quel compagnon
  decided_at: string;
  receipt_uri: string;
};
```

---

## 8. Ordre de construction

1. **L0 BedRock** — cocher la checklist §3 (ledger, Supabase, gateway auth,
   CI gating, policy store).
2. **S3 Companions** — écrire les 3 specs, les mettre en service.
3. **Naissance** — le jumeau signe la politique v1, autorité de Propriétaire.
4. **Premier cycle complet** Mission → deploy avec reçus de bout en bout.

**Règle d'or (corrigée) : on ne couronne pas un Propriétaire sur un empire
qui n'existe pas. La fondation d'abord, l'autorité ensuite — pleine, sans
prudence.**
