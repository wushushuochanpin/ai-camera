---
name: file-module-split
description: How to split oversized files and modules in ai-camera (iOS + FastAPI). Use when a file exceeds 500–1000 lines, when refactoring God files, or when planning module boundaries.
---

# How to Split Oversized Files and Modules

## Overview

This repo prefers files under ~300 lines (see `codex/rules/core-principles.md`). Mandatory split applies when a file is not single-purpose, well-decoupled, and self-contained. This skill describes when to warn (>500 lines), when to refuse or block (>1000 lines), and practical split strategies for common “god” modules in **iOS** and **FastAPI**.

## Thresholds

| Lines | Severity | Action |
|-------|----------|--------|
| >1000 | Critical | Must split before merging; refuse to add more to the file |
| >500 | Warning | Plan split; prefer splitting before adding large features |
| ≤300 | Target | Per core-principles; exception: single-purpose / decoupled / self-contained may exceed |

If a file over 300 lines is single-purpose, well-decoupled, and self-contained (e.g. one state machine, one cohesive hook), splitting is not mandatory but still preferred when feasible.

## iOS (Swift) Split Playbooks

### 1. Camera UI + Camera Session 混在一起（God file）

**Goal:** UI 文件保持可读；相机会话、帧处理、实时指导互不耦合。

**Steps:**

1. Extract camera session wiring into a controller (e.g. `CameraSessionController`): `AVCaptureSession` configuration, inputs/outputs, start/stop.
2. Extract frame ingestion + throttling into a pipeline (e.g. `FramePipeline`): sample buffer to pixel buffer, downscale, fps control.
3. Extract guidance state into a coordinator (e.g. `GuidanceCoordinator`): ranking, cooldown, “1 main suggestion” policy.
4. Extract overlay rendering into a renderer (e.g. `GuidanceOverlayRenderer`): arrows/frames/skeleton drawing and animation.

### 2. Guidance Client（HTTP + WebSocket）越来越大

**Goal:** 传输协议、重连/退避、编解码、业务策略解耦。

**Steps:**

1. Split transport: `GuidanceHTTPClient` vs `GuidanceWebSocketClient`.
2. Split protocol codec: `GuidanceMessageCodec` (DTO encoding/decoding, schema versioning).
3. Split resilience: `RetryPolicy` / `BackpressureController` (queue limits, drop policy).

## Backend (FastAPI) Split Playbooks

### 3. `server/app/main.py` 变成 God file

**Goal:** `main.py` 只做 app wiring；HTTP/WS handler 薄；业务逻辑在 service。

**Steps:**

1. Move HTTP endpoints into `server/app/api/http.py` (or `server/app/api/routes.py`).
2. Move WebSocket handlers into `server/app/api/ws.py`.
3. Keep DTOs in `server/app/schemas.py` (or `server/app/schemas/`).
4. Keep guidance policy in `server/app/services/` (or keep `guidance.py` strictly为 service）。

### 4. `server/app/guidance.py` 同时做“策略 + 模型适配 + 文案”

**Goal:** 将“策略/排序”与“模型适配/推理调用”拆开，便于替换推理服务与做 A/B。

**Steps:**

1. `policy.py`: suggestion priority, cooldown, ok-to-shoot gating.
2. `adapters/`: cloud inference adapter(s), fallback adapter(s).
3. `copywriting.py`: suggestion message templates (no business logic).

## When to Warn vs Refuse

- **Warn:** File is 500–1000 lines. In code review or when adding features, suggest a split plan and point to this skill.
- **Refuse:** File is &gt;1000 lines. Do not add new responsibilities; require a split (or at least a concrete split plan) before extending it.
- **Target:** New code should aim for &lt;300 lines per file per core-principles; files that are single-purpose, decoupled, and self-contained may exceed 300 lines.

## References

- Rule: `codex/rules/core-principles.md` – file size and SRP
