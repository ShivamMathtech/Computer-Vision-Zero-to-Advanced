"""Train TinyCNN, export ONNX and measure CPU output agreement on a held-out batch."""

import argparse
import json
from pathlib import Path

import numpy as np
import onnx
import onnxruntime as ort
import torch

from cvzero.course.models import classification_experiment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("Use a new or empty output folder.")
    args.output.mkdir(parents=True, exist_ok=True)
    model, loss, x, y, _ = classification_experiment(42, epochs=3)
    example = x[:1]
    path = args.output / "classifier.onnx"
    # Explicit legacy exporter for broad supported CPU environments. The current
    # recommended dynamo exporter also requires onnxscript; see deployment notes.
    torch.onnx.export(
        model,
        example,
        str(path),
        input_names=["image"],
        output_names=["logits"],
        opset_version=17,
        dynamo=False,
        dynamic_axes={"image": {0: "batch"}, "logits": {0: "batch"}},
    )
    onnx.checker.check_model(str(path))
    session = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
    with torch.no_grad():
        expected = model(x).numpy()
    actual = session.run(None, {"image": x.numpy()})[0]
    error = float(np.abs(actual - expected).max())
    np.testing.assert_allclose(actual, expected, rtol=1e-4, atol=1e-5)
    report = {
        "seed": 42,
        "epochs": 3,
        "batch_size": 16,
        "input_shape": list(x.shape),
        "max_absolute_logit_error": error,
        "onnx_bytes": path.stat().st_size,
        "provider": session.get_providers(),
        "scope": "synthetic classification; numeric export agreement, not deployment accuracy",
    }
    (args.output / "export-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
