# Representation learning with parameterised

**Year:** D:20

---

## ARTICLE IN PRESS

Article in Press
Representation learning with parameterised
quantum circuits for advancing speech emotion
recognition
Scientific Reports
Received: 5 August 2025
Accepted: 6 November 2025
Cite this article as: Rajapakshe T., Rana R., Riaz F. et al. Representation
learning with parameterised quantum
circuits for advancing speech emotion
recognition. Sci Rep (2025). https://doi.
org/10.1038/s41598-025-27871-4
Thejan Rajapakshe, Rajib Rana, Farina Riaz, Sara Khalifa & Björn W. Schuller
We are providing an unedited version of this manuscript to give early access to its
findings. Before final publication, the manuscript will undergo further editing. Please
note there may be errors present which affect the content, and all legal disclaimers
apply. If this paper is publishing under a Transparent Peer Review model then Peer
Review reports will publish with the final article.
https://doi.org/10.1038/s41598-025-27871-4
© The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit
to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do
not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain
permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/4.0/.

## ARTICLE IN PRESS

Representation Learning with Parameterised
Quantum Circuits for Advancing Speech Emotion
Recognition
Thejan Rajapakshe1,*, Rajib Rana1,**, Farina Riaz2, Sara Khalifa3, and Bj¨orn W. Schuller4,5
1University of Southern Queensland, Australia
2Commonwealth Scientific and Industrial Research Organisation, Australia
3Queensland University of Technology, Australia
4GLAM – the Group on Language, Audio, & Music, Imperial College London, UK
5Head of CHI - Chair of Health Informatics, Technical University of Munich (TUM), Munich, Germany
*Thejan. Rajapakshe@unisq.edu.au
**Rajib. Rana@unisq.edu.au
ABSTRACT
Quantum machine learning (QML) offers a promising avenue for advancing representation learning in complex signal domains. In this study, we investigate the use of parameterised quantum circuits (PQCs) for speech emotion recognition (SER)—a
challenging task due to the subtle temporal variations and overlapping affective states in vocal signals. We propose a hybrid
quantum-classical architecture that integrates PQCs into a conventional convolutional neural network (CNN), leveraging
quantum properties such as superposition and entanglement to enrich emotional feature representations. Experimental evalua-
tions on three benchmark datasets IEMOCAP, RECOLA, and MSP-IMPROV—demonstrate that our hybrid model achieves
improved classification performance relative to a purely classical CNN baseline, with over 50% reduction in trainable parameters. Furthermore, Adjusted Rand Index (ARI) analysis demonstrates that the quantum model yields feature representations with
improved alignment to true emotion classes compared with the classical model, reinforcing the observed performance gains. This work provides early evidence of the potential for QML to enhance emotion recognition and lays the foundation for future
quantum-enabled affective computing systems. Introduction
Representation learning has become a foundational approach in machine learning, enabling systems to extract meaningful
patterns directly from raw data. In the field of Speech Emotion Recognition (SER), this paradigm is particularly valuable for
interpreting the rich and often ambiguous emotional signals embedded in vocal expressions. Despite recent progress, SER
continues to face significant challenges in achieving high accuracy without resorting to increasingly complex models with a
large number of trainable parameters. Key obstacles include the overlapping nature of emotional states, speaker variability, and
the intricate interdependencies among acoustic features such as pitch, energy, and rhythm1–3. Quantum Machine Learning (QML) offers a compelling alternative by exploiting the unique computational characteristics
of quantum systems: most notably, superposition and entanglement. Superposition enables quantum models to process multiple
states simultaneously, allowing for a more holistic analysis of the nuanced and concurrent variations inherent in emotional
speech. Rather than evaluating features in isolation or sequentially, as is typical in classical systems, quantum models can
assess complex patterns across all dimensions in parallel. Entanglement further enhances this potential by capturing the dependencies between speech features that classical models
often overlook or treat independently4–7. In practice, emotional states are rarely expressed through isolated vocal characteristics;
instead, they emerge from subtle relationships between multiple attributes, such as correlations between tone, tempo, and
energy. QML systems inherently encode and analyse these relationships, leading to richer and more robust representations of
affective information. Parameterised Quantum Circuits (PQCs) are among the most promising constructs in QML. These circuits consist of tunable
quantum gates, which can be trained to optimise complex representations. Unlike conventional deep neural networks—which
often rely on large numbers of parameters to model high-dimensional spaces—PQCs can encode exponentially large feature
spaces using comparatively fewer resources8. This makes them especially suitable for SER, where modelling emotional
intricacies efficiently is critical. The emergence of Noisy Intermediate-Scale Quantum (NISQ) devices, such as quantum processors with limited qubit

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

counts and moderate noise resilience, has made it feasible to explore hybrid quantum-classical learning strategies. While current
quantum hardware is not yet mature for large-scale deployment, simulations of PQC-based models offer valuable insights into
their performance and architectural viability under NISQ constraints. In this study, we propose a novel hybrid architecture for speech emotion recognition that integrates PQCs within a classical
convolutional neural network framework, as illustrated in Figure 1. By combining the expressive power of quantum circuits
with the proven feature extraction capabilities of CNNs, our approach addresses key limitations of classical models in terms of
both accuracy and computational efficiency. Experiments conducted on three benchmark datasets IEMOCAP, RECOLA, and
MSP-IMPROV demonstrate that the hybrid model achieves improved classification performance compared to a classical CNN
baseline, while reducing the number of trainable parameters by over 50%. This work contributes to the growing field of quantum-enhanced affective computing by demonstrating that PQCs can
be effectively applied to emotionally rich, temporally structured data. It also provides empirical insights into how quantum
circuit design, particularly expressibility and entanglement, affects model performance, laying the groundwork for future
implementation on real quantum hardware. Representation
Learning Block -
Classical
(CNN Based)
Representation Learning Block - Quantum
Classification
Input Spectrogram
Output
Quantum Circuit
Embedding
Circuit Layer
Measurement
Figure 1. A simplified architecture of the proposed Hybrid Classical-Quantum SER model. Related Work
Speech Emotion Recognition (SER) has experienced significant advancements through the adoption of representation learning,
a paradigm where models automatically extract meaningful features directly from raw speech data. Deep learning has been
instrumental in this shift, enabling the development of models capable of learning rich and task-specific representations,
surpassing the limitations of traditional hand-engineered features. However, despite improving accuracy and adaptability,
deep learning-based methods face challenges, including high computational demands and difficulties in capturing intricate
relationships within high-dimensional feature spaces. Quantum machine learning (QML) offers a promising solution by
leveraging quantum circuits to efficiently process and represent complex, high-dimensional data with fewer resources. This
section explores recent advancements in representation learning for SER and examines how QML can address the computational
and modelling challenges of classical deep learning approaches. Representation Learning in SER
Representation learning has emerged as a powerful paradigm for extracting meaningful features from speech data, enabling
significant advancements in SER systems. Automatic Feature Extraction and Task Specificity
Conventional feature engineering requires prior domain knowledge to design features, which may not generalise well across
datasets or tasks. Representation learning, in contrast, automates feature extraction by learning task-relevant features directly
2/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

