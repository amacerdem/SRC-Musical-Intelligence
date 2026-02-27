# Exploring a digital music teaching

**Year:** D:20

---

Exploring a digital music teaching
model integrated with recurrent
neural networks under artificial
intelligence
Yang Han
This study proposes an intelligent digital music teaching model based on Artificial Intelligence (AI)
and Long Short-Term Memory (LSTM) networks to enhance personalized assessment and feedback
in music education. Within this teaching model, the music evaluation module employs a three-layer
Bidirectional LSTM (Bi-LSTM) combined with an attention mechanism, effectively capturing the
long-term sequential features of Musical Instrument Digital Interface (MIDI) music to support the
assessment of students’ musical performances. In comparative experiments with multiple models,
the three-layer Bi-LSTM achieved a final accuracy of 91.9%, significantly outperforming other models
and validating the advantages of deep network structures in complex tasks. Further comparisons
of precision, recall, and F1-score demonstrated that the average values for the three-layer Bi-LSTM
model reached 0.87, 0.854, and 0.86, respectively, showcasing superior classification accuracy
and stability. A usability survey indicated that both piano teachers and students rated the overall
satisfaction, teaching effectiveness feedback, user experience, teaching engagement, and ease of
use of the model above 4.0, highlighting its excellent applicability and potential for broader adoption
in teaching practice. This study provides a novel approach and practical reference for AI-driven
personalized music education. Keywords  Artificial intelligence, Recurrent neural networks, Long short-term memory networks, Music
teaching model, Personalized assessment
Research background and motivations
With the rapid development of Artificial Intelligence (AI) technology, deep learning has achieved significant
progress across various domains, particularly in applications such as speech, image, and natural language
processing, gradually transforming traditional education models1–3. Music education, as a discipline that
emphasizes both artistic and technical aspects, has also begun to adopt AI technologies for innovation and
optimization in recent years. Traditional music teaching methods rely heavily on teachers’ subjective judgment
and experience, while students’ musical performance evaluations are often influenced by personal biases and
inconsistent evaluation criteria, resulting in subjective and inconsistent outcomes4–6. Thus, achieving objective
evaluations in the music teaching process has become a critical challenge in the field of educational technology. Against this backdrop, AI-based music education models have garnered increasing attention, particularly due
to the advantages of deep learning algorithms such as recurrent neural networks (RNNs) in handling sequential
data. These algorithms provide a novel solution for evaluating musical performance by accurately capturing
the temporal relationships between notes in musical compositions7,8. Such models enable more precise and
objective assessments of students’ performance quality. Additionally, AI-based music evaluation systems can
offer teachers personalized teaching suggestions, helping students focus on specific areas for improvement and
thereby enhancing the overall effectiveness of instruction9,10. This study aims to explore RNNs-based music
evaluation model and further develop an intelligent music teaching model, with the goal of providing theoretical
support and practical guidance for innovation in the field of music education. Research objectives
This study aims to explore an intelligent, digitized music teaching model supported by AI technology and
integrated with RNNs. Specifically, the objectives include: The team is designing and implementing an efficient
music evaluation model using Long Short-Term Memory (LSTM) networks, leveraging their strengths to assess
School of Music and Dance, Harbin University, Harbin 150000, China. email: hanyang@hrbu.edu.cn
OPEN
Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports

students’ performance quality on instruments such as the piano. The digital music teaching model is also being
developed based on this evaluation model, which enables personalized teaching suggestions to be provided
by teachers, tailored to each student’s individual performance, thereby helping their skills to be improved in
a targeted manner. The effectiveness of this teaching model is evaluated through experiments to validate its
potential for enhancing teaching outcomes, increasing student engagement, and improving overall teaching
quality. By achieving these objectives, this study aims to provide robust theoretical support and practical
guidance for applying AI in music education and fostering innovation within the field. Literature review
With the rapid development of emerging technologies, AI has become a vital research tool in numerous fields. Wang et al. (2023) applied AI, recommendation systems, and neural network algorithms to address the complex
entrepreneurial environment in the cultural and creative industries, developing a project recommendation
and resource optimization model. Experimental results showed that after extended training cycles, the model
achieved an identification accuracy of 81.64%11. Li et al. (2023) constructed a corporate AI application index
through text mining and analyzed data from 3,185 listed companies between 2008 and 2020. Their findings
revealed that AI applications significantly enhanced corporate innovation efficiency, with the level of AI
development in the firm’s industry and region further influencing this effect12. Mao et al. (2024) explored the
potential and challenges of generative AI in educational assessment, discussing key considerations for leveraging
this technology in education to provide educators with a framework for effectively integrating AI within digital
learning ecosystems13. Intelligent teaching evaluation has also become a research hotspot in the education field in recent years. Sajja
et al. (2024) proposed an AI-driven intelligent assistant framework—designed as a personalized and adaptive
learning platform for higher education—that utilized AI and natural language processing to deliver interactive
learning experiences14. Lee (2023) adopted a mixed-methods approach to investigate how partial qualitative
coding of essays by teachers in large-scale online courses could train machine learning models for automated
grading of remaining essays. This AI-assisted assessment system effectively enhanced the sustainability of the
feedback process and significantly improved teacher-student interaction efficiency15. With the advancement of natural language processing and machine learning technologies, sentiment
analysis has gradually become a research hotspot. It has been widely applied across various domains, including
but not limited to product review analysis, social media monitoring, and customer service improvement. Zou et al. (2024)16 proposed a framework based on multi-task shared cascade learning and machine reading
comprehension, known as Triple-MRC. The multi-task shared cascade learning approach effectively addresses
the issue of contribution allocation among components. Additionally, Zou et al. (2025)17 introduced a target-
oriented cross-modal transformer, consisting of a text-aided module, a vision-aided module, and a main module,
which facilitated further optimization of cross-modal alignment between text and images. Although these studies have achieved notable progress in AI applications, certain limitations remain. First,
most research focuses on single tasks within specific domains, such as automated text grading, entrepreneurial
recommendations, or information management. Second, current AI education models still have room for
improvement in evaluating long-term sequential data and complex learning behaviors. To address these gaps,
this study explores an AI-assisted music teaching model that integrates RNNs and attention mechanisms. The
aim is to construct a personalized and intelligent music teaching evaluation system, further enhancing teaching
effectiveness and user experience. Research model
Analysis of RNNs and LSTM principles
RNNs are a class of neural networks designed for effectively modeling sequential data. Their core characteristic
is the ability to store and transmit information across time steps via hidden layer states, allowing the model to
remember historical information within the input sequence. The basic computational process of the RNNs can
be described as follows: Assume the input sequence is {x1, x2, · · ·, xT }, where xt represents the input vector at the t-th time step,
and T is the length of the sequence. Let the hidden states be {h1, h2, · · ·, hT }, with each hidden state ht
computed as shown in Eq. (1):
ht = σ (Whht−1 + Wxxt + bh)
(1)
ht−1 denotes the hidden state from the previous time step, Wh is the weight matrix for the hidden states, Wx
is the weight matrix between the input and the hidden layer, bh is the bias vector for the hidden layer, and σ
represents the activation function. To specify the dimensions of the weight matrices, assume the input vector xt has a dimension of D
(representing the number of features at each time step), and the number of hidden layer units is H (representing
the dimension of the hidden state vector). Accordingly, the weight matrix Wxh has dimensions D × H, while
Whh has dimensions H × H. This configuration ensures that the input vector and the hidden state from the
previous time step are correctly mapped to the hidden state space of the current time step18. At each time step t, the hidden state ht is updated through a series of weighted computations that involve
both the current input and the previous hidden state. This mechanism enables the hidden state to encode
information from the present input while also preserving sequential context from prior time steps. However,
traditional RNNs encounter significant limitations when processing long sequences. The challenges, primarily
the vanishing and exploding gradient problems, severely impair their ability to learn dependencies over
Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

extended time horizons. As a result, RNNs often struggle with tasks that require capturing intricate, long-term
relationships in sequential data19. To overcome these limitations, LSTM networks were developed as an advanced extension of RNNs. The
LSTM introduces specialized memory cells, complemented by three gating mechanisms: the input gate, forget
gate, and output gate. These gates work together to regulate the flow of information, enabling the network to
retain relevant information, discard unnecessary details, and focus on essential dependencies. By effectively
addressing the vanishing gradient issue, LSTM demonstrates superior performance in handling tasks with long-
term dependencies20–22. A visual comparison of the structural differences between RNNs and LSTM is provided
in Fig. 1, highlighting the additional components that enhance LSTM’s functionality. In LSTM networks, let the input sequence be {x1, x2, · · ·, xT }, the hidden states be {h1, h2, · · ·, hT },
and the cell states (memory units) be {c1, c2, · · ·, cT }. The computational process for LSTM at time step t is
described by Eqs. (2)–(7):
ft = σ (Wfxt + Ufht−1 + bf)
(2)
it = σ (Wixt + Uiht−1 + bi)
(3)
∼ct = tanh(Wcxt + Ucht−1 + bc)
(4)
ct = ft ⊙ct−1 + it ⊙
∼ct
(5)
ot = σ (Woxt + Uoht−1 + bo)
(6)
ht = ot ⊙tanh (ct)
(7)
Fig. 1. Schematic diagram of RNNs and LSTM structures. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

