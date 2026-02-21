# motor-rhythm-arxiv

IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 1
Unsupervised Domain Adaptation for Image
Classiﬁcation via Structure-Conditioned
Adversarial Learning
Hui Wang, Jian Tian, Songyuan Li, Hanbin Zhao, Qi Tian, Fei Wu, and Xi Li
Abstract—Unsupervised domain adaptation (UDA) typically carries out knowledge transfer from a label-rich source domain to an
unlabeled target domain by adversarial learning. In principle, existing UDA approaches mainly focus on the global distribution
alignment between domains while ignoring the intrinsic local distribution properties. Motivated by this observation, we propose an
end-to-end structure-conditioned adversarial learning scheme (SCAL) that is able to preserve the intra-class compactness during
domain distribution alignment. By using local structures as structure-aware conditions, the proposed scheme is implemented in a
structure-conditioned adversarial learning pipeline. The above learning procedure is iteratively performed by alternating between local
structures establishment and structure-conditioned adversarial learning. Experimental results demonstrate the effectiveness of the
proposed scheme in UDA scenarios.
Index Terms—Unsupervised Domain Adaptation, Image Classiﬁcation, Adversarial Learning, Clustering.
!
1 I NTRODUCTION
R
ECENT years have witnessed a great development of
unsupervised domain adaptation (UDA), which aims
to transfer the knowledge of a label-rich source domain to
an unlabeled target domain (with the same class information
as the source domain). However, as shown in Fig. 1, the
features of the source domain and the target domain are
often distributed on different manifolds, which poses the
problem of adapting a well-trained model from the source
domain to the target domain [1], [2], [3].
In the literature, a typical solution to UDA is based
on adversarial domain adaptation [4], [5], [6], [7], which
seeks to bridge the domain gap across domains by playing
an adversarial game between two players, i.e., a feature
extractor and a domain classiﬁer. The feature extractor con-
trives to fool the domain classiﬁer. Conversely, the domain
classiﬁer strives to determine whether the extracted features
belong to the source or target domain. As a result, such
a domain alignment scheme globally narrows down the
feature distribution gap between domains, without locally
modeling the intra-class compactness of the target domain.
Therefore, these methods are likely to have some difﬁculties
in well capturing the consistency of the local structures for
the target domain features, as illustrated in Fig. 1.
Motivated by the above observations, we propose to
learn the local structures of the target domain and inte-
grate the structures into an adversarial learning process,
resulting in a framework called structure-conditioned ad-
• H. Wang, J. Tian, S. Li, H. Zhao, F. Wu, and X. Li are with College
of Computer Science and Technology, Zhejiang University, Hangzhou
310027, China.
E-mail: {wanghui 17, tianjian29, leizungjyun, zhaohanbin, wufei,
xilizju}@zju.edu.cn.
• Q. Tian is with Cloud BU, Huawei Technologies, Shenzhen 518129,
China.
E-mail: tian.qi1@huawei.com.
(Corresponding author: Xi Li.)
The domain shift G 
Target samples 
Source samples 
Before adaptation 
Previous adversarial methods 
Reduce shift, but lose compactness 
Our method 
Reduces shift, and preserves compactness 
Labeled source feature Unlabeled target feature 
Fig. 1. (Best viewed in color.) Comparison of different UDA methods. The
G denotes the feature extractor and the shape of each feature refers
to its afﬁliated class. Top: Before adaptation, the source domain fea-
tures and the target domain features belong to two different manifolds.
Bottom-left: Previous adversarial method tries to reduce the domain
shift but fails to keep the local structures of the target domain. Bottom-
right: Our method manages to preserve the target local structures and
reduce the domain shift as well.
versarial learning (SCAL). The key to SCAL lies in the
novel clustering-based conditions which contain the lo-
cal structures of target domain features. Based on such
conditions, the adversarial process of SCAL is trained to
align conditional distributions to preserve the compactness
of the target local structures. However, due to the non-
arXiv:2103.02808v1  [cs.CV]  4 Mar 2021
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 2
differentiable property of the clustering procedure, it is hard
to adapt the obtained local structures to the changing feature
distribution in the training process. To greatly facilitate the
learning process, we use a differentiable neural network as
a surrogate for the clustering condition learner, leading to a
differentiable end-to-end learning pipeline.
The main contributions of this work are summarized as
follows. 1) We formulate unsupervised domain adaptation
from the perspective of intrinsic local structure establish-
ment by the clustering algorithm, which seeks to improve
the class-structure-aware capability of domain adaptation.
2) We propose a structure-conditioned adversarial learning
scheme (SCAL), which incorporates the clustering structure
information into the adversarial learning process structure-
aware conditions. Besides, we use a differentiable neural
network as a surrogate for a clustering learner to ensure
the learning process to be end-to-end. 3) Experiments over
several benchmark datasets demonstrate that the proposed
scheme achieves signiﬁcant performance gains in most
cases.
2 R ELATED WORK
Recently, there has been many works [8], [9], [10], [11],
[12] on unsupervised domain adaptation (UDA) with deep
models. The most relevant mainstream strategies of them to
our research are adversarial methods and pseudo-labeling-
aided methods, respectively. In the following, we discuss
those relevant UDA methods in detail.
2.1 Adversarial Domain Adaptation
In UDA, a typical line of research is based on adversarial
methods. Inspired by the success of generative adversarial
networks [13], Ganin et al. [4], [5] introduce the adversarial
methods to align features of different domains. They utilize
a domain classiﬁer (discriminator) to predict the domain
labels, and a feature generator to generate an aligned dis-
tribution between domains to confuse the domain classi-
ﬁer. Therefore, the feature distribution discrepancy between
different domains would be minimized. Following such a
framework, Tzeng et al. [7] propose the adversarial dis-
criminative domain adaptation (ADDA) to utilize a shared
domain classiﬁer to align the outputs of two indepen-
dent domain feature generators. SimNet [14] introduces a
similarity-based classiﬁer and an adversarial loss to enhance
the adaptation performance. Zhang et al. [15] use multiple
domain classiﬁers for collaborative adversarial learning.
Without the classic domain classiﬁer, Saito et al. [16] and
followers [17], [18] propose to utilize the adversarial process
of two task classiﬁers to align domain distributions.
Besides aligning marginal distribution, several meth-
ods also align conditional or joint distributions. Based on
DANN [5], Long et al. [6] consider conditioning the domain
classiﬁer on the category classiﬁer and propose Conditional
Domain Adversarial Network (CDAN). They aim to capture
the cross-covariance between feature representations and
classiﬁer predictions. pseudo-labeled target sample Cicek
and Soatto [19] also aim to align the joint distribution
over domain and label by a joint predictor and classiﬁer’s
prediction. Deng et al. [20] and Xie et al. [21] try to combine
the class center alignment (based on the source classiﬁer pre-
dictions) with the marginal distribution alignment to match
the center-based marginal distributions between domains.
However, most of the adversarial UDA methods glob-
ally narrow down the domain shift across domains and
cannot effectively preserve the intra-class compactness of
the target domain. Although some researchers discover the
phenomenon, they [21] simply utilize the predictions of the
source classiﬁer to model the conditional distribution of
the target domain features, which would suffer the domain
shift problem. Different from theirs, based on a structure-
conditioned adversarial learning scheme, we can model the
target domain structure by its intrinsic characteristics and
then preserve its compactness.
2.2 Pseudo-labeling-aided Domain Adaptation
Pseudo-labeling-aided methods have also gained great at-
tention recently. In this kind of method, the researchers iter-
atively assign a pseudo-label to each unlabeled target data
and use the pseudo-labeled target samples together with the
source samples to learn an improved classiﬁcation model.
The obtained pseudo-labels are expected to be progressively
more accurate when the model is optimized. For example,
Long et al. [22], [23], [24] propose to obtain the pseudo-labels
of target data by a classiﬁer trained on the source samples.
Sener et al. [25] utilize KNN to obtain the pseudo-labels of
target data. Pei et al. [26] assign the conditional probability
of each class to each target sample, which results in a soft
label.
Unfortunately, the performance of pseudo-labeling-
aided methods relies heavily on the accuracy of the pseudo-
labeling. Due to such a limitation, these methods may
perform poorly when data distributions embody complex
multimodal structures or need to rely on the complex noise
reduction methods [27], [28], [29] (e.g. sample selection). As
a result, Chen et al. [30] introduce easy-to-hard sample se-
lection method. Wang et al. [29] utilize a class-wise selection
of two pseudo-labeling methods. Kang et al. [27] introduce a
Contrastive Adaptation Network (CAN), which only selects
the categories with sufﬁcient samples for training.
In this paper, we are interested in employing the pseudo-
labeling method to assist adversarial unsupervised domain
adaptation. We propose a SCAL model to take the pseudo-
labels of target domain features as conditions, thus preserv-
ing the dense clustered feature spaces in the adversarial
process. Due to the statistics-based adversarial loss, our
method is not sensitive to noise caused by clustering. We
would discuss this in Section 4.4.
2.3 Metric Learning for Domain Adaptation
A growing number of researchers propose to reduce domain
shift by metric learning. The general assumption of such
methods is that the domain shift across domains can be
measured by some distance metrics. After that, the domain
shift reduction can be approximated as the optimization of
the metric-based loss. For instance, some researchers [10],
[32], [33] utilize maximum mean discrepancy as a measure
of the shift between the two domains. Sun et al. [34] and
Li et al. [35] try to minimize the F-norm of covariance
between different domains. Sun et al. [36] introduce a
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 3
A->W
(a) Before Adaptation
 (b) Adversarial method
 (c) Our Method
