# The analysis of dance teaching

**Year:** D:20

---

The analysis of dance teaching
system in deep residual network
fusing gated recurrent unit based
on artificial intelligence
Mengying Li
The purpose of this study is to investigate how deep learning and other artificial intelligence (AI)
technologies can be used to enhance the intelligent level of dance instruction. The study develops
a dance action recognition and feedback model based on the Graph Attention Mechanism (GA) and
Bidirectional Gated Recurrent Unit (3D-Resnet-BigRu). In this model, time series features are captured
using BiGRU after 3D-ResNet is inserted to extract video features. Lastly, GA dynamically modifies
the node weights to maximize action recognition performance. According to the experimental results,
this model’s F1 score is 85.34%, and its maximum accuracy on the NTU-RGBD60 datasets is more than
5% greater than that of the current 3D Convolutional Neural Network (3D-CNN) baseline algorithm. In
addition, the model shows high efficiency and resource utilization in test time, training time and CPU
occupancy. The research shows that this model has strong competitiveness in dealing with complex
dance action recognition tasks, and provides efficient and personalized technical support for future
dance teaching. Meanwhile, the model provides a powerful tool for dance educators to support their
teaching activities and enhance students’ learning experience. Keywords  Dance teaching, Action recognition, Artificial intelligence, Deep learning, 3D-ResNet
Research background and motivations
Because of the special role in fostering students’ artistic accomplishment, physical coordination, and emotional
expression, dance education has become increasingly popular in the current educational system as an integral
aspect of art education1–3. However, the traditional dance teaching usually relies on teachers’ on-the-spot
guidance and demonstration. Although this method is effective in small class teaching, it is difficult to correct
and guide each student’s actions in large-scale teaching. Scholars in related domains are now concentrating on
investigating the intelligent growth of artificial intelligence (AI) technologies in the field of dance education,
such as deep learning. The extensive usage of AI technology in education in recent years has opened new avenues for innovative
educational model development. Personalized learning route recommendations and intelligent teaching
evaluation can be achieved by using the deep learning model to examine students’ learning behaviors. This
would increase the effectiveness and efficiency of teaching4–6. For example, Sun et al.7 classified images by deep
forest algorithm, which could provide reference for image recognition and dance action analysis. Deep learning
technology is primarily used in dance education to analyze and assess students’ dancing moves in real-time
using action capture and image recognition8–10. This allows for the provision of individualized feedback and
instruction. Research objectives
To address the shortcomings of the conventional teaching approach, the objective of this study is to investigate
and create a deep learning-based dance education system. In this study, the quality and personalized level of
dance teaching are improved by constructing an intelligent dance action recognition system, intelligent teaching
evaluation and personalized learning path recommendation. This study aims to enhance the effectiveness of
dance instruction while also advancing the quality and popularization of dance education by offering more
precise learning recommendations to students with varying requirements and skill levels. In terms of the
contribution to the teaching field, the system of this study provides an innovative teaching aid tool for educators
Academy of Music, Suihua University, Suihua 152000, China. email: limengyingshxy@163.com
OPEN
Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports

through deep learning technology, and provides experimental reference in enhancing the teaching effect and
meeting the needs of different students. Literature review
Review of studies on dance teaching system
The development of dance teaching system has undergone an evolution from traditional teaching, digital
teaching to intelligent teaching. Traditional dance teaching mainly relies on on-site demonstrations by teachers
and imitation by students. For example, based on the rhythm activity model of Javanese traditional dance, Mulyaningsih et al.11 aimed to enhance rhythm skills. In Kapodestria and Chatzopoulos’ research12, Greek
traditional dance programs were used to improve young children’s balance ability. Di Russo and Naranjo13
explored the case of body percussion and traditional dance in Mallorca. Engdahl et al.14 studied the content of
dance creative teaching in physical education teacher training. Although this approach could achieve teaching
objectives to some extent, there were significant limitations in terms of large-scale teaching and personalized
guidance. Digital dance education systems started to emerge along with the advancement of information technology. For instance, Yang15 examined the features and structure of a dance education system built using digital media
technology. He16 created a cloud-based, integrated online and offline teaching system for somatosensory dancing. The efficacy of an augmented reality interactive learning system in dance training courses was investigated by
Xu et al.17, with impressive findings. The use of dynamic time warping technique in image optical detection for
dance instruction was investigated by Huang and Zhu18. These systems typically give students access to video
tutorials, online courses, and other learning materials for dance. Then, the emergence of intelligent dance teaching system brings new possibilities for dance education. Pang and Niu19, for instance, achieved the recognition of dance video actions using computer vision and image
processing. In the context of the Internet of Things (IoT), Wang and Dong20 developed a dance data management
system utilizing computer-aided technologies. The particle swarm optimization technique has demonstrated
promising results in the action recognition of sports frequency pictures, according to Zhang and Hou21. Li22
enhanced the deep neural network-based folk dance training’s picture analysis and instructional approach. Review on the application of deep learning
Deep learning is a significant area of AI that has grown quickly in recent years and is now applied broadly
across numerous industries. The intelligent teaching system, personalized learning platform, and educational
data analysis are the three primary ways that deep learning technology is being applied in the field of education. For example, Bhaskaran and Marappan23 proposed an enhanced personalized recommendation system, which
realized the modeling and simulation of public datasets through deep learning technology, and achieved
remarkable results and analysis. Xiang and Guo24 used the Gaussian mixture model guided by antagonistic
learning to optimize the melody structure of automatic game soundtrack in teaching. Sun and Wu25 proposed
a systematic teaching method of emotional analysis of sports dance based on deep learning, which improved
the ability of automatic identification of dance actions and emotions. Using a deep learning model, Chen et al.26
considerably increased recommendation accuracy and learning impact by optimizing a personalized education
recommendation system using a machine learning algorithm. Jin et al.27 proposed a redundant manipulator
control scheme imitating cerebellar learning, which improved the accuracy of complex actions and the ability
to generate dance actions. Zhang et al.28 demonstrated the application potential of deep learning in education
by using it to boost ideological and political education in colleges and universities. They also improved the
educational effect through intelligent analysis. Deep learning technology has shown impressive results in action identification thanks to its strong feature
extraction and classification capabilities. To recognize and estimate inertial actions in human-computer
interaction, Yadav et al.29 used deep learning methods to identify human activities from video streaming
datasets, verifying the potential and efficiency of deep learning in processing dynamic video data. In facial
analysis and recognition, Kim et al.30 proposed an efficient facial expression recognition algorithm based on
hierarchical deep neural network, which improved the accuracy and speed of real-time recognition. Putro et
al.31 developed a real-time facial expression detector based on sequential attention network, which improved the
ability of facial expression analysis with low delay. Jiang et al.32 improved the efficiency and accuracy of facial
expression recognition by expressing the method of strengthening network and self-training migration. Jiang et
al.33 proposed a binary network based on hierarchical consistency quantization and information refinement, and
improved the efficiency of facial expression recognition in human-computer interaction. Personalized recommendations, teaching feedback, and the identification and assessment of dance actions
are the primary ways that deep learning is applied in dance education. For instance, Xiang et al.34 proposed
an adaptive hierarchical action and structure optimization framework, which improved the naturalness of
robot actions and dance coordination. Zhu et al.35 effectively improved the effectiveness of dance teaching by
combining music and deep learning technology in the flipped classroom model of physical education. Wang36
studied the application of AI in dance education, and found that using immersive technology to teach dance
skills could significantly improve teaching efficiency and students’ skill mastery level. Jiang and Yan37 used
deep learning frameworks to achieve coherent generation of actions, improving the intelligence and accuracy
of dance teaching. Ji and Tian38 proposed a dance action recognition model based on the IoT and deep learning
framework, which effectively improved the accuracy and real-time performance of dance action recognition and
promoted the development of intelligent dance teaching. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

Research blank and innovation of this study
There are still certain research gaps and opportunities for development despite certain advancements in deep
learning applications and dance teaching systems. Firstly, the current intelligent dance teaching system still
has a lot of space for development in terms of accuracy and real-time performance, particularly when it comes
to complex moves and multiple students practicing at once. Furthermore, the current system’s personalized
recommendation and teaching feedback features are not flawless, making it challenging to completely satisfy
each student’s unique individualized learning needs. Given the research gaps, this study’s innovation is to create
a deep learning-based, high-precision dance action recognition model. By refining the network structure and
training algorithm, the study also aims to enhance the accuracy and real-time performance of complex action
recognition. Students’ dancing actions are then recorded and evaluated in real time based on the deep learning
model’s analysis results, and the system offers tailored learning programs, personalized instructional feedback,
and increased learning efficacy and efficiency. Lastly, there is a promotion of the intelligent and digital evolution
of dance education. Research model
Intelligent collection and analysis of dance actions
In the intelligent dance teaching system, accurately capturing and analyzing students’ dance actions is the basis
of realizing personalized teaching feedback. To achieve this goal, this study adopts the action analysis method of
human 3D skeleton. This method captures the dancer’s action data in real time through sensors and cameras, and
generates the corresponding 3D skeleton model, thus providing data support for subsequent action recognition
and analysis. The dancer in this study has many sensors installed on them to record action data of different body areas,
including joint angle and action trajectory, ensuring data integrity and accuracy. These sensors transmit data
to the data processing center in real time through wireless transmission technology. Meanwhile, several high-
precision cameras are arranged in the dance classroom to capture the actions of dancers from different angles. The human skeleton data all contain spatial 3D coordinates, and each frame contains 25 skeleton nodes39. In dance teaching, gestures and actions are represented by 3D skeleton data. Compared with RGB images, the
3D skeleton model can fully reflect the details of dancers’ actions, which is helpful to improve the accuracy of
action recognition. In addition, through 3D skeleton modeling, multi-dimensional analysis of dance actions can
be realized, which provides scientific basis for personalized teaching feedback and improvement suggestions. Analysis of dance action recognition and feedback model construction based on attention
mechanism of 3D-ResNet-BiGRU fusion diagram
In Fig. 1, this study creates a dance action recognition and feedback model based on 3D-ResNet-BiGRU and
integrating graph attention mechanism (GA)40 to increase the accuracy and real-time performance of dance
action recognition. The model can precisely recognize and evaluate intricate dancing moves and offer tailored
educational feedback by refining the network topology and training methodology. In Fig. 1, the input layer of the model receives the 3D skeleton action sequence as input data, which are
collected by sensors and cameras, and are desensitized, clipped and normalized to ensure the consistency of the
model in processing the input data. Then the 3D-ResNet model41,42 is used to extract the features of the video
sequence. In this model, X = (x1, x2, · · ·, xT ) = {xi}T
i=1 refers to a dance video image with T frames. It is divided
into a sequence V N of N dance video segments by a sliding window, as shown in Eq. (1): V N = (v1, v2, · · ·, vN)
(1)
Input each video segment vi into 3D-ResNet and extract its corresponding fixed-length video feature expression
fi ∈Rd. The input sequence can be expressed as Eq. (2): F N = (f1, f2, · · ·, fN) = {Φθ (vi)}N
i=1
(2)
Φθ (·) refers to 3D-resnet, and θ refers to network parameters. To capture the action information V xyz
ij
in multiple consecutive frames in dance teaching video images, this
study introduces a bidirectional gated recurrent unit (BiGRU) after the 3D-ResNet network43. As an efficient
recurrent neural network variant, BiGRU has a simpler structure compared with LSTM, which can reduce the
number of model parameters, thus reducing the training difficulty and computing resource consumption. In
addition, BiGRU is particularly good at capturing short-term dependencies in dance actions, which is very
important for identifying accurate dance actions. Because dance actions often involve rapid and continuous limb
actions, BiGRU’s bidirectional characteristics enable it to consider both past and future contextual information,
which is particularly important for understanding and predicting the dynamic changes of complex dance
actions. Compared with LSTM, BiGRU can provide faster training speed and better performance when dealing
with such data with strong time correlation. Therefore, considering the special requirements and computational
efficiency of dance action recognition, BiGRU has become a more suitable choice in this study. In the BiGRU
layer, the update gate zi is used to describe the degree to which the vector of dance video image data is brought
into the current state from the state of the previous moment i. The threshold and capture ability obtained by the
reset gate ri are opposite to those of the update gate. The states of zi and ri are shown in Eqs. (3) and (4):
zi = σ (Mxzei + Mhzhi−1 + cz)
(3)
Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

