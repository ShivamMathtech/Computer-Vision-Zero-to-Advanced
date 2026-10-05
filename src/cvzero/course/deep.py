"""Learned vision experiments with generated, explicitly labeled teaching data."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import cv2
import numpy as np
import torch
from sklearn.metrics import confusion_matrix
from torch import nn
from torch.nn import functional as F

from . import numerics as n
from .classical import picture
from .models import (
    Autoencoder,
    TinyCNN,
    TinyRadianceField,
    TinyUNet,
    TinyViT,
    classification_experiment,
    configure,
    diffusion_train_sample,
    render_torch,
    shape_data,
    train_supervised,
)
from .result import Result
from .tracking import count_repetitions, joint_angle, soft_argmax


def cnn(lesson, seed, amount):
    configure(seed)
    if lesson == 0:
        rng = np.random.default_rng(seed)
        x = np.r_[rng.normal(-1, 0.4, (24, 2)), rng.normal(1, 0.4, (24, 2))]
        y = np.r_[np.zeros(24, int), np.ones(24, int)]
        parameters, losses = n.mlp_train(x, y, learning_rate=0.15 * amount)
        return Result(
            "23 · Explicit neural-network backpropagation",
            {"Input features": x},
            curves={"Training cross entropy": losses},
            metrics={
                "training_accuracy": float((n.mlp_predict(x, parameters).argmax(1) == y).mean())
            },
            notes="Training accuracy on a constructed two-cluster problem is not held-out vision performance.",
        )
    if lesson == 1:
        image = n.gray(picture(seed))[:32, :32] / 255
        kernel = n.gaussian_kernel(3, 1)
        reference = n.correlate(image, kernel)
        tensor = torch.tensor(image, dtype=torch.float64)[None, None]
        result = F.conv2d(
            F.pad(tensor, (1, 1, 1, 1), mode="replicate"), torch.tensor(kernel)[None, None]
        ).numpy()[0, 0]
        return Result(
            "23 · Fixed filters become trainable CNN kernels",
            {"Input": image, "NumPy correlation": reference, "PyTorch conv2d": result},
            metrics={"maximum_error": float(abs(reference - result).max())},
        )
    return classification(lesson, seed, amount)


def pytorch_lab(lesson, seed, amount):
    model, history, x, y, prediction = classification_experiment(seed, epochs=3, lr=0.01 * amount)
    with TemporaryDirectory() as directory:
        checkpoint = Path(directory) / "weights.pt"
        torch.save(model.state_dict(), checkpoint)
        restored = TinyCNN()
        restored.load_state_dict(torch.load(checkpoint, map_location="cpu", weights_only=True))
        restored.eval()
        with torch.no_grad():
            error = float((model(x) - restored(x)).abs().max())
    return Result(
        "24 · DataLoader, training, evaluation and checkpoint round trip",
        {
            "Held-out example": x[0, 0].numpy(),
            "Confusion matrix": confusion_matrix(y, prediction, labels=[0, 1, 2]),
        },
        curves={"Training loss": history},
        metrics={
            "checkpoint_max_logit_error": error,
            "held_out_accuracy": float((prediction == y).float().mean()),
            "epochs": 3,
            "batch_size": 16,
            "learning_rate": 0.01 * amount,
        },
    )


def classification(lesson, seed, amount):
    model, history, x, y, prediction = classification_experiment(seed, epochs=6, lr=0.01 * amount)
    with torch.no_grad():
        probability = model(x).softmax(1)
    if lesson == 1:
        target = (y == 0).numpy()
        score = probability[:, 0].numpy()
        pred = score > 0.5
        metric = {"binary_circle_accuracy": float((target == pred).mean())}
    elif lesson == 2:
        target = torch.stack([y == 0, y != 0], 1).float()
        logits = model(x)[:, :2]
        loss = F.binary_cross_entropy_with_logits(logits, target)
        metric = {
            "multilabel_bce_demonstration": float(loss.detach()),
            "note": "BCE on two independently interpreted logits; main model trained with multiclass CE",
        }
    else:
        metric = {"held_out_accuracy": float((prediction == y).float().mean())}
    metric.update(
        epochs=6, train_samples=96, test_samples=30, classes=["circle", "square", "triangle"]
    )
    return Result(
        "25 · Classification tasks and held-out evaluation",
        {
            "Held-out circle/square/triangle": torch.cat(list(x[:6, 0]), 1).numpy(),
            "Confusion matrix": confusion_matrix(y, prediction, labels=[0, 1, 2]),
        },
        curves={"Training loss": history},
        metrics=metric,
        notes="Small synthetic classifier. ResNet/EfficientNet/MobileNet external workflows are provided separately.",
    )


def transfer(lesson, seed, amount):
    configure(seed)
    x, y, _ = shape_data(96, seed=seed)
    test_x, test_y, _ = shape_data(30, seed=seed + 1000)
    model = TinyCNN()
    pretrain = train_supervised(model, x, y, epochs=3, seed=seed)
    source_weights = {
        name: parameter.detach().clone() for name, parameter in model.features.named_parameters()
    }
    for parameter in model.features.parameters():
        parameter.requires_grad = lesson == 2
    model.head = nn.Linear(16 * 3 * 3, 3)
    shifted = (x * 0.7 + 0.15).clamp(0, 1)
    target_history = train_supervised(model, shifted, y, epochs=3, lr=0.01 * amount, seed=seed)
    changed = max(
        float((p - source_weights[name]).abs().max())
        for name, p in model.features.named_parameters()
    )
    with torch.no_grad():
        prediction = model((test_x * 0.7 + 0.15).clamp(0, 1)).argmax(1)
    return Result(
        "26 · Feature extraction versus fine-tuning",
        {"Source domain": x[0, 0].numpy(), "Shifted domain": shifted[0, 0].numpy()},
        curves={"Source training loss": pretrain, "Target adaptation loss": target_history},
        metrics={
            "feature_max_parameter_change": changed,
            "held_out_target_accuracy": float((prediction == test_y).float().mean()),
            "backbone_frozen": lesson != 2,
        },
        notes="Pretraining is performed locally on generated shapes; this is not ImageNet-pretrained transfer.",
    )


def detection(lesson, seed, amount):
    boxes = np.array([[10, 10, 50, 50], [12, 12, 49, 49], [60, 20, 85, 60]], float)
    scores = np.array([0.9, 0.8, 0.7])
    kept = n.nms(boxes, scores, min(0.9, 0.5 * amount))
    image = np.zeros((80, 100, 3), np.uint8)
    for index, box in enumerate(boxes):
        cv2.rectangle(
            image,
            tuple(box[:2].astype(int)),
            tuple(box[2:].astype(int)),
            (70, 230, 140) if index in kept else (170, 60, 70),
            2,
        )
    ap, precision, recall = n.average_precision([True, False, True], scores, 2)
    return Result(
        "27 · Bounding boxes, overlap, suppression and AP",
        {"Boxes: green retained by NMS": image},
        curves={"Precision versus recall": np.c_[recall, precision]},
        metrics={
            "iou_first_pair": float(n.iou(boxes[0], boxes[1:2])[0]),
            "nms_indices": kept.tolist(),
            "one_class_ap_at_preassigned_matches": ap,
        },
        notes="AP assumes already matched detections. Real mAP recomputes matching per class and IoU threshold; duplicates count as false positives.",
    )


def yolo_grid(lesson, seed, amount):
    configure(seed)
    x, _, masks = shape_data(64, size=24, seed=seed)
    targets = []
    for mask in masks[:, 0].numpy():
        yy, xx = np.nonzero(mask)
        targets.append(
            [
                (xx.min() + xx.max() + 1) / 48,
                (yy.min() + yy.max() + 1) / 48,
                (xx.max() - xx.min() + 1) / 24,
                (yy.max() - yy.min() + 1) / 24,
            ]
        )
    targets = torch.tensor(targets)
    model = nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(8 * 24 * 24, 4),
        nn.Sigmoid(),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.004 * amount)
    losses = []
    for _ in range(30):
        prediction = model(x)
        loss = F.smooth_l1_loss(prediction, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    test, _, test_masks = shape_data(6, size=24, seed=seed + 999)
    with torch.no_grad():
        box = model(test)[0].numpy()
    canvas = cv2.cvtColor((test[0, 0].numpy() * 255).astype(np.uint8), cv2.COLOR_GRAY2RGB)
    cx, cy, w, h = box * 24
    cv2.rectangle(
        canvas,
        (int(cx - w / 2), int(cy - h / 2)),
        (int(cx + w / 2), int(cy + h / 2)),
        (255, 80, 40),
        1,
    )
    return Result(
        "28 · Single-shot box regression before full YOLO",
        {"Unseen synthetic input and predicted box": canvas, "Training mask": masks[0, 0].numpy()},
        curves={"Training box loss": losses},
        metrics={
            "predicted_normalized_cxcywh": box.tolist(),
            "training_samples": 64,
            "updates": 30,
        },
        notes="A four-output didactic single-object regressor, NOT an implementation of Ultralytics YOLO. The included YOLO CLI performs actual dataset validation, train, val, predict and export with an optional installation.",
    )


def segmentation_lab(lesson, seed, amount):
    configure(seed)
    x, _, masks = shape_data(64, seed=seed)
    test, _, truth = shape_data(12, seed=seed + 1000)
    model = TinyUNet()
    history = train_supervised(
        model, x, masks, epochs=4, lr=0.01 * amount, segmentation=True, seed=seed
    )
    with torch.no_grad():
        probability = torch.sigmoid(model(test))
        predicted = probability > 0.5
    intersection = (predicted * truth.bool()).sum().item()
    union = (predicted | truth.bool()).sum().item()
    dice = 2 * intersection / (predicted.sum().item() + truth.sum().item() + 1e-8)
    return Result(
        "29/31 · Train a tiny U-Net for foreground segmentation",
        {
            "Held-out image": test[0, 0].numpy(),
            "Ground truth": truth[0, 0].numpy(),
            "Predicted probability": probability[0, 0].numpy(),
            "Binary prediction": predicted[0, 0].numpy(),
        },
        curves={"Training BCE": history},
        metrics={
            "held_out_pixel_iou": intersection / max(union, 1),
            "held_out_dice": dice,
            "train_samples": 64,
            "test_samples": 12,
            "epochs": 4,
        },
        notes="Generated shapes establish pipeline behavior. These are not industrial or medical-diagnostic results.",
    )


def instances(lesson, seed, amount):
    mask = np.zeros((96, 112), np.uint8)
    cv2.circle(mask, (42, 48), 22, 255, -1)
    cv2.circle(mask, (72, 48), 22, 255, -1)
    distance = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    centers = (distance > distance.max() * 0.75).astype(np.uint8)
    _, markers = cv2.connectedComponents(centers)
    markers = markers + 1
    markers[(mask > 0) & (centers == 0)] = 0
    rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    labels = cv2.watershed(rgb, markers.astype(np.int32))
    binary_labels, count = n.components(mask > 0)
    return Result(
        "30 · Semantic foreground versus separate instances",
        {
            "Merged foreground": mask,
            "Distance map": distance,
            "Seed components": centers,
            "Watershed instances": labels,
        },
        metrics={
            "binary_connected_objects": count,
            "watershed_foreground_instances": len([v for v in np.unique(labels) if v > 1]),
        },
        notes="Watershed is a classical instance baseline. Mask R-CNN inference is an optional pretrained workflow, not simulated by watershed.",
    )


def pose(lesson, seed, amount):
    rng = np.random.default_rng(seed)
    y, x = np.indices((64, 64))
    true = np.array([31.4, 25.2])
    heat = np.exp(-((x - true[0]) ** 2 + (y - true[1]) ** 2) / (2 * 3**2))
    heat += rng.normal(0, 0.01 * amount, heat.shape)
    estimate = soft_argmax(heat, 0.05)
    angles = 105 + 65 * np.cos(np.linspace(0, 6 * np.pi, 120))
    count = count_repetitions(angles)
    return Result(
        "32 · Heatmaps, keypoints and repetition state",
        {"Noisy keypoint heatmap": heat},
        curves={"Elbow angle (degrees)": angles},
        metrics={
            "keypoint_error_px": float(np.linalg.norm(estimate - true)),
            "cycles_counted": count,
            "right_angle_degrees": joint_angle(
                np.array([0, 1]), np.array([0, 0]), np.array([1, 0])
            ),
        },
        notes="Keypoints and motion are generated. This does not estimate joints from a human photograph; use the optional MediaPipe adapter with explicit model assets.",
    )


def hands(lesson, seed, amount):
    palm = np.array(
        [
            [48, 75],
            [30, 55],
            [24, 43],
            [20, 32],
            [17, 22],
            [37, 50],
            [36, 33],
            [35, 21],
            [35, 10],
            [48, 49],
            [48, 29],
            [48, 17],
            [48, 5],
            [59, 51],
            [61, 34],
            [62, 22],
            [63, 12],
            [68, 57],
            [73, 43],
            [76, 33],
            [79, 23],
        ],
        float,
    )
    if lesson == 1:
        palm[8] = [42, 46]
    if lesson == 2:
        palm[4] = palm[8] + [3 * amount, 0]
    canvas = np.zeros((88, 96, 3), np.uint8)
    for start in [1, 5, 9, 13, 17]:
        chain = [0] + list(range(start, start + 4))
        for a, b in zip(chain[:-1], chain[1:]):
            cv2.line(
                canvas, tuple(palm[a].astype(int)), tuple(palm[b].astype(int)), (40, 180, 210), 1
            )
    for point in palm:
        cv2.circle(canvas, tuple(point.astype(int)), 2, (255, 220, 80), -1)
    distance = np.linalg.norm(palm[4] - palm[8]) / np.linalg.norm(palm[0] - palm[9])
    return Result(
        "33 · Hand landmark geometry and virtual interaction",
        {"Synthetic 21-landmark hand": canvas},
        metrics={
            "normalized_pinch_distance": float(distance),
            "pinch_detected": bool(distance < 0.3),
            "pointer_normalized_xy": (palm[8] / [96, 88]).tolist(),
        },
        notes="A safe virtual-pointer calculation; no operating-system mouse clicks are performed. Real landmarks require the optional hand detector.",
    )


def actions(lesson, seed, amount):
    configure(seed)
    rng = np.random.default_rng(seed)

    def data(count):
        labels = np.arange(count) % 2
        time = np.linspace(0, 1, 12)
        positions = np.stack(
            [
                np.c_[time if label == 0 else 1 - time, np.ones(12) * rng.uniform(0.2, 0.8)]
                for label in labels
            ]
        )
        positions += rng.normal(0, 0.025 * amount, positions.shape)
        return torch.tensor(positions, dtype=torch.float32), torch.tensor(labels)

    x, y = data(80)
    test, truth = data(20)

    class ActionGRU(nn.Module):
        def __init__(self):
            super().__init__()
            self.gru = nn.GRU(2, 12, batch_first=True)
            self.head = nn.Linear(12, 2)

        def forward(self, x):
            _, h = self.gru(x)
            return self.head(h[-1])

    model = ActionGRU()
    losses = train_supervised(model, x, y, epochs=5, lr=0.01, seed=seed)
    with torch.no_grad():
        pred = model(test).argmax(1)
    return Result(
        "34 · Temporal order and sequence classification",
        curves={"Example x positions over time": x[0, :, 0].numpy(), "Training loss": losses},
        panels={"First two XY sequences": x[:2].reshape(24, 2).numpy()},
        metrics={
            "held_out_direction_accuracy": float((pred == truth).float().mean()),
            "sequence_length": 12,
        },
        notes="The GRU classifies generated motion direction, not intent or human behavior. CNN+RNN, 3D CNN and temporal transformers are discussed in the chapter.",
    )


def vit(lesson, seed, amount):
    if lesson == 0:
        configure(seed)
        x, _, _ = shape_data(3, seed=seed)
        model = TinyViT()
        with torch.no_grad():
            tokens = model.patch(x).flatten(2).transpose(1, 2)
        return Result(
            "37 · Image patches become a token sequence",
            {"Input": x[0, 0].numpy(), "Patch token vectors": tokens[0].numpy()},
            metrics={
                "tokens_shape": list(tokens.shape),
                "patch_size": 6,
                "embedding_dimension": 24,
            },
        )
    model, history, x, y, pred = classification_experiment(
        seed, kind="vit", epochs=5, lr=0.003 * amount
    )
    return Result(
        "37 · Train a simplified vision transformer",
        {
            "Held-out image": x[0, 0].numpy(),
            "Confusion matrix": confusion_matrix(y, pred, labels=[0, 1, 2]),
        },
        curves={"Training CE": history},
        metrics={
            "held_out_accuracy": float((pred == y).float().mean()),
            "epochs": 5,
            "parameters": sum(p.numel() for p in model.parameters()),
        },
        notes="One encoder and mean pooling; no claim to reproduce a published ImageNet ViT result.",
    )


def attention_lab(lesson, seed, amount):
    rng = configure(seed)
    q = rng.normal(size=(6, 4))
    k = rng.normal(size=(6, 4))
    v = rng.normal(size=(6, 3))
    mask = np.tril(np.ones((6, 6), bool)) if lesson == 1 else None
    output, weights = n.attention(q * amount, k, v, mask)
    qt, kt, vt = [torch.tensor(a, dtype=torch.float64)[None, None] for a in (q * amount, k, v)]
    comparison = F.scaled_dot_product_attention(
        qt, kt, vt, attn_mask=None if mask is None else torch.tensor(mask)
    ).numpy()[0, 0]
    return Result(
        "38 · Query, key, value and scaled attention",
        {"Attention weights (rows sum to 1)": weights, "Weighted value output": output},
        metrics={
            "row_sum_max_error": float(abs(weights.sum(1) - 1).max()),
            "pytorch_max_error": float(abs(output - comparison).max()),
            "causal_mask": lesson == 1,
        },
        notes="A causal mask is demonstrated for sequence reasoning; a standard ViT uses bidirectional patch attention.",
    )


def self_supervision(lesson, seed, amount):
    configure(seed)
    x, _, _ = shape_data(48, seed=seed)
    if lesson == 2:
        model = Autoencoder()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
        losses = []
        mask = torch.rand_like(x) > 0.4
        for _ in range(25):
            reconstructed, _, _ = model(x * mask)
            loss = ((reconstructed - x) ** 2 * (~mask)).sum() / (~mask).sum()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach()))
        return Result(
            "39 · Masked-image reconstruction",
            {
                "Input": x[0, 0].numpy(),
                "Visible patches": (x * mask)[0, 0].numpy(),
                "Reconstruction": reconstructed[0, 0].detach().numpy(),
            },
            curves={"Masked MSE": losses},
            metrics={"mask_fraction": float((~mask).float().mean())},
        )
    encoder = nn.Sequential(nn.Flatten(), nn.Linear(24 * 24, 48), nn.ReLU(), nn.Linear(48, 16))
    optimizer = torch.optim.Adam(encoder.parameters(), lr=0.002)
    losses = []
    import copy

    target = copy.deepcopy(encoder)
    for parameter in target.parameters():
        parameter.requires_grad = False
    for _ in range(30):
        a = (x + 0.08 * torch.randn_like(x)).clamp(0, 1)
        b = (x + 0.08 * torch.randn_like(x)).clamp(0, 1)
        za = F.normalize(encoder(a), dim=1)
        if lesson == 0:
            zb = F.normalize(encoder(b), dim=1)
            z = torch.cat([za, zb])
            logits = z @ z.T / (0.2 * amount)
            logits.fill_diagonal_(-1e9)
            labels = (torch.arange(96) + 48) % 96
            loss = F.cross_entropy(logits, labels)
        else:
            with torch.no_grad():
                zb = F.normalize(target(b), dim=1)
            loss = 2 - 2 * (za * zb).sum(1).mean()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if lesson == 1:
            with torch.no_grad():
                for dest, source in zip(target.parameters(), encoder.parameters(), strict=True):
                    dest.mul_(0.95).add_(source, alpha=0.05)
        losses.append(float(loss.detach()))
    with torch.no_grad():
        embedding = encoder(x)
    return Result(
        "39 · Contrastive views and stop-gradient EMA",
        {
            "Input": x[0, 0].numpy(),
            "Noisy view": a[0, 0].numpy(),
            "Embedding dimensions": embedding.numpy(),
        },
        curves={"Training objective": losses},
        metrics={
            "embedding_mean_std": float(embedding.std(0).mean()),
            "method": "NT-Xent" if lesson == 0 else "minimal EMA consistency",
        },
        notes="The EMA consistency example omits BYOL’s predictor and full augmentation recipe; monitor collapse. It is an ingredient study, not a faithful BYOL reproduction.",
    )


def vision_language(lesson, seed, amount):
    configure(seed)
    x, y, _ = shape_data(60, seed=seed)
    image_encoder = nn.Sequential(
        nn.Flatten(), nn.Linear(24 * 24, 24), nn.ReLU(), nn.Linear(24, 12)
    )
    text_encoder = nn.Embedding(3, 12)
    optimizer = torch.optim.Adam(
        list(image_encoder.parameters()) + list(text_encoder.parameters()), lr=0.006
    )
    losses = []
    for _ in range(35):
        visual = F.normalize(image_encoder(x), dim=1)
        text = F.normalize(text_encoder(torch.arange(3)), dim=1)
        logits = visual @ text.T / (0.2 * amount)
        loss = F.cross_entropy(logits, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    test, truth, _ = shape_data(12, seed=seed + 1000)
    with torch.no_grad():
        similarity = (
            F.normalize(image_encoder(test), dim=1)
            @ F.normalize(text_encoder(torch.arange(3)), dim=1).T
        )
    labels = ["circle", "square", "triangle"]
    return Result(
        "40 · Learned image-text alignment in a closed vocabulary",
        {
            "Held-out image": test[0, 0].numpy(),
            "Cosine similarity to three words": similarity.numpy(),
        },
        curves={"Alignment cross entropy": losses},
        metrics={
            "held_out_retrieval_accuracy": float((similarity.argmax(1) == truth).float().mean()),
            "retrieved_word": labels[int(similarity[0].argmax())],
            "vocabulary": labels,
        },
        notes="A trainable three-token dual encoder teaches alignment. It is not CLIP, free-form captioning or general VQA. Those use explicit optional pretrained adapters.",
    )


def generative(lesson, seed, amount):
    configure(seed)
    x, _, _ = shape_data(64, seed=seed)
    losses = []
    if lesson < 2:
        model = Autoencoder(variational=lesson == 1)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
        for _ in range(35):
            output, mu, logvar = model(x)
            reconstruction = F.mse_loss(output, x)
            kl = -0.5 * (1 + logvar - mu.pow(2) - logvar.exp()).mean()
            loss = reconstruction + (0.01 * amount * kl if lesson == 1 else 0)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach()))
        with torch.no_grad():
            samples = model.decoder(torch.randn(4, 12)).reshape(4, 24, 24)
        panels = {
            "Input": x[0, 0].numpy(),
            "Reconstruction": output[0, 0].detach().numpy(),
            "Latent samples": torch.cat(list(samples), 1).numpy(),
        }
        label = "VAE" if lesson else "Autoencoder"
    else:
        generator = nn.Sequential(nn.Linear(12, 64), nn.ReLU(), nn.Linear(64, 576), nn.Sigmoid())
        discriminator = nn.Sequential(nn.Linear(576, 64), nn.LeakyReLU(0.2), nn.Linear(64, 1))
        go = torch.optim.Adam(generator.parameters(), lr=0.002)
        do = torch.optim.Adam(discriminator.parameters(), lr=0.002)
        for _ in range(40):
            fake = generator(torch.randn(64, 12))
            real = x.flatten(1)
            dl = (
                F.softplus(-discriminator(real)).mean()
                + F.softplus(discriminator(fake.detach())).mean()
            )
            do.zero_grad()
            dl.backward()
            do.step()
            gl = F.softplus(-discriminator(generator(torch.randn(64, 12)))).mean()
            go.zero_grad()
            gl.backward()
            go.step()
            losses.append(float(gl.detach()))
        panels = {
            "Real shape": x[0, 0].numpy(),
            "Generator sample": generator(torch.randn(1, 12)).detach().reshape(24, 24).numpy(),
        }
        label = "GAN"
    return Result(
        "42 · " + label + " training and sample inspection",
        panels,
        curves={"Training objective": losses},
        metrics={"updates": len(losses)},
        notes="Short synthetic training demonstrates objectives and data flow, not photorealistic generation or a publication-quality generative score.",
    )


def diffusion(lesson, seed, amount):
    _, history, clean, sample, alpha_bar = diffusion_train_sample(
        seed, updates=40 if lesson == 0 else 70
    )
    return Result(
        "43 · Forward noise and learned reverse diffusion",
        {
            "Training shapes in [-1,1]": torch.cat(list(clean[:, 0]), 1).numpy(),
            "Generated short-run samples": torch.cat(list(sample[:, 0]), 1).numpy(),
        },
        curves={"Noise prediction MSE": history, "Signal retention alpha-bar": alpha_bar.numpy()},
        metrics={"updates": len(history), "diffusion_steps": 32},
        notes="Fixed-variance DDPM-style teaching sampler; short CPU runs often make poor samples. No pretrained diffusion weights or quality metric is implied.",
    )


def nerf(lesson, seed, amount):
    configure(seed)
    side = 12
    y, x = torch.meshgrid(torch.linspace(-1, 1, side), torch.linspace(-1, 1, side), indexing="ij")
    z = torch.linspace(-1, 1, 20)
    rays = torch.stack(
        [
            x.flatten()[:, None].expand(-1, 20),
            y.flatten()[:, None].expand(-1, 20),
            z[None].expand(side * side, -1),
        ],
        -1,
    )
    density = (rays.square().sum(-1) < 0.55**2).float() * 12
    colors = ((rays + 1) / 2).clamp(0, 1)
    target = render_torch(density, colors, 2 / 20)
    model = TinyRadianceField()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    losses = []
    for _ in range(50):
        sigma, color = model(rays)
        prediction = render_torch(sigma, color, 2 / 20)
        loss = F.mse_loss(prediction, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    with torch.no_grad():
        sigma, color = model(rays)
        rendered = render_torch(sigma, color, 2 / 20)
    return Result(
        "48 · Density, transmittance and a tiny radiance field",
        {
            "Analytic sphere render": target.reshape(side, side, 3).numpy(),
            "Learned training view": rendered.reshape(side, side, 3).numpy(),
        },
        curves={"Ray color MSE": losses},
        metrics={"rays": side * side, "samples_per_ray": 20, "final_training_mse": losses[-1]},
        notes="Orthographic, position-only single-view fit is underconstrained. It teaches volume rendering and optimization; it is not a multi-view NeRF reconstruction benchmark.",
    )


FUNCTIONS = {
    23: cnn,
    24: pytorch_lab,
    25: classification,
    26: transfer,
    27: detection,
    28: yolo_grid,
    29: segmentation_lab,
    30: instances,
    31: segmentation_lab,
    32: pose,
    33: hands,
    34: actions,
    37: vit,
    38: attention_lab,
    39: self_supervision,
    40: vision_language,
    42: generative,
    43: diffusion,
    48: nerf,
}
