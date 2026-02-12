# neural-oscillations-in-the-fronto-striatal-network

RESEA RCH ARTICL E
Neural oscillations in the fronto-striatal
network predict vocal output in bats
Kristin Weineck
ID
1,2
*, Francisco Garcı ´ a-Rosales
ID
1
, Julio C. Hechavarrı ´ a
ID
1
*
1 Auditory Comp utations lab, Institute for Cell Biology and Neurosc ience, Goethe University , Frankfurt am
Main, Germany, 2 Research Group Neural and Environm ental Rhythms, MPI for Empirical Aesthetics,
Frankfur t, Germany
* k.wein eck@hotm ail.de (KW); hechavar ria@bio.uni- frankfurt .de (JCH)
Abstract
The ability to vocalize is ubiquitous in vertebrates, but neural networks underlying vocal con-
trol remain poorly understood. Here, we performed simultaneous neuronal recordings in the
frontal cortex and dorsal striatum (caudate nucleus, CN) during the production of echoloca-
tion pulses and communication calls in bats. This approach allowed us to assess the general
aspects underlying vocal production in mammals and the unique evolutionary adaptations
of bat echolocation. Our data indicate that before vocalization, a distinctive change in high-
gamma and beta oscillations (50–80 Hz and 12–30 Hz, respectively) takes place in the bat
frontal cortex and dorsal striatum. Such precise fine-tuning of neural oscillations could allow
animals to selectively activate motor programs required for the production of either echolo-
cation or communication vocalizations. Moreover, the functional coupling between frontal
and striatal areas, occurring in the theta oscillatory band (4–8 Hz), differs markedly at the
millisecond level, depending on whether the animals are in a navigational mode (that is,
emitting echolocation pulses) or in a social communication mode (emitting communication
calls). Overall, this study indicates that fronto-stria tal oscillations could provide a neural cor-
relate for vocal control in bats.
Introduction
Vocalization-based interactions between broadcaster and receiver play an important role in
everyday life scenarios and are highly conserved throughout the animal kingdom [1,2]. Yet,
the neural circuits involved in vocal production have not been clearly delineated. Cortico-stria-
tal networks have been identified as candidate circuits determining vocal output in mammals.
Rhythmic neural activity (also known as oscillations) in striatal structures such as the caudate,
putamen, and nucleus accumbens has been linked to speech production in healthy humans, to
disorders such as stuttering [3], and to diseases that involve speech impairments such as Par-
kinson disease and Tourette syndrome [4–6]. Yet, to date, it remains largely discussed how
(and if) oscillations in neural networks involving the striatum participate in the precise control
of vocal motor outputs in humans and other vertebrate species.
In this article, we studied neural activity in the dorsal striatum (caudate nucleus, CN) and
frontal cortex during vocalization in bats. We chose to study the fronto-striatal circuit because
PLOS BIOL OGY
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 1 / 29
a1111111111
a1111111111
a1111111111
a1111111111
a1111111111
OPEN ACCESS
Citation: Weineck K, Garcı ´ a-Rosal es F, Hechavar rı ´ a
JC (2020) Neural oscillations in the fronto-s triatal
network predict vocal output in bats. PLoS Biol 18
(3): e3000658. https://do i.org/10.1371/j ournal.
pbio.30006 58
Academic Editor: Manuel S. Malmierca ,
Universida d de Salamanca, SPAIN
Received: September 6, 2019
Accepted: February 13, 2020
Published: March 19, 2020
Peer Review History: PLOS recognize s the
benefits of transpar ency in the peer review
process; therefore, we enable the publication of
all of the content of peer review and author
response s alongside final, published articles. The
editorial history of this article is available here:
https://doi.o rg/10.1371/jo urnal.pbio.3 000658
Copyright: © 2020 Weineck et al. This is an open
access article distributed under the terms of the
Creative Commons Attribution License, which
permits unrestricte d use, distribu tion, and
reproduction in any medium, provided the original
author and source are credited.
Data Availabilit y Statement: Data used in the
manuscript to correlate brain signals to vocal
production in bats are freely accessible online from
the g-node database (https://do i.org/10.12751 /g-
node.6a0d 94).
there is strong evidence suggesting a role of this network in vocal production across vertebrate
species. Fronto-striatal networks connect different parts of the frontal lobe with various
regions of the striatum, which constitute a major input structure into the basal ganglia [7,8].
Using tractographic methods, a direct connection between the CN and the prefrontal cortex
has been identified in humans and other mammals [9–12]. Both brain regions are highly con-
nected to brain areas of the canonical vocal motor pathway. For example, in primates, the CN
receives inputs from the laryngeal motor cortex [13,14]. It is also known that the frontal cortex
is connected to structures participating in vocal control, such as the periaqueductal gray in the
brainstem [15]. Moreover, studies examining the function of frontal and striatal regions have
identified their putative role in vocalization in humans [16–18] and bats [19,20]. Likewise, in
songbirds, Area X (the bird striatum) appears to be involved in vocal learning and in modulat-
ing song production in adult animals [21]. Together these studies support the involvement of
frontal and striatal areas in mediating and predicting vocal output across vertebrate species.
To assess the neural dynamics during vocalization, we recorded local field potentials (LFPs)
and spiking activity during the production of echolocation pulses and communication calls in
bats. LFPs reflect the sum of synaptic activity in neuronal populations and slow spike compo-
nents, and they represent a correlate of signals obtained with noninvasive techniques such as
electroencephalography [22]. We focused on investigating synchronized neural oscillations
occurring in the LFPs before and after vocal production. Oscillations are thought to enable
communication between neural populations and, at least in humans and birds, they are known
to be related to vocal production [23–25].
Neural oscillations can be split into different frequency bands comprising delta (1–3 Hz),
theta (4–8 Hz), alpha (8–12 Hz), beta (12–30 Hz), and gamma (30–80 Hz). Empirical evidence
indicates that LFP oscillations with different frequencies correlate well with distinct neural
computations, motor control, and cognitive states [26]. In particular, low frequencies such as
theta and alpha are known to modulate sensory processing, action selection and neuronal
excitability; are implicated in cognitive control; and are involved in long-range synchrony
facilitating, e.g., top-down processing [27–32]. Beta band oscillations potentially hold func-
tions in perception, memory, and sensory processing [33–35]; are linked to motor actions in
the motor cortex and striatum [36,37]; and are dysregulated in disorders such as Parkinson
disease [6,38]. Gamma rhythms can be linked to selective attention, (local) neural computa-
tion, and motor control [25,27,39] and are correlated with vocalization production [24,40]. In
humans, distinct oscillatory patterns and coherence across frequency bands have been found
during speech production and singing [41,42].
We studied neural oscillatory activity during vocal production in bats of the species Carollia
perspicillata. This bat species belongs to the suborder Microchiroptera, which are characterized
by laryngeal echolocation, similar to human laryngeal-based speech production [43]. As bats
heavily depend on their ability to vocalize in order to communicate and orient in the environ-
ment, they serve as a good animal model for studying the neural underpinnings of hearing and
vocal production. Bat calls can be broadly split into two types of outputs, including echoloca-
tion pulses and communication calls such as distress and social calls (here classified as echolo-
cation pulses versus communication calls) [44,45]. At the level of the brainstem, it is has been
demonstrated that the two types of vocal outputs are distinctly controlled [46,47]. However,
whether differences exist in the neural activity patterns leading to the production of both types
of vocal outputs on a cortical/cortico-striatal level in bats is unknown. So far, only a very lim-
ited number of experiments were able to obtain electrophysiological recordings from vocaliz-
ing bats [48–51], even though the brain of these animals has been studied for over 50 years.
In bats, an elevated c-fos immunoreactivi ty was found in the CN of the striatum when com-
paring vocally active with silent animals [19]. However, the striatal neural activity patterns
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 2 / 29
Funding: The project was conducte d with funds
provided by the German Research Foundation
(DFG) to JCH (grant #275755787 ). The funders
had no role in study design, data collecti on and
analysis, decision to publish, or prepara tion of the
manuscript.
Competing interests : The authors have declared
that no competing interests exist.
Abbreviati ons: CN, caudate nucleus; dVS,
difference in vector strength; FAF, frontal auditory
field; IQR, interquart ile range; LF, low-frequen cy;
LFP, local field potential; LHF, low- and high-
frequency; PIN, pyramidal-inte rneuron; PING,
pyramidal-inte rneuron gamma; PSTH, peri-
stimulus time histogram ; SPL, sound pressure
level; SVM, support vector machine ; VS, vector
strength.
related to vocal production remain unknown. The bat frontal lobe is also a rather unexplored
region. Most previous experiments in bat frontal areas evaluated the auditory responsiveness
of the frontal cortex and defined the frontal auditory field (FAF) [52–54]. It remains contro-
versial whether the FAF is an analogue to the prefrontal areas found in other mammals based
on morphology and connectivity [55,56]. This work will refer to the FAF when discussing the
recordings from the bats’ frontal lobe.
We hypothesized that the production of echolocation pulses and communication calls in
bats could involve different fronto-striatal oscillatory dynamics. Echolocation and communi-
cation sounds have different purposes: the former are used to create an acoustic image of the
environment (which depends on listening to echoes of the calls emitted), while the latter are
uttered to convey information to other individuals. As neural oscillations have been demon-
strated to be involved in a multitude of tasks (see above) and are altered in movement/speech
disorders, we thought they could provide a neural correlate of vocal production. Our results
show that fronto-striatal oscillations can be used to predict vocal output in bats. Vocal produc-
tion correlates well with distinct inter-areal coupling in the theta band and specialized intra-
areal processing mechanisms in the gamma and beta bands of LFPs. Taken together, our
results present correlative evidence for the involvement of fronto-striatal circuits in motor
action-pattern selection to produce different vocal outputs.
Results
To assess fronto-striatal network activity during vocalization, 47 extracellular, paired record-
ings were acquired from the FAF and the CN of the dorsal striatum of four male bats. Striatal
recordings were performed with linear tetrodes (electrode spacing: 200 μm), while FAF activity
was measured with linear 16-channel probes (electrode spacing: 50 μm). The placement of
chronically implanted tetrodes in the CN was confirmed histologically for each animal (see
example Nissl section in S1 Fig). The laminar probe used for FAF measurements was intro-
duced on each recording day. Throughout the manuscript, we will refer to different frequency
bands of the LFP as theta (4–8 Hz), alpha (8–12 Hz), low beta (12–20 Hz), high beta (20–30
Hz), low gamma (30–50 Hz), and high gamma (50–80 Hz).
Properties of bat vocalizations
Individual bats were placed in an acoustically and electrically isolated chamber and allowed to
vocalize spontaneously while neural activity in the CN and FAF were simultaneously mea-
sured. A total of 39,014 spontaneously emitted calls were recorded from implanted, head-fixed
animals. Most of the vocalizations recorded occurred as trains of syllables produced at short
intervals (Fig 1A and 1B). Across recordings, the median calling interval amounted to 12 ± 54
ms (± interquartile range, IQR).
For analyzing neural activity related to vocalization, we focused on utterances surrounded
by at least 500 ms pre- and post-time without sounds. A pool of 628 communication calls and
493 echolocation pulses remained after vocalization selection (communication: 628/16,204
[3.9%]; and echolocation: 493/22,810 [2.2%]). The main criterion used for classifying sounds
into echolocation and communication was based on their spectro-temporal structure. It is
known that C. perspicillata’s echolocation pulses are short (<2 ms) downward frequency mod-
ulated and peak at high frequencies >50 kHz (see example spectrogram in Fig 1C and [57]),
while communication calls cover a wider range of sound durations and contain most energy at
lower frequencies, generally below 50 kHz (see examples in Fig 1D and 1E and [58,59]).
In our dataset, at the population level, call duration of both types of isolated vocalizations
did not differ statistically (p = 0.56, Wilcoxon rank-sum test; the test considered only the
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 3 / 29
temporally isolated calls used for further analysis) with a median around 0.33 ms in both cases
and IQR values of ±1.73 ms for communication and ±1.23 ms for echolocation (Fig 1F). As
expected, peak frequency differed significantly between the two call types (echolocation, 72
kHz ± 30 kHz, and communication, 14.0 kHz ± 6 kHz, rank-sum test p < 0.0001, Fig 1F). In
the echolocation category, differences in peak frequency across calls could be due to interindi-
vidual variability in sonar pulse design and to the use of different echolocation harmonics even
by the same bat. Differences between echolocation and communication calls reported here
were also evident in median spectra calculated considering all calls from each call type (Fig
1G). As frequency was used as the main distinctive feature for characterizing the two call clas-
ses, the results described in the preceding text constitute a proof-of-principle.
Communication calls were further subdivided into those that contained pronounced power
only at low frequencies (<50 kHz, “LF” communication calls, n = 319) and those that con-
tained pronounced energy at both low and high frequencies (“LHF” communication calls,
n = 309, see call examples and median spectra of both communication call groups in S2 Fig).
This classification of communication calls considers only the spectral structure of the sounds
but does not provide information about the function of the calls uttered. The communication
call category considered in this manuscript covers a broad range of vocalizations, and it might
include different sound types.
Besides neural recordings during spontaneous vocalization, bats were presented with pure
tones (10–90 kHz in steps of 5 kHz at a 60-dB sound pressure level [SPL] with a 10-ms duration)
Fig 1. Properti es of echoloca tion pulses and communi cation calls produced by bats. (a) Exemplar y acoustic recording includin g
an isolated call and a vocalizat ion train. Zoomed-in views have been included in (b) and (c) to show spectrogram s of the syllable
train and the isolated echolocation pulse. Panels (d) and (e) display two further examples of isolated vocalizat ions (communic ation
calls in this case). Panel (f) shows a combined histogram of sound duration and peak frequency in echolocat ion and commun ication
sounds. Note that these two call types are well segregated in the frequency domain. The latter is also noticeable in the average call
spectra shown in (g). Data underl ying this figure can be found at https://doi .org/10.12 751/g-node .6a0d94.
https:// doi.org/10.1371 /journal.pbio .3000658.g001
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 4 / 29
to evaluate auditory responsiveness in the neural populations recorded (see frequency tuning
results in S3 Fig). The acquired LFPs in both brain regions showed pronounced responses to
sounds (see population-evoked responses in S3A and S3B Fig and S3I–S3K Fig), revealing a pref-
erence towards low frequencies around 15–20 kHz (best frequency distributions for both struc-
tures studied are shown in S3C and S3D Fig). Note that a preference towards low-frequency
sounds does not necessarily imply a lack of responses to natural high-frequency sounds such as
echolocation calls (see below). Within columns of the FAF, channels located at depths below
400 μm showed the highest auditory responsiveness, and neighboring channels had similar fre-
quency tuning properties (see comparison of frequency tuning curves across cortical layers in S3E
Fig).
Correlating LFP oscillations with vocal output
LFPs occurring 500 ms before and after call onset were analyzed to gain insights into the
involvement of fronto-striatal regions in vocalization. LFPs were filtered (1–90 Hz), demeaned,
and z-normalized (see Methods). Average LFPs obtained in the CN and FAF are shown in Fig
2 (CN: Fig 2A and 2B; FAF: colormaps in Fig 2C and 2D; see also S4 Fig for recordings in one
example column). Deflections in the LFP signals following the production of echolocation
pulses and communication calls were evident in both brain areas. These deflections could
reflect evoked responses related to the processing of the vocalizations. In the FAF, vocaliza-
tion-evoked responses were strongest in deep layers (i.e., channels located at depths >400 μm)
Fig 2. LFPs during vocalization in the CN and FAF. (a) Mean LFP (± SEM) of all isolated communic ation calls (n = 628)
studied. Signals from all three channels of the striatum were pooled together thus rendering a higher number of responses
for the striatum than for the FAF. (b) Mean LFP (± SEM) obtained during the productio n of isolated echolocation pulses
(n = 493) in the striatum . (c) and (d) Colorma ps showing the mean of z-scored LFPs in the FAF across cortical depths, 500
ms before and after commun ication calls (c) and echolocation pulses (d). Data underly ing this figure can be found at https://
doi.org/10.12 751/g-node .6a0d94. CN, caudate nucleus; FAF, frontal auditory field; LFP, local field potential.
https://doi.org/10 .1371/journal.p bio.3000658. g002
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 5 / 29
matching the areas of highest responsivity to pure tones (compare colormaps in Fig 2C and
2D with the colormap shown in S3 Fig; see also the example column in S4 Fig).
Next, we performed spectral analysis of the LFP signals. LFP spectrograms were calculated
from bootstrapped signals based on 10,000 randomization trials for each vocalization type (see
Methods). This approach allowed us to assess spectral components that are consistently time
locked across vocalization trials. The striatal spectrograms followed the typical power rule by
which high power occurred in the low LFP frequencies and power decreased as LFP frequency
increased (Fig 3A and 3B).
When comparing both conditions (echolocation versus communication) with each other,
time- and frequency-dependent variations were detected. These differences became obvious
when comparing both power spectrograms using the Cliff’s Delta (d) metric (Fig 3C). Briefly,
the d-metric describes the effect size of group comparisons and ranges from −1 to 1, with iden-
tical groups rendering values around zero [60]. This measure was designed for nonparametric
tests (in contrast to Cohen’s d), and it quantifies how often values in one distribution are larger
than values in a second distribution.
Cliff’s Delta matrices revealed higher power in the gamma range of the LFP (especially fre-
quencies >70 Hz) before communication call production in relation to the time before emis-
sion of echolocation pulses (blue areas in Fig 3C). Differences in the gamma range prior to
vocalization had a medium size effect (gray contour lines in Fig 3C) following values proposed
in previous studies [60]. In contrast, power in the beta range (12–30 Hz) was found to be more
pronounced before and during echolocation than during communication emission. Both
effects observed suggest that the power in distinct striatal LFP frequencies can be correlated
with the production of different types of vocalization (beta is higher for echolocation, and
gamma for communication). To portray the power of individual examples, representative sin-
gle trials of LFP signals in the frequency ranges displaying the highest vocalization-dependent
differences are shown in S5A–S5D Fig (CN) and S5E–S5L Fig (FAF).
Similar to the CN, spectrograms of FAF neural signals related to communication calls (Fig
4A–4D) and echolocation pulses (Fig 4E–4H) followed a power rule. Large differences could
be detected when comparing the neural spectrograms obtained during echolocation and com-
munication (Fig 4I–4L). The largest differences were found in the low- and high-gamma
range, with the power being higher before and during echolocation pulses than during com-
munication calls, especially at FAF depths below 200 μm. The latter is illustrated in Fig 4I–4L
for four exemplary recording channels located at different depths and in Fig 4O for all FAF
Fig 3. Spectral differenc es in neural activity obtained in the CN during echoloca tion and communica tion production . (a)–(b) Power spectrogram in
the CN during commun ication (a) and echolocat ion (b). Mean values of 10,000 randomiz ation trials are displayed in each case. (c) Colormap representing
the Cliff’s Delta values of echolocat ion versus communica tion comparison s at each time point and frequency . Gray outlined regions mark areas with a
medium effect size (Cliff’s Delta > 0.33 [60]). Red colors indicate more power in the LFPs during echoloca tion than communicat ion. Blue regions indicate
the opposite trend. The LFPs underlying this figure can be found at https://d oi.org/10.12 751/g-node .6a0d94. CN, caudate nucleus; LFP, local field
potential.
https://doi.o rg/10.1371/j ournal.pbio.30 00658.g003
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 6 / 29
depths studied. Other large spectral differences were found in the theta-alpha range both
before and after vocalization with a time- and depth-dependent pattern (see red and blue
regions in example channels in Fig 4I–4L and across-depths data in Fig 4M). Differences in
Fig 4. Time-freque ncy differenc es in power distribution s across FAF channels, depending on the vocalizatio n type. (a)–(d) LFP spectrogram s of four
illustrativ e channels of the FAF for the commun ication condition (n = 10,000 randomiz ation trials, see Methods). (e)–(h) Spectrogram s obtained in the same
four example channels during echoloc ation. (i)–(l) Colormap s of Cliff’s Delta values obtained when comparin g the time-freque ncy dynamics in the
echoloca tion and commun ication conditions in the four example channels . Black highlighted regions indicate large effect size (d > 0.47). Gray indicates
medium effect size (d > 0.33) [60]. (m)–(o) Mean Cliff’s Delta values across FAF depths. Mean values were obtained for all the frequenc ies that composed
the theta (4–8 Hz), beta (12–30 Hz), and gamma (30–80 Hz) bands, represente d in panels m, n, and o, respectively. This figure was created based on data that
can be found at https://d oi.org/10.1 2751/g-node .6a0d94. FAF, frontal auditory field; LFP, local field potentia l.
https://d oi.org/10.1371/j ournal.pbio. 3000658.g004
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 7 / 29
the beta band were pronounced mostly before sound production and occurred at different
time points before call onset across cortical depths (Fig 4N). Overall, these results suggest that
different neural frequency channels in the FAF and CN correlate differently with the bats’
vocal output.
We considered the possibility that differences in neural oscillations observed may be
directly related to specializations for producing high- versus low-frequency sounds, and only
secondarily to the fact that one vocalization set is used for navigation, while the other is used
for social communication. To test this possibility, spectral analyses were performed comparing
LFPs recorded during the emission of communication calls with low- and high-frequency
components (LHF calls) versus echolocation calls (see Fig 5). As mentioned in the preceding
text, besides high power in low frequencies, LHF calls exhibited pronounced power at frequen-
cies above 50 kHz (see S2 Fig and Fig 5A). The results of comparing neural activity related to
the production of LHF calls versus echolocation pulses are shown in Fig 5B, 5C–5F for the CN
and FAF, respectively. Overall, the results obtained when considering only LHF calls did not
Fig 5. LFP power differences during the production of LHF communica tion calls and echolocat ion pulses. LHF
commun ication calls carry pronounced energy at both low (<50 kHz) and high frequenc y (see median vocaliza tion
spectra in (a)). LF calls carry power only at low frequenc ies, while echolocation pulses carry power at high frequencies.
(b) Cliff’s Delta effect size measu res obtained in the CN when comparing LHF versus echoloca tion sounds. (c)–(d)
Similar to panel (b), but for the FAF at 300-μm and 800-μm depths, respective ly. (e)–(f) Average Cliff’s Delta across
FAF depths in the beta and gamma ranges, respectively. Overall, the results obtained when comparing neural activity
related to LHF and echoloca tion call productio n resembled those obtained when pooling data from all communica tion
calls (see Fig 4; for results of comparing LHF and LF calls, see S6 Fig). Data underlying this figure can be found at
https://d oi.org/10.12 751/g-node .6a0d94. CN, caudate nucleus; FAF, frontal auditory field; LF, low-frequen cy; LFP,
local field potentia l; LHF, low- and high-freq uency.
https://d oi.org/10.1371/j ournal.pbio. 3000658.g005
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 8 / 29
differ from those obtained after pooling all communication calls together (compare results
presented in Fig 4 and Fig 5). In both cases, differences between echolocation pulse and com-
munication call production appeared before call production in the gamma and beta bands.
Comparing LHF and LF communication calls with each other rendered only post-vocalization
differences in the gamma range and differences in the theta-alpha range in the FAF localized
around the time of call production (see S6 Fig). Taken together, our results indicate that differ-
ences in LFP spectral power are not related solely to the presence/absence of high-frequency
components in the calls emitted.
The spectral structure of LFPs predicts vocal output
We used binary support vector machine (SVM) classifiers to assess whether models could be
constructed to “predict” the bats’ vocal output based solely on the power distribution of LFPs
before (or after) call production. SVM classifiers were trained (only once) with 10,000 ran-
domly chosen power distributions across time and frequency bands (for each frequency band,
the average power at each time point was calculated; 5,000 randomization trials per call type).
In a first analysis step, only spectral power occurring before call onset was considered for train-
ing and predicting vocal output. The remaining 10,000 power distributions (5,000 per call
type) were used to compute the percentage of correct hits by the models (Fig 6A).
In the CN, when using only pre-vocalization information, low-beta and high-gamma band
LFPs provided the best predictions about the type of upcoming vocal outputs (approximately
65% correct hits in both cases; Fig 6A top panel). Note that these frequency bands showed the
highest differences in power when comparing both vocalization conditions (cf. Fig 3C). Over-
all, the FAF provided higher prediction accuracy than the CN (Fig 6A bottom panel). Here,
the gamma band (in particular the high gamma band [50–80 Hz]) displayed high accuracy in
predicting the type of vocal output, reaching values of approximately 80% accuracy at depths
>500 μm. Gamma signals in the FAF also produced the lowest model cross-validation errors
(see S7A and S7B Fig). In both brain structures, training the SVM classifiers with false infor-
mation created by randomization of the labels in training signals led to a drop in prediction
capability, with true detection rates around chance level (i.e., 50%, see S7C and S7D Fig).
Next, the same SVM classifier analysis was performed based on the power of LFPs recorded
after vocal production (Fig 6B). For the post-vocalization LFP power, the best prediction
occurred again in deep layers of the FAF in gamma frequencies (maximum of approximately
78% correct hits). Interestingly, prediction power in the CN was lower in post-vocalization sig-
nals when compared to the pre-vocalization time (compare colors in top panels of Fig 6A and
6B). The latter suggests that evoked responses following vocal production in the striatum are
poorly correlated with the type of vocalization perceived by the bats.
In a last step, we ran the classifier analysis using a third dataset composed of pre-vocaliza-
tion LFPs in trials in which the post-vocalization time was contaminated with other sounds
produced by the animal. This includes cases in which trains of vocalizations (sometimes mix-
tures of echolocation and communication) were produced. Despite this possible confound, the
classifier was still able to reach accuracy levels of approximately 68% correct hits when consid-
ering gamma activity in deep FAF channels (Fig 6C).
Fronto-striatal coupling occurs in low-frequency bands of the LFP
To investigate the functional coupling between the FAF and CN during vocalization, the neu-
ral coherency was calculated. Coherency refers to the trial-averaged cross-spectral density of
two signals measured simultaneously, taking into account the phase synchrony of the signals.
Here, the magnitude of coherency (defined as “coherence”) was calculated between neural
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 9 / 29
signals recorded at different depths of the FAF and the CN (Fig 7). The preferred frequencies
for coherence between both structures were located in the low spectral range (under 12 Hz,
mostly in theta, see below) for both types of vocalizations. There was a striking difference in
the temporal pattern of coherence observed in both vocalization conditions. For communica-
tion calls, the highest fronto-striatal coherence was found before and during call production
(Fig 7A–7D). This temporal pattern could be further divided into LHF communication calls
showing highest coherence before call onset and LF communication calls exhibiting coherence
maxima during/slightly after call emission (see S8 Fig for coherence patterns for LF and LHF
calls). However, when echolocation pulses were produced, coherence shifted to even later time
points after call emission (Fig 7G–7J).
The different temporal coherence patterns in the two vocalization conditions were also
clear in average coherence plots that display the mean theta and alpha coherence across all
FAF depths studied (Fig 7E, 7F, 7L and 7L). Note that regardless of the vocalization type pro-
duced, FAF depths below 600 μm rendered the lowest coherence values, even though they dis-
played the strongest LFP deflections during call production (compare results in Fig 7E and 7K
with Fig 2C and 2D). Also note that the gamma band of the LFP was not involved in inter-
Fig 6. LFP signals leading to vocaliz ation can be used to predict vocal output. (a) Prediction accurac y calculated using a binary SVM
classifier (see Methods) trained with LFP informa tion (filtered by frequency band) occurring before vocalizat ion in the echolocation and
commun ication conditions (all communica tion calls were pooled together). Models were trained with half of the data (n = 5,000
randomiz ation trials in each vocalization condition). The other data half was used for calculating the models’ prediction accuracy. (b) Same
as panel (a), but in this case the models had to classify post-v ocalization activity. Note that in the post-vocali zation condition, prediction
accuracy dropped in the striatum . In the FAF, accuracy was still highest in deep layers in the gamma range. (c) Same as (a) and (b), but here
the model had to predict a third dataset correspond ing to pre-vocal ization activity in trials with contamin ated post-vocali zation time
(training set was the same as in (a)). Even in this case, FAF signals render ed good predictions about ensuing vocal output. The SVM was
computed based on data that can be found at https://doi .org/10.127 51/g-node.6a0 d94. CN, caudate nucleus ; FAF, frontal auditory field; LFP,
local field potentia l; SVM, support vector machine.
https://d oi.org/10.1371/j ournal.pbio. 3000658.g006
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 10 / 29
Fig 7. Functional coupling between the FAF and the CN during vocalization . Time-fre quency resolved coherence
between the striatum and four exemplary channels of the FAF at (a) 100-μm; (b) 300-μm; (c) 500-μm; and (d) 800-μm
depths during commun ication (n = 628 trials). Black lined regions refer to the 95th percentile of all computed
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 11 / 29
areal coherence, even though this band did show differences in within-structure analysis of
LFP signals during echolocation pulse and communication call production (see Results pre-
sented in Figs 3 and 4). Taken together, our results indicate temporally defined functional cou-
pling of fronto-striatal circuits depending on the type of vocal output produced by bats.
Frequency-dependent spike-LFP locking prior to vocalization
We also studied the spiking pattern of striatal and FAF neurons and the relation between spik-
ing and LFP phase. Spiking activity was gathered from spike-sorted single units (see Methods).
Peri-stimulus time histograms (PSTHs) computed for the CN did not show clear evidence for
evoked responses following vocalization in either vocalization condition (Fig 8A and 8B). In
the FAF, spiking was strongest in superficial and deep layers and vocalization-trigger ed spik-
ing was apparent at depths below 600 μm in both vocalization conditions (Fig 8C and 8D).
The locking between spikes and the phase of LFPs occurring before vocalization was stud-
ied. Phase-locking values were calculated by linking spike times to the instantaneous phase of
each LFP frequency band (see example phase-locking calculations in S9 Fig). The circular dis-
tributions of LFP phases at which spiking occurred for each frequency band were compared
with random-phase distributions obtained by extracting LFP phases at time points not related
to spiking. To get robust circular spike-phase and random-phase distributions, circular distri-
butions were calculated via bootstrapping (see Methods). Differences in vector strength (dVS)
between spike-phase and random-phase distributions were calculated to estimate the strength
of spike-phase locking (see circular distributions and vector strengths [VS] in S10 Fig). Signifi-
cance was assessed by comparing VS values obtained across randomization trials for the spike-
phase and random-phase conditions (Bonferroni-corrected Wilcoxon rank-sum test
p < 0.001, see Methods).
In the CN, significant differences between spike-phase and random-phase distributions
were found in the theta band during communication and in the alpha and high-gamma bands
during echolocation (Fig 9A and 9B). When comparing VS distributions from both vocaliza-
tion conditions (not with the surrogate data) in the striatum, significant differences were only
found in the high beta range (Fig 9C). The FAF showed statistically significant spike-phase
locking in several LFP frequency bands and cortical depths (Fig 9D and 9E). In particular,
spike-phase locking in the low- and high-gamma LFP bands was pronounced across layers,
and consistent differences appeared when comparing between vocalization types in the low-
gamma range at FAF depths >600 μm (Fig 9F). Besides the gamma spike-phase locking
observed, in the communication condition, there was consistent spike-phase locking in the
theta band at depths spanning from 250 to 400 μm (Fig 9D), although this effect was not signif-
icant when comparing between vocalization types (Fig 9F). Note that we refer to “consistent”
spike-phase locking differences whenever statistical significance occurred in more than two
contiguous FAF channels. The effect size calculations (e.g., Cliff’s Delta) complementing rank-
sum testing rendered in all cases values below 0.2, thus indicating high data variability (see
effect size plots in S11 Fig). Overall, our results indicate that coupling between LFPs and spik-
ing occurs in the striatum and deep layers of the FAF before vocal production.
coherenc e values during vocaliz ation. (e) Time resolved coherence strength between both structures across cortica l
depths in theta and alpha (panel (f)) during the production of communica tion calls. Mean coherence values across
frequenc ies in each range were calculated. (g)–(j) Coherogram s in four example channel s during echoloca tion pulse
productio n (n = 493 trials). (k)–(l) Same as (e) and (f) but for the echolocat ion case. During echoloc ation production,
pronounce d coherence in theta in the top-to-mid dle layers was found 200 ms after call onset. This tempo ral pattern
differs from that observed during the production of communic ation calls. The coherence was computed based on data
that can be found at https://doi .org/10.127 51/g-node.6a0 d94. CN, caudate nucleus ; FAF, frontal auditory field.
https://d oi.org/10.1371/j ournal.pbio. 3000658.g007
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 12 / 29
Discussion
Previous work has shown alterations in the fronto-striatal network in disorders with impaired
speech production in humans [8,61]. However, electrophysiological mechanisms by which
fronto-striatal activity could participate in vocal production in humans and other vertebrate
species remain elusive. In this article, we show that neural oscillations in fronto-striatal circuits
are distinctly linked to the type of vocalizations produced by bats. The main findings reported
in this paper include the following:
1. A unique intra-areal pattern of LFP frequency representation during vocalization (most
prominent in beta and gamma LFP ranges (12–30 and 30–80 Hz, respectively), which can
be used to predict ensuing vocal actions.
2. Functional coupling between the CN and FAF in low frequencies (theta, 4–8 Hz) with tem-
porally distinct characteristics depending on the vocal output.
3. The occurrence of spike-LFP phase locking, especially in frontal areas in the gamma LFP
band prior to vocalization.
Taken together, these results suggest a functional involvement of the fronto-striatal network
in neural processing for selecting and producing different types of vocalizations, with the
capacity to discriminate between, and predict, different vocal motor outputs. Moreover, neural
activity in the FAF and CN appears to correlate on a LFP and single-unit basis to vocalization,
but appears to be coupled in distinct frequencies and time points in relation to the vocal motor
Fig 8. Spiking activity in the CN and FAF during vocalizatio n. Spiking probability (comput ed as numbers of spikes per
trial per bin, binsize = 3 ms) in the CN 500 ms before and after commun ication ((a), n = 628 trials) and echolocation ((b),
n = 493). Spiking across all channels recorded in the FAF during communic ation (c) and echolocat ion (d). In the FAF,
during both types of vocaliza tions, distinct spiking activity could be identified in deep layers. One reason for the small
increase in spiking activity in response to the vocaliza tion could be due to the sparse distributi on of vocalizat ion relevant
neurons in the FAF. Data underl ying this figure can be found at https://doi .org/10.12 751/g-node .6a0d94. CN, caudate
nucleus; FAF, frontal auditory field.
https://doi.org/10 .1371/journal.p bio.3000658 .g008
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 13 / 29
action. A graphical abstract summarizing the results presented in this manuscript can be
found in Fig 10 (see also the summary presented in S1 Table).
Linking fronto-striatal oscillations to vocal output: General considerations
Our hypothesis that echolocation pulses and communication calls involve different fronto-
striatal network dynamics could be corroborated. In bats, differences related to the production
Fig 9. Spike-ph ase locking across vocaliz ation condition s. (a) dVS obtained before vocalizat ion onset in the communica tion-surrogat e condition in
the CN; (b) echolocation -surrogate condition; and (c) echolocation -communica tion condition. (d)–(f) dVS values computed for all recorded
channels in the FAF in the three conditions mention ed above. Statistic al differe nces were tested by comparing VS distributions (Wilcoxon rank-sum
tests with Bonferron i correctio n,
�
p < 0.001, see Methods). Data underly ing this figure can be found at https://doi .org/10.127 51/g-node.6a0 d94. CN,
caudate nucleus; dVS, difference in vector strength; FAF, frontal auditory field; VS, vector strength.
https:// doi.org/10.1371 /journal.pbio .3000658.g009
Fig 10. Visual abstract depicting the main results presented in this study. “SG,” “G,” and “IG” indicate a putative
subdivisio n of the FAF into supragranu lar, granular, and infragranul ar layers, respective ly. Note that we do not report
data on the direction ality of the connectio n between both regions, and thus functional coupling is displayed with a
double arrow. Different electrophysio logical parameters such as LFP power measurements , spike-phase locking and
LFP–LFP coherence demonstrate that fronto-st riatal circuits can predict ensuing vocal output in bats. CN, caudate
nucleus; FAF, frontal auditory field; LFP, local field potential.
https://d oi.org/10.1371/j ournal.pbio. 3000658.g010
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 14 / 29
and processing of different types of vocalizations encompass neural oscillations in the theta,
beta, and gamma bands. This study presents only correlative evidence linking vocal produc-
tion to neural oscillations in the fronto-striatal network. The latter does not imply a causal role
of neural oscillations in vocal control.
Neural oscillations are a generalized phenomenon in the nervous system, and they have
been studied extensively in past years (for reviews see [29,35,62–64]). The current consensus is
that oscillations represent different excitability states in neural populations. Oscillatory activity
differs across brain structures and it participates in processes such as inter-areal synchroniza-
tion, local information binding, selective attention, and memory formation, among others
[27,65,66]. The neural mechanisms by which oscillations are generated in the brain are still
under debate. At least gamma oscillations observed in the neocortex and hippocampus seem
to originate from an interplay between excitatory and inhibitory activity in pyramidal cells and
interneurons (“pyramidal-interneuro n gamma” [PING] networks, for review see [62,67]). It
has been postulated that oscillations in other frequency bands could also be linked to pyrami-
dal-interneuron networks (PIN) that oscillate with different time constants (see for example
the PIN-theta networks proposed for the auditory cortex [64]). Low-frequency oscillations
(i.e., alpha and theta) also have been linked to pace-making pyramidal neurons, although it is
not clear if the underlying mechanism for pace-making relates to pyramidal-interneuron net-
works as well [68,69]. In humans, beta oscillations found in the striatum also seem to involve
inhibitory interactions between neurons [70]. With our current data, we cannot assess the cel-
lular mechanisms responsible for the oscillations observed in the bat striatum and frontal cor-
tex during vocalization. Regardless of the cellular origin of fronto-striatal oscillations, our data
show that, at least in bats, neural rhythms in these two structures correlate well with vocal
output.
In the present study, we focused on analyzing oscillatory activity related to vocalizations
that were surrounded by silent periods to avoid possible confounds related to the production
of call trains (except in Fig 6C, where calls with contaminated post-vocalization times were
used as control for the prediction analysis). We reasoned that situations in which bats pro-
duced vocalization trains with mixtures of echolocation and communication calls could render
misleading results. Future studies could assess whether pre-vocalization activity carries infor-
mation about the physical parameters of vocalization trains.
Overall, the observed electrophysiological effects during communication call production
need to be considered cautiously. Bats produce communication calls in numerous situations
such as, e.g., distress calling, courtship, and territorial disputes, among others [44,45]. The
most common way to parse communication calls into different subcategories is to score the
behavior/context during which the calls are produced [59,71,72]. As we recorded in head-fixed
animals, it is difficult to assess what type of communication calls were broadcasted. Pooling
vocalization trials from many types of communication calls together could potentially hide
call-specific effects.
Based on spectro-temporal features, we identified two types of communication vocaliza-
tions (containing either only low-frequency or high- and low-frequency components, see Fig 5
and S2 Fig). Even communication calls containing pronounced power at high frequency dif-
fered markedly from echolocation vocalizations. The latter indicates that differences observed
in terms of LFP spectral structure and inter-areal coupling are not related solely to the
absence/presence of high frequencies in the sounds uttered. Note that we cannot discard that
communication calls containing only high frequencies involve LFP patterns similar to those
observed during echolocation. Communication calls carrying only high frequencies were not
observed in our dataset, but C. perspicillata produces such calls in contexts such as mating
[59].
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 15 / 29
Theta oscillations for inter-areal coupling in the fronto-striatal circuit
According to our data, in bats, vocal production is linked to activity in the theta, beta, and
gamma bands of LFPs. The production of communication calls and echolocation pulses ren-
dered power in the theta range after vocalization (cf. Fig 4A with Fig 4B, across-depths data in
Fig 4M) as well as vocalization dependent inter-areal coherence patterns (Fig 7). Power differ-
ences after call onset also occurred in the beta and gamma range (Fig 4N and 4O). The time
period after vocal production must be examined carefully, as the calls produced could differ in
their acoustic attributes (i.e., frequency composition and duration, among others), which
could lead to differences in call-evoked neural responses. In different sensory cortices, low fre-
quencies such as theta and alpha are known to modulate sensory processing and enable sen-
sory selection [29,73,74]. Unlike sensory cortices, low-frequency oscillations in frontal areas
are less understood in terms of sensory processing.
Our data suggest that low-frequency rhythms in frontal areas (especially theta, see Fig 7)
relate to inter-areal communication between FAF superficial layers and the dorsal striatum
during vocalization, as quantified by computing inter-areal LFP coherence (Fig 7). This result
falls in line with a putative involvement of low-frequency oscillations in long-range synchrony
[27,28]. The FAF constitutes a nonclassical sensory area, and its laminar structure (i.e., loca-
tion of inputs and outputs, such as layer 4 and 5 in sensory cortices [75]) needs further ana-
tomical exploration.
According to our data, FAF layers could hold a crucial role in oscillatory communication
between frontal and striatal regions during vocalization initiation. When assessing the cou-
pling between fronto-striatal regions, the timing of inter-areal coherence seems to play an
important role when planning and producing different types of sounds (see Fig 7 and S8 Fig).
While the highest level of coherence was found before, during, or shortly after (<250 ms) com-
munication call production, echolocation-related coherence occurred at least 250 ms after
pulse onset. One possible explanation for the strong coherence following echolocation pulses
could be that the latter require a more thorough sensory processing and auditory feedback
after vocal production (i.e., for echo evaluation) than communication calls. Such post-process-
ing of echolocation pulses could be relevant for planning ensuing vocal actions and for a
coherent representation of the environment in bats. Note that the inter-areal coherence results
presented in this paper have implications beyond bat echolocation, as they suggest that tempo-
rally precise oscillatory coupling in the fronto-striatal circuit correlates with the production of
different vocal outputs. Such fine communication synchrony between brain structures could
be affected in conditions such as Parkinson, Huntington disease, and Asperger syndrome, in
which fronto-striatal impairments have been described [8,61].
Intra-areal beta and gamma oscillations provide neural correlates of vocal
output
Differences in LFP activity preceding vocal production also occurred in the beta band. Accord-
ing to our data in bats, the beta band of LFPs is differentially involved in echolocation pulse
and communication call emission. Beta power is highest during echolocation production in
the CN and in superficial layers of the FAF (see Fig 3 and Fig 4). As especially the beta band
activity is correlated with motor action planning and performance [36,37], one could hypothe-
size that the strength of beta oscillations in the CN and in superficial FAF layers is linked to dif-
ferent sensorimotor programs required for the production and/or post-vocalization evaluation
of acoustic signals (i.e., echoes during echolocation). Overall, beta is typically dominant in the
motor system, correlating with the maintenance of ongoing sensorimotor cognitive states and
endogenous timing processes [35,76]. Aberrant beta oscillations (especially in the striatum)
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 16 / 29
are also a key feature of the parkinsonian brain [4,8,77]. Our results together with those from
previous studies suggest that beta oscillations within the fronto-striatal path are important for
vocal motor output production.
Another large vocalization type–dependent effect was detected in the gamma band. Before
echolocation, high power in this frequency band was observed in deep layers of the FAF,
whereas before communication, high gamma power was found in the CN. As the power max-
ima in gamma was reversed across vocalization conditions in both brain structures, it could be
suggested that each component of the fronto-striatal path relies on a differential power distri-
bution of high frequencies in order to produce the same vocal output. This could be supported
by the fact that in both brain structures, power in the gamma band was the best predictor of
vocal output (Fig 6).
Gamma LFPs also appear to be related to spiking activity. The time periods before both
echolocation pulses and communication calls displayed significant phase-locking values in the
gamma range across FAF layers (Fig 9D and 9F). The latter suggests a generalized role of
gamma-phase coupling preceding vocalization. Spike-phase locking in the gamma range has
been demonstrated previously, correlated to vocalization in the sensorimotor nucleus of zebra
finches [24].
Classical functions of gamma rhythms across species are linked to selective attention, corti-
cal computation, and working memory [25]. In bats, changes in gamma power have been asso-
ciated with the processing of auditory stimulation in the bat auditory cortex and with social
interaction in frontal areas [78,79]. Moreover, an increase in gamma power was found in the
superior colliculus after the production of clusters of echolocation pulses in freely flying bats
[48]. The latter could relate to the detected rise of gamma power before echolocation in com-
parison to communication in the FAF (this study), and could indicate the putative importance
of gamma rhythms during navigation, whether the animals are freely flying (as in previous
studies) or exploring their environment using their biosonar from a fixed location (this study).
Note that gamma oscillations were not involved in long-range fronto-striatal communication
(see Fig 7). This finding supports the current view of gamma rhythms being important for
local neural computations [25,27].
To our knowledge, changes in gamma power linked to a specific motor action have not
been described before for the CN. The ventral striatum is known to display a prominent pat-
tern of gamma power during reward ingestion or decision-making [80], but the oscillatory
properties of the nuclei that form the dorsal striatum (such as the CN) are less studied. Our
results show that not only the FAF but also the gamma power in the CN are correlated with
the type of vocal output.
Taken together, the findings presented in this manuscript indicate that neural oscillations
in the gamma and beta bands in fronto-striatal brain regions represent ensuing vocal actions
in bats, while oscillations in the theta-alpha range represent the differential sensory processing
of the type of call uttered and play a role in long-range inter-areal coupling. Our data suggest
that fronto-striatal circuits are an important component of canonical networks underlying
vocalization in mammals, and that these circuits could bear key specializations supporting bat
echolocation.
Methods
Ethics statement
All experiments described in this article comply with current guidelines and regulations for
animal experimentation and the Declaration of Helsinki. Experiments were approved by the
Regierungspra ¨ sidium Darmstadt, Germany (permit number: FU1126).
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 17 / 29
Surgical procedure
For neurophysiological recordings, 4 adult Seba’s short-tailed bats (C. perspicillata) were used.
The animals originated from a breeding colony at the Institute for Cell Biology and Neurosci-
ence, Goethe University, Frankfurt am Main (Germany). Bats underwent a surgical procedure
for gaining access to frontal and striatal brain regions. The surgery encompassed the implanta-
tion of a chronic tetrode mounted on a microdrive in the striatum, a craniotomy above the
FAF for the insertion of a linear silicon probe, and the attachment of a custom-made metal
rod. The latter facilitated stable recording conditions by preventing head movements. The
implantation protocol was modified from the procedure used in previous studies [73,74,81–
84].
First, after monitoring the health status, bats were anesthetized subcutaneously with a mix-
ture of ketamine (10 mg/kg Ketavet, Pfizer, Berlin, Germany) and xylazine (38 mg/kg Rom-
pun, Bayer, Leverkusen, Germany) and topically with local anaesthesia (Ropivacaine 1%,
AstraZeneca GmbH, Wedel, Germany). After achieving stable anaesthesia conditions, animals
were placed on a heating blanket (Harvard Apparatus, Homoeothermic blanket control unit,
Holliston, MA) at 28˚C. Afterwards, the fur on top of the head was excised, the skull was
exposed via a longitudinal midline incision, and the skin, connective tissue, muscle, and debris
were removed. Using macroscopically visible landmarks (e.g., the pseudocentral sulcus and
blood vessels), the skull was evenly aligned. With a scalpel blade, a first craniotomy (approxi-
mate 2-mm diameter) was made between the sulcus anterior and pseudocentral sulcus for the
chronic implantation of a tetrode (Q1-4-5mm-200-177-H Q4_21mm, NeuroNexus, Ann
Arbor, MI, see S1 Fig) mounted on a moveable microdrive (dDrive-m, NeuroNexus, Ann
Arbor, MI) to ensure mobility of the electrodes. To prevent the electrodes from bending, the
tetrode was introduced into the tissue (partial implant with 2.0-mm depth) with an angle of
17˚ perpendicular to the brain surface under the microscope. Subsequently, the microdrive
was fixed to the scalp with a two-component UV-acrylic glue (Kulzer GmbH, Hanau, Ger-
many) and dental cement (Paladur, Kulzer GmbH, Hanau, Germany) and was placed via a
screw (1 full counterclockwise turn = 150 μm) at the target position (in total: >2.1-mm depth).
For protection and shielding, a plastic cap covering the implant was glued using UV-acrylic.
The connector was permanently attached to the cap. For stability purposes, a custom-made
metal rod (2-cm length, 0.1-cm diameter) was fixed to the surface of the bat’s skull. The metal
post was glued using UV-acrylic and dental cement to the bone and the plastic cap posterior to
the tetrode (see sketch in S1A Fig). All efforts were made to reduce the weight of the implant
and the bat health status was carefully monitored throughout the experiments.
Before starting the recordings, a second craniotomy (2–3-mm diameter) rostral to the tet-
rode between the sulcus anterior and longitudinal fissure above the FAF was implemented
using a scalpel blade [52]. To record extracellular action potentials and LFPs in the FAF, an
acute A16 laminar probe (NeuroNexus, Ann Arbor, MI, S1B Fig) was introduced into the
brain on each recording day. After surgery, the animals had at least 48 hours of recovery before
starting electrophysiologica l recordings.
Neurophysiological recordings in vocalizing animals
All experiments were performed chronically for a maximum of 2 weeks after surgery. When-
ever the wounds were handled, local anaesthesia (Ropivacaine 1%, AstraZeneca GmbH,
Wedel, Germany) was administered topically. Before starting the electrophysiological record-
ings, the bat was placed in a custom-made holder with an attached heating blanket (see previ-
ous section) in a Faraday chamber. Subsequently, the tetrode was connected via an adaptor
(Adpt. CQ4-Omnetics16, NeuroNexus, Ann Arbor, MI) to a micro amplifier (MPA 16,
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 18 / 29
Multichannel Systems MCS GmbH, Reutlingen, Germany). For detecting neural activity in the
FAF, the laminar probe was lowered through the craniotomy under the cortical surface using a
micro manipulator (piezo manipulator PM101, Science Products GmbH, Hofheim, Germany)
with a speed of 50 μm/s. The linear probe spanned cortical depths of 50–800 μm below the
brain’s surface, with channels evenly distributed in 50-μm steps. One silver wire was placed
above the dura mater through a third small craniotomy and served as common ground elec-
trode for both the tetrode and the laminar probe. The reference of each electrode array was
short-circuited with the respective top recording channel (the electrode closest to the brain
surface) to obtain local signals and prevent movement artifacts. Neuronal signals from the stri-
atum and FAF were preamplified and connected via flexible cables to a portable multichannel
recording system with integrated AD converter (Multi Channel Systems MCS GmbH, model
ME32 System, Reutlingen, Germany). The recording was digitized at a sampling frequency of
20 kHz (16-bit precision). For monitoring, visualizing, and storing the data, MC_Rack_Soft-
ware Version 4.6.2 (Multi Channel Systems MCS GmbH, Reutlingen, Germany) was used.
For the acquisition of vocal outputs, a microphone (CMPA microphone, Avisoft Bioacus-
tics, Glienicke, Germany) was placed 10 cm in front of the animal. Acoustic recordings were
conducted with a sampling rate of 250 kHz. Vocalizations were amplified (gain = 0.5, Avisoft
UltraSoundGate 116Hm mobile recording interface system, Glienicke, Germany) and stored
in a PC using the Avisoft Recorder Software (Avisoft Bioacoustics, Glienicke, Germany) with
16-bit precision. Offline analysis was conducted to separate vocalizations into echolocation
and communication calls based on their spectro-temporal structure.
In order to synchronize the recording of the vocalization signals and the neurophysiological
signals, Matlab-generated triggers (i.e., a sound for acoustic recordings and a TTL pulse for the
neural acquisition system) were used to align both recordings. Each recording comprised
3 × 10-minute vocalization experiments, during which bats were let to vocalize at their own
volition, with a short break to stimulate vocal production by opening and closing the recording
chamber.
Acoustic stimulation
To estimate the responsiveness of the areas studied to acoustic stimuli, a frequency tuning par-
adigm was used. Frequency tuning was controlled via a custom-written Matlab software (Math
Works, Natick, MA). A stimulation speaker (NeoCD 1.0 Ribbon Tweeter; Fuontek Electronics,
Jiaxing, China) was placed 12 cm in front of the animal and pure tones were presented ranging
from 10 to 90 kHz in 5-kHz steps (randomized order, repetitions of each pure tone = 30 times)
for a duration of 10 ms (0.5-ms rise/fall time) at 60 dB SPL. Following digital-to-analogue con-
version using a soundcard (RME Fireface 400, 192 kHz, 24-bit), the generated pure tones were
amplified (Rotel power amplifier, model RB-1050, Worthing, United Kingdom) and presented
to the bats.
Analysis of LFP data
The analysis was implemented using custom-written Matlab scripts (MATLAB R2015b, The
Math Works, Natick , MA). All vocalizations were assessed offline using the Avisoft SAS Lab
Pro software (v.5.2 Avisoft Bioacoustics, Glienicke, Germany). The initial acoustic trigger,
communication calls (typical power maximum around 5–50 kHz) and echolocation pulses
(peaking above 50 kHz, [57,58]) were manually located, individually labelled, and their timing
was exported to Matlab. To evade response contamination by other auditory stimuli, the
“clean” communication calls and echolocation pulses were identified, which comprised at least
500 ms without any vocalization prior to and following call production. Spectrograms of the
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 19 / 29
vocalizations were calculated with a frame width of 0.8 ms, a frame shift of 0.05 ms, and a ham-
ming window of 2,048-points length.
The peak frequency of each call was estimated from the de-noised FFT. De-noising was
achieved by subtracting the FFT of the noise floor to the FFT of the call in question (duration
of call and noise were matched in each case). Communication calls were split into two groups:
one group of communication calls with only high power at low frequencies (<50 Hz, LF calls)
and a second group that showed pronounced power in low and high frequencies (>50 kHz,
LHF calls). LF and LHF communication calls were classified based on their spectrum; e.g., a
call was assigned to the LHF group if the power maximum at frequencies above 50 kHz was at
least larger than half the power at frequencies below 50 kHz.
To investigate LFPs during each calling condition, the electrophysiological signal was fil-
tered between 1 and 90 Hz (second-order Butterworth filter), the line noise removed using the
rmlinesmovingwinc function of the Chronux toolbox [85], and down-sampled from 20 kHz to
1 kHz. Additionally, the signals were normalized by calculating the z-score at each time point
by subtracting the mean and dividing by the standard deviation per recording. Z-scoring was
conducted across channels for the FAF (to keep amplitude relationships across channels) and
for each channel of the CN individually.
To extract LFP fluctuations linked to vocalization, a randomization procedure was used.
This randomization procedure rendered 10,000 communication and echolocation signals for
the CN and each recording channel of the FAF. Each randomization trial was obtained by
averaging 100 randomly chosen LFPs corresponding to either the communication or echolo-
cation condition. Note that because of extensive averaging, this randomization procedure
removes signal components that are not locked to the vocalizations.
Time-frequency analysis was conducted for each randomization trial using the Chronux
function mtspecgramc with a 250-ms window size, 0.5-ms time step, and a time-bandwidth
product of 2 with 3 tapers. To compute the difference in power during the production of dif-
ferent call types, the logarithmic power spectrogram of the communication condition was sub-
tracted from the logarithm of the power spectrogram obtained during echolocation. Statistical
power was evaluated using Cliff’s Delta (d). This measure ranges between −1 and 1, with
almost identical observations rendering d-values around zero. The d-value borders for defin-
ing large, medium, and small effect sizes were set to 0.474, 0.333, and 0.147, respectively [60].
A binary SVM classifier was used for predicting vocal output using the average spectral sig-
nal in each LFP band either before or after vocalization. The SVM classifier was trained
(fitcsvm function, rbf kernel, Matlab 2015, single training, no standardization, fitting posterior
probabilities after model creation) using signals obtained in 10,000 randomization trials
(5,000 per vocalization type, see preceding text). SVM models obtained were cross-validated
using 10-fold cross-validation. In a second step, labels were swapped in the training set before
classification to assess the performance of the models in the absence of reliable training
information.
To evaluate the oscillatory coherence and phase consistency between signals in the striatum
and the different cortical depths of the FAF, the Chronux function cohgramc with the same
parameters used for spectral analysis (see neural spectrogram specifications above) was used.
This operation performed coherency calculations between all possible pairs of different chan-
nels in the FAF and each channel in the striatum (here, no randomization was used; in other
words, we used the LFPs linked to the production of each echolocation and communication
trial). Then, the average coherogram obtained between FAF channels and each striatal channel
was calculated. For displaying and assessing the strength of coherency, the magnitude of the
coherency (“coherence”) was used. Coherence values exceeding the 95th percentile of all
coherence values obtained were labelled as significant.
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 20 / 29
Using the same pre-processing methods described above (filtering, down-sampling, z-scor-
ing per recording, and demeaning), LFP responses obtained from the frequency tuning para-
digm were quantified. The absolute value of the analytical signal (obtained after Hilbert
transforming) was used to calculate the instantaneous energy of each recording channel in
response to each sound frequency tested. The frequency eliciting the highest amount of energy
was labelled as best frequency.
Analysis of spike data
Spiking activity was acquired by filtering neural signals in the frequency range of 300–3,000
Hz (second-order Butterworth filter). Spike detection was performed using the SpyKING CIR-
CUS toolbox with automatic clustering and a threshold of 5 median absolute deviations using
the best spiking template per channel and recording [86]. With a bin size of 3 ms, PSTHs were
calculated for both brain structures.
To investigate the relationship between spikes and LFPs, phase-locking values were calcu-
lated using the circular statistics toolbox [87]. For phase-locking calculations, only the time
window before vocalization was considered. The procedure used for calculating phase locking
values is illustrated in S9 Fig for one example echolocation trial. After extracting spike times
and raw LFPs related to the isolated vocalization trial, the LFP signal was filtered in different
frequency bands (e.g., theta [4–8 Hz], alpha [8–12 Hz], low beta [12–20 Hz], high beta [20–30
Hz], low gamma [30–50 Hz], and high gamma [50–80 Hz]). Filtered LFPs were Hilbert-trans-
formed, and their instantaneous phase information was extracted. The phase at which spiking
occurred for each LFP frequency band was stored and analyzed using circular statistics (see
below).
Circular distributions of LFP phases at which spiking occurred for each frequency band
were compared with random-phase distributions obtained by extracting LFP phases at ran-
dom time points not related to spiking. To get robust circular spike-phase and random-phase
distributions, circular distributions were calculated 10,000 times, with 100 randomly chosen
spike-phase and random-phase values included in each randomization trial. Two parameters
were extracted from the circular distributions obtained in each spike- and random-phase trial:
the distribution’s VS (circ_r function in the circular statistics toolbox [87]) and its angular
mean (circ_mean function in the circular statistics toolbox [87]). VS values obtained from all
randomization trials were used for assessing statistical significance when comparing spike-
phase and random-phase distributions using Bonferroni-correct ed Wilcoxon rank-sum tests
(p < 0.001). Angular mean values were used for visual display and for calculating population
VS differences (dVS). In our calculations, positive dVS values indicate higher VS in the spike-
phase distribution when compared to the random-phase control.
Histological verification of striatal recordings
For visualization of the electrode implantation location, histological analysis was performed
following the completion of the experiments. To locate the tracks of the chronically implanted
tetrode in the striatum, an electric lesion was performed for 10 seconds with 10 μA DC current
using a Stimulus Isolator A365 (World Precision Instruments, Friedberg, Germany) under
deep anaesthesia prior to perfusion. Electric lesions were set for each animal on the last experi-
mental day on the most ventral and dorsal striatal electrodes. Subsequently, the animals were
euthanized with an intraperitoneal injection of 0.1 mL sodium pentobarbital (160 mg/mL,
Narcoren, Boehringer-Ingelheim , Ingelheim am Rhein, Germany) and transcardially perfused
using a peristaltic pump (Ismatec, Wertheim, Germany) with a pressure rate of 3–4 mL/min-
utes. The bats were perfused with 0.1 M phosphate buffer saline for 5 minutes, followed by a
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 21 / 29
4% paraformaldehyde solution for 30 minutes. After removing the surrounding tissue, mus-
cles, and skull, the brain was carefully eviscerated, fixed in 4% paraformaldehyde at 4˚C for at
least one night, and placed in an ascending sucrose sequence solution (1 hour in 10%, 2–3
hours in 20%, 1 night in 30%) at 4˚C to avoid the formation of ice crystals in the tissue. Subse-
quently, the brain was frozen in an egg yolk embedding encompassing the fixation in glutaral-
dehyde (25%) with CO
2
. For sectioning the frozen brain, a cryostat (Leica CM 3050S, Leica
Microsystem, Wetzlar, Germany) was utilized and coronal slices (50 μm thick) were prepared,
mounted on gelatin-coated slides and Nissl stained. In brief, the brain slices were immersed in
96% ethanol overnight and 70% ethanol (5 minutes), hydrated in distilled water (3 × 3 min-
utes), stained in 0.5% cresylviolet (10 minutes), rinsed in diluted glacial acetic acid (30 sec-
onds), differentiated in 70% ethanol + glacial acetic acid until neuronal somata were still red-
violet stained with only faint coloration of the background, fixed in an ascending alcohol
sequence (2 × 5 minutes in 96% ethanol, 2 × 5 minutes in 100% isopropyl alcohol), cleaned by
Rotihistol I, II, and III solution (Carl-Roth GmbH, Karlsruhe, Germany) and covered with
DPX mounting medium. The inspection of the lesion was facilitated by a bright-field, fluores-
cence microscope (Keyence BZ-9000, Neu-Isenburg, Germany). A Nissl staining of a bat brain
with the associated track of a chronically implanted HQ4 tetrode in the dorsal part of the CN
can be found in S1D Fig.
Supporting information
S1 Fig. Electrode implantation procedure. (a) Schematic outline of the implantation sites.
Olfactory bulb denotes the anterior part of the brain, while the cerebellum is found in the pos-
terior part. (b) Mapping of the A16 laminar silicon probe with 50-μm spacing between elec-
trodes (which was implanted in the FAF), and (c) the HQ4 laminar tetrode with 200 μm
between recording sites chronically implanted in the CN. (d) The Nissl -stained section,
including the track of an HQ4 laminar tetrode implanted in the CN (4× magnification). CN,
caudate nucleus; FAF, frontal auditory field.
(EPS)
S2 Fig. Parsing communication vocalizations into LHF and LF calls. (a) Example communi-
cation call containing pronounced power at low (i.e., <50 kHz) and high frequencies. (b)
Example LF call. (c) Average spectrum of LHF and LF vocalizations. Data underlying this fig-
ure can be found at https://doi.org/10.12751/g-node.6a 0d94. LF, low-frequency; LHF, low-
and high-frequency.
(EPS)
S3 Fig. CN and FAF display auditory responsiveness to stimulation with pure tones. (a)
Mean population striatal activity ± SEM in response to the best frequency (bf) across recording
sites. The arrow indicates stimulus onset. (b) Bitmap of the amplitude of z-scored LFPs from
100 ms before up to 350 ms after the stimulus onset across cortical depths in the FAF. (c) His-
togram of bfs in the striatum. Mean (M) and SEM are indicated. (d) Histogram of bfs in the
FAF. Both brain structures exhibited pronounced auditory responsiveness to low frequencies.
(e) Distribution of the mean correlation coefficient obtained by correlating tuning curves of all
simultaneous recordings in different FAF depths. The mean value across recordings (n = 47)
was calculated. The high mean correlation (0.68) indicates similar tuning in neighboring chan-
nels. (f) Exemplary area under the curve (AUC) of the LFP response to different simulation
frequencies in the striatum and the FAF at depths of 300 μm (g) and 800 μm (h). The red cir-
cles indicate the bf. (i), (j), (k) Mean LFP traces (±SEM) following auditory stimulation at the
bf in the same exemplary recordings mentioned above. The arrows refer to the stimulation
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 22 / 29
onset. Subpanels (l), (m), (n) show the instantaneous energy of the respective LFP traces
shown in (i)-(k). Data underlying this figure can be found at https://doi.org/10.12751/g-node .
6a0d94. CN, caudate nucleus; FAF, frontal auditory field; LFP, local field potential.
(EPS)
S4 Fig. Illustrative differences in LFP activity during vocalization in the FAF and CN. (a)
Mean LFP (±SEM) of all isolated communication calls (n = 31) during one recording in the
striatum and (b) of all isolated echolocation pulses in the same recording (n = 28). (c) The
mean ± SEM traces in the FAF at four representative depths (200, 400, 600, and 800 μm) in the
same time period as (a) for communication and (d) echolocation. In the FAF, highest differ-
ences between call types occurred in the deepest channels. The example traces show activity
before call onset, which could be used to predict the type of vocal output in both brain regions.
Data underlying this figure can be found at https://doi.org/10.12751/g-node .6a0d94. CN, cau-
date nucleus; FAF, frontal auditory field; LFP, local field potential.
(EPS)
S5 Fig. Example neural recordings showing different LFP frequency patterns in the FAF
and CN. In each subpanel, bottom panels show the broadcasted call, whereas top panels show
filtered LFP traces obtained before and after call production in each case. (a) Individual exam-
ple LFP in the CN during echolocation and (b) communication filtered in high gamma. (c)
Example filtered LFPs (in the beta range) during echolocation and (d) communication. (e)–
(h) Analogous exemplification for the FAF at 800-μm cortical depth. (i)–(l) Second example
FAF recording during echolocation ((i) and (k)) and communication trials ((j) and (l)). In the
FAF, during echolocation trials, high gamma and beta power occurs before call production.
Data underlying this figure can be found at https://doi.org/10.12751/g-node .6a0d94. CN, cau-
date nucleus; FAF, frontal auditory field; LFP, local field potential.
(EPS)
S6 Fig. Differences in LFP power during the production of LHF communication versus LF
communication calls (see also S2 Fig). (a) Bitmap of the Cliff’s Delta effect size measure in
the CN when comparing LHF communication calls (higher power in red) with LF calls (higher
power in blue) revealing small power differences. (b) Similar as panel (a), but for the FAF at
300 μm and (c) 800-μm depth. Also in the FAF, the distinct pattern of power differences was
less clear than when comparing communication calls to echolocation pulses (see Figs 5 and 6
of the main manuscript). (d) Average Cliff’s Delta across FAF depths in the theta-alpha and (e)
in gamma ranges. Here, the strongest size effect occurred in low alpha-theta (but not in
gamma) in deep FAF channels at time points close to vocal production (0 in the x-axis). LFPs
underlying this figure can be found at https://doi.org/10.1 2751/g-node.6a0d94. CN, caudate
nucleus; FAF, frontal auditory field; LF, low-frequency; LFP, local field potential; LHF, low-
and high-frequency.
(EPS)
S7 Fig. Cross-validation and prediction accuracy of SVM prediction models. (a) Cross-vali-
dation error across LFP frequencies in the CN and (b) in the FAF. Note that the lowest cross-
validation errors occurred in the deep channels of the FAF in high gamma. (c) Assessment of
the SVM model performance based on randomly chosen labels in the training sessions in the
CN and (d) in the FAF. With unfaithful training information, model accuracy drops to values
around a chance level, approximately 50%. Data underlying this figure can be found at https://
doi.org/10.12751/g-node.6a0d94. CN, caudate nucleus; FAF, frontal auditory field; LFP, local
field potential; SVM, support vector machine.
(EPS)
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 23 / 29
S8 Fig. Coherence in fronto-striatal areas during the production of LF and LHF communi-
cation calls. (a) Mean LFP coherence related to LHF communication calls between the CN
and FAF at 300-μm depth and (b) 800-μm cortical depth. (c) Average coherence between the
CN and different cortical depths of the FAF in theta and (d) alpha. Black lines indicate coher-
ence values above the 95th percentile. For LHF calls, the highest coherence occurred before
call onset in the low frequencies. (e)–(f) Same as (a)–(b) and (g)–(h) same as (c)–(d) but for
LF communication calls. The coherence during LF communication call production was stron-
gest in the same frequency band but shifted in time to early times (<250 ms) after call onset.
Note that coherence in the echolocation condition occurred at later time points (>250 ms
after call onset; see Fig 7 in the main manuscript). Data underlying this figure can be found at
https://doi.org/10.12751/g-node .6a0d94. CN, caudate nucleus; FAF, frontal auditory field; LF,
low-frequency; LHF, low- and high-frequency.
(EPS)
S9 Fig. Illustrative calculation of phase locking values in one example trial within one
brain structure. (a) Spectrogram of the echolocation pulse emitted in this vocalization trial.
(b) Top: spike times obtained in this trial in the CN (represented as dots). Bottom: simulta-
neously recorded raw LFP trace in the CN. Filtered LFP signals are shown in (c) theta, (d)
alpha, (e) low-beta, (f) high-beta, (g) low-gamma, and (h) high-gamma. (i)–(n) Instantaneous
phase values extracted after Hilbert-transforming the filtered LFP signals associated with pan-
els (c)-(h), respectively. Phase values at the time points in which spiking occurred were used
for phase-locking calculations. CN, caudate nucleus; LFP, local field potential.
(EPS)
S10 Fig. Circular mean distributions illustrating spike-phase locking across brain regions
and frequencies. Circular mean distributions for communication call production in (a) theta,
(b) alpha, (c) low beta, (d) high beta, (e) low gamma, and (f) high gamma. In each row, the
first column indicates values acquired from the CN, whereas columns 2–4 display data
obtained at three different FAF depths (i.e., 50 μm, 500 μm, and 800 μm). Red lines indicate
the VS of each circular distribution. Data plotted in orange represent surrogate distributions.
(g)–(l) Same as (a)-(h) but for the echolocation condition. dVS = difference in VS between the
spike-phase locking distributions and the surrogate distributions;
�
p < 0.001 (Wilcoxon rank-
sum comparing VS values across randomization trials, Bonferroni corrected). Data underlying
this figure can be found at https://doi.org/10.12751/g-node .6a0d94. CN, caudate nucleus; FAF,
frontal auditory field; VS, vector strength.
(EPS)
S11 Fig. Effect sizes obtained from comparisons of phase locking values. (a) Cliff’s Delta (d-
values) obtained when comparing VS in the communication condition to the surrogate distri-
butions in the CN across LFP frequencies bands (n = 10,000; l. = low; h. = high). (b) Same as
(a), for the echolocation-surrogate condition. (c) d-Values obtained when comparing the VS
of the echolocation and communication conditions (positive = higher phase locking before
echolocation; negative = higher phase locking before communication). (d)–(f) d-Values across
depths and LFP frequency bands in the FAF for the communication-surrogat e condition, (e)
echolocation-surrogate condition, and (f) echolocation-communication condition.
�
Indicates
a small effect size (i.e., d > 0.147, found only in one case, see panel (e)). Data underlying this
figure can be found at https://doi.org/10.1 2751/g-node.6a0d94.
CN, caudate nucleus; FAF, frontal auditory field; LFP, local field potential; VS, vector strength.
(EPS)
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 24 / 29
S1 Table. Table depicting the main results of this study. See also Fig 10 of the main manu-
script. CN, caudate nucleus; FAF, frontal auditory field.
(EPS)
Acknowledgmen ts
We thank Gisa Prange for histological support, Christin Reißig for animal care, and Manfred
Ko ¨ ssl for valuable comments on an earlier version of the article.
Author Contributions
Conceptualization: Kristin Weineck, Francisco Garcı ´ a-Rosales, Julio C. Hechavarrı ´ a.
Formal analysis: Kristin Weineck.
Funding acquisition: Julio C. Hechavarrı ´ a.
Investigation: Kristin Weineck, Julio C. Hechavarrı ´ a.
Methodology: Kristin Weineck, Francisco Garcı ´ a-Rosales, Julio C. Hechavarrı ´ a.
Project administration: Julio C. Hechavarrı ´ a.
Resources: Julio C. Hechavarrı ´ a.
Software: Kristin Weineck, Francisco Garcı ´ a-Rosales.
Supervision: Julio C. Hechavarrı ´ a.
Visualization: Kristin Weineck.
Writing – original draft: Kristin Weineck.
Writing – review & editing: Francisco Garcı ´ a-Rosales, Julio C. Hechavarrı ´ a.
References
1. Wegdell F, Hammers chmidt K, Fischer J. Conserved alarm calls but rapid auditory learning in monkey
response s to novel flying objects. Nature ecology & evolution. 2019:1.
2. Kanwal JS, Rauschec ker JP. Audito ry cortex of bats and primates: managin g species-spec ific calls for
social communicat ion. Frontiers in bioscience: a journal and virtual library. 2007; 12:4621.
3. Etchell AC, Johnson BW, Sowman PF. Beta oscillation s, timing, and stuttering . Frontiers in Human
Neuroscienc e. 2015; 8(1036). https://doi.or g/10.338 9/fnhum.20 14.01036 PMID: 25601832
4. Volkmann J, Hefter H, Lange HW, Freund HJ. Impairmen t of temporal organizat ion of speech in basal
ganglia diseases. Brain and Languag e. 1992; 43(3):386– 99. https://do i.org/10.1016 /0093-934x (92)
90108-q PMID: 144620 9
5. Sukhodo lsky DG, Leckman JF, Rothenber ger A, Scahill L. The role of abnorm al neural oscillation s in
the pathoph ysiology of co-occurr ing Tourette syndrome and attention -deficit/hyp eractivity disorder.
European Child & Adolesce nt Psychiat ry. 2007; 16(1):51–9 . https://d oi.org/10.100 7/s00787 -007-1007 -
3 PMID: 176652 83
6. Gatev P, Darbin O, Wichmann T. Oscillati ons in the basal ganglia under normal condition s and in move-
ment disorders. Movem ent Disorders. 2006; 21(10):156 6–77. https://doi.or g/10.1002 /mds.21033
PMID: 168303 13
7. Voorn P, Vandersc huren LJ, Groenewege n HJ, Robbins TW, Penna rtz CM. Putting a spin on the dor-
sal–ventra l divide of the striatum. Trends in neuroscie nces. 2004; 27(8):468– 74. https://doi. org/10.
1016/j.tin s.2004.06.0 06 PMID: 15271494
8. Birba A, Garcı ´ a-Cordero I, Kozono G, Legaz A, Iba ´ ñez A, Sedeño L, et al. Losing ground: frontostr iatal
atrophy disrupts language embodime nt in Parkinson’s and Huntington ’s disease. Neuroscienc e & Bio-
behavio ral Reviews. 2017; 80:673–87.
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 25 / 29
9. Leh SE, Ptito A, Chakrav arty MM, Strafella AP. Fronto-st riatal connect ions in the human brain: a proba-
bilistic diffusion tractogr aphy study. Neurosc ience letters. 2007; 419(2):113 –8. https://doi.o rg/10.1016/j.
neulet.200 7.04.049 PMID: 174851 68
10. Ferry AT, O
¨
ngu ¨ r D, An X, Price JL. Prefrontal cortical projections to the striatum in macaque monkeys :
evidence for an organization related to prefrontal networks. Journal of Comparative Neurolo gy. 2000;
425(3):447 –70. https:// doi.org/10.10 02/1096-986 1(200009 25)425:3<447::a id-cne9>3.0. co;2-v PMID:
10972944
11. O
¨
ngu ¨ r D, Price JL. The Organizat ion of Networks within the Orbital and Medial Prefrontal Cortex of
Rats, Monkey s and Humans . Cerebral Cortex. 2000; 10(3):206– 19. https://doi.or g/10.109 3/cercor/10.
3.206 PMID: 10731217
12. Hintiryan H, Foster NN, Bowman I, Bay M, Song MY, Gou L, et al. The mouse cortico-str iatal projec-
tome. Nature Neurosc ience. 2016; 19:1100. https://doi.o rg/10.1038/nn .4332 https:// www.natur e.com/
articles/nn .4332#su pplementa ry-information . PMID: 27322419
13. Simonyan K, Ju ¨ rgens U. Efferent subcortical projections of the laryngeal motorcorte x in the rhesus mon-
key. Brain Research. 2003; 974(1):43– 59. https://doi.or g/10.1016/ S0006-899 3(03)0254 8-4.
14. Ju ¨ rgens U. Affere nts to the cortical larynx area in the monkey. Brain Research. 1982; 239(2):377 –89.
https://doi.or g/10.101 6/0006-8993 (82)90516 -9 PMID: 7093697
15. Petkov C, Jarvis E. Birds, primates, and spoken language origins: behavio ral phenotyp es and neurobio-
logical substrates . Frontiers in Evolutio nary Neuroscience . 2012; 4:12. https:// doi.org/10.33 89/fnevo.
2012.00012 PMID: 22912615
16. Vargha-K hadem F, Gadian DG, Copp A, Mishkin M. FOXP2 and the neuroanatom y of speech and lan-
guage. Nature Reviews Neuroscienc e. 2005; 6(2):131. https://doi.o rg/10.1038/nr n1605 PMID:
15685218
17. Robles SG, Gatignol P, Capelle L, Mitchell M, Duffau H. The role of dominan t striatum in language: a
study using intraopera tive electrical stimulations . Journal of Neurolo gy, Neurosur gery & Psychiat ry.
2005; 76(7):940– 6.
18. Holland R, Leff AP, Josephs O, Galea JM, Desikan M, Price CJ, et al. Speech facilitatio n by left inferior
frontal cortex stimulation. Current Biology. 2011; 21(16):140 3–7. https://doi.or g/10.1016/ j.cub.2011. 07.
021 PMID: 218203 08
19. Schwartz CP, Smotherm an MS. Mapping vocalization -related immediate early gene expression in
echolocati ng bats. Behavioural brain research. 2011; 224(2):358 –68. https://doi.or g/10.101 6/j.bbr.
2011.06. 023 PMID: 21726584
20. Tressler J, Schwartz C, Wellman P, Hughes S, Smother man M. Regulatio n of bat echolocati on pulse
acoustics by striatal dopamin e. The Journal of Experime ntal Biology. 2011; 214(19):32 38. https://doi.
org/10.1242/ jeb.058149 PMID: 219004 71
21. Jarvis ED. Neural systems for vocal learning in birds and humans: a synopsis . J Ornithol. 2007; 148
(1):35–44. https://doi.o rg/10.1007/s1 0336-007-0 243-0 PMID: 19684872.
22. Kajikawa Y, Schroeder Charles E. How Local Is the Local Field Potential? Neuron. 2011; 72(5):847– 58.
https://doi.or g/10.101 6/j.neuron.20 11.09.02 9 PMID: 22153379
23. Sengupta R, Nasir SM. The predictive roles of neural oscillation s in speech motor adaptability . Journal
of Neuroph ysiology. 2016; 115(5):251 9–28. https://doi.or g/10.1152/ jn.00043.2016 PMID: 26936976
24. Lewandows ki BC, Schmidt M. Short bouts of vocalization induce long-lasting fast gamma oscillation s in
a sensorimoto r nucleus. Journal of Neurosc ience. 2011; 31(39):139 36–48. https://doi.or g/10.152 3/
JNEUROS CI.6809-1 0.2011 PMID: 219572 55
25. Fries P. Rhythms for Cognition : Commun ication through Coherence . Neuron. 2015; 88(1):220– 35.
https://doi.or g/10.101 6/j.neuron.20 15.09.03 4 PMID: 26447583
26. Bressler SL, Kelso JAS. Cortical coordination dynamic s and cognition . Trends in Cognitive Sciences.
2001; 5(1):26–36 . https:/ /doi.org/10.10 16/s1364 -6613(00) 01564-3 PMID: 11164733
27. Von Stein A, Sarnthein J. Different freque ncies for different scales of cortical integra tion: from local
gamma to long range alpha/th eta synchronizati on. International journal of psychophy siology. 2000; 38
(3):301–13 . https://doi. org/10.1016/s 0167-8760( 00)00172-0 PMID: 11102669
28. Buzsa ´ ki G, Draguhn A. Neuronal oscillation s in cortical networks. science . 2004; 304(5679) :1926–9.
https://doi.or g/10.112 6/science.109 9745 PMID: 15218136
29. Schroeder CE, Lakatos P. Low-frequenc y neuronal oscillation s as instrumen ts of sensory selection.
Trends in neuroscie nces. 2009; 32(1):9–18 . https://doi.or g/10.1016/ j.tins.2008. 09.012 PMID:
19012975
30. Narayanan NS, Cavanagh JF, Frank MJ, Laubach M. Common medial frontal mechanis ms of adaptive
control in humans and rodent s. Nature neuroscienc e. 2013; 16(12):188 8–95. Epub 2013/10/20. https://
doi.org/10.10 38/nn.3549 PMID: 241413 10.
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 26 / 29
31. Mahjoory K, Cesnaite E, Hohlefeld FU, Villringer A, Nikulin VV. Power and temporal dynamics of alpha
oscillation s at rest differentiate cognitive performanc e involving sustained and phasic cognitive control.
NeuroImage . 2019; 188:135–44. https:// doi.org/10.10 16/j.neu roimage.2018.1 2.001 PMID: 30517844
32. Stenner M-P, Litvak V, Rutledge RB, Zaehle T, Schmitt FC, Voges J, et al. Cortical drive of low-fre-
quency oscillation s in the human nucleus accumbens during action selection. Journal of Neuroph ysiol-
ogy. 2015; 114(1):29– 39. https://doi.o rg/10.1152/jn .00988.2 014 PMID: 25878159
33. Arnal LH, Doelling KB, Poeppel D. Delta–beta coupled oscillation s underlie temporal prediction accu-
racy. Cerebral Cortex. 2014; 25(9):3077 –85. https://doi.or g/10.109 3/cercor/bhu10 3 PMID: 24846147
34. Wiener M, Parikh A, Krakow A, Coslett HB. An intrinsic role of beta oscillation s in memory for time esti-
mation. Scientific reports. 2018; 8(1):7992. https:// doi.org/10.10 38/s4159 8-018-263 85-6 PMID:
29789611
35. Engel AK, Fries P. Beta-band oscillation s—signal ling the status quo? Current Opinion in Neurobiology .
2010; 20(2):156– 65. https://doi.or g/10.1016/ j.conb.2010. 02.015 PMID: 20359884
36. Khanna P, Carmena JM. Beta band oscillation s in motor cortex reflect neural population signals that
delay movem ent onset. Elife. 2017; 6:e2457 3. https://doi.or g/10.7554 /eLife.24573 PMID: 284673 03
37. Bartolo R, Prado L, Merchant H. Informatio n processing in the primate basal ganglia during sensory-
guided and internally driven rhythmic tapping. Journal of Neuroscience. 2014; 34(11):391 0–23. https://
doi.org/10.15 23/JNEURO SCI.2679-1 3.2014 PMID: 24623769
38. Singh A. Oscillato ry activity in the cortico-b asal ganglia-tha lamic neural circuits in Parkinson’s disease.
European Journal of Neurosc ience. 2018; 48(8):286 9–78. https://doi.or g/10.111 1/ejn.13853 PMID:
29381817
39. An K-m, Ikeda T, Yoshimur a Y, Hasegaw a C, Saito DN, Kumazaki H, et al. Altered Gamma Oscillations
during Motor Control in Children with Autism Spectrum Disorder. The Journal of Neurosc ience. 2018;
38(36):787 8. https://do i.org/10.1523 /JNEUROS CI.1229-1 8.2018 PMID: 30104338
40. Cho-Hisam oto Y, Kojima K, Brown EC, Matsuzaki N, Asano E. Cooing- and babbling-r elated gamma-
oscillation s during infancy: Intracran ial record ing. Epilepsy & Behavio r. 2012; 23(4):494– 6. https://doi.
org/10.1016/ j.yebeh.201 2.02.012.
41. Kingyon J, Behroozm and R, Kelley R, Oya H, Kawasak i H, Narayanan NS, et al. High-ga mma band
fronto-tem poral coherence as a measure of functional connectiv ity in speech motor control. Neurosci-
ence. 2015; 305:15–25. https:/ /doi.org/10.10 16/j.neu roscience.2 015.07.06 9 PMID: 26232713
42. Gunji A, Ishii R, Chau W, Kakigi R, Pantev C. Rhythmic brain activities related to singing in humans.
NeuroImage . 2007; 34(1):426– 34. https://doi.or g/10.101 6/j.neuroimag e.2006.07.018 PMID: 17049276
43. Teeling EC, Scally M, Kao DJ, Romagnoli ML, Springer MS, Stanhope MJ. Molecular evidence regard-
ing the origin of echolocati on and flight in bats. Nature. 2000; 403(6766) :188. https:/ /doi.org/10.10 38/
35003188 PMID: 10646602
44. Chaverri G, Ancillotto L, Russo D. Social commu nication in bats. Biological Reviews. 2018; 93(4):1938 –
54. https://doi. org/10.1111/b rv.12427 PMID: 29766650
45. Salles A, Bohn KM, Moss CF. Auditory commu nication processing in bats: What we know and where to
go. Behavio ral neuroscie nce. 2019; 133(3):305 . https://doi.o rg/10.1037/bn e0000308 PMID: 31045392
46. Fenzl T, Schuller G. Dissimila rities in the vocal control over commu nication and echolocati on calls in
bats. Behavioural Brain Research. 2007; 182(2):173 –9. https://doi.or g/10.1016/ j.bbr.2006.12 .021
PMID: 172276 83
47. Fenzl T, Schuller G. Echoloca tion calls and communicat ion calls are controlled differe ntially in the brain-
stem of the bat Phyllostomu s discolor. BMC Biology. 2005; 3(1):17. https://doi.or g/10.1186/ 1741-7007-
3-17 PMID: 16053533
48. Kothari NB, Wohlgemu th MJ, Moss CF. Dynamic representatio n of 3D auditory space in the midbrai n of
the free-flying echolocat ing bat. Elife. 2018; 7:e2905 3. https://doi.or g/10.755 4/eLife.29053 PMID:
29633711
49. Kawasaki M, Margolias h D, Suga N. Delay-tune d combinatio n-sensitive neurons in the auditory cortex
of the vocalizing mustach ed bat. Journal of neurophys iology. 1988; 59(2):623– 35. https://doi.or g/10.
1152/jn.19 88.59.2.623 PMID: 3351577
50. Metzner W. A possible neuronal basis for Doppler-shif t compensation in echo-loca ting horsesho e bats.
Nature. 1989; 341(6242) :529. https:// doi.org/10.10 38/3415 29a0 PMID: 2797179
51. Wohlgemu th MJ, Yu C, Moss CF. 3D Hippocampal Place Field Dynamics in Free-Flying Echoloca ting
Bats. Frontiers in Cellular Neurosc ience. 2018; 12(270). https:// doi.org/10.33 89/fncel.20 18.0027 0
PMID: 301906 73
52. Eiermann A, Esser K-H. Auditory responses from the frontal cortex in the short-ta iled fruit bat Carollia
perspicillat a. Neuroreport. 2000; 11(2):421– 5. https://doi.or g/10.109 7/00001756- 200002070- 00040
PMID: 106744 99
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 27 / 29
53. Kanwal JS, Gordon M, Peng JP, Heinz-Esser K. Auditory response s from the frontal cortex in the mus-
tached bat, Pteronotus parnellii. Neurore port. 2000; 11(2):367– 72. https://doi.or g/10.1097/ 00001756-
200002070- 00029 PMID: 10674488
54. Kobler JB, Isbey SF, Cassed ay JH. Auditory pathways to the frontal cortex of the mustache bat, Ptero-
notus parnellii. Science. 1987; 236(4803) :824–6. https://doi.or g/10.112 6/science.243 7655 PMID:
2437655
55. Laubach M, Amaran te LM, Swanson K, White SR. What, if anything, is rodent prefront al cortex?
Eneuro. 2018; 5(5).
56. Seaman s JK, Lapish CC, Durstewi tz D. Comparing the prefrontal cortex of rats and primates: insights
from electrop hysiology. Neurotoxic ity research . 2008; 14(2–3):24 9–62. https://d oi.org/10.100 7/
BF03033814 PMID: 19073430
57. Thies W, Kalko EK, Schnitzler H-U. The roles of echolocati on and olfaction in two Neotropica l fruit-eat-
ing bats, Carollia perspicillat a and C. castanea , feeding on Piper. Behavioral Ecology and Sociobiology .
1998; 42(6):397– 409.
58. Hechava rrı ´ a JC, Beetz MJ, Macias S, Ko ¨ ssl M. Distres s vocalization sequences broadca sted by bats
carry redundant information. Journal of Comparative Physiolog y A. 2016; 202(7):503 –15.
59. Kno ¨ rnschild M, Feifel M, Kalko EKV. Male courtship displays and vocal commu nication in the polygy-
nous bat Carollia perspicillat a. 2014; 151(6):781 . https://doi. org/10.1163/1 568539X-0 000317 1.
60. Romano J, Kromrey JD, Coraggi o J, Skowrone k J, editors. Appropria te statistic s for ordinal level data:
Should we really be using t-test and Cohen’sd for evaluatin g group differe nces on the NSSE and other
surveys. annual meeting of the Florida Association of Institutiona l Research; 2006.
61. Radulescu E, Minati L, Ganesh an B, Harrison NA, Gray MA, Beache r FD, et al. Abnormalitie s in fronto-
striatal connectiv ity within language networks relate to differences in grey-matte r heterogene ity in
Asperger syndrome. NeuroIm age: Clinical. 2013; 2:716–26.
62. Fries P, Nikolić D, Singer W. The gamma cycle. Trends in Neurosc iences. 2007; 30(7):309– 16. https://
doi.org/10.10 16/j.tins.20 07.05.005 PMID: 175558 28
63. Engel AK, Fries P, Singer W. Dynamic predicti ons: Oscillati ons and synchrony in top–down processing .
Nature Reviews Neuroscience. 2001; 2(10):704– 16. https://doi.or g/10.103 8/35094565 PMID:
11584308
64. Giraud A-L, Poeppel D. Cortical oscillation s and speech processing : emergin g computation al principles
and operations . Nature Neurosc ience. 2012; 15(4):511 –7. https://doi.or g/10.103 8/nn.3063 PMID:
22426255
65. Lakatos P, Karmos G, Mehta AD, Ulbert I, Schroeder CE. Entrainment of Neurona l Oscillations as a
Mechanism of Attentional Selectio n. Science. 2008; 320(5872) :110. https:// doi.org/10.11 26/scienc e.
1154735 PMID: 18388295
66. Womelsdor f T, Everling S. Long-Range Attentio n Networks: Circuit Motifs Underlyin g Endogenously
Controlle d Stimulus Selectio n. Trends in Neurosciences . 2015; 38(11):682 –700. https:// doi.org/10.
1016/j.tin s.2015.08.0 09 PMID: 26549883
67. Gonzalez -Burgos G, Lewis DA. GABA Neurons and the Mechanism s of Networ k Oscillations : Implica-
tions for Underst anding Cortical Dysfunct ion in Schizophrenia . Schizoph renia Bulletin. 2008; 34
(5):944–61 . https://doi. org/10.1093/s chbul/sbn0 70 PMID: 18586694
68. Bollimunta A, Chen Y, Schroe der CE, Ding M. Neurona l Mechanism s of Cortical Alpha Oscillations in
Awake-B ehaving Macaques . The Journal of Neurosc ience. 2008; 28(40):997 6. https://doi.or g/10.152 3/
JNEUROS CI.2699-0 8.2008 PMID: 188299 55
69. Sun W, Dan Y. Layer-sp ecific network oscillation and spatiotem poral receptive field in the visual cortex.
Proceedings of the National Academy of Sciences. 2009; 106(42):17 986. https://doi.or g/10.107 3/pnas.
0903962106 PMID: 19805197
70. McCarthy MM, Moore-Koch lacs C, Gu X, Boyden ES, Han X, Kopell N. Striata l origin of the pathologic
beta oscillation s in Parkinso n&#039;s disease. Procee dings of the National Academy of Sciences.
2011; 108(28):11 620. https://doi.or g/10.1073/ pnas.1107748 108 PMID: 21697509
71. Fernandez AA, Fasel N, Kno ¨ rnschild M, Richner H. When bats are boxing: aggressive behavio ur and
communic ation in male Seba’s short-tailed fruit bat. Animal Behaviour. 2014; 98:149– 56. https://doi.
org/10.1016/ j.anbehav.2 014.10.011.
72. Clement M, Kanwal J. Simple Syllabic Calls Accom pany Discrete Behavior Patterns in Captive Pterono-
tus parnellii: An Illustrati on of the Motivation- Structur e Hypothesis. TheScientific WorldJournal . 2012;
2012:12869 5. https://doi.or g/10.1100 /2012/128695 PMID: 226934 29
73. Garcı ´ a-Rosales F, Beetz MJ, Cabral- Calderin Y, Ko ¨ ssl M, Hechav arria JC. Neurona l coding of multi-
scale temporal feature s in communic ation sequences within the bat auditory cortex. Commun ications
biology. 2018; 1(1):200.
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 28 / 29
74. Garcı ´ a-Rosales F, Martin LM, Beetz MJ, Cabral- Calderin Y, Ko ¨ ssl M, Hechav arria JC. Low-Freq uency
Spike-Field Coheren ce Is a Fingerprin t of Periodicity Coding in the Audito ry Cortex. iScience. 2018;
9:47–62. https://doi.or g/10.1016/j. isci.2018.10 .009 PMID: 3038413 3
75. Harris KD, Mrsic-Floge l TD. Cortical connectivity and sensory coding. Nature. 2013; 503(7474): 51.
https://doi.or g/10.103 8/nature1265 4 PMID: 24201278
76. Fujioka T, Trainor LJ, Large EW, Ross B. Internaliz ed Timing of Isochrono us Sounds Is Represente d in
Neuromagn etic Beta Oscillations . The Journal of Neurosc ience. 2012; 32(5):1791 . https://doi.or g/10.
1523/JNEU ROSCI.4107 -11.2012 PMID: 22302818
77. Cagnan H, Mallet N, Moll CKE, Gulberti A, Holt AB, Westphal M, et al. Tempora l evolution of beta bursts
in the parkinson ian cortical and basal ganglia network. Proceedings of the National Academy of Sci-
ences. 2019; 116(32):16 095. https://doi.or g/10.1073/ pnas.1819975 116 PMID: 31341079
78. Zhang W, Yartsev MM. Correlated Neural Activity across the Brains of Socially Interacting Bats. Cell.
2019.
79. Medvedev AV, Kanwal JS. Commun ication call-evoked gamm a-band activity in the auditory cortex of
awake bats is modified by complex acoustic feature s. Brain research. 2008; 1188:76–86. https://doi.
org/10.1016/ j.brainres.20 07.10.08 1 PMID: 18054896
80. Van Der Meer MA, Redish AD. Covert expectation -of-reward in rat ventral striatum at decision points.
Frontiers in integrat ive neuroscie nce. 2009; 3:1. https://doi.or g/10.338 9/neuro.07.00 1.2009 PMID:
19225578
81. Beetz MJ, Garcı ´ a-Rosales F, Ko ¨ ssl M, Hecha varrı ´ a JC. Robustnes s of cortical and subcortical process-
ing in the presence of natural masking sounds. Scientifi c reports. 2018; 8(1):6863. https://doi.or g/10.
1038/s41 598-018-2 5241-x PMID: 297172 58
82. Garcı ´ a-Rosales F, Ro ¨ hrig D, Weineck K, Ro ¨ hm M, Lin Y-H, Cabral- Calderin Y, et al. Laminar specificity
of oscillator y coheren ce in the auditory cortex. Brain Structure and Function. 2019:1– 18.
83. Hechava rrı ´ a JC, Beetz MJ, Macias S, Ko ¨ ssl M. Vocal sequences suppress spiking in the bat auditory
cortex while evoking concomit ant steady-state local field potentials. Scientifi c reports . 2016; 6:39226.
https://doi.or g/10.103 8/srep39226 PMID: 27976691
84. Martin LM, Garcı ´ a-Rosales F, Beetz MJ, Hechav arrı ´ a JC. Processin g of temporally patterned sounds in
the auditory cortex of Seba’s short-tailed bat, Carollia perspicillata. European Journal of Neuroscienc e.
2017; 46(8):2365 –79. https://doi.or g/10.1111/ ejn.13702 PMID: 2892174 2
85. Bokil H, Andrews P, Kulkarni JE, Mehta S, Mitra PP. Chronux: a platfor m for analyzing neural signals.
Journal of neuroscie nce methods. 2010; 192(1):146 –51. https:// doi.org/10.10 16/j.jne umeth.201 0.06.
020 PMID: 206378 04
86. Yger P, Spampinat o GL, Esposito E, Lefebvre B, Deny S, Gardella C, et al. A spike sorting toolbox for
up to thousand s of electrod es validated with ground truth recordings in vitro and in vivo. Elife. 2018; 7:
e34518. https:// doi.org/10.75 54/eLife .34518 PMID: 29557782
87. Berens P. CircStat: a MATLAB toolbox for circular statistics. J Stat Softw. 2009; 31(10):1–2 1.
PLOS BIOL OGY
Neural correlat es of vocal control in bats
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000658 March 19, 2020 29 / 29
