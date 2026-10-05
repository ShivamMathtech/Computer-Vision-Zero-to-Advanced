"""Create runnable portfolio baselines linked to the shared course implementations."""

import json
from pathlib import Path

from build_course_material import CONTENT, project_text, write

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    "beginner": [
        (
            "Image Editor",
            6,
            "Compare brightness, contrast, gamma and local enhancement with saved visual reports.",
        ),
        (
            "Color Detector",
            8,
            "Isolate a calibrated color interval and inspect its failure under low saturation.",
        ),
        (
            "Edge Detector",
            13,
            "Compare explicit Canny stages with optimized derivatives and edges.",
        ),
        (
            "Shape Detector",
            12,
            "Measure segmented shapes and distinguish geometric descriptors from category labels.",
        ),
        (
            "Motion Detector",
            17,
            "Detect changes in a generated sequence and compare background adaptation.",
        ),
        (
            "Webcam Filter",
            15,
            "Process video frames consistently and extend the tested generated stream to a local camera.",
        ),
        (
            "Document Scanner",
            7,
            "Estimate a planar warp from corners and inspect resampling artifacts.",
        ),
    ],
    "intermediate": [
        (
            "Face Detection System",
            19,
            "Run an actual cascade API and explain why a synthetic face cartoon is not a face benchmark.",
        ),
        (
            "OCR System",
            21,
            "Build a preprocessing and recognition baseline before running optional Tesseract.",
        ),
        (
            "Object Counter",
            12,
            "Count distinct segmented regions and analyze touching-object errors.",
        ),
        (
            "Vehicle Detector",
            27,
            "Understand box evaluation and connect a trained object detector for real vehicle classes.",
        ),
        (
            "Image Classifier",
            25,
            "Train and evaluate a small CNN before adapting a real ImageFolder dataset.",
        ),
        (
            "Image Stitching",
            10,
            "Find correspondences and a robust planar transform from overlapping views.",
        ),
        (
            "Camera Calibration",
            16,
            "Estimate intrinsics from multiple board views and quantify reprojection residuals.",
        ),
        (
            "Hand Gesture Controller",
            33,
            "Use scale-normalized landmarks and stable interaction states without automatic OS control.",
        ),
    ],
    "advanced": [
        (
            "YOLO Custom Detector",
            28,
            "Prepare labels, validate splits, train, evaluate, predict and export a selected YOLO model.",
        ),
        (
            "Multi-Object Tracking",
            36,
            "Associate detections to persistent temporary IDs and inspect missed-observation behavior.",
        ),
        (
            "Semantic Segmentation",
            31,
            "Train a dense foreground predictor and extend the label/loss contract to multiple classes.",
        ),
        (
            "Instance Segmentation",
            30,
            "Separate touching objects and compare classical markers with an optional learned mask model.",
        ),
        (
            "Pose Estimation",
            32,
            "Decode heatmaps, compute angles and count complete motion cycles.",
        ),
        (
            "Real-Time Surveillance Analytics",
            53,
            "Build local scene analytics with anonymous IDs and numeric event logs.",
        ),
        (
            "Industrial Defect Detection",
            26,
            "Compare frozen transfer and fine-tuning under a controlled domain shift.",
        ),
        (
            "Autonomous Vision Pipeline",
            53,
            "Integrate perception, monitoring and an API; this project contains no actuator or vehicle control.",
        ),
    ],
    "research": [
        (
            "Vision Transformer",
            37,
            "Compare patch encoders and CNNs under a declared data and compute budget.",
        ),
        (
            "Self-Supervised Vision",
            39,
            "Compare representation objectives and evaluate a frozen downstream probe.",
        ),
        (
            "Multimodal Vision",
            41,
            "Study sensor weighting, missing modalities and correlated failures.",
        ),
        (
            "3D Reconstruction",
            44,
            "Measure how baseline and correspondence noise affect triangulation.",
        ),
        (
            "Vision-Language Model",
            40,
            "Study image-text alignment and distinguish closed-vocabulary learning from pretrained retrieval.",
        ),
        (
            "Segmentation Architecture Study",
            31,
            "Use the U-Net baseline to test a clearly specified architectural hypothesis; novelty is not assumed.",
        ),
        (
            "Domain Adaptation",
            26,
            "Quantify source-to-target shift and compare adaptation strategies without test leakage.",
        ),
        (
            "Few-Shot Computer Vision",
            20,
            "Use synthetic prototypes as a few-shot nearest-embedding baseline and extend it to consented labeled classes.",
        ),
    ],
}
chapters = json.loads((ROOT / "docs/curriculum.json").read_text())["chapters"]
all_rows = []
for level, projects in PROJECTS.items():
    rows = []
    for title, number, goal in projects:
        slug = title.lower().replace(" ", "-")
        folder = ROOT / "projects" / level / slug
        chapter = dict(chapters[number - 1])
        chapter["mini_project"] = title
        chapter["outcome"] = goal.rstrip(".")
        config = {"chapter": number, "lesson": 2, "seed": 42, "amount": 1.0}
        write(folder / "config.json", json.dumps(config, indent=2))
        write(
            folder / "run.py",
            '"""Launch the configured project; shared algorithms live in cvzero.course."""\nfrom pathlib import Path\nfrom cvzero.course.project import main\n\nif __name__ == "__main__":\n    main(default_config=Path(__file__).with_name("config.json"))\n',
        )
        readme = project_text(
            chapter,
            CONTENT[number],
            "../../../",
            f"projects/{level}/{slug}/config.json",
            f"../../../{chapter['folder']}/assets/lab-preview.png",
        )
        readme += f"\n## Project-specific extension\n\n{goal}\n\nThe shipped command runs the chapter baseline. Complete the real-data extension with a documented dataset, independent evaluation and the optional adapters where appropriate. The research projects provide executable baselines and experimental protocols, not claims of new scientific results.\n"
        write(folder / "README.md", readme)
        rows.append(f"| [{title}]({slug}/README.md) | {number:02d} | {goal} |")
        all_rows.append(f"| [{title}]({level}/{slug}/README.md) | {level.title()} | {number:02d} |")
    extra = (
        "\n\n[Pixel Lab](pixel-lab/README.md) is the fully worked introductory image editor with image input and HTML reports."
        if level == "beginner"
        else ""
    )
    write(
        ROOT / "projects" / level / "README.md",
        f"# {level.title()} projects\n\nEvery project has a runnable educational baseline and a separately stated extension.\n\n| Project | Chapter | Goal |\n|---|---:|---|\n"
        + "\n".join(rows)
        + extra,
    )
write(
    ROOT / "projects/README.md",
    "# Project portfolio\n\n31 configured topic projects, the original Pixel Lab, 53 chapter mini projects and the end-to-end capstone connect the course to practical work. The runnable baselines use generated data or packaged digits; real-data and research extensions state what the learner must evaluate.\n\n| Project | Level | Chapter |\n|---|---|---:|\n"
    + "\n".join(all_rows)
    + "\n\n[Pixel Lab](beginner/pixel-lab/README.md) · [End-to-End Real-Time Platform](capstone/README.md)\n\nRun a project with `python scripts/run_project.py --config projects/<level>/<project>/config.json --output artifacts/my-run`, using the exact path from its README.\n",
)
print(f"Created {len(all_rows)} project baselines.")
