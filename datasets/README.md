# Datasets and preparation policy

Default notebooks do not download large data. Generated images, masks, trajectories, glyphs and 3D geometry make the expected truth inspectable. Chapter 22 uses the small digit dataset packaged with scikit-learn. No external photographs, biometric collections or model weights are redistributed in this ZIP.

## Immediately runnable data

| Data | Creation | Where used |
|---|---|---|
| RGB shapes and gradients | `cvzero.synthetic.make_scene` | Python, image processing and features |
| Binary shapes/masks | `cvzero.course.classical.shapes` | Morphology, contours and segmentation |
| Moving colored objects | `cvzero.course.classical.video_frames` | Video, motion and analytics |
| Handwritten digits | [`sklearn.datasets.load_digits`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html) | Classical image classification |
| Labeled shape images | `cvzero.course.models.shape_data` | Tiny CNN/U-Net/ViT and generation |
| Camera/point geometry | Seeded NumPy generators in the spatial labs | Calibration, stereo, depth and 3D |
| Synthetic YOLO images/labels | `scripts/prepare_yolo_dataset.py` | Full annotation/training workflow |

```bash
python scripts/prepare_datasets.py --help
python scripts/prepare_yolo_dataset.py --output datasets/generated-yolo
python scripts/prepare_yolo_dataset.py --output datasets/generated-yolo --validate-only
```

The YOLO generator writes `images/{train,val,test}`, matching `labels/{train,val,test}`, `dataset.yaml` and `manifest.json`. Its counts are generated and recorded by the script, not attributed to an external benchmark. Each label is a normalized box and a declared class ID.

## Official external sources

| Dataset | Suitable practice | Official source and download guidance |
|---|---|---|
| CIFAR-10 | Multiclass classification | [University of Toronto](https://www.cs.toronto.edu/~kriz/cifar.html); opt-in torchvision adapter below |
| Oxford-IIIT Pet | Classification and segmentation trimaps | [Oxford VGG](https://www.robots.ox.ac.uk/~vgg/data/pets/); download images plus annotations or use the adapter |
| COCO | Detection, instance masks and keypoints | [COCO download page](https://cocodataset.org/#download); select a subset appropriate to disk/compute limits |
| MVTec AD | Industrial anomaly inspection | [MVTec official page](https://www.mvtec.com/research-teaching/datasets/mvtec-ad); obtain the category data through its download procedure and preserve its intended anomaly protocol |
| MOT17 | Anonymous multi-object tracking | [MOTChallenge](https://motchallenge.net/data/MOT17/); use permitted sequences and the official evaluation conventions |
| Middlebury stereo | Stereo matching and depth | [Middlebury](https://vision.middlebury.edu/stereo/data/); select calibrated pairs and read their disparity/scale conventions |

Review the current license on each official page. Repository MIT terms do not replace dataset or model licenses. MVTec's anomaly-only training setup is different from ordinary supervised defect classification; do not move labeled test defects into training while still claiming the original benchmark protocol. Educational medical-image extensions require suitable permissions and expert validation and are **not diagnostic tools**.

## Optional automated preparation

After installing a compatible torchvision build:

```bash
python scripts/download_dataset.py --name cifar10 --output datasets/raw --download
python scripts/download_dataset.py --name pets --output datasets/raw --download
```

Without `--download`, the script only opens an existing local copy. These optional downloads were not executed during this release. Inspect actual downloaded metadata and record version, license and checksum in your experiment manifest.

## Expected folder contracts

| Task | Contract |
|---|---|
| ImageFolder classifier | `my-classifier/train/<class>/*`, `val/<class>/*`, `test/<class>/*` |
| YOLO detector | `images/<split>/*`, `labels/<split>/*.txt`, YAML class map and split paths |
| Paired segmentation | `images/<split>/<id>.png`, `masks/<split>/<id>.png`, same dimensions and an explicit class/ignore map |
| Video tracking | sequence frames/video plus timestamp and object-ID annotations; split by sequence |
| Stereo | left/right images plus intrinsics, distortion, extrinsics and physical baseline units |

Do not assume Oxford trimap values are binary: inspect the label definitions and choose a boundary/ignore policy. Resize class masks with nearest-neighbor interpolation.

## Split integrity

Group related observations before splitting: the same video, specimen, subject, capture session or near-duplicate must not straddle train and test. Fit scaling, PCA, thresholds and augmentation choices using training/validation only. Store the exact split manifest. Dataset validation includes paired filenames, decode success, dimensions, label ranges, class distribution and duplicate hashes; visual annotation review is also required.

The `.gitignore` excludes raw/downloaded datasets, generated large experiment folders and model weights. Commit small synthetic fixtures and preparation code instead of full data.
