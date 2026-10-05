import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('mesh',Path(__file__).resolve().parents[1]/'tools/agent_mesh.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def pr(sha='a'*40):
 return {'number':8,'state':'open','draft':False,'author_association':'OWNER','user':{'type':'User'},'head':{'sha':sha,'ref':'mission','repo':{'full_name':'Amdkn/Aspace_OS-V4'}},'base':{'sha':'b'*40},'html_url':'https://github.com/Amdkn/Aspace_OS-V4/pull/8'}
class MeshTests(unittest.TestCase):
 def setUp(self):
  self.env=patch.dict(os.environ,{'GITHUB_REPOSITORY':'Amdkn/Aspace_OS-V4','GITHUB_RUN_ID':'123'},clear=True);self.env.start()
  self.temp=tempfile.TemporaryDirectory();self.out=patch.object(m,'OUT',Path(self.temp.name));self.out.start()
  self.mission=dict(m.mission_for(pr(),'rick'),provider='codex')
 def tearDown(self):self.out.stop();self.temp.cleanup();self.env.stop()
 def result(self):return dict(mission_id=self.mission['mission_id'],head_sha=self.mission['head_sha'],verdict='ready',summary='Verified',findings=[],evidence=['command + result'])
 def test_identity_provider_independent_head_and_agent_sensitive(self):
  self.assertEqual(self.mission['mission_id'],m.mission_for(pr(),'rick')['mission_id'])
  self.assertNotEqual(self.mission['mission_id'],m.mission_for(pr('c'*40),'rick')['mission_id'])
  self.assertNotEqual(self.mission['mission_id'],m.mission_for(pr(),'yaz')['mission_id'])
 def test_claim_unknown_and_final_not_retried(self):
  for state in ['CLAIMED:codex:123','UNKNOWN:timeout','READY:codex','CHANGES_REQUIRED:codex']:
   self.assertFalse(m.resumable({'description':state},'new'))
 def test_connection_change_resumes_only_pre_effect_blocker(self):
  self.assertFalse(m.resumable({'description':'BLOCKED:unavailable:old'},'old'))
  self.assertTrue(m.resumable({'description':'BLOCKED:unavailable:old'},'new'))
 def test_explicit_provider_not_silently_replaced(self):
  self.assertIsNone(m.select_provider({'codex':True},'jules'));self.assertEqual(m.select_provider({'hermes':True}),'hermes')
 def test_wrong_head_or_mission_rejected(self):
  for key in ['head_sha','mission_id']:
   r=self.result();r[key]='wrong'
   with self.assertRaises(ValueError):m.validate_result(r,self.mission)
 def test_ready_requires_evidence_without_findings(self):
  for key,val in [('evidence',[]),('findings',['race condition'])]:
   r=self.result();r[key]=val
   with self.assertRaises(ValueError):m.validate_result(r,self.mission)
 def test_head_moved_cannot_receive_success(self):
  with patch.object(m,'gh',return_value=pr('c'*40)),patch.object(m,'receipt') as rec:
   m.finish(self.result(),self.mission)
  self.assertEqual(rec.call_args.args[1],'error');self.assertTrue(rec.call_args.args[2].startswith('STALE'))
 def test_claim_before_dispatch_and_duplicate_delivery(self):
  states=[]
  def pages(path):return [pr()] if path.startswith('pulls') else list(reversed(states))
  def rec(mission,state,desc,url=None):states.append(dict(context=mission['context'],state=state,description=desc))
  with patch.dict(os.environ,{'CODEX_AVAILABLE':'true'}),patch.object(m,'pages',side_effect=pages),patch.object(m,'receipt',side_effect=rec):m.prepare();m.prepare()
  self.assertEqual(len(states),1);self.assertTrue(states[0]['description'].startswith('CLAIMED:codex'))
 def test_no_runtime_reports_blocked(self):
  with patch.object(m,'pages',side_effect=lambda p:[pr()] if p.startswith('pulls') else []),patch.object(m,'receipt') as rec:m.prepare()
  self.assertEqual(rec.call_args.args[1],'error');self.assertTrue((m.OUT/'blocked.json').exists())
 def test_fork_never_dispatches(self):
  p=pr();p['head']['repo']['full_name']='external/fork'
  with patch.object(m,'pages',return_value=[p]),patch.object(m,'receipt') as rec:m.prepare()
  rec.assert_not_called()
 def test_jules_uses_discovered_source(self):
  mission=dict(self.mission,provider='jules',operation='dispatch');(m.OUT/'prompt.txt').write_text('review')
  with patch.object(m,'google_pages',return_value=[{'name':'sources/actual','githubRepo':{'owner':'Amdkn','repo':'Aspace_OS-V4'}}]),patch.object(m,'gh',return_value=pr()),patch.object(m,'google',return_value={'name':'sessions/123'}) as google,patch.object(m,'receipt'):m.jules(mission)
  body=google.call_args.args[1];self.assertEqual(body['sourceContext']['source'],'sources/actual');self.assertFalse(body['requirePlanApproval']);self.assertNotIn('automationMode',body)
 def test_jules_completion_without_receipt_blocked(self):
  with patch.object(m,'google',return_value={'state':'COMPLETED'}),patch.object(m,'google_pages',return_value=[]),patch.object(m,'receipt') as rec:m.jules(dict(self.mission,provider='jules',operation='poll',session='sessions/123'))
  self.assertEqual(rec.call_args.args[1],'error')
 def test_profiles_all_provider_agnostic(self):
  for profile,data in m.REGISTRY['profiles'].items():
   self.assertEqual(data['providers'],['codex','jules','hermes'])
   self.assertNotIn('tools:',(m.ROOT/'.github/agents'/f'{profile}.agent.md').read_text())
if __name__=='__main__':unittest.main()
