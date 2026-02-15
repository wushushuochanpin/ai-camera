---
description: Auth boundary guardrails for ai-camera: token issuance must be protected, public endpoints must not leak data, and Sign in with Apple must be server-verifiable.
---

# Auth Boundaries & Public APIs (ai-camera)

## Token Issuance / Sessions

- MUST NOT expose an unauthenticated “token mint” endpoint to the public internet.
- Auth decisions MUST be made from **verified server-side identity** (JWT/session). Never trust `userId`/`role`/`plan` from request bodies/queries.
- For mobile clients, prefer short-lived access tokens + refresh tokens (or server sessions) with revocation support.

## Sign in with Apple (User Login)

- Client-side “Apple login success” is not sufficient.
- Backend MUST verify Apple identity server-side (e.g., validate `id_token` signature/audience/issuer, check nonce, handle key rotation).
- Backend issues its own session/token; app uses that for subsequent APIs.

## Admin Console (Backend Management UI)

- Admin endpoints must require admin auth (SSO/OIDC preferred) + strict RBAC.
- MUST have audit logs for admin actions (disable user, force logout, entitlement changes, config changes).
- Avoid sharing user-auth tokens with admin-auth tokens.

## Public Routes

- Public endpoints MUST be limited to truly public operations (login initiation/exchange, health checks).
- MUST NOT expose:
  - user lists or account enumeration
  - config secrets (provider keys, internal URLs)
  - cross-user data via “default user” fallbacks
- Login endpoints MUST have brute-force protection:
  - rate limiting
  - minimal error detail (avoid user enumeration)
  - audit logging

