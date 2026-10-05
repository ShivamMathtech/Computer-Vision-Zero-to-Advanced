"""Chapter 29: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.deep import segmentation_lab as experiment
from cvzero.course.models import TinyUNet as reference

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
