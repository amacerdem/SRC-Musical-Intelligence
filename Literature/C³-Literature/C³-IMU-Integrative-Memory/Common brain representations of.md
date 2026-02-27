# Common brain representations of

**Year:** D:20

---

Common brain representations of
action and perception investigated
with cross-modal classification of
newly learned melodies
Yu-Hsin Fiona Chang1,2, Fredrik Ullén1,2,3 & Örjan de Manzano1,2,3
An important feature of human cognition is the ability to predict sensory outcomes of motor actions
and infer actions from sensory information – a process enabled by action-perception coupling. Through repeated and consistent sensory feedback, bidirectional sensorimotor associations can
become highly automatic with experience. In musicians, for instance, auditory cortex activity can
increase spontaneously even when observing piano playing without auditory feedback. A key question
is whether such associations rely on shared neural representations, or a “common code”, between
actions and their sensory outcomes. To test this, we trained non-musicians to play two melodies with
different pitch sequences on the piano. The following day, they underwent an fMRI experiment with
an MR-compatible piano while (a) playing the trained melodies without auditory feedback but imagining
the sound, and (b) listening to the same melodies without playing but imagining the finger movements. Within-condition multivariate pattern analyses revealed that patterns of activity in auditory-motor
regions represent pitch sequences. Importantly, cross-modal classification showed that these patterns
generalized across conditions in the right premotor cortex, indicating the emergence of a common
code across perception and action. Keywords  Action-perception coupling, fMRI, Music perception, MVPA, Sequence learning
Motor actions are often associated with sensory consequences that we learn to anticipate. For example, when
learning to play the piano, we become familiar with the sounds that result from pressing down different piano
keys. The process of establishing such associations between actions and their sensory outcomes is referred to
as action-perception coupling1. A long-standing question in cognitive neuroscience is how our brain performs
such sensorimotor integration. The ideomotor theory states that there are bidirectional associations between
movements and their sensory consequences, and that an action can be initiated by representing the desired
perceptual effect which in turn triggers the motor program required to reach that goal state. The common coding
principle extends this idea by proposing a common representational “code” for both action and perception at
higher levels of abstraction2–4. However, such a common code has yet to be demonstrated. Musical performance has proved an excellent model for exploring action-perception coupling due to the
required strong integration between auditory and motor systems. Through extensive training, musicians
develop strong bidirectional associations between finger movements and auditory feedback from their musical
instruments. During performance, movements are guided by the intended auditory outcomes, and conversely,
listening to melodies may prime the associated movements5–9. Behavioral studies have shown that experimentally
induced incongruences between actions and expected sounds interfere with musicians’ performance but not
that of non-musicians, highlighting the strength of these learned sensorimotor associations10. Neuroimaging
studies provide similar findings: Haslinger et al.11, for instance, found that when observing silent piano playing,
pianists – compared to musically naïve participants – exhibited higher activity not only in the premotor cortex
but also auditory cortex. This could be interpreted as action observation triggering representations of sounds in
the “mind’s ear” of the musicians. In the reverse direction, Lahav and colleagues showed that after brief piano
training, non-musicians had additional activity in the premotor cortex when listening to the learned melody
but not when listening to novel music12. All these findings highlight the importance of training for establishing
sensory-motor associations.
1Department of Cognitive Neuropsychology, Max Planck Institute for Empirical Aesthetics, Grüneburgweg 14,

### 60322 Frankfurt, Germany. 2Department of Neuroscience, Karolinska Institutet, Stockholm, Sweden. 3Fredrik Ullén

and Örjan de Manzano have contributed equally to this work. email: yu-hsin.chang@ae.mpg.de
OPEN
Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports

An additional important advantage of action-perception coupling is that it enables imagery, i.e. mental
simulation. Musicians often engage in mental rehearsal, which involves imagining the movements and sensory
experiences associated with playing the instrument, thereby presumably activating the neural circuits associated
with organizing motor output. Similarly, visualizing actions and outcomes is considered vital preparation for
optimal performance in many sports13–15. Interestingly, research has shown that even in the absence of actual
physical experience, mental imagery can activate the corresponding neural substrate. This is supported by brain
imaging studies that find overlapping areas of brain activity during motor execution and motor imagery16,17. Furthermore, studies on auditory processing and motor imagery reveal substantially shared neural substrates18–20. Most of the studies to date have primarily demonstrated a spatial overlap of neural activity between
observation, imagery, and motor execution21. A more specific question, however, is whether these activations
also represent a content-specific overlap, i.e. shared neural representations, or a “common code”, as mentioned
previously. Multivariate pattern analysis (MVPA) can address this by using machine learning to determine,
for instance, whether a classifier can learn to differentiate between voxel-wise patterns of brain activity that
correspond to different mental content22,23. The advantage of MVPA in comparison to traditional univariate
analysis, is that the informational content of brain activity is not left to interpretation, but can be probed and
confirmed with a machine learning classifier that is first trained, and then tested on previously unseen data. If
the classification can be done above chance with for instance permutation testing, even in a few individuals, this
is strong evidence that spatial patterns of activity in a given brain region can indeed encode the labels provided. Notably, MVPA is not limited to decoding information within the same modality, but can also provide evidence
for the generalization of representations across modalities24,25. For instance, Etzel, et al.26 trained a classifier on
brain activity patterns associated with the motor execution of hand or mouth actions, then tested whether it
could classify activity induced by listening to the corresponding action sounds. They found that the classifier was
able to decode the information in the premotor cortex across modalities. This provides a convincing case that the
same representations were used both in performance and perception. Thus far, the majority of evidence supporting the common coding principle has been limited to single
actions27,28. However, many – if not most – of our daily tasks are composed of numerous individual actions
carried out continuously in sequential order. It is therefore crucial to understand how the brain represents
sequences of actions. Using MVPA, several studies have revealed the representations of sequential movements
in motor and parietal regions29–31. In our previous work, we also applied MVPA to test if a classifier was able to
differentiate between brain patterns associated with listening to different pitch sequences (i.e. melodies), which
non-musicians had learned to play on the piano32. Consistent with the ideomotor theory, our findings indicated
that perceiving learned sequences elicited sequence-specific representations not only in the auditory cortex but
also in the premotor cortex, presumably through action-perception coupling. This did not happen in a control
group that listened to melodies without piano training, which confirms the training-dependent nature of these
sensorimotor associations. In the present study, we aimed to extend this finding to also test the common coding principle. Specifically,
we hypothesized that the same neural representations would be recruited during piano playing without auditory
feedback (while imagining the sound), as during listening to the same trained musical material without overt
movements (while imagining playing). For this purpose, we designed an experiment in which participants without prior musical training learned
to play two melodies on the piano. On the subsequent day, an fMRI experiment was performed in which the
participants (a) played the melodies without sound while imagining the auditory output (playing condition), and
(b) listened to the same melodies without playing while imagining the corresponding finger movements (listening
condition). We first examined the brain regions that were jointly active during both conditions using a univariate
conjunction analysis. Subsequently, a region-of-interest (ROI) based MVPA was conducted to see if a classifier
could differentiate between brain patterns corresponding to the two melodies in either condition/modality. Specifically, we focused on areas of the premotor cortex (the dorsal premotor area – PMD; the ventral premotor
area – PMV), and of the auditory cortex (superior temporal gyrus – STG), since previous research shows these
regions to be heavily engaged in action observation/imagery and auditory processing/imagery respectively. These regions are also engaged during the process of learning to play a melody33 and was in our previously
study shown to display spatial patterns of activity that differ systematically between melodic pitch sequences32. Lastly, cross-modal classification was performed to investigate if both conditions would induce similar brain
representations in the ROIs. Again, if the common coding principle were true, the spatial patterns of activity
induced by a melody should be the same regardless of condition. Therefore, a classifier trained on differentiating
between the melodies and their corresponding patterns of brain activity in one modality should also be able to
differentiate between the corresponding brain patterns in the other modality, and vice versa. Materials and methods
Participants
A total of 27 individuals participated in the study. The participants were recruited via the participant database
of the Max Planck Institute for Empirical Aesthetics and via open advertisement on our homepage, using
convenience sampling. The inclusion criteria required participants to be right-handed adults (> 18  years),
have less than 2 years of musical training in childhood, no musical training in adulthood, no neurological or
psychological disorders, and be eligible for MRI in accordance with general safety regulations. Five participants
were excluded; one participant due to a technical problem with the MRI scanner, one participant did not pass the
MRI safety screening, one participant chose to abort the scanning procedure, and two participants completed
both sessions but were excluded due to excessive head movements (> 2 mm displacement). Thus, 22 participants
were included in the final analysis (6 males, age = 30.41 ± 7.62 years). All experimental procedures followed the
guidelines of The Code of the World Medical Association (Declaration of Helsinki); they were ethically approved
Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

by the Ethics Council of the Max Planck Society and the ethics committee of the Department of Medicine of the
Goethe University Frankfurt (Dnr. 2017_12 and 415/17); and were undertaken with written informed consent of
each participant. Participants were compensated €7 per half-hour for the behavioral study and €10 per half-hour
for the MRI session, resulting in a total of €61 for each participant. Auditory stimuli
Two melodies were composed for this experiment. Each melody consisted of 2 bars with 7 notes from 5 pitches
(Fig. 1a). Both melodies were composed to be played with the right hand only, with a pitch range from C to G so
that each finger corresponded to one key. We thus avoided lateral movements of the hand in order to minimize
motion artifacts. Furthermore, no pitch was repeated more than 2 times, and no more than 1 note was in the
same sequential position across the melodies, in order to minimize representational overlap. MR-compatible keyboard
An MRI-compatible keyboard was used by the participants to play the melodies during scanning. The keyboard
was based on a Kawaii digital piano that was cut down to 24 keys (2 octaves), with all metal parts replaced with
plastic. The hammers were 3D-printed and weighted to match the action of the original hammers (Fig. 1b). Since
this experiment did not include auditory feedback from the piano, we will not elaborate on that functionality
here. Experimental procedure
Day 1 – Piano training and psychological testing
The day before the MRI experiment, participants were invited to a piano training session. Before the training
session started, the participants performed the Swedish Musical Discrimination Test (SMDT) to assess their
musical auditory ability34. In the experimental setup, two 25-key MIDI keyboard controllers (Alesis V25) were placed next to one
another to enable the participants to observe and replicate the finger movement of the instructor. The participants
listened to the two melodies, which were implemented in MuseScore3™ and presented through loudspeakers. The instructor first demonstrated the finger position on one keyboard and asked the participants to place their
fingers in the same way on the other. After the participants familiarized themselves with the keyboard, the
instructor then played one of the melodies (one bar at a time), while the participants tried to match the finger
movements. The participants were also asked to pay attention to the auditory feedback, which they heard through
the speakers. When the participant had learned to play the melody independently and repeatedly (10 times in
a row) without mistakes, the instructor moved on to teach the second melody. After both melodies had been
memorized, the participants were asked to practice them in an alternating fashion for 10 min. The instructor
then asked the participants to play without looking at their fingers, to mimic the conditions in the scanner, for
another 10 min. Lastly, the instructor asked participants to imagine the melodies while playing them without
Fig. 1. Stimuli, materials and experimental procedure. (a): The two melodies learned by the participants.
(b): The MRI piano. Numbers indicate fingering starting with the thumb (1) to the little finger (5) of the right
hand, matching the notes C, D, E, F, and G. (c): The experimental paradigm used in fMRI experiments. The
paradigm consisted of three blocks: one listening block and two playing blocks. All blocks started with four
beats of metronomes (96 bpm), followed by either melody A or B, and ended with a 4s resting period. Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

