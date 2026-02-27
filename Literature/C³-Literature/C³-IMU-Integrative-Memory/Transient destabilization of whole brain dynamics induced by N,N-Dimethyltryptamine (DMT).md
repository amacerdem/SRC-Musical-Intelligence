# Transient destabilization of whole brain dynamics induced by N, N-Dimethyltryptamine (DMT)

**Authors:** Juan Ignacio Piccinini
**Year:** D:20
**Subject:** Communications Biology, doi:10.1038/s42003-025-07576-0

---

communications biology
Article
https://doi.org/10.1038/s42003-025-07576-0
Transient destabilization of whole
brain dynamics induced by N, N-
Dimethyltryptamine (DMT)
Check for updates
Juan Ignacio Piccinini, Yonatan Sanz Perl
1,2, Carla Pallavicini1,3, Gustavo Deco
2,4, Morten Kringelbach
5,6,7, David Nutt
8, Robin Carhart-Harris8,9, Christopher Timmermann8 &
Enzo Tagliazucchi
1,10
The transition towards the brain state induced by psychedelic drugs is frequently neglected in favor of
a static description of their acute effects. We use a time-dependent whole-brain model to reproduce
large-scale brain dynamics measured with fMRI from 15 volunteers under 20 mg intravenous N, N-
Dimethyltryptamine (DMT), a short-acting psychedelic. To capture its transient effects, we parametrize
the proximity to a global bifurcation using a pharmacokinetic equation. Simulated perturbations reveal
a transient of heightened reactivity concentrated in fronto-parietal regions and visual cortices,
correlated with serotonin 5HT2a receptor density, the primary target of psychedelics. These advances
suggest a mechanism to explain key features of the psychedelic state and also predicts that the
temporal evolution of these features aligns with pharmacokinetics. Our results contribute to
understanding how psychedelics introduce a transient where minimal perturbations can achieve a
maximal effect, shedding light on how short psychedelic episodes may extend an overarching
inﬂuence over time. Psychedelic drugs offer an opportunity to investigate how changes in the
brain across multiple spatiotemporal scales interact with human con-
sciousness and cognition1. At the molecular level, psychedelics bind to the
serotonin 5HT2a receptor2, recruiting speciﬁc intracellular signaling path-
ways that are different from those implicated in the action of non-
psychedelic 5HT2A agonists3,4. The subjective effects of psychedelics may
also depend on other pharmacological and non-pharmacological factors5,
the latter including the context of drug intake and the mindset of the user6. At the systems level, psychedelics increase global network integration
measured with functional magnetic resonance imaging (fMRI)7–12, and
evidence from multiple modalities links their effects to increased entropy
and complexity of spontaneous brain activity ﬂuctuations13–19. An inte-
grative understanding of psychedelic action would require the identiﬁcation
of causal mechanisms behind these empirical observations, from molecules
to subjective experience1. In recent years, generative whole-brain activity models have been
increasingly adopted to test potential mechanisms underlying neuroima-
ging data, including successful applications to the speciﬁc case of psyche-
deliccompoundspsilocybin and lysergicacid diethylamide(LSD)20. In these
two case studies, biophysical models consisting of local excitatory and
inhibitory populations with excitatory long-range connections were used to
provide evidence supporting psychedelic-induced modulation of 5HT2a
synaptic scaling21–23. Herzog and colleagues implemented a similar modelto
show that 5HT2a receptor stimulation is consistent with increased brain-
wide entropy13, in agreement with the theoretical model of psychedelic
action proposed by Carhart-Harris24. A complementary approach is to
consider phenomenological models to investigate changes in global brain
dynamics in line with insights and metrics from complexity science25. This
approach was followed to demonstrate that LSD increases the complexity of
spontaneous brain activity as assessed via fMRI26, an observation consistent
1Universidad de Buenos Aires, Facultad de Ciencias Exactas y Naturales, Departamento de Física, and CONICET - Universidad de Buenos Aires, Instituto de Física
Aplicada e Interdisciplinaria (INFINA), Buenos Aires, Argentina. 2Center for Brain and Cognition, Computational Neuroscience Group, Department of Information
and Communication Technologies, Universitat Pompeu Fabra, Barcelona, Spain. 3Integrative Neuroscience and Cognition Center, CNRS, Université Paris Cité, Paris, France. 4Institució Catalana de la Recerca i Estudis Avançats (ICREA), Barcelona, Spain. 5Centre for Eudaimonia and Human Flourishing, University of
Oxford, Oxford, UK. 6Department of Psychiatry, University of Oxford, Oxford, UK. 7Center for Music in the Brain, Department of Clinical Medicine, Aarhus
University, Aarhus, Denmark. 8Centre for Psychedelic Research, Department of Brain Sciences, Faculty of Medicine, Imperial College London, London, UK.
9Psychedelics Division, Neuroscape, Department of Neurology, University of California San Francisco, San Francisco, CA, USA. 10Latin American Brain Health
Institute (BrainLat), Universidad Adolfo Ibañez, Santiago, Chile.
e-mail: piccijuan@gmail.com; tagliazucchi.enzo@googlemail.com
Communications Biology | (2025) 8:409

1234567890():,;
1234567890():,;

with previous studies showing an expanded repertoire of brain states with
facilitated transitions between them19,27, constituting a potential mechanism
for the psychedelic-induced enhancement of neural ﬂexibility28. Moreover,
the dynamical characterization of psychedelic action reveals a scenario
opposite to that of unconsciousness, where a reduction in the repertoire of
brain states and an increase in their stability against perturbations is
observed25,29,30 as hypothesized in previous theoretical work24. To date, whole-brain models have been used to investigate the
mechanisms underlying the steady-state effects of LSD and psilocybin, two
classic psychedelic drugs. However, it is currently unknown whether the
putative mechanisms of psychedelic action identiﬁed by these models also
extend to the transitions from pre-dose baseline and the acute effects. Time-
dependent models capable of ﬁtting dynamics across transitions are
necessary to distinguish between the neurochemical modulation of brain
activity, aligned with the drug pharmacokinetics, and the indirect effects of
factors linked to the interplay between expectations, subjective effects, and
the short-term impact of the experience on the emotional state of the
subjects1. Moreover, developing computational models sensitive to slow
temporalﬂuctuations in brain activity may contribute to determine whether
the pharmacology of certain psychedelics is multi-phasic, as has been pro-
posed for the case of LSD31. The short-lasting psychedelic effects of intra-
venous DMT are ideally suited for this purpose, as they are highly dynamic
and give way to the recovery of the baseline state after around 30 minutes32. Making progress in this direction, recent studies have found that speciﬁc
EEG features of the DMT state are correlated with the serum concentration
of the drug17,33. However, the dynamical principles behind the transition to
altered consciousness remain to be addressed by modeling efforts. In this work, we adopted a model previously used to investigate the
effects of psychedelic drugs26, introducing time dependency in the para-
metergoverningtheproximitytodynamicalcriticality,i.e.aphasetransition
between qualitatively different dynamics (chaos/noise vs. statistical regula-
rities/oscillations34). To model the relatively short-lasting effects induced by
DMT, the temporal evolution of the model bifurcation parameter was
constrained to represent a simpliﬁed version of DMT pharmacokinetics35. The optimization of the free parameters underlying this temporal evolution
allowed us to reproduce the empirical functional connectivity dynamics
(FCD)36, and subsequently the optimal peak intensity and latency for DMT
vs. a placebo control condition. Finally, we investigated the stability of the
simulated dynamics against external perturbations, thus assessing potential
correlations between the local regional reactivity and the density of 5HT2a
receptors, the main pharmacological target of DMT2. Results
Methodological overview
Figure 1 provides an outline of the methods and the overall procedure. Following previous work, the local dynamics in the whole-brain model were
given by Stuart-Landau nonlinear oscillators, with a bifurcation at a = 036. For a > 0 the model presents stable oscillations, while a < 0 results in stable
spirals, which extinguish the oscillation amplitude until the dynamics are
dominated by the additive noise term, ηðtÞ. Close to the bifurcation (i.e.
dynamic criticality), the noise introduces spontaneous switches between
both regimes, resulting in oscillations with complex amplitude ﬂuctuations. To model the time-dependent changesintroduced by DMT, we put forward
an assumed equation forthebifurcationparameter aðtÞ givenby the gamma
function shown in Fig. 1. Parameters λ and β determine the peak amplitude
and its latency, respectively. For an adequate choice of parameters, this
function rises rapidly and then presents a slow decay, constituting an
approximate description of the pharmacokinetics of bolus intravenous
DMT administration35. The local Stuart-Landau nonlinear oscillators were
coupled using an averaged structural connectivity matrix inferred using
diffusion tensor imaging (DTI) from healthy individuals and scaled by the
global coupling parameter G. Since we aimed to capture the temporal
evolution introduced by the short-acting effects of DMT, we optimized the
gamma function parameters λ and β to ﬁt the reproduction of the mean
FCD computed from n = 15 participants, which contains in its i; j entry the
similarity between functional connectivity (FC) matrices computed over
short windows starting at time points i and j (see Methods). Note that in
contrast to previous applications of this model to resting state data21,34,36–38,
we did not optimize the statistical similarity between the empirical and
simulated FCD matrices; instead, we employed the Euclidean distance -also
known as Frobenius distance-for their comparison, as we were interested in
capturing the temporal evolution introduced by DMT. Model optimization
To determine the optimal gamma function parameters to reproduce the
whole-braindynamicsrepresentedbytheFCD,weperformedanexhaustive
exploration of all pairwise combinations of λ and β within a range of values
compatible with the expected DMT pharmacokinetics (see Methods). The
results of this exploration are shown in Fig. 2A for the placebo (left) and
DMT conditions (right), with lower values indicating a better model ﬁt
(average of n = 50 independent simulations). For the placebo condition, the
optimal values were located within a large region of comparatively low
amplitude and variable latency, evidencing a weak temporal dependency
without a clearly deﬁned peak of maximal intensity. Conversely, for DMT
this region was displaced and reduced to encompass shorter and less vari-
able latencies, together with larger amplitude values. Figure 2B represents
the empirical (left column) and optimal simulated (right column) FCD
matricesfortheplacebo(ﬁrstrow)andDMTconditions(second row). Note
that the two diagonal blocks of the FCD matrices separate the baseline (see
Fig. 1, “Functional connectivity dynamics”) and post-administration peri-
ods. The model is capable of approximating this temporal structure, as well
as the overall intensity of the matrix element values. After determining the optimal λ and β for each independent run of the
simulation,weexploredthecorrespondingaðtÞplotsdisplayedinFig.3Afor
placebo and DMT, with thicker lines indicating the mean across all n = 50
simulations. This ﬁgure shows that dynamics start from a baseline of sus-
tained oscillations at a = 0.07. After DMT infusion, we observed a sharp and
rapid decrease of aðtÞ which displaced whole-brain dynamics towards the
bifurcation at a = 0. Reaching itspeak after  5 minutes, the parameter aðtÞ
gradually recovered towards baseline values at the end of the scanning
session. In contrast, results for the placebo condition showed a lower peak
amplitudecombinedwithlongerlatencies,tothepointwherethepeakswere
not reached during the scanning session. As a consequence, aðtÞ for the
placebo condition approximated the constant baseline value with com-
paratively smaller temporal variation. Figure 3B summarizes the differences
between the dynamics of aðtÞ found for placebo and DMT in the two-
dimensional space spannedby λ and β, where eachpoint represents optimal
values for an independent run of the simulation, and the larger full circles
indicate the mean across all simulations. For the DMT condition, we could
observe that λ and β were clustered in the upper left corner, indicating
comparatively low latencies and high amplitude peaks (λ = 159.3 ± 7, β =
284 ± 37, 95% conﬁdence interval [CI]). Conversely, the placebo condition
resulted in low amplitude values and more variable latencies, skewed
towards larger values relative to DMT (λ = 65.6 ± 9, β = 588 ± 69, 95% CI). Both clusters of values could be clearly separated, supporting the ﬁnding of
qualitatively different aðtÞ dynamics between conditions (t-test p < 0.0001
for both parameters). Oscillatory perturbations produce transients of heightened
reactivity in DMT
After determining the optimal parameters to ﬁt the FCD, we used the
resulting models to investigate the time-dependent effects of delivering
external perturbations. This analysis was motivated in previous reports
indicating that psychedelics increase the reactivity to external stimuli and
facilitate transitions between brain metastable states26,27. Based on these
results, we hypothesized that DMT would result in a transient episode of
more sensitive brain dynamics, arising due to a destabilization of whole-
brain dynamics, i.e. due to the increased proximity to dynamic criticality. To test our hypothesis, we introduced a periodic external perturbation
atthefrequencyoftheendogenousoscillations,whichwaspreviouslyshown
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

