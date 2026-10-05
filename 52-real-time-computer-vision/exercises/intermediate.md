# Level 2 — modify an algorithm

1. Compare FIFO and bounded queues under a service-time spike. Report dropped frames alongside p50 and p95 frame latency.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Reporting average FPS hides long stalls. Repeated wait calls and unbounded queues can make live results increasingly stale.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