from raw audio signals. Trigeorgis et al. demonstrated that deep convolutional recurrent networks could extract hierarchical
features from raw waveforms, outperforming traditional MFCC-based systems9. This approach eliminates the need for manual
feature design, reducing human intervention and improving adaptability to diverse datasets10–12. Enhanced Representational Power
Deep learning architectures like Convolutional Neural Networks (CNNs) and Long Short-Term Memory (LSTM) networks
learn temporal and spectral dependencies, enhancing their ability to model subtle emotional cues13,14. Satt et al.15 found that
deep models with spectrogram-based inputs significantly outperformed systems using hand-crafted features to detect speech
emotions. Zhao et al.16 introduced two CNN-LSTM architectures: one utilising 1D CNNs for raw audio input and the other
employing 2D CNNs for Mel-spectrogram inputs. They reported achieving an accuracy of 52.14% on the IEMOCAP database
for speaker-independent SER using the 2D CNN-LSTM model. Further advancing classical methods, researchers have also explored complex architectures to address multiple SER
challenges simultaneously. For instance, Daneshfar and Kabudian proposed a system using a hierarchical multi-layer sparse
auto-encoder combined with an Extreme Learning Machine (ELM)2. Their approach utilised a rich set of spectral and spectro-
temporal features and notably introduced a new adaptive weighting method specifically to counteract the problem of data
imbalance, a persistent challenge in SER datasets. This highlights a direction in classical SER research focused on creating
sophisticated, multi-stage processing pipelines to extract discriminative features and build robust classifiers. Scalability Across Languages and Domains
Hand-crafted features often need to be tailored for specific languages or domains, limiting their scalability. Representation
learning, however, leverages large-scale pre-training to learn universal speech representations applicable across multiple tasks
and languages. Huang et al.17 highlighted that attention-based models trained on multilingual datasets generalise well, enabling
SER systems to scale efficiently. Mirsamadi et al.18 demonstrated that deep recurrent neural networks can effectively learn
and aggregate frame-level acoustic features into compact utterance-level representations for improved emotion recognition. Additionally, they proposed a local attention-based pooling strategy to focus on emotionally salient regions of speech, achieving
superior performance on the IEMOCAP corpus compared to existing methods. Robustness to Limited Labelled Data
Representation learning, especially self-supervised approaches, reduces the reliance on labelled data, which is often scarce in
SER. Models pre-trained on large unlabelled datasets, such as HuBERT19, can be fine-tuned with limited labelled data, making
them ideal for settings with sparse annotations. This adaptability is a significant advantage over traditional methods requiring
extensive labelled data for optimal performance. Challenges in Representation Learning for SER: Computational Demands and High-Dimensional Modelling
Representation learning has brought transformative advancements to SER, enabling the automatic extraction of task-relevant
features and outperforming traditional hand-crafted approaches20,21. However, the underlying deep learning models are
computationally intensive, leading to significant resource demands, especially during training. Moreover, the classical deep
learning models face challenges in efficiently modelling complex correlations and entanglements in high-dimensional feature
spaces, which are critical for capturing subtle emotional cues in speech22. QML addressing the Challenges in Representation Learning for SER
QML offers a promising alternative to address these issues. Quantum circuits, by leveraging principles of superposition and
entanglement, have the potential to represent and process exponentially large feature spaces with fewer resources compared to
classical systems23. This capability could enable more efficient representation learning for SER, particularly in scenarios with
limited labelled data or high-dimensional inputs. Quantum Machine Learning for SER and Related Fields
Early QML research focused on foundational algorithms like the quantum support vector machine24,25 and the Harrow-
Hassidim-Lloyd (HHL) algorithm for solving linear systems25. With the advent of noisy intermediate-scale quantum (NISQ)
devices, practical quantum-enhanced models, such as PQCs, have become feasible26. These advancements suggest that QML
can potentially overcome the limitations of classical deep learning, particularly in modelling high-dimensional data and reducing
resource requirements. Parameterised Quantum Circuits (PQCs)
QML has also shown promise in augmenting traditional neural network structures through Quantum Neural Networks (QNNs). By employing PQCs as neural layers, QNNs can encode quantum states while exploiting quantum advantages for specific
tasks. Farhi and Neven pioneered quantum-enhanced learning frameworks for combinatorial optimisation8, and Schuld and
3/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Killoran demonstrated how quantum circuits can efficiently process and generalise high-dimensional data27, showcasing their
suitability for complex learning tasks. While none of the above studies focused on SER, Qu et al. introduced a Quantum
Federated Learning (QFL) algorithm for emotion recognition in speech. Their method emphasised privacy and robustness in
noisy environments by employing quantum minimal gated unit RNNs28. However, a key shortcoming of this work is that it did
not focus on representation learning. By not leveraging the feature representation capabilities of PQCs, the model’s ability
to capture the complex, high-dimensional dependencies inherent in emotional speech data remained unexplored, limiting its
potential effectiveness for the core SER task. Hybrid Classical-Quantum Architectures
Hybrid quantum-classical architectures have been explored to enhance model expressiveness and training efficiency. These
architectures integrate the representational strengths of classical deep learning with the computational power of quantum
systems29,30. Hybrid models are particularly suited for tasks where classical models face limitations, as quantum layers
can introduce novel features and expand the solution space. Other explorations into hybrid quantum-classical architectures
have shown promise but have not yet unlocked a quantum advantage for SER. For instance, Thejha et al. applied a hybrid
quantum-classical CNN to general speech recognition, achieving performance merely comparable to classical CNNs without
demonstrating a clear benefit31. Likewise, work by Esposito et al. on audio classification for cough detection32 also failed
to investigate representation learning for SER. These studies, while foundational, stopped short of demonstrating that QML
could either outperform classical methods or effectively model the nuanced feature representations required for robust emotion
recognition. Similarly, Norval and Wang proposed a Quantum AI-based approach for SER, but its practical viability was limited,
achieving a low accuracy of only 30% on a custom dataset33. Their approach, which relied on basic quantum encoding and
variational algorithms without exploring PQCs or representation learning, underscores the significant performance challenges
that early QML-SER models faced. An area of significant interest is the application of hybrid architectures in CNNs, leading to the development of quantum
CNNs (QCNNs). QCNNs effectively process structured data by utilising quantum circuits to perform convolution-like
operations, as demonstrated by Cong et al.34. Table 1. Summary of the Literature related to Quantum (Q.) Machine Learning used for SER and related fields
Research Study
Focus
Dataset
Hybrid Classical-Q. Model
Parameterised Q. Circuits
Representation Learning w/ Q. Speech Emotion Recognition
Esposito et al.

✓
✓
✓
✗(Audio Classification)
DiCOVA35
Thejha et al. 202331
✓
✗
✓
✗(Speech Recognition)
Not Available
Norval & Wang

✗
✗
✗(SVM)
✓
Custom Dataset
Qu et al. 202428
✗
✓
✗(QFL)
✓
CASIA36
RAVDESS37
EMO-DB38
This Paper
✓
✓
✓
✓
IEMOCAP39
RECOLA40
MSP-Improv41
4/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Research Gap
Table 1 provides a comparative overview of existing research utilising QML for SER and related fields. While the table
highlights investigations into hybrid classical-quantum architectures and PQCs within broader audio and speech processing
domains, a significant research gap exists in their application to representation learning for SER. Three key observations
characterise this gap:
• Limited SER Focus - Existing QML research for audio predominantly targets broader applications like general audio
classification and speech recognition, with comparatively little exploration of the specific nuances and complexities of
SER.
• Unexplored Representation Learning - While some studies have incorporated hybrid classical-quantum models and PQCs
in related audio tasks, their potential for representation learning within the SER domain remains largely untapped. This
represents a significant avenue for future research.
• Potential for Advancement - This identified research gap highlights the novelty and substantial potential of integrating
QML techniques, particularly PQCs and hybrid architectures, into representation learning paradigms for SER. Such
integration promises to unlock more efficient and robust emotion recognition systems, addressing the current limitations
of classical approaches. This paper aims to investigate the of integration QML techniques, specifically PQCs and hybrid architectures, into representation
learning frameworks to address these gaps and drive advancements in the field of SER. Contextualising Quantum Machine Learning for Speech Emotion Recognition
In this study, we conduct a preliminary investigation to evaluate the applicability of Quantum Machine Learning (QML) with
Parameterised Quantum Circuits (PQCs) for Speech Emotion Recognition (SER) tasks. By leveraging the quantum properties
of superposition and entanglement, we hypothesise that QML can learn more complex and abstract representations from speech
data, which are crucial for improving SER performance. A simplified architecture of the proposed hybrid Classical-Quantum model is illustrated in Figure 1. In this model, the
input spectrograms of speech audio data are first processed through a CNN-based representation learning block to generate
classical representations. These representations are subsequently passed through a quantum representation learning block,
where quantum operations are performed. Finally, the learnt quantum representations are fed into a classification block to
predict the emotional state. The Quantum Representation Learning block incorporates a quantum layer composed of three key components: the
Quantum Embedding Component, the Quantum Circuit Layer, and the Quantum Measurement Component. This architecture
allows the block to accept classical inputs, transform them into quantum states, and output classical representations, facilitating
seamless representation transition in the hybrid classical-quantum model. Preamble
Quantum Embedding refers to the process of encoding classical speech features into quantum states within the quantum
Hilbert space. This step enables classical audio features to interface with quantum systems and serves as the foundation for
quantum machine learning algorithms27. To achieve quantum embeddings, PQCs or predefined encoding schemes are employed
to transform speech feature inputs into quantum states that can be manipulated by quantum gates. A Quantum Circuit Layer consists of a series of quantum gates that act on qubits to perform specific transformations
or computations. Quantum circuits layers form the computational backbone of QNNs, enabling quantum systems to process
information and learn. Two main types of circuits are utilised: Static Quantum Circuits – These circuits have fixed configurations with pre-specified gate sequences and no adjustable
parameters. Static circuits typically perform predefined operations, such as feature extraction or classical-to-quantum encoding,
without further tuning during the training process. Parameterised Quantum Circuits – PQCs include variable parameters – such as rotation angles in quantum gates – that are
optimised iteratively during training26. As the trainable core of QNNs, PQCs enable dynamic adaptation to input data by
minimising a defined cost function. Quantum Measurement is the process of extracting classical information from quantum states by projecting them onto
specific basis states25. In this study, we explore several commonly used measurement configurations in PennyLane, namely
PauliZ, Z, PauliX, and Probability measurements. It is important to note that these measurement types are conceptually related: all can be expressed as probability measure-
ments over different observables or bases. The distinction lies primarily in the choice of measurement operator (e.g. Z, X) and
5/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

