#!/usr/bin/env python3
"""
Unit tests for preflight API key verification and diagnostics tooling (ADR 0006).
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from scripts.check_api_keys import (
    check_agy_cli,
    check_ollama,
    check_openrouter_quota,
    mask_key,
    probe_provider,
    run_checks,
)


class TestCheckApiKeys(unittest.TestCase):
    """Test suite for preflight API key verification and diagnostics."""

    def test_mask_key_security(self):
        """Verify that API keys are always masked and never leaked in plain text."""
        self.assertEqual(mask_key(None), "(not set)")
        self.assertEqual(mask_key(""), "(not set)")
        self.assertEqual(mask_key("   "), "(not set)")
        self.assertEqual(mask_key("12345"), "***")
        self.assertEqual(mask_key("12345678"), "***")

        # Standard OpenAI / OpenRouter key format
        key = "sk-or-v1-abcdef1234567890abcdef6eb"
        masked = mask_key(key)
        self.assertTrue(masked.startswith("sk-o..."))
        self.assertTrue(masked.endswith("6eb"))
        self.assertNotIn("1234567890", masked)
        self.assertEqual(masked, "sk-o...6eb")

        # Google Gemini key format
        gemini_key = "AIzaSyD1234567890abcdefghijklmJfQ"
        masked_gemini = mask_key(gemini_key)
        self.assertEqual(masked_gemini, "AIza...JfQ")
        self.assertNotIn("1234567890", masked_gemini)

    def test_probe_provider_mock_mode(self):
        """Verify that mock probe mode returns instantaneous success without network calls."""
        ok, reply, latency, note = probe_provider("gemini", "gemini-2.5-flash", is_mock=True)
        self.assertTrue(ok)
        self.assertEqual(reply, "pong")
        self.assertEqual(note, "Mock verification pass")
        self.assertLessEqual(latency, 50.0)

    def test_run_checks_mock_mode(self):
        """Verify that full preflight check runs cleanly in mock simulation mode."""
        exit_code = run_checks(is_mock=True)
        self.assertEqual(exit_code, 0)

    def test_check_ollama_offline_graceful(self):
        """Verify that offline Ollama daemon is handled gracefully without crashing."""
        result = check_ollama(base_url="http://127.0.0.1:59999", timeout=1)
        self.assertFalse(result["ok"])
        self.assertIn("not running", result["note"])

    @patch("urllib.request.urlopen")
    def test_check_openrouter_quota_parsing(self, mock_urlopen):
        """Verify that OpenRouter key metadata is parsed accurately."""
        mock_response = MagicMock()
        mock_response.read.return_value = (
            b'{"data": {"is_free_tier": true, "usage_daily": 4, "limit": null}}'
        )
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        quota = check_openrouter_quota("fake-key", timeout=1)
        self.assertTrue(quota["ok"])
        self.assertTrue(quota["is_free_tier"])
        self.assertEqual(quota["usage_daily"], 4)
        self.assertIn("Free Tier (50 req/day cap)", quota["quota_label"])


if __name__ == "__main__":
    unittest.main()
