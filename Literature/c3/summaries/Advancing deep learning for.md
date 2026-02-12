# Advancing deep learning for

**Year:** D:20

---

Advancing deep learning for
expressive music composition and
performance modeling
Man Zhang
The pursuit of expressive and human-like music generation remains a significant challenge in the field
of artificial intelligence (AI). While deep learning has advanced AI music composition and transcription,
current models often struggle with long-term structural coherence and emotional nuance. This study
presents a comparative analysis of three leading deep learning architectures: Long Short-Term Memory
(LSTM) networks, Transformer models, and Generative Adversarial Networks (GANs), for AI-generated
music composition and transcription using the MAESTRO dataset. Our key innovation lies in the
integration of a dual evaluation framework that combines objective metrics (perplexity, harmonic
consistency, and rhythmic entropy) with subjective human evaluations via a Mean Opinion Score (MOS)
study involving 50 listeners. The Transformer model achieved the best overall performance (perplexity:
2.87, harmonic consistency: 79.4%, MOS: 4.3), indicating its superior ability to produce musically rich
and expressive outputs. However, human compositions remained highest in perceptual quality (MOS:
4.8). Our findings provide a benchmarking foundation for future AI music systems and emphasize the
need for emotion-aware modeling, real-time human-AI collaboration, and reinforcement learning to
bridge the gap between machine-generated and human-performed music. Keywords  Deep learning, AI music generation, Music transcription, Transformer models, Generative
adversarial networks (GANs), Long short-term memory (LSTM), Harmonic consistency, Perplexity, Expressive
performance modeling
Music has developed through technology since its initial recorded notation systems, continuing until
contemporary digital audio workstation (DAW) systems. Deep learning has taken a leading role in modernizing
the creation process, along with music performance and tone evaluation techniques. Through the power of
artificial intelligence (AI), users can obtain generated melodies, piece harmonization, and composer style
emulation. Recent advancements enable novel artistic aspects that artists, composers, and researchers can utilize. The main hurdle in AI music generation involves developing compositions that preserve the harmony of
musical structures while accomplishing emotional symbolism and authentic musical expression. To ensure a
fair and unbiased comparison between AI-generated and human-composed music, we curated a balanced set of
stimuli across all conditions. Each evaluation set consisted of 10 audio samples per category: LSTM, Transformer, GAN, and human-composed music. All stimuli were matched in terms of genre (classical), instrumentation
(piano), and approximate duration (30–45 s). This alignment was done to minimize confounding variables such
as stylistic or temporal disparities, ensuring that listener ratings reflected model output rather than unrelated
acoustic factors. We acknowledge that further refinement in stimulus control—such as balancing expressive
range, dynamics, and musical complexity—would strengthen future evaluations. As recommended in1,2, we
plan to adopt standardized guidelines for perceptual experiment design in subsequent studies to enhance
reproducibility and fairness. Deep learning implements sophisticated approaches for music generation through its recurrent neural
networks, LSTM networks, and transformer models. The Musical Instrument Digital Interface (MIDI) and
Audio Edited for Synchronous TRacks and Organization (MAESTRO) dataset serves as an essential tool
for deep learning models in music generation through its MIDI and Audio Edited for Synchronous TRacks
and Organization content. The dataset, composed of high-quality classical piano recordings combined with
synchronized MIDI data, enables proper research in transcription work performance modeling and AI
composition. To further refine the spectral representation, the Mel spectrogram is computed by applying a Mel
filter bank to the power spectrogram. While the Mel scale approximates human auditory pitch perception, it
does not capture the full range of perceptual features relevant to musical expressiveness, such as timbral texture, School of Mechanical Engineering, Yellow River Conservancy Technical University, Kaifeng 475004, Henan, China.
email: 2010830675@yrcti.edu.cn
OPEN
Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports

dynamic articulation, or spatial perception. Therefore, although effective for pitch-oriented learning tasks, Mel-
scale features have limitations when modeling the broader perceptual experience of music. For richer perceptual
modeling, alternative representations such as perceptual linear prediction (PLP) or the constant-Q transform
(CQT) may offer improved alignment with human hearing3. The dataset provides researchers with the capability
to study AI techniques that extract knowledge from human-based performances to create expressive musical
compositions with proper structure. A study examines deep learning methods that apply to the MAESTRO
dataset for developing and reviewing automated music. A study investigates the capability of neural networks to
receive musical composition training, which allows them to generate new pieces with a structured framework
and emotional elements. Through deep learning applications, this research enhances the development of AI
music generation technology. Modern technology focuses on the combined effects of Artificial Intelligence and
musical composition over recent years. During the early phases of computational music creation systems based
on predefined musical rules, algorithms were used to produce compositions4. This computational method works
for specific purposes yet lacks the human quality of emotional expression and adaptability in output. The data-
oriented capabilities of deep learning allow it to produce complex musical patterns through automated methods
without requiring preprogrammed musical rules. AI models can now interpret and generate music better than
ever because both large music datasets and modern computational capabilities are increasing. Neural networks
achieve successful results throughout music processing operations such as melody prediction, chord progression
modeling and rhythm generation5. The modern advances in AI music generation leave out significant human
qualities that characterize emotional and nuanced musical compositions. A research effort exists to establish connections between computer-generated music and music produced by
humans. AI can obtain authentic musical performance knowledge from the MAESTRO dataset to teach itself
human qualities of musical expressiveness, such as dynamic patterns, alongside rhythmic and phrasing elements. This research conditions AI-produced music to enhance its quality so AI can act as a skilled musical assistant
for both composers and musicians. The technology of AI music generation extends its functions past musical
composition tasks. This technology proves useful to improve music education while simultaneously aiding
transcription processes and delivering live performance accompaniments6. The research supports continuous
developments of artificial intelligence in artistic realms by developing enhanced deep-learning techniques for
musical composition. The field of music has transformed deep learning because computers now create complex musical compositions
and perform analytical and performing operations with enhanced capabilities. Deep learning models extract
musical structures from extensive datasets because they do not follow traditional algorithmic rules for generation,
but produce more complex compositions as a result6. Sequences of data provided by RNNs and LSTM networks
allow them to process musical structures, which makes them ideal for chord progressions and musical phrase
modeling7. OpenAI’s MuseNet, together with Google’s Music Transformer, represent Transformer-based models
that show exceptional performance in producing structured musical sequences6. Deep learning models create
new musical works in different styles, ranging from classical music and jazz to pop genres. The combination of
AIVA with OpenAI’s Jukebox enables musicians to produce new musical compositions without much human
labor involvement8. Through AI technology, programmers can perform human performance evaluation to
generate live musical accompaniment. Live performances receive an enhancement through the deep learning
adaptation capability that Yamaha’s AI-powered piano applies to pace and volume control from performers3. The
technique of deep learning turns real-time audio into musical notations expressed through MIDI by improving
automatic music transcription methods. AI models require the MAESTRO dataset to achieve accurate piano
score transcription results9. Through deep learning methods streaming platforms including Spotify and Apple
Music generate personalized song suggestions for users based on their listening behavior with solutions such
as collaborative filtering and convolutional neural networks10. The technology can produce musical sequences
that match a specific emotional condition of a listener. Using deep learning models from affective computing
allows applications in therapy while providing features to gaming and interactive media through the emotional
classification of music11. Deep learning is redefining music production by democratizing access to high-quality composition tools. Independent artists can now leverage AI to enhance creativity without extensive musical training. However,
the rise of AI-generated music also raises ethical questions about authorship, copyright, and the role of human
musicians in an AI-driven industry12. As deep learning models evolve, their ability to create, analyze, and
personalize music will expand. Future advancements may lead to AI composers collaborating seamlessly with
human musicians, further blurring the line between human and machine-generated music. This research uses the MAESTRO dataset to apply deep learning techniques in music composition and analysis. The primary objective is to develop and evaluate neural network models that generate expressive and structured
music compositions. The study aims to bridge the gap between AI-generated and human-composed music by
improving musical coherence, emotional depth, and stylistic adaptation.
•	 To analyze the effectiveness of AI-generated music by comparing it to human performances in structure,
harmony, and expressiveness.
•	 To enhance music transcription and performance modeling using the MAESTRO dataset.
•	 To explore real-world applications such as AI-assisted composition, automatic accompaniment, and emo­
tion-based music generation.
•	 To address ethical and creative implications of AI in music production, focusing on authorship, originality,
and artistic collaboration. The key Contributions of this research are: Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

