"""Chapter 01 teaching entry point.

The actual documented implementations live in src/cvzero/images.py to avoid
copying algorithms between notebooks, projects and tests. Open that file to
compare the three-loop reference with its vectorized equivalent.
Run from the repository root after installation:
    python 01-python-for-computer-vision/src/implementations.py
"""

import cv2
import numpy as np

from cvzero.images import adjust_brightness, brightness_loop, grayscale_loop, rgb_to_gray
from cvzero.synthetic import tiny_palette


def main() -> None:
    """Check exact arithmetic and a library grayscale comparison."""
    image = tiny_palette()
    np.testing.assert_array_equal(brightness_loop(image, 30), adjust_brightness(image, 30))
    np.testing.assert_array_equal(grayscale_loop(image), rgb_to_gray(image))
    reference = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    difference = np.abs(reference.astype(np.int16) - rgb_to_gray(image).astype(np.int16))
    assert difference.max() <= 1
    print("Loop and NumPy agree; OpenCV grayscale is within one intensity level.")


if __name__ == "__main__":
    main()
