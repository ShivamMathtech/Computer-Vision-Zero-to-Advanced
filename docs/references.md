# Primary references

Primary library documentation was consulted while preparing this release on 2026-10-04. They explain library contracts; lessons use original small numerical examples. Documentation versions may advance independently of the tested package versions.

| Source | Why it is useful |
| --- | --- |
| [Python tutorial: control flow](https://docs.python.org/3/tutorial/controlflow.html) | Functions, loops and branching before image algorithms |
| [Python data structures](https://docs.python.org/3/tutorial/datastructures.html) | Lists and dictionaries used for pixels and configuration |
| [Python classes](https://docs.python.org/3/tutorial/classes.html) | Connecting state and behavior without prematurely building a framework |
| [Python pathlib](https://docs.python.org/3/library/pathlib.html) | Portable paths and file handling |
| [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) | Arrays, axes, operations and shape reasoning |
| [NumPy indexing](https://numpy.org/doc/stable/user/basics.indexing.html) | Indexing and slice semantics |
| [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) | How channel operations apply over an image |
| [OpenCV basic image operations](https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html) | Image arrays, rows/columns and BGR ordering |
| [Matplotlib imshow](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html) | Plotting conventions and scalar display ranges |
| [Pillow Image API](https://pillow.readthedocs.io/en/stable/reference/Image.html) | Image decoding, modes and decompression limits |
| [Packaging Python projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) | Installable source layout and project metadata |
| [nbclient execution](https://nbclient.readthedocs.io/en/latest/client.html) | Fresh-kernel notebook execution |

## Research connection for Chapter 01

**Harris et al., “Array programming with NumPy,” 2020.** [Paper](https://arxiv.org/abs/2006.10256). The contribution is an array-oriented numerical programming foundation and ecosystem, not a new image classifier. Its relevance here is that the same image calculation can be written as one operation on whole arrays. Learners can inspect how shape, memory and vectorized operations interact before moving to learned tensor computations. This does not remove intermediate allocations or guarantee a speedup for every small input. Later GPU tensor libraries build on related array ideas while introducing devices, automatic differentiation and synchronization.

## Advanced readings and API contracts

The [research companion](research-reading.md) explains influential papers, their contributions, architecture intuition, limitations and later alternatives. Each chapter also links its primary documentation or paper.

- [PyTorch quickstart](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
- [torchvision models](https://docs.pytorch.org/vision/stable/models.html)
- [Ultralytics training](https://docs.ultralytics.com/modes/train/), [validation](https://docs.ultralytics.com/modes/val/) and [export](https://docs.ultralytics.com/modes/export/)
- [Transformers CLIP](https://huggingface.co/docs/transformers/model_doc/clip) and [BLIP](https://huggingface.co/docs/transformers/model_doc/blip)
- [MediaPipe hand landmarks](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python) and [pose landmarks](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/python)
- [Open3D ICP](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html)
- [PyTorch ONNX](https://docs.pytorch.org/docs/stable/onnx.html), [ONNX Runtime](https://onnxruntime.ai/docs/) and [FastAPI](https://fastapi.tiangolo.com/tutorial/)

Primary pages were checked during preparation. Optional adapters must still be tested against the chosen model, installed versions and target hardware; source-document review is not an execution claim.
