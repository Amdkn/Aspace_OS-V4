# Inventaire — Wise Staffing Group / Avionté (cas pilote)

Portail : `wisestaffinggroup.myavionte.com` (login "Satellite")
Compte : Sallou Camara — session ouverte 2026-10-06, lecture seule.
Statut : ✅ inventaire complet — 19/19 tâches ouvertes, **rien rempli, coché, signé ni soumis**.

## Verdict

| Catégorie | Nombre | Automatisable |
|-----------|--------|---------------|
| `data-entry` (formulaires in-portal) | 4 | Oui — remplissage depuis le dossier client |
| `esign` (Adobe Sign, redirection externe) | 15 | Non — porte de signature obligatoire |
| `upload` | 0 | — |
| `acknowledgment` pur (case à cocher seule) | 0 | — |

Chaque tâche Adobe Sign affiche : *"To complete the [task], you will be navigated to a partner site, Adobe Sign. Once you have completed the forms, you will be redirected back to this site. All forms must be signed when presented."*

## Formulaires in-portal (remplissage automatisable)

### 1. Direct Deposit — `data-entry`
"Add an Account" révèle :
| Champ | Type | Requis | Source dossier |
|-------|------|--------|----------------|
| Account Type | combobox (Checking/Savings/Paycard) | oui | `dossier.banking.accountType` |
| Account Number | textbox | oui | `dossier.banking.accountNumber` |
| Bank Country | combobox (USA/Canada) | non | `dossier.banking` (inféré) |
| Bank Name | textbox | oui | `dossier.banking` (à ajouter) |
| Routing Number — 9 Digits | textbox | oui | `dossier.banking.routingNumber` |

Notes : jusqu'à 10 comptes ; la liste doit être réordonnée pour que le compte de solde soit en dernier. Bouton Save désactivé tant que le formulaire est invalide.
⚠️ `Bank Name` manque dans le schéma — à ajouter à `dossier.banking`.

### 2. Work History — `data-entry`
Par employeur :
| Champ | Requis | Source dossier |
|-------|--------|----------------|
| Employer | oui | `dossier.workHistory[].employer` |
| Current Job | checkbox | `dossier.workHistory[].endDate == "present"` |
| Title | oui | `dossier.workHistory[].title` |
| From / To | non | `dossier.workHistory[].startDate` / `endDate` |
| Describe Your Duties | non | `dossier.workHistory[]` (à ajouter : `duties`) |
| Country / City / State | non | `dossier.workHistory[]` (à ajouter : `location`) |
| Reason for Leaving | non | `dossier.workHistory[].reasonForLeaving` |

Note : **une entrée pré-existante (UPS)** déjà présente — à vérifier avec le client avant tout écrasement.

### 3. Education — `data-entry`
Checkbox **"No education history" actuellement cochée**. Décocher révèle les champs école.
| Source dossier | Règle |
|----------------|-------|
| `dossier.education` vide | laisser la case cochée |
| `dossier.education` non vide | décocher, remplir par entrée |

### 4. Personal Info — `data-entry` (profil talent)
| Champ | Requis | Source dossier |
|-------|--------|----------------|
| First Name / Middle Name / Last Name | oui/oui* | `dossier.client.fullName` (à découper : `firstName`, `middleName`, `lastName`) |
| Email | non | `dossier.client.email` |
| Country | combobox | `dossier.address` (inféré) |
| Phone | oui | `dossier.client.phone` |
| Address Line One / Two, City, State/Province, Zip/Postal Code | oui/non/oui/oui/oui | `dossier.address` |
| "I have a different Payment Address" | checkbox | `dossier` (à ajouter si pertinent) |

Note : **formulaire pré-rempli** — vérification à l'écran obligatoire avant tout remplissage futur.
⚠️ `Person.fullName` doit être découpé en `firstName` / `middleName` / `lastName` dans le schéma.

## Documents Adobe Sign (porte de signature — 15/15 cartographiés)

Flux universel (identique sur les 15) : bouton « Continue » du portail → Adobe Sign →
second « Continue » (« Your turn to sign — By selecting Continue, I agree to the Terms
of Use, Consumer Disclosure and to use electronic signatures ») → document sur
`secure.na2.echosign.com` (« Review and Sign »). Retour via le bouton retour du top bar.
**Rien tapé, rien appliqué, rien signé** — dialogues fermés via « Close ».

