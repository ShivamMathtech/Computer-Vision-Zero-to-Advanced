"""Rebuild authored chapters 02–53; content is stored separately from rendering logic.

Run before notebook validation. This overwrites generated lesson files and clears
notebook outputs. It does not regenerate Chapter 01 or validation evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat
from content_advanced import CONTENT as ADVANCED
from content_foundations import CONTENT as FOUNDATIONS
from content_learning import CONTENT as LEARNING
from research_notes import PAPERS

from cvzero.course.runner import LABS, run

ROOT = Path(__file__).resolve().parents[1]
CONTENT = {**FOUNDATIONS, **LEARNING, **ADVANCED}


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def chapter_link(chapters, number, prefix="../"):
    item = chapters[number - 1]
    return f"[{number:02d} · {item['title']}]({prefix}{item['folder']}/README.md)"


def research(number):
    if number not in PAPERS:
        return "Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation."
    title, year, url, note = PAPERS[number]
    return f"**{title} ({year}).** {note}\n\n[Read the original paper]({url}). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results."


def notebook(chapter, content, index, next_link, prerequisites):
    n = chapter["number"]
    title = content["titles"][index]
    module, name = content["scratch"].split(".")
    cells = []

    def md(value):
        cells.append(nbformat.v4.new_markdown_cell(value))

    def code(value):
        cells.append(nbformat.v4.new_code_cell(value))

    md(
        f"# {n:02d}.{index + 1} · {title}\n\nCPU · Python 3.11–3.13 · seeded teaching experiment\n\n[Open in Google Colab](https://colab.research.google.com/) — use the [ZIP setup workflow](../../docs/colab.md). No model or dataset downloads occur in this notebook."
    )
    md(
        f'## Learning Objectives\n\n- Explain {title.lower()} using the chapter\'s assumptions.\n- Translate the worked equation into Python and inspect an implementation.\n- Run, visualize and critique a reproducible experiment.\n\n## Prerequisites\n\n{prerequisites}\n\nInstall the repository before opening this notebook: `python -m pip install -e ".[notebooks,deep,api]"`. The deep/API extras are needed only by chapters that use them.'
    )
    md(
        f"## 1. Introduction\n\n{content['overview']}\n\n## 2. Intuition\n\n{content['lessons'][index]}"
    )
    code(
        "import inspect\nimport json\nimport platform\nfrom importlib.metadata import version\nimport numpy as np\nimport cv2\nfrom IPython.display import display, Code\nfrom cvzero.course.runner import run, lab_function\n\n"
        + f"CHAPTER = {n}\nLESSON = {index}\nSEED = 42\nAMOUNT = 1.0\n"
        + "print({'python': platform.python_version(), 'numpy': version('numpy'), 'opencv': cv2.__version__, 'device': 'cpu', 'seed': SEED})"
    )
    md(
        f"## 3. Mathematical Foundation\n\n$$\n{content['math']}\n$$\n\n{content['symbols']}\n\nRead the symbols aloud, predict the numerical result, and only then execute the worked example."
    )
    md(
        "## 4. Visual Explanation\n\nThe chapter preview shows an actual baseline run. Read every panel title before interpreting color or brightness; some panels show a mask, an error, or a matrix rather than a photograph.\n\n![Measured chapter baseline](../assets/lab-preview.png)"
    )
    md(
        "## 5. Basic Implementation\n\nThis small calculation isolates the equation from the larger pipeline. Change one number and predict its effect before rerunning."
    )
    code(content["example"])
    md(
        f"## 6. OpenCV Implementation\n\nThe relevant library is selected by the problem: OpenCV for image operations and geometry, scikit-learn for classical learning, PyTorch for differentiable models, and FastAPI for service contracts. OpenCV handles image arrays where it is useful; it does not supply every advanced model.\n\n{content['internals']}\n\nThe lab function below calls the actual implementation. Inspect its source to see preprocessing, fixed hyperparameters and reported metrics."
    )
    code(
        "display(Code(inspect.getsource(lab_function(CHAPTER)), language='python'))\nresult = run(CHAPTER, lesson=LESSON, seed=SEED, amount=AMOUNT)\nprint(json.dumps(result.metrics, indent=2))\nprint(result.notes)"
    )
    md(
        f"## 7. From-Scratch Implementation\n\nRead the following reusable reference implementation line by line. Identify input shapes, the main update or reduction, and the boundary/invalid-input policy. Its source lives in `src/cvzero/course/{module}.py`; notebooks reuse it so fixes apply everywhere. Optimized libraries are compared where matching behavior is meaningful."
    )
    code(
        f"from cvzero.course.{module} import {name}\ndisplay(Code(inspect.getsource({name}), language='python'))"
    )
    md(
        f"## 8. Experiment\n\n{content['experiment']}\n\nThe run configuration is defined above. `lesson` selects the chapter experiment, `seed` fixes generated data or initialization, and `amount` controls the active experiment's perturbation when supported. Consult the displayed function before changing it: a fixed mathematical example may deliberately ignore a random seed or perturbation. Keep all other settings fixed when testing one hypothesis."
    )
    code(
        "# A second independent seed checks sensitivity; fixed examples may remain identical.\nrepeat = run(CHAPTER, lesson=LESSON, seed=SEED + 1, amount=AMOUNT)\nprint(json.dumps({'baseline': result.metrics, 'second_seed': repeat.metrics}, indent=2))"
    )
    md(
        "## 9. Visualization\n\nThese figures are generated by the current run. The second plot uses the second seed. Compare the numerical report with the visible result; a single scalar rarely explains every failure."
    )
    code("display(result.plot())\ndisplay(repeat.plot())")
    md(
        f"## 10. Real-World Application\n\nThe chapter mini project is **{chapter['mini_project']}**. {chapter['outcome']}. Start with the generated data so expected geometry or labels are known, then use a separately documented real dataset. Do not transfer synthetic metrics to a real deployment claim.\n\n## 11. Common Mistakes\n\n{content['pitfall']}\n\nCheck shape, dtype, units, split and coordinate conventions before tuning an algorithm."
    )
    md(
        f"## 12. Exercises\n\n- **Easy:** Reproduce the worked numerical example by hand and add a second case.\n- **Medium:** {content['experiment']}\n- **Hard:** Create a failure case for one assumption stated in this lesson and propose a measurable remedy.\n\n## 13. Challenge\n\n{content['challenge']}\n\nWrite acceptance criteria before coding. No challenge solution is included beside the question."
    )
    md(
        f"## 14. Summary\n\n{content['lessons'][index]}\n\n**Checkpoint:** explain the mechanism, implement a small case, modify one parameter, debug a failure and apply it to a new example. Record evidence for all five.\n\n## 15. Next Step\n\n"
        + (
            f"Continue with **{content['titles'][index + 1]}** in this chapter."
            if index < 2
            else next_link
        )
        + f"\n\n[Primary reference]({content['reference']}) · [Chapter exercises](../exercises/beginner.md) · [Mini project](../mini-project/README.md)"
    )
    nb = nbformat.v4.new_notebook(cells=cells)
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "cvzero": {
            "chapter": n,
            "lesson": index,
            "seed": 42,
            "device": "cpu",
            "data": "generated; chapter 22 uses packaged sklearn digits",
            "external_downloads": False,
        },
    }
    nbformat.validate(nb)
    return nb


def project_text(chapter, content, prefix, config_path, screenshot):
    n = chapter["number"]
    return f"""# {chapter["mini_project"]}