the number of shots or post-processing applied to obtain expectation values. Thus, these configurations represent alternative
ways to extract classically interpretable information from the quantum circuit, rather than fundamentally different measurement
paradigms. PauliZ and Z Measurements – The PauliZ observable measures the expectation value of the Z operator, providing a
continuous value in [−1,+1], corresponding to the average over repeated shots. In contrast, the Z measurement returns a
single-shot projection in the computational basis, yielding discrete outcomes |0⟩or |1⟩. In practice, the two differ mainly in how measurement statistics are aggregated: PauliZ corresponds to computing the
expected value over many Z-basis shots, while Z represents the raw projective measurement itself. Both can be interpreted
within a unified probabilistic framework, where PauliZ is the expectation of the Z-basis probability distribution. PauliX Measurement – involves projecting the qubit state onto the eigenstates of the Pauli X operator:
• |+⟩= |0⟩+|1⟩
√
2 (eigenvalue+1)
• |−⟩= |0⟩−|1⟩
√
2 (eigenvalue−1)
This measurement essentially determines the “flip basis” (analogous to flipping the computational basis). The Mathematical
representation of the PauliX measurement is as follows.

## X =




Similar to PauliZ and Z measurements, PauliX operates as a probability measurement in the X-basis, yielding expectation
values or single-shot outcomes depending on the readout configuration. Probability Measurement – The Probability measurement returns the full probability distribution over all computational
basis states. As such, PauliZ, PauliX, and Z measurements can be regarded as specific marginal or expectation-based forms of
this general probabilistic readout, obtained by selecting appropriate observables or basis rotations. In summary, while different measurement operators provide varied perspectives on the encoded quantum state, they are
mathematically interrelated through the probability distribution over basis states. The inclusion of multiple measurement
forms in this study was intended to evaluate whether specific observables (e.g., Z vs. X) yield more discriminative quantum
representations for speech emotion features under the same probabilistic framework. Model Architecture
Figure 2 illustrates the detailed architecture employed in this study. The model builds upon the foundational SER architecture
proposed by Issa et al.42. This architecture was selected for its simplicity, as it avoids the complexities introduced by components
such as transformers, attention mechanisms, and LSTM networks. By focusing on a streamlined architecture, we aim to isolate
and evaluate the specific contribution of the quantum layer to the SER task. Classification Block
Representation Learning Block - Quantum
Representation Learning Block - Classical
Quantum
Measurement
Quantum Embedding
Input Mel-Spectrogram
CNN
Batch
Normalise
CNN
Batch
Normalise
|0⟩
R(ϴ1)
R(ϴ2)
R(ϴ8)
|0⟩
|0⟩
U
Fully Connected Layer 1
Fully Connected Layer 2
Output Layer
Classical-Quantum Adapter
Figure 2. Overview of the model architecture used in this study. Input features pass through a CNN representation learning
module, followed by a Quantum representation learning module, before reaching the classification layer that assigns the input
spectrogram to one of the output classes. The Quantum representation learning block contains Quantum Embedding, Quantum
Circuit Layer (U), and Quantum Measurement respectively. We acknowledge the limitations of this approach. The baseline CNN model does not incorporate more complex components
like LSTM layers for temporal modeling or attention mechanisms, which have been shown to enhance SER performance by
enabling the model to dynamically focus on the most emotionally salient segments of speech43. This choice represents a
6/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

critical trade-off: while a more sophisticated classical architecture could potentially yield higher overall accuracy, it would also
introduce confounding variables, making it more difficult to isolate and interpret the specific impact of the quantum components. Our primary goal in this study is to establish a clear and foundational understanding of the quantum layer’s capabilities. By
benchmarking against a simpler, well-understood classical model, we can more directly attribute performance gains to the
quantum representation learning, thereby balancing the pursuit of absolute performance with the need for clear, interpretable
results. The architecture consists of three primary blocks: a CNN-based classical representation learning block, a quantum
representation learning block, and a classification block. The input spectrograms are initially processed by the CNN block,
which extracts classical feature maps using convolutional operations. These intermediate representations are subsequently
forwarded to the quantum representation learning block for further processing. To ensure compatibility between the classical
and quantum components, a classical-to-quantum adaptor is introduced. This adaptor reshapes, flattens, and reformats the CNN
output to match the input requirements of the quantum embedding layer. Representation Learning Block - Classical
The CNN-based representation learning block consists of two convolutional layers. The first convolutional layer employs 256
filters with a kernel size of 5, stride of 1, and no padding, followed by a batch normalisation layer and a ReLU activation. The
second convolutional layer applies 128 filters with a kernel size of 5, stride of 1, and no padding, followed by a ReLU activation,
dropout (p = 0.1), batch normalisation, and a max pooling layer with kernel size 8 and stride 1. An additional dropout layer (p
= 0.2) is applied after pooling. These CNN layers were deliberately kept simple to isolate the contribution of the quantum
feature extraction block, while still providing sufficiently rich feature maps for quantum embedding. Representation Learning Block - Quantum
The quantum representation learning block consists of three interconnected modules:

### 1. Quantum Embedding Module: Converts the classical input feature maps into quantum embeddings using quantum

embedding algorithms. This step ensures that the input data is represented as quantum states in the Hilbert space, enabling
manipulation by quantum gates.

### 2. Quantum Circuit Layer (U): Utilises PQCs to process the quantum embeddings. PQCs include adjustable parameters

(e.g., rotation angles) that are optimised during training to enhance the SER task. These circuits enable the model to learn
complex and abstract representations by leveraging the unique properties of quantum systems such as superposition and
entanglement.

### 3. Quantum Measurement Module: Extracts classical information from the processed quantum states by projecting

them onto specific basis states. This step produces interpretable outputs, such as probabilities or projections, that are
subsequently passed to the classification block. In this study, as stated, we employ four quantum measurement methods – PauliZ, PauliX, Probability, and Z – to project
quantum states onto classical outcomes. These methods are critical for bridging the quantum-to-classical transition, enabling
the integration of quantum features into the SER task. To construct the quantum embedding module, we utilise three embedding algorithms – Angle Embedding, Amplitude
Embedding, and IQP Embedding – as described in Havlíˇcek et al.44. These embeddings map input features into quantum
vectors of n qubits (n = 8 in this study). The resulting quantum vectors are processed through the quantum circuit layer, which
applies quantum rotations and other transformations. For this layer, we employ Strongly Entangling Layers45 and Random
Layers as circuit designs. The random circuits were implemented using the RandomLayers class in the PennyLane library?,
which applies random sequences of rotation and entangling gates across the qubits. Importantly, these circuits include trainable
parameters — specifically, the rotation angles — that are optimised during the training process via gradient descent. This
configuration introduces stochasticity in the gate arrangement, promoting higher expressibility and richer feature interactions
while maintaining trainability. Random circuits are known to efficiently explore larger subspaces of the Hilbert space, which
may explain their superior empirical performance compared to more structured, deterministic circuits. These circuits facilitate
rich entanglement among qubits, enhancing the model’s capacity to capture intricate dependencies in the data. To maintain consistency across experiments, the quantum circuit size was fixed at n = 8 qubits for all embedding strategies. This uniform qubit configuration allows fair comparison of embedding effectiveness while controlling for circuit depth and
parameter count. A classical-to-quantum adaptor preprocesses the CNN output to align the classical feature dimensionality
with the embedding requirements. For instance, AngleEmbedding directly maps eight continuous-valued features (one per
qubit), while AmplitudeEmbedding requires normalising the feature vector into a 28 = 256-dimensional state vector as per
the PennyLane implementation. This projection ensures that all embeddings operate under the same 8-qubit constraint while
preserving their mathematical validity.
7/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Figure 3 illustrates the quantum circuit of a strongly entangling layer with four qubits. This configuration exemplifies how
entanglement is incorporated into the quantum layer to improve the model’s ability to learn nuanced emotional features from
speech data. The design of this four-qubit circuit, which uses sequential controlled-NOT (CNOT) gates to link the qubits,
systematically builds up correlations between them. This robust entanglement is critical for the model’s ability to represent the
complex, interdependent relationships among the various acoustic features that characterise emotional speech. R(α1
2,β1
2,Ɣ1
2)
R(α1
2,β1
2,Ɣ1
2)
R(α1
1,β1
1,Ɣ1
1)
R(α1
2,β1
2,Ɣ1
2)
R(α1
1,β1
1,Ɣ1
1)
R(α1
2,β1
2,Ɣ1
2)
R(α1
1,β1
1,Ɣ1
1)
R(α1
1,β1
1,Ɣ1
1)
Figure 3. Quantum Circuit Diagram of a Strongly Entangling Layer of four qubits
Classification Block
The classification block consists of two fully connected layers. The first fully connected layer maps the quantum measurement
output (dimension equal to the measurement size, e.g., 8 or 16 depending on the quantum configuration) to 8 neurons, followed
by a ReLU activation. The second fully connected layer reduces this to the final output dimension, which corresponds to the
number of emotion classes (2 for binary valence tasks and 4 for multi-class emotion classification). A softmax activation is
applied at the output to generate class probabilities. Experimental Setup
In this section, we outline the datasets, input features, and model configurations used in this study. The complete Python codebase
for the experiments and data pre-processing is publicly accessible on GitHub under the repository iot-health/QuantumMachineLearning-
for-SER. Datasets
To robustly evaluate the proposed hybrid classical-quantum model, we selected three benchmark datasets commonly used in the
SER field: IEMOCAP39, MSP-Improv41, and RECOLA40
IEMOCAP
is a widely used dataset containing 12 hours of audio-visual data from dyadic interactions between actors. The sessions include
both scripted and improvised scenarios designed to elicit specific emotions. While the emotions are acted, the improvisational
nature of many interactions introduces a degree of spontaneity not found in purely scripted datasets. By including IEMOCAP,
we test our model’s performance on more archetypal and clearly expressed emotions, which serves as a crucial baseline for
SER tasks. In this study, we focus on the audio from the improvised sessions and use the valence annotations, which range
from 1 to 5, to evaluate the model’s ability to capture nuanced emotional states. MSP-Improv
is a valuable resource designed to bridge the gap between acted and naturalistic data. It features actors improvising scenarios
that are specifically designed to elicit genuine emotional responses in a controlled setting. This methodology aims to produce
more realistic emotional expressions than simple script-reading, providing a unique test case for our model. The dataset
contains 20 predetermined scripts, allowing for the study of key emotions like happiness, sadness, anger, and neutrality. Using
MSP-Improv allows us to evaluate our model’s effectiveness on lexically controlled but emotionally varied speech. RECOLA
consists of recordings of spontaneous, naturalistic interactions between participants collaborating on a task remotely. The
emotional expressions in RECOLA are not acted or elicited, but arise naturally from the interaction, making them more
subtle and representative of real-world conversational speech. This presents a significant challenge for any SER model. By
8/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