•	 Implement deep learning models trained on the MAESTRO dataset for music generation and transcription.
•	 Comparative analysis of AI-generated compositions versus human-created pieces using objective and subjec­
tive evaluation metrics.
•	 Development of a framework for integrating AI into real-time music performance and interactive composi­
tion tools.
•	 Insights into AI’s impact on the music industry, including creative collaboration, copyright challenges, and
future trends in AI-generated music. This study contributes to the growing field of AI-driven music creation, offering technical advancements and
new perspectives on the role of deep learning in musical artistry. This paper is structured as follows: The related work section presents a comprehensive related work on
traditional computational approaches and recent deep learning advancements in music generation. The
methodology section details the dataset and preprocessing techniques, outlining the structure and feature
extraction methods. It also describes the deep learning architectures used, including LSTMs, Transformers, and
GANs, along with the training pipeline and evaluation metrics. The results and discussion section covers the
experimental setup, hardware specifications, and hyperparameter tuning. The results, comparing AI-generated
compositions to human music using objective and subjective assessments. It also highlights the limitations and
challenges of AI-based music composition. Finally, the conclusion and future work section concludes the study
and outlines future research directions in AI-driven music generation and performance modeling. Related work
Before deep learning dominated music composition and analysis, computational approaches relied on rule-
based systems, probabilistic models, and algorithmic methods. These techniques aimed to simulate creativity
and music theory principles through structured mathematical and logical frameworks. While they provided
foundational insights into computational musicology, they often failed to produce compositions with natural
expressiveness or long-term coherence. Early computational methods for music generation were rule-based,
relying on handcrafted constraints and heuristics to guide composition. These systems encoded harmonic and
rhythmic rules derived from classical music theory. One notable example is the harmonization algorithms
used for Bach chorales, where predefined rules determined chord progressions and voice-leading13. However,
rule-based approaches struggled with stylistic diversity and lacked the adaptability for complex compositions. Algorithmic composition methods, such as stochastic processes and fractal-based algorithms, also played a
role in computational music. Xenakis’ stochastic music models, for instance, used mathematical probability to
generate sound structures with controlled randomness14. While such methods introduced creative variability,
they could not learn musical structure dynamically from real-world data. Probabilistic models improved upon rule-based systems by introducing data-driven statistical learning into
music composition. Markov chains were widely adopted to model sequential note transitions, enabling the
generation of melodies and harmonic progressions based on learned probability distributions15. Markov models
succeeded in improving compositions, but their restricted memory capacity prevented them from recognizing
longer musical dependencies. The expansion of Markov models into Hidden Markov Models (HMMs) added
latent state transitions, which improved harmonic and rhythmic structure representation according to16. The
implementations of HMMs had two primary limitations that restricted their flexibility in producing expressive
musical sequences. Music generation through formal grammar-based composition relied on hierarchical rules that built
structures in traditional music creation processes. Musical composers adopted Chomskyesque context-
free grammar to define melody and harmony rules which operated through music composition recursion17. Grammatical music modeling approaches succeeded in structural analysis yet needed significant adjustment
to work properly because they could not properly represent performance elements aside from structure. Music
generation through genetic algorithms (GAs) alongside evolutionary computation operates with optimization
as the main process. The systems use fitness functions defined by users to mimic evolutionary natural selection
during sequence evolution18. Through GAs, users could explore creative potential but manual intervention
during the selection process restricted their self-directed operations. Traditional computational methods proved essential for music analysis and retrieval operations through
their use in symbolic music processing. Before the development era of computer science, handcrafted machine
learning models extracted musical features from pitch contours while performing rhythm pattern and harmonic
relationship analysis19. These techniques found broad usage throughout the fields of genre classification as well
as melody retrieval and chord recognition while needing professional musical input during feature extraction. The main drawback of traditional musical analysis approaches stemmed from their insufficient ability to
operate across different musical styles. These models predicated their function either on explicit rule systems
or predefined statistical variables, which proved inadequate when encountering advanced or non-Western
musical structures and experimental piece compositions. The development of modern AI music composition
and analysis abilities received substantial support from traditional computer methods, although these methods
encountered numerous obstacles. The application of rule-based and probabilistic models proved unsuccessful in
handling human musical diversity and creative variety. Markov models, together with statistical approaches, fell
short of producing structurally comfortable musical pieces that could be sustained for prolonged periods. Recent
research in low-resource speech processing and expressive audio modeling also offers valuable insights relevant
to AI-based music generation, particularly regarding domain adaptation, stylistic variability, and sequential
modeling in Transformer-based architectures20–23. Artificial intelligence gained the ability to acquire musical
patterns through data-based learning due to breakthroughs in deep learning models that use RNNs, LSTM
networks, and transformers24,25. The software no longer depends on specialist rules for its functional operation. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

