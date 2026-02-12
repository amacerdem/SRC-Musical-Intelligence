# The singing style of female roles

**Year:** D:20

---

The singing style of female roles
in ethnic opera under artificial
intelligence and deep neural
networks
Huixia Yang
With the rapid advancement of artificial intelligence technology, efficiently extracting and analyzing
music performance style features has become an important topic in the field of music information
processing. This work focuses on the classification of singing styles of female roles in ethnic opera
and proposes an Attention-Enhanced 1D Residual Gated Convolutional and Bidirectional Recurrent
Neural Network (ARGC-BRNN) model. The model uses a Residual Gated Linear Unit with Squeeze-
and-Excitation (RGLU-SE) block to efficiently extract multi-level features of singing styles and
combines a Bidirectional Recurrent Neural Network to model temporal dependencies. Finally,
it uses an attention mechanism for global feature aggregation and classification. Experiments
conducted on a self-constructed dataset of ethnic opera female role singing segments and the publicly
available MagnaTagATune dataset show that the classification performance of the ARGC-BRNN
model outperforms other comparison models. The model achieves an accuracy of 0.872 on the self-
constructed dataset and an Area Under Curve of 0.912 on the MagnaTagATune dataset. The proposed
model improves the results by 0.44% and 0.46%, respectively, compared to other models. The model
also demonstrates significant advantages in training efficiency. The results indicate that the ARGC-
BRNN model can effectively capture music singing style features, providing technical support for the
digital and intelligent analysis of ethnic opera art. Keywords  Singing style classification, Ethnic opera, Residual gated convolution, Bidirectional recurrent
neural network, Attention mechanism
Research background and motivations
Ethnic opera, as a unique art form, profoundly reflects the diversity of national culture, language, and music. In particular, the singing styles of female roles often encompass complex emotional expressions and sound
characteristics. In ethnic opera, female roles are required not only to display subtle emotional shifts but also to
possess rich vocal techniques and artistic expressiveness. Given that the musical structure of ethnic opera differs
significantly from Western opera and other types of traditional Chinese opera, the singing styles of female roles
present unique technical and artistic features1–3. However, traditional analysis of singing styles often relies on
subjective experience, lacking systematic and objective methods. This issue becomes even more challenging in
the recognition of diverse and highly complex singing styles4–6. With the rapid development of Artificial Intelligence (AI) technologies, deep learning, particularly the Deep
Neural Network (DNN), has shown great potential in the fields of audio analysis and processing7,8. In recent
years, DNN models such as Convolutional Neural Network (CNN) and Recurrent Neural Network (RNN) have
achieved significant success in music style classification and emotion recognition tasks9,10. However, despite
their widespread application in the analysis of Western music and popular songs, the effective application of
these technologies in the field of ethnic opera remains an unresolved challenge. This is particularly obvious in the
analysis of the singing styles of female roles. Research in this area not only contributes to advancing theoretical
developments in musicology and vocal studies but also provides scientific support for opera performers’ training,
thereby improving the quality of performances. Therefore, this work aims to explore how AI-assisted DNN
technologies can play a role in the study of singing styles for female roles in ethnic opera. Xingzhi College, Zhejiang Normal University, Jinhua 321000, China. email: m13868991959@163.com
OPEN
Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports

Research objectives
The main objective of this work is to develop an innovative CNN-RNN model based on AI technology to assist
in the analysis and recognition of singing styles for female roles in ethnic opera. Specifically, the work aims to
achieve the following objectives: (1) design and implement a hybrid model that integrates gating mechanisms,
residual connections, and attention mechanisms to automatically extract multi-level features of singing style
from audio signals; (2) utilize the temporal learning capabilities of Bidirectional Recurrent Neural Network
(BRNN) to further capture emotional changes and rhythmic features in the singing style; (3) optimize the model’s
feature learning process using the attention mechanism, and assign different weights to audio data from different
time segments to more accurately identify subtle differences in the singing style. This work aims to provide new
technological pathways and theoretical foundations for the systematic analysis and digital expression of the
singing styles of female roles in ethnic opera. Literature review
In recent years, AI technology has made breakthrough advancements across various fields. For example, Li et
al. studied the impact of AI on corporate innovation efficiency using data from 3,185 listed companies. They
found that AI significantly enhanced innovation efficiency, particularly in environments with intense market
competition and flattened organizational structures11. Wang et al. built a recommendation and resource
optimization model for cultural and creative industry-related entrepreneurial projects using neural network
algorithms. Their model evaluation revealed that as the training period increased, the recognition accuracy
reached 81.64%. Additionally, the prediction error of the recommendation system was minimized when the
word vector length and number of hidden features were set to 20012. El Ardeliya et al. explored the application of
AI in generative arts, music creation, and design. They analyzed how AI drove transformative changes in creative
fields and emphasized its revolutionary potential in enhancing human creativity13. Deep learning technology has demonstrated powerful feature extraction and pattern recognition capabilities
in music classification tasks, gradually becoming a mainstream method in this field. Prabhakar and Lee (2023)
proposed five new music genre classification methods. They included a weighted visual graph-based elastic net
sparse classifier, stacked denoising autoencoders, Riemannian alliance transfer learning, transfer support vector
machine algorithms, and a deep learning model combining two networks. They found that deep learning models
achieved the highest classification accuracy14. Faizan et al. compared the performance of Long Short-Term
Memory (LSTM), CNN, and CNN-LSTM models, and found that the CNN-based music genre classification
system performed the best15. Mehra et al. introduced a multimodal music representation method based on
spectrograms and lyrics. They used deep learning models to encode songs and perform multi-genre classification
experiments. Their research showed that the simple linear combination of spectrograms and lyrics outperformed
using either one alone in terms of classification accuracy16. Despite the progress made in music classification, there are still some shortcomings. Many models have failed
to fully incorporate temporal information and global features, resulting in limited classification performance. Furthermore, the application of attention mechanisms is not widespread, and key temporal differences have not
been effectively captured. To address these issues, this work proposes a hybrid model based on residual gated
convolution and BRNN, and incorporates an attention mechanism to improve the accuracy of singing style
classification. Research model
Overview of the singing style classification model architecture
Existing music classification models often face challenges when dealing with complex spectrogram features
and long-term dependencies. These challenges include insufficient capture of key features and difficulties
in effectively filtering redundant information, which limits their application in the classification of ethnic
opera singing styles17. Specifically, traditional CNN may excessively focus on detailed features during feature
extraction, making it difficult to handle the multi-level temporal dependencies in singing styles. While RNN
has certain advantages in handling temporal dependencies, it is prone to the vanishing gradient problem when
capturing long-term dependencies, which limits the model’s performance. Therefore, to address these issues,
this work proposes an Attention-Enhanced 1D Residual Gated Convolutional and Bidirectional RNN (ARGC-
BRNN) model. The model combines the Residual Gated Linear Unit with Squeeze-and-Excitation block (RGLU-
SE) and BRNN, and incorporates an attention mechanism to efficiently extract and aggregate multi-level features
of singing styles. The reason for adopting this structure is that, on the one hand, the residual gated convolutional units can
effectively capture multi-level local features while avoiding the vanishing gradient problem. This can enhance
the model’s performance when dealing with complex sequential data. This work has incorporated the Squeeze-
and-Excitation (SE) module, allowing the network to automatically focus on important feature channels, which
further strengthens the feature extraction process. Additionally, the BRNN can model contextual information
in the time series through both forward and backward propagation of the input data, which is crucial for
capturing time-dependent features such as pitch and rhythm in operatic singing. When processing audio data
with significant temporal characteristics, the bidirectional structure of the BRNN enables a more comprehensive
understanding of the data sequence. The attention mechanism dynamically focuses on the most relevant parts
of the input data, effectively improving the model’s performance during the global feature aggregation process. In the proposed model, the attention mechanism helps the model better understand which audio segments are
most important for the classification task, resulting in significant advantages in both classification accuracy and
training efficiency. Figure 1 illustrates its architecture. In Fig. 1, the ARGC-BRNN model is divided into three layers based on the functions of each part and the
sequence of information transmission: the music representation learning layer, the music sequence modeling and
Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

