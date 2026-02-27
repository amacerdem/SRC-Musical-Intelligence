# The analysis of Chinese National

**Year:** D:20

---

The analysis of Chinese National
ballad composition education
based on artificial intelligence and
deep learning
Chao Zhang
This study focuses on generating national ballads with ethnic characteristics through algorithms, and
exploring the application of artificial intelligence in music composition. As an important component of
Chinese traditional culture, national ballads carry rich emotions and historical significance. However,
due to the complexity and artistry of their creation process, traditional manual composition faces
certain limitations. To address this, the study proposes a music composition model based on the
combination of the Markov chain (MC) and Bidirectional Recurrent Neural Network (Bi-RNN). The
model aims to generate melodies and emotional expressions that align with the style of ethnic
national ballads. This method uses the MC to generate the basic framework of the melody, and adopts
the Bi-RNN to further optimize rhythm and emotional expression. Experimental results show that,
compared to traditional manual composition and the MC approach in music computing, the proposed
method has significant advantages in melody creation and emotional expression. Besides, it can
generate music that is consistent with ethnic styles. This study provides a new approach and method
for the application of artificial intelligence in music composition, which has important implications for
music education and cultural heritage preservation. Keywords  National ballad, Markov chain, Bidirectional recurrent neural network, Deep learning, National
ballad composition education
National ballads are treasures of ethnic culture and one of the important art forms through which humans
express emotions and record history1. As a form of oral art passed down through generations, national ballads
contain rich ethnic sentiments and cultural memories. Their melodies, lyrics, and rhythms not only reflect the
lifestyles of the people but also depict the cultural characteristics and spirit of different regions2. In recent years,
with the acceleration of globalization and the impact of modern culture, the inheritance of traditional national
ballads has faced severe challenges. How to stimulate creative vitality in the composition of national ballads
through modern technological means has become an important issue in music education and cultural research. Chinese national ballads, as an important part of Chinese culture, have a long history and diverse forms. This
is especially obvious in regions with a large ethnic minority population, such as Guangxi and Yunnan, where their
national ballad culture is even more unique and varied. However, due to geographic limitations, interruptions
in inheritance, and insufficient innovation, the creation and dissemination of Chinese national ballads have
been constrained. In the field of music education, finding ways to use technological innovation to overcome
these limitations has become the key to promoting the inheritance and development of national ballads. Wu et
al. (2019) emphasized the importance of flexible learning for students, and highlighted that educators should
take individual differences and special educational needs into account during instruction3. Unlike traditional
education, composition education is a form of innovative learning. Wu and Chen (2021) argued that experiential
learning played a crucial role in fostering innovation in education4. Consequently, students must accumulate
significant experience before engaging in music composition. Traditional national ballads, which vary in style
depending on regional influences, further demonstrate the diversity in student composition styles. However,
the scarcity of traditional national ballad resources from various regions limits their availability for students,
making it challenging to teach national music composition. Deep learning (DL), a branch of machine learning
(ML) inspired by neural architectures, allows networks to automatically extract features from datasets and
learn complex nonlinear functions. This ability makes artificial intelligence (AI) technology a powerful tool in
School of Music and Recording Arts, Communication University of China, Beijing, Beijing 100024, China. email:
zhangchaomusic@cuc.edu.cn
OPEN
Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports

music composition, marking an innovative intersection between modern technology and artistic creation. The
integration of AI technology into music creation has significantly lowered the barriers to entry, provided rich
musical resources for teaching and greatly facilitated national ballad composition education. This study aims to introduce AI and DL technology into the creation and education of Chinese national
ballads to propose a national ballads composition model based on the Markov chain (MC) and bidirectional
recurrent neural network (Bi-RNN). By analyzing the patterns and melodic characteristics of traditional
national ballads, it adopts MC to generate stimulating melodies and combines Bi-RNN for the multi-voice
composition of the melodies. Additionally, a music scoring standard is constructed using the entropy weight
method to quantitatively evaluate the generated works and validate the effectiveness of the model. This study not
only provides technical support for national ballad composition but also explores the potential of technology in
overcoming the geographic limitations of national ballad creation. The structure of the research is as follows. Section 1 outlines the research background, content, and structure; Sect.  2 introduces the MC-based melody generation method and the Bi-RNN-based composition network
model; Sect. 3 describes the evaluation methods used, including the application of the entropy weight method
and the setting of scoring criteria; Sect. 4 presents the experimental results and discussion; Sect. 5 concludes with
the research findings and suggests directions for future research. Literature overview
In recent years, significant progress has been made in AI composition research. Zulić (2019) explored the
application of AI in composition, performance, and music education, and outlined the potential directions for
AI in music creation5. Hong et al. (2021) conducted an experiment to evaluate AI-generated music, and found
a positive correlation between human acceptance of creative AI and the evaluation of AI compositions6. Kumar
et al. (2020) provided a comprehensive summary of AI and ML techniques in algorithmic composition, and
proposed a new framework for AI-driven music creation7. Fang (2021) developed a method that combined
genetic algorithms and neural networks to automatically generate pleasant music from randomly generated
notes8. The application of AI in music composition has gradually become a research hotspot. In particular, the
development of DL technologies provides powerful technical support for music generation and creation. Min
et al. (2022) proposed a DL-based music generation system that enabled the automatic generation of melodies
and harmonies through large-scale analysis of musical works9. Their study demonstrates that AI technology
could simulate human creative logic in the music composition process, and exhibited a high level of artistic
expressiveness. Meanwhile, Bihani et al. (2023) analyzed MC-based music generation methods and introduced
an improved MC model to enhance the coherence and artistry of the generated music10. Their research provided
the theoretical foundation for the use of MC in this study. Additionally, Kumar et al. (2024) further developed
the Music Transformer model, and utilized self-attention mechanisms to generate more complex musical works
with long-distance dependencies11. In the context of the inheritance and protection of Chinese national ballads, recent research has focused
on the digitization of cultural heritage and modern creative methods. Wang (2024) proposed a multimedia-
based national ballad preservation model, which diversified the transmission of traditional national ballads by
constructing a national ballad database and an interactive learning system12. Furthermore, Chen et al. (2024)
studied the application of AI in ethnic music composition, and pointed out that DL algorithms could inject new
vitality into traditional music, enhance its appeal and expand its dissemination13. In the research of music evaluation methods, the entropy weight method has been widely applied in rating
systems for music, film, and other art forms due to its scientific and objective nature. For example, Teixeira et al.
(2021) applied the entropy weight method to the scoring system for ethnic music competitions, and optimized
the fairness of the scoring criteria through weight distribution14. In addition, Punetha et al. (2024) proposed
a music scoring system based on a multi-indicator comprehensive evaluation. They used the entropy weight
method to allocate weights to various indicators such as melody and rhythm, and improved the accuracy of the
scoring results15. Building on these research findings, this study introduces the MC and Bi-RNN into national ballad
composition and employs the entropy weight method to evaluate the generated works. It achieves innovation
both in terms of technology and evaluation methods. This study aims to further explore the potential applications
of AI technology in the inheritance and innovation of national ballads. National ballads are distinguished by
their unique melodies, modes, and rhythms16. However, existing research methods often fail to capture these
defining characteristics in the composition of national ballads. To address this, the MC17is employed to generate
motivating melodies, while a Bi-RNN model18 is used to learn and replicate the melody, mode, and rhythm
specific to national ballads. This integrated model is then utilized for the composition of national ballads. Theory and research methods
Markov model and RNN
(1) The Markov model is a statistical probability model widely used in speech recognition, speech-to-text
conversion, part-of-speech tagging, and other fields. Its application in speech recognition has been highly
successful, making it one of the most effective and accurate methods for fast speech recognition. The probabilities
associated with transitions between different states in a Markov model are known as transition probabilities. It
is assumed that the sequence of the state is j at time xt, and the sequence of the state is i at time xt−1. Then,
the state j at time xt is only related to the state i at time xt−1. Equation (1) expresses the transition probability.
pij = p (i →j) = p (xt = j |xt−1 = i)
(1)
Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

