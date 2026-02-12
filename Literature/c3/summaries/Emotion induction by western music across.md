# Emotion induction by western music across

**Authors:** WQ
**Year:** D:20

---

## ARTICLE IN PRESS

Article in Press
Emotion induction by western music across
personality types using internet of things
technology
Scientific Reports
Received: 6 June 2024
Accepted: 20 November 2025
Cite this article as: Ru D. & Wei Z. Emotion induction by western
music across personality types using
internet of things technology. Sci
Rep (2025). https://doi.org/10.1038/
s41598-025-29934-y
Dandan Ru & Zhifang Wei
We are providing an unedited version of this manuscript to give early access to its
findings. Before final publication, the manuscript will undergo further editing. Please
note there may be errors present which affect the content, and all legal disclaimers
apply. If this paper is publishing under a Transparent Peer Review model then Peer
Review reports will publish with the final article.
https://doi.org/10.1038/s41598-025-29934-y
© The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit
to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do
not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain
permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/4.0/.

## ARTICLE IN PRESS

Emotion induction by Western music across
personality types using Internet of Things
Technology
Dandan Ru1,2 and Zhifang Wei3*
1School of International Studies, Zhengzhou University, Zhengzhou 450001, China
2Music College, Philippine Women's University, Manila 0900, Philippines
3School of Journalism and Communication, Chongqing University, Chongqing
401331, China
*Corresponding author e-mail: 20181401@alu.cqu.edu.cn
Abstract: The traditional music recommendation algorithm is an algorithm that
measures the similarity of user preferences, or an algorithm that distinguishes
types according to music styles and genres, which cannot meet the needs of
emotional induction for different personality types. It is necessary to study the
emotional induction of varying personality types by Western music based on the
Internet of Things (IoT) technology. Electroencephalogram (EEG) emotion
recognition based on IoT technology is a new research field, which involves
emotion induction, EEG feature extraction, and pattern recognition technology. According to the dimensional model of emotion, this paper selects three kinds of
Western music fragments, which can express neutral, positive, and negative
emotions. It uses these Western music materials to induce an EEG in three
emotional states. Comparing the classification effects of the eigenvectors of
different rhythms, it is found that the classification with the eigenvectors of the
beta and gamma rhythms has the highest accuracy, with the overall average
accuracy of 0.842 and 0.841, respectively, and the electrodes that provide features
under these two rhythms are in the head. The location distribution of the table was
consistent between subjects. Comparing the classification effects of different
classifiers, it is found that support vector machine (SVM) and Query-by-Committee
(QBC) are better than other classifiers, and the highest average correct rates
between subjects on different rhythms are 94.7% and 90.0%, respectively. Keywords: Emotion Induction, Internet of Things Technology, Western Music, Emotion Feature Learning, EEG

### 1. Introduction

Most of the common emotion measures are completed by the subjects'
subjective emotion label selection [1]. However, subjective scales are affected by
aspects such as word comprehension and may not fully express the true
experience of emotions. EEG signals are relatively more feasible and accurate for
emotion recognition by reflecting the activation state of human brain functions [2]. Research on user emotions has been the focus of multiple disciplines. Numerous

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

studies in neuroscience, cognitive science, and biology have shown that emotions
play a critical role in rational and intelligent behavior. A person's emotional state
not only affects an individual's attention span but also has an impact on the ability
to solve problems and make decisions [3]. Finding and calculating user emotions
has important practical application value. Adding user emotions when profiling
users can make user portraits more accurate, to provide users with better
personalized services and improve users' quality of life. Although virtual reality (VR) is increasingly recognized as an effective emotion-
inducing technology, little research has been done on the relationship between the
two. Chirico and Gaggioli [4] introduced 50 people to participate in the experiment
to compare the emotional type and valence under different conditions. The results
of the study showed that there was no significant difference in the emotions
evoked by virtual and natural conditions. How do humans distinguish between
emotions and non-emotions? Using the discriminative psychophysical MRI sparse
sampling paradigm to locate threshold responses to happy and sad acoustic stimuli, Manno et al. [5] found that threshold emotion recognition in Western music
exploits fine structural cues. Western musical anhedonia means the acquired and
selective loss of Western musical emotion. The study of Masayuki and Satoh [6]
found that there were cases in which Western music emotion was preserved even
in the presence of impaired Western music perception and recognition, findings
consistent with the findings of activation studies using PET and fMRI [7]. However,
it is necessary to explain and explain the experimental results on the basis of
understanding the characteristics and limitations of the case. Evans [8] conducts
empirical research to explore potential connections between the emotional
significance attributed to musical stimuli (expressed emotion, or external locus of
emotion) and the personal emotional response triggered by listening to music (felt
emotion, or internal locus). It is commonly assumed that the relationship between
these two emotional loci is positive, implying that the emotional experience
elicited while listening to music aligns with the emotion expressed by the music
itself. Soulier [9] aimed to study the effect of negative emotion induction in
Western music on the lexical spelling performance of children with and without
written language impairment. Studies have found that the effects of emotion vary
by spelling level and only affect the performance of children with written language
impairments. Kabrin et al. [10] I incorporated a new technology for audiovisual
induction of states of consciousness. The study aimed to demonstrate that this
technique can induce a relaxed state. He conducted two experiments using
synchronous fractals and specific configurations of Western music sequences,
which showed that a relaxed state could be induced. The study of Vlker [11]
investigated the effects of personal Western music and a researcher's pre-selected
Western music on inducing sadness and happiness. Results indicated that
participants' choice of Western music had a stronger effect on reported mood, with
sadness and happiness mainly elicited by contagion and episodic memories
associated with Western music. Wang et al. [12] used the V-A model as the
emotional perception model, selected about 1000 classic extracts from China and

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