sequence feature aggregation layer, and the fully connected classification layer. The entire architecture is designed
around the feature extraction and sequence modeling requirements for the vocal styles of female characters in
Chinese national opera. It focuses on targeted structural optimization and integration of the residual gated
convolution units (RGLU) and BPNN to enhance the model’s performance in complex spectral feature extraction
and temporal dependency modeling. On the one hand, this work proposes the RGLU-SE module, which involves
multiple improvements to the traditional gated convolution structure. This module integrates one-dimensional
convolution, gating mechanisms, residual connections, channel attention mechanisms (SE), and max pooling
operations, forming a deep structure with strong capabilities in extracting local frequency features and channel
selectivity. The one-dimensional convolution is responsible for extracting shift-invariant local frequency features
from the audio signal, while the gating mechanism dynamically suppresses redundant information at the feature
level, highlighting key stylistic elements. On this basis, residual connections are introduced to enhance the deep
propagation ability of the network and mitigate the vanishing gradient problem during training. Furthermore,
by incorporating the SE attention mechanism, the model learns the dependencies between different channels
and selectively enhances the frequency bands related to the singing style. This improves the model’s ability to
perceive subtle differences between different style features. Max pooling reduces dimensionality while expanding
the receptive field, making the model more efficient and robust when processing complex spectrograms. On the other hand, after feature extraction, the resulting high-dimensional semantic feature map is unfolded
into a time series and input into the BRNN. Unlike traditional methods that model based on raw audio, this
work uses the high-level features extracted by convolution-attention as inputs to the BRNN, improving the
information density and expression efficiency of the temporal modeling. The BRNN structure can capture both
historical and future contextual information, making it suitable for the complex singing rhythm and emotional
changes in national opera. The work also integrates the attention mechanism to perform weighted aggregation
on the BRNN output. It allows the model to automatically focus on the most representative time nodes in the
singing segments, thereby achieving a more precise and globally consistent style representation. Finally, this
global feature vector is passed to the fully connected layer to complete the classification task. In summary, the ARGC-BRNN model, through the deep integration and structural optimization of
residual gated convolution units and BRNN, enhances the hierarchy of spectral information extraction, the
completeness of temporal dependency modeling, and the accuracy of overall style classification. It overcomes
the expressive bottleneck of traditional methods when dealing with the complex musical structure of national
opera, demonstrating good performance and application potential. Analysis of the residual gated convolutional unit structure
In the music classification task, the RGLU-SE module addresses the problems of gradient vanishing and network
degradation by integrating gated convolution units, 1D convolution, residual connections, channel attention
mechanisms, and max pooling layers18. The 1D convolution effectively captures the translational invariance
of frequency features while reducing computational load. The gating mechanism ensures that only category-
relevant information is retained, filtering out irrelevant data. Residual connections help alleviate network
degradation and enhance the network’s ability to selectively retain meaningful features. The SE structure
Fig. 1. Schematic diagram of the ARGC-BRNN model structure. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

implements a channel-level attention mechanism that automatically learns the importance of spectral features
across different channels. The max pooling layer reduces the size of the feature maps and expands the receptive
field of the convolution kernel in the time domain, aiding in the extraction of deeper features. As shown in Fig. 2,
the RGLU-SE module consists of two residual gated convolution units, an SE structure, and a max pooling layer. In Fig. 2, the core of the residual gated convolutional unit is the Gated Linear Unit (GLU). GLU selectively
retains key features by performing a pointwise multiplication of linear transformations and nonlinear
activations19,20. The input spectrogram sequence is set to X = [x1, x2, · · ·, xn], and the output of the GLU
can be expressed as: YGLU = Conv1D1 (X) ⊙σ (Conv1D2( X )).
(1)
Conv1D1 and Conv1D2 represent two distinct 1D convolution operations, ⊙ denotes element-wise
multiplication, and σ is the sigmoid activation function. In this mechanism, Conv1D1 (X) represents the
linear transformation of the initial features, while σ (Conv1D2( X )) models the importance of feature
selection via the sigmoid function, effectively adding a “gating” operation to each feature channel. This design
allows for the selective retention of important information relevant to the target classification task, while filtering
out irrelevant or redundant information. As the number of layers in DNN increases, the issue of gradient vanishing or network degradation becomes
more prominent. The introduction of residual networks offers an effective solution by incorporating identity
mappings at each layer, allowing information to bypass certain convolutional layers and flow directly to subsequent
layers. This prevents features from being excessively transformed or attenuated in deep networks21,22. In the
RGLU-SE, the residual structure is integrated into the gated convolutional unit. Its mathematical expression is: Y = X + Conv1D1 (X) ⊙σ (Conv1D2( X )).
(2)
X represents the input features, and Y denotes the final output features. This structure allows the original input
features to directly participate in the computations of subsequent layers, while utilizing convolution and gating
mechanisms to extract deeper features. Within this framework, the network’s training process becomes more
stable and can alleviate the vanishing gradient problem during backpropagation23. Further derivation yields: Y = (1 −σ ) · X + σ · Conv1D1 (X).
(3)
From the above equation, it is clear that there are two paths for information flow. One is the direct transmission
of the original features X with a probability of 1 −σ, and the other is the transmission of features after
convolution and gating operations with a probability of σ. This characteristic allows the network to flexibly
propagate information across multiple channels, effectively enhancing its feature expression capability. In terms of the channel dimension, different spectral features have varying levels of importance for the
classification task. To better allocate the weight among the channels, the RGLU-SE integrates a SE module. The
SE module consists of two parts: Squeeze and Excitation24. The Squeeze operation reduces the dimensionality
through global average pooling, and the calculation equation is:
wc =

## H · W

∑
H
i=1
∑
W
j=1xijc.
(4)
H and W represent the time and frequency dimensions of the feature map, xijc denotes the feature value of a
specific channel, and wc is the weight of channel c. This process extracts important statistical information from
each channel. Fig. 2. Schematic diagram of the RGLU-SE structure. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