Once the transition probability pij between any two states in the system is calculated, the transition matrix
between states can be obtained. Equation (2) describes the state transition matrix P. P = [pij]k×k =


p11
p12
· · ·
p1k
p21
p22
· · ·
p2k.........
pk1
pk2
· · ·
pkk


(2)
k represents the total number of states, and pij (i, j = 1, 2, 3, · · ·, k) illustrates the probability of transferring
from the current state i to the next state j. pij should meet the following two conditions.
0 < pij < 1
(3)
k
∑
j
pij = 1
(4)
When the Markov probability model is used to predict the probability of a state of the event at the kth time, if the
state is Ej, the probability πj (k) satisfies the following conditions:
n
∑
j=1
πj (k) = 1
(5)
n indicates the total number of states. It is assumed that the initial probability vector is π (0). Then, according to
the non-aftereffect of the Markov process and Bayesian conditional probability, there is Eq. (6).
π (k) = π (k −1) P
(6)
The vector is marked as π (k) = [π1 (k), π2 (k), · · ·, πn (k)], and Eq.  (7) can be obtained through the
recurrence formula of state probability step by step.



π (1) = π (0) P
π (2) = π (1) P = π (0) P 2
· · · · · ·
π (k) = π (k −1) P = π (k −2) P 2 = · · · = π (0) P k

(7)
There is π (0) = [π1 (0), π2 (0), · · ·, πn (0)].
(2) RNN19 captures the relationship between the current output and previous outputs in a sequence, enabling
the network to retain short-term memory of time series data. This ability makes it particularly effective in natural
language processing (NLP) tasks, such as speech recognition, language modeling, and machine translation
(MT). Figure 1 provides an overview of the RNN architecture. A Bi-RNN is formed by adding a second RNN that processes the input in the opposite direction. In this
structure, the current output is influenced not only by previous outputs but also by future ones, allowing
the network to capture both past and future contextual information simultaneously20. Figure 2 indicates the
structure of Bi-RNN. RNNs often struggle with vanishing and exploding gradients when handling long-range sequence prediction
tasks. To address these issues, the gated recurrent unit is proposed as a gating mechanism21. This model is
designed to mitigate the challenges of vanishing and exploding gradients, while effectively preserving long-term
dependencies within the sequence. Fig. 1. Structure of RNN. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

Motivative melody generation by MC
Music creation begins with inspiration and motivation, and computer-assisted composition is designed to
mirror the process of human creativity. Initially, a melody that reflects personal creative intent is input, and the
composition of the entire piece unfolds based on this input. In this context, MC is applied to generate melodies,
serving as a crucial step in creating the foundational motive of a computer-generated composition. Before embarking on melody creation, it is essential to first study the unique characteristics of Chinese
national ballads. The pentatonic scale is one of the most commonly used scale structures in traditional Chinese
national ballads. Its characteristic feature is the omission of the half-step intervals present in the seven-note
scale (the fourth and seventh degrees), consisting of five notes. The typical form of the pentatonic scale includes
the “Gong, Shang, Jue, Zhi, Yu” tones, corresponding to “1, 2, 3, 5, 6” in the simplified notation system. This
scale structure offers a naturally smooth intervallic relationship, which helps create a unique ethnic style and
emotional atmosphere22. Figure 3 provides a musical score example of the pentatonic scale in the key of C. Figure 3 provides a clear example of the pentatonic scale in the key of C. It shows that the pentatonic scale
omits the fourth (F) and seventh (B) notes from the seven-note scale, thus avoiding the appearance of half-step
intervals. This simplified scale structure gives the pentatonic scale a more open and harmonious sound, which is
especially suitable for expressing the gentle and simple emotions found in traditional Chinese national ballads. The intervals in the pentatonic scale primarily involve third and fifth jumps, avoiding the tension created by half-
step intervals, and making the melody softer and more fluid. This compositional approach fully demonstrates the
central role of the pentatonic scale in national ballad creation. According to the interval structure of the pentatonic scale, there are three trisyllabic sequences: major
second + major second, major second + minor third, and minor third + major second. These trisyllabic sequences
serve as a crucial foundation for music generation, providing a key basis for the algorithm design in this study. Fig. 3. A musical score example of the pentatonic scale in the key of C. Fig. 2. Structure of Bi-RNN. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

