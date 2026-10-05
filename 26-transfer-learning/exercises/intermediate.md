# Level 2 — modify an algorithm

1. Vary target brightness and compare frozen features with fine-tuning at two learning rates using an unchanged test set.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Replacing the head without matching the label map can silently swap class meanings. Pretraining data may overlap an evaluation set.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
