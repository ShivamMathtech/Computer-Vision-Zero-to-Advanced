"""Camera and 3D geometry with explicit pixel/world coordinate conventions."""

from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree


def homogeneous(points):
    points = np.asarray(points, float)
    return np.column_stack([points, np.ones(len(points))])


def project(points, matrix):
    """Project world XYZ through a 3x4 matrix into pixel xy; require finite depth."""
    q = homogeneous(points) @ np.asarray(matrix).T
    if np.any(np.abs(q[:, 2]) < 1e-12):
        raise ValueError("Point projects to zero homogeneous depth.")
    return q[:, :2] / q[:, 2:3]


def apply_homography(points, h):
    q = homogeneous(points) @ np.asarray(h).T
    return q[:, :2] / q[:, 2:3]


def fit_homography(source, destination):
    """Normalized direct linear transform for at least four point pairs."""
    source, destination = np.asarray(source, float), np.asarray(destination, float)
    if source.shape != destination.shape or len(source) < 4:
        raise ValueError("Need four or more paired xy points.")

    def normalize(points):
        center = points.mean(0)
        scale = np.sqrt(2) / max(np.linalg.norm(points - center, axis=1).mean(), 1e-12)
        transform = np.array(
            [[scale, 0, -scale * center[0]], [0, scale, -scale * center[1]], [0, 0, 1]]
        )
        return apply_homography(points, transform), transform

    a, ta = normalize(source)
    b, tb = normalize(destination)
    design = []
    for (x, y), (u, v) in zip(a, b, strict=True):
        design.extend(
            [[-x, -y, -1, 0, 0, 0, u * x, u * y, u], [0, 0, 0, -x, -y, -1, v * x, v * y, v]]
        )
    _, _, vt = np.linalg.svd(design)
    h = np.linalg.inv(tb) @ vt[-1].reshape(3, 3) @ ta
    return h / h[2, 2]


def triangulate(left_xy, right_xy, p1, p2):
    """Linear triangulation: solve four equations per correspondence by SVD."""
    points = []
    for (u, v), (s, t) in zip(left_xy, right_xy, strict=True):
        design = np.stack(
            [u * p1[2] - p1[0], v * p1[2] - p1[1], s * p2[2] - p2[0], t * p2[2] - p2[1]]
        )
        _, _, vt = np.linalg.svd(design)
        points.append(vt[-1, :3] / vt[-1, 3])
    return np.array(points)


def disparity_to_depth(disparity, focal_px, baseline):
    """Z=fB/d. Invalid/nonpositive disparity returns NaN, not invented distance."""
    disparity = np.asarray(disparity, float)
    if focal_px <= 0 or baseline <= 0:
        raise ValueError("Focal length and baseline must be positive.")
    return np.divide(
        focal_px * baseline, disparity, out=np.full_like(disparity, np.nan), where=disparity > 0
    )


def backproject(depth, intrinsic):
    y, x = np.indices(depth.shape)
    rays = np.column_stack([x.ravel(), y.ravel(), np.ones(depth.size)]) @ np.linalg.inv(intrinsic).T
    return rays * depth.ravel()[:, None]


def rigid_fit(source, target):
    """Kabsch rigid alignment with reflection correction."""
    a, b = source.mean(0), target.mean(0)
    u, _, vt = np.linalg.svd((source - a).T @ (target - b))
    rotation = vt.T @ u.T
    if np.linalg.det(rotation) < 0:
        vt[-1] *= -1
        rotation = vt.T @ u.T
    translation = b - rotation @ a
    return rotation, translation


def icp(source, target, iterations=15):
    """Point-to-point ICP; depends on a reasonable initial alignment."""
    aligned = np.array(source, float, copy=True)
    tree = cKDTree(target)
    errors = []
    for _ in range(iterations):
        distances, indices = tree.query(aligned)
        r, t = rigid_fit(aligned, target[indices])
        aligned = aligned @ r.T + t
        errors.append(float(np.mean(distances)))
    return aligned, errors


def voxel_downsample(points, size=0.1):
    """Average points within integer voxel coordinates."""
    if size <= 0:
        raise ValueError("Voxel size must be positive.")
    keys, inverse = np.unique(np.floor(points / size).astype(int), axis=0, return_inverse=True)
    sums = np.zeros((len(keys), 3))
    np.add.at(sums, inverse, points)
    return sums / np.bincount(inverse)[:, None]


def volume_render(sigma, colors, distances):
    """Emission-absorption along one or more rays; background is white."""
    alpha = 1 - np.exp(-np.maximum(sigma, 0) * distances)
    transmittance = np.concatenate(
        [np.ones_like(alpha[..., :1]), np.cumprod(1 - alpha[..., :-1] + 1e-10, axis=-1)], axis=-1
    )
    weights = alpha * transmittance
    color = (weights[..., None] * colors).sum(axis=-2) + (1 - weights.sum(axis=-1))[..., None]
    return color, weights
