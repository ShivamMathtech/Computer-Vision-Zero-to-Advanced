"""Known values, invariants and regression cases for the teaching algorithms."""

import cv2
import numpy as np
import pytest

from cvzero.images import (
    adjust_brightness,
    adjust_channels,
    brightness_loop,
    channel_histograms,
    crop_rgb,
    grayscale_loop,
    image_summary,
    require_rgb,
    rgb_to_gray,
)
from cvzero.synthetic import make_scene, tiny_palette


@pytest.mark.parametrize("delta", [-255, -30, -0.5, 0, 0.5, 20, 255])
def test_brightness_matches_scalar_reference_without_mutating(delta):
    image = make_scene(16, 24)
    before = image.copy()
    vectorized = adjust_brightness(image, delta)
    np.testing.assert_array_equal(vectorized, brightness_loop(image, delta))
    np.testing.assert_array_equal(image, before)
    assert not np.shares_memory(vectorized, image)


def test_brightness_clips_instead_of_wrapping():
    image = np.array([[[250, 10, 0], [0, 100, 255]]], dtype=np.uint8)
    assert adjust_brightness(image, 20).tolist() == [[[255, 30, 20], [20, 120, 255]]]
    assert adjust_brightness(image, -20).tolist() == [[[230, 0, 0], [0, 80, 235]]]


@pytest.mark.parametrize("delta", [float("nan"), float("inf"), -256, 256])
def test_bad_brightness_rejected(delta):
    with pytest.raises(ValueError, match="finite number"):
        adjust_brightness(tiny_palette(), delta)


def test_gain_axis_and_rounding():
    image = np.array([[[100, 80, 40], [250, 1, 3]]], dtype=np.uint8)
    assert adjust_channels(image, (2, 0.5, 0)).tolist() == [[[200, 40, 0], [255, 0, 0]]]


@pytest.mark.parametrize("gains", [(1, 2), (1, -1, 1), (1, 1, 5), (1, float("nan"), 1)])
def test_invalid_gains(gains):
    with pytest.raises(ValueError):
        adjust_channels(tiny_palette(), gains)


def test_gray_primary_colors_and_reference():
    image = tiny_palette()
    assert rgb_to_gray(image).tolist() == [[76, 150, 29], [0, 127, 255]]
    np.testing.assert_array_equal(rgb_to_gray(image), grayscale_loop(image))
    random_image = make_scene(32, 48)
    error = np.abs(
        rgb_to_gray(random_image).astype(np.int16)
        - cv2.cvtColor(random_image, cv2.COLOR_RGB2GRAY).astype(np.int16)
    )
    assert error.max() <= 1


def test_crop_shape_coordinates_and_copy():
    image = make_scene(16, 24)
    cropped = crop_rgb(image, 2, 3, 7, 8)
    assert cropped.shape == (5, 5, 3)
    np.testing.assert_array_equal(cropped[0, 0], image[3, 2])
    cropped[:] = 0
    assert image[3:8, 2:7].any()
    assert not np.shares_memory(cropped, image)


@pytest.mark.parametrize("bounds", [(-1, 0, 2, 2), (0, 0, 25, 10), (1, 2, 1, 5), (0, 5, 2, 3)])
def test_bad_crop_bounds(bounds):
    with pytest.raises(ValueError, match="Crop must"):
        crop_rgb(make_scene(16, 24), *bounds)


@pytest.mark.parametrize("bounds", [(0.5, 0, 2, 2), (True, 0, 2, 2)])
def test_noninteger_crop(bounds):
    with pytest.raises(TypeError):
        crop_rgb(make_scene(16, 24), *bounds)


@pytest.mark.parametrize(
    "image",
    [
        np.zeros((0, 3, 3), dtype=np.uint8),
        np.zeros((2, 3), dtype=np.uint8),
        np.zeros((2, 3, 4), dtype=np.uint8),
    ],
)
def test_invalid_shape(image):
    with pytest.raises(ValueError):
        require_rgb(image)


def test_type_is_explicit():
    with pytest.raises(TypeError):
        require_rgb([1, 2, 3])
    with pytest.raises(TypeError):
        require_rgb(np.zeros((2, 3, 3), dtype=float))


def test_histograms_conserve_pixel_count():
    image = tiny_palette()
    hist = channel_histograms(image)
    assert hist.shape == (3, 256)
    np.testing.assert_array_equal(hist.sum(axis=1), [6, 6, 6])
    assert hist[0, 255] == 2 and hist[0, 0] == 3 and hist[0, 127] == 1
    assert image_summary(image)["array_bytes"] == 18


def test_seed_reproducibility_and_change():
    np.testing.assert_array_equal(make_scene(seed=42), make_scene(seed=42))
    assert not np.array_equal(make_scene(seed=42), make_scene(seed=43))


@pytest.mark.parametrize("size", [0, 15, 2049, True, 16.5])
def test_bad_synthetic_size(size):
    with pytest.raises(ValueError):
        make_scene(size, 32)
