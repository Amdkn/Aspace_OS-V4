# Ports — mono-repo

| Service | Port | Source vérifiée |
|---|---|---|
| os/life web (vite dev) | 4444 | `os/life/package.json` (`vite --port=4444`) |
| os/life blackboard server | 4445 | `os/life/server/blackboard/index.ts` (défaut, `PORT` overridable) |
| Life→Business bridge | 3001 (127.0.0.1) | `os/life/src/lib/api/client.ts` |
| os/agent web (vite dev) | 5555 | `os/agent/vite.config.ts` (strictPort) |
| os/business visualizer (server) | 4600 | `os/business/.claude/skills/sssf/apps/visualizer/server/index.ts` (défaut, `PORT` overridable) |
| os/business visualizer (vite dev) | 4601 | `os/business/.claude/skills/sssf/apps/visualizer/vite.config.ts` |
| os/agent | TBD | à documenter |
| os/business | TBD | à documenter |

Règle : un service = un port. Documenter ici avant d'écouter — pas de port
en dur non documenté.
