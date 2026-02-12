# decoding-auditory-working-memory-load-from-eeg-alp

1 of 18Psychophysiology, 2025; 62:e70210
https://doi.org/10.1111/psyp.70210
Psychophysiology
ORIGINAL ARTICLE OPEN ACCESS
Decoding Auditory Working Memory Load From EEG 
Alpha Oscillations
Yichen Yuan 1 |  Surya Gayet 1  |  Derk Christiaan Wisman 1 |  Stefan van der Stigchel 1 |  Nathan van der Stoep 1,2
1Department of Experimental Psychology, Helmholtz Institute, Utrecht University, Utrecht, the Netherlands | 2Human Machine Teaming, Defense, Safety, 
and Security, TNO, Soesterberg, the Netherlands
Correspondence:  Yichen Yuan (y.yuan@uu.nl)
Received:  3 March 2025 | Revised:  29 November 2025 | Accepted:  2 December 2025
Keywords: auditory working memory | CDA | EEG decoding | memory capacity | modality-  specific
ABSTRACT
Working memory (WM) enables temporary retention of task- relevant information for imminent use. Increases in visual WM load 
are accompanied by elevated contralateral delay activity (CDA) and EEG alpha-  band power. While most WM research focuses 
on the visual domain, it remains unknown whether similar EEG responses also reflect WM load in the auditory domain. Using 
EEG, we set out to establish such neural markers of auditory WM load. Participants memorized the pitches of 1–4 pure tones 
presented to one ear, with 1–4 identical distractor tones presented to the other ear. Behaviorally, auditory WM capacity plateaued 
between set sizes two and three. Unlike for visual WM, auditory WM load was not reflected in lateralized EEG responses. This 
shows that the CDA is a vision-  specific rather than domain-  general neural marker of WM load. Applying multivariate pattern 
analyses on the delay activity revealed that auditory WM load is reflected in patterns of alpha-  band oscillations. Surprisingly, 
a temporal generalization analysis revealed that the alpha patterns reflecting specific load conditions changed throughout the 
maintenance period (despite load being inherently constant), revealing dynamic coding of auditory WM load.
1   |   Introduction
Working memory (WM) is a limited-  capacity system that al -
lows us to temporarily hold several representations accessible in 
service of other mental tasks (Cowan  1998). Commonly, not all 
task- relevant information is available in one location or at a sin -
gle moment, which requires us to temporarily retain informa -
tion in mind. For instance, we may memorize a phone number 
for subsequent dialing or remember a list of ingredients while 
grocery shopping. WM functions as our central information 
storage- and- processing structure (Cowan et al.  2005), which en-
ables us to interact with the world over space and time.
So far, Baddeley and Hitch  ( 1974) proposed probably the most 
influential WM model, which comprises three components: 
(1) a visuo-  spatial sketchpad for storage of visual information; 
(2) a phonological loop for storage of auditory information; (3) 
a central executive that regulates the content of the active por -
tion of WM. Years later, Baddeley ( 2000) added a fourth com -
ponent, the episodic buffer, that binds features from different 
sources together into multidimensional objects. According to 
Baddeley's model, the storage of WM is modality-  specific, with 
a visuo-  spatial sketchpad for visual information and a phono -
logical loop for auditory information. Indeed, previous studies 
have provided evidence that visual and auditory WM may rely 
on at least partly distinct structures that produce dissociable 
neural responses (Lefebvre et al.  2013; Pratt et al.  1989; also see 
Scimeca et al. 2018  for sensory recruitment hypothesis).
Given the (at least partly) modality-  specific nature of WM, it 
is reasonable to use modality-  specific stimuli to study visual 
WM and auditory WM separately. Yet, most WM studies to date 
focused on the visual modality, for instance the color, orienta -
tion, spatial location, etc. of visual items (Carlisle et  al.  2011; 
This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium, 
provided the original work is properly cited.
© 2025 The Author(s). Psychophysiology  published by Wiley Periodicals LLC on behalf of Society for Psychophysiological Research.
2 of 18 Psychophysiology, 2025
Diamantopoulou et  al.  2011; Harrison and Tong  2009; 
Li and Saiki  2015; Luria and Vogel  2011; Schurgin  2018). 
Correspondingly, studies have found evidence for the existence 
of a “magic number four,” the observation that visual working 
memory capacity is severely limited to an average of four items 
in young adults (Cowan  2010). By recording electroencephalo -
grams (EEG), Luck and Vogel ( 1997) identified a neural marker 
of visual WM load and named it Contralateral Delay Activity 
(CDA). Specifically, they presented a symmetric visual array in 
which the left and right side differed in features and instructed 
the participants to memorize the objects in only one hemifield. 
In this bilateral change-  detection paradigm, information pre -
sented on both sides was perceptually processed, but informa -
tion presented in only one hemifield was subsequently retained 
in WM. Interhemispheric difference waves were calculated for 
each set-  size condition by subtracting the ipsilateral activity 
from the contralateral activity. By doing so, any nonspecific, 
bilateral Event-  Related Potentials (ERPs) were removed. This 
approach thus allows isolating the neural activity specifically 
related to the encoding and maintenance of the memorized 
objects. A large negative-  going voltage over the contralateral 
hemisphere (relative to the memorized hemifield) was observed, 
located primarily over posterior parietal and lateral occipital 
electrodes. Moreover, the amplitude of the CDA varied with 
visual WM load, as it increased between set sizes of one, two, 
and three items, and then leveled off at the group's average ca -
pacity limit of about three items (Vogel and Machizawa  2004). 
Interestingly, the existence of lateralized responses to set size 
(such as the CDA) implies that visual WM is inherently spatially 
organized.
Another neural marker of visual WM has been observed in the 
frequency domain, particularly in the alpha band, although stud-
ies have reported contradictory results regarding its modulation 
direction. For instance, Jensen et  al.  ( 2002) have shown that 
the power of oscillations in the alpha-  band (8–12 Hz) over the 
posterior and central EEG channels tracks visual memory load 
during the maintenance period. Such increases in alpha band 
power during WM maintenance are widely accepted as reflect -
ing functional disengagement or inhibition of task- irrelevant vi-
sual inputs to protect the task-  relevant information maintained 
in WM (Bonnefond and Jensen  2012; Roux and Uhlhaas  2014; 
Tuladhar et  al.  2007; Wianda and Ross  2019). In contrast, a 
number of studies have reported attenuated alpha oscillations in 
sensory areas that are mnemonically relevant, suggesting that 
alpha decreases may support the recruitment of these areas for 
perceptual WM retention (Fukuda et  al.  2015; van Ede  2018). 
Taken together, several neural markers of WM load have been 
established in the visual domain, some of which are lateralized 
(capitalizing on the spatial organization of visual WM) and some 
of which are not.
Surprisingly, much less is known about auditory WM com -
pared to visual WM. In the current study, we define auditory 
WM as the maintenance of acoustic properties of sound stimuli, 
such as the pitch, duration, timbre, and amplitude (following 
Lefebvre et al.  2013). It should be noted that the maintenance 
of verbal information is not necessarily the same as auditory 
WM. Studies have found that the maintenance of verbal and 
of purely acoustic material share relatively few characteristics 
(Deutsch  1970; Williamson et al.  2010). In the studies focusing 
on the maintenance of acoustic properties, the auditory WM ca -
pacity found in tasks using pure tones was around 2–3 (Alunni- 
Menichini et  al.  2014; Li et  al.  2013; Prosser  1995). Lefebvre 
et  al.  ( 2013) set out to identify the neural marker of auditory 
short- term memory. Contrasting the univariate EEG response 
during the maintenance period between the memory task and a 
control task revealed a sustained negative- going voltage over the 
central- frontal electrodes that scaled with auditory WM load. 
This negativity was identified as a neural marker of auditory 
WM and named the sustained anterior negativity (SAN). In a 
follow- up study, Alunni- Menichini et al. ( 2014) showed that the 
amplitude of SAN increased in negativity from 2 to 4 items and 
then leveled off from 4 to 8 items. Thus, they established the SAN 
as an index of brain activity specifically reflecting the amount of 
information (load) maintained in auditory WM. In these studies 
investigating auditory WM, however, stimulus presentation was 
not lateralized, unlike typical visual WM studies measuring lat -
eralized responses (CDA). Thus, it remains unknown whether 
lateralized responses that hinge on the inherently spatial orga -
nization of WM (akin to the CDA for visual WM) can also be ob-
served for auditory WM load. On the one hand, it is reasonable to 
assume that the visual CDA reflects an enhanced representation 
of the contralateral spatial location where the memorized items 
are stored (e.g., Klaver et al.  1999; Talsma et al.  2001), suggesting 
a modality- specific neural marker for visual WM alone. On the 
other hand, if the CDA reflects a more abstract form of work -
ing memory representation, the lateralized CDA-  like responses 
should also be observed in auditory working memory tasks.
Other studies, focusing on the frequency domain of the EEG 
response, have found that alpha oscillations (8–12 Hz) are also 
a sensitive marker for auditory WM load (Kaiser et  al.  2007; 
Leiberg et al.  2006; Luo et al.  2005; van Dijk et al.  2010). For in-
stance, Leiberg et al. ( 2006) found monotonic increases in spec -
tral amplitude as a function of memory load for the alpha band 
over right frontal sensors during the delay period. Similarly, van 
Dijk et al. ( 2010) also found a left-  lateralized (left temporal re -
gions) increase in 5–12 Hz during the maintenance of pitches, 
compared to a non-  memory control task. Alpha-  band oscilla -
tions can therefore be considered to reflect the maintenance of 
auditory information. Earlier work has interpreted alpha-  band 
oscillatory responses to either reflect the top-  down control of 
WM representations (Leiberg et  al.  2006) or the inhibition of 
task- irrelevant neural processes (van Dijk et  al.  2010). Either 
way, alpha- band oscillatory responses are closely related to the 
maintenance of auditory information (for a review, see Wilsch 
and Obleser 2016 ), and may therefore track auditory WM load.
Recently, multivariate pattern analysis (MVPA) has been ad -
vocated in the study of higher-  order brain states, as it is more 
sensitive to pick up on complex scalp patterns of neural activ -
ity, compared to univariate methods (Kikumoto and Mayr  2018; 
Peelen and Downing  2023). While most WM decoding studies 
have focused on visual representations, less is known about the 
maintenance of auditory stimulus features. A handful of mul -
tivariate fMRI studies have shown that auditory information 
(e.g., frequency, location, etc.) can be decoded in auditory cor -
tex, inferior frontal cortex, precentral cortex, and superior pa -
rietal lobule (for a review, see Kaiser  2015). Moreover, we are 
not aware of any study using multivariate analyses to investigate 
executive properties (such as load) of auditory WM. Thus, in the 
3 of 18Psychophysiology, 2025
present study, we set out to uncover the spatio- temporal patterns 
of EEG activity relating to auditory WM load.
Considering the large knowledge gap between what we know 
about visual WM and auditory WM, it seems imperative to 
study auditory WM via various methods (especially multivar -
iate methods) used in visual WM literature. Moreover, previ -
ous studies into auditory WM have only used binaural stimuli, 
where potential lateralized (i.e., contralateral-  minus- ipsilateral) 
responses akin to the CDA would remain unnoticed. It there -
fore remains unknown whether the CDA is a modality-  specific 
neural marker for visual WM or whether it is a supra- modal neu-
ral marker that also reflects auditory WM load. In the current 
study, we aimed to identify load-  dependent neural markers of 
auditory WM by recording EEG signals. Specifically, we asked 
two research questions, namely, (1) whether auditory WM load 
is reflected in lateralized neural responses, akin to the CDA 
for visual WM load, and (2) whether we could identify non- 
lateralized load-  dependent neural markers of auditory WM, 
using multivariate pattern analyses.
To address these questions, we conducted an auditory delayed 
change- detection task (e.g., Rouder et al.  2011) while recording 
EEG. On each trial, participants memorized a tone sequence 
comprising 1, 2, 3, or 4 pure tones differing in pitch, thus yielding 
four set sizes. Importantly, this auditory change-  detection task 
was combined with a dichotic listening task (e.g., Hugdahl 2011), 
whereby the to-  be- memorized tone sequence was presented to 
one ear, while a to- be- ignored distractor sequence was presented 
to the other ear. Participants were instructed to memorize the 
tones presented to one ear while ignoring the tones presented 
to the other ear. After a delay period, a probe sound was pre -
sented to the attended ear, with a distractor presented to the un- 
attended ear. Participants were required to indicate whether the 
probe was present or absent in the memory tone sequence. This 
dichotic listening approach allowed us to isolate load- dependent 
and hemisphere- specific EEG responses during the delay period 
of the auditory WM task. By doing so, we could compute the 
contralateral- minus- ipsilateral response differences and com -
pare these between set-  size conditions to identify potential lat -
eralized load-  dependent neural markers of auditory WM (akin 
to the CDA).
We analyzed the EEG data using both univariate and multivar -
iate methods (EEG and decoding), investigating lateralized and 
non- lateralized responses in the time and frequency domain. 
EEG responses are retrieved from the maintenance period when 
participants held varying numbers of pitches (i.e., set-  sizes) in 
auditory WM. For behavioral performance, we expected that the 
estimation of WM capacity should increase with set-  size, level-
ing off at the WM capacity limit. For the univariate EEG results, 
we focused on lateralized responses, namely the CDA responses 
and lateralized alpha oscillations, based on previous visual 
WM studies (Jensen et  al.  2002; Vogel and Machizawa  2004). 
If auditory WM is also reflected in lateralized responses, the 
contralateral- minus- ipsilateral univariate responses and alpha-  
band power should scale with auditory WM set-  size (until it 
levels off at the WM capacity limit). For multivariate pattern 
analysis, we focused on decoding scalp patterns of alpha-  band 
(8–12 Hz) power, based on previous findings that alpha was 
closely related to auditory WM (Leiberg et al.  2006; Wilsch and 
Obleser  2016). If the patterns of alpha oscillation during the 
maintenance period indeed track auditory WM load, the alpha 
oscillation patterns should be distinguishable between load con-
ditions up to the group-  level capacity limitations but fail to dif -
ferentiate among conditions that exceeded this limit, as reflected 
in the auditory WM capacity calculated by the behavioral data.
To preface the results, we found that auditory WM load was not 
reflected in lateralized responses, neither in the time nor in the 
frequency domain. This implies that the CDA is a vision- specific 
rather than a domain- general marker of WM load. Our decoding 
results showed that patterns of alpha-  band oscillations during 
the maintenance period reflected auditory WM load. Moreover, 
the alpha patterns associated with specific load conditions were 
changing throughout the maintenance period, which suggests 
that auditory WM load is reflected in dynamic—rather than 
static—neural population codes. Mirroring the behavioral data 
that the auditory WM capacity is around 2 tones, these load- 
specific EEG responses allowed us to distinguish between load 
conditions within, but not beyond, the group-  level capacity lim-
itations. We thus consider scalp patterns of alpha band power as 
a novel neural marker for auditory WM load.
2   |   Materials and Methods
2.1   |   Participants
To determine the required sample size for a main effect of set- 
size in our within-  participants design, a sample size estimation 
was performed in G*power software (Faul et al.  2009). This sug-
gested that at least 19 participants were required for 85% power 
to observe a medium effect size (Cohen's f = 0.3) with a repeated 
measure ANOVA ( /u1D6FC = 0.05). The medium effect size was in -
ferred based on (1) a general benchmark that is often used when 
effect sizes are a priori unknown, (2) the neural effect sizes in -
ferred from Vogel and Machizawa ( 2004), and (3) one of our pi-
loting behavioral experiment with the same design but having 
set- size 1, 2, 3, 4, 5, and 6. A total of 27 participants were tested 
(18 participants reported their gender as female, 9 as male; mean 
age = 22.41 years, SD = 1.91, range = 19–25 years). We stopped 
testing after enough participants (> 19) met our inclusion crite -
ria for the EEG analyses (for details, see the EEG recording sec -
tion below). Six participants were excluded due to excessive EEG 
artifacts (> 25%). Thus, EEG data of 21 participants were ana -
lyzed. All participants reported normal or corrected-  to- normal 
vision and normal hearing (as tested with a pre-  experiment au-
diogram). They signed informed consent and received money or 
course credits for their participation. The study protocols were 
approved by the faculty ethics committee (FETC) of Utrecht 
University (number 18–048 van der Stoep).
2.2   |   Apparatus and Stimuli
The experiments were conducted in a dimly lit lab and con -
trolled using Matlab 2018a. Participants were seated with their 
heads positioned in a chin rest to keep their viewing distance 
at a fixed 60 cm in front of a 27-  in. monitor. The auditory stim -
uli were played through 3M E-  A- RTONE Insert Earphone 3A 
(10 Ohm).
4 of 18
 Psychophysiology, 2025
The auditory stimuli consisted of 25 pure tones with differ -
ent frequencies and white noises, each lasting for 200 ms. All 
sounds were generated in Matlab 2018a, sampled at 96 kHz. The 
frequencies of the 25 target pure tones ranged from 125 Hz to 
8.1 kHz with a 19% increase in between tones (125, 149, 177, 211, 
251, 298, 355, 422, 503, 598, 712, 847, 1008, 1200, 1428, 1699, 2021, 
2406, 2863, 3407, 4054, 4824, 5740, 6831, 8129 Hz), which should 
be distinguishable for naive listeners (Ahissar et al.  2006). The 
lowest (125 Hz) and highest (8129 Hz) frequencies from this set 
of pure tones were used as distractors, while the remaining 23 
pure tones were used as the set of target stimuli. Linear ramps of 
25 ms were applied both to the beginning and the end of tones to 
prevent auditory pop artifacts. Participants were able to slightly 
adjust the volume to a subjectively comfortable level at the start 
of the WM tasks. Sounds were on average presented at 60 dB (A).
2.3   |   Procedure
2.3.1   |   Pitch Discrimination Task
To make sure that participants could distinguish different pure 
tones, a behavioral pitch discrimination task was conducted be -
fore the main auditory WM task. In this pitch discrimination 
task, each of the 25 pre-  generated pure tones was paired with 
itself, yielding 25 same-  frequency trials. In addition, 23 pure 
tones (except for the lowest and highest ones) were paired with 
their one- step higher or lower neighbors, yielding 46 different- 
frequency trials. Finally, the lowest tone was paired with its 
one- step higher neighbor, and the highest tone with its one-  
step lower neighbor, yielding 2 additional different-  frequency 
trials. This resulted in a total of 73 trials (pairs), consisting of 
25 same-  frequency and 48 different-  frequency trials. On each 
trial, one pair of tones was presented bilaterally and sequen -
tially. Participants were required to indicate whether the two 
tones were the same or different. All pairs were presented once. 
Accuracies in the task for all participants were higher than 85% 
(M = 97.2%, SD = 2.86%, range = 89%–100%), indicating that par-
ticipants could distinguish the different tones; therefore, no par-
ticipants were excluded based on this criterion.
2.3.2   |   Auditory WM Task
After the pitch discrimination task, participants performed the 
auditory WM task during EEG recording. In this WM task, a 4 
(set- size: 1, 2, 3, vs. 4) × 2 (attended side: Left vs. Right) within- 
participants design was adopted. At the beginning of each trial, 
participants were always given instructions to remind them of 
which side to attend to. They were required to memorize the 
pitches of a sound sequence presented on the attended side, 
while ignoring the sound sequence presented on the unattended 
side. The manipulation of the to-  be- attended side was blocked, 
while set- size varied randomly from trial to trial. The order of 
blocks was counterbalanced across participants.
On each trial, a fixation cross appeared at the center of the 
screen for 1000 ms, after which two different sound sequences 
were presented separately to each ear. These two sequences 
were presented simultaneously, comprised the same number of 
pure tones, but differed in pitch. The sound sequence consisted 
of four sounds, separated by inter-  sound intervals. Each sound 
was either a pure tone or a white noise burst, depending on the 
experimental condition. The duration of the pure tones, the 
white noise, and the inter-  tone intervals was 200 ms, yielding 
a sound sequence that consistently lasted for 1400 ms. For the 
attended side, the last one (set- size 1), two (set- size 2), three (set- 
size 3), or four (set- size 4) sounds were randomly sampled with -
out replacement from the predefined set of 23 target pure tones, 
and participants were required to memorize the exact pitches of 
these pure tones. White noise bursts were used to fill up the se -
quence where no pure tone was presented (i.e., in set sizes below 
4; see Figure  1). For the unattended side, the last one (set-  size 
1), two (set- size 2), three (set-  size 3), or four (set-  size 4) sounds 
consisted of distractor sounds. The distractor sound was either 
the lowest (125 Hz) or the highest frequency (8.1 kHz) from the 
predefined distractor set of pure tones (with equal probability) 
and was repeated once (in set- size 1 condition), twice (in set- size 
2 condition), three times (in set-  size 3 condition), or four times 
(in set- size 4 condition), matching the number of pure tones on 
the attended side. Similarly to stimulus presentation in the at -
tended side, white noise bursts were used to fill up the sequence 
of pure tones in the unattended side (i.e., in set sizes below 4). 
After the presentation of the sound sequence, a maintenance 
period of 2000 ms followed, during which participants had to 
hold the pitches in memory (1–4 target sounds). Finally, after the 
maintenance period, two sounds were presented for 200 ms, sep-
arately to the attended and unattended side. The probe sound on 
the attended side was the test sound, which could either be pres-
ent (50% trials) or absent (50% trials) in the memorized sound 
sequence. On target-  present trials, the probe sound was ran -
domly selected from the memorized sound sequence with equal 
probability. On target-  absent trials, a tone from the memorized 
sound sequence was similarly selected but substituted with an 
adjacent pure tone (i.e., one step higher or one step lower in the 
pre- generated target set of 23 pure tones). The sound on the un -
attended side was the same distractor that was presented in the 
original sound sequence (125 Hz or 8.1 kHz). After the offset of 
the probe sound, participants were required to indicate as ac -
curately as possible whether the probe sound on the attended 
side was present or absent in the memorized sound sequence 
while ignoring the sound on the unattended side. After the re -
sponse (present vs. absent), the next trial started (see Figure  1). 
Overall, participants completed a total of 416 trials divided into 
eight blocks: two practice blocks of 16 trials each, followed by six 
experimental blocks of 64 trials each.
2.4   |   EEG Recording
EEG was recorded at a sample rate of 2048 Hz from 32 standard 
electrode sites placed according to the international 10/20 sys -
tem using a BioSemi EEG system. Six additional EXG flat-  type 
electrodes were used to record horizontal and vertical eye move-
ments and provide mastoid references. During the experiment, 
participants were instructed to fixate on the center of the mon -
itor and try not to make horizontal or vertical eye movements.
The offline analysis of EEG data was performed using Matlab 
2022a ( https:// www. mathw orks. com/ ) and eeglab 14.1.2b 
(Delorme and Makeig  2004). For pre-  processing, EEG data 
were first re-  referenced to the average of all 32 channels. Then 
5 of 18
Psychophysiology, 2025
a 0.01–40 Hz band- pass filter and a 50 Hz notch filter were ap -
plied to remove high frequency noise and electromagnetic radi -
ation from the environment. After the filtering, EEG data were 
down- sampled to 256 Hz to speed up computation. Then, an 
infomax independent component analysis (ICA) algorithm (Bell 
and Sejnowski  1995) was applied to correct the signal for eye 
movement artifacts. The SASICA plugin was used to automati -
cally identify the artifact component (Chaumon et al.  2015). On 
average, 1 independent component was rejected per participant 
(SD = 0.71, range = 0–2).1 Furthermore, the EEG signals were 
segmented into 5500 ms epochs ( −1000 to 4500 ms relative to 
the onset of the sound sequence) separately for each attended 
side and set-  size condition. The interval of 0–200 ms prior to 
the onset of the sound sequence served as baseline. Finally, if 
the voltage value at any time point in the epoch on any of the 
32 channels exceeded ±200 μV, this epoch was excluded from 
further analysis. Six participants were excluded because an ex -
cessive number (> 25%) of EEG epochs were removed (i.e., volt -
ages exceeding ±200 μV). The average epoch rejection rate of 
the remaining participants was 6.40% of all trials (SD = 6.67%, 
range = 0%–24.7%).2
2.5   |   Behavioral Data Analyses
Accuracy rate and working memory capacity K were calculated 
separately for each participant in each experimental condition 
(Equation  1; Rouder et al.  2011). In the equation, K is WM capac-
ity, N is the number of items in the memory sequence (set-  size), 
and H and F are the observed hit rates and false alarms in Set- 
size N condition, respectively. Moreover, participants whose ac -
curacy and/or WM capacity K exceeded ±3 SD of the group mean 
were identified as outliers and removed. The ±3 SD threshold 
is commonly used in EEG and behavioral research to identify 
outliers that may reflect misunderstanding, disengagement, 
or atypical strategies (Berger and Kiefer  2021; Mohanathasan 
et al.  2024). In the present study, this criterion led to the exclu -
sion of data from one participant.
Bayesian repeated measures analyses of variance (RM ANOVAs) 
were conducted separately for mean accuracy and mean auditory 
WM capacity K with factors Set-  size (1, 2, 3, vs. 4) and Attended 
side (Left vs. Right) using JASP 0.17.3.0 (JASP Team  2024). The 
default priors were applied while the seed value was consis -
tently set to 1 for repeatability. Moreover, effects were evaluated 
across matched models (Mathôt  2017), by comparing models 
containing the factor of interest to equivalent models without 
this factor. This approach provides an “Inclusion Bayes Factor” 
(BFincl), which reflects the amount of evidence for or against the 
specific (main or interaction) effect of interest. We followed the 
guidelines suggested by Kass and Raftery ( 1995) for the interpre-
tation of Bayes factors. Specifically, BFs larger than 3 signified 
substantial (or more) evidence in favor of the effect; BFs between 
0.3 and 3 signified no conclusive evidence in favor of or against 
the effect; BFs smaller than 0.3 signified substantial (or more) 
evidence against an effect.
(1)K = N × (H − F)
FIGURE 1    |    Schematic depiction of the task. Two different sound sequences were presented separately and simultaneously to each ear, whereby 
the participant was instructed to attend one side and ignore the other. On the attended side, the last 1, 2, 3, or 4 sounds (depending on the set-  size) 
of the sequence were pure tones of different frequencies that participants were instructed to memorize. On the unattended side, the last 1, 2, 3, or 4 
sounds in the sequence consisted of the same (lowest or highest pitched) pure tone, which participants could ignore. On both sides, the remaining 
(3, 2, or 1) sounds consisted of white noise. After a 2 s delay, during which participants maintained 1, 2, 3 or 4 sounds in memory, a probe sound was 
presented to the attended side while the to-  be- ignored tone was presented to the other side. Participants were required to indicate whether the probe 
sound was present or absent in the memorized sound sequence.

6 of 18
 Psychophysiology, 2025
2.6   |   EEG Data Analyses
For EEG data analyses, we aimed to answer the following two 
questions: (1) Is auditory WM load reflected in lateralized neural 
responses, akin to the CDA for visual WM load? (2) Can we iden-
tify non-  lateralized load-  dependent neural markers of auditory 
WM? To answer question 1, we computed the lateralized (i.e., 
contralateral minus ipsilateral) EEG response amplitude and the 
lateralized alpha-  band (8–12 Hz) power evoked in the four dif -
ferent set- size conditions. For question 2, we applied multivari -
ate decoding to patterns of alpha- band power across the scalp, as 
measured during the maintenance period. The focus on alpha- 
band over other frequency bands followed from previous studies 
showing a close relationship between alpha oscillations and WM 
maintenance (Leiberg et al.  2006; Wilsch and Obleser  2016). All 
data analyses were performed in Matlab with Fieldtrip toolbox 
(Oostenveld et al.  2011; Donders Institute for Brain, Cognition 
and Behavior, Radboud University, the Netherlands). See http:// 
field tript oolbox. org and MVPA- light toolbox (Treder 2020 ).
2.6.1   |   Lateralized Responses in Time 
and Frequency Domain
To test whether there is an overall lateralized (CDA-  like) re -
sponse (reflecting the instruction to either memorize tones 
on the left or the right side), contralateral and ipsilateral 
EEG responses were averaged across all set-  size conditions. 
Then a cluster-  based permutation test (paired t) (Maris and 
Oostenveld  2007) was conducted to test for a difference be -
tween the contralateral and ipsilateral EEG responses during 
the maintenance period (1400–3400 ms relative to the onset of 
the sound sequence). This permutation test was performed on 
all lateralized electrodes to assess which timepoints exhibit a 
CDA- like response to auditory WM load. The permutation test 
consisted of four steps: (1) Paired- sample t- tests were used to test 
at each time point and each electrode whether the contralateral 
and ipsilateral responses differed at the group level. (2) Clusters 
were defined as contiguous time points for which the t - test was 
significant ( p < 0.05) at least at one electrode. Then, for each of 
these clusters, the t- values were summed to obtain a cluster- level 
t mass. (3) We constructed a null distribution of cluster-  level t 
mass values by randomly swapping the condition label (contra -
lateral or ipsilateral) across trials for each participant, and then 
calculating the maximum cluster-  level t mass at the group level. 
Importantly, labels were swapped for an entire trial (i.e., time- 
series) rather than timepoint-  by- timepoint, to preserve autocor -
relations between timepoints in the null data. By repeating this 
procedure 1000 times, we obtained a null distribution of maxi -
mum cluster- level t mass values. (4) Finally, we computed p val-
ues for each of the clusters in the observed data by computing the 
fraction of permuted data sets containing t mass values at least 
as extreme as that of each observed cluster (using a two-  tailed 
alpha = 0.05). For each significant cluster, we also reported the 
averaged Cohen's d over a rectangular region covering the clus -
ter as effect size (Meyer et al.  2021). We considered channels to 
exhibit a CDA- like response whenever channels yielded a signif-
icant lateralized response throughout the entire cluster.
To test whether the CDA-  like response scaled with set-  size, 
we followed the same procedure as above, but for each set-  size 
condition individually. Another cluster-  based permutation test 
was conducted to compare the lateralized responses across 
four set- size conditions during the maintenance period (1400–
3400 ms relative to the onset of the sound sequence). This per -
mutation test was performed on all lateralized electrodes to 
assess during which timepoints and for which electrodes the 
CDA- like response scales with set-  size.
A similar approach was followed to test for lateralized load- 
dependent responses in the time-  frequency domain (alpha 
power). Instead of using the raw (i.e., voltage) EEG responses, 
a time-  frequency analysis was performed first, using 7-  cycle 
Morlet wavelet decomposition (i.e., mf 0σt = 7; Roach and 
Mathalon  2008) for frequencies ranging between 4 and 30 Hz 
in 1 Hz steps. The Morlet filtering was performed by convolving 
single- trial EEG epochs from each scalp electrode with complex 
Morlet wavelets. A 7- cycle Morlet wavelet was used in this anal -
ysis to provide a good tradeoff between time and frequency res -
olution. The decomposition was performed on 5.5 s EEG epochs 
after the pre- processing described above, ranging from −1000 to 
4500 ms relative to the onset of the sound sequence. After Morlet 
wavelet decomposition of the trials was performed, oscillatory 
power was calculated, by taking the square of the modulus of 
the resulting complex number. Each trial was baseline cor -
rected using a decibel (dB) normalization, with the −200–0 ms 
window before onset of the sound sequence serving as base -
line. Following the approach of previous studies, we focused 
on the power in the alpha frequency band (8–12 Hz) (Leiberg 
et al. 2006 ; Wilsch and Obleser 2016 ).
Cluster- based permutation testing (following the same proce -
dures as above) was performed to test for the existence of a later-
alized alpha response and to test whether this lateralized alpha 
response scales with set-  size.
2.6.2   |   EEG Decoding Analyses
The goal of the decoding analyses was to test for the existence 
of non- lateralized EEG responses that scale with auditory WM 
load. Compared to univariate approaches, multivariate decod -
ing is more sensitive to uncover differences between conditions 
as it leverages the scalp distribution of neural signals, allowing 
for the detection of discriminable patterns that may not be evi -
dent in individual electrodes (Peelen and Downing  2023). Here, 
we set out to classify different load conditions based on the scalp 
distribution of alpha- band power, using the MVPA- light toolbox 
(Treder  2020) in Matlab.
We performed two distinct MVPAs to test whether we could 
distinguish the patterns of activity evoked by different set-  size 
conditions. First, we trained classifiers to differentiate between 
set- size conditions by performing timepoint-  by- timepoint de -
coding (i.e., training and testing the classifier on data from 
the same timepoint within a trial). Six different decoding 
comparisons (set-  size 1 vs. 2, 1 vs. 3, 1 vs. 4, 2 vs. 3, 2 vs. 4, 3 
vs. 4) were performed separately for each time point from the 
onset of the sound sequence to the end of the maintenance 
period. Second, we conducted a temporal generalization anal -
ysis, whereby classifiers were trained and tested on all possi -
ble combinations of timepoints. This temporal generalization 
7 of 18
Psychophysiology, 2025
analysis allowed us to identify whether the neural response 
to auditory WM load was stable over time or was dynamically 
changing during the maintenance period. Here as well, we 
conducted six different decoding comparisons (set-  size 1 vs. 2, 
1 vs. 3, 1 vs. 4, 2 vs. 3, 2 vs. 4, 3 vs. 4). Finally, for both analyses, 
we also performed a searchlight analysis. The significant de -
coding accuracy for each electrode in the searchlight analysis 
would inform us of which electrodes are most informative to 
distinguish between set-  size conditions.
2.6.2.1    |   Decoding: Timepoint-  By- Timepoint Classifica -
tion. To test whether scalp patterns of alpha oscillations tracked 
auditory WM load, we conducted a timepoint-  by- timepoint 
decoding analysis, ranging from the start of stimulus encoding 
to the end of the maintenance period, using electrodes as fea -
tures. To obtain the mean alpha-  band power, the data was first 
down- sampled over time by averaging every five consecutive 
time points (20 ms) without overlap. Then the data was z- scored, 
and data from each set of 5 consecutive trials within the same 
set- size condition were averaged to improve the signal-  to- noise 
ratio. This resulted in 35 compound “trials” (samples) on aver -
age (SD = 2.62, range = 28–38) that could be used for our decod -
ing analyses.
We used linear SVM classifiers with a leave-  one- trial- out cross- 
validation procedure to decode between set sizes. Taking set size 
1 vs. 2 as an example, we performed classification analyses to 
investigate whether the scalp pattern of alpha- band power could 
distinguish between set size 1 and 2 conditions. Above-  chance 
classification would imply that the patterns of alpha- band power 
were load- dependent. Specifically, for a given timepoint, and on 
each cross- validation iteration, one compound trial (i.e., the av -
erage of 5 trials) was drawn from the set size 1 or 2 condition. 
The remaining compound trials were then used to train a linear 
SVM classifier to distinguish between activity evoked in set size 
1 and set size 2 conditions. This classifier was then tested on 
the trial that was left out of the training procedure. To keep the 
number of training examples equal between the two conditions, 
a random selection of trials was removed from the condition 
with more trials. The classification was performed repeatedly 
until each compound trial was used to test the classifier once, 
thus yielding one classifier outcome per compound trial. These 
classifier outcomes were averaged to yield a single decoding ac -
curacy score for a given participant and a given timepoint. This 
procedure was repeated for every timepoint of a trial, and for 
every participant, and for classifying between each of six possi -
ble pairs of set size condition. In a final step, decoding accuracies 
from all six classification pairs were averaged (per timepoint) to 
obtain an overall classification performance for set size.
2.6.2.2    |   Decoding: Temporal Generalization.  To test 
whether the specific patterns of alpha-  band power reflect -
ing the different set-  size conditions were stable or dynamic 
(i.e., varying over time), we performed a temporal general -
ization decoding approach. The procedure was identical to 
that of the timepoint-  by- timepoint decoding described above, 
with the exception that the linear SVM trained at one time 
point was not only tested on the same time point at which 
it was trained, but also tested on all other time points (King 
and Dehaene  2014). Thus, the temporal generalization analy -
ses resulted in a 2-  dimensional matrix of decoding accuracies, 
wherein each timepoint in a trial is used for training and for test-
ing the classifier. If the pattern of alpha-  band power reflecting 
specific set- sizes is dynamically changing over time, significant 
decoding should be found only along the diagonal line (which 
is the same data as the timepoint-  by- timepoint classification 
analysis described above). If the alpha oscillation pattern under-
lying classification performance is stable throughout the delay 
interval, significant decoding should not only be found along 
the diagonal line, but also spread over all combinations of train -
ing and testing times during the maintenance period, resulting 
in a square- like shape of significant decoding performance.
2.6.2.3    |   Decoding: Statistics.  To test for significance 
in the timepoint-  by- timepoint decoding analysis, we followed 
the same cluster-  based permutation approach as described 
for the lateralized univariate responses above. In this case, 
cluster- based permutation tests were applied to compare decod -
ing accuracy against chance level (0.5 for binary classification). 
The cluster- level t mass was computed across one dimension (i.e., 
timepoints within a trial). This permutation test was performed 
for each of the six set-  size comparisons as well as the average 
of all set-  size conditions. For the temporal generalization anal -
ysis, the same cluster-  based permutation approach was used, 
except that the cluster-  level t mass was now computed across 
two dimensions (i.e., train and test timepoints within a trial).
2.6.2.4    |   Decoding: Searchlight Analyses.  To identify 
which electrodes were most informative for distinguishing 
between set-  size conditions, we conducted an independent 
searchlight analysis across all significant decoding time points 
during the maintenance period. The rationale was that elec -
trodes can only be considered informative when decoding accu -
racy is significantly above chance. Specifically, for the set-  size 1 
vs. 2, 1 vs. 3, and 1 vs. 4 comparisons, we defined for each elec -
trode a cluster consisting of its neighboring electrodes. Instead 
of using the entire scalp pattern, we used these local clusters 
as features and performed timepoint-  by- timepoint decoding as 
well as temporal generalization analyses for each participant 
and each significant time point. Decoding accuracies were then 
averaged across the significant set-  size comparisons and across 
the significant decoding time points within the maintenance 
period. Finally, group-  level topographies of decoding accu -
racy were obtained by averaging electrode-  wise accuracies 
across participants. This procedure yielded two topographic 
maps showing which electrodes better distinguished between 
different set-  size conditions during the maintenance period, 
separately for timepoint-  by- timepoint and temporal generaliza -
tion decoding.
To test which electrodes were most informative for distinguish -
ing between set-  size conditions, we performed a permutation 
test. On each of 1000 permutations, we randomly shuffled the 
searchlight decoding accuracy across electrodes for each par -
ticipant and each significant time point, and then applied the 
exact same analysis steps as described above for the observed 
data. For each electrode, we then computed the proportion of 
permutations containing any searchlight decoding accuracy at 
least as high as the searchlight decoding accuracy for that elec -
trode in the observed data. These proportions were interpreted 
as p- values that implicitly account for multiple comparisons (i.e., 
across electrodes).
8 of 18
 Psychophysiology, 2025
3   |   Results
3.1   |   Behavioral Data
For accuracy, we found decisive evidence ( BFincl = 7.85 × 1026) 
in favor of a main effect of Set- size (Figure  2a). Subsequent pair-
wise analyses provided overwhelming evidence that accuracy 
differed between all set-  size conditions (all BFincl > 2.59 × 105), 
showing that accuracy dropped dramatically as the set-  size in -
creased. This indicates that the manipulation of auditory WM 
load was successful. We found no evidence for a main effect of 
Attended side (BFincl =0.73), and substantial evidence against an 
interaction of Set-  size and Attended side ( BFincl = 0.14). Thus, 
accuracy did not systematically depend on left versus right pre -
sentation of the memory array.
For working memory capacity, we also found decisive evi -
dence ( BFincl = 2.68 × 108) in favor of a main effect of Set-  size 
(Figure  2b). In follow- up analyses, we found evidence that WM 
capacity was lower in Set-  size 1 than in Set-  sizes 2, 3, and 4 (all 
BFincl > 2.52 × 105), and that WM capacity was lower in Set-  size 
2 than in Set-  size 3 ( BFincl = 76.87). We found no conclusive 
evidence that WM capacity differed between Set-  sizes 2 and 4 
(BFincl = 1.47), and we found evidence against a difference in 
WM capacity between Set-  sizes 3 and 4 ( BFincl = 0.15). Finally, 
we found no conclusive evidence for a main effect of Attended 
side (BFincl = 0.41), and we found evidence against an interaction 
of Set- size and Attended side (BFincl = 0.09).
Together, these behavioral results demonstrate that estimated 
WM capacity initially increased as the set-  size increased, but 
then leveled off when set- size (the number of items to be memo-
rized) reached 3, and the corresponding WM capacity K equaled 
about 2 items. The relatively low capacity for auditory WM is 
largely consistent with previous studies (Alunni-  Menichini 
et  al.  2014; Li et  al.  2013; Prosser  1995), in which researchers 
also found the maximum capacity of auditory WM was 2.8, 2.9, 
and 2 pure tones, respectively. Importantly, this plateau estab -
lishes that the ceiling of auditory WM capacity (in the present 
experimental setting) is somewhere between two and three 
pitches of pure tones, and indicates that our higher set-  size con-
dition(s) exceeded capacity limitations.
3.2   |   Lateralized Univariate Responses
To test whether auditory working memory load was reflected 
in lateralized neural responses, akin to the CDA for visual WM 
load, we calculated interhemispheric differences for each set- 
size condition for both mean univariate responses (time domain) 
and mean alpha-  band power (frequency domain) during the 
maintenance interval. Two cluster- based permutation tests were 
performed to test (1) whether an overall lateralized response is 
observed during the maintenance period, reflecting the side of 
the attended memory items, and (2) whether this putative later -
alized response scales with set-  size.
Testing for a lateralized response across set- sizes in the time do-
main revealed a significant cluster across the whole maintenance 
period (between 1400 and 3400 ms after stimulus onset), with 
stronger contralateral compared to ipsilateral activity ( t- mass 
= − 6.80 × 103, p < 0.01). The average effect size over a rectan -
gular region spanning 10 channel pairs and 1400–3400 ms was 
d = −0.59. This negative difference waves confirms the existence 
of a CDA- like response during the maintenance interval, indicat-
ing the validity of our attention manipulation (Figure  3a). This 
lateralized response, however, did not differ between set-  size 
conditions (no significant clusters were observed), suggesting 
that auditory WM load is not reflected in lateralized responses.
Conducting the same two analyses with alpha-  band power 
(in the frequency domain) revealed no significant clusters 
(Figure  3c); neither when collapsing across set sizes, nor when 
testing for differences between set sizes.
In sum, substantial lateralized responses were found in the time 
domain, reflecting which side was attended for the memory task. 
This demonstrates that our attention manipulation (attend left 
FIGURE 2     |    Results of behavioral performance. Panel (a) shows the accuracy, and panel (b) shows the auditory working memory capacity esti -
mate K, separately for set- size 1 (red), 2 (blue), 3 (green) and 4 (black) conditions. In all plots, the mid-  black- line in the box plot represents the group 
mean. *Indicates evidence in favor of the post hoc differences; ø indicates inconclusive evidence (1/3 < BF10 < 3); ⊙ indicates evidence against the 
post hoc difference.

9 of 18
Psychophysiology, 2025
or attend right) was successful. However, we found no evidence 
that auditory WM load was reflected in lateralized responses, 
neither in the time nor in the frequency domain, suggesting that 
the CDA is a modality- specific marker for visual WM load rather 
than a supra- modal marker.
3.3   |   Alpha- Band Power Decoding
3.3.1   |   Timepoint- By- Timepoint Classification
We set out to test whether WM load could be decoded from 
scalp patterns of EEG alpha-  band oscillations. To this end, we 
trained a linear SVM classifier to distinguish between patterns 
of alpha- band power evoked by different set- size conditions. For 
this first decoding analysis, the classifier was trained and tested 
using data from the same time point in a trial (i.e., timepoint- 
by- timepoint decoding), ranging from the onset of the memory 
sequence to the end of maintenance period. The results of the 
cluster- based permutation test showed that, overall, set-  size 
could be reliably decoded from alpha-  band power from around 
450 ms after the onset of the memory sequence, until around 
3000 ms, thereby covering most of the encoding and mainte -
nance period (1 cluster, p < 0.001, dmean = 0.78; see Figure  4). 
The independent searchlight analyses showed that the centro- 
parietal electrodes were most informative to the decoding of 
auditory WM load during the maintenance periods. Thus, au -
ditory WM load can be decoded from scalp patterns of alpha- 
band power.
We then investigated for each pair of set-  size conditions in -
dividually, whether they evoked discriminable scalp patterns 
of alpha-  band power (i.e., 1 vs. 2, 1 vs. 3, 1 vs. 4, 2 vs. 3, 2 
vs. 4, and 3 vs. 4). As can be seen in the six smaller panels of 
Figure  4, significant decoding during the maintenance period 
was found for the set-  size 1 versus 2 (1300–1750 ms; 1 cluster, 
p < 0.001, dmean = 0.71), set- size 1 versus 3 (1400–2200 ms, and 
2300–3000 ms; 2 clusters, both p  < 0.01, dmean = 0.66 and 0.60), 
and set-  size 1 versus 4 (1400–2650 ms, and 2850–3050 ms; 2 
clusters, both p  < 0.05, dmean = 0.78 and 0.74). A visualiza -
tion of alpha power patterns during the maintenance period 
is shown in Figure  5. These results showed that patterns of 
alpha- band oscillations during the maintenance period can 
distinguish between set-  sizes of 1 and higher, but not between 
set- sizes of 2 and higher (which are above the group-  level ca -
pacity estimations).
3.3.2   |   Temporal Generalization
In a final set of analyses, we set out to test whether the scalp 
patterns of alpha-  band power reflecting auditory WM load are 
FIGURE 3    |    Lateralized (contralateral minus ipsilateral) response, and its topographical distribution. (a) Left: Grand average lateralized response 
in the time domain data averaged across all set- size conditions and all electrodes, shown from baseline (−0.2 ms) until the end of retention (3.4 s). The 
shaded areas depict the standard error of the mean. The vertical dashed lines indicate (from left to right) the onset of the tone sequence, the onset of 
the maintenance period, and the end of the maintenance period. The horizontal purple line indicates a significant lateralized effect (deviating from 
0) collapsed across all four set- size conditions. Right: The topographical maps depict the magnitude of the overall lateralized effect ( t- value) averaged 
across four set- size conditions during the time window with significant lateralized effects. Electrodes where these effects are significant are marked 
with an * (if any). (b) Left: Lateralized responses in the time domain data measured in the set-  size 1 (red), 2 (blue), 3 (green), and 4 (black) conditions, 
averaged across all electrodes. Right: The topographical maps depict the magnitude of the set-  size effect ( F- value) averaged across four set-  size con-
ditions during the time window with significant lateralized effects. Panel (c, d) depict the same as panel (a, b), but for lateralized alpha-  band power.

10 of 18
 Psychophysiology, 2025
stable, or vary dynamically over the course of the maintenance 
period. To this end, we performed temporal generalization anal-
yses, whereby linear SVM classifiers were trained and tested on 
data from all possible combinations of timepoints (thus yielding 
a 2D decoding matrix, instead of a time-  series). When consid -
ering all set-  sizes together, we replicated the finding that set- 
size can be decoded from scalp patterns of alpha-  band power 
during the maintenance period (from 400 to 3400 ms, 1 cluster, 
p < 0.001, dmean = 0.25). Importantly, the present analysis also 
shows that significant set-  size decoding (depicted in black in 
Figure  6) is way more prevalent on-  diagonal than off-  diagonal, 
indicating that the specific pattern of alpha-  band power associ -
ated with different set-  sizes varies over the course of the main -
tenance period.
These findings are largely confirmed when considering the six set- 
size comparisons in isolation. As shown in the six smaller panels, 
temporal generalization decoding during the maintenance period 
revealed significant decoding for set- sizes 1 versus 2 (1400–1950 ms; 
1700–3200 ms, 2 clusters, both p  < 0.05, dmean = 0.46 and 0.36), 1 
versus 3 (1400–3250 ms, 1 cluster, p < 0.001, dmean = 0.38), and set- 
size 1 versus 4 (1450–3350 ms, 1 cluster, p  < 0.001, dmean = 0.38). 
Again, no significant decoding performance was found for set-  
sizes 2 versus 3, 2 versus 4, and 3 versus 4, thus mirroring the re-
sults of the timepoint- by- timepoint decoding analysis.
In sum, we found that scalp patterns of alpha-  band power 
during the maintenance period reflect auditory WM load, with 
FIGURE 4     |    Timepoint- by- timepoint decoding of scalp patterns of alpha-  band (8–12 Hz) power. All panels depict decoding accuracy ( y- axis) as a 
function of time (x- axis). The big panel depicts decoding accuracy averaged across all six pairwise comparisons (i.e., main effect set-  size), which are 
depicted individually in the surrounding smaller panels. Bold blue lines indicate significant above chance (50%) decoding, based on cluster-  based 
permutation testing to account for multiple comparisons. The vertical dashed-  purple lines split time into the encoding and maintenance periods. 
The topographical map depicts the most informative sites for distinguishing between set-  size conditions during the maintenance period, based on 
a separate searchlight analysis. Electrodes with significant information for distinguishing between set-  size conditions are marked with an *. In the 
small panels, the blue squares indicate the target tones, while the blurred squares indicate the white noise.
FIGURE 5     |    Scalp topographies of alpha-  band (8–12 Hz) power 
during the maintenance period for set-  size 1, 2, 3, and 4 conditions. 
Each row corresponds to one set- size condition, and each column shows 
a topographic map averaged over a 200- ms time window within the 
maintenance period.

11 of 18
Psychophysiology, 2025
centro- parietal electrodes being most informative to distinguish 
between set sizes. These load- specific EEG responses allowed us 
to distinguish between load conditions up to the group-  level ca-
pacity limitations, but not between load conditions exceeding this 
limit, as established from the behavioral data (i.e., around K = 2). 
Interestingly, the specific patterns of alpha-  band power that re -
flected specific set- size conditions evolved dynamically across the 
maintenance period, suggesting the dynamic coding of auditory 
WM load.
4   |   General Discussion
In the present study, we set out to investigate whether auditory 
WM load is reflected in lateralized neural responses, akin to 
the CDA for visual WM load. We further attempted to iden -
tify other (non-  lateralized) load-  dependent neural markers of 
auditory WM, using multivariate pattern analysis (MVPA). To 
these aims, we recorded EEG while participants were holding 
the pitches of 1, 2, 3, or 4 tones in WM for a subsequent audi -
tory recognition task. The behavioral results showed that au -
ditory WM capacity plateaued between two and three tones. 
Two key findings emerged from the analyses of EEG data. 
First, although we identified a lateralized (CDA-  like) response 
during the maintenance period, this response did not scale 
with set-  size; neither in the time nor in the frequency (alpha 
oscillation) domain. Thus, we found no evidence that WM load 
was reflected in lateralized responses. Second, using MVPA, 
we found that scalp patterns of alpha-  band power during the 
maintenance period reflected auditory WM load. These load-  
specific EEG responses were mostly confined to bilateral 
centro- parietal channels, and allowed us to distinguish be -
tween set- size conditions up until—but not above—group level 
capacity limitations (i.e., about 2 items, based on the behav -
ioral data). Interestingly, we also found that the scalp patterns 
of alpha- band power reflecting specific auditory WM were not 
stable across the maintenance period. Instead, these patterns 
dynamically changed across the maintenance period, with pat -
terns evoked at the start of the maintenance period barely gen -
eralizing to patterns at the end of the interval, and vice versa. 
In short, our results show that dynamic scalp patterns of alpha-  
band power can be used as a novel neural marker of auditory 
WM load. In the following sections, we will first discuss what 
it means that (unlike for visual WM load) auditory WM load is 
not reflected in lateralized responses. Then, we will elaborate 
on the scalp patterns of alpha power that were shown to track 
auditory WM load, and discuss what they tell us about the neu -
ral coding of auditory WM.
FIGURE 6    |    Temporal generalization decoding of scalp patterns of alpha- band (8–12 Hz) power. The big panel depicts decoding accuracy averaged 
across all six pairwise comparisons (i.e., main effect set-  size), which are depicted individually in the surrounding smaller panels. In each plot, each 
data point corresponds to a classification analysis performed with training data from one time point ( x- axis) and tested on another time point (y- axis). 
Black data points in each plot indicate significant above chance (50%) decoding, based on cluster-  based permutation testing to account for multiple 
comparisons. The dashed-  purple lines split time into encoding and maintenance periods. The topographical map depicts the most informative sites 
for distinguishing between set-  size conditions during the maintenance period, based on a separate searchlight analysis. Electrodes with significant 
information for distinguishing between set-  size conditions are marked with an *.

12 of 18
 Psychophysiology, 2025
4.1   |   No Lateralized Responses to Auditory 
WM Load
In the current study, we identified a lateralized univariate 
response during the WM delay, akin to the CDA for visual 
WM. Control analyses indicated that the observed lateral -
ized response is unlikely to be driven by eye movements (see 
Supporting Information  S1 for more details). Unlike the CDA, 
however, we found no evidence that the lateralized response 
to auditory WM was modulated by load, neither in the time 
nor in the frequency domain. That is, whereas the amplitude 
of the CDA increases when visual WM load increases, the lat -
eralized responses to auditory WM load observed in our study 
did not differ between load conditions. This raises the ques -
tion of why auditory WM load is not reflected in lateralized re -
sponses, while visual WM load is, even when both require the 
maintenance of lateralized sensory input? We approach this 
question from a cognitive, an anatomical, and a functional 
perspective.
From a cognitive perspective, our results can be framed in 
the context of the multi-  component model of WM, proposed 
by Baddeley and Hitch  ( 1974). The absence of a lateralized 
response to auditory WM load suggests that the CDA, as ob -
served for visual WM, may reflect load in the visuo-  spatial 
sketchpad specifically, rather than load in the domain-  general 
central executive or episodic buffer. Thus, although regulating 
the quantity of information in WM (i.e., load) may be regarded 
as an executive process, sustained neural responses tracking 
visual WM load (i.e., the CDA) may instead be more sensory-  
like and depend on the specific content that is maintained in 
WM. This may explain why neural markers of WM load are 
not so much observed in frontal electrodes—that are typi -
cally associated with executive processes—but tend to arise in 
sensory-  specific processing regions. That is, the CDA is typi -
cally most pronounced in posterior electrodes for visual WM, 
and we found neural responses tracking auditory WM load 
(scalp patterns of alpha power, discussed below) to arise pre -
dominantly around centro-  parietal electrodes. Accordingly, 
different modalities may rely on qualitatively distinct storage 
mechanisms. However, as our data are restricted to the audi -
tory modality, further cross-  modal investigations are needed 
to directly assess this distinction.
From an anatomical perspective, the differences between vi -
sual and auditory WM may be due to the difference in the vi -
sual and auditory processing pathways, leading from sensory 
receptors to the cortex. For the visual pathway, due to the optic 
chiasm, items presented in the left hemifield are projected to 
the right primary visual cortex, whereas items presented in 
the right hemifield are projected to the left primary visual cor -
tex (De Moraes  2013; Rodieck  1979). Thus, these hemisphere-  
specific responses during stimulus encoding may foster a 
difference between contralateral and ipsilateral responses 
during the WM delay, when items on one side are to be re -
membered while items on the other side are to be ignored. In 
the case of auditory processing, however, the input to each ear 
is first extensively processed and combined subcortically, be -
fore being projected to the left and right primary auditory cor -
tex (Pickles  2015). Specifically, the superior olivary complex 
receives information from both contralateral and ipsilateral 
ears to support sound localization. Then the auditory infor -
mation is projected to both contralateral and ipsilateral sides 
of the superior colliculus (Hackney  1987), before projecting 
to the primary auditory cortices. Thus, for the auditory path -
way, tones presented via the left or right ear activate both the 
left and right auditory cortex, albeit with a bias toward the 
contralateral auditory cortex (Lipschutz et al.  2002 ; Woldorff 
et  al.  1999). This slight contralateral dominance in auditory 
processing might explain the overall lateralized responses 
that we observed during the WM delay. Importantly, however, 
contralateral dominance is much weaker in auditory process -
ing than in visual processing because auditory input from 
both ears is largely integrated subcortically (Schwartz  1992). 
This reduced lateralization during auditory processing may 
explain the absence of a load-  dependent modulation in later -
alized responses for auditory WM load.
From a functional perspective, the reason for why we did not 
find a lateralized response to auditory WM load might stem 
from the different organizational principles of auditory com -
pared to visual information. In visual WM tasks, visual infor -
mation is processed via spatial coding, while in auditory WM 
tasks, auditory information may be processed predominantly 
through temporal coding. For instance, while it is known that 
observers use spatial location as an organizational principle 
to help maintain visual information (even if the spatial loca -
tion is irrelevant for the task at hand (Arora et al.  2025; van 
Ede et al.  2019)), several studies have shown that auditory spa -
tial information only has an effect on working memory and 
perception when space is relevant for the task at hand (Klatt 
et al.  2018a, 2018b). In the current study, the spatial location 
of the to-  be- memorized array was irrelevant for the auditory 
WM recognition task. In contrast to the spatial organization 
observed during the maintenance of visual WM items, the 
maintenance of auditory WM items (such as pitches of pure 
tones) may be organized within a temporal reference frame, by 
iterating through the different items over time. This interpre -
tation fits well with the classical example of the phonological 
loop (the auditory counterpart of the visuo-  spatial sketchpad) 
as the repetition of sequences of items over time, such as the 
digits of a to-  be- memorized phone number. In this case, at 
any given timepoint (in a singular brain area), although load 
may influence the overall system state, the number of items 
concurrently represented in working memory at each point in 
time is always 1. If auditory WM items are indeed segregated 
over time rather than over space, then their location is un -
likely to be encoded or retained, and thus a lateralized neural 
response to load would not be expected to scale with set-  size. 
The finding that our neural markers of auditory WM load 
(scalp patterns of alpha oscillations) appear to change over 
the course of the maintenance period (see below) is very much 
in line with this idea of temporal coding. Following the same 
line of reasoning, we also consider it unlikely that presenting 
sounds from different horizontal locations within the same 
hemifield would produce lateralized ERP responses that scale 
with set-  size.
Another possible explanation is that participants may have 
perceptually grouped the sequential tones into a melodic 
structure, thereby reducing the item-  specific set-  size effect. 
However, our task design discouraged such strategies by 
13 of 18
Psychophysiology, 2025
using single-  tone probes, and previous studies observed load-  
dependent ERP effects under similar sequential presentations. 
Moreover, behavioral results revealed a capacity plateau at 
around two items, consistent with item-  based working mem -
ory. Thus, while we cannot fully rule out melodic encoding, it 
is unlikely to be the sole factor underlying the null ERP load 
effect.
Notably, given the similarity between our paradigm and the 
original SAN studies (Alunni-  Menichini et  al.  2014; Lefebvre 
et  al.  2013), we examined whether auditory working memory 
load was reflected in non-  lateralized neural responses during 
the maintenance period. To this end, we tested for differences 
between set sizes using both univariate ERP responses and 
multivariate decoding of scalp voltage patterns (see Supporting 
Information  S1 for more details). In short, during the encod -
ing period, we observe clearly distinct EEG responses to target 
pure tones compared to white noise distractors, which were 
also reflected in the distinct time windows of significant decod -
ing across set-  size comparisons (e.g., 1 vs. 4, compared to 3 vs. 
4). Although a sustained anterior negative wave was observed 
during the maintenance period, both univariate and multivar -
iate analyses revealed that EEG responses during the delay 
were not reliably modulated by set size. Thus, non-  lateralized 
responses did not scale with set size in the current study.
Taken together, the absence of both lateralized and non- 
lateralized ERP set-  size effects during the maintenance period 
suggests that, at least in the present paradigm, ERP activity did 
not reflect abstract non-  spatial working memory representa -
tions. This interpretation is consistent with the view that previ -
ously reported lateralized effects (such as CDA) may be tied to 
spatially specific, sensory-  like storage mechanisms (e.g., Klaver 
et al. 1999 ; Talsma et al. 2001 ).
4.2   |   Alpha Patterns Reflecting Auditory WM Load
In recent years, multivariate pattern analysis has become in -
creasingly prominent in working memory research, provid -
ing sensitive measures of internal memory states beyond what 
univariate ERPs can reveal. A growing body of recent visual 
WM studies has shown that multivariate EEG decoding also 
provides a sensitive and reliable measure of visual working 
memory load (Adam et al.  2020; Jones, Diaz, et al.  2024; Jones, 
Thyer, et al.  2024; Thyer et al.  2022; Yu and Lau  2024; Yu and 
Lau  2025; see Awh and Vogel 2025, for review). Notably, a recent 
cross- modal study demonstrated that both visual and auditory 
WM load can be decoded from broadband EEG signals (Suplica 
et al.  2025). Our decoding findings contribute to this growing 
body of literature by focusing on auditory WM, showing that 
auditory WM load can be decoded from scalp patterns of alpha- 
band activity, and that these load-  related patterns change dy -
namically during the maintenance interval.
First, using both timepoint-  by- timepoint decoding and tem -
poral generalization decoding, we found that scalp patterns of 
alpha- band power during the delay period allowed distinguish -
ing between individual load conditions up until WM capacity 
limitations (set- size 1 vs. 2, 1 vs. 3, 1 vs. 4). In contrast, patterns 
of alpha- band power during maintenance could not distinguish 
between load conditions that exceeded capacity limitations 
based on the behavioral results (set-  size 2 vs. 3, 2 vs. 4, 3 vs. 4). 
The correspondence between these behavioral results and de -
coding results further substantiates that patterns of alpha-  band 
power specifically reflect auditory WM load. The differences 
in alpha-  band power patterns between load conditions might 
reflect content-  invariant differences in executive demands: for 
instance, competition between items or switching from one item 
to another during the delay, which scales with the number of 
tones held in working memory (Leiberg et al.  2006). The more 
tones held in memory, the more resources had to be allocated 
over areas where representations of the to-  be- memorized stim-
uli are presumably stored. Importantly, the topographical maps 
reveal that alpha power patterns were most pronounced in the 
set- size 1 condition, but their overall amplitude decreased with 
increasing WM load (set-  size 2–4), indicating an overall atten -
uation of alpha activity as more items were held in working 
memory. This decrease is consistent with recent accounts that 
interpret attenuated alpha activity as reflecting stronger recruit -
ment of task- relevant sensory areas for mnemonic retention and 
attentional prioritization (Fukuda et  al.  2015; van Ede  2018). 
Notably, previous studies have also found alpha power increase 
with working memory load. In these studies, the role of alpha 
oscillations is interpreted to reflect top-  down inhibition of task- 
irrelevant sensory input and/or task-  irrelevant neural processes 
(Kaiser et al.  2007; van Dijk et al.  2010; Wilsch and Obleser 2016). 
Most of the studies, however, compared responses in a memory 
task to that of a non-  memory control task and found stronger 
alpha- band power in the memory task. Therefore, during the 
maintenance period in the memory task, participants had to 
inhibit irrelevant information for successful retention while 
participants did not need to do so in the non-  memory control 
task. In the current study, we instead compared different load 
conditions. In these different load conditions, the number of to- 
be- remembered items (presented to the attended side) varied, 
but the number of to-  be- ignored distractor items (presented to 
the unattended side) was constant. The set-  size of the distrac -
tors, therefore, did not covary with the set-  size of the memory 
items. As such, the differences in scalp patterns of alpha-  band 
power between set- size conditions reflect WM load, rather than 
distractor inhibition. Thus, our findings reveal the role of alpha 
oscillations in the maintenance of information in auditory WM.
Second, the absence of generalization between the encoding and 
maintenance period (in our temporal generalization analyses) 
indicates that our significant decoding during the maintenance 
period specifically reflects maintenance-  related processes, 
rather than residual signals from the encoding period. Focusing 
on the maintenance period, our temporal generalization analy -
ses suggest that the scalp patterns of alpha-  band power associ -
ated with specific WM loads are not stable over time, but change 
over the course of the maintenance period. One possible inter -
pretation of this is that auditory WM load is inherently repre -
sented through dynamic coding (akin to visual WM content; see 
Stokes  2015). In the context of load, changing neural representa-
tions may also reflect the interplay, over time, between sensory 
regions involved in maintenance and frontal regions involved 
in executive processes. Another potentially related possibility 
could be that participants were maintaining the different pitches 
sequentially (i.e., as they were presented). In this scenario, the 
changing patterns of alpha-  band power associated with specific 
14 of 18
 Psychophysiology, 2025
load conditions may reflect the duration of the sequence or the 
number of consecutive items in a sequence. It should be noted, 
though, that in the later stages of the delay period, we did ob -
serve some off-  diagonal decoding, indicating some temporal 
generalization of the load-  specific responses. This may either 
reflect smearing out of the load-  specific responses as they de -
synchronize over time, or it may reflect the stabilization of the 
memory content into a format that is relevant for the upcoming 
test (the timing of which was predictable). During most of the 
delay period, however, decoding of individual load conditions 
was substantially more pronounced on the diagonal compared 
to the off- diagonal. We therefore conclude that, overall, patterns 
of alpha-  band power reflecting auditory WM load change dy -
namically during the maintenance period. Future research is 
needed to understand what cognitive processes or storage mech-
anisms underlie these dynamics.
Finally, if neural markers of WM load (such as scalp patterns 
of alpha- band power) are modality specific, they would be ex -
pected to mostly involve sensory processing regions. Indeed, 
we found that bilateral centro-  parietal electrodes were most 
distinguishable to the decoding of auditory WM load during 
the maintenance periods, rather than posterior or frontal elec -
trodes in visual working memory studies. Previous studies 
have shown the involvement of temporo-  parietal regions, in -
cluding auditory cortex and supramarginal gyrus, in auditory 
WM (Gaab et al.  2003; Grimault et al.  2014; Koelsch et al.  2009). 
Consistently, here the searchlight analyses revealed that pat -
terns in bilateral centro-  parietal were most distinguishable 
across set- sizes in classification. This is in line with the sensory 
recruitment hypothesis (Gayet et  al.  2018; Katus et  al.  2015; 
Scimeca et  al.  2018; Silvanto and Soto  2012), which has been 
more extensively studied in visual WM and proposes that the 
same neural populations that represent sensory features during 
perception are also recruited during WM maintenance, thereby 
reducing cortical redundancy.
Taken together, our decoding results identified alpha-  band pat-
terns as a neural marker of auditory working memory load, re -
flected in reduced alpha activity. Such decreases are commonly 
interpreted as stronger sensory recruitment, which is consis -
tent with our searchlight analyses showing that centro-  parietal 
channels were most informative in distinguishing set-  size 
conditions. This interpretation is also in line with accounts of 
temporal coding (e.g., rehearsal) in auditory working memory, 
in which repeating tones are thought to be maintained within 
auditory cortical areas. Moreover, our temporal generalization 
results revealed dynamically changing load-  related patterns, 
further supporting the view that auditory WM relies on tempo -
rally coded rehearsal of pure tones within auditory cortex, in 
line with the sensory recruitment hypothesis.
4.3   |   Limitations
One may argue that the capacity of auditory WM is relatively 
low (around 2 tones) in the current study. However, this rela -
tively low capacity is largely consistent with previous studies 
(Alunni- Menichini et al.  2014; Li et al.  2013; Prosser  1995), in 
which researchers also found the maximum capacity of auditory 
WM was 2.8, 2.9, and 2 pure tones, respectively. It should be 
noted that calculations of WM capacity are estimates, and do not 
reflect perfect measurement of WM capacity. Indeed, capacity 
estimates should theoretically remain constant across set-  size 
conditions, but the estimate of WM capacity K is known to vary 
when large differences in set-  size are used (Rouder et al.  2011). 
Thus, it is unclear whether auditory WM capacity in our study 
should be estimated to be around 2 items (the actual capacity 
estimate K) or at ~3–4 items (the set- size conditions at which the 
capacity estimate K started to plateau). Could the challenging 
dichotic presentation tasks employed in our study have reduced 
capacity estimates? Studies using binaural stimulation typically 
show that observers can ignore the unattended auditory stream 
with little to no effort, yielding virtually no interference to the 
processing of the attended auditory stream (Alho et  al.  1994; 
Carpenter et al.  2002). Thus, the use of binaural stimulation is 
unlikely to have substantially reduced capacity estimations in 
our study. Taken together, the present behavioral results cannot 
be taken to reflect a universal auditory WM capacity limit, but 
they do demonstrate the relatively low capacity as compared to 
(for instance) visual WM in similar task designs. 3
Another potential limitation is that we manipulated the to-  be- 
attended side in a block-  wise rather than trial-  wise manner. 
The majority of visual WM studies reporting CDA effects used 
trial- wise cueing, which could be argued to enhance lateralized 
responses. We opted for a block design to minimize confusion 
in our challenging dichotic auditory task, following extensive pi-
loting. Importantly, however, earlier work has reported reliable 
visual CDA effects using blocked designs (e.g., Katus et al.  2015), 
suggesting that CDA components can be successfully elicited 
and measured under blocked conditions. Thus, it seems unlikely 
that the absence of CDA effects in the current study is solely due 
to the blocked design.
A final limitation concerns statistical power for detecting set- size 
differences in lateralized ERP responses. According to Ngiam 
et al. ( 2021), although our sample size and trial numbers (N = 21; 
~96 trials per set-  size condition) provide high power to detect 
the presence of an overall lateralized ERP response, substan -
tially more participants and trials are needed to robustly detect 
set- size effects. Their simulations indicate that approximately 
390 clean trials per condition with 25 participants are needed 
to detect a difference in visual CDA amplitude between set-  size 
2 and set-  size 4 conditions. Thus, we interpret our findings as 
yielding no evidence for lateralized load effects, rather than pro-
viding evidence for the absence. Future studies with more power 
are needed to detect potential small but reliable CDA- like differ-
ences across set- size conditions in the auditory domain.
5   |   Conclusion
In conclusion, we observed two main findings in the current 
study. First, we found no evidence that auditory WM load is 
reflected in lateralized responses—neither in the time nor in 
the frequency domain. This implies that CDA-  like responses 
as observed for visual WM load are vision-  specific rather than 
domain- general markers of WM load. The lack of location- 
specific response further suggests that auditory WM is not 
inherently spatially organized, as is the case for visual WM. 
Second, using multivariate pattern analyses, we found that scalp 
15 of 18
Psychophysiology, 2025
patterns of alpha-  band power during the maintenance period 
reflect auditory WM load. Interestingly, patterns of alpha-  band 
power reflecting specific load conditions were changing dynam -
ically over the course of the maintenance period, revealing that 
(1) principles of dynamic neural population coding—which is 
known to underly the storage of WM content—may also be ex -
tended to executive WM processes, and (2) auditory WM may 
be inherently temporally organized, reflecting the repetition of 
information streams over time.
Author Contributions
Yichen Yuan: conceptualization, data curation, formal analysis, fund -
ing acquisition, methodology, software, resources, visualization, valida -
tion, writing – original draft, writing – review and editing. Surya Gayet: 
conceptualization, methodology, project administration, supervision, 
resources, writing – original draft, writing – review and editing. Derk 
Christiaan Wisman:  conceptualization, data curation, investigation, 
methodology, resources, software, writing – review and editing. Stefan 
van der Stigchel: conceptualization, methodology, supervision, project 
administration, resources, writing – review and editing. Nathan van der 
Stoep: conceptualization, methodology, project administration, supervi-
sion, resources, writing – original draft, writing – review and editing.
Funding
This work was supported by the China Scholarship Council (grant num-
ber 202206380011 to Yichen Yuan).
Ethics Statement
The study protocols were approved by the faculty ethics committee 
(FETC) of Utrecht University (number 18-  048 van der Stoep). All par -
ticipants signed informed consent for their participation.
Conflicts of Interest
The authors declare no conflicts of interest.
Data Availability Statement
All data, codes to run the experiments, analyze, and visualize the data 
are uploaded to the OSF platform ( https:// osf. io/ mw5ve/  ).
Endnotes
 1 A more strict criterium (eye movement correction plus ADJUST) 
did not change the lateralized ERPs and alpha power results (see 
Supporting Information  S1 for more details).
 2 The grand- average ERP responses in all eight conditions can be found 
in Supporting Information S1 .
 3 Unlike tasks where verbal labeling is possible, which can greatly in -
crease WM capacity, participants in the present study could not rely on 
such a strategy. This may have contributed to the observed relatively 
low capacity estimates.
References
Adam, K. C. S., E. K. Vogel, and E. Awh. 2020. “Multivariate Analysis 
Reveals a Generalizable Human Electrophysiological Signature of 
Working Memory Load.” Psychophysiology  57, no. 12: e13691. https://  
doi. org/ 10. 1111/ psyp. 13691 .
Ahissar, M., Y. Lubin, H. Putter- Katz, and K. Banai. 2006. “Dyslexia and 
the Failure to Form a Perceptual Anchor.” Nature Neuroscience 9, no. 12: 
1558–1564. https:// doi. org/ 10. 1038/ nn1800.
Alho, K., W. Teder, J. Lavikainen, and R. Näätänen. 1994. “Strongly 
Focused Attention and Auditory Event-  Related Potentials.” Biological 
Psychology  38, no. 1: 73–90. https://  doi. org/ 10. 1016/ 0301-  0511(94) 
90050  -  7.
Alunni- Menichini, K., S. Guimond, P. Bermudez, S. Nolden, C. Lefebvre, 
and P. Jolicoeur. 2014. “Saturation of Auditory Short-  Term Memory 
Causes a Plateau in the Sustained Anterior Negativity Event-  Related 
Potential.” Brain Research  1592: 55–64. https://  doi. org/ 10. 1016/j. brain 
res. 2014. 09. 047.
Arora, K., S. Gayet, J. L. Kenemans, S. Van der Stigchel, and S. Chota. 
2025. “Dissociating External and Internal Attentional Selection.” 
iScience 28, no. 4: 112282. https:// doi. org/ 10. 1016/j. isci. 2025. 112282.
Awh, E., and E. K. Vogel. 2025. “Working Memory Needs Pointers.” 
Trends in Cognitive Sciences 29, no. 3: 230–241. https:// doi. org/ 10. 1016/j. 
tics. 2024. 12. 006.
Baddeley, A. 2000. “The Episodic Buffer: A New Component of Working 
Memory?” Trends in Cognitive Sciences 4, no. 11: 417–423. https://  doi. 
org/ 10. 1016/ s1364 -  6613(00) 01538 -  2.
Baddeley, A. D., and G. J. Hitch. 1974. “Working Memory.” In Psychology 
of Learning and Motivation , edited by G. H. Bower, vol. 8, 47–89. 
Academic Press. https:// doi. org/ 10. 1016/ S0079 -  7421(08) 60452 -  1.
Bell, A. J., and T. J. Sejnowski. 1995. “An Information-  Maximization 
Approach to Blind Separation and Blind Deconvolution.” Neural 
Computation 7, no. 6: 1129–1159. https://  doi. org/ 10. 1162/ neco. 1995.7. 
6. 1129.
Berger, A., and M. Kiefer. 2021. “Comparison of Different Response 
Time Outlier Exclusion Methods: A Simulation Study.” Frontiers in 
Psychology  12: 675558. https:// doi. org/ 10. 3389/ fpsyg. 2021. 675558.
Bonnefond, M., and O. Jensen. 2012. “Alpha Oscillations Serve to Protect 
Working Memory Maintenance Against Anticipated Distracters.” 
Current Biology  22, no. 20: 1969–1974. https://  doi. org/ 10. 1016/j. cub. 
2012. 08. 029.
Carlisle, N. B., J. T. Arita, D. Pardo, and G. F. Woodman. 2011. 
“Attentional Templates in Visual Working Memory.” Journal of 
Neuroscience  31, no. 25: 9315–9322. https://  doi. org/ 10. 1523/ JNEUR 
OSCI. 1097-  11. 2011.
Carpenter, M., J. L. Cranford, M. R. Hymel, A. R. De Chicchis, and 
D. Holbert. 2002. “Electrophysiologic Signs of Attention Versus 
Distraction in a Binaural Listening Task.” Journal of Clinical 
Neurophysiology  19, no. 1: 55–60. https://  doi. org/ 10. 1097/ 00004 691-  
20020  1000-  00007 .
Chaumon, M., D. V. Bishop, and N. A. Busch. 2015. “A Practical Guide to 
the Selection of Independent Components of the Electroencephalogram 
for Artifact Correction.” Journal of Neuroscience Methods 250: 47–63. 
https:// doi. org/ 10. 1016/j. jneum eth. 2015. 02. 025.
Cowan, N. 1998. “Visual and Auditory Working Memory Capacity.” 
Trends in Cognitive Sciences 2, no. 3: 77. https://  doi. org/ 10. 1016/ s1364 
-  6613(98) 01144 -  9.
Cowan, N. 2010. “The Magical Mystery Four: How Is Working Memory 
Capacity Limited, and Why?” Current Directions in Psychological 
Science 19, no. 1: 51–57. https:// doi. org/ 10. 1177/ 09637 21409 359277.
Cowan, N., E. M. Elliott, J. Scott Saults, et al. 2005. “On the Capacity 
of Attention: Its Estimation and Its Role in Working Memory and 
Cognitive Aptitudes.” Cognitive Psychology  51, no. 1: 42–100. https:// doi. 
org/ 10. 1016/j. cogps ych. 2004. 12. 001.
De Moraes, C. G. 2013. “Anatomy of the Visual Pathways.” Journal of 
Glaucoma 22: S2–S7. https:// doi. org/ 10. 1097/ IJG. 0b013 e3182 934978.
Delorme, A., and S. Makeig. 2004. “EEGLAB: An Open Source Toolbox 
for Analysis of Single-  Trial EEG Dynamics Including Independent 
Component Analysis.” Journal of Neuroscience Methods 134, no. 1: 9–21. 
https:// doi. org/ 10. 1016/j. jneum eth. 2003. 10. 009.
16 of 18
 Psychophysiology, 2025
Deutsch, D. 1970. “Tones and Numbers: Specificity of Interference in 
Immediate Memory.” Science  168, no. 3939: 1604–1605. https://  doi. org/ 
10. 1126/ scien ce. 168. 3939. 1604.
Diamantopoulou, S., L. Poom, P. Klaver, and D. Talsma. 2011. “Visual 
Working Memory Capacity and Stimulus Categories: A Behavioral and 
Electrophysiological Investigation.” Experimental Brain Research  209, 
no. 4: 501–513. https:// doi. org/ 10. 1007/ s0022 1-  011-  2536-  z.
Faul, F., E. Erdfelder, A. Buchner, and A. G. Lang. 2009. “Statistical 
Power Analyses Using G*Power 3.1: Tests for Correlation and Regression 
Analyses.” Behavior Research Methods  41, no. 4: 1149–1160. https:// doi. 
org/ 10. 3758/ BRM. 41.4. 1149.
Fukuda, K., I. Mance, and E. K. Vogel. 2015. “α Power Modulation 
and Event- Related Slow Wave Provide Dissociable Correlates of Visual 
Working Memory.” Journal of Neuroscience 35, no. 41: 14009–14016. 
https:// doi. org/ 10. 1523/ JNEUR OSCI. 5003-  14. 2015.
Gaab, N., C. Gaser, T. Zaehle, L. Jancke, and G. Schlaug. 2003. 
“Functional Anatomy of Pitch Memory—An fMRI Study With Sparse 
Temporal Sampling.” NeuroImage  19, no. 4: 1417–1426. https://  doi. org/ 
10. 1016/ s1053 -  8119(03) 00224 -  6.
Gayet, S., C. L. E. Paffen, and S. Van der Stigchel. 2018. “Visual Working 
Memory Storage Recruits Sensory Processing Areas.” Trends in Cognitive 
Sciences 22, no. 3: 189–190. https:// doi. org/ 10. 1016/j. tics. 2017. 09. 011.
Grimault, S., S. Nolden, C. Lefebvre, et al. 2014. “Brain Activity Is Related 
to Individual Differences in the Number of Items Stored in Auditory Short- 
Term Memory for Pitch: Evidence From Magnetoencephalography.” 
NeuroImage 94: 96–106. https://  doi. org/ 10. 1016/j. neuro image. 2014. 
03. 020.
Hackney, C. M. 1987. “Anatomical Features of the Auditory Pathway 
From Cochlea to Cortex.” British Medical Bulletin 43, no. 4: 780–801. 
https:// doi. org/ 10. 1093/ oxfor djour nals. bmb. a072218.
Harrison, S. A., and F. Tong. 2009. “Decoding Reveals the Contents of 
Visual Working Memory in Early Visual Areas.” Nature  458, no. 7238: 
632–635. https:// doi. org/ 10. 1038/ natur e07832.
Hugdahl, K. 2011. “Fifty Years of Dichotic Listening Research -  Still 
Going and Going and….” Brain and Cognition 76, no. 2: 211–213. https://  
doi. org/ 10. 1016/j. bandc. 2011. 03. 006.
JASP Team. 2024. “JASP (Version 0.19.0)[Computer Software].”
Jensen, O., J. Gelfand, J. Kounios, and J. E. Lisman. 2002. “Oscillations 
in the Alpha Band (9–12 Hz) Increase With Memory Load During 
Retention in a Short-  Term Memory Task.” Cerebral Cortex  12, no. 8: 
877–882. https:// doi. org/ 10. 1093/ cercor/ 12.8. 877.
Jones, H. M., G. K. Diaz, W. X. Q. Ngiam, and E. Awh. 2024. 
“Electroencephalogram Decoding Reveals Distinct Processes for 
Directing Spatial Attention and Encoding Into Working Memory.” 
Psychological Science  35, no. 10: 1108–1138. https://  doi. org/ 10. 1177/ 
09567 97624 1263002.
Jones, H. M., W. S. Thyer, D. Suplica, and E. Awh. 2024. “Cortically 
Disparate Visual Features Evoke Content-  Independent Load Signals 
During Storage in Working Memory.” Journal of Neuroscience 44, 
no. 44: e0448242024. https://  doi. org/ 10. 1523/ JNEUR OSCI. 0448-  
24.  2024.
Kaiser, J. 2015. “Dynamics of Auditory Working Memory.” Frontiers in 
Psychology  6: 613. https:// doi. org/ 10. 3389/ fpsyg. 2015. 00613 .
Kaiser, J., T. Heidegger, M. Wibral, C. F. Altmann, and W. Lutzenberger. 
2007. “Alpha Synchronization During Auditory Spatial Short-  Term 
Memory.” Neuroreport 18, no. 11: 1129–1132. https://  doi. org/ 10. 1097/ 
WNR.  0b013 e3282 1c553b.
Kass, R. E., and A. E. Raftery. 1995. “Bayes Factors.” Journal of the 
American Statistical Association  90, no. 430: 773–795. https://  doi. org/ 
10. 1080/ 01621 459. 1995. 10476572.
Katus, T., M. M. Müller, and M. Eimer. 2015. “Sustained Maintenance 
of Somatotopic Information in Brain Regions Recruited by Tactile 
Working Memory.” Journal of Neuroscience 35, no. 4: 1390–1395. https:// 
doi. org/ 10. 1523/ JNEUR OSCI. 3535-  14. 2015.
Kikumoto, A., and U. Mayr. 2018. “Decoding Hierarchical Control 
of Sequential Behavior in Oscillatory EEG Activity.” eLife  7: e38550. 
https:// doi. org/ 10. 7554/ eLife. 38550 .
King, J. R., and S. Dehaene. 2014. “Characterizing the Dynamics 
of Mental Representations: The Temporal Generalization Method.” 
Trends in Cognitive Sciences 18, no. 4: 203–210. https:// doi. org/ 10. 1016/j. 
tics. 2014. 01. 002.
Klatt, L. I., S. Getzmann, E. Wascher, and D. Schneider. 2018a. 
“Searching for Auditory Targets in External Space and in Working 
Memory: Electrophysiological Mechanisms Underlying Perceptual and 
Retroactive Spatial Attention.” Behavioural Brain Research  353: 98–107. 
https:// doi. org/ 10. 1016/j. bbr. 2018. 06. 022.
Klatt, L. I., S. Getzmann, E. Wascher, and D. Schneider. 2018b. “The 
Contribution of Selective Spatial Attention to Sound Detection and 
Sound Localization: Evidence From Event-  Related Potentials and 
Lateralized Alpha Oscillations.” Biological Psychology  138: 133–145. 
https:// doi. org/ 10. 1016/j. biops ycho. 2018. 08. 019.
Klaver, P., D. Talsma, A. A. Wijers, H. J. Heinze, and G. Mulder. 1999. 
“An Event-  Related Brain Potential Correlate of Visual Short-  Term 
Memory.” Neuroreport 10, no. 10: 2001–2005. https://  doi. org/ 10. 1097/ 
00001 756-  19990 7130-  00002 .
Koelsch, S., K. Schulze, D. Sammler, T. Fritz, K. Müller, and O. Gruber. 
2009. “Functional Architecture of Verbal and Tonal Working Memory: 
An FMRI Study.” Human Brain Mapping 30, no. 3: 859–873. https://  doi. 
org/ 10. 1002/ hbm. 20550 .
Lefebvre, C., F. Vachon, S. Grimault, et  al. 2013. “Distinct 
Electrophysiological Indices of Maintenance in Auditory and Visual 
Short- Term Memory.” Neuropsychologia  51, no. 13: 2939–2952. https://  
doi. org/ 10. 1016/j. neuro psych ologia. 2013. 08. 003.
Leiberg, S., W. Lutzenberger, and J. Kaiser. 2006. “Effects of Memory 
Load on Cortical Oscillatory Activity During Auditory Pattern Working 
Memory.” Brain Research  1120, no. 1: 131–140. https:// doi. org/ 10. 1016/j. 
brain res. 2006. 08. 066.
Li, D., N. Cowan, and J. S. Saults. 2013. “Estimating Working Memory 
Capacity for Lists of Nonverbal Sounds.” Attention, Perception & 
Psychophysics  75, no. 1: 145–160. https://  doi. org/ 10. 3758/ s1341 
4-  012-  0383-  z.
Li, Q., and J. Saiki. 2015. “Different Effects of Color- Based and Location- 
Based Selection on Visual Working Memory.” Attention, Perception 
& Psychophysics  77, no. 2: 450–463. https://  doi. org/ 10. 3758/ s1341 
4-  014-  0775-  3.
Lipschutz, B., R. Kolinsky, P. Damhaut, D. Wikler, and S. Goldman. 
2002. “Attention- Dependent Changes of Activation and Connectivity in 
Dichotic Listening.” NeuroImage  17, no. 2: 643–656. https://  doi. org/ 10. 
1006/ nimg. 2002. 1184.
Luck, S. J., and E. K. Vogel. 1997. “The Capacity of Visual Working 
Memory for Features and Conjunctions.” Nature 390, no. 6657: 279–281. 
https:// doi. org/ 10. 1038/ 36846 .
Luo, H., F. T. Husain, B. Horwitz, and D. Poeppel. 2005. “Discrimination 
and Categorization of Speech and Non-  Speech Sounds in an MEG 
Delayed- Match- To- Sample Study.” NeuroImage 28, no. 1: 59–71. https:// 
doi. org/ 10. 1016/j. neuro image. 2005. 05. 040.
Luria, R., and E. K. Vogel. 2011. “Shape and Color Conjunction Stimuli 
Are Represented as Bound Objects in Visual Working Memory.” 
Neuropsychologia  49, no. 6: 1632–1639. https://  doi. org/ 10. 1016/j. neuro 
psych ologia. 2010. 11. 031.
17 of 18
Psychophysiology, 2025
Maris, E., and R. Oostenveld. 2007. “Nonparametric Statistical Testing 
of EEG-  and MEG-  Data.” Journal of Neuroscience Methods 164, no. 1: 
177–190. https:// doi. org/ 10. 1016/j. jneum eth. 2007. 03. 024.
Mathôt, S. 2017. “Bayes Like a Baws: Interpreting Bayesian Repeated 
Measures in JASP.” Cognitive Science and More 6: 66. https:/ /  www. 
cogsci. nl/ blog/ inter preti ng-  bayes ian-  repea ted-  measu res-  in-  jasp.
Meyer, M., D. Lamers, E. Kayhan, S. Hunnius, and R. Oostenveld. 2021. 
“Enhancing Reproducibility in Developmental EEG Research: BIDS, 
Cluster- Based Permutation Tests, and Effect Sizes.” Developmental 
Cognitive Neuroscience  52: 101036. https://  doi. org/ 10. 1016/j. dcn. 2021. 
101036.
Mohanathasan, C., J. Fels, and S. J. Schlittmeier. 2024. “Listening to 
Two- Talker Conversations in Quiet Settings: The Role of Listeners' 
Cognitive Processing Capabilities for Memory and Listening Effort.” 
Scientific Reports  14, no. 1: 22764. https://  doi. org/ 10. 1038/ s4159 8-  024-  
74085 -  1.
Ngiam, W. X. Q., K. C. S. Adam, C. Quirk, E. K. Vogel, and E. Awh. 
2021. “Estimating the Statistical Power to Detect Set-  Size Effects in 
Contralateral Delay Activity.” Psychophysiology  58, no. 5: e13791. 
https:// doi. org/ 10. 1111/ psyp. 13791 .
Oostenveld, R., P. Fries, E. Maris, and J. M. Schoffelen. 2011. 
“FieldTrip: Open Source Software for Advanced Analysis of MEG, 
EEG, and Invasive Electrophysiological Data.” Computational 
Intelligence and Neuroscience  2011: 156869. https://  doi. org/ 10. 1155/ 
2011/ 156869.
Peelen, M. V., and P. E. Downing. 2023. “Testing Cognitive Theories 
With Multivariate Pattern Analysis of Neuroimaging Data.” Nature 
Human Behaviour  7, no. 9: 1430–1441. https://  doi. org/ 10. 1038/ s4156 2-  
023-  01680 -  z.
Pickles, J. O. 2015. “Auditory Pathways: Anatomy and Physiology.” In 
Handbook of Clinical Neurology , vol. 129, 3–25. Elsevier. https:// doi. org/ 
10. 1016/ B978-  0-  444-  62630 -  1. 00001 -  9.
Pratt, H., H. J. Michalewski, G. Barrett, and A. Starr. 1989. “Brain 
Potentials in a Memory-  Scanning Task. I. Modality and Task Effects 
on Potentials to the Probes.” Electroencephalography and Clinical 
Neurophysiology  72, no. 5: 407–421. https://  doi. org/ 10. 1016/ 0013-  
4694(89) 90046 -  1.
Prosser, S. 1995. “Aspects of Short-  Term Auditory Memory as Revealed 
by a Recognition Task on Multi-  Tone Sequences.” Scandinavian 
Audiology  24, no. 4: 247–253. https://  doi. org/ 10. 3109/ 01050 39950 
9047544 .
Roach, B. J., and D. H. Mathalon. 2008. “Event-  Related EEG Time- 
Frequency Analysis: An Overview of Measures and an Analysis of Early 
Gamma Band Phase Locking in Schizophrenia.” Schizophrenia Bulletin  
34, no. 5: 907–926. https://  doi. org/ 10. 1093/ schbul/ sbn093.
Rodieck, R. W. 1979. “Visual Pathways.” Annual Review of Neuroscience 
2: 193–225. https:// doi. org/ 10. 1146/ annur ev. ne. 02. 030179. 001205.
Rouder, J. N., R. D. Morey, C. C. Morey, and N. Cowan. 2011. “How 
to Measure Working Memory Capacity in the Change Detection 
Paradigm.” Psychonomic Bulletin & Review 18, no. 2: 324–330. https://  
doi. org/ 10. 3758/ s1342 3-  011-  0055-  3.
Roux, F., and P. J. Uhlhaas. 2014. “Working Memory and Neural 
Oscillations: α-  γ Versus θ-  γ Codes for Distinct WM Information?” 
Trends in Cognitive Sciences 18, no. 1: 16–25. https://  doi. org/ 10. 1016/j. 
tics. 2013. 10. 010.
Schurgin, M. W. 2018. “Visual Memory, the Long and the Short of 
It: A Review of Visual Working Memory and Long-  Term Memory.” 
Attention, Perception & Psychophysics  80, no. 5: 1035–1056. https://  doi. 
org/ 10. 3758/ s1341 4-  018-  1522-  y.
Schwartz, I. R. 1992. “The Superior Olivary Complex and Lateral 
Lemniscal Nuclei.” In The Mammalian Auditory Pathway: 
Neuroanatomy, 117–167. Springer.
Scimeca, J. M., A. Kiyonaga, and M. D'Esposito. 2018. “Reaffirming 
the Sensory Recruitment Account of Working Memory.” Trends in 
Cognitive Sciences  22, no. 3: 190–192. https://  doi. org/ 10. 1016/j. tics. 
2017. 12. 007.
Silvanto, J., and D. Soto. 2012. “Causal Evidence for Subliminal Percept- 
To- Memory Interference in Early Visual Cortex.” NeuroImage  59, no. 1: 
840–845. https://  doi. org/ 10. 1016/j. neuro image. 2011. 07. 062.
Stokes, M. G. 2015. “'Activity-  Silent' Working Memory in Prefrontal 
Cortex: A Dynamic Coding Framework.” Trends in Cognitive Sciences 
19, no. 7: 394–405. https://  doi. org/ 10. 1016/j. tics. 2015. 05. 004.
Suplica, D., H. M. Jones, G. K. Diaz, J. P. Veillette, H. C. Nusbaum, and 
E. Awh. 2025. “Neural Evidence for Modality-  Independent Storage in 
Working Memory.” Current Biology  35, no. 19: 4620–4630.e4. https://  
doi. org/ 10. 1016/j. cub. 2025. 08. 007.
Talsma, D., A. A. Wijers, P. Klaver, and G. Mulder. 2001. “Working 
Memory Processes Show Different Degrees of Lateralization: Evidence 
From Event-  Related Potentials.” Psychophysiology  38, no. 3: 425–439. 
https:// doi. org/ 10. 1111/ 1469-  8986. 3830425.
Thyer, W., K. C. S. Adam, G. K. Diaz, I. N. Velázquez Sánchez, E. K. 
Vogel, and E. Awh. 2022. “Storage in Visual Working Memory Recruits 
a Content-  Independent Pointer System.” Psychological Science  33, no. 
10: 1680–1694. https:// doi. org/ 10. 1177/ 09567 97622 1090923.
Treder, M. S. 2020. “MVPA-  Light: A Classification and Regression 
Toolbox for Multi- Dimensional Data.” Frontiers in Neuroscience  14: 289. 
https:// doi. org/ 10. 3389/ fnins. 2020. 00289 .
Tuladhar, A. M., N. ter Huurne, J. M. Schoffelen, E. Maris, R. Oostenveld, 
and O. Jensen. 2007. “Parieto- Occipital Sources Account for the Increase 
in Alpha Activity With Working Memory Load.” Human Brain Mapping 
28, no. 8: 785–792. https://  doi. org/ 10. 1002/ hbm. 20306 .
van Dijk, H., I. L. Nieuwenhuis, and O. Jensen. 2010. “Left Temporal 
Alpha Band Activity Increases During Working Memory Retention of 
Pitches.” European Journal of Neuroscience  31, no. 9: 1701–1707. https:// 
doi. org/ 10. 1111/j. 1460-  9568. 2010. 07227. x.
van Ede, F. 2018. “Mnemonic and Attentional Roles for States of 
Attenuated Alpha Oscillations in Perceptual Working Memory: A 
Review.” European Journal of Neuroscience  48, no. 7: 2509–2515. https:// 
doi. org/ 10. 1111/ ejn. 13759 .
van Ede, F., S. R. Chekroud, and A. C. Nobre. 2019. “Human Gaze Tracks 
Attentional Focusing in Memorized Visual Space.” Nature Human 
Behaviour 3, no. 5: 462–470. https:// doi. org/ 10. 1038/ s4156 2-  019-  0549-  y.
Vogel, E. K., and M. G. Machizawa. 2004. “Neural Activity Predicts 
Individual Differences in Visual Working Memory Capacity.” Nature  
428, no. 6984: 748–751. https:// doi. org/ 10. 1038/ natur e02447.
Wianda, E., and B. Ross. 2019. “The Roles of Alpha Oscillation in 
Working Memory Retention.” Brain and Behavior 9, no. 4: e01263. 
https:// doi. org/ 10. 1002/ brb3. 1263.
Williamson, V. J., A. D. Baddeley, and G. J. Hitch. 2010. “Musicians' and 
Nonmusicians' Short- Term Memory for Verbal and Musical Sequences: 
Comparing Phonological Similarity and Pitch Proximity.” Memory & 
Cognition 38, no. 2: 163–175. https:// doi. org/ 10. 3758/ MC. 38.2. 163.
Wilsch, A., and J. Obleser. 2016. “What Works in Auditory Working 
Memory? A Neural Oscillations Perspective.” Brain Research  1640: 
193–207. https:// doi. org/ 10. 1016/j. brain res. 2015. 10. 054.
Woldorff, M. G., C. Tempelmann, J. Fell, et  al. 1999. “Lateralized 
Auditory Spatial Perception and the Contralaterality of Cortical 
Processing as Studied With Functional Magnetic Resonance Imaging 
and Magnetoencephalography.” Human Brain Mapping 7, no. 1: 49–66. 
https:// doi. org/ 10. 1002/ (SICI) 1097-  0193(1999)7: 1< 49:: AID-  HBM5> 3.0. 
CO; 2-  J.
Yu, X., and E. Lau. 2024. “Same Set of Visual Pointers for Biological and 
Non- Biological Objects in Working Memory.” Visual Cognition 32, no. 8: 
687–700. https:// doi. org/ 10. 1080/ 13506 285. 2025. 2487860.
18 of 18
 Psychophysiology, 2025
Yu, X., and E. Lau. 2025. “A Finite Set of Content-  Free Pointers in 
Visual Working Memory: Magnetoencephalography (MEG) Evidence.” 
Neuroreport 36, no. 3: 153–160. https:/ /  doi. org/ 10. 1097/ WNR. 00000 
00000 002132.
Supporting Information
Additional supporting information can be found online in the 
Supporting Information section. Figure S1: An example of one partici -
pants' frontal channel data before and after ICA and eye- movement cor-
rection, both at the single-  trial level (a) and across the entire recording 
(b). Figure S2: Lateralized (contralateral minus ipsilateral) responses, 
and their topographical distributions. (a) Left: Grand-  average lateral -
ized responses in the time-  domain data averaged across all set-  size con-
ditions and all electrodes, shown from baseline ( −0.2 ms) until the end 
of retention (3.4 s). The shaded areas depict the standard error of the 
mean. The vertical dashed lines indicate (from left to right) the onset of 
the tone sequence, the onset of the maintenance period, and the end of 
the maintenance period. The horizontal purple line indicates a signifi -
cant lateralized effect (deviating from 0) when collapsing across all four 
set- size conditions. Right: the topographical maps depict the magnitude 
of the overall lateralized effect ( t- value) averaged across four set-  size 
conditions during the time window with significant lateralized effects. 
Electrodes where these effects are significant are marked with an * (if 
any). (b) Left: lateralized responses in the time-  domain data measured 
in the Set-  size 1 (red), 2 (blue), 3 (green), and 4 (black) conditions, av -
eraged across all electrodes. Right: The topographical maps depict the 
magnitude of the set-  size effect ( F- value) averaged across four set-  size 
conditions during the time window with significant lateralized effects. 
Panel (c) and (d) depict the same as Panel (a, b), but for lateralized alpha- 
band power. Figure S3:  The grand average ERPs across participants 
for all 8 conditions (2 attend-  side * 4 set- size) from −1 s until the end of 
retention (3.6 s), separated into frontal (Fp1, Fp2, AF3, AF4, F7, F3, Fz, 
F4, F8, FC5, FC1, FC2, FC6) and posterior (CP5, CP1, CP2, CP6, P7, 
P3, Pz, P4, P8, PO3, PO4, O1, Oz, O2) electrode clusters. The vertical 
dashed lines indicate (from left to right) the onset of the tone sequence, 
the onset of the maintenance period, and the end of the maintenance 
period. Figure S4: Non- lateralized responses, and their topographical 
distributions (averaged across the delay), separately for the set-  size 1, 
2, 3, and 4 conditions. Left: Non- lateralized responses in the time do -
main data measured in the set-  size 1 (red), 2 (blue), 3 (green), and 4 
(black) conditions. The vertical dashed lines indicate (from left to right) 
the onset of the tone sequence, the onset of the maintenance period, 
and the end of the maintenance period. Right: The four topographical 
maps depict the magnitude of the non- lateralized responses in set-  size 
1, 2, 3, and 4 conditions during the maintenance period. Figure S5: 
Timepoint- by- timepoint decoding of scalp voltage patterns. All panels 
depict decoding accuracy ( y- axis) as a function of time ( x- axis). The big 
panel depicts decoding accuracy averaged across all six pairwise com -
parisons (i.e., main effect of set-  size), which are shown individually in 
the surrounding smaller panels. Bold blue lines indicate significant 
above chance (50%) decoding, based on cluster-  based permutation tests 
to account for multiple comparisons. The vertical dashed-  purple lines 
split time into the encoding and maintenance periods. In the small pan -
els, the blue squares indicate the target tones, while the blurred squares 
represent the white noise. 
