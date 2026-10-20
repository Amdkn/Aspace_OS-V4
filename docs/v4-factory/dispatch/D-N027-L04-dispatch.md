# Dispatch L04 — CI : intégrité prouvée par les reçus (D-N027, phase 2)

**Statut : PRÉPARÉ — à envoyer dès la clôture H-L06-3 tracée au registre (9/9).**
**Destinataire : 13e Doctor (Kernel) — autorité pleine sur le noyau, validateur F-02.**
**Référence design : `plans/FONDATIONS-F-02-plan-borne-bedrock-l0.md` §L04 (signé Clara).**

---

13e — Nardole, dispatch **D-N027 phase L04** (séquence L06 → **L04** → L02 → L01 → L05 → L03). H-L06-3 est clos (9/9 tracé au registre).

## Objet (bornes du plan signé)

**IN :**
1. **Job d'audit non-bypass** : pour chaque merge sur `main` (fenêtre glissante), vérifier que les checks requis étaient verts **avant** le merge (timestamps check-runs vs merge). Rôle : **transparence du trail** (qui a bypassé, quand) — bypass détecté → alerte visible et tracée. Tier D (pur code, comparaison de timestamps).
2. **Bypass documenté comme capacité délibérée** : la doc dit explicitement `enforce_admins=false`, bypass owner = capacité délibérée (capacité maximale, arbitrage Capitaine A2) — jamais « aucun bypass possible ».
3. **Intégrité par les reçus** : le check `r10-receipt` (L01) rejoint les checks requis — c'est lui qui bloque un merge sans reçu. Si le check existe déjà (factory/H-02-A1), le prouver ; sinon, l'enforcement complet atterrit avec L01 et L04 le prépare.

**OUT :** reconstruction de la CI ; verrouillage `enforce_admins` (écarté par arbitrage Capitaine A2). Ne pas refaire ce qui existe : on prouve et on documente, on ne reconstruit pas.

## Hold-outs à tester (AVANT de déclarer la phase)

| ID | Vérifie | Seuil |
|---|---|---|
| H-L04-1 | Protection intacte | `verify (ubuntu-latest)` + `verify (windows-latest)` requis sur `main` |
| H-L04-2 | Audit non-bypass vert | Job présent ; échantillon de merges récents : 100 % checks verts pré-merge (ou bypass tracés avec qui/quand) |
| H-L04-3 | Bypass documenté comme doctrine | La doc dit explicitement : `enforce_admins=false`, bypass owner = capacité délibérée, jamais « aucun bypass possible » |
| H-L04-4 | Intégrité par les reçus | Un merge sans reçu R10 est bloqué par le check `r10-receipt` (L01) — la preuve d'intégrité ne dépend pas du verrouillage GitHub |

Tout écart sur un hold-out → **BLOQUÉ avec raison** au registre, pas de contournement silencieux.

## Règles d'exécution

- Un exécutant à la fois (pas de swarm) ; tu décides l'exécution dans ta lane (délégation Graham/Ryan à ton jugement).
- Doctrine recovery/rescue (addendum L00) : retry technique auto ; 3 recoveries KO ou cale 2× sans crash → cas nommé, je réachemine, tu valides si changement de lane. « Une boucle ne se tait jamais. »
- **Point de processus D-N029 (consigné)** : l'acteur du merge attend le feu vert du relecteur.
- Reçu R10 attendu au registre à la clôture de la phase (mission D-N027/L04 + SHA), puis je dispatche L02.
