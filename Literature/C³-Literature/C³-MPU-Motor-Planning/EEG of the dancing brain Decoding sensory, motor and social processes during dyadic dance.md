# EEG of the dancing brain Decoding sensory, motor and social processes during dyadic dance

> **Source:** EEG of the dancing brain Decoding sensory, motor and social processes during dyadic dance.pdf  
> **Converted:** 2025-12-17 15:32:28

---

## Page 1

Research Articles | Behavioral/Cognitive 
  
EEG of the dancing brain: Decoding sensory, motor and
social processes during dyadic dance
 
 
https://doi.org/10.1523/JNEUROSCI.2372-24.2025
 
Received: 17 December 2024
Revised: 5 March 2025
Accepted: 11 March 2025
 
Copyright © 2025 Bigand et al.
This is an open-access article distributed under the terms of the Creative Commons
Attribution 4.0 International license, which permits unrestricted use, distribution and
reproduction in any medium provided that the original work is properly attributed.
This Early Release article has been peer reviewed and accepted, but has not been through
the composition and copyediting processes.The final version may differ slightly in style or
formatting and will contain links to any extended data.
Alerts: Sign up at www.jneurosci.org/alerts to receive customized email alerts when the fully
             formatted version of this article is published.

## Page 2

1 
 
EEG of the dancing brain: Decoding sensory, motor and social processes during 
1 
dyadic dance 
2 
Félix Bigand1,*, Roberta Bianco1, Sara F. Abalde1, Trinh Nguyen1, Giacomo Novembre1,* 
3 
1Neuroscience of Perception & Action Lab, Italian Institute of Technology, Viale Regina Elena 291, 00161 Rome, 
4 
Italy 
5 
*Correspondence: felix.bigand@iit.it (F.B.), giacomo.novembre@iit.it (G.N.)  
6 
 
7 
Abbreviated title: EEG of the dancing brain 
8 
Number of pages: 34 
9 
Number of figures: 7 
10 
Number of multimedia: 1 video 
11 
Number of words: 250 (abstract), 649 (introduction), 1498 (discussion). 
12 
Conflict of interest: The authors declare no conflict of interest.   
13 
Acknowledgments: F.B., S.F.A., and G.N. are supported by the European Research Council 
14 
(ERC, MUSICOM, 948186). R.B. is supported by the European Union (MSCA, 
15 
PHYLOMUSIC, 101064334). T.N. is supported by the European Union (MSCA, SYNCON, 
16 
101105726). We thank Alison Rigby for her help with data collection, and Raoul Tchoï for his 
17 
help creating the stimuli. 
18 
Code accessibility: All original code is publicly available on Github repositories: 
19 
https://github.com/felixbgd/dancing_brain  
20 
Data accessibility: EEG, EMG, EOG, kinematic, and musical data have been deposited to IIT 
21 
Dataverse and are publicly available as of the date of publication:  
22 
https://dataverse.iit.it/privateurl.xhtml?token=bb0689c8-137d-4742-9f94-d7c6b0148827 
23 
JNeurosci Accepted Manuscript

## Page 3

2 
 
Abstract 
24 
Real-world social cognition requires processing and adapting to multiple dynamic information 
25 
streams. Interpreting neural activity in such ecological conditions remains a key challenge for 
26 
neuroscience. This study leverages advancements in de-noising techniques and multivariate 
27 
modeling to extract interpretable EEG signals from pairs of participants (male-male, female-
28 
female, and male-female) engaged in spontaneous dyadic dance. Using multivariate temporal 
29 
response functions (mTRFs), we investigated how music acoustics, self-generated kinematics, 
30 
other-generated kinematics, and social coordination uniquely contributed to EEG activity. 
31 
Electromyogram recordings from ocular, face, and neck muscles were also modeled to control 
32 
for artifacts. The mTRFs effectively disentangled neural signals associated with four 
33 
processes: (I) auditory tracking of music, (II) control of self-generated movements, (III) visual 
34 
monitoring of partner movements, and (IV) visual tracking of social coordination. We show that 
35 
the first three neural signals are driven by event-related potentials: the P50-N100-P200 
36 
triggered by acoustic events, the central lateralized movement-related cortical potentials 
37 
triggered by movement initiation, and the occipital N170 triggered by movement observation. 
38 
Notably, the (previously unknown) neural marker of social coordination encodes the 
39 
spatiotemporal alignment between dancers, surpassing the encoding of self- or partner-related 
40 
kinematics taken alone. This marker emerges when partners can see each other, exhibits a 
41 
topographical distribution over occipital areas, and is specifically driven by movement 
42 
observation rather than initiation. Using data-driven kinematic decomposition, we further show 
43 
that vertical bounce movements best drive observers’ EEG activity. These findings highlight 
44 
the potential of real-world neuroimaging, combined with multivariate modeling, to uncover the 
45 
mechanisms underlying complex yet natural social behaviors. 
46 
Keywords: Electroencephalography (EEG), multivariate modeling, temporal response 
47 
function (TRF), real-world behavior, dance, full-body kinematics, spontaneous movement, 
48 
sensorimotor processing, social coordination. 
49 
Significance statement 
50 
Real-world brain function involves integrating multiple information streams simultaneously. 
51 
However, due to a shortfall of computational methods, laboratory-based neuroscience often 
52 
examines neural processes in isolation. Using multivariate modeling of EEG data from pairs of 
53 
participants freely dancing to music, we demonstrate that it is possible to tease apart 
54 
physiologically established neural processes associated with music perception, motor control, 
55 
and observation of a partner’s movement. Crucially, we identify a previously unknown neural 
56 
marker of social coordination that encodes the spatiotemporal alignment between dancers, 
57 
JNeurosci Accepted Manuscript

## Page 4

3 
 
beyond self- or partner-related kinematics alone. These findings highlight the potential of 
58 
computational neuroscience to uncover the biological mechanisms underlying real-world social 
59 
and motor behaviors, advancing our understanding of how the brain supports dynamic and 
60 
interactive activities. 
61 
Introduction 
62 
A central challenge in neuroscience is understanding how the brain supports natural behavior 
63 
in real-world contexts. Neuroimaging studies have traditionally been limited by bulky, motion-
64 
sensitive equipment, restricting research to controlled, motionless behaviors. This approach 
65 
fails to capture how the brain manages the dynamic, multifaceted demands of everyday life, 
66 
where cognition involves simultaneous neural processes, unconstrained movement, and 
67 
interaction with ever-changing sensory environments—factors that traditional lab studies are 
68 
poorly equipped to address (Stangl et al., 2023). Despite the recent advancements in mobile 
69 
neuroimaging techniques (Niso et al., 2023) and algorithms for removing motion artifacts 
70 
(Kothe and Jung, 2016), studying brain activity during natural behavior remains 
71 
underexploited. As a result, it remains unclear how neural processes identified in lab-controlled 
72 
studies generalize to real-world experiences, limiting our ability to interpret neural signals 
73 
recorded during free behavior. 
74 
Here we used human collective dance as a model to study the neural basis of real-world 
75 
interactions. We reason that dance offers an ideal testbed for several reasons: 1) it is culturally 
76 
ubiquitous, hence broadly generalizable (Mithen, 2006; Dunbar, 2012); 2) it is complex yet 
77 
controllable through musical structure (D’Ausilio et al., 2015); and 3) it encapsulates several 
78 
intertwined neural processes, including auditory-tracking of music, movement control, 
79 
monitoring others’ movements, and integrating these signals into cohesive experiences 
80 
(Foster Vander Elst et al., 2023). These processes—notably targeting a variety of sensory and 
81 
motor systems—can be effectively measured, for example, using electroencephalography 
82 
(EEG). Yet, the main analytical challenge lies in disentangling these simultaneous neural 
83 
signals (capturing sensory, motor, and social functions) from each other, and artifactual 
84 
signals. 
85 
We tackled this challenge using multivariate temporal response functions (mTRFs), a 
86 
computational approach that models the influence of different input variables on neural activity 
87 
(Lalor et al., 2009; Crosse et al., 2016). We applied this method to a dataset of 80 participants, 
88 
forming 40 dyads, who danced spontaneously to music while their brain activity, muscle 
89 
activity, and full-body movements were recorded. Specifically, we captured EEG (64 
90 
channels), 3D full-body kinematics (22 markers),  electrooculography (EOG), and 
91 
electromyography (EMG, from neck and facial muscles), across various experimental 
92 
JNeurosci Accepted Manuscript

## Page 5

4 
 
conditions—detailed below (Bigand et al., 2024). mTRFs were meant to isolate four concurrent 
93 
neural processes: 1) auditory perception of music, 2) motor control of specific body parts or 
94 
specific movements, 3) visual perception of a partner’s body movements, and 4) visual tracking 
95 
of social coordination, defined as the spatiotemporal alignment of movements between 
96 
dancers, whether in-phase or anti-phase. Importantly, EOG and EMG signals were included 
97 
as model predictors to account for potential muscle artifacts affecting the neural data. 
98 
Additionally, we used event-related potential (ERP) analyses to anchor our findings in 
99 
established physiological markers of sensory (auditory and visual evoked potentials) and motor 
100 
(movement-related cortical potentials) processes (Novembre et al., 2018; Bach and Ullrich, 
101 
1997; Deecke et al., 1969). 
102 
Previous studies have used mTRFs to extract neural tracking of ecological auditory and visual 
103 
stimuli, such as speech, music, or films (Di Liberto et al., 2015, 2020; O’Sullivan et al., 2017; 
104 
Fiedler et al., 2019; Jessen et al., 2019; Bianco et al., 2024; Desai et al., 2024). However, 
105 
aside from one human study and recent animal research incorporating body kinematics (Musall 
106 
et al., 2019; Stringer et al., 2019; Di Liberto et al., 2021; Mao et al., 2021; Tremblay et al., 
107 
2023; Lanzarini et al., 2025), human studies that concurrently examine both sensory and motor 
108 
processes using mTRFs—particularly in naturalistic behaviors—remain scarce. Furthermore, 
109 
to our knowledge, no study has explicitly modeled social processes or addressed the neural 
110 
activity associated with body-movement artifact leakage, as we do here. As such, our holistic 
111 
approach aims to demonstrate that naturalistic human behaviors—implying real-time 
112 
adaptation and movement—can be effectively explored using traditional electrophysiology. 
113 
Therefore, our study highlights the potential of advanced neural analysis techniques to bridge 
114 
the gap between lab-controlled and real-world neuroimaging research, enhancing our 
115 
understanding of the neural basis of natural human behavior. 
116 
Materials and methods 
117 
The EEG, EOG, EMG, and kinematic data analyzed here were collected as part of a previous 
118 
study (Bigand et al., 2024), where participant dyads engaged in spontaneous dance under a 
119 
2x2 experimental design (Figs. 1a and 1b). The manipulated within-dyad factors were musical 
120 
input (whether participants danced to the same [synchronous] or different [asynchronous] 
121 
music) and visual contact (whether participants could see or not see their dancing partner). 
122 
 
123 
Participants 
124 
80 participants (54 females; mean age: 26.15 years, SD: 6.43 years, 74 right-handed) formed 
125 
40 dyads (52% female-male, 41% female-female, and 7% male-male). To minimize inter-
126 
JNeurosci Accepted Manuscript

## Page 6

5 
 
individual variability while maximizing generalizability, we recruited only laypersons (i.e. 
127 
individuals without formal dance training). All participants forming a dyad were familiar with 
128 
each other and were informed about the social nature of the task during recruitment, when 
129 
they received the following message (translated from Italian): “You will have to come with 
130 
someone you know (friend, family member, colleague...) with whom you will dance while 
131 
listening to music (almost) like in a disco!”. As a measure of participants’ inclination toward 
132 
social dance, we present the results of a post-hoc questionnaire. Specifically, participants rated 
133 
the statement “How often do you dance to music” with a mean score of 4.363 (SD = 1.052) on 
134 
a 6-point Likert scale (1 = Never to 6 = Very frequently), and rated the statements “When at a 
135 
party, I am likely to be one of the first people dancing” and “I do not worry what other people 
136 
think of my dancing skills” with mean scores of 3.863 (SD = 1.626) and 3.863 (SD = 1.349), 
137 
respectively, on a 6-point Likert scale (1 = Strongly disagree to 6 = Strongly agree). Participants 
138 
had normal or corrected-to-normal vision, normal hearing, and no history of neurological 
139 
disorders. Data from five dyads were excluded due to recording failure in the motion capture 
140 
system, leaving data from 70 participants for the analysis. All participants provided written 
141 
informed consent to participate in the study and were compensated €25 for their participation. 
142 
All experimental procedures were approved by “Comitato Etico Regionale della Liguria” 
143 
(794/2021 - DB id 12093) and were carried out under the principles of the revised Helsinki 
144 
Declaration. 
145 
Musical stimuli 
146 
The musical stimuli consisted of eight songs with an average duration of 39.8 seconds 
147 
(standard deviation: 1.95 seconds). Each song was presented in all four experimental 
148 
conditions (see Experimental Design and Procedure below), resulting in a total of 32 trials. 
149 
These songs were remakes of famous song refrains from electronic dance music and disco-
150 
funk genres (see Bigand et al. (2024)). Each song was adapted using the same four musical 
151 
instruments: drums, bass, keyboards, and violin (the latter providing the vocal melody). All 
152 
stimuli followed a 4/4 meter and spanned 20 bars. To create these adaptations, author FB and 
153 
a professional composer (Raoul Tchoï) transcribed the original 4-bar refrain loops into MIDI 
154 
format and synthesized them using MIDI instruments in Logic Pro X (Apple, Inc.). The 
155 
rearranged songs were then systematically structured by repeating the 4-bar loops five times 
156 
and sequentially adding each instrument to the musical scene, in the following order: (1) 
157 
drums, (2) bass, (3) keyboards, (4) voice, (5) voice bis (i.e. the loop with full instruments was 
158 
repeated twice). Loudness level across songs was controlled within a range of 1.5 LUFS (a 
159 
measure accounting for the frequency sensitivity of the human auditory system). The songs 
160 
were presented to the two participants forming each dyad through two separate EEG-
161 
JNeurosci Accepted Manuscript

