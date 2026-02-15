from __future__ import annotations

import uuid
from typing import Dict, Tuple

from .schemas import GuidanceRequest, GuidanceResponse, GuidanceSuggestion


STYLE_LABELS: Dict[str, str] = {
    "natural": "自然松弛",
    "cool": "清冷高级",
    "sweet_cool": "甜酷",
    "film": "复古胶片",
    "hk_night": "港风夜景",
}


def _sid() -> str:
    return uuid.uuid4().hex[:10]


def _arrow(direction: str, strength: float = 0.7):
    return {"type": "arrow", "direction": direction, "strength": strength}


def generate_guidance(req: GuidanceRequest) -> GuidanceResponse:
    """MVP stub.

    Inputs are lightweight signals. Real implementation will be replaced by
    model inference (pose + scene + lighting) and policy/ranking.

    Output rule: return 1 main suggestion (+ optional 1 secondary).
    """

    suggestions = []

    # 0) No person detected
    if req.persons <= 0:
        msg = "画面里还没有人，先把人放进取景框里"
        suggestions.append(
            GuidanceSuggestion(
                id=_sid(),
                category="composition",
                target="photographer",
                message=msg,
                tts=msg,
                action="find_subject",
                overlay=None,
                priority=5,
            )
        )
        return GuidanceResponse(ok_to_shoot=False, suggestions=suggestions)

    target = "self" if req.camera == "front" else "subject"

    # 1) Lighting check (simple)
    if req.brightness is not None and req.brightness < 0.22:
        if req.style == "hk_night":
            msg = "找一盏灯或霓虹，让脸靠近光源一点"
        else:
            msg = "有点暗，把人转向光源或靠近窗边"
        suggestions.append(
            GuidanceSuggestion(
                id=_sid(),
                category="lighting",
                target=target,
                message=msg,
                tts=msg,
                action="move_to_light",
                overlay=_arrow("up", 0.55),
                priority=5,
            )
        )
        return GuidanceResponse(ok_to_shoot=False, suggestions=suggestions, debug={"style": req.style})

    # 2) Horizon / stability (simple)
    if req.horizon_deg is not None and abs(req.horizon_deg) > 2.0:
        direction = "left" if req.horizon_deg > 0 else "right"
        msg = "把画面扶正一点"
        suggestions.append(
            GuidanceSuggestion(
                id=_sid(),
                category="stability",
                target="photographer",
                message=msg,
                tts=msg,
                action="level_horizon",
                amount=abs(req.horizon_deg),
                unit="deg",
                overlay=_arrow(direction, 0.7),
                priority=5,
            )
        )
        return GuidanceResponse(ok_to_shoot=False, suggestions=suggestions)

    # 3) Pose hints (very lightweight; real version uses keypoints)
    pose_msg, ok = _pose_hint(req.style, req.camera, req.selfie_mode)
    suggestions.append(
        GuidanceSuggestion(
            id=_sid(),
            category="pose",
            target=target,
            message=pose_msg,
            tts=pose_msg,
            action="pose_step",
            overlay=None,
            priority=4,
        )
    )

    return GuidanceResponse(
        ok_to_shoot=ok,
        suggestions=suggestions,
        debug={"style": req.style, "style_label": STYLE_LABELS.get(req.style, req.style)},
    )


def _pose_hint(style: str, camera: str, selfie_mode: str | None) -> Tuple[str, bool]:
    # For dev we treat it as always achievable after 1 step.
    if camera == "front" and selfie_mode == "tripod":
        base = "站直，身体侧 20 度，下巴微收，眼神看向镜头"
        return base, True

    if style == "natural":
        return "肩放松，身体侧 30 度，手自然放在腰线附近", True
    if style == "cool":
        return "下巴微抬，表情克制，身体侧 20 度，留一点侧脸线条", True
    if style == "sweet_cool":
        return "重心放一侧，手做一个小动作（拨头发/扶帽檐）", True
    if style == "film":
        return "轻轻回头看镜头，别绷紧，像被抓拍到一样", True
    if style == "hk_night":
        return "脸朝向光源，眼神看向远处，再慢慢回到镜头", True

    return "身体侧一点，肩放松，下巴微收", True
