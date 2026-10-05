# Level 2 — modify an algorithm

1. Introduce a brightness shift without changing object labels, then a label change without a large brightness shift. Explain which monitoring signal detects each.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: No drift alert does not imply no accuracy degradation. A dashboard full of metrics is unhelpful without thresholds, ownership and response actions.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
