# detection in aging populations with

**Year:** D:20

---

Evaluating cognitive decline
detection in aging populations with
single-channel EEG features based
on two studies and meta-analysis
Lior Molcho1,7, Neta B. Maimon1,2,6,7, Talya Zeimer1, Ofir Chibotero1, Sarit Rabinowicz5, Vered Armoni5, Noa Bar On5, Nathan Intrator1,3,4 & Ady Sasson5
Timely detection of cognitive decline is paramount for effective intervention, prompting researchers
to leverage EEG pattern analysis, focusing particularly on cognitive load, to establish reliable markers
for early detection and intervention. This comprehensive report presents findings from two studies
and a meta-analysis, involving a total of 237 senior participants, aimed at investigating cognitive
function in aging populations. In the first study, 80 seniors were classified into two groups: 40 healthy
individuals (MMSE > 28) and 40 at risk of cognitive impairment (MMSE 24–27). Dimensionality
reduction models, such as Lasso and Elastic Net, were employed to analyze EEG features correlated
with MMSE scores. These models achieved a sensitivity of 0.90 and a specificity of 0.57, indicating a
robust capability for detecting cognitive decline. The second study involved 77 seniors, divided into
three groups: 30 healthy individuals (MMSE > 27), 30 at risk of MCI (MMSE 24–27), and 17 with mild
dementia (MMSE < 24). Results demonstrated significant differences between MMSE groups and
cognitive load levels, particularly for Gamma band and A0, a novel machine learning biomarker used
to assess cognitive states. A meta-analysis, combining data from both studies and additional data,
included 237 senior participants and 112 young controls. Significant associations were identified
between EEG biomarkers, such as A0 activity, and cognitive assessment scores including MMSE and
MoCA, suggesting their potential as reliable indicators for timely detection of cognitive decline. EEG
patterns, particularly Gamma band activity, demonstrated promising associations with cognitive
load and cognitive decline, highlighting the value of EEG in understanding cognitive function. The
study highlights the feasibility of using a single-channel EEG device combined with advanced machine
learning models, offering a practical and accessible method for evaluating cognitive function and
identifying individuals at risk in various settings. Cognitive decline poses a significant challenge, making the implementation of timely detection methods
essential1,2. The advent of disease-modifying therapies such as Aducanumab3,4 and Lecanemab5, which target
amyloid plaques, a hallmark of Alzheimer’s Disease (AD), offers potential to alter disease progression. These
FDA-approved therapies have demonstrated efficacy primarily when administered in the initial phases of AD. Identifying subtle changes in cognitive function before significant deficits occur is paramount for maximizing
the therapeutic benefits of these drugs, ultimately aiming to preserve cognitive function and improve quality of
life in at-risk individuals6. Standard tools such as the Mini-Mental State Examination (MMSE)7 and the Montreal
Cognitive Assessment (MoCA)8, are widely used in clinical settings. Despite its widespread use, the MMSE
is criticized for limited sensitivity and susceptibility to confounding factors such as education levels, age and
socioeconomic background9,10. Research shows that this lack of sensitivity allows many patients with cognitive
impairments to go unnoticed, undermining the need for cognitive rehabilitation11. Consequently, while the
MMSE remains a valuable initial screening tool, its limitations underscore the importance of supplementing
it with additional assessments to ensure a more comprehensive evaluation of cognitive function, particularly
during the early stages of cognitive decline12.
1Neurosteer Inc, NYC, New York, USA. 2School of Psychological Sciences, Tel Aviv University, Tel Aviv, Israel.
3Blavatnik School of Computer Science, Tel-Aviv University, Tel-Aviv, Israel. 4Sagol School of Neuroscience, Tel Aviv
University, Tel Aviv, Israel. 5Dorot Geriatric Medical Center, Netanya, Israel. 6 Buchmann-Mehta School of Music, Tel
Aviv University, Tel Aviv, Israel. 7These authors contributed equally to this work: Lior Molcho and Neta B. Maimon.
email: lior@neurosteer.com
OPEN
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports

In this regard, biomarkers derived from cerebrospinal fluid (CSF) and blood offer complementary diagnostic
perspectives, providing a window into the molecular changes occurring in the brain. Their levels can reflect
distinct stages of neurodegeneration, allowing clinicians and researchers to assess disease progression and stratify
patients for targeted interventions13. Beta-amyloid (Aβ), for instance, is a pivotal biomarker in AD research. Advances in assay technologies have recently facilitated the detection of Aβ biomarkers in blood, addressing
challenges such as low concentrations and interference from peripheral sources. The CSF Aβ42/Aβ40 ratio
is widely regarded as the gold standard for identifying amyloid pathology. Furthermore, emerging studies on
plasma biomarkers for AD have demonstrated their potential to differentiate AD from other neurodegenerative
disorders, predict the onset of AD dementia in its early stages, and provide valuable insights into disease
progression13,14. While CSF and blood biomarkers offer valuable insights for understanding disease pathology, they are
often invasive, resource-intensive, and less suited for capturing dynamic brain activity during cognitive tasks. Electroencephalography (EEG) provides a non-invasive window into real-time cognitive processes, offering
insights into the neurophysiological disruptions associated with cognitive decline. This approach complements
molecular biomarkers by bridging the gap between disease pathology and functional brain dynamics, enabling
a more comprehensive evaluation of cognitive health. EEG is effectively identifying changes in power spectral
density, disruptions in functional connectivity, and altered coherence patterns associated with cognitive
decline and AD15,16. These disruptions in neural processing and connectivity underscore the complexity of
neurophysiological changes linked to declining cognitive functions17. Previous research has extensively explored
the impact of cognitive load on various frequency bands, particularly within the frontal lobe. Frontal Theta
activity, for example, increases with the growing demands on memory retention across various cognitive tasks
like the n-back18–20. Diminished Theta power has been observed in individuals with mild cognitive impairment
(MCI) and AD during auditory and visual oddball tasks compared to healthy controls21. Similarly, Delta activity
has been shown to play a role in inhibiting potential interferences that may affect performance in high-load
cognitive tasks22, while diminished Delta power has been observed in MCI and AD patients during oddball
tasks23. Gamma waves, associated with prefrontal cortex activation during cognitive processing, exhibit positive
correlations with the fMRI-BOLD signal in frontal regions24. In middle-aged adults, heightened frontal Gamma
activity was observed during the high cognitive load level of verbal n-back task compared to younger adults,
suggesting age-related modulation of Gamma oscillations25. However, reduced Gamma oscillations in elderly
individuals (mean age 75) indicate that Gamma activity may increase until midlife and starts to decline in older
age26. Research shows cognitive decline often involves reduced amplitude and synchronization of Gamma wave
activity27. AD patients demonstrate elevated Gamma activity during performance of cognitive tasks, potentially
reflecting increased resource allocation under cognitive load compared to healthy seniors28. Beta waves, linked
to cognitive processes such as working memory maintenance and information inhibition, have also shown
correlations with fMRI-BOLD signals in the prefrontal cortex and exhibited a positive load effect specifically
during cognitive working memory tasks24. In the prefrontal cortex, heightened Beta activity aids in processes like
information erasure from working memory and preserves contents during delay periods29. Furthermore, while
behavioral performance was similar between young and healthy elderly participants in an auditory memory
task study, notable differences in Beta band desynchronization during retrieval suggest age-related influences
on Beta responses during working memory task30. Notably, Beta power was higher in MCI patients compared
to controls, both at rest and during working memory tasks31. Understanding how cognitive load influences
frequency bands in the frontal lobe contributes valuable insights into the neural mechanisms underlying
cognitive processes and can shed light on cognitive decline. Building on these insights, EEG biomarkers enable
clinicians to monitor activity in real time, capturing dynamic changes across various tasks and functions. This
facilitates a deeper understanding of patient challenges, which can also be correlated with self-reported data. Furthermore, EEG’s non-invasive nature, high accuracy, and straightforward interpretability enhance its utility
in clinical settings, providing objective, quantifiable data to identify abnormal brain patterns and support timely
diagnosis and intervention for individuals at risk32. Advancements in device design and analytical approaches
have further improved the accessibility and clinical relevance of EEG biomarkers. The present study highlights
the development of novel biomarkers derived from a single-channel EEG to effectively assess cognitive states. Single-channel EEG retains the key advantages of multichannel systems—being non-invasive, cost-effective,
and portable—while offering additional benefits, such as forehead placement, which eliminates the need for a
full cap, enhancing comfort and simplifying the setup for participants and clinicians. This streamlined approach
supports more frequent recordings and may be particularly suitable for elderly individuals and clinical settings,
reducing the need for hospital visits. Notably, single-channel EEG achieves these benefits without compromising
data quality33. In recent years, machine learning (ML) and deep learning (DL) approaches have been increasingly applied to
EEG data to predict early cognitive decline, yielding high accuracy results. A review analyzing 209 studies found
that DL models, particularly convolutional neural networks (CNNs) and support vector machines (SVMs), can
achieve accuracies exceeding 93% in distinguishing between cognitive decline stages34. Another review of 116
studies on the progression from MCI to AD reported that ML techniques, including SVMs, random forests,
and CNNs, delivered classification accuracies up to 95% and AUC values of 0.98 for EEG-based predictions35. Additionally, ensemble methods and feature selection techniques like Lasso and ElasticNet were frequently used
to enhance model performance36. While these results show potential, the effectiveness of ML and DL techniques
applied to EEG data is often limited by small sample sizes, impacting generalizability and increasing the risk
of overfitting. Studies with larger EEG cohorts have demonstrated the potential of these approaches to detect
cognitive deficits, enhancing their applicability to broader populations and widespread use in clinical settings. For instance, a study involving frontotemporal EEG data from 120 participants showed that EEG multifractal
analysis, combined with ML models, effectively detected MCI in healthy individuals, correlating well with
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

