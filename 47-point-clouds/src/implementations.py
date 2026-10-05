"""Chapter 47: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.geometry import icp as reference
from cvzero.course.spatial import point_clouds as experiment

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
