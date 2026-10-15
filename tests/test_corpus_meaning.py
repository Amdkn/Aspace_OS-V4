import copy
import unittest
from tools.corpus_meaning import check

def scenario():
    return {
        "schema": "aspace.contextual_passage.v1",
        "corpus_id": "DEMO-NO-PERSONAL-DATA",
        "source_ref": "https://example.org/fictional-creative-work",
        "source_kind": "video",
        "operational_assignment": False,
        "outcome_status": "NOT_APPLICABLE",
        "passages": [
            {"id": "p1", "locator": "00:04", "transcript_status": "UNAVAILABLE"},
            {"id": "p2", "locator": "06:38", "transcript_status": "UNKNOWN"}
        ],
        "utterances": [
            {"id": "u1", "passage_id": "p1", "speaker": "SOURCE_AUDIO", "status": "UNKNOWN", "sequence": 1,
             "text_status": "UNAVAILABLE", "provenance_ref": "source:local:unknown"},
            {"id": "u2", "passage_id": "p1", "speaker": "AGENT", "status": "MODEL_PROPOSED", "sequence": 2,
             "text": "Possibly a directive", "provenance_ref": "demo:agent:1"},
            {"id": "u3", "passage_id": "p1", "speaker": "USER", "status": "USER_EXPLICIT", "sequence": 3,
             "text": "That was a quotation of audio, not my own directive", "provenance_ref": "demo:user:2"},
            {"id": "u4", "passage_id": "p2", "speaker": "USER", "status": "USER_EXPLICIT", "sequence": 4,
             "text": "The phrase was a joke and its meaning evolved", "provenance_ref": "demo:user:3"},
        ],
        "relations": [
            {"id": "r1", "from_id": "u3", "to_id": "u2", "kind": "CORRECTS",
             "justification": "User corrected the agent's reading"},
            {"id": "r2", "from_id": "u3", "to_id": "u4", "kind": "EVOLVES_INTO",
             "justification": "User elaborated a separate joke"}
        ],
        "associations": [],
    }

