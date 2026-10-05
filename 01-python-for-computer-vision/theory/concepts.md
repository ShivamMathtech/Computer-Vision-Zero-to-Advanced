# Python for Computer Vision — Concepts

## 1. What are we trying to do?

A computer does not receive “a red rectangle.” It receives numbers arranged in a grid. Computer vision connects those measurements to useful descriptions. Our first job is smaller: inspect the grid, make a deliberate change and verify its effect. This is useful whenever an image enters a processing or learning system.

Imagine a spreadsheet. Each cell corresponds to one location. A grayscale image puts one value at each location. A color image keeps several values there, like three aligned spreadsheets. This analogy explains storage; it does not mean real cameras measure red, green and blue in exactly this arrangement internally.

The chapter follows **what → why → how → experiment → limitations → next step**. We start with Python structures because they let us describe these operations clearly. No model is involved.

## 2. Python values and control flow

A variable is a name referring to a value. `width = 3` stores an integer under a name; `label = 'sample'` refers to a string. `is_color = True` is a boolean. Booleans choose branches; numbers support arithmetic; strings describe files and results.

```python
width = 3
height = 2
label = "sample"
is_color = True
pixel_count = width * height
if is_color:
    print(label, pixel_count, "color pixels")
else:
    print(label, pixel_count, "grayscale pixels")
```

An `if` statement selects a branch based on a condition. Indentation groups the lines that belong to it. A `for` loop repeats work. `range(3)` produces indices 0, 1 and 2: the stop is excluded.

```python
for column in range(width):
    print("column", column)
```

Use a list for an ordered collection, such as `[255, 0, 0]`. Use a dictionary for named settings, such as `{'brightness': 20, 'seed': 42}`. Looking up `settings['brightness']` tells a reader what the number means. A tuple such as `(height, width, 3)` is a fixed collection often used for a shape.

A nested list can describe an image by rows, then columns, then channels. It is easy to inspect but cumbersome for repeated numerical operations. NumPy gives this structure a precise shape and dtype.

## 3. A function is a reusable recipe

A function accepts inputs, performs an operation and may return a result. A parameter is a local name in its definition; an argument is a value passed by the caller.

```python
def clip_channel(value):
    """Keep one numeric value within an 8-bit channel range."""
    return min(255, max(0, value))


print(clip_channel(270))  # 255
```

`return` hands the value back. `print` only displays it. Forgetting `return` is a common reason a later variable contains `None`. A pure transformation reads an input and returns a new output without modifying that input. This makes before/after comparisons easier to trust.

Type hints describe the intended interface; they do not validate data automatically. A function annotated `delta: float` still needs to reject NaN, infinity or inappropriate ranges if those would break its contract. A docstring explains behavior, assumptions and units; comments should explain a reason, not merely repeat a line of code.

## 4. A class groups state and behavior

An object can keep data together with methods that operate on it. `self` is the current object; `__init__` initializes it. Start with an ordinary function when no persistent state is needed.

```python
class BrightnessSetting:
    def __init__(self, delta):
        self.delta = delta

    def describe(self):
        return f"Add {self.delta} intensity levels to each channel"


setting = BrightnessSetting(20)
print(setting.describe())
```

The mini project uses a small `LabConfig` dataclass to group parameters by name. A dataclass can generate routine initialization for us; it does not make the image transformation smarter. In this repository, the transformation itself remains a readable function.

## 5. Shape, axes and coordinates

For a color array, write the shape as

$$I \in \{0,1,\ldots,255\}^{H\times W\times C},\qquad C=3.$$

Here $I$ is the stored image, $H$ is its number of rows (height), $W$ is its number of columns (width) and $C$ is the number of channels. The notation says each entry is one integer from 0 through 255. It is a description of the array, not a multiplication of pixel values.

**Numerical example:** height 2, width 3 and 3 channels require 18 channel values across 6 pixels.

```python
import numpy as np

image = np.zeros((2, 3, 3), dtype=np.uint8)
print(image.shape, image.size)  # (2, 3, 3), 18
image[0, 1] = [255, 0, 0]  # red at row 0, column 1
```

`image[y, x, c]` means row, column, channel. Row `y` increases down the displayed image; column `x` increases to the right. A point written geometrically as `(x, y)` must therefore be converted to `[y, x]` for array indexing. This matters in cropping, annotation and drawing.

A grayscale array has shape `(H, W)`. A color array has shape `(H, W, 3)`. These are not interchangeable simply because both can be plotted. Later ML frameworks also use layouts such as `(channels, height, width)` and batches; always write the contract down.

## 6. Dtype and storage

`uint8` means an unsigned integer represented with eight bits. Its range is

$$0 \leq v \leq 2^8-1 = 255.$$

