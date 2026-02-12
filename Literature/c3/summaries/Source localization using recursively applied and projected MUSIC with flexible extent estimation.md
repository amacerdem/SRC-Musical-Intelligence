# Source localization using recursively applied and projected MUSIC with flexible extent estimation

**Authors:** Lukas Hecker
**Year:** D:20
**Subject:** Hecker L, Tebartz van Elst L and Kornmeier J (2023) Source localization using recursively applied and projected MUSIC with flexible extent estimation. Front. Neurosci. 17:1170862. doi: 10.3389/fnins.2023.1170862

---

TYPE Methods
PUBLISHED 15 May 2023
DOI 10.3389/fnins.2023.1170862

## OPEN ACCESS

## EDITED BY

Fabio Baselice, University of Naples Parthenope, Italy

## REVIEWED BY

Stefano Franceschini, University of Naples Parthenope, Italy
Rachel Sparks, King’s College London, United Kingdom
*CORRESPONDENCE
Lukas Hecker
lukas_hecker@web.de
RECEIVED 21 February 2023
ACCEPTED 17 April 2023
PUBLISHED 15 May 2023
CITATION
Hecker L, Tebartz van Elst L and Kornmeier J
(2023) Source localization using recursively
applied and projected MUSIC with ﬂexible
extent estimation. Front. Neurosci. 17:1170862.
doi: 10.3389/fnins.2023.1170862
COPYRIGHT
© 2023 Hecker, Tebartz van Elst and
Kornmeier. This is an open-access article
distributed under the terms of the Creative
Commons Attribution License (CC BY). The use,
distribution or reproduction in other forums is
permitted, provided the original author(s) and
the copyright owner(s) are credited and that
the original publication in this journal is cited, in
accordance with accepted academic practice. No use, distribution or reproduction is
permitted which does not comply with these
terms. Source localization using
recursively applied and projected
MUSIC with ﬂexible extent
estimation
Lukas Hecker1,2,3,4,5*, Ludger Tebartz van Elst1,5 and
Jürgen Kornmeier1,3,4,5
1Department of Psychiatry and Psychotherapy, University of Freiburg Medical Center, Freiburg, Germany,
2Department of Psychosomatic Medicine and Psychotherapy, University of Freiburg Medical Center, Freiburg, Germany, 3Perception and Cognition Lab, Institute for Frontier Areas of Psychology and Mental
Health, Freiburg, Germany, 4Faculty of Biology, University of Freiburg, Freiburg, Germany, 5Faculty of
Medicine, University of Freiburg, Freiburg, Germany
Magneto- and electroencephalography (M/EEG) are widespread techniques to
measure neural activity in-vivo at a high temporal resolution but low spatial
resolution. Locating the neural sources underlying the M/EEG poses an inverse
problem, which is ill-posed. We developed a new method based on Recursive
Application of Multiple Signal Classiﬁcation (MUSIC). Our proposed method is able
to recover not only the locations but, in contrast to other inverse solutions, also the
extent of active brain regions ﬂexibly (FLEX-MUSIC). This is achieved by allowing it
to search not only for single dipoles but also dipole clusters of increasing extent to
ﬁnd the best ﬁt during each recursion. FLEX-MUSIC achieved the highest accuracy
for both single dipole and extended sources compared to all other methods tested. Remarkably, FLEX-MUSIC was capable to accurately estimate the level of sparsity
in the source space (r = 0.82), whereas all other approaches tested failed to do
so (r ≤0.18). The average computation time of FLEX-MUSIC was considerably
lower compared to a popular Bayesian approach and comparable to that of
another recursive MUSIC approach and eLORETA. FLEX-MUSIC produces only few
errors and was capable to reliably estimate the extent of sources. The accuracy
and low computation time of FLEX-MUSIC renders it an improved technique to
solve M/EEG inverse problems both in neuroscience research and potentially in
pre-surgery diagnostic in epilepsy. KEYWORDS
electroencephalography (EEG),
magnetoencephalography (MEG), inverse problem,
electric source imaging (ESI), Multi-Signal Classiﬁcation (MUSIC)

### 1. Introduction

