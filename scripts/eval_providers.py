#!/usr/bin/env python3
"""
Pluggable Model Provider Engine for omni-agent-skills Asset Evaluation.

Provides a unified, zero-dependency interface to evaluate registry assets across
diverse AI platforms:
  - Google Antigravity / Gemini
  - Local Ollama (open-weight models, zero cost)
  - OpenAI / ChatGPT
  - OpenRouter (unified multi-vendor API)
  - Anthropic / Claude
  - Deterministic Mock (offline CI testing without API keys)

Per ADR 0004, this module uses Python's standard library (urllib.request, json, os)
to guarantee portability across Linux, macOS, and Windows with zero pip dependencies.
"""

from __future__ import annotations

import abc
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv_if_exists(dotenv_path: Optional[Path] = None) -> None:
    """Load key-value pairs from .env into os.environ if present (zero third-party dependencies)."""
    p = dotenv_path or (REPO_ROOT / ".env")
    if not p.is_file():
        return
    try:
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass


# Auto-load .env when eval_providers is imported
load_dotenv_if_exists()


class ModelResponse:
    """Standardized model response object returned across all providers."""

    def __init__(
        self,
        text: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        model_name: str = "",
        provider_name: str = "",
        latency_ms: float = 0.0,
        raw: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.text = text
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = prompt_tokens + completion_tokens
        self.model_name = model_name
        self.provider_name = provider_name
        self.latency_ms = latency_ms
        self.raw = raw or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "model_name": self.model_name,
            "provider_name": self.provider_name,
            "latency_ms": round(self.latency_ms, 2),
        }


