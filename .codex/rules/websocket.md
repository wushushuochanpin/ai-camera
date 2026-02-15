---
description: WebSocket real-time communication standards for ai-camera (mobile + backend) including lifecycle, reconnection, and backpressure.
---

# WebSocket Standards (ai-camera)

## Critical Constraints

- MUST manage connection lifecycle: connect on session start, disconnect on session end; no orphan tasks.
- MUST implement reconnection with backoff and jitter (mobile networks are unstable).
- MUST deduplicate / ignore stale messages where applicable (avoid UI “rewind”).
- MUST apply backpressure: client must not outpace server; server must not queue unbounded.
- WebSocket messages should be schema-versioned (or at least backward-compatible) to support app upgrades.

## iOS Client Notes

- Prefer one `URLSessionWebSocketTask` per “guidance session” (not per view re-render).
- Avoid doing heavy JSON parsing on the main thread.

## Backend Notes

- Enforce per-connection rate limits (messages/sec, bytes/sec).
- Validate payloads strictly; reject unknown fields if they indicate client drift.
- Ensure disconnect cleanup is reliable (no leaking session state).

