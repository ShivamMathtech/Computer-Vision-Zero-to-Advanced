"""Write the release entry points from the delivered chapter catalog."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "docs/curriculum.json").read_text())
chapters = catalog["chapters"]
rows = "\n".join(
    f"| {c['number']:02d} | [{c['title']}]({c['folder']}/README.md) | {c['level']} | {4 if c['number'] == 1 else 3} |"
    for c in chapters
)
readme = f"""# Computer Vision — Zero to Advanced

**A visual learning journey from pixels to intelligent vision systems.**

Developed by **Shivam Singh · MathTech**.

![Learning journey](assets/learning-journey.png)

This release contains **all 53 chapters**, with **160 executable lesson notebooks**, theory, worked mathematics, reusable Python implementations, three exercise levels, open-ended challenges, 53 chapter mini projects and a local real-time capstone. It progresses from Python and pixels to classical CV, learning, detection, segmentation, transformers, generative vision, 3D and deployment.

The default labs use small generated datasets or packaged handwritten digits and run on CPU. Advanced labs teach real algorithms at a manageable scale. Optional workflows connect pretrained models and real datasets; their separate dependencies and validation limits are stated explicitly. This is an educational repository, not a claim of state-of-the-art benchmarks or a fully hardened commercial service.

## Start here

1. Extract this ZIP.
2. Follow the detailed [Windows/Linux/macOS setup guide](docs/setup.md).
3. Read the [roadmap](00-roadmap/README.md) and begin [Chapter 01](01-python-for-computer-vision/README.md).
4. Open the first notebook and run it from top to bottom. Do the exercises before advancing.

For an existing Python 3.12 environment:

```bash
python -m venv .venv
# Windows: use .venv\\Scripts\\python.exe in place of python below.
# Linux/macOS: source .venv/bin/activate
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e ".[notebooks,deep,api,dev,export]"
python -m jupyter lab
```

On macOS, install PyTorch using `python -m pip install torch` instead of the Linux/Windows CPU-wheel command. The setup guide gives complete environment-specific commands. Core-only study can start with `python -m pip install -e ".[notebooks]"`.

## What this repository teaches

- Arrays, images, gradual mathematical foundations, I/O and visualization.
- Filtering, enhancement, color, geometry, morphology, contours, edges and features.
- Video, calibration, motion, tracking, face-detection mechanics and OCR.
- Dataset design, metrics, explicit backpropagation, CNNs, PyTorch and transfer learning.
- Detection, YOLO workflows, binary/semantic/instance segmentation, pose, hands and actions.
- Attention, ViT, self-supervision, image–text learning, fusion, generation and diffusion.
- Projection, stereo, depth, point clouds, radiance fields, optimization and deployment.
- Reproducibility, failure analysis, latency, monitoring and model-release decisions.

## Who should use it

Beginners with basic Python, engineering students, ML newcomers, working developers, portfolio builders and research-oriented learners. No CV or advanced mathematics is assumed at the beginning. Advanced chapters require the earlier array, geometry and learning foundations.

## Prerequisites

A computer with Python, basic file navigation and willingness to experiment. CPU is enough for the default notebooks. A webcam, GPU, paid service, downloaded model or large dataset is not required. Optional real-data work has its own hardware and data requirements.

## Complete roadmap

Python → NumPy → image fundamentals → OpenCV → image processing → classical CV → machine learning → CNNs → PyTorch → detection → segmentation → tracking → attention/transformers → 3D and multimodal vision → production systems.

Read chapters sequentially. Chapter 37 includes an attention primer before the ViT implementation and points to Chapter 38 for deeper attention experiments; directory numbering follows the requested catalog. [Learning progression and checkpoints](00-roadmap/learning-path.md).

## Chapter map

| # | Chapter | Difficulty | Notebooks |
|---|---|---|---:|
{rows}

## Learning strategy

**Theory → intuition → visualization → code → experiment → exercise → mini project → real project.**

For each equation, identify symbols and units, work a small numerical example and run its Python equivalent. Change one assumption at a time. Keep an experiment journal, inspect intermediate images and preserve failure examples. At each checkpoint, explain, implement, modify, debug and apply the concept.

## Technology stack

Python, NumPy, Matplotlib, Pillow, OpenCV, SciPy and scikit-learn form the core. PyTorch powers small learned models. Optional torchvision, Ultralytics, Transformers, MediaPipe and Open3D adapters extend the same concepts. FastAPI, SQLite and a browser dashboard form the capstone; ONNX Runtime validates one export path. [Stack and dependency layers](docs/technology-stack.md).

## Projects

[Project catalog](projects/README.md): beginner tools, intermediate systems, advanced applications and research baselines. Each includes configuration, commands, data, training/evaluation guidance, inference, actual baseline visualizations, limits and extension criteria.

[Pixel Lab](projects/beginner/pixel-lab/README.md) is the introductory image editor. The [End-to-End Real-Time Platform](projects/capstone/README.md) includes an API, per-session tracking, color/shape classification, HSV segmentation, SQLite reports and a local image/video/webcam dashboard.