MC is then employed to generate a pitch sequence for the motivational melodies. MC effectively captures
the patterns in note transitions, and the concept of a sound level set can be viewed as a method for combining
sound sequences. MC is relatively simple to implement and computationally efficient, making it a popular
tool for sequence prediction problems. This makes MC particularly suitable for composing national ballads,
particularly for generating motivating melodies in line with the sound level set concept23. In this context, the
recurring trilogies and their transitions in national ballads are treated as the state sequence for the MC, with
the melody being generated through the Markov state transition matrix. The key to applying this method lies in
constructing the state transition matrix. The approach used here involves creating rules for folk music knowledge
through statistical analysis of a collection of works. The state transition matrix generated by motivation melody
is obtained by music material knowledge rules. Among them, the state set is the trisyllabic sequence in the
pentatonic scale, and the trisyllabic sequence is the set tone sequence composed of any three sequential tones in
the “1”, “2”, “3”, “5” and “6” pentatonic scale. According to the two different rotation methods of “up” and “down”
of the trisyllabic sequence, the deformation modes of the trisyllabic sequence can be classified. “Up” indicates
that the pitch is arranged from low to high. There are 11 states: 123, 235, 216·, 5·6·1, 56˙1, 356, 3·5·6·, ˙2˙16, ˙2˙3˙5, ˙1˙2˙3,
and ˙3˙5˙6, numbered 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, and 21 respectively. “Down” indicates that the pitch is arranged
from high to low. There are 11 states: 321, 532, 6·12, 16·5·, ˙165, 653, 6·5·3·, 6˙1˙2, ˙5˙3˙2, ˙3˙2˙1, and ˙6˙5˙3, numbered
2, 4, 6, 8, 10, 12, 14, 16, 18, 20, and 22 respectively. In this approach, the state sequence of the MC is used to
represent the trisyllabic sequences and their transitional shifts in national ballads, with a total of 22 states. The
next step involves calculating the transfer frequencies between these trisyllabic sequence states and determining
the probability of one state transitioning to another. These data are used to construct the state transition matrix,
which then generates the pitch sequence. For generating the time value sequence, the process follows a similar method to the pitch sequence
generation. The first step is to identify all possible rhythm state types from the national ballad material library. Next, the frequency of each rhythm type transitioning to the next is recorded. The transition probabilities are
then calculated, the state transition matrix is constructed, and finally, the time value sequence is generated. Figure 4 illustrates the steps of generating motive melody by MC. Construction of composition network model
The multi-part national ballad serves as the fundamental form of national ballads. By analyzing the application
of polyphonic techniques in these multi-part compositions, this study explores the underlying principles and
patterns of multi-part national ballads in China. Guangxi, as a region rich in ethnic diversity, preserves a wide
variety of nationalities and cultural expressions, offering abundant material for this research. As a result, this
study primarily focuses on two-voice national ballads from Guangxi. To realize the national music composition model based on MC and Bi-RNN, a multi-layer neural network
architecture is designed. It integrates melodies generated by MC and emotional expression and rhythm
generation through the Bi-RNN network. The input layer of the model receives data such as note sequences,
rhythm, and modal information, which are then converted into vector form through One-hot encoding. The MC
generation module, based on a second-order MC model, generates the foundational framework for the melody
by statistically analyzing the transition probabilities between notes. This provides an initial melody sequence for
the Bi-RNN. Building on this generated melody, the Bi-RNN module further optimizes the emotional expression
and rhythm of the music. Using a bidirectional Long Short-Term Memory (LSTM) network, the Bi-RNN
simultaneously considers both past and future context to generate richer and more coherent note sequences. Then, it dynamically adjusts the output based on the features of historical input data. Finally, the output layer
converts the generated note and rhythm information into a Musical Instrument Digital Interface (MIDI) format
for subsequent audio playback and evaluation. During the training process, the MC algorithm constructs a model based on national ballad data. The model
statistically analyzes the transition frequencies between notes to calculate the transition matrix and generate
melody sequences. The specific generation process calculates the probability of the next note based on the
current and previous note states. The Bidirectional LSTM network is used to enhance the emotional expression
and optimize the rhythm of the melody. The generated melody sequence is first segmented and then input
into the Bidirectional LSTM network for further optimization. By simultaneously processing both forward and
backward sequence information, the Bi-RNN learns the structure and emotional expression of the music more
deeply. Then, it generates richer melody and rhythm sequences. Finally, the optimized melody and rhythm
sequences are combined with the MC-generated melody sequence to form a complete national ballad. In terms of data flow, the note data, rhythm, and modal information are first preprocessed and converted
into vector form via One-hot encoding before being input into the MC module. The melody sequence generated
by the MC serves as the input to the Bi-RNN, used to further optimize the melody’s emotion and rhythm. The optimized note sequence produced by the Bi-RNN undergoes post-processing and is ultimately output as
complete MIDI-format music data for subsequent audio evaluation. The proposed model uses the cross-entropy loss function to measure the accuracy of the generated note
sequence and trains the model using the Adam optimizer. During the training process, parameters such as
learning rate and batch size are adjusted to optimize the convergence speed and stability of the model. After
training is completed, the model undergoes validation to ensure that the generated music aligns with the
characteristics of national ballads and possesses a high level of emotional expressiveness. Data preprocessing
Initially, music data should be processed by an AI composer. Two commonly used audio formats for music
storage are WAV and MIDI24. While the WAV format is the most basic and accessible, it presents challenges
Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