The MAESTRO dataset, together with large-scale available datasets, has sped up research in AI-driven music,
allowing scientists to create human-like compositions with structured and expressive patterns26,27. Through its
crucial function, MAESTRO contributes to widespread research advances regarding deep learning applications in
musical domains, especially automated transcription tasks and AI-based composing and expressive performance
prediction methods. Research that uses the MAESTRO dataset al.lows the creation of neural networks that
achieve high accuracy and artistic delivery for analyzing and transcribing music that traditional computational
techniques cannot match. Automatic music transcription relies heavily on the MAESTRO dataset since deep
learning models employ it to convert audio recordings into MIDI symbolic notations. The authors presented a
cutting-edge transcription tool that combined recurrent and convolutional neural networks3,28. The MAESTRO
dataset enabled their model to achieve better polyphonic music transcription results by understanding precise
expressive aspects that occur during piano performances. The high-quality relationship between MIDI and
audio recordings in the dataset enabled the model to acquire precise knowledge about note onset detection and
sustain pedal capabilities, along with velocity dynamics mastering29. The Music Transformer built by Google
employs the MAESTRO dataset to create its transformer-based programming structure that generates extended
musical sequences coherently. Music Transformer displayed superior phrasing and structural consistency in
composition generation due to a structural design that differed from traditional recurrent models according
to30. Through exposure to the expressive piano performances from MAESTRO, the model acquired abilities to
imitate rubato and tempo elements, which enhanced its human-like music generation ability. GANs showed
practical use in symbolic music generation through their applications. MuseGAN31 generates multi-track
piano compositions by utilizing the MAESTRO database. Adversarial training forms the core of their study,
which investigates how it helps create realistic music through its analyses of harmonic structure and temporal
relationships. The analysis of human performances from MAESTRO enabled the model’s successful generation
of polyphonic music, which successfully preserved various musical styles in different compositional formats. The
dataset supports research on expressive performance modeling in addition to transcription and composition
tasks. The research paper by32 employed MAESTRO for training a reinforcement learning-based model that
acquired abilities to express dynamics in piano performance. The authors proved deep reinforcement learning’s
ability to create expressive musical dynamism through velocity modification and timing modulation, which
improved life-like performance when applied to piano notations from MAESTRO. Live AI accompaniment
systems use MAESTRO as part of their operations. Researchers created a neural network system that adapts AI-
generated accompaniments by monitoring live human performances33. showed their findings in this study. The
model acquired real-time harmonic progression abilities through MAESTRO’s expressive interpretations during
the training process. The system can transform music performance through direct collaboration between human
musicians and artificial intelligence in live shows and rehearsal settings. The advancement of AI music generation has encountered obstacles on its path toward producing music
that cannot be differentiated from human-made compositions. Some studies have highlighted limitations in
existing deep learning models, such as difficulties in maintaining long-term coherence in complex compositions
and a tendency for AI to generate repetitive musical structures. Future research aims to address these issues
by incorporating self-supervised learning techniques and larger, more diverse training datasets to enhance the
creativity and authenticity of AI-generated music. The research field aims to solve present issues by including
self-supervised learning models in its operations and implementing substantial training datasets to create more
legitimate AI musical compositions. Methodology
AI-driven music generation and transcription apply the deep learning approach in their operations. The
research presents information about dataset preparation together with preprocessing approaches and explains
the structure of chosen models which consist of LSTM alongside Transformer and GAN-based networks. The evaluation technique for each model’s ability to produce structured expressive and human-like musical
compositions involves discussion of the training pipeline as well as hyperparameter optimization and metric
assessment. Figure 1 demonstrates AI music processing operations which begin with MIDI input files and audio waveforms
and spectrograms leading to deep learning systems that utilize LSTMs for note sequences then Transformers for
dependency modeling as well as GANs for style transformation and CNNs for spectrogram identification. Dataset
The MAESTRO dataset3 serves as a major database for creating deep learning models for musical transcription
tasks, generation purposes, and performance evaluation capabilities. The Magenta team at Google created
this dataset from International Piano-e-Comp titles, achieving high-quality classical piano performances that
establish MAESTRO as a premier AI research tool in musical expressions and details. MAESTRO includes more than 200 h of piano recordings that match with MIDI files for exact timing,
dynamics, and articulation modeling. The recordings within the database extend from 2004 to 2018, ensuring
it encompasses multiple styles and performer interpretations. The Yamaha Disklavier pianos used during
recordings created high-definition MIDI data and audio representations of each musical piece. The data consists of three fundamental sections, including FLAC stereo format audio at 44.1 kHz with 16-bit
resolution and MIDI files and metadata files. The MIDI files become a helpful resource by expressing musical
expressions through their embedded note onset times, durations, velocities, and pedal data. Research into
stylistic variations of various compositions can be performed through the metadata that incorporates composer
names, piece titles, performance durations, and recording years. The MAESTRO dataset distributes its content into three parts for model testing: an 80% train portion
and 10% each for validation and testing purposes. The MIDI files benefit researchers by enabling automatic
Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

music transcription, style transfer, and neural music synthesis practices. Combining MIDI file data and piano
recordings allows AI systems to learn from end to end to generate performances that simulate human piano
musicianship. The MAESTRO dataset contains structured information combining symbolic and audio formats
of classical piano performances, thus enabling researchers to conduct sophisticated deep-learning research on
music generation, transcription techniques, and performance modeling approaches. The database provides
MIDI files with musical notations alongside high-fidelity audio examples containing expressive elements. An
exact pairing of these file formats enables AI training by combining symbolic data and acoustic signals. MIDI files recorded in MAESTRO encompass precise timings regarding note onsets, quantity measurements
(velocities), duration specifications, and pedal status data. Deep learning models can learn expressive musical
elements from tempo variations through rubato alongside articulation marks because the MIDI files contain
exact timestamp information and expression markings that get lost in manual MIDI transcriptions. Because
MIDI files contain structured abstract musical event information without timbral details, the format excels for
symbolically generating music and performance examination. The FLAC format audio recordings in the dataset use 44.1 kHz and 16-bit stereo resolution for high-quality
playback. The Yamaha Disklavier pianos record the audio performances that enable precise timing alignment
between MIDI files. Combining MIDI and audio representations enables deep learning models to perform
automatic music transcription, translating raw sound into symbolic notation with greater accuracy than previous
datasets. Table 1 summarizes the key components of the MAESTRO dataset, detailing the format, resolution,
and main features of each data type. The structured nature of the MAESTRO dataset provides a benchmark for deep learning-based music analysis
by offering precisely aligned symbolic and acoustic data. Researchers have utilized this dataset in polyphonic
transcription, style transfer, and AI-generated expressive performance modeling. The dataset’s combination of
structured MIDI events and high-resolution audio makes it one of the most valuable resources for machine
learning applications in computational musicology. Data cleaning and preprocessing techniques
Preprocessing is essential in preparing the MAESTRO dataset for deep learning models. Since the dataset
includes MIDI files and audio recordings, specific preprocessing techniques are applied to each format to
ensure consistency, accuracy, and high-quality feature extraction. The main objectives of preprocessing include
Data type
File format
Resolution
Key features
MIDI files.mid
Millisecond-level precision
Note onsets, durations, velocities, pedal events
Audio files.flac
44.1 kHz, 16-bit stereo
High-fidelity live performance recordings
Metadata.csv
–
Composer, piece title, performance duration, recording year
Dataset split
Train (80%), Validation (10%), Test (10%)
–
Standardized evaluation framework for AI models
Table 1. MAESTRO dataset structure. Fig. 1. Deep learning models for music processing. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

