import json
import jsonschema
from jsonschema import Draft202012Validator
from datetime import datetime, timezone
import aspace.temporal_truth.temporal_truth as tt

tt.SCHEMA_PATH = "aspace/contracts/TEMPORAL_TRUTH_CONTEXT_V1.schema.json"
tt._schema = tt._load_schema()
graph = tt.TemporalCanonGraph()

schema_def = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$defs": tt._schema.get("$defs", {}),
    **tt._schema["$defs"]["TemporalClaim"]
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
    "temporal_state": "CURRENT",
    "recorded_at": "NOT-A-DATE",
    "source_ref": "c1"
}

try:
    jsonschema.validate(instance=claim, schema=schema_def, format_checker=Draft202012Validator.FORMAT_CHECKER)
    print("Ingest success (BAD for NOT-A-DATE)")
except Exception as e:
    print("Ingest failed (GOOD for NOT-A-DATE):", e.message)