Fig. 2. Real feature visualization of different methods from the source domain A to the target domain W (i.e., A→W) on Ofﬁce-31 [31] with 10
classes (◦:A;×:W). Here, the color of each point denotes its class, and the local structures of the features refer to the clusters of the features.
method to match the mean and covariance across domains.
Li et al. [37] propose a maximum density divergence which
aims to jointly minimizes the inter-domain divergence and
maximizes the intra-domain density, while Luo et al. [38]
adopt the afﬁne Grassmann distance and the Log-Euclidean
metric in unsupervised domain adaptation.
Apart from the above metrics, optimal transport [39] at-
tracts much attention in recent years. Shen et al. [40] utilizes
Wasserstein distance as the metric loss in promoting similar-
ities between the features of different domains. Damodaran
et al. [39] propose to transport the source samples to the
target domain by an estimated mapping. Li et al. [41] intro-
duce an enhanced optimal transport framework for domain
adaptation. These optimal transport-based methods focus
on global matching between source and target distributions,
while we aim to model the local structures of target features
by clustering.
3 P ROPOSED METHOD
In this section, we illustrate our framework, called structure-
conditioned adversarial learning (SCAL), in detail. First, we
formulate the problem of SCAL in Section 3.1. Second, we
elaborate on how to form the structure-conditioned adver-
sarial loss of SCAL in Section 3.2. Third, we describe the two
main components (i.e., local structure establishment and
surrogate classiﬁer approximation) of SCAL in Section 3.3.
Finally, we make a theoretical analysis of SCAL based on
domain adaptation theory [1] in Section 3.4.
3.1 Problem Formulation
Given a labeled source domain Ds and an unlabeled target
domainDt, our goal is to train a network using Ds andDt
to make predictions on Dt. Note that Ds andDt have the
sameK-label space{1, 2,...,K }, and the data of them are
drawn from different distributions, which leads to a domain
shift [1], [2], [3].
Our motivation is to reduce the domain shift and pre-
serve the local structures of the target domain simultane-
ously. For better illustration, we take Fig. 2 as an example.
As shown in Fig. 2, on task A→W, it is notable that the
variance of the target local structures increases after the
adversarial domain adaptation [5] (the × of Fig. 2(a) vs.
the× of Fig. 2(b)), which makes the classiﬁer difﬁcult to
perform the classiﬁcation of target domain data. As a result,
we propose SCAL, which aims to preserve the target local
structures, i.e., the clusters of the target features, to improve
the discriminability of the adapted target features.
Concretely, SCAL consists of a feature extractor G, a
source classiﬁer F , a surrogate classiﬁer FS, and a domain
classiﬁerD. And the training process of SCAL is a minimax
game:
min
G,F
max
D
Lcls−λLscal, (1)
whereLcls denotes the classiﬁcation loss andLscal denotes
the structured-conditioned adversarial loss.Lcls is the cross-
entropy lossLce in source domain with ground-truth labels:
Lcls = E(x,y)∼Ds [Lce(F (G(x)),y )]. (2)
3.2 Structure-Conditioned Adversarial Loss
The idea behind SCAL is to preserve the local structures
between domains in the global alignment process of adver-
sarial learning. With this motivation, we propose to extract
the structure-conditioned features of target domain data and
incorporate them into the adversarial loss:
Lscal =− Ex∼Ds [logD(S(x))]
− Ex∼Dt [log(1−D(S(x)))], (3)
whereS denotes the extractor of the structure-conditioned
features. Note that Eq. (3) deﬁnes the adversarial loss on the
structure-conditioned features. By using the conditioning
strategy, the structure-aware conditions have been success-
fully applied to the feature distribution. As a result, the
adversarial process could potentially align the features that
have similar structure-aware conditions, thereby achieving
the goal of preserving the compactness of the target local
structures.
To extract the structure-conditioned feature S(x), we
need a function that outputs the pseudo-label conditions ˆy,
which can represent the local structures of target features.
As shown in Fig. 3, we achieve it by two steps: local
structure establishment and surrogate classiﬁer approxima-
tion. Indeed, by doing these two steps, we are making a
differentiable approximation, i.e, a surrogate classiﬁerFS to
the non-differentiable local structures for the target domain.
We describe the two steps in the next subsection.
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 4
G
Unlabeled
target data Local structures  on
source class centers
Local structures on
clustering centers
Pseudo
labels G
B. Training a surrogate classifier using the pseudo labels
A. Establishing target local structures by clustering
Frozen
Target Class
classification error
Labeled
source data
G
G
D
Frozen
C. Reducing domain gap between domains by SCAL
Domain class
classification error
(source/target)
Unlabeled
target data 
Source class
classification error
Frozen
Gradient
Reverse
Layer
Unlabeled
target data 
Fig. 3. The framework of structure-conditioned adversarial learning (SCAL). Here, Gradient Reverse Layer [4], [5] is used to make the gradients
of its subsequent module D opposite to the gradients of its previous module G, therefore achieving adversarial training in one backpropagation
process. Before each epoch, we establish the target local structures by clustering in step A (Section 3.3). For each batch of one epoch, we adopt
two steps. We ﬁrst employ a surrogate classiﬁer to mimic the non-differentiable clustering procedure in step B. Then the predictions of the surrogate
classiﬁer are used as structure-aware conditions for the adversarial learning process in step C.
3.3 Local Structures for Target Domain
Based on Eq. (3), we need to establish the local structures,
i,e,, the feature clusters, for the unlabeled target domain
data. Mathematically, searching the feature clusters could
be cast as the following optimization problem:
min
{Ct
k}K
k=1
K∑
k=1
∑
x∈Ct
k
Ldist(G(x),µt
k), (4)
whereCt
k denotes the learned target cluster for class k, µt
k
denotes the center of Ct
k, and the distance metric satisﬁes:
Ldist(G(x),µt
k) = 1
2 (1− <G (x),µt
k >
∥G(x)∥∥µt
k∥ ). (5)
A common approach for Eq. (4) is spherical K-
means [42], [43]. Inspired by it, we adopt a source class
center initialized clustering algorithm, as shown in Fig. 3,
Algorithm 1 Class-aware Memory-base Domain adaptation
Input: The source domain dataset Ds, the target domain
datasetDt;
Output: The learned parameters of G,F , andFS;
1: Initialize a feature extractor G by an ImageNet pre-
trained ResNet
2: Randomly initialize a source classiﬁerF and a surrogate
classiﬁerFS
3: for epochs 1, 2, 3,..., MAX EPOCH do
4: Compute source class centers over the source features
5: Initialize target cluster centers by the source class
centers
6: Obtain the pseudo-labels of target samples by the
spherical K-means (Section 3.3)
7: for iterations 1, 2, 3,..., MAX ITER do
8: Sample a source data batch Bs and a target data
batchBt fromDs andDt
9: UpdateFS by Eq. (6) on Bt
10: UpdateG andF by Eq. (1) on Bs andBt
11: end for
12: end for
especially for the UDA scenarios (considering the inherent
relation between domains). With such a clustering algo-
rithm, we can obtain the target clusters as well as the
clustering labels for all target samples.
Note that the above local structures establishment pro-
cess is non-differentiable. Because of it, it is hard to adapt the
obtained local structures to the changing feature distribution
in the training process. The ﬁxed clustering result is harmful
for the ﬁnal performance, as shown in Table 4.
To deal with this issue, we provide a differentiable ap-
proximation, i.e., a differentiable surrogate classiﬁer FS, to
approximate the obtained local structures. The differentiable
surrogate classiﬁer FS is updated at each batch by mini-
mizing the cross-entropy loss Lce on the obtained pseudo-
labeled target sample set ˆDt:
min
FS
E(x,ˆy)∼ ˆDt [Lce(FS(G(x)), ˆy)]. (6)
Then the structure-conditioned featuresS(x) for each in-
stancex∈D s∪Dt can be obtained by taking the predictions
of the surrogate classiﬁer as conditions:
S(x) = G(x)⊗FS(G(x)). (7)
where ⊗ denotes outer product. Therefore, the overall
structured-conditioned loss Lscal of SCAL can be formu-
lated as:
Lscal =− Ex∼Ds [logD(G(x)⊗FS(G(x)))]
− Ex∼Dt [log(1−D(G(x)⊗FS(G(x))))]. (8)
For a clear description of our implementation procedure,
we provide the algorithm ﬂow of SCAL in Algorithm 1. Our
method mainly consists of three steps: local structure estab-
lishment, surrogate classiﬁer approximation, and structure-
conditioned adversarial learning. For each epoch, we ﬁrstly
establish the local structure by a source center initialized
clustering algorithm (lines 4-6). And for each batch of one
epoch, we use the surrogate classiﬁer to approximate the
local structure FS (line 9) and then integrate it into an
adversarial process (line 10) as structure conditions.
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 5
A -> W W -> A
Transfer Task
0.00
0.05
0.10
0.15
0.20
0.25
0.30
0.35T(h * )
ResNet-50
DANN
Our Method
Fig. 4. The expected errorET (h∗) on the target features of the ideal joint
hypothesis h∗ for different methods.
3.4 Theoretical Analysis
The theoretical analysis of SCAL is based on the domain
adaptation theory [1]. The theory reveals that the expected
errorET (h) on target samples of any classiﬁer h (drawn
from a hypothesis set H with optimal classiﬁer h∗) has the
following upper-bound w.r.t. the source errorES(·):
∀h∈H,ET (h)≤E S(h) + 1
2dH +ES(h∗) +ET (h∗). (9)
In fact, previous adversarial methods mainly focus on
the domain discrepancy dH (Note that ES(h) andES(h∗)
can be controlled by the classiﬁcation loss on labeled source
data) and usually ignore the discriminability of the target
featuresET (h∗). In contrast, we aim to pursue the balance
between dH andET (h∗) for UDA, which is detailed in the
following sections.
3.4.1 Analysis for T arget Feauture Discriminability
To investigate target feature discriminability ET (h∗) in-
depth, we use a well-trained multilayer perceptron (MLP)
classiﬁer to measure the ET (h∗) for different methods. For
convenience, we take the adversarial domain adaptation
method, i.e., DANN, for example. In domain adaptation
theory [2], the ideal joint hypothesis h∗ is deﬁned as:
h∗ = min
h∈H
ES(h) +ET (h) (10)
which is the optimal classiﬁer h∗ for the source dataset
and the target dataset. To obtain the h∗, we train a MLP
with the ﬁxed representations outputted by the feature
extractor of DANN over all data with the labels from both
domains. Note that the target labels are only used for this
analysis. Then the ET (h∗) of DANN is expected to be the
average prediction error of the MLP , i.e., h∗, on the ﬁxed
representations of the target domain data. The process of
obtainingET (h∗) in other methods is the same as the above
process with results shown in Fig. 4.
From Fig. 4, we observe that the ET (h∗) is reduced after
adversarial domain adaptation by DANN [11]. Obviously,
a higher error rate implies weaker discriminability, which
means the classiﬁer is difﬁcult to perform the classiﬁca-
tion of target domain data. With the cluster conditions,
our method can preserve the discriminability of original
feature distribution as shown in Fig. 4, therefore lowering
the upper-bound of the expected errorET (h).
3.4.2 Analysis for the Domain Discrepancy
Based on domain theory [2], the general domain discrep-
ancydH is measured over the feature space:
dH =2 sup
h∈H
⏐⏐Ex∼Ds(G)[I(h(x) = 1)]
− Ex∼Dt(G)[I(h(x) = 1)]
⏐⏐,
(11)
whereDs(G) ={G(x)|x∈Ds} andDt(G) ={G(x)|x∈Dt}
denote the set of the source and target features respectively.
Note a hypothesis is a function h :X→{ 0, 1}, andH is the
hypothesis space. We then deﬁne the HD-distance over the
structure-conditioned feature space as:
dHD =2 sup
D∈HD
⏐⏐Ex∼Ds(S)[I(D(x) = 1)]
− Ex∼Dt(S)[I(D(x) = 1)]
⏐⏐,
(12)
where
S(x) = G(x)⊗FS(G(x)). (13)
In the above equation,Ds(S) ={S(x)|x∈Ds} andDt(S) =
{S(x)|x∈Dt} denote the structure-conditioned feature set
of the source and target domains, respectively.
Theorem 1. Let D be a hypothesis in a symmetric
hypothesis space HD (If D∈H D, the inverse hypothesis
1−D is also inHD), then following inequality is satisﬁed:
dH≤dHD. (14)
Proof Formally, for a sample x, given the output of the
feature generator G(x) = ( g1,g 2,...,g N )T , the surrogate
classiﬁer prediction FS(G(x)) = ( f1,f 2,...,f M )T , and an
all-ones vectorJM = (1, 1,..., 1  
M
)T , we have
S(x)JM = (G(x)⊗ FS(G(x)))JM = G(x)
M∑
i=1
fi. (15)
For any hypothesis h ∈ H, we can construct a corre-
sponding hypothesis Dh(x) = h( xJM∑M
i=1fi
). Assuming the
family of domain classiﬁer HD is rich enough to contain
Dh(x), i.e., Dh(x)∈H D. Such an assumption is realistic as
we can use a complex domain classiﬁer D, i.e., the multi-
layer perceptrons, to ﬁt any functions. Then from Eq. (15),
we have
Dh(S(x)) = h( S(x)JM
∑M
i=1 fi
) = h(G(x)). (16)
From Eqs. (12) and (16), the following inequality can be
derived:
dHD = 2 sup
D∈HD
⏐⏐Ex∼Ds(S)[I(D(x) = 1)]−Ex∼Dt(S)[I(D(x) = 1)]
⏐⏐
≥ 2
(
Ex∼Ds(S)[I(Dh(x) = 1)]−Ex∼Dt(S)[I(Dh(x) = 1)]
)
= 2
(
Ex∼Ds [I(Dh(S(x)) = 1)]−Ex∼Dt [I(Dh(S(x)) = 1)]
)
.
= 2
(
Ex∼Ds [I(h(G(x)) = 1)]−Ex∼Dt [I(h(G(x)) = 1)]
)
= 2
(
Ex∼Ds(G)[I(h(x) = 1)]−Ex∼Dt(G)[I(h(x) = 1)]
)
.
(17)
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 6
Amazon 
 DSLR 
 Webcam 
