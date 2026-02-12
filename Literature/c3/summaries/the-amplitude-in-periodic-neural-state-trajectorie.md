# the-amplitude-in-periodic-neural-state-trajectorie

RESEA RCH ARTICL E
The amplitude in periodic neural state
trajectories underlies the tempo of rhythmic
tapping
Jorge Ga ´ mez
ID
, Germa ´ n Mendoza
ID
, Luis Prado, Abraham Betancourt
ID
,
Hugo Merchant
ID
*
Instituto de Neurobi ologı ´ a, Universidad Nacional Auto ´ noma de Me ´ xico, Camp us Juriquilla, Quere ´ taro, Me ´ xico
* hugomer chant@unam .mx
Abstract
Our motor commands can be exquisitely timed according to the demands of the environ-
ment, and the ability to generate rhythms of different tempos is a hallmark of musical cogni-
tion. Yet, the neuronal underpinnings behind rhythmic tapping remain elusive. Here, we
found that the activity of hundreds of primate medial premotor cortices (MPCs; pre-supple-
mentary motor area [preSMA] and supplementary motor area [SMA]) neurons show a
strong periodic pattern that becomes evident when their responses are projected into a
state space using dimensionality reduction analysis. We show that different tapping tempos
are encoded by circular trajectories that travelled at a constant speed but with different radii,
and that this neuronal code is highly resilient to the number of participating neurons. Cru-
cially, the changes in the amplitude of the oscillatory dynamics in neuronal state space are a
signature of duration encoding during rhythmic timing, regardless of whether it is guided by
an external metronome or is internally controlled and is not the result of repetitive motor
commands. This dynamic state signal predicted the duration of the rhythmically produced
intervals on a trial-by-trial basis. Furthermore, the increase in variability of the neural trajec-
tories accounted for the scalar property, a hallmark feature of temporal processing across
tasks and species. Finally, we found that the interval-depend ent increments in the radius of
periodic neural trajectories are the result of a larger number of neurons engaged in the pro-
duction of longer intervals. Our results support the notion that rhythmic timing during tapping
behaviors is encoded in the radial curvature of periodic MPC neural population trajectories.
Author summary
The ability to extract the regular pulse in music and to respond in synchrony to this pulse
is called beat synchronization and is a natural human behavior exhibited during dancing
and musical ensemble playing. A part of the brain called the medial premotor cortex has
been associated with rhythmic entrainment, and yet the neural basis of this complex
behavior is still far from known. In this work, we recorded the neuronal activity from the
medial premotor cortices of macaques trained to tap rhythmically to the frequency of a
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 1 / 32
a1111111111
a1111111111
a1111111111
a1111111111
a1111111111
OPEN ACCESS
Citation: Ga ´ mez J, Mendoza G, Prado L,
Betancour t A, Merchant H (2019) The amplitude in
periodic neural state trajectori es underlies the
tempo of rhythmic tapping. PLoS Biol 17(4):
e3000054. https://d oi.org/10.1371/j ournal.
pbio.30000 54
Academic Editor: Robert Zatorre, McGill
University , CANADA
Received: September 13, 2018
Accepted: March 19, 2019
Published: April 8, 2019
Copyright: © 2019 Ga ´ mez et al. This is an open
access article distributed under the terms of the
Creative Commons Attribution License, which
permits unrestricte d use, distribu tion, and
reproduction in any medium, provided the original
author and source are credited.
Data Availabilit y Statement: All underlying
experimen tal data used in this study have been
deposited in G-Node (https://doid .gin.g-node .org/
d315b3db 0cee15869b3 d9ed164f8 8cfa/).
Funding: This work was funded by Consej o
Nacional de Ciencia y Tecnologia #236836 and
#196, https://ww w.conacyt.gob .mx/, and
Programa de Apoyo a Proyect os de Investigac io ´ n e
Innovacio ´ n Tecnolo ´ gica #IN202317, http://dgapa.
unam.mx/i ndex.php/im pulso-a-la-inv estigacion/
papiit. The funders had no role in study design,
metronome. Using principal component analysis, we projected the time-varying activity
of hundreds of neurons into a low-dimensional space. The projected activity of the neural
population generated a circular trajectory for every interval produced in the sequence,
which travelled at a constant speed but with different radii for different tapping tempos.
In addition, the increase in amplitude and variability of the neural trajectories accounted
for the scalar property of timing, a generalized feature of temporal processing across tasks
and species and which defines a linear relationship between the variability of temporal
performance and interval duration.
Introduction
Precise timing is a fundamental requisite for a select group of complex actions such as the exe-
cution and appreciation of music and dance [1]. In these behaviors, the perception of time
intervals is facilitated by the presence of a regular beat in the rhythmic sequence, and individ-
ual intervals are encoded relative to this pulse or beat. This is called beat-based timing and
serves as a framework for rhythmic entrainment, in which subjects perform movements syn-
chronized to music [2–4]. Most of occidental music is organized by a quasi-isochronous pulse
and frequently also in a metrical hierarchy, in which the beats of one level are typically spaced
at two or three times those of a faster level (i.e., the tempo of one level is 1/2 [march meter] or
1/3 [waltz meter] that of the other), and humans can typically synchronize at more than one
level of the metrical hierarchy [5,6]. Rhythmic tapping to an isochronous metronome is the
simplest case of beat entrainment [7] and has been thoroughly studied in humans [8,9]. In
contrast to the large human flexibility to perceive and entrain to complex beats in music, non-
human primates can perceive [10–13] and synchronize to simple isochronous beats [14–16].
On the other hand, other sets of behaviors, such as the interception of a moving target or the
production of a single interval, seem to depend on a duration-based timing mechanism, in
which the absolute duration of individual time intervals is encoded discretely, like a stopwatch
[2,17]. Functional imaging and behavioral studies have suggested the existence of a partially
segregated timing neural substrate, with the cerebellum as a key structure for duration-based
timing, the basal ganglia as main nuclei for beat-based timing, and medial premotor cortices
(MPCs; which include the pre-supplementary motor area [preSMA] and supplementary
motor area [SMA]) as a potential master clock for both timing mechanisms [7,18–20]. Yet, the
neural substrate for absolute timing, and especially for beat perception and rhythmic entrain-
ment, is still largely unknown.
Recent advances on the neurophysiology of absolute timing during single interval repro-
duction tasks suggest that time is represented in the structured patterns of activation of cell
populations in timing areas such as the MPC and the neostriatum [21–24]. Rather than being
quantified in the instantaneous activity of single cells that accumulate elapsed time or encode
the time remaining for an action [25–27], the duration of produced intervals depends on the
speed at which the neural population response changes. This implies that the activation pro-
files are compressed for short and elongated for long intervals due to temporal scaling on the
activity of the same population of cells [23,24].
On the other hand, MPC neurons are tuned to the duration and ordinal sequence of rhyth-
mic movements produced either in synchrony with a metronome or guided by an endogenous
tempo (synchronization-continuatio n task [SCT]) [4,21]. Remarkably, the time-varying profile
of activation of these interval-specific neural circuits forms a moving bump, which is defined
as a sequential pattern of responses in which the cells are activated consecutively within a
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 2 / 32
data collection and analysis , decision to publish, or
preparation of the manuscript.
Competing interests : The authors have declared
that no competing interests exist.
Abbreviati ons: a.u., arbitrary unit; CC, continuat ion
condition; DAT, Dynamic Attending Theory; dPCA,
demixed PCA; EEG, electroence phalogram ; MPC,
medial premot or cortex; MSE, mean square error;
PC, principal component; PCA, principal
componen t analysis; preSMA, pre-supple mentary
motor area; SC, synchroniza tion condition; SCT,
synchroniza tion-continuat ion task; SI, surprise
index; SMA, suppleme ntary motor area; SRTT,
serial reaction time task; ST, synchroniza tion task;
SVM, support vector machine; TDNN, time-de lay
neural network; TIND, target interva l normalize d
data; UTND, unit time normalize d data.
produced interval. The moving bump repeats itself on each produced interval of the tapping
sequence [4,21,28]. Nevertheless, single MPC cells multiplex the interval, the serial order, and
task phase of the SCT, showing complex and heterogenous time-varying profiles of activation
that make it difficult to understand the neural population mechanisms behind rhythmic tap-
ping. A successful approach to determine the latent task variables in cell populations is to proj-
ect high-dimensional individual neural activity into a low-dimensional topological space, in
order to generate a robust and stable manifold [29]. Recent studies have reconstructed key hid-
den task parameters in the neural state population dynamics [30–32]. Thus, the combined use
of high-density single unit recordings with dimensional reduction methods have revealed
basic organizing principles at the level of the population dynamics, which seem to be extremely
complex at the level of individual neurons [29,33].
Here, we investigated the population dynamics of hundreds of MPC neurons in monkeys
performing two isochronous tapping tasks, testing whether low-dimensional state network tra-
jectories can act as a neural clock during rhythmic tapping. Using dimensional reduction anal-
ysis, we found highly stereotyped neural trajectories that had two main properties during the
SCT. First, the three first principal components showed a periodic path for each produced
interval. Notably, these oscillatory state trajectories did not overlap across durations, a signa-
ture of temporal scaling; instead, they showed a linear increase in their radius and a constant
linear speed as a function of the target interval during metronome guidance (synchronization
condition [SC]), as well as during internally controlled rhythmic tapping (continuation condi-
tion [CC]). Second, the intertrial variability of the trajectories’ radial magnitude also increased
as a function of the interval, accounting for a key feature of timing behavior: the scalar prop-
erty, which states that the variability of produced or estimated intervals increases linearly as a
function of interval duration. These properties were highly resilient to the number of partici-
pating neurons and were replicated using simultaneously recorded cells during synchronized
tapping, but not during a serial reaction time-control task that precluded rhythmic prediction.
Finally, we found a tight correlation between the interval-associated changes in trajectory
amplitude and variability during SCT, the number of neurons involved in the sequential tran-
sient activation patterns, and the duration of the neural activation periods within these moving
bumps. Indeed, moving bumps simulations revealed that scaling the duration of the transient
period of activity and increasing the number of neurons participating in the evolving patterns
produced an increase in the radius and the variability of the corresponding neural trajectories,
replicating the empirical findings. These results suggest that rhythmic timing depends on the
radial amplitude of periodic state population trajectories in MPC, which in turn depend on the
number of neurons involved and the duration of these cells’ activation periods within moving
bumps.
Results
Rhythmic tapping behavior
We trained two monkeys (M01 and M02) in the SCT. M01 was also trained in two additional
tapping tasks: the synchronization task (ST) and the serial reaction time task (SRTT). During
SCT, the animals tapped on a push button in synchronization with a rhythmic metronome for
four times, thus producing three intervals (SC phase), followed by three internally generated
intervals (CC phase; Fig 1A). In the ST, the monkey produced five intervals guided by a metro-
nome, similarly to the SC of SCT (Fig 1B). During the SRTT, the animal pressed the button in
response to five brief visual stimuli presented in a sequence but separated by a random inter-
stimulus interval, precluding the prediction of the next stimulus-response loop (Fig 1C). Thus,
during SCT and ST, the animals entrained their rhythmic movements to a sensory
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 3 / 32
metronome, while in the CC of SCT, this was done to an internal representation of the same
rhythm. The asynchronies in the SC of SCT were (mean ± SD: 288.7 ± 70 ms). On the other
hand, the SRTT involved similar stimuli, tapping behavior, and sequential structure, but no
predictive rhythmic timing was possible. Expectedly, the reaction times were significantly
larger in the SRTT than the asynchronies in the ST (mean ± SD: 263 ± 37 ms in the ST and
381 ± 46 ms in the SRTT; ANOVA main effect of task: F(1, 718) = 1443.93, p < 0.0001). The
constant error, a measure of timing accuracy that corresponds to the difference between the
produced and the instructed interval, was slightly negative during SCT and ST, indicating that
the monkeys were able to properly produce the intervals with a small underestimation across
Fig 1. Tasks. A. SCT. The trial started when the monkey placed his hand on a lever for a variable delay. Then, a visual metronom e was
presented, and the monkey tapped on a button to produce three intervals of a specific duration following the isochron ous stimuli
(synchronizati on phase), after which the animal had to maintain the tapping rate to produce three addition al intervals without the
metronome (continuation phase). Correct trials were rewarded with an amount of juice that was proportional to the trial length. The
instructed target intervals were 450, 550, 650, 850, and 1,000 ms. B. ST. Similar to the synchroniz ation phase of the SCT, the animal
had to produce five intervals guided by a visual metronom e. The instruct ed intervals were 450, 550, 650, 750, 850, and 950 ms. C.
SRTT. As in ST, the trial started when the monkey placed its hand on a lever for a variable delay. However, in this task, the monkey
tapped the button after six stimuli separated by a random interstimulu s interval, precluding the tempora lization of the tapping
behavior. D. Constant error (mean ± SD/2) as a function of target interval during the SC (orange) and CC (red) of the SCT (ANOVA
main effect interval, F(4, 1,112) = 61.01, p < 0.0001; main effect task condition, F(1, 1,112) = 43.16, p < 0.0001; interval × condition
interaction, F(4, 1,112) = 17.66, p < 0.0001), and the ST (purple) as a function of target interval (ANOVA for 450, 550, 650, and 850
target intervals between SC of the SCT and the ST, main effect interval, F(3, 631) = 4.18, p < 0.01; main effect condition, F(1, 631) =
202.16, p < 0.0001; nonsignifi cant interval × condition interaction, F(3, 631) = 2.46, p = 0.06). Underlyin g data are availabl e in https://
doid.gin.g-no de.org/d315b 3db0cee 15869b3d9ed1 64f88cfa/. CC, continua tion condition; SC, synchroniz ation condition; SCT,
synchroniza tion-continu ation task; SRTT, serial reactio n time task; ST, synchroniza tion task.
https://doi.org/10 .1371/journal.p bio.3000054. g001
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 4 / 32
target durations (Fig 1D). Finally, the temporal variability (a measure of timing precision) dur-
ing the SCT and ST are depicted in Fig 2H and Fig 4E, respectively.
Neural state trajectories
We characterized the dynamics of the evolving response patterns using the projection of the
neural population time-varying activity onto a low-dimensional state space using principal
component analysis (PCA) on a population of 1,477 MPC cells recorded during SCT (see
Materials and methods, recording locations in S1 Fig). The results showed highly stereotyped
trajectories with a strong periodicity in the first three principal components (PCs) (Fig 2A–
2D). Indeed, PC2 and PC3 showed together a cyclic path for each produced interval (Fig 2C
and 2D). Each loop in the trajectory corresponded to the periodic network state variation dur-
ing the production of the rhythmic tapping sequence of the SCT. The circular trajectories in
the plane exhibited the tendency to start at the same position in the phase-space after each tap,
suggesting the existence of a movement-triggering point at a particular location in the popula-
tion trajectory across durations (see below). Crucially, from this common phase-space loca-
tion, longer intervals produced larger state trajectory loops, with a monotonic increase in the
trajectory radius as a function of target interval during both the SC and CC (Fig 2E). However,
the observed interval-dependent modulations in curvilinear amplitude were not accompanied
by modulations of the linear speeds of the periodic neural trajectories, as these remained con-
stant across durations (Fig 2F). The same properties were observed in PC1 and when the PCA
is computed from a subpopulation of neurons whose activity was task related (see S2 Fig).
Hence, contrary to a prototypical temporal scaling, in which there is a decrease in linear speed
as a function of interval and similar trajectory paths and traversed distances for different dura-
tions [24,34], the present results show that rhythmic timing during the SCT is represented as
an increase in curvature radii in the neural network state dynamics.
To test the relationship between the radius of the curvature in the neural-state trajectories
and the monkeys’ behavior during SC and CC, we split the produced intervals into two groups:
those in which the monkeys produced an inter-tap time that was below the 20th percentile,
and those with inter-tap times above the 80th percentile [21]. Strikingly, on those intervals in
which the monkeys tended to produce shorter inter-tap durations, the state trajectory radius
was smaller, and vice versa (Fig 2G).
Another important property of the curvilinear radii in the PCA neural trajectories was that
their variability (SD of the trajectory radii) followed the same linear increase as a function of
target interval observed in the monkeys’ behavior (Fig 2H). This linear relation between tem-
poral variability and interval duration, known as scalar property of interval timing, has been
widely reported in the timing literature, and our findings suggest that it depends on the radius
of the rotatory dynamical state of MPC neural populations during both SCT conditions. It is
important to mention that all the described properties in the neural trajectories are resilient on
the methods used to compute the PCs (see S3 Fig).
The dynamics in the MPC population activity during the SCT was also characterized using
demixed PCA (dPCA; Fig 3, see Materials and methods). This method not only captures most
of the variance in the neural data but, most importantly, also decomposes the dependencies of
the neural population activity into latent components associated with task parameters [30]. In
contrast, PCA only focuses on the total variance explained using orthogonal decomposition.
The first dPCA (dPCA1) showed a strong periodic structure with a minimum value around
the beginning of each produced interval in the SCT sequence, similar to the findings from the
PCA neural trajectories (Fig 2C and 2D). In addition, the dPCA1 showed a strong change in
amplitude with target duration (Fig 3A). Because we used time-normalized neural data as
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 5 / 32
Fig 2. Neural populati on trajectories during SCT and their oscillator y dynam ic properties. A, C. Projectio n of the neural activity in the MPC
(1,477 neurons) during the SC of the SCT onto the first (A) or second and third PCs (C). The first three PCs explained the 10.7%, 3.8%, and 2.3% of
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 6 / 32
input to the dPCA, all trials had the same length regardless of the target interval. In this sce-
nario, a scaling mechanism should have produced similar dPCAs across durations. Instead, we
observed a time-dependent modulation in dPCA1 amplitude. In order to compare the two
methods for dimensional reduction, we computed the bin-by-bin distance between the
450-ms and the other four target intervals (Fig 3D) using the PCAs (Fig 3B) and dPCA1 (Fig
3C). The resulting distance profiles are very similar between methods, with a periodic structure
whose amplitude mean and variability increased as a function of the target interval (Fig 3E and
3F). Thus, with a separate set of assumptions, the dPCA corroborates the existence of both the
periodic structure of the neural state dynamics and a beat-based timing mechanism based on
the amplitude modulation of the rotatory population trajectories during SCT.
The analyses described above were done on neurons recorded throughout different ses-
sions. Thus, as a next step we determine the neural state trajectories on simultaneously
recorded cells while monkey M01 performed an ST (Fig 1B) and an SRTT (Fig 1C). This strat-
egy not only allows us to validate the data of the SCT on the ST but also permits us to deter-
mine population dynamics on a trial-by-trial basis. As in the SCT, the PCA-projected activity
during the ST showed periodic state dynamics (Fig 4A; S4A Fig), whereas the SRTT neural tra-
jectories were not as periodic (Fig 4B; S4B Fig). In fact, the fitting of a normalized sinusoidal
function on the first PC was statistically more robust for ST than SRTT (in terms of mean
square error [MSE]: Fig 4C), even when the length of the inter-tap PCA-projected activity was
matched between different produced intervals (see Materials and methods). Again, the radius
of the neural trajectories during the ST showed a significant increase in both mean radius (Fig
4D, purple) and variability (Fig 4E), but a constant linear speed (Fig 4F), as a function of the
target interval, reproducing the findings in SCT. In contrast, the radius and variability of the
trajectories during SRTT showed small changes across target intervals, with a nonsignificant
linear fit as a function of target interval for the three parameters (Fig 4D, 4E and 4F, green).
This phenomenological comparison suggests that rhythmic tapping to a metronome depends
on the amplitude of the cyclic dynamics of population activity and that the shift from a predic-
tive to a reactive behavior during SRTT precludes the organization of periodic population state
trajectories.
The simultaneity of the recordings during ST [35] allowed for the decoding of the produced
intervals on a trial-by-trial basis. Using a time-delay neural network (TDNN; see Materials and
methods) (Fig 4G), we found that an ideal reader of the neural trajectories could predict
the total variance . Each point in the trajectory represents the neural network state at a particular moment. The trajectory complet es an oscillatory
cycle on every produced interval during the synchro nization and continua tion phases of the SCT. Target interval in millisecond s is color coded (450,
green; 650, blue; 1,000, red). Color progress ion within each target interval correspond s to the elapsed time. A cube indicates the beginning of each
trajectory, while an octahedron indicates the end. B, D. Projectio n of the neural activity during CC of the SCT onto the first (B) or the second and
third (D) PC. Color code is the same as (A). E. Monotoni c increase of the radii in the oscillatory neural trajectories during SC (orange, mean ± SD,
slope = 0.0009, constant = 0.0679, R
2
= 0.9, p = 0.01) and CC (red, mean ± SD, slope = 0.0009, constant = −0.0296, R
2
= 0.9, p < 0.01) as a function of
target interval. F. Linear speed of neural trajectori es during SC (orange, mean ± SD, slope = 0.0001, constant = 7.322, R
2
= 0.0007, p = 0.896) and CC
(red, mean ± SD, slope = 0.002, constant = 4.049, R
2
= 0.354, p = 0.002) as a function of target interval (ANOVA main effect interval, F(4, 39) =
92.15, p < 0.0001; main effect condition, F(1,39) = 381.46, p < 0.0001; interval × condition interaction, F(4, 39) = 15.15, p < 0.0001). The linear
speed was similar (SC) or showed a slight increase (CC) with the target interval. G. Neural trajectory radii for the top 20% (red, slope = 0.0011,
constant = −0.035, R
2
= 0.7, p < 0.0001) and bottom 20% (green, slope = 0.00088, constant = −0.009, R
2
= 0.75, p < 0.0001) inter-tap intervals across
target intervals. Note that on those intervals in which the monkeys tended to produce shorter inter-tap durations , the state trajectory radius was
smaller , and vice versa (ANOVA main effect interval, F(4, 40) = 155.7, p < 0.0001; main effect population, F(1, 40) = 33.3, p < 0.0001;
interval × population interaction, F(4, 40) = 3.98, p = 0.008). H. Variability (SD) of SCT rotational neural trajectories (orang e, mean ± SD,
normali zed data slope = 0.0019, constant = −1.02, R
2
= 0.94, p = 0.005) and the monkeys’ produced intervals (gray, mean ± SD, normaliz ed data
slope = 0.005, constant = −0.721, R
2
= 0.98, p = 0.0008) as a functio n of target interval. The Weber increase in tapping variabil ity was not statisticall y
differe nt from the increase in the variabil ity of neural trajectori es across target intervals (normaliz ed data, slope t test = 0.86, p = 0.42; constant t
test = 1.36, p = 0.22). Underlyin g data are available in https://d oid.gin.g-nod e.org/d315b3 db0cee15869b 3d9ed164f 88cfa/. a.u., arbitrary unit; CC,
continua tion condition; MPC, medial premotor cortex ; PC, principal compone nt; SC, synchroniz ation condition; SCT, synchroniz ation-
continua tion task.
https:// doi.org/10.1371 /journal.pbio .3000054.g002
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 7 / 32
Fig 4. Compar ison of ST and SRTT trajectories in simultaneo usly recorded neurons. A. Neural activity data projected on the PC1 (solid line,
linearly detrended) and the correspondent sinusoidal fit (dotted line) during a trial of ST for the target interval of 650 ms. B. Similar to (A) for SRTT.
Note that the strong periodic structur e of the ST neural trajectory is lost during SRTT for the same population of cells. C. The MSE of the sinusoidal fits
during ST (purple) is significan tly smaller than during SRTT (green; 60 trials, two-sample t test = −6.78, p < 0.0001). D. Radii of the neural trajectories
during ST (purple, slope = 0.000087, constant = 0.055, R
2
= 0.619, p < 0.0001) and SRTT (green, nonsigni ficant linear regression, R
2
= 0.0172 and
p = 0.489) as a function of target interval. E. Variability of the neural trajectories during ST (purple, data slope = 0.00003 7, constant = 0.028, R
2
= 0.368,
p < 0.0001), SRTT (green, nonsigni ficant linear regression, R
2
= 0.0005 and p = 0.903), and temporal variability of the monkeys ’ produced intervals
(gray, mean ± SD/2, data slope = 0.0009, constant = −0.003, R
2
= 0.999, p < 0.0001) across target intervals during ST. F. Linear speed of neural
trajectories during ST (purple, mean ± SD, slope = 0.0001, constant = 7.322, R
2
= 0.0007, p = 0.896) and SRTT (green, mean ± SD, slope = 0.002,
constant = 4.049, R
2
= 0.354, p = 0.002) did not change as a function of target interval. G. Output of the time-del ay neural network (TDNN, in blue)
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 8 / 32
accurately the tapping times during ST on 86% of the produced intervals. Indeed, the decoding
accuracy was better than the actual percent of correct trials in this demanding task (Fig 4H),
supporting the notion that the neural trajectories can robustly predict the rhythmic tapping
behavior.
trained to decode the duration of produced intervals based on the PC1 neural trajectories (orang e) during a target interval of 850 ms. Tapping times are
shown in yellow. H. TDNN error, defined as the difference between the produced and the decoded interval, as a function of produced interval. TDNN
predicted accurately the performance of the monkey on a trial-by-t rial basis (the decoded mean was not statistical ly differe nt from 0, t test = −0.5228,
p = 0.6). Underlyin g data are available in https://d oid.gin.g-nod e.org/d315 b3db0cee158 69b3d9ed164f 88cfa/. a.u., arbitrary unit; MSE, mean square
error; PC, principal component ; SRTT, serial reaction time task; ST, synchro nization task; TDNN, time-del ay neural network.
https://doi.o rg/10.1371/j ournal.pbio.30 00054.g004
Fig 3. dPCA applied to neural population activity during SCT. A, dPC1 of the dPCA of the neural activity associated with the target interval (explains 7.8% of
the total variance). Target interval in millisecond s is color coded (see inset A). The neural trajectories show oscillatory activity, and their amplitude varies across
target intervals. B,C. Euclidean distance between the first PC of the 450-ms target interval and the first PC of each target interval across time for (B) time-
normalized PCA and (C) dPCA. Target interval is color coded as in (A). Two-sam ple Kolmogo rov–Smirnov test on the distributi ons of PCA and dPCA
distances showed nonsignifi cant differences (p < 0.05) across target intervals. D. Distance calculati on diagram for PCA data. The inter-tap trajectori es for two
target intervals are shown (green, 450 ms; red, 1,000 ms). The 450-ms target interval trajectory is used as the referenc e for distance calculati on. The Euclidean
distance between each sequenti al bin is calculated among the reference interval and the other target intervals trajectories. Both population analyses, PCA and
dPCA, produced populati on signals with similar characteristi cs. Thus, oscillatory activity, modulation of the amplitude with the target interval, and an
intersectio n close to the tap time are characteristi cs of the underly ing neural populati on activity, irrespective of the dimension reduction algorithm. E. Mean
inter-tap Euclidean distance (mean ± SD) between the 450-ms and each target interval for the PCA data using PC1–3, (orang e) and dPCA using dPC1
(magenta) . There was no significan t difference between the slopes of PCA and dPCA (slope t test = 1.97, p = 0.0539) F. Variability of the distance between the
450-ms and each target interval for the PCA (orange) and dPCA (magent a). The variabil ity increased monotonically as a function of the target interval for both
analyses. Underlyin g data are available in https://d oid.gin.g-nod e.org/d315b3 db0cee15869b 3d9ed164f 88cfa/. a.u., arbitrary unit; dPCA, demixed PCA; PC,
principal compone nt; PCA, principal compone nt analysis; SCT, synchroniz ation-continu ation task.
https://do i.org/10.1371/j ournal.pbio. 3000054.g003
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 9 / 32
The population state dynamics are not related to the tapping kinematics
The cyclic and smooth nature of the neural trajectories during ST and SCT sharply contrast
with the kinematics of movement (Fig 5A, 5C and 5D), which is characterized by stereotypic
tapping movements separated by a dwell period that increased as a function of the target inter-
val (Fig 5E; [16,37]). These observations suggest that during rhythmic tapping, an explicit tim-
ing mechanism in MPC keeps track of the dwell time by setting in motion a continuous and
periodic change in the neural population state. According to this scheme, the tapping com-
mand is triggered once the state trajectories get to a specific position in the phase-space that
corresponds to the intersection point between the tangent circular paths whose radii increase
with the tapping tempo. To test the hypothesis, we computed the distance between a point in
state space and the position of the taps in the neural trajectory and found a similar distance
across target intervals (Fig 5B, see inset). In addition, the distance between the same point and
half inter-tap position increased as a function of target interval (Fig 5B). Therefore, these
results support the idea that the neural trajectories behave as tangent circles and encode the
dwell time between taps in the PC amplitude and trigger the stereotypic tapping movements
once the neural dynamics reach a point in state space (S5 Fig).
Distributed nature of the trajectories’ timing information
We determined whether we could extract information about the target interval from the neural
population dynamics, and how this information was modulated by the size of the neural popu-
lation used to compute the trajectories. To this end, we first segregated each segment of the
single-dimension trajectory according to the SCT target interval (450, 550, . . . 1,000 ms; see
insets in Fig 6A). Then, to capture the shape of the trajectory segments as a single three-dimen-
sional coordinate, we applied a second-layer PCA (PCA
0
) and kept the first three PCs. As a
result, we obtained a dot cloud in 3D, in which each point represents a particular produced
interval trajectory segment (Fig 6A). We trained support vector machines (SVMs) to classify
the cloud of points for the five target intervals of the SCT. We trained the SVM ten times and
used 5-fold cross-validation to evaluate the performance of the classifier. On the other hand,
each neuron was sorted according to the weight magnitude of the original PCAs. The neurons
with the largest PC participation were removed in steps of 10% from the original population
size, and the second-layer PCAs were computed on the new trajectories. Finally, the SVM was
carried out on the second-layer PCAs for different population sizes (see Fig 6). There was an
asymptotic decline in the classifier performance with the removal of a larger percentage of the
neural population (Fig 7A). However, even with very small populations (total cells: 15), the
classifier was able to extract all SCT target intervals above chance. These results are in line with
the idea that the temporal structure of rhythmic behavior depends on a neural population
code that is distributed within MPC.
Neural population trajectories and evolving activation patterns
The results of the previous section revealed a distributed representation of tapping tempo
across MPC cell populations. However, a critical question is what aspects of the time-varying
activity defined the changes in amplitude in the neural trajectories as a function of the timed
duration [28]. Based on our previous observations [4,21], we hypothesized that the evolving
patterns of neural activity could be directly linked with the time-encoding features of the neu-
ral trajectories during the SCT. Consequently, to test this idea we first characterized the prop-
erties of neuronal moving bumps [21,23,36] during this task. With this information we carried
out simulations to determine whether the key features of the moving bumps were linked to the
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 10 / 32
Fig 5. Neural trajectories do not follow the tapping kinemat ics. A. Diagram of the rotational trajectory of the SCT neural activity during three
inter-tap intervals: one 450-ms interval (green) and two 1,000-ms intervals (red). Each tap is numbered and projected in the trajectory as a white
circle. A blue triangle marks the beginning, whereas a yellow triangle marks the end of the movement time. The monkeys produced phasic
stereotypic movements whilst timing the dwell between taps during SCT [37]. B. Euclidean distance (d
t
, see inset) between an anchor point (red)
and the position of each tap (green, mean ± SD, slope = 0.00007, R
2
= 0.0633, p = 0.225), or half of the inter-tap interval position on the neural
trajectories (blue, mean ± SD, slope = −0.001, R
2
= 0.801, p < 0.0001) across target intervals for SC. A two-way ANOVA detected significan t main
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 11 / 32
observed changes in curvature radius and variability as a function of duration in the neural
state trajectories.
As expected, a substantial proportion of MPC cells during the SCT showed a progressive
pattern of activation in the neuronal population, consisting of a gradual response onset of sin-
gle cells within a produced interval (Fig 8, see Materials and methods). This activation pattern
started before a tap, migrated during the timed interval, and finished after the next tap (Fig 8).
In addition, a similar response profile was repeated in a cyclical manner for the three intervals
of SC and the three intervals of CC (Fig 8A and 8B) [4,21]. These findings suggest that rhyth-
mic timing can be encoded in the sequential activation of neural populations [23]. A central
question is what parameters of the neuronal response profiles are encoding the target interval
and the SCT condition. Remarkably, the number of neurons involved in these evolving activa-
tion patterns (Fig 8A and 8B, Fig 9C), as well as the duration of neural activation periods (Fig
9D), increased as a function of the target interval. SC showed a larger number of active cells,
whereas CC showed a longer activation period. In contrast, the neural recruitment lapse,
namely the time between pairs of consecutively activated cells (Fig 9E), and the cells’ discharge
rate (Fig 9F) did not show statistically significant changes across target intervals and task
phases. These results suggest that both the size of the circuits involved in measuring the pas-
sage of time and the duration of their activation times are core time-encoding signals in MPC,
and suggest the existence of a delicate balance between these two measures to produce the pro-
gressive activation profiles of neurons when tapping to a metronome or an internally gener-
ated rhythmic signal (Fig 9C and 9D).
Next, we simulated evolving patterns of population activity with different response profiles
and evaluated their translation onto PCA state space. First, we generated activity patterns on
individual units that were complex, heterogenous, and that scaled in time, producing activa-
tion periods with the same time-varying activity but different durations (Fig 10A, see Materials
and methods) [24]. Then, we simulated population cascade patterns for three consecutive
intervals, emulating two key features on the MPC population responses: a gradual response
onset of single cells that started before, migrated within, and finished after the end of an inter-
val, with a constant overall recruitment of cells over time; and the cyclical repetition of this
response profile for the three intervals (Fig 10C and 10D). In addition, Fig 11A shows that neu-
rons were added randomly in the intermediate portion of the simulated moving bumps when
effects on position (F(1, 40) = 1855.72, p < 0.0001), target interval (F(4, 40) = 77, p < 0.0001) and their interaction (F(4, 40) = 63.68, p < 0.0001).
Tukey HSD post hoc test showed that the distances of the anchor point to tap and half inter-tap positions were significant ly differe nt (p < 0.05).
In contrast, the anchor to tap distanc es across target intervals were not statisticall y different. Inset: scheme of the distance calculation; red sphere
marks the anchor point and two-sam ple inter-tap trajectories for 550 ms (dark gray) and 1,000 ms (light gray) are shown. The green sphere marks
the tap positio n and the blue sphere marks the half inter-tap positio n. Thus, the neural trajectori es converge on an attractor around the tap time,
to later diverge at half the inter-tap interval. Note that these results suggest the existence of tangent circular trajectories that converge in an
intersectio n zone close to the tapping moment, although their amplitude change d as a function of interval. C. Speed of the tapping moveme nt
(orange trace) from the second to the sixth tap of ST, and the PC1 projected neural information (cyan) for 26 simultaneous ly recorded neurons
during a trial with a target interval of 550 ms. Taps were repres ented as yellow squares and stimuli as red circles. Movement and dwell times are
depicted in green and magenta, respectively. D. Similar to (C) during an 850-ms target interval (PC1 projected neural information as a yellow
trace). E. Mean ± SD of the duration of the movement (green) and the dwell between movements (magenta) across target intervals, computed
from the speed profile of the tapping movements . A two-way ANOVA showed significant main effects on kinemati c state (movemen t/dwell
duration, F(1, 228) = 1,850.61, p < 0.0001), target interval (F(5, 228) = 272.72, p < 0.0001), and their interaction (F(5, 228) = 236.18, p < 0.0001).
Tukey HSD post hoc test showed that dwell durations across intervals were significan tly different (p < 0.05). Therefore , the monkey modulated
the dwell duration to successfull y temporali ze her behavior, while the down-pus h-up sequence of the tapping movement was phasic and
stereotypic across target intervals. F. Mean ± SD of the peak speed during the tapping movement as a function of the target interval during ST
(ANOVA main effect interval, F(5, 114) = 5.13, p < 0.001). The Tukey HSD post hoc test showed that only the peak speed of the 450-ms target
interval trials were significan tly different from the 650-, 750-, 850-, and 950-ms trials (p < 0.05). Underlyin g data are available in https://d oid.gin.
g-node.org/d 315b3db0c ee15869b3d 9ed164f88c fa/. a.u., arbitrary unit; d
h
, Euclidean distance of the anchor point to the half inter-tap position; d
t
,
Euclidean distance from the anchor point to the tap position; HSD, honestly significan t difference; PC, principal componen t; SCT,
synchroniz ation-continu ation task; ST, synchroniza tion task.
https://doi. org/10.1371/j ournal.pbio.3 000054.g005
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 12 / 32
Fig 6. Robustnes s in the classifier for SCT target interval using segmen ts of the PCA neural trajector y between taps with different neural
populati on sizes. A-C. Three principal component s projection of the second-laye r PCA
0
applied to each of the six inter-tap neural trajectory segments
and the five trial repetitions (see inset) for (A) 100%, (B) 50%, and (C) 1% of the neural populati on. Each dot in the second-la yer PCA
0
correspond s to
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 13 / 32
increasing the total number of neurons. The projection of the simulated cascades onto PCA
space produced oscillatory trajectories (Fig 10B), whose radii and variability increased but the
linear speed was similar with the target interval, as seen in the actual population responses.
Importantly, these properties were only followed when the simulated neural cascades included
an increase in both the number of neurons and the duration of the activation periods as a func-
tion of target interval (Fig 10E and 10F). Simulations with constant values in both parameters
produced PCA trajectories with similar radii or variability across interval durations, and a
decrease in speed with target interval consistent with the notion of temporal scaling (Fig 10E–
10G, Fig 11B–11E). Furthermore, the scaling of the response duration alone did not reproduce
the observed changes in radii and variability across durations in the state trajectories (Fig
11D–11E). These findings indicate not only a close relation between the properties of the
sequential neural patterns of activation and the neural state trajectories during rhythmic tap-
ping, but also suggest that an increment in the number of neurons engaged in the evolving pat-
terns of population activity is fundamental to reproducing the two critical duration-dependent
features of the PCA neural population trajectories: the increase in the magnitude and variabil-
ity of the radii as a function of target interval.
an inter-tap trajectory segment. Target interval color in the inset in (A). D-F. Distan ces between cluster centroids of data projection across target
intervals for (D) 100%, (E) 50%, and (F) 1% of the neural population. Underlyin g data are available in https://d oid.gin.g-nod e.org/
d315b3db0c ee15869b3d 9ed164f88c fa/. a.u., arbitrary unit; PC, principal compone nt; PCA, principal component analysi s; SCT, synchro nization-
continua tion task.
https://d oi.org/10.1371/j ournal.pbio. 3000054.g006
Fig 7. Trajecto ry classifier robustn ess across neural populati on sizes during SCT. A. SVM classifier performan ce (mean ± SD of percent of correct classificati ons)
for target interval (five instructed intervals) during the SCT task based on the neural trajectory computed from different population sizes. The total initial population
size was of 1,477 neurons. Dotted lines correspond to random level. The neurons with the largest PC partic ipation were removed in steps of 10% of the original
population size, until reaching 1% of the original population. Inset shows the original time-norma lized neural trajectory PC used to generate the second-laye r PCA
0
.
B. Point cloud in 3D for the second-l ayer PCAs’ for target interval. See color code in the inset. Note that the percentag e of correct classificati on decreased as a
function of the population size; however , the classificati on was above chance even for the trajectories based on small cell ensembles. Underly ing data are available in
https://doid.g in.g-node.org /d315b3db 0cee15869 b3d9ed164f8 8cfa/. a.u., arbitrary unit; PC, principal component s; PCA, principal component analysis; SCT,
synchroniz ation-continu ation task; SVM, support vector machine.
https://doi.org/10 .1371/journal.p bio.3000054 .g007
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 14 / 32
Discussion
The present study supports four conclusions. First, the time-varying discharge rate of MPC
cells shows a strong periodic organization when projected onto a two-dimensional state space,
generating a circular neural trajectory during each produced interval. The amplitude of this
trajectory increases with target duration and is closely related to the rhythmic tapping during
the SCT and ST, but not during the reactive tapping of SRTT. Second, the scalar property, a
hallmark of timing behavior, was accounted for by the variability of the curvilinear radii in the
PCA neural trajectories. Third, the population dynamics for simultaneously recorded MPC
cell populations during ST contained information to accurately decode the tapping times on a
trial-by-trial basis. Last, there is a strong correlation between the interval-associated changes in
radial magnitude and variability of the periodic neural trajectories during SCT and the number
of neurons involved in the sequential activation patterns, as well as the duration of their tran-
sient periods of activation within these moving bumps.
Rhythmic timing and the amplitude of neural state trajectories
The network state trajectories showed the following properties: they were simple, periodic,
exhibited an amplitude modulation according to the timed duration, and were different from
the stereotypic kinematics of the phasic tapping movements and the timing control of the
dwell between movements in this task [16,37]. Notably, the increases in trajectory amplitude
as a function of target interval were observed during the two rhythmic tapping tasks, repro-
duced with dPCA, and closely related with the monkeys’ produced intervals during SCT and
Fig 8. Overall patterns of activity in cell populations . A,B. Neural activation periods, sorted by their mean peak activation time, during the
SCT task for the target intervals of 450 (A) and 850 (B) ms. Each horizontal line corresponds to the onset and duration of the significan t
activation period of a cell according to the Poisson-train analysis (see Materials and methods) . The Poisson-trai n analysis was carried out on
the discharge rate of cells that was warped in relation to the tapping times (seven white vertical lines [4,73]). Note that the number of cells with
significant activation periods is larger for the longer target interval. Underlyin g data are available in https://d oid.gin.g-nod e.org/
d315b3db0c ee15869b3d 9ed164f88c fa/. SCT, synchroniza tion-continu ation task.
https://doi. org/10.1371/j ournal.pbio.3 000054.g008
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 15 / 32
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 16 / 32
ST. Furthermore, the switch from predictive rhythmic tapping to a reaction time task (SRTT)
produced a profound disorganization in the periodicity of neural trajectories, accompanied by
no changes in radial amplitude. In contrast with the temporal scaling model [24], we found
that the neural trajectories do not scale in time, because they present a time-related amplitude
modulation with similar linear speed profiles across durations. In line with our observations,
neural-network simulations of complex sensorimotor patterns showed that temporal scaling
of input stimuli produced curvilinear trajectories that increased in radii for longer intervals
[38]. Hence, amplitude modulations in neural population trajectories can be associated with
rhythmic timing [39] or complex temporal processing [38].
We found a strong correlation between the duration of the produced intervals and the cur-
vilinear amplitude of the MPC neural trajectories during the SCT and ST, and, due to the
simultaneity of the recordings in the latter task, we decoded accurately the produced durations
on a trial-by-trial basis. In addition, the cyclic and smooth nature of the neural trajectories
during ST and SCT sharply contrasts with the tapping kinematics, which are characterized by
stereotypic tapping movements separated by a dwell period that increases with the timed inter-
val [16,37]. Previous studies have demonstrated that cell populations in premotor and motor
cortical areas show rotatory non-muscle-like trajectories that reflect the internal dynamics
needed for controlling reaching and cycling [40,41]. Under this scenario, we found evidence
supporting the notion that the periodic MPC trajectories during rhythmic tapping encode the
dwell between taps in their curvilinear radii and that the tapping command is triggered when-
ever the trajectory reaches a specific phase-space, which corresponds to the intersection point
between the tangent circular paths. This dynamical geometry contrasts with the neural trajec-
tories of medial frontal areas during a single interval reproduction task [34]. In this interval-
based paradigm, the state trajectories not only evolve at different speeds but also generate par-
allel paths for different timed intervals, depending on the initial conditions of the neural popu-
lation dynamics [34]. Thus, the present data are consistent with the notion that timing is
encoded in a neural population clock [28,42–45] and puts forward the hypothesis that tempo-
ral processing during the entrainment to an isochronous metronome depends on the ampli-
tude of tangent circular trajectories in MPC populations. Under this scenario, temporal
processing is governed by MPC neural population clocks that switch from temporal scaling of
their state dynamics during interval timing to amplitude modulation in their tangent circular
trajectories during rhythmic timing. Importantly, because MPC is part of both the cortico-
basal ganglia and the cortico-cerebellar circuits, it can play an important role in both interval
and rhythmic timing and can act as a synergistic context-dependent element within the two
core timing systems, as suggested previously [46–49].
Fig 9. Evolving patterns of activation. A. Neural activation periods for the second produced interval (second and third taps as white vertical
lines) during SC for the target interval of 850 ms. The horizontal lines of each row correspond to the onset and extent of the activation
periods detected by the Poisson-train analysi s. Cells were sorted by their time of peak activity. B. Recruitment lapse as a function of cell
number. The activation lapse was the difference in the time of peak activity between contiguous cells in the neural avalanche . The mean
activation lapse (±SEM) was 2.98 ± 0.08 ms. C. Number of cells with significant activation periods across target intervals for SC (blue) and CC
(red). Avalanches for longer intervals recruited more cells (ANOVA main effect target interval, F(4, 20) = 21.1, p < 0.0001; main effect task
condition, F(1, 20) = 6.2, p < 0.02; interval × condition interaction, F(4, 20) = 0.71, p = 0.594). D. Duration of the activation periods during
the SC (blue) and CC (red) increased as a function of target intervals. (ANOVA main effect target interval, F(4, 20) = 18.9, p < 0.0001; main
effect task condition, F(1, 20) = 26.7, p < 0.0001; interval × condition interaction, F(4, 20) = 1.3, p = 0.268). E. Mean neural recruitme nt lapse
during SC (blue) and CC (red) did not change as a function of target interval (ANOVA main effect target interval, F(4, 20) = 2.7, p = 0.06;
main effect task condition, F(1, 20) = 3.4, p = 0.08; interval × condition interacti on, F(4, 20) = 0.79, p = 0.55). F. The discharge rate during
activation periods in SC (blue) and CC (red) did not vary across target intervals (ANOVA main effect target interval, F(4, 20) = 2.2, p = 0.06;
main effect task condition, F(1, 20) = 0.86, p = 0.35; interval × condition interaction, F(4, 20) = 0.92, p = 0.45). Underly ing data are available
in https://doi d.gin.g-nod e.org/d315b3db 0cee15869 b3d9ed164f8 8cfa/. CC, continua tion condition; SC, synchro nization condition.
https://d oi.org/10.1371/j ournal.pbio. 3000054.g009
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 17 / 32
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 18 / 32
Beat perception in humans is shaped by the temporal structure of extrinsic musical sound
and by the metrical interpretation that defines where a subject hears the beat. Thus, the percep-
tion of a beat and the corresponding movement entrainment depend on a mental interpreta-
tion of the metrics of music. The Dynamic Attending Theory (DAT) is one of the most
successful hypotheses to explain these phenomena. According to DAT, it is possible to match
the tapping movements to a beat during rhythmic entrainment because the periodic dynamics
of music drive our attention [50,51], allowing the prediction of the next pulse in the rhythmic
auditory sequence. The DAT suggests that attention is a dynamic process that can be success-
fully modeled by internal self-sustained oscillations in the auditory system [52,53]. These inter-
nal oscillations generate periodic shifts in attention to the most salient events in the sound
signal (the pulse that constructs an isochronous sequence in the musical stream), so that the
brain generates rhythmic expectations that correspond to the subjective interpretation of the
beat. Indeed, electroencephalogram recordings in auditory areas of humans have shown that
the brain oscillates at both the exogenous frequency of stimuli and at the metric interpretation
of the beat, providing strong support for DAT [54]. In addition, the perception of an inferred
musical beat in humans strongly engages the motor system, including the basal ganglia and
the MPC [55,56], supporting the notion that rhythmic perception and entrainment depend on
a dynamic interaction between the auditory and motor systems in the brain [15,43,57]. Conse-
quently, the present findings add important elements to these ideas, namely, neural popula-
tions in the motor system show cyclic dynamics whose period is tightly associated with the
tempo of the isochronous metronome, even when the metronome is turned off and the mon-
keys continue tapping with the same tempo. Hence, in accordance with DAT, the MPC neural
trajectories act as a neural oscillator, with a period similar to the tapping tempo during both
the sensory cued and the internally driven rhythmic tapping. Furthermore, in agreement with
the audiomotor hypothesis for beat perception and entrainment, our data suggest that preSMA
and SMA generate a periodic and predictive neural population signal that not only times the
inter-tap dwell and triggers the rhythmic tapping movement, but also may help the sensory
system to expect a specific temporal structure on the metronome [57,58]. However, a couple of
cautionary notes are in place here. First, monkeys can perceive and predictively synchronize to
isochronous metronomes [11,16,59]. We still do not know what the metrical hierarchy is that
monkeys can perceive and entrain to [11], but, definitively, nonhuman primates do not have
the flexibility to predictively perceive and entrain to a pulse across the range of tempi and
meters observed in humans [6]. Hence, our present data may generalize only to isochronous
rhythmic timing in humans. Second, monkeys show a bias to synchronize to visual rather than
Fig 10. Simulat ions of moving bumps and neural trajector ies. A. Activity profile of one simulated neuron during its activation period is scaled for
the five simulate d durations. B. Neural trajectories genera ted from the population activity of moving bumps simulatio ns. The number of neurons and
activation periods varied across intervals (see Materials and methods) . The simulated interval is color coded. Second and third simulate d taps are
marked as white spheres on each trajectory. C,D. Activation profiles of neurons for three consecutive simulated intervals with durations of 450 ms (C)
and 1,000 ms (D). The white vertical lines correspond to the tap events defining the intervals. The activation profiles follow a Gaussian shape of cell
recruitme nt, with slow activation rates at the tails (close to each tap). The number of neurons and the duration of the activation periods increased as a
function of simulated interval. E,F,G. Radii (E), variability (F), and linear speed (G) of the neural trajectori es generated from simulations . Data from
the simulate d neural activity with growing numbers of neurons and activation periods (expanding simulatio n: red), constant duration of activa tion
periods and constant number of neurons (static simulatio n: orange), and from the actual recorded population during SCT (blue) across target intervals.
Note that a constant was added to both simulatio n data in graphs. (E) Radii for simulatio n with expanding parameters (red, mean ± SD, slope = 0.0009,
R
2
= 0.811, p < 0.0001), simulation with static parameters (orange, mean ± SD, nonsignificant linear regressio n, slope = −0.0001, R
2
= 0.811, p = 0.214),
and actual neural activity (blue, mean ± SD, slope = 0.0009, R
2
= 0.897, p < 0.0001). The slopes of the radius, variabil ity, and linear speed were not
statistical ly differen t between the simulatio ns with expanding parame ters and the actual neuronal trajectories (radius slope t test = 0.15, p = 0.878;
variabil ity slope t test = 0.25, p = 0.803; linear speed slope t test = 1.8, p = 0.077). However, the slopes between the simulatio ns with constant parame ters
and neuronal trajectories showed statisticall y significant differences (radiu s slope t test = 9.13, p < 0.0001; variability slope t test = 3.73, p < 0.001;
linear speed slope t test = 17.71, p < 0.0001). Underlyin g data are available in https://d oid.gin.g-nod e.org/d315b3 db0cee15869b 3d9ed164f 88cfa/. a.u.,
arbitrary unit; PC, principal compone nt; SCT, synchroniz ation-con tinuation task.
https:// doi.org/10.1371 /journal.pbio .3000054.g010
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 19 / 32
Fig 11. Moving bump simulation parameters . A. Temporal positions of the activation periods of the neurons that were included to the
simulatio n of the 1,000-ms target interval trial (red), in addition to the position of the activation periods of neurons that also particip ated in the
450-ms simulation (shaded). B,C. Radius (B) and variabil ity (C) of PCA trajectori es generated from moving bump simulations when the
number of neurons was modified by a constant number (−100, green; −50, cyan; +50, yellow; and +100, red) from the original number of
neurons (208 neurons for 450-ms target interval, 220 neurons for 550-ms target interval, 230 neurons for 650-ms target interval, 270 neurons
for 850-ms target interval, and 282 neurons for 1,000-ms target interval; blue) while the activation period was kept constant at 257 ms across
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 20 / 32
auditory metronomes [16], whereas humans have a strong entrainment bias towards auditory
sequences, including music [1,14]. It has been suggested that the connections between the dor-
sal auditory regions and the motor planning areas via parietal cortex are stronger in humans
than in nonhuman primates, conferring the latter their larger ability for beat perception and
entrainment [15,57]. Therefore, it is quite possible that the neural state dynamics in the audio-
motor system of the Homo sapiens are more flexible and complex than what we report here.
The scalar property of timing and the state dynamics variability
The scalar property states that temporal variability increases linearly as a function of timed
duration [60]. This hallmark feature of temporal processing has been documented across
many timing tasks and species [20,60–63]. Several computational models based on neural pop-
ulation time representations have been implemented to describe this property, including drift
diffusion [64,65] and recurrent networks [36,66]. Here, we found that the variability in the
radii of neural trajectories increased as a function of target interval during SCT and ST, but
remained similar during the SRTT, a task that precludes time prediction while preserving the
sensory and tapping components. Therefore, these results suggest that the amplitude of the
MPC state-network trajectories is a feasible neural correlate of the scalar property during
rhythmic tapping.
The relation between neural trajectories and moving bumps during
rhythmic tapping
The dynamics of coordinated neural population activity define the evolution of the network
state trajectories, which in turn have revealed functional principles in a variety of behaviors
that are not evident at the single cell level [24,30,32,67]. Notably, the tapping tempo is strongly
mapped in the neural trajectories and is encoded in a distributed fashion, not dependent on a
particular response profile of individual neurons. Within this neural population framework,
we found large groups of neurons that showed sequential transient activation patterns that tra-
versed each produced interval during the SCT. Previous studies have reported moving bumps
as a timing mechanism in parietal cortex [68], MPC [4,21], the basal ganglia [23,69,70], and
hippocampus [71,72]. For example, the bump activity in the rat striatum during a peak interval
task moved progressively slower as the timed interval progressed, providing a functional basis
for the decrease in the animals’ timing accuracy as the length of the timed interval increased
[23]. In contrast, during the SCT we found that the rate of engagement of the neurons within
target intervals. A two-way ANOVA on the radius showed significan t main effects for number of neurons (F(4, 100) = 10,544.2, p < 0.0001),
target interval (F(4, 100) = 4,013.12, p < 0.0001), and their interaction (F(16, 100) = 25.8, p < 0.0001). Tukey HSD post hoc test showed
significan t difference s for the radii of all simulatio ns with different numbers of neurons and for all target intervals (p < 0.05). Additio nally, A
two-wa y ANOVA on the variability showed significan t main effects for number of neurons (F(4, 100) = 2,421.8, p < 0.0001), target interval (F
(4, 100) = 3,476.91, p < 0.0001), and their interacti on (F(16, 100) = 22.53, p < 0.0001). Tukey HSD post hoc test showed significant differences
for the variability of all simulations with different numbers of neurons (p < 0.05). D,E. Radius (D) and variability (E) of the trajectori es
genera ted from neural moving bumps in which the duration of the activation periods was reduced by 50% (short, green) or increased by 50%
(long, red) of the original scaled duration (197 ms for 450-ms target interval, 205 ms for 550-ms target interval, 213 ms for 650-ms target
interval, 233 ms for 850-ms target interval, and 257 ms for 1,000-ms target interval; blue) while the number of neurons was kept constant at
130 across target intervals. A two-way ANOVA on the variabil ity showed significan t main effects for activation duration (F(2, 60) = 3,081.54,
p < 0.0001), target interval (F(4, 60) = 2,801.16, p < 0.0001), and their interaction (F(8, 60) = 211.34, p < 0.0001). Tukey HSD post hoc test
showed significan t difference s for all simulations with different activation durations (p < 0.05). In addition , a two-way ANOVA on the
variab ility showed significant main effects for activation duration (F(2, 60) = 1,227.53, p < 0.0001), target interval (F(4, 60) = 257.49,
p < 0.0001), and their interaction (F(8, 60) = 24.87, p < 0.0001). Tukey HSD post hoc test showed significan t differences for all simulatio ns
with different activation durations (p < 0.05). Thus, the number of neurons and the activation duration within moving bumps produce large
change s in the radius and variability of the simulate d neural trajectories. a.u., arbitrary unit; HSD, honestly significan t difference; PCA,
principal component analysis.
https:// doi.org/10.1371 /journal.pbio .3000054.g011
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 21 / 32
moving bumps was constant and was accompanied by an increase in the number of neurons
participating in the evolving patterns of population activity. Thus, an optimal reader could
estimate the tempo of rhythmic tapping based on two signals: the location of the activity within
a bump, in which longer intervals engaged moving bumps composed of a larger number of
neurons, and the resetting between consecutive evolving activation patterns [65]. Strikingly,
our simulations revealed a tight relation between the scaling of the duration of the transient
period of activity, the increase in the number of neurons within moving bumps, and the
increase in radius and variability of the corresponding neural trajectories. The simulations also
suggest that neurons have the same relative position within a moving bump independently of
the timed interval, as seen previously in the rat striatum [23]. Consequently, the increase in
neural population size for longer intervals implies incorporation of new cells at intermediate
locations within the moving bump [21]. These results not only replicate our empirical observa-
tions but also support the notion that the properties of moving bumps, especially the number
of participating neurons, can shape the curvilinear amplitude and the corresponding variabil-
ity in neural state trajectories during SCT.
Conclusions
Overall, these findings support the notion that the rhythmic timing mechanism is based on the
changes in curvature radii of the neural population state dynamics in MPC, with slower tem-
pos encoded in larger traversed distances in the tangent periodic neural trajectories, and sug-
gest that the variability in these neural trajectories is a feasible neural substrate of the scalar
property during rhythmic tapping.
Materials and methods
Ethics statement
All the animal care, housing, and experimental procedures (protocol 090.A INB) were
approved by the Ethics in Research Committee of the Universidad Nacional Auto ´ noma de
Me ´ xico and conformed to the principles outlined in the Guide for Care and Use of Laboratory
Animals (NIH, publication number 85–23, revised 1985).
Subjects
Two monkeys (M01 and M02, Macaca mulatta, both males, 5–7 kg BW) were trained to tap
on a push button in SCT, ST, and SRTT. The monkeys were monitored daily by the research-
ers and the animal care staff to check their conditions of health and welfare.
Tasks
SCT. The SCT has been described before [14]. Briefly, the monkeys were trained to push a
button each time stimuli with a constant interstimulus interval were presented. This resulted
in a stimulus-movement cycle (Fig 1A). After four consecutive synchronized movements, the
stimuli were eliminated, and the monkeys had to continue tapping with the same interval for
three additional intervals. Monkeys received a reward (drops of juice) if each of the intervals
produced had an error <30% of the target interval. The daily performance of the monkeys was
>70% of correct trials. The amount of juice was proportional to the trial length. Trials were
separated by a variable intertrial interval (1.2–4 s). The target intervals, defined by visual sti-
muli (red square with a side length of 5 cm, presented for 33 ms), were 450, 550, 650, 850, and
1,000 ms. The target intervals were chosen pseudorandomly within a repetition. Five repeti-
tions were collected for each target interval.
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 22 / 32
ST. This task was similar to the synchronization phase of the SCT [16]. The subject had to
push a button with a stimulus. Six stimuli with a constant interstimulus were presented (red
square with a side length of 5 cm, shown for 33 ms). Thus, the metronome was always present
during the task. The target intervals were 450, 550, 650, 750, 850, and 950 ms. Five repetitions
were collected for each target interval.
SRTT. This task is also described elsewhere [14]. Monkeys were required to push a button
each time a stimulus was presented, but in this case the interstimulus interval within a trial was
random (picking randomly from the same 450, 550, 650, 750, 850, or 950 ms), precluding the
explicit temporalization of tapping (Fig 1B). Monkeys received a reward if the response time to
each of the five stimuli was within a window of 200 to 500 ms. The intertrial interval was as ST.
Visual (white square with a side length of 5 cm, presented for 33 ms) stimuli were used, and
five repetitions were collected.
Neural recordings
For the SCT, the extracellular recordings were obtained from the MPC of the monkeys using a
system with 7 or 16 independently movable microelectrodes (1–3 MO, Uwe Thomas Record-
ing, Germany, S3). Only correct trials were analyzed. All isolated neurons were recorded
regardless of their activity during the task, and the recording sites changed from session to ses-
sion. At each site, raw extracellular membrane potentials were sampled at 40 kHz. Single-unit
activity was extracted from these records using the Plexon offline sorter (Plexon, Dallas, TX).
Using the seven-electrode system, the number of simultaneously recorded cells ranged from 5
to 14 cells, whereas with the 16-electrode system the number ranged from 10 to 35 cells during
a recording session. In the present paper we analyzed the activity of 1,477 (1,074 of Monkey 1
and 403 of Monkey 2) MPC neurons in both monkeys. The functional properties of some of
these cells (1,083 neurons) have been reported previously [20,21,25]. In addition, using a semi-
chronic, high-density electrode system [35], 26 and 41 MPC cells were recorded simulta-
neously while Monkey 1 was performing the ST and SRTT tasks. All the isolated neurons were
recorded regardless of their activity during the SCT, ST, and SRTT, and the recording sites
changed from session to session.
Neural activation periods
We used the Poisson-train analysis to identify the cell activation periods within each interval
defined by two subsequent taps. This analysis determines how improbable it is that the number
of action potentials within a specific condition (i.e., target interval and ordinal sequence) was a
chance occurrence. For this purpose, the actual number of spikes within a time window was
compared with the number of spikes predicted by the Poisson distribution derived from the
mean discharge rate during the entire recording of the cell. The measure of improbability was
the surprise index (SI), defined as follows:
SI ¼   logP
where P was defined by the Poisson equation:
P ¼ e
  rT
