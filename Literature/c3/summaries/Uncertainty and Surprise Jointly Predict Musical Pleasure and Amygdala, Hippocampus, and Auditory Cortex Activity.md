# Uncertainty and Surprise Jointly Predict Musical Pleasure and Amygdala, Hippocampus, and Auditory Cortex Activity

**Authors:** Vincent K. M. Cheung
**Year:** D:20
**Subject:** Current Biology, 29 (2019) 4084-4096. doi:10.1016/j.cub.2019.09.067

---

Report
Uncertainty and Surprise Jointly Predict Musical
Pleasure and Amygdala, Hippocampus, and Auditory
Cortex Activity
Highlights
d Musical pleasure depends on prospective and retrospective
states of expectation
d A machine-learning model quantiﬁed the uncertainty and
surprise of pop song chords
d Chords with low uncertainty and high surprise, and vice
versa, evoked high pleasure
d Joint effects of uncertainty and surprise found in the
amygdala and auditory cortex
Authors
Vincent K. M. Cheung, Peter M. C. Harrison, Lars Meyer, Marcus T. Pearce, John-Dylan Haynes, Stefan Koelsch
Correspondence
stefan.koelsch@uib.no
In Brief
Cheung et al. use a machine-learning
model to mathematically quantify the
predictive uncertainty and surprise of
80,000 chords in 745 commercially
successful pop songs. The authors
further show that chord uncertainty and
surprise jointly modulate musical
pleasure, as well as activity in the
amygdala, hippocampus, and auditory
cortex using fMRI. Cheung et al., 2019, Current Biology 29, 4084–4092
December 2, 2019 ª 2019 Elsevier Ltd.
https://doi.org/10.1016/j.cub.2019.09.067

Current Biology
Report
Uncertainty and Surprise Jointly
Predict Musical Pleasure and Amygdala, Hippocampus, and Auditory Cortex Activity
Vincent K. M. Cheung,1 Peter M. C. Harrison,2 Lars Meyer,3 Marcus T. Pearce,2,4 John-Dylan Haynes,5
and Stefan Koelsch1,6,7,*
1Department of Neuropsychology, Max Planck Institute for Human Cognitive and Brain Sciences, Stephanstraße, 04103 Leipzig, Germany
2School of Electronic Engineering & Computer Science, Queen Mary University of London, Mile End Road, London E1 4NS, UK
3Research Group Language Cycles, Max Planck Institute for Human Cognitive and Brain Sciences, Stephanstraße, 04103 Leipzig, Germany
4Department of Clinical Medicine, Aarhus University, Palle Juul-Jensens Boulevard, 8200 Aarhus N, Denmark
5Bernstein Center for Computational Neuroscience, Charite – Universit€atsmedizin Berlin, Corporate Member of Freie Universit€at Berlin, Humboldt-Universit€at zu Berlin, Berlin Institute of Health (BIH), Chariteplatz 1, 10117 Berlin, Germany
6Department of Biological and Medical Psychology, University of Bergen, Jonas Lies vei, 5009 Bergen, Norway
7Lead Contact
*Correspondence: stefan.koelsch@uib.no
https://doi.org/10.1016/j.cub.2019.09.067
SUMMARY
Listening to music often evokes intense emotions
[1, 2]. Recent research suggests that musical plea-
sure comes from positive reward prediction errors,
which arise when what is heard proves to be better
than expected [3]. Central to this view is the engage-
ment of the nucleus accumbens—a brain region that
processes
reward
expectations—to
pleasurable
music and surprising musical events [4–8]. However,
expectancy violations along multiple musical dimen-
sions (e.g., harmony and melody) have failed to
implicate the nucleus accumbens [9–11], and it is un-
known how music reward value is assigned [12]. Whether changes in musical expectancy elicit plea-
sure has thus remained elusive [11]. Here, we
demonstrate that pleasure varies nonlinearly as a
function of the listener’s uncertainty when antici-
pating a musical event, and the surprise it evokes
when it deviates from expectations. Taking Western
tonal harmony as a model of musical syntax, we
used a machine-learning model [13] to mathemati-
cally
quantify
the
uncertainty
and
surprise
of
80,000 chords in US Billboard pop songs. Behavior-
ally, we found that chords elicited high pleasure rat-
ings when they deviated substantially from what
the listener had expected (low uncertainty, high
surprise) or, conversely, when they conformed to ex-
pectations in an uninformative context (high uncer-
tainty, low surprise). Neurally, we found using fMRI
that activity in the amygdala, hippocampus, and
auditory cortex reﬂected this interaction, while the
nucleus
accumbens
only
reﬂected
uncertainty. These ﬁndings challenge current neurocognitive
models of music-evoked pleasure and highlight
the synergistic interplay between prospective and
retrospective states of expectation in the musical
experience. RESULTS
Humans use structured sound sequences known as music to ex-
press and evoke emotions [1]. Manipulating the listener’s expec-
tations is a key mechanism through which music elicits pleasure
[1, 2, 14–16]. A fundamental concept and characteristic feature
of Western music is tonal harmony, which describes the syntac-
tic regularities of how simultaneous pitches are combined into
chords, and how chords are related to other chords in a progres-
sion [17]. In this study, we directly addressed whether musical
pleasure depended on the expectancy of individual chords in a
progression (Experiment 1), and how that was reﬂected in human
brain activity (Experiment 2). Quantifying Uncertainty and Surprise with Information
Theory
As music unfolds in time, the listener continuously forms expec-
tations on upcoming temporal and acoustic features [3, 13, 18]. This implies the presence of two temporally dissociable states
through which the expectancy of a chord can evoke pleasure:
the uncertainty when anticipating what the next chord could be
before it occurs, and the surprise elicited when the actual chord
deviates from expectations [16, 19]. In contrast, the existing liter-
ature has almost exclusively focused on surprising musical
events [19, 20] and found inconclusive effects on musical plea-
sure [6, 11]. To mathematically quantify uncertainty and surprise, we em-
ployed an unsupervised statistical-learning model [13] that
learned the statistical regularities of over 80,000 chord progres-
sions from a corpus of 745 pop songs listed in the US Billboard
‘‘Hot 100’’ chart between 1958 and 1991 [21]. Our model uses
these learned statistical regularities to simulate a listener’s pre-
diction for novel chord sequences using Shannon’s entropy
and information content (Figure 1; STAR Methods). Entropy re-
ﬂects how uncertain a listener is when anticipating an upcoming

Current Biology 29, 4084–4092, December 2, 2019 ª 2019 Elsevier Ltd.

chord given only the portion of the song heard so far. Information
content, or surprisal, reﬂects how surprised the listener is once
actually hearing the chord. These two established information-
theoretic measures have been extensively applied to natural
language processing [22], but only recently to harmony [23] in
music. Our data-driven approach is superior to traditional de-
signs for three reasons. First, we quantify uncertainty and sur-
prise as continuous variables as opposed to comparing a small
number of discrete categories (e.g., violation/no violation) prede-
ﬁned by the experimenter [6, 9, 23–27]. Second, our chord stimuli
are taken directly from the corpus to ensure conformity to stylis-
tic conventions, as opposed to artiﬁcial chord progressions used
in prior studies (e.g., [9, 25, 26]). Third, instead of examining plea-
sure elicited by a musical piece overall (e.g., [4, 5, 7]), we inves-
tigate how expectancy differences on a chord-to-chord level
affect musical pleasure. Experiment 1: Joint Effects of Uncertainty and Surprise
on Musical Pleasure
In Experiment 1, healthy adults (n = 39) listened to 1,039 chords
in 30 chord progressions (Table S1) selected from the 745 pop
songs and rated the pleasantness of each chord using a me-
chanical slider. We only kept the chord progressions from the
original songs (and removed the melody and rhythm) to ensure
that our isochronous chord stimuli were not confounded by
effects of other musical dimensions and familiarity (songs were
conﬁrmed to be unidentiﬁable by our subjects). We used a linear
mixed model to analyze the extent to which uncertainty and sur-
prise, and their interaction, predicted pleasantness of chords
taken from the commercially successful pop songs. To account
for temporal autocorrelations in the slider ratings, we used a
ﬁrst-order autoregressive covariance structure to model the rela-
tionship between successive chords in each stimulus. To disam-
biguate probabilistic processing of expectations from sensory
processing, we controlled for low-level acoustic features (i.e.,
sensory dissonance, spectral centroid, and spectral complexity)
in the model (see Table S3 for correlations with chord uncertainty
and surprise). We found that the pleasure rating of a chord was signiﬁcantly
predicted by main effects of uncertainty and surprise, as well as
their interaction (Figure 2; Table 1; see Table S2 for correlation of
random effects). In other words, pleasantness depended on joint
effects of the precision of the listener’s predictions, and the
probability of the chord given the tonal harmonic context. Since
the generation of an expectation precedes its deviation, we inter-
pret this interaction as the modulatory effect of uncertainty on
the effect of surprise on musical pleasure. When the uncertainty
of the harmonic context was low (e.g., toward the end of a
musical section), chords with higher surprise (i.e., those that
were less probable) were rated as more pleasant than those
Figure 1. Quantifying Uncertainty and Surprise of a Chord
(A) An unsupervised statistical-learning model was trained on a corpus of 745 US Billboard ‘‘Hot 100’’ pop songs to derive the uncertainty (red) and surprise (blue)
of chords (here, ‘‘Knowing Me, Knowing You’’ by ABBA; refer to Audio S1). Uncertainty is the lack of a clear expectation when anticipating an event before it is
heard, while surprise occurs when what is actually heard deviates from expectations. Uncertainty of chord ei is quantiﬁed by its entropy, or expected negative log-
probability, taken across the set of all chords S in the corpus and conditional on the previous context of chords fe1;.; ei1g in the progression. Surprise of chord
ei is quantiﬁed by its information content, and is the negative log-probability of the actual chord conditional on the context. Gray bars indicate points of high
uncertainty but low surprise, and low uncertainty but high surprise. Subjects (n = 79) were asked to either rate the pleasantness of each chord (2.4 s) from 30 pop
song chord progressions behaviorally or listen attentively and focus on how they ﬁtted together in the context while undergoing fMRI scanning.
(B and C) Scatterplot and marginal densities of the uncertainty and surprise for all chords in the McGill Billboard corpus [21] (circles, n = 80,943) and in our chord
stimuli (triangles, n = 1,039; Table S1). Current Biology 29, 4084–4092, December 2, 2019