in music data processing and may result in a loss of accuracy. As a result, MIDI format is often preferred in AI
composition, as it facilitates feature extraction and better representation of music data. The dataset used is the
Chinese Songs dataset, which contains 150 training samples of national songs and 50 test samples of songs. Rhythm is a crucial element in conveying a composer’s emotions through a melody. It is the harmonious
blend of pitch and time value, structured according to specific rules. The type of rhythm plays a significant
role in shaping the overall musical style. Without rhythm, notes are akin to people without a soul—disjointed
and lacking purpose. Rhythm organizes otherwise scattered pitch sequences into cohesive music, unveiling its
Fig. 4. Steps of generating motive melody by MC. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

artistic charm. In previous algorithmic composition approaches, pitch and time value features from the melody
are treated as independent training inputs, failing to capture the interrelationship between pitch and rhythm. To address this, an up-down sampling encoding method is proposed. This “up-sampling” technique25 samples
pitch based on the time value of each note and feeds it into the network for training, generating a prediction
model. The model then produces a pitch sequence, which is downsampled and decoded according to the time
value, yielding both pitch and time value sequences. This method allows a neural network to better learn the
deep relationship between pitch and time, ensuring that the rhythmic style of the original music is preserved in
the generated composition. Figure 5 demonstrates the flow of up-down sampling coding. Initially, the characteristics of the music’s mode, pitch, and rhythm are extracted from the MIDI-format
compositions in the national ballad material library. The music is then converted into a unified mode, followed
by upsampling coding, transforming it into a digital sequence suitable for neural network training. Upon
completion of the training, the digital sequence is transformed back into a pitch sequence for downsampling
coding. In the end, the pitch sequences, along with their corresponding time value sequences, are obtained. During the unified mode preprocessing phase, the pitch sequence and the corresponding time value sequence
are represented as follows: Pitchs = [pitch1, pitch2, · · ·, pitchn]
(8)
Durations = [duration1, duration2, · · ·, durationn]
(9)
After preprocessing the pitch sequence, the up-sampling sequences are obtained according to the up-sampling
coding of the time value sequence, that is, the input sequence of the network model. The input sequence of the
neural network is defined as follows: X = [pitch1, · · · pitch1, pitch2, · · · pitch2 · · ·, pitchn, · · · pitchn]
(10)
The number of pitches after each pitch rise sampling in the input sequence is determined by the value coding at
the time of rise and fall sampling. Construction of the composition network model
Music is created through the arrangement and combination of notes according to specific rules26. A neural
network can learn these rules and predict the notes, enabling the generation of music. In this context, a Bi-
RNN is employed to construct the prediction module for the composition network model. Initially, the
melody sequence generated by the MC serves as the input to the prediction module. Through this process, the
prediction module generates the trisyllabic sequence for voice composition. The composition’s pitch sequence
is then downsampled to yield a part pitch sequence, along with the corresponding time value sequence. Next, Fig. 5. Lifting sampling coding flow chart. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

by combining the part pitch sequence with its time value sequence, the polynomial fitting method is applied to
produce the two-part pitch and time value sequences, ensuring pitch correction. The pitch sequence and time
value sequence generated by one sound part and two sound parts are converted into corresponding MIDI audio
format for output. Figure 6 illustrates the structure of this process. Training of neural network model
Based on the input sequence and network characteristics, specific training rules are established to predict the
output pitch. This is done by using the previous pitch in the input sequence to generate a predicted output pitch,
which is then compared to the target pitch. The error is calculated, and the network parameters are updated
accordingly. The input pitch sequence is then shifted backward by one pitch distance, and the note is predicted. This process is repeated for each subsequent note. Comparison is made between the second note and the second
target node of the network prediction output to obtain the best prediction model with the minimum error after
repeated iterative training. Equation (11) illustrates the expected output note set of the network model.

## Y =



pitchi+1
pitchi+2
pitchi+3...
pitchn


(11)
Figure 7 demonstrates the network structure of the training model. The network structure of the training model consists of three primary layers. The first layer is the input
layer, responsible for receiving the input pitch sequence. The second layer is the hidden layer, which includes
the Dense layer, the Flatten layer, and the fully connected layer. The Dense layer reduces the dimensionality of
features and enhances the model’s ability to capture nonlinearity. The Flatten layer converts the features into a
one-dimensional vector before passing them to the fully connected layer, which maps the previously learned
distributed features to the f target pitch vector values. The third layer is the output layer, where the “softmax”
function is applied to compress the vector values of the f target notes into the range (0, 1). This produces the
output probabilities for the target notes, with the highest probability chosen as the predicted note. Evaluation method
Music is an art form that expresses human emotions. Due to the inherent subjectivity in how individuals
perceive and feel about music, evaluations often vary, making it challenging to assess the quality of algorithmic
compositions. To address this, five criteria—“melody, mode, rhythm, aesthetic feeling, and emotional
expression”—are established for evaluating music quality, with each category having a maximum score of 100
Fig. 6. Structure of the composition network model. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

