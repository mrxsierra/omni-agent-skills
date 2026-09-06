# 🏗️ omni-agent-skills: Master Architecture & Discovery Specification

## 1. System Vision & Purpose

**`omni-agent-skills`** is a portable, tool-neutral open-source skill registry and asset catalog designed to extend AI coding agents (such as Google Antigravity, Claude Code, Cursor, Codex, and OpenCode) without overloading system prompts or context windows.

Per [ADR 0001](docs/adr/0001-registry-not-control-plane.md), this repository strictly publishes reusable assets and the tooling needed to discover, validate, and install them. It is not an autonomous control plane or runtime orchestration engine.

---

## 2. Three-Tier Agent Discovery Architecture

To support diverse agent workflows and search engines, the repository exposes three distinct, complementary discovery tiers:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       omni-agent-skills Discovery Layers                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
      ┌────────────────────────────────┼────────────────────────────────┐
      ▼                                ▼                                ▼
  Tier 1: Agent Catalog         Tier 2: LLM Sitemap            Tier 3: RAG & Semantic QA
 [registry/registry.json]          [llms.txt]                     [llms-qa.json]
   • Machine-readable index       • Human & LLM text sitemap    • Chunked, tagged Q&A pairs
   • Skill paths & metadata       • Cursor/Copilot context      • Dense vector retrieval
   • Tool invocation & loading    • LLM crawler index           • Zero context fragmentation
```

1. **Tier 1 — Executable Asset Registry ([`registry/registry.json`](registry/registry.json)):**
   Machine-readable catalog generated from [`registry/skills/`](registry/skills/) and validated against [`registry/registry.schema.json`](registry/registry.schema.json). AI agents query this index on demand to inspect and load relevant skills.
2. **Tier 2 — LLM Context Sitemap ([`llms.txt`](llms.txt)):**
   Compact Markdown overview following the `/llmstxt.org` convention. Designed for fast context-window ingestion and search crawlers.
3. **Tier 3 — Semantic Q&A Retrieval ([`llms-qa.json`](llms-qa.json)):**
   Pre-chunked, tagged Q&A pairs optimized for vector embedding models and RAG retrieval engines, dogfooding the repository's [`rag-qa-chunking-engine`](registry/skills/data-and-ai/rag-qa-chunking-engine/SKILL.md) specification.

---

## 3. Core Architectural Principles

1. **Single-Responsibility Principle (SRP):** Each skill, rule, and asset is strictly scoped to a single expert capability to prevent context bleed and maintain high precision.
2. **Verification Over Claiming:** This repository does not publish benchmark performance claims unless backed by reproducible CI runs with explicit golden data and reviewable artifacts.
3. **Safe-by-Default Execution:** Reference runners and installation helpers are simulation-first and non-destructive. Shell execution requires explicit maintainer configuration.
4. **Tool Neutrality:** Published assets declare clear constraints, inputs, and expected outputs without assuming vendor-specific runtime privileges.
5. **Secret Hygiene:** Scans for obvious secret and credential patterns using `scripts/sanitize.py` and protects private local overrides via `.gitignore`.

---

## 4. Directory Layout

```text
omni-agent-skills/
├── llms.txt                         # Tier-2 AI Search & RAG sitemap
├── llms-qa.json                     # Tier-3 Tagged Q&A dataset for RAG vector search
├── README.md                        # Project landing page and entry point
├── SECURITY.md                      # Security policy and secret-scanning guidance
├── LICENSE                          # MIT License
├── package.json                     # Node/npm package metadata
├── pyproject.toml                   # Python/uv package metadata (PEP 621)
├── VERSION                          # Single source of truth for versioning
├── .gitignore                       # Git exclusion rules
├── install.sh                       # Safe-by-default POSIX installer helper
├── install.ps1                      # Windows PowerShell installer helper
│
├── docs/                            # Human-readable architectural and governance docs
│   ├── README.md                    # Documentation index and lifecycle guide
│   ├── adr/                         # Architecture Decision Records (e.g. ADR 0001)
│   ├── foundation/                  # Charter, scope, non-goals, and principles
│   ├── governance/                  # Maintainer responsibility and review rules
│   ├── roadmap/                     # Active milestones and long-term direction
│   ├── sops/                        # Contribution and feature delivery SOP
│   └── specifications/              # Registry asset model and schema specifications
│
├── .agents/                         # Contributor instructions and reference workflows
│   ├── AGENTS.md                    # Operating guidelines for AI agents working on this repo
│   └── workflows/                   # Reference task workflow definitions
│
├── registry/                        # Published skill registry and asset catalog
│   ├── registry.json                # Generated machine index of published skills
│   ├── registry.schema.json         # JSON Schema validating registry.json
│   ├── skills/                      # Scoped skill runbooks (engineering, web-and-geo, etc.)
│   ├── subagents/                   # Focused persona configurations
│   ├── rules/                       # Coding and security rules
│   ├── prompts/                     # Reusable system and task prompts
│   ├── snippets/                    # Reusable code snippets
│   ├── hooks/                       # Pre-tool and post-tool guard hooks
│   └── mcp-configs/                 # Model Context Protocol server configuration templates
│
├── scripts/                         # Maintenance, validation, and build tooling
│   ├── build_registry.py            # Generates registry.json and llms.txt
│   ├── validate_registry.py         # Validates registry.json against schema and skills
│   ├── bump.py                      # Multi-file version synchronizer
│   ├── sanitize.py                  # Local regex-based secret/PII scanner
│   └── run_workflow.py              # Safe simulation-first reference workflow runner
│
└── tests/                           # Repository integrity and validation test suite
    ├── test_repo_integrity.py       # Validates file presence, registry parity, and claims
    ├── test_registry_validation.py  # Tests schema validation script behaviors
    └── test_workflow_runner.py      # Tests reference workflow runner execution
```

---

## 5. Verification Pipeline

The repository enforces hygiene and integrity via reproducible local commands:

```bash
python3 scripts/sanitize.py
python3 scripts/build_registry.py
python3 scripts/validate_registry.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

---

## 6. Project Roadmap

Active and upcoming milestones are maintained in [`docs/roadmap/roadmap.md`](docs/roadmap/roadmap.md):
- **Milestone 1:** Repository operating foundation (charter, scope, governance, SOP).
- **Milestone 2:** Registry contract, three-tier discovery usability, and documentation alignment.
- **Milestone 3:** Reliable tooling, community health, and release automation.
- **Milestone 4:** Curated catalog quality and schema enforcement.
