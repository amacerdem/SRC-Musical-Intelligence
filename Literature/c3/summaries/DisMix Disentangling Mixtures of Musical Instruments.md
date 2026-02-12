# DisMix: Disentangling Mixtures of Musical Instruments

**Year:** D:20

---

DisMix: Disentangling Mixtures of Musical Instruments
for Source-level Pitch and Timbre Manipulation
Yin-Jyun Luo1 Kin Wai Cheuk2 Woosung Choi2 Toshimitsu Uesaka2 Keisuke Toyama3
Koichi Saito2 Chieh-Hsin Lai2 Yuhta Takida2 Wei-Hsiang Liao2 Simon Dixon1 Yuki Mitsufuji2,3
1C4DM, Queen Mary University of London
2Sony AI
3Sony Group Corporation
yin-jyun.luo@qmul.ac.uk, kinwai.cheuk@sony.com
Abstract
Existing work on pitch and timbre disentanglement has been
mostly focused on single-instrument music audio, exclud-
ing the cases where multiple instruments are presented. To
fill the gap, we propose DisMix, a generative framework
in which the pitch and timbre representations act as mod-
ular building blocks for constructing the melody and in-
strument of a source, and the collection of which forms a
set of per-instrument latent representations underlying the
observed mixture. By manipulating the representations, our
model samples mixtures with novel combinations of pitch
and timbre of the constituent instruments. We can jointly
learn the disentangled pitch-timbre representations and a la-
tent diffusion transformer that reconstructs the mixture condi-
tioned on the set of source-level representations. We evaluate
the model using both a simple dataset of isolated chords and
a realistic four-part chorales in the style of J. S. Bach, identify
the key components for the success of disentanglement, and
demonstrate the application of mixture transformation based
on source-level attribute manipulation. Introduction
Disentangled representation learning (DRL) captures se-
mantically meaningful latent features of observed data in
a low-dimensional latent space (Bengio, Courville, and
Vincent 2013). By applying a generative framework such
as variational autoencoders (VAEs) (Kingma and Welling
2014), we can train an encoder to encode the data and asso-
ciate data-generating factors with separate subspaces in the
latent space, and a decoder to reconstruct the data given the
original encoding or to render novel data given manipulated
latent features (Tschannen, Bachem, and Lucic 2018; Chen
et al. 2018; Kim and Mnih 2018; Higgins et al. 2016). Because each feature representation lives in a subspace
corresponding to a unique concept or data attribute such as
the size or shape of a physical object in an image, manip-
ulating specific representations only renders variation of a
few and particular factors in the decoder output, and thereby
facilitates controllable transformation of existing data. DRL has been applied to music audio to extract represen-
tations of timbre (e.g., the musical instrument played in a
recording) and pitch (e.g., the melody played by the instru-
ment) (Luo, Agres, and Herremans 2019; C´ıfka et al. 2021; Tanaka et al. 2021; Luo et al. 2020; Tanaka et al. 2022; Luo, Ewert, and Dixon 2022; Engel et al. 2017; Bitton, Esling,
and Chemla-Romeu-Santos 2018; Wu et al. 2023; Liu et al.
2023; Wu et al. 2024a). Disentangling the two attributes en-
ables applications such as transferring the instrument played
in a reference audio to a target instrument provided by an-
other audio example, while preserving the melody played
by the reference instrument. This is similar to voice con-
version, which aims at replacing a reference speaker’s iden-
tity such that the converted speech sounds as if a different
speaker spoke the content originally uttered by the reference
speaker (Hsu, Zhang, and Glass 2017; Qian et al. 2019). Despite being widely adopted for instrument attribute
transfer, pitch-timbre disentanglement has been mostly ap-
plied to single-instrument audio. Therefore, the analysis and
the synthesis of the two attributes are only amenable to a sin-
gle instrument at a time, which excludes cases where multi-
ple instruments are presented in music audio. Alternatively, one can use off-the-shelf source separation
models to first separate each instrument from a mixture and
apply the aforementioned approaches for disentanglement. However, it introduces artefacts into the separated instru-
ment and limits the instruments that can be handled to those
supported by the state-of-the-art source separation mod-
els (e.g., drums, bass, vocals, and others) (Lu et al. 2024; Rouard, Massa, and D´efossez 2023; Hennequin et al. 2020). To fill the gap, we propose DisMix, a framework which
disentangles a mixture of instruments and renders a novel
mixture conditioned on a set of pitch-timbre disentan-
gled representations. DisMix represents each instrument, or
source, in a mixture by a source-level representation that
combines a pair of pitch and timbre latent variables. The two
attributes are encoded separately so that they can be inde-
pendently manipulated for each instrument. A decoder then
takes as input the manipulated set of source-level represen-
tations and renders a new mixture that consists of sources
whose pitch and timbre are dictated by the manipulated
source-level representations. The pitch and timbre representations act as modular build-
ing blocks to construct the melody and instrument of a
source or an “audio object”. The decoder assembles these
objects in a way that preserves their pitch and timbre. This
is reminiscent of “object representation” motivated by hu-
mans’ capability to understand complex ideas in terms of
reusable and primitive components (Greff, van Steenkiste,
and Schmidhuber 2020; Bizley and Cohen 2013).
arXiv:2408.10807v1 [cs. SD] 20 Aug 2024

To extract source-level representations, the pitch and tim-
bre encoders are conditioned on a mixture and queries. The
timbre of each query determines which instrument’s latents
are extracted; the extracted representation should match the
timbre of the query, regardless of their pitch information. We propose two parameterisations of DisMix and eval-
uate using the MusicSlot (Gha et al. 2023) and the Coco-
Chorale dataset (Wu et al. 2022). Our final implementa-
tion admits a latent diffusion model (LDM) (Rombach et al.
2022) which jointly learns the disentangled representations
and a conditional diffusion transformer (DiT) (Peebles and
Xie 2023). Our contributions are summarised as follows:
• We propose DisMix to disentangle pitch and timbre
of constituent sources from multi-instrument mixtures,
whereby it is capable of rendering novel mixtures by ma-
nipulating the attributes of individual instruments.
• Without employing domain-specific data augmentation
or adversarial training, we propose and identify a bina-
risation layer as a key component for disentanglement,
and apply the model to the four-part Bach Chorales from
CocoChorale, which features 13 orchestral instruments.
• Based on the DiT architecture, we demonstrate that re-
constructing a mixture conditioned on a set of jointly
learnt source-level latents can yield superior performance
than iteratively reconstructing a single source at a time. Related Work
Pitch and Timbre Disentanglement
Strategies for pitch-
timbre disentanglement include supervised learning (Luo, Agres, and Herremans 2019; Engel et al. 2017; Bitton, Es-
ling, and Chemla-Romeu-Santos 2018; Wu et al. 2023), met-
ric learning based on domain knowledge (Esling, Chemla-
Romeu-Santos, and Bitton 2018; Tanaka et al. 2021, 2022; C´ıfka et al. 2021; Luo et al. 2020), and more general induc-
tive biases (C´ıfka et al. 2021; Luo, Ewert, and Dixon 2022; Liu et al. 2023; Wu et al. 2024a; Luo, Ewert, and Dixon
2024). Despite their success for tasks such as attribute swap-
ping, these methods are focused on single-instrument input. Instead, we disentangle mixtures of instruments and rep-
resent each instrument by a source-level latent representa-
tion which captures pitch and timbre in separate dimensions. Only a few studies explicitly extract pitch and timbre in-
formation from mixtures of instruments. Hung et al. (2019)
and Cwitkowitz et al. (2024) encode the overall timbre of
a mixture and consider applications of symbolic music re-
arrangement and transcription, respectively. Cheuk et al.
(2023) propose a multi-task framework that conditions mu-
sic pitch transcription on intermediate timbre information. Lin et al. (2021) tackle transcription and separation
of mixtures and single-instrument generation in a unified
framework. Rather than focusing on single-instrument cases,
we are interested in sampling novel mixtures by condition-
ing a DiT on a set of per-instrument representations and we
evaluate our model by source-level attribute manipulation. Object-Centric Representation Learning
Learning ob-
ject representations entails encoding object entities in a vi-
sual scene by unique representations (Greff, van Steenkiste, Figure 1: A mixture xm of Ns instruments is represented by
a set of source-level latents {s(i)}Ns
i=1 integrating latents of
pitch ν(i) and timbre τ (i). Diamond nodes denote determin-
istic mappings.
and Schmidhuber 2020; Locatello et al. 2020). Singh, Kim,
and Ahn (2022); Wu, Lee, and Ahn (2023); Wu et al.
(2024b) take a step further to disentangle attributes of in-
dividual objects for achieving compositional scene genera-
tion. For audio, Gha et al. (2023) and Reddy et al. (2023)
learn separate representations for different sources from
mixtures. We further disentangle pitch and timbre of indi-
vidual sources and tackle a more complex dataset with a
conditional LDM. DisMix: The Proposed Framework
Given a mixture xm of Ns instruments and a query x(i)
q
(detailed in Section 3.1), our goal is to extract latent rep-
resentations of pitch ν(i) and timbre τ (i) for an instrument
i ∈[1, Ns], and to be able to sample a novel mixture condi-
tioned on a set of manipulated pitch and timbre latents. We propose DisMix to achieve the goal. Its generative
process on the left side of Fig. 1 samples xm, through a neu-
ral network θm, conditioned on a set of source-level repre-
sentations S = {s(i)}Ns
i=1 where s(i) = fθs(τ (i), ν(i)) is a
deterministic function of timbre and pitch. The pitch latent
ν(i) is computed via a neural network θν by its correspond-
ing ground-truth pitch annotation y(i). The joint distribution
over the variables can be written as follows:
pθm(xm|S)
YNs
i=1 pθν(ν(i)|y(i))p(τ (i)),
(1)
where p(τ (i)) = N

