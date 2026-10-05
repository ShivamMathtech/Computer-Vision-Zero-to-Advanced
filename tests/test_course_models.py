"""Shape/gradient and checkpoint contracts without expensive benchmark training."""

import numpy as np
import pytest

torch = pytest.importorskip("torch")
from cvzero.course.models import TinyCNN, TinyUNet, TinyViT, configure, shape_data  # noqa: E402
from cvzero.course.numerics import attention  # noqa: E402


@pytest.mark.parametrize(
    "model_class,shape", [(TinyCNN, (4, 3)), (TinyViT, (4, 3)), (TinyUNet, (4, 1, 24, 24))]
)
def test_model_forward_backward_and_save_load(model_class, shape, tmp_path):
    configure(42)
    x, _, _ = shape_data(4, seed=42)
    model = model_class()
    output = model(x)
    assert tuple(output.shape) == shape
    output.square().mean().backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
    path = tmp_path / "weights.pt"
    torch.save(model.state_dict(), path)
    restored = model_class()
    restored.load_state_dict(torch.load(path, weights_only=True))
    model.eval()
    restored.eval()
    with torch.inference_mode():
        torch.testing.assert_close(model(x), restored(x))


def test_attention_matches_torch_with_causal_mask():
    configure(42)
    q = torch.randn(4, 3, dtype=torch.float64)
    k = torch.randn(4, 3, dtype=torch.float64)
    v = torch.randn(4, 2, dtype=torch.float64)
    mask = np.tril(np.ones((4, 4), bool))
    reference, _ = attention(q.numpy(), k.numpy(), v.numpy(), mask)
    actual = torch.nn.functional.scaled_dot_product_attention(q, k, v, attn_mask=torch.tensor(mask))
    np.testing.assert_allclose(reference, actual.numpy(), rtol=1e-10, atol=1e-10)
