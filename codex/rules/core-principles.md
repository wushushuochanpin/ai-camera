---
description: Core development principles for ai-camera (iOS + FastAPI) including file size constraints, module boundaries, and naming conventions.
---

# Core Development Principles (ai-camera)

## Role & Context

You are a senior engineer/architect working on **ai-camera**:

- iOS app (Swift, AVFoundation, Vision/Core ML as applicable)
- Backend (Python/FastAPI; HTTP + WebSocket for real-time guidance)
- Optional: Web Admin Console (internal use)

Your goal is to ship a reliable, privacy-safe real-time camera product with clear module boundaries.

## Critical Rules (Must Follow)

### 1) Keep Files Small and Single-Purpose

- **File size guideline (not a hard cap):** Prefer keeping files under **300 lines**.
- If a file grows beyond ~300 lines, propose a split unless it is clearly **single-purpose, well-decoupled, and self-contained**.
- Avoid “god” modules that mix UI, business logic, networking, and persistence.

### 2) Enforce Boundaries (No Layer Leaks)

- UI should not directly do networking, persistence, or cloud protocol handling.
- Domain/policy logic should not depend on UI frameworks.
- Backend route handlers should not contain heavy business logic; push into services.

### 3) Privacy and Safety First

- Camera frames, pose keypoints, user identifiers, device identifiers are sensitive.
- Do not log raw frames or unredacted PII.
- Prefer data minimization: send the smallest/lowest-fidelity payload that achieves the desired UX.

## Suggested Project Structure (Guidance)

### iOS (Swift)

Keep strong separation between:

- **UI** (SwiftUI/UIKit views, view models)
- **Camera pipeline** (AVCaptureSession setup, frame capture, preview rendering)
- **Guidance** (policy/ranking, suggestion state machine)
- **Networking** (cloud requests, WebSocket streaming, retry/backoff)
- **Models** (request/response DTOs, style/pose catalogs)

If you need a concrete shape, prefer feature-first modules:

```
AICamera/
  App/
  Features/
    Camera/
    Review/
    Settings/
  Services/
    GuidanceClient/
    AudioTTS/
  Core/
    Models/
    Utils/
```

### Backend (FastAPI)

Prefer:

```
server/app/
  main.py            # App wiring, middleware, route registration
  api/               # Route handlers (thin)
  schemas/           # Pydantic models (DTOs)
  services/          # Business logic / policies
  utils/             # Logging, trace id, helpers
```

## Naming Conventions

### Swift

- Types/Protocols/Enums: `PascalCase`
- Variables/Functions: `camelCase`
- Avoid `Any`/force unwrap (`!`) except at strict boundaries with justification.

### Python

- Modules/vars/functions: `snake_case`
- Classes: `PascalCase`
- Avoid broad `except Exception: pass` and “swallowing” errors.

