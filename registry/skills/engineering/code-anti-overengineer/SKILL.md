---
name: code-anti-overengineer
description: Simplifies over-engineered code, removes dead abstractions and redundant dependencies, flattens nested conditionals into early returns, and preserves exact behavioral contracts.
---

# 🧹 Code Anti-Overengineer

The **Code Anti-Overengineer** audits and refactors implementation code to strip unnecessary abstractions, simplify control flows, and enforce minimal, readable code while preserving exact system behavior.

## 1. Inputs & Context Required
- **Target Implementation:** Source code files with complex hierarchies, deep conditional nesting, or unneeded design patterns.
- **Existing Test Suite:** Passing unit and integration tests that define the contract and baseline behavior.
- **Architectural Scope:** Minimum requirements of the feature (avoiding speculative future-proofing).

## 2. Step-by-Step Procedure
1. **Establish Baseline:** Run the existing test suite to ensure all tests pass before making any edits.
2. **Flatten Control Flow:** Replace deeply nested `if/else` blocks with guard clauses and early returns.
3. **Strip Speculative Abstractions:** Replace single-implementation interfaces, redundant factory wrappers, and premature generic abstractions with direct, clear code.
4. **Eliminate Dead Code:** Remove unused variables, dead helper functions, unneeded imports, and obsolete comments.
5. **Verify Contract Invariance:** Re-run the full verification test suite to prove that all external behaviors, signatures, and outcomes remain identical.

## 3. Expected Outputs & Artifacts
- **Refactored Code:** Clean, readable source files with reduced cyclomatic complexity and fewer lines of code.
- **Diff Summary:** Concise explanation detailing removed abstractions and confirming zero changes to public contracts.

## 4. Constraints & Tool Neutrality
- **Behavior Preservation:** Never alter functional logic, public API contracts, or existing test assertions during an anti-overengineering refactor.
- **Language Agnostic:** Principles apply equally across Python, TypeScript, Go, Rust, and C++.
