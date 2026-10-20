# D-N029(b) — DeepSeek Harness : reçu d'enquête (2026-10-19)

**Décision S2** : Discussion #46, commentaire 19056049 — PROLONGER, en 2 temps.
**Échéance** : 2026-11-01. **Exécutant** : Ryan / Factory (13e Doctor).

## (i) Source officielle — IDENTIFIÉE ✓
- Repo : `github.com/deepseek-ai/deepseek-harness` (DeepSeek AI, MIT) — confirmé par sources multiples
  (dshbase.com, deepseekharness.io, springbrand.ai, datacamp.com, dev.to).
- Paquet npm : `@deepseek-ai/dsh` — cohérent avec le wrapper du repo V4
  (`os/agent/src/apps/DeepSeekHarness/index.tsx` : iframe `:3080`, remède `dsh web --port 3080`).
- → pas d'abandon sur le volet (i).

## (ii) Checks
1. **Install** : `npm install -g @deepseek-ai/dsh` → `@deepseek-ai/dsh@0.2.1-rc.2` installé
   (note : le lien `/usr/bin/dsh` n'a pas été créé par npm ; le binaire est appelé
   directement via `node /usr/lib/node_modules/@deepseek-ai/dsh/lib/bin.js`). ✓
2. **`dsh --version`** → `0.2.1-rc.2`. ✓
3. **`dsh web --port 3080`** → serveur démarré ; `/` → 401 sans auth (normal : le serveur
   exige le token imprimé au boot), puis **HTTP 200** après le handshake token→cookie standard. ✓
4. **Capacité exercée** : `dsh web --dump-config` → exit 0, 1229 lignes d'arbre de composition
   du profil (noyau Cordis : tool-plugin-manager, llm, session, typert, …) — le harnais a
   réellement composé et monté son profil. Reçu : `deepseek-dsh-dump-config.txt` (1229 lignes).

## Limite honnête
Un appel modèle outillé (tool_call) nécessiterait une clé API DeepSeek — non disponible
dans la factory. La preuve couvre : install depuis la source officielle + boot + serveur web 200
+ composition du profil exécutée. Pas d'appel modèle.

## Recommandation Factory (décision S2)
Les 3 conditions écrites par le Conseil sont remplies avec reçus
(source officielle / install+version / web 200 / capacité exercée = composition du profil).
**Recommandation : QUALIFIER** DeepSeek Harness (niveau `executed`) sur ces reçus —
sauf si le Conseil exige un appel modèle avec clé API (auquel cas : la clé est requise).

## Annexe — Prime Agent (constat 2026-10-19 ~21:53 EDT)
Enquête **bloquée-route** (pas abandonnée) : 13e Doctor vérifié — Tailscale installé mais non
connecté sur sa VM, aucun hôte SSH configuré ; le VPS est injoignable depuis toutes nos VMs.
Signalée au registre comme bloquée-route. Déblocage : le Capitaine expose le VPS
(Tailscale/SSH), ou routage via une route existante. Sans route au 2026-11-01, la décision S2
s'applique : « Si échec/inaccessible à l'échéance → ABANDONNER ».

## Annexe — Cube Farm (constat 2026-10-19 ~21:53 EDT, 13e Doctor, vérifié navigateur)
Enquête **bloquée-capacité** (budget Codespaces), PAS un échec de Cube Farm : le Codespace
« A-Space V4 Control Plane » n'est pas démarré (dernière utilisation il y a 9 jours), options
Start désactivées, GitHub : « You are out of monthly free usage or have exceeded your budget
for Codespaces ». Aucun des 3 checks n'a pu tourner — Cube Farm n'a jamais été atteint.
Déblocage : décision Capitaine (budget) ou reset mensuel — hors de nos routes.
