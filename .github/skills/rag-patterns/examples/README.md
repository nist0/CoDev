# rag-patterns skill -- examples

## Worked example 1: Basic RAG pipeline (Python + pgvector)

**User request**: "build a RAG pipeline that answers questions from my document store using pgvector"

**Expected routing**: capability `code-analysis`, domain `ai-ml-engineering`, agent `Architect`, skill `rag-patterns`

### Result: ingestion + retrieval pipeline

**Ingestion (one-time / incremental):**

```python
import os
import asyncpg
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-small")

async def ingest_document(
    conn: asyncpg.Connection,
    doc_id: str,
    content: str,
    source_url: str,
    chunk_size: int = 400,
    overlap: int = 80,
) -> None:
    # Overlapping chunks -- boundary context is preserved
    chunks = [
        content[i : i + chunk_size]
        for i in range(0, len(content), chunk_size - overlap)
    ]
    # Batch embeddings -- one API call per document, not per chunk
    response = await client.embeddings.create(input=chunks, model=EMBED_MODEL)
    embeddings = [item.embedding for item in response.data]
    await conn.executemany(
        """
        INSERT INTO documents (doc_id, chunk_index, content, embedding, metadata)
        VALUES ($1, $2, $3, $4::vector, $5)
        ON CONFLICT (doc_id, chunk_index) DO UPDATE
          SET content = EXCLUDED.content,
              embedding = EXCLUDED.embedding
        """,
        [
            (doc_id, i, chunk, emb, {"source": source_url, "chunk": i})
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
        ],
    )
```

**Retrieval + generation:**

```python
async def ask(conn: asyncpg.Connection, question: str, top_k: int = 4) -> str:
    q_emb = (
        await client.embeddings.create(input=[question], model=EMBED_MODEL)
    ).data[0].embedding

    rows = await conn.fetch(
        """
        SELECT content, metadata
        FROM documents
        ORDER BY embedding <=> $1::vector
        LIMIT $2
        """,
        q_emb, top_k,
    )

    context = "\n\n".join(
        f"[{r['metadata']['source']}]\n{r['content']}" for r in rows
    )

    response = await client.chat.completions.create(
        model=os.environ.get("CHAT_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the question using only the provided context. "
                    "If the answer is not in the context, reply: "
                    "'I could not find this in the available documents.'"
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
        max_tokens=512,
    )
    return response.choices[0].message.content
```

**Why each rule exists**:

- Overlapping chunks (`chunk_size - overlap`) prevent context loss at boundaries.

- Batch embedding call amortises API latency across all chunks.

- `ON CONFLICT ... DO UPDATE` enables incremental upserts without full re-index.

- Model names come from environment variables -- never hardcoded.

- System prompt explicitly instructs the model to stay grounded and provides a fallback phrase for out-of-context questions.

---

## Worked example 2: Hybrid retrieval with re-ranking

**User request**: "improve my RAG pipeline recall -- currently missing exact product code matches"

```python
import os
import asyncpg
from openai import AsyncOpenAI
from sentence_transformers import CrossEncoder  # pip install sentence-transformers

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-small")
_reranker = CrossEncoder(os.environ.get("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"))

async def hybrid_search_with_rerank(
    conn: asyncpg.Connection,
    question: str,
    candidate_k: int = 20,
    final_k: int = 4,
) -> list[str]:
    q_emb = (
        await client.embeddings.create(input=[question], model=EMBED_MODEL)
    ).data[0].embedding

    # Pull more candidates than needed for re-ranking
    rows = await conn.fetch(
        """
        SELECT id, content,
               (1 - (embedding <=> $1::vector))           AS dense_score,
               ts_rank(fts_index, plainto_tsquery($2))    AS sparse_score
        FROM documents
        ORDER BY 0.6 * (1 - (embedding <=> $1::vector))
               + 0.4 * ts_rank(fts_index, plainto_tsquery($2)) DESC
        LIMIT $3
        """,
        q_emb, question, candidate_k,
    )
    candidates = [r["content"] for r in rows]

    # Cross-encoder re-ranking -- far more accurate than bi-encoder alone
    scores = _reranker.predict([(question, c) for c in candidates])
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [text for text, _ in ranked[:final_k]]
```

**Why hybrid + re-ranking**:

- Dense retrieval misses exact keyword matches (product codes like `SKU-4821`).

- Sparse (BM25 / `ts_rank`) retrieval misses paraphrase-level matches.

- Hybrid scoring fuses both; `0.6 dense + 0.4 sparse` is a reasonable starting weight -- tune on your eval set.

- The cross-encoder re-ranker reads both query and candidate together, giving much higher precision than the bi-encoder similarity used during retrieval.

---

## Anti-patterns quick reference

| Anti-pattern | Risk | Fix |
| --- | --- | --- |
| One embedding model at ingest, another at query | Nonsensical similarity scores | Pin model in config, re-index on change |
| No chunk overlap | Context at boundaries lost | 10--20% overlap |
| Dense-only retrieval | Exact-term misses (codes, names) | Hybrid dense + sparse |
| Full context window filled | No token budget for the answer | Reserve completion tokens |
| No grounding instruction | Model hallucinates plausibly | Always instruct "answer only from context" |

---

## Expected routing shape

- Domain: `ai-ml-engineering`

- Capability: `code-analysis`

- Agent: `Architect`

- Skills invoked: `rag-patterns`, `llm-integration`
