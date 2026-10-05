# Level 2 — modify an algorithm

1. Add the same disparity noise at 2 m and 6 m. Compare depth MAE and explain the nonlinear difference.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A visually smooth depth map can be consistently wrong in scale. Depth Z and Euclidean range are different away from the optical axis.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