ft, it, and ot denote the outputs of the forget gate, input gate, and output gate, respectively. The forget gate
determines which information from the previous cell state should be discarded. The input gate controls how
much of the current input is stored in the cell state. The output gate decides how the cell state influences the
current hidden state.
∼ct represents the candidate cell state, while ct is the updated cell state. Wf, Wi, Wc, and
Wo are the input weight matrices for each gate, while Uf, Ui, Uc, and Uo represent the corresponding hidden
state weight matrices23. bf, bi, bc, and bo denote the bias terms. σ represents the Sigmoid activation function,
tanh is the hyperbolic tangent activation function, and ⊙ denotes element-wise multiplication. By introducing memory cells and gating mechanisms, LSTM effectively preserves critical information
over long sequences, making them suitable for modeling long-term dependencies24. Consequently, LSTM is
highly applicable in music education for handling long-sequence data, such as analyzing students’ performance
behaviors, generating music fragments, and constructing evaluation models. Music evaluation model based on LSTM networks
To objectively evaluate students’ musical performance in music education, this study proposes a music evaluation
model by a Bidirectional LSTM network with Attention (Bi-LSTM-Att). The model efficiently and accurately
evaluates the quality of performances using Musical Instrument Digital Interface (MIDI) data. It provides an
intelligent tool for assisting in the music teaching process. The primary subject is MIDI-format piano music. The
model comprises three main components. These components are: a data acquisition module, a data preprocessing
module, and a music evaluation and classification module. These components are shown in Fig. 2. Data collection and preprocessing
In the data collection phase, MIDI data is transferred to the Hadoop Distributed File System (HDFS) using
the Sqoop tool. Sqoop is a utility designed for efficient data transfer between relational databases and big data
platforms. By importing data from traditional databases into HDFS, it provides support for subsequent data
processing and analysis25. HDFS, as a distributed file storage system within the Hadoop ecosystem, is capable
of storing and managing large-scale data while supporting distributed computation. Its high fault tolerance and
scalability make it particularly suited for handling big data tasks26. During the data preprocessing phase, invalid data is filtered out, and raw data is transformed into a format
suitable for neural network training. As MIDI-format piano music typically adheres to a 4/4 time signature,
timestamps are set to 1/16 notes to segment long sequences of musical data into uniform units. The preprocessing
steps include filtering out multi-track and synthesized data, while extracting key feature vectors such as pitch,
duration, and volume, to form input matrices suitable for the model27,28. Bi-LSTM network
In the Bi-LSTM-Att music evaluation model, the Bi-LSTM layer is employed to capture the bidirectional
temporal relationships inherent in MIDI music, simulating human comprehension of the sequential order
Fig. 2. Framework of the music evaluation model. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

of musical notes. To further enhance the model’s performance, a three-layer Bi-LSTM network is utilized,
increasing the model depth and strengthening its capability to represent complex temporal relationships. Let the
input sequence be {x1, x2, · · ·, xT }, where xT denotes the feature vector at time step t. The Bi-LSTM consists
of a forward LSTM and a backward LSTM. Their outputs are computed as shown in Eqs. (8) and (9):
−→
ht = LSTM(xt, −−→
ht−1)
(8)
←−
ht = LSTM(xt, ←−−
ht−1)
(9)
−→
ht and ←−
ht represent the hidden states at time step t in the forward and backward LSTM, respectively. The final
output of the Bi-LSTM is obtained by concatenating the forward and backward hidden states:
ht = [−→
ht; ←−
ht]
(10)
Attention mechanism layer
To further enhance the model’s performance, an attention mechanism is introduced following the Bi-LSTM
output. The attention mechanism automatically identifies key segments in the music, capturing features that are
most critical to the final evaluation29,30. The attention weights are calculated as shown in Eq. (11):
at,i =
exp (pt,i)
∑N
j=1exp (pt,i)
(11)
at,i denotes the attention weight assigned to the i-th feature at time step t, pt,i is the output of the scoring
function that measures the importance of a feature, and N represents the total number of features. Using the
attention weights, a context vector ct is generated:
ct =
∑
N
i=1at,ihi
(12)
hi is the hidden state at the i-th time step. By weighting and summing these hidden states, the context vector ct
effectively integrates information across different time steps. Classification layer and softmax function
After the attention mechanism layer, the context vector is passed through a fully connected layer and classified
using the Softmax function, which assigns probabilities to determine the evaluation level of the music. The
Softmax function is defined as shown in Eq. (13): S (xj) =
exp (xj)
∑K
k=1exp (xk)
(13)
S (xj) represents the probability of the output belonging to category j, xj is the j-th input feature to the
classification layer, and K denotes the total number of categories, representing the five evaluation levels: excellent,
good, fair, poor, and very poor. To optimize the classification results, the Bi-LSTM-Att model employs a cross-entropy loss function, defined
as shown in Eq. (14):

