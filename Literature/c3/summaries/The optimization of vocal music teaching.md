# The optimization of vocal music teaching

**Authors:** victor chen
**Year:** D:20

---

## ARTICLE IN PRESS

Article in Press
The optimization of vocal music teaching
by integrating the STEAM concept with the
intelligent recommendation system
Scientific Reports
Received: 16 August 2025
Accepted: 24 November 2025
Cite this article as: Su F. & Guo Q. The
optimization of vocal music teaching
by integrating the STEAM concept with
the intelligent recommendation system. Sci Rep (2025). https://doi.org/10.1038/
s41598-025-30288-8
Fanbo Su & Qianping Guo
We are providing an unedited version of this manuscript to give early access to its
findings. Before final publication, the manuscript will undergo further editing. Please
note there may be errors present which affect the content, and all legal disclaimers
apply. If this paper is publishing under a Transparent Peer Review model then Peer
Review reports will publish with the final article.
https://doi.org/10.1038/s41598-025-30288-8
© The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit
to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do
not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain
permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/4.0/.

## ARTICLE IN PRESS

Article in Press
The optimization of vocal music teaching
by integrating the STEAM concept with the
intelligent recommendation system
Scientific Reports
Received: 16 August 2025
Accepted: 24 November 2025
Cite this article as: Su F. & Guo Q. The
optimization of vocal music teaching
by integrating the STEAM concept with
the intelligent recommendation system. Sci Rep (2025). https://doi.org/10.1038/
s41598-025-30288-8
Fanbo Su & Qianping Guo
We are providing an unedited version of this manuscript to give early access to its
findings. Before final publication, the manuscript will undergo further editing. Please
note there may be errors present which affect the content, and all legal disclaimers
apply. If this paper is publishing under a Transparent Peer Review model then Peer
Review reports will publish with the final article.
https://doi.org/10.1038/s41598-025-30288-8
© The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit
to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do
not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain
permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/4.0/.

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

The Optimization of Vocal Music Teaching by Integrating
the STEAM Concept with the Intelligent Recommendation
System
Fanbo Su1, Qianping Guo2,*
1School of Art, Chongqing College of Humanities, Science & Technology, Chongqing, 401524, China;
305903169@qq.com
2College of Music, Chongqing Normal University, Chongqing, China; 15340524767@163.com
*Correspondence: 15340524767@163.com
Abstract: To improve the personalization and intelligence level of vocal music teaching, this study
integrates the Science, Technology, Engineering, Arts, and Mathematics (STEAM) concept into an
intelligent recommendation system. It proposes a teaching optimization model based on multimodal
learning and sentiment analysis (SA). The study comprehensively applies Neural Collaborative
Filtering (NCF) to realize personalized recommendations, Deep Q-Network (DQN) to optimize
teaching strategies, and Generative Adversarial Network (GAN) to generate diverse resources. It
also combines multimodal fusion and SA to achieve real-time evaluation. The experiment is based
on public data sources such as LibriSpeech, YouTube-8M, Common Voice, and TED-LIUM. The
results show that this model outperforms traditional methods in recommendation precision (F1-
Score: 0.88), teaching strategy stability (97.24%), resource generation quality (97.91%), and
multimodal fusion accuracy (99.79%). The study demonstrates the advantages of the in-depth
integration of the STEAM concept and artificial intelligence. At the same time, it provides a
practical new path for optimizing and promoting vocal music teaching. However, the real-time
synchronization and deep semantic alignment among multimodal features still inevitably have
certain limitations due to the computational complexity of existing algorithms and the limitations
of model generalization abilities. In the future, a lightweight architecture and adaptive constraint
mechanism can be combined to gradually improve the relevant technical paths. Keywords: Optimization of vocal music teaching; Neural Collaborative Filtering; Deep Q-Network; Generative Adversarial Network; STEAM concept

### 1 Introduction

1.1 Research Background and Motivations
In recent years, with the swift development of artificial intelligence (AI) and big data
technology, the traditional vocal music teaching model has faced many challenges [1]. The demand
for personalized and intelligent teaching is increasing, but existing systems still have shortcomings
in processing multimodal data, real-time feedback, and sentiment analysis (SA) [2,3]. Therefore,
this study integrates the Science, Technology, Engineering, Arts, and Mathematics (STEAM)
concept into an intelligent recommendation system. The vocal music teaching process is optimized
to enhance the teaching effect and student engagement by combining multimodal learning (ML) and
SA methods [4-6]. An efficient, robust, and practical optimization model for vocal music teaching

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

is implemented by integrating advanced algorithms and open data sources.
1.2 Research Objectives
Although existing studies on vocal music teaching optimization have achieved certain results
in introducing personalized recommendations, ML, and AI methods, there are still obvious
shortcomings. On the one hand, the in-depth fusion of multimodal data is insufficient. Multi-source
information, such as audio, video, and text, is often used in isolation, and a unified feature modeling
framework is lacking. On the other hand, current intelligent recommendation systems mostly stay
at static matching or single-dimensional optimization, failing to dynamically capture and real-time
adjust students' learning status and emotional feedback. In addition, existing models have limited
performance in handling long-tail user behaviors and extreme data, and it is hard to balance
personalization and robustness. This restricts the effect of teaching optimization in practical
applications. These shortcomings indicate that the intelligent development of vocal music teaching
urgently needs a systematic method that can balance multimodal data fusion, real-time feedback,
and strategy optimization. Grounded on this, the study constructs an optimization model of vocal music teaching driven
by ML and SA by combining the STEAM concept with an intelligent recommendation system. Specific objectives include improving the accuracy of personalized recommendations, optimizing
teaching strategies through Deep Q-Network (DQN), and using the Generative Adversarial Network
(GAN) to enhance teaching resources' diversity and quality. In addition, multimodal data and
emotional feedback are integrated to facilitate the teaching process's real-time response and
guidance effect. Finally, a remarkable improvement in teaching effect is achieved, and student
engagement is enhanced [7]. This design breaks through the limitations of traditional models in
single modality, static recommendation, and limited feedback. It provides vocal music teaching with
a complete integrated solution that can achieve "accurate matching - dynamic optimization -
resource expansion - real-time evaluation". Thus, an overall improvement can be realized in
teaching effectiveness, student engagement, and system intelligence levels.

### 2 Literature Review

2.1 The Application of AI and ML in Music Education
Over the years, the integration of AI and ML in education and music has gradually become a
research hotspot. Chang et al. (2024) proposed the MusicARLtrans Net model, which integrated
speech-to-text and Reinforcement Learning (RL) algorithms. This model achieved an accuracy of
96.77% on the LibriSpeech dataset and markedly improved the real-time feedback effect of
interactive music education [8]. Sharif and Uckelmann (2024) introduced the Knowledge-driven
and INtelligent Guidance for Holistic Teaching (KNIGHT) framework in education. They explored
the application of multimodal data integration and Deep Reinforcement Learning (DRL) in
educational analysis. Meanwhile, they focused on the issue of privacy-protected personalized
feedback and revealed the complexity of educational technology in the digital context [9]. Govea et
al. (2024) realized real-time emotion detection and personalized teaching strategies through DRL. The emotion recognition accuracy increased from 72.4% to 89.3%, and the personalization level
rose from 70.2% to 90.1%. This indicated that emotion-driven changing adjustment played a key
role in learning effectiveness [10]. Zaman et al. (2025) combined an Efficient Convolutional Neural
Network (EfficientNet) with a convolutional neural network (CNN) optimized by transfer learning. This combination achieved an accuracy of 94.36% on the Facial Expression Recognition 2013
(FER-2013) dataset for human emotion recognition tasks, further strengthening the technical

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

