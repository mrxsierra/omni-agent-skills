---
name: ai-first-web-geo
description: Structures web applications and documentation for Generative Engine Optimization (GEO), RAG search indexing, and machine-readable context discovery.
---

# 🌐 AI-First Web Design & Generative Engine Optimization (GEO)

The **AI-First Web Design & GEO** skill structures web applications and documentation sites to optimize discovery, citation, and indexing by AI search engines, RAG systems, and autonomous coding agents.

## 1. Inputs & Context Required
- **Target Site / Documentation:** Web pages, documentation layouts, and routing structure.
- **Key Entity Data:** Site metadata, organization or author details, and software capabilities.
- **Target Distribution Channels:** RAG crawlers, AI search engines (Perplexity, SearchGPT), and direct LLM client requests.

## 2. Step-by-Step Procedure
1. **Semantic Content Layout:** Organize content with a single primary `<h1>`, followed immediately by a concise direct-answer summary block, and use semantic HTML5 elements (`<article>`, `<main>`, `<section>`).
2. **Structured Metadata Implementation:** Embed JSON-LD schemas (`SoftwareApplication`, `TechArticle`, `Organization`) in the document `<head>` to expose structured entity attributes.
3. **Machine-Readable Discovery (`llms.txt`):** Publish `/llms.txt` and `/llms-full.txt` at the web root containing clean, markdown-formatted summaries and documentation catalogs.
4. **Direct Markdown Endpoints:** Provide lightweight `.md` content mirrors or endpoints so agents can fetch clean content without running headless browser JavaScript runtimes.
5. **Validation & Verification:** Validate structured data using schema validator tools and verify that `/llms.txt` accurately resolves and references existing URLs.

## 3. Expected Outputs & Artifacts
- **Site Root `llms.txt`:** Manifest listing project summary, documentation links, and API references.
- **Semantic HTML Templates:** Markup incorporating JSON-LD schema blocks and structured summary sections.

## 4. Constraints & Tool Neutrality
- **Dual Audience Accessibility:** Ensure optimizations for AI indexing enhance or preserve human accessibility and standard SEO.
- **Tool Neutral:** Works across static site generators (Next.js, Astro, MkDocs, Hugo) and modern web frameworks.