X
1
i¼n
ðrT Þ
i
i!
where P is the probability that, given the average discharge rate r, the spike train for a produced
interval T contains n or more spikes in a trial. Thus, a large SI indicates a low probability that a
specific elevation in activity was a chance occurrence. This analysis assumes that an activation
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 23 / 32
period is statistically different from the average discharge rate r, considering that the firing of
the cell is following a nonhomogenous Poisson process (see also [73]). The detection of activa-
tion periods above randomness has been described previously [4,74]. Importantly, the Pois-
son-train analysis provided the response-onset latency and the activation period for each cell
and for each combination of target interval/serial order.
Neural trajectories
Event time normalization and binarization. We developed a time-normalization algo-
rithm to align the neural data from different tapping times of different recording sessions in
the same relative time framework. For each neuron, we calculated the produced interval (time
between two taps). Then, we subtracted the time of the second tap of a produced interval in
the task sequence from all spike and stimulus times (event
times
) and divided them by the pro-
duced interval. The tapping times acquired values of minus one and zero, and all the other
event
times
were normalized between these two values. Finally, we added the tap sequence num-
ber. Thus, all the normalized values for movement, sensory, and spike events acquired values
between zero and seven in an SCT trial, as follows:
ti me nor mal ize d even t ¼
ðeven t ti me   tap tim eÞ
pr oduce d int er val
þ tap sequ ence
Therefore, the time range of events between the first and the last tap of the normalized data
of a trial (unit time normalized data [UTND]) was the same regardless of the target interval. In
addition to the trial relative time framework, we also used the target interval normalized data
(TIND), which corresponds to the UTND multiplied by the target interval. This time-normali-
zation procedure was not necessary for simultaneously recorded data.
Trial binarization. For UTND, TIND, and simultaneously recorded data, we divided the
neural data in bins by calculating the discharge rate on consecutive windows of 0.02 units. For
UTND, we always got 50 bins between each pair of taps across target intervals, whereas for
TIND and the simultaneously recorded data, this number depended on the target interval of
the trial. For example, the total number of bins was 23 and 50 for trials with the 450- and
1,000-ms intervals, respectively. The binned data of each neuron were divided by the maxi-
mum discharge rate of that particular neuron across all repetitions and target intervals of the
SCT. We did not use this time-normalization algorithm on the ST and SRTT data.
Principal component coefficients matrix. Given a linear transformation of a matrix X
into a matrix Y, such that each dimension of Y explains variance of the original data X in
descending order, PCA can be described as the search for matrix P that transforms X into Y,
as follows:
Y ¼ PX
Hence, we first calculated the matrix P using a matrix X that includes all trials and target
interval combinations for the visual SCT of our UTND cell population. Using this P on other
data guarantees that the same transformation is applied to different neural activity sets. There-
fore, using the UTND framework we avoided over- or underrepresentation of the information
for different target intervals, due to the constant total number of bins across conditions.
Generating neural trajectories
The TIND information for every trial of all neurons constituted the columns of the X’ matrix.
The principal component coefficients matrix P were multiplied by the X’ matrix to transform
the neural data into the space of the original Y. Using the same transformation matrix for each
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 24 / 32
trial allowed the comparison of trajectories for different trials and tasks. A locally weighted
scatterplot smoothing function was applied to the columns of the Y matrix. The first three
dimensions of Y were used to generate graphical three-dimensional trajectories, while the first
eight dimensions, which explained at least 1% of the variance, were used for the other analysis.
Trajectory radius and variability
The first three PCs explained 10.7%, 3.8%, and 2.3% of the total variance. These three first PCs
produced highly stereotyped trajectories with a strong periodicity. In addition, the PC2 and
PC3 showed a strong oscillatory structure with a phase difference of π/2 radians during SCT.
For these two PCs, we calculated the centroids of the segments of trajectories between adjacent
taps. We measured the radius of the 2D trajectory segment as the mean of the Euclidean dis-
tances between the centroid and each point in the trajectory segment. The variability of the tra-
jectory was calculated as the standard deviation of the Euclidean distances between the
centroid and each point in the trajectory segment across the six serial order elements (three of
the SC and three of the CC) for each target interval. Accordingly, the temporal variability of
the behavior for each target interval was computed as the standard deviation of the produced
intervals within a trial, namely the across-six-serial-order elements of the SCT.
Neural trajectory decoder
We trained a TDNN [75] to decode the produced intervals from the first PC of the simulta-
neously recorded neural activity during ST. The TDNN architecture had an input layer with
20 time delays and one hidden 10-unit layer. The output layer consisted of a single unit that
was trained to generate a value of 1 when a tap occurred, or 0 otherwise. We trained the net-
work using a Bayesian regularization backpropagation algorithm that minimized the mean
squared error of the output. The tap time was defined as the time of the peak of the neural net-
work output higher than a threshold of 0.12. We considered a correctly decoded interval when
the decoded and the produced taps times’ difference was less than 60 ms. We used 5-fold
cross-validation to evaluate the performance of the neural network.
dPCA
The dPCA method finds separate decoder (F) and encoder (D) matrices for each task parame-
ter (;) by minimizing the loss function,
L
dPCA
¼
X
;
kX
;
  F
