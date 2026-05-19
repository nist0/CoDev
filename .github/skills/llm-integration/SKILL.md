---
name: llm-integration
description: LLM integration patterns -- provider abstraction, streaming, retries, rate limiting, token counting, structured output, and prompt-template discipline for production AI features.
argument-hint: "[provider] [language] [use-case]"
user-invocable: true

disable-model-invocation: false
---

# LLM Integration Skill

## 1) Provider abstraction

- Hide the provider SDK behind an interface (`ICompletionClient`, `CompletionClient`) so switching providers requires no downstream changes.

- Accept the model name and base URL via configuration (environment variables or options pattern) -- never hardcode model strings in application code.

- Validate configuration at startup; fail fast with a clear error rather than failing at first inference call.

- Support at least one fallback provider or model tier for availability; document the fallback chain.

## 2) Streaming completions

- Prefer streaming (`stream=True` / `IAsyncEnumerable`) for user-facing responses to reduce perceived latency.

- Buffer partial tokens before flushing to the transport layer; avoid sending a network write per token.

- Handle stream interruption (connection reset, timeout) gracefully: surface a partial result with a clear truncation indicator rather than an unhandled exception.

- Always cancel the upstream stream when the downstream client disconnects (pass `CancellationToken` through the entire call chain).

## 3) Retries and rate limiting

- Use exponential backoff with jitter on 429 (rate-limit) and 5xx responses; respect the `Retry-After` header when present.

- Set a hard deadline (outer timeout) separate from the per-attempt timeout to bound total wall time.

- Expose retry budget metrics (attempt count, total delay) in structured logs for observability.

- Never retry on 400 (invalid request) or 401 (auth failure) -- these are programmer errors, not transient failures.

## 4) Token counting and context management

- Count tokens before sending to avoid silent truncation; use the provider's tokenizer or a compatible local library (`tiktoken`, `tokenizers`).

- Reserve a fixed budget for the system prompt, a variable budget for retrieved context, and a minimum budget for the completion.

- Log the prompt token count, completion token count, and total cost estimate per request for cost monitoring.

- Trim or summarise conversation history when approaching the context window limit rather than silently dropping the oldest turns.

## 5) Structured output (JSON mode)

- Use provider JSON mode (`response_format={"type": "json_object"}`) or tool/function calling to guarantee parseable output.

- Always validate the parsed object against a schema (Pydantic model, JSON Schema, `System.Text.Json` source generator) before returning it to callers.

- Include a fallback parse path for when the model returns valid JSON that does not match the schema (log, alert, return a typed error).

- Never `eval()` or dynamically execute LLM output.

## 6) Prompt template discipline

- Separate prompt templates from application code; store them as versioned files or configuration entries, not inline strings.

- Parameterise templates with typed inputs; validate inputs before interpolation to prevent prompt injection.

- Include a system prompt that sets role, output format, and any safety constraints -- never omit the system prompt in production.

- Log the rendered prompt (sanitised of PII) at DEBUG level so issues are reproducible.

## 7) Observability

- Emit a structured log entry per LLM call: provider, model, input tokens, output tokens, latency ms, status (success/rate-limited/error).

- Use correlation IDs that span from the user request through every LLM call and downstream tool call.

- Alert on p99 latency and error rate thresholds; track cost per capability area.

## Canonical Python pattern (streaming + structured output)

```python
import os
from openai import AsyncOpenAI
from pydantic import BaseModel

client = AsyncOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL"),
)

class SummaryOutput(BaseModel):
    headline: str
    bullets: list[str]

async def summarise(text: str, model: str = "gpt-4o-mini") -> SummaryOutput:
    response = await client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a summarisation assistant. Return JSON only.",
            },
            {"role": "user", "content": f"Summarise:\n\n{text}"},
        ],
        response_format=SummaryOutput,
        max_tokens=512,
    )
    return response.choices[0].message.parsed
```

## Canonical .NET pattern (streaming with CancellationToken)

```csharp
public async IAsyncEnumerable<string> StreamChatAsync(
    string userMessage,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    var options = new ChatCompletionOptions { MaxOutputTokenCount = 1024 };
    await foreach (var update in _client.CompleteChatStreamingAsync(
        [new UserChatMessage(userMessage)], options, ct))
    {
        foreach (var part in update.ContentUpdate)
            yield return part.Text;
    }
}
```

## Anti-patterns

| Anti-pattern | Risk | Fix |
| --- | --- | --- |
| Hardcoded model name (`"gpt-4o"`) | Cannot switch models without code change | Read from configuration |
| No retry on 429 | Brittle under load | Exponential backoff with jitter |
| `response.content` used directly without validation | Schema drift causes runtime errors | Parse against Pydantic/JSON Schema |
| System prompt omitted | Unpredictable model behaviour | Always include a system prompt |
| Full conversation history sent every turn | Context window exhaustion + cost explosion | Trim/summarise history |
| LLM output passed to `eval()` or `exec()` | Remote code execution | Never execute model output |
