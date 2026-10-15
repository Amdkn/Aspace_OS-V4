import unittest
from tools.pr_life_status_guard import inspect

class PRLifeStatusGuardTests(unittest.TestCase):
    def test_direct_life_outcome_issue_is_blocked(self):
        self.assertEqual(inspect("Tech PR", "Related to SOH-148"), ["SOH-148"])
        self.assertEqual(inspect("SOH-152 implementation", ""), ["SOH-152"])
        self.assertEqual(inspect("", "SOH-145 and SOH-147"), ["SOH-145", "SOH-147"])

    def test_tech_issues_can_be_referenced_without_life_auto_close(self):
        self.assertEqual(inspect("Factory handoff", "Refs SOH-154 and SOB-13"), [])
        self.assertEqual(inspect("No domain key", "Bill/Tilly/LD04"), [])

    def test_guard_not_infer_live_linear_settings(self):
        self.assertEqual(inspect("Fix factory", "Related GitHub #78"), [])

if __name__=="__main__":
    unittest.main()
