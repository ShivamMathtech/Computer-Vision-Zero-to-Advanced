"""Chapter 35: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.numerics import lucas_kanade_global as reference
from cvzero.course.spatial import optical_flow as experiment

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
