# Mathematical reference: symbols, intuition and small examples

Use this companion after the Chapter 02 introduction and return to each topic when its chapter uses it. Code fragments assume `import numpy as np`. A formula is useful only when its shapes, units and assumptions are known.

## Scalars, vectors and matrices

A scalar is a number, a vector an ordered collection and a matrix a rectangular collection. A color pixel is a three-entry vector; a grayscale image is a matrix. In $y=Ax$, A maps an input vector x to an output y. For A=[[1,2],[0,1]] and x=[3,4], y=[11,4]. In Python: `np.array([[1,2],[0,1]]) @ np.array([3,4])`. This is the same row/column dot-product structure used in linear layers and coordinate maps. Elementwise `*` answers a different question.

## Derivatives and partial derivatives

For $f(x)=x^2$, the derivative $f'(x)=2x$ is the local change per unit input. At x=3 it is 6. A central difference approximates it as `(f(x+h)-f(x-h))/(2*h)` with a small h; excessively small h magnifies floating-point cancellation. For $L(a,b)=a^2+3b^2$, the gradient is $[2a,6b]$. At (1,2), `np.array([2*1,6*2])` gives [2,12]. Each partial derivative holds the other parameter fixed. Networks use these sensitivities to update weights.

## Chain rule and gradient descent

If $y=g(f(x))$, then $dy/dx=g'(f(x))f'(x)$. For $y=(2x+1)^2$, at x=1 the derivative is `2*(2*1+1)*2 = 12`. Backpropagation accumulates such local derivatives in reverse order through a computation graph. Gradient descent updates $\theta' = \theta-\eta\nabla L$, where η is a step size. A weight 3, gradient 4 and step 0.1 gives 2.6. Optimizers change how the step is scaled; they do not remove the need for gradients and a meaningful objective.

## Probability, mean and covariance

A probability is a nonnegative weight on an outcome, with total one. The expectation $E[X]=\sum_x xp(x)$ is a weighted average. A fair die has expectation `np.arange(1,7).mean() = 3.5`; this value need not be an actual observed face. Variance $E[(X-\mu)^2]$ measures spread around μ. Covariance $E[(X-\mu_X)(Y-\mu_Y)]$ measures joint variation. `np.cov(points, rowvar=False)` estimates a covariance matrix from samples. State whether your variance divides by N or N−1. Covariance is central to PCA and Kalman uncertainty.

## Eigenvectors and PCA

$Av=\lambda v$ means A maps direction v back onto itself, scaled by λ. With A=diag(2,3), vector [1,0] has eigenvalue 2. `np.linalg.eigh(np.diag([2.,3.]))` returns real eigenpairs for a symmetric matrix. PCA centers samples, estimates covariance and projects onto leading eigenvectors. High variance is not automatically the feature most useful for a class label; PCA is unsupervised.

## Gaussian kernels and separability

A Gaussian weight is proportional to $\exp(-(x^2+y^2)/(2\sigma^2))$. Here x,y are offsets in pixels and σ controls width. At σ=1, offset (1,0) has unnormalized weight `np.exp(-.5)`. Normalize all sampled weights so they sum to one. The product of one-dimensional Gaussian weights equals the two-dimensional weight, permitting separable filtering. The reference samples finite support, so it is a discrete approximation rather than an infinite continuous Gaussian.

## Convolution and correlation

Correlation computes $Y_{ij}=\sum_{uv}K_{uv}X_{i+u,j+v}$. Convolution flips K before that sum. Kernel [1,0,−1] and input [1,2,4] give correlation −3 and convolution 3 for the one valid position. `np.dot([1,2,4],[1,0,-1])` and the reversed kernel demonstrate the difference. Symmetric blur kernels yield the same result either way, which often hides the convention. See `correlate` and `convolve` in the numeric references.

## Convolution size and receptive field

For input size n, kernel k, padding p and stride s, output size is $\lfloor(n+2p-k)/s\rfloor+1$ when dilation is one. For n=8,k=3,p=1,s=2, Python `(8+2-3)//2+1` gives 4. Receptive field expands as layers combine neighboring locations. Two stride-one 3×3 layers have a 5×5 receptive field, not 6×6, because their neighborhoods overlap. Dilation and stride change the recurrence and must be included explicitly for deeper models.

## Fourier transform

$X_k=\sum_{n=0}^{N-1}x_n e^{-2\pi i kn/N}$ converts N samples into frequency coefficients. k indexes frequency bins; i is the imaginary unit. For x=[1,1,1,1], `np.fft.fft(x)` gives [4,0,0,0]: only the constant component remains. Magnitude measures component strength, phase records alignment. Frequency is cycles per sampling interval, so converting bins into physical units requires the sampling rate. Images have horizontal and vertical frequency axes.

## Homogeneous coordinates, rotation and translation

Append one to [x,y] so a 3×3 matrix can include translation. A rotation $R(\theta)=[[\cos\theta,-\sin\theta],[\sin\theta,\cos\theta]]$ turns [1,0] into [0,1] at 90 degrees. `np.array([[0,-1],[1,0]]) @ [1,0]` demonstrates this. Translation by [3,−2] then gives [3,−1]. Camera and image coordinate directions must be declared: image y usually points downward. A perspective map additionally divides by the homogeneous coordinate.

## Epipolar geometry

For corresponding homogeneous pixels, $p_2^T Fp_1=0$. F is the fundamental matrix and $Fp_1$ describes an epipolar line in the second image. For rectified views, points share y. The illustrative matrix F=[[0,0,0],[0,0,−1],[0,1,0]] yields `p2 @ F @ p1 = 0` for p1=[2,3,1], p2=[1,3,1]. This constraint reduces correspondence search but does not choose the correct match among repeated patterns. With calibrated rays the essential matrix is $E=[t]_\times R$, linking relative rotation and translation up to scale.

## Perspective and stereo depth

$u=f_xX/Z+c_x$ projects camera-frame position to horizontal pixels. X,Z use the same world units; fx,cx use pixels. X=.2,Z=2,fx=400,cx=320 yields 360. For rectified stereo, $Z=fB/d$: f is focal pixels, B baseline length and d disparity pixels. `200*.12/8` gives 3 meters. Differentiating gives $|\partial Z/\partial d|=fB/d^2$, explaining why the same disparity error hurts distant-depth estimates more.

## Cross entropy and attention

Cross entropy for a true class is $L=-\log p_{true}$. If ptrue=.8, `-np.log(.8)` is about .223. Do not apply softmax twice when a framework loss expects logits. Attention computes a softmax of scaled query/key dot products, then a weighted sum of values. Chapter 38 gives shapes, a numerical example, masking and a NumPy implementation. Both formulas combine stable normalization with a clearly defined axis; the axis is part of the algorithm.
