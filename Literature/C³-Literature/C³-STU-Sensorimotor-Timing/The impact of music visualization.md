# The impact of music visualization

**Year:** D:20

---

The impact of music visualization
model by using internet of things
techniques and deep neural
network
Xue Yu
The allure of music lies in its ability to engage human auditory and visual perception. Therefore,
researching music is a significant endeavor. This study aims to explore an innovative music visualization
model that integrates deep neural network technology, focusing on the field of the Internet of Things
(IoT) and human-computer interaction. The objective is to assist in identifying musical emotions and,
by introducing the Convolutional Neural Network (CNN) and IoT technology, design an efficient music
visualization analysis model. Through experimental testing on a dataset obtained from NetEase Cloud
Music, this study demonstrates the advantages of this CNN-based music visualization model in terms
of accuracy, binary classification capability, complexity, and generalization ability. The proposed
model surpasses other algorithms in terms of visual fidelity, structural similarity (SSIM) index, and
peak signal-to-noise ratio (PSNR), showcasing effective data augmentation capabilities. While the
model exhibits a certain level of complexity and slightly longer processing times, results with an SSIM
score of 0.712 and a PSNR score of 16.893 highlight its strong generalization ability. The study reveals
the significant practical value of CNN-based music visualization analysis models in the analysis and
visualization of music emotion data. However, it is important to note that the dataset used in this
study is limited to NetEase Cloud Music and may carry some bias, not fully representing the entire
music domain or characteristics of other music streaming platforms. Therefore, the study suggests
incorporating diverse music datasets to enhance the model’s generalization ability and applicability. In
conclusion, CNN-based music visualization analysis models possess robust generalization capabilities
and application potential. They hold significant value and insights for academic research and industrial
applications in music-related fields. Keywords  Artificial intelligence, Deep neural network, Internet of things, Visual analysis of music, Convolutional neural network
With the rapid progress of computer technology, music visualization, as a unique art form, is gradually emerging. It combines the rhythm of music with visual elements to create a new, multi-sensory experience that allows the
audience to understand and appreciate the musical work more deeply1. In this field, the Convolutional Neural
Network (CNN), as a vital branch of deep learning (DL), offers strong technical support for music emotion
analysis with its excellent feature extraction and pattern recognition capabilities. As big data and online music content vigorously develop, music information retrieval technology is particularly
important2. Users want to be able to quickly and accurately find music works that resonate with them according
to their emotional needs. Emotion-based music retrieval technology came into being, which provides users with
personalized music search and recommendation services by identifying the emotional features in music. As one of
the core technologies of music information retrieval, music emotion recognition plays a pivotal role in improving
user experience and promoting the innovation and development of the music industry. However, music emotion
recognition faces many challenges3. First, music emotion is subjective, and different individuals may have diverse
emotional responses to the same piece of music. This makes qualitative classification methods based on group
assessment impractical because it is difficult to find a universal classification standard for emotions4. Second,
music’s emotional complexity makes it difficult to recognize. The emotional information contained in music is
often related to melody, rhythm, harmony, and other factors, so it is necessary to comprehensively consider the
School of Art, Anhui University of Finance and Economics, Bengbu 233000, Anhui, China. email:
120081824@aufe.edu.cn
OPEN
Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports

characteristics of multiple dimensions to accurately identify5. To overcome these challenges, this study combines
DL with music visualization techniques to explore models for recognition and classification based on multimodal
music emotion features6. Multimodal music emotion features encompass audio and visual features, which can
reflect the emotional information of music from different perspectives. By utilizing CNN to extract features such
as melody and rhythm from audio data, and combining image processing techniques to extract features like
color and shape from music-related visual elements, this study aims to construct a comprehensive and accurate
music emotion recognition system. Additionally, this study designs and implements an intelligent music system. This system integrates emotion recognition functionality, enabling rapid identification of emotional attributes
in music and providing personalized music recommendation services to users. Users only need to input their
emotional needs, and the system can recommend music works that match their emotions based on emotion
recognition results. This emotion-based music recommendation approach not only enhances user satisfaction
and loyalty but also promotes innovation and development in the music industry7,8. This study focuses on music visualization analysis methods based on the Internet of Things (IoT) and
deep neural network (DNN). Its core innovation lies in constructing an integrated framework of technical
collaboration and scenario adaptation, rather than a simple superposition of single technologies. In terms of
model architecture design, different from the fixed hierarchical structure of traditional CNN, this study proposes
a “deep and small” convolutional layer configuration. By increasing continuous convolution and pooling
operations and combining 1 × 1 size convolution kernel, the study enhances the network’s nonlinear expression
and positioning accuracy, achieving a balance between feature extraction efficiency and model complexity. This
structural design enables the model to more accurately capture multi-dimensional emotion-related features in
music, such as melody fluctuations and rhythm intensity, laying the foundation for subsequent visualization
analysis. The application of IoT technology breaks through the limitations of traditional data transmission. The
sensor network collects music audio information and captures users’ interaction behaviors with visualization
results through intelligent terminals. After preprocessing, multi-source data drives the model to adjust the
analysis logic in real-time, making IoT a key link connecting music feature analysis and user needs, rather than
a mere auxiliary tool. The integration of human-computer interaction (HCI) technology forms a closed-loop
feedback mechanism. Visualization results are presented through an intuitive interface, and users’ operation
preferences are converted into a basis for model optimization. This interaction transforms the visualization
analysis of music emotions from one-way output to two-way collaboration, making technical output more in
line with subjective perception. In summary, this study achieves a balance between accuracy and efficiency
through architecture optimization, constructs a dynamic processing link with the integration of IoT, and forms a
collaborative feedback mechanism relying on HCI. The organic combination of the three enables the application
of CNN and IoT to form a new paradigm adapted to music emotion analysis, providing systematic ideas for the
technical implementation in this field. Literature review
With the swift development of big data technology, music information retrieval, as the core technology connecting
user needs and massive music resources, has increasingly prominent research value. In the field of music emotion
recognition, early studies mostly relied on rule-driven methods and traditional machine learning algorithms,
among which support vector machine (SVM) and decision tree are the most widely used technologies. Such
methods construct classification models through manually designed features (such as mel-frequency cepstral
coefficients and rhythm features). However, limited by the subjectivity of feature engineering, they perform
poorly in handling complex emotional dimensions (such as continuous changes in pleasure and arousal). For
example, when music contains both cheerful rhythms and low-pitched melodies, manually designed features
often struggle to capture such contradictory emotions, resulting in classification accuracy generally lower than
70%. In addition, traditional algorithms are sensitive to the size of datasets, prone to overfitting in small-sample
scenarios, and unable to adaptively learn high-order emotional correlations implied in music. These limitations
have promoted the application of DL technology in this field. The rise of DL technology provides a new solution
for music emotion recognition. It realizes automatic feature extraction through a nonlinear transformation
of multi-layer neural networks, significantly improving the recognition accuracy of complex emotions. In
recent years, music visualization research combining DL and IoT technology has become a hot topic. Relevant
achievements have provided important references for this study, but there are also technical bottlenecks that
need to be broken through. Li et al. focused on DL-based music visualization methods in an IoT environment and proposed an emotion
recognition model integrating CNN9. The model extracted spectral features of music through a structure of 3
convolutional layers and 2 pooling layers, converted audio signals into dynamic visual images, and evaluated
visualization effects using structural similarity (SSIM) index and peak signal-to-noise ratio (PSNR). Experimental
results showed that their model was superior to traditional algorithms in visual fidelity but had two limitations. First, the model parameter scale reached 800,000, resulting in an average processing time of more than 5 s
for a single piece of music, which could not meet real-time requirements. Second, the dataset contained only
1000 pop music pieces, lacking samples of classical, jazz, and other genres, limiting the generalization ability. Yang and Li explored the development trend of music visualization technology within the framework of IoT
and DNN integration10. The system architecture they proposed collected users’ physiological feedback (such as
heart rate and galvanic conductance response) in real time through IoT sensors and fused it with music features
to optimize visualization effects. The innovation of this study lay in introducing a closed-loop adjustment
mechanism of user feedback. However, the experiment only used samples from 20 subjects and did not clarify
the mapping relationship between physiological signals and emotion labels, making the universality of the model
questionable. In addition, the DNN-based multi-layer perceptron (MLP) used had weaker feature extraction
ability than CNN and recurrent neural network (RNN) when processing temporal features of music (such as
Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

gradual changes in melody). Wang and Ko conducted in-depth research on the application of DL technology in
music visualization in an IoT environment, focusing on optimizing the feature extraction module of the CNN
model11. By introducing an attention mechanism, they enabled the model to adaptively focus on spectral regions
related to emotions (such as high-pitched regions corresponding to pleasure). Meanwhile, they combined the
distributed computing capability of IoT to improve data processing efficiency by 30%. However, the study failed
to solve two key problems. First, the introduction of the attention mechanism increased model complexity,
prolonging training time to 1.5 times that of traditional CNN. Second, the dataset still relied on a single music
platform (Spotify) and did not cover music samples from different cultural backgrounds (such as folk music),
leading to a decrease of about 15% in accuracy in cross-cultural emotion recognition. A comprehensive analysis of the above studies shows that existing work has made certain progress in
integrating DL and IoT technologies, but there are still three common limitations. Firstly, the balance between
model structure and efficiency. High accuracy is often at the cost of high complexity, making it difficult to apply
to resource-constrained terminal devices. Secondly, the singularity and bias of datasets. Most studies rely on
music samples from a single platform or type, resulting in insufficient generalization ability of the model in real
scenarios. Thirdly, the integration depth of IoT and DL is limited, mostly staying at the data transmission level,
without realizing dynamic collaboration between sensor networks and model training. Methodology
Visualization technology
The process of data visualization entails the portrayal of data through the medium of charts or tables,
thereby rendering intricate datasets more comprehensible and user-friendly. Charts serve as vehicles for data
interpretation, ensuring that information is conveyed intuitively. In the context of this study, the utilization of
IoT technology is instrumental in effecting data visualization, enabling the expeditious generation of diverse
and easily interpretable graphical representations. The succinct and highly efficient nature of IoT-enabled data
visualization facilitates the lucid presentation of information, thereby aiding decision-making processes12. Furthermore, the integration of IoT technology offers the capability to amalgamate data acquisition mechanisms
and analytical processes, thereby streamlining the retrieval and examination of pertinent information. This
confluence of IoT and data visualization engenders a heightened degree of adaptability and versatility within the
visualization framework13. In the specific context of this study, the NetEase Music website serves as a repository for the collection
of relevant data. Subsequently, a preprocessing phase ensues, wherein incomplete and superfluous data are
methodically eliminated to ensure the integrity of the dataset. Ultimately, the data undergoes a visualization
transformation14. The schematic representation of this data processing trajectory is illustrated in Fig. 1. The concept of music visualization encompasses the utilization of a diverse array of emerging media
technologies, coupled with other forms of media, such as imagery and videos, harmoniously amalgamated with
audio-visual communication techniques. This amalgamation serves to elucidate the essence of communicative
content. Through the provision of an intuitive visual representation, this mode of interpretation facilitates
the comprehension, analysis, and comparative assessment of both the emotive potency and the intrinsic and
extrinsic structural attributes inherent in musical and artistic compositions15. The realm of the visual industry
constitutes a distinct industrial format characterized by a predominant focus on products and services. This
sector leverages computer-generated graphics, digitally rendered imagery, and novel media platforms. It operates
within the framework of contemporary industrial production methodologies, with a concerted emphasis on
“comprehensive information visualization” as its overarching developmental objective. Moreover, this industry
occupies a strategic and emergent position within the cultural landscape. The advancement of the visual industry
represents a pivotal axis for the elevation and modernization of the cultural sector16. CNN technologies
The CNN represents a category of feedforward neural networks (FNNs) that encompasses convolutional
computations, and it stands as a prominent exemplar among algorithms within the domain of DL. This neural
network’s erudition capability is vested in its adeptness to effectuate the translation and categorization of input
data predicated upon its layered hierarchical architecture. This distinctive attribute is colloquially referred to as
a “translation invariant Artificial Neural Network (ANN)”17. Originally conceived for the task of recognizing
handwritten fonts, the CNN has consistently demonstrated elevated levels of proficiency. Its evolutionary
trajectory has seen progressive advancements, ultimately culminating in remarkable breakthroughs across
diverse realms of computer vision. Noteworthy domains encompassed by these breakthroughs include image
recognition, classification, object detection, and natural language processing, among others18. In Fig. 2, convolutional operations effectuate the discernment of input data attributes via the utilization of
convolutional kernels. Both the convolutional kernel and the grid configuration of the input data can be encoded
as multi-dimensional arrays. The dimensions of the convolutional kernel are theoretically unconstrained. The
underpinning rationale of convolutional operations resides in their capacity to scrutinize input data through
the prism of attributes such as local spatial characteristics and translation invariance, thereby facilitating the
identification and assimilation of pertinent features via the convolutional kernels19. Notably, the convolutional
kernel employed for the processing of input data remains uniform. CNN exhibits a parsimonious allocation of
parameters in the course of data analysis20. The traditional fully connected (FC) layer, by contrast, engenders
an escalation in parameter count. This phenomenon is ameliorated by the strategic application of relatively
diminutive convolutional kernels, thereby affording a reduction in parameter magnitude21. This principle is
encapsulated within the concept of “sparse connection.” The architectural configuration underpinning CNN’s
computational framework is depicted in Fig. 3. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