In this paper, we present a novel approach for solving the inverse problem of magneto
and electroencephalography (M/EEG) using truncated recursively applied multi-signal
classiﬁcation for sources with variable coherent (FLEX-MUSIC). The EEG and MEG inverse
problem is a fundamental challenge in the ﬁeld of neuroscience, as it involves inferring
the underlying neural activity that generates a given set of EEG or MEG measurements
(Nunez and Srinivasan, 2006; He et al., 2018; Awan et al., 2019; Michel and Brunet,
2019). The problem is that many diﬀerent conﬁgurations of brain activity can cause
the same signal measured on the scalp. Traditional methods for solving this inverse
problem rely on mathematical assumptions that are often not aligned with biophysical
Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862
models of the brain. Others rely on statistical techniques
or optimization algorithms, which can be computationally
expensive and may not scale well to large datasets. Despite the
underdetermined nature of the M/EEG inverse problem, inverse
solutions help researchers and clinicians alike. M/EEG inverse
solutions help researchers gain insights into the spatio-temporal
workings of the brain during, e.g., perceptual and/ or cognitive
processing (Feige et al., 2005; Luck, 2014; Kornmeier et al., 2019). M/EEG inverse solutions allow for the identiﬁcation of functional
brain networks and is also used in neurofeedback applications
where participants learn to control brain activity in diﬀerent
frequency bands within a speciﬁed location (van Lutterveld et al.,
2017). Clinicians utilize M/EEG inverse solutions to categorize
brain abnormalities or to guide brain surgery, e.g., in drug-resistant
epileptic patients (Ebersole, 1994; Lantz et al., 1996; Aydin et al.,
2015; Willemse et al., 2016; Sharma et al., 2018). There are several existing approaches for solving the M/EEG
inverse problem (henceforth referred to as solvers), each with its
own strengths and limitations. A popular class of methods are the
minimum norm estimates (MNE, Hamalainen, 1984; Hämäläinen
and Ilmoniemi, 1994; Pascual-Marqui, 1999) that aim to ﬁnd a
solution that explains the observed EEG data with minimal energy
of the sources. While these approaches typically incorporate the L2-
norm of the source, L1-type solvers have been proposed and termed
minimum current estimates (MCE) in the domain of M/EEG
inverse problems (Beck and Teboulle, 2009). These L1-type solvers
ﬁnd sources that are sparse in nature since the imposed L1-penalty
ultimately sets most dipole values close to zero. Low-resolution tomography (LORETA) and its iterations,
standardized and exact LORETA, fall within this class of solvers
(Pascual-Marqui, 1999, 2002, 2007). While these approaches are
fast to compute and easy to interpret, these approaches often
produce blurred solutions, despite their ability to correctly localize
source maxima. Beamformers are a class of spatial ﬁltering techniques that
are commonly used to solve the M/EEG inverse problem. These methods involve constructing a set of spatial ﬁlters that
are applied to the measured signals to estimate the neural
activity at each location in the brain. Beamformers can be
eﬀective in certain scenarios but struggle to correctly localize
multiple correlated sources or spatially coherent source activity. Furthermore, minimum variance beamformers are known to
be sensitive to errors in the forward model. Robust minimum
variance beamformers have shown to mitigate the impact of
modelling errors recently (Hosseini et al., 2018). A commonly used
proponent is the linearly constrained minimum variance (LCMV)
Beamformers (Van Veen et al., 1997; Grech et al., 2008). A novelty
in the ﬁeld of Beamformers are the multiple constrained minimum
variance (MCMV) Beamformers, which alleviate the problem of
correlated sources (Nunes et al., 2020). Bayesian methods provide a framework for incorporating prior
knowledge and uncertainty into the inverse solving process (Friston
et al., 2008; Grech et al., 2008; Wipf and Nagarajan, 2009; Wipf et al.,
2010). These approaches involve constructing a probabilistic model
of the forward and inverse problems, and then apply Bayesian
inference to estimate the posterior distribution of the neural activity
given the measured M/EEG signals. Bayesian approaches, like
sparse Bayesian learning (SBL, Friston et al., 2008; Wipf and
Nagarajan, 2009), are capable to accurately localize sources under
diﬀerent sparsity assumptions. However, Bayesian optimization
can often be computationally intensive. This problem is ampliﬁed
when many dipoles are present in the source space, exacerbating
the computational load. A novel class of inverse solvers arose in the past decade that
utilize the recent advances in machine learning, predominantly
artiﬁcial neural networks (ANNs) to solve M/EEG inverse
problems. These approaches require training an ANN to produce
a source estimate based on simulated pairs of source and M/EEG
activity and achieve high accuracy compared to many conventional
methods (Cui et al., 2019; Hecker et al., 2020, 2022; Pantazis
and Adler, 2021). ANNs are prone to biases in the training data,
wherefore their application is yet limited. Multiple Signal Classiﬁcation (MUSIC, Mosher and Leahy,
1998) and recursively applied (RAP-) MUSIC (Mosher and Leahy,
1999) are popular approaches for solving the M/EEG inverse
problem. Both methods are based on the concept of subspace
estimation, which involves estimating the subspace of the neural
activity from the measured M/EEG signals using singular value
decomposition (SVD). While MUSIC calculates an inverse solution
by applying an SVD on the data covariance matrix in a single step, RAP-MUSIC extends the MUSIC method by repeatedly applying
the MUSIC algorithm to the measured M/EEG signals. At each
iteration, the estimated signal subspace is used to update the
estimate of the neural activity, and the updated estimate is then used
to update the estimate of the noise subspace. This recursive process
continues until convergence is achieved. An improvement of the
RAP-MUSIC algorithm was proposed by truncating the recursively
calculated subspace with each iteration (TRAP-MUSIC, Mäkelä
et al., 2018). This eﬀectively removes residual variance that could
not be explained in the prior iterations which leads to disturbances
in localization (“RAP dilemma”, cf. Figure 2 in Mäkelä et al., 2018). Algorithms that follow the RAP-MUSIC-scheme have in
common that a spatially coherent source patch will not be detected
reliably. Approaches to ﬁnd multiple dipoles per recursion were
proposed by Mosher and Leahy (1998) and Katyal and Schimpf
(2004), albeit with factorial increase in computational complexity. Liu and Schimpf (2006) introduced a more computationally
eﬃcient way to ﬁnd extended source clusters by applying
computing a weighted Minimum Norm Estimate (wMNE) solution
on all estimated single dipoles and their respective neighbors. This
step, however, can introduce (1) spurious sources at locations in
which a single dipole would have explained suﬃcient parts of the
signal subspace and (2) the approach is limited to ﬁnding sources of
larger extent beyond single dipoles and their ﬁrst-order neighbors. In this paper we summarize the results of our endeavor to
overcome this limitation in creating an analysis algorithm that is
capable to eﬀectively solve the inverse problem in constellations
where established methods do have limitations.

### 2. Methods

The M/EEG inverse problem refers to the process of inferring
the underlying neural activity that generates a given set of EEG
Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862
measurements. This problem is a fundamental challenge in the ﬁeld
of neuroscience, as it involves understanding the spatio-temporal
patterns of neural activity that underlie various cognitive and
behavioral processes. The EEG inverse problem is described as correctly identifying
the source matrix J ∈Rp×t that, when multiplied by the leadﬁeld
matrix L ∈Rq×p (also referred to as gain-matrix) produces the
observed EEG data matrix M ∈Rq×t with q electrodes, p dipoles
(i.e., positions in the brain) and t time points. The propagation of neural currents J through the leadﬁeld L is
thus deﬁned as: M = LJ + ζ,
(1)
where ζ is the noise in the EEG data. For simplicity, we assume
dipoles with ﬁxed orientation perpendicular to the cortical surface.
2.1. Multi-Signal Classiﬁcation (MUSIC) and
its iterations
MUSIC approaches can be interpreted as algorithms that aim
to select candidate dipoles in the brain that explain the signal of the
EEG data. This is accomplished by calculating the signal and noise
subspace of the data covariance C ∈Rq×q:

## C = MMT

