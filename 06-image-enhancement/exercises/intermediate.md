# Level 2 — modify an algorithm

1. Increase CLAHE strength on a noisy flat region and quantify both local contrast and noise variance. Find a setting that improves the downstream threshold mask.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Equalizing R, G and B independently can change hue. Clipping after sharpening discards values and can hide overshoot.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
