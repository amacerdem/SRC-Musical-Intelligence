# Brain Topography (2026) 39:8

**Year:** D:20

---

## ORIGINAL PAPER

Brain Topography (2026) 39:8
https://doi.org/10.1007/s10548-025-01162-7
magnetoencephalography (MEG), are its lower participant
burden, resistance to noise, cost-effectiveness, and portabil­
ity (Koizumi et al. 2003). Due to these advantages, fNIRS
has been applied in various fields, including developmental
science (Homae et al. 2010; Sato et al. 2012; Taga et al.
2003) and clinical research (Monden et al. 2015; Takizawa
et al. 2014; Watanabe et al. 1998). Capitalizing on these
benefits, researchers have increasingly applied fNIRS in
the development of brain-computer interfaces (BCIs) for
bedside and daily use (Hong et al. 2018; Naseer and Hong
2015; Schudlo and Chau 2014). Furthermore, for patients
with amyotrophic lateral sclerosis (ALS) or complete paral­
ysis due to injury, who are unable to engage in voluntary
physical activities (Birbaumer 2006; Kübler and Birbaumer
2008), BCIs are recognized as a crucial means for com­
munication, offering a means to maintain and potentially
enhance the quality of life (Borgheai et al. 2020). Although
the present study focuses on healthy adults, this clinical con­
text motivates our choice of task design: targeting preserved
sensory and cognitive functions, such as auditory selective
Introduction
Functional near-infrared spectroscopy (fNIRS) is a non-
invasive neuroimaging technique that uses near-infrared
light to measure relative changes in the concentrations of
oxygenated and deoxygenated hemoglobin in the cerebral
cortex (Ferrari and Quaresima 2012). The primary advan­
tages of fNIRS over other neuroimaging modalities, such
as functional magnetic resonance imaging (fMRI) and
Communicated by Urs Maurer. Hiroki Sato
hiroki@shibaura-it.ac.jp

Graduate School of Engineering and Science, Shibaura
Institute of Technology, Saitama, Japan

Department of Language Sciences, Graduate School of
Humanities, Tokyo Metropolitan University, Tokyo, Japan

Department of Bioscience and Engineering, College of
Systems Engineering and Science, Shibaura Institute of
Technology, Saitama, Japan
Abstract
To advance the application of functional near-infrared spectroscopy (fNIRS) in brain-computer interface (BCI) technol­
ogy, we investigated cortical activation patterns associated with auditory selective attention. Using a dichotic listening
paradigm, participants were presented with simultaneous music and reading sounds to the left or right ear. During fNIRS
recordings, they were instructed to selectively attend to the sound attribute (music vs. reading) or the spatial location (left
vs. right ear). Cortical activity differences related to attentional targets were analyzed using a two-way analysis of vari­
ance (ANOVA), with sound attribute and spatial information as factors. Our results revealed a significant main effect of
the sound attribute factor across multiple measurement channels. Notably, the right parietal region exhibited consistently
greater activation when attention was directed toward music compared to reading sounds. Conversely, bilateral dorsolat­
eral prefrontal cortex (DLPFC) channels showed higher activation when participants attended to reading sounds than to
music. These findings indicate that cortical activation patterns are modulated by auditory attentional states based on sound
attributes. Furthermore, preliminary classification analyses achieved an accuracy of 73.7% in discriminating attentional
targets (music vs. reading sounds), demonstrating the feasibility of fNIRS-based BCI applications. Keywords  BCI · FNIRS · Hemodynamics · Auditory function · Selective attention · Dichotic listening · Music ·
Speech
Received: 9 April 2025 / Accepted: 25 November 2025
© The Author(s) 2025
Cortical Representation of Auditory Selective Attention in a Dichotic
Listening Task: A Functional Near-Infrared Spectroscopy Study
Takumu Yamaguchi1
· Ryu-ichiro Hashimoto2
· Hiroki Sato1,3
1 3

Brain Topography (2026) 39:8
attention, is essential for developing BCIs that remain fea­
sible even in severe paralysis. In fNIRS-based BCI applications, selecting appropriate
tasks is critical. Many BCI studies have employed motor
imagery or cognitive tasks, such as mental arithmetic,
which do not rely on external stimuli, allowing users to
voluntarily modulate their brain activity (Hong et al. 2018; Naseer and Hong 2015). For instance, studies using motor
imagery tasks have demonstrated high discrimination rates
based on measurements from the motor cortex (Naseer and
Hong 2013; Sitaram et al. 2007). However, for patients in
the locked-in state who are unable to perform actual move­
ments, the motor cortex may not exhibit significant acti­
vation in response to motor imagery (Conson et al. 2008; Murguialday et al. 2011). In contrast, cognitive tasks can be
performed by patients even in a completely locked-in state
(CLIS) (Hong et al. 2018; Kübler and Birbaumer 2008). Additionally, the prefrontal cortex (PFC) is a preferred
measurement site in BCI applications not only because of
its central role in attentional control and executive function,
but also because hair coverage is minimal in this region,
resulting in higher signal quality compared to hair-covered
areas (Hong et al. 2015; Naseer and Hong 2015). Although
advances in fNIRS optode technology have reduced hair-
related artifacts, this anatomical advantage continues to
contribute to reliable measurement. Cognitive load is bet­
ter conceptualized as a continuum rather than a simple
low/high dichotomy. In real-world BCI applications, tasks
with lower or moderate demands are generally preferable
because they minimize fatigue and maximize usability, even
though highly demanding tasks may yield somewhat clearer
brain signals. Another issue is how the baseline is defined when evalu­
ating brain signals during cognitive tasks. Because a simple
resting state, during which no instructions are provided, can
be uncontrolled and unstable (Schudlo and Chau 2014),
this study employed an active baseline to ensure stable
and reproducible brain signals during task-related analysis. This approach is consistent with prior studies that aimed
to improve baseline stability by employing mild cognitive
engagement instead of an uncontrolled resting condition. For instance, some studies have compared brain activity dur­
ing mental arithmetic tasks using a mild cognitive task, such
as counting (Naito et al. 2007) or imagining alphabet pro­
nunciation (Shin et al. 2016) as the baseline. Ang et al. used
three levels of difficulty in mental arithmetic tasks and per­
formed a two-class classification for each condition (Ang et
al. 2010). These approaches are expected to provide greater
stability as they discriminate brain activity without rely­
ing on a resting state. However, the reported classification
accuracy is approximately 60–80% in binary classification,
which is not sufficiently high. Furthermore, higher-order
cognitive tasks are considered more demanding than typi­
cal cognitive activities. While highly demanding cognitive
tasks may yield clearer and more distinguishable brain sig­
nals for classification, they are not always practical for real-
world BCI applications, where enabling communication
requiring minimal cognitive effort is preferable. Therefore, we are investigating a new BCI task that does
not require a resting state signal or a highly demanding cog­
nitive load to identify brain activity states. To this end, we
focused on selective auditory attention for the following
reasons. First, auditory sensations remain largely unaffected
in ALS patients, making auditory stimuli well-suited for
BCI tasks (Kübler and Birbaumer 2008; Murguialday et al.
2011). Second, selective attention—the ability to filter out
irrelevant information—develops early in life (Jones et al.
2015; Ridderinkhof and Van Der Stelt 2000) and becomes
habitual for many individuals. It is also frequently used in
everyday life (Alain et al. 2013; Fritz et al. 2007) and may
reduce individual variation in task difficulty and less cogni­
tive burden for participants. A representative task requiring auditory selective atten­
tion is dichotic listening, which involves presenting two
distinct sounds simultaneously to the left and right ears
(Westerhausen 2019). This task has been used to study bot­
tom-up processing, such as hemispheric dominance (Della
Penna et al. 2007; Hugdahl and Westerhausen 2016; Mei et
al. 2020), as well as top-down control of attention (Jäncke et
al. 2003; Pugh et al. 1996; Thomsen et al. 2004). Although
auditory stimuli are primarily processed in the temporal
regions, including the auditory cortex, the frontal region is
also suggested to be involved due to the demands of selec­
tive attention. In an fMRI study, bilateral activation of the
dorsolateral prefrontal cortex (DLPFC) was observed during
a dichotic listening task (Pugh et al. 1996), which is attrib­
uted to the inhibition of input from one ear while focusing
on the other. Other fMRI studies using dichotic listening
tasks have also indicated that the activation of attentional
networks within the prefrontal cortex is linked to selec­
tive attention (Jäncke et al. 2003). Additionally, an fNIRS
study examined hemodynamic changes related to selective
attention during a dichotic listening task (Eskicioglu et al.
2019). This study assessed brain activity under three dis­
tinct conditions: non-attentive, forced-left, and forced-right
attention during a binaural dichotic listening task involving
consonant-vowel (CV) syllables. Results showed significant
activation in the right prefrontal cortex under forced atten­
tion conditions compared to the non-attention condition,
regardless of the direction of attention (left or right). These
findings suggest that activation patterns in the prefrontal
cortex serve as markers of inhibition and focused attention. However, previous dichotic listening studies have primarily
used simple speech or tonal stimuli. We introduced a novel
1 3

Page 2 of 16

