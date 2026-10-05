# First-chapter glossary

| Term | Plain meaning | Example |
| --- | --- | --- |
| Variable | A name referring to a value | `width = 4` |
| Function | A reusable operation with inputs and a result | `adjust_brightness(image, 20)` |
| Class | A definition of objects that group state and behavior | An editor with an image and an `apply` method |
| List | An ordered Python collection | `[255, 0, 0]` |
| Dictionary | Values looked up by names or keys | `{"brightness": 20}` |
| Array | A grid of values with a consistent dtype | A `uint8` RGB image |
| Shape | Length along every axis | `(2, 3, 3)` = 2 rows, 3 columns, 3 channels |
| Pixel | One image location | Three channel values at `image[y, x]` |
| Channel | One component of each pixel | Red is channel 0 in RGB |
| Dtype | The kind and storage size of array elements | `uint8` stores integers 0–255 |
| Slice | A selected region using start and exclusive stop | `image[1:3, 2:5]` |
| View | An array that shares underlying data | A basic NumPy slice |
| Copy | Independent array storage | `image.copy()` |
| Broadcasting | Applying compatible smaller-shaped values across axes | Multiply an RGB image by three channel gains |
| Vectorization | Expressing whole-array work in array operations | `image.astype(float) + 20` |
| Clipping | Stopping values at specified bounds | 270 becomes 255 |
| Seed | A starting value for a pseudorandom generator | `np.random.default_rng(42)` |
| Histogram | Counts for value bins | Number of red pixels at each intensity |
| Benchmark | A specified repeatable timing or resource experiment | Same image and operation across implementations |
| Kernel | The Python process behind a notebook | Restarting removes hidden variables |