## Page 7

6 
 
compatible earphones (Etymotic ER3C), each connected to a distinct output channel of an 
162 
audio interface (RME Fireface UC). 
163 
Every trial consisted of one song flanked with a fast-rising tone (rise time: 5 ms, fall time: 30 
164 
ms, frequency: 494 Hz, duration: 350 ms), preceded by 8 seconds of silence and followed by 
165 
7 seconds of silence, following this pattern: beep-silence-song-silence-beep. Trials were 
166 
controlled using Presentation software (Neurobehavioral Systems), with synchronization 
167 
between song presentation, EEG, and motion capture recordings achieved via TTL pulses. A 
168 
TTL pulse was sent at the start of each trial from Presentation to both the EEG system 
169 
(BioSemi ActiveTwo) and the motion capture system (Vicon; Lock+). This pulse activated the 
170 
motion capture system, initiating recording, which automatically stopped after one minute. 
171 
Simultaneously, the TTL pulse was stored alongside the continuous EEG recordings, which 
172 
remained uninterrupted throughout the experiment. The TTL pulse, whose value varied based 
173 
on the trial condition, enabled us to epoch the EEG data and retrieve the corresponding trial 
174 
condition for analysis. 
175 
Experimental design and procedure 
176 
EEG and kinematic data were recorded across four conditions derived from a 2x2 experimental 
177 
design with visual contact (Yes, No) and musical input (Same, Different) as within-dyad factors. 
178 
Conditions with or without visual contact were defined by the presence or absence of a curtain 
179 
between the two participants in each dyad. Musical input was manipulated by presenting either 
180 
identical or different songs to the participants through earphones. Because each song had a 
181 
different tempo, the songs played simultaneously to the two participants were either perfectly 
182 
synchronized (in the same-music condition) or slightly out of sync (in the different-music 
183 
condition). To minimize inter-trial variability, this degree of asynchrony was maintained 
184 
constant across trials belonging to the different-music condition (i.e. relative tempo difference 
185 
between the two songs was precisely 8.5%). This was achieved by presenting participants with 
186 
songs from different genres during the different-music condition (the tempo associated with 
187 
electronic dance music songs was on average faster than that of disco-funk songs; see Bigand 
188 
et al. (2024)). Trials were organized into four blocks, with each block including eight trials (two 
189 
trials per condition, each trial featuring a different song). The presentation order of the blocks 
190 
– and trials within blocks – was randomized, except for the deliberate presentation of 
191 
subsequent pairs of yes-vision or no-vision trials to minimize the displacement of the curtain.  
192 
Before the experiment began, participants were told to behave as in a “silent disco,” in which 
193 
they should face each other, enjoy the music, and remain still during periods of silence before 
194 
and after the music. To enhance participants’ comfort, the overhead lighting was dimmed using 
195 
JNeurosci Accepted Manuscript

## Page 8

7 
 
alternating red and blue colored filters, creating a softer, “disco-like” atmosphere. Additionally, 
196 
the experimenter remained out of sight in a custom-built cabin (enclosed by 1.5m-high panels), 
197 
ensuring mutual invisibility between the experimenter and participants, as well as concealing 
198 
the acquisition computers. Participants completed two training trials using songs not included 
199 
in the main experiment to familiarize themselves with the task and setting. During this phase, 
200 
they could request volume adjustments to their earphones, which were instructed to be set “as 
201 
loud as possible without discomfort.” Participants were allowed (but not required) to dance 
202 
freely within their designated space, keeping their head orientation towards their partner as 
203 
steady as possible. Speaking or singing during trials was prohibited. Throughout the 
204 
experiment, participants stood facing each other, each positioned within a marked area of 
205 
0.5x0.7 meters, with a separation of 2.5 meters between them. 
206 
Kinematics data acquisition and preprocessing 
207 
3D full-body kinematics were recorded using wearable markers (22 per participant, size=14 
208 
mm). Markers were placed on specific body parts, denoted as follows (L = left, R = right, F = 
209 
front, B = back): (1) LB Head, (2) LF Head, (3) RF Head, (4) RB Head, (5) Sternum, (6) L 
210 
Shoulder, (7) R Shoulder, (8) L Elbow, (9) L Wrist, (10) L Hand, (11) R Elbow, (12) R Wrist, 
211 
(13) R Hand, (14) Pelvis, (15) L Hip, (16) R Hip, (17) L Knee, (18) L Ankle, (19) L Foot, (20) R 
212 
Knee, (21) R Ankle, (22) R Foot (Fig. 1a). Additionally, one supplementary marker was placed 
213 
asymmetrically on either the left or right thigh of each participant. This marker was only used 
214 
to facilitate Nexus software in the distinction between participants and was not considered in 
215 
subsequent analyses. Eight optical motion capture cameras (Vicon system) recorded the 
216 
markers’ trajectories at a sampling rate of 250 Hz. The cameras were positioned to capture 
217 
the participants from various angles, ensuring that each participant was visible to at least six 
218 
cameras even when visual contact was obstructed by the curtain. A high-definition video 
219 
camera, synchronized with all the optical motion capture cameras, recorded the scene from 
220 
an aerial view (Vicon Vue; 25 Hz sampling frequency; 1,920 × 1,080 pixels). We used a Vicon 
221 
motion capture system to record full-body 3D positions with high spatial (<1 mm precision) and 
222 
temporal (250 Hz) resolution. While alternative methods, such as inertial measurement units 
223 
or accelerometers, could be considered, the feasibility of repeating our study with fewer 
224 
markers remains to be tested. Notably, full-body tracking was essential here for breaking down 
225 
complex dance kinematics into the elementary movement components that drove neural 
226 
signals (see Kinematic feature selection below).  
227 
Markers’ trajectories were corrected for swaps or mislabels via the Nexus manual labeling tool 
228 
(Vicon). Then, automated correction of frequent and systematic marker swaps was performed 
229 
JNeurosci Accepted Manuscript

## Page 9

8 
 
using custom Python code. Any gaps in the marker trajectories were then filled using the 
230 
automatic gap-filling pipeline in Nexus. The proportion of time with gaps, calculated for each 
231 
marker and averaged across participants, ranged from a minimum of 0.128% (L Foot) to a 
232 
maximum of 2.767% (R Hip), with a mean of 0.688% and a standard deviation of 0.739%. 
233 
Lastly, all trajectories were inspected visually within Nexus software and manually adjusted if 
234 
they did not match the aerial-view video recording. Subsequent data analyses were carried 
235 
out in Python using custom code. Marker trajectories comprised 3D positions (along x, y, and 
236 
z axes) corresponding to each of the 22 body parts, resulting in time-series of posture vectors 
237 
of 66 dimensions. 
238 
EEG data acquisition and preprocessing 
239 
We recorded neural activity from both participants simultaneously using a dual-EEG setup with 
240 
the BioSemi ActiveTwo system. This setup consists of two AD-Boxes, each independently 
241 
recording and referencing EEG from a single participant. The data from the two AD-Boxes are 
242 
synchronized at the hardware level: the ‘slave’ AD-Box transmits data via optical fiber to the 
243 
‘master’ AD-Box, which then relays all EEG signals and triggers information to the acquisition 
244 
computer. For a detailed schematic of the BioSemi ActiveTwo dual-EEG configuration, see 
245 
Barraza et al. (2019). For each participant, the EEG was recorded from 64 Ag/AgCl active 
246 
electrodes (placed on the scalp according to the extended international 10–10 system). To 
247 
help retain the naturalistic nature of the study, we used 2-meter-long cables, custom-built by 
248 
the manufacturer to meet our specific requirements. Each EEG amplifier was positioned 
249 
behind the participant at hip height, with cables taped to the upper back to minimize weight 
250 
while ensuring they remained loose enough to prevent any perceived constraint or pulling. This 
251 
setup allowed participants to move relatively freely while remaining within their designated 
252 
area (see Experimental Design and Procedure). 
253 
EEG signals were digitized at 1024 Hz using the BioSemi Active Two system. Subsequently, 
254 
the data were pre-processed and analyzed using Matlab R2022. Measuring EEG from moving 
255 
participants is susceptible to muscular artifacts in the recordings. To mitigate this issue, we 
256 
pre-processed the EEG data of the dancing participants using a fully data-driven pipeline that 
257 
we had previously developed for analyzing EEG data in awake monkeys (Bianco et al., 2024). 
258 
This pipeline primarily utilizes open-source algorithms from Fieldtrip (Oostenveld et al., 2011) 
259 
and EEGLAB (Delorme and Makeig, 2004) toolboxes. EEG signals were digitally filtered 
260 
between 1 and 8 Hz (Butterworth filters, order 3), down-sampled to 100 Hz, and trimmed 
261 
according to the duration of the trial-specific songs. Faulty or noisy electrodes were 
262 
provisionally discarded before re-referencing the data using a common average reference. 
263 
JNeurosci Accepted Manuscript

## Page 10

9 
 
This was done to prevent the leakage of noise to all electrodes during re-referencing. Criteria 
264 
for flagging faulty or noisy electrodes included prolonged flat lines (lasting more than 5 
265 
seconds), abnormal inter-channel correlation (lower than 0.8), or deviations in amplitude 
266 
metrics from the scalp average (mean, STD, or peak-to-peak values exceeding 3 STD from 
267 
the scalp average). These assessments were made using EEGlab's clean_flatlines and 
268 
clean_channels functions (Delorme and Makeig, 2004) and custom Matlab code. To remove 
269 
movement artifacts, we further denoised the re-referenced data using a validated algorithm for 
270 
automatic artifact correction: Artifact Subspace Reconstruction (ASR, threshold value 5) 
271 
(Kothe and Jung, 2016). This algorithm has been previously applied to human data, including 
272 
in music-making and dance studies (Ramírez-Moreno et al., 2023; Theofanopoulou et al., 
273 
2024). Finally, eye-movement artifacts were subtracted from the ASR-cleaned data using 
274 
another automatic artifact-correction algorithm – ICA, using EEGlab’s IClabel function (Pion-
275 
Tonachini et al., 2019). Independent Components that were classified by IClabel as eye-
276 
movement artifacts (i.e., those for which the ‘eye’ category had the highest probability, with no 
277 
minimum threshold) were removed. At this stage, noisy or faulty electrodes (as assessed at 
278 
the start of this preprocessing pipeline) were interpolated by replacing their voltage with the 
279 
average voltage of the neighboring electrodes (20-mm distance).  
280 
EOG and EMG data acquisition and preprocessing 
281 
Two EOG channels were recorded using surface Ag–AgCl electrodes from all participants. 
282 
Electrodes were attached using disposable adhesive disks at specific anatomical locations: 
283 
the left and right outer canthi. Additionally, we also recorded four EMG signals from the cheeks 
284 
(the left and right zygomata) and the neck (the left and right paraspinal muscles) for control 
285 
purposes. EOG/EMG signals were digitized at 1024 Hz using the BioSemi Active Two system. 
286 
The EOG/EMG data were filtered, down-sampled, and trimmed similarly as the EEG data, re-
287 
referenced using scalp average, and ASR-cleaned using a threshold value of 5, to maintain 
288 
consistency with the EEG signals from scalp channels. It should be noted that these signals 
289 
were measured from a subset of participants (n=58), therefore all subsequent analyses 
290 
involving this data subset include only these participants. 
291 
Multivariate temporal response functions (mTRFs) 
292 
Events, such as hearing a fast-rising sound or initiating a movement, elicit phase-locked brain 
293 
activity within a specific time window [t1,t2], which can include post-event (e.g., response to 
294 
sounds) and pre-event (e.g., movement initiation) components (Luck, 2014). Temporal 
295 
response functions (TRFs) can be used to characterize this relationship at the level of EEG 
296 
electrodes (Lalor et al., 2009; Crosse et al., 2016). In this study, we applied mTRFs to delineate 
297 
JNeurosci Accepted Manuscript

