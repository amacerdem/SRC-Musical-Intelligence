# An EEG Dataset on Aesthetic and Creative Judgments of Brief Structured Poetry

**Authors:** Soma Chaudhuri
**Year:** D:20
**Subject:** Scientific Data, doi:10.1038/s41597-025-06189-w

---

Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
An EEG Dataset on Aesthetic
and Creative Judgments of Brief
Structured Poetry
Soma Chaudhuri1,2 & Joydeep Bhattacharya1,3 ✉
Understanding how the brain engages with poetic language is key to advancing empirical research
on aesthetic and creative cognition. We present a 64-channel EEG and behavioural dataset from 51
participants who read and evaluated 210 short English-language texts (70 Haiku, poems focusing on
nature; 70 Senryu, poems focusing on emotion; 70 structurally-matched non-poetic control texts). Participants rated each stimulus on five dimensions (aesthetic appeal, vivid imagery, emotional
impact, originality and creativity) on a 7-point scale. The dataset includes time-aligned EEG and
behavioural responses, self-report trait measures, and rich stimulus metadata. Further, the dataset
also includes resting state EEG data before and after the experiment. Exploratory validation analysis
revealed condition-specific spectral power differences and trial-level brain-behaviour associations. By
combining poetic structure, subjective evaluation, and high-temporal-resolution neural activity, this
comprehensive dataset enables detailed investigation into neuroaesthetics, cognitive poetics, and the
neuroscience of creativity. Background & Summary
Imagine reading Wordsworth’s The Solitary Reaper, where the beauty of nature unfolds vividly before your eyes,
and the melody of the reaper’s song lingers in your mind. Or turning to Yeats’ When You Are Old, where the
gentle pull of nostalgia and subtle melancholy fills your heart. These poetic experiences, simultaneously visual,
emotional, and rhythmic, are familiar to many readers. Yet, the underlying neurocognitive processes that shape
our experience of poetry remain only partially understood1,2. Poetic language is rich in stylistic devices and ‘figures of thought’, such as metaphor, conceit or extended met-
aphor, polysemy, irony, metonymy, oxymoron and so on, which engage both affective and cognitive processes3. Such features make poetry a powerful domain for empirical investigation of the mind–brain interface. Turner
and Pöppel4 argued that poetry reflects and resonates with the hierarchical and rhythmic organisation of the
human brain. Thus, neuroscientific explorations of poetry offer not only novel perspectives for neuroaesthetics
but also valuable insights into broader questions concerning language, creativity, and emotion. Compared to other art forms, poetry has received considerably less attention in cognitive neuroscience. Robust empirical work has focused on the neural mechanisms underlying music perception5–7, visual aesthet-
ics8–10, and story comprehension11–13. In contrast, relatively few studies have examined how poetic language is
processed in the brain14,15. Functional neuroimaging research indicates that reading poetry engages distinct
neural circuits compared to prose, including lateral frontal, temporal, and occipital cortices, and regions associ-
ated with introspection and emotion16,17. Although these findings demonstrate that poetic language can activate
emotional brain circuits, they offer only limited insight into the temporal dynamics of this engagement. In
contrast to fMRI, M/EEG provides millisecond-level resolution, enabling a more detailed examination of the
unfolding cognitive and emotional processes during the experience of poetry. However, despite growing interest in the neurocognitive dimensions of literary language, there is currently
a lack of open-access, high-temporal-resolution M/EEG datasets that allow for the systematic examination of
poetic engagement. Existing public electrophysiological datasets in the domain of language largely focus on
sentence comprehension18,19, emotion recognition20,21, or story/narrative comprehension22,23, but no publicly
available dataset offers integrated behavioural and electrophysiological responses to authentic poetic stimuli.
1Department of Psychology, Goldsmiths University of London, London, UK. 2Penn Center for Neuroaesthetics, University of Pennsylvania, Pennsylvania, USA. 3Academy of Music, School of Creative Arts, Hong Kong Baptist
University, Hong Kong, China. ✉e-mail: jbhattacharya@hkbu.edu.hk
Data Descriptor
OPEN

Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
To address this gap, we present a dataset comprising 64-channel EEG recordings and concurrent behavioural
evaluations obtained during silent reading and contemplation on English-language Haiku and Senryu. These
brief poetic forms are structurally constrained yet semantically and emotionally rich24–26. While Haiku tend to
evoke natural imagery and seasonal transitions, Senryu focus on human experiences and emotional nuance,
often delivered with irony or humour. Normative, traditionally structured Haiku and Senryu, with their highly
constrained yet evocative structures, offer a unique balance of semantic richness and formal constraints, making
them particularly well-suited for isolating aesthetic and cognitive responses to poetic language27; see also28. Their brevity not only facilitates precise experimental control but also foregrounds essential poetic features, such
as imagery, affect and insight, that are central to neuroaesthetic inquiry. Participants rated each poem along five dimensions: aesthetic appeal, vivid imagery, emotional impact, orig-
inality, and creativity. These were chosen to capture key facets of aesthetic and creative engagement with poetry. This dimensions were grounded in established theoretical frameworks in neuroaesthetics3,14,29–31 and empirical
aesthetics15,32–38, which emphasize the role of evaluative, imagery-based, and affective processes in art perception
and experience. The inclusion of originality and creativity reflects their centrality in psychological models39–42
of creative cognition and their empirical validation43–48. Further, these dimensions have recently been vali-
dated specifically in the context of poetry evaluation49–52. Together, the selected dimensions offer a theoretically
grounded and empirically supported framework for capturing nuanced subjective responses to poetic stimuli. This dataset captures not only neural responses to poetic language but also subjective evaluations of poetic
quality, enabling the study of how aesthetic and creative judgments are instantiated in the brain. Further, the
dataset also contains resting-state brain activity and several self-reported personality traits of the participants. The dataset complements and extends prior behavioural studies suggesting that creativity judgments in poetry
are modulated by affective and perceptual dimensions53,54 and provides a foundation for linking such judgments
to large-scale brain oscillations in future analyses. By making this dataset publicly available, we offer a novel,
well-annotated resource that enables fine-grained exploration of how the human brain engages with poetic
language. This resource will serve a wide community of researchers across cognitive neuroscience, psychology,
linguistics, poetics, and digital humanities, and we hope it will stimulate further interdisciplinary research into
the neurocognitive mechanisms of literary aesthetics and creativity. Methods
Study design. This study employed a within-subjects design to investigate neural and behavioural responses
to structurally concise but semantically rich poetic stimuli. Each participant completed several tasks: (i) com-
pletion of the demographic and personality questionnaires before the EEG recording, (ii) resting-state EEG
recordings before and after the full session of poetic reading and evaluations, (iii) EEG recording during reading,
contemplation and evaluation of poetic stimuli. Ethical approval was obtained from the Local Ethics Committee
at the Department of Psychology, Goldsmiths University of London (Protocol Number: PS270423SCS). The
experiment was conducted in accordance with the Declaration of Helsinki. All participants provided informed content after reading an information sheet explaining the purpose of
the study, its procedures, provisions for confidentiality, and intended use of the data. For example, the sheet
explained: “This student research project aims to assess the neural signatures associated with perception and
evaluation of creativity of poems. The study would explore how our brain responds while reading and contem-
plating poems. Here, you are to evaluate English poems based on your subjective feelings and experiences. No
prior knowledge is expected.” Participants were explicitly informed about the use of their anonymized data for
research and publication purposes (e.g., “All data collected from the study will be strictly confidential, stored
on secure electronic information systems. All data that leaves the university will be anonymised, and names
and other identifying information will be removed” and “The data will be used to further this research, any
publication of the study will maintain confidentiality and anonymity of participants.”). Informed consent was
obtained electronically prior to participation. Each participant completed an electronic consent form, where
they confirmed (by selecting “Yes/No”) that they had read the Research Participant Information Sheet, under-
stood the confidentiality provisions, and were informed of their right to terminate the experiment at any time
without any consequence. They were also informed of their right to withdraw at any time, including post-study
withdrawal via their unique participant ID. Only those participants who responded “Yes” to all mandatory items
were allowed to proceed. Each participant then provided a unique ID (“First three letters of your mother’s name
followed by two digits of your month of birth”) which was used in place of names. Participants were informed
of their rights under the General Data Protection Regulation (GDPR) and Goldsmiths Research Guidelines,
which outlined their rights regarding personal data (e.g., the right to be informed about data use and the right
of access through subject access requests). All data were stored securely on university computers, and only fully
anonymized data were exported for further analysis and sharing. Subject. Fifty-one right-handed individuals participated in the experiment (N = 51; 16 male, 28 female, 7
non-binary; mean age = 27.14 years, SD = 4.55). An a priori power analysis was conducted using G*Power 3.155
to determine the minimum sample size required for a repeated-measures ANOVA with within-subject factors. Assuming an effect size of f = 0.229 (corresponding to η² = 0.05), α = 0.05, power = 0.80, three measurements
(Haiku, Senryu, Control), a correlation of 0.5 among repeated measures, and a nonsphericity correction ε = 1,
the required sample size was 33. The sample size of 51 participants exceeded this threshold, yielding an actual
power of 0.81. All participants provided written informed consent and received monetary compensation (£30). However, four participants’ recordings (participant numbers # 5, 41, 42, and 46) were discarded during the spec-
tral power validation analyses due to procedural interruptions (e.g., repeated absences), that compromised data
integrity. Nevertheless, their EEG recordings are included in a separately shared dataset for transparency and
potential reuse. Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
Questionnaires. Before the main experiment, participants completed self-reported questionnaires on demo-
graphics, and personality traits. Mood was captured before and after the experiment. For each trait questionnaire,
instructions were provided to participants, who chose the most appropriate option for each item. Participants
were also informed that there were no right or wrong answers and were instructed to respond honestly and with-
out long deliberation. Demographic questionnaire. Demographic data comprised gender, age, ethnicity, location, education, and
prior experience or exposure to poetry (e.g. “Do you like reading poetry?”, and “How long have you been associ-
ated with poetry?”). Of note, poetry liking was assessed with a single broad item (‘Do you like reading poetry?’),
which was intended to capture general orientation toward poetry and did not distinguish between preferences
for specific poetic traditions or genres. Psychometric questionnaires. Positive and Negative Affect Schedule (PANAS). This is a 20-item scale56 (10
positive, 10 negative) for assessing participants’ general affective tendencies over the past week. Example items
include “Excited” and “Jittery.”
Openness/Intellect. It is a subscale of the Big Five Aspect Scale (BFAS57) to assess openness and intellect. It has
20 items, 10 items for assessing openness and 10 items for assessing intellect. Example items include “I love to
reflect on things” and “I like to solve complex problems”. Curiosity. It is a 10-item scale58 for assessing an individual’s tendency to seek out and explore novel information. Example items include “I enjoy learning about subjects which are unfamiliar”. Vividness of Visual Imagery Questionnaire (VVIQ). It is a 16-item scale59 to assess visual imagery, i.e., the
ability to generate clear and detailed mental images. Participants were asked to imagine specific scenarios (e.g., a
rising sun) and then rate the vividness of their mental images. Vividness of Auditory Imagery (BAIS-V, termed here as AVIQ, auditory vividness imagery questionnaire,
for clarity). This 14-item scale60 evaluates the clarity and vividness of internally generated auditory imagery. Participants were asked to imagine specific auditory scenarios (e.g., attending a choir rehearsal) and then rate the
vividness of their mental images. Mindfulness Attention Awareness Scale (MAAS). This 15-item scale61 provides an unidimensional measure
of dispositional mindfulness and present-moment awareness. Sample items include “I rush through activities
without being really attentive to them”. Aesthetic Responsiveness Assessment (AReA). This 12-item scale62 evaluates an individual’s sensitivity to aes-
thetic experiences in diverse artistic domains. Sample items include “I notice beauty when I look at art”. Stimuli. The stimulus set consisted of 210 short English-language texts: 70 Haiku, 70 Senryu, and 70 structur-
ally matched non-poetic control texts. All Haiku and Senryu were sourced from prestigious literary competitions
to ensure authenticity, quality, and adherence to traditional poetic forms. Specifically, poems were drawn from
award-winning entries of the Haiku Society of America Haiku Award (1976–2022), the British Haiku Society
Awards (2002–2021), and the Haiku Society of America Senryu Award (1988–2022). Haiku and Senryu were chosen because they represent two minimalist Japanese poetic genres that share
the same 3-line, 5–7–5 syllabic structure but differ thematically. Haiku traditionally evoke nature, seasonal
references, and aesthetic imagery, while Senryu often focus on human affairs, irony, or humor63,64. This com-
bination of structural uniformity (controlled syllabic constraints) and content variability (nature vs. human/
social themes) makes them particularly suitable for controlled experimentation in cognitive and neuroaesthetic
research. In the present study, we used original English-language Haiku (ELH) and Senryu rather than translated
versions. ELH have been increasingly adopted in empirical investigations due to their brevity, structural consist-
ency, and accessibility, enabling precise experimental control while engaging diverse cognitive processes such as
imagery, emotion, and aesthetic evaluation27,51–53,65,66. The control texts were structurally matched to the Haiku
and Senryu with a 3-line, 5-7-5 syllabic pattern, and were carefully selected and adapted from AI-generated
repositories using prompts designed to avoid emotional depth, figurative language, or poetic elements. To con-
firm emotional neutrality, we conducted a sentiment analysis of the 70 control texts using the sentimentr pack-
age67 in R (v2.7.1), which showed that the corpus was, on average, neutral in polarity (mean = 0.17, SD = 0.37;
range –0.82 to +1.25). These texts served as a structurally equivalent but semantically neutral baseline, allowing
for isolating the effects of poetic content on neural and behavioural responses. See Table 1 for a typical example
of each type of stimulus used in the study. Importantly, all stimuli were presented without identifying information, including the poets’ names, award
status, or genre classification (Haiku or Senryu). This anonymisation was implemented to minimise potential
biases in creativity judgments, ensuring that evaluations were based solely on textual content. By eliminating
contextual cues, our design sought to reduce familiarity effects, preconceived expectations, and prestige bias,
thereby supporting a more objective appraisal of poetic aesthetics and creativity. Experimental procedure. The experiment was implemented using PsychoPy68, an open-source software
platform widely used for the design of psychophysics and neuroscience experiments. The study employed a
within-subjects, repeated-measures design in which each participant encountered all three stimulus conditions
(Haiku, Senryu, and Control). The stimuli were presented in seven blocks of 30 trials each, totalling 210 trials

Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
(70 Haiku, 70 Senryu, 70 control). Each block comprised 10 stimuli of each type. The order of blocks and the trial
sequence within each block were randomised per participant to mitigate order effects and ensure variability in
presentation. The EEG session began with a 5-minute resting-state period with eyes open, during which participants
maintained visual fixation on a centrally presented cross. Following the initial resting-state period, the main
experimental phase began, during which participants were presented with all three stimulus conditions: Haiku, Senryu, and control texts, along with on-screen instructions guiding them through the upcoming tasks. In each trial, a stimulus was presented for 10 seconds: 5 seconds for silent reading and 5 seconds for con-
templation, and these instructions (i.e. whether to read or to contemplate) were shown on the screen (see
Fig. 1). Afterwards, participants rated the text on five dimensions using a 7-point Likert scale (1 = “very low,”
7 = “very high”): aesthetic appeal (“How aesthetically appealing is the poem?”), vivid imagery (“How vivid is
the imagery?”), emotional impact (“How moved are you?”), originality (“How original is the poem?”), and
creativity (“How creative is the poem?”). No time limit was imposed for making ratings. Participants initiated
each new trial manually by pressing the space bar. Each poem remained on the screen during the reading and
reflection phases, as well as during the subsequent evaluation phase, which had no time limit. This ensured that
participants had sufficient time to contemplate and evaluate the text beyond the fixed reflection interval. The
5-second reflection represents a methodological compromise given the high number of trials (210), trial dura-
tion needed to be constrained to avoid excessive session length and associated participant fatigue or disengage-
ment. Optional breaks were offered between blocks to reduce fatigue. Each poem was presented in its entirety
(rather than word-by-word) to preserve a natural reading experience. Eye movements were monitored using
electrooculographic (EOG) channels to enable artefact detection and correction. A second 5-minute eyes-open resting-state period was recorded at the end of the session to complete the
EEG protocol. Resting-states EEG was recorded in an eyes-open condition, during which participants were
instructed to fixate on a central cross on the screen. Thus, choice was made to enhance ecological validity and
ensure comparability with the visual and attentionally engaging nature of the main task (i.e. reading poetic
texts). Further, eyes-open rest mitigates the dominance of occipital alpha typically observed in eyes-closed
Haiku
Senryu
Control
harvest festival
refugee –
laptop powers up
jars of fig jam
where to bury
display glowing
full of galaxies
his child
ready for us
Table 1. Examples of the three stimulus categories used in the study: Haiku (nature-focused), Senryu
(emotion-focused), and non-poetic control texts. All stimuli adhered to the 3-line, 5-7-5 syllabic structure. Control texts were structurally matched but devoid of poetic devices, figurative language, or emotional content. Fig. 1  Experimental design. Each session began with a 5-minute resting-state EEG recording. Each trial
consisted of a fixation cross (4 s), followed by poem presentation (5 s reading), during which the poem remained
on screen for an additional 5 s contemplation period. In the subsequent evaluation phase, the poem was re-
displayed on the left side of the screen together with the five rating scales (aesthetic appeal, vivid imagery, being
moved, originality, creativity) presented on the right. The right column of the figure illustrates these elements
together for compactness of visualization; in the actual experiment, however, they appeared sequentially in the
order described. The session concluded with a second 5-minute resting-state recording. Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
conditions69), thereby preserving spectral variability across bands. Prior studies also show that eyes-open rest
engages neural networks more similar to task-based states70,71. Thus, this design provides a functionally aligned
baseline for studying aesthetic and creative engagement. Data acquisition. Electroencephalographic (EEG) signals were recorded using a 64-channel active electrode
system (BioSemi ActiveTwo; www.biosemi.com), with electrode placement conforming to the extended 10–20
international system. Eye movements were monitored using four electrooculographic (EOG) electrodes: two
placed above and below the right eye (vertical EOG), and two at the outer canthi of both eyes (horizontal EOG). Two additional electrodes were placed on the left and right earlobes, whose average was used as the reference
signal72. Electrocardiographic (ECG) activity was recorded using electrodes placed on the right collarbone and
left waist. These signals were acquired as part of the recording setup but were not analyzed in the present study
and are therefore not reported in the dataset description. All signals were recorded at a sampling rate of 512 Hz. Data preprocessing. EEG data were preprocessed using EEGLAB73. Signals were re-referenced to the aver-
age of the two earlobes. A 0.5 Hz high-pass filter was applied to remove slow drifts, and notch filters were applied
at 50 Hz (±2 Hz) and 100 Hz (±2 Hz) to eliminate powerline interference. The continuous EEG data were seg-
mented into epochs time-locked to stimulus onset. Each trial was epoched into a 15 s window spanning –4 to
+11 s relative to stimulus onset. This included a 4 s pre-stimulus baseline, the 10 s stimulus period (5 s reading and
5 s contemplation), and a 1 s post-stimulus buffer to accommodate delayed neural responses (i.e. capturing those
responses that might extend slightly beyond the visual presentation, like internal evaluation, imagery, memory
access) and reduce edge effects in spectral analyses. Independent component analysis (ICA) was performed using the EEGLAB73 function, runica(). ICA was
applied to the 64 EEG channels (excluding external electrodes). Components associated with artefacts, such
as eye blinks and muscle activity, were identified through a semi-automated procedure and removed following
visual inspection. On average, one component was excluded per participant (M = 1.0, SD = 0.0), typically corre-
sponding to blink artifacts. The resulting artefact-cleaned data were subsequently saved. Data Records
The datasets74,75 are available at OpenNeuro and contain data from 51 participants collected during the poetry
assessment EEG study. The full collection comprises EEG and behavioural data from 51 participants, organized
into two BIDS (Brain Imaging Data Structure)-compliant datasets. Poetry Assessment EEG Dataset 174 includes
47 participants whose data were used in primary analyses, while Poetry Assessment EEG Dataset 275 includes the
four excluded participants (P105, P141, P142, and P146), whose EEG sessions were interrupted and later concat-
enated. These excluded participants’ data were not used in power spectral density analyses due to compromised
recordings (e.g., repeated absence from sessions) but are shared for completeness and transparency. To maintain
traceability while preserving anonymity, both datasets include a participants.tsv file that maps anonymized BIDS
IDs (e.g., sub-001 to sub-047 in Poetry Assessment EEG Dataset 174; sub-001 to sub-004 in Poetry Assessment
EEG Dataset 275) to the original participant identifiers used during data collection (e.g., P101–P151). Each subject folder contains four core EEG files (channels.tsv, eeg.json, eeg.set, events.tsv), and a code/ direc-
tory includes the MATLAB preprocessing script (Preprocessing.m) and the BioSemi 64-channel coordinate
file. Within the /derivatives/ directory, two subfolders—Behavioural_Ratings/ and Psychometric_Responses/—
organize trial-level behavioural ratings (e.g., aesthetic appeal, imagery, emotional impact, originality, creativ-
ity) and trait-level psychometric measures (e.g., PANAS, openness, curiosity, VVIQ, AVIQ, MAAS, AReA),
respectively. The Behavioural_Ratings/ folder contains trial-level behavioural ratings for each participant, stored as indi-
vidual.csv files (e.g., P101.csv). The Psychometric_Responses/ folder includes a single comprehensive.csv file
containing demographic and trait-level psychometric measures for all participants along with references to the
source questionnaires. Stimulus materials (all 210 poems and block-wise assignments) are provided in a /stim-
uli/ folder. Each dataset is accompanied by a comprehensive README file documenting structure, variable
definitions, preprocessing steps, and usage instructions, with additional README files in the behavioural and
psychometric subfolders. To facilitate navigation, Table 2 provides a structured overview of the dataset contents
and file organization, including folder hierarchy, file types, and descriptions. This table summarizes the location
of raw EEG data, event metadata, behavioural and psychometric responses, questionnaires, stimuli, preprocess-
ing code, participant mappings, and documentation files. Of note, the anonymized participant IDs (e.g., PXXX) are used consistently across all data modalities,
enabling reliable cross-referencing between EEG data, behavioural ratings, and psychometric responses. Resting-state recordings collected at the beginning and end of the session are included in the raw EEG files. These segments can be identified via event codes 65285 and 65286 (start) and 65287 and 65288 (end) in the
corresponding events.tsv files. Technical Validation
We implemented strong quality control protocols across all modalities to ensure the reliability and scientific
utility of the dataset. Behavioural Validation. To verify task compliance and engagement, we analyzed behavioural ratings for
scale use and consistency across conditions. Participants used the full range of all five 7-point dimensions (aes-
thetic appeal, imagery, emotional impact, originality, creativity), indicating appropriate engagement. Internal
consistency of trait questionnaires was high (Cronbach’s α > 0.80 across all scales), and response completeness
was 100%. To examine potential fatigue effects, we computed block-level means across the seven experimen-
tal blocks for each evaluative dimension. Ratings remained stable over time (e.g., Aesthetic Appeal: M = 4.04, Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
SD = 0.10; Imagery: M = 4.65, SD = 0.15; Emotional impact (‘Moved’): M = 3.70, SD = 0.10; Originality: M = 3.95, SD = 0.07; and Creativity: M = 3.92, SD = 0.08), and linear trend analyses revealed all slope estimates
were near zero and no significant changes across blocks (all ps >.50), indicating no systematic decline in ratings
over time. The mean ratings (see Fig. 2) showed that Haiku received the highest aesthetic appeal score (M = 4.68),
followed by Senryu (M = 4.40), while control texts were rated lower (M = 3.04). Haiku was also rated high-
est for vivid imagery (M = 5.12), slightly above Senryu (M = 5.00), with controls scoring lower (M = 3.81). For emotional impact (‘Moved’), Senryu (M = 4.18) slightly outperformed Haiku (M = 4.16), while control
texts again scored the lowest (M = 2.73). For originality, ratings were close between Haiku (M = 4.50)
and Senryu (M = 4.52), both surpassing controls (M = 2.79). For creativity, ratings were similarly high for
Haiku (M = 4.54) and Senryu (M = 4.53), with controls rated notably lower (M = 2.65). Together, these
descriptive differences indicate that the poetic stimuli elicited stronger aesthetic and creative evaluations
than control texts, validating the behavioural task. These results indicated that while Haiku was more aes-
thetically appealing, Senryu was perceived as slightly more emotionally moving, with both poetic forms
being rated highly for vividness and originality. A detailed analysis of these behavioral findings has been
reported in a recent study51. EEG Validation. Spectral power analyses were conducted across five canonical frequency bands (delta:
0–4 Hz, theta: 4–8 Hz, alpha: 8–12 Hz, beta: 12–30 Hz, gamma: 30–48 Hz) using Welch’s method76,77. Four partic-
ipants’ recordings were excluded due to procedural interruptions that compromised data integrity (e.g., repeated
absence from recording sessions), resulting in a final sample of 47 participants (13 male, 28 female, 6 non-binary;
mean age = 27.06 years, SD = 4.66). Power spectral density (PSD) was calculated with the 10-s post-stimulus period divided into 2-s windows
(500 ms overlap). Periodograms were computed per electrode and trial, with the first 4 seconds (–4–0 s) serving
as baseline, 0–5 s as the early (reading) phase, and 5–10 s as the late (contemplation) phase. Spectral power values
were averaged across frequencies within a frequency band, log-transformed, and normalized by baseline power
to account for inter-individual variability. File Type(s)
Description
Poetry Assessment EEG Dataset 174 (47 participants’ dataset)
Raw EEG data for 47 participants, organized in BIDS format. Poetry Assessment EEG Dataset 275 (4 excluded participants’ dataset)
Raw EEG data for 4 participants, organized in BIDS format. Each Folder contains the following folders/files
code/
Preprocessing.m
MATLAB preprocessing script. BioSemi64.loc
BioSemi 64-channel electrode coordinate file.
derivatives/Behavioural_Ratings/
PXXX.csv
Trial-level behavioural ratings (PoemName, PoemType, Block, 5
rating scales). README_Behavioural
Documentation of behavioural data structure and usage notes.
derivatives/Psychometric_Responses/
Psychometric_Responses.csv
Demographic and psychometric data..pdf
Questionnaire references and demographic questions. README_Psychometric
Description of questionnaire variables and scoring.
stimuli/
Stimuli information.pdf
All 210 texts (Haiku, Senryu, Control).xlsx
Trial assignment files for Block_1 to Block_7.
sub-001 to sub-047
Each subject folder contains:
sub-***_task-readpoetry_channels.tsv
Channel information for EEG data.
sub-***_task-readpoetry_eeg.json
EEG metadata.
sub-***_task-readpoetry_eeg.set
EEG data in EEGLAB format.
sub-***_task-readpoetry_events.tsv
Trial-by-trial event annotations. Top-level files
dataset_description.json
Dataset metadata file.
participants.tsv
Participant information and demographics. README
Comprehensive documentation of dataset structure.
task-readpoetry_events.json
Key for experimental event codes and descriptions. Table 2. Overview of dataset contents and file structure, including folder hierarchy, file types, and descriptions
of all components: raw EEG data, event metadata, behavioural and psychometric responses, questionnaires,
stimuli, preprocessing code, participant mappings, and documentation files. All EEG, behavioural, and
psychometric data were anonymized. Participant identifiers were coded (P101–P151), and no names, dates of
birth, or other direct identifiers are included. Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
To ensure cortical region-specific coverage of neural activity, and in alignment with standard practices
in EEG research78–81, we grouped electrodes into six scalp-based clusters (frontal, fronto-temporal, and
parieto-occipital in each hemisphere; see Fig. 3) to provide broad anterior–posterior coverage while keeping
the structure simple and interpretable. This clustering scheme was based on topography alone, rather than
frequency- or power-specific characteristics. Mid-line electrodes (e.g., FCz, Cz, Pz) were not grouped into a
separate ROI, as they often capture spatially averaged or overlapping activity from adjacent electrode regions,
making them less suitable for coarse regional grouping in exploratory analyses. This scheme was intended
to balance spatial coverage with interpretability, and our primary goal was to demonstrate that the data-
set supports interpretable frequency-domain analyses rather than to test specific hypotheses about regional
specialization. Fig. 2  Distribution of ratings across three conditions (C = Control, H = Haiku, and S = Senryu) for five
evaluative dimensions: aesthetic appeal, imagery, emotional impact (being moved), originality, and creativity. There are five subplots, one for each evaluative dimension. Each subplot shows three violin plots depicting the
full distribution of ratings across the three conditions for that specific evaluative dimension. Fig. 3  Electrode groupings into six scalp-based regions of interest (ROIs) used for spectral quality checks. Electrodes were clustered according to the international 10–20 system into frontal, fronto-temporal,
and parieto-occipital regions, separately for the left (CL1–CL3) and right (CL4–CL6) hemispheres. This
organization provides region-specific coverage for assessing EEG signal quality across the scalp. Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
To provide a descriptive overview of EEG spectral responses, Fig. 4 shows mean power values across six
electrode clusters for each frequency band (delta, theta, alpha, beta, gamma) and condition (Haiku, Senryu, Control). These plots illustrate that reliable oscillatory activity was obtained across clusters and conditions, with
visible variation across bands and hemispheric groupings. Error bars represent the standard error of the mean,
confirming stable estimation across participants. To provide a descriptive overview of the spatial distribution
of spectral power, Fig. 5 presents topographical maps for all five canonical frequency bands (delta, theta, alpha,
beta, gamma) across Haiku, Senryu, and Control conditions at early and late intervals. These scalp distributions
are shown without inferential contrasts (in line with the journal’s guidelines), and serve to illustrate the spatial
resolution and signal quality of the dataset. The maps confirm that robust and interpretable topographical pat-
terns are observable across conditions, supporting the dataset’s suitability for frequency-domain and topograph-
ical analyses. Together, PSD plots (Fig. 4) and topographical maps (Fig. 5) confirm that the dataset preserves meaning-
ful oscillatory and spatial organization. In combination with behavioural compliance checks (e.g., full scale
use, systematic stimulus differentiation), these validations indicate that the EEG signals are of high quality
and suitable for a wide range of advanced applications such as connectivity analysis, network modeling, and
machine-learning approaches. These quality assurances enable a wide range of downstream applications, sup-
porting both conventional and cutting-edge EEG analysis. Usage Notes
The datasets74,75 are provided in standard EEG formats compatible with widely used analysis toolboxes, includ-
ing EEGLAB, FieldTrip, and MNE-Python. Researchers may choose to apply their own preprocessing pipelines
depending on the analytical goals. While basic preprocessing guidance is described in the Methods section,
users may wish to adapt alternative strategies to suit their specific hypotheses. This study supports multiple lines
of research. First, it enables trial-level investigations of brain-behaviour relationships, linking EEG dynamics
(spectral, connectivity, network parameters etc) with subjective evaluations of poetic stimuli. Second, the inclu-
sion of demographic and psychometric data allows for analysis of individual differences in aesthetic and creative
evaluation. Third, the data can also be used for methodological development, including EEG processing, and
machine learning-based decoding of aesthetic or creative judgments. Finally, the availability of both resting-state
and task-based EEG supports comparative studies of intrinsic and stimulus-driven neural dynamics. However,
given the modest sample size, users are advised to interpret group-level inferences with appropriate caution. Nevertheless, the dataset provides a valuable resource for advancing research in neuroaesthetics, cognitive poet-
ics, and the neuroscience of creativity. Fig. 4  Power spectral density (PSD) estimates across all five canonical frequency bands (delta, theta, alpha,
beta, gamma) and electrode clusters. The plots illustrate that robust and reliable neural oscillations were
obtained across participants, confirming that the dataset supports frequency-domain EEG analyses. Error bars
represent standard error of the mean. Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
Data availability
The datasets74,75 are available at OpenNeuro and contain data from 51 participants collected during the poetry
assessment EEG study. The full collection comprises EEG and behavioural data from 51 participants, organized
into two BIDS (Brain Imaging Data Structure)-compliant datasets. Poetry Assessment EEG Dataset 174 includes
47 participants whose data were used in primary analyses, while Poetry Assessment EEG Dataset 275 includes
the four excluded participants, whose EEG sessions were interrupted and later concatenated. These excluded
participants’ data were not used in power spectral density analyses due to compromised recordings (e.g., repeated
absence from sessions) but are shared for completeness and transparency. Code availability
All MATLAB preprocessing code is included in the code/ directory of both Poetry Assessment EEG Dataset 174
and Poetry Assessment EEG Dataset 275, available at OpenNeuro. Each dataset contains an identical version of
the script Preprocessing.m, which documents the complete EEG preprocessing pipeline applied to the raw data. Received: 24 July 2025; Accepted: 21 October 2025; Published: xx xx xxxx
References