with lower surprise. Conversely, when uncertainty was high (e.g.,
in chord progressions atypical of the listener’s musical experi-
ence), subjects rated chords that were less surprising as more
pleasant (Figure 2B). In fact, the regression surface (Figure 2C) resembled a sad-
dle, where the multiplicative effect of uncertainty and surprise
along the two diagonals predicted pleasantness in a parabolic
(U/inverted-U) manner. This is reminiscent of Berlyne’s [31]
inﬂuential model in empirical aesthetics, which postulated an
inverted-U relationship between pleasure and variables such
as exposure and complexity. Critically, however, our ﬁndings
paint a more complicated and multifaceted picture of musical
pleasure. Our ﬁndings imply that isolated effects of individual
variables alone cannot fully explain the musical experience,
as it is likely to be a nonlinear function of multiple interacting
factors. Furthermore, consistent with prior work [32–36], the low-level
acoustic features also showed signiﬁcant effects on pleasure
(but were controlled for in the model). The magnitude of stan-
dardized beta estimates in our model (Table 1) indicated that
when the uncertainty of the chord was at its mean, the effect
of surprise was 30% larger than sensory dissonance, and this
marginal effect became twice as large when chord uncertainty
was increased to 1.5 SD above the mean. Experiment 2: Neural Basis of Uncertainty and Surprise
in Music-Evoked Pleasure
To directly assess the underlying brain regions whose activity
correlated with uncertainty and surprise, another group of sub-
jects (n = 40) listened to the same isochronous chord stimuli
and was instructed to pay attention to how the chords ﬁtted
together in the progression while undergoing fMRI scanning in
Experiment 2. As before, we conﬁrmed that our stimuli were un-
familiar to the subjects. Despite the sluggishness of the blood-
oxygen-level-dependent (BOLD) response, the long duration of
each chord (2.4 s) meant that metabolic changes could still be
measured on a chord-to-chord level. We also used multiband
echo-planar imaging (EPI) [37, 38] to allow for a sub-second tem-
poral resolution while maintaining good spatial coverage. We
focused our analysis on brain regions previously shown to be
implicated in music-evoked emotions across multiple studies
[1]: the bilateral amygdala and adjacent anterior hippocampus,
bilateral auditory cortex, right nucleus accumbens, left caudate
nucleus, and the pre-supplementary motor area. Given that
musical pleasure depends on joint effects of uncertainty and sur-
prise, we hypothesized that the underlying brain regions would
also show the same interaction. Figure 2. Uncertainty and Surprise Jointly Shape the Pleasure Rat-
ing of a Chord
(A) Standardized pleasure ratings to a chord progression taken from ‘‘Knowing
Me, Knowing You’’ by ABBA (Audio S1). Diamonds indicate mean pleasant-
ness ratings for each chord. Filled circles indicate ﬁtted values from a linear
mixed model with chord uncertainty, surprise, and their interaction as
predictors. Error bars indicate 95% conﬁdence intervals (95% CI). Low-level
acoustic parameters were also included as covariates to control for sensory
confounds.
(B) Contour plot demonstrating how pleasantness ratings jointly depend on
uncertainty and surprise. When the tonal harmonic context does not allow for a
prediction with high precision (i.e., when uncertainty is high), the pleasantness
of a surprising chord is low. However, when the uncertainty is low, surprising
chords are highly pleasurable.
(C) Data from (B) replotted in 3D. Although reminiscent of the characteristic
inverted-U response from empirical aesthetics, the regression surface is in fact
a saddle for which pleasantness varies nonlinearly across different levels of
uncertainty and surprise. Current Biology 29, 4084–4092, December 2, 2019

Consistent with our behavioral ﬁndings, we found in Experi-
ment 2 (Figure 3; see Table S4 for parameter estimates) that
the interaction between uncertainty and surprise signiﬁcantly
modulated the BOLD response in the bilateral amygdala and hip-
pocampus (left: b = 0.116, corrected 95% CI = [0.201,
0.0445], sign test: s = 11, corrected p = 0.0450; right: b =
0.140, corrected 95% CI = [0.238, 0.0410], one-sample
t test: t(39) = 4.02, corrected p = 0.00181; see also Figure S1). This is in line with prior studies implicating the amygdala in sur-
prises in tonal harmony and changes in musical tension [26,
27], as well as the hippocampus in encoding the uncertainty of
sequences [39, 40], and forming memory associations during
music listening [5]. Furthermore, this interaction modulated activity in the bilateral
auditory cortex (left: b = 0.182, corrected 95% CI = [0.288,
0.0766], t(39) = 4.90, corrected p = 0.000120; right: b =
0.128, corrected 95% CI = [0.220, 0.0355], t(39) = 3.93,
corrected p = 0.00234), with stronger effects in the left compared
to the right (Figure S2). In line with our observed interaction, pitch
deviants in melodies [41] and timing deviants in rhythm [42]
evoke reduced auditory mismatch responses for stimuli with
increased uncertainty (although pleasantness was not investi-
gated in those studies; see [16] for a discussion). The established
role of the auditory cortex in processing sound, as well as the
amygdala and hippocampus in processing emotions, suggests
that the pleasure evoked by expectations in music rests on a
close link between perceptual analysis and affective evaluation
[1, 3, 43]. Remarkably, neither a signiﬁcant interaction between uncer-
tainty and surprise nor a main effect of surprise was detected
in the nucleus accumbens or caudate (all corrected p > 0.993). We instead detected a positive main effect of uncertainty in
the right nucleus accumbens (b = 0.242, corrected 95% CI =
[0.0720, 0.412], t(39) = 4.04, corrected p = 0.00170) and left
caudate (b = 0.281, corrected 95% CI = [0.0661, 0.496],
t(39) = 3.71, corrected p = 0.00447). This means striatal activity
was increased when the tonal harmonic context was less infor-
mative in revealing what the ensuing chord could be and
decreased when more informative. In a post hoc analysis, we
found comparable results in the contralateral nucleus accum-
bens and caudate with no evidence of laterality (Figure S3). Our data therefore suggest that striatal activity encodes the un-
certainty of an expectation, irrespective of the magnitude of sur-
prise. Finally, the pre-supplementary motor area likewise only
showed a signiﬁcant positive modulation to uncertainty (b =
0.358, corrected 95% CI = [0.145, 0.570], t(39) = 4.78, corrected
p = 0.000176). DISCUSSION
Our results contribute direct evidence in support of an expec-
tancy mechanism in evoking musical pleasure [2, 14–16, 18,
44]. We showed that surprise, a retrospective response, alone
cannot fully explain the link between expectations in music and
pleasure. Our data demonstrate that uncertainty, a prospec-
tive state of expectation, is another crucial dimension needed
to describe this relationship. Pleasantness ratings to isochro-
nous chord progressions taken from commercially successful
Western pop music indicated high pleasure in two situations:
when a chord with high surprise had been predicted with low
uncertainty, or conversely, when a chord with low surprise
had been predicted with high uncertainty. This interaction ef-
fect was reﬂected by metabolic changes in the amygdala,
anterior hippocampus, and auditory cortex, but not the nu-
cleus accumbens. Uncertainty and surprise are in fact key
components of an inﬂuential predictive-coding model of
neuronal message-passing across the cortical hierarchy [16,
20, 45]. In this model, music perception is construed as an
active process where the brain continuously updates its
generative model of the environment to minimize variational
free-energy [16, 20]. Music may therefore elicit pleasure by
encouraging the listener to continuously generate and resolve
expectations as the piece unfolds in time [16, 20]. The impor-
tance of the temporal dimension in evoking pleasure sets mu-
sic apart from the static visual objects that are traditionally
studied in empirical aesthetics [46, 47]. Table 1. Parameter Estimates of the Linear Mixed Model in Experiment 1
Fixed-Effect Predictor
Standardized b

## 95% CI

