# Open in Google Colab

All 160 default lesson notebooks use generated or packaged data and support CPU execution. Colab is a hosted environment with changing dependencies; this release was validated locally, not in a live Colab session. No account/repository-specific badge is fabricated.

1. Open [Google Colab](https://colab.research.google.com/) and select **File → Upload notebook**. Choose a chapter `.ipynb`.
2. Upload the repository ZIP through the Files panel on the left.
3. Add this setup cell before the first lesson cell, using the actual uploaded ZIP filename:

```python
from pathlib import Path
from zipfile import ZipFile
import subprocess
import sys

archive = Path("Computer-Vision-Zero-to-Advanced-v1.0.0.zip")
with ZipFile(archive) as bundle:
    bundle.extractall("course")  # Extract this trusted release only.
repo = Path("course/computer-vision-from-zero-to-advanced").resolve()
subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", f"{repo}[notebooks,deep,api]"])
```

4. Restart the runtime if requested after package changes, then rerun imports and use **Runtime → Run all**.
5. Keep CPU selected for the baseline. Optional external training can use a GPU runtime if available; check `torch.cuda.is_available()` before selecting CUDA.
6. Download saved outputs before the temporary Colab session ends. No notebook depends on a hardcoded personal filesystem path.

The static preview image may not display when only one notebook is uploaded; the executed visualization cells generate their own images. After publishing your own GitHub copy, use Colab's GitHub tab and actual repository URL to create working notebook badges.