class CorpusMeaningTests(unittest.TestCase):
    def test_correction_chain_retains_original_model_proposal(self):
        s = scenario()
        result = check(s)
        self.assertEqual(result["agent_proposals"], 1)
        self.assertEqual(result["explicit_user_utterances"], 2)
        self.assertEqual(result["relations"], 2)
        self.assertFalse(result["operational_assignment"])
        self.assertEqual(result["unknown_transcripts"], 2)

    def test_user_correction_not_forged_by_model(self):
        s = scenario()
        s["utterances"][2]["speaker"] = "AGENT"
        with self.assertRaises(ValueError): check(s)

    def test_earlier_model_is_not_rewritten_or_erased(self):
        s = scenario()
        s["relations"][0]["from_id"] = "u2"
        s["relations"][0]["to_id"] = "u3"
        with self.assertRaises(ValueError): check(s)

    def test_zero_architecture_assignments_are_valid(self):
        s = scenario()
        s["associations"] = []
        self.assertEqual(check(s)["associations"], 0)

    def test_independent_business_axes(self):
        s = scenario()
        s["associations"] = [
            {"axis": "BUSINESS_DIRECTION", "target": "E1", "status": "MODEL_PROPOSED", "justification": "Demo only", "basis_utterance_ids": ["u2"]},
            {"axis": "BUSINESS_L2_FUNCTION", "target": "PRD", "status": "MODEL_PROPOSED", "justification": "Demo only", "basis_utterance_ids": ["u2"]}
        ]
        self.assertEqual(check(s)["associations"], 2)
        s["associations"][0]["target"] = "PRD"
        with self.assertRaises(ValueError): check(s)

    def test_invalid_agent_meaning_cannot_become_direct_intention(self):
        s = scenario()
        s["associations"] = [{"axis": "IPBD", "target": "IPBD-D-0005", "status": "USER_EXPLICIT",
                              "justification": "Model guess is not user meaning", "basis_utterance_ids": ["u2"]}]
        with self.assertRaises(ValueError): check(s)

    def test_existing_ipbd_link_only_when_in_registry(self):
        s = scenario()
        s["associations"] = [{"axis": "IPBD", "target": "IPBD-D-0005", "status": "MODEL_PROPOSED",
                              "justification": "Hypothesis", "basis_utterance_ids": ["u2"]}]
        self.assertEqual(check(s, {"IPBD-D-0005"})["associations"], 1)
        with self.assertRaises(ValueError): check(s, {"IPBD-I-0001"})

    def test_missing_verbatim_marked_unknown_not_synthesized(self):
        s = scenario()
        s["passages"][0]["transcript_status"] = "VERIFIED"
        with self.assertRaises(ValueError): check(s)
        s = scenario()
        s["utterances"][0]["text_status"] = "VERBATIM"
        with self.assertRaises(ValueError): check(s)

    def test_raw_source_cannot_authorize_execution(self):
        s = scenario()
        s["operational_assignment"] = True
        with self.assertRaises(ValueError): check(s)
        s = scenario()
        s["outcome_status"] = "VERIFIED_WITH_EVIDENCE"
        with self.assertRaises(ValueError): check(s)

    def test_no_forced_factory_or_work_value(self):
        s = scenario()
        s["associations"] = [{"axis": "UNCLASSIFIED", "target": "ENJOYMENT_OR_UNKNOWN",
                              "status": "UNKNOWN", "justification": "The work need not serve a factory",
                              "basis_utterance_ids": []}]
        self.assertEqual(check(s)["associations"], 1)


    def test_correction_can_address_third_party_without_relabeling_it_as_agent(self):
        s = scenario()
        s["utterances"].append({"id": "u5", "passage_id": "p1", "speaker": "THIRD_PARTY",
            "status": "HISTORICAL", "sequence": 0, "text": "Fictional third-party statement",
            "provenance_ref": "demo:third-party:1"})
        s["relations"][0]["to_id"] = "u5"
        s["relations"][0]["justification"] = "Human correction to third party, not Gemini"
        self.assertEqual(check(s)["relations"], 2)
        self.assertEqual(s["utterances"][1]["speaker"], "AGENT")

    def test_correction_can_address_own_earlier_statement(self):
        s = scenario()
        s["relations"].append({"id": "r3", "from_id": "u4", "to_id": "u3",
            "kind": "CORRECTS", "justification": "Human revises their own statement"})
        self.assertEqual(check(s)["relations"], 3)

    def test_distinct_third_party_and_agent_correction_targets(self):
        s = scenario()
        s["utterances"].append({"id": "u5", "passage_id": "p1", "speaker": "THIRD_PARTY",
            "status": "HISTORICAL", "sequence": 0, "text": "Third-party reading",
            "provenance_ref": "demo:third-party:2"})
        s["relations"][0]["to_id"] = "u5"
        s["relations"].append({"id": "r3", "from_id": "u4", "to_id": "u2",
            "kind": "CORRECTS", "justification": "Separate correction to model"})
        self.assertEqual(check(s)["relations"], 3)
        self.assertNotEqual(s["relations"][0]["to_id"], s["relations"][2]["to_id"])

    def test_ipbd_reference_without_index_is_unverified_not_certified(self):
        s = scenario()
        s["associations"] = [{"axis": "IPBD", "target": "IPBD-I-9999",
            "status": "MODEL_PROPOSED", "justification": "Unresolved candidate",
            "basis_utterance_ids": ["u2"]}]
        report = check(s)
        self.assertEqual(report["ipbd_status"], "NOT_VERIFIED")
        self.assertEqual(report["unresolved_ipbd_count"], 1)
        self.assertEqual(report["validation_scope"], "STRUCTURE_ONLY")
        with self.assertRaises(ValueError):
            check(s, known_ipbd_ids={"IPBD-I-0001"})

    def test_verbatim_requires_resolved_source_to_claim_matching(self):
        s = scenario()
        s["utterances"][2]["text_status"] = "VERBATIM"
        unverified = check(s)
        self.assertEqual(unverified["unresolved_verbatim_count"], 1)
        self.assertEqual(unverified["provenance_status"], "NOT_VERIFIED")
        with self.assertRaises(ValueError):
            check(s, source_text_by_ref={"demo:user:2": "Invented replacement"})
        verified = check(s, known_ipbd_ids=set(), source_text_by_ref={
            "demo:user:2": s["utterances"][2]["text"]})
        self.assertEqual(verified["unresolved_verbatim_count"], 0)
        self.assertEqual(verified["provenance_status"], "MATCHED_SUPPLIED_REFERENCES")

if __name__ == "__main__":
    unittest.main()