### 1. Mar, R. A. The Neural Bases of Social Cognition and Story Comprehension. Annu. Rev. Psychol. 62, 103–134, https://doi.

org/10.1146/annurev-psych-120709-145406 (2011).

### 2. Holland, N. N. The Brain of Robert Frost: A Cognitive Approach to Literature. (Taylor & Francis Group, Milton, 1988).

### 3. Jacobs, A. M. Towards a neurocognitive poetics model of literary reading. in Cognitive Neuroscience of Natural Language Use

135–159 (Cambridge University Press, 2015).

### 4. Turner, F. & Pöppel, E. The Neural Lyre: Poetic Meter, the Brain, and Time. Poetry 142, 277–309 (1983).

### 5. Koelsch, S. & Siebel, W. A. Towards a neural basis of music perception. Trends in Cognitive Sciences 9, 578–584, https://doi.

org/10.1016/j.tics.2005.10.001 (2005).

### 6. Vuust, P., Heggli, O. A., Friston, K. J. & Kringelbach, M. L. Music in the brain. Nat Rev Neurosci 23, 287–305, https://doi.org/10.1038/

s41583-022-00578-5 (2022).

### 7. Brattico, E. & Pearce, M. The neuroaesthetics of music. Psychology of Aesthetics, Creativity, and the Arts 7, 48–61, https://doi.

