# Level 2 — modify an algorithm

1. Change the foreground threshold and plot precision/recall for foreground pixels. Inspect small objects separately.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Resize categorical masks with nearest-neighbor interpolation. Bilinear interpolation creates invalid intermediate class IDs.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