auditory feedback for yet another 10 min. After this training, all participants were able to play both melodies
flawlessly without looking at their fingers, without auditory feedback, and without moving anything but the right
hand. In addition, the participants practiced imagining the finger movements while listening to the melodies. This familiarization process helped participants get accustomed to the tasks they would perform during the
fMRI experiment. The training session lasted for 1 to 1.5 h in total. On the basis of previous studies using similar
doses of training (de Manzano et al.32), we assumed the training duration would be sufficient to establish action-
perception coupling. This assumption is also consistent with TMS studies that has shown plasticity changes in
auditory-motor regions after 30–40 min of piano practice5,7. MRI scanning parameters
The MRI data were collected on a 3 T Siemens Prisma scanner with a 32-channel head coil. The functional
scans were acquired using a multiband sequence with a factor of 3 with 2 mm isotropic voxels (TR = 2000 ms; TE = 30 ms; field of view (FOV) = 19.2 cm; matrix size = 96 × 96; flip angle = 90°). For each participant, we also
acquired a high-resolution T1-weighted (T1w) anatomical image (1 × 1 × 1 mm3, TR = 2000 ms; TE = 2.12 ms; TI = 1000 ms; FOV = 25.6 cm; matrix size = 256 × 256; flip angle = 8°) and a T2-weighted (T2w) scan (1 × 1 × 1
mm3, TR = 1500 ms; TE = 356 ms; FOV = 25.6 cm; matrix size = 256 × 256; flip angle = 120°). MRI experiment
Upon arrival on the second day, the participants practiced playing the melodies for around 10 min without
auditory feedback, to make sure they were able to play the melodies correctly in the scanner. The instructor
then explained the tasks and demonstrated the visual instructions. During scanning, these were projected onto
the screen behind the scanner and viewed through the periscope mirror system on the head coil. The visual
instructions, as well as the auditory stimuli, were delivered using the Presentation® software (Version 23.0, Neurobehavioral Systems, Inc., Berkeley, CA). In the scanner, the participants were put in supine position with the MRI-piano placed on their lap. MR-
compatible noise-canceling headphones were provided (OptoAcoustics OptoActive II TM ANC) to enable
presentation of the auditory stimuli. In addition, cushions were placed under the elbows of the participants to
minimize fatigue and hand/arm movements. The fMRI experiment consisted of 10 sessions (runs). Each session consisted of 2 conditions: a listening
and a playing condition (Fig. 1c). During the listening condition, the participants listened to both melodies in
a pseudorandomized order, with each melody presented 5 times. Each trial began with a four-beat metronome
cue (96 bpm), after which the melody was played. Participants were explicitly instructed not to move their
fingers during this condition, and instead imagine the finger movements as if they were playing. They were
further instructed to maintain their gaze at a red fixation cross which was displayed on screen to minimize eye-
movements. The playing condition consisted of 2 blocks, each corresponding to one of the melodies. Each block began
with an auditory presentation of the melody, indicating which melody the participant would be playing in that
block. The order of the melodies was randomized across the two blocks, so that each melody appeared in each
block an equal number of times across all participants. A four-beat metronome was then presented to indicate
the tempo, upon which the red fixation cross switched to green and the participants played the melody; then the
fixation cross switched back to red and there was a brief rest period. This metronome-play-rest sequence was
repeated 5 times before moving on to the next block. The participants were instructed to play the piano with the
right hand, without auditory feedback, while imagining the sound of the melody. Data analysis
Preprocessing of MRI data
The data were transformed from DICOM to NIfTI format using the MRIcroGL software. We then used the
Statistical Parametric Mapping software package (SPM12; Wellcome Department of Imaging Neuroscience, London, UK) for MATLAB™ (The Mathworks Inc., Natick, MA, USA) to preprocess the data. The functional
images were slice timing corrected and realigned to the first image of the first session. The T2w image and the
fMRI images were then coregistered to the T1w image, and both T2w and T1w images were jointly segmented. All images were then normalized to the MNI standard space. For MVPA, the fMRI images were smoothed using
a Gaussian kernel with a full-width-at-half-maximum (FWHM) of 4 mm, while for the univariate group-level
analysis, the images were smoothed with a FWHM of 8 mm. In addition, we visually checked the functional
images and used the artifact detection function in the CONN toolbox to identify potential artifacts ​(​h​t​t​p​:​/​/​w​w​w​.​n​i​t​r​c​.​o​r​g​/​p​r​o​j​e​c​t​s​/​c​o​n​n​; McGovern Institute for Brain Research, MIT, Cambridge, MA, USA)35. First-level univariate analysis of the fMRI data
A general linear model (GLM) combined with the standard hemodynamic response function was applied to the
fMRI data to calculate beta estimates. The beta estimates were later used as input for the multivariate pattern
analysis (MVPA). For the GLM, 4 regressors of interest (2 melodies × 2 conditions) were included for each
session. Also included as regressors in the model were the auditory instructions before blocks (melodies), the
metronome, realignment parameters, and regressors related to transient artifacts detected during preprocessing. Group-level univariate analysis
The contrast images of each condition (Listen and Play) versus baseline were calculated and then entered into
the second-level group analyses. To identify brain areas that were significantly activated in both conditions, we
performed a conjunction analysis based on the minimum statistic test36. The results were corrected for multiple
comparisons using a false discovery rate (FDR) threshold of p < 0.0537. Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

