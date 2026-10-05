# Level 2 — modify an algorithm

1. Add a visually similar distractor prompt to a candidate set and inspect score changes. Evaluate retrieval rank rather than assuming a fixed probability meaning.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A plausible caption may hallucinate objects. An embedding similarity cannot establish a person’s identity, intent or protected traits.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
