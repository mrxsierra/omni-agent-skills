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
├── registry.json                    # Automated machine index of all skills (v0.0.1)
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
├── subagents/                       # Niche Persona JSON Configs (SRP Scoped)
│   ├── system-architecture-planner.json
│   ├── secret-leak-shield.json
│   └── code-anti-overengineer.json
│
├── hooks/                           # Executable Pre/Post Tool Hooks
│   ├── pre-tool/secret-leak-guard.sh
│   └── post-tool/auto-formatter.sh
│
├── prompts/                         # Reusable System & Task Prompts
│   └── system/architect-persona.md
│
├── snippets/                        # Reusable Code Snippets / Gists
│   ├── python/async_http_client.py
│   └── typescript/hsl_theme_tokens.ts
│
├── mcp-configs/                     # Reusable MCP Server Templates
│   └── chrome-devtools.json
│
├── scripts/                         # Repo maintenance and validation scripts
│   ├── sanitize.py
│   ├── build-registry.py
│   └── tests/ (or smoke checks under tests/)
│
├── tests/                           # Real repo integrity and smoke tests
│   └── test_repo_integrity.py
│
├── skills/                          # Niche skill runbooks
│   ├── engineering/                 # Planner, Implementer, Pytest, Reviewer, Simplifier, Release
│   ├── web-and-geo/                 # GEO, A11y Web Auditor
│   ├── data-and-ai/                 # RAG QA Chunking Engine, AI Eval Benchmarker
│   └── security-and-governance/     # Secret Shield, OSS Governance, Tech Competitive Intel
│
└── rules/                           # Framework & Security Rules
    ├── global/                      # security_shield.md, self_healing_diagnostics.md
    └── frameworks/                  # python_rules.md, nextjs_rules.md
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