the West, and finally extracted about 20 VITs of different data sets and other
emotional dimensions. Valence (V) dimension represents the positivity or
negativity of an emotion. Emotions with positive valence are associated with
positive feelings like happiness, joy, or love, while emotions with negative valence
are associated with negative feelings such as sadness, anger, or fear. At the same
time, Arousal (A) refers to the intensity or activation level of an emotion. Emotions
with high arousal are intense and stimulating, like excitement or anger, while low
arousal emotions are more subdued, like calmness or boredom. The results show
that the packaging method combining MaxAbsScaler preprocessing and the
recursive feature elimination algorithm based on the maximum random tree is the
best algorithm. Harmonic change detection function is a universal feature of
culture, while spectral flux is a cultural specificity of Chinese classical music. The
study also found that the pitch characteristics of Western classical music are more
significant, while the loudness and rhythm characteristics of Chinese classical
music are less significant. Sentiment analysis methods are used to evaluate
general opinions expressed in tweets about entities. Seghouani et al. [13]
proposed a new method to determine entity reputation based on the set of events
involved in the entity. Also, they proposed a new sampling method driven by a
tweet weighting metric to provide better target entity quality and summarization. To sum up, the activation of emotions is due to the involvement of all levels of the
nervous system. The initiation and occurrence of emotions are the result of the
integration of nervous systems at all levels and are the product of multiple levels
of physiology. The role of the Internet of Things (IoT) in emotional induction is becoming
increasingly important. Tallapragada et al. [14] integrate data intelligence
through IoT to track customer sentiment and provide customer behavioral insights. The proposed system uses model-based face and emotion tracking under real-use
case conditions. Wu and Zhang [15] carried out a detailed analysis and research
on the necessity, feasibility, and implementation of intelligent home voice emotion
recognition technology, introduced the definition and classification of emotion,
and proposed five primary emotions to be recognized for voice emotion
recognition based on the intelligent home environment. Then, on this basis, we
analyze the methods of obtaining emotional voice data. Building upon this
foundation, the study delves into key aspects of voice data acquisition within smart
home environments. It addresses issues like voice characteristics, acquisition
methods, and more. Additionally, the study proposes three fundamental principles
for voice text design and identifies a suitable hybrid voice recording method
tailored for smart homes. Furthermore, the study provides a comprehensive
account of the design and establishment process of an emotional voice database
for smart homes, offering insights into feature extraction challenges in speech
emotion recognition. In the realm of Western music mood prediction, the study
focuses on constructing regression models to forecast mood dimensions such as
valence (happiness level) and arousal (energy level). Hu and Yang [16] evaluated
a mood regression model built on fifteen acoustic features of five mood-related

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

aspects of Western music, with a focus on generalization across datasets. Emotion
is considered a physiological state that occurs whenever an individual observes a
transition in their environment or body. EEG rhythms, such as delta, theta, alpha,
beta, and gamma bands, have been widely studied for their role in decoding
emotional states, as they reflect different aspects of brain activity associated with
affective processing. Prior research has demonstrated that rhythm-based analysis
can enhance the accuracy of emotion recognition by capturing frequency-specific
neural patterns linked to various affective dimensions. Vempati et al. [17]
proposed an EEG rhythm–based emotion recognition approach using multivariate
decomposition and an ensemble machine learning classifier, achieving significant
improvements in classification performance by leveraging rhythm-specific
features. Such studies underscore the relevance of EEG rhythm analysis in
emotion recognition tasks and provide strong motivation for incorporating rhythm-
based features into IoT-enabled systems for music recommendation. Garg et al.
[18] have conducted extensive experiments on different Western music emotion
datasets and human emotion for impactful feature extraction, training, testing,
and performance evaluation. The above research shows that the role of the
Internet of Things in emotional induction should be further explored. A research gap exists in the current body of studies related to emotion
recognition, as there is a limited exploration of cross-cultural emotional
recognition. The existing research predominantly focuses on Western contexts,
neglecting the potential variations in emotion recognition across different cultures. Investigating the adaptability of IoT-based emotion recognition systems to diverse
cultural contexts and understanding how cultural nuances influence emotion
recognition is essential for achieving more accurate and globally applicable
emotion recognition technology. In this experiment, we selected 9 Western music clips as experimental stimuli
based on their average scores, each clip lasting approximately 11 seconds, and
repeated each stimulus 27 times. The experiment had a minimum theoretical
duration of 44.5 minutes. Notably, the experimental data revealed that emotional
arousal in Western music scenes, including joy, sadness, fear, and disgust, was
slightly higher than in videos. Subjective scales offer a straightforward and cost-
effective means of gathering individuals' self-reported experiences, making them
accessible for large-scale studies and versatile in various fields. However, their
reliance on subjective interpretation and potential biases can introduce limitations. On the other hand, an Electroencephalogram (EEG) provides an objective measure
of brain activity with high temporal resolution, making it valuable for
understanding neural processes. Yet, it has limitations in spatial resolution,
sensitivity to artifacts, and complexity in interpretation. The choice between these
methods hinges on research goals and practical considerations, with a potential
for synergy when used in conjunction to obtain a more comprehensive
understanding of both subjective experiences and underlying neural mechanisms. This study's novelty lies in the development of an Internet of Things-based emotion
induction system, which evaluates emotions in visual images using image-based

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

emotion calculation algorithms. It also contributes to the creation of an intelligent
multi-vision fusion annotation model. This research highlights a gap in current
studies related to emotion recognition, emphasizing the need to explore cross-
cultural emotional recognition and adapt IoT-based systems for diverse cultural
contexts, ultimately enhancing the universality and accuracy of emotion
recognition technology.

### 2. Principles and Methods of Emotional Induction

2.1 Principles Related to Emotion Induction
(1) The brain mechanism of emotion
Traditionally, it is believed that information from emotional stimuli is
transmitted to the limbic system, which includes the thalamus, hippocampus, and
amygdala, from where emotions are generated and expressed. Still, the limbic
system is structurally and functionally challenging [19]. The two-loop model of
emotion is shown in Figure 1.
sensory cortex
Expressway
sensory thalamus
amygdala
emotional response
emotional stimulation
Figure 1. Two-loop model of emotion
As shown in Figure 1, emotional stimuli are transmitted from the sensory
organs through the cortex of the sensory thalamus to the amygdala, which
immediately produces innate gross emotions. Simultaneously, stimuli are
transmitted from the sensory organs through the cortex of the sensory thalamus
to higher-order regions such as the frontal lobe and hippocampus, which process
information and transmit the processed information to the amygdala, producing
micro-emotions [20].
(2) The role of the auditory system in emotion induction
When responding to external stimuli, individuals automatically develop

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