UsDsUT
s = C0,
(2)
where MT denote the transpose of the EEG data matrix
M and C0 denotes the covariance matrix of the noiseless data. Us denotes the eigenvectors and Ds the eigenvalues that both
belong to the signal subspace. Signal and noise are sought to
be disentangled by selecting only the ﬁrst n eigenvalues of the
covariance matrix UDUT = C. While this selection is inherently
diﬃcult, it was recommended to overestimate n to avoid losing
parts of the signal subspace (Mosher and Leahy, 1999). We
followed a diﬀerent approach by algorithmically selecting the set
of eigenvalues belonging to the signal subspace. First, eigenvalues
were normalized to a maximum of 1 by dividing all eigenvalues by
the largest eigenvalue, yielding the normalized set of eigenvalues
˜D. We then calculate the diﬀerence from each eigenvalue to the
next eigenvalue, yielding ˜d1. Let ˜d1 be the set of eigenvalues and
ǫ = 0.01 be the relative selection criterion, which was determined
empirically during our testing phase. The smallest eigenvector ˜n
that belongs to the signal subspace is deﬁned as

## UDVT = C

d = [D1,1, D2,2,.. Dq,q]
˜di =
di
max(d)
˜d1,i = ˜di+1 −˜di, ∀i ∈{2,..., q}
˜n = i|˜di < ǫ ≤˜di−1
(3)
The estimated signal subspace is thus Us = U(1: ˜n) and the
projection to the signal space is deﬁned as Ps = UsUT
s. The MUSIC localizer is then calculated as follows:
µp =
Psl(p)

l(p)
2,
(4)
where l(p) denotes the pth column of the leadﬁeld matrix L. The
resulting localizer µ is ﬁnally ﬁltered to only contain values above a
certain criterion (typically between 0.9 to 0.99). Recursively applied MUSIC (RAP-MUSIC) also makes use
of the signal subspace and its projection by iteratively selecting
candidate dipoles as follows. We henceforth describe the RAP-
MUSIC algorithm. The ﬁrst candidate is the dipole with the largest source
amplitude in the MUSIC localizer as described above (Eq. 4). Let ˆI1 be the topography of the initially selected candidate at
iteration i we construct a set of topographies B = [ˆI1,..., ˆIi] that
stores all topographies of the selected candidates. Using the set of
topographies B ∈Rq×i at iteration i we deﬁne the out-projector
matrix Qi: Qi = I −BiB†
i,
(5)
where I ∈Rq×q denotes the identity matrix and B† denotes the
Moore-Penrose pseudo inverse of B. The updated covariance matrix Ci is then calculated by
multiplying the out-projector matrix by the signal subspace and the
new signal subspace is thusly calculated: C = QUi
C = UiDiUT
i
(6)
We then calculate the new signal subspace projection as Pi =
Ui(1: ˜n)Ui(1: ˜n)T. Note, that the number of selected components
can be truncated to Ui(1:
˜
n −k −1) to alleviate the problem of the
RAP-dilemma (Mäkelä et al., 2018). The (T)RAP-MUSIC localizer
is then calculated as follows:
µi(p) =
PiQil(p)

Qil(p)
2,
(7)
where l(p) denotes the pth column of the leadﬁeld matrix L. The
dipole at which ui is maximal is selected as the new candidate ci. The
equations 5, 6 & 7 are iterated while i < q or a stopping criterion is
met. The stopping criterion typically is met when the maximum of
the (T)RAP-MUSIC localizer ui falls below a threshold (in our case
0.975), i.e., when no dipole is able to explain the signal subspace
projection suﬃciently.

## 2.2. FLEX-MUSIC

A new dipole is selected in each iteration of the RAP-MUSIC
algorithm based on the current subspace projection P. As described
by Mäkelä et al. (2018), the selection of the most optimal dipoles
often leaves some residual of the signal subspace projection to
Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862
be explained. One reason for this is that neural sources can
often not be represented by a single dipole due to the functional
coherence in the cortex that is reﬂected by locally smooth activity
of varying extent. To overcome this limitation we extended the set
of candidate dipoles by multiple sets of smoothly distributed dipole
clusters. We have therefore calculated gradients Gk
∈
Rp×p for
increasing smoothness orders k ∈1, 2,..., 8. Each gradient Gk
transforms the original leadﬁeld matrix L to leadﬁeld matrices of
increasing smoothness orders Lk as based on the adjacency matrix
A ∈Rq×q:

## G1 = I

G2 = laplacian(A)
Gk = Gk−1A|k > 2
Lk = LGk,
(8)
where S is the largest order of smoothness and I ∈Rp×p is
the identity matrix. In summary, Eq. 8 states that we create a set
leadﬁeld matrices Gk with progressing smoothness. This is achieved
using the Laplacian of the adjacency matrix. The adjacency matrix,
also referred to as neighborhood matrix describes which dipoles in
our model are directly connected (i.e., are neighbors). The selection of the highest smoothness order k depends on the
upper boundary of smoothness to be assumed in the source model
and should be adjusted depending on the number of dipoles in
the source model. Note, that the original leadﬁeld, denoted as L1,
remains, since the respective gradient G1 is the identity matrix. We calculate the FLEX-MUSIC localizer at iteration i by
µi,k = ∥PiQiLk∥2
∥QiLk∥2,
(9)
yielding one localizer for each smoothness order k. The dipole or dipole cluster ˆp (depending on the estimated
optimal smoothness order ˆk) at which µi,k is maximal is selected
as the new candidate. We then update the set of topographies B with the newly added
topography Lˆk,ˆp. Furthermore, we update the source covariance
matrix S by adding the column vector of Gˆk,ˆp: Si = Si−1 + Gˆk,ˆp
(10)
FLEX-MUSIC iterates the equations 5, 6, 8, 9 and 10. No
truncation, as done in TRAP-MUSIC, was applied since that yielded
better results during testing. Unlike MUSIC, the recursive approaches (e.g., RAP-, TRAP-
and FLEX-MUSIC) require a ﬁnal estimation of the current source
density ˆJ ∈Rp×t after candidate selection. We use the source
covariance matrix S to calculate a weighted minimum-norm-like
solution:

## ˆJ = SLT(LSLT)−1M,

