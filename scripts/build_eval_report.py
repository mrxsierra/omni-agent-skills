#!/usr/bin/env python3
"""
Evaluation Scorecard Compiler for omni-agent-skills.

Parses all committed evaluation baselines in `evals/baselines/*.json` and compiles
a comprehensive public evaluation scorecard at `evals/README.md`.

Supports:
  python3 scripts/build_eval_report.py          # Compile evals/README.md
  python3 scripts/build_eval_report.py --check  # Verify evals/README.md is up-to-date
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINES_DIR = REPO_ROOT / "evals" / "baselines"
OUTPUT_FILE = REPO_ROOT / "evals" / "README.md"


def load_all_baselines() -> List[Dict[str, Any]]:
    """Load and sort all baseline files from evals/baselines/."""
    records = []
    if not BASELINES_DIR.is_dir():
        return records

    for f in sorted(BASELINES_DIR.glob("*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                data["_file"] = f.name
                records.append(data)
        except Exception as e:
            print(f"Warning: Failed to load baseline '{f.name}': {e}", file=sys.stderr)

    return sorted(records, key=lambda x: (x.get("domain", ""), x.get("suite_id", "")))


def generate_markdown(records: List[Dict[str, Any]]) -> str:
    """Generate the full public scorecard markdown content."""
    total_assets = len(records)
    total_providers = set()
    total_passed = 0
    total_entries = 0
    token_taxes = []

    for r in records:
        for p_name, p_data in r.get("baselines", {}).items():
            total_entries += 1
            total_providers.add(p_name)
            if p_data.get("passed_gate"):
                total_passed += 1
            if "token_tax_per_turn" in p_data:
                token_taxes.append(p_data["token_tax_per_turn"])

    avg_tax = round(sum(token_taxes) / len(token_taxes)) if token_taxes else 0
    pass_rate_pct = round((total_passed / total_entries * 100), 1) if total_entries else 0.0

    lines = [
        "# 📊 Empirical Evaluation & Quality Scorecard",
        "",
        "This directory contains the empirical evaluation baselines, benchmark task suites,",
        "and reproducible results for the assets published in the `omni-agent-skills` registry.",
        "",
        "> [!IMPORTANT]",
        "> **Zero-Hype Empirical Gate (ADR 0004 & ADR 0005):**",
        "> Every skill, rule, or workflow admitted to this registry must prove positive $\\Delta$-utility",
        "> or high baseline parity with minimal token tax. Prompt bloat, unverified claims, and",
        "> performance-degrading instructions are rejected automatically.",
        "",
        "## Summary Metrics",
        "",
        f"- **Total Catalog Assets Benchmarked:** {total_assets}",
        f"- **Benchmark Pass Rate:** {pass_rate_pct}% ({total_passed}/{total_entries} evaluations passed)",
        f"- **Average Context Token Tax:** +{avg_tax} tokens / turn",
        f"- **Evaluated Provider Engines:** {', '.join(sorted(total_providers))}",
        "",
        "---",
        "",
        "## Multi-Tier Evaluation Architecture (ADR 0005)",
        "",
        "Evaluation is decoupled into three operational tiers:",
        "",
        "| Tier | Engine | Target Environment | Cost & Speed | Primary Purpose |",
        "| :--- | :--- | :--- | :--- | :--- |",
        "| **Tier 1: Harness Gate** | `mock` (`MockProvider`) | Local & CI (`ci.yml`) | 0 cost, < 2s | Validates task format, schema wiring, and scoring algorithms deterministically. |",
        "| **Tier 2: Neural Smoke** | `ollama` (`qwen2.5-coder:1.5b`) | CI & Local Podman | 0 cost, ~2m | Smoke tests real open-weights neural token generation on CPU. |",
        "| **Tier 3: Cloud Heavy Lifting** | `agy` (Gemini 3.8 / Claude) | Local & Scheduled CI | Minimal API cost, ~5s | High-capacity reasoning benchmarks for complex multi-step refactoring skills. |",
        "",
        "---",
        "",
        "## Asset Benchmark Scorecard",
        "",
        "| Asset / Skill | Domain | Suite ID | Provider (Model) | Base % | Aug % | $\\Delta$-Utility | Token Tax | Gate Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for r in records:
        target_asset = r.get("target_asset", "")
        asset_name = Path(target_asset).parent.name if Path(target_asset).name == "SKILL.md" else Path(target_asset).name
        domain = r.get("domain", "n/a")
        suite_id = r.get("suite_id", "n/a")

        baselines = r.get("baselines", {})
        if not baselines:
            lines.append(f"| `{asset_name}` | {domain} | `{suite_id}` | *Pending evaluation* | - | - | - | - | ⏳ Pending |")
            continue

        for p_name, p_data in baselines.items():
            model = p_data.get("model", p_name)
            base_rate = f"{p_data.get('baseline_pass_rate', 0.0)}%"
            aug_rate = f"{p_data.get('augmented_pass_rate', 0.0)}%"
            delta_val = p_data.get("delta_utility", 0.0)
            delta_sign = "+" if delta_val >= 0 else ""
            delta_str = f"**{delta_sign}{delta_val}%**"
            tax = f"+{p_data.get('token_tax_per_turn', 0)} tok"
            status = "✅ PASS" if p_data.get("passed_gate") else "❌ FAIL"
            lines.append(
                f"| `{asset_name}` | {domain} | `{suite_id}` | `{p_name}` (`{model}`) | {base_rate} | {aug_rate} | {delta_str} | {tax} | {status} |"
            )

    lines.extend([
        "",
        "---",
        "",
        "## Reproducing & Running Evaluations",
        "",
        "Use the unified local evaluation helper script:",
        "",
        "```bash",
        "# 1. Instant deterministic mock run (< 2s, offline)",
        "scripts/run_local_eval.sh mock registry/skills/engineering/clean-code-auditor/SKILL.md",
        "",
        "# 2. Cloud evaluation via Antigravity CLI (zero download)",
        "scripts/run_local_eval.sh agy registry/skills/engineering/clean-code-auditor/SKILL.md gemini-3.8-flash-high",
        "",
        "# 3. Rootless containerized open-weights evaluation (Podman/Docker)",
        "scripts/run_local_eval.sh podman start qwen2.5-coder:1.5b",
        "scripts/run_local_eval.sh podman eval registry/skills/engineering/clean-code-auditor/SKILL.md",
        "scripts/run_local_eval.sh podman stop",
        "```",
        "",
        "To rebuild this report after updating baselines:",
        "```bash",
        "python3 scripts/build_eval_report.py",
        "```",
    ])

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile public evaluation scorecard for evals/README.md.")
    parser.add_argument("--check", action="store_true", help="Verify that evals/README.md matches current baselines.")
    args = parser.parse_args()

    records = load_all_baselines()
    if not records:
        print("Error: No baseline files found in evals/baselines/.", file=sys.stderr)
        return 1

    generated_md = generate_markdown(records)

    if args.check:
        if not OUTPUT_FILE.is_file():
            print(f"Check failed: {OUTPUT_FILE} does not exist. Run 'python3 scripts/build_eval_report.py'.", file=sys.stderr)
            return 1
        with open(OUTPUT_FILE, "r", encoding="utf-8") as fp:
            current_md = fp.read()
        if current_md != generated_md:
            print(f"Check failed: {OUTPUT_FILE} is out of date. Run 'python3 scripts/build_eval_report.py'.", file=sys.stderr)
            return 1
        print(f"✅ {OUTPUT_FILE} is up to date.")
        return 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fp:
        fp.write(generated_md)

    print(f"✅ Compiled evaluation scorecard for {len(records)} assets to {OUTPUT_FILE}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