Deviance
p
Intercept
0.0219
[0.0740, 0.118]
0.200
0.655
Uncertainty
0.143
[0.186, 0.0989]
40.2
2.33 3 1010***
Surprise
0.327
[0.418, 0.236]
29.2
6.57 3 108***
Uncertainty 3 surprise
0.124
[0.183, 0.0644]
13.4
0.000246***
Sensory dissonance
0.251
[0.345, 0.158]
19.3
1.41 3 105***
Spectral centroid
0.0719
[0.0244, 0.119]
8.77
0.00306**
Spectral complexity
0.224
[0.147, 0.300]
23.0
1.65 3 106***
Overall pleasantness of sequence
0.171
[0.032, 0.309]
5.28
0.0215*
Overall arousal of sequence
0.0321
[0.160, 0.0956]
0.242
0.623
Subjects (n = 39) continuously rated the pleasantness of 1,039 chords in 30 chord sequences using a mechanical slider. The pleasantness of a chord
depended on not only the amount of surprise evoked, but also the uncertainty in anticipating the chord before it was actually heard. Low-level acoustic
effects were also introduced as covariates (see Table S3 for correlations with chord uncertainty and surprise) to disambiguate probabilistic processing
from low-level sensory processing. Deviance here denotes twice the difference in log-likelihood between the full model and a restricted model with the
effect omitted. Signiﬁcance of individual ﬁxed effects was determined using the likelihood-ratio test after a full-null model comparison [28, 29]. Marginal
and conditional R2 values for the model were estimated according to [30]. See Table S2 for correlation of random effects. Marginal R2 = 0.476; con-
ditional R2 = 0.654; *p < 0.05, **p < 0.01, ***p < 0.001. Current Biology 29, 4084–4092, December 2, 2019

Figure 3. Neural Basis of Uncertainty and Surprise in Music-Evoked Pleasure
(A) Model-based fMRI revealed that BOLD activity in the bilateral amygdala and neighboring anterior hippocampus (Amyg/Hipp), as well as the bilateral auditory
cortex (AC), is signiﬁcantly modulated by the interaction of chord uncertainty and surprise.
(B) The right nucleus accumbens (NAcc), left caudate (CN), and pre-supplementary area (pre-SMA) instead only showed signiﬁcant positive modulations to chord
uncertainty. See also Figures S1–S3 and Table S4. Boxplots show parameter estimates for the effect of uncertainty, surprise, and their interaction in each region
of interest (n = 40; ﬁlled circles, data points; solid line, median; diamond, mean; notches, 95% CI of the median; hinges, IQR; whiskers, 1.5*IQR; statistical in-
ferences were made using one-sample t tests (two-tailed) or sign tests (for non-normal data) and Bonferroni-corrected for multiple comparisons (n.s., p R 0.05,
*p < 0.05, **p < 0.01, ***p < 0.001). Current Biology 29, 4084–4092, December 2, 2019

Unlike prior studies [4, 7, 8, 48], which appealed to the estab-
lished role of the nucleus accumbens in reward expectation [49,
50] as evidence supporting an expectancy mechanism of
musical pleasure, we directly addressed how predictability in
our stimuli modulated pleasantness. These studies also left un-
explained which musical dimensions constituted an expected
musical reward, and how reward value is assigned to musical
events [12]. In contrast, our results indicate that musical pleasure
comes from manipulating both the uncertainty of the listener’s
expectations before hearing an event and the surprise that fol-
lows when such expectations are not met. Here, these events
are chords represented on the symbolic level and objectively
quantiﬁed using information theory. These chord expectations
are likely generated, at least partly, in the inferior frontal gyrus,
a region shown to process expectation deviations in musical
structure [9, 18, 51], and passed top-down to the auditory cortex
[16, 20, 44]. Since the uncertainty and surprise of a chord were
derived independently from its acoustic characteristics and
solely on its conditional probability of occurrence, the same
chord will have a different level of uncertainty and surprise de-
pending on the combination of chords prior in the progression. Combined with the control of low-level acoustic regressors, we
can rule out that our results were driven by sensory-acoustic
features. Activity in the nucleus accumbens and caudate did not show
signiﬁcant modulation to the effect of chord surprise and its inter-
action with uncertainty. Given the central role of the nucleus ac-
cumbens in reward prediction, this might be seen as at odds with
our behavioral ﬁnding that pleasantness is predicted by the joint
effect of uncertainty and surprise. Instead, we found that uncer-
tainty positively modulated striatal activity. Our results suggest
that the striatum performs a facilitatory, although important,
role in generating musical pleasure —that of modulating incen-
tive salience, or the motivation or ‘‘wanting’’ of subsequent infor-
mation that resolves uncertainty [44, 49]. In addition to reward
expectation, the nucleus accumbens is argued to play a signiﬁ-
cant role in integrating cognitive and affective information to
direct attention and modify actions toward motivationally rele-
vant stimuli through dopaminergic pathways [50]. In line with
this and consistent with our ﬁndings, dopamine is assumed to
encode the precision (the inverse of uncertainty) of prediction er-
rors in the free-energy principle [16, 20]. Indeed, causal studies
on musical pleasure [48, 52] do not claim that striatal dopami-
nergic neurons induce pleasurable emotions per se, but highlight
their necessity in regulating affective responses to music. Taken
together, we suggest that a role of the nucleus accumbens in
musical pleasure is to modulate attention deployment, depend-
ing on uncertainty, in the amygdala, hippocampus, and auditory
cortex. In line with this, the nucleus accumbens has shown
increased functional connectivity with the amygdala, hippocam-
pus, auditory cortex, and the inferior frontal cortex for music that
was more pleasant [4, 6]. Our study has certain limitations. First, our auditory stimuli
consisted of computer-generated isochronous chord progres-
sions taken from original pop songs. Although this allowed
us to isolate effects of harmonic expectancy by controlling
for confounds such as rhythm, melody, familiarity, dynamics,
and instrumentation, the expectancy of these other dimen-
sions and the dimensions themselves are also likely to
inﬂuence pleasure [2, 8, 15, 53, 54]. Second, the parametric
values of uncertainty and surprise derived from our computa-
tional model are constrained by the corpus from which the
statistical regularities are computed. In other words, a highly
surprising chord predicted with low uncertainty here is only
relative to other chords present in the McGill Billboard corpus
of commercially successful pop songs [21]. Third, listeners’
experiences shape their internal model of the statistical regu-
larities of chords in a progression [13]. This means that factors
such as culture, genre, and style affect how surprising a chord
is, and with how much precision it can be expected [13]. Whether our results extend to other musical styles (see, e.g.,
[55] for a discussion on atonal music), and the extent to which
enculturation, expertise, and individual differences shape our
preferences and emotional responses to music thus remain
open questions. In summary, we show with the help of an unsupervised statis-
tical-learning model that musical pleasure depends on the dy-
namic interplay between prospective and retrospective states
of expectation. We demonstrate that this joint effect is reﬂected
by metabolic changes in the amygdala, hippocampus, and audi-
tory cortex, and is likely mediated through dopaminergic incen-
tive salience signals in the nucleus accumbens—which instead
showed a positive modulation to uncertainty. Our fundamental
ability to predict [16, 20] is therefore an important mechanism
through which abstract sound sequences acquire affective
meaning and transform into a universal cultural phenomenon
that we call ‘‘music’’ [15]. STAR+METHODS
Detailed methods are provided in the online version of this paper
and include the following:
d KEY RESOURCES TABLE
d LEAD CONTACT AND MATERIALS AVAILABILITY
d EXPERIMENTAL MODEL AND SUBJECT DETAILS
d METHOD DETAILS
B Information Dynamics Of Music model
B Stimuli
B Procedure for Experiment 1
B Procedure for Experiment 2
B fMRI data acquisition for Experiment 2
d QUANTIFICATION AND STATISTICAL ANALYSIS
B Behavioral data analysis for Experiment 1
B fMRI data preprocessing for Experiment 2
B fMRI data analysis for Experiment 2
d DATA AND CODE AVAILABILITY

## SUPPLEMENTAL INFORMATION

Supplemental Information can be found online at https://doi.org/10.1016/j.
cub.2019.09.067. A video abstract is available at https://doi.org/10.1016/j.cub.2019.09.
067#mmc4. ACKNOWLEDGMENTS
We are grateful to Angela D. Friederici for securing funding and resources to
conduct this study. We thank Alex Billig, David Huron, Thomas C. Gunter, Current Biology 29, 4084–4092, December 2, 2019

Daniela Sammler, Philipp Kuhnke, and Joshua Grant for valuable reviews and
comments on an earlier version of this manuscript; Nina Ro¨ ßler for helping with
documentation and data collection; Chiao-Yi Wu for feedback on the fMRI
experimental design; Roger Mundry for feedback on the behavioral data anal-
ysis; Kerstin Flake for editing the ﬁgures; and Tina Sierpinski for helping with
stimuli production. We also thank the University of Minnesota Center for Mag-
netic Resonance Research for providing the multiband EPI sequence. This
work was funded by the Max Planck Society. V. K. M. C. was supported by an
honorary doctoral scholarship from the Croucher Foundation. P. M. C. H. was
supported by a doctoral studentship from the EPSRC and AHRC Centre for
Doctoral Training in Media and Arts Technology (EP/L01632X/1).

## AUTHOR CONTRIBUTIONS

V. K. M. C. and S. K. conceived the study. V. K. M. C., S. K., P. M. C. H., M. T. P., L. M., and J.-D. H. conceptualized the study. V. K. M. C., S. K., L. M., P. M. C. H., J.-D. H., and M. T. P. developed the experimental paradigm. P. M. C. H. and
M. T. P. developed the computational model. V. K. M. C. and P. M. C. H. devel-
oped the stimuli. L. M., S. K., M. T. P., and J.-D. H. supervised the research. V. K. M. C. collected and analyzed the data, prepared the ﬁgures, and wrote
the original draft of the manuscript. V. K. M. C., S. K., P. M. C. H., L. M., M. T. P.,
and J.-D. H. reviewed and edited the manuscript.

## DECLARATION OF INTERESTS

The authors declare no competing interests. Received: July 6, 2019
Revised: September 11, 2019
Accepted: September 25, 2019
Published: November 7, 2019
REFERENCES

### 1. Koelsch, S. (2014). Brain correlates of music-evoked emotions. Nat. Rev. Neurosci. 15, 170–180.

### 2. Juslin, P. N., and V€astfj€all, D. (2008). Emotional responses to music: the

need to consider underlying mechanisms. Behav. Brain Sci. 31, 559–
575, discussion 575–621.

### 3. Salimpoor, V. N., Zald, D. H., Zatorre, R. J., Dagher, A., and McIntosh, A. R.

(2015). Predictions and the brain: how musical sounds become rewarding. Trends Cogn. Sci. 19, 86–91.

### 4. Salimpoor, V. N., van den Bosch, I., Kovacevic, N., McIntosh, A. R., Dagher, A., and Zatorre, R. J. (2013). Interactions between the nucleus accumbens
and auditory cortices predict music reward value. Science 340, 216–219.

### 5. Mueller, K., Fritz, T., Mildner, T., Richter, M., Schulze, K., Lepsien, J., Schroeter, M. L., and Mo¨ ller, H. E. (2015). Investigating the dynamics of
the brain response to music: a central role of the ventral striatum/nucleus
accumbens. Neuroimage 116, 68–79.

### 6. Shany, O., Singer, N., Gold, B. P., Jacoby, N., Tarrasch, R., Hendler, T.,

and Granot, R. (2019). Surprise-related activation in the nucleus accum-
bens interacts with music-induced pleasantness. Soc. Cogn. Affect. Neurosci. 14, 459–470.

### 7. Gold, B. P., Mas-Herrero, E., Zeighami, Y., Benovoy, M., Dagher, A., and

Zatorre, R. J. (2019). Musical reward prediction errors engage the nucleus
accumbens and motivate learning. Proc. Natl. Acad. Sci. USA 116, 3310–
3315.

### 8. Salimpoor, V. N., Benovoy, M., Larcher, K., Dagher, A., and Zatorre, R. J.

(2011). Anatomically distinct dopamine release during anticipation and
experience of peak emotion to music. Nat. Neurosci. 14, 257–262.

### 9. Koelsch, S., Fritz, T., Schulze, K., Alsop, D., and Schlaug, G. (2005). Adults

and children processing music: an fMRI study. Neuroimage 25, 1068–
1076.

### 10. Royal, I., Vuvan, D. T., Zendel, B. R., Robitaille, N., Scho¨ nwiesner, M., and

Peretz, I. (2016). Activation in the right inferior parietal lobule reﬂects the
representation of musical structure beyond simple pitch discrimination. PLoS ONE 11, e0155291.

### 11. Goupil, L., and Aucouturier, J.-J. (2019). Musical pleasure and musical

emotions. Proc. Natl. Acad. Sci. USA 116, 3364–3366.

### 12. Hansen, N. C., Dietz, M. J., and Vuust, P. (2017). Commentary: predictions

and the brain: how musical sounds become rewarding. Front. Hum. Neurosci. 11, 168.

### 13. Pearce, M. T. (2018). Statistical learning and probabilistic prediction in mu-

sic cognition: mechanisms of stylistic enculturation. Ann. N Y Acad. Sci. Published online May 11, 2018. https://doi.org/10.1111/nyas.13654.

### 14. Meyer, L. B. (1956). Emotion and Meaning in Music (The University of

Chicago Press).

