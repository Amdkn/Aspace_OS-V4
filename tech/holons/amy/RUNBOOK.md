# Procédure de travail — Amy

1. Charger la source canonique de mandat `agents/registry.json`, puis ce README, AGENTS, CONTRACTS, MEMORY, STATE; lire `.github/agents/amy.agent.md`.
2. Retrouver `mission_id`, `head_sha`, `correlation_id`, lease, droits et références natives depuis l'issue/WorkGraph; UNKNOWN si manquant.
3. Exécuter sans multiplier les appels : partir de SOH-31 ou d'une demande d'usage; spécifier forme/entrée/action/résultat; passer à Rory puis River avec receipt.
4. Comparer résultat attendu/observé, test/receipt/readback, consentement et budget; refuser 'DONE' si le résultat humain/métier n'est pas prouvé.
5. Écrire le receipt au lieu d'origine avec `mission_id, correlation_id, owner, status, effect_id, evidence_refs, return_to`; escalade vers doctor-11 si mandat dépassé.
6. À la reprise sur un autre provider, recharger l'état de l'objet natif plutôt que réciter une conversation; un effet ambigu exige réconciliation avant retry.


## Exceptions
Conflit de permissions, deux claims, provider timeout ou publication incomplète ⇒ `BLOCKED` ou `UNKNOWN`; conserver traces et prévenir doctor-11. Ne jamais vider les receipts pour relancer.
