# Prerequisites and self-check

## You need

A Python 3.11–3.13 environment, permission to install packages, a terminal and enough disk space for that environment. No webcam or CUDA is required for Chapter 01. Installation needs internet; the chapter's synthetic experiments run offline afterward.

## Python readiness

Can you assign `width = 4`, write a `for` loop, call `print(width)` and save a `.py` file? If not, work slowly through notebook 01. It explains variables, integers, strings, booleans, lists, dictionaries, branching, loops and functions before using images.

## Arithmetic readiness

1. A 3-row, 5-column image contains how many pixels?
2. What is the mean of 10, 20 and 30?
3. If a channel is 250 and you add 20, what should an 8-bit display value become when clipped?
4. In a list of three items, which indices are valid?

Check after attempting: 15 pixels; 20; 255; 0, 1, 2. Clipping means stopping at the representable boundary, not wrapping back to a dark value.

## Useful terminal habits

Use `cd` to enter the extracted repository. Run `python --version` and `python -m pip --version` to identify your environment. Prefer `pathlib.Path` in Python to hardcoded operating-system paths. A Jupyter kernel is a Python process; selecting the wrong kernel can hide installed packages.

## What is deliberately not assumed?

Calculus, probability, linear algebra, neural networks, PyTorch, GPU programming and model training. These arrive gradually. Never treat not knowing a term as a reason to stop; use the glossary and small examples.
