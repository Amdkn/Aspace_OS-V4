import json
import os
import jsonschema
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "../contracts/TEMPORAL_TRUTH_CONTEXT_V1.schema.json"
)

def _load_schema() -> Dict[str, Any]:
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

_schema = _load_schema()

class TemporalCanonGraph:
    def __init__(self):
        # In-memory storage for the core capability
        self.claims: Dict[str, Dict[str, Any]] = {}
        self.transitions: Dict[str, Dict[str, Any]] = {}

    def validate_schema(self, instance: Dict[str, Any], def_name: str) -> None:
        # Create a validator focusing on the specific definition
        schema_def = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$defs": _schema.get("$defs", {}),
            **_schema["$defs"][def_name]
        }
        jsonschema.validate(instance=instance, schema=schema_def)

    def ingest_claim(self, claim: Dict[str, Any]) -> None:
        # Auto-fill some fields to make it easier for callers if they are missing
        if "recorded_at" not in claim:
            claim["recorded_at"] = datetime.now(timezone.utc).isoformat()
        if "source_ref" not in claim:
            claim["source_ref"] = claim.get("claim_id", "unknown")
        if "temporal_state" not in claim:
            claim["temporal_state"] = "CURRENT"

        self.validate_schema(claim, "TemporalClaim")

        self.claims[claim["claim_id"]] = claim

    def record_transition(self, transition: Dict[str, Any]) -> None:
        if "recorded_at" not in transition:
            transition["recorded_at"] = datetime.now(timezone.utc).isoformat()

        self.validate_schema(transition, "CanonTransition")

        self.transitions[transition["transition_id"]] = transition

    def _get_superseded_claim_ids(self, t: str) -> set:
        superseded = set()
        # Explicit supersedes from claims up to time t
        for claim in self.claims.values():
            if claim["observed_at"] <= t:
                if "supersedes" in claim and claim["supersedes"]:
                    superseded.update(claim["supersedes"])
        # From transitions up to time t
        for transition in self.transitions.values():
            if transition.get("effective_at", transition.get("recorded_at")) <= t:
                superseded.update(transition.get("from_claims", []))
        return superseded

    def _get_contradicted_claim_ids(self, t: str) -> set:
        contradicted = set()
        # Explicit contradicts up to time t
        for claim in self.claims.values():
            if claim["observed_at"] <= t:
                if "contradicts" in claim and claim["contradicts"]:
                    contradicted.update(claim["contradicts"])
        # Transition contradictions up to time t
        for transition in self.transitions.values():
            if transition.get("effective_at", transition.get("recorded_at")) <= t:
                contradicted.update(transition.get("contradiction_refs", []))
        return contradicted

    def state_at(self, subject: str, predicate: str, t: str, scope: str) -> List[Dict[str, Any]]:
        # Find claims up to time t based on observed_at
        relevant = [
            c for c in self.claims.values()
            if c["subject"] == subject
            and c["predicate"] == predicate
            and c["scope"] == scope
            and c["observed_at"] <= t
        ]

        # Group by source_authority
        grouped = {}
        for c in relevant:
            auth = c["source_authority"]
            if auth not in grouped:
                grouped[auth] = []
            grouped[auth].append(c)

        superseded = self._get_superseded_claim_ids(t)

        results = []
        for auth, group_claims in grouped.items():
            # Sort by observed_at to find the head
            sorted_claims = sorted(group_claims, key=lambda x: x["observed_at"], reverse=True)

            # The most recent one is CURRENT unless it's superseded explicitly or globally
            head_claim = None
            for claim in sorted_claims:
                if claim["claim_id"] not in superseded:
                    head_claim = claim
                    break

            if not head_claim and sorted_claims:
                # All are superseded
                head_claim = sorted_claims[0] # we still return the most recent, but its temporal state is SUPERSEDED

            if head_claim:
                res_claim = head_claim.copy()
                if head_claim["claim_id"] in superseded:
                    res_claim["temporal_state"] = "SUPERSEDED"
                else:
                    res_claim["temporal_state"] = "CURRENT"
                results.append(res_claim)

        return results

    def state_now(self, subject: str, predicate: str, scope: str) -> List[Dict[str, Any]]:
        t_now = datetime.now(timezone.utc).isoformat()
        return self.state_at(subject, predicate, t_now, scope)

    def replay_history(
        self,
        *,
        subject: str | None = None,
        scope: str | None = None,
        t: str | None = None,
        limit: int = 64,
    ) -> Dict[str, Any]:
        """Return a bounded longitudinal replay without rewriting source truth."""
        if limit < 1 or limit > 128:
            raise ValueError("anthology replay limit must be between 1 and 128")

        cutoff = t or datetime.now(timezone.utc).isoformat()
        claims = [
            c.copy()
            for c in self.claims.values()
            if c.get("observed_at", "") <= cutoff
            and (subject is None or c.get("subject") == subject)
            and (scope is None or c.get("scope") == scope)
        ]
        claims.sort(
            key=lambda item: (
                str(item.get("observed_at") or ""),
                str(item.get("recorded_at") or ""),
                str(item.get("claim_id") or ""),
            )
        )
        total_claims = len(claims)
        bounded_claims = claims[-limit:]
        claim_ids = {str(item.get("claim_id")) for item in bounded_claims}

        transitions = []
        for transition in self.transitions.values():
            effective = transition.get("effective_at") or transition.get("recorded_at") or ""
            if effective > cutoff:
                continue
            linked = set(transition.get("from_claims", [])) | set(
                transition.get("to_claims", [])
            )
            if claim_ids and linked and not (claim_ids & linked):
                continue
            transitions.append(transition.copy())
        transitions.sort(
            key=lambda item: (
                str(item.get("effective_at") or item.get("recorded_at") or ""),
                str(item.get("transition_id") or ""),
            )
        )
        transitions = transitions[-limit:]

        return {
            "schema": "aspace.anthology-replay.v1",
            "cutoff_at": cutoff,
            "subject": subject,
            "scope": scope,
            "claims": bounded_claims,
            "transitions": transitions,
            "truncated": total_claims > len(bounded_claims),
            "limit": limit,
        }