## L = −

∑
T
j=1yjlog (sj)
(14)
L represents the value of the loss function, yj denotes the actual label in the form of a one-hot vector, and sj
represents the Softmax output for the predicted label. The direct relationship between the gradient of the cross-entropy function and the Softmax output enables
efficient gradient computation, ensuring a stable and effective training process. Design of a music teaching model based on the evaluation framework
To achieve intelligent and personalized music teaching, this study proposes an innovative teaching model
based on AI and the Bi-LSTM-Att music evaluation framework. The model provides an objective assessment
of students’ performance and delivers real-time teaching feedback. It is structured around three key stages: the
Learning Input Stage, the Intelligent Evaluation Stage, and the Feedback Improvement Stage, which collectively
form an integral part of the music teaching process. Firstly, during the learning input stage, students’ performance data is collected via a MIDI interface to ensure
high-quality input for evaluation. This data includes detailed features such as note pitch, rhythm, dynamics, and
tempo. The raw MIDI data undergoes cleaning and preprocessing to be transformed into a structured format
suitable for input into the Bi-LSTM-Att model. Next, in the intelligent evaluation stage, the Bi-LSTM-Att model
is employed to automatically assess students’ performance. The model classifies the results into five grades—
Excellent, Good, Fair, Poor, and Very Poor—and generates a detailed scoring report. This report provides
teachers with an in-depth analysis of students’ performance. Finally, a personalized feedback stage is designed
based on the evaluation results. Teachers use the assessment outcomes to provide students with tailored practice
suggestions and resources. For instance, if the evaluation identifies weaknesses in rhythm control, teachers can
Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

