#!/usr/bin/env python3
"""
Preflight API Key & Model Connectivity Diagnostic Tool for omni-agent-skills.

Verifies configured AI provider credentials, model accessibility, and rate-limit quotas
before launching heavy neural evaluation benchmarks.

Supported Providers:
  - Google Gemini (Direct REST API)
  - Mistral AI (Direct REST API)
  - OpenRouter (Free-tier & Paid API)
  - Local Ollama (Daemon connectivity & local model tags)
  - Google Antigravity CLI (`agy`)
  - OpenAI / ChatGPT
  - Anthropic / Claude

Zero external dependencies: Uses Python standard library only (urllib, json, os, sys).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from eval_providers import get_provider, load_dotenv_if_exists  # noqa: E402

load_dotenv_if_exists()


def mask_key(key: Optional[str]) -> str:
    """Mask an API key for safe terminal display, guaranteeing zero secret exposure."""
    if not key or not key.strip():
        return "(not set)"
    k = key.strip()
    if len(k) <= 8:
        return "***"
    prefix = k[:4]
    suffix = k[-3:]
    return f"{prefix}...{suffix}"


def check_openrouter_quota(api_key: str, timeout: int = 10) -> Dict[str, Any]:
    """Query OpenRouter /api/v1/key endpoint for account limits and usage stats."""
    url = "https://openrouter.ai/api/v1/key"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/mrxsierra/omni-agent-skills",
            "X-Title": "omni-agent-skills key checker",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            key_data = data.get("data", {})
            is_free = key_data.get("is_free_tier", False)
            usage_daily = key_data.get("usage_daily", 0)
            limit = key_data.get("limit")
            return {
                "ok": True,
                "is_free_tier": is_free,
                "usage_daily": usage_daily,
                "limit": limit,
                "quota_label": "Free Tier (50 req/day cap)" if is_free else f"Paid/Credit Tier (Limit: {limit or 'Unlimited'})",
            }
    except Exception as e:
        return {"ok": False, "error": str(e), "quota_label": "Unknown"}


def check_ollama(base_url: str = "http://localhost:11434", timeout: int = 5) -> Dict[str, Any]:
    """Check local Ollama daemon reachability and list installed models."""
    url = f"{base_url.rstrip('/')}/api/tags"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name", "") for m in data.get("models", [])]
            return {
                "ok": True,
                "models": models,
                "note": f"{len(models)} model(s) available locally",
            }
    except Exception as e:
        return {"ok": False, "error": str(e), "note": "Ollama daemon not running (run `ollama serve`)"}


def check_agy_cli() -> Dict[str, Any]:
    """Check if Antigravity CLI (`agy`) binary is available on PATH."""
    import shutil

    cli_path = os.environ.get("AGY_CLI_PATH") or shutil.which("agy")
    if cli_path:
        return {"ok": True, "path": cli_path, "note": "Antigravity CLI available"}
    return {"ok": False, "path": None, "note": "agy CLI not found on PATH"}


def probe_provider(
    provider_name: str,
    model_name: str,
    is_mock: bool = False,
    timeout: int = 15,
) -> Tuple[bool, str, float, str]:
    """Perform a minimal 1-token ping probe to verify endpoint connectivity."""
    if is_mock:
        return True, "pong", 2.0, "Mock verification pass"

    start = time.time()
    try:
        provider = get_provider(provider_name, model=model_name)
        response = provider.invoke(
            messages=[{"role": "user", "content": "Respond with the word pong."}],
            max_tokens=5,
        )
        latency = (time.time() - start) * 1000
        reply = response.text.strip()[:30]
        return True, reply, latency, "OK"
    except Exception as e:
        latency = (time.time() - start) * 1000
        err_msg = str(e)
        return False, "", latency, err_msg


def run_checks(is_mock: bool = False) -> int:
    """Execute all preflight provider checks and display formatted diagnostics."""
    print("\n" + "=" * 75)
    print("🔍 omni-agent-skills Preflight API Key & Model Connectivity Check")
    print("=" * 75)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print(f"Mode:      {'MOCK SIMULATION' if is_mock else 'LIVE ENDPOINT PROBE'}")
    print("-" * 75)

    results: List[Dict[str, Any]] = []

    # 1. Google Gemini
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    gemini_model = "gemini-2.5-flash"
    if gemini_key or is_mock:
        ok, reply, latency, err = probe_provider("gemini", gemini_model, is_mock=is_mock)
        results.append({
            "provider": "Google Gemini",
            "key": mask_key(gemini_key if not is_mock else "AIzaSyFakeKeyMockTesting"),
            "model": gemini_model,
            "status": "✅ PASS" if ok else "❌ FAIL",
            "latency_ms": latency,
            "quota_tier": "Free Tier (15 RPM / 1,500 RPD)",
            "details": reply if ok else err,
        })
    else:
        results.append({
            "provider": "Google Gemini",
            "key": "(not set)",
            "model": gemini_model,
            "status": "⚪ SKIPPED",
            "latency_ms": 0.0,
            "quota_tier": "Set GEMINI_API_KEY in .env",
            "details": "Provider key not configured",
        })

    # 2. Mistral AI
    mistral_key = os.environ.get("MISTRAL_API_KEY")
    mistral_model = "codestral-latest"
    if mistral_key or is_mock:
        ok, reply, latency, err = probe_provider("mistral", mistral_model, is_mock=is_mock)
        results.append({
            "provider": "Mistral AI",
            "key": mask_key(mistral_key if not is_mock else "mis_fakeKeyMockTesting"),
            "model": mistral_model,
            "status": "✅ PASS" if ok else "❌ FAIL",
            "latency_ms": latency,
            "quota_tier": "Standard (125 RPM / 625k TPM)",
            "details": reply if ok else err,
        })
    else:
        results.append({
            "provider": "Mistral AI",
            "key": "(not set)",
            "model": mistral_model,
            "status": "⚪ SKIPPED",
            "latency_ms": 0.0,
            "quota_tier": "Set MISTRAL_API_KEY in .env",
            "details": "Provider key not configured",
        })

    # 3. OpenRouter
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    openrouter_model = "nvidia/nemotron-3.5-lightning:free"
    if openrouter_key or is_mock:
        quota_info = check_openrouter_quota(openrouter_key or "fake") if not is_mock else {"ok": True, "quota_label": "Free Tier (50 req/day cap)"}
        ok, reply, latency, err = probe_provider("openrouter", openrouter_model, is_mock=is_mock)
        results.append({
            "provider": "OpenRouter",
            "key": mask_key(openrouter_key if not is_mock else "sk-or-fakeKeyMockTesting"),
            "model": openrouter_model,
            "status": "✅ PASS" if ok else "❌ FAIL",
            "latency_ms": latency,
            "quota_tier": quota_info.get("quota_label", "Unknown"),
            "details": reply if ok else err,
        })
    else:
        results.append({
            "provider": "OpenRouter",
            "key": "(not set)",
            "model": openrouter_model,
            "status": "⚪ SKIPPED",
            "latency_ms": 0.0,
            "quota_tier": "Set OPENROUTER_API_KEY in .env",
            "details": "Provider key not configured",
        })

    # 4. Local Ollama
    ollama_info = check_ollama() if not is_mock else {"ok": True, "note": "1 model(s) available locally"}
    results.append({
        "provider": "Local Ollama",
        "key": "N/A (Local Daemon)",
        "model": "qwen2.5-coder:1.5b",
        "status": "✅ READY" if ollama_info["ok"] else "⚪ OFFLINE",
        "latency_ms": 0.0,
        "quota_tier": "Unlimited (Local Compute)",
        "details": ollama_info.get("note", ""),
    })

    # 5. Antigravity CLI (agy)
    agy_info = check_agy_cli() if not is_mock else {"ok": True, "note": "Antigravity CLI available"}
    results.append({
        "provider": "Antigravity CLI (agy)",
        "key": "N/A (Local Auth)",
        "model": "gemini-3.8-flash-high",
        "status": "✅ READY" if agy_info["ok"] else "⚪ NOT FOUND",
        "latency_ms": 0.0,
        "quota_tier": "Frontier Cloud (via agy CLI)",
        "details": agy_info.get("note", ""),
    })

    # 6. Optional Direct OpenAI
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        ok, reply, latency, err = probe_provider("openai", "gpt-4o-mini", is_mock=is_mock)
        results.append({
            "provider": "OpenAI",
            "key": mask_key(openai_key),
            "model": "gpt-4o-mini",
            "status": "✅ PASS" if ok else "❌ FAIL",
            "latency_ms": latency,
            "quota_tier": "Paid / Account Credit",
            "details": reply if ok else err,
        })

    # 7. Optional Direct Anthropic
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        ok, reply, latency, err = probe_provider("anthropic", "claude-3-5-haiku-20241022", is_mock=is_mock)
        results.append({
            "provider": "Anthropic",
            "key": mask_key(anthropic_key),
            "model": "claude-3-5-haiku-20241022",
            "status": "✅ PASS" if ok else "❌ FAIL",
            "latency_ms": latency,
            "quota_tier": "Paid / Account Credit",
            "details": reply if ok else err,
        })

    # Display aligned results
    print(f"{'Provider':<24} {'Key Status':<15} {'Model / Probe':<30} {'Status':<10} {'Latency':<9}")
    print("-" * 90)
    for r in results:
        lat_str = f"{r['latency_ms']:.0f}ms" if r['latency_ms'] > 0 else "-"
        print(f"{r['provider']:<24} {r['key']:<15} {r['model']:<30} {r['status']:<10} {lat_str:<9}")

    print("-" * 90)
    print("\n📋 Quota & Tier Breakdown:")
    for r in results:
        print(f"  • {r['provider']}: {r['quota_tier']}")

    # Check for failures and print actionable remediation
    failures = [r for r in results if r["status"] == "❌ FAIL"]
    if failures:
        print("\n" + "!" * 75)
        print("⚠️  Actionable Remediation Guidance:")
        for f in failures:
            print(f"\n[{f['provider']} - {f['model']}]:")
            print(f"  Error: {f['details']}")
            if "openrouter" in f['provider'].lower():
                print("  Hint:  Free OpenRouter accounts require models ending in ':free'.")
                print("         Try: --model nvidia/nemotron-3.5-lightning:free or --model liquid/lfm-2.5-2.6b:free")
            elif "gemini" in f['provider'].lower():
                print("  Hint:  Google AI Studio free tier supports gemini-2.5-flash (15 RPM).")
                print("         Ensure model is 'gemini-2.5-flash'.")
            elif "mistral" in f['provider'].lower():
                print("  Hint:  For code evaluation, use 'codestral-latest' which has 125 RPM quota.")
        print("!" * 75 + "\n")
        return 1

    configured_count = sum(1 for r in results if "PASS" in r["status"] or "READY" in r["status"])
    print(f"\n✅ Preflight check complete: {configured_count} provider engine(s) operational.")
    print("   You are ready to run neural evaluation benchmarks!\n")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Preflight API Key & Model Diagnostic Tool")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run offline mock simulation (tests tool output without network requests)",
    )
    args = parser.parse_args()
    exit_code = run_checks(is_mock=args.mock)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