ri = σ (Mxrei + Mhrhi−1 + cr)
(4)
Among them, σ refers to sigmoid loss function, which is responsible for the control signals between different
gates. Mxz, Mhz, Mxr, Mhr refer to the parameters constructed by autonomous learning in GRU unit. For
parameter hi−1, it refers to the last output vector during the execution of step i−1. zi and ri refer to the vectors
obtained by updating the gate and resetting the gate respectively. The reset signal hi−1 is represented by hi−1
′,
as shown in Eq. (5). The signal spliced with the input vector signal xi is represented by ˜hi, as shown in Eq. (6): Fig. 1. Schematic diagram of dance action recognition and feedback model based on 3DResNet-BiGRU-GA. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

hi−1
′ = hi−1 ⊙ri
(5)
˜hi = tanh (M · [hi, xi])
(6)
The vector data is scaled to the interval [1,1] under the operation of tanh activation function, and the specific
operation of this GRU model for ˜hi is shown in Eq. (7):
˜hi = tanh (
Mxz/xr · ei + riMhz/hrhi−1 + cz/r
)

(7)
Then the information processing result of step l in the unit hi:
hi = (1 −zi) ˜hi + zihi−1
(8)
Finally, the features are encoded by the gating cycle unit. To capture more abundant long-distance dependencies
between features, the positive and negative vectors of the features can be encoded by GRU, which are expressed
as Eqs. (9) and (10):
⃗gi = −−−→
GRU
(−−→
hi−1, ei
)

(9)
←g i = ←−−−
GRU
(←−−
hi−1, ei
)

(10)
The two-way coded feature vector can be expressed as ei =
[
⃗gi,
←g i
], and the corresponding feature is also used
as the input of the attention mechanism layer of the next layer of graph. This study introduces the GA in 3D-ResNet and BiGRU networks to further enhance the model’s recognition
capabilities. Firstly, the 3D skeleton model is represented as a graph structure, in which skeleton points are nodes
and joint connections are edges. Then, using GA, the weight of each node is dynamically adjusted to highlight
the action characteristics of key parts. The core of GA is to calculate the correlation between nodes through Self-
Attention Mechanism. The value is normalized by the Softmax function, as shown in Eq. (11): Fig. 2. The pseudo-code flow chart of 3DResNet-BiGRU-GA algorithm applied to dance action recognition
and feedback. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

