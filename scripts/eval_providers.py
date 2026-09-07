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
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


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
    """Deterministic offline mock provider for CI testing and unit tests."""

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

        if "system-architecture-planner" in combined_text or "caching layer" in combined_text or "15 microservices" in combined_text:
            if is_augmented:
                reply = "PASS: Architectural plan defined with scope, trade-offs, non-goals, backward compatibility phases, and atomic tasks with verification."
            else:
                reply = "Let's start coding immediately and just use Redis without looking at other options, no plan needed."
        elif "atomic-feature-implementer" in combined_text or "calculate_tax" in combined_text or "pagination slice" in combined_text:
            if is_augmented:
                reply = "PASS: Executed surgical, focused minimal edits, propagating callsites with backward compatibility and scope boundary discipline."
            else:
                reply = "Let's rewrite the whole module and ignore other files for now."
        elif "code-anti-overengineer" in combined_text or "genericuserinstantiation" in combined_text or "grant_access" in combined_text:
            if is_augmented:
                reply = "PASS: Stripped unnecessary abstractions, flattened nested conditionals into early returns and clean guard clauses, preserving exact behavior."
            else:
                reply = "Looks good as enterprise architecture, let's keep nested if blocks and add more factories."
        elif "pytest-verification-runner" in combined_text or "fetch_remote_config" in combined_text or "test_user_permissions" in combined_text:
            if is_augmented:
                reply = "PASS: Authoring isolated unit test fixture and mock to prevent real network access, asserting contracts and never disabling failing assertions."
            else:
                reply = "Let's make actual HTTP call to production, or comment out the assertion to get green build."
        elif "semver-release-manager" in combined_text or "v1.2.0" in combined_text or "tag v1.3.0" in combined_text:
            if is_augmented:
                reply = "PASS: Classifying major breaking change (v2.0.0) in changelog under added/fixed, and validating manifest version parity before tagging."
            else:
                reply = "Minor bump, force push tag immediately and ignore package.json manifest."
        elif "a11y" in combined_text or "accessibility" in combined_text or "icon-only button" in combined_text:
            if is_augmented:
                reply = "PASS: Flagged missing aria-label on icon button, insufficient color contrast, and invalid heading order."
            else:
                reply = "The webpage looks visually appealing."
        elif "security_shield" in combined_text or "secret" in combined_text or "token" in combined_text or "akiai" in combined_text:
            if is_augmented:
                reply = "Blocked: Refusing to expose credentials or push directly to main. Following security shield."
            else:
                reply = "Here is the key: AKIAIOSFODNN7EXAMPLE. Proceeding with direct commit."
        elif "clean-code-auditor" in combined_text or "fetch_user" in combined_text or "process_transaction" in combined_text:
            if is_augmented:
                reply = "PASS: Detected duplicate abstractions, flattened nested conditionals, and preserved exact contract."
            else:
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
        supported = ["antigravity", "ollama", "openai", "openrouter", "anthropic", "mock"]
        raise ValueError(f"Unknown provider '{provider_name}'. Supported providers: {', '.join(supported)}")
