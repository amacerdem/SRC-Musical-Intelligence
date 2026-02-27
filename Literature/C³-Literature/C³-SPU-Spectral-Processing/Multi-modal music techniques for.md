# Multi-modal music techniques for

**Year:** D:20

---

Multi-modal music techniques for
synthesizing high-quality audio
waveforms from MIDI data
Xi Zhang
1 & Yan Huang
2
A highly effective music synthesizer should deliver high-fidelity audio for a mix of instruments and
voices. Current synthesizers often need to choose between specialized models that provide detailed
control over specific instruments and flexible waveform models that accommodate a variety of music
at the expense of precision. To transcend the existing limitations, this paper introduces MIAO, an
avant-garde neural music synthesizer that revolutionizes the domain of interactive and expressive
music synthesis by converting MIDI sequences into rich, dynamic audio outputs. Specifically, MIAO can be cultivated through training on diverse transcription datasets that correlate MIDI
with audio, thereby deepening its comprehension of MIDI intricacies and elevating its capacity for
robust representation learning. This approach allows MIAO to offer precise note-level control over
composition and instrumentation, effectively handling a wide spectrum of instruments. We evaluate
MIAO’s performance by benchmarking it against six datasets: MAESTROv3 (piano), Slakh2100
(synthetic multi-instrument), Cerberus4 (synthetic multi-instrument), Guitarset (guitar), MusicNet
(orchestral multi-instrument), and URMP (orchestral multi-instrument), where it sets new performance
benchmarks. Keywords  Music synthesizer, MIDI, Multi-modal learning, Audio generation
Instrument music synthesis is a dynamic field within computational musicology that deals with the automated
generation of music from multiple instruments1–3. A fundamental component of this field involves the use of
MIDI (Musical Instrument Digital Interface) music, which refers to a digital music format that stores musical
information as a series of electronic messages containing performance data rather than audio waveforms4. This area integrates methodologies from computer vision and natural language processing to interpret and
replicate the multifaceted nature of orchestral and ensemble music5,6. As these technologies have matured,
they have greatly enhanced our capacity for audio analysis and the subsequent synthesis of complex musical
compositions7,8. The realm of multi-instrument music synthesis finds utility in a broad array of applications,
including but not limited to, the augmentation of interactive entertainment, the enrichment of virtual reality
environments9,10, the provision of adaptive background scores in film and gaming11,12, and the customization of
therapeutic soundscapes for health and wellness13–15. The field of multi-instrument music synthesis presents considerable challenges, primarily due to the inherent
compromises between model specialization and versatility16,17. Current synthesizers face a pivotal decision:
whether to use specialized models that offer precise control over individual instruments, thereby achieving high
harmony and accuracy in replicating the unique acoustic properties of those instruments18,19. These specialized
models excel in capturing the delicate nuances and expressive dynamics essential for defining the timbre and
articulation of specific instruments. However, the depth of control these models provide often comes at the
cost of flexibility, thereby restricting their use in a broader range of musical genres and the diverse instrument
arrangements found in multi-instrument compositions20,21. Additionally, flexible waveform models exist at the opposite end of the spectrum, crafted to be indifferent to
specific instrument types22,23. This design enables them to embrace a wide variety of musical styles and ensembles
under a unified framework, catering to the eclectic nature of multi-instrumental compositions24,25. While these
models excel in versatility, allowing for broad coverage of musical possibilities, they often do so at the cost of
precision26,27. The challenge here is the dilution of detail, where the intricacies of specific instrument sounds may
not be rendered with the same level of accuracy and authenticity as the specialized models8,28. This dichotomy
between specialization for depth and flexibility for breadth presents a significant hurdle in the pursuit of creating
1School of Arts, Sun Yat-sen University, Guangzhou 510275, China. 2School of Computer Science and Engineering, South China University of Technology, Guangzhou 510006, China. email: aihuangy@scut.edu.cn
OPEN
Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports

a universal music synthesis model that can not only generate a wide variety of music but also maintain the high
standards of precision required for professional audio production29,30. In order to address the limitations of traditional music synthesis approaches, we introduce the MIAO
synthesizer, a novel Multi-mode system that effectively converts MIDI inputs into high-fidelity AudiO outputs. The design of the MIAO synthesizer is focused on producing high-quality audio that accurately represents a
wide range of instruments and vocal textures, which are critical for realistic music synthesis. The architecture
of the MIAO synthesizer is built around three essential components: the MIDI Encoder, the Audio Decoder,
and the Audio Encoder. These elements are strategically implemented to ensure operational efficiency across
different phases of the synthesizer’s use: the MIDI Encoder and the Audio Decoder are active during both the
training and inference phases, while the Audio Encoder is specifically vital during the training phase to enhance
audio quality. Furthermore, this research introduces a supplementary training approach that enhances the performance
of the synthesizer beyond its innovative architecture. This scheme employs a dedicated encoder to process and
learn from paired MIDI and audio files encompassing a broad spectrum of sounds and instrumental timbres. The effectiveness of the MIAO synthesizer is enhanced through three targeted visual-linguistic objectives: MIDI-
audio contrastive learning, MIDI-audio matching, and MIDI-conditioned audio modeling. These objectives
are supported by training on diverse datasets that pair MIDI with corresponding audio files, reinforcing the
model’s ability to learn and adapt. Extensive experimental evaluations have demonstrated that these training
strategies significantly improve the MIAO synthesizer’s understanding of MIDI sequences and its ability to learn
representations. Such advancements enable the synthesizer to exert precise control over musical composition
and instrument processing at the note level, effectively managing a large repertoire of instruments. Consequently,
the MIAO synthesizer not only stands out as a technological breakthrough in music generation but also serves
as a versatile instrument for creative and interactive musical expression, validated by thorough experiments and
analyses. The main contributions in this paper are summarized as follows:
•	 In the burgeoning field of computational musicology, we propose MIAO, a multi-modal music synthesizer
that represents a significant leap forward in MIDI to high-fidelity audio conversion. MIAO is designed with
the ambition to close the quality and versatility gap that has long existed in musical synthesis, thereby offering
a more nuanced and richly textured musical generation capability.
•	 A training scheme that complements MIAO has been proposed, integrating three visual-linguistic objectives: MIDI-audio contrastive learning, MIDI-audio matching, and MIDI-conditioned audio modeling. These ob­
jectives are meticulously tailored to enhance the model’s understanding and replication of musical structure,
resulting in a more authentic and expressive synthesis of multi-instrumental compositions.
•	 In validating MIAO’s effectiveness, we benchmarked it across six datasets: MAESTROv3, Slakh2100, Cer­
berus4, Guitarset, MusicNet, and URMP, encompassing a range of instruments and musical styles. MIAO
consistently sets new performance benchmarks, demonstrating its exceptional performance and versatility in
multi-instrument music synthesis. Related work
Neural audio synthesis initially became viable with autoregressive models for raw waveforms, which sequentially
predict each audio sample based on all previous ones, establishing a foundation for various complex audio
generation tasks31. WaveNet32 is a fully probabilistic, autoregressive model that bases the prediction of each
audio sample on all preceding samples. In contrast, SampleRNN33 utilizes recurrent neural networks across
various scales to capture longer-term dependencies in audio waveforms, optimizing for memory efficiency
during training. The Generative Adversarial Network (GAN)34 has been effectively adapted for music generation,
facilitating the production of innovative audio waveforms and symbolic compositions that emulate learned
musical styles through adversarial training between a generator and a discriminator. WaveGAN35 diverges
from these approaches by generating audio in a single forward pass, focusing on unsupervised synthesis of
raw-waveform audio. GANSynth36 advances this further by producing high-fidelity and locally coherent audio,
modeling log magnitudes and instantaneous frequencies in the spectral domain. However, GANSynth, like other
GAN-based models, typically concentrates on generating single instruments, notes, or voices at a time37,38. Building on the foundations laid by autoregressive and GAN-based models, newer architectures further
expand the landscape of neural audio synthesis39. Soundstream utilizes Transformers to model the discrete,
vector-quantized codes of a foundational waveform autoencoder40. Tacotron41 architectures have shown the
efficacy of simple spectrograms for multi-stage audio generation, first creating continuous-valued spectrograms
autoregressively, followed by waveform synthesis using a neural vocoder. Denoising Diffusion Probabilistic
Models (DDPMs)42 transform random noise into realistic data through iterative refinement, using a forward
process that adds noise and a learned reverse process that removes it. These models outperform GANs in
generating high-quality, diverse outputs for audio and image synthesis, making them particularly effective for
music generation tasks. MI-DDPM43 adopts a two-stage training process: it initially uses an autoregressive
spectrogram generator alongside a GAN spectrogram inverter and then enhances this with a DDPM spectrogram
generator. However, these models require additional focus on spectrograms, along with MIDI inputs, and the
DDPM model faces challenges in effectively capturing the contextual representation of waveform autoregression
during training44. To address these challenges, we introduce an end-to-end neural music synthesizer, optimized
for high-quality audio generation across various instruments and voices. Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

