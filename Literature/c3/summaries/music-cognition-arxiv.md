# music-cognition-arxiv

RA VE: A variational autoencoder for fast and
high-quality neural audio synthesis
Antoine Caillon & Philippe Esling
IRCAM - Sorbonne Universit´e
CNRS UMR 9912
1, place Igor Stravinsky, Paris, France
{caillon,esling}@ircam.fr
Abstract
Deep generative models applied to audio have improved by a large margin the
state-of-the-art in many speech and music related tasks. However, as raw wave-
form modelling remains an inherently difﬁcult task, audio generative models are
either computationally intensive, rely on low sampling rates, are complicated to
control or restrict the nature of possible signals. Among those models, Variational
AutoEncoders (V AE) give control over the generation by exposing latent vari-
ables, although they usually suffer from low synthesis quality. In this paper, we
introduce a Realtime Audio Variational autoEncoder (RA VE) allowing both fast
and high-quality audio waveform synthesis. We introduce a novel two-stage train-
ing procedure, namely representation learning and adversarial ﬁne-tuning. We
show that using a post-training analysis of the latent space allows a direct control
between the reconstruction ﬁdelity and the representation compactness. By lever-
aging a multi-band decomposition of the raw waveform, we show that our model
is the ﬁrst able to generate 48kHz audio signals, while simultaneously running
20 times faster than real-time on a standard laptop CPU. We evaluate synthesis
quality using both quantitative and qualitative subjective experiments and show
the superiority of our approach compared to existing models. Finally, we present
applications of our model for timbre transfer and signal compression. All of our
source code and audio examples are publicly available.
1 Introduction
Deep learning applied to audio signals proposes exciting new ways to perform speech generation,
musical composition and sound design. Recent works in deep audio modelling have allowed novel
types of interaction such as unconditional generation (Chung et al., 2015; Fraccaro et al., 2016; Oord
et al., 2016; Vasquez & Lewis, 2019; Dhariwal et al., 2020) or timbre transfer between instruments
(Mor et al., 2018). However, these approaches remain computationally intensive, as modeling audio
raw waveforms requires dealing with extremely large temporal dimensionality. To cope with this
issue, previous approaches usually rely on very low sampling rates (16 to 24kHz), which can be
sufﬁcient for speech signals, but is considered as low-quality for musical applications. Furthermore,
the auto-regressive sampling procedure used by most models (Engel et al., 2017) is prohibitively
long. This precludes real-time application which are pervasive in musical creation, while parallel
models (D´efossez et al., 2018) can only allow fast generation at the cost of a lower sound quality.
More recently, Engel et al. (2019) and Wang et al. (2019) proposed to leverage classical synthesis
techniques to address these limitations, by relying on pre-computed audio descriptors as an extra-
neous information to condition the models. While these approaches achieve state-of-the-art results
in terms of audio quality, naturalness and computational efﬁciency, the extensive use of audio de-
scriptors highly restricts the type of signals that can be generated. A possible solution to alleviate
arXiv:2111.05011v2  [cs.LG]  15 Dec 2021
this issue would be to rely on Variational Autoencoders (Kingma & Welling, 2014), as they provide
a form of trainable analysis-synthesis framework (Esling et al., 2018), without explicit restrictions
on the type of features learned. However, estimating the dimensionality of the latent representation
associated with a given dataset prior to model training is far from trivial. Indeed, a wrong esti-
mation of the latent dimensionality may result in either poor reconstruction or uninformative latent
dimensions, which makes latent exploration and manipulation difﬁcult.
In this paper, we overcome the limitations outlined above by proposing a V AE model built speciﬁ-
cally for fast and high-quality audio synthesis. To do so, we introduce a speciﬁc two-stage training
procedure where the model is ﬁrst trained as a regular V AE for representation learning, then ﬁne-
tuned with an adversarial generation objective in order to achieve high quality audio synthesis. We
combine a multi-band decomposition of the raw waveform alongside classical synthesis blocks in-
spired by Engel et al. (2019), allowing to achieve high-quality audio synthesis with sampling rates
going up to 48kHz without a major increase in computational complexity. We show that our model
is able to converge on complex datasets using a low number of parameters, achieving state-of-the-
art results in terms of naturalness and audio quality, while being usable in real-time on a standard
laptop CPU. We compare our model with several state-of-the-art models and show its superiority in
unsupervised audio modeling. In order to address the dimensionality of the learned representation,
we introduce a novel method to split the latent space between informative and uninformative parts
using a singular value decomposition, and show that replacing the latter part with random noise does
not affect the reconstruction quality. This procedure allows easier exploration and manipulation of
latent trajectories, since we only need to operate on a subset of informative latent dimensions. Fi-
nally, we discuss the application of our model in signal compression and timbre style transfer. Our
key contributions are:
• A two-stage training procedure where the model is ﬁrst trained as a regular V AE, then
ﬁne-tuned with an adversarial generation objective, as depicted in ﬁgure 1
• A post-training analysis of the latent space providing a way to balance between reconstruc-
tion ﬁdelity and representation compactness
• High-quality audio synthesis models with sampling rates going up to 48kHz
• 20 times faster than realtime synthesis on a standard laptop CPU
Audio samples and supplementary ﬁgures are provided in the accompanying website 1. We highly
encourage readers to listen to accompanying samples while reading the paper.
Stage 1:
Representation Learning
Stage 2:
Adversarial fine-tuning
multiband encoder z decoder multiband
multiband encoder z decoder multiband
multiband spectral 
distance
discriminator
x
sg
x^
Figure 1: Overall architecture of the proposed approach. Blocks in blue are the only ones optimized,
while blocks in grey are ﬁxed or frozen operations.
2 State-of-art
2.1 Variational autoencoders
Generative models aim to understand a given dataset x∈ Rdx by modelling its underlying dis-
tributionp(x). To simplify this problem, we can consider that the generation of x is conditioned
by latent variables z∈ Rdz, responsible for most of the variations present in x. Therefore, the
1https://anonymous84654.github.io/ICLR_anonymous/
2
complete model is deﬁned by the joint distributionp(x, z) = p(x|z)p(z), which is usually not an-
alytically solvable given the complexity of real-world data. Variational autoencoders address this
problem by introducing an inference model qφ(z|x), optimized to minimize its Kullback-Leibler
(KL) divergence with the true posterior distributionp(z|x)
φ∗ = argmin
φ
DKL[qφ(z|x)∥p(z|x)], (1)
which can be rearranged to obtain the ﬁnal objective used to train a V AE, called the Evidence Lower
BOund (ELBO), as shown by Kingma & Welling (2014)
Lφ,θ(x) =−Eqφ(z|x)[logpθ(x|z)] +DKL[qφ(z|x)∥p(z)]. (2)
The ELBO minimizes the reconstruction error of the model through the likelihood of the data given
a latent logpθ(x|z), while regularizing the posterior distribution qφ(z|x) to match a predeﬁned
priorp(z). Both posterior distributions qφ andpθ are parametrized by neural networks respectively
called encoder and decoder. Higgins et al. (2016) proposes to weight the KL divergence in equation
(2) with a parameter β to control the trade-off between accurate reconstruction and strong latent
regularization. They show that increasing β > 1 leads to less entangled latent dimensions, at the
detriment of the reconstruction quality.
2.2 Autoencoding raw waveform
One of the ﬁrst approaches addressing the raw waveform modelling task are WaveNet (Oord et al.,
2016) and SampleRNN (Mehri et al., 2017), where the probability of a waveform x is factorized as
a product of conditional probabilities
p(x) =
∏
t>1
p(xt|x1,...,x t−1). (3)
Those models require a large amount of data and parameters to properly converge. Furthermore, the
autoregressive nature of the synthesis process makes it prohibitively slow, and prone to accumulate
errors.
WaveNet has also been adapted by Engel et al. (2017) for their NSynth model, addressing the rep-
resentation learning task. Unlike equation (2), they do not regularize the learned representation, and
rather encode the raw waveform determinisitically to its latent counterpart. It implies the absence of
a prior distribution p(z) and, therefore, prevents sampling from the latent space. This restricts the
applications of the model to simple reconstructions and interpolations.
As a way to speed-up the synthesis process, D ´efossez et al. (2018) proposed an autoencoder with
feed-forward convolutional networks parametrizing both the encoder and the decoder. They use a
perceptually-motivated distance between waveforms called spectral distance as the reconstruction
objective
l(x, y) =
log(STFT(x)2 +ϵ)− log(STFT(y)2 +ϵ)