normal MMSE scores (≥ 26)37. Another study analyzed resting-state prefrontal EEG biomarkers from 496 elderly
individuals and used various ML methods (including WLS, Ridge, ElasticNet and Lasso) to predict cognitive
impairment. These models achieved moderate AUC (0.84) and accuracy (0.75), effectively differentiating
between individuals at risk of MCI and those with cognitive deficits38. These findings underscore the potential of
advanced ML and DL methods for accurate, non-invasive early diagnosis of cognitive decline. This study includes pre-extracted EEG features, identified as significant markers of cognitive function,
validated in prior research conducted on diverse populations, including young, healthy subjects39–41, and elderly
experiencing various cognitive states42,43. These features were utilized in our pilot study and are further applied in
the current studies to assess their effectiveness in detecting cognitive decline. Our previous pilot study44 included
50 seniors with MMSE scores ranging from 10 to 30, divided into three groups: healthy individuals (MMSE > 27),
individuals at risk of MCI (MCI-R, MMSE 24–27), and individuals with mild dementia (MD, MMSE < 24). EEG
data was collected during an auditory cognitive assessment with varying cognitive load levels and at rest. Pre-
extracted EEG features showed significant correlations with MMSE scores, particularly ST4 and A0, across task
difficulty levels. Furthermore, these features effectively distinguished between seniors with high vs. low MMSE
scores. EEG features Theta, Delta, A0, and VC9 increased with higher cognitive load levels, indicating different
activity patterns between young and senior participants in different cognitive states, particularly notable for
VC9, which differentiated between all levels of cognitive load. This pilot study demonstrated that single-channel
wearable EEG and ML features can effectively evaluate cognitive states and align with clinical measurements for
detecting cognitive decline. The recent FDA approval of drugs designed to slow beta amyloid buildup in AD, results in seniors increasingly
seeking evaluations for eligibility for these new treatments, placing a substantial burden on clinicians. This
situation intensified the demand for highly specific AI-based assessments that can accurately distinguish between
healthy individuals and those who may need further evaluation. Motivated by this need, the first study presented
here focuses on the high range of MMSE scores (24–30, typically considered healthy), aiming to distinguish
between cognitively healthy individuals and those who may be at risk for early cognitive decline, with a cutoff
score of 27. The goal was to identify subtle cognitive changes that may signal the onset of decline among elderly
individuals using EEG biomarkers. To enhance the rigor of the study, participants underwent two EEG recording
sessions conducted on separate days within a seven-day period. This dual-session design was implemented to
test the reliability and consistency of the EEG data across sessions for each participant, as well as to examine the
effects of learning and adaptation over time compared to stable neural patterns observable in both sessions. We
hypothesized that EEG biomarkers can distinguish between cognitively healthy individuals and those at risk for
early cognitive decline with MMSE scores in the high range (24–30). The second study aims to validate the outcomes of the pilot study by incorporating additional clinical
diagnostic tools, such as MoCA. While MMSE is a reliable tool, its sensitivity can be limited by educational
level variations. A review of over 50 studies indicates that MoCA exhibits greater sensitivity than MMSE in
detecting subtle early-stage MCI deficits45. Additionally, previous work demonstrated that a single-channel EEG
approach successfully extracted features comparable to MoCA scores46. To further enhance the clinical aspect of
our assessment, we introduced functional tasks in the second study protocol. Two tasks from the Performance
Assessment of Self-Care Skills (PASS), which evaluates functional status and change47. A study found significant
associations between PASS tasks focusing on cognitive skills and performance in verbal memory and executive
function, effectively differentiating MCI subjects from healthy controls48. We hypothesized that a combined
approach using single-channel EEG, MMSE, and MoCA scores will provide a more accurate assessment of early
cognitive decline, particularly in individuals who are at risk for MCI. Finally, we conducted a meta-analysis of data gathered in all three studies, including additional healthy
controls (n = 349), to achieve a comprehensive perspective on the relationships between EEG features, cognitive
assessments, and functional tasks in the elderly population. Methods
Participants
The first study recruited 80 patients from the inpatient rehabilitation department at Dorot Geriatric Medical
Center, with a mean age of 73.51 (SD: 10.45) years, evenly distributed between males and females. Both groups
exhibited a diverse age range. An age difference was observed between the healthy male group and the MCI-R
male group. This difference is primarily attributed to the presence of a male participant in the MCI-R group,
whose age (101 years) is more than two standard deviations above the group average. When this outlier is
excluded from the analysis, the age difference between the male subjects is no longer significant (t = -1.86,
p = 0.07). Other than that, no significant age differences were found between the groups. The second study included 77 patients from the same department, with a mean age of 74.17 (SD: 8.90)
years, comprising 52% females and 48% males. Each group displayed a wide age range. Differences in age were
observed between the MD group and the other two groups (MCI-R and Healthy), particularly among female
participants. Full demographic details are provided in Tables 1 and 2. In both studies, clinical staff identified potential participants during hospital admissions. Participants were
selected based on study inclusion criteria and had MMSE scores of 24–30 (first study), or 10–30 (second study). For the meta-analysis, a total of 112 healthy participants with mean age of 37.6 (SD: 15.4) years, comprising
62% females and 38% males were recruited. They completed auditory cognitive tasks similar to the study groups. All participants included in this paper provided informed consent in line with the Declaration of Helsinki. Individuals who objected or had neurological comorbidities, scalp or skull damage, facial skin irritation,
significant hearing impairments, or a history of significant drug abuse were excluded. Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

Ethics approval, accordance statement and informed consent
This study was conducted in accordance with the Declaration of Helsinki and relevant institutional and national
regulations. Ethical approval was granted by the Ethics Committee (EC) of Dorot Geriatric Medical Center. The
first study received approval on September 07, 2020 (NIH Clinical Trials Registry number: NCT04683835), and
the second study received approval on March 01, 2022 (NIH Clinical Trials Registry number: NCT05528445). Ethical approval for healthy participants included in the meta-analysis was obtained from Tel Aviv University. All participants provided informed consent before their inclusion in the study. Study groups
Figure 1 illustrates the group allocation and analysis details for each part of the study. In the first study, participants were divided into two groups based on their MMSE scores: Healthy group
(MMSE scores of 28–30, n = 40); and MCI-R group (MMSE scores of 24–27, n = 40); Groups
Healthy (MMSE ≥ 28)

## MCI -R

## (MMSE 24–27)

## MD (MMSE < 24)

Total
MMSE scores
28–30
24–27
10–23
n

MMSE
28.76 (0.71)
25.51 (1.15)
20.22 (2.21)
Age
73.3 (6.5)
72.05 (10.37)
79.68 (7.46)
Age t-tests
Healthy vs. MCI-R
t = 0.57, p = 0.57
Healthy vs. MD
t=-3.02, p = 0.005
MCI -R vs. MD
t=-2.99, p = 0.004
MoCA scores
23.53 (2.56)
19.34 (3.58)
12.96 (4.47)
Male
n

MMSE
28.76 (0.73)
25.86 (1.19)
20.04 (1.97)
Age
74 (7.85)
71.32 (10.94)
76 (8.76)
Age t-tests
Healthy vs. MCI -R
t = 0.78, p = 0.43
Healthy vs. MD
t=-0.45, p = 0.65
MCI -R vs. MD
t=-0.98, p = 0.34
Female
n

MMSE
28.76 (0.69)
25.19 (1.01)
20.31 (2.34)
Age
72.38 (4.11)
72.69 (9.82)
81.84 (5.56)
Age t-tests
Healthy vs. MCI-R
t = 0.13, p = 0.89
Healthy vs. MD
t=-4.63, p = 0.0002
MCI -R vs. MD
t=-3.09, p = 0.004
Age males vs. females
t = 0.70, p = 0.48
t=-0.40, p = 0.68
t=-1.46, p = 0.18
Table 2. Demographic information for the second study groups, including mean ages, Mini-Mental state
examination (MMSE) scores, and Montreal cognitive assessment (MoCA) scores for total participants, as well
as for males and females separately (SDs presented in brackets). The table provides t and p values comparing
mean ages between healthy, MCI-R, and MD groups, both overall and by gender. The final row presents t and p
values comparing ages between genders. Groups
Healthy (MMSE ≥ 28)

## MCI -R (MMSE 24–27)

Total
n

MMSE
29.03 (0.8)
25.34 (1.02)
Age
72.23 (9.63)
75.89 (10.66)
Age t-test
Healthy vs. MCI-R t=-1.76, p = 0.08
Male
n

MMSE
29.08 (0.82)
25.59 (1.08)
Age
69.01 (6.4)
75.64 (11.5)
Age t-test
Healthy vs. MCI -R t=-2.15, p = 0.03
Female
n

MMSE
29 (0.79)
25.07 (0.87)
Age
74.54 (10.83)
76.16 (9.61)
Age t-test
Healthy vs. MCI -R t=-0.7, p = 0.48
Age males vs. females
t=-1.81, p = 0.07
t=-0.39, p = 0.69
Table 1. Demographic information for the first study groups, including mean ages and Mini-Mental state
examination (MMSE) scores for total participants, and separately for males and females (SDs presented in
brackets). The table also includes t and p values comparing mean ages between healthy and MCI-R groups,
both overall and by gender. Additionally, t and p values comparing ages between genders are shown in the final
row. Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

