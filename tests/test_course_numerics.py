"""Independent numeric or library oracles for reusable teaching implementations."""

import cv2
import numpy as np
import pytest
from scipy.ndimage import convolve as scipy_convolve
from scipy.ndimage import label

from cvzero.course import geometry as g
from cvzero.course import numerics as n
from cvzero.course.engineering import population_stability, quantize_symmetric, queue_simulation
from cvzero.course.tracking import KalmanTracker, count_repetitions, joint_angle


def test_correlation_and_convolution_match_independent_oracles():
    image = np.arange(35, dtype=float).reshape(5, 7)
    kernel = np.array([[1.0, 2.0, 0.0], [3.0, 0.0, -1.0], [0.0, 4.0, -2.0]])
    np.testing.assert_allclose(
        n.correlate(image, kernel), cv2.filter2D(image, -1, kernel, borderType=cv2.BORDER_REPLICATE)
    )
    np.testing.assert_allclose(
        n.convolve(image, kernel), scipy_convolve(image, kernel, mode="nearest")
    )
    assert not np.array_equal(n.correlate(image, kernel), n.convolve(image, kernel))


@pytest.mark.parametrize("size", [3, 5, 7])
def test_gaussian_and_mean_preserve_constants(size):
    image = np.full((12, 12), 7.0)
    assert np.isclose(n.gaussian_kernel(size, 1.3).sum(), 1)
    np.testing.assert_allclose(n.gaussian_filter(image, size), image)
    np.testing.assert_allclose(n.mean_filter(image, size), image)


def test_equalization_matches_opencv_and_handles_constant():
    image = np.random.default_rng(42).integers(50, 180, (31, 25), dtype="uint8")
    np.testing.assert_allclose(n.equalize(image), cv2.equalizeHist(image), atol=1)
    constant = np.full((4, 4), 83, np.uint8)
    np.testing.assert_array_equal(n.equalize(constant), constant)


@pytest.mark.parametrize("operation", ["erode", "dilate"])
def test_morphology_matches_explicit_zero_border(operation):
    mask = np.random.default_rng(42).random((14, 17)) > 0.4
    function = cv2.erode if operation == "erode" else cv2.dilate
    expected = (
        function(
            mask.astype("uint8"),
            np.ones((3, 3), np.uint8),
            borderType=cv2.BORDER_CONSTANT,
            borderValue=0,
        )
        > 0
    )
    np.testing.assert_array_equal(n.morphology(mask, operation=operation), expected)


def test_components_four_connectivity():
    mask = np.eye(4, dtype=bool)
    labels, count = n.components(mask)
    expected, num = label(mask)
    assert count == num == 4
    np.testing.assert_array_equal(labels, expected)


def test_kmeans_finds_two_separated_groups():
    values = np.array([[-4.0, 0.0], [-3.8, 0.0], [4.0, 1.0], [4.2, 1.0]])
    labels, centers = n.kmeans(values, k=2)
    assert labels[0] == labels[1] and labels[2] == labels[3] and labels[0] != labels[2]
    np.testing.assert_allclose(np.sort(centers[:, 0]), [-3.9, 4.1])


def test_canny_constant_and_step():
    assert not n.canny_reference(np.zeros((24, 24))).any()
    image = np.zeros((32, 32))
    image[:, 16:] = 255
    edges = n.canny_reference(image)
    assert edges[:, 14:18].any()
    assert not edges[:, :10].any()


def test_iou_nms_and_ap_known_values():
    boxes = np.array([[0, 0, 2, 2], [1, 1, 3, 3], [0, 0, 2, 2]])
    np.testing.assert_allclose(n.iou(boxes[0], boxes), [1, 1 / 7, 1])
    assert n.nms(boxes, [0.9, 0.7, 0.8], 0.5).tolist() == [0, 1]
    ap, precision, recall = n.average_precision([True, False, True], [0.9, 0.8, 0.7], 2)
    assert np.isclose(ap, 5 / 6)
    assert np.isclose(recall[-1], 1)
    assert len(n.nms([], [], 0.5)) == 0


def test_attention_mask_and_stability():
    q = np.eye(2)
    v = np.array([[2.0, 4.0], [6.0, 8.0]])
    output, weights = n.attention(q, q, v, np.eye(2, dtype=bool))
    np.testing.assert_allclose(output, v)
    np.testing.assert_allclose(weights.sum(1), 1)
    np.testing.assert_allclose(n.softmax([1000, 1000]), [0.5, 0.5])
    with pytest.raises(ValueError):
        n.attention(q, q, v, np.zeros((2, 2), bool))


