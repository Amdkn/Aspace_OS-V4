// gateway/adapt.ts
// Traduit un gestionnaire de forme Web vers la forme Node — EXTRACTION
// telle quelle de `os/business/api/_agent/adapt.ts` (qualifié H-04), seul
// l'en-tête de provenance est ajouté.
//
// LE DEFAUT QU'IL CORRIGE. Les gestionnaires écrits en forme Web —
// `(request: Request)` qui rend une `Response` — invoqués en `(req, res)`
// par le runtime Node ne rendent jamais la main : personne n'appelle
// `res.end()`, la requête reste ouverte jusqu'à expiration.
//
// On garde donc les gestionnaires en forme Web — c'est la forme standard,
// la plus testable — et on les enveloppe ici.

import type { IncomingMessage, ServerResponse } from 'node:http'

type GestionnaireWeb = (request: Request) => Response | Promise<Response>

/** Reconstitue le corps de la requête. `IncomingMessage` est un flux : sans
 *  cette lecture, `request.json()` côté gestionnaire ne verrait rien. */
function lireCorps(req: IncomingMessage): Promise<Buffer | undefined> {
  const sansCorps = req.method === 'GET' || req.method === 'HEAD'
  if (sansCorps) return Promise.resolve(undefined)
  return new Promise((resolve, reject) => {
    const morceaux: Buffer[] = []
    req.on('data', (c: Buffer) => morceaux.push(c))
    req.on('end', () => resolve(Buffer.concat(morceaux)))
    req.on('error', reject)
  })
}

export function versNode(gestionnaire: GestionnaireWeb) {
  // Deux appelants, deux formes. Un serveur Node invoque `(req, res)` ; un
  // appelant Web invoque `(request)` et lit la `Response` rendue.
  return async function adapte(
    req: IncomingMessage | Request,
    res?: ServerResponse,
  ): Promise<void | Response> {
    if (!res || req instanceof Request) {
      return gestionnaire(req as Request)
    }
    try {
      const hote = req.headers.host ?? 'localhost'
      // Le protocole vient de l'en-tête posé par le proxy ; en local il manque.
      const schema = (req.headers['x-forwarded-proto'] as string | undefined) ?? 'https'
      const corps = await lireCorps(req)

      const entetes = new Headers()
      for (const [cle, valeur] of Object.entries(req.headers)) {
        if (valeur === undefined) continue
        entetes.set(cle, Array.isArray(valeur) ? valeur.join(', ') : valeur)
      }

      const requete = new Request(`${schema}://${hote}${req.url ?? '/'}`, {
        method: req.method ?? 'GET',
        headers: entetes,
        body: corps && corps.length > 0 ? corps : undefined,
      })

      const reponse = await gestionnaire(requete)

      const sortie: Record<string, string> = {}
      reponse.headers.forEach((v, k) => { sortie[k] = v })
      res.writeHead(reponse.status, sortie)

      if (!reponse.body) {
        res.end()
        return
      }

      // Le corps est un flux : on l'écoule morceau par morceau — c'est ce
      // qui fait diffuser la réponse au fil de l'eau au lieu d'attendre.
      const lecteur = reponse.body.getReader()
      for (;;) {
        const { done, value } = await lecteur.read()
        if (done) break
        res.write(Buffer.from(value))
      }
      res.end()
    } catch (err) {
      // Une erreur ici laisserait la requête ouverte — exactement le défaut
      // qu'on corrige. On répond, même mal.
      const message = err instanceof Error ? err.message : String(err)
      if (!res.headersSent) {
        res.writeHead(500, { 'Content-Type': 'application/json' })
      }
      res.end(JSON.stringify({ error: `Erreur interne : ${message}` }))
    }
  }
}
