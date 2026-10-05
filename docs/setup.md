# Environment setup

Use **Python 3.12** for the validated environment. The package declares Python 3.11–3.13; the release was executed on Linux/Python 3.12. Windows/macOS and the other declared Python versions have setup instructions and CI configuration, but were not run in this build.

## Windows: first-time setup

1. Install Python 3.12 from [python.org](https://www.python.org/downloads/). Enable **Add python.exe to PATH** in the installer.
2. Right-click the downloaded ZIP and choose **Extract All**. Open the extracted `computer-vision-from-zero-to-advanced` folder.
3. Click the folder address bar, type `powershell`, and press Enter. The commands below use the virtual environment's Python directly, so changing PowerShell execution policy is unnecessary.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -e ".[notebooks,deep,api,dev,export]"
.\.venv\Scripts\python.exe -m cvzero doctor
.\.venv\Scripts\python.exe -m jupyter lab
```

Jupyter prints a local URL and usually opens your browser. Open `01-python-for-computer-vision/notebooks/01_python_and_images.ipynb`. Choose **Run → Run All Cells**. Keep the PowerShell window open while using Jupyter; Ctrl+C stops it.

To run a chapter lab without notebooks:

```powershell
.\.venv\Scripts\python.exe -m cvzero.course --chapter 5 --lesson 0 --output artifacts/ch05-run1
```

Use a different output directory on the next run. The tool intentionally refuses to overwrite a nonempty report folder.

## Linux and macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# Linux CPU wheel; on macOS use: python -m pip install torch
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e ".[notebooks,deep,api,dev,export]"
python -m cvzero doctor
python -m jupyter lab
```

The core-only path is `python -m pip install -e ".[notebooks]"`. It covers Python, image processing, geometry, classical ML and other non-PyTorch labs. For a uniform all-chapter environment, install the deep and API extras above. Beginner notebooks do not import PyTorch.

## Dependency layers

| Layer | Installation | Used for |
|---|---|---|
| Core | `pip install -e .` | NumPy, plotting, OpenCV, Pillow, SciPy, scikit-learn |
| Notebooks | `pip install -e ".[notebooks]"` | Jupyter and notebook execution |
| Deep learning | `pip install -e ".[deep]"` | Tiny CNN, U-Net, ViT, SSL, generation, NeRF |
| API | `pip install -e ".[api]"` | Capstone and Chapter 50 |
| Export | `pip install -e ".[export]"` | ONNX and ONNX Runtime comparison |
| Development | `pip install -e ".[dev]"` | Tests, formatting and package build |
| Optional models | See external workflows | torchvision, Ultralytics, Transformers, MediaPipe, Open3D |

`constraints-validated.txt` records versions used in this release. It is a tested-version snapshot, not a universal cross-platform lockfile. Install the matching CPU PyTorch wheel before using its constraint. External model packages are kept separate because hardware, Python support and licenses vary.

## GPU and Colab

All shipped default lessons run on CPU, including small training experiments. For larger real-data training, select a PyTorch build appropriate to your hardware from the [official installation guide](https://pytorch.org/get-started/locally/). Never assume CUDA is present. [Colab instructions](colab.md) explain how to upload and install this ZIP.

## Common setup problems

- **Python not found:** restart the terminal after installing Python, then run `py --list` on Windows.
- **No module named cvzero:** install `-e .` from the repository root using the same Python that runs Jupyter.
- **Wrong notebook kernel:** launch Jupyter through `.venv` Python, or register that environment with `python -m ipykernel install --user --name cvzero --display-name "CV Zero"`.
- **Image missing:** use an existing path or the generated-data command; examples report missing files explicitly.
- **Camera unavailable:** use generated video first, then check device index, browser permission and whether another app has the camera open.
- **OpenCV GUI unavailable:** notebooks use `opencv-python-headless`. For `opencv_interactive.py`, create a separate desktop environment, uninstall conflicting OpenCV wheels and install `opencv-python`. Do not install headless and GUI wheels together.
- **Model missing:** provide a local model path or opt into the documented download command. Default notebooks need no separate weight downloads; Chapter 19 uses OpenCV’s bundled Haar cascade.
- **CUDA unavailable:** keep `--device cpu`; the small models are designed for it.
- **Port 8000 in use:** choose `--port 8001` and open the corresponding localhost URL.