In the second study, participants were divided into three groups based on their MMSE scores: Healthy group
(MMSE scores of 28–30, n = 30); and MCI-R group (MMSE scores of 24–27, n = 30); mild dementia (MD) group
(MMSE scores of 10–23, n = 17). We used MMSE score cutoffs of 24 and 27 for group allocation, focusing on timely detection of cognitive
decline. Previous evidence suggests that a higher cutoff score enhances diagnostic accuracy49. Additionally,
research indicates that educated individuals scoring below 27 on the MMSE are at increased risk of developing
dementia50. Finally, the meta-analysis included data from both studies and additional healthy participants, totaling 237
elderly individuals (allocated as in the second study) and 112 healthy young participants. Clinical and demographic data
To enhance the validation of clinical assessments and cognitive states of participants, additional evaluations
were conducted alongside the MMSE in both studies. In the first study, participants underwent Instrumental
Activities of Daily Living (IADL)51 assessments, which measures daily living tasks across eight domains, with
scores ranging from 0 (low functioning) to 23 (high functioning). The IADL is self-reported and assessed
through interviews and has seldom been linked to objective measures like brain activity. However, a study using
single-channel EEG effectively classified elderly subjects based on IADL scores52. In the second study, several clinical assessment methods were collected including the Montreal Cognitive
Assessment (MoCA)8, the Geriatric Depression Scale (GDS)53 for depression diagnosis, and the Executive Clock
Drawing Task (CLOX)54 for assessing cognitive impairment. Additionally, demographic and sleep-related data
were collected in the second study (see full details in Supplementary Material Table S17). Designed for the detection of MCI or early Dementia by healthcare professionals, the MoCA evaluates various
cognitive domains including visuospatial abilities, memory, attention, and delayed recall55. The interpretation
of scores, including the threshold for normal cognitive function (commonly 26 or higher), should consider
adjustments based on the individual’s years of education and age56. The GDS, designed for elderly individuals,
consists of “yes” or “no” questions about the past week’s emotional experiences, scores from 0 to 15, with higher
scores indicating more severe depression57. The CLOX task, involving drawing and replicating a clock, scores
from 0 to 15, with lower scores indicating greater cognitive impairment54. EEG recording and auditory battery
EEG recording followed the previously described protocols43,44, and was conducted in a quiet, well-lit room. A research assistant prepared the sanitized Neurosteer EEG equipment, including the disposable electrode
patch, sensor, EEG monitor, and clicker. After the electrode patch was attached to the participant’s forehead, the
recording commenced. Participants remained seated throughout the session, receiving auditory instructions
through a speaker linked to the EEG monitor. The session lasted approximately 30 min, including a brief baseline
activity recording to ensure accurate evaluation. This battery consisted of pre-recorded tasks: musical detection, musical n-back, and resting state tasks
as outlined in prior studies43,44. Initial instructions were provided to minimize further guidance and reduce
Fig. 1. Study design with group allocation and analytical approach at each step. Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

potential bias. The detection task comprised a sequence of melodies performed by a violin, trumpet, and flute. Participants used a clicker to respond to auditory cues based on specific instructions provided at the beginning
of each block. The task included two levels of difficulty to examine escalating cognitive demands. In Level 1,
melodies lasted 3 s and repeated throughout the block. Participants clicked the button for each repetition of the
melody, with three 90-second trials (one per instrument). Each melody appeared 5–6 times, interspersed with
10–18 s of silence. In Level 2, melodies were shortened to 1.5 s, and all three instruments were intermixed within
a single block. Participants clicked only for the specified instrument, ignoring others. Each trial included 6–8
melodies, with 8–14 s of silence between them, and the target melody appeared 2–3 times. The n-back task further tested cognitive load with three levels of difficulty (0-back, 1-back and 2-back). Participants were presented with a sequence of melodies played by different instruments and instructed to
respond using the clicker. In the 0-back condition, participants clicked the button each time a melody was
played, with one 90-second block consisting of nine trials, where each melody lasted 1.5 s and was followed by
6–11 s of silence. In the 1-back condition, participants clicked the button each time a melody repeated itself
(n = 1). This condition consisted of two 90-second blocks, with 12–14 trials per block. Melodies lasted 1.5 s,
followed by 4–6 s of silence. Approximately 30–40% of trials in this condition included target stimuli, where
the melody repeated. In the 2-back condition, participants were asked to click the button each time a melody
repeated itself two steps apart (n = 2). A 45-second block consisting of 12 trials was played, with melodies of 1.5
seconds, followed by 4–6 seconds of silence. Approximately 25% of trials in this condition included target stimuli
(where the melody that was played two steps ago repeated). Resting state tasks were interspersed within the auditory battery to provide baseline measurements. The first
resting state task occurred between the detection and n-back tasks, during which participants were instructed
to keep their eyes open and think of positive autobiographical thoughts for 45 s. The second resting state task
followed the auditory assessment, where participants closed their eyes and allowed their minds to wander for
60 s. In the first study, participants underwent two EEG recording sessions with different randomizations of the
auditory battery trials. Each patient was re-examined under the same conditions over the next seven days, with
sessions at least one day apart. In the second study, participants completed two additional C-IADL51 sub-tasks from PASS: telephone use
and medication management. Each task is rated on a 4-point scale (0–3), and patients receive three types of
scores: independence, safety, and adequacy (quality)47. EEG device
EEG data were collected using the high dynamic range Neurosteer® Recorder (hdrEEG), which employs a single-
channel setup. Each participant was fitted with a three-electrode patch placed on the forehead, utilizing dry gel
to ensure good signal transmission. The non-invasive electrodes were arranged in the prefrontal cortex, with
the single channel of EEG obtained from the differential signal between electrodes at Fp1 and Fp2, according to
the International 10/20 system, and a reference electrode at Fpz. The recordings were digitized at a continuous
sampling rate of 500 Hz. Power spectrum and frequency bands
The EEG power spectrum was obtained through the fast Fourier transform (FFT) of the EEG signals within a
4-second window, using a Hamming window to minimize spectral leakage. Power spectral density was calculated
from the frontal channel (Fp1-Fp2) and transformed to dB (logarithm base 10), to reflect log-transformed
absolute power (in µV²/Hz). Delta (0.5–4 Hz), Theta (4–7 Hz), Alpha (8–15 Hz), Beta (16–31 Hz), and lower
Gamma (32–45 Hz) frequency bands were included in the analysis. The frequency band ranges employed in the
present study fall within established conventions in EEG analysis58,59. Signal processing and EEG features
In recent years, a time-frequency approach has been adopted for analyzing EEG data to characterize brain states
in AD60,61. In line with this approach, our study employs an advanced time-frequency method to process the EEG
signal, as previously described40,43,44. The EEG features are produced by a secondary layer of machine learning
applied to labeled datasets previously gathered by Neurosteer, to derive several linear combinations. Specifically,
the EEG features VC9 and A0 were calculated employing the linear discriminant analysis (LDA) technique62. LDA is designed to identify an optimal linear transformation that maximizes class separability. Previous studies
employing LDA models on imaging data have demonstrated success in predicting the development of cognitive
decline. Simple LDA models using MRI and PET data were shown to predict cognitive decline or stability up
to four years prior to the manifestation of decline symptoms63. The calculation of EEG feature ST4 utilized
principal component analysis (PCA)64, a technique employed for reducing feature dimensionality before
classification. Research indicates that features extracted through PCA exhibit a significant correlation with
MMSE scores and effectively distinguish individuals with AD from healthy subjects65–67. Notably, all three EEG
features were derived from datasets different from those analyzed in the current study, to avoid overfitting the
data. Consequently, the weight matrices previously determined were applied to transform the data acquired in
the present study. In studies conducted on young healthy participants, VC9 feature showed increased activity with escalating
levels of cognitive load manipulated by a numeric n-back task39. Furthermore, during an arithmetic task, VC9 activity decreased in response to external visual interruptions41. Additionally, in a surgery simulator
task performed by medical interns, VC9 activity declined with task repetition, correlating with individual
performance40. VC9 demonstrated greater sensitivity than Theta particularly for tasks with lower cognitive load,
making it more suitable for clinical and elderly populations. Notably, in the preceding pilot study44, higher
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