recommend specific rhythm exercises or arrange specialized rhythm training. This data-driven approach offers
teachers clear guidance, enabling them to precisely track each student’s progress and weaknesses, and adjust their
teaching strategies accordingly. Moreover, students can use the feedback and recommended learning resources
to make independent improvements, gradually enhancing their musical performance skills. Through these interconnected stages of Learning, Evaluation, and Feedback, the AI- and Bi-LSTM-Att-
based music teaching model achieves refined and personalized guidance throughout the teaching process. This
model not only improves teaching efficiency and optimizes outcomes but also provides students with a clear path
for self-assessment and improvement. It fosters autonomous learning and musical expressiveness, effectively
meeting the demands for individualized instruction in large-scale music education settings. Although the application of Bi-LSTM and attention mechanisms in sequential data tasks is not new, this
study’s innovative application of this combination in the field of music education is undoubtedly significant. The
unique strength of Bi-LSTM lies in its ability to capture contextual information within data, which is critical
for understanding dynamic features such as melodic flow, rhythmic changes, and emotional expression in
musical performances. By processing data through both forward and backward LSTM layers in parallel, the
model comprehensively grasps the overall structure and local details of musical performances, thereby enabling
a deeper understanding of performance quality. The introduction of the attention mechanism further enhances
the model’s ability to identify key elements of a musical performance. It allows the model to dynamically adjust
its focus on different segments during evaluation, enabling detailed analysis of crucial components such as the
climax of a piece, key moments showcasing technique, or the performer’s emotional expression. This mechanism
ensures that the evaluation goes beyond general impressions, delving into the finer details of the performance,
significantly improving the objectivity and precision of the assessment. Experimental design and performance evaluation
Datasets collection
The dataset for this study was collected from two primary sources to ensure it covered piano performance data
across different skill levels and met the requirements for model training. The first part of the data was obtained
from the databases of over 30 musical instrument training institutions in City X. This dataset included extensive
performance records of beginners, intermediate, and advanced students on piano and violin, making it highly
representative. The second part of the data was sourced from the MIDIShow platform, where MIDI enthusiasts
upload their performances to be rated by other users. Ratings on MIDIShow are divided into five intervals,
corresponding to the five evaluation levels defined in this study, providing reliable evaluation labels for the
music assessment model. For consistency in training and analysis, the selected data samples included the piano
piece Ode to Joy in 4/4 time and the piano rendition of Coldplay’s Viva La Vida in 4/4 time. A total of 15,500
samples were selected, with 3,300 samples from each evaluation level, ensuring an even distribution of data
across different performance levels. The data was divided into training, testing, and validation sets in a 6:2:2
ratio for each evaluation level. The model’s performance was evaluated using accuracy, precision, recall, and F1
score as key metrics. Additionally, to comprehensively assess the application effect of the AI- and Bi-LSTM-Att-based teaching
model, a three-month application was conducted at five piano training institutions in X city. After the usage
period, a questionnaire survey was conducted to gather feedback from students and teachers on the teaching
model and the system. The questionnaire aimed to collect their experiences, satisfaction, and feedback on the
teaching effectiveness of the intelligent music teaching model, with a 5-point Likert scale used for evaluation. The questionnaires were created and distributed using Questionnaire Star, targeting the teachers and students
of these five piano training institutions. A total of 208 questionnaires were distributed and fully returned. After
screening, 202 valid responses were obtained, yielding a response rate of 97.1%. Experimental environment and parameters setting
The performance validation of the Bi-LSTM-Att model was carefully designed, with the experimental
environment and parameter settings optimized to ensure efficient convergence and the best prediction results
during model training. The experimental environment and parameter settings for the Bi-LSTM-Att model
performance validation are shown in Table 1. The Deeplearning4J deep learning framework was used, which supports distributed computing, enabling
efficient processing of large-scale data and accelerating the training process. As a deep learning library on the
Java platform, Deeplearning4J offers a flexible application programming interface that integrates effectively with
other big data tools and provides good performance optimization capabilities. The output layer node count was
set to 5, corresponding to the five levels of music evaluation (Excellent, Good, Fair, Poor, and Very Poor), which
ultimately outputs the model’s evaluation of the musical piece. With these precise hardware configurations and
reasonable parameter settings, the experiment was able to comprehensively evaluate the performance of the Bi-
LSTM-Att model in the digital music teaching model, ensuring the scientific validity and reproducibility of the
experimental results. Performance evaluation
Music evaluation performance of the Bi-LSTM-Att model
To assess the effectiveness of the music evaluation framework utilizing a deep three-layer sequential model,
comparisons were made with three other network architectures: a traditional backpropagation-based neural
network, a recurrent neural structure, and a LSTM network. These models were evaluated using the same test
dataset, and their respective accuracy outcomes are presented in Fig. 3. In Fig. 3, the three-layer Bi-LSTM model demonstrated consistent superiority over other models across all
training cycles. At the beginning of training, its accuracy stood at 31.6%, indicating a solid starting performance. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

Fig. 3. Accuracy comparison of five models. Hardware/parameter name
Configuration/value
Operating system
CentOS 7
Processor
8 cores
Memory
8GB
Storage
50GB
Integrated development environment
DVD-1908.iso
Deep learning framework
Deeplearning4J
Learning rate
0.001
Mini-batch size

Number of iterations

Optimizer
Adam
Input layer node count

First hidden layer node count

Second hidden layer node count

Third hidden layer node count

Output layer node count

Table 1. Experimental parameter settings. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

As the training iterations progressed, the model exhibited a steady and remarkable improvement, ultimately
achieving an accuracy of 91.9% by the 1000th iteration, a level that was significantly higher than that of
competing models. This exceptional performance highlights the model’s ability to capture more comprehensive
and nuanced temporal features, effectively enhancing its capability to process complex long-sequence data. Such
advantages underscore its robustness and adaptability in handling challenging evaluation tasks. To further evaluate the effectiveness of the three-layer Bi-LSTM model, a detailed comparison was conducted
with the single-layer Bi-LSTM and four-layer Bi-LSTM models. As illustrated in Fig. 4, key metrics such as
precision, recall, and F1 score were analyzed across various evaluation scenarios. These results provide additional
evidence of the superior performance and reliability of the three-layer Bi-LSTM model, confirming its suitability
for tasks requiring high precision and stability. In Fig. 4, the three-layer Bi-LSTM model exhibits significant advantages across all evaluation levels. The
average precision, recall, and F1 score of the three-layer Bi-LSTM model are 0.87, 0.854, and 0.86, respectively,
which are notably higher than those of the single-layer and four-layer Bi-LSTM models. In contrast, the four-
layer Bi-LSTM model tends to suffer from overfitting due to an excessive number of parameters, thereby
compromising its generalization ability. On the other hand, the two-layer Bi-LSTM model may lack sufficient
depth to fully capture the complexity of musical structures. These results underscore the considerable
improvement brought by increasing the number of hidden layers, which enhances the model’s ability to process
complex temporal features and ensures greater accuracy and stability in evaluating musical performances across
different levels. The enhanced architecture makes the model better equipped to handle the intricate patterns and
diversity inherent in music evaluation tasks. Furthermore, the confusion matrices for the two models are presented in Figs. 5 and 6, offering a detailed
comparison of their classification performance. Figure 5 illustrates the confusion matrix for the single-layer Bi-
LSTM model, highlighting its limitations in capturing detailed distinctions. In contrast, Fig. 6 provides a clearer
representation of the improved classification accuracy achieved by the three-layer Bi-LSTM model. In Fig. 5, the single-layer Bi-LSTM model performs well in music evaluation but still has some classification
errors. In the “Excellent” category, 76% of samples were correctly classified as “Excellent,” but 12% were
misclassified as “Good.” The recognition rate for the “Good” category is 69.5%, with a small portion of samples
incorrectly classified as “Excellent.” The confusion matrix for the three-layer hidden Bi-LSTM model is shown
in Fig. 6. Fig. 4. Performance comparison of three models under different evaluation results. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

