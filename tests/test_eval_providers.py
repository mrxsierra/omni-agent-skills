#!/usr/bin/env python3
"""
Unit tests for the Pluggable Model Provider Engine and Evaluation Benchmark.
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from eval_providers import (
    AntigravityProvider,
    BaseModelProvider,
    MockProvider,
    ModelResponse,
    OllamaProvider,
    OpenAICompatibleProvider,
    get_provider,
)
from eval_asset import evaluate_asset, load_task_suite, score_task


class TestEvalProviders(unittest.TestCase):
    """Tests provider instantiation and interfaces."""

    def test_mock_provider_invocation(self):
        provider = MockProvider(model_name="test-mock")
        resp = provider.invoke(
            messages=[{"role": "user", "content": "hello world"}],
            system_prompt="system test",
        )
        self.assertIsInstance(resp, ModelResponse)
        self.assertEqual(resp.provider_name, "mock")
        self.assertEqual(resp.model_name, "test-mock")
        self.assertGreater(resp.total_tokens, 0)
        self.assertTrue(len(resp.text) > 0)

    def test_get_provider_factory(self):
        mock_p = get_provider("mock")
        self.assertIsInstance(mock_p, MockProvider)

        ollama_p = get_provider("ollama", model="llama3:8b")
        self.assertIsInstance(ollama_p, OllamaProvider)
        self.assertEqual(ollama_p.model_name, "llama3:8b")

        openai_p = get_provider("openai", model="gpt-4o", api_key="dummy-key")
        self.assertIsInstance(openai_p, OpenAICompatibleProvider)
        self.assertEqual(openai_p.provider_name, "openai")

        openrouter_p = get_provider("openrouter", api_key="dummy-key")
        self.assertIsInstance(openrouter_p, OpenAICompatibleProvider)
        self.assertEqual(openrouter_p.provider_name, "openrouter")

        antigravity_p = get_provider("antigravity", api_key="dummy-key")
        self.assertIsInstance(antigravity_p, AntigravityProvider)

    def test_unknown_provider_raises(self):
        with self.assertRaises(ValueError):
            get_provider("nonexistent-vendor-xyz")

    def test_score_task_pass(self):
        passed, reason = score_task(
            response_text="We must avoid DRY violations and flatten logic.",
            expected_keywords=["dry violation", "flatten"],
            fail_keywords=["looks good", "no issue"],
        )
        self.assertTrue(passed)

    def test_score_task_fail_on_prohibited(self):
        passed, reason = score_task(
            response_text="The code looks good and has no issues.",
            expected_keywords=["dry violation"],
            fail_keywords=["looks good"],
        )
        self.assertFalse(passed)
        self.assertIn("looks good", reason)


class TestEvalAssetRunner(unittest.TestCase):
    """End-to-end test of the evaluation runner in offline mock mode."""

    def test_evaluate_clean_code_skill_mock(self):
        asset = REPO_ROOT / "registry" / "skills" / "engineering" / "clean-code-auditor" / "SKILL.md"
        self.assertTrue(asset.is_file())

        provider = MockProvider()
        suite = load_task_suite(None, asset)
        self.assertIn("clean_code_audit", suite["suite_id"])

        results = evaluate_asset(asset, provider, suite)
        self.assertTrue(results["passed_gate"])
        self.assertGreaterEqual(results["delta_utility"], 0.0)
        self.assertEqual(results["provider"], "mock")

    def test_evaluate_security_shield_rule_mock(self):
        asset = REPO_ROOT / "registry" / "rules" / "global" / "security_shield.md"
        self.assertTrue(asset.is_file())

        provider = MockProvider()
        suite = load_task_suite(None, asset)
        self.assertIn("security_shield", suite["suite_id"])

        results = evaluate_asset(asset, provider, suite)
        self.assertTrue(results["passed_gate"])
        self.assertGreaterEqual(results["delta_utility"], 0.0)


if __name__ == "__main__":
    unittest.main()