(11)
where M ∈Rq×t is the EEG or MEG data matrix. In summary, FLEX-MUSIC further alleviates the RAP-dilemma
of residual variance in the signal subspace projector P. This is
achieved by adding clusters of neighboring dipoles to the set of
candidate dipoles at each recursion step. The algorithm is still
capable to localize single dipoles since they remain part of the
set of candidates (cf. Eq. 8). This renders FLEX-MUSIC a ﬂexible
solution to the M/EEG inverse problem in which the spatial extent
of neural activations is often unknown a priori. In this way, FLEX-
MUSIC increases the probability to identify extended sources and
integrate their extensions into the result source space, instead of
either ignoring the extension or treating the neighboring dipoles as
separate sources.
2.3. Evaluation
In order to evaluate the proposed method, we simulated pairs
of source- and EEG- data using an anatomical template brain
“fsaverage” (Fischl et al., 1999) by the Freesurfer image analysis
suite1. EEG simulations were carried out using a precomputed three
shell boundary element method (BEM; Fuchs et al., 2002) forward
solution as provided by mne-python (v20.3, Gramfort et al., 2013). Each shell (brain, skull & scalp tissue) was composed of 5120
vertices. The conductivity was set to 0.3S/m2 for brain and scalp
tissue, and 0.06S/m2 for the skull. The source model was chosen with p = 1, 284 dipoles with
icosahedral spacing. For the EEG electrodes we used the Biosemi
64-channel layout consisting of q = 64 electrodes of the 10-20
system. Using the forward model and the parameters described, we
calculated a leadﬁeld L ∈Rq×p. We
evaluate
our
proposed
method
FLEX-MUSIC
by
comparing it to a diverse set of other inverse algorithms
including TRAP-MUSIC, eLORETA, a sparse Bayesian learning
(SBL) approach called Convexity Champagne and the Multiple
Constrained Minimum Variance Beamformer (MCMV, Mosher
and Leahy, 1999; Pascual-Marqui, 2007; Wipf and Nagarajan, 2009; Mäkelä et al., 2018; Nunes et al., 2020; Cai et al., 2022). Motivation is given for the choice of each method for solving
the EEG inverse problem. TRAP-MUSIC was chosen as one of the
latest developments of the recursive MUSIC approaches. eLORETA
is a popular choice in many EEG studies with theoretically low
localization errors, rendering it the most suitable choice within
the minimum-norm family. Convexity Champagne was chosen
as a very recent improvement to the Champagne algorithm. Champagne was shown to produce fast and accurate solutions
within the framework of empirical Bayes (Wipf et al., 2010). MCMV
is a similar approach as the linearly constrained minimum variance
(LCMV) beamformer. However, it is designed to be less prone to
correlations between sources, rendering it a useful innovation over
LCMV. All methods were implemented in-house and are available
in our python package invertmeeg2. Optimal regularization of eLORETA, MCMV and Convexity
Champagne was achieved using generalized cross validation (GCV, Grech et al., 2008) on a set of 7 regularization parameters

http://surfer.nmr.mgh.harvard.edu/

https://github.com/lukethehecker/invert
Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862
TABLE 1 Simulation parameters. Parameter
Settings
single
dipoles
Settings
extended
dipoles
Domain
Number of samples

–
Number of available
dipole positions
1,284
1,284
Spatial
Number of available
electrodes

Spatial
Number of simulated
dipole
[1, 10]
[1, 10]
Spatial
Neighborhood orders

[1, 3]
Spatial
Number of simulated
time points

Temporal
EEG signal-to-noise ratio
[0.1, 100]
[0.1, 100]
Temporal
Parameters and parameter ranges (denoted in square brackets) for the source and EEG
simulations of single and extended dipoles. Diameters are reported in neighborhood orders
(the higher, the larger the diameter of the cluster).
λ = {10−3..., 103}. The MUSIC-type methods (FLEX- and TRAP-
MUSIC) do not require the regularization parameters since the
noise is estimated by selecting the signal subspace. A set of 1,000 samples consisting of ground truth sources J ∈
Rp×t and corresponding EEG M ∈Rp×t was simulated in order to
evaluate the accuracy of all solvers. The number of simulated consecutive time points was set
to t = 20. The simulation parameters are outlined in Table 1. Half of all samples contained single dipoles, whereby the other
half contained samples of extended dipole clusters with coherent
activity over time. The cluster size was varied in terms of
neighborhood orders, whereas an order of 1 indicates a single
dipole and an order of 2 indicates a dipole including all its
neighbors. The source time course was generated as random
sequence of a colored frequency spectrum as described by the
P(f ) =

f beta, where beta controls the level of temporal smoothness. Noise was generated as random spatio-temporal white noise with
inter-channel correlation between -1 and 1. The noise was added
to the EEG matrix such that a random signal-to-noise ratio (SNR)
within the given range outlined in Table 1 was achieved. Only white
noise is considered since the presence of colored noise in real data
can be handled by whitening the EEG data as a preprocessing step. We calculated inverse solutions to each of the simulated
samples of EEG data using the diﬀerent methods, as described
above. Accuracy of the individual inverse solutions is quantiﬁed
by calculating the mean localization error (MLE), Earth Mover’s
Distance (EMD, Hitchcock, 1941) and the mean squared error
(MSE). Furthermore, we quantiﬁed the sparsity of each inverse
solution. We calculated the MLE by ﬁrst identifying the local maxima
of the ground truth source matrix J and the inverse solution ˆJ and
then calculating the minimum Euclidean distance between each
true dipole location and all estimated dipole locations. MSE quantiﬁes how close the estimated dipole moments (in
nAm) are to the true dipole moments and was calculated as follows:

## MSE(J, ˆJ) =

## J −ˆJ

(12)
EMD is a measure that calculates the distance between two
distributions. It is a suitable method to quantify the accuracy of
an inverse solution since, unlike MSE, it takes into account the
distance between dipole locations. It was calculated as follows:

## EMD(J, ˆJ) =

X
p

## D(J −ˆJ),