org/10.1037/a0031624 (2013).

### 8. Boccia, M. et al. Where does brain neural activation in aesthetic responses to visual art occur? Meta-analytic evidence from

neuroimaging studies. Neuroscience & Biobehavioral Reviews 60, 65–71, https://doi.org/10.1016/j.neubiorev.2015.09.009 (2016).

### 9. Iigaya, K., Yi, S., Wahle, I. A., Tanwisuth, K. & O’Doherty, J. P. Aesthetic preference for art can be predicted from a mixture of low-

and high-level visual features. Nat Hum Behav 5, 743–755, https://doi.org/10.1038/s41562-021-01124-6 (2021). Fig. 5  Topographical maps of EEG power density across the five canonical frequency bands (delta, theta, alpha,
beta, gamma) for Haiku, Senryu, and Control conditions during early (0–5 s) and late (5–10 s) task intervals. These maps are presented as descriptive illustrations of scalp-level power distributions and serve as validation of
spatial resolution and signal quality. No inferential comparisons between conditions are reported, in line with
the journal’s guidelines. While visual inspection suggests similarities (e.g., between Haiku and Senryu), formal
statistical evaluation requires additional analysis (e.g., cluster-based permutation tests), which the dataset fully
enables but are beyond the scope of this descriptive report. Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/

