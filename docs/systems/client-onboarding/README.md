# Client Onboarding Automation System — SOP

Prototype Gerber : le dossier Wise Staffing / Avionté (19 tâches) est le cas pilote.
Le livrable n'est pas "19 formulaires remplis" mais ce pipeline, réutilisable pour tout portail (Avionté, Workday, ADP, etc.).

**Contrat canonique : `masterProfile.ts`** — le Master Profile est le noyau de données
souverain (SSOT), topologie tri-polaire OMK (Pôle 1 Légal · Pôle 3 Carrière/JaaS · Pôle 2 Vault).
`dossier.schema.ts` reste la forme de collecte ; le Master Profile est la forme projetée.
Découplage Zero Trust : **Verified Candidate Passport** (public, `OMK-OS-ID`, QR) vs
**Secure Intake Vault** (SSN, banque, adresse, DOB — chiffré local, jamais distribué).
Profils : `DEMO` (ex. "Abdoulaye Traoré") vs `REAL` (ex. "Sallou Camara").

## Pipeline (5 étapes, toujours dans cet ordre)

1. **INVENTAIRE** — `inventory.md` : lister chaque tâche du portail, la typer (`data-entry` | `acknowledgment` | `esign` | `upload`), relever champs requis, textes légaux, méthode de signature. Lecture seule : rien n'est rempli, coché, signé ni soumis.
2. **DOSSIER CLIENT** — `dossier.schema.ts` : une seule source de vérité par client. On ne demande jamais deux fois la même donnée. Le dossier est rempli une fois, mappé vers tous les portails.
3. **MAPPAGE** — colonne "Source dossier" de `inventory.md` : chaque champ du portail pointe vers un champ du dossier. Les champs sans source = données à collecter.
4. **EXÉCUTION** — remplissage automatisé par catégorie :
   - `data-entry` → auto-rempli depuis le dossier
   - `acknowledgment` → texte légal extrait et présenté au client pour relecture
   - `esign` (Adobe Sign "Type") → **PORTE DE SIGNATURE** : le système prépare tout, le client relit et autorise explicitement la signature. Jamais l'inverse.
   - `upload` → fichier demandé au client, déposé via le navigateur
5. **REÇUS** — chaque tâche exécutée produit un reçu (quoi, quand, capture). Règle dure : rien n'est marqué "actif/terminé" sans reçu.

## Règles non négociables

- La signature électronique (même "Type") est un acte juridique du client : porte de signature obligatoire.
- Aucune donnée inventée : champ sans source = bloqué, signalé, demandé.
- Les identifiants portail vivent dans le Secure Vault, jamais dans les fichiers.
- Chaque dossier client est isolé : un répertoire par client sous `clients/`.
