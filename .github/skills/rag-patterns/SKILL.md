---
name: rag-patterns
description: RAG (Retrieval-Augmented Generation) pipeline patterns -- chunking strategies, embedding model selection, vector store operations, dense/sparse/hybrid retrieval, context-window assembly, and hallucination mitigation.
argument-hint: "[language] [vector-store] [retrieval-mode]"
user-invocable: true

disable-model-invocation: false
---

# RAG Patterns Skill

## 1) Document ingestion and chunking

- Choose chunk size based on the embedding model's token limit and your retrieval granularity needs; 256--512 tokens is a common default for sentence-level recall.

- Use overlapping chunks (10--20% overlap) to avoid losing context that spans chunk boundaries.

- Preserve document metadata (source URL, section title, page number, timestamp) alongside each chunk -- attach it to the vector store record, not just the raw text.

- Re-chunk when the embedding model or chunk strategy changes; stale embeddings from a different model cause silent quality regressions.

- For structured documents (code, tables, HTML), use structure-aware splitting rather than naive character/token splitting.

## 2) Embedding model selection

- Use the same embedding model at ingestion time and at query time -- any mismatch produces nonsensical similarity scores.

- Prefer models with demonstrated performance on your content domain (code retrieval vs. prose retrieval vs. multilingual).

- Pin the embedding model version in your configuration; upstream model updates can silently change the vector space and require a full re-index.

- Batch embedding calls to reduce API latency and cost; most providers support batch sizes of 100--2048.

## 3) Vector store operations

- Index vectors with appropriate metadata filters so retrieval queries can scope by document type, date range, or tenant without post-filtering the full result set.

- Choose an index type matched to your scale: HNSW for approximate nearest-neighbour at million+ record scale; exact search for smaller corpora.

- For multi-tenant systems, enforce tenant isolation at the vector store level (separate namespaces or collections), not in application code.

- Implement incremental upserts so updated documents replace stale embeddings without requiring a full re-index.

## 4) Retrieval strategies

- **Dense retrieval**: semantic similarity using vector cosine/dot-product search. Best for paraphrase-level matching.

- **Sparse retrieval**: BM25/keyword overlap. Best for exact term matching (product codes, proper nouns, technical identifiers).

- **Hybrid retrieval**: combine dense + sparse scores (reciprocal rank fusion is a robust default). Hybrid consistently outperforms either approach alone on mixed-content corpora.

- **Re-ranking**: apply a cross-encoder re-ranker on the top-K candidates before context assembly. Adds latency but significantly improves precision.

- Return more candidates than needed (top-20) before applying re-ranking, then trim to top-5 for context assembly.

## 5) Context-window assembly

- Sort retrieved chunks by relevance score, then assemble them into the prompt context respecting the token budget.

- Include the source reference (URL, document ID) alongside each chunk in the prompt so the model can cite sources.

- Deduplicate chunks that share substantial overlap before assembly.

- Structure the prompt clearly: system instructions first, then retrieved context with labels, then the user question.

- Reserve enough tokens for a complete answer; do not fill the context window entirely with retrieved text.

## 6) Hallucination mitigation

- Instruct the model to answer only from the provided context; include a fallback instruction: "If the answer is not in the provided context, say so explicitly."

- Implement a faithfulness check: verify that key claims in the answer are grounded in the retrieved context (LLM-as-judge or NLI classifier).

- Log retrieved chunk IDs alongside the response so offline evaluation can correlate answers to sources.

- Monitor the rate of "I don't know" responses -- a sudden increase often signals a retrieval quality regression.

## 7) Evaluation

- Measure retrieval quality with Recall@K and Mean Reciprocal Rank (MRR) on a labelled question-answer test set.

- Measure generation quality with faithfulness (grounded in context?) and answer relevance (answers the question?) using RAGAS or a comparable eval framework.

- Run evaluation on every embedding model upgrade or chunking strategy change before deploying to production.

## Canonical Python pipeline (hybrid retrieval + pgvector)

```python
import os
import asyncpg
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-small")

async def embed(text: str) -> list[float]:
    r = await client.embeddings.create(input=text, model=EMBED_MODEL)
    return r.data[0].embedding

async def hybrid_search(
    conn: asyncpg.Connection,
    query: str,
    top_k: int = 5,
) -> list[dict]:
    q_vec = await embed(query)
    rows = await conn.fetch(
        """
        SELECT id, content, metadata,
               (1 - (embedding <=> $1::vector)) AS dense_score,
               ts_rank(to_tsvector('english', content),
                       plainto_tsquery('english', $2)) AS sparse_score
        FROM documents
        ORDER BY 0.7 * dense_score + 0.3 * sparse_score DESC
        LIMIT $3
        """,
        q_vec, query, top_k,
    )
    return [dict(r) for r in rows]

async def answer(conn: asyncpg.Connection, question: str) -> str:
    chunks = await hybrid_search(conn, question)
    context = "\n\n".join(
        f"[{c['metadata']['source']}]\n{c['content']}" for c in chunks
    )
    completion = await client.chat.completions.create(
        model=os.environ.get("CHAT_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided context. "
                    "If the answer is not in the context, say so explicitly."
                ),
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        max_tokens=512,
    )
    return completion.choices[0].message.content
```

## Anti-patterns

| Anti-pattern | Risk | Fix |
| --- | --- | --- |
| Different embedding models at ingest vs. query | Wrong similarity scores, poor recall | Pin model in config; re-index on change |
| No chunk overlap | Context split across boundaries, recall gap | 10--20% overlap |
| Dense-only retrieval | Poor recall on exact terms (product IDs, codes) | Hybrid dense + sparse (RRF) |
| Filling the entire context window with chunks | No room for the answer | Reserve token budget for completion |
| No faithfulness check | Hallucinated answers presented as fact | Implement LLM-as-judge or NLI faithfulness check |
| Re-indexing avoided on model update | Silent quality regression | Always re-index after embedding model change |
