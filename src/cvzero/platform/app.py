"""FastAPI factory; run locally with uvicorn cvzero.platform.app:create_app --factory."""

from __future__ import annotations

import base64
import logging
import os
import threading
import time
import uuid
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field

from .engine import Engine
from .store import EventStore

logger = logging.getLogger("cvzero.platform")


class FrameRequest(BaseModel):
    frame_id: int = Field(ge=0)
    image_base64: str = Field(min_length=8, max_length=2_800_000)


@dataclass
class Session:
    engine: Engine = field(default_factory=Engine)
    last_frame: int = -1
    lock: threading.Lock = field(default_factory=threading.Lock)
    touched: float = field(default_factory=time.monotonic)


def decode_image(encoded):
    try:
        raw = base64.b64decode(encoded, validate=True)
        if len(raw) > 2_000_000:
            raise ValueError("Encoded image exceeds 2 MB.")
        with Image.open(BytesIO(raw)) as image:
            if image.format not in {"PNG", "JPEG", "WEBP"}:
                raise ValueError("Use PNG, JPEG or WebP.")
            if image.width * image.height > 2_000_000:
                raise ValueError("Resize to at most 2 megapixels.")
            return np.array(image.convert("RGB"))
    except (ValueError, UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise HTTPException(400, f"Invalid image: {exc}") from exc


def create_app(database=None, model_path=None):
    app = FastAPI(title="CV Zero teaching platform", version="1.0.0")
    store = EventStore(database or os.environ.get("CVZERO_DB", "artifacts/platform/events.sqlite3"))
    sessions = {}
    registry_lock = threading.Lock()
    selected_model = model_path or os.environ.get("CVZERO_MODEL")
    detector = None
    if selected_model:
        selected_model = Path(selected_model)
        if not selected_model.is_file():
            raise FileNotFoundError(f"CVZERO_MODEL file is missing: {selected_model}")
        from ultralytics import YOLO

        class LockedDetector:
            def __init__(self, path):
                self.model = YOLO(str(path))
                self.lock = threading.Lock()

            def predict(self, *args, **kwargs):
                with self.lock:
                    return self.model.predict(*args, **kwargs)

        detector = LockedDetector(selected_model)

    @app.get("/")
    def dashboard():
        return FileResponse(Path(__file__).parent / "static/index.html")

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "version": "1.0.0",
            "active_sessions": len(sessions),
            "mode": "local teaching demo",
        }

    @app.post("/sessions", status_code=201)
    def new_session():
        with registry_lock:
            expired = [
                k
                for k, v in sessions.items()
                if time.monotonic() - v.touched > 1800 and not v.lock.locked()
            ]
            for k in expired:
                del sessions[k]
            if len(sessions) >= 64:
                raise HTTPException(
                    429, "Session limit reached; retry after inactive sessions expire."
                )
            identity = uuid.uuid4().hex
            sessions[identity] = Session(engine=Engine(yolo_model=detector))
        return {"session_id": identity}

    def get_session(identity):
        if identity not in sessions:
            raise HTTPException(404, "Unknown session. Create a new session first.")
        return sessions[identity]

    @app.post("/sessions/{identity}/frames")
    def analyze(identity: str, request: FrameRequest):
        session = get_session(identity)
        image = decode_image(request.image_base64)
        with session.lock:
            if request.frame_id <= session.last_frame:
                raise HTTPException(409, "frame_id must increase within a session.")
            report, overlay = session.engine.analyze(image)
            ok, buffer = cv2.imencode(".jpg", overlay[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 80])
            if not ok:
                raise HTTPException(500, "Output encoding failed.")
            store.append(identity, request.frame_id, time.time(), report)
            session.last_frame = request.frame_id
            session.touched = time.monotonic()
            logger.info(
                "frame_processed session=%s frame=%s count=%s latency_ms=%.2f",
                identity,
                request.frame_id,
                report["count"],
                report["latency_ms"],
            )
            return {
                "frame_id": request.frame_id,
                **report,
                "image_base64": base64.b64encode(buffer).decode("ascii"),
            }

    @app.get("/sessions/{identity}/history")
    def history(identity: str, limit: int = 100):
        get_session(identity)
        if not 1 <= limit <= 500:
            raise HTTPException(400, "limit must be in [1,500].")
        return {"events": store.history(identity, limit)}

    return app
