# Optional real-data and pretrained workflows

The 160 default notebooks execute without downloads. This guide extends their mechanics to external datasets and pretrained models. These adapters were syntax/import-path reviewed, but pretrained weights, live cameras and external dataset training were **not executed** in the release build. Review the model card, dataset terms and installed library version before using them.

## Custom YOLO: complete workflow

1. **Dataset:** create a small annotated synthetic dataset, or prepare your own permissioned images. For real data, keep frames from the same video/source in one split.
2. **Annotation:** one text row per object, `class_id center_x center_y width height`, normalized by image dimensions. Empty files represent valid negative images. Draw label overlays and check class definitions before training.
3. **Validation:** verify ranges, paired files and duplicate images; this script supplies those checks for its PNG shape dataset.

```bash
python scripts/prepare_yolo_dataset.py --output datasets/generated-yolo
python scripts/prepare_yolo_dataset.py --output datasets/generated-yolo --validate-only
python -m pip install ultralytics
python scripts/external_models.py yolo-train --model yolo11n.yaml --data datasets/generated-yolo/dataset.yaml --epochs 10 --device cpu --output artifacts/yolo-training
```

`yolo11n.yaml` explicitly selects an available model-family configuration for a scratch demonstration; this is not a claim that it is the latest version. You can instead supply a compatible local model YAML or pretrained `.pt` path. Ultralytics can download assets for explicitly selected model names; review its [training](https://docs.ultralytics.com/modes/train/), [license](https://www.ultralytics.com/license) and installed-version documentation. The synthetic set teaches plumbing; train on appropriate real data for real categories.

4. **Evaluation:** use validation during development, then evaluate the held-out test after freezing decisions.

```bash
python scripts/external_models.py yolo-evaluate --model artifacts/yolo-training/train/weights/best.pt --data datasets/generated-yolo/dataset.yaml --output artifacts/yolo-test
```

5. **Inference and visualization:**

```bash
python scripts/external_models.py yolo-predict --model artifacts/yolo-training/train/weights/best.pt --image datasets/generated-yolo/images/test/0000.png --output artifacts/yolo-predict
```

6. **Export and deployment:**

```bash
python scripts/external_models.py yolo-export --model artifacts/yolo-training/train/weights/best.pt --output artifacts/yolo-export
```

The exporter reports the actual model path; exported files may be written beside source weights by the external library. Check output agreement before selecting a new runtime. To use trained weights in the capstone, set `CVZERO_MODEL` to that existing `.pt` path and launch the API. No synthetic mAP is advertised as real-object performance.

## Real-data classification and transfer

Install a compatible torchvision build using [PyTorch's installation guidance](https://pytorch.org/get-started/locally/). Arrange `datasets/my-classifier/{train,val,test}/{class-name}/*.jpg`. Class folders must match across splits. Group sources before copying images; the generic ImageFolder loader cannot infer duplicate capture sessions.

```bash
python scripts/train_classifier.py --data datasets/my-classifier --model resnet18 --pretrained --freeze-backbone --epochs 5 --device cpu --output artifacts/transfer-frozen
python scripts/train_classifier.py --data datasets/my-classifier --model mobilenet_v3_small --pretrained --epochs 5 --device cpu --output artifacts/transfer-finetuned
```

The script selects weights on validation loss, reloads the best checkpoint and evaluates the test split afterward. It writes weights and an experiment manifest. Use the same model family when isolating freezing versus fine-tuning; the two example commands also illustrate selectable backbones. EfficientNet-B0 is supported. The torchvision inference adapter supports compatible model names, including ViT:

```bash
python scripts/external_models.py classify --model resnet18 --download-weights --image path/to/image.jpg --output artifacts/pretrained-classification
```

## Semantic and instance segmentation

The CPU course trains a tiny U-Net on generated masks. These optional commands run real pretrained torchvision models:

```bash
python scripts/external_models.py semantic --download-weights --image path/to/image.jpg --output artifacts/deeplab
python scripts/external_models.py instance --download-weights --image path/to/image.jpg --output artifacts/maskrcnn
```

Semantic output is a PNG of integer class IDs with the class list in JSON. Instance output is a compressed archive of boxes, masks, labels and scores. These commands do not fine-tune on a medical dataset or establish diagnostic performance.

## Image–text retrieval, captioning and VQA

```bash
python -m pip install transformers torchvision
python scripts/external_models.py clip --download-weights --image path/to/image.jpg --text "a bicycle" "a dog" "a building" --output artifacts/clip
python scripts/external_models.py caption --download-weights --image path/to/image.jpg --output artifacts/caption
python scripts/external_models.py vqa --download-weights --image path/to/image.jpg --question "What objects are visible?" --output artifacts/vqa
```

Default model IDs are `openai/clip-vit-base-patch32`, `Salesforce/blip-image-captioning-base` and `Salesforce/blip-vqa-base`. Without `--download-weights`, the loader uses local cached files only. Candidate-set CLIP scores are relative; generated captions/answers can be wrong. See [Transformers CLIP](https://huggingface.co/docs/transformers/model_doc/clip) and [BLIP](https://huggingface.co/docs/transformers/model_doc/blip).

## Landmarks and OCR

```bash
python -m pip install mediapipe pytesseract
python scripts/external_models.py hands --model path/to/hand_landmarker.task --image path/to/image.jpg --output artifacts/hands
python scripts/external_models.py pose --model path/to/pose_landmarker.task --image path/to/image.jpg --output artifacts/pose
python scripts/external_models.py ocr --image path/to/page.png --output artifacts/ocr
```

Obtain compatible `.task` files from the official [hand](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) or [pose](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker) guide. Tesseract needs its separate system executable and language data on PATH; `pytesseract` alone is not the engine. The default OCR notebook uses fixed-font templates so it needs neither dependency.

## Point clouds and model export

```bash
python -m pip install open3d
python scripts/external_models.py point-cloud --data path/to/cloud.ply --output artifacts/cloud
python -m pip install -e ".[deep,export]"
python scripts/export_model.py --output artifacts/onnx-export
```

Unlike the optional pretrained runs, the tiny-model ONNX export/runtime comparison was actually executed in the release. The script explicitly uses PyTorch's legacy exporter for this small static architecture; current PyTorch recommends its dynamo exporter for new work. Record exporter, opset and runtime versions when changing it.

## Alternative local interfaces

FastAPI serves the shipped dashboard. For a small experiment, these optional wrappers can call the same `Engine` from Streamlit or Gradio:

```python
# Save as app_streamlit.py, then: streamlit run app_streamlit.py
import numpy as np
import streamlit as st
from PIL import Image
from cvzero.platform.engine import Engine

st.title("CV Zero image inspection")
file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
if file:
    report, overlay = Engine().analyze(np.array(Image.open(file).convert("RGB")))
    st.image(overlay)
    st.json(report)
```

```python
# Save as app_gradio.py, then: python app_gradio.py
import gradio as gr
from cvzero.platform.engine import Engine


def inspect_image(image):
    report, overlay = Engine().analyze(image)
    return overlay, report


gr.Interface(
    inspect_image, gr.Image(type="numpy", image_mode="RGB"), [gr.Image(), gr.JSON()]
).launch(server_name="127.0.0.1")
```

Install the chosen optional UI package separately. These concise alternative-interface examples are not part of the executed notebook gate.