The excitation operation generates weights sc through two fully connected layers and activation functions
(ReLU and sigmoid), and these weights are then used to recalibrate the original channel features. The calculation
for the excitation step is as follows:
x′
ijc = sc · xijc.
(5)
This channel-level dynamic attention adjustment allows the RGLU-SE block to adaptively enhance discriminative
features based on the characteristics of different music genres. To further optimize feature extraction, RGLU-SE
incorporates a max pooling layer at the end of its structure. The max pooling layer reduces the feature map size. This not only lowers the model’s computational complexity but also indirectly expands the receptive field of the
convolution kernels, thereby helping to capture deeper patterns across the time dimension25. Modeling temporal dependencies with BRNN
Music signals are highly time-dependent sequential data. The classification tasks not only rely on features
from individual time points but also need to consider the global temporal context to capture deeper musical
patterns26. To better model the bidirectional temporal dependencies within the music sequence, this work
employs a BRNN, and simultaneously considers the past and future features at the current time step, enabling
comprehensive modeling of musical patterns. Traditional RNN captures temporal dependencies by recursively
updating the hidden state. The mathematical expression is:
ht = f(Whht−1 + Wxxt + bh).
(6)
Wh and Wx represent the weight matrices for the hidden state and input, respectively. bh is the bias term,
and f(· ) is the activation function. However, a unidirectional RNN can only capture dependencies from the
past to the present, while information from future time steps is equally important for understanding the music
sequence27. The BRNN consists of two recurrent networks: a forward and a backward network. At time step t,
the forward and backward hidden states are calculated by the following equations:
−→
ht = f(Wh
−−→
ht−1 + Wxxt + bh)
(7)
←−
ht = f(W ′
h
←−−
ht−1 + W ′
xxt + b′
h).
(8)

## W ′

h, W ′
x, and b′
h represent the weight matrices and bias term for the backward network. The forward and
backward networks do not share weights, allowing them to learn temporal dependencies in different directions. The final output is obtained by summing or concatenating, yielding the BRNN output ot:
ot = U−→
ht + U′ ←−
ht + bo.
(9)
Here, U and U ′ represent the output weight matrices for the forward and backward hidden states, respectively,
and bo is the output bias term. To feed the high-level features extracted by the CNN into the BRNN, a feature sequence construction method
is designed. The feature maps generated by the convolutional layers have already been processed along the time
dimension by the sliding of the convolutional kernels, capturing feature responses at different time points. In
constructing the input sequence, each column of the feature map is treated as the input for a time step. Each
column contains the convolution results of all the kernels at that specific time point. It is set that the dimension of
the convolution feature map is C × W × H. C is the number of convolutional kernels, and W and H represent
the size along the time axis and frequency axis, respectively. Figure 3 illustrates the steps of the feature sequence
construction. In Fig. 3, the convolutional feature map is first scanned column by column in temporal order. Then, the
responses of the C convolutional kernels in each column are concatenated into a feature vector, which represents
the input for that time step. After this process, the feature map is transformed into a time series of length W. The
input dimension for each time step is C. This input format is more aligned with the modeling requirements of
the BRNN, enabling effective use of the local features captured by the convolutional layer while further learning
the temporal dependencies within the sequence. Integration of attention mechanism
After the BRNN models the music feature sequence, the features generated at each time step describe the deep
characteristics of the music at different time points. The attention mechanism assigns weights to each time step,
dynamically adjusting the contribution of features from different time steps to the classification task28–30. The
output feature sequence of the BRNN is represented as X = [x1, x2, · · ·, xL], where L is the number of time
steps, and xt ∈Rd is the feature vector at each time step. The calculation equation for the attention weight at
is:
at = softmax (W2ϕ ( W1xt )).
(10)
W1 and W2 are the learned weight matrices, and ϕ (· ) represents the tanh activation function. The Softmax
function ensures the normalization of the weights at, such that the sum of the weights across all time steps
equals 1: Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

∑
L
t=1at = 1.
(11)
After obtaining the attention weight vector A = [a1, a2, · · ·, aL], the features from all time steps are aggregated
through a weighted sum to obtain the global feature representation:

## V =

∑
L
t=1atxt = AX.
(12)
V ∈Rd is the aggregated global feature vector, which dynamically represents the important information
within the sequence. The aggregated global feature V is then fed into a fully connected layer. Further integration and selection are
performed through linear transformations and activation functions, generating high-level feature representations
for the classification task. The attention mechanism refines the aggregation process through dynamic weight
adjustment, enabling the modeling of discriminative global features. Experimental design and performance evaluation
Datasets collection
This work conducts experiments using two datasets: the publicly available MagnaTagATune dataset and a self-
built dataset, the Self-built Ethnic Opera Female Role Singing Excerpt Dataset (SEOFRS). The MagnaTagATune
dataset is a widely used public dataset for music classification and tag prediction research. It contains over
25,000 music clips, each 29 s long, and is annotated with various labels, such as emotion, instruments, and
genre information. All audio files are processed to mono format and resampled at a 16 kHz sampling rate. When converted to Mel spectrograms, the window length for the Fourier transform is set to 512. It has a sliding
window step size of 256 and 128 frequency bins, resulting in a final Mel spectrogram size of (1813, 128). The SEOFRS dataset focuses on traditional Chinese opera and comprises vocal segments performed by
multiple female singers, covering various character types and emotional expressions. All audio samples adhere
to the following standards: First, high-quality, uncompressed audio is selected to ensure vocal features are clearly
identifiable. Besides, performance clips are chosen from a range of traditional opera character types, capturing
diverse emotional expressions and singing techniques. This ensures the dataset’s diversity and representativeness,
with balanced samples to avoid overrepresentation of any single category. During data preprocessing, all audio
files are first converted to mono format and standardized to a 16 kHz sampling rate to ensure consistency in
the frequency range of the audio data, thereby enhancing the stability and effectiveness of subsequent feature
extraction. Next, the audio segments are split into fixed time intervals, with each segment having a duration of 5 s. This
duration is chosen considering the characteristics of ethnic opera singing, as it captures enough variation in
sound while ensuring the dataset’s operability and training efficiency. All audio samples, after being cut, are
further processed into Mel spectrograms, which serve as features for input into the deep learning model. The
generation of Mel spectrograms uses common audio signal processing methods, including Fourier transforms
and the application of Mel filter banks. During this process, the window length is set to 512, the window sliding
step to 256, and the frequency bin count to 128. The generated Mel spectrograms have dimensions of (313
and 128), which meet the common requirements for processing sequential audio data. Mel is chosen as the
primary input feature due to its strong perceptual relevance and computational efficiency in the fields of music
Fig. 3. Construction process of convolutional feature sequence. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

