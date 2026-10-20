# Ledger R10 — le registre vivant des reçus (L01, D-N027)

**Doctrine :** sans reçu, pas de merge. Ce dossier est le mécanisme vivant :
il porte l'intégrité du repo, pas GitHub (arbitrage A2 : pas de verrouillage,
`enforce_admins` reste false — le contrôle vient des reçus).

## Layout

```
ledger/
  README.md          — ce fichier
  SCHEMA.md          — le schéma de reçu versionné (aspace.r10-receipt.v1)
  genesis/           — le bloc genesis : les 22 reçus historiques, verbatim, intacts
    README.md        — provenance du bloc genesis
    receipts.md      — les 22 reçus G-20261009-001→022, copiés à l'identique
    genesis.sha256   — hash du bloc (vérification d'intégrité, H-L01-4)
  receipts/          — les reçus émis sous schéma v1, un JSON par reçu
    G-YYYYMMDD-NNN.json
```

## Émission ritualisée (H-L01-1)

Graham émet :
- **1 reçu par mission terminée** (mission_id + SHA du livrable) ;
- **1 reçu hebdo** au rituel M'Benga/Graham (battement du noyau, même sans mission).

Le check CI `r10-receipt` (workflow `.github/workflows/r10-receipt.yml`) vérifie sur
chaque PR vers `main` : un reçu valide référençant le head SHA (ou la PR). Sans reçu
valide → check rouge → merge bloqué (H-L01-2). Le check est du pur code (zéro modèle).

## Règle d'or du ledger

On n'efface rien, on ne réécrit rien. Une erreur se corrige par une entrée datée
qui nomme ce qu'elle remplace — jamais en éditant le passé.
