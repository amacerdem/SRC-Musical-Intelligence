# Music genre classification with

> **Source:** Music genre classification with.pdf  
> **Converted:** 2025-12-17 15:32:28

---

## Page 1

Music genre classification with 
parallel convolutional neural 
networks and capuchin search 
algorithm
Yuxin Zhang1 & Teng Li2
With the primary objective of creating playlists that suggest songs, interest in music genre 
categorization has grown thanks to high-tech multimedia tools. To develop a strong music classifier 
that can quickly classify unlabeled music and enhance consumers’ experiences with media players 
and music files, machine learning and deep learning ideas are required. This study presents a 
unique method that blends convolutional neural network (CNN) models as an ensemble system to 
detect musical genres. The method makes use of discrete wavelet transform (DWT), mel frequency 
cepstral coefficients (MFCC), and short-time fourier transform (STFT) characteristics to provide 
a comprehensive framework for expressing stylistic qualities in music. To do this, each model’s 
hyperparameters are generated using the capuchin search algorithm (CapSA). Preprocessing the 
original signals, feature description utilizing DWT, MFCC, and STFT signal matrices, CNN model 
optimization to extract signal features, and music genre identification based on combined features 
make up the four main components of the technique. By integrating many signal processing 
techniques and CNN models, this study advances the field of music genre classification and provides 
possible insights into the blending of diverse musical components for improved classification 
accuracy. The GTZAN and Extended-Ballroom datasets were the two used in the studies. The 
average classification accuracy of 96.07 and 96.20 for each database, respectively, show how well our 
suggested strategy performs when compared to earlier, comparable methods.
Keywords  Music genre classification, Convolutional neural network, Deep learning, Capuchin search 
algorithm
Music is one of the most popular types of entertainment in the digital era. In order to use music to communicate 
their thoughts and emotions, humans invented rhythm, harmony, and melody1,2. Additionally, music has a 
significant impact on people’s life as it may improve concentration at work and hasten the reduction of stress3. 
Multimedia technologies are evolving rapidly, and as more digital music resources become accessible, people are 
steadily moving their music consumption to online music streaming services. Pattern recognition and machine 
learning technologies are highly helpful in overcoming this difficulty since they can fulfill different sophisticated 
music retrieval needs at a given moment from a big music collection4. Many high adjectives, such artist, genre, 
instrumentation, and mood, may be used to define music. Musical genre is one of the main high-level descriptors 
that best describes the semantic elements of a particular music recording. A professional music collection’s 
database often contains millions of songs, whereas a typical home music collection could only include a few 
thousand tracks. Most of the world’s music databases index information primarily using the artist, title, album, 
and genre of each song5.
Music comes in a wide variety of genres, such as pop, jazz, blues, folk, rock, and so on6–8. “Musical genres are 
descriptive categories used to classify music in record stores, radio stations, and increasingly online.”9. Certain 
elements of the work’s rhythm, instrumentation, and texture may be used to identify a certain genre, even if the 
classification of music into genres is arbitrary and subjective10,11. Additionally, a lot of music-based applications 
and recommendation engines start by asking users to select a certain musical genre12. The user experience of 
listening to music has been enhanced and refined in recent years by the use of machine learning models to detect 
1Conservatory of Music, Jilin University of the Arts, Changchun 130000, Jilin, China. 
2Academy 
of 
Arts, 
Pingdingshan 
Polytenchnic 
College, 
Pingdingshan 
467000, 
Henan, 
China. 
email: 
1807050217@stu.hrbust.edu.cn; 15937539636@163.com
OPEN
Scientific Reports |         (2025) 15:9580 
1
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports

## Page 2

different musical genres13,14. The methods required to prepare data for use in machine learning classifier training 
may be characterized using data science15. During data preparation, unprocessed data is merged and sanitized. 
A subset of artificial intelligence known as “machine learning” uses input data to recognize certain domain 
attributes, which enables it to resolve issues in the training domain. It applies scientific concepts like statistics 
and arithmetic to examine the feature pattern in the given data.
Applying a machine learning model to a music dataset, it may identify several musical features and cluster 
similar pieces together. This enables the user to look for music depending on their tastes that is comparable 
to them. In this way, online music businesses may grow by satisfying their clientele. According to recent 
research, supervised learning techniques are not as effective as machine learning classifiers such as artificial 
neural networks, convolutional neural networks, decision trees, logistic regression, random forests, support 
vector machines, and naïve Bayes in classifying musical genres16. However, since processing costs and model 
training durations rise quickly, calculating machine learning predictions with a large-scale music collection is 
challenging17. Deep learning methods have shown to be quite effective in solving this problem in recent years. 
The achievement of a perfect model is still a long way off, however. Our suggested approach seeks to lessen this 
discrepancy. Three parallel convolutional neural network (CNN) models are used to form an ensemble system 
in this study to categorize different musical genres.
In order to create a general framework for distinguishing artistic elements in music using features like 
discrete wavelet transform (DWT), Mel frequency cepstral coefficients (MFCC), and short-time fourier 
transform (STFT), the hyperparameters for each model are determined using the capuchin search algorithm 
(CapSA). Preprocessing the original signal, getting feature descriptions using DWT, MFCC, and STFT signal 
matrices, improving CNN models and extracting signal features, and classification using combined features are 
the four primary components of the approach. CapSA is used to adjust each CNN model’s hyperparameters in 
order to reduce training mistakes. The last extracted characteristics of these models are the values derived from 
the last completely linked layer. The goal of this suggested approach is to provide a thorough framework for 
characterizing musical style characteristics. The following is a list of contributions made to this work:
•	 A parallel architecture for integrating deep learning models for audio information processing and merging is 
proposed in order to increase the accuracy of the detection model.
•	 CNN models and deep learning are improved to attain optimum performance in music genre categorization 
via the use of optimization methodologies.
Here is the remainder of the paper: Next, we looked at a number of pertinent studies. The third section covered 
the materials and method. The findings are evaluated in the fourth part, and a summary is given in the fifth and 
final section.
Related works
A well-researched and complex subject in music information retrieval is the categorization of musical genres. A 
program that could identify the mood, genre, and context of music from users’ Pérez-Marcos et al. demonstrated 
the first use of Last.fm with Twitter tweets18. It allowed for the dynamic addition of additional modules and the 
construction of a scalable system with dispersed sub-processes when applied to a multi-agent platform. The 
technology was integrated to build a multi-agent platform.
Wassi et al.19 introduced a unique approach to realistic MGC using transmit data from the benchmark 
FM frequency. Using an FPGA-based method, the system first extracts attributes before classifying them into 
categories. The system was developed with efficiency using a system-level model, which cut down on the total 
design time. Scalability and resource management were given substantial weight in the selected methodology.
Li et al.20 provided a balanced, trustworthy loss function for categorizing music using DNN models. They 
evaluated performance using three distinct music datasets, created spectrograms from audio recordings of music, 
and then used deep learning to categorize the music. ResNet50_trust, their suggested model, consistently beat 
other DNN models in testing. The user provided spectrograms to the CNN model. This study has recognized 
the following six musical genres: rap, soundtrack, hardcore, dubstep, electro, and classical. The songs are first 
converted into spectrograms and then split into segments. Every track has a 2.56-second gap in between. There 
are four CNN layers, a fully connected layer, a softmax function, and a song classification model based on 
musical genres21.
Foleiss et al.22 provided the first description of the use of k-means for texture selection. This technique aims 
to detect the sound textures in the recordings. Extracting textures from music is a useful technique to reduce 
the amount of processing that goes into storage. Liu et al. devised a broadcast module structure that consists 
of inception blocks, transition layers, and decision layers in Ref.23. The broadcast module is essential since it 
preserves all extracted characteristics in higher layers, enabling decision layers to make predictions based on 
them. Mobile phones and other devices have been used via this method. Adiyansjah et al.24 created an innovative 
“music recommender system” that provided suggestions by analyzing similarities in audio signal features. 
The researchers calculated similarity distance by extracting features using CRNN to assess feature similarity. 
Furthermore, the suggested similarity model was assessed to confirm its quality and feasibility.
Allamy and Koerich25 introduced a 1D residual convolutional neural network (CNN) architecture for 
classifying musical genres. To enhance precision, the method divided audio waves into overlapping parts. The 
1D CNN model achieved a higher mean accuracy of 80.93% on a 1,000 audio sample public dataset compared 
to previous architectures. Scarpiniti et al.26 use a stacked auto-encoder architecture to address music genre 
categorization. The method is based on 57 characteristics collected from the audio stream.
Melo et al.27 developed the ASVD approach, which utilizes a graph’s topological features generated from 
an audio source to extract rhythmic elements from music signals. The local standard deviation of a music 
Scientific Reports |         (2025) 15:9580 
2
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 3

