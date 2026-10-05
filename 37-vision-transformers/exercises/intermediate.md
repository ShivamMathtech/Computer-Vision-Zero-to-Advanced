# Level 2 — modify an algorithm

1. Double the number of tokens and estimate attention-matrix growth before measuring memory. Compare the tiny CNN and ViT on the same synthetic split.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Reshape cannot replace a correct patch permutation. Pretrained position embeddings may need resizing when image resolution changes.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