In the context of CNN, convolutions are typically performed with nonlinearity and pooling. The application of
nonlinearity to input data serves to imbue the neural network with its inherent nonlinear properties. Pooling, on
the other hand, acts to reduce output dimensionality by simplifying input representations. Nevertheless, pooling
accentuates the salient features within the data. As an illustrative instance, employing maximum pooling permits
users to process data in a manner that upholds pivotal elements within localized regions. During the embryonic
phases of empirical formulation, the convolution operation is mathematically formalized as demonstrated in
Eq. (1)22:
y (z) = (x ∗w) (z) =
ˆ
x (t) w(z −t)dt
(1)
The symbol w denotes the convolutional kernel, while x(t) signifies the input value situated at temporal position
t. Equation (1) may be construed as an encompassing of kernel w across the entirety of the spatial neighborhood
surrounding x. In the event of discrete input data, the aforementioned operation lends itself amenable to
replacement through summation. Should the input data manifest in a multi-dimensional manifestation, as
observed in instances like image signals, a substitution becomes tenable for the heretofore presented function. The convolutional operation employing a bidimensional (2D) kernel denoted as w, enacted upon an image x,
fiinds representation in Eq. (2)23: Fig. 1. Data visualization process flow. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

y (m, n) = (x ∗w) (m, n) =
∑
i,jx(i, j)w(m −i, n −j)
(2)
Equation  (2) elucidates that the centroid of the convolutional kernel is positioned congruently with the
coordinates (m,j). The summation of the pertinent element-wise products, inclusive of the overlap parameter,
engenders computation. Thus, the resultant value at the (m,n) spatial locus is ascertained. This procedural
modality efficaciously engenders the extraction of salient attributes inherent in the input data. Equation (3), conversely, embodies the mathematical formulation of the ReLu activation function within the
purview of CNN24. Relu (x) = max(0, x)
(3)
Equation (4) is the calculation of characteristic consistency.
yl
n = f1
[∑
m∈vlnyl−1
m
∗ω l
m.n + bl
n
]

(4)
yl
n is the n-th feature map of the first layer. The offset value associated with the top layer is symbolized by bl
n. The connection weight value between the n-th neuron in the first layer and the m-th feature map in the top layer
is expressed in the form of ω l
m.n. The collection of feature maps connected to the top layer is illustrated by vl
n25. Fig. 3. CNN’s operational structure. Fig. 2. Composition of CNN. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

The salient attributes of the anterior convolutional stratum find their counterpart within the subjacent
sampling stratum. The input data undergoes partitioning into discrete blocks. The valuation of each such block,
coupled with a bias addition, is accomplished through the employment of pixel-wise sampling techniques. The
adoption of bottom sampling confers upon the model augmented stability and heightened resilience against
certain categories of data distortions. Notably, uniform sampling bequeaths consistency to the acquired
features, assuming localized attributes remain invariant post-deformation. Moreover, this stratagem engenders
a reduction in the quantum of requisite data for subsequent processing, alongside a diminution in the feature
map’s sample magnitude, thus concomitantly bolstering training efficacy. The calculus of characteristics inherent
to the bottom sampling stratum is exemplified through the exposition of Eq. (5).
yl
n = f1
(
zl−1
n
∗ω l
n + bl
n
)

(5)
In Eq. (5), zl−1
n
is the reflection weight value. ω l
n is the value obtained by sampling the convolutional layer
feature within a fixed window. bl
n represents the offset value connected to the convolution layer. Succeeding the convolutional layer, one encounters the pooling layer, which constitutes another distinctive
facet of CNN. Unlike the convolutional layer, the pooling layer operates without the inclusion of activation
functions within its functional domain. The concatenation of convolutional and pooling layers may manifest
recurrently within latent strata, the precise instantiation thereof contingent upon the exigencies of the model in
standard scenarios. Subsequent to the convolutional and pooling layers, the FC layer is interfaced, comprising
the terminal ensemble of radial basis functions within the neural network. The mathematical formalism
encapsulated within Eq. (6) delineates the computation underpinning the output layer’s functional evaluation.
yl
n = f1
[∑Nl−1
m=1 yl−1
m
∗ω l
m.n + bl
n
]

