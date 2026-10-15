import json, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TestBillTillyVideoRegistry(unittest.TestCase):
 def test_unique_and_sourced(self):
  j=json.loads((R/'research/bill_tilly/video_manifest.json').read_text())
  ids=['ZHOmBeMNbnc','mQBuZ6Dp0u0','Lt8XH8HJU_M','-dq5PkLdAZ0','7PLKOz3gHSA','SeQXCpZhbjc']
  self.assertEqual([x['video_id'] for x in j['sources']],ids)
  self.assertEqual(len({x['url'] for x in j['sources']}),6)
  self.assertEqual(sum(isinstance(x['first_party_watch_history'],dict) for x in j['sources']),5)
  self.assertTrue(all(x['transcript_ref'] is None for x in j['sources']))
  self.assertEqual(j['question_owner'],'aspace:life:a3:discovery:tilly')
  self.assertEqual(j['research_owner'],'aspace:tech:bill')
  self.assertIn('aspace:business:E2:PRD',j['business_chain'])
