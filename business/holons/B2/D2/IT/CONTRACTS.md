# D2 IT — Cyborg / Suivi Santé

- Identifiant : `aspace:business:D2:IT` — **manager B2 DC** attaché à [Jerry D1 Culber](../../../B1/D1/README.md), Blue Life Zone, LD03.
- Fonction contextualisée : Suivi Santé ; fonction transversale IT/R&D. Chef de squad Kang Dynasty : [D3 IT](../../../B3/D3/IT/README.md).
- Source manager : [Playbook DC](https://docs.google.com/document/d/1XEVH0OVoqiFcW7UjoFp54dDXIlXKfASYfSDw9QxQeL8/edit) ; squad [dossier physique](https://drive.google.com/drive/folders/1q6lq-_iQOjtLCy9hAi3tz_2wcJitGvms) ; [Runbook](https://docs.google.com/document/d/166flPC5KAciT7-xgbe4_1iF0vaMIqQ3INopyqN-yZDM/edit) ; [portail canonique](https://docs.google.com/document/d/185i8YMtFr73sEAtyg_XX9_ecPCbS9mw40ygm8QRCTNY/edit). Source du Playbook actuel sur Drive; ne pas copier son contenu sensible sur GitHub.
- Ancien patrimoine VP : Cyborg (R&D & IT), agent_canon `b2-06-cyborg-it` ; **ne transforme pas Coach OS V3 en instructions obligatoires V4**.
## Relations distinctes
1. **Manager** : D1 Culber — responsabilité résultat durable; aucun transfert à J1 par défaut.
2. **Pairs** : D2/GRO, D2/SAL, D2/PRD, D2/OPS, D2/FIN, D2/PPL, D2/LEG ; résolution meso inter-fonctionnelle.
3. **Engagements partagés** : Curie fournit cycle, GTD l'action, DEAL supprime/automatise les frictions; la fonction Suivi Santé garde son owner natif. Aucun A3 Life ni B3 ne change de rattachement lors d'un travail transversal.
## Input / Output
Input `mission_id, correlation_id, parent_b1, source_ref, authority, expected_effect, DoD, return_to`. Output `accepted_jtbd, squad_ref, evidence_refs, actual_effect_or_unknown, observed_at, recorded_at, return_to`. Idempotency avant mutation; UNKNOWN après effet incertain.
