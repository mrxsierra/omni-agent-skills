---
name: oss-launch-governance
description: Manages open-source pre-launch auditing, namespace availability verification, community governance documentation, and release readiness checklists.
---

# 🚀 Open-Source Phase-0 Pre-Launch & Governance Engine

The **OSS Launch Governance** skill coordinates pre-launch readiness checks, community governance documentation, package namespace availability audits, and repository hygiene before public release.

## 1. Inputs & Context Required
- **Project Identity:** Proposed project name, repository URL, maintainer identities, and description.
- **Target Distribution Targets:** Target package managers (e.g. PyPI, npm, Crates.io, Homebrew, Docker Hub).
- **Licensing & Policy:** Preferred open-source license (e.g. MIT, Apache-2.0) and security contact point.

## 2. Step-by-Step Procedure
1. **Namespace Availability Check:** Query target package registries and GitHub organization namespaces to confirm no name conflicts exist.
2. **Community Governance Scaffolding:** Create canonical governance documents: `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `SUPPORT.md`.
3. **Repository Workflow Templates:** Set up standard GitHub issue templates, pull request templates, and `.github/CODEOWNERS`.
4. **Clean History & Secret Audit:** Verify git commit history contains no secrets, API keys, credentials, or private credentials.
5. **Community Profile Audit:** Check repository settings and file locations to ensure 100% compliance with community health standards.

## 3. Expected Outputs & Artifacts
- **Governance Documentation Suite:** Complete set of OSI-compliant governance files.
- **Issue & PR Templates:** YAML issue forms and markdown pull request templates.
- **Pre-Launch Clearance Audit:** Checklist showing namespace clearance and hygiene verification status.

## 4. Constraints & Tool Neutrality
- **OSI Standards:** Follow Open Source Initiative licensing standards and Contributor Covenant codes of conduct.
- **Tool Neutral:** Usable across GitHub, GitLab, and self-hosted Git repositories.