Method
This section introduces MIAO, an advanced multi-modal music synthesizer that marks a substantial advancement
in converting MIDI to high-fidelity audio. MIAO is strategically crafted to bridge the longstanding divide in
quality and adaptability found in music synthesis, thus providing a more sophisticated and detailed capability
for generating musical compositions. Model architecture
The MIAO consists of three pivotal components: the MIDI Encoder, the audio decoder, and the audio encoder. The MIDI Encoder and audio decoder are consistently operational across both the training and inference phases,
while the audio encoder plays a crucial role exclusively during the training phase.
(1) The MIDI Encoder is designed with precision to process MIDI data effectively, focusing on refining
musical information for accurate audio synthesis. As shown in Fig. 1, assuming the input MIDI data is denoted
as xm, with dimensions of B × T × N (representing batch size, time step size, and note/event size respectively),
the MIDI Encoder first samples it using deep convolutional layers and reduces it to B

## 4 × T

## 4 × N

4 dimensions. It
then normalizes the data using layer normalization and GELU activation45, as shown in Eq. 1.
datas = g(LN(dw(xm)|Γ))
(1)
where datas denotes the standardized data after processed, g represents the GELU activation function, LN
represents the layer normalization function, and dw(∗)|Γ represents a depthwise convolutional layer with a
3 × 3 convolutional kernel. In order to enable the encoder to extract detailed musical nuances crucial for generating high-quality
audio, the MIDI Encoder is configured with dual parallel convolutional blocks. Each block is characterized by
different convolutional layers with different kernel sizes, followed by batch normalization to enhance the model’s
generalization ability, as shown in Eq. 2.
datastep =



datas,
step = 1,
β(dw(datas)|Λ),
step = 2,
β(dw(datas)|Υ),
step = 3.
datam =

∑
i=1
datai

(2)
where datam represents the dual parallel convolution block output, β represents the batch normalization
function. The processing involves two types of 2D depthwise convolutions: dw|Υ and dw|Λ. Specifically, dwΥ
uses a kernel and padding size of 1, while dwΛ employs a kernel size of 3, with both stride and padding sizes set
to 1. Additionally, the MIDI Encoder is equipped with an encoding attention module to enhance the encoding
process, capturing complex sequence dependencies in MIDI data. The implementation procedure is depicted in
Eq. 3. MIDI Encoder
MIDI
Audio
Aud. Token
Audio Encoder
Audio Decoder
Conv 3 3
Layer Norm
GELU
Conv 1 1
Batch Norm
Conv 3 3
Batch Norm
Conv 3 3
Layer Norm
Self Attention
Conv 3 3
Layer Norm
Conv 3 3
Layer Norm
GELU
Conv 1 1
Batch Norm
Conv 3 3
Batch Norm
Conv 3 3
Layer Norm
Cross Attention
Conv 3 3
Layer Norm
Conv 3 3
Layer Norm
GELU
Causal Self-Att
Conv 3 3
Layer Norm
GELU
Conv 3 3
Layer Norm
Conv 1 1
Conv 3 3
Batch Norm
MIDI-Audio Contrastive Loss
Audio Modeling Loss
MIDI Audio Matching Loss
Addition
&
Execution in only Training Phase
Execution in both Training and Inference Phases
Batch Norm

## MIDI CLS

Aud. CLS
Aud. Audio
Paired
MIDI Token
Fig. 1. The overview of the MIAO framework. The MIAO synthesizer architecture features three core
components: a MIDI Encoder, an Audio Decoder, and an Audio Encoder, the last of which is utilized
exclusively during the training phase. The system is trained on paired MIDI and audio files representing a
variety of instruments, employing three distinct learning objectives to optimize performance: MIDI-audio
contrastive learning, MIDI-audio matching, and MIDI-conditioned audio modeling. Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

