# 🏗️ omni-agent-skills: Master Architecture & Roadmap Specification

## 1. System Vision & Purpose
**`omni-agent-skills`** (`mrxsierra/omni-agent-skills`) is a universal, open-source skill registry, security harness, and reusable asset ecosystem designed to extend AI coding agents (Google Antigravity, Claude Code, Cursor, Codex, OpenCode, Gemini) without overloading context windows or system prompts.

## 2. Core Architectural Principles
1. **Single-Responsibility Principle (SRP):** Each skill, subagent, and prompt is strictly scoped to a single expert task (e.g. `system-architecture-planner` *only* plans; `secret-leak-shield` *only* scans security) to eliminate context bleeding and hallucination risks.
2. **Lazy Loading for AI Agents:** AI agents query `registry.json` or `/llms.txt` and fetch ONLY the specific `SKILL.md` needed for a given task.
3. **Update-First Deduplication:** Rather than creating hundreds of redundant files, new patterns are merged into existing domain skills (`engineering`, `web-and-geo`, `data-and-ai`, `security-and-governance`).
4. **100% Anonymized & PII-Free:** All skills, rules, prompts, snippets, and scaffolds use generic placeholders (`your-org`, `YOUR_API_KEY`). Private files (`bio.md`, `private_client_targets.md`, `journal.md`) are strictly excluded.
5. **Empirical Verification & Security Shield:** Built-in secret detection rules (`gitleaks`), staging-first protection (`drafts/`), and self-healing diagnostic loops (`self_healing_diagnostics`).

## 3. Directory Layout (v0.0.1)
```text
omni-agent-skills/
├── llms.txt                         # AI Search & RAG sitemap (v0.0.1)
├── registry.json                    # Automated 1-line machine index of all skills (v0.0.1)
├── qa_pairs_generic_tagged.json      # High-precision vector dataset (>95% match accuracy)
├── README.md                        # High-converting open-source landing page
├── BENCHMARKS.md                    # Empirical Evaluation Proof & Multi-Model Matrix
├── SECURITY.md                      # Security policy & secret scanning rules
├── LICENSE                          # MIT License
├── package.json                     # Node/npm Package metadata (v0.0.1)
├── pyproject.toml                   # Python/uv Package metadata (PEP 621, v0.0.1)
├── .gitignore                       # Git exclusion rules (.sanitize-local.json, .env)
├── install.sh                       # 1-Click executable installer script
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
├── scripts/                         # Auto-Indexers & Security Sanitizer
│   ├── sanitize.py                  (Passed 100% ✅)
│   └── build-registry.py            (Passed 100% ✅)
│
├── skills/                          # 15 Niche Skill Runbooks (No ECC words!)
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
- **Threat 1: Accidental PII / Secret Leaks:** Prevented via `scripts/sanitize.py` CI check and generic placeholders (`your-org`).
- **Threat 2: Context Window Overload:** Solved by `registry.json` lazy-loading.
- **Threat 3: AI Hallucinations:** Solved via SRP single-task subagent scoping.
- **Threat 4: Duplicate / Bloated Skills:** Solved via update-first deduplication protocol.

## 5. Project Roadmap
- **v0.0.1 (Current):** Alpha Scaffold - Initial 15 Niche Skills, SRP Subagents, Security Shield, Sanitizer Script, `llms.txt`, and RAG Dataset.
- **v0.1.0 (Next):** Beta Launch - Multi-harness CLI testing, PyPI/NPM package publishing, and 5 scaffolding starters.
- **v1.0.0 (Stable):** Production Release - 1-Click Installer, Full MCP Integration, and Community Governance.
