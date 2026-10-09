import jsonschema
import json
from datetime import datetime, timezone
from aspace.temporal_truth.temporal_truth import _schema

schema_def = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$defs": _schema.get("$defs", {}),
    **_schema["$defs"]["TemporalClaim"]
}

claim = {
    "schema": "aspace.temporal-claim.v1",
    "claim_id": "c1",
    "subject": "jules",
    "predicate": "active_slots",
    "scope": "runtime",
    "source_authority": "yaz",
    "observed_at": "NOT-A-DATE",
    "assertion": "0 active",
    "evidence_refs": ["ev_1"],
    "temporal_state": "CURRENT"
}

try:
    jsonschema.validate(instance=claim, schema=schema_def, format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER)
    print("VALID (BAD)")
except Exception as e:
    print("INVALID (GOOD):", e)
