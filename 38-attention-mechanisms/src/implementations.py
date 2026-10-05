"""Chapter 38: public teaching entry points; algorithms are shared, not duplicated."""

from cvzero.course.deep import attention_lab as experiment
from cvzero.course.numerics import attention as reference

__all__ = ["experiment", "reference"]

if __name__ == "__main__":
    result = experiment(lesson=0, seed=42, amount=1.0)
    print(result.metrics)
