# The impact of musical expertise on disentangled and contextual neural encoding of music revealed by generative music models

**Authors:** Gavin Mischler
**Year:** D:20
**Subject:** Nature Communications, doi:10.1038/s41467-025-63961-7

---

Article
https://doi.org/10.1038/s41467-025-63961-7
The impact of musical expertise on
disentangled and contextual neural
encoding of music revealed by generative
music models
Gavin Mischler
1,3, Yinghao Aaron Li1,3, Stephan Bickel
2, Ashesh D. Mehta2 &
Nima Mesgarani

Music perception requires integrating individual notes into their broader
musical context, yet how musical expertise shapes the neural encoding of this
information across the auditory hierarchy remains unclear. Here, we address
this by using the hierarchical representations from a generative music trans-
former model to predict human brain activity. We recorded scalp electro-
encephalography (EEG) from expert musicians and non-musicians, as well
as intracranial EEG (iEEG) from six neurological patients, during listening to
classical piano pieces. We found that deeper layers of the transformer, which
represent more disentangled and contextual musical features, were more
predictive of neural responses in both groups. However, this neural corre-
spondence was signiﬁcantly enhanced by musical expertise: for non-musi-
cians, prediction accuracy plateaued across the model’s ﬁnal layers, whereas
for musicians it continued to increase. This enhanced encoding in experts was
also strongly lateralized to the left hemisphere. Finally, the iEEG recordings
revealed an anatomical gradient for this function, where neural sites pro-
gressively farther from the primary auditory cortex encoded musical context
more strongly. Our study reveals how musical training reﬁnes the hierarchical
neural processing of music and provides a neuro-computational account of
this remarkable cognitive skill. A central challenge in auditory neuroscience is understanding how the
brain transforms a sequence of discrete sounds into a coherent and
structured musical experience. With its intricate tapestry of pitch,
rhythm, and harmony, music is a unique and complex auditory sti-
mulus that engages a wide variety of neural processes1–7. The brain not
only deciphers individual notes, characterized by features such as
pitch, duration, and timbre, but also integrates these elements into
rhythmic patterns, melodic contours, and larger musical sequences. This process spans multiple timescales, from the rapid recognition of
individual notes and intervals to the apprehension of melodic contours
and rhythms, and up to the integration of musical phrases and the-
matic structures8–11. The perception of music and the pleasure derived from it are
intimately connected to the predictability and surprisal of musical
events12–15. Hence, the ability to integrate and interpret contextual cues
is pivotal for the appreciation and understanding of music, which is
also shaped by musical training16. The neural basis for this predictive
processing lies within the auditory pathway. The auditory cortex is
Received: 6 January 2025
Accepted: 28 August 2025
Check for updates
1Mortimer B. Zuckerman Mind Brain Behavior Institute, Columbia University, New York, NY, USA. 2The Feinstein Institutes for Medical Research, Northwell
Health, Manhasset, NY, USA. 3These authors contributed equally: Gavin Mischler, Yinghao Aaron Li.
e-mail: nima@ee.columbia.edu
Nature Communications| (2025) 16:8874

1234567890():,;
1234567890():,;

