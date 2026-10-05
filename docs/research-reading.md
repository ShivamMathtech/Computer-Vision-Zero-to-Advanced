# Research reading companion

Original contributions, useful intuition and limitations. Publication/preprint years are stated explicitly; later revisions may have different dates.

## Chapter 01

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 02

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 03

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 04

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 05

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 06

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 07

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 08

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 09

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 10

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 11

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 12

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 13

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 14

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 15

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 16

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 17

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 18

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 19

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 20

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 21

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 22

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 23

**LeNet-5 / Gradient-Based Learning Applied to Document Recognition (1998).** Jointly learned convolutional features and a classifier connected representation learning to document recognition. Shared filters and subsampling offered a useful image-specific architecture. Its original scale and tasks differ greatly from current vision workloads; residual networks and transformers are later alternatives.

[Read the original paper](http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 24

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 25

**Deep Residual Learning for Image Recognition (2015).** Residual connections let a block learn a change around an identity path, helping optimize deeper image networks. A residual block adds its input to a learned transformation. Depth alone still does not solve domain shift or data quality; efficient convolutional designs and ViTs offer different tradeoffs.

[Read the original paper](https://arxiv.org/abs/1512.03385). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 26

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 27

**Faster R-CNN (2015).** A region proposal network shares convolutional features with the detector, integrating proposal generation into the learned system. The two-stage structure remains useful when inspecting proposal and classification behavior. Single-stage detectors and set-prediction detectors offer alternative latency and assignment choices.

[Read the original paper](https://arxiv.org/abs/1506.01497). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 28

**You Only Look Once (2015).** The original YOLO formulation predicted boxes and classes in one network evaluation, making detection a unified regression problem. It helped establish practical single-stage detection. Its grid assumptions and small-object limitations should not be projected onto every later YOLO-named implementation; inspect the chosen version.

[Read the original paper](https://arxiv.org/abs/1506.02640). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 29

**U-Net (2015).** An encoder–decoder with skip connections combines contextual features and localization. It became an influential segmentation pattern, particularly where dense labels are expensive. The original work does not make every U-Net clinically valid; later convolutional and transformer-based segmentation systems modify context and scaling.

[Read the original paper](https://arxiv.org/abs/1505.04597). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 30

**Mask R-CNN (2017).** Adding a parallel mask branch to a detector and using RoIAlign made instance masks a natural extension of two-stage detection. The separation of box, class and mask predictions is pedagogically useful. Query-based mask predictors provide another way to organize instances.

[Read the original paper](https://arxiv.org/abs/1703.06870). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 31

**Fully Convolutional Networks for Semantic Segmentation (2014).** Replacing image-level output with dense convolutional predictions enabled end-to-end semantic segmentation. Upsampling and skip information connect coarse semantics to pixel locations. Boundary detail remains difficult; U-Net and DeepLab introduce different localization and context mechanisms.

[Read the original paper](https://arxiv.org/abs/1411.4038). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 32

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 33

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 34

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 35

**RAFT (2020).** RAFT uses all-pairs correlation features and iterative updates for optical flow. It connects matching evidence with repeated refinement rather than one direct displacement prediction. Memory and domain generalization still matter; classical flow remains valuable for understanding assumptions and simple deployments.

[Read the original paper](https://arxiv.org/abs/2003.12039). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 36

**SORT and DeepSORT (2016).** SORT combines Kalman prediction and Hungarian assignment for online tracking. DeepSORT (2017, https://arxiv.org/abs/1703.07402) adds learned appearance matching. These papers clarify why detector quality and association both matter. Occlusion and crowding still cause identity errors; benchmark ID continuity separately from detection quality.

[Read the original paper](https://arxiv.org/abs/1602.00763). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 37

**An Image is Worth 16x16 Words (2020).** ViT applies a transformer to patch tokens, demonstrating the value of large-scale pretraining for image recognition without relying on a conventional convolutional backbone. Patch projection, positions and encoder blocks form its core. Small-data behavior and quadratic attention motivate data-efficient, hierarchical and windowed alternatives.

[Read the original paper](https://arxiv.org/abs/2010.11929). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 38

**Attention Is All You Need (2017).** The Transformer combines attention and position-wise transformations instead of recurrent sequence processing. Scaled dot products and multiple heads became reusable components for vision and multimodal systems. Full token-pair attention grows quadratically; sparse patterns and optimized attention kernels address different parts of this cost.

[Read the original paper](https://arxiv.org/abs/1706.03762). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 39

**SimCLR and BYOL (2020).** SimCLR studies contrastive representation learning with paired augmentations and a projection head. BYOL (https://arxiv.org/abs/2006.07733) uses an online predictor and slowly updated target without explicit negative pairs. These objectives changed how unlabeled images could train useful features. Augmentation choices and collapse behavior require careful evaluation; masked modeling is another family.

[Read the original paper](https://arxiv.org/abs/2002.05709). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 40

**CLIP / Learning Transferable Visual Models From Natural Language Supervision (2021).** A dual image/text encoder trained on paired data supports retrieval and text-defined classification. This changes the interface from a fixed trained label head to comparisons with candidate descriptions. Prompt sensitivity and training-data biases remain; captioning and VQA need additional generative or question-conditioned machinery.

[Read the original paper](https://arxiv.org/abs/2103.00020). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 41

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 42

**Auto-Encoding Variational Bayes and Generative Adversarial Nets (2013).** The VAE uses variational inference and reparameterized latent sampling. GANs (2014, https://arxiv.org/abs/1406.2661) instead learn through a generator/discriminator game. They offer different likelihood, reconstruction and optimization tradeoffs. Neither a low reconstruction loss nor a few attractive samples establishes distribution coverage; diffusion provides another generative route.

[Read the original paper](https://arxiv.org/abs/1312.6114). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 43

**Denoising Diffusion Probabilistic Models (2020).** DDPM connects a fixed noising process with a learned reverse process using a practical denoising objective. This makes iterative image generation understandable through noise schedules and time-conditioned prediction. Sampling cost motivates faster samplers and latent-space methods; the tiny course model only teaches the mechanics.

[Read the original paper](https://arxiv.org/abs/2006.11239). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 44

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 45

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 46

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 47

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 48

**NeRF (2020).** NeRF represents a scene with a continuous neural field and differentiable volume rendering for novel-view synthesis. Position and direction inputs predict density and appearance. Multiple calibrated views constrain the scene. Training/rendering cost and geometry ambiguity motivate accelerated fields and explicit representations such as Gaussian splatting.

[Read the original paper](https://arxiv.org/abs/2003.08934). The local lab is a teaching implementation with its own scope, not a claimed reproduction of published benchmark results.

## Chapter 49

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 50

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 51

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 52

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.

## Chapter 53

Design an ablation that changes one assumption in this chapter. State a hypothesis, freeze the evaluation protocol and compare against the simplest appropriate baseline. A measured negative result is useful if the experiment rules out a plausible explanation.
