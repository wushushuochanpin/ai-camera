---
name: release-hardening
description: Plan and implement internet-facing release hardening for ai-camera: minimize public ports, enforce single edge entrypoint (80/443), proxy WebSocket, verify Sign in with Apple server-side, and manage secrets correctly.
---

# Release Hardening (Ports + Auth + Secrets)

## Scope

Use this skill when preparing **staging/prod** for internet-facing use (or when touching `docker-compose`, reverse proxy/LB, WebSocket, auth/login, secrets).

Treat staging as public: anything reachable can be scanned and abused.

## Goals

- Reduce public ports to a single edge entrypoint (`80/443`)
- WebSocket is reachable via the same public domain (no direct `:8000` dependencies in browsers)
- Auth is server-verifiable (Sign in with Apple verified server-side; no token mint endpoints)
- Secrets are never committed; prod fails fast when required secrets are missing

## Workflow

### 1) Confirm Target Topology

Pick one (do not mix casually):

- **Edge reverse proxy / load balancer** in front (recommended): clients only see `https://<domain>`.
- **Direct port exposure** (dev-only): acceptable only on localhost or behind strict IP allowlist/VPN.

### 2) Port Hardening Checklist

Goal: close or firewall these from the public internet (examples):

- Databases (Postgres/MySQL), Redis
- Internal model services
- Internal FastAPI services (if they are not the edge)

Only keep:

- `80/443` (edge entrypoint)

### 3) WebSocket Proxying

- Ensure WebSocket works through the public domain:
  - Example: `wss://<domain>/v1/guidance/ws`
- Edge proxy must forward Upgrade headers correctly.

### 4) Auth Hardening Checklist

User auth (mobile):

- Sign in with Apple must be verified server-side.
- Backend issues its own session/token.
- No unauthenticated token issuance endpoints.
- Rate limit login and sensitive endpoints.

Admin auth (admin console):

- Prefer SSO/OIDC + 2FA.
- Add audit logging for admin actions (disable user, force logout, entitlement changes, config changes).

### 5) Verification (Minimum)

- Publicly reachable ports: only `80/443`
- WebSocket works via the domain path (not a raw port)
- CORS origins are explicit (no `*` for authenticated/admin APIs)
- Missing required secrets in prod causes startup failure (fail fast)