to maximize the effect on the ongoing brain activity39,40. We determined the
reactivity or sensitivity to the perturbation at each time point, noted here by
χðtÞ,computingthederivativeoftheinducedFCDchangeswithanumerical
differentiation algorithm (see methods for more details, and see Supple-
mentary Fig. 1 for an example of how FCD changes at two different sti-
mulation intensities). To facilitate the interpretation of the results, we
introduced this perturbation at nodes located within six resting state net-
works (RSN)41 known to encompass different functional brain systems:
primary visual (Vis), extrastriate (ES), auditory (Aud), sensorimotor (SM),
default mode (DM) and executive control (EC) cortices. Figure 4A shows
χðtÞ for each RSN, both for the placebo (top) and DMT (bottom) conditions
(see Supplementary Fig. 2 for an analysis of χ tð Þ computed using inter-
network FCD only). For the latter, it is clear that χðtÞ is aligned with the
expected evolution of drug effect intensity, with the largest reactivity
obtainedattheextrastriatevisualcortex. Incontrast,thetimedependencyof
χðtÞ was considerably less marked for the placebo group. Figure 4B displays
the peak of χðtÞ, i.e. χmax, for each RSN and for three different external
perturbationintensities (Fext),comparingtheDMT andplacebo conditions. Consistent with the results shown in Fig. 4A, the peak values were sys-
tematically lower in placebo vs. DMT for all intensities, indicating higher
reactivity to external perturbations during the acute effects of the drug. Correlation between peak differential reactivity and local 5HT2a
receptor density
Finally, we investigated the correlation between the 5HT2a receptor density
(see Methods) and the peak reactivity (χmax) across RSN. Based on the
known pharmacological action of DMT2, we expected a positive correlation
between these two variables, i.e. that RSN with higher 5HT2a receptor
density would show higher χmax values, and vice-versa. Figure 5A illustrates
thespatialconﬁgurationoftheRSN,whilethemean5HT2areceptordensity
per RSN is shown in Fig. 5B. To assess if the difference in χmax between
conditions can be attributed to the local density of serotonin receptors, we
ﬁrst computed the difference between the reactivity curves of DMT and
placebo,resultingin ΔχðtÞ. Figure5C showsthepeak of ΔχðtÞ,Δχmax, vs. the
5HT2a receptor density of each RSN, together with the best least-squares
linear ﬁt. To estimate the signiﬁcance of this correlation, we conducted a
Fig. 1 | Overview of the whole-brain model and the choice of optimization target. A Dynamics of a single node (“Local Model”), consisting of a Stuart-Landau non-
linear oscillator with bifurcation parameter a, and the imaginary and real part of
complex variable z vs. a, showing a transition between stable spirals and limit cycles
at a = 0. B Temporal parametrization of the bifurcation parameter aðtÞ, given by a
gamma function with parameters λ (peak amplitude) and β (peak latency). C Illustration of how the nodes were coupled (“Inter-areal coupling”) following the
structural connectivity given by DTI scaled by G to reproduce the empirical FCD. D Representation of the computation of the FCD matrix, which contains in its i; j
entry the similarity between FC matrices computed over short windows starting at
time points i and j. The diagonal block encased in red indicates the baseline period
before the administration of DMT (FCD: functional connectivity dynamics; DMT:
dimethyltryptamine; DTI: diffusion tensor imaging).
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

