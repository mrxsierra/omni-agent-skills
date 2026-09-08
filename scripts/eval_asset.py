#!/usr/bin/env python3
"""
Asset Evaluation & Delta-Utility CLI Benchmark Runner for omni-agent-skills.

Measures whether a proposed registry asset (skill, rule, workflow) provides
positive delta utility over a baseline foundation model, or whether it is
simply prompt bloat/junk.

Supports pluggable providers:
  - Google Antigravity / Gemini
  - Local Ollama (open weights, zero cost)
  - OpenAI / ChatGPT
  - OpenRouter
  - Anthropic / Claude
  - Offline Mock (zero API keys, CI safe)

Usage:
  python3 scripts/eval_asset.py --asset registry/skills/engineering/clean-code-auditor/SKILL.md --provider mock
  python3 scripts/eval_asset.py --asset registry/skills/web-and-geo/a11y-web-auditor/SKILL.md --provider ollama --model qwen2.5-coder:7b
  python3 scripts/eval_asset.py --asset registry/rules/global/security_shield.md --provider antigravity --model gemini-2.5-pro
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from eval_providers import BaseModelProvider, ModelResponse, get_provider

REPO_ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = REPO_ROOT / "evals" / "tasks"


def load_task_suite(task_suite_arg: Optional[str], asset_path: Path) -> Dict[str, Any]:
    """Find and load the appropriate evaluation task suite."""
    if task_suite_arg:
        p = Path(task_suite_arg)
        if not p.is_absolute():
            p = REPO_ROOT / p
        if p.is_file():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        suite_path = TASKS_DIR / f"{task_suite_arg}.json"
        if suite_path.is_file():
            with open(suite_path, "r", encoding="utf-8") as f:
                return json.load(f)
        raise FileNotFoundError(f"Task suite '{task_suite_arg}' not found.")

    # Auto-resolve task suite by scanning evals/tasks/ for matching target_asset or parent skill dir
    asset_rel = str(asset_path.relative_to(REPO_ROOT) if asset_path.is_relative_to(REPO_ROOT) else asset_path)
    if TASKS_DIR.is_dir():
        for f in TASKS_DIR.glob("*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    target = data.get("target_asset", "")
                    if target == asset_rel or (target and Path(target).parent.name == asset_path.parent.name):
                        return data
            except Exception:
                continue

    # Fallback to general clean_code_audit if none matched
    fallback = TASKS_DIR / "clean_code_audit.json"
    if fallback.is_file():
        with open(fallback, "r", encoding="utf-8") as fp:
            return json.load(fp)

    raise FileNotFoundError("No matching evaluation task suite found in evals/tasks/.")


def score_task(response_text: str, expected_keywords: List[str], fail_keywords: List[str]) -> Tuple[bool, str]:
    """Deterministically score a response against keyword invariants."""
    text_lower = response_text.lower()

    # Check for forbidden failure keywords
    for bad in fail_keywords:
        if bad.lower() in text_lower:
            return False, f"Failed on forbidden keyword: '{bad}'"

    # Check for expected success keywords (at least one match)
    matches = [good for good in expected_keywords if good.lower() in text_lower]
    if not matches and expected_keywords:
        return False, f"Missing required keywords from: {expected_keywords}"

    return True, f"Passed ({len(matches)} matching criteria)"


def evaluate_asset(
    asset_path: Path,
    provider: BaseModelProvider,
    task_suite: Dict[str, Any],
    verbose: bool = False,
) -> Dict[str, Any]:
    """Execute baseline vs. augmented evaluation and compute delta metrics."""
    with open(asset_path, "r", encoding="utf-8") as f:
        asset_content = f.read()

    tasks = task_suite.get("tasks", [])
    if not tasks:
        raise ValueError("Task suite contains no tasks.")

    baseline_system = "You are a software engineering assistant. Answer user queries accurately."
    augmented_system = (
        "You are an expert software engineer adhering strictly to the following instructions:\n\n"
        f"{asset_content}\n\n"
        "Apply these principles deterministically to the user request."
    )

    baseline_results = []
    augmented_results = []

    total_baseline_tokens = 0
    total_augmented_tokens = 0

    for task in tasks:
        prompt = task["user_prompt"]
        expected = task.get("expected_keywords", [])
        fail_kw = task.get("fail_keywords", [])

        # 1. Baseline Run (Without Asset)
        base_resp: ModelResponse = provider.invoke(
            messages=[{"role": "user", "content": prompt}],
            system_prompt=baseline_system,
        )
        base_passed, base_reason = score_task(base_resp.text, expected, fail_kw)
        total_baseline_tokens += base_resp.prompt_tokens
        baseline_results.append({
            "task_id": task["id"],
            "passed": base_passed,
            "reason": base_reason,
            "response": base_resp.text,
            "tokens": base_resp.prompt_tokens,
        })

        # 2. Augmented Run (With Asset Injected)
        aug_resp: ModelResponse = provider.invoke(
            messages=[{"role": "user", "content": prompt}],
            system_prompt=augmented_system,
        )
        aug_passed, aug_reason = score_task(aug_resp.text, expected, fail_kw)
        total_augmented_tokens += aug_resp.prompt_tokens
        augmented_results.append({
            "task_id": task["id"],
            "passed": aug_passed,
            "reason": aug_reason,
            "response": aug_resp.text,
            "tokens": aug_resp.prompt_tokens,
        })

        if verbose:
            print(f"[{task['id']}] Baseline: {'PASS' if base_passed else 'FAIL'} | Augmented: {'PASS' if aug_passed else 'FAIL'}")

    n_tasks = len(tasks)
    base_pass_count = sum(1 for r in baseline_results if r["passed"])
    aug_pass_count = sum(1 for r in augmented_results if r["passed"])

    base_rate = base_pass_count / n_tasks
    aug_rate = aug_pass_count / n_tasks
    delta = aug_rate - base_rate

    avg_base_tokens = total_baseline_tokens // n_tasks
    avg_aug_tokens = total_augmented_tokens // n_tasks
    token_tax = avg_aug_tokens - avg_base_tokens

    # Determine Verdict
    if delta > 0:
        verdict = "ACCEPTED (Positive Delta Utility)"
        passed_gate = True
    elif delta == 0 and aug_rate == 1.0 and token_tax < 500:
        # Both passed, reasonable token tax
        verdict = "ACCEPTED (High Baseline Parity, Low Token Tax)"
        passed_gate = True
    else:
        verdict = "REJECTED (Bloat/Junk: No measurable improvement over baseline)"
        passed_gate = False

    return {
        "asset_path": str(asset_path),
        "provider": provider.provider_name,
        "model": provider.model_name,
        "task_suite": task_suite.get("suite_id", "custom"),
        "total_tasks": n_tasks,
        "baseline_pass_rate": round(base_rate * 100, 1),
        "augmented_pass_rate": round(aug_rate * 100, 1),
        "delta_utility": round(delta * 100, 1),
        "token_tax_per_turn": token_tax,
        "passed_gate": passed_gate,
        "verdict": verdict,
        "harness_verification_only": provider.provider_name == "mock",
        "baseline_details": baseline_results,
        "augmented_details": augmented_results,
    }


def print_report(results: Dict[str, Any]) -> None:
    """Print an aligned, human-readable terminal report."""
    print("\n" + "=" * 70)
    print("📊 omni-agent-skills Asset Evaluation & Delta-Utility Benchmark")
    print("=" * 70)
    print(f"Target Asset:     {results['asset_path']}")
    print(f"Provider:         {results['provider']} ({results['model']})")
    print(f"Task Suite:       {results['task_suite']} ({results['total_tasks']} tasks)")
    print("-" * 70)
    print(f"Baseline Pass Rate:    {results['baseline_pass_rate']}%")
    print(f"Augmented Pass Rate:   {results['augmented_pass_rate']}%")
    delta_sign = "+" if results['delta_utility'] >= 0 else ""
    print(f"Delta Utility:         {delta_sign}{results['delta_utility']}%")
    print(f"Context Token Tax:     +{results['token_tax_per_turn']} tokens / turn")
    print("-" * 70)
    if results['provider'] == 'mock':
        print("Notice:           MOCK HARNESS RUN (Validates CLI & scoring plumbing only; not neural quality)")
    print(f"Final Verdict:         {results['verdict']}")
    print("=" * 70 + "\n")


def append_github_step_summary(results: Dict[str, Any]) -> None:
    """Append a Markdown evaluation scorecard to $GITHUB_STEP_SUMMARY if present."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    asset_path = Path(results["asset_path"])
    asset_name = asset_path.parent.name if asset_path.name == "SKILL.md" else asset_path.name
    delta_sign = "+" if results["delta_utility"] >= 0 else ""
    status_badge = "✅ PASSED" if results["passed_gate"] else "❌ REJECTED"
    tier = "Deterministic Mock" if results.get("harness_verification_only") else f"Neural ({results['provider']})"

    md_content = f"""
### 📊 Asset Evaluation Scorecard: `{asset_name}`

| Metric | Result |
| :--- | :--- |
| **Asset Path** | `{results['asset_path']}` |
| **Evaluation Tier** | {tier} |
| **Provider / Model** | `{results['provider']}` / `{results['model']}` |
| **Task Suite** | `{results['task_suite']}` ({results['total_tasks']} tasks) |
| **Baseline Pass Rate** | `{results['baseline_pass_rate']}%` |
| **Augmented Pass Rate** | `{results['augmented_pass_rate']}%` |
| **$\\Delta$-Utility (Delta)** | **`{delta_sign}{results['delta_utility']}%`** |
| **Context Token Tax** | `+{results['token_tax_per_turn']} tokens / turn` |
| **Gate Status** | **{status_badge}** |
| **Verdict** | {results['verdict']} |

> *Evaluated autonomously via omni-agent-skills dual-engine verification pipeline (ADR 0005).*
"""
    try:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(md_content.strip() + "\n\n")
    except Exception as e:
        print(f"Warning: Failed to write to GITHUB_STEP_SUMMARY: {e}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark registry assets across AI providers to verify positive delta utility."
    )
    parser.add_argument(
        "--asset",
        required=True,
        help="Path to the registry asset to evaluate (skill, rule, workflow).",
    )
    parser.add_argument(
        "--provider",
        default="mock",
        choices=["antigravity", "agy", "ollama", "openai", "openrouter", "anthropic", "mock"],
        help="Model provider to execute evaluation against (default: mock).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (e.g. gemini-2.5-pro, gemini-3.8-flash-high, qwen2.5-coder:7b, gpt-4o).",
    )
    parser.add_argument(
        "--tasks",
        default=None,
        help="Specific task suite name or path in evals/tasks/ (auto-resolved by default).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if the asset fails the delta-utility gate.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output evaluation results as raw JSON.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose task-by-task execution details.",
    )

    args = parser.parse_args()

    asset_path = Path(args.asset)
    if not asset_path.is_absolute():
        asset_path = REPO_ROOT / asset_path

    if not asset_path.is_file():
        print(f"Error: Asset file '{asset_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        provider = get_provider(args.provider, model=args.model)
    except Exception as e:
        print(f"Error initializing provider '{args.provider}': {e}", file=sys.stderr)
        return 1

    try:
        suite = load_task_suite(args.tasks, asset_path)
    except Exception as e:
        print(f"Error loading task suite: {e}", file=sys.stderr)
        return 1

    try:
        results = evaluate_asset(asset_path, provider, suite, verbose=args.verbose)
    except Exception as e:
        print(f"Evaluation error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)

    append_github_step_summary(results)

    if args.strict and not results["passed_gate"]:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
