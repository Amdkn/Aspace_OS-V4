# D-N029(b) — Prime Agent : reçus des checks (1)/(2)/(3) — 2026-10-20

**Hôte** : Umbrel du Capitaine (tailnet, SSH clé publique — user `umbrel`, Debian 13).
**Cadre** : autorisation INVARIANT du Capitaine (jonction + installation), inscrite au dossier
`prime-agent-route-evaluation.md`. Persistance : installation sous le domicile utilisateur,
qui repose sur `/dev/sda6` (partition persistante, montée sur `/home` ET `/data`, 59G libres).
La cible littérale `/data` est root (lecture seule pour `umbrel`, sudo à mot de passe) —
la persistance visée est obtenue par la même partition physique.

## Check (1) — Installation + version + help ✅

- Script officiel (URL vérifiée par le Capitaine le 2026-08-24) récupéré et **lu avant
  exécution** (3 251 lignes, installeur Rust : lanceur `~/.local/bin/prime-agent`, charge
  utile `~/.local/share/prime-agent/`).
- Exécution : la connexion SSH a coupé à ~30 s (VM affamée CPU — soft lockups connus) ;
  état vérifié AVANT tout nouvel essai → installation **terminée côté serveur**
  (binaire + charge utile datés du run).
- `prime-agent --version` → **`0.10.0`**.
- `prime-agent --help` → capturé. Modes vérifiés : `--mode <text|json|rpc|acp|daemon>`.
  La sous-commande de lancement persistant laissée « À CONFIRMER » dans l'unité du repo
  (`prime-agent run`, non vérifiée) est corrigée par le fait : c'est **`--mode daemon`**.

## Check (2) — Mode ACP confirmé contre la doc officielle ✅ (3 niveaux)

- **Documenté** : repo officiel `PrimeIntellect-ai/prime-agent`, `crates/pa-daemon/README.md`
  (« ACP stdio transport (`acp`) ») + `.changes/acp-session-flags.md`.
- **Installé** : `--help` du binaire 0.10.0 liste `acp` dans `--mode`.
- **Exécuté** : voir l'appel routé du check (3).
→ La « PISTE NON VERIFIEE (aperçu IA) » du registre est close : le mode ACP est réel.

## Check (3) — Service systemd + appel routé avec reçu ✅

- Unité **utilisateur** `~/.config/systemd/user/prime-agent.service`
  (`ExecStart=%h/.local/bin/prime-agent --mode daemon`, `Restart=on-failure`) — aucun sudo
  requis. `systemctl --user enable --now` → **active (running)**, Main PID 487916,
  démarrée le 2026-10-20 05:33:34 UTC, stable (vérifiée à +65 s, journal propre).
- **Appel routé (ACP, stdio)** — requête `initialize` JSON-RPC envoyée à
  `prime-agent --mode acp --no-session`, réponse reçue :
  `{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":1,"agentCapabilities":{"loadSession":false,"promptCapabilities":{"image":true,"embeddedContext":true},"mcpCapabilities":{"http":true},"sessionCapabilities":{"close":{}}},"agentInfo":{"name":"prime-agent","title":"Prime Agent","version":"0.10.0"},"_meta":{"ai.primeintellect.prime-agent":{}}}}`
  → le daemon répond sur sa surface protocole. **Reçu conservé (cette ligne).**

## Limites honnêtes

- `prime-agent status` / `prime-agent doctor` renvoient « No background services found »
  alors que systemctl montre le service actif : le suivi de socket du CLI diffère du daemon
  lancé par systemd. Les preuves substantielles sont systemctl (actif) + l'appel ACP (répondu).
- Aucun appel **modèle** (prompt) : aucun fournisseur d'inférence n'est configuré (clé ou
  abonnement requis). L'appel exécuté est au niveau protocole (initialize ACP).
- Redémarrage machine : l'unité est `enabled` (démarre à l'ouverture de session utilisateur) ;
  un démarrage sans login exigerait `loginctl enable-linger` (sudo, mot de passe du Capitaine).
- Santé VM : soft lockups CPU connus — le daemon tourne (66M, stable pendant l'enquête).

## Recommandation Factory (décision S2)

Les 3 checks de la décision écrite sont exécutés avec reçus : installation depuis la source
officielle, `--mode acp` confirmé par la doc ET le binaire ET l'appel, service actif,
appel routé répondu. **Recommandation : QUALIFIER Prime Agent (niveau `executed`)** —
au Conseil de confirmer ; la Factory ne touche pas le registre sans sa décision.
