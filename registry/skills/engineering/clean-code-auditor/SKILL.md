---
name: clean-code-auditor
description: Audits git diffs and code modifications for code smells, DRY violations, adherence to repository conventions, and architectural consistency.
---

# 🔍 Clean Code Auditor

The **Clean Code Auditor** inspects proposed codebase changes, detects anti-patterns, audits adherence to DRY principles, and provides actionable code review feedback.

## 1. Inputs & Context Required
- **Git Diff:** Staged diff (`git diff --cached`) or branch diff (`git diff origin/main...HEAD`).
- **Style Rules & Guidelines:** Workspace coding rules (e.g. `registry/rules/frameworks/`, linter configs, or docstring standards).
- **Target Context:** Relevant neighboring modules to verify naming and architectural consistency.

## 2. Step-by-Step Procedure
1. **Diff Scope Review:** Inspect the diff to confirm that all changes are strictly relevant to the task's stated intent.
2. **Detect Anti-Patterns:** Check for code duplication (DRY violations), magic numbers, overly long functions (>50 lines), unhandled edge cases, and swallowed errors.
3. **Naming & Convention Check:** Verify that variable, function, and file names follow established project conventions and clearly express intent.
4. **Dependency & Import Audit:** Confirm no unnecessary dependencies, dead imports, or circular references are introduced.
5. **Formulate Review Feedback:** Present findings as concise, constructive suggestions with file path and line number references.

## 3. Expected Outputs & Artifacts
- **Code Review Report:** Structured review summarizing strengths, critical findings, and actionable improvement recommendations.
- **Pass/Revision Verdict:** Clear determination of whether the diff meets workspace quality standards.

## 4. Constraints & Tool Neutrality
- **Read-Only / Non-Mutating:** The auditor reviews and recommends; it does not unilaterally rewrite source code without authorization.
- **Tool Neutral:** Works alongside git CLI, GitHub PR review comments, or standalone agent audit tools.
