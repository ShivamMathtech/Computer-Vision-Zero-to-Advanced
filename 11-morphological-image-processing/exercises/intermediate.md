# Level 2 — modify an algorithm

1. Try a horizontal line stencil on broken text and compare it with a square stencil. Measure whether neighboring letters incorrectly merge.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Opening can delete legitimate thin lines. The structuring element size should reflect object scale, not an arbitrary constant copied from another image.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
