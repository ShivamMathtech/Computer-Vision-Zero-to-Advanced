# Roadmap: from pixels to deployed systems

Start with Chapter 01 even if your long-term goal is YOLO, transformers or generative vision. Each stage adds a tool needed by the next. The repository contains teaching material and CPU labs for every numbered chapter.

| Stage | Chapters | Competence checkpoint |
|---|---|---|
| Foundations | 01–04 | Explain image shape/dtype/channel order and build reliable I/O |
| Classical image analysis | 05–14 | Design and inspect filters, masks, features and geometric maps |
| Temporal and camera systems | 15–21 | Handle streams, calibration, tracking and OCR failure cases |
| Learned vision | 22–31 | Split data, train models and evaluate classification/detection/segmentation |
| Motion and structured outputs | 32–36 | Use landmarks, temporal features, flow and identity association |
| Representation and generation | 37–43 | Explain attention, SSL, image–text alignment and generative objectives |
| Geometry and neural scenes | 44–48 | Reconstruct points, estimate depth and understand differentiable rendering |
| Engineering and capstone | 49–53 | Measure, export, serve and monitor an integrated local system |

The directory order is stable. Read the attention primer linked from Chapter 37 before its transformer block; Chapter 38 then expands it. Chapter 38 does not require an already-trained ViT. [Detailed progression](learning-path.md) · [Prerequisites](prerequisites.md) · [Progress](../docs/PROGRESS.md).

For every stage, demonstrate that you can explain an idea, implement a small version, modify it, debug it and transfer it to a new input. Complete the stage project before treating the stage as learned; running a notebook is only the first step.