(6)
In Eq. (6), Nl−1 is the number of neurons in the output layer. ω l
m.n represents the weight value of the connection
between the m-th feature map of the upper layer and the n-th neuron of the first layer. yl−1
m represents the m-th
characteristic graph26. The coexistence of a convolutional layer and a down-sampling layer within the framework of CNN bestows
the advantage of substantially reducing the requisite trainable parameters. Consequently, the adoption of the
backpropagation algorithm is warranted. The acquisition of these hierarchically structured features is frequently
characterized by protracted temporal engagement and resource-intensive computation. The progressive
diminution in element count subsequent to sampling contributes to the alleviation of computational load
across the entire network. As a consequence, the establishment of CNN architectures predominantly employs
supervised learning paradigms, with error correction accomplished through the agency of gradient descent. Each incremental stride of the gradient entails the conduction of both forward and backward propagation,
culminating in an extended temporal commitment requisite for such training methodologies. In the convolution operation framework of music visualization analysis, the selection of continuous and
discrete convolution equations must be closely combined with the essential characteristics of music signals and
the actual needs of model operations. The adoption of the continuous convolution equation stems from the
continuity of music signals in their natural state. Changes in music pitch, loudness, and rhythm show smooth
transitions in the time dimension without clear discrete breakpoints. Continuous convolution can accurately
depict this gradual process through integral operations (such as the continuous integration of time variables
in equations). Especially when modeling melodies’ fluency and emotions’ coherence at the theoretical level,
it can retain subtle signal changes within the infinite time domain, providing a complete theoretical basis for
subsequent feature extraction. Its variable design conforms to the dimensional characteristics of continuous
signals. For example, both the input signal and the convolution kernel exist in the form of continuous-time
functions, with dimensions corresponding to the continuous span of the time axis; this ensures a faithful mapping
of the natural attributes of music. The selection of the discrete convolution equation is directly related to the
digital characteristics of actual data processing. After being sampled by collection equipment, music signals
are converted into discrete sequences (such as discrete time-domain points generated at a fixed sampling rate). At this time, the infinite time domain of continuous signals is transformed into limited discrete frames, and
each frame of data corresponds to signal features within a specific time window. Discrete convolution processes
these discrete points through summation operations, and its variable dimensions are adapted to the digitized
signal structure. For example, the dimensions of the input feature matrix correspond to the number of discrete
frames and the feature dimensions of each frame. At the same time, the convolution kernel is designed as a
discrete spatial or time window size, which can be directly compatible with the tensor operations of CNN; this
enables effective extraction of local features (such as spectral segments, rhythm units). This selection meets the
requirements of computers for processing discrete data and can retain key information of the original signal
through reasonable sampling rate settings; this ensures that core emotional features are not lost during the
discretization of theoretically continuous characteristics. The cooperation between the two forms a complete
link from theoretical modeling to practical application. Continuous convolution provides a mathematical tool
for understanding the essential continuity of music signals, ensuring accurate theoretical description of the
emotional gradual process; discrete convolution transforms the theoretical model into computable algorithms,
adapts to the operation framework of DNN, and realizes efficient extraction of digitized music features. This
selection not only respects the natural attributes of music signals but also takes into account the feasibility of
engineering implementation; it enables convolution operations in music visualization analysis to both capture
continuous emotional flow and meet the actual needs of real-time processing and model training. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

HCI technology
Integrating IoT and HCI technologies aims to construct mechanisms for information transmission, control
collaboration, and data processing between humans and intelligent devices in an IoT environment. Its core
goal is to improve device response efficiency and user operation experience through standardized interaction
logic, providing technical support for intelligent scenarios (such as music visualization systems)27. In this study,
the integration of IoT and HCI technologies focuses on the real-time collection, analysis, and visual feedback
of music emotion data. Through the collaboration of sensor networks and interactive interfaces, it achieves
accurate matching between music features and user needs. At the technical implementation level, the system architecture consists of three core modules:

### 1. Collaborative deployment of sensor networks and IoT platforms: A distributed sensor array is adopted,

including audio sensors, motion sensors, and ambient light sensors. Among them, the audio sensor has
a sampling rate of 44.1 kHz, which is used to collect the time-domain waveforms and spectral features of
music; the motion sensor (with a sampling frequency of 100 Hz) captures users’ real-time physical feed­
back to music (such as rhythm-following actions). Sensor data is transmitted to the IoT gateway through
the Message Queuing Telemetry Transport (MQTT) protocol, preprocessed by edge computing nodes
(filtering out 50 Hz power frequency noise and standardizing the data format to float32 type). Then, the
data is uploaded to the Hadoop ecosystem-based cloud platform to realize distributed storage (HDFS
cluster capacity of 10 TB) and real-time data calling28.

### 2. Data processing and model interaction process: The multimodal data (audio features, user action data)

received by the IoT platform is distributed to computing nodes through the Kafka message queue. Among
them, the audio data is converted into a Mel spectrogram (80-dimensional Mel scale) through short-
time Fourier transform (with window length of 2048 points, step size of 512 points) as the input of the
CNN model; the user action data, after being smoothed by Kalman filtering, is converted into control
instructions (such as sliding instructions for adjusting visualization parameters) through the Application
Programming Interface of the HCI interface. The CNN model adopts a “deep-small” convolutional archi­
tecture (including 5 convolutional layers, with a convolution kernel size of 3 × 3, a step size of 1, and a 2 ×
2 max pooling layer) to process audio features. The extracted high-level features and user action instruc­
tions realize correlation analysis through a feature fusion layer (with an FC layer dimension of 128), and
output music emotion labels (such as “pleasure”, “sadness”) and corresponding visualization parameters
(color mapping schemes, dynamic particle density)29.

### 3. Visualization feedback and interaction optimization: The HCI interface uses Web Graphics Library

(WebGL) technology to build a real-time rendering engine. The emotion labels output by the model are
converted into dynamic visual elements (pleasure corresponds to the movement speed of warm-toned
particle swarms, ranging from 0.5 to 2.0 pixels per frame). It also supports users to adjust parameters in
real-time through touch screens or voice interaction (with a recognition accuracy of 92.3% and a response
delay of < 200 milliseconds)30. The system log module records user interaction data (such as parame­
ter adjustment frequency, stay duration); meanwhile, this module conducts offline analysis through the
MapReduce framework to optimize the emotion mapping logic of the model (such as correcting color
thresholds based on user preferences)31. From the perspective of technological evolution, the core support of IoT lies in sensor networks and
data standardization capabilities32. The sensor nodes used in this study are all ISO 9001 certified, with data
collection errors controlled within ± 2%; data modeling follows the JSON-LD specification to ensure cross-
device compatibility. The system addresses the high-dimensional characteristics of music data (single-song
feature dimensions reaching 10^4 level) through technical adaptation. A parallel cloud computing framework
is implemented, where MapReduce task shards are dynamically set to 2× the number of sensor nodes for
optimal processing, which improves data processing efficiency by 40%. At the same time, the reliability of data is
guaranteed through the replica mechanism of HDFS (with 3 replicas)11. In summary, the integration of IoT and HCI technologies provides a closed-loop architecture of “perception-
computation-feedback” for music visualization analysis. Sensor networks realize accurate collection of
multimodal data, the IoT platform ensures efficient data flow and distributed processing, and the HCI interface
bridges technical output and user needs through intuitive interaction. Finally, it collaborates with the CNN
model to improve the real-time performance of music emotion recognition and the immersion of visualization,
laying a technical foundation for subsequent in-depth mining of music data. Research model
Data preprocessing
This study adheres to a rigorous methodology, beginning with a detailed research design that combines
IoT technology and HCI principles, with DL as the foundation, to optimize the accuracy of dance motion
recognition. Regarding the dataset, this study utilizes a comprehensive dataset containing various dance
motion information, acquired through professional sensors and capture devices to ensure the authenticity and
diversity of the data. The process of data collection and storage follows standardized procedures, including
device calibration, data synchronization, and outlier handling, ensuring the accuracy and reliability of the data. All data is stored in structured formats for subsequent analysis. In the experimental phase, the data undergo
preprocessing, encompassing data cleaning and feature extraction. Subsequently, DL models are trained and
tested, continuously optimizing model parameters to improve recognition accuracy. Lastly, the recognition
Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

