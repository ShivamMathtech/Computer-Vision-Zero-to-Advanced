"""Round trips, bad input paths and a real CLI subprocess, without internet."""

import json
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

from cvzero.benchmark import benchmark_brightness
from cvzero.cli import main
from cvzero.io import load_rgb, save_rgb
from cvzero.lab import LabConfig, run_lab, transform
from cvzero.synthetic import make_scene, tiny_palette


def test_lossless_round_trip_with_unicode_path(tmp_path):
    path = tmp_path / "café image.png"
    save_rgb(path, tiny_palette())
    np.testing.assert_array_equal(load_rgb(path), tiny_palette())


def test_alpha_is_composited_on_white(tmp_path):
    path = tmp_path / "alpha.png"
    Image.fromarray(np.array([[[255, 0, 0, 0], [255, 0, 0, 255]]], dtype=np.uint8)).save(path)
    assert load_rgb(path).tolist() == [[[255, 255, 255], [255, 0, 0]]]


def test_grayscale_expands_to_three_equal_channels(tmp_path):
    path = tmp_path / "gray.png"
    Image.fromarray(np.array([[0, 255]], dtype=np.uint8)).save(path)
    assert load_rgb(path).tolist() == [[[0, 0, 0], [255, 255, 255]]]


def test_missing_corrupt_and_oversize_input(tmp_path):
    with pytest.raises(FileNotFoundError, match="Image not found"):
        load_rgb(tmp_path / "absent.png")
    corrupt = tmp_path / "corrupt.png"
    corrupt.write_text("not an image")
    with pytest.raises(ValueError, match="Cannot decode"):
        load_rgb(corrupt)
    path = save_rgb(tmp_path / "small.png", tiny_palette())
    with pytest.raises(ValueError, match="exceeds"):
        load_rgb(path, max_pixels=5)


def test_scientific_depth_is_not_silently_scaled(tmp_path):
    path = tmp_path / "depth.png"
    Image.fromarray(np.array([[1000, 65535]], dtype=np.uint16)).save(path)
    with pytest.raises(ValueError, match="Unsupported image mode"):
        load_rgb(path)


def test_lossy_output_rejected(tmp_path):
    with pytest.raises(ValueError, match=".png"):
        save_rgb(tmp_path / "lossy.jpg", tiny_palette())


def test_report_artifacts_and_safe_label(tmp_path):
    output = tmp_path / "report"
    image = make_scene(32, 48)
    result = run_lab(image, output, LabConfig(brightness=0), "<script>bad</script>")
    assert result["edited"]["width"] == 48
    assert {p.name for p in output.iterdir()} == {
        "original.png",
        "edited.png",
        "grayscale.png",
        "contact-sheet.png",
        "histograms.png",
        "summary.json",
        "report.html",
    }
    np.testing.assert_array_equal(load_rgb(output / "edited.png"), image)
    text = (output / "report.html").read_text()
    assert "<script>" not in text and "&lt;script&gt;" in text
    assert json.loads((output / "summary.json").read_text())["configuration"]["brightness"] == 0
    with pytest.raises(ValueError, match="new or empty"):
        run_lab(image, output, LabConfig())


def test_pipeline_order_with_clipping():
    image = np.array([[[250, 100, 20]]], dtype=np.uint8)
    out = transform(image, LabConfig(brightness=20, gains=(0.5, 1, 1)))
    assert out.tolist() == [[[128, 120, 40]]]


def test_cli_success_and_error_exit(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "cvzero", "doctor"],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["status"] == "ok"
    bad = subprocess.run(
        [sys.executable, "-m", "cvzero", "inspect", "missing.png"],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert bad.returncode == 2 and "Image not found" in bad.stderr


def test_cli_demo_and_edit(tmp_path, capsys):
    output = tmp_path / "demo"
    assert main(["demo", "--output", str(output)]) == 0
    assert main(["inspect", str(output / "edited.png")]) == 0
    assert (
        main(
            [
                "edit",
                str(output / "original.png"),
                "--output",
                str(tmp_path / "edit"),
                "--crop",
                "0",
                "0",
                "30",
                "20",
            ]
        )
        == 0
    )
    assert main(["demo", "--output", str(tmp_path / "bad"), "--brightness", "nan"]) == 2
    assert "finite number" in capsys.readouterr().err


def test_benchmark_records_real_samples_and_correctness():
    result = benchmark_brightness(repeats=2)
    assert result["peak_memory_measured"] is False
    assert result["shape"] == [96, 128, 3]
    for row in result["results"]:
        assert len(row["samples_ms"]) == 2
        assert row["median_ms"] >= 0
        assert row["max_absolute_pixel_error"] == 0
        assert row["input_array_bytes"] == 96 * 128 * 3


@pytest.mark.parametrize("repeats", [0, 51, True])
def test_benchmark_rejects_bad_repeat_count(repeats):
    with pytest.raises(ValueError):
        benchmark_brightness(repeats)