standardizing time data alongside pitch while eliminating errors and transforming raw information to suitable
training input for neural networks. Time quantization is a primary preprocessing step that maps note events onto
a uniform time framework. Deep learning models need time quantification from MIDI events, which measure
their durations at the millisecond level. Given a quantization factor Q, the adjusted event time t′ is computed as:
t′ =
⌊
t
Q
⌉
Q
(1)
where t represents the original event time, and t′ is the quantized time. This process ensures uniform timing
across all training samples. Another essential step is pitch standardization, which involves transposing all MIDI sequences to a reference
key such as C major or A minor. This transformation is performed by shifting each note’s pitch value P by a
transposition factor k, yielding: P ′ = P + k
(2)
where P ′ is the standardized pitch. Standardization allows the model to focus on relative harmonic structures
rather than absolute key signatures. Velocity normalization is applied to scale note velocities, representing dynamic intensity, into a fixed range
between 0 and 1. The normalized velocity V ′ is computed as:

## V ′ =

V −Vmin
Vmax −Vmin 
(3)
where V is the original velocity value, and Vmin​ and Vmax represent the dataset-wide minimum and maximum
velocities. This ensures consistent dynamic representation across different piano pieces. Duplicate note events and overlapping articulations are removed to maintain data clarity. MIDI files sometimes
contain unintended duplicated note-on messages, which can distort the training data. These redundant events
are filtered out to improve model performance. The FLAC recordings in MAESTRO require transformation into feature-rich representations for models that
process raw audio. This begins with resampling, as different neural network architectures require different audio
sampling rates. Most deep learning models work best at 16–22.05 kHz, so all recordings are standardized to one
of these rates. A crucial step in audio preprocessing is spectrogram computation, which converts the waveform into a time-
frequency representation. This is achieved using the Short-Time Fourier Transform (STFT), defined as: X(t, f) =
∑
N−1
n=0 x (n) w(n −t)e−j2π fn
(4)
where X(t, f) represents the spectrogram, x (n) is the raw waveform, w (n) is a window function, and f is the
frequency bin index. STFT is widely used in deep learning models for music transcription and synthesis, as it
provides a rich representation of harmonic and rhythmic content. To further refine the spectral representation, the Mel spectrogram is computed by applying a Mel filter bank
to the power spectrogram: Sm = M · |X(t, f)|2
(5)
where Sm is the Mel spectrogram and M represents the Mel filter bank matrix. The Mel scale closely matches
human auditory perception, making it an effective input representation for machine learning models. The data augmentation techniques consisting of pitch shifting time stretching and dynamic range
compression work to expand dataset diversity. The audio processing technique of pitch shifting makes semitone
range transformations that preserve sample duration and the time stretching technique maintains pitch stability
through speed modifications. Model generalization benefits from these augmentations which allow AI-generated
music to maintain expressive musical attributes. Preprocessing enhances the MAESTRO dataset for deep-learning application by creating a well-structured
and noise-free optimized format. When this processed dataset provides clean data to models, they can create
expressive musical structures that advance both music creation and transcription capabilities of AI programs. Deep-learning models require feature extraction to analyze and produce structured music that expresses
visible emotions when working with the MAESTRO dataset. AI models gain the capability to learn essential
musical foundations through the extraction of musical elements which include pitch along with tempo together
with chord progressions and dynamics. The fundamental pitch frequency appears in both MIDI note data and
audio signal data. MIDI files contain MIDI note numbers directly available between 0 and 127 that represent
pitch values. Both YIN and CREPE algorithms and Fourier Transform-based methods enable pitch estimation
in audio files by delivering fundamental frequency f0​ estimations in Hz:
f0 = argmin
f E (f)
(6)
where E (f) is the fundamental frequency estimation that produces errors. Accurate pitch tracking serves as
a foundation for successfully carrying out melody extraction together with polyphonic transcription activities. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

The musical speed depends on tempo which shows its pace by counting beats each minute (BPM). MIDI files
have embedded MIDI meta-events for tempo control whereas the extraction of tempo occurs through onset
detection and beat tracking algorithms such as the Dynamic Bayesian Network (DBN) model in audio files.

## T = 60

∆t
(7)
where ∆t  is the time difference between the beats detected. Tempo variation is key to representing expressive
timing changes, including ritardando and accelerando, which affect performance style. The harmonic structure of music is described by chord progressions. For MIDI files, we extract chords
by combining simultaneous note events and determining the root note and the chord quality (major, minor,
diminished, etc.). Usually, chromagram analysis in audio detects harmonic content: C(f, t) =
∑
k∈H(f) |X(k, t)|
(8)
where C(f, t) represents the chroma feature, and H (f) is the set of harmonic frequencies. Chord progressions
are crucial in genre classification, music generation, and accompaniment models. Dynamics refer to variations in note intensity (loudness), affecting musical expression. MIDI’s dynamics are
represented by velocity values ranging from 0 (soft) to 127 (loud). In audio, dynamics are measured through
amplitude envelope analysis using the Root Mean Square (RMS) energy.

## E = 1

