"""Explicit opt-in downloads through official torchvision dataset adapters."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", choices=["cifar10", "pets"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--download",
        action="store_true",
        help="Explicitly allow network download; review official dataset terms first.",
    )
    args = parser.parse_args()
    try:
        from torchvision.datasets import CIFAR10, OxfordIIITPet

        if args.name == "cifar10":
            train = CIFAR10(args.output, train=True, download=args.download)
            test = CIFAR10(args.output, train=False, download=args.download)
        else:
            train = OxfordIIITPet(
                args.output, split="trainval", target_types="segmentation", download=args.download
            )
            test = OxfordIIITPet(
                args.output, split="test", target_types="segmentation", download=args.download
            )
        print(
            {
                "dataset": args.name,
                "train_or_trainval": len(train),
                "test": len(test),
                "root": str(args.output),
            }
        )
        print("Create a validation split from training data; preserve the official test split.")
    except (ImportError, RuntimeError, OSError) as exc:
        parser.exit(
            2,
            f"Dataset unavailable: {exc}\nInstall compatible torchvision, check the path, or opt into --download.\n",
        )


if __name__ == "__main__":
    main()
