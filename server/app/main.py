from __future__ import annotations

import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from .guidance import STYLE_LABELS, generate_guidance
from .schemas import GuidanceRequest, GuidanceResponse


load_dotenv()


def _parse_allow_origins(raw: str) -> List[str]:
    raw = (raw or "").strip()
    if not raw or raw == "*":
        return ["*"]
    return [o.strip() for o in raw.split(",") if o.strip()]


app = FastAPI(
    title="AI Camera API",
    version="0.1.0",
    default_response_class=ORJSONResponse,
)

allow_origins = _parse_allow_origins(os.getenv("ALLOW_ORIGINS", "*"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/v1/styles")
def list_styles():
    styles = [{"id": k, "label": v} for k, v in STYLE_LABELS.items()]
    return {"styles": styles, "default": "natural"}


@app.post("/v1/guidance", response_model=GuidanceResponse)
def guidance(req: GuidanceRequest):
    return generate_guidance(req)


@app.websocket("/v1/guidance/ws")
async def guidance_ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            payload = await ws.receive_json()
            req = GuidanceRequest.model_validate(payload)
            resp = generate_guidance(req)
            await ws.send_json(resp.model_dump())
    except WebSocketDisconnect:
        return
