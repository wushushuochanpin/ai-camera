---
description: Project-specific standards for ai-camera including env var hygiene, API versioning, and commit message conventions.
---

# Project-Specific Standards (ai-camera)

## Environment Variable Management

- All configuration must be documented in `.env.example` with short comments.
- Never hardcode sensitive information (API keys, secrets, credentials) in code or committed configs.
- Prefer “secure-by-default” behavior for prod-like modes (fail fast when required env vars are missing).

## API Version Management

- Keep public APIs versioned (current pattern: `/v1/*`).
- Prefer backward-compatible changes; if breaking is needed, add `/v2/*` rather than changing `/v1` in-place.

## Git Commit Standards

- Commit message format: `type(scope): subject`
  - `type`: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
  - `scope`: short module name (e.g., `ios`, `server`, `prd`, `admin`)
  - `subject`: imperative, concise

Examples:

```text
feat(server): add websocket guidance rate limiting
fix(ios): avoid main-thread JSON decoding in guidance stream
docs(prd): clarify v1 out-of-scope night long-exposure
```

