# Repository architecture

| Location | Responsibility |
|---|---|
| `00-roadmap/` | Prerequisites, progression and section checkpoints |
| `01-…/` through `53-…/` | Chapter README, theory, focused notebooks, exercises, source entry point, mini project and assets |
| `src/cvzero/` | Installable package; original pixel operations and shared course implementations |
| `src/cvzero/course/numerics.py` | Readable NumPy algorithms and explicit backpropagation |
| `src/cvzero/course/geometry.py` | Homography, projection, triangulation, clouds and volume rendering |
| `src/cvzero/course/tracking.py` | Kalman/Hungarian tracking, heatmaps, angles and hysteresis |
| `src/cvzero/course/models.py` | Small trainable PyTorch models and training utilities |
| `src/cvzero/course/{classical,deep,spatial,engineering}.py` | Topic-specific runnable experiments |
| `src/cvzero/platform/` | Capstone API, engine, storage and dashboard |
| `projects/` | Runnable portfolio baselines, Pixel Lab and capstone |
| `datasets/` | Dataset policy and small local fixtures; large data is excluded |
| `scripts/` | Dataset preparation, optional workflows, validation and release packaging |
| `docs/templates/` | Chapter, notebook, project and experiment templates |
| `docs/PROGRESS.md` | Completion and validation evidence by chapter |

Notebook code imports reusable modules. Chapter source files re-export the relevant entry points; this keeps algorithm fixes consistent across lessons. The authored content data in `scripts/content_*.py` and `research_notes.py` can be rendered with `build_course_material.py`. Rebuilding clears generated notebook outputs, so rerun validation afterward. It does not overwrite Chapter 01.

Image-facing functions use RGB at their public boundary unless a function explicitly documents BGR. Numeric references prefer float arrays for arithmetic; file images use uint8. Camera/world geometry explicitly states units, frame direction and coordinate conventions.
