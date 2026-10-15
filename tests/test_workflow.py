import unittest

import storage
import workflow


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        storage.clear_requests()
        self.rid = storage.create_request("F001", "visitor")["id"]

    def test_issue_before_approval_rejected(self):
        with self.assertRaises(ValueError):
            workflow.issue_card(self.rid)
        self.assertEqual(storage.get_request(self.rid)["status"], "requested")

    def test_blank_approver_rejected(self):
        with self.assertRaises(ValueError):
            workflow.approve_request(self.rid, "   ")
        record = storage.get_request(self.rid)
        self.assertEqual(record["status"], "requested")
        self.assertIsNone(record["approved_by"])

    def test_full_workflow(self):
        workflow.approve_request(self.rid, "M01")
        workflow.issue_card(self.rid)
        workflow.return_card(self.rid)
        record = storage.get_request(self.rid)
        self.assertEqual(record["status"], "returned")
        self.assertEqual(record["approved_by"], "M01")

    def test_double_return_rejected(self):
        workflow.approve_request(self.rid, "M01")
        workflow.issue_card(self.rid)
        workflow.return_card(self.rid)
        with self.assertRaises(ValueError):
            workflow.return_card(self.rid)
        self.assertEqual(storage.get_request(self.rid)["status"], "returned")


if __name__ == "__main__":
    unittest.main()