selective for core musical features like pitch6,17,18, rhythm19,20, and
timbre17,21. Higher order areas of the auditory pathway, and in parti-
cular the inferior frontal gyrus, exhibit a complex, hierarchical neural
encoding adept at both ﬁne-grained acoustic analysis and higher-level
structural and syntactic awareness22–26. The neural responses to musi-
cal notes also encode their predictability13,27, a feature that relies on
contextual processing of higher-order structure. The precise nature of
this context-dependent neural encoding across various timescales and
its modulation by musical expertise remains unknown. Musicians
develop
heightened
automatic
auditory
sensitivity
to
melodic
contours28 and enhanced predictive capabilities29, leading to greater
perception and enjoyment of complex musical compositions16. Fur-
thermore, musicians may recruit distinct neural regions, including
increased involvement of the left hemisphere, compared to non-
musicians,
during
music
note
and
low-level
musical
feature
analysis30–32. This suggests that the musician’s brain constructs an
enhanced representation of music, facilitating heightened sensitivity
to musical features and improved predictive capabilities. However, the
neural basis of this enhanced representation, including how hemi-
spheric recruitment patterns support the hierarchical processing of
musical features, remains unclear. A major challenge in studying the cortical encoding of musical
context is the difﬁculty in measuring and quantifying context in music
at various timescales. Previous studies approached this problem with a
scrambling paradigm, showing that degradation of the musical struc-
tures at different timescales, such as randomizing the pitch or timing
of notes, results in reduced neural encoding in different brain
areas3,22,33. Other studies used computational models with limited
temporal dependencies to measure the predictability of musical
notes13. Past studies of deep learning model features in musical
encoding have shown that they can be used to estimate the melodic
expectation and surprise in listeners27,34, though they did not investi-
gate the properties of the representations or their relation to musical
training. Thus, a computational tool capable of capturing the hier-
archical and long-range contextual dependencies of naturalistic music
is critically needed to fully probe the brain’s processing of complex
musical structure. The advent of computational models capable of
naturalistic music generation35,36, particularly transformer models,
presents an unprecedented opportunity to probe the depths of con-
textual processing in the human auditory system during music per-
ception. These models, capable of handling sequential data over
multiple timescales and mimicking the hierarchical nature of musical
structure, offer a parallel for examining how the brain might organize
and interpret musical information. By simulating the complex layering
of musical context, these models enable a comparative analysis
between the model and the brain that can advance our understanding
of the capacity of the auditory processing pathway for contextual
integration and how it changes with musical expertise. In this study, we directly test how the human auditory pathway
encodes the structure and context of musical stimuli, and how this
encoding is inﬂuenced by musical training. We used electro-
physiological recordings from both the scalp (EEG) and depth and
surface intracranial electrodes (iEEG) as subjects listened to a series of
musical compositions. Linear predictions of the neural responses from
various layers of a transformer model trained to produce music
allowed us to map the encoding of hierarchical and context-dependent
musical features in the brain. We speciﬁcally examined the model’s
disentangled feature encoding, which we deﬁne as the separability of
distinct musical attributes like pitch and duration within the model’s
representations, and found signiﬁcant distinctions between musicians
and non-musicians. In addition, the intracranial recordings illuminated
spatial variations of this encoding, elucidating the role of training and
exposure in shaping the cortical representation of music and offering
insights
into
the
brain
regions
responsible
for
these
neural
representations. Results
To examine the cortical encoding of musical context, we recorded
scalp EEG from 10 expert pianists with a degree in music and a mini-
mum of ten years of music training (musicians) and 10 subjects without
musical training (non-musicians) (Fig. 1a)13. We also recorded intra-
cranial EEG (iEEG) from 6 neurological patients undergoing epilepsy
surgery, none of whom had any musical training. All subjects listened
to 30 minutes of music consisting of 8 Bach pieces played on piano. Subjects were asked to report their familiarity with the pieces after
hearing them, and no signiﬁcant differences between musicians and
non-musicians were found (see Methods). We used a 13-layer
sequence-to-sequence transformer model to model the same musi-
cal pieces (Musicautobot37). The model was trained on music MIDI
data, including classical music from a wide range of composers, and
consisted of both an encoder and a decoder, and was trained on
multiple tasks including masked note, chord, and melody prediction. We derived causal transformer features from all layers of the encoder
to understand the representations learned by the model for processing
continuous music, which we then compared to the neural recordings
from subjects listening to the same piano pieces. Increased contextual encoding in transformer layers
We ﬁrst quantiﬁed the encoding of music features in transformer
layers. These models have been shown to generate contextualized
embeddings reﬂecting not only the note itself, but its relationship
with other notes. The architecture of transformer models in lan-
guage processing is characterized by a progression from encoding
simple, low-level information in the initial layers to capturing more
detailed, higher-order features in the deeper layers38. We examined
this gradual encoding in the music transformer model to under-
stand whether it demonstrated a similar hierarchical encoding of
features based on their complexity and departure from simple
acoustic features. First, we projected the embeddings from each
layer to two dimensions using t-SNE39. Figure 1b illustrates two-
dimensional t-SNE features for layers 1, 7, and 13 of the transformer
models. In Fig. 1b, data points represent individual music notes
across all music pieces and are colored based on a certain music
feature, including pitch class (chromatic categories, e.g., C, C#),
note duration (normalized temporal lengths), music piece (assigned
from MIDI metadata), and full pitch name (combination of pitch
class and octave, e.g., C4, G#3). As we progress from layer 1 to layer
13, clear clusters for note duration begin to form by layer 7 and
become more distinct by layer 13, indicating that note duration is
encoded more explicitly in deeper layers. In contrast, more abstract
attributes, such as the identity of the music piece to which a given
note belongs, require a broader understanding of musical context
and structure. t-SNE embeddings do not show obvious clustering
based on this attribute at layer 7 (Fig. 1b). However, by layer 13, more
distinct clusters emerge, demonstrating that the deeper layers of
the transformer model contain more disentangled representations
of these features. Further evidence of this progressively hierarchical
encoding comes from computing the f-ratio of these discrete note
classes from the embeddings, a measure of the separability of the
classes in the high-dimensional space. We measured the f-ratio
between notes grouped by either pitch classes, note duration, music
piece, and full pitch names using the full representations from layers
1 to 13. The f-ratio between these note features generally increases
over layers (Fig. 1c), indicating that the representations become
increasingly separable over layers based on these attributes. These
ﬁndings conﬁrm that the music transformer model’s embeddings
are extracting relevant features from the music pieces, which go
beyond simple acoustic features, and that later layers more robustly
separate various characteristics of the notes that likely require
integration
over
longer
timescales
and
greater
contextual
information. Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

Layer 1
Layer 2
Layer 13
Waveform
(Bach piano piece)... NMF
TRF
NMF
TRF
NMF
TRF
MIDI representation
13-layer music
transformer encoder
Non-negative matrix factorization
Temporal response function...... EEG

### 10 Musician

### 10 Non-musician

iEEG

### 6 Non-musician

Layer 1
Layer 7

Layer 13

f-statistics

9 11 13

9 11 13

9 11 13

9 11 13
t-SNE 2

-50
t-SNE 1

-50

t-SNE 2

-50

-50

t-SNE 2

-50

-50

-50

-50

-50

-50

-50

-50

-50

-50

-50
t-SNE 1
t-SNE 1
t-SNE 1

Layers
Layers
Layers
Layers
Methodology for Predicting Neural Signal from Representations of Music Stimuli
a.
t-SNE Embeddings of Music Transformer Embeddings Show Separation of Certain Note Features
b. Pitch class
Note duration
Music piece identity
Full pitch name
F-ratio of Music Feature Separability over Model Layers
c. Pitch class
Note duration
Music piece identity
Full pitch name
Fig. 1 | Investigating music transformer embeddings. a The paradigm for pre-
dicting neural data from a generative music transformer model. Bach music pieces
were fed into a pre-trained encoder-decoder transformer model using their MIDI
representation, and then the note embeddings from each of the initial embedding
layer and subsequent 12 layers of the encoder were extracted for further analysis. The dimensionality of these embeddings was reduced via nonnegative matrix
factorization (NMF), and then cross-validated temporal response function (TRF)
models were trained to predict the EEG and iEEG electrode responses. b Note
embeddings from layers 1, 7, and 13 of the transformer model were plotted in two
dimensions with t-SNE, and notes were colored based on either their pitch class,
note duration, music piece identity, and full pitch name. c To measure the separ-
ability of each illustrated feature from the embedding space, the f-ratio from the
full-dimensional embeddings was computed from each layer of the model. Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

Progressive neural encoding of transformer music features
To understand the extent to which the cortical surface responses to
the music reﬂect the embeddings of the transformer models, we pre-
dicted the EEG response of each electrode for all 20 subjects from the
transformer features. This was done after applying nonnegative matrix
factorization (NMF) for dimensionality reduction. These transformed
features were then used to linearly predict the EEG data using temporal
response functions (TRF) with leave-one-out cross-validation for each
subject and music piece40,41, ensuring more reliable scores than a
shufﬂed train-test splitting scheme42. We analyzed the correlation
between actual and predicted neural responses with cross-validation. We used Pearson correlation to assess the prediction performance
with cross-validation (see Methods). Given that the ﬁrst layer embed-
dings provide the least contextual and separable feature encoding, we
computed the improvement in prediction correlation by each sub-
sequent layer compared to the ﬁrst layer. This also served to control
for differences in low-level acoustic feature encoding between musi-
cians and non-musicians, ensuring that the comparison was restricted
to the contextual information being extracted by the music model,
since prior work with this dataset found that musicians encode both
acoustic features and music-speciﬁc features more strongly than non-
musicians13. The raw prediction correlation values illustrate differ-
ences in the baseline encoding strength of these features for musicians
and non-musicians (Supplementary Fig. 1). Figure 2a shows these
correlation improvements over the layers of the transformer, averaged
over the musician and non-musician groups. Both populations showed
an increase in prediction correlations over layers, meaning that the
more disentangled note representations formed in the later layers
were more predictive of the EEG responses. This suggests that across
subject groups, the encoding of musical features in the brain is a
progressive process that unfolds over multiple levels of neural pro-
cessing, with separable representations of musical features arising in
both musicians and non-musicians. Differential neural encoding of music from expertise
We then explored the impact of musical expertise on the strength of
this encoding of disentangled musical features by directly comparing
the musician and non-musician groups. Although the correlation
generally increased over layers for both groups, the average correla-
tion is signiﬁcantly higher for musicians than non-musicians in nearly
all the later layers of the model (Fig. 2b). In fact, the correlation values
plateaued for non-musicians in the last four layers of the model, while
they continued to increase for the musician group, leading to the
difference in correlation between musicians and non-musicians gen-
erally increasing over transformer layers (Fig. 2b). As a control to
ensure that changes in correlation over layers were not due to sys-
tematic noise ampliﬁcation or other artifacts of the transformer
architecture, we extracted the same representations from 10 randomly
initialized music transformer models, training TRF models for each in
the same way as before. We averaged these 10 prediction correlations
and plotted the results for the random model (Fig. 2a), ﬁnding that the
later layers of the model show only slight improved correlation com-
pared to the ﬁrst layer in the random model, and there are no sig-
niﬁcant differences between this progression in musician and non-
musicians in later layers (Wilcoxon ranksum test, p > 0.05, FDR
corrected43, for all layers except for layer 3, where musicians are less
negative than non-musicians, and layer 7, where non-musicians are
more positive than musicians). These ﬁndings suggest that musical
expertise facilitates the formation of more disentangled musical fea-
tures which are more similar to those created by the later layers of a
pretrained music transformer model. Since all musical features displayed relative increases in separ-
ability over layers of the model (Fig. 1c), we sought to uncover which
aspects of musical feature encoding were driving the differences
between musicians and non-musicians. We used a linear model to
predict the correlation difference between musician and non-musician
EEG predictions from the f-ratio of the four musical features examined
earlier over layers. We found that only the f-ratio of music piece
identity, which is the most highly contextualized of the four features,
had
a
signiﬁcant
linear
prediction
coefﬁcient
(Supplementary
Fig. 2) (p = 0.009). Building from this result, and since layer progression is related to
contextual encoding in transformer language models44,45, we hypo-
thesized that contextual encoding may play a signiﬁcant role in the
observed patterns in the music transformer. To test thishypothesis, we
predicted the EEG responses from the ﬁnal transformer encoder layer
as we varied the contextual input size to the model. The context size
refers to the number of music notes fed into the model before the
current note, thus limiting the maximum information available to the
network. We varied the input size from 1 (a single note with no context)
to full context (in which all notes before the current note were inclu-
ded in the input). For musicians, we found that the ﬁnal layer EEG
prediction correlations continued to increase as the context size grew
larger, even until an input size of 300 notes (Fig. 2d). Non-musicians, in
contrast, did not show improvement after an input size of 100 notes. The difference between musicians and non-musicians over context
also continues increasing over layers (Fig. 2e), and musicians always
showed signiﬁcantly higher correlations than non-musicians except at
a context size of 100 notes (Wilcoxon ranksum test, p < 0.05, FDR
corrected43). These ﬁndings suggest that musicians integrate musical
context over longer time periods, while non-musicians may be limited
in integrating extended musical contexts, reaching a plateau beyond a
certain contextual window. This could be attributed to the musicians’ enhanced cognitive
functions and neural mechanisms for processing complex musical
structures46, including their ability to anticipate and integrate long-
term dependencies in music47. Our ﬁndings demonstrate that strongly
disentangled musical features and contextual information are more
strongly encoded in musicians, underscoring the profound impact of
musical training on the brain’s capacity to process and understand
music and providing further evidence for the plasticity of the human
auditory system in response to specialized training. Spatial variations in music context encoding and hemispheric
lateralization of musical experience
We systematically quantiﬁed the effects of contextual encoding of
each electrode by measuring its slope of change in the prediction
correlation (y) as a function of either transformer layers or context
window (x) to calculate the slope of change (a) in the equation y = ax +
b. A higher coefﬁcient indicates a larger improvement over the base-
line (ﬁrst layer or no context) as either the layers or context window
increases, and therefore it suggests that more separable features or
extended context are more important for that electrode when pro-
cessing the music stimuli. We visualized the spatial variation of slopes over layers and con-
text windows on topographic maps, focusing on the difference
between musicians and non-musicians. This uncovered hemispheric
differences between these subject groups, where the prediction cor-
relations of the left hemisphere in musicians displayed a more positive
correspondence with model layer and context length than in non-
musicians (Fig. 2c and f). A similar left hemisphere bias was identiﬁed
when simply plotting the correlation improvement in the last layer for
musicians versus non-musicians (Supplementary Fig. 3), illustrating
that this effect does not depend on the method used to quantify dif-
ferences in encoding strength over layers. To ensure that this was
indeed related to the learned musical feature extraction being per-
formed by the model, and not an artifact of its architecture, we plotted
the same spatial variation of slopes over layers for the scores produced
by the randomly initialized music transformers (Supplementary Fig. 4),
ﬁnding no left hemispheric bias visually. Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

Given the left-hemispheric lateralization we identiﬁed, we sum-
marized the impact of musical training on the lateralization of EEG
prediction correlations in further analyses. For each subject, we esti-
mated the left hemispheric lateralization by computing the difference
in prediction correlation between the left and right hemisphere elec-
trodes. Then we computed the difference in this lateralization value
between the musician and non-musician at each layer of the model. We
found that musicians showed signiﬁcantly higher left hemisphere
lateralization in all layers of the model compared to non-musicians
(Wilcoxon ranksum test, p < 0.05, FDR corrected43) (Fig. 2g), and this
difference became even more pronounced in later layers. Similarly, by
varying the context size and using the correlations from the last layer
only, we found that musicians had signiﬁcantly higher left hemisphere
lateralization atallbut a single note of context (Wilcoxon ranksum test,
p < 0.05, FDR corrected43) (Fig. 2h). These ﬁndings suggest that the left
hemisphere may be more involved in the disentanglement of musical
Correlation Improvement

Layer
-2

Correlation Difference
10-3
0.5

1.5

10-3
1 10 100 200 300 500
all

Last Layer Correlation
1 10 100 200 300 500
all

Correlation Difference
10-3

10-3

Layer
Context size
Layer
Context size
Correlation (Left - right)
Correlation (Left - right)

10-4
Slope of change
over layers
Slope of change
over context

10-4
10-3

10 100 200 300 500 all
Context size
EEG Prediction Correlation
by Layer
Musician - Non-musician
Correlation Difference by Layer
-2

2.5

b.
a. Musician - Non-musician
Layer Slope Difference
c. EEG Prediction Correlation from
Last Layer by Context Size
d. Musician - Non-musician Last Layer
Correlation Difference by Context
e. Musician - Non-musician
Context Slope Difference
f. Musician - Non-musician
Correlation Lateralizationby Layer
g. Musician - Non-musician Last Layer
Correlation Lateralizationby Context
h.
***
***
*
**
***
n.s.
n.s.
10-3
-10
-5

Musician
Non-Musician
Trained model
Random model

Fig. 2 | Results from the analysis of EEG recordings from musicians and non-
musicians. a EEG prediction correlation improvements compared to the ﬁrst layer
(averaged over all electrodes from each subject at each transformer layer, then
averaged over subjects) were grouped into musician and non-musician brains and
averaged. Shaded regions indicate standard error of the mean over subjects. b The
difference between musician and non-musician EEG prediction correlations over
model layers. The signiﬁcance was computed with a two-sided Wilcoxon ranksum
test, with signiﬁcant positive differences indicated by stars above each layer
(**p < 0.01, ***p < 0.001, FDR corrected43) and exact p-values p = 0.0002, p = 0.0011,
p = 0.0467, p = 0.0008, p = 3.8 × 10-8 for layers 7, 10, 11, 12, and 13, respectively. Shaded region indicates the average standard error of the musician and non-
musician sub-groups. c Slope of the correlations over layers via line ﬁtting. The
slopes were averaged for each electrode across musicians and non-musicians
separately, then the difference between the group-average slopes was plotted on a
scalp topoplot. d Average EEG prediction correlations using the ﬁnal layer’s
embeddings for a range of limited musical note context sizes. Shaded regions
indicate the standard error of the mean. e The difference between musician and
non-musician EEG prediction correlations over context sizes. Signiﬁcant differ-
ences were tested with a two-sided Wilcoxon ranksum test. All context sizes were
statistically signiﬁcant (p < 0.05, FDR corrected43) except for 100 notes. f The slope
of the correlations over context sizes via line ﬁtting. The slopes were averaged for
each electrode across musicians and non-musicians separately, then the difference
between the group-average slopes was plotted on a scalp topoplot. g The differ-
ence between the average EEG prediction lateralization in musicians and non-
musicians. The shaded region indicates the average standard error of the mean
between musicians and non-musicians. A two-sided Wilcoxon ranksum test for
statistical signiﬁcance of the difference between musicians and non-musicians
found every layer to be signiﬁcantly different (p < 0.05, FDR corrected43). h The
difference in lateralization of the EEG prediction correlations between musicians
and non-musicians for different limited context sizes in the last layer. Shaded
regions indicate the average standard error of the mean between musicians and
non-musicians. A two-sided Wilcoxon ranksum test for statistical signiﬁcance of the
difference between musicians and non-musicians found every context size except
for 1 note to be signiﬁcantly different (p < 0.05, FDR corrected43). Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

features and that frontal areas may play a more signiﬁcant role in the
increased encoding of musical context after musical training. These
ﬁndings highlight the differences in where and how disentangled
musical features and long-term contextual information emerge with
musical training. Intracranial EEG analysis of brain regions involved in contextual
music encoding
While these EEG ﬁndings demonstrate that musical expertise enhances
the encoding of contextual features with a left-hemispheric bias, they
lack the spatial resolution to determine where in the brain this hier-
archical processing occurs. To uncover the underlying anatomical
substrates, we extended our analysis to intracranial EEG (iEEG) from
6 subjects, using a similar analysis approach as the one used for EEG. Although these human subjects were not trained musicians, the ana-
tomical recording speciﬁcity allowed for new insights into the locus of
music-transformer brain similarity. The iEEG signals were predicted
using transformer features across layers in the same way as was done
with EEG recordings, and we identiﬁed a rise in cross-validated pre-
diction correlation over layers for most electrodes, though not all. The
raw correlation values varied widely over electrodes and were highest
in the primary auditory cortex (Supplementary Fig. 5), likely due to
differences in acoustic responsiveness and SNR across intracranial
electrodes and the auditory hierarchy, limiting interpretation of these
raw correlations. So, we normalized the correlations of each electrode
over layers in order to separate electrodes by their pattern of trans-
former correspondence and performed unsupervised k-means clus-
tering (Fig. 3a) (cluster 0: 24 electrodes, cluster 1: 54 electrodes, cluster
2: 100 electrodes). This data-driven approach allowed us to test whe-
ther distinct neural populations would emerge that mirrored the
shallow-to-deep feature extraction hierarchy of the transformer
model. We set the number of clusters to three based on the elbow
method on the within-cluster sum of squares (Supplementary Fig. 6). These clusters signiﬁcantly differed in which layers scored highest, as
quantiﬁed by the center of mass of the correlations over layers for
electrodes in each cluster (Fig. 3b) (Wilcoxon ranksum test, 0 vs 1:
p = 4.6 × 10−12, 1 vs 2: p = 3.8 × 10−9). This indicates that certain elec-
trodes were more similar in their musical encoding to early layers of
the transformer model, while others were more similar to later layers. Two of the clusters, cluster 1 and cluster 2, display increasing corre-
lations over layers, but cluster 1 reaches a plateau earlier, while cluster
2 continues increasing in model similarity over layers. Cluster 2 is also
located signiﬁcantly further from posteromedial Heschl’s Gyrus
(pmHG) (Wilcoxon ranksum test, 0 vs 2: p = 0.046, 1 vs 2: p = 7.7 × 10−7),
or primary auditory cortex (Fig. 3c)48–50. We also conﬁrmed that loca-
tion along the auditory hierarchy was related to the correlation center
Cluster
Normalized prediction correlation

1.0

HG
Insula
PT
STG
ITG
IFG
T. Pole
MTG
Distance from pmHG (mm)
Fraction of neural
sites in each cluster
Layer
Correlation C.o. M. over layers
Fraction of neural sites
Region

6.0
6.5
7.0
0.00
0.02
0.04
0.01
0.03
0.05
0.5
1.0
0.0

0.5

iEEG Prediction
Correlation Clustering
a. Layer Depth by
Cluster
b. Distance from Primary AC
by Cluster
c. Cluster Assignment by
Region
d. Clustered Electrode Locations on the Brain
e.
n=20
n=6
n=14
n=27
n=9
n=13
n=9
n=5
Fig. 3 | Layer-wise analysis of the prediction correlations of iEEG recordings
from the model. a Prediction correlations for each electrode over model layers
were normalized between 0 and 1 and clustered into 3 clusters. The cluster averages
are plotted over model layers, with shaded regions indicating standard error of the
mean over electrodes. b The center of mass (C.o. M.) of the normalized correlations
over layers was computed for each electrode and electrodes were grouped by
cluster. The distributions of each cluster are shown with box-and-whisker plots,
where the black line is the median, the box deﬁnes the ﬁrst and third quartiles, and
the whiskers extend to the minimum and maximum values (n = 24, 54, and 100 for
clusters 0, 1, and 2, respectively). c The distributions of the distances of each
electrode from pmHG from each cluster’s electrodes are shown. Vertical lines
above each distribution indicate the median distance for that cluster. d Regions of
interest were selected based on the presence of at least 5 electrodes, and the
fraction of electrodes in each region which were assigned to each cluster is shown,
along with the total number of electrodes in each region. e iEEG electrodes are
plotted on an inﬂated FreeSurfer average brain98, with electrode colors indicating
cluster assignment. Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

of mass by ﬁtting a linear mixed-effects model to predict the correla-
tion center of mass using the distance from pmHG and the hemisphere
label as independent variables, controlling for subject coverage by
using the subject identity of each electrode as a random effect. We
found a signiﬁcant ﬁxed effect of distance from pmHG (p = 0.044) but
not hemisphere (Supplementary Fig. 7), illustrating that electrodes
further along the hierarchy correspond better to later layers, without
signiﬁcant differences between hemispheres. We grouped electrodes
into anatomical regions (Fig. 3d) which contained at least 5 electrodes
each and plotted them on the brain (Fig. 3d and e). The electrode
clusters display notable anatomical correspondence, with cluster 0
mostly comprising neural sites in primary auditory cortex, cluster 1
including mostly auditory cortex, posterior STG, and planum tem-
porale, and cluster 2 electrodes were predominantly found outside
auditory cortex and into MTG, temporal pole (T. pole), and frontal
gyrus. Overall, electrodes from both clusters 1 and 2 were spread
across the entire neural processing hierarchy, demonstrating that
contextual processing of music also occurs at several stages of the
hierarchy. We then conducted the same analysis as with the EEG recordings
by varying the input context window of the transformer embeddings
and predicting the iEEG data. The peak scores (over layers) for the
electrodes are shown for each context window (Fig. 4a). On average,
the peak score rises and plateaus around 50 notes of context, in
agreement with the non-musician EEG results. To investigate the ana-
tomical inﬂuence on contextual processing of music in the iEEG data,
we quantiﬁed the amount of context used by a given electrode using
the center of mass of the prediction correlation over context lengths,
with a higher value indicating a later rise or plateau in score. This
metric for contextual encoding is signiﬁcantly correlated with the
distance of an electrode from primary auditory cortex (Fig. 4b)
(Pearson r = 0.32, p = 1.5 × 10−5). Additionally, we ﬁt a linear mixed-
effects model to predict each electrode’s contextual encoding using its
distance from pmHG, with a random effect of subject identity to
control for the varying electrode coverage by subject. We found a
signiﬁcant ﬁxed effect of distance from pmHG (p = 0.004). Thus,
although the range of contextual encoding assessed with this center of
mass metric is relatively small (most electrodes fall between 240 and
*
Distance from pmHG (mm)

Correlation C.o. M. over context
Score C.o. M. over context length

iEEG Last Layer Correlation
by Context
a. Context Length Used by Electrodes
Relates to Neural Hierarchy
b. Context Length Used by
Region
c. Score C.o. M. over
context size
Context Length Used by Electrodes
d.
r = 0.32 ***

Region
HG
Insula
PT
STG
ITG
IFG
T. Pole
MTG

10 20 50

Context size
Last layer correlation
0.07
0.09
0.08
0.06
Fig. 4 | Results from analyzing the relationship between context size and
prediction correlations of iEEG recordings. a Last transformer layer correlation
of the iEEG electrode prediction correlations when the embeddings were generated
from context-limited input. The line shows the average over all electrodes, and the
shaded region indicates standard error of the mean. b The center of mass (C.o. M.)
of each electrode’s correlations over context sizes was computed and is correlated
with each electrode’s distance from pmHG (Pearson r = 0.32, p = 1.5 × 10−5). Line
shows the line of best ﬁt, with the shadedregion showing a bootstrapped (n = 1000)
conﬁdence interval of the line, and *** indicates p < 0.001 from the Pearson corre-
lation’s signiﬁcance test. c Box and whisker plots showing the context size C.o. M. of
electrodes in each region of interest, where the line in the box is the median, the
box deﬁnes the ﬁrst and third quartiles, and the whiskers extend to the
minimum and maximum values that are within 1.5 times the inter-quartile
range. Data points outside this range are indicated individually by circles. The
number of electrodes in each region is as follows (HG: 20, Insula: 6, PT: 14, STG: 27, ITG: 9, IFG: 13, T. Pole: 9, MTG: 5). Statistically signiﬁcant differences in C.o. M. are
shown with the black lines above the bars, where * indicates p < 0.05, and
p = 0.0348, p = 0.0348, p = 0.0425, p = 0.0425 for T. Pole vs HG, PT, STG, and ITG,
respectively (two-sided Wilcoxon rank sum test, FDR corrected43). d The context
size C.o. M. of each electrode is indicated with its color on the inﬂated FreeSurfer
average brain98, clipping the color scale at the 5th and 95th percentiles of the
distribution of C.o. M. values. Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

260 words), electrodes further along the processing pathway utilize
more contextual information from the music in their responses. Splitting electrodes into all regions of interest with at least ﬁve elec-
trodes each, we found that temporal pole, a region far from the pri-
mary auditory cortex, encoded context more strongly than primary
regions (Fig. 4c). Speciﬁcally, temporal pole displayed signiﬁcantly
stronger contextual encoding compared to HG, PT, STG, and ITG
(Wilcoxon ranksum test, p < 0.05, FDR corrected43 across all pairs of
regions). This measure of context length used by each electrode can
also be seen visually over the neural hierarchy in Fig. 4d. Overall, these
results suggest that a hierarchy of musical feature extraction exists in
the brain, with greater contextual encoding of music pieces occurring
primarily beyond the boundaries of the auditory cortex. Discussion
Our study reveals that musical expertise profoundly shapes the brain’s
ability to process musical context, an effect we mapped by comparing
neural responses to the hierarchical representations of a generative
music transformer model. We found that neural prediction correla-
tions were signiﬁcantly greater for musicians, an advantage that was
most pronounced in the model’s deeper layers. Furthermore, musi-
cians demonstrated an enhanced capacity to integrate information
over longer temporal windows compared to non-musicians. These
ﬁndings suggest that musical training reﬁnes the brain’s ability to
construct disentangled representations of music, a process that cor-
responds to the deeper, more contextualized layers of the transfor-
mer model. We found that the layers of the model demonstrate an increasing
processing of musical structure and context, with deeper layers
encoding more disentangled features and integrating over longer
context, a result which matches similar ﬁndings in transformer models
trained on text44,51. When predicting the EEG responses of musicians
and non-musicians from the layers of the transformer model, the
neural prediction correlations were greater for musicians compared to
non-musicians, especially in later layers and for longer context win-
dows, indicating thatmusical training mayreﬁne the brain’s capacity to
construct disentangled representations of music and process musical
context. Although prior works have demonstrated stronger baseline
encoding in the right hemisphere of melodic content52 and musical
syntax53, several previous studies have identiﬁed increased left hemi-
sphere recruitment by musicians compared to non-musicians during
music note and low-level musical feature processing30–32 as well as in
chord discrimination54. Our ﬁndings build on these lateralization
effects by showing stronger correspondence with disentangled and
contextual music features in the left hemisphere by musicians com-
pared to non-musicians. Moreover, our results suggest a distinction in
where structure and context are processed in musicians, where the
encoding of longer context increasingly involves the left frontal cor-
tical areas. To uncover the neural regions behind this contextual pro-
cessing of music, our iEEG recordings offered more insight. The neural
sites that were most similar to the latest layers of the model were
distributed throughout the entire auditory processing hierarchy,
though they were most prevalent further from the primary auditory
cortex. A limitation of the iEEG recordings was that we were unable to
record from trained musicians, and the electrode coverage in non-
musicians was unequally distributed across hemispheres, preventing
us from assessing hemispheric differences in more localized neural
regions. Nonetheless, our results build on recent investigations of
music feature encoding and contextual integration and suggest that
the brain’s processing of musical context is hierarchical, adaptable,
and is inﬂuenced by cognitive factors such as experience and
exposure. Our analyses suggest that music processing in the brain is hier-
archical in nature, especially in the context of varying temporal
scales22,23. The distinct patterns of neural response to music in
musicians and non-musicians when compared to the later layers of the
transformer model, suggest that higher-order cognitive processes are
signiﬁcantly involved in music listening. This is consistent with pre-
vious research that has identiﬁed a hierarchical organization in the
brain for processing musical elements, ranging from simple features
like pitch and rhythm to more complex aspects such as melody and
harmony22,23,55,56 as well as long-term syntactic structure57. Additionally,
prior research has highlighted the critical role of the frontal cortex,
particularly the inferior frontal gyrus, in the hierarchical processing of
music24–26,58,59. Consistent with these ﬁndings, our results demonstrate
increased recruitment of the left frontal cortex in musicians and
stronger correspondence between neural activity in regions beyond
the primary auditory cortex and the deeper layers of the model. The
progression of predictability in neural responses from the mid to the
deeper layers of the transformer in our study may reﬂect this same
hierarchicalprocessing, where basic musicalelements are processed at
lower levels, and more complex, temporally extended structures are
understood at higher levels. Such a multi-tiered processing mechanism
is supported by studies showing that different brain regions are acti-
vated in response to different musical structures, indicating a dis-
tributed yet organized processing network60,61. A major implication of
our study is that this hierarchical processing may be ﬁne-tuned in
musicians, enabling them to more effectively integrate and interpret
complex musical structures over time62. A limitation of our metho-
dology is that musicians may have greater familiarity with the Bach
pieces used in the study, potentially enhancing their ability to predict
upcoming musical structures. While our self-reported familiarity rat-
ings for the speciﬁc pieces did not signiﬁcantly differ between groups,
a more critical factor may be the musician’s greater implicit familiarity
with the stylistic rules and structure of the Western classical genre. This deeper stylistic knowledge could partly explain the more disen-
tangled and contextual neural responses observed in musicians, as
well as the stronger correspondence between their neural activity and
the deeper layers of the model. Consequently, the differences in
frontal cortex EEG predictability between musicians and non-
musicians may reﬂect differential recruitment of these regions for
generating musical predictions and expectation during listening59. A
signiﬁcant direction for future work would be to explicitly control for
this with carefully selected musical stimuli. Besides music stimuli style,
training in speciﬁc genres of music, such as for jazz or classical musi-
cians, has been shown to differentially modulate neural responses to
different musical features63,64, implying that neural responses to music
arise from a complex combination of familiarity, training, and genre-
speciﬁc musical experience. In this study, all musicians were trained in
Western classical music, and the stimuli came from this same genre. Despite the fact that self-reported familiarity ratings were not sig-
niﬁcantly different between musicians and non-musicians, familiarity
with the stimuli may have played a role in differentiating between
musicians and non-musicians through the recognition of long-term
musical structure. Nonetheless, while it remains unclear whether the
observed differences are driven primarily by musical training or
familiarity, the consistent observation of enhanced neural encoding in
musicians highlights the unique ways their brains process music. The differential neural responses to musical context between
musicians and non-musicians observed in our study also align with the
growing body of research indicating that musical training can induce
long-lasting functional and structural changes in the brain. For
instance, studies have shown that musicians typically exhibit enhanced
auditory processing, more robust neural encoding of sound, and
greater connectivity in brain regions associated with auditory and
motor functions and working memory65,66. These adaptations are
thought to result from the demands of musical training, which requires
precise auditory discrimination and motor coordination, and they
manifest as heightened sensitivity and efﬁciency in processing musical
information62,67,68. Our ﬁndings contribute to this understanding by
Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

suggesting that such neuroplastic adaptations extend to the proces-
sing of musical structure and context, with musicians exhibiting more
reﬁned neural encoding patterns, especially in higher-order cognitive
processes. This adds a new dimension to our understanding of how
musical training shapes the brain, indicating that it not only enhances
basic auditory skills but also inﬂuences the hierarchical processing of
complex musical structures. Future research should delve deeper into
these neuroplastic changes, examining how various forms of musical
training and exposure distinctively shape the brain’s response to
music16,69. A particularly insightful future direction is to explore whe-
ther enhanced contextual processing in musicians stems from their
established superior working memory70. The ability to integrate
musical information over long time windows, as we observed in our
expert group, places signiﬁcant demands on neural resources for
holding and manipulating sequential information that is central to
working memory. Furthermore, future work should investigate if the
underlying mechanisms are akin to those involved in the improved
perception of speech in noise, a contextual skill also found to be better
developed in musicians67,71. The utilization of advanced AI models, such as the music gen-
erative transformer in our study, offers a novel lens through which we
can view and understand complex cognitive processes. The success of
this model in predicting neural responses to musical stimuli under-
scores its potential as a proxy for human cognitive processing. This
aligns with emerging research suggesting that AI, particularly deep
learning models, can simulate aspects of human cognition, offering
insights into underlying neural mechanisms72,73. In music listening,
recent studies have found recurrent and transformer model features
to relate to melodic expectations27,34. In visual processing, deep
learning models like convolutional neural networks (CNNs) have pro-
vided insights into the brain’s hierarchical processing of visual stimuli,
mirroring the organization of the visual cortex74,75. Similar insights
have been gained in both recurrent and transformer models of speech
and language processing76–84. Our analysis of the contextual encoding
of music follows recent ﬁndings in language processing, which have
identiﬁed greater contextual dependence in later regions of the neural
hierarchy82–84. Several studies have also suggested similarities between
linguistic
and
musical
processing
through
shared
neural
mechanisms24,25,58,59, providing further evidence that similar transfor-
mer architectures can be useful in studying the neural encoding of
both types of stimuli. One critical point about the music transformer
used in this study is that, although the pre-trained model is publicly
available, the exact data that was used to train it has not been released,
meaning that the Bach pieces we used may have been in its training
data. Whether or not the model was trained on these stimuli does not
alter our fundamental ﬁndings, since we do not compare the model to
another music model with a different style of training, and pre-training
would likely only alter the quality of the embeddings for these stimuli,
increasing prediction correlations with neural data across the board by
reducing noise in the embeddings. This, however, suggests another
limitation of this study, which is its lack of comparison with other
music transformer models. Future work should explicitly compare this
model with other music transformer models85,86 to assess which
aspects of a model, such as architecture, size, and performance,
impact their similarity with neural responses, as they do in other
domains84,87–89. Our study extends the growing ﬁeld of AI models in neuroscience
by demonstrating how a music generative transformer model can
simulate the hierarchical and temporal aspects of musical context
processing in the brain. We found that such a model revealed distinct
differences in this processing between musicians and non-musicians,
thereby contributing a unique perspective to the understanding of
how musical expertise shapes cognitive functions and neural network
models’ role in unraveling these intricate processes. In conclusion, by
uniting generative AI models with human electrophysiology, our study
reveals the intricate, hierarchical nature of musical encoding and
demonstrates how this neural architecture is profoundly reshaped by
musical training. This work advances our understanding of auditory
cognition and highlights a path forward for using complex computa-
tional models to unravel the brain’s processing of rich, naturalistic
stimuli. Methods
Bach piano piece stimuli
Ten musical pieces from Bach’s monodic instrumental repertoire were
converted into monophonic MIDI ﬁles and segmented into 150-second
snippets. The chosen melodies were originally derived from violin
(partita BWV 1001, presto; BWV 1002, allemande; BWV 1004, alle-
mande and gigue; BWV 1006, loure and gavotte) and ﬂute (partita BWV
1013, allemande, corrente, sarabande, and bourrée angloise) scores,
and were synthesized using piano sounds with MuseScore software
(MuseScore BVBA), maintaining a constant tempo (between 47 and
140 bpm). This approach was intended to reduce the familiarity of the
pieces for expert pianists while leveraging their preferred instrument
timbre to enhance neural responses90. A list of the Bach pieces, and the
corresponding MIDI ﬁles, are publicly accessible through Dryad Digital
Repository
(https://doi.org/10.5061/dryad.g1jwstqmh)
as
well
as
online (http://www.jsbach.net). Each 150-second snippet, representing
an EEG/ECoG trial, was presented three times during the experiment,
resulting in a total of 30 trials presented in a randomized order. Calculation of musical features
Musical features were derived from the MIDI representation of the
musical pieces and included the pitch class, note duration, music piece
identity, and full pitch name. Pitch class grouped each note into its
respective chromatic category (e.g., C, C#, D), representing the pitch
irrespective of octave. Note duration was calculated as the temporal
length of each note and normalized to account for tempo variability
across the pieces. Music piece identity labeled each note with its cor-
responding musical piece based on metadata from the MIDI ﬁles. Full
pitch name combined the pitch class with octave information to assign
a unique identiﬁer (e.g., C4, G#3) for each note. These features were
analyzed to assess their separability within the embeddings generated
by the transformer model and to compare their representations across
layers. Music Transformer and Temporal Response Function
We used Musicautobot37, a public pre-trained joint encoder-decoder
multi-tasking music transformer model, to extract the contextual
music embeddings from 10 MIDI ﬁles. The music transformer model
was trained on four tasks: one for the encoder only, one for the
decoder only, and two for the joint encoder and decoder. The encoder
was trained on the bidirectional masked prediction objective, and the
decoder was trained on the next token prediction task. They were
jointly trained to do chord predictions and melody predictions from
melody and chord inputs, respectively. The data used to train the
model contained classical music from a wide variety of composers, as
well as other genres. In this study, we only use the encoder as its
bidirectional masked prediction objective is known to preserve the
most contextual information. Since the encoder is bidirectional and
does not produce causal representations, we masked future note
inputs when computing each note’s representations to align with the
causal processing of the brain. To perform dimensionality reduction
with t-SNE for visualization of a layer’s embeddings, we used the
implementation from scikit-learn91 with the default parameters (per-
plexity = 30, Euclidean distance). We applied non-negative matrix factorization (NMF) with scikit-
learn to reduce the dimensionality of the representations from 2048 to
100, ﬁtting a separate NMF transformation for each layer. We con-
ﬁrmed that 100 dimensions was sufﬁcient in two ways. First, we
Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

conﬁrmed that increasing the dimensionality to 150 produced dimin-
ishing improvement in reconstruction accuracy with the original
representations compared to a smaller size of 50 dimensions (Sup-
plementary Fig. 8). Furthermore, we found that the ﬁnal layer EEG
prediction scores were highly correlated no matter what dimension-
ality we chose between 50, 100, and 150 (Pearson r = 0.99, p = 2.4e−163
between scores from 50 and 100 dimensions, and r = 0.999, p = 7.6e
−163 between scores from 100 and 150 dimensions). We then ﬁlled the
time-steps between the notes to align these note-aligned transformer
features with the EEG or iEEG signals so they would have the same
sampling rate. We trained linear regression models to estimate the temporal
response function (TRF) using the mTRF Toolbox41 with L2 regular-
ization to predict the EEG and iEEG responses from the transformer
representations. We applied leave-one-out cross-validation (LOOCV)
with the regularization term ranging from 10−6 to 106 with an increment
of power of 10 in the log scale. We used a time-lag window of −300 to
750 ms to ﬁt the TRF models. We employed leave-one-out cross-
validation for model ﬁtting, where each model was ﬁtted repeatedly
with 9 music pieces and tested on the left-out piece. The average
correlation between the predicted neural responses and actual EEG or
iEEG signals over these cross-validation folds was reported as an
electrode’s correlation. Scalp EEG recording and preprocessing
Twenty subjects (10 male, aged between 23 and 42, M = 29) partici-
pated in the EEG experiment13,92. Ten of them were highly trained
pianists with a degree in music and at least ten years of experience,
while the other participants had no musical background. All subjects
provided written informed consent and were paid for their participa-
tion. The study protocol was approved by the CERES committee of
Paris Descartes University and was performed in accordance with the
Declaration of Helsinki. The EEG signals were recorded from 64 electrode positions,
digitized at 512 Hz using a BioSemi Active Two system. Audio stimuli
were presented at a sampling rate of 44,100 Hz using headphones. Subjects were instructed to maintain visual ﬁxation on a crosshair
centered on the screen to minimize motor activities while music was
played. We applied a bandpass ﬁlter on the normalized EEG signal
between 0.5 and 8 Hz using a Butterworth zero-phase ﬁlter. This ﬁl-
tering was applied across the response to an entire musical piece. The
frequency band was chosen following a prior analysis of the data,
which also found no signiﬁcant changes in results when the bounds
were as low as 0.1 Hz or as high as 30 Hz13. The average of the two
mastoid channels was used as the reference. The tasks were repeated
three times, so we obtained three recordings for each subject and
music piece. We ﬁtted a TRF model with all three repetitions combined
for each subject and music piece. A non-parametric shufﬂing paradigm
was used to test for electrode signiﬁcance by shufﬂing notes 100 times
and retraining TRF models for each shufﬂed set of stimuli. Electrodes
were retained which had signiﬁcant TRF prediction correlations com-
pared to the shufﬂed null distribution (p < 0.05) across all subjects,
resulting in 54 of the 64 electrodes being included in the analysis
(Supplementary Fig. 9). Example distributions of correlation scores
from shufﬂed notes are shown in Supplementary Fig. 10 for a typical
electrode, illustrating that the distributions have similar statistics over
layers and thus the noise distributions are relatively similar across
layers, though the ﬁrst layer scores have the largest variability. After each stimulus presentation, subjects were asked to report
their familiarity with the musical piece they just heard on a scale of 1 to

### 713. All subjects indicated increasing familiarity over repetitions of the

same stimuli, but there were no signiﬁcant differences between
musicians and non-musicians at each presentation (two-sample t-test,
p = 0.07, 0.16, 0.19 for the ﬁrst, second, and third presentation,
respectively) (see ref. 13 for details). Intracranial EEG recording and preprocessing
We recorded iEEG data from six subjects who were undergoing clinical
monitoring for epilepsy. The iEEG electrodes were implanted accord-
ing to clinical need for identifying epileptogenic foci, and any elec-
trodes showing signs of epileptiform discharges, as identiﬁed by an
epileptologist, were excluded. Prior to electrode implantation, all
subjects gave written informed consent for participation in research. The protocol was approved by the institutional review board of North
Shore University Hospital. The recordings were preprocessed by ﬁrst
extracting the envelope of the high-gamma band (70-150 Hz) using the
Hilbert transform93. This signal has been shown to be highly correlated
with neuronal ﬁring rates94,95. Each electrode was then downsampled
to 100 Hz and used as the neural response target for the TRF models in
the same way as for EEG responses. Electrodes were only retained for
analysis if they met two signiﬁcance criteria. The ﬁrst was a test for
acoustic responsiveness using a paired t-test between responses in the
half-second before and the half-second after acoustic onsets (p < 0.05, FDR corrected96). The second was a test for TRF encoding signiﬁcance,
requiring at least 4 out of the 13 model layers to be signiﬁcantly pre-
dictive of the electrode’s response, as judged by the p-values of the
trained TRF models (p < 0.05). These p-values were computed from a
non-parametric shufﬂing paradigm, whereby notes were shufﬂed 100
times and TRF models were trained for each shufﬂed case, producing
the null distribution of correlations for each electrode. All experi-
mental procedures were approved by the local Institutional Review
Board (IRB). Intracranial EEG Electrode Localization and Code
Each subject’s electrode locations were mapped to the subject’s indi-
vidual brain by performing co-registration between the pre-implant
and post-implant MRI scans with iELVis97. Then, each subject’s elec-
trodes were mapped to the FreeSurfer average brain98 for plotting and
inter-subject comparisons. Distance from primary auditory cortex was
deﬁned as the Euclidean distance of an electrode from posteromedial
HG (TE1.1)48 in FreeSurfer average brain space, since TE1.1 is a common
landmark of the beginning of primary auditory cortex49,50,84. For plot-
ting purposes, all subdural electrodes were snapped to the nearest
surface point and plotted on the inﬂated brain. iEEG neural recordings
were preprocessed, including high-gamma envelope extraction, with
naplib-python99. TRF models were trained with the mTRF toolbox41,
and all other analyses were performed with custom scripts in Matlab
and Python. Reporting summary
Further information on research design is available in the Nature
Portfolio Reporting Summary linked to this article. Data availability
The iEEG recordings cannot be made publicly available due to ethical
restrictions aimed at protecting the privacy and conﬁdentiality of the
human subjects involved in this study. However, the stimuli and the
EEG recordings are publicly accessible through Dryad Digital Reposi-
tory (https://doi.org/10.5061/dryad.g1jwstqmh). Source data, includ-
ing encoding model scores for the EEG and iEEG analyses are provided
with this paper. Source data are provided with this paper. Code availability
The code that can be used to extract representations for TRF training is
available on GitHub (https://github.com/naplab/Music-Transformer-
Representations)100. References
1. Leaver, A. M. & Rauschecker, J. P. Cortical representation of nat-
ural complex sounds: effects of acoustic features and auditory
object category. J. Neurosci. 30, 7604–7612 (2010). Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

2. Rogalsky, C., Rong, F., Saberi, K. & Hickok, G. Functional anatomy
of language and music perception: temporal and structural fac-
tors investigated using functional magnetic resonance imaging. J. Neurosci. 31, 3843–3852 (2011).
3. Fedorenko, E., McDermott, J. H., Norman-Haignere, S. & Kanw-
isher, N. Sensitivity to musical structure in the human brain. J. Neurophysiol. 108, 3289–3300 (2012).
4. Tierney, A., Krizman, J., Skoe, E., Johnston, K. & Kraus, N. High
school music classes enhance the neural processing of speech. Front. Psychol. 4, 855 (2013).
5. LaCroix, A. N., Diaz, A. F. & Rogalsky, C. The relationship between
the neural computations for speech and music perception is
context-dependent: an activation likelihood estimate study. Front. Psychol. 6, 1138 (2015).
6. Norman-Haignere, S., Kanwisher, N. G. & McDermott, J. H. Distinct
cortical pathways for music and speech revealed by hypothesis-
free voxel decomposition. neuron 88, 1281–1296 (2015).
7. Norman-Haignere, S. V. et al. A neural population selective
for song in human auditory cortex. Curr. Biol. 32, 1470–1484
(2022).
8. Patel, A. D. Music, Language, and the Brain (Oxford University
Press, 2010).
9. Zatorre, R. J., Chen, J. L. & Penhune, V. B. When the brain plays
music: auditory–motor interactions in music perception and pro-
duction. Nat. Rev. Neurosci. 8, 547–558 (2007).
10. Overy, K. & Molnar-Szakacs, I. Being together in time: Musical
experience and the mirror neuron system. Music Percept. 26,
489–504 (2009).
11. Koelsch, S. Brain correlates of music-evoked emotions. Nat. Rev. Neurosci. 15, 170–180 (2014).
12. Gold, B. P., Pearce, M. T., Mas-Herrero, E., Dagher, A. & Zatorre, R. J. Predictability and uncertainty in the pleasure of music: a reward
for learning?. J. Neurosci. 39, 9397–9409 (2019).
13. Di Liberto, G. M. et al. Cortical encoding of melodic expectations
in human temporal cortex. Elife 9, e51784 (2020).
14. Koelsch, S., Vuust, P. & Friston, K. Predictive processes and the
peculiar case of music. Trends Cogn. Sci. 23, 63–77 (2019).
15. Cheung, V. K. M. et al. Uncertainty and surprise jointly predict
musical pleasure and Amygdala, Hippocampus, and auditory
cortex activity. Curr. Biol. 29, 4084–4092.e4 (2019).
16. Münte, T. F., Altenmüller, E. & Jäncke, L. The musician’s brain as a
model of neuroplasticity. Nat. Rev. Neurosci. 3, 473–478 (2002).
17. Walker, K. M., Bizley, J. K., King, A. J. & Schnupp, J. W. Cortical
encoding of pitch: recent results and open questions. Hear. Res.
271, 74–87 (2011).
18. Tervaniemi, M., Just, V., Koelsch, S. & Widmann, A. E. Schröger, Pitch discrimination accuracy in musicians vs nonmusicians: an
event-related potential and behavioral study. Exp. Brain Res. 161,
1–10 (2005).
19. Proksch, S., Comstock, D. C., Médé, B., Pabst, A. & Balasu-
bramaniam, R. Motor and predictive processes in auditory beat
and rhythm perception. Front. Hum. Neurosci. 14, 578546 (2020).
20. Lenc, T. et al. Mapping between sound, brain and behaviour: Four-
level framework for understanding rhythm processing in humans
and non-human primates. Philos. Trans. R. Soc. B 376,
20200325 (2021).
21. Town, S. M. & Bizley, J. K. Neural and behavioral investigations into
timbre perception. Front. Syst. Neurosci. 7, 88 (2013).
22. Farbood, M. M., Heeger, D. J., Marcus, G., Hasson, U. & Ler-
ner, Y. The neural processing of hierarchical structure in
music and speech at different timescales. Front. Neurosci. 9,
157 (2015).
23. Williams, J. A. et al. High-order areas and auditory cortex both
represent the high-level event structure of music. J. Cogn. Neu-
rosci. 34, 699–714 (2022).
24. Fitch, W. T. & Martins, M. D. Hierarchical processing in music,
language, and action: Lashley revisited. Ann. N. Y. Acad. Sci. 1316,
87–104 (2014).
25. Asano, R., Boeckx, C. & Seifert, U. Hierarchical control as a shared
neurocognitive mechanism for language and music. Cognition
216, 104847 (2021).
26. Koelsch, S. Toward a neural basis of music perception – a review
and updated model. Front. Psychol. 2, 110 (2011).
27. Kern, P., Heilbron, M., de Lange, F. P. & Spaak, E. Cortical activity
during naturalistic music listening reﬂects short-range predictions
based on long-term experience. elife 11, e80935 (2022).
28. Fujioka, T., Trainor, L. J., Ross, B., Kakigi, R. & Pantev, C. Musical
Training Enhances Automatic Encoding of Melodic Contour and
Interval Structure. J. Cogn. Neurosci. 16, 1010–1021 (2004).
29. Boh, B., Herholz, S. C., Lappe, C. & Pantev, C. Processing of
complex auditory patterns in musicians and nonmusicians. PLoS
One 6, e21458 (2011).
30. Ono, K. et al. The effect of musical experience on hemispheric
lateralization in musical feature processing. Neurosci. Lett. 496,
141–145 (2011).
31. Kuriki, S., Kanda, S. & Hirata, Y. Effects of musical experience on
different components of MEG responses elicited by sequential
piano-tones and chords. J. Neurosci. 26, 4046–4053 (2006).
32. Vuust, P. et al. To musicians, the message is in the meter: Pre-
attentive neuronal responses to incongruent rhythm are left-
lateralized in musicians. Neuroimage 24, 560–564 (2005).
33. Boebinger, D., Norman-Haignere, S. V., McDermott, J. H. &
Kanwisher, N. Music-selective neural populations arise without
musical training. J. Neurophysiol. 125, 2237–2263 (2021).
34. Sankaran, N., Leonard, M. K., Theunissen, F. & Chang, E. F. Encoding of melody in the human auditory cortex. Sci. Adv. 10,
eadk0010 (2024).
35. Magenta, Magenta. https://magenta.tensorﬂow.org/.
36. P. Dhariwal, et al. Jukebox: A Generative Model for Music. arXiv
arXiv:2005.00341 [Preprint] (2020). http://arxiv.org/abs/
2005.00341.
37. Shaw, A., bearpelican/musicautobot, (2024); https://github.com/
bearpelican/musicautobot.
38. Rogers, A., Kovaleva, O. & Rumshisky, A. A primer in BERTology: What we know about how BERT works. Trans. Assoc. Comput. Linguist. 8, 842–866 (2021).
39. Van der Maaten, L. & Hinton, G. Visualizing data using t-SNE. J. Mach. Learn. Res. 9, 2579–2605 (2008).
40. Ding, N. & Simon, J. Z. Neural coding of continuous speech in
auditory cortex during monaural and dichotic listening. J. Neuro-
physiol. 107, 78–89 (2012).
41. Crosse, M. J., Di Liberto, G. M., Bednar, A. & Lalor, E. C. The mul-
tivariate temporal response function (mTRF) toolbox: a MATLAB
toolbox for relating neural signals to continuous stimuli. Front. Hum. Neurosci. 10, 604 (2016).
42. Hadidi, N., Feghhi, E., Song, B. H., Blank, I. A., Kao J. C. Illusions of
Alignment Between Large Language Models And Brains Emerge
From Fragile Methods And Overlooked Confounds. bioRxiv [Pre-
print] (2025). https://doi.org/10.1101/2025.03.09.642245.
43. Benjamini, Y. & Hochberg, Y. Controlling thE False Discovery Rate: A Practical And Powerful Approach To Multiple Testing. J. R. Stat. Soc.: Ser. B (Methodol. 57, 289–300 (1995).
44. Ethayarajh K. How contextual are contextualized word repre-
sentations? Comparing the geometry of BERT, ELMo, and GPT-2
embeddings. In Proc. 2019 Conference on Empirical Methods in
Natural Language Processing and the 9th International Joint Con-
ference on Natural Language Processing (EMNLP-IJCNLP),
55–65 (2019).
45. O’Connor, J., Andreas, J. What context features can transformer
language models use? arXiv preprint arXiv:2106.08367 (2021). Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

46. D’Souza, A. A., Moradzadeh, L. & Wiseheart, M. Musical training,
bilingualism, and executive function: working memory and inhi-
bitory control. Cogn. Res.: Princ. Implic. 3, 1–18 (2018).
47. Carey, D. et al. Generality and speciﬁcity in the effects of musical
expertise on perception and cognition. Cognition 137,
81–105 (2015).
48. Morosan, P. et al. Human primary auditory cortex: cytoarchitec-
tonic subdivisions and mapping into a spatial reference system. Neuroimage 13, 684–701 (2001).
49. Baumann, S., Petkov, C. I. & Grifﬁths, T. D. A uniﬁed framework for
the organization of the primate auditory cortex. Front. Syst. Neu-
rosci. 7, 11 (2013).
50. Norman-Haignere, S. V. & McDermott, J. H. Neural responses to
natural and model-matched stimuli reveal distinct computations
in primary and nonprimary auditory cortex. PLoS Biol. 16,
e2005127 (2018).
51. Tenney, I., Das, D. & Pavlick, E. BERT rediscovers the classical NLP
pipeline. Proc 57th Annual Meeting of the Association for Com-
putational Linguistics, 4593–4601 (2019).
52. Albouy, P., Benjamin, L., Morillon, B. & Zatorre, R. J. Distinct sen-
sitivity to spectrotemporal modulation supports brain asymmetry
for speech and melody. Science 367, 1043–1047 (2020).
53. Patel, A. D., Gibson, E., Ratner, J., Besson, M. & Holcomb, P. J. Processing Syntactic Relations in Language and Music: An Event-Related Potential Study. J. Cogn. Neurosci. 10,
717–733 (1998).
54. Tervaniemi, M., Sannemann, C., Noyranen, M., Salonen, J. & Pihko, E. Importance of the left auditory areas in chord discrimination in
music experts as demonstrated by MEG. Eur. J. Neurosci. 34,
517–523 (2011).
55. Peretz, I. & Coltheart, M. Modularity of music processing. Nat. Neurosci. 6, 688–691 (2003).
56. Koelsch, S. Neural Substrates of Processing Syntax and Semantics
in Music (Springer, 2009).
57. Koelsch, S., Rohrmeier, M., Torrecuso, R. & Jentschke, S. Proces-
sing of hierarchical syntactic structure in music. Proc. Natl. Acad. Sci. Usa. 110, 15443–15448 (2013).
58. Jeon, H.-A. Hierarchical processing in the prefrontal cortex in
a variety of cognitive domains. Front. Syst. Neurosci. 8, 223
(2014).
59. Slevc, L. R. & Okada, B. M. Processing structure in language and
music: a case for shared reliance on cognitive control. Psychon. Bull. Rev. 22, 637–652 (2015).
60. Levitin, D. J. & Menon, V. The neural locus of temporal structure
and expectancies in music: evidence from functional neuroima-
ging at 3 Tesla. Music Percept. 22, 563–575 (2005).
61. Patel, A. D. Language, music, syntax and the brain. Nat. Neurosci.
6, 674–681 (2003).
62. Zhang, J., Jiang, C., Zhou, L. & Yang, Y. Perception of hierarchical
boundaries in music and its modulation by expertise. Neu-
ropsychologia 91, 490–498 (2016).
63. Tervaniemi, M., Janhunen, L., Kruck, S., Putkinen, V., Huotilainen, M., Auditory proﬁles of classical, jazz, and rock musicians: genre-
speciﬁc sensitivity to musical sound features. Front. Psychol.
6 (2016).
64. Vuust, P., Brattico, E., Seppänen, M., Näätänen, R. & Tervaniemi, M. The sound of music: Differentiating musicians using a fast, musical
multi-feature mismatch negativity paradigm. Neuropsychologia
50, 1432–1443 (2012).
65. Hyde, K. L. et al. Musical training shapes structural brain devel-
opment. J. Neurosci. 29, 3019–3025 (2009).
66. Herholz, S. C. & Zatorre, R. J. Musical training as a framework for
brain plasticity: behavior, function, and structure. Neuron 76,
486–502 (2012).
67. Kraus, N. & Chandrasekaran, B. Music training for the development
of auditory skills. Nat. Rev. Neurosci. 11, 599–605 (2010).
68. Koelsch, S., Schmidt, B. & Kansok, J. Effects of musical expertise
on the early right anterior negativity: An event-related brain
potential study. Psychophysiology 39, 657–663 (2002).
69. Zatorre, R. J. Predispositions and plasticity in music and speech
learning: neural correlates and implications. Science 342,
585–589 (2013).
70. Parbery-Clark, A., Skoe, E., Lam, C. & Kraus, N. Musician
enhancement for speech-in-noise. Ear Hearing 30,
653–661 (2009).
71. Strait, D. L., Parbery-Clark, A., Hittner, E. & Kraus, N. Musical
training during early childhood enhances the neural encoding of
speech in noise. Brain Lang. 123, 191–201 (2012).
72. Kell, A. J. & McDermott, J. H. Deep neural network models of
sensory systems: windows onto the role of task constraints. Curr. Opin. Neurobiol. 55, 121–132 (2019).
73. Richards, B. A. et al. A deep learning framework for neuroscience. Nat. Neurosci. 22, 1761–1770 (2019).
74. Yamins, D. L. & DiCarlo, J. J. Using goal-driven deep learning
models to understand sensory cortex. Nat. Neurosci. 19,
356–365 (2016).
75. Cichy, R. M., Khosla, A., Pantazis, D., Torralba, A. & Oliva, A. Comparison of deep neural networks to spatio-temporal cortical
dynamics of human visual object recognition reveals hierarchical
correspondence. Sci. Rep. 6, 27755 (2016).
76. Jain. S., Huth, A. Incorporating context into language encoding
models for fMRI. Adv. Neural Inf. Process. Syst. 31 (2018).
77. Toneva, M., Wehbe, L. Interpreting and improving natural-
language processing (in machines) with natural language-
processing (in the brain). Adv. Neural Inf. Process. Syst. 32 (2019).
78. Antonello, R., Turek, J. S., Vo, V. & Huth, A. Low-dimensional
structure in the space of language representations is reﬂected in
brain responses. Adv. neural Inf. Process. Syst. 34,
8332–8344 (2021).
79. Caucheteux, C. & King, J.-R. Brains and algorithms partially con-
verge in natural language processing. Commun. Biol. 5,
134 (2022).
80. Caucheteux, C., Gramfort, A. & King, J.-R. Evidence of a predictive
coding hierarchy in the human brain listening to speech. Nat. Hum. Behav. 7, 430–441 (2023).
81. Goldstein, A. et al. others, Shared computational principles for
language processing in humans and deep language models. Nat. Neurosci. 25, 369–380 (2022).
82. Sheng, J. et al. The cortical maps of hierarchical linguistic struc-
tures during speech perception. Cereb. Cortex 29,
3232–3240 (2019).
83. Keshishian, M. et al. Joint, distributed and hierarchically organized
encoding of linguistic features in the human auditory cortex. Nat. Hum. Behav. 7, 740–753 (2023).
84. Mischler, G., Li, Y. A., Bickel, S., Mehta, A. D., Mesgarani, N. Con-
textual feature extraction hierarchies converge in large language
models and the brain. Nat. Mach. Intell., 1–11 (2024).
85. Roberts, A. et al. Magenta Studio: Augmenting Creativity with
Deep Learning in Ableton Live.
86. Thickstun, J., Hall, D., Donahue, C. & Liang, P. Anticipatory Music
Transformer. Transactions on Machine Learning Research.
(2024).
87. Schrimpf, M. et al. The neural architecture of language: Integrative
modeling converges on predictive processing. Proc. Natl. Acad. Sci. 118, e2105646118 (2021).
88. Antonello, R., Vaidya, A. & Huth, A. Scaling laws for language
encoding models in fMRI. Adv. Neural. Inf. Process. Syst. 36,
21895–21907 (2023). Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874

89. Nonaka, S., Majima, K., Aoki, S. C., Kamitani, Y. Brain
hierarchy score: Which deep neural networks are hierarchically
brain-like? IScience 24 https://doi.org/10.1016/j.isci.2021.103013
(2021).
90. Pantev, C., Roberts, L. E., Schulz, M., Engelien, A. & Ross, B. Timbre-speciﬁc enhancement of auditory cortical representations
in musicians. NeuroReport 12, 169 (2001).
91. Pedregosa, F. et al. Scikit-learn: Machine learning in Python. J. Mach. Learn. Res. 12, 2825–2830 (2011).
92. Di Liberto, G. M., Peloﬁ, C., Shamma, S. & De Cheveigné, A. Musical expertise enhances the cortical tracking of the acoustic
envelope during naturalistic music listening. Acoust. Sci. Tech. 41,
361–364 (2020).
93. Edwards, E. et al. Comparison of time–frequency responses and
the event-related potential to auditory speech stimuli in human
cortex. J. Neurophysiol. 102, 377–386 (2009).
94. Ray, S. & Maunsell, J. H. Different origins of gamma rhythm and
high-gamma activity in macaque visual cortex. PLoS Biol. 9,
e1000610 (2011).
95. Steinschneider, M., Fishman, Y. I. & Arezzo, J. C. Spectrotemporal
analysis of evoked and induced electroencephalographic
responses in primary auditory cortex (A1) of the awake monkey. Cereb. Cortex 18, 610–625 (2008).
96. Holm, S. A simple sequentially rejective multiple test procedure. Scand. J. Stat. 65, 70 (1979).
97. Groppe, D. M. et al. iELVis: An open source MATLAB toolbox for
localizing and visualizing human intracranial electrode data. J. Neurosci. methods 281, 40–48 (2017).
98. Fischl, B. et al. Automatically parcellating the human cerebral
cortex. Cereb. Cortex 14, 11–22 (2004).
99. Mischler, G., Raghavan, V., Keshishian, M. & Mesgarani, N. naplib-
python: Neural acoustic data processing and analysis tools in
python. Softw. Impacts 17, 100541 (2023).

### 100. Mischler, G. Naplab/music-transformer-representations: Release 1

(2025). doi: 0.5281/zenodo.16374911. Acknowledgements
This work was funded by the National Institutes of Health, United
States grant R01DC016234 [NM] and the National Institute on Deafness
and Other Communication Disorders, United States grant
R01DC014279 [NM]. The funders had no inﬂuence on study design,
data collection and analysis, decision to publish, or preparation of the
manuscript. Author contributions
Conceptualization: G. M., Y. A. L., N. M. Methodology: G. M., Y. A. L., S. B., A. D. M., N. M. Investigation: G. M., Y. A. L., N. M. Supervision: N. M. Writing –
original draft: Y. A. L., N. M. Writing – review & editing: G. M., N. M. Competing interests
The authors declare no competing interests. Additional information
Supplementary information The online version contains
supplementary material available at
https://doi.org/10.1038/s41467-025-63961-7. Correspondence and requests for materials should be addressed to
Nima Mesgarani. Peer review information Nature Communications thanks the anon-
ymous reviewer(s) for their contribution to the peer review of this work. A
peer review ﬁle is available. Reprints and permissions information is available at
http://www.nature.com/reprints
Publisher’s note Springer Nature remains neutral with regard to jur-
isdictional claims in published maps and institutional afﬁliations. Open Access This article is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivatives 4.0 International License,
which permits any non-commercial use, sharing, distribution and
reproduction in any medium or format, as long as you give appropriate
credit to the original author(s) and the source, provide a link to the
Creative Commons licence, and indicate if you modiﬁed the licensed
material. You do not have permission under this licence toshare adapted
material derived from this article or parts of it. The images or other third
party material in this article are included in the article’s Creative
Commons licence, unless indicated otherwise in a credit line to the
material. If material is not included in the article’s Creative Commons
licence and your intended use is not permitted by statutory regulation or
exceeds the permitted use, you will need to obtain permission directly
from the copyright holder. To view a copy of this licence, visit http://
creativecommons.org/licenses/by-nc-nd/4.0/.
© The Author(s) 2025
Article
https://doi.org/10.1038/s41467-025-63961-7
Nature Communications| (2025) 16:8874
