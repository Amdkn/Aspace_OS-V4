import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TestCrossOSReciprocity(unittest.TestCase):
 def test_all_8_a3_and_9_s3(self):
  g=json.loads((R/'architecture/cross_os_collaboration.json').read_text())
  self.assertEqual(len(g['historic']),8)
  self.assertEqual(len(g['tech_to_a3']),9)
  for h in g['historic']:
   home=R/h['life_a3_home']
   self.assertIn('CROSS-OS-20261014',(home/'RELATIONS.md').read_text())
   self.assertIn('CROSS-OS-20261014',(home/'CONTRACTS.md').read_text())
  for edge in g['tech_to_a3']:
   home=R/edge['tech_home']
   self.assertIn('CROSS-OS-20261014',(home/'CONTRACTS.md').read_text())