## Problem Statement

{content["challenge"]}

This folder includes a runnable, inspectable baseline. The open-ended extension asks you to generalize and evaluate it; the baseline is not presented as a completed real-world research result.

## Objectives

- {chapter["outcome"]}.
- Measure a declared quality criterion and inspect failure cases.
- Save configuration, plots and measured results for reproduction.

## Architecture

The entry point calls the shared chapter implementation in `{LABS[n][0]}.py`. Data generation and numeric/model code are separate from plotting and reporting. [Implementation]({prefix}src/cvzero/course/{LABS[n][0]}.py).

## System Flow

Load configuration → generate or validate data → compute prediction/transformation → evaluate → save arrays, metrics and visual report. Consult the source for the active experiment's exact steps.

## Dataset

The baseline generates its own data with seed 42; Chapter 22 uses scikit-learn's packaged digit dataset. No large data or pretrained weights are bundled. [Dataset catalog and preparation]({prefix}datasets/README.md). Use separate acquisition groups for real train, validation and test splits.

## Installation

From the repository root:

```bash
python -m pip install -e ".[notebooks,deep,api]"
```

CPU is sufficient for the baseline. Larger real-data model training can benefit from a GPU; no CUDA device is required here.

## Folder Structure

`README.md` explains the project; `config.json` defines the run; `run.py` launches it. Generated outputs contain `metrics.json`, `arrays.npz` and `result.png`. Reusable algorithms live in `src/cvzero/course/`.

## Configuration

Read `config.json` before running. It selects chapter {n}, lesson 2, seed 42 and amount 1.0. `amount` only affects a parameter when that experiment uses it; exact model, optimizer, batch size and epochs are visible in the shared source and notebook source display. [Experiment protocol]({prefix}docs/reproducibility.md).