and vocal analysis. In the preliminary experiments, in addition to the Mel spectrogram, other commonly used
audio features such as Mel-Frequency Cepstral Coefficients (MFCC) and Chroma features are also explored
and compared. The experimental results show that the Mel spectrogram can better capture the subtle frequency
changes when dealing with the emotional expressions and vocal techniques of female characters in ethnic
operas. It outperforms other features, especially in terms of emotion and timbre recognition. Table 1 presents
the experimental results obtained using the Mel spectrogram, MFCC, and Chroma features: The results in Table 1 indicate that the Mel spectrogram achieves an AUC of 0.912 on the MagnaTagATune
dataset and an accuracy of 0.872 on the SEOFRS dataset, both of which are higher than those of MFCC and
Chroma features. This demonstrates that the Mel spectrogram can better extract and represent the key features
of speech. Especially when recognizing the timbre and emotional changes of female characters in ethnic operas,
its performance is more outstanding. Therefore, the Mel spectrogram is ultimately selected as the main input
feature for this study. The Mel scale is constructed based on the human auditory system’s sensitivity to different
frequency bands, making it more aligned with how the human ear perceives sound during actual listening. This
makes it particularly suitable for capturing variations in pitch, timbre, and intensity throughout the singing
process. In the context of female vocal styles in traditional opera, emotional expression and vocal techniques
are often accompanied by subtle and complex frequency changes. The Mel spectrogram can effectively capture
key frequency-band information within these changes, thus providing more discriminative input features for
subsequent style classification tasks. To ensure the reliability and generalization of the data, all audio samples undergo strict quality control after
splitting and processing. All audio segments are manually reviewed to ensure they are free from background
noise, recording distortion, or other non-compliant issues. In the final construction phase of the dataset, all
audio samples are divided into training, validation, and test sets with a ratio of 8:1:1. Additionally, to enhance
the model’s generalization ability, the data are repeatedly split 10 times to perform ten-fold cross-validation. This approach not only ensures the balance of categories in the dataset but also helps the model better cope with
potential overfitting issues during training. Experimental environment and parameters setting
Tables 2 and 3 shows the experimental environment and parameter settings for this work. In this experiment, the selection of hyperparameters is determined through extensive tuning and aligns
with best practices documented in current deep learning optimization literature. A small-scale grid search is
conducted to determine the optimal values, focusing primarily on key hyperparameters such as hidden layer
size, learning rate, and batch size. The work tests hidden layer sizes of [64, 128, 256], learning rates in the range
of [0.001, 0.01, 0.1], and batch sizes of [32, 64, 128], exploring different combinations. Through this grid search
process, the optimal configuration for each model is identified. The goal in selecting these parameters is to
maximize model performance while ensuring efficient use of computational resources. For the convolutional
layer configuration, 1D convolution is used, which proves highly effective for processing one-dimensional time-
series data. The number of convolution kernels is set to 64 and 128. This is an optimal setting determined through
experimentation, aiming to balance feature extraction capability with computational efficiency. A kernel size
of 3 × 1 is chosen to effectively capture local frequency characteristics while maintaining low computational
complexity. The convolution stride is set to 1 to ensure accurate feature extraction at each time step. In terms
of the gating mechanism, the RGLU is employed, integrating a gating structure with a SE module. The gating
mechanism enables the network to selectively retain important features and suppress redundant information,
while the SE module dynamically adjusts channel-wise feature weights to enhance the model’s performance
across different feature dimensions. ReLU is chosen as the activation function for the gating unit to enhance the
model’s nonlinear representation capabilities. The BRNN is configured with two layers and 128 hidden neurons. This is an optimal setup derived from
repeated experiments, allowing the model to effectively capture the temporal dependencies in vocal performance
Environment
Configuration
Operating System
Windows10
Central Processing Unit (CPU)
Intel(R) Xeon(R) Silver 4210@2.20 GHz
Memory
64G
Graphics Processing Unit (GPU)

## NVIDIA RTX 2080

Programming Language
Python3.6
Table 2. Experimental environment. Feature type
MagnaTagATune dataset AUC
SEOFRS dataset accuracy
Mel spectrogram
0.912
0.872
MFCC
0.876
0.850
Chroma
0.884
0.863
Table 1. Comparison of results of different audio features. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

styles. Tanh is used as the activation function for each layer and it can smoothly handle long-term dependencies
in sequential data. The design of the fully connected layers takes into account the need for feature fusion. The
first layer is set to 200 neurons and the second to 100 neurons. The number of neurons is progressively reduced
to prevent overfitting while maintaining computational efficiency. To further mitigate overfitting, a dropout
rate of 0.2 is applied, which is an optimal value verified through repeated experiments. The optimizer used is
Adam, a widely adopted adaptive optimization algorithm that effectively improves model convergence speed. The batch size is set to 16, a choice that balances computational resource constraints with convergence speed
during training. The selection and adjustment of these parameters rely primarily on experimentation and cross-
validation, ensuring the model achieves optimal performance across different configurations while avoiding
overfitting and enhancing computational efficiency. The classification accuracy (Acc) and Area Under Curve (AUC) are selected as the evaluation metrics for
the proposed music performance style classification method. The classification accuracy is calculated as follows: Acc = N0

## N × 100%.

(13)
N represents the total number of audio samples in the test set, and N0 denotes the number of audio samples
correctly classified by the classifier. Since the MagnaTagATune dataset is a multi-label classification dataset, Recall@k is also used as an evaluation metric to more comprehensively evaluate the model’s performance,. The
calculation is as follows: Recall@k = |Y ∩R1:k|

## |Y |.
(14)
Here, Y represents the actual label set of the test samples, and R1:k denotes the set of the top k labels sorted by
the predicted probabilities from the model, in descending order. Performance evaluation
(1)	 Impact of structure on model performance
First, the effectiveness of the RGLU-SE module is verified. The convolutional network part of the model is
replaced with other forms of convolutional modules, while keeping the rest of the architecture unchanged. The
convolutional modules include CNN, GLU, CNN with residual structure (Residual CNN, RCNN), and GLU
with residual structure (Residual GLU, RGLU). The BRNN memory unit type is selected as LSTM. Experiments
are conducted on both datasets. Figure 4 shows the results. Figure 4 shows that the RGLU-SE module achieves significant performance improvements over other
convolutional structures on both datasets. On the SEOFRS dataset, RGLU-SE achieves an accuracy of
0.872, outperforming CNN, GLU, RCNN, and RGLU by 2.5%, 1.7%, 1.3%, and 1.1%, respectively. On the
MagnaTagATune dataset, RGLU-SE achieves an AUC of 0.912, which is an improvement of 1.5%, 1.3%, 1.4%,
and 0.5% over CNN, GLU, RCNN, and RGLU, respectively. This demonstrates that the RGLU-SE module has
strong generalization capability and is more effective than other convolutional structures in extracting music
Parameter
Configuration/value
Convolution Layer Type
1D Convolution
Number of Convolution Kernels
64 (first layer), 128 (second layer)
Kernel Size
3 × 1
Stride

Gating Mechanism
RGLU
Gating Module
Gating Mechanism with SE Module
Gating Activation Function
ReLU
Number of Channels in SE Module
Same as the number of convolution kernels
Number of Hidden Neurons in BRNN Memory Units

Number of BRNN Layers
2 layers
BRNN Activation Function
Tanh
Number of Neurons in Fully Connected Layers
First layer: 200; Second layer: 100
Activation Function for Fully Connected Layers
ReLU
Dropout Rate in Fully Connected Layers
0.2
Optimizer
Adam
Batch Size

Loss Function for Single-label Classification
Cross-Entropy Loss
Loss Function for Multi-label Classification
Binary Cross-Entropy Loss
Table 3. Parameter settings. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

