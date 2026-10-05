# Level 2 — modify an algorithm

1. Compare raw-pixel and HOG features while keeping the split fixed. Tune settings on validation data before inspecting final test results.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Fitting a scaler or PCA before splitting leaks test distribution information. Accuracy can hide poor minority-class recall.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
