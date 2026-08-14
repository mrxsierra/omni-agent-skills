---
name: ai-first-web-geo
description: Generative Engine Optimization (GEO) & AI-First Web Design. Build websites optimized for RAG crawlers, Perplexity/SearchGPT indexing, and AI agent consumption.
---

# 🌐 AI-First Web Design & Generative Engine Optimization (GEO)

This skill governs the design and structure of web applications and portfolio sites to maximize indexing, citation rates, and content consumption by AI search engines (Perplexity, SearchGPT, Gemini, Claude).

## 1. Structural Markup & Semantic Ingestion
- **Semantic HTML5:** Use clean `<main>`, `<article>`, `<section>`, `<header>`, and `<table>` elements. Avoid unsemantic `div`-soup.
- **Direct Answer Summaries:** Include a 2-sentence summary block directly under the primary `<h1>` title to provide immediate context for RAG crawlers.
- **JSON-LD Schema Metadata:** Embed structured JSON-LD schemas (`SoftwareApplication`, `TechArticle`, `Person`) in the `<head>` section.

## 2. Machine-Readable Content Mirroring
- **Web-Root `/llms.txt`:** Expose `/llms.txt` and `/llms-full.txt` at the root of the site containing raw markdown text of all major projects and posts.
- **Markdown Endpoints:** Provide clean, un-rendered `.md` URLs alongside HTML pages so AI agents can fetch lightweight text directly without running heavy JS runtimes.