Multivariate pattern analysis (MVPA)
To determine whether (i) the two melodies induced sequence-specific brain representations and (ii) whether
the representations would generalize across conditions, we conducted several MVPAs. These analyses were
performed using The Decoding Toolbox (TDT, version 3.999E)38 implemented in MATLAB™. We first selected
6 a priori regions of interest (ROIs) (see Introduction), which included the left and right superior temporal
gyri (left/right STG), the left and right dorsal premotor cortices (left/right PMD), and the left and right ventral
premotor cortices (left/right PMV) (Fig. 2a). The STG masks were extracted from the Automated Anatomical
Atlas 3 (AAL-3)39 while the PMD and PMV masks were obtained from the Human Motor Area Template
(HMAT)40. The ROI masks were transformed to the native space of each participant and masked by the gray
matter mask. Functional ROIs were then defined by overlaying the activation map from the conjunction analysis
(uncorrected threshold of p < 0.001) onto these individual ROI masks. For MVPA decoding, we used a linear support vector machine (SVM)41 with a leave-one-out cross-validation
scheme for partitioning the data into training and test sets. Decoding was conducted in two stages. Firstly, we
performed within-condition decoding, that is, the SVM was trained to distinguish between the melodies based
on the voxel-wise patterns of the beta images from each condition separately. Secondly, we performed a cross-
modal classification with training data from the listening condition and testing data from the playing condition,
and vice versa (Fig. 2b). To determine the statistical significance of the decoding results, a permutation analysis
was performed with 10,000 permutations. For the group-level results, we performed a one-tailed one-sample
t-test on the individual accuracies from each ROI to test if they were significantly above chance (50%). The p-
values were corrected for the number of ROIs using FDR. ROIs with p-values less than 0.05 after FDR-correction
were deemed significant. Auditory ability and classification accuracy
In order to evaluate if individual differences in auditory ability would relate to action-perception coupling, we
performed Kendall’s Tau correlations between SMDT scores and individual classification accuracies obtained
from the MVPA. Results
Univariate analyses
In the listening condition, there were extensive activations across all ROIs, extending further into the parietal
cortices bilaterally (Fig.  3; Supplementary Table S1). Similar regions were active in the playing condition,
however with seemingly less extensive activity in the STG (Supplementary Table S2). The conjunction analysis
confirmed that all of the ROIs were activated during both conditions. In addition, bilateral supplementary motor
areas (SMA), primary sensory and motor cortices, and posterior parietal cortices including the superior parietal
lobes (SPL) and inferior parietal lobes (IPL) were found active during both conditions (Table 1). ROI-based multivariate pattern analysis
In the listening condition, all ROIs showed above-chance classification accuracies (p < 0.05, FDR corrected),
indicating that the melodies could be successfully decoded from these regions (Fig. 4). In contrast, during the
playing condition, decoding was successful in premotor regions but not in the STG. Finally, when performing the
cross-modal MVPA, the right PMD and PMV showed above-chance accuracies at the group level, demonstrating
its involvement in integrating the auditory and motor processing. Beyond the group level findings, permutation
Fig. 2. ROI-based MVPA. (a): Illustration of the selected ROIs: the superior temporal gyri (STG) in cyan
(sagittal slice at x = − 53.0), the premotor cortex (PMC) including the PMD in red and green, and the PMV in
yellow and blue (coronal slice at y = 4.6). (b): Illustration of the MVPA, including the within-condition MVPA
and the cross-modal MVPA. Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

testing on the individual level could confirm that 10 individuals had established strong and consistent spatial
patterns of activity that were similar enough to allow the machine learning classifier to train on one condition
and then decode the identity of the melodies with significant accuracy in the other, from at least one of the ROIs
(see Supplementary Table S3).
kE
p(FDR-corr)
Peak MNI coordinate (x, y, z)
Region
31,023
0.000
[60, 4, 20]
Precentral_R
0.000
[− 54, − 2, 42]
Precentral_L
0.000
[− 46, − 40, 20]
Temporal_Sup_L

0.000
[− 24, − 64, − 54]
Cerebellum_8_L
0.000
[26, − 64, − 50]
Cerebellum_8_R
0.000
[24, − 64, − 22]
Cerebellum_6_R

0.001
[− 46, − 58, 8]
Temporal_Mid_L
0.008
[− 38, − 46, 10]
Temporal_Sup_L

0.001
[34, 40, 28]
Frontal_Mid_R
0.002
[32, 40, 14]
Frontal_Mid_R
0.005
[22, 36, 20]
Frontal_Mid_R
Table 1. Activation peak statistics in conjunction analysis thresholded at p < 0.05 (FDR-corrected). For
interpretability, only clusters with a minimum of 100 contiguous voxels were reported. kE = the number of
significant voxels in the cluster; p(FDR-corr) = false discovery rate corrected p-values. Fig. 3. Illustration of active brain regions during the conditions. Significant activations at p < 0.05, FDR-
corrected (y = 8, − 4, − 16, − 28, − 40). Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

Associations between auditory ability and action perception coupling
We found no evidence for an association between auditory ability (SMDT scores) and classification accuracy,
neither from the within-modality MVPA of the listening condition, the playing condition nor from the cross-
modal classification (Table 2). Discussion
In this study, we examined the action-perception coupling effect in non-musicians after they learned to play
two melodies on the piano. According to the common coding principle, a shared neural code will represent
both an action and its corresponding sensory outcome once the association between the two is established2,4. On this basis, we hypothesized that after learning new melodies, the perception of their sounds would evoke
similar voxel-wise patterns of brain activity as the execution of the finger movements used to perform the same
melody on a keyboard. In line with earlier literature we, in both conditions, found overlapping brain activity
Listening
Playing
Cross-modal
τ
p
τ
p
τ
p
left STG
0.00
0.818
− 0.17
0.342
− 0.08
0.625
right STG
− 0.12
0.491
− 0.08
0.643
− 0.35
0.035
left PMD
− 0.10
0.624
0.10
0.423
− 0.21
0.194
right PMD
− 0.15
0.251
0.17
0.492
− 0.09
0.565
left PMV
− 0.10
0.488
0.00
0.954
0.09
0.582
right PMV
− 0.25
0.111
− 0.16
0.228
− 0.10
0.530
Table 2. Kendall’s Tau correlation between SMDT scores and classification accuracies. Fig. 4. ROI-based MVPA classification accuracy results. * Significant at p < 0.05, FDR-corrected. Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

