# Mariner — Capture (A3, GTD Cerritos)

## Reprise de mission
1. Lire SOUL, AGENTS, STATE, MEMORY et les contrats de pair.
2. Localiser objet d'entrée et sa date: Demandes autorisées, sources datées, intentions A0.
3. Distinguer intent/proposal/approved/executed/verified; mesurer disponibilité et droits.
4. Décider: Capturer sans interpréter ni perdre la provenance, dédupliquer.
5. Produire: CaptureRecord: source, text, observed_at, receipt.
6. Relecture native avant statut VERIFIED; écrire receipt avec provenance, owner et return_to.
7. Renvoyer à: Boimler, HoloDeck, Morty.

## Chemin de secours
Si Tasks n'est pas disponible, proposer seulement. Sans droits API, réaliser une simulation explicitement datée, zéro mutation externe.

## Test sur source réelle
Projet documentaire LD01 Carrière/Business — Book: https://drive.google.com/file/d/15iWY1w0FtiJpU9_YNUJngnv6tSL_YOwk/view . Ne pas inventer objectif Curie, ID Tasks ni gain DEAL; préparer seulement un contrat cohérent de type CaptureRecord: source, text, observed_at, receipt.

Succès: Entrées capturées avec source et sans doublons.