cognitive load levels resulted in increased VC9 activity exclusively in the healthy young group compared to
the healthy senior group, highlighting different activity patterns between young and senior participants across
various cognitive states. In clinical settings, VC9 activity correlated with the auditory mismatch negativity
(MMN) component in minimally responsive patients68. EEG feature A0, previously identified as a classifier for distinguishing cognitive load from rest in healthy
subjects, has proven to be a robust predictor of cognitive decline in individuals with mild-to-moderate
impairment44. Furthermore, A0 effectively differentiates between healthy controls and Parkinson’s disease (PD)
patients, with higher activity observed in healthy individuals43. EEG feature ST4 was found to correlate with individual performance in the numeric n-back task, specifically
correlating the disparity in RTs between high and low cognitive load levels to differences in ST4 activity per
participant39. In the preceding pilot study44, ST4 demonstrated the ability to differentiate between individuals
with low MMSE scores, those with scores between 24 and 27, and those with scores above 28, as well as healthy
young participants. This suggests that ST4 can detect subtle changes in cognitive states, indicating its potential
as a sensitive marker of cognitive functioning. Statistical analysis
Overview
The statistical analysis was conducted separately for the first and second studies, followed by a meta-analysis
incorporating data from a total of 349 participants from both studies and previously collected data. In the first study, the analysis began with dimensionality reduction using Lasso, Elastic Net, Ridge, and SVM
with RBF kernel models to identify key features correlated with MMSE scores. This was followed by Linear
Mixed Model (LMM) analyses, typically used when the dependent variable is continuous, and when there are
repeated measurements for the same subject. In the current study, we used LMMs to assess the relationships
between EEG variables, MMSE groups, and cognitive load levels with the following variables: MMSE group
(numeric, between), visit (categorical, within), and cognitive load level (numeric, within). Separate LMMs were
then conducted for each visit, considering MMSE group and cognitive load. In the second study, LMM analyses incorporated the MMSE group (numeric, between) and cognitive load
level (numeric, within) variables. Additionally, correlation models were employed to examine the associations
between EEG variables and clinical test scores. Logistic regression models were applied to predict both MMSE
and MoCA results based on brain activity features and collected clinical data (e.g., CLOX, GDS, and PASS
scales). Logistic regression was chosen for its ability to model the relationship between predictors and outcomes
in a probabilistic framework, providing interpretable insights into how different features influence prediction. The significance level for all analyses was set at p < 0.05. Post-hoc effects with Benjamini-Hochberg
correction69 were applied following significant main effects and interactions. All analyses were carried out using
Python Statsmodel70. Variables
These studies included EEG variables, performance data, and clinical scales. EEG variables comprised frequency
bands: Delta, Theta, Alpha, Beta and lower Gamma, as well as three EEG features: VC9, ST4, and A0 (normalized
to a scale of 0-100). All EEG variables were calculated every second using a moving window of four seconds,
and mean activity per condition was analyzed. Behavioral variables included mean response accuracy and mean
RTs per participant. The independent variable representing cognitive load was constructed as follows: tasks
performed during resting state; Detection task level 1 and 0-back were categorized as cog_load 1; Detection task
level 2 and 1-back were categorized as cog_load 2. Finally, 2-back was categorized as cog_load 3. Results
Demographic and clinical results
To ensure proper adjustment for age and gender, mean ages were compared within each MMSE group using the
Welch Two Sample t-test, both overall and separately by gender (see Tables 1 and 2 for detailed results). In the first study, a significant positive correlation between MMSE and IADL scores was observed (r = 0.26,
p = 0.03), as expected based on previous literature71,72. Significant correlations were also found between MMSE
and IADL scores and A0 biomarker activity during both cognitive and resting tasks (detection task: r = -0.25,
p = 0.04; n-back task: r = -0.29, p = 0.02; and resting state tasks: r = -0.39, p = 0.003), suggesting that higher A0
activity might be associated with greater cognitive decline, as indicated by lower IADL and MMSE scores. The second study included additional demographic and clinical data (see full details in Supplementary
Material table S17). No significant differences in education level, years of employment, average sleep hours,
sleep quality, or tiredness were found between groups (MD, MCI-R, and Healthy, p > 0.05). MoCA scores showed
significant differences between all groups (all ps < 0.05, see Table 2). First study results
The first study aimed to detect early cognitive decline in healthy seniors. Initially, dimensionality reduction
techniques (Lasso, Elastic Net, Ridge, and SVM with RBF kernel) were used to identify features correlated with
MMSE scores. Subsequently, linear mixed models (LMM) were employed to examine relationships between
EEG variables, MMSE groups, and cognitive load levels. Dimensionality reduction
To identify a combination of features that would result in the highest correlation with MMSE scores, mean feature
activity as well as reaction times (RTs), and accuracy were calculated for each auditory task per participant. Since
the focus was on detection of timely cognitive decline in the healthy elderly population (typically associated with
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

MMSE > 24), the aim was to differentiate between healthy individuals (MMSE > 27) and those at risk for MCI
(MMSE between 24 and 27). Multiple linear predictors and one nonlinear predictor were tested, including ridge, Lasso, and Elastic
regression, linear kernel RBF, and SVM with RBF kernel. Lasso and Elastic Net yielded slightly better results than
ridge regression, indicating the usefulness of both L1 and L2 penalties in feature selection. We set the number
of features to analyze at 30, based on individual R2 values. The data was then analyzed using cross-validated
binary prediction of MMSE scores. Each cross-validation group produced an ensemble average over multiple
regularization parameters to improve reliability73. The average R2 was 0.31, corresponding to an r > 0.55. See
Table 3 for results from four models. These results indicate that our approach effectively predicts cognitive performance as measured by MMSE
scores, achieving a good balance between sensitivity and specificity. Specifically, Lasso and ElasticNet models
achieved the highest sensitivity (0.90), indicating excellent detection of true positives. Both Lasso and ElasticNet
models yielded the highest F1 score (0.77), indicating a strong balance between precision and sensitivity. Elastic
Net achieved the highest AUC (0.74) with Lasso closely following (0.73), demonstrating superior overall ability
to distinguish between classes. Figure 2 illustrates the predictions of these two models, showing a correlation of
r = 0.38 and r = 0.35, with lower variability in the higher MMSE scores (27–30). Linear mixed model (LMM) results
For the complete LMM results of all studies, including standard deviations, p- and z-values, refer to
Supplementary Material Sect.  3. This study involved two recording sessions across consecutive visits, each
featuring a comparable auditory battery with tasks of varying cognitive load. The initial LMM analysis included
data from both visits, with MMSE score (numeric, between-subjects), visit (categorical, within-subjects), and
cognitive load (numeric, within-subjects) as variables. No significant main effects or interactions were found for
any of the features analyzed. Consequently, further analyses were conducted for each visit separately. Analysis of the first visit data revealed no main effects between the groups. However, significant interactions
between group and cognitive load were found for VC9, ST4, and Theta, with the healthy group showing higher
activity at higher cognitive loads: cognitive load 2 vs. rest for VC9 (p = 0.014), ST4 (p = 0.016), and Theta
(p = 0.028); and cognitive load 1 vs. rest for VC9 (p = 0.016) and ST4 (p = 0.018). No differences in cognitive load
were detected in the MCI-R group. In the second visit, A0 showed a significant main effect of group, with higher activity in the MCI-R group
compared to the healthy group (p = 0.033). Additionally, VC9, Theta, Delta, Alpha, and Beta exhibited significant
main effects of cognitive load (all ps < 0.001), with similar cognitive load effects observed across both groups (see
Fig. 3 and Supplementary Material Sect. 3.1.2). Fig. 2. Prediction of Lasso model (left) and ElasticNet model (right), of Mini-Mental State Examination
(MMSE) scores. The red trend line indicates a positive correlation. Shaded areas highlight clusters of higher
MMSE scores (27–30) with corresponding higher predicted values and lower variability. Model
Sensitivity
Specificity
Precision
F1 Score
AUC
Lasso
0.90 (0.02)
0.57 (0.022)
0.67 (0.012)
0.77 (0.012)
0.73 (0.014)
Elastic
0.90 (0.015)
0.58 (0.011)
0.68 (0.007)
0.77 (0.009)
0.74 (0.01)
LinRBF
0.86 (0.013)
0.60 (0)
0.68 (0.003)
0.76 (0.007)
0.73 (0.007)
Ridge
0.73 (0.024)
0.57 (0.012)
0.63 (0.012)
0.68 (0.016)
0.65 (0.015)
Table 3. Performance metrics for four predictive models used to detect early cognitive decline in healthy
elderly population. SDs are presented in parentheses. Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

Inter-patient variability results
Refer to supplementary material Sect. 2 for the full details and results. Testing reliability between the two visits
for all EEG features and frequency bands revealed moderate to excellent reliability (ICCs 0.5–0.8) for the n-back
task, and moderate to good reliability (ICCs 0.5–0.75) for the detection task. Findings from Pearson correlations
revealed significant correlations between the two visits across both detection and n-back tasks for all EEG features
and frequency bands (all p-values < 0.01). In summary, the low within-patient variability observed between the
two visits in the first study enhances the validity of our measurement method. Second study results
The second study included a single recording session with cognitive assessments involving musical tasks of
varying cognitive loads. To gain a deeper insight into participants’ clinical status, additional clinical information
and measurements were collected. Correlation with clinical measures
Pearson correlations were calculated between each EEG feature per cognitive load, and the MMSE score and
the MoCA score (full correlation results are provided in Supplementary Material Table S18). A0 and Gamma
demonstrated strong correlations with MMSE scores across all tasks, and with the MoCA scores for most tasks
(see Fig. 4). Fig. 3. Mean values per participant for A0, VC9, Theta, and Delta during visit 1 (left) and visit 2 (right)
in Healthy and MCI-R groups, across different cognitive load levels: resting state (purple), cognitive load
level 1 (red), and cognitive load level 2 (green). Asterisks denote significant effects (*p < 0.05, **p < 0.01 and
***p < 0.001). Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

Linear mixed model (LMM) results
In the LMM model with group (3 levels, categorical, between), and cognitive load (3 levels, categorical, within)
variables, A0, Gamma and Beta exhibited significant differences between the groups (see Fig. 5 for individual
means of A0 and Gamma per group and cognitive load). Post-hoc analyses showed that the difference between
Healthy and MD groups was significant for A0 (padj = 0.017) and Beta (padj = 0.002). For Gamma, the difference
between Healthy and MD groups (padj = 0.001), as well as MCI-R and MD groups (padj = 0.0431) showed
significance. The main effect for cognitive load was significant for A0, VC9, Delta, Theta, Beta and Gamma. Post-hoc
analysis revealed that for most features, the differences between cognitive load levels were highly significant for
the Healthy and MCI-R groups, but not significant for the MD group (see Supplementary Material Table S21). Logistic regression model results
To incorporate the clinical data gathered in the second study, logistic regression models were created to predict
the MMSE scores based on EEG features and clinical data. This approach contrasts with the linear regression
models used in the first analysis, which focused on healthy participants (with MMSE > 24), aiming to identify
early signs of cognitive decline. The logistic regression approach here provides a broader understanding of
cognitive impairment across a wider spectrum of MMSE scores (18–30) with multiple clinical measures included. Two linear regression analyses were conducted to identify significant predictors of MMSE score. Both
regressions included potential predictors from EEG features (i.e., A0, ST4, VC9, and Delta, Beta and Gamma),
demographic factors (i.e., age, gender, years of education), cognitive task performance (i.e., accuracy, response
time), and clinical measures (i.e., CLOX, GDS, and PASS scales). In the first regression, we tested all predictors
across the different cognitive load levels, and the second regression was repeated for each cognitive load level. All
Fig. 4. A0 (left) and Gamma (right) correlations to Mini-Mental State Examination (MMSE) score (top panel)
and Montreal Cognitive Assessment (MoCA) scores (bottom panel), as a function of cognitive load level: low
(red), medium (blue), high (green), and resting state (purple). Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

