# Level 2 — modify an algorithm

1. Change blur, rotation and character spacing independently. Identify whether errors arise before or during recognition.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: A higher-resolution resize cannot restore unreadable strokes. OCR confidence is not a guarantee that a number was read correctly.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