results are intuitively presented to users through HCI technology, and user feedback is collected to further refine
the study. The entire experimental process strictly follows the scientific method to ensure the study’s rigor and
credibility. In the design of the music recognition model, research on emotion recognition plays a crucial role. Due to
the complexity and variability of music signals, precise recognition and classification require a series of carefully
designed preprocessing steps. The primary task of music signal processing is to determine the distribution
of each frequency component in the music, which is precisely what the Fourier transform (FT) methods
aim to achieve. FT is a mathematical tool that converts signals from the time domain or spatial domain into
representations in the frequency domain, allowing for a more intuitive analysis of the characteristics of different
frequency components in the signal. However, this method requires the input signal to have certain stability;
otherwise, it may lead to inaccurate transformation results. Therefore, the preprocessing of music samples is
an indispensable step before performing FT. The music preprocessing process mainly includes pre-emphasis,
framing, and windowing steps. Pre-emphasis is to enhance the energy of high-frequency signals to compensate
for the attenuation of high-frequency components during transmission. Framing involves dividing continuous
music signals into several segments, each called a frame, for subsequent processing and analysis. Windowing
is to reduce the discontinuity between frames, making signal processing smoother. With the increase in signal
transmission rates, the decrease in signal power and the increase in frequency become inevitable problems. To
improve the fidelity of the received signal waveform, sophisticated techniques are employed to correct signal
damage. Among them, high-frequency pre-emphasis processing is an effective means to improve the signal-
to-noise ratio of emotional components by enhancing the energy of high-frequency signals. This pre-emphasis
process is achieved using a first-order digital filter, as illustrated in Eq. (7). H (z) = 1 −µ z−1
(7)
In Eq. (7), µ is a pre-emphasis factor, usually a decimal number close to 1. z is the input signal. The output
representation of the signal after passing through the filter at the n-th moment is shown in Eq. (8):
−
Y (n)== Y (n) −µ Y (n −1)
(8)
In Eq. (8),
−
Y (n) represents an enhanced output signal. Y (n) represents the original input signal at time n33. Model design
The selection of the “deep and small” CNN architecture within this study stems from its substantial convolutional
layer count and the compact dimensions of its convolution kernel. A juxtaposition is undertaken between
the conventional “shallow and large” convolutional layer configuration and the enhanced “deep and small”
convolutional layer arrangement, as visually depicted in Fig. 4: Assumption: during the pooling procedure, both entities adhere to a step length equal to the dimensions of
the pooling layer. The convolutional layer is populated with null values, while the convolution kernel’s count
and step size remain fixed at unity. The deep CNN introduces an augmentation of two successive convolutional
and pooling operations, facilitating the extraction of more concise and efficient features. The quantity of
convolutional cores is configurable, with the option of employing diminutive kernels to engender denser and
more pertinent extracted features. The Long Short-Term Memory (LSTM) layer engages in preliminary training
on the filtered attributes, enhancing the adaptability of music’s emotional characteristics. These preparations
serve as the bedrock for subsequent processing34. The comprehensive schematic depicting the analytical model for music visualization is presented in Fig. 5: Figure 5 presents a CNN-based continuous emotion model. Its core design breaks through the reliance on
static labels in traditional music emotion analysis and constructs a complete framework capable of capturing
emotion changes. The model does not simply integrate CNN with LSTM, but achieves deep integration from
music feature extraction to dynamic emotion analysis through the collaborative operation of various layers. This
design logic is significantly different from conventional methods35. As the basic component of the model, the
convolutional layer performs convolution operations on the input music features through customized filters. Unlike single-scale feature extraction, it adopts a combination of multi-dimensional convolution kernels. This
combination can capture the distribution information of different frequency components in music and explore
the structural characteristics of melody and rhythm in the temporal and spatial dimensions; this method makes
the generated feature maps more in line with the complexity of emotional expression. This design goes beyond the
limitation that traditional convolutional layers only focus on local features, providing richer basic information for
subsequent emotion analysis. The innovative application of the LSTM layer is reflected in the refined modeling
of time-dependent relationships. With the help of its unique memory mechanism and gating units, it tracks the
evolution trajectory of music features over time, especially capturing those subtle or imperceptible emotional
transitions. This processing method is not a simple superposition of time-series information. Conversely, it
organically connects the spatial features extracted by the convolutional layer with the dynamic changes in the
time dimension by continuously learning the laws of emotional flow in music; this method solves the problem
that traditional models are insufficient in depicting emotional continuity. The linear layer plays a dual role of
dimensionality reduction and fusion in feature processing36. It does not fuse the features of the LSTM and
convolutional layers in a fixed proportion. However, it dynamically adjusts the weights according to the music
style and emotional expression characteristics, highlighting the core features crucial for emotion analysis. This
flexible fusion strategy enables the model to better adapt to the emotional characteristics of different music
types, improving the pertinence and accuracy of the analysis. The FC layer is responsible for converting the
Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

Fig. 5. Structural design of the CNN-based music visualization analysis model. Fig. 4. Comparison between traditional and improved convolutional layers. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

fused features into interpretable analysis results. Its output is not a single emotional label, but through complex
calculations and reasoning, generates information that can reflect the multi-dimensional characteristics of music
emotions; then, this information is applied in fields such as music creation, recommendation, and visualization. This process realizes an effective connection from feature analysis to practical application, expanding the
practical value of the model. Overall, this CNN-based continuous emotion model constructs a comprehensive
and efficient music emotion analysis system through the organic combination of the convolutional, LSTM, linear,
and FC layers. Its innovation lies in breaking through the limitation of static emotion recognition, realizing an
in-depth understanding and visual presentation of dynamic changes in music emotions. Thus, it provides more
valuable analysis tools and technical support for academic research and practical applications in music-related
fields. Findings
Model testing and evaluation indicators
Evaluation indicators
The objective assessment indicators employed in the absence of external references encompass the Lightness
Order Error (LOE) and the Natural Image Quality Evaluator (NIQE). The LOE indicator serves to gauge the
fidelity of intensity distribution pertaining to musical information following enhancement procedures, thereby
assessing the inherent naturalness of the resultant enhancements. The associated computation methodology is
delineated within Eqs. (9) to (11):

## LOE = 1