## 0, I

. Note that ν(i) and τ (i) are sam-
pled independently and so are {s(i)}Ns
i=1, whereby the pitch
and timbre latents can act as modular building blocks to
compose a mixture. We propose two instances of DisMix: 1) an auto-encoder
for a simple case study using a simplistic dataset (Section 4)
and 2) an LDM implemented using a DiT verified with a
more complex dataset (Section 5). We specify θm, θs, and
θν for the two instances in Sections 4 and 5, respectively. Here, we describe the common components between them. Following VAEs (Kingma and Welling 2014), we learn
DisMix using an inference network to approximate posteri-
ors over the latent variables that are otherwise intractable,
and learns the model by maximising a lower bound to the
marginal likelihood p(xm|{y(i)}Ns
i=1). For the two instances
of DisMix, we employ a common parameterisation of the in-
ference network illustrated on the right side of Fig. 1, which
we explain in the following sections.

3.1
Mixture and Query Encoders
Given a mixture of instruments, additional information
would be necessary to specify which instrument’s latents are
to be extracted. Motivated by Lin et al. (2021) and Lee, Choi,
and Lee (2019), we use the query x(i)
q
so that the extracted
latents of the source i and the query share the same timbre
characteristics, while they can carry arbitrary pitch informa-
tion. We describe the objective function Eq. (7) that could
encourage this behaviour in Section 3.3. During training, we pair each mixture xm with Xq =
{x(i)
q }Ns
i=1, a set of Ns queries with their instruments corre-
sponding to the constituent instruments of the mixture, and
each x(i)
q
is randomly sampled from a subset of the complete
training dataset consisting of a constituent instrument. As illustrated on the right side of Fig. 1, the inference of
τ (i) and ν(i) is conditioned on both xm and x(i)
q. In practice,
we extract their compact counterparts em = Eϕm(xm) and
e(i)
q
= Eϕq(x(i)
q ), respectively, where Eϕm(·) and Eϕq(·) are
neural network encoders with parameters ϕm and ϕq.
3.2
Pitch and Timbre Encoders
As suggested by Fig. 1, we propose that the pitch and timbre
encoders admit a common factorised form:
qϕu(U|xm, Xq) =
YNs
i=1 qϕu(u(i)|em, e(i)
q ),
(2)
where u ∈{ν, τ} and U ∈{{ν(i)}Ns
i=1, {τ (i)}Ns
i=1}. ϕν and
ϕτ are parameters of the two encoders. Given em and e(i)
q,
the pitch and timbre latents of the i-th source are encoded
independently of each other and of other sources. We apply a binarisation layer (Dong and Yang 2018) to
constrain the capacity of the pitch latent, which is proven
crucial for disentanglement in our empirical studies. We also
show that imposing the standard Gaussian prior p(τ (i)) is a
simple yet effective way to constrain the timbre latent. Constraining Pitch Latents
The pitch encoder combines
a transcriber Eϕν(·) that extracts pitch logits of the i-th
source ˆy(i) = Eϕν(em, e(i)
q ), a stochastic binarisation layer
(SB) that constrains the information capacity, and a transla-
tor fθν(·) that computes the final outcome:
qϕν(ν(i)|em, e(i)
q ):= δ(ν(i) −fϕν(ˆy(i)
bin)),
(3)
where δ(·) is the Dirac delta function, corresponding to the
diamond node of ν(i) on the right of Fig. 1, and:
ˆy(i)
bin = SB(ˆy(i)) = 1{Sigmoid(ˆy(i))>h},
(4)
where 1{·} is the indicator function, and h is the threshold
sampled from the uniform distribution U(0,1) at each train-
ing step and is fixed at 0.5 during evaluation. The straight-
through estimator (Bengio, L´eonard, and Courville 2013) is
used to bypass the non-differentiable operator. Table 1 suggests that the bottleneck imposed by the bina-
risation layer is crucial for disentanglement even if a pitch
classification loss is included. We also show that using only
SB without the pitch supervision still yields a decent perfor-
mance in Table 3. Constraining Timbre Latents
The timbre encoder pa-
rameterises a Gaussian with a neural network ϕτ:
qϕτ (τ (i)) = N(τ (i); µϕτ (em, e(i)
q ), σ2
ϕτ (em, e(i)
q )I),
(5)
where qϕτ (τ (i)):= qϕτ (τ (i)|em, e(i)
q ) and sampling τ (i) is
reparameterised as µϕτ (·) + ϵσϕτ (·), where ϵ ∼N

## 0, I

, to
be differentiable (Kingma and Welling 2014). We let p(τ (i)) = N

## 0, I


to constrain the timbre latent
through the Kullback–Leibler divergence (KLD) in Eq. (6).
3.3
Training Objectives
ELBO
We start with an evidence lower bound (ELBO) to
the marginal log-likelihood log p(xm|{y(i)}Ns
i=1):

## LELBO = EQ

i qϕτ (τ (i))

log pθm(xm|{τ (i), ˆν(i)}Ns
i=1)

+
X
i log pθν(ˆν(i)|y(i)) −DKL
qϕτ (τ (i))∥p(τ (i))
,
(6)
where ˆν(i) = fϕν(ˆy(i)
bin) by Eq. (3). Note that the condi-
tionals of the first term can be expressed in terms of S =
{s(i)}Ns
i=1, where s(i) = fθs(τ (i), ˆν(i)) as described previ-
ously for Eq. (1). LELBO is derived as a result of the fac-
torised posteriors in Eq. (2) and the deterministic pitch en-
coder by Eq. (3), which we detail in Appendix A. We specify
θm, θs, and θν in Section 4 and 5. Intuitively speaking, we extract both a pitch and a timbre
latent for each source given a mixture and a query, and the
collection of which is used to reconstruct the mixture. The
pitch and timbre latents adhere to certain constraints and pri-
ors to encourage the disentanglement of the two attributes. Apart from mixtures, we also observe individual sources
x(i)
s, so we include a source-wise reconstruction loss. This
is a special case of the first term in Eq. (6) when Ns = 1
and xm becomes x(i)
s, and we can reuse θm to reconstruct
individual sources. Pitch Supervision
To enhance the disentanglement, we
also minimise a binary cross entropy loss BCE(ˆy(i), y(i))
where y(i) is the pitch annotation of the i-th source. We ex-
plore relaxing the model by excluding this term, with the
results reported in Table 3. Barlow Twins
Finally, we minimise a simplified Barlow
Twins loss (Zbontar et al. 2021) to enhance the correlation
between the query and the timbre latent for them sharing the
timbre characteristics as described in Section 3.1:

## LBT =

