# © The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0

**Year:** D:20

---

RESEARCH
Open Access
© The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0
International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you
give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the
licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or
other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the
material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or
exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit ​h​t​t​p​:​/​/​c​r​e​a​t​i​
v​e​c​o​m​m​o​n​s​.​o​r​g​/​l​i​c​e​n​s​e​s​/​b​y​-​n​c​-​n​d​/​4​.​0​/. Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
https://doi.org/10.1186/s12984-025-01778-7
Journal of NeuroEngineering
and Rehabilitation
†Haojie Li, Xinyu Lin: co-first authorship.
*Correspondence: Xie Wu
wuxie_sus@163.com
Full list of author information is available at the end of the article
Abstract
Background  While music is known to influence exercise performance through auditory-motor coupling, the
biomechanical mechanisms by which musical groove—characterized by rhythmic drive and movement-inducing
qualities—modulates cycling coordination remain poorly understood. This study investigates how groove levels
systematically alter lower extremity kinematics and neuromuscular control during high-torque cycling. Methods  Twenty-four well-trained, right-handed cyclists completed high-torque cycling trials under three
counterbalanced conditions: metronome (control), low-groove (LG), and high-groove (HG) music, with groove levels
objectively classified by a validated deep learning model (R2 = 0.85). Three-dimensional motion capture (200Hz)
quantified hip-ankle and pelvis-torso coordination using vector coding techniques, while surface electromyography
(EMG) of 12 lower limb muscles was analyzed via non-negative matrix factorization (NMF) to extract muscle synergy
patterns. The NMF approach decomposes multi-muscle activation patterns into fundamental synergistic components,
providing insight into neuromuscular control strategies. Results  Compared to LG and control conditions, HG music significantly: (1) increased hip-ankle in-phase
coordination by 28.7% (HG:29.8% vs. LG:23.2%, p = 0.020), (2) enhanced pelvis-torso synchronization by 27.1%
(HG:38.0% vs. LG:29.9%, p = 0.048), and (3) promoted greater muscle synergy complexity (median synergies: HG = 7
vs LG = 6, p = 0.039). Notably, the soleus (SOL) muscle—crucial for ankle stabilization—showed significantly higher
activation weights in HG condition (0.11 ± 0.03 vs 0.04 ± 0.02, p = 0.030), suggesting improved distal control. The
emergence of a unique erector spinae-gastrocnemius lateralis (ES-GL) synergy pattern (present in 54% of HG trials)
indicates enhanced trunk-limb coupling under high-groove conditions. Conclusion  High-groove music promotes more coordinated movement patterns during cycling through two
key mechanisms: (1) optimized joint coordination, particularly in proximal–distal (hip-ankle) and axial (pelvis-torso)
linkages, and (2) reorganization of neuromuscular control strategies evidenced by increased synergy complexity and
Impact of Neural network-quantified
musical groove on cyclists’ joint coordination
and muscle synergy: a repeated measures
study
Haojie Li1†, Xinyu Lin1† and Xie Wu1*

Page 2 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
Introduction
The application of music in exercise science is increas­
ingly valued, with its influence on performance through
multimodal perception becoming a key interdisciplin­
ary research focus [1]. Music has been shown to enhance
exercise performance and reduce perceived fatigue via
neuromodulator mechanisms [2]. This effect is closely
tied to temporal structural features of music—such as
pulse, beat salience, and groove—which trigger sponta­
neous motor responses through auditory-motor coupling
[3]. Rhythm, a core temporal feature of music, is defined
as a multidimensional property that promotes movement
synchronization and pleasure through integrated acous­
tic features and predictive cognition [4]. Its mechanisms
include: (1) moderate prediction error from syncopation,
(2) a motor reference frame from beat salience gradients,
(3) cognitive engagement modulated by event density,
and (4) bio motor resonance driven by low-frequency
acoustic cues [5]. High-groove music activates basal gan­
glia–motor pathways, enabling motor timing prediction
via beta-band oscillation and shifting auditory percep­
tion from passive reception to active simulation [6]. Tra­
ditional research often categorizes music simplistically
as either synchronous or asynchronous based solely on
beats per minute (BPM) alignment with movement [7]. This linear approach has limitations: BPM reflects tem­
poral resolution but not groove complexity [8]. Ignoring
groove’s role in sensorimotor synchronization may lead
to varied motor coupling effects even under identical
BPM [9]. Dynamic Systems Theory suggests that motor-
music synchronization is a multidimensional coupling
process involving beat predictability, groove complexity,
and biomechanical constraints [10]. Although groove’s
impact on motor performance is established, its mecha­
nisms remain underexplored due to a methodological
challenge: quantifying groove as a multidimensional fea­
ture [11]. Unlike unidimensional BPM, groove perception
involves dynamic interactions among acoustic features
and cognitive prediction, requiring a comprehensive
evaluation framework covering temporal, spectral, and
experiential dimensions [12]. Early quantitative studies employed behavioral para­
digms, such as Elliott et al.'s use of a phase synchrony
index to measure finger tapping alignment with musi­
cal events, establishing a groove potency scoring system
[13]. However, this approach has limitations: the stimulus
repertoire was limited to older popular music, and musi­
cal familiarity—modulating striatal dopamine via mem­
ory reconsolidation—may introduce generational bias
in groove perception. Additionally, simplified harmonic
processing controls groove complexity but removes eco­
logically critical features like dynamic compression and
low-frequency resonance, reducing ecological valid­
ity [14]. Recent advances in artificial intelligence, par­
ticularly music information retrieval (MIR), offer a new
paradigm. By extracting 21-dimensional acoustic features
(e.g., pulse clarity, groove flux) and modeling their rela­
tionship with movement synchronization, researchers
have achieved high predictive accuracy (R2 = 0.704) for
music-induced arousal [15], supporting the feasibility of
kinematic-acoustic feature modeling to decipher groove
mechanisms. In exercise science, muscle synergy and
joint coordination form a dual framework for analyzing
neural motor control [16]. Joint coordination emerges
as a biomechanical expression of muscle synergy—the
nervous system’s solution for multi-joint control via
temporal coupling [17]. Muscle synergy reflects a neu­
ral strategy where the CNS combines limited synergis­
tic modules, rather than controlling individual muscles,
to simplify movement control under biomechanical and
neural constraints [19]. This is evident in rhythmic activi­
ties like cycling, where phase-locked activation of lower-
limb muscle groups occurs [20]. Joint coordination,
quantifiable through vector coding of inter-joint phase
relationships [21], exhibits temporal coupling influenced
by synergy topology, while proprioceptive feedback fine-
tunes synergy activation coefficients [22]. Musical groove influences the motor system through
two main pathways. First, its beat salience and low-fre­
quency harmonics improve the timing accuracy of mus­
cle synergy activation by enhancing beta-band oscillation
synchronization between auditory and motor regions,
facilitated by the basal ganglia [23]. Second, pulse clar­
ity enhances inter-joint phase locking and promotes
more efficient hip-knee-ankle coordination in the sagit­
tal plane, approaching a biomechanically optimal pattern
[24]. These neural and biomechanical effects together
optimize motor control: muscle synergy reorganiza­
tion improves joint moment covariance, while adjust­
ments in synergy activation fine-tune kinematics via
proprioceptive feedback [22]. Groove perception also
aids internal–external rhythm matching [25], improving
selective activation of postural stabilizers (SOL). These findings provide biomechanical evidence supporting groove-
based auditory-motor interventions, though direct performance benefits require verification through additional
kinetic and metabolic measures. The successful application of deep learning for groove quantification establishes a
framework for personalized music selection in sports and rehabilitation contexts. Keywords  Auditory-motor synchronization, Neuromechanics, Exercise enhancement, Deep learning in sports, Biomechanical efficiency, Rhythmic entrainment

