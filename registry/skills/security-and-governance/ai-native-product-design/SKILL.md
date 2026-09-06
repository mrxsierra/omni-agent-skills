---
name: ai-native-product-design
description: Architects software repositories and products for direct AI agent integration, tool exposure via protocols (MCP, OpenAPI), and structured discoverability.
---

# 🤖 AI-Native Product & Repo Engineering

The **AI-Native Product Design** skill structures software repositories, libraries, and web services for seamless discovery, consumption, and execution by AI agents and developer tools.

## 1. Inputs & Context Required
- **Target Repository / Service:** Codebase architecture, public API endpoints, CLI entry points, and documentation.
- **Protocol Targets:** Model Context Protocol (MCP), OpenAPI 3.1, or agentic CLI interfaces.
- **Audience Scope:** AI coding agents, autonomous workflows, and human developers.

## 2. Step-by-Step Procedure
1. **Discoverability Layer Setup:** Place machine-readable index files (`llms.txt`, `registry.json`, `llms-qa.json`) at the repository root describing architecture, tools, and usage.
2. **Tool Contract Definition:** Define tool inputs, parameter schemas, and return structures with unambiguous descriptions and validation rules.
3. **Protocol Interface Scaffolding:** Implement MCP servers (`stdio` or SSE transports) or publish validated OpenAPI 3.1 specifications.
4. **Agent Guardrails & Sandboxing:** Ensure actions that modify data or run external commands have safety flags, dry-run options, and explicit permission boundaries.
5. **Self-Describing Examples:** Include runnable examples demonstrating typical usage and error handling.

## 3. Expected Outputs & Artifacts
- **Machine-Readable Discovery Assets:** Root `llms.txt` and registry descriptors.
- **Tool Protocol Specifications:** Validated MCP server definitions or OpenAPI specs.
- **Documentation & Examples:** Clear guide documenting agentic tool calling and parameters.

## 4. Constraints & Tool Neutrality
- **Least Privilege:** Enforce minimal operational scopes; do not expose destructive actions without confirmation guards.
- **Tool Neutral:** Works across MCP clients, REST callers, and standard command-line tools.
