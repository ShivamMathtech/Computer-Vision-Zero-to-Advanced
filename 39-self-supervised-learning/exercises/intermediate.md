# Level 2 — modify an algorithm

1. Remove an augmentation and measure downstream probe performance, not only training loss. Check embedding variance for collapse.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Two crops can remove the object and cease to be meaningful positive pairs. EMA consistency without the full method can collapse.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
