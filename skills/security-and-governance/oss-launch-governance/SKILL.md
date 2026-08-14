---
name: oss-launch-governance
description: Manage end-to-end Open-Source Phase-0 pre-launch auditing, namespace & registry clearance (PyPI, npm, Crates, Homebrew, USPTO, GitHub Orgs), community health governance (CODEOWNERS, SECURITY.md, GOVERNANCE.md), contributor ladders, T-Minus launch countdown execution (T-30 to T+1), grant/funding readiness, and zero-leak commit sanitization for any open-source software project. Trigger when preparing to open-source a repo, checking namespace availability, auditing pre-launch health, or establishing open-source governance.
---

# 🚀 Open-Source Phase-0 Pre-Launch & Governance Engine

This skill provides the comprehensive protocol for preparing, clearing, and launching high-impact open-source software projects.

## 1. Brand Namespace Clearance Matrix
Before naming an open-source project, execute automated namespace availability checks:
- **PyPI / npm / Crates.io / Cargo / RubyGems:** Check package name availability via API/CLI.
- **Homebrew Formulae / Docker Hub:** Verify container and package formula namespaces.
- **GitHub Orgs & Usernames:** Audit `github.com/<name>` and `github.com/<name>-os`.

## 2. Phase-0 Pre-Launch Checklist
- **Community Governance Files:** Create `LICENSE` (MIT/Apache-2.0), `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `GOVERNANCE.md`.
- **Zero-Leak Commit Sanitization:** Audit full git history using `gitleaks` or `trufflehog` to ensure zero API keys or `.env` files exist in past commits.
- **Grant & Funding Readiness:** Include `SPONSORS.md` and `FUNDING.yml`.
