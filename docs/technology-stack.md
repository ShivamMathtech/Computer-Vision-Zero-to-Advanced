# Technology stack

| Layer | Libraries | Role and boundary |
|---|---|---|
| Foundations | Python, NumPy | Arrays, loops, vectorization, math and explicit algorithms |
| Visualization | Matplotlib, Pillow | Plots, image I/O and small generated assets |
| Classical CV | OpenCV, SciPy | Filtering, features, masks, motion, calibration and geometry |
| Classical ML | scikit-learn | Splits, scaling, classifiers, PCA and metrics |
| Deep learning | PyTorch | Explicit tiny-model training, inference and checkpoints |
| Pretrained families | torchvision, Ultralytics, Transformers | Optional real-model workflows; weights downloaded explicitly |
| Landmark/3D tools | MediaPipe, Open3D | Optional supplied-model landmarks and point-cloud files |
| Export | ONNX, ONNX Runtime | Graph validation and actual CPU output comparison |
| Service | FastAPI, Uvicorn, SQLite | Local API, session state and numeric event persistence |
| Interface | HTML, CSS, browser JavaScript | Local dashboard with synthetic/image/video/webcam input |
| Quality | pytest, Ruff, nbformat, ipykernel | Meaningful checks and isolated notebook execution |
| Packaging | setuptools, Docker/Compose configuration | Installable Python package and local-service container recipe |

TensorFlow/Keras are not required: this course uses one deep-learning framework consistently to avoid making beginners learn two APIs at once. Streamlit/Gradio integration is illustrated in the deployment guide as optional UI alternatives.
