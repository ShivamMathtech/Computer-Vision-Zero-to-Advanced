# Level 2 — modify an algorithm

1. Replace random texture with a flat patch and inspect ambiguity in the full cost curve. Add an occluder visible to only one camera.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Using raw SGBM integer output as pixels makes depth wrong by a factor of 16. Rectification does not create missing correspondence in occluded regions.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
