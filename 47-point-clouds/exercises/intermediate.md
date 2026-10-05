# Level 2 — modify an algorithm

1. Increase initial rotation and partial overlap to find ICP failures. Compare point count and geometric detail at several voxel sizes.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: ICP residual can be small for an incorrect symmetric alignment. Voxel size has physical units and must match the cloud scale.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
