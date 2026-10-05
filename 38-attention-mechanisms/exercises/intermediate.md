# Level 2 — modify an algorithm

1. Scale query/key magnitudes and inspect whether attention becomes peaked. Apply a triangular mask and verify forbidden weights are zero.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A softmax over the wrong axis can still produce plausible array shapes. Attention weights are not automatically causal explanations of predictions.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
