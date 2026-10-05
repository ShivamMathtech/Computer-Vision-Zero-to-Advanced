# Level 2 — modify an algorithm

1. Use many nearly identical front-facing board views versus varied views. Compare parameter stability, not just training reprojection error.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Chessboard dimensions count inner corners, not squares. Mixing units changes estimated translations and baseline scale.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
