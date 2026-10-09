# SELECTORS.md — sélecteurs DOM muse.ai

> Rempli par inspection réelle du DOM.
> Règle du repo upstream : si un sélecteur dérive, échouer explicitement —
> jamais basculer silencieusement de transport.
>
> Source : capture DOM du Capitaine, 2026-10-09 (navigateur réel, chat « A0 Sandbox d'entraînement »).

## Session
- Connecté : oui (screenshot)
- Pattern d'URL d'un thread : `muse.ai/thread/<id>` (à confirmer)

## Sélecteurs

| Rôle | Sélecteur CSS | Fiabilité |
|---|---|---|
| Champ de saisie | `textarea[data-hatch-composer-prehydration-input="true"]` (fallback : `textarea[aria-label="Message"]`) | **stable** — attribut produit dédié, observé dans le DOM réel |
| Bouton d'envoi | `button[aria-label="Send"]` (ancre parente : `div[data-hatch-composer-action="send"]`) | **stable** — `aria-label="Send"` + attribut produit `data-hatch-composer-action="send"`, observés dans le DOM réel |
| Fil de conversation | <!-- à renseigner --> | |
| Message assistant en streaming | `[message-body="true"]` — prendre le **dernier** (`:last-child` / `.last()`) = le message le plus récent | **stable** — attribut produit dédié, observé dans le DOM réel (bulle interne : `div.hatch-chat-groupable-bubble`) |
| Fin de génération (détection) | `button[aria-label="Stop"]` présent = génère encore ; `div[data-hatch-composer-action="send"]` réapparu = terminé | **très stable** — le slot d'action bascule entre `send` ↔ `stop`, signal d'état binaire |
| Liste des side chats | `getByRole("button", { name: "<titre du chat>" })` — chaque chat est un bouton dont le nom accessible est son titre (observé : « A0 Sandbox d'entraînement », role=button) | **stable** — recherche par nom, pas par classe |
| Bouton nouveau chat | `button[aria-label="New side chat"]` | **stable** — observé dans le DOM réel |
| Indicateur de modèle | <!-- à renseigner, si visible --> |

## Notes
- Le champ de saisie est un `<textarea rows="1" aria-label="Message" placeholder="Message">`.
- L'attribut `data-hatch-composer-prehydration-input="true"` est le plus stable :
  spécifique au produit, pas une classe utilitaire Tailwind (celles-ci dérivent).
- **Découverte clé** : le slot d'action du composer bascule entre deux états —
  `div[data-hatch-composer-action="send"]` (prêt) ↔
  `div[data-hatch-composer-action="stop"]` (génère). C'est un signal d'état
  binaire, bien plus fiable que la disparition d'un bouton.
- Pattern d'URL confirmé : `muse.ai/thread/<chat-uuid>` — l'UUID du thread est
  l'identifiant du chat (vérifié : `3ced6d78-8a96-4a75-83ca-9b9efd8255c1`
  = ce chat « A0 Sandbox d'entraînement »).
