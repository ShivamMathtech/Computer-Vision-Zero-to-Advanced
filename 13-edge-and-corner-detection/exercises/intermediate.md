# Level 2 — modify an algorithm

1. Increase noise and independently change blur scale and hysteresis thresholds. Observe missing boundaries versus false texture edges.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Edges are not closed object masks. Applying contours to a broken Canny map can produce fragmented shapes.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
