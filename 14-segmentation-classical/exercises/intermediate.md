# Level 2 — modify an algorithm

1. Add a lighting gradient before thresholding. Compare Otsu and adaptive masks at fixed object geometry, then inspect component counts.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Cluster zero is not automatically background. Accuracy on a mostly-background image can be high for an empty prediction.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
