"""Chapter 28: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.deep import yolo_grid as experiment
from cvzero.course.numerics import iou as reference

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
