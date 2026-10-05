# Level 2 — modify an algorithm

1. Stop the object midway and vary adaptation rate. Measure how long it remains foreground and how long a ghost remains after it leaves.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Global lighting changes resemble motion. A binary foreground mask does not distinguish one object from two touching objects.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
