# Reproducibility and measurement

Every claim should identify data, code, environment, protocol and scope. This release uses seed 42 unless a notebook deliberately compares another seed. Default experiments run on CPU and do not download weights.

## Experiment manifest

Record Python/library versions, code revision or ZIP checksum, dataset source/license/version, exact split identities, model architecture, preprocessing, initialization, seed, optimizer, learning rate, batch size, epochs/steps, hardware, precision, evaluation metrics and output locations. If a field does not apply to a deterministic transform, write “not applicable”. Do not invent a GPU or training run.

The chapter notebooks print their environment and display the exact lab source, including fixed hyperparameters. `src/cvzero/course/models.py` contains reusable models and trainers. `Result.save()` writes run configuration, package versions, platform, metrics and scope to `metrics.json`; arrays and a plot are saved beside it. Static chapter assets record the seed and source function used to generate the preview. The real-data classifier writes its full configuration, class map, history and final test result.

## Default learned experiments

| Experiment | Data and model | Training convention |
|---|---|---|
| CNN/classification | Generated 24×24 shapes, TinyCNN | Independent training/test seeds; Adam; see notebook source for epochs and learning rate |
| Transfer | Locally pretrained shape CNN | Source training followed by frozen-head or full adaptation; independent target test images |
| Binary/semantic masks | Generated images and masks, TinyUNet | BCEWithLogitsLoss; held-out IoU/Dice |
| ViT | Generated shapes, one-block TinyViT | Fixed patch size and seed; held-out class predictions |
| SSL/VLM/generation | Small generated data | Objective-specific training; metrics labeled by their actual scope |
| Tiny radiance field | Analytic synthetic volume/rays | One training view; does not establish multiview reconstruction |

These are small educational experiments with settings fixed in source, not hyperparameter searches on validation data. A full study should add a validation split before selecting settings, repeat seeds, and preserve a final test set. Training loss and test accuracy are not interchangeable.

## Split integrity and uncertainty

Group related observations before splitting: adjacent video frames, the same specimen or capture session should not cross boundaries. Fit scalers and PCA on training data. Select thresholds on validation only. Report per-class or per-condition errors and appropriate uncertainty; synthetic accuracy is not evidence of real-world robustness.

## Runtime comparisons

Warm up, repeat and report a distribution. State input size, dtype, thread count, device and whether transfer/preprocessing is included. Synchronize asynchronous accelerators when timing them. Array `nbytes` measures buffer storage, not total process peak memory. A local microbenchmark is not a video FPS guarantee.

Chapter 01 compares loop, vectorized NumPy and OpenCV brightness on identical arrays. Chapter 23 compares matching NumPy/PyTorch filtering. Chapter 49 measures quantization error without pretending dequantized float multiplication is accelerated int8 inference. Chapter 51 compares resolution, local latency and edge-map agreement. Chapter 52 is a scheduling simulation, clearly labeled as such.

## Results and artifacts

Keep both success and failure examples. Never fill a README with plausible benchmark numbers. Use “Expected output” for commands not run and “Not evaluated” for external data or hardware. See [validation evidence](VALIDATION.md) and the [experiment-log template](templates/experiment-log.md).
