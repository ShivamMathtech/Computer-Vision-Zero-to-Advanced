# Level 2 — modify an algorithm

1. Reduce the baseline while holding pixel noise fixed and measure how 3D error changes. Include points at several depths.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Low reprojection error alone does not fix scale or guarantee accurate depth. Mixing left-handed and right-handed frames can mirror a reconstruction.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