evaluating on RECOLA’s valence annotations, we specifically test our model’s capacity to recognise emotions in spontaneous
and unscripted contexts, which is a key objective for advancing the field of SER. Input Features
Mel-Frequency Cepstral Coefficients (MFCCs) are commonly used as input features in SER studies46–49. While MFCCs
capture the spectral characteristics of an audio signal, they do not offer a direct visual representation of the signal’s structure. In
contrast, Mel-spectrograms provide a two-dimensional visual representation that more intuitively reflects the temporal and
spectral patterns of the audio. For this preliminary study, the interpretability of input features in relation to the audio signal is
crucial; hence, Mel-spectrograms were chosen as the input features for our model. To ensure uniformity across the dataset, each audio utterance was resampled to a sampling rate of 22 kHz and standardised
to a duration of 3 seconds, either by truncating or zero-padding as necessary. Mel-spectrograms were then extracted using a
window size of 2048 samples and a hop size of 512 samples, resulting in spectrograms with consistent dimensions for input to
the model. Table 2. Hyper Parameters used in the grid search
Hyper Parameter
Values
Learning Rate
0.001, 0.001, 0.00001
Optimiser
Adam, SGD, RMSProp, AdaDelta, AdaGrad
Weight Decay
0, 0.01, 0.001
Q. Embedding
Angle Embedding, Amplitude Em-
bedding, IQP Embedding
Q. Circuit Layer
Random Layers, Strongly Entan-
gling Layers
Q. Measurements
PauliZ, PauliX, Z + PauliZ, Proba-
bility
Model Configuration
Hyperparameters such as Quantum Measurement methods, Quantum Embedding algorithms, and Quantum Circuit Layers
were tuned alongside traditional training parameters, including the optimiser, learning rate, and weight decay. To identify the
optimal combination of these hyperparameters, we employed a grid search approach50. A comprehensive summary of the
hyperparameters and their respective values used in the grid search process is provided in Table 2. The models were implemented using the PyTorch framework, with the quantum components simulated using the PennyLane
library51. All training and evaluation experiments were conducted on a high-performance computing node equipped with an
NVIDIA A100 40GB GPU, a 60-core CPU, and 120GB of RAM. Given the extensive hyperparameter space, the grid search
was computationally intensive, requiring significant runtime to systematically evaluate all possible configurations and identify
the optimal model for each experiment. Design Rationale
The selection of model configurations was guided by both theoretical considerations and empirical evidence from prior quantum
machine learning studies. Among embedding methods, Angle and Amplitude embeddings were chosen for their proven
compatibility with variational quantum circuits and ability to encode continuous-valued acoustic features efficiently within
limited qubit budgets52,53. IQP embedding was included for comparison due to its strong expressibility properties. For circuit
types, Strongly Entangling Layers and Random Layers were selected to explore the trade-off between structured and stochastic
entanglement generation; both have been shown to yield highly expressive quantum states while maintaining trainability. The
hyperparameter values, including optimisers and learning rates, were determined through grid search (Table 2) to ensure
reproducibility and unbiased model selection. These choices collectively aim to balance model expressibility, training stability,
and computational feasibility under NISQ constraints. Furthermore, fixing the quantum circuit to n = 8 qubits across all
embedding types ensured architectural consistency and parameter parity, enabling direct comparison of embedding effectiveness
without the confounding effect of varying qubit counts.
9/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Baseline Classical Model
To ensure a fair comparison between the hybrid classical–quantum model and the purely classical baseline, we replaced the
quantum representation learning block with a dimensionality adaptor. This adaptor consists of a flattening operation followed
by a fully connected linear layer that projects the CNN feature maps into the same dimensional space expected by the classifier. While this makes the overall architecture structurally similar, it is not identical to the hybrid model, as the quantum block
introduces a distinct representational learning mechanism. Therefore, we use the term “classical baseline” rather than “identical
model” to acknowledge this structural difference. This design choice ensures that any observed performance differences can be
attributed specifically to the quantum block rather than architectural mismatches. The architecture of the classical model used
in this study is illustrated in Figure 4. Classification Block
Representation Learning Block - Classical
Input Mel-Spectrogram
CNN
Batch
Normalise
CNN
Batch
Normalise
Fully Connected Layer 1
Fully Connected Layer 2
Output Layer
Dimensionality  Adapter
Figure 4. Architecture of the classical model used in this study. The input Mel-spectrogram is processed through a
CNN-based representation learning block, followed by a dimensionality adaptor that feeds into the classification block. The
final output layer generates predictions using a softmax function. Evaluation Metrics
We evaluate model performance using the Unweighted Average Recall (UAR, %), a widely adopted metric in speech-based
machine learning research54–57. UAR is calculated by first computing the recall for each class label in the classification task
and then averaging these recall values equally across all labels. Experiments
We designed our experiments to address two primary scenarios: binary classification and multi-class emotion classification.
• Binary Classification: The objective of this task was to classify input speech samples into one of two categories: “High”
or “Low” valence. For this evaluation, we utilised the IEMOCAP and RECOLA datasets, which are well-suited for
valence-based classification.
• Multi-Class Emotion Classification: This task aimed to identify the specific emotion conveyed in the input speech,
selecting from the categories: happy, angry, sad, or neutral. For this purpose, we employed the IEMOCAP and
MSP-Improv datasets, which offer comprehensive annotations for a diverse range of emotions. Evaluation
This section presents the results of the experiments conducted in our study. The results of the binary classification are detailed in
subsection “Binary Classification”, while those of the multi-class classification are provided in subsection “Multi-class Emotion
Classification”. Performance is evaluated using UAR%, while the number of trainable parameters is reported to indicate the
relative complexity of each model. Alongside UAR, we also evaluate model complexity by reporting the number of trainable parameters. For the classical
CNN baseline, the parameter count was obtained directly by summing all learnable weights and biases across convolutional
filters, batch-normalisation layers, and fully connected layers, using the PyTorch model.parameters() utility. For the hybrid
model, the total count is composed of both the CNN parameters and the additional parameters introduced by the PQC. In
the PQC, only the rotation gates (e.g., Rx, Ry, Rz) are trainable 34,58, while entangling operations such as CNOTs are fixed
and therefore do not contribute parameters. For a strongly entangling layer with n qubits, the number of trainable parameters
10/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## UAR (%)

