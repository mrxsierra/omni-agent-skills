---
name: advanced-verification-testing
description: Designs, implements, and executes multi-tier verification suites including unit, integration, golden snapshot regression, and property-based invariant testing.
---

# 🔬 Advanced Verification & Visual Testing Harness

The **Advanced Verification Testing** skill structures and executes multi-tiered testing suites, combining unit tests, deterministic snapshot regressions, and property-based invariant testing.

## 1. Inputs & Context Required
- **Target Subsystem:** Source code modules, serialization schemas, parser components, or API boundaries.
- **System Invariants:** Expected business logic invariants, data contracts, and boundary conditions.
- **Test Toolchain:** Testing framework and property generators (e.g. `pytest` + `Hypothesis`, `jest` / `vitest` + `fast-check`, `cargo test` + `proptest`).

## 2. Step-by-Step Procedure
1. **Tier 1 — Unit & Integration Testing:** Implement deterministic unit tests asserting functional correctness across standard inputs, edge cases, and error branches.
2. **Tier 2 — Golden Snapshot Regression:** Record canonical golden output baselines (JSON payloads, serialized schemas, ASTs) and assert exact matches across builds to catch unintended drift.
3. **Tier 3 — Property-Based Invariant Testing:** Formulate invariant properties using randomized input generators to verify system stability across broad input spaces.
4. **Tier 4 — Boundary & Conformance Testing:** Feed malformed, boundary, or high-volume payloads into parsers and decoders to verify graceful error handling.
5. **Execution & Reporting:** Run the full verification suite and generate structured execution logs.

## 3. Expected Outputs & Artifacts
- **Tiered Test Suite:** Well-organized test files mapping directly to system tiers.
- **Golden Baseline Fixtures:** Deterministic fixtures stored under version control.
- **Verification Summary:** Structured test execution results and coverage reports.

## 4. Constraints & Tool Neutrality
- **Deterministic Runs:** Golden snapshot and property tests must be reproducible (using explicit random seeds where appropriate).
- **Tool Neutral:** Principles apply across Python, TypeScript, Rust, Go, and C++.
