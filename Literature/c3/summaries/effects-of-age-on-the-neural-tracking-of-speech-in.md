# effects-of-age-on-the-neural-tracking-of-speech-in

Academic Editor: Gavin M Bidelman
Received: 11 July 2025
Revised: 12 August 2025
Accepted: 14 August 2025
Published: 16 August 2025
Citation: An, H.; Lee, J.; Park, Y.-j.;
Suh, M.-W.; Lim, Y. Effects of Age on
the Neural Tracking of Speech in Noise.
Brain Sci. 2025, 15, 874. https://
doi.org/10.3390/brainsci15080874
Copyright: © 2025 by the authors.
Licensee MDPI, Basel, Switzerland.
This article is an open access article
distributed under the terms and
conditions of the Creative Commons
Attribution (CC BY) license
(https://creativecommons.org/
licenses/by/4.0/).
Article
Effects of Age on the Neural Tracking of Speech in Noise
HyunJung An 1,2 , JeeWon Lee 1,3 , Young-jin Park 4
 , Myung-Whan Suh 5 and Yoonseob Lim 1,6, *
1 Center for Intelligent & Interactive Robotics, Korea Institute of Science and Technology, 5, Hwarang-ro 14-gil,
Seongbuk-gu, Seoul 02792, Republic of Korea; hyunjung.an@hallym.ac.kr (H.A.)
2 Division of Speech Pathology and Audiology, Hallym University, Chuncheon 24252, Republic of Korea
3 Department of Electronic and Electrical Engineering, Ewha Womans University,
Seoul 03760, Republic of Korea
4 Electro-Medicine Device Research, KERI, An-San city 15588, Republic of Korea
5 Department of Otorhinolaryngology Head and Neck Surgery, Seoul National University Hospital,
Seoul 03080, Republic of Korea
6 Department of HY-KIST Bio-Convergence, Hanyang University, Seoul 04763, Republic of Korea
* Correspondence: yslim@kist.re.kr
Abstract
Background: Older adults often struggle to comprehend speech in noisy environments, a
challenge influenced by declines in both auditory processing and cognitive functions. This
study aimed to investigate how differences in speech-in-noise perception among individ-
ual with clinically normal hearing thresholds (ranging from normal to mild hearing loss
in older adults) are related to neural speech tracking and cognitive function, particularly
working memory. Method: Specifically, we examined delta (1–4 Hz) and theta (4–8 Hz) EEG
oscillations during speech recognition tasks to determine their association with cognitive
performance in older adults. EEG data were collected from 23 young adults (20–35 years)
and 23 older adults (65–80 years). Cognitive assessments were administered to older adults,
and both groups completed an EEG task involving speech recognition in Speech-Shaped
Noise (SSN) at individualized noise levels based on their Sentence Recognition Scores (SRS).
Results: The results showed that age significantly impacted hit rates and reaction times in
noisy speech recognition tasks. Theta-band neural tracking was notably stronger in older
adults, while delta-band tracking showed no age-related difference. Pearson’s correlations
indicated significant associations between age-related cognitive decline, reduced hear-
ing sensitivity, and Mini-Mental State Examination (MMSE) scores. Regression analyses
showed that theta-band neural tracking at specific SRS levels significantly predicted word
list recognition in the higher SRT group, while constructional recall was strongly predicted
in the lower SRT group. Conclusions: These findings suggest that older adults may rely
on theta-band neural tracking as a compensatory mechanism. However, regression results
alone were not sufficient to fully explain how working memory affects neural tracking,
and additional cognitive and linguistic factors should be considered in future studies.
Furthermore, cognitive assessments were administered only to older adults, which limits
the ability to determine whether group differences are driven by age, hearing, or cognitive
status—a major limitation that should be addressed in future research.
Keywords: neural tracking; theta oscillation; age effect; speech perception in noise;
Electroencephalography (EEG); neural decoding
Brain Sci. 2025, 15, 874 https://doi.org/10.3390/brainsci15080874
Brain Sci. 2025, 15, 874 2 of 22
1. Introduction
Older listeners often experience increased difficulty understanding speech in noisy
environments. Advancing age coincides with an observable decline in both peripheral
and central auditory processing, which has the potential to affect speech recognition.
Previous studies investigating the effect of aging on speech recognition abilities have
consistently identified peripheral hearing loss and central auditory processing abilities as
major influencing factors, in both quiet and noisy environments [1,2]. Age-related damage
to the cochlea leads to higher hearing thresholds in the high-frequency range, which is
assumed to contribute to difficulties in understanding speech in noise [3]. Decreased speech
perception in noise without deficit in peripheral system may be due to a decline in central
auditory processing. Central auditory system with reduced gray matter volume in the
fronto-temporal cortex [4,5] and diminished white matter microstructure lead to central
presbycusis [6]. Central presbycusis is often indicated by deteriorated auditory object
perception and a decline in higher-level auditory processing, including difficulties with
speech perception in noisy environments [3,5,7].
Recent studies have attempted to identify the factors contributing to the difficulties of
speech perception in noise through neural envelope tracking. Neural envelope tracking
was found to be enhanced when focusing on target speech in noise, and this tendency was
particularly pronounced in older adults compared to younger adults [8–12]. Such enhanced
envelope tracking observed in older adults may be due to central compensatory gain
mechanisms. These mechanisms increase cortical activity in the brain region to compensate
for declined peripheral input. However, it is unclear whether the differences in envelope
tracking due to age are a result of basic acoustic processing or attributable to more complex,
higher-order factors.
Older adults often face specific perceptual challenges, such as differentiating speech
from background noise and recognizing individual words within the stream of acoustic
information. They particularly struggle with word recognition when words have many
phonetically similar neighbors [13]. A possible explanation for these perceptual challenges
is that older adults may employ distinct strategies and neural structures to maintain
functional speech processing [ 14]. Studies by Giraud and Poeppel [ 15] demonstrated
that brain oscillations (specifically delta, theta, and gamma) play a crucial role in speech
processing by breaking down continuous speech into discrete units at different timescales
that match the natural rhythms of speech (phonemes, syllables, and phrases). Specifically,
delta oscillations (1 to 4 Hz) are posited to play an essential role in the segmentation of
verbal input into discrete units such as words and phrases, facilitating the integration
of lexical units for complex language processing [ 16,17]. Theta oscillations (4 to 8 Hz)
facilitated the decoding of acoustic elements (e.g., syllable onset or syllable rate) in speech.
Etard and Reichenbach [9] employed native and non-native speech in various levels of
background noise to distinguish between the influence of acoustic attributes and language
comprehension. Their findings revealed a primary association of theta-band activity with
speech acoustics and delta-band entrainment with comprehension. Moreover, Keshavarzi,
Kegler [18] revealed that modulating theta-band activity through transcranial alternating
current stimulation can influence language comprehension, highlighting the important role
of theta frequencies in speech processing. These results align with the notion that the delta
band is synchronizing with more complex linguistic elements (words or phrases and other
abstract linguistic structures), while theta band oscillations are involved in fundamental
acoustic patterns (onset of syllables or syllable rate) [19,20]. Although many recent studies
have focused on speech processing mechanisms, only a few studies investigated age-related
differences in speech envelope tracking in older adults during speech comprehension [21].
Brain Sci. 2025, 15, 874 3 of 22
Difficulties in perceiving speech in noise among older adults could be related to
lower-level sensory and perceptual changes as well as higher-level cognitive abilities
such as working memory span, processing speed, and selective attention [ 22,23]. It has
been demonstrated that there are connections between cognitive abilities and temporal
processing deficits observed during challenging listening tasks [24,25]. Moreover, previous
studies have shown that the central regions involved in auditory and language processing
are critical for speech recognition in noise [ 26,27]. These findings indicate that central
nervous system, which involves cognitive processes, is important for speech recognition
in noise.
Among various cognitive processes, working memory is an essential cognitive function
for understanding speech in noisy environments [28]. To perceive speech in noise, a listener
rapidly processes incoming auditory information, focuses on the speech, and disregards
irrelevant background noise. At the same time, the listener must extract and retain relevant
auditory information for integration with subsequent input and later recall. Therefore, it is
reasonable to conclude that both working memory and attentional resources are crucial for
speech recognition in noise. Specifically, the ability to focus on relevant information while
ignoring distractions (selective attention), manage multiple streams of information at once
(divided attention), and temporarily store and integrate selected information in working
memory are all crucial for perceiving and recognizing speech [ 28,29]. Several studies
have suggested that age-related declines in working memory and speech recognition in
noisy environments are significant only for older adults, not younger adults [30–32]. For
younger adults with normal hearing, working memory capacity does not significantly
predict speech recognition in noise, whereas for older adults, it does. These suggested
that working memory and attentional declines in aging may impair speech recognition in
noise, underscoring the need to explore these cognitive contributions in depth. Therefore,
this study aims to examine how age-related changes in working memory impact speech
recognition in noise, addressing a key gap in understanding how these cognitive factors
contribute to older adults’ speech processing difficulties in complex auditory environments.
When older adults try to perceive speech in challenging listening environments, they
have to rely more on cognitive systems than younger adults. The increased demand on
cognitive resources is referred to as listening effort [33,34]. Various subjective and objective
methods have been employed to assess listening effort [35]. Subjective measures, including
tools such as questionnaires and response times [36–38], have shown that response times
increase under severe noise conditions and that the older group requires more listening
effort than the younger group, even in similar listening environments. Conversely, objective
assessments of listening effort include techniques like electroencephalography (EEG),
neuroimaging, and pupillometry [39–41]. Previous studies showed that while young adults
exhibit noticeable increases in pupil dilation during sentence processing correlated with
the signal-to-noise ratio (SNR), older adults are less responsive to SNR changes, possibly
because they are already utilizing additional cognitive resources for speech understanding
in noise [41]. Other studies showed that diminished spectral and temporal resolution in
discrimination are known to contribute to the increased demand on cognitive resources
during speech understanding in noise [42–44]. Specifically, changes in the amplitude of
neural oscillations during speech presentation and memory retention periods measured
by EEG have been shown to correlate with variations in listening effort, with an increase
in theta band (4–7 Hz) power localized to frontal midline regions reflecting subjective
listening effort in speech in noise tasks [ 45]. Given these findings, this study aims to
investigate how listening effort and working memory demands are reflected in neural
tracking during speech processing in noise. By focusing on neural tracking in theta band,
this study addresses understanding how listening effort and working memory support
Brain Sci. 2025, 15, 874 4 of 22
speech recognition in challenging listening environments, particularly for older adults. We
expect to find that age-related increases in listening effort will correspond with specific
patterns in neural oscillations, indicating a greater reliance on cognitive resources for
effective speech processing.
This study investigates the neural factors and listening effort underlying differences
in speech recognition in noise, with a particular focus on older adults with normal hearing.
We first analyzed the role of different cortical oscillation bands, particularly delta and
theta, in the neural tracking of speech in noise across various age groups. Additionally, we
examined the relationship between cognitive functions—especially working memory—and
neural tracking in noise among older adults with different levels of hearing ability. While
previous studies have consistently emphasized the impact of peripheral hearing loss and
central auditory processing on speech recognition, especially in noisy environments, they
have not directly clarified how these age-related auditory declines connect to cognitive
function and speech-in-noise perception. To address this, participants were grouped based
on their speech reception threshold (SRT) rather than hearing thresholds, which allowed
us to focus on listening effort while also investigating the correlation between cognitive
function and speech envelope tracking in noise within each group.
2. Materials and Methods
2.1. Participants
Twenty-three younger adults (fifteen males and eight females; ages 20–33 years, mean
age = 26, standard deviation = 3.3), all right-handed except one, participated in the study.
All reported normal hearing, no history of neurological or psychiatric disorders, and no cur-
rent use of medications that affect central nervous system function. Participants provided
written informed consent prior to enrollment. Inclusion criteria for the younger group
were: age between 20 and 35 years, normal hearing as self-reported, right-handedness,
and no history of cognitive or neurological disorders. Exclusion criteria included hearing
loss, diagnosed learning disabilities (e.g., dyslexia), history of concussion, or the use of
psychoactive medications (e.g., for insomnia or anxiety). These criteria were verbally
confirmed with all participants prior to the start of the experiment.
Twenty three older adults (four males and nineteen females; ages 65 to 80 years, mean
age = 72, standard deviation = 3.3) demonstrate that hearing loss was most apparent in
the high frequencies and varied from normal to mild hearing loss (HL). To assess the
individuals’ hearing ability, we calculated the PTA across the frequency 0.5, 1, 2 and 4 kHz,
which ranged from 20 dB hearing level (normal hearing) to 20–40 dB hearing level (mild
hearing loss). Speech perception was assessed using the Korean Standard Phonetically
Balanced Monosyllabic Word List (KS-MWL), which is widely used in Korean clinical
practice for word recognition testing. Unlike English SRT tests that use spondaic (bisyllabic)
words, Korean audiology uses separate bisyllabic lists for SRT and monosyllabic lists like
the KS-MWL for speech recognition. Our study followed Korean clinical standards by
using the KS-MWL for speech perception assessment [46]. This score represents the dB HL
level at which the patient accurately recognizes 50% of the presented words. Older adults
were recruited through a screening at Seoul National University Hospital. Inclusion criteria
included age between 65 and 80 years, no diagnosis of dementia or cognitive impairment
(as determined via screening), and no history of major neurological or learning disorders.
Exclusion criteria included significant hearing loss (greater than 40 dB HL), diagnosed
cognitive impairment, history of traumatic brain injury, or use of medications known to
affect EEG measures [47,48].
All the procedures in this study followed the ethical standards of the Declaration of
Helsinki and were approved by the Institutional Review Board (IRB) of the Seoul National
Brain Sci. 2025, 15, 874 5 of 22
University Hospital (IRB codes: 2009-090-1157 and H-2112-075-1282, respectively). The
study was conducted by a researcher who majored in clinical psychology and was included
as a certified examiner in the approved IRB protocol.
2.2. Cognitive T esting
The recruited young adults were university students. Given their clear understanding
of the oral explanation of the experiment and their ability to follow the procedures without
any issues, it was determined that their cognitive levels were within the normal range.
Therefore, the cognitive assessment protocols were applied to only older participants to
evaluate their cognitive function: Korean Version of Consortium to Establish a Registry for
Alzheimer’s Disease Neuropsychological Assessment (CERAD-K) [49]. The CERAD-K was
administered by trained clinical laboratory technologists under the supervision of a licensed
psychiatrist, who also conducted clinical evaluations. All technologists received prior
instruction on standardized administration procedures from clinical neuropsychologists to
ensure consistency and reliability. The battery comprises nine tests, administered in the
standardized order as recommended by the CERAD-K protocol. For this study, participants
were invited to visit the laboratory on two separate occasions. During the first visit, they
completed the full cognitive assessment battery. Only those who were confirmed to have
normal cognitive function based on this assessment were invited back for a second visit to
undergo EEG experiment.
(1) The Korean version of Mini-Mental Status Examination (MMSE-K): The MMSE [50]
is a widely used cognitive screening tool that assesses functions such as orientation,
language, attention, visuospatial skills, and memory. In the Korean version, MMSE-
KC, the reading and writing tasks were replaced by two judgment-based items to
accommodate the significant number of illiterate individuals in Korea. The test has a
maximum score of 30.
(2) The Korean version of the Short Blessed Test (SBT-K): The SBT-K consists of 6 items
that evaluate orientation, delayed memory, and concentration. It has been designed to
suit the characteristics of the Korean language. This test includes questions about the
current year, month, and time; counting backward from 20 to 1; saying the months
of the year in reverse order; and delayed recall of an address and a person’s name.
Scores are based on the number of errors in each item, with more errors resulting in a
higher score. The maximum score is 28.
(3) Word list memory: This free-recall memory test evaluates the ability to learn new
verbal information. It involves three trials, each presenting a list of 10 words in a
different order. The participant reads each word aloud as it appears. After each trial,
the participant has 90 s to recall as many words as possible. The Korean version of the
Word List Memory task was designed considering Korean language characteristics, in-
cluding phonemic similarity, semantics, and word length equivalence. The maximum
score across the three trials is 30.
(4) Word list recall: This test assesses the ability to remember words. Participants have
up to 90 s to recall the 10 words previously given in the word list memory task. The
maximum score for this test is 10. The values presented in the table are converted to
percentages based on this maximum score.
(5) Word list recognition: This test measures the ability to recognize target words from
the word list memory task including 10 distractor words. To minimize the chance of
guessing correctly, the final score is calculated by adding the total correct answers for
both the target and distractor words, then subtracting 10. If the result is less than zero,
the score is set to zero. The test has a maximum score of 10.
Brain Sci. 2025, 15, 874 6 of 22
(6) Korean version of the Boston Naming Test (K-BNT): This test assesses visual naming
capability by showing 15-line drawings of familiar objects. The drawings are orga-
nized into three sets of five, each representing objects with high, medium, or low
frequency in the Korean language. The maximum score is 15.
(7) Word fluency: This test evaluates verbal production, semantic memory, and language
skills. Participants are asked to list as many animals as they can within one minute.
(8) Constructional praxis: This task evaluates visuospatial and constructional skills.
Participants are asked to copy four-line drawings of increasing complexity: a circle,
a diamond, intersecting rectangles, and a cube. Each figure must be copied within
2 min. The maximum score for accurately drawing all four figures is 11.
(9) Constructional recall: This task evaluates the ability to visuospatial recall, after a brief
delay, the four line drawings from the Constructional praxis task. The maximum score
for correctly drawing all four figures is 11.
Table 1 presents the demographic characteristics (i.e., age and year of education) and
the results of each subtest of the CERAD-K and hearing test.
Table 1. Clinical characteristics of old adults.
Older Adult
Age (years) 72.2 ± 4.6
Educational duration (years) 11.6 ± 4
CERAD-K
MMSE-KC 26.2 ± 1.8
Short Blessed Test 1.7 ± 1.5
Word list memory 17.7 ± 3
Word list recall 71.9 ± 21.1
Word list recognition 8.5 ± 1.2
Boston naming test 11.6 ± 1.6
Word fluency 18.4 ± 3.5
Constructional praxis 10.6 ± 0.8
Constructional recall 6.4 ± 2.7
Trail making test A 54.0 ± 24.7
Trail making test B 139.5 ± 51.9
Hearing tests
PTA right ear (dB HL) 20.4 ± 6
PTA left ear (dB HL) 19.1 ± 7.5
SRT right ear (dB HL) 15.8 ± 7.2
SRT left ear (dB HL) 14.1 ± 6.7
Pure Tone Average (PTA); Speech Recognition Score (SRT); Mini-Mental Status Examination (MMSE); Korean
V ersion of Consortium to Establish a Registry for Alzheimer’s Disease Neuropsychological Assessment (CERAD-K).
However, the lack of direct cognitive and audiometric evaluation in the younger
control group is a key limitation of the present study, as it prevents clear interpretation of
whether group differences stem from age, hearing, or cognitive status. This limitation is
acknowledged here as well as in the limitation section.
2.3. EEG Experimental Design and Procedure
2.3.1. Stimuli and Experiment Procedure
Stimuli—In this experiment, the Korean version of the Flemish Matrix Sentence Test
was used as the behavioral measure for evaluating the speech recognition of participants, as
referenced in a prior study [51]. The matrix sentences, consisting of five words representing
distinct word categories (name, adjective, object, numeral, and verb), were utilized. To
ensure comparable behavioral speech intelligibility scores, 10 alternatives were randomly
chosen for each word category, forming a set of sentences with similar characteristics. These
Brain Sci. 2025, 15, 874 7 of 22
matrix sentences were intentionally crafted to natural sound while featuring grammatically
simple and semantically unexpected content. This design aimed to minimize the influence
of complex language comprehension on the observed results. Additionally, sentences
were equated for Root Mean Square (RMS) amplitude at 65 dB Sound Pressure Level
(SPL). To explore the speech understanding in noise on neural tracking, matrix sentences
were presented under a background noise condition. Speech Shaped Noise (SSN) was
employed, representing noise with a spectrum similar to that of the matrix sentences. This
allowed for an investigation into how neural tracking is affected by speech understanding
in background noise.
Experiment Procedure—Before initiating the EEG recording, a speech recognition test
was administered to determine the speech understanding level necessary for each indi-
vidual to accurately recognize speech with the provided speech material (Flemish matrix
sentence test). Participants were instructed to repeat each sentence during the test verbally.
The adaptive procedure relied on the number of words correctly repeated in each sentence,
ranging from zero to five. To determine the noise level, Signal-to-Noise Ratios (SNRs) were
established based on participants’ repeated responses. If the participant correctly repeated
fewer than 2 words out of the five presented, the noise level was decreased by 3 or 4 dB.
However, if they responded correctly with more than 2 words, the noise level was increased
by 1 or 2 dB. Through these procedures, we determined the individual SNR required to
achieve 25%, 50%, 75%, 95% correct speech recognition scores (SRS). Each participant had
an individual SNR level established based on their respective SRS levels.
During the EEG recoding, the participants listened to a 12 min children’s story titled
“Kongjui and Patjui,” narrated by a female Korean speaker. The story was segmented
into 1 min fragments by considering sentence boundaries, thus establishing an optimal
condition for constructing a linear decoder, as elaborated in the previous study [51]. Fol-
lowing this, the Flemish Matrix sentence test was administered. The participants were
instructed to repeat sentences presented under Speech Shaped Noise (SSN) conditions.
Across four SRS blocks (SRS 25%, SRS 50%, SRS 75%, and SRS 95%), 10 sentence stimuli
were utilized for each SRS block, resulting in a total of 40 sentences. The sentences were
presented in random order within each block (Figure 1). To avoid potential order effects,
blocks for different sentences were executed in a pseudo-random order. The hit rate was
scored as correct if the verbal response was an exact match to the target word. For example,
if the target word was “broom”, responses such as “brum” or “broon” were scored as
incorrect. The response time was measured from the moment the participants pressed the
ENTER key after hearing the sentence, extending to the initiation of their verbal repetition
of the sentence heard. The participants were not informed that the response times would
be measured to prevent encouraging speed-speech, which could compromise response
accuracy and induce speed-accuracy trade-offs [52].
Brain Sci. 2025, 15, 874 8 of 22
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Figure 1. Overview of the main procedures conducted during the behavioral and EEG experiment. In
the behavioral experiment, the participants were directed to repeat each sentence heard verbally. The
noise level was adjusted based on the number of words correctly repeated in each sentence, which
varied from zero to five. For the EEG study, noise levels were selected to match specific target speech
recognition levels (SRS: 25%, 50%, 75%, and 95%). The EEG experiment procedure was structured into
two sessions. In the first session, a decoder model for speech recognition was developed using the
narrative “Kongjui and Patjui” without noise. In the second session, SSN was presented at varying
levels of SRS (25%, 50%, 75%, and 95%), as determined by the behavioral test. For each level of noise,
the participants were presented with 10 sentence stimuli within four blocks of noise conditions. They
were required to attend to each sentence under noise conditions and repeat what they heard within a
limited time (8 s).
2.3.2. Acquisition and Pre-Processing of EEG Data
The EEG experiment was conducted in an electromagnetic-shielded, double-wall,
soundproof chamber that meets the ambient noise level requirements of the American
National Standards Institute (ANSI) S3.1-1999. EEG data were collected using a 64-electrode
Neuroscan SynAmps RT system (64-channel Quik-Cap from Compumedics, Victoria, Aus-
tralia) at a sampling rate of 1000 Hz and raw signals were re-referenced through a common
average reference method, excluding vertical and horizontal electrooculograms.
The preprocessing of all data analysis was conducted using EEGLAB and the mTRF
toolbox [53] in MATLAB (v9.5.0 R2018b, The MathWorks, Inc., Natick, MA, USA). The
preprocessing procedure involved applying bandpass filtering to the original recordings
using a zero-phase Hamming windowed sinc FIR filter in the delta range (1–4 Hz) and
theta range (4–8 Hz). After filtering, both the EEG and speech envelope data were down-
sampled to a sampling rate of 64 Hz to maintain uniform sample lengths across datasets.
Additionally, z-scoring was employed to normalize the data.
We analyzed the decoding by distinguishing the neural activity in the cerebral cortex
to understand the mechanism of speech in noise conditions.
2.4. Data Analyses
Decoder model—To examine how speech perception processes and neural representa-
tions of speech are affected under noisy conditions, we employed a stimulus reconstruction
method as described by Vanthornhout, Decruy [12]. In this method, a speech envelope is
Brain Sci. 2025, 15, 874 9 of 22
reconstructed from EEG signals recorded while participants listen to speech stimuli. The
degree of similarity between the original and reconstructed speech envelopes indicates
the accuracy of the cortical representation of actual speech and can vary depending on
the listener’s level of attention [12,54,55]. Based on this method, we calculated the linear
decoder for the EEG signals to generate a reconstructed envelope of the stimulus, denoted
as ˆS(t). The mathematical representation of this reconstruction is as follows:
ˆS(t) = ∑
k
∑
τ
w(τ, k)R(t − τ, k)
w =