64.68%
61.36%
80.85%
74.42%
55.93%
52.54%
34.6%
32.78%
Hybrid Classical-Quantum
Classical
(a) IEMOCAP Binary
(b) RECOLA Binary
(c) IEMOCAP Multi-Class
(d) MSP-Improv Multi-Class
Experiments
0.0
0.5
1.0
1.5
2.0
No. Parameters (106)
1,122,792
2,261,186
1,122,834
2,261,186
1,122,810
2,261,316
1,122,810
2,261,316
UAR(%) and No. Parameters Comparision
Figure 5. Comparison of UAR (%) and Number of Parameters with Hybrid classical-quantum model and Classical Model in
the experiments (a) IEMOCAP Binary Classification, (b) RECOLA Binary Classification, (c) IEMOCAP Multi-class
Classification, and (d) MSP-Improv Multi-class Classification.
grows linearly as NPQC = 3nL where n is the number of qubits and L is the number of circuit layers. In this study, with n = 8
qubits, each layer contributes 24 parameters, and the depth L scales this count proportionally. This results in a PQC with only a
few hundred trainable parameters, compared to the millions of weights typically present in the CNN’s fully connected layers. The final parameter counts reported in Figure 5 and Table 3 were obtained by combining the CNN parameters and the PQC
parameters, ensuring a fair and consistent comparison of model complexity between the classical and hybrid architectures. Binary Classification
In this section, we evaluate the binary classification performance of the hybrid classical-quantum models within the SER
domain. The experiments were conducted using the IEMOCAP and RECOLA datasets. The objective was to classify speech
emotion into one of two dimensional labels: Valence – High or Low. IEMOCAP
The IEMOCAP dataset is annotated with both categorical and dimensional emotional labels. For the valence dimension,
annotations range from 1 to 5. We categorised valence as “Low” for values less than 3 and “High” for values 3 and above. Figure 5(a) illustrates the UAR% and the number of trainable parameters for the best-performing model obtained through
grid search. The hyper-parameters selected from the grid search for the best performing model are:
• Learning Rate: 0.00001
• Optimiser: Adam Optimiser with zero weight decay
• Quantum Layer: Angle Embedding, Random Layers as Quantum Circuit and Summation of Z and PauliZ measurements
as Quantum Measurement.
11/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

It also shows the comparison with the corresponding classical baseline model described earlier, ensuring a fair and
parameter-matched comparison. Analysing the UAR% results, the hybrid classical-quantum model outperforms the identical classical DNN model. This
suggests that the inclusion of the “Quantum representation learning block” contributes significantly to the observed performance
improvement31,32. Also, the hybrid classical-quantum model has nearly as half of the number of parameters which indicates the reduced
training complexity of the model. RECOLA
The RECOLA dataset is an annotated resource containing multiple markers for emotion recognition. For this binary classification
task in SER, we focused on the valence dimension. Valence in the RECOLA dataset is annotated with positive and negative
values. We categorised negative valence values as “Low” and positive valence values as “High”. Figure 5(b) presents the UAR% and the number of trainable parameters for each hybrid classical-quantum model and its
corresponding classical model. The best-performing quantum model, selected via grid search, is configured with the following
hyper-parameters:
• Learning Rate: 0.00001
• Optimiser: Stochastic Gradient Descent (SGD) with zero weight decay
• Quantum Layer: Amplitude Embedding, Strongly Entangling Layers for the Quantum Circuit, and PauliX for Quantum
Measurement
From the results, the hybrid classical-quantum model demonstrates superior performance compared to its classical
counterpart, achieving this with nearly half the number of trainable parameters. Multi-class Emotion Classification
In this section, we assess the multi-class emotion classification performance of the hybrid classical-quantum models in the SER
domain. The experiments were conducted using the IEMOCAP and MSP-Improv datasets. The goal was to classify speech
emotions into one of four categorical labels: Angry, Happy, Neutral, and Sad. IEMOCAP
In this scenario, we utilise the categorical annotations of the IEMOCAP dataset. Figure 5(c) presents the performance comparison between the best quantum model and its classical counterpart. When comparing Figure 5(a) and Figure 5(c), it is evident that the UAR% for the multi-class classification task is lower. This decline in performance can be attributed to the increased complexity of the SER task and the higher number of output
classes. However, the quantum model demonstrates higher accuracy compared to the corresponding classical model in this
multi-class scenario. The selected model employs the following hyper-parameters:
• Learning Rate: 0.001
• Optimiser: Stochastic Gradient Descent (SGD) with zero weight decay
• Quantum Layer: Angle embedding, random layers as the quantum circuit, and a combination of Z and PauliZ measure-
ments for quantum measurement
When compared to the binary classification experiments on the IEMOCAP dataset, the same quantum layer configuration is
observed for both binary and multi-class scenarios. This suggests that the parameters of the quantum layer should be tailored to
the underlying data distribution. MSP-Improv
We use four categorical emotions (Angry, Happy, Neutral, and Sad) annotated in the MSP-Improve dataset. The task of this
classification model is to correctly classify the emotion embedded in the audio. Figure 5(d) compares the performance and the complexity of the best quantum model selected by the grid search and the
corresponding classical model. The hyper-parameters selected by grid search for the best performing quantum model are:
• Learning Rate: 0.0001
• Optimiser: AdaGrad optimiser with zero weight decay
• Quantum Layer: Angle embedding, random layers as the quantum circuit, and PauliZ measurements for quantum
measurement
12/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Analysis on Representation Learning
To examine the quality of the representations learned by the proposed hybrid model and to facilitate a direct comparison with
the classical baseline, we extracted the feature spaces obtained after the Input Layer and the Feature Extraction block. The
Adjusted Rand Index (ARI) was then computed to evaluate the alignment between the clusters formed within these feature
spaces and the true emotion class labels59. A higher ARI value indicates a stronger agreement, reflecting how effectively the
learned representations capture the underlying emotional structure of the data. Figure 6 presents the ARI values derived from the feature spaces of the Input Layer and the Feature Extraction Block for both
the classical and quantum models. As expected, the ARI values at the Input Layer are low, indicating limited agreement between
the learned representations and the output classes, since the early layers have insufficient information to form discriminative
features. In contrast, the ARI values obtained after the Feature Extraction Block are notably higher for both models, suggesting
that the learned representations align more closely with the emotion classes. Notably, the quantum model achieves a higher ARI
compared to the classical counterpart, demonstrating that its learned features exhibit stronger class separability—consistent
with its superior classification performance. Input Layer
Feature Extraction Block
Layer
0.00
0.05
0.10
0.15
0.20
0.25
Adjusted Rand Index
Clustering Agreement (Adjusted Rand Index)
Model
Hybrid Classical-Quantum
Classical
Figure 6. Adjusted Rand Index (ARI) values from the feature spaces of the Input Layer and Feature Extraction Block for the
classical and quantum models. The low ARI at the Input Layer indicates limited class information, while higher ARI values
after feature extraction show improved feature–class alignment. The quantum model’s higher ARI demonstrates stronger class
separability, consistent with its superior accuracy. Summary of the Results
A summary of the results obtained by the experiments in this study is tabulated in the Table 3. The results demonstrate the
effectiveness of the hybrid classical-quantum model for SER tasks, highlighting superior performance and reduced complexity
13/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

compared to classical models. For binary classification on the IEMOCAP dataset, the hybrid model achieved a UAR of 64.68%,
outperforming the classical model’s 61.36%, with 50.34% fewer trainable parameters. Table 3. UAR (%) of Best Quantum Model and corresponding Classical Model along with the Hyper-parameters selected by
Grid Search. Hyper
Parameter
Dataset
IEMOCAP
Binary
RECOLA
Binary
IEMOCAP

### 4 Class

MSP-Improv

### 4 Class

Learning Rate
0.00001
0.00001
0.001
0.0001
Optimiser
Adam
SGD
SGD
AdaGrad
Weight Decay

Q. Embedding
Angle Embedding
Amplitude Embedding
Angle Embedding
Angle Embedding
Q. Circuit Layer
Random Layers
Strongly Entangling Layers
Random Layers
Random Layers
Q. Measurement
Z + PauliZ
PauliX
Z + PauliZ
PauliZ

## UAR (%)

Quantum
64.68 ± 3.34
80.85 ± 4.45
55.93 ± 4.62
34.60 ± 5.19

## UAR (%)