### 15. Huron, D. (2006). Sweet Anticipation (The MIT Press).

### 16. Koelsch, S., Vuust, P., and Friston, K. (2019). Predictive processes and the

peculiar case of music. Trends Cogn. Sci. 23, 63–77.

### 17. Moss, F. C., Neuwirth, M., Harasim, D., and Rohrmeier, M. (2019). Statistical
characteristics
of
tonal
harmony:
a
corpus
study
of
Beethoven’s string quartets. PLoS ONE 14, e0217242.

### 18. Rohrmeier, M. A., and Koelsch, S. (2012). Predictive information process-

ing in music cognition. A critical review. Int. J. Psychophysiol. 83, 164–175.

### 19. Hansen, N. C., and Pearce, M. T. (2014). Predictive uncertainty in auditory

sequence processing. Front. Psychol. 5, 1052.

### 20. Friston, K. J., and Friston, D. A. (2013). A free energy formulation of music

generation and perception: Helmholtz revisited. In Sound - Perception –
Performance, R. Bader, ed. (Springer), pp. 43–70.

### 21. Burgoyne, J. A., Wild, J., and Fujinaga, I. (2011). An expert ground-truth set

for audio chord recognition and music analysis. 12th Int. Soc. Music Inf. Retr. Conf. 633–638.

### 22. Hale, J. (2016). Information-theoretical complexity metrics. Lang. Linguist. Compass 10, 397–412.

### 23. Sears, D. R. W., Pearce, M. T., Spitzer, J., Caplin, W. E., and McAdams, S.

(2019). Expectations for tonal cadences: sensory and cognitive priming ef-
fects. Q. J. Exp. Psychol. 72, 1422–1438.

### 24. Steinbeis, N., Koelsch, S., and Sloboda, J. A. (2006). The role of harmonic

expectancy violations in musical emotions: evidence from subjective,
physiological, and neural responses. J. Cogn. Neurosci. 18, 1380–1393.

### 25. Loui, P., and Wessel, D. (2007). Harmonic expectation and affect in

Western music: effects of attention and training. Percept. Psychophys.
69, 1084–1092.

### 26. Koelsch, S., Fritz, T., and Schlaug, G. (2008). Amygdala activity can be

modulated by unexpected chord functions during music listening. Neuroreport 19, 1815–1819.

### 27. Lehne, M., Rohrmeier, M., and Koelsch, S. (2014). Tension-related activity

in the orbitofrontal cortex and amygdala: an fMRI study with music. Soc. Cogn. Affect. Neurosci. 9, 1515–1523.

### 28. Forstmeier, W., and Schielzeth, H. (2011). Cryptic multiple hypotheses

testing in linear models: overestimated effect sizes and the winner’s curse. Behav. Ecol. Sociobiol. (Print) 65, 47–55.

### 29. Mundry, R. (2014). Statistical issues and assumptions of phylogenetic

generalized
least
squares. In
Modern
Phylogenetic
Comparative
Methods and Their Application in Evolutionary Biology, L. Z. Garamszegi,
ed. (Springer Berlin Heidelberg), pp. 131–153.

### 30. Nakagawa, S., Johnson, P. C. D., and Schielzeth, H. (2017). The coefﬁcient

of determination R2 and intra-class correlation coefﬁcient from general-
ized linear mixed-effects models revisited and expanded. J. R. Soc. Interface 14, 20170213.

### 31. Berlyne, D. E. (1971). Aesthetics and Psychobiology (Appleton-Century-

Crofts).

### 32. Popescu, T., Neuser, M. P., Neuwirth, M., Bravo, F., Mende, W., Boneh, O., Moss, F. C., and Rohrmeier, M. (2019). The pleasantness of sensory disso-
nance is mediated by musical style and expertise. Sci. Rep. 9, 1070. Current Biology 29, 4084–4092, December 2, 2019

### 33. Eerola, T., Friberg, A., and Bresin, R. (2013). Emotional expression in mu-

sic: contribution, linearity, and additivity of primary musical cues. Front. Psychol. 4, 487.

### 34. Shahin, A., Roberts, L. E., Pantev, C., Trainor, L. J., and Ross, B. (2005). Modulation of P2 auditory-evoked responses by the spectral complexity
of musical sounds. Neuroreport 16, 1781–1785.

### 35. McAdams, S., Douglas, C., and Vempala, N. N. (2017). Perception and

modeling of affective qualities of musical instrument sounds across pitch
registers. Front. Psychol. 8, 153.

### 36. Laurier, C., Meyers, O., Serra`, J., Blech, M., Herrera, P., and Serra, X.

(2010). Indexing music by mood: design and integration of an automatic
content-based annotator. Multimedia Tools Appl. 48, 161–184.

### 37. Feinberg, D. A., Moeller, S., Smith, S. M., Auerbach, E., Ramanna, S., Gunther, M., Glasser, M. F., Miller, K. L., Ugurbil, K., and Yacoub, E.
(2010). Multiplexed echo planar imaging for sub-second whole brain
FMRI and fast diffusion imaging. PLoS ONE 5, e15710.

### 38. Moeller, S., Yacoub, E., Olman, C. A., Auerbach, E., Strupp, J., Harel, N.,

and Ugurbil, K. (2010). Multiband multislice GE-EPI at 7 tesla, with 16-
fold acceleration using partial parallel imaging with application to high
spatial and temporal whole-brain fMRI. Magn. Reson. Med. 63, 1144–
1153.

### 39. Strange, B. A., Duggins, A., Penny, W., Dolan, R. J., and Friston, K. J. (2005). Information theory, novelty and hippocampal responses: unpredicted or
unpredictable? Neural Netw. 18, 225–230.

### 40. Harrison, L. M., Duggins, A., and Friston, K. J. (2006). Encoding uncertainty

in the hippocampus. Neural Netw. 19, 535–546.

### 41. Quiroga-Martinez, D. R., Hansen, N. C., Højlund, A., Pearce, M. T., Brattico, E., and Vuust, P. (2019). Reduced prediction error responses
in high-as compared to low-uncertainty musical contexts. Cortex 120,
181–200.

