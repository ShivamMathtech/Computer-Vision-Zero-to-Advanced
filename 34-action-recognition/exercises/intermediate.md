# Level 2 — modify an algorithm

1. Reverse each test sequence and check whether the predicted direction changes. Shuffle frame order and measure the damage.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A model may recognize the background or actor instead of the action. Random clip splitting can make evaluation misleadingly easy.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