Brain Topography (2026) 39:8
variation by pairing music with spoken text (reading) to
capitalize on their distinct hemispheric processing tenden­
cies—music being preferentially processed in right-hemi­
sphere networks and speech in left-hemisphere networks
(Limb 2006; Pastuszek-Lipińska 2025; Plakke and Roman­
ski 2014; Perani et al. 2010; Vigneau et al. 2006). Further­
more, dichotic listening literature has reported a left-ear
advantage for music and a right-ear advantage for speech
(Kimura 1967; Kompus et al. 2012), reflecting both hemi­
spheric specialization and contralateral auditory pathways. These asymmetries are not limited to the temporal cortex
(Plakke and Romanski 2014); they can influence prefrontal
attentional control networks, thereby providing a principled
rationale for testing whether stimulus type and ear of pre­
sentation jointly modulate DLPFC activity. Based on this framework, we hypothesized that DLPFC
activation would differ depending on (i) the attended stimu­
lus category (music vs. reading), and (ii) the ear of presenta­
tion (left vs. right), with potential interaction effects when
the ear advantage aligns with the hemispheric specializa­
tion of the stimulus. This hypothesis directly links selective
attention mechanisms, lateralized auditory processing, and
prefrontal top-down control, thereby addressing both theo­
retical and practical aspects of stimulus-driven BCI design. To further evaluate the feasibility of this paradigm for
BCI applications, we also performed an exploratory clas­
sification analysis to examine whether distinct patterns of
DLPFC activation across attentional conditions could be
used to discriminate attentional states. This analysis, con­
ducted at the participant level using aggregated task-related
features, aimed to assess the potential separability of atten­
tional states in a practical BCI context. Materials and Methods
Participants
Twenty-two healthy men (19–24 years old) participated in
the study; all were right-handed and had no history of audi­
tory disorders. All participants were native Japanese speak­
ers, born and raised in Japan, and were university students or
graduates from the same institution. Therefore, they shared
a relatively homogeneous sociocultural and educational
background, minimizing interindividual variability related
to language or cultural familiarity with the auditory stimuli. Data from three participants were excluded from the analy­
sis due to technical errors in the measurements. This study
was approved by the Biotechnology Research Ethics Com­
mittee of the Shibaura Institute of Technology. Informed
consent was obtained from all the participants before the
experiment. The experimental protocol was performed in
accordance with the “Guidelines for ethics-related problems
with non-invasive research on human brain function” estab­
lished by the Japan Neuroscience Society. The target sample size for this study was determined
based on practical considerations, such as participant avail­
ability, and to ensure comparability with sample sizes used
in previous fNIRS studies employing similar paradigms. Although a formal a priori power analysis was not con­
ducted, we performed post hoc power analyses using the
results of the repeated-measures ANOVA (see Results) to
evaluate the achieved statistical power for the observed
effects.
fNIRS System
An fNIRS system (ETG-4000, Hitachi Medical Corpora­
tion, Tokyo, Japan) was used to measure brain activity
signals during auditory selective attention tasks involving
dichotic listening stimuli. The fNIRS system was equipped
with 33 probes (17 near-infrared light sources and 16 detec­
tors) arrayed in a 3 × 11 lattice pattern centered on the fron­
tal cortex, resulting in 52 measurement points (channels). In each channel (CH) between a light source and a detector,
signals for oxygenated hemoglobin (oxy-Hb) and deoxy­
genated hemoglobin (deoxy-Hb) were recorded at a sam­
pling rate of 10 Hz. The source–detector distance was fixed
at 30 mm, which is standard for cortical measurements. The probe arrangement was based on the international
10–20 system, with the bottom-center probe positioned
at Fpz. To estimate the measurement channel locations in
Montreal Neurological Institute (MNI) space, we utilized
the coordinate data published by Sato et al. (2013), which
employed the same channel configuration during simultane­
ous fNIRS and fMRI measurements. In addition, a proba­
bilistic registration method (Singh et al. 2005) was applied
to generate 3D topographic maps, confirming adequate
coverage of the DLPFC across participants. Based on this
mapping, channels over the DLPFC were primarily located
in the anterior–lateral areas of both hemispheres (approxi­
mately CH 2–5, 13–15, 23–26, 34–36, 45–47 in the right
hemisphere; and CH 6–9, 17–19, 27–30, 38–40, 48–50 in
the left hemisphere). Although the auditory cortex was not
fully covered, this was not essential for the current research
objectives, which focused on prefrontal activation patterns
as markers of attentional control. Dichotic Listening Task
We created dichotic listening stimuli using music and read­
ing sounds. For the music stimuli, classical music recorded
from CDs played on both traditional Japanese instru­
ments (MUSICAL INSTRUMENT WAGAkki 01, 02,
1 3
Page 3 of 16

Brain Topography (2026) 39:8
sound. Thus, we defined four conditions: music presented
to the left ear (Music-Left condition), reading sounds pre­
sented to the right ear (Reading-Right condition), reading
sounds presented to the left ear (Reading-Left condition),
and music presented to the right ear (Music-Right condi­
tion), based on the sound attribute of the attended target,
regardless of the instruction type (Fig. 1(a)). In each session, three trials for each condition were pre­
sented in random order, resulting in a total of 12 task tri­
als per session. Each participant completed four sessions:
two attribute instruction sessions and two spatial instruc­
tion sessions, yielding a total of 48 task trials. The experi­
mental sessions were spread across two days to minimize
the influence of experimental fatigue and to enhance result
reproducibility. Experimental Procedure
Participants attended two experimental days, separated by
one week. On the first experimental day, they were informed
about the study and asked to complete a consent form and an
information sheet to record details such as age, gender, and
handedness. Four practice trials were conducted before the
actual measurements began. On each experimental day, participants sat in a chair in a
sound-attenuated chamber while wearing the fNIRS probe
cap. They then completed an attribute instruction session
and a spatial instruction session in a counterbalanced order. As mentioned above, each session consisted of 12 task trials
(Fig. 1(b)). The duration of the rest period between trials
was set to 20 s to ensure sufficient recovery of the hemo­
dynamic response before the onset of the next task block. In previous studies using basic sensorimotor paradigms,
most participants’ hemodynamic waveforms returned to
baseline within 10–15  s after stimulus offset, and these
responses were shown to be highly reproducible (Sato et
al. 2006). Furthermore, the best-practice recommendations
for fNIRS experimental design (Yücel et al. 2021) illustrate
a 15-second inter-block interval as a representative exam­
ple. Therefore, the present study adopted a 20-second rest
period, which falls within the standard range commonly
used in fNIRS block designs and provides a conservative
buffer to ensure full baseline recovery. The time sequence
of each task trial was as follows: 20 s of rest, 5 s of atten­
tion instruction, 20 s of task performance, and up to 5 s of
response to a question followed by an additional 20 s of
rest. Each session lasted approximately 11 min, and two ses­
sions were conducted per day over two experimental days
(approximately one week apart). Thus, the total active task
time per participant was within 30 min per day. This design
minimized participant fatigue and ensured that the total
measurement duration remained within the range typically
manufactured by Nippon Television Music Corporation)
and Western instruments (100 CLASSICS, manufactured
by AVEX MARKETING INC.) were used. We selected
standard, well-known classical pieces to minimize both
linguistic interference and differences in familiarity among
participants. For the reading stimuli, recordings of Japanese
folk tales from CDs (“Kiku-Ehon: Mukashi-Banashi Best
100”, manufactured by Pan Rolling Inc.) were used. We
selected well-known Japanese folk tales that are culturally
familiar and linguistically simple, so that all participants
could easily understand the content without differences in
comprehension or cultural background. Although no formal
pre-test was conducted, informal pilot listening among labo­
ratory members confirmed that the selected stories were eas­
ily understandable. Using Adobe Audition 2021, each sound
was segmented into 20-second clips and edited to present
different types of sounds to the left and right ears. There
were two types of stimuli; one presented music to the left
ear and reading sounds to the right ear, while the other pre­
sented reading sounds to the left ear and music to the right
ear. We created 24 different stimuli for each type, result­
ing in a total of 48 stimuli. These stereo stimuli were deliv­
ered through earphones (SE215, Shure Inc., IL, USA). To
ensure comparable perceptual intensity between the reading
and music sounds, their sound pressure levels (SPLs) were
adjusted based on subjective loudness matching. The out­
put SPLs from the earphones were evaluated using a multi-
environmental measuring instrument (LM-8102, Mother
Tool, Nagano, Japan). Based on representative random sam­
pling of several 20-second clips, the maximum SPL of the
reading sounds within a single segment was approximately
67 dB, and that of the music sounds was approximately 66
dB. The minimum SPL values were not reported because
short pauses in the reading stimuli produced transient near-
silent periods, which do not reflect the perceived loudness
of the auditory stimuli. Therefore, these measurements are
presented as representative estimates of the typical maxi­
mum levels across all stimuli. For the dichotic listening task, there were two types of
sessions with different instructions. In the “attribute instruc­
tion” session, participants were instructed to pay attention
to either the “music” or the “reading” sounds. In the “spatial
instruction” session, they were instructed to focus on the
“sound presented to the left ear” or the “sound presented to
the right ear.” These instructions were displayed on a screen
in front of the participants for 5 s before the task began. Notably, participants always attended to the sound attribute,
as their performance was evaluated based on responses to a
simple two-choice question related to the sound attribute in
both sessions. The questions were “What is the title of this
story?” when they focused on the reading sound and “What
is the style of this music?” when they focused on the music
1 3

Page 4 of 16

Brain Topography (2026) 39:8
Questions included prompts such as “What is the title of this
story?” or “What is the style of this music?”
Behavioral analysis focused on participants’ responses to
these simple questions to confirm that their attention was
correctly aligned with the intended stimulus. Response
accuracy was computed for each participant and a repeated-
measures analysis of variance (ANOVA) was performed,
factoring in both the sound attributes (music or reading
sounds) and the spatial information (left or right ear) of
the attended stimulus. Only responses within the 5-second
used in fNIRS block-design studies. During the rest peri­
ods, participants were instructed to relax, clear their minds,
and fixate on a cross displayed at the center of the screen
while avoiding head movement. In the attention instruc­
tion phase, the screen indicated where participants should
direct their selective attention—toward the music, reading
sounds, left ear, or right ear. During task performance, par­
ticipants focused their attention on the instructed target. In
the response phase, participants answered a two-alternative
question related to the sound attribute by pressing a key. Fig. 1  Experimental design and attentional conditions. (a) Two types
of auditory stimulus configurations and the resulting four attentional
conditions. The “suitable” configuration consisted of music presented
to the left ear and reading sounds to the right ear, whereas the “unsuit­
able” configuration presented reading sounds to the left ear and music
to the right ear. Four distinct attentional states were measured by
directing participants’ focus toward one of the two sounds, yielding
the following conditions: music in the left ear, music in the right ear,
reading in the left ear, and reading in the right ear. In the schematic,
the ♬ and book symbols represent the positions of the music and read­
ing sounds, respectively. Letters within the figure indicate the sound
attribute (music or reading) and spatial information (left or right ear) of
the attended target. (b) Schematic illustrating the time sequence of the
two session types—attribute instruction and spatial instruction—and
the detailed structure of a single task trial. Each session consisted of
12 task trials, each comprising an instruction phase (5 s), a task per­
formance phase during which participants attended to the designated
target sound, and a response phase (within 5 s) in which they answered
a two-choice question regarding the attended sound attribute. The two
session types were conducted in a counterbalanced order within a sin­
gle recording day. Each participant completed four sessions in total
across two recording days
1 3
Page 5 of 16

