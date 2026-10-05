# Level 2 — modify an algorithm

1. Increase translation until the small-motion estimate fails, then compare with pyramidal tracking. Add a uniform brightness offset as a separate failure test.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A colorful flow image can look plausible even when magnitudes are wrong. Use endpoint error against known displacement.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
