import unittest
from copy import deepcopy
import importlib
import os
import sys


compiler_module = importlib.import_module("aspace.temporal_truth.compiler")
temporal_truth_module = importlib.import_module("aspace.temporal_truth.temporal_truth")

ContextCompiler = compiler_module.ContextCompiler
ContextCompilerBoundaryError = compiler_module.ContextCompilerBoundaryError
MAX_CONTEXT_REFS_V1 = compiler_module.MAX_CONTEXT_REFS_V1
TemporalCanonGraph = temporal_truth_module.TemporalCanonGraph


class TestDeterministicBoundedContextCompiler(unittest.TestCase):
    def setUp(self):
        self.graph = TemporalCanonGraph()
        self.cutoff = "2026-10-03T20:00:00+00:00"
        self.graph.ingest_claim(
            {
                "schema": "aspace.temporal-claim.v1",
                "claim_id": "claim-role",
                "subject": "ryan",
                "predicate": "role",
                "scope": "mission-496",
                "source_authority": "canon",
                "observed_at": "2026-10-03T19:00:00+00:00",
                "assertion": "builder",
                "evidence_refs": ["evidence:role"],
            }
        )
        self.compiler = ContextCompiler(self.graph)
        self.kwargs = {
            "holon_id": "ryan",
            "mission_id": "mission-496",
            "correlation_id": "corr-496",
            "scope": "mission-496",
            "authority_envelope": {
                "scope": "build",
                "policy": "bounded",
            },
            "workgraph_neighborhood": {
                "work_id": 496,
                "dependencies": [448],
            },
            "evidence_head": ["evidence:request"],
            "return_to": {"issue": 448, "gate": "G5"},
            "t": self.cutoff,
            "anthology_window": ["anthology:event:1", "anthology:event:2"],
            "source_slice": {
                "github_issue": 496,
                "work_id": 496,
                "refs": ["#448", "#496"],
            },
        }

    def test_same_replay_inputs_produce_same_snapshot_and_capsule_identity(self):
        first = self.compiler.compile_context_capsule(**deepcopy(self.kwargs))
        second = self.compiler.compile_context_capsule(**deepcopy(self.kwargs))
        self.assertEqual(first["capsule_id"], second["capsule_id"])
        self.assertEqual(first["physiology_ref"], second["physiology_ref"])
        self.assertEqual(first, second)

    def test_material_source_or_cutoff_change_changes_identity(self):
        first = self.compiler.compile_context_capsule(**deepcopy(self.kwargs))

        changed_cutoff = deepcopy(self.kwargs)
        changed_cutoff["t"] = "2026-10-03T20:01:00+00:00"
        second = self.compiler.compile_context_capsule(**changed_cutoff)
        self.assertNotEqual(first["capsule_id"], second["capsule_id"])

        changed_anthology = deepcopy(self.kwargs)
        changed_anthology["anthology_window"].append("anthology:event:3")
        third = self.compiler.compile_context_capsule(**changed_anthology)
        self.assertNotEqual(first["capsule_id"], third["capsule_id"])

    def test_source_links_authority_unknowns_and_return_path_are_preserved(self):
        capsule = self.compiler.compile_context_capsule(**deepcopy(self.kwargs))
        self.assertEqual(
            capsule["anthology_window"],
            ["anthology:event:1", "anthology:event:2"],
        )
        self.assertEqual(capsule["source_slice"]["github_issue"], 496)
        self.assertEqual(
            capsule["authority_envelope"],
            self.kwargs["authority_envelope"],
        )
        self.assertEqual(capsule["return_to"], self.kwargs["return_to"])
        self.assertIn("evidence:role", capsule["evidence_head"])
        self.assertNotIn("next_action", capsule)
        self.assertNotIn("prompt", capsule)
        self.assertNotIn("giant_role_prompt", str(capsule))

    def test_unknown_dimension_survives_context_compilation(self):
        kwargs = deepcopy(self.kwargs)
        kwargs["holon_id"] = "unknown-holon"
        capsule = self.compiler.compile_context_capsule(**kwargs)
        # With no predicates recorded for the unknown holon there is no invented
        # state; the capsule remains bounded and does not manufacture a role.
        self.assertEqual(capsule["canon_slice"], [])
        self.assertNotIn("next_action", capsule)

    def test_oversized_reference_windows_fail_closed(self):
        too_many = [f"ref:{i}" for i in range(MAX_CONTEXT_REFS_V1 + 1)]
        for field in ("anthology_window", "evidence_head"):
            with self.subTest(field=field):
                kwargs = deepcopy(self.kwargs)
                kwargs[field] = too_many
                with self.assertRaises(ContextCompilerBoundaryError):
                    self.compiler.compile_context_capsule(**kwargs)

    def test_non_list_anthology_window_fails_closed(self):
        kwargs = deepcopy(self.kwargs)
        kwargs["anthology_window"] = "not-a-list"
        with self.assertRaises(ContextCompilerBoundaryError):
            self.compiler.compile_context_capsule(**kwargs)

    def test_nested_or_oversized_source_slice_fails_closed(self):
        kwargs = deepcopy(self.kwargs)
        kwargs["source_slice"] = {"nested": {"forbidden": True}}
        with self.assertRaises(ContextCompilerBoundaryError):
            self.compiler.compile_context_capsule(**kwargs)

        kwargs = deepcopy(self.kwargs)
        kwargs["source_slice"] = {
            f"k{i}": i for i in range(33)
        }
        with self.assertRaises(ContextCompilerBoundaryError):
            self.compiler.compile_context_capsule(**kwargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
