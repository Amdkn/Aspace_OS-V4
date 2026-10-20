# Ports — mono-repo

| Service | Port | Source vérifiée |
|---|---|---|
| os/life web (vite dev) | 4444 | `os/life/package.json` (`vite --port=4444`) |
| os/life blackboard server | 4445 | `os/life/server/blackboard/index.ts` (défaut, `PORT` overridable) |
| Life→Business bridge | 3001 (127.0.0.1) | `os/life/src/lib/api/client.ts` |
| os/agent | TBD | à documenter |
| os/business | TBD | à documenter |

Règle : un service = un port. Documenter ici avant d'écouter — pas de port
en dur non documenté.