when participants listened to the trained melodies and only imagined playing, and when they were playing the
piano and only imagined the sound. This overlap included motor and auditory regions, as well as extended areas
in the posterior parietal lobe. MVPA further demonstrated sequence-specific representations in the bilateral
PMD and PMV across both conditions, with bilateral STG reflecting distinct patterns specifically during the
listening condition. Most importantly, we found support for our main hypothesis, showing that brain activity
patterns in the right PMD and right PMV could be generalized across modalities in many specific individuals
and at the group level, as indicated by the cross-modal classification results. There were individual differences in
the classification accuracy, indicating variability in auditory-motor integration between participants; however,
this variability could not be attributed to individual differences in auditory ability. Instead, it appears that other
factors were at play, and we suggest that a longer training period may have facilitated the establishment of
more robust sensorimotor associations between pitch sequences and finger movements across the sample. We
elaborate on these findings below. Univariate analysis
Action observation, imagery, and execution recruit largely overlapping sets of brain regions, as revealed by
previous research21,42,43. These areas include the PMD, PMV, SMA, IPL, and SPL. Furthermore, in the context of
perceiving an action associated with sound or auditory imagery, the STG is also involved11,44–46. Our results from
the conjunction analysis support these findings, showing joint activation in the aforementioned regions during
both conditions. However, it is important to highlight that although the regions were jointly activated, univariate
analysis does not provide evidence that the regions represented the melodies equally during both conditions. On the contrary, the multivariate analyses of patterns of activity in auditory-motor areas point to interesting
differences between listening with motor imagery and playing with auditory imagery. Within-condition MVPA
A primary purpose of these multivariate analyses was to investigate whether there were sequence-specific
representations of pitches/finger movements in the ROIs. Classification within the listening condition essentially
replicated our previously reported findings32, showing above-chance classification accuracies in all ROIs. For
the playing condition, the classification accuracy was significant only for the premotor regions. One explanation
for the non-significant classification in auditory regions could be interference between auditory imagery during
playing and scanner noise, which is naturally a limiting factor and perhaps even more so in non-musicians. Cross-modal MVPA
Cross-modal classification allowed us to examine the formation of a common representational code between
listening (while imagining playing) and playing (while imagining listening) to the melodies. Out of the 6 ROIs
selected, we found that decoding across conditions and across the sample was successful in the right PMD and
PMV, suggesting that common sequence-specific patterns were formed in these regions. These results support
the common coding principle; that the association between an action sequence and its corresponding sensory
outcome is established in the form of a shared brain representation, or more specifically, a shared spatial pattern
of brain activity. Notably, previous studies have primarily applied cross-modal classification to single actions. Our study extends this approach to motor sequences, which demonstrates that common codes can also be
formed for more complex action patterns. The presence of shared representations between action and perception in the premotor cortex aligns with
previous studies, which highlighted the role of this area in auditory-motor coupling26,32,47–49. Located at the
interface between the primary motor cortex and STG, the premotor cortex integrates inputs from motor and
sensory aspects20. The right PMD and PMV, in particular, appear to be crucial for this integration, as they
exhibit consistent activation patterns when the participants perform and perceive the same melody. Although it
may seem surprising that the right hemisphere showed more prominent results than the left, given that only the
right hand was used by the participants throughout the task, previous studies have illustrated the recruitment of
ipsilateral motor cortex during movements that require higher task demands50,51. Wiestler and colleagues also
reported effector independent representations in these regions52. Additionally, the right hemisphere has been
shown to be more involved in musical processing, which may further contribute to its role in auditory-motor
integration53–55. While it remains unclear whether these findings are due to lateralization, our findings suggest
that the right hemisphere plays a more significant role in this process. In contrast, we did not find cross-modal representations in the left PMD and PMV across the sample, despite
observing within-condition sequence-specific patterns in these areas during both the listening and playing
conditions. In other words, while the left premotor cortex was engaged in processing the auditory and motor
sequences, the sequence representations were condition-specific rather than shared. Notably, even though action
and perception can be coupled, they are not usually confused, and our findings indicate that distinct and shared
codes are maintained in parallel, by lateralizing the different forms of representation. This might be an interesting
avenue for further research on the integration and segregation of action and perception. Although the STG was jointly activated during both conditions, as shown by the conjunction analysis, no
cross-modal representations were present. This might be related to the results from the within-condition MVPA,
where the classifier did not perform above-chance during the playing/imagine-sound condition. As suggested
previously, this could be related to auditory imagery being more inconsistent, perhaps in part due to the scanner
noise, resulting in lower classification performance. Consequently, this variability would also tend to reduce
cross-modal classification accuracy. Individual differences across regions were observed, as shown in Supplementary Table S3. While we found
strong and significant evidence for cross-modal representations at the individual level in 10 participants, there
were some differences with regard to the specific ROIs. This suggests that many participants indeed formed
Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

integrated action-sound representations during training, which were used during the performance of both
conditions, but also that there were individual differences in the spatial location of these representations. One
potential source of variability could be that the more fine-grained functional organization of brain regions
involved in the processing of music depends on learning and plasticity related to previous musical experiences
and music listening habits. Given this variability, an interesting question for future studies is to see if common auditory-motor codes
can also form in other regions. Although we found extensive overlaps in brain activity between listening and
playing conditions, we found the “common code” mostly in the right PMD and PMV. Previous studies have
demonstrated that 20–30 min of piano training in naïve participants could lead to plasticity changes in the brain
or intracortical facilitation7,56. At the same time, during the learning process, the brain is still reorganizing,
and therefore the sequence representations may vary across time during the experiment57,58. Indeed, previous
studies indicate that sequence-specific representations may be more robust after longer periods (days or weeks)
of training30,31,59. Thus, this study, with its limited training dose and musical material, could be viewed as a proof
of concept that future work could extend on. To this date, not many studies have applied cross-modal classification within auditory and motor domains26. The majority of studies that have reported successful cross-modal decoding focused on the relationship
between visual and motor representations28,60. In addition, only a few investigations have specifically addressed
sequential learning. Consequently, numerous factors might conceivably influence cross-modal classification
that require further investigation. As mentioned previously, the individual differences in classification accuracy
observed in this study suggest that the presence of such influencing factors. Future studies could investigate the
relationship between factors such as training dose, personal characteristics, and previous personal experience on
the formation of action-perception coupling. This study was limited with regard to such information. Exploring
similar factors could provide valuable insights into the neural mechanisms underlying musical learning and skill
learning in general. Despite the complexities outlined above, a fundamental question arises as to whether the common coding
principle fully explains the action-perception coupling effect. While several studies have supported this notion,
it is still possible that during the initial stage of the learning process, there are separate codes for action and
perception. As famously proposed by Donald Hebb, synaptic connections between neurons may increase in
strength when they are repeatedly activated simultaneously, so that initially independent neural circuits
eventually form larger integrated assemblies that control behavior61. Along these lines, it could be speculated
that although different coding principles are used for sensory and motor information at the initial learning
stage, such modality-specific representations can through repeated coactivation and plastic adaptations
in sensorimotor brain networks eventually become unified into a more abstract code that facilitates or even
automates bidirectional associations. Conclusions
In summary, our study demonstrates, firstly, that sequence-specific representations of complex acquired skills
and their sensory consequences are possible to establish via short-term training. Specifically, melody-specific
patterns of neural activity were found in bilateral PMD and PMV in both listening and playing conditions,
while STG only showed distinct patterns in the listening condition. Secondly, we found evidence for cross-
modal representations in the right PMD and right PMV, suggesting that these regions play an important role for
integrating action and sound, including tasks involving mental imagery. Finally, analyses of single participants
indicate individual variation in cognitive strategies and the spatial localization of relevant neural processes. Important questions for future studies will be to address the implications of individual variation in neural
coding, as well as the question whether common coding can be established in different brain regions as action-
perception coupling is strengthened during prolonged training. Data availability
The datasets generated during and/or analyzed during the current study are available from the corresponding
author on reasonable request. Received: 16 August 2024; Accepted: 25 April 2025
References

