"""Train or fine-tune a torchvision classifier on train/val/test ImageFolder data.

Images must be grouped by acquisition source before creating these folders.
This opt-in real-data workflow is separate from the downloaded-free CPU lessons.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--model", choices=["resnet18", "efficientnet_b0", "mobilenet_v3_small"], default="resnet18"
    )
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--pretrained", action="store_true", help="Explicitly download/reuse pretrained weights"
    )
    parser.add_argument("--freeze-backbone", action="store_true")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    import torch
    from torch import nn
    from torch.utils.data import DataLoader
    from torchvision import datasets, models, transforms

    if args.epochs < 1 or args.batch_size < 1:
        parser.error("epochs and batch-size must be positive.")
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("Choose a new or empty output folder.")
    for split in ("train", "val", "test"):
        if not (args.data / split).is_dir():
            parser.error(f"Missing split directory: {args.data / split}")
    if args.device.startswith("cuda") and not torch.cuda.is_available():
        parser.error("CUDA is unavailable. Use --device cpu.")
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    weights = models.get_model_weights(args.model).DEFAULT if args.pretrained else None
    # Fixed ImageNet normalization matches the selected pretrained families.
    common = [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
    dataset = {
        s: datasets.ImageFolder(args.data / s, transform=transforms.Compose(common))
        for s in ("train", "val", "test")
    }
    if any(d.class_to_idx != dataset["train"].class_to_idx for d in dataset.values()):
        parser.error("Class folders must match across all splits.")
    model = models.get_model(args.model, weights=weights)
    if args.freeze_backbone:
        for p in model.parameters():
            p.requires_grad = False
    classes = len(dataset["train"].classes)
    if args.model == "resnet18":
        model.fc = nn.Linear(model.fc.in_features, classes)
    else:
        model.classifier[-1] = nn.Linear(model.classifier[-1].in_features, classes)
    model.to(args.device)
    optimizer = torch.optim.Adam(
        (p for p in model.parameters() if p.requires_grad), lr=args.learning_rate
    )
    criterion = nn.CrossEntropyLoss()
    generator = torch.Generator().manual_seed(args.seed)
    loaders = {
        s: DataLoader(
            d,
            batch_size=args.batch_size,
            shuffle=s == "train",
            num_workers=0,
            generator=generator if s == "train" else None,
        )
        for s, d in dataset.items()
    }
    args.output.mkdir(parents=True, exist_ok=True)
    best = float("inf")
    history = []

    def evaluate(split):
        model.eval()
        total = 0.0
        correct = 0
        count = 0
        with torch.inference_mode():
            for images, labels in loaders[split]:
                images, labels = images.to(args.device), labels.to(args.device)
                logits = model(images)
                loss = criterion(logits, labels)
                total += loss.item() * len(labels)
                correct += int((logits.argmax(1) == labels).sum())
                count += len(labels)
        return {"loss": total / count, "accuracy": correct / count, "samples": count}

    for epoch in range(args.epochs):
        model.train()
        if args.freeze_backbone:
            # Preserve frozen BatchNorm statistics as well as frozen parameters.
            for module in model.modules():
                if isinstance(module, nn.modules.batchnorm._BatchNorm):
                    module.eval()
        total = 0.0
        count = 0
        for images, labels in loaders["train"]:
            images, labels = images.to(args.device), labels.to(args.device)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            total += loss.item() * len(labels)
            count += len(labels)
        validation = evaluate("val")
        history.append({"epoch": epoch + 1, "train_loss": total / count, "validation": validation})
        if validation["loss"] < best:
            best = validation["loss"]
            torch.save(model.state_dict(), args.output / "best-weights.pt")
        print(json.dumps(history[-1]), flush=True)
    model.load_state_dict(
        torch.load(args.output / "best-weights.pt", map_location=args.device, weights_only=True)
    )
    report = {
        "configuration": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
        "classes": dataset["train"].class_to_idx,
        "history": history,
        "test": evaluate("test"),
        "torch": torch.__version__,
    }
    (args.output / "experiment.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