### 42. Lumaca, M., Trusbak Haumann, N., Brattico, E., Grube, M., and Vuust, P.

(2019). Weighting of neural prediction error by rhythmic complexity: A pre-
dictive coding account using mismatch negativity. Eur. J. Neurosci. 49,
1597–1609.

### 43. Zald, D. H., and Zatorre, R. J. (2011). Music. Neurobiology of Sensation and

Reward (CRC Press), pp. 405–428.

### 44. Gebauer, L., Kringelbach, M. L., and Vuust, P. (2012). Ever-changing cy-

cles of musical pleasure: the role of dopamine and anticipation. Psychomusicology 22, 152–167.

### 45. Friston, K. (2010). The free-energy principle: a uniﬁed brain theory? Nat. Rev. Neurosci. 11, 127–138.

### 46. Brielmann, A. A., and Pelli, D. G. (2018). Aesthetics. Curr. Biol. 28, R859–

R863.

### 47. Huron, D., and Margulis, E. H. (2010). Musical expectancy and thrills. Handbook of Music and Emotion: Theory, Research, Applications
(Oxford University Press), pp. 575–604.

### 48. Mas-Herrero, E., Dagher, A., and Zatorre, R. J. (2018). Modulating musical

reward sensitivity up and down with transcranial magnetic stimulation. Nat. Hum. Behav. 2, 27–32.

### 49. Berridge, K. C., and Kringelbach, M. L. (2015). Pleasure systems in the

brain. Neuron 86, 646–664.

### 50. Floresco, S. B. (2015). The nucleus accumbens: an interface between

cognition, emotion, and action. Annu. Rev. Psychol. 66, 25–52.

### 51. Cheung, V. K. M., Meyer, L., Friederici, A. D., and Koelsch, S. (2018). The

right inferior frontal gyrus processes nested non-local dependencies in
music. Sci. Rep. 8, 3822.

### 52. Ferreri, L., Mas-Herrero, E., Zatorre, R. J., Ripolles, P., Gomez-Andres, A., Alicart, H., Olive, G., Marco-Pallares, J., Antonijoan, R. M., Valle, M., et al.
(2019). Dopamine modulates the reward experiences elicited by music. Proc. Natl. Acad. Sci. USA 116, 3793–3798.

### 53. Matthews, T. E., Witek, M. A. G., Heggli, O. A., Penhune, V. B., and Vuust, P.

(2019). The sensation of groove is affected by the interaction of rhythmic
and harmonic complexity. PLoS ONE 14, e0204539.

### 54. Stark, E. A., Vuust, P., and Kringelbach, M. L. (2018). Music, Dance, and

Other Art Forms: New Insights into the Links between Hedonia
(Pleasure) and Eudaimonia (Well-Being), First Edition (Elsevier B. V.).

### 55. Mencke, I., Omigie, D., Wald-Fuhrmann, M., and Brattico, E. (2019). Atonal

music: can uncertainty lead to pleasure? Front. Neurosci. 12, 979.

### 56. Pearce, M. T. (2005). The construction and evaluation of statistical models

of melodic structure in music perception and composition. PhD thesis
(City University London).

### 57. Brooks, M. E., Kristensen, K., van Benthem, K. J., Magnusson, A., Berg, C. W., Nielsen, A., Skaug, H. J., Maechler, M., and Bolker, B. M. (2017).
{glmmTMB} balances speed and ﬂexibility among packages for zero-in-
ﬂated generalized linear mixed modeling. R J. 9, 378–400.

### 58. Brett, M., Anton, J.-L., Valabregue, R., and Poline, J.-B. (2002). Region of

interest analysis using the MarsBar toolbox for SPM 99. Neuroimage 16, S497.

### 59. Mu¨ llensiefen, D., Gingras, B., Musil, J., and Stewart, L. (2014). The musi-

cality of non-musicians: an index for assessing musical sophistication in
the general population. PLoS ONE 9, e89642.

### 60. Mas-Herrero, E., Marco-Pallares, J., Lorenzo-Seva, U., Zatorre, R. J., and

Rodriguez-Fornells, A. (2013). Individual differences in music reward ex-
periences. Music Percept. An Interdiscip. J. 31, 118–138.

### 61. Shannon, C. E. (1948). A mathematical theory of communication. Bell Syst. Tech. J. 27, 379–423.

### 62. Cleary, J., and Witten, I. (1984). Data compression using adaptive coding

and partial string matching. IEEE Trans. Commun. 32, 396–402.

### 63. Moffat, A. (1990). Implementing the PPM data compression scheme. IEEE

Trans. Commun. 38, 1917–1921.

### 64. Bunton, S. (1997). Semantically motivated improvements for PPM vari-

ants. Comput. J. 40, 76–93.

### 65. Pearce, M., Conklin, D., and Wiggins, G. (2005). Methods for combining

statistical models of music. Lect. Notes Comput. Sci. 3310, 295–312.

### 66. Pearce, M. T., and Wiggins, G. A. (2012). Auditory expectation: the informa-

tion dynamics of music perception and cognition. Top. Cogn. Sci. 4,
625–652.

### 67. Pearce, M., and Wiggins, G. A. (2004). Improved methods for statistical

modelling of monophonic music. J. New Music Res. 33, 367–385.

### 68. Pearce, M. T., Ruiz, M. H., Kapasi, S., Wiggins, G. A., and Bhattacharya, J.

(2010). Unsupervised statistical learning underpins computational, behav-
ioural, and neural manifestations of musical expectation. Neuroimage 50,
302–313.

### 69. Omigie, D., Pearce, M. T., Williamson, V. J., and Stewart, L. (2013). Electrophysiological correlates of melodic processing in congenital amu-
sia. Neuropsychologia 51, 1749–1762.

### 70. Omigie, D., Pearce, M. T., and Stewart, L. (2012). Tracking of pitch proba-

bilities in congenital amusia. Neuropsychologia 50, 1483–1493.

### 71. Egermann, H., Pearce, M. T., Wiggins, G. A., and McAdams, S. (2013). Probabilistic models of expectation violation predict psychophysiological
emotional responses to live concert music. Cogn. Affect. Behav. Neurosci.
13, 533–553.

### 72. Hedges, T., and Wiggins, G. A. (2016). The prediction of merged attributes

with multiple viewpoint systems. J. New Music Res. 45, 314–332.

### 73. Eerola, T., and Toiviainen, P. (2004). MIR in Matlab: The MIDI Toolbox. In

Proc. 5th International Conference on Music Information Retrieval,
pp. 22–27.

### 74. Gingras, B., Pearce, M. T., Goodchild, M., Dean, R. T., Wiggins, G., and

McAdams, S. (2016). Linking melodic expectation to expressive perfor-
mance timing and perceived musical tension. J. Exp. Psychol. Hum. Percept. Perform. 42, 594–609.

### 75. Brainard, D. H. (1997). The psychophysics toolbox. Spat. Vis. 10, 433–436.

### 76. Eaton, J. W., Bateman, D., Hauberg, S., and Wehbring, R. (2017). GNU

Octave} version 4.4.1 manual: a high-level interactive language for numer-
ical computations (Octave). Current Biology 29, 4084–4092, December 2, 2019

### 77. Tervaniemi, M., Schro¨ ger, E., Saher, M., and N€a€at€anen, R. (2000). Effects

of spectral complexity and sound duration on automatic complex-sound
pitch processing in humans - a mismatch negativity study. Neurosci. Lett. 290, 66–70.

### 78. Bogdanov, D., Wack, N., Go´ mez, E., Gulati, S., Herrera, P., Mayor, O., Roma, G., Salamon, J., Zapata, J. R., and Serra, X. (2013). ESSENTIA:
an audio analysis library for music information retrieval. In International
Society for Music Information Retrieval Conference (ISMIR13) (Curitiba, Brazil), pp. 493–498.

### 79. Barr, D. J., Levy, R., Scheepers, C., and Tily, H. J. (2013). Random effects

structure for conﬁrmatory hypothesis testing: keep it maximal. J. Mem. Lang. 68, 255–278.

### 80. Cox, R. W. (1996). AFNI: software for analysis and visualization of functional

magnetic resonance neuroimages. Comput. Biomed. Res. 29, 162–173.

### 81. Mueller, K., Lepsien, J., Mo¨ ller, H. E.,
and
Lohmann, G.
(2017). Commentary: Cluster failure: why fMRI inferences for spatial extent have
inﬂated false-positive rates. Front. Hum. Neurosci. 11, 345.

### 82. Gl€ascher, J. P., and O’Doherty, J. P. (2010). Model-based approaches to

neuroimaging: combining reinforcement learning theory with fMRI data. Wiley Interdiscip. Rev. Cogn. Sci. 1, 501–510.

### 83. Holmes, A. P., and Friston, K. J. (1998). Generalisability, random effects &

population inference. Neuroimage 7, S754.

### 84. Mumford, J. A., Poline, J.-B., and Poldrack, R. A. (2015). Orthogonalization

of regressors in FMRI models. PLoS ONE 10, e0126255.

### 85. Chen, G., Cox, R. W., Glen, D. R., Rajendra, J. K., Reynolds, R. C., and

Taylor, P. A. (2019). A tail of two sides: artiﬁcially doubled false positive
rates in neuroimaging due to the sidedness choice with t-tests. Hum. Brain Mapp. 40, 1037–1043. Current Biology 29, 4084–4092, December 2, 2019

STAR+METHODS

