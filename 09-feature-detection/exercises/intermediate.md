# Level 2 — modify an algorithm

1. Rotate and blur a checkerboard. Count repeatable detections after transforming coordinates back, rather than comparing only raw detection counts.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A high feature count is not proof of useful coverage. Border padding and threshold units influence the response.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
