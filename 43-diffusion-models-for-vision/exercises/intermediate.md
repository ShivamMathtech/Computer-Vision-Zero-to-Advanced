# Level 2 — modify an algorithm

1. Plot signal retention across steps and compare samples after different training budgets. Check that the final forward state is close to the assumed starting distribution.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Confusing predicted noise with a predicted clean image changes the reverse equation. A falling noise loss is not a guarantee of visually good samples.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
