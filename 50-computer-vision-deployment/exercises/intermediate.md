# Level 2 — modify an algorithm

1. Send invalid images, duplicate IDs and oversized dimensions. Verify status codes and that failed requests do not create stored events.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: In-memory session state is not shared across server processes. Multiple workers need a deliberate state partitioning or external-state design.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