In Fig. 6, the three-layer Bi-LSTM model demonstrates a remarkable improvement in classification accuracy
across all evaluation levels, particularly excelling in the “Excellent” and “Fair” categories, where 90% and 91%
of samples, respectively, were accurately classified. In comparison to the single-layer Bi-LSTM model, the three-
layer Bi-LSTM exhibits significant enhancements in accuracy, with an 18.4% increase in the recognition rate for
the “Excellent” category and a 21.3% increase for the “Fair” category. These results highlight the model’s superior
capability to extract and interpret complex feature information, effectively enhancing classification precision. Moreover, its advanced architecture enables better differentiation of subtle patterns and characteristics, offering
notable advantages in tasks requiring detailed analysis and reliable categorization. Teaching mode effectiveness validation
The questionnaire data were organized to assess the satisfaction and experience of both students and teachers
with the teaching mode. The results are shown in Fig. 7. In Fig. 7, most students and teachers provided high ratings for the teaching mode. The final scores for overall
satisfaction, feedback on teaching effectiveness, user experience, teaching engagement, and model usability
were 4.03, 4.07, 4.15, 4.12, and 4.1, respectively, all above 4.0. This indicates that the intelligent music teaching
mode received positive feedback in the teaching practice, not only improving the quality of instruction but also
enhancing interaction and engagement between students and teachers. Discussion
The three-layer Bi-LSTM-Att music evaluation model proposed in this study demonstrates significant
superiority in terms of accuracy and stability, with a clear competitive advantage over other traditional
models, and has received widespread praise from both teachers and students in its educational application. In
contrast, Jiang (2021) developed a vocal teaching assessment system based on a Back Propagation-Radial Basis
Function-Support Vector Machine (BP-RBF-SVM) integrated neural network. This system aimed to optimize
the quality of vocal teaching in universities by improving the accuracy and reliability of the assessments31. Wu
(2023) proposed a vocal teaching assessment model based on hybrid intelligent technologies, incorporating
Fig. 5. Confusion matrix for single-layer hidden Bi-LSTM model. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

an integrated evaluation framework constructed with convolutional neural networks, LSTM networks, and
multi-layer perceptrons. Case studies and experimental results demonstrated that this model effectively realized
automated vocal teaching assessments, reducing reliance on expert ratings32. Additionally, Yuan et al. (2023)
evaluated the generalization ability of open-source pre-trained music models, with their research showing that
although large pre-trained music language models performed excellently on most tasks, there was still room
for improvement33. Compared to these studies, the three-layer Bi-LSTM model in this study, combined with
the attention mechanism, can more effectively capture subtle feature changes in long sequences, significantly
improving the accuracy and stability of the evaluations. It particularly excels in optimizing user experience and
teaching feedback. Conclusion
Research contribution
This study combines Bi-LSTM and the attention mechanism to propose an AI-based music evaluation model
for an intelligent digital music teaching mode, aiming to enhance personalized assessments and feedback in
the music teaching process. Through experimental validation of the model’s effectiveness and a questionnaire
survey, the following conclusions are drawn:
(1)	 In the comparison of various models, the three-layer Bi-LSTM model consistently demonstrated superior
performance throughout all training cycles, achieving a final accuracy of 91.9%. This result highlights the
model’s ability to effectively capture and utilize the temporal dependencies inherent in long sequence data. Furthermore, its performance in handling complex and demanding tasks underscores the practical benefits
of employing deep network architectures. The findings validate that deeper network structures are better
equipped to process and analyze intricate temporal patterns, thereby confirming their effectiveness in im­
proving overall model capability.
(2)	 The three-layer Bi-LSTM model also exhibited substantial advantages over the single-layer Bi-LSTM model,
particularly in key evaluation metrics such as precision, recall, and F1 score, with averages of 0.87, 0.854, Fig. 6. Confusion matrix for three-layer hidden Bi-LSTM model. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