### 10. Chatterjee, A. & Vartanian, O. Neuroscience of aesthetics: Neuroscience of aesthetics. Ann. N. Y. Acad. Sci. 1369, 172–194, https://

doi.org/10.1111/nyas.13035 (2016).

### 11. Mar, R. A. The neuropsychology of narrative: story comprehension, story production and their interrelation. Neuropsychologia 42,

1414–1434, https://doi.org/10.1016/j.neuropsychologia.2003.12.016 (2004).

### 12. Jääskeläinen, I. P., Klucharev, V., Panidi, K. & Shestakova, A. N. Neural Processing of Narratives: From Individual Processing to Viral

Propagation. Front. Hum. Neurosci. 14, 253, https://doi.org/10.3389/fnhum.2020.00253 (2020).

### 13. Hsu, C.-T., Jacobs, A. M., Altmann, U. & Conrad, M. The Magical Activation of Left Amygdala when Reading Harry Potter: An fMRI

Study on How Descriptions of Supra-Natural Events Entertain and Enchant. PLoS ONE 10, e0118179, https://doi.org/10.1371/
journal.pone.0118179 (2015).

### 14. Jacobs, A. M. Neurocognitive poetics: methods and models for investigating the neuronal and cognitive-affective bases of literature

reception. Front. Hum. Neurosci. 9, https://doi.org/10.3389/fnhum.2015.00186 (2015).