foundation of multimodal emotion feedback modeling [11]. At the same time, Zhang (2025) verified
through comparative experiments that STEAM courses could effectively promote students'
interdisciplinary knowledge transfer in music teaching. This enabled students to show stronger
comprehensive abilities in lyric interpretation, understanding of creative backgrounds, and aesthetic
appreciation, highlighting the STEAM concept's in-depth value for music education [12]. Besides, Daneshfar et al. (2024) systematically reviewed semi-supervised graph clustering technology,
pointing out its potential in complex data analysis. They also provided methodological inspiration
for the structured processing of multimodal data in education and art fields [13]. Meanwhile, Keshun et al. (2024) showed new progress in the research of multimodal and
physical information fusion. They proposed a fusion framework that combined acoustic vibration
signals, physical constraints, and deep learning models. By embedding physical laws such as kinetic
equations and energy conservation into the loss function, the model was guided to follow the
constraint relationships of the real system during the feature learning process. Thus, pure data-driven
models' overfitting and non-interpretability problems could be avoided [14][17]. This method
realizes the dynamic correlation modeling between multi-modal signals while strengthening the
expression of causal dependence between different signals through the attention mechanism. It
enables the model to perform feature allocation and semantic interpretation under physical
consistency. Although this direction mainly serves the state recognition of mechanical systems, its
idea of "multi-modal representation guided by physical constraints" can also be transferred to the
field of vocal music teaching. It can be used to construct a collaborative modeling mechanism for
audio, video, and emotional feedback, thereby improving feature interpretability and the scientific
nature of teaching feedback.
2.2 Research Progress of Recommendation Systems and Generative Models in Teaching
Optimization
In terms of audio and video generation as well as educational resource expansion, Ahmad et al.
(2025) proposed Deformable Periodic Network GAN (DPN-GAN). This model effectively
improved the resolution and fidelity of audio synthesis by introducing periodic Rectified Linear
Unit (ReLU) activation and deformable convolutional networks. It outperformed mainstream GAN
architectures on multiple datasets, offering a reference for the generation of high-quality vocal
practice resources [18]. Tong et al. (2024) proposed the Wav2Vid system, which used GAN to
generate video avatars from audio. While maintaining perceived quality, it reduced the transmitted
data volume by up to 83%, demonstrating the potential to reduce redundant data in distance
education and interactive scenarios [19]. Bethencourt-Aguilar et al. (2023) verified the practical
value of GAN in educational resource generation, with user satisfaction reaching as high as 92.1%
[20]. In terms of recommendation and personalization, Prabhakar and Lee (2023) analyzed students'
audio based on convolutional neural networks. It achieved a recommendation accuracy of 82.5%
and promoted the development of behavior data-based learning recommendation systems [21]. The
multimodal fusion model constructed by Chango et al. (2022) achieved a fusion accuracy of 94.2%
after integrating audio, video, and text information. This illustrated the advantages of multimodal
data collaboration in learning analysis [22]. Prottasha et al. (2022) used Bidirectional Encoder
Representations from Transformers (BERT) to conduct SA, achieving a classification accuracy of
88.7% and improving the effectiveness of intelligent feedback systems [23]. The DQN optimization
method proposed by Oroojlooyjadid et al. (2022) simulated the learning process, increasing the
cumulative reward by 15.3%. This verified the potential of RL in dynamic teaching strategy

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

optimization [24]. Meanwhile, Vaziri et al. (2024) conducted a comprehensive evaluation of various
machine learning methods. They emphasized the advantages and disadvantages of different models
in multi-objective tasks and provided a reference for selecting multimodal algorithms in educational
scenarios [25]. Overall, the above studies have gradually promoted the in-depth integration of music
education and AI technology from multiple perspectives, including recommendation, generation,
emotion recognition, and strategy optimization. A conclusion can be drawn from existing studies. AI-driven personalized recommendation,
multimodal fusion, and RL have achieved substantial progress in education and music teaching, and
can significantly improve learning experience and teaching efficiency. This emphasizes the core
role of cross-modal data integration, intelligent recommendation, and emotion recognition in future
teaching optimization. However, most of the existing achievements focus on performance
improvement of a single task or module, such as improving recommendation accuracy, enhancing
audio synthesis quality, or optimizing emotion detection accuracy. They lack systematic integration
of multimodal interaction, sentiment-driven feedback, and resource generation. At the same time,
there are still distinct deficiencies in handling long-tail user behaviors, extreme data, and teaching
robustness. Facing the growing demand for personalization and real-time performance, existing
studies mostly stay at "local optimization" and fail to form a complete teaching optimization loop. In real vocal music teaching scenarios, however, it is often necessary to balance artistic expression
and scientific optimization. Therefore, this study proposes an intelligent recommendation-driven
vocal music teaching optimization model that integrates the STEAM concept. It uses Neural
Collaborative Filtering (NCF) to improve the accuracy of personalized recommendations; DQN is
utilized to realize optimization of strategies; GAN is employed to expand high-quality and diverse
teaching resources. It also combines attention mechanism-based ML and SA to achieve real-time
feedback, to build an integrated framework of "accurate matching - dynamic optimization - resource
expansion - real-time evaluation". This fills the gaps in existing studies and promotes the intelligent
and personalized development of vocal music teaching.

### 3 Research Model

3.1 The STEAM Concept
The STEAM concept refers to integrating Science, Technology, Engineering, Arts, and
Mathematics in education. Students' innovative thinking and problem-solving ability are cultivated
through the interdisciplinary integrated teaching mode. This concept emphasizes the integration of
disciplines and uses art as a medium to stimulate students' creativity and practical ability, thus
promoting all-around development and knowledge application. The STEAM concept's key features
and representations are presented in Figure 1.

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Science
Arts
Mathematics
Engineering
Technology
STEAM
Inquiry, Experimentation
Creativity, Expression
Logic, Analysis
Design, Problem-solving
Innovation, Application
Figure 1: The key features and representations of the STEAM concept
3.2 Related Algorithms of the Optimization Model for Vocal Music Teaching
3.2.1 The Neural Collaborative Filtering (NCF) algorithm
The NCF algorithm is a recommendation algorithm that integrates neural networks and
collaborative filtering technology. By capturing the non-linear interaction between users and
projects, a Multilayer Perceptron (MLP) is used to model complex user preference patterns to
improve the recommendation system's accuracy and effect [26]. The core calculation of personalized recommendation based on NCF is:
(1) Calculation of user embedding vector
𝑃𝑢= 𝑊𝑃⋅(
𝑥𝑢
∥𝑥𝑢∥) + 𝑏𝑃 (1)
𝑃𝑢 means the embedding vector of user 𝑢; 𝑊𝑃 refers to the user embedding matrix;
𝑥𝑢
∥𝑥𝑢∥
indicates the normalized user feature vector; 𝑏𝑃 stands for the user embedding vector to calculate
the bias vector.
(2) Computation of item embedding vectors
𝑄𝑖= 𝑊𝑄⋅(
𝑦𝑖
∥𝑦𝑖∥) + 𝑏𝑄 (2)
𝑄𝑖 refers to the embedding vector of item 𝑖; 𝑊𝑄 represents the item embedding matrix;
𝑦𝑖
∥𝑦𝑖∥
is the normalized item eigenvector; 𝑏𝑄 means the item embedding vector to calculate the bias
vector.
(3) Interactive computation of embedding vectors
𝑧𝑢𝑖= 𝑐𝑜𝑛𝑐𝑎𝑡((𝑃𝑢∘𝑄𝑖), (𝑃𝑢+ 𝑄𝑖), |𝑃𝑢−𝑄𝑖|) (3)
𝑧𝑢𝑖 represents the connected representation of the user and the project embedding vector; ∘

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

denotes the Hadamard product (element product); |𝑃𝑢−𝑄𝑖| means the absolute value of the
element, and 𝑐𝑜𝑛𝑐𝑎𝑡 refers to the vector join operation.
(4) Computation of MLP
ℎ𝑙= 𝑓(
𝑊𝑙⋅ℎ𝑙−1+𝑏𝑙
√∑
𝑑𝑙−1
𝑘=1 (𝑊𝑙⋅ℎ𝑙−1)2) (4)
ℎ𝑙, 𝑊𝑙, and 𝑏𝑙 represent the hidden vector, weight matrix, and bias vector of the 𝑙th layer; 𝑓
is the activation function; ℎ𝑙−1 and 𝑑𝑙−1 refer to the output and dimension of the previous layer.
(5) Calculation of the final prediction score
𝑦̂𝑢𝑖= 𝜎(
ℎ𝐿⋅𝑤𝑜+𝑏𝑜
1+𝑒𝑥𝑝 (−(ℎ𝐿⋅𝑤𝑜+𝑏𝑜))) (5)
𝑦̂𝑢𝑖 refers to the predicted score of the user 𝑢 on item 𝑖; ℎ𝐿 denotes the output of the last
layer; 𝑤𝑜 and 𝑏𝑜 are the weight and bias of the output layer; 𝜎 is the sigmoid function. In NCF, the calculation of user vector 𝑃𝑢 and item vector 𝑄𝑖 is essentially a vectorized mapping
of learner features and teaching resource features. Through normalization, the model can emphasize
relative relationships rather than absolute differences in high-dimensional space. This allows
students' learning behaviors and music piece features to be compared on a unified scale. This design
does not simply pursue algorithm performance, but aligns with the scientific and mathematical
dimensions in the STEAM framework: it transforms artistic performances into quantifiable
structures, enabling individual differences to be modeled and explained. In the interaction
representation of Equation (3), the product, sum, and difference of vectors are considered
simultaneously, reflecting the multi-level alignment and differences between students and music
pieces. The modeling logic here has an inherent similarity to "style matching" in art education:
instead of relying on a single indicator, it uses multi-angle mathematical operations to reveal
potential learning paths. Finally, the MLP realizes non-linear mapping through Equations (4) and
(5), further abstracting this complex relationship to form a recommendation probability. Its value
lies in providing a mathematically driven interpretation framework for the teaching process,
allowing art education to go beyond empirical judgments.
3.2.2 The DQN algorithm
The DQN algorithm combines the Deep Neural Network (DNN) and reinforcement learning. This algorithm also uses DNN to approximate the Q function (the action-value function) and learns
the optimal strategy through environmental interaction [27]28]. Meanwhile, by simulating the
interaction between students and teaching content, teaching strategies can be dynamically adjusted
to achieve personalized teaching and improve learning efficiency [29,30]. The core calculation of teaching strategy optimization by the DQN is as follows:
(1) Update of the Q value
𝑄(𝑠𝑡, 𝑎𝑡) ←𝑄(𝑠𝑡,𝑎𝑡) + 𝛼(𝑟𝑡+ 𝛾𝑚𝑎𝑥
𝑎′  𝑄(𝑠𝑡+1, 𝑎′) −𝑄(𝑠𝑡, 𝑎𝑡)) (6)
𝑄(𝑠𝑡, 𝑎𝑡) represents the Q value of the 𝑎𝑡 taken in the state 𝑠𝑡; 𝛼 means the learning rate;
𝑟𝑡 refers to the immediate reward; 𝛾 is the discount factor; 𝑚𝑎𝑥
𝑎′  𝑄(𝑠𝑡+1, 𝑎′) denotes the
maximum Q value of the next state 𝑠𝑡+1 [31].
(2) Loss function

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