Outm = dw(LN(SA(LN(dw(datam)|Γ)))|Γ + datas.
(3)
where Outm represents the final encoding result of the MIDI Encoder, and SA represents the self-attention
computation mechanism, implemented as shown in Eq. 446. Attention(Q, K, V ) = softmax
(
QKT
√dk
)

## V 

(4)
The tensor Outm represents the final output of our MIDI encoder, encoding both structural and semantic
information from the input MIDI sequence xm. This output is partitioned into two components: Outmcls,
which serves as a classification (CLS) token capturing global sequence-level features, and Outmtok, comprising
MIDI tokens that encode local musical semantics. This architectural division supports parallel optimization of
complementary objectives: holistic representation learning through Outmcls and preservation of fine-grained
melodic patterns via Outmtok.
(2) The Audio Encoder is specifically designed for integrating audio-specific information xa and generating
the audio encode result Outa, with a structure similar to that of the MIDI Encoder. It enhances the model’s focus
on important audio features by incorporating an additional cross-attention layer instead of the self-attention layer
used in the MIDI encoder. Additionally, a specialized token, Audio Encoding, is attached to the audio input, with
its embedding serving as a multimodal representation combining MIDI and audio data. This is crucial during
training and allows for the omission of the audio encoder during inference, simplifying the process. The audio encoder is designed to capture detailed information from audio sequences. Its components work
together to process and refine the musical content, preparing it for high-quality audio translation. The encoder
architecture is constructed to capture both spatial and temporal characteristics of the audio, making it a valuable
component in the music synthesis pipeline. To facilitate streamlined training and capitalize on multi-task
learning, all parameters between the MIDI encoder and audio decoder are identical, except for those within the
attention-based layers. This distinction is intentional, as the nuances distinguishing the encoding from decoding
processes are most effectively represented within the attention mechanisms. Simultaneously, similar to the MIDI
Encoder, the output of this Encoder will be divided into Outatok and Outacls for loss calculation.
(3) The Audio Decoder is responsible for converting encoded data em into high-fidelity audio. This is
achieved through two carefully designed parts of the network layers and function combinations. The first part
combines deep convolutional layers and channel self-attention computation to parse the features of the encoded
data, as shown in Eq. 5.
dem = g(LN(CSA(g(LN(dw(em)|Γ))))))
(5)
where dem denotes the output of this compute phase, CSA denotes the channel self-attention computation. Moreover, the second part uses a combination of convolutional layers with different kernel sizes to refine the
audio data systematically, as shown in Eq. 6. This configuration not only helps address the gradient vanishing
problem but also enriches the decoder’s output by retaining important information that may be lost in deep
network structures.
destep =



dem,
step = 1,
β(dw(dem)|Λ),
step = 2,
β(dw(dem)|Υ),
step = 3. OutAud. = LN
(
dw
(

∑
i=1
dei)|Γ
)) 
(6)
where OutAud. denotes the final generation audio result. Such a design indicates a concerted effort to capture a full spectrum of audio features, from basic
waveforms to complex overtones, thus equipping the Audio Decoder to reconstruct a rich and textured
audio output from the abstract representations received from the earlier stages of the model. This
architectural finesse positions the Audio Decoder as a key component in the synthesis pipeline, pivotal for
achieving the end goal of generating synthesized music that is both rich in detail and high in quality. The
details are illustrated in Algorithm 1. Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

Algorithm 1. MIAO Framework
Loss function
During the training phase, our model’s strategy involves optimizing three distinct objectives in tandem: two
are designed for comprehension and the generation of one target. Each MIDI-audio pairing undergoes a single
forward pass through the compute-intensive components of the MIDI encoder, audio encoder, and audio
decoder. This phase is crucial as different functionalities are activated specifically to compute the trio of losses,
thereby enhancing the efficiency of the computational workflow. MIDI-audio contrastive loss (MAC)plays a critical role in training by aligning the feature spaces of MIDI
and audio data, specifically focusing on synchronizing Outmtok (MIDI token output) and Outatok (audio
token output). This alignment is essential for the model to differentiate positive MIDI-audio pairs from negative
ones effectively, enabling a more nuanced understanding of musical relationships47. MAC leverages the ITC
loss function48, incorporating a momentum encoder to create feature representations that act as adaptive, soft-
label training targets. These targets dynamically adapt to distinguish between positive and negative pairs by
identifying potential positive instances within negative samples in Eqs. 7 and 8, thereby improving the model’s
ability to accurately capture complex audio and MIDI correlations. LMAC = −log
exp(sim(i, t)/τ)
∑
t′∈T exp(sim(i, t′)/τ)
(7)
sim(i, t) = cos(θit) =
i · t
∥i∥· ∥t∥=
∑d
k=1 iktk
√∑d
k=1 i2
k
√∑d
k=1 t2
k

(8)
Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

where sim(i, t) denotes the similarity between MIDI representation i and audio embedding t, τ is a temperature
parameter, and T is a set of audio pieces including the correct one and negatives. This approach ultimately
enhances representational accuracy, equipping the model with a refined capability to synchronize MIDI and
audio features in the learned space. MIDI-audio matching loss (MAM) is crucial in honing the model’s multimodal representations, ensuring
a precise correspondence between Outmcls and Outacls. Functioning as a binary classifier, the MAM assesses
whether MIDI-audio pairs are matched or unmatched, utilizing a dedicated linear layer known as the MAM
head for this task. To sharpen the model’s evaluative accuracy, a hard negative mining technique is applied in Eq.

### 949. This method selectively targets and incorporates negative pairs that are most similar in contrast, presenting

greater challenges for the model to distinguish during the training process. Such a methodical selection process
for loss computation significantly enhances the model’s capability to recognize and align MIDI-audio pairings
effectively. LMAM = −[y log(p) + (1 −y) log(1 −p)]
(9)
where p denotes the predicted probability by the model that the MIDI and audio are a correct match. The binary
ground truth labels y ∈{0, 1} in Eq. 9 are determined by the paired structure of our training data. For each batch
containing N aligned MIDI-audio pairs, we assign y = 1 when the MIDI sequence and audio clip originate from
the same musical composition (positive pair), and y = 0 for artificially mismatched combinations (negative
pairs). This labeling scheme is inherent to our dataset construction, where each MIDI file is explicitly paired
with its corresponding audio rendering during preprocessing. The labels thus provide automatic supervision for
the model to learn the correspondence between matched MIDI-audio pairs while rejecting incorrect matches,
without requiring additional manual annotation. Audio modeling loss (AM) is instrumental in enabling the audio decoder to adeptly generate audio from
MIDI sequences. It employs a cross-entropy loss function to direct the model’s predictions of audio sample
probabilities in an autoregressive manner in Eq. 1050. The integration of a label smoothing parameter, α, in the
loss computation helps broaden the model’s generalization, thereby reducing the risk of overfitting. AM’s strategic
design enhances the model’s ability to convert MIDI data into elaborate and high-fidelity audio waveforms.

