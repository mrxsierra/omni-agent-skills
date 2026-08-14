---
trigger: always_on
---

# 🩹 Self-Healing Diagnostic & Build-Error Resolver Protocol

This protocol governs automated debugging and build repair behavior across all terminal execution failures (`pytest`, `npm run build`, `tsc`, `cargo check`).

## 1. Zero-Abandonment Error Extraction
- When a terminal command fails with a non-zero exit code or stack trace, **NEVER** abandon log extraction or guess the cause.
- Read the full un-truncated error log and extract:
  1. The failing file path and line number.
  2. The exact exception class / error message (`ModuleNotFoundError`, `TypeError`, `SyntaxError`, `ImportError`).
  3. The target symbol name that broke the build contract.

## 2. Autonomous Empirical Fix Loop
```
1. Capture Execution Failure
2. Read Full Log & Trace Failure Root Cause
3. Inspect Target Symbol Definition
4. Apply Minimal, Atomic Code Fix
5. Re-run Verification Command
```
- Attempt up to **3 automated repair iterations** before surfacing unresolved state to the user.
