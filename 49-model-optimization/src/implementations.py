"""Chapter 49: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.engineering import optimization as experiment
from cvzero.course.engineering import quantize_symmetric as reference

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
