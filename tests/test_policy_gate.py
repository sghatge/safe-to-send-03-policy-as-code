import unittest

from policy_gate import diff, evaluate, load

REC = load("policies/recommended.json")
AUTO = load("policies/autopilot.json")
SESSION = load("examples/session.json")


class PolicyGateTest(unittest.TestCase):
    def test_unknown_tool_fails_closed(self):
        self.assertEqual(evaluate(REC, {"tool": "data_export"})[0], "block")

    def test_first_matching_rule_wins(self):
        self.assertEqual(evaluate(REC, {"tool": "query_run", "is_write": True, "returns_pii": True})[0], "block")

    def test_volume_threshold(self):
        self.assertEqual(evaluate(REC, {"tool": "delivery_send", "qa_passed": True, "volume": 150000})[0], "needs_approval_x2")

    def test_compliance_workflow_protected(self):
        self.assertEqual(evaluate(REC, {"tool": "workflow_control", "compliance": True})[0], "block")

    def test_autopilot_diff_shows_every_loosened_call(self):
        changed = {c["call"] for c in diff(REC, AUTO, SESSION)}
        self.assertEqual(changed, {2, 5, 6, 8, 9, 10})

    def test_failed_qa_still_blocked_in_autopilot(self):
        self.assertEqual(evaluate(AUTO, {"tool": "delivery_send", "qa_passed": False})[0], "block")


if __name__ == "__main__":
    unittest.main()