## Page 11

10 
 
the distinct neural processes that occur simultaneously during dyadic dance. Specifically, we 
298 
first extracted a diverse set of time-resolved variables, representing: (I) musical input, (II) self-
299 
generated movements, (III) partner-generated movements, (IV) social coordination, and (V, VI, 
300 
and VII) ocular, facial and neck muscle activity (Fig. 1c, left). Next, we estimated TRFs (Fig. 
301 
1c, middle) to quantify how these variables modulate EEG signals, for each electrode 
302 
separately (Fig. 1c, right). The following sections provide a detailed explanation of these two 
303 
steps.  
304 
Step 1: Extraction of variables. (I) Music. Musical input was represented using spectral flux, 
305 
which captures fluctuations in the acoustic power spectrum. Spectral flux has been shown to 
306 
outperform other acoustic features, such as the envelope and its derivative, in predicting neural 
307 
signals elicited by music (Weineck et al., 2022). To extract it, we first bandpass filtered the 
308 
musical stimuli into 128 logarithmically spaced frequency bands ranging from 100 to 8000 Hz 
309 
using a gammatone filter bank. Spectral flux was then computed for each frequency band by 
310 
calculating the first derivative of the band’s amplitude over time. Finally, the broadband spectral 
311 
flux, representing overall changes in the spectral content, was derived by averaging the 
312 
spectral flux across all 128 bands. (II and III) Self- and other-generated movements. The 
313 
movements produced by each participant (self-generated) and their partners (other-generated) 
314 
were represented using velocity magnitude. To reduce dimensionality, full-body trajectories 
315 
were decomposed into 15 principal movement patterns that collectively explained over 95% of 
316 
the kinematic variance (see Methods in Kinematic feature selection below). The velocity 
317 
magnitude of each principal movement was calculated by taking the first derivative of its 
318 
position over time and then computing the absolute value of this derivative. Out of the 15 
319 
principal movements, preliminary analyses identified bounce as the movement that explained 
320 
most of the neural encoding of both self- and other-generated movements (see results in 
321 
Kinematic feature selection below, and Fig. 2). Consequently, only the velocity magnitude of 
322 
the bounce trajectory was included in subsequent models. (IV) Social coordination. To assess 
323 
social coordination, we extracted a categorical measure to determine whether the bounce 
324 
movements of participants within a dyad were in-phase or anti-phase. This measure indexed 
325 
whether both individuals moved in the same direction (in-phase) or opposite directions (anti-
326 
phase). We obtained this measure by multiplying the signs of the bounce velocity time series 
327 
(i.e., the respective directions of movement) across the two participants forming a dyad. (V, 
328 
VI, and VII) Ocular, facial, and neck muscle activity. To control for muscular activity potentially 
329 
leaking into the EEG signals, we also included EOG (measured from the left and right eyes) 
330 
and EMG (measured from the cheeks and the neck) time-series in the models. Both EOG 
331 
channels (left and right eye) were included to capture horizontal saccades, which generate 
332 
opposite left-right activity (positive values on one side and negative on the other). For cheek 
333 
JNeurosci Accepted Manuscript

## Page 12

11 
 
and neck muscles, the average signal from the left and right EMG channels was used, 
334 
respectively. All these variables, each of which is time-resolved, were down-sampled to match 
335 
the EEG sampling frequency of 100 Hz and trimmed according to the duration of the trial-
336 
specific songs. To account for inter-individual variability, all variables were standardized on a 
337 
per-participant basis by normalizing each time-series to its standard deviation across all trials 
338 
for the corresponding participant. 
339 
Step 2: mTRF estimation. We estimated TRFs via a multivariate lagged regression, which fitted 
340 
the optimal linear mapping between the abovementioned variables and EEG at each electrode 
341 
(mTRF toolbox, encoding model (Crosse et al., 2016); Fig. 1c). A time-lag window of -250 to 
342 
300 ms was selected to encompass commonly observed ERP responses associated with 
343 
sound perception (Novembre et al., 2018), execution of fast-repeated movements (Gerloff et 
344 
al., 1997), and visual perception of biological movements (Jokisch et al., 2005). This window 
345 
also ensured that the contribution of redundant (potentially irrelevant) information was 
346 
minimized, especially considering the rhythmic structure of the task, with musical beats and 
347 
some dance movements (e.g., bounce) occurring approximately every 500 ms. Importantly, in 
348 
a control analysis we confirmed that the selected window did not reduce prediction accuracy 
349 
compared to a broader [-700, +700 ms] window. For each participant and experimental 
350 
condition, mTRFs were estimated, including either all variables simultaneously (full model) or 
351 
all variables except the specified one (reduced models; see below for details). Participant- and 
352 
condition-specific TRFs were estimated as the average TRF required to predict each of the 
353 
eight condition trials using data from the remaining seven trials (i.e., TRFs were fit eight times). 
354 
Regularized (ridge) regression was used to fit the TRFs, maximizing prediction accuracy (the 
355 
correlation between the predicted and actual EEG data; Pearson’s r) without overfitting the 
356 
training data. The optimal regularization parameter (λ) was selected via leave-one-out cross-
357 
validation across trials (i.e., songs), tested over a range from 0 to 10⁸ (0, 10⁻⁴, 10⁻³, …, 10⁸). 
358 
This yielded one optimal λ value per trial, condition, and participant. Finally, prediction 
359 
accuracies for each condition were assessed using a generic approach (Di Liberto and Lalor, 
360 
2017; Jessen et al., 2019), where the Pearson’s r between predicted and actual EEG data was 
361 
calculated across all eight trials of the nth participant, with predictions based on a generic TRF 
362 
averaged across the subject-specific TRFs of the N-1 remaining participants (N=70). The 
363 
prediction accuracy of a model describes the amount of EEG variance that the model can 
364 
account for. To evaluate the unique amount of EEG variance that each variable accounts for, 
365 
we constructed reduced models that included all variables apart from the specified one. The 
366 
difference in prediction accuracy between the full (comprising all variables) and the reduced 
367 
model yielded the unique contribution, denoted as Δr, of that specific variable to the variance 
368 
explained in the EEG data (Fig. 1d).  
369 
JNeurosci Accepted Manuscript

## Page 13

12 
 
Kinematic feature selection 
370 
To reduce dimensionality, we used a data-driven method to determine a subset of kinematic 
371 
variables to use in the TRF models. The kinematic data were decomposed into a set of 
372 
principal movements using Principal Component Analysis (PCA), following the same pipeline 
373 
as described in  Bigand et al., (2024). These principal movements reflect movement primitives 
374 
that are generalizable across trials, conditions, and participants. This PCA approach has been 
375 
previously validated for a wide range of human movements, including dance (Troje, 2002; 
376 
Daffertshofer et al., 2004; Toiviainen et al., 2010; Federolf et al., 2014; Yan et al., 2020; Bigand 
377 
et al., 2021). The first 15 principal movements – accounting for more than 95% of the kinematic 
378 
variance – were retained for further analyses (Federolf et al., 2014; Bigand et al., 2021). The 
379 
score time series obtained from the PCA reflected the position of each principal movement 
380 
over time. These time-series were low-pass filtered below 6 Hz using a Butterworth filter 
381 
(second-order, zero-phase) to increase the signal-to-noise ratio. These 15 principal 
382 
movements were reminiscent of common “dance moves” such as body sway, twist, upper-
383 
body side bend and rock, bounce, side displacement, head bob, hip swing, and hand 
384 
movements (see Fig. 2 and Video 1) (Bigand et al., 2024). 
385 
To determine which principal movements to include in the TRF models, we tested their 
386 
association with EEG modulations. Previous evidence suggests that TRFs or equivalent 
387 
models can accurately capture neural activity associated with both the generation (Musall et 
388 
al., 2019) and the observation (O’Sullivan et al., 2017; Jessen et al., 2019) of biological 
389 
movement. Accordingly, we tested the unique contribution of the 15 principal movements, 
390 
either self-generated or generated by (and therefore observed in) the dancing partner. In other 
391 
words, we fit 30 reduced models and computed the difference in prediction accuracy (Δr) 
392 
between each reduced model and a full model (including all 30 principal movements plus 
393 
spectral flux) for each participant and condition, using the generic approach outlined above 
394 
(see Methods in mTRF estimation above). Spectral flux was included in the full model to ensure 
395 
that the explanatory power of individual principal movements was not influenced by 
396 
movements correlated with the music as participants were dancing to music. To reduce 
397 
computational cost, the 15 models for other-generated movements were trained in the visual 
398 
conditions, while those for self-generated movements were trained in the non-visual 
399 
conditions. This ensured a balanced number of trials for analyzing both motor control and 
400 
movement observation activities while testing movement observation under the conditions 
401 
where it was most likely to occur. The full model was trained across all conditions, allowing for 
402 
the computation of “self” and “other” Δr values, averaged across the two non-visual and visual 
403 
conditions, respectively. 
404 
JNeurosci Accepted Manuscript

## Page 14

13 
 
The results of this preliminary analysis revealed that bounce movement—i.e., vertical 
405 
oscillations of the body achieved through knee flexion and extension—was largely the main 
406 
contributor to EEG prediction, notably across both self- and other-generated movements (see 
407 
PM10; Fig. 2), despite accounting for no more than 1% of the total kinematic variance. 
408 
Specifically, self-generated bounce alone explained >84% of the EEG prediction gain (Δr > 0) 
409 
across all principal movements at electrode Cz, commonly associated with motor activity 
410 
(Kornhuber and Deecke, 1965; Deecke et al., 1969; Shibasaki et al., 1980; Smulders and 
411 
Miller, 2011; Vercillo et al., 2018). Additionally, other-generated bounce alone accounted for 
412 
>80% of EEG prediction gain at electrode Oz, a canonical site indicative of motion-evoked 
413 
visual responses (Kubová et al., 1995; Bach and Ullrich, 1997; Puce et al., 2000; Jokisch et 
414 
al., 2005; O’Sullivan et al., 2017). Given these results, bounce will serve as the primary 
415 
movement feature in all subsequent analyses. Henceforth, when referring to “movement” in 
416 
the following sections, we specifically denote “bounce” (except when discussing the results of 
417 
the body-part-specific analyses). 
418 
Statistical analyses  
419 
We assessed the distinct neural encoding of music, self-generated movements, other-
420 
generated movements, and social coordination while controlling for artifact leakage from eye, 
421 
facial, and neck movements. We created seven reduced models, accounting for: (I) music (all 
422 
variables minus spectral flux); (II) self-generated movements (all variables minus velocity 
423 
magnitude of self-generated bounce); (III) other-generated movements (all variables minus 
424 
velocity magnitude of other-generated bounce); (IV) social coordination (all variables minus 
425 
interpersonal bounce coordination); and (V, VI and VII) ocular, facial and neck muscle activity 
426 
(all variables minus EOG, facial EMG, or neck EMG, respectively). We then compared the 
427 
prediction accuracies of these reduced models to that of a full model encompassing all seven 
428 
variables, i.e., the unique contribution Δr of each variable.  
429 
To compare the unique contributions of music, self-generated movements, other-generated 
430 
movements, and social coordination across different experimental conditions (visual contact 
431 
(yes/no) x music (same/different)), Δr values were averaged across relevant electrodes for 
432 
each participant and predictor. Relevant electrodes were defined independently for each 
433 
predictor as those that exhibited a prediction gain (Δr > 0). For each predictor, this gain was 
434 
computed across conditions where the associated neural process was expected to occur: all 
435 
conditions for music and self-related movements, and visual conditions for other-generated 
436 
movements and coordination. The Δr values to be statistically compared were computed for 
437 
each condition and then averaged across the defined electrodes. This yielded a Δr value per 
438 
JNeurosci Accepted Manuscript

## Page 15

14 
 