ℒ(𝜃) = 𝔼(𝑠,𝑎,𝑟,𝑠′) [(𝑟+ 𝛾𝑚𝑎𝑥
𝑎′  𝑄(𝑠′, 𝑎′; 𝜃−) −𝑄(𝑠, 𝑎; 𝜃))

] (7)
ℒ(𝜃) means the loss function; 𝜃 is the parameter of the Q network; 𝜃− denotes the
parameter of the target Q network; (𝑠, 𝑎, 𝑟, 𝑠′) represents the sample in the empirical replay [32].
(3) Calculation of the target Q value
𝑦𝑡= 𝑟𝑡+ 𝛾𝑚𝑎𝑥
𝑎′  𝑄(𝑠𝑡+1, 𝑎′; 𝜃−) (8)
𝑦𝑡 stands for the target Q value.
(4) Update of experience replay pool
𝐷←𝐷∪{(𝑠𝑡, 𝑎𝑡, 𝑟𝑡,𝑠𝑡+1)} (9)
𝐷 represents the experience replay pool; (𝑠𝑡,𝑎𝑡,𝑟𝑡, 𝑠𝑡+1) denotes the current experience.
(5) Parameter update
𝜃←𝜃−𝜂∇𝜃ℒ(𝜃) (10)
𝜂 refers to the learning rate, and ∇𝜃ℒ(𝜃) is the gradient of the loss function.
(6) Expansion of the Bellman equation
𝑄(𝑠𝑡, 𝑎𝑡) = 𝔼[𝑟𝑡+ 𝛾𝑚𝑎𝑥
𝑎′  𝑄(𝑠𝑡+1, 𝑎′)|𝑠𝑡,𝑎𝑡] (11)
In the core update Equation (6) of DQN, the learning of state-action value depends on the
quantitative description of students' performance, such as intonation deviation, rhythm stability, and
timbre consistency. The introduction of these indicators is not only for strategy optimization, but
also reflects the reconstruction of artistic subjectivity by scientific and engineering methods: the
"good" and "bad" that originally relied on teachers' intuition are now translated into measurable
signals. The loss function in Equation (7) and the calculation of the target Q-value in Equation (8)
aim to continuously adjust the parameters of the strategy network, enabling the teaching process to
dynamically follow changes in students' states. This mechanism actually corresponds to the
"engineering-feedback" link in STEAM, that is, maintaining the system's stability and
personalization through continuous testing and correction.
3.2.3 The GAN algorithm
GAN consists of generators and discriminators that generate high-quality vocal practice
content through adversarial training. The generator is responsible for generating new practice
resources; the discriminator is used to evaluate the authenticity and validity of the generated content
[33-35]. The core calculation of resource generation based on GAN is:
(1) The loss function of the generator
ℒ𝐺= −𝔼𝑧∼𝑝𝑧(𝑧)[log 𝐷(𝐺(𝑧))] (12)
ℒ𝐺 stands for the loss function of the generator; 𝐺(𝑧) represents the sample generated by the
generator; 𝐷(𝐺(𝑧) means the discriminator's discrimination result on the generated sample; 𝑝𝑧(𝑧)
denotes the distribution of latent variables [36].
(2) The loss function of the discriminator
ℒ𝐷= −𝔼𝑥∼𝑝data(𝑥)[log 𝐷(𝑥)] −𝔼𝑧∼𝑝𝑧(𝑧) [log (1 −𝐷(𝐺(𝑧)))] (13)
ℒ𝐷 means the loss function of the discriminator, 𝑥 denotes the real sample, and 𝑝data(𝑥)
represents the distribution of the real data.
(3) The weight update of the discriminator
𝜃𝐷←𝜃𝐷−𝜂𝐷∇𝜃𝐷ℒ𝐷 (14)

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

𝜃𝐷 and 𝜂𝐷 refer to the weight parameter and learning rate of the discriminator; ∇𝜃𝐷ℒ𝐷
represents the gradient of the discriminator loss function to the weight parameter [37-39].
(4) Wasserstein GAN loss function
ℒ𝐷= 𝔼𝑥∼𝑝data(𝑥)[𝐷(𝑥)] −𝔼𝑧∼𝑝𝑧(𝑧)[𝐷(𝐺(𝑧))] (15)
In GAN, the adversarial training relationship between the generator and discriminator loss in
Equations (12) Equation (13) is not just an algorithmic game. Conversely, they can be understood
as the tension between artistic creation and scientific verification. The generator tries to synthesize
materials similar to real singing, while the discriminator provides an "objectified critique," similar
to the professional evaluation of a teacher. Through this dynamic balance, the system can form a
continuously evolving resource library. The audio generated by GAN is used as practice materials
and further input into the NCF recommendation module as candidate resources. The generator
expands the boundaries of artistic resources, and the recommendation system integrates them into
the overall path of personalized learning. Thus, scientific modeling, technical implementation, and
artistic creation form a closed loop. The mapping relationship among the STEAM concept, NCF/DQN/GAN technical tools, and
educational functions is displayed in Figure 2: Figure 2: The mapping relationship among the STEAM concept, NCF/DQN/GAN technical
tools, and educational functions
In Figure 2, the STEAM concept is systematically transformed into the internal logical
framework for algorithm design and teaching optimization in the proposed intelligent
recommendation system. The Science dimension is reflected in the quantitative modeling and law
extraction of the vocal music learning process. By establishing testable hypotheses and data
feedback mechanisms, it converts teaching behaviors into an observable and verifiable scientific
process. The Technology dimension is integrated into the multi-modal data fusion and knowledge
representation system. It emphasizes the dynamic transmission and structural coordination of
information flow, enabling the system to form stable semantic consistency and adaptive correlation
at the auditory, visual, and textual levels. The Engineering dimension is embodied in the real-time

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

feedback and continuous optimization mechanism of the system architecture. Through parameter
constraints and self-adjustment of the objective function, it simulates strategy improvement and path
optimization in teaching, and constructs a learning closed loop with self-evolution ability. The Arts
dimension is not an additional rhetorical element in the design, but one of the core driving forces. The system incorporates emotional expression, aesthetic consistency, and expressive intention into
the selection and generation of learning resources, making the recommendation results conform to
logical efficiency and have artistic appeal and educational resonance. The Mathematics dimension
runs through the system's underlying structure and serves as the formal basis for realizing the above
concepts. Whether in constructing embedded space, allocating feature weights, or verifying
convergence and optimization solutions, mathematical logic provides the model with rigorous
theoretical constraints and interpretability support. Thus, the STEAM concept no longer stays at the
level of educational philosophy. Instead, through structural mapping and function embedding, it
becomes a generative framework and the core of innovative logic for the design of the
recommendation system.
3.3 The Integrated System Architecture of the Vocal Music Teaching Optimization Model
Under the guidance of the STEAM concept, the constructed vocal music teaching optimization
model is not a simple stack of single technologies. Instead, it forms a functional system centered on
data-driven logic through the integration of scientific methods, engineering modeling, and art
education. Specifically, the system first inputs audio, video, and text into the multimodal evaluation
(ML/SA) module. Through feature extraction, attention mechanism, and SA, it realizes unified
modeling of cross-modal features, thereby converting students' singing performance, emotional
fluctuations, and learning status into quantifiable indicators. This objective data serves as real-time
feedback to the teaching process and provides basic support for subsequent modules. Subsequently,
the NCF personalized recommendation module uses the NCF method to achieve in-depth matching
between students' learning features and teaching resource features. This ensures that the
recommendation results can match students' skill levels and meet the needs of improving their
artistic expression. At the same time, the GAN resource generation module expands diverse vocal
practice materials through adversarial training. This alleviates the problems of limited traditional
teaching resources and a single style, and continuously supplements the generated resources to the
recommendation and evaluation links, enhancing the richness and creativity of learning. Regarding
strategy optimization, the DQN module dynamically adjusts teaching strategies based on the
learning status and emotional feedback from the teaching platform. This ensures that the teaching
progress is compatible with students' emotional states, avoiding excessive frustration and preventing
learning stagnation. Through the interactive flow of the above modules, the system realizes a closed-
loop process from multimodal data collection, accurate recommendation, resource expansion to
strategy optimization. It combines the interdisciplinary integration in the STEAM concept with the
creative needs of art education, thereby solving the problem of over-reliance on teachers' experience
and subjective judgment in traditional vocal music teaching. This enables artistic evaluation to be
based on scientific data and dynamic optimization, ultimately promoting vocal music teaching to
achieve objective, personalized, and intelligent development. The integration implementation process of the proposed vocal music teaching optimization
model's system architecture is shown in Figure 3:

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Figure 3: The integration implementation process of the system architecture for the vocal
music teaching optimization model

### 4 Experimental Design and Performance Evaluation

This study integrates the STEAM concept into the intelligent recommendation system to
optimize vocal music teaching. It selects key algorithms from four major optimization directions:
personalized recommendation, teaching strategy optimization, resource generation, and
comprehensive assessment; it aims to enhance teaching effectiveness and student engagement. The
specific optimization processes and implementation principles are as follows: First, personalized recommendation utilizes DNN to process user data (learning progress and
feedback) and item data (practice repertoire). Meanwhile, it constructs an interaction matrix and
generates high-dimensional embeddings for users and items. Through MLP, it learns users' latent
ratings for items and makes personalized teaching content recommendations based on predicted
ratings, achieving precise matching. Second, modeling the teaching environment as a Markov Decision Process (MDP), the study
employs the DQN algorithm to optimize teaching strategies for improving student learning
outcomes and engagement. DQN continuously updates the state-action values approximated by the
Q-function, utilizing techniques such as experience replay and target networks to optimize teaching
strategies [44]. This process adjusts teaching content and methods in real-time to maximize student
learning progress and satisfaction. Regarding resource generation in vocal music teaching, the generator takes random noise as

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

input to simulate vocal exercise audio. The discriminator provides feedback by comparing real and
generated audio signals. Through iterative adversarial training, the generator improves its capability
to produce increasingly realistic exercise resources, enriching teaching materials and enhancing
student interest and engagement Error! Reference source not found.. In a comprehensive assessment, ML and SA are integrated to analyze audio, video, and text
data, extracting features including facial expressions and actions. Attention mechanisms are used to
fuse multimodal features and the BERT model for sentiment classification. Then, an evaluation
model is constructed to offer real-time feedback on student learning outcomes and emotional states,
guiding teaching optimizations.
4.1 Datasets Collection
During the model validation process, data collection and processing are conducted through
public channels to ensure the avoidance of ethical issues. A total of no less than 300,000 pieces of
audio, video, and text data are collected using large-scale open-source datasets such as LibriSpeech, YouTube-8M, Common Voice, AVSpeech, TED-LIUM, and VoxCeleb. Compared with other open-
source datasets that can be accurately adapted to vocal music types, the TED-LIUM and VoxCeleb
general speech datasets are selected. This is because they cover a wide range of speaker
characteristics and high-quality speech samples. These data can provide the model with diverse
speech patterns and emotional features. Although they are not specialized vocal music datasets, their
speech diversity and transferability help improve the model's generalization ability in vocal music
teaching scenarios. Data preprocessing encompasses audio feature extraction, video frame
segmentation, and others. Through standardization, denoising, and data enhancement techniques,
data quality and diversity can support the efficiency and reliability of model training and validation
[45]. In the data preprocessing stage, all multimodal data undergo a unified process of feature
extraction and standardization. The LibriSpeech and Common Voice datasets are the main audio
and text sources. They undergo silent segment truncation, amplitude normalization, and feature
extraction (Mel-Frequency Cepstral Coefficients (MFCC), Chroma, Spectrogram), respectively. Text samples are processed through cleaning, lowercasing, and synonym replacement. Meanwhile,
sample diversity is enhanced through standardization and corresponding augmentation strategies
(such as noise addition, frequency masking, and semantic replacement). The YouTube-8M and
AVSpeech datasets mainly provide video and multimodal samples. They first undergo frame
extraction, facial key point detection, and frame standardization. Then, CNN and 3D-CNN extract
frame-level features, followed by brightness normalization and frame augmentation. The TED-
LIUM dataset mainly consists of high-quality transcribed text. After text cleaning, lowercasing,
tokenization, and synonym replacement, it is stratified by speaker ID to maintain the diversity and
independence of the corpus. Before feature extraction, the VoxCeleb audio data uses Voice Activity
Detection (VAD) and energy normalization to filter out segments with low signal-to-noise ratio. Subsequently, MFCC and Chroma features are extracted, and noise addition is adopted for data
augmentation. To ensure sample balance and representativeness, all datasets are divided into training set,
validation set, and test set at a ratio of 8:1:1. For cross-data source tasks, five-fold cross-validation
is used to reduce data bias. Input data in the training stage are all standardized by Z-score. The
length of audio samples is unified to a 4-second window, the video frame sampling rate is set to 24
fps, and the text sequence length is truncated to 256 tokens. These measures ensure the dimensional
consistency of multimodal features. After preprocessing and division, the total amount of data

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

reaches 327,837 entries. The dataset information is exhibited in Table 1: Table 1: The proposed dataset
Data source
Data
type
Data
volume
Preprocessing
steps
Feature
extraction
methods
Standardization
Data
enhancement
LibriSpeech
Audio 84893
Feature
extraction
MFCC, Chroma
Standardization
Noise
addition
LibriSpeech
Text

Text cleaning
Tokenization
Lowercase
Synonym
replacement
YouTube-
8M
Video

Frame
extraction
CNN for
Frames
Frame
standardization
Frame
enhancement
YouTube-
8M
Text

Text
vectorization
BERT
Embeddings
/
/
Common
Voice
Audio

Feature
extraction
Spectrogram
Standardization
Frequency
mask
AVSpeech
Video

Frame
extraction
3D-CNN
Frame
standardization
Frame
enhancement
TED-LIUM
Text

Text cleaning
Tokenization
Lowercase
Synonym
replacement
VoxCeleb
Audio

Feature
extraction
MFCC, Chroma
Standardization
Noise
addition
In the multi-source data integration stage, the six datasets are not used in isolation. Instead,
they are mapped to unified learning units by aligning labels and timestamps. Specifically, audio
samples correspond to vocal music segments, video samples correspond to performance movements
or classroom clips, and text samples are associated with lyrics, teaching prompts, or student
feedback. This multimodal information is uniformly labeled as teaching resource units, which form
the "items" in the interaction matrix. Correspondingly, "users" refer to individual students. Their
historical learning trajectories, singing records, and emotional expressions are mapped to the same
space. This method abstracts data of different modalities into comparable units, allowing NCF to
directly model the relationship between students and cross-modal resources. In the unified modeling process, audio features (MFCC, Chroma, spectrogram), video frame
features (expressions and movements extracted by CNN/3D-CNN), and text features (BERT-based
embedding vectors) are aligned with the learning trajectories of individual students; it aims to
construct a cross-modal "user-item" interaction matrix. Among them, "users" are defined as
individual students, and "items" are specified as vocal music teaching resources. These resources
include existing music pieces, practice segments, and teaching videos; meanwhile, extended
materials are generated by GAN. After this processing, NCF can capture the interaction relationship

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

between students and multimodal resources in a unified space. In the experimental implementation
of DQN, the state 𝑠𝑡 is mapped to the quantifiable performance of a student at a certain moment. This includes intonation deviation, rhythm stability, timbre consistency, and emotional tone
(obtained through the joint analysis of the emotional color of text feedback and singing audio by
BERT). The action 𝑎𝑡 corresponds to the specific intervention method selected by the system in the
next teaching step, such as recommending new practice pieces, adjusting difficulty, or providing
emotional feedback. The reward 𝑟𝑡 takes the comprehensive indicators of the students' immediate
performance improvement (e.g., reduced intonation error, improved rhythm stability) and subjective
feedback scores. In the GAN part, the generator adopts a Conv-Deconv structure, which takes
random noise vectors and simplified music score segments as input to generate vocal practice audio. The discriminator is based on a convolutional discriminant network, which distinguishes between
generated samples and real audio, and uses feedback signals to optimize the generator in a reverse
manner. Through this design, the system generates materials similar in style to the target music
library and produces audio with differences in pitch, rhythm, and emotional color. This provides
diverse resource support for subsequent recommendations and training links.
4.2 Experimental Environment
The experimental environment is listed in Table 2: Table 2: Experimental environment
Category
Parameter
Specification
Hardware environment
Central Processing Unit (CPU)
Intel Xeon E5-2680 v4
Graphics Processing Unit
(GPU)
NVIDIA Tesla V100
Memory

## 128GB DDR4

Software environment
Operating system
Ubuntu 20.04 LTS
Programming language
Python 3.8
4.3 Parameters Setting
To further verify the contribution of each module to the overall system performance, a
systematic ablation experiment is designed. The specific method involves removing or replacing
key components one by one. 1. NCF is replaced with traditional CF to observe changes in the effect
of personalized recommendation; 2. DQN is removed, leaving only static recommendations without
dynamic teaching strategy optimization; 3. GAN is removed, relying only on real data resources; 4. ML/SA is removed, using only single-modal speech features as evaluation input. All experimental
groups and the complete model run under the same environment and data conditions. The following
indicators are calculated respectively. Recommendation accuracy: The F1-score is calculated based
on the consistency between predicted results and actual interaction records. Strategy stability: It is
measured by the fluctuation range of the cumulative reward curve in multiple training rounds. Generation diversity: The gap between generated and real samples is quantified based on the
distribution difference of Mel spectrum features. Sentiment recognition accuracy: Determined by

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

the consistency between the model's classification results and the labels of public benchmark data. The results are listed in Table 3: Table 3: Comparison of ablation experiment results
Model settings
Recommendation
accuracy
Strategy
stability (%)
Generation
diversity
index
Sentiment
recognition
accuracy (%)
Complete model
0.88
97.24
0.93
99.79
Replace NCF with CF
0.74
96.81
0.91
99.65
Remove DQN
0.87
84.56
0.92
99.72
Remove GAN
0.85
96.93
0.00
99.77
Remove ML/SA
0.87
97.15
0.92
83.64
It can be found from the results that each module makes a remarkable contribution to the system
performance. When NCF is replaced with traditional CF, the recommendation accuracy decreases
most obviously (F1-score drops from 0.88 to 0.74), which indicates the necessity of deep modeling. Removing DQN leads to a significant decline in teaching strategy stability (dropping from 97.24%
to 84.56%), demonstrating the key role of RL in real-time teaching feedback. After removing GAN,
the resource generation diversity index drops to 0 directly, verifying the unique contribution of this
module in expanding practice resources. Removing the ML/SA module causes a sharp decline in
sentiment recognition accuracy (dropping from 99.79% to 83.64%), showing that single-modal
evaluation is difficult to capture complex sentiment features. Overall, the four modules complement
each other and jointly ensure the integrity and advantages of the system in personalized
recommendation, dynamic optimization, resource expansion, and sentiment feedback. During the formal verification process, the optimized system's stability is first analyzed by
examining parameters such as training epochs, learning rate variations, batch size changes, and data
noise levels. Subsequently, model convergence and parameter sensitivity are assessed to evaluate
the system's stability and robustness under diverse conditions. This ensures that the model maintains
high performance and consistency across various scenarios. The parameters for robustness testing
are given in Table 4: Table 4: Robustness test parameters
Parameter
Value
Description
Training epochs
100 epochs
The length of the model training epochs, used to observe
long-term stability
Batch size
changes
±32
The impact of batch size changes on training effectiveness

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Data noise
levels
±5%
Changes in noise levels introduced in input data
Model
convergence
Convergence speed
and error
Convergence speed and error analysis of models under
different conditions
Parameter
sensitivity
Performance
fluctuations
Sensitivity of the model to parameter changes and
performance fluctuations
Second, the study uses six publicly available data sources, including LibriSpeech, YouTube-
8M, Common Voice, AVSpeech, TED-LIUM, and VoxCeleb. The effectiveness of personalized
recommendations is validated across six groups of data. Each group covers multimodal information
such as student learning progress, audio features, and textual feedback. Personalized
recommendations are made by constructing user-item interaction matrices and employing the NCF
algorithm to generate a high-dimensional embedded representation. The optimization process is
assessed using indicators such as Mean Absolute Error (MAE), precision, recall, F1-score, and Root
Mean Square Error (RMSE) to demonstrate the advantages of personalized recommendations in
vocal music teaching. Among them, the F1 value is calculated based on the harmonic mean of
Precision and Recall; MAE and RMSE measure the error between the predicted score and the actual
feedback, respectively. The used NCF parameters are detailed in Table 5: Table 5: The NCF parameters of the proposed model in the personalized recommendation
validation
Parameter
Value
User embedded size

Project embedding size

Hidden layer
[64, 32, 16]
Activation function
ReLU
Optimizer
Adam
Training data volume

Third, the effectiveness of DQN in optimizing teaching strategies is evaluated based on
cumulative rewards, learning curves, and strategy stability indicators. By simulating learning
processes and adjusting parameters, the convergence and optimization effects of DQN are verified
to ensure the effectiveness and stability of optimized strategies. To ensure the interpretability and
stability of the optimization of teaching strategies, this study designs a composite reward function
in the DQN:
𝑅𝑡= 𝛼𝐴𝑡+ 𝛽𝑃𝑡−𝜆𝐿𝑡 (16)
𝐴𝑡 represents the learner's immediate performance improvement in the current round (such as
the reduction rate of intonation error and the improvement rate of rhythm stability); 𝑃𝑡 denotes the

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