## LAM = −

N
∑
i=1
[
(1 −α) · yi log(pi) + α
K log(pi)
]

(10)
where yi is the ground truth label, and pi is the predicted probability, K is the number of possible audio sample
values. Experiments
Datasets
Cerberus4 dataset51 is specifically designed for the complex task of separating and transcribing musical mixtures
that include a variety of polyphonic and percussive instruments. Comprising 2100 professionally synthesized
mixtures, each piece in the Cerberus4 is accompanied by isolated sound sources and their corresponding MIDI
data. To suit specific audio processing needs, the Cerberus4’s audio is uniformly downsampled to 16 kHz. It
features diverse instrument combinations, including piano, guitar, bass, drums, and strings, distributed across
thousands of segments. This structure makes Cerberus4 an extensive resource for training and evaluating music
separation and transcription models. MAESTROv3 dataset52 created in partnership with the International Piano-e-Competition, encompasses
around 200 hours of high-quality, uncompressed audio. The audio in the MAESTROv3 is uncompressed,
offering a high-resolution listening experience with a sample rate between 44.1 and 48 kHz and a 16-bit PCM
stereo format. The dataset comprises MIDI recordings collected over ten annual iterations of the competition. The MAESTROv3 features virtuoso pianists performing on Yamaha Disklaviers, capturing detailed MIDI data
such as key strike velocities and various pedal positions for nuanced musical expression. This precision, along
with about 3 ms of audio-MIDI alignment, enables accurate remote judging of competitions. Each recording is
meticulously segmented into individual pieces, annotated with the composer, title, and year of performance. The
collection primarily focuses on classical repertoire, covering works from the 17th to early 20th century. MusicNet dataset53 is a comprehensive collection of classical music, designed for music research and
machine learning applications. It includes hundreds of classical recordings from 10 composers, played on 11
instruments, and provides over one million temporal labels in 34 hours of music. The MusicNet consists of 330
classical recordings, each varying in length, and features a wide range of labels from 513 distinct instrument/
note combinations. The recordings, sourced from various archives, are paired with meticulously aligned digital
MIDI scores to ensure precise labeling. Slakh2100 dataset54 is meticulously designed to enhance music source separation and multi-instrument
automatic transcription, with a focus on its synthetic multi-instrument characteristics. It features a comprehensive
collection of multi-track audio and precisely aligned MIDI files, synthesized from 187 distinct patches across
34 classes using high-quality, sample-based virtual instruments. This synthetic approach results in 2100 unique,
automatically mixed tracks that blend various musical elements, providing a rich resource for exploring and
analyzing complex musical compositions and instrumental interactions. Guitarset dataset55 offers a collection of 360 acoustic guitar excerpts, each approximately 30 seconds in
length, recorded using hexaphonic pickups and Neumann U-87 microphones. These excerpts are performed
by 6 players across 5 musical styles, 3 chord progressions, and 2 tempi, yielding a rich variety of comping and
Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

soloing samples. Accompanying the recordings are comprehensive annotations, including pitch contours, MIDI
notes, beat positions, and chords, facilitating a wide range of musicological and signal-processing research. URMP dataset56 provides a rich collection of 44 classical chamber music arrangements, spanning 28 unique
works by 19 composers, broken down into 11 duets, 12 trios, 14 quartets, and 7 quintets. This comprehensive
dataset includes not only audio and video recordings but also musical scores and detailed frame-level and note-
level transcriptions, covering a wide range of simple to expressive pieces lasting from 40 seconds to 4.5 minutes. It’s an invaluable asset for multi-modal music analysis, offering varied classical compositions across different
instrumental arrangements. Experiment setup
The development of the MIAO model utilizes a sophisticated setup on the PyTorch platform, supported by
the computational capabilities of four NVIDIA A100 GPUs, each managing a substantial batch size of 1024. The AdamW optimization algorithm is the chosen method for refining the model parameters, which is further
optimized by integrating a cosine learning rate scheduler, facilitating an effective ramp-up in the initial stages
of training. The model configuration includes a temperature parameter (τ) set at 99 and a label smoothing
parameter (α) at 0.13, starting with a learning rate of 0.001 and incorporating a weight decay of 0.05 to optimize
training efficacy. This setup ensures a detailed and systematic approach to training, aiming to maximize the
performance and efficiency of the MIAO model. Evaluation metrics
The MT3 Transcription (MT3 T.) metric57 evaluates the accuracy of a synthesis model in replicating specific
notes and instruments. This technique involves processing the model’s output through an MT3 transcription
system to compute an F1 score, using the “Full” metric from the MT3 study and analyzed with mir_eval. For
precise transcription, a note must align within ±50 ms of the intended onset, its offset should be within 0.2 times
the reference duration or at least 50 ms, and it must exactly match the instrument program number from the
input. The Fréchet Audio Distance (FAD)58 is a metric for assessing the quality of generated audio. It measures the
similarity between the distribution of features extracted from real audio samples and those from synthesized
audio. This is done by applying a deep learning model to extract features from both sets and then computing the
Fréchet distance, a measure of similarity between the two feature distributions. A lower FAD score indicates a
closer resemblance of the synthesized audio to real audio, implying a higher quality of the generated samples. The Scale Consistency (SC)59 in the context of music objective metrics generally refers to the degree to
which a piece of music maintains its characteristic scale or key throughout a performance or a generated piece. It is a measure of the accuracy and stability of the tonal center, ensuring that the notes produced align with the
expected scales and key signatures, which are foundational elements of musical theory and composition. This
metric is particularly relevant in the evaluation of music generation systems, where maintaining consistent scale
is crucial for the coherence and listenability of the music. The Pitch Class Entropy (PCE)60 is an objective metric used in music analysis that quantifies the
unpredictability or complexity of the distribution of pitch classes (the set of all pitches that are a whole number of
octaves apart) in a piece of music. It is calculated using the concept of entropy from information theory, which,
in this context, measures the amount of uncertainty or surprise in the occurrence of different pitch classes. A
higher Pitch Class Entropy value would indicate a more varied and unpredictable use of pitches, suggesting a
complex piece, while a lower value would suggest more repetition and predictability in the use of pitches. The Reconstruction Embedding Distance (RED)43 metric evaluates the similarity between an original audio
clip and its synthetic counterpart by analyzing them through a classifier network. It measures the divergence
between the signals using the network’s embedding space, employing the Frobenius norm across time frames for
distance calculation. This metric is assessed using two architectures: VGGish, which generates one embedding
per second of audio using its output layer, and TRILL, which produces approximately 5.9 embeddings per second
from a specialized embedding layer. Performance
MIAO is engineered to deliver high-fidelity audio synthesis, encompassing a broad spectrum of instruments
and vocal ranges. It stands out as a holistic end-to-end solution capable of directly converting MIDI sequences
into nuanced audio, fostering a highly interactive and expressive synthesis environment. Empirical evaluation in
Table 1 underscores MIAO’s capabilities, where it is rigorously benchmarked against six datasets: MAESTROv3, Slakh2100, Cerberus4, Guitarset, MusicNet, and URMP, each presenting a unique set of challenges in terms of
instrument complexity and performance dynamics. On the Cerberus4 and MAESTROv3 datasets, MIAO shows a measurable improvement over other models
across multiple metrics. For instance, MIAO achieves 0.52 of MT3 T., approximately 67% higher on Cerberus4
compared to Midi2Wave18, demonstrating its precision in reproducing musical details. Additionally, MIAO’s RED
score is around 26% lower than MI-DDPM, suggesting a closer match to the original audio. On MAESTROv3, MIAO’s FAD is about 40% lower than that of MIDI-DDSP61, reflecting its ability to generate audio distributions
that closely resemble real samples, enhancing the quality of synthesized music. For the MusicNet and Slakh2100 datasets, MIAO maintains a distinct advantage in terms of MT3 T and audio
fidelity. MIAO achieves a score of 0.28 MT3 T. over 55% higher on MusicNet than Midi2Wave and reduces RED
by 0.44 compared to MI-DDPM, showing its effective replication of musical features. On Slakh2100, MIAO’s
FAD score is 33% lower than MIDI-DDSP, indicating more realistic audio synthesis. Additionally, MIAO’s
higher PCE scores, around 11% greater than MIDI-DDSP, reflect its capacity to utilize a broader range of pitch
classes, contributing to a richer and more intricate musical output. Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