Brain Topography (2026) 39:8
subsequent analyses. Although a 1-second baseline may
appear short compared with more conventional 5-second
periods, our previous studies have shown that it yields sta­
ble activity waveforms in similar experimental paradigms
(Sato et al. 2012; Aoki et al. 2011). Statistical Analysis
The brain activity values used for the analysis were com­
puted as follows. To explore potential temporal changes in
task-related activation, two-time windows were defined as
analysis periods to explore the common activation associ­
ated with the dichotic listening task across all attentional
conditions: the first half (0.1–10.0 s) and the second half
(10.1–20.0 s) of the stimulus presentation period. The first
half was expected to capture the initial phase of attention
engagement, whereas the second half might involve sus­
tained attention or possible habituation effects. Initially, the
mean oxy-Hb signal for each attentional condition in both
analysis periods was calculated. Using these mean values
from individual trials, z-values were computed as the com­
mon brain activity value by dividing the mean values across
trials by the corresponding standard deviation (Eqs.  1–3)
(Sato et al. 2011).
−x= 1
n
∑n
i=1xi
(1)

## SD =

√

n
∑n
i=1
(
xi−
−x
)2
(2)
z =
−x
SD

(3)
Using the common brain activity values, t-tests were con­
ducted to determine which channels were significantly acti­
vated by the dichotic listening tasks in both the first and
the second halves of the stimulus presentation period. All
52 channels covering the prefrontal region were included
in this exploratory analysis to examine the overall spatial
distribution of activation patterns. The threshold for p-val­
ues was corrected for multiple testing using a permutation
test (Nichols and Holmes 2002). Specifically, forty-eight
26-second windows were randomly sampled from the oxy-
Hb signals across four sets of 12-trial measurements, where
band-pass filtering and hemodynamic modality separation
methods had been applied. The 26-second window corre­
sponds to one task period, including 1 s of pre-task and 20 s
of post-task period, with no overlap between windows. Sub­
sequently, the z-values for each CH were obtained in the
same manner as in the real analysis described earlier. A t-test
was then conducted on these z-values across participants for
window, the maximum duration allocated for the question,
were accepted. Preprocessing of fNIRS Signals
The fNIRS signals were preprocessed using the Platform for
Optical Topography Analysis Tools (POTATo) (Sutoko et al.
2016) in MATLAB (MathWorks). First, the light attenuation
data, represented by the voltage signal, were converted into
oxy- and deoxy-Hb signals based on the Beer–Lambert law
(Maki et al. 1995). Second, a band-pass filter (0.01–0.8 Hz)
was applied to both Hb signals to eliminate low-frequency
drift/oscillation and high-frequency noise components
(Kamran et al. 2016; Naseer and Hong 2015). Subsequently, the signals were divided into functional
and systemic components using the hemodynamic modal­
ity separation method (Yamada et al. 2012), which sepa­
rates neural-related hemodynamic responses from global
physiological oscillations. Only the functional signals were
retained for further analysis to minimize physiological noise
contamination. Furthermore, since the paradigm involved
multiple repetitions of each attentional condition, the sub­
sequent trial-averaging process effectively reduced uncorre­
lated physiological noise and transient artifacts, enhancing
the signal-to-noise ratio of task-related responses. Their
method separates the signals based on their physiological
origins, assuming that the functional components of oxy-
and deoxy-Hb signals show an inverse correlation. This pro­
cedure also inherently reduces the influence of outliers and
physiological noise unrelated to task-induced activation. Compared with commonly used filtering and preprocessing
techniques summarized by Herold et al. (2018), this modal­
ity separation approach offers a practical advantage because
it does not require additional hardware such as short-sepa­
ration channels while effectively isolating functional com­
ponents from systemic interference. After applying this
method, the oxy- and deoxy-Hb functional signals were sta­
tistically identical, indicating that they contained equivalent
functional information. Both parameters were examined,
but as they produced statistically identical results, only the
oxy-Hb signal is reported here to avoid redundancy. The
continuous-time data of the oxy-Hb signals recorded dur­
ing each session were segmented into 50-second task blocks
to calculate the block average. Each block consisted of
a 6.0-second pre-task period (1 s of rest and 5 s of atten­
tion instruction), a 20-second task period, and a 24-second
post-task period (5 s of response and 19 s of rest). Baseline
correction was applied using the 1-second rest signal imme­
diately preceding the attention instruction for each block. This duration was selected to (1) minimize fluctuations
carried over from the preceding task and response phases,
and (2) maximize the post-task resting period available for
1 3

Page 6 of 16