XNs
i=1
XDτ
d=1(1 −Cdd(e(i)
q, τ (i)))2,
(7)
where C is a cross-correlation matrix, and both e(i)
q
and τ (i)
share the same dimensionality Dτ. Empirically, LBT coun-
teracts the over-regularisation effect of the prior p(τ (i)) and
promotes a discriminative timbre space as shown in Fig. 2. The Final Objective
In summary, we maximise: LDisMix = LELBO −LBCE −LBT.
(8)
We do not find explicitly weighting each loss term necessary. Next, we detail the implementations specific to the sim-
ple and more sophisticated variants of DisMix in Sections 4
and 5, respectively. A Simple Case Study
Reconstructing Mixtures
pθm(xm|S) in
Eq. (6) is a
Gaussian likelihood parameterised by a decoder θm, which
can be a permutation invariant function such as a trans-
former (Vaswani et al. 2017) without positional embeddings
that outputs the Gaussian mean, reconstructing a mixture
given a set of source-level representations. We opt for a simple implementation of θm here and dis-
cuss a transformer in Section 5. In particular, we slightly
deviate from Eq. (6) and reconstruct xm using em in Sec-
tion 3.1, instead of S, whereby the likelihood becomes
pθm(xm|em), and we maximise an additional term: EQ
i qϕτ (τ (i))

