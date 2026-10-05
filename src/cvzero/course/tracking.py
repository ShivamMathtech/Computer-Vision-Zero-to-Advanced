"""Small Kalman/Hungarian tracker and landmark geometry for educational sequences."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linear_sum_assignment


@dataclass
class Track:
    identity: int
    state: np.ndarray
    covariance: np.ndarray
    missed: int = 0
    history: list = field(default_factory=list)


class KalmanTracker:
    """Track XY centers; anonymous IDs, constant-velocity model and distance gating.

    This teaches SORT's ingredients, but is not a reproduction of SORT/DeepSORT:
    there is no box-size state or learned appearance embedding.
    """

    def __init__(self, gate=25.0, max_missed=4):
        self.gate, self.max_missed = gate, max_missed
        self.tracks = []
        self.next_identity = 1

    def update(self, centers, dt=1.0):
        centers = np.asarray(centers, float).reshape(-1, 2)
        if dt <= 0:
            raise ValueError("dt must be positive.")
        f = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1.0]])
        h = np.eye(2, 4)
        q = (
            np.array(
                [
                    [dt**4 / 4, 0, dt**3 / 2, 0],
                    [0, dt**4 / 4, 0, dt**3 / 2],
                    [dt**3 / 2, 0, dt**2, 0],
                    [0, dt**3 / 2, 0, dt**2],
                ]
            )
            * 0.1
        )
        for track in self.tracks:
            track.state = f @ track.state
            track.covariance = f @ track.covariance @ f.T + q
            track.missed += 1
        matched = set()
        if self.tracks and len(centers):
            costs = np.linalg.norm(
                np.array([t.state[:2] for t in self.tracks])[:, None] - centers, axis=2
            )
            rows, cols = linear_sum_assignment(np.where(costs <= self.gate, costs, 1e6))
            for row, col in zip(rows, cols, strict=True):
                if costs[row, col] > self.gate:
                    continue
                track = self.tracks[row]
                residual = centers[col] - h @ track.state
                s = h @ track.covariance @ h.T + np.eye(2) * 2
                gain = np.linalg.solve(s, h @ track.covariance).T
                track.state += gain @ residual
                a = np.eye(4) - gain @ h
                track.covariance = a @ track.covariance @ a.T + gain @ (np.eye(2) * 2) @ gain.T
                track.missed = 0
                matched.add(col)
        self.tracks = [t for t in self.tracks if t.missed <= self.max_missed]
        for index, center in enumerate(centers):
            if index not in matched:
                self.tracks.append(
                    Track(self.next_identity, np.r_[center, 0.0, 0.0], np.eye(4) * 10)
                )
                self.next_identity += 1
        for track in self.tracks:
            track.history.append(track.state[:2].tolist())
            track.history = track.history[-100:]
        return self.tracks


def joint_angle(a, b, c):
    """Angle ABC in degrees; reject a zero-length limb."""
    u, v = np.asarray(a) - b, np.asarray(c) - b
    length = np.linalg.norm(u) * np.linalg.norm(v)
    if length < 1e-10:
        raise ValueError("Cannot measure an angle with a zero-length limb.")
    return float(np.degrees(np.arccos(np.clip(u @ v / length, -1, 1))))


def soft_argmax(heatmap, temperature=0.1):
    """Expected xy under a softmax spatial distribution."""
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    probability = np.exp((heatmap - heatmap.max()) / temperature)
    probability /= probability.sum()
    y, x = np.indices(heatmap.shape)
    return np.array([(x * probability).sum(), (y * probability).sum()])


def count_repetitions(angles, low=60.0, high=150.0):
    """Hysteresis state machine: high -> low -> high completes one cycle."""
    count, state = 0, "waiting_high"
    for angle in angles:
        if state == "waiting_high" and angle >= high:
            state = "ready"
        elif state == "ready" and angle <= low:
            state = "bent"
        elif state == "bent" and angle >= high:
            count += 1
            state = "ready"
    return count