α(t,i)→(t,j) =
exp (
u(t,i)→(t,j)
)
N∑
u=1
exp (
u(t,i)→(t,n)
)
(11)
α refers to the normalized similarity of the inner product u. Therefore, the introduction of graph attention
module can effectively learn the weights of any two body joint points in different actions, and this data-driven
way increases the universality of the model. The technology can record and analyze students’ dancing actions in real time and deliver tailored educational
feedback based on the deep learning model’s analysis results. In the model constructed in this study, the specific
pseudo-code is shown in Fig. 2. In order to clearly show the pseudo-code of this model, the specific process is shown in Fig. 3. In Fig. 3, the flow chart describes in detail the workflow of the 3DResNet-BiGRU-GA algorithm in the dance
action recognition and feedback system. Firstly, the system receives the 3D skeleton action sequence in dance
video pictures collected by sensors and cameras as input data. Subsequently, these data go through preprocessing
steps, including desensitization, editing and normalization, to ensure the consistency of the data and the effective
processing of the model. The pre-processed data is sent to 3D-ResNet model for feature extraction, which can
capture the key visual features in the video sequence. Next, BiGRU layer intervenes, using the characteristics
of its BiGRU to capture the time series characteristics of dance actions, thus identifying the continuity and
complexity of the actions. After the BiGRU layer, the graph attention (GA) mechanism layer is further analyzed
and adjusted, and the action characteristics of key parts in the dance are highlighted by dynamically adjusting
the node weights, thus enhancing the recognition ability of the model. Finally, the system outputs the recognition
results and feedback of dance actions, providing personalized technical support for dance teaching. Experimental design and performance evaluation
Datasets collection
To analyze the performance of the constructed model, the data source comes from the self-built data set and
NTU-RGBD60 database (https://rose1.ntu.edu.sg/dataset/actionRecognition/). The self-built dataset uses
Kinect for Windows SDK and Kinect V2 to develop an action acquisition software to capture and record the
dancer’s dance action data and collect skeleton information. In the process of data collection of dance actions,
a total of 85 experiments are carried out, 3 times for each action, and finally a self-built dance action dataset
containing 1549 samples is constructed. NTU-RGBD60 database collects and labels skeleton nodes through Microsoft Kinect v2 sensor. This database
is a high-quality database, with 60 human action classes and 56,000 human action fragments. In this paper, the
skeleton sequence data of moving images in the database are pre-processed, as shown in Table 1, and finally 2531
action samples are selected. It is divided into training dataset (70%) and test dataset (30%), and the proportion
of each type of action data in the two datasets is guaranteed to be consistent. Experimental environment
This study is conducted in a high-performance computing environment. Hardware configuration includes
NVIDIA Tesla V100 32GB GPU, Intel Xeon E5-2698 v4 @ 2.20 GHz CPU, 256GB RAM and 2 TB SSD. In terms
of software, Windows 10 operating system is adopted, and PyTorch 1.8.1 is used as the deep learning framework. Python version is 3.8.5, CUDA version is 11.2, and cuDNN version is 8.1.1. The development tools mainly use
Jupyter Notebook, Git and Visual Studio Code. These configurations ensure the efficiency and stability of the
model training and evaluation process. Parameters setting
A series of optimized hyperparameters is used in the experiment to optimize the model performance and
training efficiency. The specific super parameter settings are shown in Table 2. In the training process, Adaptive Moment Estimation (Adam) optimization algorithm is used to optimize the
parameters of the network model. The training times of the model are 80 times, the batch size is set to 32, and
the initial learning rate is 0.001. The loss function adopts Cross-Entropy Loss function, and the optimization
algorithm uses Adam optimizer to update the parameters, control the learning rate and momentum, and
accelerate the convergence speed. Performance evaluation
To evaluate the performance of the model constructed in this study, the proposed model algorithm is compared
with the model algorithm proposed by 3D CNN44, 3D-ResNet, ResNet45 and Ji & Tian (2024) in the self-built
dataset and NTU-RGBD60 dataset respectively. Among them, 3D CNN, as a basic deep learning model, extracts
feature by applying convolution operation in the space-time dimension, which is suitable for the processing of
video and image sequences. But it still needs to be explored in dealing with complex dance action sequences. The
3D-ResNet model enhances the training effect of deep network by introducing residual learning mechanism,
especially in extracting deep features and improving recognition accuracy. ResNet, as a classic model in the field
of image recognition, solves the problem of gradient disappearance in deep network training through residual
connection. Although it was originally designed for static images, its application in video processing also shows
certain potential. The model of Ji & Tian (2024) represents the latest research progress and may integrate
specific technological innovations. The selection of these baseline models not only provides a benchmark for the
performance comparison of the new models, but also shows the application potential and limitations of different
algorithms in the field of dance action recognition. Through these comparisons, people can deeply understand
Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

the advantages of 3DResNet-BiGRU-GA model in accuracy, efficiency and resource utilization, and its potential
application value in the intelligent development of dance teaching system. The accuracy and F1 value are evaluated, as shown in Figs. 4, 5, 6 and 7. In Figs. 4 and 5, comparing the performance of this model algorithm with other algorithms (including
Ji & Tian (2024), 3D-ResNet, ResNet and 3D CNN) on self-built datasets, it shows that with the increase of
iteration times, the accuracy and F1 of each algorithm show a trend of increasing first and then stabilizing. In
the comparison of accuracy, the accuracy of 3DResNet-BiGRU-GA is improved from 66.06 to 96.06%, which
Fig. 3. Flow chart of dance action recognition and feedback model. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

is significantly higher than other models. In addition, the F1 score also shows that 3DResNet-BiGRU-GA has
increased from 51.32 to 90.62%, which is also superior. In contrast, the accuracy and F1 scores of Ji & Tian,
3D-ResNet, ResNet and 3D CNN are all low, which proves that 3DResNet-BiGRU-GA has higher accuracy and
robustness in dance action recognition tasks. Fig. 4. The dance action recognition Accuracy chart of different algorithms in self-built dataset. Module
Parameter
Value
3D-ResNet
Number of convolution layers
5 layers
Convolution kernel size
3 × 3 × 3
Number of residual modules

Activation function
ReLU
Batch normalization
After each convolution layer
BiGRU
Input dimension

Hidden layer dimension

Number of plies
2 layers
Bidirectional coding
Yes
GA
Input feature dimension

Output feature dimension

Table 2. Configuration of experimental environment. Number of step
Pretreatment step
Description

Data cleaning
Remove abnormal values and noises, and
eliminate incomplete or low-quality dance action samples

Normalize
Normalize the 3D skeleton data to eliminate the
differences in body shape and action range among dancers

Data enhancement
Through geometric transformation and time series
data enhancement technology, the diversity of datasets is increased

Editing and segmentation
The continuous dance action sequence is cut into fixed-length
fragments, which are segmented by sliding window method

Data annotation
Ensure that each data segment has the correct action
tag, and carry out necessary cleaning and verification

Data segmentation
The dataset is randomly divided into training set and
test set to ensure the uniform distribution of samples
Table 1. Data preprocessing step. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

In Figs. 6 and 7, further evaluating the performance of each algorithm on NTU-RGBD60 dataset, it shows
that the accuracy of each algorithm increases with the number of iterations, and F1 shows a trend of first
increasing and then stabilizing, which is consistent with the trend in self-built dataset. Meanwhile, the accuracy
of 3DResNet-BiGRU-GA increase from 63.20 to 95.34%, which is significantly higher than other models, and
Fig. 6. The dance action recognition Accuracy diagram of different algorithms in NTU-RGBD60 dataset. Fig. 5. F1 diagram of dance action recognition with different algorithms in self-built dataset. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

increases by 5%. Ji & Tian’s model has increased from 52.13 to 90.68%, while the performances of 3D-ResNet, ResNet and 3D CNN are relatively low, reaching the highest of 86.40%, 77.50% and 70.68% respectively. The
F1 score in Fig. 6 further verifies this trend. The F1 score of 3DResNet-BiGRU-GA has increased from 57.84
to 85.34%, which is also superior. In order to further verify the performance advantages of 3DResNet-BiGRU-
GA model compared with other baseline models, a statistical significance test is conducted by using t- test to
compare the accuracy and F1 scores of different algorithms on NTU-RGBD60 dataset, as shown in Table 3. In Table  3, through t- test, 3DResNet-BiGRU-GA model shows statistically significant differences in
accuracy and F1 score compared with other baseline models. Specifically, compared with 3D CNN, 3D-ResNet
and ResNet models, the p-value of 3DReSNet-BiGRU-GA model is less than 0.01, which indicates that its
performance improvement is extremely significant. Compared with the model algorithm proposed by Ji & Tian
(2024), although the performance is slightly improved, the p-value is still less than 0.05, which indicates that the
performance advantage of 3DResNet-BiGRU-GA model is statistically significant. These results further verify
the superiority and reliability of the model in dance action recognition tasks. Furthermore, the calculation efficiency of each model is compared, including training time, prediction time
and CPU occupancy, as shown in Table 4; Fig. 8. This study also compares the performance of different algorithms in terms of test time, training time and
CPU utilization, as shown in Table 4; Fig. 8. It shows that the test time of 3DResNet-BiGRU-GA is 71.02 s,
the training time is 76.40 s, and the CPU utilization rate is 40.50%, which is the best among all models. Ji &
Tian’s model test time is 77.90 s, training time is 91.94 s, and CPU utilization rate is 43.64%, followed by. The
test time of 3D-ResNet is 88.06 s, the training time is 105.40 s, and the CPU utilization rate is 50.72%. The
Model comparison
Accuracy difference (p-value)
F1 score difference (p-value)
3DResNet-BiGRU-GA vs. 3D CNN
0.003
0.005
3DResNet-BiGRU-GA vs. 3D-ResNet
0.007
0.004
3DResNet-BiGRU-GA vs. ResNet
0.002
0.007
3DResNet-BiGRU-GA vs. Ji & Tian (2024)
0.02
0.04
Table 3. Comparison of calculation efficiency of each model algorithm. Fig. 7. Dance action recognition F1 diagram of different algorithms in NTU-RGBD60 dataset. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

performances of ResNet and 3D CNN are poor. The test time of ResNet is 104.50 s, the training time is 109.28 s,
and the CPU utilization rate is 58.64%, while that of 3D CNN is 109.28 s, the training time is 112.87 s, and the
CPU utilization rate is 63.52%. These results show that the proposed 3DResNet-BiGRU-GA algorithm also has
significant advantages in efficiency and resource utilization. Discussion
The proposed 3DResNet-BiGRU-GA model shows significant advantages in the task of dance action recognition. The accuracy of this model on NTU-RGBD60 dataset is 95.34%, and the F1 score is 85.34%, which significantly
exceeds the algorithms such as Ji & Tian, 3D-ResNet, ResNet and 3D CNN. The model not only performs well in
accuracy and F1 score, but also shows higher efficiency in test time, training time and CPU utilization. Compared
with the research of Vrskova et al.46, Tu et al.47, and Song et al.48, 3DResNet BiGRU GA has made breakthroughs
in method innovation and practical applications, providing effective technical support for the intelligent
development of dance teaching systems and having broad application prospects and practical significance. This study serves as a valuable source of inspiration for the thoughtful creation of dance education systems. By introducing a dance action recognition model based on 3D-ResNet-BiGRU and integrating GA, people can
Fig. 8. Comparison of calculation efficiency of each model algorithm. Algorithm type
Testing time
Training time
CPU occupancy rate
3DResNet-BiGRU-GA
71.02
76.40
40.50
Ji & Tian
77.90
91.94
43.64
3D-ResNet
88.06
105.40
50.72
ResNet
104.50
109.28
58.64

## 3D CNN

109.28
112.87
63.52
Table 4. Comparison of calculation efficiency of each model algorithm. Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

not only accurately identify complex dance actions, but also capture students’ action performance in real time
and provide personalized feedback. Therefore, it provides a practical technical scheme for the intellectualization
of dance teaching system and promotes the modernization process of dance education. In terms of feasibility, although the proposed intelligent dance teaching system based on 3D-ResNet-
BiGRU and GA mechanism is technically advanced, its feasibility and practicability must be considered when
implementing the system in an educational environment with limited resources. For an environment with limited
resources, cost-effectiveness and ease of use are key factors. Therefore, while maintaining high performance,
the designed system also pays attention to reducing hardware requirements and operational complexity. For
example, the system can be optimized to run on lower-cost hardware, such as using integrated graphics cards
or cloud services to handle compute-intensive tasks. In addition, the user interface and operation flow of the
system can be designed to be intuitive and easy to use to reduce the dependence on professional and technical
personnel. Online tutorials and remote technical support can also be provided to help teachers and students
quickly master the use of the system. Through these measures, even in the case of limited budget and resources,
the system can be effectively integrated into the educational environment to provide innovative support for
dance teaching. In addition, although the proposed 3DResNet-BiGRU-GA model performs well in the task of dance action
recognition, there are still some limitations that deserve further discussion. First, the interpretability of the
model is a challenge. Although deep learning models have made remarkable progress in recognition accuracy,
they are usually regarded as “black boxes” and it is difficult to explain their decision-making process intuitively. This is especially important for dance education, because teachers and students may need to understand why
the model makes specific action recognition and feedback. Secondly, the possible deviation in the dataset may
also affect the generalization ability of the model. Because the dataset mainly comes from a specific group of
dancers, it may not cover all the diversity of dance styles and actions, which leads to the performance decline of
the model in the face of new and unprecedented dance actions. In addition, the recording deviation that may
exist in the process of data collection, such as the inconsistency of sensor placement or the change of recording
environment, may also affect the accuracy and robustness of the model. Future work could further explore ways
to improve the interpretability of the model, and consider reducing potential data bias through multi-source
data fusion and enhancing data diversity to improve the applicability and effectiveness of the model in a wider
range of scenarios. Conclusion
Research contribution
In this study, a dance action recognition and feedback model based on 3D-ResNet-BiGRU and integrating GA
is proposed, which significantly improves the accuracy and efficiency of dance action recognition. By combining
3D-ResNet feature extraction with BiGRU to capture time series features, and dynamically adjusting node
weights by using GA, the accuracy of our model on NTU-RGBD60 dataset reaches 95.34%, and the F1 score is
85.34%. The model is not only superior to the existing comparison algorithms in recognition accuracy, but also
shows higher efficiency in test time, training time and CPU utilization. The research results show that the model
has strong competitiveness in dealing with complex dance actions, which promotes the intelligent development
of dance teaching system and provides strong technical support for future dance teaching and training. Future works and research limitations
This study does still have certain shortcomings, though, and there are still areas for improvement. First, the
model is trained and tested on a particular dataset, which can later be expanded to bigger and more varied
datasets to confirm the model’s robustness and universality. Secondly, there is still room for improvement in
the model’s real-time feedback performance, particularly about response speed and system stability in large-
scale practical applications. In addition, more types of deep learning models and algorithm optimization can be
explored in future work to further improve the recognition accuracy and efficiency. Meanwhile, expanding the
application scope of the model by combining more data sources of human posture and action will help promote
the application of this technology in different dance styles and scenes. Data availability
The datasets used and/or analyzed during the current study are available from the corresponding author Meng­
ying Li on reasonable request via e-mail limengyingshxy@163.com. Received: 4 November 2024; Accepted: 2 January 2025
References

### 1. Zhang, Y. et al. High-precision detection for sandalwood trees via improved YOLOv5s and StyleGAN. Agriculture 14(3), 452

(2024).

### 2. Li, N. & Boers, S. Human motion recognition in dance video images based on attitude estimation. Wirel. Commun. Mob. Comput.

2023(1), 4687465 (2023).

### 3. Tomescu, G., Stănescu, M. I. & Aivaz, K. A. The contribution of dance to Optimizing Motor skills and improving the Educational

process in Institutionalized Children. BRAIN Broad Res. Artif. Intell. Neurosci. 15(2), 362–377 (2024).

### 4. Cob-Parro, A. C., Losada-Gutiérrez, C., Marrón-Romera, M., Gardel-Vicente, A. & Bravo-Muñoz, I. A new framework for deep

learning video based Human Action Recognition on the edge. Expert Syst. Appl. 238, 122220 (2024).

### 5. Suglia, V. et al. A novel framework based on deep learning architecture for continuous human activity recognition with inertial

sensors. Sensors 24(7), 2199 (2024). Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

### 6. Hung, N. V. et al. Building an online learning model through a dance recognition video based on deep learning. Информатика и

автоматизация 23(1), 101–128 (2024).

### 7. Sun, L. et al. Adaptive feature selection guided deep forest for covid-19 classification with chest ct. IEEE J. Biomed. Health Inf.

24(10), 2798–2805 (2020).

### 8. Zhang, Y. Application of knowledge model in dance teaching based on wearable device based on deep learning. Mob. Inform. Syst.

2022(1), 3299592 (2022).

### 9. Zhao, P., Lu, C. X., Wang, B., Trigoni, N. & Markham, A. Cubelearn: end-to-end learning for human motion recognition from raw

mmwave radar signals. IEEE Internet Things J. 10(12), 10236–10249 (2023).

### 10. Wang, F., Quiles, O. L. & Li, J. Music-driven generative dance movement teaching game based on a multi-feature fusion strategy. Entertainment Comput. 50, 100646 (2024).

### 11. Mulyaningsih, F., Suherman, W. S., Sukoco, P. & Susanto, E. A rhythmic activity learning Model based on Javanese Traditional

Dance to improve rhythmic skills. Int. J. Hum. Mov. Sports Sci. 10(3), 501–509 (2022).

### 12. Kapodistria, L. & Chatzopoulos, D. A Greek traditional dance program for improving balance of young children. Res. Dance Educ.

23(3), 360–372 (2022).

### 13. Di Russo, S. & J. R. Naranjo, F. Body percussion and traditional dances: the case of ball dels moretons in Mallorca. Retos: Nuevas

Tenden. Educ. Física Deporte Recreac. 49, 442–458 (2023).

### 14. Engdahl, C., Lundvall, S. & Barker, D. Free but not free-free’: teaching creative aspects of dance in physical education teacher

education. Phys. Educ. Sport Pedagogy 28(6), 617–629 (2023).

### 15. Yang, X. Analysis of the construction of dance teaching system based on digital media technology. J. Interconnect. Netw. 22(Supp05),

2147021 (2022).

### 16. He, Y. Design of online and offline integration teaching system for body sense dance based on cloud computing. J. Interconnect. Netw. 22(Supp05), 2147001 (2022).

### 17. Xu, W., Xing, Q. W., Zhu, J. D., Liu, X. & Jin, P. N. Effectiveness of an extended-reality interactive learning system in a dance

training course. Educ. Inform. Technol. 28(12), 16637–16667 (2023).

### 18. Huang, H. & Zhu, H. Application of image optical detection based on dynamic time warping algorithm in dance teaching. Opt. Quant. Electron. 56(3), 287 (2024).

### 19. Pang, Y. & Niu, Y. Dance video motion recognition based on computer vision and image processing. Appl. Artif. Intell. 37(1),

2226962 (2023).

### 20. Wang, Z. & Dong, J. Design of dance data management system based on computer-aided technology under the background of

internet of things. Comput. Aided Des. Appl. 20(S2), 45–55 (2023).

### 21. Zhang, Y. & Hou, X. Application of video image processing in sports action recognition based on particle swarm optimization

algorithm. Prev. Med. 173, 107592 (2023).

### 22. Li, Z. Image analysis and teaching strategy optimization of folk dance training based on the deep neural network. Sci. Rep. 14(1),

10909 (2024).

### 23. Bhaskaran, S. & Marappan, R. Enhanced personalized recommendation system for machine learning public datasets: generalized

modeling, simulation, significant results and analysis. Int. J. Inform. Technol. 15(3), 1583–1595 (2023).

### 24. Xiang, Z. & Guo, Y. Controlling melody structures in automatic game soundtrack compositions with adversarial learning guided

gaussian mixture models. IEEE Trans. Games 13(2), 193–204 (2020).

### 25. Sun, Q. & Wu, X. A deep learning-based approach for emotional analysis of sports dance. PeerJ Comput. Sci. 9, e1441 (2023).

### 26. Chen, W., Shen, Z., Pan, Y., Tan, K. & Wang, C. Applying machine learning algorithm to optimize Personalized Education

Recommendation System. J. Theory Pract. Eng. Sci. 4(01), 101–108 (2024).

### 27. Jin, L., Huang, R., Liu, M. & Ma, X. Cerebellum-inspired learning and control scheme for redundant manipulators at joint velocity

level. IEEE Trans. Cybern. 54(11), 6297–6306 (2024).

### 28. Zhang, Y., Yan, Y., Kumar, R. L. & Juneja, S. Improving college ideological and political education based on deep learning. Int. J. Inf. Commun. Technol. 24(4), 431–447 (2024).

### 29. Yadav, R. K., Arockiam, D. & Bhaskar Semwal, V. Motion signal-based recognition of human activity from video stream dataset

using deep learning approach. Recent. Adv. Comput. Sci. Commun. 17(3), 77–91 (2024).

### 30. Kim, J. H., Kim, B. G., Roy, P. P. & Jeong, D. M. Efficient facial expression recognition algorithm based on hierarchical deep neural

network structure. IEEE Access. 7, 41273–41285 (2019).

### 31. Putro, M. D., Nguyen, D. L. & Jo, K. H. A fast CPU real-time facial expression detector using sequential attention network for

human–robot interaction. IEEE Trans. Industr. Inf. 18(11), 7665–7674 (2022).

### 32. Jiang, C. S., Liu, Z. T., Wu, M., She, J. & Cao, W. H. Efficient facial expression recognition with representation reinforcement

network and transfer self-training for human–machine interaction. IEEE Trans. Industr. Inf. 19(9), 9943–9952 (2023).

### 33. Jiang, C. S., Liu, Z. T. & She, J. Hierarchical co-consistency quantization and information refining binary network for facial

expression recognition in human–robot interaction. IEEE Trans. Industr. Inf. 20(10), 12178–12188 (2024).

### 34. Xiang, Z., Xiang, C., Li, T. & Guo, Y. A self-adapting hierarchical actions and structures joint optimization framework for automatic

design of robotic and animation skeletons. Soft. Comput. 25(1), 263–276 (2021).

### 35. Zhu, Z., Xu, Z. & Liu, J. Flipped classroom supported by music combined with deep learning applied in physical education. Appl. Soft Comput. 137, 110039 (2023).

### 36. Wang, Z. Artificial intelligence in dance education: using immersive technologies for teaching dance skills. Technol. Soc. 77, 102579

(2024).

### 37. Jiang, H. & Yan, Y. Sensor based dance coherent action generation model using deep learning framework. Scalable Comput. Pract. Exp. 25(2), 1073–1090 (2024).

### 38. Ji, Z. & Tian, Y. IoT based dance movement recognition model based on deep learning framework. Scalable Comput. Pract. Exp.

25(2), 1091–1106 (2024).

### 39. Lovanshi, M. & Tiwari, V. Human skeleton pose and spatio-temporal feature-based activity recognition using ST-GCN. Multimedia

Tools Appl. 83(5), 12705–12730 (2024).

### 40. Wei, Y., Wu, D. & Terpenny, J. Bearing remaining useful life prediction using self-adaptive graph convolutional networks with self-

attention mechanism. Mech. Syst. Signal Process. 188, 110010 (2023).

### 41. Yang, M., Huang, X., Huang, L. & Cai, G. Diagnosis of Parkinson’s disease based on 3D ResNet: the frontal lobe is crucial. Biomed. Signal Process. Control 85, 104904 (2023).

### 42. He, R., Xiao, Y., Lu, X., Zhang, S. & Liu, Y. ST-3DGMR: Spatio-temporal 3D grouped multiscale ResNet network for region-based

urban traffic flow prediction. Inf. Sci. 624, 68–93 (2023).

### 43. Lalwani, P. & Ramasamy, G. Human activity recognition using a multi-branched CNN-BiLSTM-BiGRU model. Appl. Soft Comput.

154, 111344 (2024).

### 44. Wang, Y. et al. E3D: an efficient 3D CNN for the recognition of dairy cow’s basic motion behavior. Comput. Electron. Agric. 205,

107607 (2023).

### 45. Zhang, J. et al. SOR-TC: self-attentive octave ResNet with temporal consistency for compressed video action recognition. Neurocomputing 533, 191–205 (2023).

### 46. Vrskova, R., Kamencay, P., Hudec, R. & Sykora, P. A new deep-learning method for human activity recognition. Sensors 23(5), 2816

(2023). Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/

### 47. Tu, Z., Liu, Y., Zhang, Y., Mu, Q. & Yuan, J. DTCM: joint optimization of dark enhancement and action recognition in videos. IEEE

Trans. Image Process. 32, 3507–3520 (2023).

### 48. Song, B., Yoshida, S. & Alzheimer’s Disease Neuroimaging Initiative. Explainability of three-dimensional convolutional neural

networks for functional magnetic resonance imaging of Alzheimer’s disease classification based on gradient-weighted class
activation mapping. Plos One 19(5), e0303278 (2024). Author contributions
Mengying Li: Conceptualization, methodology, software, validation, formal analysis, investigation, resources,
data curation, writing—original draft preparation, writing—review and editing, visualization, supervision, pro­
ject administration, funding acquisition. Funding
This work was supported by following fundings:

### 1. Heilongjiang Province Philosophy and Social Science Planning Project, Project number: 21YSC234.

### 2. Heilongjiang Provincial Art and Science Planning Project, Project number: 2024D057.

### 3. Heilongjiang Provincial Education and Science Planning Key Issues, Project number: GLB1424231.

### 4. Heilongjiang University Students Innovation and Entrepreneurship Project, Project number: S202410236045.

### 5. Heilongjiang University Students Innovation and Entrepreneurship Project, Project number: S202410236063S.

### 6. Heilongjiang Provincial Art and Science Planning Project, Project number: 2023D035. Competing interests
The authors declare no competing interests. Ethics statement
The studies involving human participants were reviewed and approved by Academy of Music, Suihua
University Ethics Committee (Approval Number: 2022.54510023). The participants provided their written
informed consent to participate in this study. All methods were performed in accordance with relevant
guidelines and regulations. Additional information
Correspondence and requests for materials should be addressed to M. L. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:1305

| https://doi.org/10.1038/s41598-025-85407-2
www.nature.com/scientificreports/