N
∑
N
n=1x2 (n)
(9)
where x (n) is the amplitude of the signal. Dynamics are essential for modeling expressive playing styles and
improving the realism of AI-generated performances. Deep learning architectures for music generation and analysis
Deep learning has transformed music generation and analysis by enabling AI models to learn pitch, rhythm,
harmony, and dynamics from data. RNNs, particularly LSTM networks, are widely used for sequential music
modeling. LSTM networks keep track of musical sequences through time, enabling generated musical content to
stay harmonious. During the LSTMs’ hidden state update, the calculation works as follows:
ht = ot ⊙tanh (ct)
(10)
Music Transformer represents an advancement over RNNs by implementing self-attention mechanisms that
enable it to detect distant connections while abandoning the necessity for sequence ordering. The attention
mechanism is defined as: Attention(Q, K, V ) = softmax
(
QKT
dk
)

## V 

(11)
Generative Adversarial Networks (GANs) generate music by training a generator and a discriminator, refining
AI compositions through adversarial learning. Their objective function is:
min
G
max
D Ex∼Pdata(x)[logD(x )] + Ez∼Pz(z)[log(1 −D (G( z )) )]
(12)
Convolutional Neural Networks (CNNs) analyze spectrograms for chord recognition, transcription, and genre
classification using: Y (i, j) =
∑
m
∑
nX(i −m, j −n)W(m, n)
(13)
Model selection: LSTMs, transformers, GANs, and CNNs
Different deep-learning models should be selected according to the type of music task that needs to be performed. The effectiveness of LSTM networks in dealing with sequential data proves helpful in melody creation and
polyphonic music representation. The sequential operating method hinders scalability potential. The Music
Transformer and other Transformer models relieve the technical restriction through self-attention designs to
analyze long-range structural elements for sophisticated melody sequences. GANs are used in music style transfer and improvisation, where a generator creates new music and
a discriminator refines it. GANs help in creating music that closely resembles human compositions. CNNs,
primarily applied to spectrogram-based tasks, are effective in chord recognition, transcription, and genre
classification, extracting hierarchical musical features from audio data. Training pipeline and hyperparameter tuning
The training pipeline starts with data preprocessing, where MIDI sequences and audio spectrograms are
normalized. Training data is split into 80% for training, 10% for validation, and 10% for testing. The selected
model is trained using gradient-based optimization, often with the Adam optimizer for stability. The loss
Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

function varies by task: categorical cross-entropy for classification and mean squared error (MSE) for music
reconstruction. Hyperparameter tuning involves adjusting the learning rate, batch size, and sequence length to optimize
performance. Learning rates are typically set between 1e−4 and 1e−3, with batch sizes ranging from 32 to 128. Regularization techniques such as dropout (0.2–0.5) and L2 weight decay are applied to prevent overfitting. Training is monitored using validation loss and accuracy, with early stopping mechanisms to optimize
convergence. Evaluation metrics for AI-generated music
The evaluation process regarding AI-generated music includes multiple assessment dimensions that involve
quantitative and qualitative measurement elements. Guiding music evaluation differs from regular machine
learning tasks, which use defined objective measures, because it requires the assessment of harmonic structure,
temporal coherence, and expressive quality values. Different metrics analyze the extent of melody similarity,
rhythmic stability, harmonic development, and human recognition of AI musical output. Objective metrics
Sequence modeling uses Perplexity (PPL) as a widespread evaluation metric. Lower perplexity numbers directly
correspond to better music sequence prediction outcomes. It is calculated as: PPL = exp
(
−1
N
∑
N
i=1logP (xi)
)

(14)
where P (xi) is the probability of the next musical event and N is the sequence length. Pitch Class Histogram (PCH) metric analyzes the pitch distributions in generated music melodies relative to
those of human compositions. Rhythmic Entropy provides a measure to check for variation in note durations so
generated music stays interesting rather than sounding monotonous. The calculation involves Shannon entropy.

## H = −

∑
pi log2 pi
(15)
where pi​ is the probability of a particular rhythmic pattern occurring. The evaluation of Harmonic Consistency depends on chord transition matrices to compute the degree
of match between AI-generated and traditional harmonic progressions. Cross-correlation analysis detects
functional and tactical structural analogies between compositions made by AI systems and human-composed
music. Subjective metrics
Subjects must assess musical elements and emotional resonance since human judgment remains vital. Researchers
conduct listening tests that ask participants to evaluate automated music using different criteria, including
coherence and human likeness, together with originality and expressive qualities. Listening participants use the
Mean Opinion Score (MOS) to evaluate scores from 1 to 5 based on their assessment of generated music. The Turing Test’s success relies on the Turing Test Success Rate, which measures the percentage of listeners
who cannot differentiate between human music performance and artificial intelligence-created songs. Higher
scores from these evaluations show that the high-FI becomes more realistic while its creative value improves. Results and discussion
The deep learning-based music generation training process demands powerful high-performance computing
equipment because it involves sophisticated sequential data processing and audio processing requirements. TensorFlow and PyTorch frameworks ran the training process on NVIDIA A100 GPUs, which included 40GB
VRAM. Fast data retrieval is possible through SSD storage, and the system utilizes Intel Xeon 32-core processors
together with 128GB RAM and SSD storage modules. The training took place on Ubuntu 20.04, which used CUDA
as well as cuDNN for optimized parallel processing. For sequential modeling, LSTM networks were implemented
with two stacked layers and 512 hidden units per layer, applying dropout (0.3) to prevent overfitting. The Music
Transformer model used self-attention layers with 8 attention heads, enabling long-range dependency learning. GAN-based music generation models consisted of a generator with transposed convolutions and a discriminator
with convolutional layers, both using batch normalization. CNN models for transcription tasks operated on Mel
spectrogram inputs, using 3 convolutional layers followed by fully connected layers. The MAESTRO dataset was
divided into training (80%), validation (10%), and test (10%) sets to ensure proper model evaluation. Stratified
sampling was used to maintain diversity across composers and styles. MIDI and audio pairs were randomly
shuffled before splitting to prevent data leakage. Time-based splitting was avoided to ensure models generalize
across different compositions. For sequence generation, Categorical Cross-Entropy Loss was used to optimize note prediction:

## L = −

yilog (yi)
(16)
where yi​ represents true note events and yi​ represents predicted probabilities. Mean Squared Error (MSE) loss
was used for transcription tasks. GAN models were trained using Wasserstein loss to improve stability: L = E [D( x )] −E [D( G (z) )]
(17)
Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