(13)
where D
∈
Rp×p is the distance matrix containing the
Euclidean distance between each dipole pair. Prior to calculating
the EMD, we have computed the absolute mean over time points
for J and ˆJ and normalized them. Sparsity was calculated by ﬁrst normalizing the columns of the
estimated source matrix ˆJ ∈Rp×t to unit length by division of
the respective columns L2-norm. The L1 norm of the normalized
matrix
ˆJ
1 was then calculated, yielding a metric with an inverse
relationship to sparsity. According to the dogma of Occam’s
Razor, which states that complexity should not be posited without
necessity, we can assume that sparse solutions make the fewest
assumptions about the brain’s activity and are therefore preferred,
given that they explain a suﬃcient amount of the data. In summary, the evaluation metrics described above capture the
accuracy of estimated local maxima positions (MLE), the accuracy
of the global pattern of the inverse solution (EMD), the accuracy of
dipole moments (MSE) and the sparsity of the solution (L1 norm).

### 3. Results

We calculated the accuracy of all inverse algorithms as
described in the previous section. Exemplary samples of ground
truth source activity and estimated sources are shown in Figure 1. Figure 2 depicts the Mean Localization Error (MLE), Earth
Mover’s Distance (EMD) and the Mean Squared Error (MSE) for
all inverse solutions of each solver. All metrics are summarized in
Table 2. Samples were divided into those containing single dipole
sources and those containing extended source clusters. FLEX-
and TRAP-MUSIC show overall lowest MLE and EMD for single
dipole sources when compared to all other solvers. Notably, the
median MLE is zero for both MUSIC-based methods, and there
was no signiﬁcant diﬀerence in MLE for single-dipole sources (p =
0.96, t = 0.36, d = 0.02). FLEX- and TRAP-MUSIC did also not
diﬀer signiﬁcantly in EMD (p = 0.95, t = 0.73, d = 0.05) and
MSE (p = 1.00, t = 0.31, d = 0.02). Champagne produced the
next best accuracies, eLORETA and the MCMV Beamformer show
comparatively poor accuracy in correctly estimating the source
distribution as depicted in relatively high EMD and MSE, whereas
the Convexity Champagne solver lies in-between. The advantage of the proposed FLEX-MUSIC solver becomes
most apparent for extended sources. While TRAP-MUSIC fails
to accurately localize sources with spatial extent, FLEX-MUSIC
retains the lowest MLE and EMD compared to all other solvers
(Figure 2). Figure 3 shows the sparsity of the produced inverse solutions
of all solvers, deﬁned as the L1-norm of the L2-normalized source
Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862

## FIGURE 1

Examples of ground truth and estimated sources. Exemplary plots of ground truth sources and the estimated sources of FLEX-MUSIC and
comparative approaches. For demonstration purposes, samples were selected based on visibility on the right lateral view. (First Row) Single
non-extended source. (Seconds Row) Multiple non-extended sources. (Third Row) Single extended source. (Fourth row) Multiple extended sources. Colorbars were adjusted for eLORETA and MCMV to improve visibility of the source pattern. FLEX-MUSIC visibly recovers the actual source extent
whereas all other approaches tested show biases toward single dipoles or extended dipoles.

## FIGURE 2

Evaluation of all solvers. Boxplots depict the accuracy of FLEX-MUSIC and all other solvers tested. (Left) Mean Localization Error in mm. (Center)
Earth Mover’s Distance (EMD), (Right) Mean Squared Error. Blue: Single dipoles. Orange: Extended dipoles. Note, that FLEX-MUSIC achieves
competitive accuracy for single-dipole sources and the highest accuracy for samples containing spatially extended sources.
estimate ˆJ. We ﬁnd that FLEX- and TRAP-MUSIC exhibit the
highest sparsity, MCMV and eLORETA the lowest, and Convexity
Champagne lies in the middle. Interestingly, only FLEX-MUSIC
shows a clear diﬀerence in sparsity between samples containing
single dipoles and those containing extended dipole clusters,
which is consequence of its ﬂexibility to estimate sources of
varying extent. This aspect is shown in detail in Figure 4, depicting each solver’s
capability to recover the spatial level of sparsity in the ground
truth. FLEX-MUSIC shows the highest correlation (r = 0.82)
between the sparsity in the ground truth sources and the sparsity
in the predicted sources. TRAP-MUSIC shows a high correlation
for highly sparse samples and is biased for less sparse samples. Convexity Champagne produced solutions that were often less
sparse that the ground truth, whereas MCMV and eLORETA had
a strong bias toward ﬁnding less sparse activations. Despite the
strong bias, the sparsity of eLORETA was signiﬁcantly correlated
with the sparsity in the ground truth samples. Next, we tested the dependence of the inverse solution accuracy
on varying levels of noise. For this comparison we have combined
samples containing single dipoles and those containing extended
dipole clusters (Figure 5). The graph shows that FLEX-MUSIC
yields inverses solutions with the highest accuracy regardless of the
level of noise in the EEG data. Finally, we analyzed the accuracy of all solvers depending
on a varying number of dipoles/ dipole clusters in the ground
truth (Figure 6). FLEX-MUSIC achieves again the highest accuracy
on all metrics regardless of how many dipoles/ dipole clusters
Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862
were present in the ground truth source. Similar to Champagne, FLEX-MUSIC showed remarkably low MSE when multiple sources
were active simultaneously.

## FIGURE 3

Sparsity of inverse solutions. Boxplot depicts the L1 norm for all
inverse solvers tested. The L1 norm reﬂects the level of
“non-sparsity”.
3.1. Computational expense
The computational expense to calculate the EEG inverse
operators is presented in Figure 7 (right). The framework
for these calculations was the invertmeeg library which was
developed in-house in python (https://github.com/lukethehecker/
invert). Although FLEX-MUSIC has some additional processing
steps compared to TRAP-MUSIC, we ﬁnd that the median
computation time diﬀers only slightly (1t
=
0.042s, p
=
1.72 · 10−6, t
= 5.25, d = 0.23). eLORETA required similar
computation times of 0.32s. Convexity Champagne required the
longest computation time of 2.66s. Note, that eLORETA, Convexity
Champagne and MCMV were re-computed 7 times for varying
levels of regularization. If the optimal regularization parameter
was known in advance, the computation time could be reduced
seven-fold.

### 4. Discussion