points. The “entropy weight method”27 is employed to calculate the weight of each criterion. Professionals
are then invited to assess both the composition and its performance, and based on their evaluations, a final
composition score is computed. The panel of reviewers consists of three professors from the Composition
and Theory departments of music conservatories, four professional composers, and three experienced music
critics. All reviewers have over ten years of experience in music practice or research and are well-versed in
the characteristics and compositional style of Chinese national ballads. Prior to scoring, all reviewers undergo
standardized training on the evaluation criteria to minimize individual differences and ensure consistency in the
assessment process. A total of 30 pieces of music are selected for performance, among them, 10 are composed
manually and 10 are from the algorithmic composition. The weighting28 step of the entropy weight method is divided into three steps, and each step is briefly
described in combination with the evaluation index of music: At first, the data of each index are standardized. Five indicators are defined as X1, X2, X3, X4, X5, for which
there is Xi = {x1, x2, · · · x30}. Y1, Y2, Y3, Y4, Y5 represent the value after standardizing the processing of each
indicator data. Among them, Yij denotes the value of the ith index of the jth piano music after standardized
treatment. Equation (12) indicates the calculation process. Yij =
Xij −min (Xi)
max (Xi) −min (Xi)
(12)
Then, the information entropy of each index needs to be calculated. Equations  (13) and (14) indicate the
calculation process.
pij = Yij/
n
∑
i=1
Yij
(13)
Hi = −
(
n
∑
i=1
pij ln pij
)
/ ln (n)
(14)
In Eqs. (13) and (14), Hi represents the ith entropy of the index. Finally, a calculation is carried out on the entropy of the five indicators of “melody, mode, rhythm, aesthetic
feeling and emotional expression”, and the weight of each indicator. Equation  (15) signifies the calculation
process. Wi =
1 −Hi
5 −∑
Hi 
(15)
Wi refers to the weight of the ith indicator. A calculation is conducted on the evaluation score of each music. Equation (16) illustrates the calculation
process. Fig. 7. Network structure of the training model. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

Sj =

∑
i=1
XijWi
(16)
Sj means the score of the jth music. Experimental design process
The custom code and algorithms used in this study are shared via the GitHub platform. Readers can access the
code through the following link: ​h​t​t​p​s​:​/​/​g​i​t​h​u​b​.​c​o​m​/​g​k​d​0​f​K​0​O​K​/​M​a​r​k​o​v​-​c​h​a​i​n​-​a​n​d​-​b​i​d​i​r​e​c​t​i​o​n​a​l​-​r​e​c​u​r​r​e​n​t​-​n​
e​u​r​a​l​-​n​e​t​w​o​r​k​-​b​i​-​R​N​N​-​f​o​r​-​c​o​m​p​o​s​i​n​g​-​C​h​i​n​e​s​e​-​f​o​l​k​-​s​o​n​g​s​/​b​l​o​b​/​m​a​i​n​/​R​E​A​D​M​E​.​m​d​? plain=1. To validate the
effectiveness and general applicability of the proposed Markov Bi-RNN-based music composition method, the
following experimental process is designed: Dataset Preparation: Ten manually composed national-style songs are collected from 5sing.kugou.com. Using the Markov Bi-RNN model, ten songs are generated algorithmically. Additionally, ten songs are generated
using the MC algorithm for comparison. Dataset Partitioning: All data are divided into three parts: Training Set: Used to train the Markov Bi-RNN and MC models, containing 15 songs (including both
manually composed and model-generated songs). Validation Set: Contains 8 songs, used for hyperparameter adjustment and model selection during the
training process. Test Set: The remaining 7 songs serve as the final test set, used to verify the model’s generalization ability and
evaluate performance. All datasets maintain a consistent musical style to ensure the validity and accuracy of the experimental results. To clearly demonstrate the implementation steps of the experiment, a flowchart is designed, as shown
in Fig. 8. The flowchart illustrates key steps such as dataset preparation, model training, and calculation of
evaluation metrics. Fig. 8. Experimental Process. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

Results
Experimental results
The dataset used here includes 30 national ballads, of which 10 are manually created national ballads sourced
from the renowned Chinese original music websites 5sing and Kugou. These songs are composed by various
folk musicians and showcase strong ethnic characteristics. Another 10 songs are generated using the Markov
Bi-RNN model, serving as algorithmically composed works. The final 10 songs are generated by a manually
crafted MC model. All data are original works, and there are no copyright disputes involved. All songs are
traditional Chinese national ballads, featuring rich melodic variations and rhythmic patterns that reflect the
distinctiveness of Chinese traditional music. Each song has an approximate duration of 10 min, encompassing
a range of emotional expressions and aesthetic experiences, making them suitable as examples for folk song
creation. It is ensured that all datasets consist of public or original data, exclusively for non-commercial
purposes, adhering to ethical guidelines for academic research. No commercial copyrighted materials are used
here. Figure 9 denotes the results. The actual length of each national ballad ranges from 3 to 5 min. During the
evaluation process, to ensure a comprehensive and efficient assessment, the entire music piece is played without
a fixed 10-minute duration. The total listening time is approximately 120 min (2 h). To minimize the potential
effects of prolonged listening on the attention and judgment of the evaluators, the review process is divided into
two sessions. Each session involves playing 15 national ballads, with ample break time in between to ensure that
the evaluators remain in optimal listening condition throughout the process. Each evaluator completes their
scoring independently, without being informed of the creation method of each piece, to maintain fairness and
impartiality in the evaluation. Figure 8 compares manually composed national ballads with those generated
using two AI-based algorithmic approaches: the MC model and the Markov Bi-RNN model proposed. Music
generated by the MC model mainly relies on probabilistic statistical patterns to create compositions. The Markov
Bi-RNN model composing refers to the algorithmic approach based on the Markov Bi-RNN model proposed. Manual compositions, created by professional musicians using traditional methods, are represented by gray
bars in the chart. These pieces are sourced from the 5sing.kugou.com original music platform, certified by
professional platforms, and are of high artistic value and representativeness. Figure 9 suggests that the score of manual composition is better than that of MC composition and the Markov
Bi-RNN model in terms of melody, mode, rhythm, aesthetic feeling, and emotional expression. When the
Markov Bi-RNN model is used for composition, the scores, rhythm, and melody, mode are scored 85.1, 88.3, and
87.1 respectively. In comparison, manual composition receives scores of 95.7, 93.2, and 89.7, respectively. This
Fig. 9. Average score of each index of composition created in different ways. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