signal was graphed against a visibility graph to analyze the modularity, density, average degree, and number of 
communities. Supervised Artificial Neural Network (ANN) classification trials employing certain characteristics 
as input achieved equal or better accuracy compared to beat histogram in 70% of musical genre pairings. Nanni 
et al.28 introduced a distinctive method that utilizes visual and auditory data extracted from song audio files to 
automatically classify music genres. Various methods were used to generate the visual elements that depicted an 
audio file as a picture. Each section of the divided images has a set of local texture descriptors that are retrieved. 
SVMs were combined to get a final decision. Finally, many characteristics connected to hearing are evaluated. 
Research indicates that the combination of many texture components results in outstanding performance.
Jaishankar et al.29 created a method in the field of Music Information Retrieval (MIR) to classify music genres 
by analyzing audio data from popular online repositories including GTZAN, ISMIR 2004, and the Latin Music 
Dataset. The researchers used African Buffalo Optimization (ABO) to choose variables that represent differences 
across musical genres. Various classifiers such as back propagation neural networks (BPNN), support vector 
machines (SVM), Naïve Bayes, decision trees, and kNN were used to classify audio using selected characteristics. 
The ABO-based feature selection strategy achieved an average accuracy of 82%.
Prabhakar et al.30 constructed five strategies for music genre categorization and evaluated them on three 
datasets. The deep learning BAG model demonstrated higher classification accuracy, achieving 93.51% for the 
GTZAN dataset and 92.49% for the ISMIR 2004 dataset. The GMM-HMM with SDA model achieved an accuracy 
of 92.2% when tested on the MagnaTagATune dataset. Future research will focus on enhancing classification 
accuracy by creating new architectures, such as hybrid deep learning methods, and enhancing transfer learning 
and deep learning models.
Cheng and Kuo31 proposed a new technique for categorizing musical genres using the YOLOv4 neural 
network architecture and the visual Mel spectrum. The approach attained a mean Average Precision (mAP) of 
99.26% across ten trials, with an average of 97.93%. This novel strategy focuses successfully on certain musical 
genres.
Li32 presents a new method for music genre classification using two standalone CNN models for MFCC 
and STFT feature sets. The hyperparameters of each CNN are tuned by the Black Hole Optimization (BHO) 
algorithm. The main strength is that this method allows for the hyperparameters tuning in order to achieve 
maximum performance. But one can argue about the problem of higher computational cost when training two 
different CNNs and fine-tuning their hyperparameters. In this context, Ahmed et al.33 analyze the classification 
results of the different machine learning models of CNN, FNN, SVM, kNN, and LSTM for music genre 
classification using the GTZAN dataset. Their work shows that, based on the spectrogram, the modified CNN 
model outperforms other models in identifying intricate patterns. One strength of this study is the ability to 
compare multiple deep learning architectures for music genre classification. However, one of the weaknesses is 
that the work is largely restricted to the GTZAN dataset only.
In the study by Wijaya et al.34, the authors develop a music genre classification approach based on BiLSTM 
with MFCC features. The study uses the GTZAN and ISMIR2004 datasets, although the latter has been 
preprocessed to have a similar duration with GTZAN dataset. BiLSTM is favorable for extracting temporal 
relation between each corresponding point of the audio signal and is essential for the music genre classification. 
Nevertheless, one possible limitation is that the computational cost may be higher than for other less complex 
models such as CNN. Chen et al.35 propose a new framework CNN-TE that is based on CNN and Transformer 
to classify music genres. This approach leverages the strengths of both architectures: CNN for local details and 
Transformer for the global context. The proposed CNN-TE model outperforms other CNN architectures on the 
GTZAN and FMA datasets while having fewer parameters and less inference time. One major strength of this 
hybrid approach is that it is time efficient and has great accuracy in capturing local and global features of the 
audio signal.
Methodology
Data
Two datasets were used in the analysis: GTZAN36 and Extended-Ballroom37. The GTZAN database is one of 
the first and most often used datasets for this issue. The database contains one thousand audio files, each with a 
duration of thirty seconds and a frequency of 21.5 kHz. Ten musical genres are allocated to the files: pop, reggae, 
rock, hiphop, jazz, blues, country, and disco. Each genre of music in this collection has 100 samples in each 
class. The Ballroom dataset was altered and enhanced to become the Extended-Ballroom database. There are a 
total of 4180 audio tracks, each lasting 30 s. The audio files are categorized into 13 unique groups: chacha(455), 
jive(350), quickstep(497), rumba(470), samba(468), tango(464), Viennese waltz(252), waltz(529), foxtrot(507), 
pasodoble(53), salsa(47), slow waltz(65), and wcswing(23). The GTZAN and Extended-Ballroom datasets 
include samples saved as .wav files, each dataset is used separately in the study.
Proposed model
Three CNN models, known as parallel CNN ensembles, are used in this work to classify music genres. CapSA 
is used to determine the hyperparameters of each model. This approach combines DWT, MFCC, and STFT 
elements to provide a detailed pattern for expressing musical artistic attributes. The proposed technique consists 
of four essential phases:
	1.	 Converting incoming signals into a standardized format is referred to as signal preprocessing. This proce­
dure involves standardizing and transforming the frequency of the signal.
	2.	 Features extracted from signal matrices by the Discrete Wavelet Transform (DWT), Mel-frequency Cepstral 
Coefficients (MFCC), and Short-Time Fourier Transform (STFT): This stage consists of obtaining the feature 
matrices for Discrete Wavelet Transform (DWT), Mel-Frequency Cepstral Coefficients (MFCC), and Short-
Scientific Reports |         (2025) 15:9580 
3
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 4

Time Fourier Transform (STFT) from the preprocessed signal. A CNN model processes inputs from each 
matrix individually. The final extracted features are generated using the data acquired from the last complete­
ly linked layer of these models.
	3.	 Before extracting the ultimate features, the hyperparameters of each CNN model are fine-tuned using CapSA 
to enhance the CNN models. The pooling function type and convolution filter size are selected for each CNN 
model to minimize training error.
	4.	 The collective attributes of the CNN models are used as the foundation for categorization. A SoftMax-based 