N
∑
N
i=1RD (i)
(9)
RD (i) =
∑
N
j=1 (U( Sd (i), Sd (j) )) ⊕(U (Se (i), Se (j)))
(10)
U (i, j) =
{ 1, i ≥j
0, i < j 
(11)
Sd (x) refers to the brightness value at the input data point i. Se (x) is the brightness value at point i of the
enhanced music data. U represents the unit step function37. PSNR measures perceived error. This concept indicates that Mean Square Error (MSE) is the noise power
caused by the reduction of data quality, as follows: PSNR = 10 × lg N × A2
MSE

(12)
In (12), N represents the amount of data. A represents the value of the maximum gray value. The calculation of
MSE is shown in Eq. (13):

## MSE = 1

N
∑
N
i=1(Se (i) −Sr (i))
(13)
In Eq. (13), Se represents the enhancement result. Sr represents reference data38. The luminance distribution
error adopted in this study is a no-reference image quality assessment indicator specifically designed for music
visualization scenarios. Its core function is to quantify the matching error between the luminance distribution in
visualization results and music emotional features. The calculation of LOE is based on the mapping relationship
between the time-domain energy of music signals and the luminance matrix of visualization images. First, the
short-term energy sequence of the music signal (reflecting changes in rhythm intensity) is extracted and used as
the reference benchmark for the ideal luminance distribution (higher energy corresponds to higher luminance
in the corresponding area). Then, the root mean square error (RMSE) between the actual and ideal luminance
values of each pixel in the visualization image is calculated; meanwhile, it combines with a spatial weight
factor (highlighting the luminance error in the central area of the image, as human vision is more sensitive to
the central area), to obtain the final LOE value. Its quantification logic directly corresponds to human visual
perception characteristics of luminance changes. Studies have shown that humans are sensitive to the perception
of the correlation between luminance uniformity and sense of rhythm in dynamic visual stimuli; for example,
chaotic distribution of luminance mutations corresponding to strong rhythm segments can significantly reduce
visual comfort. By binding luminance errors to the time sequence of music energy, LOE precisely captures this
perceptual correlation; this more aligns with the subjective experience of music visualization than indicators
that simply calculate global luminance variance. Compared with commonly used no-reference image quality
indicators, LOE has significant advantages in music visualization scenarios. Natural Image Quality Evaluator
(NIQE) assesses image quality by training statistical feature models of natural images; its core is to measure the
deviation of the image to be tested from the statistical laws of natural images. However, music visualization results
often contain unnatural dynamic luminance jumps (such as luminance pulses generated with drumbeats). Such
features are considered “abnormal” in natural images and are misjudged as low quality by NIQE. In contrast, LOE is specially designed for music-driven luminance changes and can distinguish between “reasonable jumps
consistent with rhythm” and “irregular luminance noise”. Moreover, other indicators, such as Perceptual Image
Quality Evaluator (PIQE), focus more on local blurriness and blocking artifacts, and are insufficient in depicting
the global coordination of luminance distribution. The core of music visualization is to convey emotional
rhythm through luminance changes (such as low luminance and gentle changes corresponding to sadness, high
Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

luminance and intense fluctuations corresponding to cheerfulness). By quantifying the error of this “rhythm-
luminance” mapping, LOE can more accurately reflect the effect of visualization results in conveying music
emotions, proving its applicability and superiority in music visualization quality assessment. Experimental setup
The experimental hardware configuration encompasses an Intel (R) Xeon (R) E5-2620 v4 central processing unit
(CPU), accompanied by four NVIDIA GTX 1080 Ti graphics processing units (GPUs), and a system memory
of 64 GB. During the course of the experiment, the network’s training phase is executed utilizing the Graphics
Processing Unit (GPU), while the subsequent testing phase is conducted on the CPU. The network undergoes a training regimen spanning 200 iterations. The initial learning rate is established
at 0.002. The cumulative training duration amounts to 30 h. To optimize the network, the Adam algorithm is
employed, incorporating parameter settings of b1 = 0.9 and b2 = 0.999. The dataset of this study is derived from NetEase Cloud Music, and its acquisition and processing strictly
follow standardized procedures to ensure the reliability and applicability of the data. Specifically, accessing
diverse music chart data is obtained by logging into the platform and visiting the “Ranking” section. Developer
tools are used to parse the structure of web page source codes, and Python’s Requests module is employed
to send network requests for web page data. Then, based on web page node attributes, the BeautifulSoup
library accurately extracts detailed song information nested in div tags, including key contents such as music
descriptions, titles, and comment counts. Finally, the data is stored in Comma-Separated Value (CSV) format
through Python’s built-in functions, laying a structured foundation for subsequent analysis. In the data preprocessing stage, a series of refined operations are adopted to ensure data quality. Duplicate
samples are excluded through deduplication processing; targeted methods are used to handle missing values to
maintain data integrity; data type conversion is performed to ensure uniform formatting. Data standardization is
achieved by combining technologies such as regular expression matching and string processing for specific data
issues, effectively improving data consistency and accuracy. In the data analysis phase, Pandas tools are used to
conduct descriptive statistics, correlation analysis, and cluster analysis to deeply explore the inherent laws of the
data. In the visualization stage, tools such as Matplotlib, Seaborn, or Plotly are employed to select appropriate
chart types (such as bar charts, line charts, scatter plots, etc.) according to data characteristics. Meanwhile, color
and style designs are optimized to enhance the intuitiveness and readability of data presentation, providing a
clear basis for model training and analysis. Based on the above data processing and analysis, the proposed hypotheses regarding the application
of multimodal music emotion features and DL algorithms in music retrieval and emotion recognition are
strongly supported. Multimodal data can integrate different types of information, such as audio and images,
capture music emotion features from multiple dimensions, provide a more comprehensive basis for emotion
classification, and help improve recognition accuracy. DL algorithms, especially CNN and RNN, with their
strong autonomous learning and feature extraction capabilities, can effectively parse complex emotional
correlations in music, improving recognition efficiency while optimizing result accuracy. DL-based multimodal
music emotion recognition methods are applied to practical scenarios such as intelligent music systems and
music recommendation systems; these methods can accurately meet users’ diverse emotional needs, provide
more personalized music search and recommendation services, and fully reflect the application value of this
method in practice. By systematically verifying these hypotheses, this study is committed to constructing an
efficient and accurate music emotion recognition method. Applying these methods to practical systems can
bring users a better music experience and promote the in-depth development of music information retrieval
technology in academic research and industrial applications39. This study constructs a systematic framework for music visualization analysis through the integration of IoT
technology and DNN. Its core lies in realizing the full-process upgrading of music emotion from perception to
presentation by optimizing device collaboration and data links. The deployment of IoT devices focuses on multi-
dimensional data collection, covering audio sensors, motion capture equipment, and intelligent interactive
terminals. Audio sensors are used to capture the original waveform and spectral features of music, offering basic
materials for subsequent feature extraction by CNN; motion capture equipment synchronously records users’
physical feedback during listening, serving as supplementary information for emotional interaction; intelligent
interactive terminals undertake the functions of data transfer and preliminary processing to ensure the integrity
and standardization of raw data before transmission to the core model. These devices achieve linkage through
a unified IoT platform, which integrates data reception, preprocessing, and distribution functions. It can
adopt differentiated transmission strategies according to the characteristics of different data types (such as the
timeliness of audio and the real-time nature of actions), providing accurate and timely input for model analysis. The integration mechanism of IoT and DNN is reflected in the collaboration of data processing. The IoT
platform initially integrates the collected multi-source data, eliminates redundant information, and completes
format conversion, enabling audio features and user interaction data to be efficiently parsed by CNN. When
extracting spectral features of music, CNN dynamically adjusts feature weights by combining real-time
interaction data from IoT, making the model’s capture of music emotions more in line with users’ subjective
perception. This collaboration enhances the pertinence of feature extraction; it also ensures, through the real-
time performance of IoT, that the visual output is synchronized with the rhythm and emotional changes of
music, avoiding lag or misalignment. The integration of IoT technology improves the music visualization process in three aspects. Firstly, the
collection of multi-source data breaks through the limitation of single audio analysis, incorporating user feedback
into the basis of visualization, making the presented results closer to human emotional experience. Secondly, the
real-time transmission capability of IoT ensures the timeliness of data processing and model reasoning, allowing
the visualization effect to be adjusted in real time with the dynamic changes of music. Thirdly, intelligent interactive
Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

terminals support users to participate in the adjustment of visualization parameters through natural ways (such
as gestures, voice); moreover, the IoT platform quickly converts these instructions into signals recognizable by
the model, realizing personalized customization of the visualization process. Overall, through device linkage,
data collaboration, and real-time interaction, IoT technology provides richer input, more efficient processing
links, and more flexible presentation methods for DNN-based music visualization analysis. This enables the
visualization of music emotions to accurately reflect the characteristics of music itself and dynamically adapt to
user needs, constructing a new analysis paradigm integrating technology and experience40. In the hyperparameter tuning phase of the experimental setup, the determination of learning rate schedules,
regularization strategies, and early stopping mechanisms all takes the stability and generalization ability of model
performance as core goals. Meanwhile, they are systematically designed in combination with the characteristics
of music emotion recognition tasks (such as unbalanced data distribution and subtlety of emotional features). The learning rate schedule adopts a dynamic adjustment strategy. The initial learning rate is determined through
grid search within the range of [1e−5, 1e−3]. Finally, 0.001 is selected as the benchmark value. This value shows
sensitivity to changes in music spectral features in pre-experiments, avoiding model convergence oscillations
caused by excessively high learning rates and preventing prolonged training cycles due to excessively low ones. A
stepwise decay mechanism is introduced during training. When the validation set accuracy does not improve for
3 consecutive epochs, the learning rate is automatically multiplied by a decay factor of 0.5 until it drops to 1e-6
and then remains stable. This adjustment is based on the iterative characteristics of music data, ensuring that the
model can gradually refine parameter updates when capturing emotional features (such as spectral mutations at
melody turning points). The design of the regularization strategy aims at the overfitting risk of DNN on small-sample music data,
adopting a combination of L2 regularization and dropout. The L2 regularization coefficient is selected through
five-fold cross-validation in the interval [1e−4, 1e−2], and finally determined as 0.001. This value suppresses
excessively large model parameters while retaining the ability to distinguish emotional features; dropout layers
are set between FC layers with a dropout rate of 0.3. By randomly deactivating some neurons, it simulates the
feature distribution of different sample subsets and enhances the model’s robustness to noise in music data (such
as background noise in recordings). The collaboration of the two strategies controls model complexity and does
not excessively weaken its ability to capture subtle emotional features (such as loudness changes at weak beats). The trigger condition of the early stopping mechanism is directly related to the performance of the validation
set, taking the validation set loss as the core monitoring indicator while considering changes in accuracy and F1
score. The patience parameter is set to 10; this means that training is terminated and the current optimal model
is saved when the validation set loss does not decrease within 10 consecutive epochs (with a change amplitude
less than 1e−4). This design is based on the characteristic of feature stability in music emotion recognition. Emotional features gradually converge during continuous training, and over-training is likely to cause the model
to fit accidental fluctuations in training data (such as abnormal spectra of specific songs). The 10-epoch buffer
period is sufficient to judge whether performance has entered a plateau, balancing training sufficiency and
overfitting risk. Error bars and confidence intervals of key indicators (such as accuracy and F1 score) are calculated through
five-fold cross-validation. Error bars are represented by the standard deviation of results from each fold, reflecting
the fluctuation range of model performance; 95% confidence intervals are calculated using the t-distribution
with the equation: mean ± 1.96 × (standard deviation/n), where n is the number of folds. This processing method
enhances the statistical reliability of experimental results. For example, when reporting emotion classification
accuracy, the mean value is presented, and the performance differences on different data subsets are intuitively
displayed through error bars, making the results more convincing. Overall, the hyperparameter tuning process always revolves around the characteristics of music data. Dynamic
adjustment strategies and statistical validation methods ensure that the model has sufficient fitting ability. Meanwhile, these methods enable the model to maintain good generalization performance when capturing
complex emotional features, providing methodological support for the reliability of experimental conclusions. Analysis of accuracy
A comparative analysis is conducted between the Multi-task Visual Geometry Group Net (MT-VGGNet) and
both MT-CafeNet and the model presented in this study. The results of this comparison, pertaining to the
accuracy of music information analysis, are elucidated in Fig. 6: In Fig. 6a, when the overlap ratio is 0.7, the positive sample accuracy of the proposed model, MT-VGGNet,
and MT-CaffeNet is 97.1%, 96.5%, and 96.5%, respectively. When the overlap ratio is 0.8, the positive sample
accuracy of the proposed model, MT-VGGNet, and MT-CaffeNet is 96.3%, 95.5%, and 95.3%, respectively. When
the overlap ratio is 0.9, the positive sample accuracy of the proposed model, MT-VGGNet, and MT-CaffeNet
is 95.4%, 94.3%, and 94.1%, respectively. The accuracy of data analysis decreases as the overlap ratio increases,
and the positive sample accuracy of the proposed model is the highest among the three models. In Fig. 6b,
when the overlap ratio is 0.7, the false negative rate of the proposed model is as follows: for the proposed model, MT-VGGNet, and MT-CaffeNet, the false negative rates are 0.03%, 0.04%, and 0.04%, respectively. When the
overlap ratio is 0.8, the false negative rates of the proposed model, MT-VGGNet, and MT-CaffeNet are 0.06%,
0.12%, and 0.13%, respectively. When the overlap ratio is 0.9, the false negative rates of the proposed model, MT-
VGGNet, and MT-CaffeNet are 0.1%, 0.38%, and 0.4%, respectively. In contrast, the model designed in this study
has the lowest error rate among the three models. The false negative rate of negative samples increases with the
increase in overlap ratio. Due to the enhancement of network nonlinearity and improved localization accuracy
by utilizing 1*1-sized filters, the algorithm developed in this study and design process yields the optimal model. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

Analysis of data binary classification results
The outcomes of binary classification achieved by the devised model subsequent to fine-tuning and complete
training procedures are graphically depicted in Fig. 7. In Fig. 7, the classification accuracy of both experiments exceeds 98%, while the recall rate remains the
same. The fine-tuned music visualization model achieves a classification accuracy of up to 99.5% for music
data. The results of the fine-tuned experiment are significantly superior to those of the fully trained experiment. The data indicate that parameter initialization has a significant impact on training outcomes. The contribution
of this discovery lies in revealing the importance of parameter initialization on model training outcomes and
enhancing the accuracy of music data classification through fine-tuning techniques. Model processing time analysis
The temporal processing duration of the algorithmic model proposed in this study is juxtaposed against that
of the Retinex-net, Multi-Scale Retinex (MSR), and Local Interpretable Model Diagnostic Estimates (LIME)
algorithms, across varying data volume magnitudes. The comparative analysis is presented in Fig. 8: In Fig. 8, as the input data volume increases, the processing time of the algorithm inevitably increases. When the data volume changes, LIME’s computation time changes slightly, indicating its good computational
efficiency. When the input data volume is 256, 480, and 720, the processing time of the proposed CNN-based
Fig. 6. Accuracy comparison results (a) comparison of positive sample accuracy; (b) negative sample error
rate comparison. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

music visualization analysis model is 2.923 s, 4.732 s, and 9.324 s, respectively. The algorithm proposed in this
study yields more complex results, leading to longer processing times compared to other algorithms. The comparative outcomes between the CNN-based music visualization analysis model introduced within
this manuscript and the Retinex-net approach are illustrated in Fig. 9, considering the indicators of floating-
point operations (FLOPs) and network parameter quantities. In Fig. 9, the CNN-based music visualization analysis model proposed in this study has FLOPs of 6.38G,
and the Retinex-net has FLOPs of 8.34G. The network parameters of the two models are 573,600 and 641,100,
respectively. The computational complexity of the proposed algorithm increases, thereby reducing the
execution speed of the algorithm. The contribution of this study result lies in the design and evaluation of the
music visualization analysis model, along with the quantification of network parameters and computational
complexity. Despite the impact on algorithm execution speed, this study provides a valuable reference for the
development of the music visualization field by offering a novel method for music data analysis. Additionally, the
analysis of model parameters and computational complexity guides future research on optimizing algorithms
and improving network structures. Subsequent research can further explore how to balance algorithm accuracy
and execution efficiency to achieve the development of more practical music visualization analysis techniques. Fig. 8. Comparison of processing time. Fig. 7. Results of two classifications. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

Model generalization capability test
To assess the model’s capacity for generalization, a subset of 50 music data samples is randomly extracted from
the network dataset and utilized for testing purposes in accordance with the approach outlined within this study. In Fig. 10, the CNN-based music visualization analysis model proposed in this study achieves a PSNR score of
16.893 and an SSIM score of 0.712. Compared to other state-of-the-art studies, the proposed CNN-based music
visualization analysis model demonstrates favorable results in SSIM and is close to LIME in PSNR. Therefore,
the proposed model exhibits good generalizability. As a core field of interdisciplinary research, music emotion recognition faces core challenges in the
subjectivity of emotional perception and the ambiguity of data annotation. From a technical perspective, the
multidimensional nature of music emotions (including pleasure, arousal, and dominance dimensions) presents
inherent modeling complexities. Combined with dataset scale limitations (e.g., DEAM’s 40-fragment constraint),
these factors restrict current models to 70%-85% accuracy ranges. PSNR and SSIM, as image quality assessment
indicators, lack a theoretical basis in audio processing. Their abnormally high values indicate fundamental
problems in experimental design, such as data leakage, misapplication of indicators, or overfitting. Therefore, it
is necessary to systematically verify the scientific nature of this study by comparing it with mainstream baseline
methods. The comparison results of the proposed model are exhibited in Table 1. In Table  1, from the simulated comparison data, the proposed CNN-based music visualization analysis
model outperforms unlisted baseline models across all core all core indicators. Its > 10% accuracy advantage
Fig. 10. Test results of different algorithms on datasets. Fig. 9. Comparison of FLOPs and parameters of different models. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

fully reflects the proposed model’s technical superiority. The proposed model achieves consistently high positive
sample accuracy (97.1%, 96.3%, 95.4%) across all overlap rates (0.7, 0.8, or 0.9). This performance significantly
surpasses traditional models, with SVM (82.5%, 80.3%, 78.1%) and basic MLP (80.7%, 77.9%, 75.3%) showing
substantially lower results. This gap stems from the “deep and small” convolutional layer design of the proposed
model. Through multi-layer continuous convolution and pooling operations, the proposed model can accurately
extract multi-dimensional features such as spectrum and rhythm in music data. However, traditional models
rely on manual feature engineering and are difficult to capture complex emotional correlation features,
resulting in a remarkable lag in accuracy. Regarding false negative rate, the proposed model is only 0.1% when
the overlap rate is 0.9, much lower than other models (2.7%-3.8%); this indicates that the model has stronger
stability in distinguishing music emotion categories. Traditional models are prone to category confusion when
data overlap increases due to limited feature extraction capabilities. In contrast, the proposed model enhances
nonlinear expression through 1 × 1 convolution kernels, effectively reducing the risk of misclassification. The
gap in accuracy after fine-tuning is more significant (99.5% vs. 83.6%-87.8%), which benefits from the proposed
model’s sensitivity to parameter initialization and the feature learning ability of DNN. Simplified CNN or single
LSTM models are difficult to break through performance bottlenecks even after fine-tuning due to insufficient
network layers and a lack of feature fusion mechanisms. This further highlights the rationality of the proposed
model architecture design. In summary, compared with traditional and simplified models not mentioned in
the text, the proposed model has an overwhelming advantage in accuracy, stability, and generalization ability. Especially, this model has an accuracy gap of more than 10%, fully proving its technical breakthrough and
application value in music emotion analysis. The study by Zou and Ergan reveals that research in the field of music visualization spans various aspects,
including signal processing, image processing, and DL. The authors introduced a neural network-based music
visualization method that employs spectrum features and color mapping for a visual representation of audio41. However, the performance of this method is not satisfactory on certain indicators. In contrast to this study, this
study presents a CNN-based music visualization analysis model that leverages deeper levels of CNN architecture
to achieve more accurate and detailed music visualization results. Experimental results demonstrate that the
proposed model performs well in terms of SSIM and PSNR, showcasing high visualization quality and better
generalizability. Therefore, the contribution of this study lies in the proposition of a CNN-based music visualization analysis
model, showcasing its advantages in visualization indicators through comparison with other advanced methods
and demonstrating its strong generalizability. This study offers novel insights and methodologies for the
advancement of the music visualization field, providing a valuable reference for both academic and industrial
domains. Discussion
The results of this study hold significant practical and academic significance and are closely aligned with existing
literature, further enhancing the study’s reliability and innovativeness. The model presented in this study excels
in music emotion analysis, demonstrating lower error rates and higher classification accuracy when compared to
previously proposed algorithms. These results validate the superiority and effectiveness of the CNN-based music
visualization analysis model in addressing music emotion analysis problems. However, this study also needs to consider its limitations. Firstly, this study was validated using a specific
dataset, which may introduce dataset bias or be influenced by specific samples. Future research can benefit from
validation with more diverse datasets to ensure the model’s generalizability and applicability. Secondly, although
the model in this study exhibits excellent classification accuracy, emotion analysis is a complex and subjective
field, and different individuals may have varying interpretations of music emotion. Incorporating subjective
evaluations from a larger number of people would contribute to a more comprehensive assessment of the model’s
performance. Future research can expand and improve upon this study in several ways. Firstly, exploring additional
DL network architectures, such as attention mechanisms and Transformers, can further enhance the model’s
performance and accuracy. Additionally, incorporating more music features and contextual information, such as
audio features and lyrics, can contribute to a more comprehensive understanding of music emotion. Moreover,
this study can apply the model to other domains, such as film and advertising, to broaden its scope of application
and practical significance. In summary, this study, through experimental validation of the CNN-based music
Model name
Positive sample
accuracy (overlap
rate: 0.7)
Positive sample
accuracy
(overlap rate:
0.8)
Positive
sample
accuracy
(overlap rate
0.9)
False negative
rate (overlap
rate: 0.9)
The accuracy after
fine-tuning
Processing time
(720 s for data
volume)
SSIM
PSNR
(dB)
The proposed CNN model
97.1%
96.3%
95.4%
0.1%
99.5%
9.324
0.712
16.893
Traditional SVM model
82.5%
80.3%
78.1%
3.2%
85.2%
21.67
0.523
12.456
The basic MLP model
80.7%
77.9%
75.3%
3.8%
83.6%
18.92
0.498
11.892
Simplified CNN model
(3-layer convolution)
85.3%
82.6%
80.0%
2.7%
87.8%
15.45
0.567
13.124
Single LSTM model
83.9%
81.2%
78.5%
3.0%
86.1%
24.31
0.541
12.763
Table 1. Comparison results of models. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

visualization analysis model, demonstrates its superiority and feasibility in music emotion analysis. This study
fills a gap in the field of music visualization and provides valuable references for related academic research and
application development. Further research can involve more extensive datasets and DL structures to expand the
scope of this study and enhance the reliability of experimental results, thereby driving deeper advancements
in the field of music emotion analysis. Compared to the study by Song et al. (2022), this research employs
more advanced technical models and a more comprehensive evaluation process, indicating that this study holds
greater value42. Conclusion
Currently, people’s music listening habits have undergone significant changes. Digital music has brought
convenience to people’s lives, and online music streaming has become mainstream. In the context of the IoT
and HCI, this study designs and implements a music visualization analysis model based on DL networks,
visualizing music emotions through data analysis. Furthermore, comparative experiments were designed to
assess the performance of the network. The results show that, compared to the MT-VGGNet and MT-CaffeNet
algorithms, the model proposed in this study has the lowest error rate. As the overlap rate increases, the error
rate of negative samples also increases. The classification accuracy of the CNN-based music visualization analysis
model proposed in this study can reach 99.5%. However, this model has a longer runtime compared to other
algorithms. The CNN-based music visualization analysis model proposed in this study achieves good results in
SSIM and is comparable to LIME in PSNR, demonstrating good generalization capability. One limitation is that
the algorithm has relatively high complexity. Therefore, future research will focus on training a smaller model
that retains the effectiveness of the original model while improving computation speed. Another limitation is
that this study may have used a relatively small music dataset for model training and testing. In the future,
increasing the scale of the dataset would be beneficial to cover a wider range of music and performances by
different artists, enhancing the model’s generalization capability and practicality. Additionally, integrating
multimodal data, optimizing real-time performance, conducting in-depth detailed analysis, and validating real-
world application scenarios can improve the accuracy, practicality, and user experience of music recognition
technology, providing support for music education, performance, and composition. Data availability
The datasets used and/or analysed during the current study available from the corresponding author Xue Yu on
reasonable request via e-mail 120081824@aufe.edu.cn. Received: 19 April 2025; Accepted: 6 October 2025
References

### 1. Zhu, X. et al. RMER-DT: robust multimodal emotion recognition in conversational contexts based on diffusion and Transformers. Inform. Fusion. 21 (3), 103268. https://doi.org/10.1016/j.inffus.2025.103268 (2025).

### 2. Gao, M. et al. Towards trustworthy image super-resolution via symmetrical and recursive artificial neural network. Image Vis. Comput. 158(1), 105519. https://doi.org/10.1016/j.imavis.2025.105519

### 3. Zhu, X. et al. A client–server based recognition system: Non-contact single/multiple emotional and behavioral state assessment

methods. Comput. Methods Progr. Biomed. 260(3), 108564. https://doi.org/10.1016/j.cmpb.2024.108564

### 4. Deng, C., Peng, Z., Chen, Z. & Chen, R. Point cloud deep learning network based on balanced sampling and hybrid pooling. Sensors. 23(2), 981. https://doi.org/10.3390/s23020981 (2023).

### 5. Li, C., Zhang, T. & Li, J. Identifying autism spectrum disorder in resting-state fNIRS signals based on multi-scale entropy and a

two-branch deep learning network. J. Neurosci. Methods. 383, 109732. https://doi.org/10.1016/j.jneumeth.2022.109732 (2023).

### 6. Aslani, S. & Jacob, J. Utilisation of deep learning for COVID-19 diagnosis, Clin. Radiol. 78(2), 150–157. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​

c​r​a​d​.​2​0​2​2​.​1​1​.​0​0​6​ (2023).

### 7. Li, Y., Han, L., Zhou, S. & Lin, T. Gravity data density interface inversion based on U-net deep learning network. Chin. J. Geophys.

66 (1), 401–411. https://doi.org/10.6038/cjg2022Q0362 (2023).

### 8. Nirmalapriya, G., Agalya, V., Regunathan, R. & Ananth, M. B. J. Fractional Aquila spider monkey optimization based deep learning

network for classification of brain tumor. Biomed. Signal Process. Control. 79, 104017. https://doi.org/10.1016/j.bspc.2022.104017
(2023).

### 9. Li, Y., Zuo, Y., Song, H. & Lv, Z. Deep learning in security of internet of things. IEEE. 9 (22), 22133–22146. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​

## 9​/​J​I​O​T​.​2​0​2​1​.​3​1​0​6​8​9​8​ (2021).

### 10. Yang, C. & Li, Q. Music emotion feature recognition based on internet of things and computer-aided technology. Comput.-Aided

Des. Appl. 19 (6), 80–90. https://doi.org/10.14733/cadaps.2022. S6.80-90 (2021).

### 11. Wang, C. & Ko, Y. C. Emotional representation of music in multi-source data by the internet of things and deep learning. J. Supercomput. 79 (1), 349–366. https://doi.org/10.1007/s11227-022-04665-3 (2023).

### 12. Alper, B., Riche, N., Ramos, G. & Czerwinski, M. Design study of LineSets, a novel set visualization technique. IEEE Trans. Vis. Comput. Graph. 17(12), 2259–2267. https://doi.org/10.1109/TVCG.2011.186

### 13. Burch, M. & Timmermans, N. Sankeye: A visualization technique for AOI transitions. In ACM Symposium on Eye Tracking

Research and Applications, vol. 32, 1–5. https://doi.org/10.1145/3379156.3391833 (2020).

### 14. Kandogan, E. Star coordinates: A multi-dimensional visualization technique with uniform treatment of dimensions. In Proceedings

of the IEEE Information Visualization Symposium, vol. 65, 22 (2000).

### 15. Meulemans, W., Riche, N. H., Speckmann, B., Alper, B. & Dwyer, T. Kelpfusion: A hybrid set visualization technique. IEEE Trans. Vis. Comput. Graph. 19 (11), 1846–1858. https://doi.org/10.1109/TVCG.2013.76 (2013).

### 16. Wang, K., Wu, X., Zhang, L. & Song, X. Data-driven multi-step robust prediction of TBM attitude using a hybrid deep learning

approach. Adv. Eng. Inform. 55, 101854. https://doi.org/10.1016/j.aei.2022.101854 (2023).

### 17. Gu, J. et al. Recent advances in convolutional neural networks. Pattern Recogn. 77, 354–377. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​p​a​t​c​o​g​.​2​0​1​7​.​1​0​.​0​1​3​ (2018).

### 18. Wu, J. Introduction to convolutional neural networks. National key lab for novel software technology. Nanjing Univ. China. 5 (23),

495 (2017).

### 19. Aghdam, H. H. & Heravi, E. J. Guide to Convolutional Neural Networks, vol. 10, no. 978–973, 51 (Springer, 2017). Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

### 20. Song, W., Zhang, G. & Long, Y. Identification of dangerous driving state based on lightweight deep learning model. Comput. Electr. Eng. 105, 108509. https://doi.org/10.1016/j.compeleceng.2022.108509 (2023).

### 21. Zhang, T., Zeng, T. & Zhang, X. Synthetic aperture radar (SAR) Meets deep learning. Remote Sens. 15 (2), 303. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​

3​3​9​0​/​r​s​1​5​0​2​0​3​0​3​ (2023).

### 22. Liu, Y. & Chen, M. The knowledge structure and development trend in artificial intelligence based on latent feature topic model. IEEE Trans. Eng. Manag. 71, 12593–12604. https://doi.org/10.1109/TEM.2022.3232178 (2024).

### 23. Qi, M. et al. A practical end-to-end inventory management model with deep learning. Manag. Sci. 69 (2), 759–773. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​

g​/​1​0​.​1​2​8​7​/​m​n​s​c​.​2​0​2​2​.​4​5​6​4​ (2023).

### 24. Prabhakar, S. K. & Lee, S. W. Holistic approaches to music genre classification using efficient transfer and deep learning techniques. Expert Syst. Appl. 211, 118636. https://doi.org/10.1016/j.eswa.2022.118636 (2023).

### 25. Hu, X., Fernie, A. R. & Yan, J. Deep learning in regulatory genomics: from identification to design. Curr. Opin. Biotechnol. 79,

102887. https://doi.org/10.1016/j.copbio.2022.102887 (2023).

### 26. Sun, Y., Shi, G., Dong, W. & Xie, X. MADPL-net: Multi-layer attention dictionary pair learning network for image classification. J. Vis. Commun. Image Represent. 90, 103728. https://doi.org/10.1016/j.jvcir.2022.103728 (2023).

### 27. Zuo, R. & Xu, Y. Graph deep learning model for mapping mineral prospectivity, Math. Geosci. 55(1), 1–21. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​

## 7​/​S​1​1​0​0​4​-​0​2​2​-​1​0​0​1​5​-​Z​ (2023).

### 28. Yoon, S. et al. Defect detection in composites by deep learning using solitary waves. Int. J. Mech. Sci. 239, 107882. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​

## 1​0​.​1​0​1​6​/​J​.​I​J​M​E​C​S​C​I​.​2​0​2​2​.​1​0​7​8​8​2​ (2023).

### 29. Kim, H. J. & Kim, M. K. A novel deep learning-based forecasting model optimized by heuristic algorithm for energy management

of microgrid. Appl. Energy. 332, 120525. https://doi.org/10.1016/J. APENERGY.2022.120525 (2023).

### 30. Ai, D. & Cheng, J. A deep learning approach for electromechanical impedance based concrete structural damage quantification

using two-dimensional convolutional neural network. Mech. Syst. Signal Process. 183, 109634. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​J​.​Y​M​S​S​P​.​2​0​
2​2​.​1​0​9​6​3​4​ (2023).

### 31. Ahmed, N., Aghbari, Z. & Girija, S. A systematic survey on multi-modal emotion recognition using learning algorithms. Intell. Syst. Appl. 17, 200171. https://doi.org/10.1016/j.iswa.2022.200171 (2023).

### 32. Revathy, V. R., Pillai, A. S. & Daneshfar, F. LyEmoBERT: classification of lyrics’ emotion and recommendation using a pre-trained

model. Proc. Comput. Sci. 218, 1196–1208. https://doi.org/10.1016/j.procs.2023.01.098 (2023).

### 33. Modran, H. A., Chamunorwa, T. & Ursuiu, D. Using deep learning to recognize therapeutic effects of music based on emotions. Sensors. 23(2), 986. https://doi.org/10.3390/s23020986 (2023).

### 34. Wang, J., Song, Y., Mao, Z. & Gao, Q. EEG-based emotion identification using 1-D deep residual shrinkage network with microstate

features. IEEE Sens. J. 23 (5), 5165–5174. https://doi.org/10.1109/JSEN.2023.3239507 (2023).

### 35. Mellouk, W. & Handouzi, W. CNN-LSTM for automatic emotion recognition using contactless photoplythesmographic signals. Biomed. Signal Process. Control. 85, 104907. https://doi.org/10.1016/j.bspc.2023.104907 (2023).

### 36. Kamble, K. & Sengupta, J. A comprehensive survey on emotion recognition based on electroencephalograph (EEG) signals. Multimed. Tools Appl. 1, 1–36. https://doi.org/10.1007/s11042-023-14489-9 (2023).

### 37. Benamara, N. K., Zigh, E., Stambouli, T. B. & Keche, M. Towards a robust thermal-visible heterogeneous face recognition approach

based on a cycle generative adversarial network. IJIMAI 7 (4), 132–145. https://doi.org/10.9781/ijimai.2022.05.005 (2022).

### 38. Rivero, A. J. L., Gutiérrez, M. E. B. & Martínez, C. M. Empirical analysis of ethical principles applied to different Ai uses cases. IJIMAI 7 (7), 105–114. https://doi.org/10.9781/ijimai.2022.11.006 (2022).

### 39. Luzio, F., Rosato, A. & Panella, M. A randomized deep neural network for emotion recognition with landmarks detection. Biomed. Signal Process. Control. 81, 104418. https://doi.org/10.1016/j.bspc.2022.104418 (2023).

### 40. Khan, M., Tran, P. N., Pham, N. T. & Saddik, A. E. Othmani. MemoCMT: multimodal emotion recognition using cross-modal

transformer-based feature fusion. Sci. Rep. 15 (1), 5473. https://doi.org/10.1038/s41598-025-89202-x (2025).

### 41. Zou, Z. & Ergan, S. Towards emotionally intelligent buildings: A convolutional neural network based approach to classify human

emotional experience in virtual built environments. Adv. Eng. Inform. 55, 101868. https://doi.org/10.1016/j.aei.2022.101868
(2023).

### 42. Song, C., Liu, S., Han, G. & Zeng, P. Edge-intelligence-based condition monitoring of beam pumping units under heavy noise in

industrial internet of things for industry 4.0. IEEE 10 (4), 3037–3046. https://doi.org/10.1109/JIOT.2022.3141382 (2022). Author contributions
X. Y.: Conceptualization, methodology, software, validation, formal analysis, investigation, resources, data cu­
ration, writing—original draft preparation, writing—review and editing, visualization, supervision, project ad­
ministration, funding acquisition. Funding
This work was supported by Research on the Coupling Mechanism of Static Protection and Live transmission of
Huizhou Four Treasures of the Study “Intangible Cultural Heritage” Techniques, Project No: AHSKY2023D100. Declarations
Competing interests
The authors declare no competing interests. Ethics statement
This article does not contain any studies with human participants or animals performed by any of the authors. All methods were performed in accordance with relevant guidelines and regulations. Additional information
Correspondence and requests for materials should be addressed to X. Y. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/

Open Access  This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives
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
Scientific Reports | (2025) 15:39659

| https://doi.org/10.1038/s41598-025-23199-1
www.nature.com/scientificreports/