demonstrates that the Markov Bi-RNN model produces compositions with a national style, making it well-suited
for national ballad creation. In terms of aesthetic feeling and emotional expression, the Markov Bi-RNN model
scores higher than the MC composition, but both AI-generated methods fall significantly behind the manual
composition. This indicates substantial room for improvement in these areas within AI composition techniques. Table 1 presents the scores of music composed in the three ways, separately. Table 2 lists the average of 10 pieces of music for various composition methods, and the overall effect of each
composition method. In Table  2, the overall score of manual composition is better than that of AI composition. The overall
performance of the constructed Markov Bi-RNN model is significantly better than the MC model, but only
slightly lower than manual composition. It means that music created in this way satisfies people’s appreciation
of national ballads to a certain extent. Table 1 shows that some compositions created with the Markov Bi-RNN
model achieve higher scores than certain manually composed songs, such as MIDI-02 and MIDI-15, which
scores 92.1 and 93.4, respectively, surpassing MIDI-01’s score of 91.2. While 100% of the manually composed
songs score over 90, only 20% of those generated by the Markov Bi-RNN model reach scores above 90. In
addition, the scores of other fields are all above 80, indicating that the model is practical, but further research
and improvement are needed. To further validate the universality and effectiveness of the method, the Lakh MIDI Dataset is selected as
supplementary experimental data. This publicly available dataset contains a large number of MIDI-format music
Composition method
Average Score
Manual composition
93.62
MC
80.87
Markov Bi-RNN model
87.22
Table 2. The average score of music of songs created in different ways. Music number
Score
Composition method
MIDI-01
91.2
Manual composition
MIDI-02
92.1
Markov Bi-RNN model
MIDI-03
90.7
Manual composition
MIDI-04
79.2
MC composition
MIDI-05
98.7
Manual composition
MIDI-06
83.7
Markov Bi-RNN model
MIDI-07
93.1
Manual composition
MIDI-08
80.1
MC composition
MIDI-09
87.9
Markov Bi-RNN model
MIDI-10
94.3
Manual composition
MIDI-11
96.3
Manual composition
MIDI-12
75.4
MC composition
MIDI-13
77.5
MC composition
MIDI-14
93.2
Manual composition
MIDI-15
93.4
Markov Bi-RNN model
MIDI-16
83.5
MC composition
MIDI-17
85.4
Markov Bi-RNN model
MIDI-18
85.3
MC composition
MIDI-19
93.5
Manual composition
MIDI-20
82.1
MC composition
MIDI-21
83.2
MC composition
MIDI-22
90.9
Manual composition
MIDI-23
82.9
MC composition
MIDI-24
84.3
Markov Bi-RNN model
MIDI-25
86.7
Markov Bi-RNN model
MIDI-26
94.3
Manual composition
MIDI-27
87.1
Markov Bi-RNN model
MIDI-28
83.5
Markov Bi-RNN model
MIDI-29
79.5
MC composition
MIDI-30
88.1
Markov Bi-RNN model
Table 1. Scores of each composition music. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

works, covering various styles and genres. By conducting experiments on this dataset, the performance of the
algorithm across different musical styles can be tested, allowing for the evaluation of the model’s generalization
ability and diversity. Specifically, 20 representative works are selected from the dataset, spanning classical,
pop, and electronic music, to verify the effectiveness of the Markov Bi-RNN model in different types of music
composition. Table 3 presents the comparison of experimental results between the self-built dataset and the
Lakh MIDI Dataset. It can be observed that the experimental results on both datasets exhibit similar trends
across most evaluation metrics. Specifically, manually composed songs generally score higher across various
indicators, indicating that human-composed national ballads excel in melody, rhythm, and emotional expression. In contrast, while songs generated using the Markov Bi-RNN model show scores close to those of manually
composed pieces, there remains a certain gap in emotional expression and aesthetic feeling. To comprehensively evaluate the performance of the proposed Markov Bi-RNN model, two mainstream
baseline models—LSTM and Transformer-based models—are introduced for comparison. All models are
trained and tested on the same dataset and evaluation metrics to ensure the comparability of the results. Table 4
displays the average scores of each model on different evaluation metrics. As observed, the Markov Bi-RNN
model outperforms MC composition, LSTM, and Transformer models in all evaluation metrics, approaching the
level of manual composition. Specifically, this model achieves scores of 85.1, 88.3, and 87.1 for melody, mode,
and rhythm, respectively. It significantly surpasses MC composition (melody: 79.2, mode: 80.1, rhythm: 75.4),
and is slightly lower than manual composition (melody: 95.7, mode: 93.2, rhythm: 89.7). In terms of aesthetic
feeling and emotional expression, the Markov Bi-RNN model also scores better than other AI composition
methods but still lags behind manual composition. To further validate the effectiveness of the Markov Bi-RNN model, its performance is compared with the
LSTM and Transformer models in music generation tasks. Table 5 presents the results of different models in
terms of Bilingual Evaluation Understudy (BLEU) scores and music feature similarity are shown in. It reveals
that the Markov Bi-RNN model outperforms the other AI composition methods in both BLEU score and music
feature similarity, further demonstrating its advantage in generating music with national style and emotional
expression. Discussion
In summary, the analysis of the MC and RNN models provides valuable insights into the melody and creation
of national ballads. The findings indicate that combining Markov’s algorithm with RNN enhances the quality
Model
BLEU Scores
Music Feature Similarity
Manual Composition
-
-
MC Composition
65.4
70.2
Markov Bi-RNN
78.5
80.3
LSTM
72.0
75.0
Transformer
75.3
77.8
Table 5. Performance of different models in BLEU score and music feature similarity. Evaluation Metric
Manual Composition
MC Composition
Markov Bi-RNN
LSTM
Transformer
Melody
95.7
79.2
85.1
82.5
84.0
Mode
93.2
80.1
88.3
85.0
86.5
Rhythm
89.7
75.4
87.1
80.3
83.2
Aesthetic Feeling
90.5
78.3
82.0
79.5
81.0
Emotional Expression
92.0
76.0
83.5
80.0
82.5
Average Score
93.62
80.87
87.22
81.46
83.17
Table 4. Average scores of each model on different evaluation metrics. Dataset
Composition Method
Melody
Mode
Rhythm
Aesthetic Feeling
Emotional Expression
Average Score
Self-Built Dataset
Manual Composition
95.7
93.2
89.7
91.2
92.0
93.62
Markov Bi-RNN Model
85.1
88.3
87.1
79.0
80.5
87.22
MC Composition
80.1
83.2
79.5
70.6
75.3
80.87
Lakh MIDI Dataset
Manual Composition
94.5
92.7
88.4
90.0
91.5
93.10
Markov Bi-RNN Model
85.7
87.2
86.5
78.2
79.8
86.80
MC Composition
82.5
81.3
78.1
71.0
74.9
78.60
Table 3. Comparison of experimental results between the Self-Built dataset and the Lakh MIDI dataset. Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

of musical compositions. In addition, Bell (2021)29examined ballad music and education, describing how
Bates’ approach to ballad teaching has evolved across editions and presenting early American academic
ballads. The results denoted that ballad research can improve classroom teaching efficiency. Khamhongsa et
al. (2021)30conducted research on the creative melody of contemporary music. The results demonstrated that
modern Molam bands and other ballads were based on Isaan national ballads. Askarova (2021)31studied the
great song genres in Uzbek folk music, covering Uzbek musical creativity and complex playing styles with the
theme of “Uzbek Musical Creativity”. Hariyadi et al. (2019)32 analyzed the ballads of the Aoxin and ethnic
pedagogy. The purpose was to explore the character and values contained in the ballads of the Nanmeng tribe
of the Aoxin. This was of great significance for explaining the national educational value of different national
music. Therefore, the research results manifest that the proposed Markov Bi-RNN model can provide practical
reference and value for national ballads and education. Conclusion
This study aims to explore the potential application of AI algorithms in the creation of national ballads to
enhance the automation level of ethnic music composition. To achieve this, a music creation model combining
the Markov model and Bi-RNN is proposed and systematically compared with traditional manual composition
and MC model-generated music. The research process employs a comprehensive evaluation system based on
five criteria: melody, mode, rhythm, aesthetic feeling, and emotional expression. Professionals in the music
field are invited to evaluate 30 pieces of national ballads, including 10 manually composed national ballads,
10 pieces generated by the MC model, and 10 pieces generated by the proposed model. The results show that
while the manually composed pieces perform best across all criteria, the Markov Bi-RNN model performs
similarly to manual compositions in the core dimensions of melody, mode, and rhythm, outperforming the MC
model-generated music. Notably, some works created with this model even score higher than certain manually
composed pieces, suggesting that the model has potential feasibility and practical value in ethnic music creation. However, this study also has some limitations. For example, in terms of emotional expression and aesthetic
feeling, AI-generated music still falls short. This highlights the need for future research to improve the model
to better capture emotional details in music composition. Additionally, future studies could explore how to
incorporate more music style features and user-specific needs to enhance the diversity and adaptability of AI-
generated compositions. In summary, this study has achieved preliminary results in the field of ethnic music
creation and demonstrated the potential of AI technology in this domain. It is hoped that the research here can
provide valuable references for subsequent studies and contribute to the inheritance and innovation of ethnic
culture. Data availability
The human participants/human dataset were not directly involved in the manuscript. The datasets used and/
or analyzed during the current study are available from the corresponding author Chao Zhang on reasonable
request via e-mail zhangchaomusic@cuc.edu.cn. Received: 5 July 2024; Accepted: 4 March 2025
References

### 1. Pan, Y. Y. et al. Effect of music intervention on depression in graduate students. Music Educ. Res. 23 (1), 41–49 (2021).

### 2. Song, C. Development and utilization of National folk music resources in vocal music courses in new era local universities.

## CONVIVIUM 34, 39–47 (2018).

### 3. Wu, W. et al. Effect of narcissism, psychopathy, and machiavellianism on entrepreneurial intention the mediating of entrepreneurial

self-efficacy. Front. Psychol. 10, 360–360 (2019).

### 4. Wu, Y. J. & Chen, J. C. Stimulating innovation with an innovative curriculum: A curriculum design for a course on new product

development. Int. J. Manage. Educ. 19 (3), 100561 (2021).

### 5. Zulić, H. How AI can change/improve/influence music composition, performance and education: three case studies. INSAM J. Contemp. Music Art Technol. 1 (2), 100–114 (2019).

### 6. Hong, J. W., Peng, Q. & Williams, D. Are you ready for artificial mozart and Skrillex? An experiment testing expectancy violation

theory and AI music. new. Media Soc. 23 (7), 1920–1935 (2021).

### 7. Kumar, L., Goyal, P. & Kumar, R. Creativity in machines: music composition using artificial intelligence. Asian journal for

convergence in technology. 6(2): 36–40. (2020). https://doi.org/10.33130/AJCT.2020v06i02.007

