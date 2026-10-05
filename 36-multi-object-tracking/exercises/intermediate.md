# Level 2 — modify an algorithm

1. Make two trajectories cross, remove observations briefly and compare the ID sequence before and after occlusion.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Track IDs are temporary anonymous identifiers, not person identities. A detector score is not a track survival probability.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
