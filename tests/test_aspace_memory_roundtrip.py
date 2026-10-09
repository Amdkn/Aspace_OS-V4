import unittest
import subprocess
import json
import tempfile
import os
import sys

class AspaceMemoryRoundTripTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_memory.sqlite")

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_memory_cli(self, command, **kwargs):
        cmd = [sys.executable, "-m", "aspace.memory", command, "--db", self.db_path]
        for key, value in kwargs.items():
            if value is not None:
                cmd.extend([f"--{key}", str(value)])

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        return json.loads(result.stdout)

    def test_round_trip(self):
        # 1. Write a claim
        input_path = os.path.join(self.temp_dir.name, "claim.json")
        claim_data = {
            "schema": "aspace.temporal-claim.v1",
            "claim_id": "test_claim_1",
            "source_ref": "test_ref",
            "source_authority": "test_auth",
            "recorded_at": "2026-10-09T00:00:00Z",
            "observed_at": "2026-10-09T00:00:00Z",
            "scope": "test_scope",
            "subject": "test_subject",
            "predicate": "test_predicate",
            "assertion": {"test": "data"},
            "evidence_refs": ["test_digest"],
            "temporal_state": "CURRENT"
        }
        with open(input_path, "w") as f:
            json.dump(claim_data, f)

        write_result = self.run_memory_cli("claim", authority="test_auth", input=input_path)
        self.assertEqual(write_result.get("identity"), "test_claim_1")

        # 2. Read the claim via context or replay
        replay_result = self.run_memory_cli("replay", at="2026-10-09T00:00:00Z", subject="test_subject", scope="test_scope")

        self.assertEqual(len(replay_result["claims"]), 1)
        self.assertEqual(replay_result["claims"][0]["claim_id"], "test_claim_1")

if __name__ == '__main__':
    unittest.main()