## KEY RESOURCES TABLE

## LEAD CONTACT AND MATERIALS AVAILABILITY

Further information and requests for resources and reagents should be directed to and will be fulﬁlled by the Lead Contact, Stefan
Koelsch (stefan.koelsch@uib.no). This study did not generate new unique reagents.

## EXPERIMENTAL MODEL AND SUBJECT DETAILS

A total of 83 healthy human adults took part in the study. Data from one male subject in Experiment 1 was excluded due to non-
compliance with the experimental procedure. Functional MRI data from two subjects (1 female, 1 male) in Experiment 2 were
excluded due to data-handling errors, and one further female subject was excluded as her overall music reward score (see below)
was over 3 standard deviations below the population mean. Subjects took part in either the behavioral or fMRI experiment, but not
both to ensure that the stimuli were novel to the subjects. For Experiment 1, data were analyzed from 39 subjects with diverse levels of musical training (21 females, age: M = 24.1 y, SD =
3.80, general musical sophistication: M = 71.5, SD = 16 (corresponding to the 31st percentile of 147,633 self-selected subjects in the
‘How musical are you?’ test on the BBC website) from the Goldsmiths Musical Sophistication Index (Gold-MSI) [59], musical training
subscale of the Gold-MSI: M = 23.4, SD = 10.3, range = 7–41 (corresponding to the 1st and 86th percentile), overall music reward: M =
48.6, SD = 8.53 (population M = 49.98 and SD = 10.01 based on a sample of 857 young-adult subjects) from the Barcelona Music
Reward Questionnaire (BMRQ) [60]). For Experiment 2, data were analyzed from 40 subjects also with diverse levels of musical training (20 females, age: M = 25.2 y, SD = 4.16, general musical sophistication: M = 72.2, SD = 19.9 (corresponding to the 32nd percentile), musical training: M = 23.6, SD =
11.5, range = 7– 48 (corresponding to the 1st and 100th percentile), overall music reward: M = 47.9, SD = 10.3). No signiﬁcant differences in age (Mann-Whitney U = 888, p = 0.290), general musical sophistication (Welch’s t test t(74.38) = 0.175,
p = 0.861), musical training (Mann-Whitney U = 779, p = 0.996), or overall music reward (Mann-Whitney U = 817, p = 0.720) were
observed between subjects from the behavioral experiment (Experiment 1) and fMRI experiment (Experiment 2). No sex-speciﬁc an-
alyses were conducted as we were interested in effects general to the population. All subjects were self-reported right-handed, with normal hearing, had normal or corrected-to-normal vision, and reported no
known history of psychological or neurological disorders. Written informed consent was obtained from each subject prior to the
experiment, and the study was approved by the Ethical Committee of the Medical Faculty at Leipzig University.

## METHOD DETAILS

Information Dynamics Of Music model
We used the Information Dynamics Of Music (IDyOM) model [13, 56] to derive the surprise and uncertainty of every chord in the McGill
Billboard Corpus [21]. This unsupervised statistical-learning model computes the Shannon information content and entropy [61] of a
chord by prospectively generating a probability distribution for each chord in a song (or more generally, symbols in a sequence)
conditioned on its previous context and the prior experience of the model. REAGENT or RESOURCE
SOURCE
IDENTIFIER
Deposited Data
Brain-masks of regions involved in music-evoked emotions
[1]
https://doi.org/10.1038/nrn3666
McGill Billboard Corpus
[21]
https://ddmal.music.mcgill.ca/research/The_McGill_
Billboard_Project_(Chord_Analysis_Dataset)/
Software and Algorithms
Statistical Parametric Mapping 12 (version 7219)
Wellcome Centre for
Human Neuroimaging
https://www.ﬁl.ion.ucl.ac.uk/spm/software/spm12/
Information Dynamics Of Music (IDyOM) model
[56]
https://code.soundsoftware.ac.uk/projects/idyom-
project
MATLAB 2017b
MathWorks
https://www.mathworks.com

## R 3.5.1

RStudio
https://rstudio.com/
glmmTMB (ﬁx_conﬁnt_ar1 branch)
[57]
https://github.com/glmmTMB/glmmTMB
MarsBar 0.44
[58]
http://marsbar.sourceforge.net/
Current Biology 29, 4084–4092.e1–e4, December 2, 2019
e1

At the core of IDyOM is the PPM algorithm, a variable-order Markov model introduced by Cleary and Witten [62] and subsequently
updated by Moffat [63] and Bunton [64]. The PPM algorithm reads a sequence one symbol at a time, and generates a probability
distribution for the symbol by blending together predictions from n-gram models of different orders. An n-gram model of order
n–1 is a Markov model that generates the probability of a symbol by conditioning on the previous context of n–1 symbols. Thus, given
the set of all chords S and a chord progression fe1;.; ei;.; eNg, the n-gram probability of chord ei is given by pðei j eiðn1Þ;.;
ei1Þ. The information content of chord ei is deﬁned as the negative logarithm of its conditional probability, i.e., IðeiÞ =  log2p

ei
eiðn1Þ;.; ei1

while the entropy of chord ei is the expected information content of chord ei. This is obtained by multiplying the conditional probability
of all possible chords in S by their information contents then summing together, giving
HðeiÞ = 
X
e˛S
p

ei = e
eiðn1Þ;.; ei1

log2p

ei = e
eiðn1Þ;.; ei1

Previous work has demonstrated the superiority of IDyOM over ﬁxed order n-gram models in modeling listeners’ probabilistic ex-
pectations of musical events [19, 56]. IDyOM incorporates both a short-term model and a long-term model. The short-term model is trained incrementally on the current
progression, thereby learning statistical regularities speciﬁc to the current stimulus. The long-term model is trained on all stimuli in a
representative corpus of musical compositions, simulating the listener’s prior musical exposure; here we used the McGill Billboard
pop music corpus as it reﬂects a musical style that is popular and widely accessed by listeners of Western tonal music, and contains
the most common chord progressions in pop music. We also applied 10-fold cross-validation to avoid overﬁtting to individual songs. IDyOM combines the short- and long-term models using a geometric weighted mean [65], where each model is inversely weighted by
the entropy of its predictions. This model conﬁguration, termed ‘BOTH’ in [66], has proved to be useful both for modeling musical
style [67] and for modeling music perception (e.g., [19, 68–71]). Consequently, IDyOM captures both stylistic regularities (from the
training corpus) and local regularities (from the portion of the song heard so far) to improve its ability to generate successful
predictions. Although previous applications of IDyOM have mostly been limited to the melodic domain [19, 56, 68–71], there is emergent inter-
est in applying the model to harmonies [23]. In melodic applications, an important aspect of IDyOM is the use of viewpoints to embody
different psychological and music-theoretic principles (e.g., relative pitch, tonality). Comparable viewpoint systems have yet to be
established in the harmonic domain (although see [72] for initial work in this direction). We therefore used IDyOM in a single-viewpoint
conﬁguration, where the symbolic alphabet consisted of chord symbols present in the training corpus and included scale degree,
chord type, and inversions. Stimuli
Stimuli consisted of 30 unique auditory chord progressions (Table S1) selected from 745 songs listed on the US Billboard ‘Hot 100’
chart between 1958 and 1991 in the McGill Billboard Corpus [21], resulting in a total of 1039 chords. The duration of each chord was
2.4 s, and each progression contained 30-38 chords (M = 34.6). These parameters were chosen to optimize signal-to-noise ratio of
the data given the long rise time (6 s until peak after stimulus onset) and sluggishness of the BOLD response in fMRI. Each chord
progression was also transposed to C major to further reduce the possibility of familiarity effects. No signiﬁcant correlations between
the uncertainty and surprise of chords were detected in the stimulus set (r = 0.0218, p = 0.482; Figure 1C; Table S3). Chord sequences were chosen by ﬁrst generating all possible (494,807) chord progressions containing 30-38 chords for every
song in the corpus, and imposing the criteria that 1) each progression must begin on the tonic root position and end on a perfect
or plagal cadence (as in most Western tonal compositions), 2) each progression must contain at least one chord that belongs to
each quadrant of the product [high/low informational content] 3 [high/low entropy] (where high and low respectively denote the upper
and lower 40th percentile of chords in the corpus), and occurs at least ﬁve chords after onset and before the end of each progression,
3) each progression must contain at least unit variance in entropy and log(information content) (to adjust for skewness in the distri-
bution) in each progression, and that 4) each sub-sequence of at least ﬁve chords must only repeat after a gap of at least two chords
and not repeat more than three times (including the ﬁrst presentation) consecutively. Note that the quadrant boundaries are con-
strained by the set of chords in the corpus, and may thus be conservative within the broader spectrum of musical styles beyond
pop music. We then selected exactly one progression from the remaining songs that minimized the ordinal relationship between in-
formation content and 1-lagged entropy (i.e., the entropy of the subsequent chord) using Kendall’s tau. This ﬁnal step was carried out
for another study with a different research question. All chords were initially generated as MIDI ﬁles using the MIDI-Toolbox [73] in MATLAB R2013b (MathWorks, Natick, MA, USA) and
rendered as wav ﬁles (44100 Hz sampling rate) with a synthetic timbre composed of a jazz guitar, an acoustic guitar, and a marimba
using Pro Tools (Avid Technology, Burlington, MA, USA). All instruments played the full chords together in every stimulus. Three sepa-
rate background rhythms with a synthetic drum-kit timbre were made using GarageBand for iOS (Apple, Cupertino, CA, USA), and
superposed on the sound waves in MATLAB. Each rhythm spanned the duration of each chord, was in quadruple time (regardless of
the time signature of the original song), and was repeated throughout each stimulus. These background rhythms were introduced to
enhance the momentum of the stimuli given the relatively slow tempo of the chord progressions. Reverberation and damping were
e2
Current Biology 29, 4084–4092.e1–e4, December 2, 2019

