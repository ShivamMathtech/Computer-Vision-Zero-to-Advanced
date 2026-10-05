"""Small actual trainable models. Sizes are for CPU teaching, not benchmark claims."""

from __future__ import annotations

import cv2
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset


def configure(seed=42):
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    return np.random.default_rng(seed)


def shape_data(count=96, size=24, seed=42):
    """Independent random circles/squares/triangles with masks and class labels."""
    rng = np.random.default_rng(seed)
    images = []
    masks = []
    labels = []
    for index in range(count):
        label = index % 3
        mask = np.zeros((size, size), np.uint8)
        cx, cy = rng.integers(size // 3, 2 * size // 3, size=2)
        radius = int(rng.integers(size // 6, size // 3))
        if label == 0:
            cv2.circle(mask, (int(cx), int(cy)), radius, 1, -1)
        elif label == 1:
            cv2.rectangle(
                mask,
                (int(cx - radius), int(cy - radius)),
                (int(cx + radius), int(cy + radius)),
                1,
                -1,
            )
        else:
            cv2.fillPoly(
                mask,
                [
                    np.array(
                        [[cx, cy - radius], [cx - radius, cy + radius], [cx + radius, cy + radius]],
                        np.int32,
                    )
                ],
                1,
            )
        image = np.clip(mask * rng.uniform(0.6, 1) + rng.normal(0.05, 0.06, (size, size)), 0, 1)
        images.append(image)
        masks.append(mask)
        labels.append(label)
    return (
        torch.tensor(np.array(images), dtype=torch.float32)[:, None],
        torch.tensor(labels),
        torch.tensor(np.array(masks), dtype=torch.float32)[:, None],
    )


class TinyCNN(nn.Module):
    def __init__(self, classes=3):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 8, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(8, 16, 3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((3, 3)),
        )
        self.head = nn.Linear(16 * 3 * 3, classes)

    def forward(self, x):
        return self.head(self.features(x).flatten(1))


class TinyUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.Conv2d(8, 8, 3, padding=1), nn.ReLU()
        )
        self.middle = nn.Sequential(nn.Conv2d(8, 16, 3, padding=1), nn.ReLU())
        self.decoder = nn.Sequential(nn.Conv2d(24, 8, 3, padding=1), nn.ReLU(), nn.Conv2d(8, 1, 1))

    def forward(self, x):
        skip = self.encoder(x)
        bottom = self.middle(F.max_pool2d(skip, 2))
        up = F.interpolate(bottom, size=skip.shape[-2:], mode="bilinear", align_corners=False)
        return self.decoder(torch.cat([skip, up], 1))


class TinyViT(nn.Module):
    def __init__(self, size=24, patch=6, dimension=24, classes=3):
        super().__init__()
        self.patch = nn.Conv2d(1, dimension, patch, stride=patch)
        self.position = nn.Parameter(torch.zeros(1, (size // patch) ** 2, dimension))
        layer = nn.TransformerEncoderLayer(
            dimension, 4, dim_feedforward=48, dropout=0.0, batch_first=True
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=1, enable_nested_tensor=False)
        self.norm = nn.LayerNorm(dimension)
        self.head = nn.Linear(dimension, classes)

    def forward(self, x):
        tokens = self.patch(x).flatten(2).transpose(1, 2) + self.position
        return self.head(self.norm(self.encoder(tokens)).mean(1))


def train_supervised(model, x, y, epochs=6, batch_size=16, lr=0.01, seed=42, segmentation=False):
    """Training-only loop. Caller owns an independent held-out set and evaluation."""
    generator = torch.Generator().manual_seed(seed)
    loader = DataLoader(
        TensorDataset(x, y), batch_size=batch_size, shuffle=True, generator=generator
    )
    optimizer = torch.optim.Adam([p for p in model.parameters() if p.requires_grad], lr=lr)
    history = []
    model.train()
    for _ in range(epochs):
        total = 0
        for batch, target in loader:
            optimizer.zero_grad(set_to_none=True)
            prediction = model(batch)
            loss = (
                F.binary_cross_entropy_with_logits(prediction, target)
                if segmentation
                else F.cross_entropy(prediction, target)
            )
            loss.backward()
            optimizer.step()
            total += float(loss.detach()) * len(batch)
        history.append(total / len(x))
    model.eval()
    return history


def classification_experiment(seed=42, kind="cnn", epochs=6, lr=0.01):
    configure(seed)
    train_x, train_y, _ = shape_data(96, seed=seed)
    test_x, test_y, _ = shape_data(30, seed=seed + 1000)
    model = TinyViT() if kind == "vit" else TinyCNN()
    history = train_supervised(model, train_x, train_y, epochs=epochs, lr=lr, seed=seed)
    with torch.no_grad():
        logits = model(test_x)
        predictions = logits.argmax(1)
    return model, history, test_x, test_y, predictions


class Autoencoder(nn.Module):
    def __init__(self, variational=False):
        super().__init__()
        self.variational = variational
        self.encoder = nn.Sequential(nn.Linear(24 * 24, 64), nn.ReLU())
        self.mu = nn.Linear(64, 12)
        self.logvar = nn.Linear(64, 12)
        self.decoder = nn.Sequential(
            nn.Linear(12, 64), nn.ReLU(), nn.Linear(64, 24 * 24), nn.Sigmoid()
        )

    def forward(self, x):
        hidden = self.encoder(x.flatten(1))
        mu = self.mu(hidden)
        logvar = self.logvar(hidden).clamp(-8, 8)
        z = mu + torch.randn_like(mu) * torch.exp(0.5 * logvar) if self.variational else mu
        reconstruction = self.decoder(z).reshape(-1, 1, 24, 24)
        return reconstruction, mu, logvar


class NoisePredictor(nn.Module):
    def __init__(self, size=16, steps=32):
        super().__init__()
        self.steps = steps
        self.network = nn.Sequential(
            nn.Linear(size * size + 1, 128), nn.SiLU(), nn.Linear(128, size * size)
        )

    def forward(self, x, t):
        inputs = torch.cat([x.flatten(1), t[:, None].float() / self.steps], 1)
        return self.network(inputs).reshape_as(x)


def diffusion_train_sample(seed=42, updates=80):
    configure(seed)
    x, _, _ = shape_data(64, size=16, seed=seed)
    x = x * 2 - 1
    model = NoisePredictor()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    beta = torch.linspace(0.0001, 0.2, 32)
    alpha = 1 - beta
    alpha_bar = alpha.cumprod(0)
    history = []
    for _ in range(updates):
        indices = torch.randint(0, len(x), (16,))
        clean = x[indices]
        t = torch.randint(0, 32, (len(clean),))
        noise = torch.randn_like(clean)
        a = alpha_bar[t, None, None, None]
        noisy = a.sqrt() * clean + (1 - a).sqrt() * noise
        loss = F.mse_loss(model(noisy, t), noise)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        history.append(float(loss.detach()))
    sample = torch.randn(4, 1, 16, 16)
    with torch.no_grad():
        for index in range(31, -1, -1):
            noise = model(sample, torch.full((4,), index))
            sample = (sample - beta[index] / torch.sqrt(1 - alpha_bar[index]) * noise) / torch.sqrt(
                alpha[index]
            )
            if index:
                sample += torch.sqrt(beta[index]) * torch.randn_like(sample)
    return model, history, x[:4], sample.clamp(-1, 1), alpha_bar


class TinyRadianceField(nn.Module):
    """Position-only radiance field: view-independent color in a bounded scene."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(21, 48), nn.ReLU(), nn.Linear(48, 48), nn.ReLU(), nn.Linear(48, 4)
        )

    def forward(self, points):
        encoding = torch.cat(
            [points]
            + [
                f(points * frequency)
                for frequency in (1.0, 2.0, 4.0)
                for f in (torch.sin, torch.cos)
            ],
            -1,
        )
        raw = self.net(encoding)
        return F.softplus(raw[..., 0]), torch.sigmoid(raw[..., 1:])


def render_torch(sigma, color, delta):
    alpha = 1 - torch.exp(-sigma * delta)
    transmission = torch.cumprod(
        torch.cat([torch.ones_like(alpha[..., :1]), 1 - alpha[..., :-1] + 1e-8], -1), -1
    )
    weights = alpha * transmission
    return (weights[..., None] * color).sum(-2) + (1 - weights.sum(-1))[..., None]
