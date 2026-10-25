# ÉTAT COURANT — Bill ↔ Tilly : six vidéos identifiées

Manifest actuel : [video_manifest.json](video_manifest.json). Six URLs confirmées : cinq dans le [Takeout YouTube](https://docs.google.com/spreadsheets/d/1AEKge1Cr3GSfF_ciakAZt6P43kuPIHmL9O3QbgTJ__w/edit) aux lignes 52, 142, 253, 260, 1426 ; la sixième sur la page publique de Tinker Tut.

**Preuve disponible :** identité/source des six vidéos et classement initial par métadonnées ou résumés publics. **Non prouvé :** lecture intégrale des six transcripts, déploiement, expérimentation ou réduction du temps A0.

| # | Vidéo | Contribution envisagée | Provenance |
|---|---|---|---|
| 01 | [Stop coding, build Software Factories instead](https://www.youtube.com/watch?v=ZHOmBeMNbnc) | LD04 / Tech Factory — triggers, reviews et réduction de coordination | Takeout ligne 52 |
| 02 | [How I Build AI Teammates With Claude Code — Grok Bot Clone](https://www.youtube.com/watch?v=mQBuZ6Dp0u0) | LD04 / Tech — poste worker, interface et persistance | Takeout ligne 142 |
| 03 | [How 3D Logistics Simulations Work](https://www.youtube.com/watch?v=Lt8XH8HJU_M) | LD07 MC Sandbox + LD06 Habitat — visualisation 3D et gestion d'état | Takeout ligne 253; titre seulement |
| 04 | [Spynel — manage ALL of your AI work with one chat](https://www.youtube.com/watch?v=-dq5PkLdAZ0) | LD04 / Rick-Nardole-Rory — canal unique, travail durable | Takeout ligne 260, source GitHub publique |
| 05 | [My Smart Home Digital Twin](https://www.youtube.com/watch?v=7PLKOz3gHSA) | LD06 Famille/Présence, G1 Habitat — floorplan, capteurs et commandes | Page YouTube publique; pas dans les lignes Takeout consultées |
| 06 | [Il a laissé l'IA gérer sa vie pendant 6 mois](https://www.youtube.com/watch?v=SeQXCpZhbjc) | LD04 / A0 et LD03 — usages rapportés, mesurer résultats | Takeout ligne 1426, entretien |

## Collaboration réciproque et reprise
Tilly LD04 définit la question de connaissance et accepte une pratique observable. Bill, sous Doctor12, extrait sources/risques, sépare récit, démonstration, code et résultat. Graham conserve provenance, Geordi indexe sans cloner; E1 → E2/PRD Flash → E3/PRD Avengers transforme uniquement une piste approuvée en exercice mesurable.
Champs de reprise : video_id, source_ref, timestamp, transcript_ref_or_unknown, claim_class, potential_reuse, acceptance, proof, return_to. Ne pas refaire rechercher les six IDs à A0; demander seulement une exception d'autorité effective. Sources et statuts : SOH-148, SOB-13, architecture/cross_os_collaboration.json.

## HISTORIQUE ANTERIEUR — état des références avant récupération

# Bill ↔ Tilly — pilote documentaire et reprise

La consigne référence six vidéos déjà fournies. L'inventaire original URL/titres/transcriptions n'a pas été retrouvé dans les sources consultables. Le [manifest](video_manifest.json) contient six entrées distinctes, état **UNRESOLVED**. Une seule transcription a été résumée dans le retour Astra cité par l'utilisateur, mais le titre, l'URL et le fichier source n'ont pas été confirmés. Aucun des six slots n'est déclaré traité.

**Question LD04 :** Quels usages d'agents améliorent effectivement la cognition, l'apprentissage et le temps de coordination sans promettre un effet réel sur la foi d'une démonstration ? Propriétaire de l'acceptation : Tilly. Bill qualifie les vidéos, Graham leur provenance et la mémoire, Geordi les références réutilisables. E1 puis E2/PRD Flash et E3/PRD Avengers peuvent tester un exercice ou outil seulement si une demande contextualisée existe.

**Six usages rapportés dans l'entretien, et non six vidéos distinctes :** centralisation/brief quotidien ; programme sportif adapté LD03 ; mémoire vocale et recherche documentaire ; réponses automatiques à périmètre borné ; réparation documentaire guidée par commentaire factuel ; extraction de thèmes des transcriptions et commentaires YouTube. Ce sont des hypothèses à étudier, non des gains mesurés.

**Protocole Bill :** retrouver les IDs d'origine, ajouter titre/URL/horodatage/transcript et droit de réemploi, distinguer récit/démonstration/test, produire un Discovery Packet, joindre au registre Geordi et retour à Tilly. Tilly choisit une mise en pratique concrète ou note UNKNOWN. Les objets SOH-148 et SOB-13 sont les ancrages de suivi, sans créer de mission parallèle ni déclarer de runtime actif.

**Packet de retour minimal :** question, source_ref, provenance, point vérifiable, risque, alternative, learning_action, acceptance_method, observed_effect_or_unknown, evidence_refs, next_question, return_to. État actuel : DOCUMENTARY_INTAKE_ONLY.


## Progrès sourcé sur VIDEO-01 (15 octobre 2026) — une transcription secondaire accessible

Un [transcript horodaté tiers consultable de la vidéo de David Ondrej](https://moderncreator.app/2026-10-11-david-ondrej-stop-coding-build-software-factories-instead) permet maintenant une **revue ciblée de passages**, indépendamment de la liste Takeout; ne pas le présenter comme une extraction native de sous-titres YouTube ou la lecture des six vidéos. L'index du transcript et les passages autour de **11:00–16:40** (lancement d'une boucle et mesure), **17:32–18:04** (déclencheur et contexte/outils), **19:15–20:17** (dépendance au laptop), **50:35–56:30** (démonstration de boucle) distinguent argument du créateur et méthode proposée.

**Hypothèse transférable pour Tilly / Bill, pas preuve A'Space :** une mission doit avoir trigger explicite, objet natif, capacité/outils, décision située, vérification indépendante et return_to. **Première expérimentation réversible proposée** : rejouer la consultation de SOH-148 dans `tools/holon_route.py --cases`, puis le reçu `tools/handoff_compiler.py` dans les outils déjà présents; comparer sur 2 reprises le nombre de relances A0, erreurs et temps de reprise. Si aucune autorité/owner fiable, état UNKNOWN plutôt que déclenchement d'une flotte. Le test du routeur est logiciel; l'essai inter-session avec bénéficiaire reste à réaliser.

**Grade de preuve :** `SECONDARY_TIMECODED_SOURCE_PARTIALLY_REVIEWED` pour VIDEO-01. Le manifest conserve `transcript_ref=null` tant qu'un fichier transcript identifié et contrôlé n'est pas ingéré comme preuve native; `full_transcripts_ingested=0`, `validated_real_world_outcomes=0`. Les cinq autres vidéos restent à ce stade au grade métadonnées.


## Périmètre élargi — corpus personnel et sens (15 octobre 2026)

Ce dossier de **six vidéos techniques** conserve son histoire, mais ne définit plus à lui seul la mission Bill–Tilly. Celle-ci inclut aussi culture, divertissement, humour, musique, fiction, corrections, prompts, annotations et sources quotidiennes, même sans utilité architecturale. Aucun contenu ne doit être rejeté parce qu'il ne produit pas de ROI; aucune classification Life, Business ou Tech n'est obligatoire. Le cas culturel récent à quatre timecodes est consigné dans le **registre IPBD privé A0 existant**, non dupliqué dans GitHub. Il est extérieur à la copie Takeout du 12 oct. et doit être réconcilié par ID de source, sans supprimer ses annotations.

Contrat de passage: `tools/corpus_meaning.py`. Conserver indépendamment source, passage, horodatage, voix de la source, commentaires utilisateur, interprétation du modèle, correction explicite, relation chronologique et éventuel usage. Un jeu de mots qui évolue n'est ni une instruction métier ni une affirmation factuelle. Une correction de l'auteur demeure attachée à la proposition qu'elle corrige, sans effacement. Les éléments audio/commentaires non retrouvés sont UNKNOWN, pas « transcrits » par Gemini.

**Rattrapage IPBD source:** MonActivite.html Gemini est le corpus primaire; les fichiers mensuels et synthèses servent au repérage, non au statut de vérité. L'index privé annonce 19 mois / 3694 échanges ; un rapport ancien annonçait 4054 entrées brutes, métriques distinctes à réconcilier. La première tranche a inspecté des prompts de mars et août et des sorties de modèle d'octobre, pas 3694 intentions ni une lecture exhaustive. Les rapprochements restent dans le registre IPBD A0 préexistant. B1–I1 (directions Jerry) et les huit fonctions L2 de *chacun* sont deux axes, jamais fusionnés.

**Valeur visée:** retrouver pourquoi une personne a écrit/corrigé une expression, ainsi que son évolution; et reconstituer une IPBD depuis plusieurs prompts avec provenance et prise en charge, sans en fabriquer une nouvelle à chaque occurrence. Bill qualifie source/passage, Graham conserve les versions et corrections, Geordi indexe, Tilly examine la fidélité du sens; autres A3 conseillent si demandés. Un autre harness ne peut revendiquer une reprise indépendante qu'après avoir lu le registre privé sous autorité, restitué une correction sans paraphrase inventée et reçu un readback.
