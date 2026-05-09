# llm-integration skill -- examples

## Worked example 1: Streaming chat completion (Python + OpenAI)

**User request**: "implement a streaming chat endpoint in my FastAPI app using OpenAI"

**Expected routing**: capability `code-analysis`, domain `ai-ml-engineering`, agent `Architect`, skill `llm-integration`

### Result: streaming endpoint

```python
import os
from collections.abc import AsyncIterator
from openai import AsyncOpenAI
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()
_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

async def _token_stream(user_message: str) -> AsyncIterator[str]:
    stream = await _client.chat.completions.create(
        model=os.environ.get("CHAT_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        stream=True,
        max_tokens=1024,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta

@app.post("/chat/stream")
async def chat_stream(body: dict) -> StreamingResponse:
    return StreamingResponse(
        _token_stream(body["message"]),
        media_type="text/event-stream",
    )
```

**Why each rule exists**:

- Model read from `os.environ` -- never hardcoded.
- `stream=True` returns tokens as they arrive, reducing perceived latency.
- `max_tokens` bounds cost and prevents runaway completions.
- `system` prompt is always present.

---

## Worked example 2: Structured JSON output with schema validation (Python + Pydantic)

**User request**: "call GPT-4o and get back a structured JSON object validated against a schema"

```python
import os
from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError
import logging

log = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

class ProductSuggestion(BaseModel):
    name: str
    price_usd: float
    reasons: list[str]

async def suggest_product(category: str) -> ProductSuggestion | None:
    try:
        response = await client.beta.chat.completions.parse(
            model=os.environ.get("CHAT_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a product recommender. "
                        "Return a single JSON object matching the schema."
                    ),
                },
                {"role": "user", "content": f"Suggest a product in: {category}"},
            ],
            response_format=ProductSuggestion,
            max_tokens=256,
        )
        return response.choices[0].message.parsed
    except ValidationError as exc:
        log.warning("LLM returned schema-invalid JSON", extra={"error": str(exc)})
        return None
```

**Why each rule exists**:

- `response_format=ProductSuggestion` instructs the model to use JSON mode and validates the response against the Pydantic model.
- `ValidationError` is caught explicitly -- schema drift is a recoverable error, not a crash.
- A `None` return is the typed error path; callers handle the absence explicitly.
- Log entry uses structured fields (not f-string interpolation) for machine-parseable observability.

---

## Anti-patterns quick reference

| Anti-pattern | Risk | Fix |
| --- | --- | --- |
| `model="gpt-4o"` hardcoded | Cannot swap models without code change | `os.environ.get("CHAT_MODEL", "gpt-4o-mini")` |
| No `max_tokens` limit | Runaway completion cost | Always set `max_tokens` |
| `json.loads(response.content)` without schema | Runtime crash on schema drift | Use `response_format=MyModel` + Pydantic |
| No retry on 429 | Brittle under load spikes | Wrap with tenacity `@retry(retry=retry_if_exception_type(RateLimitError))` |
| System prompt omitted | Unpredictable behaviour | Always set a system prompt |

---

## Expected routing shape

- Domain: `ai-ml-engineering`
- Capability: `code-analysis`
- Agent: `Architect`
- Skills invoked: `llm-integration`
