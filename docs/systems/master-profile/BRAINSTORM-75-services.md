# Master Profile × 75 Services — Brainstorm : l'entreprise E-Myth

**Thèse.** Le run Avionté a prouvé le pattern : tout service administratif =
donnée (Master Profile) + workflow (étapes typées) + adaptateur (browser / API / humain)
+ reçus. Les 75 services OMK sont 75 instances de ce pattern. L'entreprise E-Myth,
c'est l'usine qui produit et opère ces instances — pas 75 bricolages, une franchise.

## 1. Architecture en 4 couches

```text
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 1 — SSOT : Master Profile (masterProfile.ts)         │
│   PublicPassport · PrivateVault · legal · career             │
│   signatureGate · profileKind DEMO/REAL                      │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 2 — WORKFLOWS : 75 définitions typées                 │
│   WorkflowDef { act, pole, subFrame, steps[], gates[] }      │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 3 — ADAPTATEURS : comment chaque step s'exécute       │
│   computer-use · api · document · human-gate                │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ COUCHE 4 — REGISTRE : reçus à vérité temporelle              │
│   observed_at vs recorded_at — rien n'est "fait" sans reçu  │
└─────────────────────────────────────────────────────────────┘
```

## 2. Le template franchise — chaque service = 5 actifs

Prouvé sur le cas Avionté (`workspace/systems/client-onboarding/`) :

| Actif | Rôle | Exemple Avionté |
|-------|------|-----------------|
| `SOP.md` | les étapes, toujours dans le même ordre | README.md |
| `schema.ts` | les données d'entrée typées | masterProfile.ts |
| `inventory.md` | cartographie du terrain (portail, formulaires, dialogues) | inventaire 19 tâches + 15 docs Adobe |
| `intake-checklist.md` | la fiche guichet — collecte unique | fiche client A–H |
| `receipts/` | preuves d'exécution horodatées | journal des reçus |

Un nouvel acte = cloner le template, remplir les 5 actifs. C'est ça, la franchise.

## 3. Taxonomie des workflows — toutes sortes

| Code | Archétype | Pattern de référence | Pôle |
|------|-----------|----------------------|------|
| W1 | **Computer-Use Portal** — login Vault → recon lecture seule → remplissage → reçus | Avionté (19 tâches) | 1·2·3 |
| W2 | **Form-Fill & E-Sign** — dialogue Adobe « Type » documenté, porte de signature | 15 docs Adobe Sign | 1·2 |
| W3 | **Document Generation** — CV ATS, lettres, affidavits, passeport de compétences | à construire | 1·3 |
| W4 | **Translation Pipeline** — NotebookLM, fiabilité juridique, ATA | OMK Translate | 1 |
| W5 | **Financial Wiring** — Direct Deposit, W-4/W-2, suivi parrainage $50 | à construire | 2 |
| W6 | **Verification & Audit** — I-9/E-Verify, validité USCIS, certifications | à construire | 1 |
| W7 | **Dispatch & Matching** — files Amazon/DHL/Kroger/Wayfair, SLA 24–48h | à construire | 3 |
| W8 | **Human-Gate Orchestration** — le client décide (48 questions, signature, banque), la machine exécute | porte de signature | 1·2·3 |

## 4. Le Computer-Use Adapter — spec tirée du cas réel

```typescript
interface ComputerUseStep {
  kind: 'navigate' | 'read' | 'fill' | 'click' | 'gate';
  target: string;          // sélecteur ou description d'écran
  valueRef?: string;       // pointeur Master Profile, jamais la valeur en clair
  receipt: boolean;        // tout step produit un reçu
}

interface WorkflowDef {
  act: string;             // ex. "3.2-4"
  pole: 1 | 2 | 3;
  title: string;
  steps: ComputerUseStep[];
  gates: string[];         // points d'arrêt déterministes (signature, banque, médical)
  adapters: ('computer-use' | 'api' | 'document' | 'human-gate')[];
}

interface Receipt {
  act: string;
  step: string;
  observed_at: string;     // quand ça s'est passé sur le terrain
  recorded_at: string;     // quand c'est entré au registre
  evidence: string;        // capture / référence
  actor: 'agent' | 'human';
}
```

**Règles dures du computer-use** (payées cash sur le cas Avionté) :
1. Reconnaissance en lecture seule **avant** toute exécution — inventaire typé d'abord.
2. Identifiants uniquement via Secure Vault, jamais dans les fichiers ni les prompts.
3. Valeurs sensibles par référence (`vault.directDeposit.routingNumber`), jamais en clair.
4. Portes humaines : signature juridique, argent (banque), médical (48 questions), données pré-remplies à vérifier (Personal Info, entrée UPS).
5. CAPTCHA : ne pas contourner — le signaler, basculer en takeover humain.
6. Session : re-login propre à l'expiration (pattern `forceOutReason=NoToken` observé).

## 5. Priorisation — V1 FOCUS = Pôle 3 JaaS

Le badge V1 FOCUS du site est déjà sur le Pôle 3 : c'est le cœur du forfait $300.
Ordre de workflow-isation :

1. **Pôle 3 (Carrière/JaaS)** — onboarding portails (Avionté = prototype, Acte 3.x),
   génération CV ATS calibré, Passeport Compétences scellé, dispatch vers les files.
2. **Pôle 1 (Légal)** — audit I-9, pipeline traductions ATA, attestations notariées.
3. **Pôle 2 (Finance)** — wiring Direct Deposit, W-4/W-2, tracking parrainage $0 Net.

## 6. Le moat — pourquoi c'est une entreprise et pas un script

Le computer-use est une commodité (tout le monde aura un agent navigateur).
Le moat OMK, c'est l'empilement que personne ne clone en un week-end :
**Master Profile SSOT** (la donnée canonique) + **pipeline vérifié** (les 5 actifs par acte,
la cartographie terrain réelle) + **communauté** (Billion Dollar Brand Club) +
**registre de reçus** (la preuve d'exécution). Le 3D/7D n'est que le véhicule.

## 7. Prochaines étapes concrètes

- [ ] Figer le template franchise (les 5 actifs) comme générateur : `new-act <pole> <code>`
- [ ] Coder `WorkflowDef`, les 4 adaptateurs, et le registre de reçus (Supabase, vérité temporelle)
- [ ] Pilote : 3 actes du Pôle 3 workflow-isés de bout en bout (CV ATS, onboarding portail, dispatch)
- [ ] Drop-in monorepo : `src/types/masterProfile.ts` + validateur Zod dans le landing site
- [ ] Fiche démo « Abdoulaye Traoré » (DEMO) pour vendre le système sans exposer de réel
