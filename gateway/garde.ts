// gateway/garde.ts
// Portier du Gateway V4 — EXTRACTION de `os/business/api/_agent/garde.ts`
// (Business OS, qualifié H-04), composée pour le serveur standalone D-N015.
//
// Provenance et deltas (H-H04-1 : l'auth trace vers la brique ; la posture
// n'est pas réimplémentée, elle est reprise) :
//   - Posture reprise telle quelle : fermé par défaut, refus muet sur la
//     cause, plafond de corps vérifié avant lecture (TAILLE_MAX_CORPS,
//     verifierTaille — extrait sans changement).
//   - Delta D-N015 §0.2 : le jeton vit dans la variable GATEWAY_TOKEN
//     (la brique lisait AGENT_API_TOKEN, son contexte Vercel).
//   - Delta D-N015 G1 : jeton requis dans TOUS les modes. La brique ouvrait
//     le développement local quand le jeton manquait ; le gateway est le
//     frontal d'auth de V4 — un frontal ouvert « en dev » échouerait G1.
//     Fail-closed partout : oublier de poser le jeton coupe le service,
//     jamais ne l'ouvre.
//   - Delta D-N015 G3/G4 : comparaison en temps constant (timingSafeEqual
//     sur empreintes SHA-256 — longueurs toujours égales, aucun `===` sur
//     le jeton) et refus 401 strictement identique pour jeton absent ou
//     invalide : aucune fuite sur la cause.

import { createHash, timingSafeEqual } from 'node:crypto'

/** Taille maximale du corps accepté (extrait tel quel de la brique).
 *
 *  Sans plafond, un POST de 3 Mo de texte part au modèle et se paie. */
export const TAILLE_MAX_CORPS = 256 * 1024

export interface Refus {
  status: number
  message: string
}

/** Le seul refus d'auth, pour absence comme pour invalidité (G3). */
const REFUS_AUTH: Refus = { status: 401, message: 'Authentification requise.' }

/** Jeton serveur absent : muet sur la cause, comme la brique en production —
 *  dire ce qui manque renseignerait l'appelant sur la configuration. */
const REFUS_INDISPONIBLE: Refus = { status: 503, message: 'Service indisponible.' }

function empreinte(valeur: string): Buffer {
  return createHash('sha256').update(valeur, 'utf8').digest()
}

/** Rend `null` si la requête passe, ou le refus à renvoyer. */
export function verifierAcces(request: Request): Refus | null {
  const attendu = process.env.GATEWAY_TOKEN

  if (!attendu) {
    return REFUS_INDISPONIBLE
  }

  const entete = request.headers.get('authorization') ?? ''
  const presente = entete.startsWith('Bearer ') ? entete.slice(7).trim() : ''
  if (presente.length === 0) return REFUS_AUTH
  if (!timingSafeEqual(empreinte(presente), empreinte(attendu))) return REFUS_AUTH
  return null
}

/** Refuse un corps trop gros avant même de le lire (extrait tel quel).
 *
 *  `Content-Length` peut mentir ou manquer — c'est un premier filtre, pas
 *  une garantie. Le second filtre est la taille réelle après lecture. */
export function verifierTaille(request: Request): Refus | null {
  const brut = request.headers.get('content-length')
  if (!brut) return null
  const taille = Number(brut)
  if (Number.isFinite(taille) && taille > TAILLE_MAX_CORPS) {
    return { status: 413, message: 'Corps de requete trop volumineux.' }
  }
  return null
}