$v$ is one stored channel value. Eight binary digits have 256 possible combinations, counted from zero. For example, a black RGB pixel is `(0, 0, 0)` and a white one is `(255, 255, 255)` in this representation. A value such as 270 cannot be represented directly.

The array's element storage is

$$B = H\,W\,C\,s,$$

where $B$ is bytes, and $s$ is bytes per element. **Example:** $2\cdot3\cdot3\cdot1=18$ bytes for the tiny RGB image. This excludes the Python array object's own overhead and any temporary arrays.

```python
print(image.dtype.itemsize)  # 1 byte per uint8 element
print(image.nbytes)  # 18 bytes of array elements
```

Storage reasoning becomes important for video queues and neural-network batches. A `float64` image uses eight bytes per value rather than one. Do not call `.nbytes` a peak-memory measurement.

## 7. Safe brightness arithmetic

For this lesson, additive brightness is

$$J_{yxc}=\operatorname{clip}(I_{yxc}+\Delta,0,255).$$

$I$ is the original, $J$ is the edited image, $(y,x,c)$ selects a channel value, and $\Delta$ is the same added offset everywhere. `clip(value, 0, 255)` means values below zero become zero and values above 255 become 255. We round fractional values to the nearest integer; ties use the implementation's explicit round-to-even convention.

**Intuition:** move the intensity numbers up or down, but stop at the display range's edges.

**Example:** with $\Delta=20$, `(250, 10, 0)` becomes `(255, 30, 20)`. With $\Delta=-20$, the same pixel becomes `(230, 0, 0)`.

```python
pixel = np.array([250, 10, 0], dtype=np.uint8)
result = np.rint(np.clip(pixel.astype(np.float64) + 20, 0, 255)).astype(np.uint8)
print(result)  # [255, 30, 20]
```

Conversion happens **before** arithmetic. Adding equal-shaped `uint8` arrays can wrap at 256; 250 plus 20 becomes 14. Some scalar operations may also reject out-of-range values depending on the operation and NumPy version. Neither behavior implements the desired clipping rule. Casting an already-wrapped result to float cannot recover the lost number.

Brightness adjustment is useful for a controlled preprocessing experiment. It does not recover saturated detail, fix all illumination differences or calibrate exposure. Clipping is irreversible: many different large values map to 255.

## 8. Indexing, slices, views and copies

Select one red value with `image[y, x, 0]`. Select all channels at a point with `image[y, x]`. Select a region with `image[y0:y1, x0:x1]`; the stop indices are exclusive. Thus `[1:4, 2:6]` selects three rows and four columns.

Basic NumPy slices can share data with the original. Such an array is a **view**, like a window onto the same spreadsheet. Editing the window changes the underlying values. `.copy()` creates independent storage, like photocopying those cells.

```python
original = np.zeros((4, 6, 3), dtype=np.uint8)
view = original[1:3, 2:5]
view[:] = [255, 0, 0]  # original changes
independent = original[1:3, 2:5].copy()
independent[:] = 0  # original does not change this time
```

Use views deliberately for efficient read-only access; use copies when you need an independent edited result. Advanced indexing has different copy behavior, so consult the array operation's contract rather than assuming every selection is a view. The public crop function always returns a copy.

## 9. Broadcasting and channel gains

To multiply channels by separate gains,

$$J_{yxc}=\operatorname{clip}(I_{yxc}g_c,0,255).$$

$g_c$ is the multiplier for channel $c$. A gain vector `(1.2, 1.0, 0.5)` makes red 20% larger, leaves green unchanged and halves blue, before rounding/clipping.

**Example:** `(100, 80, 40)` becomes `(120, 80, 20)`.

```python
pixel = np.array([[[100, 80, 40]]], dtype=np.uint8)
gains = np.array([1.2, 1.0, 0.5])
edited = np.rint(np.clip(pixel.astype(float) * gains, 0, 255)).astype(np.uint8)
```

For a full image, shape `(H, W, 3)` combines with shape `(3,)`. NumPy aligns dimensions from the right; matching sizes or a size of one can be combined. This is **broadcasting**. We do not need a Python loop to repeat the same three gains over every pixel. Incompatible shapes should fail instead of silently guessing your intent.

Multiplying by gains is a useful toy color-balance operation. It is not a calibrated white-balance method and does not account for sensor response or color profiles. Order matters when combined with clipping: adding 20 to 250, clipping to 255, then halving gives 128 after rounding; halving first and adding gives 145.

## 10. Grayscale as a weighted sum

A familiar grayscale approximation is

$$G_{yx}=0.299R_{yx}+0.587G^{(\text{green})}_{yx}+0.114B_{yx}.$$

The left-hand $G$ is the grayscale result; $R$, $G^{(\text{green})}$ and $B$ on the right are encoded red, green and blue channel values. We use different notation for the green channel so it is not confused with the output. The weights sum to one.

