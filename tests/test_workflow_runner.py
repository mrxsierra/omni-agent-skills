import json
import os
import tempfile
import unittest

from scripts.run_workflow import run


class TestWorkflowRunner(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.outdir = os.path.join(self.temp_dir.name, "runs")
        os.makedirs(self.outdir, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_run_pr_review_creates_log(self):
        log = run("pr-review", self.outdir)
        self.assertTrue(os.path.exists(log))
        with open(log, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["workflow_id"], "pr-review")
        self.assertIn("steps", data)

    def test_run_feature_plan_creates_log(self):
        log = run("feature-plan", self.outdir)
        self.assertTrue(os.path.exists(log))
        with open(log, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["workflow_id"], "feature-plan")
        self.assertIn("steps", data)

    def test_run_security_audit_creates_log(self):
        log = run("security-audit", self.outdir)
        self.assertTrue(os.path.exists(log))
        with open(log, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["workflow_id"], "security-audit")
        self.assertIn("steps", data)

    def test_run_feature_delivery_creates_log(self):
        log = run("feature-delivery", self.outdir)
        self.assertTrue(os.path.exists(log))
        with open(log, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["workflow_id"], "feature-delivery")
        self.assertIn("steps", data)


if __name__ == "__main__":
    unittest.main()