regressions were created with a backward elimination process, first inserting all variables and then sequentially
removing the non-significant variables based on their p-values (> 0.05). After backward elimination, the final
first model predicting MMSE score across cognitive load levels, had an R2 value of 0.988, with three significant
predictors: A0 (p = 0.009), Gamma (p < 0.001), and accuracy (p < 0.001). For the full results and figures, see
Supplementary Material Sect. 3.2.4. To identify the factors influencing cognitive load, a series of regression models were constructed for each
cognitive load level, using the same methods as the first regression. For the highest level of cognitive load level
(i.e., brain activity during 2-back), seven significant predictors were retained: A0 (p < 0.001), Gamma (p < 0.001), ST4 (p = 0.046), CLOX (p = 0.015), PASS - drugs safety (p < 0.001), years of employment (p = 0.011), and tiredness
(p = 0.019). For the mid-high cognitive load level (i.e., detection level 2 and the 1-back), the significant predictors
included A0 (p = 0.001), Beta (p < 0.001), CLOX (p = 0.003), age (p = 0.04), PASS - drugs safety (p < 0.001), marital
status (p = 0.002), years of employment (p < 0.001), living arrangements (p = 0.011), and tiredness (p = 0.004). In the low cognitive load level (i.e., 0-back and detection level 1), the significant variables were: A0 (p < 0.001), ST4 (p = 0.026), Beta (p < 0.001), PASS - drugs quality (p = 0.024), PASS - drugs safety (p < 0.001), marital status
(p = 0.002), years of employment (p = 0.009), living arrangements (p = 0.020), tiredness (p = 0.018), and accuracy
(p = 0.003). Interestingly, the resting state model, the variables who were found significant were the EEG features
of VC9 (p < 0.001) and Theta (p < 0.001), and CLOX (p = 0.002), PASS - drugs safety (p = 0.003), marital status
(p = 0.002), years of employment (p = 0.001), living arrangements (p = 0.000), tiredness (p = 0.018), and accuracy
(p = 0.003) as clinical variables. In conclusion, while each cognitive load level displayed a distinct set of significant predictors, there were
shared factors such as A0 and years of employment consistently identified across models as significant. Conversely, certain variables like Gamma played a crucial role in specific cognitive load levels but did not
demonstrate universal applicability across all levels. Fig. 5. The mean activity per participant in the second study for A0 (top), and Gamma (bottom), in healthy
participants, MCI-R, and MD groups, as a function of cognitive load level: resting state (blue), cognitive load
level 1 (red), cognitive load level 2 (green), and cognitive load level 3 (purple). Asterisks denote significant
effects (*p < 0.05, **p < 0.01 and ***p < 0.001). Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

Meta analysis
In the final stage of our analysis, we combined the data from both studies with previously collected data44
that included seniors with different MMSE scores and a cohort of healthy young participants. This integration
enabled a thorough meta-analysis, incorporating a total of 237 elderly individuals (categorized as healthy seniors
n = 121, MCI-R n = 84, and MD n = 32), along with healthy young controls (n = 112). All participants completed
similar tasks with the same levels of cognitive load, allowing for analysis of differences in mean brain activity
between groups and across cognitive load levels, and their interactions. The population distributions of mean
A0 activity levels during both rest and cognitive resource allocation were also computed and are provided in
Supplementary Material figures S2 and S3. Initially, our focus was directed toward the elderly population (senior participants who underwent MMSE
evaluation, n = 203). Pearson correlations were calculated for each EEG feature, MMSE score and cognitive load
level. A0 exhibited a significant correlation with MMSE score (r = -0.25, p < 0.001), which remained significant
across all cognitive load levels after Bonferroni correction (all corrected ps < 0.05). Similarly, Gamma band
exhibited a significant correlation with MMSE score (r = -0.23, p < 0.001), with significance maintained only for
rest after Bonferroni correction (corrected p = 0.004). Refer to Fig. 6 and Supplementary Material Table S26 for
the full results. Next, we constructed an LMM that integrated the group variable (including all senior groups and healthy
young controls), with the cognitive load levels (see Fig. 7 and Supplementary Material Sect. 4.2 for all LMM and
post-hoc results). Significant main effects of group were found for A0, Delta and Gamma, indicating lower activity
levels the healthier and younger the group. Subsequent post-hoc comparisons revealed significant differences
for A0 between the healthy young group and all other groups (all ps = 0.001), as well as between healthy seniors
and the MD group (p = 0.001), and MCI-R group (p = 0.037). For Gamma, the MD group showed significantly
higher activity compared to the healthy young group (p = 0.002). Delta showed a significant difference between
the MCI-R and healthy young groups (p = 0.001). An interaction between group and cognitive load was observed for VC9, ST4, Theta, Alpha, Beta and
Gamma. Simple effect comparisons indicated that differences between cognitive load levels were generally more
pronounced in cognitively healthier groups, with significant differences between cognitive load levels and rest for
healthy seniors and healthy young participants (all ps < 0.001). Complete results are available in Supplementary
Material Sect. 4.2. Discussion
Timely detection of cognitive decline is crucial for effective intervention, highlighted by the recent FDA approval
of two new AD drugs3,4. EEG serves as a valuable tool for identifying abnormal brain activity patterns that
may indicate cognitive impairment. Building on our previously published pilot study44, which explored neural
activity using a single-channel EEG, this paper presents two follow-up studies and a meta-analysis involving
237 seniors and 112 healthy young subjects, aimed at extending the scope and broadening the applicability and
relevance of the results. An auditory assessment protocol was implemented to evaluate cognitive function under
varying load conditions, facilitating a comprehensive exploration of EEG pattern changes to identify reliable
biomarkers for timely detection. The first study aimed to detect subtle cognitive differences within the healthy elderly population by examining
cognitively healthy participants. The Lasso regression model effectively selected relevant EEG and behavioral
features, demonstrating its utility in identifying individuals at risk for MCI, with results showing strong predictive
relationships between EEG patterns and cognitive performance. This approach aligns with research showing
Fig. 6. Correlation between Mini-Mental State Examination (MMSE) scores and EEG features A0 (left), and
Gamma (right) as a function of cognitive load level. Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

Fig. 7. A0 activity (top) and VC9 activity (middle), and Gamma (bottom) of the groups in the meta-analysis,
as a function of cognitive load level. Asterisks denote significant effects (*p < 0.05, **p < 0.01 and ***p < 0.001). Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

Lasso regression can predict the relationship between working memory ability and frontal brain activity through
EEG signal processing74. Another study used Lasso regression to select functional brain indicators associated
with cognitive impairment, effectively classifying participants into groups based on MoCA and MMSE scores75. An additional study suggested that a predictive model for MMSE scores based on Lasso regression, highlighting
the effectiveness of EEG biomarkers, particularly from the prefrontal regions, in indicating early cognitive
decline38. These findings highlight the potential of this approach, though further refinement and additional
variables may improve precision. Temporal patterns in EEG biomarkers revealed differences in cognitive
adaptability and load-related responses between the two study groups. Cognitive adaptability differed between
the study groups, with the Healthy group (MMSE 28–30) demonstrating more pronounced differences in VC9, ST4, and Theta activity across cognitive load levels compared to the MCI-R group (MMSE 24–27). While these
differences were initially absent in the MCI-R group, they became evident over time, suggesting a delayed or
limited adaptation process. This potential learning effect over time is consistent with the multiday learning
curve approach, which indicates that assessing learning over multiple days can reveal early Aβ-related memory
declines before conventional AD symptoms appear76,77. Higher A0 activity in the MCI-R group compared to the
Healthy group further supports this reduced adaptability. Cognitive load effects were more pronounced in the
Healthy group, suggesting cognitive load effects are more pronounced in healthy individuals and may indicate
a greater risk for MCI with lower initial MMSE scores. Theta and Delta bands showed consistent increases
during cognitively demanding tasks relative to rest, consistent with our previous findings39,44 as well as recent
literature regarding increased frontal activity of Theta18,20,78 and Delta22,79 during the performance of cognitive
demanding tasks. High within-patient consistency of EEG features across visits highlights the stability of these
biomarkers. Collectively, the first study demonstrated good intra-group consistency and notable inter-group
variability among healthy seniors. Our hypothesis was realized, as EEG biomarkers successfully identified subtle
changes in individuals at risk for cognitive decline, highlighting the potential of EEG measures to track cognitive
dynamics and differentiate between healthy aging and potential early decline. The second study aimed to validate and extend these findings by incorporating additional demographic data
and clinical evaluations using MoCA8 and PASS47. Addressing a limitation of the pilot study, the inclusion of
information regarding the education of senior participants in this study revealed no significant group differences
in education levels, a factor that can influence individual MMSE scores45,80. Other factors were also ruled out as
confounding effects, including years of employment, sleep patterns, and GDS scores, however, their inclusion
improved statistical models, enhancing the results related to the novel EEG biomarkers. A0 and Gamma activity
emerged as consistent predictors of MMSE score across different cognitive load levels, while other clinical and
demographic factors (such as CLOX, PASS drug safety, and years of employment) showed varying significance
depending on cognitive load levels. Lower MMSE and MoCA scores (indicative of greater cognitive impairments)
were associated with increased Gamma activity during the performance of cognitive tasks. Although previous
studies showed decreased Gamma band synchronization in AD81,82, the increased Gamma band power observed
during task performance persists even in cognitive decline patients, possibly indicating heightened resource
allocation under cognitive load28,83. Studying the effects of cognitive load on brain wave patterns can provide
crucial insights into the processes underlying cognitive decline, enhancing our understanding of the mechanisms
involved. These results highlight the nuanced interplay between EEG features, clinical measures, and cognitive
performance, confirming our hypothesis that combining these tools enhances the accuracy of early cognitive
decline assessment and provides a more comprehensive understanding of cognitive health and the mechanisms
underlying cognitive decline. The consistent negative correlation between A0 activity and MMSE scores, initially identified in the pilot
study44, was replicated in both the second study and the meta-analysis, strengthening the evidence for A0 as a
biomarker of cognitive function. This correlation was also extended to MoCA and IADL scores, fulfilling the
primary objective of the second study. These associations to clinical measures further validate A0 as a biomarker
related to cognitive state, as previously described43,44. Moreover, A0 effectively differentiates cognitive groups
across all analyses, thus achieving the primary goal of successfully identifying changes between cognitively
healthy individuals and individuals at risk of decline (who initially scored lower with MMSE scores between 27
and 24). This is further supported by the finding that individuals exhibiting more advanced decline showed even
higher A0 levels, suggesting a gradient of A0 activity that correlates with cognitive health. Collectively, these
findings provide further evidence that A0 is sensitive to subtle cognitive changes and is potentially suitable as a
cognitive decline biomarker. One of the central findings presented here highlights the relationship between EEG activity and cognitive
load, with healthier individuals demonstrating greater adaptability to increasing task demands. A0 activity varied
most significantly across cognitive load levels within healthy individuals, whereas the individuals at-risk for MCI
exhibited significant differences only between rest and high cognitive load conditions. In contrast, individuals
with existing cognitive deficits showed no significant changes in A0 across cognitive load levels. This pattern
of diminishing responsiveness in individuals with cognitive decline suggests reduced flexibility in managing
cognitive demands. Similarly, VC9 revealed a graded response across cognitive groups, where differences
between task and rest conditions diminished as cognitive health declined. Notably, individuals at risk of MCI
demonstrated reduced activity during higher load conditions compared to lower ones, a pattern not seen in
cognitively healthier participants. This plateauing of EEG activity indicates that individuals with early cognitive
decline may activate additional neural resources during lower loads but face difficulty sustaining this activation
as task complexity increases. These findings align with previous research showing compromised adaptability
in brain activity among seniors experiencing cognitive impairment84,85, highlighting potential limitations in
cognitive reserve. This study adds to existing diagnostic approaches, including blood and CSF biomarkers,
by offering a non-invasive, real-time assessment of brain activity that could enhance timely detection. EEG
biomarkers offer a cost-effective screening tool that may integrate with pathology-specific methods to improve
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