participant, condition, and variable (music, self- and other-generated movements, and social 
439 
coordination).  
440 
We assessed differences in unique contributions across conditions using a 2×2 repeated-
441 
measures ANOVA with the factors “visual contact” and “musical input”. Δr values were 
442 
normally distributed and entered into the ANOVA as the dependent variable. To control for 
443 
multiple comparisons across the four variables, p-values were Bonferroni-corrected. 
444 
Event-related potentials (ERPs) 
445 
Extraction of ERPs. To aid in interpreting the TRF results—particularly the physiological origins 
446 
of the TRF model weights—we examined phase-locked neural responses, i.e., event-related 
447 
potentials (ERPs), evoked by changes in music intensity, self-generated movement velocity, 
448 
other-generated movement velocity, and social coordination (transitions between in-phase and 
449 
anti-phase coordination – see below). EEG responses are largely evoked by fast changes in 
450 
the environment (Somervail et al., 2021), including fluctuations in the auditory spectrum 
451 
(Weineck et al., 2022) and peaks in movement velocity (Varlet et al., 2023). Therefore, we 
452 
determined the onset times of events, such as sounds or movements, by identifying peaks in 
453 
the respective time series using Matlab’s findpeaks function (with default parameters). 
454 
Acoustic onsets were thus aligned with musical notes played by any of the four instruments in 
455 
the stimuli, while motion onsets were aligned with velocity peaks. Coordination onsets were 
456 
obtained from the first derivative of the coordination time series, corresponding to transitions 
457 
between in-phase and anti-phase states. To improve the signal-to-noise ratio, acoustic peaks 
458 
were filtered by selecting only the most salient, i.e., those that were 3 STD away from the mean 
459 
of the trial. This step was unnecessary in the case of the other variables, such as movement 
460 
and coordination, presumably because the kinematic data had already been low-pass filtered, 
461 
as described earlier. Consequently, the signal-to-noise ratio for these variables was already 
462 
maximized. The ERP epochs spanned the same time window as the TRFs (-250 to 300 ms). 
463 
ERP sensitivity to variables’ intensity. ERP amplitude largely depends on the differential 
464 
intensity of the evoking change, and this sensitivity to differential intensity is supramodal, i.e., 
465 
it’s a property observed across different sensory systems (Somervail et al., 2021). Here, to 
466 
quantify whether ERPs were modulated by the differential amplitude of musical sounds or by 
467 
the speed of self- and other-generated movements, we categorized acoustic onsets into 
468 
soft/loud and movement onsets into slow/fast. For each participant and experimental condition, 
469 
we selected acoustic and motion onsets with the highest and lowest 20% values of spectral 
470 
flux or velocity magnitude, respectively. Similarly, to quantify the ERP modulation as a function 
471 
of coordination, we grouped coordination onsets into their two possible values: change to in-
472 
JNeurosci Accepted Manuscript

## Page 16

15 
 
phase or anti-phase. Following established ERP literature (Jokisch et al., 2005; Novembre et 
473 
al., 2018; Vercillo et al., 2018), epochs linked to external stimuli (music and other) were 
474 
baseline corrected using a pre-stimulus interval (-250 to 0 ms), while epochs involving 
475 
internally-initiated actions (self and coordination) were baseline corrected using the entire 
476 
epoch duration. Differences between the two groups (soft vs. loud, slow vs. fast, or in-phase 
477 
vs. anti-phase) were tested separately for each experimental condition, by means of a cluster-
478 
based permutation test (implemented in Fieldtrip, with 1000 permutations [Maris and 
479 
Oostenveld, 2007]). This analysis focused on the EEG channels of interest informed by the 
480 
mTRF results: Fz (music), C3 and C4 (self-generated movements), Oz (other-generated 
481 
movements), and Oz (social coordination). 
482 
Body-part-specific mTRF (self) 
483 
In the main analysis, motor activity was assessed using mTRFs predicted by the kinematics of 
484 
self-generated bounce, as this movement explained most motor activity across the 15 principal 
485 
movements identified via PCA. Hence, the main analysis does not differentiate between body 
486 
parts, as the bounce movement activates nearly all of them (see Fig. 2 and Video 1), making 
487 
it challenging to determine whether the movement of specific body parts drove specific motor 
488 
activities. To address this issue, we leveraged kinematic data from all parts of the body to 
489 
calculate the unique contribution of self-generated motion to the EEG from the left and right 
490 
hand, left and right foot, and head velocity magnitudes. Specifically, we created a full model 
491 
that included major body markers (‘LB Head’, ‘LF Head’, ‘RF Head’, ‘RB Head’, ‘Sternum’, ‘L 
492 
Shoulder’, ‘R Shoulder’, ‘L Hand’, ‘R Hand’, ‘Pelvis’, ‘L Hip’, ‘R Hip’, ‘L Knee’, ‘L Foot’, ‘R Knee’, 
493 
‘R Foot’) along with neck EMG controls, and five reduced models, each excluding specific 
494 
markers: left/right hand markers, left/right foot markers, and the average of the four head 
495 
markers. Markers expected to be almost intrinsically correlated with hand and foot movements 
496 
(e.g., elbows, wrists, and ankles) were not included in the full model. As in the main analysis, 
497 
the unique contribution of each body part’s kinematics to the EEG variance was determined 
498 
by the difference in prediction accuracy between the full model and each reduced model. 
499 
Encoding of social coordination  
500 
Coordination beyond self and other? Social coordination was operationalized as the 
501 
spatiotemporal alignment of movements produced by participants (self-generated) and their 
502 
partners (other-generated). Specifically, this construct assessed whether participants and their 
503 
partners not only bounced at the same time but also in the same direction. As such, social 
504 
coordination relied on both temporal features (velocity magnitude time-series) and spatial 
505 
features (velocity sign time-series), with the latter indicating the up versus down phases of 
506 
JNeurosci Accepted Manuscript

## Page 17

16 
 
movement. In contrast, the measures of self and other were derived solely from temporal 
507 
features. Consequently, it was essential to conduct a control analysis to assess the extent to 
508 
which social coordination was influenced by the spatial characteristics of both self- and other-
509 
generated movements. To address this, we implemented an mTRF analysis utilizing a 
510 
comprehensive model that incorporated music, self-generated and other-generated 
511 
movements (velocity magnitude time-series), social coordination, and the spatial directions of 
512 
both self- and other-generated movements (velocity sign time-series). For this control analysis, 
513 
we did not include other control variables, such as muscular activity, because the previous 
514 
analyses already demonstrated that these do not predict social coordination.  
515 
Coordination ERPs driven by self or other? In our main ERP analysis, we extracted 
516 
“coordination ERPs” by epoching EEG time-series at transition onsets between in-phase and 
517 
anti-phase coordination (see Extraction of ERPs methods described above). These transitions 
518 
could potentially arise from changes in movement direction elicited by either the self or the 
519 
partner. To disentangle these two possibilities—specifically, whether ERPs related to social 
520 
coordination were driven by self-generated movements (self) or by partner-generated 
521 
movements (other)—we categorized coordination ERPs into two distinct groups: those 
522 
triggered by self-movements (i.e., when coordination changes were aligned with shifts in the 
523 
velocity sign of self-generated movements) and those triggered by partner movements (i.e., 
524 
when coordination changes aligned with shifts in the velocity sign of other-generated 
525 
movements). We quantified the in-phase/anti-phase ERP modulation separately for these two 
526 
groups, following the methods outlined previously (see previous ERP analyses). Differences 
527 
between in-phase and anti-phase onsets were assessed independently for the “self” and 
528 
“other” groups in each experimental condition using a cluster-based permutation test 
529 
(implemented in FieldTrip with 1000 permutations [Maris and Oostenveld, 2007]). This analysis 
530 
focused on the channel of interest informed by the mTRF results: Oz. 
531 
Results 
532 
Multivariate temporal response functions (mTRFs) 
533 
In our analysis, we assessed the unique contributions of four variables to the EEG by 
534 
comparing the prediction gain (Δr) between a full mTRF model and reduced models excluding 
535 
each variable of interest (see Methods for details). The results showed that musical sounds, 
536 
self-generated movements, other-generated movements, and social coordination each made 
537 
distinct contributions to participants’ neural activity. This allowed us to isolate four neural 
538 
processes co-occurring during dyadic dance: (I) auditory perception of music, (II) control of 
539 
movement, (III) visual perception of the partner’s body movements, and (IV) visual tracking of 
540 
JNeurosci Accepted Manuscript

## Page 18

17 
 
social coordination. These processes were clearly distinguished from ocular, facial, and neck 
541 
muscle artifacts (V, VI, and VII). The following section provides detailed information on each 
542 
of these EEG activities. 
543 
(I) Auditory perception of music. The spectral flux of the music uniquely predicted EEG 
544 
across frontal and parietal electrodes, as evidenced by the prediction gain Δr (the difference 
545 
between the prediction of the full model and that of the reduced model excluding spectral flux) 
546 
at each electrode (Fig. 3a). A repeated-measures ANOVA, with “musical input” and “visual 
547 
contact” as factors, yielded a main effect of vision, demonstrating a significant reduction in the 
548 
prediction gain Δr when participants could see each other (F(1,57) = 7.48, p = .033; Fig. 4). 
549 
This finding suggests a diminished neural tracking of music when participants could see their 
550 
partners. The regression weights associated with the music TRF model (representing 
551 
electrode Fz) highlight three post-stimulus modulations, i.e., a positive-negative-positive 
552 
pattern with peaks at around +60, +120, and +200 ms post-stimulus, respectively (Fig. 3b). 
553 
The weights also exhibit a consistent peak around -200 ms pre-stimulus, which, considering 
554 
the periodic rhythmic nature of the music, is likely evoked by the preceding beat sound. We 
555 
confirmed so by observing that the sound differential intensity (specifically, the spectral flux 
556 
value) of the previous beat modulated the amplitude of this -200 ms peak. 
557 
(II) Control of movement (self-generated). Self-generated movements uniquely predicted 
558 
EEG across central and occipital electrodes, as indicated by the electrode-specific prediction 
559 
gain Δr (Fig. 3a). The ANOVA did not yield evidence of significant effects of musical input or 
560 
visual contact on the unique contribution of self-generated movements on EEG signals, 
561 
suggesting comparable motor control processes across conditions (all ps > .224; Fig. 4). The 
562 
TRF weights associated with self-generated movements (representing the average between 
563 
electrodes C3 and C4) highlighted three main modulations, i.e., a negative-positive-negative 
564 
pattern with peaks at around -100, 0, and +80 ms relatively to movement onset, respectively 
565 
(Fig. 3b). 
566 
(III) Visual perception of partner’s body movements (other-generated). Other-generated 
567 
movements uniquely predicted EEG across occipital electrodes, surrounding the visual cortex 
568 
(Fig. 3a), only when participants could see each other. This was confirmed by the ANOVA, 
569 
yielding a main effect of visual contact (F(1,57) = 83.23, p < .001; Fig. 4). This finding is 
570 
consistent with the expectation that neural tracking of others’ movements can only occur when 
571 
these movements are observable. The TRF weights associated with other-generated 
572 
movements (representing electrode Oz) highlighted a biphasic modulation characterized by a 
573 
JNeurosci Accepted Manuscript

## Page 19

18 
 
positive peak at around +70 ms, and a negative peak at around +160 ms relative to movement 
574 
onset (Fig. 3b). 
575 
(IV) Social coordination. Social coordination uniquely predicted EEG primarily across 
576 
occipital electrodes (Fig. 3a), especially when participants could see each other and listened 
577 
to the same music. This was supported by the ANOVA, which yielded main effects of visual 
578 
contact (F(1,57) = 249.75, p < .001) and musical input (F(1,57) = 30.22, p < .001), along with 
579 
a significant interaction effect (F(1,57) = 50.10, p < .001) (Fig. 4). Follow-up comparisons 
580 
revealed that EEG prediction accuracy was specifically enhanced when participants danced 
581 
to the same music, but only with visual contact (Δ = 0.0009, SE = 0.0001, p < .001); no music 
582 
effect was observed without visual contact (p = .676) (Fig. 4). This suggests that the level of 
583 
coordination between participants is encoded in each participant’s EEG, and that neural 
584 
tracking occurs primarily when partners are visible and synchronizing to the same musical 
585 
tempo. In this condition, the TRF weights (representing electrode Oz) exhibited a quadriphasic 
586 
pattern characterized by negative-positive-negative-positive peaks, at -180, -90, +30, and 
587 
+160 ms relative to a change in coordination (between in-phase and anti-phase – see 
588 
Methods), respectively (Fig. 3b). 
589 
(V, VI, and VII) Ocular, facial, and neck muscle artifacts. EOG and EMG signals uniquely 
590 
predicted EEG at electrode sites that closely matched artifactual topographical maps 
591 
documented in previous EEG research (Fig. 3a) (Goncharova et al., 2003; Plöchl et al., 2012). 
592 
Specifically, EMG from facial and neck muscles predicted EEG activity at the scalp periphery, 
593 
which is typical of muscle contraction topographies (Goncharova et al., 2003), while EOG 
594 
predicted EEG activity nearby the eyes (electrodes AF7 and AF8, approaching the lateral 
595 
canthi), characteristic of eye saccades (Plöchl et al., 2012). Note that most blinks-related 
596 
artifacts were presumably removed beforehand via ASR and ICA pipelines (see Methods). The 
597 
TRF weights for eye, facial, and neck movements displayed features of instantaneous impulse 
598 
responses (Fig. 3b), indicating that non-cerebral signals propagate to the EEG without 
599 
measurable delay—a characteristic previously established for artifact leakage (Croft and 
600 
Barry, 2000). Additionally, these EOG and EMG signals contributed orders of magnitude more 
601 
to the EEG than brain processes (compare Δr scales within Fig. 3a), another expected property 
602 
of EMG and EOG activations (Urigüen and Garcia-Zapirain, 2015). Collectively, these findings 
603 
underscore the efficiency of our analysis in distinguishing simultaneous neurophysiological 
604 
processes from each other, as well as from movement-related artifact leakage. 
605 
Event-related potentials (ERPs) 
606 
JNeurosci Accepted Manuscript

