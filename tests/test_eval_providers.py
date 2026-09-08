#!/usr/bin/env python3
"""
Comprehensive Unit tests for the Pluggable Model Provider Engine and Evaluation Benchmark.
"""

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add scripts directory to path
REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from eval_providers import (
    AnthropicProvider,
    AntigravityCliProvider,
    AntigravityProvider,
    BaseModelProvider,
    MockProvider,
    ModelResponse,
    OllamaProvider,
    OpenAICompatibleProvider,
    get_provider,
)
from eval_asset import append_github_step_summary, evaluate_asset, load_task_suite, score_task
from build_eval_report import load_all_baselines, generate_markdown


class TestEvalProviders(unittest.TestCase):
    """Tests provider instantiation, payload serialization, and mock responses."""

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
        self.assertIn("latency_ms", resp.to_dict())

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

        anthropic_p = get_provider("anthropic", api_key="dummy-key")
        self.assertIsInstance(anthropic_p, AnthropicProvider)

        agy_p = get_provider("agy")
        self.assertIsInstance(agy_p, AntigravityCliProvider)
        self.assertEqual(agy_p.model_name, "gemini-3.8-flash-high")

    def test_unknown_provider_raises(self):
        with self.assertRaises(ValueError):
            get_provider("nonexistent-vendor-xyz")

    def test_provider_missing_key_raises(self):
        openai_p = OpenAICompatibleProvider(api_key="")
        with self.assertRaises(ValueError):
            openai_p.invoke([{"role": "user", "content": "test"}])

        antigravity_p = AntigravityProvider(api_key="")
        with self.assertRaises(ValueError):
            antigravity_p.invoke([{"role": "user", "content": "test"}])

        anthropic_p = AnthropicProvider(api_key="")
        with self.assertRaises(ValueError):
            anthropic_p.invoke([{"role": "user", "content": "test"}])

    @patch("urllib.request.urlopen")
    def test_ollama_provider_invoke_mocked(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "message": {"content": "Ollama generated response"},
            "prompt_eval_count": 25,
            "eval_count": 10,
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        ollama_p = OllamaProvider(model_name="qwen2.5-coder:7b")
        resp = ollama_p.invoke([{"role": "user", "content": "Write hello world"}], system_prompt="Sys")

        self.assertEqual(resp.text, "Ollama generated response")
        self.assertEqual(resp.prompt_tokens, 25)
        self.assertEqual(resp.completion_tokens, 10)
        self.assertEqual(resp.provider_name, "ollama")

    @patch("urllib.request.urlopen")
    def test_openai_provider_invoke_mocked(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": "OpenAI response text"}}],
            "usage": {"prompt_tokens": 40, "completion_tokens": 20},
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        openai_p = OpenAICompatibleProvider(api_key="sk-dummy", model_name="gpt-4o")
        resp = openai_p.invoke([{"role": "user", "content": "Test OpenAI"}])

        self.assertEqual(resp.text, "OpenAI response text")
        self.assertEqual(resp.prompt_tokens, 40)
        self.assertEqual(resp.completion_tokens, 20)

    @patch("urllib.request.urlopen")
    def test_antigravity_provider_invoke_mocked(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "candidates": [{"content": {"parts": [{"text": "Gemini response text"}]}}],
            "usageMetadata": {"promptTokenCount": 55, "candidatesTokenCount": 30},
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        antigravity_p = AntigravityProvider(api_key="dummy-gemini-key", model_name="gemini-2.5-pro")
        resp = antigravity_p.invoke([{"role": "user", "content": "Test Gemini"}], system_prompt="Sys prompt")

        self.assertEqual(resp.text, "Gemini response text")
        self.assertEqual(resp.prompt_tokens, 55)
        self.assertEqual(resp.completion_tokens, 30)

    @patch("urllib.request.urlopen")
    def test_anthropic_provider_invoke_mocked(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "content": [{"text": "Claude response text"}],
            "usage": {"input_tokens": 35, "output_tokens": 15},
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        anthropic_p = AnthropicProvider(api_key="dummy-anthropic-key", model_name="claude-3-5-sonnet")
        resp = anthropic_p.invoke([{"role": "user", "content": "Test Claude"}], system_prompt="Sys prompt")

        self.assertEqual(resp.text, "Claude response text")
        self.assertEqual(resp.prompt_tokens, 35)
        self.assertEqual(resp.completion_tokens, 15)

    @patch("subprocess.run")
    def test_agy_provider_invoke_mocked(self, mock_subproc):
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Antigravity CLI simulated response"
        mock_proc.stderr = ""
        mock_subproc.return_value = mock_proc

        agy_p = AntigravityCliProvider(model_name="gemini-3.8-flash-high")
        resp = agy_p.invoke([{"role": "user", "content": "Refactor this code"}], system_prompt="Sys")

        self.assertEqual(resp.text, "Antigravity CLI simulated response")
        self.assertEqual(resp.provider_name, "agy")
        self.assertEqual(resp.model_name, "gemini-3.8-flash-high")
        self.assertGreater(resp.total_tokens, 0)

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
        self.assertTrue(results.get("harness_verification_only"))

    def test_evaluate_security_shield_rule_mock(self):
        asset = REPO_ROOT / "registry" / "rules" / "global" / "security_shield.md"
        self.assertTrue(asset.is_file())

        provider = MockProvider()
        suite = load_task_suite(None, asset)
        self.assertIn("security_shield", suite["suite_id"])

        results = evaluate_asset(asset, provider, suite)
        self.assertTrue(results["passed_gate"])
        self.assertGreaterEqual(results["delta_utility"], 0.0)
        self.assertTrue(results.get("harness_verification_only"))

    def test_cli_execution_json_mode(self):
        cmd = [
            sys.executable,
            str(SCRIPTS_DIR / "eval_asset.py"),
            "--asset",
            "registry/skills/engineering/clean-code-auditor/SKILL.md",
            "--provider",
            "mock",
            "--json",
        ]
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout.decode("utf-8"))
        self.assertTrue(data.get("passed_gate"))
        self.assertEqual(data.get("provider"), "mock")
        self.assertTrue(data.get("harness_verification_only"))

    def test_append_github_step_summary(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tf:
            summary_file = tf.name

        try:
            with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary_file}):
                results = {
                    "asset_path": "registry/skills/engineering/clean-code-auditor/SKILL.md",
                    "provider": "mock",
                    "model": "mock-deterministic-v1",
                    "task_suite": "clean_code_audit",
                    "total_tasks": 2,
                    "baseline_pass_rate": 0.0,
                    "augmented_pass_rate": 100.0,
                    "delta_utility": 100.0,
                    "token_tax_per_turn": 522,
                    "passed_gate": True,
                    "verdict": "ACCEPTED (Positive Delta Utility)",
                    "harness_verification_only": True,
                }
                append_github_step_summary(results)

            with open(summary_file, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("### 📊 Asset Evaluation Scorecard: `clean-code-auditor`", content)
            self.assertIn("Deterministic Mock", content)
            self.assertIn("+100.0%", content)
            self.assertIn("✅ PASSED", content)
        finally:
            if os.path.exists(summary_file):
                os.remove(summary_file)

    def test_build_eval_report_generator(self):
        records = load_all_baselines()
        self.assertEqual(len(records), 16)

        md = generate_markdown(records)
        self.assertIn("# 📊 Empirical Evaluation & Quality Scorecard", md)
        self.assertIn("Multi-Tier Evaluation Architecture (ADR 0005)", md)
        self.assertIn("`clean-code-auditor`", md)
        self.assertIn("`security_shield.md`", md)


if __name__ == "__main__":
    unittest.main()
