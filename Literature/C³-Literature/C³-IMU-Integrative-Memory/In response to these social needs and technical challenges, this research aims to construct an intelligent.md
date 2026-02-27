# emotion recognition with hybrid

**Year:** D:20

---

LyricEmotionNet for robust
emotion recognition with hybrid
CapsNet-memory network
architecture
Guodong Zheng1 & Juan Huang2
With the rapid development of music streaming platforms, accurate understanding of lyric emotions
has become crucial for enhancing personalized services in music recommendation systems. However,
existing methods show significant limitations in processing local emotional features and long-range
dependencies, particularly performing poorly when dealing with incomplete song information. This
paper proposes LyricEmotionNet, a hybrid deep learning architecture based on CapsNet and Memory
Networks, to address the challenges of local feature extraction and long-range dependency modeling
in lyric emotion analysis tasks. The model achieves precise capture of local emotional features through
CapsNet while utilizing Memory Networks to process long-sequence emotional dependencies,
achieving a classification accuracy of 94.29% on a dataset comprising 660 songs across six emotion
categories. Moreover, the model maintains a performance level of 90.20% in scenarios with missing
data, significantly outperforming existing methods. Through systematic comparative experiments and
ablation studies, we validate the model’s advantages in terms of accuracy and robustness. The research
findings provide new technical insights for music emotion analysis and personalized recommendation
systems, while offering valuable reference for studies dealing with incomplete textual information. Background
In the digital era, the popularization of music streaming platforms has enabled users to instantly access massive
music resources, fundamentally transforming music consumption patterns. However, faced with extensive
music libraries, users often struggle to quickly find music works that match their current emotional needs1–3. Research indicates that music, as a non-intrusive means of emotion regulation, plays a unique role in individual
emotional management and mental health maintenance4,5. Particularly in the post-pandemic era, the significant
rise in global mental health demands has made it increasingly urgent to provide precise music emotion matching
services6. In response to this demand, music platforms have developed various recommendation services. However,
current recommendation algorithms primarily rely on users’ historical listening behaviors and social network
data, with limited consideration of the emotional characteristics inherent in music works, especially the rich
emotional information carried by lyrics7–9. This technical approach leads to significant discrepancies between
recommendation results and users’ real-time emotional needs. Previous studies have confirmed that lyrics,
as an essential component of musical works, have a direct correlation with listeners’ emotional experiences10. Therefore, accurately identifying and utilizing emotional information in lyrics has become a key breakthrough
point for improving music recommendation accuracy, as shown in Fig. 1. This technological breakthrough is not only crucial for user experience but becomes even more significant
from an industry development perspective. The music industry is currently undergoing a transformation
from experience-oriented to data-driven approaches. Precise lyric emotion analysis can not only optimize the
performance of music recommendation systems but also provide valuable market insights for music creators11,12. These data can help musicians better understand listeners’ emotional needs and guide their creative direction
and marketing strategy development, thereby improving the overall efficiency of the music industry13,14. More
importantly, as the music market becomes increasingly globalized and cross-cultural music exchanges become
more frequent, music analysis and recommendation based on emotional features can break through language
barriers, offering new possibilities for cross-cultural music dissemination15.
1College of Music and Dance, Beibu Gulf University, Qin Zhou, Guangxi Zhuang Autonomous Region, China. 2Beibu
Gulf University, Qin Zhou, Guangxi Zhuang Autonomous Region, Nanning, China. email: 19978007223@163.com
OPEN
Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports

In response to these social needs and technical challenges, this research aims to construct an intelligent
system for lyric emotion analysis. Through innovative algorithm design and experimental validation, it provides
reliable technical support for music emotion recommendation while offering new ideas and methods for the
digital transformation of the music industry. This research not only addresses people’s need for emotional
resonance in the post-pandemic era but will also make positive contributions to promoting cross-cultural music
dissemination and maintaining public mental health. Related work
Music recommendation technology is undergoing profound transformation, evolving from traditional
collaborative filtering methods toward deep learning and multimodal fusion approaches. While Wang et al.’s
UPMCL method based on contrastive learning employs masking and augmentation strategies for learning music
representations and performs well with sparse interaction data, it primarily focuses on user session data learning
and cannot address emotional feature loss in lyrics16. Hou et al.’s CNN-based personalized recommendation
system achieved 95% accuracy in multiple benchmarks, but its fixed convolutional structure struggles to
adaptively handle varying degrees of lyric incompleteness10. Yuan et al.’s counterfactual music recommendation
framework effectively mitigates artist and song popularity bias through causal inference, but its reliance on
complete user-music interaction graphs leads to significant performance degradation in scenarios with
missing lyric data17. While Xu et al.’s MMusic method achieves multi-information fusion through hierarchical
structures, its simple feature concatenation approach fails to effectively capture deep emotional associations in
incomplete lyrics18. Wang et al.’s MEGAN utilizes graph attention networks to process user behavior and music
textual content, but its attention mechanism struggles to maintain stable representation learning when facing
substantial lyric text loss19. Oh et al.’s MUSE framework enhances shuffle play quality through session-enhanced
self-supervised learning but fails to consider the impact of missing lyrics on sequence representation20. In cross-
language recommendations, while Stoikos et al.’s approach based on matrix factorization and breadth-first
search makes progress in cross-language artist recommendations, it performs poorly in multilingual scenarios
with incomplete lyrics21. Regarding the core issue of music emotion analysis, existing research primarily focuses on single modality or
simple multimodal fusion approaches. Cheng et al.’s PerSong system constructs global-local similarity functions
by integrating physiological signals like visual and heart rate data, but its over-reliance on external features leads
to unstable emotion recognition when lyric information is missing22. Patel et al.’s ConCollA system combines
facial expression recognition with collaborative filtering for emotion-aware recommendations, but its simple
CNN structure struggles to establish dynamic mapping relationships between incomplete lyrics and emotions23. While Reddy et al.’s GS-RNN model based on gravity search optimization achieved high accuracy in audio signal
similarity calculations, its recursive structure is prone to gradient vanishing when processing long sequences
with missing lyrics25. Feng et al.’s FAC model improved the HR@10 metric by fusing chord, melody, and rhythm
features through user attention mechanisms, but its feature-level fusion strategy cannot adapt to dynamic
lyric information loss26. Peng et al.’s hierarchical clustering analysis method based on multi-label propagation
improved clustering effectiveness but lacks robustness considerations for label noise and missing data27. Recent
multimodal approaches including joint transformer architectures28, contrastive learning frameworks29, and
cross-modal feature fusion methods30 have shown promise in emotion recognition tasks. Magadum et al.’s
dynamic feedback mechanism innovatively introduces ELLT and DVS features, but its feedback mechanism
struggles to provide reliable guidance when substantial lyric content is missing24. Recent research indicates
that integrating emotional and contextual factors plays a crucial role in enhancing music recommendation
effectiveness31. Through in-depth analysis of existing research, we observe several key challenges in the field of music
recommendation systems, as shown in Table 1. Regarding lyric information processing, existing methods
cannot effectively handle incomplete lyric information, severely affecting recommendation system performance. Meanwhile, current network structure designs struggle to accurately capture multi-level emotional information
contained in lyrics, particularly when facing real-world scenarios with incomplete or noisy data, where model
performance often falls short. Breaking through these technical bottlenecks becomes increasingly urgent, Fig.1. Song Emotion Analysis and Recommendation. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

as research indicates music emotions significantly impact human psychological health32. From a technical
development perspective, constructing robust emotion analysis models that effectively handle incomplete lyric
information will be key to advancing music recommendation systems33. Moreover, solving these fundamental
technical issues can not only enhance recommendation system performance but also open new possibilities for
music emotion analysis and cross-cultural communication. Our contributions

### 1. Innovative Hybrid Architecture Design We propose a hybrid deep learning architecture combining Caps­

Net and Memory Networks, achieving multi-scale understanding of lyric emotions through organic fusion
of local feature extraction and long-range dependency modeling. Experimental validation shows this archi­
tecture achieves 94.29% accuracy under complete lyric conditions.

### 2. Robust Incomplete Information Processing Capability We innovatively address the problem of missing

lyric information, with the model maintaining a 90.20% performance level even when song data contains
missing information. This stability provides reliable assurance for lyric emotion analysis in practical applica­
tion scenarios.

### 3. Systematic Experimental Validation and Analysis Through comprehensive comparative experiments and

ablation studies, we quantitatively evaluate model performance and reveal the working mechanisms of dif­
ferent components, providing new insights and empirical evidence for the development of music emotion
analysis technology. Method
Problem statement
The core objective of music emotion analysis and recommendation systems is to provide personalized music
recommendations that meet users’ emotional needs based on understanding the emotional content of lyrics. To
formally describe this problem, we first construct a mathematical representation of lyric text. Let the lyric text
collection be L = {l1, l2,..., ln}, where n represents the total number of songs in the music library. Each lyric
text li is represented as a word sequence:
li = {wi1, wi2,..., wim}
(1)
where wij ∈V represents word tokens from vocabulary V, and m is the maximum sequence length. Each
word undergoes preprocessing and standardization, including removal of stop words, punctuation marks, and
lemmatization. This sequential representation preserves the temporal information of words. Define emotion space E = {e1, e2,..., ek}, where k = 6 is the number of emotional dimensions (joy, sadness,
anger, fear, love, neutral), each dimension ei representing a basic emotion type. Introduce weight coefficients:
ωi ∈[0, 1],
k
∑
i=1
ωi = 1
(2)
where ωi represents the importance weight of the i-th emotional dimension, with larger weight values indicating
higher importance of that emotional dimension in specific scenarios. In practical applications, the emotional
features of lyrics are divided into local and global levels: Authors
Application Scenario
Research Content
Potential Limitations
Cheng et
al.22
Personalized Music
Recommendation
Utilizes multimodal physiological signals (visual and heart rate) to construct
temporal sequences, proposes global-local similarity function
Over-reliance on external physiological signals,
insufficient utilization of music content features
Stoikos et
al.21
Cross-language Music
Recommendation
Uses matrix factorization and breadth-first search for cross-language artist
recommendation
Focuses only on artist-level matching, neglects
song-level emotional features
Oh et al.20
Shuffle Play Recommendation
Proposes self-supervised learning framework, optimizes recommendations
using session enhancement
Primarily focuses on play order optimization,
insufficient attention to emotional matching
Patel et al.23
Driving Scenario Emotion
Recommendation
Hybrid recommendation system incorporating facial expression recognition,
uses CNN for emotion recognition
Emotion recognition relies solely on visual features,
neglects emotional features in music content
Hou et al.10
Personalized Content
Recommendation
CNN-based deep learning recommendation system focusing on music
content feature analysis
Lacks deep analysis of lyric text, incomplete
emotional feature extraction
Magadum et
al.24
Dynamic Feedback
Recommendation
Hybrid recommendation system combining user preferences and playback
data, introduces ELLT and DVS features
Fails to consider emotional changes in music
content, lacks text-level analysis
Reddy et al.25
Entertainment-oriented
Recommendation
Recursive neural network based on gravity search optimization, focuses on
audio signal similarity
Ignores lyric text features, single-dimensional
emotional analysis
Wang et al.19
Session-based Music
Recommendation
Proposes multi-view enhanced graph attention network, integrates
heterogeneous information
Insufficient depth in emotional analysis of lyric
content
Feng et al.26
Music Content
Recommendation
Integrates chord, melody, and rhythm features using user attention
mechanism
Fails to consider lyrics’ impact on music emotion
expression
Table 1. Comparison of Related Research Methods. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