In this work we have presented FLEX-MUSIC, a new
approach to solve the M/EEG inverse problem embedded in the
recursive MUSIC scheme. Similar to the well-known RAP-MUSIC
techniques, it iteratively adds candidate positions to the set of active
sources. In addition to the RAP-MUSIC approaches it adds an
extended dictionary of increasingly smooth source patches. We have shown that FLEX-MUSIC works as well as TRAP-
MUSIC in scenarios where the EEG was produced by singular
dipole sources. Furthermore, we have shown that FLEX-MUSIC

## FIGURE 4

Accuracy in extent estimation. Scatter plots depict the relationship between the L1 norm in the ground truth and the L1 norm in the prediction. The
L1 norm reﬂects the level of “non-sparsity.” Note, that only FLEX-MUSIC is capable to reproduce the true sparsity with high correlation (r = 0.82).
***p < 0.001. Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862

## FIGURE 5

Dependence on SNR. Accuracy of all solvers separated by the signal-to-noise ratio (SNR) in the simulated EEG samples. (Left) Mean localization Error
for diﬀerent levels of noise in the EEG data. (Center) Earth Mover’s Distance for diﬀerent levels of noise in the EEG data. (Right) Mean Squared Error
for diﬀerent levels of noise in the EEG data. Note that the advantage of FLEX-MUSIC over other solvers persists for varying levels of noise. TABLE 2 Medians of all metrics. Method
MLE [mm]
EMD
Mean squared error
Sparsity
Time [s]
FLEX-MUSIC
2.11
66,291.31
4.15e-07
2.36
0.35
TRAP-MUSIC
5.50
125,233.79
5.37e-07
1.73
0.32
Champagne
7.73
123,775.42
4.67e-07
6.29
2.66
eLOR
19.05
185,186.10
8.16e-07
28.29
0.32
MCMV
16.25
184,793.86
9.65e-07
30.04
1.82
Table depicts the median performance of each solver in each metric considered. Both single-dipole and extended-dipole samples were included in this analysis. Best performance per metric is
highlighted in bold font. MLE: Mean localization error. EMD: Earth Mover’s Distance. Sparsity: Sparsity of the produced inverse solutions. Time: Computation time of the inverse operator.

## FIGURE 6

Dependence on number of active sources. Accuracy of all solvers for varying numbers of active sources within the simulated EEG samples. Error bars
depict standard errors of the mean (SEM).
accurately estimates the spatial extent of the underlying sources. Strikingly, of all inverse solvers tested, only FLEX-MUSIC was
capable of estimating the level of sparsity in the ground truth,
showing the highest correlation between the sparsity levels in the
ground truth sources and the estimated sources or r = 0.82,
whereas the next best solver achieved only a correlation of r = 0.18. We consider this aspect to be the most compelling argument for
FLEX-MUSIC, since the correct estimation of the extent of neural
generators underlying an M/EEG signal is of high interest for
multiple reasons. First, as stated above, RAP-MUSIC approaches suﬀer in general
from what is called the RAP dilemma, i.e., the interference of
residual variance from previous iterations. Since FLEX-MUSIC
is capable to explain a larger portion of the subspace, it
eﬀectively diminishes the residual variance from the previous
iterations, leading to more accurate inverse solutions throughout
all iterations. Second, good estimations of the extent of neural sources is of
high interest in the pre-surgical diagnostic in epilepsy. Not only
does FLEX-MUSIC more reliably ﬁnd the true location of the
Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862

## FIGURE 7

Time of computation. Boxplot depicts the computation time in
seconds for all inverse solvers tested. Convexity Champagne
requires ten times longer computation time compared to
FLEX-MUSIC.
source maxima regardless of their extent (cf. Figure 2), it is also
capable to isolate the prospective resection area in the brain. As stated earlier, the recursive MUSIC approaches are a suitable
option to solve inverse problems where the solution space is
considerably large due to their low computation time and built-
in regularization. While the presented Convexity Champagne has
shown competitive accuracy in many cases, we showed that the
computational expense was almost 10 times higher in our setting. We further argue that the diﬀerence in computational expense may
further increase with larger source models (i.e., higher number of
dipoles), rendering the computation of Bayesian inverse solutions
unfeasible ﬁr certain clinical applications. The simulations presented in this work contained spherical
sources, similar as to what FLEX-MUSIC is able to model by
progressively smoothing the leadﬁeld. This may have led to
optimistic results, and it is expected that deviant source shapes
(e.g., elliptical) could cause FLEX-MUSIC to perform worse. However, we have made eﬀorts to simulate a broad set of neural
activity with up to 10 simultaneously active sources. Diverse spatial
patterns of neural activity form when many spherical sources are
combined, e.g., through overlap. FLEX-MUSIC performed well
even under these conditions, as was shown in Figure 6, which
indicates robustness of the algorithm. A potential weakness of our proposed FLEX-MUSIC algorithm
is that mesoscale brain activity may not be suﬃciently modelled
with single dipoles and smooth dipole clusters. Various shapes,
e.g., elliptical coherent sources, may be involved in real-world
M/EEG recordings of brain activity. However, we expect that for
a suﬃciently large source model, FLEX-MUSIC should still be able
to reconstruct deviant shapes of sources using the circular smooth
patches. Future improvements of the FLEX-MUSIC algorithm
could involve changing the way the dictionary of candidate dipoles
or dipole clusters is applied. One potentially fruitful modiﬁcation
may be to ﬁnd the set of active dipoles that explain the signal
subspace in each iteration is found in a data-driven manner,
unlike the dictionary-like search that we proposed in the present
work. Another idea would be a combination of SBL and FLEX-
MUSIC, in which a small set of active dipoles are added to the
source covariance matrix (cf. Eq. 10) based on the maximum a
posteriori (MAP) estimation. An interesting development of the
recursive MUSIC algorithms was presented recently by Adler et al.
(2022), called Alternating Projections (AP). The approach yielded
lower MLE compared to RAP- and TRAP-MUSIC, especially under
low SNR conditions. It may be promising to translate the idea
of FLEX-MUSIC to the domain of AP, which could potentially
further increase the accuracy of the AP-approach in scenarios
where spatially coherent sources are expected. A very important ﬁnding of the present work, beyond the
performance beneﬁts of FLEX-MUSIC, is that diﬀerent inverse
solutions applied to the same data set can produce quite divergent
results. In the case of real EEG data, where a ground truth is not
available, we strongly recommend to use diﬀerent methods for EEG
source calculations in parallel and compare the results with each
other. As we have shown in this work, combining FLEX-MUSIC
and a Champagne algorithm may be useful, although Champagne
may overestimate the size of neural sources in some cases. Data availability statement
Publicly available datasets were analyzed in this study. This
data can be found here: https://github.com/LukeTheHecker/ﬂex_
paper_analyses. Author contributions
LH is the author of the idea and implemented the inverse
solution and wrote the initial manuscript. LH, JK, and LT designed
the evaluation procedure. All authors reviewed the manuscript. All authors contributed to the article and approved the submitted
version. Funding
The project was funded by the European Campus (Eucor)
seeding money. Acknowledgments
We acknowledge support by the Open Access Publication Fund
of the University of Freiburg. Conﬂict of interest
The authors declare that the research was conducted in the
absence of any commercial or ﬁnancial relationships that could be
construed as a potential conﬂict of interest. Frontiers in Neuroscience

