# ohmae-2022-cerebellar-rhythm

ARTICLE
Neural signals regulating motor synchronization in
the primate deep cerebellar nuclei
Ken-ichi Okada 1,2, Ryuji Takeya 1,2 & Masaki Tanaka 1 ✉
Movements synchronized with external rhythms are ubiquitous in our daily lives. Despite the
involvement of the cerebellum, the underlying mechanism remains unclear. In monkeys
performing synchronized saccades to periodically alternating visual stimuli, we found that
neuronal activity in the cerebellar dentate nucleus correlated with the timing of the next
saccade and the current temporal error. One-third of the neurons were active regardless of
saccade direction and showed greater activity for synchronized than for reactive saccades.
During the transition from reactive to predictive saccades in each trial, the activity of these
neurons coincided with target onset, representing an internal model of rhythmic structure
rather than a speci ﬁc motor command. The behavioural changes induced by electrical sti-
mulation were explained by activating different groups of neurons at various strengths,
suggesting that the lateral cerebellum contains multiple functional modules for the acquisi-
tion of internal rhythms, predictive motor control, and error detection during synchronized
movements.
https://doi.org/10.1038/s41467-022-30246-2 OPEN
1 Department of Physiology, Hokkaido University School of Medicine, Sapporo 060-8638, Japan. 2These authors contributed equally: Ken-ichi Okada, Ryuji
Takeya. ✉email: masaki@med.hokudai.ac.jp
NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications 1
1234567890():,;
S
ynchronized movements to periodic events, such as dancing
to music or clapping hands, are common in daily life. Such
movements require information processing in the sensor-
imotor areas in the cerebral cortex, the basal ganglia, and the
cerebellum
1–4. In particular, when the cerebellum is damaged,
rhythmic movements cannot be performed with a precision of
tens to hundreds of milliseconds 5,6. This is not surprising since
the cerebellum is involved in regulating the timing of contraction
of multiple muscles during motor execution, thereby enabling
coordinated movements 7,8. The cerebellum has also been shown
to be important in the initiation of movement, especially its
timing9–11. In theories of motor control, the essential role of the
cerebellum is to generate internal models that allow for predictive
motor control 12. The internal models are formed by experience
and updated through learning to maintain accurate movement 13.
This adaptive learning mechanism by the cerebellum optimizes
not only the magnitude and direction of movement 14–16 but also
its timing 17,18.
In addition to motor control, when synchronizing with exter-
nal rhythms, it is also necessary to detect the periodicity of events
and make sensory predictions accordingly. The importance of the
basal ganglia in such processes has long been recognized. Evi-
dence from clinical cases 19,20, functional imaging with non-motor
rhythmic tasks 21,22, and physiological experiments in
primates23,24 all suggest a role for the basal ganglia in beat-based
timing25. Recent studies have also shown that the cerebellum is
involved in rhythm processing. For example, studies using
magnetoencephalography26 and experimental animals 27,28 have
demonstrated that rhythm perception without movement
involves periodic entrainment of neuronal activity in the cere-
bellum and its connected brain regions. Such activities might be
related to temporal attention 29,30. Furthermore, the cerebellum
has been shown to be involved in predicting the trajectory of
visual stimuli in the absence of movement, indicating that the
cerebellum also generates internal forward models for purely
sensory events 31–33. Thus, the cerebellum is likely to be respon-
sible for information processing necessary for synchronized
movements, including sensory prediction of periodic events,
predictive motor control based on these internal representations,
and error monitoring for updating the forward models. Since the
cerebellum forms loop circuits with various areas in the cerebral
cortex and therefore contains multiple functional modules
34–36,i t
is possible that these functions are processed in parallel through
the relevant networks. However, it remains largely unknown how
the cerebellum represents and processes information for syn-
chronized movements.
The present study aimed to investigate this in monkeys per-
forming a series of predictive saccades to targets that alternately
appeared on the left and right at regular intervals. Although
predictive movements synchronized with external rhythms were
previously thought to be behaviours speci ﬁc to vocal learning
species such as humans, songbirds, and dolphins 37, it has recently
been shown that monkeys also perform synchronized movements
when reinforced with immediate rewards 38,39. Human functional
imaging studies using a similar task have reported increased
regional blood ﬂow in the cerebellar crus I during predictive
(synchronized) saccades compared to reactive saccades 40.W e
examined single neuron activity during synchronized saccades
from the posterior portion of the cerebellar dentate nucleus,
which receives input from the lateral lobules of the cerebellum
and is involved in self-initiated eye movements 41,42. We found
that many neurons exhibited activity correlated with saccade
timing and temporal errors, and some responded to eye move-
ments in both directions with enhanced activity during predictive
synchronized saccades. The results of electrical stimulation
applied to the recording sites indicated that these signals were
causally related to the timing of synchronized movements. The
posterior portion of the cerebellar dentate nucleus may be part of
multiple functional modules involved in the acquisition of
internal rhythms, predictive motor control, and error detection.
Results
Animal behaviour. In the synchronized (predictive) saccade task,
red saccade targets were alternately presented within horizontally
arranged landmarks (white square contours) at a ﬁxed interval
(stimulus onset asynchrony or SOA, Fig. 1a). The SOA was
randomly selected from 400, 550, and 700 ms for each trial and
remained constant during the 12-s trial interval. Since monkeys
do not spontaneously generate synchronized saccades to periodic
stimuli43, we rewarded them for every three saccades within
±20% SOA from target presentation to reinforce predictive
movements (Fig. 1b, red shadings) 38. As a control, a reactive
saccade task was randomly mixed into the block of trials. In this
task, the saccade targets were green, and the duration of each
target presentation was randomly selected from 400, 550, and
700 ms. A liquid reward was given for every three reactive sac-
cades (reaction time >100 ms, Fig. 1b, blue shadings).
Fig. 1c plots the temporal error between the stimulus onset and
saccade (i.e., saccade latency for reactive saccades) for each
condition during the recording experiment in monkey I. In the
synchronized saccade task, the temporal error decreased rapidly
within a few seconds for all SOAs, indicating that the animal
detected rhythmic structure and predictively generated synchro-
nized saccades to the stimulus (Supplementary Movies 1 and 2).
In the reactive task, however, the temporal error remained almost
unchanged throughout the trial. The latency of the ﬁrst saccade in
the sequence during the recording sessions averaged 305 ± 100 ms
(s.d., monkey I) and 291 ± 51 ms (monkey J), while that of the
tenth saccade averaged −11 ± 79 ms (monkey I) and −16 ± 87 ms
(monkey J) for the synchronized saccade trials and 307 ± 50 ms
(monkey I) and 313 ± 73 ms (monkey J) for the reactive saccade
trials. Thus, both animals were able to ﬂexibly adjust saccade
timing for each task depending on the reward conditions.
Classiﬁcation of neurons and recording sites . During these
behavioural tasks, we recorded activity from single neurons
responding to saccades in the posterior part of the cerebellar
dentate nucleus (Fig. 1d, Supplementary Fig. 1a for all neurons).
Quantitative analysis was performed on 95 neurons ( n = 72 and
23 for monkeys I and J, respectively) for which we were able to
examine neuronal activity with a suf ﬁcient number (>200) of
synchronized saccades. Many of these neurons increased their
activity prior to synchronized saccades in one (Supplementary
Movie 1) or both directions (Supplementary Movie 2), while the
other neurons increased their activity after the saccades. All
neurons showed signi ﬁcant changes in activity for saccade
direction, the relative time to saccades (± 200 ms), or their
interaction (two-way ANOVA, P < 0.05). To classify them, a
cluster analysis was performed based on the data of each neuron
aligned with the synchronized saccades in the 550 ms SOA con-
dition (Fig. 2a, Supplementary Fig. 2a). Approximately 35%
(n = 33/95) of the neurons exhibited increased activity before
saccades in both directions (Bilateral neurons). An equal number
of neurons showed clear directional selectivity, with increased
activity before saccades ipsilateral ( n = 24) or contralateral
(n = 9) to the recording side (Unilateral neurons). The remaining
31% ( n = 29/95) showed activity mainly after saccades (Post-
saccade neurons). When we performed one-way ANOVAs with
three factors to compare the ﬁring rate at speci ﬁc intervals rather
than the time course of activity, 89% ( n = 85/95) of neurons
discriminated the direction of saccades and 60% ( n = 57/95) of
ARTICLE NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2
2 NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications
neurons signiﬁcantly modulated their activity by the SOA or task
condition (Supplementary Fig. 2b).
To characterize the properties of the three types of neurons, we
ﬁrstly calculated the directional index (DI, Methods) for the data of
550 ms SOA. Unilateral neurons showed strong directional selectivity
(−0.82 ± 0.13, s.d. and 0.73 ± 0.19 for neurons with contralateral and
ipsilateral preferences, respect ively), while Bilateral neurons
(−0.08 ± 0.31) and Postsaccade neurons (−0.16 ± 0.46) showed only
weak directional modulation (Supplementary Fig. 3a). The distribu-
tion of the DI did not differ betwe en the Bilateral and Postsaccade
neurons (Tukey test, P = 0.78), while Unilateral neurons showed a
different distribution from the others ( P < 0.01). When the mutual
information (MI) was computed to quantify the directional selectivity
for each neuron (Supplementary Methods), the MI and DI correlated
well ( r = 0.94), and similar results wer e obtained (Supplementary
Fig. 3d).
We also found that the time course of preparatory activity
differed between groups, with the peak timing of Unilateral
neurons ( −140 ± 76 ms, s.d.) being preceded by saccades to a
greater degree than that of Bilateral neurons ( −58 ± 87 ms,
unpaired t-test, t63 = 4.06, P = 0.0001, Supplementary Fig. 3b).
To further assess the time course of preparatory activity, the
timing and magnitude of peak activity and the slope of ramping
activity were compared across SOAs (Supplementary Fig. 4).
Although many individual neurons showed signi ﬁcant changes
for different SOAs, the time course of the population activity of
Bilateral neurons exhibited a signi ﬁcant change only in the slope
of ramping activity and that of Unilateral neurons in the slope
and peak timing. When the preparatory activity was temporally
scaled, the time course of activity for different SOAs appeared to
be very similar for both types of neurons (Supplementary Fig. 4c).
The temporal scaling of preparatory activity was consistent with
the previous studies in the medial frontal cortex 44–46 and
striatum46,47, as well as those in the cerebellum in the range of
hundreds of milliseconds 42.
The recording sites of these groups of neurons differed in
the dorsoventral direction (one-way ANOVA, F3,94 = 6.14,
P = 0.0008, Supplementary Fig. 1b) but not in the anteroposterior
(F3,94 = 1.22, P = 0.31) and mediolateral directions ( F3,94 = 1.96,
P = 0.13). Postsaccade neurons and Unilateral neurons with a
contralateral directional preference were predominantly distrib-
uted dorsally in the dentate nucleus, while Unilateral neurons
with an ipsilateral preference and Bilateral neurons were widely
distributed. This suggests that these neurons may send informa-
tion to different areas in the brain and are involved in different
aspects of behavioural control.
Enhancement during motor synchronization . Previous func-
tional imaging studies have shown that cerebellar activity
increases during synchronized eye movements 40. We also found
that some neurons in the cerebellar nuclei exhibited differential
activity between the synchronized (predictive) and reactive sac-
cades. In the example Bilateral neuron shown in Fig. 2b, the
activity was greater during synchronized than reactive saccades.
In contrast, in the case of the Unilateral neuron shown in Fig. 2c,
the activity before ipsilateral saccades was comparable between
the conditions. To compare the activity of individual neurons
between conditions, the prediction index (PI) was calculated for
each neuron during saccades in the preferred direction (550 ms
SOA, Methods). The PI is positive if the ﬁring modulation for
synchronized saccades is greater than that for reactive saccades,
and negative in the opposite case. The PI averaged 0.10 ± 0.16
(s.d.), 0.01 ± 0.09, and 0.03 ± 0.11 for Bilateral, Unilateral, and
Postsaccade neurons, respectively, and only the PIs for Bilateral
neurons were signi ﬁcantly greater than zero (one sample t-test,
Eye
14 deg
500 ms
Target
Synchronized task
Reactive task
400
0
Temporal error (ms)
Time from the first target (s)
Reactive
400
700
048 1 2
b c
d
Synchronized
550
P7 P6
P8
P9
P7
2 mm
6 mm
Anterior
Posterior
TE
ISI
Fixation 1st 2nd
Time
3rd 4th 5th
a
Fig. 1 Behavioural paradigm and recording sites. a Saccade targets were
presented alternately at landmarks (white squares, 14° apart) that were
visible throughout each trial. In the synchronized (predictive) condition, a
red saccade target appeared for a ﬁxed interval (stimulus onset asynchrony
or SOA) of 400, 550, or 700 ms (constant in each trial), and monkeys
were rewarded for predictive saccades (±20% SOA). In the reactive
condition, a green target was presented for a random duration, and reactive
saccades (reaction time > 100 ms) were reinforced. These conditions were
randomly interleaved during each recording session. In both conditions, the
stimulus sequence lasted for 12 or 8 s. b Sample traces of eye and target
positions. Red and blue shadings represent spatiotemporal windows for
correct saccades. A liquid reward was given after a random time period
(0–600 ms) following three consecutive correct responses. Arrows
indicate two temporal parameters of saccades. ISI, inter-saccadic interval;
TE, temporal error. The behavioural performance in representative
recording sessions is shown in Supplementary Movies 1 and 2. c Temporal
error (or saccade latency) as a function of stimulus timing in a single
recording session. For the reactive condition (blue symbols), data for all
target sequences with different SOAs are averaged and plotted every
550 ms. Data from multiple trials are shown as mean ± s.d. ( n = 36 for the
reactive condition, and n = 36, 37, and 38 trials for the synchronized 400,
550, and 700 ms SOA conditions, respectively). Numerical data are
available in the Source Data ﬁle. d Histological sections and recording sites
in monkey I. Outlines of the dentate nucleus in coronal sections are shown
for different posterior locations (P) from the interaural line. Red, green, and
blue circles indicate the recording sites of Bilateral, Unilateral, and
Postsaccade neurons, respectively. Stars ( ☆) indicate electrolytic marking
lesions. The scale bar in the drawing is common to the enlarged image. A
3-D plot of recording sites in stereotaxic coordinates for all neurons and the
depth from the dorsal surface of the cerebellar nucleus is shown in
Supplementary Fig. 1.
NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2 ARTICLE
NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications 3
t30 = 3.36, P = 0.002). We obtained similar results for different
SOAs, with the PIs for only Bilateral neurons being greater than
zero ( P < 0.02, Supplementary Fig. 5b). These results suggest that
the elevated activity during synchronized saccades found in
previous studies might be related to the increased activity of
Bilateral neurons (Fig. 2a, top panel). We also found a signi ﬁcant
negative correlation between the DI and PI for all neurons
(r = −0.31, P = 0.003, Supplementary Fig. 3c), indicating that
neurons with weak directionality tended to have greater activity
during synchronized saccades than during reactive saccades.
Neural correlations with the next saccade timing and the cur-
rent temporal error . The lateral cerebellum is essential for the
adjustment of saccade timing
42,48. For both the Unilateral neuron
shown in Fig. 3a and the Bilateral neuron in Fig. 3b, the ﬁring rate
during a few hundred milliseconds after a saccade varied with the
timing of the next saccade. To assess the relationship between
neuronal activity and motor timing, we calculated the partial
correlation between the trial-by-trial activity of individual neu-
rons and the inter-saccadic interval (ISI), controlling for the
previous ISI and temporal error in trials with a 550 ms SOA. The
a
Pref sac Opposite
Bilateral
Ipsi pref
400550
700
Synchronized
saccades
Reactive
saccades
PI = 0.36
14 deg
Prediction index (PI)
0–0.6 0.6
CDF
1
0
Bilateral
Unilateral
Postsac
b
d
Postsaccade
Unilateral
Reactive
Normalized
activity
0
1Ipsi sac Contra sac
00–275 275 –275 275
Time (ms)
0
1
00–275 275 –275 275
Time (ms)
0
1Ipsi sac Contra sac
00–275 275 –275 275
10
1
Time (ms)
0–550 550
Time (ms) Time (ms)
Time (ms) Time (ms)
PI = –0.029
1
24
Cell #Cell # Cell #
c
0–550 550
0–550 550 0 –550 550
SOA:
550 ms
Contra pref
150 spk/s100 spk/s
Normalized
activity
Normalized
activity
33
29
n = 91
Synchronized
Fig. 2 Classi ﬁcation of neurons in the dentate nucleus. a Neurons are classi ﬁed into four groups according to the time courses of the normalized ﬁring
rate aligned with saccades in the opposite directions. Each row illustrates the time course of the population activity (mean ± s.e.) and a heatmap of
normalized activity for individual neurons. Yellow and blue indicate higher and lower activity, respectively ( parula colormap, Matlab). Red and blue traces
on each panel indicate the data for synchronized (predictive) saccades and reactive saccades, respectively. Data for neurons exhibiting preparato ry activity
for either saccade direction were combined (Unilateral type). A clustering dendrogram and the results of ANOVA for different conditions are shown in
Supplementary Fig. 2. The directionality of saccade-related responses is summarized in Supplementary Figs. 3a and 5a. Comparison of the time course of
preparatory activity between Bilateral and Unilateral neurons across the SOAs are shown in Supplementary Fig. 4. b Activity of a Bilateral neuron during
synchronized versus reactive saccades. In both panels, the rasters are aligned with ipsilateral saccades for the target with a 550 ms SOA. Green and pu rple
dashed lines on the left panel represent the data for 400 and 700 ms SOAs, respectively. Note the enhancement of activity before synchronized saccades .
c A Unilateral (contralateral preferred) neuron. As in this example, the peak activity of Unilateral neurons preceded saccades by a greater degree tha n that
of Bilateral neurons (Supplementary Fig. 3b). d Comparison of the prediction index (PI) across neuron types. The PI was de ﬁned as ( Pred − Reac)/
(Pred + Reac), where Pred and Reac indicated the ﬁring modulation for predictive and reactive saccades, respectively. The gray histogram represents data
from all neurons. The PI was signi ﬁcantly different from zero for Bilateral neurons only (one sample t-test, two-sided, t30 = 3.36, P = 0.002; Unilateral
neurons, t31 = 0.64, P = 0.53; Postsaccade neurons, t27 = 1.64, P = 0.11). Similar results were obtained from the mutual information analysis
(Supplementary Fig. 3e). The PIs for the other SOAs are shown in Supplementary Fig. 5b. Numeral data are available in the Source Data ﬁle.
ARTICLE NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2
4 NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications
heatmap of the partial correlation coef ﬁcients in Fig. 3c indicates
that most Unilateral neurons showed a negative correlation at
200–400 ms after the saccade in the non-preferred direction. A
comparison of the normalized population activity for one-third of
trials with early and late saccades also showed that the elevated
activity was associated with a shorter ISI (Fig. 3c, top). The same
was true for Bilateral neurons (Fig. 3d), where more than half of
them showed a negative correlation. The time course of the
partial correlation calculated for the three groups of neurons is
shown in Fig. 3e (Supplementary Fig. 5c for the other SOAs). For
both Unilateral and Bilateral neurons, the correlation with the
next saccade timing appeared at approximately 100 ms after
saccades and reached a maximum at ~300 ms, whereas no sig-
niﬁcant correlation was found in Postsaccade neurons. The par-
tial correlation coef ﬁcients 200 –400 ms after saccades averaged
−0.16 ± 0.16 (s.d.) for Unilateral neurons and −0.18 ± 0.24 for
Bilateral neurons, both of which signi ﬁcantly differed from zero
(one sample t-test, two-sided, Unilateral neurons, t
32 = −5.59
P = 3.58 × 10−6; Bilateral neurons, t32 = −4.38, P = 1.20 × 10−4;
Postsaccade neurons, t28 = −1.89, P = 0.07, Fig. 3f). These cor-
relations between neuronal activity and saccade timing were
calculated for saccades in the preferred direction, and similar
results were obtained for saccades in the ipsilateral and con-
tralateral directions for both Unilateral and Bilateral neurons
(Supplementary Fig. 6). In addition, a signi ﬁcant partial correla-
tion was also observed when the data were aligned with the next
saccades (Supplementary Fig. 7b). However, the partial correla-
tion disappeared when the analysis interval was extended back-
ward in time to the previous ISI, indicating that the neuronal
activity may regulate the timing of only the next saccades (Sup-
plementary Fig. 7c).
The cerebellum is also thought to be involved in error
detection, which is necessary for motor learning. We therefore
examined whether neurons in the deep cerebellar nuclei carry
information about temporal errors during synchronized sac-
cades. Both the Postsaccade neuron in Fig. 4a and the Bilateral
neuron in Fig. 4b showed an increase in post-movement
transient activity (inverted triangle) when the saccade preceded
the target (yellow dots). To quantify this, we calculated the
partial correlation between trial-by-trial neuronal activity and
temporal error in individual neurons, controlling for prior ISI in
trials with a 550 ms SOA. The results showed that most
Postsaccade neurons (Fig. 4c) and about half of Bilateral neurons
(Fig. 4d) showed a negative correlation immediately after
saccades in the preferred direction. The time course of the
correlation coef ﬁcients in the three groups of neurons displayed
that these negative correlations were maximal at 100 –200 ms
after saccades and were not observed in Unilateral neurons
(Fig. 4e, Supplementary Fig. 5d for the other SOAs). The partial
correlation coef ﬁcients during 200 ms after saccades averaged
−0.10 ± 0.13 (s.d.) for Postsaccade neurons and −0.07 ± 0.27 for
Bilateral neurons, and only those for Postsaccade neurons were
signiﬁcantly different from zero (one sample t-test, two-sided,
t28 = −4.37, P = 0.0002, Fig. 4f). When the same analysis was
performed for saccades ipsilateral and contralateral to the
recording sites (Supplementary Fig. 8), a signi ﬁcant correlation
was found for Postsaccade neurons during ipsilateral saccades
(t28 = −4.14, P = 2.9 × 10 −4) and for Bilateral neurons during
contralateral saccades ( t32 = −2.48, P = 0.019).
We also performed decoding analysis to see if information
about saccade timing and task condition can be extracted from
each neuron population (Supplementary Methods), and found
that all types of neurons carried signi ﬁcant information of the ISI,
temporal error and other task conditions at different timing
(Supplementary Fig. 9).
0
1
02 0 0 4 0 0
1
0
1
0 200 400
0 200 400 6000 200 400 600
200 spk/s
150 spk/s
–0.5 0.5
Time after saccade (ms) Time after saccade (ms)
Time after saccade (ms) Time after saccade (ms)
Bilateral neuronUnilateral (ipsi) neuron
Unilateral Bilateral
n = 33
n = 33
ab
cd
Cell # Normalized
activity
33
Short
ShortLong
Long
Short
Long
Short
Long
1
33
Partial correlation coefficient
Time after saccade (ms) Partial correlation
n = 33
X = –0.18
P < 0.01
Unilateral
Bilateral
Postsac
ef Correlation with ISI
(preferred direction)
Uni
10 cells
–1.0 0 1.0
n = 33
X = –0.16
P < 0.01
n = 29
X = –0.06
02 0 0 4 0 0
–0.3
0
0.3
Post
Bi P = 0.07
Fig. 3 Neuronal correlates of the timing of the next saccade. a AU n i l a t e r a l
neuron with a preference for ipsilateral saccades. The data are from
synchronized saccade experiments (550 ms SOA) and trials are aligned with
contralateral saccades and sorted by the intersaccadic interval (ISI). Orange
and magenta dots on each raster line indicate the onsets of the contralateral
target and ipsilateral saccade, respectively. Below the raster plot, the time
courses of neuronal activity are separately shown for one-third of trials with
longer ISIs and those with shorter ISIs. Note that ramping activity is more
advanced in trials with shorter ISIs. b A Bilateral neuron (aligned with
ipsilateral saccades).c Heatmap represents the partial correlation coefﬁcient
between the trial-by-trial activity of individual Unilateral neurons and the ISI in
trials with a 550 ms SOA. The partial correlation was computed for every
200 ms window (10 ms step) by controlling the temporal error and previous
ISI (Supplementary Fig. 6a). The above traces show the mean (±s.e.) of
normalized activity in one-third of the trials with short and long ISIs. The same
data aligned with the next saccades are shown in Supplementary Fig. 7b.
d The population activity and partial correlation for individual Bilateral
neurons. e Time courses of the mean (±s.e.) of the partial correlation
coefﬁcients for trials with a 550 ms SOA. The array of coloured dots above
the trace indicates when the correlation coefﬁcients signiﬁcantly differed from
zero (one sample t-test, two-sided, P < 0.05). Gray shading denotes the
interval for quantiﬁcation in f. The data for the other SOAs are shown in
Supplementary Fig. 5c. f Distributions of the correlation coefﬁcients for the
Bilateral, Unilateral, and Postsaccade neurons. Black bars indicate data with
signiﬁcant correlations (permutation test,P < 0.05). The inverted triangle
represents the population mean (X) and theP-value on each panel reports the
result of the two-sided one sample t-test. For this analysis, partial correlation
was computed for the preferred saccade direction. Data for contralateral and
ipsilateral saccades are shown in Supplementary Fig. 6. Numeral data are
available in the Source Data ﬁle.
NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2 ARTICLE
NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications 5
Separation of sensory and motor responses . Recent studies have
shown that the cerebellum is also involved in sensory prediction
without movement execution 27,31. Is the activity of the different
groups of neurons associated with periodic sensory prediction
necessary for synchronized saccades, or solely associated with
motor execution? Since synchronized saccades are made at the
predicted timing of target presentation, it is dif ﬁcult to separate
them. To address this, we focused on neuronal activity during the
transition from reactive to synchronized saccades at the begin-
ning of each trial (Fig. 1c), where sensory prediction may precede
saccade execution.
The Unilateral neuron shown in Fig. 5a displayed strong
activity before leftward saccades, with the peak of the activity
gradually preceding the target as the saccade reaction time
shortened for the ﬁrst, third, and ﬁfth leftward targets (vertical
red lines). In the right panel, the activity aligned with the ﬁrst,
second, third, fourth, and subsequent targets and saccades show
that this neuron consistently exhibited increased activity before
leftward saccades (the second column with orange shading). In
contrast, the Bilateral neuron in Fig. 5b exhibited a transient
decrease in activity after the ﬁrst target onset, followed by an
increase in activity that peaked at the time of the second target
(the ﬁrst vertical blue line). Subsequently, the activity peaked
around the time of the target presentation with some directional
selectivity. When the data were aligned with either target onset or
saccades (right panel), the neuronal activity was more consistent
with the target appearance than with saccade initiation.
To assess whether the activity of each neuron was better
aligned with sensory prediction or saccade, we calculated the
sensorimotor index (SMI, Methods) for the second saccades. The
SMI was negative if the neuronal activity was associated with
saccades and positive if it was associated with the visual stimulus,
and the index was calculated to be −0.90 and 0.27 for the neuron
shown in Fig. 5a and b, respectively. As shown in Fig. 5c, the
SMIs of most Unilateral and Postsaccade neurons were negative,
with means (s.d.) of −0.45 ± 0.34 and −0.33 ± 0.40, respectively.
In Bilateral neurons, about half showed a positive SMI, with a
mean of −0.04 ± 0.41, which was signi ﬁcantly greater than that of
the other types of neurons (Tukey test, P < 0.02). The SMI
calculated for saccades in the non-preferred direction also
differed between Postsaccade and Bilateral neurons (unpaired t-
test, t
46 = 3.52, P = 0.001, Supplementary Fig. 10b). These results
suggest that Bilateral neurons may play a role in sensory
prediction whereas Unilateral and Postsaccade neurons are
involved in motor control.
To further con ﬁrm these ﬁndings, we performed three
additional analyses. First, the similarity of the time course (rather
than the magnitude) of neuronal activity was examined by
calculating a correlation coef ﬁcient between the data for the
second reactive saccades and later synchronized saccades (>5th).
When the data were aligned with saccades, Unilateral neurons
showed more consistent response than Bilateral neurons
(Supplementary Fig. 10c, left panel). However, when the data
were aligned with the target onset, Bilateral neurons exhibited
more consistent response than Unilateral neurons (right panel).
Second, we applied the time-warping analysis that was
previously used to dissociate sensory from motor responses
during synchronized tapping 49 (Supplementary Methods).
Brieﬂy, this analysis quanti ﬁes the likelihood of spike occurrence
under the assumption of sensory or motor alignments. Although
all neurons showed a preference for motor alignment during
synchronized saccades (because movement occurred at the
predicted rather than actual sensory timing), only Bilateral
neurons signi ﬁcantly changed their preference toward sensory
alignment during the second saccades (paired t-test, two-sided,
t32 = 3.19, P = 0.003, Supplementary Fig. 11a).
0
1
02 0 0 4 0 0
1
0
1
02 0 0 4 0 0
1
0 200 400 600
100 spk/s
0 200 400 600
30 spk/s
Time after saccade (ms) Time after saccade (ms)
Time after saccade (ms) Time after saccade (ms)
Bilateral neuronPostsaccade neuron
n = 33
BilateralPostsaccade
n = 29
ab
cd
Cell # Normalized
activity
–0.5 0.5
29 33
Early
Late Late
Early
Late
EarlyLate
Early
Time after saccade (ms)
Partial correlation coefficient
Partial correlation
ef Correlation with error
(preferred direction)
Post
Bi
10 cells
–1.0 0 1.0
Unilateral
Bilateral
Postsac
n = 33
X = –0.07
P = 0.12
n = 33
X = 0.01
P = 0.73
n = 29
X = –0.10
P < 0.01
02 0 0 4 0 0
–0.3
0
0.3
Uni
Fig. 4 Neuronal correlates of temporal error. a A Postsaccade neuron that
responded to the temporal error. The data are from synchronized saccade
experiments (550 ms SOA) and trials are aligned with ipsilateral saccades
and sorted by temporal error (saccade latency). Orange and magenta dots
on each raster line indicate the timing of target onset and the following
contralateral saccade, respectively. The time courses of neuronal activity
are shown separately for one-third of trials with early and late saccades.
Note that the postsaccade activity was large when saccades preceded the
target onset (inverted triangle). b A Bilateral neuron aligned with ipsilateral
saccades. c Correlation with temporal error in individual Postsaccade
neurons. For each neuron, the partial correlation was computed every
200 ms (10 ms steps) by controlling the preceding ISI (Supplementary
Fig. 8a). The above traces indicate the mean (±s.e.) of the normalized
population activity. d Partial correlation for Bilateral neurons. The traces
indicate the mean (±s.e.) of the normalized population activity. e Time
courses of the partial correlation coef ﬁcient (mean ± s.e.) for different types
of neurons. The array of coloured dots above the trace indicates when the
correlation coef ﬁcients signi ﬁcantly differed from zero (one sample t-test,
two-sided, P < 0.05). The data for the other SOAs are shown in
Supplementary Fig. 5d. f Distributions of the correlation coef ﬁcient for
individual neurons. Partial correlation was measured during the interval
denoted by the gray shading in e. The black bar indicates signi ﬁcant
correlation (permutation test, P < 0.05). The inverted triangle represents
the population mean (X) and the P-value indicates the result of the two-
sided one sample t-test (Bilateral neurons, t
32 = −1.60, P = 0.12; Unilateral
neurons, t32 = 0.34, P = 0.73; Postsaccade neurons, t28 = −4.37,
P = 1.5 × 10−4). Data for all types of neurons sorted by either saccade
direction are shown in Supplementary Fig. 8. The results of decoding
analysis for the ISI, temporal error, and the other task conditions are shown
in Supplementary Fig. 9. Numeral data are available in the Source Data ﬁle.
ARTICLE NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2
6 NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications
F i n a l l y ,w ea l s oe x a m i n e dt h ec h a n g ei nt h et i m ec o u r s eo f
target-aligned neuronal activity with the order of target
presentation (Supplementary Fi g. 11b). When the difference
in the time course of activity for Unilateral neurons between
the ﬁrst and the later cycles was quanti ﬁed using the ROC
analysis (Supplementary Methods), the area under the curve
(AUC) averaged 0.71 ± 0.15 (s.d.) and was signi ﬁcantly
different from 0.5 (one sample t-test, two-sided, t32 = 8.26,
P <1 0−8). In contrast, for Bilateral neurons, the activity lasted
longer in the ﬁrst cycle, but the centre of the activity was
almost the same as that during s ynchronized saccades (AUC,
0.51 ± 0.15, P = 0.66). These results further suggest that
Unilateral neurons are involved in saccade generation,
while Bilateral neurons may re ﬂect the temporal prediction
of target appearance both in the initial cycles and during
synchronization.
When the relationship between the SMI and the absolute value of
the DI was examined for all neurons, there was a signiﬁcant negative
correlation between them (r = −0.55, P = 1.5 × 10−8,F i g .5d). There
was also a signi ﬁcant correlation between the SMI and PI, with
neurons that increased their activity during synchronized move-
ments re ﬂecting the sensory component more strongly ( r = 0.38,
P = 1.8 × 10−4,F i g . 5e). The relationships between these three
indices are summarized in Supplementary Fig. 11c.
Causal role in synchronized saccades . To determine the causal
relationship between these neuronal activities and behavioural
LRLRLR
1
2
3
4
Targ Sac Targ Sac
Left Right
LRLRLR Targ Sac Targ Sac
550 ms
Left Right
c
b
1
2
3
4
Eye
position
Firing rate
Sensorimotor index (SMI)
0–1 1
0
1CDF
| Directional index |
SMI
1
0
–1
01
SMI
1
0
–1
–0.3 0.50
200 ms
r = –0.55
P < 10–7
r = 0.38
P < 10–3
de
SMI = 0.27
SMI = –0.90
Firing rate
n = 94
sensorymotor 
Bilateral
Unilateral
Postsac
a
Eye
position
550 ms 200 ms
Prediction index
>5
>5
Fig. 5 Dissociation between sensory prediction and motor preparation. a Left: Response of a Unilateral neuron to the early stimulus sequence. Data are
aligned with the target onset (blue and red vertical lines) in the synchronized (predictive) saccade trials with a 550 ms SOA. The black symbol on each
raster line indicates saccade onset. Note that neuronal activity consistently preceded the leftward saccade rather than the target onset. Right: Traces of the
mean ﬁring rate aligned either to the target onset or saccade initiation. Numbers on the left denote the stimulus sequence. Green and orange shadings
represent the 100 ms window centred at the peak activity during the later stimulus sequence (red dot on the bottom trace). Red curves indicate the
responses to the second target or saccade in the preferred direction, which were used for the quantitative analysis in c. b Response of a Bilateral neuron.
Note that the peak of the neuronal ﬁring rate roughly aligned with target onset even during the initial few cycles of target presentation, while saccades
lagged behind the target onset. c Comparison of the sensorimotor index (SMI) across neuron types. The SMI was computed for the response to the second
stimulus in the sequence as ( Targ − Sac)/(Targ + Sac), where Targ and Sac indicated the activity for target onset and saccades, respectively. The value
becomes positive as neuronal activity is better aligned to the target onset than to saccade initiation. Since the SMI became close to zero as the animal s
generated synchronized saccades (Supplementary Fig. 10a), we focused on the SMI for the second saccades. The SMI computed for saccades in the non-
preferred direction is shown in Supplementary Fig. 10b. d, e Relationship between the indices. The colour of the dots indicates the type of neuron. The
relationship between the three indices is shown in Supplementary Fig. 11c. Numeral data are available in the Source Data ﬁle.
NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2 ARTICLE
NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications 7
performance, electrical microstimulation was applied to the
recording sites during synchronized saccades (550 ms SOA). A
train of stimulation pulses (100 ms in duration at 333 Hz, 100 µA)
was delivered 100, 200, 300 or 400 ms after the saccade, and the
effects on the next saccade timing (or ISI) were examined
(Fig. 6a). The box-whisker plot in Fig. 6b summarizes the effect
sizes for all stimulation conditions for the 40 sites that showed
signiﬁcant effects in any of the conditions (Dunnett test, P < 0.05,
n = 32 and 8 for monkeys I and J, respectively). The stimulation
affected only the timing of the next saccades, and monkeys
adjusted after the next ISI to compensate temporal errors induced
by the stimulation (Supplementary Fig. 12).
The effects of electrical stimulation varied greatly from site to
site, and signi ﬁcant facilitatory and suppressive effects on
saccades were found in various proportions, even under the
same conditions (Fig. 6b). To examine the differences by
stimulation site in detail, the data were clustered into three
categories based on the effect size in each condition (Fig. 6c and
d). In the ﬁrst group, electrical stimulation promoted saccades in
both directions (vertical cyan bar on the right in Fig. 6c). In the
second group, stimulation facilitated contralateral but delayed
ipsilateral saccades, and the effect was greater when stimulation
was delivered immediately after the previous saccade (magenta).
In the third group, only contralateral saccades were delayed
regardless of stimulation timing (orange).
We assumed that the changes in saccade timing for each site
could be explained by a certain combination of the effects of
stimulation to the three types of neurons (Methods). We estimated
the relative impact of electrical stimulation to each group of
neurons by calculating simple Pearson correlations between
neuronal activity at speci ﬁc 100 ms periods and the ISI
(Supplementary Fig. 13a –c). Our model well explained the
stimulation effects such that the coef ﬁcients of determination
(CDs) were signi ﬁcantly greater than those obtained from the
permutation data (1000 iterations, Wilcoxon ’sr a n k - s u mt e s t ,
P < 0.01, Supplementary Fig. 13d) and the CDs for 72.5% of the
stimulation sites were greater than the median of the permutation
data. The triangular plot in Fig. 6e summarizes the relative
contribution of each neuronal population to the changes in saccade
timing derived from the ﬁtted data. The data showed that the ﬁrst
group (cyan) was mainly accounted for by the stimulation effects of
Bilateral and Unilateral neurons, and that the second group
(magenta) was due to the Postsaccade neurons. In addition,
Bilateral neurons and Unilateral neurons were stimulated in
various relative proportions, while Bilateral neurons and Post-
saccade neurons were rarely stimulated simultaneously. This
observation was consistent with the results of our neuronal
recordings, which showed that Bilateral neurons and Postsaccade
neurons were distributed separately, mainly in the ventral and
dorsal portions of the dentate nucleus, respectively (Supplementary
Fig. 1). In fact, the stimulation sites for the second group tended to
be distributed more dorsally than the other groups (one-way
a
cd
e Bilateral
Postsac
1
16
35
40
–1 1
effect size
100200300400100200300400
Ipsi Contra
Session number (sorted)
Unilateral
Stimulation timing (ms)
100 200 400300 100 200 400 300
b
n = 40
0
1.5
0
15Count Cohen's d
Contra sacIpsi sac
Contra
saccade
No stim
200
300
400
100
100 ms
d’ = 0.27
d’ = 0.28
d’ = –0.70
300 800
d’ = –0.04
0
10
ISI (ms)
delay mean of control
Fig. 6 Effects of electrical microstimulation. a Left: Traces of eye position
in a representative session. A train of biphasic pulses of stimulation current
(100 μA, 333 Hz for 100 ms) was delivered through an electrode at
different times following the ﬁfth or later saccade during the synchronized
saccade trial. The numbers indicate the stimulation timing in milliseconds.
Right: Histogram shows the distribution of the ISI in each condition. Red
vertical dashed line represents the mean for the non-stimulation control. d ’
indicates the effect size (Cohen ’s d) for each condition. b The box-whisker
plot in the upper panel summarizes the median, quartiles, and range of the
effect size on the next saccade timing for different stimulation times and
saccade direction. Circles indicate the respective mean value. The lower
panel summarizes the number of sessions with a signi ﬁcant stimulation
effect (Dunnett test, P < 0.05), separately showing the facilitatory (negative
values) and suppressing (positive) effects. The stimulation effects on the
timing of two later saccade are shown in Supplementary Fig. 12. The
stimulation effects are separately plotted for dorsal and ventral sites in
Supplementary Fig. 13f. c Effects of electrical stimulation in individual
sessions. For each site, the stimulation effects on the ISI are shown for
different stimulation times and saccade direction. Sessions are sorted based
on the clustering analysis, and the colour bars on the right indicate different
groups. Depths of stimulation sites for each cluster are shown in
Supplementary Fig. 13e. d A dendrogram derived from the cluster analysis.
e Relative contribution of the different types of neurons to the stimulation
effect. For each type of neuron, the impact of stimulation was estimated by
computing the simple correlation coef ﬁcients between the neuronal activity
and the ISI at different stimulation times (100 ms interval, Supplementary
Fig. 13a–c). The contributions of different types of neurons were calculated
by ﬁtting the data of stimulation effects in c with the impact of neuronal
activity on saccade timing shown in Supplementary Fig. 13c. Colour and size
of circles indicate the cluster number and the goodness-of- ﬁt summarized
in Supplementary Fig. 13d, respectively. Numeral data are available in the
Source Data ﬁle.
ARTICLE NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2
8 NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications
ANOVA, F2,39 = 3.37, P = 0.045, Supplementary Fig. 13e). Con-
sistent with these ﬁndings, the effects of stimulation at dorsal and
ventral sites showed similar properties to the second and ﬁrst
groups, respectively (Supplementary Fig. 13f).
Although we did not deliver electrical stimulation during
reactive saccades, the sizeable neuronal activity between condi-
tions in Unilateral and Postsaccade neurons (Fig. 2d) suggests
that electrical stimulation of these neurons may change the
latency of reactive saccades. Indeed, the activity of these neurons
before target presentation in the reactive task correlated with
saccade latency in a similar way to those during synchronized
saccades (Supplementary Fig. 14). The correlation analysis also
showed that the activity of Bilateral neurons inversely correlated
with the latency of contralateral reactive saccades but not with the
latency of ipsilateral saccades, whereas the same neurons were
signiﬁcantly correlated with the timing of synchronized saccades
in both directions (Supplementary Fig. 13b). These results
indicate that the signals conveyed by Bilateral neurons may not
be strictly related to movement like the other types of neurons.
Furthermore, the correlation with temporal error after saccades,
normally found in Postsaccade neurons during synchronization
(Fig. 4e), disappeared during reactive saccades. These results
suggest that electrical stimulation to the ventral part of the
dentate nucleus (where Bilateral neurons reside) may promote
only contralateral reactive saccades, while the same stimulation
promoted synchronized saccades in both directions (Fig. 6c and
Supplementary Fig. 13f).
Discussion
Synchronized movement requires multiple neural processes,
including adjustment of movement timing, detection of temporal
error, and generation of internal rhythms. We have shown that all
these signals for synchronized saccades are represented in the
posterior part of the cerebellar dentate nucleus. Unilateral neu-
rons mostly showed ipsilateral directional preference and exhib-
ited preparatory activity that closely correlated with the timing of
the next saccade. Postsaccade neurons showed transient activity
immediately after saccades, and about half of them correlated
with temporal error of synchronized saccades. Bilateral neurons,
which made up about one-third of the recorded neurons, had
both of these properties. Of the three types of neurons, only
Bilateral neurons displayed greater activity during synchronized
saccades than during reactive saccades, which might be related to
the increased activity reported in the previous imaging study
40.
During synchronization, the brain needs to maintain an
internal rhythm to make a series of predictive movements 50.
Since our monkeys had been trained on the synchronized saccade
task for many months, it is likely that they were able to quickly
generate an internal rhythm in each trial. In fact, we have pre-
viously shown that the animals can continue to make saccades for
many cycles even after removing the temporal error by presenting
a target at the time of eye movements (error-clamp condition) 38.
We found in this study that Unilateral and Postsaccade neurons
consistently increased their activity in relation to saccades, but
many Bilateral neurons were active at the time of target onset
during the transition from reactive to synchronized saccades in
each trial (Fig. 5). These results suggest that Bilateral neurons
may represent the expected timing of target onset, rather than
promoting a speci ﬁc motor output.
Previous studies have shown that internal rhythms emerge in
predicting the appearance of periodic stimuli even in the absence
of movement 51, and that the cerebellum is involved in this
process26. In particular, recent studies in primates have demon-
strated that neurons in the posterior portion of the dentate
nucleus exhibit predictive activity that peaks at the timing of
periodic visual stimuli 27,52. Furthermore, evidence shows that the
cerebellum also plays a role in generating internal forward models
for purely sensory aperiodic events, such as trajectory of slowly
moving objects31–33,53. The activity of Bilateral neurons described
so far could be regarded as an internal model of periodically
alternating visual stimulus, which guides synchronized saccades.
The three types of neurons were localized in a restricted region
of the cerebellar dentate nucleus. While there was no difference in
the anterior-posterior or medial-lateral coordinates of the
recording sites between the groups, there was a clear difference in
the depth of the recording sites (Supplementary Fig. 1). Since the
stimulation effects on saccade timing can be explained as a
combination of the effects of excitation of these groups of neu-
rons, each group may be involved in multiple processes necessary
for synchronized saccades in parallel, by sending information to
different brain regions. Neurons in the posterior portion of the
cerebellar dentate nucleus are known to project directly to the
superior colliculus (SC) 54 and indirectly via the thalamus to the
frontal eye ﬁelds (FEF), supplementary eye ﬁeld (SEF), and pos-
terior parietal cortex (PPC) 34. Recent studies using trans-synaptic
tracers have reported that the FEF and PPC receive signals mainly
from the ventral portion of the dentate nucleus 34,55, whereas the
trans-thalamic projections to the SEF originate from both the
dorsal and ventral portions 56.
Supplementary Fig. 15 shows a diagram of the hypothesis
that the cerebellum controls synchronized saccades through
multiple loops with oculomotor areas in the cerebral cortex.
Bilateral neurons participate in the link with the SEF and
represent the temporal prediction of the target sequence.
Postsaccade neurons participate in the link with the PPC and
SEF, which plays a role in monitoring errors and updating
internal rhythms. Unilateral neurons participate in the link
with the FEF and/or SC and regulate saccade timing. Although
this multiple-loop hypothesis is highly speculative, it will pro-
vide a practical working hypothesis for future studies exploring
signals in these cortical areas and the SC during synchronized
saccades.
Two issues must be considered when interpreting the present
results. First, the possible involvement of the medial part of the
cerebellum in synchronized saccades cannot be ruled out. For
oculomotor control, vermal lobules VI –VII regulate signals in
the brainstem saccade generator through the fastigial nucleus 57.
This pathway is important for the adaptation of saccade
amplitude and direction 15, but its involvement in saccade
timing might become apparent in future studies. For example,
recent studies in rodents have shown that both the medial 58 and
lateral 59 cerebellum are involved in self-timed somatic move-
ments. The second issue is that in the present study, the animals
alternated saccades in opposite directions, whereas many stu-
dies of synchronized movement employ tasks with a repetition
of identical movements, such as tapping. However, everyday
activities such as dancing and clapping involve adjusting the
timing of multiple movements, and many similarities can be
found with synchronized eye movements. The present results
may be generalized by exploring neuronal activity in the medial
frontal cortex and the striatum, which has been examined
during tapping 24,60, using the synchronized saccade task.
Methods
Animal preparation . Two adult male Japanese macaques (monkeys I and J, 7 –9
years old, 8 –9 kg) were used. These animals were previously used in a series of
behavioural experiments 38,61,62. All experimental protocols were evaluated and
approved in advance by the Hokkaido University Animal Care and Use Committee
and were in accordance with the Guidelines for Proper Conduct of Animal
Experiments (Science Council of Japan, 2006). Animal health and well-being were
carefully monitored by animal care staff and experimenters, and food intake, water
supply, stool volume, and overall physical condition were checked and recorded
NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2 ARTICLE
NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications 9
daily. To motivate the animals to perform the tasks, their water intake was regu-
lated during weekday training and experiments, but they had free access to water
on weekends. There was no strict dietary restriction, and a variety of vegetables,
fruits, nuts and grains were provided daily.
The procedures for animal surgery and recording experiments were identical to
those described previously 63. Brieﬂy, in separate surgeries under general iso ﬂurane
and nitrous oxide anaesthesia, a pair of plastic head holders was installed to the
skull using titanium screws and dental acrylic, and a scleral search coil was
implanted under the conjunctiva. Analgesics were administered during each
surgery and for the following few days. After recovery from surgery, the monkeys
were trained in the synchronized saccade task
38 for several months. During the
training and the subsequent experimental sessions, the monkey ’s head was secured
to the primate chair in a darkened booth, and horizontal and vertical eye position
were recorded using the search coil technique (MEL-25, Enzanshi Kogyo). After
training on eye movement tasks, a third surgery was performed to place a recording
chamber for vertical electrode penetration aimed at the deep cerebellar nuclei. The
location of the chamber was veri ﬁed postsurgically using MRI. Daily recording
sessions began after full recovery from the surgery. Topical or systemic antibiotics
were administered as necessary.
Visual stimuli and behavioural task . Experiments were controlled by a Windows-
based stimulus presentation and data acquisition system (TEMPO, Re ﬂective
Computing). Visual stimuli were presented on a 27-inch liquid crystal display
monitor (XL2720Z, BenQ, refresh rate 120 or 144 Hz) that was located 40 cm away
from the eyes and subtended 73° × 46° of visual angle. Throughout the experiment,
two landmarks (white un ﬁlled 1° squares) were presented ±7° horizontally (Fig. 1a)
on a dark background, and all visual stimuli were presented within the landmark.
Each trial started with the appearance of an initial ﬁxation point (blue or purple
square, 10.9 cd/m
2) at either landmark location. After a random 1000 –2000 ms
period, the ﬁxation point was extinguished and a saccade target (red or green
square, 33.9 cd/m 2) was presented at the other landmark location. The saccade
target was alternately presented at the landmark locations with a stimulus onset
asynchrony (SOA; 400, 550, or 700 ms) for 8000 or 12000 ms (11 –30 target steps)
and was visible until the appearance of the opposite target. The animals were
trained to follow the alternating targets with their eyes. The trial was aborted
immediately if the monkey made an anticipatory saccade to the ﬁrst target in the
sequence (reaction time < 100 ms), or if the inter-saccadic interval (ISI) was shorter
than 25% SOA or longer than twice of the SOA, or if the eyes were deviated >3.5°
vertically from the target locations.
The animals performed the task under two different stimulus conditions. In the
synchronized (predictive) condition (Fig. 1b, top), the initial ﬁxation point was
blue, the saccade target was red, and the SOA was constant in each trial but varied
from trial to trial. To promote synchronized saccades, a liquid reward was given
after every three consecutive predictive saccades (generated within ±20% SOA of
the target appearance) for the fourth or subsequent targets in the sequence. The
reward was delivered at a random time within 600 ms after every three
synchronized saccades. Because the initial ﬁxation period and SOA varied from
trial to trial, the monkeys were unable to predict the timing of the ﬁrst two stimuli.
In the reactive condition (Fig. 1b, bottom), the initial ﬁxation point and saccade
target were purple and green, respectively, and each SOA was randomly selected
from 400, 550, and 700 ms within each trial. Animals received an immediate
reward after every three reactive saccades that were generated between 100 ms after
the target onset and the appearance of the opposite target. In both conditions, the
amount of a single reward was adjusted so that the total reward for each trial was
approximately the same across the SOAs. These two conditions were presented
randomly in a block of trials. During the recording sessions, reactive saccade trials
were presented with equal probability to synchronized saccade trials of each SOA,
although four neurons (4.2%) were tested for synchronized saccades only. Because
both monkeys had previously been trained on a similar synchronized saccade
task
38,62, they quickly learned to switch behavioural strategies on each trial within a
few days.
Recording procedures . Single neuron activity was recorded from three dentate
nuclei of the two monkeys. Single tungsten microelectrodes (~1.0 M Ω at 1 kHz,
Alpha Omega Engineering or FHC Inc. ) were lowered through a 23-gauge
stainless steel guide tube using a grid system (Crist Instruments). The electrodes
were advanced remotely using a micr omanipulator (MO-97S, Narishige)
attached to the recording chamber. Signals obtained from the electrodes were
ampliﬁed, bandpass ﬁltered (300 Hz to 10 kHz), and monitored online using
oscilloscopes and an audio device. Once a task-related neuron was encountered,
waveforms of action potentials were isolated using software with real-time
template-matching algorithms (ASD, Alpha Omega Engineering). The occur-
rence of each action potential was saved in ﬁles as a time stamp with the data of
eye movements and visual stimuli during the experiments. We found task-
related neurons in the caudal part of the cerebellar dentate nucleus (Fig. 1d).
Most neurons were recorded from stereotaxic coordinates 8 mm posterior to the
interaural line and 9 mm lateral to the midline in monkey I, and 8 mm posterior
and 8 mm lateral in monkey J (Supplementary Fig. 1).
Electrical microstimulation . To examine the causal role of neuronal activity,
electrical stimulation was applied to the recording sites during the synchronized
saccade task. A train of 0.2 ms biphasic pulses at 333 Hz for 100 ms was delivered
as electrical stimulation. The current intensity was monitored by measuring the
voltage across a 1 k Ω resistor placed in series with the electrode, and was adjusted
to 100 μA. Electrical stimulation was applied at 100, 200, 300, or 400 ms following
every four synchronized saccades (550 ms SOA). The stimulation timing was
constant during each trial (~ four times per trial), but varied from trial to trial. We
have never delivered stimulation during the reactive saccade trials.
Histological procedures . After completion of the experiments in monkey I, sev-
eral marking lesions were made by injecting direct current (10 –20 µA, tip negative,
~1 mC) through electrodes placed at known coordinates. Several days after this
procedure, the animal was sedated, administered analgesics, deeply anesthetized
with pentobarbital, and transcardially perfused with phosphate-buffered saline
followed by 3.5% paraformaldehyde. The brain was then removed, ﬁxed, and
equilibrated with 30% sucrose. Histological sections (100 μm, coronal) were cut on
a freezing microtome (HM440E, Microm) and stained with cresyl violet. The
recording sites were reconstructed according to stereotaxic coordinates, and the
depth of the electrode tip relative to the dorsal border of the dentate nucleus, which
was veri ﬁed physiologically during the experiments (Fig. 1d and Supplementary
Fig. 1).
Behavioural data analysis . The eye position signals obtained directly from the eye
coil device (MEL-25, Enzanshi Kogyo) were digitized at a 16-bit resolution, sam-
pled at 1 kHz, saved to a ﬁle during the experiments, and analysed of ﬂine using
Matlab (Mathworks). During the experiments, saccades were detected online when
horizontal eye position crossed the centre of the screen. However, for the of ﬂine
analysis, saccade onset was detected when the angular eye velocity exceeded 200°/s
and an eye displacement was >7°. We measured two temporal parameters of
saccades. The inter-saccadic interval (ISI) was the onset interval of successive
targeting saccades in opposite directions. The temporal error was the time from the
target onset to saccade initiation and was equivalent to the latency of reactive
saccades. When we examined the time course of saccade latency in each trial
(Fig. 1c), the data of reactive saccades for different SOAs were plotted every 550 ms.
Classiﬁcation of neurons . Neurons that showed periodic activity during saccades
were classi ﬁed according to the time course of their activity. First, we aligned the
data with the sixth and subsequent synchronized saccades in each direction and
calculated the spike density function (Gaussian kernel, σ = 20 ms). Next, the data at
275 ms before and after saccades in the opposite directions were concatenated and
normalized by the maximum and minimum values for each neuron. Based on the
time course of normalized activity, a total of 95 neurons were classi ﬁed into four
categories using Ward
’s hierarchical clustering method (Supplementary Fig. 2a).
The classiﬁcation was made using the data from the trials with a 550 ms SOA, and
the activities in different conditions were compared across groups. The Unilateral
neurons showed a preference for ipsilateral ( n = 24) or contralateral ( n = 9) sac-
cades to the recording site, and data from these neurons were combined in the
subsequent quantitative analysis (Fig. 2a). Unilateral, Bilateral, and Postsaccade
neurons had different preferences for saccade direction, behavioural condition, and
sensory stimulus, and were recorded from different depths in the cerebellar nucleus
(Supplementary Fig. 1). We also performed one-way ANOVAs with three factors of
saccade direction, task condition, and SOA for neuronal activity during a 200 ms
period before (Unilateral and Bilateral neurons) and after (Postsaccade neuron)
saccades (Supplementary Fig. 2b).
Calculation of indices that characterize neuronal activity . To characterize
neuronal activity, we calculated the following modulation indices for individual
neurons and compared them across neuronal groups. The directional index (DI)
was de ﬁned as ( Ipsi–Contra)/(Ipsi + Contra), where Ipsi and Contra indicate the
magnitude of neuronal activity measured for ipsilateral and contralateral saccades,
respectively. Neuronal activity was measured from the spike density function
during a 200 ms period starting from 250 ms before (Unilateral and Bilateral
neurons) or immediately after (Postsaccade neurons) saccades.
The prediction index (PI) was calculated as ( Pred–React)/(Pred + React), where
Pred and React represent the magnitude of ﬁring modulation during predictive and
reactive saccades in the preferred direction, respectively. For predictive saccades,
the activity was measured for the sixth or later saccades in the sequence in trials
with a 550 ms SOA. For reactive saccades, the data were aligned with saccades
following a 550 ms ﬁxation interval. To measure the ﬁring modulation, we initially
searched for the peak of the spike density function during ±275 ms of the saccades
in the preferred direction. We then searched for the minimum value of the activity
within ±275 ms of the peak. The magnitude of the ﬁring modulation was measured
as the difference between these values. Similarly, the PI for different SOAs was also
calculated by measuring the ﬁring modulation for saccades with the same length of
measurement interval as the SOA. The modulation of neuronal activity for
different task conditions and saccade direction were also evaluated by computing
the mutual information (Supplementary Methods and Supplementary Fig. 3).
ARTICLE NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2
10 NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications
The sensorimotor index (SMI) was de ﬁned as ( Targ–Sac)/(Targ + Sac), where
Targ and Sac denote the neuronal activity around the time of the target onset and
saccade, respectively. To calculate the index, we ﬁrst aligned the neuronal data with
target onset or saccade initiation for the sixth and subsequent synchronized
saccades in trials with a 550 ms SOA. Then the time of peak activity was
determined from the spike density function computed for each alignment. Next, we
measured the neuronal activity at ±50 ms from the time of the peak for each of the
2nd–5th sequences of the target ( Targ) and saccade ( Sac) and computed the SMI
(Supplementary Fig. 10a). We mainly consider the value obtained from the second
saccade because these saccades were reactive in nature and therefore the target
onset and saccade initiation were temporally decoupled. If the neuronal activity
was better aligned with the target onset, the SMI had a positive value. If the
neuronal activity was better aligned with saccades, it had a negative value. The
SMIs for the second saccades in the preferred direction were compared across
neuronal groups (Fig. 5c), although one neuron was tested only in the non-
preferred direction in the second sequence. The index was also computed for
saccades in the opposite direction for only those Bilateral and Postsaccade neurons
that exhibited bidirectional modulation (Supplementary Fig. 10b). We also
performed additional analyses to complement the results obtained from the
comparison of the SMIs across types of neurons. Details are described
in Supplementary Methods and Supplementary Figs. 10 and 11 legends.
Correlation between neuronal activity and saccade timing . The cerebellum is
thought to be involved in the predictive control of movement and the detection of
errors that are necessary for learning. To evaluate the information carried by each
dentate nuclear neuron, the correlations between neuronal activity and the timing
of saccades were examined. When investigating the relationship between neuronal
activity and motor control, data were aligned with synchronized saccades, and
partial correlations of trial-by-trial neuronal ﬁring rate with the timing of the next
saccade (ISI) were calculated every 200 ms (10 ms steps), controlling for temporal
errors of saccades and the previous ISI (Fig. 3c–e). Since the goal of this analysis
was to evaluate the signals regulating saccade initiation, the partial correlation was
calculated for the data until the next saccade. Therefore, the number of trials
contributing to the partial correlation decreased shortly before the next target
onset. To examine the relationship between neuronal activity and timing errors,
data were again aligned with synchronized eye movements, and partial correlations
with temporal error (saccade latency) were calculated after controlling for the
previous ISI (Fig. 4c–e). The partial correlation coef ﬁcients at 200 –400 ms and
0–200 ms following synchronized saccades, where large correlations were found,
were used as indices for evaluating the involvement of neuronal activity in motor
control and error monitoring, respectively, and the groups of neurons were com-
pared (Fig. 3f, 4f, Supplementary Figs. 6d and 8d).
Stimulation data analysis . The effects of electrical microstimulation were quantita-
tively analysed for 49 sites where stimulation was delivered for ≥20 synchronized
saccades in each condition. The effect size (Cohen’s d) for each condition was calculated
as (μ
stim – μcont)/sqrt[(σstim2 + σcont2)/2], whereμ and σ indicate the mean and standard
deviation of the ISI with (stim) or without (cont) stimulation, respectively. The Dunnett
test was used to evaluate the effect of electrical stimulation at each site and the timing of
saccades in either direction. If a signiﬁcant effect was found in at least one stimulation
condition, the data obtained from that site were included for further analysis (n = 32
and 8 sites for monkeys I and J, respectively, Fig. 6b, bottom). The data from 40 sti-
mulation sites were classiﬁed into three groups using the hierarchical clustering method
based on the effect sizes under eight different stimulation conditions (Fig.6ca n dd ) .
Since the stimulus effect at each site is expected to be determined by combinations of
task-related neurons in the surrounding area, we attempted to model the stimulation
effect by a certain combination of the effects of stimulation to the three groups of
neurons. The stimulation effects on the different groups of neurons were estimated
based on simple Pearson correlations between each neuron’s activity and the ISI cal-
culated at the four electrical stimulation times and averaged for each group of neurons
(Supplementary Fig. 13a–c). Because there were only nine Unilateral neurons with
contralateral preference, the correlation coefﬁcient for the population of Unilateral
neurons was calculated by combining the values of the ipsilateral and contralateral
neurons andﬂipping the same value (Supplementary Fig. 13c, green dotted lines). Since
these values are considered to reﬂect the strength of the in ﬂuence of each group’s
activity on saccade timing, we assumed that theeffect of electrical stimulation would be
a linear sum of these values with appropriate weights. Thus, the effect sizes in eight
different conditions for each stimulation site (d) will be described as,
d ¼ w
ipsiUniipsi þ wcontraUnicontra þ wbiBi þ wpostPost ð1Þ
where w indicates the weight for each group of neurons and Uni, Bi, Post are the
impacts of stimulation effect of each group of neurons on saccade timing calculated
above as the Pearson correlation at eight different timing (Supplementary Fig. 13c). We
constrained the weight (w) of each group to be positive because electrical stimulation
increases the activity of nearby neurons. The values of w calculated by the least-squares
method for each stimulation site were normalized and are plotted in Fig. 6e.
Statistical analysis . The unpaired t-test or analysis of variance (ANOVA) was
used to compare the indices, peak latencies, and recording sites among the
neuronal groups, and the one sample t-test was used to compare the mean of each
group with a constant value. To evaluate the effects of electrical stimulation,
Dunnett’s test was performed between the ISI in each stimulation condition and in
the control. All tests were performed using the Statistical toolbox for Matlab. To
evaluate the partial correlation between neuronal activity and saccade timing for
each neuron, the distribution of the r-values obtained from the permutated data
(1,000 iterations) was compared with the actual data (Fig. 3f, 4f, Supplementary
Figs. 6d and 8d). Other statistical methods are described in the relevant text or
ﬁgure legends.
Further details of the analysis in the Supplementary Figures can be found in
the Supplementary Methods and in the relevant ﬁgure legends.
Reporting summary . Further information on research design is available in the Nature
Research Reporting Summary linked to this article.
Data availability
All data analysed here are included in this article and its supplementary information ﬁles.
Numerical data for each ﬁgure and supplemental ﬁgures are provided in the Source
Data ﬁle.
Received: 10 September 2021; Accepted: 21 April 2022;
References
1. Merchant, H., Harrington, D. L. & Meck, W. H. Neural basis of the perception
and estimation of time. Annu Rev. Neurosci. 36, 313 –336 (2013).
2. Kotz, S. A., Ravignani, A. & Fitch, W. T. The evolution of rhythm processing.
Trends Cogn. Sci. 22, 896 –910 (2018).
3. Wiener, M., Turkeltaub, P. & Coslett, H. B. The image of time: a voxel-wise
meta-analysis. Neuroimage 49, 1728 –1740 (2010).
4. Coull, J. T., Cheng, R. K. & Meck, W. H. Neuroanatomical and neurochemical
substrates of timing. Neuropsychopharmacology 36,3 –25 (2011).
5. Holmes, G. The cerebellum of man. Brain 62,1 –30 (1939).
6. Ivry, R. B., Keele, S. W. & Diener, H. C. Dissociation of the lateral and medial
cerebellum in movement timing and movement execution. Exp. Brain Res. 73,
167–180 (1988).
7. Bastian, A. J., Martin, T. A., Keating, J. G. & Thach, W. T. Cerebellar ataxia:
abnormal control of interaction torques across multiple joints. J. Neurophysiol.
76, 492 –509 (1996).
8. Thach, W. T. Does the cerebellum initiate movement? Cerebellum 13, 139–150
(2014).
9. Tanaka, M. et al. Roles of the cerebellum in motor preparation and prediction
of timing. Neuroscience 462, 220 –234 (2021).
10. Dacre, J. et al. A cerebellar-thalamocortical pathway drives behavioral context-
dependent movement initiation. Neuron 109, 2326 –2338 (2021).
11. Spencer, R. M., Zelaznik, H. N., Diedrichsen, J. & Ivry, R. B. Disrupted timing
of discontinuous but not continuous movements by cerebellar lesions. Science
300, 1437 –1439 (2003).
12. Wolpert, D. M., Miall, R. C. & Kawato, M. Internal models in the cerebellum.
Trends Cogn. Sci. 2, 338 –347 (1998).
13. Shadmehr, R., Smith, M. A. & Krakauer, J. W. Error correction, sensory prediction,
and adaptation in motor control. Annu Rev. Neurosci. 33,8 9–108 (2010).
14. Lisberger, S. G. The rules of cerebellar learning: around the Ito hypothesis.
Neuroscience 462, 175 –190 (2021).
15. Soetedjo, R., Kojima, Y. & Fuchs, A. F. How cerebellar motor learning keeps
saccades accurate. J. Neurophysiol. 121, 2153 –2162 (2019).
16. Boyden, E. S., Katoh, A. & Raymond, J. L. Cerebellum-dependent learning: the
role of multiple plasticity mechanisms. Annu Rev. Neurosci. 27, 581 –609
(2004).
17. Perrett, S. P., Ruiz, B. P. & Mauk, M. D. Cerebellar cortex lesions disrupt
learning-dependent timing of conditioned eyelid responses. J. Neurosci. 13,
1708–1718 (1993).
18. Medina, J. F. & Mauk, M. D. Computer simulation of cerebellar information
processing. Nat. Neurosci. 3, 1205 –1211 (2000).
19. Tokushige, S. I. et al. Does the clock tick slower or faster in Parkinson ’s
disease? - insights gained from the synchronized tapping task. Front Psychol.
9, 1178 (2018).
20. Breska, A. & Ivry, R. B. Double dissociation of single-interval and rhythmic
temporal prediction in cerebellar degeneration and Parkinson ’s disease. Proc.
Natl Acad. Sci. USA 115, 12283 –12288 (2018).
2 1 . T e k i ,S . ,G r u b e ,M . ,K u m a r ,S .&G r i fﬁths, T. D. Distinct neural substrates of
duration-based and beat-based auditory timing.J. Neurosci.31,3 8 0 5–3812 (2011).
NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2 ARTICLE
NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications 11
22. Schubotz, R. I., Friederici, A. D. & von Cramon, D. Y. Time perception and
motor timing: a common cortical and subcortical basis revealed by fMRI.
Neuroimage 11,1 –12 (2000).
23. Kameda M., Ohmae S., Tanaka M. Entrained neuronal activity to periodic
visual stimuli in the primate striatum compared with the cerebellum. Elife 8,
e48702 (2019).
24. Bartolo, R., Prado, L. & Merchant, H. Information processing in the primate
basal ganglia during sensory-guided and internally driven rhythmic tapping. J.
Neurosci. 34, 3910 –3923 (2014).
25. Merchant, H., Grahn, J., Trainor, L., Rohrmeier, M. & Fitch, W. T. Finding the
beat: a neural perspective across humans and non-human primates. Philos.
Trans. R. Soc. Lond. B Biol. Sci. 370, 20140093 (2015).
26. Fujioka, T., Trainor, L. J., Large, E. W. & Ross, B. Internalized timing of
isochronous sounds is represented in neuromagnetic beta oscillations. J.
Neurosci. 32, 1791 –1802 (2012).
27. Ohmae, S., Uematsu, A. & Tanaka, M. Temporally speci ﬁc sensory signals for
the detection of stimulus omission in the primate deep cerebellar nuclei. J.
Neurosci. 33, 15432 –15441 (2013).
28. Matsuyama, K. & Tanaka, M. Temporal prediction signals for periodic sensory
events in the primate central thalamus. J. Neurosci. 41, 1917 –1927 (2021).
29. Kotz, S. A., Stockert, A. & Schwartze, M. Cerebellum, temporal predictability
and the updating of a mental model. Philos. Trans. R. Soc. Lond. B Biol. Sci.
369, 20130403 (2014).
30. Breska A., Ivry R. B. The human cerebellum is essential for modulating
perceptual sensitivity based on temporal expectations. Elife 10, e66743 (2021).
31. Cerminara, N. L., Apps, R. & Marple-Horvat, D. E. An internal model of a
moving visual target in the lateral cerebellum. J. Physiol. 587, 429–442 (2009).
32. Roth, M. J., Synofzik, M. & Lindner, A. The cerebellum optimizes perceptual
predictions about external sensory events. Curr. Biol. 23, 930 –935 (2013).
33. O ’Reilly, J. X., Mesulam, M. M. & Nobre, A. C. The cerebellum predicts the
timing of perceptual events. J. Neurosci. 28, 2252 –2260 (2008).
34. Strick, P. L., Dum, R. P. & Fiez, J. A. Cerebellum and nonmotor function.
Annu Rev. Neurosci. 32, 413 –434 (2009).
35. Ramnani, N. The primate cortico-cerebellar system: anatomy and function.
Nat. Rev. Neurosci. 7, 511 –522 (2006).
36. Buckner, R. L., Krienen, F. M., Castellanos, A., Diaz, J. C. & Yeo, B. T. The
organization of the human cerebellum estimated by intrinsic functional
connectivity. J. Neurophysiol. 106, 2322
–2345 (2011).
37. Patel, A. D., Iversen, J. R., Bregman, M. R. & Schulz, I. Experimental evidence
for synchronization to a musical beat in a nonhuman animal. Curr. Biol. 19,
827–830 (2009).
38. Takeya, R., Kameda, M., Patel, A. D. & Tanaka, M. Predictive and tempo- ﬂexible
synchronization to a visual metronome in monkeys.Sci. Rep. 7, 6127 (2017).
39. Gámez J., et al Predictive rhythmic tap ping to isochronous and tempo changing
metronomes in the nonhuman primate.Ann N Y Acad Sci. 1423 396–414 (2018).
40. Lee, S. M. et al. Neural correlates of predictive saccades. J. Cogn. Neurosci. 28,
1210–1227 (2016).
41. Ashmore, R. C. & Sommer, M. A. Delay activity of saccade-related neurons in
the caudal dentate nucleus of the macaque cerebellum. J. Neurophysiol. 109,
2129–2144 (2013).
42. Ohmae, S., Kunimatsu, J. & Tanaka, M. Cerebellar roles in self-timing for sub-
and supra-second intervals. J. Neurosci. 37, 3511 –3522 (2017).
43. Fuchs, A. F. Periodic eye tracking in the monkey. J. Physiol. 193,1 6 1–171 (1967).
44. Xu, M., Zhang, S. Y., Dan, Y. & Poo, M. M. Representation of interval timing
by temporally scalable ﬁring patterns in rat prefrontal cortex. Proc. Natl Acad.
Sci. USA 111, 480 –485 (2014).
45. Merchant, H. & Averbeck, B. B. The computational and neural basis of
rhythmic timing in medial premotor cortex. J. Neurosci. 37, 4552–4564 (2017).
46. Wang, J., Narain, D., Hosseini, E. A. & Jazayeri, M. Flexible timing by
temporal scaling of cortical responses. Nat. Neurosci. 21, 102 –110 (2018).
47. Mello, G. B., Soares, S. & Paton, J. J. A scalable population code for time in the
striatum. Curr. Biol. 25, 1113 –1122 (2015).
48. Kunimatsu J., Suzuki T. W., Ohmae S., Tanaka M. Different contributions of
preparatory activity in the basal ganglia and cerebellum for self-timing. Elife 7,
e35676 (2018).
49. Perez, O., Kass, R. E. & Merchant, H. Trial time warping to discriminate
stimulus-related from movement-related neural activity. J. Neurosci. Methods
212, 203 –210 (2013).
50. Joiner, W. M. & Shelhamer, M. An internal clock generates repetitive
predictive saccades. Exp. Brain Res. 175, 305 –320 (2006).
51. Cadena-Valencia J., Garcia-Garibay O., Merchant H., Jazayeri M., de Lafuente
V. Entrainment and maintenance of an internal metronome in supplementary
motor area. Elife 7, e38983 (2018).
52. Uematsu, A., Ohmae, S. & Tanaka, M. Facilitation of temporal prediction by
electrical stimulation to the primate cerebellar nuclei. Neuroscience 346,
190–196 (2017).
53. Bares, M. et al. Impaired predictive motor timing in patients with cerebellar
disorders. Exp. Brain Res 180, 355 –365 (2007).
54. May, P. J., Hartwich-Young, R., Nelson, J., Sparks, D. L. & Porter, J. D.
Cerebellotectal pathways in the macaque: implications for collicular
generation of saccades. Neuroscience 36, 305 –324 (1990).
55. Prevosto, V., Graf, W. & Ugolini, G. Cerebellar inputs to intraparietal cortex
areas LIP and MIP: functional frameworks for adaptive control of eye
movements, reaching, and arm/eye/head movement coordination. Cereb.
Cortex 20, 214 –228 (2010).
56. Lu, X., Inoue, K. I., Ohmae, S. & Uchida, Y. New Cerebello-cortical pathway
involved in higher-order oculomotor control. Cerebellum 19, 401–408 (2020).
57. Yamada, J. & Noda, H. Afferent and efferent connections of the oculomotor
cerebellar vermis in the macaque monkey.J. Comp. Neurol. 265, 224–241 (1987).
58. Gao, Z. et al. A cortico-cerebellar loop for motor planning. Nature 563,
113–116 (2018).
59. Chabrol, F. P., Blot, A. & Mrsic-Flogel, T. D. Cerebellar contribution to
preparatory activity in motor neocortex. Neuron 103, 506 –519 (2019).
60. Merchant, H., Zarco, W., Pérez, O., Prado, L. & Bartolo, R. Measuring time
with different neural chronometers during a synchronization-continuation
task. Proc. Natl Acad. Sci. USA 108, 19784 –19789 (2011).
6 1 . T a k e y a ,R . ,N a k a m u r a ,S .&T a n a k a ,M .S p o n t a n e o u sg r o u p i n go fs a c c a d et i m i n g
in the presence of task-irrelevant objects.PLoS One 16, e0248530 (2021).
62. Takeya, R., Patel, A. D. & Tanaka, M. Te mporal generalization of synchronized
saccades beyond the trained range in monkeys. Front Psychol. 9, 2172 (2018).
63. Tanaka, M. Involvement of the central thalamus in the control of smooth
pursuit eye movements. J. Neurosci. 25, 5866 –5876 (2005).
Acknowledgements
The authors thank M. Suzuki for administrative help; H. Miyaguchi for animal care and
training; M. Takei and M. Kusuzaki for manufacturing some equipment; and other lab
members for comments, discussions, and their help on surgical and histological procedures.
Animals were provided by the National Bio-Resource Project. This work was supported
partly by grants from the Ministry of Education, Culture, Sports, Science and Technology of
Japan (21K06418 to K.O., 15H05985 to R.T., 18H05523, 21H04810 to M.T.).
Author contributions
K.O. analysed the data and edited and revised the manuscript. R.T. designed and per-
formed the experiments and analysed the data. M.T. conceptualized and supervised the
project, helped designing and performing the experiments, drafted and revised the
manuscript. K.O. and R.T. contributed equally to this work.
Competing interests
The authors declare no competing interests.
Additional information
Supplementary information The online version contains supplementary material
available at https://doi.org/10.1038/s41467-022-30246-2.
Correspondence and requests for materials should be addressed to Masaki Tanaka.
Peer review information Nature Communications thanks the anonymous reviewer(s) for
their contribution to the peer review of this work. Peer reviewer reports are available.
Reprints and permission information is available at http://www.nature.com/reprints
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in
published maps and institutional af ﬁliations.
Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative
Commons license, and indicate if changes were made. The images or other third party
material in this article are included in the article ’s Creative Commons license, unless
indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons license and your intended use is not permitted by statutory
regulation or exceeds the permitted use, you will need to obtain permission directly from
the copyright holder. To view a copy of this license, visit http://creativecommons.org/
licenses/by/4.0/.
© The Author(s) 2022
ARTICLE NATURE COMMUNICATIONS | https://doi.org/10.1038/s41467-022-30246-2
12 NATURE COMMUNICATIONS |         (2022) 13:2504 | https://doi.org/10.1038/s41467-022-30246-2 | www.nature.com/naturecommunications
