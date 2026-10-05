"""Chapter 30: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.deep import instances as experiment
from cvzero.course.numerics import components as reference

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
