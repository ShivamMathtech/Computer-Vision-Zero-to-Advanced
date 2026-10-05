"""Explicit opt-in pretrained workflows. Models/data are never downloaded by notebooks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def require_file(path, label):
    if path is None or not Path(path).is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    return Path(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "task",
        choices=[
            "yolo-train",
            "yolo-evaluate",
            "yolo-predict",
            "yolo-export",
            "clip",
            "caption",
            "vqa",
            "hands",
            "pose",
            "ocr",
            "classify",
            "semantic",
            "instance",
            "point-cloud",
        ],
    )
    parser.add_argument(
        "--model", help="Local model file/directory or explicitly selected repository model ID"
    )
    parser.add_argument("--data")
    parser.add_argument("--image")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--text", nargs="+", default=["a circle", "a square", "a triangle"])
    parser.add_argument("--question", default="What objects are in the image?")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--device", default="cpu")
    parser.add_argument(
        "--download-weights",
        action="store_true",
        help="Allow pretrained model download for torchvision/Hugging Face",
    )
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("Choose a new or empty output directory.")
    args.output.mkdir(parents=True, exist_ok=True)
    try:
        result = {}
        if args.task.startswith("yolo"):
            from ultralytics import YOLO

            if not args.model:
                raise ValueError(
                    "--model must explicitly name a local YAML/weight path or downloadable Ultralytics model."
                )
            model = YOLO(args.model)
            if args.task == "yolo-train":
                require_file(args.data, "Dataset YAML")
                metrics = model.train(
                    data=args.data,
                    epochs=args.epochs,
                    imgsz=128,
                    batch=8,
                    seed=42,
                    device=args.device,
                    workers=0,
                    project=str(args.output),
                    name="train",
                )
                result = {
                    "training_directory": str(model.trainer.save_dir),
                    "metrics": metrics.results_dict if metrics else {},
                }
            elif args.task == "yolo-evaluate":
                require_file(args.data, "Dataset YAML")
                metrics = model.val(
                    data=args.data,
                    split="test",
                    device=args.device,
                    project=str(args.output),
                    name="test",
                )
                result = {"metrics": metrics.results_dict, "split": "test"}
            elif args.task == "yolo-predict":
                require_file(args.image, "Image")
                pred = model.predict(
                    source=args.image,
                    device=args.device,
                    save=True,
                    project=str(args.output),
                    name="predict",
                )
                result = {"images": len(pred), "detections": [p.to_json() for p in pred]}
            else:
                result = {"exported_path": str(model.export(format="onnx", device=args.device))}
        elif args.task in ("clip", "caption", "vqa"):
            import torch
            from transformers import AutoProcessor

            require_file(args.image, "Image")
            defaults = {
                "clip": "openai/clip-vit-base-patch32",
                "caption": "Salesforce/blip-image-captioning-base",
                "vqa": "Salesforce/blip-vqa-base",
            }
            model_id = args.model or defaults[args.task]
            local = not args.download_weights
            processor = AutoProcessor.from_pretrained(model_id, local_files_only=local)
            image = Image.open(args.image).convert("RGB")
            if args.task == "clip":
                from transformers import CLIPModel

                model = (
                    CLIPModel.from_pretrained(model_id, local_files_only=local)
                    .eval()
                    .to(args.device)
                )
                inputs = processor(
                    text=args.text, images=image, return_tensors="pt", padding=True
                ).to(args.device)
                with torch.inference_mode():
                    scores = model(**inputs).logits_per_image.softmax(dim=1)[0].cpu().tolist()
                result = {
                    "candidate_labels": args.text,
                    "relative_scores": scores,
                    "warning": "Closed candidate-set scores are not calibrated probabilities.",
                }
            else:
                from transformers import BlipForConditionalGeneration, BlipForQuestionAnswering

                cls = (
                    BlipForConditionalGeneration
                    if args.task == "caption"
                    else BlipForQuestionAnswering
                )
                model = cls.from_pretrained(model_id, local_files_only=local).eval().to(args.device)
                kwargs = {"text": args.question} if args.task == "vqa" else {}
                inputs = processor(images=image, return_tensors="pt", **kwargs).to(args.device)
                with torch.inference_mode():
                    tokens = model.generate(**inputs, max_new_tokens=30)
                result = {
                    "text": processor.decode(tokens[0], skip_special_tokens=True),
                    "warning": "Generated text can be wrong; inspect against the image.",
                }
        elif args.task in ("hands", "pose"):
            import mediapipe as mp

            require_file(args.model, "MediaPipe .task model")
            require_file(args.image, "Image")
            vision = mp.tasks.vision
            cls = vision.HandLandmarker if args.task == "hands" else vision.PoseLandmarker
            with cls.create_from_model_path(args.model) as detector:
                output = detector.detect(mp.Image.create_from_file(args.image))
            landmarks = output.hand_landmarks if args.task == "hands" else output.pose_landmarks
            result = {
                "landmarks": [
                    [{"x": p.x, "y": p.y, "z": p.z} for p in group] for group in landmarks
                ]
            }
        elif args.task == "ocr":
            import cv2
            import pytesseract

            require_file(args.image, "Image")
            image = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
            if image is None:
                raise ValueError("Image format could not be decoded.")
            image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            result = {"text": pytesseract.image_to_string(image, config="--psm 6")}
        elif args.task in ("classify", "semantic", "instance"):
            import torch
            from torchvision import models

            require_file(args.image, "Image")
            if not args.download_weights:
                raise ValueError(
                    "Use --download-weights to opt into torchvision pretrained weights (cached weights are reused)."
                )
            if args.task == "classify":
                name = args.model or "resnet18"
                weights = models.get_model_weights(name).DEFAULT
                model = models.get_model(name, weights=weights).eval().to(args.device)
            elif args.task == "semantic":
                weights = models.segmentation.DeepLabV3_ResNet50_Weights.DEFAULT
                model = (
                    models.segmentation.deeplabv3_resnet50(weights=weights).eval().to(args.device)
                )
            else:
                weights = models.detection.MaskRCNN_ResNet50_FPN_Weights.DEFAULT
                model = (
                    models.detection.maskrcnn_resnet50_fpn(weights=weights).eval().to(args.device)
                )
            image = weights.transforms()(Image.open(args.image).convert("RGB")).to(args.device)
            with torch.inference_mode():
                output = model([image]) if args.task == "instance" else model(image[None])
            if args.task == "classify":
                values, indices = output[0].softmax(0).topk(5)
                result = {
                    "top5": [
                        {"label": weights.meta["categories"][int(i)], "score": float(v)}
                        for i, v in zip(indices, values, strict=True)
                    ]
                }
            elif args.task == "semantic":
                mask = output["out"][0].argmax(0).cpu().numpy().astype("uint8")
                Image.fromarray(mask).save(args.output / "class-ids.png")
                result = {"mask": "class-ids.png", "classes": weights.meta["categories"]}
            else:
                prediction = output[0]
                keep = prediction["scores"] > 0.5
                np.savez_compressed(
                    args.output / "instances.npz",
                    **{k: v[keep].cpu().numpy() for k, v in prediction.items()},
                )
                result = {"instances": int(keep.sum()), "arrays": "instances.npz"}
        else:
            import open3d as o3d

            require_file(args.data, "Point cloud")
            cloud = o3d.io.read_point_cloud(args.data)
            if len(cloud.points) == 0:
                raise ValueError("Point cloud is empty.")
            reduced = cloud.voxel_down_sample(0.02)
            o3d.io.write_point_cloud(str(args.output / "downsampled.ply"), reduced)
            result = {
                "input_points": len(cloud.points),
                "output_points": len(reduced.points),
                "voxel_size": 0.02,
            }
        (args.output / "report.json").write_text(json.dumps(result, indent=2, default=float) + "\n")
        print(json.dumps(result, indent=2, default=float))
    except (ImportError, FileNotFoundError, ValueError, OSError) as exc:
        parser.exit(
            2,
            f"Workflow could not run: {exc}\nSee docs/external-workflows.md for optional dependencies and model downloads.\n",
        )


if __name__ == "__main__":
    main()
