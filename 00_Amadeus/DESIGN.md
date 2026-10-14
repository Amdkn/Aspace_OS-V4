# DESIGN — Twin Continuity Architecture v1
Statut: design exécutable des fichiers et contrats; l'intégration live Gateway/Drive↔GitHub↔WorkGraph n'est pas présumée.

## 1. Frontière Amadou ↔ Amadeus
Amadou est la personne vécue: intentions, besoins, mémoire autobiographique, consentement, arbitrage, données privées. `aspace:a0:amadeus` est une entité institutionnelle logicielle et **révocable**: modèle du contexte connu, des préférences déclarées, de leur évolution et des pouvoirs explicitement accordés. Elle ne déduit ni droit civil ni volonté à partir d'une prédiction. Les alias Kirby et les sessions sont des `EmbodimentRef`, jamais des nouvelles racines identitaires.

## 2. Modèle causal (pas un pipeline forcé)
```text
human utterance / durable source / observed event
   ├─ Raw Evidence + capture timestamp + classification (Graham)
   └─ IPBD Candidate [Intent|Problem|Need|Desire]
       ├─ clarify uncertainty / preserve original words
       ├─ Meaning Links [Ikigai pillar+horizon, Wheel LD, values]
       ├─ Ownership [A1/A2/A3, B1/B2/B3, S1/S2/S3]
       ├─ Demand / Commitment [PARA, 12WY, GTD, DEAL only if needed]
       └─ CapabilityNeed / WorkGraph Mission (only if executable)
          → effect + receipt + outcome evidence
          → return_to A0 (summary/options only when useful)
```
Un besoin peut rester une Area; un désir peut rester une possibilité; ni un projet ni une Issue n'est obligatoire. Les six frameworks sont **services transverses composables**, pas six validations séquentielles.

## 3. Contrats de capture et temporalité
`IPBDRecord` conserve `id,kind,formulation,statement_type,source_refs,observed_at,recorded_at,source_authority,epistemic_state,validity_scope,prior_versions,supersedes`. Vocabulaire d'état: `CURRENT|HISTORICAL|SUPERSEDED|CONTRADICTED|PROPOSED|UNKNOWN` pour la connaissance; fraîcheur `FRESH|STALE|UNKNOWN` séparée du type épistémique; `OPEN|IN_REVIEW|ON_HOLD|CLOSED_WITH_EVIDENCE` pour prise en charge. Une source retrouvée tard n'est jamais plus récente du seul fait de son `recorded_at`.

`HumanUtterance` se cite verbatim avec ID/horodatage; `AgentInterpretation` affiche son inférence et peut être contestée; `ThirdPartyContent` ne vaut pas parole du fondateur. Si l'extrait direct est introuvable, garder `REPORTED_DIRECTIVE` avec source secondaire.

## 4. Mémoire durable et état volatile
**Drive privé** = formulations personnelles et archive originale; **Git V4 `00_Amadeus`** = identité/instructions/schémas publics; **`40_Memory`** = preuves, mémoire indexée et temporalité gérée par Graham; **WorkGraph** = claims, bindings, events, receipts; **STATE.md** = curseur lisible dérivé avec date de contrôle, n'est pas SSOT; **HANDOFF.md** = point de reprise, pas bus de messages. Sources brutes immuables et checksum; synthèses versionnées, liens de supersession; pas de duplication de données sensibles dans les branches.

## 5. Délégation et retour
`IntentEnvelope` → `CapabilityNeed/GoalCommitment` → `DelegationEnvelope` (scope, version policy, expiry, budget, `work_id`, `correlation_id`, `return_to`) → dispatch local Nardole/Gateway/routage du framework → WorkGraph event/receipt → DomainOutcome → `A0ReturnEnvelope`. Un agent peut décider de sa méthode, solliciter des pairs, ralentir, vérifier, réparer et conclure dans son périmètre; il ne demande pas un aller-retour A0 pour chaque transaction. Aucun scheduler « décide la prochaine intention »; un réveil restaure le monde, puis le holon décide dans son mandat.

## 6. Contradictions et évolution
Ne jamais fusionner silencieusement « marketing digital » (personnel 2026-10-02) et « AaaS » (encodage 2026-05-21). Conserver deux `TemporalClaim` de provenance différente, relation `CORRESPONDS_POSSIBLY` jusqu'à ratification. Lors de contradiction: comparer sujet/predicat/scope/source_authority, observation vs enregistrement, produire `CanonTransition` ou `UNKNOWN`. Une intention ancienne demeure présente comme OPEN/HISTORICAL tant qu'aucune clôture/évolution source n'existe.

## 7. Plusieurs sessions, un seul A0
Session A: lit `main` au SHA connu et capsule à cutoff T; propose mutation branchée + diff+evidence. Session B: lit même identity ID, pas de fork de personne; compare `base_sha`, `version`, `authority_envelope` et `correlation_id`. Concurrence → merge contrôlé ou conflit explicite, jamais last-writer-wins sur décision personnelle. Autorité retirée → sessions anciennes fenced et aucune nouvelle mutation. Exécution = receipt idempotent; statut runtime ≠ institution ≠ travail.

## 8. Reprise à froid
1. Lire README/IDENTITY/GOVERNANCE et version constitutionnelle applicable. 2. Charger seulement les IPBD/LD nécessaires, source et temporal cutoff. 3. Lire STATE et event/receipt les plus récents, pas seulement un vieux handoff. 4. Réconcilier `UNKNOWN`, supersessions et authorizations. 5. Récupérer `return_to`, poursuivre une cellule sûre, faire remonter seulement décision non déléguée. 6. Mettre à jour curseur et pointeurs après preuve.

## 9. Implémentation / cible / raccordements
| Élément | Prouvé par lecture | À raccorder ou certifier |
|---|---|---|
| Résidence Drive A0 | dossier existant, ID conservé | Docs privés et Markdown bruts projetés |
| V4 Git Home | cette PR crée les contrats | review/merge + contexte harness |
| IPBD | sources historiques sourcées | extraction exhaustive Takeout, registre privé, vraie autorité Supabase |
| Mémoire | `python -m aspace.memory`, `40_Memory` selon V4 | compilateur de contexte live par A0 |
| Life | `life/registry.json` + 6 frameworks | engagements GTD/12WY/DEAL par IDs natifs |
| Exécution | contrats de WorkGraph et modèle receipts documentés | Gateway runtime, sync Drive/Git/WorkGraph, tests de 2 sessions |

## 10. Acceptance
Nouveau harness lit README et trouve même `holon_id`, IPBD connu, source, domaine, steward, autorité, conflit, preuve, `return_to`. Il sait dire « inconnu », peut produire un diff réversible, et ne peut pas fabriquer une décision humaine. `tests/test_home_contract.py` sert de contrôle documentaire; pas de certification de la vie vécue.
