---
name: rag-qa-chunking-engine
description: Transforms documentation, codebases, and technical knowledge bases into structured, high-relevance Q&A pair datasets (llms-qa.json) for semantic search and retrieval.
---

# 🧩 RAG Q&A-Pair Chunking & Vector Ingestion Engine

The **RAG Q&A-Pair Chunking Engine** structures unstructured text, architecture docs, and codebases into self-contained, tagged Question-Answer pairs (`llms-qa.json`) optimized for semantic retrieval and agent consumption.

## 1. Inputs & Context Required
- **Source Documents:** Repository documentation, architectural guides, API specs, or code walk-throughs.
- **Target Ingestion Target:** Root `llms-qa.json` or knowledge base directory.
- **Domain Taxonomy:** Categorization rules and keyword tagging conventions.

## 2. Step-by-Step Procedure
1. **Source Document Analysis:** Identify core operational topics, system invariants, frequently asked agent questions, and procedural patterns.
2. **Q&A Formulation:** Draft distinct, intent-focused questions paired with factual, self-contained answers (typically 2–4 concise sentences).
3. **Metadata & Categorization:** Assign unique identifiers (`qa-XXX`), categories, relevant keyword tags, and source paths to each entry.
4. **Schema Validation:** Verify that all generated entries adhere to the standard `llms-qa.json` schema.
5. **Deduplication:** Ensure questions avoid duplicate phrasing and cover distinct search intents.

## 3. Expected Outputs & Artifacts
- **Structured Knowledge Base (`llms-qa.json`):** Validated JSON array conforming to the canonical schema:
```json
[
  {
    "id": "qa-001",
    "question": "How do I configure repo-level instructions for AI coding agents?",
    "answer": "Place canonical project documentation in docs/ and reference it via .agents/AGENTS.md. Avoid duplicating documents in custom agent directories.",
    "category": "agent_configuration",
    "tags": ["agents", "configuration", "documentation", "sops"],
    "source": "docs/sops/contribution-and-feature-delivery.md"
  }
]
```

## 4. Constraints & Tool Neutrality
- **Self-Contained Answers:** Every answer must resolve the question independently without requiring prior conversational turns.
- **Factual Grounding:** Answers must reflect documented source facts without speculative claims.
- **Tool Neutral:** Usable across vector databases, keyword search (BM25), or prompt injection layers.