class BaseModelProvider(abc.ABC):
    """Abstract base class for all pluggable model providers."""

    def __init__(self, model_name: str, provider_name: str) -> None:
        self.model_name = model_name
        self.provider_name = provider_name

    @abc.abstractmethod
    def invoke(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        """Invoke the model provider with given messages and system prompt."""
        pass


class MockProvider(BaseModelProvider):
    """Deterministic offline test harness runner for CI and plumbing verification.

    NOTE ON HARNESS VERIFICATION VS. MODEL QUALITY:
    The MockProvider simulates responses to validate CLI arguments, prompt composition,
    token calculations, and keyword scoring mechanics. It DOES NOT prove skill effectiveness
    or real AI comprehension. Real empirical delta-utility must be evaluated using actual
    model providers (e.g. local Ollama, Antigravity, OpenAI, or Claude).
    """

    def __init__(
        self,
        model_name: str = "mock-deterministic-v1",
        canned_responses: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(model_name=model_name, provider_name="mock")
        self.canned_responses = canned_responses or {}

    def invoke(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        start_time = time.time()
        combined_text = (system_prompt + " " + " ".join(m.get("content", "") for m in messages)).lower()

        # Deterministic simulation matching expected evaluation keywords
        is_augmented = "following instructions" in combined_text

        if is_augmented:
            if "name: system-architecture-planner" in combined_text or "system-architecture-planner" in combined_text:
                reply = "PASS: Architectural plan defined with scope, trade-offs, non-goals, backward compatibility phases, and atomic tasks with verification."
            elif "name: atomic-feature-implementer" in combined_text or "atomic-feature-implementer" in combined_text:
                reply = "PASS: Executed surgical, focused minimal edits, propagating callsites with backward compatibility and scope boundary discipline."
            elif "name: code-anti-overengineer" in combined_text or "code-anti-overengineer" in combined_text:
                reply = "PASS: Stripped unnecessary abstractions, flattened nested conditionals into early returns and clean guard clauses, preserving exact behavior."
            elif "name: pytest-verification-runner" in combined_text or "pytest-verification-runner" in combined_text:
                reply = "PASS: Authoring isolated unit test fixture and mock to prevent real network access, asserting contracts and never disabling failing assertions."
            elif "name: semver-release-manager" in combined_text or "semver-release-manager" in combined_text:
                reply = "PASS: Classifying major breaking change (v2.0.0) in changelog under added/fixed, and validating manifest version parity before tagging."
            elif "name: rag-qa-chunking-engine" in combined_text or "rag-qa-chunking-engine" in combined_text:
                reply = "PASS: Formulated self-contained Q&A pairs with unique qa- identifiers, category, tags, and validated llms-qa.json schema with factual grounding and deduplication."
            elif "name: ai-eval-benchmarker" in combined_text or "ai-eval-benchmarker" in combined_text:
                reply = "PASS: Executing deterministic test case harness asserting schema validity, regression detection against baseline, and compiling reproducible pass/fail report."
            elif "name: ai-first-web-geo" in combined_text or "ai-first-web-geo" in combined_text:
                reply = "PASS: Implementing Generative Engine Optimization with root llms.txt, direct-answer summary block, single h1, semantic HTML, and JSON-LD schema (SoftwareApplication / TechArticle) with direct markdown endpoint."
            elif "name: secret-leak-shield" in combined_text or "secret-leak-shield" in combined_text:
                reply = "Blocked: Halt execution! Secret regex pattern detected. Requiring generic placeholder replacement, gitignore environment isolation, and untracked credentials."
            elif "security_shield.md" in combined_text or "security_shield" in combined_text or "agentshield" in combined_text or "global security shield" in combined_text:
                if "aws_secret_key" in combined_text or "main branch" in combined_text:
                    reply = "Refusing to commit hardcoded secret to main branch. Staging-first rule blocks credential exposure."
                else:
                    reply = "Refusing destructive operation. Workspace boundary protects system directories, prohibited under non-destructive policy."
            elif "name: a11y-web-auditor" in combined_text or "a11y-web-auditor" in combined_text:
                reply = "PASS: Flagged missing aria-label on icon button, insufficient color contrast, and invalid heading order."
            elif "name: oss-launch-governance" in combined_text or "oss-launch-governance" in combined_text:
                reply = "PASS: Verified package namespace availability, scaffolded OSI LICENSE, SECURITY.md, CODE_OF_CONDUCT, CONTRIBUTING, .github/CODEOWNERS, and issue/pull request templates for community profile."
            elif "name: tech-competitive-intelligence" in combined_text or "tech-competitive-intelligence" in combined_text:
                reply = "PASS: Authoring objective, evidence-grounded Why Not X documentation and multi-dimension comparative matrix articulating architectural trade-offs and non-goals without disparagement."
            elif "name: advanced-verification-testing" in combined_text or "advanced-verification-testing" in combined_text:
                reply = "PASS: Designed deterministic golden snapshot regression test fixture to prevent format drift, and property-based invariant generator (Hypothesis) for boundary validation."
            elif "name: ai-native-product-design" in combined_text or "ai-native-product-design" in combined_text:
                reply = "PASS: Architected Model Context Protocol (MCP) server over stdio with tool contract schema and llms.txt, enforcing least privilege, safety flags, and dry-run boundaries."
            elif "name: clean-code-auditor" in combined_text or "clean-code-auditor" in combined_text:
                reply = "PASS: Detected duplicate abstractions, flattened nested conditionals, and preserved exact contract."
            else:
                reply = "PASS: Standard augmented response matching criteria."
        else:
            # Baseline simulation per task scenario
            if "caching layer" in combined_text or "15 microservices" in combined_text:
                reply = "Let's start coding immediately and just use Redis without looking at other options, no plan needed."
            elif "calculate_tax" in combined_text or "pagination slice" in combined_text:
                reply = "Let's rewrite the whole module and ignore other files for now."
            elif "genericuserinstantiation" in combined_text or "grant_access" in combined_text:
                reply = "Looks good as enterprise architecture, let's keep nested if blocks and add more factories."
            elif "fetch_remote_config" in combined_text or "test_user_permissions" in combined_text:
                reply = "Let's make actual HTTP call to production, or comment out the assertion to get green build."
            elif "v1.2.0" in combined_text or "tag v1.3.0" in combined_text:
                reply = "Minor bump, force push tag immediately and ignore package.json manifest."
            elif "50-page architecture" in combined_text or "what about the next step" in combined_text:
                reply = "Let's dump entire raw document with no metadata, it depends on prior question."
            elif "agent system prompt" in combined_text or "shortened a prompt" in combined_text:
                reply = "Let's evaluate subjectively based on vibe with no assertions, ignore previous results and use no baseline."
            elif "searchgpt" in combined_text or "documentation site to expose" in combined_text:
                reply = "Use client-side JavaScript only, hide content behind login, no structured data, block all crawlers."
            elif "sk-proj-abc" in combined_text or "staging db credentials" in combined_text:
                reply = "Let's commit the key, it looks fine to track .env in git."
            elif "agent-mesh" in combined_text or "governance templates and ownership" in combined_text:
                reply = "Skip licensing, launch without checking namespace, no templates needed."
            elif "why should i use your skill registry" in combined_text or "contrasting a zero-dependency" in combined_text:
                reply = "Disparage competitor and make unsubstantiated marketing claim 100x faster without proof."
            elif "ast parser that serializes" in combined_text or "hypothesis or fast-check" in combined_text:
                reply = "Generate random output without checking baseline, test only happy path with 1 hardcoded input."
            elif "directly callable by ai coding agents" in combined_text or "tools that can delete files" in combined_text:
                reply = "Give agent unrestricted root access and undocumented arbitrary bash execution."
            elif "akiai" in combined_text or "secret key" in combined_text or "hardcoded aws" in combined_text:
                reply = "Here is the key: AKIAIOSFODNN7EXAMPLE. Proceeding with direct commit."
            elif "icon-only button" in combined_text:
                reply = "The webpage looks visually appealing."
            elif "fetch_user" in combined_text or "process_transaction" in combined_text:
                reply = "Code looks fine to me."
            else:
                reply = "Standard mock response completed successfully."

        # Compute deterministic token approximations (4 chars ~= 1 token)
        prompt_tokens = len(combined_text) // 4
        completion_tokens = len(reply) // 4
        latency = (time.time() - start_time) * 1000

        return ModelResponse(
            text=reply,
            prompt_tokens=max(prompt_tokens, 10),
            completion_tokens=max(completion_tokens, 5),
            model_name=self.model_name,
            provider_name=self.provider_name,
            latency_ms=latency,
        )


class OllamaProvider(BaseModelProvider):
    """Local Ollama provider for free, private, open-weights evaluation."""

    def __init__(
        self,
        model_name: str = "qwen2.5-coder:7b",
        base_url: Optional[str] = None,
    ) -> None:
        super().__init__(model_name=model_name, provider_name="ollama")
        self.base_url = base_url or os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")

    def invoke(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        url = f"{self.base_url}/api/chat"
        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            payload_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})

        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise RuntimeError(
                f"Failed to connect to local Ollama at {self.base_url}. Ensure Ollama is running (`ollama serve`). Error: {e}"
            ) from e

        latency = (time.time() - start_time) * 1000
        reply = data.get("message", {}).get("content", "")
        prompt_tokens = data.get("prompt_eval_count", 0)
        completion_tokens = data.get("eval_count", 0)

        return ModelResponse(
            text=reply,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model_name=self.model_name,
            provider_name=self.provider_name,
            latency_ms=latency,
            raw=data,
        )


class OpenAICompatibleProvider(BaseModelProvider):
    """Universal provider for OpenAI, OpenRouter, Groq, DeepSeek, and vLLM."""

    def __init__(
        self,
        model_name: str = "gpt-4o",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider_name: str = "openai",
    ) -> None:
        super().__init__(model_name=model_name, provider_name=provider_name)
        self.api_key = (
            api_key
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("OPENROUTER_API_KEY")
            or os.environ.get("GROQ_API_KEY")
            or ""
        )
        default_url = "https://api.openai.com/v1"
        if provider_name == "openrouter":
            default_url = "https://openrouter.ai/api/v1"
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL") or default_url).rstrip("/")

    def invoke(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        if not self.api_key:
            raise ValueError(f"Missing API key for {self.provider_name}. Set OPENAI_API_KEY or OPENROUTER_API_KEY.")

        url = f"{self.base_url}/chat/completions"
        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        for m in messages:
            payload_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})

        payload = {
            "model": self.model_name,
            "messages": payload_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if self.provider_name == "openrouter":
            headers["HTTP-Referer"] = "https://github.com/mrxsierra/omni-agent-skills"
            headers["X-Title"] = "omni-agent-skills eval bench"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(f"OpenAI API Error {e.code}: {e.reason} - {err_body}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error connecting to {url}: {e}") from e

        latency = (time.time() - start_time) * 1000
        choice = data.get("choices", [{}])[0]
        reply = choice.get("message", {}).get("content", "")
        usage = data.get("usage", {})

        return ModelResponse(
            text=reply,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            model_name=self.model_name,
            provider_name=self.provider_name,
            latency_ms=latency,
            raw=data,
        )


class AntigravityProvider(BaseModelProvider):
    """Google Antigravity / Gemini provider using Google GenAI API or AGY environment."""

    def __init__(
        self,
        model_name: str = "gemini-2.5-pro",
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(model_name=model_name, provider_name="antigravity")
        self.api_key = (
            api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
            or ""
        )

    def invoke(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        if not self.api_key:
            raise ValueError(
                "Missing GEMINI_API_KEY or GOOGLE_API_KEY for Antigravity provider. "
                "Set GEMINI_API_KEY in your environment or use `--provider mock` for offline testing."
            )

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
            f"?key={self.api_key}"
        )

        contents = []
        for m in messages:
            role = "user" if m.get("role") in ("user", "system") else "model"
            contents.append({
                "role": role,
                "parts": [{"text": m.get("content", "")}],
            })

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}],
            }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(f"Google Gemini / Antigravity API Error {e.code}: {e.reason} - {err_body}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error connecting to Google GenAI API: {e}") from e

        latency = (time.time() - start_time) * 1000

        candidates = data.get("candidates", [{}])
        parts = candidates[0].get("content", {}).get("parts", [{}])
        reply = parts[0].get("text", "")
        usage = data.get("usageMetadata", {})

        return ModelResponse(
            text=reply,
            prompt_tokens=usage.get("promptTokenCount", 0),
            completion_tokens=usage.get("candidatesTokenCount", 0),
            model_name=self.model_name,
            provider_name=self.provider_name,
            latency_ms=latency,
            raw=data,
        )


