# Metastable oscillatory modes emerge from synchronization in the brain spacetime connectome

**Authors:** Joana Cabral
**Year:** D:20
**Subject:** Communications Physics, doi:10.1038/s42005-022-00950-y

---

ARTICLE
Metastable oscillatory modes emerge from
synchronization in the brain spacetime connectome
Joana Cabral
1,2,3,4,14✉, Francesca Castaldo
5,14, Jakub Vohryzek2,6, Vladimir Litvak
5, Christian Bick
7,8,9,10, Renaud Lambiotte
9, Karl Friston
5, Morten L. Kringelbach
1,2,3,11 &
Gustavo Deco6,12,13
A rich repertoire of oscillatory signals is detected from human brains with electro- and mag-
netoencephalography (EEG/MEG). However, the principles underwriting coherent oscillations
and their link with neural activity remain under debate. Here, we revisit the mechanistic
hypothesis that transient brain rhythms are a signature of metastable synchronization,
occurring at reduced collective frequencies due to delays between brain areas. We consider a
system of damped oscillators in the presence of background noise – approximating the short-
lived gamma-frequency oscillations generated within neuronal circuits – coupled according to
the diffusion weighted tractography between brain areas. Varying the global coupling strength
and conduction speed, we identify a critical regime where spatially and spectrally resolved
metastable oscillatory modes (MOMs) emerge at sub-gamma frequencies, approximating the
MEG power spectra from 89 healthy individuals at rest. Further, we demonstrate that the
frequency, duration, and scale of MOMs – as well as the frequency-speciﬁc envelope functional
connectivity – can be controlled by global parameters, while the connectome structure
remains unchanged. Grounded in the physics of delay-coupled oscillators, these numerical
analyses demonstrate how interactions between locally generated fast oscillations in the
connectome spacetime structure can lead to the emergence of collective brain rhythms
organized in space and time.
https://doi.org/10.1038/s42005-022-00950-y
OPEN

### 1 Life and Health Sciences Research Institute (ICVS), School of Medicine, University of Minho, Braga, Portugal. 2 Centre for Eudaimonia and Human

Flourishing, Linacre College, University of Oxford, Oxford, UK. 3 Center for Music in the Brain, Department of Clinical Medicine, Aarhus University, Aarhus, Denmark. 4 ICVS/3B’s - Portuguese Government Associate Laboratory, Braga/Guimarães, Portugal. 5 Wellcome Centre for Human Neuroimaging, University College London, Queen Square Institute of Neurology, London, UK. 6 Center for Brain and Cognition, Computational Neuroscience Group, Universitat Pompeu Fabra, Barcelona, Spain. 7 Department of Mathematics, Vrije Universiteit Amsterdam, Amsterdam, The Netherlands. 8 Amsterdam
Neuroscience – Systems & Network Neuroscience, Amsterdam, The Netherlands. 9 Mathematical Institute, University of Oxford, Oxford, UK. 10 Department
of Mathematics, University of Exeter, Exeter, UK. 11 Department of Psychiatry, University of Oxford, Oxford, UK. 12 Institució Catalana de la Recerca i Estudis
Avançats (ICREA), Barcelona, Spain. 13 Department of Neuropsychology, Max Planck Institute for Human Cognitive and Brain Sciences, Leipzig, Germany.
14These authors contributed equally: Joana Cabral, Francesca Castaldo. ✉email: joanacabral@med.uminho.pt
COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

1234567890():,; T
he human brain is one of the most complex networks in
nature, exhibiting a rich repertoire of activity patterns
organized not only in space and time but also in the fre-
quency domain. Indeed, rhythmicity is a central property of brain
function—and perhaps of all biotic self-organization: from fast
gamma activity in neurons to the life-cycle itself1–4. Within the
broad range of oscillations emerging at frequencies between
0.05 Hz and 500 Hz, the oscillations detected extracranially with
electro- and magnetoencephalography (EEG/MEG) in resting
humans typically peak between 0.5 and 30 Hz, being categorized as
delta (~0.5–4 Hz), theta (~4–8 Hz), alpha (~8–13 Hz), and beta
(~13–30 Hz)5. Notably, these oscillations lock in phase over long
distances, generating metastable spatial topographies lasting up to a
few hundred milliseconds6–8. Falling signiﬁcantly below the range of frequencies generated in
local neuronal networks by feedback inhibition (>35 Hz, in the
gamma-frequency range), it is generally agreed that sub-gamma
oscillatory activity does not have a purely local origin and is asso-
ciated with synchronization between distant neural assemblies9–14. Notably, there is a relation between the distance over which syn-
chronization is observed and the frequency of the synchronized
oscillations15–17. Speciﬁc brain circuitries, including among others
the thalamocortical loop, have been proposed to play a role in
the generation of rhythmic activity18–20, which appears disrupted
in neurological/neuropsychiatric disorders1,21. Still, the funda-
mental mechanisms driving the spontaneous emergence of short-
lived spatially and spectrally resolved oscillatory patterns remain
unclear9,22–24. Given the spatial distance and the ﬁnite propagation speed,
interactions between brain areas are intrinsically time-delayed,
which can manifest in network activity in the frequency domain. Indeed, delay-coupled limit-cycle oscillators have been demon-
strated to synchronize at frequencies slower than the natural
frequency of the oscillators, leading to a form of collective fre-
quency emerging from synchronization mechanisms25,26. Brieﬂy,
when N phase oscillators—with natural frequency ω—are coupled
together with a time delay τ, they synchronize at a delay- and
interaction-dependent collective frequency Ω given by Ω = ω
/(1 + K*N*τ), where K is the global coupling strength25. How-
ever, this phenomenon has so far only been demonstrated for
networks of limit-cycle oscillators25, and it is unclear how it
generalizes to systems where oscillations are not self-sustained,
but instead emerge only transiently. Computational models have proved helpful for demonstrating
how the brain’s complex network structure of long axonal
projections connecting brain areas—the so-called structural
connectome27—can shape brain activity in space and time28–36. Particularly, simulations of oscillatory units interacting in the
connectome reveal a critical regime where different subsets of units
temporarily synchronize and desynchronize, leading to transiently
correlated
activity
across
spatially
segregated
units20,30,31,37. This reinforces the hypothesis that long-range functional con-
nectivity between brain areas is driven by synchronization
mechanisms24,38–42. Importantly, when considering realistic time
delays in the Kuramoto model of coupled phase oscillators, periods
of increased synchrony are accompanied by increased power at
slower frequencies, generating spatially-organized band-limited
power ﬂuctuations similar to the ones captured with MEG20. While
these numerical results revealed the critical role of time delays to
generate collective oscillations at reduced frequencies, it remains to
be veriﬁed whether this phenomenon holds in the more realistic
setting, wherein local oscillations have ﬂuctuating amplitude—
which is neglected in the Kuramoto model—,as observed empiri-
cally in electrophysiological recordings of neural activity43,44. Furthermore, understanding the parameters that control the
duration, size and occupancy of collective oscillations is crucial to
inform the prediction of therapeutic strategies aimed at modulating
dysfunctional oscillatory brain activity. To address these fundamental questions, we build a phenom-
enological brain network model with realistic connectivity and
time delays, where each node is described by a Stuart–Landau
oscillator operating in the subcritical regime, i.e., responding to a
stimulus with an oscillation with decaying amplitude34,35,45. As
the amplitude dynamics introduces an additional degree of
complexity, it needs to be veriﬁed if the analytic predictions made
for coupled limit-cycle oscillators46 (valid for phase oscillators or
supercritical Stuart–Landau oscillators) still hold47. Selecting

### 40 Hz as a typical frequency of gamma oscillations, we set all

units with identical natural frequency to exclude additional effects
of frequency dispersion48,49, and perturb all units with uncorre-
lated white noise, considering that units resonate at their natural
frequency in the presence of background noisy activity50. Assuming the generalizability of collective synchronization fre-
quencies to delay-coupled damped oscillators, we hypothesize to
identify a critical range of global model parameters (global cou-
pling and conduction speed) where metastable synchronization
generates the transient emergence of sub-gamma collective
oscillations, approximating features of human MEG recordings. Results
Dynamical
regimes
of
the
brain
network
model. The
reduced brain network model comprises N = 90 dynamical units
Fig. 1 Reducing the brain to a system of oscillators coupled in Connectome spacetime structure. a The phenomenological brain network model consists
in N = 90 nodes representing brain regions with links representing diffusion tracts between them. b A Stuart–Landau oscillator in the subcritical regime
responding to perturbation (vertical arrow) with an oscillation with decaying amplitude. c In the supercritical regime, the Stuart–Landau oscillator enters a
limit-cycle (with constant amplitude), approximating a phase oscillator. ARTICLE
COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y

COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

representing anatomically deﬁned brain areas coupled according
to a normative structural connectome of the human brain (see
Methods—Structural Connectome) with reciprocal (i.e., bidirec-
tional/symmetric) coupling CNxN and distance DNxN matrices
(Fig. 1a). Each unit is described by a Stuart–Landau oscillator
operating in the subcritical (underdamped) regime, such that
when perturbed it decays to a ﬁxed-point equilibrium with a
damped oscillation at a natural frequency ω (Fig. 1b), in contrast
with the supercritical regime, where the oscillations are in a limit
cycle (Fig. 1c, see Methods and Supplementary Note 1). To verify that novel frequencies emerge purely from delayed
interactions, the natural frequency of all units is set at ω = 40 Hz
(representing the resonant frequency of isolated neural masses
driven by feedback inhibition) and each unit is perturbed with
uncorrelated white noise. The model—represented mathemati-
cally by a system of stochastic delay coupled differential equations
—is solved numerically for two parameter ranges: the global
coupling strength, K, which scales all pairwise connections, and
the mean conduction delay, 〈τ〉, which scales the time delays
between units in proportion to the diffusion tract lengths (Fig. 2,
see Methods for details). The synchrony degree of the system, evaluated using the
Kuramoto Order Parameter (KOP), is modulated by the global
coupling strength K: for weak coupling, the synchrony is low, and
all units exhibit oscillations close to the natural frequency ω
(Fig. 2a). In the critical range between incoherence and full
synchrony, periods of weakly stable synchronization drive slow
ﬂuctuations in the KOP (Fig. 2b). For sufﬁciently strong coupling,
all units tend to synchronize at a global collective frequency Ω,
which, in the presence of time-delays, is distinct from the natural
frequency ω (Fig. 2c). Observing the levels of synchrony and metastability across the
range of parameters explored (Fig. 2d, e), we ﬁnd that the critical
value of K above which the system can synchronize increases
logarithmically with the mean delay, in line with analytic
predictions for coupled oscillators with heterogeneous delays51
(see Supplementary Note 2 and Supplementary Fig. 5). When
synchronization occurs in the presence of delays, we observe a
sharp decrease in the global peak frequency (Fig. 2f), closely
approximating
the
analytic
prediction
given
by

## Ω =

ω /(1 + K*N*〈τ〉) (Fig. 2g, see also Supplementary Note 2 and
Supplementary Fig. 6). These ﬁndings serve to verify that the phenomenon of
synchronization at reduced collective frequencies is not restricted
to coupled phase oscillators and generalizes to units in the
subcritical regime, where damped oscillations emerge in response
to perturbation (Supplementary Fig. 7). Further, it demonstrates
that the peak frequency of synchronization can be predicted
analytically from global variables such as the mean natural
frequency ω, the number of units N, the coupling strength K,
and the mean delay 〈τ〉. The robustness of this prediction to
distributed natural frequencies is reported in Supplementary Fig. 8. Simulations reveal spectral features of human brain activity. One characteristic feature of MEG (and EEG) signals from
healthy humans at rest is the transient emergence of oscillations
in the alpha frequency range (~8–13 Hz), resulting in a peak in
the power spectrum whose prominence varies strongly across
people (see Fig. 3a for the normalized power spectrum of MEG
signals from 89 healthy young adults resting with eyes open from
the Human connectome Project (HCP) open-source database;
details in Methods section, individual power spectra reported in
Supplementary Fig. 9). We ﬁnd that the brain network model approximates the
average MEG power spectrum of awake resting subjects within
the critical region of high metastability where synchronization
occurs at reduced collective frequencies (comparing Fig. 3c with
Fig. 2e, f). In detail, for each pair of model parameters we
calculate the squared Euclidean distance between the power
spectrum of the simulated signals (Fig. 3b) and the MEG power
spectrum averaged across all sensors and all subjects (Fig. 3a),
revealing the greatest disparity when no delays are considered or
if the global coupling is too weak (see Methods for details). Given the observed (and well-established) variability between
MEG power spectra across individuals (Fig. 3a), we investigate
the extent to which this variability can be associated with changes
in global model parameters, while keeping the structural
connectivity unchanged. To do so, we identify the pair of model
parameters that approximates the individual MEG power spectra
of each of the 89 participants, falling in 29 pairs of parameters
(white asterisks in Fig. 3c, see also Supplementary Fig. 10). Notably, this reveals a conﬁned region in parameter space for
a range of average delays 〈τ〉of 2–11 milliseconds, with
slight changes in the coupling strength and conduction speed
maximizing the ﬁt to individual MEG power spectra, while the
structural connectivity remains unchanged. These results do not
exclude the role of individual variability in structural connectivity
across subjects but reveal additional parameters that modulate a
network’s frequency spectrum. This serves to demonstrate that
the same connectome structure can support distinct activity
patterns depending on global model parameters, with longer/
shorter time delays and stronger/weaker coupling inducing shifts
in the peak frequency and modulating the distribution of power
across the spectrum (Fig. 3b). Metastable oscillatory modes emerge from weakly stable cluster
synchronization. In the range of parameters where the model
optimally approximates the power spectrum of MEG signals,
ﬂuctuations in the magnitude of the order parameter are driven
by metastable cluster synchronization. In other words, when the
coupling is strong, but not sufﬁciently strong to stabilize full
synchronization, some subsets of units that are more strongly
connected together (i.e., clusters/communities) can engage in
partially-synchronized modes that remain stable for a short
period in time. Given the presence of time delays, these clusters
do not synchronize at the natural frequency of the individual
units (ω = 40 Hz), but instead synchronize at slower cluster-
speciﬁc collective frequencies, leading to the emergence of
metastable oscillatory modes (MOMs) at sub-gamma frequencies. To detect the occurrence of MOMs and characterize them in
space and time, we band-pass ﬁlter the simulated signals in four
frequency bands (delta 0.5–4 Hz, theta 4–8 Hz, alpha 8–13 Hz,
and beta 13–30 Hz). In Fig. 4, a colored shade is added when the
amplitude in each frequency band exceeds 5 standard deviations
of the amplitude in that same frequency range detected in
simulations without delays (see Supplementary Note 3, Supple-
mentary Fig. 11). As shown in Fig. 4, we ﬁnd that MOMs are structured both in
space and in time. Speciﬁcally, the units synchronizing together
exhibit the simultaneous emergence of an oscillation at the same
collective frequency, leading to the vertical alignment of shaded
areas, particularly visible for the alpha frequency range in Fig. 4a. Notably, for different sets of parameters, the conﬁguration of
Fig. 4a changes strongly. Indeed, while for very weak coupling,
almost no supra-threshold oscillations are detected (Supplemen-
tary Fig. 12), for stronger coupling, globally synchronized supra-
threshold oscillations emerge transiently in the delta band
(Fig. 5a). For longer delays, oscillations are detected with a less
deﬁnitive temporal alignment between brain areas (Supplemen-
tary Fig. 13). COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y
ARTICLE
COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

Fig. 2 Collective oscillations emerge at reduced frequencies from time-delayed synchronization. The system of N = 90 coupled oscillators, Z, was
simulated for 50 s in the presence of white noise, varying only two global parameters: the Global Coupling K (increasing exponentially to better capture the
effect of delays) and the conduction speed, which scales the Mean Conduction Delay. a–c To illustrate the effect of the coupling strength in the frequency
of synchronization, the collective signal given by ∑N
n¼1Zn. with N = 90 is reported for three levels of global coupling, keeping the same mean conduction
delay of 5 milliseconds. The corresponding power spectra are reported on the right of each plot, and the Kuramoto Order Parameter (KOP) is reported
below. For weak coupling (a) the simulated signal exhibits oscillations peaking close to the node’s natural frequency. For intermediate coupling (b), weakly
stable synchronization generates transient oscillations at reduced frequencies. For strong coupling (c), global synchronization becomes more stable, and all
units are entrained in a collective oscillation at a reduced frequency. For intermediate coupling, ﬂuctuations in the order parameter are indicative of
metastability. d–g For each simulation across the parameters explored, we report: (d) the mean of the KOP (referred to as Synchrony); (e) the standard
deviation of the KOP (referred to as Metastability87); (f) the peak frequency of the simulated collective signal; (g) the synchronization frequency predicted
analytically, showing agreement with simulation results for sufﬁcient synchrony. ARTICLE
COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y

COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

