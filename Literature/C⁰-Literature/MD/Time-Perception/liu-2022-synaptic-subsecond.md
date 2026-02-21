# liu-2022-synaptic-subsecond

Article https://doi.org/10.1038/s41467-022-35395-y
Synaptic basis of a sub-second representa-
tion of time in a neural circuit model
A. Barri 1 ,M .T .W i e c h e r t1,M .J a z a y e r i2,3 &D .A .D i G r e g o r i o1
Temporal sequences of neural activity are essential for driving well-timed
behaviors, but the underlying cellular and circuit mechanisms remain elusive.
We leveraged the well-deﬁned architecture of the cerebellum, a brain region
known to support temporally precise actions, to explore theoretically whether
the experimentally observed diversity ofshort-term synaptic plasticity (STP) at
the input layer could generate neural dynamics sufﬁcient for sub-second
temporal learning. A cerebellar circuit model equipped with dynamic synapses
produced a diverse set of transient granule cellﬁring patterns that provided a
temporal basis set for learning precisely timed pauses in Purkinje cell activity
during simulated delay eyelid conditioning and Bayesian interval estimation.
The learning performance across time intervals was inﬂuenced by the tem-
poral bandwidth of the temporal basis, which was determined by the input
layer synaptic properties. The ubiquity of STP throughout the brain positions it
as a general, tunable cellular mechanism for sculpting neural dynamics and
ﬁne-tuning behavior.
The neuronal representation of time on the sub-second timescale is a
fundamental requisite for the perception of time-varying sensory sti-
muli, generation of complex motor plans, and cognitive anticipation of
action
1–4. But how neural circuits acquire speci ﬁct e m p o r a lc o n -
tingencies to drive precisely timed behaviors remains elusive. A pro-
gressive increase in ﬁring rate ( “ramping”) towards a threshold can
represent different elapsed times by altering the slope of the ramping
behavior. Elapsed time can also be encoded by a population of neurons
that ﬁre in a particular sequence ( “time cells”)
5–8. Sequential synaptic
connections between neurons (synﬁre chains) can explain the neural
sequences representing bird song 9 and contribute to time delays
necessary to cancel self-generated sensory stimuli in the electro-
sensory lobe of mormyrid ﬁsh
10. Temporal dynamics of neural popu-
lation activity can also be reproduced by training recurrent neural
network models
11–13. Nevertheless, the search for a candidate
mechanism for generating a temporal reference (biological timer) for
neural dynamics is an ongoing challenge.
Short-term synaptic plasticity (STP) is the rapid change in synaptic
strength occurring over tens of milliseconds to seconds that is thought
to transform presynaptic activity into distinct postsynaptic spike
patterns
14. Depression and facilitation of synaptic strength can act as
low-and high-pass ﬁlters, respectively15, and synaptic depression can
mediate gain modulation 16,17. Network models of neocortical con-
nectivity exhibit improved temporal pattern discrimination when
augmented with STP
18. Within recurrent neural networks, the long
timescales of cortical synaptic facilitation provide the substrate for
working memory
19. Finally, low-gain recurrent network models that
include STP also show enriched neural dynamics and generate neural
representations of time 20. However, experimental evidence of STP-
dependent circuit computations is rare and is associated mainly with
sensory adaptation
21.
The cerebellar cortex is a prototypical microcircuit known to be
important for generating temporally precise motor 22 and cognitive
behaviors23–26 on the sub-second timescale. It receives mossy ﬁbers
(MFs) from various sensory, motor and cortical areas. MFs are thought
to convey contextual information and converge onto granule cells
(GCs), the most numerous neuron i n the brain. The excitatory GCs
project onto the inhibitory molecular layer interneurons and Purkinje
cells (PCs). PCs, being the sole output neurons of the cerebellar cortex,
inhibit neurons in the deep cerebellar nuclei. According to the Marr-
Received: 31 March 2022
Accepted: 29 November 2022
Check for updates
1Institut Pasteur, Université Paris Cité, Synapse and Circuit Dynamics Laboratory, CNRS UMR 3571 Paris, France. 2McGovern Institute for Brain Research,
Massachusetts Institute of Technology, Cambridge, MA, USA. 3Department of Brain and Cognitive Sciences, Massachusetts Institute of Technology,
Cambridge, MA, USA. e-mail: alessandrobarri@gmail.com; david.digregorio@pasteur.fr
Nature Communications|         (2022) 13:7902 1
1234567890():,;
1234567890():,;
Albus-Ito model of cerebellar cortical circuit computations, precisely
timed Purkinje cell activity can be learned by adjusting the synaptic
weights formed by GCs with differing activity patterns
27,28.T h i sl a r g e l y
feed-forward circuitry has been proposed to learn the temporal con-
tingencies required for prediction from neural sequences across the
population of GCs within the input layer29. The synapses between MFs
and GCs are highly variable in their synaptic strength and STP time
course
30. Therefore, we hypothesized that STP of MF-GC synapses could
be used as internal timers for a population clock within the cerebellar
cortex to generate neural dynamics necessary for temporal learning.
To elaborate this hypothesis, we modeled the cerebellar cortex as
a rate-based two-layer perceptron network that includes realistic MF-
GC connectivity and STP dynamics. The model reproduces learned PC
activity associated with a well-known temporal learning task: delay
eyelid conditioning
31. The timescales of STP determined the temporal
characteristics of the GC population activity, which de ﬁned the tem-
poral window of PC temporal learning. The width of PC pauses scaled
proportionally with the learned time intervals, similar to experimen-
tally observed scalar variability of the eyelid conditioning behavior
32.
Additionally, we found that STP-driven GC activity was well suited to
implement a Bayesian estimator of time intervals
33. We propose that
within neural circuits, dynamic synapses serve as tunable clocks that
determine the bandwidth of neural circuit dynamics and enable
learning temporally precise behaviors.
Results
Cerebellar cortex model with STP
The cerebellar cortex can be modeled as a two-layer perceptron that
performs pattern separation of static inputs
27,28,34,35. Cerebellar models of
temporal processing are generally supplemented with additional
mechanisms that generate temporally varying activity patterns in the GC
layer
10,29,36,37. To test whether heterogeneous MF-GC STP is sufﬁcient to
support temporal learning, we implemented STP of the MF-GC synapse
in a simpliﬁed cerebellar cortex model, hereafter referred to as CCM
STP.
This model deliberately omits all other potential sources of temporal
dynamics. In particular, in most of the simulations presented here, we did
not include recurrent connectivity (Fig.1b). STP was simulated using a
parallel vesicle pool model of the MF-GC synapse, similar to ref.38.I t
comprises two readily releasable and depletable vesicle pools, synaptic
facilitation, and postsynaptic desensitization. To reproduce the observed
functional synaptic diversity, we set vesicle fusion probabilities ( p
v),
synaptic pool sizes (N), and synaptic facilitation to match the relative
strengths, paired-pulse ratios, and transient behaviors acrossﬁve differ-
ent types of synapses that were previously characterized30 (Fig 1a2–a6).
Importantly, the longest timescale in CCMSTP is associated with a 2 s
vesicle reﬁlling time constant of the slow vesicle pool (τref =2 s ,F i g .1a1).
To capture depression over long timescales38,39,w ei n t r o d u c e dap h e -
nomenological parameter (pref = 0.6) that effectively mimics a simpliﬁed
form of activity-dependent recovery from depression (see Methods).
The CCMSTP consisted ofﬁring rate units representing MFs, GCs, a
single PC, and a single molecular layer interneuron, i.e., each neuron’s
activity was represented by a single continuous value corresponding to
an instantaneous ﬁring rate. Each GC received 4 MF synapses, ran-
domly selected from the different synapse types according to their
experimentally characterized frequency of occurrence
30. Importantly,
we associated different synapse types with different MF ﬁring rates
(Fig. 1b, left panels, see Methods). Highpv MF inputs were paired with
high average ﬁring rates (primary sensory groups 1, 2) and low pv
synapses with MF inputs with comparatively low average ﬁring rates
(secondary/processed sensory groups 3, 4, 5), according to experi-
mental observations40,41. We will reconsider this relationship below.
To examine CCMSTP network dynamics, input MF activity patterns
were sampled every second from respective ﬁring rate distributions
s h o w ni nF i g .1b. Each change in MF patterns evoked transient changes in
M F - G Cs y n a p t i cw e i g h t s ,w h i c hin turn generated transient GCﬁring rate
responses that decayed at different rates to a steady-state (Fig.1c). Similar
to experimentally recorded PC responses to sensory stimuli in vivo42,
switches between different MF activty patterns also generated hetero-
geneous transient changes in the PC ﬁring rate, whose directions and
magnitudes were controlled by the ratio of the average excitatory to
inhibitory weight (Fig.1c, bottom). In contrast, when MF-GC STP was
removed, the transient GC and PC responses disappeared (Fig.1d). The
amplitude of the ﬁring rate transients increased as the difference from
one MF pattern to the next increased, similar to previous theoretical
work
16. Sequential delivery of uncorrelated MFﬁring patterns in CCMSTP
(Fig. 1e) generated GC and PC transien ts with broadly distributed
amplitudes (Fig.1f1,2), which were progressively reduced as the relative
change in MF rate decreased (Fig. 1g). Thus, dynamic MF-GC synapses
allow both GCs and PCs to represent the relative changes in sensory
stimuli.
Simulating PC pauses during eyelid conditioning
We next explored whether MF-GC STP diversity permits learning of
precisely timed PC pauses associated with delay eyelid conditioning, a
prototypical example of a cerebellar cortex-dependent learning. In this
task, animals learn to use a conditioned stimulus (CS) to precisely time
eyelid closure in anticipation of an aversive unconditioned stimulus
(US). This eyeblink is driven by a preceding decrease in PC ﬁring
rates
31,43 (Fig. 2a). Since the CS is typically constant until the time of the
US and a precisely timed eyelid response can be learned even if the CS
is replaced by direct and constant MF stimulation
44,45,w em o d e l e dC S
delivery in the CCMSTP by an instantaneous switch to a novel MF input
pattern that persists over the duration of the CS (Fig. 2a). Most GC
activity transients exhibited a characteristic rapid increase or decrease
in ﬁring rate, followed by an exponential-like decay in ﬁring rate
(Fig. 2c). In contrast to other models of eyelid conditioning
29,t h e
activity of most GCs in the CCMSTP peaked only once, occurring shortly
(<50ms) after the CS onset (Fig. 2c). However, the distribution of GC
ﬁring rate decay times across the population was highly variable with a
fraction of GCs showing decay times to 10% of the transient peak as
long as 700 ms (Fig. 2c, d).
To test whether the GC population dynamics could act as a basis
set for learning the precisely timed PC ﬁring rate pauses known to
drive the eyelid response, we subjected the GC-PC synaptic weights to
a gradient descent-based supervised learning rule
46.T h er u l e’s target
signal consisted of a square pulse (zeroﬁring rate at a speciﬁc time bin)
at the designated time of the PCﬁring rate pause (Fig.2e, dotted line).
In the course of learning, there was a progressive acquisition of a pause
in the PC ﬁring rate (Fig. 2e). However, without MF-GC STP, the PC
pause did not develop (Fig. 2e, pink). We tested learning of different
delay intervals ranging from 25 ms to 700 ms and found that PC pauses
could be generated for all delays. The PC pause amplitude and tem-
poral precision (time and width) decreased with increasing CS-US
delays (Fig. 2f), reminiscent of the shape of PC simple-spike pauses
recorded during eyelid conditioning
31.
Why might the learned PC pause amplitude and temporal preci-
sion be reduced for longer CS-US delays? The parameters associated
with the learning algorithm (e.g. the number of iterations) are identical
for each CS-US delay. The state of the GC population activity, in con-
trast, changes throughout the CS. Once all GC activity dynamics reach
steady-state, temporal discrimination by PCs is diminished, and
interval learning becomes impossible. In other words, for temporal
learning to be effective, changes in GCﬁring rates must be prominent
over the relevant timescale. Indeed, eyeblink conditioning simulations
where slow or fast GCs were removed, the efﬁciency of generating PC
pauses for short and long intervals were reduced (Fig. S2). CCM
STP
simulations thus demonstrate that a GC temporal basis generated by
MF-GC STP is suf ﬁcient to reproduce the cerebellar cortex computa-
tion underlying delay eyelid conditioning and suggests that the time-
scale of GC dynamics inﬂuences the timescale of behavioral learning.
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 2
Analysis of the synaptic mechanism underlying GC transient
responses using a reduced model
PC temporal learning requires transient GC activity responses, which in
our model only arise from STP at the MF-GC synapse30,39.H o wa r et h e
dynamics of synapses and GCs determined by quantal and ﬁring rate
parameters? The complexity of the full CCMSTP with many interacting
parameters makes it dif ﬁcult to assess the effect of each synaptic
parameter. To overcome this challenge, we developed a reduced MF-
GC synapse model, which was analytically solvable for an instanta-
neous and persistent switch of MF rates. This allowed us to identify the
key computational building blocks of CCM
STP and explore how they
control the overall behavior of the model. Speci ﬁcally, we omitted
a1
b
0 0.2 0.4
W (C)
0
5
10
15
0 0.02 0.04
ppr = 0.6
W (C)
0
5
10
15
0 0.2 0.4
0 0.02 0.04
ppr = 0.74
W (C)
0
5
10
15
00 . 2 0 . 4
00 . 0 2 0 . 0 4
ppr = 1.04
group 1
group 2
group 3
group 4
group 5
pre-synaptic
depletion + facilitation
post-synaptic
desensitization
W (C)
0
5
10
15
00 . 2 0 . 4
00 . 0 2 0 . 0 4
ppr = 0.78
W (C)
0
5
10
15
time (s)
00 . 2 0 . 4
00 . 0 2 0 . 0 4
ppr = 1.33
Purkinje cell
Granule cells
Mossy fibres
Molecular layer
interneuron
M=100
N=3000
W(t)
JE
JI
pdfpdfpdfpdf
firing rate (Hz)
0 100 200 300
-
16%
16%
38%
24%
6%
pdf
a2
a3
a5
a6
a4
e
g
100
50 
1  MF idx
0
100
200
300firing rate [Hz]
0123
time (s)
100
50 
1  GC idx
0
50
100
150firing rate [Hz]
00 . 51
correlation
0
0.2
0.4
0.6
0.8
1
norm. trans. SD
00 . 3 0 . 6
-50
0
50
firing rate
00 . 3 0 . 6
-50
0
50
100
150firing rate
00 . 3 0 . 6
00 . 3 0 . 6
time after CS onset (s)
GC transients
PC transients
f1
f2
corr = 0 corr = 0.85
corr = 0 corr = 0.85
time (s)
c
without STP transientswith STP
JE/JI < 1
JE/JI ~ 1
JE/JI > 1
MFs
GCs
d
0
100
200
300rates (Hz)
0.1
0.2
0.3
weights (C)
0
50
100rates (Hz)
012345
time (s)
0
40
80
rates (Hz)
PC
time (s)
012345
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 3
short-term facilitation and postsynaptic desensitization and reduced
the synaptic model to a single population of high pv synapses
(“drivers”30) and a single population of low pv synapses
(“supporters”30), each with a fast and a slow re ﬁlling ready-releasable
pool (Fig. 3b), thus obtaining a model where STP results from vesicle
depletion only. Each GC received exactly two driver and two supporter
MF inputs with random and pairwise distinct identities (Fig.3a).
In this reduced model, an instantaneous and persistent switch of
MF ﬁring rates generates an average postsynaptic current (Isyn(t)) for
each vesicle pool that is remarkably simple. It features a sharp transient
change, followed by a mono-exponential decay to a steady-state
synaptic current amplitude,A
s,( F i g .3c) and can be generally expressed
as
IsynðtÞ = As + At e
/C0 t
τsyn ð1Þ
Here, As is a time-invariant component and At e
/C0 t
τsyn is a transient
component with synaptic relaxation time constant τsyn (Fig. 3c) and
amplitude At. This transient component determines the synapse ’s
ability to encode the passage of time.
The solution of the synaptic dynamics model reveals the crucial
dependence of τsyn and At on the presynaptic and ﬁring rate
Fig. 1 | Cerebellar cortex model with short-term synaptic plasticity within
the input layer (CCMSTP). a1 Synaptic model scheme showing the principal para-
meters. a2-6 Properties of the ﬁve model synapse types matching experimental
groups from ref.30. Left: Schemes show differences in presynaptic parameters; the
postsynaptic side is identical for all groups. Right: average synaptic weights in
response to repetitive 100 Hz stimulation as in ref. 39. Insets: First ﬁve responses
with paired-pulse ratio (PPR) roughly mimic results from ref.30. Color code for
synapse groups is the same as in ref. 30. b Scheme of CCMSTP. MFs are classiﬁed
according to the groups in (a). Percentages indicate relative frequency of MF
groups. Insets: ﬁring rate distributions for different MF groups.c Simulation of
CCMSTP with randomly drawn JE weights. First panel: 5 sample MFs. Every second,
MF activity is re-drawn from distributions in (b). Second panel: Normalized weights
of 10 example MF-GC synapses. Third panel: activity of 10 sample GCs. Last panel:
PC activity with different shades of gray indicating different E/I ratios onto the PC.
d Same as c but without STP transient dynamics. Low amplitude GC and PC ﬁring
rate transients result from 10 ms GC integration time constant. e Example simula-
tion in which correlated (black symbols) and uncorrelated (red symbols) MF pat-
terns were presented to the network in alternation. The correlation coefﬁcient for
sequential patterns was ≈0:85. Firing rates are color-coded. f1 Steady-state sub-
tracted GC responses from simulation in (e) for uncorrelated (left) and correlated
MF pattern switches (right). f2 Same as (f1)b u tf o rP C .g Normalized standard
deviation of PC transient amplitudes for switches between MF patterns of differing
levels of correlation.
e
GC population dynamicsab c
time after CS onset (s)
4000
20001000
15010
50
# trials
PC firing rate (Hz)
target signal
no STP0
10
20
30
40
50
0.750.50.250
1
1000
GC index
2
3
4
5
1MF group
0
50
100
150
200
250
firing rate [Hz]
0
50
100
150
200
firing rate [Hz]
0 0.25 0.5 0.75
time after CS onset (s)
-1
0
1
norm. firing rate
0 0.25 0.5 0.75
time after CS onset (s)
0
100
200
300 firing rate (Hz)
Mossy Fibers (CS)
target time
PC learningGC decay times fd Learned PC responses
PC firing rate (Hz)
0 0.25 0.5 0.75
0
10
20
30
40
50 CS
50
700 300200100 500
time after CS onset (s)
target times
0 0.2 0.4 0.6
90% decay time (s)
10-2
10-1
100
101
log(pdf)
Fig. 2 | Simulating Purkinje cell pauses during eyelid conditioning. aScheme of
eyelid conditioning. CS: conditioned stimulus (red). US: unconditioned stimulus
(violet). After experiencing CS and US pairings at a ﬁxed temporal interval over
many trials, the animal learns to close its eyelid just before the US is delivered
(green). A pause in PC activity (blue) precedes the eyelid closure (target time, gray
dashed line).b The CS is modeled as an instantaneous change in MFﬁring rate. Top:
plot of ﬁring rates of 100 MFs, sorted according to synaptic types (MF groups). MF
ﬁring rates are color-coded and drawn according to the distributions shown in
Fig. 1b. Bottom: two sample MF rates per synaptic group. Colors as in Fig.1. c Model
GC responses to the CS. Top: 1000 GCs sorted according to averageﬁring rate after
CS onset. Firing rates are color-coded. Bottom: steady-state subtracted and indi-
vidually normalized GC transient responses.d Pdf of the distribution of GC activity
decay times to 10% of the transient peak. e Example of delay eyelid conditioning
over the course of 4000 learning steps for a 200 ms delay. Dashed line represents
the target time used in the supervised learning procedure. Without STP-induced GC
transients, no PC pause could be learned (pink line). f Simulated PC responses
after 4000 learning trials for each target time (colored dashed lines).
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 4
parameters (see “Methods”):
τsyn = τref
1+ αpvm ð2Þ
Here, α = τrefð1/C0 prefÞ, m is the MFﬁring rate persisting during the
CS, and the synaptic parameters pv, τref,a n dpref are deﬁned as above.
Equation (2) shows that τsyn is inversely related to the MF ﬁring rate
during the CS and the release probability,pv(Fig. 3d). Intuitively, this is
because higher pv and/or m lead to a higher rate of synaptic vesicle
fusion, and hence depletion, driving the synaptic response amplitude
to steady-state faster. Conversely, slow time constants arise from low
pv and/or low m with the maximum τsyn being equal to the vesicle
recovery time τref.
The transient amplitudeAt is given by
At = Npvm
1+ αpvm
αpvðm/C0 mpreÞ
1+ αpvmpre
ð3Þ
Here, N is the number of release sites. Importantly, and in contrast
to τsyn, At depends on the presynaptic MF ﬁring rate before the CS,
mpre, and the difference between the MFﬁring rates before and during
the CS. In particular, for both rates suf ﬁciently high, At becomes a
linear function of the normalized difference between m and mpre, i.e.
high p synapse low p synapse
GC
Drivers
Supporters
synaptic time constant:
synaptic input:
ab
c
firing rate (Hz)
0 100 200 300
(s)
0.2
0.4
0.6
0.8
1
pv=0.1
pv=0.2
pv=0.4
pv=0.6
pv=0.8
relative change of firing rate
-1 0 1 2
At )s/C( (
0
50
100
150
200
250
time
d
e
f g
MF rates (Hz) Synaptic currents
time after CS onset (s)
00 . 2 0 . 4
GC rate (Hz)
0
100
200
00 . 2 0 . 4
11
12
13
0
50
100
150
0
50
100
150
100
150
200
250
100
150
200
250
100 C/s
fast GC slow GC
time after CS onset (s)
00 . 2 0 . 4
GC rate (Hz)
0
100
200
00 . 2 0 . 4
11
12
13(C/s 103)
threshold
0
50
100
150
100
150
200
250
0
50
100
150
100
150
200
250
MF rates (Hz) Synaptic currents
100 C/s
0.2s
0.2s
(C/s 103)
Fig. 3 | MF-GC synaptic time constants and their relative weights determine the
time course of GC responses. a Scheme of GC inputs in the simpliﬁed synaptic
model. Each GC receives exactly two distinct high release probability driver (red)
and low release probability supporter MFs (blue).b Schemes of the reduced
synaptic model of high p
v (red) and low pv synapses (blue).c Left: scheme of single
pool response with the time constantτsyn (blue line) to aﬁring rate switch during CS
presentation (black solid line). The dashed black line separates the transient (At )
from the steady-state amplitude (As). Right: equations determining the synaptic
time constant and synaptic input. d Slow vesicle pool time constant (τsyn)v e r s u s
presynaptic MF ﬁring rate. Different shades of gray indicate different release
probabilities.e Driver synapse transient amplitude (At )v e r s u sr e l a t i v eﬁring rate
change for a baselineﬁring rate of 80 Hz (m−mpre/mpre, mpre= 80 Hz). A negative At
corresponds to a transient decrease in ﬁring rate. Same color code as in ( d).
f Sample fast GC. Left: driver and supporter MFﬁring rates drawn from thresholded
normal distributions (N thr (200 Hz, 15 Hz) andN thr (25 Hz, 15 Hz), respectively) and
the corresponding synaptic responses. For clarity, only theτsyn of the respective
slow pool is indicated. Upper right panel: GC threshold (dashed line), total synaptic
input (black line), total driver input (red line), and total supporter input (blue line).
The transient response is dominated by the driver input (red). Lower right panel:
resulting GC ﬁring rate response.g Like (f) but for a sample slow GC. The transient
response is dominated by the supporter input (blue).
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 5
At/ð m/C0 mpreÞ=mpre (Fig. 3e). At is sensitive to the relative and not the
absolute change in presynaptic rate, as observed previously16.
The transient GC activity results from the sum of eight synaptic
transient current components, (i.e. four inputs, each with two pools).
To illustrate the interplay between the At and τsyn,w ec o m p a r e dt h e
behavior of each synaptic input for a selected fast and slow GC (Figs.3f,
g). Generally, synaptic inputs from supporters display longer transient
currents than synaptic inputs from drivers (Figs.3f, g, middle panels)
due to their lower ﬁring rates (Figs. 3f, g, left panels) and low pv
(Fig. 3b). At is largely determined by the relative change in the
respective presynaptic MF ﬁring rates,ðm/C0 mpreÞ=mpre (Fig. 3fa n dg ,
left panels). Thus, “fast” GCs are generated when the high pv driver
inputs exhibit large relative changes inﬁring rates (Fig.3f). “Slow” GCs
are generated from synapses with a small relative change in driver
ﬁring rates, but large relative supporter (low p
v) rate changes paired
with low supporter rates during the CS (Fig.3g). Taken together, in the
reduced modelτsyn and At determine the effective timescales of the GC
responses and are explicitly in ﬂuenced by quantal parameters,
synaptic time constants, and the diversity of MF ﬁring rates.
The explicit inﬂuence of synaptic parameters on temporal
learning
Our simulations suggest that delay eyelid conditioning across multiple
delays necessitates GC population dynamics spanning multiple time-
scales (Fig.2,F i g .S 2 ) .S i n c ei n d i v i d u a lG Cﬁring rate dynamics depend
on the A
t and τsyn of their synaptic inputs (Fig.3), this implies that 1) the
spectrum of τsyn available to the network should cover the relevant
timescales and 2) the At associated with different τsyn, which can be
understood as the relative weights of synaptic transient components,
should be of comparable magnitude across τ
syn. To illustrate these
points, we used the reduced CCM STP to simulate eyelid response
learning with different ﬁring rate properties and examined the rela-
tionship betweenτsyn, At, the GC temporal basis, and learning outcome.
Importantly, since At and τsyn are not independent, the quantity of
interest is their joint distribution. We initially set up a reference
simulation by choosing MF ﬁring rate distributions such that the
diversity of GC transient responses and the temporal learning perfor-
mance (Fig. 4a) were comparable to the CCM
STP with native synapses
(Fig. 2f). For this case, the joint distribution shows that At decreased
with increasing τsyn .N o t et h a tAt is maximal when the MF ﬁring rates
increased from zero mpre to a ﬁnite m upon CS onset, maximizing m-
mpre (Eq. 3, see also Fig. S3b, c). We quanti ﬁed learning accuracy by
calculating an error based on 1) the PC response amplitude, 2) its full
width at half maximum and 3) the temporal deviation of its minimum
from the target delay (Fig. 4a, ﬁfth panel, Fig. S2a, see “Methods”").
Importantly, the degradation in temporal precision of the learned PC
pauses for longer CS-US intervals was concomitant with the reduction
of the A
t associated with longer τsyn (Fig. 4a ) .T h i ss u g g e s t st h a t
inspection of the joint distribution of τsyn and At can provide insight
into the temporal learning performance of the network.
When changing only the mean ﬁring rate of supporter MFs ( μS)
from 25 Hz to 70 Hz, the synaptic time constants were shortened due
to the inverse relationship betweenτ
syn and the mossy-ﬁber ﬁring rate
m (Fig. 4b, second panel). Consequently, and expectedly, the dis-
tribution of GC ﬁring rate decay times was shifted to shorter values,
and learning performance was degraded for all CS-US intervals, except
the 25 ms delay (Fig. 4b). Lowering the mean ﬁring rate of driver MFs
(μ
D) from 200 Hz to 100 Hz and increasing the standard deviation (σD)
from 15 Hz to 50 Hz, led to an overall increase of the time constants
contributed by driver synapses, as well as an increase in their relative
weight ( A
t;F i g . 4c, second panel, marginals). As a result, the joint
probability distribution shows a shift towards faster weighted time
constants. It also follows that GC transients are accelerated, and
learning precision is decreased for long CS-US intervals. Removing
synaptic currents originating from driver synapses only disrupted
learning PC pauses for the shortest CS-US interval (Fig. 4d). Reduced
model simulations with systematic parameter scans across a wide
range of MF ﬁring rate distributions for both synapse types suggested
that good synaptic regimes for temporal learning are achieved when
driver synaptic weights are comparable or smaller than those of the
slow supporting synapses (Fig. S4).
All the results taken together suggest that optimal learning occurs
when the spectrum ofτ
syn available to the network covers behaviorally
relevant timescales with balanced relative weights ( At). Synaptic and
GC activity timescales can therefore be tuned by simultaneously
modulating p
v and the absolute scale of m to provide the necessary
distribution of τsyn, whereas the relative change of MF ﬁring can be
used to tune the weight (At)o f τsyn.
Firing rate and synaptic parameters that improve temporal
learning performance
Thus far, we used the reduced model to explore how MF ﬁring rates
and synaptic properties inﬂuenced the timescales of GC activity and
the temporal precision of learned PC pauses. The model, however, was
constrained by (1) the use of only two synapse types, (2) ﬁxed release
probabilities (p
v), (3) MF ﬁring rates that were consistently higher for
high pv synapses than their low pv counterparts, and (4) an equal
number of driver and supporter synapses. We next considered how the
relaxation of these assumptions and speciﬁc parameter combinations
could inﬂuence the precision of learned PC pauses. In particular, we
simulated reduced models where, in addition to MFﬁring rates,p
v was
sampled from continuous distributions.
Equation(2) suggests that a positive correlation betweenpv and m
should broaden the distribution ofτsyn and broaden the time window
of learning. Speciﬁcally, we expect learning performance to improve
when high(low) ﬁring rate MFs are, on average, paired with high(low)
pv synapses. We chose uniformly distributedpv and MF ﬁring rates and
split both of these equally into two contiguous groups (Fig. 5a). We
performed training simulations in which we paired high pv(driver)
synapses with high ﬁring rates, or we paired low pv (supporter)
synapses and high MF ﬁring rates, and vice versa (Fig. 5b). Formally,
this is equivalent to adjusting the rank correlation (crk) between the pv
category (supporter or driver) and the m category (high or low,
Fig. 5b). We found better learning performance when pv and m were
positively correlated (Fig. 5c, Fig. S5). Indeed, primary vestibular
afferents that form driver-like synapses have been shown to have high
ﬁring rates
30,40 while supporter-like secondary vestibular afferents
have low ﬁring rates30,41.
Inspired by the number of synapse types observed
experimentally30,w ea u g m e n t e dt h en u m b e ro fs y n a p s eg r o u p sf r o m2
to 5 without changing the pv and ﬁring rate distributions (Fig.5d). We
reasoned that the introduction of a larger number of MG-GC synapse
types would in principle permit a stronger linear correlation between
p
v and m to occur (Fig. 5e), leading to a broader τsyn spectrum (not
shown) and an improved learning of PC pauses. Indeed, for highcrk,t h e
learning performance of theﬁve group CCMSTP was better than that of
the two-group CCM STP (compare Fig. 5ca n dF i g .5f, Fig. S5). These
simulation results suggest that good temporal learning performance
of CCM
STP can be achieved not simply by generating variability in
parameters, but by structuring, or tuning, the relationship betweenpv
and m.
Equipped with an understanding of how the synaptic and MF
rate parameters can generate different synaptic time constants,
we set out to further improve the temporal learning for longer
CS-US delays by adjusting the variance of the clustered MF rate
distributions. To increase the weighting of long τ
syn,w ei n v e r s e l y
scaled the variance of the MF ﬁring rate distributions with respect
to the mean ﬁring rate (Fig. 5g), thereby increasing At (Fig. 4c). As
expected, PC pause learning was better than when using equal-
width MF groups (Fig. 5g, Fig. S5). An additional enhancement of
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 6
learning performance could be achieved by adding a small frac-
tion of zero-rate MFs to the lowest group (Figs. 5g, 6% zero MFs,
same fraction as in Fig. 4a), which provide maximal At(see Fig. 4).
Finally, taking into account the experimental ﬁnding that low pv
synapses are more frequent than high pv synapses 30, we doubled
the fraction of MFs and release probabilities in the lowest group,
resulting in the best performance of all versions of CCM STP tested
here (Fig. 5g). These simulations show that positive correlations
between vesicle release probability and presynaptic ﬁring rate
broaden the temporal bandwidth o f circuit dynamics and improve
temporal learning.
STP permits learning optimal estimates of time intervals
Humans and animals have an unreliable sense of time and their timing
behavior exhibits variability that scales linearly with the base interval
47.
Previous work has found that humans seek to optimize their time
interval estimates by relying on their prior expectations. A canonical
example of this optimization is evident in the so-called ready-set-go-
task
48 in which subjects have to measure and subsequently reproduce
different time intervals. It has been shown that when the intervals are
drawn from a previously learned probability distribution (i.e., prior),
subjects integrate their noisy measurements with the prior to generate
optimal Bayesian estimates. For example, when the prior distribution is
Fig. 4 | Learning performance depends on MF ﬁring rate distributions. a First
panel: Driver and supporter MFﬁring rate pdfs (μD = 200 Hz,μS =2 5H z ,σD = σS =1 5
Hz). Second panel: Resulting joint At and τsyn distribution, featuring four partially
overlapping clusters, corresponding to the slow and fast pools for driver and
supporter synapses, and marginal distributions. The color code of the joint dis-
tribution scales logarithmically. Colors of marginal distributions indicate driver
(red) and supporter (blue) components. Third panel: Normalized GC transient
responses to CS. Inset: pdf of the distribution of decay times to 10% of the transient
peak. Fourth panel: learned PC pauses, averaged over n = 20 simulations with
different realizations of MF patterns and MF-GC connectivity. Dashed lines mark
CS-US intervals (color code is the same as in Fig.2e). Fifth panel: Error for each CS-
US interval is calculated based on PC response amplitude, full-width at half-
maximum and temporal deviation (Fig. S2a) and averaged over n = 20 realizations
of MF patterns and MF-GC connectivity. Black lines indicate the distribution ranges;
gray boxes indicate the 25th to 75th percentile range and black-white circles the
medians.b Same as a,b u tw i t hμ
S = 70 Hz. Inset: black line is the pdf for simulation
with μS = 70 Hz and gray line is the pdf from (a) for comparison. Fifth panel: change
in error relative to the average error in (a). c Same as (a), but with μD = 100 Hz and
σD =5 0H z . d Same as (a), but without driver inputs.
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 7
uniform, interval estimates are biased towards the mean of the prior,
and biases are generally larger for longer intervals that are associated
with more variable measurements (Fig. 6c). Such Bayes-optimal tem-
poral computations are evident in a wide range of timing tasks such as
time interval reproduction
48, coincidence detection 49,a n dc u e
combination50.
A recent study developed a cerebellar model called TRACE for
temporal Bayesian computations33. TRACE implements Bayesian inte-
gration by incorporating two features. First, it assumes that GCs form a
temporal basis set that exhibits temporal scaling. This feature accounts
for the scalar variability of timing. Second, it assumes that prior-
dependent learning alters the GC-PC synapses. This feature allows the
dentate nucleus neurons (DNs) downstream of PCs to represent a
Bayesian estimate of the time interval.
In our analysis of eyelid conditioning (Fig. 2), we showed that
CCM
STP generates PC ﬁring rate pauses whose width and amplitude
linearly scale with time (Fig. 6a). Therefore, we reasoned that CCMSTP
might have the requisite features for Bayesian integration. To test this
possibility quantitatively, we presented our model with variable
intervals drawn from various prior distributions. The interval was
introduced as a tonic input to MFs, similar to the CS in the eyelid
simulations. The onset of this tonic input caused an abrupt switch of
the MF input rates that persisted over the course of a trial. During
learning, we subjected the model to intervals sampled randomly from
a desired prior distribution.
We tested CCM
STP with ﬁve different uniform distributions of
ready-set intervals (25-150 ms, 50–200 ms, 100–300 ms, 200–400 ms,
300–500 ms), resulting in PC pauses that broadened for longer
interval distributions, and integrated DN activity that could easily
match the Bayesian least-square model
33 by adjusting a single para-
meter, the Weber fraction wweber (see “Methods”"; Fig. 6d, h). The
reduced model interval estimates were more similar to the Bayesian
estimates than for CCM
STP with native synaptic parameters, especially
for the 200 –400 ms and 300 –500 ms intervals (Fig. 6h–k). Never-
theless, in both cases the CCM STP simulations show that a GC basis
generated by MF-GC STP is sufﬁcient for driving Bayesian-like learning
of time intervals spanning several hundreds of milliseconds. It should
be noted that our GC temporal basis was not explicitly constructed to
accommodate scalar properties. Nevertheless, as in the TRACE model,
we observed that interval estimates were biased towards the mean and
that these biases were larger for longer intervals. These results suggest
that a GC basis set generated from the diverse properties of native
0 100 200pdf
MF firing rates (Hz)ab c
efMF firing rates (Hz)
g
d
h
anti-correlated pv and m correlated p v and m
0 0.5 1pdf
release probability (pv) 0 0.25 0.5 0.75
time after CS onset (s)
0
10
20
30
40
50PC firing rate (Hz)
0 0.25 0.5 0.75
time after CS onset (s)
0
10
20
30
40
50PC firing rate (Hz)
00 . 51pdf
release probability (pv)
0 100 200pdf
0 100 200pdf
00 . 51pdf
release probability (pv)
0 0.25 0.5 0.75
time after CS onset (s)
0
10
20
30
40
50
0 100 200pdf
00 . 51
release probability (pv)
pdf
0 0.25 0.5 0.75
time after CS onset (s)
0
10
20
30
40
50
MF firing rates (Hz) MF firing rates (Hz)
0
1 corr. = -0.91
0 100 200
MF rate (Hz)
0
1 corr. = 0.91
0
1
corr. = -0.91
0 100 200
MF rate (Hz)
0
1 corr. = 0.91
0 0.25 0.5 0.75
time after CS onset (s)
0
10
20
30
40
50PC firing rate (Hz)
0 0.25 0.5 0.75
time after CS onset (s)
0
10
20
30
40
50PC firing rate (Hz)
pv pv pv pv
Fig. 5 | Correlating release probability and MF ﬁring rates improves learning
performance. aTop: distribution of MFﬁring rates (m) used to drive the network,
divided into low (supporter, green) and high (driver, yellow) rates. Bottom: Dis-
tribution of synaptic release probabilities (p
v), divided into low (light gray) and high
(dark gray) probabilities.b Top: pv versus m for 500 sample synapses for a network
with a strong negative rank correlation between the m category (supporter or
driver) and the pv category (high or low). Bottom: same as top, but for strongly
positive correlatedm and pv. c Learned PC pauses for low (left) and high (right)
correlations. CS-US intervals are color-coded as in Fig.2f. Each curve is the average
of n = 20 simulations with different realizations of MF patterns and MF-GC con-
nectivity. d–f Same as (a–c), but for distributions divided into ﬁve groups. g Left:
MF rates and release probabilities for ﬁve synapse types where the average group
ﬁring rate is as in ( d), but the ﬁring rate variance progressively decreases with the
average rate. Right: resulting PC eyelid response learning for high correlations.
h Same as (g) but with zero-rate MFs added to the lowest rate distribution. Dashed
lines indicate the case when the count of lowest rates and release probabilities is
doubled.
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 8
MF-GC synapses likely exhibits a scalar property necessary for gen-
erating optimally timed behaviors.
Discussion
In order to generate temporally precise behaviors, the brain must
establish an internal representation of time. This theoretical study
posits that the diversity of synaptic dynamics is a fundamental
mechanism for encoding sub-second time in neural circuits. By using
eyelid conditioning as a benchmark task for the CCM
STP, we eluci-
dated the conditions under which the variability in MF-GC synaptic
dynamics generates a GC temporal basis set that represents elapsed
time and is suf ﬁcient for temporal learning on a sub-second scale.
According to David Marr ’s levels of analysis of information proces-
sing systems
51, our study connects all three levels, from the circuit
computation (learning timed PC pauses) to its underlying algorithm
(learning with a temporal basis set), and the fundamental biological
mechanism (STP diversity).
STP diversity as a timer for neural dynamics
Cerebellar adaptiveﬁlter models posit that GCs act as a heterogeneous
bank of ﬁlters that decompose MF activity into various time-varying
activity patterns - or temporal basis functions - which are selected and
summed by a synaptic learning rule at the PC to produce an output
ﬁring pattern that generates behaviors that minimize error signals
arriving via climbing ﬁbers
36,37.C C MSTP can be viewed as an adaptive
ﬁlter in which MF-GC synapses act as non-linear elements whoseﬁlter
properties are determined by the experimentally de ﬁned synaptic
parameters and modulated by the presynaptic MF ﬁring rates.
Recent theoretical work proposes that a scale-invariant neuronal
representation of a temporal stimulus sequence can be obtained by
using a population of leaky integrators that produce exponentially
decaying neural activity transients
52. Indeed, exponential-like activity
has been observed in the entorhinal cortex—a region that projects to
the hippocampus6. The exponential-like population activity is remi-
niscent of the GC temporal basis set in CCM STP following persistent
ﬁring rate changes. However, the MF-GC synaptic inputs are always a
mixture of multiple exponential components. Nevertheless, our work
suggests that STP could be a plausible biological mechanism explain-
ing exponential dynamics in neuronal populations
6 and merits further
theoretical and experimental investigation.
The use of an instantaneous and persistent change in MF activity
was motivated by the fact that eyelid conditioning can be achieved if
the CS is replaced with a constant MF stimulation
44,45,53. Recent evi-
dence from pons recordings during reaching suggests that MF activity
can be persistent with little dynamics 54.F o rd y n a m i cc h a n g e si nM F
rates, STP is likely to generate outputs that are phase-shifted and/or
the derivatives of their input
55. Using heterogeneity of MF-GC STP as a
mechanism for adaptive ﬁltering, even time-varying inputs will
ab
de f
00 . 51
10
20
30
40
50PC rate (Hz)
25-150 ms
50-200 ms
100-300 ms
200-400 ms
300-500 ms
00 . 51
-1
0
1
2
3
DN activity (a.u.)
g
hi j k
00 . 51
time after tm onset (s)
-1
0
1
2
3
DN activity (a.u.)
00 . 51
time after tm onset (s)
10
20
30
40
50PC rate (Hz)
Dentate nucleus cell
constant input
autapse
-
0 0.2 0.4 0.6 0.8
delay (s)
0
0.2
0.4
0.6
0.8FWHM (s)
0
1norm. Amplitude
rescaled DN activities
BLS estimator
te (s)
RMSE (10 -2 s)RMSE (10 -2 s)
tm (s)
te (s)
0.1 0.2 0.3
0
0.1
0.2
wweber = 0.12
wweber = 0.09
tm (s)
0.2 0.4 0.6
0
0.2
0.4
0.6
0 
5 
10
15
0 
5 
10
15
0.2 0.4 0.6
0
0.2
0.4
0.6
0.1 0.2 0.3
0
0.1
0.2
CCMSTP + DCN c
tm
Sample interval
distribution
te
tm
te
Estimated 
interval
Measured interval
Prior
CCMSTP + DCN
ts
Noise
full model
reduced model
Fig. 6 | STP-generated temporal basis enables the computation of Bayesian
time-interval estimates. aFull width at half maximum (cyan) and normalized
amplitudes (magenta) of learned PC pauses versus delay interval from the experi-
mentally constrained CCMSTP (see Fig. 2). Solid lines are linear ﬁts. b Scheme of
CCMSTP with added dentate nucleus cell. c Scheme of Bayesian integration. The
sample intervalts (red dashed line, here drawn from a uniform distribution, upper
left) is subject to a noisy measurement yielding a measured intervaltm (lower left).
CCMSTP implements Bayesian integration yielding an estimated intervalte (right).
d PC responses after 12,000 learning trials, averaged overn = 20 simulations with
different realizations of MF patterns and MF-GC connectivity. Shaded area indicates
standard deviation. Different colors represent learning of different uniform sample
interval distributions.e Same as (d), but for DN cell activity.f Rescaled DN cell activity
for different learned interval distributions (colored) andﬁtted theoretical Bayesian
least squares (BLS) estimator (solid black line), withwweber = 0.12 resulting fromﬁt.
g Squared deviation of rescaled DN activity from the BLS estimator for all tested
intervals.h–k Same as (d–g), but for the reduced model. The reduced modelﬁring
rate parameters wereμD =2 0 0H z ,μS =2 0H z ,σD=10Hz andσS = 15 Hz and resulted in
DN activity consistent with a Bayesian least squares model withwweber =0 . 0 9 .
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 9
effectively be diversiﬁed within the GC layer and improve the precision
of temporal learning.
Synapses within the prefrontal cortex 56 and at thalamocortical
connections57 exhibit diverse ﬁring rate inputs and release
probabilities58, generating synaptic dynamics that could drive complex
neural dynamics. Reminiscent of PC ﬁring rate pauses during eyelid
conditioning, hippocampal time cells are thought to be generated by a
linear combination of exponentially decaying input activity patterns
from upstream entorhinal cortical neurons
6. More generally, it has
been shown that STP also provides a critical timing mechanism within a
recurrent neural network model of neocortical activity by facilitating
temporal pattern descrimination
18. We note that all synapses in this
study featured only a single STP timescale, but we expect that the
addition of heterogeneous STP would further diversify the network’s
dynamics and enhance its computational properties. Thus, these pre-
vious studies and our present study underscore the proposal that STP
diversity is a tunable timing mechanism for generating neural
dynamics across brain regions.
Timing mechanisms in the cerebellar cortex
In addition to MF-GC STP, the cerebellar cortex is equipped with
multiple mechanisms potentially enabling temporal learning
59.I n d e e d ,
time-varying MF inputs could directly provide a substrate for learning
elapsed time
60, but whether the observed diversity of MF ﬁring is
sufﬁcient to mediate temporally precise learning is unknown and
merits further exploration. Within the cerebellar cortex, unipolar
brush cells are thought to provide delay lines to diversify GC activity
patterns10,61,62,b u tt h e s ec e l lt y p e sa r er a r eo u t s i d et h em a m m a l i a n
vestibular cerebellum. The diversity of GC STP 63 could add to the
diversity of the effective GC-layer basis set 64.C o n s i s t e n tw i t ht h e
importance of MF-GC STP, delay eyelid conditioning was selectively
altered due to the loss of fast EPSCs in AMPAR KO mice
65. Simulations
including realistic NMDA and spillover dynamics66 can further enrich
the temporal scales available to the network67. It would be of particular
interest to investigate the role of MF-GC STP in the context of recur-
rent GC-Golgi-Cell-cell network models that have been shown to gen-
erate rich GC temporal basis sets
12,29. Finally, we note that MF-GC STP
and other timing mechanisms described above are not mutually
exclusive but presumably act in concert with the diverse intrinsic
properties of GCs
68 and PCs69 to cover different timescales of learning
or increase mechanistic redundancy.
Predictions of the CCMSTP
Our theory makes several testable predictions. The transient response
amplitude of PCs, which is proportional to the relative change inﬁring
rate, can serve as a detector of rapid changes in MF ﬁring patterns
(novelty) and thus amplify pattern discrimination similar to that
demonstrated for synapse-dependent delay coding
30. Consistent with
this prediction, single whisker de ﬂections have been shown to gen-
erate transient PC activity42.
CCMSTP predicts that persistent changes in MF activity would
generate exponential-like GC activity pro ﬁles (Figs. 2, 4). However,
although the majority of simulated GCs shown here are active at the
onset of the CS, this is not a necessary feature of CCM
STP.W h e nw e
included a single, average-subtracting Golgi cell (possibly representing
the “common mode” of Golgi Cell population activity
64), more GCs
showed delayed onsetﬁring and the variability of onset and peak times
(Fig. S6). This did not affect the learning performance of simulated
delay eyelid conditioning (Fig. S6). Note that our implementation of
Golgi cell feedback is simpli ﬁed and does not account for reciprocal
inhibition between multiple Golgi cells, which in simulations has also
been shown to generate diverse GC activity
12,29.T ot e s tt h e s ep r e d i c -
tions, MFs could be driven at constant rates using direct electrical or
optogenetic stimulation of the cerebellar peduncle in vivo or the white
matter in acute brain slices, with and without intact Golgi cell
inhibition. Unfortunately, high-temporal resolution population
recordings of GCs are challenging due to the small size of GC somata.
In the future, small impendence silicon probe recordings
70 or ultra-fast
optical indicators71 might permit experimentally testing our hypoth-
eses. If successful, we predict that the time course of GC responses
should be diverse and exponential-like, with prominent delayed
activity in some granule cells when Golgi cells are intact. Furthermore,
decreasing or increasing the MF ﬁring rate should in turn slow or
accelerate GC responses, respectively. Finally, for complex behavioral
experiments in which the MF activity is dynamic (and measurable), one
could examine which circuit connectivity of the CCM
STP best repro-
duces the measured GC activity.
The CCM STP is one of the few network models directly linking
quantal synaptic parameters and presynaptic activity dynamics to
population activity dynamics and temporal learning. Figures 3 and 4
show that the relative weight and temporal span of synaptic time
constants dictate the distribution of GCﬁring rate decay times and, in
turn, the timescales of temporal learning. Analytical solutions for
simple synapse models (Eq. (3)) provide insight into how synaptic
parameters in ﬂuence STP. For example, high levels of correlation
between p
v and m, coupled with balanced relative weights of the
synaptic time constants, generated a learning performance superior to
t h en a t i v es y n a p s e s( F i g .5d). Therefore, CCM
STP predicts that MFs
forming driver synapses (high pv) would have a high baseline and sti-
mulated ﬁring rates, while MFs forming supporter synapses (low pv)
would exhibit low baseline and stimulatedﬁring rates, albeit with large
relative changes inﬁring rates. Indeed, vestibular neurons, which have
been shown to exhibit high ﬁring rates72,73, produced MF-GC synapses
with high release probability30. In the C3 zone of the anterior lobe in
cats, speciﬁc ﬁring rates were associated with different MF types74.I ti s
tempting to hypothesize that nature tunes presynaptic activity and
synaptic dynamics (perhaps by homeostatic or activity-dependent
mechanisms) in order to preconﬁgure the window of temporal asso-
ciations required for a particular behavior.
Choice of the cerebellar learning rule
The learning rule we used here was adapted from a previous modeling
study that investigated cerebellar adaptation of the vestibular ocular
reﬂex and was argued to be biologically plausible 75. This synaptic
weight update rule is mathematically equivalent to a gradient descent
in which the error magnitude is transmitted via the climbing ﬁber
75.
Consequently, CCMSTP learning rule features graded climbing- ﬁber
responses and a gradual reduction in climbing- ﬁber spiking that is
concomitant with the progression of learning. These phenomena have
been observed experimentally
43,76. Moreover, a recent study that
thoroughly investigated the role of the climbing ﬁber spike in cere-
bellar learning found that the GC and climbing- ﬁber spike pairings
necessary for the induction of long-term depression/potentiation
under physiological conditions are compatible with a stochastic gra-
dient descent rule 46. The CCM STP learning rule can be seen as a
deterministic variant of this.
Synaptic implementation of a Bayesian computation
Bayesian theories of behavior provide an attractive framework for
understanding how organisms, including humans, optimize time per-
ception and precise actions despite the cumulative uncertainty in
sensory stimuli, neural representations, and generation of actions
48,77.
We found that CCM STP could generate biased time estimates con-
sistent with Bayesian computations. In general, the magnitude of bia-
ses for a Bayesian agent depends on the magnitude of timing
variability (i.e., Weber fraction). In our simulations, model parameters
corresponding to native synapses from the vestibular cerebellum
produced biases that were optimal for a typical weber fraction of 0.12.
However, CCM
STP is ﬂexible and can be adjusted to generate optimal
biases for a wide range of weber fractions. The exact relationship
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 10
between model parameters and wweber is an important question for
future research. We note that the timescales of synaptic properties
observed empirically in the vestibular cerebellum
30 are only suitable
for generating optimal estimates for relatively short time intervals.
Therefore, whether the synaptic mechanisms that underlie CCM STP
could accommodate timing behavior for longer timescales remains to
be seen. One intriguing hypothesis is that synaptic parameters in dif-
ferent cerebellar regions are tuned to generate optimal estimates for
different time intervals, similar to the timing variability observed for
cerebellar long-term synaptic plasticity rules
78.
Methods
MF-GC synapse model
The synaptic weight between the jth MF and the ith GC is denoted by
Wij.T h e ﬁring rate of the jth MF is represented by mj(t)a n dt h e
average current per unit time transmitted by the synapse between GCi
and MF j is
Isyn,ijðtÞ = W ij tðÞ/C1mj tðÞ : ð1Þ
Time-dependent MF-GC synaptic weights were modeled using
two ready-releasable vesicle pools 38, each according to the general
f o r me s t a b l i s h e db yT s o d y k sa n dM a r k r a m79. A similar model was
shown to accurately describe STP at the MF-GC synapse38. Accordingly,
one vesicle pool was comparatively small, with a high release prob-
ability and a low rate of recovery from vesicle depletion (0.5 s
−1), while
the other was comparatively large, with low release probability and a
high rate of recovery from depletion (20ms −1)38. We refer to these
pools as’slow’ and’fast’, respectively. In the Hallermann model 38,t h e
slow pool is re ﬁlled by vesicles from the fast pool. For the sake of
mathematical tractability, we modeled the pools as being re ﬁlled
independently (see scheme in Fig. 1).
To model vesicle depletion, we use the variables xslow and xfast,
denoting the fraction of neurotransmitter available at the slow and fast
vesicle pool. The state of the pools between GC i and MF j at time t is
then described by
_x
slow
ij ðtÞ =
1/C0 xslow
ij ðtÞ
τslow
ref
/C0 uslow
ij ðtÞ/C1ð1/C0 prefÞ/C1xslow
ij ðtÞ/C1mjðtÞ
_xfa s t
ij ðtÞ =
1/C0 xfa s t
ij ðtÞ
τfa s t
ref
/C0 ufa s t
ij ðtÞ/C1xfa s t
ij ðtÞ/C1mjðtÞ,
ð2Þ
where, τslow
ref and τfa s t
ref are the time constants of recovery from vesicle
depletion for the slow and fast pools, and are identical for all synapses.
The variables u
slow
ij ðtÞ and ufa s t
ij ðtÞ denote the pools’ respective release
probabilities at time t. Experimental data show that, in response to
trains of action potentials, MF-GC synapses approach synaptic steady-
state transmission with a long time constant
38,39. This feature can be
captured with a serial pool model38 (see scheme in Fig. S7). In order to
capture this behavior with a parallel pool model, we added the
phenomenological parameter pref to the slow pool ’s dynamical
equation. In mechanistic terms, pref can be thought of as the
probability of immediately reﬁlling a synaptic docking site after the
release of a vesicle. This mechanism effectively mimics a simpli ﬁed
form of activity-dependent recovery from depression. Theﬁnal release
probabilitiesuslow
ij ðtÞ and ufa s t
ij ðtÞ are modulated by synaptic facilitation
according to
_uslow
ij ðtÞ =
pα
v,slow/C0uslow
ij ðtÞ
τα
F
+ pα
v,slow/C1ð1/C0 uslow
ij ðtÞÞ/C1mjðtÞ
_ufa s t
ij ðtÞ =
pα
v,fa s t/C0ufa s t
ij ðtÞ
τα
F
+ pα
v,fa s t/C1ð1/C0 ufa s t
ij ðtÞÞ/C1mjðtÞ:
ð3Þ
Here, pα
v,fa s t and pα
v,slow denote the release probabilities for the fast
and slow pools, respectively, and τα
F is the facilitation time constant.
The index α denotes different synapse types (groups from Chabrol
et al.30) and varies from 1 to 5. The average number of vesicles released
at any time t can be written as:
nslow
ij ðtÞ = Nα
slow/C1uslow
ij ðtÞ/C1xslow
ij ðtÞ
nfa s t
ij ðtÞ = Nα
fa s t/C1ufa s t
ij ðtÞ/C1xfa s t
ij ðtÞ:
ð4Þ
Postsynaptic receptor desensitization induces an additional
component of depression of phasic MF-GC synaptic transmission. As
both pools share the same postsynaptic target, we model desensiti-
zation via the modulation of a single variable q
ijðtÞ for each synapse
type, which represents the synaptic quantal size and which is in ﬂu-
enced by the total number of vesicles released from both pools:
_qijðtÞ =
q0/C0qijðtÞ
τD
/C0 ΔD/C1qijðtÞ/C1
nslow
ij ðtÞ + nfa s t
ij ðtÞ
Ntot
/C1mjðtÞ ð5Þ
where Nα
tot = Nα
slow + Nα
fa s t, τD is the time constant of recovery from
desensitization,q0 is the quantal size in the absence of ongoing sti-
mulation and ΔD is a proportionality factor that determines the frac-
tional reduction of qijðtÞ. As explained below, we set q0 = 1, i.e. qij(t)i s
normalized. Both τD and ΔD are identical across all synapse types.
Finally, the total synaptic weight is equal to the sum of the contribu-
tions from both vesicle pools:
W
ijðtÞ = qijðtÞ/C1nslow
ij ðtÞ + nfa s t
ij ðtÞ
/C16/C17
, ð6Þ
Synaptic parameters for generating diverse synaptic strength
and dynamics
We set the synaptic parameters of our model to reproduce the average
behavior of the 5 MF-GC synapse groups which were determined in
ref. 30 based on unitary response current amplitudes, pair pulse ratios,
and response coefﬁcients of variation.
The vesicle pool reﬁlling time constantsτ
slow
ref and τfa s t
ref were set to
the values measured at the MF-GC synapse in ref.38 and were identical
for all synapse groups. The time constant of facilitationτα
F for groups
1–4w a st a k e nf r o mr e f .39. The time constant of recovery from
desensitization,τD, was set equal to the value reported in ref.38 for all
groups, and the parametersΔD w a sc h o s e ns oa st oo b t a i nt h er e l a t i v e
reduction in quantal size reported in the same ref.38.T oq u a l i t a t i v e l y
account for the slow approach to steady-state transmission observed
in MF-GC synapses
38,39 we set pref to a value of 0.6 for all synapse types.
To set the presynaptic quantal parameters, we matched model
quantal parameters,q0, N and pv, to the average of those measured in
ref. 30 for each synapse group. The estimation of the experimental
values qα
0, exp, Nα
exp and pα
v,e x p was carried out via multiple-probability
ﬂuctuation analysis30, which assumes a single vesicle pool. To con-
strain the corresponding parameters of our two-pool model, we
assumed:
N
α
exp = Nα
tot = Nα
slow + Nα
fa s t
pα
v,e x p=
Nα
slow pα
v,slow
+ Nα
fa s tpα
v,fa s t
Nα
tot
ð7Þ
while keepingpα
v,slow >pα
v,fa s t. Since the quantal size did not signiﬁcantly
differ between groups30,w es e t q0 = 1 for all groups for simplicity. As
group 4 featured almost no STP, we modeled these synapses without
slow pool.
The above equations do not have a unique solution. In order to
constrain the synaptic parameters further, we additionally required
that the relative unitary response current amplitudes between synapse
groups and their pair pulse ratios approximately equal the
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 11
experimentally measured ones. To account for the fact that group 5’s
pair pulse ratio is larger than one, we setτF = 30 ms for this group, as in
ref. 30.
Finally, we extracted the relative occurrence of each synapse type
from ref. 30.
A set of synaptic parameters that reproduces the behavior of the
ﬁve synapse groups from ref. 30 that we used in Figs. 1, 2,a n d 6 is
summarized in Table 1.
MF ﬁring rate parameters
MF ﬁring rate distributions of the full CCMSTP were set according to the
broad range described in the literature 40,41,70,72,73,80–84.M F sf o r m i n g
synapse types 1 and 2, which convey primary sensory information,
were set to high ﬁring frequencies according to experimental
observations40,41 (see Fig.1b, left panels). In contrast, theﬁring rates for
the other synapses types were lower70,83. For the full model, this led to
synapses with high pv being associated with MF inputs with com-
paratively higher averageﬁring rates (primary sensory groups 1, 2) and
synapses with low pv being associated with MF inputs with compara-
tively lower averageﬁring rates (secondary/processed sensory groups
3, 4, 5). We chose to describe MF ﬁring rate distributions by Gaussian
distributions whose negative tails were set to zero. Means and stan-
dard deviations of the Gaussian distributions were set such that the
means and standard deviations of the resulting thresholded distribu-
tions resulted in the values summarized in Table 2.
Cerebellar cortical circuit model
The standard cerebellar cortex model with STP (CCM STP)c o n s i s t so f
ﬁring rate units corresponding to 100 MFs, 3000 GCs, a single PC, and
a single molecular layer interneuron (MLI). The PC linearly sums
excitatory inputs from GCs and inhibition from the MLI. Each GC
receives four MF synapses, randomly selected from the different
synapse types according to their experimentally characterized fre-
quency of occurrence
30. The synaptic inputs to the GCs and theirﬁring
rates are given by:
Igc,iðtÞ =
X
j2K
Isyn,ijðtÞ =
X
j2K
W ijðtÞmjðtÞ
τg _gciðtÞ =/C0 gciðtÞ + αi/C1maxðIgc,iðtÞ/C0 θi,0Þ
ð8Þ
where the granule cell membrane time constantτg = 10ms. In the above
equation, K is a set of four indices, randomly drawn from all MF. We
require that at least one MF per GC belongs to groups 1, 2 or 5, as
observed experimentally
30.T h eg a i nαi and threshold θi are set indi-
vidually for each GC i as explained below.
MLI activity is assumed to represent the average rate of the GC
population, thus allowing each GC to have a net excitatory or inhibi-
tory effect depending on the difference between the MLI-PC inhibitory
weight and the respective GC-PC excitatory weight:
mliðtÞ =
1
N
XN
i =1
gci tðÞ , ð9Þ
The synaptic weights between theith GC and the PC and between
t h eM L Ia n dP Cw e r ed eﬁned as JE,i and JI , respectively. The total
synaptic input to the PC is thus given by
IpcðtÞ =
XN
i =1
JE,i
N gciðtÞ/C0 JI mliðtÞ + Ispont
= 1
N
XN
i =1
ðJE,i/C0 JIÞgciðtÞ + Ispont :
ð10Þ
Ispont is an input that maintains the spontaneous ﬁring of the PC
at 40 Hz.
Finally, the PC ﬁring rate is given by
pcðtÞ =m a xðIpcðtÞ,0Þ: ð11Þ
In Fig. 1, the GC-PC weights JE,i were drawn from an exponential
distribution with mean equal to 1. To decrease or increase the ratio of
the average excitatory to inhibitory weight, in Figs. 1ca n d 1dw es e t
J
I =1 :025 and JI =0 :975, respectively. The full CC model and the
reduced model (described below) were numerically integrated using
the Euler method with step size 0.5 ms.
GC Threshold and gain adjustment. Changing the statistics of the MF
ﬁring rate distributions changes the fraction of active GCs at any given
time and the average GCﬁring rates. To avoid the confounding impact
that co-varying these quantities has on learning performance when
comparing different MF parameter sets, we adjusted GC thresholds,θ
i
and gains αi such that, at steady state, the fraction of active GCs and
the average GCﬁring rates were identical for all MF parameter choices.
Speciﬁcally, we drew 1000 random MF patterns from the respective
ﬁring rate distributions, and we calculated the steady inputs values of
the synaptic dynamics as follows:
uslow,μ
ij
/C16/C17 *
= pα
v,slow/C1 1+ τα
F/C1mμ
1+ pα
v,slow/C1τα
F/C1mμ
j
ufa s t,μ
ij
/C16/C17 *
= pα
v,fa s t/C1 1+ τα
F/C1mμ
1+ pα
v,fa s t/C1τα
F/C1mμ
j
ð12Þ
xslow,μ
ij
/C16/C17 *
= 1
1+ uslow,μ
ij
/C16/C17 *
/C1τslow
ref /C11/C0 pref
/C16/C17
/C1mμ
j
xfa s t,μ
ij
/C16/C17 *
= 1
1+ ufa s t,μ
ij
/C16/C17 *
/C1τfa s t
ref /C1mμ
j
ð13Þ
qμ
ij
/C16/C17 *
= Ntot
Ntot + ΔD/C1τD/C1 nslow,μ
ij
/C16/C17 *
+ nfa s t,μ
ij
/C16/C17 *
/C18/C19
/C1mμ
j
ð14Þ
Table 1 | Synaptic parameters used in full model
Group 1 Group 2 Group 3 Group 4 Group 5 Ref.
Nslow 43 4 – 3 30
Nfast 16 12 6 10 12 30
pv,slow 0.9 0.8 0.4 – 0.4 30
pv,fast 0.72 0.55 0.35 0.3 0.15 30
τslow
ref [ms] 2000 2000 2000 – 2000 38
τfast
ref [ms] 20 20 20 20 20 38
τF [ms] 12 12 – 12 30 30,39
pref 0.6 0.6 0.6 – 0.6 –
ΔD 0.1 0.1 0.1 0.1 0.1 38
τD [ms] 100 100 100 100 100 38
occurrence 6% 16% 38% 24% 16% 30
Table 2 | MF ﬁring rate parameters used in the full model
Group 1 Group 2 Group 3 Group 4 Group 5
μ [Hz] 200 200 20 20 20
σ [Hz] 20 20 20 20 20
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 12
With these, we obtained, for each GC, the distribution of steady-
state inputs and ﬁring rates:
Iμ
gc,i
/C16/C17 *
=
X
j2K
W μ/C0/C1 *
ij mμ
j tðÞ
gcμ
i
/C0/C1 *
= αi/C1max Iμ
gc,i
/C16/C17 *
/C0 θi,0
/C18/C19 ð15Þ
We then adjusted αi and θi f o re a c hG Ct om a i n t a i na na v e r a g e
steady-state GCﬁring rate of 5 Hz for all patterns. The lifetime sparsity
of each GC was set to 0.2, which is within the range of experimental
observations84,85. Throughout the article, this adjustment was carried
out every time we changed synaptic parameters (Fig. 5), the para-
meters of the MF ﬁring rate distributions (Fig.4) or the MF to synapse
connectivity (Fig.5).
Supervised learning rule. Purkinje cell pauses associated with eyelid
conditioning acquisition were generated by adjusting JE,i using a
supervised learning rule. The target PCﬁring rate ItargetðtÞ was set as a
Dirac pulse in which the PC rate is zero in the time bin around ttarget
following the start of the CS.:
ItargetðtÞ = Ispont/C11/C0 St /C0 ttarget
/C16/C17hi
ð16Þ
where S = 1 in the time bin around ttarget and S =0 o t h e r w i s e . W e
quantify the deviation of the PC ﬁring rate from the target rate by the
least squares loss E that is to be minimized during learning:
E = 1
2
Z TCS
/C0Tpre
dtew2
errðtÞϵ2ðtÞ
= 1
2
Z TCS
/C0Tpre
dtew2
errðtÞ IpcðtÞ/C0 ItargetðtÞ
/C16/C17 2
ð17Þ
½0,TCS/C138is the time interval after CS onset (at t = 0) during which we
require the PC to follow the target signal and½/C0Tpre ,0/C138is a time interval
before CS onset during which the PC should ﬁre at its spontaneous
rate. ϵðtÞ denotes the deviation between the target and the actual PC
output at timet.ewerr is a factor that we use to increase the sensitivity of
the loss E function to the target time, and is given by:
ewerrðtÞ = werrðtÞ
R TCS
/C0Tpre
dt’werrðt’Þ
werrðtÞ = 3:5i f t = ttarget
1e l s e
/C26 ð18Þ
In all main ﬁgures, we used TCS =1 :4s and Tpre =0 :1s.
GC-PC weights JE,i were modiﬁed during learning using gradient
descent to reduce the error E at each step of the learning algorithm:
Ji Ji + ΔJi
ΔJi = η ∂E
∂Ji
= η
N
Z TCS
/C0Tpre
dtew2
errðtÞ/C1ϵðtÞ/C1gciðtÞ
ð19Þ
Here, η is a learning rate. For our simulations, we modi ﬁed this basic
rule in two ways. Firstly, similar to ref. 75, we explicitly simulated a
climbing ﬁber (CF) rate, cf, that is modulated by the error signal
ϵðtÞ = IpcðtÞ/C0 ItargetðtÞ according to
cfðtÞ =m a xðcf spont + βϵðtÞ,0Þ ð20Þ
where cf spont is the spontaneous CF rate andβ a proportionality factor.
The CF rate was then used to update the synaptic weight according to
the following equation:
ΔJ
i = η
N
Z TCS
/C0Tpre
d tew2
errðtÞ/C1ðcf spont/C0 cfðtÞÞ/C1gciðtÞ ð21Þ
where we also set JE,i = 0 when a learning iteration resulted in a nega-
tive weight. As the CF rate is required to be positive or zero, this
formulation limits the error information transmitted to the PC com-
pared to the simple gradient rule. This learning rule yields synaptic
long-term depression when CF and GC are simultaneously active and
long-term potentiation when GCs are active alone, consistent with
experimental data on GC-PC synaptic plasticity
59.
Furthermore, recent experimentalﬁndings suggest that the tem-
poral properties of GC-PC plasticity rules are tuned to compensate for
the typical delays expected for error information arriving in the cere-
bellar cortex
78. Here, we did not explicitly model CF error information
delays, and for the sake of simplicity, directly modeled the timing of PC
activity to show that the GC basis set is suf ﬁcient to generate an
appropriately timed PC pause.
To increase the learning speed, we added a Nesterov acceleration
scheme to Eq. ( 21)
86, introducing a momentum term to the gradient,
i.e. weight updates made during a given iteration of the algorithm
depended on the previous iteration. The implementation we chose
additionally features an adaptive reset of the momentum term,
improving convergence properties
86. This addition is for practical
convenience and does not reﬂect biological mechanisms.
For the weight learning, we subsampled the simulated GC rates by
a factor of 10 and set η = 0.0025, β =0 :5 and the initial distribution of
weights to JE,i = JI = 10 for all i. For all eyelid response learning simu-
lations, we chose cf spont =1 Hz (Figs. 2, 4, 5).
Error measure of learned Purkinje cell pause.W ed e ﬁned the error
between the PC pause and the Itarget (see Fig. 4, S3, S4 and S5) in the
following way:
ϵtot =1 /C0 ϵamp
hspont
 !
+ ϵf whm
s +5/C1ϵt
s ð22Þ
The ﬁrst term depends on the amplitude of the PC pause relative to
baselineﬁring, yielding a small error when the amplitude goes to zero.
The second term corresponds to the normalized width of the PC
pause. Finally, the third term is the normalized deviation of the pause’s
minimum from the target time, ϵt . To increase the importance of this
term, we scaled it by a factor 5. The error measure in Figs. S4 and S5 is
the sum of ϵ
tot over all tested delays.
Reduced CC model
T h er e d u c e ds y n a p t i cm o d e li n c l u d e do n l yt w os y n a p s et y p e s .W ea l s o
neglected facilitation and desensitization, yielding constant release
probabilities and constant normalized quantal size:
u
slow
ij ðtÞ = pα
v,slow
ufa s t
ij ðtÞ = pα
v,fa s t
qijðtÞ =1 :
ð23Þ
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 13
We obtain for the vesicle pool dynamics:
_xslow
ij ðtÞ =
1/C0 xslow
ij ðtÞ
τslow
ref
/C0 pα
v,slowð1/C0 prefÞxslow
ij ðtÞ/C1mjðtÞ
_xfa s t
ij ðtÞ =
1/C0 xfa s t
ij ðtÞ
τfa s t
ref
/C0 pα
v,fa s txfa s t
ij ðtÞ/C1mjðtÞ:
ð24Þ
and the total synaptic weight becomes
W ijðtÞ = Nα
slow/C1pα
v,slow/C1xslow
ij ðtÞ + Nα
fa s t/C1pα
v,fa s t/C1xfa s t
ij ðtÞ: ð25Þ
Here the index α denotes membership in the driver or supporter
category. The synaptic currents of the reduced model are computed as
in the full model. Each GC receives exactly two driver and two sup-
porter MF inputs with random and pairwise distinct identities. To
eliminate any non-synaptic dynamics from the reduced model, we
removed the GC membrane time constant yielding GC dynamics that
follow the synaptic input instantaneously:
gc
iðtÞ = αi/C1maxðIgc,iðtÞ/C0 θi,0Þ: ð26Þ
Finally, GC threshold and gain adjustments were carried out similarly
to the full CCMSTP where instead of Eqs. (12)a n d(14)w eu s e dE q .(23).
Synaptic parameters of the reduced model. The parameters of the
reduced model were set to create two synapse types that capture the
essence of the experimentally observed synaptic behavior: a strong
and fast driver synapse, and a weak and slow supporter synapse. All
synaptic parameters of the model used in Figs. 3, 4 and 6 are sum-
marized in Table 3.
In Fig. 5, ﬁring rates and release probabilities were randomly
drawn from uniform distributions. In detail, the release probabilities of
the slow pool, p
v,slow , were drawn from distributions with a lower and
upper bound of 0.1 and 0.9, respectively, (Fig.5a, d, g, and h), and the
corresponding release probabilities of the fast pool were calculated
according to p
v,fa s t = 2
3pv,slow , keeping them strictly lower. The lower
and upper bounds of the distribution of ﬁring rates used in panels a
and d were 5 Hz and 270 Hz, resulting inﬁring rate standard deviations
of σrate ≈38:2 Hz for the two-groups case (Fig.5a) and σrate ≈15:3H zf o r
the ﬁve groups case (Fig.5d). The bounds of the distributions in panels
g and h were chosen to match the average group ﬁring rates equal to
those in paneld and ﬁring rate standard deviations that increased with
the group index, i.e. σrate ≈f5:0,7:6,10:2,12:7,15:3g Hz for groups 1 to 5,
respectively. Finally, the sizes of the slow vesicle pool were ﬁxed at
Nslow = 4 and the size of the fast vesicle pools were set to decrease with
the group index, i.e. Nfa s t =f16,6g for the two-groups case, and
Nfa s t =f16,12,8,6,6g for the ﬁve groups case. Finally, the desired rank
correlation between pv identities and MF identities was achieved by
creating a Gaussian copula reﬂecting their statistical dependency and
reordering the marginalpv and MF distributions accordingly.
Derivation of τsyn and At
In the reduced model, we derived an analytical solution to the synaptic
current driving a GC in response to the CS. Since the equations
describing slow and fast vesicle pool dynamics are formally very
similar, we describe the derivation for a single slow pool only. Addi-
tionally, we suppress all indices for the sake of readability. We assume
that the MF rate mðtÞ switches instantaneously fromm
preCS to mCS at
time t’ = 0. Integration of equations (Eq. (24)) from t’ =0 t o t yields:
xðtÞ =ðx*
preCS/C0 x*
CSÞ exp /C0 1
τref
+ pvð1/C0 prefÞmCS
 !
t
 !
+ x*
CS , ð27Þ
Here, x*
preCS and x*
CS denote the steady-state values of x before (preCS)
and after (CS) the ﬁring rate switch. They are given by
x*
γ = 1
1+ αpvmγ
, ð28Þ
with
α =
τrefð1/C0 prefÞ for slow pool
τref for fast pool
(
ð29Þ
Equation ( 27)d e ﬁnes the synaptic time constant that governs the
speed of transition from a steady-state value before the CS to a steady-
state value during the CS:
τ
syn = τref /C1x*
CS = τref
1+ αpvmCS
ð30Þ
This equation is similar to one derived previously 55,87.T h et o t a l
synaptic current per unit time for a single pool during the CS is given
by
I
synðtÞ = NpvxðtÞmCS ð31Þ
Combining Eqs. (27)a n d (31) we obtain
IðtÞ = NpvmCS
1+ αpvmCS
1+ αpvðmCS/C0 mpreCSÞ
1+ αpvmpreCS
exp /C0 t
τsyn
 !"#
= As|{z}
steady state
+ At|{z}
transient amplitude
exp /C0 t
τsyn
 ! ð32Þ
Thus, the transient amplitude for a single vesicle pool is
At = NpvmCS
1+ αpvmCS
αpvðmCS/C0 mpreCSÞ
1+ αpvmpreCS
ð33Þ
For a single synapse, the total transient amplitude is the sum of the
individual fast pool and slow pool transients:
Atot
t = Aslow
t + Afa s t
t ð34Þ
To generate the surface plots in Fig. 4 and Fig S3 we generated 10 5
ﬁring rates from the driver and supporter MF rate distributions,
respectively, and used Equations ( 30), ( 33)a n d( 34) to calculate the
corresponding values of the At and τsyn . From these, the plots of the
joint At and τsyn distribution and the marginal distributions were
generated using a two- or one-dimensional kernel density estimator,
respectively88.N o t et h a t ,f o r m a l l y ,τsyn is maximal whenmCS =0 .I nt h a t
case, however, there is no synaptic transmission as
A
tot
t = Aslow
t = Afa s t
t = 0. When plotting the joint At -τsyn distribution in
Fig. 4 and Fig S3, we therefore omitted time constants and transient
amplitudes corresponding tomCS =0 .
Table 3 | Synaptic parameters used in reduced model
Drivers Supporters
Nslow 3.5 4
Nfast 14 6
pv,slow 0.8 0.4
pv,fast 0.6 0.2
τslow
ref [ms] 2000 2000
τfast
ref [ms] 20 20
pref 0.6 0.6
occurrence 50% 50%
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 14
Bayesian estimation of time intervals
To learn the mapping between tm and te, we presented CCMSTP with
variable intervals drawn from various prior distributions ( ts)s u b -
jected to measurement noise. The interval was introduced as a tonic
input to MFs, similar to the CS in the eyelid simulations. The onset of
this tonic input caused an abrupt switch of the MF input rates that
persisted over the course of a trial. For each iteration of our learning
algorithm, we generated target signals sampled randomly from one
of ﬁve different uniform prior distributions: 25 –150 ms, 50 –200 ms,
100–300 ms, 200 –400 ms, 300 –500 ms. Learning was carried out
separately for each interval and for 12000 iterations. We found that
to achieve the correct biases for the two longest intervals, we had to
introduce a higher CF baseline ﬁring rate, cf
spont = 5 Hz. The other
learning parameters were kept the same as in the eyelid learning
simulations.
In keeping with ref. 33, we modeled the DN neuron as an inte-
grator, whose rate was calculated according to
dntðÞ =
Z
I
ext/C0 JpcpcðtÞ
/C16/C17
dt, ð35Þ
where the Jpc is the weight of the inhibitory PC-DN synapse and
Iext = pc
/C10/C11
is an external excitatory input to DN. It was set equal to the
average PC ﬁring rate during the interval period to ensure that
excitation and inhibition onto the DN are of comparable size. For
simplicity, we set J
pc =1 .
In order to map the DN rate to a time axis (Fig. 6f, j), we rescaled
every individual DN output curve according to:
cdn tðÞ = ts,m a x/C0 ts,m i n
/C0/C1 dn tðÞ/C0 dnmin
dnmax/C0 dnmin
+ ts,m i n, ð36Þ
where ts,m a x and ts,m i n are the maximum and minimum of the
respective prior interval and dnmax and dnmin are the maximum and
minimum values of the DN ﬁring rate. Since the transformation
described in Eq. ( 36) is linear, the essential features exhibited by the
DN ﬁring rate (i.e. its biases) are preserved.
To show how the theoretical Bayesian least squares (BLS) interval
estimate can be obtained, we follow the reasoning from ref. 33.I ti s
assumed that to estimate a time-interval, ts, subjects perform a noisy
measurement,tm, according to:
pt m∣ts
/C0/C1
= 1ﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃ
2πðwweber tsÞ2
q e
/C0 ðts/C0tmÞ2
2ðwweber tsÞ2
: ð37Þ
Note that the standard deviation of the estimate of tm increases with
the length of the intervalts with proportionality factorwweber,w h i c hi s
the weber fraction. Given the prior distribution of time intervals,ΠðtsÞ,
t h eB a y e s i a ne s t i m a t eo fts given tm is:
pt s ∣tm
/C0/C1
/ Π ts
/C0/C1
pt m∣ts
/C0/C1
: ð38Þ
The BLS estimate is the expected value of the previous expression:
te = E½pt s ∣tm
/C0/C1
/C138: ð39Þ
We performed a least squares ﬁt of the BLS model to the CCM STP
outputs (from allﬁve interval distributions simultaneously) withwweber
as a single free parameter.
Recurrent Golgi cell inhibition
To probe the effect of recurrent inhibition in the reduced CCMSTP,w e
added one Golgi cell (GoC) that received excitatory inputs from all GCs
and formed inhibitory synapses onto all GCs. For simplicity, we
assumed that the GoC ﬁres with a rate goc equal to the average GC
ﬁring rate, similarly to the MLI, and that all GoC to GC synapses have
identical weights,Jgoc:
gocðtÞ = 1
N
XN
i =1
gciðtÞ =hgcðtÞi
Igc,iðtÞ =
X
j2K
W ijðtÞmjðtÞ/C0 Jgoc/C1gocðtÞ
gciðtÞ = αi/C1maxðIgc,iðtÞ/C0 θi,0Þ:
ð40Þ
The above equations imply that, in this conﬁguration, the GoC acts as
an activity-dependent GC threshold.
To ensure that the overall GC activity level in the reduced
CCMSTP with GoC inhibition is comparable to the case without, we
require the same criterion as above: an average GC rate of 5 Hz and a
fraction of activated GCs of 0.2 in steady state. Since the average GC
input now depends on the average GC ﬁring rate itself, manual
adjustment of GC thresholds,θ
i, and gains, αi, carried out as above, is
not feasible.
Instead, a steady-state solution of the set of Eq. (40) satisfying our
requirements has to be found numerically. We ﬁrst set up the CC
network without the GoC and adjusted GC thresholds,θi,a n dg a i n s ,αi,
according to the procedure described above. Note that in the reduced
model, due to every GC receiving the same combination of inputs (i.e.
2 supporter and two driver inputs), both θ
i and αi are similar across
GCs. We thus made the additional simpliﬁcation of settingθ =EðθiÞ and
α =EðαiÞ for all GCs. We then reduced GC thresholds by 10% and
introduced the GoC.
To obtain the average steady-state GCﬁring rate we assumed that
the synaptic currents of a single GC are normally distributed across MF
input patterns or, equivalently, across GCs. Mean and variance of the
GC inputs are:
I
*
gc
DE
=E I*
gc,i
/C16/C17
=E
X
j2K
W *
ij/C1mj
 !
/C0 Jgoc/C1gc*/C10/C11
σ2
I* =V a r I*
gc,i
/C16/C17
=V a r
X
j2K
W *
ij/C1mj
 ! ð41Þ
W ec a nt h e ne x p r e s st h ea v e r a g eG Cﬁring rate in the N!1 limit as:
hgc*i = α
Z +1
/C01
max I*
gc
DE
+ σ*
I/C1ξ/C0 ~θ,0
/C16/C17
exp /C0 ξ2
2
 !
dξﬃﬃﬃﬃﬃﬃ
2π
p ð42Þ
whereeθ =0 :9θ. The fraction of active GCs f can be written as:
f = 1
2 erfc
θ/C0 I*
gc
DE
ﬃﬃﬃ
2
p
σI*
0
@
1
A ð43Þ
We can now impose that
gc*/C10/C11
=5 H z
f =0 :2 ð44Þ
and ﬁnd a self-consistent solution of Eqs. (41), (42), and (43) by adjusting
the parametersJgoc and α. To do so we used the hybrid numerical root-
ﬁnder from the GNU scientiﬁc library89 with default step size.
Reporting summary
Further information on research design is available in the Nature
Portfolio Reporting Summary linked to this article.
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 15
Data availability
No experimental data were generated in this study.
Code availability
Figures were generated with Matlab (R2019b) and python (3.8). All
simulations were performed with C++11 using the GNU scientiﬁcl i b r a r y
(2.6)89 and the armadillo library (11.0.1)90. The code is available on the
following GitHub repository: https://github.com/alessandrobarri/
cerebellar_cortex_input_STP.
References
1. Broome, B. M., Jayaraman, V. & Laurent, G. Encoding and decoding
of overlapping odor sequences.Neuron 51,4 6 7–482 (2006).
2. Crowe, D. A., Averbeck, B. B., Chafee, M. V. & Georgopoulos, A. P.
Dynamics of parietal neural activity during spatial cognitive pro-
cessing. Neuron 47,8 8 5–891 (2005).
3 . H a r v e y ,C .D . ,C o e n ,P .&T a n k ,D .W .C h o i c e - s p e c iﬁcs e q u e n c e si n
parietal cortex during a virtual-navigation decision task.Nature484,
62–68 (2012).
4. Sauerbrei, B. A. et al. Cortical pattern generation during dexterous
movement is input-driven.Nature 577,3 8 6–391 (2020).
5. Zhou, S., Masmanidis, S. C. & Buonomano, D. V. Neural sequences
as an optimal dynamical regime for the readout of time. Neuron
108,6 5 1–658.e5 (2020).
6. Bright, I. M. et al. A temporal record of the past with a spectrum of
time constants in the monkey entorhinal cortex.Proc. Natl Acad.
Sci. 117,2 0 2 7 4–20283 (2020).
7. MacDonald, C. J., Lepage, K. Q., Eden, U. T. & Eichenbaum, H.
Hippocampal“time cells” bridge the gap in memory for dis-
contiguous events.Neuron 71,7 3 7–749 (2011).
8. Pastalkova, E., Itskov, V., Amarasingham, A. & Buzsaki, G. Internally
generated cell assembly sequences in the rat hippocampus.Sci-
ence 321,1 3 2 2–1327 (2008).
9 . L o n g ,M .A . ,J i n ,D .Z .&F e e ,M .S .S u p p o r tf o ras y n a p t i cc h a i nm o d e l
of neuronal sequence generation.Nature 468,3 9 4–399 (2010).
10. Kennedy, A. et al. A temporal basis for predicting the sensory
consequences of motor commands in an electricﬁsh. Nat. Neu-
rosci. 17,4 1 6–422 (2014).
11. Laje, R. & Buonomano, D. V. Robust timing and motor patterns by
taming chaos in recurrent neural networks.Nat. Neurosci. 16,
925–933 (2013).
12. Yamazaki, T. & Tanaka, S. The cerebellum as a liquid state machine.
Neural Netw. 20,2 9 0–297 (2007).
13. Toyoizumi, T. & Abbott, L. F. Beyond the edge of chaos: ampli ﬁca-
tion and temporal integration by recurrent networks in the chaotic
regime. P h y s .R e v .E :S t a t .N o n l i n .S o f tM a t t e rP h y s .84,
051908 (2011).
14. Dittman, J. S., Kreitzer, A. C. & Regehr, W. G. Interplay between
facilitation, depression, and residual calcium at three presynaptic
terminals. J. Neurosci. 20,1 3 7 4–1385 (2000).
1 5 . A b b o t t ,L .F .&R e g e h r ,W .G .S y n a p t i cc o m p u t a t i o n .Nature 431,
796–803 (2004).
16. Abbott, L. F., Varela, J. A., Sen, K. & Nelson, S. B. Synaptic depres-
sion and cortical gain control. Science 275, 220–224 (1997).
1 7 . R o t h m a n ,J .S . ,C a t h a l a ,L . ,S t e u b e r ,V .&S i l v e r ,R .A .S y n a p t i c
depression enables neuronal gain control.Nature 457,
1015–1018 (2009).
18. Buonomano, D. V. & Merzenich, M. M. Temporal information trans-
formed into a spatial code by a neural network with realistic prop-
erties. Science 267,1 0 2 8–1030 (1995).
19. Mongillo, G., Barak, O. & Tsodyks, M. Synaptic theory of working
memory. Science 319,1 5 4 3–1546 (2008).
20. Buonomano, D. V. & Maass, W. State-dependent computations:
spatiotemporal processing in cortical networks.Nat. Rev. Neurosci.
10,1 1 3–125 (2009).
21. Chadderton, P., Schaefer, A. T., Williams, S. R. & Margrie, T. W.
Sensory-evoked synaptic integration in cerebellar and cerebral
cortical neurons.Nat. Rev. Neurosci. 15,7 1–83 (2014).
22. Popa, L. S., Hewitt, A. L. & Ebner, T. J. Predictive and Feedback
Performance Errors Are Signaled in the Simple Spike Discharge of
Individual Purkinje Cells.J. Neurosci. 32,1 5 3 4 5–15358 (2012).
23. Burguière, E. et al. Spatial navigation impairment in mice lacking
cerebellar LTD: a motor adaptation deﬁcit? Nat. Neurosci. 8,
1292–1294 (2005).
24. Moberget, T., Gullesen, E. H., Andersson, S., Ivry, R. B. & Endestad,
T. Generalized role for the cerebellum in encoding internal models:
evidence from semantic processing.J. Neurosci. 34,
2871–2878 (2014).
25. Gao, Z. et al. A cortico-cerebellar loop for motor planning. Nature
563, 113
–116 (2018).
2 6 . C h a b r o l ,F .P . ,B l o t ,A .&M r s i c - F l o g e l ,T .D .C e r e b e l l a rc o n t r i b u t i o n
to preparatory activity in motor neocortex.Neuron 103,
506–519.e4 (2019).
27. Marr, D. A theory of cerebellar cortex. J. Physiol. 202,
437–470 (1968).
28. Albus, J. S. A theory of cerebellar function. Math. Biosci. 10,
25–61 (1971).
29. Medina, J. F. & Mauk, M. D. Computer simulation of cerebellar
information processing.Nat. Neurosci. 3,1 2 0 5–1211 (2000).
3 0 . C h a b r o l ,F .P . ,A r e n z ,A . ,W i e c h e r t ,M .T . ,M a r g r i e ,T .W .&D i G r e -
gorio, D. A. Synaptic diversity enables temporal coding of coin-
cident multisensory inputs in single neurons.Nat. Neurosci. 18,
718–727 (2015).
3 1 . H a l v e r s o n ,H .E . ,K h i l k e v i c h ,A .&M a u k ,M .D .R e l a t i n gc e r e b e l l a r
Purkinje cell activity to the timing and amplitude of conditioned
eyelid responses.J. Neurosci. 35,7 8 1 3–7832 (2015).
32. White, N. E., Kehoe, E. J., Choi, J. S. & Moore, J. W. Coef ﬁcients of
variation in timing of the classically conditioned eyeblink in rabbits.
Psychobiology28,5 2 0–524 (2000).
33. Narain, D., Remington, E. D., Zeeuw, C. I. D. & Jazayeri, M. A cere-
bellar mechanism for learning prior distributions of time intervals.
Nat. Commun. 9, 469 (2018).
34. Litwin-Kumar, A., Harris, K. D., Axel, R., Sompolinsky, H. & Abbott, L.
F. Optimal degrees of synaptic connectivity.Neuron 93,
153–1164.e7 (2017).
35. Cayco-Gajic, N. A., Clopath, C. & Silver, R. A. Sparse synaptic con-
nectivity is required for decorrelation and pattern separation in
feedforward networks.Nat. Commun. 8, 1116 (2017).
36. Fujita, M. Adaptive ﬁlter model of the cerebellum.Biol. Cybern.45,
195–206 (1982).
37. Dean, P., Porrill, J., Ekerot, C .-F. & Jörntell, H. The cerebellar
microcircuit as an adaptiveﬁlter: experimental and computational
evidence. Nat. Rev. Neurosci. 11,3 0–43 (2010).
38. Hallermann, S. et al. Bassoon sp eeds vesicle reloading at a central
excitatory synapse.Neuron 68
,7 1 0–723 (2010).
39. Saviane, C. & Silver, R. A. Fast vesicle reloading and a large pool
sustain high bandwidth transmission at a central synapse.Nature
439,9 8 3–987 (2006).
4 0 . P a r k ,H .J . ,L a s k e r ,D .M .&M i n o r ,L .B .S t a t i ca n dd y n a m i cd i s c h a r g e
properties of vestibular-nerve afferents in the mouse are affected
by core body temperature. Exp. Brain Res. 200,2 6 9–275 (2010).
4 1 . A r e n z ,A . ,S i l v e r ,R .A . ,S c h a e f e r ,A .T .&M a r g r i e ,T .W .T h ec o n -
tribution of single synapses to sensory representation in vivo.Sci-
ence 321,9 7 7–980 (2008).
42. Bosman, L. W. J. et al. Encoding of whisker input by cerebellar
Purkinje cells: Whisker encoding by Purkinje cells.J. Physiol. 588,
3757–3783 (2010).
4 3 . O h m a e ,S .&M e d i n a ,J .F .C l i m b i n gﬁbers encode a temporal-
difference prediction error during cerebellar learning in mice.Nat.
Neurosci. 18,1 7 9 8–1803 (2015).
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 16
44. Steinmetz, J. E., Lavond, D. G. & Thompson, R. F. Classical con-
ditioning of the rabbit eyelid response with mossyﬁber stimulation
as the conditioned stimulus.Bull. Psychon. Soc. 23,2 4 5–248
(1985).
45. Khilkevich, A., Zambrano, J., Richards, M.-M. & Mauk, M. D. Cere-
bellar implementation of movement sequences through feedback.
eLife 7,e 0 6 2 6 2( 2 0 1 8 ) .
46. Bouvier, G. et al. Cerebellar learning using perturbations. eLife
45,( 2 0 1 8 ) .
47. Gibbon, J. Scalar expectancy theory and Weber ’s law in animal
timing. Psychol. Rev. 84,4 7( 1 9 7 7 ) .
48. Jazayeri, M. & Shadlen, M. N. Tem poral context calibrates interval
timing. Nat. Neurosci. 13,1 0 2 0–1026 (2010).
49. Miyazaki, M., Nozaki, D. & Nakaj ima, Y. Testing Bayesian models of
human coincidence timing.J. Neurophysiol.94,3 9 5–399
(2005).
50. Egger, S. W., Remington, E. D., Chang, C.-J. & Jazayeri, M. Internal
models of sensorimotor integration regulate cortical dynamics.Nat.
Neurosci. 22,1 8 7 1–1882 (2019).
51. Marr, D. Vision: A Computational Investigation Into the Human
Representation and Processing of Visual Information (MIT
Press, 1982).
5 2 . S h a n k a r ,K .H .&H o w a r d ,M .W .As c a l e - i n v a r i a n ti n t e r n a lr e p r e -
sentation of time. Neural Comput 24,1 3 4–193 (2012).
5 3 . A l b e r g a r i a ,C . ,S i l v a ,N .T . ,P r i t c h e t t ,D .L .&C a r e y ,M .R .L o c o m o t o r
activity modulates associative learning in mouse cerebellum.Nat.
Neurosci. 21,7 2 5–735 (2018).
54. Guo, J.-Z. et al. Disrupting cortico-cerebellar communication
impairs dexterity.eLife 10, e65906 (2021).
55. Puccini, G. D., Sanchez-Vives, M. V. & Compte, A. Integrated
mechanisms of anticipation and rate-of-change computations in
cortical circuits.PLoS Comput. Biol. 3,e 8 2( 2 0 0 7 ) .
56. Wang, Y. et al. Heterogeneity in the pyramidal network of the medial
prefrontal cortex.Nat. Neurosci. 9,5 3 4–542 (2006).
57. Diaz-Quesada, M., Martini, F. J., Ferrati, G., Bureau, I. & Maravall, M.
Diverse thalamocortical short-term plasticity elicited by ongoing
stimulation.J. Neurosci. 34,5 1 5–526 (2014).
58. Buzsáki, G. & Mizuseki, K. The log-dynamic brain: how skewed dis-
tributions affect network operations.Nat. Rev. Neurosci. 15,
264–278 (2014).
5 9 . G a o ,Z .&v a nB e u g e n ,B .J .&D eZ e e u w ,C .I .D i s t r i b u t e ds y n e r g i s t i c
plasticity and cerebellar learning.Nat. Rev. Neurosci. 13,
619–635 (2012).
60. Gilmer, J. I., Farries, M. A., Kilpatrick, Z., Delis, I. & Person, A. L.
An Emergent Temporal Basis Set Robustly Supports Cerebellar
Time-series Learning . https://doi.org/10.1101/2022.01.06.
475265 (2022).
61. Zampini, V. et al. Mechanisms and functional roles of glutamatergic
synapse diversity in a cerebellar circuit.eLife 5,e 1 5 8 7 2( 2 0 1 6 ) .
62. Guo, C., Huson, V., Macosko, E. Z. & Regehr, W. G. Graded het-
erogeneity of metabotropic signaling underlies a continuum of cell-
intrinsic temporal responses in unipolar brush cells.Nat. Commun.
12, 5491 (2021).
63. Dorgans, K. et al. Short-term plas ticity at cerebellar granule cell to
molecular layer interneuron synapses expands information pro-
cessing. eLife 8,e 4 1 5 8 6( 2 0 1 9 ) .
64. Gurnani, H. & Silver, R. A. Multidimensional population activity in an
electrically coupled inhibitory circuit in the cerebellar cortex.
Neuron 109,1 7 3 9–1753.e8 (2021).
65. Kita, K. et al. GluA4 enables associative memory formation by
facilitating cerebellar expansion coding.bioRxiv https://doi.org/10.
1101/2020.12.04.412023(2020).
66. DiGregorio, D. A., Nusser, Z. & Silver, R. A. Spillover of glutamate
onto synaptic AMPA receptors enhances fast transmission at a
cerebellar synapse.Neuron 35,5 2 1–533 (2002).
67. Yamazaki, T. & Tanaka, S. A spiking network model for passage-of-
time representation in the cerebellum: Cerebellar passage-of-time
representation.Eur. J. Neurosci. 26, 2279–2292 (2007).
68. Straub, I. et al. Gradients in the mammalian cerebellar cortex
enable Fourier-like transformation and improve storing capacity.
eLife 9,e 5 1 7 7 1( 2 0 2 0 ) .
69. Johansson, F., Jirenhed, D.-A., Rasmussen, A., Zucca, R. & Hesslow,
G. Memory trace and timing mechanism localized to cerebellar
Purkinje cells. Proc. Natl Acad. Sci. 111, 14930–14934 (2014).
70. Van Dijck, G. et al. Probabilistic identi ﬁcation of cerebellar cortical
neurones across species.PLoS ONE 8, e57669 (2013).
71. Liu, Z. et al. Sustained deep-tissue voltage recording using a fast
indicator evolved for two-photon microscopy.Cell 185,4 8
(2022).
72. Sadeghi, S. G., Chacron, M. J., Taylor, M. C. & Cullen, K. E. Neural
variability, detection thresholds, and information transmission in
the vestibular system.J. Neurosci. 27,7 7 1–781 (2007).
73. Medrea, I. & Cullen, K. E. Multisensory integration in early vestibular
processing in mice: the encoding of passive vs. active motion.J.
Neurophysiol.110,2 7 0 4–2717 (2013).
74. Bengtsson, F. & Jorntell, H. Sensory transmission in cerebellar
granule cells relies on similarly coded mossyﬁber inputs.Proc. Natl
Acad. Sci. 106,2 3 8 9–2394 (2009).
75. Clopath, C., Badura, A., De Zeeuw, C. I. & Brunel, N. A Cerebellar
learning model of vestibulo-ocular reﬂex adaptation in wild-type
and mutant mice. J. Neurosci. 34,7 2 0 3–7215 (2014).
76. Naja ﬁ,F .&M e d i n a ,J .F .B e y o n d“all-or-nothing” climbing ﬁbers:
graded representation of teaching signals in Purkinje cells.Front.
Neural Circuits 7, 115 (2013).
77. Remington, E. D., Narain, D., Hosseini, E. A. & Jazayeri, M. Flexible
sensorimotor computations through rapid reconﬁguration of cor-
tical dynamics. Neuron 98,1 0 0 5–1019.e5 (2018).
78. Suvrathan, A., Payne, H. L. & Raymond, J. L. Timing rules for synaptic
plasticity matched to behavioral function.Neuron 92,
959–967 (2016).
7 9 . M a r k r a m ,H . ,W a n g ,Y .&T s o d y k s ,M. Differential signaling via the
same axon of neocortical pyramidal neurons.Proc. Natl Acad. Sci.
95,5 3 2 3–5328 (1998).
80. Van Kan, P. L., Gibson, A. R. & Houk, J. C. Movement-related inputs
to intermediate cerebellum of the monkey.J. Neurophysiol.69,
74–94 (1993).
81. Beraneck, M. & Cullen, K. E. Acti vity of vestibular nuclei neurons
during vestibular and optokinetic stimulation in the alert mouse.J.
Neurophysiol.98,1 5 4 9–1565 (2007).
82. Dale, A. & Cullen, K. E. The nucleus prepositus predominantly out-
puts eye movement-related information during passive and active
self-motion.J. Neurophysiol.109,1 9 0 0–1911 (2013).
83. Muzzu, T., Mitolo, S., Gava, G. P. & Schultz, S. R. Encoding of
locomotion kinematics inthe mouse cerebellum.PLoS ONE 13,
e0203900 (2018).
84. Chen, S., Augustine, G. J. & Chadderton, P. Serial processing of
kinematic signals by cerebellar circuitry during voluntary whisking.
Nat. Commun. 8
, 232 (2017).
85. Giovannucci, A. et al. Cerebellar granule cells acquire a widespread
predictive feedback signal during motor learning.Nat. Neurosci.
20,7 2 7–734 (2017).
86. O ’Donoghue, B. & Candes, E. Adaptive restart for accelerated gra-
dient schemes. Found. Comput. Math. 15,7 1 5–732 (2015).
87. Goldman, M. S., Maldonado, P. & Abbott, L. F. Redundancy reduc-
tion and sustained ﬁring with stochastic depressing synapses.J.
Neurosci. 22,5 8 4–591 (2002).
88. Botev, Z. I., Grotowski, J. F. & Kroese, D. P. Kernel density estimation
via diffusion. Ann. Stat. 38,2 9 1 6–2957 (2010).
8 9 . G a l a s s i ,M .&T h e i l e r ,J .G N US c i e n t iﬁc Library Reference Manual.
3rd edn.
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 17
90. Sanderson, C. & Curtin, R. Armadillo: a template-based C++ library
f o rl i n e a ra l g e b r a .J. Open Source Softw. 1,2 6( 2 0 1 6 ) .
Acknowledgements
A.B. thanks Gianluigi Mongillo and Zuzanna Piwkowska Zvonkine for
helpful discussions. We thank the DiGregorio Lab for feedback on this
manuscript. This work is supported by the Institut Pasteur, Centre
National de la Recherche Scientiﬁque, Fondation pour la Recherche
Médicale (FRM EQU202003010555), Fondation pour l’Audition (FPA-RD-
2018-8), BioPsy Laboratory of Excellence, and the Agence Nationale de
la Recherche (ANR-17-CE16-0019, and ANR-18-CE16-0018, ANR-19-CE16
0019-02, ANR-21-CE16-0036-01), which were awarded to the labora-
tory of DAD.
Author contributions
All simulations and analyses were performed by A.B. A.B., M.W., M.J.,
and D.A.D. conceived the project and wrote the manuscript.
Competing interests
The authors declare no competing interests.
Additional information
Supplementary informationThe online version contains
supplementary material available at
https://doi.org/10.1038/s41467-022-35395-y.
Correspondenceand requests for materials should be addressed to
A. Barri or D. A. DiGregorio.
Peer review informationNature Communicationsthanks the anon-
ymous reviewer(s) for their contribution to the peer review of this work.
Peer reviewer reports are available.
Reprints and permissions informationis available at
http://www.nature.com/reprints
Publisher’s note Springer Nature remains neutral with regard to jur-
isdictional claims in published maps and institutional afﬁliations.
Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as
long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license, and indicate if
changes were made. The images or other third party material in this
article are included in the article’s Creative Commons license, unless
indicated otherwise in a credit line to the material. If material is not
included in the article’s Creative Commons license and your intended
use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright
holder. To view a copy of this license, visithttp://creativecommons.org/
licenses/by/4.0/.
© The Author(s) 2022
Article https://doi.org/10.1038/s41467-022-35395-y
Nature Communications|         (2022) 13:7902 18
