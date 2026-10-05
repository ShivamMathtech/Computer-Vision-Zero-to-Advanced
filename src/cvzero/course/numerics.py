"""Readable NumPy reference algorithms. Prefer optimized libraries for large inputs."""

from __future__ import annotations

from collections import deque

import numpy as np


def gray(image):
    """Convert RGB to float grayscale; leave 2D input as floating point."""
    values = np.asarray(image, dtype=float)
    return values @ np.array([0.299, 0.587, 0.114]) if values.ndim == 3 else values


def correlate(image, kernel):
    """Odd-sized correlation with replicated borders; no kernel reversal."""
    image, kernel = np.asarray(image, float), np.asarray(kernel, float)
    if image.ndim != 2 or kernel.ndim != 2 or any(v % 2 != 1 for v in kernel.shape):
        raise ValueError("Use a 2D image and an odd-sized 2D kernel.")
    ry, rx = np.array(kernel.shape) // 2
    padded = np.pad(image, ((ry, ry), (rx, rx)), mode="edge")
    out = np.empty_like(image)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            out[y, x] = np.sum(padded[y : y + kernel.shape[0], x : x + kernel.shape[1]] * kernel)
    return out


def gaussian_kernel(size=5, sigma=1.0):
    """Sample and normalize a Gaussian; discrete weights sum to one."""
    if size < 1 or size % 2 == 0 or sigma <= 0:
        raise ValueError("size must be positive/odd and sigma positive")
    x = np.arange(size) - size // 2
    weights = np.exp(-x * x / (2 * sigma * sigma))
    weights /= weights.sum()
    return np.outer(weights, weights)


def sobel(image):
    """Return horizontal/vertical derivatives and gradient magnitude."""
    kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    gx, gy = correlate(gray(image), kernel), correlate(gray(image), kernel.T)
    return gx, gy, np.hypot(gx, gy)


def equalize(image):
    """Histogram equalization with the first occupied CDF bin subtracted."""
    image = np.asarray(image, dtype=np.uint8)
    counts = np.bincount(image.ravel(), minlength=256)
    cdf = counts.cumsum()
    first = cdf[counts > 0][0]
    if cdf[-1] == first:
        return image.copy()
    table = np.rint((cdf - first) / (cdf[-1] - first) * 255).clip(0, 255).astype(np.uint8)
    return table[image]


def otsu(image):
    """Choose the threshold maximizing between-class variance."""
    values = np.asarray(image, dtype=np.uint8)
    hist = np.bincount(values.ravel(), minlength=256).astype(float)
    probabilities = hist / hist.sum()
    weights = probabilities.cumsum()
    means = (probabilities * np.arange(256)).cumsum()
    denom = weights * (1 - weights)
    score = np.divide((means[-1] * weights - means) ** 2, denom, out=np.zeros(256), where=denom > 0)
    threshold = int(np.argmax(score))
    return threshold, values > threshold


def morphology(mask, size=3, operation="erode"):
    """Binary square erosion/dilation with false values outside the image."""
    if size < 1 or size % 2 == 0 or operation not in {"erode", "dilate"}:
        raise ValueError("Use odd size and erode/dilate.")
    mask = np.asarray(mask, bool)
    pad = size // 2
    padded = np.pad(mask, pad, mode="constant")
    out = np.zeros_like(mask)
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            patch = padded[y : y + size, x : x + size]
            out[y, x] = patch.all() if operation == "erode" else patch.any()
    return out


def components(mask):
    """4-connected foreground labels using a queue flood-fill, background=0."""
    mask = np.asarray(mask, bool)
    labels = np.zeros(mask.shape, np.int32)
    count = 0
    for y, x in zip(*np.nonzero(mask), strict=True):
        if labels[y, x]:
            continue
        count += 1
        labels[y, x] = count
        queue = deque([(y, x)])
        while queue:
            yy, xx = queue.popleft()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yn, xn = yy + dy, xx + dx
                if 0 <= yn < mask.shape[0] and 0 <= xn < mask.shape[1]:
                    if mask[yn, xn] and not labels[yn, xn]:
                        labels[yn, xn] = count
                        queue.append((yn, xn))
    return labels, count


