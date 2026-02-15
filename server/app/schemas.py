from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


Style = Literal[
    "natural",  # 自然松弛
    "cool",  # 清冷高级
    "sweet_cool",  # 甜酷
    "film",  # 复古胶片
    "hk_night",  # 港风夜景
]

Camera = Literal["back", "front"]
SelfieMode = Literal["handheld", "tripod"]


class PoseKeypoint(BaseModel):
    name: str
    x: float
    y: float
    score: float = Field(default=1.0, ge=0.0, le=1.0)


class GuidanceRequest(BaseModel):
    # Client context
    style: Style = "natural"
    camera: Camera = "back"
    selfie_mode: Optional[SelfieMode] = None

    # Lightweight signals (MVP). Real implementation will be model-driven.
    persons: int = Field(default=0, ge=0)
    brightness: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    horizon_deg: Optional[float] = None
    stable: Optional[bool] = None

    # Optional pose keypoints (if client computes on-device for low latency)
    pose: Optional[List[PoseKeypoint]] = None

    # Client timestamp (ms)
    ts_ms: Optional[int] = None


SuggestionCategory = Literal["angle", "distance", "composition", "lighting", "pose", "stability"]
SuggestionTarget = Literal["photographer", "subject", "self"]


class GuidanceSuggestion(BaseModel):
    id: str
    category: SuggestionCategory
    target: SuggestionTarget

    # User-facing
    message: str
    tts: Optional[str] = None

    # Machine-readable action hint
    action: Optional[str] = None
    amount: Optional[float] = None
    unit: Optional[str] = None

    # UI overlay parameters (rendered client-side)
    overlay: Optional[Dict[str, Any]] = None

    priority: int = Field(default=1, ge=1, le=5)


class GuidanceResponse(BaseModel):
    ok_to_shoot: bool = False
    suggestions: List[GuidanceSuggestion] = Field(default_factory=list)

    # Debug only (dev)
    debug: Optional[Dict[str, Any]] = None
