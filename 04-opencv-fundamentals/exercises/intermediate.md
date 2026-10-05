# Level 2 — modify an algorithm

1. Save the same RGB image as PNG and JPEG, reload both, and measure the maximum absolute difference after casting to signed integers.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: cv2.imread returns None on many failures. A missing camera or display is an environmental condition, not evidence that the vision algorithm is wrong.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
