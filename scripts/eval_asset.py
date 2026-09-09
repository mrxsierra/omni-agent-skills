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
  python3 scripts/eval_asset.py --asset registry/rules/global/security_shield.md --provider gemini --model gemini-2.5-flash
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
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


def resolve_eval_tier(asset_path: Path, task_suite: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
    """Dynamically resolve the required evaluation capacity tier (ADR 0006).

    Tier S: Small / Compact (1B–7B)
    Tier M: Medium (8B–32B)
    Tier L: Large / Frontier (70B+)
    """
    suite = task_suite or {}
    explicit_tier = str(suite.get("eval_tier", "")).upper().strip()
    if explicit_tier in ("S", "M", "L"):
        labels = {
            "S": "Tier S: Small / Compact (1B–7B)",
            "M": "Tier M: Medium (8B–32B)",
            "L": "Tier L: Large / Frontier (70B+)",
        }
        return explicit_tier, labels[explicit_tier]

    path_str = str(asset_path).lower()
    if "rules" in path_str or "security-and-governance" in path_str:
        return "S", "Tier S: Small / Compact (1B–7B) [Taxonomy Default]"
    elif "architecture" in path_str or "protocols" in path_str:
        return "L", "Tier L: Large / Frontier (70B+) [Taxonomy Default]"
    else:
        return "M", "Tier M: Medium (8B–32B) [Taxonomy Default]"


def score_task(
    response_text: str,
    expected_keywords: List[str],
    fail_keywords: List[str],
    match_mode: str = "any",
    min_matches: int = 1,
) -> Tuple[bool, str]:
    """Deterministically score a response against keyword invariants and negative criteria (ADR 0006)."""
    text_lower = response_text.lower()

    # Check for forbidden failure keywords
    for bad in fail_keywords:
        if bad.lower() in text_lower:
            return False, f"Failed on forbidden keyword: '{bad}'"

    if not expected_keywords:
        return True, "Passed (no required keywords specified)"

    mode = match_mode.lower().strip()
    if mode == "all":
        missing = [good for good in expected_keywords if good.lower() not in text_lower]
        if missing:
            return False, f"Missing required keywords (match_mode=all): {missing}"
        return True, f"Passed (all {len(expected_keywords)} criteria met)"

    # Default 'any' mode with configurable min_matches threshold
    matches = [good for good in expected_keywords if good.lower() in text_lower]
    threshold = max(min_matches, 1)
    if len(matches) < threshold:
        return False, f"Matched only {len(matches)}/{threshold} required keywords from: {expected_keywords}"

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

    eval_tier_code, eval_tier_label = resolve_eval_tier(asset_path, task_suite)

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
        match_mode = task.get("match_mode", "any")
        min_matches = task.get("min_matches", 1)

        # 1. Baseline Run (Without Asset)
        base_resp: ModelResponse = provider.invoke(
            messages=[{"role": "user", "content": prompt}],
            system_prompt=baseline_system,
        )
        base_passed, base_reason = score_task(
            base_resp.text, expected, fail_kw, match_mode=match_mode, min_matches=min_matches
        )
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
        aug_passed, aug_reason = score_task(
            aug_resp.text, expected, fail_kw, match_mode=match_mode, min_matches=min_matches
        )
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
    elif delta == 0 and aug_rate == 1.0 and token_tax < 750:
        # Both passed on high-capacity model, reasonable token tax for comprehensive skill (< 750 tokens)
        verdict = "ACCEPTED (High Baseline Parity, Low Token Tax)"
        passed_gate = True
    else:
        verdict = "REJECTED (Bloat/Junk: No measurable improvement over baseline)"
        passed_gate = False

    return {
        "asset_path": str(asset_path),
        "eval_tier": eval_tier_code,
        "eval_tier_label": eval_tier_label,
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
    print(f"Capacity Tier:    {results.get('eval_tier_label', results.get('eval_tier', 'Tier M'))}")
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
| **Capacity Tier** | `{results.get('eval_tier_label', 'Tier M')}` |
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


def get_all_evaluable_assets() -> List[Path]:
    """Return all published evaluable assets in the registry (skills + task-targeted assets)."""
    assets = set()
    reg_dir = REPO_ROOT / "registry"
    # 1. All published skills
    skills_dir = reg_dir / "skills"
    if skills_dir.is_dir():
        for skill_file in skills_dir.glob("**/SKILL.md"):
            assets.add(skill_file.resolve())

    # 2. Any rules or workflows with dedicated task suites
    if TASKS_DIR.is_dir():
        for f in TASKS_DIR.glob("*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    target = data.get("target_asset", "")
                    if target:
                        p = (REPO_ROOT / target).resolve()
                        if p.is_file():
                            assets.add(p)
            except Exception:
                continue

    return sorted(assets)


def detect_changed_assets(base_ref: str = "origin/dev") -> List[Path]:
    """Detect added or modified assets in the working tree or branch compared to base_ref."""
    all_evaluable = {p.resolve(): p for p in get_all_evaluable_assets()}
    diff_targets = [f"{base_ref}...HEAD", base_ref, "dev...HEAD", "dev", "HEAD~1", "HEAD"]

    output = ""
    for target in diff_targets:
        try:
            res = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR", target, "--", "registry/"],
                cwd=REPO_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            if res.returncode == 0 and res.stdout.strip():
                output = res.stdout
                break
        except Exception:
            continue

    # Also include uncommitted, staged, or untracked changes
    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain", "--", "registry/"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if status_res.returncode == 0 and status_res.stdout.strip():
            for line in status_res.stdout.splitlines():
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    filepath = parts[1].strip()
                    if filepath not in output:
                        output += f"\n{filepath}"
    except Exception:
        pass

    changed = []
    for line in output.splitlines():
        rel = line.strip()
        if not rel:
            continue
        p = (REPO_ROOT / rel).resolve()
        if p in all_evaluable:
            changed.append(all_evaluable[p])
        elif p.is_file() and "registry" in str(p):
            # If a subfile in the asset directory changed, map it to the parent asset
            for eval_path in all_evaluable.values():
                if p.is_relative_to(eval_path.parent):
                    if eval_path not in changed:
                        changed.append(eval_path)

    return sorted(set(changed))


def save_baseline_result(results: Dict[str, Any]) -> None:
    """Update or create the baseline record in evals/baselines/ for this asset and provider."""
    baselines_dir = REPO_ROOT / "evals" / "baselines"
    if not baselines_dir.is_dir():
        return

    asset_rel = results["asset_path"]
    suite_id = results["task_suite"]

    # Locate existing baseline file
    target_file = None
    for f in baselines_dir.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                if data.get("target_asset") == asset_rel or data.get("suite_id") == suite_id:
                    target_file = f
                    break
        except Exception:
            continue

    if not target_file:
        target_file = baselines_dir / f"{suite_id}.json"
        data = {
            "suite_id": suite_id,
            "target_asset": asset_rel,
            "domain": Path(asset_rel).parent.parent.name if "skills" in asset_rel else "global",
            "phase": "phase-4-implementation",
            "baselines": {},
        }
    else:
        with open(target_file, "r", encoding="utf-8") as fp:
            data = json.load(fp)

    import datetime
    data["last_updated"] = datetime.date.today().isoformat()
    if "baselines" not in data:
        data["baselines"] = {}

    provider_key = results["provider"]
    data["baselines"][provider_key] = {
        "provider": results["provider"],
        "model": results["model"],
        "baseline_pass_rate": results["baseline_pass_rate"],
        "augmented_pass_rate": results["augmented_pass_rate"],
        "delta_utility": results["delta_utility"],
        "token_tax_per_turn": results["token_tax_per_turn"],
        "passed_gate": results["passed_gate"],
        "verdict": results["verdict"],
        "harness_verification_only": results.get("harness_verification_only", False),
    }

    with open(target_file, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)
        fp.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark registry assets across AI providers to verify positive delta utility."
    )
    parser.add_argument(
        "--asset",
        default=None,
        help="Path to the registry asset to evaluate (skill, rule, workflow). If omitted, delta mode auto-detects changed assets.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Force evaluation across all published registry assets.",
    )
    parser.add_argument(
        "--base-ref",
        default="origin/dev",
        help="Git base reference for delta detection (default: origin/dev).",
    )
    parser.add_argument(
        "--provider",
        default="mock",
        choices=[
            "antigravity",
            "gemini",
            "google",
            "agy",
            "mistral",
            "mistralai",
            "ollama",
            "openai",
            "openrouter",
            "anthropic",
            "mock",
        ],
        help="Model provider to execute evaluation against (default: mock).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (e.g. gemini-2.5-flash, codestral-latest, gemini-3.8-flash-high, qwen2.5-coder:7b, gpt-4o).",
    )
    parser.add_argument(
        "--tasks",
        default=None,
        help="Specific task suite name or path in evals/tasks/ (auto-resolved by default).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any asset fails the delta-utility gate.",
    )
    parser.add_argument(
        "--save-baseline",
        action="store_true",
        help="Save evaluation outcomes to evals/baselines/ for public scorecard generation.",
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

    # Determine asset paths to evaluate
    if args.asset:
        target_path = Path(args.asset)
        if not target_path.is_absolute():
            target_path = REPO_ROOT / target_path
        if not target_path.is_file():
            print(f"Error: Asset file '{target_path}' does not exist.", file=sys.stderr)
            return 1
        asset_paths = [target_path]
    elif args.all:
        asset_paths = get_all_evaluable_assets()
        print(f"ℹ️ Full catalog sweep: evaluating all {len(asset_paths)} registry assets.")
    else:
        # Default: Git-aware Delta Detection
        asset_paths = detect_changed_assets(base_ref=args.base_ref)
        if not asset_paths:
            print(f"ℹ️ No modified or newly added registry assets detected compared to '{args.base_ref}'. Neural evaluation skipped.")
            return 0
        print(f"ℹ️ Delta evaluation: detected {len(asset_paths)} modified/added registry asset(s):")
        for p in asset_paths:
            print(f"   - {p.relative_to(REPO_ROOT) if p.is_relative_to(REPO_ROOT) else p}")

    try:
        provider = get_provider(args.provider, model=args.model)
    except Exception as e:
        print(f"Error initializing provider '{args.provider}': {e}", file=sys.stderr)
        return 1

    all_results = []
    any_gate_failed = False

    for asset_path in asset_paths:
        try:
            suite = load_task_suite(args.tasks, asset_path)
        except Exception as e:
            print(f"Error loading task suite for '{asset_path}': {e}", file=sys.stderr)
            if args.strict:
                return 1
            continue

        try:
            results = evaluate_asset(asset_path, provider, suite, verbose=args.verbose)
            all_results.append(results)
            if not results["passed_gate"]:
                any_gate_failed = True

            if not args.json:
                print_report(results)

            append_github_step_summary(results)

            if args.save_baseline:
                save_baseline_result(results)

        except Exception as e:
            print(f"Evaluation error on '{asset_path}': {e}", file=sys.stderr)
            if args.strict:
                return 1

    if args.json:
        if len(all_results) == 1:
            print(json.dumps(all_results[0], indent=2))
        else:
            print(json.dumps(all_results, indent=2))

    if len(all_results) > 1 and not args.json:
        # Print summary banner for multi-asset runs
        passed_count = sum(1 for r in all_results if r["passed_gate"])
        print("\n" + "=" * 70)
        print(f"🏁 Batch Evaluation Complete: {passed_count}/{len(all_results)} passed gate.")
        print("=" * 70 + "\n")

    if args.strict and any_gate_failed:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