**Intuition:** combine three numbers into one while making green contribute more than blue. **Example:** pure red `(255, 0, 0)` produces $0.299\cdot255=76.245$, which rounds to 76. Pure green rounds to 150 and pure blue to 29.

```python
weights = np.array([0.299, 0.587, 0.114])
values = (image.astype(float) * weights).sum(axis=2)
gray = np.rint(values).astype(np.uint8)
```

Summing `axis=2` collapses the channel axis while keeping rows and columns. A simple average `(R+G+B)/3` is a different transform. OpenCV's `COLOR_RGB2GRAY` gives a practical comparison; implementation rounding can cause a one-level difference. The loop and NumPy references implement the same stated formula.

This operation is useful before intensity-based algorithms. It discards color distinctions. These coefficients applied directly to encoded RGB values are **not physical luminance** and are not a substitute for color calibration or linear-light calculations.

## 11. Summaries and histograms

The average of $N$ values is

$$\mu=\frac{1}{N}\sum_{i=1}^{N}v_i.$$

$\mu$ is the mean, $v_i$ is value $i$, and $N$ is the count. The sigma symbol means “add them all.” **Example:** `(10+20+30)/3 = 20`.

```python
values = np.array([10, 20, 30])
print(values.mean())
mean_rgb = image.mean(axis=(0, 1))
```

Averaging rows and columns keeps one mean per channel. Mean intensity is a useful descriptor of a preprocessing change, not a quality score.

A histogram counts how often each value occurs. For one channel, `np.bincount(channel.ravel(), minlength=256)` returns 256 counts. The counts must sum to the number of pixels. A black/white checkerboard and a black/white split image can have the same histogram while having very different spatial arrangements. Counting discards location.

## 12. RGB, BGR and visualization

The package's public arrays are RGB. OpenCV image decoding commonly produces BGR, placing blue first. `cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)` changes that order explicitly. Passing RGB to a function expecting BGR can exchange red and blue without producing an error.

```python
import cv2

bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
restored = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
assert np.array_equal(restored, image)
```

Matplotlib expects RGB for three-channel color arrays. For a single-channel image, use `cmap='gray', vmin=0, vmax=255` to keep the same display scale across plots. Without fixed limits, automatic scaling may exaggerate or hide differences. Label axes as columns/x and rows/y; never infer physical millimeters from pixels alone.

## 13. Paths, reading, writing and errors

`Path('datasets') / 'synthetic' / 'scene.png'` builds a portable relative path. Relative paths begin at the current working directory, not necessarily where a notebook file lives. A saved report should tell you what data and parameters produced it without depending on someone else's personal directory.

A context manager (`with Image.open(path) as opened:`) closes resources when the block ends, including after an exception. An exception is a structured failure. Catch expected input failures and offer a useful message; do not catch everything and pretend success.

The loader checks that the file exists, limits decoded pixels, rejects unsupported scientific/16-bit and animated input, honors EXIF orientation and composites transparency on white. It converts common 8-bit modes to RGB. The lesson does not implement color-profile management; output PNGs omit original metadata. Keep original scientific or color-critical files untouched.

PNG supports lossless pixel round trips for our arrays. JPEG is lossy: it should not be used for an exact equality assertion. File size is also not the same as in-memory array storage, because encoding and metadata change the byte count.

## 14. Vectorization and fair comparison

A Python loop visits each pixel and channel explicitly. Vectorized code expresses the same operation on whole arrays, where numerical libraries perform the repeated work. The shorter expression is useful only after you understand the underlying operation.

For speed comparison, define a ratio

$$S = t_{\text{loop}} / t_{\text{array}},$$

where both times measure the same workload in the same unit. A hypothetical 12 ms loop and 3 ms array operation would give $S=4$. This is an arithmetic illustration, **not a measured result**. Notebook 04 measures its own values.

Warm up each method, repeat it, retain raw times, compare medians and check output correctness. Exclude unrelated disk I/O from an arithmetic timing. Array size, allocation, caching, CPU power behavior, threads and background work can affect results. Small-array runtime cannot be converted into an end-to-end webcam FPS claim. An array's `.nbytes` excludes temporaries and process overhead.

## 15. What next?

Complete the notebooks, solve the three exercise levels and build Pixel Lab. Then apply it to a new image that you have permission to use. Explain both the intended change and any information loss. Chapter 02 expands these arithmetic ideas into mathematical tools; Chapter 03 goes deeper into image representation; Chapter 04 introduces broader OpenCV I/O and interaction.

## References

[Python tutorial](https://docs.python.org/3/tutorial/), [NumPy arrays](https://numpy.org/doc/stable/user/quickstart.html), [broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html), [OpenCV basic operations](https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html), [Pillow image modes](https://pillow.readthedocs.io/en/stable/handbook/concepts.html). See the repository [reference guide](../../docs/references.md) for research connections.