Optimization was performed using the Adam optimizer with a learning rate of 1e −4, and gradient clipping was
applied to prevent exploding gradients. Early stopping was used to halt training when validation loss stopped
improving. Performance evaluation of music generation models
The evaluation of AI-generated music was conducted using both quantitative metrics and qualitative assessments. The models tested—LSTM, Transformer, and GAN-based architectures were trained on the MAESTRO dataset
and assessed for their ability to generate structured, expressive, and harmonically coherent compositions. The
key evaluation metrics included perplexity, pitch class similarity, harmonic consistency, rhythmic entropy, and
human listener ratings. Perplexity measures how well a model predicts the next musical event. A lower perplexity score indicates
better predictive accuracy and phrase coherence. Table 2 summarizes the perplexity scores, pitch class similarity,
and harmonic consistency for the three models. Figure 2 illustrates the perplexity comparison across models, showing that the Transformer model performs
best in sequential note prediction. Pitch class similarity measures how closely the generated pitch distributions align with human-composed
pieces. GAN-based models performed the best in this metric, indicating that adversarial training improved the
harmonic balance of generated compositions. Harmonic consistency, which evaluates how well chord transitions
follow musical rules, was highest in Transformer models due to their ability to model long-range dependencies in
chord progressions. To evaluate the rhythmic structure, rhythmic entropy was computed. Higher values indicate
a greater diversity of rhythmic patterns, suggesting more natural variation. The Transformer model achieved
the highest rhythmic entropy, while LSTMs struggled with repetitive phrasing. Table 3 presents a comparative
analysis of rhythm and expressive dynamics. Figure 3 shows the comparison of rhythmic entropy and note duration distributions, reinforcing that
Transformer models produced the most dynamically rich compositions. Model
Average note duration (s)
Tempo stability (%)
Velocity variation (Std. Dev.)
Rubato usage (%)
LSTM
0.62
88.5
14.2
12.1
Transformer
0.74
91.2
18.5
19.8
GAN
0.69
92.4
16.8
14.7
Table 3. Rhythmic and expressive features across models. Fig. 2. Perplexity comparison across AI models. Model
Perplexity (↓)
Pitch class similarity (%)
Harmonic consistency (%)
Rhythmic entropy (bits)
LSTM
3.21
82.3
74.8
4.12
Transformer
2.87
85.6
79.4
4.35
GAN
3.02
88.1
76.5
4.18
Table 2. Performance metrics for LSTM, transformer, and GAN models. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

A listening study was conducted with 50 participants, who rated AI-generated compositions based on
melodic coherence, harmonic richness, and expressiveness. A Mean Opinion Score (MOS) was used, where
1 = Poor, and 5 = Excellent. Table 4 presents the results of the subjective evaluation. Figure 4 visualizes the MOS ratings, confirming that Transformer models achieved the highest overall
ratings, followed by GANs and LSTMs. Fig. 4. Mean Opinion Score (MOS) comparison. Model
Melodic coherence
Harmonic richness
Expressiveness
Overall MOS
LSTM
3.4
3.6
3.2
3.4
Transformer
4.2
4.5
4.3
4.3
GAN
3.9
4.1
3.8
4.0
Table 4. Mean opinion score (MOS) for AI-generated music. Fig. 3. Rhythm and note duration distribution. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

The results indicate that Transformer-based models are the most effective for structured, expressive, and
musically rich AI-generated compositions. They performed the best in perplexity, harmonic consistency,
rhythmic diversity, and human perception scores. GANs showed superior pitch class similarity, making them
more suitable for style transfer applications. LSTMs, while still functional, struggled with long-range coherence
and expressive phrasing. Subjective and objective analysis of generated music
Evaluating AI-generated music requires a combination of objective metrics (quantifiable measures such as
harmonic structure, rhythmic complexity, and pitch accuracy) and subjective assessments (human perception
of expressiveness, coherence, and overall musicality). This section presents a detailed analysis of AI-generated
compositions using both methods. To assess the structural quality of AI-generated music, several quantitative metrics were used, including
harmonic consistency, rhythmic entropy, note duration variance, and phrase coherence. Table 5 presents the
comparative analysis between different AI models and human compositions. Results indicate that Transformer-based models achieve the highest phrase coherence and harmonic
accuracy, while GAN-based models closely replicate human-like chord transitions. LSTMs perform well but
often generate repetitive sequences, reducing overall phrase coherence. Figure 5 provides a comparison of harmonic consistency scores across different models (LSTM, Transformer, GAN) and human-composed music. The results show that while AI-generated compositions demonstrate a
reasonable level of structural harmony, particularly with Transformer and GAN models, they still fall short of
the nuanced harmonic transitions present in human compositions. This highlights the current gap in expressive
variability and subtlety between machine-generated and human-performed music. To complement objective metrics, a human perception study was conducted where 50 participants rated
AI-generated and human-composed pieces based on melodic fluency, harmonic richness, expressiveness, and
overall musicality. Participants listened to 10 compositions per model and rated them on a 1–5 scale (1 = Poor,
5 = Excellent). The Mean Opinion Score (MOS) for each model is presented in Table 6. Figure 6 illustrates the MOS comparison for music generated by LSTM, Transformer, and GAN models versus
human-composed music. Participants rated each piece on melodic fluency, harmonic richness, expressiveness,
and overall musicality using a 1–5 scale. The Transformer model achieved the highest scores among AI systems,
though all AI-generated outputs remained below human compositions in perceived expressiveness and musical
quality. These results underscore the perceptual gap between human and machine-generated music. Fig. 5. Harmonic consistency scores for AI and human compositions. Model
Pitch class similarity (%)
Chord transition accuracy (%)
Rhythmic entropy (bits)
Note duration variance
LSTM
82.3
74.8
4.12
0.15
Transformer
87.6
80.4
4.38
0.27
GAN
88.1
77.3
4.18
0.23
Human
100.0
100.0
4.55
0.32
Table 5. Objective evaluation metrics for AI and human compositions. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

