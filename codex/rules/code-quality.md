---
description: Code quality standards for ai-camera (Swift + FastAPI): type safety, error handling, config hygiene, and avoiding silent failures.
---

# Code Quality Standards (ai-camera)

## Type Safety

### Swift

- Prefer strong types over `Any`/`NSDictionary`.
- Prefer `Codable` DTOs for network payloads.
- Avoid force unwrap (`!`) and forced casts (`as!`) in production paths.
- When working with realtime streams, make decoding failures explicit and observable (metrics/log).

### Python (FastAPI)

- Prefer Pydantic models at API boundaries.
- Keep `Any` limited to truly unstructured JSON blobs (e.g., debug fields) and isolate them in dedicated fields.
- Avoid “catch-all” exception handling that hides errors.

## Error Handling (No Silent Failures)

- No empty `catch` / `except` blocks.
- Network failures must be surfaced as actionable states:
  - iOS: show degraded mode UI, retry/backoff, allow user to continue shooting.
  - Backend: return clear error codes; avoid leaking internals.
- Timeouts are mandatory for outbound calls; do not rely on defaults.

## Configuration Hygiene (No Hardcoding)

- All configuration must be env-driven and documented in `.env.example`.
- No hardcoded URLs, keys, or secret tokens.
- In “prod-like” modes, fail fast when required secrets/config are missing.

## Performance Guardrails (Realtime Product)

- Avoid per-frame allocations and heavy work on the main thread (iOS).
- Throttle/debounce realtime guidance updates; avoid UI “jitter”.
- Backend must enforce rate limits and per-session backpressure (WebSocket).

