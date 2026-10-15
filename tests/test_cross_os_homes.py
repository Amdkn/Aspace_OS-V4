import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TestCrossOSHomes(unittest.TestCase):
 def test_agent_design(self):
  b=json.loads((R/'business/holons/registry.json').read_text())
  t=json.loads((R/'tech/holons/bindings.json').read_text())
  homes=[R/'tech/holons'/x['registry_key'] for x in t['records']]
  homes += [R/'business/holons'/x['home'] for k in ('directions','managers','squads') for x in b[k]]
  homes.append(R/'business/holons/J1')
  self.assertEqual(len(homes),150)
  for h in homes:
   self.assertTrue((h/'AGENT.md').is_file())
   self.assertTrue((h/'DESIGN.md').is_file())