Page 3 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
contraction timing and neuromuscular control. Addition­
ally, by reducing control dimensionality, music may help
minimize energy dissipation in muscle and joint systems,
supporting movement efficiency [26]. Cycling, with its
cyclic, multi-joint, and stabilized motion pattern, offers a
suitable model for studying groove effects [27, 28]. How­
ever, how musical groove influences cycling performance
and neuromuscular control remains underexplored. This
study aims to investigate the effects of groove features
on cycling performance, joint coordination, and muscle
synergy patterns, to reveal how music optimizes neuro­
muscular control, and to provide theoretical support for
music selection in practical exercise. Participants and methods
Participants
A total of 24 right-handed university students (12 women,
12 men; age 21.1 ± 1.4 years) were recruited. The a-priori
sample size was computed with G*Power 3.1 (Düsseldorf, Germany) for a repeated-measures ANOVA (within-
factor effect size = 0.01, α = 0.05, power = 0.90, correlation
among repeated measures = 0.5); the analysis indicated
that a minimum of 23 participants was required. Inclu­
sion criteria: (a) age 18–25 years; (b) regular exercis­
ers performing ≥ 3 sessions per week, each lasting at
least 30 min; (c) high interest in music or demonstrable
musical understanding; (d) familiar with bicycle opera­
tion and able to cycle unaided in the laboratory; and (e)
signed informed consent. Exclusion criteria: (a) history
of cardiovascular, respiratory, or neurological disorders;
(b) systematic cycling or competitive training within the
past year; (c) participation in any music-assisted cycling
intervention within the past three months; (d) acute or
chronic conditions limiting exercise capacity; (e) audi­
tory impairments or other sensorimotor deficits that
could compromise data collection; and (f) current use
of psychoactive medication (e.g., antidepressants, anxio­
lytics, or sedatives). All participants wore standardized
athletic attire (short-sleeved T-shirt and shorts). After
receiving a full explanation of the experimental risks,
they provided written informed consent. The protocol
adhered to the Declaration of Helsinki and was approved
by the Beijing Normal University Ethics Committee
(ICBIR_B_0213_001). Participants’ baseline characteris­
tics are presented in Table 1. Methods
Experimental design
This study utilized a repeated measures design. Subjects
visited the laboratory at three different time points, each
visit being 24 h apart. The first visit served two purposes. The first was to establish a baseline of the subjects' per­
formance on music-free rides and to familiarize them
with the power bike and exercise protocol. The torque
was set at 5 N-m and the ride duration was 3 min, fol­
lowed by a 30-min rest period. The second objective was
to perform a formal riding task in the synchronized met­
ronome condition (MT) as a Control group. At the sec­
ond visit, subjects completed the riding task in the low
groove music condition (LG). At the third visit, subjects
completed the riding task in the high-groove music con­
dition (HG). The experimental flow is shown in Fig. 1. To ensure consistency across all experimental vis­
its (MT, LG, and HG conditions), the electromyogram
(EMG) electrodes were reapplied before each session by
the same trained operator, following a strict standardized
protocol: Reapply the electromyography sensor before each visit
test. Skin Preparation: The skin over target muscles was
shaved and cleaned with alcohol to minimize impedance
variability. Electrode Placement: Sensors (Delsys wire­
less EMG, 10-mm inter-electrode spacing) were posi­
tioned according to SENIAM guidelines [29]. Operator
Table 1  Characteristics of subjects
Parameter
Male
Female
Age (years)
20.66 ± 1.07
20.66 ± 0.88
Height (cm)
173.65 ± 4.38
167.73 ± 3.44
Weight (kg)
68.11 ± 7.45
55.42 ± 9.27
Body mass index (kg/m2)
23.54 ± 2.61
20.41 ± 2.97
Fig. 1  Design of the research experiment

Page 4 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
Consistency: A single researcher handled all electrode
placements to eliminate inter-operator variability. This
approach ensured identical sensor positioning and mus­
cle sampling across visits, guaranteeing that observed
differences in muscle synergy patterns reflect true neu­
romuscular adaptations to rhythmic stimuli, not mea­
surement artifacts. We confirm full adherence to best
practices for EMG reliability. Based on previous research, we selected a fixed
cadence of 100 BPM to deliberately deviate from partici­
pants’ spontaneous pedaling rate (≈ 65–75 BPM), thereby
imposing an external rhythmic constraint that allows us
to isolate the influence of musical entrainment. In addi­
tion, 100 BPM lies within the tempo range most fre­
quently encountered in popular music (≈ 90–110 BPM),
ensuring a large and ecologically valid repertoire of tracks
for future applications [29]. Deep learning-based rhythmic music screening and
verification
The purpose of this study was to compare two types of
music with different levels of perceived groove: high-
groove music versus low-groove music. In previous stud­
ies, the assessment of groove usually relies on complex
behavioral experiments, which limits the number of avail­
able music samples. To overcome this limitation, a deep
learning model was trained in this study. The model was
trained using acoustic features and scoring data from 264
music clips provided by Janata [30], this selection is not
based on a dataset, but rather on the vocal characteris­
tics provided by Janata. For specific details, please visit ​h​t​
t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​6​0​8​4​/​m​9​.​f​i​g​s​h​a​r​e​.​3​0​2​1​7​8​4​6​.​v​1, where we
have published the full text of Janata's article. (The Janata
classification is a music research database that combines
subjective perception scores with objective acoustic fea­
tures. It contains 264 diverse music clips (each approxi­
mately 30 s long), which were rated on a scale of 1 to 7
by professional musicians and ordinary listeners based on
the dimension of “groove.” At the same time, 21 acous­
tic features, such as pulse clarity and rhythmic complex­
ity, were extracted to provide a standardized assessment
benchmark for music-movement research.) and was
able to assess the groove of any music clip and identify
key acoustic features that affect the level of groove. Spe­
cifically, the whole process is divided into three steps. First, a Temporal Convolutional Network (TCN) model
is constructed, which is used to build a dataset contain­
ing rough groove scores. Second, this dataset is uti­
lized to pre-train a Multilayer Perceptron (MLP) model
that is capable of inputting interpretable acoustic fea­
tures as independent variables. Finally, the MLP model
was fine-tuned on the original Janata dataset to achieve
the highest accuracy. The construction strategy of the
model is shown in Figs. 2 and 3. Correlation analysis of
deep learning groove scoring and behavioral experiment
scoring using tenfold cross-validation showed that the
average R2 of the groove scoring model was 0.85, which
suggests that the model's scoring accuracy is high enough
to be used for scoring instead of behavioral experiments. In addition, this study used SHAP to explore the acoustic
features that contributed the most to groove movement,
where the top 5 acoustic features all reflected elements
of the music such as beat pattern, timbre, and chords. Detailed information is shown in Fig. 4 [31]. Musical segments from the top 100 English songs on
the major music charts in December 2024 were rated
using the model. Based on the ratings, the range of rat­
ings for high-groove music was between 90 and 110 (top
25%), and the range of ratings for low-groove music was
between 30 and 50 (bottom 25%). In this study, 11 high-
groove and 11 low-groove songs were randomly selected
from the 1280 scored songs. Ten college students were
then recruited to subjectively assess the groove of these
songs on a scale of 7. Of these songs, three high-groove
songs had mean subjective groove ratings below 4.5,
and two low-groove songs had mean subjective groove
ratings above 4.5 and were therefore excluded from the
study (Table  2). Ultimately, eight high-groove and nine
low-groove songs were selected for this study. There were
significant differences in the main acoustic characteris­
tics of the songs with different groove levels (Fig. 5). The beat frequency (BPM) of all songs was uniformly
normalized to 100 BPM using Abelton Live 11 software
(Abelton AG, Berlin, Germany). The music was played
to the subjects through wireless Apple headphones (Air­
Pods Pro, Apple Inc, California, USA) at a comfortable
volume. The cycling task was initiated when the music
started playing and completed by the end of the music. The order in which the songs were played was random­
ized to minimize sequential effects. In addition, for the
beat Control group, this study used the GarageBand
application to create an auditory beat tone of 100 beats/
minute. Recognizing grooves using deep learning models
enhances the scientific validity and reproducibility of the
recognition process. First, the model recognizes as much
music as possible that is familiar to the current subject,
which can reduce potential bias due to unfamiliarity with
previous songs. Second, the model can provide impor­
tant information about the effect of acoustic features on
groove scores, thus improving understanding of groove
[31]. Traditional methods for quantifying musical rhythm
characteristics typically rely on manually extracted
acoustic features (such as beat clarity and rhythm flux) or
subjective behavioral scores. These methods have obvi­
ous limitations: first, manual feature extraction strug­
gles to fully capture the multidimensional complexity

Page 5 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
of musical rhythm perception, especially higher-order
nonlinear features (such as the interactive effects of syn­
copation patterns and dynamic compression); Second,
behavioral experiments suffer from high inter-subject
variability and are time-consuming, limiting the scale of
music sample libraries. This study employs a deep learn­
ing model based on temporal convolutional networks
(TCN) to automatically extract rhythm features most
closely related to movement-synchronized behavior from
raw audio signals through end-to-end learning. Its advan­
tages include: (1) Transfer learning using 21-dimensional
acoustic features analyzed within the Music Informa­
tion Retrieval (MIR) framework and human rating data
(R2 = 0.85), which retains the physiological significance
of acoustic features (e.g., low-frequency harmonic reso­
nance) while overcoming the sensitivity of traditional lin­
ear regression models to feature collinearity; (2) Through
SHAP value analysis of the interpretability module, the
acoustic features with the highest contribution to rhythm
perception (such as pulse clarity and spectral flux) are
identified, providing a mechanistic explanation for sub­
sequent motion-acoustic feature coupling modeling; (3)
Standardized scoring was achieved for a large sample of
contemporary popular music (N = 1280), avoiding eco­
logical validity issues caused by previous studies using
limited MIDI stimuli or outdated music libraries. This
quantitative paradigm provides a methodological foun­
dation for establishing reproducible standards for music-
movement coupling research in the field of movement
science. For more details on deep learning and music,
please refer to Appendix 1. In addition, it should be noted that: “Rhythm” (opera­
tionalized here as BPM) refers solely to the temporal
regularity and tempo of the acoustic signal, whereas
“groove” is a higher-order, multi-dimensional percept
that encompasses not only rhythm, but also syncopation,
micro-timing deviations, dynamic accents, and timbral
complexity. In other words, BPM is a necessary but not
sufficient component of groove; the same BPM can yield
high or low groove ratings depending on how these addi­
tional musical features are arranged. Consequently, the
two constructs are measured on different conceptual lev­
els—BPM on a one-dimensional tempo scale, groove on a
Fig. 2  This figure shows the construction process of the music rhythm scoring model: first, a temporal convolutional network (TCN) is used to extract pre­
liminary rhythm features from the original audio, then a multi-layer perceptron (MLP) is used to optimize these features in combination with 21 acoustic
features, and finally, the model is fine-tuned on a class scoring dataset to obtain a high-precision (R2 = 0.85) rhythm scoring model

