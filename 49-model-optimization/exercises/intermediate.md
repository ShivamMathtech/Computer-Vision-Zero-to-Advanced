# Level 2 — modify an algorithm

1. Quantize a weight distribution with an outlier and compare per-tensor and per-channel error. Measure the target runtime rather than extrapolating from file size.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Benchmarking a first call includes initialization. Numerically close logits can still cross a decision threshold on borderline examples.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
