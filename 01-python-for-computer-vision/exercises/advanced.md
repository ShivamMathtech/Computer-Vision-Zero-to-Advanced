# Level 3 — Advanced foundations

“Advanced” here means deeper use of Chapter 01, not neural networks that have not been taught yet.

1. **Small editor design.** Write an editor class with a preserved original image and an `apply` method. Explain whether the object or each returned image can be mutated. Keep validation outside the plotting code.
2. **Benchmark size study.** Compare the same brightness operation on at least three image sizes using loops, NumPy and OpenCV. Record versions, CPU/platform, seed, warm-up, repeats and medians. Inspect output equality before interpreting timing. Do not report video FPS.
3. **Memory reasoning.** Estimate element storage for input, float conversion, intermediate and output arrays. Explain why this is still not a measured peak-process-memory result. Propose a real measurement protocol without claiming you ran it.
4. **Robust file pipeline.** Process a list of local image paths and collect successes and failures separately. Reject missing/corrupt inputs with useful messages. Preserve original files and keep each run's metadata.
5. **Numerical tolerance.** Compare your grayscale formula with OpenCV on seeded random uint8 pixels. Show the distribution of absolute differences and justify a tolerance, rather than rounding away disagreements.
6. **Reproducible experiment.** Save parameters, seed and source hashes with an output image. Re-run in a new folder and verify that pixel outputs match even if timing metadata changes.

## Completion check

Present one failure mode you found and one limitation you have not solved. Your conclusions should match the evidence, including what was not measured.