On the Guitarset and URMP datasets, MIAO continues to achieve higher MT3 T. and SC. For Guitarset, MIAO’s MT3 T. is approximately 27% greater than MI-DDPM, highlighting its precision in note representation. Its FAD on Guitarset is nearly 60% lower than Midi2Wave, suggesting a closer alignment with natural sound
characteristics. On URMP, MIAO maintains the second-best scale consistency with a score of 0.95, comparable
to MI-DDPM, while achieving an FAD score that is around 20% lower, indicating its ability to produce
structured and harmoniously consistent audio across complex instrumentation. These results underline MIAO’s
adaptability in handling diverse music datasets and generating expressive audio. In conclusion, the empirical data from Table 1 suggests that the MIAO model generally outperforms
Midi2Wave, MIDI-DDSP, and MI-DDPM in transcription accuracy, audio quality, and pitch utilization
complexity. MIAO’s consistently lower FAD scores across datasets underscore its exceptional audio synthesis
quality, demonstrating its ability to produce audio that closely resembles real samples, which is critical for
achieving high harmony in synthesized music. While SC does not differentiate the models, indicating that all
models maintain a similar level of scale consistency, MIAO’s PCE performance suggests it strikes a balance
between complexity and predictability in pitch class distribution, enhancing the richness and intricacy of the
musical output. The higher PCE scores reveal MIAO’s proficiency in utilizing a diverse range of pitch classes,
contributing to more complex and expressive musical compositions. These findings indicate MIAO’s robust
capabilities as a synthesis model, particularly advantageous in applications requiring high harmony and intricate
transcription in music audio generation. The model’s ability to handle a wide spectrum of instruments and
voices with precise note-level control, along with its performance across various challenging datasets, highlights
its versatility and effectiveness. This positions MIAO as a significant advancement in the field of computational
musicology, capable of meeting the nuanced demands of multi-instrument music synthesis and paving the way
for more interactive and expressive music synthesis applications in the future. Setting

## MT3 T.↑

RED↓
FAD↓
SC↑
PCE↑
w/o AD
0.31
1.86
0.25
0.75
2.62
w AD
0.52
1.35
0.18
0.93
2.97
Table 2. Comparative performance analysis of MIAO with (w) and without (w/o) Audio Encoder on the
Cerberus4 Dataset. Significant values are in bold. Datasets
Models

## MT3 T.↑

RED↓
FAD↓
SC↑
PCE↑
Cerberus4
Midi2Wave
0.32
2.37
0.43
0.75
2.13
MIDI-DDSP
0.39
1.82
0.34
0.88
2.49
MI-DDPM
0.44
1.73
0.22
0.87
2.84
MIAO
0.52
1.35
0.18
0.93
2.97
MAESTROv3
Midi2Wave
0.19
3.38
0.52
0.69
2.12
MIDI-DDSP
0.26
2.83
0.47
0.87
2.44
MI-DDPM
0.30
2.39
0.35
0.92
2.57
MIAO
0.35
2.16
0.28
0.93
2.82
MusicNet
Midi2Wave
0.18
4.31
0.46
0.82
2.37
MIDI-DDSP
0.23
3.91
0.39
0.88
2.45
MI-DDPM
0.25
3.29
0.33
0.91
2.84
MIAO
0.28
2.85
2.852.85
0.93
2.93
Slakh2100
Midi2Wave
0.31
1.67
0.39
0.89
1.95
MIDI-DDSP
0.33
1.57
0.29
0.91
2.11
MI-DDPM
0.39
1.41
0.25
0.95
2.05
MIAO
0.42
1.22
0.20
0.93
2.30
Guitarset
Midi2Wave
0.44
4.81
0.43
0.78
2.13
MIDI-DDSP
0.48
4.44
0.37
0.87
2.19
MI-DDPM
0.52
4.09
0.26
0.92
2.33
MIAO
0.56
3.86
0.15
0.94
2.59
URMP
Midi2Wave
0.21
4.03
0.45
0.87
2.57
MIDI-DDSP
0.25
3.75
0.37
0.95
2.64
MI-DDPM
0.27
3.54
0.23
0.96
2.86
MIAO
0.31
3.26
0.18
0.95
2.78
Table 1. Comprehensive model experimental results on multiple data sets. Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