frontiersin.org

Hecker et al.
10.3389/fnins.2023.1170862
Publisher’s note
All claims expressed in this article are solely those of the
authors and do not necessarily represent those of their aﬃliated
organizations, or those of the publisher, the editors and the
reviewers. Any product that may be evaluated in this article, or
claim that may be made by its manufacturer, is not guaranteed or
endorsed by the publisher. References
Adler, A., Wax, M., and Pantazis, D. (2022). “Brain source localization by alternating
projection,” in 2022 IEEE 19th International Symposium on Biomedical Imaging (ISBI)
(IEEE), 1–5. doi: 10.1109/ISBI52829.2022.9761604
Awan, F. G., Saleem, O., and Kiran, A. (2019). Recent trends and advances in solving
the inverse problem for EEG source localization. Inverse Probl. Sci. Eng. 27, 1521–1536.
doi: 10.1080/17415977.2018.1490279
Aydin, Ü., Vorwerk, J., Dümpelmann, M., Küpper, P., Kugel, H., Heers, M.,
et al. (2015). Combined EEG/MEG can outperform single modality EEG or MEG
source reconstruction in presurgical epilepsy diagnosis. PLoS ONE 10, e0118753.
doi: 10.1371/journal.pone.0118753
Beck, A., and Teboulle, M. (2009). A fast iterative shrinkage-thresholding algorithm
for linear inverse problems. SIAM J. Imaging Sci. 2, 183–202. doi: 10.1137/080716542
Cai, C., Kang, H., Hashemi, A., Chen, D., Diwakar, M., Haufe, S., et al. (2022). Bayesian algorithms for joint estimation of brain activity and noise in electromagnetic
imaging. IEEE Trans. Med. Imaging. 42, 762–773. doi: 10.1109/TMI.2022.3218074
Cui, S., Duan, L., Gong, B., Qiao, Y., Xu, F., Chen, J., et al. (2019). EEG source
localization using spatio-temporal neural network. China Commun. 16, 131–143.
doi: 10.23919/JCC.2019.07.011
Ebersole, J. S.
(1994). Non-invasive
localization
of
the
epileptogenic
focus
by
EEG
dipole
modeling. Acta
Neurol. Scand.
89,
20–28.
doi: 10.1111/j.1600-0404.1994.tb05179.x
Feige, B., Scheﬄer, K., Esposito, F., Di Salle, F., Hennig, J., and Seifritz, E.
(2005). Cortical and subcortical correlates of electroencephalographic alpha rhythm
modulation. J. Neurophysiol. 93, 2864–2872. doi: 10.1152/jn.00721.2004
Fischl, B., Sereno, M. I., Tootell, R. B., and Dale, A. M. (1999). High-resolution
intersubject averaging and a coordinate system for the cortical surface. Hum. Brain
Mapp. 8, 272–284. doi: 10.1002/(SICI)1097-0193(1999)8:4&lt;272:: AID-HBM10&gt;3.
0. CO;2-4
Friston, K., Harrison, L., Daunizeau, J., Kiebel, S., Phillips, C., Trujillo-Barreto, N.,
et al. (2008). Multiple sparse priors for the M/EEG inverse problem. Neuroimage 39,
1104–1120. doi: 10.1016/j.neuroimage.2007.09.048
Fuchs, M., Kastner, J., Wagner, M., Hawes, S., and Ebersole, J. S. (2002). A
standardized boundary element method volume conductor model. Clin. Neurophysiol.
113, 702–712. doi: 10.1016/S1388-2457(02)00030-5
Gramfort, A., Luessi, M., Larson, E., Engemann, D. A., Strohmeier, D., Brodbeck, C., et al. (2013). MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7,
267. doi: 10.3389/fnins.2013.00267
Grech, R., Cassar, T., Muscat, J., Camilleri, K. P., Fabri, S. G., Zervakis, M., et al.
(2008). Review on solving the inverse problem in EEG source analysis. J. Neuroeng. Rehabil. 5, 25. doi: 10.1186/1743-0003-5-25
Hamalainen, M. (1984). Interpreting Measured Magnetic Fields of the Brain: Estimates of Current Distributions. Univ. Helsinki, Finland Tech. Rep. TKK-F-A559. Hämäläinen, M. S., and Ilmoniemi, R. J. (1994). Interpreting magnetic ﬁelds
of the brain: minimum norm estimates. Med. Biol. Eng. Comput. 32, 35–42.
doi: 10.1007/BF02512476
He, B., Sohrabpour, A., Brown, E., and Liu, Z. (2018). Electrophysiological source
imaging: a noninvasive window to brain dynamics. Ann. Rev. Biomed. Eng. 20,
171–196. doi: 10.1146/annurev-bioeng-062117-120853
Hecker, L., Rupprecht, R., van Elst, L. T., and Kornmeier, J. (2020). ConvDip:
a convolutional neural network for better M/EEG Source Imaging. bioRxiv.
doi: 10.1101/2020.04.09.033506
Hecker, L., Rupprecht, R., van Elst, L. T., and Kornmeier, J. (2022). Long-short
term memory networks for electric source imaging with distributed dipole models. Neuroscience. bioRxiv. doi: 10.1101/2022.04.13.488148
Hitchcock, F. L. (1941). The distribution of a product from several sources to
numerous localities. J. Math. Phys. 20, 224–230. doi: 10.1002/sapm1941201224
Hosseini, S. A. H., Sohrabpour, A., Akçakaya, M.,
and
He, B.
(2018). Electromagnetic
brain
source
imaging
by
means
of
a
robust
minimum
variance
beamformer. IEEE
Trans. Biomed. Eng.
65,
2365–2374.
doi: 10.1109/TBME.2018.2859204
Katyal, B., and Schimpf, P. H. (2004). “Multiple current dipole estimation in a
realistic head model using R-MUSIC,” in The 26th Annual International Conference
of the IEEE Engineering in Medicine and Biology Society, vol. 1 (IEEE), 829–832.
doi: 10.1109/IEMBS.2004.1403286
Kornmeier, J., Friedel, E., Hecker, L., Schmidt, S., and Wittmann, M. (2019). What
happens in the brain of meditators when perception changes but not the stimulus? PLoS
ONE 14, e0223843. doi: 10.1371/journal.pone.0223843
Lantz, G., Holub, M., Ryding, E.,
and
Rosén, I.
(1996). Simultaneous
intracranial
and
extracranial
recording
of
interictal
epileptiform
activity
in
patients with drug resistant partial epilepsy: patterns of conduction and results
from dipole reconstructions. Electroencephalogr. Clin. Neurophysiol. 99, 69–78.
doi: 10.1016/0921-884X(96)95686-6
Liu, H., and Schimpf, P. H. (2006). Eﬃcient localization of synchronous EEG
source activities using a modiﬁed RAP-MUSIC algorithm. IEEE Trans. Biomed. Eng.
53, 652–661. doi: 10.1109/TBME.2006.870236
Luck, S. J. (2014). An Introduction to the Event-Related Potential Technique. MIT
Press. Mäkelä, N., Stenroos, M., Sarvas, J., and Ilmoniemi, R. J. (2018). Truncated rap-
music (trap-music) for MEG and EEG source localization. Neuroimage 167, 73–83.
doi: 10.1016/j.neuroimage.2017.11.013
Michel, C. M., and Brunet, D. (2019). EEG Source imaging: a practical review of the
analysis steps. Front. Neurol. 10, 325. doi: 10.3389/fneur.2019.00325
Mosher, J. C., and Leahy, R. M. (1998). Recursive MUSIC: a framework for
EEG and MEG source localization. IEEE Trans. Biomed. Eng. 45, 1342–1354.
doi: 10.1109/10.725331
Mosher, J. C., and Leahy, R. M. (1999). Source localization using recursively
applied and projected (RAP) MUSIC. IEEE Trans. Signal Process. 47, 332–340.
doi: 10.1109/78.740118
Nunes, A. S., Moiseev, A., Kozhemiako, N., Cheung, T., Ribary, U., and
Doesburg, S. M. (2020). Multiple constrained minimum variance beamformer
(MCMV)
performance
in
connectivity
analyses. Neuroimage
208,
116386.
doi: 10.1016/j.neuroimage.2019.116386
Nunez, P. L.,
and
Srinivasan, R.
(2006). Electric
Fields
of
the
Brain: The
Neurophysics
of
EEG. Oxford
University
Press, USA.
doi: 10.1093/acprof:oso/9780195050387.001.0001
Pantazis, D., and Adler, A. (2021). MEG source localization via deep learning. Sensors 21, 4278. doi: 10.3390/s21134278
Pascual-Marqui, R. D. (1999). Review of methods for solving the EEG inverse
problem. Int. J. Bioelectromagn. 1, 75–86. Pascual-Marqui, R. D. (2002). Standardized low-resolution brain electromagnetic
tomography (sLORETA): technical details. Methods Find Exp. Clin. Pharmacol. 24,
5–12. Pascual-Marqui, R. D. (2007). Discrete, 3D distributed, linear imaging methods
of electric neuronal activity. Part 1: exact, zero error localization. arXiv preprint
arXiv:0710.3341. Sharma, P., Scherg, M., Pinborg, L. H., Fabricius, M., Rubboli, G., Pedersen, B., et al. (2018). Ictal and interictal electric source imaging in pre-surgical
evaluation: a prospective study. Eur. J. Neurol. 25, 1154–1160. doi: 10.1111/ene.