## Training

For learned baselines, the runner performs the short CPU training experiment and reports its actual loss. For deterministic image/geometry methods, there is no training stage: choose parameters on validation examples. Checkpointed real-data classification and opt-in pretrained workflows are documented in [external workflows]({prefix}docs/external-workflows.md).

## Evaluation

{content["experiment"]}

Use the metrics' exact names and the report's scope notes. Distinguish training loss, held-out synthetic evaluation and external-dataset evaluation. Never choose a final threshold on the test set.

## Inference

```bash
python scripts/run_project.py --config {config_path} --output artifacts/{n:02d}-project-run
```

Use a new or empty output folder. For direct inference on user images with optional pretrained models, follow the external workflow instructions.

## Results

The chapter's `assets/lab-metrics.json` records a baseline run and its environment. Your run produces a fresh report. No accuracy or FPS is guaranteed; synthetic and local timing results have the scope stated in the report.

## Screenshots

![Actual baseline output]({screenshot})

## Limitations

{content["pitfall"]} The synthetic baseline is deliberately small and does not establish reliability on unobserved data, hardware or users.

## Future Improvements

Complete the problem statement on a documented real dataset, add the failure cases from the chapter, and compare one justified alternative under identical splits and compute conditions. Advanced projects should progress through tests, held-out evaluation, optimization, deployment and monitoring.

## References

- [Primary documentation or paper]({content["reference"]})
- [Reproducibility and reporting]({prefix}docs/reproducibility.md)

## Example commands

```bash
python scripts/run_project.py --config {config_path} --output artifacts/{n:02d}-seed43 --seed 43
```

## Expected output

A `Saved measured report` message and three output files: `result.png`, `metrics.json`, `arrays.npz`. The image shows the actual current run. Metric values depend on the seed, versions, algorithm and hardware; they are not fabricated sample scores.
"""


def build(assets=False):
    catalog = json.loads((ROOT / "docs/curriculum.json").read_text())
    chapters = catalog["chapters"]
    for chapter in chapters[1:]:
        n = chapter["number"]
        data = CONTENT[n]
        base = ROOT / chapter["folder"]
        for folder in ("theory", "notebooks", "src", "exercises", "mini-project", "assets"):
            (base / folder).mkdir(parents=True, exist_ok=True)
        chapter["status"] = "in_validation"
        chapter["notebooks"] = 3
        prerequisites = (
            ", ".join(chapter_link(chapters, p) for p in chapter["prerequisites"])
            or "Basic Python."
        )
        if n == 37:
            prerequisites += ". First read [38 attention primer](../38-attention-mechanisms/theory/concepts.md); return here to build ViT."
        next_link = (
            chapter_link(chapters, n + 1)
            if n < 53
            else "[Complete the capstone](../projects/capstone/README.md) and design a controlled research extension."
        )
        notebook_links = []
        for index, title in enumerate(data["titles"]):
            filename = (
                f"{index + 1:02d}_"
                + ("foundations", "mechanisms", "practical_experiments")[index]
                + ".ipynb"
            )
            nb = notebook(
                chapter,
                data,
                index,
                next_link.replace("](../", "](../../"),
                prerequisites.replace("](../", "](../../"),
            )
            nbformat.write(nb, base / "notebooks" / filename)
            notebook_links.append(f"- [{index + 1}. {title}](notebooks/{filename})")
        terms = ", ".join(chapter["topics"])
        write(
            base / "README.md",
            f"""# {n:02d} · {chapter["title"]}

**{chapter["level"]} · CPU baseline · 3 focused notebooks · no required downloads**

{data["overview"]}

## What You Will Learn

{chr(10).join("- " + t for t in data["titles"])}

## Why It Matters

{chapter["outcome"]}. {data["lessons"][0]}

## Prerequisites

{prerequisites}

## Core Concepts

{terms}. Each is introduced in the [theory notes](theory/concepts.md), runnable lab or linked continuation. The default experiments isolate the mechanics; optional pretrained workflows extend the relevant chapters.

## Mathematics

$$
{data["math"]}
$$

{data["symbols"]} A worked Python calculation is included in every notebook.

## Practical Examples

{data["internals"]}

```bash
python -m cvzero.course --chapter {n} --lesson 0 --seed 42 --output artifacts/ch{n:02d}-first-run
```

Run from the installed repository. Use `--lesson 1` and `--lesson 2` for the other experiments and a fresh output directory. The source entry point is [src/implementations.py](src/implementations.py).

## Notebooks

{chr(10).join(notebook_links)}

