# [Concept] — Theory template

## What and why?

[Name a concrete problem. Define the term in plain language.]

## Intuition before notation

[Use a familiar analogy and state where the analogy stops being accurate.]

## Mathematical foundation

1. Write one equation.
2. Define every symbol and unit.
3. Describe what the equation does in words.
4. Work one small numerical example by hand.
5. Implement that same example in Python.
6. Show the relevant CV use and an assumption it makes.

## Internal steps

[Explain each stage before calling a high-level API. For example, an edge lesson must explain gradients, magnitude, thinning and hysteresis before presenting Canny as one call.]

## Implementations and comparison

[Readable reference → NumPy → relevant optimized library. State border handling, rounding, data layout and numerical tolerance.]

## Controlled experiment

[Question, varied parameter, fixed parameters, metric, actual results and limits.]

## Applications and limitations

[Where this is useful, where it fails and how to notice failure.]

## Paper-to-code connection, when relevant

| Field | Authoring prompt |
| --- | --- |
| Paper/year | Original citation and primary link |
| Earlier limitation | What existing methods could not do well |
| Contribution | Which concrete mechanism changed the situation |
| Intuition | Plain-language explanation |
| Architecture | Modules, data flow and objective |
| Code connection | Which function or experiment demonstrates the idea |
| Limitations | Data, compute, assumptions and failure modes |
| Alternatives | Later approaches and why one might choose them |

## What next?

[Exercise, project and subsequent concept.]