1, (4)
where STFT is the Short-Term Fourier Transform. Since they use a squared STFT, the phase com-
ponent is discarded making the loss permissive to inaudible phase variations. They show that their
model is 2500 times faster that NSynth during synthesis, at the expense of a degraded sound quality.
Following the recent advances in generative adversarial modelling (Goodfellow et al., 2014), Kumar
et al. (2019) proposed to use an adversarial objective to address the parallel audio modelling task.
The discriminator is trained to differentiate true samples from generated ones, while the generator
is optimized to produce samples that are classiﬁed as true by the discriminator. A feature matching
loss is added to the adversarial loss, minimizing the L1 distance between the discriminator feature
maps of real and synthesized audio. This feature matching mechanism can be seen as a learned
metric to evaluate the distance between two samples, and has been successfully applied to the con-
ditional waveform modelling task (e.g spectrogram to waveform or replacement of the decoder in a
pretrained autoencoder model).
3
3 Method
3.1 Two-stage training procedure
Ideally, the representation learned by a variational autoencoder should contain high-level attributes
of the dataset. However, two perceptually similar audio signals may contain subtle phase variations
that produce dramatically different waveforms. Hence, estimating the reconstruction term in equa-
tion (2) using the raw waveform penalizes the model if those subtle variations are not included in
the learned representation. This might both hamper the learning process and include in the latent
space those low-level variations about audio signal that are not relevant perceptually. To address this
problem, we split the training process in two stages, namelyrepresentation learningand adversarial
ﬁne-tuning.
3.1.1 Stage 1: Representation learning
The ﬁrst stage of our procedure aims to performrepresentation learning. We leverage the multiscale
spectral distance S(·,·) proposed by Engel et al. (2019) in order to estimate the distance between
real and synthesized waveforms, deﬁned as
S(x, y) =
∑
n∈N
[∥STFTn(x)− STFTn(y)∥F
∥STFTn(x)∥F
+ log (∥STFTn(x)− STFTn(y)∥1)
]
, (5)
whereN is a set of scales, STFT n is the amplitude of the Short-Term Fourier Transform with
window size n and hop size n/4, and∥·∥ F ,∥·∥ 1 are respectively the Frobenius norm and L1
norm. Using an amplitude spectrum-based distance does not penalize the model for inaccurately
reconstructed phase, but encompasses important perceptual features about the signal. We train the
encoder and decoder with the following loss derived from the ELBO
Lvae(x) = Eˆ x∼p(x|z)[S(x, ˆ x)] +β×D KL[qφ(z|x)∥p(z)], (6)
We start by training the model solely withLvae, and once this loss converges, we switch to the next
training phase.
3.1.2 Stage 2: Adversarial ﬁne-tuning
The second training stage aims at improving the synthesized audio quality and naturalness. As we
consider that the learned representation has reached a satisfactory state at this point, we freeze the
encoder and only train the decoder using an adversarial objective.
GANs are implicit generative models allowing to sample from a complex distribution by transform-
ing a simpler one, called thebase distribution. Here, we use the learned latent space in the ﬁrst stage
as the base distribution, and train the decoder to produce synthesized signals similar to the real ones
by relying on a discriminatorD. We use the hinge loss version of the GAN objective, deﬁned as
Ldis(x, z) = max(0, 1−D(x)) + Eˆ x∼p(x|z)[max(0, 1 +D(ˆ x))],
Lgen(z) =−Eˆ x∼p(x|z)[D(ˆ x)]. (7)
In order to ensure that the synthesized signal ˆ xdoes not diverge too much from the ground truth x,
we keep minimizing the spectral distance deﬁned in equation (5), but also add the feature matching
lossLFM proposed by Kumar et al. (2019). Altogether, this yields the following objective for the
decoder
Ltotal(x, z) =Lgen(z) + Eˆ x∼p(x|z)[S(x, ˆ x) +LFM(x, ˆ x)]. (8)
3.2 Latent representation compactness
The loss proposed in equation (6) contains two terms, a reconstruction and regularisation term.
Those two terms are somewhat conﬂicting, since the reconstruction term maximises the mutual
4
information between the latent representation and the data distribution, while the regularisation term
guides the posterior distribution towards independence with the data (potentially causing posterior
collapse). In practice, the pressure applied by the regularisation term to the encoder during training
encourages it to learn a compact representation, where informative latents have the highest KL
divergence from the prior, while uninformative latents have a KL divergence close to 0 (Higgins
et al., 2016).
Here, we address the task of identifying the most informative parts of the latent space in order to
restrict the dimensionality of the learned representation to the strict minimum required to reconstruct
a signal. To do so, we adapt the method for range and null space estimation (see appendix A) to this
problem. Let Z∈ Rb×d be a matrix composed of b samples z∈ Rd, where z∼ qφ(z|x). Using
a Singular Value Decomposition (SVD) directly on Z to solve the problem of ﬁnding informative
parts of the latent space would not be relevant given the high variance present in the collapsed parts
of Z. In order to adapt this to our problem, we ﬁrst remove the variance fromZ, by considering the
matrix Z′∈ Rb×d that veriﬁes
Z′
i = argmax
z
qφ(z|x), (9)
Hence, dimensions of the posterior distribution qφ(z|x) that have collapsed to the prior p(z) will
result in a constant value in Z′, that we set to 0 by removing the average of Z′ across the ﬁrst
dimension. The only dimensions of Z′ with non-zero values are therefore correlated with the input,
which constitute the informative part of the latent space. Applying a SVD on this centered matrix,
we can obtain the matrix Σ containing the singular values of Z′, by computing
Z′ = UΣVT, (10)
As detailed in appendix A, the rank r of Z′ is equal to the number of non-zero singular values in
Σ. Given the high variation that exists in real-world data, it is unlikely that the vanishing singular
values of Z′ are equal to 0. Therefore, instead of tracking the exact rankr of Z′, we deﬁne aﬁdelity
parameterf∈ [0− 1], with the associated rankrf deﬁned as the smallest integer verifying
∑
i≤rf
Σii
∑
i Σii
≥f. (11)
Given the ﬁdelity valuef, and a latent representation z∼ qφ(z|x), we reduce the dimensionality
of z by projecting it on the basis deﬁned by VT and keep only the rf ﬁrst dimensions. We obtain
a low-rank representation zf , whose dimensionality depends on both the dataset and f. Before
providing zf to the decoder, we concatenate it with noise sampled from the prior distribution, and
project it back on its original basis usingV. We demonstrate in section 5.3 the inﬂuence of f on the
reconstruction.
4 Experiments
4.1 RA VE
Here, we introduce our Realtime Audio Variational autoEncoder (RA VE) built for high-quality audio
representation learning and faster than realtime synthesis. Since we target the modelling of 48kHz
audio signals, we leverage a multiband decomposition of the raw waveform (see appendix B) as a
way to decrease the temporal dimensionality of the data (Yang et al., 2020). This allows us to expand
the temporal receptive ﬁeld of our model without a major increase in computational complexity. We
demonstrate the inﬂuence of the multiband decomposition on the synthesis speed in section 5.2.
Using a 16-band decomposition, we successfully model 48kHz audio signals while producing a
compact latent representation using the post-training analysis presented in section 3.2.
Encoder. We deﬁne our encoder as the combination of a multiband decomposition followed by a
simple convolutional neural network, transforming the raw waveform into a 128-dimensional latent
representation. A detailed description of the architecture of the encoder is given in annex C.1.
5
Decoder. Our decoder is a modiﬁed version of the generator proposed by Kumar et al. (2019).
We use the same alternation of upsampling layers and residual networks, but instead of directly
outputting the raw waveform we feed the last hidden layer to three sub-networks. The ﬁrst sub-
network (waveform) synthesizes a multiband audio signal (withtanh activation), which is multiplied
by the output of the second sub-network (loudness), generating an amplitude envelope (withsigmoid
activation). The last sub-network is a noise synthesizer as proposed in Engel et al. (2019), and
produces a multiband ﬁltered noise added to the previous signal.
We found that using an explicit amplitude envelope helps reducing artifacts in the silent parts of the
signal, while the noise synthesizer slightly increases the reconstruction naturalness of noisy signals.
See annex C.2 for more details about the architecture of the decoder.
Discriminator. We use the exact same discriminator as in Kumar et al. (2019), which is a strided
convolutional network applied on different scales of the audio signal to prevent artifacts. We also
use the same feature matching loss as in the original paper.
Training. We follow the training procedure proposed in 3.1, and train RA VE for 3M steps, specif-
ically 1.5M steps for each stage, summing to a total of approximately 6 days on a single TITAN V
GPU. We use theAdam optimizer (Kingma & Ba, 2015) with a learning rate of10−4,β = (0.5, 0.9),
and batch size 8. We use dequantization, random crop and allpass ﬁlters with random coefﬁcients
as our data augmentation strategy.
Baselines. We evaluate our model in the context of unsupervised representation learning. We
compare it against two state-of-the-art models: an unsupervised NSynth (Engel et al., 2017) and
the autoencoder from SING (D ´efossez et al., 2018). We use the ofﬁcial implementations for both
baselines with default parameters. We do not to evaluate the DDSP (Engel et al., 2019) and NSF
(Wang et al., 2019) approaches since we target the unsupervised modelling of any type of audio
signals. Notably, our proposal is able to model both monophonic and polyphonic signals, while the
aforementioned methods are restricted to monophonic signals.
4.2 Datasets
Strings. Since our main target is the modelling of musical audio signals, we use an internal dataset
composed of approximately 30 hours of raw recordings of strings in various conﬁgurations (mono-
phonic solos and polyphonic group performances, with different styles and recording conﬁgurations)
sampled at 48kHz. We employ a 90/10 train/test split. We downsample this dataset to 16kHz when
using NSynth and SING.
VCTK. The V oice Conversion ToolKit (Yamagishi et al., 2019) is a speech dataset composed of
approximately 44 hours of raw audio sampled at 48kHz, produced by 110 different speakers with
various accents. We use it to evaluate the performances of RA VE when addressing the speech
modelling task in an unsupervised fashion. We also employ a 90/10 train/test split and downsample
to 16 kHz for other methods.
5 Results
To encourage reproducibility, we release the source code of our model alongside pretrained weights
used to produce the presented results. Audio samples corresponding to the different parts of this
section are available on our accompanying website.
5.1 Synthesis quality
First, we performed a qualitative experiment where participants were asked to rate audio samples on
a scale of 1 to 5. The test consisted of 15 trials, with each presenting an audio sample of the strings
dataset never seen during training, alongside its reconstruction by the three models. The order in
which the trials and samples are presented was randomized. A total of 33 participants took the test,
with most being audio professionals. We report the results of this study in table 1.
6
Table 1: Reconstruction quality evaluation (Mean Opinion Score)
Model MOS 95% CI Training time Parameter count
Ground truth 4.21 ±0.04 - -
NSynth 2.68 ±0.04 ∼ 13 days 64.7M
SING 1.15 ±0.02 ∼ 5 days 80.8M
RA VE (Ours) 3.01 ±0.05 ∼ 7 days 17.6M
As we can see, RA VE outperforms both NSynth and SING in terms of audio quality without relying
on autoregressive generation. Furthermore, it achieves high-quality audio synthesis with at least 3.5
times less parameters. There is still a gap in the evaluation between the ground truth and the other
models. This might come from the difﬁculty of modeling the variety of room acoustics conditions
present in the original dataset (as discussed in Engel et al. (2019)), sometimes making it obvious
that the evaluated samples are synthesized.
5.2 Synthesis speed
Several approaches using normalizing ﬂows (Prenger et al., 2019) or adversarial models (Kumar
et al., 2019) can achieve faster than realtime synthesis, but only by relying on GPUs. Other ap-
proaches make strong assumptions about the signal in order to simplify the generation process (En-
gel et al., 2019; Wang et al., 2019), allowing real-time synthesis on CPU, while restricting the range
of audio signals that can be modeled. In table 2, we evaluate the synthesis speed of all models
on both CPU and GPU. The synthesis speed is calculated as the average number of audio samples
generated per second for 100 trials.
Table 2: Comparison of the synthesis speed for several models
Model CPU synthesis GPU synthesis
NSynth 18 Hz 57 Hz
SING 304 kHz 9.8 MHz
RA VE (Ours) w/o multiband 38 kHz 3.7 MHz
RA VE (Ours) 985 kHz 11.7 MHz
Being the only model relying on autoregressive synthesis, NSynth is also the slowest, peaking at
57Hz during generation. As expected, the parallel nature of SING and RA VE makes them several
orders of magnitude faster than NSynth. The addition of the multiband decomposition speeds up
RA VE by a factor of 25, allowing our model to outperform SING on both CPU and GPU. Overall,
we obtain audio synthesis at 48kHz with a 20× faster than realtime factor on CPU, and up to 240×
on GPU.
5.3 Balancing compactness and ﬁdelity
Having a compact learned representation has several beneﬁts, since it is easier to analyse, manipulate
and understand. However, it usually comes at the expense of trading off the reconstruction quality.
Instead of determining the latent space dimensionality prior to the training, we rely on the ﬁdelity
parameterf to estimate it post-training and accordingly crop the learned representation, as explained
in section 3.2.
In ﬁgure 2, we compute the relationship betweenf and the estimated number of dimensions rf for
both the strings and vctk datasets. We depict the inﬂuence of f on the reconstruction quality by
measuring the spectral distance (see equation 5) between the original and reconstructed samples.
By setting f = 0.99, the dimensionality of the learned representation drops from 128 to just 24
on the strings dataset and 16 on the vctk dataset. The downsampling factor of the encoder is 2048,
resulting in a latent representation sampled at ∼ 23Hz. Further decreasing f results in a higher
spectral distance as shown in ﬁgure 2 (right), but signiﬁcantly reduces the learned representation
7
0.0 0.2 0.4 0.6 0.8 1.0
fidelity
100
101
dimension number
strings
vctk
0.0 0.2 0.4 0.6 0.8 1.0
fidelity
0.7
0.8
0.9
1.0
1.1spectral distance
strings
vctk
Figure 2: Estimated latent space dimensionality according to the ﬁdelity parameter and its corre-
sponding inﬂuence on the reconstruction quality.
size. To exemplify this, we reconstruct a sample from thevctk dataset using different ﬁdelity values,
and display the resulting melspectrograms in ﬁgure 3.
(a) Original sample
 (b) f = 0.99
 (c) f = 0.90
 (d) f = 0.80
