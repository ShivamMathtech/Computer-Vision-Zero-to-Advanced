# Level 2 — modify an algorithm

1. Add repeated tiles and increase viewpoint change. Record keypoints, accepted matches, inliers and reprojection error separately.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Drawing many lines between two images can conceal false correspondences. A low residual on a tiny cluster of points may extrapolate badly.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