flocal: li →Rd×k
(3)
fglobal: li →Rk
(4)
where d represents the local feature dimension, which determines the model’s ability to capture local emotional
details. In the d × k dimensional matrix output by flocal, each row represents a local feature vector corresponding
to an emotional expression segment in the lyrics. The k-dimensional vector output by fglobal integrates all local
features, representing the overall emotional tendency of the lyrics. To evaluate model robustness, introduce missing rate parameter λ ∈[0, 1] to construct incomplete lyrics:
lλ
i = {wij|j ∈Sλ}
(5)
where Sλ is the index set of retained words, |Sλ| = ⌈(1 −λ)m⌉ represents the number of retained words. When
λ = 0, it represents complete lyrics, larger λ indicates more severe missing information. In user emotional state
space U = {u1, u2,..., up}, define emotional matching function:
ϕ(ui, lj) →[0, 1]
(6)
where ui ∈Rk represents the user’s current emotional state vector, lj is candidate lyrics. The output value
is a normalized matching score, 1 indicating perfect match, 0 indicating complete mismatch. In music genre
collection G = {g1, g2,..., gq}, q represents the number of predefined music genres. The genre distribution
function is defined as:
ψ(li) = {pi1, pi2,..., piq}
(7)
where each pij ∈[0, 1] and ∑q
j=1 pij = 1, representing the probability distribution of song li belonging to
each music genre. The recommendation list diversity score takes the form of information entropy:

## D(R) = −

q
∑
i=1
|Ri|
|R| log |Ri|

## |R| 

(8)
where R is the recommended song set, |R| is the recommendation list length, Ri represents the subset of songs
belonging to music genre gi. This score takes values in the interval [0, log q], larger values indicating higher
diversity. Problem 1  In today’s fast-paced life, music serves as an important medium for emotional expression and mood
regulation. Its recommendation system needs not only to accurately understand the emotional content in lyrics
but also to broaden users’ musical horizons while maintaining emotional resonance. Based on the above formal
definitions, this research proposes the following optimization objectives:
max
R
li∈R
ϕ(u∗, li) + αD(R)
s.t.

|R|
li∈R
fglobal(li) −fglobal(u∗)

≤ϵ

## |R| = K

## R ⊆L


(9)
where u∗∈Rk represents the target user’s current emotional state vector, α ∈[0, 1] is the diversity weight
coefficient, used to balance personalization and diversity. ϵ > 0 is the emotional matching threshold,
controlling the maximum deviation between recommendation results and user emotional states. K is the fixed
recommendation list length, typically valued between 10–20. The first constraint uses L2 norm to measure the
deviation between the overall emotional features of the recommendation list and user state, ensuring it does
not exceed threshold ϵ. The second constraint fixes the recommendation list size, and the third constraint limits
the recommendation candidate range. This multi-objective optimization framework ensures recommendation
quality while achieving flexible balance between personalization and diversity through adjustment of parameters
α and ϵ. Capsule Network (CapsNet): local emotion recognition
CapsNet: comparison with traditional methods
•	 Most traditional methods employ bag-of-words models or simple sequence models to process text, ignoring
the complex hierarchical relationships and interaction patterns between words, making it difficult to accu­
rately capture subtle emotional changes in lyrics. These models often view emotion recognition as a simple
classification task, using fixed feature extractors and classifiers, lacking dynamic organization and adaptive
learning capabilities for emotional features. In terms of feature processing, traditional methods typically em­
Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

ploy independent feature extraction steps, unable to achieve end-to-end joint optimization, leading to poten­
tially insufficiently discriminative extracted features.
•	 In contrast, CapsNet adaptively learns hierarchical relationships between words through dynamic routing
mechanisms, enabling precise modeling of emotional hierarchical structures in lyrics, thus better understand­
ing complex emotional expressions. The capsule structure in the model naturally possesses dynamic feature
organization capabilities, capturing the direction and intensity of emotional features through vectorized rep­
resentations, achieving flexible modeling of emotional features. In terms of optimization strategy, this method
adopts end-to-end training, simultaneously optimizing feature extraction and emotion recognition through
backpropagation, ensuring the discriminative nature of extracted features. Figure 2 shows the CapsNet network structure applied to lyric emotion analysis, progressing from CapsNet
input through ReLU Convolution and PrimaryCaps to DigitCaps in a hierarchical process, ultimately outputting
emotion analysis results. This design effectively captures hierarchical relationships between words in lyrics,
overcoming the limitations of traditional bag-of-words models in modeling complex emotional expressions. CapsNet mechanism in local emotion recognition
CapsNet captures local emotional features through hierarchical capsule structures that mirror human emotional
perception. Primary capsules detect emotional phrases and expressions within lyrics (e.g., “broken heart,” “pure
joy”), while high-level capsules aggregate these local patterns into coherent emotional representations. The
dynamic routing mechanism enables adaptive attention to emotionally relevant content, allowing the model to
focus on the most expressive parts of the lyrics while maintaining contextual relationships. CapsNet models local emotional features of lyrics through multi-level capsule structures. Given an input
sequence li = {wi1, wi2,..., wim}, after word embedding, we obtain the initial feature matrix E ∈Rm×d,
where m represents sequence length and d represents word embedding dimension. The construction process of
the primary capsule layer based on multi-head self-attention mechanism is:
u(1)
j
= squash
(
H
∑
h=1
softmax
((WQ
h Ej:j+k)(WK
h E)T
√dk
)
WV
h E
+
T
∑
t=1
[
R
∏
r=1
σ
(W(t)
r Ej:j+k + b(t)
r
√dk
)]
⊙W(1)
t Ej:j+k
+ γ
N
∑
n=1
LN
(
FFNn
(
MultiHead(Ej:j+k))))

(10)
The primary capsule construction employs multi-head attention to capture diverse emotional aspects
simultaneously. Parameter H determines the number of attention heads, allowing the model to focus on different
emotional dimensions in parallel. The depth parameters T and width parameters R control the complexity of
emotional pattern recognition, enabling the capture of subtle emotional nuances. The balancing coefficient γ
weights different architectural components for optimal emotional feature extraction. Transformation matrices
WQ
h, WK
h, WV
h ∈Rd×dk represent query, key, and value projections respectively, where dk is the attention
feature dimension. The squash function adopts an improved form to enhance gradient propagation:
squash(x) =
∥x∥2
1 + ∥x∥2 ·
x
∥x∥·
(
1 + α
d
∑
i=1
tanh(x2
i )
)
·
L
∏
j=1
σ
(wT
j x
√
d
)

(11)
The improved squash function incorporates nonlinear regulation through coefficient α, which controls the
influence of the tanh activation term. Parameter L determines the depth of normalization layers, where larger
values enhance high-order feature expression capabilities. The dynamic routing process between high-level
capsules introduces multi-dimensional emotional attention mechanisms: Fig. 2. Capsule Network Framework Structure. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

cij =
exp(bij + αij + βij)
∑
k exp(bik + αik + βik)
·
M
∏
m=1
softmax
((WQ
mu(l)
i )(WK
mu(l+1)
j
)T
√dk
+ vT
mtanh(Wm[u(l)
i; u(l+1)
j
])
)
· sigmoid
(
P
∑
p=1
FFNp
(
[u(l)
i; u(l+1)
j; |u(l)
i
−u(l+1)
j
|; u(l)
i
⊙u(l+1)
j
]))

(12)
The coupling coefficient cij represents the strength of emotional connection between capsules, enabling the
model to learn which emotional patterns should be grouped together. Parameter M controls the attention depth,
allowing multiple perspectives on capsule relationships, while P determines the complexity of inter-capsule
feature interactions through feed-forward networks. The calculation of emotional attention weights integrates
multiple context levels:
αij =
S
∑
s=1
λs
(
vT
s tanh
(
Ws[u(l)
i; u(l+1)
j
] + bs
)
·
K
∏
k=1
σ
(W(s)
k [u(l)
i; u(l+1)
j
] + b(s)
k
√dk
)
+ γs
H
∑
h=1
softmax
((WQ
h u(l)
i )(WK
h U(l))T
√dk
)
WV
h U(l)
)

(13)
The emotional attention mechanism operates at S context levels (word, phrase, and sentence levels) with
corresponding weights λs that emphasize different granularities of emotional expression. The nonlinear
transformation depth K enables the model to capture complex emotional relationships between capsule pairs. The subsequent prediction vector calculation introduces multi-level emotional modulation mechanisms:
ˆuj|i =
(
W(l)
ij u(l)
i
+
N
∑
n=1
αnFFNn(u(l)
i )
)
⊙sigmoid
(
M
∑
m=1
βm
(
W(s)
m u(l)
i
+ γm
H
∑
h=1
MultiHeadh(u(l)
i )
))
⊙
R
∏
r=1
tanh
(
W(e)
r [u(l)
i; si] + b(e)
r
)

(14)
The prediction vector incorporates emotional state modulation through vector si, which encodes contextual
emotional information. The feature extraction network employs N layers with adaptive weighting, while the
emotional modulation mechanism uses M parallel pathways and nonlinear transformation depth R to capture
complex emotional dynamics. The update rules for high-level capsules integrate residual connections and layer
normalization:
u(l+1)
j
= squash
(
n
∑
i=1
cijˆuj|i + λgj
+
P
∑
p=1
αpLNp
(
FFNp
(
n
∑
i=1
cijˆuj|i
)
+ γpgj
)
+ β
H
∑
h=1
softmax
((WQ
h
∑n
i=1 cijˆuj|i)(WK
h G)T
√dk
)
WV
h G
)

