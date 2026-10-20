# BOOK IT IT — README de projection fractale (prototype LD01)

> A3 parent : LD01 Career & Business (Book) · Domaine business : R&D & IT
> VP : Cyborg · Squad : Kang Dynasty (Kang Prime lead)
> Source : `20_Life_OS/22_Wheel_Discovery/LD01_Business_Book/01_Guides_Business/07_RD_et_IT.md`
> Corpus : 11 620 fichiers (~99 % de bruit ; canon ~40 fichiers). Porte 4 ADRs L0.

## Mission

Des loops vérifiables, observables, durables, avec humain-in-the-loop. **Le skill est
dans le harness, pas dans la loop.**

## Frameworks / processus clés

1. **3 primitives** : `/loop` (intervalle), `/goal` (critères done), `/routines` (scheduled).
2. **3 anti-patterns deal-breakers** : pas d'observability / pas de durability DB /
   pas de HITL par node = loop interdite.
3. **Archon** : YAML + orchestrator + workers isolés + Postgres (resume au crash) +
   per-node model choice = **-60 à -80 % sur workflows longs**.
4. **4 ADRs** : LOOP-001 (verification-first), LOOP-002 (queues-over-loops + HITL),
   LOOP-003 (Orient + Signals + Wagers), CORE-005 (state.local → Supabase).
5. **Stigmergie** : coordination via environnement partagé éditable par tous
   (grille de phéromones + évaporation), pas de messages inter-agents.

## Actifs

- Radar Top 10 AI Agent Tools (Agent Reach 193K stars, CUA, Agent Memory, Hermes…).
- **Skill Spector** (Nvidia) : 64 patterns × 16 catégories, score 0-100.
- **Niner** : router local 3-tier fallback (subscription → cheap → free).

## Reçu

- Per-node routing mesuré sur 7 jours.
- Skill Spector > 70 = publication bloquée.

## B1 de Coacher — À DÉFINIR (prochaine étape)
