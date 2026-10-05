# Level 2 — modify an algorithm

1. Test how resizing and contrast affect a detector on a small consented evaluation set; include empty scenes and partial occlusions.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A detected box is not proof that a person is present. Cascade scores should not be treated as calibrated probabilities.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