features. This performance improvement is mainly attributed to the design of the residual gated convolutional
units in the RGLU-SE module. It allows the model to more effectively filter out irrelevant information while
the channel attention mechanism enhances its focus on key features. As a result, the model’s ability to represent
complex musical data and its classification accuracy are significantly improved. The strength of this module
enables the proposed model to better capture the multi-level features of female vocal styles in ethnic opera,
ultimately leading to superior classification performance. Next, the impact of the RNN structure on the performance of the ARGC-BRNN model is compared. The
performance of models with one and two layers of Gated Recurrent Unit (GRU), LSTM, Bidirectional GRU
(BGRU), and Bidirectional LSTM (BLSTM) is compared on the two datasets. Figure 5 displays the results. Figure 5 reveals that different RNN structures have varying impacts on the performance of the ARGC-
BRNN model. On the SEOFRS dataset, a 1-layer BLSTM structure achieves the highest accuracy of 0.872. On
the MagnaTagATune dataset, BLSTM also demonstrates the best performance, with an AUC of 0.912. Overall, BRNN (BGRU and BLSTM) have certain advantages in capturing sequence context information, especially
in more complex datasets, where BLSTM performs particularly well. This phenomenon suggests that BLSTM
can better model long-range dependencies in the sequence by processing information in both the forward
and backward directions of the sequence. Especially in complex singing style sequences, BLSTM is able to
capture more contextual information, which leads to superior performance in classification tasks. Compared
to traditional unidirectional RNN structures, BLSTM has a stronger contextual modeling capability, enabling
the model proposed to achieve better results when handling the singing styles of female roles in ethnic opera.
(2)	 Comparison of ARGC-BRNN with other models
On the two datasets, the performance of the Timbre CNN, End-to-end, Convolutional RNN (CRNN), CRNN
with Temporal Features (CRNN-TF), RGLU-SE, as well as the models in references16 and 31 is compared with
that of the proposed ARGC-BRNN model. The Timbre CNN is a timbre recognition model based on the CNN,
focusing on the extraction of local patterns in the audio. The End-to-end is a model that directly inputs the audio
signal into a deep neural network for end-to-end training. The CRNN is a method that combines the CNN and
the RNN, enabling the extraction of both local and time series features. The CRNN-TF enhances the ability to
model temporal features on the basis of the CRNN. The RGLU-SE is a model that combines the residual gated
linear unit with the Squeeze-and-Excitation mechanism to improve the multi-level feature extraction ability. The model in reference16 uses a multi-modal spectrogram-lyric embedding method, combining deep visual and
language models to achieve music style classification, emphasizing the joint representation of audio and lyrics. The model in reference31 is a model based on functional data analysis, using the latent representation of the
original audio to classify the style of traditional Irish music, emphasizing the capture of cultural and structural
features. Table 4 presents the results. Fig. 4. Performance comparison of different convolutional structures on datasets. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

To provide a more intuitive comparison of the performance of each model, Fig. 6 is drawn based on Table 4. Table 4; Fig. 6 show that on the MagnaTagATune dataset, the ARGC-BRNN model achieves an AUC of 0.912
and performs excellently in Recall@k, demonstrating its strong global feature recognition ability. Compared to
Timbre CNN, End-to-End, CRNN, CRNN-TF, and RGLU-SE, the AUC of ARGC-BRNN is improved by 2.13%,
3.52%, 2.13%, 0.44%, and 1.45%, respectively. On the SEOFRS dataset, ARGC-BRNN achieves an accuracy of
0.872, which is at least 0.46% higher than the other models, indicating its good classification ability on this
dataset. All the results are better than those in reference16 (SEOFRS accuracy is 0.861, AUC on MagnaTagATune
is 0.905) and reference31 (SEOFRS accuracy is 0.830, AUC on MagnaTagATune is 0.887). Overall, ARGC-
BRNN performs exceptionally well on both datasets, proving its superiority in the music performance style
classification task. These relatively small improvements still hold significant value in practical applications. First, these enhancements demonstrate that ARGC-BRNN can more accurately capture and recognize multi-
level features in complex music singing style classification tasks. In particular, when the dataset has higher
diversity and complexity, the model’s classification capability is improved. Second, the impact of these small
improvements in real-world applications should not be overlooked. In environments with high-dimensional
features and significant noise, even slight performance boosts can effectively improve the model’s robustness and
stability, ensuring more reliable classification results. Therefore, these results suggest that ARGC-BRNN holds
considerable practical value and application potential for the automated analysis of music singing styles. Models
MagnaTagATune dataset
SEOFRS dataset
AUC
Recall@1
Recall@3
Recall@5
Recall@10
Acc
Timbre CNN
0.893
0.285
0.534
0.664
0.829
0.857
End-to-end
0.881
0.29
0.5345
0.667
0.836
0.824
CRNN
0.893
0.304
0.561
0.692
0.854
0.789
CRNN-TF
0.908
0.32
0.579
0.715
0.873
0.78
RGLU-SE
0.899
0.295
0.55
0.712
0.861
0.868
Reference31
0.905
0.315
0.572
0.719
0.875
0.861
Reference32
0.887
0.29
0.548
0.685
0.845
0.83
ARGC-BRNN
0.912
0.327
0.561
0.727
0.882
0.872
Table 4. Performance comparison of different models. Fig. 5. Performance comparison of different RNN structures on datasets. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

Additionally, Fig. 7 shows a comparison of accuracy, recall, and F1 score results for each model on the
SEOFRS dataset. Figure 7 suggests that the ARGC-BRNN model performs exceptionally well across all metrics on the SEOFRS
dataset. It achieves accuracy, recall, and F1 scores of 0.874, 0.869, and 0.871, respectively, all surpassing the other
comparative models. This indicates that ARGC-BRNN effectively balances accuracy and recall in classification
tasks, particularly in the classification of ethnic opera female character singing styles, demonstrating strong
discrimination ability. The superior performance can be primarily attributed to the ARGC-BRNN model’s
ability to better extract and model singing style features through the combination of the RGLU-SE module and
BRNN structure. First, the RGLU-SE module enhances feature extraction efficiency and robustness through the
integration of residual gated convolution units and channel attention mechanisms, effectively capturing subtle
differences in singing styles. Additionally, the BRNN structure (particularly the BLSTM) is capable of capturing
temporal information from both forward and backward directions. This enables the model to have stronger
contextual modeling capabilities when processing complex musical data, especially in handling long-range
dependencies. As a result, ARGC-BRNN can effectively balance accuracy and recall. This ensures the model’s high
discrimination between different styles while also avoiding the loss of sensitivity to minority class samples
due to overfitting. This makes the model excel in classification tasks. These design choices provide significant
advantages in classifying the singing styles of female roles in ethnic opera. Figure 8 shows the confusion matrix
for the ARGC-BRNN model on different emotional singing styles in the SEOFRS dataset. From the confusion matrix in Fig. 8, it can be observed that the ARGC-BRNN model performs well in
recognizing different emotional singing styles. For the five emotions, “Calm,” “Joy,” “Anger,” “Sadness,”
and “Excited,” the model is able to accurately predict the correct emotion most of the time. However, some
misclassifications still occur. For example, 8% of “Calm” samples are misclassified as “Joy,” and 10% of “Joy”
samples are misclassified as “Calm.” These misclassification rates are relatively low, indicating that the model
has a strong ability to differentiate between emotions, but there is still some confusion when classifying similar
emotions. Finally, a comparison of the model parameters and training time for CRNN, CRNN-TF, and ARGC-
BRNN on the MagnaTagATune dataset is made. The results can be attributed to the ARGC-BRNN model’s
exceptional ability in emotion feature extraction and modeling. First, the model incorporates the RGLU-
SE module, which effectively enhances the extraction of emotional features through gating and attention
Fig. 6. Comparison of performance results across different models. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

