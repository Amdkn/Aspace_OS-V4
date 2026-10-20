# G-02 — « Jules MCP » : config et surface MCP réelles

**Mission :** Bill (holon DISCOVER) — qualification « Fusion overview », ordre S1 Rick 2026-10-17.
**Date :** 2026-10-17 ~05:00 EDT · **Statut :** QUALIFIÉ.
**Méthode :** docs officielles (developers.google.com/jules/api — lue en intégralité), repo officiel `google-labs-code/jules-sdk` (README packages/mcp, source primaire), clone V4 (`repo-v4-readonly`), API GitHub (`gh`, URLs avec `/repos/`). Lecture seule stricte.

---

> ## ⛔ CONTRAINTE DURE — SECRETS GITHUB ACTIONS
>
> **Les valeurs des secrets GitHub Actions (`JULES_API_KEY` sur V4) ne sont JAMAIS lisibles via API** — garantie de la plateforme GitHub + règle dure du Capitaine.
> Si une clé doit être réutilisée hors Actions, elle viendra du Capitaine via Secure Vault — **jamais par extraction, jamais par contournement**.
> Cette qualification n'a tenté **aucune** lecture de valeur de secret (ni via API, ni via logs, ni via artefacts de workflow).
>
> **Frontière documentée :**
> | Visible (utilisé ici) | JAMAIS visible |
> |---|---|
> | Noms des secrets (`JULES_API_KEY`, `LABEL_PAT`), date de dernière MAJ | Valeurs des secrets |
> | Workflows qui les référencent (`.github/workflows/issue-factory.yml:39`) | Contenu des secrets dans les logs (masqué par GitHub) |
> | Nom de la variable d'env dans le code (`os.environ['JULES_API_KEY']`) | Clé dans les artefacts `factory-out/` (reçus de session uniquement, pas la clé) |

---

## 1 — Correction du modèle mental : « le MCP de Jules » ne se configure pas sur jules.google.com

**Il n'existe aucun serveur MCP hébergé par Google pour Jules, et rien ne se configure côté jules.google.com / Google Cloud pour le MCP.** Le paysage réel, en deux couches :

**Couche 1 — Jules = API REST officielle (seule interface serveur).**
- Base : `https://jules.googleapis.com/v1alpha` — ressources `Source`, `Session`, `Activity`.
- Auth : clé générée dans la **page Settings de l'app web jules.google.com** (maximum 3 clés), passée dans le header `X-Goog-Api-Key`.
- Prérequis : la **Jules GitHub App** doit être installée sur le repo cible via « Connect GitHub » dans l'app web, sinon le repo n'apparaît pas dans `GET /v1alpha/sources`.
- Source : https://developers.google.com/jules/api (lue le 2026-10-17 — sections Authentication, API concepts, Quickstart).

**Couche 2 — « Jules MCP » = serveur MCP côté client qui enveloppe l'API REST.** Il se configure dans le **client MCP** (Claude Desktop, Cursor, ChatGPT avec support MCP), jamais côté Google :
- **Officiel (Google Labs)** : paquet npm `@google/jules-mcp`, repo `google-labs-code/jules-sdk` (Apache-2.0, mention « not an officially supported Google product »), `packages/mcp/`. Config type :
  ```json
  { "mcpServers": { "jules": { "command": "npx", "args": ["@google/jules-mcp"], "env": { "JULES_API_KEY": "<api-key>" } } } }
  ```
  Source primaire : https://raw.githubusercontent.com/google-labs-code/jules-sdk/main/packages/mcp/README.md
- **Communautaires** : `CodeAgentBridge/jules-mcp-server` (Python/FastMCP, `uv run … jules_mcp/jules_mcp.py`, env `JULES_API_KEY`) ; `GatienBoquet/jules_mcp` (service HTTP persistant `127.0.0.1:3323/mcp`).
- **Alternative GitHub Actions** : `google-labs-code/jules-action` (input `jules_api_key` → header `X-Goog-Api-Key`) — pattern Actions sans MCP.

## 2 — Surface MCP effective (officielle, source primaire)

7 outils, 3 catégories (`packages/mcp/README.md`, repo `google-labs-code/jules-sdk` @ `19fc117`) :

| Outil | Rôle |
|---|---|
| `create_session` | Créer une session Jules (prompt + source GitHub optionnelle) |
| `list_sessions` | Lister les sessions récentes (pagination) |
| `get_session_state` | État : `busy`/`stable`/`failed`, prompt d'origine, dernière activité, dernier message, plan en attente |
| `send_reply` (= `send_reply_to_session`) | Envoyer un message ou approuver un plan en attente |
| `get_code_review_context` | Résumé des changements (fichiers + métadonnées) |
| `show_code_diff` | Patch unidiff complet |
| `query_cache` | Requêter le cache local (sessions + activités) en JQL |

Note : une source secondaire (deepwiki) annonçait « 9 outils » — la source primaire dit 7. Retenir 7.

**Limites connues :** le MCP n'ajoute aucune capacité au-delà de l'API REST qu'il enveloppe ; la clé reste le seul secret (1 clé = 1 identité Jules). Quotas du compte : free = 15 tâches/24 h, 3 concurrentes (source secondaire kie.ai — **non vérifié sur le compte du Capitaine**).

## 3 — Comment V4 déclenche les sessions Jules : REST direct, pas de MCP

**V4 n'utilise aucun MCP.** Le dispatch passe par l'Issue Factory en REST direct (`tools/issue_factory.py`, clone V4) :