teaching path matching degree (calculated from the similarity between the recommendation result
and the learning goal); 𝐿𝑡 is a strategy fluctuation penalty term, which is used to suppress excessive
exploration. The parameter weights are set to 𝛼=0.4, 𝛽=0.5, and 𝜆=0.1 to balance individual
performance and strategy stability. In the result analysis, independent sample t-tests and one-way
Analysis of Variance (ANOVA) are used to verify the statistical significance of the DQN
optimization effect. The two methods conduct significance tests on cumulative rewards, learning
curve slopes, and strategy convergence values, with the significance level set to p < 0.05. Statistical
results show that the optimized DQN model is remarkably superior to the baseline model in
convergence speed and strategy stability; this verifies the effectiveness and robustness of the
teaching strategy optimization. Other key parameters of DQN in the study are detailed in Table 6: Table 6: The proposed model's DQN parameters in teaching strategy optimization verification
Parameter
Value
State size

Action size

Playback buffer size

Discount factor (Gamma)
0.95
Target update frequency

Maximum exploration

Minimum exploration
0.01
Explore attenuation
0.99
Training set size

Verification set size

Fourth, the GAN's performance in generating high-quality and diverse vocal exercise resources
is evaluated using indicators such as generation quality, diversity, and user satisfaction. Combining
signal processing techniques and subjective evaluations, the study analyzes the practical value of
GAN-generated resources in educational practices. The used GAN parameters are drawn in Table
7: Table 7: GAN parameters of the proposed model in resource generation effect validation
Parameter
Value
Generator input size

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Generator hidden layer
[256, 512, 1024]
Discriminator hidden layer
[1024, 512]
Activation function
LeakyReLU
Optimizer
RMSprop
Fifth, through indicators such as audio feature extraction accuracy and video analysis accuracy,
the comprehensive evaluation effect of the proposed model and baseline models is compared. The
explanation of the indicators selected in the study is depicted in Table 8: Table 8: An explanation of the relevant indicators for comparing the comprehensive
evaluation effects of the proposed model and baseline models
Names of indicators
Explanation of meaning
Audio feature extraction
accuracy (%)
The accuracy of acoustic feature recognition by the system during the
audio processing phase
Video analysis accuracy
(%)
The accuracy of expression and action recognition by the system in
video frames
Multimodal fusion
accuracy (%)
The system's overall discriminative accuracy after integrating audio,
video, and text features
Sentiment classification
accuracy (%)
The accuracy of the system in recognizing students' emotional states
Real-time feedback
accuracy (%)
The system's consistency in providing immediate teaching feedback
with standard results
Teaching guidance
improvement (%)
The improvement rate in learning progress and teaching effectiveness
after system optimization
Overall system
efficiency (%)
The system's comprehensive efficiency in completing
recommendations, generation, and feedback within a unit of time
4.4 Performance Evaluation
4.4.1 Robustness test analysis
The robustness analysis results of the complete training epoch-based vocal music teaching
optimization model are presented in Figure 4:

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

