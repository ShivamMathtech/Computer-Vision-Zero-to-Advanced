# Level 2 — modify an algorithm

1. Remove the activation from a multilayer network and reason about which functions remain possible. Change stride and compute output size before running.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Calling backward accumulates gradients unless they are cleared. A decreasing training loss does not prove generalization.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
