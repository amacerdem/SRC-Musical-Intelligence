# Reconfiguration of functional brain hierarchy in schizophrenia

**Authors:** Irene Acero-Pousa
**Year:** D:20
**Subject:** Translational Psychiatry, doi:10.1038/s41398-025-03584-0

---

ARTICLE
OPEN
Reconﬁguration of functional brain hierarchy in schizophrenia
Irene Acero-Pousa
1,2✉, Anira Escrichs
1, Paulina Clara Dagnino1,2, Yonatan Sanz Perl1,2,3, Morten L. Kringelbach
2,4,5,6, Peter J. Uhlhaas
7,8 and Gustavo Deco
1,2,9
© The Author(s) 2025, corrected publication 2025
The multidimensional nature of schizophrenia requires a comprehensive exploration of the functional and structural brain
networks. While prior research has provided valuable insights into these aspects, our study goes a step further to investigate the
reconﬁguration of the hierarchy of brain dynamics, which can help understand how brain regions interact and coordinate in
schizophrenia. We applied an innovative thermodynamic framework, which allows for a quantiﬁcation of the degree of functional
hierarchical organisation by analysing resting state fMRI-data. Our ﬁndings reveal increased hierarchical organisation at the whole-
brain level and within speciﬁc resting-state networks in individuals with schizophrenia, which correlated with negative symptoms,
positive formal thought disorder and apathy. Moreover, using a machine learning approach, we showed that hierarchy measures
allow a robust diagnostic separation between healthy controls and schizophrenia patients. Thus, our ﬁndings provide new insights
into the nature of functional connectivity anomalies in schizophrenia, suggesting that they could be caused by the breakdown of
the functional orchestration of brain dynamics. Translational Psychiatry (2025) 15:356; https://doi.org/10.1038/s41398-025-03584-0
INTRODUCTION
Schizophrenia is a severe and often chronic psychiatric disorder
characterized by a range of multidimensional symptoms, includ-
ing positive symptoms, such as hallucinations and delusions, and
negative symptoms, such as anhedonia and avolition [1]. The
multifaceted nature of schizophrenia is further compounded by
ﬂuctuating symptomatology throughout individuals’ lives, leading
to signiﬁcant heterogeneity among patients [2]. This complexity
and variability require a comprehensive exploration of both the
anatomical and functional brain networks. The presence of neuroanatomical anomalies in both grey and
white matter is a well-established phenomenon in schizophrenia
[3, 4]. Robust evidence has revealed regionally decreased grey
matter in both ﬁrst-episode and chronic schizophrenia patients,
speciﬁcally in the frontal lobe [5–7], cingulate cortex [5, 8], the
thalamus [9, 10], insula [11], post-central gyrus [5], and medial
temporal regions [5, 6]. In terms of white matter alterations,
reductions in the corpus callosum [8], as well as in the frontal and
temporal lobes [8, 12] have been extensively documented. Furthermore,
alterations
in
functional
brain
dynamics
in
schizophrenia have been thoroughly reported using resting-state
functional magnetic resonance imaging (fMRI) [13, 14]. Among the
networks considered most relevant are the salience network and
the default mode network (DMN) [15, 16]. Studies have identiﬁed
heterogeneous ﬁndings, with some indicating hyperconnectivity
[17, 18], while others report hypoconnectivity [19] which can vary
across networks [20–22]. Despite the numerous identiﬁed structural and functional
abnormalities, the underlying nature of the pathophysiology
remains unclear [23], emphasizing the need for alternative
perspectives
and
hypotheses. One
promising
approach
to
conceptualize these anomalies is to consider these deﬁcits as a
disorder of integration of information across brain regions [24–27]. Information integration can be studied by analysing the level of
asymmetry in the interactions among brain regions, that is, the
extent to which information is transmitted in a non-reciprocal
manner between them. In a symmetrical system, communication
between regions is reciprocal, with no dominant directionality,
leading to a uniform distribution of information processing. However, this lacks the differentiation needed for hierarchical
organisation, where certain regions play specialized or more
inﬂuential roles in guiding brain function. On the other hand,
asymmetrical interactions indicate non-reciprocal communication,
where information is integrated in a small group of regions before
being transmitted to the others across the whole-brain [28, 29]. This creates a hierarchical arrangement that is indicative of non-
equilibrium systems, facilitates distinct processing of specialized
functional domains and allows for dynamic conﬁguration and
intercommunication among brain regions [30, 31]. Hierarchical organisation in fMRI-data has been previously
assessed in several studies. For instance, previous studies have
revealed that states of reduced consciousness exhibit lower
hierarchical arrangements compared to conscious wakefulness
[32, 33]. Moreover, physically and cognitively demanding tasks
Received: 13 May 2025 Revised: 29 July 2025 Accepted: 28 August 2025
1Computational Neuroscience Group, Center for Brain and Cognition, Department of Information and Communication Technologies, Universitat Pompeu Fabra, Barcelona, Spain.
2International Centre for Flourishing, Universities of Oxford (UK), Aarhus (Denmark) and Pompeu Fabra (Spain), Oxford, UK. 3Department of Engineering, University of San Andrés, Buenos Aires, Argentina. 4Department of Psychiatry, University of Oxford, Oxford, UK. 5Center for Music in the Brain, Department of Clinical Medicine, Aarhus University, Aarhus, Denmark. 6Centre for Eudaimonia and Human Flourishing, Linacre College, University of Oxford, Oxford, UK. 7Department of Child and Adolescent Psychiatry, Charité-
Universitätsmedizin Berlin, Berlin, Germany. 8Institute of Neuroscience and Psychology, University of Glasgow, Glasgow, Scotland, United Kingdom of Great Britain and Northern
Ireland. 9Institució Catalana de la Recerca i Estudis Avançats (ICREA), Barcelona, Spain. ✉email: irene.aceroi@upf.edu
www.nature.com/tp
Translational Psychiatry
1234567890();,:

increase the hierarchical organisation compared to a resting state
[34, 35]. In the context of schizophrenia, some studies suggest
overall altered hierarchy [36–40], while others highlight speciﬁc
alterations in individual networks [41–43]. Here, we apply a new theoretical framework able to quantify
the hierarchical organisation of brain networks in schizophrenia
[44]. The core idea is that the level of hierarchy in a system is
reﬂected in how far it deviates from thermodynamic equilibrium
[28]. To capture this, we use the ﬂuctuation-dissipation theorem
(FDT) from statistical physics, in combination with whole-brain
modeling [45, 46]. At equilibrium, a system’s spontaneous
ﬂuctuations can accurately predict its response to small perturba-
tions, a principle formalized by FDT. In contrast, non-equilibrium
systems violate this principle: their intrinsic ﬂuctuations fail to
predict dissipation after perturbations. The magnitude of these
violations serves as a proxy for the level of non-equilibrium, which
in turn reﬂects the system’s hierarchical organisation [44]. This is
because hierarchical systems are inherently directional: informa-
tion ﬂows preferentially from higher to lower levels, introducing
asymmetries that push the system away from equilibrium. We apply this framework to investigate whether individuals
with schizophrenia exhibit altered hierarchical dynamics. We
hypothesize that in schizophrenia, the ﬂow of information across
brain regions is disrupted, leading to a breakdown in the
orchestrated coordination that underlies healthy brain function. Furthermore, we hypothesize that the degree of hierarchical
organisation correlates with symptom severity across individuals.

## MATERIALS AND METHODS