log p(em|{τ (i), ˆν(i)}Ns
i=1
,
(9)
where p(em|S) = N(em; PNs
i=1 s(i), σ2
mI) and σm = 0.25
is a hyperparameter. Intuitively, we extract the source-level
latents S = {s(i)}Ns
i=1 whose summation ssum = P
i s(i)
and em are pulled together as measured by a mean square
error weighed by σ−2
m. During evaluation, we instead use ssum to reconstruct the
mixture xm or render a novel one by manipulating {s(i)}Ns
i=1
before the summation. The assumption is that both em and
ssum can reconstruct xm comparably well by maximis-
ing Eq. (9) as we reconstruct xm by em during training. This approach avoids implementing a (potentially expen-
sive and complicated) permutation invariant decoder and im-
poses linearity between em and ssum in the latent space. The
linearity could enable other applications, which we explain
in Appendix B.1 and leave for future work. Integrating Pitch and Timbre
We employ FiLM (Perez
et al. 2018; Kim et al. 2018a) and derive the source-level
representation as s(i) = fθm(τ (i), ν(i)) = αθs(τ (i))⊙ν(i) +
βθs(τ (i)), where ν(i) is scaled and shifted element-wise by
the factors determined as a deterministic function θs of τ (i). Configuring Pitch Priors
We study pitch priors at dif-
ferent levels of capacity. The first follows Eq. (1) and de-
fines pθν(ν(i)|y(i)) = N(ν(i); µfac
θν (y(i)), σ2
νI), a Gaussian
parameterised by θν given the ground-truth pitch y(i). σν is
a hyperparameter. We also consider a richer prior to capture the source inter-
action: pθν(ν(i)|Y\i) = PK
k=1 πkN
ν(i); µrich
θν,k(Y\i), σ2
νI
,
where Y\i denotes a set of pitch annotations excluding that
of the i-th source, and θν,k parameterises the mean of the
k-th Gaussian in a Gaussian mixture. The rationale is that
ˆy(i) is conditionally dependent on pitch of other sources in a
mixture to confer musical harmony.
4.1
Implementations
Dataset
Gha et al. (2023) compile synthetic audio us-
ing 3,131 unique chords from JSB Chorales (Boulanger-
Lewandowski, Bengio, and Vincent 2012), rendered by
sound fonts of piano, violin, and flute via FluidSynth. Given a chord, each composite note is synthesised to an
audio waveform at 16kHz with a sound font randomly sam-
pled with replacement, whereby a sound font i can play
multiple notes in a chord. These notes together define a
source x(i)
s
whose pitch annotation is a mutli-hot vector
y(i) ∈{0, 1}Np. The note waveforms are summed to form
the chord’s waveform which defines a mixture xm. There are 28,179 samples of mixtures split into the train,
validation, and test sets with a ratio of 70/20/10. The wave-
forms are converted into mel spectrograms using 128 mel-
filter bands, a window size of 1,024, and a hop length of

### 512. We crop a 320ms segment, or 10 spectral frames, from

the sustain phase of each sample. Architecture
Simple layers including the MLP and RNN
are used for implementation to evaluate this simple case
study, and we extend DisMix to a more complex setup with
an LDM in Section 5. A major difference between the two
setups is that both ν(i) and τ (i) are represented as a single
vector, as pitch and timbre are time-invariant within the sim-
plified scope of the MusicSlot dataset (Gha et al. 2023). On
the other hand, the CocoChorale dataset (Wu et al. 2022)
features time-varying melodies in each sample. We elabo-
rate the implementation details in Appendix B.1. Optimisation
We use Adam (Kingma and Ba 2015) and
a batch size of 32, a learning rate of 0.0004, and a gradient
clipping value of 0.5. Training is terminated if Eq. (8) stops
improving on the validation set for 260k steps.
4.2
Results
Evaluation
Given xm and a set of queries {x(i)
q }Ns
i=1 cor-
responding to the constituent instruments of the mixture,
we first extract {τ (i), ν(i)}Ns
i=1. To evaluate disentanglement,
we conduct a random permutation so that the pitch latent
of the source i can be swapped for that of the source j,
while the timbre remains unchanged, which yields ˆs(i) =
fθs(τ (i), ν(j)). Then, we render a novel source ˆxs
(i) by pass-
ing ˆs(i) to the decoder pθm. Note that we render sources in-
stead of mixtures by using ˆs(i) as the input instead of the
summation of multiple source-level representations. A successful disentanglement entails that judges of pitch
and instrument should classify ˆx(i)
s
as the pitch of x(j)
s
(as
it was swapped) and the instrument of x(i)
s
(as it was pre-
served), respectively. We pre-train a pitch and an instrument
classifier using the training set and direct them as the judges. The classification accuracy is reported under “Disentangle-
ment” in Table 1 and 2. To see if the model can render novel mixtures, we first
produce a new set {ˆs(i)}Ns
i=1 after the permutation and ren-
der a novel mixture ˆxm by passing pθm the summation
ˆssum = P
i ˆs(i). To check whether the constituent attributes
of ˆxm are indeed dictated by the manipulated {ˆs(i)}Ns
i=1, we
once again extract its source-level representations with the
original queries and reconstruct the sources, which are then
fed to the judges. “Mixture Rendering” in Table 1 and 2 re-
port the classification accuracy. Examples
Fig. 2 shows mel spectrograms on the right
side. The first row shows queries for different instruments. The second row shows an input mixture xm and the corre-
sponding sources. The timbre characteristics are consistent

Disentanglement
Mixture Rendering
Pitch
Inst. Pitch
Inst. DisMix
93.39%
100.00%
90.69%
100.00%

## - LBT

93.18%
99.92%
87.92%
100.00%

## - KLD

69.41%
100.00%
35.10%
100.00%

## - SB

93.46%
46.71%
40.23%
98.91%
Table 1: Ablation study: classification accuracy for various
loss terms for the simple case study. Figure 2: Left: PCA of the timbre space. Top: DisMix,
plot τ (i). Mid and bottom: Remove LBT, plot the mean of
qϕτ (τ (i)) and the sampling, respectively. Right: Novel mix-
ture rendering. Refer to Section 4.2 for details.
across rows for the last three columns. In the third row, the
leftmost is the reconstructed mixture given ssum and the rest
are the reconstructed sources given s(i). The first column of the last row refers to the manipu-
lated mixture rendered by ˆssum, and the rest are the sources
extracted from the mixture using the original queries. At-
tributes are successfully manipulated. In the last row, the
second column combines the first source’s timbre with the
second’s pitch, and the third column combines the second’s
timbre with the first’s pitch. The third source is unchanged. Ablation Study
Table 1 is an ablation study of the loss
term for identifying the key loss terms for disentanglement. The table suggests that removing the KLD in Eq. (6), or the
prior p(τ (i)) from the timbre latent space, contaminates the
timbre latent τ (i) with the pitch information. Consequently,
the pitch of ˆx(i)
s
is determined not only by ν(j), but also by
τ (i), leading to a low pitch accuracy of 69.41%. On the other hand, removing the SB layer introduces ex-
cessive capacity for the pitch latent, such that the instrument
of ˆx(i)
s
is dictated by both τ (i) and ν(j), resulting in a low
instrument classification accuracy of 46.71%. Even though
the BCE loss for pitch supervision is always included in the
training, the model fails to disentangle without SB, suggest-
ing that an additional information constraint is necessary in
addition to supervision to achieve disentanglement. In terms of mixture rendering, removing LBT negatively
DisMix
+fac
+rich (K=10)
Disentanglement
93.39% 93.98%
94.18%
Mixture Rendering 90.69% 91.15%
92.04%
Table 2: Pitch accuracy using different pitch priors.
affects pitch accuracy. This could be attributed to the timbre
prior p(τ (i)) which potentially over-regularises τ (i), leading
to noisy samples of τ (i) due to a large posterior variance
σ2
ϕτ (·). This could cause a poor optimisation of Eq. (9), ag-
gravating the existing gap between using em and ssum for
mixture reconstruction during training and evaluation, re-
spectively. The left side of Fig. 2 shows that, when LBT is
removed, the instrument clusters in the timbre space disap-
pear from the PCA of τ (i) ∼qϕτ (τ (i)|em, e(i)
q ), suggesting
excessively noisy sampling. Pitch Priors
In Table 2, we compare the pitch priors dis-
cussed in Section 4 in terms of pitch accuracy. It includes the
model without a pitch prior (DisMix), with the factorised
prior (fac), and with the one that captures the source inter-
action by a Gaussian mixture of K = 10 components. The
standard deviation σν is 0.5 in both cases. We can observe
that the accuracy improves with a richer prior. A Latent Diffusion Framework
We also implement DisMix by an LDM framework (Rom-
bach et al. 2022), where the decoder pθm(xm|S) is a diffu-
sion transformer (DiT) (Peebles and Xie 2023) that directly
reconstructs a mixture given a set of source-level latents, and
no additional objective such as Eq. (9) is introduced. Data Representation
The LDM framework (Rombach
et al. 2022) improves the compute efficiency of diffusion
models (DMs) (Sohl-Dickstein et al. 2015; Ho, Jain, and
Abbeel 2020) by first projecting data to a low-dimensional
latent space. We leverage the pre-trained VAE from Audi-
oLDM2 (Liu et al. 2024) which is trained on multiple mu-
sic and audio datasets to extract z(i)
s
= Evae(x(i)
s ), where
Evae(·) is the VAE encoder, and we use the pre-trained VAE
decoder Dvae(·) to recover x(i)
s. Latent Diffusion Models
LDMs operate DMs in a latent
space and sample z0, the latent representation of data, from
a Markov chain: p(zT ) QT
t=1 pθ(zt−1|zt), with p(zT ) =
N(zT; 0, I) and pθ(zt−1|zt) = N(zt−1; µθ(zt, t), Σθ(zt, t))
parameterised by θ. The posterior is a linear Gaussian
q(zt|zt−1) = N(zt; √αtzt−1,(1 −αt)I), where αt is a hy-
perparameter evolving over the diffusing step t. Given that the forward process q is known and fixed, Ho, Jain, and Abbeel (2020) employ specific forms of µθ and Σθ
to match q and simplify the training to essentially minimis-
ing ∥fθ(zt, t)−z0∥2
2, which boils down to training a decoder
fθ to predict the clean z0 given its corrupted counterpart zt.

5.1
Adapting Diffusion Transformers
Different from the vanilla LDMs, we condition the decoder
with S, replacing the first term of Eq. (6) with:
pθm(zm,0: T |S) = p(zm, T )
YT
t=1 pθm(zm,t−1|zm,t, S).
(10)
zm,t denotes the noised latent feature of mixtures at dif-
fusing step t and is defined in terms of {z(i)
s,t}Ns
i=1, where
z(i)
s,0 = z(i)
s. pθm models the interaction among the elements
in the set S = {s(i)}Ns
i=1 and iteratively performs the reverse
process. Defining zm,t in terms of the constituent sources
facilitates the conditioning mechanism that we explain next. Partition
DiTs (Peebles and Xie 2023) operate on a se-
quence of image patches to work with a transformer. Simi-
larly, we first apply a sinusoidal positional encoding to z(i)
s
to preserve the temporal order and partition it by Par(z(i)
s ): RTz×(Dz×C) →RL×D′
z, where Tz = 100, Dz = 16, C = 8, and L = 25 are the numbers of time frames, feature
dimensions, channels, and patches, respectively. That is, we
partition along the time axis and flatten each patch whose
size becomes D′
z = Tz
L ×Dz ×C. We repeat the process for
all Ns elements in {z(i)
s }Ns
i=1, the outcome of which finally
defines zm,t ∈R(Ns×L)×D′
z in Eq. (10). In other words, we
can consider it as a sequence of Ns × L patches, with the
size of each patch being D′
z. Similarly, we partition the source-level representations
S = {s(i)}Ns
i=1 and obtain sc ∈R(Ns×L)×D′
s, where D′
s =
Tz
L × Ds × C, which we detail in Section 5.2. We can then
represent the set condition S by sc in Eq. (10). As mentioned earlier, we define zm,t in terms of its con-
stituent sources and conveniently align the dimensions of sc
and zm,t (except for their sizes D′
z and D′
s) which facilitates
the conditioning described next. We do not add another positional encoding to zm,t and sc,
ensuring the permutation invariance w.r.t. the Ns sources. Conditioning
A transformer block consists of the multi-
head self-attention mechanism and a feedforward network. Each of these modules is followed by a skip connection and
a layer normalisation (LN) (Vaswani et al. 2017). We replace
the standard LN with its adaptive variant (adaLN) for the
conditioning (Peebles and Xie 2023). In particular, sc is added with a diffusing step embedding
and is used to regress the scaling and shifting factors ρ and γ
of adaLN layers which match the dimension of zm,t. Then,
by passing zm,t through the transformer blocks, it is mod-
ulated by ρ and γ which carry the source-level pitch and
timbre information computed from sc.
5.2
Implementations
Dataset
The CococChorale dataset (Wu et al. 2022)
provides realistic generative music in the style of Bach
Chorales (Boulanger-Lewandowski, Bengio, and Vincent
2012), featuring 13 orchestral instruments played at the pitch
ranges of a standard four-part chorale (i.e., Soprano, Alto, Tensor, Bass, or SATB). We use the random ensemble subset of 60,000 four-part
chorales, totalling 350 hours of audio. Each part of an ex-
ample is played by an instrument randomly sampled from
a pool of instruments belonging to the part. The maxi-
mum number of sources Ns is four. The pitch annotation
y(i) ∈{0,1}Np×Tp is a time sequence of one-hot vectors. The dataset follows a split ratio of 80/10/10 for the training,
validation, and test sets. Each audio file is sampled at 16kHz and is converted into
mel spectrograms using 64 mel-filter bands, a window size
of 1,024, and a hop length of 160. We randomly sample a
four-second segment for each example during training. Architecture
We reuse the architecture of the pre-trained
VAE encoder Evae and decoder Dvae from AudioLDM2 (Liu
et al. 2024) to implement parts of our encoders, which leads
to the a pitch latent ν(i) ∈RC×Tz×Dz and a timbre latent
τ (i) ∈RC×1×Dz. Note that we compute a time-invariant
timbre latent to reflect the fact that the instrument identity
does not change within each individual source. The source-
level representation s(i) ∈RC×Tz×Ds simply concatenates
ν(i) and τ (i), where Ds = 2Dz. We can then apply the par-
tition method to {s(i)}Ns
i=1 and obtain sc ∈R(Ns×L)×D′
s. By Eq. (10), we can reconstruct zm, defined in terms of
{z(i)
s }Ns
i=1, by sampling the DiT pθm conditioned on the set
S, represented as sc. We use HiFi-GAN (Kong, Kim, and
Bae 2020) to convert the reconstructed mel spectrograms
Dvae(ˆz(i)
s ) back to audio ˆxs
(i), and we can obtain the mix-
ture by ˆxm = PNs
i=1 ˆx(i)
s. More implementation details are
left in Appendix B.2
Optimisation
We use Adam (Kingma and Ba 2015) with a
batch size of eight and a gradient clipping value of 0.5. The
learning rate warms up linearly to 0.0001 over 308k steps
and decreases following the cosine wave (Loshchilov and
Hutter 2017) for a maximum of 4,092k steps.
5.3
Results
Evaluation
Given a reference mixture and its extracted set
of pitch and timbre latents {τ (i), ν(i)}Ns
i=1, we arbitrarily re-
place the timbre latents {τ (i)}Ns
i=1 with the set from another
target mixture. We expect that the four instruments of the
reference mixture are replaced by those of the target mixture
and that the target instruments play the original melodies of
the reference instruments. We ensure that each instrument
is swapped for the instrument labelled as the same SATB
part in the target mixture, so that the target instruments play
melodies that match their pitch range. We sample {ˆz(i)
s }Ns
i=1 from N

## 0, I


conditioned on the
manipulated set of timbre and pitch latents (Eq. (10)) and
sample {ˆx(i)
s }Ns
i=1 with T = 1000 steps. We expect that
feeding ˆx(i)
s
to pre-trained instrument and pitch classifiers
produces the targeted instrument and the original reference
melody, respectively. Because the mixture is obtained by
ˆxm = PNs
i=1 ˆx(i)
s
in the audio domain, the evaluation of dis-
entanglement suggests the results of mixture rendering. The
results are reported in Table 3. Instrument (↑)
Pitch (↑)

## FAD (↓)

Set
Single
Set
Single
Set
Single
M0
89.94
96.43
94.37
97.15
2.27
2.13
M1
97.49
96.05
97.15
97.02
2.10
2.14
M2
82.83
80.16
97.19
97.03
2.14
2.14
Table 3: Disentanglement in terms of instrument and pitch
classification (%) and audio quality in terms of FAD. Benchmark
To justify the design that conditions the de-
coder with a set of source-level representations, we experi-
ment with a model variant trained exclusively to reconstruct
one source conditioned on a single source-level latent at a
time. Instead of rendering all sources in T steps of diffusion
sampling, this variant iteratively renders Ns sources to re-
cover a mixture, totalling Ns × T steps. This could serve as
a proxy to Lin et al. (2021) as they similarly use a query-
based encoder to extract a pitch and a timbre latent of a sin-
gle source and condition a decoder to reconstruct the source. Moreover, we relax the training by discarding the BCE
loss in Eq. (8) and evaluate whether the model can achieve
decent performance without explicit pitch supervision. Disentanglement
In Table 3, M0 is the single source-
conditioned variant, M1 is the proposed set-conditioned
model, and M2 drops the pitch supervision. “Set” and “Sin-
gle” denote rendering {ˆx(i)
s }Ns
i=1 conditioned on a set of
source-level representations and a single condition for Ns it-
erations, respectively. The transformer accepts varying input
sequence lengths, whereby all the models can operate with
the two approaches regardless of how they were trained. M1 yields the best instrument classification accuracy at
97.49% with the set-conditioned method, slightly outper-
forming M0 under the single source-conditioned setup at
96.43%. M1’s accurate instrument classification is reflected
in the discriminative timbre space shown in Fig. 3. Surprisingly, M0 yields decent performance using the set-
conditioned approach (89.94% and 94.37% for instrument
and pitch accuracy) although it was not trained for the setup. M2 achieves a decent performance without the pitch su-
pervision, which implies the efficacy of the SB layer pro-
posed for disentanglement. The inferior instrument accuracy
suggests the pitch latent is contaminated by timbre. Redun-
dant information is preserved in the pitch latent for a good
reconstruction, and thus M2 maintains a high pitch accuracy. Fr´echet Audio Distance (FAD)
For each one of the 13
instruments, we compute an FAD (Kilgour et al. 2018) by
comparing the VGG feature extracted from ˆx(i)
s
and that of
the original data. A successful timbre swapping and a good
audio quality are necessary for achieving a low FAD. Table 3
reports the averaged FAD and suggests that the proposed M1
performs the best under the setup (Set) it was trained for. Together, Table 3 verifies the proposed design of the set-
conditioned reconstruction by showing a better performance
than its single source-conditioned counterpart. Figure 3: Left: PCA of the timbre space. Right: Composi-
tional mixture rendering is achieved by modifying the mem-
bers of a set of source-level latents. Figure 4: Replacing instruments of a reference mixture (the
top row) given a target mixture (the bottom row). Examples
Fig. 4 shows an example of instrument re-
placement between a reference and a target mixture. By
replacing the timbre representations of the first three in-
struments for those from the target mixture, we can ren-
der a new mixture with the targeted instruments playing
the original melodies. We demonstrate audio samples at
yjlolo.github.io/dismix-audio-samples. Compositional Mixture Rendering
The right side of
Fig. 3 showcases an example of compositional mixture syn-
thesis by modifying the members (s(i)) of a set of source-
level representations, instead of manipulating the compo-
nents (τ (i) and ν(i)) of each member. In the leftmost column, we begin with two-source mix-
tures for illustration. We first extract the mixtures’ source-
level latents. Then, by passing only one source to the de-
coder, we can isolate the source as shown in the second and
the third column. Finally, in the last column we can synthe-
sise a new mixture conditioned on a set that takes a source
from each of the two mixtures. The two mixtures effectively
“exchange” one of their sources. Conclusion
We present DisMix to tackle pitch-timbre disentanglement
for multi-instrument mixtures. The pitch and timbre latents
act as modular building blocks, and we are able to render
novel mixtures conditioned on sets of pitch and timbre rep-
resentations. In future work, we plan to relax the model by
addressing the requirement for queries. For applications, we
consider “attribute inpainting” where the decoder is tasked
to fill missing semantic information in its conditional inputs. References
Bengio, Y.; Courville, A.; and Vincent, P. 2013. Represen-
tation Learning: A Review and New Perspectives. In Trans.
on Pattern Analysis and Machine Intelligence. Bengio, Y.; L´eonard, N.; and Courville, A. C. 2013. Estimat-
ing or Propagating Gradients Through Stochastic Neurons
for Conditional Computation. In ArXiv. Bitton, A.; Esling, P.; and Chemla-Romeu-Santos, A. 2018. Modulated Variational Auto-Encoders for Many-to-many
Musical Timbre Transfer. arXiv:1810.00222. Bizley, J. K.; and Cohen, Y. E. 2013. The What, Where
and How of Auditory-Object Perception. Nature Reviews
Neuroscience, 14(10): 693–707. Boulanger-Lewandowski, N.; Bengio, Y.; and Vincent,

## P. 2012. Modeling Temporal Dependencies in High-
Dimensional Sequences: Application to Polyphonic Music
Generation and Transcription. In Int. Conf. on Machine
Learning. Chen, R. T. Q.; Li, X.; Grosse, R. B.; and Duvenaud, D. K.

### 2018. Isolating Sources of Disentanglement in Variational

Autoencoders. In Advances in Neural Information Process-
ing Systems. Cheuk, K. W.; Choi, K.; Kong, Q.; Li, B.; Won, M.; Wang, J.-C.; Hung, Y.-N.; and Herremans, D. 2023. Join-
tist: Simultaneous Improvement of Multi-instrument Tran-
scription and Music Source Separation via Joint Training.
arXiv:2302.00286. Cwitkowitz, F.; Cheuk, K. W.; Choi, W.; Mart´ınez-Ram´ırez, M. A.; Toyama, K.; Liao, W.-H.; and Mitsufuji, Y. 2024. Timbre-Trap: A Low-resource Framework for Instrument-
agnostic Music Transcription. In Int. Conf. on Acoustics, Speech and Signal Processing. C´ıfka, O.; Ozerov, A.; S¸ims¸ekli, U.; and Richard, G. 2021. Self-Supervised VQ-VAE for One-Shot Music Style Trans-
fer. In Int. Conf. on Acoustics, Speech and Signal Process-
ing. Dong, H.-W.; and Yang, Y.-H. 2018. Convolutional Gener-
ative Adversarial Networks with Binary Neurons for Poly-
phonic Music Generation. In Proc. of the Int. Soc. for Music
Information Retrieval. Engel, J.; Resnick, C.; Roberts, A.; Dieleman, S.; Norouzi, M.; Eck, D.; and Simonyan, K. 2017. Neural Audio Synthe-
sis of Musical Notes with WaveNet Autoencoders. In Proc.
of the Int. Conf. on Machine Learning. Esling, P.; Chemla-Romeu-Santos, A.; and Bitton, A. 2018. Generative Timbre Spaces with Variational Audio Synthesis. In Proc. of the Int. Conf. on Digital Audio Effects. Gha, J.; Herrmann, V.; Grewe, B.; Schmidhuber, J.; and
Gopalakrishnan, A. 2023. Unsupervised Musical Object
Discovery from Audio. In Conf. on Neural Information Pro-
cessing Systems, ML4Audio Workshop. Greff, K.; van Steenkiste, S.; and Schmidhuber, J. 2020. On
the Binding Problem in Artificial Neural Networks. ArXiv,
abs/2012.05208. Hennequin, R.; Khlif, A.; Voituret, F.; and Moussallam, M.

### 2020. Spleeter: A Fast and Efficient Music Source Separa-

tion Tool with Pre-trained Models. Journal of Open Source
Software, 5(50): 2154. Higgins, I.; Matthey, L.; Pal, A.; Burgess, C.; Glorot, X.; Botvinick, M.; Mohamed, S.; and Lerchner, A. 2016. beta-
VAE: Learning Basic Visual Concepts with a Constrained
Variational Framework. In Int. Conf. on Machine Learning. Ho, J.; Jain, A.; and Abbeel, P. 2020. Denoising diffusion
probabilistic models. Advances in neural information pro-
cessing systems, 33: 6840–6851. Hsu, W.-N.; Zhang, Y.; and Glass, J. 2017. Unsupervised
Learning of Disentangled and Interpretable Representations
from Sequential Data. In Advances in Neural Information
Processing Systems, volume 30. Hung, Y.-N.; Chiang, I.-T.; Chen, Y.-A.; and Yang, Y.-H.

### 2019. Musical Composition Style Transfer via Disentangled

Timbre Representations. In Proc. of the Int. Joint Conf. on
Artificial Intelligence. Kilgour, K.; Zuluaga, M.; Roblek, D.; and Sharifi, M. 2018. Fr\’echet audio distance: A metric for evaluating music en-
hancement algorithms. arXiv preprint arXiv:1812.08466. Kim, H.; and Mnih, A. 2018. Disentangling by Factorising. In Proc. of the Int. Conf. on Machine Learning. Kim, J. W.; Bittner, R.; Kumar, A.; and Bello, J. P. 2018a. Neural Music Synthesis for Flexible Timbre Control. In Int. Conf. on Acoustics, Speech and Signal Processing. Kim, J. W.; Salamon, J.; Li, P.; and Bello, J. P. 2018b. Crepe: A convolutional representation for pitch estimation. In Proc.
of the Int Conf on Acoustics, Speech and Signal Processing. Kingma, D. P.; and Ba, J. 2015. Adam: A Method for
Stochastic Optimization. In Proc. of the Int. Conf. on Learn-
ing Representations. Kingma, D. P.; and Welling, M. 2014. Auto-encoding Vari-
ational Bayes. In Int. Conf. on Learning Representations. Kong, J.; Kim, J.; and Bae, J. 2020. HiFi-GAN: Generative
Adversarial Networks for Efficient and High Fidelity Speech
Synthesis. Advances in Neural Information Processing Sys-
tems, 33: 17022–17033. Lee, J. H.; Choi, H.-S.; and Lee, K. 2019. Audio Query-
based Music Source Separation. In Int. Soc. for Music In-
formation Retrieval. Lin, L.; Kong, Q.; Jiang, J.; and Xia, G. 2021. A Unified
Model for Zero-shot Music Source Separation, Transcrip-
tion and Synthesis. In Int. Soc. for Music Information Re-
trieval. Liu, H.; Yuan, Y.; Liu, X.; Mei, X.; Kong, Q.; Tian, Q.; Wang, Y.; Wang, W.; Wang, Y.; and Plumbley, M. D. 2024. AudioLDM 2: Learning Holistic Audio Generation With
Self-Supervised Pretraining. Trans on Audio, Speech, and
Language Processing, 32: 2871–2883. Liu, X.; Chin, D.; Huang, Y.; and Xia, G. 2023. Learning
Interpretable Low-dimensional Representation via Physical
Symmetry. In Conf. on Neural Information Processing Sys-
tems. Locatello, F.; Weissenborn, D.; Unterthiner, T.; Mahendran, A.; Heigold, G.; Uszkoreit, J.; Dosovitskiy, A.; and Kipf, T. 2020. Object-Centric Learning with Slot Attention. In
Advances in Neural Information Processing Systems. Loshchilov, I.; and Hutter, F. 2017. SGDR: Stochastic Gra-
dient Descent with Warm Restarts. In Proc. of the Int. Conf.
on Learning Representations. Lu, W.-T.; Wang, J.-C.; Kong, Q.; and Hung, Y.-N. 2024. Music Source Separation With Band-Split Rope Trans-
former. In Proc. of the Int. Conf. on Acoustics, Speech and
Signal Processing. Luo, Y.-J.; Agres, K.; and Herremans, D. 2019. Learning
Disentengled Representations of Timbre and Pitch for Mu-
sical Instrument Sounds Using Gaussian Mixture Variational
Autoencoders. In Int. Soc. for Music Information Retrieval. Luo, Y.-J.; Cheuk, K. W.; Nakano, T.; Goto, M.; and Herre-
mans, D. 2020. Unsupervised Disentanglement of Pitch and
Timbre for Isolated Musical Instrument Sounds. In the Int. Soc. for Music Information Retrieval. Luo, Y.-J.; Ewert, S.; and Dixon, S. 2022. Towards Ro-
bust Unsupervised Disentanglement of Sequential Data —
A Case Study Using Music Audio. In Int. Joint Conf. on
Artificial Intelligence. Luo, Y.-J.; Ewert, S.; and Dixon, S. 2024. Unsupervised
Pitch-Timbre Disentanglement of Musical Instruments Us-
ing a Jacobian Disentangled Sequential Autoencoder. In
Proc. of the Int. Conf. on Acoustics, Speech and Signal Pro-
cessing. Peebles, W.; and Xie, S. 2023. Scalable Diffusion Models
with Transformers. In Proc. of the Int. Conf. on Computer
Vision. Perez, E.; Strub, F.; de Vries, H.; Dumoulin, V.; and
Courville, A. 2018. FiLM: Visual Reasoning With a Gen-
eral Conditioning Layer. In AAAI Conf. on Artificial Intelli-
gence. Qian, K.; Zhang, Y.; Chang, S.; Yang, X.; and Hasegawa-
Johnson, M. 2019. AutoVC: Zero-Shot Voice Style Transfer
with Only Autoencoder Loss. In Proc. of the Int. Conf. on
Machine Learning. Reddy, P.; Wisdom, S.; Greff, K.; Hershey, J. R.; and Kipf, T. 2023. Audioslots: A Slot-Centric Generative Model For
Audio Separation. In Proc. of the Int. Conf. on Acoustics, Speech, and Signal Processing Workshops. Rombach, R.; Blattmann, A.; Lorenz, D.; Esser, P.; and Om-
mer, B. 2022. High-Resolution Image Synthesis with Latent
Diffusion Models. In Proc. of the Int. Conf. on Computer
Vision and Pattern Recognition (CVPR). Rouard, S.; Massa, F.; and D´efossez, A. 2023. Hybrid Trans-
formers for Music Source Separation. In Proc. of the Int. Conf. on Acoustics, Speech and Signal Processing. Singh, G.; Kim, Y.; and Ahn, S. 2022. Neural Systematic
Binder. In Proc. of the Int. Conf. on Learning Representa-
tions. Sohl-Dickstein, J.; Weiss, E.; Maheswaranathan, N.; and
Ganguli, S. 2015. Deep unsupervised learning using
nonequilibrium thermodynamics. In Proc. of the Int. Conf.
on Machine Learning. Tanaka, K.; Bando, Y.; Yoshii, K.; and Morishima, S. 2022. Unsupervised Disentanglement of Timbral, Pitch, and Vari-
ation Features From Musical Instrument Sounds With Ran-
dom Perturbation. In Asia-Pacific Signal and Information
Processing Association Annual Summit and Conference. Tanaka, K.; Nishikimi, R.; Bando, Y.; Yoshii, K.; and Mor-
ishima, S. 2021. Pitch-Timbre Disentanglement Of Musical
Instrument Sounds Based On Vae-Based Metric Learning. In Proc. of the Int. Conf. on Acoustics, Speech and Signal
Processing. Tschannen, M.; Bachem, O.; and Lucic, M. 2018. Recent
Advances in Autoencoder-Based Representation Learning. ArXiv, abs/1812.05069. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A. N.; Kaiser, L.; and Polosukhin, I. 2017. At-
tention is All you Need. In Conf. on Neural Information
Processing Systems. Wu, Y.; Gardner, J.; Manilow, E.; Simon, I.; Hawthorne, C.; and Engel, J. 2022. The Chamber Ensemble Generator: Limitless High-Quality MIR Data via Generative Modeling.
arXiv preprint arXiv:2209.14458. Wu, Y.; He, Y.; Liu, X.; Wang, Y.; and Dannenberg, R. B.
2023. Transplayer: Timbre Style Transfer with Flexible
Timbre Control. In Proc. of the Int. Conf. on Acoustics, Speech and Signal Processing. Wu, Y.; Wang, Z.; Raj, B.; and Xia, G. 2024a. Emergent
Interpretable Symbols and Content-Style Disentanglement
via Variance-Invariance Constraints. arXiv:2407.03824. Wu, Y.-F.; Lee, M.; and Ahn, S. 2023. Neural Language
of Thought Models. In Proc. of the Int. Conf. on Learning
Representations. Wu, Z.; Rubanova, Y.; Kabra, R.; Hudson, D. A.; Gilitschen-
ski, I.; Aytar, Y.; van Steenkiste, S.; Allen, K. R.; and Kipf, T. 2024b. Neural Assets: 3D-Aware Multi-Object Scene
Synthesis with Image Diffusion Models.
arXiv preprint
arXiv:2406.09292. Zbontar, J.; Jing, L.; Misra, I.; LeCun, Y.; and Deny, S. 2021. Barlow Twins: Self-Supervised Learning via Redundancy
Reduction. In Proc. of the Int. Conf. on Machine Learning. A
Derivation of LELBO
For a multi-instrument mixture containing Ns sources, we define its corresponding sets of the pitch annotations, the timbre
latents, and the pitch latents as Y = {y(i)}Ns
i=1, T = {τ (i)}Ns
i=1, and V = {ν(i)}Ns
i=1, respectively. An instrument can be
represented by a source-level representation s(i) = fθs(τ (i), ν(i)), where fθs is a deterministic function, the diamond node that
precedes xm illustrated on the left side of Fig. 1. Similarly, the set of source-level representations is denoted as S = {s(i)}Ns
i=1
and can be expressed in terms of T and V by fθs(T, V). In the following derivation of the objective function LELBO (Eq. (6)), we begin with the defined set notations, expand and
simplify the equations with the factorised form of the posteriors (Eq. (2)), and recover LELBO based on the deterministic
posterior over the pitch latent (Eq. (3)).
log p(xm|Y) ≥LELBO
(11)
= Eqϕτ (T |xm, Xq)qϕν (V|xm, Xq)

log pθm(xm|S = fθs(T, V))

(12)
−DKL
qϕτ (T |xm, Xq)∥p(T )

−DKL
qϕν(V|xm, Xq)∥pθν(V|Y)

(13)
= EQNs
i=1 qϕτ (τ (i)|xm,x(i)
q )qϕν (ν(i)|xm,x(i)
q )

log pθm(xm|S = {fθs(τ (i), ν(i))}Ns
i=1)

(14)
−
Z
Ns
Y
i=1
qϕτ (τ (i)|xm, x(i)
q ) log
QNs
i=1 qϕτ (τ (i)|xm, x(i)
q )
QNs
i=1 p(τ (i))
dτ (1)... dτ (Ns)
(15)
−
Z
Ns
Y
i=1
qϕν(ν(i)|xm, x(i)
q ) log
QNs
i=1 qϕν(ν(i)|xm, x(i)
q )
QNs
i=1 pθν(ν(i)|y(i))
dν(1)... dν(Ns)
(16)
= EQNs
i=1 qϕτ (τ (i)|xm,x(i)
q )qϕν (ν(i)|xm,x(i)
q )

log pθm(xm|S = {fθs(τ (i), ν(i))}Ns
i=1)

(17)
−
Z
Ns
Y
i=1
qϕτ (τ (i)|xm, x(i)
q )
XNs
i=1 log qϕτ (τ (i)|xm, x(i)
q )
p(τ (i))
dτ (1)... dτ (Ns)
(18)
−
Z
Ns
Y
i=1
qϕν(ν(i)|xm, x(i)
q )
XNs
i=1 log qϕν(ν(i)|xm, x(i)
q )
pθν(ν(i)|y(i))
dν(1)... dν(Ns)
(19)
= EQNs
i=1 qϕτ (τ (i)|xm,x(i)
q )qϕν (ν(i)|xm,x(i)
q )

log pθm(xm|S = {fθs(τ (i), ν(i))}Ns
i=1)

(20)
−
XNs
i=1
Z
qϕτ (τ (i)|xm, x(i)
q ) log qϕτ (τ (i)|xm, x(i)
q )
p(τ (i))
dτ (i)
(21)
−
XNs
i=1
Z
qϕν(ν(i)|xm, x(i)
q ) log qϕν(ν(i)|xm, x(i)
q )
pθν(ν(i)|y(i))
dν(i)
(22)
= EQNs
i=1 qϕτ (τ (i)|xm,x(i)
q )δ(ν(i)−fϕν (ˆy(i)
bin))

log pθm(xm|S = {fθs(τ (i), ν(i))}Ns
i=1)

(23)
−
XNs
i=1 DKL
qϕτ (τ (i)|xm, x(i)
q )∥p(τ (i))

(24)
+ H(δ(ν(i) −fϕν(ˆy(i)
bin))) +
XNs
i=1
Z
δ(ν(i) −fϕν(ˆy(i)
bin)) log pθν(ν(i)|y(i)))dν(i)
(25)
= EQNs
i=1 qϕτ (τ (i)|xm,x(i)
q )

