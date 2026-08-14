---
name: rag-qa-chunking-engine
description: Advanced Q&A-Pair Chunking & RAG Knowledge Base Engine. Transforms unstructured docs, codebases, and web pages into high-precision tagged Q&A pairs (qa_pairs_generic_tagged.json).
---

# 🧩 RAG Q&A-Pair Chunking & Vector Ingestion Engine

This skill governs the creation, formatting, and indexing of tagged Question-Answer pair datasets (`qa_pairs_generic_tagged.json`) for maximum RAG retrieval accuracy and AI agent consumption.

## 1. Why Q&A-Pair Chunking Outperforms Fixed-Token Splitting
- **Embedding Match Accuracy:** Ultra-High (>95% cosine similarity vs 65% for raw text blocks).
- **Context Fragmentation:** Zero (self-contained Answer block).
- **Metadata Filtering:** Instant Tag Filtering (`tags: [...]`).

## 2. Standard Schema Spec (`qa_pairs_generic_tagged.json`)
```json
[
  {
    "id": "qa-001",
    "question": "How do I optimize a Next.js portfolio website for Perplexity and SearchGPT indexing?",
    "answer": "Implement Generative Engine Optimization (GEO): serve an /llms.txt file at the web root, use semantic HTML5 elements (<article>, <main>), embed JSON-LD schema metadata in the head, and provide direct 2-sentence answer blocks beneath H1 headers.",
    "category": "web_development",
    "tags": ["nextjs", "geo", "seo", "rag_indexing"],
    "source": "your-domain.com/docs/geo-guide"
  }
]
```