0.0009
0.0010
0.0011
0.0012
0.0013
Change in learning rate
Training cycle (round)
Change in learning rate
a
-0.03
-0.02
-0.01
0.00
0.01
0.02
0.03
Growth rate of data noise level (%)
Growth rate of data noise level (%)

Batch size change (sample size)
Training cycle (round)
Batch size change (sample size)
b

Model convergence speed (s)
Model convergence error ratio (%)
Parameter sensitivity (%)
Other indicator results (line legend)
Figure 4: Robustness analysis of the vocal music teaching optimization model by the
complete training epoch ((a): Results of changes in learning rate and data noise level; (b): Results
of model convergence and sensitivity)
Figure 4 denotes that within 100 training epochs, the learning rate varies between 0.0009 and
0.0013, batch sizes range from 118 to 148 samples, and data noise level changes are between -0.03%
and 0.03%. Moreover, model convergence speeds are between 9.88 seconds and 10.3 seconds,
convergence errors are between 5.2% and 6.9%, and parameter sensitivity ranges from 4% to 7%.
4.4.2 The personalized recommendation effect analysis
The analysis results of the personalized recommendation effect of the vocal music teaching
optimization model based on six datasets are revealed in Figure 5:

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

LibriSpeech YouTube-8M
Common
Voice
AVSpeech
TED-LIUM
VoxCeleb
0.65
0.70
0.75
0.80
0.85
0.90
Personalized recommendation index calculation value
Data Source
Precision
Recall
F1-Score
MAE
RMSE
Coverage
Diversity
Figure 5: The personalized recommendation effect analysis of the vocal music teaching
optimization model based on six datasets
In Figure 5, based on the LibriSpeech data source, the recommendation model achieves
outstanding performance with Precision and Recall reaching 0.85 each. The Common Voice data
source excels in F1-Score and Coverage, at 0.76 and 0.85, respectively. The TED-LIUM data source
performs well in MAE and Diversity, scoring 0.70 and 0.79.
4.4.3 Analysis of teaching strategy optimization effect
The analysis results of the teaching strategy optimization effect of the six datasets-based vocal
music teaching optimization model are illustrated in Figure 6: LibriSpeech YouTube-8M
Common
Voice
AVSpeech
TED-LIUM
VoxCeleb

