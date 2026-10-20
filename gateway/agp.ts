// gateway/agp.ts
// AGP — contrôle d'accès de la passerelle, appliqué aux routes.
// EXTRACTION du contrôle d'accès de
// `os/business/src/lib/tooling/adapters/agp.ts` (qualifié H-04) : le refus
// par défaut, le contrôle appliqué avant toute traduction/proxy. La
// traduction de protocoles de la brique (traduire/buildPasserelle, pensée
// pour les outils) est hors bornes D-N015 et n'est pas extraite.
//
// « Une passerelle qui laisse passer ce qui n'est pas nommé n'est pas une
// passerelle : c'est un trou avec une documentation. »
// Ici : seules les routes nommées dans REGLES_ROUTES sont proxées. Tout le
// reste de /api/* est refusé — y compris avec un jeton valide.

export interface RegleRoute {
  /** Motif de chemin autorisé. Une règle sans motif n'autorise rien. */
  motif: string
  methodes: string[]
}

/** Refus par défaut. Le motif `$^` ne peut correspondre à aucune chaîne. */
export const REGLE_VIDE: RegleRoute = { motif: '$^', methodes: [] }

/** Les routes nommées du gateway : le blackboard, et rien d'autre
 *  (D-N015 §0.5 — proxy frontal vers 127.0.0.1:4445, chemin préservé). */
export const REGLES_ROUTES: RegleRoute[] = [
  { motif: '^/api/blackboard(/.*)?$', methodes: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'] },
]

export function autoriserRoute(
  chemin: string,
  methode: string,
  regles: ReadonlyArray<RegleRoute> = REGLES_ROUTES,
): boolean {
  return regles.some(
    (r) => new RegExp(r.motif).test(chemin) && r.methodes.includes(methode),
  )
}
