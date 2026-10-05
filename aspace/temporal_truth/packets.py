from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import datetime
import uuid
import json

def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

@dataclass
class ObservationPacket:
    packet_id: str
    observed_at: str
    source_ref: str
    source_authority: str
    dimension: str
    value: Any
    evidence_refs: List[str]
    correlation_id: Optional[str] = None
    return_to: Optional[Dict[str, Any]] = None
    schema: str = "aspace.observation-packet.v1"

    @classmethod
    def create(cls, source_ref: str, source_authority: str, dimension: str, value: Any, evidence_refs: List[str], correlation_id: Optional[str] = None, return_to: Optional[Dict[str, Any]] = None) -> 'ObservationPacket':
        return cls(
            packet_id=str(uuid.uuid4()),
            observed_at=_now_iso(),
            source_ref=source_ref,
            source_authority=source_authority,
            dimension=dimension,
            value=value,
            evidence_refs=evidence_refs,
            correlation_id=correlation_id,
            return_to=return_to
        )

@dataclass
class ContradictionPacket:
    packet_id: str
    detected_at: str
    subject: str
    predicate: str
    scope: str
    claims: List[str]
    detector_authority: str
    correlation_id: Optional[str] = None
    return_to: Optional[Dict[str, Any]] = None
    schema: str = "aspace.contradiction-packet.v1"

    @classmethod
    def create(cls, subject: str, predicate: str, scope: str, claims: List[str], detector_authority: str, correlation_id: Optional[str] = None, return_to: Optional[Dict[str, Any]] = None) -> 'ContradictionPacket':
        return cls(
            packet_id=str(uuid.uuid4()),
            detected_at=_now_iso(),
            subject=subject,
            predicate=predicate,
            scope=scope,
            claims=claims,
            detector_authority=detector_authority,
            correlation_id=correlation_id,
            return_to=return_to
        )

@dataclass
class CapabilityNeed:
    need_id: str
    issued_at: str
    target_capability: str
    evidence: List[str]
    issuer_authority: str
    correlation_id: Optional[str] = None
    return_to: Optional[Dict[str, Any]] = None
    schema: str = "aspace.capability-need.v1"

    @classmethod
    def create(cls, target_capability: str, evidence: List[str], issuer_authority: str, correlation_id: Optional[str] = None, return_to: Optional[Dict[str, Any]] = None) -> 'CapabilityNeed':
        return cls(
            need_id=str(uuid.uuid4()),
            issued_at=_now_iso(),
            target_capability=target_capability,
            evidence=evidence,
            issuer_authority=issuer_authority,
            correlation_id=correlation_id,
            return_to=return_to
        )

@dataclass
class TemporalClaim:
    claim_id: str
    source_ref: str
    source_authority: str
    recorded_at: str
    observed_at: str
    scope: str
    subject: str
    predicate: str
    assertion: Any
    evidence_refs: List[str]
    temporal_state: str
    correlation_id: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    supersedes: Optional[List[str]] = None
    superseded_by: Optional[List[str]] = None
    contradicts: Optional[List[str]] = None
    return_to: Optional[Dict[str, Any]] = None
    schema: str = "aspace.temporal-claim.v1"

@dataclass
class CanonTransition:
    transition_id: str
    subject: str
    predicate: str
    scope: str
    from_claims: List[str]
    to_claims: List[str]
    recorded_at: str
    effective_at: str
    reason: str
    evidence_refs: List[str]
    resolution_authority: str
    resolution_scope: str
    resulting_canon_heads: List[str]
    contradiction_refs: Optional[List[str]] = None
    correlation_id: Optional[str] = None
    return_to: Optional[Dict[str, Any]] = None
    schema: str = "aspace.canon-transition.v1"

@dataclass
class ContextCapsule:
    capsule_id: str
    compiled_at: str
    source_cutoff_at: str
    holon_id: str
    mission_id: str
    correlation_id: str
    canon_slice: List[str]
    anthology_window: List[str]
    authority_envelope: Dict[str, Any]
    workgraph_neighborhood: Dict[str, Any]
    evidence_head: List[str]
    contradictions: List[str]
    unknowns: List[str]
    return_to: Dict[str, Any]
    physiology_ref: Optional[str] = None
    source_slice: Optional[Dict[str, Any]] = None
    schema: str = "aspace.context-capsule.v1"

def serialize_packet(packet: Any) -> str:
    """Serialize any typed packet to JSON string without losing properties."""
    d = asdict(packet)
    # filtering out None values to respect schemas where these fields are optional or nullable
    d = {k: v for k, v in d.items() if v is not None}
    return json.dumps(d)

def deserialize_packet(json_str: str) -> Any:
    """Deserialize a JSON string back into the correct packet dataclass."""
    data = json.loads(json_str)
    schema = data.get("schema")

    if schema == "aspace.observation-packet.v1":
        return ObservationPacket(**data)
    elif schema == "aspace.contradiction-packet.v1":
        return ContradictionPacket(**data)
    elif schema == "aspace.capability-need.v1":
        return CapabilityNeed(**data)
    elif schema == "aspace.temporal-claim.v1":
        return TemporalClaim(**data)
    elif schema == "aspace.canon-transition.v1":
        return CanonTransition(**data)
    elif schema == "aspace.context-capsule.v1":
        return ContextCapsule(**data)
    else:
        raise ValueError(f"Unknown packet schema: {schema}")