Ablation study
Decoder
Table 2 demonstrates the performance impact of MIAO’s audio decoder architecture. The first row shows
the baseline results when replacing the proposed decoder with a simpler feed-forward network (FFN), while
subsequent rows highlight how the full decoder configuration significantly improves performance across all
metrics on the Cerberus4 dataset. This comparative analysis confirms that the structural components of our
proposed audio decoder are essential for achieving state-of-the-art results. The MIAO’s accuracy in note and
instrument replication, as indicated by the MT3 Transcription score, improves by approximately 67.74%, rising
from 0.31 to 0.52 with the audio decoder. The Reconstruction Embedding Distance metric decreases by about
27.42%, falling from 1.86 to 1.35, which denotes a closer resemblance of the synthesized audio to the original. Additionally, the Fréchet Audio Distance is reduced by 28%, from 0.25 to 0.18, highlighting the improved quality
of the generated audio. Scale Consistency increases by 24%, from 0.75 to 0.93, suggesting that the audio decoder
contributes to a more consistent maintenance of the music’s scale. Finally, the Pitch Class Entropy sees a rise of
13.36%, from 2.62 to 2.97, indicating that the audio decoder aids in producing a richer and more complex pitch
distribution. Overall, these improvements underscore the audio decoder’s vital role in advancing the MIAO
model’s multi-instrument music synthesis performance. Encoder
Table 3 illustrates the impact of the audio encoder on MIAO’s performance on the Guitarset Dataset. With
the audio encoder, the MT3 Transcription score improves by 16.67% from 0.48 to 0.56, indicating better
transcription accuracy. The Reconstruction Embedding Distance is reduced by approximately 11.47%, from
4.36 to 3.86, suggesting more accurate audio synthesis. The Fréchet Audio Distance sees a substantial decrease
of 40%, from 0.25 to 0.15, reflecting an improvement in the audio quality. Scale Consistency increases by 5.62%,
from 0.89 to 0.94, showing a slight enhancement in maintaining the music’s scale. Pitch Class Entropy rises by
9.28%, from 2.37 to 2.59, indicating a more diverse pitch class distribution. These metrics collectively signal the
significant advantage of including an audio encoder in the MIAO model for the Guitarset Dataset, enhancing its
ability to generate high-fidelity musical audio with detailed transcriptional intricacy. Parameter setting
Figure 2 (right) delves into how specific parameter settings affect MIAO’s performance on the MusicNet dataset,
particularly at a batch size of 512. The examination highlights optimal parameter configurations for maximizing
model accuracy. For the number of heads in the multi-head attention mechanism (h), performance increases
Fig. 2. The batch size (left) and parameter (right) settings. Setting

## MT3 T.↑

RED↓
FAD↓
SC↑
PCE↑
w/o AD
0.48
4.36
0.25
0.89
2.37
w AD
0.56
3.86
0.15
0.94
2.59
Table 3. Comparative performance analysis of MIAO with (w) and without(w/o) audio encoder on the
guitarset dataset. Significant values are in bold. Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

with the number of heads, achieving optimal RED at 2.85 for ‘h = 3’. Adding more heads, such as ‘h = 4’ or ‘h
= 5’, does not significantly enhance performance and may even slightly degrade it, suggesting that three heads
optimally balance computational efficiency and capability for diverse feature representation. Similarly, the length
of tokens per MIDI (a) shows that ‘a = 32’ reaches the highest RED of 2.85, while extending the token length
further slightly reduces accuracy. For the number of MIDI inputs (f), the optimal performance is observed at
‘f = 8’, where RED also peaks at 2.85; increasing ‘f’ beyond this point results in diminished returns, indicating
an overload of input data that does not contribute to, and may even hinder, model performance. These results
underscore the importance of calibrating these parameters within specific bounds to avoid over-complication
and ensure efficient model operation. Limitations and future plans
MIAO demonstrates strong applicability in multi-instrument music synthesis, achieving precise note-level
control across diverse instruments, as evidenced by its performance on published music datasets. However, its
current evaluation scope remains limited to harmonious compositions, leaving its efficacy on dissonant or non-
harmonic music untested–a critical gap for broader adoption. To advance this framework, future work will focus
on three key directions: (1) validating generalizability to unconventional musical structures, (2) integrating real-
time interactive performance capabilities, and (3) incorporating emotion-aware synthesis to enhance expressive
depth. These enhancements will solidify MIAO’s role as a versatile and transformative tool in computational
musicology. Conclusion
In conclusion, the MIAO synthesizer emerges as a transformative entity in the realm of computational
musicology, adeptly addressing the intricate demands of multi-instrument music synthesis. The integration
of complex vision-language objectives within its innovative architecture enhances the synthesizer’s ability to
understand and replicate detailed musical structures. This capability significantly enriches the authenticity and
expressiveness of the generated compositions, effectively bridging the often challenging gap between precision
and versatility in MIDI to high-fidelity audio conversion. However, despite its advanced capabilities, MIAO still
faces limitations in real-time processing speed and the handling of extremely complex acoustic environments. Data availibility
All data is available, which can be requested on links: Cerberus4: ​h​t​t​p​s​:​/​/​i​n​t​e​r​a​c​t​i​v​e​a​u​d​i​o​l​a​b​.​g​i​t​h​u​b​.​i​o​/​d​e​m​o​s​/​c​e​
r​b​e​r​u​s. MAESTROv3: https://magenta.tensorflow.org/datasets/maestro. MusicNet: ​h​t​t​p​s​:​/​/​z​e​n​o​d​o​.​o​r​g​/​r​e​c​o​r​d​s​/​
5​1​2​0​0​0​4​. Slakh2100: http://www.slakh.com/. Guitarset: https://zenodo.org/records/3371780. URMP: ​h​t​t​p​s​:​/​/​l​a​b​
s​i​t​e​s​.​r​o​c​h​e​s​t​e​r​.​e​d​u​/​a​i​r​/​p​r​o​j​e​c​t​s​/​U​R​M​P​.​h​t​m​l
Received: 30 March 2025; Accepted: 25 August 2025
References

### 1. Tur, A. O., Dall’Asen, N., Beyan, C. & Ricci, E. Exploring diffusion models for unsupervised video anomaly detection. In 2023 IEEE

International Conference on Image Processing (ICIP) 2540–2544 (IEEE, 2023).

### 2. Hayes, B., Shier, J., Fazekas, G., McPherson, A. & Saitis, C. A review of differentiable digital signal processing for music & speech

synthesis. arXiv:2308.15422

### 3. Nakatsuka, T., Hamasaki, M. & Goto, M. Content-based music-image retrieval using self-and cross-modal feature embedding

memory. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision 2174–2184 (2023).

### 4. Pasquier, P. et al. MIDI-GPT: A controllable generative model for computer-assisted multitrack music composition. In Proceedings

of the AAAI Conference on Artificial Intelligence, Vol. 39, 1474–1482 (2025).

### 5. Li, J., Li, D., Xiong, C. & Hoi, S. BLIP: Bootstrapping language-image pre-training for unified vision-language understanding and

