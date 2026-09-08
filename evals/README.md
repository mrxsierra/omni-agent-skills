# 📊 Empirical Evaluation & Quality Scorecard

This directory contains the empirical evaluation baselines, benchmark task suites,
and reproducible results for the assets published in the `omni-agent-skills` registry.

> [!IMPORTANT]
> **Zero-Hype Empirical Gate (ADR 0004 & ADR 0005):**
> Every skill, rule, or workflow admitted to this registry must prove positive $\Delta$-utility
> or high baseline parity with minimal token tax. Prompt bloat, unverified claims, and
> performance-degrading instructions are rejected automatically.

## Summary Metrics

- **Total Catalog Assets Benchmarked:** 16
- **Benchmark Pass Rate:** 100.0% (16/16 evaluations passed)
- **Average Context Token Tax:** +548 tokens / turn
- **Evaluated Provider Engines:** mock

---

## Multi-Tier Evaluation Architecture (ADR 0005)

Evaluation is decoupled into three operational tiers:

| Tier | Engine | Target Environment | Cost & Speed | Primary Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Harness Gate** | `mock` (`MockProvider`) | Local & CI (`ci.yml`) | 0 cost, < 2s | Validates task format, schema wiring, and scoring algorithms deterministically. |
| **Tier 2: Neural Smoke** | `ollama` (`qwen2.5-coder:1.5b`) | CI & Local Podman | 0 cost, ~2m | Smoke tests real open-weights neural token generation on CPU. |
| **Tier 3: Cloud Heavy Lifting** | `agy` (Gemini 3.8 / Claude) | Local & Scheduled CI | Minimal API cost, ~5s | High-capacity reasoning benchmarks for complex multi-step refactoring skills. |

---

## Asset Benchmark Scorecard

| Asset / Skill | Domain | Suite ID | Provider (Model) | Base % | Aug % | $\Delta$-Utility | Token Tax | Gate Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ai-eval-benchmarker` | data-and-ai | `ai_eval_benchmarker` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +539 tok | ✅ PASS |
| `rag-qa-chunking-engine` | data-and-ai | `rag_qa_chunking_engine` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +624 tok | ✅ PASS |
| `atomic-feature-implementer` | engineering | `atomic_feature_implementer` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +528 tok | ✅ PASS |
| `clean-code-auditor` | engineering | `clean_code_audit` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +522 tok | ✅ PASS |
| `code-anti-overengineer` | engineering | `code_anti_overengineer` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +537 tok | ✅ PASS |
| `pytest-verification-runner` | engineering | `pytest_verification_runner` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +542 tok | ✅ PASS |
| `semver-release-manager` | engineering | `semver_release_manager` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +553 tok | ✅ PASS |
| `system-architecture-planner` | engineering | `system_architecture_planner` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +565 tok | ✅ PASS |
| `advanced-verification-testing` | security-and-governance | `advanced_verification_testing` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +575 tok | ✅ PASS |
| `ai-native-product-design` | security-and-governance | `ai_native_product_design` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +541 tok | ✅ PASS |
| `oss-launch-governance` | security-and-governance | `oss_launch_governance` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +538 tok | ✅ PASS |
| `secret-leak-shield` | security-and-governance | `secret_leak_shield` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +567 tok | ✅ PASS |
| `security_shield.md` | security-and-governance | `security_shield` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +406 tok | ✅ PASS |
| `tech-competitive-intelligence` | security-and-governance | `tech_competitive_intelligence` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +566 tok | ✅ PASS |
| `a11y-web-auditor` | web-and-geo | `a11y_audit` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +574 tok | ✅ PASS |
| `ai-first-web-geo` | web-and-geo | `ai_first_web_geo` | `mock` (`mock-deterministic-v1`) | 0.0% | 100.0% | **+100.0%** | +590 tok | ✅ PASS |

---

## Reproducing & Running Evaluations

Use the unified local evaluation helper script:

```bash
# 1. Instant deterministic mock run (< 2s, offline)
scripts/run_local_eval.sh mock registry/skills/engineering/clean-code-auditor/SKILL.md

# 2. Cloud evaluation via Antigravity CLI (zero download)
scripts/run_local_eval.sh agy registry/skills/engineering/clean-code-auditor/SKILL.md gemini-3.8-flash-high

# 3. Rootless containerized open-weights evaluation (Podman/Docker)
scripts/run_local_eval.sh podman start qwen2.5-coder:1.5b
scripts/run_local_eval.sh podman eval registry/skills/engineering/clean-code-auditor/SKILL.md
scripts/run_local_eval.sh podman stop
```

To rebuild this report after updating baselines:
```bash
python3 scripts/build_eval_report.py
```
