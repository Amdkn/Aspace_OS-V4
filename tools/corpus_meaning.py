#!/usr/bin/env python3
"""Inspect contextual meaning and corrections without converting culture into work.

This is a LOCAL, read-only validator. Inputs can be sensitive: by default CLI
prints *only* status/counts, never user utterances, names, or references.
Nothing is sent to providers, GitHub, Linear or other APIs.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

ALLOWED_SPEAKERS = {"USER", "AGENT", "THIRD_PARTY", "SOURCE_AUDIO", "SCHEDULER", "UNKNOWN"}
EPISTEMIC = {"USER_EXPLICIT", "MODEL_PROPOSED", "HISTORICAL", "CORRECTED", "UNKNOWN"}
RELATIONS = {"QUOTES", "REPLIES_TO", "CORRECTS", "EVOLVES_INTO",
             "WORDPLAY_ON", "CULTURAL_ECHO", "CONTRADICTS", "REFINES"}
AXES = {"LIFE_DOMAIN", "BUSINESS_DIRECTION", "BUSINESS_L2_FUNCTION",
        "FRAMEWORK", "TECH_CAPABILITY", "PERSON", "WORK", "CONCEPT",
        "IPBD", "UNCLASSIFIED"}
DIRECTIONS = {f"{x}1" for x in "BCDEFGHI"}
L2_FUNCTIONS = {"GRO", "SAL", "PRD", "OPS", "IT", "FIN", "PPL", "LEG"}
FRAMEWORKS = {"Ikigai", "Discovery", "PARA", "12WY", "GTD", "DEAL"}


def _nonempty(x):
    return isinstance(x, str) and bool(x.strip())


def check(record, known_ipbd_ids=None):
    if not isinstance(record, dict) or record.get("schema") != "aspace.contextual_passage.v1":
        raise ValueError("Unsupported record schema")
    if not _nonempty(record.get("corpus_id")) or not _nonempty(record.get("source_ref")):
        raise ValueError("Source and corpus identifiers are required")
    if record.get("operational_assignment") not in (None, False):
        raise ValueError("Source interpretation cannot authorise execution")
    passages = record.get("passages", [])
    voices = record.get("utterances", [])
    relations = record.get("relations", [])
    associations = record.get("associations", [])
    if not isinstance(passages, list) or not isinstance(voices, list):
        raise ValueError("Passages and utterances must be arrays")
    ids = set()
    passage_ids = set()
    for p in passages:
        pid = p.get("id")
        if not _nonempty(pid) or pid in passage_ids:
            raise ValueError("Passage IDs must be unique and non-empty")
        passage_ids.add(pid)
        if not _nonempty(p.get("locator")):
            raise ValueError("Locator is required even when transcript is unavailable")
        if p.get("transcript_status") not in ("VERIFIED", "PARTIAL", "UNAVAILABLE", "UNKNOWN"):
            raise ValueError("Transcript quality cannot be inferred")
        if p.get("transcript_status") == "VERIFIED" and not _nonempty(p.get("transcript_ref")):
            raise ValueError("Verified transcript requires evidence")
    by_id = {}
    for v in voices:
        vid = v.get("id")
        if not _nonempty(vid) or vid in ids:
            raise ValueError("Utterance IDs must be unique")
        ids.add(vid)
        if v.get("passage_id") not in passage_ids:
            raise ValueError("Utterance references nonexistent passage")
        if v.get("speaker") not in ALLOWED_SPEAKERS or v.get("status") not in EPISTEMIC:
            raise ValueError("Speaker and epistemic status are independent")
        if v.get("status") == "USER_EXPLICIT" and v.get("speaker") != "USER":
            raise ValueError("Only actual USER utterance can claim explicit human intent")
        if v.get("status") == "MODEL_PROPOSED" and v.get("speaker") != "AGENT":
            raise ValueError("Model proposal must be voiced by an agent")
        if not _nonempty(v.get("provenance_ref")):
            raise ValueError("Each utterance needs provenance")
        if type(v.get("sequence")) is not int or v["sequence"] < 0:
            raise ValueError("Sequence must be a nonnegative integer")
        if not _nonempty(v.get("text")) and v.get("text_status") != "UNAVAILABLE":
            raise ValueError("Missing verbatim must be explicitly unavailable")
        if v.get("text_status") == "VERBATIM" and not _nonempty(v.get("text")):
            raise ValueError("No fabricated verbatim")
        by_id[vid] = v
    rel_ids = set()
    for edge in relations:
        relid = edge.get("id")
        if not _nonempty(relid) or relid in rel_ids:
            raise ValueError("Relation ID must be unique")
        rel_ids.add(relid)
        if edge.get("from_id") not in ids or edge.get("to_id") not in ids:
            raise ValueError("Relation endpoints must be present")
        if edge.get("kind") not in RELATIONS or not _nonempty(edge.get("justification")):
            raise ValueError("Relation kind and justification required")
        if edge["kind"] == "CORRECTS":
            a, b = by_id[edge["from_id"]], by_id[edge["to_id"]]
            if a["speaker"] != "USER" or b["speaker"] != "AGENT":
                raise ValueError("User corrections require user->agent voice attribution")
            if a["sequence"] <= b["sequence"]:
                raise ValueError("Correction must follow the interpretation it corrects")
        if edge["kind"] == "EVOLVES_INTO" and by_id[edge["from_id"]]["sequence"] >= by_id[edge["to_id"]]["sequence"]:
            raise ValueError("A future utterance cannot evolve into the past")
    for assoc in associations:
        axis = assoc.get("axis")
        if axis not in AXES:
            raise ValueError("Unknown association axis")
        if assoc.get("status") not in EPISTEMIC:
            raise ValueError("Association has no epistemic basis")
        if not _nonempty(assoc.get("justification")):
            raise ValueError("Every assignment must explain why")
        if axis == "BUSINESS_DIRECTION" and assoc.get("target") not in DIRECTIONS:
            raise ValueError("B1–I1 must not be confused with L2 functions")
        if axis == "BUSINESS_L2_FUNCTION" and assoc.get("target") not in L2_FUNCTIONS:
            raise ValueError("Business function axis accepts only eight L2 functions")
        if axis == "FRAMEWORK" and assoc.get("target") not in FRAMEWORKS:
            raise ValueError("Unknown framework")
        if axis == "LIFE_DOMAIN" and assoc.get("target") not in {f"LD{i:02d}" for i in range(1,9)}:
            raise ValueError("Unknown Life domain")
        if axis == "IPBD" and known_ipbd_ids is not None and assoc.get("target") not in known_ipbd_ids:
            raise ValueError("Never invent a new IPBD ID through corpus classification")
        if not isinstance(assoc.get("basis_utterance_ids"), list) or any(x not in ids for x in assoc["basis_utterance_ids"]):
            raise ValueError("Association requires in-record voice evidence, even if empty")
        if assoc["status"] == "USER_EXPLICIT" and not any(by_id[x]["speaker"] == "USER" and by_id[x]["status"] == "USER_EXPLICIT" for x in assoc["basis_utterance_ids"]):
            raise ValueError("Cannot label an agent inference USER_EXPLICIT")
    if record.get("outcome_status") not in ("UNKNOWN", "NOT_APPLICABLE", "VERIFIED_WITH_EVIDENCE"):
        raise ValueError("No default outcome from a cultural source")
    if record.get("outcome_status") == "VERIFIED_WITH_EVIDENCE" and not _nonempty(record.get("outcome_evidence_ref")):
        raise ValueError("No verified effect without external evidence")
    return {
        "corpus_id": record["corpus_id"],
        "passages": len(passages), "utterances": len(voices), "relations": len(relations),
        "associations": len(associations), "explicit_user_utterances": sum(x["status"] == "USER_EXPLICIT" for x in voices),
        "agent_proposals": sum(x["status"] == "MODEL_PROPOSED" for x in voices),
        "unknown_transcripts": sum(x["transcript_status"] in ("UNKNOWN","UNAVAILABLE") for x in passages),
        "operational_assignment": False, "outcome_status": record["outcome_status"],
    }


def load_ipbd_ids(public_register_path):
    obj = json.loads(Path(public_register_path).read_text(encoding="utf-8"))
    def walk(node):
        if isinstance(node, dict):
            yield from (k for k in node.keys() if re.fullmatch(r"IPBD-[IPBD]-\d{4}", k))
            for val in node.values():
                yield from walk(val)
        elif isinstance(node, list):
            for val in node:
                yield from walk(val)
        elif isinstance(node, str):
            if re.fullmatch(r"IPBD-[IPBD]-\d{4}", node):
                yield node
    return set(walk(obj))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("private_record", type=Path, help="Locally accessible contextual record, never auto-uploaded")
    p.add_argument("--public-ipbd-index", type=Path, default=None)
    args = p.parse_args(argv)
    try:
        data = json.loads(args.private_record.read_text(encoding="utf-8"))
        ids = load_ipbd_ids(args.public_ipbd_index) if args.public_ipbd_index else None
        print(json.dumps(check(data, ids), ensure_ascii=False, indent=2))
    except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
        print("INVALID CONTEXTUAL CORPUS RECORD: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