(a) Ofﬁce-31
Artistic Clip Art Product Real-World (b) Ofﬁce-Home
Real Synthetic (c) VisDA-2017
Fig. 5. Exemplary images from different datasets. (a) Ofﬁce31: It has three distinct domains, including Amazon, DSLR, and Webcam. (b) Ofﬁce-
Home: It has four dissimilar domains, including Artistic, Clip Art, Product, and Real-World. (c) VisDa-2017: It has two domains, including Synthetic
and Real.
Considering Eq. (16) and the symmetry of HD, i.e., 1−
Dh(x)∈H D, we have
dHD≥− 2
(
Ex∼Ds(G)[I(h(x) = 1)]− Ex∼Dt(G)[I(h(x) = 1)]
)
.
(18)
Since for each h∈H , Eqs. (17) and (18) are satisﬁed, the
distribution discrepancy dHD with a symmetric hypothesis
spaceHD upper-bounds the general distribution discrep-
ancydH.
It is worth noting that the objective of the minimax game
we solve in our method is to minimize dHD. Concretely,
the domain classiﬁer D is trained to distinguish source and
target sample (obtain dHD) and the extractor G tries to
minimize it. As a result, the bound, i.e., dHD, of the domain
discrepancy dH is expected to be lowered in the training
process of SCAL.
4 E XPERIMENTS
4.1 Datasets
Ofﬁce-Home [50] is a challenging dataset, which contains
around 15,500 images from 65 categories. It consists of
images from four dissimilar domains: Artistic (Ar), Clip Art
(Cl), Product (Pr), and Real-World (Rw). We evaluate our
methods on all the twelve transfer tasks.
Ofﬁce-31 [31] is the most widely used benchmark for
unsupervised domain adaptation. It consists of 4110 images
belonging to 31 categories collected from three distinct
domains: Amazon (A), Webcam (W), DSLR (D). In particular,
the dataset is imbalanced across domains, with 2,817 images
in A, 795 images in W, and 498 images in D. We evaluate
our methods on all the six transfer tasks.
VisDA-2017 [51] is a large simulation-to-real dataset,
which consists of over 280K images across 12 classes. It
contains two very distinct domains: Synthetic, synthetic 2D
renderings of 3D models generated from different angles
and with different lighting conditions;Real, a photo-realistic
or real-image domain. We evaluate our methods on Syn-
thetic→Real transfer task.
4.2 Setup
Network Architectures. Similar to other unsupervised do-
main adaptation methods [5], [6], we employ ResNet [44]
(including ResNet-50 and ResNet-101) as our backbone net-
work. Speciﬁcally, we utilize the feature extractor part of
ResNet (before average pooling layer) as our feature extrac-
tor and one fully-connected layer as our source classiﬁer.
As for the domain classiﬁer or surrogate classiﬁer, we also
adopt one fully-connected layer.
Evaluation Protocol. We follow the standard evaluation
protocol for the unsupervised domain adaptation [5], [6].
We use all labeled source domain samples and all unlabeled
target domain samples during the training procedure, and
choose the output of the surrogate classiﬁer as our ﬁnal
prediction. We compare the mean classiﬁcation accuracy
based on three random experiments.
Training Details. For all benchmarks, we implement
our methods based on PyTorch and ﬁnetune our network
with the feature extractor part of ResNet pre-trained on
ImageNet [52]. And we train the network through back-
propagation [53], where the source classiﬁer and the sur-
rogate classiﬁer are trained from scratch with a learning
rate ten times that of the feature extractor part. For hyper-
parameters of Ofﬁce-31 and Ofﬁce-Home, we adopt mini-
batch SGD with epoch number of 100, momentum of 0.9,
λ of 1, and learning rate decay strategy implemented in
DANN [5]: the learning rate is updated by ηp = η0(1 +
αp)−β, where p is the training process linearly changing
from 0 to 1, and η0 = 0.001, α = 10 , β = 0.75. As for
VisDA-2017, the difference is that we use a new learning
rate decay strategy with η0 = 0.001,α = 5,β = 2.25.
4.3 Results
We compare SCAL with state-of-the-art (SOTA) methods of
DANN [5], CDAN+E [6], SymNets [45], BSP+CDAN [46],
SPL [29], DMP [38], ATM [37], AADA+CCN [47],
DMRL [54], GVB-GD [48], SRDC [28] and RSDA [49]. Most
results of them are directly quoted from their original pa-
pers while a small portion of the results are obtained by
running their online codes with the default training setting
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 7
TABLE 1
Accuracy (%) for all the twelve transfer tasks of Ofﬁce-Home based on ResNet-50. For simplicity, Ar→Cl is denoted by ArCl, and the names of
other transfer tasks are simpliﬁed similarly.
Method Year ArCl ArPr ArRw ClAr ClPr ClRw PrAr PrCl PrRw RwAr RwCl RwPr Avg
ResNet-50 [44] CVPR’2016 34.9 50.0 58.0 37.4 41.9 46.2 38.5 31.2 60.4 53.9 41.2 59.9 46.1
DANN [5] JMLR’2016 45.6 59.3 70.1 47.0 58.5 60.9 46.1 43.7 68.5 63.2 51.8 76.8 57.6
CDAN+E [6] NIPS’2018 50.7 70.6 76.0 57.6 70.0 70.0 57.4 50.9 77.3 70.9 56.7 81.6 65.8
SymNets [45] CVPR’2019 47.7 72.9 78.5 64.2 71.3 74.2 64.2 48.8 79.5 74.5 52.6 82.7 67.6
BSP+CDAN [46] ICML’2019 52.0 68.6 76.1 58.0 70.3 70.2 58.6 50.2 77.6 72.2 59.3 81.9 66.3
SPL [29] AAAI’2020 54.5 77.8 81.9 65.1 78.0 81.1 66.0 53.1 82.8 69.9 55.3 86.0 71.0
DMP [38] PAMI’2020 52.3 73.0 77.3 64.3 72.0 71.8 63.6 52.7 78.5 72.0 57.7 81.6 68.1
ATM [37] PAMI’2020 52.4 72.6 78.0 61.1 72.0 72.6 59.5 52.0 79.1 73.3 58.9 83.4 67.9
AADA+CCN [47] ECCV’2020 54.0 71.3 77.5 60.8 70.8 71.2 59.1 51.8 76.9 71.0 57.4 81.8 67.0
GVB-GD [48] CVPR’2020 57.0 74.7 79.8 64.6 74.1 74.6 65.2 55.1 81.0 74.6 59.7 84.3 70.4
RSDA-MSTN [49] CVPR’2020 53.2 77.7 81.3 66.4 74.0 76.5 67.9 53.0 82.0 75.8 57.8 85.4 70.9
SRDC [28] CVPR’2020 52.3 76.3 81.0 69.5 76.2 78.0 68.7 53.8 81.7 76.3 57.1 85.0 71.3
SCAL - 55.3 72.7 78.7 63.1 71.7 73.5 61.4 51.6 79.9 72.5 57.8 81.0 68.3
SCAL+SPL - 57.3 77.5 80.7 68.8 77.9 79.3 65.2 55.9 81.7 75.0 61.0 83.9 72.0
TABLE 2
Accuracy (%) for all the six transfer tasks of Ofﬁce-31 based on ResNet-50. (*) the implementation is based on the authors’ code.
Method Year A → W D → W W → D A → D D → A W → A Avg
ResNet-50 [44] CVPR’2016 68.4 ±0.2 96.7 ±0.1 99.3 ±0.1 68.9 ±0.2 62.5 ±0.3 60.7 ±0.3 76.8
DANN [5] JMLR’2016 82.0 ±0.4 96.9 ±0.2 99.1 ±0.1 79.7 ±0.4 68.2 ±0.4 67.4 ±0.5 82.2
CDAN+E [6] NIPS’2018 94.1 ±0.1 98.6 ±0.1 100.0±0.0 92.9 ±0.2 71.0 ±0.3 69.3 ±0.3 87.7
SymNets [45] CVPR’2019 90.8 ±0.1 98.8 ±0.3 100.0±0.0 93.9 ±0.5 74.6 ±0.6 72.5 ±0.5 88.4
BSP+CDAN [46] ICML’2019 93.3 ±0.2 98.2 ±0.2 100.0±0.0 93.0 ±0.2 73.6 ±0.3 72.6 ±0.3 88.5
SPL [29] AAAI’2020 92.7 ±0.0 98.1 ±0.0 99.8 ±0.0 93.7 ±0.0 76.4 ±0.0 76.9 ±0.0 89.6
DMP [38] PAMI’2020 93.0 ±0.3 99.0 ±0.1 100.0±0.0 91.0 ±0.4 71.4 ±0.2 70.2 ±0.2 87.4
ATM [37] PAMI’2020 95.7 ±0.3 99.3±0.1 100.0±0.0 96.4±0.2 74.1 ±0.2 73.5 ±0.3 89.8
DMRL [54] ECCV’2020 90.8 ±0.3 99.0 ±0.2 100.0±0.0 93.4 ±0.5 73.0 ±0.3 71.2 ±0.3 87.9
MCC [55] ECCV’2020 95.5 ±0.2 98.6 ±0.1 100.0±0.0 94.4 ±0.3 72.9 ±0.2 74.9 ±0.3 89.4
Symnets-G [48] CVPR’2020 93.8 ±0.4 98.8 ±0.2 100.0±0.0 96.1 ±0.3 74.9 ±0.4 72.8 ±0.3 89.4
SRDC* [28] CVPR’2020 94.6 ±1.0 99.2 ±0.5 100.0±0.0 92.6 ±0.6 78.1 ±1.3 76.3 ±0.2 90.1
RSDA-MSTN [49] CVPR’2020 96.1±0.2 99.3±0.2 100.0±0.0 95.8 ±0.3 77.4 ±0.8 78.9±0.3 91.1
SCAL - 93.5 ±0.2 98.5 ±0.1 100.0±0.0 93.4 ±0.3 72.4 ±0.1 74.0 ±0.3 88.6
SCAL+SPL - 95.8 ±0.3 99.2 ±0.4 100.0±0.0 94.6 ±0.1 77.5 ±0.2 76.0 ±0.2 90.5
TABLE 3
Accuracy (%) for Synthetic→Real task of VisDA-2017 based on
ResNet-101. (*) the implementation is based on the authors’ code.
Method Synthetic →Real
ResNet-101 [44] 52.4
CDAN+E [6] 71.7
BSP+CDAN [46] 75.9
SPL* [29] 67.3
DMP [38] 79.3
ATM [37] 75.1
DMRL [54] 75.5
MCC [55] 78.8
GVB-GD [48] 75.3
RSDA-DANN [49] 75.8
SCAL 80.1
SCAL+SPL 81.7
(denoted by *). To further investigate the effectiveness of the
proposed framework, we also apply SPL [29], a state-of-the-
art pseudo-labeling method to SCAL (replacing the original
clustering method with SPL).
Ofﬁce-Home. As shown in Table 1, we evaluate our
methods on all the twelve transfer tasks of Ofﬁce-Home.
We show that the proposed framework SCAL improves
the average accuracy of CDAN [6] by 2.5%, showing the
effectiveness of the proposed conditions. Compared to other
domain adaptation methods, SCAL+SPL achieves a signiﬁ-
cant improvement as well.
Ofﬁce-31. Table 2 lists the average classiﬁcation accura-
cies of the target samples on six transfer tasks of Ofﬁce-31.
Results demonstrate that our SCAL+SPL achieves second-
place performance with other domain adaptation methods.
It is notable that SCAL+SPL boosts the average accuracy
of the best method [49] on Ofﬁce-31 by 1.1% and 5.9% on
Ofﬁce-Home and VisDA-2017, respectively.
VisDA-2017. Table 3 shows the results on Syn-
thetic→Real transfer task of VisDA-2017. Following stan-
dard UDA setting [6], we use ResNet-101 as the feature
extractor for VisDA-2017. The results of Table 3 shows that
SCAL is universal for different datasets.
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 8
TABLE 4
Ablation studies of our methods for Ofﬁce-31 on individual components. (*) the implementation is based on the authors’ code.
Method A → W D → W W → D A → D D → A W → A Avg
analysis of the conditions:
Ours w/o conditions 82.0 96.9 99.1 79.7 68.2 67.4 82.2
Ours with src.center 89.8 94.3 99.0 86.5 63.7 62.2 82.6
Ours with src.KNN 92.6 98.1 100.0 86.3 67.0 67.3 85.2
Ours with src.classiﬁer 94.1 98.6 100.0 92.9 71.0 69.3 87.7
Ours with tgt.k-means (last) 94.3 95.8 99.8 91.4 71.2 72.4 87.5
SCAL 93.5 98.5 100.0 93.4 72.4 74.0 88.6
SCAL+SPL 95.8 99.2 100.0 94.6 77.5 76.0 90.5
analysis of the differentiable approximation:
Ours with non-differentiable 90.4 97.6 100.0 89.2 68.9 68.6 85.8
SCAL 93.5 98.5 100.0 93.4 72.4 74.0 88.6
analysis of the base pipelines:
JAN* 85.4 97.4 99.8 84.7 68.6 70.0 84.3
JAN with tgt.k-means (src.center) 93.0 97.9 99.8 88.0 68.6 68.2 85.9
MCD* 79.5 97.6 100.0 81.1 61.2 61.5 80.1
MCD with tgt.k-means (src.center) 89.8 97.0 98.6 89.2 76.3 73.8 87.4
0 10 20 30 40 50
Number of Loop
80
85
90
95
100Clustering Accuracy
SCAL
SCAL+SPL
(a) Clustering
 