Furthermore, the power at sub-gamma frequencies is found to
correlate strongly with the instantaneous phase synchronization
evaluated by the KOP over time (r = 0.7595 and r = 0.8247 for
Figs. 4b and 5b correspondingly). This demonstrates that the
emergence of oscillations at sub-gamma frequencies in the
simulations is modulated by ﬂuctuations in the synchrony degree. We further deﬁne quantitative metrics to characterize the
MOMs emerging at different frequency bands for different sets of
model parameters in terms of their duration (i.e., consecutive time
that the power remains above threshold), their size (i.e., the number
of units simultaneous displaying power above threshold) and
occupancy (i.e., the proportion of time that the power is detected
above threshold). As can be seen in Fig. 6, in the range of
parameters where optimal ﬁts to MEG data are obtained (Optimal
Range), the alpha MOMs last longer, recruit more units and occur
more often. Importantly, we demonstrate that global parameters,
such as the coupling strength and the conduction speed, modulate
the spatiotemporospectral properties of the whole system in a non-
trivial way, while the dynamics at the local level and the underlying
structural network remain unchanged. The implicit sensitivity to global model parameters is illustrated
in Fig. 7, where the emergence of supra-threshold oscillations in
different frequency bands is represented in the brain at a single
time point for ﬁve distinct sets of parameters. The evolution over
time is shown in Supplementary Movie 1. Frequency-speciﬁc functional connectivity. To link with studies
of functional connectivity in MEG, we further investigate how the
model parameters modulate the correlation between the ampli-
tude envelopes across frequency bands. To do so, we band-pass
ﬁlter the signals in each frequency band, extract the amplitude of
the Hilbert transform and report the envelope correlation
matrices in Fig. 8 for each frequency band and for four repre-
sentative sets of model parameters. For weak coupling, the
envelope correlations are close to zero (Pearson’s correlation
coefﬁcient cc < 0.1 for all pairs of brain areas), indicating that the
coupling is insufﬁcient to drive functional connections between
brain areas. For global parameters in the optimal range (here
K = 10 and 〈τ〉= 3 ms), different brain areas exhibit correlated
envelopes, with stronger correlations (up to cc = 0.78) being
detected in the alpha frequency range. In contrast, for strong
coupling the functional connectivity in the alpha band is reduced
(maximum pairwise correlation of cc = 0.25), while the envelopes
of delta and theta oscillations are strongly correlated across the
brain (up to cc = 0.89). Keeping the optimal range of global
coupling, K = 10, but increasing the delays to an average of
〈τ〉= 20 ms, envelope functional connectivity is detected mostly
in the delta frequency range. This illustrates how, given the same
underlying spacetime network structure (i.e., the matrices of
coupling weights C and distances D), changes in global para-
meters strongly affect the envelope functional connectivity pat-
terns at different frequency bands. To illustrate the level of functional connectivity across the brain,
next to each correlation matrix in Fig. 8, we represent each area as a
sphere placed at its centre of gravity and colored according to the
strongest correlation with any other brain area. This shows that, for
the optimal range of parameters, the areas exhibiting the strongest
functional connectivity in the alpha band are distributed mostly in
posterior and dorsal cortical areas, aligning with empirical
observations of stronger functional connectivity in the alpha band
in the visual and somatomotor systems. However, it is important to
consider that the speciﬁc spatial conﬁguration of functional
connections is inherently dependent on the resolution and
topology of the structural connectome, which is known to depend
on the parcellation scheme and on the brain parts (i.e., cortical,
subcortical) considered. In Supplementary Methods 1, we perform
the same analysis on data simulated using a structural connectome
including 200 cortical-only brain areas52. These results show that,
while the phenomenology of MOMs is robust to changes in the
parcellation scheme, the spatial speciﬁcity across frequency bands
is sensitive to the parcellation scheme considered (Supplementary
Figs. 16 and 17). Most importantly, this analysis illustrates how
c
Disparity between MEG and Model PS
a
MEG Power Spectrum
* Optimal fit to each subject
Average power across all MEG
sensors for each individual
Average across individuals
Frequency (Hz)
r
e
w
o
P
d
e
sila
m
r
o
N
Mean Conduction Delay (ms)
K
g
nilp
u
o
C
la
b
ol
G
Squared Euclidean Distance
Mean Conduction Delay (ms)
Global Coupling K
b
Model Power Spectra

0.1

Fig. 3 Approximation of human magnetoencephalography (MEG) power spectra (PS) in a critical range of parameters. a MEG power spectra from 89
healthy young adults resting with eyes open from the open-source database of the Human connectome Project. The average power spectrum across
individuals is reported in blue. b For each pair of parameters, the power spectra of the simulated signals (averaged across units and normalized between 0
and 80 Hz) is reported. c Squared Euclidean distance between the MEG power spectrum averaged across all sensors and subjects and the power spectrum
of the simulated signals. Asterisks indicate the sets of parameters that optimally approximate the MEG power spectra of each of the 89 individuals (size
scaled according to the number of subjects in each point). COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y
ARTICLE
COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

frequency-speciﬁc functional connectivity patterns depend sensi-
tively on global variables modulating the distributed dynamics,
while the structural connectivity remains unchanged. Discussion
This work addresses the physical mechanisms underlying brain
rhythms detected empirically, employing a reductionist perspec-
tive to ground the inner complexity of encephalographic signals
to universal theoretical principles53,54. Approaching the problem
from a macroscopic perspective, we focus on the emergent
properties of interacting dynamical units, where the collective
ensemble engages in functionally relevant activity patterns that
cannot be inferred from the isolated units alone55–58. Speciﬁcally, we ﬁrst demonstrate the generalizability of a syn-
chronization mechanism described for networks of delay-coupled
limit-cycle oscillators to networks of delay-coupled damped
oscillators (i.e., in the subcritical range of a Hopf bifurcation). This is important for the neuroscience ﬁeld, since empirical
electrophysiological recordings show that local ﬁeld oscillations in
the gamma-frequency band are not limit-cycle oscillations (as
considered in previous models using the Kuramoto of coupled
oscillators20), but instead emerge only transiently. Therefore, the
substantial reduction of brain areas to phase oscillators in Cabral
et al. (2014) has raised concerns on the generalizability of the
proposed mechanism to more realistic settings, given the
demonstrated importance of considering the amplitude dynamics
on the connectivity between phases46,47,59,60. Subsequently, we extend on previous brain network modelling
works by demonstrating that the synchronization frequency can be
approximated analytically from global model parameters, namely
the number of units, the mean coupling strength, the average time
delay between units, and the mean natural frequency of the units. Regarding the latter, we show that, in the presence of delays, the
system is less sensitive to the spread of frequencies across units, in
line with theoretical predictions25 (Supplementary Fig. 8). These insights are crucial to explain the macroscopic spatio-
temporally organized oscillatory signals detected with EEG/MEG
at sub-gamma frequencies, without explicitly introducing these
oscillations in the model61. Here, we consider that only gamma-
frequency oscillations can be generated at the local neuronal
level, with power at other frequencies resulting purely from
synchronization with time delays. Furthermore, we demonstrate
Fig. 4 Sub-gamma oscillations emerge from weakly stable cluster synchronization. a An example of the simulated signals in all 90 units plotted over
25 s, each representing a brain area from a brain parcellation template, ﬁltered below 30 Hz to highlight the sub-gamma oscillatory activity typically
detected with magnetoencephalography (MEG). Shades indicate the time points of increased power in the delta (yellow), theta (red), alpha (blue) and beta
(green) frequency bands. For each frequency band, the threshold was deﬁned as ﬁve standard deviations (STD) of the amplitude—in the same frequency
bands—when no delays were considered. For the simulations, the resonant frequency, ω0, of all units was set to 40 Hz, the conduction speed was tuned
such that the average delay between units, 〈τ〉, was 3 milliseconds (ms) and the global coupling strength was set to K = 10. b The mean amplitude envelope
(blue) of the ﬁltered signals shown in (a) correlates with a Pearson’s correlation coefﬁcient r = 0.7595 with the phase synchronization evaluated by the
Kuramoto Order Parameter (orange, right y-axis). ARTICLE
COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y

COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

