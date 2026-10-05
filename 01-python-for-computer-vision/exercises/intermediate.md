# Level 2 — Intermediate

Modify a working idea and predict the result before running it. Keep notes about the prediction and observation.

1. **Loop-to-array translation.** Implement channel multiplication with three loops, then NumPy broadcasting. Compare on a 16×24 synthetic image, including values that clip.
2. **Brightness sign.** Extend a positive-only brightness function to accept negative and fractional offsets. Verify black, white and half-integer boundary cases with a stated rounding rule.
3. **Crop contract.** Implement an `(x0,y0,x1,y1)` crop with exclusive stop indices. Reject an empty crop and a crop outside the image. Prove the result is an independent copy.
4. **Views versus copies.** Construct a demonstration in which a view changes its original. Rebuild it using a copy and explain the different memory relationship with `np.shares_memory`.
5. **Histogram conservation.** Compute each RGB histogram with `np.bincount`. Assert every channel's counts sum to height times width. Compare images with identical histograms but different layouts.
6. **Color boundary.** Save an RGB image, read it with `cv2.imread`, convert to RGB and compare. Explain why comparing the unconverted OpenCV result would fail.
7. **Operation order.** Apply brightness then gain, and gain then brightness. Create one image for which they disagree. Explain both arithmetic order and clipping.

## Completion check

Each experiment needs one explicit expected property, a plotted result and a short explanation of what changed. An assertion failing is useful evidence to investigate, not something to remove.
