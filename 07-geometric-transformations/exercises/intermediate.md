# Level 2 — modify an algorithm

1. Perturb one corner by two pixels and visualize the interior displacement. Compare nearest and bilinear interpolation on a checkerboard.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A homography cannot generally align a scene with multiple depths under translation. Wrong corner order can fold the page across itself.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
