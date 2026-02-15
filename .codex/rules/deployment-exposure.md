---
description: Deployment security guardrails for ai-camera: minimize public ports, manage secrets, and harden staging like production.
---

# Deployment Exposure & Secrets (Staging/Prod)

## Public Surface Area

- Treat staging/test as internet-facing. Apply production-grade hardening.
- MUST expose only one entrypoint to the internet (`80/443`) via reverse proxy/load balancer.
- MUST NOT publish host ports for internal services in staging/prod:
  - databases, caches
  - internal model services
  - internal FastAPI services (unless it is the single edge service)

## Reverse Proxy Requirements

- WebSocket should be same-origin where possible (e.g. `wss://<domain>/v1/guidance/ws` behind the edge).
- Avoid mobile clients depending on direct `:8000` style ports in production.

## Secrets & Defaults

- MUST NOT commit secrets, default credentials, or “placeholder secrets” that look real.
- In production, services MUST fail fast when required secrets/config are missing.

## CORS / Origins

- Production MUST NOT use `ALLOW_ORIGINS="*"` for admin or user-authenticated APIs.
- Origins should be explicit and environment-scoped.

