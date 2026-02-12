# of drum music scores based on

**Year:** D:20

---

Intelligent generation method
of drum music scores based on
improved CNN and STFT
Yuting Ni
Existing music score generation methods are Limited by the scene Limitations and the quality of their
generated scores is relatively Limited. To address these problems, an intelligent music score generation
method combining short-time Fourier transform and improved convolutional neural network is
proposed. The study firstly utilizes short-time Fourier transform to transform the time-frequency
of music signals, and then inputs the transformed time-frequency information into an improved
convolutional neural network model. The model improves the accuracy and diversity of music score
generation by introducing label enhancement strategy and internal convolution structure. The method
may effectively increase the quality of music score creation on various music datasets with strong
generalization ability, according to the experimental results. The matching rate and complete rate of
the generated score of the proposed method were 92% and 95%, respectively, and its score generation
time was only 1.05s. The proposed method could improve the efficiency and quality of the music score
generation. The intelligent music score generation method can help the drum learners understand their
own performance in time, and give feedback on their training to improve the learning efficiency. Keywords  Improvement, CNN, STFT, Music score generation, Internal convolution, Labeling
Music is an art composed of elements such as melody, harmony, rhythm and timbre, which can express
emotions and convey information, and is an important part of human culture. Digital processing and intelligent
music production have steadily emerged as a research hotspot as science and technology have advanced1. As
an important percussion instrument, the drum set occupies a special position in music education. It can not
only train learners’ sense of rhythm and coordination, but also enhance musical expression and creativity2. However, the current drum learning is mainly one-on-one teaching by teachers, with limited teacher teaching
resources and high learning costs3. If it can be combined with intelligent technology for assisted teaching, it will
further enhance the teaching efficiency and reduce students’ dependence on teachers4. Intelligent music score
generation is the basis for assisted instruction, which automatically recognizes and converts the drumming
music played by the learner into sheet music during practice. In this way, learners can instantly access their
music scores to better understand the musical structure and rhythmic patterns5. In recent years, intelligent sheet
music generation has also gradually become a key direction of scholars’ research. Gu et al. proposed a general
framework for implementing two tasks of multimodal transportation in an attempt to enhance the accuracy and
efficiency of automatic lyrics transcription and music transcription tasks. To address the lack of labeled data,
the architecture used a self-supervised learning model as both a visual and an auditory encoder. It also added
a residual cross-attention method to further combine video and audio data. The results demonstrated that the
method achieved a transcription accuracy of 92.45%6. A music transcription method was proposed by Minor
et al. in order to solve the musician’s difficulty in finding sheet music by retrieving the music information and
generating the sheet music automatically. The study used the note value detection method to identify the window
frequency by Fourier transform. The outcomes revealed that the music transcription accuracy of this method
reached 95.11%7. Liang et al. proposed an automatic transcription method based on combining convolutional
neural network (CNN) and bi-directional gated recurrent unit (GRU) in an effort to address the problem of the
difficulties in automatic transcription due to the polyphonic characteristics of piano tones. The method further
improved the transcription accuracy by analyzing the piano pitch characteristics. The outcomes revealed that
the automatic transcription accuracy of the method was 97.10%8. To give a more comprehensive overview of
symbolic music generating approaches, Ji et al. conducted a task-oriented assessment of the field using deep
learning (DL) techniques. The study utilized this survey to analyze the motivation as well as the functionality of
the current mainstream models. The results were summarized with datasets suitable for various tasks and discuss
the existing challenges faced by the method9. College of Arts, Xiamen University, Xiamen 361005, China. email: Nyt2024@163.com
OPEN
Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports

Whereas CNN is a powerful DL model that excels in image recognition and processing, it is also applicable
to the processing of music signals. By training the CNN model to recognize drum beats with different timbres
and rhythms, accurate recognition of drum playing and score generation can be achieved10. Qian et al. proposed
an emotion decoding method based on electroencephalogram signals and CNN in order to effectively recognize
people’s various emotions. The method extracted emotional features from electroencephalogram signals for
decoding and then classified them. The findings demonstrated that the method’s accuracy for emotion cognition
exceeded 90%11. Ghatas et al. proposed a CNN-based classification model in order to estimate music difficulty. The model converted a symbolic music file played on a piano into a rolling representation of the piano and trained
the model on the parts labeled with difficulty. The findings demonstrated that, in comparison to traditional
methods, the method’s estimating accuracy was increased by over 10%12. Shen et al. proposed a new method of
voice quality evaluation based on one-dimensional CNN to address the problems of poor information fusion
efficiency and low robustness of the current singing and pronunciation quality evaluation methods for vocal
students. The method combined wavelet neural network and CNN to further improve the information fusion
effect. The findings indicated that the evaluation accuracy of the method reached 95%13. To achieve effective
retrieval of music, Zhang proposed a CNN-based music feature recognition method. The method used ternary
samples as training samples and used CNN to extract the music melody features and recognize its genre. The
findings indicated that the retrieval accuracy of the method rubber oils traditional CNN and support vector
machines, with higher body recognition accuracy and less recognition time14. In summary, there is still considerable room for improvement in existing methods of generating intelligent
music scores, especially when it comes to dealing with complex musical structures and emotional expressions. The existing methods are still insufficient in handling complex musical structures and emotional expressions,
and it is difficult to fully capture the delicate emotions and complex rhythmic changes in music. The current
issue that needs to be addressed is how to enhance the accuracy of sheet music generation and strengthen the
ability to delicately capture the emotions and rhythms of music. This will allow for more realistic and expressive
music creation15. Therefore, the study proposes an intelligent music score generation method based on improved
CNN and short-time Fourier transform (STFT), which extracts the music feature information through STFT
and automatically generates the music score using improved CNN. The study aims to provide learners with
personalized practice suggestions and feedback based on their performance level and progress. Through the
intelligent music score generation method, learners can improve their performance skills in a targeted way. The
innovativeness of the research lies in:
(1) Label enhancement training method: A joint label training strategy allows each time frame to correspond
to multiple drum labels, enabling more accurate capture of complex musical structures.
(2) Internal convolution structure: By introducing internal convolution, redundant computational steps are
reduced, computational efficiency is improved, and the model structure is simplified. Methods and materials
To assist drum music learners, the study proposes an intelligent music score generation method based on
improved CNN and STFT. To better capture the frequency features of the music signal, the study first uses STFT
to transfer the sound signal from the time domain to the frequency domain. Then, the converted spectrum is
analyzed and learned by the improved CNN, which in turn realizes the automatic generation of music score. Time-frequency transformation of music signals based on STFT
The main methods for automatic generation of drum music scores are segmentation and classification-based
methods and activation-based methods. The first method relies on the recognition of drumming patterns and
the understanding of rhythmic structures, and has a relatively high error rate. In contrast, activation-based
methods focus on modeling the drummer’s playing habits and techniques, and algorithms are used to generate
drum sequences with dynamic changes and expressiveness16. Therefore, the study adopts the activation-based
score generation method, as shown in Fig. 1. In Fig.  1, the study combines the STFT and the improved CNN to realize the automatic generation of
drum music sheet music through the operations of time-frequency conversion, feature mapping, and label
reinforcement. It mainly consists of three modules, which are time-frequency conversion module, CNN
activation module, and peak extraction module. The activation module uses an improved CNN model to capture
the subtle rhythmic changes of the music. From the feature maps produced by the activation module, the peak
extraction module is in charge of identifying noteworthy rhythmic peaks that correlate to the crucial percussion
moments in drumming. Before the automatic generation of music scores, the study uses STFT to analyze the
time-frequency of the sound signal and transforms it to obtain the Mel time-frequency map. The specific flow of
the time-frequency transformation is shown in Fig. 2. In Fig. 2, in order to make the captured audio signals have the same length for better feature extraction
and model training in the subsequent score generation, the study performs a length-alignment process on the
audio signals. The study first normalizes the audio signal and adds appropriate 0-symbol frames at the end of
the processed audio segment. At the end of the processing, frame division is performed and time-frequency
conversion is performed by combining the window function and discrete Fourier transform. To further improve
the utilization of the audio features, further filtering is performed using a Mel filter. The specific process of
converting dual-channel audio to mono in the preprocessing stage is shown in Eq. (1). Si =
{
S1
i, n = 1
S1i+S2i, n = 2 
(1)
Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

In Eq. (1), S1
i and S2
i are mono and dual channel audios, respectively. n is the quantity of audio channels. Si
is the processed mono audio. is the sample point sequence quantity. Sound is mainly composed of physical
characteristics such as timbre, frequency, amplitude, etc., and these characteristics are more obvious in the time-
frequency domain (TFD). Among them, two physical quantities, frequency and amplitude, can be clearly shown
in the TFD by STFT. Moreover, the ranges of sound signals are not the same. Before the time-frequency signal
conversion, it is necessary to unify the sampling rate of the audio signal and normalize the processed signal. When the maximum value of the absolute value function is equal to 0, the study sets the normalized audio signal
as its initial signal. Whereas, when its maximum value is not equal to 0, it is necessary to carry out calculations
to process it, as expressed in Eq. (2). S′
i (i) =
Si
max {abs [S1,..., Sm]}
(2)
In Eq. (2), abs [] is the absolute value function. S′
i is the normalization result. max () is the maximum value
screening process. After pre-processing the audio signals, the study is framing them. The framing operation is
shown in Fig. 3. In Fig. 3, the study splits the audio signal into multiple short-time frames by adding window processing to
better capture the local features of the signal. The length of each frame is chosen to be 20ms ~ 40ms, and there
is some overlap between frames to ensure the continuity of the signal. During the process of frame splitting, the
choice of window function is crucial for the feature extraction of the signal. Hamming window is widely used
because of its good performance in reducing spectral leakage. Therefore, the Hamming window is chosen as the
window function for frame segmentation in the study. This is due to the fact that the Hamming window has a
better width of the main flap and lower level of the side flap in the frequency domain, which helps to reduce the
inter-frame leakage. The Hamming window function is calculated as shown in Eq. (3).
w = 0.54 −0.46cos 2πi
m-1
(3)
In Eq.  (2), m window length. w is the window function. After framing, the study utilizes discrete Fourier
transform to transform the audio signal for processing. After obtaining the spectrum, in order to further extract
the characteristic parameters of the audio signal, the study uses Mel filter for further filtering process. Finally, Fig. 2. The specific flow of time-frequency conversion. Fig. 1. Method flow of music score generation based on STFT and improved CNN. Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

the study uses the obtained Mel time-frequency as the input data for the CNN model. It provides data support
for the subsequent music score generation. Improved CNN-based score generation model construction for drum set
After processing the input audio signals using STFT and Mel filters, the study feeds these signals into the CNN
model for activation processing. The CNN model outputs frame level activity values after activation processing
and performs peak extraction, which leads to feature extraction of the audio signal. Then, the CNN is used to
classify the performance information in order and map the extracted features to the individual hit points of
the drum set. The hitting patterns of different drum hits in the audio signal are recognized and converted into
symbols on the music score17. For the time-frequency transformed Mel time-frequency map, the study inputs
the features into the CNN model on a frame-by-frame basis. The formula for obtaining the context is shown in
Eq. (4). Con (k) = concat {T (k) T (k + 1),..., T (k + h + 1)}
(4)
In Eq. (4), T (k) denotes the time-frequency of the kth frame. h is the context size. concat is the splicing
operation. Con (k) is the context frame result. After obtaining the context of size 16 frames, the study inputs
it into the CNN for mapping classification. The activity values of the drums are obtained through mapping
classification, which leads to the generation of the music score. In this process, the CNN model labels the signals
according to the classification and recognition results, and maps their hit points to the corresponding locations
in the music score. The network structure of the CNN for the research setup is shown in Fig. 4. In Fig.  4, the convolutional network structure proposed in the study contains three main parts: the
downsampling layer, the pooling layer, and the fully connected layer. While the downsampling layer has four
convolutional structures of 3 × 3 size and an activation function. After the signal is output from the CNN
model, the study obtains the distribution maps of the activity values of the components of the drum set. These
distribution maps can clearly show the activity level of each drum component on the time series, thus providing
accurate data support for subsequent score generation. The study uses localized peaks in the activity values as
starting points for drum events. The distance between two localized peaks needs to be greater than 4 frames. The
study uses Sigmoid cross entropy (CE) as the loss function (LF), as shown in Eq. (5). Lloss =
N
∑
i=1
ξiLs (fi (x), yi)
(5)
In Eq. (5), Lloss is the LF of the training process. Ls (·) is the Sigmoid CE loss. fi (x) is the output after CNN. ξi
is the weight of the corresponding drum component. N is the number of drum components. The study assigns
Fig. 4. The network structure of CNN. Fig. 3. The specific process of framing operation. Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

weights to the drum components based on their variability and frequency of occurrence. The weight value of kick
drum (KD) is set to 0.5, snare drum (SD) is set to 2.0, and hi-hat (HH) is set to 1.5. Whereas, the weights of high,
medium, and low tom, suspended cymbal, and rhythm cymbal are 0.8, 0.8, 0.8, 1.0, 1.0, and 1.0, respectively. It is found in the course of the study that the drum events by the proposed CNN model extraction has some
limitations with a single label for the training process. This leads to a reduction in the recognition accuracy of
the model when dealing with complex rhythms and multiple drums intertwined. To address this issue, the study
further introduces the joint labels training strategy, which allows each time frame to correspond to multiple
drum labels, thus capturing complex musical structures more accurately. The joint labels labeling method is
shown in Fig. 5. In Fig. 5, joint labels contain the track signals of different drum components, and in the process of activity
recognition, it is necessary to first identify the track to which the signal belongs, and then discriminate its activity
value afterwards. After the introduction of joint labels training method, the study applies it to the training as
well as the common label training, and adopts the self-distillation method to realize the coding layer sharing
of the two classifiers. Further, it realizes the common training of the two. After the training is completed, the
joint labels obtained from the joint labels trained classifiers need to be aggregated. The process of aggregation is
shown in Eq. (6). Px,z,u =
(
1 + e
−1
M
∑M
j=1 uT )-1

(6)
In Eq. (6), z is the network parameters of the coding layer. u is the network parameters of the joint classifier. M is
the quantity of tracks. Px,w,v is the label after aggregation. The research on label enhancement training is based
on a multi-task learning framework using DL. This framework enhances the model’s ability to recognize different
drum components by sharing the underlying feature extraction layer. The internal convolutional structure can
effectively capture the features of the TFD, enhance the expression of musical signals, and thereby improve the
recognition accuracy of complex rhythms. Moreover, to further enhance the computational efficiency of the
model and simplify the model structure, the study optimizes the convolutional model structure. The study first
introduces the inner convolution to replace the convolutional layers in its convolutional module. The inner
convolution is an efficient convolutional method, which locally connects inside each convolutional layer and
reduces redundant computational steps. The improved CNN structure is shown in Fig. 6. In Fig. 6(a), after inputting the feature map, the study efficiently compresses its feature map through the inner
convolution operation, which reduces the consumption of computational resources. The internal convolution
operation is not simply dot product but achieves feature extraction through local connection. Internal
convolution ensures feature alignment by making local connections within each convolution kernel. The feature
compression process utilizes the efficiency of internal convolution to gradually reduce the dimensionality of the
feature map. This reduces computational complexity and improves model efficiency. The specific steps include
feature extraction, local connection, and dimension compression. This ensures that key information is retained
while redundant computations are reduced. Feature compression is achieved by replicating and expanding
the feature map through channels, enhancing multi-dimensional information fusion, and further improving
the feature expression ability. First, channel replication of the original feature map is performed to generate
multi-channel copies. Second, local concatenation and feature extraction are performed for each channel using
internal convolution. Finally, dimension compression technology merges multi-channel information to form
an efficient feature representation. This ensures that key feature information is retained while reducing the
computational load. In Fig. 6(b), the four downsampling layers of the improved CNN structure have more than
one inner convolution module, which contains two convolution layers and one inner convolution kernel. By
introducing the involution module, the number of channels in the model is further reduced. In summary, the
study establishes an intelligent music score generation method based on improved CNN and STFT. First, the
Fig. 5. The labeling method of joint labels. Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

method extracts and transforms the audio signal features using STFT. Then, it analyzes and recognizes the signal
using a CNN model that introduces label enhancement training and an involution module. Finally, it generates a
music score. The convolution kernel size of the model is 3 × 3, with a step size of (1) The activation function uses
ReLU, the pooling layer adopts Max pooling, the pooling window is 2 × 2, and the step size is (2) The network has
four downsampling layers, each of which is followed by an involution module that effectively reduces the feature
dimension. The learning rate is set to 0.001, and the Adam optimizer is employed to update the parameters and
enhance convergence speed. Results
To test the performance of the proposed intelligent music score generation method based on improved CNN and
STFT, the study designs a series of experiments to discuss and analyze it. Analysis of the training situation of the improved CNN model
The study uses the audio of frame drum performances contained in the Million Song Sataset (MSD) as a
dataset. The dataset contains a variety of styles and rhythms of drum performance, totaling 5811 songs. The
MSD dataset is currently one of the largest open-source music datasets. It covers a wide range of genres and
playing techniques. The MSD dataset includes audio waveforms, spectrograms, rhythm patterns, etc. Among
them, the audio waveform records the original signal of the performance, the spectrogram reveals the frequency
distribution, and the rhythm pattern reflects the rhythm changes of the performance. By analyzing these features
in depth, the model can more accurately capture the essential characteristics of music, thereby improving the
precision and fidelity of music score generation. For the experiments, the study divides the dataset into training,
validation, and test sets with a ratio of 7:1:2. The experimental environment is as follows: the operating system
is Windows 10, the memory is 64 GB, the processor is Intel Core i7-8700 K, and the graphics card is NVIDIA
GeForce GTX 1080 Ti. During the training process, the Adam optimizer is used with an initial learning rate of
0.001 and a CE LF. To prevent overfitting, Dropout technique is introduced and a hold probability of 0.5 is set. To test the training of the improved CNN proposed by the study, the study compares the conventional CNN with
recurrent neural network (RNN) and GRU, which are currently commonly used as network models for music
information processing. The comparison results are shown in Fig. 7. In Fig. 7(a), the training accuracy of several network models gradually increase as the number of training
times increases. Among them, the convergence speed of the studied improved CNN model is basically the same
as that of the relatively simpler structure of GRU, which has a far higher accuracy of convergence than the other
models. It reaches a convergence accuracy of 0.94 after only up to 36 iterations. In Fig. 7(b), the recall of the
improved CNN model peaks at 50 iterations, with an accuracy of 92%. In summary, the improved CNN model
has better convergence and is able to achieve the target precision with fewer training times. This is because
the research introduces depthwise separable convolutions, which effectively reduces the number of parameters
and enhanced the model’s generalization ability. At the same time, a multi-scale fusion strategy is incorporated
Fig. 6. The improved network structure of CNN. Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

into the feature extraction stage to increase the model’s sensitivity to features of different frequencies. Thus, the
convergence speed is accelerated while ensuring accuracy. To further examine the training of the improved CNN proposed in the study, the study compares the change
in F1 value of the centralized model on the dataset for both drum components, KD and SD. The F1 value is
a comprehensive indicator for measuring the performance of a model. Its value is the harmonic mean of the
precision and recall rates, which reflects the model’s overall performance. This is specifically shown in Fig. 8. In Fig. 8(a) and 8(b), the F1 value of several models gradually grows with the increase of the iterations. Moreover, for the analysis results of two different drum components, the magnitude of the change is not the
same. Among them, the improved CNN model has the fastest convergence of F1 value, and its convergence value
reaches 0.93, which is significantly higher compared with other models. Improvement effect of CNN model with the introduction of label enhancement strategy and
internal convolution structure
To test the improvement effect of the label enhancement strategy proposed in the study on the CNN model, the
study compares the accuracy and recall of the model before and after the introduction of the strategy for the
three drum components KD, SD, and HH. The results are shown in Fig. 9. In Fig. 9(a), as a whole, the accuracy of the model after the introduction of the strategy is significantly higher
than that of the model before the introduction of the strategy, and its average accuracy reaches 93.45%. In
Fig. 9(b), the recall of the model after the introduction of the strategy is also higher compared to the model
before the introduction of the strategy. Its recall rate reaches 92.12%, which indicates that the introduction of
the label enhancement strategy and internal convolution structure effectively improves the model’s ability to
recognize drum components. Fig. 8. Comparison of training F1 values of several models. Fig. 7. Comparative results of training the improved CNN model. Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

To examine the improvement effect of the proposed internal convolution structure on the CNN model, the
study compares the calculation time as well as the computational accuracy of the model before and after the
introduction of the internal convolution structure. Table 1 depicts the outcomes. In Table 1, after the introduction of internal convolution structure, the model shows a significant reduction
in the calculation time and also an improvement in the accuracy. For the KD component, the average calculation
time before the introduction of internal convolution structure is 1.24s, and the accuracy rate is 88.7%. After the
introduction of internal convolution structure, the calculation time is shortened to 0.97s, and the accuracy is
increased to 93.35%. For the SD component, the calculation time is reduced from 1.16s to 0.91s, and the accuracy
is improved from 87.75 to 92.55%. For the HH component, the calculation time is reduced from 1.31s to 1.04s,
and the accuracy is improved from 89.2 to 93.95%. The findings indicate that the incorporation of internal
convolution structures within the model not only enhances its computational efficiency but also significantly
improves its recognition accuracy. Application effect of music score generation method based on improved CNN and STFT
To test the effectiveness of the application of the proposed music score generation method (Method 1) based
on improved CNN and STFT, the study compares it with the music score generation method (Method 2) in
literature18, the music score generation method (Method 3) in literature19, and the music score generation method
(Method 4) in literature20 for comparative experiments. Five drum learners are selected for the experiment, and
they are asked to play 10 identical pieces of music and generate scores using each of the four different methods. The score recognition speed and score integrity of the four methods are shown in Fig. 10. In Fig. 10(a), Method 1 demonstrates superiority over the other three methods in terms of score recognition
speed, with an average time of 1.05 s, the shortest of the four. Its average time is only 60% of Method 2, 50% of
Method 3, and 40% of Method 4. This indicates that the improved CNN model combined with STFT technique
has higher efficiency in processing music signals. In Fig. 10(b), Method 1 also excels in terms of score integrity,
with a recognition accuracy of 95%. This is higher than 85% for Method 2, 80% for Method 3, and 75% for
Method 4. This indicates that the method is able to maintain the integrity of the score better while maintaining
fast score recognition, providing more accurate score information for drum learners. To further validate the performance of Method 1 in music score generation, the study compares the score
average matching rate, maximum matching rate, complete rate, and calculation time of several methods. The
Project
Test 1
Test 2
Calculation time (s)
Accuracy (%)
Calculation time (s)
Accuracy (%)
KD
Pre-introduction
1.23
8.5
1.25
88.7
Post-introduction
0.98
93.2
0.96
93.5
SD
Pre-introduction
1.15
87.6
1.17
87.9
Post-introduction
0.92
92.4
0.90
92.7
HH
Pre-introduction
1.30
89.1
1.32
89.3
Post-introduction
1.05
93.8
1.03
94.1
Table 1. Comparison of computational efficiency and accuracy of the model before and after the introduction
of the internal Convolution structure. Type of drum assembly
Accuracy
1.00
0.95
0.90
0.85
0.80
0.75
0.70
0.65
0.60
0.55
0.50
(a) Accuracy
Before
introduction
After
introduction
Recall rate
1.00
0.95
0.90
0.85
0.80
0.75
0.70
0.65
0.60
0.55
0.50
(b) Recall rate
Before
introduction
After
introduction
KD
SD
HH
Type of drum assembly
KD
SD
HH
Fig. 9. The accuracy and recall rate of the model before and after introducing the strategy. Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

score matching rate refers to the degree of matching between the generated score and the actual performed score,
while the complete rate reflects the detail retention of the generated score. Table 2 depicts the outcomes. In Table 2, Method 1 outperforms the other three methods in all metrics. The average matching rate and
maximum matching rate are 92% and 98%, respectively. In addition, the completion rate of Method 1 reaches
95%. In terms of calculation time, Method 1 can complete the music score generation in 1.05 s, which is much
faster than the other methods, which provides the possibility of real-time music score generation. In summary, Method 1 not only has obvious advantages in speed, but also excels in accuracy and completeness. This fully
demonstrates the effectiveness and practicality of combining improved CNN models and STFT techniques in
the field of intelligent music score generation. To further test the performance of the proposed music score generation method in the research, a comparative
experiment is conducted between it and the existing advanced methods. The comparison methods include
MusicNet, MuseScore, and DeepJ. The comparison indicators include pitch deviation rate for verification,
matching accuracy rate, beat alignment error (BAE), completeness rate, and calculation time. The generalization
ability of this method is tested by the study on more different datasets. The selected datasets include Giantmi-
piano and Expanded Groove MIDI (E-GMD). The comparison results are shown in Table 3. As shown in Table 3, all the indicators of Method 1 are significantly better than those of other methods. Its
pitch deviation rate is 0.12%, its note matching accuracy rate is 91.00%, and its BAE is 10.34 ms. The quality
of the generated musical scores is significantly higher than that of other methods. It demonstrates relatively
excellent performance in both the piano and electronic drum datasets. The research utilize several methods to identify different drum components and rhythm patterns, and
compares the recognition accuracy rates of each method. The comparison results are shown in Table 4. Method
Pitch deviation rate (%)
Matching accuracy rate (%)
BAE (ms)
Completeness rate (%)
Calculation time (s)
GiantMIDI-Piano
Method 1
0.12
91.00
10.34
93.47
1.05
MusicNet
0.35
84.31
20.00
85.32
2.55
MuseScore
0.28
88.45
15.64
89.12
2.00
DeepJ
0.40
80.36
22.48
82.60
2.97
E-GMD
Method 1
0.13
91.01
10.32
93.50
1.04
MusicNet
0.37
84.02
19.78
85.34
2.46
MuseScore
0.30
88.43
16.00
89.36
1.98
DeepJ
0.42
80.26
22.36
82.45
3.01
Table 3. Comparison of the music score generation capabilities of each method. Methods
Average matching rate (%)
Maximum matching rate (%)
Complete rate (%)
Calculation time (s)
Method 1

1.05
Method 2

1.75
Method 3

2.10
Method 4

2.60
Table 2. Comparison of music score generation effect of several methods. Fig. 10. Score recognition speed and score integrity results of several score generation methods. Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

As shown in Table 4, Method 1 demonstrates significant advantages in the recognition accuracy of various
drum components and rhythm patterns. For the identification of the three representative drum components,
namely Hanging cymbal, string sounding device and Tambourine, the accuracy rates of Method 1 reaches
93.11%, 92.46%, and 92.77%, respectively. These are significantly higher than those of other comparison
methods. In terms of rhythmic pattern recognition, the performance of Method 1 is equally stable and excellent
for both alternating rhythms, segmented rhythms and compound rhythms. Its recognition accuracy reaches
92.45%, 92.11% and 92.36%, respectively. These results fully demonstrate that the improved CNN and STFT-
based score generation method can not only efficiently and accurately recognize core drum components such as
KD, SD, and HH. Moreover, the method has strong generalization recognition ability for a wider range of drum
component types and complex rhythmic patterns. Discussion and conclusion
To assist the teaching of drum set and enhance the learning efficiency of learners, the study proposed a music
score generation method based on improved CNN and STFT. The method firstly performed the time-frequency
transformation of music signals using STFT, and then generated the drum music score through the improved
CNN model. The outcomes revealed that the improved method proposed by the study could effectively enhance
the efficiency and accuracy of the CNN model for music analysis. Specifically, after the introduction of the
enhancement strategy, the accuracy of the model reached 93.45%, while the recall reached 92.12%. Compared
with the pre-introduction strategy, its robustness was significantly improved. Second, after the introduction of
internal convolution structure, its calculation time was reduced by 0.97 s and 0.91 s compared with that before
the introduction. This indicated that the improved CNN model not only improved the processing speed, but
also optimized the accuracy and efficiency significantly. The method outperformed traditional methods in both
matching rate and complete rate, especially in real-time applications. Its matching rate and completion rate were
92% and 95%, respectively, which were significantly higher compared with other methods. Moreover, Method 1
only needed 1.05 s to realize the music score generation, which is significantly higher than other methods in real
time. This method could provide instant feedback to the drum learners in the teaching scenario and help them
master the playing skills more accurately. Current music feature extraction methods focus on frequency and
rhythm information of music signals. With the future expansion of data and changes in demand, the universality
and accuracy of music score generation need to be further improved. In future research, a more simplified and
efficient neural network architecture can be considered, and more music features and DL techniques can be
combined. The performance of the model can be further optimized. The method proposed in the research has good universality and can be extended to other music signal
processing tasks, such as piano and guitar. Its application value lies in enhancing the efficiency of music teaching
and assisting with music creation and arrangement. It also brings more efficient, intelligent solutions to the
field of music. This method is expected to be widely applied in more music fields by further optimizing the
model architecture and algorithms. This will facilitate music education and creation, promote the intelligent
development of music, and inject new vitality into the music industry. Data availability
The datasets used and/or analyzed during the current study are available from the corresponding author upon
reasonable request. Received: 28 May 2025; Accepted: 8 September 2025
References

### 1. Li, Z. et al. Hardware acceleration of MUSIC algorithm for sparse arrays and uniform linear arrays. IEEE Trans. Circuits Syst. I

Regul. Pap. 69 (7), 2941–2954 (2022).

### 2. Zhao, X., Tuo, Q., Guo, R. & Kong, T. Research on music signal processing based on a blind source separation algorithm. Annals

Emerg. Technol. Comput. 6 (4), 24–30 (2022).

### 3. George, A., Mary, X. A. & George, S. T. Development of an intelligent model for musical key Estimation using machine learning

techniques. Multimedia Tools Appl. 81 (14), 19945–19964 (2022).

### 4. Iqbal, S. N., Qureshi, A., Li, J. & Mahmood, T. On the analyses of medical images using traditional machine learning techniques

and convolutional neural networks. Arch. Comput. Methods Eng. 30 (5), 3173–3233 (2023).

### 5. Sams, A. S. & Zahra, A. Multimodal music emotion recognition in Indonesian songs based on CNN-LSTM, XLNet Transformers. Bull. Electr. Eng. Inf. 12 (1), 355–364 (2023). Method
Drum component
Rhythm mode
Hanging cymbal
String sounding device
Tambourine
Alternating rhythm
Divide the rhythm
Compound rhythm
Method 1
93.11
92.46
92.77
92.45
92.11
92.36
MusicNet
86.42
86.55
86.34
86.12
86.22
86.34
MuseScore
89.12
90.05
89.37
89.92
90.00
90.13
DeepJ
82.36
82.11
82.54
82.69
82.74
82.16
Table 4. Comparison of the recognition effects of drum components and rhythm patterns in various methods
(%). Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/

### 6. Gu, X. et al. Automatic lyric transcription and automatic music transcription from multimodal singing. ACM Trans. Multimedia

Comput. Commun. Appl. 20 (7), 1–29 (2024).

### 7. Minor, K. A. & Kartowisastro, I. H. Automatic music transcription using fourier transform for monophonic and polyphonic audio

file. Ingénierie Des. Systèmes d’Information. 27 (4), 629–635 (2022).

### 8. Liang, Y. & Pan, F. Study of automatic piano transcription algorithms based on the polyphonic properties of piano audio. IEIE

Trans. Smart Process. Comput. 12 (5), 412–418 (2023).

### 9. Ji, S., Yang, X. & Luo, J. A survey on deep learning for symbolic music generation: representations, algorithms, evaluations, and

challenges. ACM Comput. Surveys. 56 (1), 1–39 (2023).

### 10. Bhosle, K. & Musande, V. Evaluation of deep learning CNN model for recognition of devanagari digit. Artif. Intell. Appl. 1 (2),

114–118 (2023).

### 11. Qian, W., Tan, J., Jiang, Y. & Tian, Y. Deep learning with convolutional neural networks for EEG-based music emotion decoding

and visualization. Brain-Apparatus Communication: J. Bacomics. 1 (1), 38–49 (2022).

### 12. Ghatas, Y., Fayek, M. & Hadhoud, M. A hybrid deep learning approach for musical difficulty Estimation of piano symbolic music. Alexandria Eng. J. 61 (12), 10183–10196 (2022).

### 13. Shen, D. & Zhao, W. A method for improving the pronunciation quality of vocal music students based on big data technology. Int. J. Web-Based Learn. Teach. Technol. 19 (1), 1–18 (2024).

### 14. Zhang, Z. Extraction and recognition of music melody features using a deep neural network. J. VibroEng. 25 (4), 769–777 (2023).

### 15. Chalaki, M. & Omranpour, H. Epileptic seizure classification using ConvLSTM deep classifier and rotation short-time fourier

transform. J. Ambient Intell. Humaniz. Comput. 14 (4), 3809–3825 (2023).

### 16. Hudson, S. S. Bang your head: construing beat through familiar drum patterns in metal music. Music Theory Spectr. 44 (1), 121–

140 (2022).

### 17. Câmara, G. S., Sioros, G. & Danielsen, A. Mapping timing and intensity strategies in drum-kit performance of a simple back-beat

pattern. J. New. Music Res. 51 (1), 3–26 (2022).

### 18. Borodovskaya, L., Yav gildina, Z., Dyganova, E., Maykovskaya, L. & Medvedeva, I. The possibilities of artificial intelligence in

automatic musical transcription of the Tatar folk song. Rast Müzikoloji Dergisi. 10 (1), 147–161 (2022).

### 19. Hernández, R., Guerrero, A. & Macías-Díaz, J. E. A template-based algorithm by geometric means for the automatic and efficient

recognition of music chords. Evol. Intel. 17 (1), 467–481 (2024).

### 20. Zehren, M., Alunno, M. & Bientinesi, P. High-quality and reproducible automatic drum transcription from crowdsourced data. Signals 4 (4), 768–787 (2023). Author contributions
Yuting Ni wrote the main manuscript text, prepared figures, tables and equations. Yuting Ni reviewed the man­
uscript. Declarations
Competing interests
The authors declare no competing interests. Additional information
Correspondence and requests for materials should be addressed to Y. N. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:35322

| https://doi.org/10.1038/s41598-025-19348-1
www.nature.com/scientificreports/