### 15. Wassiliwizky, E., Koelsch, S., Wagner, V., Jacobsen, T. & Menninghaus, W. The emotional power of poetry: neural circuitry,

psychophysiology and compositional principles. Social Cognitive and Affective Neuroscience 12, 1229–1240, https://doi.org/10.1093/
scan/nsx069 (2017).

### 16. O’Sullivan, N., Davis, P., Billington, J., Gonzalez-Diaz, V. & Corcoran, R. Shall I compare thee”: The neural basis of literary awareness,

and its benefits to cognition. Cortex 73, 144–157, https://doi.org/10.1016/j.cortex.2015.08.014 (2015).

### 17. Zeman, A. & Milton, F. Smith, Alicia & Rylance, Rick. By Heart: An fMRI study of brain activation by poetry and prose. Journal of

Consciousness Studies 20, 132–158 (2013).

### 18. Hollenstein, N. et al. ZuCo, a simultaneous EEG and eye-tracking resource for natural sentence reading. Sci Data 5, 180291, https://

doi.org/10.1038/sdata.2018.291 (2018).

### 19. Quach, B. M., Gurrin, C. & Healy, G. DERCo: A Dataset for Human Behaviour in Reading Comprehension Using EEG. Sci Data 11,

1104, https://doi.org/10.1038/s41597-024-03915-8 (2024).