Calculation value of teaching strategy indicators
Data Source
Cumulative Reward
Learning Curve Slope
Convergence Time (s)
Policy Stability (%)
Adaptability (%)
Student Engagement (%)
Improvement Rate (%)
Figure 6: Analysis of the teaching strategy optimization effect of the vocal music teaching
optimization model based on six datasets
Figure 6 displays that, based on the LibriSpeech data source, the recommendation model
exhibits excellent performance with Policy Stability at 97.24% and Adaptability at 99.46%. The
Common Voice data source performs exceptionally well with Cumulative Reward at 99.51% and

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Convergence Time at 100.41 seconds. The TED-LIUM data source shows strong performance in
Student Engagement at 88.97% and Improvement Rate at 87.63%.
4.4.4 Analysis of the resource generation effect
The analysis results of the resource generation effect of the vocal music teaching optimization
model based on six datasets are indicated in Figure 7: LibriSpeech YouTube-8M
Common
Voice
AVSpeech
TED-LIUM
VoxCeleb

Calculation value of teaching strategy indicators
Data Source
Quality Score
Realism Score
Variety Score
User Satisfaction (%)
Engagement Rate (%)
Resource Utilization (%)
Improvement Rate (%)
Figure 7: Analysis of the resource generation effect of the vocal music teaching optimization
model using six datasets
Figure 7 underscores that the Common Voice d demonstrates significant advantages in Quality
Score at 97.91% and User Satisfaction at 95.20%, indicating its superior quality of generated
resources and user satisfaction. The TED-LIUM shows strong performance in Engagement Rate
and Improvement Rate at 97.60% and 91.54%, indicating its potential to enhance student
engagement and learning improvement. The VoxCeleb exhibits competitive scores in Realism Score
at 93.14% and Variety Score at 90.72%, showcasing its strength in realism and diversity of generated
resources. The LibriSpeech displays balanced performance across all indicators, including Resource
Utilization at 89.25% and Improvement Rate at 88.15%, reflecting its stability and reliability in
resource utilization efficiency and teaching effectiveness.
4.4.5 Comprehensive evaluation effect analysis
Figure 8 presents the comprehensive evaluation effect results of the vocal music teaching
optimization model based on six datasets:

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

LibriSpeech
YouTube-8M
Common
Voice
AVSpeech
TED-LIUM
VoxCeleb

Integration effectiveness and feedback effectiveness score (1-10)
Data Source
Real-time Feedback Effectiveness (1-10)
Multimodal Fusion Effectiveness (1-10)
LibriSpeech
YouTube-8M
Common
Voice
AVSpeech
TED-LIUM
VoxCeleb

Sentiment Classification Accuracy (%)
Sentiment Classification Accuracy (%)
Data Source
Figure 8: The comprehensive evaluation effect results of the vocal music teaching
optimization model using six datasets
Figure 8 reveals that VoxCeleb performs best in real-time feedback effectiveness at 9.718 and
sentiment classification accuracy at 94.98%, demonstrating its superiority in handling multimodal
data. The Common Voice also shows impressive results in sentiment classification accuracy
(91.42%) and real-time feedback effectiveness (9.131). LibriSpeech has a real-time feedback
effectiveness of 9.715, indicating its efficiency in providing immediate teaching feedback. In
contrast, AVSpeech performs weaker across all indicators, with a sentiment classification accuracy
of only 73.19%. These results indicate that different data sources significantly influence the model's
comprehensive evaluation effects. Particularly, these findings demonstrate the remarkable
advantages of VoxCeleb and Common Voice in enhancing model performance and timely teaching
feedback. Figure 9 shows the comparative analysis of the comprehensive evaluation effects based on the
proposed vocal music teaching optimization model and baseline models: Audio Feature
Extraction
Accuracy (%)
Video Analysis
Accuracy (%)
Multimodal Fusion
Accuracy (%)
Sentiment
Classification
Accuracy (%)

Different model values
Metric
Baseline Model
Article Model
a

Improvement (%)
Standard Deviation
Improvement changes and standard deviations
0.020
0.022
0.024
0.026
0.028
0.030
0.032
p-value
p-value

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Real-time Feedback
Accuracy (%)
Teaching Guidance
Improvement (%)
Overall System
Efficiency (%)

Different model values
Metric
Baseline Model
Article Model

Improvement (%)
Standard Deviation
Improvement changes and standard deviations
b
0.010
0.012
0.014
0.016
0.018
0.020
0.022
0.024
p-value
p-value
Figure 9: Comparative analysis of the comprehensive evaluation effects of the proposed
model and baseline models ((a): Comparative analysis of model performance indicators; (b): Comparative analysis of model teaching effect indicators)
In Figure 9, the vocal music teaching optimization model shows substantial differences
compared with baseline models in multiple indicators. First, the audio feature extraction accuracy
increases from 85.99% to 94.34%, with an improvement of 8.35%, and the p-value is 0.032, which
is statistically significant. The video analysis accuracy rises from 83.09% to 92.55%, an increase of
9.46%, and the p-value is 0.021, which proves the improved model's effectiveness. The multimodal
fusion accuracy rises from 88.26% to 98.02%, an improvement of 9.76%, and the p-value is 0.028,
showing the effect of multimodal fusion technology. The sentiment classification accuracy increases
from 84.75% to 98.99%, a rise of 14.24%, and the p-value is 0.026, indicating the BERT model's
remarkable improvement. Regarding real-time feedback accuracy, it adds from 90.05% to 95.71%,
an improvement of 5.66%, and the p-value is 0.020, showing a notable improvement. The teaching
guidance improvement rate and overall system efficiency rise from 87.34% and 89.12% to 97.45%
and 98.07% respectively, with increases of 10.11% and 8.95%, and the p-values are 0.019 and 0.022. The above results show that the optimized improved model has prominent advantages in multimodal
data processing, SA, and real-time feedback, which enhances teaching effects and system efficiency.
4.4.5 Generated resources and multi-dimensional SA
To further verify the application value of the proposed model in vocal music teaching scenarios,
this study conducts extended experiments from two aspects. 1. It compares the role of traditional
resources and GAN-generated resources in teaching optimization. 2. It expands the dimension of
SA, extending from single positive-negative sentiment classification to multi-category and intensity
recognition, and conducting systematic evaluation combined with a confusion matrix. In the resource value evaluation, the experiment builds a "traditional resource group" and a
"generated resource group" based on six public datasets: LibriSpeech, YouTube-8M, Common
Voice, AVSpeech, TED-LIUM, and VoxCeleb. The traditional resource group only uses original
samples, while the generated resource group introduces GAN-generated extended materials on this
basis. Both groups of experiments were run under the same conditions. Comparisons are made

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

through indicators such as recommendation accuracy (F1-score), strategy stability, fusion accuracy,
and system efficiency. Table 9 shows the results: Table 9: The results of the comparative experiment between the generated and traditional
resources
Resource type
Recommendation
accuracy (F1)
Strategy
stability (%)
Fusion
accuracy (%)
System
efficiency (%)
Traditional resources
0.81
89.72
92.36
90.58
Generated resources
0.88
97.24
98.02
98.07
In Table 9, all indicators improve after the introduction of generated resources. Among them,
the recommendation accuracy increases by 0.07, and the strategy stability rises by 7.52 percentage
points. This indicates that GAN plays an important role in alleviating data sparsity and enriching
teaching materials. Further observation shows that the improvement ranges of fusion accuracy and
system efficiency are close to 8 percentage points. This demonstrates that generated resources
expand data coverage and improve the effect of cross-modal feature alignment, making the model
more robust when processing complex inputs. Such improvements mean that in practical teaching
applications, students can obtain more continuous and diverse learning experiences. At the same
time, learning bottlenecks caused by insufficient resources are reduced. In the SA extension experiment, emotional categories are divided into four types: happiness,
sadness, passion, and calmness. Multimodal features of audio, video, and text are used for
classification and intensity recognition. The results are plotted in Table 10: Table 10: Confusion matrix of multi-dimensional emotion classification (%)
Actual category
Prediction: Happiness
Prediction: Sadness
Prediction: Passion
Prediction: Calmness
Happiness
95.12
2.34
1.25
1.29
Sadness
3.11
93.47
2.02
1.4
Passion
2.26
1.85
94.08
1.81
Calmness
1.72
2.43
1.89
93.96
Table 10 reveals that the ML/SA model achieves high accuracy in recognizing all types of
emotions, and performs particularly well in the "happiness" and "sadness" categories. Although
there is a certain degree of confusion in the "passion" category, the overall accuracy still reaches
98.99%. This indicates that the model can effectively distinguish the main emotional types in vocal
music singing. It further shows that there is a close connection between emotion recognition results
and artistic expression evaluation, providing solid data support for emotional feedback in the
teaching process. To sum up, the extension experiments show that generated resources improve the performance
of recommendation and teaching optimization. Generated resources also enable the model to capture
more fine-grained emotional categories and intensities in multimodal emotion recognition, closely

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