classifier is used to categorize music genres.
Figure 1 displays the architecture of the proposed technique, with more computational details provided in the 
following sections. Our parallel architecture contains three independent CNN networks that extract features 
from DWT, MFCC, and STFT signal representations. The parallel method brings more benefits than traditional 
serial processing systems. We split signal processing tasks into separate domains to let each technique work 
best at its specialty. DWT is best at detecting sharp events and high frequencies but MFCC shows strength in 
capturing audio signal spectral patterns. The CNN architecture lets us split feature processing across different 
domains so the model can collect a wider range of features than a single model. Parallel processing improves 
system efficiency by letting multiple cores or GPUs handle feature extraction and processing tasks at the same 
time. All CNN features are merged into a single input that helps the final classification layer learn more effectively.
Preprocessing
Preprocessing the incoming information is the first stage in classifying music genres. This stage seeks to mitigate 
the negative effects of certain circumstances unique to each sample that might hinder categorization. Among 
these criteria are the temporal and spectral characteristics of the samples. When the frequency of an audio 
broadcast is altered, the individual samples become less discernible. A signal with a higher frequency generates a 
greater number of samples within a certain time frame. As this attribute is unrelated to musical genres, all input 
signals’ frequencies are first standardized to a constant value, such as Fs, before preprocessing. Subsequently, 
signals having many channels are transformed into single-channel signals. Each signal may be represented as a 
vector. After preprocessing, all signals are transformed into vectors with a mean of zero and a variance of one38.
	
−
S= s −µ s
σ s

(1)
s and 
−
S represent the input and output of the signal normalization step, with µs denoting the mean of the signal 
sequence values. Finally, σ s is the standard deviation of s.
Fig. 1.  Block diagram of the proposed method.
 
Scientific Reports |         (2025) 15:9580 
4
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 5

Feature description
The characteristics of the processed signal are separated in the second phase of the proposed method. Three 
methods used for obtaining the characteristics are Short-Time Fourier Transform (STFT), Mel-Frequency 
Cepstral Coefficients (MFCC), and Discrete Wavelet Transform (DWT). Each approach utilizes a matrix to 
depict the characteristics of the input signal. Music genres are classified using individual matrices.
Feature description based on DWT  The Discrete Wavelet Transform (DWT) is a technique that utilizes fre­
quency to transform information into a set of wavelet functions. The process involves splitting the original signal 
into a low-frequency segment and a high-frequency component. Each of these sections is repeatedly divided into 
two smaller portions until they reach a sufficient size. An audio stream may be transformed into a matrix format 
by using Discrete Wavelet Transform (DWT). Each wavelet coefficient is arranged as a column in a matrix in this 
approach. The matrix has the same number of columns as the wavelet coefficients. Applying the Discrete Wavelet 
Transform (DWT) to convert an audio signal into a matrix form involves the following procedures:
	(a)	 Converting audio signal to digital signal: To depict the audio signal in a matrix format, it has to be trans­
formed into a digital signal. The audio stream is sampled for this purpose. Sampling the audio stream re­
quires measuring the signal at precise intervals. An adequate sample frequency is necessary to maintain all 
the information included in the audio stream. The sampling frequency in this experiment is set at twice the 
highest frequency of the audio source.
	(b)	 After converting the audio signal to digital form, it is then processed into wavelet coefficients. The preferred 
approach for computing wavelet coefficients involves using the Haar wavelet function. The wavelet function 
is multiplied by the digital signal to get the wavelet coefficients. The product is transformed into an expo­
nential series. The series depicts exponential factors using wavelet coefficients.
	(c)	 Organizing the wavelet coefficients in a matrix: After calculating them, the wavelet coefficients may be 
positioned as columns in a matrix. The matrix has the same number of columns as the wavelet coefficients.
A PCNN component uses the matrices produced by running the steps on each audio stream as inputs.
Feature description based on MFCC  The MFCC approach is a typical technique used for extracting audio 
information. This approach offers benefits such as improved clarity and effective feature summary by simulating 
the operations of the human auditory system. The MFCC methodology is now part of the recommended method 
as a signal description tool due to its benefits. The procedure of getting the MFCC matrix from an audio stream 
involves the following stages:
	(a)	 Pre-emphasis filter: At this point, the signal’s frequency responsiveness is enhanced by using a pre-boost 
filter. This guarantees a more effective upkeep of the acoustic characteristics at lower frequencies.
	(b)	 At this stage, the signal is divided into small frames using framing, windowing, and overlapping techniques. 
A window is used to blur the borders of frames to reduce the impact of the frame edges. The frames overlap, 
allowing for the consideration of data from adjacent frames.
	(c)	 Determining the Mel-Scale and Spectrum Calculating the spectrum of each frame in the Filter Bank is 
essential. Subsequently, the Mel scale is used to transform the spectrum into a filter bank. The Mel scale’s 
filter bank is crafted to accurately mimic the frequency response of the human auditory system.
	(d)	 The Logarithm and Discrete Cosine Transform are used to get the logarithm of the spectrum in the Mel 
scale. The feature summarizing procedure utilizes the discrete cosine transform (DCT). The features are 
condensed into a low-dimensional space by the use of Discrete Cosine Transform (DCT).
	(e)	 Cepstral derivatives Coefficients are established at this step. Derivatives may enhance the accuracy of clas­
sification.
The technical details of how the signal’s characteristics are explained using MFCC were previously covered in39 
and will not be repeated in this section.
Feature description based on STFT  The Short-Time Fourier Transform (STFT) is a kind of feature used for 
analyzing input signals. The input signal is denoted by N consecutive frames labeled as f(m, n), where m rep­
resents the frame identifier and n represents the sample identification inside the current frame. Each frame 
undergoes an STFT transformation to create a vector of dimension D. This transformation for every frame f in 
the signal can be formulated as follows40:
	
F (m, k) =
∑
nf (m, n) e−j2π nk
N

(2)
In the above relation, we have:
	
f (m, n) = f (n) ω (n −mS)
(3)
The function ω(n) is applied to N samples located at point mS. S represents the increment value used in the 
samples. N represents the distinct frequencies identified by the fast Fourier transform (FFT) while using a power 
of 2. In this configuration, the overlap rate between two consecutive frames is N−S
N . Having F (m, k) based on 
Eq. (2), the power spectral density (PSD) can be calculated as follows40:
Scientific Reports |         (2025) 15:9580 
5
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 6

