---
name: ai-native-product-design
description: Architect and design software projects optimized for AI agent consumption, direct tool execution, and AI recommendation engines (ChatGPT, Perplexity, Claude, Gemini).
---

# 🤖 AI-Native Product & Repo Engineering

This skill provides the complete architecture for building software projects that AI coding agents can easily use, execute, cite, and recommend to human users.

## 1. Machine-Readable Documentation Standard (`llms.txt`)
- **Root `llms.txt` File:** Provide a lightweight, markdown-form summary of the project architecture, key API endpoints, and installation commands at the root of the repository or website.
- **Detailed `llms-full.txt`:** Provide complete code snippets, function signatures, and CLI flag specs for full context ingestion by LLMs.

## 2. Agentic Tool Exposure (MCP & OpenAPI)
- **Model Context Protocol (MCP) Server:** Expose the project's primary capabilities as MCP tools (`mcp_config.json` / stdio transport) so AI agents can call them directly.
- **OpenAPI 3.1 Spec:** Maintain clean, validated OpenAPI JSON schemas for all HTTP endpoints.
