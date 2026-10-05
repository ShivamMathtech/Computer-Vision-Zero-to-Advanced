# Contributing

Start with a small, reproducible issue or a focused improvement to a chapter. This is a sequential curriculum: do not submit a high-level model demonstration that assumes unexplained concepts.

## Local workflow

1. Create a branch in your own checkout and install `python -m pip install -r requirements-dev.txt`.
2. Copy the chapter, notebook and project templates in `docs/templates/`.
3. Explain a concept with a familiar analogy, a numerical example and a runnable implementation before using a library shortcut.
4. Use deterministic synthetic data first; document external data licenses and consent separately.
5. Add tests for meaningful properties, error cases or numerical comparisons. Do not test only that a function exists.
6. Run `python -m ruff check .`, `python -m ruff format --check .`, `python -m pytest -q`, `python scripts/check_repository.py` and `python scripts/validate_full_course.py --jobs 4`.
7. Inspect plots, labels, math and notebook outputs. Strip personal paths, tokens, private images and unrelated data from your contribution.
8. Update `docs/curriculum.json`, `docs/PROGRESS.md` and `CHANGELOG.md` only after the chapter completion gate passes.

## Pull request evidence

State the learner problem, prerequisites, changes, exact commands executed and any untested environment. Report measured results with hardware, versions, data and protocol. Expected output must be explicitly labeled. Never fabricate accuracy, FPS or a dataset evaluation.

Keep notebooks focused; put reusable code under `src/cvzero/`. Chapter `src/implementations.py` files are teaching entry points and may re-export shared implementations. Avoid duplicated algorithms. Use RGB at public boundaries and convert to BGR only for an OpenCV operation that requires it.

## Editorial review

Ask a reviewer to explain the lesson back in their own words. Every important equation needs symbols, intuition, a worked number, Python and an application. Challenges have acceptance criteria but no immediately adjacent solution. See `docs/chapter-completion-checklist.md`.

## Data and ownership

Submit work you may share. Include primary-source references. Do not commit large datasets, model weights, personal identifiers or copied textbook pages. A model or dataset's license is separate from this repository's MIT license.