the impact of global model parameters in the modulation of
frequency-speciﬁc collective oscillations emerging across space
and time. The detailed characterization of metastable oscillatory
modes in terms of number of units synchronizing together,
duration and occupancy provides a new framework to analyze
collective brain oscillations complementary to frequency-speciﬁc
envelope functional connectivity analysis. Our hypothesis is endorsed using a phenomenological brain
network model, reduced to its key essential ingredients to allow
efﬁcient numerical approximations to analytic predictions, but at
the same time sufﬁciently complex to allow a fair approximation
of MEG spectral features. The deliberate reductionist perspective
inherent in this brain network model is intended to link with
theoretical works on delay-coupled oscillatory systems25,51,62,63. Towards this end, we consider identical units with same natural
frequency, same damping coefﬁcient and same noise level, cou-
pled in the structural connectome. Therefore, we focus solely on
the effects of global variables, namely the global coupling K and
the mean conduction delay 〈τ〉in the emerging synchronization
phenomena. To establish the construct validity of our numerical
simulations, we show that the peak synchronization frequency
can be approximated by the analytic prediction derived for
synthetic networks of coupled Kuramoto oscillators with time
delays25. Further, in line with theoretical predictions51,64, we ﬁnd
that the complex spacetime topology of the structural con-
nectome widely expands the critical border between incoherence
and global synchrony where ﬂuctuations in the order parameter
are indicative of metastability25. Despite its simplicity, this model
provides a robust framework to test a theoretically grounded
mechanistic scenario for the spontaneous formation of frequency-
speciﬁc long-range coherence in complex networks. While the investigation of mechanistic principles and control
parameters beneﬁts from reduced complexity, adding hetero-
geneity is certainly needed to improve the ﬁtting to real brain
activity from individuals in different conditions. Building up on
these fundamental aspects, additional degrees of complexity can
be added to the model, namely by considering more ﬁne-grained
connectome structures, considering non-homogeneous intrinsic
frequencies and damping properties, or even replacing the noisy
input by dynamic concentration patterns to mimic local neuro-
modulatory effects. Further, given the potential generalizability of
this synchronization mechanism, we expect our analysis may
provide valuable insight to interpret some of the complex self-
organizing phenomena emerging in more realistic biophysical
Fig. 5 Global delta waves emerge for strong coupling. a The simulated signals in all 90 units plotted over 25 s, each representing a brain area from a brain
parcellation template, ﬁltered below 30 Hz to focus on the sub-gamma oscillatory activity typically detected with magnetoencephalography (MEG). Shades
highlight the time points of increased power in the delta (yellow), theta (red), alpha (blue) and beta (green) frequency bands. For each frequency band, the
threshold was deﬁned as ﬁve standard deviations (STD) from the amplitude in the same frequency bands when no delays were considered. These
simulations were performed setting the resonant frequency of all units ω0 = 40 Hz, the average delay between units, 〈τ〉= 3 milliseconds (ms) and the
global coupling strength was increased to K = 50 with respect to the simulations shown in Fig. 4. b The mean amplitude envelope (blue) of the ﬁltered
signals shown in (a) correlates with r = 0.8247 with the phase synchronization evaluated by the Kuramoto Order parameter (orange, right y-axis). COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y
ARTICLE
COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

models of neural networks65,66 for which a precise analytic pre-
diction cannot be solved. Our ﬁndings reinforce the idea that conduction delays—often
neglected in network models of whole brain activity due to the
added complexity—play a crucial role in shaping the frequency
spectrum of coupled oscillatory systems. Although the frequency
of the oscillations considered herein is relatively fast with respect
to the ultra-slow ﬂuctuations (<0.1 Hz) detected with functional
Magnetic Resonance Imaging (fMRI), it is important to highlight
that metastable synchronization drives power ﬂuctuations on
ultra-slow timescales, and therefore, even relatively short time
delays can signiﬁcantly modulate spontaneous activity at ultra-
slow time-scales. We note that for the numerical integration of
stochastic delay differential equations to be stable and align with
analytic predictions, the time step for numerical integration needs
to be sufﬁciently small and a running history needs to be saved
for the length of the maximum delay between units, which sig-
niﬁcantly increases the computation times when compared to
simulations where delays are neglected (here the numerical results
were found to stabilize for dt ≤10−4 s, see Supplementary
Figs. 18–20). The discovery of multistability in systems of delay-coupled
oscillators, initially described in 1999 by Young and Strogatz62
and extended to heterogeneous delays in 2009 by Lee, Ott and
Antonsen51, was crucial to develop the theoretical hypothesis
behind this work, opening grounds to speculate that this phe-
nomenon may be related to the maintenance of the right balance
between integration and segregation in living brains67,68. Beyond
the range where the model best approximates healthy awake
brain activity, we ﬁnd that higher coupling enhances global
order, where the whole brain displays slow coherent oscillations
in the delta-range (0.5–2 Hz), which nicely approximate the most
powerful brain rhythms detected during unconscious states
such as slow-wave sleep, coma or anaesthesia. On the other
hand, operating at weaker coupling hinders the formation of
MOMs at sub-gamma frequencies, altering the spectral proﬁle
similarly to what is observed in M/EEG recordings of patients
with neuropsychiatric disorders associated to disconnection,
such as schizophrenia, where the power in alpha appears to
be
signiﬁcantly
reduced69–72. Such
abnormal
interactions
within cortico-subcortical oscillatory networks may emerge from
speciﬁc
local
deregulation
or
neural
circuit
disruption73. However, how a local change may alter the communication
between brain-areas and brain network dynamics remains an
open question. Overall, these results are aligned with recent
works proposing that spontaneous transitions between multiple
space-time patterns on complex networks provide a solid theo-
retical framework for the interpretation of the non-stationary
but recurrent macroscopic patterns emerging spontaneously in
brain activity, and ultimately supporting brain function74,75. From a technical perspective, it may be surprising that this kind
of itinerant dynamics emerges under symmetrical coupling
between nodes; in the sense that asymmetric coupling is nor-
mally required for breaking detailed balance—and engendering
Fig. 6 Characterization of metastable oscillatory modes (MOMs) emerging from the system. For different Global Coupling strength (K) and Conduction
Delays 〈τ〉, MOMs are characterized in terms of duration (i.e., consecutive time that the power remains above threshold), size (i.e., the number of units
simultaneous displaying power above threshold) and occupancy (i.e., the proportion of time that the power is detected above threshold over the entire
simulation), for each frequency band. This demonstrates that the same network structure, i.e., the connectome, can exhibit different oscillatory modes
organized in space and in time, depending on global parameters of the system. In the critical range of parameters (Optimal Range), oscillations in the alpha
frequency band emerge more frequently and involve more units. Globally synchronized delta oscillations—as typically observed in states of reduced
consciousness—are associated to an increase in the global coupling strength (Strong Coupling). Error bars represent 1 standard deviation. See also
Supplementary Movie 1. ARTICLE
COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y

COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