Classical
61.36 ± 3.21
74.42 ± 5.28
52.54 ± 7.56
32.78 ± 4.32
Similarly, for the RECOLA dataset, the hybrid model recorded a UAR of 80.85%, considerably higher than the classical
model’s 74.42%, while maintaining the same parameter efficiency. In multi-class classification, the hybrid model also
outperformed its classical counterpart, achieving a UAR of 55.93% on the IEMOCAP dataset (versus 52.54%) and 34.60% on
MSP-Improv (versus 32.78%), again with reduced complexity. Across all tasks, optimal configurations for the hybrid model
consistently included zero weight decay and specific quantum embeddings, such as angle or amplitude embedding, paired with
random or strongly entangling quantum layers. These results highlight the potential of integrating quantum feature extraction
into SER models, offering improved accuracy and efficiency in handling complex emotional data. Discussion and Future Work
The results of the study highlight how well the proposed hybrid classical-quantum framework can handle the challenges that
come with SER. The work shows that combining PQCs with a traditional CNN substantially decreases model complexity while
improving classification performance on both binary and multi-class problems. For binary classification tasks, the hybrid models demonstrated higher accuracies on both the IEMOCAP and RECOLA
datasets, consistently outperforming their classical counterparts in terms of UAR(%). The quantum layer’s potential to
utilise entanglement and superposition, which enhance feature representation and capture subtle relationships among speech
components, contributes for these improvements. Among the tested circuit configurations, random circuits demonstrated
particularly strong performance. This can be attributed to their high expressibility, enabling the model to capture a broader
range of feature correlations in the quantum state space. The stochastic yet trainable nature of the random layers facilitates
more diverse quantum feature representations, which likely enhances generalisation across datasets. Furthermore, the hybrid
approach’s effectiveness is demonstrated by a reduction in the number of trainable parameters, which makes it an intriguing
option for situations with limited resources. The hybrid framework had slightly lower UAR(%) values than binary tasks, but it still performed better for multi-class
classification. The higher complexity involved in identifying more subtle emotional states is consistent with this outcome. The
quantum-enhanced model proved stable in spite of this difficulty, especially when tested on the MSP-Improv dataset, which
includes a variety of emotional expressions. Key Observations
Key observations observed throughout this study are;
• The experiments reveal that quantum embeddings and circuit configurations (e.g., Angle Embedding and Strongly
Entangling Layers) are critical to achieving optimal performance. The observed consistency in selected quantum
components across binary and multi-class tasks suggests a potential universality of these configurations for SER tasks.
14/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

• The absence of weight decay in the best-performing models indicates that quantum layers inherently provide sufficient
regularisation.
• The hybrid models’ reduced parameter count underscores their suitability for deployment in real-world scenarios where
computational resources and energy efficiency are critical constraints. Lessons Learnt
The development of the hybrid classical-quantum framework presented in this paper involved a significant exploration of
different architectural and methodological approaches. Before arriving at the final design, several alternative strategies were
implemented and evaluated, providing valuable insights into the challenges and opportunities of integrating QML with SER. These explorations highlighted the complexities of leveraging quantum properties effectively and guided the iterative refinement
of the model towards improved performance and efficiency.
(a) 2-CNOT
(b) 3-CNOT
(c) 4-CNOT
Figure 7. 2-CNOT, 3-CNOT, and 4-CNOT quantum circuits we used in the experiments
Our initial investigations focused on incorporating static quantum circuits within established deep learning architectures. We hypothesised that these circuits, despite their fixed structure, could offer advantages in feature extraction due to their ability
to exploit quantum phenomena like superposition. A variety of circuit configurations, including those based on 2-CNOT,
3-CNOT, and 4-CNOT gates (Figure 7), were designed and tested. The output of these static quantum circuits, essentially
quantum measurements representing extracted features, were then passed as input to various classical deep learning models. These included standard CNNs, LSTMs for capturing temporal dependencies, multi-kernel CNNs to explore different receptive
fields, and combinations of CNNs and LSTMs (Figure 8 (a)). However, across these various architectures and circuit designs,
the performance on benchmark datasets like IEMOCAP remained consistently below 49% accuracy. This suggested that the
static nature of these circuits limited their ability to adapt to the nuances and complexities of emotional expression in speech
data. Static Quantum Circuit
CNN Layer
Fully Connected Layer
Output Layer
Input Spectrogram
(a) CNN-based SER model architecture employing a static quantum circuit as the feature extractor
2-CNOT
Output Layer
Input Spectrogram
3-CNOT
4-CNOT
Fusion
CNN Layer
Fully Connected Layer
(b) A fusion-based SER model architecture employing three static quantum circuits to extract and early-fuse the features. Figure 8. Two of the model architectures employed in our experiments involving static quantum circuits. Subsequently, we explored the potential of fusion-based models, aiming to combine the strengths of both quantum and
classical processing. Two primary fusion strategies were investigated: early fusion and decision-level fusion. In the early
15/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

fusion approach, the outputs of the static quantum circuits and the classical CNNs were concatenated before being passed to a
final classification layer (Figure 8 (b)). This aimed to leverage both quantum and classical features in the decision-making
process. The decision-level fusion approach, on the other hand, involved training separate quantum and classical models, and
their respective classification outputs were then combined using techniques like averaging or weighted averaging. Despite the
conceptual appeal of these fusion strategies, the observed performance gains were marginal, with accuracies hovering around
44% on the IEMOCAP dataset. This suggested that simply combining static quantum computations with classical deep learning
was insufficient to capture the intricate relationships within emotional speech data. Further experimentation delved into the role of regularisation within these hybrid models. Specifically, we investigated
the impact of L2 regularisation, commonly used to prevent over-fitting in classical deep learning. We observed a clear trend:
increasing the weight decay (the hyperparameter controlling L2 regularisation) improved the performance of the classical CNN
components. However, the same trend was not observed for the quantum components, suggesting that they might possess
inherent regularisation properties due to the constraints of the quantum Hilbert space. The culmination of these explorations led to the realisation that the fixed nature of static quantum circuits was a limiting
factor in achieving optimal performance. This prompted the shift towards PQCs, which allow for adaptive learning through
the optimisation of circuit parameters. The flexibility of PQCs, combined with carefully chosen quantum embeddings and
circuit architectures, proved to be the key to unlocking the potential of QML for SER, as demonstrated by the improved results
presented in this study. This journey emphasises the significance of systematic exploration and iterative refinement in the
nascent field of QML, laying the groundwork for future research to further optimise and expand upon these promising initial
discoveries. Limitations of the Proposed Model
While the hybrid framework offers promising results, several limitations merit discussion. First, the study relies on simulated
quantum environments, which may not fully capture the hardware-related challenges and noise associated with physical
quantum systems. Future work should validate these findings on real quantum devices to assess their practical applicability. Additionally, the current approach uses fixed configurations for the classical CNN component. Exploring alternative
architectures, such as transformer-based models, could further enhance performance by leveraging their strengths in capturing
long-term dependencies. Finally, the scope of datasets used in this study, though diverse, does not encompass all linguistic and cultural variations
in emotional speech. Expanding the evaluation to include more diverse datasets would provide a more comprehensive
understanding of the model’s generalisation capacity. Conclusion
This paper has introduced a novel hybrid classical-quantum framework for Speech Emotion Recognition (SER), leveraging
the power of Parameterised Quantum Circuits (PQCs) integrated within a Convolutional Neural Network (CNN) architecture. By harnessing the principles of quantum superposition and entanglement, the proposed model demonstrates a significant
improvement in both accuracy and model efficiency. The experimental results across three widely used benchmark datasets – IEMOCAP, RECOLA, and MSP-Improv –
consistently showcase the superior performance of the hybrid classical-quantum model compared to its purely classical
counterpart. Notably, the hybrid models achieve enhanced accuracy in both binary and multi-class emotion classification tasks,
while simultaneously reducing the number of trainable parameters by 50.34%. This reduction in model complexity translates to
lower computational overhead and improved energy efficiency, rendering these quantum-enhanced methods more suitable for
practical real-world applications. Furthermore, the study reveals crucial insights into optimal configurations for hybrid classical-quantum models in SER. The experiments suggest that specific quantum embeddings, such as Angle and Amplitude embedding, coupled with strongly
entangling or random quantum circuit layers, and a summation of Pauli Z measurements consistently contribute to superior
performance. The absence of weight decay in these optimal configurations implies that L2 regularisation might not be necessary
for such hybrid models. Notably, the optimal configurations consistently emerge with zero weight decay. This directly supports
the observation from Section “Key Observations”, which indicates that the quantum layers inherently provide sufficient
regularisation. This behaviour suggests that classical techniques like L2 regularisation may be redundant, potentially due to
the intrinsic properties and constraints of the quantum Hilbert space, simplifying the training process. These findings provide
valuable guidance for future research and development in quantum-enhanced SER. While these results are promising, the study also acknowledges certain limitations. Firstly, the experiments were performed
using simulated quantum environments. Future studies should validate these findings on physical quantum devices. Secondly,
the current implementation uses a fixed architecture for the classical CNN component; exploring alternative architectures could
16/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

