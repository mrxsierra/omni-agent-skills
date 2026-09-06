---
name: ai-eval-benchmarker
description: Evaluates AI agent responses, tool invocation schemas, prompt regression suites, and model outputs against reproducible test cases.
---

# 🔬 AI Eval Benchmarker

The **AI Eval Benchmarker** executes evaluation harnesses, assesses agent tool invocation correctness, tests for prompt regressions, and validates structured outputs against reproducible test cases.

## 1. Inputs & Context Required
- **Evaluation Dataset:** Test cases containing inputs, expected tool calls or outputs, and evaluation criteria.
- **Target Component:** Agent prompt template, system instruction, or tool invocation handler.
- **Evaluation Metrics:** Verification criteria (e.g. schema validity, deterministic assertion checks, rubric scoring).

## 2. Step-by-Step Procedure
1. **Test Case Preparation:** Load test cases and ensure input formats match the expected evaluation harness schema.
2. **Harness Execution:** Run the target agent, model, or function against the evaluation dataset in an isolated, reproducible environment.
3. **Output & Schema Validation:** Verify returned tool arguments against formal schemas and evaluate outputs against baseline assertions.
4. **Regression Comparison:** Compare execution results against recorded baseline runs to detect behavioral or quality regressions.
5. **Report Compilation:** Generate an evaluation summary detailing pass/fail counts, failure logs, and execution diagnostics.

## 3. Expected Outputs & Artifacts
- **Evaluation Report:** Structured summary showing test outcomes, failure modes, and schema errors.
- **Execution Log / Metrics:** Machine-readable test execution logs (JSON or GFM table).

## 4. Constraints & Tool Neutrality
- **Truthful Evaluation:** Document actual test results against explicit test cases without making unsubstantiated claims.
- **Environment Isolation:** Evaluation harnesses must execute in safe sandboxes without running destructive commands.
- **Tool Neutral:** Compatible with standard testing frameworks (`unittest`, `pytest`, `vitest`) and AI evaluation runners.
