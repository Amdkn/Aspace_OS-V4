/**
 * Authority Envelope - Constitutional safety primitives for factory execution.
 *
 * V4 inter-harness governance module implementing:
 * - AuthorityEnvelope: the complete governance container
 * - Lease: with fencing token for lifecycle management
 * - Budget: caps on resource consumption
 * - Evidence: append-only log of decisions/actions
 *
 * Immutable and serializable. No external dependencies.
 */

import { createHash } from 'node:crypto'

// ============================================================================
// Fencing Token
// ============================================================================

/**
 * A fencing token prevents reuse of a stale/dead lease.
 * A restarted process cannot reuse a dead lease.
 */
export interface FencingToken {
  token: string
  issuedAt: string
}

/** Create a new fencing token with fresh timestamp */
export function newFencingToken(): FencingToken {
  const timestamp = new Date().toISOString()
  const token = [...Array(16)].map(() => Math.random().toString(36)[2]).join('') + '-' + timestamp.replace(/[:.-]/g, '')
  return { token, issuedAt: timestamp }
}

/** Validate a fencing token format */
export function validateFencingToken(token: FencingToken): boolean {
  if (!token.token || token.token.length < 8) return false
  if (!token.issuedAt) return false
  try {
    new Date(token.issuedAt) // validate ISO format
    return true
  } catch {
    return false
  }
}

// ============================================================================
// Lease
// ============================================================================

/**
 * A lease with fencing token, deadline, and optional promotion metadata.
 * A stale/fenced-out lease MUST be rejected when it tries to act.
 */
export interface Lease {
  leaseId: string
  fencingToken: FencingToken
  issuedAt: string
  deadline?: string | null
  promotionId?: string | null  // None = permanent lease, set for temp promotion
}

/** Create a new lease with fresh fencing token */
export function newLease(options?: {
  leaseId?: string
  promotionId?: string
  ttlSeconds?: number
}): Lease {
  const now = new Date().toISOString()
  const deadline = options?.ttlSeconds ? new Date(Date.now() + options.ttlSeconds * 1000).toISOString() : null
  return {
    leaseId: options?.leaseId ?? crypto.randomUUID(),
    fencingToken: newFencingToken(),
    issuedAt: now,
    deadline: deadline,
    promotionId: options?.promotionId ?? null
  }
}

/** Check if a lease is expired */
export function isLeaseExpired(lease: Lease, at: string = new Date().toISOString()): boolean {
  if (!lease.deadline) return false
  return at >= lease.deadline
}

/**
 * Check if a lease is valid with the given fencing token.
 * A fenced-out stale lease MUST be rejected.
 */
export function checkLeaseValidity(lease: Lease, fencingToken: string, at?: string): boolean {
  if (lease.fencingToken.token !== fencingToken) return false
  return !isLeaseExpired(lease, at)
}

// ============================================================================
// Budget
// ============================================================================

/** Error thrown when budget is exceeded */
export class BudgetExceededError extends Error {
  constructor(public readonly attempted: number, public readonly limit: number) {
    super(`Budget exceeded: attempted ${attempted} > limit ${limit}`)
    this.name = 'BudgetExceededError'
  }
}

/**
 * A budget cap for resource consumption.
 * An action over budget is rejected.
 */
export interface BudgetData {
  limit: number
  spent: number
  currency: string
}

export interface Budget extends BudgetData {
  remaining: number
  isExhausted: boolean
}

/** Create a new budget */
export function newBudget(limit: number, spent: number = 0, currency: string = 'token'): Budget {
  const remaining = Math.max(0, limit - spent)
  return {
    limit,
    spent,
    currency,
    remaining,
    isExhausted: spent >= limit
  }
}

/** Check if action would fit in budget, throws if not */
export function checkBudget(budget: Budget, cost: number): void {
  if (budget.remaining < cost) {
    throw new BudgetExceededError(budget.remaining + cost, budget.limit)
  }
}

/** Add cost to budget, returns new budget or throws */
export function chargeBudget(budget: Budget, cost: number): Budget {
  checkBudget(budget, cost)
  return newBudget(budget.limit, budget.spent + cost, budget.currency)
}

// ============================================================================
// Evidence Record
// ============================================================================

/** An entry in the append-only evidence log */
export interface EvidenceRecord {
  operationId: string
  evidenceRefs: string[]
  recordedAt: string
  authority: string
  checksum: string
}

/** Create hash for stable identification */
function stableHash(value: string): string {
  return createHash('sha256').update(value, 'utf8').digest('hex').slice(0, 16)
}

