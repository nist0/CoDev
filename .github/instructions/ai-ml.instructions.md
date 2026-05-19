---
name: "AI/ML Engineering"
description: "Always-on responsible-AI defaults for LLM integration and RAG pipeline code: PII guards, no hardcoded model names, output sanitisation, and content-filter requirements."

## applyTo: "**/*llm*.{py,ts,cs,js},**/*rag*.{py,ts,cs,js},**/*openai*.{py,ts,cs,js},**/*anthropic*.{py,ts,cs,js},**/*langchain*.{py,ts,cs,js},**/*embedding*.{py,ts,cs,js},**/*vector_store*.{py,ts,cs,js},**/*chat_completion*.{py,ts,cs,js}"

# AI/ML Engineering

> Boundary: This instruction governs LLM integration and RAG pipeline code. Do not duplicate general API security rules here; those are covered by `security.instructions.md`.

## Required rules

- **No hardcoded model names**: read model identifiers from configuration (environment variables, options pattern). Hardcoded model strings make A/B testing, cost control, and emergency model swaps impossible without a code deployment.

- **PII must not enter prompts**: sanitise or pseudonymise user data before constructing any prompt. Log prompts at DEBUG level only, never INFO or above, and never include full user-submitted text in production logs.

- **Output sanitisation**: treat every LLM response as untrusted input. Validate structured outputs against a schema (Pydantic, JSON Schema, typed deserialiser) before passing them to callers. Never pass LLM output to `eval()`, `exec()`, shell commands, or dynamic SQL.

- **Content filter required**: integrate a content safety layer (e.g., Azure AI Content Safety, OpenAI moderation endpoint, a custom classifier) on both user input and model output for any user-facing feature.

- **System prompt always present**: every LLM call must include a system prompt that sets role, output format, and safety constraints. Omitting the system prompt produces unpredictable behaviour in production.

- **Secrets via environment only**: API keys, endpoint URLs, and organisation IDs must come from environment variables or a secrets manager -- never from source code, committed config files, or default argument values.

- **Token budget enforcement**: set `max_tokens` (or equivalent) on every completion call. No unbounded completions.

- **Retry with backoff on rate limits**: handle `429` and `5xx` responses with exponential backoff and jitter. Log retry attempts and surface cost/quota metrics.

## Procedure

- Follow end-to-end implementation patterns in `.github/skills/llm-integration/SKILL.md` for LLM call patterns.

- Follow end-to-end pipeline patterns in `.github/skills/rag-patterns/SKILL.md` for retrieval-augmented generation.
