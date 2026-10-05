"""API contract, persistence, input errors and session isolation."""

import base64
from io import BytesIO

import cv2
import numpy as np
import pytest
from PIL import Image

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from cvzero.platform.app import create_app
from cvzero.platform.engine import Engine


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(tmp_path / "events.sqlite")) as client:
        yield client


def image_payload(frame_id=0):
    image = np.zeros((64, 64, 3), np.uint8)
    cv2.circle(image, (30, 30), 10, (0, 0, 255), -1)
    _, buffer = cv2.imencode(".png", image)
    return {"frame_id": frame_id, "image_base64": base64.b64encode(buffer).decode()}


def test_pipeline_detects_and_preserves_input():
    rgb = np.zeros((64, 64, 3), np.uint8)
    cv2.circle(rgb, (30, 30), 10, (255, 0, 0), -1)
    before = rgb.copy()
    report, overlay = Engine().analyze(rgb)
    assert report["count"] == 1 and report["detections"][0]["track_id"] == 1
    assert report["detections"][0]["score"] is None
    np.testing.assert_array_equal(rgb, before)
    assert overlay.shape == rgb.shape


def test_api_persistence_order_and_session_isolation(client):
    a = client.post("/sessions").json()["session_id"]
    b = client.post("/sessions").json()["session_id"]
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/").status_code == 200
    response = client.post(f"/sessions/{a}/frames", json=image_payload())
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert client.post(f"/sessions/{a}/frames", json=image_payload()).status_code == 409
    assert len(client.get(f"/sessions/{a}/history").json()["events"]) == 1
    assert client.get(f"/sessions/{b}/history").json()["events"] == []
    assert client.post(f"/sessions/{b}/frames", json=image_payload()).status_code == 200
    assert client.get(f"/sessions/{a}/history?limit=1000").status_code == 400
    assert client.get("/sessions/missing/history").status_code == 404


def test_invalid_requests_do_not_persist(client):
    sid = client.post("/sessions").json()["session_id"]
    assert (
        client.post(
            f"/sessions/{sid}/frames", json={"frame_id": 0, "image_base64": "not+an+image"}
        ).status_code
        == 400
    )
    assert client.post(f"/sessions/{sid}/frames", json=image_payload(-1)).status_code == 422
    assert client.get(f"/sessions/{sid}/history").json()["events"] == []


def test_decode_dimension_limit(client):
    buffer = BytesIO()
    Image.new("RGB", (1500, 1500)).save(buffer, format="PNG")
    sid = client.post("/sessions").json()["session_id"]
    response = client.post(
        f"/sessions/{sid}/frames",
        json={"frame_id": 0, "image_base64": base64.b64encode(buffer.getvalue()).decode()},
    )
    assert response.status_code == 400
    assert "2 megapixels" in response.json()["detail"]
