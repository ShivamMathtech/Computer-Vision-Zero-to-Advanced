"""Chapter 46: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.geometry import disparity_to_depth as reference
from cvzero.course.spatial import stereo as experiment

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
