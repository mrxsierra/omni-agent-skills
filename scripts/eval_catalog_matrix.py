#!/usr/bin/env python3
"""
Catalog Evaluation Matrix Runner for omni-agent-skills.

Executes real model evaluations across all catalog assets, records empirical
baselines into `evals/baselines/*.json`, and rebuilds `evals/README.md`.

Supports:
  python3 scripts/eval_catalog_matrix.py --provider agy --model gemini-3.8-flash-high
  python3 scripts/eval_catalog_matrix.py --provider mock
  python3 scripts/eval_catalog_matrix.py --provider ollama --model qwen2.5-coder:1.5b
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
BASELINES_DIR = REPO_ROOT / "evals" / "baselines"

sys.path.insert(0, str(SCRIPTS_DIR))
from eval_asset import evaluate_asset, load_task_suite
from eval_providers import get_provider
from build_eval_report import load_all_baselines, generate_markdown, OUTPUT_FILE


def get_all_target_assets() -> List[Path]:
    """Return all catalog assets with evaluation task suites."""
    assets = sorted(Path(p) for p in glob.glob(str(REPO_ROOT / "registry" / "skills" / "**" / "SKILL.md"), recursive=True))
    rule_path = REPO_ROOT / "registry" / "rules" / "global" / "security_shield.md"
    if rule_path.is_file():
        assets.append(rule_path)
    return assets


def update_baseline_file(suite_id: str, results: Dict[str, Any], provider_key: str) -> None:
    """Update or inject provider benchmark results into evals/baselines/<suite_id>.json."""
    baseline_file = BASELINES_DIR / f"{suite_id}.json"
    if not baseline_file.is_file():
        print(f"Warning: Baseline file '{baseline_file}' does not exist. Skipping update.", file=sys.stderr)
        return

    with open(baseline_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    today_str = datetime.date.today().isoformat()
    data["last_updated"] = today_str

    if "baselines" not in data:
        data["baselines"] = {}

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

    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def run_matrix(provider_name: str, model_name: str, verbose: bool = False) -> int:
    """Run evaluation matrix across all assets."""
    assets = get_all_target_assets()
    print(f"\n🚀 Launching Catalog Evaluation Matrix ({len(assets)} assets)")
    print(f"Provider: {provider_name} | Model: {model_name}")
    print("=" * 70)

    try:
        provider = get_provider(provider_name, model=model_name)
    except Exception as e:
        print(f"Error initializing provider '{provider_name}': {e}", file=sys.stderr)
        return 1

    passed_count = 0
    failed_count = 0

    for idx, asset in enumerate(assets, 1):
        asset_rel = asset.relative_to(REPO_ROOT)
        print(f"[{idx}/{len(assets)}] Evaluating: {asset_rel} ...", end=" ", flush=True)

        try:
            suite = load_task_suite(None, asset)
            results = evaluate_asset(asset, provider, suite, verbose=verbose)
            update_baseline_file(suite["suite_id"], results, provider_key=provider.provider_name)

            if results["passed_gate"]:
                passed_count += 1
                delta_sign = "+" if results['delta_utility'] >= 0 else ""
                print(f"✅ PASS (Δ={delta_sign}{results['delta_utility']}%, tax=+{results['token_tax_per_turn']}tok)")
            else:
                failed_count += 1
                print(f"❌ FAIL ({results['verdict']})")
        except Exception as e:
            failed_count += 1
            print(f"⚠️ ERROR: {e}")

    print("=" * 70)
    print(f"Matrix Completed: {passed_count} Passed, {failed_count} Failed.")

    # Rebuild evals/README.md public scorecard
    records = load_all_baselines()
    scorecard_md = generate_markdown(records)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fp:
        fp.write(scorecard_md)
    print(f"✅ Updated public scorecard at {OUTPUT_FILE}")

    return 0 if failed_count == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run full catalog evaluation matrix across models.")
    parser.add_argument("--provider", default="agy", choices=["agy", "mock", "ollama", "openai", "openrouter"], help="Provider name")
    parser.add_argument("--model", default="gemini-3.8-flash-high", help="Model name")
    parser.add_argument("--verbose", action="store_true", help="Print verbose reasoning")
    args = parser.parse_args()

    return run_matrix(args.provider, args.model, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