### 1. Novembre, G. & Keller, P. E. A conceptual review on action-perception coupling in the musicians’ brain: What is it good for?. Front. Hum. Neurosci. 8, 1–11. https://doi.org/10.3389/fnhum.2014.00603 (2014).

### 2. Prinz, W. In Relationships Between Perception and Action 167-201 (Springer Berlin Heidelberg, 1990).

### 3. Herwig, A. Linking perception and action by structure or process? Toward an integrative perspective. Neurosci. Biobehav. Rev. 52,

105–116. https://doi.org/10.1016/j.neubiorev.2015.02.013 (2015).

### 4. Hommel, B., Müsseler, J., Aschersleben, G. & Prinz, W. The Theory of Event Coding (TEC): A framework for perception and action

planning. Behav. Brain Sci. 24, 849–878. https://doi.org/10.1017/s0140525x01000103 (2001).

### 5. Stephan, M. A., Lega, C. & Penhune, V. B. Auditory prediction cues motor preparation in the absence of movements. Neuroimage

174, 288–296. https://doi.org/10.1016/j.neuroimage.2018.03.044 (2018).

### 6. Haueisen, J. & Knosche, T. R. Involuntary motor activity in pianists evoked by music perception. J Cogn Neurosci 13, 786–792.

https://doi.org/10.1162/08989290152541449 (2001).

### 7. D’Ausilio, A., Altenmüller, E., Olivetti Belardinelli, M. & Lotze, M. Cross-modal plasticity of the motor cortex while listening to a

rehearsed musical piece. Eur. J. Neurosci. 24, 955–958. https://doi.org/10.1111/j.1460-9568.2006.04960.x (2006).

### 8. Bangert, M. et al. Shared networks for auditory and motor processing in professional pianists: evidence from fMRI conjunction. Neuroimage 30, 917–926. https://doi.org/10.1016/j.neuroimage.2005.10.044 (2006). Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

### 9. Stephan, M. A., Brown, R., Lega, C. & Penhune, V. Melodic priming of motor sequence performance: The role of the dorsal

premotor cortex. Front Neurosci 10, 210. https://doi.org/10.3389/fnins.2016.00210 (2016).

### 10. Drost, U. C., Rieger, M., Brass, M., Gunter, T. C. & Prinz, W. Action-effect coupling in pianists. Psychol Res 69, 233–241. ​h​t​t​p​s​:​/​/​d​

o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​0​0​4​2​6​-​0​0​4​-​0​1​7​5​-​8​ (2005).

### 11. Haslinger, B. et al. Transmodal sensorimotor networks during action observation in professional pianists. J Cognitive Neurosci 17,

282–293. https://doi.org/10.1162/0898929053124893 (2005).

### 12. Lahav, A., Saltzman, E. & Schlaug, G. Action representation of sound: audiomotor recognition network while listening to newly

acquired actions. J Neurosci 27, 308–314. https://doi.org/10.1523/JNEUROSCI.4822-06.2007 (2007).

### 13. Driskell, J. E., Copper, C. & Moran, A. Does mental practice enhance performance?. J. Appl. Psychol. 79, 481–492. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​

1​0​.​1​0​3​7​/​0​0​2​1​-​9​0​1​0​.​7​9​.​4​.​4​8​1​ (1994).

### 14. Roure, R. et al. Imagery quality estimated by autonomic response is correlated to sporting performance enhancement. Physiol

Behav 66, 63–72. https://doi.org/10.1016/S0031-9384(99)00026-8 (1999).

### 15. Cumming, J. & Hall, C. Deliberate imagery practice: The development of imagery skills in competitive athletes. J. Sports Sci. 20,

137–145. https://doi.org/10.1080/026404102317200846 (2002).

### 16. Gerardin, E. et al. Partially overlapping neural networks for real and imagined hand movements. Cereb. Cortex 10, 1093–1104.

https://doi.org/10.1093/cercor/10.11.1093 (2000).

### 17. Hanakawa, T., Dimyan, M. A. & Hallett, M. Motor planning, imagery, and execution in the distributed motor network: A time-

course study with functional MRI. Cereb. Cortex 18, 2775–2788. https://doi.org/10.1093/cercor/bhn036 (2008).

### 18. Zatorre, R. J., Halpern, A. R., Perry, D. W., Meyer, E. & Evans, A. C. Hearing in the mind’s ear: A PET investigation of musical

imagery and perception. J Cognitive Neurosci 8, 29–46. https://doi.org/10.1162/jocn.1996.8.1.29 (1996).

### 19. Herholz, S. C., Halpern, A. R. & Zatorre, R. J. Neuronal correlates of perception, imagery, and memory for familiar tunes. J

Cognitive Neurosci 24, 1382–1397. https://doi.org/10.1162/jocn_a_00216 (2012).

### 20. Zatorre, R. J., Chen, J. L. & Penhune, V. B. When the brain plays music: auditory–motor interactions in music perception and

production. Nat. Rev. Neurosci. 8, 547–558. https://doi.org/10.1038/nrn2152 (2007).

### 21. Hardwick, R. M., Caspers, S., Eickhoff, S. B. & Swinnen, S. P. Neural correlates of action: Comparing meta-analyses of imagery,

observation, and execution. Neurosci. Biobehav. Rev. 94, 31–44. https://doi.org/10.1016/j.neubiorev.2018.08.003 (2018).

### 22. Haynes, J. D. & Rees, G. Decoding mental states from brain activity in humans. Nat Rev Neurosci 7, 523–534. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​

