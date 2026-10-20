# Registre des politiques — A'Space OS V4 (L05)

Statut d'une politique : **OPPOSABLE** (enforcement déclaré et testé,
effet observable) ou **DÉCLARATIVE** (aucun enforcement — jamais présentée
comme opposable). Protocole de changement : politique = PR + revue +
entrée au CHANGELOG — aucune édition silencieuse.

| ID | Énoncé | Statut | Enforcement | Version |
|---|---|---|---|---|
| [P-001](POLICY-001.md) | Sans reçu R10, pas de merge | OPPOSABLE | check CI `r10-receipt` (L01) | v1 · 2026-10-20 |
| [P-002](POLICY-002.md) | Jamais de swarm sans design Clara signé | OPPOSABLE | gate dispatch Nardole (registre) | v1 · 2026-10-20 |
| [P-003](POLICY-003.md) | Aucun secret en repo | OPPOSABLE | check CI `secret-scan` (grep) | v1 · 2026-10-20 |
| [P-004](POLICY-004.md) | Un service = un port, documenté avant d'écouter | OPPOSABLE | check CI `ports-check` ↔ `os/PORTS.md` | v1 · 2026-10-20 |

Changement de statut OPPOSABLE → DÉCLARATIVE (ou l'inverse) = PR + revue +
entrée CHANGELOG, comme tout changement de politique.