## Page 20

19 
 
To elucidate the physiological origins of the temporal responses modeled by the mTRFs, we 
607 
extracted ERPs by epoching the EEG time series around salient changes (see Methods) in 
608 
music, self-generated movements, other-generated movements, and social coordination. This 
609 
analysis was specifically designed to clarify the neurophysiological origin of the temporal 
610 
responses, or model weights, modeled by the mTRFs. Notably, the focus was not on the 
611 
condition-specific contribution of these responses to the EEG, as ERP analysis cannot fully 
612 
account for concurrent contributions from other variables. Rather, the results demonstrated 
613 
that the ERPs exhibited morphologies closely resembling the TRF weights observed earlier 
614 
(compare Fig. 5 with Fig. 3b) and consistent with typical EEG markers of sensory and motor 
615 
processes established in laboratory-controlled studies. Detailed ERP results for each process 
616 
are presented in the following sections.  
617 
(I) Auditory perception of music. The individual sounds embedded within the musical tracks 
618 
elicited a characteristic triphasic ERP response, consisting of an early positivity (P50), followed 
619 
by a widespread negativity (N100), and a later positivity (P200), all displaying a frontal 
620 
topographic distribution (Fig. 5). This pattern aligns with established findings from both ERP 
621 
(Novembre et al., 2018; Di Liberto et al., 2020) and TRF studies (Di Liberto et al., 2015, 2020; 
622 
Fiedler et al., 2019; Jessen et al., 2019; Kern et al., 2022) in motionless participants, and 
623 
closely resembles the regression weights of the music TRF observed in our study with dancing 
624 
participants (Fig. 3b). These similarities suggest that our music TRF primarily captured phase-
625 
locked responses evoked by the individual sounds embedded within the musical stimuli, as 
626 
observed in previous work (Di Liberto et al., 2020; Bianco et al., 2024). To validate this 
627 
assumption, we further report a known physiological property of these responses—ERP 
628 
amplitude sensitivity to variations in stimulus intensity (Somervail et al., 2021)—as evidenced 
629 
by the amplitude of the P200 being larger in response to loud vs soft sounds (Fig. 5).  
630 
(II) Control of movement (self-generated). ERPs time-locked to self-generated movements 
631 
displayed a triphasic pattern, characterized by a pre-motor negativity (N-100), a positivity at 
632 
movement onset (P0) and a post-motor negativity (N100), with a central distribution (Fig. 5). 
633 
These components are reminiscent of movement-related cortical potentials (Shibasaki et al., 
634 
1980; Hallett, 1994), which might include steady-state movement-evoked potentials (Gerloff et 
635 
al., 1997) or readiness potentials (Kornhuber and Deecke, 1965; Vercillo et al., 2018) (see also 
636 
body-part-specific analyses, and Fig. 6). The pattern closely mirrors the regression weights 
637 
observed in our TRF model of self-generated movements (Fig. 3b). Notably, the amplitude of 
638 
the ERPs associated with self-generated movements was larger during relatively faster, as 
639 
opposed to relatively slower movements, a pattern previously suggested to reflect increased 
640 
motor activity during higher-rate movement execution (Brunia et al., 2011). These results 
641 
JNeurosci Accepted Manuscript

## Page 21

20 
 
suggest that the mTRF model effectively captured EEG potentials traditionally linked to motor 
642 
control, with amplitudes modulated by movement speed. 
643 
(III) Visual perception of partner’s body movements (other-generated). When the 
644 
participants could see each other, the observed partner-generated movements elicited 
645 
biphasic responses in occipital regions, characterized by a positive peak at ~70 ms (P70) and 
646 
a negative peak at ~160 ms (N160) (Fig. 5). This pattern resembles traditional visual responses 
647 
to biological motion, notably characterized by the N170 component, typically observed around 
648 
170 ms post-movement onset (Kubová et al., 1995; Bach and Ullrich, 1997; Puce et al., 2000; 
649 
Jokisch et al., 2005). Similar to the responses associated with music and self-generated 
650 
movements, these ERPs closely align with the regression weights yielded by the TRF model 
651 
of other-generated movements (Fig. 3b). As for ERPs evoked by motor control (previous 
652 
section), ERP amplitudes scaled with movement speed, most prominently under visual contact 
653 
in the different-music condition (by contrast, the modulation in the same-music condition was 
654 
less apparent, likely obscured by concurrent neural processes not considered in the ERP 
655 
analysis, such as those related to coordination). The increased ERP amplitudes for faster 
656 
compared to slower movements (Fig. 5) further highlight a well-established physiological 
657 
property of sensory ERPs: their sensitivity to variations in stimulus intensity (Somervail et al., 
658 
2021). 
659 
(IV) Social coordination. ERPs time-locked to changes in social coordination were associated 
660 
with quadriphasic EEG modulations in occipital regions across all conditions. However, ERP 
661 
amplitude differences between changes to in-phase vs anti-phase coordination emerged only 
662 
when participants could see their partners and listened to same-tempo music (Fig. 5). The 
663 
response pattern appears to bridge motor control and movement observation processes, 
664 
showing a triphasic N-P-N sequence, similar to self-generated movement ERPs, followed by 
665 
a positive occipital peak at 160 ms post-onset—resembling the inverted polarity of the posterior 
666 
N160 observed for other-generated movements. The presence of a clear pattern in non-visual 
667 
conditions suggests that these ERPs partially reflect motor activity, as changes in coordination 
668 
coincide with movement initiation by either the self or the partner, a confound that traditional 
669 
ERP analysis fails to fully resolve, unlike TRF analysis. Supporting this interpretation, ERP 
670 
amplitude in non-visual conditions did not vary between changes to in-phase and anti-phase 
671 
(Fig. 5), and the TRFs—designed to disentangle concurrent processes—did not reveal any 
672 
EEG activity related to coordination, beyond motor activity, in the non-visual conditions (Fig. 
673 
3b). 
674 
mTRFs tease apart body-part-specific motor activity 
675 
JNeurosci Accepted Manuscript

## Page 22

21 
 
Thus far, the EEG activity related to self-generated movements was extracted using the 
676 
velocity time-series of bounce movements (see Methods), either to predict EEG signal (mTRF 
677 
analysis) or to time-lock EEG epochs (ERP analysis). To determine whether specific body 
678 
parts contribute to distinct motor activities, we performed an additional TRF analysis using 
679 
velocity time series associated with five distinct body parts: left and right hands, left and right 
680 
feet, and head. Rather than relying on principal movements extracted from PCA, we modeled 
681 
EEG signals using the kinematics of these specific body parts as input variables in the TRF 
682 
models (Fig. 6). The unique contributions of the left and right hands (beyond that of all other 
683 
body parts) to the EEG prediction exhibited lateralized spatial maps at central sites (Fig. 6a), 
684 
a typical marker of hands’ motor control (Kornhuber and Deecke, 1965; Deecke et al., 1969; 
685 
Shibasaki et al., 1980; Gerloff et al., 1997; Smulders and Miller, 2011; Vercillo et al., 2018; 
686 
O’Neill et al., 2024). Furthermore, feet movements exhibited a more posterior topographical 
687 
activation than hands (Fig. 6b), reminiscent of EEG differences found when comparing motor 
688 
activity across hands and feet (Brunia et al., 2011). Notably, these feet-related EEG activities 
689 
showed no clear lateralization, which is expected given the organization of the motor cortex 
690 
(Gordon et al., 2023; O’Neill et al., 2024) and the limited spatial resolution of EEG (Osman et 
691 
al., 2005). Indeed, as the feet are represented in the deeper, more central regions of the motor 
692 
cortex, along the inner surface of the longitudinal fissure, it is notoriously difficult to differentiate 
693 
EEG activity evoked by left vs. right foot movements (Osman et al., 2005; Jensen et al., 2023). 
694 
Finally, head movements were associated with EEG activity not only in motor sites, such as 
695 
C3 and C4 electrodes but also in occipital regions (Fig. 6c). Importantly, this occipital activation 
696 
did not result from neck muscle artifact leakage, as neck EMG’s contribution was already 
697 
accounted for in the full model (see Methods). Moreover, no such occipital activation was found 
698 
for hand or foot movements, suggesting that head movements specifically involve visual 
699 
(besides motor) processing. Visual processes could be at play when moving the head (e.g., 
700 
bouncing or head bobbing) as this involves salient changes in the field of view. Taken together, 
701 
these findings support the conclusion that our TRF and ERP analyses (see Figs. 3 and 5) 
702 
efficiently isolated neural processes related to self-generated movements. Moreover, beyond 
703 
validating these prior results, this new analysis demonstrates the feasibility of isolating motor 
704 
activity of specific body parts (note that in the prior analyses, motor activity related to bounce 
705 
[involving all body parts] was assessed, limiting visibility into body-part-specific motor activity).  
706 
Social coordination encoding acts beyond self and other 
707 
Coordination beyond self and other. In previous analyses, we demonstrated that adding the 
708 
social coordination variable to models including music, self-, and other-generated movements 
709 
yielded a gain in EEG prediction, suggesting neural encoding of coordination (Figs. 3 and 4). 
710 
JNeurosci Accepted Manuscript

## Page 23

22 
 
To ensure this gain was not solely attributed to the inclusion of spatial direction features – i.e., 
711 
up versus down phases of bounce movement inherent in the social coordination variable but 
712 
absent in the self- and other-generated movement variables – we conducted a supplementary 
713 
mTRF analysis that included the spatial directions of both self- and other-generated 
714 
movements. This analysis yielded cross-condition differences in unique contributions (i.e., Δr) 
715 
that were identical to those observed in our primary analysis (compare Fig. 7a, top, with Figs. 
716 
3a and 4), along with consistent model weights (compare Fig. 7a, bottom, with Fig. 3b). These 
717 
findings indicate that the encoding of social coordination extends beyond merely representing 
718 
the spatial directions of self- and other-generated movements in isolation. These results further 
719 
suggest that the encoding of coordination is not merely driven by a modulation of the partner-
720 
evoked visual processes as a function of whether the self is moving congruently or not 
721 
congruently with the partner (hence suppressing or amplifying the observed movements 
722 
relative to the field of view). To further show that the encoding of coordination was not solely 
723 
capturing this, we conducted an additional control analysis for which we re-referenced the 
724 
other-generated movements to the position of the self. Even following such re-referencing, 
725 
social coordination yielded a significant and unique contribution to EEG recorded from occipital 
726 
sites, and this contribution was most pronounced under conditions of visual contact and shared 
727 
music. Taken together, these findings indicate that the reported encoding of coordination is 
728 
linked to a high-order process tracking the alignment between self- and partner-related 
729 
movements, independently of the encoding of self and other taken alone. 
730 
Coordination ERPs are time-locked to other-generated movements. “Coordination ERPs” were 
731 
extracted by epoching EEG time-series to shifts from anti-phase to in-phase coordination and, 
732 
vice versa, from in-phase to anti-phase. Here we investigated how such ERPs changed as a 
733 
function of whether the shifts were driven by changes in movement direction produced by 
734 
either the self (movement production) or the other (movement observation) (see Methods). 
735 
Our analysis indicated that the EEG modulations previously associated with changes to in-
736 
phase coordination, specifically observed at occipital sites (Oz) and specifically under 
737 
conditions of visual contact and same-tempo music (Fig. 5), were present only when these 
738 
changes were time-locked to other-generated movement changes (Fig. 7b). This indicates that 
739 
larger amplitude ERPs are evoked when a partner initiates a change in movement direction 
740 
that leads to in-phase coordination compared to a change in movement direction that leads to 
741 
anti-phase coordination. This result further strengthens the conclusion that the brain encodes 
742 
social coordination and that this encoding is specifically driven by movements of the partner 
743 
being in phase vs. anti-phase concerning self-initiated movements. 
744 
Discussion 
745 
JNeurosci Accepted Manuscript

## Page 24

23 
 