### 8. Fang, Y. Research on application of ethnic music in piano teaching in colleges and universities. J. Front. Art Res. 1 (5), 25–28 (2021).

### 9. Min, J. et al. Music generation system for adversarial training based on deep learning. Processes 10 (12), 2515 (2022).

### 10. Bihani, H. et al. Automatic music melody generation using LSTM and Markov chain model check for updates. IOT Smart Syst.:

## ICTIS. 2 (720), 249 (2023).

### 11. Kumar, A. & Lal, A. Applying recurrent neural networks with integrated attention mechanism and transformer model for

automated music generation. Int. J. Smart Sustainable Intell. Comput. 1 (2), 58–69 (2024).

### 12. Wang, Y. Virtual sound image reconstruction method for Multi-objective optimization of folk music based on evolutionary

algorithm. ACM Trans. Asian Low-Resource Lang. Inform. Process. 23 (6), 1–15 (2024).

### 13. Chen, D. et al. Digital technology in cultural heritage: construction and evaluation methods of AI-Based ethnic music dataset. Appl. Sci. 14 (23), 10811 (2024).

### 14. Teixeira, S. J. et al. Evaluation model of competitive and innovative tourism practices based on information entropy and alternative

criteria weight. Tour. Econ. 27 (1), 23–44 (2021).

### 15. Punetha, N. & Jain, G. Integrated Shannon entropy and COPRAS optimal model-based recommendation framework. Evol. Intel.

17 (1), 385–397 (2024).

### 16. Doush, I. A. & Sawalha, A. Automatic music composition using genetic algorithm and artificial neural networks. Malaysian J. Comput. Sci. 33 (1), 35–51 (2020).

### 17. Munthali, M. G. et al. Modelling land use and land cover dynamics of Dedza district of Malawi using hybrid cellular automata and

Markov model. Remote Sens. Applications: Soc. Environ. 17, 100276 (2020). Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/

### 18. Wang, F. et al. A day-ahead PV power forecasting method based on LSTM-RNN model and time correlation modification under

partial daily pattern prediction framework. Energy. Conv. Manag. 212, 112766 (2020).

### 19. Mao, X. T. et al. Semi-random subspace with Bi-GRU: fusing statistical and deep representation features for bearing fault diagnosis. Measurement 173, 108603 (2021).

### 20. Zhao, F. et al. Time-sequenced flow field prediction in an optical spark-ignition direct-injection engine using bidirectional

recurrent neural network (bi-RNN) with long short-term memory. Appl. Therm. Eng. 173, 115253 (2020).

### 21. Zhao, R. et al. Machine health monitoring using local feature-based gated recurrent unit networks. IEEE Trans. Industr. Electron.

65 (2), 1539–1548 (2017).

### 22. Forkert, A. Magical serialism: modernist enchantment in Elisabeth Lutyens’s O Saisons, O châteaux! Twentieth-Century Music. 14

(2), 271–303 (2017).

### 23. Ramanto, A. S. & Maulidevi, N. U. Markov chain based procedural music generator with user chosen mood compatibility. Int. J. Asia Digit. Art Des. Association. 21 (1), 19–24 (2017).

### 24. Wu, S., Dai, G. & Heterotopia A study on the Spatial practice of midi music festival. Hum. Geogr. 33 (161), 49–56 (2018).

### 25. Yang, Y., Kim, D. & Oh, B. T. Deep convolutional grid warping network for joint depth map upsampling. IEEE Access. 8, 147580–

147590 (2020).

### 26. Harmon, J. & Adams, R. G. Building a life note-by-note: music and the life course. World Leisure J. 60 (2), 140–155 (2018).

### 27. Bao, Q. et al. Can entropy weight method correctly reflect the distinction of water quality indices?? Water Resour. Manage. 34 (11),

3667–3674 (2020).

### 28. Na, W. & Zhao, Z. C. The comprehensive evaluation method of low-carbon campus based on analytic hierarchy process and

weights of entropy. Environ. Dev. Sustain. 23 (6), 9308–9319 (2021).

### 29. Bell, M. J. Katharine Lee Bates’ ballad book and the pedagogy of the ballad. J. Am. Folklore. 134 (533), 319–342 (2021).

### 30. Khamhongsa, A. et al. The creation of contemporary music from Isan folk melodies: the modern Molam, all-Thidsa Molam band. Rev. Int. Geographical Educ. Online. 11 (10), 43–50 (2021).

### 31. Askarova, S. Great song genre in the ethno music of Uzbek folk music. JournalNX 7 (05), 131–134 (2021).

### 32. Hariyadi, S., Tamalene, M. N. & Hariyono, A. Ethnopedagogy of the Osing tribe folk song: exploration and formation of biology

learning character. Biosfer: Jurnal Pendidikan Biologi. 12 (2), 258–276 (2019). Author contributions
Chao Zhang: Conceptualization, methodology, software, validation, formal analysis, investigation, resources,
data curation, writing—original draft preparation, writing—review and editing, visualization, supervision, pro­
ject administration, funding acquisition. Funding
This work was supported by Key Laboratory of Intelligent Processing Technology for Digital Music (Zhejiang
Conservatory of Music), Ministry of Culture and Tourism (Grant No.: 2024DMKLB004). Declarations
Competing interests
The authors declare no competing interests. Ethical approval
The studies involving human participants were reviewed and approved by School of Music and Recording
Arts, Communication University of China Ethics Committee (Approval Number: 2022.04956545). The
participants provided their written informed consent to participate in this study. All methods were performed
in accordance with relevant guidelines and regulations. Additional information
Correspondence and requests for materials should be addressed to C. Z. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:9215

| https://doi.org/10.1038/s41598-025-93063-9
www.nature.com/scientificreports/
