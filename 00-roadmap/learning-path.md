# Learning progression

The chapter numbers are stable navigation addresses. Study in order, taking the short attention primer during Chapter 37 before its ViT implementation. Prerequisite numbers identify especially useful prior knowledge, not permission to skip the rest of the foundation.

| Chapter | Prior concepts | Learning outcome | Mini project |
|---|---|---|---|
| [01 · Python for Computer Vision](../01-python-for-computer-vision/README.md) | Basic Python | Build a reliable image editor and explain each pixel operation | Pixel Lab |
| [02 · Mathematics for Computer Vision](../02-mathematics-for-computer-vision/README.md) | 01 | Translate small equations into array operations before using models | Visual Math Workbook |
| [03 · Image Fundamentals](../03-image-fundamentals/README.md) | 01, 02 | Explain sampling, quantization and image memory | Image Inspector |
| [04 · OpenCV Fundamentals](../04-opencv-fundamentals/README.md) | 01, 03 | Build image and webcam tools with useful failure messages | Paint and Webcam Viewer |
| [05 · Image Processing](../05-image-processing/README.md) | 02, 04 | Implement a sliding window and compare denoising methods | Image Restoration Lab |
| [06 · Image Enhancement](../06-image-enhancement/README.md) | 05 | Choose an enhancement method using image evidence | Image Enhancement Studio |
| [07 · Geometric Transformations](../07-geometric-transformations/README.md) | 02, 04 | Map coordinates correctly and control resampling artifacts | Document Rectifier |
| [08 · Color Spaces](../08-color-spaces/README.md) | 03, 04 | Isolate a colored object while testing illumination changes | Color Object Tracker |
| [09 · Feature Detection](../09-feature-detection/README.md) | 02, 05 | Find repeatable image locations and explain detector tradeoffs | Corner Explorer |
| [10 · Feature Description and Matching](../10-feature-description-and-matching/README.md) | 07, 09 | Reject false matches before estimating a geometric map | Image Stitching System |
| [11 · Morphological Image Processing](../11-morphological-image-processing/README.md) | 05, 08 | Clean binary masks without destroying useful structure | Document Cleanup Pipeline |
| [12 · Contours and Shapes](../12-contours-and-shapes/README.md) | 07, 11 | Measure image shapes and distinguish pixels from physical units | Shape Measurement System |
| [13 · Edge and Corner Detection](../13-edge-and-corner-detection/README.md) | 05, 09 | Construct a simplified Canny pipeline and evaluate noise effects | Document Boundary Detector |
| [14 · Classical Segmentation](../14-segmentation-classical/README.md) | 08, 11, 13 | Separate regions with explicit assumptions and evaluation | Classical Segmentation Lab |
| [15 · Video Processing](../15-video-processing/README.md) | 04, 08, 14 | Process finite files and release camera resources reliably | Motion and Traffic Counter |
| [16 · Camera and Calibration](../16-camera-and-calibration/README.md) | 02, 07 | Calibrate a camera and validate on held-out board views | Camera Calibration Toolkit |
| [17 · Motion Detection](../17-motion-detection/README.md) | 14, 15 | Detect scene change without confusing it with object identity | Motion Detector |
| [18 · Object Tracking](../18-object-tracking/README.md) | 12, 15, 17 | Follow a visible object and explain when its identity is uncertain | Ball Tracker |
| [19 · Face Detection](../19-face-detection/README.md) | 09, 12, 15 | Evaluate face boxes on consented examples without identity claims | Consented Face Detection Demo |
| [20 · Face Recognition](../20-face-recognition/README.md) | 02, 19 | Study small consented verification experiments with error analysis | Local Opt-in Verification Lab |
| [21 · OCR](../21-ocr/README.md) | 07, 11, 13 | Extract text while preserving reading order and error evidence | Document OCR Pipeline |
| [22 · Machine Learning for Vision](../22-machine-learning-for-vision/README.md) | 02, 09, 14 | Evaluate a baseline with a genuinely held-out split | Digit and Defect Classifier |
| [23 · CNN Fundamentals](../23-cnn-fundamentals/README.md) | 02, 05, 22 | Derive a tiny network update and compare fixed and learned filters | Tiny CNN from First Principles |
| [24 · PyTorch for Computer Vision](../24-pytorch-for-computer-vision/README.md) | 23 | Write a reproducible training and validation loop | Reusable Training Engine |
| [25 · Image Classification](../25-image-classification/README.md) | 22, 24 | Train a classifier and report per-class failures | Vehicle or Plant Classifier |
| [26 · Transfer Learning](../26-transfer-learning/README.md) | 25 | Compare frozen features against controlled fine-tuning | Industrial Defect Classifier |
| [27 · Object Detection](../27-object-detection/README.md) | 12, 22, 24, 26 | Implement IoU and NMS before calling a detector API | Detection Evaluation Toolkit |
| [28 · YOLO](../28-yolo/README.md) | 27 | Run an auditable custom detector workflow | Custom YOLO Detector |
| [29 · Object Segmentation](../29-object-segmentation/README.md) | 14, 24, 27 | Match segmentation formulations to an industrial question | Segmentation Task Explorer |
| [30 · Instance Segmentation](../30-instance-segmentation/README.md) | 27, 29 | Keep object identity when masks overlap | Instance Counting System |
| [31 · Semantic Segmentation](../31-semantic-segmentation/README.md) | 29 | Train and inspect a dense labeling model | Industrial Surface Segmentation |
| [32 · Pose Estimation](../32-pose-estimation/README.md) | 24, 27 | Visualize joints with uncertainty and safe exercise feedback | Exercise Counter |
| [33 · Hand Tracking](../33-hand-tracking/README.md) | 18, 32 | Convert landmarks into reversible desktop interactions | Virtual Pointer Simulator |
| [34 · Action Recognition](../34-action-recognition/README.md) | 15, 24, 32 | Classify visible actions without inferring private mental states | Action Sequence Classifier |
| [35 · Optical Flow](../35-optical-flow/README.md) | 02, 13, 15, 18 | Estimate apparent motion and test its assumptions | Flow Visualization Lab |
| [36 · Multi-Object Tracking](../36-multi-object-tracking/README.md) | 18, 27, 35 | Evaluate association separately from detection quality | Vehicle Tracking System |
| [37 · Vision Transformers](../37-vision-transformers/README.md) | 24, 25 | Implement small attention first, then a simplified ViT | Tiny Vision Transformer |
| [38 · Attention Mechanisms](../38-attention-mechanisms/README.md) | 02, 23, 24 | Investigate the attention mechanism introduced in Chapter 37 | Attention Inspector |
| [39 · Self-Supervised Learning](../39-self-supervised-learning/README.md) | 26, 38 | Compare representations with fixed evaluation protocols | Self-Supervised Representation Lab |
| [40 · Vision-Language Models](../40-vision-language-models/README.md) | 38, 39 | Measure retrieval and prompt sensitivity with documented model licenses | Image-Text Search |
| [41 · Multimodal Computer Vision](../41-multimodal-computer-vision/README.md) | 16, 35, 40 | Combine visual and nonvisual observations without hiding missing data | RGB and Sensor Fusion Lab |
| [42 · Generative Computer Vision](../42-generative-computer-vision/README.md) | 23, 24, 39 | Separate reconstruction quality from distribution coverage | Generative Shapes Lab |
| [43 · Diffusion Models for Vision](../43-diffusion-models-for-vision/README.md) | 02, 38, 42 | Explain noise prediction before using a pretrained generator | Tiny Diffusion Experiment |
| [44 · 3D Computer Vision](../44-3d-computer-vision/README.md) | 07, 16, 35 | Recover geometry while tracking coordinate frames and scale ambiguity | Two-View Geometry Lab |
| [45 · Depth Estimation](../45-depth-estimation/README.md) | 31, 44 | Evaluate depth without pretending image estimates are measurements | Depth Inspector |
| [46 · Stereo Vision](../46-stereo-vision/README.md) | 16, 44, 45 | Convert calibrated disparity into depth with valid masks | Stereo Depth Toolkit |
| [47 · Point Clouds](../47-point-clouds/README.md) | 44, 46 | Construct and inspect point clouds with units and frame labels | Point Cloud Workshop |
| [48 · Neural Radiance Fields](../48-neural-radiance-fields/README.md) | 24, 42, 44, 47 | Train a tiny synthetic scene and separate camera errors from model errors | Tiny NeRF Study |
| [49 · Model Optimization](../49-model-optimization/README.md) | 24, 27, 31, 37 | Benchmark speed, memory and accuracy on the same workload | Model Optimization Lab |
| [50 · Computer Vision Deployment](../50-computer-vision-deployment/README.md) | 49 | Serve a versioned model and validate requests and predictions | Production Vision API |
| [51 · Edge AI](../51-edge-ai/README.md) | 49, 50 | Measure performance under actual device constraints | Edge Inference Benchmark |
| [52 · Real-Time Computer Vision](../52-real-time-computer-vision/README.md) | 15, 36, 49, 50 | Keep displays responsive while processing bounded work queues | Real-Time Analytics Dashboard |
| [53 · Production Computer Vision](../53-production-computer-vision/README.md) | 41, 50, 51, 52 | Integrate, monitor and evaluate an end-to-end vision service | End-to-End Real-Time Vision Platform |

## Section checkpoints

After 04: create and inspect an image, explain a pixel operation and handle a bad path.
After 14: implement a neighborhood operation, compare a library version and design a mask/feature pipeline.
After 21: process a sequence, explain projection and distinguish motion, identity and text recognition errors.
After 31: define splits and losses, train a small network and evaluate boxes/masks without leakage.
After 36: reason about time, missed observations, IDs and landmark uncertainty.
After 43: implement attention, distinguish representation objectives and critique generated outputs.
After 48: state coordinate frames and units, triangulate points and distinguish training-view fit from 3D reconstruction.
After 53: reproduce a result, export/check a model, run the API and explain monitoring and rollback needs.

Do not assign yourself a fixed completion speed. Use the exercises and failure analysis to determine whether to continue. Advanced external-data projects can require substantially more compute and time than the small CPU lessons.