This study demonstrates that the neural processes underlying dance—a complex, natural, and 
746 
social behavior—can be effectively isolated from EEG signals recorded from dyads dancing 
747 
together. Using multivariate TRF models applied to dual EEG and full-body kinematics, we 
748 
disentangled intertwined neural processes, separated them from movement artifacts, and 
749 
confirmed their physiological origins through ERP analyses. This approach delineated sensory 
750 
and motor processes underlying free-form, naturalistic dance: (I) auditory tracking of music, 
751 
(II) control of self-generated movements, and (III) visual monitoring of partner-generated 
752 
movements. Crucially, we also uncovered a previously unknown neural marker of social 
753 
processing: (IV) visual encoding of social coordination, which emerges only when partners can 
754 
make visual contact, is topographically distributed over the occipital areas, and is driven by 
755 
movement observation rather than initiation. Additionally, movement-specific models 
756 
highlighted “bounce” as the primary dance move driving EEG activity associated with both self-
757 
generated movements and movements observed in the partner. Together, these findings 
758 
illustrate how advanced neural analysis techniques can illuminate the mechanisms supporting 
759 
complex natural behaviors. 
760 
mTRFs can unravel the complex orchestration of natural behavior 
761 
Recent advancements in mobile imaging and de-noising techniques have enhanced our ability 
762 
to study neural activity during real-world behavior (Bateson et al., 2017; Niso et al., 2023). 
763 
However, disentangling the contribution of the multiple simultaneous neural processes 
764 
remains challenging. In this study, we addressed this challenge within the context of a 
765 
spontaneous, interactive, yet controlled task, balancing ecological validity with experimental 
766 
control (D’Ausilio et al., 2015). Using mTRFs, we successfully isolated four distinct, yet 
767 
overlapping, neural processes underlying dyadic dance.  ERP analyses confirmed that mTRF 
768 
modeled responses, or model weights, align with well-characterized EEG potentials linked to 
769 
sensory perception and motor control. This result suggests that mTRFs can capture 
770 
physiologically established signals, akin to ERP analyses, but in real-world scenarios with 
771 
multiple concurrent activities—contexts where traditional ERP approaches fall short. 
772 
ERP analyses struggle to isolate the unique contributions of individual processes amidst 
773 
overlapping neural activities. This limitation is evident in our results: visual ERP modulation to 
774 
movement speed was weak under visual contact and same-music conditions (Fig. 5), while 
775 
mTRFs captured robust visual tracking (Figs. 3 and 4). This discrepancy likely stems from 
776 
social coordination activity, which ERP analysis cannot disentangle, and which was particularly 
777 
prominent in these conditions. Similarly, coordination ERPs appeared in non-visual conditions 
778 
(Fig. 5), whereas mTRFs showed no corresponding activity, likely reflecting unaccounted self-
779 
JNeurosci Accepted Manuscript

## Page 25

24 
 
motor contributions in ERP analyses. Although techniques like frequency tagging have 
780 
addressed some of these challenges (Varlet et al., 2020, 2023; Cracco et al., 2022), they are 
781 
limited to identifying periodic EEG responses and typically focus on univariate kinematics (e.g., 
782 
gait cycles or hand trajectories). In contrast, mTRFs offer a precise characterization of neural 
783 
responses to diverse features, effectively separating them from concurrent activities. 
784 
The interplay between music and partner tracking 
785 
Dyadic dance requires simultaneous sensory processing of music and a partner’s movements, 
786 
both of which contribute to coordinated behavior (Bigand et al., 2024). To what extent do these 
787 
concurrent streams of information influence EEG activity, and how are these effects modulated 
788 
by social factors like visual contact? Our findings show that model weights and ERPs 
789 
associated with music, partner movements, and coordination exhibit similar amplitude, 
790 
suggesting that each element—whether a musical sound, observed movement, or change in 
791 
coordination—elicits an EEG response of comparable magnitude. Notably, visual processes 
792 
accounted for less variance at occipital sites than auditory processes at frontal sites (see Δr 
793 
scales in Fig. 3a). This may reflect the broader range of EEG signals in occipital regions, which 
794 
likely include visual processing of not only partner movements but also other visual cues and, 
795 
importantly, artifactual leakage from neck movements (see Fig. 3a). 
796 
In visual-contact conditions, where both music (acoustic) and partner (visual) information were 
797 
present, we observed a decrease in music tracking (Fig. 4). This reduction may arise from 
798 
competition between visual and auditory modalities for attentional resources (Woods et al., 
799 
1992; Lavie, 2005; Molloy et al., 2015), especially in naturalistic dance, where both auditory 
800 
and visual inputs drive coordination (Bigand et al., 2024). Naturalistic dance likely places 
801 
heightened demands on visual input, as recent findings suggest that visual drivers dominate 
802 
full-body rhythmic synchronization—a phenomenon not observed in simpler tasks like finger 
803 
tapping (Nguyen et al., 2024).  
804 
Movement control and observation 
805 
Our principal component analysis of dance kinematics revealed that bounce movements 
806 
accounted for most EEG activity associated with self-generated movements (Fig. 2). 
807 
Intriguingly, these movements predicted EEG activity not only over motor areas (e.g., 
808 
electrodes C3 and C4), but also at occipital sites (Fig. 3a). To better understand these 
809 
activities, we further dissected the components of bounce control, pinpointing motor activity 
810 
specific to different body parts (Fig. 6). In participants engaged in free-form dancing, we 
811 
successfully replicated established EEG findings observed during isolated movements, with 
812 
JNeurosci Accepted Manuscript

## Page 26

25 
 
more posterior-medial activity associated with foot movements and more central-lateralized 
813 
activity for hand movements (Brunia et al., 2011). Notably, our analysis showed that head 
814 
displacement was linked to occipital brain activity in addition to central motor activity, likely due 
815 
to visual responses resulting from changes in the visual field (Testard et al., 2024). This 
816 
analysis clarifies why the main mTRF for self-generated bounce movements included activity 
817 
at occipital sites (Fig. 3a), suggesting that bouncing not only involves motor activity but also 
818 
induces significant visual changes. 
819 
Bounce also emerged as the movement most predictive of EEG activity linked to visual tracking 
820 
of a partner’s movements. This finding raises an intriguing question: what makes bounce 
821 
particularly captivating compared to other dance movements? Our previous research has 
822 
highlighted bounce’s key role in fostering interpersonal coordination (Bigand et al., 2024), 
823 
serving as a supramodal (audio-visual) pace-setter between participants and their partners. 
824 
This may explain why bounce is so prominent in predicting EEG activity associated with 
825 
movement observation. This finding also suggests that EEG signals are particularly sensitive 
826 
to salient movement changes, rather than merely high-amplitude movements. Indeed, while 
827 
bounce explained less than 1% of the total kinematic variance (ranking 10th in the PCA), it 
828 
accounted for over 80% of the EEG variance. This likely reflects bounce’s heightened salience, 
829 
possibly driven by the fact that this movement was the only one peaking sharply with each 
830 
musical beat (Bigand et al., 2024). 
831 
Encoding of social coordination 
832 
Our study reveals that coordination between self- and other-generated movements uniquely 
833 
predicts EEG signals recorded at occipital electrodes. Recent research in social neuroscience 
834 
has shown that EEG can delineate separate components supporting coordinated behaviors: 
835 
some monitor self- and partner-generated actions distinctly, while others integrate the joint 
836 
action outcome produced by oneself and the partner (Novembre et al., 2016; Varlet et al., 
837 
2020). In line with this, we identified three distinct neural processes—control of one’s own 
838 
movements, observation of a partner’s movements, and processing of social coordination (Fig. 
839 
3)—and observed heightened coordination tracking in conditions where musical synchrony 
840 
between participants was greater. Importantly, our findings suggest that the encoding of 
841 
coordination does not merely combine the individual “self” and “other” processes; rather, it 
842 
captures a distinct neural representation of their coordination (see Results and Fig. 7a).  
843 
The temporal response underlying social coordination tracking integrates both motor control 
844 
(self) and movement observation (other), as evidenced by the N-P-N pattern and a subsequent 
845 
JNeurosci Accepted Manuscript

## Page 27

26 
 
modulation peaking around 160 ms. Notably, this response appears to be triggered by 
846 
observing a partner’s movements, rather than initiating one’s own actions. ERPs associated 
847 
with changes in the partner’s movements—rather than self-initiated actions—were modulated 
848 
by social coordination at visual sites (see Results and Fig. 7b). This finding suggests that 
849 
neural tracking of coordination is more reliant on visual monitoring of the partner than on the 
850 
internal control of one’s own movements, aligning with earlier observations that this process is 
851 
localized in visual areas and enhanced during visual contact. 
852 
In summary, we identified a previously unknown neural marker of social processing, with five 
853 
key observations: 1) it is topographically distributed over the occipital areas; 2) it emerges 
854 
when participants can see each other and is most pronounced when musical synchrony 
855 
between them is high; 3) its underlying neural signal integrates components from both self and 
856 
other processes; yet 4) rather than merely combining the individual “self” and “other” 
857 
components, it represents a distinct neural encoding of their coordination; and 5) it is primarily 
858 
anchored to movement observation, not movement initiation. 
859 
Bridging traditional physiology with real-world applications 
860 
Our findings show that neurophysiological signals, traditionally examined in controlled settings, 
861 
can be disentangled and analyzed within real-world contexts. This highlights the potential for 
862 
future research to incorporate ecologically valid stimuli and behavioral predictors (e.g., body 
863 
movements, eye gaze, speech) into multivariate modeling. Such an approach could deepen 
864 
our understanding of brain processes during live social interactions—a field of growing 
865 
significance across human adult (Dumas et al., 2010; Pan et al., 2018; Koul et al., 2023; Cross 
866 
et al., 2024; Orgs et al., 2024), developmental (Wass et al., 2018, 2020; Nguyen et al., 2020, 
867 
2021, 2023) and animal studies (Zhang and Yartsev, 2019; Rose et al., 2021; Yang et al., 
868 
2021). 
869 
References 
870 
Bach M, Ullrich D (1997) Contrast dependency of motion-onset and pattern-reversal VEPs: 
871 
Interaction of stimulus type, recording site and response component. Vision Research 
872 
37:1845–1849. 
873 
Barraza P, Dumas G, Liu H, Blanco-Gomez G, van den Heuvel MI, Baart M, Pérez A (2019) 
874 
Implementing EEG hyperscanning setups. MethodsX 6:428–436. 
875 
JNeurosci Accepted Manuscript

## Page 28

27 
 
Bateson AD, Baseler HA, Paulson KS, Ahmed F, Asghar AUR (2017) Categorisation of 
876 
Mobile EEG: A Researcher’s Perspective. BioMed Research International 2017:5496196. 
877 
Bianco R, Zuk NJ, Bigand F, Quarta E, Grasso S, Arnese F, Ravignani A, Battaglia-Mayer A, 
878 
Novembre G (2024) Neural encoding of musical expectations in a non-human primate. 
879 
Current Biology 34:444-450.e5. 
880 
Bigand F, Bianco R, Abalde SF, Novembre G (2024) The geometry of interpersonal 
881 
synchrony in human dance. Current Biology 0 Available at: https://www.cell.com/current-
882 
biology/abstract/S0960-9822(24)00698-5 [Accessed June 25, 2024]. 
883 
Bigand F, Prigent E, Berret B, Braffort A (2021) Decomposing spontaneous sign language 
884 
into elementary movements: A principal component analysis-based approach. PLOS ONE 
885 
16:e0259464. 
886 
Brunia CHM, van Boxtel GJM, Böcker KBE (2011) Negative Slow Waves as Indices of 
887 
Anticipation: The Bereitschaftspotential, the Contingent Negative Variation, and the 
888 
Stimulus-Preceding Negativity. In: The Oxford Handbook of Event-Related Potential 
889 
Components (Kappenman ES, Luck SJ, eds), pp 0. Oxford University Press. Available at: 
890 
https://doi.org/10.1093/oxfordhb/9780195374148.013.0108 [Accessed May 16, 2024]. 
891 
Cracco E, Lee H, van Belle G, Quenon L, Haggard P, Rossion B, Orgs G (2022) EEG 
892 
Frequency Tagging Reveals the Integration of Form and Motion Cues into the Perception 
893 
of Group Movement. Cerebral Cortex 32:2843–2857. 
894 
Croft RJ, Barry RJ (2000) Removal of ocular artifact from the EEG: a review. 
895 
Neurophysiologie Clinique/Clinical Neurophysiology 30:5–19. 
896 
Cross ES, Darda KM, Moffat R, Muñoz L, Humphries S, Kirsch LP (2024) Mutual gaze and 
897 
movement synchrony boost observers’ enjoyment and perception of togetherness when 
898 
watching dance duets. Sci Rep 14:24004. 
899 
JNeurosci Accepted Manuscript

## Page 29

28 
 
Crosse MJ, Di Liberto GM, Bednar A, Lalor EC (2016) The Multivariate Temporal Response 
900 
Function (mTRF) Toolbox: A MATLAB Toolbox for Relating Neural Signals to Continuous 
901 
Stimuli. Front Hum Neurosci 10 Available at: 
902 
https://www.frontiersin.org/articles/10.3389/fnhum.2016.00604 [Accessed May 16, 2024]. 
903 
Daffertshofer A, Lamoth CJC, Meijer OG, Beek PJ (2004) PCA in studying coordination and 
904 
variability: a tutorial. Clinical Biomechanics 19:415–428. 
905 
D’Ausilio A, Novembre G, Fadiga L, Keller PE (2015) What can music tell us about social 
906 
interaction? Trends in Cognitive Sciences 19:111–114. 
907 
Deecke L, Scheid P, Kornhuber HH (1969) Distribution of readiness potential, pre-motion 
908 
positivity, and motor potential of the human cerebral cortex preceding voluntary finger 
909 
movements. Exp Brain Res 7:158–168. 
910 
Delorme A, Makeig S (2004) EEGLAB: an open source toolbox for analysis of single-trial 
911 
EEG dynamics including independent component analysis. Journal of Neuroscience 
912 
Methods 134:9–21. 
913 
Desai M, Field AM, Hamilton LS (2024) A comparison of EEG encoding models using 
914 
audiovisual stimuli and their unimodal counterparts. PLOS Computational Biology 
915 
20:e1012433. 
916 
Di Liberto GM, Barsotti M, Vecchiato G, Ambeck-Madsen J, Del Vecchio M, Avanzini P, 
917 
Ascari L (2021) Robust anticipation of continuous steering actions from 
918 
electroencephalographic data during simulated driving. Sci Rep 11:23383. 
919 
Di Liberto GM, Lalor EC (2017) Indexing cortical entrainment to natural speech at the 
920 
phonemic level: Methodological considerations for applied research. Hearing Research 
921 
348:70–77. 
922 
Di Liberto GM, O’Sullivan JA, Lalor EC (2015) Low-Frequency Cortical Entrainment to 
923 
Speech Reflects Phoneme-Level Processing. Current Biology 25:2457–2465. 
924 
JNeurosci Accepted Manuscript

