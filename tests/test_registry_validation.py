import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_registry import REGISTRY_PATH, validate_registry


class TestRegistryValidation(unittest.TestCase):
    def test_checked_in_registry_is_valid(self):
        self.assertEqual([], validate_registry())

    def test_validator_rejects_version_drift(self):
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        registry["version"] = "999.0.0"
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "registry.json"
            candidate.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("version does not match VERSION", validate_registry(candidate))