log pθm(xm|S = {fθs(τ (i), ˆν(i))}Ns
i=1)

(26)
−
XNs
i=1 DKL
qϕτ (τ (i)|xm, x(i)
q )∥p(τ (i))

+
XNs
i=1 log pθν(ˆν(i)|y(i)).
(27)
Starting with the standard form of the evidence lower bound (ELBO), we first assume that the posteriors over T and V are
factorised in term (12), and thus the two terms of the Kullback–Leibler divergence (KLD) corresponding to T and V are written
as in term (13). In terms (14) to (16), we further assume and factorise each posterior into a product over Ns sources. Note
that the two KLD terms are expanded by the definition of KLD. Based on the configuration of a deterministic posterior over
ν(i) in Eq. (3), we rewrite qϕν(ν(i)|xm, x(i)
q ) as the Dirac delta function in terms (23) and (25). Finally, by replacing ν(i) with
ˆν(i) = fϕν(ˆy(i)
bin), we recover LELBO in Eq. (6). Input channel
Output channel
Kernel size
Stride
Padding
Normalization
Activation

Layer
ReLU

Layer
ReLU

Layer
ReLU

Layer
ReLU

Layer
ReLU

None
None
Table 4: The Conv1D layers used to implement Eϕm and Eϕq for the simple model in Section 4. Module
Input size
Output size
Normalization
Activation
Eϕν

