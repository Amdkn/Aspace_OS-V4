from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable

from .packets import CanonTransition, ContradictionPacket
from .temporal_truth import TemporalCanonGraph


class ReconciliationBoundaryError(ValueError):
    """Raised when an explicit semantic decision exceeds the G3 boundary."""


_REQUIRED_DECISION_FIELDS = {
    "resolution_authority",
    "resolution_scope",
    "selected_claims",
    "reason",
    "evidence_refs",
    "effective_at",
}


def _require_nonempty_strings(values: Iterable[Any], field: str) -> list[str]:
    out = list(values)
    if not out or any(not isinstance(value, str) or not value.strip() for value in out):
        raise ReconciliationBoundaryError(f"{field} must contain non-empty refs")
    return out


def transition_from_explicit_decision(
    graph: TemporalCanonGraph,
    packet: ContradictionPacket,
    decision: Dict[str, Any],
    *,
    expected_resolution_authority: str = "rory",
) -> CanonTransition:
    """Validate and materialize an explicit Rory reconciliation decision.

    This function never chooses a winning claim. It only converts an already
    explicit, bounded semantic decision into a CanonTransition.
    """
    missing = sorted(_REQUIRED_DECISION_FIELDS - set(decision))
    if missing:
        raise ReconciliationBoundaryError(
            f"explicit reconciliation decision missing: {', '.join(missing)}"
        )

    resolution_authority = str(decision["resolution_authority"]).strip()
    if resolution_authority != expected_resolution_authority:
        raise ReconciliationBoundaryError(
            "resolution_authority does not match the authorized semantic owner"
        )

    resolution_scope = str(decision["resolution_scope"]).strip()
    if resolution_scope != packet.scope:
        raise ReconciliationBoundaryError(
            "resolution_scope must exactly match contradiction scope in v1"
        )

    packet_claims = _require_nonempty_strings(packet.claims, "packet.claims")
    if len(set(packet_claims)) < 2:
        raise ReconciliationBoundaryError(
            "ContradictionPacket must reference at least two distinct claims"
        )

    selected = _require_nonempty_strings(
        decision["selected_claims"], "selected_claims"
    )
    if not set(selected).issubset(set(packet_claims)):
        raise ReconciliationBoundaryError(
            "selected_claims must be drawn from the ContradictionPacket"
        )

    evidence_refs = _require_nonempty_strings(
        decision["evidence_refs"], "evidence_refs"
    )

    reason = str(decision["reason"]).strip()
    if not reason:
        raise ReconciliationBoundaryError("reason must be explicit")

    # Every contradictory claim must already exist in the CanonGraph and must
    # describe the exact same semantic dimension as the packet.
    for claim_id in packet_claims:
        claim = graph.claims.get(claim_id)
        if claim is None:
            raise ReconciliationBoundaryError(
                f"ContradictionPacket references unknown claim: {claim_id}"
            )
        expected = (packet.subject, packet.predicate, packet.scope)
        actual = (
            claim.get("subject"),
            claim.get("predicate"),
            claim.get("scope"),
        )
        if actual != expected:
            raise ReconciliationBoundaryError(
                f"claim {claim_id} does not match contradiction dimension"
            )

    correlation_id = decision.get("correlation_id", packet.correlation_id)
    if packet.correlation_id is not None and correlation_id != packet.correlation_id:
        raise ReconciliationBoundaryError("correlation_id drift is forbidden")

    return_to = decision.get("return_to", packet.return_to)
    if packet.return_to is not None and return_to != packet.return_to:
        raise ReconciliationBoundaryError("return_to drift is forbidden")

    losing = [claim_id for claim_id in packet_claims if claim_id not in set(selected)]
    if not losing:
        raise ReconciliationBoundaryError(
            "decision must actually reconcile at least one contradictory claim"
        )

    transition = CanonTransition(
        transition_id=str(
            decision.get("transition_id")
            or f"rory-{packet.packet_id}"
        ),
        subject=packet.subject,
        predicate=packet.predicate,
        scope=packet.scope,
        from_claims=losing,
        to_claims=selected,
        recorded_at=datetime.now(timezone.utc).isoformat(),
        effective_at=str(decision["effective_at"]),
        reason=reason,
        evidence_refs=evidence_refs,
        resolution_authority=resolution_authority,
        resolution_scope=resolution_scope,
        resulting_canon_heads=selected,
        contradiction_refs=[packet.packet_id],
        correlation_id=correlation_id,
        return_to=return_to,
    )

    # record_transition validates against the canonical Temporal Truth schema.
    graph.record_transition(asdict(transition))
    return transition
