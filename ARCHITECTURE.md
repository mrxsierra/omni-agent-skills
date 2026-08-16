# 🏗️ omni-agent-skills: Master Architecture & Validation Specification

## 1. System Vision & Purpose
**`omni-agent-skills`** (`mrxsierra/omni-agent-skills`) is a universal, open-source skill registry, security harness, and cross-platform installer suite designed to extend AI coding agents (Google Antigravity, Claude Code, Cursor, Codex, OpenCode) without overloading context windows.

## 2. Core Architectural Principles
1. **Single-Responsibility Principle (SRP):** Each skill, subagent, and prompt is strictly scoped to a single expert task (e.g. `system-architecture-planner` *only* plans; `secret-leak-shield` *only* scans security) to eliminate context bleeding and hallucination risks.
2. **Verification Over Claiming:** Public metrics must be backed by reproducible checks, not by hand-written or auto-generated claims. For now, repo health is validated by smoke tests and security checks.
3. **Cross-Platform Desktop Native:** Ships with native installers for POSIX Linux/macOS (`install.sh`), Windows PowerShell (`install.ps1`), Python/`uv` (`pyproject.toml`), and Node/`npm` (`package.json`).
4. **Anonymized & Leak-Aware:** All scripts scan generic credential patterns. Private developer patterns use `.sanitize-local.json` (protected by `.gitignore`).

## 3. Directory Layout (v0.0.1)
```text
omni-agent-skills/
├── llms.txt                         # AI Search & RAG sitemap (v0.0.1)
├── qa_pairs_generic_tagged.json      # Tagged Q&A dataset for retrieval and indexing
├── README.md                        # Repository landing page and usage docs
├── SECURITY.md                      # Security policy & secret scanning guidance
├── LICENSE                          # MIT License
├── package.json                     # Node/npm Package metadata (v0.0.1)
├── pyproject.toml                   # Python/uv Package metadata (PEP 621)
├── .gitignore                       # Git exclusion rules (.sanitize-local.json, .env)
├── install.sh                       # POSIX (Linux/macOS/WSL) 1-Click Installer
├── install.ps1                      # Windows PowerShell 1-Click Installer
│
├── .agents/                         # Internal repo guidance and agent runbooks
│   ├── AGENTS.md                    # Operating guidelines for AI agents working on this repo
│   └── workflows/                   # Internal task execution workflows (feature-plan, pr-review, etc.)
│
├── registry/                        # Shippable Skill Registry & Asset Catalog
│   ├── registry.json                # Automated machine index of all skills
│   ├── skills/                      # Niche skill runbooks (engineering, web-and-geo, etc.)
│   ├── subagents/                   # Niche persona JSON configs (SRP scoped)
│   ├── rules/                       # Framework & security rules
│   ├── prompts/                     # Reusable system & task prompts
│   ├── snippets/                    # Reusable code snippets / gists
│   ├── hooks/                       # Executable pre/post tool hooks
│   └── mcp-configs/                 # Reusable MCP server templates
│
├── scripts/                         # Repo maintenance and validation scripts
│   ├── sanitize.py
│   ├── build-registry.py
│   └── run_workflow.py
│
└── tests/                           # Real repo integrity and smoke tests
    ├── test_repo_integrity.py
    └── test_workflow_runner.py
```

## 4. Initial Due Diligence & Threat Analysis
- **Threat 1: Accidental PII / Secret Leaks:** Mitigated via `scripts/sanitize.py`, `.gitignore`, and the repo validation pipeline.
- **Threat 2: Context Window Overload:** Solved by `registry.json` lazy-loading and focused skill discovery.
- **Threat 3: AI Hallucinations:** Solved via SRP single-task subagent scoping.
- **Threat 4: Unverified Claims:** Mitigated by removing public benchmark claims until a real CI-backed evaluation exists.

## 5. Project Roadmap
- **v0.0.1 (Current):** Alpha Scaffold - 15 Niche Skills, SRP Subagents, Security Shield, real smoke tests, `install.sh`/`install.ps1`, `llms.txt`, and registry-driven indexing.
- **v0.1.0 (Next):** Beta Launch - PyPI/NPM package publishing, scaffolding starters, and broader repo validation coverage.
- **v1.0.0 (Stable):** Production Release - Full MCP Integration, and Community Governance.