The evaluation reveals that objective metrics and subjective assessments align, confirming that Transformer
models outperform LSTMs and GANs in structural coherence and human perception. However, GAN models
excel in harmonic realism, making them more effective for applications requiring style transfer and musical
adaptation. Limitations and challenges in AI-based music composition
Recent progress in AI music development comes with multiple restrictions on its use. The essential obstacle
AI faces pertains to emotional inadequacy since it fails to match human vocal expressions involving phrasing,
rubato, and dynamic range adjustments. The sophisticated deep learning models create harmonically thorough
music, yet they lack the ability to replicate human artistic creativity together with intended expression methods. Another limitation is long-term coherence. AI music generation occurs through short music units that
produce pieces that fail to build coherent themes or provide structural progression. The music creation process
of synthetic composers differs from humans because artificial intelligence shows mechanical repetition rather
than transformative transitions between musical themes. Style generalization poses a problem because artificial intelligence primarily duplicates the data it received
in its training. AI systems need specialized training on new musical genres such as jazz, electronic music, and
folk music apart from classical music datasets from MAESTRO in order to adapt to them effectively. The specific
choice of genre in which the AI operates hinders the number of music variations it can create because it requires
pre-training within that exact style. One notable limitation of this study is the reliance on the MAESTRO dataset,
which is heavily biased toward classical piano music. While its high-quality alignment of MIDI and audio makes
it ideal for symbolic and transcription-focused tasks, the stylistic and instrumental homogeneity may restrict
the generalizability of trained models to other genres such as jazz, pop, or electronic music. Furthermore, real-
world musical environments involve diverse instruments, mixed ensembles, varying production styles, and live
performance contexts that are not well-represented in the dataset. This genre and modality bias could impact
the robustness of AI-generated music when applied outside the classical domain. To overcome this, future work
should explore training on more diverse and multimodal datasets, integrate genre-agnostic feature extraction,
and develop transfer learning strategies to improve performance across a wider range of musical forms and real-
world applications. The use of existing data in AI-generated music creation leads to dual ethical and copyright issues that
challenge the validity of creatorship authenticity. There is limited clarity about the authorized legal framework
for compositions produced by AI because of which music rights and ownership remain uncertain. Fig. 6. Mean Opinion Score (MOS) for AI-Generated vs. human compositions. Model
Melodic fluency
Harmonic richness
Expressiveness
Overall MOS
LSTM
3.2
3.4
3.1
3.2
Transformer
4.3
4.5
4.2
4.3
GAN
4.0
4.2
3.8
4.0
Human
4.8
4.9
4.7
4.8
Table 6. Mean opinion score (MOS) for AI and human Compositions. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

Computational cost stands as the last significant hurdle in the field. The need for large computational
power makes high-performance AI models unattainable for numerous independent musicians and researchers. Improving model efficiency with preserved quality stands as a vital field of future research development. Conclusion and future work
The researchers implemented deep learning techniques by evaluating different models, such as LSTMs, Transformers, and GANs, when working with the MAESTRO dataset for music composition and analysis. The study showed that Transformer models show superiority over other architectural designs by achieving
better results in structural coherence, melodic fluency, and phrase consistency. However, GAN models excel
at harmonic accuracy and stylistic adaptation. However, AI-generated music still lacks expressive nuances,
such as dynamic phrasing, emotional variation, and human-like improvisation, despite these advancements. A
mixture of perplexity and pitch class similarity, harmonic consistency, and rhythmic entropy metrics indicated
that artificial compositions develop structural elements that approach patterns found in human music. Human
subjects’ evaluations proved that algorithms produce compositions that appear structured, but they lack the
natural improvisation found in human artistic activity. Research findings demonstrated how Transformers obtain
outstanding musical continuity yet are unable to sustain long developments, while GANs present harmonic
depth with occasional non-musical outputs. Various matters about ethics and copyright laws came under
evaluation. AI models obtaining knowledge from existing musical compositions have generated continuing
disputes about music copyright ownership matters. To fully integrate AI systems in the music processing
industry, we need to resolve both model performance limitations, accessibility issues, and optimization needs
for computational expenses. Research should focus on developing emotion-friendly AI music models because
they will automatically change melody delivery and musical intensity through human emotional signals. The current generation of deep-learning models produces music using statistical patterns they have learned
to accomplish, yet remain unable to understand emotion or adjust their output based on user preferences. AI
music creation is enhanced through the integration of affective computing and emotion-conditioned learning
systems, enabling better emotional responsiveness and adaptation. Current research focuses on interactive AI
composition since AI functions as a contemporary collaborator rather than operating autonomously. AI systems
with dynamic response capabilities during real-time human interaction are poised to transform how musicians
improvise, perform live concerts, and score for activities including gaming and cinematic entertainment. The
ability of AI to develop reinforcement learning systems that use feedback for real-time learning will enhance its
music creation capability. AI models can obtain a deeper understanding of musical styles and interpretation when they learn through
multi-modal approaches that combine MIDI symbols with raw waveforms and tracking data on musical
performance expressions. Implementing gesture-based or visual markers originated by musicians enables AI to
develop musical compositions that adjust their output accordingly to human contact. Current AI models still struggle with long-term structure and musical development. We can solve this issue
through hierarchical learning because it teaches AI systems to understand musical structures above single-
note transitions and concert patterns of motifs alongside themes and variations. Through such an approach, AI models would produce musical works that display adaptable narrative patterns like classical human musical
compositions. AI training with reinforcement learning techniques should focus on achieving optimal musical
cohesion and emotional depth instead of repeating data patterns. When reinforcement learning receives
aesthetic feedback from humans, it can modify itself instead of using static predefined rules. Few-shot and
transfer learning methods will enable AI models to learn any genre or musical style through quick adaptation
without significant retraining. The present models demand big training datasets that focus on specific genres,
reducing their versatility range. Creating adaptable AI music models capable of sharing acquired information
across various musical traditions and genres would improve the diversity and adaptability of AI music
generation. Computational efficiency is another challenge. The high computational demands of deep learning
models mainly affect Transformer-based models that need copious training durations. Applying pruning along
with quantization methods and knowledge distillation techniques would lower GPU dependency in music
composition, thus enabling independent artists to access AI-assisted musical composition. The progress of
AI-generated music in recent times continues to miss human-level creativity, emotional expression, and story
development. The present-day deep learning models generate music with rich harmonies, diverse rhythm
patterns, and adaptive musical styles. Still, they fail to achieve human-like expressive traits, development in long
musical form, or musical spontaneity. AI music composition research and development must now focus on finding ways to bridge the gap between
programmed exactness and musical expression that produces human empathy. Innovation needs to occur across
emotion-based computing systems and adaptive roles for AI working with humans while incorporating live
music exchanges. The development of AI in the creative industry depends heavily on combining reinforcement
learning with multi-modal training and ethical standards for ownership of AI-generated music. The development of Artificial Intelligence music primarily aims to help composers expand their creative
potential instead of replacing them to create novel collaborative methods and musical interactions. Modern
advancements suggest that AI will mature to become an irreplaceable tool for artistic expression through its
ability to generate innovative musical tales that sustain human musical storytelling principles. Data availability
The data presented in this study are available on request from the corresponding author. Received: 1 May 2025; Accepted: 21 July 2025
Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

References

### 1. Zaman, K. et al. Ability of human auditory perception to distinguish human-Imitated speech. IEEE Access. 13, 6225–6236. ​h​t​t​p​s​:​/​

