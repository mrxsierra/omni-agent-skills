import json
import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestRepoIntegrity(unittest.TestCase):
    def test_registry_exists_and_has_skill_entries(self):
        registry_path = os.path.join(REPO_ROOT, "registry.json")
        self.assertTrue(os.path.exists(registry_path), "registry.json is missing")

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

        with open(os.path.join(REPO_ROOT, "registry.json"), "r", encoding="utf-8") as f:
            registry = json.load(f)

        skill_ids = [skill["id"] for skill in registry.get("skills", [])]
        for skill_id in skill_ids:
            self.assertIn(skill_id, llms_text, f"llms.txt does not include {skill_id}")

    def test_required_project_files_exist(self):
        required = [
            "README.md",
            "LICENSE",
            "registry.json",
            "llms.txt",
            "scripts/build-registry.py",
            "scripts/sanitize.py",
            "package.json",
        ]

        for relative in required:
            full_path = os.path.join(REPO_ROOT, relative)
            self.assertTrue(os.path.exists(full_path), f"Required file missing: {relative}")


if __name__ == "__main__":
    unittest.main()
