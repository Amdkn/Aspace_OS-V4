# BEFORE YOU BUILD — Finalisation des Fondations Aspace

**Mission S1** : Rick (S1 · Délégation) — reçue d'A0 (main) le 2026-10-17 ~02:20 EDT, « go » du Capitaine.
**Chaîne lore** : Bill (Discover) → Clara (Design + Architecture des Design Systems) → Nardole (Dispatch) → validation Doctors (13e Kernel, 11e Life, 12e Buzz) → exécution par Compagnons nommés.
**Référence d'écart** : audit GitHub du 2026-10-17.

---

## 1. Objectif

Finaliser les Fondations d'Aspace **AVANT** le transfert V4.1. C'est le chantier sur lequel le Capitaine a perdu la semaine dernière sur GPT.

**Produit attendu** : des Fondations finalisées et **vérifiables** — chaque fondation a une preuve (test, reçu, check qui casse si c'est faux).

**HORS PÉRIMÈTRE** (missions suivantes, sur ordre du Capitaine uniquement) :
- Transfert V4.1 (tous les principes transférables de V3/V4, structurés et organisés)
- Structuration des Holons dans leur complétude
- Première incarnation (usage)
- Harnesses sur le VPS

---

## 2. Les deux chantiers

### Chantier 1 — Corpus des principes transférables

**Matière première** :
- Salvage ChatGPT en cours (lots C, D, E — Phase 1 : C partie 1/2 en cours ; Phase 2 : D registre 4 états, E IPBD via chaîne Bill→Clara→Nardole→Doctors)
- Takeout Gemini déjà disponible

**Séquencement** : le salvage se termine d'abord — c'est la matière. L'exécution du Chantier 1 démarre quand le corpus est complet.

**À qualifier par Bill** : état exact du corpus disponible, complétude, structure cible du corpus de principes, critères de « transférable », méthode d'extraction des principes depuis les transcriptions + IPBD.

### Chantier 2 — Autonomisation du BedRock L0

**Composants** (chacun avec preuve) :
1. **Ledger R10** — état actuel à qualifier (reçu G-20261009-009 existe ; fonctionnement ?)
2. **Supabase connecté** — DDL absent du code (audit) → à qualifier : ce qui existe, ce qui manque
3. **Gateway avec authentification** — rouge, D-N015, aucun design Clara (état 2026-10-12) → à qualifier
4. **CI réellement bloquante** — protection de branche active (verify ubuntu + windows requis) → à vérifier : bloque-t-elle vraiment ?
5. **Policy store versionné** — état à qualifier
6. **S3 Compagnons opérationnels** — 9 Compagnons nommés avec canaux (correction lore 2026-10-17) → à qualifier : qui est actif, qui manque

**Référence d'écart** (audit 2026-10-17) **corrigée par Discover Bill (2026-10-17)** :
- « Supabase DDL absent du code » est **FAUX** : `os/business/supabase/migrations/` (~20 fichiers), `os/life/supabase/migrations/` + `config.toml` existent. Ce qui manque : **preuve de connexion live** (sonde automatisée).
- « S3 Compagnons » : **9/9 chats existent** (structure OK) — mission = **réactivation**, pas recréation. Yaz = « interrupted » (inspecter en premier).
- Ledger R10 : mécanisme à l'arrêt (aucun reçu depuis 8 jours, aucune enforcement codée).
- Gateway + auth : part de zéro côté code (aucun code serveur). D-N015 existe au registre (ligne 61, assigné Clara depuis 2026-10-09 — encalminé 8 jours, relance en cours).
- CI bloquante : verte avec réserve (`enforce_admins=false`).
- Policy store : inexistant.

**À qualifier par Bill** : pour chaque composant, état réel vs état attendu, écart précis, preuve d'écart.

**Séquencement** : le Chantier 2 ne dépend pas du salvage — il peut avancer en parallèle dès que le design Clara est validé.

**ARBITRAGES CAPITAINE TRANCHÉS (2026-10-17 ~04:35 EDT, via A0) :**
- **A1 — Takeout Gemini : PAS de miroir workspace.** Drive est son PARA ; les archives récupérables vivent avec Data dans Life OS (`1hwj0LviT3JOwrp5fHvvKItGn9LW_oUtM`). Bill archive le Takeout en lecture seule, exactement comme l'extraction ChatGPT. Le routage capacitaire multi-dimensions (horizons vertical, diagonal, orthogonal) est le domaine de Nardole (Hyper Dispatcher, Router de l'Infini) ; Clara crée les systèmes depuis ces archives.
- **A2 — enforce_admins : reste à false.** Bypass owner conservé. Doctrine : capacité MAXIMALE dans orchestration déterministe (inverse du moindre privilège) ; le contrôle = l'organigramme + les reçus, pas le verrouillage. Le design F-02/L4 ne verrouille pas — il prouve l'intégrité par les reçus.

**Règle doctrine (2026-10-17) : PLUS DE FAUX CHOIX BINAIRES.** Ne jamais présenter un widget (a)/(b) réducteur au Capitaine — c'est « le plus gros symptôme de production de Slop IA ». Lui présenter l'analyse ; il arbitre dans son propre langage architectural.

**Mapping org :** 9 Compagnons en horizontal, Doctors en vertical, Rick (S1) en 3D, Red Code 4D temporalité/continuation avec A0.

---

## 3. Contraintes inviolables

- Rapports en français ; note vocale MP3 française par livraison.
- Lecture seule sur le compte ChatGPT (rien modifié, rien envoyé).
- **Pas d'écriture Linear sans instruction explicite du Capitaine.**
- GitHub/Drive : doctrine No Human Gate — les Doctors ont autorité sur le noyau. Si une autorisation vision du Capitaine est requise, remonter via A0 comme arbitrage vision, jamais en direct.
- Le Capitaine ne reçoit que l'arbitrage vision (via A0).
- Aucune exécution sans design Clara signé (chaîne lore).
- Chaque fondation livrée a une preuve vérifiable (test, reçu, check qui casse si faux).

---

## 4. Chaîne d'exécution

| Étape | Acteur | Livrable |
|---|---|---|
| Discover | Bill (Frameworks) | Missions typées par chantier : état réel, écarts, périmètre qualifié |
| Design | Clara (Décisions) | Plan borné + tests hold-out ÉCRITS AVANT exécution + Architecture des Design Systems |
| Dispatch | Nardole (Agora) | Assignation aux Compagnons nommés, suivi, routage |
| Validation | Doctors S2 (13e, 11e, 12e) | Validation du design avant exécution |
| Exécution | Compagnons nommés | Fondations + preuves |

**Séquencement d'exécution** (à affiner par Clara) :
- Chantier 2 (BedRock) : peut démarrer dès design validé (indépendant du salvage)
- Chantier 1 (Corpus) : démarre quand salvage (lots C, D, E) terminé

---

## 5. Critères d'acceptation (mission)

- [ ] Chaque composant du Chantier 2 a une preuve vérifiable (test/reçu/check).
- [ ] Le corpus du Chantier 1 est complet (salvage + Takeout intégrés) et structuré.
- [ ] Les principes transférables sont extraits avec critères explicites.
- [ ] Aucune fondation n'est déclarée « finalisée » sans preuve qui casse si c'est faux.
- [ ] Le transfert V4.1 peut démarrer sur ces fondations (mission suivante, non incluse).
