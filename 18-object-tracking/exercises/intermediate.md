# Level 2 — modify an algorithm

1. Increase measurement noise and insert a short occlusion. Plot position error and inspect uncertainty rather than judging smoothness alone.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A smooth trajectory can still be wrong. Pixel velocity changes when FPS changes unless elapsed time is included.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
