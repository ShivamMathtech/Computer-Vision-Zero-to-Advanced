"""Temporal, multimodal and geometric experiments on known synthetic truth."""

from __future__ import annotations

import cv2
import numpy as np
from scipy.ndimage import gaussian_filter

from .geometry import (
    disparity_to_depth,
    icp,
    project,
    rigid_fit,
    triangulate,
    voxel_downsample,
)
from .numerics import lucas_kanade_global
from .result import Result
from .tracking import KalmanTracker


def optical_flow(lesson=0, seed=42, amount=1.0):
    rng = np.random.default_rng(seed)
    first = (gaussian_filter(rng.random((80, 96)), 1) * 255).astype("uint8")
    shift = min(3.0, 0.5 * amount)
    second = cv2.warpAffine(
        first, np.float32([[1, 0, shift], [0, 1, 0]]), (96, 80), borderMode=cv2.BORDER_REFLECT
    )
    u, v = lucas_kanade_global(first.astype(float) / 255, second.astype(float) / 255)
    flow = cv2.calcOpticalFlowFarneback(first, second, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    points = cv2.goodFeaturesToTrack(first, 30, 0.01, 6)
    moved, status, _ = cv2.calcOpticalFlowPyrLK(first, second, points, None)
    valid = status.ravel().astype(bool)
    sparse = (moved - points)[valid].reshape(-1, 2)
    error = np.linalg.norm(flow[10:-10, 10:-10] - [shift, 0], axis=-1)
    return Result(
        "35 · Brightness constancy and optical flow",
        {
            "First frame": first,
            "Shifted frame": second,
            "Dense horizontal flow (pixels)": flow[..., 0],
            "Dense endpoint error (interior)": error,
        },
        metrics={
            "true_dx": shift,
            "numpy_dx": float(u),
            "numpy_dy": float(v),
            "sparse_mean_dx": float(sparse[:, 0].mean()),
            "dense_mean_endpoint_error": float(error.mean()),
        },
        notes="Lucas–Kanade reference estimates one small global translation. Dense flow is not object identity. Reflect padding is excluded from the error region.",
    )


def multi_tracking(lesson=0, seed=42, amount=1.0):
    rng = np.random.default_rng(seed)
    tracker = KalmanTracker(gate=18, max_missed=4)
    frames = 32
    paths = [[], []]
    switches = 0
    previous = {}
    for t in range(frames):
        true = np.array([[10 + 2 * t, 24 + 0.2 * t], [80 - 1.8 * t, 62 - 0.4 * t]])
        detections = true + rng.normal(0, amount, true.shape)
        if lesson > 0 and 12 <= t <= 14:
            detections = detections[1:]
        tracks = tracker.update(detections)
        for obj in range(2):
            if tracks:
                track = min(tracks, key=lambda tr: np.linalg.norm(tr.state[:2] - true[obj]))
                if np.linalg.norm(track.state[:2] - true[obj]) < 8:
                    if obj in previous and previous[obj] != track.identity:
                        switches += 1
                    previous[obj] = track.identity
                    paths[obj].append(track.state[:2].copy())
    return Result(
        "36 · Assignment, prediction and track IDs",
        curves={f"Track for truth object {i} (x→y)": np.array(p) for i, p in enumerate(paths)},
        metrics={
            "frames": frames,
            "nearest_truth_id_switches": switches,
            "final_active_tracks": len(tracker.tracks),
        },
        notes="Two well separated generated trajectories. This is a center-only Kalman/Hungarian teaching tracker, not a full SORT or DeepSORT implementation. Nearest-truth association is a toy diagnostic, not HOTA or IDF1.",
    )


def multimodal(lesson=0, seed=42, amount=1.0):
    rng = np.random.default_rng(seed)
    truth = rng.integers(0, 2, 160)
    visual = truth + rng.normal(0, 0.55 * amount, len(truth))
    depth = truth + rng.normal(0, 0.35, len(truth))
    present = rng.random(len(truth)) > (0.35 if lesson else 0)
    # Precision-weighted fusion assumes conditionally independent Gaussian errors.
    wv, wd = 1 / (0.55 * amount) ** 2, 1 / 0.35**2
    fused = (wv * visual + wd * depth * present) / (wv + wd * present)
    return Result(
        "41 · Sensor fusion and missing modalities",
        curves={
            "Visual signal": visual[:40],
            "Depth signal": depth[:40],
            "Fused signal": fused[:40],
        },
        metrics={
            "visual_accuracy": float(((visual > 0.5) == truth).mean()),
            "fusion_accuracy": float(((fused > 0.5) == truth).mean()),
            "missing_depth": int((~present).sum()),
        },
        notes="Generated binary labels and noisy scalar sensor readings. Precision weights use known synthetic noise; real systems must estimate uncertainty on held-out data and synchronize timestamps. Text-image learning is in Chapter 40.",
    )


def reconstruction(lesson=0, seed=42, amount=1.0):
    rng = np.random.default_rng(seed)
    xyz = rng.uniform([-1, -0.6, 3], [1, 0.6, 6], (150, 3))
    k = np.array([[240.0, 0, 160], [0, 240, 120], [0, 0, 1]])
    p1 = k @ np.column_stack([np.eye(3), np.zeros(3)])
    p2 = k @ np.column_stack([np.eye(3), [-0.3, 0, 0]])
    a, b = project(xyz, p1), project(xyz, p2)
    sigma = 0 if lesson == 0 else 0.15 * amount
    noisy_a, noisy_b = a + rng.normal(0, sigma, a.shape), b + rng.normal(0, sigma, b.shape)
    recovered = triangulate(noisy_a, noisy_b, p1, p2)
    cv = cv2.triangulatePoints(p1, p2, noisy_a.T, noisy_b.T)
    cv = (cv[:3] / cv[3]).T
    return Result(
        "44 · Two-view 3D reconstruction",
        points={"True world coordinates (m)": xyz, "Triangulated coordinates (m)": recovered},
        metrics={
            "mean_3d_error_m": float(np.linalg.norm(recovered - xyz, axis=1).mean()),
            "numpy_opencv_max_difference": float(np.abs(recovered - cv).max()),
            "noise_sigma_px": sigma,
        },
        notes="Calibrated rectified cameras and known correspondences. Pose recovery, correspondence search and bundle adjustment are separate problems; this experiment isolates triangulation.",
    )


def depth(lesson=0, seed=42, amount=1.0):
    y, x = np.mgrid[:64, :96]
    true = 2 + x / 40 + y / 60
    focal, baseline = 200.0, 0.12
    rng = np.random.default_rng(seed)
    disparity = focal * baseline / true + rng.normal(0, 0.1 * amount, true.shape)
    if lesson == 2:
        disparity[20:30, 20:40] = 0
    estimate = disparity_to_depth(disparity, focal, baseline)
    valid = np.isfinite(estimate)
    uncertainty = focal * baseline / np.maximum(disparity, 1e-6) ** 2 * 0.1 * amount
    return Result(
        "45 · Metric depth and uncertainty",
        {
            "True Z (m)": true,
            "Disparity (px)": disparity,
            "Estimated Z (m)": estimate,
            "First-order uncertainty (m)": np.where(valid, uncertainty, np.nan),
        },
        metrics={
            "valid_fraction": float(valid.mean()),
            "valid_mae_m": float(np.abs(estimate[valid] - true[valid]).mean()),
        },
        notes="Stereo depth from known calibration; zero disparity is invalid. Monocular learned depth may have unknown scale, so it cannot silently be substituted into this formula as metric distance.",
    )


def stereo(lesson=0, seed=42, amount=1.0):
    rng = np.random.default_rng(seed)
    left = rng.integers(0, 256, (80, 160), dtype="uint8")
    d = int(np.clip(round(8 * amount), 2, 14))
    right = np.zeros_like(left)
    right[:, :-d] = left[:, d:]
    # Compare integer disparity hypotheses after rectification; invalid left columns excluded.
    costs = []
    for candidate in range(16):
        shifted = np.zeros_like(right)
        if candidate:
            shifted[:, candidate:] = right[:, :-candidate]
        else:
            shifted[:] = right
        error = np.abs(left.astype(float) - shifted.astype(float))
        costs.append(cv2.boxFilter(error, -1, (7, 7), normalize=True))
    reference = np.argmin(costs, axis=0)
    matcher = cv2.StereoSGBM_create(
        minDisparity=0, numDisparities=16, blockSize=5, P1=8 * 25, P2=32 * 25, uniquenessRatio=5
    )
    prediction = matcher.compute(left, right).astype(float) / 16
    roi = (slice(8, -8), slice(24, -16))
    return Result(
        "46 · Rectified stereo matching",
        {
            "Left": left,
            "Right": right,
            "Block matching disparity": reference,
            "SGBM disparity": prediction,
        },
        metrics={
            "true_disparity_px": d,
            "block_mae_px": float(np.abs(reference[roi] - d).mean()),
            "sgbm_mae_px": float(np.abs(prediction[roi] - d).mean()),
        },
        notes="One fronto-parallel plane with random texture, no distortion and one known disparity. Dividing OpenCV fixed-point disparity by 16 is essential. Occlusions and textureless surfaces are not solved here.",
    )


def point_clouds(lesson=0, seed=42, amount=1.0):
    rng = np.random.default_rng(seed)
    target = rng.uniform(-1, 1, (250, 3))
    target[:, 2] *= 0.3
    angle = 0.06 * amount
    r = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    source = target @ r.T + [0.06, 0.04, 0.03]
    aligned, errors = icp(source, target, iterations=20)
    sampled = voxel_downsample(aligned, 0.18 * amount)
    rr, tt = rigid_fit(source, target)
    return Result(
        "47 · Point cloud alignment and sampling",
        points={"Source": source, "Aligned": aligned, "Voxel means": sampled},
        curves={"ICP nearest-neighbor mean distance": errors},
        metrics={
            "input_points": len(source),
            "voxel_points": len(sampled),
            "paired_rigid_rmse": float(np.sqrt(np.mean((source @ rr.T + tt - target) ** 2))),
        },
        notes="ICP uses nearest neighbors and can converge to a local minimum. The paired Kabsch result is a separate easier problem with known correspondences. Units are arbitrary scene units.",
    )
