# Level 2 — modify an algorithm

1. Hold out a camera view in an extended multiview experiment and compare its error with training-view error. Inspect whether density is plausible or merely explains one view.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Low training-image loss does not prove correct 3D geometry. Ignoring background transmittance darkens empty rays.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