Brain Topography (2026) 39:8
Results
Behavioral Analysis
Basic behavioral data are shown in Table 1, indicating that
participants responded to the simple question after the task
with an average accuracy of more than 96% across all con­
ditions. Repeated-measures ANOVA did not reveal any
significant main effects or interactions between sound attri­
butes and spatial information (main effect of sound attri­
butes: F(1,18) = 0.443, p = 0.514, η 2
P = 0.0150; main effect
of spatial information: F(1,18) = 0.00617, p = 0.938,, η 2
P
= 0.0000106; interaction: F(1,18) = 2.660, p = 0.120,, η 2
P
= 0.0105). General Activation Channels during the Dichotic
Listening Task
In the permutation test, the results of 1000 simulations for
each analysis period yielded t-value thresholds of 3.23 for
the first half and 3.26 for the second half. Using these thresh­
olds, ACT-CHs were determined for both analysis peri­
ods, revealing eighteen ACT-CHs in the first half (Fig. 2,
left) and nine ACT-CHs in the second half (Fig. 2, right)
around the DLPFC. All ACT-CHs identified in the second
half overlapped with those in the first half, indicating that
the first-half window captured the most robust task-related
activation. Consistent with the rationale described in the
Methods section, only the ACT-CHs from the first half were
therefore used for subsequent statistical analyses. Cortical activation pattern depending on selective
attention. We conducted a repeated-measures ANOVA to examine
the cortical activation patterns depending on auditory selec­
tive attention to sound attributes (music vs. reading sounds)
or spatial information (left vs. right ear) in the ACT-CH
(Fig. 3). Significant main effects of sound attributes were
detected in three channels (CH 2, CH 25, and CH 28)
(Fig. 3(a)), and significant interaction effects were found in
CH 13 (Fig. 3(c)). In addition, no significant effects of spa­
tial information were observed. The significant channels that showed a main effect in
the ANOVA were examined in detail (Fig. 4, red squares). In CH 2 (BA6), which showed the main effect of sound
attributes, higher activity was observed when listening to
music compared to reading sounds (first half: F(1,18) = 6.07,
p = 0.0240, η 2
P = 0.123). Conversely, we found the opposite
results in CH 25 and CH 28 (BA46), which also showed the
main effect of sound attributes: attention to reading sounds
induced higher activation than attention to music (CH 25:
each CH, and the maximum t-value among the 52 CHs was
recorded for each iteration. This process was repeated 1000
times, and the t-value corresponding to the upper 5% of the
maximum t-values across all simulations was used as the
threshold value, corrected for multiple comparisons. Chan­
nels with t-values higher than the threshold obtained from
the permutation test were defined as activated channels
(ACT-CHs) in both the first and second halves of the task. To maximize sensitivity while maintaining reliability, we
selected the analysis period that best captured robust task-
related activation for subsequent analyses. The rationale and
specific results supporting the choice of the first-half window
are presented in the Results section. Both analysis windows
were examined in an exploratory manner, and the activation
patterns for each window are reported in the Results section
to empirically justify the selection of the first-half window. The choice of a 10-second division is also consistent with
previous neuroimaging studies, as both BOLD fMRI and
fNIRS share the temporal characteristics of the neurovascu­
lar hemodynamic response, and several fMRI studies have
employed analysis windows of approximately 10 s to char­
acterize activation patterns (e.g., Fox et al. 2005; Wen et al.
2019). This segmentation thus allowed us to capture both
the initial rising phase and the later, potentially habituated
phase of the task-evoked hemodynamic response, provid­
ing a balanced temporal resolution for detecting dynamic
changes in activation. Next, z-values were calculated for each attentional con­
dition—Music-Left, Reading-Left, Music-Right, and Read­
ing-Right—in the ACT-CHs for each participant to perform
a repeated-measures ANOVA. This ANOVA was based on
a 2 × 2 repeated-measures factorial design, with the primary
factors being sound attributes (music versus reading sounds)
and spatial information (left versus right ear) corresponding
to the stimuli that directed attention. In this test, the partial
eta squared value was calculated as the effect size. All trials, including those in which participants either
failed to respond within the 5-second window or responded
incorrectly (19 out of 1,056 trials; 1.8%), were included
in the statistical analyses. These cases were regarded as
unavoidable noise inherent to human behavior, occurring
even when participants attended to the target stimulus. Table 1  EBehavioral results showing average accuracy and standard
error for simple questions on stimuli to which selective attention was
directed, across four attention conditions
Accuracy [%]
Left
Right
Music
96.9 ± 1.55
97.6 ± 1.89
Reading sounds
98.7 ± 0.697
97.8 ± 1.05
1 3
Page 7 of 16

Brain Topography (2026) 39:8
(Fig. 4, yellow squares). CH 13 exhibited a significant inter­
action (F(1,18) = 5.11, p = 0.0364, η 2
P = 0.068). Subsequent
post hoc tests (corrected using Tukey’s honest significant
difference (HSD) method) revealed higher activation in the
F(1,18) = 6.90, p = 0.0171, η 2

## P = 0.104; CH 28: F(1,18) =

6.60, p = 0.0193, η 2

## P = 0.098). A few channels showed a significant interaction between
sound attributes and spatial information in the ANOVA
Fig. 3  Results of ANOVA (sound attribute × spatial information). The
analysis was carried out for each ACT-CH. (a) Results in the main
effects of sound attributes; (b) results in main effects of spatial infor­
mation; and (c) results in the interaction. Positions shown in light blue
represent ACT-CH, while positions shown in red signify channels rep­
resenting statistical significance in either main effects or interactions
Fig. 2  Distribution of activated channels (ACT-CHs) during the selec­
tive auditory attention task involving dichotic listening stimuli. The
left figure presents the results for the first half, and the right figure pres­
ents the results for the second half of the analysis period. In these fig­
ures, CHs whose t-values surpassed the threshold determined through
simulation are denoted by red markers
1 3

Page 8 of 16

Brain Topography (2026) 39:8
labels indicating music versus reading sounds. Channels
showing a significant main effect of sound attributes in
the ANOVA were used as features, with the aim of testing
whether accurate classification could be achieved using a
compact, cost-effective set of channels suitable for practical
BCI implementation. We acknowledge that using the same dataset for both
feature selection and classification can raise concerns about
circular analysis (“double dipping”), which can lead to opti­
mistically biased accuracy estimates. While group-level
statistical significance reflects consistent differences across
participants, it does not necessarily imply high classifica­
tion performance at the individual level (Hebart and Baker
2018; Haufe et al. 2014). Therefore, the present classifica­
tion should be considered as complementary evidence to the
group-level results rather than as definitive proof of discrim­
inability. This analysis was intended purely as a preliminary
step to explore feasibility, and future work should employ
independent feature selection procedures or external valida­
tion datasets for more rigorous evaluation. Music-Left condition than in the Music-Right condition (p
= 0.0185). The graph for CH 13 also shows distinct high and
low activity conditions. The high activity conditions were
Music-Left and Reading-Right, while the low activity con­
ditions were Music-Right and Reading-Left, suggesting that
Music-Left (Reading-Right) stimuli elicited higher activa­
tion than Music-Right (Reading-Left) stimuli. We performed a posteriori power analyses using the
results of the repeated-measures ANOVA and the software
G*Power 3.1.9.7. First, the partial eta squared (η2) was cal­
culated for each channel showing a main effect to determine
the effect size. Power calculations with alpha set to 0.05 and
sample size set to 19 yielded power values of 0.87, 0.80, and
0.77 for CH 2, CH 25, and CH 28, respectively. Exploratory Classification Analysis
In addition to the pre-planned analyses, we performed an
exploratory classification analysis to assess whether brain
activity states could be identified from fNIRS signals using
Fig. 4  Detailed results of the ANOVA conducted for the first half of
the analysis period. In the brain map, light blue represents ACT-CHs,
red designates channels with significant main effects related to sound
attributes, and yellow signifies channels with significant interaction
effects. In the bar graphs, blue and orange bars show the attentional
state of focusing on music and reading sounds, respectively. Spatial
information is shown on the horizontal axis of the graph. The activa­
tion level (mean z-value) for each attentional condition is presented in
the bar graphs, with error bars indicating the standard error
1 3
Page 9 of 16

Brain Topography (2026) 39:8
stimulus regardless of differences in sound attributes or spa­
tial information. Significant activation (ACT-CH) was observed in regions
centered around the DLPFC during both analysis periods of
the dichotic listening task. The wider spatial extent of acti­
vation in the first half compared with the second half may
reflect the temporal profile of the hemodynamic response,
such as earlier peak latency, and may also be related to the
initial cognitive demands of the task and attention setting. The DLPFC, in conjunction with the parietal cortex, forms
a network responsible for the top-down coordination of sen­
sory processing (Gazzaley and Nobre 2012). This region
has been identified as playing a critical role in detecting and
maintaining attention, as well as in working memory (WM)
related to auditory stimuli (Kane and Engle 2002; Okada
et al. 2010; Plakke and Romanski 2014). Indeed, research
focusing on dichotic listening stimuli and selective atten­
tion has consistently observed activation in frontal regions,
especially in the DLPFC (Jäncke et al. 2003; Pugh et al.
1996; Thomsen et al. 2004). On the other hand, we did not
observe any significant activation in the temporal cortex,
whereas previous studies have reported activation in this
region during dichotic listening tasks (Jäncke et al. 2003; Sato et al. 1999). Regarding this inconsistency, it is possible
that the present task did not require as much attention as
in previous studies. In the earlier fNIRS study, participants
were instructed to continuously respond to whether a tone
presented every 2 s was delivered to the right or left ear,
requiring sustained attention (Sato et al. 1999). Similarly,
in the fMRI experiment, participants were asked to judge
the pitch of a pure tone presented every second (Jäncke
et al. 2003). In contrast, the task in the present study did
not require as high a level of continuous attention, as par­
ticipants were instructed to focus on the stimulus but were
only required to respond to a simple task after a 20-second
interval. This finding suggests that a high level of sustained
attention is necessary to maintain significant activation in
the auditory cortex. ACT-CH exhibited more consistent activation in the right
than in the left hemisphere. This pattern possibly reflects
selective attention-driven activation of the right frontopa­
rietal network, which is activated in association with audi­
tory spatial and selective attention (Kong et al. 2014; Lee et
al. 2014; Li et al. 2012), as verified during attentional tasks
involving dichotic listening stimuli (Jäncke et al. 2003; Westerhausen et al. 2010). Beyond simple attentional pro­
cesses, this network is also implicated in a range of func­
tions, including motor planning, mental imagery, mental
rotation, and working memory (Ptak et al. 2017). As our
task required both selective attention to dichotic listening
stimuli and retention of stimulus information, it is plausible
Machine learning was performed using the Classification
Learner application in MATLAB. The “Optimized Support
Vector Machine (SVM)” was selected as the classification
algorithm, with hyperparameters automatically tuned via
Bayesian optimization over 100 iterations and evaluated
using fivefold cross-validation. Four hyperparameters were
optimized: kernel function, box constraint level, kernel
scale, and data standardization. Classification performance was assessed across par­
ticipants, where the dataset consisted of brain activity val­
ues for all four attentional conditions of each participant. These values were labeled according to their correspond­
ing attentional states for sound attributes, either as music
(Music-Left, Music-Right conditions) or reading sounds
(Reading-Left, Reading-Right conditions). Three distinct
classification models were evaluated: (1) the all-CH model,
using all channels; (2) the ACT-CH model, using the 18
channels (ACT-CHs) showing significant activation in the
main task analysis; and (3) the effective-CH model, using
the three channels with significant main effects of sound
attributes. The classification results are presented in Table 2,
with accuracies of 50.0%, 65.8%, and 73.7% for the all-CH, ACT-CH, and effective-CH models, respectively. In both
the ACT-CH and effective-CH models, the results signifi­
cantly surpassed the chance level of 50%. Discussion
We examined cortical activation patterns depending on
auditory selective attention in dichotic listening stimuli
consisting of music and reading sounds. We found distinct
activation patterns related to the attended sound attributes in
cortical regions, including the DLPFC. In the dichotic listening task, a simple question about the
auditory stimuli was asked to confirm participants’ atten­
tion to the targeted sounds. The behavioral data, represented
by the accuracy of the responses, was greater than 96%, on
average across all conditions. This confirms that, across
all conditions, participants’ attention was reliably directed
toward the appropriate stimuli with high accuracy. Further­
more, the ANOVA indicated no significant main effects or
interactions involving attentional conditions, confirming
that participants were able to correctly focus on the target
Table 2  Classification accuracy of three models utilizing Support Vec­
tor Machine (SVM) for binary classification of attention to music and
reading sounds
Model
Number of channels
Accuracy [%]
All-CH

50.0
ACT-CH

65.8
Effective-CH

73.7
1 3

Page 10 of 16

Brain Topography (2026) 39:8
but was dependent on the type of dichotic listening stimu­
lus presented. Previous studies have indicated hemispheric
dominance for musical and linguistic stimuli, with the left
ear advantage (LEA) associated with musical stimuli and
the right ear advantage (REA) associated with linguistic
stimuli (Kimura 1967; Kompus et al. 2012; Majidpour et
al. 2022). When such dominance is manifested, detection
becomes more rapid and precise. These ear advantages can
be attributed to two factors: hemispheric dominance and
the architecture of the auditory processing pathways. Music
is predominantly processed in the right hemisphere (Limb
2006; Perani et al. 2010), whereas linguistic information
from reading is processed primarily in the left hemisphere
(Dehaene-Lambertz et al. 2002; Vigneau et al. 2006). For
dichotic listening stimuli, input from the contralateral ear
inhibits the ipsilateral pathway, making the contralateral
auditory pathway more dominant, which transmits infor­
mation more rapidly and abundantly than the ipsilateral
pathway (Kimura 1967). Within the context of this study,
the Music-Left and Reading-Right conditions were aligned
with LEA and REA, respectively, whereas the Music-Right
and Reading-Left conditions did not. These insights sug­
gest the existence of regions that, apart from those activated
based on the attention target’s information, might also be
activated according to the arrangement of dichotic listen­
ing stimuli. Nevertheless, our findings do not entirely con­
form to these brain regions, highlighting the need for further
investigation. Significant distinctions between music and
language typically emerge in temporal regions, such as the
auditory cortex, rather than in frontal regions, necessitating
further validation in this domain. One possible reason for
the absence of significant effects in the temporal channels
is that the optode arrangement in this study covered only
part of the auditory cortex, with limited coverage of higher-
order auditory areas, because it was optimized to target the
dorsolateral prefrontal cortex (DLPFC) in line with our pri­
mary aim of examining frontal activation related to selec­
tive attention. In addition, the DLPFC may exhibit robust
modulation in this task because it is critically involved in
top-down attentional control, integrating auditory input with
task goals and suppressing irrelevant streams, regardless of
whether the primary sensory response in the auditory cortex
reaches statistical significance. This is consistent with prior
neuroimaging findings showing that prefrontal activation
can occur even when sensory cortical responses are weak or
undetectable, provided that the task engages executive con­
trol processes. Future studies incorporating probe arrange­
ments that cover both frontal and temporal regions would
help clarify the relationship between attentional control net­
works and auditory sensory processing. The exploratory cross-participant classification analysis
indicated that attentional states for different sound attributes
that the right frontoparietal network was predominantly
activated. The main effect of the sound attribute was found in CH
2 (BA6). This region displayed heightened activation dur­
ing attention to music compared to reading sound attention. BA6 corresponds to the premotor and supplementary motor
areas. Previous studies on auditory perception and imag­
ery have identified activation in this region across various
sounds, nonverbal utterances, and music (Bengtsson et al.
2009; Gordon et al. 2018). This activation persisted even
in tasks devoid of a motor component (Lima et al. 2016). Furthermore, the supplementary motor area (SMA) and pre-
SMA are hypothesized to be activated by the structural ele­
ments of music, such as rhythms and beats (Gordon et al.
2018). Compared to fMRI, which has been used in many
previous studies, fNIRS can be conducted in a quiet envi­
ronment, allowing participants to hear the structural features
of music, which may result in BA6 activation. In contrast, higher activation of attention to reading
sounds than to music was found in CH 25 and CH 28,
which showed significant main effects of attribute informa­
tion. The DLPFC, which corresponds to these channels, is
integral to the WM and plays a pivotal role in information
maintenance. In this study, participants were required to
retain information about the attentional target for subse­
quent simple questions. Specifically, when the target was
music, the participants answered questions identifying the
type of instrument being played. In contrast, participants
were queried about the title when the attentional target was
a narrated story. It is worth noting that, whereas questions
about music sought to distinguish between conventional and
Japanese instruments, those pertaining to reading required
participants to recall distinct titles for each story. This sug­
gests a potentially greater WM load for attention to reading
sounds than to music. Consistent with this finding, previous
studies have indicated that the DLPFC is activated under a
heightened WM load (Ayaz et al. 2012; Huang et al. 2013; Power et al. 2012). Furthermore, given that the DLPFC is
also implicated in verbal WM tasks (Crottaz-Herbette et al.
2004; Wei et al. 2004), it is plausible that this, combined
with inherent task demands, resulted in the observed higher
attentional activity to reading sounds. We found significant interactions in CH 13, where the
Music-Left and Reading-Right conditions generally exhib­
ited higher activation, while the Music-Right and Reading-
Left conditions showed lower activation. The Music-Left
and Reading-Right conditions correspond to an identical
stimulus, where music is directed to the left ear and read­
ings to the right, whereas the Music-Right and Reading-Left
conditions correspond to another stimulus, in which the
auditory configuration is reversed. Thus, it is possible that
the activity was not generated by attention to a target sound
1 3
Page 11 of 16

Brain Topography (2026) 39:8
in selective attention and auditory processing. For instance,
selective attention and functional cerebral networks in
women are influenced by menstrual cycles (Thimm et al.
2014). Furthermore, gender differences have been observed
in selective attention responses to dichotic listening stimuli
(Voyer 2011). This factor warrants careful consideration
when evaluating the potential applicability of our findings
to female participants. Second, we discuss the application
with actual users and patients with CLIS. In this study,
experiments were conducted on adult male subjects with­
out CLIS, and our results suggest the possibility of using
auditory selective attention to classify brain activity. How­
ever, it is unclear whether the same results can be obtained
when applied to patients with CLIS. Several studies have
shown that auditory and cognitive functions are maintained
in patients (Kübler and Birbaumer 2008; Murguialday et al.
2011) with CLIS and that fNIRS-based BCI with mental
tasks can be applied to patients with CLIS (Borgheai et al.
2020; Naito et al. 2007). However, CLIS patients may show
different brain activity trends than healthy subjects (Chenji
et al. 2016; Khalili-Ardali et al. 2021; Naito et al. 2007). Therefore, it is necessary to examine whether the proposed
BCI task will be useful for patients with CLIS. Third, we
did not apply explicit rejection criteria for individual noisy
channels, as our trial-averaging approach was expected to
substantially reduce random noise in the present paradigm. However, this strategy may not fully address all sources of
poor channel quality, and future work should incorporate
systematic channel quality assessment and rejection proce­
dures to align with current best practices. Finally, the effects
of “habituation” to the stimuli and task procedures should
be considered. In this study, 12 consecutive trials were
conducted. Because all dichotic listening stimuli were dif­
ferent, it is unlikely that there was complete habituation to
the auditory content. However, the use of the same type of
question (“What is the title of this story?” or “What is the
style of this music?”) across trials may have contributed to
the ceiling behavioral accuracy, raising the possibility that
participants primarily attended to the stimuli in the initial
trials to obtain the necessary information. Such a strategy
could potentially lead to greater fNIRS responses in the first
half compared to the second half. In addition to stimulus-
related habituation, procedural habituation associated with
the temporal structure of the task should also be considered. Although the overall sequence of each trial was consistent,
the inter-stimulus interval was not strictly fixed because the
response period allowed up to 5 s, resulting in small varia­
tions in the onset-to-onset timing across trials. This vari­
ability may have reduced complete temporal predictability;
however, the general structure of the task remained highly
regular, and participants may still have formed expecta­
tions about the trial flow. Such procedural predictability
could be discriminated from fNIRS signals with accuracies
above the chance level when using a subset of channels
showing robust group-level effects. In particular, the effec­
tive-CH model, consisting of only three channels, achieved
the highest accuracy (73.7%), suggesting the potential fea­
sibility of developing compact and cost-effective fNIRS-
based BCI systems for auditory selective attention tasks. For
BCIs, especially those based on EEG or fNIRS, classifica­
tion accuracies in the range of 0.70–0.90 are not uncommon
(Huggins et al. 2011; Perelmouter and Birbaumer 2000),
indicating that our result lies within the functional range for
practical use, particularly in binary-choice communication
systems where some degree of error can be tolerated. Nev­
ertheless, surveys of potential end-users, such as individuals
with amyotrophic lateral sclerosis (ALS), show that many
prioritize accuracies of at least 90% as a key requirement
(Huggins et al. 2011). Thus, while our current accuracy is
encouraging, further improvements toward this target will
be necessary for widespread adoption. One important limitation is the potential risk of circular
analysis (“double dipping”), as the same dataset was used
for both feature selection and classification. This approach
can lead to optimistically biased accuracy estimates. It is
also important to note that statistical significance at the
group level does not necessarily imply high classification
performance at the individual level (Hebart and Baker 2018; Haufe et al. 2014). Indeed, Haufe et al. (2014) demonstrated
that features showing high statistical significance are not
guaranteed to improve classification accuracy, especially in
high-dimensional neuroimaging data. In addition, the rela­
tively small sample size (n = 19) limits the generalizability
of the classification results. Therefore, the classification
analysis in this study should be regarded as exploratory in
nature, intended to evaluate the feasibility of distinguish­
ing attentional states from DLPFC activation patterns rather
than to establish a generalizable predictive model. There­
fore, we consider our classification analysis as providing
complementary evidence to the statistical results by directly
testing whether the observed effects can be used for pre­
diction. Future studies should validate the approach using
independent feature selection, larger and more diverse par­
ticipant samples, and external datasets to rigorously assess
generalizability. For this purpose, it will be important to
identify features that can reduce or tolerate trial-to-trial
variability among participants and investigate more optimal
learning methods (Aydin 2020; Hong et al. 2018; Kwon and
Im 2021; Petrantonakis and Kompatsiaris 2018). Beyond the considerations specific to the classifica­
tion analysis, this study had some additional limitations. First, the effect of gender differences should be consid­
ered, although we restricted the gender of the participants
to males, primarily because of potential gender differences
1 3

Page 12 of 16

Brain Topography (2026) 39:8
Declarations
Competing Interests  The authors declare no competing interests. Ethical Approval  The Biotechnology Research Ethics Committee of
the Shibaura Institute of Technology approved this study (Receipt No.
21 − 012). Informed consent was obtained from all the participants
before the experiment. The experimental protocol was performed in
accordance with the “Guidelines for ethics-related problems with non-
invasive research on human brain function” established by the Japan
Neuroscience Society. Open Access  This article is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivatives 4.0 International License,
which permits any non-commercial use, sharing, distribution and
reproduction in any medium or format, as long as you give appropri­
ate credit to the original author(s) and the source, provide a link to the
Creative Commons licence, and indicate if you modified the licensed
material. You do not have permission under this licence to share
adapted material derived from this article or parts of it. The images or
other third party material in this article are included in the article’s Cre­
ative Commons licence, unless indicated otherwise in a credit line to
the material. If material is not included in the article’s Creative Com­
mons licence and your intended use is not permitted by statutory regu­
lation or exceeds the permitted use, you will need to obtain permission
directly from the copyright holder. To view a copy of this licence, visit ​
h​t​t​p​:​/​/​c​r​e​a​t​i​v​e​c​o​m​m​o​n​s​.​o​r​g​/​l​i​c​e​n​s​e​s​/​b​y​-​n​c​-​n​d​/​4​.​0​/. References
Alain C, Arnott S, Dyson B (2013) Varieties of auditory attention. In: Ochsner KN, Kosslin SM (eds) The Oxford handbook of cogni­
tive neuroscience: volume I core topics. Oxford University Press,
pp 215–236. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​3​/​o​x​f​o​r​d​h​b​/​9​7​8​0​1​9​9​9​8​8​6​9​3​.​0​
1​3​.​0​0​1​1
Ang KK, Guan C, Lee K, Lee JQ, Nioka S, Chance B (2010) A brain-
computer interface for mental arithmetic task from single-trial
near-infrared spectroscopy brain signals. Paper presented at
the 2010 20th International Conference on Pattern Recogni­
tion 3764–3767. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​C​P​R​.​2​0​1​0​.​9​1​7
Aoki R, Sato H, Katura T, Utsugi K, Koizumi K, Matsuda R, Maki
A (2011) Relationship of negative mood with prefrontal cortex
activity during working memory tasks: an optical topography
study. Neurosci Res 70(2):189–196. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​
u​r​e​s​.​2​0​1​1​.​0​2​.​0​1​1
Ayaz H, Shewokis PA, Bunce S, Izzetoglu K, Willems B, Onaral B
(2012) Optical brain monitoring for operator training and mental
workload assessment. Neuroimage 59(1):36–47. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​1​.​0​6​.​0​2​3
Aydin EA (2020) Subject-specific feature selection for near infrared
spectroscopy based brain-computer interfaces. Comput Methods
Programs Biomed 195:105535. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​c​m​p​b​.​2​
0​2​0​.​1​0​5​5​3​5
Bengtsson SL, Ullén F, Ehrsson H, Hashimoto H, Kito T, Naito T, Forssberg E, H., Sadato N (2009) Listening to rhythms activates
motor and premotor cortices. Cortex 45(1):62–71. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​
/​1​0​.​1​0​1​6​/​j​.​c​o​r​t​e​x​.​2​0​0​8​.​0​7​.​0​0​2
Birbaumer N (2006) Breaking the silence: Brain-computer interfaces
(BCI) for communication and motor control. Psychophysiology
43(6):517–532. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​1​1​/​j​.​1​4​6​9​-​8​9​8​6​.​2​0​0​6​.​0​0​4​5​6​.​
x
Borgheai SB, McLinden J, Zisk AH, Hosni SI, Deligani RJ, Abtahi
M, Mankodiya K, Shahriari Y (2020) Enhancing communication
could contribute to reduced attentional engagement in later
portions of the task and may partially explain the weaker
hemodynamic responses observed in the second half of the
task window. Nevertheless, as each trial presented different
auditory content and the questions were only revealed after
stimulus offset, participants were still required to attend to
the entire stimulus to answer correctly. In actual BCI use,
habituation to stimuli and tasks may occur over extended
sessions, and continuous task practice is known to decrease
the range and intensity of activation in attention and control
areas, including the prefrontal cortex, anterior cingulate cor­
tex, and posterior parietal cortex (Kelly and Garavan 2005). Further studies are required to investigate these issues and
to develop strategies to mitigate potential habituation or
early-trial attention biases. In conclusion, we investigated the relationship between
the control of auditory selective attention and brain activ­
ity and attempted to classify brain activity using common
trends among participants. In investigating brain activity for
auditory selective attention, we used dichotic listening stim­
uli comprising both music and reading sounds and found
significant activation, mainly in the DLPFC. This activa­
tion was particularly pronounced in the right hemisphere,
which may correspond to the right frontoparietal network
associated with attentional control. BA6 exhibited increased
activity during attention to music, whereas BA46 was more
active during attention to reading sound. Focusing on chan­
nels that exhibited activation dependent on the attentional
target, we attempted an exploratory cross-participant classi­
fication, which achieved a promising classification accuracy
of 73.7%. This result suggests the potential applicability of
fNIRS-based BCIs that leverage auditory selective attention
control. In future studies, we aim to adapt these findings to
individual properties to further enhance accuracy. Supplementary
Information  The
online
version
contains
supplementary material available at ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​1​0​5​4​8​-​0​
2​5​-​0​1​1​6​2​-​7. Acknowledgements  We thank Mr. K. Osumi, Mr. Y. Morita and Mr. R. Satake for their helpful assistance. We also thank Dr. N. Tanaka and
Mr. K. Ozawa for the meaningful discussions we had with them. Author Contributions  TY: conceptualization, investigation, methodol­
ogy, formal analysis, validation, visualization, writing - original draft,
writing - review and editing. RH: methodology, writing-review and
editing, HS: conceptualization, investigation, methodology, writing-
review and editing, funding acquisition, project administration, super­
vision. Funding  This work was supported by JSPS KAKENHI Grant Number
20K11367. There are no conflicts of interest to disclose. Data Availability  Raw data in support of the conclusions of this article
will be available from the authors upon request.
1 3
Page 13 of 16

Brain Topography (2026) 39:8
Front Hum Neurosci 12:246. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​3​8​9​/​f​n​h​u​m​.​2​0​1​
8​.​0​0​2​4​6
Huang S, Seidman LJ, Rossi S, Ahveninen J (2013) Distinct cortical
networks activated by auditory attention and working memory
load. Neuroimage 83:1098–1108. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​
i​m​a​g​e​.​2​0​1​3​.​0​7​.​0​7​4
Hugdahl K, Westerhausen R (2016) Speech processing asymmetry
revealed by dichotic listening and functional brain imaging. Neu­
ropsychologia 93(B):466–481. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​p​s​
y​c​h​o​l​o​g​i​a​.​2​0​1​5​.​1​2​.​0​1​1
Huggins JE, Wren PA, Gruis KL (2011) What would brain-computer
interface users want? Opinions and priorities of potential users
with amyotrophic lateral sclerosis. Amyotroph Lateral Scler
12(5):318–324. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​1​0​9​/​1​7​4​8​2​9​6​8​.​2​0​1​1​.​5​7​2​9​7​8
Jäncke L, Specht K, Shah JN, Hugdahl K (2003) Focused attention
in a simple dichotic listening task: an fMRI experiment. Cogn
Brain Res 16(2):257–266. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​s​0​9​2​6​-​6​4​1​0​(​0​
2​)​0​0​2​8​1​-​1
Jones PR, Moore DR, Amitay S (2015) Development of auditory
selective attention: why children struggle to hear in noisy envi­
ronments. Dev Psychol 51(3):353–369. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​3​7​/​
a​0​0​3​8​5​7​0
Kamran MA, Mannan MMN, Jeong MY (2016) Cortical signal analy­
sis and advances in functional near-infrared spectroscopy signal:
a review. Front Hum Neurosci 10:261. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​3​8​9​/​f​n​
h​u​m​.​2​0​1​6​.​0​0​2​6​1
Kane MJ, Engle RW (2002) The role of prefrontal cortex in working-
memory capacity, executive attention, and general fluid intelli­
gence: an individual-differences perspective. Psychon Bull Rev
9(4):637–671. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​7​5​8​/​b​f​0​3​1​9​6​3​2​3
Kelly AMC, Garavan H (2005) Human functional neuroimaging of
brain changes associated with practice. Cereb Cortex (New York
N Y 1991) 15(8):1089–1102. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​3​/​c​e​r​c​o​r​/​b​h​i​0​
0​5
Khalili-Ardali M, Wu S, Tonin A, Birbaumer N, Chaudhary U (2021)
Neurophysiological aspects of the completely locked-in syn­
drome in patients with advanced amyotrophic lateral sclerosis. Clin Neurophysiol 132(5):1064–1076. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​
c​l​i​n​p​h​.​2​0​2​1​.​0​1​.​0​1​3
Kimura D (1967) Functional asymmetry of the brain in dichotic listen­
ing. Cortex 3(2):163–178. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​S​0​0​1​0​-​9​4​5​2​(​6​
7​)​8​0​0​1​0​-​8
Koizumi H, Yamamoto T, Maki A, Yamashita Y, Sato H, Kawaguchi
H, Ichikawa N (2003) Optical topography: practical problems and
new applications. Appl Opt 42(16):3054–3062. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​6​4​/​A​O​.​4​2​.​0​0​3​0​5​4
Kompus K, Specht K, Ersland L, Juvodden HT, van Wageningen H, Hugdahl K, Westerhausen R (2012) A forced-attention dichotic
listening fMRI study on 113 subjects. Brain Lang 121(3):240–
247. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​b​a​n​d​l​.​2​0​1​2​.​0​3​.​0​0​4
Kong L, Michalka SW, Rosen ML, Sheremata SL, Swisher JD, Shinn-
Cunningham BG, Somers DC (2014) Auditory spatial attention
representations in the human cerebral cortex. Cereb Cortex (New
York N Y 1991) 24(3):773–784. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​3​/​c​e​r​c​o​r​/​
b​h​s​3​5​9
Kübler A, Birbaumer N (2008) Brain–computer interfaces and com­
munication in paralysis: extinction of goal directed thinking in
completely paralysed patients? Clin Neurophysiol 119(11):2658–
2666. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​c​l​i​n​p​h​.​2​0​0​8​.​0​6​.​0​1​9
Kwon J, Im C (2021) Subject-independent functional near-infrared
spectroscopy-based brain–computer interfaces based on convolu­
tional neural networks. Front Hum Neurosci 15:646915. ​h​t​t​p​s​:​/​/​d​
o​i​.​o​r​g​/​1​0​.​3​3​8​9​/​f​n​h​u​m​.​2​0​2​1​.​6​4​6​9​1​5
Lee AKC, Larson E, Maddox RK, Shinn-Cunningham BG (2014)
Using neuroimaging to understand the cortical mechanisms of
for people in late-stage ALS using an fNIRS-based BCI system. IEEE Trans Neural Syst Rehabil Eng 28(5):1198–1207. ​h​t​t​p​s​:​/​/​d​o​
i​.​o​r​g​/​1​0​.​1​1​0​9​/​T​N​S​R​E​.​2​0​2​0​.​2​9​8​0​7​7​2
Chenji S, Jha S, Lee D, Brown M, Seres P, Mah D, Kalra S (2016)
Investigating default mode and sensorimotor network connectiv­
ity in amyotrophic lateral sclerosis. PLoS One 11(6):e0157443. ​h​
t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​7​1​/​j​o​u​r​n​a​l​.​p​o​n​e​.​0​1​5​7​4​4​3
Conson M, Sacco S, Sarà M, Pistoia F, Grossi D, Trojano L (2008)
Selective motor imagery defect in patients with locked-in syn­
drome. Neuropsychologia 46(11):2622–2628. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​
1​0​1​6​/​j​.​n​e​u​r​o​p​s​y​c​h​o​l​o​g​i​a​.​2​0​0​8​.​0​4​.​0​1​5
Crottaz-Herbette S, Anagnoson RT, Menon V (2004) Modality effects
in verbal working memory: differential prefrontal and parietal
responses to auditory and visual stimuli. Neuroimage 21(1):340–
351. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​0​3​.​0​9​.​0​1​9
Dehaene-Lambertz G, Dehaene S, Hertz-Pannier L (2002) Func­
tional neuroimaging of speech perception in infants. Science
298(5600):2013–2015. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​2​6​/​s​c​i​e​n​c​e​.​1​0​7​7​0​6​6
Della Penna S, Brancucci A, Babiloni C, Franciotti R, Pizzella V, Rossi D, Torquati K, Rossini PM, Romani GL (2007) Lateral­
ization of dichotic speech stimuli is based on specific auditory
pathway interactions: neuromagnetic evidence. Cereb Cortex
17(10):2303–2311. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​3​/​c​e​r​c​o​r​/​b​h​l​1​3​9
Eskicioglu E, Taslica S, Narin B, Guducu C, Oniz A, Ozgoren M
(2019) Brain asymmetry in directing attention during dichotic lis­
tening test: an fNIRS study. Laterality 24(4):377–392. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​8​0​/​1​3​5​7​6​5​0​X​.​2​0​1​8​.​1​5​2​7​8​4​7
Ferrari M, Quaresima V (2012) A brief review on the history of human
functional near-infrared spectroscopy (fNIRS) development and
fields of application. Neuroimage 63(2):921–935. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​2​.​0​3​.​0​4​9
Fox MD, Snyder AZ, McAvoy MP, Barch DM, Raichle ME (2005)
The BOLD onset transient: identification of novel functional dif­
ferences in schizophrenia. Neuroimage 25(3):771–782. ​h​t​t​p​s​:​/​/​d​o​
i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​0​4​.​1​2​.​0​2​5
Fritz JB, Elhilali M, David SV, Shamma SA (2007) Auditory atten­
tion–focusing the searchlight on sound. Curr Opin Neurobiol
17(4):437–455. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​c​o​n​b​.​2​0​0​7​.​0​7​.​0​1​1
Gazzaley A, Nobre AC (2012) Top-down modulation: bridging selec­
tive attention and working memory. Trends Cogn Sci 16(2):129–
135. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​t​i​c​s​.​2​0​1​1​.​1​1​.​0​1​4
Gordon CL, Cobb PR, Balasubramaniam R (2018) Recruitment of the
motor system during music listening: an ALE meta-analysis of
fMRI data. PLoS One 13(11):e0207213. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​7​1​
/​j​o​u​r​n​a​l​.​p​o​n​e​.​0​2​0​7​2​1​3
Haufe S, Meinecke F, Görgen K, Dähne S, Haynes JD, Blankertz B, Bießmann F (2014) On the interpretation of weight vectors of
linear models in multivariate neuroimaging. Neuroimage 87:96–
110. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​3​.​1​0​.​0​6​7
Hebart MN, Baker CI (2018) Deconstructing multivariate decoding for
the study of brain function. Neuroimage 180(Part A):4–18. ​h​t​t​p​s​:​
/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​7​.​0​8​.​0​0​5
Herold F, Wiegel P, Scholkmann F, Müller NG (2018) Applications of
functional near-infrared spectroscopy (fNIRS) neuroimaging in
exercise–cognition science: a systematic, methodology-focused
review. J Clin Med 7(12):466. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​3​9​0​/​j​c​m​7​1​2​0​
4​6​6
Homae F, Watanabe H, Otobe T, Nakano T, Go T, Konishi Y, Taga G
(2010) Development of global cortical networks in early infancy. J Neuroscience: Official J Soc Neurosci 30(14):4877–4882. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​5​2​3​/​J​N​E​U​R​O​S​C​I​.​5​6​1​8​-​0​9​.​2​0​1​0
Hong K, Naseer N, Kim Y (2015) Classification of prefrontal and
motor cortex signals for three-class fNIRS-BCI. Neurosci Lett
587:87–92. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​l​e​t​.​2​0​1​4​.​1​2​.​0​2​9
Hong K, Khan MJ, Hong MJ (2018) Feature extraction and classifica­
tion methods for hybrid fNIRS-EEG brain-computer interfaces.
1 3

Page 14 of 16

Brain Topography (2026) 39:8
Petrantonakis PC, Kompatsiaris I (2018) Single-trial NIRS data classi­
fication for brain-computer interfaces using graph signal process­
ing. IEEE Trans Neural Syst Rehabil Eng 26(9):1700–1709. ​h​t​t​p​
s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​T​N​S​R​E​.​2​0​1​8​.​2​8​6​0​6​2​9
Plakke B, Romanski LM (2014) Auditory connections and functions
of prefrontal cortex. Front Neurosci 8:199. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​3​
8​9​/​f​n​i​n​s​.​2​0​1​4​.​0​0​1​9​9
Power SD, Kushki A, Chau T (2012) Intersession consistency of sin­
gle-trial classification of the prefrontal response to mental arith­
metic and the no-control state by NIRS. PLoS One 7(7):e37791. ​
h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​7​1​/​j​o​u​r​n​a​l​.​p​o​n​e​.​0​0​3​7​7​9​1
Ptak R, Schnider A, Fellrath J (2017) The dorsal frontoparietal net­
work: a core system for emulated action. Trends Cogn Sci
21(8):589–599. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​t​i​c​s​.​2​0​1​7​.​0​5​.​0​0​2
Pugh KR, Shaywitz BA, Shaywitz SE, Fulbright RK, Byrd D, Skudlar­
ski P, Shankweiler DP, Katz L, Constable RT, Fletcher J, Lacadie
C, Marchione K, Gore JC (1996) Auditory selective attention: an
fMRI investigation. Neuroimage 4(3):159–173. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​0​6​/​n​i​m​g​.​1​9​9​6​.​0​0​6​7
Ridderinkhof KR, Van Der Stelt O (2000) Attention and selection in
the growing child: views derived from developmental psycho­
physiology. Biol Psychol 54(1–3):55–106. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​
6​/​s​0​3​0​1​-​0​5​1​1​(​0​0​)​0​0​0​5​3​-​3
Sato H, Takeuchi T, Sakai KL (1999) Temporal cortex activation dur­
ing speech recognition: an optical topography study. Cognition
73(3): B55–B66.
​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​S​0​0​1​0​-​0​2​7​7​(​9​9​)​0​0​0​6​
0​-​8
Sato H, Katura T, Koizumi H, Aoki R, Matsuda R (2011) Correlation
of within-individual fluctuation of depressed mood with prefron­
tal cortex activity during verbal working memory task: optical
topography study. J Biomed Opt 16(12):126007. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​
/​1​0​.​1​1​1​7​/​1​.​3​6​6​2​4​4​8
Sato H, Hirabayashi Y, Tsubokura H, Kanai M, Ashida T, Konishi I, Uchida-Ota M, Konishi Y, Maki A (2012) Cerebral hemodynam­
ics in newborn infants exposed to speech sounds: a whole‐head
optical topography study. Hum Brain Mapp 33(9):2092–2103. ​h​t​
t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​2​/​h​b​m​.​2​1​3​5​0
Sato H, Yahata N, Funane T, Takizawa R, Katura T, Atsumori H, Nishimura Y, Kinoshita A, Kiguchi M, Koizumi H, Fukuda M, Kasai K (2013) A NIRS-fMRI investigation of prefrontal cortex
activity during a working memory task. Neuroimage 83:158–173. ​
h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​3​.​0​6​.​0​4​3
Sato H, Kiguchi M, Maki A, Fuchino Y, Obata A, Yoro T, Koizumi H
(2006) Within-subject reproducibility of near-infrared spectros­
copy signals in sensorimotor activation after 6  months. J Biomed
Opt 11(1):014021. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​1​7​/​1​.​2​1​6​6​6​3​2
Schudlo LC, Chau T (2014) Dynamic topographical pattern classifica­
tion of multichannel prefrontal NIRS signals: II. online differen­
tiation of mental arithmetic and rest. J Neural Eng 11(1):016003. ​
h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​8​8​/​1​7​4​1​-​2​5​6​0​/​1​1​/​1​/​0​1​6​0​0​3
Shin J, Müller NR, Hwang H (2016) Near-infrared spectroscopy
(NIRS)-based eyes-closed brain-computer interface (BCI) using
prefrontal cortex activation due to mental arithmetic. Sci Rep
6:36203. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​3​8​/​s​r​e​p​3​6​2​0​3
Singh AK, Okamoto M, Dan H, Jurcak V, Dan I (2005) Spatial regis­
tration of multichannel multi-subject fNIRS data to MNI space
without MRI. Neuroimage 27(4):842. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​
e​u​r​o​i​m​a​g​e​.​2​0​0​5​.​0​5​.​0​1​9
Sitaram R, Zhang H, Guan C, Thulasidas M, Hoshi Y, Ishikawa A, Shimizu K, Birbaumer N (2007) Temporal classification of multi­
channel near-infrared spectroscopy signals of motor imagery for
developing a brain–computer interface. Neuroimage 34(4):1416–
1427. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​0​6​.​1​1​.​0​0​5
Sutoko S, Sato H, Maki A, Kiguchi M, Hirabayashi Y, Atsumori H, Obata A, Funane T, Katura T (2016) Tutorial on platform for
auditory selective attention. Hear Res 307:111–120. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​
g​/​1​0​.​1​0​1​6​/​j​.​h​e​a​r​e​s​.​2​0​1​3​.​0​6​.​0​1​0
Li C, Chen K, Han H, Chui D, Wu J (2012) An fMRI study of the neu­
ral systems involved in visually cued auditory top-down spatial
and temporal attention. PLoS One 7(11):e49948. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​3​7​1​/​j​o​u​r​n​a​l​.​p​o​n​e​.​0​0​4​9​9​4​8
Lima CF, Krishnan S, Scott SK (2016) Roles of supplementary motor
areas in auditory processing and auditory imagery. Trends Neu­
rosci 39(8):527–542. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​t​i​n​s​.​2​0​1​6​.​0​6​.​0​0​3
Limb CJ (2006) Structural and functional neural correlates of music
perception. Anat Rec 288(4):435–446. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​2​/​a​
r​.​a​.​2​0​3​1​6
Majidpour A, Moheb Aleaba M, Aghamolaei M, Nazeri A (2022)
Review of the factors affecting dichotic listening. Auditory Vestib
Res 31(2). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​8​5​0​2​/​a​v​r​.​v​3​1​i​2​.​9​1​1​1
Maki A, Yamashita Y, Ito Y, Watanabe E, Mayanagi Y, Koizumi H
(1995) Spatial and temporal analysis of human motor activity
using noninvasive NIR topography. Med Phys 22(12):1997–
2005. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​1​8​/​1​.​5​9​7​4​9​6
Mei N, Flinker A, Zhu M, Cai Q, Tian X (2020) Lateralization in the
dichotic listening of tones is influenced by the content of speech. Neuropsychologia 140:107389. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​p​s​
y​c​h​o​l​o​g​i​a​.​2​0​2​0​.​1​0​7​3​8​9
Monden Y, Dan I, Nagashima M, Dan H, Uga M, Ikeda T, Tsuzuki D, Kyutoku Y, Gunji Y, Hirano D, Taniguchi T, Shimoizumi H, Wata­
nabe E, Yamagata T (2015) Individual classification of ADHD
children by right prefrontal hemodynamic responses during a go/
no-go task as assessed by fNIRS. Neuroimage Clin 9:1–12. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​i​c​l​.​2​0​1​5​.​0​6​.​0​1​1
Murguialday AR, Hill J, Bensch M, Martens S, Halder S, Nijboer F, Schoelkopf B, Birbaumer N, Gharabaghi A (2011) Transition
from the locked in to the completely locked-in state: a physiologi­
cal analysis. Clin Neurophysiol 122(5):925–933. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​1​6​/​j​.​c​l​i​n​p​h​.​2​0​1​0​.​0​8​.​0​1​9
Naito M, Michioka Y, Ozawa K, Ito Y, Kiguchi M, Kanazawa T (2007)
A communication means for totally locked-in ALS patients based
on changes in cerebral blood volume measured with near-infrared
light. IEICE Trans Inf Syst 90(7):1028–1037. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​
0​9​3​/​i​e​t​i​s​y​/​e​9​0​-​d​.​7​.​1​0​2​8
Naseer N, Hong K (2013) Classification of functional near-infrared
spectroscopy signals corresponding to the right- and left-wrist
motor imagery for development of a brain-computer interface. Neurosci Lett 553:84–89. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​l​e​t​.​2​0​1​3​.​
0​8​.​0​2​1
Naseer N, Hong K (2015) fNIRS-based brain-computer interfaces: a
review. Front Hum Neurosci 9:3. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​3​8​9​/​f​n​h​u​m​.​2​0​1​5​.​0​0​0​0​3
Nichols TE, Holmes AP (2002) Nonparametric permutation tests for
functional neuroimaging: a primer with examples. Hum Brain
Mapp 15(1):1–25. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​2​/​h​b​m​.​1​0​5​8
Okada K, Rong F, Venezia J, Matchin W, Hsieh I, Saberi K, Serences
JT, Hickok G (2010) Hierarchical organization of human auditory
cortex: evidence from acoustic invariance in the response to intel­
ligible speech. Cereb Cortex (New York N Y 1991) 20(10):2486–
2495. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​3​/​c​e​r​c​o​r​/​b​h​p​3​1​8
Pastuszek-Lipińska B (2025) The role of musical aspects of language
in human cognition. Front Psychol 16:1505694. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​3​3​8​9​/​f​p​s​y​g​.​2​0​2​5​.​1​5​0​5​6​9​4
Perani D, Saccuman MC, Scifo P, Spada D, Andreolli G, Rovelli R, Baldoli C, Koelsch S (2010) Functional specializations for music
processing in the human newborn brain. Proc Natl Acad Sci U S
A 107(10):4758–4763. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​7​3​/​p​n​a​s​.​0​9​0​9​0​7​4​1​0​7
Perelmouter J, Birbaumer N (2000) A binary spelling interface with
random errors. IEEE Trans Rehabil Eng 8(2):227–232. ​h​t​t​p​s​:​/​/​d​o​
i​.​o​r​g​/​1​0​.​1​1​0​9​/​8​6​.​8​4​7​8​2​4
1 3
Page 15 of 16

Brain Topography (2026) 39:8
Neurosci Lett 256(1):49–52. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​S​0​3​0​4​-​3​9​4​
0​(​9​8​)​0​0​7​5​4​-​X
Wei X, Yoo S, Dickey CC, Zou KH, Guttmann CRG, Panych LP (2004)
Functional MRI of auditory verbal working memory: long-term
reproducibility analysis. Neuroimage 21(3):1000–1008. ​h​t​t​p​s​:​/​/​d​
o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​0​3​.​1​0​.​0​3​9
Wen T, Duncan J, Mitchell DJ (2019) The time-course of component
processes of selective attention. Neuroimage 199:396–407. ​h​t​t​p​s​:​
/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​9​.​0​5​.​0​6​7
Westerhausen R (2019) A primer on dichotic listening as a para­
digm for the assessment of hemispheric asymmetry. Laterality
24(6):740–771. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​8​0​/​1​3​5​7​6​5​0​x​.​2​0​1​9​.​1​5​9​8​4​2​6
Westerhausen R, Moosmann M, Alho K, Belsby S, Hämäläinen H, Medvedev S, Specht K, Hugdahl K (2010) Identification of atten­
tion and cognitive control networks in a parametric auditory
fMRI study. Neuropsychologia 48(7):2075–2081. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​p​s​y​c​h​o​l​o​g​i​a​.​2​0​1​0​.​0​3​.​0​2​8
Yamada T, Umeyama S, Matsuda K (2012) Separation of fNIRS sig­
nals into functional and systemic components based on differ­
ences in hemodynamic modalities. PLoS One 7(11):e50271. ​h​t​t​
p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​7​1​/​j​o​u​r​n​a​l​.​p​o​n​e​.​0​0​5​0​2​7​1
Yücel MA, Lühmann AV, Scholkmann F, Gervain J, Dan I, Ayaz H, Boas D, Cooper RJ, Culver J, Elwell CE, Eggebrecht A, Fran­
ceschini MA, Grova C, Homae F, Lesage F, Obrig H, Tachtsidis
I, Tak S, Tong Y, Torricelli A, Wabnitz H, Wolf M (2021) Best
practices for fNIRS publications. Neurophotonics 8(1):012101. ​h​
t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​1​7​/​1​.​N​P​h​.​8​.​1​.​0​1​2​1​0​1
Publisher’s Note  Springer Nature remains neutral with regard to juris­
dictional claims in published maps and institutional affiliations.
optical topography analysis tools. Neurophotonics 3(1):010801.
​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​1​7​/​1​.​N​P​h​.​3​.​1​.​0​1​0​8​0​1
Taga G, Asakawa K, Maki A, Konishi Y, Koizumi H (2003) Brain
imaging in awake infants by near-infrared optical topography. Proc Natl Acad Sci USA 100(19):10722–10727. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​
1​0​.​1​0​7​3​/​p​n​a​s​.​1​9​3​2​5​5​2​1​0​0
Takizawa R, Fukuda M, Kawasaki S, Kasai K, Mimura M, Pu S, Noda
T, Niwa S, Okazaki Y, Joint Project for Psychiatric Applica­
tion of Near-Infrared Spectroscopy (JPSY-NIRS) Group (2014)
Neuroimaging-aided differential diagnosis of the depressive state. Neuroimage 85(1):498–507. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​
e​.​2​0​1​3​.​0​5​.​1​2​6
Thimm M, Weis S, Hausmann M, Sturm W (2014) Menstrual cycle
effects on selective attention and its underlying cortical networks. Neuroscience 258:307–317. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​s​c​i​e​n​
c​e​.​2​0​1​3​.​1​1​.​0​1​0
Thomsen T, Rimol LM, Ersland L, Hugdahl K (2004) Dichotic listen­
ing reveals functional specificity in prefrontal cortex: an fMRI
study. Neuroimage 21(1):211–218. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​
r​o​i​m​a​g​e​.​2​0​0​3​.​0​8​.​0​3​9
Vigneau M, Beaucousin V, Hervé PY, Duffau H, Crivello F, Houdé
O, Mazoyer B, Tzourio-Mazoyer N (2006) Meta-analyzing left
hemisphere language areas: phonology, semantics, and sentence
processing. Neuroimage 30(4):1414–1432. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​
6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​0​5​.​1​1​.​0​0​2
Voyer D (2011) Sex differences in dichotic listening. Brain Cogn
76(2):245–255. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​b​a​n​d​c​.​2​0​1​1​.​0​2​.​0​0​1
Watanabe E, Maki A, Kawaguchi F, Takashiro K, Yamashita Y, Koi­
zumi H, Mayanagi Y (1998) Non-invasive assessment of lan­
guage dominance with near-infrared spectroscopic mapping.
1 3

Page 16 of 16