Figure 3: Reconstruction of an input sample with several ﬁdelity parametersf.
As the ﬁdelity parameter decreases, reconstructed samples get less accurate, loosing parts of their
attributes such as phonemes or speaker identity.
5.4 Timbre transfer
We demonstrate that RA VE can be used to perform domain transfer even if it has not been specif-
ically trained to address this particular task. We perform domain transfer by simply providing to a
pretrained RA VE model audio samples coming from outside of its original training distribution (e.g
violin samples are reconstructed with a model trained on speech, see section F for more details).
5.5 Signal compression
Since the representation learned by RA VE is signiﬁcantly more compact than the raw audio wave-
form, it can be used as a data-driven compression system for transmission and storage purposes,
or to produce the base signal for a higher-level model to work on. Applying our model provides
a compression ratio of 2048, producing latent signals sampled at ∼ 23Hz, which can be used as a
simpler representation for further learning tasks.
To illustrate this, we train a WaveNet-inspired model at generating latent signals in an autoregressive
fashion for performing audio synthesis with RA VE. Combining this autoregressive model with the
decoder from RA VE, we still obtain synthesis at a 5 times faster than realtime factor. Furthermore,
since latent signals are sampled at a much slower rate than the raw waveform, we obtain a 3-second-
long receptive ﬁeld with as few as 9M parameters, corresponding to only 10 layers of the original
WaveNet architecture. Examples of unconditional generation are available on our accompanying
website.
8
6 Related work
The combination of V AE and GAN has already been studied as a way to build a representation
learning model with high quality generation abilities. Larsen et al. (2015) propose to replace the
reconstruction loss with a learned metric similar to the feature matching loss we use in equation 8.
This learned metric can be seen as a perceptual loss (Kumar et al., 2019), but we demonstrate in
annex E that using it to train our encoder results in a larger estimated latent space dimensionality,
making the learned representation harder to analyse and interact with.
Previous approaches combine perceptual losses and auxiliary losses to achieve high quality audio
synthesis. Yamamoto et al. (2020) leverage a multiscale spectral loss together with an adversarial
objective to address the mel-scale spectrogram inversion task, while Ping et al. (2018) use a spectral
loss as a guide to stabilize their distillation procedure. Contrary to our two-stage procedure, they
mainly use this combination as a warmup mechanism to help their model converge, whereas we
use both losses with two separate tasks in mind: representation learning encompassing spectral
attributes of the signal, and high-quality audio synthesis based on an adversarial objective, using a
ﬁxed learned latent space.
The use of a multiband decomposition of the raw waveform has been successfully applied by Yu
et al. (2019) and Yang et al. (2020) to the audio modelling task, and they both show that it helps
producing higher quality results while reducing the training and synthesis time. Modelling 48kHz
audio is challenging in term of temporal complexity and memory requirements, and building up from
the aforementioned work we show that using a 16 band decomposition allows RA VE to address this
task.
7 Conclusion
In this paper, we introduced RA VE: a Realtime Audio Variational autoEncoder for fast and high-
quality neural audio synthesis. First, we proposed a two-stage training procedure, which ensures
that the latent representation is adequate, prior to performing adversarial ﬁne-tuning for generating
high-quality audio signals. We showed that our method outperforms the performances of previous
approaches in both quantitative and qualitative analyses. By leveraging a multiband decomposition
of the raw waveform, we are able to achieve 20 times faster than realtime synthesis on a standard
laptop CPU. Finally, we proposed a method to control the trade-off between reconstruction quality
and representation compactness, easing the analysis and control of the learned representation. We
provide the open-source code of RA VE and hope that this will spark contributions and creative uses
of our model.
9
References
Junyoung Chung, Kyle Kastner, Laurent Dinh, Kratarth Goel, Aaron Courville, and Yoshua Ben-
gio. A Recurrent Latent Variable Model for Sequential Data. Advances in Neural Informa-
tion Processing Systems , 2015-January:2980–2988, 6 2015. ISSN 10495258. URL https:
//arxiv.org/abs/1506.02216v6.
Alexandre D ´efossez, Neil Zeghidour, Nicolas Usunier, L ´eon Bottou, and Francis Bach. SING:
Symbol-to-Instrument Neural Generator. Advances in Neural Information Processing Systems ,
2018-December:9041–9051, 10 2018. URL https://arxiv.org/abs/1810.09785v1.
Prafulla Dhariwal, Heewoo Jun, Christine Payne, Jong Wook Kim, Alec Radford, and Ilya Sutskever.
Jukebox: A Generative Model for Music. arXiv, 4 2020. URL http://arxiv.org/abs/2005.
00341.
Jesse Engel, Cinjon Resnick, Adam Roberts, Sander Dieleman, Mohammad Norouzi, Douglas Eck,
and Karen Simonyan. Neural Audio Synthesis of Musical Notes with WaveNet Autoencoders, 7
2017. ISSN 2640-3498. URL https://proceedings.mlr.press/v70/engel17a.html.
Jesse Engel, Lamtharn Hantrakul, Chenjie Gu, and Adam Roberts. DDSP: Differentiable
Digital Signal Processing. Technical report, 9 2019. URL https://goo.gl/magenta/
ddsp-examples.
Philippe Esling, Axel Chemla-Romeu-Santos, and Adrien Bitton. Generative timbre spaces: reg-
ularizing variational auto-encoders with perceptual metrics. DAFx 2018 - Proceedings: 21st
International Conference on Digital Audio Effects, pp. 369–376, 5 2018. URL http://arxiv.
org/abs/1805.08501.
Marco Fraccaro, Søren Kaae Sønderby, Ulrich Paquet, and Ole Winther. Sequential Neural Models
with Stochastic Layers. Advances in Neural Information Processing Systems , pp. 2207–2215, 5
2016. ISSN 10495258. URL https://arxiv.org/abs/1605.07571v2.
Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair,
Aaron Courville, and Yoshua Bengio. Generative Adversarial Networks. Communications of the
ACM, 63(11):139–144, 6 2014. URL https://arxiv.org/abs/1406.2661v1.
Irina Higgins, Loic Matthey, Arka Pal, Christopher Burgess, Xavier Glorot, Matthew Botvinick,
Shakir Mohamed, and Alexander Lerchner. beta-V AE: Learning Basic Visual Concepts with a
Constrained Variational Framework, 11 2016.
Diederik P. Kingma and Jimmy Lei Ba. Adam: A method for stochastic optimization. In 3rd Inter-
national Conference on Learning Representations, ICLR 2015 - Conference Track Proceedings .
International Conference on Learning Representations, ICLR, 2015.
Diederik P. Kingma and Max Welling. Auto-encoding variational bayes. In 2nd International Con-
ference on Learning Representations, ICLR 2014 - Conference Track Proceedings. International
Conference on Learning Representations, ICLR, 12 2014. URL https://arxiv.org/abs/
1312.6114v10.
Kundan Kumar, Rithesh Kumar, Thibault de Boissiere, Lucas Gestin, Wei Zhen Teoh, Jose Sotelo,
Alexandre de Brebisson, Yoshua Bengio, and Aaron Courville. MelGAN: Generative Adversarial
Networks for Conditional Waveform Synthesis.arXiv, 10 2019. URL http://arxiv.org/abs/
1910.06711.
Guillaume Lample, Neil Zeghidour, Nicolas Usunier, Antoine Bordes, Ludovic Denoyer, and
Marc’aurelio Ranzato. Fader Networks: Manipulating Images by Sliding Attributes. Advances in
Neural Information Processing Systems, 2017-December:5968–5977, 6 2017. ISSN 10495258.
URL https://arxiv.org/abs/1706.00409v2.
Anders Boesen Lindbo Larsen, Søren Kaae Sønderby, Hugo Larochelle, and Ole Winther. Autoen-
coding beyond pixels using a learned similarity metric. 33rd International Conference on Ma-
chine Learning, ICML 2016 , 4:2341–2349, 12 2015. URL https://arxiv.org/abs/1512.
09300v2.
10
Yuan Pei Lin and P. P. Vaidyanathan. A kaiser window approach for the design of prototype ﬁlters
of cosine modulated ﬁlterbanks. IEEE Signal Processing Letters , 5(6):132–134, 1998. ISSN
10709908. doi: 10.1109/97.681427.
M. Rossi, Jin-Yun Zhang, and W. Steenaart. A new algorithm for designing prototype ﬁlters for M-
band Pseudo QMF banks, 1996. URL https://ieeexplore.ieee.org/document/7083013.
Soroush Mehri, Kundan Kumar, Ishaan Gulrajani, Rithesh Kumar, Shubham Jain, Jose Sotelo,
Aaron Courville, and Yoshua Bengio. Samplernn: An unconditional end-to-end neural audio
generation model. In 5th International Conference on Learning Representations, ICLR 2017
- Conference Track Proceedings. International Conference on Learning Representations, ICLR,
2017.
Noam Mor, Lior Wolf, Adam Polyak, and Yaniv Taigman. A Universal Music Translation Network.
arXiv, 5 2018. URL http://arxiv.org/abs/1805.07848.
Truong Q. Nguyen. Near-Perfect-Reconstruction Pseudo-QMF Banks.IEEE Transactions on Signal
Processing, 42(1):65–76, 1994. ISSN 19410476. doi: 10.1109/78.258122.
Aaron van den Oord, Sander Dieleman, Heiga Zen, Karen Simonyan, Oriol Vinyals, Alex Graves,
Nal Kalchbrenner, Andrew Senior, and Koray Kavukcuoglu. WaveNet: A Generative Model for
Raw Audio. 9 2016. URL http://arxiv.org/abs/1609.03499.
Wei Ping, Kainan Peng, and Jitong Chen. ClariNet: Parallel Wave Generation in End-to-End Text-
to-Speech. Technical report, 9 2018. URL https://clarinet-demo.github.io/.
Ryan Prenger, Rafael Valle, and Bryan Catanzaro. Waveglow: A Flow-based Generative Network
for Speech Synthesis. InICASSP , IEEE International Conference on Acoustics, Speech and Signal
Processing - Proceedings, volume 2019-May, pp. 3617–3621. Institute of Electrical and Electron-
ics Engineers Inc., 5 2019. ISBN 9781479981311. doi: 10.1109/ICASSP.2019.8683143.
Sean Vasquez and Mike Lewis. MelNet: A Generative Model for Audio in the Frequency Domain.
arXiv, 6 2019. URL http://arxiv.org/abs/1906.01083.
Xin Wang, Shinji Takaki, and Junichi Yamagishi. Neural source-ﬁlter waveform models for sta-
tistical parametric speech synthesis. IEEE/ACM Transactions on Audio Speech and Language
Processing, 28:402–415, 4 2019. URL https://arxiv.org/abs/1904.12088v2.
Junichi Yamagishi, Christophe Veaux, and Kirsten MacDonald. CSTR VCTK Corpus: English
Multi-speaker Corpus for CSTR V oice Cloning Toolkit, 2019.
Ryuichi Yamamoto, Eunwoo Song, and Jae Min Kim. Parallel Wavegan: A Fast Waveform Gener-
ation Model Based on Generative Adversarial Networks with Multi-Resolution Spectrogram. In
ICASSP , IEEE International Conference on Acoustics, Speech and Signal Processing - Proceed-
ings, volume 2020-May, pp. 6199–6203. Institute of Electrical and Electronics Engineers Inc., 5
2020. ISBN 9781509066315. doi: 10.1109/ICASSP40776.2020.9053795.
Geng Yang, Shan Yang, Kai Liu, Peng Fang, Wei Chen, and Lei Xie. Multi-band MelGAN: Faster
Waveform Generation for High-Quality Text-to-Speech. arXiv, 5 2020. URL http://arxiv.
org/abs/2005.05106.
Chengzhu Yu, Heng Lu, Na Hu, Meng Yu, Chao Weng, Kun Xu, Peng Liu, Deyi Tuo, Shiyin
Kang, Guangzhi Lei, Dan Su, and Dong Yu. DurIAN: Duration Informed Attention Network For
Multimodal Synthesis. 9 2019. URL http://arxiv.org/abs/1909.01700.
11
A Range and null space estimation
Let Z be ab×d real-valued matrix with∑
iZij = 0. We consider the singular value decomposition
of Z
Z = UΣVT (12)
where U and V are orthogonal real-valued matrices of respective dimensionsb×b andd×d, and
Σ is a rectangular diagonal matrix with non-negative values on the diagonal called singular values,
sorted by decreasing value. The number of non-zero singular values gives the rankr of the matrix,
i.e the dimension of the vector space spanned by its columns.
The range and null space associated with Z are respectively spanned by the ﬁrst r and last d−r
columns of VT. A low rank version of Z can be obtained by keeping only ther ﬁrst columns ofΣ
and V, such that
Z = U˜Σ˜VT, (13)
where ˜Σ and ˜VT are respectively of dimensionb×r andr×d. Note that the equality in equation
(13) only holds if the lastd−r singular values are equal to 0. Rearranging equation (13), we get the
formula to perform a Principal Component Analysis (PCA) on Z withr components
˜Z = Z˜V = U˜Σ. (14)
Since V is orthogonal, we can get Z back by multiplying equation (14) by VT.
B Multiband decomposition
The main use of a multiband decomposition is to represent an audio signal sampled at a given sam-
pling rate (e.g 48kHz) as a combination of several downsampled sub-signals (e.g 3kHz), where each
sub-signal covers a particular range of frequencies. This decomposition is useful for compression
purposes such as mp3 encoding/decoding, since it allows the use of different bit rates on speciﬁc
areas of the spectrum.
Multiband decompositions of the raw waveform have already been repeatedly applied in the context
of audio generative modelling. (Yu et al., 2019) speciﬁcally use Pseudo Quadrature Mirror ﬁlters
(PQMF), deﬁned by Nguyen (1994). PQMF are M−band ﬁlter-banks that split a signal into M
sub-signals decimated by a factorM. TheM ﬁlters are cosine modulations of a prototype low-pass
ﬁlter with cutoff frequency
fc = sr
2M, (15)
carefully designed to avoid aliasing in the reconstructed signal. In practice, it is impossible to create
a perfect prototype ﬁlter (i.e perfectly rejected band), but we can instead design a ﬁlter that allows the
cancellation of aliasing between neighbouring sub-bands, using methods such as the optimisation
of a non-linear objective function as described by M. Rossi et al. (1996), or using a simple Kaiser
window whose parameters are optimised in an analysis-synthesis pipeline, as proposed by Lin &
Vaidyanathan (1998).
Since the ﬁlter-bank is an orthogonal basis of the signal due to the cosine modulations implied during
its creation, the re-synthesis process can be performed by reapplying a temporally ﬂipped version of
the ﬁlter-bank to the sub-bands.
12
C Model architecture
C.1 Encoder
The encoder of RA VE is a convolutional neural network with leaky ReLU activation and batch
normalization (see ﬁgure 4). For all of our experiments we useN = 4, with hidden sizes [64, 128,
256, 512] and strides [4, 4, 4, 2]. The full latent space has 128 dimensions.
Conv1d BatchNorm1dLeaky
ReLU
x N
audio in multiband
decomposition
Conv1d
Conv1d softplus
mean
variance
Figure 4: Architecture of the encoder used in the RA VE model.
C.2 Decoder
We detail the different blocks composing the decoder.
waveform
conv
loudness
conv
noise
synthesizer
upsampling
layer
residual
stack
latent
representation
x N
x + audio out
Figure 5: Overview of the proposed decoder. The latent representation is upsampled using alternat-
ing upsampling layers and residual stack. The result is processed by three sub-networks, respectively
producing waveform, loudness envelope and ﬁlterednoise signals.
Conv 
Transpose1d
leaky
ReLU
(a) Upsampling layer
Conv1dleaky
ReLU +
x 3
x N (b) Residual stack
Conv1d leaky
ReLU
x N
filter
white noise
filtered noise out
(c) Noise synthesizer
Figure 6: Detailed architecture of the decoder blocks used in the RA VE model.
13
D Latent component collapse
The regularisation term in equation 6 applies a pressure on the encoder to produce a posterior distri-
bution that is close to the prior, and therefore not correlated with the input data. Since this objective
is contrary to the reconstruction objective, it has been empirically shown by Higgins et al. (2016)
that some latents are more informative than others, as it can be seen in ﬁgure 7 in the case of RA VE.
0 25 50 75 100 125
latent component number
10 −2
10 −1
10 0
divergence from prior
(a) Strings dataset
0 25 50 75 100 125
latent component number
10 −3
10 −2
10 −1
10 0
divergence from prior (b) VCTK dataset
Figure 7: Mean Kullback Leibler divergence for each latent component between the posterior distri-
butionqφ(z|x) estimated over the test set of the strings and VCTK datasets and the prior distribution.
For both datasets, most of the latents have a low KL divergence (lower than 0.01), and only a few
(respectively 16 and 9 for the strings and VCTK datasets) have a KL divergence higher than 0.1,
which is consistent with the dimensionality estimated by the method proposed in section 3.2 for a
ﬁdelity parameterf = 0.95.
E Two stage training and latent space compactness
Compared to previous approaches combining V AE and GANs, there are no adversarial losses in-
volved when training the encoder. We demonstrate in ﬁgure 8 how training the encoder to minimize
the feature matching loss as proposed by Larsen et al. (2015) during the second stage results in a
dramatically increased estimated latent space dimensionality, which goes against our objective of
building a compact representation.
0.0 0.5 1.0 1.5 2.0
Iteration number 1e6
0
20
40
60Latent dimensionality
f=0.80
f=0.90
f=0.95
f=0.99
(a) Frozen encoder
0.0 0.5 1.0 1.5 2.0
Iteration number 1e6
0
20
40
60Latent dimensionality
f=0.80
f=0.90
f=0.95
f=0.99 (b) Trained encoder
Figure 8: Comparison of the estimated latent space dimensionality for two trainings of RA VE on
the Strings dataset with and without freezing the encoder during the adversarial ﬁne tuning stage
(starting at 1.106 iterations).
14
F Out of domain latent representation
We demonstrate in ﬁgure 9 that RA VE can be used to address the timbre transfer task (see section
5.4).
(a) Transfer from strings to vctk
 (b) Transfer from vctk to strings
Figure 9: Example of timbre transfer using RA VE.
High-level attributes such as the overall loudness and the fundamental frequency of the harmonic
components are kept after performing domain transfer. Other audio attributes such as formants are
absent in the examples coming from the strings dataset, and are added by the model in the speech-
transfered version.
However, there are no guarantees that the encoder will encode signals from an out-of-domain distri-
bution into a latent representation that matches the prior. We empirically evaluate the KL divergence
of two trained RA VE models for in and out-of-domain data distributions, and report the results in
table 3.
Table 3: KL divergence from the prior for in and out-of-domain data.
RA VE Strings RA VE VCTK
data from Strings 0.11± 0.09 0.16± 0.11
data from VCTK 0.24± 0.37 0.09± 0.02
Unsurprisingly, the smallest KL divergences are observed when encoding data sampled from the
training distribution, while encoded out-of-domain signals roughly double the KL divergence.
Stronger transfer abilities may be achieved by integrating a domain adaptation technique such as
the one proposed by Lample et al. (2017) or Mor et al. (2018).
15
