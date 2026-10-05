"""Finite differences verify manual convolution and classifier backpropagation."""

import numpy as np
import pytest

from cvzero.course.scratch_cnn import forward_backward, initialize, stripe_data


@pytest.mark.parametrize(
    "name,index", [("kernel", (0, 1, 2)), ("bias", (0,)), ("weight", (0, 1)), ("head_bias", (1,))]
)
def test_manual_cnn_gradients_match_finite_difference(name, index):
    images, labels = stripe_data(count=4, seed=5)
    parameters = initialize(2)
    _, _, gradients = forward_backward(images, labels, parameters)
    step = 1e-6
    original = parameters[name][index]
    parameters[name][index] = original + step
    plus = forward_backward(images, labels, parameters)[0]
    parameters[name][index] = original - step
    minus = forward_backward(images, labels, parameters)[0]
    parameters[name][index] = original
    np.testing.assert_allclose(
        gradients[name][index], (plus - minus) / (2 * step), atol=1e-7, rtol=1e-4
    )
