# Semantic Segmentation — concepts and mechanisms

## What and why

Semantic segmentation assigns a category to every pixel. All pixels of the same category share a label even when they belong to separate objects. Dense prediction requires spatially aligned targets, careful loss design and evaluation across classes.

## 1. Dense class targets and FCN

A fully convolutional network replaces image-level classification with spatial logits. For C mutually exclusive classes, logits have shape N×C×H×W and targets typically have integer IDs N×H×W. Binary one-channel segmentation is a special case and uses a different target contract.

## 2. U-Net, DeepLab and context

U-Net uses skip connections to combine localization and deeper context. DeepLab uses dilated convolutions and multiscale context mechanisms in common variants. Dilation increases receptive field without necessarily reducing output resolution, but can introduce sampling artifacts. The local lab trains a small foreground/background U-Net; optional workflows expose pretrained DeepLab.

## 3. IoU, imbalance and deployment masks

Compute a confusion matrix across pixels, derive each class IoU and state how absent classes are handled when averaging. Rare classes and uncertain boundaries require care in loss weighting and metrics. Medical datasets require appropriate permissions and expert validation; educational segmentation outputs are not diagnostic tools.

## Mathematical foundation

$$
IoU_c=TP_c/(TP_c+FP_c+FN_c)
$$

TPc counts pixels correctly assigned class c, FPc pixels incorrectly assigned c and FNc missed class-c pixels. Counts 8,2,4 give IoU=8/14. Mean IoU averages class scores under a declared absent-class policy.

The numerical example makes the units and reduction visible before the larger pipeline:

```python
import numpy as np
import cv2

tp, fp, fn = 8.0, 2.0, 4.0
class_iou = tp / (tp + fp + fn)
assert np.isclose(class_iou, 8 / 14)
print(class_iou)
```

## What happens internally

The baseline is binary semantic segmentation with a shallow U-Net. The same dense-prediction principles extend to C classes by changing head channels, targets and loss together.

Read the chapter entry point, then follow its shared source. The core reference is `models.TinyUNet`. Separate data construction, algorithm, metric and plotting when changing the experiment.

## Visual reasoning

![Actual baseline](../assets/lab-preview.png)

Predict a change before rerunning. Explain what each axis, color, mask or matrix cell represents. In learned examples, compare a loss curve with held-out predictions; in geometry examples, compare coordinate residuals with known synthetic truth. Visual plausibility is useful evidence, but does not replace a declared metric.

## Controlled experiment

Create a rare foreground class and compare unweighted loss with a documented weighting scheme. Report per-class IoU rather than only the mean.

Write down the independent variable, what remains fixed, and the metric before changing code. Repeat stochastic experiments with multiple seeds and retain negative results. A timing comparison should include warm-up, repeat count and hardware; never compare unmatched preprocessing or data sizes.

## Applications and limits

Train and inspect a dense labeling model. The mini project applies the mechanism in a small runnable baseline. Colorful mask visualizations are not training targets unless colors are mapped consistently to integer class IDs.

The local generated distribution deliberately removes some real-world complexity. External data, pretrained models and hardware paths are documented separately in [external workflows](../../docs/external-workflows.md). A toy objective or synthetic score must be labeled as such when used in a portfolio.

## Exercises and checkpoint

Explain this chapter to someone using one concrete example. Then implement a tiny case, change a parameter, create a failure and apply the method to new data. Use the [three exercise levels](../exercises/beginner.md) and [challenge](../exercises/challenge.md) to record evidence.

## Research connection

[Read the chapter research note](../../docs/research-reading.md#chapter-31). It distinguishes the original contribution, architecture intuition, limitations and alternatives from the scope of the runnable lab.

## References and next step

[Primary reference](https://arxiv.org/abs/1606.00915). Continue through the chapter notebooks and mini project, then follow the next-chapter link in the [chapter README](../README.md).
