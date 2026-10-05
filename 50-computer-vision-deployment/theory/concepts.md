# Computer Vision Deployment — concepts and mechanisms

## What and why

Deployment wraps model behavior in a stable interface. Input validation, preprocessing, versioned outputs and useful failure responses are part of correctness. A local demo becomes a service only when its state, storage and operating assumptions are explicit.

## 1. Inference contracts and FastAPI

An inference contract specifies image formats, maximum size, color order, output coordinates and label meanings. The FastAPI app validates bounded base64 payloads, checks decoded dimensions and returns structured detections plus an overlay. Invalid input should produce a useful client error rather than crash the worker.

## 2. Persistence, sessions and request ordering

Tracking requires per-stream state, so the app creates anonymous sessions and rejects repeated or out-of-order frame IDs. A session lock serializes updates, and SQLite stores numeric event reports without images. The notebook exercises actual routes through an in-process HTTP client and verifies persistence and duplicate rejection.

## 3. Containers and deployment boundaries

A container packages the application but does not automatically supply authentication, TLS, quotas or scalable storage. Run the teaching service on localhost first. FastAPI suits APIs; Streamlit and Gradio can provide quick local model interfaces. A production service needs deployment-specific load tests, monitoring and a migration plan for stateful workers.

## Mathematical foundation

$$
L_{end}=L_{decode}+L_{pre}+L_{model}+L_{post}+L_{transport}
$$

Lend is end-to-end latency and the remaining terms are decode, preprocessing, inference, postprocessing and transport times. Components 2,3,10,2,5 milliseconds sum to 22 ms. Server model time alone is only one component.

The numerical example makes the units and reduction visible before the larger pipeline:

```python
import numpy as np
import cv2

components_ms = np.array([2.0, 3.0, 10.0, 2.0, 5.0])
end_to_end_ms = components_ms.sum()
assert end_to_end_ms == 22
print(end_to_end_ms)
```

## What happens internally

The capstone factory constructs an API, per-session engine and SQLite event store. Tests send real request payloads without opening a public network listener.

Read the chapter entry point, then follow its shared source. The core reference is `engineering.queue_simulation`. Separate data construction, algorithm, metric and plotting when changing the experiment.

## Visual reasoning

![Actual baseline](../assets/lab-preview.png)

Predict a change before rerunning. Explain what each axis, color, mask or matrix cell represents. In learned examples, compare a loss curve with held-out predictions; in geometry examples, compare coordinate residuals with known synthetic truth. Visual plausibility is useful evidence, but does not replace a declared metric.

## Controlled experiment

Send invalid images, duplicate IDs and oversized dimensions. Verify status codes and that failed requests do not create stored events.

Write down the independent variable, what remains fixed, and the metric before changing code. Repeat stochastic experiments with multiple seeds and retain negative results. A timing comparison should include warm-up, repeat count and hardware; never compare unmatched preprocessing or data sizes.

## Applications and limits

Serve a versioned model and validate requests and predictions. The mini project applies the mechanism in a small runnable baseline. In-memory session state is not shared across server processes. Multiple workers need a deliberate state partitioning or external-state design.

The local generated distribution deliberately removes some real-world complexity. External data, pretrained models and hardware paths are documented separately in [external workflows](../../docs/external-workflows.md). A toy objective or synthetic score must be labeled as such when used in a portfolio.

## Exercises and checkpoint

Explain this chapter to someone using one concrete example. Then implement a tiny case, change a parameter, create a failure and apply the method to new data. Use the [three exercise levels](../exercises/beginner.md) and [challenge](../exercises/challenge.md) to record evidence.

## Research connection

[Read the chapter research note](../../docs/research-reading.md#chapter-50). It distinguishes the original contribution, architecture intuition, limitations and alternatives from the scope of the runnable lab.

## References and next step

[Primary reference](https://fastapi.tiangolo.com/tutorial/). Continue through the chapter notebooks and mini project, then follow the next-chapter link in the [chapter README](../README.md).