## Page 30

29 
 
Di Liberto GM, Pelofi C, Bianco R, Patel P, Mehta AD, Herrero JL, de Cheveigné A, Shamma 
925 
S, Mesgarani N (2020) Cortical encoding of melodic expectations in human temporal 
926 
cortex Peelle JE, Shinn-Cunningham BG, eds. eLife 9:e51784. 
927 
Dumas G, Nadel J, Soussignan R, Martinerie J, Garnero L (2010) Inter-Brain 
928 
Synchronization during Social Interaction. PLOS ONE 5:e12166. 
929 
Dunbar RI (2012) On the evolutionary function of song and dance. Music, language, and 
930 
human evolution:201–214. 
931 
Federolf P, Reid R, Gilgien M, Haugen P, Smith G (2014) The application of principal 
932 
component analysis to quantify technique in sports. Scandinavian Journal of Medicine & 
933 
Science in Sports 24:491–499. 
934 
Fiedler L, Wöstmann M, Herbst SK, Obleser J (2019) Late cortical tracking of ignored speech 
935 
facilitates neural selectivity in acoustically challenging conditions. NeuroImage 186:33–42. 
936 
Foster Vander Elst O, Foster NHD, Vuust P, Keller PE, Kringelbach ML (2023) The 
937 
Neuroscience of Dance: A Conceptual Framework and Systematic Review. Neuroscience 
938 
& Biobehavioral Reviews 150:105197. 
939 
Gerloff C, Toro C, Uenishi N, Cohen LG, Leocani L, Hallett M (1997) Steady-state 
940 
movement-related cortical potentials: a new approach to assessing cortical activity 
941 
associated with fast repetitive finger movements. Electroencephalography and Clinical 
942 
Neurophysiology 102:106–113. 
943 
Goncharova II, McFarland DJ, Vaughan TM, Wolpaw JR (2003) EMG contamination of EEG: 
944 
spectral and topographical characteristics. Clinical Neurophysiology 114:1580–1593. 
945 
Gordon EM et al. (2023) A somato-cognitive action network alternates with effector regions in 
946 
motor cortex. Nature 617:351–359. 
947 
JNeurosci Accepted Manuscript

## Page 31

30 
 
Hallett M (1994) Movement-related cortical potentials. Electromyogr Clin Neurophysiol 34:5–
948 
13. 
949 
Jensen MA, Huang H, Valencia GO, Klassen BT, van den Boom MA, Kaufmann TJ, Schalk 
950 
G, Brunner P, Worrell GA, Hermes D, Miller KJ (2023) A motor association area in the 
951 
depths of the central sulcus. Nat Neurosci 26:1165–1169. 
952 
Jessen S, Fiedler L, Münte TF, Obleser J (2019) Quantifying the individual auditory and 
953 
visual brain response in 7-month-old infants watching a brief cartoon movie. NeuroImage 
954 
202:116060. 
955 
Jokisch D, Daum I, Suchan B, Troje NF (2005) Structural encoding and recognition of 
956 
biological motion: evidence from event-related potentials and source analysis. Behavioural 
957 
Brain Research 157:195–204. 
958 
Kern P, Heilbron M, de Lange FP, Spaak E (2022) Cortical activity during naturalistic music 
959 
listening reflects short-range predictions based on long-term experience Obleser J, Büchel 
960 
C, Sedley W, Doelling K, eds. eLife 11:e80935. 
961 
Kornhuber HH, Deecke L (1965) Hirnpotentialänderungen bei Willkürbewegungen und 
962 
passiven Bewegungen des Menschen: Bereitschaftspotential und reafferente Potentiale. 
963 
Pflügers Arch 284:1–17. 
964 
Kothe CAE, Jung T-P (2016) Artifact removal techniques with signal reconstruction. Available 
965 
at: https://patents.google.com/patent/US20160113587A1/en [Accessed May 16, 2024]. 
966 
Koul A, Ahmar D, Iannetti GD, Novembre G (2023) Spontaneous dyadic behavior predicts 
967 
the emergence of interpersonal neural synchrony. NeuroImage 277:120233. 
968 
Kubová Z, Kuba M, Spekreijse H, Blakemore C (1995) Contrast dependence of motion-onset 
969 
and pattern-reversal evoked potentials. Vision Research 35:197–205. 
970 
JNeurosci Accepted Manuscript

## Page 32

31 
 
Lalor EC, Power AJ, Reilly RB, Foxe JJ (2009) Resolving Precise Temporal Processing 
971 
Properties of the Auditory System Using Continuous Stimuli. Journal of Neurophysiology 
972 
102:349–359. 
973 
Lanzarini F, Maranesi M, Rondoni EH, Albertini D, Ferretti E, Lanzilotto M, Micera S, 
974 
Mazzoni A, Bonini L (2025) Neuroethology of natural actions in freely moving monkeys. 
975 
Science 387:214–220. 
976 
Lavie N (2005) Distracted and confused?: Selective attention under load. Trends in Cognitive 
977 
Sciences 9:75–82. 
978 
Luck SJ (2014) An Introduction to the Event-Related Potential Technique, second edition. 
979 
MIT Press. 
980 
Mao D, Avila E, Caziot B, Laurens J, Dickman JD, Angelaki DE (2021) Spatial modulation of 
981 
hippocampal activity in freely moving macaques. Neuron 109:3521-3534.e6. 
982 
Maris E, Oostenveld R (2007) Nonparametric statistical testing of EEG- and MEG-data. 
983 
Journal of Neuroscience Methods 164:177–190. 
984 
Mithen SJ (2006) The Singing Neanderthals: The Origins of Music, Language, Mind, and 
985 
Body. Harvard University Press. 
986 
Molloy K, Griffiths TD, Chait M, Lavie N (2015) Inattentional Deafness: Visual Load Leads to 
987 
Time-Specific Suppression of Auditory Evoked Responses. J Neurosci 35:16046–16054. 
988 
Musall S, Kaufman MT, Juavinett AL, Gluf S, Churchland AK (2019) Single-trial neural 
989 
dynamics are dominated by richly varied movements. Nat Neurosci 22:1677–1686. 
990 
Nguyen T, Bánki A, Markova G, Hoehl S (2020) Chapter 1 - Studying parent-child interaction 
991 
with hyperscanning. In: Progress in Brain Research (Hunnius S, Meyer M, eds), pp 1–24 
992 
New Perspectives on Early Social-cognitive Development. Elsevier. Available at: 
993 
JNeurosci Accepted Manuscript

## Page 33

32 
 
https://www.sciencedirect.com/science/article/pii/S0079612320300455 [Accessed July 4, 
994 
2024]. 
995 
Nguyen T, Lagacé-Cusiac R, Everling JC, Henry MJ, Grahn JA (2024) Audiovisual 
996 
integration of rhythm in musicians and dancers. Atten Percept Psychophys 86:1400–1416. 
997 
Nguyen T, Reisner S, Lueger A, Wass SV, Hoehl S, Markova G (2023) Sing to me, baby: 
998 
Infants show neural tracking and rhythmic movements to live and dynamic maternal 
999 
singing. Developmental Cognitive Neuroscience 64:101313. 
1000 
Nguyen T, Schleihauf H, Kayhan E, Matthes D, Vrtička P, Hoehl S (2021) Neural synchrony 
1001 
in mother–child conversation: Exploring the role of conversation patterns. Social Cognitive 
1002 
and Affective Neuroscience 16:93–102. 
1003 
Niso G, Romero E, Moreau JT, Araujo A, Krol LR (2023) Wireless EEG: A survey of systems 
1004 
and studies. NeuroImage 269:119774. 
1005 
Novembre G, Pawar VM, Bufacchi RJ, Kilintari M, Srinivasan M, Rothwell JC, Haggard P, 
1006 
Iannetti GD (2018) Saliency Detection as a Reactive Process: Unexpected Sensory 
1007 
Events Evoke Corticomuscular Coupling. J Neurosci 38:2385–2397. 
1008 
Novembre G, Sammler D, Keller PE (2016) Neural alpha oscillations index the balance 
1009 
between self-other integration and segregation in real-time joint action. Neuropsychologia 
1010 
89:414–425. 
1011 
O’Neill GC, Seymour RA, Mellor S, Alexander N, Tierney TM, Bernachot L, Hnazaee MF, 
1012 
Spedden ME, Timms RC, Bush D, Bestmann S, Brookes MJ, Barnes GR (2024) 
1013 
Combining video telemetry and wearable MEG for naturalistic imaging. 
1014 
:2023.08.01.551482 Available at: 
1015 
https://www.biorxiv.org/content/10.1101/2023.08.01.551482v2 [Accessed December 16, 
1016 
2024]. 
1017 
JNeurosci Accepted Manuscript

## Page 34

33 
 
Oostenveld R, Fries P, Maris E, Schoffelen J-M (2011) FieldTrip: open source software for 
1018 
advanced analysis of MEG, EEG, and invasive electrophysiological data. Intell 
1019 
Neuroscience 2011:1:1-1:9. 
1020 
Orgs G, Vicary S, Sperling M, Richardson DC, Williams AL (2024) Movement synchrony 
1021 
among dance performers predicts brain synchrony among dance spectators. Sci Rep 
1022 
14:22079. 
1023 
Osman A, Müller K-M, Syre P, Russ B (2005) Paradoxical lateralization of brain potentials 
1024 
during imagined foot movements. Cognitive Brain Research 24:727–731. 
1025 
O’Sullivan AE, Crosse MJ, Di Liberto GM, Lalor EC (2017) Visual Cortical Entrainment to 
1026 
Motion and Categorical Speech Features during Silent Lipreading. Frontiers in Human 
1027 
Neuroscience 10 Available at: 
1028 
https://www.frontiersin.org/articles/10.3389/fnhum.2016.00679 [Accessed July 21, 2023]. 
1029 
Pan Y, Novembre G, Song B, Li X, Hu Y (2018) Interpersonal synchronization of inferior 
1030 
frontal cortices tracks social interactive learning of a song. NeuroImage 183:280–290. 
1031 
Pion-Tonachini L, Kreutz-Delgado K, Makeig S (2019) ICLabel: An automated 
1032 
electroencephalographic independent component classifier, dataset, and website. 
1033 
NeuroImage 198:181–197. 
1034 
Plöchl M, Ossandón JP, König P (2012) Combining EEG and eye tracking: identification, 
1035 
characterization, and correction of eye movement artifacts in electroencephalographic 
1036 
data. Frontiers in Human Neuroscience 6 Available at: 
1037 
https://www.readcube.com/articles/10.3389%2Ffnhum.2012.00278 [Accessed June 25, 
1038 
2024]. 
1039 
Puce A, Smith A, Allison T (2000) ERPS EVOKED BY VIEWING FACIAL MOVEMENTS. 
1040 
Cognitive Neuropsychology Available at: 
1041 
JNeurosci Accepted Manuscript

## Page 35

34 
 
