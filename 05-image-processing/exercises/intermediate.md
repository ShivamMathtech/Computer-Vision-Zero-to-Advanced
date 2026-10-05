# Level 2 — modify an algorithm

1. Use equal noise seeds to compare mean, Gaussian and median filtering. Report MSE against the clean synthetic image and also inspect whether thin edges disappear.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Smoothing may lower noise while removing a real small object. Numerical equality comparisons are invalid when border modes differ.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