Layer
ReLU

Layer
ReLU

Layer
ReLU

Layer
ReLU

Layer
ReLU

Layer
ReLU

None
Sigmoid
Stochastic Binarisation (SB)
fϕν

None
ReLU

None
ReLU

None
None
Table 5: The three modules of the pitch encoder for the simple model in Section 4: The transcriber Eϕν, the SB layer, and the
projector fϕν. Input
Multi-head Attention
+
Layer Norm
Feed Forward
+
Layer Norm
Output
Figure 5: A regular post-norm Transformer block. B
Implementation Details
B.1
The Simple Case Study
The mixture encoder Eϕm and the query encoder Eϕq, mentioned in Section 3.1, share an architecture which is a stack of
Conv1D layers that take as input the mel spectrograms of xm and x(i)
q
and output em, e(i)
q
∈R64, respectively. Table 4 outlines
the architecture. The encoders are followed by a mean pooling along the temporal dimension such that a mel spectrogram of
R128×10 is projected to em, e(i)
q
∈R64. The two are concatenated as a 128-dimensional vector used to extract the pitch and
timbre according to Eq. (2). By Eq. (3) and given the concatenation of em and e(i)
q, the pitch encoder qϕν first transcribes ˆy(i) ∈RNp using Eϕν: R128 →RNp, where Np = 52. ν(i) ∈R64 is then extracted by applying fϕν: RNp →R64 to ˆy(i)
bin. Table 5 shows the
complete architecture. The timbre encoder shares the same architecture as Eϕν, except for that the last layer is replaced by a
Gaussian parameterisation layer which consists of two linear layers that project the 256-dimensional hidden state to the mean
and variance of the posterior, from which the timbre latent τ (i) ∈R64 is sampled. The FiLM layer fθs obtains the source-level latent s(i) by combining the pitch and the timbre latent. In particular, the timbre
latent is linearly transformed to compute the scaling and shifting factors, and the pitch latent is modulated by the factors. To reconstruct the mel spectrograms, the source-level latent s(i) is then temporally broadcast to match the number of time
frames 10 of the mel spectrograms. A two-layer bi-directrional gated recurrent unit (GRU) then transforms the broadcast s(i)
to an output of R128×10 which is then processed by a linear layer to reconstruct the input mel spectrograms. Pitch Priors
The factorised pitch prior µfac
θν takes as input the pitch annotation y(i) and reuses fϕν for the transformation. The rest of the network shares the same architecture as the timbre encoder as it also parameterises a Gaussian pθν(ν(i)|y(i)) =
N(ν(i); µfac
θν (y(i)), σ2
νI), except for that the input size is 64. The standard deviation σν is fixed at 0.5. For the expressive variant, each element from the set of pitch annotations Y\i is also transformed by fϕν first. To handle a set

