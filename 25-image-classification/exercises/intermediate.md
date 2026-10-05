# Level 2 — modify an algorithm

1. Create a background-only class and inspect whether confidence on unknown objects falls. Compare macro and micro metrics under class imbalance.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Softmax forces scores to sum to one even for an out-of-distribution image. A confident prediction is not proof that the image belongs to a known class.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