/** Create a new evidence record with deterministic checksum */
export function newEvidenceRecord(
  operationId: string,
  evidenceRefs: string[],
  authority: string,
  previousChecksum: string = ''
): EvidenceRecord {
  const content = `${previousChecksum}${operationId}:${evidenceRefs.sort().join(',')}:${authority}`
  const checksum = stableHash(content)
  return {
    operationId,
    evidenceRefs: [...evidenceRefs],
    recordedAt: new Date().toISOString(),
    authority,
    checksum
  }
}

// ============================================================================
// Authority Envelope
// ============================================================================

/**
 * The authority envelope for inter-harness governance.
 * Contains all constitutional safety primitives for a work item.
 */
export interface AuthorityEnvelope {
  workId: string
  missionId: string
  operationId: string
  correlationId: string
  lease: Lease
  budget: Budget
  evidence: EvidenceRecord[]
  returnTo: Record<string, unknown> | null
}

/** Create a new authority envelope */
export function newAuthorityEnvelope(options: {
  workId: string
  missionId: string
  operationId: string
  lease: Lease
  budget: Budget
  correlationId?: string
  returnTo?: Record<string, unknown> | null
}): AuthorityEnvelope {
  return {
    workId: options.workId,
    missionId: options.missionId,
    operationId: options.operationId,
    correlationId: options.correlationId ?? crypto.randomUUID(),
    lease: options.lease,
    budget: options.budget,
    evidence: [],
    returnTo: options.returnTo ?? null
  }
}

/** Serialize envelope to JSON string (losslessly) */
export function serializeEnvelope(envelope: AuthorityEnvelope): string {
  return JSON.stringify(envelope, null, 2)
}

/** Deserialize envelope from JSON string */
export function deserializeEnvelope(json: string): AuthorityEnvelope {
  const parsed = JSON.parse(json)
  // Ensure nested objects are properly typed
  return {
    workId: parsed.workId,
    missionId: parsed.missionId,
    operationId: parsed.operationId,
    correlationId: parsed.correlationId,
    lease: parsed.lease as Lease,
    budget: parsed.budget as Budget,
    evidence: (parsed.evidence ?? []) as EvidenceRecord[],
    returnTo: parsed.returnTo
  }
}

/**
 * Append a new evidence record to the envelope.
 * Returns new envelope (immutable pattern).
 */
export function appendEvidence(
  envelope: AuthorityEnvelope,
  operationId: string,
  evidenceRefs: string[],
  authority: string
): AuthorityEnvelope {
  const previousChecksum = envelope.evidence.length > 0
    ? envelope.evidence[envelope.evidence.length - 1].checksum
    : ''
  const newRecord = newEvidenceRecord(
    operationId,
    evidenceRefs,
    authority,
    previousChecksum
  )
  return {
    ...envelope,
    evidence: [...envelope.evidence, newRecord]
  }
}

/** Check if envelope's lease is still valid (not expired, not fenced out) */
export function isLeaseValid(envelope: AuthorityEnvelope, at?: string): boolean {
  return checkLeaseValidity(envelope.lease, envelope.lease.fencingToken.token, at)
}

/** Check if envelope's budget has capacity for action */
export function isBudgetAvailable(envelope: AuthorityEnvelope, cost: number): boolean {
  return envelope.budget.remaining >= cost
}

/**
 * Validate envelope for use.
 * Checks lease validity, budget, and evidence integrity.
 */
export function validateEnvelope(envelope: AuthorityEnvelope, actionCost: number): {
  valid: boolean
  errors: string[]
} {
  const errors: string[] = []

  // Check lease validity
  if (!isLeaseValid(envelope)) {
    errors.push('Lease expired or fenced out')
  }

  // Check budget
  try {
    checkBudget(envelope.budget, actionCost)
  } catch (e) {
    if (e instanceof BudgetExceededError) {
      errors.push(e.message)
    } else {
      errors.push(`Budget check failed: ${e}`)
    }
  }

  // Verify evidence is append-only (by checksum chain)
  const latestChecksum = envelope.evidence.length > 0
    ? envelope.evidence[envelope.evidence.length - 1].checksum
    : ''

  let expectedPrev = ''
  for (const record of envelope.evidence) {
    const content = `${expectedPrev}${record.operationId}:${record.evidenceRefs.sort().join(',')}:${record.authority}`
    const expected = stableHash(content)
    if (record.checksum !== expected) {
      errors.push(`Evidence checksum mismatch at ${record.operationId}`)
      break
    }
    expectedPrev = record.checksum
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

// ============================================================================
// Convenience exports for API consumption
// ============================================================================

export const AuthorityPrimitives = {
  newAuthorityEnvelope,
  serializeEnvelope,
  deserializeEnvelope,
  appendEvidence,
  validateEnvelope,
  isLeaseValid,
  isBudgetAvailable,
  checkBudget,
  checkLeaseValidity,
  newLease,
  newBudget,
  newEvidenceRecord,
  newFencingToken
}