# Level 2 — modify an algorithm

1. Scale all landmark coordinates by two and verify that a normalized pinch ratio stays constant. Add noise and inspect click stability.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Raw pixel thresholds change with distance from the camera. Mirroring the display without adjusting coordinates reverses interaction.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