[Open in Google Colab](https://colab.research.google.com/) using the [repository ZIP workflow](../docs/colab.md). All default notebooks run on CPU; real model training may benefit from GPU hardware.

## Exercises

[Beginner](exercises/beginner.md) · [Intermediate](exercises/intermediate.md) · [Advanced](exercises/advanced.md) · [Challenge](exercises/challenge.md)

## Mini Project

[{chapter["mini_project"]}](mini-project/README.md) includes a runnable baseline, configuration, evaluation guidance and an open-ended extension.

## Common Mistakes

{data["pitfall"]}

Before tuning, verify shape, dtype, units and split conventions. Match border behavior and preprocessing when comparing implementations.

## Interview Questions

### Beginner Questions

What problem does {data["titles"][0].lower()} solve? Explain the worked equation without mathematical jargon.

### Intermediate Questions

{data["experiment"]} What evidence would distinguish a useful change from an accidental improvement?

### Advanced Questions

Which assumption in this chapter fails first on your intended data, and how would you measure that failure?

### Coding Questions

Reimplement the core operation on a tiny array and compare it with the shared reference. State the input and output contracts before coding.

### Conceptual Questions

{data["pitfall"]} Why can a successful function call or a plausible visualization fail to reveal this problem?

### System Design Questions

How would you turn {chapter["mini_project"]} into a service with bounded inputs, versioned configuration and monitoring? Which state must persist between frames or requests?

## Research Directions

See the [research reading notes](../docs/research-reading.md#chapter-{n:02d}) for the historical connection or an ablation proposal. Do not equate the small teaching lab with a benchmark reproduction.

## CHECKPOINT

- Explain the mechanism and its assumptions.
- Implement a small numerical case.
- Modify a parameter and predict the effect.
- Debug a failure using intermediate outputs.
- Apply the method to a new example and report its limits.

## Dataset and results

[Dataset policy](../datasets/README.md) · [Measured baseline](assets/lab-metrics.json) · [Plot](assets/lab-preview.png). Results are actual local runs with the scope recorded in the JSON. Default data are generated, except the packaged digits in Chapter 22.

## References

[Primary source]({data["reference"]}) · [Implementation and validation notes](../docs/VALIDATION.md)

## Next Chapter

{next_link}
""",
        )
        theory = f"# {chapter['title']} — concepts and mechanisms\n\n## What and why\n\n{data['overview']}\n\n"
        for i, (title, lesson) in enumerate(zip(data["titles"], data["lessons"], strict=True), 1):
            theory += f"## {i}. {title}\n\n{lesson}\n\n"
        theory += f"""## Mathematical foundation

$$
{data["math"]}
$$

{data["symbols"]}

The numerical example makes the units and reduction visible before the larger pipeline:

```python
import numpy as np
import cv2
{data["example"]}
```

## What happens internally

{data["internals"]}

Read the chapter entry point, then follow its shared source. The core reference is `{data["scratch"]}`. Separate data construction, algorithm, metric and plotting when changing the experiment.

## Visual reasoning

![Actual baseline](../assets/lab-preview.png)

Predict a change before rerunning. Explain what each axis, color, mask or matrix cell represents. In learned examples, compare a loss curve with held-out predictions; in geometry examples, compare coordinate residuals with known synthetic truth. Visual plausibility is useful evidence, but does not replace a declared metric.

## Controlled experiment

{data["experiment"]}

Write down the independent variable, what remains fixed, and the metric before changing code. Repeat stochastic experiments with multiple seeds and retain negative results. A timing comparison should include warm-up, repeat count and hardware; never compare unmatched preprocessing or data sizes.

## Applications and limits

{chapter["outcome"]}. The mini project applies the mechanism in a small runnable baseline. {data["pitfall"]}

The local generated distribution deliberately removes some real-world complexity. External data, pretrained models and hardware paths are documented separately in [external workflows](../../docs/external-workflows.md). A toy objective or synthetic score must be labeled as such when used in a portfolio.

## Exercises and checkpoint

Explain this chapter to someone using one concrete example. Then implement a tiny case, change a parameter, create a failure and apply the method to new data. Use the [three exercise levels](../exercises/beginner.md) and [challenge](../exercises/challenge.md) to record evidence.

## Research connection

[Read the chapter research note](../../docs/research-reading.md#chapter-{n:02d}). It distinguishes the original contribution, architecture intuition, limitations and alternatives from the scope of the runnable lab.

## References and next step

[Primary reference]({data["reference"]}). Continue through the chapter notebooks and mini project, then follow the next-chapter link in the [chapter README](../README.md).
"""
        write(base / "theory/concepts.md", theory)
        write(
            base / "src/implementations.py",
            f'''"""Chapter {n:02d}: public teaching entry points; algorithms are shared, not duplicated."""
from cvzero.course.{LABS[n][0]} import {LABS[n][1]} as experiment
from cvzero.course.{data["scratch"].split(".")[0]} import {data["scratch"].split(".")[1]} as reference

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
''',
        )
        write(
            base / "exercises/beginner.md",
            f"""# Level 1 — {chapter["title"]}

1. Explain `{data["titles"][0]}` using a concrete image or small array.
2. Calculate the chapter equation by hand, then implement the calculation with NumPy. Use one normal and one boundary case.
3. Run notebook 1 from a fresh kernel and describe every input and output shape.
4. Annotate the baseline visualization: what is observed, computed, predicted or assumed?

**Acceptance:** a short explanation, the two checked calculations, and a labeled figure. Use the theory after making your own prediction.
""",
        )
        write(
            base / "exercises/intermediate.md",
            f"""# Level 2 — modify an algorithm

1. {data["experiment"]}
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: {data["pitfall"]}
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
""",
        )
        write(
            base / "exercises/advanced.md",
            f"""# Level 3 — design a solution

1. Extend **{chapter["mini_project"]}** to a new input distribution.
2. Choose a metric and held-out evaluation protocol before implementing your change.
3. Replace one algorithmic assumption with a justified alternative. Compare using the same data and compute conditions.
4. Add useful handling for missing, malformed or unsupported inputs, and report the remaining limitations.

**Acceptance:** design notes, reproducible commands, an ablation table with measured results, and a failure gallery. Research-level claims require a suitable baseline and independent evaluation.
""",
        )
        write(
            base / "exercises/challenge.md",
            f"""# Challenge — {chapter["mini_project"]}

{data["challenge"]}

## Deliverables

Provide a runnable module, a configuration file, a documented dataset/split, a visual report and a short decision log. Define acceptance criteria before inspecting final test results. Include at least one failure case and explain the scope of each number.

No solution is supplied here. The mini-project baseline demonstrates the chapter mechanism; completing this broader challenge requires your own design and evaluation.
""",
        )
        config = {"chapter": n, "lesson": 2, "seed": 42, "amount": 1.0}
        write(base / "mini-project/config.json", json.dumps(config, indent=2))
        write(
            base / "mini-project/run.py",
            '"""Launch the adjacent project configuration after installing cvzero."""\nfrom pathlib import Path\nfrom cvzero.course.project import main\n\nif __name__ == "__main__":\n    main(default_config=Path(__file__).with_name("config.json"))\n',
        )
        write(
            base / "mini-project/README.md",
            project_text(
                chapter,
                data,
                "../../",
                chapter["folder"] + "/mini-project/config.json",
                "../assets/lab-preview.png",
            ),
        )
        write(
            base / "assets/README.md",
            """# Learning assets

`lab-preview.png` is rendered by an actual seeded CPU baseline. `lab-metrics.json` records its configuration, versions, metrics and scope notes. These are small generated teaching assets, not external dataset samples or benchmark claims. Recreate the current experiment with the command in the chapter README.
""",
        )
        if assets:
            result = run(n, lesson=0, seed=42)
            result.plot().savefig(base / "assets/lab-preview.png", dpi=100)
            import platform
            from importlib.metadata import version

            report = {
                "chapter": n,
                "lesson": 0,
                "seed": 42,
                "amount": 1.0,
                "device": "cpu",
                "python": platform.python_version(),
                "numpy": version("numpy"),
                "opencv": version("opencv-python-headless"),
                "metrics": result.metrics,
                "scope": result.notes or "Generated teaching data; local result only.",
                "implementation": f"src/cvzero/course/{LABS[n][0]}.py::{LABS[n][1]}",
            }
            if LABS[n][0] == "deep":
                report["torch"] = version("torch")
            write(base / "assets/lab-metrics.json", json.dumps(report, indent=2, allow_nan=False))
        print(f"Built chapter {n:02d}", flush=True)
    catalog["release"] = "1.0.0"
    write(ROOT / "docs/curriculum.json", json.dumps(catalog, indent=2))
    write(
        ROOT / "docs/research-reading.md",
        "# Research reading companion\n\nOriginal contributions, useful intuition and limitations. Publication/preprint years are stated explicitly; later revisions may have different dates.\n\n"
        + "\n\n".join(f"## Chapter {c['number']:02d}\n\n{research(c['number'])}" for c in chapters),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", action="store_true")
    build(parser.parse_args().assets)