DANN SCAL (b) Visualization
A -> W W -> D
Transfer Task
0.4
0.6
0.8
1.0
1.2
1.4
1.6
1.8
2.0A-Distance
ResNet-50
DANN
SCAL
SCAL+SPL (c) Divergence
50 1000 2000 3000 4000 5000 6000
Number of Iterations
0.0
0.1
0.2
0.3
0.4Test Error
ResNet-50
DANN
SCAL
SCAL+SPL (d) Convergence
Fig. 6. Empirical analysis of clustering accuracy, visualization on the toy dataset, distribution divergence, and convergence performance. Please
refer to the main text for how different experiments are deﬁned.
4.4 Empirical Analysis
Analysis of the Conditions. As shown in Table 4, we
examine the ablation experiments on Ofﬁce-31 to investigate
the effects of the conditions used in the adversarial adap-
tation method. Baseline “Ours w/o conditions” adopts the
adversarial adaptation method without conditions. “Ours
with src.center”, “Ours with src.KNN” (K=1), and “Ours
with src.classiﬁer” treat the pseudo label obtained by the
nearest source center, nearest K source features, and the
predictions of source classiﬁer as the conditions for the
baseline. We can observe that the result is improved with the
added conditions, showing the effectiveness of conditional
distribution alignment. We then adopt the non-parametric
clustering methods to model the target local structure.
The difference between “Ours with tgt.k-means (last)” and
SCAL is the center initialization way. The former utilizes the
last clustering center to initialize the target center, while the
latter utilizes the new source center to reinitialize the target
center. In Table 4, we can observe that the SCAL achieve
better average accuracy than “Ours with tgt.k-means (last)”
(+1.1%), indicating the effectiveness of the source center
initialization. We also employ SCAL+SPL to test the ef-
fect of our method when using a complex pseudo-labeling
method, i.e., SPL [29], which shows a better performance
than SCAL by 1.9%. These results of Table 4 demonstrate
the importance of the conditions for adversarial learning.
Different from previous methods, SCAL can integrate the
effective non-differentiable clustering conditions into adver-
sarial learning, thereby achieving a better performance.
(a) ResNet
 (b) DANN