be an avenue for further improvement. Finally, the dataset diversity should be expanded in future studies to better understand
the models’ generalisation capacity across various linguistic and cultural contexts. In summary, this study demonstrates the potential of quantum machine learning to revolutionise the field of SER. By
integrating PQCs with classical CNNs, our proposed framework achieves improved accuracy and reduced complexity, paving
the way for the development of more robust and efficient SER models for real-world applications. The future work includes
extending these experiments on a quantum hardware and implementing more robust feature extraction methods for the CNN
model. References

### 1. Shah Fahad, M., Ranjan, A., Yadav, J. & Deepak, A. A survey of speech emotion recognition in natural environment. Digit. Signal Process. 110, 102951, DOI: 10.1016/J. DSP.2020.102951 (2021).

### 2. Daneshfar, F. & Kabudian, S. J. Speech Emotion Recognition Using Multi-Layer Sparse Auto-Encoder Extreme Learning

Machine and Spectral/Spectro-Temporal Features with New Weighting Method for Data Imbalance. ICCKE 2021 - 11th
Int. Conf. on Comput. Eng. Knowl. 419–423, DOI: 10.1109/ICCKE54056.2021.9721524 (2021).

### 3. George, S. M. & Muhamed Ilyas, P. A review on speech emotion recognition: A survey, recent advances, challenges, and

the influence of noise. Neurocomputing 568, 127015, DOI: 10.1016/J. NEUCOM.2023.127015 (2024).

### 4. Sharma, D., Singh, P. & Kumar, A. The role of entanglement for enhancing the efficiency of quantum kernels towards

classification. Phys. A: Stat. Mech. its Appl. 625, 128938, DOI: 10.1016/J. PHYSA.2023.128938 (2023).

### 5. Wang, X. et al. Transition role of entangled data in quantum machine learning. Nat. Commun. 2024 15:1 15, 1–8, DOI:

10.1038/s41467-024-47983-1 (2024).

### 6. WANG, X. et al. Exploring the Power of Entangled Data in Quantum Machine Learning. Wuhan Univ. J. Nat. Sci. 29,

## 193–194, DOI: 10.1051/WUJNS/2024293193 (2024).

### 7. Gaspar, J. M., Bergerault, A., Apostolou, V. & Ricou, A. Entanglement-enhanced Quantum Reinforcement Learning:

an Application using Single-Photons. 2024 IEEE Int. Conf. on Quantum Comput. Eng. (QCE) 329–334, DOI: 10.1109/

## QCE60285.2024.10301 (2024).

### 8. Farhi, E. & Neven, H. Classification with Quantum Neural Networks on Near Term Processors. arXiv: Quantum Phys.

(2018).

### 9. Trigeorgis, G. et al. Adieu features? End-to-end speech emotion recognition using a deep convolutional recurrent network. ICASSP, IEEE Int. Conf. on Acoust. Speech Signal Process. - Proc. 5200–5204, DOI: 10.1109/ICASSP.2016.7472669
(2016).

### 10. Stolar, M. N., Lech, M., Bolia, R. S. & Skinner, M. Real time speech emotion recognition using RGB image classification

and transfer learning. 2017, 11th Int. Conf. on Signal Process. Commun. Syst. ICSPCS 2017 - Proc. 2018-January, 1–8,

## DOI: 10.1109/ICSPCS.2017.8270472 (2018).

### 11. Pan, L. & Wang, Q. GFRN-SEA: Global-Aware Feature Representation Network for Speech Emotion Analysis. IEEE

Access DOI: 10.1109/ACCESS.2024.3490186 (2024).

### 12. Zhang, X., Fu, W. & Liang, M. Multimodal Emotion Recognition from Raw Audio with Sinc-convolution. arXiv: Sound

(2024).

### 13. Etienne, C., Fidanza, G., Petrovskii, A., Devillers, L. & Schmauch, B. CNN+LSTM Architecture for Speech Emotion

Recognition with Data Augmentation. In Workshop on Speech, Music and Mind (SMM 2018), DOI: 10.21437/SMM.2018-5

## (ISCA, ISCA, 2018).

### 14. Rayhan Ahmed, M., Islam, S., Muzahidul Islam, A. K. & Shatabda, S. An ensemble 1D-CNN-LSTM-GRU model with data

augmentation for speech emotion recognition. Expert. Syst. with Appl. 218, 119633, DOI: 10.1016/J. ESWA.2023.119633
(2023).

### 15. Satt, A., Rozenberg, S. & Hoory, R. Efficient Emotion Recognition from Speech Using Deep Learning on Spectrograms. Proc. Annu. Conf. Int. Speech Commun. Assoc. INTERSPEECH 2017-August, 1089–1093, DOI: 10.21437/INTERSPEECH.
2017-200 (2017).

### 16. Zhao, J., Mao, X. & Chen, L. Speech emotion recognition using deep 1D & 2D CNN LSTM networks. Biomed. Signal

Process. Control. 47, 312–323, DOI: 10.1016/J. BSPC.2018.08.035 (2019).

### 17. Xie, Y. et al. Speech Emotion Classification Using Attention-Based LSTM. IEEE/ACM Transactions on Audio Speech

Lang. Process. 27, 1675–1685, DOI: 10.1109/TASLP.2019.2925934 (2019).
17/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

### 18. Mirsamadi, S., Barsoum, E. & Zhang, C. Automatic speech emotion recognition using recurrent neural networks with

local attention. ICASSP, IEEE Int. Conf. on Acoust. Speech Signal Process. - Proc. 2227–2231, DOI: 10.1109/ICASSP.
2017.7952552 (2017).

### 19. Hsu, W. N. et al. HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units. IEEE/ACM Transactions on Audio, Speech, Lang. Process. 29, 3451–3460, DOI: 10.1109/TASLP.2021.3122291 (2021).

### 20. Li, R. et al. Towards discriminative representation learning for speech emotion recognition. IJCAI Int. Jt. Conf. on Artif. Intell. 2019-August, 5060–5066, DOI: 10.24963/IJCAI.2019/703 (2019).

### 21. Latif, S. et al. Survey of Deep Representation Learning for Speech Emotion Recognition. IEEE Transactions on Affect. Comput. 14, 1634–1654, DOI: 10.1109/TAFFC.2021.3114365 (2023).

### 22. Jahangir, R., Teh, Y. W., Hanif, F. & Mujtaba, G. Deep learning approaches for speech emotion recognition: state of the

art and research challenges. Multimed. Tools Appl. 80, 23745–23812, DOI: 10.1007/S11042-020-09874-7/FIGURES/17
(2021).

### 23. Gong, L. H., Pei, J. J., Zhang, T. F. & Zhou, N. R. Quantum convolutional neural network based on variational quantum

circuits. Opt. Commun. 550, 129993, DOI: 10.1016/J. OPTCOM.2023.129993 (2024).

### 24. Rebentrost, P., Mohseni, M. & Lloyd, S. Quantum Support Vector Machine for Big Data Classification. Phys. Rev. Lett.

113, DOI: 10.1103/PhysRevLett.113.130503 (2014).

### 25. Biamonte, J. et al. Quantum machine learning. Nat. 2017 549:7671 549, 195–202, DOI: 10.1038/nature23474 (2017).

### 26. Cerezo, M. et al. Variational quantum algorithms. Nat. Rev. Phys. 2021 3:9 3, 625–644, DOI: 10.1038/s42254-021-00348-9

(2021).

### 27. Schuld, M. & Killoran, N. Quantum Machine Learning in Feature Hilbert Spaces. Phys. Rev. Lett. 122, 040504, DOI:

10.1103/PhysRevLett.122.040504 (2019).

### 28. Qu, Z., Chen, Z., Dehdashti, S. & Tiwari, P. QFSM: A Novel Quantum Federated Learning Algorithm for Speech

Emotion Recognition With Minimal Gated Unit in 5G IoV. IEEE Transactions on Intell. Veh. Early Access, 1–12, DOI:

## 10.1109/TIV.2024.3370398 (2024).

### 29. Liu, J. et al. Hybrid Quantum-Classical Convolutional Neural Networks. Sci. China: Physics, Mech. Astron. 64, DOI:

10.1007/s11433-021-1734-3 (2019).

### 30. Xiang, Q. et al. Quantum classical hybrid convolutional neural networks for breast cancer diagnosis. Sci. Reports 2024

14:1 14, 1–13, DOI: 10.1038/s41598-024-74778-7 (2024).

### 31. Thejha, B., Yogeswari, S., Vishalli, A. & Jeyalakshmi, J. Speech Recognition Using Quantum Convolutional Neural

Network. Proc. 8th IEEE Int. Conf. on Sci. Technol. Eng. Math. ICONSTEM 2023 DOI: 10.1109/ICONSTEM56934.2023.
10142793 (2023).