(15)
The update mechanism incorporates emotional prior knowledge through vector gj with weight coefficient λ,
while the global emotion prototypes G provide category-specific guidance through coefficient β. The residual
network depth P balances feature complexity with computational efficiency. The multi-head fusion mechanism
for local emotional features is defined as: Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

Flocal =
H
∑
h=1
αh
(
softmax
((WQ
h U(L))(WK
h U(L))T
√dk
)
WV
h U(L)
+
N
∑
n=1
βnLNn
(
FFNn
(
MultiHeadn(U(L))))
+ γ
R
∏
r=1
sigmoid
(
W(f)
r concat({u(L)
j
}nL
j=1) + b(f)
r
))

(16)
The local feature fusion employs adaptive head weighting with H attention heads, feature extraction complexity
controlled by N layers, and final nonlinear transformation depth R for comprehensive emotional pattern
integration. The temporal-related local emotional decay coefficient is given by the following formula:
γij = exp
(
−(i −j)2
2σ2
)
·
∥u(L)
i
∥· ∥u(L)
j
∥
maxp,q ∥u(L)
p
∥· ∥u(L)
q
∥
·
K
∏
k=1
sigmoid
(
wT
k [u(L)
i; u(L)
j; |u(L)
i
−u(L)
j
|] + bk
)
·
H
∑
h=1
αhsoftmax
((WQ
h u(L)
i
)(WK
h u(L)
j
)T
√dk
)

(17)
The temporal decay mechanism uses Gaussian decay controlled by variance parameter σ2 to model the intuition
that emotionally related words appearing closer together should have stronger connections. The similarity
network employs K transformation layers with H attention heads to allow dynamic override of distance-based
decay when semantically important emotional connections exist across distant word positions. Theorem 1  For any capsule sets U(l) at layer l and U(l+1) at layer l + 1, if there exists attention weight αij > τ (τ
is a preset threshold), then for any two capsules u(l)
i, u(l+1)
j, there exists an emotional transmission path Pij
such that:
∥Flocal(Pij) −ϕ(u(l)
i, u(l+1)
j
)∥≤ϵ(1 −γij)
K
k=1
exp(−λkα(k)
ij ) +
H
h=1
βh∥MultiHeadh(u(l)
i ) −MultiHeadh(u(l+1)
j
)∥2
+ δ
R
r=1
∂u(l+1)
j
∂u(l)
i
F
M
m=1
(1 −c(m)
ij )
 (18)
where the mapping function ϕ(·, ·) maps a pair of capsules to emotional feature space, ϵ and δ are constants related
to network depth L. λk represents the decay coefficient of the k-th attention layer, α(k)
ij is the corresponding
attention weight. βh is the weight coefficient of the h-th head in the multi-head attention mechanism. The
Frobenius norm ∥· ∥F is used to measure gradient relationships between capsules, c(m)
ij represents the coupling
coefficient in the m-th routing iteration. This theorem characterizes the error upper bound of local emotional
feature transmission, where error sources include temporal decay (first term), attention difference (second
term), and gradient propagation (third term). Corollary 1  For any local emotional feature sequence {ft}T
t=1 and high-level capsule set {u(L)
j
}nL
j=1, if each
feature can be captured by at least k high-level capsules with attention weights greater than τ, then there exist
constants C1, C2, C3 such that:
∥Flocal −1
T
T
t=1
ft∥≤C1
√
k
H
h=1
1 −1
H
k
i=1
α(h)
i

## + C2

L
l=1
nl
j=1
∥W(l)
j ∥2 exp
−
k
i=1 cij
k
+
C3
log(k)
M
m=1
∂Flocal
∂U(m)

F
R
r=1
(1 −γ(m)
r
)  (19)
In this inequality, C1, C2, C3 are constants related to network structure, with values monotonically increasing
with network depth L and width. α(h)
i
represents the attention weight of the h-th attention head to the i-th capsule. W(l)
j is the weight matrix of the j-th capsule in layer l, its L2 norm reflecting the intensity of feature transmission.
cij is the routing coupling coefficient, γ(m)
r
is the temporal decay coefficient. The first term characterizes the
aggregation effect of the multi-head attention mechanism, the second term describes the decay of inter-layer
feature transmission, and the third term characterizes the impact of gradient propagation on feature extraction. Notably, as the number of capturing capsules k increases, the upper bounds of the first and third terms decrease,
indicating that more capsule participation can improve feature extraction accuracy. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

Memory networks: overall emotion recognition
Memory networks: comparison with traditional methods
•	 Current mainstream text emotion analysis methods face numerous challenges when processing long text
sequences such as lyrics. Traditional models using fixed sliding window mechanisms to process sequential
information struggle to maintain long-distance emotional coherence. In terms of information storage, fixed-
size hidden state vectors limit the model’s long-term memory capacity, easily missing key emotional cues that
appear early. These methods compress all features into the same semantic space, lacking hierarchical expres­
sion capabilities for emotional features, and their fixed attention mechanisms struggle to dynamically adjust
focus based on context, constraining the depth of understanding complex emotional scenarios.
•	 Models based on Memory Networks achieve flexible modeling of long-distance emotional dependencies
through addressable external memory matrices. The hierarchical memory storage structure allows different
levels to separately preserve word-level detail features and paragraph-level thematic emotions. In the retrieval
phase, content-based dynamic addressing mechanisms can adaptively locate and extract relevant emotion­
al features based on the current context, significantly enhancing the model’s ability to understand complex
emotional scenarios. Figure 3 shows the workflow of emotion analysis and recommendation system based on Memory Networks. The
model takes preprocessed emotion label data as input and precisely extracts local details and global emotional
features from lyrics through the dynamic addressing mechanism of the external memory module. The Memory
Networks module updates memory content through encoding and addressing mechanisms, generating output
feature maps for similar song recommendations. This design effectively addresses the shortcomings of traditional
models in long-sequence emotional coherence and hierarchical feature expression. Memory networks mechanism in overall emotion recognition
Memory Networks model the overall emotional semantics of lyrics through hierarchical memory storage,
mimicking human emotional understanding processes. The key insight is that human emotional comprehension
involves both short-term emotional cues and long-term emotional context. Lower memory layers capture
detailed word-level emotional features (e.g., individual emotional words like “sad,” “happy”), while higher layers
maintain abstract emotional themes (e.g., overall song mood, emotional narrative arc). The addressable memory
mechanism allows dynamic retrieval of relevant emotional context based on current processing needs, enabling
the model to maintain coherent emotional understanding across long lyrical sequences. Memory Networks capture the overall emotional semantics of lyrics through hierarchical memory
architecture. Given a local emotional feature sequence {ft}T
t=1, construct a multi-level memory storage system
{M(l)}L
l=1, where the memory matrix at layer l is M(l) ∈RNl×dl. Here, Nl represents the number of memory
slots at layer l, typically decreasing with increasing layer number to achieve layer-wise memory abstraction; dl
is the feature dimension at the corresponding layer, used to control representation granularity. The hierarchical
memory writing process is achieved through cascaded attention: M(l)
t
= ξ(l)
t M(l)
t−1 + (1 −ξ(l)
t ) ˜M
(l)
t
˜M
(l)
t
=
Nl−1
∑
i=1
π(l)
i,tW(l)M(l−1)
t
[i]
π(l)
i,t = softmax
(sim(q(l)
t, M(l−1)
t
[i])
√
dl−1
)
q(l)
t

## = MLP

(
concat[
AvgPool(M(l−1)
t
), h(l)
t−1
])

(20)
Fig. 3. Memory Networks Framework Structure. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

The hierarchical writing mechanism enables progressive abstraction of emotional information across memory
layers. The forgetting gate ξ(l)
t
∈[0, 1] controls how much historical information to retain versus incorporating
new emotional content, balancing memory persistence with adaptability. Attention weights π(l)
i,t determine
which lower-layer memory slots contribute most to the current layer’s emotional representation, enabling
selective information propagation. The transformation matrix W(l) ∈Rdl×dl−1 implements cross-layer feature
mapping, with parameters optimized through backpropagation.
ξ(l)
t
= sigmoid
( 1
Nl
Nl
∑
j=1
KL(
M(l)
t [j]∥˜M
(l)
t [j]))
· exp
(
−λ
Kl
∑
k=1
MI(
M(l)
t, M(l−k)
t
))

(21)
The memory compression mechanism prevents redundant information accumulation while preserving
essential emotional content. KL divergence KL(·∥·) measures the information difference between current
and candidate memory states, ensuring meaningful updates. The mutual information term MI(·, ·) evaluates
statistical dependencies between memory representations at different layers, with parameter λ > 0 controlling
its influence strength and Kl representing the range of historical layers considered.
z(l)
t
=
Nl
∑
j=1
α(l)
j,tM(l)
t [j]
α(l)
j,t =
exp(ψ(l)
j,t)
∑Nl
k=1 exp(ψ(l)
k,t)
ψ(l)
j,t =
k(l)T
t
M(l)
t [j]
∥k(l)
t ∥· ∥M(l)
t [j]∥
+ βexp
(
−∥∆M(l)
t [j]∥2
2σ2
)

(22)
The temporal indexing mechanism retrieves relevant emotional context through content-based addressing. The
retrieved vector z(l)
t
∈Rdl represents the most relevant emotional context at the current time step. The scoring
function ψ(l)
j,t combines cosine similarity for content matching with a Gaussian kernel for temporal smoothness,
where parameter β > 0 balances these components and σ2 controls the temporal bandwidth. Query key vector
k(l)
t
∈Rdl encodes the current emotional retrieval intent.
ˆM
(l)
t
= LayerNorm
(
M(l)
t

## + GAT(

G(l)
t
))
G(l)
t
= {(i, j)|cos(M(l)
t [i], M(l)
t [j]) > θ(l)}
GAT(i, j) = LeakyReLU
(
aT [WM(l)
t [i]∥WM(l)
t [j]]
)