(c) Our Method
Fig. 7. Visualization of different methods onW→A (all classes) of Ofﬁce-
31 (blue: W; red: A).
Differentiable Approximation Analysis. We test the
strength of the differentiable approximation by compar-
ing our method with the non-differentiable conditioned
adversarial learning, i.e., “Ours with non-differentiable”.
This method uses the same clustering algorithm as SCAL,
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 9
ResNet
speaker
 bike helmet
 mug
 headphones
 laptop computer
DANN
SCAL
Fig. 8. Visualization of different methods on W→A (1 classes) of Ofﬁce-31 (blue: W; red: A).
but simply uses the obtained pseudo-labels as conditions.
SCAL boosts the average accuracy of “Ours with non-
differentiable” by 2.8%, which suggests the effectiveness of
our surrogate classiﬁer approximation.
Baseline Analysis. We further evaluate the performance
of the structure-aware conditions by incorporating it into
other types of UDA pipelines on Ofﬁce-31. MCD [16] is
another line of the adversarial methods which do not use
the domain classiﬁer, and JAN [33] is a typical metric-
based method. Similar to SCAL, “JAN with tgt.k-means
(src.center)” and “MCD with tgt.k-means (src.center)” per-
form distribution alignment on the features conditioned on
the outputs of the surrogate classiﬁer. As shown in Table 4,
“JAN with tgt.k-means (src.center)” achieves better accuracy
than JAN by 1.6%, and “MCD with tgt.k-means (src.center)”
boosts the average accuracy of MCD by 7.3%. These results
demonstrate the transferability of the proposed conditions.
Clustering Accuracy Analysis. To deeply explore the
advantages of SCAL over the pseudo-labeling methods, we
report the accuracy curves of them in our framework. From
Fig. 6(a), we can observe that the clustering accuracies of
SCAL and SCAL+SPL are both improved in the global ad-
versarial alignment process. This supports the effectiveness
of our framework.
Visualization of Toy Dataset. We visualize the decision
boundaries of different methods on inter twinning moons
2D problems in Fig. 6(b). We follow the experimental setting
of MCD [16]. The source samples of classes 0 and 1 are
denoted by the red and green points. Blue points are target
samples generated by rotating the source samples. The dark
line and dashed line are the decision boundaries of DANN
and SCAL. The result of SCAL is clearly better than DANN.
Divergence Analysis. The distribution divergence [2]
can be measured by the A-distance [1], [6]. As shown
in Fig. 6(c), we observe that the A-distance on ResNet-
50 is larger than these adversarial methods, implying the
efﬁcacy of adversarial adaptation on reducing the domain
gap. Besides, theA-distance on SCAL is smaller than theA-
distance on DANN, manifesting that structure-conditioned
adversarial learning can further reduce distribution diver-
gence.
Convergence Analysis. We testify the convergence per-
formance of different methods on task A→ W (31 classes)
shown in Fig. 6(d). Without the adversarial process, ResNet-
50 enjoys faster convergence than other methods but the do-
main shift is preserved, thereby suffer an obvious accuracy
drop. For the adversarial adaptation methods, SCAL and
SCAL+SPL obtain consistent lower test error than DANN.
Visualization of Feature Distribution. Figs. 2 and 7
TABLE 5
Accuracy (%) of SCAL with the different noise levels of clustering for
A→W task on Ofﬁce-31.
Noise Level w/o conditions with noisy conditions
0% 82.0 93.5
25% 82.0 93.3
50% 82.0 91.6
75% 82.0 86.9
100% 82.0 74.7
TABLE 6
Time (s) of SCAL variants in one epoch for different datasets based on
ResNet-50.
Task Baseline SCAL
A→W (Ofﬁce-31) 48.3 55.4
Ar→Cl (Ofﬁce-Home) 86.2 98.9
Synthetic→Real (VisDA-2017) 2260.3 2759.4
visualize the feature distribution under different granularity
on task W→A of Ofﬁce-31 by t-SNE [56]. As shown in Fig. 8,
the intra-class compactness exists in the feature distribu-
tion of the target domain, and the distribution alignment
process has a potential risk of damaging it. This supports
our motivation. And with the structure-aware conditions,
our method can preserve the intra-class compactness and
reduce the domain shift simultaneously. As shown in Fig. 7,
compared to ResNet-50 and DANN, as expected, SCAL can
preserve the intra-class compactness and reduce the domain
shift as well.
Noise Sensitivity. We also investigate the sensitivity
of SCAL with respect to different noise levels nl on
task A→W for Ofﬁce-31. Speciﬁcally, we replace nl ∈
{0%, 25%, 50%, 75%, 100%} of the cluster-based pseudo-
labels with the random labels and then integrate them as
conditions into the adversarial process. Here we use the
source classiﬁer output as the ﬁnal predictions. As shown
in Table 5, the accuracy of our method is reduced by less
than 0.2% when the noise level is 25%. Besides, even in the
situation of a large noise level ( nl = 75% ), our method can
boost the accuracy of ”w/o conditions” by 4.9%.
Time Cost Analysis. Besides the network training, our
method needs to perform the clustering algorithm at each
epoch. Therefore, we testify the time costs of the baseline
method (i.e., DANN) and SCAL in one epoch on one Nvidia
GeForce GTX 1080 Ti. As shown in Table 6, we need about
15% additional time to perform the clustering algorithm,
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 10
which is acceptable in the domain adaptation task.
5 C ONCLUSION
In this paper, we have proposed an end-to-end structure-
conditioned adversarial domain adaptation scheme, which
aims to preserve the intra-class compactness through
structure-aware conditions in the adversarial learning pro-
cess. Speciﬁcally, the proposed scheme establishes local
structures by the clustering algorithm and then incorpo-
rates the obtained structures into the adversarial learning
process as structure-aware conditions for domain distribu-
tion alignment. The structure establishment and structure-
conditioned adversarial learning have been iteratively per-
formed. Experimental results have validated the effective-
ness of the proposed method.
REFERENCES
[1] S. Ben-David, J. Blitzer, K. Crammer, and F. Pereira, “Analysis of
representations for domain adaptation,” in Proc. NeurIPS , 2007,
pp. 137–144.
[2] S. Ben-David, J. Blitzer, K. Crammer, A. Kulesza, F. Pereira, and
J. W. Vaughan, “A theory of learning from different domains,”
Mach. Learn., vol. 79, no. 1-2, pp. 151–175, 2010.
[3] A. Torralba and A. A. Efros, “Unbiased look at dataset bias,” in
Proc. CVPR. IEEE, 2011, pp. 1521–1528.
[4] Y. Ganin and V . Lempitsky, “Unsupervised domain adaptation by
backpropagation,” in Proc. ICML, 2014.
[5] Y. Ganin, E. Ustinova, H. Ajakan, P . Germain, H. Larochelle,
F. Laviolette, M. Marchand, and V . Lempitsky, “Domain-
adversarial training of neural networks,” J. Mach. Learn. Res. ,
vol. 17, no. 1, pp. 2096–2030, 2016.
[6] M. Long, Z. Cao, J. Wang, and M. I. Jordan, “Conditional adver-
sarial domain adaptation,” in Proc. NeurIPS, 2018, pp. 1640–1650.
[7] E. Tzeng, J. Hoffman, K. Saenko, and T. Darrell, “Adversarial
discriminative domain adaptation,” in Proc. CVPR, 2017, pp. 7167–
7176.
[8] H.-K. Hsu, C.-H. Yao, Y.-H. Tsai, W.-C. Hung, H.-Y. Tseng,
M. Singh, and M.-H. Yang, “Progressive domain adaptation for
object detection,” in Proc. WACV, 2020, pp. 749–757.
[9] J. Hoffman, E. Tzeng, T. Park, J.-Y. Zhu, P . Isola, K. Saenko,
A. A. Efros, and T. Darrell, “Cycada: Cycle-consistent adversarial
domain adaptation,” in Proc. ICML, 2017.
[10] E. Tzeng, J. Hoffman, N. Zhang, K. Saenko, and T. Darrell, “Deep
domain confusion: Maximizing for domain invariance,” arXiv
preprint arXiv:1412.3474, 2014.
[11] S. Chen, M. Harandi, X. Jin, and X. Yang, “Domain adaptation by
joint distribution invariant projections,” IEEE Trans. Image Process.,
vol. 29, pp. 8264–8277, 2020.
[12] H. Yan, Z. Li, Q. Wang, P . Li, Y. Xu, and W. Zuo, “Weighted
and class-speciﬁc maximum mean discrepancy for unsupervised
domain adaptation,” IEEE Trans. Multimedia, 2019.
[13] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley,
S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial
nets,” in Proc. NeurIPS, 2014, pp. 2672–2680.
[14] P . O. Pinheiro, “Unsupervised domain adaptation with similarity
learning,” in Proc. CVPR, 2018, pp. 8004–8013.
[15] W. Zhang, D. Xu, W. Ouyang, and W. Li, “Self-paced collaborative
and adversarial network for unsupervised domain adaptation,”
IEEE Trans. Pattern Anal. Mach. Intell., 2019.
[16] K. Saito, K. Watanabe, Y. Ushiku, and T. Harada, “Maximum
classiﬁer discrepancy for unsupervised domain adaptation,” in
Proc. CVPR, 2018, pp. 3723–3732.
[17] S. Lee, D. Kim, N. Kim, and S.-G. Jeong, “Drop to adapt: Learning
discriminative features for unsupervised domain adaptation,” in
Proc. ICCV, 2019, pp. 91–100.
[18] K. Saito, Y. Ushiku, T. Harada, and K. Saenko, “Adversarial
dropout regularization,” in Proc. ICLR, 2018.
[19] S. Cicek and S. Soatto, “Unsupervised domain adaptation via
regularized conditional alignment,” in Proc. ICCV, 2019, pp. 1416–
1425.
[20] Z. Deng, Y. Luo, and J. Zhu, “Cluster alignment with a teacher for
unsupervised domain adaptation,” in Proc. ICCV, 2019, pp. 9944–
9953.
[21] S. Xie, Z. Zheng, L. Chen, and C. Chen, “Learning semantic
representations for unsupervised domain adaptation,” in Proc.
ICML, 2018, pp. 5423–5432.
[22] M. Long, J. Wang, G. Ding, J. Sun, and P . S. Yu, “Transfer feature
learning with joint distribution adaptation,” in Proc. ICCV, 2013,
pp. 2200–2207.
[23] J. Zhang, W. Li, and P . Ogunbona, “Joint geometrical and statistical
alignment for visual domain adaptation,” in Proc. CVPR, 2017, pp.
1859–1867.
[24] J. Wang, W. Feng, Y. Chen, H. Yu, M. Huang, and P . S. Yu,
“Visual domain adaptation with manifold embedded distribution
alignment,” in Proc. ACM MM, 2018, pp. 402–410.
[25] O. Sener, H. O. Song, A. Saxena, and S. Savarese, “Learning trans-
ferrable representations for unsupervised domain adaptation,” in
Proc. NeurIPS, 2016, pp. 2110–2118.
[26] Z. Pei, Z. Cao, M. Long, and J. Wang, “Multi-adversarial domain
adaptation,” in Proc. AAAI, 2018.
[27] G. Kang, L. Jiang, Y. Yang, and A. G. Hauptmann, “Contrastive
adaptation network for unsupervised domain adaptation,” inProc.
CVPR, 2019, pp. 4893–4902.
[28] H. Tang, K. Chen, and K. Jia, “Unsupervised domain adaptation
via structurally regularized deep clustering,” in Proc. CVPR, 2020,
pp. 8725–8735.
[29] Q. Wang and T. Breckon, “Unsupervised domain adaptation via
structured prediction based selective pseudo-labeling,” in Proc.
AAAI, 2020.
[30] C. Chen, W. Xie, W. Huang, Y. Rong, X. Ding, Y. Huang, T. Xu,
and J. Huang, “Progressive feature alignment for unsupervised
domain adaptation,” in Proc. CVPR, 2019, pp. 627–636.
[31] K. Saenko, B. Kulis, M. Fritz, and T. Darrell, “Adapting visual
category models to new domains,” in Proc. ECCV. Springer, 2010,
pp. 213–226.
[32] M. Long, Y. Cao, J. Wang, and M. Jordan, “Learning transferable
features with deep adaptation networks,” in Proc. ICML, 2015, pp.
97–105.
[33] M. Long, H. Zhu, J. Wang, and M. I. Jordan, “Deep transfer
learning with joint adaptation networks,” in Proc. ICML. JMLR.
org, 2017, pp. 2208–2217.
[34] B. Sun, J. Feng, and K. Saenko, “Return of frustratingly easy
domain adaptation,” in Proc. AAAI, vol. 30, no. 1, 2016.
[35] H. Li, S. Wang, R. Wan, and A. K. Chichung, “Gmfad: Towards
generalized visual recognition via multi-layer feature alignment
and disentanglement,” IEEE Trans. Pattern Anal. Mach. Intell., 2020.
[36] B. Sun and K. Saenko, “Deep coral: Correlation alignment for deep
domain adaptation,” in Proc. ECCV. Springer, 2016, pp. 443–450.
[37] J. Li, E. Chen, Z. Ding, L. Zhu, K. Lu, and H. T. Shen, “Maximum
density divergence for domain adaptation,” IEEE Trans. Pattern
Anal. Mach. Intell., 2020.
[38] Y.-W. Luo, C.-X. Ren, D. Dao-Qing, and H. Yan, “Unsupervised do-
main adaptation via discriminative manifold propagation,” IEEE
Trans. Pattern Anal. Mach. Intell., 2020.
[39] B. B. Damodaran, B. Kellenberger, R. Flamary, D. Tuia, and
N. Courty, “Deepjdot: Deep joint distribution optimal transport
for unsupervised domain adaptation,” in Proc. ECCV , 2018, pp.
447–463.
[40] J. Shen, Y. Qu, W. Zhang, and Y. Yu, “Wasserstein distance guided
representation learning for domain adaptation,” in Proc. AAAI ,
vol. 32, no. 1, 2018.
[41] M. Li, Y.-M. Zhai, Y.-W. Luo, P .-F. Ge, and C.-X. Ren, “Enhanced
transport distance for unsupervised domain adaptation,” in Proc.
CVPR, 2020, pp. 13 936–13 944.
[42] I. S. Dhillon and D. S. Modha, “Concept decompositions for large
sparse text data using clustering,” Mach. Learn. , vol. 42, no. 1-2,
pp. 143–175, 2001.
[43] S. Zhong, “Efﬁcient online spherical k-means clustering,” in Proc.
IJCNN, vol. 5. IEEE, 2005, pp. 3180–3185.
[44] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for
image recognition,” in Proc. CVPR, 2016, pp. 770–778.
[45] Y. Zhang, H. Tang, K. Jia, and M. Tan, “Domain-symmetric net-
works for adversarial domain adaptation,” in Proc. CVPR , 2019,
pp. 5031–5040.
[46] X. Chen, S. Wang, M. Long, and J. Wang, “Transferability vs. dis-
criminability: Batch spectral penalization for adversarial domain
adaptation,” in Proc. ICML, 2019, pp. 1081–1090.
IEEE TRANSACTIONS ON PATTERN ANAL YSIS AND MACHINE INTELLIGENCE 11
[47] J. Yang, H. Zou, Y. Zhou, Z. Zeng, and L. Xie, “Mind the discrim-
inability: Asymmetric adversarial domain adaptation.”
[48] S. Cui, S. Wang, J. Zhuo, C. Su, Q. Huang, and Q. Tian, “Gradually
vanishing bridge for adversarial domain adaptation,” in Proc.
CVPR, 2020, pp. 12 455–12 464.
[49] X. Gu, J. Sun, and Z. Xu, “Spherical space domain adaptation with
robust pseudo-label loss,” in Proc. CVPR, 2020, pp. 9101–9110.
[50] H. Venkateswara, J. Eusebio, S. Chakraborty, and S. Panchanathan,
“Deep hashing network for unsupervised domain adaptation,” in
Proc. CVPR, 2017, pp. 5018–5027.
[51] X. Peng, B. Usman, N. Kaushik, J. Hoffman, D. Wang, and
K. Saenko, “Visda: The visual domain adaptation challenge,” 2017.
[52] O. Russakovsky, J. Deng, H. Su, J. Krause, S. Satheesh, S. Ma,
Z. Huang, A. Karpathy, A. Khosla, M. Bernstein et al., “Imagenet
large scale visual recognition challenge,” Int. J. Comput. Vis. , vol.
115, no. 3, pp. 211–252, 2015.
[53] Y. LeCun, B. E. Boser, J. S. Denker, D. Henderson, R. E. Howard,
W. E. Hubbard, and L. D. Jackel, “Handwritten digit recognition
with a back-propagation network,” inProc. NeurIPS, 1990, pp. 396–
404.
[54] Y. Wu, D. Inkpen, and A. El-Roby, “Dual mixup regularized learn-
ing for adversarial domain adaptation,” in Proc. ECCV. Springer,
2020, pp. 540–555.
[55] Y. Jin, X. Wang, M. Long, and J. Wang, “Minimum class confusion
for versatile domain adaptation,” in Proc. ECCV. Springer, 2020,
pp. 464–480.
[56] L. v. d. Maaten and G. Hinton, “Visualizing data using t-sne,” J.
Mach. Learn. Res., vol. 9, no. Nov, pp. 2579–2605, 2008.
