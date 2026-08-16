---
name: advanced-verification-testing
description: Design, implement, and run enterprise-grade multi-tier verification test suites across Python, Rust, TypeScript, Go, and C++, including golden snapshot regression testing, property-based invariant testing (Hypothesis/QuickCheck/fast-check), parser fuzzing, conformance matrices, and AI-agent evaluation benchmarks. Trigger when implementing complex verification testing, building compiler or parser test benches, verifying AST invariants, or testing AI agent code generation reliability.
---

# 🔬 Advanced Verification & Visual Testing Harness

This skill governs enterprise-grade verification testing, golden snapshot regression, visual UI regression, and property-based invariant testing.

## 1. Multi-Tier Verification Hierarchy
- **Tier 1: Unit & Integration Testing (`pytest`, `jest`):** Standard assertion test suites.
- **Tier 2: Golden Snapshot Regression:** Save exact baseline outputs (JSON, SVG, render trees) and verify zero drift across releases.
- **Tier 3: Property-Based Invariant Testing (`Hypothesis`, `fast-check`):** Generate hundreds of synthetic inputs to prove system invariants hold.
- **Tier 4: Visual UI Regression Testing:** Automated screenshot pixel diffing across standard viewport breakpoints.