predictive accuracy. Additionally, EEG-based tools could ease the diagnostic workload for clinicians by serving
as an initial screening method in general or geriatric care settings. Fully automated algorithms for interpreting
EEG data may streamline this process, reducing the need for specialized training. While showing promising results, further research is needed to address limitations encountered in our
studies. For instance, the small sample size of the MD group (n = 32), challenges robust comparisons with
the larger MCI-R (n = 84) and Healthy (n = 121) groups, increasing the risk of Type II error. Expanding the
sample size for the MD group in future studies would enhance statistical power, allowing for more thorough
analyses and interpretations of differences in cognitive states. Additionally, the age-related confound among
females between MD and other groups should be taken into account when considering the results. While the
prevalence of dementia generally increases with age86–88, which may partly explain the observed differences,
the age differences should be considered a limitation of the study. The significant EEG variables identified in
the logistic regression model could be utilized in future research to predict MMSE and MoCA scores of elderly
participants, allowing for comparison with actual clinical assessment scores to assess their predictive power. In
the second study, the PASS drugs safety score emerged as a key predictor for MMSE scores in logistic regression
models across cognitive load levels. Despite its promise in assessing functional competence and distinguishing
between subjects with cognitive decline and healthy controls48, our findings did not reveal significant differences
between study groups or correlations with EEG feature activity during PASS performance. Future investigations
could explore alternative PASS sub-tasks, such as shopping or checkbook balancing, known for their robust
discriminative capabilities89. Furthermore, while this paper focuses on the timely detection of cognitive
decline, long-term studies could provide deeper insights into the predictive power of our biomarkers. Tracking
individuals at risk for MCI over time could reveal how early biomarkers relate to the actual development of
cognitive impairment, enhancing understanding of disease progression and potential early intervention. In summary, this paper highlights the effectiveness of EEG biomarkers in detecting cognitive function among
healthy elderly individuals. The integration of additional diagnostic tools and identification of key predictors
further enhances our understanding of cognitive impairment. We demonstrated the capability of EEG features
to distinguish between cognitively healthy individuals and those at risk. Collectively, our findings underscore
the potential of EEG features as a non-invasive, cost-effective and reliable approach for better understanding
cognitive states and facilitating timely diagnosis to improve clinical outcomes. Data availability
The datasets generated during and/or analyzed during the current study are not publicly available due to ethical
and privacy restrictions but are available from the corresponding author on reasonable request. Received: 20 September 2024; Accepted: 7 July 2025
References

### 1. Grand, J. H. G., Caspar, S. & MacDonald, S. W. S. Clinical features and multidisciplinary approaches to dementia care. J. Multidiscip

Healthc. 4 https://doi.org/10.2147/JMDH. S17773 (2011).

### 2. Zihl, J. & Reppermund, S. ‘The aging mind: A complex challenge for research and practice’, Aging Brain, vol. 3, (2023). ​h​t​t​p​s​:​/​/​d​o​i​.​

o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​b​a​s​.​2​0​2​2​.​1​0​0​0​6​0​

### 3. Budd Haeberlein, S. et al. Two randomized phase 3 studies of aducanumab in early alzheimer’s disease. J. Prev. Alzheimer’s Disease.

9 (2). https://doi.org/10.14283/jpad.2022.30 (2022).

### 4. Salloway, S. et al. Amyloid-Related imaging abnormalities in 2 phase 3 studies evaluating aducanumab in patients with early

alzheimer disease. JAMA Neurol. 79 (1). https://doi.org/10.1001/jamaneurol.2021.4161 (2022).
5.	 ‘Lecanemab in Early Alzheimer’s Disease’. N. Engl. J. Med., 388, 17, doi: https://doi.org/10.1056/nejmc2301380. (2023).

### 6. Sperling, R. A. et al. Toward defining the preclinical stages of alzheimer’s disease: recommendations from the National Institute on

Aging-Alzheimer’s association workgroups on diagnostic guidelines for alzheimer’s disease. Alzheimer’s Dement. 7 (3). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​j​a​l​z​.​2​0​1​1​.​0​3​.​0​0​3​ (2011).

### 7. Folstein, M. F., Folstein, S. E. & McHugh, P. R. Mini-mental state. A practical method for grading the cognitive state of patients for

the clinician. J. Psychiatr Res. 12 (3), 189–198. https://doi.org/10.1016/0022-3956(75)90026-6 (1975).

### 8. Nasreddine, Z. S. et al. The Montreal cognitive assessment, moca: A brief screening tool for mild cognitive impairment. J. Am. Geriatr. Soc. 53 (4). https://doi.org/10.1111/j.1532-5415.2005.53221.x (2005).

### 9. Mandyla, M. A. & Kosmidis, M. H. ‘Limitations and recommendations regarding the Mini-Mental state examination (MMSE) in

illiterate and low educated older adults’, 2023. https://doi.org/10.12681/psy_hps.31694

### 10. Shiroky, J. S., Schipper, H. M., Bergman, H. & Chertkow, H. Can you have dementia with an MMSE score of 30? Am. J. Alzheimers

Dis. Other Demen. 22 (5), 406–415. https://doi.org/10.1177/1533317507304744 (2007).

### 11. Dong, Y. et al. The Montreal cognitive assessment (MoCA) is superior to the Mini-Mental state examination (MMSE) for the

detection of vascular cognitive impairment after acute stroke. J. Neurol. Sci. 299 (1–2). https://doi.org/10.1016/j.jns.2010.08.051
(2010).

### 12. Salis, F., Costaggiu, D. & Mandas, A. ‘Mini-Mental State Examination: Optimal Cut-Off Levels for Mild and Severe Cognitive

Impairment’, Geriatrics (Switzerland), vol. 8, no. 1, (2023). https://doi.org/10.3390/geriatrics8010012

### 13. Barro, C. & Zetterberg, H. ‘The blood biomarkers puzzle – A review of protein biomarkers in neurodegenerative diseases’, 2021.

https://doi.org/10.1016/j.jneumeth.2021.109281

### 14. Hansson, O., Blennow, K., Zetterberg, H. & Dage, J. ‘Blood biomarkers for alzheimer’s disease in clinical practice and trials’, 2023.

https://doi.org/10.1038/s43587-023-00403-3

### 15. Cassani, R., Estarellas, M., San-Martin, R., Fraga, F. J. & Falk, T. H. ‘Systematic review on resting-state EEG for alzheimer’s disease

diagnosis and progression assessment’, 2018. https://doi.org/10.1155/2018/5174815

### 16. Dauwels, J., Vialatte, F. & Cichocki, A. Diagnosis of alzheimer’s disease from EEG signals: where are we standing?? Curr. Alzheimer

Res. 7 (6), 487–505. https://doi.org/10.2174/1567210204558652050 (2010).

### 17. Hamm, V., Héraud, C., Cassei, J. C., Mathis, C. & Goutagny, R. ‘Precocious alterations of brain oscillatory activity in alzheimer’s

disease: A window of opportunity for early diagnosis and treatment’, 2015. https://doi.org/10.3389/fncel.2015.00491

### 18. Krause, C. M. et al. ‘The effects of memory load on event-related EEG desynchronization and synchronization’, Clinical

Neurophysiology, vol. 111, no. 11, (2000). https://doi.org/10.1016/S1388-2457(00)00429-6
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

### 19. Raghavachari, S. et al. Gating of human theta oscillations by a working memory task. J. Neurosci. 21 (9). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​5​2​3​/​j​

n​e​u​r​o​s​c​i​.​2​1​-​0​9​-​0​3​1​7​5​.​2​0​0​1​ (2001).

### 20. Jensen, O. & Tesche, C. D. ‘Frontal theta activity in humans increases with memory load in a working memory task’, European

Journal of Neuroscience, vol. 15, no. 8, pp. 1395–9, (2002). https://doi.org/10.1046/j.1460-9568.2002.01975.x

### 21. Güntekin, B., Saatçi, E. & Yener, G. Decrease of evoked delta, theta and alpha coherences in alzheimer patients during a visual

oddball paradigm. Brain Res. 1235 https://doi.org/10.1016/j.brainres.2008.06.028 (2008).

### 22. Harmony, T. ‘The functional significance of delta oscillations in cognitive processing’, 2013. https://doi.org/10.3389/fnint.2013.00083

