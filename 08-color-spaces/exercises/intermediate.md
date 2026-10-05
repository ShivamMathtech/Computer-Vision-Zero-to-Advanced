# Level 2 — modify an algorithm

1. Lower saturation while keeping hue fixed and observe the reliability of the red mask. Test two illuminations with the same object.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Using hue degrees 0–360 directly on OpenCV uint8 HSV produces incorrect thresholds. Skin color is not a reliable substitute for a trained hand detector.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
