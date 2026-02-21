# wang-2023-thalamocortical-demodulators

PERSPECTIVE
Thalamocortical loops as temporal demodulators
across senses
Ehud Ahissar 1 ✉, Guy Nelinger 1, Eldad Assa 1, Ofer Karp 1 &
Inbar Saraf-Sinik 1
Sensory information is coded in space and in time. The organization of neuronal activity in
space maintains straightforward relationships with the spatial organization of the perceived
environment. In contrast, the temporal organization of neuronal activity is not trivially related
to external features due to sensor motion. Still, the temporal organization shares similar
principles across sensory modalities. Likewise, thalamocortical circuits exhibit common
features across senses. Focusing on touch, vision, and audition, we review their shared coding
principles and suggest that thalamocortical systems include circuits that allow analogous
recoding mechanisms in all three senses. These thalamocortical circuits constitute
oscillations-based phase-locked loops, that translate temporally-coded sensory information
to rate-coded cortical signals, signals that can integrate information across sensory and
motor modalities. The loop also allows predictive locking to the onset of future modulations
of the sensory signal. The paper thus suggests a theoretical framework in which a common
thalamocortical mechanism implements temporal demodulation across senses.
B
rains are made of loops. Arguably, no open-loop (i.e., open ended, or feedforward only)
pathway can be found in the brain (sensory organs included). Among these loops, tha-
lamocortical (TC) loops have received speci ﬁc attention. Their anatomical pattern seems to
be similar across modalities 1, and implies a tight linkage between the activity of thalamic and
cortical neurons that process the same sensory or motor information 2–13. Do these anatomical
similarities imply a similar function? And what kind of function can be implemented by such
tight thalamocortical anatomical linkage?
Over the years, TC loops have been proposed to implement various functions, from tuned
oscillators14 to attentional ﬁlters15,16. Of the various proposed functions, three have gained
signiﬁcant empirical support. The ﬁrst is that thalamic neurons function as switchable, or
tunable, relay stations. Namely, they relay (i.e., amplify, clean, and replicate their input without
changing its content or coding scheme) afferent information, with the cortical feedback tuning
their relay operation, or even switching it entirely on or off 17. The second proposal also asserts
that the thalamo-cortical feedforward connections relay afferent information. The cortico-
thalamic feedback, however, includes connections that are part of downstream processing,
relaying cortical outputs to other cortical circuits via thalamic pathways 16,18. The third proposal
is that TC loops function as neuronal phase-locked loops (NPLLs), which recode temporally
encoded afferent signals in population ﬁring rates 19,20.
The latter proposal is especially relevant in perception, where the scanning motion of the
sensor interacting with the external world generates the sensory information brains can
process21. Converting the spatial characteristics of objects into temporal structures of the activity
of receptors (i.e., temporal encoding) gives temporal processing a major role in natural
perception22. We thus review how NPLLs can implement recoding of temporally encoded
sensory information in three modalities: touch, vision and audition. The article describes the
https://doi.org/10.1038/s42003-023-04881-4 OPEN
1 Department of Brain Sciences, Weizmann Institute, Rehovot 76100, Israel. ✉email: ehud.ahissar@weizmann.ac.il
COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio 1
1234567890():,;
nature of sensory temporal encoding in these three modalities,
and the principles proposed for central recoding in each of them.
Importantly, while the principles of time-to-rate recoding are
proposed to be similar across the three sensory modalities, the
parametric regimes are expected to be modality-speci ﬁc. The
article thus presents the possibility that mammalian thalamo-
cortical systems translate temporal-coding to rate-coding via
modality-speciﬁc neuronal phase-locked loops. It reviews the
empirical support for this possibility, describes its theoretical
advantages and outlines relevant empirical predictions. As the
empirical evidence supporting the operation of the NPLL model
across senses is partial, and not balanced across senses, the cur-
rent paper should be taken as a proposal of a theoretical frame-
work that calls for direct testing rather than as a summary of well-
supported ideas.
Temporal encoding
Temporal encoding induced by sensor motion . The scanning
motion by the sensory organ transforms the spatial structure of
external features into the temporal domain. The scanning direc-
tion dictates the activation order of individual and neighboring
receptors. During the continuous scanning motion, a straight-
forward formula (1) describes this spatio-temporal transforma-
tion, mapping spatial distances ( dx) into temporal delays ( dt,
between sequential neuronal activations), depending on the
scanning velocity of the sensory organ ( v)
19,20,23:
dt ¼ dx
v : ð1Þ
With this transformation, spatially closer features induce
shorter activation delays. Importantly, since the values of these
temporal delays depend on the scanning velocity, which is under
the active control of the animal, temporal encoding, such as in
mammalian touch and vision, allows hyperacuity. Slowing down
the scanning motion effectively magni ﬁes the ﬁner spatial details
of the external object. Thus, ﬁne resolution is no longer limited by
the granularity of the sensory receptors (e.g., photoreceptors at
the retina or mechanoreceptors at the ﬁngertip22). Instead, a
satisfactory resolution is dictated by the accuracy of motor
control and its compatibility with the temporal sensitivity of the
sensory receptors and their downstream processing 24–26.O f
course, since the sensory-motor compatibility also dictates the
range of sensory signals the system can acquire, the speci ﬁc
temporal delays, scanning velocities and resulting spatial resolu-
tions are likely to differ between modalities, and also between
species for the same modality.
Active control of the scanning velocity, in a way that is
adaptive to the resolution requirements (that dynamically change
during behavior) and to the speci ﬁc features of the object in focus,
can be achieved via motor-sensory-motor (MSM) closed loops 27.
MSM loops actively modulate key parameters of the scanning
motion in a dynamically adaptive way that allows, for example,
decreasing the scanning velocity when encountering a ﬁne-
textured object or when a higher resolution is behaviorally
meaningful. In addition, MSM loops introduce the information
about sensor motion inherently into the spatio-temporal
computation, allowing the distinction between self-motion and
external movements.
Temporal encoding induced by stimulus dynamics . Whereas
the mammalian tactile and visual receptor-arrays sense transient
changes in both the spatial and temporal structure of external
energies, auditory receptor-arrays sense transients only in the
temporal structure of external energies. Accordingly, while in
touch and vision temporal predictions (e.g., predictions of
activation onset times) can refer to the interactions between
sensor motion and external spatial details, in audition they refer
exclusively to the temporal structure of the auditory stimulus
itself
27,28.
In speech, a prominent temporal patterning of the signal is
carried by the temporal envelope – the signal describing the
changes in the amplitude of sound over time - that re ﬂects its
syllabic structure and typically occurs at frequencies below
8H z29. Parsing the speech signal according to its temporal
envelope is considered a necessary step in auditory processing 30.
The ef ﬁciency of such parsing, which affects processing resolu-
tion, is limited in two aspects. First, the processing bandwidth of
the human auditory system limits the comprehensible syllabic
frequency30–32, and second, the accuracy of phase-locking in the
auditory system likely limits its ability to decipher syllabic onsets,
hence limiting sentence-by-sentence intelligibility 28,31,33,34.
Central recoding
Why should temporally encoded signals require recoding? There
are two major possible reasons. One, such recoding may allow
integration with neuronal information that is coded differently.
Second, recoding may be required to allow the integration of the
temporally encoded information in the dynamics of MSM loops.
We hypothesize that the common coding scheme, which allows
integration across sensory and motor modalities, is rate
coding20,35.
An efﬁcient, arguably the most ef ﬁcient36, circuit for temporal-
to-rate transformation is the neuronal phase-locked loop
(NPLL)20,37,38. The NPLL uses a local rate-controlled oscillator
(RCO) that serves as an adaptive predictor for the temporal
structure of the loop ’ s incoming signals. Any deviation of the
incoming spike times from the RCO ’ s predicted times is infor-
mative, and is recoded as a rate-coded signal (Fig. 1). Temporal
modulations in the NPLL ’ s input signal are thus instantaneously
converted to rate modulations in its output signal; neither the
input nor the output are required to be periodic for that to
happen.
The NPLL has two arcs (Fig. 1a), each performing an opposite
transformation: the bottom-up arc (red), transforms temporal
delays into rate code ( Δt → R), and the top-down arc (blue),
transforms population rates to temporal delays ( R → Δt). To
intuitively explain how the NPLL functions, we follow the
information ﬂow step-by-step. The temporally encoded signal
comes in the bottom-up direction, conveying information from
the sensory receptors. The NPLL compares the incoming ﬁring
times ( t
in) with the ﬁring times of its cortical oscillator ( tosc).
Acting collectively as an AND gate, the population of thalamo-
cortical neurons ﬁre only when the bottom-up and top-down
signals overlap. This AND gating generates a population rate that
is inversely proportional to the delay between the bottom-up and
top-down signals, with high ﬁring rates corresponding to smaller
delays. Next, this integrated rate-coded signal drives a population
of inhibitory neurons that closes the loop projecting onto the
cortical oscillator. Functionally, the negative feedback leads the
convergence of the loop: since the population rate is a decreasing
function of the temporal delay, whereas the latter is an increasing
function of the former (Fig. 1b), the loop will converge towards a
single stable ﬁxed point de ﬁned as a pair of values ( RSS and ΔtSS;
intersection in Fig. 1b). Importantly, this ﬁxed point is deter-
mined anew for every new input spike, thus forcing the cortical
oscillator to track the timing of the input. The cycle-by-cycle
convergence dynamics is determined by the transformation
parameters in both arcs. The combined gain of the two arcs, β
(Fig. 1), de ﬁned as the “open-loop gain ”, expresses how fast the
loop locks onto the input signal. The larger the magnitude of β,
PERSPECTIVE COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4
2 COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio
the faster the convergence and the lower the stability of the
loop20,39.
It should be emphasized that the oscillator (RCO) of the NPLL
may be implemented in many ways, not necessarily in the form of
single-cell sustained oscillators. Any form of local oscillations,
whose frequencies are tunable locally within the range that is
relevant to the expected sensory frequencies, and that are effec-
tively expressed during active perception, will satisfy the
requirements of NPLL.
Touch. Tactile information is collected by skin mechanoreceptors
and, in rodents, also by vibrissal (whiskers ’ ) mechanoreceptors.
The sensation in primates and rodents is primarily active,
achieved by scanning objects of interest with the relevant sensory
organs in a manner that adapts to the tactile features of the
object24,40–46. Consequently, ﬁne spatial details representing
shapes and textures are likely encoded temporally by the
mechanoreceptors populating the moving sensor 20,22,24,25,44,47.
NPLLs would make excellent re-coders of this information,
recoding the information in population ﬁring rates. Is there evi-
dence for NPLLs operating in tactile systems?
In primates, it was found that local cortical oscillators in the
second somatosensory cortex (S2) lose their periodicity when the
monkey touches objects 19. This observation is consistent with
these oscillators functioning as part of an NPLL circuit, because
the NPLLs ’ oscillators are forced to track the instantaneous
periodicity of the input. The periodicity of the input is
determined by the interactions between hand motion and the
object’ s spatial frequencies (see Eq. 1). Periodic tactile inputs thus
can be generated only when the instantaneous hand speed is
inversely correlated with the local spatial frequency of the object ’ s
surface texture, a correlation that typically does not occur. These
observations are consistent with an NPLL scheme, but cannot
discriminate between NPLL and other possible processing
schemes. For such a discrimination, a more systematic testing is
required.
Such a systematic study, aimed at testing NPLL predictions,
was conducted in rodents. The major predictions tested were (i)
that somatosensory cortical oscillators can track the frequency of
periodic tactile stimulations and (ii) that the phase difference
between the tactile input and cortical oscillations increases with
the frequency 20. The latter prediction distinguishes NPLLs from
coupled oscillators 37. Both predictions were con ﬁrmed in
rodents22,39,48–50. Importantly, for frequencies within the range
of active whisking (~5 –11 Hz), the latency prediction (prediction
ii) was conﬁrmed only for neurons belonging to the paralemniscal
pathway (in the medial division of the posterior nucleus of the
thalamus, POm, and in layers 5 A and 2/3 of the primary
somatosensory cortex, S1).
These results suggest that at least some paralemniscal
thalamocortical loops, between POm and layer 5/6 of S1, function
as NPLLs51. For these circuits, the accumulating evidence suggest
that (i) TC circuits could switch between relay and NPLL modes,
by switching the thalamic neurons between relay and gate modes,
respectively, under cortical control (Fig. 2); (ii) if NPLLs are
indeed part of TC loops, they may function in a regime of large
open-loop gains (| β| > 2; Fig. 3), entailing unstable but fast-
reacting loops; 20,37 (iii) the TC loops that can function as NPLLs
are composed of speci ﬁc ensembles of POm and S1 neurons; 52,53
and (iv) TC loops connecting POm with S2 can also function as
NPLLs54,55.
NPLLs convert spike-time information to rate-coded signals. If
NPLLs are implemented in thalamocortical loops, then thalamic
and cortical neurons operating within the NPLL loop are
expected to code sensory information in both time and rate
(Figs. 1 and 2), whereas the ﬁring of downstream cortical neurons
is expected to be dominated by rate-coding. This is indeed the
case with primates performing tactile frequency discrimination
tasks56 – the temporal information of the two stimuli is preserved
well in thalamic and S1 neurons and fades away in downstream
stations. In parallel, downstream stations are able to perform
computations that are based on these rate-coded signals.
Furthermore, consistent with the population rate-code used in
feasible implementations of thalamocortical NPLLs 20 (Fig. 1), it
was found that population rate-coded signals are more reliable
than single-cell rate-coded signals in processing and comparing
the frequencies of the sensory signals 56. The observed population
rate code obeys the prediction of the NPLL, as it is based on a
monotonously changing rate as a function of the sensory
frequency
56 (Figs. 1 and 3).
Vision. Visual information is collected by photoreceptors popu-
lating the retina of constantly moving eyes 57–59. As with active
touch, active vision induces temporal coding, by which spatial
Fig. 1 Spike-time to population-rate transformation by TC NPLL. a Schematic description. Temporal variables are in blue and rate variables in red. t, time;
R, rate; n, cycle number; X, comparator; ~, rate-controlled oscillator (RCO); T c, the intrinsic period of the RCO; R max, maximal value of R; I, pool of inhibitory
units. b Phase-plane description. The two transfer functions describe the reciprocal relationships between the temporal ( Δ t) and rate (R) variables, leading
to a ﬁxed point at their intersection. This ﬁxed point ([Δ tss, Rss]) is the steady-state the loop tries to converge to. The equations describe a linear NPLL; the
behavior of non-linear NPLLs can be assessed near the ﬁxed point using linear approximations (see refs. 19,20,23).
COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4 PERSPECTIVE
COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio 3
POm
L5a
Brainstem
whiskers
L5/6
INH
x
(mainly Sp5I)
Steady-state
Cortical 
feedback 
(iGluR)
1st cycle
Relay
Relay
mGluR
AND-Gate
x
a b
POm 
output
Brainstem 
input
s1 s2 s3 s4
(i)
(ii)
(iii)
(iv)
1
Temporal 
code
Rate 
code
Output
Gating
Input
Whisker 
position
Fig. 2 Implementation of a tactile NPLL in a vibrissal, paralemniscal, TC loop. a The basic phase-locked loop. POm neurons, exhibiting two functional
modes ( Δ , relay mode; x, AND-gate mode), drive cortical inhibitory neurons (INH), which in turn inhibit cortical oscillatory neurons (~) that drive the
cortical feedback. , inhibitory connections; ⇾, excitatory connections. b A timing diagram describing the transition of POm neurons from relay ( Δ )t o
AND-gate (x) mode, and the effect of the stimulus pulse-width. Short black vertical lines represent spikes. Green vertical lines represent stimulus -pulse
onsets. Traces: (i) whisker de ﬂection, up denotes protraction. (ii) brainstem response. (iii) AND-gate operation at the POm: bold rectangles represent the
delayed cortical feedback; only those brainstem spikes overlapping with the cortical feedback would “pass the gate ”. Spikes are plotted with a short delay
after the brainstem spikes. (iv) the output of the POm. Following a quiescent period, POm neurons are hyperpolarized and thus shift into a relay mode. T he
response to the ﬁrst stimulus cycle (cycle 1) is relayed to the cortex (activity not shown in the diagram). The cortical feedback activates metabotropic
(mGluR) and ionotropic (iGluR) receptors at the thalamus. The slow mGluR activation depolarizes the thalamic neurons and shifts them into an AND-gat e
mode, in which brainstem activity will “pass the POm gate ” only when additional cortical feedback (via iGluR) is active. When the stimulus pulse-width is
shortened (cycles s3 and s4), the latency of the cortical feedback has to decrease in order to keep the output spike-count constant (in order to maintai n the
RCO frequency matching the input frequency, which remained unchanged). Adapted from 134.
Fig. 3 Working regime of paralemniscal NPLLs. a Example of L5A responses to constant frequency (CF) air-puff stimulations of the whiskers (blue, raster;
green, air-puff onset time; black, air pressure temporal pro ﬁle). Adapted from ref. 48. b Schematic description of a frequency modulated (FM) stimulation
and the corresponding response of a cortical cell. c L5A responses to CF (2 s) followed by FM (5.8 s) stimulation. Response latency (blue) and spike rate
(red) are plotted with the instantaneous frequency (1/inter-stim-interval; black). Errorbars denote SEM. d A graph describing the relationships between
latency and the input frequency at steady-state, from which the open-loop gain, β, can be computed if the circuit functions as an NPLL 19,20,23 (see
equations in Fig. 1). e Simulation of NPLL with the open-loop gain extracted from the experiment depicted in c ( β = −5.4). f The trends of the steady-
state dependencies of latency and spike count on the input frequency as predicted in NPLLs.
PERSPECTIVE COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4
4 COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio
offsets are encoded by temporal delays 22. Importantly, reliable
coding of ﬁne spatial details occurs only with temporal coding.
This is because (i) retinal temporal coding is signi ﬁcantly more
precise than retinal rate coding 60,61, and (ii) the continuous
motion of the eyes signi ﬁcantly contaminates rate coding, for
which integration over a certain time-window is required. Given
that the spatial scanning amplitude during a typical ﬁxational
pause (the period between two successive saccades) is 2 –3 orders
of magnitude larger than the ﬁnest perceivable spatial
offset22,58,62, temporal coding appears more compatible with the
observed perceptual acuity than spatial coding.
When the eyes are stationary, cortical simple-cells typically ﬁre
strongest in response to bars that are oriented in parallel to their
elongated axis and are moved across it 63. The temporal encoding
induced by eye movements, however, achieves its highest resolution
by encoding along, rather than across, the elongated axes of simple-
cell receptive ﬁelds62,64. This is a consequence of the anatomical
structure of these receptive ﬁelds (Fig. 4a). In this coding scheme,
the ﬁne details of shape are encoded by inter-receptor temporal
phases, texture by instantaneous intra-burst rates of individual
receptors, and motion by inter-burst temporal frequencies. The
visual system can read the encoded information in several ways.
NPLLs offer signi ﬁcant advantages also here. Speci ﬁcally, NPLLs
can lock to the retinal jitter and thereby (i) recode external motion
in population rates and (ii) set temporal windows for ef ﬁcient
processing of shape and texture by downstream circuits.
How could NPLLs be implemented in the visual system? Here
too, thalamocortical loops appear naturally tuned to function as
NPLLs (Fig. 4). All it takes is closing the loop from simple cells
(SCs) to the thalamus via cortical oscillators. Note that the
cortical oscillators can come in various forms. In principle, almost
any neuron can function as a local oscillator with certain
distributions of its ionic channels 65,66. Visual cortical oscillations
can function within NPLLs if their frequencies (i) are in the range
of the input frequencies and (ii) can be modulated by local
cortical inputs. Mammalian cortical oscillations ful ﬁll both
criteria. The spectral densities of human ﬁxational eye move-
ments (FeyeM) and neuronal oscillations in the visual cortex of
monkeys
67 exhibit a striking similarity; both emphasize alpha and
gamma modes, see 22. Oscillations at frequency ranges that match
those of FeyeM were observed in the visual cortex of cats, ferrets
and monkeys 67–72. The frequencies of visual cortical oscillations
can be controlled locally 69–71 and can be modulated by and
locked to external stimuli 71–74, as is the case in other modalities.
Besides frequency ranges, the main difference between visual and
other cortical oscillations is that single-cell visual oscillations are
usually not observed in the absence of visual stimuli. This might
indicate that the expression of cortical oscillations (e.g., translation
of sub-threshold oscillations to spike activity) requires an additional
excitatory input69,71. Such an input ( ‘ M’ in Fig. 4) can be provided
by an internal preparatory signal or an afferent stimulus-driven
signal, and shaped during development and learning 75.I n d e e d ,
evidence for preparatory enhancement of local oscillations in the
visual cortex has been accumulating over the years 76–79.
Audition. Touch and vision share a key perceptual strategy: they
scan their environments with a lateral motion of two-dimensional
thalamus
a
Oscillatory
cell
M
tD
Rout
(SC)
Input
Time
Input
Retino-cortical 
delay (tD)
Output (Rout )
b
Retino-cortical delay (tD , ms)
(Rout , Spikes / cycle)
SC
Retinal inter-burst frequency
higherlower
cortex
Concentric 
cells
Simple cell1 + 2 + 3
1
2 3
Fig. 4 Implementation of a visual NPLL by a thalamocortical loop. a A schematic description of the proposed thalamocortical closed-loop decoder. The
scheme is based on the schematic description of the feedforward connectivity suggested by Hubel and Wiesel 63; the feedback connectivity added in blue
closes the loop in a way that permits a PLL-like operation. Excitatory and inhibitory connections are represented by open triangles ( ▷ ) and solid
circles (●), respectively. Dashed line indicates possible poly-synaptic link. Input, retino-thalamic input; SC, simple cells; M, modulatory excitatory inp ut; ~,
oscillatory neurons. Inset: Implementation of the phase detection function by cortico-thalamic gating: the Output is active only when both the Inpu t and the
“gate” are active. b Schematic phase plane of the two basic transfer functions of the loop. SC ’s transfer function (red): Output spike-count ( Rout) decreases
as the retinocortical delay ( tD) increases. Oscillatory cells transfer function (blue): tD increases as Rout increases (note reversal of axes here). The crossing
point of the transfer functions is the set point for a speci ﬁc retinal temporal frequency. The gray arrows on top relate the direction of change of the inter-
burst frequency of the retinal input to those of the phase-plane variables: directly related to tD and inversely related to Rout. Adapted from ref. 62.
COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4 PERSPECTIVE
COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio 5
arrays of receptors. Since receptors are mostly sensitive to
changes (within their dynamic ranges), sensor motion is what
allows the perception of stationary objects, encoding space by
time22,80. The transduction of auditory signals (i.e., pressure
waves) to neural signals is performed in the cochlea where the
basic organization of receptors is different than the one observed
in touch and vision. Instead of the two-dimensional array of
dynamically-similar receptors which support two-dimensional
representation of space, audition is based on a uni-dimensional
array of dynamically different receptors supporting a uni-
dimensional representation of an auditory frequency spectrum.
As a result, auditory sensory activation is less dependent on
self-motion, a fact that probably puts audition in a motor-sensory
regime that is distinct from those of touch and vision. Thus, if
hearing involves sensor motion, it is not to directly serve
the encoding of spatial offsets. Instead, active hearing may involve
the encoding of spectral offsets (along the basilar membrane) by
time and the tuning of the basilar membrane to match acoustic
expectations by controlling the tension of the outer haircells 81,82.
Such implementations of active sensing are of course different
from the visual and tactile implementations. In vision and touch,
efference control of the sensory organ is manifested as overt
sensor motion. In audition, instead, efference control results in
covert tiny movements of the outer haircells, which affect the way
ongoing auditory signals are perceived.
Temporal modulations are therefore inherent components of
acoustic signals, with or without active cochlear mechanisms. One
such modulation, as mentioned above, is the temporal envelope
of speech, which de ﬁnes the slow variations of the spectral energy
of a spoken sentence, variations that are usually below 8 Hz 29.
This low-frequency information is crucial for identifying
phonemes, syllables, words, and sentences 83. Indeed, speech
comprehension depends on the integrity of its temporal
envelope84,85. The mechanisms by which this information is
extracted and processed are still unknown. We previously
suggested that circuits that can facilitate the processing of the
temporal envelope, and the locking of downstream processing of
the spectral information to its phasic changes (indicating syllable
onsets), are thalamocortical NPLLs 28,31.
How would such NPLLs work? In principle, many neuronal
circuits could implement the PLL algorithm, including sub-
cortical and cortico-cortical loops. Based on the ﬁndings in the
tactile and visual systems, we speculate that auditory NPLLs are
implemented in thalamocortical loops, and that a temporal
comparison takes place in the thalamus, most likely in the non-
lemniscal nuclei. As in the vibrissal tactile system, the auditory
non-lemniscal thalamus exhibits larger temporal dispersion 86,87
and spectral integration 87–89 than the lemniscal thalamus. Both
features, together with a typical thalamic gating mechanism 90,91
and a strong cortico-thalamic feedback 92, make the non-
lemniscal thalamus optimal for temporal comparison
functions20,22,52. According to this hypothesis, the non-
lemniscal thalamus produces a difference signal that is fed back
to the cortex, where it is used to update the frequency of the
intrinsic oscillators. If the entire loop is connected as a negative
feedback loop, via thalamic 93 or cortical inhibition, the negative
feedback would force the cortical oscillations to phase-lock to the
envelope of the speech signal (Fig. 5).
The spectral analysis of syllables must be coordinated with
syllable timing 94. Our hypothesis suggests that the local
oscillators of the NPLLs, which track the syllabic rate and thus
predict the onset timing of the next syllable, trigger the spectral
processing of each syllable. This predictive signaling by an
adaptive internal clock can prevent losing the important spectral
information contained close to the syllable onset. The existence of
such intrinsic clock is also consistent with a phenomenon often
related to in speech perception: that of perceptual center (P-
center95,96). The P-center of a signal, such as a syllable,
corresponds to its “psychological moment of occurrence ”95.
Thus, the experimental de ﬁnition of a P-center of a speech signal
depends on a comparison, by a listener, between such
psychological moments of occurrence and an internal temporal
time
compare
freq
time (ms)0 1400
freq (kHz)0
10
update
Local oscillations
INH
difference
Syllable processing
Lemniscal
thalamus
cortex
prediction
Fig. 5 Possible roles of auditory TC NPLLs in the processing of the temporal envelope and in syllable processing. We postulate that the temporal
envelope of the speech signal is processed in parallel to pre-processing of its spectral content, probably by the non-lemniscal and lemniscal system s,
respectively. In this scheme, the temporal envelope is compared against a cortical reference (temporal expectation) implemented by local neuronal
oscillations. The comparison occurs in the (non-lemniscal) thalamus, and its output (which is proportional to the temporal difference between the t wo
signals) is fed-back to the cortex, where it eventually updates the reference signal (likely via inhibitory neurons, INH). The signal that represent s the
temporal difference, which contains information about input speech rate, might be further processed (red arrow, top left). Cortical oscillations, which
express an expectation for the onset timing of the next syllable, send this timing information to a postulated “syllable processor, ” which processes the
spectral information contained in a syllable. This expectation is updated from syllable to syllable until stabilized on the speaker ’s rhythm27,28. Spectograms
are of the sentence ‘black dogs cannot bark ’31.
PERSPECTIVE COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4
6 COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio
ruler, or a pacemaker 95,97. NPLLs exhibit such a process:
comparing the rate of an input stream of syllables against an
internal temporal ruler in the form of intrinsic oscillations.
Thus, the suggestion here is that speech processing includes
at least two streams that eventually converge: those of the
temporal envelope and the spectral content (Fig. 5). Supporting
evidence for such a separation, in addition to the anatomy of
afferent auditory pathways described above, can be found in the
response selectivities of neuronal populations in the primary
auditory cortex 98 and in the anatomy of cortico-thalamic
connections99–101. Supporting evidence for the oscillations-
based processing of the temporal envelope comes from a series
of studies that demonstrate the dependency of speech compre-
hension on frequency and phase matching between the temporal
envelope and cortical oscillations 28,30–32,102,103, as well as from
theoretical work 104.
Comparison across the senses . Our senses collect complementary
information about our environment and, thus, many of their
aspects are necessarily different. Still, common principles can be
found. Both touch and vision employ two-dimensional sheets of
receptors (under the skin, around the whisker follicle, or on the
retina) that are activated by temporal modulations. Since most of
the sensed ﬁeld is usually stationary, these temporal modulations
primarily result from sensor motion (hand, whisker, or eye). In
contrast, auditory receptors are sensitive to the fundamental
dynamic ﬂuctuations of audible acoustic waves. Outlining the core
difference between these modalities: acoustic signals always activate
the inner-ear haircells, whereas physical objects activate mechano-
or photo-receptors primarily upon sensor motion.
Indeed, touch and vision have more in common when
interpreting the activation of their respective receptors and when
analyzing the operation of their motor-sensory loops. Yet, they
also share an important aspect with the auditory sense – in all
senses, the frequencies dominating sensory acquisition are in the
theta-alpha range, frequencies below 20 Hz. In vision this is the
dominant frequency range of ocular drifts during individual
ﬁxational pauses. In active touch this frequency range char-
acterizes palpation-induced modulations of mechanoreceptors. In
vibrissal active touch it characterizes whisking-induced afferent
modulations. In audition it characterizes the syllable-induced
modulations of speech signals.
Olfaction and taste are probably as active as touch and
vision105–108. Hence, their afferent activity is expected to be
strongly modulated at the frequencies of sensor motion,
frequencies that are similar to (and often synchronized with)
those of other facial senses 105,109.
Thus, it seems that all senses can bene ﬁt from a mechanism
that locks to the temporal envelope and decodes the information
it carries. First, time locking to the low-frequency envelope signal
allows a proper decoding of the information that is carried by the
envelope itself – speech rate, whisking frequency, or hand/eye
scanning speed; the latter are crucial for the control of self-
motion. Second, it allows a proper decoding of the information
carried by the high-frequency signals modulated by the envelope
– syllabic spectral information in speech and texture or shape
spatial information in touch and vision. The processing of the
high-frequency signals can also bene ﬁt from thalamocortical
NPLLs that are tuned to the appropriate frequencies 20,62.
“Higher-order” thalamic nuclei . An interesting hypothesis sug-
gests that the thalamus is a multi-way relay station, and divides
the thalamic nuclei into ﬁrst- and higher-order nuclei. This
division is based on the relative strengths of their peripheral and
cortical drives. Nuclei in which peripheral drives are signi ﬁcantly
stronger than the cortical drives are termed ﬁrst-order nuclei;
these nuclei (VPM, LGN and MGV) are considered primarily
sensory relay stations. In contrast, the nuclei whose cortical drives
are considered signi ﬁcantly stronger than their peripheral drives
are termed higher-order nuclei, and are regarded as cortico-
cortical relay stations. According to this scheme, the thalamic
nuclei are all relay stations, but not all of them necessarily relay
information between the periphery and the cortex. Rather,
higher-order nuclei, such as the POm, MGD, or pulvinar, facil-
itate communication between various cortical stations 18,110,111.
Importantly, given the poor spatiotemporal resolution of the
neuronal responses in these higher-order nuclei, the nature of the
information that is supposed to be relayed via cortico-thalamo-
cortical pathways is likely only contextual 17,99.
An alternative hypothesis for thalamic function, the closed-
loop hypothesis, assumes that the tight connectivity between
thalamus and cortex re ﬂects the fact that thalamo-cortical circuits
form processing units. Anatomy indicates that neurons in the
granular and sub-granular layers of sensory cortices form
anatomical loops with thalamic neurons. For example, layer 4
neurons in S1 of the rat affect the activity of layer 6 neurons,
which in turn affect the activity of thalamocortical neurons in the
VPM, which then drive layer 4 neurons. Similarly, layer 5a
neurons affect layer 5b neurons, which in turn drive POm
neurons, which then drive layer 5a neurons (reviewed in
ref. 1,11,20,35). Similar closed loops (i.e., circuits in which every
signal constantly, though not exclusively, affects its source or
sources) occur in the visual and auditory systems. As neuronal
processing is often iterative, these closed loops can serve as a
means by which thalamocortical networks converge upon reliable
internal representations 54,112.
The major debate is thus about the function of the so-called
higher-order thalamic nuclei – POm, MGD, and pulvinar. Do they
function as cortico-cortical links, or do they process basic sensory
information? While this debate is still open, we would like to
mention the factors that support the latter view. (i) the so-called
higher-order nuclei belong to afferent pathways that, based on
comparative anatomy, evolved earlier than those containing the so-
called ﬁrst-order nuclei. Thus, assuming that “higher-order” nuclei
function as cortico-cortical links between cortical stations that
receive their inputs from “ﬁrst-order” nuclei raises the question –
what were their functions before the so-called ﬁrst-order pathways
evolved? (ii) In contrast, the processing suggested for the so-called
higher-order nuclei by the closed-loop hypothesis is consistent with
the assumed evolutionary order - processing basic sensory
information (sensor motion in touch and vision and temporal
envelopes of acoustic waves in audition) that was most likely
relevant to animal behavior before the newer pathways evolved. (iii)
Processing of these basic signals is essential also for integrating the
information arriving from the newer pathways: high-resolution
spatial (touch and vision) and spectral (audition) information.
Without accurate tracking of sensor motion by central circuits, the
high-resolution signals would be meaningless. (iv) The so-called
higher-order nuclei receive substantial bottom-up input from the
sensory organs, which is at odds with the function of high-order
cortico-cortical link. (v) Neuronal populations at the POm function
as AND-gates (comparators, as those required for NPLLs),
comparing the timing of cortical and sensory inputs
52,w h i c hi s
again at odds with a cortico-cortical link but consistent with
temporal-to-rate recoding.
This debate may be resolved with the aid of systematic
investigations of the so-called higher-order nuclei. For example,
systematic studies of the POm showed that the nucleus is a patchy
structure, containing multiple zones with different morphology
and different neuronal response patterns 52,53; future experiments
may test whether different zones take part in different
COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4 PERSPECTIVE
COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio 7
mechanisms. It would be interesting to examine the results of
similar studies also in the MGV, where basic systematic
thalamocortical studies are still lacking, and in the pulvinar. In
any event, the list of counter evidence listed above calls for a
reconsideration of the terms “ﬁrst-order” and “higher-order” with
regard to these thalamic nuclei.
Precise manipulation techniques, such as modern optogenetic
tools, allow cell-type selective and temporaly precise manipula-
tions of speci ﬁc cell types in speci ﬁc brain areas
113,114 and can
thus facilitate such systematic studies. Applying these methods to
speciﬁc cells in the thalamus and cortex allow (i) testing the effect
of activity perturbations on the perception of ﬁne versus coarse
object details – the former is expected to be impaired when
perturbing NPLL-related cells, (ii) induction of virtual touch that
is speciﬁc to the NPLL predictions, such as activation of so-called
Touch Neurons 25,115, neurons that are sensitive selectively to
touch and not to whisking in air, at times corresponding to the
reading of the whisker angle from the rate-coded signals in
thalamus or cortex (S1), (iii) virtual contacts can also be induced
by abrupt modi ﬁcations of the rate-coded signals – perturbations
like that are expected to be interpreted by the brain as the
existence of an external obstacle, (iv) modifying whisking
frequency by modulating the population rate-coded signals in
cortex or thalamus – such modulations are expected to modify
the reading of whisking frequency, thus inducing a correction 55,
(v) modifying the frequency of cortical RCOs by direct
optogenetic stimulations should attract the whisking frequency
in the direction of the newly-generated cortical frequency, and
(vi) inhibiting speci ﬁc synapses 116 of the NPLL circuit, such as
the inhibitory synapses impinging on POm projecting S1
neurons, should prevent adaptive control of whisking frequency
(e.g., in windy conditions 117).
Code translation . Neural circuits use a variety of neural codes,
depending on their input, output and functional connections.
Thus, sensory neurons use temporal and spatial codes that refer
to the nature of the objects or waves with which they interact. For
example, the temporal frequency of auditory afferents encodes
both the spectral frequency of the acoustic wave (up to a certain
frequency) and the syllabic rate of a speaker, depending on the
applied time windows, or ﬁltering28. In vision, depending on the
time windows, the temporal frequency encodes object ’ s texture or
motion or eye motion, and temporal phases encode object ’ s
shape62. Temporal coding in touch resembles that in vision, yet
with modality-speci ﬁc differences.
Thus, integrating sensory data from different modalities is not
trivial. Even within the same modality, neural circuits have to
integrate sensory data that are encoded differently, such as data
encoded in time (e.g., spatial details) and data encoded inﬁring rate
(e.g., signal intensity). Thus, the brain could use mechanisms for
code translation very often56,118.N P L L sa r eo n es u c hm e c h a n i s m .
They translate temporal code to population rate code. Judging from
the accumulated data, it seems that population rate coding is the
code used for cross-modal integration. Moreover, it seems to ﬁt
cortical coding of motion control119–121, and is thus a suitable code
for cross-modal integrative coding.
As mentioned above, optogenetics allows the testing of speci ﬁc
predictions of the NPLL model. As NPLLs recode the information
acquired during continuous touching, viewing or hearing, it is not
expected to be operative in the detection of brief stimuli. Rather,
it is expected to be essential for perceiving features of the sensed
objects, such as location, shape, texture, or syllabic rate. Thus,
optogenetic experiments aimed at testing perceptual detection
cannot be used for testing NPLL ’ s predictions (e.g.; 122–124,
O’ Connor et al. designed a localization task, but the mice turned
it into a detection task by whisking only in an area where every
detection of an object should lead to a “yes” response).
While experiments with optogenetic perturbation of feature
perception are still lacking, an interesting insight may be learned
from experiments with intra-cortical optogenetic feedback. Prsa
et al. used a rate-to-frequency transformation as a feedback for
activating S1 neurons by M1 activity
125. This ﬁts the frequency-
to-rate transformation predicted for S1 neurons by the NPLL
algorithm. Prsa et al. used stimulation frequencies <15 Hz, which
match the typical whisking frequencies in mice 126. Similar
frequencies were also shown to convey optogenetically-induced
rate-coded information between S1 and M1 in mice 127.
It was recently shown that perceptual phenomena can be
substituted, or ampli ﬁed, by optogenetic stimulation of cortical
neurons, in rodents and primates 128,129. Such experiments
suggest that NPLLs are not per se an exclusive operative encoding
mechanism, nor a necessary ampli ﬁcation mechanism. Instead,
NPLLs are proposed here to be speci ﬁc translators between
temporal and rate coding schemes. As such, NPLLs become
crucial computational components during active sensing, when
sensory information is temporally encoded. The oscillatory basis
of the NPLL mechanism is consistent with studies in which
oscillatory cortical stimulations induce phase-speci ﬁc perceptual
enhancements and suppressions 130–133.
Summary and conclusions
The role(s) of TC loops has been a subject of several hypotheses
over the years. TC loops were hypothesized to function as tunable
oscillators, attentional ﬁlters, switchable relay stations, cortico-
cortical shortcut pathways, or neuronal phase-locked loops
transforming temporal- to rate-codes. We argue that the
empirical data collected so far about TC loops across senses does
not leave too many options regarding their functions. The tight
feedback connections almost dictate repetitive processing between
the thalamus and the cortex. In addition, the inclusion of oscil-
lating cells in such loops strongly suggests that this processing
relates to timing. Based on the similarity between senses, the
consistency of thalamocortical phase-locked loop processing with
empirical data and evolutionary traces, and the inconsistency of
the major alternative hypothesis with evolutionary traces and
anatomy, we propose that the mammalian TC systems include
loops that translate temporal-coding to rate-coding via neuronal
phase-locked loop processing.
If this is indeed the case, then it implies that the common
coding scheme in cortical networks is rate coding, and that part of
the TC loops translate the information collected with moving
sensors into a population rate-coding scheme. An important
component of this code translation is temporal predictive pro-
cessing; this translation mechanism is based on a comparison of
the actual timings of sensory inputs against those predicted by the
relevant cortex, by virtue of its adaptive local oscillations.
Proposing a uni ﬁed mechanism to three different sensory
modalities is presumptious. Inspired by the tactile system, where
evidence is compelling, we suggest here a similar framework for
the other senses, which have similar functional requirements,
anatomical structure and physiological properties. Thus, the
current paper should be taken as proposing a common theoretical
formulation that provides testable predictions for future research.
Reporting summary . Further information on research design is available in the Nature
Portfolio Reporting Summary linked to this article.
Received: 4 April 2023; Accepted: 27 April 2023;
PERSPECTIVE COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4
8 COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio
References
1. Mease, R. A. & Gonzalez, A. J. Corticothalamic pathways from layer 5:
emerging roles in computation and pathology. Front. Neural Circuits 15,
730211 (2021).
2. Guo, Z. V. et al. Maintenance of persistent activity in a frontal thalamocortical
loop. Nature 545, 181 –186 (2017).
3. Nicolelis, M. A. & Fanselow, E. E. Thalamocortical optimization of tactile
processing according to behavioral state. Nat. Neurosci. 5, 517 –523 (2002).
4. Steriade, M. Synchronized activities of coupled oscillators in the cerebral
cortex and thalamus at different levels of vigilance [published erratum appears
in Cereb Cortex 1997 Dec;7(8):779]. Cereb. Cortex 7, 583 –604 (1997).
5. Lumer, E. D., Edelman, G. M. & Tononi, G. Neural dynamics in a model of the
thalamocortical system. I. Layers, loops and the emergence of fast
synchronous rhythms. Cereb. Cortex 7, 207 –227 (1997).
6. Ghazanfar, A. A. & Nicolelis, M. A. Nonlinear processing of tactile
information in the thalamocortical loop. J. Neurophysiol. 78, 506 –510 (1997).
7. Whittington, M. A., Traub, R. D. & Jefferys, J. G. Synchronized oscillations in
interneuron networks driven by metabotropic glutamate receptor activation
[see comments]. Nature 373, 612 –615 (1995).
8. Llinas, R. & Ribary, U. Coherent 40-Hz oscillation characterizes dream state in
humans. Proc. Natl. Acad. Sci. USA 90, 2078 –2081 (1993).
9. Bernardo, K. L. & Woolsey, T. A. Axonal trajectories between mouse
somatosensory thalamus and cortex. J. Comp. Neurol. 258, 542 –564 (1987).
10. Mukherjee, A. et al. Variation of connectivity across exemplar sensory and
associative thalamocortical loops in the mouse. Elife 9, e62554 (2020).
11. Shepherd, G. M. & Yamawaki, N. Untangling the cortico-thalamo-cortical
loop: cellular pieces of a knotty circuit puzzle. Nat. Rev. Neurosci. 22, 389–406
(2021).
12. Campo, A. T. et al. Feed-forward information and zero-lag synchronization in
the sensory thalamocortical circuit are modulated during stimulus perception.
Proc. Natl. Acad. Sci. USA 116, 7513 –7522 (2019).
13. Martinez-Garcia, R. I. et al. Two dynamically distinct circuits drive inhibition
in the sensory thalamus. Nature 583, 813 –818 (2020).
14. Steriade, M., McCormick, D. A. & Sejnowski, T. J. Thalamocortical oscillations
in the sleeping and aroused brain. Science 262, 679 –685 (1993).
15. Crick, F. Function of the thalamic reticular complex: the searchlight
hypothesis. Proc. Natl. Acad. Sci. USA 81, 4586 –4590 (1984).
16. Halassa, M. M. & Sherman, S. M. Thalamocortical circuit motifs: a general
framework. Neuron 103, 762 –770 (2019).
17. Basso, M. A., Uhlrich, D. & Bickford, M. E. Cortical function: a view from the
thalamus. Neuron 45, 485 –488 (2005).
18. Sherman, S. M. & Guillery, R. W. The role of the thalamus in the ﬂow of
information to the cortex. Philos. Trans. R. Soc. Lond. Ser. B Biol. Sci. 357,
1695–1708 (2002).
19. Ahissar, E. & Vaadia, E. Oscillatory activity of single units in a somatosensory
cortex of an awake monkey and their possible role in texture analysis. Proc.
Natl. Acad. Sci. USA 87, 8935 –8939 (1990).
20. Ahissar, E. Temporal-code to rate-code conversion by neuronal phase-locked
loops. Neural Comput. 10, 597 –650 (1998).
21. Maravall, M. & Diamond, M. E. Algorithms of whisker-mediated touch
perception. Curr. Opin. Neurobiol. 25, 176 –186 (2014).
22. Ahissar, E. & Arieli, A. Figuring space by time. Neuron 32, 185 –201 (2001).
23. Darian-Smith, I. & Oke, L. E. Peripheral neural representation of the spatial
frequency of a grating moving at different velocities across the monkey ’ s ﬁnger
pad. J. Physiol. 309, 117 –133 (1980).
24. Gamzu, E. & Ahissar, E. Importance of temporal cues for tactile spatial-
frequency discrimination. J. Neurosci. 21, 7416 –7427 (2001).
25. Knutsen, P. M. & Ahissar, E. Orthogonal coding of object location. Trends
Neurosci. 32, 101 –109 (2009).
26. Ahissar, E., Arieli, A., Fried, M. & Bonneh, Y. On the possible roles of
microsaccades and drifts in visual perception. Vis. Res. 118,2 5 –30 (2014).
27. Ahissar, E. & Assa, E. Perception as a closed-loop convergence process. eLife 5,
e12830 (2016).
28. Ahissar, E. & Ahissar, M. The Auditory Cortex: A Synthesis of Human and
Animal Research (ed. Reinhard Konig, R. Heil, P., Budinger, E. & Scheich, H.)
295-313 (Lawrence Erlbaum Associates, Inc., 2005).
29. Houtgast, T. & Steeneken, H. J. M. A review of the MFT concept in room
acoustics and its use for estimating speech intelligibility in auditoria. J. Acoust.
Soc. Am. 77, 1069 –1077 (1985).
30. Ghitza, O., Giraud, A.-L. & Poeppel, D. Neuronal oscillations and speech
perception: critical-band temporal envelopes are the essence. Front. Hum.
Neurosci. 6, 340 (2013).
31. Ahissar, E. et al. Speech comprehension is correlated with temporal response
patterns recorded from auditory cortex. Proc. Natl. Acad. Sci. USA 98,
13367–13372 (2001).
32. Luo, H. & Poeppel, D. Phase patterns of neuronal responses reliably
discriminate speech in human auditory cortex. Neuron 54, 1001 –1010
(2007).
33. Peelle, J. E., Gross, J. & Davis, M. H. Phase-locked responses to speech in
human auditory cortex are enhanced during comprehension. Cereb. Cortex
23, 1378 –1387 (2013).
34. Millman, R. E., Johnson, S. R. & Prendergast, G. The role of phase-locking to
the temporal envelope of speech in auditory perception and speech
intelligibility. J. Cogn. Neurosci. 27, 533 –545 (2015).
35. Ahissar, E. & Kleinfeld, D. Closed-loop neuronal computations: Focus on
vibrissa somatosensation in rat. Cereb. Cortex 13,5 3 –62 (2003).
36. Gardner, F.M. Phaselock Techniques (John Wiley & sons, 1979).
37. Zacksenhouse, M. & Ahissar, E. Temporal decoding by phase-locked loops:
unique features of circuit-level implementations and their signi ﬁcance for
vibrissal information processing. Neural Comput. 18, 1611 –1636 (2006).
38. Hoppensteadt, F. C. & Izhikevich, E. M. Pattern recognition via
synchronization in phase-locked loop neural networks. IEEE Trans. Neural
Netw. 11, 734 –738 (2000).
39. Ahissar, E., Haidarliu, S. & Zacksenhouse, M. Decoding temporally encoded
sensory input by cortical oscillations and thalamic phase comparators. Proc.
Natl. Acad. Sci. USA 94, 11633 –11638 (1997).
40. Lederman, S. J. & Klatzky, R. L. Hand movements: a window into haptic
object recognition. Cogn. Psychol. 19, 342 –368 (1987).
41. Sherman, D., Oram, T., Harel, D. & Ahissar, E. Attention robustly gates a
closed-loop touch re ﬂex. Curr. Biol. 27, 1836 –1843 (2017).
42. Lezkan, A. & Drewing, K. Going against the grain –Texture orientation affects
direction of exploratory movement. In International Conference on Human
Haptic Sensing and Touch Enabled Computer Applications. p. 430-440
(Springer, 2016).
43. Prescott, T. J., Ahissar, E. & Izhikevich, E. Scholarpedia of Touch (Springer,
2015).
44. Saig, A., Gordon, G., Assa, E., Arieli, A. & Ahissar, E. Motor-sensory
conﬂuence in tactile perception. J. Neurosci. 32, 14022 –14032 (2012).
45. Munz, M., Brecht, M. & Wolfe, J. Active touch during shrew prey capture.
Front. Behav. Neurosci. 4, 191 (2010).
46. Gibson, J. J. Observations on active touch. Psychol. Rev. 69, 477 –491 (1962).
47. Diamond, M. E., von Heimendahl, M., Knutsen, P. M., Kleinfeld, D. &
Ahissar, E. ‘ Where’ and ‘ what’ in the whisker sensorimotor system. Nat. Rev.
Neurosci. 9, 601 –612 (2008).
48. Ahissar, E., Sosnik, R. & Haidarliu, S. Transformation from temporal to rate
coding in a somatosensory thalamocortical pathway. Nature 406, 302 –306
(2000).
49. Ahissar, E., Sosnik, R., Bagdasarian, K. & Haidarliu, S. Temporal frequency of
whisker movement. II. Laminar organization of cortical representations. J.
Neurophysiol. 86, 354 –367 (2001).
50. Ahissar, E. & Zacksenhouse, M. Temporal and spatial coding in the rat
vibrissal system. Prog. Brain Res. 130,7 5 –88 (2001).
51. Fox, K. Introduction to the barrel cortex. Barrel cortex . p. 1-13 (Cambridge
University Press, Cambridge (2008).
52. Groh, A. et al. Convergence of cortical and sensory driver inputs on single
thalamocortical cells. Cereb. Cortex 24, 3167 –3179 (2014).
53. El-Boustani, S. et al. Anatomically and functionally distinct thalamocortical
inputs to primary and secondary mouse whisker somatosensory cortices. Nat.
Commun. 11,1 –12 (2020).
54. Yu, C. et al. Coding of object location in the vibrissal thalamocortical system.
Cereb. Cortex 25, 563 –577 (2015).
55. Ahissar, E. & Oram, T. Thalamic relay or cortico-thalamic processing? old
question, new answers. Cereb. Cortex 25, 845 –848 (2015).
56. Romo, R. & Rossi-Pool, R. Turning touch into perception. Neuron 105,1 6–33
(2020).
57. Steinman, R. M. & Levinson, J. Z. The role of eye movement in the detection
of contrast and spatial detail. In Eye Movements and Their Role in Visual and
Cognitive Processes (ed. E. Kowler) p. 115 –212 (Elsevier, 1990).
58. Rucci, M., Ahissar, E. & Burr, D. Temporal coding of visual space. Trends
Cogn. Sci. 22, 883 –895 (2018).
59. Gruber, L. Z., Ullman, S. & Ahissar, E. Oculo-retinal dynamics can explain the
perception of minimal recognizable con ﬁgurations. Proc. Natl. Acad. Sci. USA
118, e2022792118 (2021).
60. Meister, M. & Berry, M. J. 2nd The neural code of the retina. Neuron 22,
435–450 (1999).
61. Berry, M. J., Warland, D. K. & Meister, M. The structure and precision of
retinal spike trains. Proc. Natl. Acad. Sci. USA 94, 5411 –5416 (1997).
62. Ahissar, E. & Arieli, A. Seeing via miniature eye movements: a dynamic
hypothesis for vision. Front. Comput. Neurosci. 6, 89 (2012).
63. Hubel, D. H. & Wiesel, T. N. Rceptive ﬁelds, binocular interaction and
functional architecture in the cat visual cortex. J. Physiol. 160, 106–154 (1962).
64. Ahissar, E., Ozana, S. & Arieli, A. 1-D vision: encoding of eye movements by
simple receptive ﬁelds. Perception 44, 986 –994 (2015).
65. Llinas, R. R., Grace, A. A. & Yarom, Y. In vitro neurons in mammalian cortical
layer 4 exhibit intrinsic oscillatory activity in the 10- to 50-Hz frequency
range. Proc. Natl. Acad. Sci. USA 88, 897 –901 (1991).
COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4 PERSPECTIVE
COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio 9
66. Alonso, A. & Llinas, R. R. Subthreshold Na +-dependent theta-like rhythmicity
in stellate cells of entorhinal cortex layer II. Nature 342, 175 –177 (1989).
67. Eckhorn, R. Oscillatory and non-oscillatory synchronizations in the visual
cortex and their possible roles in associations of visual features. Prog. Brain
Res. 102, 405 –426 (1994).
68. Gray, C. M., Kצnig, P., Engel, A. K. & Singer, W. Oscillatory responses in cat
visual cortex exhibit inter-columnar synchronization which re ﬂects global
stimulus properties. Nature 338, 334 –337 (1989).
69. Gray, C. M. & McCormick, D. A. Chattering cells: super ﬁcial pyramidal
neurons contributing to the generation of synchronous oscillations in the
visual cortex. Science 274, 109 –113 (1996).
70. Brumberg, J. C., Nowak, L. G. & McCormick, D. A. Ionic mechanisms
underlying repetitive high-frequency burst ﬁring in supragranular cortical
neurons. J. Neurosci. 20, 4829 –4843 (2000).
71. Cardin, J. A., Palmer, L. A. & Contreras, D. Stimulus-dependent gamma (30-
50 Hz) oscillations in simple and complex fast rhythmic bursting cells in
primary visual cortex. J. Neurosci. 25, 5339 –5350 (2005).
72. Bosman, C. A., Womelsdorf, T., Desimone, R. & Fries, P. A microsaccadic
rhythm modulates gamma-band synchronization and behavior. J. Neurosci.
29, 9471 –9480 (2009).
73. Eckhorn, R., Frien, A., Bauer, R., Woelbern, T. & Kehr, H. High frequency
(60-90 Hz) oscillations in primary visual cortex of awake monkey.
NeuroReport 4, 243 –246 (1993).
74. Gray, C. M. & Viana Di Prisco, G. Stimulus-dependent neuronal oscillations
and local synchronization in striate cortex of the alert cat. J. Neurosci. 17,
3239–3253 (1997).
75. Ahissar, E., Abeles, M., Ahissar, M., Haidarliu, S. & Vaadia, E. Hebbian-like
functional plasticity in the auditory cortex of the behaving monkey.
Neuropharmacology 37, 633 –655 (1998).
76. Popov, T., Gips, B., Kastner, S. & Jensen, O. Spatial speci ﬁcity of alpha
oscillations in the human visual system. Hum. Brain Mapp. 40, 4432 –4440
(2019).
77. Händel, B. F. & Jensen, O. Spontaneous local alpha oscillations predict
motion‐induced blindness. Eur. J. Neurosci. 40, 3371 –3379 (2014).
78. Zhang, H., Morrone, M. C. & Alais, D. Behavioural oscillations in visual
orientation discrimination reveal distinct modulation rates for both sensitivity
and response bias. Sci. Rep. 9,1 –11 (2019).
79. Nestvogel, D. B. & McCormick, D. A. Visual thalamocortical mechanisms of
waking state-dependent activity and alpha oscillations. Neuron 110, 120 –138.
e124 (2022).
80. Zilbershtain-Kra, Y., Graf ﬁ, S., Ahissar, E. & Arieli, A. Active sensory
substitution allows fast learning via effective motor-sensory strategies. Iscience
24, 101918 (2021).
81. Guinan J. J. Jr. The cochlea . p. 435-502 (Springer, 1996).
82. Jennings, S. G. & Strickland, E. A. Evaluating the effects of olivocochlear
feedback on psychophysical measures of frequency selectivity. J. Acoust. Soc.
Am. 132, 2483 (2012).
83. Rosen, S. Temporal information in speech: acoustic, auditory and linguistic
aspects. Philos. Trans. R. Soc. Lond. Ser. B Biol. Sci. 336, 367 –373 (1992).
84. Drullman, R., Festen, J. M. & Plomp, R. Effect of temporal envelope smearing
on speech reception. J. Acoust. Soc. Am. 95, 1053 –1064 (1994).
85. van der Horst, R., Leeuw, A. R. & Dreschler, W. A. Importance of temporal-
envelope cues in consonant recognition. J. Acoust. Soc. Am. 105, 1801 –1809
(1999).
86. He, J. & Hu, B. Differential distribution of burst and single-spike responses in
auditory thalamus. J. Neurophysiol. 88, 2152 –2156 (2002).
87. Hu, B. Functional organization of lemniscal and nonlemniscal auditory
thalamus. Exp. Brain Res. Exp. Hirnforsch. Exp. Cereb. 153, 543 –549 (2003).
88. Steriade, M., Jones, E. G. & McCormick, D. A. Thalamus. Vol. I: Organisation
and Function (Elsevier, 1997).
89. Malmierca, M. S., Merchan, M. A., Henkel, C. K. & Oliver, D. L. Direct
projections from cochlear nuclear complex to auditory thalamus in the rat. J.
Neurosci. 22, 10891 –10897 (2002).
90. Sherman, S. M. & Guillery, R. W. Functional organization of thalamocortical
relays. J. Neurophysiol. 76, 1367 –1395 (1996).
91. McCormick, D. A. & von Krosigk, M. Corticothalamic activation modulates
thalamic ﬁring through glutamate “metabotropic” receptors. Proc. Natl. Acad.
Sci. USA 89, 2774 –2778 (1992).
92. Ojima, H. Terminal morphology and distribution of corticothalamic
ﬁbers
originating from layers 5 and 6 of cat primary auditory cortex. Cereb. Cortex 4,
646–663 (1994).
93. Yu, Y., Xiong, Y., Chan, Y. & He, J. Corticofugal gating of auditory
information in the thalamus: an in vivo intracellular recording study. J.
Neurosci. 24, 3060 –3069 (2004).
94. Giraud, A. L. et al. Representation of the temporal envelope of sounds in the
human brain. J. Neurophysiol. 84, 1588 –1598 (2000).
95. Morton, J., Marcus, S. & Framkish, C. Perceptual centers (P-centers). Psychol.
Rev. 83, 405 –408 (1976).
96. Goswami, U. et al. Amplitude envelope onsets and developmental dyslexia: a
new hypothesis. Proc. Natl. Acad. Sci. USA 99, 10911 –10916 (2002).
97. Scott, S. K. P-centers - An Acoustic Analysis . PhD thesis (University College,
1993).
98. Downer, J. D., Verhein, J. R., Rapone, B. C., O ’ Connor, K. N. & Sutter, M. L.
An emergent population code in primary auditory cortex supports selective
attention to spectral and temporal sound features. J. Neurosci. 41, 7561 –7577
(2021).
99. Antunes, F. M. & Malmierca, M. S. Corticothalamic pathways in auditory
processing: recent advances and insights from other sensory systems. Front.
Neural Circuits 15, 721186 (2021).
100. Williamson, R. S. & Polley, D. B. Parallel pathways for sound processing and
functional connectivity among layer 5 and 6 auditory corticofugal neurons.
Elife 8, e42974 (2019).
101. Guo, W., Clause, A. R., Barth-Maron, A. & Polley, D. B. A corticothalamic
circuit for dynamic switching between feature detection and discrimination.
Neuron 95, 180 –194.e185 (2017).
102. Haegens, S. & Golumbic, E. Z. Rhythmic facilitation of sensory processing: a
critical review. Neurosci. Biobehav. Rev. 86, 150 –165 (2018).
103. Leszczynski, M. & Schroeder, C. E. The role of neuronal oscillations in visual
active sensing. Front. Integr. Neurosci. 13 (2019).
104. Pittman-Polletta, B. R. et al. Differential contributions of synaptic and
intrinsic inhibitory currents to speech segmentation via ﬂexible phase-locking
in neural oscillators. PLoS Computational Biol. 17, e1008783 (2021).
105. Welker, W. I. Analysis of snif ﬁng of the albino rat. Behaviour 22, 223 –244
(1964).
106. Halpern, B. P. Tasting and smelling as active, exploratory sensory processes.
Am. J. Otolaryngol.
4, 246 –249 (1983).
107. Kepecs, A., Uchida, N. & Mainen, Z. F. The sniff as a unit of olfactory
processing. Chem. Senses 31, 167 –179 (2006).
108. Mainland, J. & Sobel, N. The sniff is part of the olfactory percept. Chem. Senses
31, 181 –196 (2006).
109. Moore, J. D. et al. Hierarchy of orofacial rhythms revealed through whisking
and breathing. Nature 497, 205 –210 (2013).
110. Mo, C. & Sherman, S. M. A sensorimotor pathway via higher-order thalamus.
J. Neurosci. 39, 692 –704 (2019).
111. Lohse, M., Dahmen, J. C., Bajo, V. M. & King, A. J. Subcortical circuits
mediate communication between primary sensory cortical areas in mice. Nat.
Commun. 12,1 –14 (2021).
112. Edelman, G. M. & Gally, J. A. Reentry: a key mechanism for integration of
brain function. Front. Integr. Neurosci. 7, 63 (2013).
113. Luis-Islas, J., Luna, M., Floran, B. & Gutierrez, R. Optoception: perception of
optogenetic brain perturbations. Eneuro 9, ENEURO.0216-22.2022 (2022).
114. Yizhar, O., Fenno, L. E., Davidson, T. J., Mogri, M. & Deisseroth, K.
Optogenetics in neural systems. Neuron 71,9 –34 (2011).
115. Yu, C., Derdikman, D., Haidarliu, S. & Ahissar, E. Parallel thalamic pathways
for whisking and touch signals in the rat. PLoS Biol. 4, e124 (2006).
116. Mahn, M. et al. Ef ﬁcient optogenetic silencing of neurotransmitter release with
a mosquito rhodopsin. Neuron 109, 1621 –1635.e1628 (2021).
117. Saraf-Sinik, I., Assa, E. & Ahissar, E. Motion makes sense: an adaptive motor-
sensory strategy underlies the perception of object location in rats. J. Neurosci.
35, 8777 –8789 (2015).
118. Mountcastle, V. B. Temporal-order determinants in a somatesthetic frequency
discrimination - sequential order coding. Ann. N. Y. Acad. Sci. 682, 150 –170
(1993).
119. Georgopoulos, A. P., Schwartz, A. B. & Kettner, R. E. Neuronal population
coding of movement direction. Science 233, 1416 –1419 (1986).
120. Wise, S. P. Monkey motor cortex: movements, muscles, motoneurons and
metrics. Trends Neurosci. 16,4 6 –49 (1993).
121. Fetz, E. E. Cortical mechanisms controlling limb movement. Curr. Opin.
Neurobiol. 3, 932 –939 (1993).
122. Sachidhanandam, S., Sreenivasan, V., Kyriakatos, A., Kremer, Y. & Petersen,
C. C. Membrane potential correlates of sensory perception in mouse barrel
cortex. Nat. Neurosci. 16, 1671 –1677 (2013).
123. Huber, D. et al. Sparse optical microstimulation in barrel cortex drives learned
behaviour in freely moving mice. Nature 451,6 1 –64 (2008).
124. O’ Connor, D. H. et al. Neural coding during active somatosensation revealed
using illusory touch. Nat. Neurosci. 6, 958 –965 (2013).
125. Prsa, M., Galiñanes, G. L. & Huber, D. Rapid integration of arti ﬁcial sensory
feedback during operant conditioning of motor cortex neurons. Neuron 93,
929–939.e926 (2017).
126. Takatoh, J. et al. The whisking oscillator circuit. Nature 609, 560 –568
(2022).
127. Abbasi, A., Goueytes, D., Shulz, D. E., Ego-Stengel, V. & Estebanez, L. A fast
intracortical brain –machine interface with patterned optogenetic feedback. J.
Neural Eng. 15, 046011 (2018).
128. Sun, Z., Schneider, A., Alyahyay, M., Karvat, G. & Diester, I. Effects of
optogenetic stimulation of primary somatosensory cortex and its projections
PERSPECTIVE COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4
10 COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio
to striatum on vibrotactile perception in freely moving rats. Eneuro 8,
ENEURO.0453-20.2021 (2021).
129. Chen, S. C.-Y. et al. Similar neural and perceptual masking effects of low-
power optogenetic stimulation in primate V1. Elife 11, e68393 (2022).
130. Herrmann, C. S., Rach, S., Neuling, T. & Strüber, D. Transcranial alternating
current stimulation: a review of the underlying mechanisms and modulation
of cognitive processes. Front. Hum. Neurosci. 7, 279 (2013).
131. Kasten, F. H. & Herrmann, C. S. Discrete sampling in perception via neuronal
oscillations— Evidence from rhythmic, non ‐invasive brain stimulation. Eur. J.
Neurosci. 55, 3402 –3417 (2022).
132. Jaegle, A. & Ro, T. Direct control of visual perception with phase-speci ﬁc
modulation of posterior parietal cortex. J. Cogn. Neurosci. 26, 422–432 (2014).
133. Zoefel, B., Archer-Boyd, A. & Davis, M. H. Phase entrainment of brain
oscillations causally modulates neural responses to intelligible speech. Curr.
Biol. 28, 401 –408.e405 (2018).
134. Sosnik, R., Haidarliu, S. & Ahissar, E. Temporal frequency of whisker
movement. I. Representations in brain stem and thalamus. J. Neurophysiol. 86,
339–353 (2001).
Acknowledgements
This project has received funding from the European Research Council (ERC) under the
EU Horizon 2020 Research and Innovation Programme (grant agreement No 786949),
the United States-Israel Binational Science Foundation (BSF, grant No. 2017216), the
Israel Science Foundation (grant No. 2237/20), the Weizmann-UK collaboration grant,
the Yotam project and the Weizmann institute sustainability and energy research
initiative and the USA Air Force Of ﬁce of Scienti ﬁc Research (AFOSR) (grant No.
FA9550-22-1-0346).
Author contributions
E.A., G.N., El.A., O.K., and I.S.-S. wrote the manuscript.
Competing interests
The authors declare no competing interests.
Additional information
Supplementary information The online version contains supplementary material
available at https://doi.org/10.1038/s42003-023-04881-4.
Correspondence and requests for materials should be addressed to Ehud Ahissar.
Peer review information Primary Handling Editor: Karli Montague-Cardoso.
Reprints and permission information is available at http://www.nature.com/reprints
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in
published maps and institutional af ﬁliations.
Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative
Commons license, and indicate if changes were made. The images or other third party
material in this article are included in the article ’ s Creative Commons license, unless
indicated otherwise in a credit line to the material. If material is not included in the
article’ s Creative Commons license and your intended use is not permitted by statutory
regulation or exceeds the permitted use, you will need to obtain permission directly from
the copyright holder. To view a copy of this license, visit http://creativecommons.org/
licenses/by/4.0/.
© The Author(s) 2023
COMMUNICATIONS BIOLOGY | https://doi.org/10.1038/s42003-023-04881-4 PERSPECTIVE
COMMUNICATIONS BIOLOGY |           (2023) 6:562 | https://doi.org/10.1038/s42003-023-04881-4 | www.nature.com/commsbio 11