- **Appel API** (`issue_factory.py:37-39`) : `request('https://jules.googleapis.com/v1alpha/' + path, os.environ['JULES_API_KEY'], data, google=True)` → header `X-Goog-Api-Key` (le flag `google=True` bascule `Authorization: Bearer` → `X-Goog-Api-Key`).
- **Création de session** (`issue_factory.py:206-211`) :
  ```python
  session = jules('sessions', {'title': 'ASpace build ' + ident,
      'prompt': prompt_for(issue, record, root), 'requirePlanApproval': False,
      'automationMode': 'AUTO_CREATE_PR',
      'sourceContext': {'source': source['name'], 'githubRepoContext': {'startingBranch': branch}}})
  ```
  → plans auto-approuvés, PR créée automatiquement, branche de départ = branche par défaut du repo.
- **Résolution de la source** (`issue_factory.py:55`, `198-201`) : `GET sources` puis match `owner/repo` ; état `BLOCKED` si « Jules GitHub App has no source for this repository ».
- **Garde-fous** : reçu R10 `CLAIMED` persisté **avant** le POST externe ; pas de re-dispatch aveugle (garde-fou `no-blind-redispatch`) ; format du reçu validé par regex `sessions/[A-Za-z0-9_-]+`.
- **Déclenchement** (`.github/workflows/issue-factory.yml`) : event `issues` labeled (label `factory:ready`), cron `11,41 * * * *`, `workflow_dispatch` (inputs `issue`, `recover_session`). Concurrency group `aspace-issue-factory`. Artefacts `factory-out/` uploadés (rétention 90 j).
- **Secret** (`issue-factory.yml:39`) : `JULES_API_KEY: ${{ secrets.JULES_API_KEY }}` (env du step). `gh secret list --repo Amdkn/Aspace_OS-V4` (2026-10-17) : secrets présents = `JULES_API_KEY` (MAJ 2026-10-07T11:30:36Z), `LABEL_PAT` (MAJ 2026-10-09T15:57:28Z).

## 4 — V3 : aucune session Jules réelle

- `gh secret list --repo Amdkn/Aspace_OS_V3` → **vide** (aucun secret Actions).
- `10_Tech_OS/kernel/jules_fleet_supervisor.py` utilise bien l'endpoint officiel (`X-Goog-Api-Key`, `OFFICIAL_ENDPOINT = "https://jules.googleapis.com/v1alpha"`), mais il n'est exécuté qu'en **tests unitaires** (`.github/workflows/kernel-continuity-ci.yml:85` : `python -m unittest test_jules_fleet_supervisor.py`) avec des clés factices (`test_jules_fleet_supervisor.py`).
- **V3 ne dispatche aucune session Jules réelle. Seul V4 (Issue Factory) le fait.**

## 5 — Où vit JULES_API_KEY : synthèse

| Repo | Secret | Origine | Usage |
|---|---|---|---|
| `Amdkn/Aspace_OS-V4` | `JULES_API_KEY` (secret Actions, MAJ 2026-10-07) | Clé créée dans Settings de jules.google.com par le Capitaine (max 3) | `issue-factory.yml:39` → `X-Goog-Api-Key` vers `jules.googleapis.com` |
| `Amdkn/Aspace_OS_V3` | aucun | — | superviseur en tests unitaires uniquement |

Si la clé doit servir hors Actions (MCP local, scripts) : **Secure Vault via le Capitaine — jamais d'extraction.**

## 6 — Ce qui reste non vérifié

1. **Page Settings de jules.google.com** : combien de clés actives (max 3), laquelle correspond au secret Actions, date de création — nécessite le navigateur du Capitaine, lecture seule.
2. **Repos couverts par la Jules GitHub App** : `GET /v1alpha/sources` listerait les sources accessibles — non appelé (pas de clé disponible, et ce serait la clé du Capitaine).
3. **Quotas réels du compte** (15 tâches/24 h en free — source secondaire, non vérifié).
4. **Routage effectif** : `agents/registry.json` liste `jules` dans les providers de routage (`codex`, `jules`, `hermes`) pour tous les profils agents ; le chemin réel vers Jules passe par l'Issue Factory — `tools/agent_mesh.py` mériterait une lecture pour le détail du routage (hors périmètre G-02, noté).
5. **Issue Factory rouge en boucle** (6 échecs le 2026-10-17, 03:24→05:44 UTC — cf. F-02) : les sessions Jules #61+ restent le seul trafic observé ; l'état de santé du dispatch est suivi par le heartbeat BedRock, pas ici.

## 7 — Points saillants pour le typage (Bill)

- **Le « MCP de Jules » n'est pas un chantier d'infrastructure** : c'est un pattern d'intégration client-side. Si A'Space veut piloter Jules depuis un assistant (Claude/Cursor), la pièce à configurer est `@google/jules-mcp` + clé via Secure Vault — pas jules.google.com, pas Google Cloud.
- **V4 a déjà son intégration Jules** (Issue Factory, REST direct) — le chantier éventuel porte sur la fiabilité du dispatch (rouge en boucle), pas sur la création d'une intégration.
- **V3 n'a rien à migrer côté Jules** (superviseur = tests uniquement).
- **Contrainte dure à reporter telle quelle dans le design Clara** : aucune valeur de secret ne transite hors GitHub Actions sauf via Secure Vault + Capitaine.
- **Doctrine « pas de faux choix binaires »** : ne pas demander au Capitaine « MCP ou REST ? » — l'analyse montre que REST est déjà en place (V4) et que le MCP est un ajout client-side optionnel ; le design Clara tranche sur pièces.
