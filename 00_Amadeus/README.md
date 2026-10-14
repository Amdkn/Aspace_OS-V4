# A0 — Amadeus | Home institutionnel du jumeau numérique
> `holon_id: aspace:a0:amadeus` · créé 2026-10-14 · état: DOCUMENTED / NOT-YET-EMBODIED · aucune approbation humaine implicite

## Navigation de reprise (ordre obligatoire)
1. [IDENTITY.md](IDENTITY.md) et [SOUL.md](SOUL.md) — qui sert qui, valeurs et limites.
2. [GOVERNANCE.md](GOVERNANCE.md) et [AGENTS.md](AGENTS.md) — qui peut faire quoi et comment écrire.
3. [IPBD.md](IPBD.md) et [register/ipbd.public.json](register/ipbd.public.json) — intentions avec provenance; les contenus intimes restent dans le Drive privé.
4. [STATE.md](STATE.md), [DECISIONS.md], [HANDOFF.md](HANDOFF.md) — ce qui est vérifié, actif, bloqué, et la reprise sans humain-middleware.
5. [DESIGN.md](DESIGN.md), [RELATIONS.md](RELATIONS.md), [CAPABILITIES.md](CAPABILITIES.md), [VISION.md](VISION.md), [MISSION.md](MISSION.md), [AGENT.md](AGENT.md).
6. [contracts/README.md](contracts/README.md) et [sources/README.md](sources/README.md).

## Résidences et autorité par objet
- **Identité institutionnelle / contrats publics versionnés** : ce dossier `00_Amadeus/` dans V4 (GitHub). Version d'intégration = `main` après PR/review; toute branche de mission est candidate, pas canon promu.
- **Mémoire personnelle / paroles brutes / IPBD sensibles** : résidence privée Drive existante « A0 transversal » : https://drive.google.com/drive/folders/1eJrtfbOFARzySEQoBLf1BAJu9avpcRO7. Conserver son ID `1eJrtfbOFARzySEQoBLf1BAJu9avpcRO7` et ses enfants, ne jamais y recréer un A0 concurrent.
- **Mémoire événementielle dérivée** : `40_Memory/` V4, contractuellement sous Graham; ni une troisième personne ni un registre de consentement.
- **Patrimoine historique** : https://github.com/Amdkn/Aspace_OS_V3/tree/main/00_Amadeus, sources V2 Geordi/`01_Identity_Core` et `migration/` V4. Les vieux prompts ont statut HISTORICAL à réconcilier.
- **Local** : V3 `C:\Users\amado\ASpace_OS_V3\00_Amadeus` = miroir historique, pas cible automatique de mutation. Amd-PC non vérifié en direct lors de cette écriture. Codespace/VPS V4 = projection compute sous contrôle.
- **WorkGraph** : travaux/claims/effets, pas vérité de la personne. Registre de coordination Drive: https://docs.google.com/spreadsheets/d/1F0osspXkG-Ugu2JcNQICBXcf6_MSq0ddiSGIkNEqv3Y/edit.

## Contrôle anti-amnésie
Lecture de README → IDENTITY → GOV → IPBD → STATE → HANDOFF doit suffire pour reconstituer un contexte de travail **sans réécrire la volonté**. Une session sans connexion aux sources persistantes annonce `UNKNOWN`, jamais `ACTIVE` ou `DONE`. Lire les preuves live avant tout effet.

## Sécurité
Le dépôt V4 est **public**. Aucune donnée privée (identité civile détaillée, famille/intimité, santé, finance, secrets, transcripts bruts) ici. La projection publique conserve IDs non identifiants, statuts, contrats, et pointeurs vers les sources privées à permission distincte. Ne jamais recopier un document Drive privé dans GitHub par défaut.