/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​/​A​C​C​E​S​S​.​2​0​2​5​.​3​5​2​6​6​3​1​ (2025).

### 2. Unoki, M., Li, K., Chaiwongyen, A., Nguyen, Q. H. & Zaman, K. Deepfake speech detection: Approaches from acoustic features to

deep neural networks. IEICE. Trans. Inf. Syst. E108. D (4), 300–310. https://doi.org/10.1587/transinf.2024MUI0001 (2025).

### 3. Hawthorne, C. et al. Enabling factorized piano music modeling and generation with the MAESTRO dataset, arXiv preprint

arXiv:1810.12247 (2018).

### 4. Wen, Y. W. & Ting, C. K. Recent advances of computational intelligence techniques for composing music. IEEE Trans. Emerg. Top. Comput. Intell. 7 (2), 578–597 (2022).

### 5. Briot, J. P., Hadjeres, G. & Pachet, F. D. Deep Learning Techniques for Music Generation (Springer, 2020).

### 6. Huang, C. Z. A. et al. Music transformer. arXiv preprint arXiv:1809.04281 (2018).

### 7. Hochreiter, S. Long short-term memory. Neural Comput. (1997).

### 8. Hadjeres, G., Pachet, F. & Nielsen, F. Deepbach: A steerable model for Bach chorales generation. In: International Conference on

Machine Learning, PMLR 1362–1371 (2017).

### 9. Stais, A. Piano music generation with deep learning transformer models. (2023).

### 10. Dieleman, S., Brakel, P. & Schrauwen, B. Audio-based music classification with a pretrained convolutional network. In: 12th

International Society for Music Information Retrieval Conference (ISMIR-2011) 669–674 (University of Miami, 2011).

### 11. Machado, S. D. et al. Ambient intelligence based on IoT for assisting people with Alzheimer’s disease through context histories. Electronics 10(11), 1260 (2021).

### 12. Müllensiefen, D., Elvers, P. & Frieler, K. Musical development during adolescence: Perceptual skills, cognitive resources, and

musical training. Ann. N. Y. Acad. Sci. 1518 (1), 264–281 (2022).

### 13. Ebcioğlu, K. An expert system for harmonizing chorales in the style of JS Bach. J. Log. Program. 8, 1–2 (1990).

### 14. Xenakis, I. Formalized Music: Thought and Mathematics in Composition (Pendragon, 1992).

### 15. Ames, C. The Markov process as a compositional model: A survey and tutorial. Leonardo 22(2), 175–187 (1989).

### 16. Raphael, C. A bayesian network for real-time musical accompaniment. Adv. Neural Inform. Process. Syst. 14, 1433–1440 (2001).

### 17. Roads, C. & Wieneke, P. Grammars as representations for music. Comput. Music J. 3(1), 48–55 (1979).

### 18. Parlakgümüs, K. Generative music composition software systems using biologically inspired algorithms: A sytematic literature

review. (2015).

### 19. Takuya, F. Realtime chord recognition of musical sound: Asystem using common lisp music. In: Proceedings of the International

Computer Music Conference, Beijing (1999).

### 20. Abas Abdullah, A., Taher Karim, S. H., Azad Ahmed, S., Tariq, K. R. & Rashid, T. A. Speaker diarization for low-resource languages

through Wav2vec fine-tuning. arxiv e-prints, arXiv:2504.18582 (2025).

### 21. Abdullah, A. A. et al. From dialect gaps to identity maps: Tackling variability in speaker verification. arXiv preprint arXiv:2505.04629

(2025).

### 22. Abdullah, A. A., Tabibian, S., Veisi, H., Mahmudi, A. & Rashid, T. End-to-end transformer-based automatic speech recognition for

Northern Kurdish: A pioneering approach. arXiv preprint arXiv:2410.16330 (2024).

### 23. Abdullah, A. A., Veisi, H. & Rashid, T. Breaking walls: Pioneering automatic speech recognition for Central Kurdish: End-to-end

transformer paradigm. arXiv preprint arXiv:2406.02561, (2024).

### 24. Yang, L. Computational Modelling and Analysis of Vibrato and Portamento in Expressive Music Performance (Queen Mary University

of London, 2017).

### 25. Mienye, I. D. & Swart, T. G. A comprehensive review of deep learning: Architectures, recent advances, and applications. Information

15(12), 755 (2024).

### 26. Carpenter, P. FAIK: A Practical Guide To Living in a World of Deepfakes, Disinformation, and AI-Generated Deceptions (Wiley,

2024).

### 27. Horváth, S., Laskaridis, S., Rajput, S. & Wang, H. Maestro: Uncovering low-rank structures via trainable decomposition. arXiv

preprint arXiv:2308.14929 (2023).

### 28. Pandita, K., Thakur, P. K. S. & Annamalai, S. Contextual transcription and Summarization of audio using AI. In: Proceedings of the

5th International Conference on Information Management & Machine Intelligence 1–9 (2023).

### 29. Li, B., Liu, X., Dinesh, K., Duan, Z. & Sharma, G. Creating a multitrack classical music performance dataset for multimodal music

analysis: Challenges, insights, and applications. IEEE Trans. Multimedia. 21 (2), 522–535 (2018).

### 30. Mohammadi Farsani, R. & Pazouki, E. A transformer self-attention model for time series forecasting. J. Electr. Comput. Eng. Innov.

## (JECEI) 9 (1), 1–10 (2020).

### 31. Dong, H. W., Hsiao, W. Y., Yang, L. C. & Yang, Y. H. Musegan: Multi-track sequential generative adversarial networks for symbolic

music generation and accompaniment. In: Proceedings of the AAAI Conference on Artificial Intelligence vol. 32, no. 1 (2018).

### 32. Oore, S., Simon, I., Dieleman, S., Eck, D. & Simonyan, K. This time with feeling: Learning expressive musical performance. Neural

Comput. Appl. 32, 955–967 (2020).

### 33. Zhou, Z. & Yu, R. Automatic integration for spatiotemporal neural point processes; Advances in Neural Information Processing

Systems, 36; In: Proceedings of the 37th Conference on Neural Information Processing Systems (NeurIPS 2023) (2024). Author contributions
Man Zhang: Writing, data analysis, article review, and intellectual concept of the article. Funding
The authors have not disclosed any funding. Declarations
Competing interests
The authors declare no competing interests. Additional information
Correspondence and requests for materials should be addressed to M. Z. Reprints and permissions information is available at www.nature.com/reprints. Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/

Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:28007

| https://doi.org/10.1038/s41598-025-13064-6
www.nature.com/scientificreports/