bootstrap procedure which resulted in the distribution of correlation coef-
ﬁcients (ρ) presented in the inset of this panel, with a mean value of
ρ ¼ 0:9059 ± 0:0003, 95% CI. Figure 5D displays the mean ρ (Δχmax vs.
5HT2a receptor density) across a range of external perturbation intensities
(Fext). Thisplotindicatesthatlowstimulationamplitudesexertaneffectthat
iscomparativelyindependentofthelocal5HT2areceptordensity. However,
as the perturbation intensity increases, the receptor density becomes more
relevant, peaking at ρ > 0.9. Finally, as the intensity keeps increasing, the
reactivity decouples again from the receptor density. Discussion
This study represents a ﬁrst step towards the computational modeling of
time-dependent psychedelic effects. Our main ﬁnding is that DMT desta-
bilizes (i.e. brings closer to the global bifurcation point, or dynamic criti-
cality) whole-brain dynamics, and that the extent of this destabilization is
compatible with the characteristic pharmacokinetics of the drug, here
constrainedbyagammafunction35. Conversely,aninactiveplaceboresulted
in extreme parameter values that ﬂattened this function, thus approx-
imating a constant value over time. A consequence of this loss of stability is
the heightened sensitivity to external perturbations39, paralleling the
dynamics of the bifurcation parameter and thus being maximal when the
perturbation is applied in nodes belonging to RSN with high 5HT2a
receptor density. This increased sensitivity may affect how the brain
responds to incoming sensory stimuli under the effects of the drug, and may
also impact on its capacity to amplify endogenous events linked to ongoing
mentation and cognitive processing. Note our emphasis on endogenous
events in this regard, as a converse reduced sensitivity to perturbation may
be true in relation to certain external perturbations, such as sensory-evoked
potentials42. Indeed, recent work showed that external stimulation delivered
during the psychedelic state has stronger effects relative to a control con-
dition, which include changes in the intensity of the experience as well as a
substantial modiﬁcation of entropy-based metrics of neural activity43. It is
also important to note that in the study by Mediano et al. the content and
structure of the stimulation was linked to the change in brain entropy, and
that the results were partially driven by increased entropy of the baseline
condition. In contrast, in our analyses the structured and periodic nature of
the external stimulation exerted a comparatively weak effect on the placebo
vs. drug condition. Previous studies have used similar models to investigate the mechan-
isms underlying psychedelic-induced changes in fMRI resting state
activity26. However, these studies were concerned primarily with the steady-
state effects of the drugs, thus neglecting the analysis of periods when their
intensity changes over time, such as the transitions betweenthe baseline and
the acute state. These transitions are difﬁcult to capture for the oral
administration of LSD or psilocybin, which results in a slower onset and a
less marked transition towards the psychedelic state44,45. In contrast, the
Fig. 3 | The temporal evolution of the bifurcation
parameter, a(t), distinguishes between DMT and
the placebo condition. A aðtÞ, deﬁned as a gamma
function, for n = 50 independent runs of parameter
optimization, compared between both conditions. Plots withthicker lines indicate the curves associated
with mean value parameters. B Two-dimensional
representation of the optimal gamma function
parameters, λ and β, both for placebo and DMT. Individual points indicate the outcome of the n = 50
independent runs of parameter optimization, while
the larger full circles represent the average across
simulation runs. Comparisons for the means of both
parameters were made with two-sided t-tests with
p-values < 0.0001 for both parameters (DMT:
dimethyltryptamine). Fig. 2 | Exploration of parameter space and Functional Connectivity Dynamics
(FCD) corresponding to the optimal model parameters. A Normalized Euclidean
distance between simulated and empirical FCD averaged across n = 50 simulations
for every pair of parameters λ and β. The matrices reveal different peak amplitude (λ)
and latency (β) values for placebo vs. DMT. Optimal performance for DMT is
restricted to a narrower region. The red stars indicate the optimal pair of parameters
selected for each condition. B Empirical and optimal simulated FCD (columns) for
the placebo and DMT conditions (rows) averaged over n = 15 subjects (independent
simulations). Simulated FCD matrices were computed using optimal λ and β
parameters marked with the red stars in the left panel. Euclidean distances between
simulated and empirical FCDs were 0.19 ± 0.03 and 0.14 ± 0.02 (95% conﬁdence
interval [CI]) for DMT and placebo respectively (FCD: functional connectivity
dynamics; DMT: dimethyltryptamine).
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

intravenous administration of DMT results in a fast-onset and relatively
brief psychedelic episode that peaks in subjective intensity only a few
minutes after the infusion32 as indeed occurred in our previous work9,17. Our
current study shows that the whole-brain FCD dynamics induced by DMT
on fMRI data recapitulate this temporal evolution, which was not observed
for the placebo. It is important to note that even if the intensity of the DMT
effects is not reﬂected on the amplitude of the time-domain fMRI signals,
whole-brainFCDcontainssufﬁcientinformationtodeterminethetemporal
evolutionof the DMTexperience asshown bythe optimal ﬁtofthe modelto
the FCD data. The transient destabilization of brain dynamics induced by DMT is
consistent with multiple experimental results and theoretical accounts of
psychedelic action in the human brain24. Drawing from the theory of
bifurcations in dynamical systems, as the model approximates the bifur-
cation point, both the complexity and entropy of simulated brain activity
are expected to increase13–19, together with an expansion in the repertoire
of possible metastable states19. Also, near the bifurcation point, the sen-
sitivityofthesystemtoexternalperturbationsismaximized26,39,predicting
a larger response to a perturbation within the psychedelic state. A pro-
longed period of recovery from perturbation is known as critical slowing
and is considered to be one of several signatures of critical states, such as a
global dynamic bifurcation46. Using non-invasive transcranial magnetic
stimulation (TMS) combined with electroencephalography (EEG), Ort
and colleagues could not ﬁnd changes in cortical reactivity induced by
psilocybin; however, they informed changes in spectral content and
subjective experience linked to the stimulation47. This result is partially
consistent with our prediction, especially when taking into account the
differences between TMS and a periodic perturbation delivered at the
natural frequency of the endogenous oscillations. Empirically, this per-
turbation could be achieved by non-invasive methods such as transcranial
alternating current stimulation (tACS)48; however, to date, this form of
stimulation has not been investigated in participants undergoing the
effects of psychedelic drugs. Our results draw a parallel between the effects of DMT on whole-brain
dynamics and the theory of dynamical and statistical criticality. The main
differencebetweenconditionswasthebehaviorofthebifurcationparameter
across time, resulting in values closer to the critical value coincident with the
peak effects of DMT. This ﬁnding, which is consistent with prior work
implying increased signatures of criticality in the psychedelic state46,49,50, can
be interpreted through the critical brain hypothesis, stating that the major
features of brain dynamics can be explained by proximity to a second-order
phase transition51,52. Near this critical point, the system exhibits divergent
susceptibility (i.e. reactivity), allowing minor perturbations to propagate
throughout the entire system53. Extending this analogy, we can postulate
that 5HT2a receptor activation shifts the network state towards dynamic
criticality, which is consistent with multiple other ﬁndings related to the
brain dynamics under the effects of psychedelic drugs, as discussed by Girn, M. et al 202325. We are mindful, however, that certain speciﬁc stimuli
consonant with the ongoing state, such as music54, may have a bigger psy-
chological and, presumably, neurobiological55 impact under psychedelics. This matter may point to the special value of utilizing naturalistic stimuli
with good ecological validity in the context of psychedelic research. We also report that the sensitivity to external perturbations covariates
with the density of 5HT2a receptors. Since we normalized this value by the
total number of nodes in each RSN, the explanation for this correlation
should be found in the inﬂuence of 5HT2a in the organization of functional
and structural connectivity. This serotonin receptor subtype is implicated in
large-scale heterogeneities of the human cerebral cortex, constituting an
important factor to distinguish between unimodal and the higher-level
integrative transmodal cortex56. Moreover, by bringing the global dynamics
closer to dynamical criticality, 5HT2a receptor activation may facilitate the
switching between inter-areal coupling that may underly psychedelic-
induced neural57,58 and possibly cognitive ﬂexibility28, and also open a
transient window where the increased functional diversity may exert an
effect in the underlying structural connectivity via plasticity effects59. Eventually, this could contribute to consolidating the long-term effects
Fig. 4 | Time-dependent effect of simulated perturbations indicate higher reac-
tivity for DMT vs. placebo. A Reactivity χðtÞ normalized by the number of nodes in
the corresponding RSN, for placebo (top) and DMT (bottom). DMT curves peak
around 4 minutes after the dose, restoring baseline values at the end of the session. Placebo shows a lower peak amplitude and longer latencies remaining constant
during the whole study. Shaded regions of each line denote the standard deviation of
the reactivities (n = 25 simulations). B Plots of the peak χðtÞ across time (χmax) for
each RSN and three different external perturbation intensities (Fext) (n = 200
bootstrapped samples). Comparisons between conditions (for a given perturbation
intensity) and between successive perturbation intensities (for a given condition)
were made with two-sided t-tests, giving p-values < 0.0001 for all comparisons. Executive control (EC) network was an exception when comparing Fext = 0.005 and
Fext = 0.01 (p = 0.23) (DMT: dimethyltryptamine; RSN: resting state network).
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