def kmeans(values, k=3, iterations=20, seed=42):
    """Lloyd updates with deterministic initialization and empty-cluster repair."""
    values = np.asarray(values, float)
    if values.ndim != 2 or not 1 <= k <= len(values):
        raise ValueError("Expected N by D values and 1 <= k <= N.")
    rng = np.random.default_rng(seed)
    centers = values[rng.choice(len(values), k, replace=False)].copy()
    for _ in range(iterations):
        distances = ((values[:, None] - centers[None]) ** 2).sum(axis=2)
        labels = distances.argmin(axis=1)
        updated = np.array(
            [
                values[labels == i].mean(axis=0)
                if np.any(labels == i)
                else values[distances.min(axis=1).argmax()]
                for i in range(k)
            ]
        )
        if np.allclose(updated, centers):
            break
        centers = updated
    labels = ((values[:, None] - centers[None]) ** 2).sum(axis=2).argmin(axis=1)
    return labels, centers


def harris(image, k=0.04, window=5):
    """Corner response det(M)-k*trace(M)^2 from local gradient products."""
    gx, gy, _ = sobel(image)
    average = np.ones((window, window)) / window**2
    a, b, c = (correlate(v, average) for v in (gx * gx, gx * gy, gy * gy))
    return a * c - b * b - k * (a + c) ** 2


def hog(image, cell_size=8, bins=9):
    """Unsigned orientation histograms per cell, L2 normalized; teaching HOG."""
    gx, gy, magnitude = sobel(image)
    angles = np.mod(np.arctan2(gy, gx), np.pi)
    result = []
    for y in range(0, image.shape[0] - cell_size + 1, cell_size):
        row = []
        for x in range(0, image.shape[1] - cell_size + 1, cell_size):
            sl = np.s_[y : y + cell_size, x : x + cell_size]
            hist, _ = np.histogram(angles[sl], bins=bins, range=(0, np.pi), weights=magnitude[sl])
            row.append(hist / np.sqrt((hist * hist).sum() + 1e-8))
        result.append(row)
    return np.array(result)


