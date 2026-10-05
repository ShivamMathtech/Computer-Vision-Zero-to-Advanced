# Level 2 — modify an algorithm

1. Create a rare foreground class and compare unweighted loss with a documented weighting scheme. Report per-class IoU rather than only the mean.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Colorful mask visualizations are not training targets unless colors are mapped consistently to integer class IDs.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