associated with brief psychedelic episodes60. For high values of the external
perturbation amplitude, the reactivity decoupled from the 5HT2a receptor
density,likelyindicatingthesaturationoftheinducedeffectsonwhole-brain
dynamics. We opted to simulate perturbations of the ongoing dynamics with a
periodic signal matching the frequency of the local dynamics, i.e. the
resonant frequency. This choice represents transcranial alternating current
stimulation (tACS) at the peak frequency of the endogenous oscillations. The resonant frequency is a natural choice for stimulation, given that it is
known to elicit a maximal response39. Also, more complicated signals can be
represented in the frequency space via their Fourier decomposition, where
the response will be predominantly elicited by the amplitude of the Fourier
component at the resonant frequency. Previous studies modeled other
forms of stimulation resembling a single transcranial magnetic stimulation
(TMS) pulse38,61,62. In our model, this would correspond to displacing the
dynamics away from the limit cycle and then determining the necessary
time to recover baseline dynamics. This choice presents the advantage of
representing the effects of a TMS pulse localized in time, one of the most
commonly used forms of transcranial stimulation. However, it is unloca-
lized in the frequency domain, and therefore it does not inform how the
model responds to speciﬁc frequencies. Beyond the current application, the temporal parametrization of
whole-brain models may ﬁnd other uses to test whether a certain temporal
process underlies the recorded neuroimaging data, and to inform the
potential mechanisms behind the empirical observations. The signal pre-
processing steps applied to resting state fMRI data typically include high
pass ﬁlters which are necessary to attenuate the effects of scanner drift and
head movement63. Therefore, the fMRI time series may not directly reﬂect
the dynamics of the phenomenon under study, unless the experiment is
designed to maximize the signal-to-noise ratio, e.g. with tasks or stimulation
structured in according to an adequate block design64. However, it may not
be possible to control the onset and length of the temporal process under
study, as in the current application to the study of a transient pharmaco-
logically induced event. This could also occur in the study of seizures65,
sleep-related transients and graphoelements (e.g. spindles, K-complexes)66,
spontaneous mentation or ongoing cognition67, and in other endogenous
phenomena with an interesting temporal structure beyond experimental
control. In these cases, the use of time-dependent whole-brain models may
be useful to detect the ﬁngerprints of the event in the FCD, by comparing
different temporal parametrizations by ﬁtting and contrasting their corre-
sponding goodness of ﬁt. One important limitation of our approach is that the temporal para-
metrization a priori constrains the model and its capacity to detect the
underlying temporal dynamics. By choosing a gamma function, our
approach only allowed us to test whether the FCD dynamics under DMT
could be better explained by this speciﬁc temporal evolution of the bifur-
cation parameter relative to the placebo condition. However, since we did
not specify a prior the direction of the effect, this approach allowed us to test
whether DMT could bring the dynamics closer to the global bifurcation and
therefore towards a point of decreased stability. When comparing the
gamma function with a null model keeping aðtÞ constant post-dose, we
found that this parametrization outperformed the gamma function for the
Fig. 5 | The peak differential reactivity to external perturbations (Δχmax)
between DMT and placebo correlates with the local 5HT2a receptor density. A Spatial conﬁguration of the six RSN that constrained the simulated delivery of the
perturbation (Vis: primary visual, nVis = 7; ES: extrastriate, nES = 9; Aud: auditory,
nAud = 26; SM: sensorimotor, nSM = 13; DM: default mode, nDM = 12; EC: executive
control, nEC = 24), adapted from Ipiña, I. P. et al.40. B 5HT2a receptor density per
RSN (individual points and mean ± SE). C Peak of ΔχðtÞ (n = 200), Δχmax, vs. the
5HT2a receptor density of each RSN together with the best least-squares linear ﬁt. The inset shows the distribution of correlation coefﬁcients (ρ) obtained using a
bootstrap procedure (ncorr = 1000). D Correlation coefﬁcient ρ (mean ± SD) vs. the
external perturbation intensity, Fext, n = 1000. (DMT: dimethyltryptamine; RSN:
resting state network; 5HT: 5-hydroxytryptamine).
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

placebo condition, as expected from our results. However, we did not ﬁnd
signiﬁcant differences relative to the gamma function for the DMT condi-
tion (see supplementary Fig. 3). We note that within the family of gamma
functions used to parametrize the bifurcation parameter, the optimal ﬁt was
consistently obtained in a region of parameter space corresponding to a
relatively early peak at 10 min, and a peak value that was in all cases larger
than the peak value obtained for the placebo condition. These parameter
values are compatible with human studies of DMT pharmacokinetics68. The
lack of difference observed between both models could depend on metho-
dological choices (e.g. the choice of the optimization metric and the need to
balance relative differences between matrix values vs. the overall magnitude
of the matrix entries), which could be addressed in future studies ﬁtting
whole-brain models to transient brain states. The choice of the gamma function can be justiﬁed by the prior lit-
erature on the time course of DMT-induced effects, as well as its effects on
EEG activity and their correlation with the drug pharmacokinetics9,16,17,32. While more complex models could be implemented to adequately describe
these dynamics33, our choice has the merit of constituting a qualitative
description of the transient effects of DMT without incurring in a pro-
liferation of free parameters required for more neurobiological realism. Moreover, the comparatively poor temporal resolution of fMRI may limit
the potential gain of including a more nuanced description of pharmaco-
dynamics. This limitation could be addressed by reproducing our work with
data from faster imaging modalities (such as EEG and MEG). Another
limitationisthenumberofparticipants(n = 15),whichiscomparativelylow
for a pharmacological fMRI study. In the case of this study, after applying
strictcriteriatoexcludesubjectsduetoheadmotioninthescanneronly75%
of the original data was included. While we modeled group-averaged FCD
matrices, future studies at the single-subject level should attempt to raise the
effective number of subjects included in the model. Finally, psychedelics are
known to introduce physiological effects (e.g. heart rate, blood pressure,
respiration), as well as alterations to the coupling between neural activity
and the cardiovascular system69. In ourstudy, we followed previousresearch
by modeling physiological noise in terms of the average signal measured at
theventricles,drainingveins,andlocalwhitematter. Whilethisisastandard
procedure in the ﬁeld8,70–73, there could be limitations associated with this
approach which could be overcome by introducing regressors based on
cardiac and respiratory time series74. The limitations imposed by changes to
neurovascular coupling could be addressed in future studies by using a
condition-speciﬁc hemodynamic response, estimated either from task and/
or stimulation paradigms75, or by deconvolution of resting state BOLD
signals76. In summary, our work shifts the focus from the reproduction of the
steady-state effects of psychedelics towards disentangling the dynamics of
the fast-onset and short-lived intravenous DMT experience. The future
implementation of more realistic biophysical models could contribute to
our understanding of how the interaction betweendrugs, neurotransmitters
and receptors is capable of initiating a cascade of neural events which
ultimately results in a global brain state associated with profound alterations
in consciousness and cognitive processing with potentially lasting
consequences60. The combination of these models with a more nuanced
description of drug pharmacokinetics and pharmacodynamics could also
contribute to explain the potential multiphasic effects of some psychedelic
compounds, and to test potential mechanisms behind their long-lasting
effects, which are a key aspect of their possible therapeutic use in patients
with depression and other psychiatric disorders. Methods
Study participants and experimental design
This is a re-analysis of a previously published EEG-fMRI dataset acquired
from healthy participants under the acute effects of DMT9. The original
publication can be referenced for in-depth methodological details. The study followed a single-blind, placebo-controlled design, with all
participants providing written informed consent. The experimental proto-
col received approval from the National Research Ethics Committee
London—Brent and the Health Research Authority, conducted in adher-
ence to the Declaration of Helsinki (2000), the International Committee on
Harmonization Good Clinical Practices guidelines, and the National Health
Service Research Governance Framework. All ethical regulations relevant to
human research participants were followed. VolunteerscompletetwovisitsattheImperialCollegeClinicalImaging
Facility, spaced two weeks apart. On each testing day, participants were
subject to separate scanning sessions. In the initial session, they received
intravenous administration of either placebo (10 mL sterile saline) or 20 mg
DMT (fumarate form dissolved in 10 mL sterile saline). This was done in a
counter-balanced order, with half receiving placebo and the rest receiving
DMT. The ﬁrst session comprised continuous resting-state scans lasting
28 minutes, with DMT/placebo administered at the end of the 8th minute,
and scanning concluding 20 minutes after injection. Participants lay in the
scanner with closed eyes aided by an eye mask, while fMRI data was
recorded. In the second session, participants were cued to verbally rate the
subjectiveintensityofdrugeffectseveryminuteinreal-time. OnlyfMRIdata
from the ﬁrst scanning session was used for the present analysis. A cohort of 20 participants completed all study visits, consisting of 7
females and a mean age of 33.5 years and a standard deviation of 7.9. For the
present study data from only 15 of the subjects were used, the rest being
discarded due to strong head movement artifacts inside the scanner (see
below for further information on the exclusion criterion). This ﬁnal sample
consisted of a cohort with 5 females and a mean age of 39.6 and a standard
deviation of 9.6.
fMRI acquisition and preprocessing
Images were acquired using a 3 T MR scanner (Siemens Magnetom Verio
syngo MR B17) with a 12-channel head coil for compatibility with EEG
acquisition. Functional imaging was performed using a T2*-weighted
BOLD-sensitive gradient echo planar imaging sequence [repetition
time (TR) = 2000 ms, echo time (TE) = 30 ms, acquisition time (TA) =
28.06 min, ﬂip angle (FA) = 80°, voxel size = 3.0 × 3.0 × 3.0 mm3, 35 slices,
interslice distance = 0 mm]. The preprocessing steps involved despiking, slice time correction,
motion correction, brain extraction, rigid body registration to anatomical
scans, nonlinear registration to 2 mm MNI brain, denoising (via Indepen-
dent Component Analysis), and scrubbing(using a framewise displacement
[FD] threshold of 0.4, with scrubbed volumes replaced by the mean of
surrounding volumes)77. The BOLD time series were ﬁltered with a second-
order Butterworth ﬁlter in the range between 0.01 and 0.08 Hz, in line with
previous studies78–81. The choice of the low-pass cutoff was justiﬁed as it
helps to ﬁlter out physiological noise, which tends to dominate higher
frequencies78. Further steps included spatial smoothing (FWHM) of 6 mm,
linear and quadratic detrending, and regressing out nine nuisance regres-
sors. These regressors, all band-pass ﬁltered, consisted of six motion-related
parameters (3 translations, 3 rotations) and three anatomically related
parameters (ventricles, draining veins, local white matter). Finally, time series were extracted for each Automated Anatomical
Labeling (AAL)82 template region by averaging the time series from all
voxels within the corresponding region. Out of 20 participants, ﬁve were excluded from group analyses due to
excessiveheadmovementduringthe8-minutepost-DMTperiod ( > 20%of
scrubbed volumes with a framewise displacement threshold [FD] of 0.4). Anatomical connectivity matrix (SC)
The structural connectome was obtained by applying diffusion tensor
imaging (DTI) to diffusion-weighted imaging (DWI) recordings from 16
healthy right-handed participants (11 men and 5 women, mean age: 24.75 ±
2.54 years) recruited online at Aarhus University, Denmark. Subjects with
psychiatric or neurological disorders (or a history thereof) were excluded
from participation. The MRI data (structural MRI, DTI) were recorded in a
single session on a 3 TS Skyra scanner. The following parameters were used
for the structural MRI T1 scan: voxel size of 1 mm3; reconstructed matrix
size256×256;echotime(TE)of3.8msandrepetitiontime(TR)of2300ms.
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

