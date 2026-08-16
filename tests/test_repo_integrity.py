import json
import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestRepoIntegrity(unittest.TestCase):
    def test_registry_exists_and_has_skill_entries(self):
        registry_path = os.path.join(REPO_ROOT, "registry", "registry.json")
        self.assertTrue(os.path.exists(registry_path), "registry/registry.json is missing")

        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)

        skills = registry.get("skills", [])
        self.assertTrue(skills, "registry.json does not contain any skills")

        for skill in skills:
            skill_id = skill.get("id")
            skill_path = skill.get("path")
            self.assertTrue(skill_id, f"Skill entry missing id: {skill}")
            self.assertTrue(skill_path, f"Skill {skill_id} missing path")
            self.assertTrue(
                os.path.exists(os.path.join(REPO_ROOT, skill_path)),
                f"Skill file for {skill_id} is missing: {skill_path}",
            )

    def test_llms_file_references_registry(self):
        llms_path = os.path.join(REPO_ROOT, "llms.txt")
        self.assertTrue(os.path.exists(llms_path), "llms.txt is missing")

        with open(llms_path, "r", encoding="utf-8") as f:
            llms_text = f.read()

        with open(os.path.join(REPO_ROOT, "registry", "registry.json"), "r", encoding="utf-8") as f:
            registry = json.load(f)

        skill_ids = [skill["id"] for skill in registry.get("skills", [])]
        for skill_id in skill_ids:
            self.assertIn(skill_id, llms_text, f"llms.txt does not include {skill_id}")

    def test_required_project_files_exist(self):
        required = [
            "README.md",
            "LICENSE",
            "registry/registry.json",
            "llms.txt",
            "scripts/build-registry.py",
            "scripts/sanitize.py",
            "package.json",
        ]

        for relative in required:
            full_path = os.path.join(REPO_ROOT, relative)
            self.assertTrue(os.path.exists(full_path), f"Required file missing: {relative}")

    def test_repo_has_no_false_benchmark_claims_or_stale_benchmark_artifacts(self):
        active_files = {
            "README.md": os.path.join(REPO_ROOT, "README.md"),
            "ARCHITECTURE.md": os.path.join(REPO_ROOT, "ARCHITECTURE.md"),
            ".agents/AGENTS.md": os.path.join(REPO_ROOT, ".agents", "AGENTS.md"),
            ".github/workflows/ci.yml": os.path.join(REPO_ROOT, ".github", "workflows", "ci.yml"),
        }

        combined_text = ""
        for label, path in active_files.items():
            self.assertTrue(os.path.exists(path), f"Missing active repo file for benchmark guard: {label}")
            with open(path, "r", encoding="utf-8") as f:
                combined_text += f"\n# {label}\n{f.read().lower()}"

        self.assertIn(
            "this repository does not publish benchmark performance claims",
            combined_text,
            "Expected the repo to explicitly reject unsupported benchmark claims.",
        )
        self.assertIn(
            "python3 -m unittest discover -s tests -p 'test_*.py'",
            combined_text,
            "Expected the active CI workflow to use the real smoke-test command, not a stale benchmark runner.",
        )

        stale_patterns = [
            "pytest-benchmark",
            "benchmark.py",
            "run-benchmark",
            "benchmark-results",
            "benchmark_results",
            "results.json",
            "coverage.xml",
            "artifacts/benchmark",
            "state-of-the-art",
            "best-in-class",
            "beats all",
            "100% accuracy",
        ]
        for pattern in stale_patterns:
            self.assertNotIn(pattern, combined_text, f"Found stale benchmark or unsupported claim pattern: {pattern}")

        ci_text = combined_text.split("# .github/workflows/ci.yml\n", 1)[1] if "# .github/workflows/ci.yml" in combined_text else combined_text
        self.assertNotIn("upload-artifact", ci_text, "CI workflow should not generate benchmark evidence artifacts.")
        self.assertNotIn("benchmark", ci_text, "CI workflow should avoid benchmark runner references and generated evidence uploads.")


if __name__ == "__main__":
    unittest.main()