### 20. Chen, J., Ro, T. & Zhu, Z. Emotion Recognition With Audio, Video, EEG, and EMG: A Dataset and Baseline Approaches. IEEE

Access 10, 13229–13242, https://doi.org/10.1109/ACCESS.2022.3146729 (2022).

### 21. Lee, M.-H. et al. EAV: EEG-Audio-Video Dataset for Emotion Recognition in Conversational Contexts. Sci Data 11, 1026, https://

doi.org/10.1038/s41597-024-03838-4 (2024).

### 22. Wang, S., Zhang, X., Zhang, J. & Zong, C. A synchronized multimodal neuroimaging dataset for studying brain language processing. Sci Data 9, 590, https://doi.org/10.1038/s41597-022-01708-5 (2022).

### 23. Armeni, K., Güçlü, U., Van Gerven, M. & Schoffelen, J.-M. A 10-hour within-participant magnetoencephalography narrative dataset

to test models of language comprehension. Sci Data 9, 278, https://doi.org/10.1038/s41597-022-01382-7 (2022).

### 24. Yasuda, K. Japanese Haiku: Its Essential Nature and History. (Tuttle Publishing, New York, 2011).

### 25. Hitsuwari, J. & Nomura, M. Comparison of ambiguity and aesthetic impressions in haiku poetry between experts and novices. Poetics 107, 101944, https://doi.org/10.1016/j.poetic.2024.101944 (2024).

### 26. Deluty, R. H. Senryu. Food, Culture & Society 9, 355–359, https://doi.org/10.2752/155280106778813251 (2006).

### 27. Pierides, S., Muller, H. J., Kacian, J., Gunther, F. & Geyer, T. Haiku and the brain: an exploratory study. Juxtapositions: The Journal of

Haiku Research and Scholarship 3 (2017).

### 28. Geyer, T. et al. Reading English-language haiku: An eye-movement study of the ‘cut effect’. Journal of eye movement research 13,

https://doi.org/10.16910/jemr.13.2.2 (2020).

### 29. Leder, H., Belke, B., Oeberst, A. & Augustin, D. A model of aesthetic appreciation and aesthetic judgments. British J of Psychology 95,

489–508, https://doi.org/10.1348/0007126042369811 (2004).

### 30. Leder, H. & Nadal, M. Ten years of a model of aesthetic appreciation and aesthetic judgments: The aesthetic episode – Developments