van Lutterveld, R., Houlihan, S. D., Pal, P., Sacchet, M. D., McFarlane-Blake, C., Patel, P. R., et al. (2017). Source-space EEG neurofeedback links subjective experience
with brain activity during eﬀortless awareness meditation. Neuroimage 151, 117–127.
doi: 10.1016/j.neuroimage.2016.02.047
Van Veen, B. D., van Drongelen, W., Yuchtman, M., and Suzuki, A.
(1997). Localization of brain electrical activity via linearly constrained minimum
variance spatial ﬁltering. IEEE Trans. Biomed. Eng. 44, 867–880. doi: 10.1109/10. Willemse, R. B., Hillebrand, A., Ronner, H. E., Peter Vandertop, W., and Stam, C. J. (2016). Magnetoencephalographic study of hand and foot sensorimotor organization
in 325 consecutive patients evaluated for tumor or epilepsy surgery. Neuroimage Clin.
10, 46–53. doi: 10.1016/j.nicl.2015.11.002
Wipf, D., and Nagarajan, S. (2009). A uniﬁed Bayesian framework for
MEG/EEG source imaging. Neuroimage 44, 947–966. doi: 10.1016/j.neuroimage.2008.
02.059
Wipf, D. P., Owen, J. P., Attias, H. T., Sekihara, K., and Nagarajan, S. S. (2010). Robust Bayesian estimation of the location, orientation, and time
course of multiple correlated neural sources using MEG. Neuroimage 49, 641–655.
doi: 10.1016/j.neuroimage.2009.06.083
Frontiers in Neuroscience

frontiersin.org