DWI data were collected using the following parameters: TR = 9000 ms, TE
= 84 ms, ﬂip angle = 90°, reconstructed matrix size of 106 × 106, voxel size of
1.98 × 1.98 mm with slice thickness of 2 mm and a bandwidth of
1745Hz/Px. Furthermore,thedatawererecordedwith62optimalnonlinear
diffusion gradient directions at b = 1500 s/mm2. Approximately one non-
diffusion-weighted image (b = 0) per 10 diffusion-weighted images was
acquired. Additionally, the DTI images were recorded with different phase
encoding directions. One set was collected applying anterior to posterior
phase encoding direction and the second one was acquired in the opposite
direction. The AAL template was used to parcellate the entire brain into 90
regions (76 cortical regions and 14 subcortical regions). The parcellation
contained 45 regions in each hemisphere. To co-register the EPI image to
the T1-weighted structural image, the linear registration tool from the FSL
toolbox (www.fmrib.ox.ac.uk/fsl, FMRIB, Oxford)83wasemployed. TheT1-
weighted images were co-registered to the T1 template of ICBM 152 in MNI
space. The resulting transformations were concatenated, inverted and fur-
ther applied to warp the AAL template from MNI space to the EPI native
space,wherethediscretelabelingvalueswerepreservedbyapplyingnearest-
neighbor interpolation. SC networks were constructed following a three-
step process. First, the regions of the whole-brain network were deﬁned
using the AAL template. Second, the connections between nodes in the
whole-brain network (i.e., edges) were estimated using probabilistic trac-
tography for each participant. Third, results were averaged across
participants. Data preprocessing was performed using FSL diffusion toolbox (Fdt)
with default parameters. Following this preprocessing, the local probability
distributions of ﬁber directions were estimated at each voxel84. The prob-
trackx tool in Fdt was used to provide an automatic estimation of crossing
ﬁbers within each voxel, which has been shown to signiﬁcantly improve the
tracking sensitivity of non-dominant ﬁber populations in the human
brain85. The connectivity probability from a seed voxel i to another voxel j
was deﬁned by the proportion of ﬁbers passing through voxel i that reached
voxel j (sampling of 5000 streamlines per voxel). All the voxels in each AAL
parcel were seeded (i.e. gray and white matter voxels were considered). This
was extended from the voxel level to the region level, i.e. in a parcel con-
sisting of n voxels, 5000 × n ﬁbers were sampled. The connectivity prob-
ability Pij from region i to region j was calculated as the number of sampled
ﬁbers in region i that connected the two regions, divided by 5000 × n, where
nrepresentsthenumberofvoxelsinregioni. TheresultingSCmatriceswere
thresholded at 0.1% (i.e. a minimum of ﬁve streamlines). Due to the dependence of tractography on the seeding location, the
probability from i to j was not necessarily equivalent to that from j to i. However, these two probabilities were highly correlated across the brain for
all participants (r > 0.70, p < 10 −50). As the directionality of connections
cannot be determined using diffusion MRI, the unidirectional connectivity
probability Pij between regions i and j was deﬁned by averaging these two
connectivityprobabilities. Thisunidirectionalconnectivitywasconsidereda
measure of SC between the two areas, with Cij = Cji. The regional con-
nectivity probability was calculated using in-house Perl scripts. For both
phase encoding directions, 90 × 90 symmetric weighted networks were
constructed based on the AAL parcellation, and normalized by the number
of voxels in each AAL region, thus representing the SC network organiza-
tion of the brain of each participant. Finally, the data was averaged across
participants. (Supplementary Fig. 4 summarizes the similarity between
structural
and
functional
connectivity,
both
for
simulated
and
empirical data). Whole-brain computational model
We simulated brain activity measured with fMRI at the whole-brain levelby
using a Stuart–Landau oscillator (i.e. Hopf normal form) for the local
dynamics (see Fig. 1, “Localmodel”). This phenomenological model aims to
directly simulate recorded brain signals. The emergent global dynamics are
simulated by including mutual interactions between brain areas according
to the anatomical connectivity matrix Cij obtained from DTI (see Fig. 1,
“Inter-areal coupling”). The full model consists of 90 coupled nodes
representing the 90 cortical and subcortical brain areas from AAL parcel-
lation, with the following temporal evolution for region n:
dxn
dt ¼ aðtÞ  xn
2  yn



xn  ωyn þ G P

p¼1
Cnpðxp  xnÞ þ γηnðtÞ
dyn
dt ¼ aðtÞ  xn
2  yn



yn þ ωnxn þ G P

p¼1
Cnpðyp  ynÞ þ γηnðtÞ
ð1Þ
Here,ηn representsadditiveGaussiannoisewithstandarddeviationγ (setto
0.05), Cnp are the matrix elements of the anatomical connectivity matrix, G
is a factor that scales the anatomical connectivity (ﬁxed at G = 0.5,as
determined previously elsewhere40; see also section “Model ﬁtting to base-
line data”), ωn is the peak frequency of node n in the 0.01-0.08 Hz band
(determined using Fourier analysis applied to the empirical time series and
averagedacrossparticipants,seeSupplementaryFig.5forthedistributionof
node frequencies), and variable xn represents the empirical brain activity
signal of node n, which was used to compute the simulated FC and FCD
matrices. The simulated time series were not band-pass ﬁltered, given that
thefrequencyofeachnodewasdeﬁnedbasedontheempiricaldata,andthat
the positive optimal bifurcation parameters resulted in oscillating behavior
with frequencies within the range of the empirical values. Thelocaldynamicspresentasupercriticalbifurcationata =0,sothatif
a > 0 the system engagesin a stable limit cycle (i.e. oscillations) with angular
frequency ωn, and when a < 0 the local dynamics are attracted to a stable
ﬁxed point representing a low activity state dominated by noise. Close to the
bifurcation, the additive noise can induce a switching behavior between
regimes, resulting oscillations with a complex envelope36. To model the short-lasting effects of DMT, we introduce a time-
dependent bifurcation parameter aðtÞ following a gamma function that
represents a simpliﬁed description of drug pharmacokinetics35:
aðtÞ ¼ λ tet=β
N


ð2Þ
where N is a constant that normalizes the term between brackets, λ is a scale
parameter determining the amplitude of the peak, and β the parameter that
controls the rate of decay of the function, and therefore is related to the
latency of the peak (see Fig. 1, “Time dependency”). All codes necessary for the implementation of the model are available
online at https://github.com/juanpiccinini/DMT-whole-brain. Model ﬁtting to empirical data
To characterize the time-dependent structure of brain dynamics, we com-
puted the FCD matrices (see Fig. 1, “Functional connectivity dynamics”)37. For this purpose, each full-length signal of 28 min was split up into
M = 82 sliding windows of 60 s each, with an overlap of 40 s between suc-
cessive windows. For each sliding window centered at time t, the functional
connectivity matrix FC(t) was computed. The FCD matrix is a M × M
symmetric matrix whose t1, t2 entry is deﬁned by the Pearson correlation
coefﬁcient between the upper triangular parts of the two matrices FC(t1)
and FC(t2). These matrices were computed for each of the ﬁfteen partici-
pants and simulations by exhaustively exploring the model parameters
related to the temporal evolution of the bifurcation parameter, λ and β. To
compare the FCD matrices taking into account their temporal structure, we
used the Euclidean distance between the elements of the empirical and
simulated matrices. In Supplementary Fig. 6, we compare the obtained FCD
matrices with an alternative construction based on phase coherence, while
the agreement between sliding windows and phase coherence is summar-
ized in Supplementary Fig. 7. An alternative analysis based on metastability
and synchrony is presented in Supplementary Fig. 8.
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