related to artistic expression. This result further proves the proposed model's teaching value and art
education adaptability in vocal music teaching, offering a verifiable implementation path for
interdisciplinary integration under the STEAM concept.
4.5 Discussion
Among existing cutting-edge methods, the MusicARLtrans Net model proposed by Chang et
al. in 2024 mainly realized real-time feedback through speech-to-text and RL. The KNIGHT
framework proposed by Sharif and Uckelmann in 2024 emphasized multimodal data and privacy
protection. The DPN-GAN proposed by Ahmad et al. in 2025 focused on improving the fidelity of
audio generation. Although these studies have made breakthroughs in interaction, analysis, or
resource generation, they generally target a single task or local optimization. In contrast, the
proposed model is not a simple juxtaposition of NCF, DQN, and GAN. Instead, guided by the
inherent STEAM concept, it deeply integrates science, technology, engineering, arts, and
mathematics. From the perspective of science and learning, the model defines learning status
through quantitative indicators of intonation, rhythm, timbre, and emotion, converting the
traditional experience-dependent evaluation into observable data. Regarding mathematical
principles, the unified embedding space enables the comparison and calculation of features from
different modalities, thus transcribing subjective artistic aesthetics into an optimizable objective
function. At the technical and engineering level, the model forms a closed loop of generation,
recommendation, and strategy optimization: GAN generates targeted vocal music segments; NCF
realizes personalized ranking between real and generated resources; DQN dynamically balances
accuracy, stability, and participation through reward shaping. At the artistic and educational level,
the system trains skills and attaches importance to emotional expression and style presentation; this
ensures that learners gain a complete music experience in practice. This interdisciplinary design
allows students to understand sound in scientific analysis, receive interventions in engineering
systems, experience reasoning in mathematical modeling, and realize expression in artistic creation,
reflecting a true STEAM learning path. The innovation of this study lies in connecting
recommendations and strategies through measurable states and controllable generation. This allows
artistic evaluation to be based on verifiable computational representations rather than a simple stack
of single technologies. Combined with the study's analysis results, it can be found that the proposed system performs
well at the numerical level and has clear significance in teaching practice. The strategy stability is
improved to 97.24%, which means the system can maintain sensitivity and consistency to students'
states during long-term operation. As a result, teachers can reduce repeated trials and frequent
adjustments and focus on guiding artistic expression. The cumulative reward reaches 90.23,
indicating that students' performance in multiple dimensions, such as intonation, rhythm, timbre,
and emotion, has achieved continuous improvement. This provides learners with a more traceable
and verifiable growth path. In other words, the experimental indicators do not reflect abstract
computational advantages but correspond to continuous progress and reduced intervention burden
in real teaching. This highlights the system's value in providing two-way support for teachers and
students. From the perspective of real application scenarios, the model may face some challenges during
actual deployment. First, complex multimodal computing imposes high requirements on computing
power. In environments with limited resources, this may cause delays and affect the experience of
real-time feedback. Second, the collection and annotation of cross-modal data require high costs,

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

which may restrict the model's promotion in different schools or educational stages. Third, the
model has great differences in adaptability between K-12 education and professional music colleges;
the former requires more lightweight and universal approaches, while the latter emphasizes
precision and personalization. Future research can enhance scalability through model compression,
delay optimization, and cross-scenario transfer. This study also suggests that generative AI should
be combined with domain prior knowledge and educational rules to avoid instability caused by
completely free generation. By embedding constraints such as rhythm, vocal range, or textbook
boundaries, the model can achieve output that is reliable and creative. Thus, it can truly balance
innovation and practicality in educational environments.

### 5 Conclusion

5.1 Research Contribution
The related research in Section 2 indicates that existing STEAM education models (e.g., Zhang,
2025; Sharif and Uckelmann, 2024) mainly focus on interdisciplinary knowledge integration and
creative thinking cultivation. They promote the integration of art and science at the level of teaching
concepts, but are still insufficient in terms of intelligent optimization and dynamic feedback
mechanisms at the algorithm level. In addition, studies in the field of recommendation systems (e.g., Prabhakar and Lee, 2023; Chango et al., 2022; Oroojlooyjadid et al., 2022) have made remarkable
progress in personalized resource matching and learning behavior modeling. However, they
generally ignore the complexity of emotional expression, multimodal interaction, and aesthetic
experience in art education. Most existing achievements concentrate on task performance
optimization, while lacking the systematic integration of human-computer collaboration and
emotional feedback in educational scenarios. In contrast, this study proposes a vocal music teaching optimization model based on ML and
SA by integrating the STEAM concept into the intelligent recommendation system. Experimental
results show that this model is markedly superior to existing methods in recommendation accuracy,
teaching strategy optimization, resource generation, and real-time feedback. Meanwhile, this model
provides a reference solution for the personalization and intellectualization of vocal music education. The proposed intelligent recommendation-based vocal music teaching optimization framework,
driven by the STEAM concept, deeply couples educational concepts, affective computing, and ML. It realizes the dynamic linkage of teaching strategy optimization, resource generation, and emotional
feedback. Moreover, it makes up for the disconnection between "educational concepts-algorithm
models-teaching practice" in existing studies and reflects innovative value at the methodological
and application levels. In practical teaching application scenarios, the deployment and promotion of this system need
to fully consider the differentiated conditions of educational platform ecology and hardware
environment. In real vocal music teaching, different colleges and online education platforms have
diverse infrastructure and data interface standards. When connecting with existing Learning
Management Systems (LMS) or Content Management Systems (CMS), the system needs to achieve
multi-protocol compatibility and interface adaptation to ensure the seamless integration of
recommendation and feedback modules. In addition, in teaching environments with limited
resources or low network bandwidth, the computational load of real-time multimodal feedback may
cause delays, thereby affecting the consistency and interactivity of the teaching experience. Therefore, during actual deployment, the model can combine edge computing or cloud collaboration
strategies and reduce computational delay through local caching and distributed reasoning. At the

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

same time, regarding the usage differences between teachers and students, the system should
provide a visual feedback dashboard and a simplified mobile push mechanism to support flexible
interaction and real-time feedback in different teaching scenarios, thereby achieving in-depth
integration of technological innovation and teaching practice.
5.2 Future Works and Research Limitations
It should be noted that the results of this study should be regarded as a preliminary exploration. On the one hand, although the experimental data support the model's effectiveness, further
verification is still needed in larger-scale and more diverse educational scenarios. On the other hand,
the current model still relies on complex deep structures for real-time alignment of multimodal
features and cross-modal semantic consistency, resulting in high computational overhead. It is
necessary to consider further improving the model's computational efficiency and response speed
while maintaining its performance. Thus, it has greater feasibility and stability in subsequent
deployment in large-scale real-time teaching scenarios. In other words, this study mainly offers a
feasible technical framework and research direction, rather than a fully mature conclusion. Future research can optimize multimodal data fusion technology to improve the model's
robustness and adaptability when dealing with extreme data and long-tail user behaviors. At the
same time, future research can combine lightweight multimodal architecture with adaptive
constraint mechanisms to enhance the model's generalization ability and interpretability. It can also
explore the application of explainable artificial intelligence methods in teaching feedback and
human-computer collaboration, to realize a more efficient, transparent, and scalable intelligent vocal
music teaching system. Funding: This research received no external funding. Data Availability Statement
The datasets used and/or analysed during the current study available from the corresponding author
Qianping Guo on reasonable request via e-mail 15340524767@163.com. Competing Interest
The authors declare no competing financial or non-financial interests. Author Statement
Fanbo Su: Conceptualization, methodology, software, validation, formal analysis, investigation, resources,
data curation, writing—original draft preparation
Qianping Guo: writing—review and editing, visualization, supervision, project administration, funding
acquisition

## ETHICS STATEMENT

The studies involving human participants were reviewed and approved by College of Music, Chongqing
Normal University Ethics Committee (Approval Number: 2022.25641000). The participants provided their
written informed consent to participate in this study. All methods were performed in accordance with
relevant guidelines and regulations.

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