emotional responses. These responses are manifested through physiological and
behavioral responses, and these responses vary from situation to situation. The
physiological material manifestation of the emotion-inducing mechanism is shown
in Figure 2. Figure 2. Physiological manifestations of emotion-inducing mechanisms
As shown in Figure 2, in contrast, vocal induction is typically performed using
the International Affective Digital System (IADS). An Affective Digital System is a
technology or software designed to recognize, interpret, and respond to human
emotions and emotional cues. These systems employ various sensors, algorithms,
and artificial intelligence to detect and analyze emotional states in individuals and,
in some cases, even respond with appropriate emotional expressions or actions. Affective digital systems find applications in areas like human-computer
interaction, virtual reality, healthcare, marketing, and more, to create more
empathetic and responsive digital experiences. They are often used in emotion
recognition, sentiment analysis, and affective computing to improve the
interaction between humans and technology. In a comparative study on the effects
of visual and auditory affective induction, physiological and behavioral affective
responses during acoustic and visual induction were used to compare the effects
of inducing media [21].
(3) User emotion recognition framework
The user's listening history contributes to the creation of a personalized song
list. To achieve real-time emotion recognition, it's imperative to initially discern
the emotions associated with each song in the user's playlist. Building upon this
concept and integrating the user's historical listening patterns, an emotion
recognition algorithm is devised to compute the user's emotional response while
listening to music. The resultant emotional states during music playback are
categorized into distinct feelings, including healing, relaxation, romance,
nostalgia, excitement, loneliness, and tranquility. Figure 3 illustrates the
framework for user emotion recognition.
external stimulus
in the brain
outside the brain
hormone secretion
brain activation
heart rate blood
pressure
hormone muscle
Chemical material
internal stimulation
emotional experience

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS............... Music Emotion Corpus
User listening behavior
Musical Emotions Are
Algorithms
User sentiment
prediction algorithm
User sentiment prediction
results
Figure 3. User emotion recognition framework
Figure 3 illustrates a framework comprising three primary components. Initially, it involves the acquisition of historical user data generated during their
song-listening activities. Typically, users compile a listening song list after each
session, which essentially forms a playlist. It's important to note that the emotional
content associated with songs in these playlists may or may not be readily
available.
2.2 Sentiment Feature Learning Based on Matrix Factorization
This section will introduce in detail how to learn the emotional representation
of songs by using the features of songs and playlists based on the association
information between playlists and songs, and the user's emotional annotation
information on playlists.
(1) Constrained non-negative matrix factorization
In recent years, the Non-negative Matrix Factorization (NMF) technique has
become a popular method for data representation [22]. It appeared to deal with
the problem that the input data dimension is too high in the real world. After
characterizing the raw data in matrix form, two non-negative matrices can be
found by the NMF technique. Their product approximates the original matrix well,
thereby simultaneously mapping features in both dimensions into a hidden space
[23]. In the context of the identified research gap, Figure 3 presents a framework
consisting of three key elements. To address the gap related to cross-cultural
emotional recognition and IoT-based systems, there is a crucial need to collect
historical data generated by users as they engage in music listening. Users
typically create playlists following their listening sessions, which serve as valuable
sources of data. It's essential to recognize that the emotional attributes of songs
within these playlists may not always be well-documented, and exploring cross-
cultural variations in emotion recognition can help enhance the understanding and
adaptation of IoT-based emotional recognition systems to diverse cultural contexts.
(
𝑎11
…
𝑎m1
…
…
…
𝑎1n
…
𝑎mn)
(1)
The goal of non-negative matrix factorization (NMF) is to approximate the
original non-negative data matrix X as the product of two lower-dimensional non-

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

negative matrices U and V. Formally, the optimization problem can be expressed
as:
min

## U, V  O = ‖X - UVT‖

