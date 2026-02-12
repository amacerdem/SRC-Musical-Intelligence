# neural-representations-of-beat-and-rhythm-in-motor

Received: August 8, 2023. Revised: September 16, 2024. Accepted: September 23, 2024 
© The Author(s) 2024. Published by Oxford University Press. 
This is an Open Access article distributed under the terms of the Creative Commons Attribution Non-Commercial License (https://creativecommons.org/ 
licenses/by-nc/4.0/), which permits non-commercial re-use, distribution, and reproduction in any medium, provided the original work is properly cited. For 
commercial re-use, please contact journals.permissions@oup.com 
Cerebral Cortex, 2024,34, bhae406
https://doi.org/10.1093/cercor/bhae406
Advance access publication date 10 October 2024
Original Article
Neural representations of beat and rhythm in motor and 
association regions 
Joshua D. Hoddinott 1,2, *, Jessica A. Grahn1,2,3 
1 Centre for Brain and Mind, University of Western Ontario, Perth Drive, London, Ontario N6A 5B7, Canada 
2 Western Institute for Neuroscience, University of Western Ontario, 1151 Richmond Street, London, Ontario N6A 3K7, Canada 
3 Psychology Department, University of Western Ontario, 1151 Richmond Street, London, Ontario N6A 3K7, Canada 
*Corresponding author: Joshua D . Hoddinott, Western Interdisciplinary Research Building, University of Western Ontario, Perth Drive, London, Ontario N6A 5B7, 
Canada. Email: jhoddin@uwo.ca 
Humans perceive a pulse, or beat, underlying musical rhythm. Beat strength correlates with activity in the basal ganglia and 
supplementary motor area, suggesting these regions support beat perception. However, the basal ganglia and supplementary motor 
area are part of a general rhythm and timing network (regardless of the beat) and may also represent basic rhythmic features (e.g. 
tempo, number of onsets). T o characterize the encoding of beat-related and other basic rhythmic features, we used representational 
similarity analysis. During functional magnetic resonance imaging, participants heard 12 rhythms—4 strong-beat, 4 weak-beat, and 4 
nonbeat. Multi-voxel activity patterns for each rhythm were tested to determine which brain areas were beat-sensitive: those in which 
activity patterns showed greater dissimilarities between rhythms of different beat strength than between rhythms of similar beat 
strength. Indeed, putamen and supplementary motor area activity patterns were significantly dissimilar for strong-beat and nonbeat 
conditions. Next, we tested whether basic rhythmic features or models of beat strength (counterevidence scores) predicted activity 
patterns. We found again that activity pattern dissimilarity in supplementary motor area and putamen correlated with beat strength 
models, not basic features. Beat strength models also correlated with activity pattern dissimilarities in the inferior frontal gyrus and 
inferior parietal lobe, though these regions encoded beat and rhythm simultaneously and were not driven by beat alone. 
Key words: basal ganglia; fMRI; rhythm; Mvpa; SMA. 
Introduction 
Regular rhythms, in which onsets often align with an evenly timed 
metric “grid,” elicit a strong sense of an underlying pulse or “beat” 
unfolding in time with the rhythm (Bouwer et al. 2018). Compared 
to irregular rhythms, which do not give rise to a beat, regular (or 
strong-beat) rhythms elicit greater activity in the supplementary 
motor area (SMA) and basal ganglia, specifically the putamen, 
bilaterally (
Chen et al. 2006, 2008a; Grahn and Brett 2007; 
Bengtsson et al. 2009; Grahn and Rowe 2009, 2013; Chapin et al. 
2010; Matthews et al. 2020; Hoddinott et al. 2021), suggesting 
these regions are involved in beat perception. The basal ganglia 
and SMA also activate during rhythms with no beat (but less 
than when a beat is present), suggesting that regional activity 
may relate to more than just beat, and other features of rhythm 
(such as tempo) may be represented. Representation of rhythmic 
features in beat-sensitive regions may be overlooked in previous 
studies due to the coarse nature of univariate analyses, in which 
activity is averaged across voxels in a region, and across stimuli in 
a condition, obscuring differences in rhythmic features between 
individual rhythms. Here, we employ more sensitive multivariate 
pattern analyses (MVPAs) to test whether SMA and basal ganglia 
activity represent only beat strength or if these regions are also 
sensitive to other individual rhythmic features. We also used these 
analyses to examine whether other regions showed evidence of 
representing the beat, as this evidence may have been obscured 
in univariate analyses. 
The basal ganglia and SMA are key components in a striatal 
cortical loop involved in beat perception. During the presentation 
of rhythms with a strong beat, functional connectivity between 
the basal ganglia, SMA, and auditory sensory areas is increased 
(
Grahn 2009), perhaps ref lecting inter-regional communication of 
external auditory events (via auditory cortex) and internal beat-
based predictions (via SMA and basal ganglia) (
Cannon and Patel 
2021). Of these regions, the basal ganglia are particularly crucial 
to beat perception, as patients with Parkinson’s disease (in which 
basal ganglia function is compromised) show a selective deficit 
for strong-beat rhythms in discrimination tasks (
Grahn and Brett 
2009). The basal ganglia’s role in beat perception may relate to 
prediction, as putamen activity is greatest while maintaining (i.e. 
predicting) an ongoing beat, compared to initially detecting a beat 
(Grahn and Rowe 2013). There is also strong evidence for beat 
sensitivity in the SMA, in which activity is greatest for rhythms 
with a strong beat compared to nonbeat rhythms (
Grahn and 
Brett 2007; Grahn and Rowe 2009, 2013) and predicts subjective 
beat perception ability—individuals who easily detect a beat have 
greater beat-related SMA activity than individuals who find it 
more difficult to perceive a beat (
Grahn and McAuley 2009; Grahn 
and Schuit 2012). The mechanistic role of the SMA in beat percep-
tion is less clear, though its involvement in temporal processing 
across nonrhythmic tasks suggests that the SMA may encode 
rhythm or temporal information in general, not just when a beat 
is present.
2 | Cerebral Cortex, 2024, Vol. 34, No. 10
The SMA and basal ganglia encode temporal features in 
nonrhythmic tasks and across sensory domains, suggesting that 
general temporal processing may drive activity during rhythm 
perception, in addition to beat-related activity . For example, 
SMA, caudate, and putamen activate during auditory and tactile 
temporal discrimination—detecting whether one or two events 
were presented sequentially (
Pastor et al. 2004, 2006). Putamen 
activity during temporal discrimination corresponds to individual 
perceptual certainty—putamen activity is greatest when subjects 
are highly consistent in their responses (
Pastor et al. 2008), 
perhaps ref lecting the accuracy of temporal encoding during 
the task. Similarly , duration estimation tasks recruit the SMA and 
basal ganglia, in addition to inferior frontal gyri (IFGs) and insular 
cortices (
Coull et al. 2015). Activity in the SMA increases as interval 
duration increases and corresponds to subjective overestimation 
of the intervals—greater SMA activity during initial encoding 
of the interval increased the likelihood for the duration to be 
overestimated behaviorally , suggesting that SMA activity relates 
to temporal interval encoding accuracy (
Coull et al. 2015). 
Indeed, recent work has shown SMA activity encodes visually 
presented intervals in a “chronotopic map” such that different 
interval durations activate distinct topographic regions across 
the supplementary motor cortex (
Protopapa et al. 2019), akin to 
the “tonotopic” maps of pitches in auditory cortex ( Humphries 
et al. 2010). Using multi-interval sequences, the SMA and basal 
ganglia activate during encoding of visually presented sequences 
of temporal intervals (i.e. visual rhythms; Schubotz and von 
Cramon 2001), and the SMA exhibits distinct multivoxel activation 
patterns for the timing and order of learned finger-press 
sequences ( Kornysheva and Diedrichsen 2014), suggesting that 
both the perception and production of multi-interval timing is 
represented in the SMA and basal ganglia. Thus, the activity in the 
SMA and basal ganglia during auditory rhythm perception is likely 
to (at least partially) represent the rhythms themselves—the mul-
tiduration intervals making up the rhythmic sequences—though 
this has not been shown when also controlling for beat strength. 
Because the SMA and basal ganglia respond generally to tem-
poral processing across tasks and modalities, these motor regions 
are likely responsible for encoding auditory rhythms, regardless of 
beat presence. However, in one auditory rhythm perception study , 
a linear classifier could not accurately discriminate between two 
rhythms based on SMA activity patterns (
Notter et al. 2019)b u t 
could discriminate based on the left and right temporoparietal 
junction and the right IFG patterns. The SMA, though, was found 
to be part of a broad network that distinguished between multi-
interval rhythms and an isochronous metronome. 
Notter et al. 
(2019) suggest that this network may ref lect difficulty differences 
between rhythms and metronome, rather than multi-interval 
encoding, especially for regions not known to be involved in timing 
(e.g. the lateral occipital lobe). However, the SMA may represent a 
stimulus feature that is balanced across the rhythms but absent 
in the metronome, preventing classification between the rhythms 
but enabling it between rhythms and metronome. For example, 
the two rhythms had the same number of short, medium, and 
long intervals, and the metronome only had one repeating inter-
val, so if the durations of multiple intervals were being encoded 
(regardless of their order), both rhythms would elicit identical 
activity . Similarly , both rhythms were metric and could elicit the 
internal generation of a beat, whereas metronomes do not require 
the internal generation of a beat. Thus, it is possible that the 
SMA (and perhaps other regions) encoded either the presence of a 
beat or basic features common to both rhythms, allowing a clas-
sifier to distinguish between rhythms and a metronome but not 
between the rhythms themselves. The SMA may encode individ-
ual rhythms, based on temporal features such as interval lengths 
or tempo, in addition to beat strength. Thus, more evidence is 
needed to characterize the neural representation of rhythm and 
beat to determine whether rhythm perception regions show dif-
ferent activity patterns based on beat strength or other basic 
rhythmic features or both. 
One method to characterize neural representations in func-
tional magnetic resonance imaging (fMRI) is representational sim-
ilarity analysis (RSA). RSA operates under the assumption that 
neurons, and more widely neuronal populations, are tuned to 
specific stimulus features. For example, an auditory neuron may 
fire specifically for sound frequencies near 440 Hz but not other 
frequencies (
Bendor and Wang 2005). T o communicate informa-
tion downstream, any “tuned” region must output activity that is 
consistent and sufficiently distinct to be decoded by the region 
receiving the input. Although fMRI has a coarser spatial resolution 
than single neuron recordings, it can still show differences in 
the tuning of populations of neurons to a task, stimulus, or a 
combination of stimulus features. Thus, RSA measures encod-
ing by the relative dissimilarity (i.e. the “decodability”) between 
activity patterns for stimuli that differ along the encoded feature 
(
Kriegeskorte et al. 2008). For example, a region that encodes 
beat strength may exhibit dissimilar activity patterns across its 
voxels in response to rhythms that have a strong beat versus 
no beat but similar patterns for different rhythms with similar 
beat strength. Therefore, RSA can quantify dissimilarities between 
multivoxel activity patterns for individual rhythms and determine 
how stimulus features (such as beat strength) are represented 
across different brain regions. 
Representational similarity analysis is a form of MVPA, which 
provides complementary information to traditional univariate 
analysis. In some cases, MVPA is more sensitive than univariate 
analysis. For example, when learning motor sequences, average 
regional activity may increase or decrease across training, while 
multivariate activity patterns for each motor sequence become 
more distinct from each other, suggesting that the neural repre-
sentation of individual trained motor sequences is strengthened 
(
Wiestler and Diedrichsen 2013). Univariate analysis is appropri-
ate for identifying regions involved in a task; however, MVPA is 
better equipped to characterize how information is represented in 
an involved region (
Mur et al. 2009). Although several neuroimag-
ing studies have shown motor region involvement during rhythm 
and beat perception, to date, none have examined how rhythms 
are represented in regional activity patterns. For example, certain 
brain areas may be sensitive only to the presence or absence of a 
beat, or they may also encode additional rhythmic features. 
In this experiment, we characterized the neural represen-
tations of rhythm and beat perception using RSA and high-
resolution 7-Tesla fMRI. During MRI scanning, participants 
listened to a set of 12 unique rhythms taken from previous beat 
perception work (
Grahn and Brett 2007). Of the 12 rhythms, 4 had a 
strong beat, 4 had a weak beat, and 4 had no beat. Activity patterns 
for each rhythm were extracted from the a priori areas of interest 
(SMA, basal ganglia), as well as the whole brain. We predicted 
general rhythm encoding in the SMA and basal ganglia—highly 
dissimilar multivariate patterns between all rhythms. If the SMA 
and basal ganglia are sensitive mainly to beat strength, we would 
predict greater dissimilarity between strong-beat and weak- and 
nonbeat rhythms, compared to within-condition dissimilarities 
(e.g. the dissimilarity between patterns for the 4 strong-beat 
rhythms). Across the whole brain, we predicted rhythm encoding 
in the rhythm perception network, including the IFG, premotor
Hoddinott and Grahn | 3
Table 1. Rhythm list including interval ratios and absolute durations. 
Interval ratios Base unit (ms) Interval durations (ms) 
Strong Beat 112314 
311322 
2113113 
3141111 
270 
250 
230 
250 
270,270,810,270,1080 
750,250,250,750,500,500 
460,230,230,690,230,230,690 
750,250,1000,250,250,250,250 
Weak Beat 323211 
412212 
1411311 
2141211 
270 
250 
230 
250 
810,540,810,540,270,270 
1000,250,500,500,250,500 
230,920,230,230,690,230,230 
500,250,1000,250,500,250,250 
Non beata 132321 
221241 
2123211 
3221112 
270 
250 
230 
250 
270,972,378,972,378,270 
350,350,250,350,1000,250 
322,230,322,828,322,230,230 
900,350,350,250,250,250,350 
a Note: For nonbeat rhythms, 2 = 1.4 and 3 = 3.6 interval ratios. 
cortex (PMC), auditory cortex, inferior parietal lobe (IPL), basal 
ganglia, and cerebellum. We also examined these areas for 
evidence of beat sensitivity , which may have been obscured by 
regional averaging in previous univariate studies. 
Materials and methods 
Participants 
A sample of 26 healthy young adults (14 female) participated in 
the study . Most participants reported music-playing experience 
(M= 6.54 years,SD= 5.20 years). Participants were excluded if they 
reported neurological impairment, use of psychotropic medica-
tion at the time of study , difficulty hearing, or if they did not meet 
general MRI environment safety criteria, such as metal in the body 
or a history of claustrophobia. All participants were compensated 
for their time monetarily , and procedures were approved by the 
Health Sciences Research Ethics Board at Western University . 
Stimuli 
Four auditory rhythms were generated for each of the 3 
beat-strength conditions: strong-beat, weak-beat, and nonbeat 
rhythms. T welve rhythms were taken from a larger set used in 
previous work (
Grahn and Brett 2007; Grahn 2012); see T able 1 
for a list of stimuli. Rhythms were composed of 500 Hz sine-
wave tones. T o aid perception in an acoustically noisy scanner 
environment, the tones “filled” most of the duration of each 
interval in the rhythms, ending 40 ms short of the specified 
duration to leave a 40 ms silent “gap” to demarcate the tone onsets 
(as in previous work, 
Grahn and Brett 2007). Thus, the interval 
durations for each rhythm were the tone interonset intervals. 
Each tone had 8 ms onset/offset ramps. Rhythms included 6 or 7 
intervals and were about 3 s in duration. A final tone, the length of 
the shortest interval in the rhythm, was appended to the end of all 
sequences, such that the end of the final interval was demarcated 
by the final tone’s onset. 
Strong- and weak-beat rhythms were composed of integer-ratio 
intervals, such that interval durations were multiples of the short-
est interval (i.e. 1:2:3:4). In nonbeat rhythms, the “2” and “3” inter-
vals were replaced by 1.4 and 3.6 noninteger ratios (1:1.4:3.6:4), 
creating irregularity . Rhythms were presented at 3 different tempi, 
with the smallest interval being 230, 250, or 270 ms. Each beat-
strength condition had 1 fast, 1 slow , and 2 medium tempo 
rhythms. Strong-beat rhythms contained interval arrangements 
that induced a perceptual accent at evenly spaced time points— 
at the beginning of each group of four units, marking the location 
of the beat (
Povel and Essens 1985). Weak-beat rhythm intervals 
were arranged such that perceptual accents did not occur at 
evenly spaced time points, making any potential beat difficult 
to detect (
Grahn and Brett 2007; Grahn 2012). Additionally , the 
noninteger ratios of the nonbeat rhythms eliminated regularity 
and necessarily led to irregularly spaced perceptual accents, such 
that no beat existed in the rhythm at all. During the fMRI scan, 
participants performed a discrimination task (comparing whether 
the third rhythm in a trial was the same as or different from the 
first two rhythms in that trial); therefore, a discrimination target 
rhythm was created for each stimulus by switching the order of 
the third and fourth intervals in the original rhythm. 
Procedure 
Rhythm discrimination task 
While in the scanner, participants performed 8 blocks of the 
rhythm discrimination task. Each block lasted ∼7 min. Within 
each block, every rhythm was presented on 2 trials, resulting in 
24 total trials per block. Each trial included two presentations of 
a rhythm, with the screen depicting “First Listen” and “Second 
Listen” in text, followed by a presentation of the target rhythm. 
On half of the trials, the same rhythm, on the other half, a 
deviant rhythm in which the order of third and fourth intervals are 
switched. During the target rhythm, the screen displayed “T arget 
Rhythm: Same or Different?”. The target rhythm was followed by 
a 2-s response window with the text “Was the rhythm same or 
different? 1st finger = same, 2nd finger = different” in red letters on 
a black background. While this screen was displayed, participants 
responded via button press with either the index or middle finger 
of their right hand. Each rhythm was separated by a 1,300-ms 
interstimulus interval. Some trials were separated by an extended 
intertrial interval, unrelated to the task, to allow for silent baseline 
data collection. Stimuli were presented in a random order in every 
block. Before entering the scanner, participants were instructed 
how to complete the task and familiarized with the screens and 
response requirements. Participants were instructed to keep very 
still during the scan and specifically asked not to tap along with 
the rhythms. 
Demographics questionnaire 
After the scan, participants completed a demographics question-
naire that asked about age, gender, and musical experience. 
Image acquisition and preprocessing 
A Siemens MAGNETOM 7T MRI scanner was used to collect 
anatomical and functional images at the Center for Functional 
and Metabolic Mapping, Western University . An anatomical T1
4 | Cerebral Cortex, 2024, Vol. 34, No. 10
image was collected after the first 4 functional runs. A head-
only AC84 II gradient engine will be used with an 8-channel 
transmit/32-channel receive whole-head array . T2∗-weighted 
echo-planar imaging (EPI) data were collected using a 1-s TR, 
22-ms TE, with a multiband acceleration factor of 3 and a 30
◦ fl i p 
angle. EPI data were collected from 2 mm isotropic voxels in a 104 
× 104×60 matrix. 
SPM12 was used to preprocess the images. Functional and 
anatomical images were visually inspected and, when necessary , 
reoriented to be in a similar orientation. T o account for subject 
movement, functional images were realigned to the mean 
functional image using second-degree B-spline interpolation. 
Each subject’s functional images were then coregistered with 
their anatomical T1 image with a normalized mutual information 
cost function. T1 images were skull-stripped and segmented into 
gray-matter, white-matter, and cerebrospinal maps using the 
segment function and tissue probability maps included with 
SPM12. Multivariate analysis was performed on unsmoothed 
images in native space. For univariate analysis, coregistered 
images were spatially smoothed with an 8-mm full-width half-
maximum kernel. Smoothed images were then spatially warped 
to Montreal Neurological Institute (MNI) template space before 
the first-level general linear model (GLM) was estimated. 
First-level modeling 
Univariate 
A first-level GLM was implemented on the smoothed MNI-space 
functional images for each session. Independent regressors were 
entered for each beat strength condition (strong-, weak-, and 
nonbeat) and aligned to the onset of the first rhythm presentation 
and offset of the second presentation in each trial (thus covering 
the entire 2 presentations of a rhythm). The target rhythm (third 
presentation), button response, and 6 movement regressors were 
also entered into the first-level GLM. All trial regressors were 
modeled using an on–off boxcar method convolved with a canon-
ical hemodynamic response function. Ultimately , the analysis 
resulted in one baseline-corrected (beta) image for each beat 
strength condition (modeling the first two presentations of a 
rhythm on a trial; target rhythms and responses were entered 
as nuisance regressors and not analyzed at the second level), for 
each subject. After this step, each subject’s 3 baseline-corrected 
images (1 image per each beat strength condition) were used in the 
second-level analysis, including a one-way repeated-measures 
ANOV A using SPM12’s f lexible factorial model. 
Multivariate: item-wise 
The main RSA analysis was performed on item-wise activity 
patterns—one for each of the 12 rhythms. T o calculate item-wise 
activity patterns, a first-level GLM was implemented indepen-
dently from the univariate GLM. For each session, independent 
regressors were entered for each of the 12 rhythms and aligned to 
the onset of the first rhythm presentation and offset of the second 
presentation in each trial (thus covering the entire 2 presentations 
of a rhythm). As in the univariate GLM, the target rhythm, button 
response, and 6 movement regressors were also entered. All trial 
regressors were created using an on–off boxcar method convolved 
with a canonical hemodynamic response function. This analysis 
resulted in eight baseline-corrected (beta weight) images for each 
rhythm (one per run), for a total of 96 images. 
Multivariate: condition-wise 
The condition-wise GLM was identical to the univariate GLM, 
except that it was performed on unsmoothed native-space func-
tional images. 
Region of interest definition 
The left and right pallidum, putamen, caudate, and SMA were the 
regions of interest (ROIs). Binary masks were created in MNI space 
using anatomically defined regions from the AAL3 atlas (
Rolls 
et al. 2020). Masks were then warped from MNI space to each 
subject’s native space using the SPM12 deformation tool and the 
inverse of the affine transformation matrix generated from the 
normalization step (see 
Image Acquisition and Preprocessing). All 
native-space ROIs were visually inspected for accuracy . 
Whole-brain volumetric searchlight 
In addition to ROI analyses, we examined activity patterns across 
the whole brain. A volumetric searchlight was employed to test 
pattern dissimilarities in overlapping small spherical ROIs. The 
volumetric searchlight considered data from small spheres of 160 
voxels across each subject’s whole brain in native space. Each 
voxel in the functional mask was used as a searchlight center. For 
each searchlight center, the nearest 160 voxels were considered 
for the activity pattern calculation. If a minimum of 160 voxels 
were not present in a sphere surrounding the searchlight center 
(e.g. on the edges of the functional mask), voxels nearest to 
the center (calculated by Euclidean distance, up to a maximum 
30 mm radius) were added to the searchlight until ∼160 voxels 
were present. 
For group-level analysis of the whole-brain searchlight, all 
averaging of the crossnobis distances (see Results) was performed 
in native space, creating whole-brain average crossnobis distance 
maps for each subject. Average crossnobis distances more than 
4 times the interquartile range were removed from the whole-
brain maps for each subject. The average crossnobis distance 
maps were then warped to MNI space for group-level testing. For 
the feature-encoding analysis (see below), a group-level map of 
possible beat-encoding regions was reverse-warped from MNI to 
native space to extract the full item-wise representational dissim-
ilarity matrices (RDMs), which were averaged across searchlights 
contained in each cluster of the group-level map. 
Representational similarity analysis 
Univariate analyses average across fine-grained spatial patterns 
across voxels, thus only detecting overall increases or decreases in 
activity across a region. Multivariate pattern analysis quantifies 
patterns across multiple voxels and can detect item-specific 
activity patterns (
Mur et al. 2009). We used RSA, a multivariate 
technique that tests for the encoding or representational 
specificity of regional activity by comparing the dissimilarity 
between multivariate activity patterns elicited by different stimuli 
(
Kriegeskorte et al. 2008). Dissimilarity ref lects sensitivity to dif-
ferences in features between stimuli, such as the strength of the 
beat. We tested whether well-established beat-sensitive regions 
(i.e. the SMA and basal ganglia) encode individual rhythms regard-
less of beat (rhythm-encoding; Fig. 1B), or if activity patterns differ 
only according to beat strength (beat encoding; Fig. 1A), or if they 
showed both rhythm and beat encoding, in which activity patterns 
differ across individual rhythms, but with the greatest dissimilar-
ity between rhythms of different beat strengths (
Fig. 1C). T o test 
for these different types of encoding patterns, we performed RSA 
in each ROI and across the whole brain (using a searchlight) on 
12 activity patterns—one for each of the 12 rhythms. 
Dissimilarity metric: cross-validated Mahalanobis distance 
estimate 
Dissimilarities between activity patterns were quantified by the 
cross-validated Mahalanobis (“crossnobis”) distance estimate
Hoddinott and Grahn | 5
Fig. 1. Example activity pattern orientations in a 2-voxel ROI. Axes represent activity in each voxel. Small circles represent the 2-voxel activity patterns 
for individual rhythms; larger clouds show mean groupings. A–C) shows the theoretical layout for regions encoding beat A), individual rhythms B), or 
a combination of beat and rhythm C). Solid lines show the within-condition distances or the dissimilarity between rhythms of the same beat strength; 
dashed lines show the between-condition distances or the dissimilarity between rhythms of different beat strengths. Insets show the mean within-
condition distances (left bars) and between-condition distances (right bars). In all 3 panels, significant between-condition distances would be found: 
Average distances between conditions would be greater than 0. However, true beat encoding is only present in A and C), as the between-condition 
distances are greater than the within-condition distances, on average. Differently , in B), the region activates in a unique pattern for each rhythm but 
does not distinguish on the basis of beat-strength—between-condition distances are equal to the within-condition distances. 
( Diedrichsen et al. 2016). The distance estimate is similar to 
machine learning classifiers that classify items into groups 
based on the dissimilarity between activity patterns. However, 
the crossnobis distance returns a continuous measure of 
the dissimilarity between patterns, rather than a discretized 
classification accuracy , and is therefore informative about how 
much dissimilarity exists between activity patterns. T o calculate 
the crossnobis distance, each stimulus was assigned a BOLD 
activity pattern consisting of beta weights from the first-level 
multivariate GLM (see Multivariate Modeling section below) for 
each voxel within an ROI or searchlight. For each of the 8 imaging 
runs, the activity patterns were multivariate noise normalized 
using the variance–covariance matrix of the first-level GLM 
residuals (
Walther et al. 2016). Multivariate noise normalization 
downweighs the contribution of voxels relative to their residual 
variance (variance–covariance diagonal) and its correlational 
structure with other voxels included in the matrix (variance– 
covariance off diagonal). Because noise can be unique to each 
run, multivariate noise normalization was performed for each of 
the 8 functional runs independently . 
Noise-normalized activity patterns were cross-validated using 
a leave-one-run-out approach. T o cross-validate, distances 
between activity patterns were averaged across all but one 
imaging run. The distance was also calculated between activity 
patterns for the left-out run. Next, the inner product of the 
run-averaged distance and the left-out run distance vectors 
was calculated. The inner product reveals the consistency and 
magnitude of the two distance vectors, with 0 meaning no 
dissimilarity , and a possibility for negative distance if the vectors 
are in different spatial orientations—suggesting the dissimilarity 
is highly inconsistent across runs. The cross-validation steps 
were repeated by switching the left-out run on each iteration 
until all 8 runs were left out. The average of the 8 resulting inner 
products for each stimulus pair was taken as the cross-validated 
distance. Thus, each ROI and searchlight center exhibited 66 
crossnobis distances per subject. Multivariate pattern analysis 
was performed in Matlab using the rsa toolbox (
Nili et al. 2014), 
pcm toolbox (Diedrichsen et al. 2018), and custom code. 
Summary statistic: categorically averaged Crossnobis 
distances 
Pairwise dissimilarities were averaged into 3 within-condition 
categories, measuring the mean dissimilarity between rhythms 
of the same beat strength: (i) strong-beat vs. strong-beat (SB-SB); 
(ii) weak-beat vs. weak-beat (WB-WB); and (iii) nonbeat vs. non-
beat (NB-NB). Additionally , 3 between-condition categories were 
calculated, measuring the mean dissimilarity between rhythms 
of different beat strengths: 1. Strong-beat vs. weak-beat (SB-WB); 
2. Strong-beat vs. nonbeat (SB-NB); and 3. Weak-beat vs. nonbeat 
(WB-NB). 
Feature-encoding analysis: model testing 
Although we categorized rhythms into three beat-strength con-
ditions, individual rhythms also vary on features unrelated to 
beat. Neural patterns across rhythms may be partially driven by 
stimulus features unrelated to beat strength (e.g. tempo). Further, 
high-level features like beat strength may not be categorical, 
but continuous, with beat strength differing across stimuli even 
within one beat-strength condition. Activity patterns may there-
fore be sensitive to these continuous differences. T o test whether 
more continuous models of beat strength, as well as other rhyth-
mic features, explained the representational structure in our 
regions of interest, we created nine representational models relat-
ing to different rhythmic features and correlated the models with 
the neural item-wise representational dissimilarity matrices. 
Nine models were created by assigning each of the 12 rhythms 
a vector representing the degree of the feature being modeled 
and then computing the squared Euclidean distance between the 
feature vectors for each rhythm (feature vectors and resulting 
representational models can be found in 
Supplemental Fig. 2 ). 
Thus, each value in a model RDM represents how dissimilar two 
rhythms are based on a given feature, identically to the neural 
RDMs representing the dissimilarity between activity patterns. 
The nine representational models were organized into three 
categories: basic feature models, condition-encoding models, 
and beat-strength models. Basic feature models included (i) the 
number of onsets, (iii) the number of different interval lengths (i.e. 
the number of 1-, 2-, 3-, and 4-duration intervals in each rhythm), 
and (iii) tempo. The condition-encoding models tested whether 
one beat-strength condition was represented uniquely from all 
other conditions. Thus, there was an independent encoding model 
for (iv) only strong-beat encoded, (v) only weak-beat encoded, 
and (vi) only nonbeat encoded. Finally , the beat-strength models 
tested whether the beat-strength representation was (vii) equal 
(rhythms of the same beat strength are not dissimilar, and 
are equally dissimilar to rhythms of different beat strength),
6 | Cerebral Cortex, 2024, Vol. 34, No. 10
(viii) hierarchical (strong-beat rhythms are more dissimilar from 
nonbeat rhythms than from weak-beat rhythms), or (ix) sensitive 
to “counterevidence” using the beat counterevidence score (C-
Score) model from Povel and Essens (1985). Counterevidence 
scores were calculated for each rhythm using a 4/4 meter. Unlike 
the hierarchical beat strength model, the C-Score model indicates 
the beat strength of each individual rhythm. 
Using Pearson’s r, the 9 models were correlated with neu-
ral RDMs for each subject and ROI. Thus, a distribution of 26 
r-values was created for each model and ROI. T o establish the 
expected correlation value of a successful model, we calculated 
the upper and lower bounds of the noise ceiling independently 
for each ROI. Noise ceilings estimate the range within which 
the true explanatory model (i.e. a perfect model containing all 
features encoded by a region) can be expected to relate to the data, 
given the intersubject variability in the sample (
Lage-Castellanos 
et al. 2019). Thus, representational models that have correlations 
within the noise ceiling are likely to be an accurate estimate of 
the true representational structure of a region. Noise ceilings were 
created using a leave-one-subject-out approach ( Nili et al. 2014). 
For the lower bound, each subject’s neural RDM was correlated 
with the group-averaged RDM with that subject left out. The 
left-out subject was rotated until all subjects had been left out 
once. The lower bound of the noise ceiling is the average of 
each subject’s correlation with the group. The noise-ceiling upper 
bound is calculated in the same way as the lower bound, except 
that the “left-out” subject is still included in the group-averaged 
RDM, increasing the correlation between each subject and the 
group RDM. 
The feature-encoding analysis was performed on beat-
sensitive a priori ROIs and on candidate feature-encoding regions 
from the exploratory whole-brain searchlight. T o identify can-
didate feature-encoding regions, all searchlights with significant 
between-condition dissimilarities (compared to zero) were used in 
the feature-encoding analysis. Dissimilarities here may be driven 
by features that were balanced across beat-strength conditions 
(e.g. tempo), by features that change systematically across 
conditions (i.e. beat strength), or by a combination of features 
that differ between any set of individual rhythms. Therefore, 
comparisons in these regions are less controlled than the beat-
encoding analyses and should be considered exploratory . 
Results 
Behavioral performance 
Performance on the rhythm discrimination task was evaluated by 
calculating the percentage of correct trials for each beat strength 
condition. Overall, discrimination was significantly more accu-
rate for strong-beat rhythms (M= 78%, SD= 15%), compared to 
weak-beat (M= 68%, SD= 12%), t(24) = 3.99, P< 0.001, and nonbeat 
rhythms (M= 69%, SD= 13%), t(24) = 4.01, P < 0.001. Discrimination 
performance for weak-beat and nonbeat rhythms was not signif-
icantly different, t(24) =
− 0.44, P= 0.66. Due to a technical error, 
responses from two subjects were not recorded, and they were 
removed from this analysis. 
Univariate analysis 
As a preliminary data check, whole-brain univariate analyses 
compared activation during rhythm listening versus rest and 
differences between beat strength conditions. An [all rhythms 
> rest] contrast revealed activation in the rhythm perception 
network, including bilateral SMA, PMC, basal ganglia, cerebellum, 
and superior temporal gyrus (STG) (
Fig. 2). T o test for univari-
ate differences between beat strength conditions, a 1 × 3 (beat 
strength; strong, weak, non) repeated-measures ANOV A was per-
formed at the whole-brain level. A main effect of beat strength 
revealed greater activity in the striatum for strong-beat rhythms 
compared to nonbeat rhythms (
Fig. 2, right). The [strong-beat > 
weak-beat] and [weak-beat > nonbeat] contrasts did not reveal 
significantly different activation, and no other regions showed 
differences between beat strength conditions. 
Multivariate pattern analysis 
Multivariate activity patterns were analyzed in 8 a priori anatom-
ically defined ROIs (left and right SMA, caudate, pallidum, and 
putamen). T o determine whether activity patterns represented 
beat strength beyond that explained by individual rhythm 
encoding, the activity patterns from each rhythm (item-wise 
activity patterns) were extracted and tested for dissimilarity . Beat-
encoding regions will have greater dissimilarity between activity 
patterns of different beat strength (e.g. [Strong vs. Non]) than those 
with the same beat strength (e.g. [Strong vs. Strong]), in which 
beat strength is identical (
Fig. 1A and C). Thus, in each region, 
we tested whether the mean dissimilarities between rhythms of 
different beat strength conditions were greater than the mean 
dissimilarities within each beat strength condition combined (e.g. 
SB-WB > SB-SB+WB-WB). 
Are individual rhythms, beat strength, or both 
encoded in motor region activity? 
T o examine this question, the crossnobis distances between each 
of the 12 rhythms (66 pairwise distances) were averaged into 6 
categories of interest for statistical analysis—3 within-condition 
distances (SB-SB: strong vs. strong; WB-WB: weak vs. weak; and 
NB-NB: non vs. non), and 3 between-condition distances (SB-
WB: strong vs. weak; SB-NB: strong vs. non; and WB-NB: weak 
vs. non). Planned t-tests indicated whether significant within-
and/or between-condition distances were present ([SB-SB+WB-
WB+NB-NB> 0] & [SB-WB+SB-NB+WB-NB > 0], respectively) 
and to test for greater encoding of beat strength than individual 
rhythms by comparing each mean between-condition distance 
to its constituent within-condition distances (e.g. [SB-WB>SB-
SB+WB-WB]). 
Group mean crossnobis distances for the six comparisons are 
shown in Fig. 3. T o test for individual rhythm encoding while con-
trolling for beat strength, the 3 within-condition distances were 
averaged and tested against 0 using a one-sample t-test. Because 
within-condition distances control for beat strength, regions with 
significant within-condition distances are likely to encode some 
other rhythmic feature, such as tempo or number of onsets, which 
may differ between rhythms of the same beat strength. Of the 
8 ROIs, no regions had significant within-condition distances 
(all Ps >0.064). T o test whether beat sensitivity was detected in 
the item-wise activity patterns, the 3 between-condition mean 
distances were averaged and tested against 0 with a one-sample 
t-test. Of the 8 ROIs, 3 revealed significant between-condition 
distances: right putamen, t(25) = 2.74, P= 0.01; right caudate, 
t(25) = 2.16,P= 0.041; left SMA,t(25) = 2.13,P= 0.04. The SB-NB > SB-
SB+NB-NB test revealed significantly greater distances between 
strong-beat and nonbeat conditions compared to within strong-
beat and nonbeat conditions in 3 ROIs: left putamen, t(25) = 2.57, 
P= 0.017; left SMA t(25) = 2.07, P= 0.049; right SMA t(25) = 2.80, 
P= 0.01. All other Ps > 0.11. The SB-WB>SB-SB+WB-WB test 
revealed marginal differences in the left putamen, t(25) = 1.77, 
P= 0.089; and left caudate,t(25) = 1.97,P= 0.061. All other Ps > 0.17.
Hoddinott and Grahn | 7
Fig. 2. Univariate activation for [all rhythms > rest] (left) and [strong-beat > nonbeat] (right) contrasts. Across all rhythms, the rhythm perception 
network was active, including left and right SMA, STG, putamen, PMC, and cerebellum VI. Strong-beat rhythms revealed greater activation in the 
putamen compared to nonbeat rhythms. The [strong-beat > weak-beat] and [weak-beat > nonbeat] contrasts did not show significant whole-brain 
differences. 
Finally , the WB-NB >WB-WB+NB-NB test revealed only marginal 
differences in the left SMA, revealing greater within-conditions 
distances than between, t(25) = − 1.76, P= 0.09. All other Ps >0.13. 
Overall, this indicates that the left and right SMA and the left 
putamen encode beat strength: They show different voxel-wise 
activity patterns for rhythms with different beat strengths. The 
distances are greater between-condition than within-condition; 
thus, the effect is not caused by encoding any given rhythm with 
a unique activity pattern, but rather by more similar patterns 
for rhythms within a beat-strength category than between beat-
strength categories. 
Are mean activity patterns distinct between 
conditions? 
T o ensure that item-wise activity patterns are not only signifi-
cantly different between conditions because of high variability in 
one condition (e.g. Supplemental 1A), we followed up the item-
wise analysis by testing whether the condition-wise activity pat-
terns for each of the 3 beat strength conditions were significantly 
dissimilar. Condition-wise activity patterns were derived from 
the first-level GLM in which all rhythms in a particular beat-
strength category were modeled with the same regressor (the 
GLM that also gave rise to the univariate analyses), rather than 
individual rhythms being modeled with a unique regressor. The 
crossnobis distance between the mean activity patterns for each 
condition was calculated, resulting in 3 distances (strong vs. weak, 
strong vs. non, weak vs. non) for each ROI. Using a one-sample 
t-test (one-sample t-tests are suitable for crossnobis distances, 
as cross-validation centers the distribution of distances on 0; 
Diedrichsen et al. 2016), we found significantly dissimilar mean 
activity patterns between strong-beat and nonbeat rhythms in the 
left [t(25) = 3.74,P= 0.001] and right SMA [t(25) = 3.20,P= 0.004], and 
in the left [t(25) = 2.90, P= 0.008], and right [t(25) = 2.32, P= 0.029] 
putamen (
Fig. 3, “Between” category on left bar graphs). This 
indicates that the SMA and putamen SB-NB differences found 
in the item-wise analysis were not driven by overlapping mean 
patterns with high item-wise variance. All other ROIs (caudate 
and pallidum) did not show significantly dissimilar mean activity 
patterns (Ps >0.06). In all ROIs, strong- vs. weak-beat and weak-
vs. nonbeat distances were not significant (Ps > 0.061), although 
the left caudate approached significance for strong- vs. weak-beat 
dissimilarity [t(25) = 1.99, P= 0.057]. Condition-wise dissimilarities 
for each ROI are shown in 
Supplemental Fig. 1. 
How is beat represented in the SMA and 
putamen? Are basic rhythmic features 
represented? 
The above analyses compared differences in beat strength based 
on categorically defined beat strength conditions ( Grahn and 
Brett 2007). Both the item-wise and condition-wise tests revealed 
distinct activity patterns for strong-beat rhythms compared to 
nonbeat rhythms in the SMA and putamen. However, no region 
showed significantly dissimilar patterns between strong-beat and 
weak-beat or weak-beat and nonbeat conditions. When illustrated 
using multidimensional scaling (
Fig. 4), it appears that activity 
patterns for weak-beat rhythms fall between strong-beat and 
nonbeat patterns—dissimilar from both but not enough to be 
significant when quantified by crossnobis distances. This could 
mean that beat is represented in these regions on a continuous 
scale, with item-level beat strength dictating activity patterns, 
rather than activity patterns representing the simple presence or 
absence of a beat. Separately , there may be variations in distance 
related to other features of the rhythms (e.g. tempo, number 
of onsets). Therefore, to test whether other features explained 
dissimilarities between rhythms, as well as to test other models of 
beat strength, we correlated 9 model RDMs with the neural RDMs 
extracted from the beat-sensitive regions—the left and right SMA 
and putamen (
Fig. 5). Correlations between model and neural 
RDMs that reached the noise ceiling (see Materials and Methods) 
were considered good candidates for a true neural RDM. Models 
that do not reach the noise ceiling are considered insufficient 
in explaining the representational structure, suggesting that a 
better model exists ( Yokoi et al. 2018). Representational model 
correlations were performed on a priori ROIs that showed beat 
sensitivity in previous analyses (i.e. the left and right putamen 
and SMA). 
In both left and right SMA, the counterevidence score model 
(in which C-score indexes each rhythm’s beat strength) was 
the winning model. It reached the noise ceiling, and it had the 
numerically largest correlation with neural RDMs. We compared
8 | Cerebral Cortex, 2024, Vol. 34, No. 10
Fig. 3. Item-wise MVPA results in 8 ROIs. Bar graphs depict averaged within-condition distances (light gray) and between-condition distances (dark gray) 
in each ROI (panels). Inset: Representational dissimilarity matrices in each ROI for the 12 rhythms. Within- and between-condition distances were first 
averaged across beat strength conditions and tested against 0. For the two left-most bars in each panel,∗ indicates where between or within-condition 
distances are greater than 0 at P <0.05. For the other pairs of bars in the panel, between-condition distances (e.g. strong 
− non) were compared to the 
constituent within-condition distances (e.g. strong+ non). Horizontal lines with∗ indicate significantly greater dissimilarity for between-condition vs. 
within-condition distances at P <0.05, consistent with beat strength encoding. 
the winning model to the other 8 models using paired-sample 
t-tests on the distribution of Pearson’s r values. In the left 
SMA, the C-Score model was significantly more correlated than 
the following models: Onsets [t(25) = 2.76, P= 0.011], Interval 
[t(25) = 2.64, P= 0.014], Tempo [t(25) = 3.63, P= 0.001], Weak Beat 
[t(25) = 2.95, P= 0.007], Nonbeat [t(25) = 2.01, P= 0.056], and Equal 
Beat [t(25) = 2.16, P= 0.041] models. The C-Score model was not 
significantly more correlated than the Strong Beat [t(25) = 0.63, 
P= 0.53] or Beat Hierarchy [t(25) = 0.39,P= 0.70] models. In the right 
SMA, the C-Score model was significantly more correlated than 
the Onsets [t(25) = 3.72, P= 0.001], Interval [t(25) = 3.34, P= 0.003], 
Tempo [t(25) = 3.38, P= 0.002], Strong Beat [t(25) = 2.77, P= 0.010], 
Weak Beat [t(25) = 3.27, P= 0.003], and Equal Beat [t(25) = 2.56, 
P= 0.017] models. The C-Score model was not significantly 
more correlated than the Nonbeat [t(25) = 1.67, P= 0.11] or Beat 
Hierarchy [t(25) = 0.91, P= 0.37] models in the right SMA. Thus, in 
left and right SMA, the C-Score model best explains the neural 
RDMs, suggesting that the SMA encodes beat strength on a 
rhythm-by-rhythm basis, beyond that explained by basic rhythm 
features or categorical beat strength. 
Model RDM correlations were also calculated in the left and 
right putamen, which appeared beat-sensitive in previous analy-
ses. Similar to the SMA, the C-Score model was the winning model 
in the left and right putamen (Fig. 5). However, because the noise
Hoddinott and Grahn | 9
Fig. 4. Multidimensional scaling of activity patterns in left and right SMA (top) and putamen (bottom). Each colored data point represents the activity 
pattern for a rhythm. Small black data points represent the mean coordinates of each condition. Circles = strong-beat, squares = weak-beat, and 
triangles = nonbeat rhythms. Colors scale with the counterevidence score for each rhythm. Distances between data points represent the magnitude of 
dissimilarity between activity patterns. For visualization purposes only , each subject’s negative distances were set to 0 before taking the group average 
RDM used for multidimensional scaling. 
ceiling crosses r= 0 (suggesting high intersubject variability), we 
did not statistically test the strength of this model compared to 
others. 
Exploring beat and rhythm encoding across the 
whole brain 
In addition to testing a priori ROIs, we identified beat-encoding 
regions across the whole brain. Using a whole-brain searchlight, 
the item-wise activity pattern analysis was conducted in small 
spherical ROIs covering the brain. Identically to the a priori ROIs, 
distances from each searchlight across the brain were averaged 
to create the 6 categories described above (3 within-condition; 3 
between-condition). The 6 comparisons of interest were entered 
into a second-level analysis using SPM12’s f lexible factorial with 
subject as a random effect. Whole-brain analyses followed the 
same order as the ROI analysis: We first tested for rhythm encod-
ing while controlling for beat strength ([SB-SB+WB-WB+NB-
NB > 0]) to identify regions that encode rhythm generally . Next, we 
tested for beat-encoding by identifying searchlights with greater 
between-condition dissimilarity than their constituent within-
condition dissimilarities. 
Whole-brain searchlight: rhythm encoding 
T o test for rhythm encoding, regardless of beat strength, we tested 
the averaged within-condition distances in each searchlight 
against zero [SB-SB+WB-WB+NB-NB > 0]. This test revealed 
rhythm encoding in left and right auditory cortices, right 
PMC, right cerebellum, and right occipital cortex (
Supplemen-
tal T able 1). 
Whole-brain searchlight: beat encoding 
T o identify beat-encoding regions across the brain, we tested 
whether between-condition dissimilarities were greater than 
within-condition dissimilarities using planned comparisons 
between each between-condition distance and the constituent 
within-condition distances, identically to the a priori ROI analysis. 
For the [SB-NB >SB-SB+NB-NB], only the SMA survived multiple 
comparison corrections at the cluster-size level (P
FWE = 0.006). 
This is consistent with findings in the anatomically defined 
SMA above. Finally , no differences were found between [WB-
NB > WB-WB+NB-NB], or [SB-WB >SB-SB+WB-WB], even at a 
liberal threshold (P
unc. <0.001). 
Whole-brain searchlight: feature-encoding 
T o explore feature-encoding across the brain, we first identified 
candidate regions that may encode any of the rhythmic features 
by testing for regions with between-condition dissimilarities 
> 0. This identified regions sensitive to rhythm differences 
that could be further tested for sensitivity to basic features 
or other potential models of beat strength. That is, because 
basic features of the rhythms (e.g. tempo) were balanced across 
conditions, basic feature encoding regions and beat-encoding 
regions would both elicit between-condition distances (see inset 
in 
Fig. 1B and C). For example, a tempo-encoding region would 
have significant distances between slow and fast rhythms. 
Because the strong-beat and nonbeat conditions both have 
slow and fast rhythms, the mean between-condition distance 
(SB-NB) for tempo-encoding regions and beat-encoding regions 
would have significant between-condition distances. Thus, to 
explore encoding (basic feature and/or beat-encoding) across the 
whole brain, all searchlights with significant between-condition 
distances were passed on to the feature-encoding analysis. 
As expected, many of the regions identified as having 
significant between-condition dissimilarity overlapped with 
rhythm-encoding regions identified in the within-condition 
test above, including bilateral auditory and PMCs, and right 
cerebellum ( Supplemental T able 2 ). However, we additionally 
found between-condition dissimilarities in the bilateral SMA, IFGs, 
right putamen, and right pallidum, which were not shown in the 
within-condition test, and notably , only the SMA was identified as
10 | Cerebral Cortex, 2024, Vol. 34, No. 10
Fig. 5. MVPA results in anatomically defined SMA and putamen regions of interest. Red and black matrices are mean representational dissimilarity 
matrices for the item-wise activity patterns, thresholded at 0. Bar graphs show mean correlation values between each model RDM (x axis), and neural 
item-wise RDMs, error bars represent the standard error of the mean. Dashed lines indicate the upper and lower bound of noise ceilings: Models of good 
fit will breach the lower bound of the noise ceiling (
Lage-Castellanos et al. 2019). 
beat-encoding as reported in the previous section. This suggests 
that while the SMA is beat sensitive, the remaining regions 
identified in this exploratory analysis appear to have a more 
nuanced representation—when beat strength is controlled, 
dissimilarities are relatively weak (within-condition is not 
greater than 0), but when there are differences in beat strength, 
the patterns begin to differ more reliably (between-condition 
dissimilarities are greater than 0) but are not significantly greater 
than within-condition distances. This indicates that multiple 
features may be represented in the activity patterns from these 
regions. 
T o determine which features are represented in activity pat-
terns across the whole brain, the significant between-condition 
searchlights were passed on to the feature-encoding modeling 
analysis as performed on the a priori ROIs. For each of the 12 clus-
ters in the [SB-NB+SB-WB+WB-NB > 0] test (
Fig. 6; Supplemen-
tal T able 2), the 9 representational models were correlated with 
each subject’s RDM, averaged across all searchlights contained in 
each cluster. Because clusters 1, 2, and 3 clearly crossed functional 
and anatomical boundaries, these clusters were further divided 
using the AAL parcellation. Regions were not reported if the noise 
ceiling crossed 0 (the data are too noisy to reliably fit a model), 
or if none of the mean model correlations breached the lower 
bound of the noise ceiling (no model sufficiently explains the 
data). Interpretation of feature encoding is restricted to regions 
with evidence for rhythm and/or auditory encoding from past 
literature. This process resulted in 20 regions with successful 
model fits. T o reduce the number of tests, in each region, we 
only statistically tested the model correlations between models 
breaching the lower bound of the noise ceiling. Results of the 
model correlations for the whole-brain clusters can be found in 
T able 2 and Fig. 6. 
In motor areas, significant searchlights were found in the 
left and right PMCs (precentral gyri and left postcentral gyrus) 
and in the SMA. In the left PMC (precentral gyrus), the Strong 
Beat, Nonbeat, Beat Hierarchy , and C-Score models breached the 
lower bound of the noise ceiling. Paired sample t-tests revealed 
no differences between these models (Ps> 0.053). In the left 
postcentral gyrus, only the C-Score model breached the noise 
ceiling. In the right PMC, (precentral gyrus), the Beat Hierarchy and 
C-Score models breached the noise ceiling. Comparisons between 
these models revealed no significant difference (P= 0.68). In the 
SMA, similar to the a priori SMA ROI, the Beat Hierarchy and 
C-score models breached the noise ceiling but were not 
significantly different from each other (P= 0.60). 
The right IFG was parcellated into the operculum, triangularis, 
and orbital cortex. In the right inferior frontal operculum, the 
Strong Beat, Nonbeat, Beat Hierarchy , and C-Score models all 
breached the noise ceiling. Comparisons between these models 
revealed no significant differences (Ps >0.14). In the right inferior
Hoddinott and Grahn | 11
Fig. 6. Results of the feature-encoding model tests on clusters with significant [between condition > 0] searchlights. Heat map indicates the strength of 
the t-test [SB-WB+SB-NB+WB-NB >0], indicating areas that encode rhythmic features. Insets: Group mean and standard error of Pearson correlations 
for each representational model in each brain region. White, light-gray , and dark-gray bars represent basic feature, condition-specific, and beat strength 
models, respectively . Left and right SMGs, PMC, IPL, and IFG were most correlated with models of beat strength. Cerebellum lobule VI (∗n= 25) was most 
correlated with the tempo, strong-beat, and beat hierarchy models. Cerebellum lobule VIII (∗n= 19) was most correlated with the nonbeat model. Right 
temporal pole and right medial temporal gyrus model fits not shown. 
Table 2. Whole brain searchlight: feature-encoding results. 
Region Cluster Models above noise ceiling lower bound Best fitting 
model 
Mean fit 
(M
r ) 
SD 
L precentral gyrus 9 Strong-beat, Nonbeat, Beat Hierarchy , C-Score Beat Hierarchy 0.10 0.15 
SMA 6 Beat Hierarchy , C-Score C-Score 0.11 0.19 
R parahippocampal gyrus 8 Onsets, Nonbeat Onsets 0.048 0.12 
R inferior frontal operculum 1 Strong-beat, Nonbeat, Beat Hierarchy , C-Score Beat Hierarchy 0.085 0.14 
R inferior frontal triangularis 1 Nonbeat, Beat Hierarchy , C-Score C-Score 0.073 0.19 
R inferior frontal orbital cortex 1 Strong-beat, Beat Hierarchy , C-Score C-Score 0.086 0.13 
R precentral gyrus 1 Beat Hierarchy , C-Score Beat Hierarchy 0.098 0.18 
R insular cortex 1 Tempo, Beat Hierarchy , C-Score C-Score 0.067 0.13 
R superior temporal pole 1 Onsets, Tempo, Strong-beat, Beat Hierarchy , C-Score Tempo 0.061 0.15 
R middle temporal gyrusa 1 Strong-beat, Beat Hierarchy , C-Score C-Score 0.096 0.13 
R supramarginal cortex 1 Nonbeat, Beat Hierarchy , C-Score C-Score 0.083 0.17 
L inferior frontal triangularis 2 Nonbeat, C-Score C-Score 0.078 0.22 
L inferior frontal operculum 2 C-Score C-Score 0.070 0.20 
L postcentral gyrus 2 C-Score C-Score 0.12 0.19 
L inferior parietal lobe 2 C-Score C-Score 0.083 0.20 
L supramarginal gyrus 2 C-Score C-Score 0.10 0.20 
R fusiform gyrus 3 Nonbeat Nonbeat 0.047 0.13 
R cerebellum lobule VIa 3 Tempo, Strong-beat, Beat Hierarchy Tempo 0.039 0.14 
R cerebellum lobule VIIIa 3 Nonbeat Nonbeat 0.085 0.16 
R primary visual cortex 7 Nonbeat Nonbeat 0.029 0.16 
Note: Regions with a noise ceiling crossing 0, or with no model breaching the lower bound of the noise ceiling are not reported. a Regions with missing data: 
Middle temporal gyrus (n= 24), cerebellum lobule VI (n= 25), and cerebellum lobule VIII (n= 19). 
12 | Cerebral Cortex, 2024, Vol. 34, No. 10
frontal triangularis, Nonbeat, Beat Hierarchy , and C-Score models 
all breached the noise ceiling. Comparisons between models 
revealed no significant differences between the mean correlations 
of these three models (Ps >0.58). In the right inferior frontal 
orbital cortex, Strong Beat, Beat Hierarchy , and C-Score models 
all breached the noise ceiling. Comparisons between models 
revealed that the mean correlation of the C-Score model was 
marginally greater than the Strong Beat model [t(25) = 1.81, 
P= 0.08]. No other significant differences were detected (Ps > 0.11). 
In the left hemisphere, the IFG only covered the triangularis and 
operculum. In the left inferior frontal triangularis, the Nonbeat 
and C-Score models breached the noise ceiling. Comparisons 
between models revealed no significant differences between 
models (P= 0.87). In the left inferior frontal operculum, only the 
C-Score model breached the noise ceiling. Overall, this suggests 
that representations of rhythm in the right and left IFGs relate 
to beat strength, possibly on the individual rhythm level. In the 
right insular cortex, Tempo, Beat Hierarchy , and C-Score models 
breached the noise ceiling. Comparisons between these models 
revealed no significant differences between models (Ps> 0.56). 
The temporal lobe had significant searchlights throughout 
auditory cortices, but many did not have a model of good fit. 
However, the right superior temporal pole and the right middle 
temporal gyrus were correlated with feature-encoding models. 
In the right superior temporal pole, the Onsets, Tempo, Strong 
Beat, Beat Hierarchy , and C-Score models breached the noise 
ceiling. Comparisons across these models revealed no signifi-
cant differences (Ps> 0.28). In the right middle temporal gyrus, 
the Strong Beat, Beat Hierarchy , and C-Score models breached 
the noise ceiling. Comparisons across these models revealed no 
significant differences between models (Ps >0.13). In the right 
parahippocampal gyrus, the Onsets model and Nonbeat model 
breached the noise ceiling but were not significantly different 
[t(25) = 0.50, P= 0.62]. 
In the left IPL, dorsal to the supramarginal gyrus (SMG), and in 
the left SMG, only the C-Score model breached the noise ceiling, 
suggesting that the IPL encodes beat strength at the individual 
rhythm level. In the right SMG, the Nonbeat, Beat Hierarchy , and 
C-Score models breached the noise ceiling. Comparisons across 
these models revealed no significant differences between models 
(Ps> 0.32). 
In the right cerebellum, lobules VI and VIII had significant 
searchlights. In the right lobule VI, the Tempo, Strong Beat, and 
Beat Hierarchy models breached the noise ceiling. Comparisons 
across these models revealed no significant differences between 
model fits (Ps>0.79). In right lobule VIII, only the Nonbeat model 
breached the noise ceiling. This suggests that representations 
of rhythm in lobule VIII relates to differences between nonbeat 
rhythms and all other rhythms. 
In the right primary visual cortex and right fusiform gyrus, only 
the Nonbeat model breached the noise ceiling. As the visual cortex 
is not known to be sensitive to rhythm, we have not interpreted 
this result. 
Discussion 
In this experiment, we examined brain areas that encoded rhyth-
mic properties by testing the dissimilarity between fine-grained 
activity patterns in previously identified beat-sensitive regions, as 
well as across the whole brain. We tested a priori anatomically 
defined ROIs for the left and right SMA, caudate, pallidum, and 
putamen. Of these, the bilateral SMA and bilateral putamen 
activated in distinct activity patterns for rhythms with different 
beat strengths. Moreover, SMA and putamen activity patterns 
also encoded the relative differences in beat strength between 
individual rhythms—the magnitude of pattern dissimilarity cor-
responded to the difference in beat strength for each rhythm. 
This suggests that the activity patterns did not simply ref lect 
the presence or absence of a beat; they also ref lected evidence 
degree of beat strength. We did not find evidence that other 
basal ganglia structures (i.e. the caudate and pallidum), encoded 
rhythmic features or were sensitive to beat strength, though 
right caudate pattern dissimilarities between beat strength con-
ditions were marginally significant. Thus, building on previous 
univariate findings (
Grahn and Brett 2007; Chen et al. 2008a, 
2008b), this study is the first to show that the SMA and putamen 
encode beat strength via multivoxel activity patterns and that 
these patterns are dictated by the strength of the beat for a 
given rhythm. Our data also clarify that the SMA and puta-
men do not encode each individual rhythm with equal discrim-
inability (as would be predicted if individual interval durations 
were driving activity patterns); rather, beat strength is the driv-
ing feature behind SMA and putamen activity patterns during 
rhythm listening, with more distinct patterns between rhythms 
of different beat strengths, compared to rhythms of similar beat 
strengths. 
In addition to a priori ROIs for the SMA and basal ganglia, 
rhythm- and beat-encoding regions across the brain were iden-
tified using a whole-brain searchlight. Identically to the ROI anal-
yses, the searchlights were analyzed to find regions that encoded 
beat strength: Activity pattern dissimilarities for rhythms of dif-
ferent conditions were compared to dissimilarities within con-
ditions. After controlling for within-condition dissimilarities, we 
found regions encoding differences in beat strength beyond that 
explained by individual rhythm encoding. The only beat-encoding 
region identified in whole-brain analysis was the bilateral SMA, as 
also shown in the a priori ROI analysis. 
We also explored individual rhythm encoding across the whole 
brain to reveal areas that were sensitive to differences between 
rhythms, regardless of beat strength. Pattern dissimilarities 
between rhythms of the same beat strength were detected in the 
bilateral PMC and IFGs, temporal pole, superior temporal gyrus, 
medial temporal lobe, medial temporal gyrus, and cerebellum. 
These regions align well with the univariate activation found both 
here (in the all Rhythms > rest contrast), and in previous work 
(
Schubotz et al. 2000; Chen et al. 2006, 2008b; Chen et al. 2008a; 
Grahn and Brett 2007; Bengtsson et al. 2009; Grahn and McAuley 
2009; Grahn and Rowe 2009; Grahn and Schuit 2012; Kung et al. 
2013; Lerens et al. 2013; Matthews et al. 2020; Hoddinott et al. 
2021). 
Finally , we explored rhythmic feature representations across 
the whole brain by fitting representational models to regions 
with significant between-condition dissimilarity , which may have 
ref lected beat, rhythm, or basic feature encoding. The between-
condition dissimilarity was used to identify candidate regions in 
which representations may relate to any rhythmic feature (beat 
strength, basic features). Beat strength was largely represented 
across the rhythm perception network—left and right PMCs, SMA, 
IFG, and SMG correlated best with beat strength models. Impor-
tantly , of these regions, only the SMA had activity patterns driven 
mainly by beat strength, as this was the only region to have 
greater dissimilarity between beat strength conditions, compared 
to within conditions, an analysis in which all beat-unrelated 
rhythmic features are well controlled. In essence, this means SMA 
activity patterns are most distinct between rhythms of different 
beat strengths, as depicted in 
Fig. 1A and C, while IFG and SMG
Hoddinott and Grahn | 13
activity patterns are partially driven by features or processes 
other than beat, such as in Fig. 1B and C. 
In the temporal lobe, many regions had no winning model. 
Early auditory cortical regions, such as Heschl’s gyrus, may 
encode each sound with a unique activity pattern and may 
not distinguish rhythms along the features for which we made 
distinct models, alternatively , Heschl’s gyrus may encode many 
or all basic features of the rhythms, which would result in highly 
dissimilar activity patterns between all rhythms, but dampen 
the explanatory impact of any one basic feature model. Activity 
patterns in the right superior temporal pole correlated with 
multiple models, including the Onsets, Tempo, Strong-beat, Beat 
Hierarchy , and C-Score models, though numerically , the tempo 
model fits best. This is perhaps indicative of auditory regions 
encoding many basic and nonbasic stimulus features. Similarly , 
activity in the right insula was correlated with the Tempo, Beat 
Hierarchy , and C-Score models, though C-Scores were the model 
of best fit and may represent multiple features of rhythm. 
Overall, the current study identified the SMA and putamen as 
beat-encoding regions, and activity in the right PMC, IFGs, SFGs, 
and left IPL may partially relate to beat strength. Each of the iden-
tified regions fit well with previous univariate work in rhythm and 
beat perception. The SMA and putamen are consistently reported 
to activate more during strong-beat rhythms, compared to non-
beat rhythms (
Grahn and Brett 2007; Chen et al. 2008b; Chen et al. 
2008a; Bengtsson et al. 2009; Grahn and Rowe 2009, 2013; Chapin 
et al. 2010; Matthews et al. 2020; Hoddinott et al. 2021). In addition, 
many previous studies report a larger rhythm perception network 
incorporating the remaining regions identified in our exploratory 
analysis: Left and right auditory cortices, SMA, basal ganglia, 
PMCs, and cerebellum all activate during rhythm listening but 
do not necessarily show sensitivity to the beat (
Grahn and Brett 
2007; Chen et al. 2008a, 2008b). These findings were replicated 
with our univariate analysis, except for the effect of beat strength 
in the SMA—no differences were found univariately between 
beat strength conditions; however, our data revealed multivari-
ate encoding of beat strength in the SMA. Notably , null effects 
are somewhat difficult to interpret through the lens of previous 
univariate work—as the current study used a more repetitive task 
design (only four rhythms per condition) and an MRI scanner with 
greater field strength (7T vs. 3T), which can impact signal-to-noise 
ratios (
T riantafyllou et al. 2005). Further, previous work did not 
find univariate SMA differences between beat strength conditions 
at the whole-brain level but only in ROI analyses (Grahn and Brett 
2007). 
SMA activity may ref lect the predictability of rhythms. As the 
participants hear the rhythms repeatedly across the experiment, 
the rhythms may be learned by the later imaging runs. During 
debriefing, nearly all subjects reported that the rhythms were 
repeated. Thus, the lack of a univariate effect of beat in the SMA 
may ref lect the equalization of predictability between rhythms of 
different beat strengths. While the strong-beat rhythms are some-
what predictable (partly because of their regularity and partly 
because we experience similar rhythms in real music) at the 
beginning of the experiment, the weak- and nonbeat rhythms are 
relatively unpredictable. But, as familiarity increases with expo-
sure, the prediction-related activity in the SMA may become more 
similar between conditions. Unfortunately , in the current experi-
ment, this change in predictability correlates with the amount of 
time in the scanner, making inferences about early vs. late con-
trasts confounded by physiological run-to-run noise, and neural 
habituation as described above. 
The inferior frontal cortex activity patterns had significant 
between-condition distances and correlated with beat strength 
models. This finding aligns well with previous univariate work 
that reported greater activation in overlapping coordinates in 
the IFG for strong-beat rhythms compared to weak- and non-
beat rhythms (
Grahn and Brett 2007), perhaps revealing a beat-
sensitive region that has not been thoroughly explored in rhythm 
perception. Outside of rhythm perception work, studies using 
naturalistic music have shown that the IFG is more active when 
people listen to music, compared to amusical control conditions 
(Levitin and Menon 2003), a contrast that may also reveal areas 
active for beat vs. no-beat stimuli. The IFG also activates when 
there is rhythmic tension in music, and when subjects are tapping 
a steady beat during a rhythm with high counterevidence for that 
beat (
Vuust et al. 2006, 2011). Rhythmic tension fits well with the 
current finding that activity patterns in the IFG correlate with beat 
strength. 
Representations of rhythm in the left and right IPLs were most 
correlated with the beat strength counterevidence score model, 
compared to other models. The left and right SMGs had significant 
between-condition distances, and neural representations were 
most correlated with models of beat strength. The SMG has been 
reported active for rhythm perception compared to silence, and 
for highly complex compared to simpler rhythms (
Kasdan et al. 
2022). One study reported that SMG activity is lateralized, with 
the left SMG responding to changes in pitch, and the right SMG 
responding to rhythm ( Schaal et al. 2017), though there is also 
evidence that musicians recruit the right SMG for pitch recogni-
tion tasks (Schaal et al. 2015). Here, we did not manipulate pitch, 
and we found that SMG encoding was related to beat strength 
in both hemispheres. The SMG may encode in sequential order. 
One transcranial magnetic stimulation (TMS) study reported that 
downregulation of the left SMG increased participants’ reporting 
of memorized verbal and visual sequences in the incorrect order, 
while the content of sequences (e.g. letters in a memorized string) 
remained stable (
Guidali et al. 2019). This suggests that the SMG 
is necessary to encode the order of sequential stimuli, such as 
a list of letters, but not necessarily the content—which letters 
were in the list. However, if the SMG only encodes sequential 
order, one would expect similar encoding of all rhythms in the 
current study—each rhythm had a unique order of intervals. 
Instead, we found that left and right SMGs correlated most with 
counterevidence score models of beat perception. 
Though beat sensitivity was found bilaterally in the SMG, in 
the left hemisphere only , the between-conditions cluster extended 
dorsally from the SMG, crossing the intraparietal sulcus and then 
medially into the IPL. Similar to the SMG, representations of 
rhythm in the ventral left IPL were most correlated with the beat-
strength counterevidence score model. Theoretical models of beat 
perception predict the IPL to play a role (
Patel and Iversen 2014). 
Specifically , the parietal lobe’s position in the dorsal auditory 
stream makes it a good candidate for crosstalk between auditory 
and motor regions. It has been proposed that the parietal lobe 
encodes rhythmic information, and may facilitate motor predic-
tions of upcoming acoustic events, as predicted by the Action 
Simulation for Auditory Prediction (ASAP) hypothesis (
Patel and 
Iversen 2014), as well as recent motor physiological explanations 
for the role of the motor system in beat perception ( Cannon and 
Patel 2021). Empirical evidence also suggests a role for the parietal 
cortex in beat perception—down-regulation of the left posterior 
parietal cortex with TMS disrupts beat-based timing but not 
absolute interval timing, suggesting that the left parietal cortex
14 | Cerebral Cortex, 2024, Vol. 34, No. 10
plays a role in beat-related behavior (Ross et al. 2018). Because the 
current task did not require explicitly timed motor responses, our 
findings expand on previous brain stimulation experiments by 
showing that parietal cortex activity correlates with beat strength 
in rhythms during perception without action. 
The regions we found that encoded rhythm, but were not sensi-
tive to the beat, also align with previous research. The cerebellum 
is commonly found to be active in rhythm and timing-related 
tasks (Lee et al. 2007; Coull and Nobre 2008)a n dm a yb ei n v o l v e d 
in absolute time perception, encoding the absolute duration of 
intervals ( Grube et al. 2010; Teki et al. 2011) as opposed to the 
relative duration between two intervals (e.g. encoding intervals in 
a rhythm relative to the underlying beat interval). Indeed, TMS of 
the cerebellum affects the estimation of single-interval durations 
in tasks requiring absolute interval encoding (
Lee et al. 2007). Our 
finding that the cerebellum lobule VI represents rhythms accord-
ing to their overall tempo aligns well with an absolute timing 
process: Rhythms of different tempi must also have intervals of 
different absolute duration. It then makes sense that cerebellar 
activity patterns are highly dissimilar from each other when 
rhythms are made up of intervals that have different absolute 
durations. In cerebellum lobule VIII, we found that activity pat-
terns differentiated nonbeat rhythms from all other rhythms (the 
Nonbeat condition-specific model). This may also be explained 
by absolute timing in the cerebellum—the nonbeat condition was 
the only condition in which rhythms included noninteger ratios. 
These noninteger ratios are impossible to encode relative to other 
durations, such as a beat or by subdividing longer intervals in 
the same rhythm. Thus, to encode nonbeat rhythms, absolute 
timing must be used. Cerebellum lobule VIII correlated most with 
the Nonbeat condition model, which may indicate activation for 
rhythms that require absolute timing strategies. 
Many searchlights throughout the auditory cortex represented 
individual rhythms. Bilateral STG, Heschl’s gyrus, temporal poles, 
and other auditory regions revealed significantly dissimilar activ-
ity patterns across rhythms. However, we were not able to create 
a sufficient model to explain which features of the rhythms were 
represented in the auditory cortex. Auditory areas may encode 
many features of the rhythms and sounds, so many that we can-
not create a single model to capture this representation. Notably , 
the noise ceiling in the auditory cortex is quite high and does 
not show large variability between subjects—the upper and lower 
bounds are relatively narrow . This suggests that even though our 
models do not sufficiently explain the representations of rhythm 
in the auditory cortex, activity patterns are quite reliable across 
subjects. More work is needed to reveal how rhythmic acoustic 
stimuli are represented in the auditory cortex. Future studies may 
consider using larger, feature-rich stimulus sets, as opposed to 
the highly controlled rhythms used in the current experiment. For 
example, some work has been performed using naturalistic music 
and speech (
Norman-Haignere et al. 2015), but more can be done 
to specifically target beat strength using naturalistic music. 
The neural representation of rhythm begins in the auditory sys-
tem and transforms into beat-strength representation in motor 
and association regions. In general, the current findings align with 
the theoretical role of the dorsal auditory stream in beat percep-
tion (
Patel and Iversen 2014). Specifically , auditory information is 
proposed to pass dorsally from the auditory cortex, through the 
inferior parietal cortex, and into the PMC (i.e. the SMA). Motor-
based predictions in the SMA are sent back through the dorsal 
stream to predict incoming auditory information. Simultaneously , 
auditory information is sent from the auditory cortices to the 
inferior frontal cortex via the ventral stream. This theory would 
predict that sensory regions encode rhythms generally , without 
extra sensitivity to beat strength, while premotor regions should 
have the strongest representation of beat strength. Further, the IPL 
(dorsal stream) and IFG (ventral stream), which may be involved 
in integrating incoming auditory information and top–down pre-
dictions from the PMC, may ref lect both bottom–up sensory rep-
resentation of the rhythms and top–down beat strength repre-
sentation. Indeed, our current data show that in the auditory 
cortex, activity patterns for each rhythm are highly dissimilar 
but not explained by low- or high-level features of the rhythms. 
These sensory regions are likely to respond to each individual 
sound in the rhythm. As the sensory information is passed to 
association regions, the beat becomes the prominently encoded 
feature. The putamen, SMA, IPL and SMG, and the IFG appear to 
represent rhythms based on their individual beat strength. This 
explanation fits with the nuanced representation of rhythm in 
these regions—the IPL and IFG did not have significant within-
condition dissimilarities, indicating that they do not represent 
each individual rhythm, as auditory sensory regions do, but they 
also did not have greater between-condition dissimilarities com-
pared to within, suggesting that they do not represent beat above 
and beyond individual rhythms, as do the SMA and putamen. 
Thus, these association regions may ref lect contributions of beat-
encoding and rhythm-encoding activity that is passed down from 
the SMA and auditory cortex simultaneously . However, because 
the temporal resolution of fMRI is very slow , it is not possible to 
show which of these regions first represents the beat. However, 
compared to the other regions, the SMA, and possibly the left 
putamen, appear to be the most sensitive to the beat—as these 
are the only regions to have greater dissimilarities between beat 
strength conditions compared to within beat-strength conditions. 
This was especially the case for the SMA, which is the only region 
to survive multiple comparison corrections in the [SB-NB > SB-
SB+NB–NB] contrast at the whole-brain level and is corroborated 
by past univariate work. 
The putamen’s role in beat perception also aligns with recent 
theoretical work that expands on the ASAP hypothesis ( Cannon 
and Patel 2021). The striatum may respond to regular auditory 
stimulation by signaling a chunk of sequential predictions to 
be carried out by the SMA ( Cannon and Patel 2021). The SMA 
compares the prediction to the incoming auditory stimulation 
and reports some form of prediction error back to the striatum 
to update the following prediction. This would align well with 
our current findings in both regions: Rhythms with high coun-
terevidence for the beat are relatively unpredictable. Thus, as 
counterevidence increases, unpredictability , and prediction error, 
also increases, resulting in highly distinct activation patterns. 
When there is a strong, highly predictable beat, there is little 
prediction error, and signaling from the SMA is very similar across 
rhythms. 
In conclusion, this experiment is the first to show that the 
SMA and putamen activate in highly distinguishable multi-voxel 
patterns for rhythms of different beat strengths. Importantly , 
the beat was represented on a continuous scale—the greater 
the difference in beat strength between two rhythms, the more 
dissimilar the activity patterns were for each of the rhythms. 
Through exploratory analyses, we also show that beat strength is 
represented, at least partially , in the left inferior parietal lobe and 
the right PMC. Lastly , cerebellum activity patterns were altered 
most by tempo, suggesting that the cerebellum may be tuned to 
the overall rate of rhythms.
Hoddinott and Grahn | 15
Acknowledgments 
We thank Dr Eva Berlot and Dr Jörn Diedrichsen for their advice 
regarding multivariate pattern analysis. 
Author contributions 
Joshua Hoddinott (Data curation, Formal analysis, Investigation, 
Methodology , Visualization, Writing—original draft, Writing— 
review & editing) and Jessica Grahn (Conceptualization, Funding 
acquisition, Project administration, Resources, Supervision, 
Writing—review & editing). 
Supplementary material 
Supplementary material is available at Cerebral Cortex online. 
Funding 
This work was supported by Western University’s Canada First 
Research Excellence Fund BrainsCAN initiative; a Natural Sci-
ences and Engineering Research Council of Canada (NSERC) Dis-
covery Grant to J.A.G. (grant number 2016-05834); a McDonnell 
Foundation Scholar Award to J.A.G. (DOI:
10.37717/220020403); and 
a Natural Sciences and Engineering Research Council of Canada 
Steacie Fellowship to J.A.G. 
Conf lict of interest statement: None declared. 
References 
Bendor D , Wang X . The neuronal representation of pitch in pri-
mate auditory cortex. Nature. 2005:436:1161–1165. https://doi. 
org/10.1038/nature03867. 
Bengtsson SL , Ullén F , Henrik Ehrsson H , Hashimoto T , Kito T , 
Naito E , Forssberg H, Sadato N . Listening to rhythms activates 
motor and premotor cortices. Cortex. 2009:45:62–71. https://doi. 
org/10.1016/j.cortex.2008.07.002. 
Bouwer FL, Burgoyne JA, Odijk D, Honing H, Grahn JA. What makes a 
rhythm complex? The inf luence of musical training and accent 
type on beat perception. PLoS One. 2018:13:1–26. https://doi. 
org/10.1371/journal.pone.0190322. 
Cannon JJ, Patel AD. How beat perception Co-opts motor neurophys-
iology . T rends Cogn Sci. 2021:25:137–150. https://doi.org/10.1016/j. 
tics.2020.11.002. 
Chapin HL , Zanto T , Jantzen KJ , Kelso SJA , Steinberg F , Large 
EW. Neural responses to complex auditory rhythms: the role 
of attending. Front Psychol. 2010:1:224. https://doi.org/10.3389/ 
fpsyg.2010.00224. 
Chen JL , Zatorre RJ , Penhune VB . Interactions between auditory 
and dorsal premotor cortex during synchronization to musical 
rhythms.NeuroImage. 2006:32:1771–1781. https://doi.org/10.1016/ 
j.neuroimage.2006.04.207. 
Chen JL , Penhune VB , Zatorre RJ . Listening to musical rhythms 
recruits motor regions of the brain. Cereb Cortex. 2008a:18: 
2844–2854. https://doi.org/10.1093/cercor/bhn042. 
Chen JL, Penhune VB, Zatorre RJ. Moving on time: brain network for 
auditory-motor synchronization is modulated by rhythm com-
plexity and musical training. J Cogn Neurosci. 2008b:20:226–239. 
https://doi.org/10.1162/jocn.2008.20018. 
Coull J, Nobre A. Dissociating explicit timing from temporal expecta-
tion with fMRI. Curr Opin Neurobiol. 2008:18:137–144. https://doi. 
org/10.1016/j.conb.2008.07.011. 
Coull JT, Charras P, Donadieu M, Droit-Volet S, Vidal F. SMA selec-
tively codes the active accumulation of temporal, not spa-
tial. Magnitude J Cogn Neurosci. 2015:27:2281–2298. https://doi. 
org/10.1162/jocn_a_00854. 
Diedrichsen J , Provost S , Zareamoghaddam H . On the distribu-
tion of cross-validated Mahalanobis distances.arXiv. 2016:1:1–24. 
https://doi.org/10.48550/arXiv .1607.01371. 
Diedrichsen J, Yokoi A, Arbuckle SA. Pattern component modeling: a 
flexible approach for understanding the representational struc-
ture of brain activity patterns. NeuroImage. 2018:180:119–133. 
https://doi.org/10.1016/j.neuroimage.2017.08.051. 
Grahn JA . The role of the basal ganglia in beat perception: neu-
roimaging and neuropsychological investigations. Ann N Y Acad 
Sci. 2009:1169:35–45. https://doi.org/10.1111/j.1749-6632.2009. 
04553.x. 
Grahn JA. See what I hear? Beat perception in auditory and visual 
rhythms. Exp Brain Res. 2012:220:51–61. https://doi.org/10.1007/ 
s00221-012-3114-8 . 
Grahn JA, Brett M. Rhythm in motor areas of the brain.J Cogn Neurosci. 
2007:19:893–906. https://doi.org/10.1162/jocn.2007.19.5.893. 
Grahn JA, Brett M. Impairment of beat-based rhythm discrimina-
tion in Parkinson’s disease. Cortex. 2009:45:54–61. https://doi. 
org/10.1016/j.cortex.2008.01.005. 
Grahn JA , McAuley JD . Neural bases of individual differences 
in beat perception. NeuroImage. 2009:47:1894–1903. https://doi. 
org/10.1016/j.neuroimage.2009.04.039. 
Grahn JA , Rowe JB . Feeling the beat: premotor and striatal inter-
actions in musicians and non-musicians during beat pro-
cessing. J Neurosci. 2009:29:7540–7548. https://doi.org/10.1523/ 
JNEUROSCI.2018-08.2009. 
Grahn JA , Rowe JB . Finding and feeling the musical beat: 
striatal dissociations between detection and prediction of 
regularity . Cereb Cortex. 2013:23:913–921. https://doi.org/10.1093/ 
cercor/bhs083. 
Grahn JA , Schuit D . Individual differences in rhythmic abilities: 
behavioural and neuroimaging investigations. Psychomusicol-
ogy music mind. Brain. 2012:22:105–121. https://doi.org/10.1037/ 
a0031188. 
Grube M , Cooper FE , Chinnery PF , Griffiths TD . Dissociation of 
duration-based and beat-based auditory timing in cerebellar 
degeneration. Proc Natl Acad Sci. 2010:107:11597–11601. https:// 
doi.org/10.1073/pnas.0910473107. 
Guidali G , Pisoni A , Bolognini N , Papagno C . Keeping order in 
the brain: the supramarginal gyrus and serial order in short-
term memory . Cortex. 2019:119:89–99. https://doi.org/10.1016/j. 
cortex.2019.04.009. 
Hoddinott JD , Schuit D , Grahn JA . Comparisons between short-
term memory systems for verbal and rhythmic stimuli. 
Neuropsychologia. 2021:163:108080, 1–9. https://doi.org/10.1016/j. 
neuropsychologia.2021.108080. 
Humphries C , Liebenthal E , Binder JR . T onotopic organization of 
human auditory cortex. NeuroImage. 2010:50:1202–1211. https:// 
doi.org/10.1016/j.neuroimage.2010.01.046. 
Kasdan A V, Burgess AN, Pizzagalli F, Scartozzi A, Chern A, Kotz SA, 
Wilson SM, Gordon RL. Identifying a brain network for musical 
rhythm: a functional neuroimaging meta-analysis and system-
atic review. Neurosci Biobehav Rev. 2022:136:104588, 1–21. https:// 
doi.org/10.1016/j.neubiorev .2022.104588. 
Kornysheva K , Diedrichsen J . Human premotor areas parse 
sequences into their spatial and temporal features. elife. 
2014:3:e03043, 1–23. 
Kriegeskorte N , Mur M , Bandettini PA. Representational similarity 
analysis – connecting the branches of systems neuroscience.
16 | Cerebral Cortex, 2024, Vol. 34, No. 10
Front Syst Neurosci. 2008:2:1–28. https://doi.org/10.3389/neuro.06. 
004.2008. 
Kung S-J , Chen JL , Zatorre RJ , Penhune VB . Interacting cortical 
and basal ganglia networks underlying finding and tapping to 
the musical beat. J Cogn Neurosci. 2013:25:401–420. https://doi. 
org/10.1162/jocn_a_00325. 
Lage-Castellanos A, Valente G, Formisano E, Demartino F.M e t h o d s 
for computing the maximum performance of computational 
models of FMRI responses.PLoS Comput Biol. 2019:15:1–25.https:// 
doi.org/10.1371/journal.pcbi.1006397. 
Lee K-H, Egleston PN, Brown WH, Gregory AN, Barker AT, Woodruff 
PWR. The role of the cerebellum in subsecond time percep-
tion: evidence from repetitive transcranial magnetic stimula-
tion. J Cogn Neurosci. 2007:19:147–157. https://doi.org/10.1162/ 
jocn.2007.19.1.147. 
Lerens E , De Volder A , Araneda R , Renier L . Perception of 
rhythm through auditory , vibro-tactile and visual stimulations: 
an fMRI study. Multisensory Research. 2013:26:117:1. https://doi. 
org/10.1163/22134808-000S0085. 
Levitin DJ , Menon V . Musical structure is processed in “language” 
areas of the brain: a possible role for Brodmann area 47 in 
temporal coherence. NeuroImage. 2003:20:2142–2152. https://doi. 
org/10.1016/j.neuroimage.2003.08.016. 
Matthews TE , Witek MAG , Lund T , Vuust P , Penhune VB .T h e 
sensation of groove engages motor and reward networks. 
NeuroImage. 2020:214:116768, 1–12. https://doi.org/10.1016/j. 
neuroimage.2020.116768. 
Mur M , Bandettini PA , Kriegeskorte N . Revealing representational 
content with pattern-information fMRI - an introductory guide. 
Soc Cogn Affect Neurosci. 2009:4:101–109. https://doi.org/10.1093/ 
scan/nsn044. 
Nili H, Wingfield C, Walther A, Su L, Marslen-Wilson W, Kriegesko-
rte N . A toolbox for representational similarity analysis. PLoS 
Comput Biol. 2014:10:e1003553. https://doi.org/10.1371/journal. 
pcbi.1003553. 
Norman-Haignere S , Kanwisher NG , McDermott JH . Distinct cor-
tical pathways for music and speech revealed by hypothesis-
free voxel decomposition. Neuron. 2015:88:1281–1296. https://doi. 
org/10.1016/j.neuron.2015.11.035. 
Notter MP, Hanke M, Murray MM, Geiser E. Encoding of auditory tem-
poral gestalt in the human brain. Cereb Cortex. 2019:29:475–484. 
https://doi.org/10.1093/cercor/bhx328. 
Pastor MA, Macaluso E, Day BL, Frackowiak RSJ. The neural basis of 
temporal auditory discrimination.NeuroImage. 2006:30:2:512-520. 
https://doi.org/10.1016/j.neuroimage.2005.09.053. 
Pastor MA, Day BL, Macaluso E, Friston KJ, Frackowiak RSJ. The 
Functional Neuroanatomy of Temporal Discrimination.J Neurosci. 
2004:24:10:2585-2591. https://doi.org/10.1523/jneurosci.4210-03. 
2004. 
Pastor MA, Macaluso E, Day BL, Frackowiak RSJ. Putaminal activity 
is related to perceptual certainty. NeuroImage. 2008:41:1:123-129. 
https://doi.org/10.1016/j.neuroimage.2008.01.034. 
Patel AD, Iversen JR. The evolutionary neuroscience of musical beat 
perception: the action simulation for auditory prediction (ASAP) 
hypothesis. Front Syst Neurosci. 2014:8:57. https://doi.org/10.3389/ 
fnsys.2014.00057. 
Povel D-J, Essens PJ. Perception of temporal patterns. Music Percept. 
1985:1985:411–440. 
Protopapa F , Hayashi MJ , Kulashekhar S , Van Der Zwaag W , Bat-
tistella G , Murray MM , Kanai R , Bueti D . Chronotopic maps in 
human supplementary motor area. PLoS Biol. 2019:17:e3000026. 
https://doi.org/10.1371/journal.pbio.3000026. 
Rolls ET, Huang CC, Lin CP, Feng J, Joliot M. Automated anatomical 
labelling atlas 3. NeuroImage. 2020:206:116189, 1–5. https://doi. 
org/10.1016/j.neuroimage.2019.116189. 
Ross JM, Iversen JR, Balasubramaniam R. The role of posterior pari-
etal cortex in beat-based timing perception: a continuous theta 
burst stimulation study. J Cogn Neurosci. 2018:30:634–643. https:// 
doi.org/10.1162/jocn_a_01237. 
Schaal NK, Krause V, Lange K, Banissy MJ, Williamson VJ, Pollok B. 
Pitch memory in nonmusicians and musicians: revealing func-
tional differences using transcranial direct current stimulation. 
Cereb Cortex. 2015:25:2774–2782. https://doi.org/10.1093/cercor/ 
bhu075. 
Schaal NK , Pollok B, Banissy MJ . Hemispheric differences between 
left and right supramarginal gyrus for pitch and rhythm memory. 
Sci Rep. 2017:7:42456. https://doi.org/10.1038/srep42456. 
Schubotz RI , von Cramon DY. Interval and ordinal properties 
of sequences are associated with distinct premotor areas. 
Cereb Cortex. 2001:11:210–222. https://doi.org/10.1093/cercor/11. 
3.210. 
Schubotz RI , Friederici AD , Yves von Cramon D . Time percep-
tion and motor timing: a common cortical and subcortical 
basis revealed by fMRI. NeuroImage. 2000:11:1–12. https://doi. 
org/10.1006/nimg.1999.0514. 
Teki S , Grube M , Kumar S , Griffiths TD . Distinct neural 
substrates of duration-based and beat-based auditory timing. 
J Neurosci. 2011:31:3805–3812.https://doi.org/10.1523/JNEUROSCI. 
5561-10.2011. 
T riantafyllou C, Hoge R, Krueger G, Wiggins CJ, Potthast A, Wiggins 
GC, Wald L . Comparison of physiological noise at 1.5 T , 3 T 
and 7 T and optimization of fMRI acquisition parameters. Neu-
roImage. 2005:26:243–250. https://doi.org/10.1016/j.neuroimage. 
2005.01.007. 
Vuust P, Roepstorff A , Wallentin M, Mouridsen K , Ostergaard L .I t 
don’t mean a thing... Keeping the rhythm during polyrhythmic 
tension, activates language areas (BA47). NeuroImage. 2006:31: 
832–841. https://doi.org/10.1016/j.neuroimage.2005.12.037. 
Vuust P , Wallentin M , Mouridsen K , Østergaard L , Roepstorff A . 
T apping polyrhythms in music activates language areas. Neu-
rosci Lett. 2011:494:211–216. https://doi.org/10.1016/j.neulet.2011. 
03.015. 
Walther A , Nili H , Ejaz N , Alink A , Kriegeskorte N , Diedrichsen 
J. Reliability of dissimilarity measures for multi-voxel pattern 
analysis. NeuroImage. 2016:137:188–200. https://doi.org/10.1016/j. 
neuroimage.2015.12.012. 
Wiestler T, Diedrichsen J. Skill learning strengthens cortical repre-
sentations of motor sequences. elife. 2013:2:e00801, 1–20. 
Yokoi A , Arbuckle SA , Diedrichsen J . The role of human 
primary motor cortex in the production of skilled finger 
sequences.J Neurosci. 2018:38:1430–1442. https://doi.org/10.1523/ 
JNEUROSCI.2798-17.2017.
