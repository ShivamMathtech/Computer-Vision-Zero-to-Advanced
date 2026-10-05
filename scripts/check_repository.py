"""Audit local links, chapter status, notebook schemas and required teaching sections."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

import nbformat

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    "Learning Objectives",
    "Prerequisites",
    "1. Introduction",
    "2. Intuition",
    "3. Mathematical Foundation",
    "4. Visual Explanation",
    "5. Basic Implementation",
    "6. OpenCV Implementation",
    "7. From-Scratch Implementation",
    "8. Experiment",
    "9. Visualization",
    "10. Real-World Application",
    "11. Common Mistakes",
    "12. Exercises",
    "13. Challenge",
    "14. Summary",
    "15. Next Step",
]


def main() -> None:
    problems = []
    catalog = json.loads((ROOT / "docs/curriculum.json").read_text())
    assert [c["number"] for c in catalog["chapters"]] == list(range(1, 54))
    for chapter in catalog["chapters"]:
        folder = ROOT / chapter["folder"]
        if not (folder / "README.md").is_file():
            problems.append(f"Missing chapter README: {folder.name}")
        if chapter["status"] not in {"planned", "in_validation", "complete"}:
            problems.append(f"Unknown status: {folder.name}")
        if any(p >= chapter["number"] for p in chapter["prerequisites"]):
            problems.append(f"Forward prerequisite: {folder.name}")
        if chapter["status"] in {"complete", "in_validation"}:
            for name in (
                "theory/concepts.md",
                "src/implementations.py",
                "exercises/beginner.md",
                "exercises/intermediate.md",
                "exercises/advanced.md",
                "exercises/challenge.md",
                "mini-project/README.md",
                "assets/README.md",
            ):
                if not (folder / name).is_file():
                    problems.append(f"Missing delivered file: {folder.name}/{name}")
            notebooks = sorted((folder / "notebooks").glob("*.ipynb"))
            if len(notebooks) < 3:
                problems.append(f"Need at least three focused notebooks: {folder.name}")
            for path in notebooks:
                notebook = nbformat.read(path, as_version=4)
                nbformat.validate(notebook)
                prose = "\n".join(c.source for c in notebook.cells if c.cell_type == "markdown")
                for section in SECTIONS:
                    if f"## {section}" not in prose:
                        problems.append(f"{path.name}: missing {section}")
    for path in ROOT.rglob("*.md"):
        if any(p in {"artifacts", "build", ".venv", "dist"} for p in path.parts):
            continue
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            destination = unquote(target.split("#", 1)[0])
            if destination and not (path.parent / destination).exists():
                problems.append(f"Broken relative link: {path.relative_to(ROOT)} -> {target}")
    if problems:
        raise SystemExit("\n".join(problems))
    print("PASS: 53 chapter specifications, delivered structures, notebook schemas and local links")


if __name__ == "__main__":
    main()
