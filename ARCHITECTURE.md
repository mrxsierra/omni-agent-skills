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

## 3. Core Architectural Principles & Asset Taxonomy

Per [ADR 0002](docs/adr/0002-unified-documentation-layering-and-autonomous-agent-sdlc.md) and [ADR 0003](docs/adr/0003-registry-asset-taxonomy-shipped-capabilities-and-inclusion-criteria.md), the repository establishes a disciplined engineering foundation based on **eight concrete published asset types** structured across **two functional tiers**, navigating along a **3-Dimensional Coordinate System**:

### Published Asset Types (1-to-1 Directory Alignment)

```text
omni-agent-skills Published Asset Hierarchy
├── Tier 1: Core Orchestration & Reasoning Primitives (Agent Planning & Logic)
│   ├── skills/          (registry/skills/<domain>/<id>/SKILL.md)  ──► Atomic Runbooks
│   ├── workflows/       (registry/workflows/<id>/WORKFLOW.md)     ──► Multi-Step SDLC Pipelines
│   ├── rules/           (registry/rules/<category>/<id>.md)       ──► Invariant Behavioral Constraints
│   └── subagents/       (registry/subagents/<id>.json)            ──► Persona & Tool Isolation Manifests
│
└── Tier 2: Deterministic Integration & Context Primitives (Execution Substrate)
    ├── hooks/           (registry/hooks/<pre|post>-tool/<id>.sh)   ──► Lifecycle Guard Shell Scripts
    ├── mcp-configs/     (registry/mcp-configs/<id>.json)          ──► Tool Server Wire Configurations
    ├── snippets/        (registry/snippets/<lang>/<id>)           ──► Battle-Tested Reference Code & Tokens
    └── prompts/         (registry/prompts/<category>/<id>.md)     ──► System Prompt & Persona Templates
```

#### Tier 1: Core Orchestration & Reasoning Primitives
1. **Skills (`registry/skills/<domain>/<id>/`):** Atomic, domain-specific engineering runbooks implementing the canonical 4-section contract (Inputs, Procedure, Expected Outputs, Constraints).
2. **Workflows (`registry/workflows/<id>/`):** Composite, multi-step lifecycle orchestrations chaining skills, tools, and verification gates across SDLC phases.
3. **Rules (`registry/rules/<category>/<id>.md`):** Persistent behavioral invariants and safety constraints (e.g. `security_shield.md` enforcing branch isolation, zero secrets, and non-destructive operations).
4. **Subagents (`registry/subagents/<id>.json`):** Declarative persona manifests defining isolated execution boundaries, system instructions, and tool whitelists for workflow execution.

#### Tier 2: Deterministic Integration & Context Primitives
5. **Hooks (`registry/hooks/<pre|post>-tool/`):** Deterministic shell scripts executed before or after tool calls (`secret-leak-guard.sh`, `auto-formatter.sh`) that mechanically enforce rules.
6. **MCP Configs (`registry/mcp-configs/`):** Open Model Context Protocol connection templates for external tool integration (e.g. Chrome DevTools).
7. **Snippets (`registry/snippets/<lang>/`):** Anti-hallucination code implementations, boilerplate, and design tokens (e.g. `async_http_client.py`, `hsl_theme_tokens.ts`).
8. **Prompts (`registry/prompts/<category>/`):** Reusable system persona and task prompt templates.

*(Note: Repository-level verification, schema compilers, and lifecycle tooling reside separately in root `scripts/`).*

### The 3-Dimensional Coordinate System for Agent Discovery

To empower AI agents to choose the right assets and understand how various assets work simultaneously, the catalog is structured along three coordinates:

```text
               DIMENSION 1: SDLC Phase (WHEN?)
      Inception ──► Scaffolding ──► Implementation ──► Shipping
           │
           │           DIMENSION 2: Domain & Stack (WHERE?)
           ├──► Universal Foundation (Any repository regardless of stack)
           ├──► Web & Frontend (Next.js, TypeScript, CSS, DOM)
           ├──► Backend & Systems (Python, Go, Node, REST APIs, SQL)
           └──► Data & AI (RAG, Evals, Benchmarks, Pipelines)
           │
           │           DIMENSION 3: Relational Composition (WITH WHAT?)
           └──► Cohesive Stack: Workflow + Subagent + Skill + Rule + Hook + Snippet + MCP
```

- **Dimension 1: Temporal Phase (When?):** Maps to the 7-Phase SDLC (`Phase 1: Inception` to `Phase 7: Shipping & Operations`).
- **Dimension 2: Domain & Stack (Where?):** Distinguishes **Universal Foundation** assets (applying to every repo) from **Domain-Specific Stacks** (Web, Backend, Data/AI).
- **Dimension 3: Relational Composition (With What?):** Combines complementary assets into curated **Archetype Stacks**:

| Archetype Stack | Target Task / Workspace | Workflow & Subagent | Skills Invoked | Rules & Prompts | Hooks & Snippets | MCP Tooling |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Universal OSS Baseline** | Any repo scaffolding, PR, or release | `workflow-repo-scaffolding`, `secret-leak-shield.json` | `oss-launch-governance`, `semver-release-manager` | `security_shield.md` | `secret-leak-guard.sh`, `auto-formatter.sh` | — |
| **Modern Web & Frontend** | Next.js / React UI feature delivery | `workflow-feature-delivery`, `system-architecture-planner.json` | `atomic-feature-implementer`, `ai-first-web-geo`, `a11y-web-auditor` | `nextjs_rules.md`, `architect-persona.md` | `auto-formatter.sh`, `hsl_theme_tokens.ts` | `chrome-devtools.json` |
| **Python Backend / CLI** | Python service, testing, and clean code | `workflow-feature-delivery`, `code-anti-overengineer.json` | `atomic-feature-implementer`, `clean-code-auditor`, `pytest-verification-runner` | `python_rules.md` | `auto-formatter.sh`, `async_http_client.py` | — |
| **Data & AI Systems** | RAG pipelines, model eval, dataset chunks | `workflow-feature-delivery`, `system-architecture-planner.json` | `rag-qa-chunking-engine`, `ai-eval-benchmarker` | `security_shield.md` | `async_http_client.py` | — |

### Core Operating Principles
1. **Single-Responsibility Principle (SRP):** Each skill, rule, and asset is strictly scoped to a single expert capability to prevent context bleed and maintain high precision.
2. **Verification Over Claiming:** This repository does not publish benchmark performance claims unless backed by reproducible CI runs with explicit golden data and reviewable artifacts.
3. **Safe-by-Default Execution:** Reference runners and installation helpers are simulation-first and non-destructive. Shell execution requires explicit maintainer configuration.
4. **Tool Neutrality:** Published assets declare clear constraints, inputs, and expected outputs without assuming vendor-specific runtime privileges.
5. **Secret Hygiene:** Scans for obvious secret and credential patterns using `scripts/sanitize.py` and protects private local overrides via `.gitignore`.
6. **5-Gate Inclusion Filter:** Every addition must satisfy Orthogonality, Tool Neutrality, Deterministic Verification Invariants, Contract Conformance, and Zero-Secret/Zero-Hype criteria.

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
│   ├── adr/                         # Architecture Decision Records (ADRs 0001-0003)
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
│   ├── skills/                      # Tier-1: Scoped skill runbooks (engineering, web-and-geo, etc.)
│   ├── workflows/                   # Tier-1: Shipped lifecycle workflows with stage gates
│   ├── rules/                       # Tier-1: Behavioral and security rules
│   ├── subagents/                   # Tier-1: Focused persona and tool isolation configurations
│   ├── hooks/                       # Tier-2: Pre-tool and post-tool guard hooks
│   ├── mcp-configs/                 # Tier-2: Model Context Protocol server configuration templates
│   ├── snippets/                    # Tier-2: Reusable reference code snippets and UI tokens
│   └── prompts/                     # Tier-2: Reusable system and task prompt templates
│
├── scripts/                         # Maintenance, validation, and build tooling
│   ├── build_registry.py            # Generates registry.json and llms.txt
│   ├── validate_registry.py         # Validates registry.json against schema and skills
│   ├── manage_adr.py                # ADR and RFC lifecycle tooling
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
python3 scripts/manage_adr.py validate
python3 -m unittest discover -s tests -p 'test_*.py'
```

---

## 6. Project Roadmap

Active and upcoming milestones are maintained in [`docs/roadmap/roadmap.md`](docs/roadmap/roadmap.md):
- **Milestone 1:** Repository operating foundation (charter, scope, governance, SOP).
- **Milestone 2:** Registry contract, three-tier discovery usability, and documentation alignment.
- **Milestone 3:** Reliable tooling, community health, and release automation.
- **Milestone 4:** Curated catalog quality and schema enforcement.
- **Milestone 5:** Shipped workflows & lifecycle orchestration.
- **Milestone 6:** Greenfield scaffolding & deployment skills.
- **Milestone 7:** Distribution, installation UX & consumer verification.
- **Milestone 8:** Production release v0.1.0.