F
(2)
subject toU ≥0, V ≥0, where X ∈Rm×n is the original data matrix, U ∈
Rm×k is the non-negative basis (feature) matrix, V ∈Rn×k is the non-negative
coefficient (encoding) matrix, k is the number of latent components (emotional
dimensions), and ‖ ⋅‖F denotes the Frobenius norm. The constraints U ≥0 and
V ≥0 are applied element-wise to ensure interpretability of the factorization. As shown in Equation (2), minimizing O reduces the reconstruction error
between X and its low-rank approximation UVT, thereby learning an interpretable
representation of the data in the latent emotional space. Since there is no orthogonal constraint here, what we end up with is a r
epresentation of the distribution of playlists and songs in emotional space [2
4].
(2) Constrained non-negative matrix factorization incorporating external
information
In recent years, many researchers have proposed many methods to
incorporate external information into NMF to improve the effect of matrix
factorization. This external information is features related to matrix rows or
columns [25]. External information is usually incorporated into the objective
function of NMF in the form of a regularization term.
1) Emotional label information
Regarding the emotional depiction of Western music, expert-labeled emotional
data for song lists or individual songs is integrated into the matrix decomposition
as external information. To illustrate this, let's delve into an example using
relevant formulas that involve the inclusion of expert-tagged song information. This injection process mirrors the approach of variable V, where the relevant U
component is substituted to accommodate the external emotional label data. Gv‖V - V0‖2
F
(3)
where V is the coefficient matrix from Equation (2), V0 is the emotional label
matrix, and Gv is a diagonal indicator matrix with Gv(i,i) = 1 if the ith song has
label data and 0 otherwise. As shown in Equation (3), this regularization term
constrains V to align with known emotional labels when available, with ‖ ⋅‖F
denoting the Frobenius norm. Suppose the sentiment representations learned by matrix factorization are
inconsistent with sentiment indications contained in the data. In that case, this
loss function will penalize, thereby optimizing the direction of the next step in
matrix factorization [26].
2) Relationship network
The adjacency matrix of a graph can be defined as: Wu(i,j) = {
1, if ui ∈N(ui) or uj ∈N(ui)
0, otherwise
(4)
ui is a song in the playlist and N(uj) is the k nearest neighbors of song j, as

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

shown in Equation (4). The neighbors here can be obtained by many metrics and
further built into the adjacency matrix. The loss function of the playlist relationship
network can be defined as follows: Ru = 1
2∑m
i=1 ∑m
j=1 ||U(i, * ) - U(j, * )‖2
2Wu(i,j)
= Tr(UT(Du - Wu)U)
(5)
= Tr(UTLuU)
Among them, Tr() is the trace of the matrix, Lu = Du - Wu is the Laplacian
matrix of the constructed song list graph network, Du is a diagonal matrix, and
Du(i,i) = ∑m
j=1 Wu(i,j). If two playlists are close in the graph but have different
sentiment labels, this loss function will penalize, as presented in Equation (5). The
relationship network definition of the song dimension is similar to that of playlists,
replacing the corresponding U with V.
sim(i,j) =
ViVj
||Vi||Vj||
(6)
sim(i,j) represents the similarity between playlist i and playlist j, and Vi and
Vj represent the vectorized representation of the playlist i and playlist j in the
feature space, respectively. As shown in Equation (6). Based on song co-occurrence: A playlist contains multiple songs at the same
time, and the same song may also be included in multiple playlists. Playlist
similarity is measured by calculating the number of co-occurring songs in different
playlists. The more songs that appear in the playlist at the same time, the closer
the two playlists are. Finally, the objective function of the constrained non-negative matrix
factorization algorithm incorporating external information can be expressed as:
min J = ||X - UVT||
T
F + αu
I ||Gu(U - U0)||2
F + αv
I ||Gv(V - V0)||2
F + αu
cTr(UTLuU)
+ αv
cTr(VTLvV)
(7)
Considering the actual meaning of data representation, negative numbers
cannot appear in matrices U and V.
(3) Western music emotional representation learning
Let the emotional distribution of the 𝑖th song be 𝑉, then the song 𝑖 in the k-
dimensional emotional space is expressed as: Vi = (Vi1, Vi2,…, Vik)
(8)
The V corresponding to the 𝑖th song is normalized, and the emotional
probability distribution s*
i corresponding to the song i is obtained after
normalization. The calculation formula is as follows:
s*
i = (
Vij
∑k
j=1 Vij
)
(9)
Among them, k represents the emotional space dimension. For each song, the emotion category with the highest corresponding value is
taken as the emotion category to which the song belongs, and the calculation
formula is as follows:

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

e*
i ←argmax(s*
i )
(10)
This achieves the purpose of song emotion recognition.
(4) Western music joint representation learning based on Encoder-Decoder
In this study, the encoder and decoder of the Seq2Seq are a Recurrent Neural
Network (RNN), respectively. In the RNN structure, the input of the ith layer
neuron at time m includes not only the output of the 𝑖- 1 layer neuron at time t,
but also its output at time 𝑡- 1. Assuming that the source modality is the audio
modality and the target modality is the lyrics modality, the output of the 𝑡th
hidden layer is expressed as:
ht = RNN(ht-1, XA
t )
(11)
All hidden layers of the encoder RNN are spliced together to form the output
of the encoder, which is expressed as:
ϵA→L = [h1,h2,…,hT]
(12)
T is the length of the source mode XA. The decoder translates the intermediate representation ϵA→L into the target
modality. During decoding, the output at time t depends on both the car and all
outputs before time t, which is expressed as:
p(XL) = ∏T
t=1 p(XL
t |ϵA→L, XL
1,…, XL
t-1)
(13)
The model allows the input of variable-length data. During the training
process, the training direction is to maximize the conditional probability. The
formula is as follows: XL = argmaxp(XL|XA)
(14)
In the process of modal translation and conversion, to ensure that the model
learns the joint representation of all modalities, Cycle Consistency Loss is used as
the loss function. Let the function of learning the joint representation ϵA→L
between XA and XL be fθ, and the cycle consistency loss function decomposes fθ
into two parts: encoder fθε and decoder fθd. Among them, the encoder takes the
input and outputs a joint vector ϵA⟷L, which is expressed as:
ϵA⟷L = fθε(XA)
(15)
The decoder takes ϵA→L as input and outputs XL, which is expressed as: XL = fθd(ϵA→L)
(16)
The above process is the "forward translation" between modalities, which is
the process of translating the A mode into the L mode. Back translation is the
process of restoring the L mode to the A mode after translating the A mode into
the L mode, under the influence of the A mode. Assuming that the L mode obtained
by forward translation is XL, XL and the A mode obtained by restoring is XA, the
process of restoring translation can be expressed as:
ϵL→A = fθε(XL)
(17)
XA = fθd(ϵL→A)
(18)
The direction of model training and optimization is to maximize the translation
conditional probability p(XL|XA). The loss function is divided into two parts,
including the forward translation loss L and the cycle consistency loss Lc, the

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

formula is as follows: Lt = E(lXL(XL, XL))
(19)
Lc = E(lXA(XA, XA))
(20)
The overall loss function of the model is: L = αtLt + αcLc
(21)
αt and αc are the weight hyperparameters. The specific loss function L used
is the mean square error.
(5) Spectral Angle Mapper (SAM)
The Spectral Angle Mapper (SAM) scale is an essential metric used in this
study to evaluate the similarity between spectral signatures by measuring the
angle between vectors in a multi-dimensional spectral space. SAM is particularly
valuable because it is insensitive to changes in illumination and albedo, focusing
purely on spectral shape differences, which makes it highly effective for
hyperspectral data analysis and classification. By quantifying spectral similarity
through angular measurements rather than absolute reflectance values, SAM
provides a robust way to discriminate between classes with subtle spectral
differences, thereby enhancing the accuracy and reliability of classification results
in our experiments.

### 3. Experiment on the Effect of Western Music on Emotion Induction

3.1 Experimental Design of Emotion Induction
Electroencephalography (EEG) was employed in this study as it offers a non-
invasive, real-time method to capture the brain’s electrical activity with high
temporal resolution, enabling precise detection of rapid neural responses to
musical stimuli and providing objective physiological indicators of emotional
states. In this experiment, subjects were asked to listen to Western music clips
with three different emotions and to induce an EEG in three different emotional
states. The power spectral density information under different rhythms of EEG is
a commonly used indicator for EEG analysis. In this experiment, the state of
evoked EEG will be classified based on the power spectral features of different
EEG rhythms. By comparing the classification accuracy, it is concluded which
rhythm power spectral density information is more suitable for the emotion
recognition problem. By using different classifiers for the same kind of features
and comparing the classification results, the most suitable classifier for the EEG
emotion recognition problem is deduced. All the participants were informed about
the experiment through verbal informed consent before it began. The institutional
review board (IRB) allowed this procedure to proceed since verbal consent could
be given in a study where the risk was minimal, as was the case in a non-invasive
EEG recording. No personal sensitive or identifiable data were gathered, and
participants were completely informed of the procedures involved in the study,
their rights, as well as the voluntary nature of the study. The research team
recorded the verbal consent as per the IRB guidelines.
(1) Select the target emotion
The distribution of target emotion in the pleasure-arousal emotion space is

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

shown in Figure 4. Figure 4. Distribution of target emotion in the pleasure-arousal emotion
space
As shown in Figure 4, the pleasure-arousal emotional space is divided into four
parts: high pleasure and high arousal Valence=5~9, Arousal=5~9, high pleasure
and low arousal Valence=5~9, Arousal =1~5, low pleasure and high arousal
Valence=1~5, Arousal=5~9, and low pleasure and low arousal Valence=1~5, Arousal=1~5. Select the most representative emotion type for each space,
especially choose sadness and disgust in the space with low pleasure and low
arousal. Therefore, the target emotions are composed of: "joy", "disgust", "sorrow",
"fear" and "calm".
(2) Measurement of Western Music Emotions
According to a two-dimensional emotion model, emotion can be quantified in
two dimensions (polarity and arousal). The two-dimensional model of emotions and
the two-dimensional distribution of emotions of experimental stimuli are shown in
Figure 5.

polarity
very unhappy
arousal
extra intense
very happy
very peaceful
Negative group
positive group
neutral group
arousal
polarity

(a) Two-dimensional model of emotion
(b) Two-dimensional distribution map of experimental stimulus emotion

pleasure
arousal

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Figure 5. A two-dimensional model of emotion and a two-dimensional
distribution map of emotion for experimental stimuli
As shown in Figure 5, different emotions can be represented on a two-
dimensional coordinate graph, where the abscissa is polarity and the ordinate is
arousal. Polarity represents happiness, and arousal represents calmness or
excitement. After listening to Western music, the subjects rated the polarity and
arousal, respectively, on an integer ranging from 1 to 9. A score of 1 to 9 on the
polarity dimension represents a change from "extremely unpleasant" to "very
pleasant." A scale of 1 to 9 on the arousal scale represents a change from
"extremely peaceful" to "extremely intense."
(3) Selection of experimental stimuli
132 piano pieces were randomly selected, 7- to 12-second clips were
intercepted, and the sound intensity of all clips was normalized to 65dB. Twenty-
four college students rated the emotions expressed by these pieces of Western
music based on a two-dimensional model of emotions. According to the average
score of each Western music segment, 9 Western music segments were selected
as experimental stimuli, and the durations of the selected Western music segments
were all about 11 seconds. Then, according to the distribution of emotional scores
of stimuli on the two-dimensional emotional model, the experimental stimuli were
divided into three groups, namely the neutral group, the positive group, and the
negative group. The excerpts of Western music that triggered each of the four
target emotional categories (Joy, Sadness, Fear, and Disgust) were chosen. The
selection was done in two stages. To begin with, we have generated a list of
instrumental Western music items, which had already been tested in prior
affective neuroscience and music-psychology experiments, and whose emotional
valence and arousal qualities were known. The instrumental excerpts were
selected in particular in order to prevent linguistic or cultural bias that can be
presented by lyrics. Second, an independent group of listeners (not part of the
EEG experiment) was also tested in a pilot test to ensure that every excerpt
reliably produced the desired emotion. The experiment only included those
excerpts that received similar emotional ratings among the participants. This
process was done to make sure that every emotional state was a product of a
unique and repeatable collection of Western music stimuli. Therefore, the
emotions expressed by the Western music clips in the same experimental group
can be regarded as the same. And, the polarities of Western musical stimuli were
different in the neutral group, the positive group, and the negative group. The
polarity of the neutral group is almost 0, the polarity of the positive group is
greater than 0, and the polarity of the negative group is less than 0. Paired T-test
showed that there were significant differences in polarity between any two
experimental groups, so the emotions expressed by Western music in different
experimental groups were different.
3.2 Experimental Process
14 healthy subjects who have not received any professional Western music
training participated in the experiment. Among them, there were 13 males and 1

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

female with an average age of 25.26±2.64 years. Men are right-handed, women
are left-handed. The experiment was carried out in a soundproof, shielded room. The subjects sat on a chair 110cm away from the monitor, put on headphones, and
were told the basic purpose and procedure of the experiment. The experiment is
divided into three groups, and the experimental process is shown in Figure 6.
rest
rest
rest
neutral group
each experimental
stimulus
Shuffle 27 times
positive group
each experimental
stimulus
Shuffle 27 times
Negative group
each experimental
stimulus
Shuffle 27 times
stimulus starts
stimulus ends
button to
confirm
next stimulus
question
~11s
Experimenta
l group 1
Experiment
al group 2
Experimenta
l group 3
Figure 6. Experimental flow
As shown in Figure 6, the experimental stimuli for the first set of experiments
were taken from three pieces of Western music in the neutral group. Before the
experiment, the subjects were asked to listen to the three pieces of Western music
and memorize their titles, and at the same time, fill in the scale to record the
subjects' true feelings about the emotions expressed by the Western music. During
the experiment, three Western music stimuli were played randomly and repeated
27 times. The subjects listened to the experimental stimuli with their eyes open
and attentive, and tried to avoid head and eye movements. After playing a Western
music stimulus, the subject judged the name of the Western music he or she heard
by pressing the buttons prompted by the monitor. Adding this button task can
make the subjects more focused on completing the experiment. When the subjects
completed a keystroke task, they could rest for a while before playing the next
Western music stimulus. After the first group of experiments was completed, the
subjects rested for a while before starting the second group of experiments. The
second set of experimental stimuli came from three Western music clips in the
positive group, and the experimental procedure was the same as the previous
group. After this group of experiments was completed, the subjects rested for a
while, and then began the third group of experiments. The third group of
experiments used three pieces of Western music in the negative group as
experimental stimuli, and the experimental procedure was the same as the
previous group. Since the duration of the nine Western music stimuli was all around 11
seconds and each stimulus was repeated 27 times, the entire experiment lasted
theoretically at least 44.5 minutes. To ensure that the subjects can get enough rest,
the actual duration of the experiment varies from 1.5 hours to 2 hours. Since

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

negative emotions and positive emotions are evoked by negative and positive
Western music, respectively, negative emotions tend to last longer than positive
emotions in terms of duration. To avoid the interference of negative emotions on
the induction of positive emotions, the three groups of experiments were carried
out in the order of first neutral group, then positive group, and finally negative
group.
3.3 Emotional Induction Results
In this study, we employ two classification algorithms: the Local Binary
Classifier (LBC) and the Local Naive Bayesian Classifier (LNBC). The LBC is a non-
parametric classifier that operates by analyzing local binary patterns within the
feature space, effectively capturing texture and structural information relevant to
the classification task. It is particularly useful for distinguishing subtle variations
by encoding local neighborhood relationships. The LNBC, on the other hand, is a
probabilistic classifier based on Bayes’ theorem, which assumes feature
independence and computes the posterior probability of each class. By combining
locality principles with the Bayesian framework, the LNBC provides robust
classification performance even in scenarios with limited training data. Both
classifiers were selected for their complementary strengths in handling the
dataset’s characteristics and improving overall classification accuracy. The
classification results using LBC for subject No. 1's EEG data across five different
rhythm characteristics are presented, with similar outcomes observed for other
subjects. The x-axis indicates the feature vector dimension, which corresponds to
the number of principal components. The blue histogram illustrates the proportion
of the total principal components among all components. The red dashed line
depicts the trend in the average classification accuracy during cross-validation as
a function of feature vector dimension. The error bars along the red dashed line
denote the standard deviation of cross-validation classification accuracy. Figures
7 and 8 showcase the classification accuracy obtained through the LBC approach.
(a) Delta rhythm
(b) Theta rhythm
Figure 7. Correct rate of delta rhythm and theta rhythm classification

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9

Classification accuracy/
principal component ratio
Number of principal components

0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9

Classification accuracy/
principal component ratio
Number of principal components

0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9

Classification accuracy/
principal component ratio
Number of principal components
(a)alpha rhythm
(b)beta rhythm
(c) gamma band
Figure 8. Alpha rhythm, beta rhythm and gamma rhythm classification accuracy
It can be seen from Figures 7 and Figure 8 that the classification accuracy and
the proportion of principal components increase with the increase of feature
dimensions. When the dimension of the feature vector increases from 3 to 4, the
increase in the classification accuracy gradually slows down, and the ratio of the
principal components also begins to approach 1. Therefore, if you continue to
increase the dimension of the feature vector, not only will the accuracy rate be
difficult to improve, but it may also lead to "dimension disaster". Therefore, it is
optimal to choose 3 to 4 principal components as feature vectors in this paper. The
proportion of people with the highest classification accuracy rate on the five EEG
rhythm features is shown in Table 1. Table 1. The proportion of people with the highest classification accuracy
rate on the five EEG rhythms
delta
theta
alpha
beta
gamma
LBC
0/14
1/14
0/14
6/14
7/14
LNBC
0/14
1/14
0/14
6/14
7/14
QBC
0/14
3/14
2/14
2/14
7/14
QNBC
0/14
2/14
0/14
8/14
4/14
SVM
0/14
2/14
0/14
4/14
8/14
As shown in Table 1, on the delta rhythm, none of the subjects showed the
highest classification accuracy, which further indicates that the average power of
the delta rhythm is not suitable for studying emotion recognition. Characterized
by the average power of theta rhythm or alpha rhythm, a few subjects had the
highest classification accuracy. Characterized by the average power of beta or

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

gamma rhythms, most subjects obtained the highest classification accuracy. Figure 9(a) confusion matrix performed with 3 principal components, which
illustrates the distribution of the correctly and incorrectly classified samples in the
five emotional categories (Joy, Sadness, Fear, Disgust and Calm). Figure 9(b)
confusion matrix with the use of 4 principal components, which depicts the better
classification results when the diagonal is more dominant. All the cell values are
the samples of each of the predicted classes. Figure 9. Confusion matrices for the LNBC classifier using different numbers of
principal components
Figure 10(a) presents the mean classification error of five EEG rhythms (Delta, Theta, Alpha, Beta, and Gamma). This tendency demonstrates that higher
frequency rhythms, especially Beta and Gamma, perform better in decoding with
a significantly higher degree than the lower frequency rhythms. Figure 10(b)
depicts 95% confidence Intervals of each rhythm have narrower variability in Beta
and Gamma, resulting in more consistent and stable classification across subjects. These findings are consistent with the overall observation that high-frequency
activity in the cortex provides more discriminatory information for tasks involving
emotion recognition. Figure 10. Between-subject classification accuracy comparison across EEG
rhythms
Figure 11(a) presents the mean music and video conditions arousal of the heart
rate (increase of the baseline in bpm) with the 95% confidence bounds. Music was
more likely to cause high physiological arousal among the participants than videos. Figure 11(b) depicts the Self-Assessment Manikin (SAM) arousal ratings of four

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

categories of emotions (Joy, Sadness, Fear and Disgust) during music and video
conditions. In both instances, music produced slightly higher levels of subjective
arousal compared to video, which leads to the finding that Western music
produced a stronger emotional activation in the participants. Figure 11. Comparison of emotional arousal induced by music and
video stimuli. First, the blank items were removed, and then the average classification accuracy
rate between subjects on each rhythm was calculated separately; the delta rhythm
data were not calculated. The average classification accuracy between subjects on
the four rhythms is shown in Tables 2 and 3. Table 2. Average between-subject classification accuracy on theta and alpha
rhythms
Rhythm
Theta
Alpha
Classifier

LBC
0.753+0.092
0.829+0.068
0.761+0.101
0.784+0.099
LNBC
0.747+0.112
0.841+0.097
0.743+0.111
0.774+0.131
QBC
0.772+0.112
0.812+0.086
0.745+0.119
0.814+0.115
QNBC
0.722+0.118
0.755+0.082
0.755+0.116
0.756+0.113
SVM
0.795+0.103
0.853+0.111
0.735+0.118
0.799+0.121
Table 3. Average between-subject classification accuracy on beta and
gamma rhythms
Rhythm
Beta
Gamma
Classifier

LBC
0.823+0.099
0.853+0.087
0.785+0.127
0.846+0.113
LNBC
0.838+0.095
0.822+0.083
0.795+0.112
0.831+0.093
QBC
0.836+0.113
0.884+0.121
0.833+0.145
0.901+0.189
QNBC
0.822+0.110
0.837+0.097
0.785+0.134
0.823+0.122
SVM
0.850+0.115
0.882+0.119
0.884+0.082
0.957+0.056
Tables 2 and 3 illustrate that, for each classifier, the average between-subject
classification accuracy in beta and gamma rhythms tends to be higher than in theta
and alpha rhythms. Regardless of the classifier type and feature vector dimension,
the mean between-subject average correctness rates for theta, alpha, beta, and
gamma rhythms were 0.787, 0.766, 0.842, and 0.841, respectively. A multiple

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

comparison test, at a significance level of 0.05, was conducted on the average
classification accuracy rates across subjects in the four rhythms presented in
Tables 2 and 3. The results indicate no significant difference between theta and
alpha, no significant difference between beta and gamma, but significant
differences between either theta or alpha and either beta or gamma in the average
correctness rates among subjects. This emphasizes the suitability of average
power measurements over beta and gamma rhythms for emotion classification,
aligning with previous research findings. A graphical representation of the
multiple comparison test for average classification accuracy among subjects under
each rhythm is depicted in Figure 12.
0.74
0.76
0.78
0.8
0.82
0.84
0.86
0.88
Gamma
Beta
Alpha
Theta
Accuracy
rhythm
Figure 12. Accuracy vs. Rhythm for the Local Binary Classifier (LBC) and
the Local Naive Bayesian Classifier (LNBC).s
As shown in Figure 12, the black dot in the figure represents the mean of the
average classification accuracy among subjects under a certain rhythm, and the
black line represents the 95% confidence interval of the mean. If the confidence
intervals of different rhythms overlap, there is no significant difference between
the two rhythms, otherwise, there is a significant difference. Subjects numbered 3, 4, 7, and 13 had blanks on beta and gamma rhythms,
because the number of electrodes that could provide classification information
was too small to extract enough features for classification. Excluding the above 4
subjects, for the other 10 subjects, multiple comparison tests were used to mark
the electrodes with significant differences among the three types of EEGs in the
dataset, and the positions of these electrodes that provided classification
information were recorded on the topology map. Figure 13(a) depicts the informative electrode positions of the beta rhythm,
indicated on a standard 10 20 head map. The bigger markers represent electrodes
that have a greater contribution to classification. Figure 13(b) depicts the
distribution of informative electrodes in the gamma rhythm, with more frontal and
central sites being involved. These spatial distributions explain the distribution of

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

the activity with higher frequencies across the cortical areas when processing
emotions. Figure 13. Spatial distribution of informative EEG electrodes for higher-
frequency rhythms
All heart rate data were obtained from the Biotrace+ software. The mean value
and t-test were used for analysis. The arousal degree of emotion induced by video
material and Western music material was counted, and the mean and variance
were calculated to calculate the P value. If the P value is less than 0.05, there is a
significant difference between the two. Heart rate assessment results. The SAM
assessment results are shown in Figure 14.
(a) Heart rate assessment results (b) SAM assessment results
Figure 14. Heart rate assessment results, SAM assessment results
As shown in Figure 14, the average arousal rate of Western music for the four
emotions in terms of heart rate assessment results is higher than that of the video,
but the difference is not significant. The results show that the emotional arousal
of joy, sadness, fear and disgust in Western music scenes is slightly higher than

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

that of video. The results show that the emotional arousal of joy, sadness, fear and
disgust in Western music scenes is slightly higher than that of video. According to
the statistical analysis of the SAM scale, in the arousal experiment of joy, sadness
and fear, the arousal effect of Western music is higher than that of video. And in
the arousal of fear, there is a significant difference between the arousal of Western
music scenes and the arousal of video. Video arousal was slightly higher in arousal
to disgust, but not significantly different. It was observed that increasing the
feature vector dimension beyond three or four principal components did not lead
to further accuracy improvements; instead, performance plateaued or slightly
decreased, likely due to the “curse of dimensionality,” where data sparsity in high-
dimensional spaces hampers the classifier’s ability to effectively separate classes. While the present study focused exclusively on Western music to ensure
experimental control and dataset consistency, future work will extend the
framework to include other musical traditions—such as Chinese classical music—
to examine how differences in structural features (e.g., pitch emphasis in Western
music versus loudness and rhythm prominence in Chinese music) influence
emotional perception and EEG-based classification accuracy. After the experiment, through feedback with the subjects, the results were
consistent with their actual feelings, to analyze the reasons for the better
performance of emotionally induced arousal in Western music. On the one hand,
it may be affected by the extremely strong negative emotions of fear, and the level
of arousal is higher. On the other hand, the real-time panoramic scene of Western
music has a strong sense of immersion, a stronger sense of reality, and the plot is
more attractive, so it will produce a stronger feeling. During the experiment, in
order to improve the accuracy of the experimental data, participants were
required not to move their bodies, so the design of Western music scenes removed
dynamic interaction. Although this study was conducted within a single cultural
context, we recognize that cultural differences can significantly influence
emotional perception and musical preference. As part of our future work, we plan
to extend this research to include participants from diverse cultural backgrounds,
enabling the development of IoT-based emotion recognition models that
incorporate culturally specific features and support globally applicable music
recommendation systems.

### 4. Conclusions

The research on automatic emotion recognition has important value, which
can make human-computer interaction more humanized. EEG-based emotion
recognition has an advantage over other media-based emotion recognition, which
can more objectively reflect the subject's internal emotions. This study tried to
induce three emotional states through three kinds of emotional music stimuli and
collected the corresponding evoked EEGs, and explored the recognition effects of
the average power and brain network attribute characteristics under the five EEG
rhythms on these three types of EEGs. In emotion recognition based on power
spectrum analysis, electrodes that can provide categorical information are first
selected by a multiple comparison test. The average power on these electrodes is

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

then dimensionally reduced by PCA, and three to four principal components are
extracted to form eigenvectors. The classification results show that features on
beta and gamma rhythms can provide more effective classification information. There was some inter-subject consistency in the distribution of electrode positions
that provided categorical information on beta and gamma rhythms. By comparing
the classification effects of different classifiers for the same features, it is found
that the performance of SVM and QDC is the best. The study's focus on power
spectrum analysis and electrode selection, while informative, highlights the need
to explore alternative features and analysis methods for a more comprehensive
understanding. The identified inter-subject consistency in electrode positions
underscores potential individual variability, and the reliance on specific classifiers
may limit the generalizability of classification results. In future work, we plan to
expand the scope of our study to include a broader range of emotional states, such
as anxiety and excitement, and to incorporate diverse musical genres beyond
Western music, thereby enhancing the generalizability and applicability of the
proposed music recommendation framework. Author Contributions Statement: Conceptualization, D. R.; writing, original draft preparation, D. R.; writing,
review and editing, Z. W. All authors have read and agreed to the published version
of the manuscript. Funding Statement: This study has not received any funding. Ethics approval and consent to participate: This study was conducted by the ethical standards stipulated in the 1964
Helsinki Declaration, and does not include any animal or human drug experiments. This study obtained verbal informed consent from all participants. After discussion
by the Ethics Committee of Zhengzhou University, the project research has been
approved (Project Number: 20231002). Before participating in the study, seek
verbal informed consent from each participant. Data Availability Statement: The EEG datasets generated and analyzed during the current study are
available from the corresponding author upon reasonable request. Processed
feature matrices used for classification, along with associated labels, are included
in
the
public
code
repository
at
https://github.com/15776761752-
cpu/eeg_emotion_pipeline_complete.git to enable full reproduction of the
reported results.. Conflicts of Interest: We confirmed that there is no conflict of interest. References

### 1. Chen X Y, Peng X. Emotion: A measure of Vitality. Journal of Basic Chinese

Medicine, 2022, 28(2): 165-166+176.

### 2. Li J Y, Du X B, Zhu Z L, Deng X M, Ma C X, Wang H A. Deep Learning for EEG-

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

based Emotion Recognition: A Survey. Journal of Software, 2023, 34(1): 255-276.

### 3. Wei Y Q, Chen J L, Xu X H, Hu P. Intentional Emotional Contagion in the

Perspective of Social Interaction. Journal of Psychological Science, 2023, 46(1):
130-136.

### 4. Chirico A, Gaggioli A. When Virtual Feels Real: Comparing Emotional

Responses and Presence in Virtual and Natural Environments. Cyberpsychology,
behavior and social networking, 2019, 22(3):220-226.

### 5. Manno F A M, Lau C, Fernandez-Ruiz J, Manno S H C, Cheng S H, Barrios F A. The human amygdala, disconnecting from the auditory cortex, preferentially
discriminates musical sound of uncertain emotion by altering hemispheric
weighting. Scientific Reports, 2019, 9(1):1-18.

### 6. Masayuki, Satoh. Cognitive and emotional processing in the brain of music. Japanese Journal of Neuropsychology, 2018, 34(4):274-288.

### 7. Phan KL, Wager T, Taylor SF, Liberzon I. Functional neuroanatomy of emotion:

a meta-analysis of emotion activation studies in PET and fMRI. Neuroimage.

### 2002 Jun 1;16(2):331-48.

### 8. Evans P, Schubert E. Relationships between expressed and felt emotions in

music. Musicae Scientiae. 2008 Mar;12(1):75-99.

### 9. Soulier L. Effect of emotional induction on lexical spelling of children with and

without written language disabilities. ANAE - Approche Neuropsychologique des
Apprentissages chez l'Enfant, 2018, 30(155):435-443.

### 10. Kabrin V I, Vyskochkov V S, Prudovikov I O, Tkachenko A Y. Method of

Synchronized Fractal and Musical Dynamics as a Means to Achieve Altered
States of Consciousness. Bulletin of Kemerovo State University, 2019,
21(2):395-402.

### 11. Vlker J. Personalising music for more effective mood induction: Exploring

activation, underlying mechanisms, emotional intelligence, and motives in
mood regulation. Musicae Scientiae, 2021, 25(4):380-398.

### 12. Wang X, Wang L, Xie L Y. Comparison and Analysis of Acoustic Features of

Western and Chinese Classical Music Emotion Recognition Based on V-A
Model. Applied Sciences, 2022, 12(12):587-587.

### 13. Seghouani N B, Bugiotti F, Hewasinghage M, Isaj S, Quercini G. A Frequent

Named Entities-Based Approach for Interpreting Reputation in Twitter. Data
Science and Engineering, 2018, 3(2):86-100.

### 14. Tallapragada V, Rao N A, Kanapala S. EMOMETRIC: An IOT Integrated Big

Data Analytic System for Real-Time Retail Customers' Emotion Tracking and
Analysis. International Journal of Computational Intelligence Research, 2017,
13(5(1):673-695.

### 15. Wu X, Zhang Q. Intelligent Aging Home Control Method and System for

Internet of Things Emotion Recognition. Frontiers in Psychology, 2022, 13:
882699-882699.

### 16. Hu X, Yang Y H Cross-dataset and Cross-cultural Music Mood Prediction: A

Case on Western and Chinese Pop Songs. IEEE Transactions on Affective
Computing, 2017, 8(2):228-240.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

### 17. Vempati, R. Lakhan D. S., and Rajesh. K. T, "Cross-subject emotion recognition

from multichannel EEG signals using multivariate decomposition and
ensemble learning." IEEE Transactions on Cognitive and Developmental
Systems, 2024, 17(1): 77-88.

### 18. Garg A, Chaturvedi V, Kaur A B, Varshney V, Parashar A. Machine learning

model for mapping of music mood and human emotion based on physiological
signals. Multimedia Tools and Applications, 2022, 81(4):5137-5177.

### 19. Huang X J, Zhang C, Wan H G, Zhang L C. Effect of predictability of emotional

valence on temporal binding. Acta Psychologica Sinica, 2023, 55(1):36-44.

### 20. Yang Q. The underlying mechanisms of negative affect in(cognitive)conflict

adaptation: Separated vs. integrated insights. Advances in Psychological
Science, 2022, 30(8):1844-1855.

### 21. Sambal H, Bohon C, Weinbach N. The effect of mood on food versus non-

food interference among females who are high and low on emotional eating. Journal of Eating Disorders, 2021, 9(1):1-10.

### 22. Zhang Y, Cai Y X, Wang P, Han Y, Huang Q Q. Feature extraction of single-

time spectrum non-negative matrix coding and demodulation. Chinese Journal
of Scientific Instrument, 2022, 43(12):238-247.

### 23. Zhang W B, Wang M Y, Xue X Y, Shao M Z, Wang G. A Signal Separation

Method of Mechanical Compound Fault Based on Sparse Non-negative Matrix
Factorization. Mechanical & Electrical Engineering Technology, 2022, 51(6):
63-65+81.

### 24. Semenza D C. Feeling the Beat and Feeling Better: Musical Experience, Emotional Reflection, and Music as a Technology of Mental Health. Sociological Inquiry, 2018, 88(2):322-343.

### 25. Wang Y Y, Zhao Y J. Evolution Analysis of Technological Topic: An Approach

Based on Non-negative Matrix Factorization. Library and Information Service,
2018, 62(10):94-105.

### 26. Wu D, Huang Z Y, Sheng L, Zhang M T, Jia Y Q. Emotion polarity and influence

function-based OBTM bullet-screen topic evolution. Computer Engineering
and Design, 2021, 42(10): 2956-2961.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS
