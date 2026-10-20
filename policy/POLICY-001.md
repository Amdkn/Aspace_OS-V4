# POLICY-001 — Sans reçu R10, pas de merge

- **ID :** P-001
- **Version :** v1 — **date d'effet :** 2026-10-20 — **remplace :** —
- **Statut :** OPPOSABLE
- **Énoncé :** aucun merge sur `main` sans un reçu R10 valide le couvrant
  (schéma `aspace.r10-receipt.v1` : mission_id, sha complet, observed_at,
  recorded_at, proof, issuer).
- **Périmètre :** tout merge sur `main` du repo Aspace_OS-V4.
- **Mécanisme d'enforcement :** check CI `r10-receipt`
  (`.github/workflows/r10-receipt.yml`, `tools/check_r10_receipt.py`, L01) —
  requis sur `main`. Sans reçu valide : check rouge, merge bloqué.
- **Preuve (H-L05-2) :** `check_r10_receipt.py` contre un head sans reçu →
  `R10-FAIL`, exit 1 (seed testé à L01 sur PR #90, re-vérifié ici).

Note doctrine : le bypass owner reste possible (`enforce_admins=false`,
arbitrage A2) — mais le bypass est tracé par l'audit non-bypass (L04).
Le reçu bloque le merge normal ; la traçabilité couvre le reste.
