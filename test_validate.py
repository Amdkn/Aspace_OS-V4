import json
import jsonschema
from datetime import datetime, timezone
import aspace.temporal_truth.temporal_truth as tt

tt.SCHEMA_PATH = "aspace/contracts/TEMPORAL_TRUTH_CONTEXT_V1.schema.json"
tt._schema = tt._load_schema()
graph = tt.TemporalCanonGraph()

claim = {
    "schema": "aspace.temporal-claim.v1",
    "claim_id": "c1",
    "subject": "jules",
    "predicate": "active_slots",
    "scope": "runtime",
    "source_authority": "yaz",
    "observed_at": "2026-10-05T17:00:00+00:00",
    "assertion": "0 active",
    "evidence_refs": ["ev_1"]
}

try:
    graph.ingest_claim(claim)
    print("Ingest success")
except Exception as e:
    print("Ingest failed:", e)

# Test assertion with nested dict
claim["assertion"] = {"nested": "dict"}
try:
    graph.ingest_claim(claim)
    print("Nested dict ingest success (BAD if it should reject)")
except Exception as e:
    print("Nested dict ingest failed:", e)
