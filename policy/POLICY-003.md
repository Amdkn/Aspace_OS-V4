# POLICY-003 — Aucun secret en repo

- **ID :** P-003
- **Version :** v1 — **date d'effet :** 2026-10-20 — **remplace :** —
- **Statut :** OPPOSABLE
- **Énoncé :** aucun secret (clé API, token, clé privée, mot de passe)
  dans le repo — ni en clair, ni « en exemple réel ». Les secrets vivent
  dans l'environnement (Codespace secrets, variables CI, Secure Vault).
- **Périmètre :** tout le repo (hors `.git`, `node_modules`).
- **Mécanisme d'enforcement :** check CI `secret-scan`
  (`.github/workflows/policy-checks.yml`, `tools/secret_scan.py`, job
  `secret-scan`) — grep de patterns (JWT `eyJ…`, `sb_secret_`,
  clés AWS `AKIA…`, tokens GitHub, clés privées PEM, `service_role`
  assigné). Pattern trouvé → check rouge.
- **Preuve (H-L05-2) :** fichier seedé contenant un faux JWT →
  échec visible du scan (testé en local).