Input channel
Output channel
Kernel size
Stride
Padding
Normalization
Activation

Group(1)
ReLU

Group(1)
ReLU

Group(1)
ReLU

None
None
Table 6: The Conv1D layers used to implement the timbre encoder qϕτ for the LDM in Section 5. The last row refers to the
Gaussian layer where the 256-dimensional output is split to represent the mean and standard deviation of the posterior. The
number in the parenthesis indicates the number of groups divided for normalisation.
of inputs, we implement a transformer. The architecture consists of three blocks of a regular post-norm transformer, as shown
in Fig. 5. We use a four-head attention and an embedding size of 64. The feed-forward block is a two-layer MLP with a ReLU
and a size of 64. The elements in the set Y\i are treated as a sequence of tokens and fed to the transformer without adding positional encodings
to preserve permutation invariance. A max pooling is applied to collapse the Ns −1 tokens followed by a Gaussian parameteri-
sation to match the dimension of ν(i). The Gaussian layer consists of 2×K linear layers to parameterise the mean and standard
deviation of K components in a Gaussian mixture. Latent Linearity
We introduce Eq. (9) to avoid implementing a potentially complicated decoder, and thereby admit a linearity
between the sources and the mixture, represented by ssum = PNs
i=1 s(i) and em, respectively. This linearity could allow for
manipulating specific sources without extracting the entire set of source-level representations as follows, which we leave for
future work. Because the decoder θm would accept em in addition to {s(i)}Ns
i=1 for reconstructing xm, we can manipulate a
specific source i and sample a novel mixture by first computing a residual r = em −s(i), manipulating s(i) to get ˆs(i), and
finally using ˆ
em = r + ˆs(i) to render a novel mixture. Evaluation
The instrument and the pitch classifier share the same architecture, except for their last layers whose sizes are the
numbers of instruments 3 and the pitches 52, respectively. Both start with the architecture outlined in Table 4 followed by a
three-layer MLP. The input and output sizes of the first two layers are 64 with the ReLU activation, while that of the last layer
are 64 and the numbers of classes described above. B.2
The Latent Diffusion Model
Encoders
We extract mel spectrograms of R64×400 according to the parameters specified in Section 5.2, where the dimensions
correspond to the frequency and time axes, respectively. The mixture encoder Eϕm processes the mel spectrograms of xm and
outputs em ∈R8×100×16, with the dimensions corresponding to the channels, time frames, and feature size, respectively. We
use and freeze Evae, the pre-trained encoder of the VAE in AudioLDM2 (Liu et al. 2024) as the mixture encoder. Similarly,
we reuse the architecture of Evae for the query encoder Eϕq but train it from scratch and append a temporal pooling layer,
which outputs e(i)
q
∈R8×1×16. To combine the information of e(i)
q
and em for extracting the pitch and timbre latents according
to Eq. (2), e(i)
q
is broadcast and concatenated with em along the feature dimension. The outcome is then transformed back to
the original feature dimension of 16 by a 1 × 1 Conv2D filter before being passed for pitch and timbre extraction. The pitch encoder first transcribes with Eϕν: R8×100×16 →R129×400 whose architecture is based on the decoder Dvae from
the pre-trained VAE in AudioLDM2. We modify the output dimension from 64 to 129 to accommodate the number of pitch
values in the CocoChorale dataset (Wu et al. 2022) and train Eϕν from scratch. The output of Eϕν is then binarised by the SB
layer and passed through fϕν: R129×400 →R8×100×16 to derive the pitch latent ν(i), where fϕν is based on the architecture of
Evae and is trained from scratch. The timbre encoder qϕq: R8×100×16 →R8×1×16 converts the input which concatenates em and e(i)
q
and outputs the timbre
Input channel
Output channel
Kernel size
Stride
Padding
Normalization
Activation