Page 6 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
composite perceptual scale that integrates rhythmic and
supra-rhythmic elements [31]. Riding programs
The cycling task required subjects to synchronize as
closely as possible to the groove of the music. RPM refers
to the number of complete pedaling rotations com­
pleted per minute. The smaller the absolute difference
between the RPM of the ride and the BPM of the music,
the better the synchronization. 100 RPM was used as a
target pedaling frequency to help trigger a synchroniza­
tion effect in the subjects' perception of the music groove. In this study, a Lode Power bicycle (Lode BV, Gronin­
gen, Netherlands) was used for the cycling tasks (Fig. 6). Prior to the start of each task, subjects adjusted the seat
height to a standardized level (88.3% of the inner leg
length). The standardized riding protocol started with
a 3-min warm-up with a torque of 2.5 N-m and a ped­
aling frequency of 55–65 RPM. After the warm-up, a
30-s practice phase was performed. During this period, Fig. 4  Importance ranking of acoustic features based on SHAP values
Fig. 3  This figure shows the two-stage model architecture used for music rhythm scoring: (1) TCN (time-domain convolutional network) processes the
original audio through multiple layers of dilated convolutions to capture rhythm timing features; (2) MLP (multi-layer perceptron) integrates 21 acoustic
features with TCN outputs to generate the final rhythm score

Page 7 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
subjects adjusted the pedaling frequency to 100 RPM
based on the pedaling frequency displayed on the power
bike and auditory stimuli synchronized to a musical beat. After 30 s, the pedaling frequency display was hidden and
subjects completed the cycling task using only the musi­
cal groove cues. Next, subjects performed a 3-min low-
torque, medium-torque, and high-torque cycling task
in sequence, with a 3-min rest period after each 3-min
cycling task. To determine the loading conditions where
music had the greatest impact on riding performance, the
power bike was set up with a fixed torque setting, with
different torque levels regulating power and energy out­
put via RPM. Low torque was set at 7 N-m for males and
4.9 N-m for females; medium torque was set at 11 N-m
for males and 7.7 N-m for females; and high torque was
set at 15 N-m for males and 10.5 N-m for females. The
torque settings were based on the difference between
male and female lower limb strength, with females being
approximately 70% of the males. During the cycling
phase, subjects were required to maintain a pedaling fre­
quency of 100 RPM, synchronized to the groove of the
music. We presented the high-groove and low-groove con­
ditions in a fixed sequence purely for logistical con­
venience; because each participant heard completely
different songs in the two conditions, no track was ever
repeated. Consequently, learning or habituation effects
could not arise, and counter-balancing was therefore
deemed unnecessary. Measurement and calculation of joint coordination
In this study, a Qualisys motion capture system (Qualisys
AB, Gothenburg, Sweden) was used to record the trajec­
tories of the joints and cranks during the last 30 s of a
3-min cycling task under different conditions. The system
consists of eight infrared cameras with a sampling fre­
quency of 200 Hz. The experimental site was laid out as
shown in Fig. 7, with the origin of the experimental envi­
ronment in front of the right side of the power bike, the
X-axis along the long axis of the power bike, pointing in
front of the power bike from the origin, the Y-axis along
the short axis of the power bike, pointing to the right side
of the power bike from the origin, and the Z-axis per­
pendicular to the plane of the power bike, pointing to
the right side of the power bike from the origin. Z-axis is
perpendicular to the plane of the power bike and points
to the top from the origin. Twenty-five 14-mm-diameter
reflective marker points were affixed to track key areas
of the head, torso, and bilateral thighs and calves using
a biomechanical model of the bilateral lower extremities
in Anybody software (Denmark, Copenhagen). The exact
locations and abbreviated names of the marker points are
detailed in Fig. 8. In addition, one reflective marker point
was mounted on the outside of the right crank-pedal
joint to track the crank trajectory and delineate the rid­
ing cycle (Fig. 9). The reflective marker point was secured
by means of a muscle patch or a self-adhesive bandage,
with bandage wrapping limited to 3 turns to avoid exces­
sive compression of muscles and other soft tissues, which
could affect athletic performance. The kinematic data of the 25 reflective marker points
were preprocessed using Qualisys Track Manager soft­
ware, including naming, verification and repair of the tra­
jectories to ensure the completeness of the marker point
trajectories. Then, anybody 7.4 software was used to per­
form multi-link rigid body modeling and kinematic com­
putation on the preprocessed data [32]. The lower limb
model in Plug-in-gait Simple was selected to calculate the
angular time series data of the torso, pelvis, hip, knee and
ankle joints. In this case, the motions of the trunk and
pelvic segments were referenced relative to the global
coordinate system, with the motion of the trunk repre­
sented by the T10 marker point and the pelvis as its own
trajectory. Finally, peaks in the crank Z-axis trajectory
data were detected using an automatic peak detection
algorithm written in Python. Each peak corresponds to
the highest point of the pedal, and every two neighboring
peaks represent one pedal cycle. Using these time points, Table 2  Model scores and subjective scores of grooves of
experimental entry songs
Song title
Original
BPM
Rhythmic
score (from
model)
Subjective
rhythmic
score (from
scale)
Yeah

6.08 ± 1.12
Players

6.00 ± 1.16
Baby Again

5.85 ± 0.90
Area Codes

2.77 ± 1.53
Rhyme Dust

6.15 ± 0.95
Paint The Town Red

93.2
4.31 ± 1.49
Groove Thang

6.23 ± 1.30
Princess Diana

95.5
4.31 ± 1.65
Lady Love

5.69 ± 0.95
Esta Vaina

6.00 ± 1.16
TGIF

5.95 ± 0.90
Yes I Am

40.2
1.77 ± 1.36
I Can Love Anyone

35.3
2.77 ± 1.48
Kryptonite

40.5
2.38 ± 1.21
I'll Be Waiting

36.7
2.00 ± 1.47
Try That In A Small Town

45.6
2.46 ± 1.45
Golden Hour

39.6
2.08 ± 1.39
Heading South

47.1
5.15 ± 1.56

### 7 Summers

47.5
2.38 ± 1.32
Everything I Love

44.5
5.38 ± 1.61
Don't Understand

37.5
2.62 ± 0.99
Feathered Indians

47.4
2.23 ± 1.64
Note BPM: beats per minute

Page 8 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
Fig. 5 (See legend on next page.)