adjusted to ensure that the waveform of each chord and rhythm did not spill over to the subsequent chord. The auditory stimuli were
then normalized in loudness using ReplayGain in Audacity (https://www.audacityteam.org/). Procedure for Experiment 1
Subjects gave pleasantness ratings to chords in auditory chord sequences using a custom-built 10 cm analog mechanical slider in a
soundproof cabin. The slider was held with the left hand and placed on the lap perpendicular to the body, while the right thumb was
used to move the slider pot. Moving the pot away from the body indicated a higher rating, and vice versa. The highest rating was ‘sehr
angenehm’ (very pleasant), and the lowest was ‘nicht angenehm’ (not pleasant). Each trial began with the subject resetting the slider
to the lowest rating as the ﬁrst chord was identical for all stimuli (ratings from the ﬁrst chord were excluded from the analysis), and the
stimulus was presented 2 s afterward. Subjects rated the pleasantness of each chord in the auditory sequence by moving the slider
pot to its corresponding position, and were explicitly told to give at most one rating for every chord. They were encouraged to use the
full range of the slider, and to select extreme ratings at least 5 times throughout the entire experiment as in prior work [74]. Once the
chord progression was over, subjects were given two 3 s time-windows to rate the overall pleasantness and arousal of the progres-
sion (order pseudo-randomized) on a 1-6 scale using the top number keys on a computer keyboard. Subjects were then prompted to
begin the next trial as before. The 30 auditory isochronous chord progressions were presented in a pseudo-random order, with the three background rhythms
evenly assigned to the stimuli and counterbalanced across participants. The experiment was delivered using PsychToolbox 3 [75] in
Octave 4.0.0 [76], and stimuli were presented using supra-aural headphones (Beyerdynamic DT 770 PRO) at a comfortable volume. The slider was connected to an Arduino Micro microcontroller that acted as a digital-analog converter with a 20 Hz sampling rate. Subjects practised on three trials (with a different set of stimuli) prior to the experiment to ensure they understood the task. At the
end of the experiment, subjects were asked whether the chord progressions in the stimuli were familiar to them, and if possible,
to name the possible artist or song. No subjects mentioned the relevant artist or song featured in our stimuli, except for one subject
who suggested the possibility of a chord progression by The Beatles without actually identifying the song. Procedure for Experiment 2
The fMRI experiment was divided into ﬁve runs, and the procedure was similar to the behavior experiment. Each trial began with the
instruction asking subjects to close their eyes, then the presentation of an auditory chord progression ensued after a 10 s pause. Subjects’ task was to listen attentively to the chord progressions and to pay attention to how each chord ﬁts in with the previous
chords in the progression. A 1 s-sine wave tone (C5 = 523.25 Hz) then informed subjects to open their eyes 1 s after the end of stim-
ulation. Following a 1 s pause, subjects were given two 3 s time-windows to rate overall pleasantness and arousal of the stimulus
using a 1-6 scale (order randomized to minimize motor preparation) on an MR-compatible button box in each hand. They were
then instructed to close their eyes again and the next trial began. In each run, six auditory sequences (two of each rhythm, counterbalanced across subjects) were pseudo-randomly selected from
the 30 stimuli and presented without replacement. The experiment was delivered using PsychToolbox 3 in Octave 4.0.0, and stimuli
were presented using noise-isolating earphones (Sensimetrics S14) at a comfortable volume. Foam pads were placed around the
head to minimize movement, and the scanner was stopped for a pause of approximately 60 s at the end of each run. Subjects prac-
ticed on three trials (with a different set of stimuli) outside the scanner prior to the experiment to ensure they understood the task. At
the end of the experiment, subjects were asked whether the chord progressions in the stimuli were familiar to them, and if possible, to
name the possible artist or song. No subjects mentioned the relevant artist or song featured in our stimuli.
fMRI data acquisition for Experiment 2
Brain imaging data were acquired on a 3T Magnetom Skyra scanner (Siemens Healthcare, Erlangen, Germany) with a 32-channel
head coil and a multiband EPI sequence [37, 38] (TR = 500 ms, TE = 24 ms, ﬂip-angle = 45, FoV = 204 mm, in-plane matrix =
68 3 68, slice thickness = 3.2 mm, inter-slice gap = 0.32 mm, phase-encoding = A/P, multiband acceleration factor = 4, 7/8 par-
tial-Fourier sampling, pre-scan normalization enabled, 1241 volumes per run, 5 runs in total). Slices were oriented along the axial
plane parallel to the AC-PC line and covered the whole neocortex (with partial coverage of the cerebellum and brainstem). Six dummy
scans were acquired and discarded by the scanner for steady-state magnetisation at the start of each run.

## QUANTIFICATION AND STATISTICAL ANALYSIS

Behavioral data analysis for Experiment 1
To obtain pleasure ratings for all chords, the pleasantness time series for every chord progression was ﬁrst smoothed using a moving
median ﬁlter with a ﬁfth-order symmetric window to reduce analog noise. The mode of the smoothed signal was then sampled in a
time window from one second after each chord onset until its end to account for delays in moving the slider. The ﬁrst chord of each
progression was discarded since each trial began by resetting the slider. Stationarity of each uncertainty and surprise sequence (derived using IDyOM) was examined using the Augmented Dickey-Fuller
(ADF) test and Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test, and suggested that no differencing was required. We then ﬁtted a linear mixed model using the package glmmTMB [57] in R 3.5.1 using RStudio (RStudio, Boston, MA, USA). The
response variable was the pleasantness rating of each chord (averaged across subjects), and the predictors of interest were chord
Current Biology 29, 4084–4092.e1–e4, December 2, 2019
e3

uncertainty, surprise, as well as the interaction between the two variables. This interaction is given by the element-wise product of
uncertainty and surprise. As previous work suggested that sensory dissonance, spectral complexity, and spectral centroid also affect
pleasure ratings in music [32–35, 77], we extracted the mean value of these low-level acoustic features for every chord using Essentia
2.1 [78] and entered them as covariates in the model. We also added overall pleasantness and overall arousal ratings of each excerpt
as covariates. Furthermore, stimulus-speciﬁc random effects were included for the intercept, surprise, interaction between
uncertainty and surprise, sensory dissonance, and spectral complexity. These were selected following the suggestion of Barr and
colleagues [79], where all ﬁxed effects predictors were initially also entered as random effects, and then dropped as random effects
until the model converged. A ﬁrst-order autoregressive covariance structure was also used to model the autocorrelation between
each subsequent chord rating in a given stimulus. All predictors and the response variable were moreover standardized before
entering into the model. Parameters were estimated using maximum likelihood for model comparison. Model residuals were visually
inspected for homoscedasticity and normality. Subject-speciﬁc random effects were not included as the model residuals became
severely heteroscedastic. We further ﬁtted a null model for a full null model comparison to guard against inﬂated Type I errors [28, 29]. This null model was
formed by dropping from the full model our predictors of interest (i.e., uncertainty, surprise, and their interaction), and the random
effect of surprise (due to convergence issues). After establishing the overall signiﬁcance of the full model over the null model (likeli-
hood-ratio test: c2(8) = 225, p < 2.20 3 1016) using a signiﬁcance threshold of p < 0.05, the signiﬁcance of each ﬁxed effect in the full
model (Table 1) was tested against reduced models (where effect is dropped) using the likelihood ratio test. Here, we report Wald
95%-conﬁdence intervals.
fMRI data preprocessing for Experiment 2
Functional MRI images were analyzed using SPM12 (Wellcome Centre for Human Neuroimaging, London, UK) version 7219 in
MATLAB 2017b. After conversion to Nifti format, acquired images were despiked using 3dDespike in AFNI [80], then motion-cor-
rected, co-registered to subjects’ T1-weighted structural image, normalized to MNI space and resampled to the native voxel reso-
lution [81], before smoothing with a 6 3 6 3 6.4-mm (corresponding to twice the voxel size) FWHM Gaussian kernel. Slice-timing
correction was not applied given the fast repetition time of the acquisition sequence.
fMRI data analysis for Experiment 2
We analyzed our model-based fMRI [82] data using a two-stage mixed effects model [83]. A linear model was ﬁrst ﬁtted on the subject
level with one boxcar function modeling the stimulation of each chord progression, and standardized parametric modulators coding
uncertainty, surprise, interaction between uncertainty and surprise, sensory dissonance, spectral centroid, and spectral complexity
of each chord, as well as valence and arousal ratings for each progression. These regressors were convolved with the canonical hae-
modynamic response function and its temporal derivative. Each parametric modulator was separately orthogonalised with respect to
the task-regressor to correctly assign signal variance to the main stimulus regressor [84]. Six rigid-body transformation regressors
were further introduced as covariates to reduce motion-induced artifacts. Effects of temporal autocorrelation were modeled with a
FAST-autoregressive model, and a high-pass ﬁlter with a 128 s cut-off was applied to remove low-frequency scanner drifts. Individual
means and variances were then pooled into a group-level model for population inferences. As we aimed to identify the neural cor-
relates of chord uncertainty and surprise in brain regions previously implicated in music-evoked emotions, we took all seven signif-
icant clusters from a meta-analysis on anatomical regions implicated in music-evoked emotions [1]. These consisted of the bilateral
amygdala and a restricted portion of the anterior hippocampal formation adjacent to the amygdala (including the hippocampal-amyg-
daloid transition area, hippocampus proper, and the subiculum), right ventral striatum (including the nucleus accumbens), left
caudate nucleus, bilateral auditory cortex, and the pre-supplementary motor area. Population inferences (Figure 3; Table S4) were made on the mean parameter estimates obtained with MarsBar version 0.44 [58]
using two-tailed one-sample and paired t tests (as suggested in [85]). If data deviated from normality according to the Shapiro-Wilk
test, sign tests or Wilcoxon signed-rank tests were instead conducted with 95% bootstrap conﬁdence intervals of the median on
10000 permutations. P values and conﬁdence intervals were Bonferroni-corrected according to the number of regions tested in a
given analysis.

## DATA AND CODE AVAILABILITY

Data supporting ﬁndings of this study are available from the Lead Contact upon request. Code for the IDyOM model is available at
Sound Software: https://code.soundsoftware.ac.uk/projects/idyom-project. The McGill Billboard corpus dataset is available at
DDMAL: https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/
e4
Current Biology 29, 4084–4092.e1–e4, December 2, 2019

Current Biology, Volume 29
Supplemental Information
Uncertainty and Surprise Jointly
Predict Musical Pleasure and Amygdala, Hippocampus, and Auditory Cortex Activity
Vincent K. M. Cheung, Peter M. C. Harrison, Lars Meyer, Marcus T. Pearce, John-Dylan
Haynes, and Stefan Koelsch

Figure S1. Comparing effects between bilateral amygdala and hippocampus regions of
interest (Amyg/Hipp). Related to Figure 3. No significant differences between the hemispheres were detected in the amygdala and adjacent
anterior hippocampus for the interaction between chord uncertainty and surprise (Wilcoxon sign-
rank test (two-sided): z = -0.618, p = 0.536; n = 40; filled-circles: data points; solid line: median;
diamond: mean; notches: 95%-CI of the median; hinges: IQR; whiskers: range of data). Figure S2. Comparing effects between bilateral auditory cortex (AC). Related to Figure 3. The interaction between chord uncertainty and surprise was significantly stronger in the left
hemisphere than the right (paired t-test (two-sided): t(39) = 2.60, p = 0.013; n = 40; filled-circles:
data points; solid line: median; diamond: mean; notches: 95%-CI of the median; hinges: IQR;
whiskers: range of data). Figure S3. Testing effects of chord uncertainty at the contralateral nucleus accumbens
(NAcc) and caudate nucleus (CN). Related to Figure 3. Activity modulation by chord uncertainty was also examined in the left nucleus accumbens and
right caudate post-hoc by flipping the x-axes of the clusters to the contralateral hemisphere using
MarsBar (see STAR Methods; one-sample t-test (two-sided); * p < 0.05, ** p < 0.01, *** p <
0.001, Bonferroni-corrected for multiple comparisons; n = 40; filled-circles: data points; solid line:
median; diamond: mean; notches: 95%-CI of the median; hinges: IQR; whiskers: range of data). Stimulus
number
Title
Artist
ID in
McGill
Billboard
corpus
Position
in song
of first
chord
Position
in song
of last
chord
Sequence
length

Invisible Touch
Genesis

Suite: Judy Blue Eyes
Crosby, Stills &
Nash

Hooked On A Feeling
B. J. Thomas

Sweet Surrender
Bread

Hey Baby
Bruce Channel

Don't Ask Me Why
Billy Joel

With a Little Luck
Paul McCartney

I Want You Back
The Jacksons

Back in the High Life Again
Steve Winwood

I Love You So
Bobbi Martin

There She Goes
The LAs

You Decorated My Life
Kenny Rogers

Never Knew Love Like This
Before
Stephanie Mills

Buy For Me The Rain
Nitty Gritty Dirt
Band

Oh Father
Madonna

The Animals
San Franciscan
Nights

When It's Love
Van Halen

Country Road
James Taylor

Ob-La-Di, Ob-La-Da
The Beatles'

Knowing Me, Knowing You
ABBA

Red Red Wine
UB40

One Bad Apple
The Osmonds

This Should Go On Forever
Rod Bernard

Rock And Roll Never Forgets
Bob Seger

Black Cars
Gino Vannelli

Two Hearts
Phil Collins

My World Fell Down
Sagittarius

Don't Leave Me This Way
Thelma Houston

Sleep Walk
Santo & Johnny

Mr. Bojangles
Jerry Jeff Walker

Mean number of chords per stimulus: 34.6; Total number of chords: 1039

Table S1. Summary details of the original pop songs featured in our chord stimuli. Related
to Figure 1. Stimuli consisted of 30 unique isochronous chord progressions extracted from 30 different songs
in the McGill Billboard corpus (see STAR Methods). The chord progressions were transposed
from their original key to C major. Here we list the original titles and artists, as well as their
identification within the corpus. Consecutive repetitions of the same chord were counted as one
instance when calculating chord positions within each song. Grouping variable: Chord sequence
Predictor
SD
Correlation
Intercept
0.177
Surprise
0.209
0.69
Sensory dissonance
0.0467 -0.23
-0.54
Spectral complexity
0.168
0.16
0.12 -0.63
Uncertainty × Surprise
0.0899 0.00
0.37 -0.06 -0.23
Chord position within sequence 0.433
0.73
(AR1)
Table S2. Correlation of random effects of the linear mixed model in Experiment 1. Related
to Table 1. Please also note that stationarity was assessed using the KPSS and ADF tests, and response
autocorrelation was taken into account using an AR(1) model (see STAR Methods for details). Refer to Table 1 for fixed effects estimates of the same model. Uncertainty
Surprise
Sensory
dissonance
Spectral
centroid
Spectral
complexity
Uncertainty
-0.0218
0.0418
-0.0189
-0.118***
Surprise
0.347***
-0.312***
0.0211
Sensory dissonance
-0.215***
0.241***
Spectral centroid
-0.0681*
Spectral complexity
Table S3. Pairwise Pearson’s correlation matrix between predictive uncertainty and
surprise, as well as low-level acoustic features of all chords (n = 1039) in the stimuli. Related
to Table 1.
*: p < 0.05, **: p < 0.01, ***: p < 0.001 (all uncorrected and two-tailed)

Chord uncertainty × surprise
Anatomical location
Mean β
Corrected 95%-CI
Test statistic Corrected p
Left amygdala/hippocampus
-0.116
[-0.201, -0.0445]
s = 11
0.0450 *
Right amygdala/hippocampus
-0.140
[-0.238, -0.0410]
t(39) = -4.02
0.00181**
Left auditory cortex
-0.182
[-0.288, -0.0766]
t(39) = -4.90 0.000120 ***
Right auditory cortex
-0.128
[-0.220, -0.0355]
t(39) = -3.93
0.00234 **
Right nucleus accumbens
-0.363
[-0.155, 0.0827]
t(39) = -0.866

Left caudate nucleus
-0.0451
[-0.174, 0.0836]
t(39) = -0.996

Pre-supplementary motor area 0.00197
[-0.104, 0.0424]
s = 17

Chord uncertainty
Anatomical location
Mean β
Corrected 95%-CI
Test statistic Corrected p
Left amygdala/hippocampus
-0.123
[-0.235, 0.0327]
s = 17

Right amygdala/hippocampus -0.109
[-0.249, 0.0313]
t(39) = -2.20
0.234
Left auditory cortex
0.314
[0.105, 0.523]
t(39) = 4.26
0.000877***
Right auditory cortex
0.453
[0.299, 0.606]
t(39) = 8.37 2.17×10-9 ***
Right nucleus accumbens
0.242
[0.0720, 0.412]
t(39) = 4.04
0.00170 **
Left caudate nucleus
0.281
[0.0661, 0.496]
t(39) = 3.71
0.00447 **
Pre-supplementary motor area
0.358
[0.145, 0.570]
t(39) = 4.78 0.000176 ***

Chord surprise
Anatomical location
Mean β
Corrected 95%-CI
Test statistic Corrected p
Left amygdala/hippocampus
-0.102
[-0.223, 0.0238]
t(39) = -2.30
0.188
Right amygdala/hippocampus
-0.112
[-0.232, 0.00807]
t(39) = -2.65
0.0813
Left auditory cortex
-0.263
[-0.373, -0.152]
t(39) = -6.75 3.30×10-7 ***
Right auditory cortex
-0.227
[-0.335, -0.118]
t(39) = -5.91 4.78×10-6 ***
Right nucleus accumbens
0.000629
[-0.125, 0.138]
t(39) = 0.136

Left caudate nucleus
0.0128
[-0.143, 0.168]
t(39) = 0.235

Pre-supplementary motor area
0.105
[-0.0940, 0.304]
t(39) = 1.50
0.993
Table S4. Effects of uncertainty, surprise, and their interaction on the BOLD response in
different anatomical locations. Related to Figure 3. Mean parameter estimates of each region were obtained for all subjects and tested against zero
using two-sided one-sample t-tests, or the sign test (when data deviated from normality according
to the Shapiro-Wilk test). P-values and confidence intervals were Bonferroni-corrected for
multiple comparisons at each anatomical region. *: p < 0.05, **: p < 0.01, ***: p < 0.001.