Pf (m, k) = 1
N |F (m, k)|2
(4)
Regarding a constant frequency FS, each frame is explained in the form of N points that cover the frequency 
range [
−F S
2 , F S
2
)
. Since the spectral power is symmetric, N/2 discrete frequencies suffice for its description.
Optimization of CNN models and feature extraction of the signal
Three distinct Convolutional Neural Network (CNN) models are used to evaluate the extracted music signal 
characteristics from Discrete Wavelet Transform (DWT), Mel-frequency Cepstral Coefficients (MFCC), and 
Short-Time Fourier Transform (STFT) matrices. While the general framework of these models for handling each 
component is same, the hyperparameter settings vary across them. Hyperparameters are crucial characteristics 
of a machine learning model that greatly influence its performance. Configuring a CNN model is a complex and 
detailed task. The proposed method uses CapSA to find the best values for the hyperparameters of each CNN 
model. Figure 2 illustrates the basic architecture of the CNN models designed to analyze DWT, MFCC, and 
STFT matrices.
The suggested method entails using CNN models with an input layer, a fully connected layer, and 4 
convolutional blocks. The convolution block begins with a two-dimensional convolution layer, followed by ReLU 
and Pooling layers. Each CNN model’s input layer gets the MFCC, STFT, or DWT matrix retrieved from the 
input signal. Each CNN model’s design concludes with a fully connected layer that retains the extracted features 
from the input matrix as a vector of length F. Each CNN model has input layers with a constant and unchanging 
structure.
Different combinations of filter size and number for each CNN layer plus pooling options determine how 
effective these models become. We use CapSA to find the best settings for our three CNNs that process DWT, 
MFCC, and STFT features. CapSA uses a nature-based optimization approach to copy how capuchin monkeys 
find food during their daily searches. The optimization algorithm treats every set of CNN hyperparameters as a 
food location in its search territory. CapSA creates a virtual community of “capuchins” that move through the 
space while updating their positions based on personal experience and feedback from fellow capuchins.
Specifically, CapSA divides the population into “leaders” and “followers.” Leaders freely search the parameter 
space on their own as followers base their selection on leader behavior. CapSA uses both random sampling and 
proven strategies to find hyperparameter settings that reduce the error rate in CNN model training process.
We assess CNN model quality by training it on training data subsets to check its performance outcomes. The 
CapSA algorithm updates hyperparameter values step by step until it finds the best combination that reduces 
training errors and improves feature extraction from input data.
Our use of CapSA enables each CNN model to identify key features in DWT, MFCC, and STFT data through 
optimal hyperparameter settings. Our system uses optimized settings for each CNN which results in higher 
accuracy for both individual models and our complete system. The optimization technique is used to identify 
the characteristics of every convolution block:
•	 Length and width of the filters in each convolution layer.
•	 Number of filters in each convolution layer.
•	 Type of Pooling function.
The suggested technique determines the best configuration for each CNN model individually using CapSA. 
Training samples from the database are used to optimize each hyperparameter of the structure to minimize 
training error. Once the suitable setup for each CNN model is established, they are used to assess test samples. 
The purpose of using CapSA is to identify the most effective values for the hyperparameters of the CNN model 
layers. The adjustable parameters in the CNN models are as follows:
	1.	 Specifications for each convolution layer should include the size and quantity of filters. The CNN model 
assumes that the filters in each convolution layer have uniform dimensions in terms of length and breadth. 
Each convolution block in this scenario has two customizable parameters: size and quantity of filters. The 
filter size parameter is a continuous numerical variable that spans from 3 to 18. The “number of filters” option 
is limited to integers from 4 to 128, inclusive, and must increment by 4 each time.
Fig. 2.  The structure of the proposed CNN models for extracting DWT, MFCC, and STFT features.
 
Scientific Reports |         (2025) 15:9580 
6
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 7

2.	 Min, Max, Global, or Average functions may be used for pooling layers within the convolution blocks. You 
may choose the Pooling function type parameter when designing the optimization problem, with values 
ranging from 1 to 4. The applications of the Min, Max, Global, and Average functions are shown by numbers 
1 through 4.
	3.	 The amount of characteristics that the CNN model can extract from each sample depends on the size of the 
final fully linked layer. The method suggests specifying this as an integer with a range of 10 to 200.
The convolution blocks of CNN models may be customized by altering three optimization variables: convolution 
filter size, number of convolution filters, and pooling function type. The proposed CNN model consists of four 
convolution blocks, which generate a total of 12 optimization variables. In addition to the 12 criteria described 
before, another factor influences the size of the final fully linked layer in the CNN model. Every response vector 
in the black hole optimization (BHO) approach is a numerical vector with 13 elements. The first four components 
in each response vector indicate the predicted values for each convolution filter’s size (length and breadth), with 
search limitations [+ 3, + 18]. The number of filters used for each convolution layer is determined by the second 
four components of each response vector, which are natural values ranging from 4 to 128. Each convolution 
block’s pooling function set is determined by four natural integers between 1 and 4. The dimensions of the last 
fully connected layer in the Convolutional Neural Network model match the last optimization variable in the 
solution vector. The value falls between 10 and 200 as an integer.
Using the training error criteria, CapSA assesses each answer’s fitness throughout the CNN model’s 
optimization stage. First, the basic architecture of the CNN model is modified by adding a response vector that 
looks like x. Subsequently, the hyperparameters of the CNN model are adjusted using the values discovered in 
x. The SoftMax layer is then added to the CNN model. The CNN model’s training error is computed using this 
layer. Lastly, using the training samples as a basis, the fitness of the answer x is computed.
	
fitness (x) = F
Tr 
(5)
F is the number of training samples in which the true label of the sample differs from the predicted label of the 
CNN model. Tr stands for the total number of episodes of training. Since the CNN model, which is constructed 
based on the computation of the fitness for each answer, takes a long time to train, a limited number of training 
samples are employed in this stage. The structure provided for each response vector and the technique used to 
assess its fitness may be utilized to describe the optimization processes of each Convolutional Neural Network 
(CNN) model in the suggested approach utilizing CapSA.
Step 1) The initial population is randomly identified due to the defined bounds for every optimization 
variable.
Step 2) The fitness of every solution vector (Capuchin) is computed based on Eq. (5).
Step 3) The initial velocity of every Capuchin agent is set.
Step 4) Half of the Capuchin population is randomly chosen as leaders, and the rest are designated as follower 
Capuchins.
Step 5) If the number of algorithm iterations has reached the maximum G, go to step 13; otherwise, repeat 
the following steps.
Step 6) CapSA lifespan parameter is computed as follows41:
	
τ = β 0e
(
−β 1g
G
)β 2 
(6)
Where g shows the current number of iterations, and the parameters β 0, β 1, and β 2 have values of 2, 21, and 
2, respectively.
Step 7) for each Capuchin agent (leader and follower) like i, repeat the following steps:
Step 8) If i is a Capuchin leader; update its velocity based on Eq. (7)41:
	
vi
j = ρ vi
j + τ a1
(
xi
bestj −xi
j
)
r1 + τ a2
(
F −xi
j
)
r2
(7)
Where j shows the dimensions of the problem and vi
j​ represents the velocity of Capuchin i in dimension j. xi
j ​ 
indicates the position of Capuchin i for the jth variable and xi
bestj explains the best position of Capuchin i for 
the jth variable from the beginning until now. Moreover, r1 ​ and r2​ are two random numbers in the range [0, 
1]. At last, ρ  is the parameter of the impact of the previous velocity, which is set to 0.7.
Step 9) Update the new position of the leader Capuchins based on their velocity and movement pattern.
Step 10) Update the new position of the follower Capuchins due to their velocity and the leader’s position.
Step 11) Compute the fitness of the population members based on Eq. (5).
Step 12) If the entire population’s position was updated, go to Step 5; otherwise, repeat the algorithm from 
Step 7.
Step 13) Return the response with the least fitness value as the optimal configuration of the CNN model.
Each CNN model is constructed using the previously mentioned methodology, and it is used to assess test 
samples and categorize musical genres.
Classification and identification of music genres
In the last step of the suggested method, the features derived from each of the three CNN models are combined 
to establish the final audio signal properties. The three CNN models’ hyperparameters are first optimized using 
Scientific Reports |         (2025) 15:9580 
7
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 8

CapSA using the training set of data. Then, using the improved models, traits are extracted from the test samples. 
Preprocessing yields the DWT, MFCC, and STFT matrices for every test sample, same as in the training stage. By 
entering the output values from each CNN model’s last fully connected layer into its corresponding optimized 
CNN model, the test sample features are produced. These characteristics come together to form a vector, which a 
SoftMax classifier is used to classify. In the output neuron of the classification model, the test sample is allocated 
to the class with the greatest weight value. The number of target classes, or musical genres, is correlated with the 
number of output neurons.
Research finding
MATLAB 2021 was used to accomplish the suggested approach. As part of the suggested methodology, we used 
a 10-fold cross-validation strategy with many rounds. Based on the predetermined criteria, we assessed the 
effectiveness of our method in each iteration and compared it with other approaches. Comparing the context 
labels with the expected labels in the suggested data validation approach produced one of four results.
•	 TP (True Positive): The number of positive cases correctly determined by the model.
•	 FN (False Negative): The number of examples that the model mistakenly classified as negative.
•	 FP (False Positive): The number of examples that the model mistakenly classified as positive.
•	 TN (True Negative): The number of examples that the model correctly identified as negative.
Accuracy for every instance is the ratio of correct predicted output to total number of possible outputs for that 
instance.
	
Accuracy =
TP + TN
TP + FP + TN + FN 
(8)
One performance indicator called precision is used to calculate the accuracy rate of positive forecasts. One 
measure of precision, which is a measure of the accuracy of the minority class, is the percentage of all positive 
cases expected that a positive event was correctly predicted. Precision =
T P
T P +F P  (9)
We can calculate the ratio of accurate positive forecasts to all potential positive forecasts using the recall 
statistic. Recall includes the positive forecasts that were overlooked, while precision only considers the correct 
positive predictions out of all the positive forecasts. Recall allows us to quantify the extent to which the positive 
class was handled in this manner. Recall is used, and it’s detected. Recall =
T P
F N+T P  (10)
F-Measure is the harmonic mean of the recall and accuracy values achieved by a certain classification.
model.
	
F −Measure = 2 ∗Precision ∗recall
Precision + recall 
(11)
We have tested our proposed approach in three distinct ways for the sake of this essay; we will now go over each 
method individually.
•	 Proposed (PCNN + CapSA): The CapSA technique is used by the PCNN model to optimize each CNN com­
ponent’s parameters. A parallel convolutional neural network is what it is.
•	 Static PCNN: This mode uses the CNN model’s parallel structure while assuming that the CNN model’s con­
figuration stays unchanged.
•	 CNNSTFT + CapSA: In this instance, the genres of music may be identified by applying STFT features to a 
CNN model that has been improved by the CapSA approach.
We also conducted a comparative analysis between our proposed method and the ABO-NN, BAG, and VMS-
YOLO techniques, which are described in29,30, and31, respectively. In Fig. 3, the required precision is shown. 
As seen by the data in Fig. 3a, our strategy produced a value of 0.76 and 0.69, respectively, in contrast to the 
CNNST F T + CapSA technique and the VMS-YOLO method. Furthermore, as seen in Fig. 3b, our approach 
has achieved a superiority value of 1.7% in comparison to the VMS-YOLO method and 1.2% in comparison to 
the CNNST F T + CapSA method. The results of this study unequivocally demonstrate that our definition of 
musical genres was much more accurate than previous methods used to both datasets.
Figure 4 displays the confusion matrix. Ten music categories (foxtrot (507), salsa (47), slow waltz (65), wcswing 
(23.9), Viennese waltz (252), rumba (470), samba (468), tango (464), pasodoble (53), salsa (47), slow waltz (455), 
and jive (350) are represented by the rows and columns of the matrix in Fig. 4a. The accuracy of our proposed 
technique was 98.06%, 0.7% higher than that of the VMS-YOLO matrix. The GTZAN database, including ten 
categories (country, disco, hip hop, jazz, metal, pop, reggae, and rock), demonstrated our technique’s 96.20% 
accuracy (Fig. 4b). This is a 1.7% improvement over the VMS-YOLO matrix. The effectiveness and efficiency of 
our proposed solution was shown in both databases, indicating its superior performance and capabilities.
The accuracy, recall, and F-measure metrics, which are crucial for assessing the effectiveness of a method, 
are illustrated in Fig. 5. The CNNST F T + CapSA method, widely regarded as the most advanced approach, 
exhibits a notable 1.4% improvement in accuracy when compared to the proposed method (refer to subfigure 
5a). In addition, the accuracy of the proposed method improves by a significantly greater 1.9% in comparison 
to the VMS-YOLO method, providing further evidence of its efficacy. Analogous patterns can be observed in 
the precision criteria, as illustrated in Fig. 5b. The proposed method exhibits a substantial 1.2% enhancement 
in comparison to the CNNST F T + CapSA technique and a substantial 1.7% increase in comparison to the 
Scientific Reports |         (2025) 15:9580 
8
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 9

VMS-YOLO method. In terms of precision, the suggested method outperforms the competition, according to 
the study’s results.
Figure 5a presents valuable insights regarding the extent to which the proposed methodology fulfills the recall 
criterion. The proposed method exhibits a recall that is 1.4% higher than the established CNNST F T + CapSA 
technique. In addition, the recall performed by the proposed technique surpasses that of the BAG method by 
2.4%. These results are supported by Fig. 5b, which illustrates a recall enhancement of 1.2% compared to the 
CNNST F T + CapSA method and an even more substantial 1.7% improvement compared to the VMS-
Fig. 3.  Analyzing the average accuracy.
 
Scientific Reports |         (2025) 15:9580 
9
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 10

YOLO method. The results unequivocally illustrate the efficacy of the suggested approach in enhancing 
memory. In conclusion, the F-measure, a comprehensive statistic that merges precision and recall, is examined 
in Fig.  5a and b. Figure  5a illustrates that the suggested method outperforms the CNNST F T + CapSA 
method by 1.4% and the VMS-YOLO method by 2.1% with regard to F-measure improvement. In contrast, the 
CNNST F T + CapSA approach and the VMS-YOLO technique improved the F-measure by 1.2% and 1.7%, 
respectively, as shown in Fig. 5b. The results of this study demonstrate that the suggested approach significantly 
improves the aggregate F-measure.
The results presented in Fig.  6a illustrate that the proposed technique outperformed the comparative 
methods by 1.4%, achieving an accuracy rate of 90.31% across 13 distinct categories. This result unequivocally 
demonstrates the accuracy with which our method categorizes different musical genres. In addition, the GTZAN 
Fig. 4.  Analyzing the approaches using a confusion matrix.
 
Scientific Reports |         (2025) 15:9580 
10
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 11

database utilized in our research is illustrated in Fig.  6b. Once more, our approach demonstrated superior 
accuracy compared to the comparison methods by 1.2%. These outcomes demonstrate the efficacy of our 
methodology and its potential for categorizing various musical genres.
The recall criteria for the 13 and 10 categories are shown in Fig. 6c and d, respectively, showing how well 
our suggested method located occurrences of certain classes in the dataset. With a noteworthy recall score of 
96.16%, our technique outperformed the competing approaches by 1.4%, demonstrating its efficacy in musical 
genre categorization. Our solution also outperformed the comparable procedures by 1.2% in Fig. 6d, where it 
produced the maximum value of 96.20. All categories in both databases perform well for our suggested strategy, 
yet the categories of classical music and the blues have the lowest recall values for the ABO-NN methodology in 
this table. In Fig. 6e, our suggested method outperformed the comparable methods by 2.1%, with an F-measure 
value of 92.77%. Furthermore, Fig. 6f shows that our technique outperformed other methods by 1.2%, achieving 
the maximum value of 96.19%. These results demonstrate the method’s accuracy and memory performance, 
making it a useful tool for classifying musical genres. The receiver operating characteristic (ROC) curve is shown 
in Fig. 7. As shown in Fig. 7a, our strategy performs better than previous approaches in terms of true positive rate 
(TPR) and false positive rate (FPR), with an area under the curve (AUC) of 0.99. Furthermore, in comparison to 
other comparing methods, our suggested approach resulted in an AUC value of 0.99 and a statistically significant 
increase in TPR, as shown in Fig. 7b.
Fig. 5.  Analyzing the classification’s quality.
 
Scientific Reports |         (2025) 15:9580 
11
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 12

The strategies are compared in Table 1, which demonstrates that the suggested strategy (PCNN + CapSA) 
outperforms the other approaches in terms of accuracy. This approach has a high recall and F-Measure of 
96.1689 and 92.7717, respectively, in addition to its high accuracy of 90.3158. On the other hand, the ABO-NN 
approach performs worse than the others and has a lower accuracy of 79.4560.
The Precision, Recall, F-Measure, and Accuracy values for the various approaches are shown in Table 2. 
PCNN + CapSA, the suggested approach, received the highest scores (96.2079, 96.2000, 96.1957, and 96.2000, 
Fig. 6.  The values of precision (first row), recall (second row), and F-measure (third row) obtained from 
classifying samples of Extended-Ballroom (Left column) and GTZAN (right column).
 
Scientific Reports |         (2025) 15:9580 
12
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 13

respectively) for all criteria. When compared to other techniques, the ABO-NN methodology performs the 
lowest, with values of 81.9950, 82, 81.9810, and 82, respectively.
Ablation study
In order to assess the effectiveness of each component of our proposed framework, we perform an ablation 
study. This analysis was done by systematically deconstructing the full PCNN + CapSA model and observing 
the effects on performance. This, led to the following four cases employed for comparing with the proposed 
ensemble model:
•	 CNNMF CC + CapSA: This configuration uses only the CNN that was trained on the MFCC features and 
hyperparameters were tuned using CapSA. This removes the influence of STFT and DWT features and their 
corresponding CNNs while examining the role of MFCC features.
•	 CNNST F T + CapSA: This configuration uses only the CNN that was trained on STFT features, and hy­
per-parameter tuning is done using CapSA. This removes the influence of MFCC and DWT features and their 
corresponding CNNs while examining the role of STFT features.
Methods
Precision
Recall
F-Measure
Accuracy
Time (s)
Proposed (PCNN + CapSA)
96.2079
96.2000
96.1957
96.2000
1.0325
Static PCNN
93.0701
93
93.0084
93
1.0855
CNN_(STFT) + CapSA
95.0369
95
94.9956
95
0.7112
VMS-YOLO31
94.5274
94.5000
94.4896
94.5000
1.9232
ABO-NN29
81.9950
82
81.9810
82
0.7863
BAG30
93.5645
93.5000
93.5084
93.5000
0.0851
Table 2.  The proposed technique’s effectiveness in comparison to other methods in the GTZAN dataset.
 
Methods
Precision
Recall
F-Measure
Accuracy
Time (s)
Proposed (PCNN + CapSA)
90.3158
96.1689
92.7717
96.0766
1.021
Static PCNN
84.3224
93.0451
87.4983
92.8230
1.112
CNN_(STFT) + CapSA
88.9627
94.7879
91.3591
95.3110
0.7256
VMS-YOLO31
88.4583
93.7282
90.6647
95.3828
1.8892
ABO-NN29
79.4560
88.9569
82.4083
88.9474
0.8265
BAG30
86.7421
93.7314
89.5148
93.9474
0.1569
Table 1.  The proposed technique’s effectiveness in comparison to other methods in the extended-ballroom 
dataset.
 
Fig. 7.  Evaluation of the ROC curve.
 
Scientific Reports |         (2025) 15:9580 
13
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 14

•	 CNNDW T + CapSA: This configuration uses only the CNN trained on the DWT features and hyperpa­
rameter tuning is done using CapSA. This eliminates the influence of DWT features so that the contribution 
of each feature can be determined.
•	 PCNN (without CapSA): This configuration uses all three CNNs (MFCC, STFT, DWT) but does not use 
CapSA for hyperparameter optimization but uses the traditional grid search. This excludes the influence of 
the CapSA optimization algorithm.
The performance of each configuration was assessed using both the Extended-Ballroom and GTZAN datasets, 
in terms of accuracy, precision, recall, F-measure, and AUC.
From the ablation study presented in Table 3 for the Extended-Ballroom dataset and Table 4 for GTZAN 
dataset, we derive several insights.
•	 Superiority of Multi-Feature Representation: The full PCNN + CapSA model performs better than all sin­
gle-feature configurations ( CNNMF CC, CNNST F T , CNNDW T ) for all the performance metrics. This 
shows the effectiveness of using multiple feature representations (MFCC, STFT, DWT) for music genre iden­
tification. These assorted features capture different aspects of the audio signal; this way; the CNNs are able to 
learn from a more comprehensive set of features that is less prone to containing all the bias of the different 
sources; thus enhancing generalization performance.
•	 Crucial Role of CapSA: It is evident that the PCNN + CapSA model achieves a better performance than the 
PCNN (without CapSA) configuration. This also points to the importance of the CapSA algorithm in tuning 
hyperparameters of CNNs. By optimally searching the hyperparameter space, the proposed CapSA provides 
the specific architecture setting for each CNN, which contributes to better feature extraction, better generali­
zation characteristic, and thus higher accuracy of the classification.
•	 Feature Set Complementarity: The first observation from the ablation study is that the STFT features always 
perform well across the board, and when all three feature sets are used within the full PCNN + CapSA model, 
they outperform the other two feature sets. This indicates that the two features are independent and offer 
important information that when combined improves the model discrimination capability of distinct music 
genres.
We can attribute the superior performance of the proposed PCNN + CapSA model to the following key factors:
	1.	 Multi-Feature Representation: The proposed model takes advantage of all three forms of signal processing: 
MFCC, STFT, and DWT, to get the most comprehensive representation of the audio signal. This diversity in 
feature representation improves the power of the model to identify discriminative features of various types 
of music.
	2.	 Effective Hyperparameter Optimization: The hyperparameters are important to the performing of the CNNs 
and are fine-tuned by the CapSA algorithm. Specifically, for each classification task, CapSA finds those values 
of hyperparameters that enhance the model’s capacity for feature learning and reduce training error.
	3.	 Parallel Processing: The parallel processing architecture enables the feature extraction process to be carried 
out in parallel with the signal representations without interference from the others. This parallelism may 
faster the training and inference time comparing to the situation when all features are processed sequentially 
one by one.
The ablation study clearly shows that our proposed approach works well and is superior to the baselines. Combining 
multiple feature sets and the use of the CapSA algorithm for hyperparameter optimization are the main reasons 
why the proposed PCNN + CapSA model outperforms the other models in music genre classification. These 
Methods
Precision
Recall
F-Measure
Accuracy
AUC
Proposed (PCNN + CapSA)
96.2079
96.2000
96.1957
96.2000
0.9937
PCNN (without CapSA)
93.0701
93
93.0084
93
0.9778
CNNST F T + CapSA
95.0369
95
94.9956
95
0.9885
CNNMF CC + CapSA
91.3567
91.3000
91.3003
91.3000
0.9720
CNNDW T + CapSA
87.3006
87.2000
87.2019
87.2000
0.9448
Table 4.  Ablation study results on the GTZAN dataset.
 
Methods
Precision
Recall
F-Measure
Accuracy
AUC
Proposed (PCNN + CapSA)
90.3158
96.1689
92.7717
96.0766
0.9989
PCNN (without CapSA)
84.3224
93.0451
87.4983
92.8230
0.9768
CNNST F T + CapSA
88.9627
94.7879
91.3591
95.3110
0.9877
CNNMF CC + CapSA
85.3704
93.7184
88.4675
93.0622
0.9768
CNNDW T + CapSA
81.0844
89.9246
84.1291
90.1435
0.9552
Table 3.  Ablation study results on the extended-ballroom dataset.
 
Scientific Reports |         (2025) 15:9580 
14
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 15

results show the need to consider multiple feature representations, and the use of optimization for high accuracy 
in audio classification.
Discussion, complexity analysis, and limitations
In this section, we analyze the proposed model’s operational results and its computational demands while 
identifying its current constraints and proposing research opportunities.
Performance analysis
The proposed model shows superior performance against both single-feature CNN models and the PCNN 
without CapSA optimization in all evaluation criteria.
Our hybrid model achieves better results than single-feature CNNs which shows how combining features 
leads to improved performance. The model achieves improved results through its unified approach that 
combines DWT, MFCC, and STFT features because each technique offers distinct signal analysis benefits. The 
DWT system detects sudden audio changes and high sound frequencies whereas MFCC models the spectral 
details and STFT displays audio evolution across time and frequency. Using several signal processing techniques 
together builds a complete audio description that lets the model identify unique patterns in diverse musical 
genres.
Our model outperforms the standard PCNN model due to CapSA’s ability to effectively adjust CNN 
hyperparameters for optimal results. CapSA analyzes many CNN model options to find the most effective 
settings that boost feature recognition and reduce training inaccuracies. Our optimized approach boosts the 
performance of each CNN individually which results in higher accuracy across all classifications. Compared to 
recent neural network ensembles in audio domain such as42,43 and Ref.44, our ensemble approach exhibits several 
key advantages:
•	 Feature Extraction Diversity: By employing features from DWT, MFCC, and STFT together we develop a 
stronger audio signal description that surpasses approaches using a single feature extraction method.
•	 Hyperparameter Optimization: Our model distinguishes from other approaches by applying CapSA to tune 
each CNN model’s hyperparameters in the ensemble model. Our customized CapSA optimization approach 
for individual CNN models delivers superior results and better prediction capabilities than basic ensemble 
methods.
•	 Focus on Music Genre Classification: Our study addresses music genre classification as a specialized audio 
task instead of evaluating ensemble methods across multiple audio domains like the other papers have done.
Complexity analysis
Our model uses parallel processing to achieve better results yet demands greater computational resources than 
single CNN models. The last columns of Tables 1 and 2 display the runtime performance analysis.
Our three-parallel CNN model requires more time to classify samples (1.021 s for Extended-Ballroom and 
1.0325 s for GTZAN) than single-feature CNN models such as CNNST F T (0.7256 s for Extended-Ballroom 
and 0.7112 s for GTZAN). The increased prediction time results from the need to run more CNN models 
simultaneously. We can use different approaches to reduce the higher processing demands.
•	 Model Pruning: Stripping away unneeded database connections and filters in CNN models speeds up pro­
cessing while maintaining accurate results.
•	 Quantization: Converting CNN model weights and activations from 32-bit floating-point numbers to 8-bit 
integers helps increase performance by decreasing memory requirements and processing time during the 
inference phase.
•	 Hardware Acceleration: Networks using GPU and TPU hardware process CNN training and evaluation work 
quicker by executing multiple models in parallel operations.
Limitations and future directions
The proposed ensemble model achieved encouraging results in music genre classification tasks, but face 
limitations that point toward future research possibilities. The main limitations which lead to directions for 
future works include:
•	 Dataset Scope: We primarily tested our method using Extended-Ballroom and GTZAN datasets. Although 
these testing datasets have gained widespread acceptance they fall short of accurately reflecting the full spec­
trum of real-world musical experiences. To confirm the versatility of our approach we must apply it to addi­
tional music datasets that include various styles and larger samples.
•	 Computational Cost: Our model needs further development through research into efficient training and in­
ference solutions such as knowledge distillation and transfer learning to optimize its computational efficiency.
•	 Exploration of Alternative Ensembles: Testing ensemble techniques stacking boosting and Bayesian averaging 
alongside our current parallel architecture will help us find the best approach for music genre classification.
The proposed system delivers notable improvements in music genre classification capability. The system’s design 
with multiple feature types CapSA optimization and parallel structure forms an effective framework for good 
performance. Our next steps include solving these found issues and developing new ways to boost this approach’s 
effectiveness.
Scientific Reports |         (2025) 15:9580 
15
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 16

Conclusion
The number of songs arranged into playlists according to musical genres has increased as a result of the 
development of music streaming technologies. The internet’s progress has made music genre categorization 
more crucial for information retrieval. Because machine learning and deep learning techniques are so simple 
to use, they have become popular among academics, replacing more conventional approaches like human 
labeling and annotation. This work presents a new method for categorizing musical genres via the use of cutting-
edge multimedia tools and complex machine learning ideas. The method integrates CNN models as a parallel 
ensemble architecture to give a complete framework for characterizing stylistic elements in music, and uses 
CapSA to specify hyperparameters. With average classification accuracies of 96.07 and 96.20 on the GTZAN and 
Extended-Ballroom datasets, respectively, the findings show remarkable performance. The proposed method 
outperforms existing approaches and provides insightful information on how to blend various musical aspects, 
potentially improving label-free music recommendation playlists and user experiences with media players. 
This study highlights the efficacy of merging several signal processing techniques and CNN models to improve 
classification accuracy and media player efficiency, which represents a major improvement in the categorization 
of musical genres.
Data availability
All data generated or analysed during this study are included in this published article.
Received: 7 May 2024; Accepted: 14 February 2025
References
	 1.	 Degli Innocenti, E. et al. Mobile virtual reality for musical genre learning in primary education. Comput. Educ. 139, 102–117 
(2019).
	 2.	 Jakubec, M. & Chmulik, M. Automatic music genre recognition for in-car infotainment. Transp. Res. Procedia 40, 1364–1371 
(2019).
	 3.	 Eerola, T., Vuoskoski, J. K., Peltola, H. R., Putkinen, V. & Schäfer, K. An integrative review of the enjoyment of sadness associated 
with music. Phys. Life Rev. 25, 100–121 (2018).
	 4.	 Lee, S. H., Yoon, H. W., Noh, H. R., Kim, J. H. & Lee, S. W. Multi-spectrogan: High-diversity and high-fidelity spectrogram 
generation with adversarial style combination for speech synthesis. In Proc. of the AAAI Conference on Artificial Intelligence, 
35(14), 13198–13206 (2021).
	 5.	 McKay, C. Automatic music classification with jMIR (2010).
	 6.	 Kleć, M. & Koržinek, D. Unsupervised feature pre-training of the scattering wavelet transform for musical genre recognition. 
Procedia Technol. 18, 133–139 (2014).
	 7.	 Wehrmann, J. & Barros, R. C. Movie genre classification: a multi-label approach based on convolutions through time. Appl. Soft 
Comput. 61, 973–982 (2017).
	 8.	 Van Venrooij, A. & Schmutz, V. Categorical ambiguity in cultural fields: the effects of genre fuzziness in popular music. Poetics 66, 
1–18 (2018).
	 9.	 Coca, A. E. & Zhao, L. Musical rhythmic pattern extraction using relevance of communities in networks. Inf. Sci. 329, 819–848 
(2016).
	10.	 Aljanaki, A., Wiering, F. & Veltkamp, R. C. Studying emotion induced by music through a crowdsourcing game. Inf. Process. 
Manag. 52 (1), 115–128 (2016).
	11.	 Kalapatapu, P., Goli, S., Arthum, P. & Malapati, A. A study on feature selection and classification techniques of Indian music. 
Procedia Comput. Sci. 98, 125–131 (2016).
	12.	 Wang, Y., Lin, X., Wu, L. & Zhang, W. Effective multi-query expansions: collaborative deep networks for robust landmark retrieval. 
IEEE Trans. Image Process. 26 (3), 1393–1404 (2017).
	13.	 Bahuleyan, H. Music genre classification using machine learning techniques. Preprint at  https://arXiv.org/1804.01149 (2018).
	14.	 Silla, C. N., Koerich, A. L. & Kaestner, C. A. A machine learning approach to automatic music genre classification. J. Brazilian 
Comput. Soc. 14, 7–18 (2008).
	15.	 Karami, A. & Guerrero-Zapata, M. A fuzzy anomaly detection system based on hybrid PSO-Kmeans algorithm in content-centric 
networks. Neurocomputing 149, 1253–1269 (2015).
	16.	 Silla, C. N. Jr, Koerich, A. L. & Kaestner, C. A. Feature selection in automatic music genre classification. In 2008 Tenth IEEE 
International Symposium on Multimedia, 39–44  (IEEE, 2008).
	17.	 Cheng, G., Ying, S., Wang, B. & Li, Y. Efficient performance prediction for apache spark. J. Parallel Distrib. Comput. 149, 40–51 
(2021).
	18.	 Pérez-Marcos, J. et al. Multi-agent system application for music features extraction, meta-classification and context analysis. 
Knowl. Inf. Syst. 62, 401–422 (2020).
	19.	 Wassi, G., Iloga, S., Romain, O., Granado, B. & Tchuenté, M. FPGA-based simultaneous multichannel audio processor for musical 
genre indexing applications in broadcast band. J. Parallel Distrib. Comput. 119, 146–161 (2018).
	20.	 Li, J. et al. An evaluation of deep neural network models for music classification using spectrograms. Multimedia Tools Appl., 1–27 
(2022).
	21.	 Despois, J. Finding the genre of a song with Deep Learning-AI Odyssey part. 1 (2018).
	22.	 Foleis, J. H. & Tavares, T. F. Texture selection for automatic music genre classification. Appl. Soft Comput. 89, 106127 (2020).
	23.	 Liu, C., Feng, L., Liu, G., Wang, H. & Liu, S. Bottom-up broadcast neural network for music genre classification. Multimedia Tools 
Appl. 80, 7313–7331 (2021).
	24.	 Gunawan, A. A. & Suhartono, D. Music recommender system based on genre using convolutional recurrent neural networks. 
Procedia Comput. Sci. 157, 99–109 (2019).
	25.	 Allamy, S. & Koerich, A. L. 1D CNN architectures for music genre classification. In 2021 IEEE Symposium Series on Computational 
Intelligence (SSCI), 01–07  (IEEE, 2021).
	26.	 Scarpiniti, M., Scardapane, S., Comminiello, D. & Uncini, A. Music genre classification using stacked auto-encoders. Neural 
Approaches Dynamics Signal. Exchanges, 11–19 (2020).
	27.	 Melo, D. D. F. P., Fadigas, I. D. S. & Pereira, H. B. D. B. Graph-based feature extraction: a new proposal to study the classification 
of music signals outside the time-frequency domain. Plos One 15(11), e0240915. (2020).
	28.	 Nanni, L., Costa, Y. M., Aguiar, R. L., Silla, C. N. Jr & Brahnam, S. Ensemble of deep learning, visual and acoustic features for music 
genre classification. J. New. Music Res. 47 (4), 383–397 (2018).
Scientific Reports |         (2025) 15:9580 
16
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

## Page 17

29.	 Jaishankar, B., Anitha, R., Shadrach, F. D., Sivarathinabala, M. & Balamurugan, V. Music genre classification using African Buffalo 
optimization. Comput. Syst. Sci. Eng. 44(2). (2023).
	30.	 Prabhakar, S. K. & Lee, S. W. Holistic approaches to music genre classification using efficient transfer and deep learning techniques. 
Expert Syst. Appl. 211, 118636 (2023).
	31.	 Cheng, Y. H. & Kuo, C. N. Machine learning for music genre classification using visual mel spectrum. Mathematics 10 (23), 4427 
(2022).
	32.	 Li, T. Optimizing the configuration of deep learning models for music genre classification. Heliyon 10(2). (2024).
	33.	 Ahmed, M. et al. Musical Genre Classification Using Advanced Audio Analysis and deep Learning Techniques (IEEE Open Journal of 
the Computer Society, 2024).
	34.	 Wijaya, N. N., Setiadi, D. R., I., M. & Muslikh, A. R. Music-genre classification using bidirectional long short-term memory and 
mel-frequency cepstral coefficients. J. Comput. Theor. Appl. 1 (3), 243–256 (2024).
	35.	 Chen, J. et al. A hybrid parallel computing architecture based on CNN and transformer for music genre classification. Electronics 
13 (16), 3313 (2024).
	36.	 Tzanetakis, G. & Cook, P. Musical genre classification of audio signals. IEEE Trans. Speech Audio Process. 10 (5), 293–302 (2002).
	37.	 Marchand, U. & Peeters, G. The extended ballroom dataset. In Proc. 17th Int. Soc. Music Inf. Retr. Conf., Extended Abstr. Late-
Breaking Demo Session (ISMIR) (2016).
	38.	 Singh, B. K., Verma, K. & Thoke, A. S. Investigations on impact of feature normalization techniques on classifier’s performance in 
breast tumor classification. Int. J. Comput. Appl. 116(19) (2015).
	39.	 Gupta, S., Jaafar, J., Ahmad, W. W. & Bansal, A. Feature extraction using MFCC. Signal. Image Process.  Int. J. 4 (4), 101–108 (2013).
	40.	 Mateo, C. & Talavera, J. A. Short-time Fourier transform with the window size fixed in the frequency domain. Digit. Signal Proc. 
77, 13–21 (2018).
	41.	 Braik, M., Sheta, A. & Al-Hiary, H. A novel meta-heuristic search algorithm for solving optimization problems: capuchin search 
algorithm. Neural Comput. Appl. 33, 2515–2547 (2021).
	42.	 Nadkarni, R., Nikolakakis, E. & Marinescu, R. AFEN: Respiratory disease classification using ensemble learning. Preprint at 
https://arXiv.org/2405.05467 (2024). 
	43.	 Trapanotto, M., Nanni, L., Brahnam, S. & Guo, X. Convolutional neural networks for the identification of African lions from 
individual vocalizations. J. Imaging 8 (4), 96. https://doi.org/10.3390/jimaging8040096 (2022).
	44.	 Liu, J. et al. Birdsong classification based on ensemble multi-scale convolutional neural network. Sci. Rep. 12(1), 8636 (2022). 
Author contributions
All authors wrote the main manuscript text. All authors reviewed the manuscript.
Declarations
Competing interests
The authors declare no competing interests.
Additional information
Correspondence and requests for materials should be addressed to Y.Z. or T.L.
Reprints and permissions information is available at www.nature.com/reprints.
Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and 
institutional affiliations.
Open Access   This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 
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
Scientific Reports |         (2025) 15:9580 
17
| https://doi.org/10.1038/s41598-025-90619-7
www.nature.com/scientificreports/