;
D
;
X k
2
where X is a linear decomposition of the data matrix, which contains the instantaneous firing
rate of the recorded neurons, into parameter-specific averages:
X ¼
X
;
X
;
þ X
no ise
The decoder and encoder axes permit us to reduce the data into a few components captur-
ing the majority of the variance of the data dependent on each task parameter [30].
We used the TIND resampled to 30 bins for all target intervals as the input data to the
dPCA, and the target interval as the marginalization parameter. Therefore, the length of all the
trials for all target intervals was the same. We calculated the bin-by-bin Euclidean distance
between the 450-ms first PC and all the target intervals using the PCA and dPCA analyses.
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 25 / 32
SVM classifier
We were interested in studying the relation between the neural trajectory dynamics and the
instructed interval of the SCT (450 ms, 550 ms, . . . 1,000 ms). Therefore, we first normalized
the length of each segment of the first eight PCs of the neural trajectory associated with a pro-
duced interval (the time between two taps) to 30 bins (see inset, Fig 7A). This step was neces-
sary to avoid a bias associated with the length of the segment. Then, we applied a second-layer
PCA
0
to each of the original neural trajectory segments for each PC independently. We kept
the first three PCs, as they explained 96% of the variance. As a result, a point in a new three-
dimensional coordinate for each 30-bin trajectory segment was obtained (see Fig 7B). In order
to assess which PC had more information about each of the SCT parameters, we carried out a
classification procedure for each PC using an SVM algorithm [76]. Each classifier was
retrained 10 times, and we used 5-fold cross-validation to evaluate the performance of the clas-
sifier. Thus, we identified the PC with more information for each SCT parameter and called it
best-PC.
Additionally, we were interested in studying how the size of the neural population used to
generate the PCA affected the information contained in the trajectory. We sorted each neuron
according to the magnitude of the PCA weights for the best-PC. We iteratively removed the
activity of 10% of the neurons with the largest PCA weights for the best-PC until reaching 1%
(15 total neurons). Finally, for each population size, we computed the second-layer PCAs on
the new trajectories and the corresponding SVM classification.
Oscillatory activity analysis
To characterize the phase, frequency, and amplitude of the neural trajectories, we calculated a
series of nonlinear regression models over the residuals of linear regressions on the first PC
projected data. Each inter-tap segment of the projected data was resampled to 30 bins and
time normalized to 1 s before calculating the regressions. The general function of the nonlinear
models was as follows:
PC ¼ a � sineð2 p � t þ cÞ þ d
where t is time. In addition, the parameter a is the amplitude of the oscillatory function, c the
phase offset, and d is a constant. For each trial of both tasks (ST and SRTT), we calculated the
MSE.
Movement kinematics
We applied the Lucas-Kanade optic flow method to measure the monkey’s arm speed during
the ST. This method calculates a flow field from the intensity changes between two consecutive
video frames. The analyzed video was recorded with a Microsoft Kinect for Windows camera
with a 640 × 480 resolution. The optic flow method was applied to a smaller area of 141 × 141
pixels from the original video that contained the monkey’s arm during the whole trial, and no
other moving objects. The arm’s movement velocity vector was calculated across all frames as
the magnitude of the sum of all the individual flow fields vectors whose magnitude was larger
than a predefined threshold. The velocity vector was calculated from the first to the last tap on
each correct trial. We reported the speed as the magnitude of the velocity vector. Posteriorly,
the kinematic state of the arm was tagged as movement when the velocity vector was larger
than a threshold or dwell otherwise. The tagging algorithm considered a change on the kine-
matic state when the new state lasted longer than three consecutive frames.
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 26 / 32
Moving bumps simulations
In order to investigate how the properties of the pattern of neuronal activation affected the
generation of population neuronal trajectories, we generated five repetitions of simulations of
neuronal activity for each target interval. The individual neuronal activation period was com-
posed of the sum of 20 random gamma functions. The activation period was constant for all
the neurons on one simulation, but varied with the target interval: 197-, 205-, 213-, 233-, and
257-ms activation durations for 450-, 550-, 650-, 850-, 1,000-ms target intervals, respectively.
The initial activation time for each neuron was adjusted so that the population activation rate
followed a Gaussian function as to produce a moving bump pattern. The number of neurons
in the simulation was incremented according to the target interval (450 ms, 108 neurons; 550
ms, 120 neurons; 650 ms, 130 neurons; 850 ms, 170 neurons; 1,000 ms, 182 neurons). Fig 11A
shows neurons were added randomly in the intermediate portion of the moving bumps.
Supporting information
S1 Fig. Location of the silicon shank for the MPC recordings in Monkey 1 during the ST.
MRI cortical surface reconstruction of the macaque brain and the recording position of the
Buszaki-64 silicon shank over MPC. The green line corresponds to the anterior-posterior loca-
tion of the spur of the arcuate sulcus that divides preSMA from SMA. The silicon shank was
implanted according to this landmark, so that four more anterior shanks were located in pre-
SMA and other four posterior shanks in SMA. For the recording locations of MPC in Monkeys
1 and 2 during SCT, see Fig 1B of Merchant and colleagues, 2011. AS, arcuate sulcus; CS, cen-
tral sulcus; IPS, intraparietal sulcus; MPC, medial premotor cortex; preSMA, pre-supplemen-
tary motor cortex; PS, principal sulcus; SMA, presupplementary motor cortex proper; ST,
synchronization task.
(TIF)
S2 Fig. Neural population trajectories during SCT from a subpopulation of cells with task-
related activity. The PCA was performed on the time-varying activity of 104 cells that showed
at least 15 activation periods on the Poisson-train analysis across the five target durations and
six serial order elements of the SCT. The first three PCs explained 32.5% of the total variance.
A. Projection of the neural activity during the SC and CC of SCT onto the first three PCs. The
trajectory completes an oscillatory cycle on every produced interval during the synchroniza-
tion and continuation phases of the SCT. Target interval in milliseconds is color coded (450,
green; 650, blue; 1,000, red). Color progression within each target interval corresponds to the
elapsed time. A cube indicates the beginning of each trajectory, while an octahedron indicates
the end. B. Linear increase of the radii in the oscillatory neural trajectories during SC and CC
(mean ± SD, slope = 0.0003, constant = 0.2, R
2
= 0.7, p < 0.0001) as a function of target inter-
val. C. Linear speed of neural trajectories during SC and CC (mean ± SD, slope = −0.002, con-
stant = 6.3, R
2
= 0.42, p = 0.001) as a function of target interval. D. Variability of neural
trajectories (mean ± SD, normalized data slope = 0.0002, constant = −0.05, R
2
= 0.87,
p < 0.0001) as a function of target interval. Underlying data are available in https://doid.gin.g-
node.org/d315b3db0cee15869 b3d9ed164f88cfa/. CC, continuation condition; PC, principal
component; PCA, principal component analysis; SC, synchronization condition; SCT, syn-
chronization-continuation task.
(TIF)
S3 Fig. Effect of timing and firing rate normalization on the amplitude and speed of neural
trajectories. We used different combinations of the time and firing rate normalization of the
neural data in order to calculate the PCA coefficients and then the neural trajectories. We
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 27 / 32
fitted a sine function on each of the first 10 PCs and measured their amplitude and speed. For
all the possible normalization combinations, we found at least one of the first three PCs that
showed a robust fit of the sine function that was accompanied by a monotonic increase in the
mean and the variability of the trajectory radius and a similar speed across target intervals.
Here, we show only one PC for each normalization combination (see A, C, E, G). (A-F) These
were generated using normalized firing rate data to calculate the trajectories. The left row cor-
responds to PC radial amplitude and the right row to the PC linear speed. A,B. Coefficients
computed with time normalized but trajectories calculated on actual time bins, as presented
across this paper for SCT. (A) PC amplitude increased with target interval: PC3, data
slope = 0.00081, constant = 0.011, R
2
= 0.899, p < 0.0001, ANOVA main effect target interval,
F(4, 20) = 128.69, p < 0.0001. (B) PC linear speed is similar across target intervals: PC3, non-
significant linear regression, R
2
= 0.07, p = 0.201, ANOVA main effect target interval, F(4, 20)
= 22.12, p < 0.0001.
C,D. Coefficients and trajectories are computed using time-normalized data. (C) PC1, data
slope = 0.0012, constant = −0.651, R
2
= 0.902, p < 0.0001, ANOVA main effect target interval,
F(4, 20) = 875.21, p < 0.0001. (D) PC1, data slope = 0.0048, constant = −1.638, R
2
= 0.98,
p < 0.0001, ANOVA main effect target interval, F(4, 20) = 390.94, p < 0.0001. E,F. Coefficients
and trajectories are computed using actual time data. (E) PC1, data slope = 0.00084, constant
= −0.225, R
2
= 0.899, p < 0.0001, ANOVA main effect target interval, F(4, 20) = 332.76,
p < 0.0001. (F) PC1, data slope = 0.0034, constant = 0.641, R
2
= 0.686, p < 0.0001, ANOVA
main effect target interval, F(4, 20) = 100.04, p < 0.0001. G,H. Same as (A,B) but using non-
normalized firing rate data to calculate the trajectories. (G) PC2, data slope = 0.175, con-
stant = 62.162, R
2
= 0.625, p < 0.0001, ANOVA main effect target interval, F(4, 20) = 27.58,
p < 0.0001. (H) PC2, nonsignificant linear regression, R
2
= 0.089, p = 0.145, ANOVA main
effect target interval, F(4, 20) = 8.18, p < 0.001. Underlying data are available in https://doid.
gin.g-node.org/d315b3db0cee 15869b3d9ed164f88cfa/. PC, principal component; PCA, princi-
pal component analysis; SCT, synchronization-continuation task.
(TIF)
S4 Fig. State trajectories during ST and SRTT using simultaneously recorded neurons. A,
B. Three-dimensio nal neural dynamics trajectory of 650-ms single ST (A) and SRTT (B) inter-
vals. Elapsed time is color coded. The previous and the next taps are marked as red and white
spheres, respectively. The stimuli are marked as a white pyramid. Underlying data are available
in https://doid.gin.g-n ode.org/d315b3db0cee15869b3d9e d164f88cfa/. SRTT, serial reaction
time task; ST, synchronization task.
(TIF)
S5 Fig. State trajectory progress during SCT. A,B. One trajectory loop for the second pro-
duced interval of the (A) SC and (B) CC, during 450-ms (dark gray) and a 1,000-ms (light
gray) target intervals. Trajectory progression marked as colored spheres is as follows: previous
tap (green), first inter-tap quarter (cyan), second inter-tap quarter/half interval (blue), third
inter-tap quarter (yellow), and next tap (red). Therefore, the neural trajectories follow circular
paths with different radii that increase according to the target interval, but with similar speed
profiles. Underlying data are available in https://doid.gin.g-node.o rg/
d315b3db0cee15869b3d9ed16 4f88cfa/. CC, continuation condition; SC, synchronization con-
dition; SCT, synchronization-continuation task.
(TIF)
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 28 / 32
Acknowledgmen ts
We thank Victor de LaFuente, Ranulfo Romo, and Roman Rossi for their fruitful comments
on the manuscript. We also thank Raul Paulı ´ n for his technical assistance. Jorge Ga ´ mez is a
doctoral student from Programa de Doctorado en Ciencias Biome ´ dicas, Universidad Nacional
Auto ´ noma de Me ´ xico (UNAM), and received fellowship 339118 from CONACYT.
Author Contributions
Conceptualization: Jorge Ga ´ mez, Hugo Merchant.
Data curation: Jorge Ga ´ mez, Abraham Betancourt, Hugo Merchant.
Formal analysis: Jorge Ga ´ mez, Abraham Betancourt, Hugo Merchant.
Funding acquisition: Hugo Merchant.
Investigation: Jorge Ga ´ mez, Germa ´ n Mendoza, Luis Prado, Hugo Merchant.
Methodology: Jorge Ga ´ mez, Germa ´ n Mendoza, Luis Prado, Hugo Merchant.
Project administration: Luis Prado.
Software: Jorge Ga ´ mez, Abraham Betancourt, Hugo Merchant.
Supervision: Germa ´ n Mendoza, Luis Prado, Hugo Merchant.
Validation: Hugo Merchant.
Visualization: Hugo Merchant.
Writing – original draft: Jorge Ga ´ mez, Hugo Merchant.
Writing – review & editing: Jorge Ga ´ mez, Germa ´ n Mendoza.
References
1. Patel AD. The Evolutiona ry Biology of Musical Rhythm: Was Darwin Wrong? PLoS Biol. 2014; 12(3): 1–
6. https://doi.o rg/10.1371/jo urnal.pbio.1 001821 PMID: 24667562
2. Teki S, Grube M, Kumar S, Griffiths TD. Distin ct neural substrates of duration-b ased and beat-base d
auditory timing. J Neurosc i. 2011; 31(10): 3805–3812. https:// doi.org/10.15 23/JNEU ROSCI.5561 -10.
2011 PMID: 213892 35
3. Grahn JA. Neuroscient ific Investigation s of Musical Rhythm: Recent Advances and Future Challeng es.
Contemp Music Rev. 2009; 28(3): 251–277. https://doi. org/10.1080/0 7494460 903404360
4. Merchant H, Pe ´ rez O, Bartolo R, Me ´ ndez JC, Mendoza G, Ga ´ mez J, et al. Sensorimo tor neural dynam-
ics during isochronous tapping in the medial premotor cortex of the macaque. Eur J Neurosc i. 2015; 41
(5): 586–602. https://doi. org/10.1111/e jn.1281 1 PMID: 25728178
5. Phillips-Si lver J, Traino r LJ. Hearing what the body feels: Audito ry encoding of rhythmic movement.
Cognition . 2007; 105(3): 533–546. https://doi.or g/10.1016/ j.cognition.2006 .11.006 PMID: 171965 80
6. Fitch WT. Rhythmic cognition in humans and animals: distinguish ing meter and pulse perception. Front
Syst Neurosci. 2013; 7: 68. https://doi.or g/10.3389 /fnsys.2013.0 0068 PMID: 24198765
7. Merchant H, Grahn J, Trainor L, Rohrmeier M, Fitch WT. Finding the beat: a neural perspectiv e across
humans and non-hum an primates. Philos Trans R Soc Lond B Biol Sci. 2015; 370(1664) : 20140093.
https://doi.or g/10.109 8/rstb.201 4.0093 PMID: 2564651 6
8. Repp BH. Sensor imotor synchronizat ion: A review of the tapping literature. Psychon Bull Rev. 2005; 12
(6): 969–992. https://doi. org/10.3758/B F03206 433 PMID: 16615317
9. Repp BH, Su Y-H. Sensorimot or synchroniz ation: A review of recent research (2006–2012 ). Psychon
Bull Rev. 2013; 20(3): 403–452. https:/ /doi.org/10.37 58/s1342 3-012-037 1-2 PMID: 23397235
10. Honing H, Merchant H, Ha ´ den GP, Prado L, Bartolo R. Rhesus Monkeys (Macaca mulatta) Detect
Rhythmic Groups in Music, but Not the Beat. PLoS ONE. 2012; 7(12): e51369. https://doi.or g/10.1371/
journal.pon e.00513 69 PMID: 23251509
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 29 / 32
11. Honing H, Bouwer FL, Prado L, Merchant H. Rhesus Monkey s (Macaca mulatta) Sense Isochrony in
Rhythm, but Not the Beat: Additional Support for the Gradual Audiom otor Evolution Hypothes is. Front.
Neurosci. 2018; 12: 475. https://doi.or g/10.338 9/fnins.201 8.00475 PMID: 300618 09
12. Hoesche le M, Merchant H, Kikuchi Y, Hattori Y, ten Cate C. Searching for the origins of musica lity
across species. Philos Trans R Soc Lond B Biol Sci. 2015; 370(1664) : 201400 94. https://doi.or g/10.
1098/rstb .2014.0094 PMID: 25646517
13. Ayala YA, Lehmann A, Merchant H. Monkeys share the neurophys iological basis for encoding sound
periodicities captured by the frequency - following response with humans. Sci Rep. 2017; 7(1): 16687.
https://doi.or g/10.103 8/s41598 -017-16774 -8 PMID: 29192170
14. Zarco W, Merchant H, Prado L, Mendez JC. Subsecon d timing in primates: comparison of interval pro-
duction between human subjects and rhesus monkey s. J Neuroph ysiol. 2009; 102(6): 3191–3202.
https://doi.or g/10.115 2/jn.00066.20 09 PMID: 19812296
15. Merchant H, Honing H. Are non-human primates capable of rhythmic entrainm ent? Evidence for the
gradual audiomo tor evolution hypothesis . Front Neurosci. 2014; 7: 274. https://doi.or g/10.338 9/fnins.
2013.00274 PMID: 24478618
16. Ga ´ mez J, Yc K, Ayala YA, Dotov D, Prado L, Merchant H. Predict ive rhythmic tapping to isochrono us
and tempo changing metronome s in the nonhuma n primate. Ann N Y Acad Sci. 2018; 1–20. https://doi.
org/10.1111/ nyas.13671 PMID: 29707785
17. Merchant H, Georgopo ulos AP. Neuroph ysiology of Perceptual and Motor Aspects of Intercepti on. J
Neuroph ysiol. 2006; 95(1): 1–13. https://doi.or g/10.115 2/jn.00422.200 5 PMID: 16339504
18. Kotz SAE, Schwartz e M. Differentia l Input of the Supplement ary Motor Area to a Dedicated Tempora l
Processin g Network: Functiona l and Clinical Implications . Front Integr Neurosc i. 2011; 5: 86. https://
doi.org/10.33 89/fnint.2011. 00086 PMID: 22363269
19. Merchant H, Harrington DL, Meck WH. Neural Basis of the Perception and Estimation of Time. Annu
Rev Neurosci. 2013; 36: 313–336. https://doi. org/10.1146/a nnurev-neu ro-062012-1703 49 PMID:
23725000
20. Merchant H, Pe ´ rez O, Zarco W, Ga ´ mez J. Interval tuning in the primate medial premotor cortex as a
general timing mechan ism. J Neurosci. 2013; 33(21): 9082–9 096. https://doi.or g/10.152 3/
JNEUROS CI.5513-1 2.2013 PMID: 236995 19
21. Crowe DA, Zarco W, Bartolo R, Merchant H. Dynamic Representa tion of the Tempora l and Sequential
Structure of Rhythmic Movem ents in the Primate Medial Premoto r Cortex. J Neurosci. 2014; 34(36):
11972–11983 . https://doi.or g/10.1523/ JNEUROSCI.2 177-14. 2014 PMID: 25186744
22. Bartolo R, Prado L, Merchant H. Informatio n Processin g in the Primate Basal Ganglia during Sensory-
Guided and Internally Driven Rhythmic Tapping . J Neurosci. 2014; 34(11): 3910–3923. https://doi.or g/
10.1523/ JNEUROSCI.2 679-13. 2014 PMID: 24623769
23. Mello GBM, Soares S, Paton JJ. A Scalable Population Code for Time in the Striatum. Curr Biol. 2015;
25(9): 1113–1122. https:// doi.org/10.10 16/j.cub.20 15.02.03 6 PMID: 25913405
24. Wang J, Narain D, Hosseini EA, Jazaye ri M. Flexible timing by temporal scaling of cortical response s.
Nat Neurosci. 2018; 21(1): 102–110 . https://doi.or g/10.1038/ s41593-017- 0028-6 PMID: 292038 97
25. Merchant H, Zarco W, Pe ´ rez O, Prado L, Bartolo R. Measurin g time with differe nt neural chronomet ers
during a synchronizati on-conti nuation task. Proc Natl Acad Sci U S A. 2011; 108(49): 19784– 19789.
https://doi.or g/10.107 3/pnas.11 12933108 PMID: 221062 92
26. Knudsen EB, Powers ME, Moxon KA. Dissociating Movem ent from Movement Timing in the Rat Pri-
mary Motor Cortex. J Neurosci. 2014; 34(47): 15576–15 586. https://doi.or g/10.152 3/JNEURO SCI.
1816-14.201 4 PMID: 25411486
27. Jazayeri M, Shadlen MN. A Neural Mechanism for Sensing and Reprodu cing a Time Interval. Curr Biol.
2015; 25(20): 2599–26 09. https://doi.or g/10.1016 /j.cub.2015 .08.038 PMID: 264553 07
28. Merchant H, Bartolo R. Primate beta oscillation s and rhythmic behavio rs. J Neural Transm. 2018; 125
(3): 461–470. https://doi. org/10.1007/s 00702-017- 1716-9 PMID: 28364174
29. Cunningh am JP, Yu BM. Dimens ionality reduction for large-s cale neural recordings. Nat Neurosci.
2014; 17(11): 1500–15 09. https://doi.or g/10.1038 /nn.3776 PMID: 251512 64
30. Kobak D, Brendel W, Consta ntinidis C, Feierstein CE, Kepecs A, Mainen ZF, et al. Demixe d principal
component analysis of neural populat ion data. Elife. 2016; 5: 1–36. https://doi.or g/10.755 4/eLife.10989
PMID: 270673 78
31. Murray JM, Escola GS. Learning multiple variabl e-speed sequences in striatum via cortical tutoring.
Elife. 2017; 6: 1–24. https://doi.or g/10.755 4/eLife.26084 PMID: 28481200
32. Rossi-Pool R, Zainos A, Alvare z M, Zizum bo J, Vergara J, Romo R. Decoding a Decisio n Process in the
Neurona l Population of Dorsal Premotor Cortex. Neuron. 2017; 96(6): 1432—1446 .e7. https://doi.or g/
10.1016/ j.neuron.201 7.11.023 PMID: 29224726
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 30 / 32
33. Shenoy K V, Sahani M, Churchlan d MM. Cortical control of arm movements : a dynamical systems per-
spective. Annu Rev Neurosc i. 2013; 36: 337–359 . https://doi.or g/10.1146/ annurev-neu ro-062111 -
150509 PMID: 237250 01
34. Remington ED, Narain D, Hossein i EA, Jazaye ri M. Flexible Sensor imotor Comput ations through Rapid
Reconfigur ation of Cortical Dynami cs. Neuron. 2018; 98(5): 1005–1 019.e5. https://doi. org/10.1016/j .
neuron.2018 .05.020 PMID: 29879384
35. Mendoza G, Peyrache A, Ga ´ mez J, Prado L, Buzsa ´ ki G, Merchant H. Recording extracellu lar neural
activity in the behavin g monkey using a semich ronic and high-density electrode system. J Neuroph ysiol.
2016; 116(2): 563–574 . https://doi.or g/10.1152/ jn.00116.2016 PMID: 271695 05
36. Hardy NF, Buonomano D V. Encoding Time in Feedfor ward Trajectories of a Recurren t Neural Network
Model. Neural Comput. 2018; 30(2): 378–396. https://doi.o rg/10.1162/ne co_a_01 041 PMID: 2916200 2
37. Donnet S, Bartolo R, Fernandes JM, Cunha JPS, Prado L, Merchant H. Monkeys time their pauses of
movemen t and not their movement -kinematics during a synchronizat ion-continuati on rhythmic task. J
Neuroph ysiol. 2014; 111(10): 2138–2149. https://doi.o rg/10.1152/jn .00802.2 013 PMID: 24572098
38. Goudar V, Buonomano D V. Encoding sensory and motor patterns as time-invar iant trajectories in
recurrent neural networks. Elife. 2018; 7: 1–28. https:// doi.org/10.75 54/eLife .31134 PMID: 29537963
39. Mendoza G, Merchant H. Motor system evolution and the emergenc e of high cognitive functions. Prog
Neurobi ol. 2014; 122: 73–93. https:// doi.org/10.10 16/j.pne urobio.2014 .09.001 PMID: 25224031
40. Russo AA, Bittner SR, Perkins SM, Seely JS, London BM, Lara AH, et al. Motor Cortex Embeds Mus-
cle-like Comman ds in an Untangled Populat ion Response. Neuron. 2018; 97(4): 953—966. e8. https://
doi.org/10.10 16/j.neuron.2 018.01.0 04 PMID: 29398358
41. Churchlan d MM, Cunningh am JP, Kaufman MT, Foster JD, Nuyujukian P, Ryu SI, et al. Neural popula-
tion dynamics during reaching. Nature. 2012; 487(7405) : 51–56. https://doi.or g/10.1038/ nature11129
PMID: 227228 55
42. Karmarka r UR, Buonomano D V. Timing in the absence of clocks: encodin g time in neural network
states. Neuron. 2007; 53(3): 427–438. https:/ /doi.org/10.10 16/j.neu ron.2007.01.0 06 PMID: 17270738
43. Merchant H, Yarrow K. How the motor system both encodes and influences our sense of time. Curr
Opin Behav Sci. 2016; 8: 22–27. https://d oi.org/10.101 6/j.cobeha .2016.01. 006
44. Paton JJ, Buonom ano D V. The Neural Basis of Timing: Distributed Mechanism s for Diverse Functions.
Neuron. 2018; 98(4): 687–705. https://do i.org/10.1016 /j.neuron.2 018.03.045 PMID: 297722 01
45. Merchant H, Bartolo R, Pe ´ rez O, Me ´ ndez JC, Mendoza G, Ga ´ mez J, et al. Neurophysio logy of Timing in
the Hundred s of Millisecond s: Multiple Layers of Neurona l Clocks in the Medial Premoto r Areas. Adv
Exp Med Biol. 2014; 829: 143–15 4. https://doi.or g/10.1007 /978-1-493 9-1782-2_ 8 PMID: 25358709
46. Teki S, Grube M, Griffiths T. A Unified Model of Time Perception Accounts for Duration- Based and
Beat-Based Timing Mechanism s. Front Integr Neurosci. 2012; 5: 90. https://doi.or g/10.338 9/fnint.2011.
00090 PMID: 223194 77
47. Schwartze M, Kotz SA. A dual-pathw ay neural architectur e for specific temporal prediction. Neurosci
Biobehav Rev. 2013; 37(10 Pt 2): 2587–2596. https://d oi.org/10.101 6/j.neub iorev.2013.08.0 05 PMID:
23994272
48. Allman MJ, Teki S, Griffiths TD, Meck WH. Properties of the Internal Clock: First- and Second-Or der
Principles of Subjective Time. Annu Rev Psychol. 2014; 65: 743–771. https://do i.org/10.1146 /annurev -
psych-0102 13-115117 PMID: 24050187
49. Bartolo R, Merchant H. β Oscillations Are Linked to the Initiatio n of Sensory-C ued Movement
Sequenc es and the Internal Guidanc e of Regular Tapping in the Monkey. J Neurosci. 2015; 35(11):
4635–4640. https:/ /doi.org/10.15 23/JNEU ROSCI.4570 -14.20 15 PMID: 25788680
50. Jones MR, Boltz M. Dynamic attending and response s to time. Psychol Rev. 1989; 96(3): 459–491.
PMID: 275606 8
51. Large EW, Jones MR. The dynamics of attendin g: How people track time-varyin g events. Psychol Rev.
1999; 106(1): 119–159 . https://doi.or g/10.1037/ 0033-295X .106.1.119
52. Fujioka T, Trainor LJ, Large EW, Ross B. Internaliz ed Timing of Isochrono us Sounds Is Represente d in
Neuromagn etic Beta Oscillations . J Neurosci. 2012; 32(5): 1791–1802. https://doi.o rg/10.1523/
JNEUROS CI.4107-1 1.2012 PMID: 223028 18
53. Iversen JR, Repp BH, Patel AD. Top-down control of rhythm percepti on modulates early auditory
response s. Ann N Y Acad Sci. 2009; 1169: 58–73. https://do i.org/10.1111 /j.1749-6632 .2009.04 579.x
PMID: 196737 55
54. Nozaradan S, Peretz I, Missal M, Mourau x A. Tagging the Neuronal Entrainm ent to Beat and Meter. J
Neurosci. 2011; 31(28): 10234–10240 . https://doi.o rg/10.1523/JN EUROSC I.0411-11.201 1 PMID:
21753000
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 31 / 32
55. Chen JL, Penhune VB, Zatorre RJ. Moving on Time: Brain Network for Auditory-Motor Synchron ization
is Modulate d by Rhythm Complex ity and Musical Training. J Cogn Neurosc i. 2008; 20(2): 226–239.
https://doi.or g/10.116 2/jocn.200 8.20018 PMID: 182753 31
56. Grahn JA, Rowe JB. Feeling the Beat: Premoto r and Striatal Interactio ns in Musicians and Nonmusi-
cians during Beat Perception. J Neurosci. 2009; 29(23): 7540–7548 . https://doi.or g/10.1523/
JNEUROS CI.2018-0 8.2009 PMID: 195159 22
57. Patel AD, Iversen JR. The evolutiona ry neuroscienc e of musical beat percepti on: the Action Simulation
for Auditory Predict ion (ASAP) hypothesis. Front Syst Neurosc i. 2014; 8: 57. https:// doi.org/10.33 89/
fnsys.20 14.00057 PMID: 2486043 9
58. Honing H, Merchant H. Differences in auditor y timing between human and nonhuma n primates. Behav
Brain Sci. 2014; 37(6): 557–558 . https://doi.or g/10.1017/ S0140525X 13004056 PMID: 255149 47
59. Cadena- Valencia J, Garcı ´ a-Garibay O, Merchant H, Jazayeri M, De Lafuente V. Entrainment and main-
tenance of an internal metronome in supplemen tary motor area. Elife. 2018; 7. https:// doi.org/10.75 54/
eLife.3898 3 PMID: 30346275
60. Gibbon J, Malapan i C, Dale CL, Gallistel CR. Toward a neurobiolo gy of temporal cognition : Advances
and challeng es. Curr Opin Neurobi ol. 1997; 7(2): 170–184. https://do i.org/10.1016 /S0959-438 8(97)
80005-0 PMID: 914276 2
61. Merchant H, Zarco W, Prado L. Do we have a commo n mechanism for measurin g time in the hundreds
of millisecond range? Evidence from multiple- interval timing tasks. J Neuroph ysiol. 2008; 99(2): 939–
949. https://do i.org/10.1152 /jn.01225 .2007 PMID: 18094101
62. Garcı ´ a-Gariba y O, Cadena- Valencia J, Merchant H, de Lafuente V. Monkeys Share the Huma n Ability
to Internally Maintain a Tempora l Rhythm. Front Psychol. 2016; 7: 1–12. https://doi.or g/10.338 9/fpsyg.
2016.01971 PMID: 28066294
63. Mendez JC, Prado L, Mendoza G, Merchant H. Temporal and Spatia l Categoriza tion in Human and
Non-Hum an Primates. Front Integr Neurosci. 2011; 5: 1–10. https://doi.or g/10.338 9/fnint.20 11.00050
PMID: 219275 99
64. Simen P, Balci F, DeSouza L, Cohen JD, Holmes P. A Model of Interval Timing by Neural Integration . J
Neurosci. 2011; 31(25): 9238–9253. https://doi.org /10.1523/JN EUROSCI.31 21-10.2011 PMID: 21697374
65. Merchant H, Averbe ck BB. The Comp utational and Neural Basis of Rhythmic Timing in Medial Premoto r
Cortex. J Neurosc i. 2017; 37(17): 4552–4564. https:/ /doi.org/10.15 23/JNEU ROSCI.0367 -17.201 7
PMID: 283365 72
66. Pe ´ rez O, Merchant H. The synaptic properties of cells define the hallmarks of interval timing in a recur-
rent neural network. J Neurosc i. 2018; 38(17): 4186–4199. https:// doi.org/10.15 23/JNEU ROSCI.2651 -
17.2018 PMID: 29615484
67. Kaufman MT, Churchland MM, Ryu SI, Shenoy K V. Cortical activity in the null space: permittin g prepa-
ration without movement . Nat Neurosc i. 2014; 17(3): 440–448. https:// doi.org/10.10 38/nn.36 43 PMID:
24487233
68. Crowe DA, Averbeck BB, Chafee M V. Rapid Sequences of Population Activity Patterns Dynami cally
Encode Task-Cr itical Spatial Informatio n in Parietal Cortex. J Neurosci. 2010; 30(35): 11640–11653 .
https://doi.or g/10.152 3/JNEURO SCI.0954- 10.2010 PMID: 208108 85
69. Jin DZ, Fujii N, Graybiel AM. Neural representat ion of time in cortico-b asal ganglia circuits. Proc Natl
Acad Sci. 2009; 106(45): 19156–19161 . https://doi.or g/10.1073/p nas.090988110 6 PMID: 19850874
70. Gouvêa TS, Monteiro T, Motiwala A, Soares S, Machens C, Paton JJ. Striatal dynamics explain dura-
tion judgmen ts. Elife. 2015; 4: 1–14. https://doi. org/10.7554/e Life.113 86 PMID: 26641377
71. Pastalkova E, Itskov V, Amarasingha m A, Buzsaki G. Internally Generated Cell Assembly Seque nces
in the Rat Hippocampu s. Science. 2008; 321(5894) : 1322–13 27. https://doi.or g/10.1126 /science.
1159775 PMID: 18772431
72. MacDon ald CJ, Lepage KQ, Eden UT, Eichenbaum H. Hippocam pal “time cells” bridge the gap in mem-
ory for discontigu ous events. Neuron. 2011; 71(4): 737–749. https://doi.or g/10.101 6/j.neuron.20 11.07.
012 PMID: 218678 88
73. Perez O, Kass RE, Merchant H. Trial time warping to discrimina te stimulus -related from movement -
related neural activity. J Neurosci Methods. 2013; 212(2): 203–21 0. https://doi.or g/10.101 6/j.jneumet h.
2012.10. 019 PMID: 23147009
74. Merchant H, Battaglia-may er A, Georgopo ulos AP. Effects of optic flow in motor cortex and area 7a. J
Neuroph ysiol. 2001; 86(4): 1937–54. https://doi.or g/10.115 2/jn.2001.86. 4.1937 PMID: 1160065 2
75. Waibel A, Hanaza wa T, Hinton G, Shikano K, Lang KJ. Phonem e recognition using time-delay neural
networks. IEEE Trans Acoust. 1989; 37(3): 328–339. https:/ /doi.org/10.11 09/29.21 701
76. Cortes C, Vapnik V. Support-vec tor networks. Mach Learn. 1995; 20(3): 273–29 7. https://doi.or g/10.
1007/BF0 0994018
The amplitude in periodic neural state trajector ies underlies the tempo of rhythmic tapping
PLOS Biology | https://doi.or g/10.137 1/journal.pb io.3000054 April 8, 2019 32 / 32