0​3​8​/​n​r​n​1​9​3​1​ (2006).

### 23. Norman, K. A., Polyn, S. M., Detre, G. J. & Haxby, J. V. Beyond mind-reading: multi-voxel pattern analysis of fMRI data. Trends

Cogn Sci 10, 424–430. https://doi.org/10.1016/j.tics.2006.07.005 (2006).

### 24. Meyer, K. & Kaplan, J. T. Cross-Modal Multivariate Pattern Analysis. J. Vis. Exp. https://doi.org/10.3791/3307 (2011).

### 25. Kaplan, J. T., Man, K. & Greening, S. G. Multivariate cross-classification: applying machine learning techniques to characterize

abstraction in neural representations. Front. Human Neurosci. https://doi.org/10.3389/fnhum.2015.00151 (2015).

### 26. Etzel, J. A., Gazzola, V. & Keysers, C. Testing simulation theory with cross-modal multivariate classification of fMRI data. PLoS

ONE 3, e3690. https://doi.org/10.1371/journal.pone.0003690 (2008).

### 27. Fiave, P. A., Sharma, S., Jastorff, J. & Nelissen, K. Investigating common coding of observed and executed actions in the monkey brain

using cross-modal multi-variate fMRI classification. Neuroimage 178, 306–317. https://doi.org/10.1016/j.neuroimage.2018.05.043
(2018).

### 28. Oosterhof, N. N., Tipper, S. P. & Downing, P. E. Viewpoint (In)dependence of Action Representations: An MVPA Study. J Cognitive

Neurosci 24, 975–989. https://doi.org/10.1162/jocn_a_00195 (2012).

### 29. Mason, R. A. & Just, M. A. Neural representations of procedural knowledge. Psychol. Sci. 31, 729–740. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​7​7​/​0​9​

5​6​7​9​7​6​2​0​9​1​6​8​0​6​ (2020).

### 30. Wiestler, T. & Diedrichsen, J. Skill learning strengthens cortical representations of motor sequences. Elife 2, e00801. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​

g​/​1​0​.​7​5​5​4​/​e​L​i​f​e​.​0​0​8​0​1​ (2013).

### 31. Berlot, E., Popp, N. J. & Diedrichsen, J. A critical re-evaluation of fMRI signatures of motor sequence learning. Elife ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​

g​/​1​0​.​7​5​5​4​/​e​L​i​f​e​.​5​5​2​4​1​ (2020).
32.	 de Manzano, O., Kuckelkorn, K. L., Strom, K. & Ullen, F. Action-perception coupling and near transfer: Listening to melodies after
Piano practice triggers sequence-specific representations in the auditory-motor network. Cereb Cortex 30, 5193–5203. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​3​/​c​e​r​c​o​r​/​b​h​a​a​0​1​8​ (2020).

### 33. Chen, J. L., Rae, C. & Watkins, K. E. Learning to play a melody: An fMRI study examining the formation of auditory-motor

associations. Neuroimage 59, 1200–1208. https://doi.org/10.1016/j.neuroimage.2011.08.012 (2012).

### 34. Ullén, F., Mosing, M. A., Holm, L., Eriksson, H. & Madison, G. Psychometric properties and heritability of a new online test for

musicality, the Swedish Musical Discrimination Test. Personality Individ. Differ. 63, 87–93. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​p​a​i​d​.​2​0​1​4​.​0​1​.​
0​5​7​ (2014).

### 35. Whitfield-Gabrieli, S. & Nieto-Castanon, A. Conn: A functional connectivity toolbox for correlated and anticorrelated brain

networks. Brain Connect 2, 125–141. https://doi.org/10.1089/brain.2012.0073 (2012).

### 36. Nichols, T., Brett, M., Andersson, J., Wager, T. & Poline, J.-B. Valid conjunction inference with the minimum statistic. Neuroimage

https://doi.org/10.1016/j.neuroimage.2004.12.005 (2005).

### 37. Benjamini, Y. & Hochberg, Y. Controlling the false discovery rate: A practical and powerful approach to multiple testing. J. Roy. Stat. Soc.: Ser. B (Methodol.) 57, 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x (1995).

### 38. Hebart, M. N., Görgen, K. & Haynes, J.-D. The Decoding Toolbox (TDT): A versatile software package for multivariate analyses of

functional imaging data. Front. Neuroinf. https://doi.org/10.3389/fninf.2014.00088 (2015).

### 39. Rolls, E. T., Huang, C. C., Lin, C. P., Feng, J. & Joliot, M. Automated anatomical labelling atlas 3. Neuroimage 206, 116189. ​h​t​t​p​s​:​/​/​

d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​9​.​1​1​6​1​8​9​ (2020).

### 40. Mayka, M. A., Corcos, D. M., Leurgans, S. E. & Vaillancourt, D. E. Three-dimensional locations and boundaries of motor and

premotor cortices as defined by functional brain imaging: A meta-analysis. Neuroimage 31, 1453–1474. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​
n​e​u​r​o​i​m​a​g​e​.​2​0​0​6​.​0​2​.​0​0​4​ (2006).

### 41. Chang, C. C. & Lin, C. J. LIBSVM: A library for support vector machines. Acm T Intel Syst Tec https://doi.org/10.1145/1961189.1961199

(2011).

### 42. Filimon, F., Rieth, C. A., Sereno, M. I. & Cottrell, G. W. Observed, executed, and imagined action representations can be decoded

from ventral and dorsal areas. Cereb. Cortex 25, 3144–3158. https://doi.org/10.1093/cercor/bhu110 (2015).

### 43. Grèzes, J. & Decety, J. Functional anatomy of execution, mental simulation, observation, and verb generation of actions: A meta-

analysis. Hum. Brain Mapp. 12, 1–19. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​2​/​1​0​9​7​-​0​1​9​3​(​2​0​0​1​0​1​)​1​2​:​1​%​3​c​1​:​:​a​i​d​-​h​b​m​1​0​%​3​e​3​.​0​.​c​o​;​2​-​v (2001).

### 44. Gazzola, V., Aziz-Zadeh, L. & Keysers, C. Empathy and the somatotopic auditory mirror system in humans. Curr. Biol. 16, 1824–