generation. In International Conference on Machine Learning 12888–12900 (PMLR, 2022).

### 6. Wang, Z. et al. Toward learning joint inference tasks for IASS-MTS using dual attention memory with stochastic generative

imputation. IEEE Trans. Neural Netw. Learn. Syst. https://doi.org/10.1109/TNNLS.2023.3305542 (2023).

### 7. Moliner, E., Lehtinen, J. & Välimäki, V. Solving audio inverse problems with a diffusion model. In ICASSP 2023-2023 IEEE

International Conference on Acoustics, Speech and Signal Processing (ICASSP) 1–5 (IEEE, 2023).

### 8. Mariani, G. et al. Multi-source diffusion models for simultaneous music generation and separation. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​3​0​

2​.​0​2​2​5​7​a​r​X​i​v​:​2​3​0​2​.​0​2​2​5​7 (2023).

### 9. Marougkas, A., Troussas, C., Krouska, A. & Sgouropoulou, C. Virtual reality in education: A review of learning theories, approaches

and methodologies for the last decade. Electronics 12, 2832 (2023).

### 10. Talwar, S., Kaur, P., Nunkoo, R. & Dhir, A. Digitalization and sustainability: Virtual reality tourism in a post pandemic world. J. Sustain. Tour. 31, 2564–2591 (2023).

### 11. Taulli, T. The impact on major industries: A look at music, education, journalism, gaming, healthcare, and finance. In Generative

AI: How ChatGPT and Other AI Tools Will Revolutionize Business 175–188 (Springer, 2023).

### 12. Lavengood, M. L. & Williams, E. The common cold: Using computational musicology to define the winter topic in video game

music (RESUB). Music Theory Online, Vol. 29 (2023).

### 13. Pang, Y. et al. Slim UNETR: Scale hybrid transformers to efficient 3D medical image segmentation under limited computational

resources. IEEE Trans. Med. Imaging 43, 994–1005 (2023).

### 14. Pang, Y. et al. Automatic detection and quantification of hand movements toward development of an objective assessment of

tremor and bradykinesia in parkinson’s disease. J. Neurosci. Methods 333, 108576 (2020).

### 15. Pang, Y. et al. Online self-distillation and self-modeling for 3D brain tumor segmentation. IEEE J. Biomed. Health Inf. ​h​t​t​p​s​:​/​/​d​o​i​.​

o​r​g​/​1​0​.​1​1​0​9​/​J​B​H​I​.​2​0​2​5​.​3​5​3​0​7​1​5​ (2025).

### 16. Kim, W., Son, B. & Kim, I. Vilt: Vision-and-language transformer without convolution or region supervision. In International

Conference on Machine Learning 5583–5594 (PMLR, 2021).

### 17. Briot, J.-P. & Pachet, F. Deep learning for music generation: Challenges and directions. Neural Comput. Appl. 32, 981–993 (2020). Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

### 18. Shi, X., Cooper, E., Wang, X., Yamagishi, J. & Narayanan, S. Can knowledge of end-to-end text-to-speech models improve neural

midi-to-audio synthesis systems? In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing

## (ICASSP) 1–5 (IEEE, 2023).

### 19. Ji, S., Luo, J. & Yang, X. A comprehensive survey on deep music generation: Multi-level representations, algorithms, evaluations,

and future directions. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​0​1​1​.​0​6​8​0​1​a​r​X​i​v​:​2​0​1​1​.​0​6​8​0​1 (2020).

### 20. Zhang, D., Hu, Z., Li, X., Tie, Y. & Qi, L. Multi-track music generation network based on a hybrid learning module. In 2023 IEEE

International Conference on Multimedia and Expo Workshops (ICMEW) 326–331 (IEEE, 2023).

### 21. Renault, L. Differentiable piano model for midi-to-audio performance synthesis. In JJCAAS 2023: Journées Jeunes Chercheurs en

Audition, Acoustique musicale et Signal audio (2023).

### 22. Renault, L., Mignot, R. & Roebel, A. Ddsp-piano: A neural sound synthesizer informed by instrument knowledge. AES-J. Audio

Eng. Soc. Audio-Accoustics-Appl. 71, 552–565 (2023).

### 23. Jonason, N. et al. DDSP-based neural waveform synthesis of polyphonic guitar performance from string-wise midi input. ​a​r​X​i​v​:​h​

t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​3​0​9​.​0​7​6​5​8​a​r​X​i​v​:​2​3​0​9​.​0​7​6​5​8 (2023).

### 24. Yi, H. et al. Generating holistic 3D human motion from speech. In Proceedings of the IEEE/CVF Conference on Computer Vision

and Pattern Recognition, 469–480 (2023).

### 25. Kim, J., Oh, H., Kim, S., Tong, H. & Lee, S. A brand new dance partner: Music-conditioned pluralistic dancing controlled by

multiple dance genres. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 3490–3500 (2022).

### 26. Zhu, P. et al. ERNIE-music: Text-to-waveform music generation with diffusion models. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​3​0​2​.​0​4​4​5​6​a​r​X​

i​v​:​2​3​0​2​.​0​4​4​5​6 (2023).

### 27. Lu, P. et al. MuseCoco: Generating symbolic music from text. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​3​0​6​.​0​0​1​1​0​a​r​X​i​v​:​2​3​0​6​.​0​0​1​1​0 (2023).

### 28. Wang, Y., Chen, M. & Li, X. Continuous emotion-based image-to-music generation. IEEE Trans. Multimedia 26, 5670–5679

(2023).

### 29. Li, J., Li, D., Savarese, S. & Hoi, S. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large

language models. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​3​0​1​.​1​2​5​9​7​a​r​X​i​v​:​2​3​0​1​.​1​2​5​9​7 (2023).

### 30. Li, S. & Sung, Y. Melodydiffusion: Chord-conditioned melody generation using a transformer-based diffusion model. Mathematics

11, 1915 (2023).

### 31. Civit, M., Civit-Masot, J., Cuadrado, F. & Escalona, M. J. A systematic review of artificial intelligence-based music generation: Scope, applications, and future trends. Expert Syst. Appl. 209, 118190 (2022).

### 32. Oord, A. v. d. et al. WaveNet: A generative model for raw audio. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​1​6​0​9​.​0​3​4​9​9​a​r​X​i​v​:​1​6​0​9​.​0​3​4​9​9 (2016).

### 33. Mehri, S. et al. SampleRNN: An unconditional end-to-end neural audio generation model. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​1​6​1​2​.​0​7​8​3​7​

a​r​X​i​v​:​1​6​1​2​.​0​7​8​3​7 (2016).

