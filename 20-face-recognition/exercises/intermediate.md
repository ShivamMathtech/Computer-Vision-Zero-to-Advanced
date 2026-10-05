# Level 2 — modify an algorithm

1. Add unknown synthetic identities and sweep the threshold. Plot false acceptance and false rejection rather than only closed-set accuracy.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Selecting the threshold on the test set leaks evaluation information. Good synthetic cluster separation is not evidence of biometric performance.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
