# Level 2 — modify an algorithm

1. Make sensor errors correlated and compare the theoretical confidence with observed error. Then introduce missing depth.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Concatenating arrays is not sufficient if modalities describe different times or coordinates. A high-confidence sensor can still be systematically biased.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