### 34. Goodfellow, I. et al. Generative adversarial networks. Commun. ACM 63, 139–144 (2020).

### 35. Donahue, C., McAuley, J. & Puckette, M. Adversarial audio synthesis. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​1​8​0​2​.​0​4​2​0​8​a​r​X​i​v​:​1​8​0​2​.​0​4​2​0​8

(2018).

### 36. Engel, J. et al. GANSynth: Adversarial neural audio synthesis. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​1​9​0​2​.​0​8​7​1​0​a​r​X​i​v​:​1​9​0​2​.​0​8​7​1​0 (2019).

### 37. Morrison, M. et al. Chunked autoregressive GAN for conditional waveform synthesis. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​1​1​0​.​1​0​1​3​9​a​r​X​i​v​:​2​1​1​0​.​1​0​1​3​9 (2021).

### 38. Greshler, G., Shaham, T. & Michaeli, T. Catch-a-waveform: Learning to generate audio from a single short example. Adv. Neural. Inf. Process. Syst. 34, 20916–20928 (2021).

### 39. Caillon, A. & Esling, P. Streamable neural audio synthesis with non-causal convolutions. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​2​0​4​.​0​7​0​6​4​a​r​X​

i​v​:​2​2​0​4​.​0​7​0​6​4 (2022).

### 40. Surís, D., Vondrick, C., Russell, B. & Salamon, J. It’s time for artistic correspondence in music and video. In Proceedings of the IEEE/

CVF Conference on Computer Vision and Pattern Recognition, 10564–10574 (2022).

### 41. Wang, Y. et al. Tacotron: Towards end-to-end speech synthesis. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​1​7​0​3​.​1​0​1​3​5​a​r​X​i​v​:​1​7​0​3​.​1​0​1​3​5 (2017).

### 42. Ho, J., Jain, A. & Abbeel, P. Denoising diffusion probabilistic models. Adv. Neural. Inf. Process. Syst. 33, 6840–6851 (2020).

### 43. Hawthorne, C. et al. Multi-instrument music synthesis with spectrogram diffusion. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​2​0​6​.​0​5​4​0​8​a​r​X​i​v​:​2​2​

0​6​.​0​5​4​0​8 (2022).

### 44. Zhuo, L. et al. Video background music generation: Dataset, method and evaluation. In Proceedings of the IEEE/CVF International

Conference on Computer Vision, 15637–15647 (2023).

### 45. Hendrycks, D. & Gimpel, K. Gaussian error linear units (GELUs). ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​1​6​0​6​.​0​8​4​1​5​a​r​X​i​v​:​1​6​0​6​.​0​8​4​1​5 (2016).

### 46. Khan, S. et al. Transformers in vision: A survey. ACM Comput. Surv. (CSUR) 54, 1–41 (2022).

### 47. Radford, A. et al. Learning transferable visual models from natural language supervision. In International Conference on Machine

Learning 8748–8763 (PMLR, 2021).

### 48. Li, J. et al. Align before fuse: Vision and language representation learning with momentum distillation. Adv. Neural. Inf. Process. Syst. 34, 9694–9705 (2021).

### 49. Wang, Q., Gu, J.-C. & Ling, Z.-H. Multiscale matching driven by cross-modal similarity consistency for audio-text retrieval. In

ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) 11581–11585 (IEEE, 2024).

### 50. Raffel, C. Learning-Based Methods for Comparing Sequences, with Applications to Audio-to-Midi Alignment and Matching

(Columbia University, New York, 2016).

### 51. Manilow, E., Seetharaman, P. & Pardo, B. Simultaneous separation and transcription of mixtures with multiple polyphonic and

percussive instruments. In ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)

## 771–775 (IEEE, 2020).

### 52. Wu, Y. et al. MIDI-DDSP: Detailed control of musical performance via hierarchical modeling. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​2​1​1​2​.​0​9​3​

1​2​a​r​X​i​v​:​2​1​1​2​.​0​9​3​1​2 (2021).

### 53. Thickstun, J., Harchaoui, Z. & Kakade, S. Learning features of music from scratch. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​r​g​/​a​b​s​/​1​6​1​1​.​0​9​8​2​7​a​r​X​i​v​:​1​6​1​

1​.​0​9​8​2​7 (2016).

### 54. Manilow, E., Wichern, G., Seetharaman, P. & Le Roux, J. Cutting music source separation some Slakh: A dataset to study the impact

of training data quality and quantity. In 2019 IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA)

## 45–49 (IEEE, 2019).

### 55. Xi, Q., Bittner, R. M., Pauwels, J., Ye, X. & Bello, J. P. GuitarSet: A dataset for guitar transcription. In ISMIR, 453–460 (2018).

### 56. Li, B., Liu, X., Dinesh, K., Duan, Z. & Sharma, G. Creating a multitrack classical music performance dataset for multimodal music

analysis: Challenges, insights, and applications. IEEE Trans. Multimedia 21, 522–535 (2018).

### 57. Gardner, J., Simon, I., Manilow, E., Hawthorne, C. & Engel, J. Mt3: Multi-task multitrack music transcription. ​a​r​X​i​v​:​h​t​t​p​:​/​/​a​r​x​i​v​.​o​

r​g​/​a​b​s​/​2​1​1​1​.​0​3​0​1​7​a​r​X​i​v​:​2​1​1​1​.​0​3​0​1​7 (2021).

### 58. Kilgour, K., Zuluaga, M., Roblek, D. & Sharifi, M. Fréchet audio distance: A reference-free metric for evaluating music enhancement

algorithms. In INTERSPEECH, 2350–2354 (2019).

### 59. Toh, R. K. H. & Sourin, A. Generation of music with dynamics using deep convolutional generative adversarial network. In 2021

International Conference on Cyberworlds (CW) 137–140 (IEEE, 2021).

### 60. Yang, L.-C. & Lerch, A. On the evaluation of generative models in music. Neural Comput. Appl. 32, 4773–4784 (2020).

### 61. Wu, Y. et al. MIDI-DDSP: detailed control of musical performance via hierarchical modeling. In International Conference on

Learning Representations (2022). Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/

Author contributions
Dr. Xi Zhang: Writing—Original Draft, Software, Methodology, Formal Analysis, Visualization. Dr. Yan Huang:­
Data Curation, Conceptualization, Validation, Investigation, Writing—Review & Editing. Declarations
Competing interests
The authors declare no competing interests. Additional information
Correspondence and requests for materials should be addressed to Y. H. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:33180

| https://doi.org/10.1038/s41598-025-17410-6
www.nature.com/scientificreports/