```bash
python -m uvicorn cvzero.platform.app:create_app --factory --host 127.0.0.1 --port 8000
```

Open [localhost:8000](http://127.0.0.1:8000) and start with its synthetic stream. The default pipeline detects colored geometry. A trained detector is an explicit optional adapter, not a hidden pretrained dependency.

## Datasets

Do not commit large datasets or model weights. [Dataset catalog](datasets/README.md) provides official sources, preparation commands, expected structures and license reminders. Default notebooks generate their inputs. The real-data workflows use documented splits and validation-only model selection.

## How to run and verify

```bash
python -m cvzero demo --output artifacts/pixel-first-run
python -m cvzero.course --chapter 13 --lesson 2 --seed 42 --output artifacts/edges-first-run
python scripts/run_project.py --config projects/research/vision-transformer/config.json --output artifacts/vit-project
python -m pytest -q
python scripts/check_repository.py
python scripts/validate_full_course.py --jobs 4
```

Use fresh output folders. The notebooks and CLI fail with useful messages for missing inputs. [Google Colab workflow](docs/colab.md) · [Optional pretrained workflows](docs/external-workflows.md).

## Validation and progress

The release includes actual notebook outputs and machine-readable evidence. [Validation report](docs/VALIDATION.md) · [Chapter progress tracker](docs/PROGRESS.md) · [Reproducibility protocol](docs/reproducibility.md). Numbers shown in executed labs describe those particular data, parameters and hardware. No external-dataset accuracy or real-time FPS is invented.

## How to contribute

Read [CONTRIBUTING](CONTRIBUTING.md), use the [chapter/notebook/project templates](docs/templates/README.md), test meaningful behavior and update validation evidence. Keep explanations gradual and reusable code outside notebooks. [Code of conduct](CODE_OF_CONDUCT.md) · [MIT license](LICENSE). Dataset and model licenses remain separate.
"""
(ROOT / "README.md").write_text(readme)
roadmap = """# Roadmap: from pixels to deployed systems

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
"""
(ROOT / "00-roadmap/README.md").write_text(roadmap)
learning = """# Learning progression

The chapter numbers are stable navigation addresses. Study in order, taking the short attention primer during Chapter 37 before its ViT implementation. Prerequisite numbers identify especially useful prior knowledge, not permission to skip the rest of the foundation.

| Chapter | Prior concepts | Learning outcome | Mini project |
|---|---|---|---|
"""
for c in chapters:
    learning += f"| [{c['number']:02d} · {c['title']}](../{c['folder']}/README.md) | {', '.join(f'{p:02d}' for p in c['prerequisites']) or 'Basic Python'} | {c['outcome']} | {c['mini_project']} |\n"
learning += """
## Section checkpoints

After 04: create and inspect an image, explain a pixel operation and handle a bad path.
After 14: implement a neighborhood operation, compare a library version and design a mask/feature pipeline.
After 21: process a sequence, explain projection and distinguish motion, identity and text recognition errors.
After 31: define splits and losses, train a small network and evaluate boxes/masks without leakage.
After 36: reason about time, missed observations, IDs and landmark uncertainty.
After 43: implement attention, distinguish representation objectives and critique generated outputs.
After 48: state coordinate frames and units, triangulate points and distinguish training-view fit from 3D reconstruction.
After 53: reproduce a result, export/check a model, run the API and explain monitoring and rollback needs.

Do not assign yourself a fixed completion speed. Use the exercises and failure analysis to determine whether to continue. Advanced external-data projects can require substantially more compute and time than the small CPU lessons.
"""
(ROOT / "00-roadmap/learning-path.md").write_text(learning)
(ROOT / "docs/NEXT_STEPS.md").write_text("""# What to do next

All 53 chapters are available. Begin at Chapter 01, work through its exercises and then continue in order. After the foundations, choose a portfolio project whose prerequisites you have completed. The capstone integrates the engineering stages.

For research, select one question from the reading companion, define an independent evaluation protocol and compare a change against a baseline. The repository supplies runnable small experiments; scientific novelty and real-world reliability must be established through your own evidence.
""")
(ROOT / "CHANGELOG.md").write_text("""# Changelog

## 1.0.0 — complete chapter coverage

Added Chapters 02–53 with theory, worked mathematics, three focused notebooks each, exercises, challenge, source entry points, generated figures and runnable mini projects. Preserved the four Chapter 01 notebooks and Pixel Lab.

Added explicit NumPy algorithms, geometric and tracking utilities, PyTorch CNN/U-Net/ViT/SSL/generative/diffusion/radiance-field labs, optional real-model workflows, portfolio baseline configurations, ONNX export/runtime validation and the local API/dashboard capstone. Added full-course notebook execution and expanded tests.

The release distinguishes small validated CPU experiments from optional pretrained/hardware workflows and does not claim benchmark reproductions.

## 0.1.0 — initial foundation

Repository architecture, roadmap, templates, project conventions and complete Python/image Chapter 01.
""")
print("Updated main README and roadmap.")
