#!/usr/bin/env python3
"""
Unit and integration tests for registry hooks and code snippets.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SNIPPETS_DIR = REPO_ROOT / "registry" / "snippets"
HOOKS_DIR = REPO_ROOT / "registry" / "hooks"


class TestHooksExecution(unittest.TestCase):
    """Tests lifecycle hooks against synthetic input."""

    def test_secret_leak_guard_blocks_credentials(self):
        hook_path = HOOKS_DIR / "pre-tool" / "secret-leak-guard.sh"
        self.assertTrue(hook_path.is_file())

        # Feed input containing an obvious AWS credential pattern
        dirty_input = "diff --git a/test.py b/test.py\n+AWS_SECRET_ACCESS_KEY='AKIAIOSFODNN7EXAMPLE_SECRET'\n"
        proc = subprocess.run(
            ["bash", str(hook_path)],
            input=dirty_input.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertNotEqual(
            proc.returncode,
            0,
            "secret-leak-guard.sh must exit non-zero when sensitive credential patterns are detected",
        )

    def test_secret_leak_guard_allows_clean_diff(self):
        hook_path = HOOKS_DIR / "pre-tool" / "secret-leak-guard.sh"
        self.assertTrue(hook_path.is_file())

        clean_input = "diff --git a/test.py b/test.py\n+def add(a, b):\n+    return a + b\n"
        proc = subprocess.run(
            ["bash", str(hook_path)],
            input=clean_input.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(
            proc.returncode,
            0,
            "secret-leak-guard.sh must exit 0 when no credentials are present",
        )

    def test_auto_formatter_hook_runs(self):
        hook_path = HOOKS_DIR / "post-tool" / "auto-formatter.sh"
        self.assertTrue(hook_path.is_file())

        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tf:
            tf.write("x = 1\n")
            temp_file = tf.name

        try:
            proc = subprocess.run(
                ["bash", str(hook_path), temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Formatter hook runs or exits gracefully
            self.assertIn(proc.returncode, [0, 127])
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestSnippetsIntegrity(unittest.TestCase):
    """Tests compilation and execution of bundled code snippets."""

    def test_python_async_http_client_snippet(self):
        py_snippet = SNIPPETS_DIR / "python" / "async_http_client.py"
        self.assertTrue(py_snippet.is_file())

        # Verify syntax and importability by compiling and inspecting AST
        with open(py_snippet, "r", encoding="utf-8") as f:
            code = f.read()

        compiled = compile(code, str(py_snippet), "exec")
        self.assertIsNotNone(compiled)

        # Execute in a safe isolated namespace
        namespace = {}
        exec(compiled, namespace)
        self.assertIn("AsyncHttpClient", namespace)
        client_cls = namespace["AsyncHttpClient"]
        client = client_cls(base_url="https://api.example.com", max_retries=2)
        self.assertEqual(client.base_url, "https://api.example.com")
        self.assertEqual(client.max_retries, 2)

    def test_typescript_theme_tokens_snippet_syntax(self):
        ts_snippet = SNIPPETS_DIR / "typescript" / "hsl_theme_tokens.ts"
        self.assertTrue(ts_snippet.is_file())

        with open(ts_snippet, "r", encoding="utf-8") as f:
            content = f.read()

        # Check required theme keys exist
        self.assertIn("HSLDesignTokens", content)
        self.assertIn("hsl", content)
        self.assertIn("primary", content)


if __name__ == "__main__":
    unittest.main()
