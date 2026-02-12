# construction-of-music-intelligent-creation-model-b

Research Article
Construction of Music Intelligent Creation Model Based on
Convolutional Neural Network
Jing Chen
Department of Music, Shandong Women’s University, Jinan, Shandong 250002, China
CorrespondenceshouldbeaddressedtoJingChen;28100@sdwu.edu.cn
Received 20 April 2022; Revised 5 June 2022; Accepted 11 June 2022; Published 5 July 2022
AcademicEditor:
GengxinSun
Copyright© 2022JingChen.M__hisisanopenaccessarticledistributedundertheCreativeCommonsAttributionLicense,which
permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.
M__heapplicationofmachinelearningtechnologytointelligentmusiccreationhasbecomeaveryimportantﬁeldinmusiccreation.
M__hemaincurrentresearchonmusicintelligentcreationmethodsusesﬁxedcodingstepsinaudiodata,whichleadtoweakfeature
expressionability.Basedonconvolutionalneuralnetworktheory,thispaperproposesadeepmusicintelligentcreationmethod.
M__hemodelusesaconvolutionalrecurrentneuralnetworktogenerateaneﬀectivehashcode,ﬁrstpreprocessesthemusicsignalto
obtainaMelspectrogram,andtheninputsitintoapretrainedCNNtoextractfromitsconvolutionallayers.M__henetworkspace
detailsandthesemanticinformationofmusicalsymbolsareusedtoconstructthefeaturemapsequenceusingselectionstrategy
forthefeaturemapofeachconvolutionallayer,soastosolvetheproblemofhighdatafeaturedimensionandpoorrecognition
performance. In the simulation process, the Mel cepstral coeﬃcient method (MFCC) was used to extract the features of four
diﬀerentmusicsignals,andthefeaturesthatcouldrepresenteachsignalwereextractedthroughtheconvolutionalneuralnetwork,
andthecontinuoussignalswerediscretizedandreduced.M__heexperimentalresultsshowthatthehigh-dimensionalmusicdataare
dimensionallyreducedatthedatalevel.Afterthedataarecompressed,thecorrectrateofintelligentcreationisashighas98%,and
thecharacteristicsignaldistortionrateisreducedto5%below,eﬀectivelyimprovingthealgorithmperformanceandtheabilityto
create music intelligently.
1.Introduction
M__he application of technology to the intelligent creation of
speech and the intelligent creation of musical elements has
become twoveryimportant ﬁeldsin theintelligentcreation
of patterns. M__he intelligent creation of speech has a good
development prospect in social production and life; the
intelligent creation of musical elements belongs to an im-
portant branch of intelligent creation of patterns, and has
been successfully applied in the ﬁelds of computer vision
such as military, medical, and industrial [1–3]. Since the
birth of the world, the research on convolutional neural
networkshasalsomadegreatprogress.Atpresent,thereare
hundreds of convolutional neural networks, among which
the representative ones are convolutional neural networks,
pattern recognition, music element processing, ﬁnance, in
the ﬁelds of voice intelligent creation, and music element
intelligent creation [4–6].
M__he rapid development of online music has provided
greatconvenienceformusicoperationstoacquiremusic.In
order to facilitate user selection, online music usually
classiﬁes music, and music classiﬁcation based on the in-
telligent creation layer is a common classiﬁcation method
[7–9].Atpresent,themainprocessoftheintelligentcreation
classiﬁcation system in the ﬁeld of music information re-
trieval is to ﬁrst manually extract the music features, then
train and model the classiﬁer, and ﬁnally input the music
features into the built model for intelligent creation clas-
siﬁcation. But now the manual music feature extraction
technology has encountered a bottleneck [10–13]. As a new
feature extraction technology, deep learning has achieved
excellent performance in the ﬁelds of music element pro-
cessingandnaturallanguageunderstanding.M__herefore,this
paper uses the powerful feature extraction function of deep
learning to ﬁnd music features that are more suitable for
intelligent music creation and classiﬁcation to design
Hindawi
Computational Intelligence and Neuroscience
Volume 2022, Article ID 2854066, 11 pages
https://doi.org/10.1155/2022/2854066
diﬀerentnetworkstructurestoclassifyintelligentlybasedon
these musical features. Since the same music may generate
diﬀerentintelligentcreationlayers,itisdiﬃculttogeneralize
the intelligentcreation layerofa single tagatthis time, and
multiple intelligent creation layer tags are needed to more
accurately and comprehensively summarize the intelligent
creation layer categories of a piece of music. At the same
time, the cognition of the music intelligent creation layer is
subjective,soitisnecessarytoprovideapersonalizedmusic
intelligent creation layer classiﬁcation for each music
operation.
Tothisend,thispaperstudiestheproblemofmultilabel
personalized classiﬁcation of music based on an intelligent
composition layer. M__his problem mainly includes two sub-
problems: the acquisition of the ground-truth labels of the
music intelligent creation layer and the personalized clas-
siﬁcation of music. In response to these two problems, this
paper ﬁrst proposes a method for calculating the person-
alized truth value of the music intelligence creation layer
based on network information and music operation tags.
M__hecreativelayerpersonalizedtruthvalueiscalculated;then
a method of mapping the music intelligent creative layer
truth value to multilabel categories is proposed, and the
speciﬁc intelligent creative layer category of music is ob-
tained; ﬁnally, a deep convolutional neural network and a
random K-label set are used for multilabel classiﬁcation of
musical sentiment with the application of PCA in the in-
telligent creation of handwritten digits. Although classiﬁers
such as convolutional neural network and SVM have good
stability and generalization ability, the high dimensionality
of image data makes the time complexity of the algorithm
very high, and redundant information will also aﬀect the
classiﬁcationofintelligentcreation.Inthischapter,principal
component analysis (PCA) is used to reduce the dimension
oftheimagedata,andthe784-dimensionalfeaturesofeach
image in the MNSIT database are reduced to N-59 di-
mensions. M__he experimental results show that the running
time of the SVM model using the PCA method is greatly
reduced, and the classiﬁcation accuracy is also improved.
2.Related Work
Withtheexplosivegrowthofdata,inthecontextoftheeraof
big data, hash learning plays an increasingly important role
in the ﬁeld of information retrieval. As an important di-
rection of machine learning, hash learning can reduce
communicationandstorageoverheadandimprovelearning
andretrievaleﬃciency.Ontheotherhand,deeplearninghas
been widely studied and applied in academia and industry,
andhasshownbetterperformancethantraditionalmachine
learningmethodsintheﬁeldsofspeechintelligentcreation,
natural language processing, and music element intelligent
creation. Recently, some deep hash learning methods have
been proposed by combining hash learning and deep
learning [14–16].
Zgank[17]proposedtorealizecreationlayerbasedona
two-layer classiﬁer. M__he ﬁrst layer uses the bag-of-users
model, which is mainly used for training the general in-
telligent creation layer classiﬁcation of music; the second
layerusesresidual,themodelismainlytrainedtopredictthe
intelligentcreativelayercognition.AnantrasirichaiandBull
[18] believes that the two-layer classiﬁcation method is
superior to the traditional one-layer classiﬁcation method
because the method treats the music content itself and
speciﬁc individual music operations separately. Solankiand
Pandey [19] proposed a method based onactive learning to
realizethepersonalizedclassiﬁcationofthemusicintelligent
creationlayer.M__hemethodﬁrstlabelsthemusicdataset,and
then invites the experimenter to listen to the music on the
web page. We can think of this method as an explicit
feedback method based on music manipulation. One of the
key problems of personalization is the burden of music
operation.Inordertorealizethepersonalizationofdiﬀerent
individuals, the participation of music operation is inevi-
tablyrequiredtoensuretheeﬀectofpersonalization,buttoo
much participation is also a burden to music operation.
Chemicaltechnologyhasatrade-oﬀinbothaspects.Buehler
[20] believes that in the aspect of personalization of the
music intelligent creation layer, in order to reduce the
participation of music operation, it is appropriate to design
less music and music operation interaction.
M__heprocessingofthetruevalueofthedataisdiﬀerent.It
ﬁrst needs to group all music operations according to in-
dividual information. For example, according to age
grouping, and according to cultural background, music
operationscanbedividedintoorientalculturelikeWestern
Culture Group [21–24]. After being divided into groups,
eachgroupiscalculatedaccordingtotheaveragevalueofthe
music operation labels of all members in the group.
M__herefore, for personalized music classiﬁcation based on
network information, the burden on music operation is
almost zero [25–27].
3.Music Grading Based on Convolutional
Neural Network
3.1. Convolutional Neural Network Hierarchy Division.
M__he layers in the convolutional neural network sort each
element of the vector according to the value ofe,
(0≤i≤n −1) from large to small to obtain a new (creation
layertruthvalue,subscriptvector),andselectthekwiththe
most signiﬁcant weight elements, the corresponding cate-
gorycanbecalculatedthroughthesubscriptvaluesofthesek
elements, and ﬁnally the ﬁnal category of the song can be
calculated for “Music Operation.” M__he time complexity of
the algorithm mainly depends on the sorting time. M__he
complexity isO(nlogn), whereiis the number of classiﬁ-
cation labels.
First of all, it is necessary to collect the music operation
network relationship set:
y(x, k) �
􏽘 x(k, k −1)exp(nt),
􏽘 x −exp −
2pi
nt􏼒 􏼓 .
⎧⎪⎪⎪⎪
⎨
⎪⎪
⎪⎪⎩
(1)
For example, in the network diagram, starting from the
nodesinFigure1,whichnodescanbereachedbymovinga
2 ComputationalIntelligenceandNeuroscience
step to the adjacent nodes, that is, which music operations
themusicoperationufpaysattentionto;startingfromtheuf
node, which nodes can be reached by moving two steps to
the adjacent node, which can be regarded as the indirect
attention to music operation of the music operationU, and
so on to calculate the distance to other music operations.
And it is also necessary to collect the intelligent creation
layerclassiﬁcationlabelsofitselfandothermusicoperations
forallsongs,whicharerepresentedbythemusicintelligent
creation layer label vector label set:
s(m, n)exp(−it/nt)
1 −exp(−it/nt) − (m −1)exp(−i − t/nt)
1 +exp(−it/nt) −1 �0. (2)
We represent the network relationship between music
operations by a directed edge with an edge weight of 1 in
graph theory. We regard music operations as points of a
directed graph. When music operationsufpay attention to
musicoperationsuf,wecanuseit.IntheFlayer,ﬁrstarrange
each feature map obtained by the S4 layer into a column
vector,eachfeaturemaphas13×13�169features,andthen
connectallthecolumnvectorsinturn,andtheﬁnalnumber
offeaturesobtainedis169×10�1690.M__heextractedfeatures
are input into the SVM classiﬁer to obtain the ﬁnal classi-
ﬁcation result.
3.2. Network Dimensionality Reduction Processing.M__he
number of convolutional layers and the size of the convo-
lution kernel of the ﬁrst convolutional layer, and the
hyperparameters related to dimensionality reduction pro-
cessing: learning rate, and achieve satisfactory classiﬁcation
performance. It must be carefully adjusted before. In the
experiments in this chapter, the set hyperparameters are
used without data augmentation:
1 − k, 0<k <f(k) −1,
0, f(k) − 1 <k <f(k) +1.
􏼨 (3)
M__heintelligentcreationrateofGTZANdatasetisaround
73.6%. Given more detailed information on musical style
classiﬁcation, in the form of a confusion matrix, where the
columns correspond to the actual styles, the rows corre-
spond to the predicted categories, and the percentage of
correct classiﬁcations is located on the diagonal of the
matrix.Duetotheunclearboundariesbetweensomemusic
styles, misjudgment is easy to occur. For example, some
classicalmusichasastrongrhythmandiseasilymistakenfor
iazzmusic;andlockmusiciseasilymistakenforotherstyles
due to its wide range of characteristics, so its classiﬁcation
accuracy is lower than other styles.
SinceCNNhavemanyparameterstolearn,theycannot
betrainedeﬃcientlyunlessthereareenoughtrainingmusic
elements as shown in Figure 2, so data augmentation has
become important to generate more samples of music ele-
mentsandshouldlistvariousdiﬀerencestogainrobustness:
􏽘
x(k, k −1)
1 −exp(−2(pi/nt))− k 􏽐 x(k)exp(−2(pi/nt))
exp(n) −x(n) �0. (4)
However,theexperimentalresultsofthischapteraretoo
lowtomakeaveryreliablejudgment.Afterfurtherresearch,
itisfoundthatthevariationofmusicrepertoireisveryrich,
so it is not enough to use 100 tracks to represent various
variations of a particular genre, and compared with the
eight-layernetworkstructure,thetrainingdatainthisarticle
are too small, so that the ﬁnal classiﬁcation result is not
particularlyideal.Itcanbeforeseenthatwiththeincreaseof
music repertoire, the intelligent creation eﬀect of this
chapter will be further improved.
3.3.PrincipalComponentAnalysisofMusic.M__heﬁrsttypeof
music principal component analysis is to increase the
training sample. We extract random 224×224 small pieces
of music elements from the 256×256 music elements. M__he
extracted music elements diﬀer from the original music
elementsby32pixels,sothemainpartshouldcontaininthe
trainingset. M__heﬁrst-Toe method is to use PCA toenhance
the training data: a PCA transformation is performed for
each RGB music element to complete the denoising
function:
k(m, n) −1
k(m, n) +1 − 􏽘 x(k) − k(m, n)
k(m)k(n) −1 �1. (5)
In theSlayer, the pooling methods usually selected are
averagepoolingandmaxpooling,andtheaveragepoolingis
selected in this chapter. After passing through the S layers,
the resultingmatrixrow andcolumnscalesarehalf thesize
ofthepreviouslayer.Itshowsthatthefeaturesoftimeseries
and frequency series are manually extracted and put into
CNNnetworktrainingindiﬀerentcombinations,andﬁnally
diﬀerent eﬀects will be obtained. Among them, the intelli-
gent creation rate obtained when all three feature maps are
input into the network is the highest, indicating that better
results can be obtained only when the training features of
Figure 3 are more comprehensive.
Tosamplethemaximumfrequencythatcanbesensedis
20,000Hz, you need at least 40,000 sampling points per
second.M__heusualsamplingrateforrealaudioﬁlesis44,100
persecond,slightlymorethan40,000,sowehavetoconsider
0.0
–0.1
–0.2
–0.3
–0.4
–0.5
–0.6
2468 10 2468 1 0
Hierarchical set ratio of a Hierarchical set ratio of b
Convolutional neural network negative value
Figure 1: Convolutional neural network hierarchical relationship
set.
ComputationalIntelligenceandNeuroscience 3
thesameproblemwhenwecompressanduseatleast40,000
unitsforinput.Afterobtainingtheemotionaltruthvalue,for
eachsong’sinitialvalueofthetruthvalueiszerovector,this
paperproposesanovelmethodtomapthetruthvaluetothe
speciﬁcvalue.M__heweightedvotingproposedinthispaperis
diﬀerent from ordinary voting. It mainly assigns certain
weightstothevotesofdiﬀerentusersaccordingtothenode
distance in the social network. In the process of accumu-
latingtheweightsofallvotes,diﬀerentweightsvaluevoting
has diﬀerent eﬀects on musical emotion:
􏽘
x(k)
ln k −
����
x(k)
􏽰
− |k(m, n)|
|k(m) − 1| �1. (6)
M__hequantitativeresultsofMAEandMSEonthePartA
dataset are compared with several algorithms that perform
well in this ﬁeld. As can be seen from the above table, in
terms of MSE, the stability error of the algorithm proposed
inthischapterismuchsmallerthanthatofotheralgorithms,
and the error is reduced by an average of 2.08% compared
with the benchmark MCNN. In addition, for the MAE
indicator,itsalgorithmestimationaccuracyerroriscloseto
MCNN, the best performing algorithm for this indicator.
3.4. Network Convolution and Nesting.First, the spectral
networkconvolutiongraphofeachmusictrackisgenerated,
and the time and frequency features of the music track are
extracted using the HPSS algorithm. M__he spectrograms are
input to the CNN network together; by adjusting the net-
work parameters, the ﬁnal intelligent creation result is ob-
tained after training and testing:
􏽘 h(k, t − k +1) + 􏽘
k
h(k, t −2) � k 􏽘 h(k, t −1) + · · ·
+ h(k,1) +1.
(7)
Usually dropout and momentum can improve learning.
Sinceittakesalongtimeforthenetworktoconvergeusing
dropout for all layers, in the experiments of this chapter.
Figure4containstwoconvolutionallayers(layerC),two
poolinglayers(layerS),afullyconnectedlayer(layerF)and
an output layer. In theC layer, the size of the convolution
kernelissetto5×5,thenumberofconvolutionkernelsis5
and10,andthewindow-movingstepis1.IntheSlayer,the
pooling methods usually selected are average pooling and
maximumpooling,andtheaveragepoolingisselectedinthis
chapter:
m(x, t − y +1) − m(x, t −1)
f(x, t − y +1) − f(x, t −1)
􏼌􏼌􏼌􏼌
􏼌
􏼌􏼌􏼌
􏼌
􏼌􏼌􏼌
􏼌
􏼌􏼌􏼌 +
m(x,1) − m(x, t −1)
f(x,1) − f(x, t −1)
􏼌
􏼌􏼌􏼌
􏼌
􏼌􏼌􏼌
􏼌
􏼌􏼌􏼌
􏼌
􏼌􏼌􏼌 >1.
(8)
M__henullhypothesisandalternativehypothesisofdigital
information data are as follows: assumingt�0, if the ADF
test value is greater than or equal to the critical value at a
certain conﬁdence level, the original hypothesis wind is
accepted:Y �0, indicatingthat the sequence has a unit root
and is nonstationary. If the ADF test value is less than the
criticalvalueatacertainconﬁdencelevel,thenullhypothesis
dateisrejected,indicatingthatthesequencehasnounitroot
and is stable. However, music emotion itself is subjective,
and it is based on various inﬂuences, so even if the classi-
ﬁcation accuracy of the trained emotion classiﬁer reaches
100%, it is only based on the average emotion cognition of
the public. For diﬀerent individuals, the classiﬁcation ac-
curacy is not necessarily the best.
4.ConstructionofanIntelligentMusicCreation
Model Based on Convolutional
Neural Network
4.1. Convolutional Neural Network Feature Extraction.A
total of 20,000 iterations are performed on the network
convolution training samples, when the learning rate is
relatively small, the learning process will be very slow, and
the intelligent creation rate is still unstable. Appropriate
1.0
0.8
0.6
0.4
0.2
0.0
0 2468 10
Numerical analysis of Music reality service
Principal components of factor
extraction information
label a
label b
Figure 3: Music principal component scale factor analysis.
0
2
4
6
8 9.6
9.8
10.0
10.2
10.4
0.0
0.2
0.4
0.6
0.8
Node teaching convolutional kernel
Numerical reduction of data
The numerical value of
dimensionality layer
Figure 2: Dimensionality reduction processing of convolution
kernel network in convolution layer.
4 ComputationalIntelligenceandNeuroscience
improvement can eﬀectively improve lack of eﬃciency. In
the paper, we found some image data with large estimation
erroraccordingtotheorderofgroupID.Wefoundthatthe
modelperformedpoorlyinsomecaseswherethescenewas
too dense or the background was too complex. For this
reason, we made curve statistics on the population distri-
butionofdatasetsA and B.Inordertoﬁndtheimbalanced
distribution of the data set itself, the training set rarely
contains these complex scenes for learning, resulting in a
largeerrorintheestimationofafewextremelydensescenes
inthetestset.Inaddition,thescenemigrationabilityofthe
model needs to be further explored:
1 <f(m, n)<
����
x(k)
􏽰
−
�������
x(k) −1
􏽰
−
�������
x(k) −2
􏽰
<f(m, n) −1.
(9)
M__he stationarity test of time series means that the sta-
tisticallawoftimeseriesdoesnotchangewiththepassageof
time, that is, the characteristics of the random process that
generates variable time series data do not change with the
changeoftime.Mostoftheeconomicvariabledatainvolved
in economic analysis are time series data, and most of the
economictimeseriesarenonstationary,soitisnecessaryto
test the stationarity of the observed time series data.
A total of 50 training rounds, batch size is 25, initial
learningrateis0.8,convolutionkernelsizeis25,maximum
channel number is 128, cavity coeﬃcient is 1, step size is 1,
thenumberofunitsusedbytherecurrentneuralnetworkis
128, the size of convolution kernel connected between re-
sidual networks is 9, loss weight is 0.1 and 2.5E−4. M__he
emotion truth value involved in the emotion-based multi-
label personalized classiﬁcation in this paper is inherently
subjective, and it is almost impossible to reach consensus
among all cognitive viewpoints in terms of emotion cog-
nition, so it belongs to the second type of truth value. M__his
section mainly discusses the truth value of music emotion
involved in this paper. Experimental results show that the
proposed CRNNH can achieve superior performance
compared to other advanced hashing methods (Figure 5).
4.2. Algorithm Training for Intelligent Music Creation.
M__hismodelisusedwhenthenumberofcategoriesofmusic
intelligentcreationdataisgreaterthantwocategories.For
example, in music classiﬁcation, music signals are clas-
siﬁed into one of folk songs, guzheng, rock, and pop; in
Section 4, the classiﬁcation of handwritten digital intel-
ligent creation, the data labels are 10; in document clas-
siﬁcation, the model data can be grouped into one of
several categories such as sports, economics, entertain-
ment, technology, and more:
︷f(m, n) −f(m −1, n−1), g(m, n) −g(m −1, n−1)
f,g <1
⟶ [F(m, n), G(m, n)]. (10)
According to the music retrieval method based on ex-
ample semantics, use the improved model to learn the se-
manticvectorofmusic,usethesemanticvectortocompare
the similarity with the marked data set in the database, and
return the similarity in the semantic space according to the
cosine similarity calculation method. music. In the experi-
ment,themusicinthetestsetisobtainedbytheconvolution
model to obtain the semantic vector, and then the return
value is obtained in the labeled corpus. If the labeling ac-
curacyofthealgorithmishigh,theoriginalsongsmanually
the intelligent
creation rate
improve lack
improvement handwritten
numbers
performance learning
process unstable
classification
convergence dimensionality
reduction
oscillation
network
convolution
convolution and
nesting
training samples
the spectral network
the learning process
feature
feature
featuresequence
sequence
sequence
information
details details
1–exp (x)*exp (y)
1–exp (x+y)
Figure 4: Network convolution pooling topology.
ComputationalIntelligenceandNeuroscience 5
labeled in the corpus can be returned after retrieval.
M__herefore, set theK value in Figure 6, and ﬁnd the per-
centage of the ﬁrst K values that can be returned to the
original song.
Firstofall,wecanseethatthetwotagsofregionalwind
and rock do not belong to the intelligent creation layertags
selected in this paper, so they are directly discarded, so the
processed tags are (moved, quiet) and (passion, joy), re-
spectively. Assuming that the musicm0,m1, m2 belong to
albumo, andm3,m4, m5 belong to albuml, we pass the
intelligent creation layer of the playlist to the music in the
playlist, then the intelligent creation layer label ofm0,m1,
m2is(moved,quiet),whilethesmartcreationlayersform3,
m4, andm5 are labeled (passion, joy):
Dertimerst(k, k−1) −Dertimerst(1,1) ∈K(0,1),
hermerts(k) −k ∈K(1,1).
􏼨 (11)
For the convenience of discussion, we may assume that
thesubscriptsequenceoftheintelligentcreationlayerinthis
example is moving, loneliness, quiet, warmth, romance,
healing, sadness, missing, passion, joy, lovelorn, and nos-
talgia. Som, m1, m2 smart authoring layer labels can be
representedbyvectorsas(1,0,1,0,0,0,0,0,0,0,0,0),m3,
m4, m5smartauthoringlayerlabelscanberepresentedbya
vector as (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0).
4.3. Optimization of the Authoring Model Structure.M__he
larger the number of participants in the experiment, the
easier it is to collect more data, but the problem is that it is
more diﬃcult to achieve a consistent perception of many
musicalemotions.Whenitisdiﬃcultforthesamemusicto
achieve the same emotional perception among diﬀerent
users,thesemethodsusuallyaveragetheclassiﬁcationlabels.
M__hatis,thelossiscalculatedateachstageofthenetwork,so
as to ensure the normal parameter update in network
trainingandsolvetheproblemthattheover-deepnetworkis
diﬃcult to optimize. By analyzing and comparing a large
number of experimental results, it is found that the MSE
index of the proposed algorithm is reduced by 2.08% on
averagecomparedwiththebenchmarkonthePartAdataset
forTable1,sothispretrainedconvolutionalnetworkisused
to extract convolutional feature maps.
Inthisalgorithm,eachnodeisvisitedatleastonce.Ifthe
eﬀective attention relationship is deﬁned as the attention
relationshipinwhichthefolloweduserexistsintheuserset
we selected. M__hen, each eﬀective attention relationship al-
gorithm will only be visited once, so its time complexity
depends on the number of nodes in the directed graph and
1.0
0.5
0.0
–0.5
–1.0
125
100
75
50
25
0
1 23456
123 456
Extracting spectral distribution of features
The case of CNN data Numerical value of error (%)
Figure 5: Convolutional neural network feature extraction spectral distribution.
0.4
0.2
0.0
–0.2
–0.4
0.2 0.4 0.6 0.8 1.0
Authoring layer label identification distribution
Smart distribution for CNN parameter amplitude value
Figure 6: Label distribution of intelligent authoring layer of
convolutional neural network.
6 ComputationalIntelligenceandNeuroscience
thenumber ofeﬀectiveattention,so the timecomplexity of
the entire algorithm is:O(m), the algorithm will only visit
once, so its time complexity depends on the number of
nodes in the directed graph and the number of eﬀective
attention, so the time complexity of the entire algorithm is:
O(max(IEI, IUl)), where IEI is the number of eﬀective at-
tention for music operations, IUI is the size of the music
operation set we have chosen:
∀w(i, j) �1, ∃w(i) +w(j) + h(1 − h)
∗w(i −1, j−1) + h �1.
(12)
First normalize, the classiﬁcation eﬀect is the best. Each
sampleinthedatasetis28 ∗28 insize,thatis,784-dimensional
data,whichmeansthateachsamplehas784-dimensionaldata,
whichnotonlyincreasesthetrainingtimeofthesamplebutalso
aﬀects the processing performance of the classiﬁer. M__hat is, the
variablesarenonstationary,butacertainlinearcombinationof
themmaybestationary,thatis,agroupofvariablesmaintaina
trend of a group of linear relations within a certain period of
time,thereisacointegrationrelationshipbetweenthevariables,
regression is also useful, a certain linear combination of non-
stationary variables can correctly reﬂect the long-term rela-
tionship between them.
5.ApplicationandAnalysisofMusicIntelligent
Creation Model Based on Convolutional
Neural Network
5.1. Convolutional Neural Network Data Pooling.In the
intelligent creation classiﬁcation of convolutional neural
network, but when users actually use, only for decoding
operation, longer but can obtain better compression eﬀect,
can retain encoder part accordingly, and calculation of
compression always borne by the service side, although the
circulation of the neural network parallel eﬃciency is quite
short, but the decoder does not include circulation part of
the neural network, can avoid the high complexity of the
neuralnetwork.M__hevalueofthelearningrate77isusuallyin
[0,1].Learningrate77istoolargeortoosmallwillaﬀectthe
performance of the network:
o(k, k −1) �
􏽘 h(k)w(i, k) ⟶ o(k),
􏽘 a ∗h(k) − b ∗w(i, k) ⟶ o(k −1).
⎧⎪⎨
⎪⎩
(13)
M__hevariablelearningratemeansthatthelearningrateis
relativelylargeintheearlystageofnetworktraining,andas
the training process progresses, the learning rate decreases
continuously, so that the network in Figure 7 tends to be
stable.
M__he loadof these two growth cofactors isbelow 0.5,but
the other factors are above 0.5, indicating that the other
variables have high validity. In terms of the price of digital
lamination or services, the average score is 3.76, and the
standard deviation is 0.73, which is above the middle level.
M__herefore, the corresponding model compression can only
be carried out on the decoding end part.
5.2. Realization of Music Intelligent Creation Simulation.
Users cannot directly attach emotional labels to music, but
canonlycreateaplaylist,addaseriesofmusictotheplaylist,
and then attach emotional labels to the playlist, indicates
which categories the songs in the playlist are classiﬁed into
fortheuserwhocreatedtheplaylist.Sincethelabelsattached
byuserstotheplaylistarenotlimitedtoemotionalcategory
labels, we need to ﬁlter the labels, and directly discard the
labels that do not belong to the classiﬁcation category we
deﬁned.M__herefore,thispaperadoptsanimprovedalgorithm
tooptimizetheC and gparametersinSVM,andproposesa
supportvectormachineoptimizationbasedontheimproved
music element group algorithm, the algorithm steps are as
follows: (1) Input the training samples with features
extracted by the Mel cepstral coeﬃcient method; (2) Ini-
tialize the penalty factorcand kernel function parameterg
of the SVM; (3) Initialize the position and velocity of the
population, use the accuracy rate obtained by SVM as the
ﬁtnessfunctionofthePSOalgorithm;(4)Updatethemusic
element and calculate the ﬁtness function value of the
updatedmusicelement.Atthistime,thepenaltyfactorcand
thekernelfunctionparametergare,respectively,are73.829
and 0.71441:
o(x, y) −
1 −exp(x + y)
1 −exp(x)∗exp(y) −1 −exp(x + y)
1 +exp(x + y) ⟶
x
−y <1 1−exp( ���� �x + y√ ). (14)
Given a piece of music element it, and the size and
number of feature maps of a sample after passing through
the layer are diﬀerent, so the model intelligently composes
multiple tags of diﬀerent musical clips from the Magna-
TagATune dataset, which have diﬀerent styles, moods, and
other information about the music. M__he purpose of this
model is to correctly and intelligently create the labels of
music ﬁles, and randomly scramble the dataset used for
experiments. M__he model in Figure 8 was trained for over
60,000 iterations and completed 100 epochs.
Using regularization matrix three to control the quan-
tizationerror.Anotheradvantageofthree-1regularizationis
that compared with L2 regularization, it requires less
computational cost and has sparseness, that is, its training
processcanbesmoothlyaccelerated,andmorehashbitsare
1 or 0.1, can generate more eﬃcient hash codes. However,
optimizing the three-1 regularization term may cause the
binarycodetobecomposedof1s,whichwillaﬀecttheﬁnal
performance. M__his is because the optimization of the reg-
ularizationwill aﬀectthe balanceofthehash code. Inorder
ComputationalIntelligenceandNeuroscience 7
to maintain the balance of the hash code, the square sum
balancecriterionofthemeanvalueofthehashcodeisused,
andthebalancecriterioncanmakethehashcodeeverybitis
as consistent as possible a 1 or 0.
5.3. Example Application and Analysis.M__he weighted music
operation proposed in this paper is diﬀerent from the or-
dinary music operation. It mainly assigns certain weights to
themusicoperationsofdiﬀerentmusicoperationsaccording
tothedistanceofthenodesinthenetwork.M__herefore,wecan
usually think that in the image space, the local pixels are
relatively closely related, while the distant pixels are weakly
related. With local awareness, training parameters can be
minimized by simply computing the relationship between
each element of the input data and its local neighbors.
For music operation, the music in the training set of it
(may be set to mf), we set the true value of the intelligent
creationlayerofthemusicoperationtothemusicmfasthe
true value of the music intelligent creation layer of the
training set, which needs to be calculated and obtained by
the method proposed in this article, which is also the main
workofthepersonalizationofthemusicintelligentcreation
layer,seefordetails;forthemusicinthemusicoperationui
testset(maybesetasmk),wesetthemusicoperationtothe
musicmk’s truevalueoftheintelligentcreationlayerasthe
training set music intelligence in the truth value of the
creation layer, which can be obtained directly through the
smartcreationlayertagofthemusicoperation.Inthispaper,
unless otherwise speciﬁed, all the true values of the music
intelligent creation layer mentioned in Table 2 refer to the
truevaluesofthetrainingsetmusicintelligentcreationlayer.
M__hesizeofitscoeﬃcientrepresentsthesizeofreliability.
WhentheCronbachcoeﬃcientisabove0.6,thereliabilityis
acceptable.When theCronbach coeﬃcientis below0.6,the
reliabilityisinsuﬃcient,onlyaverageclassiﬁcationaccuracy
of the convolutional neural network using the variable rate
in Figure 9 also reached 92.6% and 91.2%, which are also
higher than 90.20% of the traditional convolutional neural
network.
M__hisexperimentinvestigatestheimpactoflayers,sothe
feature map sequence contains {40, 80, 120, 160, 240, 320}
network
network
problem
optimum performanceperformance
Problem learning rate
learning rate
the network is easy
fall into local
optimum
the learning and
training process
solve the above problem
adopt the additional
momentum method
music intelligent
creation model
the weights and bias vectors
classification of
convolutional neural
get a stable solution
the traditional
convolutional
neural network
based on
convolutional
neural network
the intelligent
creation
Figure 7: Network data pooling input pretrained network.
Table 1: Authoring model structure optimization algorithm.
Authoring model text Optimization algorithm steps
w(i) + w(j) in the input layer Import matplotlib.pyplot as plt
Between eachh (1 − h) layer Import numpy as np
M__he number of nodes Import matplotlib as mpl
Excitation function
����
x(k)
􏽰
Import settings
Initialize the connection weights g (m, n)of the hidden layer
Determine the rate andf (m, n) X �np.arange (1, st.tot_det-1, st.step)
Initialize the thresholdsw (i, j) Y �np.arange (1, st.tot_det-1, st.step)
1 −exp(x + y) Hidden layer and input layer
Calculate thek(m) −1 hidden layer 􏽐 h(k)w(i, k) −a ∗h(k) − b ∗w(i, k) ⟶ t
Dertimerst(c, c −1) ∈[0,1,2, . . ., c −1] Output layer of the network
8 ComputationalIntelligenceandNeuroscience
featuremaps,thesmartcreationresultsofdiﬀerentnumbers
of feature maps are shown in the ﬁgure, it can be seen that
when bow is set to 24, CRNNH can obtain better smart
creation accuracy. M__he intelligent creation results of feature
maps of diﬀerent sizes are shown in the ﬁgure. Better in-
telligentcreationresultscanbeobtainedwhentheimagesize
is 6∗6. M__he two features greatly reduce the training
parametersoftheneuralnetwork;atthesametime,theyalso
beneﬁt from the powerful feature abstraction ability of the
convolutional neural network. Similarly, music also has
some characteristics of images, such as local perception, so
this paper also combines it with the powerful feature ab-
stractionabilityofconvolutionalneuralnetworktoperform
multi-labelemotionclassiﬁcationformusic,theﬁrstisgood
robustness to imbalanced datasets, and the second is a
simple serve as metrics for the entire dataset description in
Figure 10.
M__he experiment uses MAP (mean average precision)
and AUC (the area under the receiver operating charac-
teristic curve) as evaluation indicators. MAP ﬁnds the
average correct rate for each point in the ranking for each
retrievedsong.M__hetrainingprocessofCNNisdescribedin
detail,andtheperformanceofthenetworkunderdiﬀerent
sizesofconvolutionkernelsiscompared,andthesizeofthe
convolution kernel that can achieve the best network
performance is screened. M__he ROC curve reﬂects the
change in the probability of a positive case being classiﬁed
as a positive case and the probability of a negative case
being mistakenly classiﬁed as a positive case. M__he value of
AUC is the size of the area below the ROC curve. Usually,
the value of AUC is between 5 and 10, a larger AUC
representsbetterretrievalperformanceistoreturnasorted
list according to the decision value for each label in the
dataset, and average the retrieval results of all labels. M__he
learning result of the convolutional neural network is
performed,andCNN-ELMistheresultofthedatasetbeing
–4
–2
0
2
4
–4
–2
0
2
4
–1.01
–0.79
–0.56
–0.34
–0.11
0.11
0.34
0.56
0.79
1.01
The sparsity distribution of music
Distribution element data
The value of intelligent
composition
Figure 8: Sparsity distribution of intelligent music creation.
Table 2: Training set music intelligent creation instructions.
Creation layer Instructions rate 1 Instructions rate 2 Instructions rate 3 Instructions rate 4
10 0.121 0.993 0.322 0.666
20 0.004 0.553 0.346 0.117
30 0.219 0.213 0.638 0.404
40 0.661 0.742 0.559 0.037
50 0.318 0.338 0.295 0.825
60 0.006 0.086 0.412 0.385
The weights of the convolutional neural network
value 3
value 2
value 1
value 8
value 7
value 6
value 5
value 4
1
2 3
4
5
Figure 9: Convolutional neural network weight music operation.
ComputationalIntelligenceandNeuroscience 9
adjusted by the SMOTE algorithm and then classiﬁed by
theELMnetwork.CNN-ELMobtainshigheraccuracyand
F value, while CNN-SMOTE has higher recall, so the re-
trievalresultswillbebetterthanotheralgorithms.Itcanbe
seenthatCNN-SMOTEreturnssevensongsthatmatchthe
labelsearch terms, which are better thanthe results before
adjustment.
6.Conclusion
In order to accurately describe the ability of intelligent
music creation, this paper uses the convolutional neural
network segmentation algorithm to obtain the pitch fre-
quency of each intelligently created note. A melody rep-
resentationmodel wasestablishedfor themusic data set to
be retrieved and the input music samples, a genetic algo-
rithmwasdesignedtoestablishanapproximationtemplate
for intelligently created music, and the individual diﬀer-
ences in the input of intelligently created music were
corrected, thereby improving the retrieval accuracy. In
orderto speed upthe retrieval speed,a local hash-sensitive
algorithm for intelligent creation retrieval is designed, and
anindexisestablishedforthemusicdatabase.M__helabeldata
of the music intelligent creation layer collected from the
online music platform is represented by a vector. For a
speciﬁc music operation, the true value of each music is
calculated by the weight accumulation method of the label
data of other music operations. In order to overcome the
“semanticgap”problem,themusicismappedtoasemantic
space, the convolutional neural network model is used to
obtain the music semantic features, and the semantic an-
notation vector is generated for the music according to the
semantic features. Replace the Softmax classiﬁer in CNN
with the SVM classiﬁer, and compare it with the classic
CNN and other related literature. Experiments show that
themodelcanstillobtainbetterlabelingresultswhenthere
are few manually labeled music in the dataset and the la-
belingsamplesareunevenlydistributed,andcanachievethe
goal of retrieval in the semantic vector space, and obtain a
higher score.
Data Availability
M__he data used to support the ﬁndings of this study are
available from the corresponding author upon request.
Conflicts of Interest
M__he authors declare that they have no known competing
ﬁnancial interests or personal relationships that could have
appeared to inﬂuence the work reported in this paper.
Acknowledgments
M__his work was supported by Department of Music, Shan-
dong Women University.
References
[1] C. H. Yu and M. J. Buehler, “Soniﬁcation based de novo
protein design using artiﬁcial intelligence, structure predic-
tion, and analysis using molecular modeling,”APL bioengi-
neering, vol. 4, no. 1, Article ID 016108, 2020.
[2] D. Chaudhary, N. P. Singh, and S. Singh, “Development of
musicemotionclassiﬁcationsystemusingconvolutionneural
network,”International Journal of Speech Technology,vol.24,
no. 3, pp. 571–580, 2021.
[3] Y.Ma,Y.Yu,andZ.Ma,“Distributedsoundtransmissionand
smart city planning management based on convolutional
neural network,”Wireless Communications and Mobile
Computing, vol. 2, pp. 18–22, 2022.
[4] X. Jia, “A music emotion classiﬁcation model based on the
improved convolutional neural network,”Computational
Intelligence and Neuroscience, vol. 2, pp. 12–16, 2022.
[5] K.Y.Wang,Y.L.Ho,andY.D.Huang,“DesignofIntelligent
EEG System for Human Emotion Recognition with Con-
volutional Neural network,” inProceedings of theArtiﬁcial
Intelligence Circuits and Systems (AICAS),pp.142–145,IEEE,
Hsinchu, Taiwan, March 2019.
[6] O. Lopez-Rincon, O. Starostenko, and G. Ayala-San Mart´ın,
“Algoritmic Music Composition Based on Artiﬁcial Intelli-
gence: A survey,” inProceedings of theElectronics, Commu-
nications and Computers (CONIELECOMP), pp. 187–193,
IEEE, Cholula, Mexico, February 2018.
[7] C. H. Chuan and D. Herremans, “Modeling temporal tonal
relations in polyphonic music through deep networks with a
novel image-based representation,” inProceedings of the
AAAI Conference on Artiﬁcial Intelligence, vol. 32, no. 1,
February 2018.
[8] C.H.Yu,Z.Qin,andF.J.Martin-Martinez,“Aself-consistent
soniﬁcation method to translate amino acid sequences into
musicalcompositionsandapplicationinproteindesignusing
artiﬁcialintelligence,”ACSNano,vol.13,no.7,pp.7471–7482,
2019.
[9] R. Sarkar, S. Choudhury, and S. Dutta, “Recognition of
emotion in music based on deep convolutional neural net-
work,”Multimedia Tools and Applications, vol. 79, no. 1,
pp. 765–783, 2020.
[10] Z. Yu, X. Xu, and X. Chen, “Temporal pyramid pooling
convolutional neural network for cover song identiﬁcation,”
IJCAI, pp. 4846–4852, 2019.
[11] L.CaiandQ.Cai,“Musiccreationandemotionalrecognition
using neural network analysis,”Journal of Ambient Intelli-
gence and Humanized Computing, pp. 6–10, 2019.
8
6
4
2
0
02468
Network neural layer node
The mean square error of music
intelligent creation data
Figure 10: Mean square error result of intelligent music creation.
10 ComputationalIntelligenceandNeuroscience
[12] Y. Yang, “Piano Online Teaching Based on Neural Network
Technology,” inProceedings of the Artiﬁcial Intelligence and
Advanced Manufacture, pp. 1544–1548, Association for
Computing Machinery, New York, NY, USA, October 2021.
[13] K. Chen, W. Zhang, and S. Dubnov, “M__he Eﬀect of Explicit
Structure Encoding of Deep Neural Networks for Symbolic
Music generation,” inProceedings of the Workshop on Mul-
tilayer Music Representation and Processing (MMRP),
pp. 77–84, IEEE, January 2019.
[14] Y. Kuang, Q. Wu, and Y. Wang, “Simpliﬁed inverse ﬁlter
tracked aﬀective acoustic signals classiﬁcation incorporating
deep convolutional neural networks,”Applied Soft Comput-
ing, vol. 97, Article ID 106775, 2020.
[15] R. Yang, L. Feng, and H. Wang, “Parallel recurrent con-
volutional neural networks-based music genre classiﬁcation
method for mobile devices,”IEEE Access, vol. 8, Article ID
19629, 2020.
[16] N. Shi and Y. Wang, “Symmetry in computer-aided music
compositionsystemwithsocialnetworkanalysisandartiﬁcial
neuralnetworkmethods,”JournalofAmbientIntelligenceand
Humanized Computing, pp. 14–16, 2020.
[17] A. Zgank, “IoT-based bee swarm activity acoustic classiﬁca-
tion using deep neural networks,”Sensors, vol. 21, no. 3,
p. 676, 2021.
[18] N. Anantrasirichai and D. Bull, “Artiﬁcial intelligence in the
creative industries: a review,”Artiﬁcial Intelligence Review,
vol. 55, pp. 65–68, 2021.
[19] A. Solanki and S. Pandey, “Music instrument recognition
using deep convolutional neural networks,”International
Journal of Information Technology, pp. 7–10, 2019.
[20] M.J.Buehler,“Liquiﬁedproteinvibrations,classiﬁcationand
cross-paradigm de novo image generation using deep neural
networks,”Nano Futures, vol. 4, no. 3, Article ID 035004,
2020.
[21] R.RajanandA.A.Raju,“DeepNeuralNetworkBasedPoetic
Meter Classiﬁcation Using Musical Texture Feature fusion,”
inProceedingsoftheSignalProcessingConference(EUSIPCO),
pp. 3–5, IEEE, Coruna, Spain, September 2019.
[22] K.K.LellaandA.Pja,“Automaticdiseasediagnosisusing1D
convolutionalneuralnetworkandaugmentationwithhuman
respiratory sound based on parameters: cough, breath, and
voice,”AIMS Public Health, vol. 8, no. 2, p. 240, 2021.
[23] Z. Yu, X. Xu, and X. Chen, “Learning a Representation for
Cover Song Identiﬁcation Using Convolutional Neural net-
work,” inProceedings of the Acoustics, Speech and Signal
Processing (ICASSP), pp. 541–554, IEEE, Barcelona, Spain,
May 2020.
[24] J.Bobadilla,F.Ortega,andA.Guti´errez,“Classiﬁcation-based
deep neural network architecture for collaborative ﬁltering
recommender systems,”International Journal of Interactive
Multimedia & Artiﬁcial Intelligence, vol. 6, no. 1, 2020.
[25] N. N. J. Siphocly, E. S. M. El-Horbaty, and A. B. M. Salem,
“Top 10 artiﬁcial intelligence algorithms in computer music
composition,”InternationalJournalofComputingandDigital
Systems, vol. 10, no. 01, pp. 373–394, 2021.
[26] A. Alariﬁ and A. Alwadain, “Killer heuristic optimized
convolution neural network-based fall detection with wear-
able IoT sensor devices,”Measurement, vol. 167, Article ID
108258, 2021.
[27] N. Davis and K. Suresh, “Environmental sound classiﬁcation
using deep convolutional neural networks and data aug-
mentation,” inProceedings of the Advances in Intelligent
Computational Systems (RAICS), pp. 41–45, IEEE, M__hir-
uvananthapuram, India, December 2018.
ComputationalIntelligenceandNeuroscience 11
