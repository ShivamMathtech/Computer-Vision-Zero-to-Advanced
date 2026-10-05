"""Executable classical-vision chapter experiments, each with a distinct question."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import cv2
import numpy as np
from scipy.ndimage import median_filter
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from ..synthetic import make_scene
from . import numerics as n
from .geometry import apply_homography, fit_homography
from .result import Result
from .tracking import KalmanTracker


def picture(seed=42, size=96):
    image = make_scene(size, size, seed)
    cv2.line(image, (5, 5), (size - 5, size - 8), (230, 230, 230), 2)
    return image


def shapes(seed=42):
    mask = np.zeros((80, 112), np.uint8)
    cv2.rectangle(mask, (8, 9), (35, 32), 255, -1)
    cv2.circle(mask, (75, 26), 16, 255, -1)
    cv2.fillPoly(mask, [np.array([[28, 51], [9, 73], [45, 73]])], 255)
    return mask


def mathematics(lesson, seed, amount):
    rng = np.random.default_rng(seed)
    if lesson == 0:
        grid = np.array([[1.0, 2.0], [3.0, 4.0]])
        values, vectors = np.linalg.eigh(grid.T @ grid)
        return Result(
            "02 · Matrices, dot products and eigenvectors",
            {
                "Matrix A": grid,
                "A transpose times A": grid.T @ grid,
                "Eigenvectors (columns)": vectors,
            },
            metrics={
                "dot_product": float(np.array([1, 2]) @ np.array([3, 4])),
                "eigen_residual": float(np.linalg.norm(grid.T @ grid @ vectors - vectors * values)),
            },
        )
    if lesson == 1:
        x = np.linspace(-2, 2, 100)
        derivative = np.gradient(x * x, x)
        w = 4.0
        losses = []
        steps = []
        for _ in range(25):
            losses.append((w - 1) ** 2)
            steps.append(w)
            w -= 0.1 * amount * 2 * (w - 1)
        return Result(
            "02 · Derivatives and gradient descent",
            curves={
                "Analytic derivative": np.c_[x, 2 * x],
                "Finite derivative": np.c_[x, derivative],
                "Loss per update": losses,
            },
            metrics={"final_parameter": w, "target": 1.0},
        )
    x = np.linspace(0, 1, 128, endpoint=False)
    signal = np.sin(2 * np.pi * 8 * x) + rng.normal(0, 0.2 * amount, len(x))
    spectrum = np.abs(np.fft.rfft(signal))
    return Result(
        "02 · Probability, noise and Fourier frequency",
        {"Signal": signal, "FFT magnitude": spectrum},
        metrics={
            "sample_mean": float(signal.mean()),
            "sample_variance": float(signal.var()),
            "peak_frequency_bin": int(spectrum[1:].argmax() + 1),
        },
    )


def fundamentals(lesson, seed, amount):
    image = picture(seed)
    if lesson == 0:
        panels = {"RGB": image, "Red channel": image[..., 0], "Grayscale": n.gray(image)}
        metrics = {
            "shape": list(image.shape),
            "dtype": str(image.dtype),
            "array_bytes": image.nbytes,
        }
    elif lesson == 1:
        levels = max(2, int(8 / amount))
        quantized = np.rint(image / 255 * (levels - 1)) / (levels - 1)
        panels = {
            "Original": image,
            f"Quantized to {levels} levels": quantized,
            "Quantization absolute error": np.abs(image / 255 - quantized).mean(2),
        }
        metrics = {"mse": float(np.mean((image / 255 - quantized) ** 2)), "levels": levels}
    else:
        reduced = cv2.resize(image, (16, 16), interpolation=cv2.INTER_AREA)
        restored = cv2.resize(reduced, (96, 96), interpolation=cv2.INTER_NEAREST)
        alpha = np.linspace(0, 1, 96)[None, :, None]
        composite = (image * alpha + 255 * (1 - alpha)).astype(np.uint8)
        panels = {
            "Low-resolution resampling": restored,
            "Alpha on white": composite,
            "HWC to CHW back": image.transpose(2, 0, 1).transpose(1, 2, 0),
        }
        metrics = {"tensor_chw_shape": list(image.transpose(2, 0, 1).shape)}
    return Result("03 · Pixels, sampling and representation", panels, metrics=metrics)


def opencv_basics(lesson, seed, amount):
    image = picture(seed)
    drawn = image.copy()
    cv2.rectangle(drawn, (7, 7), (65, 55), (255, 255, 0), 2)
    cv2.putText(drawn, "CV", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    with TemporaryDirectory() as directory:
        path = Path(directory) / "roundtrip.png"
        ok = cv2.imwrite(str(path), cv2.cvtColor(drawn, cv2.COLOR_RGB2BGR))
        bgr = cv2.imread(str(path))
        if not ok or bgr is None:
            raise RuntimeError("PNG encoder/decoder failed.")
        restored = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    panels = {
        "Drawing primitives": drawn,
        "BGR viewed as RGB (wrong)": bgr,
        "PNG round trip RGB": restored,
    }
    if lesson == 1:
        panels["Resized interpolation"] = cv2.resize(drawn, (48, 48), interpolation=cv2.INTER_AREA)
    if lesson == 2:
        panels["Simulated slider threshold"] = (n.gray(image) > 100 * amount).astype(np.uint8)
    return Result(
        "04 · OpenCV input, drawing and interaction contracts",
        panels,
        metrics={"lossless_equal": bool(np.array_equal(drawn, restored))},
        notes="The GUI and webcam adapters are separate scripts; this CPU lab uses no camera.",
    )


def filtering(lesson, seed, amount):
    clean = n.gray(picture(seed)) / 255
    rng = np.random.default_rng(seed)
    if lesson == 1:
        noisy = clean.copy()
        noise = rng.random(clean.shape)
        noisy[noise < 0.04 * amount] = 0
        noisy[noise > 1 - 0.04 * amount] = 1
        output = median_filter(noisy, size=3)
        comparison = cv2.medianBlur((noisy * 255).astype(np.uint8), 3) / 255
    else:
        noisy = np.clip(clean + rng.normal(0, 0.08 * amount, clean.shape), 0, 1)
        kernel = n.gaussian_kernel(5, 1 if lesson == 0 else 1.7)
        output = n.correlate(noisy, kernel)
        comparison = cv2.filter2D(noisy, -1, kernel, borderType=cv2.BORDER_REPLICATE)
    return Result(
        "05 · Noise and local filtering",
        {
            "Clean": clean,
            "Noisy": noisy,
            "Reference output": output,
            "OpenCV comparison": comparison,
        },
        metrics={
            "noisy_mse": float(np.mean((clean - noisy) ** 2)),
            "filtered_mse": float(np.mean((clean - output) ** 2)),
            "library_max_error": float(np.max(np.abs(output - comparison))),
        },
    )


def enhancement(lesson, seed, amount):
    image = (n.gray(picture(seed)) * 0.3 + 70).astype(np.uint8)
    if lesson == 0:
        output = n.equalize(image)
        other = cv2.equalizeHist(image)
        label = "Histogram equalization"
    elif lesson == 1:
        output = cv2.createCLAHE(clipLimit=2 * amount, tileGridSize=(4, 4)).apply(image)
        other = n.equalize(image)
        label = "CLAHE"
    else:
        output = np.rint(255 * (image / 255) ** amount).astype(np.uint8)
        other = np.clip(
            image.astype(float) + 0.8 * (image - cv2.GaussianBlur(image, (5, 5), 1).astype(float)),
            0,
            255,
        ).astype(np.uint8)
        label = "Gamma correction"
    return Result(
        "06 · Enhancement and lost information",
        {"Low contrast input": image, label: output, "Comparison": other},
        curves={
            "Input histogram": np.bincount(image.ravel(), minlength=256),
            "Output histogram": np.bincount(output.ravel(), minlength=256),
        },
        metrics={"input_std": float(image.std()), "output_std": float(output.std())},
        notes="Contrast spread is descriptive, not a perceptual quality score.",
    )


def transformations(lesson, seed, amount):
    image = picture(seed)
    if lesson == 0:
        matrix = np.float32([[1, 0, 8 * amount], [0, 1, 5]])
        output = cv2.warpAffine(image, matrix, (96, 96))
        return Result(
            "07 · Translation and interpolation",
            {"Input": image, "Warped": output, "Flip": image[:, ::-1]},
            metrics={"translation_x_px": 8 * amount},
        )
    source = np.float32([[5, 5], [85, 8], [83, 82], [10, 87]])
    target = np.float32([[10, 10], [80, 10], [80, 80], [10, 80]])
    h = fit_homography(source, target)
    output = cv2.warpPerspective(image, h, (96, 96))
    if lesson == 2:
        output = cv2.warpAffine(
            image,
            cv2.getRotationMatrix2D((48, 48), 15 * amount, 1),
            (96, 96),
            flags=cv2.INTER_LINEAR,
        )
    error = np.linalg.norm(apply_homography(source, h) - target, axis=1).mean()
    return Result(
        "07 · Homogeneous coordinates and perspective",
        {"Input": image, "Warped output": output, "Homography coefficients": h},
        metrics={"point_reprojection_error_px": float(error)},
    )


def colors(lesson, seed, amount):
    image = picture(seed)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(
        hsv,
        np.array([0, 100, 70], np.uint8),
        np.array([min(25, int(10 * amount)), 255, 255], np.uint8),
    )
    mask |= cv2.inRange(
        hsv, np.array([170, 100, 70], np.uint8), np.array([179, 255, 255], np.uint8)
    )
    space = cv2.cvtColor(image, cv2.COLOR_RGB2LAB if lesson == 1 else cv2.COLOR_RGB2YCrCb)
    return Result(
        "08 · Color spaces and red hue wraparound",
        {
            "RGB": image,
            "Hue (OpenCV 0–179)": hsv[..., 0],
            "Mask": mask,
            "Isolated object": np.where(mask[..., None] > 0, image, 0),
            "LAB or YCrCb first channel": space[..., 0],
        },
        metrics={"selected_fraction": float((mask > 0).mean())},
        notes="HSV thresholds depend on lighting. Color alone is not a reliable skin or identity classifier.",
    )


def features(lesson, seed, amount):
    image = picture(seed)
    grayscale = n.gray(image).astype(np.uint8)
    response = n.harris(grayscale)
    view = image.copy()
    if lesson == 0:
        threshold = response.max() * 0.1 * amount
        peaks = (response == cv2.dilate(response, np.ones((5, 5)))) & (response > threshold)
        view[peaks] = [255, 255, 255]
        count = int(peaks.sum())
    elif lesson == 1:
        points = cv2.goodFeaturesToTrack(grayscale, 50, 0.02 * amount, 5)
        count = 0 if points is None else len(points)
        for point in [] if points is None else points:
            cv2.circle(view, tuple(point.ravel().astype(int)), 2, (255, 255, 255), 1)
    else:
        points = cv2.FastFeatureDetector_create(threshold=max(2, int(12 * amount))).detect(
            grayscale
        )
        view = cv2.drawKeypoints(view, points, None, color=(255, 255, 255))
        count = len(points)
    return Result(
        "09 · Repeatable corners and detector responses",
        {"Image": image, "Harris response": response, "Detected locations": view},
        metrics={"feature_count": count},
    )


def matching(lesson, seed, amount):
    rng = np.random.default_rng(seed)
    first = rng.integers(0, 256, (128, 128), dtype=np.uint8)
    first = cv2.GaussianBlur(first, (3, 3), 0)
    true_h = np.array([[1, 0, 6], [0, 1, 4], [0, 0, 1.0]], float)
    second = cv2.warpPerspective(first, true_h, (128, 128))
    detector = (
        cv2.SIFT_create(nfeatures=300)
        if lesson == 1
        else cv2.ORB_create(nfeatures=300, edgeThreshold=8, fastThreshold=5)
    )
    kp1, d1 = detector.detectAndCompute(first, None)
    kp2, d2 = detector.detectAndCompute(second, None)
    norm = cv2.NORM_L2 if lesson == 1 else cv2.NORM_HAMMING
    pairs = cv2.BFMatcher(norm).knnMatch(d1, d2, k=2)
    good = [
        pair[0]
        for pair in pairs
        if len(pair) == 2 and pair[0].distance < min(0.95, 0.75 * amount) * pair[1].distance
    ]
    view = cv2.drawMatches(first, kp1, second, kp2, good[:30], None, flags=2)
    metrics = {"ratio_test_matches": len(good)}
    if len(good) >= 4:
        a = np.float32([kp1[m.queryIdx].pt for m in good])
        b = np.float32([kp2[m.trainIdx].pt for m in good])
        estimated, inliers = cv2.findHomography(a, b, cv2.RANSAC, 2.0)
        if estimated is not None:
            metrics["ransac_inliers"] = int(inliers.sum())
            metrics["translation_error_px"] = float(
                np.linalg.norm(estimated[:2, 2] - true_h[:2, 2])
            )
    return Result(
        "10 · Descriptors, ratio test and RANSAC",
        {"First": first, "Transformed": second, "Matches": cv2.cvtColor(view, cv2.COLOR_BGR2RGB)},
        metrics=metrics,
        notes="Known synthetic translation supplies geometric ground truth; repetitive real scenes can remain ambiguous.",
    )


def morphology_lab(lesson, seed, amount):
    mask = shapes() > 0
    rng = np.random.default_rng(seed)
    noisy = mask.copy()
    noise = rng.random(mask.shape)
    noisy[noise < 0.02 * amount] = True
    noisy[noise > 1 - 0.02 * amount] = False
    eroded = n.morphology(noisy, 3, "erode")
    dilated = n.morphology(noisy, 3, "dilate")
    output = n.morphology(eroded, 3, "dilate") if lesson == 0 else n.morphology(dilated, 3, "erode")
    if lesson == 2:
        output = dilated & ~eroded
    return Result(
        "11 · Morphology and structuring elements",
        {
            "Clean mask": mask,
            "Noise": noisy,
            "Erosion": eroded,
            "Dilation": dilated,
            "Opening / closing / gradient": output,
        },
        metrics={"foreground_before": int(noisy.sum()), "foreground_after": int(output.sum())},
    )


def contours(lesson, seed, amount):
    mask = shapes()
    view = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    outlines, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    vertices = []
    for contour in outlines:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * amount * perimeter, True)
        areas.append(float(area))
        vertices.append(len(approx))
        if lesson == 0:
            cv2.drawContours(view, [approx], -1, (255, 80, 30), 2)
        elif lesson == 1:
            box = np.int32(cv2.boxPoints(cv2.minAreaRect(contour)))
            cv2.drawContours(view, [box], -1, (255, 80, 30), 1)
        else:
            cv2.drawContours(view, [cv2.convexHull(contour)], -1, (255, 80, 30), 2)
    return Result(
        "12 · Contour area, perimeter and shape approximation",
        {"Binary shapes": mask, "Measured boundaries": view},
        metrics={"contour_count": len(outlines), "areas_px2": areas, "polygon_vertices": vertices},
        notes="Contour polygon area differs from the count of foreground pixels; no physical length is known without calibration.",
    )


def edges(lesson, seed, amount):
    image = n.gray(picture(seed))
    gx, gy, magnitude = n.sobel(image)
    ref = n.canny_reference(image, low=0.08 * amount, high=0.2 * amount)
    lib = cv2.Canny(image.astype(np.uint8), 50 * amount, 120 * amount)
    if lesson == 1:
        lib = cv2.Laplacian(image, cv2.CV_64F)
    if lesson == 2:
        lib = cv2.Scharr(image, cv2.CV_64F, 1, 0)
    return Result(
        "13 · Gradients, thinning and hysteresis",
        {
            "Input": image,
            "Horizontal derivative": gx,
            "Vertical derivative": gy,
            "Magnitude": magnitude,
            "Reference Canny": ref,
            "OpenCV comparison": lib,
        },
        metrics={"reference_edge_pixels": int(ref.sum())},
        notes="Simplified Canny uses four quantized directions and relative thresholds; it is not bit-identical to OpenCV Canny.",
    )


def segmentation(lesson, seed, amount):
    image = picture(seed)
    if lesson == 0:
        g = n.gray(image).astype(np.uint8)
        threshold, mask = n.otsu(g)
        lib, _ = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return Result(
            "14 · Global and adaptive thresholding",
            {
                "Input": g,
                "Otsu mask": mask,
                "Adaptive threshold": cv2.adaptiveThreshold(
                    g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5
                ),
            },
            metrics={"reference_threshold": threshold, "opencv_threshold": float(lib)},
        )
    if lesson == 1:
        labels, centers = n.kmeans(image.reshape(-1, 3) / 255, k=max(2, int(3 * amount)), seed=seed)
        return Result(
            "14 · K-means region assignment",
            {
                "RGB": image,
                "Cluster map": labels.reshape(image.shape[:2]),
                "Reconstructed colors": centers[labels].reshape(image.shape),
            },
            metrics={"clusters": len(centers)},
        )
    labels, count = n.components(shapes() > 0)
    return Result(
        "14 · Connected components",
        {"Binary input": shapes(), "4-connected labels": labels},
        metrics={"objects": count},
    )


def video_frames(count=16):
    for index in range(count):
        image = np.zeros((80, 112, 3), np.uint8)
        cv2.circle(image, (12 + index * 4, 40), 7, (240, 80, 30), -1)
        yield image


def video(lesson, seed, amount):
    frames = list(video_frames())
    differences = [cv2.absdiff(a, b) for a, b in zip(frames[:-1], frames[1:])]
    if lesson == 0:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "generated.avi"
            writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"MJPG"), 10.0, (112, 80))
            if not writer.isOpened():
                raise RuntimeError("MJPG video writer unavailable on this OpenCV build.")
            for frame in frames:
                writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            writer.release()
            capture = cv2.VideoCapture(str(path))
            decoded = 0
            while True:
                ok, _ = capture.read()
                if not ok:
                    break
                decoded += 1
            capture.release()
        metric = {"written_frames": len(frames), "decoded_frames": decoded, "nominal_fps": 10.0}
    else:
        metric = {
            "frame_count": len(frames),
            "sample_interval_s": 0.1,
            "difference_energy": float(np.mean(differences)),
        }
    return Result(
        "15 · Frames, codecs and timestamps",
        {"First": frames[0], "Last": frames[-1], "Frame difference": differences[-1]},
        metrics=metric,
        notes="Nominal playback FPS describes the generated video, not measured processing throughput.",
    )


def calibration(lesson, seed, amount):
    rng = np.random.default_rng(seed)
    board = np.zeros((6 * 7, 3), np.float32)
    board[:, :2] = np.mgrid[:7, :6].T.reshape(-1, 2) * 0.03
    true_k = np.array([[300.0, 0, 160], [0, 305, 120], [0, 0, 1.0]])
    objects = []
    images = []
    for index in range(10):
        rvec = np.array([0.1 + index * 0.025, 0.15 * np.sin(index), 0.04 * index])
        tvec = np.array([-0.09 + 0.01 * np.cos(index), -0.08, 0.65 + index * 0.025])
        projected, _ = cv2.projectPoints(board, rvec, tvec, true_k, np.zeros(5))
        projected += rng.normal(0, 0.1 * amount, projected.shape)
        objects.append(board)
        images.append(projected.astype(np.float32))
    rms, k, dist, _, _ = cv2.calibrateCamera(objects, images, (320, 240), None, None)
    canvas = np.zeros((240, 320, 3), np.uint8)
    for x, y in images[0].reshape(-1, 2):
        cv2.circle(canvas, (int(x), int(y)), 2, (100, 230, 160), -1)
    return Result(
        "16 · Pinhole camera calibration from multiple views",
        {
            "One projected chessboard view": canvas,
            "True intrinsics": true_k,
            "Estimated intrinsics": k,
        },
        metrics={
            "reprojection_rms_px": float(rms),
            "focal_relative_error": float(abs(k[0, 0] - 300) / 300),
            "view_count": 10,
        },
        notes="Known synthetic camera; real calibration needs diverse board orientations, an actual square size and held-out reprojection checks.",
    )


def motion(lesson, seed, amount):
    frames = list(video_frames())
    background = np.zeros(frames[0].shape, np.float32)
    model = cv2.createBackgroundSubtractorMOG2(
        history=20, varThreshold=16 * amount, detectShadows=False
    )
    energy = []
    for frame in frames:
        mask = model.apply(frame)
        difference = np.abs(frame.astype(float) - background).mean(2) > 20
        background = 0.95 * background + 0.05 * frame
        energy.append(int(difference.sum()))
    return Result(
        "17 · Motion masks and adaptive background",
        {
            "Current frame": frames[-1],
            "Running-mean foreground": difference,
            "MOG2 foreground": mask,
            "Adjacent difference": cv2.absdiff(frames[-1], frames[-2]),
        },
        curves={"Foreground pixels per frame": energy},
        metrics={"last_foreground_pixels": energy[-1]},
        notes="Camera motion and shadows violate a stationary-background assumption. Motion is not a semantic object label.",
    )


def single_tracking(lesson, seed, amount):
    rng = np.random.default_rng(seed)
    truth = np.c_[np.arange(20) * 3 + 10, np.ones(20) * 40]
    measurements = truth + rng.normal(0, 2 * amount, truth.shape)
    tracker = KalmanTracker()
    estimates = []
    for index, measurement in enumerate(measurements):
        detection = [] if lesson == 2 and 8 <= index <= 10 else [measurement]
        tracks = tracker.update(detection)
        estimates.append(tracks[0].state[:2].copy())
    estimates = np.array(estimates)
    return Result(
        "18 · State prediction, updates and short occlusion",
        curves={
            "True x": truth[:, 0],
            "Measured x": measurements[:, 0],
            "Tracked x": estimates[:, 0],
        },
        panels={"XY trajectory": np.vstack([truth[:, 0], measurements[:, 0], estimates[:, 0]])},
        metrics={
            "measurement_rmse_px": float(np.sqrt(np.mean((measurements - truth) ** 2))),
            "tracking_rmse_px": float(np.sqrt(np.mean((estimates - truth) ** 2))),
        },
    )


def faces(lesson, seed, amount):
    avatar = np.full((96, 96), 220, np.uint8)
    cv2.ellipse(avatar, (48, 48), (30, 38), 0, 0, 360, 160, -1)
    cv2.circle(avatar, (36, 37), 5, 30, -1)
    cv2.circle(avatar, (61, 37), 5, 30, -1)
    cv2.ellipse(avatar, (48, 62), (15, 7), 0, 0, 180, 30, 2)
    integral = np.pad(avatar.astype(float), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    region_sum = integral[45, 70] - integral[25, 70] - integral[45, 25] + integral[25, 25]
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if cascade.empty():
        raise FileNotFoundError("OpenCV Haar cascade data missing.")
    boxes = cascade.detectMultiScale(avatar, scaleFactor=1.1, minNeighbors=3)
    features = n.hog(avatar)
    return Result(
        "19 · Integral images, HOG and face detector limits",
        {
            "Synthetic avatar, not a photograph": avatar,
            "Integral image": integral,
            "HOG cell energy": features.sum(2),
        },
        metrics={
            "rectangle_sum_reference": float(region_sum),
            "rectangle_sum_direct": int(avatar[25:45, 25:70].sum()),
            "cascade_boxes_on_cartoon": len(boxes),
        },
        notes="A cartoon is a plumbing test, not an accuracy test for a human-face detector. Use consenting subjects for real evaluation. No identity, age, emotion or sensitive traits are inferred.",
    )


def recognition(lesson, seed, amount):
    rng = np.random.default_rng(seed)
    base = rng.normal(0, 1, (4, 64))
    train = []
    labels = []
    for identity in range(4):
        for _ in range(6):
            train.append(base[identity] + rng.normal(0, 0.15, 64))
            labels.append(identity)
    train = np.array(train)
    pca = PCA(n_components=8).fit(train)
    embeddings = pca.transform(train)
    centroids = np.array([embeddings[np.array(labels) == i].mean(0) for i in range(4)])
    query = base[1] + rng.normal(0, 0.2 * amount, 64)
    query_embedding = pca.transform(query[None])[0]
    distances = np.linalg.norm(centroids - query_embedding, axis=1)
    threshold = 2.0
    return Result(
        "20 · Embeddings, PCA and verification thresholds",
        {
            "Synthetic prototype 1": base[1].reshape(8, 8),
            "Perturbed query": query.reshape(8, 8),
            "PCA basis vector": pca.components_[0].reshape(8, 8),
        },
        curves={"Distance to each synthetic identity": distances},
        metrics={
            "nearest_synthetic_identity": int(distances.argmin()),
            "verified_with_threshold": bool(distances[1] < threshold),
            "threshold": threshold,
        },
        notes="Synthetic vectors demonstrate verification mathematics. They are not a face-recognition model or evidence of biometric accuracy.",
    )


def glyph(text):
    canvas = np.zeros((40, 30), np.uint8)
    cv2.putText(canvas, str(text), (3, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.9, 255, 2, cv2.LINE_AA)
    return canvas


def ocr(lesson, seed, amount):
    templates = [glyph(i) for i in range(10)]
    text = "2026"
    image = np.hstack([glyph(char) for char in text])
    if lesson == 1:
        image = cv2.GaussianBlur(image, (3, 3), 0.5 * amount)
    if lesson == 2:
        matrix = cv2.getRotationMatrix2D((60, 20), 3 * amount, 1)
        image = cv2.warpAffine(image, matrix, (120, 40))
    recognized = ""
    scores = []
    for index in range(4):
        patch = image[:, index * 30 : (index + 1) * 30]
        distances = [float(np.mean((patch / 255 - template / 255) ** 2)) for template in templates]
        recognized += str(np.argmin(distances))
        scores.append(min(distances))
    return Result(
        "21 · OCR preprocessing and template recognition",
        {
            "Generated text": image,
            "Thresholded": (image > 100).astype(np.uint8),
            "Digit templates": np.hstack(templates),
        },
        curves={"Character reconstruction error": scores},
        metrics={
            "recognized": recognized,
            "expected": text,
            "character_error_fraction": sum(a != b for a, b in zip(recognized, text)) / len(text),
        },
        notes="Fixed-font, fixed-spacing OCR baseline. It is not Tesseract or a deep OCR model; optional adapters process real documents.",
    )


def machine_learning(lesson, seed, amount):
    x, y = load_digits(return_X_y=True)
    train_x, test_x, train_y, test_y = train_test_split(
        x, y, test_size=0.25, stratify=y, random_state=seed
    )
    model = make_pipeline(StandardScaler(), LogisticRegression(C=amount, max_iter=400))
    model.fit(train_x, train_y)
    prediction = model.predict(test_x)
    matrix = confusion_matrix(test_y, prediction)
    return Result(
        "22 · A leakage-safe digit-classification baseline",
        {"One held-out digit": test_x[0].reshape(8, 8), "Confusion matrix (row=true)": matrix},
        metrics={
            "held_out_accuracy": float(accuracy_score(test_y, prediction)),
            "train_samples": len(train_x),
            "test_samples": len(test_x),
            "dataset": "scikit-learn packaged digits; 8x8 images",
        },
        notes="Scaler fits only the training set. This seeded held-out result is specific to this dataset and split, not a general CV accuracy claim.",
    )


FUNCTIONS = {
    2: mathematics,
    3: fundamentals,
    4: opencv_basics,
    5: filtering,
    6: enhancement,
    7: transformations,
    8: colors,
    9: features,
    10: matching,
    11: morphology_lab,
    12: contours,
    13: edges,
    14: segmentation,
    15: video,
    16: calibration,
    17: motion,
    18: single_tracking,
    19: faces,
    20: recognition,
    21: ocr,
    22: machine_learning,
}
