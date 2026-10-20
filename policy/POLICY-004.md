# POLICY-004 — Un service = un port, documenté avant d'écouter

- **ID :** P-004
- **Version :** v1 — **date d'effet :** 2026-10-20 — **remplace :** —
- **Statut :** OPPOSABLE
- **Énoncé :** tout service qui écoute doit être documenté dans
  `os/PORTS.md` **avant** d'écouter — un port en dur non documenté est
  une violation. Un service = un port.
- **Périmètre :** le code source du mono-repo (`os/`, `tools/`) ;
  hors périmètre : `node_modules`, tests, docs, configs d'outillage
  (ex. `supabase/config.toml` — ports gérés par la CLI).
- **Mécanisme d'enforcement :** check CI `ports-check`
  (`.github/workflows/policy-checks.yml`, `tools/check_ports.py`, job
  `ports-check`) — croisement des ports bindés dans le code
  (`.listen(N)`, défauts `PORT ?? N`, `--port=N`, `port:` vite) avec les
  ports documentés dans `os/PORTS.md`. Port non documenté → check rouge.
- **Preuve (H-L05-2) :** fichier seedé avec `.listen(9999)` non
  documenté → échec visible du check (testé en local).