def test_explicit_backprop_learns_a_separable_problem():
    rng = np.random.default_rng(4)
    x = np.r_[rng.normal(-1, 0.2, (10, 2)), rng.normal(1, 0.2, (10, 2))]
    y = np.r_[np.zeros(10, int), np.ones(10, int)]
    parameters, loss = n.mlp_train(x, y, steps=80)
    assert loss[-1] < loss[0] / 4
    assert (n.mlp_predict(x, parameters).argmax(1) == y).all()


def test_dlt_homography_and_triangulation():
    source = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0.4, 0.7]], float)
    h = np.array([[1, 0.1, 3], [0.2, 1, -2], [0.001, 0.002, 1]])
    target = g.apply_homography(source, h)
    fitted = g.fit_homography(source, target)
    np.testing.assert_allclose(g.apply_homography(source, fitted), target, atol=1e-10)
    points = np.array([[0.1, 0.2, 3], [0.3, -0.1, 4], [0.5, 0.3, 5]])
    p1 = np.column_stack([np.eye(3), np.zeros(3)])
    p2 = np.column_stack([np.eye(3), [-0.2, 0, 0]])
    recovered = g.triangulate(g.project(points, p1), g.project(points, p2), p1, p2)
    np.testing.assert_allclose(recovered, points, atol=1e-10)


def test_depth_invalid_and_backprojection():
    depth = g.disparity_to_depth(np.array([8, 0, -1]), 200, 0.12)
    assert depth[0] == 3 and np.isnan(depth[1:]).all()
    points = g.backproject(np.ones((2, 2)), np.eye(3))
    np.testing.assert_allclose(points, [[0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]])


def test_kabsch_returns_proper_rotation():
    source = np.random.default_rng(3).normal(size=(30, 3))
    r = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    target = source @ r.T + [1, 2, 3]
    recovered, translation = g.rigid_fit(source, target)
    np.testing.assert_allclose(source @ recovered.T + translation, target, atol=1e-10)
    assert np.isclose(np.linalg.det(recovered), 1)


def test_volume_rendering_transmittance():
    color, weights = g.volume_render(np.array([0.0, 0.0]), np.zeros((2, 3)), np.ones(2))
    np.testing.assert_allclose(color, np.ones(3))
    np.testing.assert_allclose(weights, 0)
    color, weights = g.volume_render(np.array([np.log(2)]), np.zeros((1, 3)), np.ones(1))
    np.testing.assert_allclose(color, 0.5)
    np.testing.assert_allclose(weights, 0.5)


def test_tracker_ids_survive_short_gap_and_expire():
    tracker = KalmanTracker(max_missed=2)
    identity = tracker.update([[10, 10]])[0].identity
    tracker.update([[11, 10]])
    tracker.update([])
    assert tracker.update([[13, 10]])[0].identity == identity
    tracker.update([])
    tracker.update([])
    assert tracker.update([]) == []


def test_angles_and_hysteresis():
    assert np.isclose(joint_angle(np.array([1, 0]), np.array([0, 0]), np.array([0, 1])), 90)
    assert count_repetitions([160, 155, 50, 55, 160, 158, 48, 152]) == 2
    with pytest.raises(ValueError):
        joint_angle(np.zeros(2), np.zeros(2), np.ones(2))


def test_bounded_queue_conserves_frames_and_limits_staleness():
    arrivals = np.arange(90) / 30
    bounded, dropped = queue_simulation(arrivals, 0.045, 2)
    fifo, other = queue_simulation(arrivals, 0.045, 1000)
    assert len(bounded) + dropped == 90 and other == 0
    assert dropped > 0 and np.percentile(bounded, 95) < np.percentile(fifo, 95)


def test_quantization_error_and_drift():
    weights = np.linspace(-1, 1, 100).astype("float32")
    q, scale, reconstructed = quantize_symmetric(weights)
    assert q.dtype == np.int8
    assert abs(weights - reconstructed).max() <= scale / 2 + 1e-6
    assert population_stability(weights, weights) == 0
    assert population_stability(weights, weights + 3) > 0
