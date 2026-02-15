# Codex Agent Instructions (ai-camera)

This repo vendors a small set of reusable **rules** and **skills** under `codex/` (adapted from an internal baseline). Codex should treat them as the project’s local operating standards.

## Repo Structure (Current)

- iOS app: `AICamera/` (Xcode project)
- Backend: `server/` (FastAPI; WebSocket endpoint for real-time guidance)
- PRD: `prd/`
- Docs: `docs/`

## Core Rules (Short)

- Keep changes small and reviewable; avoid large rewrites unless asked.
- No secrets in code or configs. All config must be env-driven and documented in `.env.example`.
- Privacy is a first-class requirement: treat camera frames, user IDs, device IDs as sensitive.
- Prefer small, single-purpose files; split “god” modules early.

For the full baseline, see `codex/rules/`.

## Project Skills (Local)

These are vendored to this repo for reuse. To apply a skill, open its `SKILL.md` and follow it.

- `docs-md-standards`: `codex/skills/docs-md-standards/SKILL.md`
- `prd-standards`: `codex/skills/prd-standards/SKILL.md`
- `codereview`: `codex/skills/codereview/SKILL.md`
- `file-module-split`: `codex/skills/file-module-split/SKILL.md`
- `release-hardening`: `codex/skills/release-hardening/SKILL.md`
- `frontend-design`: `codex/skills/frontend-design/SKILL.md`
