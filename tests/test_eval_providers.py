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
import urllib.error
import urllib.request
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
    get_model_capabilities,
    get_provider,
    http_request_with_retry,
    load_dotenv_if_exists,
)
from eval_asset import (
    append_github_step_summary,
    detect_changed_assets,
    evaluate_asset,
    get_all_evaluable_assets,
    load_task_suite,
    resolve_eval_tier,
    score_task,
)
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

        mistral_p = get_provider("mistral", api_key="dummy-key")
        self.assertIsInstance(mistral_p, OpenAICompatibleProvider)
        self.assertEqual(mistral_p.base_url, "https://api.mistral.ai/v1")
        self.assertEqual(mistral_p.model_name, "codestral-latest")

        mistralai_p = get_provider("mistralai", api_key="dummy-key")
        self.assertIsInstance(mistralai_p, OpenAICompatibleProvider)

        gemini_p = get_provider("gemini", api_key="dummy-key")
        self.assertIsInstance(gemini_p, AntigravityProvider)
        self.assertEqual(gemini_p.model_name, "gemini-2.5-flash")

        google_p = get_provider("google", api_key="dummy-key")
        self.assertIsInstance(google_p, AntigravityProvider)

    def test_unknown_provider_raises(self):
        with self.assertRaises(ValueError):
            get_provider("nonexistent-vendor-xyz")

    def test_provider_missing_key_raises(self):
        openai_p = OpenAICompatibleProvider(api_key="", provider_name="openai")
        with self.assertRaises(ValueError):
            openai_p.invoke([{"role": "user", "content": "test"}])

        mistral_p = OpenAICompatibleProvider(api_key="", provider_name="mistral")
        with self.assertRaises(ValueError):
            mistral_p.invoke([{"role": "user", "content": "test"}])

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

    @patch("time.sleep")
    @patch("urllib.request.urlopen")
    def test_http_request_with_retry_on_429(self, mock_urlopen, mock_sleep):
        req = urllib.request.Request("https://api.example.com", data=b"{}")

        # Mock first call returns 429 HTTPError, second call succeeds
        err_429 = urllib.error.HTTPError(
            url="https://api.example.com",
            code=429,
            msg="Too Many Requests",
            hdrs=None,
            fp=io.BytesIO(b'{"error": "rate limit"}'),
        )
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"success": true}'
        mock_context = MagicMock()
        mock_context.__enter__.return_value = mock_resp

        mock_urlopen.side_effect = [err_429, mock_context]

        data = http_request_with_retry(
            req=req,
            provider_name="test-prov",
            model_name="test-model",
            max_retries=2,
            base_delay=0.01,
        )
        self.assertTrue(data.get("success"))
        self.assertEqual(mock_urlopen.call_count, 2)
        mock_sleep.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_http_request_openrouter_402_guidance(self, mock_urlopen):
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=b"{}")
        err_402 = urllib.error.HTTPError(
            url="https://openrouter.ai/api/v1/chat/completions",
            code=402,
            msg="Payment Required",
            hdrs=None,
            fp=io.BytesIO(b'{"error": {"message": "insufficient credits"}}'),
        )
        mock_urlopen.side_effect = err_402

        with self.assertRaises(RuntimeError) as ctx:
            http_request_with_retry(
                req=req,
                provider_name="openrouter",
                model_name="anthropic/claude-3.5-sonnet",
                max_retries=1,
            )
        self.assertIn("OpenRouter 402 Payment Required", str(ctx.exception))
        self.assertIn(":free", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_http_request_gemini_404_guidance(self, mock_urlopen):
        req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent", data=b"{}")
        err_404 = urllib.error.HTTPError(
            url="https://generativelanguage.googleapis.com",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=io.BytesIO(b'{"error": {"message": "models/gemini-2.5-pro is no longer available"}}'),
        )
        mock_urlopen.side_effect = err_404

        with self.assertRaises(RuntimeError) as ctx:
            http_request_with_retry(
                req=req,
                provider_name="gemini",
                model_name="gemini-2.5-pro",
                max_retries=1,
            )
        self.assertIn("Google Gemini 404 Not Found", str(ctx.exception))
        self.assertIn("gemini-2.5-flash", str(ctx.exception))

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
        self.assertIn("Multi-Tier Evaluation Architecture (ADR 0005 & ADR 0006)", md)
        self.assertIn("`clean-code-auditor`", md)
        self.assertIn("`security_shield.md`", md)

    def test_get_all_evaluable_assets(self):
        assets = get_all_evaluable_assets()
        self.assertEqual(len(assets), 16)
        paths = [str(p) for p in assets]
        self.assertTrue(any("clean-code-auditor" in p for p in paths))
        self.assertTrue(any("security_shield.md" in p for p in paths))

    def test_detect_changed_assets(self):
        mock_output = "registry/skills/engineering/clean-code-auditor/SKILL.md\nREADME.md\n"
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout=mock_output)
            changed = detect_changed_assets("origin/dev")
            self.assertEqual(len(changed), 1)
            self.assertTrue(str(changed[0]).endswith("clean-code-auditor/SKILL.md"))

    def test_resolve_eval_tier(self):
        """Verify dynamic evaluation tier resolution (ADR 0006)."""
        # Explicit suite override
        tier, label = resolve_eval_tier(Path("registry/skills/engineering/custom/SKILL.md"), {"eval_tier": "S"})
        self.assertEqual(tier, "S")
        self.assertIn("Tier S", label)

        tier, label = resolve_eval_tier(Path("registry/skills/engineering/custom/SKILL.md"), {"eval_tier": "L"})
        self.assertEqual(tier, "L")
        self.assertIn("Tier L", label)

        # Taxonomy fallbacks
        tier, label = resolve_eval_tier(Path("registry/rules/global/security_shield.md"))
        self.assertEqual(tier, "S")
        self.assertIn("Taxonomy Default", label)

        tier, label = resolve_eval_tier(Path("registry/skills/security-and-governance/secret-leak-shield/SKILL.md"))
        self.assertEqual(tier, "S")

        tier, label = resolve_eval_tier(Path("registry/skills/architecture/system-planner/SKILL.md"))
        self.assertEqual(tier, "L")

        tier, label = resolve_eval_tier(Path("registry/skills/engineering/clean-code-auditor/SKILL.md"))
        self.assertEqual(tier, "M")

    def test_score_task_rigor_modes(self):
        """Verify task rigor scoring with match_mode and min_matches (ADR 0006)."""
        text = "We added mock fixtures to assert contracts and guard clauses."

        # Any mode (legacy default, min_matches=1)
        passed, reason = score_task(text, ["mock", "forbidden"], ["fail_keyword"])
        self.assertTrue(passed)

        # Fail keywords take absolute priority
        bad_text = "We will make actual http call to production."
        passed, reason = score_task(bad_text, ["mock"], ["make actual http call to production"])
        self.assertFalse(passed)
        self.assertIn("forbidden keyword", reason)

        # All mode: requires every keyword
        passed, reason = score_task(text, ["mock", "fixtures", "assert"], [], match_mode="all")
        self.assertTrue(passed)

        passed, reason = score_task(text, ["mock", "fixtures", "missing_word"], [], match_mode="all")
        self.assertFalse(passed)
        self.assertIn("Missing required keywords", reason)

        # Configurable min_matches threshold
        passed, reason = score_task(text, ["mock", "fixtures", "missing_1", "missing_2"], [], min_matches=2)
        self.assertTrue(passed)

        passed, reason = score_task(text, ["mock", "fixtures", "missing_1", "missing_2"], [], min_matches=3)
        self.assertFalse(passed)
        self.assertIn("Matched only 2/3", reason)

    def test_get_model_capabilities(self):
        """Verify model capability resolution across providers and models."""
        mock_caps = get_model_capabilities("mock", "mock-deterministic-v1")
        self.assertIn("instruction_following", mock_caps)
        self.assertIn("tool_calling", mock_caps)
        self.assertIn("structured_json", mock_caps)

        gemini_caps = get_model_capabilities("gemini", "gemini-2.5-flash")
        self.assertIn("tool_calling", gemini_caps)
        self.assertIn("code_generation", gemini_caps)

        codestral_caps = get_model_capabilities("mistral", "codestral-latest")
        self.assertIn("code_generation", codestral_caps)
        self.assertIn("structured_json", codestral_caps)

        small_caps = get_model_capabilities("ollama", "qwen2.5-coder:1.5b")
        self.assertIn("code_generation", small_caps)
        self.assertNotIn("tool_calling", small_caps)
        self.assertNotIn("long_context", small_caps)

    def test_openrouter_free_model_default(self):
        """Verify OpenRouter defaults to a zero-cost :free model while allowing overrides."""
        p_default = get_provider("openrouter", api_key="test-key")
        self.assertEqual(p_default.model_name, "meta-llama/llama-3.3-70b-instruct:free")

        p_custom = get_provider("openrouter", model="anthropic/claude-3.5-sonnet", api_key="test-key")
        self.assertEqual(p_custom.model_name, "anthropic/claude-3.5-sonnet")

    def test_capability_mismatch_guard_raises_and_bypasses(self):
        """Verify that evaluate_asset enforces required capabilities unless explicitly bypassed."""
        # Create mock provider acting as an under-capable model
        provider = MockProvider(model_name="qwen2.5-coder:1.5b")
        provider.provider_name = "ollama"  # Simulate non-mock provider check

        suite = {
            "suite_id": "test_mcp_tool_suite",
            "eval_tier": "L",
            "required_capabilities": ["tool_calling"],
            "tasks": [
                {
                    "id": "t1",
                    "user_prompt": "run tool",
                    "expected_keywords": ["tool"],
                }
            ],
        }
        asset_path = REPO_ROOT / "registry" / "rules" / "global" / "security_shield.md"

        # Should raise ValueError due to missing tool_calling capability
        with self.assertRaises(ValueError) as ctx:
            evaluate_asset(asset_path, provider, suite, ignore_capability_mismatch=False)
        self.assertIn("Capability Mismatch", str(ctx.exception))
        self.assertIn("tool_calling", str(ctx.exception))

        # Should pass when ignore_capability_mismatch=True
        results = evaluate_asset(asset_path, provider, suite, ignore_capability_mismatch=True)
        self.assertIn("passed_gate", results)


if __name__ == "__main__":
    unittest.main()
