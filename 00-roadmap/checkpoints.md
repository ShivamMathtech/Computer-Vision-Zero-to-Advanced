# Learning checkpoints

Every checkpoint has five verbs: **explain, implement, modify, debug, apply**. Record evidence in your experiment journal. These are intended milestones; only the first chapter's material is currently shipped.

| After | Explain | Implement | Modify | Debug | Apply |
| --- | --- | --- | --- | --- | --- |
| 01 | Shape, dtype, RGB, indexing | A clipped brightness function | Channel gains and crop bounds | Overflow, BGR confusion and views | Pixel Lab on a new image |
| 08 | Kernels, noise and color models | A simple filter and transform | Thresholds, kernels and interpolation | Borders and illumination failures | Restoration or color isolation |
| 14 | Features, edges, masks and contours | Matching and mask cleanup | Match rejection and morphology | Outliers and merged regions | Document measurement |
| 21 | Streams, geometry, motion and OCR | A timestamped camera pipeline | Association and preprocessing | Dropped frames and skew | An offline video or OCR tool |
| 26 | Splits, losses, gradients and transfer | Training and validation loops | Learning rate and frozen layers | Leakage and overfitting | A held-out classifier study |
| 36 | Boxes, masks, joints and identities | Detection and tracking evaluation | Thresholds and temporal windows | Identity switches and false positives | A scene analytics project |
| 43 | Attention, representations and generation | A small controlled learning experiment | Augmentations or conditioning | Collapse and prompt sensitivity | Retrieval or generative study |
| 48 | Frames, projection, depth and radiance | Triangulation and back-projection | Baseline or camera poses | Scale and calibration errors | Synthetic 3D reconstruction |
| 53 | Latency, serving, drift and monitoring | A versioned deployable pipeline | Queues and device configuration | Backpressure and model regressions | Final capstone with evaluation |

To pass Chapter 01, explain a saved output to another learner without reading the code. Reproduce it from a fresh kernel, then change one parameter and predict the effect before executing. A plot alone is not an explanation.
