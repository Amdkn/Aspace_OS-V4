import unittest, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TestCrossOS(unittest.TestCase):
 def test_anchors(self):
  x=json.loads((R/'architecture/cross_os_collaboration.json').read_text(encoding='utf8'))
  b=json.loads((R/'business/holons/registry.json').read_text(encoding='utf8'))
  assert len(x['historic'])==8
  assert len(x['tech_to_a3'])==9
  assert len(b['managers'])==64 and len(b['squads'])==64
  expected=['OPS','FIN','LEG','PRD','SAL','PPL','IT','GRO']
  for i,h in enumerate(x['historic']):
   c='BCDEFGHI'[i]
   assert h['historic_anchor_manager_id']==f'aspace:business:{c}2:{expected[i]}'
   assert h['historic_anchor_squad_id']==f'aspace:business:{c}3:{expected[i]}'
   assert b['directions'][i]['life_a3_id']==h['life_a3_id']