### 23. Başar, E., Başar-Eroǧlu, C., Güntekin, B. & Yener, G. G. ‘Brain’s alpha, beta, gamma, delta, and theta oscillations in neuropsychiatric

diseases: Proposal for biomarker strategies’, in Supplements to Clinical Neurophysiology, vol. 62, (2013). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​B​9​
7​8​-​0​-​7​0​2​0​-​5​3​0​7​-​8​.​0​0​0​0​2​-​8​

### 24. Michels, L. et al. Simultaneous EEG-fMRI during a working memory task: modulations in low and high frequency bands. PLoS

One. 5 (4). https://doi.org/10.1371/journal.pone.0010298 (2010).

### 25. Bair, M. S. et al. Age-related differences in working memory evoked gamma oscillations. Brain Res. 1576 ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​b​r​a​i​n​r​e​s​.​2​0​1​4​.​0​5​.​0​4​3​ (2014).

### 26. Missonnier, P. et al. Aging and working memory: early deficits in EEG activation of posterior cortical areas. J. Neural Transm. 111

(9). https://doi.org/10.1007/s00702-004-0159-2 (2004).

### 27. Stam, C. J. et al. Generalized synchronization of MEG recordings in alzheimer’s disease: evidence for involvement of the gamma

band. J. Clin. Neurophysiol. 19 (6). https://doi.org/10.1097/00004691-200212000-00010 (2002).

### 28. Van Deursen, J. A., Vuurman, E. F. P. M., Verhey, F. R. J., Van Kranen-Mastenbroek, V. H. J. M. & Riedel, W. J. Increased EEG

gamma band activity in alzheimer’s disease and mild cognitive impairment. J. Neural Transm. 115 (9). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​0​0​
7​0​2​-​0​0​8​-​0​0​8​3​-​y​ (2008).

### 29. Schmidt, R. et al. Beta oscillations in working memory, executive control of movement and thought, and sensorimotor function. J. Neurosci. https://doi.org/10.1523/JNEUROSCI.1163-19.2019 (2019).

### 30. Karrasch, M., Laine, M., Rapinoja, P. & Krause, C. M. Effects of normal aging on event-related desynchronization/synchronization

during a memory task in humans. Neurosci. Lett. 366 (1). https://doi.org/10.1016/j.neulet.2004.05.010 (2004).

### 31. Jiang, Z. Study on EEG power and coherence in patients with mild cognitive impairment during working memory task. J. Zhejiang

Univ. Sci. B. 6 (12). https://doi.org/10.1631/jzus.2005. B1213 (2005).

### 32. Al-Qazzaz, N. K. et al. ‘Role of EEG as biomarker in the early detection and classification of dementia’, 2014. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​

5​5​/​2​0​1​4​/​9​0​6​0​3​8​

### 33. Zeynali, M. & Seyedarabi, H. EEG-based single-channel authentication systems with optimum electrode placement for different

mental activities. Biomed. J. 42 (4). https://doi.org/10.1016/j.bj.2019.03.005 (2019).

### 34. Samal, P. & Hashmi, M. F. Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system:

a review. Artif. Intell. Rev. 57 (3). https://doi.org/10.1007/s10462-023-10690-2 (2024).

### 35. Grueso, S. & Viejo-Sobera, R. Machine learning methods for predicting progression from mild cognitive impairment to alzheimer’s

disease dementia: a systematic review. Alzheimers Res. Ther. 13 (1). https://doi.org/10.1186/s13195-021-00900-w (2021).

### 36. Modir, A., Shamekhi, S. & Ghaderyan, P. ‘A systematic review and methodological analysis of EEG-based biomarkers of alzheimer’s

disease’, 2023. https://doi.org/10.1016/j.measurement.2023.113274

### 37. Mitsukura, Y., Sumali, B., Watanabe, H., Ikaga, T. & Nishimura, T. Frontotemporal EEG as potential biomarker for early MCI: a

case–control study. BMC Psychiatry. 22 (1). https://doi.org/10.1186/s12888-022-03932-0 (2022).

### 38. Choi, J. et al. Resting-state prefrontal EEG biomarkers in correlation with MMSE scores in elderly individuals. Sci. Rep. 9 (1),

10468. https://doi.org/10.1038/s41598-019-46789-2 (2019).

### 39. Maimon, N. B., Molcho, L., Intrator, N. & Lamy, D. ‘Single-channel EEG features during n-back task correlate with working

memory load’, arXiv preprint, no. arXiv:2008.04987, Aug. 2020, Accessed: Oct. 06, 2020. [Online]. Available: ​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​
0​0​8​.​0​4​9​8​7​

### 40. Maimon, N. B. et al. ‘Continuous monitoring of mental load during virtual simulator training for laparoscopic surgery reflects

laparoscopic dexterity. A comparative study using a novel wireless device’. Front Neurosci, 15 (p. 1716) (2021). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​
3​3​8​9​/​f​n​i​n​s​.​2​0​2​1​.​6​9​4​0​1​0​

### 41. Bolton, F., Te’Eni, D., Maimon, N. B. & Toch, E. ‘Detecting interruption events using EEG’, in IEEE 3rd Global Conference on Life

Sciences and Technologies (LifeTech), IEEE, Mar. 2021, pp. 33–34., IEEE, Mar. 2021, pp. 33–34. (2021). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​L​i​f​e​
T​e​c​h​5​2​1​1​1​.​2​0​2​1​.​9​3​9​1​9​1​5​

### 42. Curcic, J. et al. Description of the method for evaluating digital endpoints in alzheimer disease study: protocol for an exploratory, Cross-sectional study. JMIR Res. Protoc. 11 (8). https://doi.org/10.2196/35442 (2022).

### 43. Molcho, L. et al. Evaluation of parkinson’s disease early diagnosis using single-channel EEG features and auditory cognitive

assessment. Front. Neurol. 14 https://doi.org/10.3389/fneur.2023.1273458 (2023).

### 44. Molcho, L. et al. Single-Channel EEG features reveal an association with cognitive decline in seniors performing. Auditory Cogn. Assessment’. https://doi.org/10.3389/fnagi.2022.773692 (2022).

### 45. Siqueira, G. S. A. et al. Can MoCA and MMSE be interchangeable cognitive screening tools?? Syst. Review’. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​

3​/​g​e​r​o​n​t​/​g​n​y​1​2​6​ (2019).

### 46. Khatun, S., Morshed, B. I. & Bidelman, G. M. ‘Single Channel EEG Based Score Generation to Monitor the Severity and Progression

of Mild Cognitive Impairment’, in IEEE International Conference on Electro Information Technology, (2018). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​
/​E​I​T​.​2​0​1​8​.​8​5​0​0​2​7​3​

### 47. Holm, M. B. & Rogers, J. C. ‘The performance assessment of Self-Care skills (PASS)’. Assessments Occup. Therapy Mental Health,

pp. 12. Routledge, (2020).

### 48. Dham, P. et al. Functional competence and cognition in individuals with amnestic mild cognitive impairment. J. Am. Geriatr. Soc.

68 (8). https://doi.org/10.1111/jgs.16454 (2020).

### 49. Crum, R. M., Anthony, J. C., Bassett, S. S. & Folstein, M. F. Population-Based norms for the Mini-Mental state examination by age

and educational level. JAMA: J. Am. Med. Association. 269 (18), 2386–2391. https://doi.org/10.1001/jama.1993.03500180078038
(1993).

### 50. O’Bryant, S. E. et al. Detecting dementia with the mini-mental state examination in highly educated individuals. Arch. Neurol. 65

(7), 963–967. https://doi.org/10.1001/archneur.65.7.963 (2008).

### 51. Graf, C. The Lawton instrumental activities of daily living scale. Am. J. Nurs. 108 (4). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​9​7​/​0​1​.​N​A​J​.​0​0​0​0​3​1​4​8​1​0​.​

4​6​0​2​9​.​7​4​ (2008).

### 52. Ou, Y. Y. et al. ‘Instrumental activities of daily living (IADL) evaluation system based on EEG signal feature analysis’, in 2013 Asia-

Pacific Signal and Information Processing Association Annual Summit and Conference, APSIPA 2013, (2013). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​
9​/​A​P​S​I​P​A​.​2​0​1​3​.​6​6​9​4​3​1​0​

### 53. Yesavage, J. A. et al. Development and validation of a geriatric depression screening scale: A preliminary report. J. Psychiatr Res. 17

(1). https://doi.org/10.1016/0022-3956(82)90033-4 (1982).

### 54. Royall, D. R., Cordes, J. A. & Polk, M. CLOX: an executive clock drawing task. J. Neurol. Neurosurg. Psychiatry. 64 (5). ​h​t​t​p​s​:​/​/​d​o​i​.​

o​r​g​/​1​0​.​1​1​3​6​/​j​n​n​p​.​6​4​.​5​.​5​8​8​ (1998).

### 55. Hobson, J. ‘The Montreal Cognitive Assessment (MoCA)’, (2015). https://doi.org/10.1093/occmed/kqv078

### 56. Malek-Ahmadi, M. et al. ‘Age-and education-adjusted normative data for the Montreal Cognitive Assessment (MoCA) in older

adults age 70–99’, Aging, Neuropsychology, and Cognition, vol. 22, no. 6, (2015). https://doi.org/10.1080/13825585.2015.1041449
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

### 57. Greenberg, S. A. ‘The geriatric depression scale (GDS) validation of a geriatric depression screening scale: A preliminary report’, Best Practices in Nursing Care to Older Adults, no. 4, (2019).

### 58. Perez, V., Duque, A., Hidalgo, V. & Salvador, A. ‘EEG frequency bands in subjective cognitive decline: A systematic review of

resting state studies’, Biol Psychol, vol. 191, p. 108823, Sep. (2024). https://doi.org/10.1016/J. BIOPSYCHO.2024.108823