(23)
The collaborative update mechanism enables memory slots to exchange information when they contain similar
emotional content. Graph structure G(l)
t is dynamically constructed based on cosine similarity threshold
θ(l) ∈[0, 1], connecting memory slots that capture related emotional patterns. The Graph Attention Network
(GAT) facilitates information flow between connected slots, with attention vector a ∈R2dl and transformation
matrix W ∈Rdl×dl learning optimal information exchange patterns.
c(l)
t
=
Nl
∑
i=1
γ(l)
i M(l)
t [i]
γ(l)
i
= softmax
(entropy(M(l)
t [i])
τ (l)
+ η(l)coverage(i, t)
)
coverage(i, t) =
t
∑
s=1
log
(
1 +
Nl
∑
j=1
exp(
−∥M(l)
s [i] −M(l)
s [j]∥2))

(24)
Memory distillation extracts the most informative emotional concepts from each layer. The concept vector
c(l)
t
∈Rdl represents distilled emotional knowledge at layer l. The distillation weight γ(l)
i combines entropy-
based information content evaluation with coverage-based usage tracking. Temperature parameter τ (l) > 0
controls the smoothness of the selection distribution, while coefficient η(l) > 0 balances information richness
with temporal utilization patterns. L(l)
contrast = −log
exp(sim(c(l)
t, c(l+1)
t
)/κ)
∑N
n=1 exp(sim(c(l)
t, c(l+1)
n
)/κ)
sim(x, y) =
xT y
∥x∥· ∥y∥+ λMI(x, y)

(25)
Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

Contrastive learning ensures consistent emotional representations across hierarchical layers. The loss function
encourages similar emotional concepts between adjacent layers while maintaining distinctiveness from unrelated
concepts. Temperature coefficient κ > 0 controls the concentration of the similarity distribution, with smaller
values producing sharper contrasts. The similarity function combines cosine similarity with mutual information,
balanced by weight coefficient λ > 0.
r(l)
t
=
L
∑
k=1
ω(l)
k,tU(k,l)c(k)
t
ω(l)
k,t = softmax
(
energy(c(l)
t, c(k)
t
) + δ(l)MI(M(l)
t, M(k)
t
)
)
energy(x, y) = vT tanh
(
W1x + W2y + b
)

