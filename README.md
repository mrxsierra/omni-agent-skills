# omni-agent-skills

A tool-neutral, open-source skill registry and asset catalog for AI-assisted engineering: structured skill runbooks, machine-readable discovery indexes, guardrail scripts, and a minimal validation harness.

This repository publishes portable assets to help developers and AI coding agents (such as Google Antigravity, Claude Code, Cursor, Codex, and OpenCode) execute scoped workflows without overloading prompt context windows.

---

## Three-Tier Agent Discovery

To support diverse agent workflows, search engines, and RAG systems, the repository provides three distinct discovery layers:

1. **Tier 1 — Executable Asset Registry ([`registry/registry.json`](registry/registry.json)):**
   Machine-readable catalog generated from [`registry/skills/`](registry/skills/) and validated against [`registry/registry.schema.json`](registry/registry.schema.json). Used by agents to query and load skill runbooks on demand.
2. **Tier 2 — LLM Context Sitemap ([`llms.txt`](llms.txt)):**
   Compact markdown summary following the `/llmstxt.org` standard, designed for prompt injection and LLM crawler indexing.
3. **Tier 3 — Semantic Q&A Retrieval ([`llms-qa.json`](llms-qa.json)):**
   Pre-chunked, tagged Q&A dataset designed for vector embeddings and RAG search over this repository, dogfooding the [`rag-qa-chunking-engine`](registry/skills/data-and-ai/rag-qa-chunking-engine/SKILL.md) skill.

---

## Truthful Status

This repository does not publish benchmark performance claims unless those claims are backed by a reproducible CI run with explicit golden data, raw outputs, and reviewable artifacts.

At present, the repository provides:
- a verified schema-backed skill registry and build generator,
- three-tier AI discovery endpoints (`registry.json`, `llms.txt`, `llms-qa.json`),
- local sanitization and secret-pattern hygiene checks,
- safe-by-default installation scripts and reference workflow runners, and
- automated integrity smoke tests.

See [docs/README.md](docs/README.md) for the project charter, scope boundary ([ADR 0001](docs/adr/0001-registry-not-control-plane.md)), governance, roadmap, and contribution procedures.

---

## Quick Start

### 1. Explore Skills

Clone the repository and inspect the published skills:

```bash
git clone https://github.com/mrxsierra/omni-agent-skills.git
cd omni-agent-skills
ls registry/skills
```

Rebuild the machine index and LLM summary at any time:

```bash
python3 scripts/build_registry.py
```

### 2. Installation

For safe, reproducible installation into your local agent environment, review [`INSTALL.md`](INSTALL.md). The project recommends installing from pinned release tags rather than unpinned remote scripts:

```bash
# Clone a pinned release tag
git clone --depth 1 --branch v0.0.1 https://github.com/mrxsierra/omni-agent-skills.git
```

See [`INSTALL.md`](INSTALL.md) for checksum verification and installer script options (`install.sh` and `install.ps1`).

---

## Validation Commands

Before committing or submitting pull requests, run the repository hygiene checks:

```bash
python3 scripts/sanitize.py
python3 scripts/build_registry.py
python3 scripts/validate_registry.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

---

## Published Skill Domains

The registry organizes capabilities into focused, single-responsibility skill runbooks under [`registry/skills/`](registry/skills/):

- **Engineering:** Architecture planning, atomic implementation, clean code auditing, anti-overengineering, Pytest runner, and SemVer release management.
- **Web & GEO:** Generative Engine Optimization (GEO) and accessibility (`a11y`) auditing.
- **Data & AI:** RAG Q&A chunking engine and evaluation benchmarking.
- **Security & Governance:** Secret leak prevention, open-source launch governance, competitive intelligence, advanced verification testing, and AI-native product design.

For full descriptions and paths, inspect [`registry/registry.json`](registry/registry.json) or [`llms.txt`](llms.txt).

---

## Contributing

We welcome community contributions. Please review:
- [Contribution & Feature Delivery SOP](docs/sops/contribution-and-feature-delivery.md) for the end-to-end contribution workflow.
- [CONTRIBUTING.md](CONTRIBUTING.md) for quick local development instructions.
- [SECURITY.md](SECURITY.md) for our security and secret hygiene policy.

---

## License

Distributed under the [MIT License](LICENSE).