Group(1)
ReLU

Group(1)
ReLU

Group(1)
ReLU

None
None
Table 7: The instrument classifier used to evaluate the disentanglement of the proposed LDM. The number in the parenthesis
indicates the number of groups divided for normalisation.

latent τ (i), a time-invariant representation that matches the dimension of e(i)
q. Its architecture is specified in Table 6 which is
followed by a temporal pooling layer. Partition
We further elaborate the partition method described in Section 5. Recall that the diffusion target zm,0 in Eq. (10)
is defined in terms of zs,0 ∈R100×(16×8) extracted from Evae, where we have transposed and flattened the extracted feature
which had the dimensions 8 × 100 × 16, corresponding to channels, time frames, and feature size, respectively. We partition
zs,0 along the time axis into L = 25 patches and flatten each patch by Par(z(i)
s ): R100×(16×8) →R25×D′
z, where D′
z =

25 × 16 × 8 = 512. By repeating the same process for all Ns sources, we obtain and define zm,0 ∈R(Ns×25)×D′
z. We can
understand it as a sequence of Ns × 25 patches with the size of each patch being D′
z = 512. The timbre latent is broadcast along the time axis and concatenated with the pitch latent to form a source-level latent s(i) ∈
R8×100×32. We follow the same process above, repeated for Ns sources, to obtain sc ∈R(Ns×25)×D′
s, where D′
s = 100
25 × 32 ×
8 = 1024. Similarly, it is a sequence of Ns × 25 patches with the size of each patch being D′
s = 1024. Decoder
The transformer pθm we implement for the LDM in Eq. (10) consists of three regular transformer blocks illustrated
in Fig. 5 and we set the number of heads to four for the multi-head self-attention mechanism. The embedding size is the same as
the input size D′
z. As described in Section 5, we replace the layer normalisation layer with its adaptive counterpart to condition
the input zm,t with sc. Evaluation
Table 7 outlines the architecture of the instrument classifier used for the evaluation of disentanglement. The last
layer is linearly projected to the logit of the 13 classes of the instruments. For the pitch classification, we employ Crepe, the
state-of-the-art monophonic pitch extractor (Kim et al. 2018b).1 We use a public repository 2 to measure the FAD.
1https://github.com/maxrmorrison/torchcrepe
2https://github.com/gudgud96/frechet-audio-distance/tree/main