Model ﬁtting to baseline data
To ﬁt the model to the baseline data before drug administration, we ﬁrst
conducted asearchfortheoptimalvaluesofthebifurcationparameter a and
the coupling parameter G. This was done by ﬁtting the FCD submatrix
comprising the 22 temporal windows (corresponding to the ﬁrst 8 minutes
before DMT injection) averaged over all subjects during both sessions
(30 submatrices in total). We performed an exhaustive parameter space
exploration by varying the two free parameters of the model: a was changed
homogeneouslyacrossallnodesfrom–0.1to0.1inincrementsof0.01,while
G was varied from 0 to 2 in steps of 0.1. This procedure was performed 30
times for each pair of parameters, and the resulting distance metrics were
then averaged to determine the optimal parameters (see Supplementary
Fig. 9A). We observed that the optimal values spanned an extended region
in parameter space, which included G = 0.5, a value consistent with pre-
vious determinations of the coupling parameter in similar datasets40. While
the global minimum was found for another value of G, the resulting
goodness of ﬁt was almost identical to the value obtained for G = 0.5,
without signiﬁcant differences between both choices (see panel B of Sup-
plementary Fig. 9). With the choice of G = 0.5 and a = 0.07, the Euclidean
distance found for the baseline was 0.084± 0.005, 95% conﬁdence interval
[CI]. Supplementary Fig. 10 presents a complementary comparison of the
normalized Euclidean distance and the Pearson correlation computed
between the empirical and simulated FCD and FC matrices. Fitting the temporal evolution of the bifurcation parameter
We ﬁxed the value of the bifurcation parameter to the baseline value of a =
0.07 for the ﬁrst 8 minutes of the simulation and introduced the time
dependency afterwards, given by the difference between the baseline value
and the gamma function λ
tet=β
N

, with t = 0 here indicating the time of the
drug injection. Next, we performed an exhaustive exploration of the para-
meter space spanned by λ and β, searching for the optimal combination of
parameters. For this purpose, we explored a grid given by λ = [0, 200] and
β = [20, 900] in steps of 5 and 20 units, respectively. For each parameter
combination, we computed the FCD 15 times (i.e. once per participant)
randomly changing the initial conditions of the model. The resulting FCD
matrices were averaged and compared with the empirical FCD using the
Euclidean distance. To compare the FCD matrices taking into account their
temporal structure, we used the Euclidean distance between the elements of
the empirical and simulated matrices, and then we normalized the results
dividing by the empirical norm to account for the relative change. The
procedure described in this section was repeated 50 times for each pair of
parameters. Simulated perturbations
Next, we modeled an oscillatory perturbation and investigated the response
of the whole-brain model ﬁtted as explained in the previous section. The
perturbation wasgivenbyanexternaladditive periodic forcingtermapplied
to node n, Fn ¼ FextðcosðωntÞ þ i sinðωntÞÞ, where the real part of the
perturbation is added to the equation for dxn
dt in Eq. 1 and the imaginary part
to the equation for dyn
dt. In the equation for Fn, ωn is the natural frequency of
the time series corresponding to node n (same as in Eq. 1). To facilitate the interpretation of the results, we applied this pertur-
bation to nodes located within six different resting state networks (RSN)
identiﬁed using independent component analysis (ICA) by Beckmann,
etal.41. Toaccountforthetimevariationofthereactivity,wesampledequally
spaced valuesofaðtÞ,herenotedap,withpindexingthetimesample. Intotal
weendedupwith42ap valuescorrespondingtothegammafunctionofeach
condition sampled at these time points. Then, for every one of those values,
we performed a simulation keeping ap constant until the end of the simu-
lation, i.e. for every simulation we set a = 0.07 for the ﬁrst 8 minutes,
corresponding to the pre-dose time interval, and then keeping the constant
valueapuntiltheendofthesimulation. Therefore,thefunctionalformofthe
bifurcation parameter is given by the concatenation of two constant
functions, a = 0.07 and ap, with p = 0,…,42. This procedure allowed to
compute how the dynamics responded to the external perturbation at each
ap value over the extended period of time that was used to obtain the FCD. Regarding the stimulation, we applied the perturbation after the ﬁrst
8 minutes corresponding to the baseline, varying the amplitude Fext from 0
to 0.015 in 0.0125 steps. The maximum value of this range was chosen as
higher values saturated the local reactivity, ﬂattening the curves. To sum-
marize, for eachcombination of RSN,amplitude Fext and the value of ap, we
computed the resulting FCDand itsdistance tothe empiricalcondition,and
then assessed the impact of the perturbation as explained in the following
section. Measure of reactivity to perturbations
We interpret the whole-brain model reactivity as the sensitivity of brain
activity to changes in the external periodic stimulation. Following an ana-
logy with the concept of susceptibility in statistical physics, we deﬁned the
reactivity as the following derivative:
χ tð Þ ¼ ∂M
∂Fext
ð3Þ
where M denotes the Euclidean distance between the simulated and
empirical FCD matrices. As Fext is increased, we expect the stimulated FCD
to depart from the baseline empirical value. χ tð Þ measures the rate at which
this divergence occurs. Thus, a large χ tð Þ value indicates that at time t, the
effect of changing Fext is maximal, measured in terms of its impact on the
Euclidean distance between the simulated and empirical FCD matrices. Conversely, a small χ tð Þ represents a regime were changing Fext exerts
comparatively little impact on the FCD. The reactivity χðtÞ was computed
using a second order ﬁnite difference method. We evaluated χðtÞ relative to
itsvalueatt =0bysubtractingχðt ¼ 0Þatlatertimes. Thiswasdoneinorder
to capture the changes of the perturbation relative to the baseline part. Furthermore, given that the number of nodes differs across the RSNs, and
that the reactivity can depend on the number of stimulated nodes, we
normalized its value by the number of nodes of each RSN. Bootstrap method
To determine the peak of χðtÞ across the duration of the simulation, we used
a bootstrapping procedure to obtain a distribution of peak values which
allowed us to compute a conﬁdence interval for the resulting average value. The bootstrap procedures were conducted by randomly drawing samples
(with replacement) from the distribution of values, creating different χðtÞ
curves in each iteration and measuring its maximum value. The size of the
sampled subsetwas equal to that of the original distribution. This procedure
was repeated 200 times, generating a bootstrap distribution of the desired
magnitude. When calculating the correlations between local 5HT2a
receptor density and the maximum reactivity per RSN, the bootstrap was
done 1000 times to generate the histograms. Statistics and Reproducibility
95% Conﬁdence Intervals were calculated using the standard error of the
mean (SEM) and a z-score of 1.96. Metric comparisons were achieved using
a two-sided paired t-test assuming non-equal variance between pair of
metrics. To determine the peak location and signiﬁcance of χðtÞ across the
duration of the simulation, we implemented a bootstrap procedure (see
section “Bootstrap method”). A Kolmogorov Smirnov test was used in
Supplementary Fig. 3. Effect size to compare model simulations in Sup-
plementary Fig. 9 were calculated using Cohen’s d. Receptor density maps
The receptor density maps used were estimated using PET tracer studies
obtained by Hansen and colleagues86. All PET images were registered to the
MNI-ICBM 152 nonlinear 2009 (version c, asymmetric) template and
subsequently parcellated to the 90 region AAL atlas82. For more details on
the acquisitions and limitations of the data set see the original publication86.
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

Reporting summary
Further information on research design is available in the Nature Portfolio
Reporting Summary linked to this article. Data availability
Source data to reproduce ﬁgures is available on https://github.com/
juanpiccinini/DMT-whole-brain.git along with the code87 (See Code avail-
ability). All other data is available from the corresponding author on rea-
sonable request. Code availability
Code needed to simulate the model and evaluate the conclusions in this
paper are available at https://github.com/juanpiccinini/DMT-whole-
brain.git87. Received: 13 March 2024; Accepted: 20 January 2025; References
1. Kwan, A. C., Olson, D. E., Preller, K. H. & Roth, B. L. The neural basis of
psychedelic action. Nat. Neurosci. 25, 1407–1419 (2022).
2. Nichols, D. E. Psychedelics. Pharm. Rev. 68, 264–355 (2016).
3. Wallach, J. et al. Identiﬁcation of 5-HT2A receptor signaling pathways
associatedwith psychedelicpotential. Nat. Commun. 14, 8221(2023).
4. González-Maeso, J. et al. Hallucinogens Recruit Speciﬁc Cortical
5-HT2A Receptor-Mediated Signaling Pathways to Affect Behavior. Neuron 53, 439–452 (2007).
5. Zamberlan, F. et al. The Varieties of the Psychedelic Experience: A
Preliminary Study of the Association Between the Reported
Subjective Effects and the Binding Afﬁnity Proﬁles of Substituted
Phenethylamines and Tryptamines. Front. Integr. Neurosci. 12,
(2018).
6. Carhart-Harris, R. L. et al. Psychedelics and the essential importance
of context. J. Psychopharmacol. 32, 725–731 (2018).
7. Tagliazucchi, E. et al. Increased Global Functional Connectivity
Correlates with LSD-Induced Ego Dissolution. Curr. Biol. 26,
1043–1050 (2016).
8. Carhart-Harris, R. L. et al. Neural correlates of the LSD experience
revealed by multimodal neuroimaging. Proc. Natl. Acad. Sci. 113,
4853–4858 (2016).
9. Timmermann, C. et al. Human brain effects of DMT assessed via EEG-
fMRI. Proc. Natl. Acad. Sci. 120, e2218949120 (2023).

### 10. Preller, K. H. et al. Changes in global and thalamic brain connectivity in

LSD-induced altered states of consciousness are attributable to the
5-HT2A receptor. eLife 7, e35082 (2018).