mechanisms, allowing it to highlight the prominent emotional characteristics. Additionally, the BRNN structure,
particularly the BLSTM, captures bidirectional information in the time series, which is crucial for classifying
emotional singing styles, as emotions often exhibit temporal dependencies. While the model can distinguish
most emotions, occasional misclassification occurs when emotional features are closely similar, which remains a
common challenge in emotion classification tasks. The parameters and training time of CRNN, CRNN-TF and
ARGC-BRNN on MagnaTagATune dataset are compared. Figure 9 shows the results. Figure 9 demonstrates that the CRNN model has the smallest number of parameters, totaling 390,000, with
a training time of 5.1 h. The CRNN-TF model has a larger parameter count, reaching 1 million, with a training
time of 5.8 h. In contrast, the ARGC-BRNN model has the largest number of parameters, totaling 4.74 million,
but its training time is only 3.6 h. Although the number of parameters in the ARGC-BRNN model is significantly
higher than that of CRNN and CRNN-TF, its training time is considerably shorter due to the use of a 1D
convolutional structure. This is mainly attributed to the design of the gated convolutional structure. Compared
to traditional CNN, the ARGC-BRNN model introduces gating mechanisms and residual connections, which
effectively enhance the computational efficiency of the convolutional layers and reduce unnecessary computation. As a result, while maintaining high model performance, the training time is optimized. Therefore, despite the
larger number of model parameters, the design of the gated convolution significantly shortens the training time,
and demonstrates the model’s advantage in computational efficiency. This design allows the ARGC-BRNN to
maintain relatively low training time costs while achieving high performance levels when handling complex
tasks.
(3)	 Ablation experiment and results
To validate the contribution of each key module in the ARGC-BRNN model to the overall performance, a series
of systematic ablation experiments are conducted. This work progressively trims the model structure to assess
the practical impact of different modules on the vocal style classification task. The experiments are primarily
based on the custom-built dataset of ethnic opera female character vocal segments, and the evaluation metrics
were accuracy and AUC value. The following model variants are constructed for comparison: Baseline-CNN: Uses a traditional 1D
convolutional network without gating, residual, or attention mechanisms. Residual: Removes the residual
connection from the RGLU module. Gate: Removes the gating mechanism from the RGLU module. SE: Fig. 7. Accuracy comparison of different models on the SEOFRS dataset. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

Fig. 9. Comparison of different model parameters and training time. Fig. 8. Confusion matrix on the SEOFRS dataset. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

Removes the Squeeze-and-Excitation channel attention mechanism from the RGLU module. BRNN: Removes
the BRNN structure, keeping only the convolutional features. Attention: Removes the final attention-based
feature aggregation module. ARGC-BRNN (Full Model): Retains all modules as a performance upper bound
reference. Table 5 shows the results of the ablation experiments. As shown in Table 5, the complete ARGC-BRNN model achieves optimal performance in both accuracy and
AUC, with values of 0.872 and 0.912, respectively, demonstrating the synergistic advantages of all the modules. In contrast, models with key modules removed show varying degrees of decline in accuracy and AUC, proving
the critical importance of these modules for overall performance. After removing the residual connection,
the model’s accuracy decreases by about 0.29%, and the AUC drops by 0.026. The residual connection plays a
vital role in alleviating the vanishing gradient problem and feature degradation in deep networks, facilitating
effective information propagation and further feature extraction. Without the residual connection, the network
struggles to consistently pass low-level information, leading to a reduction in feature representation capability,
which negatively impacts the model’s classification performance. After removing the gating mechanism, the
accuracy drops by about 0.33%, and the AUC decreases by 0.030. The gating mechanism dynamically adjusts
the information flow, helping the network filter out irrelevant or redundant features. In complex acoustic
environments, especially in ethnic opera with its varying timbres and complex vocal techniques, the gating
mechanism helps emphasize crucial information. Its removal weakens the network’s ability to selectively process
information, reducing the model’s accuracy. After removing the SE module, the model’s accuracy drops by about 0.27%, and the AUC decreases by
0.025. The SE module models the inter-channel dependencies and dynamically adjusts the importance of each
channel, thereby enhancing focus on key frequency bands. In ethnic opera, subtle differences in timbre and
pitch often define the vocal style, and the removal of the SE mechanism reduces the model’s ability to capture
these crucial features, affecting the final classification performance. After removing the BRNN structure, the
accuracy decreases by 0.52%, and the AUC drops by 0.020. The BRNN structure is crucial for modeling both
past and future temporal dependencies, which is essential for capturing the complex emotional expressions and
rhythmic structures in ethnic opera. Features such as tonal shifts, pitch variations, and emotional fluctuations
rely on contextual information processing. Therefore, removing the BRNN structure causes the model to lose its
ability to model long-term dependencies in the time series, which subsequently impacts recognition accuracy. After removing the attention mechanism, the model’s accuracy drops by 0.43%, and the AUC decreases by
0.018. The attention mechanism improves classification accuracy by focusing on the features of key time steps
in the sequence, especially when dealing with complex inputs that contain noise or redundant information. It
helps the model effectively concentrate on important regions of the input. Without this mechanism, the model
distributes processing resources evenly across the time sequence, leading to the loss of critical information and
thus reducing classification performance. In comparison to the basic CNN model, which achieves an accuracy
of only 0.832 and an AUC of 0.873, significantly lower than the other variants, this further demonstrates the
necessity and effectiveness of each module proposed. Through these ablation experiments, this work has
validated the significant advantages of the RGLU-SE module, BRNN structure, and attention mechanism in
feature extraction, temporal dependency modeling, and global feature aggregation. The effective combination
of these modules has significantly improved the model’s performance and robustness, particularly in handling
complex audio data such as ethnic opera, allowing it to better capture the subtle differences in vocal styles.
(4)	 Statistical analysis and results
To validate the stability and significant performance improvement of the proposed model, multiple trainings
are conducted under different experimental settings, and the model’s performance is recorded across various
metrics. Each model undergoes five independent trainings, and the average and standard deviation of the results
are calculated. To further ensure the significance of the results, statistical methods such as t-tests are used to
determine whether the performance differences between the models are statistically significant. Table 6 presents
the average values and standard deviations for each experiment, and also provides the upper and lower bounds
of the 95% confidence interval to further confirm whether the results are statistically meaningful. Table 6 suggests that on both datasets (SEOFRS and MagnaTagATune), the RGLU-SE and ARGC-BRNN
models demonstrate superior performance in terms of accuracy and AUC values compared to other models,
and the differences are statistically significant. Specifically, on the SEOFRS dataset, the accuracy of RGLU-SE
reaches 87.2%, which shows a clear advantage over other models such as CNN and RCNN. Similarly, on the
MagnaTagATune dataset, RGLU-SE achieves an AUC of 91.2%, improving by 1.5% and 1.3% compared to CNN
Model variants
Accuracy
AUC value
Baseline-CNN
0.832
0.873
Residual
0.843
0.886
Gate
0.839
0.882
SE
0.845
0.887
BRNN
0.850
0.892
Attention
0.854
0.894
ARGC-BRNN (Full Model)
0.872
0.912
Table 5. The results of the ablation experiments. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

