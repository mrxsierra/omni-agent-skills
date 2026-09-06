---
name: secret-leak-shield
description: Audits workspace edits and staged files for exposed API keys, private tokens, passwords, and sensitive environment variables to prevent accidental credential commits.
---

# 🛡️ Secret Leak Shield

The **Secret Leak Shield** audits workspace modifications to prevent credential leaks, private key exposures, and accidental check-ins of sensitive environment files.

## 1. Inputs & Context Required
- **Target Files & Diffs:** Staged changes, working tree diffs, or newly generated source code files.
- **Pattern Definitions:** Known secret patterns (e.g. OpenAI `sk-`, GitHub `ghp_`/`gho_`, Google API keys `AIza`, AWS access keys, private RSA/SSH keys).
- **Exclusion Rules:** Workspace ignore rules (`.gitignore`, `.sanitize-local.json`) for local developer test configs.

## 2. Step-by-Step Procedure
1. **Diff & File Inspection:** Scan all added, modified, or staged files before git staging.
2. **Regex Pattern Matching:** Check file contents against high-risk credential signatures and regex rules (as implemented in `scripts/sanitize.py` and `registry/hooks/pre-tool/secret-leak-guard.sh`).
3. **Environment Isolation:** Verify that `.env`, `.env.local`, and private credential files are explicitly listed in `.gitignore` and not tracked in git history.
4. **Remediation & Block:** If a secret pattern is detected, immediately halt execution, report the file and line number, and require substitution with a generic placeholder (e.g., `YOUR_API_KEY`, `your-org`).

## 3. Expected Outputs & Artifacts
- **Sanitization Report:** Confirmation that all inspected files passed pattern checks with zero detected credentials.
- **Remediation Summary:** Actionable instruction identifying flagged lines and placeholder replacements when a potential leak is found.

## 4. Constraints & Tool Neutrality
- **Hygiene Guardrail:** This skill provides regular-expression-based heuristic scanning; it does not replace third-party secret scanners (such as TruffleHog or GitGuardian) or provide a mathematical zero-leak guarantee in all possible environments.
- **Tool Neutral:** Compatible with POSIX shell hooks, Python sanitizers, or AI agent tool runtimes.
