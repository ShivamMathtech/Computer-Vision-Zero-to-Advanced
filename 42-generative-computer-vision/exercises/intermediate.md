# Level 2 — modify an algorithm

1. Interpolate between two latent codes, vary the VAE KL weight and inspect whether the GAN repeats a few outputs.
2. Compare the reference and library behavior on a tiny example. Identify conventions that must match before comparing numbers.
3. Create an example exposing this mistake: Low reconstruction MSE can favor blurry averages. Cherry-picked generated samples do not establish model quality.
4. Save the seed, input description, changed parameter and measured outcome in an experiment log.

**Acceptance:** a controlled comparison, a failure example and an explanation of the disagreement. Do not change several parameters at once.
