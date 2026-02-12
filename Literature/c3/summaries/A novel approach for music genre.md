# A novel approach for music genre

**Year:** D:20

---

A novel approach for music genre
identification using ZFNet, ELM,
and modified electric eel foraging
optimizer
Shuang Zhang1, Zhiyong Sun2 & Hasan Jafari3,4
Music genre categorization has been considered to be an essential task within the context of music
data recovery. Genres serve as categories or labels that enable the classification of music based on
shared attributes, including musical style, instrumentation, cultural origins, historical context, and
other distinctive elements. The purpose of classifying music genres is to automatically assign music
pieces to one or more predefined genres. The present research suggests a new method for music genre
identification via integrating deep learning models with a metaheuristic algorithm. The proposed
model uses a pre-trained Zeiler and Fergus Network (ZFNet) to extract high-level features from audio
signals, while an Extreme Learning Machines (ELM) is utilized for efficient classification. Furthermore,
the model incorporates a newly developed metaheuristic algorithm called the Modified Electric Eel
Foraging Optimization (MEEFO) algorithm to optimize the ELM parameters and enhance overall
performance. To evaluate the effectiveness of the model, it has been tested on two widely recognized
benchmark datasets, namely GTZAN and Ballroom, and the results are contrasted with some advanced
models, comprising MusicRecNet, Parallel Recurrent Convolutional Neural Network (PRCNN), RNN-
LSTM, ResNet-50, VGG-16, Deep Neural Network (DNN). The outcomes demonstrated that the
suggested system surpassed several existing methods regarding precision, recall, and accuracy. Keywords  Music genre identification, ZFNet, Extreme learning machine, Modified electric eel foraging
optimization, Deep learning, Metaheuristic
Music is an ever-evolving social phenomenon that has undergone significant transformations throughout
history. Each genre of music serves as a means of expressing the social identity of a particular segment of society,
manifested through the arrangement of musical notes1. Consequently, the vast array of music genres poses a
challenge when attempting to discern the specific style of a musical composition. Nevertheless, there exist certain
distinguishing characteristics within the primary genres of music that aid in identifying their respective styles. However, it requires extensive experience and a continuous engagement with music to accurately recognize and
interpret these musical elements. The concept of music genre is intricate, and its recognition is contingent upon various factors and
circumstances2. Consequently, identifying the genre of a musical piece can be a complex task. This complexity
is further compounded by the emergence of numerous sub-genres and sub-sub-genres that have branched out
from well-established and widely recognized genres. Music can be classified into various genres based on different factors, including melody, harmony,
instrumentation, rhythm, culture, and mood. The identification of music genres involves automatically assigning
a label to a piece of music that represents its genre, such as rock, jazz, or classical. This task has numerous
practical functions, such as suggestion of music, music analysis, retrieval of music, and music education3. On the
other hand, the identification of genres of music is a complex undertaking because of the subjective and intricate
attributes of music, which can vary across time, space, and individual listeners. Furthermore, the absence of a
clear and consistent definition of music genres adds to the challenge, as different sources may employ different
taxonomies and labels for the same type of music.
1School of Music and Dance, Zunyi Normal University, Zunyi, Guizhou 563000, China. 2Music Academy, Baicheng Normal University, Baicheng, Jilin 137000, China. 3Sharif University of Technology, Tehran, Iran.
4College of Technical Engineering, The Islamic University, Najaf, Iraq. email: bcszy230907@163.com;
jafarihasan@gmail.com
OPEN
Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports

Various methods have been proposed in the literature to tackle the challenge of music genre identification. These methods range from conventional machine learning approaches to deep learning methods. Conventional
machine learning approaches typically rely on hand-crafted features, such as temporal, cepstral, and spectral
features4. These attributes have been elicited from the signals of audio and inputted into a classifier, such as
k-nearest neighbors5, SVM6, stacked auto-encoders7, or MLP and Random Forest8. On the other hand, the
current approaches possess specific constraints. For instance, it might be difficult to choose the optimal features,
the feature space can have a high dimensionality, and the methods can be sensitive to noise and variations in the
audio signals. On the other hand, deep learning approaches can learn attributes from the raw audio signals in an automated
way9. This is achieved through multiple layers of nonlinear transformations, like CNNs (Convolutional Neural
Networks) and RNNs (Recurrent Neural Networks)10, and Cross-Modal Neural Model Reprogramming11. These methods have shown promising results in music genre identification because they can capture high-level
and abstract features that are relevant to the music genres. However, deep learning approaches also have their
drawbacks. They require large amounts of labeled data for training, have a high computational cost, and there is
a risk of overfitting the model to the training data. In this context, several studies exist. For example, Elbir et al.12 utilized a Deep Neural Network (DNN) for
the extraction of illustrative features for the music proposal engine and classification system of music genres. Acoustic elements were extracted using networks. These features were used for categorizing genres of music
and suggesting music following a dataset. It is noteworthy that MusicRecNet, a type of CNN, was utilized in
the present study. The achieved accuracy of this specific model was 97.6%, surpassing the accuracy of all other
models. Real-time music genre classification is described in13using deep learning approaches, which is a related
domain to this paper. In14, music genre classification is implemented using CNN which is a different approach. Another work provided a survey of music genre classification, including GTZAN dataset, one of the benchmark
datasets that was explored in our work15. In16covers deep learning based techniques for music genre classification
(in-principal a subject that includes our proposed method, while17 does not directly discuss classifying music
genres, it describes how deep learning can be used for predicting the genre of an audio track, a related task. In a similar vein, Foleis et al.18 commenced research to evaluate any potential effect of texture choice on
automated categorization of genres of music. A new method for identifying unique textures of sound in every
track was introduced by the implementation of a texture selector, according to K-Means. It was discovered that
each track was essential to enhance the efficacy of categorization. Moreover, when the texts are utilized, there is
an opportunity that leads to the enhancement of classification efficiency. It was revealed that the model could
outperform other models. Yang et al.19 offered a hybrid method that was called PRCNN (Parallel Recurrent Convolutional Neural
Network). The aim of the Bi-RNN blocks and Parallel Recurrent CNN is to extract both temporal orders and
spatial attributes of the frame. Next, vectors of syncretic were inserted and applied to the function of Softmax for
the classification of the data. In terms of the GTZAN dataset, the efficacy of the PRCNN, ResNet-18, AlexNet,
and VGG-11 was, in turn, 92.0%, 87.6%, 88.8%, and 88.7%. In terms of the Extended Ballroom dataset, the
efficiency of the PRCNN, VGG-11, ResNet-18, and AlexNet were, in turn, 92.5%, 93.4%, 93.38, and 92.0%. The
suggested model, ResNet-18, could perform better than all of them. Sharma et al.20 suggested a model in which two various approaches were utilized to conduct the model of
classification. MFCC (Mel Frequency Cepstral Coefficient) was utilized as attributes; in addition, numerous
techniques were carried out, such as CNN (1, 2, and 3 Layers), SVM (Gaussian Kernel, Polynomial, and Sigmoid),
and RNN-LSTM, and DNN (1, 2, and 3 Layers). A channel that had three inputs was created by integrating some
features, including Spectrogram, MFCCs, and Scalogram. Furthermore, some systems were implemented, such
as CNN (1, 2, and 3 Layers), ResNet-50, and VGG-16. It was revealed by the study that RNN-LSTM and three-
layered CNN could perform superior to other techniques. In the end, the accuracy value of MFCC was 96.08. Additionally, the loss of validation of 1-layer CNN and RNN-LSTM were, in turn, 0.1111 and 0.1356. Li et al.21 employed several advanced models of DNN (Deep Neural Network) for classifying the genres
of music and assessing the models’ efficacy by the use of spectrograms. In the beginning, the audio files of
music were converted into spectrograms by transformation of modal, and the pieces of music were classified by
deep learning. A balanced trusted function of loss was suggested for mitigating the overfitting issue within the
procedure of training. Eventually, the efficacy of the distinct models of DNN was compared in terms of classifying
genres of music. Additionally, an analysis of music sentiments was added based on a recently developed dataset
of music emotions. The experimental results illustrated the suggested Resnet50-trust could perform superior to
other models. The values the present model obtained on FMA, GTZAN-4, and EMA were, in turn, 80.14, 81.09,
and 77.03. Moreover, the accuracy of the suggested model was 71.56%, which was far better than other ones. The reliability of the traditional approaches is severely limited by several substantial issues. Using hand-
crafted features like temporal, cepstral, and spectral features is a major concern since they are sensitive to
changes in the audio signals and need a lot of domain knowledge. Metaheuristic algorithms provide important
effects on these elements. This means that they may not fully capture the intricacies and subtleties of the music
resulting in less than ideal performance. In addition, overfitting is more likely to occur if the feature space is
high-dimensional, which makes it harder to choose the most important characteristics. Another obstacle is the complexity of fluctuations handling in audio signals and background noise. The
retrieved features and classification accuracy may be affected by background noise, changes in recording
quality, and different musical instruments or arrangements. These factors might undermine the effectiveness
of traditional approaches. To make matters more complicated, there isn’t a universally accepted definition of
musical genres used in any of the available datasets or sources. Generalizing the models to other datasets and
Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

practical options is also challenging which is because of the differences in categories and labels employed by
different datasets. However, deep learning techniques are more successful at collecting high-level and abstract information, but
they have also several downsides. They need a huge quantity of labeled data for training, which may be costly and
time-consuming to get. Furthermore, deep learning models may be computationally costly and run the danger
of overfitting if not adequately regularized. The deep learning techniques typically lack interpretability making it
complicated to grasp the model’s decision-making process. Instead, the proposed model overcomes these problems through a combination of deep learning methods
and metaheuristic algorithms. The pre-trained ZFNet successfully pulls high-level features from raw audio
data, whilst the ELM performs quick and efficient classification. The MEEFO algorithm optimizes the ELM
parameters that improve performance. Mel-spectrograms with optimum window and frame widths enable a
balanced time-frequency representation with 128 Mel bins that establish a compromise between detail and
processing efficiency. The MEEFO improvement to the Electric Eel Foraging Optimizer is stronger in classification Application,
and it creates the model of optimizing Electric Eel foraging behavior in a Framework able to maximize both
exploration and exploit detection of buried objects. In contrast to other metaheuristic optimizers, MEEFO
contains explicit mechanisms of interaction, resting, hunting, and migration phases, to reproduce the competitive
and cooperative behaviors of electric eels in nature. They allow the solutions to interact together and share information which aids in global exploration of the
solution space to avoid solution early convergence. The resting phase refines local search around promising
regions of the search space identified by the interaction phase, and the hunting phase intensifies exploitation in
the regions of the search space that reflect the best solutions found so far. Also, the migration phase allows agents to move between exploration and exploitation and ensures diversity
in the solution space so it helps avoid local optima. Additionally, MEEFO incorporates chaotic maps and an
elimination phase to improve its robustness and adaptability to complex optimization landscapes. Together, these features allow an efficient search of the parameter space of ELM for improved generalization
as well as substantial improvements in music genre classification compared with traditional optimizers that may
have difficulties balancing exploration and exploitation or encounter parameter sensitivity. Therefore, MEEFO’s
bio-inspired architecture offers unique features and is well-suited for hyperparameter tuning to enhance the
ability of the model to classify. Research data
This research used two datasets, Ballroom and GTZAN, to assess our proposed method for music genre detection. Ballroom
The Ballroom dataset is a widely utilized dataset for identifying music genres that are introduced by Gouyon et
al.22. It was specifically created for the Tempo Induction Contest seized throughout the ISMIR 2004 Conference,
which was organized via the Music Technology Group at Universitat Pompeu Fabra. This dataset comprises
698 audio tracks, each with a duration of approximately 20 s. These tracks are evenly distributed across eight
genres, such as jive, cha-cha-cha, rumba, quickstep, tango, samba, waltz, and Viennese waltz. All the tracks are
in the format of 44,100 Hz Stereo 16-bit files of audio in the format of.wav. While the dataset encompasses a
diverse range of musical styles and artists, it does have certain limitations, including low quality, noise, and genre
ambiguity. The dataset is publicly accessible through the MTG website, where tempo annotations and extracted
features of the audio tracks are also provided. Researchers can utilize this dataset for various tasks, such as music
genre classification, music tempo estimation, music feature extraction, and music similarity analysis. The dataset
is accessible from the following link:
​h​t​t​p​s​:​/​/​m​t​g​.​u​p​f​.​e​d​u​/​i​s​m​i​r​2​0​0​4​/​c​o​n​t​e​s​t​/​t​e​m​p​o​C​o​n​t​e​s​t​/​d​a​t​a​1​.​t​a​r​.​g​z. GTZAN
The GTZAN is a standard dataset proposed by Tzanetakis and Cook for the music genre classification23. It serves
as a benchmark for their automatic musical genre classification method using audio signals. By considering 1000
audio tracks, each lasting 30 s, the dataset offers an equal distribution across 10 genres including blues, hip-hop,
country, classical, metal, jazz, reggae, pop, rock, and disco. Each track is presented in 22,050 Hz Mono 16-bit files
of audio in “.wav” format. While the dataset includes a range of musical artists and styles, it does possess certain
limitations such as its relatively small size, low quality, presence of mislabeling, noise, and genre ambiguity. The
data is available on the Kaggle website, which also provides “Mel” spectrograms and extracted features of the
audio tracks:
​h​t​t​p​s​:​/​/​w​w​w​.​k​a​g​g​l​e​.​c​o​m​/​a​n​d​r​a​d​a​o​l​t​e​a​n​u​/​g​t​z​a​n​-​d​a​t​a​s​e​t​-​m​u​s​i​c​-​g​e​n​r​e​-​c​l​a​s​s​i​f​i​c​a​t​i​o​n (accessed on 4 January
2024). Researchers can utilize this dataset for various purposes including music genre classification, music feature
extraction, music similarity analysis, and music visualization. The limitations of both datasets are acknowledged that may hinder generalizability and introduce potential
bias on the outcomes. The employed datasets are small with 1,000 tracks for GTZAN and 698 tracks for Ballroom,
resulting in overfitting and poor performance on larger or more diverse datasets. Moreover, the low audio quality
for the sample (22050 Hz for GTZAN and Ballroom 44100 HZ) used may affect the extraction of the feature and
also there exists a wide range of mislabeling and ambiguity within the genre that can affect the production of the
accuracy of the classification results. Moreover, these datasets are heavily biased towards Western music genres
and cultures, further enforcing a bias that constrictions the usage of the model on non-Western or niche genres
Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

of music. These limitations imply that, although the proposed model performs well on GTZAN and Ballroom, its
efficiency in broader and more mixed datasets or real-world situations with more recent music styles may suffer. Feature extraction
This research utilizes the techniques of Mel-spectrogram and MFCC (Mel-Frequency Cepstral Coefficients) for
extracting attributes. These methods have been extensively utilized within the audio and speech processing field
to gain essential data from audio signals. By incorporating both the Mel-spectrogram and MFCCs as features,
this study aims to enhance audio analysis tasks by using their complementary information. These features have
proven to be effective in distinct functions, like identification of speech, music genre categorization, and incident
of sound diagnosis. The Mel-spectrogram
A mel-spectrogram is a graphical illustration of an audio signal that records data for both time and frequency on
the mel-scale. The mel-scale has been considered to be a perceptual pitch scale, which is based on the auditory
system of humans. Its sensitivity to lower frequencies is far greater than its sensitivity to higher ones, much like
how people hear. The following equation may be used to approximate the Mel scale.
mel (f) = 2595 · Log10
(
1 +
f

)

(1)
where, f and mel (f) represent the hertz frequency, and mels frequency, respectively. First, we apply an STFT (Short-Time Fourier Transform) to the audio input for generating the mel
spectrogram. For this modification, 512 samples are used for the window size and 256 samples for the hope size. The signal has been translated through the domain of time to the domain of frequency using the STFT,
making the amplitude of each frequency component over time visible in the resultant spectrum. We use a set
of all-frequency triangle filters to convert the spectrum to mel scale. It should be mentioned that the number of
filters might vary; nevertheless, 128 filters were used for this specific investigation. For efficient feature extraction in this study, the window size of 512 samples selection in the Mel spectrogram
and 256 samples frame size is determined by providing a balance between time and frequency resolution. While a
frame size of 256 samples guarantees high temporal resolution and enables the model to capture dynamic changes
over time, a window size of 512 samples offers sufficient data points to capture the spectrum features of the audio
input. A smoother audio stream representation is guaranteed by this half overlap that reduces information loss
between successive frames. Employing 128 Mel bins strikes a compromise between computational complexity
and frequency representation detail. More Mel bins would result in a more detailed frequency resolution, but
they would also make the feature space more dimensional, which might cause overfitting and raise computing
expenses. Also, fewer Mel bins would result in less detail and perhaps the loss of significant spectral information. The total efficiency of the music genre identification system is improved by the selection of 128 Mel bins that
confirm a rich representation of the spectrum information of the audio input while preserving computing
efficiency.
where, x represents the input audio signal, fs describes its sampling rate, nfft specifies the number of
samples used for each FFT computation, hoplength represents the number of samples to hop between adjacent
STFT frames, and nmels Illustrates the number of bands of Mel to be utilized. The stft () function is responsible for calculating the STFT of the signal of input, resulting in a spectrogram. To define the Mel filterbank to be applied to the spectrogram, the librosa.filters.mel () function is employed. The np.dot () function is then utilized to apply the filterbank to the spectrogram, resulting in the Mel-
spectrogram. Finally, the librosa.power_to_db () function applies a logarithmic compression to the Mel-
spectrogram. The total amplitudes of all spectra falling inside a given filter’s frequency range constitute its output. Finally,
the filterbank’s output is converted to decibels by calculating the logarithm of the power. With dimensions of
(filter count) x (time frame count), the mel spectrogram is the final matrix that is produced. The mel spectrogram
is scaled and normalized to 256 × 256 pixels to get it ready to be fed into the deep network. Figure (1) shows a
mel spectrogram for a disco music clip as a demonstration. As can be observed, Fig. (1-A) indicates the original signal of the music illustrating the raw audio waveform
that changes over time. This provides a direct view of the amplitude fluctuations and the audio signal structure. Figure (1-B) shows the mel-spectrogram of the original signal. The mel-spectrogram is a time-frequency
representation that maps the audio signal and provides the intensity of different frequency components. This
transformation into the mel scale has been aligned with human auditory perception attempting for a more
intuitive understanding of the frequency content and dynamics of the music clip. These presentations offer
a comprehensive insight into both the temporal and spectral characteristics of the disco music sample that
facilitates a deeper analysis of its characteristics. The mel-frequency cepstral coefficient
The use of MFCCs (Mel-Frequency Cepstral Coefficient) is another noteworthy aspect of this work. Derivation of
MFCCs involves frame-by-frame signal division, window function implementation, discrete Fourier transform
calculation, magnitude spectrum application of a mel filter bank, dynamic range compression, discrete cosine
transforms on the log filter bank outputs, and final feature selection using a subset of the cepstral coefficients24. Figure (2) shows a sample illustration of the MFCC feature for a disco music clip. As can be observed, Fig. (2) provides a clear and detailed illustration of the mel-frequency cepstral coefficients
that effectively support the discussion of the results and their implications. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

Normalization of minimum and maximum
Normalization of Minimum and Maximum is a method used to scale features, which involves transforming the
values of a feature to a range spanning from 0 to 1. This is achieved by detracting the lowest value of the feature
from each value and subsequently dividing by the attribute’s range. The key benefit of Min-Max Normalization lies in its ability to maintain the original distribution of a feature
without altering its shape. However, it is important to note that this method is sensitive to outliers, which can
impact the range of the feature and result in more compressed data. To illustrate, if a feature consists of 99 values
ranging from 0 to 40, and one outlier value is 100, the 99 values will be normalized between 0 and 0.4, while the
outlier will be normalized to 1. Min-max normalization can be advantageous in music genre classification, as it
ensures that features are scaled uniformly and contribute equally to distance calculations. Fig. 1. A sample disco music clip: (A) original signal, (B) mel-spectrogram of (A). Algorithm 1: Pseudo-code of the Mel-spectrogram
Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

The proposed ZFNet/Extreme learning machine
After performing data preprocessing and acquiring spectrograms, the data is then subjected to the ZFNet/
Extreme Learning Machine (ELM) approach for the goal of data modification, extraction of features, and
recognition. To extract the features of the music genre, a novel method is investigated in this study. The trained neural
network ZFNet was first modified by music genre datasets. Since then, the residual layers adapted to ZFNet via
Fig. 2. A sample illustration of the Mel-Frequency Cepstral Coefficients. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

replacing an Extreme Learning Machine were regulated. Lastly, the ELM’s extension abilities were enhanced via
the MEEFO. Zfnet
In 2013, ZFNet became the winner of the ILSVRC race, where investigators developed a method to imagine
the taken-out properties in every single convolutional neural network layer. Then, they take advantage of it to
represent the properties gained from employing AlexNet. Two issues are detected within AlexNet’s construction,
and to resolve those issues, fluctuations are created in the design25,26. The first issue states that properties taken
out via AlexNet in the second and first layers frequently contain high and low-frequency alters; moreover, there
exist fewer mid-frequency properties within the layers. In order to resolve the present issue, the 1 st layer is
altered from 11 × 11 to 7 × 7. The second issue has been connected to interfering with the taken-out properties
within the 2nd layer that happened because of the convolution’s massive stage size; accordingly, the stage size was
altered from 4 to 2. According to these variations, more various and distinguishing properties are gained using
the ZFNet architecture, and network behavior is enhanced in comparison with AlexNet. Consequently, in the
current study, a CNN using the ZFNet structure has been utilized. Extreme learning machine
Functions, that utilize machine learning, frequently make wide utilization of one-hidden-layer NNs, for example, ELM. Initially, the input layer’s biases and weights are shaped at stochastic, and then, 2nd, the output layer’s
weights and biases are calculated based on the stochastic amounts that were produced. Classical NN learning
tactics possess a lesser ratio of activity and a sluggish learning pace. It has been supposed the neurons’ number
within the layer of input has been signified via the n, and the amounts of o and h are, in turn, the neurons’
amounts within the layer of output and the hidden. The cost value has been computed via the next formula: Yj =
∑
m
i=1Qif(wi.bi.zi)

(2)
where, wi determined for the input connection’s weight, bi illustrates the ith concealed neuron’s biases, zj
illustrates the output connection’s weight, and Yj for the ELM’s last output. The matrix form of Eq. (2) defines
with Eq. (3).

## Y T = HQ

(3)
here, Y T refers to the alteration of the matrix Y; moreover, H and Q are illustrated subsequently:

## H =



f (w1.b1.z1)
f (w2.b2.z1)...
f (wh.bh.z1).........
f (w1.b1.zγ )
f (w2.b2.zγ )...
f (wh.bh.zγ )


γ × h

(4)
Q = [Q1. Q2. · · ·. Ql]T 
(5)
The foremost aim of ELM training is to reduce the errors’ number during the training process. To appropriately
instrument a traditional ELM, weights, and biases of the input must be selected stochastically, and the function
of activation needs to have the capability to be substantially distinguished27. The ELM’s training within the
current technique manages within the weight of output ( Q) being attained via making most of the function of
least squares in Eq. (6), and the result might be defined with Eq. (7).
min Q ∥HQ −Y T ∥
(6)

## Q = H+ZT

(7)
here, H+ Illustrates the general Moore-Penrose reverse of the H matrix. Modified electric eel foraging optimization (MEEFO)
This part defines the motivation and main opinion, the mathematical model, the process, and the complications
of EEFO. Inspiration
Electrical eels have been known as the extraordinary hunters among all animals. Electric eels belong to the
family Gymnotidae which is in South America and are famous due to their outstanding skill of discharge among
river individuals. Mature individuals could produce a voltage between 300 and 800 for shock victims to consume
it. Consequently, electrical individuals have been identified as “high voltage cables” within marine. For producing electricity, individuals own 3 sets of electric organs comprising 1000 electrical-producing cells
named electrolytes. The current electrolytes within the body act like mini batteries that stock power. Eels frequently produce about 10 volts to direct and detect prey because of their limited ability to see. Eels
take advantage of the reaction of these electrical signs to effectively pursue and exactly detect speeding victims. Furthermore, to protect in contrast to an opponent as an armament, the raised electrical charge is utilized and
low electrical discharge is utilized aimed at interaction among individuals. Likewise, Eels could perceive and
understand discharge data from additional eels. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

Eels utilize electric charge as an extremely cutting-edge technique of interaction and protection. Whenever
eels discover a target, the individuals release more considerable electrical charge quickly and shock the quarry. The present capability is a significantly efficacious food-seeking approach in the realm of biology. Novel research
suggests that electric eels have a swarm-based behavior. eels similar to mammals, apply communal predation as
the hunting technique. This is because sets of eels could organize activities, counting interacting, resting, migrating, and hunting, to
pursue victim and comportment communal predation. Whenever leading set hunting, eels have a tendency to
gather, swim in loops, and corralling the school of fish into a “prey ball” before equally beginning a destructive
high-voltage assault on the ball of the quarry. This set hunting manner upsurges the chance to attain a greater
number of prey, particularly whenever there is plenty of fish. EEFO is considered based on the optimized
behaviors. Mathematical model and algorithm
The EEFO model includes the exploitation and exploration stages, which result from the social predation actions
of electric eels, namely interaction, rest, migration, and hunting. The subsequent sections are the mathematical
models for hunting behaviors. Interacting
Once eels meet a school of fish, they interact with each other by swimming and roiling. Subsequently, the
candidates commence swimming in a huge electrical ring to trick several minor individuals in the middle of
the circle. Within EEFO, each electrical individual is a contender solution; additionally, the finest contender
solutions gained up to now within the stages are regarded as the proposed quarry. The interaction designates
every individual accommodatingly cooperates with other members with the data of the individuals’ situations. The present manner could be observed as the exploration stage. Exactly, an electrical individual could interrelate
with all individuals stochastically selected from the individuals via utilizing the situation data of total members
within the population. Renewing an individual’s situation contains contrasting the distinction between a
stochastically designated individual and the individuals center. Furthermore, an electrical individual could cooperate with several stochastically designated candidates in the
population via employing the local data within the solution space. The candidate’s situation has been renewed via
defining the alteration among a stochastically designated individual from the population as well as a candidate
produced stochastically in the solution space. The communication among candidates is noticeable through a
churn that signifies a stochastic motion within numerous orientates. The subsequent model signifies this churn. A = n1 × C
(8)
n1 ∼N (0,1)
(9)
c1, c2,..., ck,..., cd
(10)
c (k) =
{ 1 if
k == g{l

else

(11)
g = randperm (d)
(12)
l = 1,..., ⌈T −t
T
× r1 × (d −2) + 2⌉
(13)
Here the amount of the maximum iterations is defined by T. The interacting behavior is determined as:



{ vi (t + 1) = zj (t) + A × (−z (t) −zi (t)) p1 > 0.5
vi (t + 1) = zj (t) + A × (zr (t) −zi (t)) p1 ≤0.5
fit (zj (t)) < fit (zi (t))
{ vi (t + 1) = zj (t) + A × (−z (t) −zi (t)) p2 > 0.5
vi (t + 1) = zj (t) + A × (zr (t) −zi (t)) p2 ≤0.5
fit (zj (t)) ≥fit (zi (t))

(14)
−z (t) = (1/n)
∑
n
i=1 (t)
(15)
zr = L + r × (U −L)
(16)
In which, p1and p2 are stochastic amounts that are in the interval (0, 1), fit (z( i )) illustrates the objective
of the individual’s location of the ith electrical candidate, zj has been found to be the situation of a candidate
selected stochastically from the present population and j = i, the population’s size is defined by n, r1 is a
stochastic amount in (0,1), r is the stochastic vector in (0,1), and, L and U are, in turn, defined as the lower
and upper restrictions. Based on Eq. (29), the ability of electric eels to communicate permits them to navigate to
several situations within the search space. This interaction plays a major role in exploring the full search space
of EEFO. Resting
The resting parts need to be recognized before electric eels accomplish resting behavior in EEFO. For enhancing
the search productivity, resting parts are recognized in the area place any 1 dimension of the location vector
of a candidate has been expected in the foremost diagonal within the solution space. For recognizing a resting
part of a candidate, the location and solution space of the candidate have been regularized to a span of 0–1. A
Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

stochastically selected location’s dimension of the candidate is expected the foremost diagonal of the regularized
solution space. The expected location has been regarded as the resting region’s center of the eel. The resting
region could be calculated by the next formula:
{Z |Z −X (t)| ≤a0 × |X −zprey (t)|}
(17)
a0 = 2.(e −e(t/T ))
(18)
X (t) = L + x (t) × (U −L)
(19)
x {t =
zrand{d
rand{n
{
t −Lrand{d
U rand{d −Lrand{d

(20)
where, zprey is the location vector of the finest solution gained to date, a0 has been found to be the primary
scale of the region of resting, a0 × |X −zprey (t)| designates the span of the resting region, zrand(d)
rand(n) is the
stochastic location dimension of a stochastically selected member of the existing population, and the regularized
amount has been illustrated by z. Consequently, the resting situation of a candidate has been gained in its resting
region before accomplishment of resting manner: Ri(t + 1) = X (t) + α × |X (t) −zprey (t)|
(21)
α = a0 × sin (2π r2)
(22)
where, α illustrates the resting region’s scale, and r2 illustrates a stochastic amount in (0,1). The scale α
makes the resting region’s range be able to reduce as the iterations progress. It would improve local search. Once
the resting region has been established, candidates would transfer it to the present phase. Namely, a candidate
renews its location to the resting region using its resting location within its resting region. The manner of resting
is determined subsequently:.
vi(t + 1) = Ri(t + 1) + n2 × (Ri (t + 1) −round(rand) × zi(t ))
(23)
n2 ∼N (0,1)
(24)
Hunting
Once eels discover prey, they do not merely make a group to hunt. Alternately, they have a tendency to
accommodatingly swim within the creation of a big circle and enclose the quarry. In the meantime, the individuals
continually interconnect and collaborate with their colleagues throughout emission of organ discharges with
low electricity. As the individuals’ communication strengthens, the size of the electrical circle declines. Lastly,
individuals move the school of fish from the low part to the upper part, in the place where they are easy to hunt. On the basis of the present manner, the electrical circle is defined as the space of hunting, at the present point,
the quarry commences moving everywhere in the region of hunting; consequently, the quarry would rapidly go
from the present location to several locations in the area of hunting because of being scared. The hunting space
could be definite as follows: Z |Z −zprey (t)| ≤β 0 ×
−z (t) −zprey (t)

(25)
β 0 = 2 × (e −e(t/T ))
(26)
here, β 0 defines the primary size of the space of hunting. Based on Eq. (25), a candidate focuses on the quarry
zprey (t) by establishing a hunting range given by the term β 0 multiplied by the total value of the distinction
between the positions
−z (t) and zprey (t). Consequently, a novel location of the grey regarding its former
location in the hunting space could be produced as: Hprey (t + 1) = zprey (t) + β ×
−z (t) −zprey (t)

(27)
β = β 0 × sin (2π r3)
(28)
here, β defines the size of the hunting space and r3 is a stochastic amount in interval (0,1). The scale β causes
the series of the space of hunting to reduce with the passage of time. Exploitation is advantageous. Having
determined hunting space, a candidate commences to catch quarry within the space of hunting. Once hunting,
the individual rapidly detects prey and coils’ the novel location to surround the prey among its head and tail;
additionally, this will emit a current that is high-voltage round the prey. The hunting performance experiment
in EEFO contains a coiling motion, in which an eel’s location is renewed to the novel prey’s location. The coiling
performance displayed by eels throughout hunting could be designated as:
vi(t + 1) = Hprey(t + 1) + η × (Hprey (t + 1) −round(rand) × zi(t ))
(29)
where, η designates the coiling factor, defined as follows: Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

η = e(r4(1−t)/T ) × cos (2π r4)
(30)
where, r4 defines a stochastic amount in interval (0,1). Once the prey is encircled by eels, some locations are
produced because the quarry accomplishes a dive that is swan. Then, a candidate surprises the quarry via coiling
performance, and a location is utilized for renewing the novel location of the candidate within the subsequent
iteration. Migrating
Once candidates discover quarry, the candidates have a tendency to travel from the space of resting to the space
of hunting. The mathematical model of the eels’ migration performance is determined by the next formula:
vi (t + 1) = −r5 × Ri(t + 1) + r6 × (Hr (t + 1) −Lf × (Hr (t + 1) −zi (t))
(31)
Hr (t + 1) = zprey (t) + β ×
−z (t) −zprey (t)

(32)
Lf = 0.01 ×
u.δ
|v|(1/b)

(33)
u, v ∼N (0,1)
(34)
δ =
(
Γ (1 + b) × sin ( π b

)
Γ ( 1+b

)
× b × 2(b−1/2)
)(1/b)

(35)
here, Hr is regarded as any location in the hunting space, r5 and r6 are stochastic amounts in interval (0,1). The term (Hr (t + 1) −zi (t)) designates that individuals transfer to the space of hunting. The function of
Levy flight has been defined by Lf and has been presented to the global search stage of EEFO for evading from
tricking into local optimum. Lf is calculated as follows:
here, Γ demonstrates the standard Gamma function; in addition, b equals 1.5. An eel could observe the prey’s
location by low discharge of electricity; therefore, it could alter its location at any time. In the foraging procedure,
if the eel feels that prey is close, it transfers to the candidate location; otherwise, the eels remain at the present
location. The eels’ locations are renewed as follows:
zi (t + 1) =
{ zi (t)
fit (zi (t)) ≤fit (vi (t + 1))
vi (t + 1)
fit (zi (t)) > fit (vi (t + 1))

(36)
The transition from exploration to exploitation
EEFO utilizes an energy factor to determine search behaviors, which could efficiently manage the shift from
exploration to exploitation for enhancing the algorithm’s optimization action. The amount of an energy factor of
a candidate has been utilized for being selected from exploitation and exploration. The factor of energy has been
calculated by the next formula: Es (t) = 4 × sin
(
1 −t
T
)
× ln 1
r7 
(37)
Here r7 is a stochastic amount in interval (0,1). Based on Eq. (45), Es (t) diminishes when the iterations
upsurge; furthermore, the factor of energy Es (t) demonstrates a lessening change by fluctuation throughout
the iterations. Whenever the factor of energy Es (t) >1, individuals accomplish exploration within the total
parameter region in a cooperating manner, consequential within global search. Whenever the factor of energy
Es (t) ≤1, eels have a tendency to accomplish exploration in a hopeful sub-region through resting, migrating,
or manners of hunting, leading to global search. Within the 1 st half of the iterations, the global search happens
using an upper possibility, whilst within the 2nd half of the iterations, the global search happens using a higher
possibility. For investing the search manner of EEFO, the possibility of Es that is more than 1 is assessed
through the optimization procedure. Let
θ = 1 −t

## T 

(38)
Then
Es (t) = sin (θ ) ln 1
r7 
(39)
The possibility of Es > 0 is gained by: P {Es (t) > 1} =
∫1

∫e

4sin

drdθ

= −
∫

4· sin(1)
−∝
ezdz
z
√
16z2 −1
≈0.5035
(40)
Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

Based on the consequence of Eq. (48), there is a possibility of about 50% to accomplish between exploration
or exploitation throughout the optimization procedure. It donates significantly to make a balance between
exploration and exploitation. Modified EEFO
The efficacy of the EEFO algorithm within complicated optimality issues with limited parameters is being
enhanced by making modifications to address its susceptibility to parameter settings and lack of search agent
variety. Chaotic maps, which are utilized in metaheuristic optimization, provide advantages such as randomness,
statistical characteristics, and nonlinearity. These benefits enable deeper exploration and yield improved solutions. Consequently, chaotic maps have become increasingly popular in the field of computer engineering, particularly
for generating random numbers and substituting pseudo-random numbers with Gaussian distributions. The EEFO algorithm, susceptible to parameter settings and lack of search agent variety, is being modified
to improve its performance in complex optimization problems with limited parameters. Chaotic maps, used
in metaheuristic optimization, offer benefits such as randomness, statistical characteristics, and nonlinearity,
allowing for deeper exploration and better answers. They have gained popularity in computer engineering for
generating random numbers and replacing pseudo-random numbers with Gaussian distributions. The chaotic enhanced optimization technique marked the beginning of a lengthy line of advancements
in optimization approaches. In the domain (0, 1), the Liebovitch map stood out due to the existence of two
separators, which may be mathematically described as follows:
θ i (t) =



σ × θ i (t),
0 < θ i (t) ≤P1
P −θ i
P2−P1, P1 ≤θ i (t) < P2
1 −γ × (1 −θ i (t), P2 ≤θ i (t) < 1

(41)
Here, all random values, including r1, r2,..., r6, i.e.,
θ i
j = rj|j=1,2,...,6
(42)
To improve the metaheuristic algorithm’s efficiency and convergence to the best solution, the “elimination phase”
is an important step. As part of this procedure, we rank all of the possible solutions so that the algorithm may be
zero in the most promising areas of the solution space. By removing the subpar results, the algorithm becomes
more efficient and gets closer to the best solution. During the elimination step, we rank all of the solutions by
objective function value, and then choose the ones with the lowest scores. Validation of the algorithm
Objective validation of the proposed updated EEFO algorithm was necessary to demonstrate its reliability. Initially, this approach was used to resolve 23 long-standing, conventional benchmark functions. LFD (Lévy
Flight Distribution)28, PRO (Poor and Rich Optimization)29, WSO (War Strategy Optimization)30, EO
(Equilibrium Optimizer)31, and Runge kutta optimizer (RUN)32 were five more advanced algorithms that were
compared to EEFO’s findings. Table 1 tabulates a comparison of the competing algorithms’ parameter values. It summarizes a comparison of parameter values for a few optimization techniques of common interest: Lévy Flight Distribution (LFD), Poor and Rich Optimization (PRO), War Strategy Optimization (WSO) and
Equilibrium Optimizer (EO), and Runge Kutta Optimizer (RUN). These parameters are used as benchmark for
performance with MEEFO algorithm. Each algorithm has its very own collection of parameters, which need to
be judiciously set to get the best possible results, as the next comparison shows. Using multimodal functions from F8–F13, unimodal functions from F1–F7, and fixed-dimensional
functions from F14–F23, the study was conducted33. Every function had a dimension of thirty. The primary goal
of the research was to find the lowest possible value for all twenty-three of the aforementioned functions. If an
algorithm could minimize its output value, it would be the most efficient. Analyzing the optimization solutions of the algorithms in the solution using the mean value and standard
deviation (StD) led to a reliable analysis. To provide a strong and fair comparison, all algorithms were tested
under identical conditions, including a fixed population size and an upper limit on the number of iterations. There can be no more than 200 iterations and 60 nodes in this example’s population. By doing this procedure 30
times, we could guarantee more accurate and trustworthy results34. The IMSR algorithm’s performance relative
to other approaches is seen in Table 2. Algorithm
Parameter/value
Lévy flight distribution (LFD)28
Threshold = 2; β = 1.5; CSV = 0.5; α 1 = 10; α 2 = 5e −5;
α 3 = 5e −3; ∂1 = 0.8; ∂2 = 0.2
Poor and Rich Optimization (PRO)29
N = 1; P = 0.8; r = 0.2; b = 0.3; c = 0.7; m = 1e −2
War Strategy Optimization (WSO)30
w = 0.3; a = 0.5; d = 0.5; 0.2
Equilibrium Optimizer (EO)31
V = 1; a1 = 2; a2 = 1; GP = 0.5
Runge kutta optimizer (RUN)32
a = 50; b = 10
Table 1. Comparison of the competing algorithms’ parameter values. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

In order to examine the outcomes, we computed the standard deviation (StD) and average of the optimization
solutions offered via each method. The results of the study and comparison could be relied upon because of this. By examining the average values, one can see that the suggested EEFO algorithm outperforms the majority of
the benchmark functions. It finds highly optimal solutions for these functions because it constantly gets extremely low mean values. When we compare EEFO to other algorithms, we find that it usually does better than or at least as well as more
sophisticated algorithms. A few examples of functions where EEFO outperforms competing techniques are F1, F4, F8, F12, F15, and F16. Function
Mean/StD
LFD
PRO
WSO
EO
RUN
EEFO
F1
Mean
2.15E-59
3.08E-08
2.10E-17
2.32E-59
4.27E-07
2.10E-59
StD
5.54E-30
3.15E-04
1.82E-09
6.06E-30
5.06E-04
5.22E-30
F2
Mean
5.74E-35
3.33E-04
1.90E-08
6.39E-35

## 3.26E + 01

5.46E-35
StD
6.97E-18
3.48E-02
4.96E-05
6.66E-18

## 5.13E + 00

6.27E-18
F3
Mean
1.26E-14

## 1.40E + 01

## 1.94E + 02

1.23E-14

## 2.46E + 02

1.19E-14
StD
2.47E-07

## 2.12E + 00

## 7.21E + 00

2.65E-07

## 1.11E + 01

2.45E-07
F4
Mean
1.52E-14
5.49E-01
9.20E-04
1.75E-14

## 7.19E + 00

1.43E-14
StD
1.31E-07
3.17E-01
8.56E-02
1.65E-07

## 1.33E + 00

1.25E-07
F5
Mean

## 8.94E + 00

## 5.62E + 01

## 2.32E + 01

## 2.05E + 01

## 1.17E + 02

## 8.75E + 00

StD
7.30E-01

## 4.99E + 00

## 3.51E + 00

7.89E-01

## 1.25E + 01

6.83E-01
F6
Mean
5.94E-11
2.75E-08
6.66E-11
4.85E-01
4.31E-07
5.38E-11
StD
5.09E-10
3.44E-04
2.15E-09
4.81E-01
5.55E-04
4.71E-10
F7
Mean
5.54E-04
5.61E-02
1.49E-02
6.39E-04
4.11E-02
5.28E-04
StD
2.43E-03
1.22E-01
6.39E-02
1.97E-02
1.24E-01
2.27E-03
F8
Mean

## −5.80E + 03

## −5.29E + 03

## −2.09E + 03

## −4.69E + 03

## −4.87E + 03

## −5.76E + 03

StD

## 1.51E + 00

## 3.30E + 01

## 1.61E + 01

## 2.54E + 01

## 2.38E + 01

## 1.43E + 00

F9
Mean
5.11E-01

## 4.48E + 01

## 1.20E + 01

6.15E-01

## 5.67E + 01

5.06E-01
StD
6.47E-01

## 2.92E + 00

## 1.62E + 00

## 1.19E + 00

## 3.87E + 00

5.85E-01
F10
Mean
1.31E-05
6.04E-02
3.19E-04

## 2.29E + 00

## 1.43E + 00

1.24E-05
StD
6.36E-07
4.86E-01
1.94E-05
7.84E-01
7.12E-01
6.27E-07
F11
Mean
1.00E-03
7.26E-03

## 3.10E + 00

1.76E-03
1.86E-01
9.39E-04
StD
2.32E-03
7.90E-02

## 1.08E + 00

6.49E-02
2.87E-01
2.21E-03
F12
Mean
1.22E-11
5.86E-03
1.92E-02
3.53E-02
4.19E-01
1.13E-11
StD
1.36E-12
1.30E-01
2.00E-01
1.17E-01
9.07E-01
1.30E-12
F13
Mean
1.68E-10
1.98E-03
1.09E-03
4.24E-01
1.32E-03
1.66E-10
StD
2.74E-11
4.94E-02
4.94E-02
3.21E-01
5.97E-02
2.45E-11
F14
Mean
8.10E-01

## 3.11E + 00

## 4.26E + 00

## 3.61E + 00

## 1.35E + 00

7.78E-01
StD
3.20E-01

## 1.36E + 00

## 1.22E + 00

## 1.70E + 00

9.59E-01
3.04E-01
F15
Mean
8.82E-05
7.13E-04
3.40E-03
2.91E-03
2.04E-03
8.25E-05
StD
2.75E-03
1.19E-02
3.55E-02
7.53E-02
5.47E-02
2.55E-03
F16
Mean
−7.45E-01
−7.59E-01
−7.83E-01
−7.14E-01
−7.32E-01
−7.64E-01
StD
5.52E-05
2.68E-04
2.54E-04
1.47E-04
2.30E-04
5.33E-05
F17
Mean
2.46E-01
3.24E-01
3.23E-01
2.95E-01
3.31E-01
2.39E-01
StD
2.51E-08
2.75E-08
2.29E-08
9.44E-03
2.37E-07
2.20E-08
F18
Mean

## 1.81E + 00

## 2.66E + 00

## 2.61E + 00

## 2.56E + 00

## 1.96E + 00

## 1.70E + 00

StD
6.42E-14
2.96E-08
4.25E-08

## 2.25E + 00

5.41E-07
6.38E-14
F19
Mean

## −3.04E + 00

## −2.77E + 00

## −2.89E + 00

## −3.10E + 00

## −2.88E + 00

## −3.25E + 00

StD
2.18E-15
7.46E-08
7.76E-08
3.70E-02
1.55E-07
2.07E-15
F20
Mean

## −2.62E + 00

## −2.41E + 00

## −2.83E + 00

## −2.57E + 00

## −2.24E + 00

## −2.81E + 00

StD
2.97E-08
1.86E-01
3.57E-08
2.64E-01
1.80E-01
2.86E-08
F21
Mean

## −7.53E + 00

## −4.96E + 00

## −4.86E + 00

## −7.97E + 00

## −4.46E + 00

## −7.58E + 00

StD
5.39E-01

## 1.56E + 00

## 1.49E + 00

## 1.17E + 00

## 1.44E + 00

5.07E-01
F22
Mean

## −7.90E + 00

## −7.14E + 00

## −7.73E + 00

## −8.16E + 00

## −5.84E + 00

## −7.83E + 00

StD
3.38E-01

## 1.12E + 00

5.82E-01
5.38E-01

## 1.44E + 00

3.32E-01
F23
Mean

## −7.54E + 00

## −6.95E + 00

## −7.66E + 00

## −8.74E + 00

## −6.03E + 00

## −8.28E + 00

StD
6.17E-01

## 1.27E + 00

9.28E-01
6.64E-01

## 1.58E + 00

5.82E-01
Table 2. Assessment of other algorithms in comparison to EEFO. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

While EEFO generally outperforms competing algorithms, there are a few benchmark functions where it falls
short. For example, other methods such as LFD, WSO, and EO provide lower average values in functions F2, F3, F6, F7, and F13. When looking at the standard deviation numbers, it’s clear that EEFO’s optimization solutions
are usually quite consistent. This means the method is reliable and seldom gives wildly different outcomes when
solving problems. Evolved ZFNet
A method to recognize the music genre, named ZFNet/ELM/MEEFO is provided is in the study. This technique
is, in turn, resultant of the ZFNet, ELM, and MEEFO processes. Applying a ZFNet that is trained provides an
opportunity for extracting properties of imaging from music genre audio signals. This part would evaluate the appropriateness of the searching agents produced by MEEFO with the
performance index identified as MSE (Mean Square Error) for arrangement aims. The useful fitness function
could be defined by the next equation:
fitnessfunction = (0.5)
T
i=0(g −g)2/T
0.5

(43)
Here g and g, in turn, signify the assessed and real outputs, and T is defined as the entire number of samples
that are utilized for training. Simulation results
The present research employed a Hybrid ZFNet/Extreme Learning Machine (ELM) for feature extraction and
identification of sound spectrums. The proposed model was optimized by a modified electric eel foraging
optimizer. The Hybrid ZFNet/ELM extracted cepstral characteristics, including the Mel-spectrograms and
MFCCs based on ZFNet. Then, these features were identified based on the ELM as a classifier to determine
the possibility of all genres. The model was evaluated by applying it to two widely used datasets, Ballroom and
GTZAN, and provided a comparative analysis with advanced techniques. By adjusting the hyperparameter in the proposed model, the number of hidden neurons (H) was set to 70%
of the training data size to provide the highest accuracy with a proper balance between model complexity and
generalization. The number of folds (K) in K-fold cross-validation was chosen to be 5 with the highest accuracy
(98.20%) and effectively balanced bias and variance that ensure reliable model evaluation. The learning rate (η)
was set to 0.01 to provide the trade-off between computational efficiency and model performance. The number
of iterations was set to 500 to provide the proper trade-off between solution space exploration and avoiding
overfitting or excessive computational time. Contrastive exam of H variables utilizing the ZFNet/ELM/MEEFO
A method for authentication between the test and training data has been found to be K-fold cross-validation. It
is employed to make predictions with a model and assess its accuracy in practical applications. By dividing the
data into K equal-sized subsets, each subset gets the chance to serve as both training and test data. This approach
effectively mitigates bias within the data, as the testing and training processes are repeated K times. Considering the present stage, the test outcomes of the suggested ZFNet/ELM/MEEFO have been analyzed
to assess the impact of various H values on accuracy. Our objective is to identify the optimal H value that ensures
the validity of the ZFNet/ELM/MEEFO method, as depicted in Table 3. The K value has a significant influence on the optimal value of H, resulting in varying levels of accuracy, as
shown in the table. From the table, several observations can be made. Firstly, increasing the K value generally
improves accuracy, except for the last two rows where a significant drop is observed. This suggests that a higher
number of folds in cross-validation enhances model performance, but too many folds can lead to overfitting or
instability. Secondly, setting H to 50% or 70% of the training data size results in higher accuracy compared to 10% or
K. This indicates that the ELM classifier benefits from a greater number of hidden neurons, but an excessive
amount may cause redundancy or complexity. The highest accuracy of 98.20% is achieved when K equals 5 and
K value
H = 10% from train data
H = 50% from train data
H = 70% from train data

## H = K

89.81%
89.81%
89.82%
89.81%

92.97%
92.85%
88.97%
93.96%

96.91%
91.79%
89.99%
93.76%

94.90%
96.81%
95.96%
93.82%

97.60%
98.11%
98.20%
97.14%

96.54%
97.46%
96.82%
95.18%

96.84%
97.97%
95.92%
96.87%

96.99%
97.75%
95.95%
95.78%

94.91%
95.79%
94.89%
92.97%

94.90%
95.76%
93.85%
90.75%
Table 3. Comparative test results to define the best H value for the proposed ZFNet/ELM/MEEFO. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

H equals 70%, while the lowest accuracy of 90.75% is obtained when K equals 10 and H equals K. This significant
difference of 7.45% highlights the sensitivity of the proposed ZFNet/ELM/MEEFO method to the choice of H
and K parameters. The optimal values may vary depending on the specific data and problem at hand. To enhance
the method, one possible approach is to utilize a dynamic or adaptive H value that adjusts following the features
of the data and the performance of the model. Model investigation
To determine the capability of the proposed hybrid model, its ability based on a simple ZFNet feature extractor
plus a softmax (ZFNet), and the hybrid model of ZFNet with ELM without MEEFO algorithm were authenticated
based on both single Mel-Spectrogram and single MFCC. Figure (3) shows the comparison analysis of different
structures based on a 10-fold analysis. The results indicate that MFCC achieves higher accuracy than Mel-Spectrogram, regardless of the framework
used. This suggests that MFCC is a more effective feature for distinguishing between sound genres in this
classification task. Additionally, as the model structure becomes more intricate, progressing from ZFNet to
ZFNet/ELM to ZFNet/ELM/MEEFO, the accuracy improves. This implies that incorporating ELM and MEEFO enhances the performance of the ZFNet feature extractor
by enhancing classification and optimization capabilities. Among the tested frameworks, the proposed ZFNet/
ELM/MEEFO with MFCC achieves the highest accuracy of 95.76%, while the simple ZFNet with Mel-
Spectrogram achieves the lowest accuracy at 85.45%. The notable difference of 10.31% between these extremes highlights the significant impact of feature and
structure choices on sound genre classification. Based on these observations, it might be deduced that the
suggested ZFNet/ELM/MEEFO approach surpasses the other frameworks in terms of accuracy. Comparison analysis
To provide a more clarified authentication of the proposed ZFNet/ELM/MEEFO, it has been compared with
some other edging literature. The methods include MusicRecNet12, Parallel Recurrent Convolutional Neural
Network (PRCNN)19, RNN-LSTM20, ResNet-5020, VGG-1620, Deep Neural Network (DNN)21. Table 4 tabulates
the comparison analysis between the proposed ZFNet/ELM/MEEFO and the different named techniques
considering accuracy, precision, and recall. The ZFNet/ELM/MEEFO model demonstrates the highest recall rate among all other models, achieving an
impressive 99.50%. This indicates that the model effectively captures nearly all sound genres accurately, resulting
in a very low false negative rate. In terms of accuracy and precision, the ZFNet/ELM/MEEFO model ranks second
with values of 98.20% and 98.22% respectively. This suggests that the model correctly classifies a significant
majority of sound genres, maintaining a very low false positive rate. On the other hand, the ResNet-50 model
exhibits the highest accuracy and precision, reaching 100.52% and 102.40% respectively. However, these values
Fig. 3. Accuracy comparison analysis for different structures for (A) Mel-Spectrogram and (B) MFCC. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

may be unrealistic and could potentially indicate overfitting or errors in calculation or reporting. In contrast,
the CNN model showcases the lowest accuracy, precision, and recall among all models, measuring at 79.73%,
64.22%, and 55.23% respectively. These results highlight poor performance in sound genre classification, with
high rates of false positives and false negatives. Based on the information provided in the table, it can be concluded that the suggested ZFNet/ELM/MEEFO
model surpasses most advanced approaches regarding accuracy, recall, and precision. The approach proves to be
robust and reliable for sound genre classification. To further enhance the model, a potential approach involves
contrasting it with other advanced approaches that utilize different features or architectures. Additionally, fine-
tuning the model parameters using the MEEFO algorithm could also lead to improvements. Table 4 compares the proposed model to existing models and highlights its benefits while also acknowledging
its possible drawbacks. While the ZFNet/ELM/MEEFO model has good accuracy, precision, and recall, it
may not beat more advanced deep learning models such as ResNet-50 and VGG-16 in all areas. For example, ResNet-50 and VGG-16, with their deep architectures, may extract more detailed and hierarchical features from
data, which may be useful for specific difficult genres or datasets. While the ZFNet/ELM/MEEFO model is
efficient and tuned, it may lack the depth and capacity required to learn such complicated patterns. In addition
to the excellence of MEEFO in optimizing ELM parameters, it may be computationally costly for especially big
datasets that impact total training time. In addition, although the model’s dependence on the Mel-spectrogram
and MFCC features is strong, it may not catch all of the subtleties found in raw audio data, which more advanced
models like ResNet-50 and VGG-16 can manage by deeper convolutional layers. Despite these limitations, the
proposed model provides a balanced method by combining efficient feature extraction and optimization, making
it an excellent choice for music genre classification tasks, particularly when computing resources are restricted. The suggested model provides multiple important components to enhance its performance. ZFNet is used
for feature extraction by efficiently reflecting high-level spectral and temporal features from the audio signals. ELM is used for efficient classification due to its fast learning speed and good generalization features. MEEFO
optimizes the ELM parameters to ensure providing optimal performance by fine-tuning the hyperparameters
and preventing overfitting. A Mel-spectrogram with a window size of 512 samples and a frame size of 256 samples
balances time-frequency resolution concerning 128 Mel bins that guarantees a detailed yet computationally
efficient representation. Statistical significance
In order to evaluate how statistically significant the performance enhancement obtained by the proposed ZFNet/
ELM/MEEFO model over other state-of-the-art models is, a Wilcoxon signed-rank test was performed. This is
a non-parametric test that is used for paired data and the distributions do not need to be normal, therefore it
is very much suitable for testing classification metrics (such as accuracy, precision, and recall) produced from
models that were built on the same datasets (GTZAN and Ballroom in this case). We performed hypothesis testing, where the null hypothesis ( H0​) states that there is no significant difference
between the performance of our proposed model and competing models, and the alternative hypothesis ( H1
) states that the performance of our proposed model is statistically superior. The test was conducted with
a  significance level α = 0.05, and the results are shown in Table 5. Particularly, we focused on the analysis of the
differences in classification metrics (accuracy, precision and recall) in both Mel-spectrogram and MFCC based
feature extraction methods. These results showed that the proposed ZFNet/ELM/MEEFO model did statistically better in significantly
improving the predictive performance than the other models. Table 5  indicates that the p value derived from
comparison with most models already in existence was always less than α, allowing the null hypothesis to be
rejected in favour of the alternative hypothesis. Thus, the improvements in accuracy, precision, and recall are
statistically significant with respect to the existing models. For example, compared to CNN, PRCNN, and RNN-
LSTM, the performance of ZFNet/ELM/MEEFO was much higher in almost all metrics, with p-values < 0.001
to 0.003. It is worth noting that the proposed model also performed better than VGG-16 and DNN, however, the
improvement in precision and recall compared to DNN was not statistically significant. The results emphasize
and demonstrate the reliability and efficiency of combining MEEFO with ELM for parameter optimization, thus
improving the classification performance. Method
Accuracy
Precision
Recall
CNN
79.73%
64.22%
55.23%
PRCNN
84.52%
68.45%
70.52%
RNN-LSTM
88.99%
91.75%
92.21%
accuracy
97.52%
97.40%
97.05%
VGG-16
94.93%
94.75%
91.18%
DNN
97.58%
97.35%
98.51%
ZFNet/ELM/MEEFO
98.20%
98.22%
99.50%
Table 4. Contrast between the suggested models and the advanced ones. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

Additionally, results of the ablative study also support these conclusions where the excellent performance is
attributed to each component, ZFNet, ELM, and MEEFO. In brief, the statistical validation is a stepping stone
for the framework to be used concretely in order to music genre classification tasks. Ablation study
An ablation study, which entails methodically removing or replacing each component and assessing the model’s
performance on the Ballroom and GTZAN datasets using accuracy, precision, and recall as performance metrics,
was carried out in order to examine the contribution of each component in the proposed ZFNet/ELM/MEEFO
model [Table 6]. As can be observed from the results, since ZFNet, ELM, and MEEFO operate well together, the baseline
model performs best with 98.20% accuracy, 98.22% precision, and 99.50% recall. Removing MEEFO (Ablation
1) affects performance, notably recall (96.85% accuracy, 96.90% precision, 98.12% recall), demonstrating that
MEEFO optimizes ELM parameters, boosting the model’s music genre classification. Since eliminating ELM and
using a simple classifier with MEEFO and ZFNet (Ablation 2) reduces performance even more (95.76% accuracy,
95.80% precision, 97.20% recall), ELM’s rapid learning and strong generalisation are crucial. After eliminating
ZFNet and using raw features with ELM and MEEFO (Ablation 3), performance reduces dramatically (92.50%
accuracy, 92.60% precision, 93.10% recall), proving ZFNet’s importance in audio data extraction. ZFNet for
feature extraction and a simple classifier (Ablation 4) reduce performance (91.20% accuracy, 91.30% precision,
92.00% recall), showing that ELM and MEEFO are needed for optimal performance. Simply using ELM for classification using raw data and Ablation 5’s basic feature extraction approach
affects performance (88.90% accuracy, 89.00% precision, 89.50% recall), proving the model needs ZFNet and
MEEFO. With a basic feature extraction and classification approach (Ablation 6), utilizing solely MEEFO for
parameter optimisation decreases performance (87.50% accuracy, 87.60% precision, 88.00% recall), indicating
that MEEFO’s function in ELM parameter optimization is vital to model efficacy. In the ablation research, ZFNet
extracts high-level features from audio signals, ELM learns rapidly and generalizes effectively, and MEEFO
optimizes ELM parameters to help the model learn and generalize from training data. Conclusions
Identifying music genres poses a formidable challenge as it necessitates the extraction and analysis of intricate
attributes from signals of audio. The process of categorization of music genres entails the analysis of audio signals
Model Variant
Accuracy (%)
Precision (%)
Recall (%)
Baseline: ZFNet/ELM/MEEFO
98.20
98.22
99.50
Ablation 1: ZFNet/ELM
96.85
96.90
98.12
Ablation 2: ZFNet/MEEFO
95.76
95.80
97.20
Ablation 3: ELM/MEEFO
92.50
92.60
93.10
Ablation 4: ZFNet
91.20
91.30
92.00
Ablation 5: ELM
88.90
89.00
89.50
Ablation 6: MEEFO
87.50
87.60
88.00
Table 6. Ablation analysis. Metric
Model comparison
Mean difference
p-value
Significant? Accuracy
Proposed vs. CNN
18.47%
< 0.001
Yes
Proposed vs. PRCNN
13.68%
< 0.001
Yes
Proposed vs. RNN-LSTM
9.21%
< 0.001
Yes
Proposed vs. VGG-16
3.27%
0.012
Yes
Proposed vs. DNN
0.62%
0.234
No
Precision
Proposed vs. CNN
34.00%
< 0.001
Yes
Proposed vs. PRCNN
29.77%
< 0.001
Yes
Proposed vs. RNN-LSTM
6.47%
0.003
Yes
Proposed vs. VGG-16
3.47%
0.021
Yes
Proposed vs. DNN
0.87%
0.315
No
Recall
Proposed vs. CNN
44.27%
< 0.001
Yes
Proposed vs. PRCNN
28.98%
< 0.001
Yes
Proposed vs. RNN-LSTM
7.29%
0.005
Yes
Proposed vs. VGG-16
8.32%
0.008
Yes
Proposed vs. DNN
0.99%
0.287
No
Table 5. Statistical significance. Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

or other relevant representations of music, wherein meaningful features such as rhythm, melody, harmony, timbre,
and tempo are extracted. These features are then utilized in conjunction with machine learning techniques to train
models capable of accurately predicting the genre of a given music sample. The ultimate aim of categorization
of music genres is effectively categorizing and labelling music pieces into specific genres, leveraging their
characteristic features. The present study introduced a proficient framework for music genre identification that
combines deep learning techniques with a metaheuristic algorithm. The framework encompasses a pre-trained
Zeiler and Fergus Network (ZFNet) as a convolutional neural network renowned for its exceptional performance
in image recognition tasks, and an extreme learning machine (ELM) as a feedforward neural network. The ELM
takes the place of the final layers of the ZFNet and functions as a classifier for the music genres. To optimize
the ELM, a novel algorithm named Modified Electric Eel Foraging Optimizer (MEEFO) has been employed. To
evaluate the proposed framework, it is applied to two widely utilized datasets, namely GTZAN and Ballroom,
and its performance is compared against various existing methods, including MusicRecNet, Parallel Recurrent
Convolutional Neural Network (PRCNN), RNN-LSTM, ResNet-50, VGG-16, Deep Neural Network (DNN). The experimental findings demonstrate that the framework attains superior accuracy, precision, and recall in
music genre identification. Moreover, the model exhibits versatility and can be applied to various applications
that necessitate music genre identification, including music recommendation, music retrieval, music analysis,
and music education. As part of future work, the model will be expanded to accommodate a broader range of
music genres and more intricate audio features. Larger datasets can be considered in the future work to further
enhance the validation and robustness of our system. Additionally, further exploration will be conducted to
investigate additional deep learning and metaheuristic techniques that have the potential to improve the model’s
efficacy. Data availability
The datasets used and/or analyzed during the current study available from the corresponding author on reason­
able request. Received: 14 August 2024; Accepted: 14 April 2025
References

### 1. Brisson, R. Music-genre identification in adolescents: an exploratory study. Poetics 99, 101802 (2023).

### 2. Kuzman, T. & Ljubešić, N. Automatic genre identification: a survey. Lang. Resour. Evaluation, 1–34 (2023).

### 3. Li, Y., Zhang, Z., Ding, H. & Chang, L. Music genre classification based on fusing audio and lyric information. Multimedia Tools

Appl. 82, 20157–20176 (2023).

### 4. Han, M. et al. Timely detection of skin cancer: an AI-based approach on the basis of the integration of echo state network and

adapted seasons optimization algorithm. Biomed. Signal Process. Control. 94, 106324 (2024).

### 5. Wu, M. & Liu, X. in 6th International Conference on Dependable Systems and Their Applications (DSA). 335–340 (IEEE). (2019).

### 6. Rahardwika, D. S. et al. in 2020 International seminar on application for technology of information and communication (iSemantic).

## 7–11 (IEEE).

### 7. Scarpiniti, M., Scardapane, S., Comminiello, D. & Uncini, A. Music genre classification using stacked auto-encoders. Neural

Approaches Dynamics Signal. Exchanges, 11–19 (2020).

### 8. Fan, S. & Fu, M. in IEEE 5th International Conference on Information Systems and Computer Aided Education (ICISCAE). 331–334

## (IEEE). (2022).

### 9. Prabhakar, S. K. & Lee, S. W. Holistic approaches to music genre classification using efficient transfer and deep learning techniques. Expert Syst. Appl. 211, 118636 (2023).

### 10. Ashraf, M. et al. A hybrid CNN and RNN variant model for music classification. Appl. Sci. 13, 1476 (2023).

### 11. Hung, Y. N., Yang, C. H. H., Chen, P. Y. & Lerch, A. in ICASSP 2023–2023 IEEE International Conference on Acoustics, Speech and

Signal Processing (ICASSP). 1–5 (IEEE).

### 12. Elbir, A. & Aydin, N. Music genre classification and music recommendation by using deep learning. Electron. Lett. 56, 627–629

(2020).

### 13. Zhang, R. & Chen, Y. What can multi-factors contribute to Chinese EFL learners’ implicit L2 knowledge? Int. Rev. Appl. Linguist. Lang. Teach. (2024).

### 14. Han, F., Yang, P., Du, H. & Li, X. Y. Accuth $^+ $+: Accelerometer-Based Anti-Spoofing voice authentication on Wrist-Worn

wearables. IEEE Trans. Mob. Comput. 23, 5571–5588 (2023).

### 15. Li, D., Tang, N., Chandler, M. & Nanni, E. An optimal approach for predicting cognitive performance in education based on deep

learning. Comput. Hum. Behav., 108607 (2025).

### 16. Liu, F., Zhao, X., Zhu, Z., Zhai, Z. & Liu, Y. Dual-microphone active noise cancellation paved with doppler assimilation for TADS. Mech. Syst. Signal Process. 184, 109727 (2023).

### 17. Song, W. et al. TalkingStyle: personalized speech-driven 3D facial animation with style preservation. IEEE Trans. Vis. Comput. Graph. (2024).

### 18. Foleis, J. H. & Tavares, T. F. Texture selection for automatic music genre classification. Appl. Soft Comput. 89, 106127 (2020).

### 19. Yang, R., Feng, L., Wang, H., Yao, J. & Luo, S. Parallel recurrent convolutional neural networks-based music genre classification

method for mobile devices. IEEE Access. 8, 19629–19637 (2020).

### 20. Sharma, A. K. et al. Classification of Indian classical music with time-series matching deep learning approach. IEEE Access. 9,

102041–102052 (2021).

### 21. Li, J. et al. An evaluation of deep neural network models for music classification using spectrograms. Multimedia Tools Appl., 1–27

(2022).
22.	 da Silva Muniz, V. H. Oliveira e Souza Filho, J. B. Robust handcrafted features for music genre classification. Neural Comput. Appl.
35, 9335–9348 (2023). de.

### 23. GTZAN. (ed Kaggle). (2020).

### 24. Ayvaz, U. et al. Automatic speaker recognition using Mel-Frequency cepstral coefficients through machine learning. Computers

Mater. Continua 71 (2022).

### 25. Liu, H. & Ghadimi, N. Hybrid convolutional neural network and flexible Dwarf mongoose optimization algorithm for strong

kidney stone diagnosis. Biomed. Signal Process. Control. 91, 106024 (2024).

### 26. Zehao, W. et al. Optimal economic model of a combined renewable energy system utilizing modified. Sustain. Energy Technol. Assess. 74, 104186 (2025). Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/

### 27. Ghiasi, M. et al. Enhancing power grid stability: design and integration of a fast bus tripping system in protection relays. IEEE

Trans. Consum. Electron. (2024).

### 28. Houssein, E. H., Saad, M. R., Hashim, F. A., Shaban, H. & Hassaballah, M. Lévy flight distribution: A new metaheuristic algorithm

for solving engineering optimization problems. Eng. Appl. Artif. Intell. 94, 103731 (2020).

### 29. Moosavi, S. H. S. & Bardsiri, V. K. Poor and rich optimization algorithm: A new human-based and multi populations algorithm. Eng. Appl. Artif. Intell. 86, 165–181 (2019).

### 30. Ayyarao, T. S. et al. War strategy optimization algorithm: a new effective metaheuristic algorithm for global optimization. IEEE

Access. 10, 25073–25105 (2022).

### 31. Faramarzi, A., Heidarinejad, M., Stephens, B. & Mirjalili, S. Equilibrium optimizer: A novel optimization algorithm. Knowl. Based

Syst. 191, 105190 (2020).

### 32. Ahmadianfar, I., Heidari, A. A., Gandomi, A. H., Chu, X. & Chen, H. RUN beyond the metaphor: an efficient optimization

algorithm based on runge Kutta method. Expert Syst. Appl. 181, 115079 (2021).

### 33. Zhang et al. A deep learning outline aimed at prompt skin cancer detection utilizing gated recurrent unit networks and improved

orca predation algorithm. Biomed. Signal Process. Control. 90, 105858 (2024).

### 34. Huang, Q., Ding, H. & Razmjooy, N. Oral cancer detection using convolutional neural network optimized by combined seagull

optimization algorithm. Biomed. Signal Process. Control. 87, 105546 (2024). Author contributions
Shuang Zhang, Zhiyong Sun and Hasan Jafari wrote the main manuscript text and prepared figures. All authors
reviewed the manuscript. Funding
This work was supported by Training Program of Guizhou North Culture Research Center, Zunyi Normal Uni­
versity, Guizhou Province: Guzheng performance involves in the inheritance of North Guizhou tea culture and
art, win-win mode (2019 JDPY004); Natural Sciences Foundation of Heilongjiang Province of China, (LH2020
A002); Heilongjiang Education Science Fifteen planning 2022 key issue: Research and practice on the training
model of “Normal students educational practice ability” in the context of teacher certification (GJB1422335); Harbin University Teacher Education Development Fund(JFXS2021011). Declarations
Competing interests
The authors declare no competing interests. Additional information
Correspondence and requests for materials should be addressed to Z. S. or H. J. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:14249

| https://doi.org/10.1038/s41598-025-98766-7
www.nature.com/scientificreports/
