---
description: Testing and logging standards for ai-camera (iOS + FastAPI) including trace id tracking and basic coverage expectations.
---

# Testing and Logging Standards (ai-camera)

## Testing

### iOS

- Unit test pure logic (guidance ranking/policy, pose template selection, throttling/state machine).
- Avoid brittle UI tests for logic that can be unit-tested.

### Backend (FastAPI)

- Add `pytest` tests for:
  - `GET /healthz`
  - `GET /v1/styles`
  - `POST /v1/guidance` (schema validation + basic behavior)
  - `WS /v1/guidance/ws` (connect, send, receive, disconnect)
- For anything auth-related, tests must cover unauthorized/expired token cases.

## Logging

### Principles

- Logs must be useful for debugging realtime issues (latency spikes, drops, retries, degrade mode).
- Never log raw frames, raw face/pose landmarks tied to identity, or secrets.

### Trace/Request IDs

- Backend should generate a request id / trace id for each request (and include in error responses).
- WebSocket messages should carry a `session_id` (client-generated) for correlation.

