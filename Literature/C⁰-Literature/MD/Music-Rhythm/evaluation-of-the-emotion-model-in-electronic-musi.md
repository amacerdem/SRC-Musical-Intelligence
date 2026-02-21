# evaluation-of-the-emotion-model-in-electronic-musi

Research Article
EvaluationoftheEmotionModelinElectronicMusic
BasedonPSO-BP
TingGuo
School of Music, Xi’an University, Xi’an, Shannxi 710065, China
Correspondence should be addressed to Ting Guo; guoting@xawl.edu.cn
Received 17 March 2022; Revised 13 April 2022; Accepted 23 April 2022; Published 30 May 2022
Academic Editor: Gengxin
Sun
Copyright© 2022 Ting Guo. WK_his is an open access article distributed under the Creative Commons Attribution License, which
permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.
Electronic music can help people alleviate the pressure in life and work. It is a way to express people’s emotional needs. With the
increaseofthetypesandquantityofelectronicmusic,thetraditionalelectronicmusicclassiﬁcationandemotionalanalysiscannot
meet people’s more and more detailed emotional needs. WK_herefore, this study proposes the emotion analysis of electronic music
basedonthePSO-BPneuralnetworkanddataanalysis,optimizestheBPneuralnetworkthroughthePSOalgorithm,andextracts
and analyzes the emotional characteristics of electronic music combined with data analysis. WK_he experimental results show that
compared with BP neural network, PSO-BP neural network has a faster convergence speed and better optimal individual ﬁtness
valueandcanprovidemorestableoperatingconditionsforlatertrainingandtesting.WK_heelectronicmusicemotionanalysismodel
based on PSO-BP neural network can reduce the error rate of electronic music lyrics text emotion classiﬁcation and identify and
analyze electronic music emotion with high accuracy, which is closer to the actual results and meets the expected requirements.
1.Introduction
With the popularity of the Internet and mobile communi-
cation devices, music, as a value-added service of Internet
and mobile devices, has developed rapidly in recent years.
WK_he study of music emotion recognition is an important
technical link in music operation and maintenance service.
WK_here are two research directions in the ﬁeld of music
emotion recognition: one direction is to extract the tone
feature valueby wavelettransform andrecognize therelated
tones. WK_his kind of music ﬁle stores the sampling data of
music acoustic signal. WK_he research focuses on signal pro-
cessing. WK_heother directionis touse HMM (hiddenMarkov
model) for single tone note recognition, that is, to use the
audiosignalofmusictoobtainthescorereﬂectingthemusic
content. Due to the heavy workload of identifying each note
inmusic,itisimpossibletoaccuratelyidentifytheemotional
type of music. WK_he existing music emotion classiﬁcation
methods have the following two shortcomings: (1) the tone
recognition method is based on the sampling data pro-
cessing of music acoustic signal, unable to recognize music
emotion information. (2) Analyze music emotion based on
the pitch, length, and intensity of a single note. BP neural
network has been successful in many ﬁelds because it can
correct the weight and threshold according to the back-
propagationof error.However, itmay fallintolocalminima
and cannot ensure convergence to the global minima. In
addition, the number of backpropagation training is large
andtheconvergencespeedisslow,whichmakesthelearning
results sometimes unsatisfactory. If the particle swarm op-
timizationalgorithmwiththemeansquareerrorindexasthe
ﬁtnessvalueisusedtotraintheweightofBPnetwork, itwill
get a faster convergence speed and avoid the occurrence of
the local maximum.
Music plays a very important role in people’s life, work,
and study. Music can not only help people reduce the
pressure in life and work but also express rich emotions and
aﬀect people’s mood and heart. It is an indispensable part of
the development of human society. With the changes of the
times, the way people listen to music has changed from tape
records to digital music ﬁles, and the types of music are also
increasing.WiththecontinuousdevelopmentoftheInternet
and technology, electronic music has gradually entered the
public’s vision and occupied a certain position in the music
Hindawi
Computational Intelligence and Neuroscience
Volume 2022, Article ID 5601689, 9 pages
https://doi.org/10.1155/2022/5601689
market. Diﬀerent people have diﬀerent preferences for
diﬀerent electronic music,and if people wantto obtain their
preferred electronic music types, they have to choose from a
largenumberofelectronicmusic,whichgreatlyincreasesthe
timecostoflistening tomusic[1].WK_herefore,howtoquickly
and accurately select and listen to much needed electronic
musichasbecomethefocusofelectronicmusicclassiﬁcation
research.Musicemotionanalysisandrecognitionarethekey
basis to improving the classiﬁcation and search eﬃciency of
electronic music. In the past, electronic music recognition
mainly used wavelet transform to extract the characteristics
of musical tones and then identify and analyze them or
recognize the single tone notes of music through music
audio signals [2]. WK_he former method cannot identify the
emotional information in electronic music, while the latter
method is inaccurate. Neither method can meet people’s
needs for emotional analysis of electronic music.
WK_he development of artiﬁcial intelligence and data
analysis technology opens up a new development direction
for electronic music emotion analysis. WK_herefore, this paper
proposes electronic music emotion analysis based on the
PSO-BP neural network and data analysis, which is opti-
mized by the PSO algorithm on the basis of the BP neural
network structure to improve the performance of the neural
network.Atthesametime,combinedwith dataanalysis,the
music emotion characteristics of electronic music are
extractedandprocessedthroughthemusicemotionanalysis
model so as to obtain the expected analysis of electronic
musicemotion.WK_hispaperismainlydividedintothreeparts.
WK_he ﬁrst part is the development of music emotion classi-
ﬁcationandanalysisandrelatedresearch.WK_hesecondpartis
theconstructionofelectronicmusicemotionanalysismodel
based on PSO-BP neural network. WK_he fourth part is the
application experiment and result analysis of the electronic
music emotion analysis model based on the PSO-BP neural
network.
2.RelatedWork
Musicemotionanalysisiscloselyrelatedtothedevelopment
of artiﬁcial intelligence. People put forward the idea of
recognizing the emotion expressed by music based on this
and combined it with corresponding computer technology
inthe earlystage ofthe developmentof artiﬁcialintelligence
so that artiﬁcial intelligence can realize the functions of
music, self-action music, and emotional music retrieval [3].
WK_here are some similarities between music emotion classi-
ﬁcation and analysis research and speech emotion analysis,
and the biggest diﬀerence between the two is that the du-
ration of music is longer, and the content composition is
more complex. If emotion analysis needs to extract a large
number of emotional features from music, it has many
dimensions and has high diﬃculty in feature analysis [4].
WK_hekeyinﬂuencingfactorsofmusicemotionanalysisresults
are characteristic parameters and classiﬁcation methods,
which is also an important research direction for most
scholars.
In foreign countries, the research on music emotion
analysis has achieved good results and has begun to be
applied.Forexample,Japan’s“chuyin”softwareconvertsthe
input tone and lyrics into sound and converts the songs
accordingly through emotional parameters so as to obtain
music works comparable to real-life performance [5]. In
addition, some scholars pointed out that music style can
classify music emotion with the help of chord and beat
information in music, but such music emotion classiﬁcation
method has certain limitations in the ﬁne-grained aspect of
emotion classiﬁcation [6]. Other scholars extracted Mel
frequency based on the frequency domain, combined with a
genetic classiﬁcation algorithm, and classiﬁed music emo-
tion information with spacing and zero-crossing rate as the
best ﬁtting ratio, and achieved good results [7]. With the
increase of music emotion classiﬁcation and analysis
methods, some scholars have studied the performance of
diﬀerent modal features in two-dimensional emotion co-
ordinates. WK_he research results show that compared with
lyrics text classiﬁcation, the eﬀect of the deep learning
method in audio classiﬁcation results is better [8]. In music,
theemotionalclassiﬁcationoflyricstextisalsoanimportant
part. Its classiﬁcation technology comes from the text
classiﬁcation model. WK_hat is, the computer extracts the
corresponding features of the formulated documents and
automatically assigns them to the categories deﬁned
according to the text content [9]. Text classiﬁcation mainly
includes two parts: text feature extraction and classiﬁcation.
On this basis, some scholars have proposed a lyric emotion
classiﬁcationmethod.WK_hatis,theemotionalfeaturesoflyrics
are extracted through partial syntactic analysis and then
classiﬁed and veriﬁed by naive Bayes and machine learning
methods [10]. With the development of a deep learning
algorithm, some scholars classify Indonesian songs and
lyrics into happy and sad music emotions through the re-
current neural network, and its highest accuracy can reach
82% [11].
WK_he research on the classiﬁcation of music emotion in
China started late, but it has also made some achievements.
Itsresearchonmusicemotionclassiﬁcationiscloselyrelated
to the development of music software functions. With the
development of online music applications, music recom-
mendation function has become an urgent demand [12].
Most of the single album and song list push services of
various online music applications in the early stage were
recommended based on a collaborative ﬁltering algorithm.
WK_he biggest disadvantage of this method is that most of the
recommended songs are current popular songs, which
greatly reduces the recommendation probability of popular
works [13, 14]. At the same time, the long-term recom-
mendation of similar songs and song lists cannot meet
people’s demand for novelty [15]. WK_he development of ar-
tiﬁcial intelligence and related technologies enables com-
puters to analyze complex music emotions and
automatically output emotion analysis results [16]. After
feature extraction and selection of 37 music samples, some
scholars improved the accuracy of feature classiﬁcation
through principal component analysis and linear discrim-
inant analysis and eﬀectively improved the accuracy of the
emotion classiﬁer based on k-NN [17]. Based on the rela-
tionship between music emotion and music genre, other
2 Computational Intelligence and Neuroscience
scholars classify music emotion through SVM emotion
classiﬁcationandusefultypeinformationin musictags[18].
Other scholars have eﬀectively extracted the emotional
features in Chinese lyrics through the CNN pretraining
word embedding model. WK_he experimental results show that
this method has higher accuracy than the traditional
learning methods and other deep learning models [19].
Some scholars have constructed MIDI music emotion
classiﬁcation based on the BP neural network according to
the characteristics of electronic music [20].
3.ConstructionoftheEmotionAnalysis
ModelofElectronicMusicBasedonPSO-BP
NeuralNetwork
Music is an artistic way for people to convey and express
their emotions. WK_he emotions in music can aﬀect people’s
inner emotions, improve people’s life beliefs, and show
people’s rich emotional world. At the same time, the
emotional information contained in music has not only
subjective initiative butalso has overall fuzziness. WK_herefore,
when analyzing data, the traditional logical reasoning
method is diﬃcult to deal with the emotion contained in it
[21]. Based on the isomorphic correspondence between
music acoustic vibration and human emotional activities
described on the basis of psychology, this paper constructs
the emotion recognition and analysis model of electronic
music. Music emotion cognitive analysis model generally
includes the music emotion psychological model and cal-
culation model, that is, the data analysis model. Among the
psychological models, Hevner model and WK_hayer model are
commonly used models, which mainly discuss the charac-
teristics of human emotion from the perspective of psy-
chology [22]. Music emotion information is the basis of the
electronic music emotion cognitive analysis model [23]. To
some extent, people’s psychological feeling process of music
canberegardedastheprocessofmusicemotioninformation
from acquisition, transformation, transmission, processing,
andstorage.WK_herefore,music[24],emotioninformationnot
onlyhassubjectivity,objectivity,integrity,andfuzziness[25]
but also has hierarchy. WK_hat is, people’s cognition of elec-
tronic music emotion is hierarchical, as shown in Figure 1.
WK_hecognitivecharacteristicsofdiﬀerentlevelsareoneofthe
theoretical basis of the construction of electronic music
emotion recognition and analysis model.
Diﬀerentlevelsofcognitivecharacteristicsareoneofthe
theoretical bases for constructing the emotion recognition
and analysis model of electronic music. In order to improve
the accuracy of music emotion recognition, this paper
proposes a music emotion recognition model based on
diﬀerent levels of features. Abandon the low-level features
such as spectrum characteristics, chromaticity, and har-
monic coeﬃcient, and take the middle and high-level fea-
tures closer to human cognition, including cognition,
feeling,andmemory,astheinputoftheemotionrecognition
model. WK_he data set of music fragments is established, and
the music emotion recognition is abstracted as a regression
problem.
3.1. Emotional Feature Extraction of Electronic Music.
Music emotion feature extraction is mainly from music
lyrics, text information, and audio information. Emotion
feature extraction in lyrics text is based on the sparse dis-
tribution of lyrics text, sentence length, repetition, emotion
word recognition degree, and other characteristics [19]. As
shown in formulas (1) and (2), it is the quantitative formula
of a word recognition degree in electronic music:
LMD(w) � 􏽘
K
i�1
LMD(w, i), (1)
LMD(w, i) � abs(P(w|i) −P(w|≠i))������������������ �
max(P(w|i), P(w|≠i))
􏽰 . (2)
WK_henumberof electronicmusicemotionclassiﬁcationis
expressed asK, the probability of occurrence of wordw ini
emotion classiﬁcation is expressed asP(w|i), and its
probabilityofoccurrenceiniemotionclassiﬁcationaccident
category is expressed asP(w|≠i).
WK_here are some diﬀerences in the energy of electronic
music.WK_heenergyvalueofelectronicmusicishigher,andits
short-term energy calculation is shown in the following:
Em � 􏽘
N− 1
N
[y(n) · c(n − m)]2. (3)
WK_he electronic music signal is expressed asy(m)􏼈 􏼉 , its
energy is expressed asEm, the window function is expressed
asc(m), and the length of the electronic music signal frame
is expressed asN.
WK_he speciﬁc descriptionof any frame of electronicmusic
after smoothing through wavelet transform is shown in the
following:
􏽢Y
t(n) � 􏽢yt(n,1), 􏽢yt(n,2),. . ., 􏽢yt(n, N)􏼈 􏼉. (4)
Any frame of the processed electronic music is repre-
sented as􏽢Yt(n). According to (4), the mean and variance of
electronicmusictimedomaincanbecalculated,asshownin
the following:
E
t(n) � 1
N 􏽘
N
i�1
􏽢yt(n, i), (5)
Dt(n) � 1
N 􏽘
N
i�1
yt(n, i) − Et(n)􏼂 􏼃2, (6)
where the time-domain mean of electronic music is
expressed asE
t(n) and the variance is expressed asDt(n).
WK_he expression of a frame of electronic music after
wavelet transform smoothing in the frequency domain is
shown in the following:
􏽢Y
f(n) � 􏽢yf(n,1), 􏽢yf(n,2),. . ., 􏽢yf(n, N)􏽮 􏽯. (7)
A frame of electronic music processed in is expressed as
􏽢Yf(n), and the frequency domain mean and frequency
domain variance of electronic music are calculated in
combination with (7), as shown in the following:
Computational Intelligence and Neuroscience 3
Ef(n) � 1
N 􏽘
N
i�1
􏽢yf(n, i). (8)
Df(n) � 1
N 􏽘
N
i�1
yf(n, i) − Ef(n)􏽨 􏽩
2
, (9)
where the frequency domain mean of electronic music is
expressed asEf(n) and the frequency domain variance is
expressed asDf(n).
3.2. Emotion Model of Electronic Music Based on PSO-BP
Neural Network.BP neural network is a multilayer feed-
forward neural network in the artiﬁcial neural network. It
not only has the characteristics of adaptability, self-orga-
nization, and self-learning but also has the advantages of
simple structure, mature algorithm, and accurate optimi-
zation. At the same time, its application in electronic music
emotion recognition and analysis is more in line with the
cognitive characteristics of human emotion in music rec-
ognition. However, with the increasing data related to
emotional analysis and recognition of electronic music, the
eﬃciencyandaccuracyofBPneuralnetworkdecline[24].In
addition, BP neural network is easy to fall into a local
minimum. WK_herefore, based on BP neural network, this
paperintroducesaparticleswarmoptimizationalgorithmto
improve the eﬃciency and optimization ability of electronic
music emotion analysis model.
BP neural network algorithm is also called error back-
propagationalgorithm.Itiscomposedofthreeormoreneural
networks. WK_he ﬁrst layer is the input layer, the last layer is the
output layer, the middle layer is the hidden layer, and the
number of hidden layers is one or more layers. WK_here is no
connectionbetweenthenodescontainedineachlayer.Letthe
number of nodes in the input layer of the neural network be
expressed asd, the number of nodes in the hidden layer is
expressed asm, and the transfer function between nodes in
each layer be sigmoid function, as shown in the following:
S(x) �
1
1 + e− x, (10)
WK_he output calculation formula of the neural network
hidden layer is shown in the following:
Dj � S 􏽘
n
i�1
Rijxi􏼐 􏼑⎡⎣ ⎤⎦. (11)
Among them, j � 1,2,. . ., d, the variable of thei input
node is expressed asx
i, and the excitation function of the
hidden layer is expressed asS.
WK_heoutputcalculationformulaoftheoutputlayerofthe
neural network is shown in the following:
Ok � S 􏽘
h
j�1
DjRjk⎛⎝ ⎞⎠. (12)
k � 1,2,. . ., m.
Let the connection weight of the neuron between the input
layer and the hidden layer of the BP neural network be
expressed asR
ij, and the connection weight of the neuron
between the hidden layer and the output layer be expressed as
R
ik. WK_he calculation formulas of the two are shown in the
following:
music
Main 
melody
Auxiliary 
eﬀect
Pitch Time 
value Timbre Chords Decorative 
sound
Rhythm, speed and strength
Mode, musical form, style, emotion
Acoustic 
characteristics cognition
Spatiotemporal 
characteristics memory
Semantic 
features feel
Figure 1: Cognitive level characteristics of electronic music emotion.
4 Computational Intelligence and Neuroscience
Rij(t +1) � Rij(t) + η[ (1− θ)Q(t) + θQ(t − 1)], (13)
Rik(t +1) � Rik(t) + η[ (1− β)W(t) + βW(t − 1)], (14)
where i � 1,2,. . ., n; j � 1,2,. . ., d, i � 1,2,. . ., n;j � 1,2
, . . ., d, the learning rate is expressed asη and η >0, and the
momentum factor is expressed as θ and 0 ≤θ <1,
Q(t) � − zE/zRij(t), W(t) � − − zE/zRik(t)..
PSO algorithm, namely particle swarm optimization
algorithm,is anevolutionary computingtechnologyderived
from the study of bird predation behavior. It is a global
optimization method based on swarm intelligence theory.
PSO algorithm can not only optimize multidimensional
space functions and dynamic objectives, but also has the
advantages of fast convergence and good robustness.
LetthespaceofLdimensionbethesearchspace,andthe
number of particles contained in the population isK, then
the position of thej particle in the population in the space
canbeexpressedbyX
j � (xj1, xj2, . . ., xjl),andtheoptimal
solution in the particle position is the global optimal indi-
vidual,expressedasP
j � (pj1, pj2, . . ., pjl),andtheposition
velocity vector of the particle is expressed as
V
j � (vj1, vj2, . . ., vjl). As shown in (15) and (16), the po-
sitionandvelocityofeachparticleinthepopulationafterthe
iterative change:
v
jl(t +1) � g · vjl(t) + z1 · r d · pjl(t) − xjl(t)􏼐 􏼑
+ z2 · r d · py(t) − xjl(t)􏼐 􏼑,
(15)
xjl(t +1) � xjl(t) + vjl(t +1). (16)
In the formula, the inertia factor is expressed asg; the
acceleration factor is expressed asz1, z2 and it is a normal
number, r d is a random value andr d ∈[0,1], and the
current iterative algebra is expressed ast. Because the ve-
locityandinitialpositionoftheparticleswarmaregenerated
randomly,thepositionandvelocityoftheparticleswarmare
iterated through (15) and (16). When both meet the ter-
mination conditions, the iteration of the particle swarm
stops.
As shown in (17), it is the calculation formula of inertia
weight in (15):
g �
g
max − gmax − gmin  􏼁 s − save  􏼁
smax − save
, s ≥save,
gmax , s <save.
⎧⎪⎪⎪
⎨
⎪⎪
⎪⎩
(17)
WK_heﬁtnessvalueofparticlesisexpressedass,theaverage
ﬁtness value of particles is expressed ass
ave, and the largest
ﬁtness value in particle swarm is expressed assmax .
Figure 2 shows the ﬂow chart of PSO Algorithm Op-
timizing BP neural network.
As can beseenfrom Figure 2,optimizing theweight and
threshold of the BP neural network through the PSO al-
gorithm needs to recover the parameters such as particle
number, position, and learning factor contained in the PSO
algorithm.WK_henBPneuralnetworkisconstructedaccording
tothenumberofinputandoutputsignals,anditsweightand
threshold length are initialized. WK_hen they are encoded to
obtain the initial population of the PSO algorithm.
WK_he BP neural network is optimized by the PSO algo-
rithm,andthentheoptimizationiterationiscarriedout.WK_he
extreme values of particles and particle swarm are deter-
mined by the ﬁtness values of each group of particles, in
which the best position is the best position in the history of
particles in the optimization iteration process. WK_he iterative
updateofparticlespeedandpositioniscarriedoutaccording
to the formula. When the ﬁtness reaches the expected ac-
curacy or the maximum number of iterations is completed,
the optimization iteration stops, and the current position of
the particle is the optimal solution to solve the target. WK_he
optimal weight and threshold of the BP neural network are
obtained by decoding. If the conditions are not met, the
optimization iteration will be carried out again.
4.ApplicationExperimentoftheEmotion
AnalysisModelofElectronicMusicBasedon
PSO-BPNeuralNetwork
WK_hisstudycollects190electronicmusicsamples,ofwhich50
electronicmusicarerandomlyselectedasthetestsampleset,
and 140 electronic music are the training set of the model.
WK_heemotionofelectronicmusicismainlydividedintoeight
types according to the Hevner model, including cheerful,
lyrical, calm, quiet, sad, passionate, resolute, and angry
emotion. WK_he output performance of the BP neural network
is greatlyaﬀected by thenumberof hiddenlayernodesinits
structure. Before the emotional analysis of electronic music,
it is necessary to determine the optimal number of nodes of
the BP neural network through training. Let the number of
iterationsofnodetrainingbe20,asshowninFigure3,which
is the relationship between the number of hidden layer
nodes of the BP neural network and the error rate of BP
neural network training results. It can be seen from the
results in the ﬁgure that the increase of nodes in the hidden
layer in the BP neural network structure will continuously
improve the accuracy of its training results. When the
number of hidden layer nodes is less than 100,the error rate
will be greatly reduced with the increase of the number of
nodes.Whenthenumberofhiddenlayernodesexceeds100,
the error rate decreases gradually with the increase of the
number of nodes. At the same time, from the perspective of
time cost, the excessive number of hidden layer nodes
contained in the BP neural network will have a great impact
on its operation eﬃciency. WK_herefore, considering all factors
and inﬂuences, the number of hidden layer nodes in BP
neural network is 100.
WK_he maximum number of iterations of the emotion
analysis model of electronic music based on the PSO-BP
neural network is 1500. Figure 4 shows the comparison of
the optimal individual ﬁtness values of the PSO-BP neural
network and BP neural network.
As can be seen from Figure 4, the BP neural network
needs 65 iterations to achieve the convergence eﬀect, and
there are short-term ﬂuctuations after convergence. WK_he
Computational Intelligence and Neuroscience 5
PSO-BPneuralnetworkcanconvergeafter46times,andthe
convergent curve tends to be stable. WK_his shows that com-
paredwithBPneuralnetwork,PSO-BPneuralnetworkhasa
faster convergence speed, more stable operation, and better
performance.
As shown in Figure 5, the accuracy of pos-bp neural
networkandtraditionalBPneural networkintheemotional
classiﬁcation of electronic music text is compared. WK_hirty-
two pieces of electronic music were randomly selected from
the test sample set and divided into four groups for the text
emotion classiﬁcation test. On the whole, the classiﬁcation
accuracyofthePSO-BPneuralnetworkishigherthanthatof
18
19
20
21
22
23
24
25
26
27
28Error rate (%)
100 200 300 400 500 600 700 800 900 10000
Number of hidden layer nodes
Figure 3: WK_he relationship between the number of hidden layer
nodes of the BP neural network and the error rate of BP neural
network training results.
BP neural network
PSO-BP neural network
0
20
40
60
80
100Fitness value
10 20 30 40 50 60 70 80 90 1000
Iterations (time)
Figure 4: Comparison of optimal individual ﬁtness between PSO-
BP neural network and BP neural network.
end
start
Decoding to obtain the threshold and weight of 
BP neural network
Get the topology of BP neural network
Initialize BP neural network threshold and 
weight length
Randomly initialize the position and velocity of 
particles
Initial value of threshold and weight of coded 
BP neural network
Calculate the ﬁtness value of particles
Update particle extremum and particle swarm 
extremum
Update particle speed and position
Initialization related parameters
Whether the end conditions are met
Figure 2: Flow chart of PSO Algorithm Optimizing BP neural network.
6 Computational Intelligence and Neuroscience
the traditional BP neural network. When the traditional BP
neural network classiﬁes the emotion of four groups of
electronic music, the accuracy ﬂuctuates greatly. WK_he ac-
curacy of emotion classiﬁcation of four groups of electronic
music by PSO-BP neural network has been maintained at a
stable level, and its operation is more stable.
Figure 6 shows the emotional analysis results of elec-
tronic music in the test sample set based on PSO-BP neural
network electronic music emotional analysis model. It can
be seen from the results in the ﬁgure that based on the PSO-
BPneuralnetworkelectronicmusicemotionanalysismodel,
the data analysis is carried out from the characteristics of
electronic music and the pitch, length, speed, strength, and
timbre of its notes. On the basis of the data analysis results,
the emotion analysis of electronic music is further carried
out and the corresponding emotion analysis results are
output.
As shown in Figure 7, it is the comparison between the
emotional analysis results of electronic music based on the
PSO-BP neural network emotional analysis model and the
actualresults.Itcanbeseenfromtheresultsintheﬁgurethat
the error between the electronic music emotion analysis
results obtained by the electronic music emotion analysis
model based on PSO-BP neural network and the actual
results is small, which shows that it has a high accuracy of
electronic music emotion analysis and meets the expected
requirements.
To sum up, compared with the traditional BP neural
network, PSO-BP neural network has a faster convergence
speed, avoids the problem that BP neural network is easy to
fall into local optimization, and provides a more stable
operation performance for later model training and testing.
Multiple neural networks can be initialized by diﬀerent
parameter values, and the smallest one can be taken as the
result. Just like enterprise job rotation, try to start from
diﬀerent positions, which can avoid falling into the trap of
thinking that the current position is the most suitable. In
addition, “simulated annealing” technology can be used.
Simulated annealing will accept worse results than the
currentwithacertainprobabilityateachstep,whichhelpsto
“jump out” of the local minimum. As time goes by, the
probability of “optimal solution” should be continuously
reduced. WK_he emotion analysis model of electronic music
based on the PSO-BP neural network can complete the
0
10
20
30
40
50
60
70
0
5
10
15
20
25
30
123456789 1 0 1 1 1 2
Pitch
speed
intensity
timbre
length
output
Cheerful
Cheerful
Cheerful
quiet
lyric
lyricpassion
passionnervous Perseverance
Grief Calmly
Figure 6: WK_he emotion analysis results of electronic music in the
test sample set are analyzed based on PSO-BP neural network
emotion analysis model of electronic music.
Cheerful quiet lyric passion nervous Perseverance Grief Calmly
/T_his paper analyzes the results
Actual results
Music emotion
0
2
4
6
8
10
12
14
16
18
20Number of music / song
Figure 7: Comparison between the emotional analysis results of
electronicmusicandtheactualresultsbasedonthePSO-BPneural
network emotional analysis model of electronic music.
G r o u p  1G r o u p  2G r o u p  3G r o u p  4
BP neural network
PSO-BP neural network
70
72
74
76
78
80
82Accuracy (%)
Figure 5: Comparison results of PSO-BP neural network and
traditional BPneural networkin emotion classiﬁcationaccuracy of
electronic music.
Computational Intelligence and Neuroscience 7
emotion analysis of electronic music lyrics and music
melody with high accuracy. WK_here is less error between the
analysis results and the actual results, which meets the ex-
pected requirements of the model.
5.Conclusion
With the development of electronic music, the type and
quantity of electronic music are increasing. People need to
spend a lot of time and energy choosing their preferred type
in a large number of electronic music. WK_herefore, the clas-
siﬁcationofelectronicmusicandtheresearchoftheemotion
analysis model have become the research focus of electronic
music operation. However, the previous emotion analysis
models of electronic music have large errors in emotion
recognition in electronic music, which cannotmeet people’s
moreandmore detailedneeds. WK_hedevelopmentof artiﬁcial
intelligence and data analysis technology provides a new
development direction for electronic music emotion anal-
ysis. WK_herefore, this paper proposes electronic music emo-
tion analysis based on PSO-BP neural network and data
analysis. Based on the BP neural network optimized by the
PSO algorithm and combined with the extraction of emo-
tionalfeaturesof electronicmusic,theemotion of electronic
music is recognized and analyzed. WK_he experimental results
show that compared with BP neural network, PSO-BP
neural network has a faster convergence speed and better
optimal individual ﬁtness value, avoids falling into local
optimal solution and provides a more stable running state
foritstrainingandtesting.Atthesametime,ptheBPneural
network optimized by PSO has a lower error rate in the
emotional analysis of electronic music lyrics, which can
better identify and classify emotions. According to the
characteristics of electronic music, PSO-BP neural network
caneﬀectivelyidentifyandanalyzetheemotionofelectronic
music with high accuracy, which is close to the actual sit-
uation and meets the expected requirements. In this paper,
theemotionanalysismodelofelectronicmusicbasedonthe
PSO-BP neural network still has many shortcomings, which
need to be further improved and improved to improve the
performance of the emotion analysis model of electronic
music. Later, it needs to be further reﬁned according to the
characteristics of electronic music, which is closer to the
needs of human emotion.
DataAvailability
WK_he data used to support the ﬁndings of this study are
available from the corresponding author upon request.
ConflictsofInterest
WK_he authors declare that they have no conﬂicts of interest.
References
[1] X. Tang, C. Zhang, and J. Li, “Music emotion recognition
basedondeeplearning,”Computer knowledge and technology,
vol. 11, no. 10, pp. 232–237, 2019.
[2] M. Yuan and C. Li, “Research on global higher education
quality based on BP neural network and analytic hierarchy
process,”Computer and communication, vol. 9, no. 6,
16 pages, 2021.
[3] J. Qiu, C. Chen, and T. Zhang, “A Novel Multi-Task Learning
Method for Symbolic Music Emotion Recognition,” 2022,
https://arxiv.org/abs/2201.05782.
[4] B. Bhattarai and J. Lee, “Automatic Music Mood Detection
Using Transfer Learning and multiplayer perceptron,”In-
ternational Journal of Fuzzy Logic and Intelligent Systems,
vol. 9, no. (2), pp. 88–96, 2019.
[5] H. H. Tan, “Semi-supervised Music Emotion Recognition
Using Noisy Student Training and Harmonic Pitch Class
proﬁles,” 2021, https://arxiv.org/abs/2112.00702.
[6] H. T. Hung, J. Ching, S. Doh, N. Kim, J. Nam, and Y. Yang,
“EMOPIA: A Multi-Modal Pop Piano Dataset for Emotion
Recognition and Emotion-Based Music Generation,” 2021,
https://arxiv.org/abs/2108.01374.
[7] S. Hizlisoy, S. Yildirim, and Z. Tufekci, “Music emotion
recognition using convolutional long short term memory
deepneuralnetworks,”Engineering Science and Technology an
International Journal, vol. 24, no. 3, pp. 760–767, 2020.
[8] J. Liu, J. Huang, R. Sun, R. Xiao, and H. Yu, “Data fusion for
multi-source sensors using GA-PSO-BP neural network,”
IEEE Transactions on Intelligent Transportation Systems,
vol. 22, no. 10, pp. 1–16, 2020.
[9] L.Parisi,S.Francia,S.Olivastri,andM.S.Tavella,“Exploiting
Synchronized Lyrics and Vocal Features for Music Emotion
detection,” 2019, https://arxiv.org/abs/1901.04831.
[10] N. Takashima, F. Li, M. Grzegorzek, and K Shirahama,
“Cross-modal Music Emotion Recognition Using Composite
Loss-Based Embeddings,” 2021, https://arxiv.org/abs/2112.
07192.
[11] K. Kowsari, K. J. Meimandi, M. Heidarysafa, S Mendu,
L Barnes, and D Brown, “Text Classiﬁcation Algorithms,”A
survey. Information, vol. 10, no. (4), 150 pages, 2019.
[12] P. Wan, H. Zou, K. Wang, and Z. Zhao, “Research on hot
deformationbehaviorofZr-4alloybasedonPSO-BPartiﬁcial
neural network,”Journal of Alloys and Compounds, vol. 826,
Article ID 154047, 2020.
[13] H. P. Lee, J. S. Fan, and W. Y. Ma, “iComposer: an automatic
songwriting system for Chinese popular music,” inPro-
ceedings of the NAACL HLT, Minneapolis, USA, June 2019.
[14] A.Fh,B.Ma,andE.Smcd,“ContinuousEmotionRecognition
during Music Listening Using EEG Signals: A Fuzzy Parallel
Cascades model,” 2020, https://arxiv.org/abs/1910.10489.
[15] X. Zhang and Z. Jingjing, “An electronic music classiﬁcation
model based on neural network optimized by particle swarm
optimization,”Modern Electronics Technique, vol. 43, no. 9,
pp. 101–108, 2020.
[16] W. D. Dang, D. M. Lv, R. M. Li et al., “Multilayer network-
based CNN model for emotion recognition,”International
Journal of Bifurcation and Chaos, vol. 32, no. 1, 2022.
[17] R. Geetha and K. Priya, “Improvised emotion and genre
detection for songs through signal processing and genetic
algorithm,”Concurrency and Computation Practice and Ex-
perience, vol. 31, no. 3, e5065 pages, 2019.
[18] Y. Agrawal, R. Shanker, and V. Alluri, “Transformer-based
Approach towards Music Emotion Recognition from lyrics,”
2021, https://arxiv.org/abs/2101.02051.
[19]Y.Deng,H.Xiao,J.Xu,andH.Wang,“PredictionmodelofPSO-
BP neural network on coliform amount in special food,”Saudi
Journal of Biological Sciences, vol. 26, no. 6, pp.1154–1160, 2019.
8 Computational Intelligence and Neuroscience
[20] E. Koh and S. Dubnov, “Comparison and Analysis of Deep
Audio Embeddings for Music Emotion Recognition,” 2021,
https://arxiv.org/abs/2104.06517.
[21] C. Sun, C. Li, Y. Liu, Z. Liu, X. Wang, and J. Tan, “Prediction
method of concentricity and perpendicularity of aero engine
multistage rotors based on PSO-BP neural network,”IEEE
Access, vol. 7, Article ID 132278, 2019.
[22] H.WangandH.Zhang,“Visualmechanismcharacteristicsof
static painting based on PSO-BP neural network,”Compu-
tational Intelligence and Neuroscience, vol. 202110 pages,
Article ID 3835083, 2021.
[23] P. Gu, C. M. Zhu, Y. Y. Wu, and A. Mura, “Energy con-
sumption prediction model of SiCp/Al composite in grinding
based on PSO-BP neural network,”Solid State Phenomena,
vol. 305, pp. 163–168, 2020.
[24] X. Liu, Z. Liu, Z. Liang, S.-P. Zhu, J. A. F. O. Correia, and
A. M. P. DeJesus, “PSO-BP neural network-based strain
prediction of wind turbine blades,”Materials, vol.12, no. 12,
1889 pages, 2019.
[25] Y. Deng, H. Xiao, J. Xu, and H. Wang, “Prediction model of
PSO-BP neural networkoncoliform amount in special food,”
Saudi Journal of Biological Sciences, vol. 26, no. 6, pp. 1154–
1160, 2019.
Computational Intelligence and Neuroscience 9
