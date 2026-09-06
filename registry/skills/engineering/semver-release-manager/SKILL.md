---
name: semver-release-manager
description: Manages Semantic Versioning lifecycle, validates release metadata, updates changelogs, and orchestrates GitHub release workflows.
---

# 📦 SemVer Release Manager

The **SemVer Release Manager** coordinates repository release packaging, version bumping, changelog maintenance, and GitHub release publication.

## 1. Inputs & Context Required
- **Target Version Increment:** SemVer target increment (`patch`, `minor`, `major`) or explicit version string (e.g. `v0.1.0`).
- **Commit History:** Commit log since the previous release tag (`git log <last-tag>..HEAD --oneline`).
- **Repository Manifests:** Version source files (e.g. `VERSION`, `package.json`, `pyproject.toml`) and `CHANGELOG.md`.

## 2. Step-by-Step Procedure
1. **Version Parity Check:** Verify that the current version manifest matches the latest git tag before incrementing.
2. **Changelog Assembly:** Aggregate unreleased commits into structured sections following Keep a Changelog (`Added`, `Changed`, `Fixed`, `Removed`).
3. **Pre-Release Verification:** Run the workspace verification suite (tests, linters, integrity checks) to ensure release readiness.
4. **Version Manifest Bump:** Update repository version files and commit changes with a conventional release commit message.
5. **Tag & Publish:** Create an annotated git tag and publish the release with formatted release notes via GitHub CLI or CI workflow.

## 3. Expected Outputs & Artifacts
- **Updated `CHANGELOG.md`:** Formatted entry with version number, release date, and categorized change list.
- **Synchronized Version Manifests:** Target files reflecting the new SemVer version.
- **Release Tag & Notes:** Annotated git tag and published release with release assets.

## 4. Constraints & Tool Neutrality
- **SemVer Compliance:** Strictly follow Semantic Versioning (breaking changes require major bump; backwards-compatible additions require minor bump).
- **Release Gating:** Never tag or release without a passing verification test suite.
- **Tool Neutral:** Compatible with GitHub CLI (`gh`), standard Git CLI, or automated CI/CD release pipelines.