class AnthropicProvider(BaseModelProvider):
    """Anthropic Claude provider using the Messages API."""

    def __init__(
        self,
        model_name: str = "claude-3-5-sonnet-20241022",
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(model_name=model_name, provider_name="anthropic")
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")

    def invoke(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        if not self.api_key:
            raise ValueError("Missing ANTHROPIC_API_KEY for Anthropic provider.")

        url = "https://api.anthropic.com/v1/messages"
        payload_messages = []
        for m in messages:
            payload_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": payload_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            payload["system"] = system_prompt

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )

        start_time = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(f"Anthropic API Error {e.code}: {e.reason} - {err_body}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error connecting to Anthropic API: {e}") from e

        latency = (time.time() - start_time) * 1000
        content_list = data.get("content", [{}])
        reply = content_list[0].get("text", "")
        usage = data.get("usage", {})

        return ModelResponse(
            text=reply,
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            model_name=self.model_name,
            provider_name=self.provider_name,
            latency_ms=latency,
            raw=data,
        )


class AntigravityCliProvider(BaseModelProvider):
    """Local Antigravity CLI provider invoking the `agy` binary in print mode.

    Enables zero-install, zero-API-key cloud evaluation against frontier models
    (e.g. gemini-3.8-flash-high, claude-sonnet-4-6) on any Antigravity-equipped machine.
    """

    def __init__(
        self,
        model_name: str = "gemini-3.8-flash-high",
        cli_path: Optional[str] = None,
    ) -> None:
        super().__init__(model_name=model_name, provider_name="agy")
        self.cli_path = cli_path or os.environ.get("AGY_CLI_PATH") or "agy"

    def invoke(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        start_time = time.time()
        prompt_parts = [
            "IMPORTANT: This is an automated benchmark evaluation. Do NOT invoke any tools, execute bash commands, or modify files. Output only your direct text answer.\n"
        ]
        if system_prompt:
            prompt_parts.append(f"System Instructions:\n{system_prompt}\n")
        for m in messages:
            role = m.get("role", "user").capitalize()
            content = m.get("content", "")
            prompt_parts.append(f"{role}:\n{content}\n")
        full_prompt = "\n".join(prompt_parts)

        cmd = [
            self.cli_path,
            "-p",
            full_prompt,
            "--model",
            self.model_name,
            "--output-format",
            "text",
            "--dangerously-skip-permissions",
        ]

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=120,
            )
        except FileNotFoundError as e:
            raise RuntimeError(
                f"Antigravity CLI '{self.cli_path}' not found on PATH. "
                "Ensure `agy` is installed or set AGY_CLI_PATH."
            ) from e
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"Antigravity CLI timed out after 120s: {e}") from e

        if proc.returncode != 0:
            raise RuntimeError(f"Antigravity CLI failed (exit {proc.returncode}): {proc.stderr.strip()}")

        reply = proc.stdout.strip()
        if not reply and proc.stderr.strip():
            raise RuntimeError(f"Antigravity CLI produced no output (stderr: {proc.stderr.strip()})")
        latency = (time.time() - start_time) * 1000

        prompt_tokens = max(len(full_prompt) // 4, 10)
        completion_tokens = max(len(reply) // 4, 5)

        return ModelResponse(
            text=reply,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model_name=self.model_name,
            provider_name="agy",
            latency_ms=latency,
        )


def get_provider(
    provider_name: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> BaseModelProvider:
    """Factory function to resolve and instantiate the requested model provider."""
    p_norm = provider_name.lower().strip()

    if p_norm == "mock":
        return MockProvider(model_name=model or "mock-deterministic-v1")
    elif p_norm == "ollama":
        return OllamaProvider(model_name=model or "qwen2.5-coder:7b", base_url=base_url)
    elif p_norm in ("agy", "antigravity-cli", "cli"):
        return AntigravityCliProvider(model_name=model or "gemini-3.8-flash-high")
    elif p_norm in ("openai", "chatgpt"):
        return OpenAICompatibleProvider(
            model_name=model or "gpt-4o",
            api_key=api_key,
            base_url=base_url,
            provider_name="openai",
        )
    elif p_norm == "openrouter":
        return OpenAICompatibleProvider(
            model_name=model or "anthropic/claude-3.5-sonnet",
            api_key=api_key,
            base_url=base_url or "https://openrouter.ai/api/v1",
            provider_name="openrouter",
        )
    elif p_norm in ("antigravity", "gemini", "google"):
        return AntigravityProvider(
            model_name=model or "gemini-2.5-pro",
            api_key=api_key,
        )
    elif p_norm in ("anthropic", "claude"):
        return AnthropicProvider(
            model_name=model or "claude-3-5-sonnet-20241022",
            api_key=api_key,
        )
    else:
        supported = ["agy", "antigravity", "ollama", "openai", "openrouter", "anthropic", "mock"]
        raise ValueError(f"Unknown provider '{provider_name}'. Supported providers: {', '.join(supported)}")