and challenges in empirical aesthetics. British J of Psychology 105, 443–464, https://doi.org/10.1111/bjop.12084 (2014).

### 31. Chatterjee, A. & Vartanian, O. Neuroaesthetics. Trends in Cognitive Sciences 18, 370–375, https://doi.org/10.1016/j.tics.2014.03.003

(2014).

### 32. Vessel, E. A., Starr, G. G. & Rubin, N. The brain on art: intense aesthetic experience activates the default mode network. Front. Hum. Neurosci. 6, https://doi.org/10.3389/fnhum.2012.00066 (2012).

### 33. Schindler, I. et al. Measuring aesthetic emotions: A review of the literature and a new assessment tool. PLoS ONE 12, e0178899,

https://doi.org/10.1371/journal.pone.0178899 (2017).

### 34. Menninghaus, W. & Wallot, S. What the eyes reveal about (reading) poetry. Poetics 85, 101526, https://doi.org/10.1016/j.

poetic.2020.101526 (2021).

### 35. Kuehnast, M., Wagner, V., Wassiliwizky, E., Jacobsen, T. & Menninghaus, W. Being moved: linguistic representation and conceptual

structure. Front. Psychol. 5, https://doi.org/10.3389/fpsyg.2014.01242 (2014).

### 36. Wassiliwizky, E., Wagner, V., Jacobsen, T. & Menninghaus, W. Art-elicited chills indicate states of being moved. Psychology of

Aesthetics, Creativity, and the Arts 9, 405–416, https://doi.org/10.1037/aca0000023 (2015).

### 37. Obermeier, C. et al. Aesthetic and Emotional Effects of Meter and Rhyme in Poetry. Front. Psychology 4, https://doi.org/10.3389/

fpsyg.2013.00010 (2013).

### 38. Obermeier, C. et al. Aesthetic appreciation of poetry correlates with ease of processing in event-related potentials. Cogn Affect Behav

Neurosci 16, 362–373, https://doi.org/10.3758/s13415-015-0396-x (2016).

### 39. Runco, M. A. & Jaeger, G. J. The Standard Definition of Creativity. Creativity Research Journal 24, 92–96, https://doi.org/10.1080/10

400419.2012.650092 (2012).

### 40. Corazza, G. E., Agnoli, S. & Mastria, S. The Dynamic Creativity Framework: Theoretical and Empirical Investigations. European

Psychologist 27, 191–206, https://doi.org/10.1027/1016-9040/a000473 (2022).

### 41. Corazza, G. E. Potential Originality and Effectiveness: The Dynamic Definition of Creativity. Creativity Research Journal 28,

258–267, https://doi.org/10.1080/10400419.2016.1195627 (2016).

### 42. Acar, S., Burnett, C. & Cabra, J. F. Ingredients of Creativity: Originality and More. Creativity Research Journal 29, 133–144, https://

doi.org/10.1080/10400419.2017.1302776 (2017).

### 43. Runco, M. A. & Charles, R. E. Judgments of originality and appropriateness as predictors of creativity. Personality and Individual

Differences 15, 537–546, https://doi.org/10.1016/0191-8869(93)90337-3 (1993).

### 44. Fink, A. & Benedek, M. EEG alpha power and creative ideation. Neuroscience & Biobehavioral Reviews 44, 111–123, https://doi.

org/10.1016/j.neubiorev.2012.12.002 (2014).

### 45. Silvia, P. J. et al. Assessing creativity with divergent thinking tasks: Exploring the reliability and validity of new subjective scoring

methods. Psychology of Aesthetics, Creativity, and the Arts 2, 68–85, https://doi.org/10.1037/1931-3896.2.2.68 (2008).

### 46. Rominger, C. et al. Functional coupling of brain networks during creative idea generation and elaboration in the figural domain. NeuroImage 207, 116395, https://doi.org/10.1016/j.neuroimage.2019.116395 (2020).

### 47. Cotter, K. N., Ivcevic, Z. & Moeller, J. Person-oriented profiles of originality and fluency in divergent thinking responses. Journal of

Research in Personality 86, 103941, https://doi.org/10.1016/j.jrp.2020.103941 (2020).

### 48. Agnoli, S., Zanon, M., Mastria, S., Avenanti, A. & Corazza, G. E. Predicting response originality through brain activity: An analysis

of changes in EEG alpha power during the generation of alternative ideas. NeuroImage 207, 116385, https://doi.org/10.1016/j.
neuroimage.2019.116385 (2020). Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/

### 49. Chaudhuri, S., Maura, D., Johnson, D., Beaty, R. E. & Bhattacharya, J. Evaluation of Poetic Creativity: Predictors and the Role of

Expertise - A Multilevel Approach. Psychology of Aesthetics, Creativity, and the Arts,19(6), 1643–1654, https://doi.org/10.1037/
aca0000649 (2025).

### 50. Chaudhuri, S., Pickering, A. & Bhattacharya, J. Evaluating Poetry: Navigating the Divide between Aesthetical and Creativity

Judgments. Journal of Creative Behavior 59, e683, https://doi.org/10.1002/jocb.683 (2025).

### 51. Chaudhuri, S. & Bhattacharya, J. The Power of Brevity: Creativity Judgments in English Language Haiku and Senryu Poetry. Journal

of Creative Behavior 59, e70018, https://doi.org/10.1002/jocb.70018 (2025).

### 52. Mehl, K., Gugliano, M. & Belfi, A. M. The role of imagery and emotion in the aesthetic appeal of music, poetry, and paintings. Psychology of Aesthetics, Creativity, and the Arts https://doi.org/10.1037/aca0000623 10.1037/aca0000623 (2023).

### 53. Belfi, A. M., Vessel, E. A. & Starr, G. G. Individual ratings of vividness predict aesthetic appeal in poetry. Psychology of Aesthetics, Creativity, and the Arts 12, 341–350, https://doi.org/10.1037/aca0000153 (2018).

### 54. Hitsuwari, J. & Nomura, M. Ambiguity and beauty: Japanese-German cross-cultural comparisons on aesthetic evaluation of haiku

poetry. Psychology of Aesthetics, Creativity, and the Arts 18, 1004–1013, https://doi.org/10.1037/aca0000497 (2024).

### 55. Faul, F., Erdfelder, E., Buchner, A. & Lang, A.-G. Statistical power analyses using G*Power 3.1: Tests for correlation and regression

analyses. Behavior Research Methods 41, 1149–1160, https://doi.org/10.3758/BRM.41.4.1149 (2009).

### 56. Watson, D., Clark, L. A. & Tellegen, A. Development and validation of brief measures of positive and negative affect: The PANAS

scales. Journal of Personality and Social Psychology 54, 1063–1070, https://doi.org/10.1037/0022-3514.54.6.1063 (1988).