1829. https://doi.org/10.1016/j.cub.2006.07.072 (2006).

### 45. Regev, M., Halpern, A. R., Owen, A. M., Patel, A. D. & Zatorre, R. J. Mapping specific mental content during musical imagery. Cereb. Cortex 31, 3622–3640. https://doi.org/10.1093/cercor/bhab036 (2021).

### 46. Rampinini, A. C. et al. Functional and spatial segregation within the inferior frontal and superior temporal cortices during

listening, articulation imagery, and production of vowels. Sci Rep-Uk https://doi.org/10.1038/s41598-017-17314-0 (2017).

### 47. Chen, J. L., Penhune, V. B. & Zatorre, R. J. The Role of Auditory and Premotor Cortex in Sensorimotor Transformations. Ann. N. Y. Acad. Sci. 1169, 15–34. https://doi.org/10.1111/j.1749-6632.2009.04556.x (2009). Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/

### 48. Siman-Tov, T. et al. The rediscovered motor-related area 55b emerges as a core hub of music perception. Commun. Biol. ​h​t​t​p​s​:​/​/​d​o​

i​.​o​r​g​/​1​0​.​1​0​3​8​/​s​4​2​0​0​3​-​0​2​2​-​0​4​0​0​9​-​0​ (2022).

### 49. Baumann, S. et al. A network for audio–motor coordination in skilled pianists and non-musicians. Brain Res. 1161, 65–78. ​h​t​t​p​s​:​/​

/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​b​r​a​i​n​r​e​s​.​2​0​0​7​.​0​5​.​0​4​5​ (2007).

### 50. Schach, S., Braun, D. A. & Lindner, A. Cross-hemispheric recruitment during action planning with increasing task demand. Sci. Rep. 13, 15375. https://doi.org/10.1038/s41598-023-41926-4 (2023).

### 51. Verstynen, T., Diedrichsen, J., Albert, N., Aparicio, P. & Ivry, R. B. Ipsilateral motor cortex activity during unimanual hand

movements relates to task complexity. J. Neurophysiol. 93, 1209–1222. https://doi.org/10.1152/jn.00720.2004 (2005).

### 52. Wiestler, T., Waters-Metenier, S. & Diedrichsen, J. Effector-independent motor sequence representations exist in extrinsic and

intrinsic reference frames. J. Neurosci. 34, 5054–5064. https://doi.org/10.1523/jneurosci.5363-13.2014 (2014).

### 53. Peretz, I. & Zatorre, R. J. Brain organization for music processing. Annu Rev Psychol 56, 89–114. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​4​6​/​a​n​n​u​r​e​v​.​

p​s​y​c​h​.​5​6​.​0​9​1​1​0​3​.​0​7​0​2​2​5 (2005).

### 54. Oechslin, M. S., Gschwind, M. & James, C. E. Tracking training-related plasticity by combining fMRI and DTI: the right hemisphere

ventral stream mediates musical syntax processing. Cereb Cortex 28, 1209–1218. https://doi.org/10.1093/cercor/bhx033 (2018).

### 55. Albouy, P., Benjamin, L., Morillon, B. & Zatorre, R. J. Distinct sensitivity to spectrotemporal modulation supports brain asymmetry

for speech and melody. Science 367, 1043–1047. https://doi.org/10.1126/science.aaz3468 (2020).

### 56. Bangert, M. & Altenmüller, E. O. Mapping perception to action in piano practice: a longitudinal DC-EEG study. BMC Neurosci. 4,

26. https://doi.org/10.1186/1471-2202-4-26 (2003).

### 57. Peters, A. J., Lee, J., Hedrick, N. G., O’Neil, K. & Komiyama, T. Reorganization of corticospinal output during motor learning. Nat. Neurosci. 20, 1133–1141. https://doi.org/10.1038/nn.4596 (2017).

### 58. Yu, M., Song, H., Huang, J., Song, Y. & Liu, J. Motor learning improves the stability of large-scale brain connectivity pattern. Front. Human Neurosci. https://doi.org/10.3389/fnhum.2020.571733 (2020).

### 59. Yokoi, A., Arbuckle, S. A. & Diedrichsen, J. The role of human primary motor cortex in the production of skilled finger sequences. J. Neurosci. 38, 1430–1442. https://doi.org/10.1523/jneurosci.2798-17.2017 (2018).

### 60. Oosterhof, N. N., Wiggett, A. J., Diedrichsen, J., Tipper, S. P. & Downing, P. E. Surface-based information mapping reveals

crossmodal vision-action representations in human parietal and occipitotemporal cortex. J. Neurophysiol. 104, 1077–1089. ​h​t​t​p​s​:​/​
/​d​o​i​.​o​r​g​/​1​0​.​1​1​5​2​/​j​n​.​0​0​3​2​6​.​2​0​1​0​ (2010).

### 61. Hebb, D. The organization of behavior. A neuropsychological theory. (1949). Acknowledgements
We thank the lab team members in the Max Planck Institute for Empirical Aesthetics and the MR Core Structure
Unit of the Brain Imaging Center in University Hospital Frankfurt for technical support. Author contributions
YC: Conceptualization, Methodology, Data Collection, Data Analysis, Writing – Original Draft, Review & Edit­
ing. FU: Conceptualization, Funding acquisition, Supervision, Writing – Review & Editing. ÖdM: Conceptual­
ization, Methodology, Project Administration, Supervision, Writing – Review & Editing. Funding
Open Access funding enabled and organized by Projekt DEAL. Competing interests
The authors declare no competing interests. Additional information
Supplementary Information The online version contains supplementary material available at ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​3​8​/​s​4​1​5​9​8​-​0​2​5​-​0​0​2​0​8​-​x​.​
Correspondence and requests for materials should be addressed to Y.-H. F. C. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Open Access  This article is licensed under a Creative Commons Attribution 4.0 International License, which
permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and
indicate if changes were made. The images or other third party material in this article are included in the article’s
Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included
in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or
exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy
of this licence, visit http://creativecommons.org/licenses/by/4.0/.
© The Author(s) 2025
Scientific Reports | (2025) 15:16492

| https://doi.org/10.1038/s41598-025-00208-x
www.nature.com/scientificreports/
