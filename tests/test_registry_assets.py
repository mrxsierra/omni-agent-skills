#!/usr/bin/env python3
"""
Unit tests for Registry Asset Integrity across Subagents, MCP Configs, Prompts, and Rules.
Enforces that all physical asset types in registry/ adhere to their schemas and contracts.
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_DIR = REPO_ROOT / "registry"


class TestRegistrySubagents(unittest.TestCase):
    """Verifies all subagent configuration definitions in registry/subagents/."""

    def setUp(self):
        self.subagents_dir = REGISTRY_DIR / "subagents"
        self.assertTrue(self.subagents_dir.is_dir(), "registry/subagents/ directory must exist.")
        self.subagent_files = sorted(self.subagents_dir.glob("*.json"))

    def test_subagent_files_exist(self):
        self.assertGreaterEqual(len(self.subagent_files), 3, "Expected at least 3 subagents in registry/subagents/.")

    def test_subagents_json_schema_and_fields(self):
        required_keys = {
            "name": str,
            "role": str,
            "description": str,
            "system_prompt": str,
            "enable_write_tools": bool,
            "enable_mcp_tools": bool,
            "enable_subagent_tools": bool,
        }

        for path in self.subagent_files:
            with self.subTest(subagent=path.name):
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError as err:
                        self.fail(f"Subagent file '{path.name}' contains invalid JSON: {err}")

                # Check required fields and types
                for key, expected_type in required_keys.items():
                    self.assertIn(key, data, f"Subagent '{path.name}' missing required key '{key}'")
                    self.assertIsInstance(
                        data[key],
                        expected_type,
                        f"Subagent '{path.name}' key '{key}' must be of type {expected_type.__name__}",
                    )
                    if expected_type is str:
                        self.assertTrue(len(data[key].strip()) > 0, f"Subagent '{path.name}' key '{key}' must not be empty")

                # Name must match filename stem
                self.assertEqual(
                    data["name"],
                    path.stem,
                    f"Subagent '{path.name}' name '{data['name']}' must match filename stem '{path.stem}'",
                )


class TestRegistryMcpConfigs(unittest.TestCase):
    """Verifies all Model Context Protocol (MCP) configuration definitions in registry/mcp-configs/."""

    def setUp(self):
        self.mcp_dir = REGISTRY_DIR / "mcp-configs"
        self.assertTrue(self.mcp_dir.is_dir(), "registry/mcp-configs/ directory must exist.")
        self.mcp_files = sorted(self.mcp_dir.glob("*.json"))

    def test_mcp_config_files_exist(self):
        self.assertGreaterEqual(len(self.mcp_files), 1, "Expected at least 1 MCP config in registry/mcp-configs/.")

    def test_mcp_configs_json_schema(self):
        for path in self.mcp_files:
            with self.subTest(mcp_config=path.name):
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError as err:
                        self.fail(f"MCP config file '{path.name}' contains invalid JSON: {err}")

                self.assertIn("mcpServers", data, f"MCP config '{path.name}' must contain root 'mcpServers' object.")
                servers = data["mcpServers"]
                self.assertIsInstance(servers, dict, f"MCP config '{path.name}' 'mcpServers' must be a dict.")
                self.assertGreater(len(servers), 0, f"MCP config '{path.name}' must define at least one server.")

                for srv_name, srv_conf in servers.items():
                    self.assertIn("command", srv_conf, f"Server '{srv_name}' in '{path.name}' missing 'command'.")
                    self.assertIsInstance(srv_conf["command"], str, f"Server '{srv_name}' 'command' must be a str.")
                    self.assertTrue(len(srv_conf["command"].strip()) > 0, f"Server '{srv_name}' 'command' must not be empty.")

                    if "args" in srv_conf:
                        self.assertIsInstance(srv_conf["args"], list, f"Server '{srv_name}' 'args' must be a list.")
                        for arg in srv_conf["args"]:
                            self.assertIsInstance(arg, str, f"Server '{srv_name}' args elements must be strings.")


class TestRegistryPrompts(unittest.TestCase):
    """Verifies all Prompt and Persona templates in registry/prompts/."""

    def setUp(self):
        self.prompts_dir = REGISTRY_DIR / "prompts"
        self.assertTrue(self.prompts_dir.is_dir(), "registry/prompts/ directory must exist.")
        self.prompt_files = sorted(self.prompts_dir.rglob("*.md"))

    def test_prompt_files_exist(self):
        self.assertGreaterEqual(len(self.prompt_files), 1, "Expected at least 1 prompt in registry/prompts/.")

    def test_prompt_content_and_structure(self):
        for path in self.prompt_files:
            with self.subTest(prompt=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertGreater(len(content.strip()), 50, f"Prompt '{path.name}' is too short (< 50 chars).")

                # Check for top-level markdown heading
                self.assertTrue(
                    re.search(r"^#\s+", content, re.MULTILINE),
                    f"Prompt '{path.name}' must contain a top-level '# Heading'.",
                )

                # Check YAML frontmatter
                self.assertTrue(
                    content.startswith("---\n"),
                    f"Prompt '{path.name}' must start with YAML frontmatter delimiter '---'.",
                )
                parts = content.split("---\n", 2)
                self.assertGreaterEqual(len(parts), 3, f"Prompt '{path.name}' must have closing frontmatter delimiter '---'.")
                fm_text = parts[1]
                self.assertIn("name:", fm_text, f"Prompt '{path.name}' frontmatter must define 'name'.")
                self.assertIn("description:", fm_text, f"Prompt '{path.name}' frontmatter must define 'description'.")


class TestRegistryRules(unittest.TestCase):
    """Verifies all Rule files in registry/rules/ across global and framework categories."""

    def setUp(self):
        self.rules_dir = REGISTRY_DIR / "rules"
        self.assertTrue(self.rules_dir.is_dir(), "registry/rules/ directory must exist.")
        self.rule_files = sorted(self.rules_dir.rglob("*.md"))

    def test_all_expected_rules_exist(self):
        expected_rules = [
            "global/security_shield.md",
            "global/self_healing_diagnostics.md",
            "frameworks/python_rules.md",
            "frameworks/nextjs_rules.md",
        ]
        for rel_path in expected_rules:
            full_path = self.rules_dir / rel_path
            self.assertTrue(full_path.is_file(), f"Expected rule file '{rel_path}' does not exist on disk.")

    def test_rule_frontmatter_and_content_quality(self):
        valid_triggers = {"always_on", "model_decision", "manual"}

        for path in self.rule_files:
            with self.subTest(rule=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertGreater(len(content.strip()), 100, f"Rule '{path.name}' is too short (< 100 chars).")

                # Verify frontmatter exists
                self.assertTrue(
                    content.startswith("---\n"),
                    f"Rule '{path.name}' must start with YAML frontmatter delimiter '---'.",
                )
                parts = content.split("---\n", 2)
                self.assertGreaterEqual(len(parts), 3, f"Rule '{path.name}' must have closing frontmatter delimiter '---'.")
                fm_text = parts[1]

                # Trigger must be valid
                trigger_match = re.search(r"trigger:\s*(\w+)", fm_text)
                self.assertIsNotNone(trigger_match, f"Rule '{path.name}' must define 'trigger' in frontmatter.")
                trigger_val = trigger_match.group(1)
                self.assertIn(
                    trigger_val,
                    valid_triggers,
                    f"Rule '{path.name}' trigger '{trigger_val}' must be one of {valid_triggers}",
                )

                # Body must contain a top-level heading
                body = parts[2]
                self.assertTrue(
                    re.search(r"^#\s+", body, re.MULTILINE),
                    f"Rule '{path.name}' body must contain a top-level '# Heading'.",
                )


if __name__ == "__main__":
    unittest.main()