Participants
In this study, we analysed resting-state fMRI data sourced from the UCLA
Consortium for Neuropsychiatric Phenomics LA5c Study ([47], open-
neuro.org/datasets/ds000030). Our participant pool encompassed two
age-matched cohorts: 50 individuals diagnosed with schizophrenia (12
female, mean group age: 36.5 ± 8.8, standard error of the mean
(SEM) ± 1.26) and 50 healthy subjects (16 female, mean group age:
36.6 ± 8.9,

## SEM ± 0.88). All
participants
provided
written
informed
consent following the University of California Los Angeles Institutional
Review Board’s approved protocols. Control group inclusion criteria
involved individuals with no prior psychiatric diagnoses or familial
psychiatric history and no prior exposure to psychotropic drugs. Detailed
dataset information is available in the data description provided by
Poldrack et al. [48]. Functional MRI data acquisition
MRI data was acquired using two distinct scanners, the Ahmanson-
Lovelace Brain Mapping Center (Siemens version syngo MR B15) and the
Staglin Center for Cognitive Neuroscience (Siemens version syngo MR B17)
at UCLA. Functional MRI data was collected using a T2* weighted
echoplanar
imaging sequence with oblique slice orientation (slice
thickness = 4 mm, 34 slices, TR = 2 s, TE = 30 ms, ﬂip angle = 90°, matrix
64 × 64, FOV = 192 mm, 152 volumes). An anatomical volume was also
captured
using
a
T1-weighted
sequence
(TR = 1.9 s, TE = 2.26 ms, FOV = 250 mm, matrix = 256 × 256, sagital plane, slice thickness = 1 mm,
176 volumes). Throughout the experiment, participants were instructed to
remain relaxed with their eyes open. Preprocessing of the fMRI data involved fMRIPrep v1.1 [49], a Nipype-based
tool developed by Gorgolewski et al. [50]. Motion-related noise was removed
using the nonaggressive variant of ICA-AROMA [51], which preserves shared
variance between motion- and neural-related components while regressing
out only motion-speciﬁc variance. Additionally, mean white matter and
cerebrospinal ﬂuid signal were regressed out and no global signal regression
(GSR) was utilized during data processing. Finally, the brain was divided using
the DK80 parcellation [52], including 62 cortical (31 per hemisphere), and
18 subcortical areas (9 per hemisphere), a total of 80 regions. Diffusion MRI data acquisition
For structural connectivity data acquisition, we processed multi-shell
diffusion-weighted imaging (DWI) data from a separate normative sample
of 32 healthy participants drawn from the Human Connectome Project
(HCP) database. These data were used solely to generate the structural
connectivity matrix for the whole-brain model and were not derived from
the same individuals included in the main experimental analyses. The
scans, spanning approximately 89 min, adhered to acquisition parameters
detailed in Thomas et al. [53]. Connectivity was estimated using the
method outlined by Horn et al. [54]. Brieﬂy, the data was processed using a
generalized q-sampling imaging algorithm implemented in DSI studio
(http://dsi-studio.labsolver.org). T2-weighted
anatomical
images
were
segmented to generate a white-matter mask, and image co-registration
to the b0 image of the diffusion data was performed employing SPM12. Within this reﬁned white-matter mask, we sampled 200,000 ﬁbres for each
participant in the Human Connectome Project. These ﬁbres were then
transformed into MNI space, utilizing Lead-DBS [55]. The methodology was
designed to employ algorithms demonstrated to be optimal, minimizing
false-positive ﬁbres, as underscored in recent open challenges [56, 57]. Theoretical framework
Violations of the ﬂuctuation-dissipation theorem. To characterize the
degree of non-equilibrium in brain dynamics, we quantify violations of
the Fluctuation-Dissipation Theorem (FDT) [44]. In essence, the FDT
formalizes a core principle of thermodynamic equilibrium: in systems that
are in equilibrium, the internal ﬂuctuations (random, spontaneous
changes) contain all the information needed to predict how the system
would respond to small perturbations. This relationship breaks down in
systems that are out of equilibrium, such as living organisms or brain
networks, because these systems are not random and spontaneous
anymore but exhibit directional, asymmetric, and history-dependent
behaviors. As a result, the actual response to perturbation deviates from
what would be predicted based on ﬂuctuations alone, leading to a
violation of the FDT. Thus, the level of violation of the FDT is indicative of
the degree of non-equilibrium in a system, which we use as a proxy of the
level of hierarchy [44]. The underlying rationale is that hierarchically
organized systems exhibit asymmetric and directional information ﬂow,
which is a hallmark of non-equilibrium. To quantify these violations, we rely on Onsager’s regression principle,
which offers a conceptual and mathematical foundation for the FDT
[45, 58]. Onsager postulated that the relaxation of a system back to
equilibrium after a small perturbation follows the same trajectory as a
spontaneous ﬂuctuation would in an unperturbed system. This symmetry
between cause and effect enables the derivation of FDT and provides a
way to measure its violations. Let us consider a system initially in equilibrium (state 1), with its
ﬂuctuations described by a probability distribution P0 G
ð Þ, where G
represents a conﬁguration of the system (e.g., a brain state). At time
t ¼ 0, we apply a small perturbation ε coupled to an observable B G
ð Þ,
causing the system to transition toward a new conﬁguration (state 2). We
then monitor the evolution of another observable A G
ð Þ over time. The
expected value of A at time t is given by:
hA tð Þiε ¼
X
G; G0

## A G

ð ÞPε G; tjG0; 0
ð

## ÞP0 G0

ð
Þ:
(1)
Here, Pε G; tjG0; 0
ð
Þ is the conditional probability that the system evolves
from conﬁguration G0 to G over time t. In this expression, we average over
all possible initial conﬁgurations G0, each weighted by their likelihood at
equilibrium P0 G0
ð
Þ to compute the expected value of observable A after
time t, depending on how the system evolves from each G0. Intuitively, this can be seen as applying a perturbation to a brain area B
and observing its effects on another brain area A. According to Onsager’s
regression hypothesis, the system’s response to a weak perturbation
mirrors the way it would spontaneously ﬂuctuate when unperturbed. In
other words, the relaxation of the system after a disturbance follows the
same statistical patterns as its natural ﬂuctuations at equilibrium. Using this
principle, we can rewrite the conditional probability Pε G; tjG0; 0
ð
Þ in terms
of the system’s equilibrium dynamics, and a correction due to the
perturbation: Pε G; tjG0; 0
ð
Þ ¼ P0 G; tjG0; 0
ð
Þ expðβε B G
ð Þ  B G0
ð
Þ
½
Þ:
(2)
Here, P0 G; tjG0; 0
ð
Þ is the unperturbed conditional probability, that is, how
the system would evolve from conﬁguration G0 to G over time t when it is
not perturbed, ε is the strength of the perturbation, B G
ð Þ is the observable
it acts on, and β ¼

KBT is the inverse of the temperature, from statistical
mechanics, which reﬂects how sensitive the system is to changes at a
given temperature. Essentially, this equation says that the perturbed
I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

conditional
probability
equals
the
unperturbed
probability
slightly
modiﬁed by how strongly the perturbation inﬂuences the system. Substituting this into Eq. 1 and expanding the exponential to ﬁrst order
in ε, we obtain:
hA tð Þiε  hA tð Þi0 ¼ βε P

## G; G0 A G

ð Þ B G
ð Þ  B G0
ð
Þ
½

## P0 G0

ð
Þ
¼ βε hA tð ÞB tð Þi0  hA tð ÞB 0
ð Þi0


(3)
Which indicates that the change in the expectation value of A due to a
small perturbation in B is governed by how A and B are spontaneously
correlated in the unperturbed system. Then, we can deﬁne the susceptibility as the change in the expectation
value of A in response to the perturbation. This measures how sensitive A is
to changes in B, and is formally given by the derivative of hA tð Þi with
respect to the perturbation strength ε:
χA; B tð Þ ¼ ∂hA tð Þi
∂ε
¼ hA tð Þiε  hA tð Þi0
ε
¼ β hA tð ÞB tð Þi0  hA tð Þi0hB tð Þi0


(4)
This expression indicates that the susceptibility at time t depends
entirely on correlation functions of the unperturbed system. To obtain the static form of the FDT, we consider the limit where the
system has had enough time to relax after the perturbation, that is when
t! 1, obtaining the correspondence between the response of a system
to a perturbation (on the left-hand side) and its unperturbed correlations
(on the right-sand side) in equilibrium:
χA; B ¼ β hABi0  hAi0hBi0


(5)
Violations of the FDT in non-equilibrium. If we describe the unperturbed
state to have the mean values of the observables equal to zero
(hAi0hBi0 ¼ 0), then we can characterize the level of non-equilibrium as
the normalized divergence of a system from the FDT: DA; B ¼ βhABi0  χA; B
χA; B;
(6)
where βhABi0 explains the unperturbed ﬂuctuations and χA; B corresponds
to the response to a small perturbation ε. To obtain the total deviation of
the FDT (D), we need to compute the mean value of DA; B for all observables
A and all perturbation points B. Thus, by leveraging the degree of deviation
from the FDT we are assessing the distance from equilibrium of a system. Model-based FDT of whole-brain data
Whole-brain model. In order to estimate the total violation of the FDT (D, Eq. 6), we need to systematically perturb all brain regions B and observe
the respective responses on all brain regions A. Thus, our initial step
involves constructing a whole-brain model ﬁtting the functional neuroima-
ging data in each group. This model allows us to derive the analytical
expressions elucidating the correlations among all brain regions under
spontaneous ﬂuctuations and, subsequently, to apply a perturbation in a
brain region and predict their average effect in all the other regions. The whole-brain model consists of describing each node’s local
dynamics as the normal form of a supercritical Hopf bifurcation, capable
of
deﬁning
the
transition
from
asynchronous
noisy
behaviour
to
oscillations [59]. Please, see the Supplementary Information (SI) for the
full mathematical description of the Hopf model and its linearization. Details on the model parameters are provided in Supplementary Table 4. Measuring violations of the model-based FDT. Using the described model,
we can compute the violations of the FDT. First, we start by computing the
covariance matrix K ¼ hδuδuTi. To do it, we ﬁrst express Eq. 3 (SI) as
dδu ¼ Jδudt þ dW, where dW stands for a Wiener process with covariance
hdWdWTi ¼ Qdt. Here, Q is the covariance matrix of the noise. Then, using
Itô’s stochastic calculus, we obtain d δuδuT
ð
Þ ¼ d δu
ð
ÞδuT þ δud δuT
ð
Þþ
d δu
ð
Þd δuT
ð
Þ. Considering that hδudWTi ¼ 0, maintaining the terms to ﬁrst
order in the differential dt and taking the expectations, we get:
dK
dt ¼ JK þ KJT þ Q:
(7)
This allows us to compute the static covariance by
JK þ KJT þ Q ¼ 0;
(8)
which can be solved using the eigen-decomposition of the Jacobian matrix
J [60] and, from the ﬁrst N rows and columns of the covariance K we ﬁnally
get the functional connectivity simulated by the model (FCsimulated), which
represents the real part of the dynamics. Having a ﬁtted coupling matrix C for each participant and each group
(see SI), we formulate an analytical expression of Eq. 6 for the deviation
from the FDT. Initially, we compute the expectation values of the state
variables hδuiεj when a perturbation ε is applied to a node j. Utilizing Eq. 3
(SI), we can determine that d
dt hδuiεj ¼ Jhδuiεj þ hj ¼ 0, being hj a 2N vector
primarily of zeros except component j that equals the value of the
perturbation ε. Solving for the desired expectation value, we obtain
hδuiεj ¼ J1hj. Considering only the real part of hδuiεj, we obtain
hδxij ¼ hδx
iεj
ε. With this, we proceed to deﬁne the deviation from the FDT
for region i when a perturbation is applied to region j: Di;j ¼
2hδxiδxj
i0
σ2  hδxiij
hδxiij
(9)
Here, the covariance hδxiδxi0 is computed from KSsimulated, and the term 2
σ2
is the inverse of temperature β. Then, the effect of perturbing region j on
all the other regions can be computed as: Pj ¼

N
P
i 2hδxiδxj
i0
σ2  hδxiij

N
P
i hδxiij
(10)
With this equation, we can deﬁne a vector, the perturbability map P
which quantiﬁes the global impact of each region’s perturbation. This
perturbability reﬂects how strongly a region drives the system’s dynamics
out of equilibrium, serving as a proxy for hierarchical position. Regions
exhibiting stronger violations of the ﬂuctuation-dissipation theorem (FDT)
are considered higher in the functional hierarchy, exerting intrinsic and
directional inﬂuence beyond symmetric equilibrium dynamics. Conversely,
regions with minimal FDT violations rank lower, with dynamics primarily
shaped by incoming interactions. This hierarchical interpretation is grounded in the fact that FDT violations
emerge from asymmetric, directional interactions between regions. Speciﬁ-
cally, regions with higher FDT deviation show a characteristic asymmetry: a
greater out-degree (number of outgoing connections) combined with a
lower in-degree (number of incoming connections). This imbalance reﬂects
their net directional inﬂuence, enabling these regions to drive the system
farther from equilibrium. Therefore, larger departures from equilibrium
correspond to stronger asymmetry, which underpins the preferential ﬂow of
information that deﬁnes functional hierarchy (Supplementary Fig. 1). Using it, we can compute the level of non-equilibrium for each participant
by averaging the deviation from the FDT over all possible perturbations:

## D^ ¼ 1

N
X
j
Pj
(11)
The analysis across the whole-brain network is performed both at the
subject and at the node level. In the ﬁrst case, we compute D^ for each
participant belonging to each group, obtaining one average value of FDT
deviations of cortical nodes per subject. In the second case, we average the
perturbability maps P across subjects in each group, obtaining one
averaged P per group, which represents the mean value per node. Resting-state networks
Resting-state networks (RSNs) were deﬁned using a canonical atlas-based
approach, previously reported in [61]. Each brain region from our
parcellation was spatially mapped onto the canonical Yeo 7-network atlas
in MNI space [62]. For each region, we calculated the fractional overlap
with each of the seven RSNs. The region was then assigned exclusively to
the RSN with which it had the highest fractional overlap. Support vector machine classiﬁcation
We trained an SVM classiﬁer to distinguish between subjects in each
group, using as input the perturbability maps. Subsequently, we assessed
classiﬁer performance using four distinct SVM linear models. These
classiﬁers were trained on different input data, speciﬁcally: functional
connectivity (FC) derived from empirical data, effective connectivity (EC)
computed within the optimised whole-brain model, FDT deviations, and a
combination of EC and FDT deviations. The distinct inputs were z-scored
I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

before being passed into the model. To ensure consistent input
dimensionality, we repeated the assessment of classiﬁer performance
using the four inputs, performing a Principal Component Analysis on each
and using the 10 ﬁrst principal components for the model. To further
assess the contribution of temporal dynamics, we implemented a sliding-
window approach (window size = 50 time points, overlap = 25) to
compute dynamic versions of FC, EC, and FDT. For each window, FC was
calculated directly, and whole-brain models were ﬁtted to estimate EC and
FDT deviations over time. PCA was again applied to the resulting dynamic
features, and the ﬁrst ten components were used for classiﬁcation. In all
cases, the training process involved utilizing 80% of the dataset, while the
accuracy was evaluated on the remaining 20% across 1000 k-folds. The
SVM used a linear kernel with automatic scaling and a box constraint of
2.5. Furthermore, a detailed analysis was conducted on the model
exhibiting the highest accuracy to comprehend its feature importance. This involved extracting the coefﬁcients of the model, sorting them from
highest to lowest, and selecting the top 5. These top coefﬁcients
correspond to speciﬁc nodes within the brain parcellation, elucidating
the signiﬁcant brain regions driving the classiﬁcation. Exploratory factor analysis
We follow the methodology in Schöttner et al. [63] to reduce the
dimensionality of our behavioral dataset. Using the “Factor Analyzer” package
implemented
in
Python
(https://github.com/EducationalTestingService/
factor_analyzer), we focus our analysis on variables from the Scale Analysis
of Positive Symptoms (SAPS) and Scale Analysis of Negative Symptoms (SANS)
that have less than 10% missing values. Prior to the analysis, all variables are
standardized (z-scored) across subjects. The “Factor Analyzer” package
facilitates dimensionality reduction by extracting underlying factors from
the dataset. This process results in the identiﬁcation of three factors, each
comprising loadings for individual variables and scores for each subject. These
factors represent distinct dimensions of symptomatology within our dataset. Statistical analysis
To gain insight into the differences in FDT deviation between individuals
with schizophrenia and the control cohort, we employ the non-parametric
independent-sample Mann-Whitney U test with 10000 permutations. To
understand the relationship between FDT deviation and symptom severity,
we conduct correlation analysis between the standard deviation of the FDT
deviation values across brain regions per subject and the scores obtained
in each factor. In all analyses, signiﬁcance is established for p-values below
0.05. For the analysis conducted between groups at the RSNs level and for
the correlations with the symptomatology, we implement the False
Discovery
Rate
(FDR)
correction
method
to
account
for
multiple
comparisons [64]. The p-values outlined are the ones obtained after FDR
correction. Preceding all the statistical analyses, outliers are excluded from
the comparison, with outliers deﬁned as data points deviating more than
three standard deviations from the mean. RESULTS
Our study applies a new model-based thermodynamic framework
that builds upon the FDT, offering a unique perspective on non-
equilibrium brain dynamics and, ultimately, to the hierarchical
organisation of the brain [44] (Fig. 1a). The FDT establishes a
relationship between the response of a perturbed system to an
external force and the internal ﬂuctuations of the same system in the
absence of the disturbance [46]. In a non-equilibrium system, these
intrinsic ﬂuctuations are inaccurate in predicting the dissipation post-
perturbation, leading to a violation of the FDT [45] (Fig. 1b). Hence,
an elevated deviation from the FDT signiﬁes a greater degree of non-
equilibrium, reﬂecting more asymmetric interactions between states
and, consequently, a heightened level of hierarchical organisation
[35, 44, 65, 66]. Building on this principle, our model-based FDT
framework combines empirical data and whole-brain modelling to
quantify perturbation responses (Fig. 1c). Hierarchical reconﬁguration across the whole-brain
We initially assessed the difference in hierarchical organisation
between schizophrenia and control groups at the whole-brain
level by leveraging the level of FDT deviations in each participant. At the whole-brain level, FDT deviation was signiﬁcantly increased
in schizophrenia patients compared to the healthy control group
(p < 0.01, median (interquartile range (IQR)) = schizophrenia =
39.75 (32.85), controls = 26.62 (23.74)), suggesting an overall
increase in hierarchical brain organisation in the disease (Fig. 2a). Additionally, we explored the hierarchical organisation for each
brain area instead of each subject, aiming to provide insights into
the speciﬁc regions implicated in the observed differences and
mitigate the potential confounding effects of individual variability. We computed the degree of FDT deviation for each brain area (i.e.,
for each group, the average of the perturbability map value across
all subjects for each brain region) (see Fig. 2b). Statistical
comparisons demonstrated a signiﬁcantly increased level of FDT
deviations in schizophrenia (p < 0.001, median (IQR): schizophre-
nia = 45.47 (14.78), controls = 34.72 (11.71)) (Fig. 2b). Subse-
quently, we examined the consistency of FDT deviation values
among brain areas within each group to determine whether the
elevated FDT deviation was associated with speciﬁc regions or
reﬂected a more generalized pattern. For this analysis, we
calculated the standard deviation (SD) of FDT deviation values
across all regions for each group, revealing higher statistically
signiﬁcant values in schizophrenia (p < 0.001, median (IQR):
schizophrenia = 35.54 (12.58), controls = 26.45 (15.09)) (Fig. 2c). This observation indicates that controls exhibit greater uniformity
in the deviation of FDT across brain areas, suggesting that the
increased whole-brain FDT values observed in schizophrenia may
stem from speciﬁc regions with notably higher FDT levels. This
localized elevation contributes to the increased variance observed
within the schizophrenia group. To further examine whether FDT deviation distinguishes
between schizophrenia subjects and controls, we developed a
support vector machine (SVM) classiﬁcation model. The model
was trained using the perturbability map of each subject as input
features and achieved an accuracy of 82.5% (Fig. 2d), indicating
that the hierarchical organisation can serve as a promising model-
based biomarker. Hierarchical reconﬁguration across resting-state networks
To investigate the localization of the alterations, we investigated
the FDT deviations across eight resting-state networks (RSNs): the
visual, somatomotor, dorsal attention, salience, limbic, control, DMN and subcortical networks. As in the whole-brain assessment,
we conducted the analysis both at the subject/single-participant
perspective and the brain region perspective. At the single-participant level, ﬁndings reveal a persistent
increased FDT deviation in schizophrenia across all RSNs (Fig. 3a). Statistically signiﬁcant differences emerge in the, somatomotor
(p < 0.01), dorsal attention (p < 0.01), limbic (p < 0.001), control
(p < 0.01), DMN (p < 0.05) and subcortical (p < 0.01) networks. However, no signiﬁcance is found in the salience (p > 0.05) and
visual (p > 0.05) networks. All reported p-values were corrected for
multiple comparisons using FDR correction (see Supplementary
Table 1). At the brain area level, results also indicate a consistent pattern
of elevated FDT deviation within schizophrenia across all RSNs
(Fig. 3b). Notably, statistically signiﬁcant differences appear in the
somatomotor
(p < 0.01),
dorsal
attention
(p < 0.05),
salience
(p < 0.05), limbic (p < 0.01), control (p < 0.01), DMN (p < 0.05) and
subcortical (p < 0.01) networks. Results do not indicate signiﬁ-
cance in the visual network (p > 0.05). All signiﬁcant p-values
persist following FDR correction for multiple comparisons (see
Supplementary Table 2). We represented the mean FDT deviation values of all subjects
for each RSN and each group on a uniform scale, aiming to
identify the regions with the largest differences in hierarchical
organisation between the two groups (Fig. 3c). The ﬁndings
indicate that the regions orchestrating the changes in hierarchical
conﬁguration are the somatomotor (standardized mean difference
I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

(SMD) = 0.67), the subcortical (SMD = 0.60) and the limbic (SMD =
0.57) networks, followed by the control (SMD = 0.51), the salience
(SMD = 0.45), the DMN (SMD = 0.44), the dorsal attention (SMD =
0.27) and ﬁnally the visual (SMD = 0.21) network (see Supple-
mentary Table 3). Hierarchical reconﬁguration correlates with symptom severity
Next, we explored the potential correlation between the
changes of the hierarchical organisation in schizophrenia and
speciﬁc symptoms. We employed exploratory factor analysis to
reduce the dimensionality of the symptom’s data from 58 to 3
factors. The analysis revealed a positive signiﬁcant correlation
between the standard deviation of each subject brain region’s
FDT deviations and Factor 1 (related to negative symptoms)
(r = 0.32, p < 0.05), a negative signiﬁcant correlation with Factor
3 (associated with features of positive formal thought disorder
and apathy) (r = −0.31, p < 0.05), but no signiﬁcant correlation
with Factor 2 (characterized by positive symptoms) (r = −0.27, Fig. 1
Capturing the hierarchical organisation using the FDT. a Hierarchical level is determined by the level of asymmetry of causal
interactions between brain regions arising from the breaking of the detailed balance in a system. In equilibrium, the interaction of brain
regions is symmetrical, that is, information ﬂows in a reciprocal manner. These symmetrical relationships are in detailed balance, leading to a
non-hierarchical organisation. In contrast, in non-equilibrium, the asymmetrical interactions break the detailed balance, introducing
hierarchical organisation in the system. b The level of non-equilibrium can be measured by the deviation of FDT, which can then be employed
to characterize the hierarchical organisation. In an equilibrium system, spontaneous ﬂuctuations predict the dissipation following the
perturbation. Nevertheless, in a non-equilibrium system, the intrinsic ﬂuctuations are not able to forecast the dissipation after a perturbation,
leading to a violation of the FDT. c FDT is combined with a whole-brain model ﬁtted to empirical neuroimaging data, incorporating functional
and structural connectivity. Each node’s local dynamics of the model is described as the normal form of a supercritical Hopf bifurcation. The
optimised model provides the effective connectivity, the FDT deviations as well as the perturbability maps for different brain states. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

p > 0.05) (Fig. 4). The reported p-values are the ones obtained
after correcting for multiple comparisons using FDR. Addition-
ally, we examined the correlation between the average FDT
deviation and each of the three symptom factors. These
analyses
did
not
reveal
any
signiﬁcant
associations
(all
p-values > 0.05). To further explore these relationships, we performed an
analysis of hierarchical organisation in brain areas associated
with each symptom factor. For each factor identiﬁed through
dimensionality reduction, we compared the perturbability maps
of subjects with high and low factor scores to identify brain areas
with the largest differences in hierarchical organisation. Subjects
were split based on the median: those with scores below the
median were classiﬁed as having low factor scores, while those
with scores above the median were classiﬁed as having high
factor scores. For Factor 1 (negative symptoms), the most
signiﬁcant changes in hierarchical organisation were observed
in the subcortical network, with contributions from the visual and
somatomotor networks. For Factor 2 (positive symptoms), the
most prominent differences were found in the limbic and
subcortical networks. Lastly, for Factor 3 (formal thought disorder
and apathy), the most notable changes were observed in the
limbic network (Supplementary Table 6). These ﬁndings suggest
that different symptom dimensions in schizophrenia are asso-
ciated with distinct patterns of hierarchical organisation in
speciﬁc brain networks. Hierarchical reconﬁguration can classify between individuals
with schizophrenia and controls
We determined whether differences in brain dynamics between
schizophrenia and controls can be more effectively explained due to
changes in brain hierarchy (as reﬂected in FDT deviations) or by other
functional metrics in the literature (Functional Connectivity (FC) and
Effective Connectivity (EC)). We trained an SVM classiﬁer using the FC,
the EC, the FDT deviations and a combination of EC and FDT (EC + FDT)
as input. Our results indicate that the FDT input, together with the
combination of EC + FDT inputs, achieve the highest accuracy among
the classiﬁers (82.5 and 81.5%, respectively), surpassing the 73%
obtained using EC and the 60% obtained using FC (Fig. 5). Furthermore,
we repeated the same analysis ensuring the same number of input
features for each model. For that, we performed a Principal Component
Analysis and used the ﬁrst ten principal components for the SVM
classiﬁers (Supplementary Fig. 2). These results follow the same trend of
performance as the full-dimensional inputs, with the highest accuracy
obtained in the FDT and EC + FDT inputs (76 and 73.5%, respectively),
followed by the EC (65%) and the FC (60.5%). Additionally, to assess
whether incorporating temporal dynamics could further improve
classiﬁcation, we repeated the SVM analysis using features extracted
through a sliding-window approach. For each window, we computed
FC and estimated the corresponding whole-brain model to derive EC
and FDT deviations, resulting in dynamic representations of all metrics. A PCA was again applied to reduce dimensionality, and the ﬁrst ten
components were used in the SVM. The results (Supplementary Fig. 3)
Fig. 2
In schizophrenia, the hierarchical organisation increases as shown by the increase in FDT deviation values across the whole-brain. Analysis of the whole-brain FDT deviation values between schizophrenia and control patients, to understand differences in hierarchical brain
organisation. a Boxplots illustrate the distribution of the average FDT values per subject b Boxplots show the distribution of the average FDT
values per node, obtained by averaging each brain area in the perturbability map across subjects. c Boxplots depict the distribution of the
standard deviation of the perturbability mapacross nodes. d The violin plot displays the distribution of the support vector machine model’s
accuracy across 1000 k-folds using the perturbability map of each subject as input. e Brain renders represent the spatial distribution of the
average FDT values per node for each group. Asterisks in the ﬁgure indicate statistical signiﬁcance: ** represents p < 0.01 and *** represents
p < 0.001. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

Fig. 3
Increased hierarchical organisation in some schizophrenia RSNs. Comparison of FDT deviation values between schizophrenia and
control groups to identify the networks contributing to the difference in hierarchical organisation. a Boxplots illustrate the distribution of the
average FDT values per subject for each RSN. b Boxplots illustrate the distribution of the average FDT values per node for each RSN. c Radar
plot shows the mean FDT values per RSN for each group on the same scale, complemented with a brain render highlighting in orange the
area of the corresponding network. All the reported p-values were corrected for multiple comparisons. * represents p < 0.05, ** represents
p < 0.01 and *** represents p < 0.001. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

showed consistent trends with the static analysis, with dynamic FDT
and EC + FDT inputs achieving the highest classiﬁcation accuracies (88
and 88.5%, respectively), supporting the relevance of hierarchical
dynamics in distinguishing schizophrenia from controls. Finally, focusing on the EC + FDT and FDT SVM models, we
conducted an in-depth analysis by identifying the top 5 most
inﬂuential features for the classiﬁcation, corresponding to the
highest coefﬁcients of the model (Table 1). These nodes are
primarily located within the subcortical and limbic networks,
being these the regions previously reported to show most of the
signiﬁcant differences between the two groups (Fig. 3c, Supple-
mentary Table 3). Moreover, the DMN and visual networks also
appear to be highly important for the classiﬁcation. DISCUSSION
We integrated a whole-brain computational model with the
ﬂuctuation-dissipation theorem (FDT) to investigate whether the
brain’s
hierarchical
organisation
differs
in
patients
with
schizophrenia, using FDT deviations as a metric of hierarchy. Our
analysis revealed consistently heightened organisation in schizo-
phrenia, with signiﬁcant differences observed in the somatomotor,
dorsal attention, salience, limbic, control, DMN and subcortical
networks. Moreover, these changes correlated with the severity of
formal thought disorder, negative and positive symptoms. Finally,
an SVM model demonstrated that including FDT in the input
features allows for superior classiﬁcation of schizophrenia patients
versus controls. At the whole-brain level, we found increased FDT deviation in
schizophrenia. A deviation from the FDT is characteristic of a
system departing from the equilibrium [45, 46], which is deﬁned
by asymmetrical interactions between its components and a
hierarchically organised structure [29, 65]. Increased FDT deviation
suggests
an
elevated
level
of
non-equilibrium
and
more
hierarchically organised brain dynamics in schizophrenia com-
pared to controls, suggesting a stronger contribution of top-down
processing [29]. Furthermore, our ﬁndings indicate increased
variability of FDT deviation across nodes in schizophrenia, aligning
Fig. 4
The variability of the hierarchical organisation in schizophrenia correlates with symptom severity. Exploration of the correlation
between the standard deviation of FDT deviation across brain regions in each subject and their symptomatology items evaluated using the
SAPS and SANS scales. a Loading matrix of the three-factor solution derived from the exploratory factor analysis, including SAPS and SANS
variables. Each row indicates an item on the scales. Interestingly, Factor 1 shows strong values for the SANS variables, Factor 2 for the SAPS,
and Factor 3 for positive formal thought disorder and avolition/apathy items. b Correlation between the factor scores of each subject and
standard deviation of their FDT deviation values. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

with previous research indicating that higher neural heterogeneity
is a general characteristic of mental illness [67]. This adds to the
growing evidence that psychiatric disorders exhibit greater
heterogeneity,
reinforcing
the
need
for
transdiagnostic
approaches in mental health research. Speciﬁcally, we found that
the higher levels of the hierarchy are occupied by the limbic,
subcortical, DMN and control networks. These areas exhibit
greater inﬂuence over the other RSNs, driving the orchestration
and organising the functional dynamics to a higher extent than
controls. Previous studies have also shown differences in the whole-brain
hierarchical organisation of networks in schizophrenia [38, 39],
while others have highlighted reduced hierarchical organisation
[29, 68]. This apparent discrepancy with our ﬁndings, which
indicate increased hierarchical organisation, may stem from
differences in the data and methods used to compute hierarchy. Speciﬁcally, Dong et al. [68] estimated hierarchy based on FC,
which captures undirected statistical dependencies between brain
regions. In contrast, our analysis relies on EC, which incorporates
the directionality of interactions, potentially providing a different
perspective on hierarchical organisation. Regarding the other
study reporting reduced hierarchy [33], the authors approached
the analysis from a non-stationarity perspective. They segmented
each subject’s data into multiple short time windows, thus
combining hierarchical metrics with dynamic changes over time. Although they found signiﬁcant group differences, these were
relatively small, likely due to the windowing approach, compared
to our analysis, where we leverage the entire time series for each
subject. Notably, a previous study found that the connectivity between
the DMN with other regions was more consistently present in
individuals with schizophrenia than controls [69]. Moreover, Yang
et al. [37] demonstrated that higher functional hierarchy in the
DMN underlies the persistently observed elevated FC in studies of
schizophrenia [17, 70, 71]. Increased connectivity between DMN
and both the somatomotor and visual networks was also reported
in [72]. This goes in line with our outcomes, emphasizing the
important role of this network in schizophrenia Regarding the
subcortical
network, Yang
et
al.
[73]
identiﬁed
functional
subcortical hierarchy disorganisation in drug-naïve schizophrenia
patients, which normalized after antipsychotic treatment. Addi-
tionally, Sabaroedin et al. [74] reported dysconnectivity within the
subcortex in ﬁrst-episode psychosis patients, which later extended
to dysconnectivity between the cortex and subcortical systems in
established schizophrenia. These ﬁndings are consistent with our
results, emphasizing the involvement of the subcortical network in
the disease. For the limbic and control networks, Xiang et al. [75]
investigated functional gradients in schizophrenia, which have
been
proposed
as
a
measure
of hierarchical
organisation. Interestingly, they found increased gradient scores in the limbic,
control, and DMN networks, alongside decreases in the visual and
somatomotor networks, ﬁndings that closely align with our results. Fig. 5
Including hierarchical organisation features in a Support Vector Machine classiﬁcation yields better accuracy than traditional
functional or effective connectivity features. Comparison of the accuracy obtained using a SVM algorithm with different inputs (FC, EC, FDT
and EC + FDT) to identify the most informative metrics. a Violin plots display the distribution of SVM accuracy across 1000 k-folds using FC, EC, FDT and EC + FDT data as inputs. b Confusion matrices illustrate the overall accuracy achieved corresponding to the distributions in (a),
presented as percentages represented on a color scale. P stands for positive, N for negative. Table 1. Subcortical, visual, limbic, and default mode regions are the most inﬂuential for accurate classiﬁcation. Node name
Corresponding RSN
Node name
Corresponding RSN
right inferior temporal
Limbic
right pericalcarine
Visual
right globus pallidus internus
Subcortical
right inferior temporal
Limbic
left nucleus accumbens
Subcortical
left pars orbitalis
DMN
right pericalcarine
Visual
right pericalcarine
Visual
right amygdala
Subcortical
right globus pallidus internus
Subcortical
This table presents the top 5 most important features obtained through SVM classiﬁcation of the best performing models, indicating the relevance of speciﬁc
nodes and their corresponding RSN, sorted in descending order. The higher the feature in the table, the greater the signiﬁcance of the node in classiﬁcation. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

Our ﬁndings highlight correlations between the variability in
hierarchical organisation in individuals with schizophrenia and
the severity of negative symptoms, positive formal thought
disorder and apathy. Previous studies have reported correlations
between changes in DMN connectivity and negative symptoms
[76, 77]. Hierarchical changes within this network could be
affecting processes such as self-referential thinking and intro-
spective cognition. Additionally, research has indicated that the
somatomotor network can also impact negative symptoms [78]. Alterations in its hierarchical organisation could impact motor
planning and execution, contributing to symptoms such as
psychomotor retardation and speech abnormalities. Further-
more, dysregulation of the salience network has been associated
with negative symptoms and motivational deﬁcits in schizo-
phrenia [16, 79], potentially leading to apathy and reduced
responsiveness to environmental cues. These ﬁndings are
consistent with our outcomes, suggesting that alterations in
the hierarchical organisation of speciﬁc networks may underlie
the manifestation of symptoms commonly observed in the
disease. Notably, we also assessed whether the average FDT
deviation across regions was associated with symptom severity
but found no signiﬁcant correlations (all p-values > 0.05). This
lack of association may reﬂect the fact that averaging can
obscure
region-speciﬁc
effects,
as
deviations
in
opposite
directions across different brain areas may cancel each other
out. In contrast, the variability in FDT captures the degree of
imbalance across regions, which appears to be more relevant for
symptom expression. Finally, we employed a machine learning classiﬁcation model to
evaluate whether the differences in brain dynamics between
schizophrenia and controls are better captured by alterations in
brain hierarchy or by other functional metrics, such as FC and EC. The
model demonstrated the highest performance when trained with
FDT deviation features, being FDT alone or in combination with EC. This result suggests that disruptions in the hierarchical organisation
of brain dynamics, as measured by FDT deviations, play a critical role
in distinguishing individuals with schizophrenia from controls and
provide more informative features than FC or EC alone. Beyond the
previously reported networks to show the greatest differences
between the two groups, the model also underscored the relevance
of the visual and DMN networks, which were not prominently
identiﬁed in the previous statistical analysis. This underscores the
complementary nature of machine learning approaches in identify-
ing patterns that may elude traditional statistical methods. Our results are potentially compatible with shifts in the balance
between excitation (E) and inhibition (I) mediated by NMDA
receptor
hypofunction
implicated
in
schizophrenia
[80–82]. Interestingly, previous research in primates using computational
models proposed that variations in local recurrent excitation
strength at different hierarchical levels account for the observed
differences in neural activity time-scales across cortical regions
[83–85]. To
bridge
between
functional
neuroimaging
and
neuronal-level alterations, a previous study constructed a biophy-
sical model integrating the hierarchical brain organisation and E/I
perturbations, which was able to predict the brain dynamics
observed in the disease [37]. Moreover, Brau et al. [86] observed
the effects of an NMDA antagonist in healthy controls, which led
to increased network ﬂexibility (i.e., higher reconﬁguration of brain
networks). Also using an NMDA antagonist for anaesthesia, Deco
et al. [33] predicted heightened hierarchy in primates compared to
their awake state. As a future step, it would be valuable to extend
our framework by including receptor maps, such as in [87, 88], to
obtain a deeper and more precise understanding of our ﬁndings. Another possible link of our ﬁndings of disrupted hierarchical
organisation in schizophrenia is with theories of impaired
predictive coding. Predictive coding is inherently hierarchical,
involving the interplay between top-down expectations and
bottom-up sensory inputs to minimize prediction errors [89]. Deﬁcits in this process, such as altered precision weighting of
sensory information and predictions, have been implicated in
schizophrenia symptomatology, including delusional thoughts
[90], hallucinations [91] and altered sense of agency [92]. Although
we do not directly measure predictive coding mechanisms, the
patterns of functional hierarchy disruption and their correlation
with clinical symptoms suggest that these mechanisms might be
interconnected. This is because hierarchical organisation reﬂects
how information is integrated and propagated across brain
regions, and disruptions here could lead to improper balancing
of sensory evidence and prior expectations, a core aspect of
predictive coding dysfunction in schizophrenia. The current study has several limitations. First, although
consistent with comparable studies in the ﬁeld [93, 94], the
dataset analysed in this study is relatively small. Second, a
potential limitation arises from the conceivable inﬂuence of
medication on brain dynamics, which could impact the observed
brain activity and subsequent results [95]. Third, in the parcella-
tion employed in the analysis (i.e., the DK80 atlas [52]), the dorsal
attention network is constituted by only two nodes and, thus, we
refrain from making detailed interpretations when comparing
groups by nodes. Finally, another limitation is that the SC matrix
was derived from a separate normative sample of healthy
participants, rather than from the same individuals in the main
analysis. This approach, consistent with prior work [96, 97], was
necessary due to the unavailability of subject-speciﬁc diffusion
data. Importantly, EC was individually optimized for each
participant, allowing the model to capture subject-speciﬁc
dynamics and reduce potential biases from using normative SC. In summary, we used a computational whole-brain model and
the violations of the FDT and found elevated hierarchical brain
organisation in schizophrenia compared to controls both across
the whole-brain and RSNs. Furthermore, we found that the
changes in hierarchy are correlated with negative symptoms,
positive formal thought disorder and apathy. Finally, through SVM
classiﬁcation, we demonstrated that including FDT deviations in
the
input
resulted
in
superior
classiﬁcation
accuracy
than
individual metrics (i.e., FC, EC). Overall, this framework can be
potentially used as a model-based biomarker to differentiate
schizophrenia from healthy controls. Importantly, this inquiry is
not limited to schizophrenia alone but opens up broader
perspectives for understanding the hierarchical brain organisation
of other psychiatric conditions and different brain states.

## DATA AVAILABILITY

Raw data are available at openneuro.org/datasets/ds000030/. Preprocessed data and
scripts are available upon request.

## CODE AVAILABILITY

Code used to analyse the data is available from https://github.com/Irenacero/
FDT_schizophrenia.git. REFERENCES

### 1. Kay SR, Fiszbein A, Opler LA. The positive and negative syndrome scale (PANSS)

for schizophrenia. Schizophr Bull. 1987;13:261–76.

### 2. Mueser KT, McGurk SR. Schizophrenia. Lancet. 2004;363:2063–72.

### 3. Glahn DC, Laird AR, Ellison-Wright I, Thelen SM, Robinson JL, Lancaster JL, et al. Meta-analysis of gray matter anomalies in schizophrenia: application of anatomic
likelihood estimation and network analysis. Biol Psychiatry. 2008;64:774–81.

### 4. Kubicki M, McCarley RW, Shenton ME. Evidence for white matter abnormalities in

schizophrenia. Curr Opin Psychiatry. 2005;18:121–34.

### 5. Chan RC, Di X, McAlonan GM, Gong QY. Brain anatomical abnormalities in high-

risk individuals, ﬁrst-episode, and chronic schizophrenia: an activation likelihood
estimation meta-analysis of illness progression. Schizophr Bull. 2011;37:177–88.

### 6. Davidson LL, Heinrichs RW. Quantiﬁcation of frontal and temporal lobe brain-

imaging ﬁndings in schizophrenia: a meta-analysis. Psychiatry Res. 2003;122:69–87. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

### 7. Honea R, Crow TJ, Passingham D, Mackay CE. Regional deﬁcits in brain volume in

schizophrenia: a meta-analysis of voxel-based morphometry studies. Am J Psy-
chiatry. 2005;162:2233–45.

### 8. Bora E, Fornito A, Radua J, Walterfang M, Seal M, Wood SJ, et al. Neuroanatomical

abnormalities in schizophrenia: a multimodal voxelwise meta-analysis and meta-
regression analysis. Schizophr Res. 2011;127:46–57.

### 9. Ellison-Wright I, Bullmore E. Anatomy of bipolar disorder and schizophrenia: a

meta-analysis. Schizophr Res. 2010;117:1–12.

### 10. Adriano F, Spoletini I, Caltagirone C, Spalletta G. Updated meta-analyses reveal

thalamus volume reduction in patients with ﬁrst-episode and chronic schizo-
phrenia. Schizophr Res. 2010;123:1–14.

### 11. Wylie KP, Tregellas JR. The role of the insula in schizophrenia. Schizophr Res.

2010;123:93–104.

### 12. Di X, Chan RC, Gong QY. White matter reduction in patients with schizophrenia as

revealed by voxel-based morphometry: an activation likelihood estimation meta-
analysis. Prog Neuropsychopharmacol Biol Psychiatry. 2009;33:1390–4.

### 13. Smitha KA, Akhil Raja K, Arun KM, Rajesh PG, Thomas B, Kapilamoorthy TR, et al. Resting state fMRI: a review on methods in resting state connectivity analysis and
resting state networks. Neuroradiol J. 2017;30:305–17.

### 14. Filippi M, Spinelli EG, Cividini C, Agosta F. Resting state dynamic functional

connectivity in neurodegenerative conditions: a review of magnetic resonance
imaging ﬁndings. Front Neurosci. 2019;13:657.

### 15. Bressler SL, Menon V. Large-scale brain networks in cognition: emerging methods

and principles. Trends Cogn Sci. 2010;14:277–90.

### 16. Palaniyappan L, Liddle PF. Does the salience network play a cardinal role in

psychosis? An emerging hypothesis of insular dysfunction. J Psychiatry Neurosci.
2012;37:17–27.

### 17. Zhou Y, Liang M, Tian L, Wang K, Hao Y, Liu H, et al. Functional disintegration in

paranoid schizophrenia using resting-state fMRI. Schizophr Res. 2007;97:194–205.

### 18. Whitﬁeld-Gabrieli S, Thermenos HW, Milanovic S, Tsuang MT, Faraone SV, McCarley RW, et al. Hyperactivity and hyperconnectivity of the default network in
schizophrenia and in ﬁrst-degree relatives of persons with schizophrenia. Proc
Natl Acad Sci USA. 2009;106:1279–84.

### 19. Camchong J, MacDonald AW 3rd, Bell C, Mueller BA, Lim KO. Altered functional

and anatomical connectivity in schizophrenia. Schizophr Bull. 2011;37:640–50.

### 20. Dong D, Wang Y, Chang X, Luo C, Yao D. Dysfunction of large-scale brain net-

works in schizophrenia: a meta-analysis of resting-state functional connectivity. Schizophr Bull. 2018;44:168–81.

### 21. Penadés R, Segura B, Inguanzo A, García-Rizo C, Catalán R, Masana G, et al. Cognitive remediation and brain connectivity: a resting-state fMRI study in
patients with schizophrenia. Psychiatry Res Neuroimaging. 2020;303:111140.

### 22. Jia Y, Gu H-G. Identifying nonlinear dynamics of brain functional networks of

patients with schizophrenia by sample entropy. Nonlinear Dynamics. 2019;96:
2327–40.

### 23. Tandon R, Nasrallah H, Akbarian S, Carpenter WT Jr, DeLisi LE, Gaebel W, et al. The

schizophrenia syndrome, circa 2024: what we know and how that informs its
nature. Schizophr Res. 2024;264:1–28.

### 24. Braff DL. Information processing and attention dysfunctions in schizophrenia. Schizophr Bull. 1993;19:233–59.

### 25. Rubinov M, Bullmore E. Schizophrenia and abnormal brain network hubs. Dia-

logues Clin Neurosci. 2013;15:339–49.

### 26. Chen Y. Abnormal visual motion processing in schizophrenia: a review of

research progress. Schizophr Bull. 2011;37:709–15.

### 27. Iglesias-Parro S, Ruiz de Miras J, Soriano MF, Ibáñez-Molina AJ. Integration-

segregation dynamics in functional networks of individuals diagnosed with
schizophrenia. Eur J Neurosci. 2023;57:1748–62.

### 28. Kringelbach ML, Sanz Perl Y, Deco G. The thermodynamics of mind. Trends Cogn

Sci. 2024;28:568–81.

### 29. Deco G, Sanz Perl Y, de la Fuente L, Sitt JD, Yeo BTT, Tagliazucchi E, et al. The

arrow of time of brain signals in cognition: potential intriguing role of parts of the
default mode network. Netw Neurosci. 2023;7:966–98.

### 30. Huntenburg JM, Bazin PL, Margulies DS. Large-scale gradients in human cortical

organization. Trends Cogn Sci. 2018;22:21–31.

### 31. Taylor P, Hobbs JN, Burroni J, Siegelmann HT. The global landscape of cognition:

hierarchical aggregation as an organizational principle of human cortical net-
works and functions. Sci Rep. 2015;5:18112.

### 32. Sanz Perl Y, Bocaccio H, Pallavicini C, Pérez-Ipiña I, Laureys S, Laufs H, et al. Nonequilibrium brain dynamics as a signature of consciousness. Phys Rev E.
2021;104:014411.

### 33. Deco G, Sanz Perl Y, Bocaccio H, Tagliazucchi E, Kringelbach ML. The INSIDEOUT

framework provides precise signatures of the balance of intrinsic and extrinsic
dynamics in brain states. Commun Biol. 2022;5:572.

### 34. Kringelbach ML, Perl YS, Tagliazucchi E, Deco G. Toward naturalistic neuroscience:

mechanisms underlying the ﬂattening of brain hierarchy in movie-watching
compared to rest and task. Sci Adv. 2023;9:eade6049.

### 35. Lynn CW, Cornblath EJ, Papadopoulos L, Bertolero MA, Bassett DS. Broken

detailed balance and entropy production in the human brain. Proc Natl Acad Sci
USA. 2021;118:e2109889118.

### 36. Lynall ME, Bassett DS, Kerwin R, McKenna PJ, Kitzbichler M, Muller U, et al. Functional connectivity and brain networks in schizophrenia. J Neurosci.
2010;30:9477–87.

### 37. Yang GJ, Murray JD, Wang XJ, Glahn DC, Pearlson GD, Repovs G, et al. Functional

hierarchy underlies preferential connectivity disturbances in schizophrenia. Proc
Natl Acad Sci USA. 2016;113: E219–28.

### 38. Wengler K, Goldberg AT, Chahine G, Horga G. Distinct hierarchical alterations of

intrinsic neural timescales account for different manifestations of psychosis. Elife.
2020;9:e56151.

### 39. Mastrandrea R, Piras F, Gabrielli A, Banaj N, Caldarelli G, Spalletta G, et al. The

unbalanced reorganization of weaker functional connections induces the altered
brain network topology in schizophrenia. Sci Rep. 2021;11:15400.

### 40. Dickie EW, Shahab S, Hawco C, Miranda D, Herman G, Argyelan M, et al. Robust

hierarchically organized whole-brain patterns of dysconnectivity in schizophrenia
spectrum disorders observed after personalized intrinsic network topography. Hum Brain Mapp. 2023;44:5153–66.

### 41. Barbalat G, Chambon V, Domenech PJ, Ody C, Koechlin E, Franck N, et al. Impaired hierarchical control within the lateral prefrontal cortex in schizophrenia. Biol Psychiatry. 2011;70:73–80.

### 42. Holmes A, Levi PT, Chen YC, Chopra S, Aquino KM, Pang JC, et al. Disruptions of

hierarchical cortical organization in early psychosis and schizophrenia. Biol Psy-
chiatry Cogn Neurosci Neuroimaging. 2023;8:1240–50.

### 43. Dong D, Yao D, Wang Y, Hong SJ, Genon S, Xin F, et al. Compressed sensorimotor-

to-transmodal
hierarchical
organization
in
schizophrenia. Psychol
Med.
2023;53:771–84.

### 44. Deco G, Lynn CW, Sanz Perl Y, Kringelbach ML. Violations of the ﬂuctuation-

dissipation theorem reveal distinct nonequilibrium dynamics of brain states. Phys
Rev E. 2023;108:064410.

### 45. Onsager L. Reciprocal relations in irreversible processes. I. Physical Review.

1931;37:405–26.

### 46. Kubo R. The Fluctuation-dissipation theorem. Reports on Progress in Physics.

2002;29:255.

### 47. Bilder R, Poldrack R, Cannon T, London E, Freimer N, Congdon E, et al. UCLA

consortium for neuropsychiatric phenomics LA5c study. OpenNeuro; 2018.

### 48. Poldrack RA, Congdon E, Triplett W, Gorgolewski KJ, Karlsgodt KH, Mumford JA,

et al. A phenome-wide examination of neural and cognitive function. Sci Data.
2016;3:160110.

### 49. Esteban O, Markiewicz CJ, Blair RW, Moodie CA, Isik AI, Erramuzpe A, et al.

fMRIPrep: a robust preprocessing pipeline for functional MRI. Nat Methods.
2019;16:111–6.

### 50. Gorgolewski K, Burns CD, Madison C, Clark D, Halchenko YO, Waskom ML, et al. Nipype: a ﬂexible, lightweight and extensible neuroimaging data processing
framework in python. Front Neuroinform. 2011;5:13.

### 51. Pruim RHR, Mennes M, van Rooij D, Llera A, Buitelaar JK, Beckmann CF. ICA-

AROMA: a robust ICA-based strategy for removing motion artifacts from fMRI
data. Neuroimage. 2015;112:267–77.

### 52. Deco G, Vidaurre D, Kringelbach ML. Revisiting the global workspace orches-

trating the hierarchical organization of the human brain. Nat Hum Behav.
2021;5:497–511.

### 53. Thomas C, Ye FQ, Irfanoglu MO, Modi P, Saleem KS, Leopold DA, et al. Anatomical

accuracy of brain connections derived from diffusion MRI tractography is
inherently limited. Proc Natl Acad Sci USA. 2014;111:16574–9.

### 54. Horn A, Neumann WJ, Degen K, Schneider GH, Kühn AA. Toward an electro-

physiological “sweet spot” for deep brain stimulation in the subthalamic nucleus. Hum Brain Mapp. 2017;38:3377–90.

### 55. Horn A, Blankenburg F. Toward a standardized structural-functional group con-

nectome in MNI space. Neuroimage. 2016;124:310–22.

### 56. Schilling KG, Daducci A, Maier-Hein K, Poupon C, Houde JC, Nath V, et al. Chal-

lenges in diffusion MRI tractography - lessons learned from international
benchmark competitions. Magn Reson Imaging. 2019;57:194–209.

### 57. Maier-Hein KH, Neher PF, Houde JC, Côté MA, Garyfallidis E, Zhong J, et al. Author

correction: the challenge of mapping the human connectome based on diffusion
tractography. Nat Commun. 2019;10:5059.

### 58. Crisanti A, Ritort F. Violation of the ﬂuctuation–dissipation theorem in glassy

systems: basic notions and the numerical evidence. J Phys A: Math Gen.
2003;36: R181–R290.

### 59. Deco G, Kringelbach ML, Jirsa VK, Ritter P. The dynamics of resting ﬂuctuations

in
the
brain:
metastability
and
its
dynamical
cortical
core. Sci
Rep.
2017;7:3095.

### 60. Deco G, Ponce-Alvarez A, Hagmann P, Romani GL, Mantini D, Corbetta M. How

local excitation-inhibition ratio impacts the whole brain dynamics. J Neurosci.
2014;34:7886–98. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

### 61. Lord LD, Expert P, Atasoy S, Roseman L, Rapuano K, Lambiotte R, et al. Dynamical

exploration of the repertoire of brain networks at rest is modulated by psilocybin. Neuroimage. 2019;199:127–42.

### 62. Yeo BT, Krienen FM, Sepulcre J, Sabuncu MR, Lashkari D, Hollinshead M, et al. The

organization of the human cerebral cortex estimated by intrinsic functional
connectivity. J Neurophysiol. 2011;106:1125–65.

### 63. Schöttner M, Bolton TAW, Patel J, Nahálka AT, Vieira S, Hagmann P. Exploring the

latent structure of behavior using the Human Connectome Project’s data. Sci Rep.
2023;13:713.

### 64. Hochberg Y, Benjamini Y. More powerful procedures for multiple signiﬁcance

testing. Stat Med. 1990;9:811–8.
65. de la Fuente LA, Zamberlan F, Bocaccio H, Kringelbach M, Deco G, Perl YS, et al. Temporal irreversibility of neural dynamics as a signature of consciousness. Cereb
Cortex. 2023;33:1856–65.

### 66. Aguilera M, Igarashi M, Shimazaki H. Nonequilibrium thermodynamics of the

asymmetric Sherrington-Kirkpatrick model. Nat Commun. 2023;14:3685.

### 67. Segal A, Parkes L, Aquino K, Kia SM, Wolfers T, Franke B, et al. Regional, circuit and

network heterogeneity of brain abnormalities in psychiatric disorders. Nat Neu-
rosci. 2023;26:1613–29.

### 68. Dong D, Luo C, Guell X, Wang Y, He H, Duan M, et al. Compression of cerebellar

functional gradients in schizophrenia. Schizophr Bull. 2020;46:1282–95.

### 69. Jafri MJ, Pearlson GD, Stevens M, Calhoun VD. A method for functional network

connectivity among spatially independent resting-state components in schizo-
phrenia. Neuroimage. 2008;39:1666–81.

### 70. Liu H, Kaneko Y, Ouyang X, Li L, Hao Y, Chen EY, et al. Schizophrenic patients and

their unaffected siblings share increased resting-state connectivity in the task-
negative network but not its anticorrelated task-positive network. Schizophr Bull.
2012;38:285–94.

### 71. Hu ML, Zong XF, Mann JJ, Zheng JJ, Liao YH, Li ZC, et al. A review of the

functional and anatomical default mode network in schizophrenia. Neurosci Bull.
2017;33:73–84.

### 72. Orliac F, Delamillieure P, Delcroix N, Naveau M, Brazo P, Razaﬁmandimby A, et al. Network modeling of resting state connectivity points towards the bottom up
theories of schizophrenia. Psychiatry Res Neuroimaging. 2017;266:19–26.

### 73. Yang C, Zhang W, Liu J, Yao L, Bishop JR, Lencer R, et al. Disrupted subcortical

functional connectome gradient in drug-naïve ﬁrst-episode schizophrenia and
the normalization effects after antipsychotic treatment. Neuropsychopharma-
cology. 2023;48:789–96.

### 74. Sabaroedin K, Razi A, Chopra S, Tran N, Pozaruk A, Chen Z, et al. Frontos-

triatothalamic effective connectivity and dopaminergic function in the psychosis
continuum. Brain. 2023;146:372–86.

### 75. Xiang J, Ma C, Chen X, Cheng C. Investigating connectivity gradients in schizo-

phrenia: integrating functional, structural, and genetic perspectives. Brain Sci.
2025;15:179.

### 76. Hare SM, Ford JM, Mathalon DH, Damaraju E, Bustillo J, Belger A, et al. Salience-

default mode functional network connectivity linked to positive and negative
symptoms of schizophrenia. Schizophr Bull. 2019;45:892–901.

### 77. Wang X, Chang Z, Wang R. Opposite effects of positive and negative symptoms

on resting-state brain networks in schizophrenia. Commun Biol. 2023;6:279.

### 78. Bernard JA, Goen JRM, Maldonado T. A case for motor network contributions to

schizophrenia symptoms: evidence from resting-state connectivity. Hum Brain
Mapp. 2017;38:4535–45.

### 79. Menon V. Large-scale brain networks and psychopathology: a unifying triple

network model. Trends Cogn Sci. 2011;15:483–506.

### 80. Uhlhaas PJ, Singer W. Abnormal neural oscillations and synchrony in schizo-

phrenia. Nat Rev Neurosci. 2010;11:100–13.

### 81. Jardri R, Denève S. Circular inferences in schizophrenia. Brain. 2013;136:3227–41.

### 82. Schobel SA, Chaudhury NH, Khan UA, Paniagua B, Styner MA, Asllani I, et al. Imaging patients with psychosis and a mouse model establishes a spreading
pattern of hippocampal dysfunction and implicates glutamate as a driver. Neu-
ron. 2013;78:81–93.

### 83. Wang XJ. Synaptic reverberation underlying mnemonic persistent activity. Trends

Neurosci. 2001;24:455–63.

### 84. Homayoun H, Moghaddam B. NMDA receptor hypofunction produces opposite

effects on prefrontal cortex interneurons and pyramidal neurons. J Neurosci.
2007;27:11496–500.

### 85. Murray JD, Bernacchia A, Freedman DJ, Romo R, Wallis JD, Cai X, et al. A hierarchy

of intrinsic timescales across primate cortex. Nat Neurosci. 2014;17:1661–3.

### 86. Braun U, Schäfer A, Bassett DS, Rausch F, Schweiger JI, Bilek E, et al. Dynamic

brain
network
reconﬁguration as
a potential schizophrenia
genetic
risk
mechanism modulated by NMDA receptor function. Proc Natl Acad Sci USA.
2016;113:12568–73.

### 87. Deco G, Cruzat J, Cabral J, Knudsen GM, Carhart-Harris RL, Whybrow PC, et al. Whole-brain multimodal neuroimaging model using serotonin receptor maps
explains non-linear functional effects of LSD. Curr Biol. 2018;28:3065–74.e6.

### 88. Vohryzek J, Cabral J, Lord LD, Fernandes HM, Roseman L, Nutt DJ, et al. Brain

dynamics predictive of response to psilocybin for treatment-resistant depression. Brain Commun. 2024;6:fcae049.

### 89. Friston K. A theory of cortical responses. Philos Trans R Soc Lond B Biol Sci.

2005;360:815–36.

### 90. Corlett PR, Murray GK, Honey GD, Aitken MR, Shanks DR, Robbins TW, et al. Disrupted prediction-error signal in psychosis: evidence for an associative
account of delusions. Brain. 2007;130:2387–400.

### 91. Blakemore SJ, Smith J, Steel R, Johnstone CE, Frith CD. The perception of self-

produced sensory stimuli in patients with auditory hallucinations and passivity
experiences: evidence for a breakdown in self-monitoring. Psychol Med.
2000;30:1131–9.

### 92. Voss M, Moore J, Hauser M, Gallinat J, Heinz A, Haggard P. Altered awareness of

action in schizophrenia: a speciﬁc deﬁcit in predicting action consequences. Brain. 2010;133:3104–12.

### 93. Mana L, Vila-Vidal M, Köckeritz C, Aquino K, Fornito A, Kringelbach ML, et al. Using

in silico perturbational approach to identify critical areas in schizophrenia. Cereb
Cortex. 2023;33:7642–58.

### 94. Guan S, Wan D, Zhao R, Canario E, Meng C, Biswal BB. The complexity of spon-

taneous brain activity changes in schizophrenia, bipolar disorder, and ADHD was
examined using different variations of entropy. Hum Brain Mapp. 2023;44:
94–118.

### 95. Takahashi T, Cho RY, Mizuno T, Kikuchi M, Murata T, Takahashi K, et al. Anti-

psychotics reverse abnormal EEG complexity in drug-naive schizophrenia: a
multiscale entropy analysis. Neuroimage. 2010;51:173–82.

### 96. Deco G, Kringelbach ML. Turbulent-like dynamics in the human brain. Cell Rep.

2020;33:108471.

### 97. Dagnino PC, Escrichs A, López-González A, Gosseries O, Annen J, Sanz Perl Y, et al. Re-awakening the brain: forcing transitions in disorders of consciousness by
external in silico perturbation. PLoS Comput Biol. 2024;20:e1011350. ACKNOWLEDGEMENTS
I. A. P and A. E. are supported by grant PID2022-136216NB-100 funded by MICIU/AEI/
10.13039/501100011033 and by ‘ERDF A way of making Europe’,’ERDF’, ‘EU’. P. D. is
supported by the AGAUR FI-SDUR Grant (no. 2022 FISDU 00229). Y. S. P. is supported by
the project NEurological MEchanismS of Injury, and Sleep-like cellular dynamics
(NEMESIS; ref. 101071900) funded by the EU ERC Synergy Horizon Europe. M. L. K. is
supported by the Centre for Eudaimonia and Human Flourishing (funded by the Pettit
and Carlsberg Foundations) and the Center for Music in the Brain (funded by the Danish
National Research Foundation, DNRF117). P. J. U. is supported by the project MR/
L011689/1 from the Medical Research Council (MRC). G. D. is supported by grant no. PID2022-136216NB-I00 funded by MICIU/AEI/10.13039/501100011033 and by ‘ERDF A
way of making Europe’, ERDF, EU, Project NEurological MEchanismS of Injury, and Sleep-
like cellular dynamics (NEMESIS; ref. 101071900) funded by the EU ERC Synergy Horizon
Europe, and AGAUR research support grant (ref. 2021 SGR 00917) funded by the
Department of Research and Universities of the Generalitat of Catalunya.

## AUTHOR CONTRIBUTIONS

IA-P: Conceptualization; Formal analysis; Investigation; Methodology; Project administra-
tion; Software; Validation; Visualization; Writing—original draft; Writing—review & editing. AE: Conceptualization; Formal analysis; Funding acquisition; Investigation; Resources; Supervision; Validation; Writing—review & editing. PCD: Formal analysis; Investigation; Resources; Software; Validation; Writing—review & editing. YSP: Conceptualization; Formal
analysis; Investigation; Methodology; Resources; Software; Supervision; Validation; Writing
—review & editing. MLK: Methodology; Resources; Software; Validation; Writing—review &
editing. PJU: Resources; Writing—review & editing. GD: Conceptualization; Funding
acquisition; Investigation; Methodology; Project administration; Resources; Software; Supervision; Validation; Writing—review & editing.

## COMPETING INTERESTS

The authors declare no competing interest.

## ETHICS APPROVAL AND CONSENT TO PARTICIPATE

All methods were performed in accordance with the relevant guidelines and
regulations. The resting-state fMRI data analyzed in this study were obtained from
the UCLA Consortium for Neuropsychiatric Phenomics LA5c Study (openneuro.org/
datasets/ds000030), which was approved by the University of California Los Angeles
Institutional Review Board. Written informed consent was obtained from all
participants by the original investigators. I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356

## CONSENT FOR PUBLICATION

Not applicable, as the study used anonymized, publicly available data.

## ADDITIONAL INFORMATION

Supplementary information The online version contains supplementary material
available at https://doi.org/10.1038/s41398-025-03584-0. Correspondence and requests for materials should be addressed to
Irene Acero-Pousa. Reprints and permission information is available at http://www.nature.com/
reprints
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims
in published maps and institutional afﬁliations. Open Access This article is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivatives 4.0 International License,
which permits any non-commercial use, sharing, distribution and reproduction in any
medium or format, as long as you give appropriate credit to the original author(s) and
the source, provide a link to the Creative Commons licence, and indicate if you modiﬁed
the licensed material. You do not have permission under this licence to share adapted
material derived from this article or parts of it. The images or otherthird party material in
this article are included in the article’s Creative Commons licence, unless indicated
otherwise in a credit line to the material. If material is not included in the article’s
Creative Commons licence and your intended use is not permitted by statutory
regulation or exceeds the permitted use, you will need to obtain permission directly
from
the
copyright
holder. To
view
a
copy
of
this
licence,
visit
http://
creativecommons.org/licenses/by-nc-nd/4.0/.
© The Author(s) 2025, corrected publication 2025
I. Acero-Pousa et al. Translational Psychiatry (2025) 15:356
