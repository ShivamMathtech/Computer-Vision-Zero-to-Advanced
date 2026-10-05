"""Chapter 21: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.classical import ocr as experiment
from cvzero.course.numerics import otsu as reference

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
