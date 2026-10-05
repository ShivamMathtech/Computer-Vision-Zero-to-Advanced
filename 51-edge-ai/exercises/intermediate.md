# Level 2 — modify an algorithm

1. Choose a small-object size and reduce resolution until it disappears. Compare the memory saving with the task-specific quality loss.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A smaller model file may still allocate large activations. Cold-start and thermally throttled timings answer different operational questions.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
