# 🚀 omni-agent-skills

[![Version](https://img.shields.io/badge/Version-v0.0.1-blue.svg)](package.json)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security Shield](https://img.shields.io/badge/Security-AgentShield-success.svg)](SECURITY.md)
[![RAG Accuracy](https://img.shields.io/badge/RAG%20Accuracy-%3E95%25-orange.svg)](qa_pairs_generic_tagged.json)

**Universal AI Agent Skill Registry, Security Harness, & Workflow Engine** designed for **Google Antigravity (AGY), Claude Code, Cursor, Codex, OpenCode, and Human Developers**.

> **"Optimize the context window. Persist everything else."**

---

## ⚡ Quick Start & Installation

### 1. 1-Click Terminal Installer (Humans & CI/CD)
```bash
curl -sSL https://raw.githubusercontent.com/mrxsierra/omni-agent-skills/main/install.sh | bash
```

### 2. Node.js / npx Installer
```bash
npx omni-agent-skills install
```

### 3. Python / uv Installer
```bash
uv pip install omni-agent-skills
```

### 4. Claude Code Plugin Marketplace
```bash
/plugin marketplace add mrxsierra/omni-agent-skills
```

---

## 🤖 How AI Agents Consume This Repository

AI agents do not need to load all skills into context. They query **`registry.json`** or **`llms.txt`** on demand:

* **Machine Sitemap:** [`llms.txt`](llms.txt)
* **Machine Registry:** [`registry.json`](registry.json)
* **Tagged Vector Dataset (>95% Match Accuracy):** [`qa_pairs_generic_tagged.json`](qa_pairs_generic_tagged.json)

---

## 🛠️ Included 15-Skill Master Matrix

| Domain | Skill Name | Description |
| :--- | :--- | :--- |
| **Engineering** | [`system-architecture-planner`](skills/engineering/system-architecture-planner/SKILL.md) | PRD generation, 4-tier system design, and 15-min task breakdowns. |
| **Engineering** | [`atomic-feature-implementer`](skills/engineering/atomic-feature-implementer/SKILL.md) | Atomic feature code implementation & callsite propagation. |
| **Engineering** | [`pytest-verification-runner`](skills/engineering/pytest-verification-runner/SKILL.md) | Unit test suites (`pytest`) & verification harnesses. |
| **Engineering** | [`clean-code-auditor`](skills/engineering/clean-code-auditor/SKILL.md) | Git diff audits & clean code refactoring. |
| **Engineering** | [`code-anti-overengineer`](skills/engineering/code-anti-overengineer/SKILL.md) | Code simplification, dead code elimination, & anti-over-engineering. |
| **Engineering** | [`semver-release-manager`](skills/engineering/semver-release-manager/SKILL.md) | README polish, changelogs, & GitHub release tags (`gh`). |
| **Web & GEO** | [`ai-first-web-geo`](skills/web-and-geo/ai-first-web-geo/SKILL.md) | Generative Engine Optimization (GEO), JSON-LD schema, & RAG endpoints. |
| **Web & GEO** | [`a11y-web-auditor`](skills/web-and-geo/a11y-web-auditor/SKILL.md) | Web accessibility (a11y WCAG 2.1), Core Web Vitals, & UI QA. |
| **Data & AI** | [`rag-qa-chunking-engine`](skills/data-and-ai/rag-qa-chunking-engine/SKILL.md) | Tagged Q&A-pair dataset generator (`qa_pairs.json`) for RAG. |
| **Data & AI** | [`ai-eval-benchmarker`](skills/data-and-ai/ai-eval-benchmarker/SKILL.md) | AI agent accuracy benchmarks, prompt regression, & ML evaluation. |
| **Security & Gov** | [`secret-leak-shield`](skills/security-and-governance/secret-leak-shield/SKILL.md) | Secret scanning, vulnerability checks, & staging safety (`drafts/`). |
| **Security & Gov** | [`oss-launch-governance`](skills/security-and-governance/oss-launch-governance/SKILL.md) | Pre-launch Phase-0 clearance & open-source launch governance. |
| **Security & Gov** | [`tech-competitive-intelligence`](skills/security-and-governance/tech-competitive-intelligence/SKILL.md) | Technical moat scoring & "Why Not X?" comparison matrices. |
| **Security & Gov** | [`advanced-verification-testing`](skills/security-and-governance/advanced-verification-testing/SKILL.md) | Multi-tier testing, golden snapshot regression, & invariant testing. |
| **Security & Gov** | [`ai-native-product-design`](skills/security-and-governance/ai-native-product-design/SKILL.md) | AI-consumable architecture (`llms.txt`, MCP tools, OpenAPI specs). |

---

## 🛡️ Privacy & Security Shield

This repository strictly enforces **Zero-PII Anonymization** and **Zero Secret Leakage**. All skills, rules, and templates use generic placeholders (`your-org`, `YOUR_API_KEY`). See [`SECURITY.md`](SECURITY.md) for details.

---

## 📜 License

Distributed under the [MIT License](LICENSE).
