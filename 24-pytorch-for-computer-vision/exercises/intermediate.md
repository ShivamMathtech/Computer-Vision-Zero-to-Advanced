# Level 2 — modify an algorithm

1. Resume a training run with and without optimizer state and compare the first update after resuming. Explain why identical weights alone may not reproduce training.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Using a shuffled validation sampler does not inherently bias metrics, but applying random training augmentation can make evaluation unstable.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