### Boîte de dialogue « Signature Options » (identique partout)

Champ « Click to Sign (required) » → dialogue **Signature Options**, 4 onglets :
- **Type** (sélectionné par défaut) : textbox « Type your signature above » (requis, vide)
- **Draw** : « Draw your signature » — **Image** : « Select an image as your signature »
- **Mobile** : « Create your signature on a mobile device »
- Boutons : **Close** | **Apply** (jamais cliqué)

Compteur « N required fields remaining » + bouton bleu « Sign » dans le panneau gauche (non cliqués).
Données pré-remplies communes : dates en lecture seule (« Oct 6, 2026 » / « 10/06/2026 »),
champs d'impression du nom en lecture seule (vides), montants W-4 à 0 par défaut.
CAPTCHA à sélection d'images présent sur les pages Adobe Sign — non touché.

### Structure par document

| # | Document | Pages | Champs | Source Master Profile |
|---|----------|-------|--------|----------------------|
| 5 | W-2 Consent Form 2025 | 2+ | dropdown « Electronic W2 Consent » yes/no [requis] ; Employee Name [requis, readonly] ; signature ; date [readonly] | `vault.tax.electronicW2Consent` |
| 6 | Screening Deduction Auth | 1 | autorisation déduction casier ($40) + dépistage ($20) sur 1er salaire ; 2 print-name [requis, readonly] ; signature ; date [readonly] | consentements |
| 7 | Employee Safety Guide 2026 | 9 | accusé de réception p.9 ; Employee Name ; signature ; date [readonly] | accusé lu |
| 8 | Policy and Procedures 2026 | 2 | **13 boutons « Click to Initial (required) »** (1 par item de checklist) ; Print Name ; Date of Signing [readonly] ; signature ; mention : signature électronique = valeur manuscrite | accusé lu |
| 9 | TERMS OF EMPLOYMENT 2026 | 2 | emploi at-will ; consentement background check + dépistage ; Print Name ; date (sélecteur) ; signature | accusé lu |
| 10 | DRUG SCREEN AUTHORIZATION 2026 | 1 | consentement dépistage urinaire/sanguin + renonciation ; Employee Name ; signature ; date [readonly] | consentement |
| 11 | Release Form 2026 | 1 | autorisation enquête casier + références (investigative consumer report) ; print-name [readonly] ; signature ; date [readonly] | consentement |
| 12 | Essential Job Functions 2026 | 3 | **le plus complexe : 48 radiogroupes Yes/No [requis]** (restrictions médicales post-offre + capacités physiques) ; 8 textboxes (explications, print name) ; date [readonly] ; signature | réponses client requises |
| 13 | Employee Agreement 2026 | 2 | **non-concurrence 12 mois** post-fin de contrat (pas d'emploi via agences concurrentes) ; pénalités **jusqu'à $10,000 + frais d'avocat + injonction** ; 2 print-name ; date (sélecteur) ; signature | ⚠ revue juridique client impérative |
| 14 | LLH Template and opt out Info English | 1 | info programme santé LLH, auto-enrôlement, opt-out au (800) 280-8034 ; Employee Name [readonly] ; signature ; date [readonly] | accusé lu |
| 15 | LLH Onboarding Flyer_English_20260409 | 2 | comparatif paie avec/sans LLH ($516.50/$496.65), opt-out 1.800.280.8034 ; name [readonly] ; signature ; date [readonly] | accusé lu |
| 16 | Child Labor & Human Rights | 3 | tolérance zéro travail des enfants/forcé, recrutement éthique, signalement ; Employee Name ; signature ; date [readonly] | accusé lu |
| 17 | Federal W-4 2025 LS | 6 | **seul formulaire de saisie** : 9 champs requis — First/Last name, SSN, adresse, ville/état/ZIP, **State combobox pré-sélectionné « AK » (à corriger vers l'état réel)**, statut marital (3 radios), montants (défaut 0), First work date [requis] ; signature ; date [readonly] | `vault.tax` + `career` + `vault.ssn` |
| 18 | Insurance Election Link Labor Source 2025 | 2 | accusé + lien d'enrôlement externe `http://www.ebaenrollment.com/644219` (enrôlement sur site tiers) ; signature ; print-name « Custom Field 1 » [requis] ; date (sélecteur) | accusé lu |
| 19 | Biometric Consent Form LS | 1 | consentement biométrie (pointeuse digitale/faciale, Labor Source LLC), révocable par écrit, données détruites en fin d'emploi ; signature ; date [readonly] ; Employee Name [requis, readonly] | consentement |

### Points durs pour la porte de signature

1. **Employee Agreement 2026** — clause de non-concurrence 12 mois + pénalités $10k : revue juridique par le client avant toute signature.
2. **Essential Job Functions 2026** — 48 réponses Yes/No médicales/physiques : seul le client peut répondre.
3. **Federal W-4 2025 LS** — State pré-sélectionné « AK » : corriger vers l'état réel au remplissage ; SSN requis.
4. **Policy and Procedures 2026** — 13 initiales + signature : lecture effective de la checklist requise.

## Dictionnaire d'exécution — Master Profile → 19 tâches Avionté

Le Master Profile sert de dictionnaire de variables pour l'agent d'exécution.

```text
  MASTER PROFILE                                    PORTAIL AVIONTÉ (19 TÂCHES)
─────────────────────────────────────────────────────────────────────────────
• career (PublicPassport)                   ──►  [Personal Info] — nom, tél, adresse
• career.education                          ──►  [Education] — diplômes & cursus
• career.workHistory                         ──►  [Work History] — postes, dates, employeurs
• vault.directDeposit (chiffré)             ──►  [Direct Deposit] — ⚠ validation manuelle opérateur
• vault.tax.electronicW2Consent             ──►  [W-2 Consent Form 2025] — porte de signature
• vault.authorizations (consentements)      ──►  [Screening Deduction Auth] — porte de signature
• legal + accusés lus                       ──►  [Employee Safety Guide 2026] — porte de signature
• legal + accusés lus                       ──►  [Policy and Procedures 2026] — porte de signature
• legal + accusés lus                       ──►  [TERMS OF EMPLOYMENT 2026] — porte de signature
• vault.tax (W-4)                           ──►  [Federal W-4 2025 LS] — porte de signature
• signatureGate                             ──►  les 9 autres documents Adobe Sign
                                                 ═════════════════════════════════════
                                                 PORTE DE SIGNATURE HUMAINE
                                                 (signatureGate.signatureAuthorized
                                                  + scope + legalTextsReviewed)
```

Règle d'or : l'agent déroule tout ce qui est `data-entry` et prépare les
documents ; **la porte de signature Adobe Sign (mode "Type") et l'étape
bancaire restent des points d'arrêt déterministes où l'humain reprend
le contrôle.**

## Écarts schéma ↔ portail (à corriger dans `dossier.schema.ts`)

1. `dossier.banking` : ajouter `bankName: string`.
2. `Person` : découper `fullName` → `firstName`, `middleName?`, `lastName`.
3. `JobEntry` : ajouter `duties?: string`, `location?: { country?, city?, state? }`.

## Journal des reçus

| Date | Tâche | Action | Preuve |
|------|-------|--------|--------|
| 2026-10-06 | Inventaire 19 tâches | lecture seule, panels fermés via Cancel/Finish Later | rapport navigateur |
| 2026-10-06 | Cartographie 15 docs Adobe Sign | Continue portail → Continue Adobe → document → retour top bar ; dialogues « Signature Options » documentés, fermés via Close ; rien tapé/appliqué/signé | rapport navigateur |
| 2026-10-06 | Vérification d'avancement | 10/19 terminées par l'utilisateur (Work History, Education, Personal Info, W-2 Consent, Screening Deduction, Safety Guide, Policy & Procedures, Terms of Employment, Drug Screen Auth, Release Form) ; 9 restantes | dashboard 12:57 EDT |
| 2026-10-06 | Revérification | 18/19 terminées ; ne reste que **Direct Deposit** (données bancaires requises) | dashboard 14:59 EDT |
