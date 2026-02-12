# neural-speech-tracking-contribution-of-lip-movemen

Neural Speech Tracking Contribution
of Lip Movements Predicts Behavioral
Deterioration When the Speaker ’s
Mouth Is Occluded
Patrick Reisinger,1
 Marlies Gillis,2
 Nina Suess,1
 Jonas Vanthornhout,2
Chandra Leon Haider, 1
 Thomas Hartmann, 1
 Anne Hauswald,1
Konrad Schwarz,3
 Tom Francart,2† and
 Nathan Weisz1,4†
1Department of Psychology, Centre for Cognitive Neuroscience, Paris-Lodron-University of
Salzburg, Salzburg 5020, Austria, 2Experimental Oto-Rhino-Laryngology, Department of
Neurosciences, Leuven Brain Institute, KU Leuven, Leuven 3000, Belgium, 3MED-EL GmbH,
Innsbruck 6020, Austria, and 4Neuroscience Institute, Christian Doppler University Hospital,
Paracelsus Medical University Salzburg, Salzburg 5020, Austria
Abstract
Observing lip movements of a speaker facilitates speech understanding, especially in challenging listening
situations. Converging evidence from neuroscientificstudies shows stronger neural responses to audiovisual
stimuli compared with audio-only stimuli. However, the interindividual variability of this contribution of lip
movement information and its consequences on behavior are unknown. We analyzed source-localized mag-
netoencephalographic responses from 29 normal-hearingparticipants (12 females) listening to audiovisual
speech, both with and without the speaker wearing a surgical face mask, and in the presence or absence of
a distractor speaker. Using temporal response functions to quantify neural speech tracking, we show that
neural responses to lip movements are, in general, enhanced when speech is challenging. After controlling
for speech acoustics, we show that lip movements contribute to enhanced neural speech tracking, partic-
ularly when a distractor speaker is present. However, the extent of this visual contribution to neural speech
tracking varied greatly among participants. Probing the behavioral relevance, we demonstrate that individ-
uals who show a higher contribution of lip movements in terms of neural speech tracking show a stronger
drop in comprehension and an increase in perceived difficulty when the mouth is occluded by a surgical face
mask. In contrast, no effect was found when the mouth was not occluded. We provide novel insights on how
the contribution of lip movements in terms of neural speech tracking varies among individuals and its beha-
vioral relevance, revealing negative consequences when visual speech is absent. Our results also offer
potential implications for objective assessments of audiovisual speech perception.
Key words: audiovisual speech; lip movements; MEG; neural tracking; temporal response functions;
TRF
Significance Statement
In complex auditory environments, simultaneous conversations pose a challenge to speech compre-
hension. We investigated on a neural level how lip movements aid in such situations and what the
behavioral consequences are, especially when lip information is occluded with a face mask. Using
magnetoencephalographic responses from participants listening to audiovisual speech, we show
that observing lip movements enhances neural speech tracking and participants who rely more on
lip movements show behavioral deterioration when the speaker wears a face mask. Remarkably,
this is not the case when no face mask was worn by the speaker. Our findings reveal interindividual
differences in the contribution of lip movements to neural speech tracking, with potential applications in
objective assessments of audiovisual speech perception.
Continued on next page.
Received Aug. 25, 2024; accepted Dec.
9, 2024.
K.S. is an employee of MED-EL GmbH.
All other authors declare no competing
ﬁnancial interests.
Author contributions: N.S., C.L.H., and
N.W. designed research; P.R. and
C.L.H. performed research; M.G., J.V.,
and T.H. contributed unpublished
reagents/analytic tools; P.R., M.G.,
N.S., J.V., C.L.H., and T.H. analyzed
data; P.R., M.G., N.S., J.V., C.L.H.,
T.H., A.H., K.S., T.F., and N.W. wrote
the paper.
This research was funded in whole or in
part by the Austrian Science Fund
(FWF; 10.55776/W1233). For open
access purposes, we have applied a
CC BY public copyright license to any
author-accepted manuscript version
arising from this submission. P.R. is
supported by FWF (Doctoral College
“Imaging the Mind”; W 1233-B), as well
as N.S. ( “Audiovisual speech
entrainment in deafness ”; P31230) and
C.L.H. (“Impact of face masks on
speech comprehension ”; P34237).
Research Article: New Research
Cognition and Behavior
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 1 of 16
Introduction
Face masks are an important tool in preventing the spread of contagious diseases such
as COVID-19 ( Chu et al., 2020 ; Suñer et al., 2022 ). However, as many have subjectively
experienced ﬁrsthand, the use of face masks also impairs speech perception, and not
only by attenuating sound. More importantly, they occlude facial expressions, such as
lip movements ( Brown et al., 2021 ; Rahne et al., 2021 ), that provide visual information
for a relevant speech stream. This is particularly critical when speech is challenging,
such as in the classic cocktail party situation, where conversations are happening simul-
taneously ( Cherry, 1953 ). Ideally, visual information is available to aid in such situations,
with numerous studies demonstrating that visual speech features enhance the under-
standing of degraded auditory input ( Sumby and Pollack, 1954 ; Grant and Seitz, 2000 ;
Ross et al., 2007 ; Remez, 2012 ). Among visual speech features, lip movements are the
most important, playing a crucial role in the perception of challenging speech ( Erber,
1975; Peelle and Sommers, 2015 ). However, substantial interindividual differences in
lip-reading performance among normal, as well as hearing-impaired, populations have
been shown in previous studies ( Suess et al., 2022b ; for a review see Summerﬁeld
et al., 1992 ). Despite our imperfect lip-reading abilities, the human brain effectively uses
lip movements to facilitate the perception of challenging speech, with the neural mecha-
nisms and regions involved still under debate ( Ross et al., 2022 ; Zhang and Du, 2022 ).
A suitable method for studying the neural responses to audiovisual speech is neural
speech tracking ( Obleser and Kayser, 2019 ; Brodbeck and Simon, 2020 ). This method
typically aims to predict the neural response to one or more stimulus features via so-called
temporal response functions (TRFs; Crosse et al., 2021 ). The TRF approach has so far
extended our understanding of speech processing from acoustic features ( Lalor et al.,
2009) to higher-level linguistic features ( Broderick et al., 2018 ; Brodbeck et al., 2018a ;
Gillis et al., 2021 ).
Previous studies have shown beneﬁcial effects of visual speech on the representation of
speech in the brain. A magnetoencephalography (MEG) study by Park et al. (2016) showed
enhanced entrainment between lip movements and speech-related brain areas when
congruent audiovisual speech was presented. Other studies have shown that the incorpo-
ration of visual speech enhances the ability of the brain to track acoustic speech
(Golumbic et al., 2013 ; Crosse et al., 2015 , 2016b). Interestingly, when silent lip move-
ments are presented, the visual cortex also follows the unheard acoustic speech envelope
(Hauswald et al., 2018) or unheard spectral ﬁne details (Suess et al., 2022a). Despite these
ﬁndings, two questions remain unanswered: First, it is unknown to which extent individu-
als vary in their unique contribution of lip movements to neural speech tracking. Given the
aforementioned interindividual differences in lip-reading performance, we hypothesize a
high degree of variability in this contribution. Second, it is unknown if the unique contribu-
tion of lip movements is of behavioral relevance, as, for example, when the lips are
occluded with a face mask, as has been common during the COVID-19 pandemic.
Given the negative impact of face masks on behavioral measures ( Rahne et al., 2021 ;
Toscano and Toscano, 2021 ; Truong et al., 2021 ), we expect the following relationship:
Individuals who show a higher unique contribution of lip movements should also show
poorer behavioral outcomes when no lip movements are available, as they are deprived
of critical visual information.
Using MEG and an audiovisual speech paradigm with one or two speakers, we probed
the unique contribution of lip movements and its behavioral relevance. Utilizing a
state-of-the-art neural tracking framework with source-localized TRFs ( Fig. 1 C), we
show that lip movements elicit stronger neural responses when speech is dif
ﬁcult com-
pared with when it is clear. Additionally, we show that the neural tracking of lip movements
is enhanced in multispeaker settings. When controlled for acoustic speech features, the
obtained unique contribution of lip movements is, in general, more enhanced in the multi-
speaker condition, with substantial interindividual variability. Using Bayesian modeling,
we show that acoustic speech tracking is related to behavioral measures. Crucially, we
demonstrate that individuals who show a higher unique contribution of lip movements
show a stronger drop in comprehension and report a higher subjective dif ﬁculty when
the mouth is occluded by a surgical face mask. In terms of neural tracking, our results sug-
gest that individuals show a unique contribution of lip movements in a highly variable man-
ner. We also establish a novel link between the neural unique contribution of visual speech
and behavior when no lip movement information is available.
P.R. is also supported by the Austrian
Research Promotion Agency (FFG;
BRIDGE 1 project “SmartCIs”; 871232).
M.G. is supported by a Strategic Basic
Research Grant by the Research
Foundation Flanders (FWO, Grant No.
1SA0620N). J.V. is supported by a
postdoctoral grant provided by the
FWO (Grant No. 1290821). We thank
Juliane Schubert for the stimulus
recordings and Sarah Danböck for her
helpful methodological input.
†T.F. and N.W. shared last authorship.
Correspondence should be addressed
to Nathan Weisz at nathan.weisz@plus.
ac.at.
Copyright © 2025 Reisinger et al.
This is an open-access article
distributed under the terms of the
Creative Commons Attribution 4.0
International license , which permits
unrestricted use, distribution and
reproduction in any medium provided
that the original work is properly
attributed.
Research Article: New Research 2 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 2 of 16
Materials and Methods
Participants. The data were collected as part of a recent study ( Haider et al., 2022 ), in which 30 native speakers of
German participated. One participant was excluded because signal source separation could not be applied to the
MEG dataset due to ﬁle corruption. This led to a ﬁnal sample size of 29 participants aged between 22 and 41 years
(12 females; M
age = 26.79 years; SD age = 4.87 years). All participants reported normal vision and hearing (thresholds did
not exceed 25 dB HL at any frequency from 125 to 8,000 Hz), the latter veri ﬁed by a standard clinical audiometer
(AS608 Basic; Interacoustics A/S). Additional exclusion criteria included nonremovable magnetic objects and any psychi-
atric or neurologic history. All participants signed an informed consent and were reimbursed at a rate of 10 € per hour.
The experimental protocol was approved by the ethics committee of the Paris-Lodron-University of Salzburg and was
conducted in accordance with the Declaration of Helsinki.
Stimuli and experimental design. The experimental procedure was implemented in MATLAB 9.10 (The MathWorks)
using custom scripts. Presentation of stimuli and response collection was achieved with the Objective Psychophysics
Toolbox (o_ptb; Hartmann and Weisz, 2020 ), which adds a class-based abstraction layer onto the Psychophysics
Toolbox version 3.0.16 ( Brainard, 1997; Pelli, 1997; Kleiner et al., 2007 ). Stimuli and triggers were generated and emitted
via the VPixx system (DATAPixx2 display driver, PROPixx DLP LED projector, RESPONSEPixx response box; VPixx
Technologies). Videos were back-projected onto a translucent screen with a screen diagonal of 74 cm ( ∼110 cm in front
of the participants), with a refresh rate of 120 Hz and a resolution of 1,920 × 1,080 pixels. Timings were measured with the
Black Box ToolKit v2 (The Black Box ToolKit) to ensure accurate stimulus presentation and triggering.
The audiovisual stimuli were excerpts from four German stories, two of each read out loud by a female or male speaker
(female: “Die Schokoladenvilla - Zeit des Schicksals. Die Vorgeschichte zu Band 3 ” by Maria Nikolai , “Die Federn des
Windes” by Manuel Timm; male: “Das Gestüt am See. Charlottes großer Traum ” by Paula Mattis and “Gegen den
Willen der Väter ” by Klaus Tiberius Schmidt). A Sony NEX-FS100 (Sony) camera with a sampling rate of 25 Hz and a
RØDE NTG2 microphone (RØDE Microphones) with a sampling rate of 48 kHz were used to record the stimuli. Each of
the four stories was recorded twice, once with and once without a surgical face mask (type IIR three-layer disposable med-
ical mask). These eight videos were cut into 10 segments of ∼1 min each (M = 64.29 s; SD = 4.87 s), resulting in 80 videos.
In order to rule out sex-speciﬁc effects, 40 videos (20 with a female speaker and 20 with a male speaker) were presented to
each participant. The speakers’ syllable rates were analyzed using Praat (Boersma, 2001; de Jong and Wempe, 2009) and
varied between 3.7 and 4.6 Hz ( M = 4.1 Hz). The audio-only distractor speech consisted of prerecorded audiobooks
(Schubert et al., 2023 ), read by either a female or a male speaker. All audio ﬁles were normalized using ffmpeg-normalize
version 1.19.1 (running on Python 3.9.7) with default options.
Before the experiment, a standard clinical audiometry was performed (for details, see above, Participants). The MEG
measurement started with a 5 min resting-state recording (not analyzed in this manuscript). Next, the participant ’s individ-
ual hearing threshold was determined in order to adjust the stimulation volume. If the participant reported that the stim-
ulation was not loud enough or comfortable, the volume was manually adjusted to the participant ’s requirements. Hearing
threshold levels ranged from −91.76 db (RMS) to −68.78 db (RMS) [ M = −80.57 db (RMS); SD = 4.20 db (RMS)].
The actual experiment consisted of four stimulation blocks, one for each of the four stories, with two featuring each sex.
Each story was presented as a block of 10 ∼1 min trials (ranging from 0.93 to 1.27 min) in a chronological order to preserve
the story content ( Fig. 1 A). In every block, a same-sex audio –only distractor speaker was added to three randomly
selected trials, with a 5 s delay and volume equal to the target speaker. The resulting ratio of 30% multispeaker trials
and 70% single-speaker trials per block was chosen because of a different data analysis method in Haider et al.
(2022). The distractor speech started with a delay of 5 s to give participants time to attend the target speaker. In two ran-
domly selected blocks, the target speaker wore a face mask (only the corresponding behavioral data were used here; see
below, Statistical analysis and Bayesian modeling). Two unstandardized correct or wrong statements about semantic
content were presented after each trial to assess comprehension and to maintain attention ( Fig. 1A
). On four occasions
in each block, participants also rated subjective dif ﬁculty and engagement on a ﬁve-point Likert scale (not depicted in
Fig. 1 A). The participants responded by pressing buttons. The blocks were presented randomly, and the total duration
of the experiment was ∼2 h, including preparation.
MEG data acquisition and preprocessing. Before entering the magnetically shielded room, ﬁve head position indicator
(HPI) coils were applied on the scalp. Electrodes for electrooculography (vertical and horizontal eye movements) and elec-
trocardiography were also applied (recorded data not used here). Fiducial landmarks (nasion and left/right preauricular
points), the HPI locations, and ∼300 head shape points were sampled with a Polhemus FASTRAK digitizer (Polhemus).
Magnetic brain activity was recorded with a Neuromag Triux whole-head MEG system (MEGIN Oy, Espoo, Finland)
using a sampling rate of 1,000 Hz (hardware ﬁlters, 0.1 –330 Hz). The signals were acquired from 102 magnetometers
and 204 orthogonally placed planar gradiometers at 102 different positions. The system is placed in a standard passive
magnetically shielded room (AK3b; Vacuumschmelze).
A signal space separation ( Taulu and Kajola, 2005 ; Taulu and Simola, 2006 ) algorithm implemented in MaxFilter ver-
sion 2.2.15 provided by the MEG manufac turer was used. The algorithm removes external noise from the MEG signal
Research Article: New Research 3 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 3 of 16
Figure 1. Experimental design, behavioral results, and analysis framework. A, Each block consisted of 10 ∼1 min trials of continuous audiovisual speech by
either a female or male speaker (single-speaker condition). In 30% of these 10 trials, a same-sex audio –only distractor speaker was added (multispeaker
condition). After every block, two comprehension statements had to be rated as correct or wrong. B, Comprehension was lower in the multispeaker con-
dition than in the single-speaker condition ( p = 0.003; rC = 0.64). Subjective difﬁculty ratings, reported on a ﬁve-point Likert scale, were higher in the multi-
speaker condition ( p = 9.00 × 10−6; rC = −0.95). The reported engagement was lower in the multispeaker condition ( p = 0.024; rC = 0.62). The black dots
Research Article: New Research 4 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 4 of 16
(mainly 16.6, and 50 Hz, plus harmonics) and realigns the data to a common standard head position (to [0 0 40] mm,
-trans default MaxFilter parameter) across different blocks, bas ed on the measured head position at the beginning of
each block.
Preprocessing of the raw data was done in MATLAB 9.8 using the FieldTrip toolbox (revision f7adf3ab0; Oostenveld
et al., 2011 ). A low-pass ﬁlter of 10 Hz (hamming-windowed sinc FIR ﬁlter; onepass-zerophase; order, 1320; transition
width, 2.5 Hz) was applied, and the data were downsampled to 100 Hz. Afterward, a high-pass ﬁlter of 1 Hz (hamming-
windowed sinc FIR ﬁlter; onepass-zerophase; order, 166; transition width, 2.0 Hz) was applied.
Independent component analysis (ICA) was used to remove eye and cardiac artifacts (data were ﬁltered between 1 and
100 Hz; sampling rate, 1,000 Hz) via the infomax algorithm (“runica” implementation in EEGLAB; Bell and Sejnowski, 1995;
Delorme and Makeig, 2004) applied to a random block of the main experiment. Prior to the ICA computation, we performed
a principal component analysis with 50 components in order to ease the convergence of the ICA algorithm. After visual
identiﬁcation of artifact-related components, an average of 2.38 components per participant were removed (SD = 0.68).
The cleaned data were epoched into trials that matched the length of the audiovisual stimuli. To account for an auditory
stimulus delay introduced by the tubes of the sound system, the data were shifted by 16.5 ms. In the multispeaker con-
dition, the ﬁrst 5 s of data were removed to match the onset of the distractor speech. The last eight trials were removed to
equalize the data length between the single-speaker and multispeaker conditions. To prepare the data for the following
steps, the trials in each condition were concatenated. This resulted in a data length of ∼6 min per condition.
Source localization. Source projection of the data was done with MNE-Python 1.1.0 running on Python 3.9.7 ( Gramfort
et al., 2013 , 2014). A semiautomatic coregistration pipeline was used to coregister the FreeSurfer “fsaverage” template
brain (Fischl, 2012) to each participant’s head shape. After an initial ﬁt using the three ﬁducial landmarks, the coregistration
was reﬁned with the iterative closest point algorithm ( Besl and McKay, 1992 ). Head shape points that were >5 mm away
from the scalp were automatically omitted. The subsequent ﬁnal ﬁt was visually inspected to con ﬁrm its accuracy. This
semiautomatic approach performs comparably to manual coregistration pipelines ( Houck and Claus, 2020 ).
A single-layer boundary element model (BEM; Akalin-Acar and Gençer, 2004 ) was computed to create a BEM solution
for the “fsaverage” template brain. Next, a volumetric source space with a grid of 7 mm was de ﬁned, containing a total of
5,222 sources (Kulasingham et al., 2020). In order to remove nonrelevant regions and shorten computation times, subcor-
tical structures along the midline were removed, reducing the source space to 3,053 sources (similar to Das et al., 2020 ).
Subsequently, the forward operator (i.e., lead ﬁeld matrix) was computed using the individual coregistrations, the BEM,
and the volume source space.
Afterward, the data were projected to the deﬁned sources using the minimum norm estimate (MNE) method (Hämäläinen
and Ilmoniemi, 1994 ). MNE is known to be biased toward super ﬁcial sources, which can be reduced by applying depth
weighting with a coefﬁcient between 0.6 and 0.8 ( Lin et al., 2006). For creating the MNE inverse operator, depth weighting
with a coef ﬁcient of 0.8 was used ( Brodbeck et al., 2018a ). The required noise covariance matrix was estimated with an
empty-room MEG recording relative to the participant ’s measurement date with the same preprocessing settings as the
MEG data of the actual experiment (see above, MEG data acquisition and preprocessing). The MNE inverse operator was
then applied to the concatenated MEG data with ℓ2 regularization [signal-to-noise ratio (SNR) = 3 dB,
l2 = 1
SNR2 ] and
three free-orientation dipoles orthogonally at each source.
Extraction of stimulus features. Since the focus of this study is on audiovisual speech, we extracted acoustic (spectro-
grams and acoustic onsets) and visual (lip movements) speech features from the stimuli (Fig. 1C). The spectrograms of the
auditory stimuli were obtained using the Gammatone Filterbank Toolkit 1.0 (Heeris, 2013), with frequency cutoffs at 20 and
5,000 Hz, 256 ﬁlter channels, and a window time of 0.01 s. This toolkit computes a spectrogram representation on the
basis of a set of gammatone ﬁlters which are inspired by the human auditory system ( Slaney, 1998 ). The resulting ﬁlter
outputs with logarithmic center frequencies were averaged into eight frequency bands (frequencies <100 Hz were omit-
ted; Gillis et al., 2021 ). Each frequency band was scaled with exponent 0.6 ( Biesmans et al., 2017 ) and downsampled to
100 Hz, which is the same sampling frequency as the preprocessed MEG data.
Acoustic onset representations were calculated for each frequency band of the spectrograms using an auditory edge
detection model (Fishbach et al., 2001). The resulting spectrograms of the acoustic onsets are valuable predictors of MEG
/shortleftarrow
represent the mean, and the bars represent the standard error of the mean (SEM). C, Three stimulus features (spectrogram, acoustic onsets, and lip move-
ments) extracted from the audiovisual stimuli are shown for an example sentence. Higher values in the lip area unit represent a wider opening of the mou th
and vice versa. Three forward models were calculated: (1) one using only acoustic features, (2) one using only lip movements, and (3) one combining all
features. Together with the corresponding source-localized MEG data, the boosting algorithm was used to calculate the models. Exemplary minimum-
norm source estimates are shown for a representative participant. The resulting TRFs (a.u.) and neural tracking (expressed as Pearson ’s r) were analyzed
in fROIs, obtained either via the acoustic or lip model of the multispeaker condition. The TRFs and prediction accuracies shown are from a representat ive
participant reﬂecting the group-level results. To obtain the unique contribution of lip movements, we controlled acoustic features by subtracting the pre-
diction accuracies in an acoustic + lip fROI of the acoustic model from the combined model. The unique contribution of lip movements was expressed as a
percentage change. *p < 0.05; **p < 0.01; ***p < 0.001.
Research Article: New Research 5 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 5 of 16
responses to speech stimuli ( Daube et al., 2019 ; Brodbeck et al., 2020 ). A delay layer with 10 delays from 3 to 5 ms, a
saturation scaling factor of 30, and a receptive ﬁeld based on the derivative of a Gaussian window (SD = 2 ms) were
used (Gillis et al., 2021 ). Each frequency band was downsampled to 100 Hz.
The lip movements of every speaker were extracted from the videos with a MATLAB script adapted from Suess et al.
(2022a; originally by Park et al., 2016). Within the lip, contour, the area, and the horizontal and vertical axis were calculated.
Only the area was used for the analysis, which leads to results comparable with using the vertical axis ( Park et al., 2016 ).
The lip area signal was upsampled from 25 to 100 Hz using FFT-based interpolation.
Forward models. A linear forward modeling approach was used to predict the MEG response to the aforementioned
stimulus features (Fig. 1C). These approaches are based on the idea that the brain’s response to a stimulus is a continuous
function in time ( Lalor et al., 2006 ). The boosting algorithm ( David et al., 2007 ), implemented in eelbrain 0.38 (running on
Python 3.9.7; Brodbeck et al., 2023 ), was used to predict MNE source-localized MEG responses to stimulus features
(“MNE-boosting”; Brodbeck et al., 2018b ). For multiple stimulus features, the linear forward model can be formulated
as follows:
ˆyt =
∑n
i=0
∑tmax
t=tmin
hi,txi,t−t.
For every n stimulus feature, the algorithm ﬁnds an optimal ﬁlter kernel h, which is also known as a TRF. When n stimulus
feature is >1, h is referred to as multivariate TRF (mTRF). The term t denotes the delays between the predicted brain
response ˆyt and stimulus feature x (for further details see Brodbeck et al., 2023 ). TRFs re ﬂect responses to continuous
data instead of averaged responses to discrete events ( Crosse et al., 2021 ). For the estimation of the TRFs, the stimulus
features and MEG data were normalized ( z-scored), and an integration window from −100 to 600 ms with a kernel basis of
50 ms Hamming windows was de ﬁned. To prevent over ﬁtting, early stopping based on the ℓ2 norm was used. By using
fourfold nested cross-validation (two training folds, one validation fold, and one test fold), each partition served as a test
set once ( Brodbeck et al., 2023 ). TRFs were estimated for each of the three free-orientation dipoles independently at all
3,053 sources (see above, Source localization). The spectrogram and acoustic onset mTRFs were averaged over the fre-
quency dimension. To account for interindividual anatomical differences, TRFs were spatially smoothed with a Gaussian
kernel (SD = 5 mm; Kulasingham et al., 2020). The Euclidean vector norm of the smoothed TRFs was taken, resulting in one
TRF per source.
To obtain a measure of neural tracking, we correlated the predicted brain response ˆy
t with the original response to cal-
culate the prediction accuracy and computed as the average dot product over time (expressed as Pearson ’s correlation
coefﬁcient r). This correlation indicates that a higher prediction accuracy re ﬂects enhanced neural tracking, meaning that
the brain response more closely aligns with the stimulus features ( Gillis et al., 2022 ).
In order to investigate the neural processing of the audiovisual speech features, we calculated three different forward
models per condition and participant (see Fig. 1C for the analysis framework). The acoustic model consisted of the two
acoustic stimulus features (spectrogram and acoustic onsets) and —also applicable to all other models —the correspond-
ing MNE source-localized MEG data. The lip model contained only the lip movements as a stimulus feature. Additionally, a
combined acoustic + lip model was calculated to control for acoustic features in a subsequent analysis.
We deﬁned functional regions of interest (fROIs; Nieto-Castanon et al., 2003 ) by creating labels based on the 90th per-
centile of the whole-brain prediction accuracies in the multispeaker condition (similar to Suess et al., 2022a ). The multi-
speaker condition was chosen for extracting the fROIs because it potentially incorporates all included stimulus
features, due to its higher demand ( Golumbic et al., 2013 ). This was done separately for the acoustic and lip models to
map their unique neural sources ( Fig. 1 C). According to the “aparc” FreeSurfer parcellation ( Desikan et al., 2006 ), the
acoustic fROI mainly involved sources in the temporal, lateral parietal, and posterior frontal lobes. The superior parietal
and lateral occipital lobes made up the majority of the lip fROI. To obtain an audiovisual fROI for the acoustic + lip model,
we combined the labels of the acoustic and lip fROIs.
For every model, the TRFs in their respective fROI were averaged and, exclusively for Figure 2A, smoothed over time
with a 50 ms Hamming window. Grand-average TRF magnitude peaks were detected with scipy version 1.8.0 (running
on Python 3.9.7; Virtanen et al., 2020 ) and visualized as a difference between the multi- and single-speaker conditions.
To suppress regression artifacts that typically occur ( Crosse et al., 2016a ), we visualized TRFs between −50 and
550 ms. Prediction accuracies in the fROIs were Fisher z-transformed and then averaged, and then the z values were back-
transformed to Pearson’s correlation coefﬁcients (Corey et al., 1998). For the lower panels of each model in Figure 2B, the
prediction accuracies of the acoustic and lip models were averaged in their respective fROIs. Figures were created with the
built-in plotting functions of eelbrain and seaborn version 0.12.0 (running on Python 3.9.7; Waskom, 2021).
In order to answer the question whether or not lip movements enhance neural tracking, a control for acoustic features
(spectrograms and acoustic onsets) is needed. This is particularly important due to the intercorrelation of audiovisual
speech features ( Chandrasekaran et al., 2009 ; Daube et al., 2019 ). To investigate the unique contribution of lip move-
ments, we used the averaged prediction accuracies in the audiovisual fROI and subtracted the acoustic model from
Research Article: New Research 6 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 6 of 16
the acoustic + lip model (for a general overview on control approaches, see Gillis et al., 2022 ). The resulting unique con-
tribution of lip movements was expressed as percentage change ( Fig. 2C).
Statistical analysis and Bayesian modeling. All frequentist statistical tests were conducted with built-in functions from
eelbrain and the statistical package pingouin version 0.5.2 (running on Python 3.9.7; Vallat, 2018 ). The three behavioral
measures (comprehension, dif ﬁculty, and engagement; Fig. 1B) were statistically compared between the two conditions
(single speaker and multispeaker) using a Wilcoxon signed-rank test and the matched-pairs rank –biserial correlation rC
was reported as the effect size ( King et al., 2018 ).
The TRFs corresponding to the three stimulus features (spectrogram, acoustic onsets, and lip movements; Fig. 2A) were
tested for statistical difference between the two conditions using a cluster-based permutation test with threshold-free
cluster enhancement (TFCE; dependent-sample t test; 10,000 randomizations; Maris and Oostenveld, 2007 ; Smith and
Nichols, 2009 ). Due to the previously mentioned TRF regression artifacts, the time window for the test was limited to
−50 to 550 ms. Depending on the direction of the cluster, the maximum or minimum t value was reported and Cohen ’s
d of the averaged temporal extent of the cluster was calculated.
We tested the nonaveraged prediction accuracies in the acoustic and lip fROIs ( Fig. 2B) with a cluster-based permuta-
tion test with TFCE (dependent-sample t test, 10,000 randomizations). According to the cluster ’s direction, the maximum
or minimum t value was reported, and Cohen’s d of the cluster’s averaged spatial extent was calculated. Additionally, aver-
aged prediction accuracies in the acoustic and lip fROIs were statistically tested with a dependent-sample t test, and
Cohen’s d was reported as the effect size. In the audiovisual fROI, the prediction accuracies and unique contribution of
lip movements ( Fig. 2 C) were tested with a dependent-sample t test, and Cohen ’s d was reported as the effect size.
If the data were not normally distributed according to a Shapiro –Wilk test, the Wilcoxon signed-rank test was used,
and the matched-pair rank –biserial correlation r
C was reported as the effect size. The distribution of the contribution of
lip movements was assessed using the bimodality coef ﬁcient (Freeman and Dale, 2013 ).
To investigate if neural tracking is predictive for behavior, we calculated Bayesian multilevel models in R version 4.2.2
(R Core Team, 2022 ) with the Stan-based package brms version 2.18.4 ( Bürkner, 2017 ; Carpenter et al., 2017 ). Neural
tracking (i.e., the averaged prediction accuracies within the respective fROI) was used to separately predict the three beha-
vioral measures (averaged over the same number of trials for all participants). A random intercept was added for each par-
ticipant to account for repeated measures (single speaker and multispeaker). The models were ﬁtted independently for the
acoustic and lip models ( Fig. 3). According to the Wilkinson notation ( Wilkinson and Rogers, 1973 ), the general formula
was as follows:
behavioral measure ≏ 1 + neural tracking + (1 | participant).
We wanted to test whether the unique contribution of lip movements to neural speech tracking (see above, Forward
models) yields any behavioral relevance. For this, we also used the behavioral data of the otherwise unanalyzed conditions
with a face mask, which were the same number of trials for all participants (see above, Stimuli and experimental design).
We ﬁtted Bayesian multilevel models with the averaged unique contribution of lip movements to separately predict the
behavioral measures when the speaker wore a face mask or not ( Fig. 4). The general formula was as follows:
behavioral measure ≏ 1 + unique contribution of lip movements + (1 | participant).
Before doing so, we ﬁtted control models to show the effect of the conditions on the behavioral measures when the lips
are occluded. Additional control models to test the effect of the unique contribution of lip movements on the averaged
behavioral data without a face mask were also ﬁtted. In all described models, a random intercept was included for
each participant to account for repeated measures (single speaker and multispeaker).
Weakly or noninformative default priors of brms were used, whose in ﬂuence on the results is negligible ( Bürkner, 2017,
2018). For model calculation, all numerical variables were z-scored, and standardized regression coef ﬁcients ( b) were
reported with 89% credible intervals (CIs; i.e., Bayesian uncertainty intervals; McElreath, 2020). In addition, we report pos-
terior probabilities (PP
b >0 ) with values closer to 100%, providing evidence that the effect is greater than zero and closer to
0% that the effect was reversed (i.e., smaller than zero). If the 89% CIs for an estimate did not include zero and PP b >0 was
below 5.5% or above 94.5%, the effects were considered statistically signi ﬁcant.
All models were ﬁtted with a Student ’s t distribution, as indicated by graphical posterior predictive checks, Pareto ˆk
diagnostics ( Vehtari et al., 2022b ), and leave-one-out cross –validation via loo version 2.5.1 ( Vehtari et al., 2017 , 2022a).
Common algorithm-agnostic ( Vehtari et al., 2021 ) and algorithm-speci ﬁc diagnostics ( Betancourt, 2018 ) showed that
all Bayesian multilevel models converged. For all relevant parameters, the convergence diagnostic ˆR , 1.01 and effective
sample size >400 indicated that there were no divergent transitions. Figures were created with ggplot2 version 3.4.0
(Wickham, 2016) and ggdist version 3.2.0 ( Kay, 2022). Unstandardized b’s were used for the ﬁtted values of the models
in Figures 3 and 4.
Research Article: New Research 7 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 7 of 16
Data and code availability. Preprocessed data and code are publicly available at GitHub (https://github.com/reispat/av_
speech_mask).
Results
Twenty-nine participants listened to audiobooks with a corresponding video of the speaker and a randomly occurring
audio-only distractor. Source-localized MEG responses to acoustic features (spectrogram and acoustic onsets) and lip
movements were predicted using forward models (TRFs). We compared the TRFs between the two conditions and eval-
uated neural tracking of the acoustic features and lip movements. The unique contribution of lip movements was obtained
by controlling for acoustic features and was compared between conditions. Using Bayesian multilevel modeling, we pre-
dicted the behavioral measures with neural tracking. We also probed the unique contribution of lip movements for their
behavioral relevance by predicting the behavioral measures when the lips were occluded with a surgical face mask or not.
Listening situations with multiple speakers are behaviorally more demanding
Participants performed worse in the multispeaker condition (M = 62.93%; SD = 17.34%), compared with the single-speaker
condition (M =7 3 . 5 2 % ; S D=9 . 7 1 % ;W =7 3 . 0 0 ;p =0 . 0 0 3 ;r
C = 0.64). In the multispeaker condition, subjective difﬁculty rat-
ings were higher (M = 3.67; SD = 0.82) than in the single-speaker condition (M =2 . 4 7 ; S D=0 . 7 1 ;W =1 1 . 5 0 ;p =9 . 0 0×1 0−6;
rC = −0.95). Engagement was rated higher in the single-speaker condition (M = 3.91; SD = 0.74) compared with the multispea-
ker condition (M =3 . 7 2 ;S D=0 . 8 5 ;W =2 9 . 0 0 ;p =0 . 0 2 4 ;rC = 0.62). Overall, behavioral data showed that in the multispeaker
condition, participants performed worse, reported the task to be more difﬁcult, and were less motivated (Fig. 1B).
Neural responses to lip movements are enhanced in a multispeaker setting
First, we analyzed the neural responses to acoustic and visual speech features by statistically comparing the corre-
sponding TRFs between the single- and multispeaker conditions within their respective fROIs ( Fig. 2A). The spectrogram
TRFs showed a signi ﬁcant difference between conditions, with three clusters extending from early (30 –110 ms; t = −5.26;
p = 0.0001; d = −0.81), middle (160 –290 ms; t = −3.78; p = 0.003; d = −1.00), and late (310 –470 ms; t = −5.58; p = 0.0001;
d = −1.02) time ranges. Grand-average TRF peaks are more pronounced in the single-speaker condition, with two peaks
at 70 and 180 ms. While the ﬁrst peak is also present in the multispeaker condition, the second peak appeared 50 ms
earlier than the single-speaker setting. The latter peak caused the largest differences in the magnitudes of the TRFs, which
are most prominent in the right hemisphere of the fROI.
The TRFs to acoustic onsets showed a signi ﬁcant difference between single- and multispeaker speech, with three clus-
ters extending from early ( −20 to 80 ms; t = −5.39; p < 0.001; d = −1.10; Fig. 2 A), mid (120 –140 ms; t = −4.54; p = 0.004;
d = −1.43), and mid-late (190 –260 ms; t = −6.11; p < 0.001; d = −1.13) time windows. The TRFs showed two peaks at
70 and 190 ms in the single-speaker condition. Similar to the spectrogram TRFs, the ﬁ
rst peak in the multispeaker
condition is at the same time point as in the single-speaker condition, and the second peak is 50 ms earlier. The magnitude
differences across peaks and hemispheres are not substantially different.
TRFs to lip movements show an opposite pattern to the TRFs to acoustic features, with stronger processing in the
multispeaker condition. Signi ﬁcant condition differences in the TRFs to lip movements between single- and multispeaker
speech were found, with four clusters extending from early ( −20 to 70 ms; t = 4.41; p = 0.0005; d = 0.86; Fig. 2 A), mid
(140–270 ms; t = 3.97; p = 0.001; d = 0.88), mid-late (290 –330 ms; t = 3.34; p = 0.01; d = 0.91), and late (420 –460 ms;
t = 3.90; p = 0.002; d = 0.90) time windows. The latencies of the peaks were later in general (160 and 290 ms), as compared
with the acoustic TRFs, which is also in line with the longer duration for a stimulus to reach the visual system ( Thorpe et al.,
1996; VanRullen and Thorpe, 2001 ). In the single-speaker condition, the peaks are delayed by 10 ms compared with the
multispeaker condition, and magnitude differences are most prominent in the ﬁrst peak and left hemisphere.
Our initial analysis showed that neural responses to acoustic features are stronger when speech is clear. In contrast,
neural responses to lip movements were enhanced in a multispeaker environment. The stronger processing of lip move-
ments suggests a greater reliance on the lips of a speaker when speech is harder to understand.
The cocktail party diametrically affects acoustic and visual neural speech tracking
So far, the TRF results indicate a stronger neural response to lip movements and a weaker one to acoustic features when
there is more than one simultaneous speaker. We also wanted to answer the question whether neural tracking of audio-
visual speech features differs between the single-speaker and multispeaker conditions in their respective fROIs ( Fig. 2B).
Acoustic neural tracking in the nonaveraged acoustic fROI showed a signi ﬁcant condition difference in the left ( t = −8.04;
p < 0.001; d = −1.47) and right (t = −9.26; p < 0.001; d = −1.30) hemispheres. Averaged acoustic neural tracking was higher
in the single-speaker condition than in the multispeaker condition ( t
(28) = −8.07; p = 8.76 × 10−9; d = −1.30). Neural tracking
of lip movements showed a signi ﬁcant condition difference in the left hemisphere ( t = 3.83; p = 0.037; d = 0.51; Fig. 2 B),
with a focal superior parietal area involved. When averaging over sources, neural tracking was higher in the multispeaker
condition than in the single-speaker condition ( W = 114.00; p = 0.026; r
C = 0.48).
Overall, the results showed that neural tracking was enhanced for acoustic features when speech is clear and higher for
lip movements when there are multiple speakers. This is in line with the observed neural responses.
Research Article: New Research 8 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 8 of 16
Lip movements enhance neural speech tracking more in multispeaker situations
When there are two speakers, we have so far demonstrated that lip movements are processed more strongly and
lead to higher neural tracking compared with one speaker. However, their unique contribution to neural tracking is
still unknown, due to the intercorrelation of audiovisual speech features ( Chandrasekaran et al., 2009 ; Daube et al.,
2019). To address this, we controlled for the acoustic features so as to obtain the unique contribution of lip
movements over and above acoustic speech features. First, the acoustic model was evaluated in the audiovisual
fROI ( Fig. 2 C). Acoustic neural tracking was higher in the single-speaker condition than in the multispeaker condition
(t
(28) = −7.20; p = 7.68 × 10−8; d = 1.18). The acoustic model served as a baseline and was subtracted from a combined
acoustic + lip model and expressed as percentage change. The obtained unique contribution of lip movements
was higher in the multispeaker condition than in the single-speaker condition ( W = 24.00; p = 0.00003; r
C = 0.89).
The unique contribution of lip movements showed high interindividual variability and seemed to follow a bimodal
Figure 2. Neural responses to audiovisual speech features, neural speech tracking, and the unique contribution of lip movements. A, The three plots show
grand-averaged TRFs for the stimulus features in their respective fROIs and the peak magnitude contrasts (multispeaker vs single speaker) between t he
two conditions in the involved sources. For the acoustic features, TRF magnitudes were generally enhanced when speech was clear, with signi ﬁcant dif-
ferences ranging from p = 0.004 to p < 0.001 (d = −0.81 to −1.43). In contrast, the TRF to lip movements showed an enhanced magnitude in the multispea-
ker condition ( p = 0.01 to p = 0.0005 and effect sizes from d = 0.86–0.91). The shaded areas of the respective conditions represent the SEM. Gray bars
indicate the temporal extent of signi ﬁcant differences ( p < 0.05) between the two conditions. B, Neural speech tracking is shown for the nonaveraged
fROIs (top brain plots) and averaged fROIs of the acoustic and lip models. Acoustic neural tracking was higher in the single-speaker condition, with s ig-
niﬁcant left- and right-hemispheric differences (both p < 0.001 with d from −1.30 to −1.47; averaged, p = 8.76 × 10−9; d = −1.30). Lip movements were
tracked higher in the multispeaker condition ( p = 0.037; d = 0.51; averaged, p = 0.026; rC = 0.48). In the averaged plots, the black dots represent the
mean, and the corresponding bars the SEM, of the respective condition. C, In a combined acoustic and lip fROI, the acoustic model showed higher neural
tracking in the single-speaker condition ( p = 7.68 × 10−8; d = 1.18). The unique contribution of lip movements was obtained by subtracting the acoustic
model from the acoustic + lip model and expressed as percentage change. Lip movements especially enhanced neural tracking in the multispeaker con-
dition (p = 0.00003; rC = 0.89). Participants showed high interindividual variability with a unique contribution of lip movements of up to 45.37% but also only
a small contribution or no contribution at all. The black dots represent the mean, and the corresponding bars the SEM, of the respective condition.
*p < 0.05; **p < 0.01; ***p < 0.001.
Research Article: New Research 9 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 9 of 16
distribution ( Fig. 2 C), which was con ﬁrmed by a bimodality coef ﬁcient of 0.68 (values >0.555 indicate bimodality;
Pﬁster et al., 2013 ).
These results strongly indicate that lip movements enhance neural tracking, especially in multitalker speech. However,
substantial interindividual variability was observed, with participants showing a unique contribution of lip movements of up
to 45.37% in the multispeaker condition, while others showed only a small contribution or no contribution at all. In the next
steps, we will probe the behavioral relevance of the unique contribution of lip movements to neural speech tracking by
depriving individuals of this source of information.
Only acoustic neural speech tracking predicts behavior
Having established that listening situations with two speakers affect neural tracking of acoustic and visual speech fea-
tures in a diametrical way, we were further interested if neural tracking is able to predict the behavioral measures. We cal-
culated Bayesian multilevel models to predict the three behavioral measures (comprehension, dif ﬁculty, and engagement;
Fig. 1B) with the averaged neural tracking of the acoustic and lip models (Fig. 3). In the acoustic model, higher neural track-
ing was linked to higher comprehension ( b = 0.29; 89% CI = [0.07, 0.51]; PP
b >0 = 98.37%; Fig. 3A). Lower neural tracking
predicted higher difﬁculty ratings (b = −0.50; 89% CI = [−0.72, −0.29]; PPb >0 = 0.01%). When neural tracking was high, the
engagement ratings were also higher ( b = 0.12; 89% CI = [0.004, 0.24]; PP b >0 = 95.05%).
Neural tracking of lip movements was not related to comprehension ( b = 0.06; 89% CI = [−0.18, 0.28]; PPb >0 = 65.61%;
Fig. 3B). We also observed no evidence for an effect of the difﬁculty (b = −0.05; 89% CI = [−0.28, 0.18]; PPb >0 = 35.63%) or
engagement (b = 0.09; 89% CI = [−0.08, 0.26]; PP b >0 = 80.40%) ratings.
These results indicate that acoustic neural speech tracking predicts behavior: The higher the neural speech tracking, the
higher the comprehension and engagement ratings. Lower acoustic neural speech tracking was linked to higher dif ﬁculty
ratings. In contrast, neural speech tracking of lip movements did not predict behavior.
Stronger unique contribution of lip movements predicts behavioral deterioration when lips are occluded
Given the ﬁnding that lip movements enhance neural speech tracking ( Fig. 2 C), we were interested in whether this
unique contribution to neural speech tracking is behaviorally relevant. To do so, we also used the behavioral data from
the otherwise unanalyzed conditions in which the mouth was occluded by a surgical face mask (see the center of
Figure 3. Relating behavior to neural speech tracking. Bayesian multilevel models were ﬁtted to predict the behavioral measures with neural speech track-
ing. A, Higher acoustic neural speech tracking was linked to higher comprehension, lower difﬁculty ratings and higher engagement ratings. B, No evidence
for an effect was observed for the neural tracking of lip movements. Both panels, The shaded areas show the 89% CIs of the respective model. The dis-
tributions on the right show the posterior draws of the three models. The black dots represent the mean standardized regression coef ﬁcient b of the cor-
responding model. The corresponding bars show the 89% CI. If zero was not part of the 89% CI, the effect was considered signi ﬁcant (*).
Research Article: New Research 10 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 10 of 16
Fig. 4 A for example stimuli). Given that critical visual information is missing in these conditions, individuals who show
a strong unique contribution of lip movements on a neural level should show poorer behavioral outcomes. An initial
analysis showed that the effect of the conditions with a surgical face mask on behavior followed a similar pattern as
those with nonoccluded lips ( Fig. 1 B): Comprehension was worse in the multispeaker condition ( b = −0.77; 89%
CI = [ −1.13, −0.41]; PP
b >0 = 0.07%). Subjective dif ﬁculty ratings were also higher in the multispeaker condition
(b = −0.77; 89% CI = [ −1.13, −0.41]; PP b >0 = 0.07%). However, there was no effect of the conditions with a surgical
face mask on the engagement ratings ( b = −0.77; 89% CI = [ −1.13, −0.41]; PPb >0 = 0.07%).
While the effects on a solely behavioral level seem not to differ substantially when the lips are occluded or not, predicting
the behavioral measures with the unique contribution of lip movements showed the expected outcome ( Fig. 4 A):
Participants that had a higher unique contribution of lip movements in terms of neural tracking showed a decline in com-
prehension (b = −0.27; 89% CI = [−0.49, −0.06]; PP
b >0 = 2.21%) and reported the task to be more dif ﬁcult (b = 0.25; 89%
CI = [0.01, 0.51]; PP b >0 = 95.41%). The engagement ratings did not yield an effect ( b = 0.05; 89% CI = [ −0.07, 0.18];
PPb >0 = 76.14%).
Interestingly, we were not able to establish a link between the unique contribution of lip movements to the behavioral
data when the lips were not occluded ( Fig. 4 B). Comprehension ( b = −0.05; 89% CI = [ −0.28, 0.17]; PP b >0 = 36.09%),
difﬁculty ( b = 0.04; 89% CI = [ −0.19, 0.28]; PP b >0 = 60.86%), and engagement ( b = 0.06; 89% CI = [ −0.08, 0.19];
PPb >0 = 76.64%) were not linked to the unique contribution of lip movements.
Taken together, these ﬁndings support a behavioral relevance of the unique contribution of lip movements. Individuals
that have a higher unique contribution of lip movements on a neural level performed worse and reported the task to be
more difﬁcult when the mouth of the speaker was covered by a surgical face mask.
Discussion
The method of neural speech tracking is widely used to study the neural processing of continuous speech, though pri-
marily with audio-only stimuli (Di Liberto et al., 2015; Keitel et al., 2018; Brodbeck et al., 2018a; Chalas et al., 2022). Recent
studies have used audiovisual speech paradigms, but without directly modeling visual speech features and their temporal
Figure 4. Relating the unique contribution of lip movements to behavior. The unique contribution of lip movements was used to predict the behavioral
measures when the lips are occluded or not. A, When the unique contribution of lip movements was high, comprehension was lower, and dif ﬁculty
was reported higher. No evidence for an effect was observed for the engagement rating. The values of the ﬁtted Bayesian multilevel models are shown
with a depiction of the conditions in which the speakers wore a surgical face mask. B, The behavioral measures when the lips were not occluded were
not linked to the unique contribution of lip movements. Both panels, The shaded areas show the 89% CIs of the respective model. The distributions
on the right show the posterior draws of the three models. The black dots represent the mean standardized regression coef ﬁcient b of the corresponding
model. The corresponding bars show the 89% CI. If zero was not part of the 89% CI, the effect was considered signi ﬁcant (*).
Research Article: New Research 11 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 11 of 16
dynamics ( Golumbic et al., 2013 ; Crosse et al., 2016b ). In this study, we ﬁrst show the temporal dynamics and cortical
origins of TRFs obtained from lip movements in an audiovisual setting with one or two speakers. Similar to Brodbeck
et al. (2018a), neural responses to acoustic features in the two-speaker paradigm were generally weaker. In both acoustic
features, we observed that the second peak was 50 ms earlier when there were two speakers. Similar temporal differences
in TRFs were also observed in normal-hearing individuals in a selective attention speech paradigm ( Kaufman and Zion
Golumbic, 2023 ), as well as in cochlear implant users, where the attended speech was showing enhanced earlier
responses compared with ignored speech ( Kraus et al., 2021 ). The TRFs to lip movements showed an opposite pattern,
with an enhanced magnitude in the multispeaker condition ( Fig. 2A) and with substantially later peaks compared with the
TRF to acoustic features. This is in line with Bourguignon et al. (2020) , where initial TRF peaks at 115 and 159 ms were
shown from two signi ﬁcant sources, overlapping with our involved parietal and occipital sources ( Fig. 1 C). However,
the TRFs in their work were modeled to lip movements from silent videos, which precludes a comparison between different
listening situations. The ﬁnding that the peaks of TRFs occur later for lip movements than for auditory features seems
counterintuitive, as the visual stimulus usually precedes the auditory stimulus (van Wassenhove et al., 2005). One possible
reason for this could be that visual stimuli require a longer period of time to reach the visual system compared with auditory
stimuli ( Thorpe et al., 1996 ; VanRullen and Thorpe, 2001 ), thus leading to a later neural response when modeled using
TRFs. For TRFs to lip movements, we also observed a stronger contribution of left parietal and occipital regions, especially
when contrasting the ﬁrst peak. A possible explanation for this lateralization could be due to asymmetries in the process-
ing of lip movements, where previous studies showed a left-hemispheric advantage ( Campbell et al., 1996 ; Nicholls and
Searle, 2006).
Our ﬁndings also strengthen the argument that TRFs to visual speech are quantitatively different from TRFs to acoustic
speech (for an analysis based on coherence, see Park et al., 2016). In this study, however, we were not able to completely
rule out the contribution of auditory speech to modeled TRFs to lip movements, since an audiovisual paradigm was used.
In future studies, a visual-only condition should also be incorporated to further compare the differences between TRFs
derived from lip movements in an audiovisual or visual-only condition.
Based on the source-localized neural tracking, we determined fROIs via a data-driven approach —separately for the
acoustic features and lip movements ( Fig. 1C). The fROIs for the acoustic speech features involved sources along tem-
poral, parietal, and posterior frontal regions, covering regions that are related to speech perception ( Franken et al.,
2022). Previous studies source-localized TRFs in audio-only settings, though commonly restricting the analysis to tem-
poral regions ( Brodbeck et al., 2018a ; Kulasingham et al., 2020 ). The fROIs for the lip movements involved parietal and
occipital regions, in line with previous studies that source-localized the neural tracking of lip movements ( Hauswald
et al., 2018 ; Bourguignon et al., 2020 ; Aller et al., 2022 ). We also observed neural tracking of lip movements in temporal
regions (similar to Park et al., 2016) but with less involvement of the primary visual cortex and prominent only in the single-
speaker condition. Due to our approach of de ﬁning our fROIs based on the multispeaker condition, we minimized the
involvement of auditory regions in the lip fROIs.
When analyzing neural speech tracking in the acoustic fROIs, we showed a large effect with enhanced tracking in the
single-speaker condition compared with the multispeaker condition ( Fig. 2B). Using phase consistency as a neural track-
ing method, and not statistically tested, a large difference in neural tracking between single- and multispeaker speech was
shown by Golumbic et al. (2013) . We were not able to identify further studies that presented such a statistical contrast,
which could be due to the general focus on neural tracking of attended versus unattended speech, especially to decode
auditory attention (Mirkovic et al., 2015
; O’Sullivan et al., 2015 ; Schäfer et al., 2018 ; Ciccarelli et al., 2019 ; Geirnaert et al.,
2021). On a group level, the neural tracking of lip movements showed an enhancement in the multispeaker condition
(Fig. 2B). When comparing the involved sources of the corresponding lip fROI, we found a medium effect in the left superior
parietal cortex. This is in line with Park et al. (2016) , showing an effect in the left occipital and parietal cortex when com-
paring two similar conditions to our design ( “AV congruent vs All congruent ”), although after partializing out
auditory-related coherence. A possible explanation for the strong focality of our left superior parietal effect could be
due to the used TFCE method with a small default step size of 0.1, leading to a downweighting of spatially larger clusters
(Smith and Nichols, 2009). When we averaged the neural tracking of lip movements, we observed interesting patterns, with
participants showing no meaningful neural tracking (i.e., close to zero or negative correlations) when there was one
speaker, but when speech became challenging, their neural tracking reached positive values. Notably, this pattern was
reversed for some participants, suggesting that not all of them used the lip movements in the same manner. To investigate
this further, eye tracking should be used to identify which face regions participants ﬁxated when attending audiovisual
speech (Rennig and Beauchamp, 2018 ) or to additionally incorporate a recently proposed phenomenon termed “ocular
speech tracking” (Gehmacher et al., 2024 ). In this study, we cannot rule out that during challenging speech, participants
ﬁxated the mouth area stronger, thus contributing to enhanced neural tracking. However, previous eye tracking research
has shown that individuals gaze at talking ( Gurler et al., 2015 ) and also nontalking faces ( Peterson and Eckstein, 2013 ;
Mehoudar et al., 2014) in a highly individual manner, which is putatively incorporated in our ﬁndings of high interindividual
variability.
Research Article: New Research 12 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 12 of 16
We ﬁrst compared the neural tracking of audiovisual speech between single-speaker and multispeaker conditions in an
isolated manner. Due to the aforementioned intercorrelation of audiovisual speech features ( Chandrasekaran et al., 2009 ;
Daube et al., 2019), this approach could not rule out any acoustic contributions to the neural tracking of lip movements or
vice versa. To reveal the unique contribution of lip movements and to incorporate regions that are part of models of audio-
visual speech perception ( Bernstein and Liebenthal, 2014 ) and multisensory integration ( Peelle and Sommers, 2015 ), we
combined both fROIs and controlled for acoustic speech features. Within the TRF framework, we show that lip movements
enhance acoustic-controlled neural speech tracking ( Fig. 2C). A general enhancement was observed for both single- and
multispeaker speech, which is in line with behavioral ﬁndings that visual speech features enhance intelligibility under clear
speech conditions as well (Stacey et al., 2016; Blackburn et al., 2019). When comparing the two conditions, we observed a
large effect, showing a higher unique contribution of lip movements in the multispeaker condition. Analogous to behavioral
ﬁndings in Aller et al. (2022) , the unique contribution of lip movements showed high interindividual variability ( Fig. 2C) and
also followed a bimodal distribution: Some individuals showed a strong unique contribution of lip movements, while others
showed only a small unique contribution or none at all. Interestingly, one individual even showed a negative inﬂuence when
adding lip movements to the acoustic model when there was only one speaker. As soon as speech became challenging,
that individual showed a contribution of lip information. Previous research on audiovisual speech processing showed that
interindividual differences are related to visual attention ( Tiippana et al., 2004 ), availability of attentional resources ( Alsius
et al., 2005 ), or individual preference for auditory or visual stimuli ( Schwartz, 2010), which are potential factors that could
explain our observed differences. Overall, our ﬁndings are in line with the beneﬁcial effects of visual speech when listening
is challenging ( Sumby and Pollack, 1954 ; Grant and Seitz, 2000 ; Ross et al., 2007 ; Remez, 2012).
Using Bayesian multilevel modeling, we established a link between neural speech tracking and behavior. We show that
higher acoustic neural tracking is related to higher comprehension ( Fig. 3A), a ﬁnding also reported in a study that used
vocoded speech (Chen et al., 2023). We also show that higher acoustic neural tracking is related to lower dif ﬁculty ratings.
This is in line with a study that showed a positive relationship between speech intelligibility ratings and acoustic neural
tracking, though using speech-in-noise ( Ding and Simon, 2013 ). Higher engagement ratings were associated with higher
acoustic neural tracking —in contrast to Schubert et al. (2023) —showing no relationship between the two measures. Our
ﬁndings suggest that enhanced neural speech tracking of acoustic features is related to a lower listening effort, where cog-
nitive demand and motivation are the key contributors (Peelle, 2018). Interpreting the relationship with comprehension per-
formance and lower dif ﬁculty ratings as cognitive demand and that with motivation as engagement, our results putatively
reﬂect a neural proxy of listening effort.
We were not able to establish any link between the neural tracking of lip movements and the behavioral measures. It is
important to note here that the analyzed neural tracking of lip movements was not yet controlled for speech acoustics
(Gillis et al., 2022 ), which could confound any relationship with behavior. A recent MEG study impressively showed that
the neural tracking of acoustic speech features can explain cortical responses to higher-order linguistic features, such
as phoneme onsets ( Daube et al., 2019 ). It is important to note that this caveat also applies to the observed relationship
between acoustic neural tracking and behavior, and it cannot be ruled out that this relationship is driven by these higher-
order features. Further audiovisual speech studies, in which linguistic features are also modeled, are necessary.
The COVID-19 pandemic established the use of face masks on a global scale ( Feng et al., 2020 ). However, it has been
demonstrated that covering the mouth has adverse effects on behavioral measures, such as speech perception ( Rahne
et al., 2021). On a neural level, Haider et al. (2022) showed that surgical face masks impair the neural tracking of acoustic
and higher-order segmentational speech features. In a follow-up study, Haider et al. (2024) incorporated lip movements in
the analysis and showed that face masks primarily impact speech processing by blocking visual speech rather than by
acoustic degradation. Here, we establish a relationship between behavioral measures and the unique contribution of
visual speech on neural tracking, which has not yet been shown. When the speaker wore a surgical face mask, individuals
that show a higher unique contribution of lip movements displayed lower comprehension and higher dif ﬁculty ratings.
Strikingly, no effect was found when the speaker did not wear a surgical face mask. Further studies with larger sample
sizes are needed to disentangle the potential in ﬂuence of experimental conditions on this relationship, e.g., using
Bayesian mediation analysis (Yuan and MacKinnon, 2009; Nuijten et al., 2015). Overall, our results suggest that individuals
who use lip movements more effectively show behavioral deterioration when visual speech is absent.
The current study provides evidence for the substantial interindividual variability in the unique contribution of lip move-
ments to neural speech tracking and its relationship to behavior. First, we show that neural responses to lip movements are
more pronounced when speech is challenging, compared with when speech is clear. We show that lip movements effec-
tively enhance neural speech tracking in brain regions related to audiovisual speech, with high interindividual variability.
Furthermore, we demonstrate that the unique contribution of lip movements is behaviorally relevant. Individuals that show
a higher unique contribution of lip movements show lower comprehension and rate the task to be more dif ﬁcult when the
speaker wears a surgical face mask. Remarkably, this relationship is completely absent when the speaker did not wear a
mask. Our results provide insights into the individual differences in the neural tracking of lip movements and offer potential
implications for future clinical and audiological settings to objectively assess audiovisual speech perception, such as in
populations where traditional task-based assessments cannot be meaningfully conducted.
Research Article: New Research 13 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 13 of 16
References
Akalin-Acar Z, Gençer NG (2004) An advanced boundary element
method (BEM) implementation for the forward problem of electro-
magnetic source imaging. Phys Med Biol 49:5011.
Aller M, Økland HS, MacGregor LJ, Blank H, Davis MH (2022)
Differential auditory and visual phase-locking are observed during
audio-visual bene ﬁt and silent lip-reading for speech perception.
J Neurosci 42:6108 –6120.
Alsius A, Navarra J, Campbell R, Soto-Faraco S (2005) Audiovisual
integration of speech falters under high attention demands. Curr
Biol 15:839–843.
Bell AJ, Sejnowski TJ (1995) An information-maximization approach to
blind separation and blind deconvolution. Neural Comput 7:1129 –
1159.
Bernstein LE, Liebenthal E (2014) Neural pathways for visual speech
perception. Front Neurosci 8:1 –18.
Besl PJ, McKay ND (1992) A method for registration of 3-D shapes.
IEEE Trans Pattern Anal Mach Intell 14:239 –256.
Betancourt M (2018) A conceptual introduction to Hamiltonian Monte
Carlo (arXiv:1701.02434). arXiv.
Biesmans W, Das N, Francart T, Bertrand A (2017) Auditory-inspired
speech envelope extraction methods for improved EEG-based
auditory attention detection in a cocktail party scenario. IEEE
Trans Neural Syst Rehabil Eng 25:402 –412.
Blackburn CL, Kitterick PT, Jones G, Sumner CJ, Stacey PC (2019)
Visual speech bene ﬁt in clear and degraded speech depends on
the auditory intelligibility of the talker and the number of back-
ground talkers. Trends Hear 23:1 –14.
Boersma P (2001) Praat, a system for doing phonetics by computer.
Glot Int 5:341 –345.
Bourguignon M, Baart M, Kapnoula EC, Molinaro N (2020) Lip-reading
enables the brain to synthesize auditory features of unknown silent
speech. J Neurosci 40:1053 –1065.
Brainard DH (1997) The psychophysics toolbox. Spat Vis 10:433 –436.
Brodbeck C, Das P, Gillis M, Kulasingham JP, Bhattasali S, Gaston P,
Resnik P, Simon JZ (2023) Eelbrain, a Python toolkit for time-
continuous analysis with temporal response functions. Elife 12:
e85012.
Brodbeck C, Hong LE, Simon JZ (2018a) Rapid transformation from
auditory to linguistic representations of continuous speech. Curr
Biol 28:3976–3983.e5.
Brodbeck C, Jiao A, Hong LE, Simon JZ (2020) Neural speech restora-
tion at the cocktail party: auditory cortex recovers masked speech
of both attended and ignored speakers. PLoS Biol 18:e3000883.
Brodbeck C, Presacco A, Simon JZ (2018b) Neural source dynamics of
brain responses to continuous stimuli: speech processing from
acoustics to comprehension. Neuroimage 172:162 –174.
Brodbeck C, Simon JZ (2020) Continuous speech processing. Curr
Opin Physiol 18:25 –31.
Broderick MP, Anderson AJ, Di Liberto GM, Crosse MJ, Lalor EC
(2018) Electrophysiological correlates of semantic dissimilarity
reﬂect the comprehension of natural, narrative speech. Curr Biol
28:803–809.e3.
Brown VA, Van Engen KJ, Peelle JE (2021) Face mask type affects
audiovisual speech intelligibility and subjective listening effort in
young and older adults. Cogn Res Princ Implic 6:49.
Bürkner P-C (2017) brms: an R package for Bayesian multilevel models
using Stan. J Stat Softw 80:1 –28.
Bürkner P-C (2018) Advanced Bayesian multilevel modeling with the R
package brms. R J 10:395 –411.
Campbell R, De Gelder B, De Haan E (1996) The lateralization of lip-
reading: a second look. Neuropsychologia 34:1235 –1240.
Carpenter B, Gelman A, Hoffman MD, Lee D, Goodrich B, Betancourt
M, Brubaker M, Guo J, Li P, Riddell A (2017) Stan: a probabilistic
programming language. J Stat Softw 76:1 –32.
Chalas N, Daube C, Kluger DS, Abbasi O, Nitsch R, Gross J (2022)
Multivariate analysis of speech envelope tracking reveals coupling
beyond auditory cortex. Neuroimage 258:119395.
Chandrasekaran C, Trubanova A, Stillittano S, Caplier A, Ghazanfar AA
(2009) The natural statistics of audiovisual speech. PLoS Comput
Biol 5:e1000436.
Chen Y-P, Schmidt F, Keitel A, Rösch S, Hauswald A, Weisz N (2023)
Speech intelligibility changes the temporal evolution of neural
speech tracking. Neuroimage 268:119894.
Cherry EC (1953) Some experiments on the recognition of speech,
with one and with two ears. J Acoust Soc Am 25:975 –979.
Chu DK, et al. (2020) Physical distancing, face masks, and eye protec-
tion to prevent person-to-person transmission of SARS-CoV-2 and
COVID-19: a systematic review and meta-analysis. Lancet
395:1973–1987.
Ciccarelli G, Nolan M, Perricone J, Calamia PT, Haro S, O ’Sullivan J,
Mesgarani N, Quatieri TF, Smalt CJ (2019) Comparison of two-
talker attention decoding from EEG with nonlinear neural networks
and linear methods. Sci Rep 9:11538.
Corey DM, Dunlap WP, Burke MJ (1998) Averaging correlations:
expected values and bias in combined Pearson rs and Fisher ’sz
transformations. J Gen Psychol 125:245 –261.
Crosse MJ, Butler JS, Lalor EC (2015) Congruent visual speech
enhances cortical entrainment to continuous auditory speech in
noise-free conditions. J Neurosci 35:14195 –14204.
Crosse MJ, Di Liberto GM, Bednar A, Lalor EC (2016a) The multivariate
temporal response function (mTRF) toolbox: a Matlab toolbox
for relating neural signals to continuous stimuli. Front Hum
Neurosci 10:1–14.
Crosse MJ, Liberto GMD, Lalor EC (2016b) Eye can hear clearly now:
inverse effectiveness in natural audiovisual speech processing
relies on long-term crossmodal temporal integration. J Neurosci
36:9888–9895.
Crosse MJ, Zuk NJ, Di Liberto GM, Nidiffer AR, Molholm S, Lalor EC
(2021) Linear modeling of neurophysiological responses to speech
and other continuous stimuli: methodological considerations for
applied research. Front Neurosci 15:1350.
Das P, Brodbeck C, Simon JZ, Babadi B (2020) Neuro-current
response functions: a uni ﬁed approach to MEG source analysis
under the continuous stimuli paradigm. Neuroimage 211:116528.
Daube C, Ince RAA, Gross J (2019) Simple acoustic features can
explain phoneme-based predictions of cortical responses to
speech. Curr Biol 29:1924 –1937.e9.
David SV, Mesgarani N, Shamma SA (2007) Estimating sparse
spectro-temporal receptive ﬁelds with natural stimuli. Network
18:191–212.
de Jong NH, Wempe T (2009) Praat script to detect syllable nuclei and
measure speech rate automatically. Behav Res Methods 41:385 –
390.
Delorme A, Makeig S (2004) EEGLAB: an open source toolbox for anal-
ysis of single-trial EEG dynamics including independent compo-
nent analysis. J Neurosci Methods 134:9 –21.
Desikan RS, et al. (2006) An automated labeling system for subdividing
the human cerebral cortex on MRI scans into gyral based regions of
interest. Neuroimage 31:968 –980.
Di Liberto GM, O ’Sullivan JA, Lalor EC (2015) Low-frequency cortical
entrainment to speech re ﬂects phoneme-level processing. Curr
Biol 25:2457–2465.
Ding N, Simon JZ (2013) Adaptive temporal encoding leads to a
background-insensitive cortical representation of speech.
J Neurosci 33:5728 –5735.
Erber NP (1975) Auditory-visual perception of speech. J Speech Hear
Disord 40:481–492.
Feng S, Shen C, Xia N, Song W, Fan M, Cowling BJ (2020) Rational use
of face masks in the COVID-19 pandemic. Lancet Respir Med
8:434–436.
Fischl B (2012) Freesurfer. Neuroimage 62:774 –781.
Fishbach A, Nelken I, Yeshurun Y (2001) Auditory edge detection: a
neural model for physiological and psychoacoustical responses
to amplitude transients. J Neurophysiol 85:2303 –2323.
Research Article: New Research 14 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 14 of 16
Franken MK, Liu BC, Ostry DJ (2022) Towards a somatosensory theory
of speech perception. J Neurophysiol 128:1683 –1695.
Freeman JB, Dale R (2013) Assessing bimodality to detect the pres-
ence of a dual cognitive process. Behav Res Methods 45:83 –97.
Gehmacher Q, Schubert J, Schmidt F, Hartmann T, Reisinger P, Rösch
S, Schwarz K, Popov T, Chait M, Weisz N (2024) Eye movements
track prioritized auditory features in selective attention to natural
speech. Nat Commun 15:3692.
Geirnaert S, Vandecappelle S, Alickovic E, de Cheveigne A,
LalorE, Meyer BT, Miran S, Francart T, Bertrand A (2021)
Electroencephalography-based auditory attention decoding:
toward neurosteered hearing devices. IEEE Signal Process Mag
38:89–102.
Gillis M, Van Canneyt J, Francart T, Vanthornhout J (2022) Neural
tracking as a diagnostic tool to assess the auditory pathway.
Hear Res 426:108607.
Gillis M, Vanthornhout J, Simon JZ, Francart T, Brodbeck C (2021)
Neural markers of speech comprehension: measuring EEG track-
ing of linguistic speech representations, controlling the speech
acoustics. J Neurosci 41:10316 –10329.
Golumbic EZ, Cogan GB, Schroeder CE, Poeppel D (2013) Visual input
enhances selective speech envelope tracking in auditory cortex at
a “cocktail party”. J Neurosci 33:1417 –1426.
Gramfort A, et al. (2013) MEG and EEG data analysis with
MNE-Python. Front Neurosci 7:1 –13.
Gramfort A, Luessi M, Larson E, Engemann DA, Strohmeier D,
Brodbeck C, Parkkonen L, Hämäläinen MS (2014) MNE software
for processing MEG and EEG data. Neuroimage 86:446 –460.
Grant KW, Seitz P-F (2000) The use of visible speech cues for improv-
ing auditory detection of spoken sentences. J Acoust Soc Am
108:1197–1208.
Gurler D, Doyle N, Walker E, Magnotti J, Beauchamp M (2015) A link
between individual differences in multisensory speech perception
and eye movements. Atten Percept Psychophys 77:1333 –1341.
Haider CL, Park H, Hauswald A, Weisz N (2024) Neural speech tracking
highlights the importance of visual speech in multi-speaker situa-
tions. J Cogn Neurosci 36:128 –142.
Haider CL, Suess N, Hauswald A, Park H, Weisz N (2022) Masking of
the mouth area impairs reconstruction of acoustic speech features
and higher-level segmentational features in the presence of a dis-
tractor speaker. Neuroimage 252:119044.
Hämäläinen MS, Ilmoniemi RJ (1994) Interpreting magnetic ﬁelds of
the brain: minimum norm estimates. Med Biol Eng Comput
32:35–42.
Hartmann T, Weisz N (2020) An introduction to the objective psycho-
physics toolbox (o_ptb). Front Psychol 11:1 –10.
Hauswald A, Lithari C, Collignon O, Leonardelli E, Weisz N (2018) A
visual cortical network for deriving phonological information from
intelligible lip movements. Curr Biol 28:1453 –1459.e3.
Heeris J (2013) Gammatone ﬁlterbank toolkit [Computer software].
Available at: https:/ /github.com/detly/gammatone
Houck JM, Claus ED (2020) A comparison of automated and manual
co-registration for magnetoencephalography. PLOS One 15:
e0232100.
Kaufman M, Zion Golumbic E (2023) Listening to two speakers: capac-
ity and tradeoffs in neural speech tracking during selective and dis-
tributed attention. Neuroimage 270:119984.
Kay M (2022) ggdist: Visualizations of distributions and uncertainty
[Computer software]. Zenodo.
Keitel A, Gross J, Kayser C (2018) Perceptually relevant speech track-
ing in auditory and motor cortex reﬂects distinct linguistic features.
PLoS Biol 16:e2004473.
King BM, Rosopa PJ, Minium EW (2018) Statistical reasoning in the
behavioral sciences, Ed 7. Hoboken, NJ: John Wiley & Sons.
Kleiner M, Brainard D, Pelli D (2007) What ’s new in psychtoolbox-3?
Perception 36:1–16.
Kraus F, Tune S, Ruhe A, Obleser J, Wöstmann M (2021) Unilateral
acoustic degradation delays attentional separation of competing
speech. Trends Hear 25:23312165211013242.
Kulasingham JP, Brodbeck C, Presacco A, Kuchinsky SE,
Anderson S, Simon JZ (2020) High gamma cortical processing
of continuous speech in younger and older listeners.
Neuroimage 222:117291.
Lalor EC, Pearlmutter BA, Reilly RB, McDarby G, Foxe JJ (2006) The
VESPA: a method for the rapid estimation of a visual evoked poten-
tial. Neuroimage 32:1549 –1561.
Lalor EC, Power AJ, Reilly RB, Foxe JJ (2009) Resolving precise tem-
poral processing properties of the auditory system using continu-
ous stimuli. J Neurophysiol 102:349 –359.
Lin F-H, Witzel T, Ahlfors SP, Stuf ﬂebeam SM, Belliveau JW,
Hämäläinen MS (2006) Assessing and improving the spatial accu-
racy in MEG source localization by depth-weighted minimum-norm
estimates. Neuroimage 31:160 –171.
Maris E, Oostenveld R (2007) Nonparametric statistical testing of EEG-
and MEG-data. J Neurosci Methods 164:177 –190.
McElreath R (2020) Statistical rethinking: a Bayesian course with exam-
ples in R and STAN, Ed 2. Boca Raton, FL: Chapman and Hall/CRC.
Mehoudar E, Arizpe J, Baker CI, Yovel G (2014) Faces in the eye of the
beholder: unique and stable eye scanning patterns of individual
observers. J Vis 14:6.
Mirkovic B, Debener S, Jaeger M, Vos MD (2015) Decoding the
attended speech stream with multi-channel EEG: implications for
online, daily-life applications. J Neural Eng 12:046007.
Nicholls MER, Searle DA (2006) Asymmetries for the visual expression
and perception of speech. Brain Lang 97:322 –331.
Nieto-Castanon A, Ghosh SS, Tourville JA, Guenther FH (2003) Region
of interest based analysis of functional imaging data. Neuroimage
19:1303–1316.
Nuijten MB, Wetzels R, Matzke D, Dolan CV, Wagenmakers E-J (2015)
A default Bayesian hypothesis test for mediation. Behav Res
Methods 47:85–97.
Obleser J, Kayser C (2019) Neural entrainment and attentional selec-
tion in the listening brain. Trends Cogn Sci 23:913 –926.
Oostenveld R, Fries P, Maris E, Schoffelen J-M (2011) Fieldtrip: open
source software for advanced analysis of MEG, EEG, and invasive
electrophysiological data. Comput Intell Neurosci 2011:1 –9.
O’Sullivan JA, Power AJ, Mesgarani N, Rajaram S, Foxe JJ,
Shinn-Cunningham BG, Slaney M, Shamma SA, Lalor EC (2015)
Attentional selection in a cocktail party environment can be
decoded from single-trial EEG. Cereb Cortex 25:1697 –1706.
Park H, Kayser C, Thut G, Gross J (2016) Lip movements entrain the
observers’ low-frequency brain oscillations to facilitate speech
intelligibility. Elife 5:e14521.
Peelle JE (2018) Listening effort: how the cognitive consequences of
acoustic challenge are re ﬂected in brain and behavior. Ear Hear
39:204–214.
Peelle JE, Sommers MS (2015) Prediction and constraint in audiovi-
sual speech perception. Cortex 68:169 –181.
Pelli DG (1997) The VideoToolbox software for visual psychophysics:
transforming numbers into movies. Spat Vis 10:437 –442.
Peterson MF, Eckstein MP (2013) Individual differences in eye move-
ments during face identi ﬁcation re ﬂect observer-speci ﬁc optimal
points of
ﬁxation. Psychol Sci 24:1216 –1225.
Pﬁster R, Schwarz K, Janczyk M, Dale R, Freeman J (2013) Good
things peak in pairs: a note on the bimodality coef ﬁcient. Front
Psychol 4:1–4.
Rahne T, Fröhlich L, Plontke S, Wagner L (2021) In ﬂuence of surgical
and N95 face masks on speech perception and listening effort in
noise. PLOS One 16:e0253874.
R Core Team (2022) R: a language and environment for statistical
computing [computer software]. R Foundation for Statistical
Computing. Available at: https:/ /www.R-project.org/
Remez RE (2012) Three puzzles of multimodal speech perception. In:
Audiovisual speech processing (Vatikiotis-Bateson E, Bailly G,
Perrier P, eds), pp 4 –20. Cambridge: Cambridge University Press.
Rennig J, Beauchamp MS (2018) Free viewing of talking faces reveals
mouth and eye preferring regions of the human superior temporal
sulcus. Neuroimage 183:25 –36.
Research Article: New Research 15 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 15 of 16
Ross LA, Molholm S, Butler JS, Bene VAD, Foxe JJ (2022) Neural cor-
relates of multisensory enhancement in audiovisual narrative
speech perception: a fMRI investigation. Neuroimage 263:119598.
Ross LA, Saint-Amour D, Leavitt VM, Javitt DC, Foxe JJ (2007) Do you
see what I am saying? Exploring visual enhancement of speech com-
prehension in noisy environments. Cereb Cortex 17:1147–1153.
Schäfer PJ, Corona-Strauss FI, Hannemann R, Hillyard SA, Strauss DJ
(2018) Testing the limits of the stimulus reconstruction approach:
auditory attention decoding in a four-speaker free ﬁeld environ-
ment. Trends Hear 22:1 –12.
Schubert J, Schmidt F, Gehmacher Q, Bresgen A, Weisz N (2023)
Cortical speech tracking is related to individual prediction tenden-
cies. Cereb Cortex 33:6608 –6619.
Schwartz JL (2010) A reanalysis of McGurk data suggests that audio-
visual fusion in speech perception is subject-dependent. J Acoust
Soc Am 127:1584 –1594.
Slaney M (1998) Auditory toolbox. Interval Research Corporation,
10(1998), 1194.
Smith SM, Nichols TE (2009) Threshold-free cluster enhancement:
addressing problems of smoothing, threshold dependence and
localisation in cluster inference. Neuroimage 44:83 –98.
Stacey PC, Kitterick PT, Morris SD, Sumner CJ (2016) The contribution
of visual information to the perception of speech in noise with and
without informative temporal ﬁne structure. Hear Res 336:17 –28.
Suess N, Hauswald A, Reisinger P, Rösch S, Keitel A, Weisz N (2022a)
Cortical tracking of formant modulations derived from silently pre-
sented lip movements and its decline with age. Cereb Cortex
32:4818–4833.
Suess N, Hauswald A, Zehentner V, Depireux J, Herzog G, Rösch S,
Weisz N (2022b) In ﬂuence of linguistic properties and hearing
impairment on visual speech perception skills in the German lan-
guage. PLOS One 17:e0275585.
Sumby WH, Pollack I (1954) Visual contribution to speech intelligibility
in noise. J Acoust Soc Am 26:212 –215.
Summerﬁeld Q, Bruce V, Cowey A, Ellis AW, Perrett DI (1992)
Lipreading and audio-visual speech perception. Philos Trans R
Soc Lond B Biol Sci 335:71 –78.
Suñer C, Coma E, Ouchi D, Hermosilla E, Baro B, Rodríguez-Arias MÀ,
Puig J, Clotet B, Medina M, Mitjà O (2022) Association between
two mass-gathering outdoor events and incidence of
SARS-CoV-2 infections during the ﬁfth wave of COVID-19 in north-
east Spain: a population-based control-matched analysis. Lancet
Reg Health Eur 15:100337.
Taulu S, Kajola M (2005) Presentation of electromagnetic multichannel
data: the signal space separation method. J Appl Phys 97:124905.
Taulu S, Simola J (2006) Spatiotemporal signal space separation
method for rejecting nearby interference in MEG measurements.
Phys Med Biol 51:1759.
Thorpe S, Fize D, Marlot C (1996) Speed of processing in the human
visual system. Nature 381:520 –522.
Tiippana K, Andersen TS, Sams M (2004) Visual attention modulates
audiovisual speech perception. EJCP 16:457 –472.
Toscano JC, Toscano CM (2021) Effects of face masks on speech rec-
ognition in multi-talker babble noise. PLOS One 16:e0246842.
Truong TL, Beck SD, Weber A (2021) The impact of face masks on the
recall of spoken sentences. J Acoust Soc Am 149:142 –144.
Vallat R (2018) Pingouin: statistics in Python. J Open Source Softw
3:1026.
VanRullen R, Thorpe SJ (2001) The time course of visual processing:
from early perception to decision-making. J Cogn Neurosci
13:454–461.
van Wassenhove V, Grant KW, Poeppel D (2005) Visual speech speeds
up the neural processing of auditory speech. Proc Natl Acad Sci
U S A 102:1181 –1186.
Vehtari A, Gabry J, Magnusson M, Yao Y, Bürkner P-C, Paananen T,
Gelman A (2022a) loo: ef ﬁcient leave-one-out cross-validation
and WAIC for Bayesian models [computer software]. Available at:
https:/ /mc-stan.org/loo/
Vehtari A, Gelman A, Gabry J (2017) Practical Bayesian model evalua-
tion using leave-one-out cross-validation and WAIC. Stat Comput
27:1413–1432.
Vehtari A, Gelman A, Simpson D, Carpenter B, Bürkner P-C (2021)
Rank-normalization, folding, and localization: an improved R^ for
assessing convergence of MCMC (with discussion). Bayesian
Anal 16:667–718.
Vehtari A, Simpson D, Gelman A, Yao Y, Gabry J (2022b) Pareto
smoothed importance sampling (arXiv:1507.02646). arXiv.
Virtanen P, et al. (2020) Scipy 1.0: fundamental algorithms for scientiﬁc
computing in Python. Nat Methods 17:261 –272.
Waskom ML (2021) Seaborn: statistical data visualization. J Open
Source Softw 6:3021.
Wickham H (2016) Ggplot2: elegant graphics for data analysis ,E d2 .
Cham: Springer-Verlag New York.
Wilkinson GN, Rogers CE (1973) Symbolic description of factorial mod-
els for analysis of variance. J R Stat Soc Ser C Appl Stat 22:392–399.
Yuan Y, MacKinnon DP (2009) Bayesian mediation analysis. Psychol
Methods 14:301–322.
Zhang L, Du Y (2022) Lip movements enhance speech representations
and effective connectivity in auditory dorsal stream. Neuroimage
257:119311.
Research Article: New Research 16 of 16
February 2025, 12(2). DOI: https://doi.org/10.1523/ENEURO.0368-24.2024. 16 of 16