https://www.tandfonline.com/doi/abs/10.1080/026432900380580 [Accessed May 16, 
1042 
2024]. 
1043 
Ramírez-Moreno MA, Cruz-Garza JG, Acharya A, Chatufale G, Witt W, Gelok D, Reza G, 
1044 
Contreras-Vidal JL (2023) Brain-to-brain communication during musical improvisation: a 
1045 
performance case study. F1000Res 11:989. 
1046 
Rose MC, Styr B, Schmid TA, Elie JE, Yartsev MM (2021) Cortical representation of group 
1047 
social communication in bats. Science 374:eaba9584. 
1048 
Shibasaki H, Barrett G, Halliday E, Halliday AM (1980) Components of the movement-related 
1049 
cortical potential and their scalp topography. Electroencephalography and Clinical 
1050 
Neurophysiology 49:213–226. 
1051 
Smulders FTY, Miller JO (2011) The Lateralized Readiness Potential. In: The Oxford 
1052 
Handbook of Event-Related Potential Components (Kappenman ES, Luck SJ, eds), pp 0. 
1053 
Oxford University Press. Available at: 
1054 
https://doi.org/10.1093/oxfordhb/9780195374148.013.0115 [Accessed May 16, 2024]. 
1055 
Somervail R, Zhang F, Novembre G, Bufacchi RJ, Guo Y, Crepaldi M, Hu L, Iannetti GD 
1056 
(2021) Waves of Change: Brain Sensitivity to Differential, not Absolute, Stimulus Intensity 
1057 
is Conserved Across Humans and Rats. Cerebral Cortex 31:949–960. 
1058 
Stangl M, Maoz SL, Suthana N (2023) Mobile cognition: imaging the human brain in the ‘real 
1059 
world.’ Nat Rev Neurosci 24:347–362. 
1060 
Stringer C, Pachitariu M, Steinmetz N, Reddy CB, Carandini M, Harris KD (2019) 
1061 
Spontaneous behaviors drive multidimensional, brainwide activity. Science 364:eaav7893. 
1062 
Testard C, Tremblay S, Parodi F, DiTullio RW, Acevedo-Ithier A, Gardiner KL, Kording K, 
1063 
Platt ML (2024) Neural signatures of natural behaviour in socializing macaques. Nature 
1064 
628:381–390. 
1065 
JNeurosci Accepted Manuscript

## Page 36

35 
 
Theofanopoulou C, Paez S, Huber D, Todd E, Ramírez-Moreno MA, Khaleghian B, Sánchez 
1066 
AM, Barceló L, Gand V, Contreras-Vidal JL (2024) Mobile brain imaging in butoh dancers: 
1067 
from rehearsals to public performance. BMC Neurosci 25:62. 
1068 
Toiviainen P, Luck G, Thompson MR (2010) Embodied Meter: Hierarchical Eigenmodes in 
1069 
Music-Induced Movement. Music Perception 28:59–70. 
1070 
Tremblay S, Testard C, DiTullio RW, Inchauspé J, Petrides M (2023) Neural cognitive signals 
1071 
during spontaneous movements in the macaque. Nat Neurosci 26:295–305. 
1072 
Troje NF (2002) Decomposing biological motion: A framework for analysis and synthesis of 
1073 
human gait patterns. Journal of Vision 2:2. 
1074 
Urigüen JA, Garcia-Zapirain B (2015) EEG artifact removal—state-of-the-art and guidelines. 
1075 
J Neural Eng 12:031001. 
1076 
Varlet M, Nozaradan S, Nijhuis P, Keller PE (2020) Neural tracking and integration of ‘self’ 
1077 
and ‘other’ in improvised interpersonal coordination. NeuroImage 206:116303. 
1078 
Varlet M, Nozaradan S, Schmidt RC, Keller PE (2023) Neural tracking of visual periodic 
1079 
motion. European Journal of Neuroscience 57:1081–1097. 
1080 
Vercillo T, O’Neil S, Jiang F (2018) Action–effect contingency modulates the readiness 
1081 
potential. NeuroImage 183:273–279. 
1082 
Wass SV, Noreika V, Georgieva S, Clackson K, Brightman L, Nutbrown R, Covarrubias LS, 
1083 
Leong V (2018) Parental neural responsivity to infants’ visual attention: How mature brains 
1084 
influence immature brains during social interaction. PLOS Biology 16:e2006328. 
1085 
Wass SV, Whitehorn M, Haresign IM, Phillips E, Leong V (2020) Interpersonal Neural 
1086 
Entrainment during Early Social Interaction. Trends in Cognitive Sciences 24:329–342. 
1087 
JNeurosci Accepted Manuscript

## Page 37

36 
 
Weineck K, Wen OX, Henry MJ (2022) Neural synchronization is strongest to the spectral 
1088 
flux of slow music and depends on familiarity and beat salience Jensen O, Shinn-
1089 
Cunningham BG, Zoefel B, eds. eLife 11:e75515. 
1090 
Woods DL, Alho K, Algazi A (1992) Intermodal selective attention. I. Effects on event-related 
1091 
potentials to lateralized auditory and visual stimuli. Electroencephalography and Clinical 
1092 
Neurophysiology 82:341–355. 
1093 
Yan Y, Goodman JM, Moore DD, Solla SA, Bensmaia SJ (2020) Unexpected complexity of 
1094 
everyday manual behaviors. Nat Commun 11:3564. 
1095 
Yang Y et al. (2021) Wireless multilateral devices for optogenetic studies of individual and 
1096 
social behaviors. Nat Neurosci 24:1035–1045. 
1097 
Zhang W, Yartsev MM (2019) Correlated Neural Activity across the Brains of Socially 
1098 
Interacting Bats. Cell 178:413-428.e22. 
1099 
 
1100 
Figure legends 
1101 
Figure 1. Experimental materials and methods. a, Experimental setup. We applied the 
1102 
mTRF method to a previously collected dataset (Bigand et al., 2024) for which dyads of 
1103 
participants 
danced 
spontaneously 
in 
response 
to 
music 
while 
we 
recorded 
1104 
electroencephalography (EEG, 64 channels), electrooculography (EOG), electromyography 
1105 
(EMG, from neck and face muscles), and 3D full-body kinematics (22 markers). b, 
1106 
Experimental design. Data were collected under the experimental conditions of the original 
1107 
study, which utilized a 2x2 factorial design. The two manipulated factors were musical input 
1108 
(whether participants listened to the same or different music presented through earphones) 
1109 
and visual contact (whether participants could see or not see each other). c, Overview of the 
1110 
modeling paradigm. We estimated multivariate Temporal Response Functions (mTRFs), which 
1111 
learned the optimal linear mapping between the set of variables of interest (here music, self- 
1112 
and other-generated movements, social coordination, as well as other control variables (not 
1113 
shown) such as ocular, facial and neck muscle activity) and the EEG data. d, Model 
1114 
comparisons. To assess the unique contribution of each variable (regressor) to the EEG data, 
1115 
we trained reduced models encompassing all variables apart from the specified one. The 
1116 
JNeurosci Accepted Manuscript

## Page 38

37 
 
difference in prediction accuracy between the reduced and full model (encompassing all 
1117 
variables), denoted Δr, yields the unique contribution of this variable. 
1118 
Figure 2. Neural encoding of self- and other-related movements across different 
1119 
principal movements (PMs). Bars represent the unique contribution (Δr) of each PM (grand-
1120 
average) to the EEG signal recorded from the self (electrode Cz) or the other (electrode Oz). 
1121 
Δr values represent the difference in EEG prediction accuracy between the PM-specific 
1122 
reduced models and the full model, for self- and other-generated movements, respectively. 
1123 
Error bars represent ±1 standard error mean (SEM). Gray circle diagrams illustrate the 
1124 
proportion (%) of kinematic variance explained by each PM, with the first 15 PMs accounting 
1125 
for more than 95% of the total variance. Together, these results indicate that bounce (PM10) 
1126 
was the strongest predictor of EEG activity, whether self-generated or observed in others, 
1127 
despite accounting for only ~1% of kinematic variance. 
1128 
Figure 3. Distinct EEG activities related to music, self- and other-generated movements, 
1129 
social coordination, and muscle artifacts. a, Topographical maps of the unique contribution 
1130 
of each model variable to the predicted EEG. Δr topographical maps represent the grand-
1131 
average difference in EEG prediction accuracy between the reduced models (excluding the 
1132 
variable of interest) and the full model (including all four variables, plus ocular, facial, and neck 
1133 
muscle activity; see Fig. 1d), for each EEG electrode and experimental condition. b, Ridge 
1134 
regression weights for TRFs corresponding to music (Fz), self-generated movements 
1135 
(averaged across C3, C4), other-generated movements (Oz), social coordination (Oz), and 
1136 
ocular (F8), facial (T8), and neck (Oz) muscle activity for the full-model TRF. Grand-average 
1137 
weights are shown. Shaded areas represent ±1 SEM. 
1138 
Figure 4. Comparison of unique contributions across experimental conditions. Bars 
1139 
indicate the grand-average unique contributions (averaged over electrodes showing a gain; Δr 
1140 
>0) of each model variable, across conditions. Error bars represent ±1 SEM. Stars indicate 
1141 
significant main effects of visual contact and musical input, as well as the interaction between 
1142 
the two factors (2x2 repeated measures ANOVA, Bonferroni-corrected; *pbonf<.05, **pbonf<.01, 
1143 
***pbonf<.001).  
1144 
Figure 5. Event-related potential (ERP) analysis. ERPs evoked by salient changes in music, 
1145 
self-generated movements, other-generated movements, and social coordination. EEG time-
1146 
series were epoched to peaks of spectral flux for music, peaks of velocity magnitude for self- 
1147 
and other-generated movements, and changes between in-phase and anti-phase for social 
1148 
coordination. ERPs amplitudes were compared across two groups of epochs within each 
1149 
variable: loud vs. soft sounds for music (Fz), fast vs. slow movements for self- (averaged 
1150 
JNeurosci Accepted Manuscript

## Page 39

38 
 
across C3, C4) and other- (Oz) generated movements, and changes to in-phase vs. to anti-
1151 
phase for social coordination (Oz). Grand-average ERPs are shown for the two groups of 
1152 
epochs within each variable and across all experimental conditions. Colored shaded areas 
1153 
represent ±1 SEM, while grey shaded regions highlight significant differences in ERP 
1154 
amplitude between groups of epochs at a given time point (permutation test over time, at the 
1155 
electrode of interest, cluster-corrected). Topographical maps display amplitude differences 
1156 
across electrodes within the time windows of identified clusters. 
1157 
Figure 6. mTRFs tease apart body-part-specific motor activity. a, Topographical maps of 
1158 
the unique contribution of (self-generated) left- and right-hand movements to the predicted 
1159 
EEG. Δr topographical maps represent the grand-average difference in EEG prediction 
1160 
accuracy between the reduced models (excluding the body part of interest) and the full model 
1161 
(including all body parts, plus the neck control variable), for each EEG electrode and across 
1162 
all trials, regardless of experimental condition. We ran the TRF models without considering 
1163 
experimental conditions, given that no statistical difference was found across conditions in our 
1164 
main analysis (see Fig. 4). Separate TRF models for hands were derived by excluding each 
1165 
marker (‘L Hand’ or ‘R Hand’) from the full model. b, Same as (a), but for left- and right-foot 
1166 
movements. Separate TRF models for feet were derived by excluding each marker (‘L Foot’ 
1167 
or ‘R Foot’) from the full model. c, Same as (a) and (b), but for head movements. The head 
1168 
TRF model was derived by excluding all four head markers together. 
1169 
Figure 7. Tracking of social coordination beyond self and other. a, Results of the mTRF 
1170 
models associated with social coordination, incorporating spatial directions of self- and other-
1171 
generated movements. Top: Social coordination uniquely predicted EEG activity at similar 
1172 
electrode sites than in the main analysis (Fig. 3a). Statistics revealed the exact same 
1173 
differences in unique contribution as observed in our main analysis (Fig. 4). Bottom: TRF 
1174 
regression weights exhibited similar patterns as in the main analysis (Fig. 3b). b, Coordination-
1175 
related ERPs time-locked to self-generated (top) or other-generated (bottom) movement 
1176 
changes, at electrode Oz. ERPs related to changes to in-phase and anti-phase coordination 
1177 
are represented by continuous and dashed lines, respectively. Grand-average ERPs are 
1178 
shown for the two groups of trials associated with each variable across all experimental 
1179 
conditions. Colored shaded areas represent ±1 SEM, while grey shaded regions highlight 
1180 
significant differences in ERP amplitude between groups of trials at a given time point 
1181 
(permutation test over time, at Oz, cluster-corrected). Topographical maps display amplitude 
1182 
differences across electrodes within the time windows of identified clusters. 
1183 
Multimedia 
1184 
JNeurosci Accepted Manuscript

## Page 40

39 
 
Video 1. The principal (dance) movements, related to Fig. 2 
1185 
Video showing original movement data (left) and their decomposition into 15 principal 
1186 
movements (PMs) explaining >95% of the kinematics variance (right). Representative data are 
1187 
displayed (excerpt from a single trial, corresponding to when participants listened to the full 
1188 
refrain of the song). For the sake of clarity, the PMs are animated with different levels of 
1189 
exaggeration (i.e. the PM scores were amplified by a factor of 1.5 (PM3), 2 (PM4,7,9,11,15), 
1190 
3 (PM8), or not amplified (all other PMs)). The PMs are reminiscent of common dance moves 
1191 
(spelled out in italics). 
1192 
 
1193 
JNeurosci Accepted Manuscript

## Page 41

JNeurosci Accepted Manuscript

## Page 42

JNeurosci Accepted Manuscript

## Page 43

JNeurosci Accepted Manuscript

## Page 44

JNeurosci Accepted Manuscript

## Page 45

JNeurosci Accepted Manuscript

## Page 46

JNeurosci Accepted Manuscript

## Page 47

JNeurosci Accepted Manuscript

## Page 48

JNeurosci Accepted Manuscript

