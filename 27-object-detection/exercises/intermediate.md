# Level 2 — modify an algorithm

1. Raise the NMS IoU threshold and explain the effect on crowded scenes versus duplicate boxes. Keep confidence and IoU thresholds distinct.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: AP50 and COCO-style AP across IoU thresholds are not interchangeable. Coordinate off-by-one conventions matter for small objects.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