### 57. DeYoung, C. G., Quilty, L. C. & Peterson, J. B. Between facets and domains: 10 aspects of the Big Five. Journal of Personality and

Social Psychology 93, 880–896, https://doi.org/10.1037/0022-3514.93.5.880 (2007).

### 58. Litman, J. A. & Spielberger, C. D. Measuring Epistemic Curiosity and Its Diversive and Specific Components. Journal of Personality

Assessment 80, 75–86, https://doi.org/10.1207/S15327752JPA8001_16 (2003).

### 59. Marks, D. F. Visual Imagery Differences In The Recall of Pictures. British J of Psychology 64, 17–24, https://doi.

org/10.1111/j.2044-8295.1973.tb01322.x (1973).

### 60. Halpern, A. R. Differences in auditory imagery self-report predict neural and behavioral outcomes. Psychomusicology: Music, Mind,

and Brain 25, 37–47, https://doi.org/10.1037/pmu0000081 (2015).

### 61. Brown, K. W. & Ryan, R. M. The benefits of being present: Mindfulness and its role in psychological well-being. Journal of Personality

and Social Psychology 84, 822–848, https://doi.org/10.1037/0022-3514.84.4.822 (2003).

### 62. Schlotz, W. et al. The Aesthetic Responsiveness Assessment (AReA): A screening tool to assess individual differences in

responsiveness to art in English and German. Psychology of Aesthetics, Creativity, and the Arts 15, 682–696, https://doi.org/10.1037/
aca0000348 (2021).

### 63. Opler, M. K. & Obayashi, F. Senryu Poetry as Folk and Community Expression. The Journal of American Folklore 58, 1, https://doi.

org/10.2307/535330 (1945).

### 64. Light Verse from the Floating World: An Anthology of Premodern Japanese Senryu. (Columbia University Press, New York, N. Y, 1999).

### 65. Müller, H., Geyer, T., Günther, F., Kacian, J. & Pierides, S. Reading English-Language Haiku: Processes of Meaning Construction

Revealed by Eye Movements. J. Eye Mov. Res. 10, 1–33, https://doi.org/10.16910/jemr.10.1.4 (2017).

### 66. Hitsuwari, J. & Nomura, M. How Individual States and Traits Predict Aesthetic Appreciation of Haiku Poetry. Empirical Studies of

the Arts 40, 81–99, https://doi.org/10.1177/0276237420986420 (2022).

### 67. Rinker, T. W. sentimentr: Calculate Text Polarity Sentiment.version 2.9.1 (2021).

### 68. Peirce, J. W. PsychoPy—Psychophysics software in Python. Journal of Neuroscience Methods 162, 8–13, https://doi.org/10.1016/j.

jneumeth.2006.11.017 (2007).

### 69. Barry, R. J., Clarke, A. R., Johnstone, S. J., Magee, C. A. & Rushby, J. A. EEG differences between eyes-closed and eyes-open resting

conditions. Clinical Neurophysiology 118, 2765–2773, https://doi.org/10.1016/j.clinph.2007.07.028 (2007).

### 70. Costumero, V., Bueichekú, E., Adrián-Ventura, J. & Ávila, C. Opening or closing eyes at rest modulates the functional connectivity

of V1 with default and salience networks. Sci Rep 10, 9137, https://doi.org/10.1038/s41598-020-66100-y (2020).

### 71. Wang, Y. et al. Open Eyes Increase Neural Oscillation and Enhance Effective Brain Connectivity of the Default Mode Network: Resting-State Electroencephalogram Research. Front. Neurosci. 16, 861247, https://doi.org/10.3389/fnins.2022.861247 (2022).

### 72. Essl, M. & Rappelsberger, P. EEG cohererence and reference signals: experimental results and mathematical explanations. Med. Biol. Eng. Comput. 36, 399–406, https://doi.org/10.1007/BF02523206 (1998).

### 73. Delorme, A. & Makeig, S. EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent

component analysis. Journal of Neuroscience Methods 134, 9–21, https://doi.org/10.1016/j.jneumeth.2003.10.009 (2004).

### 74. Chaudhuri, S. and Bhattacharya, J. Poetry Assessment EEG Dataset 1. OpenNeuro https://doi.org/10.18112/openneuro.ds006648.

v1.0.0 (2025).

### 75. Chaudhuri, S. and Bhattacharya, J. Poetry Assessment EEG Dataset 2. OpenNeuro https://doi.org/10.18112/openneuro.ds006647.

v1.0.1 (2025).

### 76. Tan, J., Di Bernardi Luft, C. & Bhattacharya, J. The After-Glow of Flow: Neural Correlates of Flow in Musicians. Creativity Research

Journal 36, 469–490, https://doi.org/10.1080/10400419.2023.2277042 (2024).

### 77. Lee, E.-J., Bhattacharya, J., Sohn, C. & Verres, R. Monochord sounds and progressive muscle relaxation reduce anxiety and improve

relaxation during chemotherapy: A pilot EEG study. Complementary Therapies in Medicine 20, 409–416, https://doi.org/10.1016/j.
ctim.2012.07.002 (2012).

### 78. Franko, E. et al. Quantitative EEG parameters correlate with the progression of human prion diseases. J Neurol Neurosurg Psychiatry

87, 1061–1067, https://doi.org/10.1136/jnnp-2016-313501 (2016).

### 79. Hashim, S., Küssner, M. B., Weinreich, A. & Omigie, D. The neuro-oscillatory profiles of static and dynamic music-induced visual

imagery. International Journal of Psychophysiology 199, 112309, https://doi.org/10.1016/j.ijpsycho.2024.112309 (2024).

### 80. Carrus, E., Koelsch, S. & Bhattacharya, J. Shadows of music–language interaction on low frequency brain oscillatory patterns. Brain

and Language 119, 50–57, https://doi.org/10.1016/j.bandl.2011.05.009 (2011).

### 81. Mastria, S. et al. Clustering and switching in divergent thinking: Neurophysiological correlates underlying flexibility during idea

generation. Neuropsychologia 158, 107890, https://doi.org/10.1016/j.neuropsychologia.2021.107890 (2021). Acknowledgements
The authors received no funding for this work. Author contributions
S. C. and J. B. conceived the experimental design; S. C. conducted the experiment and data analysis; J. B. and S. C.
wrote the paper; J. B. provided overall research supervision. Competing interests
The authors declare no competing interests. Scientific Data | (2025) 12:1898 | https://doi.org/10.1038/s41597-025-06189-w
www.nature.com/scientificdata
www.nature.com/scientificdata/
Additional information
Correspondence and requests for materials should be addressed to J. B. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Open Access This article is licensed under a Creative Commons Attribution 4.0 International
License, which permits use, sharing, adaptation, distribution and reproduction in any medium or
format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Cre-
ative Commons licence, and indicate if changes were made. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the
material. If material is not included in the article’s Creative Commons licence and your intended use is not per-
mitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the
copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.
© The Author(s) 2025
