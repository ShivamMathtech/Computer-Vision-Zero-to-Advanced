# Level 2 — modify an algorithm

1. Change the gradient-descent step from 0.1 to 0.3, then derive the stability interval for the quadratic before trying a larger step.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Elementwise multiplication A*B is not matrix multiplication A@B. A low loss after one example says nothing about generalization.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
