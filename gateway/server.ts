// gateway/server.ts
// Gateway V4 — frontal d'authentification (D-N015 ; méthode H-04 :
// extraction-composition). Compose garde.ts (auth fail-closed), agp.ts
// (routes nommées, refus par défaut) et adapt.ts (forme Web → Node) en
// serveur standalone. Zéro dépendance : Node >= 22, TypeScript natif.
//
// Bind 127.0.0.1 uniquement — machine de confiance (W03-H04 : aucune
// exposition élargie tant que H-H04-3 n'est pas vert). Port 4440
// (os/PORTS.md). Le bridge Life→Business (3001) reste hors gateway (🛡).

import { createServer } from 'node:http'
import { versNode } from './adapt.ts'
import { verifierAcces, verifierTaille } from './garde.ts'
import { autoriserRoute } from './agp.ts'

const PORT = Number(process.env.GATEWAY_PORT ?? 4440)
const HOTE = '127.0.0.1'
const BLACKBOARD_URL = process.env.BLACKBOARD_URL ?? 'http://127.0.0.1:4445'

/** Origines CORS explicites (env GATEWAY_CORS_ORIGINS, séparées par des
 *  virgules). Liste vide par défaut : aucune origine n'est autorisée. */
const ORIGINES_AUTORISEES = new Set(
  (process.env.GATEWAY_CORS_ORIGINS ?? '')
    .split(',')
    .map((o) => o.trim())
    .filter((o) => o.length > 0),
)

function json(
  corps: Record<string, unknown>,
  status = 200,
  entetes: Record<string, string> = {},
): Response {
  return new Response(JSON.stringify(corps), {
    status,
    headers: { 'Content-Type': 'application/json', ...entetes },
  })
}

/** CORS restreint (D-N015 §0.4) : l'origine n'est renvoyée que si elle est
 *  nommée dans l'env. Jamais d'origine générique en présence d'auth ; une
 *  origine non listée ne reçoit aucun en-tête — le navigateur bloque. */
function entetesCors(request: Request): Record<string, string> {
  const origine = request.headers.get('origin')
  if (!origine || !ORIGINES_AUTORISEES.has(origine)) return {}
  return {
    'Access-Control-Allow-Origin': origine,
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
    Vary: 'Origin',
  }
}

/** Proxy frontal vers le blackboard (chemin préservé). Le jeton du gateway
 *  ne fuit pas vers le service interne : l'en-tête d'autorisation est retiré
 *  avant transmission — le blackboard est derrière le frontal, pas à côté. */
async function proxer(request: Request, url: URL): Promise<Response> {
  const cible = `${BLACKBOARD_URL}${url.pathname}${url.search}`
  const entetes = new Headers(request.headers)
  entetes.delete('host')
  entetes.delete('authorization')
  const init: RequestInit = { method: request.method, headers: entetes }
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    init.body = await request.arrayBuffer()
  }
  try {
    return await fetch(cible, init)
  } catch {
    return json({ error: 'Service interne injoignable.' }, 502)
  }
}

async function gestionnaire(brut: Request): Promise<Response> {
  const url = new URL(brut.url)
  const chemin = url.pathname
  const cors = entetesCors(brut)

  let reponse: Response
  if (chemin === '/health') {
    // Ouvert, sans aucune donnée métier (G8) : deux clés, rien d'autre.
    reponse = json({ status: 'ok', time: new Date().toISOString() }, 200, cors)
  } else if (chemin.startsWith('/api/')) {
    if (brut.method === 'OPTIONS') {
      // Préflight : répondu uniquement pour les origines nommées — un
      // navigateur n'envoie pas d'autorisation sur un préflight.
      reponse = Object.keys(cors).length > 0
        ? new Response(null, { status: 204, headers: cors })
        : json({ error: 'Origine non autorisee.' }, 403)
    } else {
      const refus = verifierTaille(brut) ?? verifierAcces(brut)
      if (refus) {
        reponse = json({ error: refus.message }, refus.status, cors)
      } else if (!autoriserRoute(chemin, brut.method)) {
        // AGP : ce qui n'est pas nommé n'est pas proxé — même avec jeton.
        reponse = json({ error: 'Route inconnue.' }, 404, cors)
      } else {
        const amont = await proxer(brut, url)
        const entetes = new Headers(amont.headers)
        for (const [k, v] of Object.entries(cors)) entetes.set(k, v)
        reponse = new Response(amont.body, { status: amont.status, headers: entetes })
      }
    }
  } else {
    reponse = json({ error: 'Route inconnue.' }, 404, cors)
  }

  // Log d'accès minimal : quand, méthode, route, statut. Aucun secret,
  // aucun corps, aucun en-tête d'autorisation.
  console.log(`${new Date().toISOString()} ${brut.method} ${chemin} -> ${reponse.status}`)
  return reponse
}

const serveur = createServer(versNode(gestionnaire))
serveur.listen(PORT, HOTE, () => {
  console.log(`Gateway V4 listening on http://${HOTE}:${PORT} (proxy -> ${BLACKBOARD_URL})`)
})
