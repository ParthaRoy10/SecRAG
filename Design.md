# SecRAG Design Notes

## Goal
A cited security knowledge assistant (CVE, CWE, ATT&CK, OWASP) using
hybrid retrieval, with measured quality and prompt-injection defenses.

## Scope
- In scope: Q&A over public security data, evaluation suite, security layer, API + UI.
- Out of scope (for now): secure code review module (planned extension).

## Folders (added only when needed)
| Folder | Why it exists |
|--------|---------------|
| llm/   | Single entry point `generate(prompt) -> str`. Hides the provider
|        | (Gemini now, swappable later), and holds caching and retries. |

## Decision log
| Date | Decision | Reason |
|------|----------|--------|
| Day 1 | LLM behind `generate()` | Swap providers in one file; keep response parsing and caching in one place; allow a fake LLM in tests. |
| Day 1 | Gemini free tier as LLM | 8GB RAM / 4GB VRAM can't run a good local model. |
| Day 1 | Disk cache keyed by prompt + model + temperature | Avoid wasting quota; prevent stale results after config changes. |