and 0.86, respectively. These results emphasize the model’s superior accuracy and robustness in evaluation
scenarios. Moreover, its classification accuracy showed a marked improvement across all evaluation met­
rics. This enhancement demonstrates that increasing the number of hidden layers enables the model to
extract more nuanced and detailed features from the data, ultimately leading to a more refined and reliable
performance in diverse evaluation tasks.
(3)	 The questionnaire survey revealed that most teachers and students gave high ratings to the teaching mode,
with overall satisfaction, feedback on teaching effectiveness, user experience, teaching engagement, and
model usability all scoring above 4.0. This indicates that the intelligent music teaching mode has received
positive feedback in educational practice. Future works and research limitations
The limitations of this study are mainly related to the diversity of the dataset and sample size, and the validation
is conducted only on piano music. Future research could expand to more music styles and complex scenarios,
improve the model’s real-time performance and accuracy, and explore the integration of other AI technologies,
such as reinforcement learning, to enhance personalized teaching outcomes. In the process of constructing and
validating the music evaluation model, the potential issue of bias in the training data needs to be considered. Different training datasets may lead to biases in the model’s evaluation of student music performances, especially
when dealing with musical works that differ significantly from the training data. To mitigate these biases, future
research should more carefully select training data to ensure it includes a wide range of musical styles and genres. Fig. 7. Statistical data of questionnaire results. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

Data availability
The datasets used and/or analyzed during the current study are available from the corresponding author Yang
Han on reasonable request via e-mail hanyang@hrbu.edu.cn. Received: 25 November 2024; Accepted: 26 February 2025
References

### 1. Chiu, T. K. F. et al. Systematic literature review on opportunities, challenges, and future research recommendations of artificial

intelligence in education. Comput. Educ. Artif. Intell. 4, 100118 (2023).

### 2. Kamalov, F., Santandreu Calonge, D. & Gurrib, I. New era of artificial intelligence in education: towards a sustainable multifaceted

revolution. Sustainability 15 (16), 12451 (2023).

### 3. Chen, X. et al. Two Decades of Artificial Intelligence in Education 2528–47 (Educational Technology & Society, 2022).

### 4. Ji, S., Yang, X. & Luo, J. A survey on deep learning for symbolic music generation: representations, algorithms, evaluations, and

challenges. ACM Comput. Surveys 56 (1), 1–39 (2023).

### 5. Hernandez-Olivan, C. & Beltran, J. R. Music composition with deep learning: A review. Adv. Speech Music Technol. Comput. Aspects Appl. 25–50. (2022).

### 6. Hong, J. W. et al. Human, I wrote a song for you: an experiment testing the influence of machines’ attributes on the AI-composed

music evaluation. Comput. Hum. Behav. 131, 107239 (2022).

### 7. Xuan, Z. DRN-LSTM: a deep residual network based on long short-term memory network for students behaviour recognition in

education. J. Appl. Sci. Eng. 26 (2), 245–252 (2022).

### 8. Ahmadian Yazdi, H., Seyyed Mahdavi Chabok, S. J. & Kheirabadi, M. Dynamic educational recommender system based on

improved recurrent neural networks using attention technique. Appl. Artif. Intell. 36 (1), 2005298 (2022).

### 9. Akgun, S. & Greenhow, C. Artificial intelligence in education: addressing ethical challenges in K-12 settings. AI Ethics 2 (3),

431–440 (2022).

### 10. Nguyen, A. et al. Ethical principles for artificial intelligence in education. Educ. Inform. Technol. 28 (4), 4221–4241 (2023).

### 11. Wang, Z. et al. Achieving sustainable development goal 9: A study of enterprise resource optimization based on artificial intelligence

algorithms. Resour. Polic. 80, 103212 (2023).

### 12. Li, C. et al. Artificial intelligence, resource reallocation, and corporate innovation efficiency: evidence from China’s listed

companies. Resour. Polic. 81, 103324 (2023).

### 13. Mao, J., Chen, B. & Liu, J. C. Generative artificial intelligence in education and its implications for assessment. TechTrends 68 (1),

