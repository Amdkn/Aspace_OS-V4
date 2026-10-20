# BEFORE YOU BUILD — Fork Pixel Agents → harness-agnostic (première surface d'Amy dans l'IDE)

**Mission S1** : Rick (S1 · Délégation) — reçue d'A0 (main) le 2026-10-17 ~06:16 EDT, « go » du Capitaine.
**Chaîne lore** : Bill (Discover) → Clara (Design + Architecture des Design Systems) → Nardole (Dispatch) → validation **11e Doctor** (Amy = Interfaces, son périmètre) → exécution par Compagnons nommés.

---

## 1. Vision

Forker l'extension **Pixel Agents** (pablodelucca — le bureau pixel-art qui rend les agents Claude Code vivants dans l'IDE) et la rendre **agnostique à n'importe quel harness** :
- Plus seulement Claude Code : les **9 Compagnons** (S1/S2/S3), **Jules**, les harnesses locaux (**Umbrel/VPS**).
- C'est la **première surface d'interface d'Amy dans l'IDE** (Antigravity, marketplace Open VSX).

## 2. Points Discover obligatoires (Bill)

1. **Licence** — le badge marketplace affiche « license: invalid ». Clarifier la licence réelle du repo **avant tout fork**. Pas de fork sans base légale claire. Si la licence interdit le fork ou est ambiguë → arbitrage vision via A0 avant de continuer.
2. **Architecture de détection** — comment l'extension détecte les agents (process terminaux ? hooks ? polling ?). C'est le point d'ancrage de la couche d'adaptation harness-agnostique.
3. **Interface d'adapteur** — définir le contrat : détection, états (actif/idle/erreur/terminé), identité du harness. **Un adapteur par harness, l'UI pixel ne connaît que l'interface.**

## 3. Design (Clara)

- **Couche d'adapteurs** + **registre de harnesses** (découverte dynamique).
- **9 harnesses cibles** (scope Capitaine 2026-10-17) : Antigravity CLI, Hermes, OpenClaw, Spacebot, Prime Agents, Pi coding agent, Codex CLI, Claude, DeepSeek harness.
- **Fait d'architecture** : le Capitaine alimente ces harnesses avec son agrégateur de milliards de tokens gratuits mensuels (multi-providers). Le contrat d'adapteur prévoit l'identité et la comptabilité par harness (traçabilité) **sans** système de facturation (ressort du Capitaine).
- Livrable : **VSIX installable dans Antigravity**.
- **Critère d'acceptation** : brancher un deuxième harness (non-Claude Code) **sans toucher à l'UI**.

## 4. Contraintes inviolables

- **Pas de fork sans licence clarifiée** (point 1 = gate).
- Rapports en français ; note vocale MP3 française par livraison.
- Pas d'écriture Linear sans instruction explicite du Capitaine.
- Le Capitaine ne reçoit que l'arbitrage vision (via A0).
- Aucune exécution sans design Clara signé.
- Règle doctrine : plus de faux choix binaires.

## 5. Hors périmètre

- Le design des interfaces Amy au-delà de cette première surface (missions suivantes).
- La publication sur les marketplaces (décision de distribution = arbitrage vision ultérieur si requis).