and GLU, respectively. Moreover, the relatively low standard deviations indicate that the RGLU-SE and ARGC-
BRNN models exhibit high consistency across multiple experiments. This also demonstrates the stability of the
models across different runs, as their performance remains excellent even with different random initializations
and training data splits. The low standard deviation further enhances the reliability of the results, indicating that the performance
improvements obtained are stable and reproducible. Statistical significance tests (such as t-tests) further validate
the effectiveness of the results. On both the SEOFRS and MagnaTagATune datasets, the performance differences
between RGLU-SE and ARGC-BRNN and other models exceed the standard error, with p-values smaller than
0.05, meaning that these differences are statistically significant. Therefore, the RGLU-SE and ARGC-BRNN
models not only outperform traditional models in terms of performance but also demonstrate better stability
and reliability.
(5)	 Case analysis
In order to evaluate the performance of ARGC-BRNN model more comprehensively and deeply understand
its advantages and disadvantages, several typical samples in SEOFRS dataset are analyzed. Table  7 lists the
outstanding samples and misjudged samples of some models, and analyzes their causes. In this study, the MSA-Class model demonstrated exceptional multimodal fusion capabilities, particularly
in teacher emotion recognition and classroom behavior assessment, significantly outperforming traditional
models such as RF and SVM. This finding is consistent with previous research. Wang et al. (2024) showed
that multimodal fusion models could effectively enhance the accuracy of sentiment analysis and behavior
prediction16. Compared with single-modality research results, the multimodal fusion strategy proposed here
is evidently more adaptable to the dynamic classroom environment. The model’s superior performance in
multiple regression metrics such as MSE, MAE, and correlation reflects the in-depth mining and expressive
power of multimodal information in teaching assessment. In classification metrics, the MSA-Class model also
outperformed comparison methods. The significant increase in accuracy indicates that the model has unique
advantages in fine-grained teaching behavior recognition and emotion state classification. This is in line with
the multimodal analysis method proposed by Ezzameli and Mahersia (2023), who also found that multimodal
models could better capture the subtle connections between emotions and behaviors. Especially in scenarios
Sample
number
Role type
(real)
Forecast
category
Correct
or not
Analysis
S01
Qingyi
Qingyi
√
The sample contains clear vibrato and strong emotional expression in the high-pitched region, and the features in the Mel
spectrogram are obvious, and the model is accurately identified. The timbre characteristics of Qingyi are unique and stable,
and the model can capture these acoustic information well, so it is accurately classified. S02
Huadan
Qingyi
×
The sample has a high timbre and a part of Qingyi style, and there is slight noise in the recording, which leads to confusion of
the model. Although the timbre of the sample has certain Qingyi characteristics, Huadan’s vocal characteristics are not fully
reflected, and the interference of noise aggravates the difficulty of model identification, leading to misjudgment. S03
Daomadan
Huadan
×
Peking opera blues’s vocals incorporate Huadan’s feminine features, and the model is misjudged when the category boundary
is blurred. Peking opera blues’s style is both powerful and feminine, which belongs to the transitional area of style, which
makes it difficult to distinguish the models clearly and leads to misjudgment. S04
Laodan
Laodan
√
The timbre is low and the pronunciation is generous. The model accurately extracts low-frequency features and classifies them
correctly. Laodan’s voice has obvious low-frequency characteristics. ARGC-BRNN model can successfully identify and extract
these unique acoustic characteristics, so the prediction results are accurate. S05
Qingyi
Qingyi
√
The expression of emotion is clear, the acoustic characteristics are distinct in spectrum, and the model identification is correct. The sound characteristics of Qingyi are distinct, and the emotional expression has strong recognition. The characteristics of
pitch, timbre and volume in Mel spectrogram are very prominent, which makes the model accurately classified. Table 7. Typical sample analysis. Model
Dataset
Accuracy (%)
Standard deviation (%)
95% Confidence interval (lower)
95% Confidence interval (upper)
CNN
SEOFRS
84.7
0.72
84.1
85.3
GLU
85.5
0.67
85.0
86.0
RCNN
85.9
0.65
85.4
86.4
RGLU
86.2
0.58
85.8
86.6
RGLU-SE
87.2
0.53
86.8
87.6
ARGC-BRNN
87.2
0.52
86.8
87.6
CNN
MagnaTagATune
89.7
0.64
89.3
90.1
GLU
89.95
0.62
89.6
90.3
RCNN
89.91
0.60
89.5
90.3
RGLU
90.7
0.54
90.2
91.2
RGLU-SE
91.2
0.51
90.7
91.7
ARGC-BRNN
91.2
0.48
90.8
91.6
Table 6. Statistical analysis results. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

with significant emotional fluctuations, the model’s sensitivity and accuracy are enhanced31. The results of the
ablation experiments also provided in-depth insights into the model. When the text modality was removed,
the model’s performance dropped significantly, verifying the core role of linguistic information in classroom
assessment. This result is consistent with Zhao et al. (2023)’s research on emotions and language expression,
who pointed out that the language modality was crucial for emotion judgment. The absence of visual and audio
modalities also led to varying degrees of performance degradation, further emphasizing the synergistic effect
of multimodal information. These findings not only validate the importance of multimodal fusion in teacher
emotion and behavior assessment but also provide new ideas and methods for future educational data analysis. Discussion
The ARGC-BRNN model proposed effectively improves the accuracy and generalization ability of ethnic
opera female role singing style classification by incorporating RGLU-SE, BRNN, and the attention mechanism. Similarly, Ashraf et al. proposed a hybrid architecture combining CNN and RNN for music genre classification. Through a comparison of the Mel spectrogram and Mel-frequency cepstral coefficient features, experiments
demonstrated that the CNN and Bi-GRU hybrid architecture using Mel spectrograms achieved the best accuracy
of 89.30%32. Koşar and Barshan proposed a new hybrid network architecture combining LSTM and 2D CNN
branches. They used wearable motion sensors and deep learning techniques to recognize human activities, and
their model outperformed other common network models, achieving an accuracy improvement of 2.45% and
3.18% on two datasets, respectively33. Jena et al. proposed a deep learning-based hybrid model combining
multimodal and transfer learning methods for music genre classification. The results showed that this hybrid
model outperformed traditional deep learning models and other existing models in terms of training and
validation accuracy, loss, precision, recall, and other metrics34. In summary, these studies demonstrate the
effectiveness of hybrid networks in feature extraction. Overall, the ARGC-BRNN model shows significant
advantages in the application of ethnic opera female role singing style classification, providing new insights for
music genre classification and singing feature analysis. Conclusion
Research contribution
This work focuses on ethnic opera female role singing excerpts as the research object and constructs the ARGC-
BRNN model based on residual gated convolution, BRNN, and attention mechanisms. It explores the model
architecture design, module performance analysis, and comparisons with other models, drawing the following
conclusions: (1) On the SEOFRS dataset, the RGLU-SE module achieves an accuracy of 0.872, which improves by
2.5%, 1.7%, 1.3%, and 1.1% compared to CNN, GLU, RCNN, and RGLU, respectively. On the MagnaTagATune
dataset, RGLU-SE achieves an AUC of 0.912, surpassing other convolutional structures, indicating its advantage
in feature extraction. (2) The BLSTM structure achieves the highest accuracy of 0.872 on the SEOFRS dataset
and an AUC of 0.912 on the MagnaTagATune dataset. It outperforms GRU and LSTM, demonstrating that
BRNN is better at capturing sequential contextual information, particularly in complex datasets. (3) The ARGC-
BRNN model performs the best on both datasets, achieving the highest AUC and accuracy, surpassing other
models. Despite having the largest number of parameters, it exhibits the shortest training time, demonstrating
high computational efficiency. In summary, the ARGC-BRNN model shows great potential in extracting and
analyzing the singing style features of ethnic opera female characters. Although the current experimental results
demonstrate its strong classification capability, future validation with more extensive datasets and diverse
musical styles is needed to further enhance its application prospects in the field of music intelligence analysis. Future works and research limitations
Although the ARGC-BRNN model performs exceptionally well on two datasets, its generalization ability and
adaptability to unseen data or different singing styles still need further evaluation. The current experiments are
limited to the classification of ethnic opera female character singing styles, and the model’s ability to classify
other types of ethnic opera or different music styles has not been fully validated. Future research should expand
to a wider range of musical styles and singing styles to assess the model’s performance in different contexts and
optimize its generalization ability to unseen data. Additionally, the ARGC-BRNN model has a relatively large
number of parameters, which could impact its deployment in resource-constrained practical applications. For
example, in mobile devices or low-computational environments, the model’s computational demands may result
in reduced processing efficiency, and limit its feasibility for real-time processing and large-scale deployment. Therefore, future studies could explore lightweight model designs, model pruning, and quantization techniques
to reduce the computational resource requirements, and enhance its flexibility and deployability in practical
applications. Furthermore, to address the model’s computational efficiency and processing speed, algorithms can
be further optimized to shorten response time for real-time analysis, meeting the needs for fast and real-time
processing. Data availability
The datasets used and/or analyzed during the current study are available from the corresponding author Huixia
Yang on reasonable request via e-mail m13868991959@163.com. Received: 28 December 2024; Accepted: 2 June 2025
Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