58–66 (2024).

### 14. Sajja, R. et al. Artificial intelligence-enabled intelligent assistant for personalized and adaptive learning in higher education. Information 15 (10), 596 (2024).

### 15. Lee, A. V. Y. Supporting students’ generation of feedback in large-scale online course with artificial intelligence-enabled evaluation. Stud. Educ. Eval. 77, 101250 (2023).

### 16. Zou, W. et al. A multi-task shared cascade learning for aspect sentiment triplet extraction using bert-mrc. Cogn. Comput. 1–18.

(2024).

### 17. Zou, W. et al. TCMT: Target-oriented cross modal transformer for multimodal aspect-based sentiment analysis. Expert Syst. Appl.

264, 125818 (2025).

### 18. Mienye, I. D., Swart, T. G. & Obaido, G. Recurrent neural networks: A comprehensive review of architectures, variants, and

applications. Information 15 (9), 517 (2024).

### 19. Borkowski, L., Sorini, C. & Chattopadhyay, A. Recurrent Neural network-based Multiaxial Plasticity Model with Regularization for

Physics-Informed Constraints 258106678 (Computers & Structures, 2022).

### 20. Khan, A. et al. Short-term traffic prediction using deep learning long short-term memory: taxonomy, applications, challenges, and

future trends. IEEE Access 11, 94371–94391 (2023).

### 21. Huang, R. et al. Well performance prediction based on long Short-Term memory (LSTM) neural network. J. Petrol. Sci. Eng. 208,

109686 (2022).

### 22. Laghrissi, F. E. et al. Intrusion detection systems using long short-term memory (LSTM). J. Big Data 8 (1), 65 (2021).

### 23. Liu, Y. et al. A long short-term memory‐based model for greenhouse climate prediction. Int. J. Intell. Syst. 37 (1), 135–151 (2022).

### 24. Lindemann, B. et al. A survey on long short-term memory networks for time series prediction. Procedia Cirp 99, 650–655 (2021).

### 25. Uriti, A., Yalla, S. P. & Anilkumar, C. Understand the working of sqoop and hive in Hadoop. Appl. Comput. Eng., 6. (2023).

### 26. Merceedi, K. J. & Sabry, N. A. A comprehensive survey for Hadoop distributed file system. Asian J. Res. Comput. Sci. 11 (2), 46–57

(2021).

### 27. Islam, M. S. et al. Machine learning-based music genre classification with pre-processed feature analysis. J. Ilmiah Teknik Elektro

Komputer Inform. (JITEKI) 7 (3), 491–502 (2021).
28.	 Çetin, V. & Yıldız, O. A comprehensive review on data preprocessing techniques in data analysis. Pamukkale Üniv. Mühendislik
Bilimleri Dergisi 28 (2), 299–312. (2022).

### 29. Keerti, G. et al. Attentional networks for music generation. Multimedia Tools Appl. 81 (4), 5179–5189 (2022).

### 30. Soydaner, D. Attention mechanism in neural networks: where it comes and where it goes. Neural Comput. Appl. 34 (16), 13371–

13385 (2022).

### 31. Jiang, N. Construction and analysis of vocal music evaluation system based on BP-RBF-SVM integrated neural network. Journal

of Physics: Conference Series 1941 (1), 012045. (IOP Publishing, 2021).

### 32. Wu, R. A Hybrid Intelligence-based Integrated Smart Evaluation Model for Vocal Music Teaching (IEEE Access, 2023).

### 33. Yuan, R. et al. Marble: music audio representation benchmark for universal evaluation. Adv. Neural Inf. Process. Syst. 36, 39626–

39647 (2023). Acknowledgements
This work was supported by following fundings: Key Project of Economic Development in Heilongjiang Prov­
ince (Science Popularization Special) (Grant No. SKPJ202463). Harbin University Young Doctoral Research
Fund Project (Grant No. HUDF2024210). Author contributions
Yang Han: Conceptualization, methodology, software, validation, formal analysis, investigation, resources, data
curation, writing—original draft preparation, writing—review and editing, visualization, supervision, project
administration, funding acquisition. Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/

Declarations
Competing interests
The authors declare no competing interests. Ethics statement
The studies involving human participants were reviewed and approved by School of Music and Dance, Harbin
University Ethics Committee (Approval Number: 2022.256320120). The participants provided their written
informed consent to participate in this study. All methods were performed in accordance with relevant
guidelines and regulations. Additional information
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
Scientific Reports | (2025) 15:7495

| https://doi.org/10.1038/s41598-025-92327-8
www.nature.com/scientificreports/