### 32. Esposito, M., Uehara, G. & Spanias, A. Quantum Machine Learning for Audio Classification with Applications to

Healthcare. 13th Int. Conf. on Information, Intell. Syst. Appl. IISA 2022 DOI: 10.1109/IISA56318.2022.9904377 (2022).

### 33. Norval, M. & Wang, Z. Quantum AI in Speech Emotion Recognition. PREPRINT (Version 1) DOI: 10.21203/RS.3.

## RS-4894795/V1 (2024).

### 34. Cong, I., Choi, S. & Lukin, M. D. Quantum convolutional neural networks. Nat. Phys. 2019 15:12 15, 1273–1278, DOI:

10.1038/s41567-019-0648-8 (2019).

### 35. Muguli, A. et al. DiCOVA Challenge: Dataset, Task, and Baseline System for COVID-19 Diagnosis Using Acoustics. Proc. Annu. Conf. Int. Speech Commun. Assoc. INTERSPEECH 6, 901–905, DOI: 10.21437/INTERSPEECH.2021-74 (2021).

### 36. Tao, J., Liu, F., Zhang, M. & Jia, H. Design of Speech Corpus for Mandarin Text to Speech (2008).

### 37. Livingstone, S. R. & Russo, F. A. The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS): A

dynamic, multimodal set of facial and vocal expressions in North American English. PLOS ONE 13, e0196391, DOI:

## 10.1371/JOURNAL. PONE.0196391 (2018).

### 38. Burkhardt, F., Paeschke, A., Rolfes, M., Sendlmeier, W. & Weiss, B. A Database of German Emotional Speech. In

Interspeech, 1517–1520 (Lisbona, 2005).

### 39. Busso, C. et al. IEMOCAP: interactive emotional dyadic motion capture database. Lang. Resour. Eval. 42, 335, DOI:

10.1007/s10579-008-9076-6 (2008).
18/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

### 40. Ringeval, F., Sonderegger, A., Sauer, J. & Lalanne, D. Introducing the RECOLA multimodal corpus of remote collaborative

and affective interactions. 2013 10th IEEE Int. Conf. Work. on Autom. Face Gesture Recognition, FG 2013 DOI:

## 10.1109/FG.2013.6553805 (2013).

### 41. Busso, C. et al. MSP-IMPROV: An Acted Corpus of Dyadic Interactions to Study Emotion Perception. IEEE Transactions

on Affect. Comput. 8, 67–80, DOI: 10.1109/TAFFC.2016.2515617 (2017).

### 42. Issa, D., Fatih Demirci, M. & Yazici, A. Speech emotion recognition with deep convolutional neural networks. Biomed. Signal Process. Control. 59, 101894, DOI: 10.1016/j.bspc.2020.101894 (2020).

### 43. Chen, S. et al. The Impact of Attention Mechanisms on Speech Emotion Recognition. Sensors 21, 7530, DOI: 10.3390/

s21227530 (2021).

### 44. Havlíˇcek, V. et al. Supervised learning with quantum-enhanced feature spaces. Nat. 2019 567:7747 567, 209–212, DOI:

10.1038/s41586-019-0980-2 (2019).

### 45. Schuld, M., Bocharov, A., Svore, K. M. & Wiebe, N. Circuit-centric quantum classifiers. Phys. Rev. A 101, 032308, DOI:

10.1103/PhysRevA.101.032308 (2020).

### 46. Likitha, M. S., Gupta, S. R. R., Hasitha, K. & Raju, A. U. Speech based human emotion recognition using MFCC. Proc. 2017 Int. Conf. on Wirel. Commun. Signal Process. Networking, WiSPNET 2017 2018-January, 2257–2260, DOI:

## 10.1109/WISPNET.2017.8300161 (2017).

### 47. Latif, S., Rana, R., Khalifa, S., Jurdak, R. & Epps, J. Direct Modelling of Speech Emotion from Raw Speech. In Proceedings

of the Annual Conference of the International Speech Communication Association, INTERSPEECH, 3920–3924 (2019).

### 48. Patni, H., Jagtap, A., Bhoyar, V. & Gupta, A. Speech Emotion Recognition using MFCC, GFCC, Chromagram and RMSE

features. Proc. 8th Int. Conf. on Signal Process. Integr. Networks, SPIN 2021 892–897, DOI: 10.1109/SPIN52536.2021.
9566046 (2021).

### 49. Dolka, H., Arul Xavier, M. V. & Juliet, S. Speech emotion recognition using ANN on MFCC features. 2021 3rd Int. Conf.

on Signal Process. Commun. ICPSC 2021 431–435, DOI: 10.1109/ICSPC51351.2021.9451810 (2021).

### 50. Myung, J. I., Cavagnaro, D. R. & Pitt, M. A. A tutorial on adaptive design optimization. J. Math. Psychol. 57, 53–67, DOI:

## 10.1016/J. JMP.2013.05.005 (2013).

### 51. Bergholm, V. et al. PennyLane: Automatic differentiation of hybrid quantum-classical computations. arxiv (2018).

### 52. Huang, H. Y. et al. Power of data in quantum machine learning. Nat. Commun. 12, 1–9, DOI: 10.1038/S41467-021-22539-9;

## TECHMETA (2021).

### 53. Rath, M. & Date, H. Continuous Variable Quantum Encoding Techniques A Comparative Study of Embedding Techniques

and Their Impact on Machine Learning Performance. arXiv: Quantum Phys. (2025).

### 54. Mao, Q., Xue, W., Rao, Q., Zhang, F. & Zhan, Y. Domain adaptation for speech emotion recognition by sharing priors

between related source and target classes. In 2016 IEEE International Conference on Acoustics, Speech and Signal
Processing (ICASSP), 2608–2612, DOI: 10.1109/ICASSP.2016.7472149 (IEEE, 2016).

### 55. Ahn, Y., Lee, S. J. & Shin, J. W. Cross-Corpus Speech Emotion Recognition Based on Few-Shot Learning and Domain

Adaptation. IEEE Signal Process. Lett. 28, 1190–1194, DOI: 10.1109/LSP.2021.3086395 (2021).

### 56. Ishaq, M., Khan, M. & Kwon, S. TC-Net: A Modest & Lightweight Emotion Recognition System Using Temporal

Convolution Network. Comput. Syst. Sci. Eng. 46, 3355–3369, DOI: 10.32604/CSSE.2023.037373 (2023).

### 57. Khan, M., Gueaieb, W., El Saddik, A. & Kwon, S. MSER: Multimodal speech emotion recognition using cross-attention

with deep fusion. Expert. Syst. with Appl. 245, 122946, DOI: 10.1016/J. ESWA.2023.122946 (2024).

### 58. Sim, S., Johnson, P. D. & Aspuru-Guzik, A. Expressibility and entangling capability of parameterized quantum circuits for

hybrid quantum-classical algorithms. Adv. Quantum Technol. 2, DOI: 10.1002/qute.201900070 (2019).

### 59. Qiu, J. et al. Deep representation learning for clustering longitudinal survival data from electronic health records. Nat. Commun. 16, 1–14, DOI: 10.1038/S41467-025-56625-Z; SUBJMETA (2025). Data Availability
This study uses three publicly available datasets widely used in the field of speech emotion recognition.

### 1. IEMOCAP39 - Carlos Busso, Murtaza Bulut, Chi-Chun Lee, Abe Kazemzadeh, Emily Mower, Samuel Kim, Jeannette N

Chang, Sungbok Lee, Shrikanth S Narayanan (2018). Dataset: IEMOCAP. DOI: https://doi.org/10.1007/
s10579-008-9076-6
19/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

### 2. MSP-Improv41 - Carlos Busso, Srinivas Parthasarathy, Alec Burmania, Mohammed AbdelWahab, Najmeh Sadoughi, Emily Mower Provost (2017) Dataset: MSP-Improv. DOI: https://doi.org/10.1109/TAFFC.2016.2515617

### 3. RECOLA40 - Fabien Ringeval, Andreas Sonderegger, Juergen Sauer, Denis Lalanne (2013) Dataset: RECOLA. DOI: https://doi.org/10.1109/FG.2013.6553805
Author contributions statement
T. R. Researching the literature’s technique, gathering and analysing data, programming the experiments, generating tables and
figures, and writing and editing the manuscript, R. R. Supervised, edited and prepared the manuscript for submission, and offered
insightful and thorough feedback. Suggestions on selecting a journal, F. R contributed in developing model principles, reviewed
the manuscript for submission, and offered insightful feedback. Suggestions on selecting a journal, S. K Supervised, edited and
prepared the manuscript for submission, and offered insightful and thorough feedback, and B. S Editing and proofreading the
manuscript, feedback on experimental results, results interpretation. Funding
The Authors received NO FUNDING for this work.
20/20

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS
