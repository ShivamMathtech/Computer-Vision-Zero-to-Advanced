"""Chapter 44: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.geometry import triangulate as reference
from cvzero.course.spatial import reconstruction as experiment

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
