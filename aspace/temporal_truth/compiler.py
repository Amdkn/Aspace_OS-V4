import hashlib
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from .temporal_truth import TemporalCanonGraph


MAX_CONTEXT_REFS_V1 = 64
MAX_SOURCE_SLICE_KEYS_V1 = 32


class ContextCompilerBoundaryError(ValueError):
    """Raised when a requested context capsule exceeds the bounded G4 contract."""


def _stable_unique(values: List[str]) -> List[str]:
    return list(dict.fromkeys(values))


def _validate_ref_list(name: str, values: Optional[List[str]], limit: int) -> List[str]:
    if values is None:
        return []
    if not isinstance(values, list):
        raise ContextCompilerBoundaryError(f"{name} must be a list of refs")
    if len(values) > limit:
        raise ContextCompilerBoundaryError(
            f"{name} exceeds v1 reference budget ({len(values)} > {limit})"
        )
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ContextCompilerBoundaryError(
                f"{name} must contain non-empty string refs"
            )
    return _stable_unique(values)


def _validate_source_slice(source_slice: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if source_slice is None:
        return {}
    if not isinstance(source_slice, dict):
        raise ContextCompilerBoundaryError("source_slice must be a compact object")
    if len(source_slice) > MAX_SOURCE_SLICE_KEYS_V1:
        raise ContextCompilerBoundaryError(
            "source_slice exceeds v1 coordinate budget"
        )
    allowed_scalar = (str, int, float, bool, type(None))
    out: Dict[str, Any] = {}
    for key, value in source_slice.items():
        if not isinstance(key, str) or not key.strip():
            raise ContextCompilerBoundaryError(
                "source_slice keys must be non-empty strings"
            )
        if isinstance(value, allowed_scalar):
            out[key] = value
            continue
        if isinstance(value, list):
            if len(value) > MAX_CONTEXT_REFS_V1 or any(
                not isinstance(item, allowed_scalar) for item in value
            ):
                raise ContextCompilerBoundaryError(
                    "source_slice lists must stay compact scalar coordinates"
                )
            out[key] = list(value)
            continue
        raise ContextCompilerBoundaryError(
            "source_slice may contain only scalar coordinates or scalar lists"
        )
    return out


def _stable_id(prefix: str, payload: Dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(encoded).hexdigest()[:16]}"


class ContextCompiler:
    def __init__(self, graph: TemporalCanonGraph):
        self.graph = graph

    def derive_physiology_snapshot(
        self,
        subject: str,
        scope: str,
        requested_predicates: Optional[List[str]] = None,
        t: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Derive a replayable PhysiologySnapshot without mutating history."""
        observed_t = t or datetime.now(timezone.utc).isoformat()

        if requested_predicates is None:
            requested_predicates = sorted(
                {
                    c["predicate"]
                    for c in self.graph.claims.values()
                    if c["subject"] == subject and c["scope"] == scope
                }
            )
        else:
            requested_predicates = sorted(set(requested_predicates))

        dimensions = []
        for pred in requested_predicates:
            current_states = self.graph.state_at(subject, pred, observed_t, scope)
            active_heads = [
                c
                for c in current_states
                if c.get("temporal_state") == "CURRENT"
            ]

            if not active_heads:
                dimensions.append(
                    {
                        "name": pred,
                        "value": None,
                        "source_ref": "none",
                        "source_observed_at": observed_t,
                        "freshness": "UNKNOWN",
                        "epistemic_state": "UNKNOWN",
                        "unknown_reason": "No evidence found in canon graph",
                        "evidence_refs": [],
                        "source_authority": "none",
                    }
                )
                continue

            contradicted_ids = self.graph._get_contradicted_claim_ids(observed_t)
            is_contradicted = any(
                head["claim_id"] in contradicted_ids for head in active_heads
            )

            if not is_contradicted and len(active_heads) > 1:
                assertions = [
                    json.dumps(
                        head["assertion"],
                        sort_keys=True,
                        default=str,
                    )
                    for head in active_heads
                ]
                if len(set(assertions)) > 1:
                    is_contradicted = True

            for head in sorted(
                active_heads,
                key=lambda item: (
                    str(item.get("source_authority")),
                    str(item.get("claim_id")),
                ),
            ):
                dt_observed = datetime.fromisoformat(
                    head["observed_at"].replace("Z", "+00:00")
                )
                dt_now = datetime.fromisoformat(
                    observed_t.replace("Z", "+00:00")
                )
                age_secs = (dt_now - dt_observed).total_seconds()
                dimensions.append(
                    {
                        "name": pred,
                        "value": head["assertion"],
                        "source_ref": head["claim_id"],
                        "source_observed_at": head["observed_at"],
                        "freshness": "UNKNOWN",
                        "epistemic_state": (
                            "CONTRADICTED" if is_contradicted else "KNOWN"
                        ),
                        "evidence_refs": head.get("evidence_refs", []),
                        "source_authority": head["source_authority"],
                        "age_seconds": max(0.0, age_secs),
                    }
                )

        identity_material = {
            "subject": subject,
            "scope": scope,
            "observed_at": observed_t,
            "dimensions": dimensions,
        }
        snapshot = {
            "schema": "aspace.physiology-snapshot.v1",
            "snapshot_id": _stable_id("phys", identity_material),
            "observed_at": observed_t,
            "scope": scope,
            "valid_until": None,
            "dimensions": dimensions,
        }
        self.graph.validate_schema(snapshot, "PhysiologySnapshot")
        return snapshot

    def compile_context_capsule(
        self,
        holon_id: str,
        mission_id: str,
        correlation_id: str,
        scope: str,
        authority_envelope: Dict[str, Any],
        workgraph_neighborhood: Dict[str, Any],
        evidence_head: List[str],
        return_to: Dict[str, Any],
        t: Optional[str] = None,
        *,
        anthology_window: Optional[List[str]] = None,
        source_slice: Optional[Dict[str, Any]] = None,
        max_refs: int = MAX_CONTEXT_REFS_V1,
    ) -> Dict[str, Any]:
        """Compile a deterministic, bounded ContextCapsule for an explicit cutoff."""
        if max_refs <= 0 or max_refs > MAX_CONTEXT_REFS_V1:
            raise ContextCompilerBoundaryError(
                f"max_refs must be between 1 and {MAX_CONTEXT_REFS_V1}"
            )

        compiled_t = t or datetime.now(timezone.utc).isoformat()
        evidence_refs = _validate_ref_list(
            "evidence_head", evidence_head, max_refs
        )
        anthology_refs = _validate_ref_list(
            "anthology_window", anthology_window, max_refs
        )
        compact_source_slice = _validate_source_slice(source_slice)

        phys_snap = self.derive_physiology_snapshot(
            holon_id, scope, t=compiled_t
        )

        canon_slice: List[str] = []
        contradictions: List[str] = []
        unknowns: List[str] = []
        derived_evidence: List[str] = []

        for dim in phys_snap["dimensions"]:
            if dim["source_ref"] != "none":
                canon_slice.append(dim["source_ref"])
            if dim["epistemic_state"] == "CONTRADICTED":
                contradictions.append(dim["source_ref"])
            if dim["epistemic_state"] == "UNKNOWN":
                unknowns.append(dim["name"])
            derived_evidence.extend(dim.get("evidence_refs", []))

        canon_slice = _validate_ref_list(
            "canon_slice", _stable_unique(canon_slice), max_refs
        )
        contradictions = _validate_ref_list(
            "contradictions", _stable_unique(contradictions), max_refs
        )
        unknowns = _validate_ref_list(
            "unknowns", _stable_unique(unknowns), max_refs
        )
        evidence_refs = _validate_ref_list(
            "evidence_head",
            _stable_unique(evidence_refs + derived_evidence),
            max_refs,
        )

        material = {
            "compiled_at": compiled_t,
            "source_cutoff_at": compiled_t,
            "holon_id": holon_id,
            "mission_id": mission_id,
            "correlation_id": correlation_id,
            "canon_slice": canon_slice,
            "anthology_window": anthology_refs,
            "physiology_ref": phys_snap["snapshot_id"],
            "authority_envelope": authority_envelope,
            "workgraph_neighborhood": workgraph_neighborhood,
            "source_slice": compact_source_slice,
            "evidence_head": evidence_refs,
            "contradictions": contradictions,
            "unknowns": unknowns,
            "return_to": return_to,
        }
        identity_material = {
            "scope": scope,
            **material,
        }

        capsule = {
            "schema": "aspace.context-capsule.v1",
            "capsule_id": _stable_id("cap", identity_material),
            **material,
        }
        self.graph.validate_schema(capsule, "ContextCapsule")
        return capsule
