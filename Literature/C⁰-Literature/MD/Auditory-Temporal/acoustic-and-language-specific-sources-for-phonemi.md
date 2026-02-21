# acoustic-and-language-specific-sources-for-phonemi

Article https://doi.org/10.1038/s41467-024-44844-9
Acoustic and language-speciﬁcs o u r c e sf o r
phonemic abstraction from speech
Anna Mai 1 ,S t e p h a n i eR i è s2,3, Sharona Ben-Haim4, Jerry J. Shih 5 &
Timothy Q. Gentner 6,7,8
Spoken language comprehension requires abstraction of linguistic informa-
tion from speech, but the interaction between auditory and linguistic pro-
cessing of speech remains poorly understood. Here, we investigate the nature
of this abstraction using neural responses recorded intracranially while parti-
cipants listened to conversational English speech. Capitalizing on multiple,
language-speciﬁc patterns where phonological and acoustic information
diverge, we demonstrate the causal efﬁcacy of the phoneme as a unit of ana-
lysis and dissociate the unique contributions of phonemic and spectrographic
information to neural responses. Quantitive higher-order response models
also reveal that unique contributions of phonological information are carried
in the covariance structure of the stimulus-response relationship. This sug-
gests that linguistic abstraction is shaped by neurobiological mechanisms that
involve integration across multiple spectro-temporal features and prior pho-
nological information. These results link speech acoustics to phonology and
morphosyntax, substantiating predictions about abstractness in linguistic
theory and providing evidence for the acoustic features that support that
abstraction.
While much is known about the brain ’s response to the acoustic
properties of speech, comparatively less is known about how the
neural response to speech sounds integrates into the larger picture of
language processing and comprehension. Phonology, as the analytical
level in linguistic theory that bridges speech acoustics and morpho-
syntax, is likely critical to understanding this transformation.
However, many results characterizing phonological processing
appear reiterant of purely acoustic results. For example, tuning to
spectrotemporal features of speech is spatially organized in both pri-
mary and secondary auditory areas
1–5, and sensitivity to phonological
features recapitulates that spatial organization 6. Faced with such
similarities, some have questioned whether phonology and its atten-
dant level of abstraction are relevant to speech processing at all
7–10.
Uncertainty around the neurocognitive reality of phonology is
likely driven by the fact that phonological information is in general
highly redundant with acoustic information
11,12. Consistent with this,
word recognition modelsﬁt with purely acoustic features can perform
with human-like accuracy 13, and purely acoustic neural encoding
models can perform identically to those given phonological
information
10. Such results underscore the richness of the information
available purely from speech acoustics.
Nevertheless, divergences between acoustic similarity and pho-
nological similarity are well-established in linguistics 14–16,a n ds o m e
evidence suggests these information types are neurally dissociable as
well. For example, Di Liberto et al.
17 show that models containing both
continuous spectrotemporal features and categorical phonological
Received: 5 January 2023
Accepted: 3 January 2024
Check for updates
1University of California, San Diego, Linguistics, 9500 Gilman Dr., La Jolla, CA 92093, USA.2San Diego State University, School of Speech, Language, and
Hearing Sciences, 5500 Campanile Drive, San Diego, CA 92182, USA.3San Diego State University, Center for Clinical and Cognitive Sciences, 5500
Campanile Drive, San Diego, CA 92182, USA.4University of California, San Diego, Neurological Surgery, 9500 Gilman Dr., La Jolla, CA 92093, USA.5University
of California, San Diego, Neurosciences, 9500 Gilman Dr., La Jolla, CA 92093, USA.6University of California, San Diego, Psychology, 9500 Gilman Dr., La Jolla,
CA 92093, USA. 7University of California, San Diego, Neurobiology, 9500 Gilman Dr., La Jolla, CA 92093, USA.8University of California, San Diego, Kavli
I n s t i t u t ef o rB r a i na n dM i n d ,9 5 0 0G i l m a nD r . ,L aJ o l l a ,C A9 2 0 9 3 ,U S A .e-mail: acmai@ucsd.edu
Nature Communications|          (2024) 15:677 1
1234567890():,;
1234567890():,;
features outperform models that contain only spectrotemporal or only
phonological features, suggesting that the information accounted for
by each of these feature sets is not fully identical. However, the rela-
tionship between these two types of features remains to be
understood.
Rather than undermining the status of phonology in language
processing altogether, we argue that the high degree of overlap
between acoustic and phonological information accentuates the
importance of careful experimental design to assess the unique con-
tribution of phonological information and its relationship to speech
acoustics. Only through investigation at the edges of this informational
overlap, at points of acoustic-phonemic divergence, will it be possible
to identify neural signatures of pu rely phonological processes and
determine the nature of links between sensory processing and lan-
guage cognition.
Points of acoustic-phonemic divergence are common cross-lin-
guistically, but are speciﬁc to particular languages. That is, while two
different languages may have many points of acoustic-phonemic
divergence and may share some points of divergence in common,
altogether each language has a unique set. In this way, acoustic-
phonemic divergences provide a window on linguistic abstraction,
because they require higher-order knowledge of a particular language
(e.g., Tagalog vs. Quechua).
This study focuses on the phonological opposition between the
English abstract categories /d/ and /t/ and their contextual acoustic
neutralization to the sound [
], a coronal tap. English phonemes /d/
and /t/ have many acoustically distinct acoustic realizations that are
conditioned by the surrounding phonological context. These con-
textually conditioned variants are called allophones of /d/ and /t/.
Some allophones of /d/ and /t/ are acoustically distinct from one
another, but when either /d/ or /t/ occurs following a stressed syllable
and between two vowels, their acoustic contrast is neutralized, and
both are pronounced as a coronal tap (e.g., writing, riding). This
acoustic neutralization is demonstrated in Supplementary Fig. 1 for the
stimuli used in this study.
Given that many aspects of auditory processing proceed in a
feedforward manner from spectrotemporal features of the sensory
input, it is anticipated that many speech responsive sites will demon-
strate an acoustic ‘surface response’, where the responses for all taps
are more similar to one another than to the voiceless coronal stop
allophone of /t/. However, if it is also the case that phonological con-
text is used to compute phonemic identity during language proces-
sing, even when the acoustic contrast between two phonemes is
neutralized, then there also should exist sites demonstrating a pho-
nemic ‘underlying response’, where the neural response to under-
lyingly /t/ taps (e.g., writing) is more similar to the response to other
allophones of /t/ (e.g., voiceless alveolar stops) than to underlyingly /d/
taps (e.g., riding).
Observing both sites with acoustic surface responses and sites
with phonemic underlying responses would provide evidence for a
speciﬁc kind of phonological abstraction from surface acoustics that
to date has only been argued to exist in theory. In this way, points of
acoustic-phonemic divergence act as powerful handles on the rela-
tionship between sensory and linguistic processing, in this case, pro-
viding a window on a one-to-many mapping of acoustic forms to
phonological constructs.
Moreover, just as points of acoustic-phonemic divergence
elucidate the nature of abstraction from surface acoustics to
underlying phonological structure, points of phonemic-morphemic
divergence, where morphemes are not in a one-to-one relationship
with phonemes, provide critical testing grounds for understanding
the junction between phonology and morphosyntax. In particular,
many morphemes have more than one distinct phonemic form,
where the form that is pronounced is conditioned by the
surrounding phonological context. These contextually conditioned
variants of morphemes, called allomorphs, provide a window on
many-to-one mappings from phonological forms to morphological
meanings.
The morpho-phonological processes considered in this study are
the formation of the English regular past tense and regular plural. The
morphemes for the regular past tense and regular plural both exhibit
variation in their realization depending on the phonological context.
T h er e g u l a rp a s tt e n s et a k e so n eo ft h r e ef o r m s :as y l l a b i cv o i c e d
coronal stop [
d] following [t] or [d] (e.g., gifted, folded), a voiceless
coronal stop [t] following the remaining voiceless consonants (e.g.,
kissed, plucked), or a voiced coronal stop [d] following the remaining
voiced sounds (e.g., hugged, shoved). The regular plural analogously
manifests in one of three forms: a syllabic voiced coronal sibilant [
z]
following sibilants [s, z, tʃ,d ʒ, ʃ, ʒ]( e . g . ,beaches, palaces), a voiceless
coronal sibilant [s] following the remaining voiceless consonants (e.g.,
forests, peaks), or a voiced coronal sibilant [z] following the remaining
voiced sounds (e.g., mountains, hovels).
Since similarity of acoustic form and neural response is a well-
established principle of auditory processing (e.g., 6), it is anticipated
that some speech responsive sites will demonstrate a ‘surface
response’, where responses for [z] forms of the plural and [d] forms of
the past tense are more similar to word- ﬁnal non-plural [z] and non-
past [d], respectively, than to the voiceless forms of the plural and past
tense, respectively. Additionally, if it is the case that morphological
identity is abstracted from phonological context, then there should
also exist sites demonstrating a morphological‘underlying response’,
where the neural responses to both voiced and voiceless forms of the
plural and past tense pattern together to the exclusion of word ﬁnal
non-plural [z] and non-past [d], respectively.
In this way, observing the distribution of surface and underlying
sites for the plural and past tense comparisons has the potential to
provide critical evidence for the mental reality of phonemes and
morphemes and substantiate basic assumptions of generative lin-
guistic theory.
In addition to these phonologically and morphologically moti-
vated comparisons, this study also makes use of a receptive ﬁeld
estimation technique as a linking hypothesis. Receptive ﬁeld estima-
tion approaches use mathematically explicit hypotheses about the
nature of the relationship between stimulus and response to estimate
what features of the stimulus drive a response. Because the effects of
hypotheses used by different approaches can be compared straight-
forwardly through their explicit mathematical de ﬁnitions, these
approaches are immanently well-suited to answer questions concern-
ing the nature of the link between acoustic signals and language
representation in the brain.
Receptive ﬁeld estimation methods can be roughly divided into
linear methods that correlate the neural response directly to compo-
nents of the stimulus ( s
i)a n d quadratic methods that additionally
correlate the neural response to pairwise (sisj) (or even higher order)
products of stimulus components as well. Linear methods include the
spike-triggered average (STA)
18, maximally informative dimensions
(MID)19,a n d ﬁrst order maximum noise entropy models (MNE) 20.
Quadratic methods include the spike-triggered covariance (STC)21 and
second-order MNE models20.
This study compares the relative abilities of receptive ﬁeld com-
ponents recovered by ﬁrst-order and second-order MNE models to
reconstruct the neural response to speech. In doing so, this study
assesses whether the neural response to speech is impacted by the
stimulus covariance. To date, MNE models have been used to char-
acterize the receptive ﬁelds of putative single neurons based on spik-
ing activity in visual and auditory areas of nonhuman animals
22–25. Here,
we build on those successes, using MNE models to reconstruct
receptive ﬁelds from human intracranial LFP activity and assess whe-
ther phonemic category information aids in the reconstruction of
higher-order sensory receptiveﬁelds.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 2
In this study, a combination of MNE models, standard mixed
effects models, and targeted linguistic comparisons are used to show
how neural activity integrating over both acoustic and phonological
information supports linguistic abstraction. Language-speci ﬁcp a t -
terns of acoustic-phonemic divergence are leveraged to demonstrate
the causal efﬁcacy
12 of the phoneme as a unit of analysis and to dis-
tinguish its contributions from those of spectrotemporal cues. Mixed
effects models con ﬁrm the applicability of this ﬁnding to contexts
beyond acoustic-phonemic divergence and show how the contribution
of phonological information to the neural response varies across fre-
quency bands. Finally, using MNE models applied to human LFP data,
this work isolates features of the stimulus responsible for the efﬁcacy
of the phoneme, providing evidence for both neural features and sti-
mulus features that support phonology-speciﬁc activity in the brain. In
total, these results provide clear substantiation of predictions about
the nature of abstractness in phonology and evince acoustic features
that support that abstraction.
Results
Acoustics, phonology, and morphology drive neural activity
For assessing acoustic-phonemic divergence with coronal stop neu-
tralization, acoustic sites and phonemic sites were de ﬁned using a
sliding-window one-way ANOVA with 100ms windows and 50ms
overlap. For a site to be considered an acoustic site, there must have
existed at least one time window with a signiﬁcant ANOVA for which a
Tukey’s post hoc test indicated that there was a signiﬁcant difference
(α = 0.05) between surface [t] and tap /t/ tokens and between surface
[t] and tap /d/ tokens but no signiﬁcant difference between tap /t/ and
tap /d/ tokens. Alternatively, for a site to be considered a phonemic
site, there must have existed at least one time window with a signiﬁcant
ANOVA for which a Tukey ’s post hoc test indicated that there was a
signiﬁcant difference between tap /d/ and tap /t/ tokens and between
tap /d/ and surface [t] tokens but no signi ﬁcant difference between
surface [t] and tap /t/ tokens.
Similarly, for assessing phonemic-morphemic divergence with the
regular past tense, surface sites were considered to be those where the
sliding-window ANOVA was signiﬁcant for at least one time window
and for which a Tukey ’s post hoc test indicated that there was a sig-
niﬁcant difference (α = 0.05) between past tense [t] and past tense [d]
tokens and between past tense [t] and word ﬁnal non-past [d] tokens
but no signi ﬁcant difference between past tense [d] and word ﬁnal
non-past [d] tokens. For assessing phonemic-morphemic divergence
with the regular plural, surface sites were deﬁned as those with at least
one time window for which a Tukey’s post hoc test indicated that there
was a signiﬁcant difference (α = 0.05) between plural [s] and plural [z]
tokens and between plural [s] and wordﬁnal non-plural [z] tokens but
no signiﬁcant difference between plural [z] and word ﬁnal non-plural
[z] tokens.
For the two morphological patterns, the surface similarity com-
parison collapses the distinction between phonological surface and
underlying similarity. We take the plural comparison as an example to
illustrate this point; the following points apply analogously to the past
tense comparison. That is, the phonemic, underlying form of the plural
is typically considered to be /z/
26,27. Similarly, the phonemic underlying
form of word-ﬁnal non-plural [z] sounds is also /z/. The morphological
surface similarity response groups plural [z] and non-plural [z] toge-
ther to the exclusion of plural [s]. In this way, the morphological sur-
face similarity response groups sounds together that are both
acoustically similar ([z]) and phonemically similar (/z/). Thus, sites
identiﬁed as morphological surface similarity sites are not comparable
to the acoustic surface sites identiﬁed by the tap comparison because
morphological surface similarity sites con ﬂate phonological surface
and underlying similarity.
Morphological underlying sites were considered to be those for
which the comparison of evoked responses to past tense /t/, past tense
/d/, and word-ﬁnal non-past /d/ resulted in at least one time window
i n d i c a t i n gas i g n iﬁcant difference between word-ﬁnal non-past /d/ and
past tense /t/ tokens and between word- ﬁnal non-past /d/ and past
tense /d/ tokens but no signi ﬁcant difference between past tense /t/
and past tense /d/ tokens. Similarly, for the regular plural alternation,
morphological underlying sites were those for which there was at least
one time window indicating a signiﬁcant difference between word-ﬁnal
non-plural /z/ and plural /s/ tokens and between word-ﬁnal non-plural
/z/ and plural /z/ tokens but no signiﬁcant difference between plural /z/
and plural /s/ tokens. In this way, morphological underlying sites were
those which maintained language-speci ﬁc morphological similarity
based on the meaning of similar word- ﬁnal sounds rather than main-
taining the comparably less abstract similarity of their acoustic or
phonemic realization.
All sites that were speech responsive for at least one band are
s h o w ni nF i g .1b-e. Of the roughly 485 speech responsive electrodes for
each band, an average of 31 acoustic surface sites (SD ± 22.4) and 190
phonemic underlying sites (SD ± 38.5) were observed for the coronal
stop–tap alternation in each band. On average, six electrodes (SD ±
2.4) per band were categorized as both surface and underlying sites
for the tap comparison. The number of acoustic and phonemic sites
observed across bands is summarized in Table1, and examples of the
response observed at acoustic and phonemic sites are shown in Fig.2.
For the past tense alternation, for each band an average of 73 (SD ±
23.9) were categorized as surface sites, 46 (SD ± 8.8) were categorized
as morphological underlying sites, and one site (SD ± 1.1) was cate-
gorized as both a surface and morphological site. For the plural
alternation, 47 (SD ± 14.2) sites were categorized as surface sites, 45
(SD ± 12.2) were categorized as morphological underlying sites, and
one site (SD ± 0.5) was categorized as both a surface and morpholo-
gical site.
To assess the likelihood of observing these numbers of
surface and underlying response sites by chance, an expected null
distribution was generated for each frequency band by performing the
statistical analysis described above using 1,000 arbitrary pairs of
phones (i.e., A, B) with an arbitrary split of one phone (i.e., A, B
x, By).
For each arbitrary set of phones, surface sites were identiﬁed as those
with at least one time window in which there was a signi ﬁcant differ-
ence between the evoked response to A phones and the evoked
response to B phones, but no signi ﬁcant difference in the evoked
response toB
x and By phones. Underlying sites were identiﬁed as those
with at least one time window with no signiﬁcant difference between A
and Bx phones but a signiﬁcant difference between those phones and
By phones. In this way, the null distribution was generated from the
real, recorded data. Spatially correlated activity is thus preserved in the
null distribution, accounting for the possibility that such correlated
activity could in ﬂate the number of observed surface and under-
lying sites.
Compared against these null distributions, the numbers of
observed sites exhibiting surface and underlying patterns of activity
were greater than would be expected by chance for each band. For
example, for the high-gamma band, based on the generated distribu-
tion, the probability of observing at least 111 phonemic underlying sites
and at least 80 acoustic surface sites for the coronal stop –tap alter-
nation was <0.1%. Figure 3 shows the null distributions of surface and
underlying sites, with a dotted gold line marking the bound for 95% of
the distribution’s mass and blue points indicating the observed num-
ber of surface and underlying sites for the coronal tap comparison.
The numbers of sites exhibiting surface and underlying patterns
of activity were also greater than would be expected by chance for
both the regular past tense and plural comparisons. The probability of
observing the past tense pattern of at least 33 surface sites and at least
32 underlying sites was 0.1% for the high-gamma band, and the prob-
ability of observing the plural pattern of at least 19 surface sites and at
least 38 underlying sites was 0.2% for the same band. The expected and
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 3
observed distributions of surface and underlying sites are shown in
Fig. 3, with the expected distributions shown as heatmaps, and single
red (past) and green (plural) points indicating the observed number of
surface and underlying sites for the two morphophonological
comparisons.
Phoneme labels best explain low-frequency band power
Results from the coronal tap, plural, and past tense comparisons
provide evidence for distinct contributions of categorical phonemic
knowledge and acoustic processing to the neural response to speech.
Here we propose and assess a basic model of the relationship between
these two feature types using linear mixed effects (LME) models
similar to those reported by Di Liberto et al.
17. For each participant, for
each of the seven neural response types (=six classic frequency bands
and broadband LFP), seven LME models wereﬁt. Each model ﬁt neural
response with electrode channel and excerpt speaker as random
effects and either only spectrographic features, only phonemic label
features, or both spectrographic and phonemic label features asﬁxed
effects. Figure 4 illustrates how these three base models where con-
structed. Four additional models were also created, in which the
T a b l e1|C o u n to fs i t e sd e m o n s t r a t i n gas u r f a c es i m i l a r i t yp a t t e r no ra nu n d e r l y i n gs i m i l a r i t yp a t t e r nf o re a c hf r e q u e n c yb a n d
Coronal Tap Comparison Plural Comparison Past Tense Comparison
Band Surface Underlying Surface Underlying Surface Underlying
δ:( 1–3Hz) 16 211 59 42 95 55
θ:( 4–7Hz) 16 221 59 40 99 54
α:( 8–12Hz) 21 222 51 40 90 50
β:( 1 3–30Hz) 24 198 38 38 61 49
γ:( 3 1–50Hz) 30 178 54 72 58 36
High-γ:( 7 0–150Hz) 80 111 19 38 33 32
The observation of more surface sites than underlying sites for the morphological comparison is likely due to the fact that surface similarity for themorphological comparisons is analogous to both
surface and underlying similarity at the phonological level.
Fig. 1 | Stimulus-locked activity was recorded from speech responsive sites
across multiple lobes. a Neural activity was ﬁltered into functionally relevant
bands and labeled with time-aligned stimulus features, including spectrographic
and phonemic label information.b Coronal view of coverage for nine patients,
warped to standard MNI space.c Sagittal view of right hemisphere.d Sagittal view
of left hemisphere. e Axial view. For all views, electrodes that were speech
responsive for at least one frequency band are shown in light blue, and non-
responsive sites are shown in dark blue. The distribution of speech responsive sites
across bands is shown in Supplementary Fig. 2. Subﬁgures (b–e) were created using
the Python package nilearn (DOI: 10.5281/zenodo.8397156).
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 4
phonemic or spectrographic features had either been shufﬂed within
each excerpt or shufﬂed across the full recording session. Models were
then compared within participant and neural response type using the
Akaike Information Criterion (AIC)
28,a n da l lb e s t -ﬁt models carried
100% of the cumulative model weight and had an AIC score >200 lower
than other models.
Power in delta, theta, and alpha bands was bestﬁtb yL M Em o d e l s
that included both spectrographic features and phonemic labels
(s1p1). For these bands, the s1p1 model was the best ﬁt for nine out of
the ten participants, and the p1 model was the best ﬁt for one parti-
cipant (SD012). Power in the beta band was best ﬁt by the s1p1 model
for eight participants and the p1 model for two participants (SD010,
SD012). These results suggest that power in these bands is driven in
part by phonemic category information that is not reducible to speech
acoustics. For power in gamma and high-gamma bands, the best ﬁt
model varied across individuals. For gamma power, eight participants’
data were best ﬁt by the model that included only spectrographic
features (s1), and two participants’ data were bestﬁt by the s1p1 model
that included both spectrographic and phonemic label features
(SD013, SD018). Similarly, for high-gamma power, eight participants’
data were best ﬁt by the s1 model that included only spectrographic
features, and the remaining participants data were bestﬁtb yt h es 1 p 1
model that included both spectrographic and phonemic label feature
sets (SD011, SD018). These results suggest that power in frequencies
Fig. 2 | Responses to coronal tap, plural, and past tense comparisons exhibit
both surface similarity and underlying similarity patterns.Subplot titles indi-
cate the subject identity, channel name, and response band being plotted, and each
shows the time course of band power z-scored relative to baseline (-100 to 0 ms).
(a)a n d(b) show sites identiﬁed by the coronal stop-tap alternation. The evoked
response to tokens of [t] are shown in dark gray ( n=796); the evoked response to
taps derived from /t/ (tap /t/) is shown in teal (n=183); and the evoked response to
taps derived from /d/ (tap /d/) is shown in gold ( n=79). (c)a n d(d)s h o ws i t e s
identiﬁed by the past tense alternation. The evoked response to /t/ allomorphs of
the past tense are shown in dark gray (SD021: n=15, SD011: n=20); the evoked
response to /d/ allomorphs of the past tense is shown in teal (SD021: n=52, SD011:
n=53); and the evoked response to word-ﬁnal non-past tokens of /d/ is shown in
gold (SD021: n=141, SD011: n=138). (e)a n d(f) show sites identiﬁed by the plural
alternation. The evoked response to /s/ allomorphs of the plural is shown in dark
gray (n=51); the evoked response to /z/ allomorphs of the plural is shown in teal
(n=105); and the evoked response to word-ﬁnal non-plural tokens of /z/ is shown in
gold (n=194). For all subplots, shading indicates ±SEM. The distribution of sites
across bands for each comparison is shown in Supplementary Fig. 3.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 5
above 30Hz are primarily driven by speech acoustics rather than
phonemic category information.
For broadband LFP, nine participants ’ data were best ﬁtb yt h e
s1p1 model that included both spectrographic features and phonemic
labels, and one was best ﬁt by the p1 model (SD012) that contained
only phonemic label features. Given the 1/f structure of LFP data, this
neural measure is dominated by lower frequencies; thus, the fact that
the best ﬁt models for lower frequency bands are also the best ﬁt
models for the broadband LFP is somewhat expected. What is notable,
however, about the match between the best ﬁt models for lower fre-
quency band power and LFP is that LFP and band power are different
kinds of neural measures. LFP is a measure of extracellular voltage
ﬂuctuation over time, and band power measures are derived from LFP
through a series of non-linear transformations: LFP activity is ﬁltered
into logarithmically increasing frequency bands and the analytic
amplitude of those bands is computed and then averaged across
bands. On their own, the LFP results demonstrate that broadband LFP
contains phonemic category information that is not reducible to
Fig. 3 | Surface similarity and underlying similarity patterns are not random.
Number of signiﬁcant sites observed for each (morpho)phonological comparison
for each neural response band relative to the generated null distribution for that
band. Each null distribution (grays) contains 1000 comparisons. Vertical axes
indicate the number of sites selective for surface identity observed for each com-
parison, while horizontal axes indicate the number of sites selective for underlying
identity observed for each comparison. The proportion of the null distribution that
contains at least as many surface and underlying sites as were observed for each
comparison is indicated in the top right corner of each plot. Values for the tap
comparison are blue; values for the past tense comparison are red; and values for
the plural comparison are green. Dashed gold lines delimit the boundary contain-
ing 95% of the null distribution. Additional detail for each of the three comparisons
is given in Supplementary Figs. 4–7.
Fig. 4 | LME approach models neural activity as a combination of spectro-
graphic and phonemic label features.For each stimulus waveform, spectrograms
are computed and time-aligned phonemic-level transcriptions are assigned. Tran-
scriptions are additionally one-hot encoded (top row). Three classes of model are
created from these features: a purely spectrographic model (left column), a purely
phonemic label model (right column), and a model containing both feature sets
(middle column). For each band of neural activity, mixed effects models are ﬁt.
Model weights are used to reconstruct a predicted response for each band, and the
correlation between the predicted and recorded neural response is calculated.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 6
speech acoustics. Combined with the results from lower frequency
band power, the LFP results further suggest that this information is
robust to the set of transformations involved in deriving band power
from LFP.
As a model selection tool, the AIC straightforwardly aids the
selection of the most probable model from a set of models. More
generally, however, the AIC facilitates model ranking, and given
the partially nested structure of the models under comparison in this
study, the relative ranking of the s1 and p1 models is worthy
of assessment. Especially where s1p1 was the best-ﬁt model, assessing
the relative ﬁt of s1 and p1 models provides insight concerning
which of the two-component feature sets of the s1p1 model con-
tributed the most to its goodness-of-ﬁt. For each subject and response
type, the model with the second lowest AIC score was >100 times as
likely as the third ranked model. As shown in Fig.5b, models containing
only phonemic label features were most likely to be the second
ranked model for lower frequency bands. However, with increasing
band frequency, the s1 model becomes more likely to provide a
better ﬁt for the data until, for gamma and high-gamma bands, it is the
best ﬁt model overall. These results provide support for the general-
ization that phonemic labels better explain power at lower fre-
quencies, while acoustic features excel at explaining power in higher
frequencies.
Phoneme identity and acoustic covariance interact
Nearly all best-ﬁt mixed effects models included spectrographic fea-
tures, highlighting the pervasive importance of acoustic information in
speech processing. However, in lower frequency bands in particular,
Fig. 5 | Phonemic information dominates lower frequency band responses to
speech. a For LFP and delta–beta bands, models that include phonemic label
information in addition to spectrographic information (s1p1, red) bestﬁt the neural
response to speech for most all participants. At higher frequencies, most partici-
pants' data are best ﬁt by models containing solely spectrographic features (s1,
orange). b Models containing phonemic label information alone (p1, yellow) are
more likely to provide a better ﬁt for neural response at lower frequencies than at
higher frequencies, where models containing spectrographic information alone (s1,
orange) are more likely to provide a betterﬁt. c Time-varying correlation between
predicted and recorded neural response for the delta power response of one
electrode, illustrating a period of sustained advantage of the p1 model (yellow) over
other models, including the s1p1 (red) model.d Time-varying correlation between
predicted and recorded neural response for the high-gamma power response of
one electrode, illustrating a period of sustained advantage of the s1 model (orange)
and s1p1 (red) models over models that do not contain unshufﬂed spectrographic
information. For (c)a n d(d), gray vertical lines indicate phoneme boundaries for
the transcript provided below the plot.e Predicted-Recorded correlations averaged
across all speech responsive electrodes for all participants. For each model, box-
plots represent n=5566 delta, n=5054 theta, n=6059 alpha, n=5997 beta, n=5869
gamma, andn=3772 high-gamma Pearson’s r measurements. White horizontal lines
indicate distribution medians, colored boxes indicate interquartile range (IQR), and
black whiskers extend a further 1.5 IQR.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 7
categorical phonemic information also played a substantial role,
explaining variability in the neural data that was not otherwise
explained by spectrographic information. This observation raises two
questions: First, which aspects of the stimulus are most important in
explaining the neural response to speech? And second, what is the
nature of the relationship between spectrographic and phonemic label
features? Maximum Noise Entropy (MNE) models provide the analy-
tical tools to address these questions because they allow one to test
speciﬁc claims about the nature of the link between the stimulus and
the neural response. Here, by comparing the ﬁt of linear models to
quadratic models, we determine the extent to which relationships
between pairs of features impact neuralﬁt, and by comparing theﬁto f
models given phonemic label information to models ﬁtw i t hs o l e l y
spectrographic information, we determine the role that phonemic
information plays relative to speech acoustics.
A ss h o w ni nF i g .6, for each channel of neural activity, MNE models
estimated numerous receptive ﬁelds, including ﬁelds that corre-
sponded with an increase in the neural response (Fig. 6b,e) and ﬁelds
that corresponded with a decrease in the neural response (Fig. 6a,d).
And when MNE models wereﬁt with phonemic label information, that
information was often visible in the estimated receptiveﬁelds, as can
be seen by comparing the top row of each receptive ﬁeld in Fig. 6a, b
with those of Fig.6d, e. From the receptiveﬁelds estimated by the MNE
models, predicted neural data was generated and compared against
the recorded neural data.
To assess whether model order a nd/or the availability of pho-
nemic label information contributed to the quality of MNE modelﬁts,
ﬁve mixed effects models were ﬁt. These models predicted the Fisher
Z-transformed Pearson correlation between predicted and observed
neural responses based on the neural response type, model order, the
availability of phonemic label information, the interaction of model
order with the availability of label information, and whether the model
feature weights were shufﬂed. Subject and channel were included as
random effects. The formulas for these models are given in Supple-
mentary Table 1, and Fig. 7 shows examples and summaries of the
correlation data that these models ﬁt. In these models, model is a
binary feature referring to whether the predicted ﬁt was generated
using only the linear MNE feature or predicted using both the linear
and quadratic features; the featurelabel indicates whether or not the
MNE model wasﬁt using labeled or unlabeled spectrographic features;
and the feature shufﬂe indicates whether or not the predictedﬁtw a s
generated using MNE features whose weights had been shufﬂed. The
model containing only theshufﬂe parameter as aﬁxed effect was used
as a baseline.
Model selection was determined using the AIC. Of theﬁ
ve models,
the model containing model, label,a n dmodel:labelfeatures best
ﬁt the data, having an AIC score 54.75 units lower than the next best
model and carrying 100% of the cumulative model weight. The next-
best ﬁt model included label and shufﬂe features and had an AIC
score 1.60 units less than the model that additionally included the
model feature. The baseline model containing only theshufﬂe feature
outperformed a model that was minimally augmented by the addition
of the model feature, garnering an AIC score of 1.59 units lower than
the model containing both model and shufﬂe features. Together,
these results suggest that while MNE model complexity alone does not
positively impact prediction quality, its interaction with the label sta-
tus of the spectrograms used to ﬁt the MNE models is substantial. In
other words, when phonemic label information is available, informa-
tion in the stimulus covariance can be used to more accurately predict
neural response. Without phonemic label information, the stimulus
covariance does not contribute substantially to model goodness-of-ﬁt.
The failure of the model feature to contribute independently to
goodness-of-ﬁt was not predicted. Ceteris paribus, the higher dimen-
sionality of the quadratic model is expected to recover a higher pro-
portion of the variability in the neural response than the linear model,
as has been demonstrated by Kozlov and Gentner
22. However, whereas
Kozlov and Gentner22 recorded from songbird auditory areas only, the
data in this study were recorded from speech-responsive electrodes,
the majority of which were not localized to auditory areas. Given that
the receptive ﬁelds in this study were estimated based on primarily
spectrographic input features, it may be the case that the higher
dimensionality of the quadratic model does not confer a bene ﬁti n
non-auditory areas where spectrographic information contributes less
to neural response. Nevertheless, the fact that the interaction feature
(model:label) does substantially improve model goodness-of- ﬁt
suggests that information about spectrographic covariance is useful
for predicting neural response when it is reinforced by categorical
phonemic label information. In this sense, the auditory stimulus cov-
ariance structure and phonemic identity synergistically impact neural
response, jointly providing information available in neither feature set
independently.
Phonemic explanatory power requires language knowledge
Both LME and MNE models of the neural response to speech indicated
that categorical phonemic information contributes to the prediction
of the neural response to natural speech. Next, we asked whether the
utility of phonemic label information in these models requires speciﬁc
language knowledge. That is, it could be the case that phonemic label
information plays a signiﬁcant role in these models simply because it
reinforces acoustic information. If this were the case, we would expect
the addition of phonemic label information to improve modelﬁt both
when participants were listening to a language they understand and
are familiar with (i.e., English) and when listening to a language they do
not understand and are unfamiliar with (i.e., Catalan). Alternatively,
phonemic label information could play a signi ﬁcant role in these
models because it provides language-speci ﬁc category membership
information that is not otherwise available in the speech acoustics. If
this were the case, phonemic label information should only contribute
signiﬁcantly towards explaining neural activity while participants are
listening to speech in a language that they are familiar with (English)
and not while listening to speech in a language they are unfamiliar with
and do not understand (Catalan).
To assess whether this was the case, families of mixed effects
models were ﬁt on the predicted-recorded correlation values for the
predictions of each of the seven LME models and each of the four MNE
models.
For the LME models, each model for assessing the role of speciﬁc
language knowledge predicted the Fisher Z-transformed Pearson
correlation between predicted and observed neural responses to
particular excerpts on the basis of the LME model type (model: s1p1, s1,
p1, etc.) and the band of neural activity. A second model had an
additional feature (lang)f o rt h el a n g u a g eb e i n gs p o k e ni nt h ee x c e r p t
(English or Catalan), and a third model additionally included an
interaction term for excerpt language and model type (lang:model).
For each of these three models, subject and channel were included as
random effects. The formulas for the three models in this family are
g i v e ni nS u p p l e m e n t a r yT a b l e2 .
Model selection was then determined using the AIC. Of the three
models, the model containing bothlang and lang:modelfeatures in
addition to model and band features best ﬁt the data, having an AIC
score 609.59 units lower than the next best model and carrying 100%
of the cumulative model weight. The next-bestﬁt model included only
lang, model,a n dband features and had an AIC score 65,120.24 units
less than the model th at included only the model and band features.
These results indicate not only that the strength of correlation
between the predicted and recorded responses varies based on the
language that the participant is listening to, but also that difference in
predicted-recorded correlation between English and Catalan excerpts
also varies with model type. This is shown most clearly in Fig. 8a: the
average predicted-recorded correlation for models containing
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 8
Fig. 6 | Reconstructed receptive ﬁelds reﬂect available phonemic and spec-
trographic information. aReceptiveﬁelds corresponding to the six most negative
eigenvalues for a single electrode whose delta power response was ﬁt with purely
spectrographic information.b Receptiveﬁelds of the six most positive eigenvalues
for the same electrode as (a). c Left: Eigenvalues of the ﬁt model, ordered by their
value. Gray shaded box encompasses the bottom 95% of eigenvalue magnitudes.
Right: The power-dependent average receptiveﬁeld. d Receptive ﬁelds for the six
most negative eigenvalues reconstructed from the delta power response of the
same electrode shown in (a) using a model that was ﬁt with both spectrographic
and phonemic label information.e Receptive ﬁelds of the six most positive
eigenvalues for the same electrode as (d). f Left: Eigenvalues of the ﬁtm o d e l ,
ordered by their value. Gray shaded box encompasses the bottom 95% of eigen-
value magnitudes. Right: The power-dependent average receptiveﬁeld.
Fig. 7 | Combined with phonemic label information, stimulus covariance
structure best predicts the neural response to speech across all
response bands.Time-varying variance explained by the MNE models for the delta
(a) and high-gamma (b) power responses of single electrodes, illustrating periods
of sustained advantage of the labeled quadratic model (blue) over other models.
Gray vertical lines indicate phoneme boundaries for the transcripts provided
below each plot. c Average variance explained by the MNE models for all subjects,
broken out by model type and neural response band (n=1255 electrodes per box-
plot). d Average variance explained by the MNE models for all trueﬁt models vs. all
shufﬂed models (n=30,120 electrodes per boxplot). In (c)a n d(d), white horizontal
lines indicate distribution medians, colored boxes show the IQR, and black whis-
kers extend a further 1.5 IQR.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 9
spectrographic features (s1p1 and s1) is higher for Catalan excerpts
than for English excerpts. However, for the model containing only
phonemic label features (p1), the average predicted-recorded corre-
lation is higher for English excerpts than for Catalan excerpts. Speciﬁc
language knowledge is required for phonemic label information to
substantially predict neural response to speech.
Similarly, to assess the role of speciﬁc language knowledge on the
ﬁt of the MNE models, a family of models was ﬁt. These models pre-
dicted the Fisher Z-transformed Pearson correlation between pre-
dicted and observed neural responses on the basis of model order
(linear or quadratic), the availability of phonemic label information
(yes or no), excerpt language (English or Catalan), and combinations of
their interactions. Subject and channel were included as random
effects. The model that included band, model, label,a n d mod-
el:label features as ﬁxed effects was treated as the baseline model.
The formulas for the six models in this family are given in Supple-
mentary Table 3.
As before, model selection was determined using the AIC. Of the
six models, the model containing the simplex featuresmodel, label,
lang and all their interactions best ﬁt the data, having an AIC score
775.87 units lower than the next best model and carrying 100% of the
cumulative model weight. Among the models with lower ﬁt, those
including a feature for the interaction between excerpt language and
label status (lang:label) better ﬁt the data than models without this
feature, and all models including the excerpt language feature (lang)
better ﬁt the data than the baseline model. These results indicate that
participants’ knowledge of the language they are listening to sig-
niﬁcantly impacts model ﬁt and does so in a way that interacts pri-
marily with the availability of categorical phonemic information. As
shown in Fig. 8b, the average predicted-recorded correlation for
quadratic models is higher for Catalan excerpts than for English
excerpts when the MNE model ’s input features are purely spectro-
graphic, whereas for MNE models that include phonemic label infor-
mation in addition to spectrographic information, the average
predicted-recorded correlation is higher for English excerpts. In this
way, the availability of phonemic information does not bene ﬁtM N E
model ﬁt for neural activity recorded while participants are listening to
an unfamiliar language that they cannot understand. Categorical
speech sound information requires speci ﬁc language knowledge in
order to account for neural activity.
Discussion
In this study more sites sensitive to phonemic identity were observed
than would be predicted by chance. While simple in its articulation,
this result has far-reaching consequences for phonological theory and
theories of language representation in the brain.
These ﬁndings support a reallocation of probability mass away
from a number of common ideas about the nature of phonology and
phonological processing. For example, implicit in many theories of
speech production and processing is the assumption that language-
speciﬁc grammar only occurs at the level of syntax. Phonological
knowledge, including knowledge of language-speciﬁc phonotactics, is
cast as epiphenomenal of lexical knowledge: speech perception is
more or less a word recognition problem, and speech production
proceeds in a universal and deterministic manner from articulo-
acoustic content speciﬁed in the lexicon. This study provides evidence
that these common assumptions are inaccurate. Language-speci ﬁc
phonological grammar guides the neural response to speech, and it
does so at a level of granularity commensurate with the phoneme.
To see how this conclusion follows from the observed data, con-
sider what one would predict if phonemes were not a relevant unit of
organization for language in the brain. To maintain true skepticism
about the cognitive reality of phonemes, one would need to envision a
state of affairs in which underlying representations of speech sounds
were altogether unnecessary. That is, at no point in speech processing
would a listener assign the value /d/ to some taps and /t/ to others.
However, if this were the case and taps were not differentiated in
underlying representations, it would be unexpected to observe any
phonological underlying sites given the comparisons used in this
paper. Instead, one would expect to observe acoustic surface
sites only.
We argue that the most parsimonious explanation for the obser-
vation of phonological underlying sites is language speciﬁcp h o n o l o -
gical knowledge of the kind generally assumed by working
phonologists. More precisely, the existence of phonemic underlying
sites suggests that the representations of speech sounds and words are
not merely amalgamations of pronunciations that a listener has
encountered before. Rather, there is a degree of abstraction between
surface, acoustic forms and the prelexical forms that speech sounds
are mapped onto in the brain. The nature of this abstraction is lan-
guage speciﬁc, reﬂecting not only differences in the phonemic inven-
tories of different languages, but also the language speci ﬁc,
contextually-sensitive sound alternations that comprise a speci ﬁc
language’s phonological grammar.
The surrounding phonological context is essential to this
abstraction. For example, as prefaced in the Introduction, when either
/d/ or /t/ occurs following a stressed syllable and between two vowels,
their acoustic contrast is neutralized, and both are pronounced as a
coronal tap. The context of the /d/ or /t/ is critical to this alternation.
Without a preceding stressed vowel and following unstressed vowel,
this alternation does not take place. In this way, the surrounding
phonological environment provides cues to the underlying
Fig. 8 | Phonemic labels improve model ﬁts for English but not Catalan data.
a Average correlation between the response predicted by each of the LME models
and the actual recorded response;n=32,317 for each English boxplot, andn=12,286
for each Catalan boxplot.b Average correlation between the response predicted by
each of the MNE models and the actual recorded response;n=7530 electrodes per
boxplot. In both (a)a n d(b), white horizontal lines indicate distribution medians,
colored boxes show the IQR, and black whiskers extend a further 1.5 IQR.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 10
phonological identity of sounds. Although in the case of coronal stop
neutralization, the cues may or may not uniquely disambiguate the
phonemic identity of the /d/ or /t/ (see Supplementary Fig. 1), in gen-
eral, phonological abstraction requires that a listener be able to treat
the same acoustic information (e.g., a tap) differently based on its
surrounding phonological context. We argue that this very process
constitutes phoneme identity extraction. For this reason, the point of
the baselining in Section 2 was to ensure that what is observed in the
time window of interest is not merely the sum of what came before it.
While surrounding context undoubtedly plays a role in phoneme
identity extraction, one of the key things that this paper shows is that
some responses to acoustically similar sounds (i.e., various taps)
diverge in a way that is consistent with the extraction of phonemic
information and not with pure acoustics.
Dresher
29 lays out three ways that phonologists have con-
ceptualized of the phoneme as an object of inquiry. One class of
deﬁnitions characterizes the phoneme as a physical reality. Repre-
sentative deﬁnitions of this genre describe the phoneme as a language-
speciﬁc “family” of sounds that “count for practical purposes as if
they were one and the same ”30 (via Dresher 29), perhaps because
“the speaker has been trained to make sound-producing movements
in such a way that the phoneme features will be present in the
sound waves, and [the speaker] has been trained to respond only
to these features ”
31. The second class of de ﬁnitions views the
phoneme as a psychological concept. This class of explanation is often
presented as an alternative to the physical reality of the phoneme: if a
physical constant coextensive with the phoneme does not exist, then
perhaps a mental constant does instead. Finally, if both the physical
and psychological reality of the phoneme are rejected, then Dresher,
29
echoing Twaddell,32 concludes that the phoneme is a convenient the-
oretical ﬁction, without material basis in the mind, mouth, or
middle ear.
This study addresses the second of these three positions, inves-
tigating whether the commonly held understanding of the phoneme as
a unit of language-speciﬁc contrast has psychological reality or merely
theoretical utility. In demonstrating the existence of sites sensitive to
phonemic contrast in the absence of acoustic distinction, this study
provides support for the classical understanding of the phoneme as a
psychological entity and a core level of sublexical linguistic processing.
At the same time, it suggests that some theoretical implementations of
the phoneme as a unit characterized by minimal (as opposed to
exhaustively-speciﬁed) sets of distinctive features may have more
theoretical utility than psychological reality (see Supplementary
Fig. 8). To the extent that linguistic and psychological theories of
phonology intend to account for the same sets of behavioral phe-
nomena, these results nevertheless support the continued use of
phonemic units in phonological theory and reify the existence of
language-speciﬁc sublexical structures in language processing.
The morphological results of this study also engage with foun-
dational principles of sublexical language processing. In observing
more surface and morphological underlying sites than would other-
wise be expected by chance for both the plural and past tense com-
parisons, this study provides evidence for two interrelated processes
in the neural basis of morphology.
It is generally accepted that morphological decomposition takes
place during the processing of regularly inﬂected forms in English and
related languages
33–36;cf.37. The presence of morphological underlying
sites in this study is generally consistent with these results. However,
the paradigms typically employed to assess the compositionality of
morphological units within words arguably gauge fairly abstract
proxies for morphological structure. Many rely on priming and assess
compositionality through metrics such as reaction time or expectation
violation response. The evidence for morphological abstraction pre-
sented here has the advantage being gathered during a naturalistic
listening task and straightforwardly comparing the difference in neural
response to sounds that bear morphological exponence to those that
do not carry any morphological meaning.
From this perspective, the difference in response between non-
plural word-ﬁnal [z] and plural [s] or [z] can be attributed straightfor-
wardly to the morphological exponence of [s] or [z], without appeal to
intermediary cognitive phenomena such as priming or expectation.
That is, the meaning of ‘plural’ associated with the sounds [s] and [z]
drives the response of the morphological underlying sites for the
plural comparison, and likewise, the meaning of‘past’ associated with
[t] and [d] drives the response of the morphological underlying sites
for the past tense comparison. This, in general, is a great strength of
the paradigm employed in this study. However, these results them-
selves do not provide explicit evidence that the structure of regular
plural and past tense forms is compositional, since it could be the case
that, for instance, plural [s] and [z] pattern together at morphological
sites through an analogical process. In such a case, plural [s] and plural
[z] would still evoke similar neural responses because they index a
common morphological exponent, but that commonality would be
mediated through an analogical process via the lexicon rather than a
compositional, syntax-like process within the word itself. Moreover,
t h i ss t u d yd o e sn o ta d d r e s sw h e t her the underlying sites that we
observe for the plural and past tense are sensitive only to the regular
plural and past tense (i.e. exponent speciﬁc) or to “plural-ness” more
generally. Determining this would require a follow-up study that
includes irregular forms. Nevertheless, the results of this study provide
evidence of an early neural response to the presence of particular
morphological exponents.
Furthermore, these results support the idea that morphological
identity is abstracted over phonologically distinct alternants in a
structured, language-speciﬁc manner. As was argued for the phonemic
sites identiﬁed by the tap comparison, the structured relationships
between speech sounds and their phonological contexts form a
language-speciﬁc grammar of sounds. Given their interface with
meaning, morphophonological alternations in particular have been of
central importance to the development of phonological theory (see
Kenstowicz and Kisseberth
14) and are often appealed to in classic texts
as foundational evidence for the existence of the phoneme, since it is
through the ways that sounds either change or fail to change the
meanings of words that phonemic contrast is most strikingly estab-
lished. In this way, the existence of morphological underlying sites
identiﬁed by the plural and past tense comparisons demonstrates both
that morphological identity is abstracted over distinct, phonologically
conditioned alternants and that morphological exponence transcends
phonemic particularities.
Language has numerous levels of analysis that interact in a variety
of structured ways. This paper has focused on the dissociation of
phonetic, phonological, and morphological levels of analysis through
the lens of acoustic features, phonemic labels, and morphological
exponents. However, more abstract levels of structure are also at play
during natural speech listening, including lexical knowledge, multi-
word semantic and syntactic structure, and discourse, as well as more
general awareness of language ’s statistical structure. Given that all
these levels of structure are present in speech simultaneously, it is
reasonable to wonder how conﬁdent we can be that what appear to be
phoneme-sensitive responses are really phoneme responses and not
lexical, semantic, or some other kind of response.
Conﬁdence that the reported results reﬂect phonological and not
lexical or semantic information comes from the analysis design. In
particular, LME and MNE models show that phonemic label informa-
tion accounts for variance in the neural response that is not accounted
for by the acoustic feature set. That is, these analytical approaches do
not show evidence of a phonemic response per se; rather, they show
that phonemic label features explain aspects of the neural response
not otherwise explained by acoustic features. Thus, to be con ﬁdent
that these results are properly phonological and not lexical or
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 11
semantic, one need only be conﬁdent that the phonemic label features
and models do not implicitly have access to lexical or semantic infor-
mation. Addressing the ﬁrst of these concerns, phonemic labels are
generally free of meaning (see the arbitrariness of the sign
38). Addres-
sing the second, LME and MNE models do not use sufﬁcient sequential
information to approximate wordlike information. Together, these
facts provide conﬁdence that the reported results re ﬂect sublexical,
phonological structure and not lexical or supralexical structure.
Determining the nature and origin of the neural processes that
support language processing is crucial for building a mechanistic
understanding of linguistic cognition. In this study, band-limited
power was examined for six frequency ranges. However, the inter-
pretation of this measure, including its relation to other neural mea-
sures and its cellular origins, varies depending upon where in the brain
it is recorded.
In intracranial recordings, LFP recorded from gray matter is
credited primarily to local synaptically-induced current ﬂow. On the
other hand, LFP recorded from white matter is understood to originate
from a combination of cortical activity spread by volume conduction
into adjacent white matter as well as currentﬂows through the voltage-
gated channels that mediate the travel of action potentials along
axons
39. Thus, while the dominant components of electrical activity
recorded in gray matter result from the activity of a spatially restricted
set of cells proximal to the electrode contact, activity recorded from
white matter additionally contains signal that originates from a com-
bination of cells, possibly separated by great distance, that happen to
project axonal processes within proximity of the electrode contact.
Additionally, the volume conduction properties of white and gray
matter differ. Whereas LFP in gray matter (passively) propagates more-
or-less equally in all directions—that is, both parallel and perpendicular
to the cortical surface —propagation in white matter is directionally
biased by the higher density of axonal myelin, such that passive spread
occurs more readily along myelin sheaths rather than across them
40,41.
These key differences in the properties of gray and white matter
impact the functional interpretation of electrophysiological measures
collected from these tissues.
Thus, while activity recorded from white matter is certainly phy-
siologically valid, its interpretation differs from activity recorded in
cortical tissue. At present, the electrophysiological properties of white
matter are relatively under-explored, and consequently, activity
recorded in white matter is considered difﬁcult to interpret and likely
under-reported when it is recorded. Accordingly, while this paper does
not speculate on how signiﬁcant sitesﬁt into larger research narratives
about the language network, it nevertheless reports results that are
primarily driven by activity recorded in white matter. In doing so, this
paper contributes to an early understanding of what language-related
electrophysiological activity looks like when recorded from these sites.
Relatedly, it is a priori unclear whether the time course of
language-related activity recorded in white matter ought to follow the
same time course as activity recorded from the scalp or gray matter.
Some work suggests that the acoustic processing of phonetic detail
takes place within 100 –200ms following the onset of a speech
sound
42,43, activity related to speech sound categorization roughly
300–500ms after the sound’so n s e t43, and morphological processing
occurs even later44. However, other work suggests a messier temporal
story, where both categorical and gradient speech sound information
are represented simultaneously in the neural signal
45,46,a l o n gw i t h
morphological information46,47. To the extent that it is possible to
compare results observed in EEG, MEG, and ECoG data to those
observed in SEEG contacts embedded in white matter, the results of
this study appear to support the messier story, as shown in Supple-
mentary Figs. 9, 10.
For the coronal tap comparison in particular, the majority of sites
that show an acoustic pattern occur in the gamma power and high-
gamma power bands. In these bands, the time windows where
signiﬁcant acoustic responses occurred correlate highly with the win-
dows where signi ﬁcant phonemic responses also occurred (Supple-
mentary Fig. 9). These results suggest that both phonemic category
and acoustic detail are processed simultaneously and overwhelmingly
separately, since relatively few sites across comparisons exhibited
both acoustic and phonemic patterns or surface and morphological
patterns (Supplementary Figs. 3, 10).
In ﬁtting mixed effects models containing acoustic features and
phonemic label features across the ﬁve classic oscillatory frequency
bands, the analyses described in Section 2 provide a basic intracranial
validation of results found in scalp EEG work by Di Liberto et al.
17.D i
Liberto et al.17 ﬁt multivariate temporal response functions (mTRFs) to
bandpassed scalp EEG data using spectrographic features, phonemic
label features, and both spectrographic and phonemic label features.
As in this study, they found that models containing both spectro-
graphic and phonemic label features provided the best ﬁtm o d e lf o r
delta and theta bands. Furthermore, in these lower frequency bands,
their phonemic label model outperformed their spectrographic
model. Conversely, in higher bands (alpha, beta, gamma) the model
containing only spectrographic features outperformed the model
containing only phonemic label features. Validation of these basic
results from Di Liberto et al.
17 thus provides useful validation of the
dataset used in this study, in light of the novelty of other analyses
described in Section 2.
However, the LME analyses in Section 2 also build upon the ﬁnd-
ings of Di Liberto et al.
17. In using the AIC to inform model selection,
this study accounts for differences in model ﬁt which in Di Liberto
et al.17 could be attributed to differences in numbers of model para-
meters. This analytical choice provides greater con ﬁdence that the
observed best-ﬁt models ﬁt best due to the substance of their features
rather than their dimensionality. Additionally, in an alternative to the
LME analysis presented in Section 2, the spectrographic features used
to ﬁt LME models were drawn from the latent space of a variational
autoencoder, as described in Supplementary Fig. 11. In this sense, like
the phonemic label features, the spectrographic features in these
models were also abstracted from surface acoustics. However,
whereas the phonemic label features represent a linguistically
informed compression of the acoustic signal, the compressed spec-
trographic features are purely informed by acoustic information. It is
remarkable then, with all their compression, that the weightings of
these feature sets are still capable of reconstructing neural response
with such high ﬁdelity, with a correlation of over 0.4 at times. In this
way, the ability of these features to account for a signiﬁcant portion of
neural variance validates the use of such nonlinear compression
methods for neural encoding analyses.
Moreover, in addition to validating Di Liberto et al. ’s
17 main
results, this study validated one of the ﬁner details of their results. In
particular, Di Liberto et al.17 found that the overall correlation between
predicted and recorded responses was strongest in the lowest fre-
quency bands and dropped to a fraction of that magnitude as center
band frequency increased. This effect can be seen clearly in Fig.5ea n d
to a lesser extent for the MNE models in Fig. 7c. Di Liberto et al.
17
attributed this steep dropoff in the predictive ability of their models to
the lower signal-to-noise ratio of these bands when recorded from the
scalp. Observing this effect in intracranial recordings is not necessarily
inconsistent with Di Liberto et al.’s
17 interpretation, but the sources of
noise may be different. For example, it may be the case that higher
frequency signals have lower ﬁdelity in white matter sites due to the
distance of these sites from signal generators.
The variability in the best- ﬁt LME model across participants for
gamma power and high-gamma power data is not easily explainable.
Properties of the higher bands themselves may be in part responsible
for this variability. Because higher frequencies attenuate more quickly
over distance than lower frequencies, high-frequency components of
the signal at each electrode reﬂect more local responses while lower-
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 12
frequency components are integrated over larger anatomical space.
Thus, all else being equal, heterogeneity across sites whether within or
between participants may more easily impact LME ﬁts in higher fre-
quency bands than in lower frequency bands, since the latter are likely
capturing a more global (i.e., shared) response. This may contribute to
the fact that there is more participant variability for higher bands than
for lower bands.
Variability within particular bands may result from differential
electrode coverage across participants. The fact that both SD018 ’s
gamma power and high-gamma power were bestﬁt by the s1p1 model
would be consistent with such an explanation, since electrode cover-
age is a factor that isﬁx e df o re a c hp a r t i c i p a n t ,a n dw em i g h tt h e r e f o r e
expect coverage-based differences to be consistent within partici-
pants. However, the fact that only SD013 ’sg a m m ap o w e ra n do n l y
SD011’s high-gamma power are best ﬁt by the s1p1 model reveals the
true complexity of a coverage-based explanation for the variability in
these results. For the best ﬁtm o d e lf o rS D 0 1 3’s gamma power to
diverge from that of all other participants for only that power band
would require coverage that differs from other participants’ in such a
way that it differentially impacts gamma power only. Similarly, the fact
that the best ﬁt models for SD018 differ from the majority in only two
bands requires one to posit a state of affairs in which SD018’s coverage
differs in a way that substantially impacts only two bands.
Individual variation presents another possible explanation.
Whereas a coverage-based explanation assumes that results across
participants ought to be the same and only differ because non-
homologous sets of neurons were recorded across participants, an
explanation based on individual variation would allow for the possi-
bility that even with functionally identical coverage, individuals may
still vary in the way that they process speech sounds. From this per-
spective, the consistency across participants in lower bands is merely
artifactual of the small number of participants whose data are reported
here, and perhaps if data from a greater numbers of individuals were
available, some variability in the best-ﬁt model would be observed in
each band. However, while individual variability most certainly exists
in speech sound processing, it seems unlikely that information about
speech sound categories and their acoustics, being both quite close to
the sensory periphery and fundamental to speech perception, would
vary substantially across individuals. This is an empirical question,
though, and while its answer ought to be pursued, it is not a question
that this dataset is well-suited to address. Given the limitations of the
dataset, arriving at a satisfactory account for the cross-participant
variability of these results will require follow-up work.
Finding that phonemic label features did not improve model ﬁts
for Catalan speech provides further support for the claim that pho-
nemic label features do not simply reinforce information available in
speech acoustics. Rather, phonemic label features account for neural
activity that requires speciﬁc language knowledge.
The poor performance of phonemic label features for Catalan
speech is expected despite the overall similarity in sound inventories
between Catalan and English. This is because patterns of alternations
in Catalan differ from those in English, such that listeners unfamiliar
with Catalan phonology cannot be expected to extract accurate Cat-
alan categories without knowledge of the patterns. For example,
English speakers may interpret Catalan alveolar taps as either /d/ or /t/,
due to the English coronal neutralization pattern discussed in Section
2; however, Catalan has no such pattern, and its taps are phonologi-
cally related to neither /d/ nor /t/. For this reason, Catalan phonemic
labels were correctly predicted to poorly explain the neural response
to speech for English listeners listening to Catalan.
However, it was unexpected that the success of the acoustic
features explaining the neural response to Catalan speech exceeded
that of English speech. Two interrelated factors could explain
this unexpected result. First, participants were asked to listen carefully
for a recognizable word in the Catalan speech, but were not directed
to listen for any particular word in the English speech. For this
reason, increased attention to the speech stream could account for
the overall higher performance of the acoustic feature sets in
explaining the neural response to Catalan speech. Relatedly, as an
unfamiliar language, the faithful tracking of speech acoustics may
occupy more of the neural response to Catalan speech than to English,
a language for which all participants have much more robust pre-
dictive models.
MNE models model the relationship between the stimulus and
neural response as a linear combination of the contributions of sti-
mulus feature sets with varying cardinalities. That is, aﬁrst-order MNE
model models neural response as the contributions of individual sti-
mulus features; a second-order model sums single feature contribu-
tions with the contributions made by pairs of stimulus features; a third-
order model further includes the contributions of triplets of stimulus
features; and so on.
This study speciﬁcally compares theﬁts of ﬁrst- and second-order
models. In doing so, it assesses the extent to which relationships
between stimulus features contribute to model goodness-of- ﬁt
beyond the contributions of individual features themselves. In ﬁnd-
ing that second-order, quadratic models account for signiﬁcantly more
of the variance in neural response only when phonemic label infor-
mation is available, this study shows that categorical phonemic infor-
mation bootstraps acoustic information in explaining the neural
response to speech. More precisely, without the availability of pairwise
information about the stimulus, phonemic label information does not
contribute signiﬁcantly to predicting neural response.
This result provides structure to long-held understandings of the
important role that relative spectrotemporal features play in speech
sound identiﬁcation. For example, at single time points, measures of
F1:F2 ratio or spectral tilt provide key information for discriminating
among vowels or among fricatives, respectively, and comparing mea-
sures across time provides further discriminatory ability. Features of
spectrographic stimulus covariance have also been implicated in
speaker normalization
48. In these ways, the sensory signal itself pro-
vides an exceptional degree of structure that mirrors inﬁne scale what
linguistic categories demonstrate at a coarser scale. That is, speech
sounds are built from relationships between acoustic features; pho-
nemes from relationships between speech sounds; morphemes from
relationships between phonemes ; meaning from relationships
between morphemes, and so on.
This study provides evidence that relative power between pairs of
time-frequency bins supports the neural response to speech when
phonemic category information is also available. Linking features of
the sensory signal to linguistic categories in this way provides struc-
ture for an early link between sensory and linguistic cognition.
Methods
Participants
Study participants were ten patients at UC San Diego Health who
underwent intracranial stereo EEG and subdural electrode implanta-
tion as part of treatment for refractory epilepsy or related conditions.
All were native English speakers, who had no prior experience with
Catalan, and all reported normal hearing and performed within the
acceptable range on a battery of neuropsychological language tests.
The research protocol was approved by the UC San Diego Institutional
Review Board, and all subjects gave written informed consent prior to
surgery. Basic patient information is summarized in Table2.
Participant gender
Four of the ten participants were women, and six were men. Participant
gender information was assigned impressionistically by researchers
and recorded only for demographic purposes. Gender was not con-
sidered during study design and did not factor in participant
recruitment.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 13
English Stimuli
Participants passively listened to short excerpts of conversational
American English speech taken from the Buckeye Corpus49.T oa s s e s s
participant attention to the task, participants responded orally to a
two-alternative question about the content of each English passage
after they listened to it.
Passages were 25-76s long (mean 38s) taken from 27 (12 women;
15 men) native speakers of Midwestern American English living in
Columbus, OH between October 1999 and May 2000. Per corpus
documentation by Pitt et al.,
49 excerpts were recorded mono-
phonically on a head-mounted microphone (Crown CM-311A) and fed
to a DAT recorder (Tascam DA-30 MKII) at a 48kHz sampling rate
through an ampliﬁer (Yamaha MV 802). Following each excerpt, par-
ticipants heard a two-alternative choice question regarding the con-
tent of the passage they heard, and they were asked to respond orally
to the question to ensure that they were alert and paying attention to
the passages that they heard. These questions were recorded with a
Blue Yeti USB microphone sampling at a rate of 48kHz by a speaker of
American English. The amplitude of all English passages and questions
was normalized to -20dBFS prior to padding with 500ms of silence.
Transcription, segmentation, and labeling were performed for all
acoustic stimuli. Both orthographic and phonetic transcriptions were
created to provide human-readable text of the speech stimuli. Seg-
mentation created time codes for boundaries between units, and
labeling created labels for the spans between boundaries. All stimuli
were segmented and labeled for word, part of speech, and phone
identity. In this way, labels for words, parts of speech, and phones were
time-aligned to the acoustic stimuli. Transcription, segmentation, and
labeling procedures for passages from the Buckeye Corpus are
described in Pitt et al.,
49 and transcription, segmentation, and labeling
of task instructions and content questions was performed by a
phonetically-trained researcher at UC San Diego, using the protocols
detailed in Pitt et al.
49.
Catalan stimuli
Interspersed with the passages from the Buckeye Corpus were short
passages of conversational Catalan taken from the Corpus del Catalá
Contemporani de la Universitat de Barcelona
50. To assess participant
attention to the task, participants were instructed to listen for English
words embedded in the recording and press the space bar when they
heard an English word.
Catalan passages were 44-55s long (mean 49s) taken from 2 (1
woman; 1 man) native speakers of Catalan —one woman from Bena-
barre, Huesca and one man from Tamarit, Catalonia. Three passages
were excerpted from each speaker for a total of six Catalan excerpts,
and Catalan excerpts were interspersed into the passive listening task
such that one Catalan excerpt was included in each block of the task.
Since patients are not expected to understand Catalan speech, two-
alternative questions about the content of the Catalan passages were
not suitable to assess participant attention. Instead, English nouns
were digitally spliced into the Catalan excerpts, and participants were
asked to press the space bar when they heard an English word. For each
Catalan passage, three English nouns were excised from the Buckeye
corpus digitally spliced into the Catalan recording. These English
nouns were taken from one female speaker and one male speaker from
portions of the Buckeye Corpus not otherwise heard in the passive
listening task. Nouns were excised from their original contexts and
inserted into the Catalan speech at zero crossings to minimize acoustic
artifacts. Inserted nouns were gender-matched with their Catalan
carrier passages, but no further controls were taken to match for voice
similarity. Prior to insertion into Catalan speech, the English nouns
were normalized to -20dBFS, and after insertion into Catalan speech,
the entire mixed-language passage was normalized to -20dBFS. This
process of amplitude normalization resulted in English nouns which
were clearly audible and segregable from the Catalan speech stream.
Nouns were inserted into the Catalan speech during natural pauses at
roughly equal but not regularly spaced intervals to increase uncer-
tainty and encourage attention to the unintelligible speech stream.
Catalan stimuli were orthographically and phonetically tran-
scribed, segmented, and labeled. Phonetic and orthographic tran-
scriptions for Catalan passages were archived alongside audio
recordings in the Dipósit Digital de la Universitat de Barcelona (http://
diposit.ub.edu/dspace/handle/ 2445/10413), and the passages used in
this study were subsequently segmented and labeled in Praat
51 by a
phonetically-trained researcher at UC San Diego using the phonetic
transcriptions provided with the corpus. Given the similarity in the
phonetic inventories of Catalan and English, the segmentation criteria
used for the Buckeye corpus (reported in Pitt et al.
49) were also used to
segment the Catalan passages used in this study.
Data acquisition and processing
Experimental instructions and stimuli were presented to participants
in their hospital rooms on a Windows 10 desktop PC (Dell XPS 8910)
using PsychoPy for Python 2.7
52,53.T h et a s kw a sc o n d u c t e di ns i x
blocks, each of which contained eight English trials and one Catalan
trial. The average block duration was 6 minutes 30 seconds. All parti-
cipants completed at least two of the six blocks, and the average
participant completed four blocks, listening to 26:45 min of speech
totaling 15,070 phones. Each trial consisted of a short, spoken passage
followed by a content question and an oral response.
Intracranial EEG signals were ampli ﬁed using a multi-channel
ampliﬁer system (Natus Quantum) and recorded using Natus Neuro-
Works software. Auditory stimuli and oral responses were recorded
simultaneously with the EEG data by feeding the output of a Zoom H2n
microphone as an additional input channel to the Natus Quantum
ampliﬁer.
After recording, neural data were deidentiﬁe da n de x p o r t e df r o m
the clinical NeuroWorks system in .edf (European Data Format) format
Table 2 | Summary of basic patient information
Patient Age Gender Hand. Wada Coverage Language Experience
SD010 20s M R − sEEG: LH,RH English
SD011 30s M R LH sEEG: LH,RH English, Creole, French
SD012 20s F R LH sEEG: LH,RH; Grid,strips: LH English
SD013 40s M L LH* sEEG: LH,RH English, Spanish
SD015 50s F − sEEG: LH,RH English
SD017 20s M R − sEEG: RH English, Spanish
SD018 40s F L RH sEEG: LH,RH English, Spanish
SD019 20s M R − sEEG: LH,RH English
SD021 30s F R − sEEG: LH,RH English
SD022 20s M R − sEEG,Grid: RH English
*While patient SD013 did not experience a clear, prolonged speech arrest with either injection, he demonstrated greater language deﬁcits following left hemisphere injection.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 14
for pre-processing using the Python package MNE Python54.C h a n n e l s
displaying excessive artifacts or line noise were removed (45 channels
total). Remaining channels were common average referenced, notch
ﬁltered at 60Hz and its harmonics, bandpass ﬁltered 0.1-170Hz, and
downsampled to three times the lowpass cutoff (510Hz). Independent
Component Analysis (ICA) was used to remove stationary artifacts
from the ﬁltered data, and time intervals containing remaining arti-
facts were visually identi ﬁed and discarded. Channels selected for
analysis were those which exhibited reliable evoked response to
speech stimuli, determined by a sliding window t-test between
responses to randomly-selected time frames during the passive lis-
tening task and in silence (p < 0.05).
Open source Python (3.6.5) and R (3.6.3) libraries were used to
analyze the data in this study. Standard functions in MNE Python
(0.20.8) were used for data preprocessing. LME models were con-
structed and ﬁt using the R library lme4 (1.1-21). MNE models were
constructed and ﬁt using the Python package pyMNE (https://github.
com/MarvinT/pyMNE).
Band power
The frequency bands used in this study were delta (1 –3Hz), theta
(4–7Hz), alpha (8–12Hz), beta (13–30Hz), gamma (31–50Hz), and high-
gamma (70–150Hz) bands. To compute the power for each band, the
analytic amplitude from eight Gaussian band-pass ﬁlters with loga-
rithmically increasing center frequency55,56 was averaged. For the ERP
analyses, targets were deﬁned as phones involved in one of the three
language-speciﬁc comparisons, and band power data were then seg-
mented into peri-target epochs with 100ms pre-target and 500ms
post-target, and each epoch was z-scored relative to the mean and
standard deviation of its 100ms pre-target baseline.
Electrode localization
Stereo EEG electrodes were localized by registering each patient’s pre-
Op T1-weighted MR volume to an interaoperative CT in 3dSlicer57,58 and
manually marking the contact CT artifacts.
Signiﬁcant electrodes
Broadband neural activity was recorded from a total of 1355 valid
channels across the ten subjects, and for each functional band, each
channel was assessed for speech responsiveness using a sliding-
window one-way t-test, where the band power for 500ms silent epochs
was compared against that of an equivalent number of randomly
sampled speech epochs. Valid channels were those that were not dis-
carded due to the presence of excessive line noise or artifacts. Base-
lining was performed by subtracting from each epoch the average
channel response for the 100ms preceding the epoch onset, and t-tests
were calculated for nine 100ms windows with 50ms overlap across the
500ms post-baseline portion of the epoch. Within each window, values
for each token were averaged over time. Channels were considered
speech responsive if the t-test for at least one window was signiﬁcant
with p <0 . 0 5 .
Spectrographic features for LME models
For each timepoint of the response, a set of features representing the
preceding acoustic context was calculated. First, each excerpt was
resampled to 16 kHz, and a spectrogram was computed for the
downsampled ﬁle using the spectrogram function from the sci-
py.signal Python library. For each excerpt, this function calculated
consecutive Fourier transforms over segments of the excerpt wave-
form that were 128 time bins (=8ms) in length with no zero padding.
Segments were windowed using a Hann function and had 64 time bins
of overlap with one another. This function resulted in a spectrogram
with 65 frequency bins. The DC component of the spectrogram was
removed, and the remaining 64 frequency bins were log transformed
and then pairwise-averaged twice, resulting in a spectrogram with 16
frequency bins. Time bins were then pairwise-averaged three times,
such that each time bin of theﬁnal spectrogram represents a portion of
time eight times longer than the initial resolution (=64ms). Finally, the
full spectrogram, representing the entire excerpt, was split into over-
lapping 16 × 16 chunks, such that each time bin of the total excerpt
spectrogram—from the sixteenth bin to theﬁnal bin—could be mapped
to a 16 × 16 (=1024 ms) chunk representing the spectrographic content
immediately preceding that time bin.
The ﬁnal sample rate of the spectrogram time bins was 15.625Hz.
However, all preprocessed neural data had sample rates of 510Hz,
meaning that each spectrogram time bin corresponded to between 32
and 33 timepoints of the neural data. Therefore, to place the spec-
trographic features and neural response in one-to-one correspon-
dence with one another, for each spectrographic time bin, the samples
of the neural response that took place during that time bin were
averaged together.
As 16 × 16 chunks, each spectrogram would contribute 256 fea-
tures to the mixed effects model, a computationally prohibitive
number of features to ﬁt over hundreds of thousands of datapoints.
Thus, to further reduce the dimensionality of the spectrographic fea-
tures without resorting to further averaging and loss of spectro-
temporal resolution, two different approaches were taken. Reported in
the main body of the manuscript, dimensionality was reduced by using
only the 16 × 8 (=128) most recent features, representing the 512ms
preceding each time bin. Reported in Supplementary Information, 128-
dimensional representations of each 16 × 16 spectrogram were drawn
from the latent space of a Generative Adversarial Interpolative Auto-
encoder (GAIA)
59 that had been trained on these spectrograms.
GAIA networks are a kind of neural network whose architecture is
based on a combination of Autoencoder (AE) and Generative Adver-
sarial Network (GAN) architectures. The GAIA model used to generate
spectrographic features for the LME models used in this paper was
built in Tensorﬂow 2.2 as a class oftensorﬂow.keras.Model.T h eA E
supporting the generator role of the GAN contained two basic sub-
networks, an encoder and a decoder.
The encoder contained an input layer for batches of 16 × 16 ten-
sors followed by two convolutional layers with 32 and 64 ﬁlters,
respectively. Both convolutional layers had RELU activation, a kernel
size of 3, and a 2 × 2 stride. The output of the second convolutional
layer was ﬂattened into a single dimensional tensor using a tf.ker-
as.layers.Flatten layer and its output was sent to a densely-
connected layer of 128 units.
The decoding subnetwork was symmetrical to the encoder, taking
the output of the 128-dimensional z layer as the input to a densely-
connected layer. The densely-connected layer fed into a tf.ker-
as.layers.Reshape layer that returned its input into a multi-
dimensional tensor. This layer was then followed by three deconvo-
lutional layers. The ﬁrst two deconvolutional layers had 64 and 32
ﬁlters, respectively, and each used a RELU activation function, had a
kernel size of 3, and a 2 × 2 stride. The ﬁnal deconvolutional layer had
one ﬁlter, a kernel size of 3, a 1 × 1 stride, and used a sigmoid activation
function.
Like the generator, the discriminator network was an AE, but with
a different structure. The discriminator AE was a UNET, an end-to-end
fully-convolutional AE architecture originally developed by Ronne-
berger et al.
60 for biomedical image segmentation.
The encoder for this architecture contains an input layer followed
by blocks of convolutional and pooling layers. The ﬁrst block con-
tained two convolutional layers with RELU activation functions,
3×3s t r i d e s ,a n d3 2ﬁlters each, followed by a pooling layer where each
unit of the layer downsampled its input by taking the maximum value
of its 2 × 2 window over the input. This block was followed by a block
containing convolutional layers with 64 ﬁlters each but that was
otherwise identical to theﬁrst block. The two blocks were followed by
a ﬁnal convolutional layer with 128 ﬁlters.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 15
Like the generator, the discriminator UNET ’sd e c o d i n gn e t w o r k
was symmetrical to its encoding network. The output of the ﬁnal
convolutional layer of the encoder was the input to another 128-ﬁlter
convolutional layer. The output of that layer was fed into the ﬁrst of
two blocks of upsampling and convolutional layers. This block began
with an upsampling layer that, for each value of the input, output a
2 × 2 tensor of that value. The upsampling layer was followed by two
convolutional layers with 64 ﬁlters each. The convolutional layers of
the second block had 32 ﬁlters each, but the second block was
otherwise identical to theﬁrst block. Theﬁnal layer of the decoder was
a convolutional layer with oneﬁlter, a kernel size of 3, a 1 × 1 stride, and
used a sigmoid activation function.
The Adam optimizer ( tf.keras.optimizers.Adam)w a su s e d
to minimize the pixel-wise error for the generator network. This opti-
mization algorithm is a method of stochastic gradient descent that
adapts the learning rate for each parameter of the model based on the
ﬁrst- and second-order moments (i.e., mean and variance) of the gra-
dients. The Adam optimizer for the generator network was initialized
with a learning rate of 0.001 and an exponential decay rate of 0.5 for
the ﬁrst moment estimates, and all other parameters for the optimizer
were set to their defaults.
The optimizer used for the discriminator network was a Root
Mean Square Propagation (RMSProp) optimizer ( tf.ker-
as.optimizers.RMSprop), a stochastic gradient descent algorithm
that, like Adam, maintains adaptive learning rates for each model
parameter, but adapts learning rates based only on the mean of recent
gradient magnitudes. It was initialized with a learning rate of 0.001 as
well, and all other optimizer parameters were set to their defaults.
The overall logic of the GAIA architecture is as follows: a standard
autoencoder is trained to reproduce its inputs after passing them
through a low-dimensionalz layer. The 128-dimensional space of thez
layer is sampled linearly, sampling two points in the latent space as well
as evenly spaced samples—interpolations—between those two points.
Both the interpolations drawn from z and the low-dimensional repre-
sentations of the original inputs are passed through the decoder net-
work, yielding sets of 16 × 16 spectrograms —~x
i and ~x,r e s p e c t i v e l y .
These reconstructed spectrograms (~xi and ~x) are then passed through
the UNET autoencoder alongside original spectrograms ( x), and the
network is trained to discriminate between the three types of UNET
reconstructions—reconstructions of original inputs ( D(x)), recon-
structions of the ﬁrst AE’s reconstructions (Dð~xÞ), and reconstructions
of the interpolations drawn fromz that do not correspond to any of the
original inputs (Dð~x
iÞ).
Prior to training, each spectrogram was normalized such that its
minimum value was zero, and its maximum value was one. In total,
across all excerpts, the dataset contained 68,271 spectrograms, which
were randomly split into training and testing sets that contained 85%
and 15% of the total dataset, respectively. The GAIA model was trained
on batches of 4096 spectrograms, with 14 batches per training epoch,
and early stopping was implemented such that training halted when
the smoothed generator loss of an epoch exceeded that of the tenth-
most recent epoch. To calculate this smoothed generator loss, lists of
each epoch’s loss values were saved during training to aid in deter-
mining when to stop training. To prevent local perturbations in the
generator loss from causing training to stop inappropriately early,
these lists were smoothed using a Hann function with a window
length of 30.
The model trained for a total of 83 epochs. After training, all
spectrograms were run through the encoder portion of the generator
network, and each spectrogram’s 128-dimensional latent space repre-
sentation was saved for use in the mixed effects model. In all models,
this feature set is referred to as the s1 feature set because it contains
spectrographic features.
Phonemic label features
During preprocessing, neural data were temporally registered to sti-
muli metadata. For each phone the participant heard, the start time,
stop time, and duration of the phone were registered, alongside the
phone’s identity, the identity of the word it was part of, the word’sp a r t
of speech, and the excerpt it was part of. From this information, a
timeseries of one-hot coded features was generated for the set of
unique phone labels. In other words, each timepoint of the neural
response was assigned a vector of features, where each feature
represented a phone label; the value of the feature corresponding to
the current phone label was set to 1, and all other feature values were
set to 0. Following this feature assignment, the matrix of phone label
features was temporally averaged in the same way that neural data
were temporally averaged to attain a one-to-one mapping with the
spectrographic features. Because each vector of phone label features
was sparse and binary, the resultant values in each vector summed to 1.
In this way, the values in each feature vector corresponded to the
proportion of time within that window where a particular phone was
played for the participant. In all models, this feature set is referred to as
the p1 feature set because it contains phone label features.
Linear mixed effects models
For each participant, families of LME models were ﬁt for seven differ-
ent neural response types, each derived from preprocessed raw
recorded data. Six of these response types were the z-scored power for
different EEG frequency bands, and the seventh was broadband LFP.
The frequency bands used in these models were delta (1 –4Hz), theta
(4–7Hz), alpha (8–12Hz), beta (13–30Hz), gamma (31–50Hz), and high-
gamma (70 –150Hz) bands; broadband LFP contained frequencies
0.1–170Hz.
For each of these response types, seven LME models were ﬁt—
three models of interest and four shufﬂe conditions. The three models
of interest contained either only spectrographic features (s1), only
phonemic label features (p1), or both spectrographic and phonemic
features (s1p1). For both the s1 and p1 feature sets, two forms of
shufﬂed feature sets were also created. Feature sets s2 and p2 were
created by shufﬂing s1 and p1 features within excerpts, and feature sets
s3 and p3 were created by shufﬂing s1 and p1 features across the entire
recording session.
All s-series models contained 128 features, each corresponding to
a time-frequency bin of the spectrogram for the analyses presented in
the Main Text. For the analyses described in Supplementary Informa-
tion, each of these 128 features corresponded to a dimension of the
latent space constructed from the GAIA network trained on excerpt
spectrograms as described in the section on spectrographic features
for LME models in Section 4. However, based on the number of
excerpts that the participant listened to, the number of phonemic label
features in each model differed slightly. For participants who com-
pleted at least four blocks of the passive listening task, there were 72
unique labels included in the p-series models. Models for participants
who completed fewer blocks had at least 60 phonemic features. Labels
that did not occur in theﬁrst two task blocks were uncommon phones
and extraneous labels such as
OI, nasalized vowels like ~au and ~ei, and
laughter.
Model evaluation
Relative goodness of modelﬁt was evaluated using the AIC. The AIC is
an estimate of prediction error, calculated for each model as
AIC = 2k /C0 2ln ð^LÞ ð1Þ
Where k is the number of estimated parameters in the model and ^L is
t h em a x i m u mv a l u eo ft h em o d e l’s likelihood function.
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 16
The AICw of each model i was calculated as
expððAICmin /C0 AICiÞ=2Þ,w h e r eA I Cmin is the lowest AIC value of the set
of models and AICi is the AIC value for model i.
MNE Input Features
Input features were created for each of the two conditions of interest.
For the unlabeled spectrogram condition, 256-dimensional (16x16)
spectrograms were created for eachtimebin of the neural response to
represent the 1024ms of acoustic context preceding that timebin.
These spectrograms were created using the procedure described
in the section on spectrographic features for LME models in Section 4.
For the labeled spectrogram condition, 8-bit binary codes (i.e.,
[01010110]) were created for each possible ARPABET label present in
the Buckeye Corpus. Then, two labels (totaling 16 bits) were assigned
to each spectrogram. For 1024ms windows containing only one phone-
level label, the 16-bit label given to that spectrogram was the simple
concatenation of the code for that ARPABET label with itself. For
spectrograms containing more than one phone-level label, the 16-bit
label given to that spectrogram was the simple concatenation of the
code for the label that occupied the plurality of that 1024ms window
and the runner-up label. Then the mean and standard deviation of each
spectrogram was calculated, and the top row of each spectrogram was
replaced with a 1x16 vector representing its 16-bit label. For this row
vector, “0” entries of the 16-bit label were replaced with the value one
standard deviation below the spectrogram’s mean, and“1” entries were
replaced with the value one standard deviation above the spectro-
gram’s mean. In this way, spectrographic labels were designed to have
minimal impact on the prexisting variance and covariance structure of
the spectrograms.
MNE models
MNE models were ﬁt for each participant for each response type for
each condition. These models ﬁt a logistic function that models the
response type (LFP or band power) as a linear combination ofﬁrst- and
second-order features of the stimulus (labeled or unlabeled
spectrograms).
MNE models minimize the mutual information between the
response and the stimulus by maximizing the noise entropy of the
stimulus. This is accomplished by rewriting the mutual information
between the stimulus and the response as the difference between the
response entropy and the stimulu s noise entropy. Then, imposing a
minimal model on the conditional-response probability to ensure that
the stimulus noise entropy is capable of being maximized results in a
logistic function that models the probability (P) of a neural response
(y) given a stimulus ( s) as a linear combination of ﬁrst- and second-
order features of the stimulus.
Thus, a second-order MNE model takes the form
PðyjsÞ =
1
1+ e/C0 zðsÞ , zðsÞ = a + hTs + sTJs ð2Þ
where a corresponds to the mean unit response;h corresponds to the
neural response constrained by the stimulus variance;J corresponds to
the neural response constrained by the stimulus covariance; and s
corresponds to a set of stimulus features. A ﬁrst-order MNE model
contains only the ﬁrst two terms of z(s).
To prevent over ﬁtting, model parameters were estimated over
four jackknives, where input and response data were split into four
batches, and for each jackknife, three of the batches were used as
training data, and the remaining batch was used for testing. The log
loss between the response and the weighted input was minimized
using fmin_cg, a nonlinear conjugate gradient algorithm from the
scientiﬁc computing libraryscipy.optimize, and early stopping was
implemented such that if the log loss on the testing data did not
decrease for ten consecutive epochs, training was halted. The opti-
mized weights for each of the four jackknives were then averaged, and
this set of mean weights was used in all subsequent work.
For each channel, the ﬁt models were used to generate predicted
neural responses. First-order predictions were generated using theﬁt
linear features only, with z(s)= a + h
Ts, and second-order predictions
were ﬁtu s i n gt h ec o m p l e t em o d e l ,w i t hz(s)= a + hTs + sTJs.T h e nf o r
each predicted response, Pearson ’s r was calculated to assess the
degree of correlation between the recorded and predicted responses.
T h e s ev a l u e sw e r et h e nn o r m a l i z e du s i n gt h eF i s h e rZ - T r a n s f o r m a t i o n
such that prediction quality could be compared across model types
and conditions.
MNE shufﬂed models
To ensure that each model ﬁt better than would be expected by
chance, model predictions were also generated from the shuf ﬂed
features of the ﬁt models. For the linear model, the entries of the 256-
dimensional vector feature representing the power-responsive aver-
age were shufﬂed, and predictions were generated using the shufﬂed
linear features only, with z(s)= a + h
Ts. For the quadratic model, the
linear feature was shuf ﬂed as described for the linear model. Addi-
tionally, the quadratic model ’s J-matrix was eigen decomposed, its
eigenvalues were shuf ﬂed, and the J-matrix was then recomposed
using the shufﬂed eigenvalues. Predictions for the shufﬂed quadratic
models were then generated as expected, with z(s)= a + hTs + sTJs.
Shufﬂing in this way leaves the quadratic features (the eigenvectors of
the J-matrix) intact, altering only the weight afforded to each feature in
the predicted response. This manner of shufﬂing therefore provides a
relatively high estimate of the q uality of response that would be
expected by chance, since it preserves the structure of the second-
order features in their entirety, merely re-weighting their contribution
to the predicted response.
Reporting summary
Further information on research design is available in the Nature
Portfolio Reporting Summary linked to this article.
Data availability
The datasets generated and analyzed during the current study are
available in the OpenNeuro repository, registered with thishttps://doi.
org/10.18112/openneuro.ds004703.v1.0.0. Source data are provided
with this paper.
Code availability
Code and source data for allﬁgures are available athttps://github.com/
acmai/NCOMMS-23-00607.
References
1. Flinker, A., Chang, E., Barbaro, N., Berger, M. & Knight, R. Sub-
centimeter language organization in the human temporal lobe.
Brain Lang. 117,1 0 3–109 (2011).
2. Nourski, K. V. et al. Spectral organization of the human lateral
superior temporal gyrus revealed by intracranial recordings.Cere-
bral Cortex 24,3 4 0–352 (2014).
3. Hullett, P. W., Hamilton, L. S., Mesgarani, N., Schreiner, C. E. &
Chang, E. F. Human superior temporal gyrus organization of spec-
trotemporal modulation tuning derived from speech stimuli.J.
Neurosci. 36,2 0 1 4–2026 (2016).
4. Hamilton, L. S., Edwards, E. & Chang, E. F. A spatial map of onset
and sustained responses to speech in the human superior temporal
gyrus. Curr. Biol. 28,1 8 6 0–1871 (2018).
5. Moerel, M., De Martino, F., U ğurbil, K., Formisano, E. & Yacoub, E.
Evaluating the columnar stability of acoustic processing in the
human auditory cortex.J. Neurosci. 38,7 8 2 2–7832 (2018).
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 17
6. Mesgarani, N., Cheung, C., Johnson, K. & Chang, E. F. Phonetic
feature encoding in human superior temporal gyrus.Science 343,
1006–1010 (2014).
7. Port, R. F. & Leary, A. P. Against formal phonology. Language 81,
927–964 (2005).
8. Stilp, C. E. & Kluender, K. R. Cochlea-scaled entropy, not con-
sonants, vowels, or time, best predicts speech intelligibility.Proc.
Natl Acad. Sci. 107,1 2 3 8 7–12392 (2010).
9. Ramscar, M. & Port, R. F. How spoken languages work in the
absence of an inventory of discrete units. Lang. Sci. 53,
58–74 (2016).
1 0 . D a u b e ,C . ,I n c e ,R .A .&G r o s s ,J .S i m p l ea c o u s t i cf e a t u r e sc a n
explain phoneme-based predictions of cortical responses to
speech. Curr. Biol. 29,1 9 2 4–1937 (2019).
11. Pisoni, D. B. & Luce, P. A. Acoustic-phonetic representations in word
recognition.Cognition 25,2 1–52 (1987).
1 2 . L o t t o ,A .J .&H o l t ,L .I nChicago Linguistic SocietyVol.35 (eds Bill-
ings, S. J., Boyle, J. P. & Grifﬁt h ,A .M . )1 9 1–204 (Chicago Linguistic
Society, 2000).
13. Arnold, D., Tomaschek, F., Sering, K., Lopez, F. & Baayen, R. H.
Words from spontaneous conversational speech can be recognized
with human-like accuracy by an error-driven learning algorithm that
discriminates between meanings straight from smart acoustic fea-
tures, bypassing the phoneme as recognition unit.PLoS ONE 12,
e0174623 (2017).
14. Kenstowicz, M. & Kisseberth, C. Generative Phonology: Description
and Theory (Academic Press, 2014).
15. Hayes, B. Introductory PhonologyVol. 7 (John Wiley & Sons, 2008).
16. Silverman, D. Neutralization(Cambridge University Press, 2012).
17. Di Liberto, G. M., O ’Sullivan, J. A. & Lalor, E. C. Low-frequency
cortical entrainment to speech reﬂects phoneme-level processing.
Curr. Biol. 25,2 4 5 7–2465 (2015).
18. De Boer, E. & Kuyper, P. Triggered correlation. IEEE Trans. Biomed.
Eng. 169–179 (1968).
1 9 . S h a r p e e ,T . ,R u s t ,N .C .&B i a l e k, W. Analyzing neural responses to
natural signals: maximally informative dimensions.Neural Compu-
tation 16, 223–250 (2004).
20. Fitzgerald, J. D., Sincich, L. C. & Sharpee, T. O. Minimal models of
multidimensional computations.PLoS Comput. Biol. 7,
e1001111 (2011).
2 1 . v a nS t e v e n i n c k ,R .R . ,D eR u y t e r ,R .&B i a l e k ,W .R e a l - t i m ep e r f o r -
mance of a movement-sensitive neuron in the blowﬂyv i s u a ls y s -
tem: coding and information transfer in short spike sequences.
Proc. Roy. Soc. Lond. Ser. B: Biol. Sci. 234,3 7 9–414 (1988).
22. Kozlov, A. S. & Gentner, T. Q. Central auditory neurons have com-
posite receptiveﬁelds. P r o c .N a t lA c a d .S c i .113, 1441–1446 (2016).
23. Clemens, J., Wohlgemuth, S. & Ronacher, B. Nonlinear computa-
tions underlying temporal and population sparseness in the audi-
tory system of the grasshopper. J. Neurosci. 32,
10053–10062 (2012).
24. Rowekamp, R. J. & Sharpee, T. O. Cross-orientation suppression in
visual area V2. Nat. Commun. 8,1 –9( 2 0 1 7 ) .
25. Atencio, C. A. & Sharpee, T. O. Multidimensional receptive ﬁeld
processing by cat primary auditory cortical neurons.Neuroscience
359,1 3 0–141 (2017).
26. Pinker, S. & Prince, A. On language and connectionism: analysis of a
parallel distributed processing model of language acquisition.
Cognition 28,7 3–193 (1988).
27. Benus, S., Smorodinsky, I. & Gafos, A. Gestural coordination and the
distribution of English‘geminates’. Univ. Pennsylvania Working
Papers Linguistics10,4( 2 0 0 4 ) .
28. Akaike, H. In Selected papers of Hirotugu Akaike199–213
(Springer, 1998).
29. Dresher, B. E. The Phoneme 1–26 (John Wiley & Sons, Ltd Oxford,
UK, 2011).
30. Jones, D. The history and meaning of the term“phoneme”. Le maître
phonétique35,1 –20 (1957).
31. Bloom ﬁeld, L. Language (Motilal Banarsidass Publ., 1994).
32. Twaddell, W. F. On de ﬁning the phoneme. Language 11,
5–62 (1935).
3 3 . M ü n t e ,T .F . ,S a y ,T . ,C l a h s e n ,H . ,S c h i l t z ,K .&K u t a s ,M .D e c o m -
position of morphologically complex words in English: evidence
from event-related brain potentials.
Brain Res. Cogn. Brain Res. 7,
241–253 (1999).
34. Marslen-Wilson, W. D. & Tyler, L. K. Morphology, language and the
brain: the decompositional substrate for language comprehension.
P h i l o s .T r a n s .R .S o c .L o n d .B :B i o l .S c i .362,8 2 3–836 (2007).
35. Bozic, M. & Marslen-Wilson, W. Ne urocognitive contexts for mor-
phological complexity: dissociating inﬂection and derivation.Lang.
Linguist. Compass4,1 0 6 3–1073 (2010).
36. Schiller, N. O. Neurolinguis tic approaches in morphology.Oxford
Research Encyclopedia, Linguistics1–23 (2020).
37. Sereno, J. A. & Jongman, A. Processing of English in ﬂectional
morphology.Mem. Cognit. 25,4 2 5–437 (1997).
38. Saussure, F. M. Course in General Linguistics(Columbia University
Press, 2011).
39. Mercier, M. R. et al. Evaluation of cortical local ﬁeld potential dif-
fusion in stereotactic electro-encephalography recordings: a
glimpse on white matter signal. Neuroimage147,2 1 9–232 (2017).
4 0 . K a j i k a w a ,Y .&S c h r o e d e r ,C .E .H o wl o c a li st h el o c a lﬁeld potential?
Neuron 72,8 4 7–858 (2011).
4 1 . K a j i k a w a ,Y .&S c h r o e d e r ,C .E .G e n e r a t i o no fﬁeld potentials and
modulation of their dynamics through volume integration of cor-
tical activity. J. Neurophysiol.113, 339–351 (2015).
42. Chang, E. F. et al. Categorical speech representation in human
superior temporal gyrus.Nat. Neurosci. 13,1 4 2 8–1432 (2010).
43. Toscano, J. C., McMurray, B., Dennhardt, J. & Luck, S. J. Continuous
perception and graded categorization: electrophysiological evi-
dence for a linear relationship between the acoustic signal and
perceptual encoding of speech.Psychol. Sci.21,1 5 3 2–1540 (2010).
4 4 . L e m i n e n ,A . ,S m o l k a ,E . ,D u n a b e i t i a ,J .A .&P l i a t s i k a s ,C .M o r p h o -
logical processing in the brain: The good (inﬂection), the bad
(derivation) and the ugly (compounding).Cortex 116,4 –44 (2019).
45. Sarrett, M. E., McMurray, B. & Kapnoula, E. C. Dynamic EEG analysis
during language comprehension reveals interactive cascades
between perceptual processing and sentential expectations.Brain
Language
211,1 0 4 8 7 5( 2 0 2 0 ) .
46. Gwilliams, L. How the brain composes morphemes into meaning.
Philos. Trans. Roy. Soc. B 375,2 0 1 9 0 3 1 1( 2 0 2 0 ) .
47. Munding, D., Dubarry, A.-S. & Alario, F.-X. On the cortical dynamics
of word production: a review of the MEG evidence. Lang. Cognit.
Neurosci. 31,4 4 1–462 (2016).
48. Zhou, B. & Hansen, J. H. Rapid discriminative acoustic model based
on eigenspace mapping for fast speaker adaptation.IEEE Trans.
Speech Audio Processing13,5 5 4–564 (2005).
49. Pitt, M. A. et al. Buckeye Corpus of Conversational Speech(2nd
release) (Department of Psychology, 2007).
50. Alturo, N., Boix, E. & Perea, M.-P. Corpus de català contemporani de
la universitat de barcelona (cub): a general presentation.dins C.
PUTSCH 155–170 (2002).
51. Boersma, P. & Weenink, D. Praat: doing phonetics by computer
(version 6.0. 28) [software] (2017).
52. Peirce, J. W. PsychoPy —Psychophysics software in Python.J. Neu-
rosci. Methods 162,8 –13 (2007).
53. Peirce, J. W. Generating stimuli for neuroscience using PsychoPy.
Front. Neuroinform.2,1 0( 2 0 0 8 ) .
54. Gramfort, A. et al. MEG and EEG data analysis with MNE-Python.
Front. Neurosci.7,2 6 7( 2 0 1 3 ) .
55. Crone, N. E., Miglioretti, D. L., Gordon, B. & Lesser, R. P. Functional
mapping of human sensorimotor cortex with electrocorticographic
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 18
spectral analysis. II. Event-related synchronization in the gamma
band. Brain 121,2 3 0 1–2315 (1998).
56. Bouchard, K. E., Mesgarani, N., Johnson, K. & Chang, E. F. Functional
organization of human sensorimotor cortex for speech articulation.
Nature 495,3 2 7–332 (2013).
57. Fedorov, A. et al. 3D Slicer as an image computing platform for the
quantitative imaging network.M a g n .R e s o n .I m a g i n g30,
1323–1341 (2012).
58. Johnson, H., Harris, G. & Williams, K. et al. BRAINSFit: mutual
information rigid registrations of whole-brain 3D images, using the
insight toolkit.Insight J 57,1 –10 (2007).
59. Sainburg, T., Thielk, M., Theilman, B., Migliori, B. & Gentner, T.
Generative adversarial interpolative autoencoding: adversarial
training on latent space interpolations encourage convex
latent distributions. Preprint at https://arxiv.org/abs/1807.
06650 (2018).
60. Ronneberger, O., Fischer, P. & Brox, T. U-net: convolutional net-
works for biomedical image segmentation. InInternational Con-
f e r e n c eo nM e d i c a lI m a g eC o m p u t i n ga n dC o m p u t e r - a s s i s t e d
Intervention234–241 (Springer, 2015).
Acknowledgements
Thanks to Eric Baković, the members of Gentner Lab, and the AMP 2021
and SNL 2021 poster session audiences for questions, comments, and
suggestions on this work. Thank you also to Burke Rosen for assistance
with electrode localization. Thiswork was supported by NIMH training
fellowship T32MH020002 and William Orr Dingwall Dissertation Fel-
lowship to A.M. Remaining errors are ours.
Author contributions
A.M.: Conceptualization, Methodology, Investigation, Software, Formal
Analysis, Visualization, Writing—Original draft preparation; S.R.: Inves-
tigation, Data Curation; S.B.H.: Resources, Project Administration; J.S.:
Resources, Project Administration, Funding Acquisition; T.G.: Con-
ceptualization, Supervision, Writing—Review & Editing.
Competing interests
The authors declare no competing interests.
Additional information
Supplementary informationThe online version contains
supplementary material available at
https://doi.org/10.1038/s41467-024-44844-9.
Correspondenceand requests for materials should be addressed to
Anna Mai.
Peer review informationNature Communicationsthanks Christophe
Pallier and the other, anonymous, reviewer(s) for their contribution to the
peer review of this work. A peer review ﬁle is available.
Reprints and permissions informationis available at
http://www.nature.com/reprints
Publisher’s note Springer Nature remains neutral with regard to jur-
isdictional claims in published maps and institutional afﬁliations.
Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as
long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons licence, and indicate if
changes were made. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless
indicated otherwise in a credit line to the material. If material is not
included in the article’s Creative Commons licence and your intended
use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright
holder. To view a copy of this licence, visithttp://creativecommons.org/
licenses/by/4.0/.
© The Author(s) 2024
Article https://doi.org/10.1038/s41467-024-44844-9
Nature Communications|          (2024) 15:677 19