RR T + λI
−1
RST
ˆS(.) denotes the reconstructed envelope, wheret corresponds to the time range,k refers
to the index of the recording electrodes, τ represents the time lag between the stimulus
and the neural response, and R(.) indicates the neural response. To determine if a linear
relationship between the EEG data and the envelope of speech stimuli, ridge regression
was applied using w(.) as weights of decoder. The correlation analysis was performed
following the approach outlined in the previous study [12]. Specifically, we constructed
the model using a leave-one-out cross-validation scheme based on clean speech data.
In this framework, envelope correlations in the clean speech condition typically reach
values around 0.1, indicating reliable neural tracking. In the present study, we obtained
comparable correlation values, with young adults showing 0.119 ± 0.051 and older adults
showing 0.158 ± 0.084. These values are consistent with those reported in the previous
study, supporting the validity and quality of the EEG data used in our analysis [56].
A subject-specific decoder was first calculated using EEG recordings obtained while
participants listened to the “Kongjui and Patjui” story, a continuous narrative stimulus
selected to elicit rich neural entrainment through natural prosodic variation and sustained
attention. This narrative stimulus was used during the decoder construction phase to
model continuous neural tracking in an ecologically valid context. The resulting subject-
specific decoder was then applied to EEG recordings from the Flemish Matrix sentence
test, which was conducted under different SNR conditions. These syntactically controlled,
semantically neutral sentences allowed for precise estimation of the speech envelope in
a noise-controlled environment. The correlation between the estimated envelope and the
envelope of the clean matrix sentence was assessed using Pearson’s correlation coefficient.
The time-lag parameter τ was selected within a range of 0–500 ms, following guidelines
from previous studies [10]. The L2 regularization parameter λ was set at 103 determined
through an iterative search process aimed at optimizing detection accuracy [57].
Statistical analysis—Statistical analysis was performed using the R (version 3.3.2)
software. A p-value of 0.05 was considered to indicate statistical significance. Initially, we
employed a two-way mixed analysis of variance (ANOVA) to assess the effect of varying
noise levels on behavioral performance, including the hit rate and reaction time. The
hit rate and reaction time data underwent independent analyses using a 2 (age group:
Younger subjects, Older subjects) × 4 (SRS condition: 25%, 50%, 75%, and 95%) mixed
ANOVA. Additionally, ANOVA analyses were conducted on the neural tracking to explore
how different frequency bands (delta and theta) varied with noise levels based on age
group. This methodological approach enhanced our understanding of the interaction
between age and noise levels in both the behavioral and neural measurements. The F scores
and p-values derived from the ANOVA analysis were utilized to ascertain the statistical
significance of the observed difference. A further exploration of specific group comparisons
and identification of significant pairwise differences were conducted through post hoc
model comparisons using Bonferroni-corrected paired t-tests.
Brain Sci. 2025, 15, 874 10 of 22
Secondly, to explore the relationship between cognitive abilities and speech under-
standing or age, we conducted a descriptive statistical analysis of the demographic data,
hearing tests, cognition tests, and language assessments. Pearson correlation analysis was
conducted to examine the relationships between the participants’ age, SRT, PTA, neural
tracking of SRS in noise, MMSE, and CERAD-K test. The CERAD-K consists of two parts:
(1) verbal working memory (word list memory, word list recall, word list recognition), and
(2) visual working memory (constructional recall). In this analysis, we focused on visual
and verbal working memory, as these areas are closely related to the cognitive domains
involved in speech recognition in noise.
Lastly, the multiple regression analysis was performed with the working memory task
results as the dependent variable and the neural tracking of SRS at different noise levels
(25%, 50%, 75%, and 95%) as the independent variables (working memory part of CERAD-
K). Finally, to explore the relationship between working memory and neural tracking of SRS
at noise levels according to SRT, a multiple regression analysis was conducted, dividing
the participants into higher and lower groups based on the median value of their SRT.
Specifically, the two groups were divided based on a median SRT of 15 dB HL: participants
with thresholds higher than 15 dB HL were classified as the higher SRT group, while those
with thresholds lower than the median were classified as the lower SRT group. Statistical
significance was set at p < 0.05.
Throughout all of our analyses, we calculated effect sizes to evaluate the strength of our
results. Specifically, an eta square effect size (η2) was categorized as follows: 0.01 indicates
a small effect, 0.06 a medium effect, and 0.14 a large effect. Similarly, for Cohen’s d, effect
sizes will be interpreted with 0.2 representing a small effect, 0.5 a medium effect, and 0.8 a
large effect [58].
3. Results
3.1. Behavioral Evaluation of SRS
To compare listening effort in terms of accuracy and reaction time, we conducted
a two-way mixed ANOVA involving age groups (2) and SRS conditions (4). Figure 2A
revealed a significant main effect of the SRS conditions on hit rate (F (3, 132) = 107.432,
p = 0.0002, η2 = 0.39), indicating a notable influence of varied SRS noise conditions on
the participants’ hit rate. However, there was no significant main effect of age group
(F(1, 44) = 3.343, p = 0.0743), suggesting that age did not significantly affect the hit rate.
The interaction between age group and the SRS noise conditions was not significant
(F(3, 132) = 1.795, p = 0.151), implying that, as noise levels decreased, the hit rate increased
for both age groups. Post hoc comparisons revealed significant differences in hit rates, with
all SRS levels showing significant differences (p < 0.05).
Regarding reaction time (Figure 2B), differences were observed between the younger
and older groups. Both the SRS conditions (F (3, 132) = 3.989, p = 0.0093, η2 = 0.28) and
groups (F(1, 44) = 19.43, p = 0.0001, η2 = 0.41) showed significant main effects, suggesting
varied responses based on noise conditions and age group. A significant age group-by-
SRS condition interaction (F(3, 132) = 5.164, p = 0.00209, η2 = 0.32) indicated a differential
performance decline in reaction time for both age groups. Post hoc comparisons revealed
a significant performance difference between the SRS 25% condition and the residual
conditions (SRS 50%, 75%, and 95%) for the older group (p < 0.05). However, for the younger
group, there was no significance across all SRS conditions. These results suggest that the
older participants exhibited increased listening effort in severe noise level conditions.
Brain Sci. 2025, 15, 874 11 of 22
Figure 2. Behavioral result (hit rate and reaction time) under each noise level (SRS 25%, 50%, 75%
and 95%). (A) The hit rate across different SRS noise conditions. The younger group is represented
by dark bars, while the older group is represented by white bars. Each bar shows the mean hit rate,
with individual participant data overlaid as dots. (B) The reaction times (in seconds) for both groups
under the noise conditions, with the younger group data in dark bars and the older group in white
bars. The reaction times for individual participants are shown as dots. Error bars represent the mean
± SEM. Black bars indicate * p < 0.05. The dots are individual data points for the older (white dots)
and younger groups (black dots).
3.2. Age-Related Differences in Neural T racking of Speech in Noise
To investigate the differences in neural tracking of different frequency bands when
perceiving speech in noise across age groups, we computed the speech envelope in the
delta and theta bands based on the decoders trained while listening to clean story. The
neural tracking data were subjected to a 2 (age group) × 4 (SRS conditions: SRS 25%, 50%,
75%, and 95%) mixed ANOVA, with the SRS condition as the within-subjects factor and
age group as the between-subjects factor (Figure 3).
Figure 3. Neural tracking of speech in delta and theta bands across different noise conditions for
older and younger groups. (A) The neural tracking within the delta frequency band across the SRS
noise conditions (SRS 25%, 50%, 75%, and 95%). (B) For the theta frequency band. In both figures,
the younger group is denoted by dark bars and the older group by white bars. Each dot represents
an individual participant, and the central line on each box indicates the median value. Error bars
represent the mean ± SEM. Black bracket indicate * p < 0.05. The dots are individual data points for
the older (white dots) and younger groups (black dots).
Brain Sci. 2025, 15, 874 12 of 22
In the delta band, there was no significant main effect or interaction (Figure 3A).
On the other hand, in the theta band, there was a main effect for the age group factor
(F(1, 44) = 11.06, p = 0.0017, η2 = 0.21), but no significance for the SRS conditions factor or
interaction. Post hoc comparisons demonstrated a significant difference between age group
for all SRS conditions ( p < 0.05) except the SRS 50%, but it also showed close statistical
significance (p = 0.063) (Figure 3B). These findings suggest that the theta band might be
more involved in speech recognition among older groups in noise conditions.
3.3. Correlations Between Cognitive Function, Age, and Hearing Ability in Older Adults (PTA
and SRT)
To evaluate the interplay among cognition, age, and hearing ability, Pearson’s corre-
lations were employed to determine the relationship between participants’ MMSE score
and age, education level, as well as hearing ability. Figure 4 revealed that the MMSE score
was significantly negatively correlated with age (r = −0.42, p = 0.046, Cohen’sd = 0.58) and
significantly negatively correlated with the SRT ( r = −0.46, p = 0.027, Cohen’s d = 0.54).
However, there was no relationship with other factors (PTA, education level). This sug-
gests a correlation between age-related cognitive decline and the deterioration of hearing
sensitivity. Please note that the significance levels displayed here have been adjusted for
multiple comparisons.
Figure 4. The correlation of MMSE-KC scores with age and the SRT. (A) The relationship between the
MMSE-KC scores and age. Each dot represents an older adults score, with the trend line indicating
the direction of the correlation. (B) The correlation between the MMSE-KC scores and the SRT. The
trend line also indicates the correlation direction between the cognitive scores and hearing ability.
To identify the relationship between cognitive function and theta-band neural tracking
at each noise level, a multiple linear regression analysis was conducted. The dependent
variables were cognitive function measures (MMSE and working memory tests: word list
memory, word list recall, word list recognition, and Constructional recall).Table 2 shows
the results of the multiple regression analysis for each cognitive function test. The regression
equation for word list recognition was significant, F(4, 18) = 3.427, p < 0.05, accounting for
43.2% of the variance (R2 = 0.432). Neural tracking at SRS 25% and SRS 75% significantly
contributed to the predictions (p < 0.05). Except for word list recognition, other working
memory test did not show significant contributions.
Brain Sci. 2025, 15, 874 13 of 22
Table 2. Summary of the results of multiple regression analyses for each computerized cognitive
function tests with predictors (n = 23).
Subtest Score Predictor Standardized
Beta Coefficient R Square
MMSE
Neural tracking in SRS25 −0.110
0.118Neural tracking in SRS50 0.282
Neural tracking in SRS75 0.027
Neural tracking in SRS95 −0.432
Word list memory
Neural tracking in SRS25 0.238
0.024Neural tracking in SRS50 0.089
Neural tracking in SRS75 −0.049
Neural tracking in SRS95 −0.056
Word list
recall
Neural tracking in SRS25 −0.286
0.317Neural tracking in SRS50 0.418
Neural tracking in SRS75 −0.465
Neural tracking in SRS95 0.107
Word list recognition
Neural tracking in SRS25 0.683 *
0.432 *Neural tracking in SRS50 0.163
Neural tracking in SRS75 −0.997 *
Neural tracking in SRS95 0.056
Constructional recall
Neural tracking in SRS25 0.4470
0.086Neural tracking in SRS50 0.191
Neural tracking in SRS75 −0.281
Neural tracking in SRS95 −0.262
* p < 0.05, SRS: Speech Recognition Scorer MMSE: Mini-Mental Status Examination-Korea.
3.4. Correlation with Working Memory of Older Adults with Different Hearing Abilities
Given the observed relationship between word list recognition and theta-band neural
tracking in noise, we conducted an additional multiple regression analysis to test whether
theta-band neural tracking was correlated with cognitive functions, particularly working
memory based on hearing ability. Specifically, the two groups were divided based on the
median value of their SRT levels, which was 15 dB HL. The group with thresholds higher
than 15 dB HL was classified as the higher SRT group, while the group with thresholds
lower than the median value was classified as the lower SRT group (Table 3). For the
lower SRT group, a significant regression solution was obtained for constructional recall,
F(4, 8) = 8.064, p < 0.05, accounting for 80.1% of the variance (R 2 = 0.801). This is also
indicated by a positive correlation for neural tracking at SRS 25% and SRS 50%, and a
negative correlation for neural tracking at SRS 95% as significant predictors (p < 0.05). On
the other hand, for the higher SRT group, the regression equation for word list recognition
approached significance, F(4, 5) = 4.632, p = 0.052, accounting for 78.7% of the variance
(R2 = 0.787), with a positive correlation for neural tracking at SRS 25% and a negative
correlation for neural tracking at SRS 75% as significant predictors (p < 0.05).
Table 3. Summary of the results of multiple regression analyses for working memory tests with
predictors (lower SRT group = 13, higher SRT group = 10).
Group Subtest Score Predictor Standardized
Beta Coefficient R Square
lower SRT group
Word list memory
Neural tracking in SRS25 0.302
0.419Neural tracking in SRS50 0.384
Neural tracking in SRS75 0.667
Neural tracking in SRS95 −0.801
Word list recall
Neural tracking in SRS25 −1.556
0.507Neural tracking in SRS50 −0.740
Neural tracking in SRS75 −0.937
Neural tracking in SRS95 1.645
Brain Sci. 2025, 15, 874 14 of 22
Table 3. Cont.
Group Subtest Score Predictor Standardized
Beta Coefficient R Square
lower SRT group
Word list recognition
Neural tracking in SRS25 0.329
0.270Neural tracking in SRS50 −0.070
Neural tracking in SRS75 −0.132
Neural tracking in SRS95 −0.446
Constructional recall
Neural tracking in SRS25 0.958 **
0.801 *Neural tracking in SRS50 0.691 **
Neural tracking in SRS75 −0.077
Neural tracking in SRS95 −0.713 *
higher SRT group
Word list memory
Neural tracking in SRS25 0.032
0.114Neural tracking in SRS50 0.169
Neural tracking in SRS75 −0.558
Neural tracking in SRS95 0.236
Word list recall
Neural tracking in SRS25 0.103
0.540Neural tracking in SRS50 1.426
Neural tracking in SRS75 −1.015
Neural tracking in SRS95 −0.055
Word list recognition
Neural tracking in SRS25 0.888 *
0.787 *Neural tracking in SRS50 0.715
Neural tracking in SRS75 −1.536 *
Neural tracking in SRS95 −0.087
Constructional recall
Neural tracking in SRS25 −0.203
0.453Neural tracking in SRS50 −0.638
Neural tracking in SRS75 0.074
Neural tracking in SRS95 0.004
* p < 0.05, ** p < 0.01 SRT: Speech Recognition Threshold.
4. Discussion
4.1. Age-Related Changes in Speech Perception in Noise
In the current study, we investigated the effect of age on speech recognition perfor-
mance among individuals with normal hearing. It was observed that as the SRS decreased,
the hit rate for the older group decreased, while the reaction time increased (Figure 2).
These findings are consistent with previous studies, which show that older listeners are
more adversely influenced by background noise compared to younger listeners [ 59,60].
Yanz and Anderson [60] reported a notable increase in the precision of word recognition
among the younger participants when the SNR was adjusted from 0 to 5 dB. However,
older listeners showed no significant change under all SNR conditions. Furthermore, [59]
suggested that the diminished ability of older adults to successfully perform speech recog-
nition tasks might be linked to their less effective use of contextual information. Also,
when younger and older adults listen to speech at the SNR 0 dB, older people often find
it harder to understand, need more effort [ 38], and take longer to respond [ 61,62]. As
people age, the difficulty in recognizing speech in noise is caused not only by a decline in
the peripheral auditory system but also by a decline in central auditory function [47,63].
Several studies show that deficits in central auditory function could make it more difficult
to distinguish target sounds from background noise as the noise level increases [ 64,65].
Previous studies have also reported that cognitive overload caused by external variables
such as background noise during listening tasks can lead to increased response time on the
task or abandonment of the task [66,67]. These findings support our results, which show
that older adults, compared to younger adults, have slower response times as noise levels
increase. This suggests that older adults experienced greater listening effort under severe
noise conditions.
4.2. Neural T racking Changes Across Aging
We conducted further investigations to understand how neural tracking during speech
recognition in noise differs according to age. Our results showed that delta-band neural
tracking did not differ between younger and older listeners in any of the SRS conditions.
Brain Sci. 2025, 15, 874 15 of 22
However, theta-band neural tracking was greater for older listeners than younger listeners.
Our findings, consistent with Kurthen, Christen [ 68] highlight age-related adaptations
in neural processing of speech in challenging auditory conditions. While delta-band
neural tracking did not differ significantly between younger and older adults in our study,
older listeners showed greater theta-band neural tracking compared to younger listeners.
They demonstrated that this enhanced theta-band tracking in older adults was positively
associated with understanding interrupted speech, suggesting a compensatory mechanism
for processing degraded auditory input. Similarly, our findings indicate that older adults
might use increased theta-band tracking to support speech recognition in noise, potentially
compensating for age-related declines in auditory processing.
Previous studies have shown that theta oscillations reflect neural sensitivity to the
slow-rate envelope in the auditory cortex [ 69–71], which plays a critical role in speech
perception in noise [72–74]. Specifically, research on neural tracking in the theta frequency
band has demonstrated that it is a significant predictor of perceived speech clarity, primarily
reflecting the acoustics of the stimulus. In contrast, neural tracking in the delta band has
been found to predict speech comprehension, suggesting an association with higher-level
linguistic aspects of speech, such as syntax and semantics. This indicates that while theta
band tracking is linked to the physical properties of sound, delta band tracking relates to
the understanding of speech content [8,9,75,76]. Furthermore, the enhanced neural tracking
observed in older adults and those with hearing impairment is thought to result from
central compensatory mechanisms that increase cortical activity to compensate for the
degraded peripheral input [56,77,78]. In this context, the observed increase in theta band
neural tracking in our study may reflect neural compensatory mechanisms in response
to the diminished clarity of phoneme and syllable boundaries due to the presence of
background noise.
4.3. Relation Between Neural T racking and Working Memory in Older Adults
The correlation analysis on MMSE and hearing ability revealed that general cogni-
tive function (MMSE) showed a negative correlation with SRT and age. This finding is
consistent with previous studies that have demonstrated a significant relationship be-
tween MMSE scores and demographic variables such as age and education in the general
population [79–82]. To extend the correlation analysis results, we also performed a linear
regression analysis between the scores of working memory test in CERAD-K (word list
recall, word list memory, word list recognition, and constructional recall) and theta-band
neural tracking of the speech envelope across different noise levels. With regard to work-
ing memory, we found that theta-band neural tracking could significantly predict the
performance of word list recognition (Table 2).
Furthermore, we explored the relation between cognitive function and speech percep-
tion by categorizing the participants into two groups according to their ability to recognize
speech in noise. Specifically, the two groups were divided based on the median values of
their SRT levels. Our study observed that older adults with lower SRT and higher SRT
group showed different correlation patterns in theta-band neural tracking across different
working memory tasks (word list recognition and constructional recall).
In the lower SRT group, the regression analysis results indicate that SRS 25% and
SRS 50% have a significant positive effect on constructional recall. In particular, SRS 25%
has the highest standardized coefficient ( β = 0.958) and t-value (4.480), making it the
strongest predictor of visual working memory score. Conversely, in the higher SRT group,
the regression analysis results showed that the SRS 25% noise condition has a significant
positive effect on word recognition ability (Table 3).
Brain Sci. 2025, 15, 874 16 of 22
In higher SRT group, the positive relationship with word list recognitions, which
related the verbal working memory, can potentially be explained by the information
degradation hypothesis. According to this hypothesis [83], older adults may increasingly
rely on cognitive resources to compensate for sensory deficits. This reliance, in turn,
can deplete the resources available for other cognitive tasks, resulting in a comparative
decline in cognitive performance relative to younger adults. In this regard, the information
degradation hypothesis may explain why the higher SRT group exhibited an increased
envelope correlation at higher word list recognition specially in SRS 25% which is severe
noise conditions. Individuals in the higher SRT group, indicating hearing deficits, may
have exerted more effort in listening tasks with a greater reliance on verbal working
memory. Indeed, previous studies have also confirmed that sensory deficits are associated
with increased listening effort and greater demands on working memory resources [84–86].
Similarly, although age groups differ, several studies have found that children with cochlear
implants (CIs) perform worse than normal hearing peers in complex verbal working
memory [87–89].
In contrast, among those with a lower SRT, a positive correlation was observed between
neural tracking and the constructional recall, which reflects the visual working memory.
This finding could align with prior research indicating increased visual cortex activity in
the elderly when trying to perceive speech in noise [90,91] but further study is necessary
to understand the relationship between visual-working memory and neural tracking of
speech in noise for older adults.
Additionally, both SRT groups showed a negative correlation in the SRS 75% and SRS
95% conditions for word list recognition and constructional recall. This observation could
be explained by the Ease of Language Understanding (ELU) model. According to the ELU
model, when listening conditions are optimal, speech input is quickly and automatically
matched with phonological representations stored in semantic long-term memory, allowing
access to the lexicon. This process does not place a burden on working memory, which
involves the ability to simultaneously process and store phonological and semantic informa-
tion and to draw inferences for both predictive and reflective purposes [92–94]. Therefore,
the SRS 75% and 95% conditions, which have less noise compared to the SRS 25% and
50% conditions, exert less demand on working memory processing.
4.4. Limitations and Future Work
In this study, we investigated the relationship between cognitive function and neural
envelope tracking of speech in noise. The regression analysis revealed that the SRT groups
exhibit different patterns of correlation with the working memory task. However, the
regression results alone are not sufficient to fully explain how working memory influences
neural envelope tracking of speech in noise. One of the main limitations of our study is
the difficulty in directly explaining the relationship between auditory cognitive ability in
processing speech in noise, cognitive function, and language skills. Although our study
provides valuable insights into the role of working memory in speech understanding, we
did not simultaneously assess other cognitive factors, such as attention, linguistic skills,
which have been reported to impact speech perception in noise [ 95,96]. As a result, our
findings, while significant, may not fully capture the complex interplay between cognitive
and linguistic skills and neural envelope tracking of speech in noise. To build upon our
current findings and gain a more comprehensive understanding of these relationships,
future research should aim to incorporate a more comprehensive battery of tests, assessing
a broader range of cognitive functions and language ability alongside EEG data collection.
This approach would enable a more in-depth understanding of how these factors contribute
to speech perception in challenging listening environments and their direct influence on
Brain Sci. 2025, 15, 874 17 of 22
neural envelope tracking. Also, hearing loss or lack in temporal spectral encoding and other
sensory inputs can affect cognitive functions [26]. Previous studies have shown that patients
with deficits in auditory attention and memory have difficulty in understanding speech in
noisy environments [97,98]. Since our study was conducted on older adults with normal
hearing, it is also difficult to separate and interpret pure auditory ability from cognitive
function. Additionally, mild cognitive impairment (MCI) can affect the neural processing
of speech in noise, but our study did not adequately capture the full spectrum of cognitive
impairments. These limitations mean that we could not fully address the hypothesis
concerning the interplay between cognitive functions and neural processing of speech in
noise. Future research should include a broader cohort of older adults with varying levels
of cognitive impairments and hearing abilities, encompassing those with normal hearing
and those with hearing deficits. This would allow for a more thorough investigation into
how different cognitive abilities interact with auditory processing, potentially providing a
clearer understanding of the underlying mechanisms.
Another limitation of our study is that it is difficult to clearly distinguish and explain
the processing of speech in noise as either pure sensory processing or cognitive processing.
Perceiving speech in noise involves a complex interplay of auditory and cognitive processes.
Both bottom-up processing, which involves the direct analysis of acoustic signals, and top-
down processing, which uses context and prior knowledge, are crucial for speech in noise
processing [99]. In this study, we measured sentence recall under noise conditions by having
older adults with normal hearing listen to sentences in noisy environments. Additionally,
neural envelope tracking was measured by correlating the original envelope of the matrix
sentences with the envelope reconstructed from the EEG responses. In this regard, this
study likely involved the top-down processing, as the task required focusing on target
sentences in noise and recalling the perceived sentence. In contrast, a recent study by Mai
and Howell [100] investigated how early-stage phase-locked neural activities, specifically
the frequency-following response (FFR) and theta-band phase-locking values ( θ-PLV),
contribute to speech-in-noise (SiN) perception across different ages and levels of hearing
loss. Their study provided evidence of distinct early-stage neural mechanisms through
which aging and hearing loss affect speech-in-noise perception. Based on prior research
designs, future studies should design additional experiments that use vowel acoustic
stimuli to investigate early-stage neural activity, considering both pure sensory processing
and processes involving cognitive functions. In addition, the matrix sentence-in-noise
paradigm used in our study may not fully reflect real-life speech perception environments,
which presents a limitation. Future research should take this into account and develop
follow-up experiments that incorporate more ecologically valid listening conditions.
Although the language background of the younger and older participant groups was
matched, as all participants were native Korean speakers, we did not control for other po-
tential confounding variables such as sex, education level, and socioeconomic status during
recruitment. This limitation restricts the generalizability of our findings. In addition, we
assumed that the younger participants had normal cognitive function and did not formally
assess their cognitive status. Future studies should consider evaluating and comparing cog-
nitive function across age groups to better understand how age-related cognitive variability
may influence speech-in-noise perception and neural processing. Furthermore, in older
adults, not only cognitive function but also hearing loss—particularly in the high-frequency
range—should be carefully considered. Therefore, future research should incorporate
both age-related cognitive status and hearing sensitivity to more accurately assess their
combined effects on neural tracking and speech perception in noise.
Brain Sci. 2025, 15, 874 18 of 22
5. Conclusions
This study investigated the relationship between cognitive function and neural enve-
lope tracking during speech perception in noise among individuals with normal hearing.
Our findings suggest that theta-band neural tracking may play a compensatory role in
supporting speech understanding in challenging listening conditions, particularly among
individuals with lower speech reception thresholds (SRT). Additionally, working memory
performance was differentially associated with neural tracking depending on SRT-based
group classification, highlighting individual variability in cognitive–neural interactions.
However, the results are correlational in nature and cannot confirm causal relationships.
Furthermore, potential confounding factors such as sex, education level, and cognitive
reserve were not controlled, and the generalizability of the findings is limited due to the
inclusion of only normal-hearing older adults. Future research should expand participant
diversity and include formal cognitive assessments for all age groups to clarify how age,
cognition, and hearing jointly influence speech-in-noise processing.
Author Contributions: H.A.: Conceptualization, data curation, formal analysis, investigation,
methodology, software, validation, visualization, writing—original draft, writing—review and edit-
ing. J.L.: data curation, visualization, writing—review and editing. Y.-j.P .: funding acquisition.
M.-W.S.: investigation, resources, resources. Y.L.: conceptualization, funding acquisition, investiga-
tion, methodology, Writing—review and editing, project administration. All authors have read and
agreed to the published version of the manuscript.
Funding: This work was supported in part by a National Research Council of Science & Technology
(NST) grant from the Korean Government (MSIT) (No.CAP21053-200). This research was supported
by a National Research Foundation of Korea (NRF) grant funded by the Korean Government (MSIT)
(RS-2024-00461617).
Institutional Review Board Statement: All the procedures in this study followed the ethical standards
of the Declaration of Helsinki and were approved by the Institutional Review Board (IRB) of Seoul
National University Hospital (IRB codes:2009-090-1157 and H-2112-075-1282, respectively).
Informed Consent Statement: Informed consent was obtained from all subjects involved inthe study.
Data Availability Statement: Data are available from the corresponding author upon reasonable
request due to ethical reasons.
Conflicts of Interest: The authors declare no conflicts of interest.
Abbreviations
The following abbreviations are used in this manuscript:
EEG Electroencephalography
SNR Signal-to-Noise Ratio
PTA Pure Tone Average
SRT Speech Reception Threshold
HL Hearing Level
CERAD-K The Korean version of Disease Neuropsychological Assessment
MMSE-K The Korean version of Mini-Mental Status Examination
SBT-K The Korean version of the Short Blessed Test
K-BNT Korean version of the Boston Naming Test
SRS Speech Recognition Scores
SSN Speech-Shaped Noise
ANSI American National Standards Institute
MCI Mild Cognitive Impairment
Brain Sci. 2025, 15, 874 19 of 22
FFR Frequency-Following Response
SiN Speech-in-Noise
θ-PLV Theta-Band Phase-Locking Values
References
1. Abel, S.M.; Sass-Kortsak, A.; Naugler, J.J. The role of high-frequency hearing in age-related speech understanding deficits. Scand.
Audiol. 2000, 29, 131–138. [CrossRef] [PubMed]
2. Souza, P .E.; Turner, C.W. Masking of speech in young and elderly listeners with hearing loss.J. Speech Hear. Res. 1994, 37, 655–661.
[CrossRef] [PubMed]
3. Gates, G.A.; Mills, J.H. Presbycusis. Lancet. 2005, 366, 1111–1120. [CrossRef] [PubMed]
4. Fjell, A.M.; Walhovd, K.B.; Fennema-Notestine, C.; McEvoy, L.K.; Hagler, D.J.; Holland, D.; Brewer, J.B.; Dale, A.M. One-year
brain atrophy evident in healthy aging. J. Neurosci. 2009, 29, 15223–15231. [CrossRef]
5. Ouda, L.; Profant, O.; Syka, J. Age-related changes in the central auditory system. Cell Tissue Res. 2015, 361, 337–358. [CrossRef]
6. Wassenaar, T.M.; Yaffe, K.; van der Werf, Y.D.; Sexton, C.E. Associations between modifiable risk factors and white matter of the
aging brain: Insights from diffusion tensor imaging studies. Neurobiol. Aging 2019, 80, 56–70. [CrossRef]
7. Alain, C.; Roye, A.; Salloum, C. Effects of age-related hearing loss and background noise on neuromagnetic activity from auditory
cortex. Front. Syst. Neurosci. 2014, 8, 8. [CrossRef]
8. Ding, N.; Chatterjee, M.; Simon, J.Z. Robust cortical entrainment to the speech envelope relies on the spectro-temporal fine
structure. Neuroimage 2014, 88, 41–46. [CrossRef]
9. Etard, O.; Reichenbach, T. Neural Speech Tracking in the Theta and in the Delta Frequency Band. Differentially Encode Clarity
and Comprehension of Speech in Noise. J. Neurosci. 2019, 39, 5750–5759. [CrossRef]
10. O’SUllivan, J.A.; Power, A.J.; Mesgarani, N.; Rajaram, S.; Foxe, J.J.; Shinn-Cunningham, B.G.; Slaney, M.; Shamma, S.A.; Lalor, E.C.
Attentional Selection in a Cocktail Party Environment Can Be Decoded from Single-Trial EEG. Cereb. Cortex 2015, 25, 1697–1706.
[CrossRef]
11. Presacco, A.; Simon, J.Z.; Anderson, S. Speech-in-noise representation in the aging midbrain and cortex: Effects of hearing loss.
PLoS ONE 2019, 14, e0213899. [CrossRef]
12. Vanthornhout, J.; Decruy, L.; Wouters, J.; Simon, J.Z.; Francart, T. Speech Intelligibility Predicted from Neural Entrainment of the
Speech Envelope. J. Assoc. Res. Otolaryngol. 2018, 19, 181–191. [CrossRef]
13. Sommers, M.S.; Danielson, S.M. Inhibitory processes and spoken word recognition in young and older adults: The interaction of
lexical competition and semantic context. Psychol. Aging 1999, 14, 458–472. [CrossRef]
14. Tiedt, H.O.; Ehlen, F.; Klostermann, F. Age-related dissociation of N400 effect and lexical priming. Sci. Rep. 2020, 10, 20291.
[CrossRef]
15. Giraud, A.-L.; Poeppel, D. Cortical oscillations and speech processing: Emerging computational principles and operations. Nat.
Neurosci. 2012, 15, 511–517. [CrossRef] [PubMed]
16. Ding, N.; Simon, J.Z. Emergence of neural encoding of auditory objects while listening to competing speakers. Proc. Natl. Acad.
Sci. USA 2012, 109, 11854–11859. [CrossRef] [PubMed]
17. Schroeder, C.E.; Lakatos, P . Low-frequency neuronal oscillations as instruments of sensory selection. T rends Neurosci. 2009,
32, 9–18. [CrossRef] [PubMed]
18. Keshavarzi, M.; Kegler, M.; Kadir, S.; Reichenbach, T. Transcranial alternating current stimulation in the theta band but not in the
delta band modulates the comprehension of naturalistic speech in noise. Neuroimage 2020, 210, 116557. [CrossRef]
19. Brodbeck, C.; Presacco, A.; Anderson, S.; Simon, J.Z. Over-representation of speech in older adults originates from early response
in higher order auditory cortex. Acta Acust. United Acust. 2018, 104, 774–777. [CrossRef]
20. Ding, N.; Melloni, L.; Zhang, H.; Tian, X.; Poeppel, D. Cortical tracking of hierarchical linguistic structures in connected speech.
Nat. Neurosci. 2016, 19, 158–164. [CrossRef]
21. McHaney, J.R.; Gnanateja, G.N.; Smayda, K.E.; Zinszer, B.D.; Chandrasekaran, B. Cortical Tracking of Speech in Delta Band
Relates to Individual Differences in Speech in Noise Comprehension in Older Adults. Ear Hear. 2021, 42, 343–354. [CrossRef]
22. Slade, K.; Plack, C.J.; Nuttall, H.E. The Effects of Age-Related Hearing Loss on the Brain and Cognitive Function. T rends Neurosci.
2020, 43, 810–821. [CrossRef]
23. Fitzhugh, M.C.; Schaefer, S.Y.; Baxter, L.C.; Rogalsky, C. Cognitive and neural predictors of speech comprehension in noisy
backgrounds in older adults. Lang. Cogn. Neurosci. 2021, 36, 269–287. [CrossRef]
24. Harris, K.C.; Eckert, M.A.; Ahlstrom, J.B.; Dubno, J.R. Age-related differences in gap detection: Effects of task difficulty and
cognitive ability. Hear. Res. 2010, 264, 21–29. [CrossRef]
25. Schvartz, K.C.; Chatterjee, M.; Gordon-Salant, S. Recognition of spectrally degraded phonemes by younger, middle-aged, and
older normal-hearing listeners. J. Acoust. Soc. Am. 2008, 124, 3972–3988. [CrossRef] [PubMed]
Brain Sci. 2025, 15, 874 20 of 22
26. Wong, P .C.M.; Ettlinger, M.; Sheppard, J.P .; Gunasekera, G.M.; Dhar, S. Neuroanatomical characteristics and speech perception in
noise in older adults. Ear Hear. 2010, 31, 471–479. [CrossRef] [PubMed]
27. Wong, P .C.M.; Uppunda, A.K.; Parrish, T.B.; Dhar, S. Cortical mechanisms of speech perception in noise.J. Speech Lang. Hear. Res.
2008, 51, 1026–1041. [CrossRef] [PubMed]
28. Conway, A.R.A.; Cowan, N.; Bunting, M.F. The cocktail party phenomenon revisited: The importance of working memory
capacity. Psychon. Bull. Rev. 2001, 8, 331–335. [CrossRef]
29. Kane, M.J.; Bleckley, M.K.; Conway, A.R.A.; Engle, R.W. A controlled-attention view of working-memory capacity.J. Exp. Psychol.
Gen. 2001, 130, 169–183. [CrossRef]
30. Füllgrabe, C.; Rosen, S. Investigating the Role of Working Memory in Speech-in-noise Identification for Listeners with Normal
Hearing. Adv. Exp. Med. Biol. 2016, 894, 29–36. [CrossRef]
31. Nagaraj, N.K. Working Memory and Speech Comprehension in Older Adults With Hearing Impairment. J. Speech Lang. Hear. Res.
2017, 60, 2949–2964. [CrossRef]
32. Nagaraj, N.K.; Knapp, A.N. No evidence of relation between working memory and perception of interrupted speech in young
adults. J Acoust Soc Am. 2015, 138, EL145–EL150. [CrossRef]
33. Classon, E.; Rudner, M.; Rönnberg, J. Working memory compensates for hearing related phonological processing deficit.
J. Commun. Disord. 2013, 46, 17–29. [CrossRef] [PubMed]
34. McGarrigle, R.; Munro, K.J.; Dawes, P .; Stewart, A.J.; Moore, D.R.; Barry, J.G.; Amitay, S. Listening effort and fatigue: What exactly
are we measuring? A British Society of Audiology Cognition in Hearing Special Interest Group ‘white paper’.Int. J. Audiol. 2014,
53, 433–440. [CrossRef] [PubMed]
35. Peelle, J.E. Listening Effort: How the Cognitive Consequences of Acoustic Challenge Are Reflected in Brain and Behavior. Ear
Hear. 2018, 39, 204–214. [CrossRef] [PubMed]
36. Gatehouse, S.; Gordon, J. Response times to speech stimuli as measures of benefit from amplification. Br. J. Audiol. 1990, 24, 63–68.
[CrossRef]
37. Heinrich, A.; Schneider, B.A.; Craik, F.I. Investigating the influence of continuous babble on auditory short-term memory
performance. Q. J. Exp. Psychol. 2008, 61, 735–751. [CrossRef]
38. Houben, R.; van Doorn-Bierman, M.; Dreschler, W.A. Using response time to speech as a measure for listening effort.Int. J. Audiol.
2013, 52, 753–761. [CrossRef]
39. Kramer, S.E.; Kapteyn, T.S.; Festen, J.M.; Kuik, D.J. Assessing aspects of auditory handicap by means of pupil dilatation.Audiology
1997, 36, 155–164. [CrossRef]
40. Zekveld, A.A.; Kramer, S.E. Cognitive processing load across a wide range of listening conditions: Insights from pupillometry.
Psychophysiology 2014, 51, 277–284. [CrossRef]
41. Zekveld, A.A.; Kramer, S.E.; Festen, J.M. Cognitive load during speech perception in noise: The influence of age, hearing loss,
and cognition on the pupil response. Ear Hear. 2011, 32, 498–510. [CrossRef]
42. Pichora-Fuller, M.K.; Souza, P .E. Effects of aging on auditory processing of speech. Int J Audiol. 2003, 42 (Suppl. S2), 11–16.
[CrossRef]
43. Tun, P .A.; McCoy, S.; Wingfield, A. Aging, hearing acuity, and the attentional costs of effortful listening.Psychol. Aging. 2009,
24, 761–766. [CrossRef] [PubMed]
44. Ward, K.M.; Shen, J.; Souza, P .E.; Grieco-Calub, T.M. Age-Related Differences in Listening Effort During Degraded Speech
Recognition. Ear Hear. 2017, 38, 74–84. [CrossRef] [PubMed]
45. Wisniewski, M.G.; Thompson, E.R.; Iyer, N.; Estepp, J.R.; Goder-Reiser, M.N.; Sullivan, S.C. Frontal midline theta power as an
index of listening effort. Neuroreport 2015, 26, 94–99. [CrossRef]
46. Kim, J.-S.; Lim, D.; Hong, H.-N.; Shin, H.-W.; Lee, K.-D.; Hong, B.-N.; Lee, J.-H. Development of Korean Standard Monosyllabic
Word Listsfor Adults (KS-MWL-A). Audiol. Speech Res. 2008, 4, 126–140. [CrossRef]
47. Dobreva, M.S.; O’Neill, W.E.; Paige, G.D. Influence of aging on human sound localization.J. Neurophysiol. 2011, 105, 2471–2486.
[CrossRef]
48. Poelmans, H.; Luts, H.; Vandermosten, M.; Ghesquière, P .; Wouters, J. Hemispheric asymmetry of auditory steady-state responses
to monaural and diotic stimulation. J. Assoc. Res. Otolaryngol. 2012, 13, 867–876. [CrossRef]
49. Lee, J.H.; Lee, K.U.; Lee, D.Y.; Kim, K.W.; Jhoo, J.H.; Kim, J.H.; Lee, K.H.; Kim, S.Y.; Han, S.H.; Woo, J.I. Development of the
Korean version of the Consortium to Establish a Registry for Alzheimer’s Disease Assessment Packet (CERAD-K): Clinical and
neuropsychological assessment batteries. J. Gerontol. B Psychol. Sci. Soc. Sci. 2002, 57, P47–P53. [CrossRef]
50. Folstein, M.F.; Folstein, S.E.; McHugh, P .R. “Mini-mental state”. A practical method for grading the cognitive state of patients for
the clinician. J. Psychiatr. Res. 1975, 12, 189–198. [CrossRef]
51. An, H.; Lee, J.; Suh, M.-W.; Lim, Y. Neural correlation of speech envelope tracking for background noise in normal hearing. Front.
Neurosci. 2023, 17, 1268591. [CrossRef] [PubMed]
Brain Sci. 2025, 15, 874 21 of 22
52. Heitz, R.P . The speed-accuracy tradeoff: History, physiology, methodology, and behavior.Front. Neurosci. 2014, 8, 150. [CrossRef]
[PubMed]
53. Crosse, M.J.; Di Liberto, G.M.; Bednar, A.; Lalor, E.C. The Multivariate Temporal Response Function (mTRF) Toolbox: A MATLAB
Toolbox for Relating Neural Signals to Continuous Stimuli. Front. Hum. Neurosci. 2016, 10, 604. [CrossRef] [PubMed]
54. Ding, N.; Simon, J.Z. Cortical entrainment to continuous speech: Functional roles and interpretations. Front. Hum. Neurosci. 2014,
8, 311. [CrossRef]
55. Calderone, D.J.; Lakatos, P .; Butler, P .D.; Castellanos, F.X. Entrainment of neural oscillations as a modifiable substrate of attention.
T rends Cogn. Sci. 2014, 18, 300–309. [CrossRef]
56. Chambers, A.R.; Resnik, J.; Yuan, Y.; Whitton, J.P .; Edge, A.S.; Liberman, M.C.; Polley, D.B. Central Gain Restores Auditory
Processing following Near-Complete Cochlear Denervation. Neuron. 2016, 89, 867–879. [CrossRef]
57. Wong, D.D.E.; Fuglsang, S.A.; Hjortkjær, J.; Ceolini, E.; Slaney, M.; de Cheveigné, A. A Comparison of Regularization Methods in
Forward and Backward Models for Auditory Attention Decoding. Front. Neurosci. 2018, 12, 531. [CrossRef]
58. Lakens, D. Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs.
Front. Psychol. 2013, 4, 863. [CrossRef]
59. Wingfield, A.; Poon, L.W.; Lombardi, L.; Lowe, D. Speed of processing in normal aging: Effects of speech rate, linguistic structure,
and processing time. J. Gerontol. 1985, 40, 579–585. [CrossRef]
60. Yanz, J.L.; Anderson, S.M. Comparison of speech perception skills in young and old listeners. Ear Hear. 1984, 5, 134–137.
[CrossRef]
61. Hultsch, D.F.; MacDonald, S.W.S.; Dixon, R.A. Variability in reaction time performance of younger and older adults.J. Gerontol. B
Psychol. Sci. Soc. Sci. 2002, 57, P101–P115. [CrossRef]
62. Salthouse, T.A. Selective review of cognitive aging. J. Int. Neuropsychol. Soc. 2010, 16, 754–760. [CrossRef] [PubMed]
63. Helfer, K.S.; Wilber, L.A. Hearing loss, aging, and speech perception in reverberation and noise. J. Speech Hear. Res. 1990,
33, 149–155. [CrossRef]
64. Ben-David, B.M.; Tse, V .Y.; Schneider, B.A. Does it take older adults longer than younger adults to perceptually segregate a speech
target from a background masker? Hear. Res. 2012, 290, 55–63. [CrossRef]
65. Snyder, J.S.; Alain, C. Age-related changes in neural activity associated with concurrent vowel segregation. Brain Res. Cogn. Brain
Res. 2005, 24, 492–499. [CrossRef]
66. Brungart, D.S.; Barrett, M.E.; Cohen, J.I.; Fodor, C.; Yancey, C.M.; Gordon-Salant, S. Objective Assessment of Speech Intelligibility
in Crowded Public Spaces. Ear Hear. 2020, 41 (Suppl. S1), 68S–78S. [CrossRef]
67. Wu, Y.-H.; Stangl, E.; Zhang, X.; Perkins, J.; Eilers, E. Psychometric Functions of Dual-Task Paradigms for Measuring Listening
Effort. Ear Hear. 2016, 37, 660–670. [CrossRef]
68. Kurthen, I.; Christen, A.; Meyer, M.; Giroud, N. Older adults’ neural tracking of interrupted speech is a function of task difficulty.
Neuroimage 2022, 262, 119580. [CrossRef]
69. Howard, M.F.; Poeppel, D. Discrimination of speech stimuli based on neuronal response phase patterns depends on acoustics but
not comprehension. J. Neurophysiol. 2010, 104, 2500–2511. [CrossRef]
70. Luo, H.; Poeppel, D. Phase patterns of neuronal responses reliably discriminate speech in human auditory cortex. Neuron 2007,
54, 1001–1010. [CrossRef]
71. Rosen, S. Temporal information in speech: Acoustic, auditory and linguistic aspects. Philos. T rans. R. Soc. Lond. B Biol. Sci. 1992,
336, 367–373. [CrossRef]
72. Arai, T.; Pavel, M.; Hermansky, H.; Avendano, C. Syllable intelligibility for temporally filtered LPC cepstral trajectories.J. Acoust.
Soc. Am. 1999, 105, 2783–2791. [CrossRef]
73. Drullman, R.; Festen, J.M.; Plomp, R. Effect of temporal envelope smearing on speech reception. J. Acoust. Soc. Am. 1994,
95, 1053–1064. [CrossRef]
74. Shannon, R.V .; Zeng, F.G.; Kamath, V .; Wygonski, J.; Ekelid, M. Speech recognition with primarily temporal cues.Science 1995,
270, 303–304. [CrossRef] [PubMed]
75. Di Liberto, G.M.; O’sUllivan, J.A.; Lalor, E.C. Low-Frequency Cortical Entrainment to Speech Reflects Phoneme-Level Processing.
Curr. Biol. 2015, 25, 2457–2465. [CrossRef] [PubMed]
76. Donhauser, P .W.; Baillet, S. Two Distinct Neural Timescales for Predictive Speech Processing. Neuron 2020, 105, 385–393.e9.
[CrossRef] [PubMed]
77. Decruy, L.; Vanthornhout, J.; Francart, T. Evidence for enhanced neural tracking of the speech envelope underlying age-related
speech-in-noise difficulties. J. Neurophysiol. 2019, 122, 601–615. [CrossRef]
78. Schmitt, R.; Meyer, M.; Giroud, N. Better speech-in-noise comprehension is associated with enhanced neural speech tracking in
older adults with hearing impairment. Cortex 2022, 151, 133–146. [CrossRef]
79. Brayne, C.; Calloway, P . The association of education and socioeconomic status with the Mini Mental State Examination and the
clinical diagnosis of dementia in elderly people. Age Ageing 1990, 19, 91–96. [CrossRef]
Brain Sci. 2025, 15, 874 22 of 22
80. Pliatsikas, C.; Veríssimo, J.; Babcock, L.; Pullman, M.Y.; A Glei, D.; Weinstein, M.; Goldman, N.; Ullman, M.T. Working memory in
older adults declines with age, but is modulated by sex and education. Q. J. Exp. Psychol. 2019, 72, 1308–1327. [CrossRef]
81. Weiss, B.D.; Reed, R.; Kligman, E.W.; Abyad, A. Literacy and performance on the Mini-Mental State Examination. J. Am. Geriatr.
Soc. 1995, 43, 807–810. [CrossRef] [PubMed]
82. Ylikoski, R.; Erkinjuntti, T.; Sulkava, R.; Juva, K.; Tilvis, R.; Valvanne, J. Correction for age, education and other demographic
variables in the use of the Mini Mental State Examination in Finland. Acta Neurol. Scand. 1992, 85, 391–396. [CrossRef] [PubMed]
83. Wayne, R.V .; Johnsrude, I.S. A review of causal mechanisms underlying the link between age-related hearing loss and cognitive
decline. Ageing Res. Rev. 2015, 23 Pt B, 154–166. [CrossRef] [PubMed]
84. Amichetti, N.M.; Stanley, R.S.; White, A.G.; Wingfield, A. Monitoring the capacity of working memory: Executive control and
effects of listening effort. Mem. Cognit. 2013, 41, 839–849. [CrossRef]
85. McCoy, S.L.; Tun, P .A.; Cox, L.C.; Colangelo, M.; Stewart, R.A.; Wingfield, A. Hearing loss and perceptual effort: Downstream
effects on older adults’ memory for speech.Q. J. Exp. Psychol. A 2005, 58, 22–33. [CrossRef]
86. Wingfield, A.; Tun, P .A. Cognitive supports and cognitive constraints on comprehension of spoken language.J. Am. Acad. Audiol.
2007, 18, 548–558. [CrossRef]
87. Pisoni, D.B.; Cleary, M. Measures of working memory span and verbal rehearsal speed in deaf children after cochlear implantation.
Ear Hear. 2003, 24 (Suppl. S1), 106S–120S. [CrossRef]
88. Kronenberger, W.G.; Pisoni, D.B.; Harris, M.S.; Hoen, H.M.; Xu, H.; Miyamoto, R.T. Profiles of verbal working memory growth
predict speech and language development in children with cochlear implants. J. Speech Lang. Hear. Res. 2013, 56, 805–825.
[CrossRef]
89. Watson, D.R.; Titterington, J.; Henry, A.; Toner, J.G. Auditory sensory memory and working memory processes in children with
normal hearing and cochlear implants. Audiol. Neurootol. 2007, 12, 65–76. [CrossRef]
90. Kuchinsky, S.E.; Vaden, K.I.; Keren, N.I.; Harris, K.C.; Ahlstrom, J.B.; Dubno, J.R.; Eckert, M.A. Word intelligibility and age predict
visual cortex activity during word listening. Cereb. Cortex 2012, 22, 1360–1371. [CrossRef]
91. Peelle, J.E.; Troiani, V .; Wingfield, A.; Grossman, M. Neural processing during older adults’ comprehension of spoken sentences:
Age differences in resource allocation and connectivity. Cereb. Cortex 2010, 20, 773–782. [CrossRef]
92. Baddeley, A. Working memory: Theories, models, and controversies. Annu. Rev. Psychol. 2012, 63, 1–29. [CrossRef]
93. Erönnberg, J.; Elunner, T.; Ezekveld, A.; Esörqvist, P .; Edanielsson, H.; Elyxell, B.; Edahlström, Ö.; Esignoret, C.; Estenfelt, S.;
Epichora-Fuller, M.K.; et al. The Ease of Language Understanding (ELU) model: Theoretical, empirical, and clinical advances.
Front. Syst. Neurosci. 2013, 7, 31. [CrossRef]
94. Rönnberg, J.; Holmer, E.; Rudner, M. Cognitive hearing science and ease of language understanding. Int. J. Audiol. 2019,
58, 247–261. [CrossRef]
95. Kilman, L.; Zekveld, A.; Hällgren, M.; Rönnberg, J. The influence of non-native language proficiency on speech perception
performance. Front. Psychol. 2014, 5, 651. [CrossRef] [PubMed]
96. Magimairaj, B.M.; Nagaraj, N.K.; Champlin, C.A.; Thibodeau, L.K.; Loeb, D.F.; Gillam, R.B. Speech Perception in Noise Predicts
Oral Narrative Comprehension in Children With Developmental Language Disorder. Front. Psychol. 2021, 12, 735026. [CrossRef]
[PubMed]
97. Frisina, D.R.; Frisina, R.D. Speech recognition in noise and presbycusis: Relations to possible neural mechanisms. Hear. Res. 1997,
106, 95–104. [CrossRef] [PubMed]
98. Tun, P .A.; O’2035KAne, G.; Wingfield, A. Distraction by competing speech in young and older adult listeners.Psychol. Aging 2002,
17, 453–467. [CrossRef]
99. Zekveld, A.A.; Heslenfeld, D.J.; Festen, J.M.; Schoonhoven, R. Top-down and bottom-up processes in speech comprehension.
Neuroimage 2006, 32, 1826–1836. [CrossRef]
100. Mai, G.; Howell, P . The possible role of early-stage phase-locked neural activities in speech-in-noise perception in human adults
across age and hearing loss. Hear. Res. 2023, 427, 108647. [CrossRef]
Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual
author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to
people or property resulting from any ideas, methods, instructions or products referred to in the content.