(26)
Cross-layer routing enables information integration across all memory hierarchy levels. The routed representation
r(l)
t
∈Rdl combines emotional concepts from all layers with adaptive weighting. Transformation matrix
U(k,l) ∈Rdl×dk achieves feature alignment between different dimensional spaces. The routing weight ω(l)
k,t
combines energy-based compatibility with mutual information measures, controlled by coefficient δ(l) > 0.
e =
L
∑
l=1
ϕl
(
LayerNorm(
r(l)
T + FFN(r(l)

## T )))

ϕl = sigmoid
( 1
T
T
∑
t=1
MI(M(l)
t, c(l)
t )
)

(27)
The final global emotion representation e ∈Rd integrates emotional features from all memory layers with
adaptive weighting. Layer weight ϕl is computed through accumulated mutual information between memory
states and concept vectors, reflecting each layer’s information contribution. The feed-forward network FFN
performs nonlinear transformation with two linear layers and ReLU activation, ensuring comprehensive
emotional pattern integration. Theorem 2  Given a memory network with L layers, for any local emotional feature sequence {ft}T
t=1 of length
T, if the memory capacity at each layer satisfies Nl ≥log(T/ϵl), where ϵl is the approximation error threshold
for layer l, then the error of the global emotional representation satisfies:
∥e −E[e|{ft}]∥≤
L
l=1
ϕl
√Nl
Kl
k=1
exp
−λkMI(M(l)
T, M(l−k)
T
)
+




L
l=1
∥U(l)∥2
F
T
t=1
1 −1
Nl
Nl
i=1
γ(l)
i

+

minl Nl
L
l=1

∂e
∂M(l)
T

F
Kl
k=1
(1 −ξ(l)
k )
 (28)
This theorem establishes error bounds for global emotion representation accuracy. The first term reflects memory
capacity impact, the second term describes information transmission loss, and the third term characterizes
gradient propagation stability. The memory capacity threshold ensures sufficient storage space, while the mutual
information weight coefficient λk decays with layer distance, reflecting diminishing remote dependencies. Corollary 2  If the network satisfies hierarchical constraint conditions: (1) Memory capacity decays exponential­
ly with layer number: Nl = N1/2l−1; (2) Feature dimension increases linearly with layer number: dl = l · d1;
(3) At least kl memory slots in each layer have utilization rates exceeding threshold τl, then there exist constants
C1, C2 such that:
∥e −ϕ({ft})∥≤C1
L
∑
l=1
2l−1
N1
(
1 + l
L
L
∑
h=1
∥U(h,l)∥2
)

## + C2

L
∑
l=1
l · d1 exp
(
−kl
Nl
Nl
∑
i=1
coverage(i, T)
)
 (29)
This corollary demonstrates that the error upper bound is inversely proportional to memory capacity and inter-
layer connection strength. The first term characterizes capacity-dependent error, while the second term reflects
memory utilization efficiency impact on overall performance. LyricEmotionNet algorithm description
Figure 4 presents the complete architecture and data flow of LyricEmotionNet, illustrating the precise interface
between CapsNet and Memory Networks modules. The system processes lyric emotion analysis through a
carefully designed pipeline that addresses both local feature extraction and global emotion modeling while
supporting the broader recommendation framework. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

CapsNet to Memory Networks Interface: The critical interface between the two core modules operates
through a systematic transformation process. The DigitCaps layer outputs local emotional features as a three-
dimensional tensor with shape [batch_size, num_caps, cap_dim], where num_caps = 64 represents the
number of primary capsules and cap_dim = 32 denotes the capsule dimension. This output undergoes a key
interface transformation involving: (1) tensor reshaping from R64×32 to R2048 through flattening operations;
(2) linear projection via learned transformation matrix Wproj ∈R2048×768 to match Memory Networks input
requirements; (3) temporal sequence construction by reshaping the projected features into [batch_size, 1, 768]
format suitable for hierarchical memory processing. This interface design ensures seamless information flow
while preserving the rich local emotional representations captured by CapsNet for subsequent global modeling
by Memory Networks. Fig. 4. LyricEmotionNet Complete Architecture and Data Flow Overview. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

Algorithm 1. Lyrics Emotion-based Song Recommendation Algorithm
Time Complexity: The time complexity of this algorithm primarily consists of four parts: lyrics
embedding, emotional feature extraction, emotional matching degree calculation, and recommendation
generation. The computational complexity of lyrics embedding is O(m · d), while CapsNet and Memory
Networks have computational complexities of O(m · d2) and O(d3) respectively. The computational
complexity of emotional matching degree is O(k), and the time complexity of recommendation list
generation is O(|L∗| log K). Taking all these into account, the overall time complexity of the algorithm
is: O(|L| · (m · d + m · d2 + d3) + |U| · |L∗| · k + |L∗| log K) where |L| is the size of the song library, |U| is
the number of users, |L∗| is the size of the candidate song set, and K is the length of the recommendation list. Space Complexity: The space complexity mainly consists of storage for lyrics embedding matrix,
emotional feature matrix, and user emotional states. The space complexity of the lyrics embedding
matrix is O(|L| · m · d), emotional feature matrix is O(|L| · m · d · k), user emotional state storage is
O(|U| · k), and recommendation list space complexity is O(K). Therefore, the overall space complexity
is: O(|L| · m · d + |L| · m · d · k + |U| · k + K). Where |L| is the size of the song library, |U| is the number
of users, m is the maximum lyrics length, d is the word embedding dimension, k is the number of emotional
dimensions, and K is the length of the recommendation list. Experiments
Dataset and experimental parameters
Song Information and Lyrics: This research utilizes a music dataset containing 660 songs, designed to support
research in music emotion analysis and recommendation systems. The dataset encompasses six primary emotion
categories: joy (120 songs), sadness (115 songs), anger (105 songs), fear (98 songs), love (112 songs), and neutral
(110 songs), providing balanced representation across emotional states. Each song entry includes complete
lyrical content, artist information, genre classification (popular music 40%, rock 25%, folk 20%, others 15%),
and associated metadata. The emotion annotation process involved three independent music psychology experts
who evaluated lyrical content using a five-point Likert scale, with final labels determined through majority
consensus voting and achieving substantial inter-annotator agreement (Fleiss’ K = 0.76). Lyrical characteristics
show mean length of 78±32 words per song (range: 15–156 words) with vocabulary size of 8,247 unique terms
Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

after preprocessing. The lyrics were collected through public platforms (Spotify and SoundCloud) and converted
from audio to text using speech recognition technology, followed by systematic preprocessing including lowercase
conversion, punctuation removal, and stop-word filtering using NLTK. Word embeddings were initialized with
pre-trained GloVe-300d vectors for semantic representation. All lyrical content is in English, representing a
limitation for cross-linguistic applications. The TextCNN baseline employed embedding dimension of 300,
convolutional filter sizes of [3,4,5], 100 filters per size, dropout rate of 0.5, and Adam optimizer with learning rate
of 0.001. The diversity of this dataset makes it a valuable resource for studying the relationship between lyrical
emotions and listener preferences, providing a foundation for developing personalized music recommendation
systems, emotion analysis models, and other lyrics-based natural language processing applications. The experiments were conducted on a server equipped with an Intel Xeon E5-2698 v4 @ 2.20GHz CPU
(20 cores, 40 threads), 4 NVIDIA Tesla V100 GPUs (32GB memory each), and 256GB RAM. The model was
implemented using PyTorch 1.10.0 framework, employing mixed-precision training to optimize memory
usage. Based on preliminary experimental results, Table 2 lists the optimal parameter configuration for
LyricEmotionNet, which was tuned on the validation set using Bayesian optimization. The model employs a two-stage training strategy: the first stage involves pre-training the CapsNet and
Memory Networks components separately, while the second stage performs end-to-end joint fine-tuning. During training, mixed-precision computation and gradient accumulation are utilized to optimize memory
usage. A cosine annealing learning rate scheduler with warmup is employed, and early stopping is determined
based on comprehensive performance metrics on the validation set. Experimental results
To comprehensively evaluate LyricEmotionNet’s performance in lyrics emotion analysis, this study designed a
series of comparative experiments. The evaluation adopted three core metrics: classification accuracy (ACC),
loss function value (Loss), and Area Under the Receiver Operating Characteristic curve (AUC). ACC directly
reflects the model’s classification effectiveness, demonstrating the accuracy of prediction results; Loss describes
the optimization characteristics during the training process, reflecting convergence stability; AUC quantifies
the model’s ability to distinguish between different emotion categories, assessing classification reliability. These
metrics characterize model performance from different perspectives, collectively forming a complete evaluation
system. Parameter Name
Value
Parameter Name
Value
General Configuration
Batch Size

Maximum Sequence Length

Word Embedding Dimension

Number of Emotion Categories

Learning Rate
2e-4
Weight Decay
1e-5
Optimizer
AdamW
Training Epochs

CapsNet Configuration
Primary Capsules

Capsule Dimension

Routing Iterations

Number of Attention Heads

Convolution Kernel Size

Convolution Stride

Feature Dimension d

Dropout Rate
0.1
Attention Temperature τ
0.1
Activation Function
GELU
Local Window Size

Capsule Compression Ratio
0.5
Memory Networks Configuration
Memory Layers L

Base Memory Slots N1

Memory Dimensions dl
[256,384,512,768]
History Window Size Kl

Memory Compression Rate
0.5
Mutual Information Weight λ
0.5
Number of Attention Heads H

GAT Threshold θ(l)
0.3
Minimum Memory Utilization
0.1
Temperature Parameter τ (l)
0.5
Training Strategy
Learning Rate Warmup Steps

Gradient Clipping Threshold
1.0
Learning Rate Decay Factor
0.1
Decay Steps
30 epochs
Early Stopping Patience

Validation Frequency
500 steps
Label Smoothing Factor
0.1
Mixed Precision Level
O2
Loss Weight (Local)
0.4
Loss Weight (Global)
0.6
Gradient Accumulation Steps

Random Seed

Data Augmentation
Random Masking Rate
0.15
Random Replacement Rate
0.1
Random Deletion Rate
0.1
Maximum Perturbation Length

Table 2. LyricEmotionNet Model Experimental Parameter Configuration. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

In this study’s comparative experiments, TextCNN was selected as the baseline model for in-depth analysis
of emotional features in lyrics text. Emotional expressions in lyrics typically exhibit local aggregation, with
specific emotions often concentrated in particular word groups or phrases. TextCNN, through its local receptive
field mechanism, can effectively capture these local semantic patterns, thereby revealing the inherent patterns
of emotional features. Research has shown that when processing text classification tasks with significant local
features, CNN’s multi-layer convolution structure naturally constructs hierarchical feature representations,
which highly aligns with the progressive expression of emotions in lyrics. Therefore, TextCNN serves not only
as a performance benchmark but also provides an important reference framework for understanding the role of
local feature extraction mechanisms in lyrics emotion analysis. Model lyrics emotion analysis results
Figure 5 demonstrates the performance of different models under complete lyrics information conditions. The
LyricEmotionNet model ultimately achieved a classification accuracy of 94.29%, showing a 15.88 percentage
point improvement over the baseline TextCNN model’s 78.41%. Removing CapsNet resulted in an 8.32 percentage
point accuracy drop (from 94.29% to 85.97%), while removing Memory Networks caused a 3.36 percentage
point decline (from 94.29% to 90.93%). The disproportionate impact of CapsNet removal suggests its critical
role in capturing local emotional patterns within lyrics segments. The accuracy degradation pattern indicates
that CapsNet’s capsule routing mechanism is particularly effective at identifying spatially-related emotional
features that occur in concentrated word clusters, which aligns with the characteristic expression patterns
found in emotional lyrics where sentiment-bearing phrases tend to cluster together. The Memory Networks
component demonstrated its importance through a more moderate but consistent performance impact. The
3.36 percentage point accuracy reduction upon its removal suggests that while individual emotional expressions
can still be identified without long-range dependency modeling, the overall contextual understanding suffers. This pattern becomes more pronounced when examining the loss convergence characteristics, where the model
without Memory Networks showed 43.7% higher final loss (0.1796 vs 0.1250), indicating reduced optimization
efficiency in handling sequential emotional transitions within complete lyrics. In terms of the training process, LyricEmotionNet exhibited excellent learning efficiency and stability: maintaining rapid improvement in
the early stage (0–20 epochs), entering a steady improvement phase in the middle stage (20–35 epochs), and
still showing optimization potential in the late stage (35–50 epochs). In contrast, the model lacking Memory
Networks showed insufficient performance in handling long-range dependencies, while the version without
CapsNet displayed obvious deficiencies in local emotional feature extraction. The baseline TextCNN model
not only achieved lower final performance but also showed notably inferior convergence speed, reaching its
performance bottleneck after 25 epochs. The loss function changes during training further verified the model’s superiority. As shown in Fig. 6, LyricEmotionNet’s final loss value converged to 0.1250, significantly outperforming other comparative models. The loss value increased to 0.1796 after removing Memory Networks, further rose to 0.2501 after removing
CapsNet, while the baseline TextCNN model reached a loss of 0.3579. The loss progression reveals differential
impacts of each component on optimization dynamics. CapsNet removal resulted in a 100.1% loss increase (from
0.1250 to 0.2501), substantially higher than the 43.7% increase from Memory Networks removal (from 0.1250 to
0.1796). This disparity indicates that CapsNet’s absence creates more fundamental optimization challenges, likely
Fig. 5. Comparative Results of Model Performance Accuracy in Lyrics Emotion Analysis. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

due to the loss of hierarchical feature representation capabilities essential for capturing local emotional nuances. The steeper loss degradation suggests that without capsule-based feature routing, the model struggles more
severely with discriminating between closely-related emotional states that require fine-grained local pattern
recognition. LyricEmotionNet showed the fastest descent rate in the early training stage while maintaining a
steady optimization trend throughout the training process. Notably, even after 20 epochs, the complete model’s
loss curve maintained a slow but stable descent, indicating sustained optimization capability. In contrast, other
models showed significant oscillations at similar stages, with considerably slower loss descent rates. These
loss convergence characteristics corroborate the aforementioned accuracy analysis, further demonstrating the
stability and effectiveness of the proposed hybrid architecture in learning lyrics emotional features. The model’s classification discrimination capability was further validated through ROC curves and AUC. As shown in Fig. 7, LyricEmotionNet achieved an AUC value of 0.9210, significantly outperforming other
comparative models. ROC curve analysis indicated that the complete model could achieve high true positive
rates even in low false positive rate regions, demonstrating excellent classification discrimination ability. The
AUC degradation patterns provide insights into each component’s role in classification discrimination. CapsNet
removal resulted in a 14.4% AUC reduction (from 0.9210 to 0.7884), while Memory Networks removal caused an
8.2% decrease (from 0.9210 to 0.8457). The larger AUC impact from CapsNet removal suggests that local feature
extraction capabilities are more critical for maintaining classification boundaries between emotion categories. This finding indicates that CapsNet’s dynamic routing mechanism provides superior discrimination power for
emotions that manifest through localized linguistic patterns, enabling the model to maintain high specificity
across different emotional classes. After removing the Memory Networks and CapsNet components, the model’s
AUC values decreased to 0.8457 and 0.7884 respectively, while the baseline TextCNN model achieved an AUC of
only 0.7326. From the ROC curve morphology, LyricEmotionNet’s curve is overall closer to the upper-left corner
and shows the largest gap from the random classifier (AUC=0.5), further confirming the hybrid architecture’s
outstanding performance in balancing the recognition of different emotion categories, corroborating the
conclusions from the previous accuracy and loss analyses. To further understand CapsNet’s interpretability in capturing local emotional features, Fig. 8 presents a detailed
analysis of capsule specialization across different emotion categories. The bar chart shows average activation
levels for each emotion category, while the red line indicates specialization consistency percentages. Higher
activation levels (blue bars) indicate stronger capsule responses to specific emotions, while higher consistency
percentages (red line) reflect the stability of capsule specialization patterns. The analysis reveals distinct activation
patterns that explain CapsNet’s effectiveness in emotion classification. Anger emotions demonstrate the highest
average activation level (0.83) with strong specialization consistency (86.83%), indicating that CapsNet develops
highly specialized capsules for detecting aggressive and intense emotional expressions typical in anger-related
lyrics. Conversely, neutral emotions show the lowest activation (0.64) and consistency (58.9%), reflecting the
inherently ambiguous nature of neutral emotional content and the corresponding difficulty in developing
specialized detection mechanisms. Joy and Love emotions exhibit similar activation patterns (0.81 and 0.80
respectively), suggesting overlapping positive emotional features that CapsNet learns to distinguish through
subtle activation differences. The consistent specialization percentages above 70% for most emotion categories
(except Neutral) demonstrate CapsNet’s ability to develop stable, interpretable feature representations that align
with human understanding of emotional expression patterns in lyrics. Fig. 6. Comparative Results of Model Performance Loss in Lyrics Emotion Analysis. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

Model
Training Time (min)
Inference (ms)
GPU Memory (GB)
Throughput (samples/s)
LyricEmotionNet

8.7
12.3

w/o Memory Networks

6.2
8.9

w/o CapsNet

4.8
7.1

TextCNN (Baseline)

2.1
3.2

Table 3. Computational Resource Requirements and Efficiency Comparison. Fig. 8. Capsule Specialization Analysis. Fig. 7. Comparative Results of Model Performance ROC in Lyrics Emotion Analysis. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

Table 3 presents the computational resource requirements for different model configurations on the 660-song
dataset. LyricEmotionNet requires approximately 4× longer training time compared to TextCNN baseline, with
correspondingly higher GPU memory consumption and reduced inference throughput. CapsNet contributes
approximately 65% of the computational overhead through iterative dynamic routing operations, while
Memory Networks account for the remaining 35% via multi-head attention mechanisms. The computational
cost increase corresponds directly to performance improvements: the 15.88 percentage point accuracy gain and
superior robustness under missing data conditions justify the additional resource requirements for applications
prioritizing classification reliability over processing speed. Experimental analysis results with missing lyrics
Missing Data Simulation Methodology: To systematically evaluate model robustness under incomplete lyric
scenarios, we implemented a controlled missing data simulation approach. Figure 9 illustrates the specific
methodology employed to generate incomplete lyrics with varying missing rates. The simulation process involves
random word-level deletion where words are uniformly selected and replaced with [MASK] tokens to simulate
real-world data incompleteness scenarios. For a given missing rate λ, approximately λ × word_count words
are randomly selected and masked from each lyric sequence. This approach ensures statistical consistency while
maintaining the sequential structure of lyrics, enabling fair comparison of model robustness across different
incomplete data conditions. To evaluate model robustness in practical application scenarios, this study systematically analyzed model
performance under different lyrics missing rates. As shown in Fig. 10, model performance exhibited varying
degrees of decline as the lyrics missing rate increased. Under complete lyrics conditions, LyricEmotionNet
achieved 95.26% accuracy and maintained 80.48% performance even with a 50% missing rate, demonstrating
strong robustness. Based on the performance degradation curve analysis, this study selected 25% as the typical
missing rate for in-depth comparison. This selection was based on the following considerations: at 25% missing
rate, LyricEmotionNet achieved 90.87% accuracy, only 4.39 percentage points lower than with complete lyrics,
while other models showed significant degradation - the model without Memory Networks dropped to 74.21%,
the model without CapsNet fell to 74.85%, and the baseline model plummeted to 35.08%. This critical point
clearly demonstrates the capability differences between models in handling incomplete information, while also
approximating common lyrics missing scenarios in real applications, bearing significant practical implications. The missing data scenario provides deeper insights into component-specific functionality. Under 25%
missing conditions, the accuracy degradation patterns reveal differential robustness characteristics. Memory
Networks removal resulted in an 18.3% relative performance decrease (from 90.87% to 74.21%), substantially
exceeding the 4.6% relative decrease observed under complete data conditions (from 94.29% to 90.93%). This amplified degradation indicates that Memory Networks become increasingly critical when dealing with
incomplete sequential information, as the component’s ability to maintain contextual coherence across gaps
becomes essential for preserving overall emotional understanding. Conversely, CapsNet removal showed a
17.6% relative performance decrease under missing conditions (from 90.87% to 74.85%), compared to the 8.8%
decrease under complete conditions. While both components show increased importance under information
scarcity, the Pattern suggests that Memory Networks exhibit greater sensitivity to information completeness, Fig. 9. Missing Data Simulation Methodology: Systematic Text Processing for Model Robustness Analysis. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

supporting the hypothesis that long-range dependency modeling becomes more crucial when dealing with
fragmented textual input. As shown in Fig. 11, LyricEmotionNet demonstrated excellent learning capability and stability under 25%
lyrics missing conditions. Starting from an initial accuracy of 45.0%, the model reached a performance level of
90.2% after 50 training epochs. The training process exhibited distinct three-stage characteristics: rapid learning
and improvement in the first 20 epochs, steady improvement during epochs 20–35, and maintaining a slow
but continuous optimization trend after epoch 35. In contrast, other models showed obvious performance
improvement limitations: the model without Memory Networks improved from 35.0% to 75.5%, the version
without CapsNet from 30.0% to 73.1%, and the baseline model only from 25.0% to 38.4%, all encountering
significant performance bottlenecks in the later training stages. These results fully validate LyricEmotionNet’s
Fig. 11. Model Performance Comparison under Missing Data Conditions. Fig. 10. Selection of Data Missing Ratio. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

superiority in handling incomplete lyrics information, reflecting the model structure’s inherent advantages in
feature learning and generalization capability. Loss function analysis in data missing scenarios further verified the model’s effectiveness. As shown in
Fig. 12, LyricEmotionNet’s loss value rapidly decreased from an initial 0.95 to a final 0.15, demonstrating optimal
convergence characteristics. The loss progression under missing data conditions reveals enhanced component
interdependency. The removal of Memory Networks resulted in a final loss value that rose from 0.15 to 0.32,
an increase of over double the original loss. This was substantially higher than the 43.7% increase observed
under complete data conditions. This amplified impact demonstrates that Memory Networks’ contextual
modeling becomes increasingly vital when working with fragmented information, as the component must
compensate for missing sequential cues through enhanced long-range dependency capture. The removal of
CapsNet resulted in a final loss value that rose from 0.15 to 0.45 under missing data conditions, a three-fold
increase. In comparison, the loss demonstrated a more than two-fold increase under complete data conditions. The disproportionate degradation suggests that local feature extraction mechanisms face greater challenges
when operating on incomplete data, requiring more sophisticated pattern recognition capabilities to maintain
emotional classification accuracy from reduced input information. Although models without Memory Networks
and CapsNet also showed declining trends, their final loss values remained at 0.32 and 0.45 respectively. In
contrast, the baseline model’s loss only decreased from 1.00 to 0.85, showing poor convergence. The loss curve
morphology shows that LyricEmotionNet maintained stable optimization momentum throughout the training
process and achieved a lower final loss level, confirming the model’s superiority in handling incomplete lyrics. ROC curve and AUC analysis (Fig. 13) under data missing conditions further confirmed the model’s
robustness. LyricEmotionNet achieved an AUC value of 0.923, significantly outperforming other models. The
AUC performance under missing data conditions demonstrates remarkable stability for the complete model,
maintaining 0.923 compared to 0.9210 under complete conditions (0.3% decrease). This minimal degradation
contrasts sharply with component-removed variants: Memory Networks removal resulted in 10.3% AUC
reduction under missing conditions (0.923 to 0.758) compared to 8.2% under complete conditions, while
CapsNet removal showed 19.6% reduction (0.923 to 0.742) compared to 14.4% under complete conditions. These patterns indicate that both components demonstrate enhanced importance under information scarcity,
with CapsNet showing greater sensitivity to missing data scenarios, likely due to the increased difficulty of local
pattern recognition when working with incomplete emotional expressions. After removing Memory Networks
and CapsNet components, AUC values decreased to 0.758 and 0.742 respectively, while the baseline model’s
AUC was only 0.432, approaching the level of a random classifier (AUC=0.500). The ROC curve morphology
shows that LyricEmotionNet maintained high classification discrimination ability even with missing lyrics,
achieving high true positive rates at relatively low false positive rates. Table 4 comprehensively displays the performance of different models under complete data and missing
data conditions. All reported metrics represent mean values computed across five independent experimental
runs using different random seeds (42, 123, 256, 512, 777) to ensure statistical reliability and eliminate random
initialization bias. Experimental results show that LyricEmotionNet significantly outperforms comparative
models across all metrics, particularly demonstrating notable robustness in handling incomplete lyrics. Under
complete lyrics conditions, the model achieved 94.29% accuracy, 0.125 loss value, and 0.921 AUC value with
remarkably low variance (standard deviations of ±0.8%, ±0.02, and ±0.01 respectively), indicating highly
stable training behavior. Even with 25% missing data, performance only slightly decreased to 90.20% accuracy,
0.150 loss value, while maintaining a high AUC value of 0.923, with correspondingly low standard deviations
(±1.1%, ±0.03, ±0.02), demonstrating consistent robustness across different data conditions. In contrast, Fig. 12. Model Loss Performance Comparison under Missing Data Conditions. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

when core components were removed or the baseline model was used, performance decreased significantly
with substantially higher variance, especially in lyrics missing scenarios where both performance decline
and instability were more pronounced. The model without Memory Networks exhibited standard deviations
ranging from ±1.2% to ±2.1% for accuracy, while the model without CapsNet showed deviations from ±1.5% to
±2.3%. Most notably, the baseline TextCNN model demonstrated the highest variance with standard deviations
reaching ±2.1% under complete lyrics and ±3.2% under missing data conditions, indicating inherent training
instability when processing complex emotional features and incomplete information. These results fully confirm
the effectiveness of the proposed hybrid architecture and the model’s potential value in practical application
scenarios, where both high performance and consistent reliability are essential requirements. Capsule Number (k)
Accuracy(%)
Std Dev
Theoretical Prediction
Prediction Error
Performance Gain

88.7
±2.1
87.9
0.8
Baseline

91.3
±1.8
92.4
1.1
+2.6%

92.8
±1.6
94.1
1.3
+4.1%

94.29
±1.4
94.8
0.51
+5.6%
Table 5. Capsule Number Impact on Classification Performance. Correlation coefficient: r = 0.82, p < 0.01. Moderately supports Corollary 1 predictions. Model
Complete Lyrics
Missing Data
ACC(%)
Loss
AUC
ACC(%)
Loss
AUC
LyricEmotionNet
94.29
0.125
0.921
90.20
0.150
0.923
w/o Memory Networks
90.93
0.180
0.846
75.50
0.320
0.758
w/o CapsNet
85.97
0.250
0.788
73.10
0.450
0.742
Baseline (TextCNN)
78.41
0.358
0.733
38.40
0.850
0.432
Table 4. Model Performance Comparison under Complete Lyrics and Missing Data Conditions. All results
represent mean values across five independent runs with different random seeds (42, 123, 256, 512, 777). The standard deviations for LyricEmotionNet are: Complete Lyrics (ACC: ±0.8%, Loss: ±0.02, AUC: ±0.01), Missing Data (ACC: ±1.1%, Loss: ±0.03, AUC: ±0.02). Other models show higher variance with standard
deviations ranging from ±1.2% to ±3.2% for accuracy metrics. Fig. 13. Model ROC Performance Comparison under Missing Data Conditions. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

Critical parameter investigation
Systematic experiments examined the impact of key architectural parameters on model performance to validate
theoretical predictions regarding capsule number and memory capacity configurations. Table 5 demonstrates reasonable alignment between Corollary 1 predictions and experimental observations
regarding capsule number effects. Classification accuracy increases from 88.7% (k=8) to 94.29% (k=64),
with correlation coefficient r = 0.82 indicating moderate theoretical-experimental agreement. Performance
improvements exhibit diminishing returns beyond k = 32, suggesting optimal computational efficiency occurs at
moderate capsule counts. Experimental values show prediction errors ranging from 0.51 to 1.3 percentage points,
reflecting typical experimental variation while providing reasonable support for the theoretical framework. The
theoretical model tends to slightly overestimate performance at intermediate capsule numbers, indicating areas
where the theoretical assumptions may require refinement. Memory capacity analysis in Table 6 provides partial validation of Theorem 2 error bound predictions. Most
experimental representation errors remain within theoretical bounds, though N_l = 256 shows representation
error (0.073) slightly exceeding the theoretical bound (0.071), indicating the presence of practical factors not
fully captured by the theoretical model. Correlation r = 0.78 suggests reasonable theoretical alignment despite
experimental variability and model limitations. Performance stabilization emerges at N_l = 512, consistent
with theoretical requirement N_l ≥ log(T/ϵ_l) given average sequence length T = 78. Error reduction becomes
marginal beyond this threshold, establishing practical parameter selection guidelines while acknowledging the
approximate nature of theoretical bounds in realistic experimental conditions. The observed deviations highlight
the complexity of real-world implementation compared to idealized theoretical frameworks. Comparison with state-of-the-art approaches
To comprehensively evaluate the proposed model’s performance within the current research landscape,
systematic comparisons were conducted with recent state-of-the-art sentiment analysis approaches. The
comparative analysis encompasses four representative models from contemporary literature: Transformer-based
Model (TBM)34, Emotion Correlation-enhanced Sentiment Analysis Model (ECO-SAM)35, BERT-WWM-ATT-
BiLSTM model (NBWAB)36, and CLIP-based Cross-Modal Sentiment Analysis model37. These models represent
diverse architectural paradigms including pure transformer approaches, BERT-based correlation modeling,
multi-component hybrid architectures, and cross-modal fusion techniques. Table 7 presents comprehensive performance comparisons across multiple evaluation metrics. LyricEmotionNet demonstrates superior performance across all evaluation dimensions, achieving 94.29%
accuracy, 0.125 loss value, 0.921 AUC, and 93.85% F1-score. The performance advantages range from
5.16 percentage points over the strongest competitor (TBM) to 19.62 percentage points over cross-modal
approaches, establishing clear superiority in lyrics-specific emotion analysis tasks. The Transformer-based
Model (TBM) exhibits competitive performance with 89.13% accuracy, representing the strongest alternative
approach. However, the 5.16 percentage point accuracy gap reveals fundamental limitations in pure transformer
architectures when processing lyrics-specific emotional patterns. TBM’s reliance on standard self-attention
mechanisms lacks the specialized feature extraction capabilities required for capturing local emotional clusters
characteristic of lyrical expression. The model’s loss value of 0.198 indicates suboptimal convergence compared
to LyricEmotionNet’s 0.125, suggesting that general-purpose transformer architectures encounter optimization
challenges when adapting to domain-specific emotional feature distributions. ECO-SAM’s performance of
86.75% accuracy demonstrates the effectiveness of BERT-based correlation modeling in sentiment analysis tasks. Model
Architecture Type
ACC(%)
Loss
AUC
F1-Score(%)
LyricEmotionNet
CapsNet + Memory Networks
94.29
0.125
0.921
93.85
TBM34
Pure Transformer
89.13
0.198
0.847
91.59
ECO-SAM35
BERT + Correlation Modeling
86.75
0.224
0.823
87.42
NBWAB36
BERT + BiLSTM + Attention
84.62
0.267
0.798
85.18
CLIP-Cross-Modal37
CLIP + Cross-Modal Fusion
74.67
0.389
0.721
74.52
TextCNN (Baseline)
Convolutional Neural Network
78.41
0.358
0.733
77.89
Table 7. Performance Comparison with State-of-the-Art Sentiment Analysis Models. Memory Capacity (N_l)
Representation Error
Std Dev
Theoretical Bound
Bound Satisfaction
Efficiency Status

0.092
±0.015
0.095
✓
Suboptimal

0.073
±0.011
0.071
×
Moderate

0.051
±0.009
0.052
✓
Optimal

0.048
±0.008
0.049
✓
Saturated
Table 6. Memory Capacity Effect on Global Emotion Representation Error. Correlation coefficient: r = 0.78, p
< 0.05. Provides reasonable support for Theorem 2. Performance stabilization occurs at N_l = 512 for sequence
length T = 78. Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

The 7.54 percentage point performance gap compared to LyricEmotionNet primarily stems from architectural
limitations in handling hierarchical emotional representations. While ECO-SAM successfully models inter-
emotional correlations through self-attention mechanisms, the approach lacks specialized components for
capturing the spatial clustering of emotional expressions typical in lyrics. The correlation modeling framework
proves insufficient for addressing the unique challenge of local emotional pattern recognition that characterizes
lyrical content. NBWAB achieves 84.62% accuracy through its hybrid BERT-BiLSTM-Attention architecture. The 9.67 percentage point performance deficit reflects the model’s sequential processing limitations when
confronting the non-sequential nature of emotional expressions in lyrics. While BiLSTM components effectively
capture temporal dependencies in general text processing, emotional expressions in lyrics often manifest as
spatially clustered patterns rather than temporally sequential structures. The attention mechanism, despite
providing some capability for long-range dependency modeling, cannot compensate for the fundamental
architectural mismatch between sequential processing and spatial emotional pattern recognition. The CLIP-
based cross-modal approach demonstrates the poorest performance at 74.67% accuracy, falling 19.62 percentage
points below LyricEmotionNet. This significant performance gap results from the fundamental mismatch
between cross-modal fusion objectives and text-only emotion analysis requirements. CLIP’s strength lies in
image-text correspondence learning, which provides limited benefits for pure textual emotion classification
tasks. The model’s complexity in cross-modal attention mechanisms introduces computational overhead without
corresponding performance benefits in single-modality scenarios, resulting in suboptimal feature learning for
lyrics-specific emotional patterns. Performance analysis reveals that domain-specific architectural design provides substantial advantages over
general-purpose approaches. LyricEmotionNet’s hybrid architecture effectively addresses the dual challenges
of local emotional pattern recognition through CapsNet’s dynamic routing mechanisms and global contextual
modeling through Memory Networks’ long-range dependency capture. Pure transformer approaches, despite
their success in general natural language processing tasks, demonstrate limitations when applied to specialized
domains requiring both local and global feature integration. BERT-based models show moderate effectiveness
but lack the hierarchical feature representation capabilities necessary for optimal performance in lyrics emotion
analysis. Cross-modal approaches prove unsuitable for text-only emotion analysis tasks, highlighting the
importance of architectural alignment with task-specific requirements. The experimental evidence establishes that specialized hybrid architectures outperform general-purpose
models in domain-specific applications. LyricEmotionNet’s superior performance across all evaluation metrics
validates the theoretical foundation and practical effectiveness of combining capsule networks for local feature
extraction with memory networks for global context modeling. The consistent performance advantages
demonstrate that task-specific architectural design principles provide substantial benefits over adaptation of
existing general-purpose models to specialized domains. Discussion
Through systematic experimental validation, this study demonstrated LyricEmotionNet’s performance
advantages in lyrics emotion analysis. Based on the experimental results and current state of research in music
emotion computing, we present an in-depth discussion from three dimensions: cognitive mechanisms, technical
implementation, and application prospects, aiming to provide new insights for the development of music
emotion analysis technology.

### 1. Emotional Cognitive Mechanism of Hybrid Architecture The hybrid architecture constructed in this study

simulates the cognitive process of human lyrics emotion understanding: local feature capture resembles di­
rect perception of emotional vocabulary, while the long-term memory mechanism corresponds to grasping
overall emotional context. Experiments show that this biomimetic cognitive design achieves 94.29% accu­
racy under complete lyrics conditions. Through ablation experiments, we found that the synergistic effect of
CapsNet and Memory Networks realizes emotional feature extraction at both microscopic and macroscopic
levels, and this multi-scale processing mechanism highly aligns with how humans process musical emotional
information.

### 2. Robustness and Real-world Challenges in Music Emotion Analysis A key challenge faced by online music

platforms is the incompleteness of lyrics data. Experimental results show that under 25% missing conditions, LyricEmotionNet still maintains a 90.20% performance level, demonstrating significant anti-interference
capability. This robustness stems from the model’s simulation of human memory and understanding mecha­
nisms: when partial lyrics are missing, it maintains judgment accuracy through context supplementation and
local feature enhancement, providing a viable solution for data quality issues on music platforms.

### 3. Future-oriented Music Emotion Computing With the growing demand for personalized music recom­

mendations, accurate emotion analysis becomes increasingly important. Although this study confirms the
effectiveness of the hybrid architecture, challenges remain: the model’s dependence on lyrics language may
limit its application in the global music market, and computational complexity needs further optimization. Future research could focus on enhancing cross-language understanding capabilities and lightweight design
for edge computing, better serving personalized music recommendation needs. Conclusion
The flourishing development of online music platforms has generated an urgent demand for high-quality
emotion analysis technology. Through analyzing the limitations of existing technologies, this study proposed
an innovative LyricEmotionNet hybrid architecture, successfully addressing key challenges in lyrics emotion
analysis. Experimental results show that the proposed model achieves 94.29% classification accuracy and an
AUC value of 0.921 under complete lyrics conditions, significantly outperforming the baseline model’s 78.41%
Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

and 0.733. When processing incomplete song information, the model still maintains 90.20% accuracy and an
AUC value of 0.923, while the baseline model’s performance drops precipitously to 38.40% and 0.432. Ablation
experiments further confirm the crucial impact of the synergistic effect between CapsNet and Memory Networks
on model performance, with removal of either component leading to over 15% performance degradation. These
experimental data not only validate the effectiveness of the hybrid architecture in simulating human emotional
cognitive processes but also provide a new technical paradigm for music emotion analysis. Although current
implementation still has room for improvement in computational efficiency and language adaptability, the
model’s demonstrated performance advantages already provide a viable solution for the emotion analysis needs
of online music platforms. Data availability
The music data and song lyrics that support the findings of this study have been obtained from the “Music Da­
taset - Song Information and Lyrics” repository with the primary access link ​h​t​t​p​s​:​/​/​w​w​w​.​k​a​g​g​l​e​.​c​o​m​/​d​a​t​a​s​e​t​s​/​s​
u​r​a​j​5​2​0​/​m​u​s​i​c​-​d​a​t​a​s​e​t​-​s​o​n​g​-​i​n​f​o​r​m​a​t​i​o​n​-​a​n​d​-​l​y​r​i​c​s. Received: 22 March 2025; Accepted: 22 September 2025
References

### 1. Han, D., Kong, Y., Han, J. & Wang, G. A survey of music emotion recognition. Front. Comput. Sci.  16, (2022).

### 2. Gómez-Cañón, J. S. et al. Trompa-mer: an open dataset for personalized music emotion recognition. J. Intell. Inf. Syst. 60, 549–570

(2023).

### 3. He, N. & Ferguson, S. Music emotion recognition based on segment-level two-stage learning. Int. J. Multimed. Inf. Retr. 11, 383–

394 (2022).

### 4. Sams, A. S. & Zahra, A. Multimodal music emotion recognition in indonesian songs based on cnn-lstm, xlnet transformers. Bull. Electr. Eng. Informatics 12, 355–364 (2023).

### 5. Daneshfar, F. Speech emotion recognition using deep sparse auto-encoder extreme learning machine with a new weighting scheme

and spectro-temporal features along with classical feature selection and a new quantum-inspired dimension reduction method
(2021).

### 6. Chaturvedi, V. et al. Music mood and human emotion recognition based on physiological signals: a systematic review. Multimed. Syst. 28, 21–44 (2022).

### 7. Liu, Z., Xu, W., Zhang, W. & Jiang, Q. An emotion-based personalized music recommendation framework for emotion

improvement. Inf. Process. & Manag. 60, (2023).

### 8. Joel, J. S. et al. Emotion based music recommendation system using deep learning model. In 2023 International Conference on

Inventive Computation Technologies (ICICT), 227–232 (IEEE, 2023).

### 9. Priyanka, V. T., Reddy, Y. R., Vajja, D., Ramesh, G. & Gomathy, S. A novel emotion based music recommendation system using cnn. In 2023 7th International Conference on Intelligent Computing and Control Systems (ICICCS), 592–596 (IEEE, 2023).

### 10. Hou, R. Music content personalized recommendation system based on a convolutional neural network. SOFT COMPUTING 28,

1785–1802. https://doi.org/10.1007/s00500-023-09457-2 (2024).

### 11. Niu, N. Music emotion recognition model using gated recurrent unit networks and multi-feature extraction. Mob. Inf. Syst. 2022,

5732687 (2022).

### 12. Cui, X. et al. A review: Music-emotion recognition and analysis based on eeg signals. Front. neuroinformatics 16, (2022).

### 13. Orjesek, R., Jarina, R. & Chmulik, M. End-to-end music emotion variation detection using iteratively reconstructed deep features. Multimed. Tools Appl. 81, 5017–5031 (2022).

### 14. Daneshfar, F. & Kabudian, S. J. Speech emotion recognition system by quaternion nonlinear echo state network. arXiv preprint

arXiv:2111.07234 (2021).

### 15. Garg, A., Chaturvedi, V., Kaur, A. B., Varshney, V. & Parashar, A. Machine learning model for mapping of music mood and human

emotion based on physiological signals. Multimed. Tools Appl. 81, 5137–5177 (2022).

### 16. Wang, J. & Ma, H. Users’ preference-aware music recommendation with contrastive learning. In Huang, D., Pan, Y. & Guo, J. (eds.)

Advanced Intelligent Computing Technology and Applications, PT XII, ICIC 2024, vol. 14873 of Lecture Notes in Computer Science,
309–320, https://doi.org/10.1007/978-981-97-5615-5_25 (2024). 20th International Conference on Intelligent Computing (ICIC), Tianjin Univ Sci & Tech, Tianjin, Peoples R China, Aug 05-08, 2024.

### 17. Yuan, J., Gao, B., Wang, X., Liu, H. & Zhang, L. Counterfactual music recommendation for mitigating popularity bias. IEEE

Transactions on Computational Social Systems https://doi.org/10.1109/TCSS.2024.3491800 (2024).

### 18. Xu, J., Gan, M. & Zhang, X. Mmusic: a hierarchical multi-information fusion method for deep music recommendation. Journal of

Intelligent Information Systems 61, 795–818. https://doi.org/10.1007/s10844-023-00786-0 (2023).

### 19. Wang, D. et al. Multi-view enhanced graph attention network for session-based music recommendation. ACM Transactions on

Information Systems 42, https://doi.org/10.1145/3592853 (2024).

### 20. Oh, Y., Yun, S., Hyun, D., Kim, S. & Park, C. Muse: Music recommender system with shuffle play recommendation enhancement. In Proceedings of the 32nd ACM International Conference on Information and Knowledge Management, CIKM 2023, 1928–1938,
https://doi.org/10.1145/3583780.3614976 (Assoc Comp Machinery; ACM Special Interest Grp Informat Retrieval; ACM SIGWEB,
2023). 32nd ACM International Conference on Information and Knowledge Management (CIKM), Birmingham, England, OCT
21-25, 2023.

### 21. Stoikos, S., Kauchak, D., Papoutsaki, A., Turnbull, D. Cross-language. & music recommendation exploration. In Proceedings of the,. ACM International Conference on Multimedia Retrieval. ICMR 2023(664–668), 2023. https://doi.org/10.1145/3591106.3592274
(Assoc Comp Machinery, 2023). ACM International Conference on Multimedia Retrieval (ICMR), Thessaloniki, GREECE, JUN
12-15 (2023).

### 22. Cheng, H., Huang, X., Zhang, R. & Ye, L. Persong: Multi-modality driven music recommendation system. In 2022 IEEE

International Conference on Multimedia and Expo Workshops (IEEE ICMEW 2022), IEEE International Conference on Multimedia
and Expo Workshops, https://doi.org/10.1109/ICMEW56448.2022.9859488 (IEEE; IEEE Comp Soc; IEEE Circuits & Syst Soc; IEEE Signal Proc Soc; IEEE Commun Soc; Mediatek; Acad Sinica, Inst Informat Sci; Acad Sinica, Res Ctr Informat Technol
Innovat; Meta; Foxconn; Minist Sci & Technol, 2022). IEEE International Conference on Multimedia and Expo (IEEE ICME), Taipei, Taiwan, Jul 18-22, 2022.

### 23. Patel, J. et al. Concolla - a smart emotion-based music recommendation system for drivers. Scalable Computing-Practice and

Experience 24, 919–940, https://doi.org/10.12694/scpe.v24i4.2467 (2023).

### 24. Magadum, H., Azad, H. K., Patel, H. & Rohan, H. R. Music recommendation using dynamic feedback and content-based filtering. Multimedia Tools and Applications https://doi.org/10.1007/s11042-024-18636-8 (2024). Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/

### 25. Reddy, S. V. et al. A cutting-edge artificial intelligence paradigm for entertainment-infused music recommendations. Entertainment

Computing 51, https://doi.org/10.1016/j.entcom.2024.100717 (2024).

### 26. Feng, W., Liu, J., Li, T., Yang, Z. & Wu, D. Fac: A music recommendation model based on fusing audio and chord features (115). International Journal of Software Engineering and Knowledge Engineering 32, 1753–1770. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​4​2​/​S​0​2​1​8​1​9​4​0​2​2​5​0​0​
5​7​7​ (2022).

### 27. Peng, Y. Double music recommendation algorithm based on multi-label propagation hierarchical clustering analysis. Journal of

Computational Methods in Sciences and Engineering 24, 3003–3014. https://doi.org/10.3233/JCM-247542 (2024).

### 28. Khan, M. et al. Joint multi-scale multimodal transformer for emotion using consumer devices. IEEE Transactions on Consumer

Electron. 71, 1092–1101. https://doi.org/10.1109/TCE.2025.3532322 (2025).

### 29. Nguyen, L. H., Pham, N. T., Khan, M., Othmani, A. & EI Saddik, A. Hubert-clap: Contrastive learning-based multimodal emotion

recognition using self-alignment approach. In Proceedings of the 6th ACM International Conference on Multimedia in Asia, MMAsia ’24, https://doi.org/10.1145/3696409.3700183 (Association for Computing Machinery, New York, NY, USA, 2024).

### 30. Khan, M., Tran, P. N., Pham, N. T., Nguyen, T. K. & Duong, D. Q. Memocmt: multimodal emotion recognition using cross-modal

transformer-based feature fusion. Scientific reports 15, 5473, https://doi.org/10.1038/s41598-025-89202-x (2025).

### 31. Deldjoo, Y., Schedl, M. & Knees, P. Content-driven music recommendation: Evolution, state of the art, and challenges. Computer

Science Review 51, https://doi.org/10.1016/j.cosrev.2024.100618 (2024).

### 32. Jaaskelainen, T. Music students’ workload, stress, and coping in higher education: Evidence-based policymaking. Frontiers in

Psychology 13, https://doi.org/10.3389/fpsyg.2022.846666 (2022).

### 33. Elahi, M., Kholgh, D. K., Kiarostami, M. S., Oussalah, M. & Saghari, S. Hybrid recommendation by incorporating the sentiment of

product reviews. Information Sciences 625, 738–756. https://doi.org/10.1016/j.ins.2023.01.051 (2023).

### 34. Tamilkodi, R., Sujatha, B. & Leelavathy, N. Emotion detection in text: advances in sentiment analysis. International Journal of

System Assurance Engineering and Management 16, 552–560. https://doi.org/10.1007/s13198-024-02597-0 (2025).

### 35. Ni, Y. & Ni, W. A multi-label text sentiment analysis model based on sentiment correlation modeling. Frontiers in Psychology 15,

https://doi.org/10.3389/fpsyg.2024.1490796 (2024).

### 36. Wang, X., Huang, H., Ding, Z. & Nbwab: A model for text sentiment analysis with bert and chatgpt. In,. International Joint

Conference on Neural Networks, IJCNN 2024. IEEE International Joint Conference on Neural Networks (IJCNN) 2024, ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​I​J​C​N​N​6​0​8​9​9​.​2​0​2​4​.​1​0​6​5​0​0​1​6​ (IEEE; IEEE Computat Intelligence Soc; Int Neural Network Soc; Ask Corp; Springer; Align; Genisama; Noeon Res; Hitachi Zosen Corp; JNNS; Japanese Soc Evolutionary Computat; IPJ; EIC; SICE; SOFT; Japanese
Soc Artificial Intelligence, 2024). International Joint Conference on Neural Networks (IJCNN), Yokohama, Japan, Jun 30-Jul 05
(2024).

### 37. Lu, X., Ni, Y. & Ding, Z. Cross-modal sentiment analysis based on clip image-text attention interaction. International Journal of

Advanced Computer Science and Applications 15, 895–903 (2024). Acknowledgements
This article is a significant milestone in the 2021 Guangxi Philosophy and Social Science Planning Research Pro­
ject titled ’Research on the Modern Adaptability and Innovative Transformation of Guinan Tea picking Opera in
the Context of Rural Revitalization’ (21FZW006). Author contributions
G. Z. conceived the experiment(s), G. Z. and J. H. conducted the experiment(s), J. H. and G. Z. analysed the results. All authors reviewed the manuscript. Declarations
Competing interests
The authors declare no competing interests. Additional information
Supplementary Information The online version contains supplementary material available at ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​3​8​/​s​4​1​5​9​8​-​0​2​5​-​2​1​5​9​3​-​3​.​
Correspondence and requests for materials should be addressed to J. H. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:37785

| https://doi.org/10.1038/s41598-025-21593-3
www.nature.com/scientificreports/