Page 9 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
the continuously recorded angle data was split into indi­
vidual cycle data. The vector coding technique was used to calculate
the coupling angle and coordination between the lower
limb joints, trunk, and pelvic segments. The angle-angle
diagram was utilized to construct the angle relation­
ship between any two segments in the time series, and
the coupling angle was calculated by the vector of two
consecutive time points [33]. The coupling angle is the
angle of this vector with respect to the horizontal line
and ranges from 0° to 360° (Fig. 10A). Depending on the
coupling angle, the coordination modes are classified into
four types: in-phase coordination (22.5°–67.5° or 202.5°–
247.5°), which indicates that the two segments rotate
synchronously in the same direction; anti-phase coordi­
nation (112.5°–157.5° or 292.5°–337.5°), which indicates
that the two segments rotate in the opposite direction;
proximal phase coordination (157.5°–202.5° or 337.5°–
360°), indicating that motion occurs predominantly in the
proximal segment; and distal phase coordination (67.5°–
112.5° or 247.5°–292.5°), indicating that motion occurs
predominantly in the distal segment (Fig.  10B). This
study focused on exploring joint coordination between
the hip-knee, hip-ankle, and knee-ankle joints in the sag­
ittal plane of the lower extremity, as well as between the
pelvis-trunk in the vertical plane. Vector Coding Technique (VCT) is a kinematic-based
joint coordination analysis method that evaluates move­
ment coordination patterns by quantifying the spatio­
temporal relationships between adjacent joint angle
changes [34]. This method converts the angular changes
of two joints into vectors and calculates their phase
relationships to identify specific coordination patterns,
such as in-phase, anti-phase, proximal-dominant, and
distal-dominant movements. Compared to traditional
angle-angle plots or relative phase analysis, vector coding
technique can more intuitively reveal the dynamic cou­
pling characteristics between joints, particularly suitable
for studying coordination in periodic movements such
as cycling or gait [35]. In this study, the technique was
applied to analyze coordination patterns between hip-
ankle, knee-ankle, and pelvis-trunk joints to investigate
the effects of different rhythmic music on joint coordina­
tion strategies. Acquisition and processing of EMG data
In this study, a Delsys wireless surface EMG system (Del­
sys Inc., Boston, USA; electrode spacing 1 cm) was used
to collect surface electromyography (EMG) data from 12
muscles of the right limb during the last 30 s of a 3-min
cycling task under different conditions. The system was
sampled at a frequency of 1 kHz and synchronized with
a Qualisys system. The 12 muscles included: tibialis ante­
rior (TA), medial gastrocnemius (GM), lateral gastrocne­
mius (GL), soleus (SOL), vastus medialis femoris (VM),
vastus lateralis (VL), rectus femoris (RF), biceps femoris
(BF), semitendinosus (ST), and gluteus maximus (GMX).
rectus abdominis (RA), erector spinae (ES). In the present study, only muscle synergy differences
between the low groove music condition and the high
torque riding in the high groove music condition were
analyzed. This is partly because muscle synergy can
explain the mechanisms by which musical groove affects
riding performance. The metronome condition served
as a control, which is inherently different from musical
groove, and therefore its unsuitable for direct compari­
son with the musical condition. On the other hand, by
comparing the effects of musical groove on riding joint
coordination at different torques, low, medium and high,
the study clarified that the loading condition with the
greatest effect of musical groove on riding performance
was high-torque riding. This provides a basis for explor­
ing the mechanisms of musical groove on cycling perfor­
mance using high-torque cycling loads. The EMG signals were preprocessed and analyzed
using the muscle synergies v1.2.5 package (Santuz, 2022)
in R software (version 4.2.0, R Foundation for Statisti­
cal Computing, Vienna, Austria). Removal of averag­
ing, bandpass filtering (4th order Butterworth 20–400
Hz) and full-wave rectification were first performed to
remove low-frequency motion artifacts. Smoothing was
performed by low-pass filtering with a cutoff frequency
of 20 Hz. Then the root-mean-square amplitude was cal­
culated by moving with a time window width of 20 MS
and a window overlap width of 10 MS to obtain the enve­
lope of the EMG data. Finally, the amplitude was normal­
ized according to the maximum value for each subject;
and the envelope data were time normalized and interpo­
lated to 200 data points [36]. Calculation of muscle synergy patterns
Muscle synergies were extracted from preprocessed EMG
data by a non-negative matrix factorization (NMF) algo­
rithm. The algorithm decomposes muscle activity (D(t))
into a linear combination of time-invariant synergy vec­
tors (Wi) scaled by time-varying activation coefficients
(See figure on previous page.)
Fig. 5  Comparison of acoustic features between music with different groove levels. Note: The acoustic feature comparison between high- and low-
groove music was conducted using independent samples t-tests (for normally distributed data) or Mann–Whitney U tests (for non-normal distributions),
with significance set at p < 0.05. Effect sizes were calculated using Cohen's d (for t-tests) or rank-biserial correlation (for non-parametric tests). The top
5 features contributing to groove perception were selected based on SHAP (SHapley Additive Planations) values from our deep learning model, which
quantifies each feature's importance in predicting groove ratings. All statistical analyses were performed using Python (SciPy library) and R software

Page 10 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
Fig. 6  Power bicycles used in the cycling program

Page 11 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
(Ci(t)) using a set of iterative multiplicative updating
rules [37]. The EMG signals can be reconstructed by the
following equation: D (t) =
∑Nsyn
i=1 Ci (t) Wi
(1)
Variability Accounted For (VAF) is commonly used to
test the degree of reconstruction of the reconstructed
matrix with respect to the original matrix and to deter­
mine the optimal number of muscle synergies (Nsyn). i
was taken sequentially from 1 to 12, as 12 muscles were
recorded simultaneously in the experiment. The value of
i corresponding to an initial VAF greater than 90% was
chosen as the optimal number of muscle synergies per
subject per experiment, and the current W and C were
used as the final synergy outputs [38]. The VAF was cal­
culated using the following formula:

## V AF = 1 −SSE

SST

## SST = ∑

i,j (Dij −mDi)2, SSE = ∑
i,j (Dij −[WC]ij)2  (2)
where SST is the total sum of squares and SSE is the sum
of error squares, Dij is the EMG data of the ith muscle at
the jth time point, mDi is the average EMG value of the
ith muscle, [WC]ij is the reconstructed EMG signal. To characterize muscle synergy vector differences
between groups, representative synergy vectors for each
group were first identified by k-means clustering. The
squared Euclidean metric was used, and each cluster­
ing was repeated 1000 times to select the result with the
smallest sum of point-to-center-of-mass distances [39]. The number of synergistic clusters in each group was
determined by calculating the Gap statistic, which is used
to measure the difference in clustering compactness rela­
tive to a reference dataset with no significant clustering. Gap(k) ≥Gap(k + 1) −sd(k + 1)
(3)
where Gap(k) is the gap statistic at k clusters, sd(k) is
the standard deviation of the clustering compactness in
the reference dataset. Fig. 7  Laboratory site setup

Page 12 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
In order to compare the muscle synergistic patterns
between the high-groove condition and the low-groove
condition, the condition with the higher number of syn­
ergistic patterns after clustering was chosen as the refer­
ence synergistic pattern in this study. For example, if the
high-groove condition formed five representative syn­
ergy patterns after clustering and the low-groove condi­
tion formed four representative synergy patterns, the
clustered synergy patterns of the high-groove condition
were chosen as the reference. In the low-groove condi­
tion, the synergistic patterns of the low-groove condition
were classified into the corresponding reference synergis­
tic pattern categories based on the correlation between
their muscle weights and the muscle weights of the refer­
ence synergistic patterns [40]. The threshold value of the
correlation coefficient was 0.6, and when the correlation
coefficient was greater than 0.6, the synergistic pattern
could be considered to belong to the corresponding ref­
erence synergistic pattern. In this study, the optimal number of muscle synergies,
reference synergy patterns, muscle weights, and muscle
activation durations were analyzed. According to the
Fig. 8  Subject reflective marker points locations based on Anybody 7.4 lower extremity model specification

Page 13 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
Fig. 10  A calculation of coupling angle, B Classification of coordination modes
Fig. 9  This figure illustrates the crank motion trajectory tracking method used in the experiment to determine the cycling cycle. By installing reflective
markers (indicated by red arrows) on the outer side of the right pedal and combining them with a motion capture system to record its three-dimensional
motion trajectory, each cycling cycle can be accurately divided (each pair of adjacent peaks represents a complete pedal cycle). This method provides an
accurate time reference for subsequent joint angle and muscle coordination analysis

Page 14 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
research convention, only the activation durations in the
part of the activation curve where (Ci(t)) is greater than
0.3 are counted. For more details, please refer to Appendix 2. Statistical analysis
Data were analyzed using SPSS 26.0 software (SPSS Inc., Chicago, IL, USA). Outliers were screened using box-
and-line plots, and normality was tested by the Shapiro–
Wilk test [41]. Data that conformed to normal distribution were sub­
jected to descriptive statistics using mean ± standard
deviation, and one-way repeated measures analysis of
variance (ANOVA) was used to compare the differences
in joint coordination data among the three conditions of
MT, LG, and HG. The Greenhouse–Geisser method was
used to adjust the F-value when the sphericity assump­
tion was not valid. The Bonferroni method was used for
two-by-two comparisons. Effect sizes were evaluated
using η2p. Paired-samples t-tests were used to compare
differences in EMG data between LG and HG condi­
tions. Effect sizes were evaluated using d. Data that did
not fit the normal distribution were analyzed using the
median (interquartile range) for descriptive statistics, and
the Friedman test was used to compare the differences
in joint coordination data between the MT, LG, and HG
conditions. Two-by-two comparisons were made using
the all-pairs method. The Wilcoxon signed rank test was
used to compare differences in EMG data between the
LG and HG conditions. In addition, in the analysis of joint coordination data,
the three riding tasks were analyzed independently
because the low-torque, medium-torque, and high-
torque riding tasks were relatively independent and in a
fixed order. p < 0.05 was considered statistically signifi­
cant for the differences. Results
Comparison of joint coordination in riding to music at
different groove levels
The results in Table 3 show that the differences in hip-
ankle same phase coordination across music conditions
during high-torque riding were statistically significant
(F = 17.09; p < 0.001; η2p = 0.43). Two-by-two compari­
sons showed that hip-ankle same phase coordination was
significantly higher in HG and LG than in MT (p < 0.001;
p = 0.040) and also significantly higher in HG than in
LG (p = 0.020). Differences in pelvic-trunk same phase
coordination in the vertical plane across music condi­
tions were statistically significant (F = 4.95; p = 0.011;
η2p = 0.17), and HG had significantly higher pelvic-trunk
same phase coordination than LG and MT (p = 0.048;
p = 0.041). Differences in hip-knee and knee-ankle
Table 3  Comparison of joint coordination in high-torque riding
with different groove levels of music
High
torque
riding
Same phase
Reversed
phase
Phase of
the hip
joint
Phase of
the knee
joint
Hip-Knee
Con­
trol
group
MT
44.65 ± 14.57
10.06 ± 3.94
4.7 ± 2.47
40.59 ± 16.38
Music
group
LG
45.96 ± 15.80
9.30 ± 6.29
4.08 ± 2.34
40.66 ± 16.28
HG
47.61 ± 11.49
7.18 ± 4.44
4.63 ± 3.01
40.58 ± 13.01
F
0.26
2.16
0.41
0.00
P
0.773
0.127
0.67
1.00
η2p
0.01
0.09
0.02
0.00
Hip-Ankle
Con­
trol
group
MT
16.49 ± 6.99
20.73 ± 7.28
44.04 ± 11.45
18.75 ± 5.36
Music
group
LG
23.16 ± 7.72a
19.26 ± 7.79
40.23 ± 7.72
17.34 ± 9.03
HG
29.79 ± 6.62ab
16.58 ± 4.67
39.06 ± 6.49
14.57 ± 5.88
F
17.09
2.02
2.46
2.52
P
< 0.001
0.144
0.097
0.092
η2p
0.43
0.81
0.97
0.99
Knee-Ankle
Con­
trol
group
MT
3.05 ± 1.67
12.82 ± 4.91
81.17 ± 5.16
2.95 ± 1.75
Music
group
LG
2.39 ± 1.78
13.86 ± 5.09
79.96 ± 6.32
3.80 ± 1.91
HG
3.50 ± 1.59
16.81 ± 6.53
76.64 ± 8.35
3.05 ± 2.60
F
2.82
3.01
2.68
1.03
P
0.070
0.059
0.079
0.366
η2p
0.11
0.16
0.10
0.04
Pelvis-Torso vertical plane
Con­
trol
group
MT
30.13 ± 9.11
17.21 ± 6.68
27.99 ± 11.57
24.67 ± 9.44
Music
group
LG
29.93 ± 8.70
15.35 ± 5.91
27.23 ± 10.35
27.49 ± 11.71
HG
38.01 ± 10.29ab
14.52 ± 7.36
24.45 ± 10.71
23.02 ± 10.55
F
4.95
0.89
0.65
0.903
P
0.011
0.414
0.522
0.413
η2p
0.17
0.03
0.02
0.04
Note MT: metronome; LG: low-groove music; HG: high-groove music. a Indicates
a statistically significant difference from the control condition. b Indicates a
statistically significant difference from the low-groove condition. c Indicates
a statistically significant difference from the control condition. d Indicates
a statistically significant difference from the control condition. e Indicates a
statistically significant difference from the control condition. Higher same-phase
percentages typically indicate greater hip–knee synchrony during propulsive
phases, yet optimal coordination patterns vary with task demands and are not
universally dichotomized as ‘high’ or ‘low. “Same phase” and “Reversed phase”
report the percentage of gait cycles in which the hip–knee angle–angle plot
fell into an in-phase or anti-phase coordination pattern, respectively. “Phase
of the hip joint” and “Phase of the knee joint” denote the relative phase state
of the proximal and distal joints; in the present cycling task, “Phase of the hip
joint” corresponds to the proximal crank phase and “Phase of the knee joint”
corresponds to the distal crank phase. Each cell gives the proportion (%) of the
trial spent in that specific coordination state. (The following are the same.)

Page 15 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
coordination between music conditions were not statisti­
cally significant (p > 0.05). Differences in hip-knee, hip-ankle, knee-ankle, and pel­
vic-trunk vertical plane coordination across music con­
ditions were not statistically significant (P > 0.05) during
low-torque and medium-torque riding. Detailed data are
shown in Tables 4 and 5. Comparison of synergistic patterns of riding muscles under
different groove levels of music
The results in Table 6 show that the difference in the total
number of muscle synergistic patterns between LG and
HG was statistically significant (Z = − 2.06; P = 0.039),
with HG having more than LG. Table 7 describes the spe­
cific number of muscle synergistic patterns in subjects in
the LG versus HG condition. Table 4  Comparison of joint coordination in low-torque riding
with different groove levels of music
Low torque
riding
Same phase
Reversed
phase
Phase of the
hip joint
Phase of
the knee
joint
Hip-Knee
Con­
trol
group
MT
38.88 ± 11.43
7.78 ± 4.51
4.17 ± 1.47
49.17 ± 14.5
Music
group
LG
39.98 ± 13.98
7.92 ± 3.70
4.81 ± 2.06
47.28 ± 15.43
HG
41.95 ± 15.96
9.39 ± 4.19
4.68 ± 2.43
43.97 ± 17.38
F
0.28
1.39
0.61
0.65
P
0.754
0.272
0.546
0.526
η2p
0.01
0.06
0.03
0.03
Hip-Ankle
Con­
trol
group
MT
26.78 ± 8.07
15.01 ± 3.33
42.33 ± 8.38
15.88 ± 8.68
Music
group
LG
29.64 ± 11.29
14.94 ± 4.87
41.76 ± 7.77
13.65 ± 6.83
HG
29.1 ± 9.81
15.35 ± 3.68
40.72 ± 6.29
14.83 ± 6.28
F
0.51
0.05
0.27
0.55
P
0.599
0.943
0.758
0.579
η2p
0.02
0.01
0.01
0.02
Knee-Ankle
Con­
trol
group
MT
3.28 ± 2.49
15.63 ± 8.26
78.17 ± 8.72
2.93 ± 1.94
Music
group
LG
2.56 ± 1.99
13.89 ± 7.08
79.62 ± 9.79
3.92 ± 2.55
HG
3.13 ± 2.89
14.21 ± 5.89
79.48 ± 8.24
3.17 ± 2.40
F
0.66
0.38
0.17
1.11
P
0.52
0.68
0.839
0.336
η2p
0.02
0.01
0.01
0.05
Pelvis-Torso vertical plane
Con­
trol
group
MT
31.69 ± 10.39
17.08 ± 8.18
27.08 ± 11.95
24.15 ± 10.07
Music
group
LG
27.87 ± 11.33
18.63 ± 6.87
30.74 ± 14.09
22.76 ± 10.95
HG
33.1 ± 9.98
17.72 ± 5.95
25.26 ± 8.87
23.92 ± 7.22
F
1.51
0.26
1.30
0.15
P
0.231
0.767
0.281
0.861
η2p
0.06
0.01
0.05
0.01
Note MT: metronome; LG: low-groove music; HG: high-groove music. a Indicates
a statistically significant difference from the control condition. b Indicates a
statistically significant difference from the low-groove condition. c Indicates
a statistically significant difference from the control condition. d Indicates
a statistically significant difference from the control condition. e Indicates a
statistically significant difference from the control condition. Higher same-
phase percentages typically indicate greater hip–knee synchrony during
propulsive phases, yet optimal coordination patterns vary with task demands
and are not universally dichotomized as ‘high’ or ‘low’
Table 5  Comparison of joint coordination in medium torque
riding with different groove levels of music
Middle
torque
riding
Same phase
Reversed
phase
Phase of the
hip joint
Phase of
the knee
joint
Hip-Knee
Con­
trol
group
MT
45.3 ± 10.20
8.9 ± 3.24
4.58 ± 2.71
41.21 ± 11.66
Music
group
LG
39.38 ± 8.76
7.94 ± 4.72
3.88 ± 2.31
48.8 ± 11.04
HG
46.22 ± 16.24
8.94 ± 4.78
5.1 ± 2.78
39.75 ± 14.34
F
1.97
0.40
1.10
3.15
P
0.150
0.666
0.339
0.052
η2p
0.07
0.01
0.04
0.12
Hip-Ankle
Con­
trol
group
MT
25.73 ± 10.66
15.88 ± 3.45
44.53 ± 8.73
13.85 ± 7.99
Music
group
LG
29.71 ± 7.03
14.89 ± 4.91
39.77 ± 6.92
15.63 ± 6.12
HG
27.31 ± 8.53
15.16 ± 4.69
41.47 ± 10.51
16.06 ± 6.57
F
1.14
0.36
1.57
0.54
P
0.330
0.699
0.219
0.589
η2p
0.05
0.02
0.06
0.02
Knee-Ankle
Con­
trol
group
MT
3.42 ± 2.02
12.17 ± 6.78
81.04 ± 7.72
3.37 ± 1.87
Music
group
LG
2.28 ± 1.63
13.54 ± 6.03
80.81 ± 6.86
3.36 ± 1.24
HG
2.81 ± 1.89
15.58 ± 8.74
77.83 ± 10.69
3.78 ± 2.59
F
2.12
1.27
0.93
0.31
P
0.131
0.29
0.402
0.735
η2p
0.08
0.05
0.04
0.01
Pelvis-Torso vertical plane
Con­
trol
group
MT
33.36 ± 11.44
17.57 ± 8.97
30.16 ± 12.11
18.92 ± 11.89
Music
group
LG
31.86 ± 9.23
15.5 ± 5.59
29.9 ± 9.53
22.74 ± 9.45
HG
33.71 ± 7.17
15.74 ± 5.46
27.6 ± 9.32
22.95 ± 8.65
F
0.27
0.70
0.40
1.18
P
0.761
0.501
0.622
0.316
η2p
0.01
0.03
0.02
0.04
Note MT: metronome; LG: low-groove music; HG: high-groove music. a Indicates
a statistically significant difference from the control condition. b Indicates a
statistically significant difference from the low-groove condition. c Indicates
a statistically significant difference from the control condition. d Indicates
a statistically significant difference from the control condition. e Indicates a
statistically significant difference from the control condition. Higher same-
phase percentages typically indicate greater hip–knee synchrony during
propulsive phases, yet optimal coordination patterns vary with task demands
and are not universally dichotomized as ‘high’ or ‘low’

Page 16 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
In this study, the muscle synergy patterns in the low-
groove and high-groove conditions were clustered and
analyzed separately. The results are shown in Fig.  11,
where representative muscle synergy patterns (SYN) in
the low-groove condition were categorized into 4 classes,
while representative SYN in the high-groove condition
were categorized into 5 classes. Therefore, the represen­
tative muscle synergy patterns in the high groove con­
dition were selected as the reference synergy patterns. A comparison of the number of people who appeared
in the reference muscle synergy pattern under different
groove levels of music is detailed in Table 8. More people
appeared in the reference muscle synergy pattern in the
HG condition. Table 9 shows that for SYN2, the difference in SOL
muscle weights across music was statistically signifi­
cant, with HG significantly greater than LG (Z = − 2.17;
p = 0.030). For SYN5, there was a synergistic pattern for
HG, whereas there was no corresponding categorization
of synergistic patterns for LG. Further analysis showed
that HG had muscle weights greater than 0.3 for GL and
ES in SYN5. For SYN1, SYN3, and SYN4, the difference
in muscle weights across music was not statistically sig­
nificant (P > 0.05). Table 10 shows that for SYN1-4, the
differences in muscle activation times across music were
not statistically significant (p > 0.05). Discussion
Neuro-biomechanical regulatory mechanisms of musical
groove on joint coordination in high-load cycling
Joint coordination is one of the most important factors
affecting cycling performance [42], especially during
high-intensity exercise where the synergy of different
joints is crucial. In this study, the effect of music on joint
coordination was found to be equally prominent in high-
torque conditions, especially hip-ankle and pelvic-trunk
in-phase coordination, which are two coordination
modes that are important for overcoming high torque
and generating higher work output. During high-torque
riding, hip-ankle in-phase coordination was significantly
higher in the HG and LG music conditions than in the
MT condition, and the LG coordination was also signifi­
cantly better than that of MT. This suggests that music
helps riders to achieve better hip-ankle synergy under
high load conditions, ensuring effective force transfer and
thus improving exercise performance. Meanwhile, the
effect of high-groove music in improving hip-ankle and
pelvic-trunk Anti-phase coordination was significant. The results showed that the pelvic-trunk homoplastic
coordination was significantly higher in the HG than in
the LG and MT, suggesting that under high-torque con­
ditions, high-groove music can significantly improve the
coordination of the rider's upper- and lower-body move­
ments, maintain the overall stability of the movements,
and thus effectively cope with high-load cycling tasks. Joint coordination plays an important role in athletic
performance [43]. This neuromodulation optimizes the
matching of extensor-flexor activation timing, shortens
the time difference between peak hip flexion and peak
ankle plantarflexion, significantly improves the efficiency
of torque transmission, and also enhances the smooth­
ness and groove of movement and reduces unnecessary
energy consumption [44]. And music, especially high-
groove music, significantly improves cyclists' exercise
performance under high-load conditions by enhancing
the coordination of these key areas. Effects of musical groove on muscle synergy patterns in
cycling
Muscle synergistic reorganization induced by high-
groove music reveals adaptive strategies of the nervous
system to cope with motor complexity. The results of
Table 6  Comparison of the number of synergistic patterns of
riding to music at different groove levels
LG
HG
Z
P
Number of muscle
synergy patterns
6.00 (2.00)
7.00 (1.00)
− 2.06
0.039
Note LG: low groove music; HG: high groove music. Data are expressed as
median (interquartile range)
Table 7  Number of muscle synergy patterns in subjects
Participants number
LG
HG

Subtotal

Note HG: high groove music; LG: low groove music

Page 17 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
the present study showed that high-groove music sig­
nificantly altered muscle synergy patterns, increasing the
number of synergistic elements and reorganizing activa­
tion strategies. Specifically, the total number of muscle
synergy patterns was greater in the HG condition than
in the LG condition, with more subjects exhibiting refer­
ence synergy patterns in HG. The synergy patterns under HG music were character­
ized by enhanced coordination between trunk and calf
muscles, particularly between the erector ES and the calf
triceps (GM and GL). Additionally, the high-groove con­
dition significantly increased the contribution of the SOL
muscle in SYN2, which may improve ankle stabilization
through prolonged activation of type I muscle fibers and
better synchronization with the musical beat [45]. The identified muscle synergies served distinct func­
tional roles in cycling movement: SYN1 primarily coordi­
nated the GM and GL to generate propulsive force during
the downstroke phase; SYN2 involved the SOL for ankle
stabilization and fine force modulation during pedal
transitions; SYN3 integrated the VL and VM with RF to
control knee extension and hip flexion; SYN4 combined
ES with GMAX to maintain postural stability; while
the unique SYN5 in HG condition linked ES with GL to
enhance power transfer through the kinetic chain. This
functional specialization suggests that high-groove music
promotes more refined neuromuscular control strategies. The increased number of muscle synergies observed
under high-groove music may reflect the nervous sys­
tem's adaptive response to rhythmic auditory cues. According to dynamic systems theory, the stable tempo­
ral structure provided by high-groove music likely serves
as an external attractor, enabling the decomposition of
global muscle activation into more specialized modules. This neural fractionation strategy allows for finer con­
trol of movement components while maintaining over­
all coordination. Additionally, the rhythmic entrainment
may have reduced the neuromuscular system's degrees
of freedom, facilitating the emergence of additional syn­
ergies to meet the higher coordinative demands of syn­
chronized cycling. These findings suggest that high-groove music facili­
tates neuromuscular coordination, promoting more
effective force transfer through the pelvis [46]. The ES
muscle plays a key role in stabilizing the body during
exercise [47], while the activation of the calf triceps helps
enhance power output [48]. The improved coordination
between these muscle groups under high-groove music
may promote more efficient movement patterns and
Table 8  Comparison of the number of people who refer to
muscle synergy patterns that occur with different groove levels
of music
Reference muscle synergy model
LG
HG

## SYN 1

## SYN 2

## SYN 3

## SYN 4

## SYN 5

Total number of persons

Unrecognized synergistic patterns

Note SYN: muscle synergy mode. HG: high groove music; LG: low groove music
Fig. 11  Comparison of clustering results of muscle synergy patterns for riding with music at different groove levels. tibialis anterior (TA), medial gastroc­
nemius (GM), lateral gastrocnemius (GL), soleus (SOL), vastus medialis femoris (VM), vastus lateralis (VL), rectus femoris (RF), biceps femoris (BF), semiten­
dinosus (ST), and gluteus maximus (GMX). Rectus abdominis (RA), erector spinae (ES). The vertical bar graphs depict synergy vectors (muscle-weighting
coefficients), whereas the overlaid waveforms show the corresponding activation coefficients across the gait cycle. The small circles on the bars mark
muscles with weightings ≥ 0.30, indicating a dominant contribution to that synergy. Because all pedaling cycles were time-normalized to 200 data points
(0–100% cycle), the x-axis of the activation waveforms is labelled “Cycle (%)” rather than absolute time. Each data point therefore corresponds to a percent­
age of the average cycle duration (~ 500 MS in this study)

Page 18 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
smoother force transmission during cycling. Thus, high-
groove music appears to optimize neuromuscular con­
trol by refining muscle activation timing and enhancing
intermuscular coordination. These results support the
potential use of groove-based auditory cues in training
programs aimed at improving movement coordination in
cyclic tasks. Limitations of the study
First, the small sample size and the fact that all par­
ticipants were healthy college students limit the gen­
eralizability of the results to broader populations (e.g.,
professional athletes or clinical patients). Second, the
Table 9  Comparison of the distribution of weights of each muscle in the synergistic pattern of riding with different groove levels of
music
Muscle weight
distribution
Synergy
LG
HG
Muscle weight
distribution
Synergy
LG
HG
TA
S
Y
N

0.02 (0.00, 0.11)
0.06 (0.03, 0.14)
TA
S
Y
N

0.56 (0.23, 0.89)
0.58 (0.23, 0.94)
GM
0.45 (0.27, 0.63)
0.57 (0.44, 0.70)
GM
0.01 (0.00, 0.03)
0.00 (0.00, 0.00)
GL
0.26 (0.18, 0.34)
0.26 (0.13, 0.45)
GL
0.01 (0.00, 0.03)
0.02 (0.01, 0.04)
SOL
0.17 (0.03, 0.31)
0.13 (0.05, 0.26)
SOL
0.04 (0.00, 0.14)
0.11 (0.00, 0.30)
VM
0.00 (0.00, 0.07)
0.01 (0.00, 0.05)
VM
0.10 (0.00, 0.21)
0.27 (0.06, 0.49)
VL
0.01 (0.00, 0.04)
0.06 (0.00, 0.14)
VL
0.20 (0.06, 0.35)
0.19 (0.09, 0.30)
RF
0.04 (0.02, 0.10)
0.04 (0.02, 0.08)
RF
0.17 (0.04, 0.30)
0.24 (0.14, 0.35)
BF
0.20 (0.10, 0.35)
0.07 (0.00, 0.19)
BF
0.09 (0.00, 0.28)
0.04 (0.00, 0.08)
ST
0.30 (0.20, 0.40)
0.27 (0.20, 0.40)
ST
0.09 (0.00, 0.31)
0.15 (0.03, 0.27)
GMAX
0.03 (0.02, 0.05)
0.05 (0.03, 0.13)
GMAX
0.14 (0.06, 0.22)
0.12 (0.00, 0.32)
RA
0.12 (0.06, 0.23)
0.12 (0.05, 0.24)
RA
0.07 (0.01, 0.13)
0.19 (0.08, 0.31)
ES
0.42 (0.21, 0.60)
0.33 (0.25, 0.56)
ES
0.06 (0.02, 0.11)
0.06 (0.00, 0.17)
TA
S
Y
N

0.06 (− 0.05, 0.17)
0.07 (− 0.05, 0.19)
TA
S
Y
N

0.06 (− 0.05, 0.17)
0.07 (− 0.05, 0.19)
GM
0.01 (− 0.03, 0.04)
0.03 (− 0.03, 0.08)
GM
0.01 (− 0.03, 0.04)
0.03 (− 0.03, 0.08)
GL
0.05 (− 0.01, 0.11)
0.06 (− 0.01, 0.13)
GL
0.05 (− 0.01, 0.11)
0.06 (− 0.01, 0.13)
SOL
0.05 (− 0.05, 0.14)
0.09 (0.04, 0.15)
SOL
0.05 (− 0.05, 0.14)
0.09 (0.04, 0.15)
VM
0.01 (− 0.02, 0.03)
0.01 (− 0.06, 0.08)
VM
0.01 (− 0.02, 0.03)
0.01 (− 0.06, 0.08)
VL
0.05 (− 0.07, 0.17)
0.09 (− 0.02, 0.19)
VL
0.05 (− 0.07, 0.17)
0.09 (− 0.02, 0.19)
RF
0.04 (0.02, 0.06)
0.05 (0.00, 0.11)
RF
0.04 (0.02, 0.06)
0.05 (0.00, 0.11)
BF
0.06 (0.02, 0.11)
0.03 (− 0.02, 0.07)
BF
0.06 (0.02, 0.11)
0.03 (− 0.02, 0.07)
ST
0.13 (− 0.15, 0.40)
0.30 (0.03, 0.58)
ST
0.13 (− 0.15, 0.40)
0.30 (0.03, 0.58)
GMAX
0.11 (0.06, 0.17)
0.07 (0.00, 0.15)
GMAX
0.11 (0.06, 0.17)
0.07 (0.00, 0.15)
RA
0.39 (0.21, 0.58)
0.24 (− 0.04, 0.52)
RA
0.39 (0.21, 0.58)
0.24 (− 0.04, 0.52)
ES
0.24 (0.03, 0.46)
0.13 (− 0.09, 0.34)
ES
0.24 (0.03, 0.46)
0.13 (− 0.09, 0.34)
TA
N/A
0.00 (− 0.02, 0.02)
GM
N/A
0.06 (0.00, 0.12)
GL
N/A
0.53 (0.26, 0.81)
SOL
N/A
0.05 (− 0.09, 0.19)
VM
S
N/A
0.06 (0.03, 0.09)
VL
Y
N/A
0.09 (0.01, 0.17)
RF
N
N/A
0.05 (0.00, 0.10)
BF

N/A
0.23 (0.12, 0.35)
ST
N/A
0.19 (0.04, 0.35)
GMAX
N/A
0.17 (0.02, 0.32)
RA
N/A
0.06 (0.00, 0.13)
ES
N/A
0.57 (0.35, 0.80)
Note SYN: muscle synergy pattern. LG: low groove music; HG: high groove music. Data are expressed as median (interquartile distance)
Table 10  Comparison of activation times of each synergistic
mode under different music rides
Activation time (count)
LG
HG
Z
P
SYN1
59.00 (29.75)
62.00 (27.75)
− 1.17 0.241
SYN2
59.00 (28.75)
55.00 (24.75)
− 0.90 0.368
SYN3
108.00 (45.00)
119.0 (37.75)
− 1.86 0.063
SYN4
52.00 (32.50)
56.00 (40.00)
− 1.29 0.198
SYN5
N/A
77.00 (35.75)
N/A
N/A
Note SYN: muscle synergy mode. LG: low groove music; HG: high groove music. The medians are all integers because the times are all normalized to 200 data
points (count). Data are expressed as median (interquartile distance). shows
that for SYN1-4, the differences in muscle activation times across music were
not statistically significant (p > 0.05)

Page 19 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233
experiment only assessed the short-term effects of music
intervention and did not reveal potential long-term neu­
ral adaptations or performance changes that may result
from prolonged training. Additionally, participants'
familiarity with and personal preferences for the selected
music may have influenced rhythm perception and motor
synchronization, but these factors were not controlled
for as variables. Finally, the study did not systematically
monitor potential confounding factors such as psycho­
logical states (e.g., motivation, fatigue levels), which
may indirectly influence motor performance through
attention or effort levels. Future research could further
validate the robustness of these findings by expanding
sample diversity, extending the intervention period, and
incorporating psychological assessments. In addition,
direct performance indicators and metabolic parameters
such as VO₂ and heart rate were not included. The mea­
surement of these physiological indicators will help to
more comprehensively evaluate the effectiveness of exer­
cise performance optimization, which will be an impor­
tant direction for future research. Conclusion
This study demonstrates that high-groove music
enhances neuromuscular coordination during high-
torque cycling by optimizing joint coordination patterns
and muscle synergy organization. The improved hip-
ankle and pelvis-trunk coordination, coupled with the
emergence of additional muscle synergies under high-
groove conditions, suggests that rhythmic auditory cues
facilitate more refined motor control strategies. These
findings support the use of groove-based music in cycling
training to promote coordinated movement patterns,
though the specific mechanisms underlying these adap­
tations require further investigation with direct perfor­
mance measurements. Supplementary Information
The online version contains supplementary material available at ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​
g​/​1​0​.​1​1​8​6​/​s​1​2​9​8​4​-​0​2​5​-​0​1​7​7​8​-​7. Supplementary Material 1. Supplementary Material 2. Acknowledgements
Not applicable. Author contributions
All authors were involved in the experimental design and writing the
manuscript for this study. Funding
This research was supported by the Open Project Fund of the Provincial-
Ministerial Jointly-Built Key Laboratory of Sports Science and Technology at
Shanghai University of Sport, as well as the 2025 Shanghai University of Sport
Graduate Student Research Innovation Program (Study on the Combined
Effects of rTMS and Traditional Chinese Mind-Body Exercises in Remodeling
Cognitive-Emotional Disorders, Muscle Coordination, and Brain Functional
Connectivity in Sarcopenic Patients). Availability of data and material
Data is provided within the manuscript or supplementary information files. Declarations
Ethics approval and consent to participate
The study protocol followed the ethical principles of the Declaration of
Helsinki and was approved by the Ethics Committee of Beijing Normal
University (approval number: ICBIR_B_0213_001). All participants signed an
informed consent form agreeing to participate in this study. Consent for publication
All participants and authors agreed to publish all aspects of this study. Competing interests
The authors declare no competing interests. Author details
1School of Exercise and Health, Shanghai University of Sport, Shanghai, China
Received: 3 April 2025 / Accepted: 12 October 2025

### 6. References

1. Timmers R, Macritchie J, Schabrun SM, et al. Neural multimodal integration
underlying synchronization with a co-performer in music: influences of
motor expertise and visual information. Neurosci Lett. 2020;721:134803.
2. Proost M, Habay J, de Wachter J, et al. How to tackle mental fatigue: a system­
atic review of potential countermeasures and their underlying mechanisms. Sports Med. 2022;52(9):2129–58.
3. Stanton TR, Spence C. The influence of auditory cues on bodily and move­
ment perception. Front Psychol. 2020;10(3001).
4. Snyder JS, Gordon RL, Hannon EE. Theoretical and empirical advances
in understanding musical groove, beat and metre. Nat Rev Psychol.
2024;3(7):449–62.
5. Levitin DJ, Grahn JA, London J. The psychology of music: rhythm and move­
ment. Annu Rev Psychol. 2018;69(1):51–75.
6. Brittain JS, Brown P. Oscillations and the basal ganglia: motor control and
beyond. Neuroimage. 2014;85 Pt 2(Pt 2):637–47.
7. Karageorghis CI, Priest D, Williams L, et al. Ergogenic and psychological
effects of synchronous music during circuit-type exercise. Psychol Sport
Exerc. 2010;11(6):551–9.
8. Dixon S, Gouyon F, Widmer G. Towards characterisation of music via rhythmic
patterns; proceedings of the ISMIR, F, 2004.
9. Womelsdorf T, Fries P. Neuronal coherence during selective attentional pro­
cessing and sensory–motor integration. J Physiol-Paris. 2006;100(4):182–93.

### 10. Reh J, Schmitz G, Hwang TH, et al. Loudness affects motion: asymmetric vol­

ume of auditory feedback results in asymmetric gait in healthy young adults. BMC Musculoskelet Disord. 2022;23(1):586.

### 11. Large EW, Roman I, Kim JC, et al. Dynamic models for musical groove percep­

tion and coordination. Front Comput Neurosci. 2023;17(1151895).

### 12. Patel AD, Iversen JR. The evolutionary neuroscience of musical beat percep­

tion: the Action Simulation for Auditory Prediction (ASAP) hypothesis. Front
Syst Neurosci. 2014;8(57).

### 13. Elliott MT, Ward D, Stables R, et al. Analysing multi-person timing in music

and movement: event based methods. Timing and time perception: proce­
dures, measures, & applications. Brill. 2018:177–215.

### 14. Collins T, Tillmann B, Barrett FS, et al. A combined model of sensory and

cognitive representations underlying tonal expectations in music: from audio
signals to behavior. Psychol Rev. 2014;121(1):33–65.

### 15. Abri F, GUTIéRREZ LF, Datta P, et al. A comparative analysis of modeling and

predicting perceived and induced emotions in sonification. Electronics.
2021;10(20):2519.

### 16. Winters JMJHMS. How detailed should muscle models be to understand

multi-joint movement coordination? Hum Mov Sci. 1995;14(4–5):401–42. Page 20 of 20
Li et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:233

### 17. Cheung VC, Seki K. Approaches to revealing the neural basis of muscle syner­

gies: a review and a critique. J Neurophysiol. 2021;125(5):1580–97.

### 18. Latash ML, Scholz JP, Schoner G. Toward a new theory of motor synergies. Motor Control. 2007;11(3):276–308.

### 19. Wojtara T, Alnajjar F, Shimoda S, et al. Muscle synergy stability and human

balance maintenance. J Neuroeng Rehabil. 2014;11(129).

### 20. Raasch CC. Coordination of pedaling: functional muscle groups and locomo­

tor strategies. Stanford University; 1996.

### 21. BOCKEMüHL T, Troje NF, DüRR V. Inter-joint coupling and joint angle synergies

of human catching movements. Hum Mov Sci. 2010;29(1):73–93.

### 22. Dejnabadi H, Jolles BM, Aminian K. A new approach for quantitative

analysis of inter-joint coordination during gait. IEEE Trans Biomed Eng.
2008;55(2):755–64.

### 23. Phillips-Silver J, Keller PE. Searching for roots of entrainment and joint action

in early musical interactions. Front Human Neurosci. 2012;6(26).

### 24. Mondok C, Wiener M. An entrainment oscillator mechanism underlies human

beat matching performance. bioRxiv, 2024, 2024.03. 07.583955.

### 25. Bacon CJ, Myers TR, Karageorghis CI. Effect of music-movement synchrony on

exercise oxygen consumption. J Sports Med Phys Fitness. 2012;52(4):359–65.

### 26. Braun Janzen T, Koshimori Y, Richard NM, et al. Rhythm and music-based

interventions in motor rehabilitation: current evidence and future perspec­
tives. Front Human Neurosci. 2022;15(789467).

### 27. SO C-H R. Fatigue of lower limb muscles during repetitive cycling exercise:

electromyographic assessment and intervention; 2009.

### 28. Symsack A, Gaunaurd I, Thaper A, Springer B, Bennett C, Clemens S, et al. Usability assessment of the rehabilitation lower-limb orthopedic assistive
device by service members and veterans with lower limb loss. Mil Med.
2021;186(3–4):379–86.

### 29. Hermens HJ, Freriks B, Disselhorst-Klug C, Rau G. Development of recommen­

dations for SEMG sensors and sensor placement procedures. J Electromyogr
Kinesiol. 2000;10(5):361–74. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​s​1​0​5​0​-​6​4​1​1​(​0​0​)​0​0​0​2​7​-​4.

### 30. Janata P, Tomic ST, Haberman JM. Sensorimotor coupling in music and the

psychology of the groove. J Exp Psychol Gen. 2012;141(1):54–75.

### 31. Chen J, Zhou G, Han J, Su P, Zhang H, Tang D. The effect of perceived groove

in music on effective brain connectivity during cycling: an fNIRS study. Med
Sci Sports Exerc. 2025;57(4):857–66.

### 32. Li H, Peng F, Lyu S, Ji Z, Li X, Liu M. Newly compiled tai chi (Bafa Wubu)

promotes lower extremity exercise: a preliminary cross sectional study. PeerJ.
2023;11:e15036.

### 33. Sarvestan J, Aghaie Ataabadi P, Khaleghi Tazji M, Hamill J. Determining the

optimum number of cycles for calculating joint coordination and its vari­
ability during running at different speeds: a timeseries analysis. J Biomech.
2024;176:112375.

### 34. Robbins SM, Teoli A, Huk OL, Zukor DJ, Antoniou J. Inter-segment coordina­

tion amplitude and variability during gait in patients with knee osteoarthritis
and asymptomatic adults. Gait Posture. 2024;107:324–9.

### 35. Persine S, Simoneau-Buessinger E, Charlaté F, Bassement J, Gillet C, Découfour

N, et al. Transfemoral amputees adapt their gait during cross-slope walking
with specific upper-lower limb coordination. Gait Posture. 2023;105:171–6.

### 36. Kibushi B. Muscle coordination patterns in regulation of medial gastrocne­

mius activation during walking. Hum Mov Sci. 2023;90:103116.

### 37. Baifa Z, Xinglong Z, Dongmei L. Muscle coordination during archery

shooting: a comparison of archers with different skill levels. Eur J Sport Sci.
2023;23(1):54–61.

### 38. Seo G, Park JH, Park HS, Roh J. Developing new intermuscular coordination

patterns through an electromyographic signal-guided training in the upper
extremity. J Neuroeng Rehabil. 2023;20(1):112.

### 39. Saito H, Yokoyama H, Sasaki A, Nakazawa K. Muscle synergy patterns as

altered coordination strategies in individuals with chronic low back pain: a
cross-sectional study. J Neuroeng Rehabil. 2023;20(1):69.

### 40. Hafer JF, Roelker SA, Boyer KA. Changes in lower extremity muscle coordina­

tion over a 30-minute walk do not differ by muscle fatigability. J Biomech.
2024;177:112434.

### 41. Vendrame E, Rum L, Belluscio V, Truppa L, Vannozzi G, Lazich A, Bergamini E, Mannini A. Muscle synergies in archery: an explorative study on experienced
athletes with and without physical disability. Annual international conference
of the IEEE engineering in medicine and biology society. IEEE Engineer­
ing in Medicine and Biology Society. Annual international conference;
2021:6220–23.

### 42. Choi A, Lee IK, Choi MT, Mun JH. Inter-joint coordination between hips

and trunk during downswings: effects on the clubhead speed. J Sports Sci.
2016;34(20):1991–7.

### 43. Heuvelmans P, Di Paolo S, Benjaminse A, Bragonzoni L, Gokeler A. Relation­

ships between task constraints, visual constraints, joint coordination and
football-specific performance in talented youth athletes: an ecological
dynamics approach. Percept Mot Skills. 2024;131(1):161–76.

### 44. Dorel S. Mechanical effectiveness and coordination: new insights into sprint

cycling performance. Biomechanics of training and testing: innovative con­
cepts and simple field methods; 2018:33–62.

### 45. Bini RR, Diefenthaeler F, Carpes FP. Lower limb muscle activation during a

40km cycling time trial: co-activation and pedalling technique. Int SportMed

## J. 2011;12(1):7–16.

### 46. Hankinson K. Can rhythm change the brain? Investigating the effect of a

novel music-motor therapy app, GotRhythm, on motor control and cortico­
spinal excitability in healthy and clinical populations. 2021.

### 47. Turpin NA, Costes A, Moretto P, Watier B. Upper limb and trunk muscle

activity patterns during seated and standing cycling. J Sports Sci.
2017;35(6):557–64.

### 48. Kassiano W, Costa BDV, Kunevaliki G, Lisboa F, Tricoli I, Francsuel J, et al. Big­

ger calves from doing higher resistance training volume? Int J Sports Med.
2024;45(10):739–47. Publisher's Note
Springer Nature remains neutral with regard to jurisdictional claims in
published maps and institutional affiliations.