References
[1] Jena K K, Bhoi S K, Mallick C, et al. Neural model based collaborative filtering for movie
recommendation system. International Journal of Information Technology, 2022, 14(4): 2067-
2077.
[2] Rehman I, Hanif M S, Ali Z, et al. Empowering neural collaborative filtering with contextual
features for multimedia recommendation. Multimedia Systems, 2023, 29(4): 2375-2388.
[3] Morise H, Atarashi K, Oyama S, et al. Neural collaborative filtering with multicriteria
evaluation data. Applied Soft Computing, 2022, 119(22): 108548.
[4] Song G J, Song H S. Algorithm for generating negative cases for collaborative filtering
recommender. Expert Systems, 2022, 39(7): e12986.
[5] Do P M T, Nguyen T T S. Semantic-enhanced neural collaborative filtering models in
recommender systems. Knowledge-Based Systems, 2022, 257(13): 109934.
[6] Magron P, Févotte C. Neural content-aware collaborative filtering for cold-start music
recommendation. Data Mining and Knowledge Discovery, 2022, 36(5): 1971-2005.
[7] Jena K K, Bhoi S K, Malik T K, et al. E-learning course recommender system using
collaborative filtering models. Electronics, 2022, 12(1): 157.
[8] Chang J, Wang Z, Yan C. MusicARLtrans Net: a multimodal agent interactive music education
system driven via reinforcement learning. Frontiers in Neurorobotics, 2024, 18: 1479694.
[9] Sharif M, Uckelmann D. Multi-Modal LA in Personalized Education Using Deep
Reinforcement Learning Based Approach. IEEE Access, 2024, 12: 54049-54065.
[10] Govea J, Navarro A M, Sánchez-Viteri S, et al. Implementation of deep reinforcement learning
models for emotion detection and personalization of learning in hybrid educational
environments. Frontiers in Artificial Intelligence, 2024, 7: 1458230.
[11] Zaman K, Zengkang G, Zhaoyun S, et al. A Novel Emotion Recognition System for Human–
Robot Interaction (HRI) Using Deep Ensemble Classification. International Journal of
Intelligent Systems, 2025, 2025(1): 6611276.
[12] Zhang Z. The Teaching Method of STEAM Education-based Audio-visual Aesthetics in
College Vocal Music Teaching. Frontiers in Educational Research, 2025, 8(2).
[13] Daneshfar F, Soleymanbaigi S, Yamini P, et al. A survey on semi-supervised graph clustering. Engineering Applications of Artificial Intelligence, 2024, 133: 108215.
[14] Keshun Y, Zengwei L, Yingkui G. A performance-interpretable intelligent fusion of sound and
vibration signals for bearing fault diagnosis via dynamic CAME[J]. Nonlinear Dynamics, 2024,
112(23): 20903-20940.
[15] Keshun Y, Yingkui G, Yanghui L, et al. A novel physical constraint-guided quadratic neural
networks for interpretable bearing fault diagnosis under zero-fault sample[J]. Nondestructive

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Testing and Evaluation, 2025: 1-31.
[16] Keshun Y, Chenlu L, Yanghui L, et al. DTMPI-DIVR: A digital twins for multi-margin physical
information via dynamic interaction of virtual and real sound-vibration signals for bearing fault
diagnosis without real fault samples[J]. Expert Systems with Applications, 2025, 292: 128592.
[17] Keshun Y, Puzhou W, Peng H, et al. A sound-vibration physical-information fusion constraint-
guided deep learning method for rolling bearing fault diagnosis[J]. Reliability Engineering &
System Safety, 2025, 253: 110556.
[18] Ahmad Z, Bao S, Chen M. DPN-GAN: Inducing Periodic Activations in Generative
Adversarial Networks for High-Fidelity Audio Synthesis. IEEE Access, 2025.
[19] Tong H, Li H, Du H, et al. Multimodal semantic communication for generative audio-driven
video conferencing. IEEE Wireless Communications Letters, 2024.
[20] Bethencourt-Aguilar A, Castellanos-Nieves D, Sosa-Alonso J J, et al. Use of generative
adversarial networks (GANs) in educational technology research. Journal of New Approaches
in Educational Research, 2023, 12(1): 153-170.
[21] Prabhakar S K, Lee S W. Holistic approaches to music genre classification using efficient
transfer and deep learning techniques. Expert Systems with Applications, 2023, 211(12):
118636.
[22] Chango W, Lara J A, Cerezo R, et al. A review on data fusion in multimodal learning analytics
and educational data mining. Wiley Interdisciplinary Reviews: Data Mining and Knowledge
Discovery, 2022, 12(4): e1458.
[23] Prottasha N J, Sami A A, Kowsher M, et al. Transfer learning for sentiment analysis using
BERT based supervised fine-tuning. Sensors, 2022, 22(11): 4157.
[24] Oroojlooyjadid A, Nazari M R, Snyder L V, et al. A deep q-network for the beer game: Deep
reinforcement learning for inventory optimization. Manufacturing & Service Operations
Management, 2022, 24(1): 285-304.
[25] Vaziri P, Ahmadi S, Daneshfar F, et al. Machine learning techniques in enhanced oil recovery
screening using semisupervised label propagation. SPE Journal, 2024, 29(09): 4557-4578.
[26] Ma D, Zhu H, Liao S, et al. Learning path recommendation with multi-behavior user modeling
and cascading deep Q networks. Knowledge-Based Systems, 2024, 294(08): 111743.
[27] Shuvo S S, Yilmaz Y. Home energy recommendation system (hers): A deep reinforcement
learning method based on residents’ feedback and activity. IEEE Transactions on Smart Grid,
2022, 13(4): 2812-2821.
[28] Gupta K D, Sadman N, Sadmanee A, et al. Behavioral recommendation engine driven by only
non-identifiable user data. Machine Learning with Applications, 2023, 11(42): 100442.

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

[29] Keat E Y, Sharef N M, Yaakob R, et al. Multiobjective deep reinforcement learning for
recommendation systems. IEEE Access, 2022, 10(38): 65011-65027.
[30] Altamimi B, Côté D, Shirmohammadi S. Toward a Superintelligent Action Recommender for
Network Operation Centers Using Reinforcement Learning. IEEE Access, 2023, 11(19):
20216-20229.
[31] Iqbal M J, Farhan M, Ullah F, et al. Intelligent multimedia content delivery in 5G/6G networks:
a reinforcement learning approach. Transactions on Emerging Telecommunications
Technologies, 2024, 35(4): e4842.
[32] Modirrousta M H, Aliyari Shoorehdeli M, Yari M, et al. Deep Q‐learning recommender
algorithm with update policy for a real steam turbine system. IET Collaborative Intelligent
Manufacturing, 2023, 5(3): e12081.
[33] Shafqat W, Byun Y C. A hybrid GAN-based approach to solve imbalanced data problem in
recommendation systems. IEEE access, 2022, 10(36): 11036-11047.
[34] Chakraborty T, KS U R, Naik S M, et al. Ten years of generative adversarial nets (GANs): a
survey of the state-of-the-art. Machine Learning: Science and Technology, 2024, 5(21): 011001.
[35] Ramdurai B, Adhithya P. The impact, advancements and applications of generative AI. International Journal of Computer Science and Engineering, 2023, 10(6): 1-8.
[36] Zaman K, Zhaoyun S, Shah B, et al. A novel driver emotion recognition system based on deep
ensemble classification. Complex & Intelligent Systems, 2023, 9(6): 6927-6952.
[37] Abdelmoumin G, Whitaker J, Rawat D B, et al. A survey on data-driven learning for intelligent
network intrusion detection systems. Electronics, 2022, 11(2): 213.
[38] Yuan C, Marion T, Moghaddam M. Dde-gan: Integrating a data-driven design evaluator into
generative adversarial networks for desirable and diverse concept generation. Journal of
Mechanical Design, 2023, 145(4): 041407.
[39] Yang Q, Yu C. [Retracted] Fusion of Emotional Thinking and Mental Health of Students in
Vocal Music Teaching. Occupational Therapy International, 2023, 46(048): 85.
[40] Park K, Ergan S, Feng C. Quality assessment of residential layout designs generated by
relational Generative Adversarial Networks (GANs). Automation in Construction, 2024,
158(26): 105243.
[41] Agrawal A, Gans J S, Goldfarb A. Artificial intelligence adoption and system‐wide change. Journal of Economics & Management Strategy, 2024, 33(2): 327-337.
[42] Arora A, Shantanu. A review on application of GANs in cybersecurity domain. IETE Technical
Review, 2022, 39(2): 433-441.
[43] Zhu Y, Wang M, Yin X, et al. Deep learning in diverse intelligent sensor based systems. Sensors,

## ARTICLE IN PRESS

## ARTICLE IN PRESS

## ARTICLE IN PRESS

2022, 23(1): 62.
[44] Gong X. Research on discrete dynamic system modeling of vocal performance teaching
platform based on big data environment. Discrete Dynamics in Nature and Society, 2022,
20(22): 5111896.
[45] Sansom R. Framing the “Vocal Traditions” Series. Voice and Speech Review, 2022, 16(2): 220-
222.

## ARTICLE IN PRESS

## ARTICLE IN PRESS