### 59. Kane, N. et al. A revised glossary of terms most commonly used by clinical electroencephalographers and updated proposal for the

report format of the EEG findings. Revision 2017. Clin. Neurophysiol. Pract. 2 https://doi.org/10.1016/j.cnp.2017.07.002 (2017).

### 60. Jeong, J. ‘EEG dynamics in patients with alzheimer’s disease’, 2004. https://doi.org/10.1016/j.clinph.2004.01.001

### 61. Nimmy John, T., Subha Dharmapalan, P. & Ramshekhar Menon, N. Exploration of time-frequency reassignment and homologous

inter-hemispheric asymmetry analysis of MCI-AD brain activity. BMC Neurosci. 20 (1). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​8​6​/​s​1​2​8​6​8​-​0​1​9​-​0​5​1​
9​-​3​ (2019).

### 62. Hastie, T., Buja, A. & Tibshirani, R. ‘Penalized Discriminant Analysis’, The Annals of Statistics, vol. 23, no. 1, (2007). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​

g​/​1​0​.​1​2​1​4​/​a​o​s​/​1​1​7​6​3​2​4​4​5​6​

### 63. Rizk-Jackson, A. et al. Early indications of future cognitive decline: stable versus declining controls. PLoS One. 8 (9). ​h​t​t​p​s​:​/​/​d​o​i​.​o​

r​g​/​1​0​.​1​3​7​1​/​j​o​u​r​n​a​l​.​p​o​n​e​.​0​0​7​4​0​6​2​ (2013).

### 64. Rokhlin, V., Szlam, A. & Tygert, M. A randomized algorithm for principal component analysis. SIAM J. Matrix Anal. Appl. 31 (3),

1100–1124. https://doi.org/10.1137/080736417 (2009).

### 65. Meghdadi, A. H. et al. February,., ‘Resting state EEG biomarkers of cognitive decline associated with Alzheimer’s disease and mild

cognitive impairment’, PLoS One, vol. 16, no. 2 (2021). https://doi.org/10.1371/journal.pone.0244180

### 66. López, M. M. et al. ‘SVM-based CAD system for early detection of the Alzheimer’s disease using kernel PCA and LDA’, Neurosci

Lett, vol. 464, no. 3, (2009). https://doi.org/10.1016/j.neulet.2009.08.061

### 67. Choi, H. & Jin, K. H. Predicting cognitive decline with deep learning of brain metabolism and amyloid imaging. Behav. Brain. Res.

344 https://doi.org/10.1016/j.bbr.2018.02.017 (2018).

### 68. Maimon, N. B. et al. ‘EEG reactivity changes captured via mobile BCI device following tDCS intervention–a pilot-study in

disorders of consciousness (DOC) patients’, in 10th International Winter Conference on Brain-Computer Interface (BCI), IEEE, Feb.
pp. 1–3. (2022).

### 69. Benjamini, Y. & Hochberg, Y. ‘Controlling the false discovery Rate - a practical and powerful approach to multiple testing. Journal

of the Royal Statistical Society: Series B (Methodological) 57(1), 289–300 (1995). https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

### 70. Seabold, J. & Perktold, S. S., Econometric and statistical modeling with python’, in In Proceedings of the 9th Python in Science

Conference, p. 61. (2010).

### 71. Cahn-Weiner, D. A., Malloy, P. F., Boyle, P. A., Marran, M. & Salloway, S. ‘Prediction of functional status from neuropsychological

tests in community-dwelling elderly individuals’, Clinical Neuropsychologist, vol. 14, no. 2, (2000). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​7​6​/​1​3​8​5​-​4​0​
4​6​(​2​0​0​0​0​5​)​1​4​:​2​;​1​-​Z​;​F​T​1​8​7​.​

### 72. Lopez, O. L. et al. Neuropsychological characteristics of mild cognitive impairment subgroups. J. Neurol. Neurosurg. Psychiatry. 77

(2). https://doi.org/10.1136/jnnp.2004.045567 (2006).

### 73. Naftaly, U., Intrator, N. & Horn, D. ‘Optimal ensemble averaging of neural networks’, Network: Computation in Neural Systems, vol.

8, no. 3, (1997). https://doi.org/10.1088/0954-898x/8/3/004

### 74. Zhang, Y. et al. Prediction of working memory ability based on EEG by functional data analysis. J. Neurosci. Methods. 333 ​h​t​t​p​s​:​/​/​

d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​j​n​e​u​m​e​t​h​.​2​0​1​9​.​1​0​8​5​5​2​ (2020).

### 75. Liu, Y. et al. Classification of cognitive impairment in older adults based on brain functional state measurement data via hierarchical

clustering analysis. Front. Aging Neurosci. 15 https://doi.org/10.3389/fnagi.2023.1198481 (2023).

### 76. Jutten, R. J. et al. ‘Longitudinal multi-day learning curves (MDLCs) to capture subtle cognitive changes in preclinical Alzheimer’s

disease’, Alzheimer’s & Dementia, vol. 19, no. S18, (2023). https://doi.org/10.1002/alz.078818

### 77. Papp, K. V. et al. Early detection of Amyloid-Related changes in memory among cognitively unimpaired older adults with daily

digital testing. Ann. Neurol. 95 (3). https://doi.org/10.1002/ana.26833 (2024).

### 78. Onton, J., Delorme, A. & Makeig, S. ‘Frontal midline EEG dynamics during working memory’, Neuroimage, vol. 27, no. 2, (2005).

https://doi.org/10.1016/j.neuroimage.2005.04.014

### 79. Schmiedt-Fehr, C., Dühl, S. & Basar-Eroglu, C. Age-related increases in within-person variability: Delta and theta oscillations

indicate that the elderly are not always old. Neurosci. Lett. 495 (2). https://doi.org/10.1016/j.neulet.2011.03.062 (2011).

### 80. Ardila, A., Ostrosky-Solis, F., Rosselli, M. & Gómez, C. Age-related cognitive decline during normal aging: the complex effect of

education. Arch. Clin. Neuropsychol. 15 (6). https://doi.org/10.1016/S0887-6177(99)00040-2 (2000).

### 81. Koenig, T. et al. Decreased EEG synchronization in alzheimer’s disease and mild cognitive impairment. Neurobiol. Aging. 26 (2). ​h​

t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​b​i​o​l​a​g​i​n​g​.​2​0​0​4​.​0​3​.​0​0​8 (2005).

### 82. Stam, C. J. et al. ‘Magnetoencephalographic evaluation of resting-state functional connectivity in Alzheimer’s disease’, Neuroimage,

vol. 32, no. 3, (2006). https://doi.org/10.1016/j.neuroimage.2006.05.033

### 83. Osipova, D., Pekkonen, E. & Ahveninen, J. Enhanced magnetic auditory steady-state response in early alzheimer’s disease. Clin. Neurophysiol. 117 (9). https://doi.org/10.1016/j.clinph.2006.05.034 (2006).

### 84. Schneider-Garces, N. J. et al. Span, CRUNCH, and beyond: working memory capacity and the aging brain. J. Cogn. Neurosci. 22

(4). https://doi.org/10.1162/jocn.2009.21230 (2010).

### 85. Cappell, K. A., Gmeindl, L. & Reuter-Lorenz, P. A. ‘Age differences in prefontal recruitment during verbal working memory

maintenance depend on memory load’, Cortex, vol. 46, no. 4, (2010). https://doi.org/10.1016/j.cortex.2009.11.009

### 86. Sachdev, P. S. et al. Risk profiles for mild cognitive impairment vary by age and sex: the Sydney memory and ageing study. Am. J. Geriatric Psychiatry. 20 (10). https://doi.org/10.1097/JGP.0b013e31825461b0 (2012).

### 87. Ritchie, K. & Lovestone, S. ‘The dementias’, in Lancet, (2002). https://doi.org/10.1016/S0140-6736(02)11667-9

### 88. Yaffe, K. et al. Mild cognitive impairment, dementia, and their subtypes in oldest old women. Arch. Neurol. 68 (5). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​

1​0​.​1​0​0​1​/​a​r​c​h​n​e​u​r​o​l​.​2​0​1​1​.​8​2​ (2011).

### 89. Rodakowski, J. et al. Can performance on daily activities discriminate between older adults with normal cognitive function and

those with mild cognitive impairment? J. Am. Geriatr. Soc. 62 (7). https://doi.org/10.1111/jgs.12878 (2014). Acknowledgements
The authors express heartfelt thanks extended to the study participants and the supportive staff for their contri­
butions to this research. Author contributions
Conception and study design L. M., N. B. M, T. Z. and N. I.; Data acquisition; T. Z., O. C., S. R, V. A and N. B. O; Supervision N. I. and A. S; Data analysis and Writing L. M., N. B. M, T. Z., O. C., and N. I; All authors read and ap­
proved the final manuscript. Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/

Declarations
Competing interests
L. M., N. B. M., and N. I. have equity interest in Neurosteer, which developed the Neurosteer EEG recorder. T. Z
and O. C. are employed in Neurosteer. The other authors declare no competing interests. Additional information
Supplementary Information The online version contains supplementary material available at ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​3​8​/​s​4​1​5​9​8​-​0​2​5​-​1​0​9​8​3​-​2​.​
Correspondence and requests for materials should be addressed to L. M. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Open Access  This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives
4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in
any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide
a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have
permission under this licence to share adapted material derived from this article or parts of it. The images or
other third party material in this article are included in the article’s Creative Commons licence, unless indicated
otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence
and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to
obtain permission directly from the copyright holder. To view a copy of this licence, visit ​h​t​t​p​:​/​/​c​r​e​a​t​i​v​e​c​o​m​m​o​
n​s​.​o​r​g​/​l​i​c​e​n​s​e​s​/​b​y​-​n​c​-​n​d​/​4​.​0​/​.​
© The Author(s) 2025
Scientific Reports | (2025) 15:25503

| https://doi.org/10.1038/s41598-025-10983-2
www.nature.com/scientificreports/