stochastic chaos of the sort described above. However, the
dynamics of each node are generated with asymmetric Jacobians,
suggesting that symmetry breaking of intrinsic connectivity is
a sufﬁcient condition for the nonequilibrium dynamics that
characterize real brains. While metastability appears to be crucial for brain function,
the speciﬁc role of MOMs to support cognitive functions
remains unclear4,24,68,76,77. One possibility is that the areas
engaged in a MOM are directly involved in long-range func-
tional integration, but another is that these areas are inhibited
by entering in a collective low-energy mode13,39. Shedding some
light on this open question, we ﬁnd that synchronization with
delays induces not only a shift to slower frequencies but also a
decrease in amplitude, in line with theoretical studies reporting
amplitude death in systems with distributed delays78 (see the
vertical axes in Fig. 2a–c, top panels). From a ‘metabolic’ per-
spective, this shows that MOMs can be approached as ‘low-
energy modes’ with respect to high power gamma oscillations,
providing a physical explanation for the emergence of the so-
called ‘idle rhythms'79. Although the functional implications of
this mechanism are beyond the scope of this work, we expect it
will provide fertile grounds for the formulation of novel falsi-
ﬁable predictions to be further tested. Moreover, these ﬁndings
give room to further investigations of how local perturbations
can affect the spatiotemporospectral dynamics on the macro-
scopic scale, to gain insight on the mechanisms of action of
perturbative strategies such as transcranial magnetic stimulation
or deep brain stimulation. Methods
Ethics statement. All human data used in this study is from the public repository
of the Human Connectome Project (HCP)80 (https://www.humanconnectome.org),
which is distributed in compliance with international ethical guidelines. Structural connectome. The NxN matrices of structural connectivity, C, and
distances, D, used for the network model were derived from a probabilistic
tractography-based normative connectome provided as part of the leadDBS tool-
box (https://www.lead-dbs.org/)81. This normative connectome was generated
from diffusion-weighted and T2-weighted Magnetic Resonance Imaging (MRI)
from 32 healthy participants (mean age 31.5 years old ± 8.6, 14 females) from the
HCP. The diffusion-weighted MRI data was recorded for 89 min on a specially-
designed MRI scanner with more powerful gradients then conventional scanners. The dataset and the acquisition protocol details are available in the Image & Data
Archive under the HCP project (https://ida.loni.usc.edu/). DSI Studio (http://dsi-
studio.labsolver.org) was used to implement a generalized q-sampling imaging
algorithm to the diffusion data. A white-matter mask, derived from the segmen-
tation of the T2-weighted anatomical images, was used to co-register the images to
the b0 image of the diffusion data using the SPM12 toolbox (https://www.ﬁl.ion.
ucl.ac.uk/spm/software/spm12/). Within the white-matter mask, 200,000 most
probable ﬁbres were sampled for each participant. Then, ﬁbres were transformed to
the standard Montreal Neurological Institute (MNI) space applying a nonlinear
deformation ﬁeld derived from the T2-weighted images via a diffeomorphic
registration algorithm82. The individual tractograms were then aggregated into a
joint dataset in MNI standard space resulting in a normative tractogram repre-
sentative of a healthy young adult population and made available in the leadDBS
toolbox81. The NxN matrices were computed from the normative tractogram using the
Automated Anatomical Labelling (AAL) parcellation scheme83 with N = 90
cortical and subcortical areas, by calculating the number of tracts, C(n,p), and mean
tract length, D(n,p), between the voxels belonging to each pair of brain areas n and
p. Further details on the structural matrices in the AAL and other parcellation
schemes are reported in Supplementary Methods 1 and Supplementary Fig. 14. Long delays < >=10ms K=10
No delays < >=0ms K=10
Weak Coupling < >=3ms K=0.1
Conduction Delays
Optimal Point < >=3ms K=10
Strong Coupling < >=3ms K=50
Global Coupling
Delta [0.5-4] Hz
Theta [4-8] Hz
Alpha [8-13] Hz
Beta [13-30] Hz
Fig. 7 Metastable Oscillatory Modes (MOMs) emerge transiently from interactions in the Connectome spacetime structure only for sufﬁcient coupling
and conduction times. Each brain area is represented as a sphere located at its centre of gravity. A color code is used to highlight the brain areas with
power exceeding ﬁve standard deviations from the baseline power at a given time point. This image is a still frame from Supplementary Movie 1. While the
structural connectome is the same for all simulations, MOMs only emerge at reduced frequencies in the presence of Conduction Delays 〈τ〉and for
sufﬁcient Coupling strength (K). COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y
ARTICLE
COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

MEG power spectra from healthy participants. The power spectra from
human resting-state MEG signals were also downloaded from the HCP database
as a FieldTrip structure in a MATLAB ﬁle. The MEG power spectra are provided
for 89 healthy participants at rest (mean age 28.7 years old, range 22–35, 41
female) distinct from the 32 participants from which the structural connectomes
were derived, but with similar age range and gender ratio. Resting-state
MEG signals were recorded on a Magnes 3600 MEG (4D NeuroImaging) with
248 magnetometers for 6 min and the “powavg” pipeline was used to obtain
the power spectrum of the resting-state MEG data in each MEG sensor. Brieﬂy, the signals were segmented, Hanning-tapered, Fourier-transformed
and the power spectrum was averaged over all segments. Notch ﬁlters were
applied to remove the power line noise (cut-off frequencies 59–61 Hz and
119–121 Hz). Additional details are explained in the HCP reference manual
(https://humanconnectome.org/storage/app/media/documentation/s1200/HCP_
S1200_Release_Reference_Manual.pdf). The MEG power spectra were
averaged across the 248 sensors to obtain a power spectrum representative of
each subject. Brain network model. The Stuart–Landau (SL) equation (ﬁrst term in Eq. 1) is
the canonical form to describe the behavior of a system near an Andronov–Hopf
bifurcation, i.e. exhibiting the birth of an oscillation from a ﬁxed point40,84. In
other words, it is used to describe systems that have a static ﬁxed point (like a
resting spring), but respond to perturbation with an oscillation, which may
damped or self-sustained depending on the operating point of the system with
respect to the bifurcation (see Supplementary Note 1 and Supplementary
Figs. 1–4). This model allows to describe complex-systems behavior among
several applications, bridging the gap between the simplicity of the Kuramoto
model and the extensiveness of the phase-amplitude frameworks85,86. It
describes how the oscillator behaves both when it is weakly attracted to a limit
cycle (displaying only damped oscillations in response to perturbation) and, on
the other hand, when it is purely restricted to a limit cycle (oscillations remain
self-sustained). Our analysis is based on a system of N = 90 SL oscillators coupled in the
connectome, considering both the connectivity strength, Cnp, and the conduction
delays, τnp, between each pair of brain areas n and p. The conduction delays are
deﬁned in proportion to the ﬁber lengths between brain areas, assuming an
homogenous conduction speed v, such that τnp ¼ Dnp=v, where Dnp is the length of
the ﬁbres detected between brain areas n and p. To simulate how the activity in
node n is affected by the behavior of all other nodes p ðp 2 N ^ p≠nÞ, we describe
the interaction between nodes in the form:
dZn
dt ¼ Zn a þ iω  Z2
n




þ K∑N
p≠nCnp Zp t  τnp


 Zn tð Þ
h
i
þ βη1 þ iβη2; 8n 2 N;
ð1Þ
where the complex variable Zn(t) describes the state of the nth oscillator at time
t. The ﬁrst term in Eq. (1) describes the intrinsic dynamics of each unit, the
second term describes the input received from coupled units and the last terms
represent uncorrelated white noise (see Supplementary Note 2 for detailed
analysis of the model). With this approach, we consider that the ﬁrst term of Eq. 1 represents the
natural excitability of neuronal assemblies, where ω ¼ 2π  f f is the angular
frequency, with ff as the fundamental frequency in Hertz. For our proof of
concept, we set all nodes with identical natural frequency ω0 ¼ 2π  40Hz,
representing the undifferentiated ability of a neural mass to engage in gamma-
frequency oscillations. The parameter a determines the position of the each unit with respect to the limit
cycle. For a > 0, a stable limit cycle appears via a superciritical Hopf bifurcation, while
when a < 0 there is only a stable ﬁxed point at the origin Zn = 0, so the bifurcation
point is at a = 0. Importantly, if a is sufﬁciently close to the bifurcation, the system is
still weakly attracted to the limit cycle and damped oscillations emerge in response
to external input, with a decay time scaled by a. In this work, we pick a value of
a = −5 for all nodes, such that a single input drives a damped oscillation decaying
after ~1 s, approximating the slowest decay time-constants of inhibitory receptors
(Supplementary Fig. 4) (τdecay(GABAB) ≈500–1000 ms). In Supplementary Note 2
and Supplementary Fig. 7 we show that our results are qualitatively similar for a
broad range of a values, both positive and negative, thus demonstrating the
generalizability of synchronization at collective frequencies to coupled oscillatory
systems with ﬂuctuating amplitude, be they damped or self-sustained. We note that
this mechanism only fails when the units have an overdamped response (exponential
decay without oscillation), which, in this case, only occurred for a = −500. Thus it is
of great interest in future research to investigate whether the local bifurcation
parameters can be tuned based on sensitive observables to ﬁt the MEG data of
different individuals in different conditions. The second term represents the total input received from other brain areas,
scaled by parameter K, which sets the strength of all network interactions with
respect to the intrinsic node dynamics. Because we wish to focus on the nonlinear
Long Delays
=20ms K=10
Weak Coupling
=3ms K=0.1
Strong Coupling
=3ms K=50
Optimal Range
=3ms K=10
13-30Hz
8-13Hz
4-8Hz
0.5-4Hz
Brain areas
Brain areas
max(FC)
Fig. 8 Inﬂuence of global model parameters in frequency-speciﬁc envelope functional connectivity patterns. For 4 simulations obtained with different
Global Coupling strength (K) and Conduction Delays 〈τ〉, we report the frequency-speciﬁc functional connectivity (FC) estimated as the correlation
matrices of the envelopes of signals band-pass ﬁltered in the delta (δ), theta (θ), alpha (α) and beta (β) frequency bands. The colormap limits of the
matrices are scaled by the maximum absolute correlation and centred at zero. Next to each matrix, each of the N = 90 brain areas is represented as a
sphere placed in its centre of gravity and colored according to the maximum envelope FC to any other brain area (same colorbar applied to all spheres,
scaled between −1 and 1). ARTICLE
COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y

COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

phenomena introduced by time delays, we model the node-to-node interactions
using a particular linear diffusive coupling, as the simplest approximation of the
general coupling function, considering delayed interactions. Here, the signal of
node n at time t is calculated with respect to the activity of all other nodes p at time
t  τnp (where τnp is the time delay between n and p), scaled by the relative
coupling strength given by Cnp. The third term of Eq. 1 represents the added uncorrelated noise to each unit
(with real and imaginary components η1 and η2). In this analysis, the system is
perturbed with uncorrelated white noise, where η1 and η2 are independently drawn
from a Gaussian distribution with mean zero and standard deviation β ¼ 0:001
(integrated as β*
ﬃﬃﬃﬃ
dt
p
). In this framework, our whole-brain network model is purely bottom-up (i.e.,
not inferred from the MEG data we aim at explaining). For a qualitative
comparison with the literature in delay-coupled oscillatory systems25,51,62, we
explore the network dynamics as a function of the coupling strength K and the
mean delay τh i ¼ D
h i=v, where 〈D〉is the mean length of all ﬁbres detected
between each pair of brain areas. For each set of parameters, the model is solved
numerically for 50 s with an integration step dt = 10−4 s. Kuramoto order parameter. To evaluate the global synchrony of the simulated
network activity over time, we use the Kuramoto order parameter [Eq. 2]: RðtÞeiΘðtÞ ¼ 1

## N ∑

N
n¼1 eiθnðtÞ
ð2Þ
where θnðtÞ is the phase of each node, given by the argument of Zn. The temporal
evolution of the Order Parameter R(t) provides an instantaneous measure of the
degree of synchrony of the ensemble. Since we add noise in the simulations, we ﬁrst
band-pass ﬁlter the signals Zn around the peak frequency of the ensemble. A steady
order parameter indicates a stable solution (be it asynchronous, RðtÞ

~0 or syn-
chronous RðtÞ

~1), whereas ﬂuctuations in the order parameter are indicative of
Metastability, driven by constant transitions between different weakly stable
solutions65,87. For the analysis in parameter space, we take the mean
RðtÞ

as a
measure of the global synchronization while the standard deviation STDðR tð ÞÞ
indicates how much R(t) ﬂuctuates in time87. Analytic prediction of the collective frequency of synchronization. Previous
theoretical studies have shown analytically that coupled oscillatory networks with
homogeneous delays can ﬁnd stable solutions at multiple collective frequencies Ω. Let us consider the Kuramoto transition in a population of phase oscillators deﬁned
by Eq. 3:
_θn tð Þ ¼ ω0 þ K ∑
N
p≠n Cnpsin θp t  τnp


 θn tð Þ
h
i;
ð3Þ
and the fully synchronized, uniformly rotating one-cluster state θn = … = θN = Ωt. Substituting this expression into Eq. 3 we obtain25,26,62,78,88:
Ω ¼ ω0  KNsin Ωτ
ð
Þ
ð4Þ
where ω0 corresponds to the nodes’ intrinsic frequency and τ is the homogeneous
time delay between nodes. As K is increased and full synchrony is approached, the
system ﬁnds an equilibrium point at the lowest stable solution for Eq. 4, which is
given by:
Ωmin ¼ ω0=ð1 þ KNτÞ
ð5Þ
Note that, for collective oscillations to emerge, the global coupling K needs to be
sufﬁciently strong such that the synchronized solutions are at least weakly stable. To approximate the analytic prediction from Eq. (5), the coupling matrix was
normalized by its mean, such that <C> = 1. Model performance. We perform a parameter space exploration by tuning the two
free parameters K and 〈τ〉. We choose to increase K exponentially as a power of 10
from 10−1 to 101.7 in steps of 100.1, to ensure a range that covers from weak to
strong coupling. 〈τ〉is explored in the range from 0 ms to 30 ms in steps of 1 ms. We measure the ﬁtting between the empirical sensor MEG PS for each of the
89 subjects and the simulated PS for each pair of parameters as the squared
Euclidean distance, resulting in one ﬁtting value for each subject. This can be
regarded as a maximum likelihood procedure under the assumption of Gaussian
observation noise. Metastable oscillatory modes. To detect MOMs and characterize them in space
and time, we band-pass ﬁlter the simulated signals in each frequency band and
obtain the corresponding amplitude envelopes using the Hilbert transform for each
band. Subsequently, we consider that a node (or brain area) engages in a MOM if
the amplitude increases ﬁve standard deviations above the baseline amplitude in
that frequency range. We deﬁne the baseline threshold considering the simulations
with the optimal K but with zero delays. Since some areas are more coupled
together than others, even with “zero delays” these areas may exhibit more power
across frequencies that is purely due to noisy interactions. Therefore, we deﬁne a
different threshold for each node and each band. Envelope functional connectivity patterns. Following standard procedures to
estimate frequency-speciﬁc functional connectivity in empirical source-projected
MEG data42, we ﬁrst band-pass ﬁlter the simulated signals in each frequency band
of interest, compute the analytic signal using the Hilbert transform and then cal-
culate the correlation matrices between the amplitude (i.e. the absolute value) of the
analytic signal. This is done in one optimal point (K = 10, 〈τ〉= 3 ms), for weak
coupling (K = 0.1, 〈τ〉= 3 ms), strong coupling (K = 50, 〈τ〉= 3 ms), no delays
(K = 10, 〈τ〉= 0 ms) and long delays (K = 10, 〈τ〉= 20 ms). The same analysis
performed using N = 200 units is shown in Supplementary Methods 1 and Sup-
plementary Fig. 17. Data availability
Human neuroimaging data used in this study were provided by the Human Connectome
Project (HCP)80 (https://www.humanconnectome.org), WU-Minn Consortium
(Principal Investigators: David Van Essen and Kamil Ugurbil; 1U54MH091657) funded
by the 16 NIH Institutes and Centers that support the NIH Blueprint for Neuroscience
Research; and by the McDonnell Center for Systems Neuroscience at Washington
University. The normative connectomes were computed from Human Connectome
Project data and included as part of the leadDBS toolbox81 (https://www.lead-dbs.org/). The matrices computed from the normative connectomes used for simulations, together
with the MEG power spectra from 89 individuals, are publicly available in.mat format at:
https://github.com/fcast7/Hopf_Delay_Toolbox. Simulated data are available from the
corresponding author on reasonable request. Supplementary Notes, Supplementary
Methods and Supplementary Video 1 are available with this paper. Code availability
All simulations were performed in MATLAB2021b. The codes used in this study are
publicly available at: https://github.com/fcast7/Hopf_Delay_Toolbox. Received: 19 November 2021; Accepted: 20 June 2022; References
1. Uhlhaas, P. J. & Singer, W. Neural synchrony in brain disorders: relevance
for cognitive dysfunctions and pathophysiology. Neuron 52, 155–168
(2006).
2. Engel, A. K., Fries, P. & Singer, W. Dynamic predictions: oscillations and
synchrony in top-down processing. Nat. Rev. Neurosci. 2, 704–716 (2001).
3. Buzsáki, G. & Draguhn, A. Neuronal oscillations in cortical networks. Science
304, 1926–1929 (2004).
4. Singer, W. Synchronization of cortical activity and its putative role in
information processing and learning. Annu. Rev. Physiol. 55, 349–374 (1993).
5. Buzsaki, G. Rhythms of the Brain. (Oxford University Press, 2006).
6. Baker, A. P. et al. Fast transient networks in spontaneous human brain
activity. eLife 3, e01867 (2014).
7. Vidaurre, D. et al. Spectrally resolved fast transient brain states in
electrophysiological data. NeuroImage 126, 81–95 (2016).
8. Michel, C. M. & Koenig, T. EEG microstates as a tool for studying the
temporal dynamics of whole-brain neuronal networks: a review. NeuroImage
180, 577–593 (2018).
9. Jensen, O., Spaak, E. & Zumer, J. M. In Magnetoencephalography 359–403
(Springer, 2014).

### 10. Sherman, M. A. et al. Neural mechanisms of transient neocortical beta

rhythms: Converging evidence from humans, computational modeling,
monkeys, and mice. Proc. Natl Acad. Sci. 113, E4885–E4894 (2016).

### 11. Varela, F., Lachaux, J.-P., Rodriguez, E. & Martinerie, J. The brainweb: phase

synchronization and large-scale integration. Nat. Rev. Neurosci. 2, 229 (2001).

### 12. Hipp, J. F., Hawellek, D. J., Corbetta, M., Siegel, M. & Engel, A. K. Large-scale

cortical correlation structure of spontaneous oscillatory activity. Nat. Neurosci.
15, 884–890 (2012).

### 13. Palva, S. & Palva, J. M. Discovering oscillatory interaction networks with M/

EEG: challenges and breakthroughs. Trends Cogn. Sci. 16, 219–230 (2012).

### 14. Traub, R. D., Whittington, M. A., Stanford, I. M. & Jefferys, J. G. A

mechanism for generation of long-range synchronous fast oscillations in the
cortex. Nature 383, 621–624 (1996).

### 15. Schnitzler, A. & Gross, J. Normal and pathological oscillatory communication

in the brain. Nat. Rev. Neurosci. 6, 285–296 (2005).

### 16. Von Stein, A. & Sarnthein, J. Different frequencies for different scales of

cortical integration: from local gamma to long range alpha/theta
synchronization. Int. J. Psychophysiol. 38, 301–313 (2000).

### 17. Nunez, P. L. & Srinivasan, R. Electric ﬁelds of the brain: the neurophysics of

EEG. (Oxford University Press, 2006). COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y
ARTICLE
COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

### 18. Bhattacharya, S., Cauchois, M. B., Iglesias, P. A. & Chen, Z. S. The impact of a

closed-loop thalamocortical model on the spatiotemporal dynamics of cortical
and thalamic traveling waves. Sci. Rep. 11, 1–19 (2021).

### 19. Freyer, F. et al. Biophysical mechanisms of multistability in resting-state

cortical rhythms. J. Neurosci.: Off. J. Soc. Neurosci. 31, 6353–6361 (2011).

### 20. Cabral, J. et al. Exploring mechanisms of spontaneous functional connectivity

in MEG: How delayed network interactions lead to structured amplitude
envelopes of band-pass ﬁltered oscillations. NeuroImage 90, 423–435 (2014).

### 21. Llinás, R. R., Ribary, U., Jeanmonod, D., Kronberg, E. & Mitra, P. P. Thalamocortical dysrhythmia: a neurological and neuropsychiatric syndrome
characterized by magnetoencephalography. Proc. Natl Acad. Sci. 96,
15222–15227 (1999).

### 22. Vidaurre, D. et al. Spontaneous cortical activity transiently organises into

frequency speciﬁc phase-coupling networks. Nat. Commun. 9, 1–13 (2018).

### 23. O’Neill, G. C. et al. Dynamics of large-scale electrophysiological networks: a

technical review. NeuroImage 180, 559–576 (2018).

### 24. Friston, K. J. Transients, metastability, and neuronal dynamics. NeuroImage 5,

164–171 (1997).

### 25. Niebur, E., Schuster, H. G. & Kammen, D. M. Collective frequencies and

metastability in networks of limit-cycle oscillators with time delay. Phys. Rev. Lett. 67, 2753–2756 (1991).

### 26. Atay, F. M., Jost, J. & Wende, A. Delays, connection topology, and

synchronization of coupled chaotic maps. Phys. Rev. Lett. 92, 144101
(2004).

### 27. Sporns, O., Tononi, G. & Kotter, R. The human connectome: a structural

description of the human brain. PLoS Comput. Biol. 1, e42 (2005).

### 28. Honey, C. J., Kotter, R., Breakspear, M. & Sporns, O. Network structure of

cerebral cortex shapes functional connectivity on multiple time scales. Proc. Natl Acad. Sci. USA 104, 10240–10245 (2007).

### 29. Ghosh, A., Rho, Y., McIntosh, A. R., Kotter, R. & Jirsa, V. K. Cortical network

dynamics with time delays reveals functional connectivity in the resting brain. Cogn. Neurodyn. 2, 115–120 (2008).

### 30. Deco, G., Jirsa, V., McIntosh, A. R., Sporns, O. & Kotter, R. Key role of

coupling, delay, and noise in resting brain ﬂuctuations. Proc. Natl Acad. Sci.

## USA 106, 10302–10307 (2009).

### 31. Cabral, J., Hugues, E., Sporns, O. & Deco, G. Role of local network oscillations

in resting-state functional connectivity. NeuroImage 57, 130–139 (2011).

### 32. Cabral, J., Kringelbach, M. & Deco, G. Functional Connectivity dynamically

evolves on multiple time-scales over a static Structural Connectome: Models
and Mechanisms. NeuroImage 160, 84–96 (2017).

### 33. Deco, G. & Kringelbach, M. L. Turbulent-like dynamics in the human brain. Cell Rep. 33, 108471 (2020).

### 34. Deco, G. et al. Single or Multi-Frequency Generators in on-going brain

activity: a mechanistic whole-brain model of empirical MEG data. NeuroImage 152, 538–550 (2017).

### 35. Deco, G., Kringelbach, M. L., Jirsa, V. K. & Ritter, P. The dynamics of resting

ﬂuctuations in the brain: metastability and its dynamical cortical core. Sci. Rep.
7, 3095 (2017).

### 36. Tewarie, P. et al. How do spatially distinct frequency speciﬁc MEG networks

emerge from one underlying structural connectome? The role of the structural
eigenmodes. NeuroImage 186, 211–220 (2019).

### 37. Roberts, J. A. et al. Metastable brain waves. Nat. Commun. 10, 1–17 (2019).

### 38. Ponce-Alvarez, A. et al. Resting-state temporal synchronization networks

emerge from connectivity topology and heterogeneity. PLoS Comput. Biol. 11,
e1004100 (2015).

### 39. Engel, A. K., Gerloff, C., Hilgetag, C. C. & Nolte, G. Intrinsic coupling modes:

multiscale interactions in ongoing brain activity. Neuron 80, 867–886 (2013).

### 40. Cocchi, L., Gollo, L. L., Zalesky, A. & Breakspear, M. Criticality in the brain: a

synthesis of neurobiology, models and cognition. Prog. Neurobiol. 158,
132–152 (2017).

### 41. Deco, G. et al. Rare long-range cortical connections enhance human

information processing. Curr. Biol. 31, 4436–4448. e4435 (2021).

### 42. Brookes, M. J. et al. Measuring functional connectivity using MEG:

methodology and comparison with fcMRI. NeuroImage 56, 1082–1104
(2011).

### 43. Buhl, E. H., Tamas, G. & Fisahn, A. Cholinergic activation and tonic excitation

induce persistent gamma oscillations in mouse somatosensory cortex in vitro. J. Physiol. 513, 117–126 (1998).

### 44. Sanchez-Vives, M. V. & McCormick, D. A. Cellular and network mechanisms

of rhythmic recurrent activity in neocortex. Nat. Neurosci. 3, 1027 (2000).

### 45. Selivanov, A. A. et al. Adaptive synchronization in delay-coupled networks of

Stuart-Landau oscillators. Phys. Rev. E 85, 016201 (2012).

### 46. Daffertshofer, A. & van Wijk, B. C. On the Inﬂuence of Amplitude on the

Connectivity between Phases. Front. Neuroinform. 5, 6 (2011).

### 47. Ashwin, P., Coombes, S. & Nicks, R. Mathematical frameworks for oscillatory

network dynamics in neuroscience. J. Math. Neurosci. 6, 1–92 (2016).

### 48. Strogatz, S. H. & Mirollo, R. E. Stability of incoherence in a population of

coupled oscillators. J. Stat. Phys. 63, 613–635 (1991).

### 49. Petkoski, S., Iatsenko, D., Basnarkov, L. & Stefanovska, A. Mean-ﬁeld and

mean-ensemble frequencies of a system of coupled oscillators. Phys. Rev. E 87,
032908 (2013).

### 50. Samanta, H. S., Bhattacharjee, J. K., Bhattacharyay, A. & Chakraborty, S. On

noise induced poincaré–andronov–Hopf bifurcation. Chaos: Interdiscip. J. Nonlinear Sci. 24, 043122 (2014).

### 51. Lee, W. S., Ott, E. & Antonsen, T. M. Large coupled oscillator systems with

heterogeneous interaction delays. Phys. Rev. Lett. 103, 044101 (2009).

### 52. Schaefer, A. et al. Local-Global Parcellation of the Human Cerebral Cortex

from Intrinsic Functional Connectivity MRI. Cereb. Cortex 28, 3095–3114
(2018).

### 53. Pikovsky, A., Kurths, J., Rosenblum, M. & Kurths, J. Synchronization: a

universal concept in nonlinear sciences. (Cambridge university press, 2003).

### 54. Strogatz, S. Sync: The emerging science of spontaneous order. (Penguin UK,

2004).

### 55. Winfree, A. T. Biological rhythms and the behavior of populations of coupled

oscillators. J. Theor. Biol. 16, 15–42 (1967).

### 56. Haken, H. Information and Self-Organization - A Macroscopic approach to

Complex Systems. (Springer, 1988).

### 57. Mirollo, R. E. & Strogatz, S. H. Synchronization of pulse-coupled biological

oscillators. SIAM J. Appl. Math. 50, 1645–1662 (1990).

### 58. Strogatz, S. H. & Stewart, I. Coupled oscillators and biological

synchronization. Sci. Am. 269, 102–109 (1993).

### 59. Daffertshofer, A., Ton, R., Kringelbach, M. L., Woolrich, M. & Deco, G. Distinct criticality of phase and amplitude dynamics in the resting brain. NeuroImage 180, 442–447 (2018).

### 60. Siems, M. & Siegel, M. Dissociated neuronal phase-and amplitude-coupling

patterns in the human brain. NeuroImage 209, 116538 (2020).

### 61. Deco, G. et al. Single or multiple frequency generators in on-going brain

activity: a mechanistic whole-brain model of empirical MEG data. NeuroImage 152, 538–550 (2017).

### 62. Yeung, M. K. S. & Strogatz, S. H. Time Delay in the Kuramoto Model of

Coupled Oscillators. Phys. Rev. Lett. 82, 648–651 (1999).

### 63. Earl, M. G. & Strogatz, S. H. Synchronization in oscillator networks with

delayed coupling: a stability criterion. Phys. Rev. E 67, 036204 (2003).

### 64. Wildie, M. & Shanahan, M. Metastability and chimera states in modular delay

and pulse-coupled oscillator networks. Chaos 22, 043131 (2012).

### 65. Bick, C., Goodfellow, M., Laing, C. R. & Martens, E. A. Understanding the

dynamics of biological and neural oscillator networks through exact mean-
ﬁeld reductions: a review. J. Math. Neurosci. 10, 1–43 (2020).

### 66. Izhikevich, E. M. & Edelman, G. M. Large-scale model of mammalian

thalamocortical systems. Proc. Natl Acad. Sci. USA 105, 3593–3598 (2008).

### 67. Tononi, G., Sporns, O. & Edelman, G. M. A measure for brain complexity:

relating functional segregation and integration in the nervous system. Proc. Natl Acad. Sci. 91, 5033–5037 (1994).

### 68. Tognoli, E. & Kelso, J. A. The metastable brain. Neuron 81, 35–48 (2014).

### 69. Cabral, J., Kringelbach, M. L. & Deco, G. Functional graph alterations in

schizophrenia: a result from a global anatomic decoupling. Pharmacopsychiatry 45(Suppl 1), S57–S64 (2012).

### 70. Cabral, J., Hugues, E., Kringelbach, M. L. & Deco, G. Modeling the outcome of

structural disconnection on resting-state functional connectivity. NeuroImage
62, 1342–1353 (2012).

### 71. Schartner, M. M., Carhart-Harris, R. L., Barrett, A. B., Seth, A. K. &

Muthukumaraswamy, S. D. Increased spontaneous MEG signal diversity for
psychoactive doses of ketamine, LSD and psilocybin. Sci. Rep. 7, 46421 (2017).

### 72. Carhart-Harris, R. L. et al. The entropic brain: a theory of conscious states

informed by neuroimaging research with psychedelic drugs. Front. Hum. Neurosci. 8, 20 (2014).

### 73. Goriely, A., Kuhl, E. & Bick, C. Neuronal oscillations on evolving networks:

dynamics, damage, degradation, decline, dementia, and death. Phys. Rev. Lett.
125, 128102 (2020).

### 74. Bick, C. Heteroclinic switching between chimeras. Phys. Rev. E 97, 050201

(2018).

### 75. Ansmann, G., Lehnertz, K. & Feudel, U. Self-induced switchings between

multiple space-time patterns on complex networks of excitable units. Phys. Rev. X 6, 011030 (2016).

### 76. Rabinovich, M. I., Simmons, A. N. & Varona, P. Dynamical bridge between

brain and mind. Trends Cogn. Sci. 19, 453–461 (2015).

### 77. Roberts, J. A. et al. Metastable brain waves. Nat. Commun. 10, 1056 (2019).

### 78. Atay, F. M. Distributed delays facilitate amplitude death of coupled oscillators. Phys. Rev. Lett. 91, 094101 (2003).

### 79. Ritter, P., Moosmann, M. & Villringer, A. Rolandic alpha and beta EEG

rhythms’ strengths are inversely related to fMRI‐BOLD signal in primary
somatosensory and motor cortex. Hum. Brain Mapp. 30, 1168–1187 (2009).

### 80. Van Essen, D. C. et al. The WU-Minn Human Connectome Project: an

overview. NeuroImage 80, 62–79 (2013).

### 81. Horn, A. et al. Lead-DBS v2: Towards a comprehensive pipeline for deep brain

stimulation imaging. NeuroImage 184, 293–316 (2019). ARTICLE
COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y

COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys

### 82. Ashburner, J. A fast diffeomorphic image registration algorithm. NeuroImage

38, 95–113 (2007).

### 83. Tzourio-Mazoyer, N. et al. Automated anatomical labeling of activations in

SPM using a macroscopic anatomical parcellation of the MNI MRI single-
subject brain. NeuroImage 15, 273–289 (2002).

### 84. Andronov, A. A., Vitt, A. A. & Khakin, S. E. Theory of oscillators. (Dover

Mathematics,1987).

### 85. Aranson, I. S. & Kramer, L. The world of the complex Ginzburg-Landau

equation. Rev. Mod. Phys. 74, 99–143 (2002).

### 86. Olinger, D. J. A low‐dimensional model for chaos in open ﬂuid ﬂows. Phys. Fluids A: Fluid Dyn. 5, 1947–1951 (1993).

### 87. Shanahan, M. Metastable chimera states in community-structured oscillator

networks. Chaos 20, 013108 (2010).

### 88. Sethia, G. C., Sen, A. & Atay, F. M. Clustered chimera states in delay-coupled

oscillator systems. Phys. Rev. Lett. 100, 144102 (2008). Acknowledgements
J. C. is funded by the Portuguese Foundation for Science and Technology grants UIDB/
50026/2020, UIDP/50026/2020 and CEECIND/03325/2017, Portugal. F. C. is funded by the
EU-project euSNN European School of Network Neuroscience (MSCA-ITN-ETN H2020-
860563). The Wellcome Centre for Human Neuroimaging is supported by core funding
from Wellcome [203147/Z/16/Z]. J. V. is supported by the EU H2020 FET Proactive project
Neurotwin grant agreement no. 101017716. R. L. acknowledges support from EPRSC Grants
No. EP/V013068/1 and EP/V03474X/1. C. B. acknowledges support from the Engineering
and Physical Sciences Research Council (EPSRC) through the grant EP/T013613/1. MLK is
supported by the Center for Music in the Brain, funded by the Danish National Research
Foundation (DNRF117), and the Centre for Eudaimonia and Human Flourishing, funded
by the Pettit Foundation and Carlsberg Foundation. G. D. is supported by the Spanish
national research project (PID2019-105772GB-I00 MCIU AEI), funded by the Spanish
Ministry of Science, Innovation and Universities (MCIU), State Research Agency (AEI); HBP SGA3 Human Brain Project Speciﬁc grant agreement 3 (945539), funded by the EU
H2020 FET Flagship program; SGR Research Support Group (reference 2017 SGR 1545),
funded by the Catalan Agency for Management of University and Research Grants
(AGAUR); Neurotwin Digital twins for model-driven non-invasive electrical brain stimu-
lation (grant agreement 101017716), funded by the EU H2020 FET Proactive program;
euSNN (grant agreement 860563), funded by the EU H2020 MSCA-ITN Innovative
Training Networks; The Emerging Human Brain Cluster (CECH) (001-P-001682) within
the framework of the European Research Development Fund Operational Program of
Catalonia 2014–2020; Brain-Connects: Brain Connectivity during Stroke Recovery and
Rehabilitation (201725.33), funded by the Fundacio La Marato TV3; and Corticity, FLAG-
ERA JTC 2017 (reference PCI2018-092891), funded by the MCIU, AEI. Author contributions
J. C., G. D., and M. L. K. conceived and designed the analysis. J. C., F. C., J. V., G. D.
contributed with data and analysis tools. J. C. and F. C. performed the simulations and
analysis. V. L., K. F., R. L., C. B., M. L. K., and G. D. supervised the analysis. J. C. wrote the
original draft. F. C. wrote the Supplementary Information. All authors reviewed and
edited the ﬁnal paper and Supplementary Information. Competing interests
The authors declare no competing interests. Additional information
Supplementary information The online version contains supplementary material
available at https://doi.org/10.1038/s42005-022-00950-y. Correspondence and requests for materials should be addressed to Joana Cabral. Peer review information Communications Physics thanks Fatihcan Atay and the other,
anonymous, reviewer(s) for their contribution to the peer review of this work. Peer
reviewer reports are available. Reprints and permission information is available at http://www.nature.com/reprints
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in
published maps and institutional afﬁliations. Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative
Commons license, and indicate if changes were made. The images or other third party
material in this article are included in the article’s Creative Commons license, unless
indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons license and your intended use is not permitted by statutory
regulation or exceeds the permitted use, you will need to obtain permission directly from
the copyright holder. To view a copy of this license, visit http://creativecommons.org/
licenses/by/4.0/.
© The Author(s) 2022
COMMUNICATIONS PHYSICS | https://doi.org/10.1038/s42005-022-00950-y
ARTICLE
COMMUNICATIONS PHYSICS | (2022) 5:184 | https://doi.org/10.1038/s42005-022-00950-y | www.nature.com/commsphys