### 11. Luppi, A. I. et al. LSD alters dynamic integration and segregation in the

human brain. NeuroImage 227, 117653 (2021).

### 12. Bedford, P. et al. The effect of lysergic acid diethylamide (LSD) on

whole-brain functional and effective connectivity. Neuropsychopharmacol 48, 1175–1183 (2023).

### 13. Herzog, R. et al. A whole-brain model of the neural entropy increase

elicited by psychedelic drugs. Sci. Rep. 13, 6244 (2023).

### 14. Schartner, M. M., Carhart-Harris, R. L., Barrett, A. B., Seth, A. K. &

Muthukumaraswamy, S. D. Increased spontaneous MEG signal
diversity for psychoactivedoses of ketamine, LSDand psilocybin. Sci. Rep. 7, 46421 (2017).

### 15. Viol, A., Palhano-Fontes, F., Onias, H., de Araujo, D. B.& Viswanathan, G. M. Shannon entropy of brain functional complex networks under
the inﬂuence of the psychedelic Ayahuasca. Sci. Rep. 7, 7388 (2017).

### 16. Pallavicini, C. et al. Neural and subjective effects of inhaled N, N-

dimethyltryptamine in natural settings. J. Psychopharmacol. 35,
406–420 (2021).

### 17. Timmermann, C. et al. Neural correlates of the DMT experience

assessed with multivariate EEG. Sci. Rep. 9, 16324 (2019).

### 18. Lebedev, A. V. et al. LSD-induced entropic brain activity predicts

subsequent personality change. Hum. Brain Mapp. 37, 3203–3213
(2016).

### 19. Tagliazucchi, E., Carhart-Harris, R., Leech, R., Nutt, D. & Chialvo, D. R. Enhanced repertoire of brain dynamical states during the psychedelic
experience. Hum. Brain Mapp. 35, 5442–5456 (2014).

### 20. Cofré, R. et al. Whole-Brain Models to Explore Altered States of

Consciousness from the Bottom Up. Brain Sci. 10, 626 (2020).

### 21. Deco, G. et al. Whole-Brain Multimodal Neuroimaging Model Using

Serotonin Receptor Maps Explains Non-linear Functional Effects of
LSD. Curr. Biol. 28, 3065–3074.e6 (2018).

### 22. Kringelbach, M. L. et al. Dynamic coupling of whole-brain neuronal

and neurotransmitter systems. Proc. Natl. Acad. Sci. 117, 9566–9576
(2020).

### 23. Burt, J. B. et al. Transcriptomics-informed large-scale cortical model

captures topography of pharmacological neuroimaging effects of
LSD. eLife 10, e69320 (2021).

### 24. Carhart-Harris, R. L. et al. The entropic brain: a theory of conscious

states informed by neuroimaging research with psychedelic drugs. Front. Hum. Neurosci. 8, (2014).

### 25. Girn, M. et al. A complex systems perspective on psychedelic brain

action. Trends Cogn. Sci. 27, 433–445 (2023).

### 26. Jobst, B. M. et al. Increased sensitivity to strong perturbations in a

whole-brain model of LSD. NeuroImage 230, 117809 (2021).

### 27. Singleton, S. P. et al. Receptor-informed network control theory links

LSD and psilocybin to a ﬂattening of the brain’s control energy
landscape. Nat. Commun. 13, 5812 (2022).

### 28. Doss, M. K. et al. Psilocybin therapy increases cognitive and neural

ﬂexibility in patients with major depressive disorder. Transl. Psychiatry
11, 1–10 (2021).

### 29. Demertzi, A. et al. Human consciousness is supported by dynamic

complex patterns of brain signal coordination. Sci. Adv. 5, eaat7603
(2019).

### 30. Solovey, G. et al. Loss of Consciousness Is Associated with

Stabilization of Cortical Activity. J. Neurosci. 35, 10866–10877 (2015).

### 31. Marona-Lewicka, D., Thisted, R. A. & Nichols, D. E. Distinct temporal

phases in the behavioral pharmacology of LSD: dopamine D2
receptor-mediated effects in the rat and implications for psychosis. Psychopharmacology 180, 427–435 (2005).

### 32. Strassman, R. J. Human psychopharmacology of N, N-

dimethyltryptamine. Behavioural Brain Res. 73, 121–124 (1995).

### 33. Eckernäs, E., Timmermann, C., Carhart-Harris, R., Röshammar, D. &

Ashton, M. N, N-dimethyltryptamine affects electroencephalography
response in a concentration-dependent manner—A
pharmacokinetic/pharmacodynamic analysis. CPT Pharm. Syst. Pharma 12, 474–486 (2023).

### 34. Piccinini, J. et al. Noise-driven multistability vs deterministic chaos in

phenomenological semi-empirical models of whole-brain activity. Chaos: Interdiscip. J. Nonlinear Sci. 31, 023127 (2021).

### 35. Salway, R. & Wakeﬁeld, J. Gamma Generalized Linear Models for

Pharmacokinetic Data. Biometrics 64, 620–626 (2008).

### 36. Deco, G., Kringelbach, M. L., Jirsa, V. K. & Ritter, P. The dynamics of

resting ﬂuctuations in the brain: metastability and its dynamical
cortical core. Sci. Rep. 7, 3095 (2017).

### 37. Hansen, E. C. A., Battaglia, D., Spiegler, A., Deco, G. & Jirsa, V. K. Functional connectivitydynamics: Modeling the switching behavior of
the resting state. NeuroImage 105, 525–535 (2015).

### 38. Kaboodvand, N., van den Heuvel, M. P. & Fransson, P. Adaptive

frequency-based modeling of whole-brain oscillations: Predicting
regional vulnerability and hazardousness rates. Netw. Neurosci. 3,
1094–1120 (2019).

### 39. Jobst, B. M. et al. Increased Stabilityand Breakdown of Brain Effective

Connectivity During Slow-Wave Sleep: Mechanistic Insights from
Whole-Brain Computational Modelling. Sci. Rep. 7, 4634 (2017).
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

### 40. Ipiña, I. P. et al. Modeling regional changes in dynamic stability during

sleep and wakefulness. NeuroImage 215, 116833 (2020).

### 41. Beckmann, C. F., DeLuca, M., Devlin, J. T. & Smith, S. M. Investigations into resting-state connectivity using independent
component analysis. Philos. Trans. R. Soc. B: Biol. Sci. 360,
1001–1013 (2005).

### 42. Murray, C. H. et al. Low doses of LSD reduce broadband oscillatory

power and modulate event-related potentials in healthy adults. Psychopharmacology 239, 1735–1747 (2022).

### 43. Mediano, P. A. M. et al. Effects of External Stimulation on Psychedelic

State Neurodynamics. ACS Chem. Neurosci. 15, 462–471 (2024).

### 44. Dolder, P. C. et al. Pharmacokinetics and Pharmacodynamics of

Lysergic Acid Diethylamide in Healthy Subjects. Clin. Pharmacokinet.
56, 1219–1230 (2017).

### 45. Holze, F., Becker, A. M., Kolaczynska, K. E., Duthaler, U. & Liechti, M. E. Pharmacokinetics and Pharmacodynamics of Oral Psilocybin
Administration in Healthy Participants. Clin. Pharmacol. Therapeutics
113, 822–831 (2023).

### 46. Toker, D. et al. Consciousness is supported by near-critical slow

cortical electrodynamics. Proc. Natl. Acad. Sci. 119, e2024455119
(2022).

### 47. Ort, A. et al. TMS-EEG and resting-state EEG applied to altered states

of consciousness: oscillations, complexity, and phenomenology.
iScience 26, 106589 (2023).

### 48. Helfrich, R. F. et al. Entrainment of Brain Oscillations by Transcranial

Alternating Current Stimulation. Curr. Biol. 24, 333–339 (2014).

### 49. Atasoy, S. et al. Connectome-harmonic decomposition of human

brain activity reveals dynamical repertoire re-organization under LSD. Sci. Rep. 7, 17661 (2017).

### 50. Varley, T. F., Carhart-Harris, R., Roseman, L., Menon, D. K. &

Stamatakis, E. A. Serotonergic psychedelics LSD & psilocybin
increase the fractal dimension of cortical brain activity in spatial and
temporal domains. NeuroImage 220, 117049 (2020).

### 51. Chialvo, D. R. Emergent complex neural dynamics. Nat. Phys. 6,

744–750 (2010).

### 52. Cocchi, L., Gollo, L. L., Zalesky, A. & Breakspear, M. Criticality in the

brain: A synthesis of neurobiology, models and cognition. Prog. Neurobiol. 158, 132–152 (2017).

### 53. Tian, Y. et al. Theoreticalfoundationsof studyingcriticality inthebrain. Netw. Neurosci. 6, 1148–1185 (2022).

### 54. Kaelen, M. et al. LSD enhances the emotional response to music. Psychopharmacology 232, 3607–3614 (2015).

### 55. Kaelen, M. et al. LSD modulates music-induced imagery via changes

in parahippocampal connectivity. Eur. Neuropsychopharmacol. 26,
1099–1109 (2016).

