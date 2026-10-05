# Level 2 — modify an algorithm

1. Process every second frame and compare trajectory displacement per processed frame with displacement per second.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: VideoCapture.read returning false can mean end-of-stream or failure. Writing frames of the wrong shape may silently produce a broken video.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