def canny_reference(image, low=0.1, high=0.25):
    """Simplified Canny: smooth, Sobel, four-direction NMS, hysteresis."""
    if not 0 < low <= high <= 1:
        raise ValueError("Require 0 < low <= high <= 1 for relative thresholds.")
    smoothed = correlate(gray(image), gaussian_kernel())
    gx, gy, magnitude = sobel(smoothed)
    orientation = (np.rad2deg(np.arctan2(gy, gx)) + 180) % 180
    thinned = np.zeros_like(magnitude)
    offsets = [(0, 1), (1, 1), (1, 0), (1, -1)]
    for y in range(1, magnitude.shape[0] - 1):
        for x in range(1, magnitude.shape[1] - 1):
            direction = int((orientation[y, x] + 22.5) // 45) % 4
            dy, dx = offsets[direction]
            value = magnitude[y, x]
            if value >= magnitude[y + dy, x + dx] and value >= magnitude[y - dy, x - dx]:
                thinned[y, x] = value
    if thinned.max() == 0:
        return np.zeros_like(thinned, bool)
    strong = thinned >= high * thinned.max()
    weak = thinned >= low * thinned.max()
    queue = deque(zip(*np.nonzero(strong), strict=True))
    while queue:
        y, x = queue.popleft()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                yy, xx = y + dy, x + dx
                if 0 <= yy < strong.shape[0] and 0 <= xx < strong.shape[1]:
                    if weak[yy, xx] and not strong[yy, xx]:
                        strong[yy, xx] = True
                        queue.append((yy, xx))
    return strong


def iou(box, others):
    """Continuous xyxy boxes with exclusive extent; broadcast against N boxes."""
    box, others = np.asarray(box, float), np.asarray(others, float).reshape(-1, 4)
    intersection = np.maximum(
        0, np.minimum(box[2:], others[:, 2:]) - np.maximum(box[:2], others[:, :2])
    ).prod(1)
    area_a = np.maximum(0, box[2:] - box[:2]).prod()
    area_b = np.maximum(0, others[:, 2:] - others[:, :2]).prod(1)
    return intersection / np.maximum(area_a + area_b - intersection, 1e-12)


def nms(boxes, scores, threshold=0.5):
    """Greedily keep the best score and suppress same-class overlap."""
    boxes = np.asarray(boxes, float).reshape(-1, 4)
    if len(scores) != len(boxes) or not 0 <= threshold <= 1:
        raise ValueError("Scores must match boxes and threshold must be in [0, 1].")
    order = np.argsort(-np.asarray(scores), kind="stable")
    keep = []
    while len(order):
        index = int(order[0])
        keep.append(index)
        order = order[1:][iou(boxes[index], boxes[order[1:]]) <= threshold]
    return np.array(keep, int)


def average_precision(truth_flags, scores, ground_truth_count):
    """All-points interpolated AP for already matched detections of one class."""
    if ground_truth_count < 1:
        raise ValueError("AP requires at least one ground-truth positive.")
    order = np.argsort(-np.asarray(scores), kind="stable")
    tp = np.asarray(truth_flags, bool)[order].cumsum()
    recall = tp / ground_truth_count
    precision = tp / np.arange(1, len(tp) + 1)
    r = np.r_[0, recall, 1]
    p = np.r_[0, precision, 0]
    p = np.maximum.accumulate(p[::-1])[::-1]
    changes = np.where(r[1:] != r[:-1])[0]
    return float(((r[changes + 1] - r[changes]) * p[changes + 1]).sum()), precision, recall


def softmax(values, axis=-1):
    values = np.asarray(values, float)
    exp = np.exp(values - values.max(axis=axis, keepdims=True))
    return exp / exp.sum(axis=axis, keepdims=True)


def attention(q, k, v, mask=None):
    """Scaled dot-product attention, optionally masking prohibited pairs."""
    scores = np.asarray(q) @ np.asarray(k).T / np.sqrt(np.asarray(q).shape[-1])
    if mask is not None:
        mask = np.broadcast_to(np.asarray(mask, bool), scores.shape)
        if not mask.any(axis=-1).all():
            raise ValueError("Every query must have at least one allowed key.")
        scores = np.where(mask, scores, -np.inf)
    weights = softmax(scores)
    return weights @ v, weights


def lucas_kanade_global(first, second):
    """One global small-translation estimate via brightness-constancy least squares."""
    first, second = gray(first), gray(second)
    gy, gx = np.gradient((first + second) / 2)
    design = np.column_stack([gx[2:-2, 2:-2].ravel(), gy[2:-2, 2:-2].ravel()])
    delta = (second - first)[2:-2, 2:-2].ravel()
    velocity, _, _, _ = np.linalg.lstsq(design, -delta, rcond=None)
    return velocity


def mlp_train(x, y, steps=150, learning_rate=0.2, seed=42):
    """One hidden tanh layer; explicit cross-entropy backpropagation."""
    rng = np.random.default_rng(seed)
    classes = int(max(y)) + 1
    w1 = rng.normal(0, 0.3, (x.shape[1], 12))
    b1 = np.zeros(12)
    w2 = rng.normal(0, 0.3, (12, classes))
    b2 = np.zeros(classes)
    onehot = np.eye(classes)[y]
    losses = []
    for _ in range(steps):
        hidden = np.tanh(x @ w1 + b1)
        probability = softmax(hidden @ w2 + b2)
        losses.append(float(-np.log(probability[np.arange(len(y)), y] + 1e-12).mean()))
        dz = (probability - onehot) / len(x)
        dw2, db2 = hidden.T @ dz, dz.sum(0)
        dh = (dz @ w2.T) * (1 - hidden**2)
        dw1, db1 = x.T @ dh, dh.sum(0)
        w1 -= learning_rate * dw1
        b1 -= learning_rate * db1
        w2 -= learning_rate * dw2
        b2 -= learning_rate * db2
    return (w1, b1, w2, b2), losses


def mlp_predict(x, parameters):
    w1, b1, w2, b2 = parameters
    return softmax(np.tanh(x @ w1 + b1) @ w2 + b2)


def convolve(image, kernel):
    """Mathematical 2D convolution: flip both kernel axes before correlation."""
    return correlate(image, np.asarray(kernel)[::-1, ::-1])


def mean_filter(image, size=3):
    """Uniform neighborhood mean, using the same explicit border convention."""
    if size < 1 or size % 2 == 0:
        raise ValueError("Use a positive odd filter size.")
    return correlate(image, np.ones((size, size)) / size**2)


def gaussian_filter(image, size=5, sigma=1.0):
    """Gaussian smoothing through explicit NumPy correlation."""
    return correlate(image, gaussian_kernel(size, sigma))


def threshold(image, cutoff):
    """Boolean threshold with strict greater-than semantics."""
    if not np.isfinite(cutoff):
        raise ValueError("cutoff must be finite")
    return np.asarray(image) > cutoff