### 56. Luppi, A. I. et al. A role for the serotonin 2A receptor in the expansion

and functioning of human transmodal cortex. Brain 147, 56–80 (2024).

### 57. Roseman, L., Leech, R., Feilding, A., Nutt, D. J. & Carhart-Harris, R. L. The effects of psilocybin and MDMA on between-network resting
state functional connectivity in healthy volunteers. Front. Hum. Neurosci. 8, (2014).

### 58. Petri, G. et al. Homological scaffolds of brain functionalnetworks. J. R. Soc. Interface 11, 20140873 (2014).

### 59. Rocha, R. P. et al. Recovery of neural dynamics criticality in

personalized whole-brain models of stroke. Nat. Commun. 13, 3683
(2022).

### 60. Aday, J. S., Mitzkovitz, C. M., Bloesch, E. K., Davoli, C. C. & Davis, A. K. Long-term effects of psychedelic drugs: A systematic review. Neurosci. Biobehav. Rev. 113, 179–189 (2020).

### 61. Spiegler, A., Hansen, E. C. A., Bernard, C., McIntosh, A. R. & Jirsa, V. K. Selective Activation of Resting-State Networks following Focal
Stimulation in a Connectome-Based Network Model of the Human
Brain. eNeuro 3, (2016).

### 62. Iravani, B., Arshamian, A., Fransson, P. & Kaboodvand, N. Whole-

brain modelling of resting state fMRI differentiates ADHD subtypes
and facilitates stratiﬁed neuro-stimulation therapy. NeuroImage 231,
117844 (2021).

### 63. Cordes, D. et al. Frequencies Contributing to Functional Connectivity

in the Cerebral Cortex in “Resting-state” Data. Am. J. Neuroradiol. 22,
1326–1333 (2001).

### 64. Liu, J., Duffy, B. A., Bernal-Casas, D., Fang, Z. & Lee, J. H. Comparison

of fMRI analysis methods for heterogeneous BOLD responses in
block design studies. NeuroImage 147, 390–408 (2017).

### 65. Chaudhary, U. J., Duncan, J. S. & Lemieux, L. Mapping hemodynamic

correlates of seizures using fMRI: A review. Hum. Brain Mapp. 34,
447–466 (2013).

### 66. Duyn, J. H. EEG-fMRI Methods for the Study of Brain Networks during

Sleep. Front. Neurol. 3, (2012).

### 67. Bréchet, L. et al. Capturing the spatiotemporal dynamics of self-

generated, task-initiated thoughts with EEG and fMRI. NeuroImage
194, 82–92 (2019).

### 68. Good, M. et al. Pharmacokinetics of N, N-dimethyltryptamine in

Humans. Eur. J. Drug Metab. Pharmacokinet. 48, 311–327 (2023).

### 69. Padawer-Curry, J. A. et al. Psychedelic 5-HT2A Receptor Agonism

Alters Neurovascular Coupling in Mice. in Optica Biophotonics
Congress: Biomedical Optics 2024 (Translational, Microscopy, OCT, OTS, BRAIN) (2024), paper JS4A.48 JS4A.48 (Optica Publishing Group,
2024). https://doi.org/10.1364/TRANSLATIONAL.2024. JS4A.48.

### 70. Mueller, F. et al. Acute effects of LSD on amygdala activity during

processing of fearful stimuli in healthy subjects. Transl. Psychiatry 7,
e1084–e1084 (2017).

### 71. Schmidt, A. et al. Acute LSD effects on response inhibition neural

networks. Psychological Med. 48, 1464–1473 (2018).

### 72. Carhart-Harris, R. L. et al. Neural correlates of the psychedelic state as

determined by fMRI studies with psilocybin. Proc. Natl. Acad. Sci.
109, 2138–2143 (2012).

### 73. Grimm, O., Kraehenmann, R., Preller, K. H., Seifritz, E. & Vollenweider, F. X. Psilocybin modulates functional connectivity of the amygdala
during emotional face discrimination. Eur. Neuropsychopharmacol.
28, 691–700 (2018).

### 74. Kasper, L. et al. The PhysIO Toolbox for Modeling Physiological Noise

in fMRI Data. J. Neurosci. Methods 276, 56–72 (2017).

### 75. Chang, C., Thomason, M. E. &Glover, G. H. Mappingandcorrectionof

vascular hemodynamic latency in the BOLD signal. NeuroImage 43,
90–102 (2008).

### 76. Wu, G.-R. et al. rsHRF: A toolbox for resting-state HRF estimation and

deconvolution. NeuroImage 244, 118591 (2021).

### 77. Power, J. D., Barnes, K. A., Snyder, A. Z., Schlaggar, B. L. & Petersen, S. E. Spurious but systematic correlations in functional connectivity MRI
networksarise from subject motion. NeuroImage 59, 2142–2154 (2012).

### 78. Zou, Q.-H. et al. An improved approach to detection of amplitude of

low-frequency ﬂuctuation (ALFF) for resting-state fMRI: Fractional
ALFF. J. Neurosci. Methods 172, 137–141 (2008).

### 79. Cabral, J. et al. Cognitive performance in healthy older adults relates

to spontaneous switching between states of functional connectivity
during rest. Sci. Rep. 7, 5135 (2017).

### 80. Deco, G. et al. One ring to rule them all: The unifying role of prefrontal

cortex in steering task-related brain dynamics. Prog. Neurobiol. 227,
102468 (2023).

### 81. Gu, Y. et al. Abnormal dynamic functional connectivity in Alzheimer’s

disease. CNS Neurosci. Therapeutics 26, 962–971 (2020).

### 82. Tzourio-Mazoyer, N. et al. Automated Anatomical Labeling of

Activations in SPM Using a Macroscopic Anatomical Parcellation of
the MNI MRI Single-Subject Brain. NeuroImage 15, 273–289 (2002).

### 83. Jenkinson, M., Bannister, P., Brady, M. & Smith, S. Improved

Optimization for the Robust and Accurate Linear Registration and
Motion Correction of Brain Images. NeuroImage 17, 825–841 (2002).

### 84. Behrens, T. E. J. et al. Characterization and propagation of uncertainty

in diffusion-weighted MR imaging. Magn. Reson. Med. 50, 1077–1088
(2003).
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409

### 85. Behrens, T. E. J., Berg, H. J., Jbabdi, S., Rushworth, M. F. S. &

Woolrich, M. W. Probabilistic diffusion tractography with multiple ﬁbre
orientations: What can we gain? NeuroImage 34, 144–155 (2007).

### 86. Hansen, J. Y. et al. Mapping neurotransmitter systems to the

structural and functional organization of the human neocortex. Nat. Neurosci. 25, 1569–1581 (2022).
87. juanpiccinini. juanpiccinini/DMT-whole-brain: DMT_whole_brain. Zenodo https://doi.org/10.5281/ZENODO.14588378 (2025). Acknowledgements
E. T. is supported by PICT-2019–02294 (Agencia I + D + i, Argentina), ANID/
FONDECYT Regular 1220995 (Chile) and by PIP 1122021010 0800CO
(2022-2024) (CONICET, Argentina). The collectionofthe empirical data used
in thismanuscript was funded via a donation by Patrick Vernon, mediated by
the Beckley Foundation. C. T. is funded by a donation by Anton Bilton to the
Centre for Psychedelic Research. Author contributions
J. I. P., Y. S.-P., C. P. and E. T. designed the research. J. I. P. conducted the
research. J. I. P., Y. S.-P. and E. T. analyzed and interpreted the results. J. I. P.
created the code and made the ﬁgures. D. N, R. C.-H. and C. T. provided the
curated data. J. I. P. and E. T. wrote the manuscript. C. P., G. D, M. K. provided
analyticsupport. Y. S.-P.and E. T.supervised the research. All authors edited
the manuscript. Competing interests
The authors declare no competing interest. E. T. is an Editorial Board
Member for Communications Biology, but was not involved in the editorial
review or the decision to publish this article. Additional information
Supplementary information The online version contains
supplementary material available at
https://doi.org/10.1038/s42003-025-07576-0. Correspondence and requests for materials should be addressed to
Juan Ignacio Piccinini or Enzo Tagliazucchi. Peer review information Communications Biology thanks the anonymous
reviewers for their contribution to the peer review of this work. Primary
Handling Editors: Laura Rodríguez Pérez and Benjamin Bessieres. A peer
review ﬁle is available. Reprints and permissions information is available at
http://www.nature.com/reprints
Publisher’s note Springer Nature remains neutral with regard to
jurisdictional claims in published maps and institutional afﬁliations. Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as long
as you give appropriate credit to the original author(s) and the source,
provide a link to the Creative Commons licence, and indicate if changes
were made. The images or other third party material in this article are
included in the article’s Creative Commons licence, unless indicated
otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons licence and your intended use is not permitted
by statutory regulation or exceeds the permitted use, you will need to
obtain permission directly from the copyright holder. To view a copy of this
licence, visit http://creativecommons.org/licenses/by/4.0/.
© The Author(s) 2025
https://doi.org/10.1038/s42003-025-07576-0
Article
Communications Biology | (2025) 8:409