References

### 1. Li, Y. & Damdindorj, T. Analysing the singing style and teaching of American voice in colleges and universities: the marriage of

Figaro as an Example. Front. Bus. Econ. Manage. 13 (1), 183–186 (2024).

### 2. Pengzhen, N. P. & Punvaratorn, M. The study of the Opera baritone’s singing skills in the where is the wind blowing Song. Asia Pac. J. Religions Cultures. 8 (1), 296–313 (2024).

### 3. Yang, X., Rodsakan, T. & Jamnongsarn, S. The artistic characteristics of Opera funded by the Chinese National arts Fund. J. Multidisciplinary Humanit. Social Sci. 7 (5), 2646–2664 (2024).

### 4. Liu, N. An investigation of the fusion path of multiple singing styles in american vocal singing by incorporating Markov Chain

prediction model. Appl. Math. Nonlinear Sci. (2023).

### 5. Brandner, M. et al. Classification of phonation modes in classical singing using modulation power spectral features. IEEE Access.

11, 29149–29161 (2023).

### 6. Ikävalko, T. et al. Three professional singers’ vocal tract dimensions in operatic singing, kulning, and edge—a multiple case study

examining loud singing. J. Voice. 38 (5), 1253 (2024). e11-1253. e27.

### 7. Rascon, C. Characterization of deep learning-based speech-enhancement techniques in online audio processing applications. Sensors 23 (9), 4394 (2023).

### 8. Zaman, K. et al. A survey of audio classification using deep learning. IEEE Access 11, 106620–106649 (2023).

### 9. Latif, S. et al. A survey on deep reinforcement learning for audio-based applications. Artif. Intell. Rev. 56 (3), 2193–2240 (2023).

### 10. Moysis, L. et al. Music deep learning: deep learning methods for music signal processing—a review of the state-of-the-art. Ieee

Access. 11, 17031–17052 (2023).

### 11. Li, C. et al. Artificial intelligence, resource reallocation, and corporate innovation efficiency: evidence from china’s listed companies. Resour. Policy. 81, 103324 (2023).

### 12. Wang, Z. et al. Achieving sustainable development goal 9: A study of enterprise resource optimization based on artificial intelligence

algorithms. Resour. Policy. 80, 103212 (2023).

### 13. El Ardeliya, V., Taylor, J. & Wolfson, J. Exploration of artificial intelligence in creative fields: generative art, music, and design. Int. J. Cyber IT Service Manage. 4 (1), 40–46 (2024).

### 14. Prabhakar, S. K. & Lee, S. W. Holistic approaches to music genre classification using efficient transfer and deep learning techniques. Expert Syst. Appl. 211, 118636 (2023).

### 15. Faizan, M. et al. Implementation of deep learning models on an SoC-FPGA device for real-time music genre classification. Technologies 11 (4), 91 (2023).

### 16. Mehra, A., Mehra, A. & Narang, P. Classification and study of music genres with multimodal spectro-lyrical embeddings for music

(SLEM). Multimed. Tools Appl. 23(12), 1–21 (2024).

### 17. Tsavalias, V. Transparent and accessible audio processing: hybrid CNN-LSTM deep learning techniques for vocal separation in

music. (2024).

### 18. Singh, J. An efficient deep neural network model for music classification. Int. J. Web Sci. 3 (3), 236–248 (2022).

### 19. Liu, S. et al. An efficient spatial–temporal model based on gated linear units for trajectory prediction. Neurocomputing 492, 593–

600 (2022).

### 20. Liu, C., Zhen, J. & Shan, W. Time series classification based on convolutional network with a gated linear units kernel. Eng. Appl. Artif. Intell. 123, 106296 (2023).

### 21. Hu, Y., Tang, H. & Pan, G. Spiking deep residual networks. IEEE Trans. Neural Networks Learn. Syst. 34 (8), 5200–5205 (2021).

### 22. Li, Y. & Wang, L. Human activity recognition based on residual network and BiLSTM. Sensors 22 (2), 635 (2022).

### 23. Zhang, R. F. & Li, M. C. Bilinear residual network method for solving the exactly explicit solutions of nonlinear evolution equations. Nonlinear Dyn. 108 (1), 521–531 (2022).

### 24. Zeng, C. et al. Squeeze-and-excitation self-attention mechanism enhanced digital audio source recognition based on transfer

learning. Circuits Syst. Signal. Process. 44(1), 480–512 (2024).

### 25. Zafar, A. et al. A comparison of pooling methods for convolutional neural networks. Appl. Sci. 12 (17), 8643 (2022).

### 26. Grekow, J. Music emotion recognition using recurrent neural networks and pretrained models. J. Intell. Inform. Syst. 57 (3), 531–

546 (2021).

### 27. Kumaraswamy, B. Improved harmonic spectral envelope extraction for singer classification with hybridised model. Int. J. Bio-

Inspired Comput. 24 (3), 150–163 (2024).

### 28. Gan, J. Music feature classification based on recurrent neural networks with channel attention mechanism. Mob. Inform. Syst. 2021

(1), 7629994 (2021).

### 29. Yu, Y. et al. Deep attention based music genre classification. Neurocomputing 372, 84–91 (2020).

### 30. Yu, B. et al. Museformer: transformer with fine-and coarse-grained attention for music generation. Adv. Neural. Inf. Process. Syst.

35, 1376–1388 (2022).

### 31. Shen, J. & Xiao, G. Music genre classification based on functional data Analysis. IEEE Access. 12, 185482–185491 (2024).

### 32. Ashraf, M. et al. A hybrid Cnn and Rnn variant model for music classification. Appl. Sci. 13 (3), 1476 (2023).

### 33. Koşar, E. & Barshan, B. A new CNN-LSTM architecture for activity recognition employing wearable motion sensor data: enabling

diverse feature extraction. Eng. Appl. Artif. Intell. 124, 106529 (2023).

### 34. Jena, K. K. et al. A hybrid deep learning approach for classification of music genres using wavelet and spectrogram analysis. Neural

Comput. Appl. 35 (15), 11223–11248 (2023). Author contributions
Huixia Yang: Conceptualization, methodology, software, validation, formal analysis, investigation, resources,
data curation, writing—original draft preparation, writing—review and editing, visualization, supervision, pro­
ject administration, funding acquisition. Funding
This research received no external funding. Declarations
Ethics approval and consent to participate
The studies involving human participants were reviewed and approved by Xingzhi College, Zhejiang Normal
University Ethics Committee (Approval Number: 2022.2510023). The participants provided their written
informed consent to participate in this study. All methods were performed in accordance with relevant
guidelines and regulations. Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/

Competing interests
The authors declare no competing interests. Additional information
Correspondence and requests for materials should be addressed to H. Y. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:20341

| https://doi.org/10.1038/s41598-025-05429-8
www.nature.com/scientificreports/
