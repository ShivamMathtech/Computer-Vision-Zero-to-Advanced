# Level 2 — modify an algorithm

1. Inspect every generated label as an overlay, then intentionally introduce an invalid width and confirm that validation rejects it.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Training and test images from adjacent video frames can leak scene content. A synthetic regressor loss must not be advertised as YOLO mAP.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
