# Innovation of entrepreneurship education in

**Year:** D:20

---

## ARTICLE IN PRESS

Article in Press
Innovation of entrepreneurship education in
auxiliary instruction system for college aesthetic
course teaching under BPNN model
Scientific Reports
Received: 15 July 2025
Accepted: 28 November 2025
Cite this article as: Xia J. Innovation of
entrepreneurship education in auxiliary
instruction system for college aesthetic
course teaching under BPNN model. Sci Rep (2025). https://doi.org/10.1038/
s41598-025-30967-6
Juan Xia
We are providing an unedited version of this manuscript to give early access to its
findings. Before final publication, the manuscript will undergo further editing. Please
note there may be errors present which affect the content, and all legal disclaimers
apply. If this paper is publishing under a Transparent Peer Review model then Peer
Review reports will publish with the final article.
https://doi.org/10.1038/s41598-025-30967-6
© The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit
to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do
not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain
permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/4.0/.

## ARTICLE IN PRESS

Innovation of Entrepreneurship Education in
Auxiliary Instruction System for College
Aesthetic Course Teaching under BPNN Model
Juan Xia1,*
1Conservatory of music, Hubei Normal University, Huangshi, 435000, China
*Correspondence Email: xiaxia0211@hbnu.edu.cn
Abstract: Music colleges in China currently face significant challenges in
innovation
and
entrepreneurship
education
(IEE),
including
inadequate
instructional support systems and fragmented teaching methods. These issues are
particularly pronounced in aesthetic education courses, where scientific
assessment and personalized guidance for students’ entrepreneurial competence
remain underdeveloped. To address this gap, this study proposes and validates an
auxiliary instructional system based on the back propagation neural network
(BPNN) model aimed at improving the precision and effectiveness of IEE within
aesthetic education. The study investigates whether the BPNN model can
accurately model and assess students’ entrepreneurial abilities to support
pedagogical optimization. Targeting graduates from music colleges in the Xi’an
region, this study constructs a competence evaluation framework comprising four
primary indicators and twelve secondary indicators, gathering 444 valid
questionnaire responses. Using this data, the BPNN model is designed and trained
to predict and provide feedback on students’ innovation and entrepreneurship
competencies. The model achieves a maximum relative error of only 1.64%
between predicted and actual outputs, demonstrating strong accuracy and
practical viability. Results highlight the theoretical and applied value of leveraging
deep learning for entrepreneurial competence assessment in the integration of
arts education and IEE. However, the current evaluation framework requires
further refinement to better meet the evolving demands of specialization and
industrialization. Keywords: Innovation
and
entrepreneurship
education
(IEE); Auxiliary
instruction system; Back propagation neural network (BPNN); Music students; College aesthetic course

### 1. Introduction

In recent years, Artificial Intelligence (AI) and deep learning technologies have
created new opportunities for the transformation of higher education, driving a
shift from traditional teaching models toward intelligent systems. In response to
China’s “Mass Entrepreneurship and Innovation” policy, universities have
introduced abundant entrepreneurial resources and platforms. However, existing
innovation and entrepreneurship education (IEE) systems remain primarily
focused on science and engineering disciplines. As a result, students in the arts—
particularly those majoring in music—face a gap in entrepreneurship training. These students need solid professional knowledge and enhanced creativity,
interdisciplinary integration, and market adaptability [1, 2]. The application of AI
in personalized instruction, precise assessment, and dynamic curriculum
adjustment has become a central topic in educational research. Although AI-
assisted learning systems have demonstrated strong potential in personalized
learning and skill assessment, existing research remains largely focused on STEM
and language education. Studies exploring how AI can support the development
of entrepreneurial competence in the arts are still relatively limited. To address this gap, this study proposes an AI-assisted teaching system based
on a Back Propagation Neural Network (BPNN) to improve entrepreneurship
education outcomes for music students. The BPNN model possesses strong
nonlinear fitting capabilities, making it suitable for processing complex
educational data. When combined with Principal Component Analysis (PCA), it

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

enhances evaluation accuracy. The proposed model accounts for the diversity of
educational environments and highlights its potential for broader applications in
intelligent teaching decision-making. Although the study focuses on music
universities, the proposed method and evaluation framework can be extended to
other art education domains—especially those involving artistic creation and
interdisciplinary collaboration. By employing a data-driven teaching support
mechanism, this study provides a replicable solution for the intelligent
transformation of art education and promotes deeper integration of AI
technologies in the educational landscape.

### 2. Related Work

In recent years, the application of AI and deep learning-based instructional
support systems in IEE for music university students has garnered growing
academic interest [3, 4]. For instance, Yang (2020) explored the integration of AI
in music education, focusing on areas such as automatic music composition, music
theory instruction, and music technology applications, while also addressing its
future potential in educational contexts [5]. Zhang et al. (2022) proposed a deep
learning-based model for music composition instruction that analyzed student
works, automatically evaluated composition quality, and provided targeted
instructional feedback [6]. Similarly, Ma et al. (2021) examined various AI
applications in music education, including AI-assisted teaching tools and
automated music generation, and discussed their future development directions
[7]. In the field of entrepreneurship education, Sari and Yuliawan (2020)
developed an AI-based system that delivered personalized entrepreneurship
training and assessment to students [8]. Despite these advancements, current
research in both music composition instruction and entrepreneurship education
continues to present several notable limitations. First, most existing studies have
primarily focused on automatic music generation or basic educational support
functions, lacking the integration of advanced deep learning algorithms
specifically designed to support both music composition and entrepreneurship
education. Although these efforts have broadened the scope of AI applications in
music education, they have fallen short in addressing how deep learning can be
leveraged for personalized guidance and formative assessment throughout the
creative process. Second, many AI-assisted instructional systems remain at the
theoretical or prototype stage, with limited empirical validation of their
effectiveness and adaptability in real-world teaching environments. Specifically,
the application of such systems in the context of entrepreneurship education
within music institutions has not yet been comprehensively verified. Therefore,
although existing research provides a valuable foundation, several critical
challenges remain unresolved. Chief among these is how to effectively integrate
AI and deep learning algorithms into a system that supports music composition
and fosters entrepreneurial competence. Developing such a system with
demonstrable instructional value and scalability represents a significant research
gap that this study aims to address. Despite continued progress in the application of AI technologies in music
education—particularly in areas such as automated music generation and
instructional tools—significant gaps persist in integrating music composition
education with entrepreneurship training. Most existing studies focus on isolated
components of instruction and rarely address how musical creativity can be
effectively aligned with entrepreneurial practice. Within university-level IEE
frameworks, music students encounter challenges that extend beyond creative
expression, including the transformation of artistic output into marketable
products, the development of market-oriented thinking, and the construction of
viable business models. Current research lacks AI-driven instructional systems
based on deep learning that can simultaneously provide personalized guidance
during the music composition process and assess the practical translation of
creative skills into entrepreneurial outcomes. Moreover, most AI-assisted
instructional systems remain at the conceptual or prototype stage, with limited

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

empirical evidence supporting their effectiveness and adaptability in real-world
educational settings. In particular, the integration of technological tools into
entrepreneurship education at art-focused institutions remains insufficiently
developed. The use of such tools to enhance student competence in music creation,
brand development, and business decision-making has yet to be thoroughly
explored. This underscores an urgent need to develop intelligent instructional
systems that integrate artistic expression with entrepreneurial practice, offering
dynamic support for the creative process while fostering scientifically grounded
entrepreneurial competence. Among various deep learning algorithms, the BPNN demonstrates particular
value in bridging music and entrepreneurship education. With its powerful
nonlinear modeling capabilities, BPNN enables precise analysis of individual traits
expressed during the creative process and maps them to key dimensions of
entrepreneurial competence—such as innovative thinking, project execution, and
market awareness. BPNN technology supports feedback regulation based on
students’ creative output and behavioral data, allowing instructors to develop
targeted instructional interventions. It also provides a scientific basis for
evaluating student performance in applied settings such as music intellectual
property incubation, project presentations, and entrepreneurship competitions. Therefore, constructing an AI-assisted instructional support system based on
BPNN offers a promising approach to linking music composition with
entrepreneurship education, enhancing students’ comprehensive competence and
practical application skills.

### 3. IEE-oriented Evaluation Index System based on BPNN

## 3.1 IEE

IEE is an educational model designed to cultivate students’ innovative
awareness, entrepreneurial competence, and comprehensive capabilities. It
emphasizes the integration of theoretical knowledge and practical application,
while promoting individual development and creative potential [9]. In music-
focused higher education institutions, IEE extends beyond the transmission of
professional knowledge to the holistic development of students’ abilities in artistic
creation, project planning, market orientation, and entrepreneurial practice [10,
11]. Integrating IEE into aesthetic education courses facilitates a more effective
alignment between artistic training and innovation development. For instance,
project-based instruction can guide students in planning and presenting original
music works; data analytics and intelligent systems can support multidimensional
assessments
of
the
creative
process
and
performance;
and
simulated
entrepreneurship
platforms
can
enable
students
to
understand
the
commercialization pathways of musical products. These methods help foster
student initiative and enhance problem-solving abilities. Furthermore, IEE
systems can be embedded into AI-assisted instructional platforms to provide
personalized learning recommendations and dynamic competence assessments. Such integration helps guide students to continuously refine their creative
thinking and entrepreneurial strategies, while improving their practical skills and
adaptability [12]. As a result, IEE introduces new directions for art education and
provides both technical infrastructure and theoretical support for improving the
quality of entrepreneurship education in higher education [13]. Fig. 1 illustrates the relationship between professional education and the IEE
framework.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Fig. 1 The relationship between IEE and professional education
The distinction between IEE and traditional professional education can be
understood through several core features:
(1) Integration, which incorporates diverse social, industrial, and practical
elements into higher education, forming a cohesive system that evolves with
societal progress.
(2) Timeliness, as IEE aligns with current social and economic trends, enabling
graduates who receive entrepreneurship training alongside professional
education to access enhanced career opportunities.
(3) Transformational impact, where the skills fostered through IEE—such as
creativity, initiative, and risk tolerance—contribute not only to professional
development but also to personal growth, exceeding the scope of conventional
disciplinary training [14–16]. BPNN is a widely used type of artificial neural network that operates by
iteratively adjusting network weights and thresholds through the backpropagation
algorithm. This process enables the network to optimize its internal parameters
and achieve accurate classification or prediction results. In the context of
educational support systems, BPNN has been effectively applied to personalized
instruction and the assessment of students’ learning performance. Within music
composition education, BPNN can be used to classify and evaluate students’
creative outputs, thereby offering targeted instructional recommendations [17]. In
entrepreneurship education, BPNN can analyze students’ entrepreneurial
competence and potential, support individualized entrepreneurship training, and
perform adaptive evaluations. By continuously updating its parameters based on
feedback, the model contributes to improved instructional effectiveness. As a
result, BPNN plays a critical role in enhancing the precision and adaptability of
AI-assisted instructional systems. It enables educators to gain deeper insights into
students’ learning behaviors and instructional needs, ultimately supporting the
delivery of personalized educational services. When implementing AI- and deep
learning-based support systems in music entrepreneurship education, the
integration of BPNN with IEE frameworks significantly enhances system
intelligence and instructional effectiveness. This approach also provides a
pathway for the innovation and development of entrepreneurship education
practices in art-focused academic contexts [18–20].
3.2 Research and Analysis of the BPNN Model
A BPNN consists of multiple layers of neurons, including one or more hidden
layers positioned between the input and output layers. Although neurons within
the hidden layers do not directly interact with the external environment, changes
in their activation states significantly influence the relationship between inputs
and outputs [21]. Each layer may contain numerous nodes, and the overall
structure is designed to accommodate complex computational processes. Since its
initial development in 1986, BPNN has undergone continuous improvements in
both theoretical foundations and performance. Its primary advantages include a
strong nonlinear mapping capability and a highly flexible network architecture. Drawing on the characteristics and principles of mathematical functions, BPNN is

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

capable of learning from complex data samples and is particularly effective in
modeling nonlinear relationships [22–24]. The network's adaptive, self-organizing,
and self-learning features enable it to conduct scientific analyses of complex
problems and to identify efficient strategies for solving them [25, 26]. The
topological structure of the BPNN model is illustrated in Fig. 2. Input
layer
Hidden
layer
Output
layer
Data
input
Vector
output
Fig. 2 Topology of the BPNN model
The BPNN architecture comprises an input layer, one or more hidden layers,
and an output layer. Neurons within the same layer are not interconnected;
connections are only established between adjacent layers. The network is capable
of generating diverse outputs based on varying inputs, thereby satisfying the
requirements of the training dataset [27–29]. Let the input vector be defined as
x = (x1,x2,…⋯,xi,⋯⋯,xn)T, the output vector of the hidden layer as y =
(y1,y2,……yi,⋯⋯⋅ym)T, and the output vector of the output layer as O =
(O1, O2,……, Ok,……, Ol)T. The weight matrix between the input and hidden layers is
v = (v1,v2,……vk,⋯⋯⋅vm)T,and the weight matrix between the hidden and output
layers is w = (w1,w2,……wj,⋯⋯⋅wl)T. The output of the output layer is defined
as Eq. (1): Ok = f(∑m
j=0  wjkyj) k = 1,2,……,n
(1)
The hidden layer activation is defined as Eq. (2):
yj = f(∑m
i=0  jvijxi) j = 1,2,……,m
(2)
In general, the activation function applied between the hidden and output
layers is the sigmoid function, which has two common variants: the log-sigmoid
function and the tan-sigmoid function [30]. These are defined respectively as Eq.
(3):
f(x) =

1+e-x
(3)
f(x) = 1-e-x
1+e-x
(4)
The sigmoid function is the most frequently used activation function in BPNN. It compresses the output of the previous layer into a bounded range, thereby
enabling the network to realize nonlinear mappings from input to output. This
property is essential for solving complex classification and regression tasks in
educational systems [31–33]. Compared with other machine learning models, the BPNN demonstrates
distinct advantages in handling nonlinear, multidimensional, and fuzzy-boundary
educational evaluation data. First, BPNN can capture complex interactions among
students’ ability indicators through its multilayer neural structure. This capability
is particularly important in music-related courses, where entrepreneurial
competence is closely linked to aesthetic literacy, originality, and interdisciplinary
collaboration. These traits are often highly nonlinear and subjective in nature. Second, BPNN possesses adaptive learning capabilities. It continuously optimizes
its parameters through backpropagation, allowing it to adjust to the unique
characteristics of individual students. Compared with models such as Support
Vector Machines (SVM) and Random Forests, BPNN offers greater flexibility in
processing continuous output variables (e.g., ability scores). It also better
accommodates variations in feature dimensions and importance, thereby

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

enhancing the model’s generalization ability and stability.
3.3 BPNN Training and Optimization Process
The training of a BPNN involves a systematic algorithmic approach designed
to iteratively optimize the weights and thresholds of the network to improve
classification or prediction performance. The detailed training process consists of
the following steps: Step 1: Initialization of variables and parameters. Let
the
input
vector
be
defined
as
xk = [xk1,xk2,……,xkm],
where
k = 1,2,3,……n, and n represents the total number of training samples. After n
iterations, the weight matrices connecting various network layers are denoted as
follows: The weight matrix between the input layer M and the first hidden layer I is
given by Eq. (5):
wMI(n) = [
w11(n)
w12(n)..
w1I(n)
w21(n)
w22(n)..
w2I(n)::::
wM1(n)
wM2(n)..
wMI(n)]
(5)
The weight matrix between hidden layers I and J is:
wIJ(n) = [
w11(n)
w12(n)..
w1J(n)
w21(n)
w22(n)..
w2J(n)::::
wI1(n)
wI2(n)..
wIJ(n)]
(6)
The weight matrix between the hidden layer J and the output layer P is:
wJP(n) = [
w11(n)
w12(n)..
w1P(n)
w21(n)
w22(n)..
w2P(n)::::
wJ1(n)
wJ2(n)..
wJP(n)]
(7)
The
predicted
output
after
the
n-th
iteration
is
yk(n) =
[yk1(n),yk2(n),……,ykn(n)], and the expected output is dk = [dk1dk2,……,dk3],
where k = 1,2,3……n. These values are derived from the labeled dataset used for
model training. Step 2: Network initialization. The weights wMI(n), wIJ(n), and wJP(n) are initialized with non-zero random
values, and the iteration counter is set to n = 0. This step ensures that the model
has the capacity to learn and begin the iterative optimization process. Step 3: Sample input. Each training sample xk. is input into the network. The dimensionality of the
sample vector corresponds to the number of neurons in the input layer, serving as
the foundation for pattern recognition and weight adjustments during training. Step 4: Forward propagation. The relationship between hidden and output layers is calculated as Eq. (8): Vp(np) = ykp(n), p = 1,2,……p
(8)
Step 5: Error computation. The output error E(n) is calculated based on the difference between dk and yk
(n). If the error meets the predefined threshold, the training proceeds to Step 8. Otherwise, the process continues to Step 6. Step 6: Backpropagation. This step is the core of the learning process. The network compares the
current error with the previous iteration [34]. If the error increases, training
terminates; otherwise, the neuron’s local gradient δ is calculated as Eq. (9):
δ
p
p(n) = y(n)
p (1 - y(n)
p )(d(n)
p
- y(n)
p )
(9)
Step 7: Weight Update. Weights are adjusted based on the gradients and learning rate η. The update

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

formulas incorporate a momentum term to prevent oscillations and improve
convergence stability:
{
Δwjp(n) = ηδP
p(n)νJ
j(n),j = 1,2,3……J
wjp(n + 1) = Wjp(n) + Δwjp(n),p = 1,2,……p
ΔWij(n) = ηδJ
j(n)VI
i(n),i = 1,2,……I
wij(n + 1) = wij(n) + Δwij(n),j = 1,2,3……J
(10)
Step 8: Training Completion Check. If all samples have been processed and error convergence criteria are met,
training ends. Otherwise, return to Step 3. Despite its effectiveness, BPNN presents several limitations:
(1) Slow convergence of the total error during training [35].
(2) Prone to local minima, which can hinder global optimization [36].
(3) Catastrophic forgetting, where new data learning causes loss of previously
learned patterns [37]. To address these issues, several optimization strategies are implemented:
(1) Momentum Term Introduction: A momentum coefficient: The learning rate α is added to improve convergence
behavior:
Δwij(n) = αΔwij(n - 1) + ηδj(n)Vi(n)
(11)
Eq. (11) generalizes to:
ΔWij(n) = η∑n
t=0 an-tδj(t)Vi(t)
(12)
(2) Adaptive Learning Rate: The learning rate η is dynamically adjusted to control error reduction. When
the overall error decreases after weight adjustment, a decay factor (θ < 1) is
applied so that η = θη.
(3) Modified Activation Function: To accelerate convergence, a hyperbolic tangent function is adopted:
f(u) = atanh⁡(bu) = a[
1-exp⁡(-bu)
1+exp⁡(-bu)] =
2a
1+exp⁡(-bu) -a
(13)
This study adopts a questionnaire survey (QS) approach from the perspective
of aesthetic education to identify student characteristics and needs, thereby
delivering personalized entrepreneurial education services. Empirical analysis is
used to validate research hypotheses and inform educational recommendations. Additionally, PCA is employed to extract latent factors that significantly influence
students’ acceptance of the instructional system.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Creative data
Entrepreneurship
education data
Aesthetic
education data
Data initialization
Data input
Error Calculation
and
Backpropagation
Training
optimization
Music creation
evaluation
Entrepreneurship
education
feedback
Comprehensive
ability assessment
Fig. 3 Optimized model framework for BPNN-IEE integration
The optimized model framework, illustrated in Fig. 3, integrates BPNN with
the IEE evaluation system and incorporates data from music composition and
entrepreneurial training. It enables adaptive, personalized feedback for students
by assessing their creative competence, entrepreneurial awareness, and aesthetic
literacy. This approach provides precise evaluation and targeted guidance,
thereby enhancing both music composition and entrepreneurship instruction.
3.4 Analysis and Construction of the College Music Major’s Aesthetic
Course-oriented IEE Evaluation Index System
This study selects undergraduate music majors from A Music College as the
target population. The pilot study was conducted from March 1 to March 5, 2024,
with a total of 30 senior music students participating. Expert consultations were
carried out in two rounds, on March 10 and March 17, 2024, involving three
university-level
IEE
mentors,
two
music
education
scholars,
and
one
entrepreneurship mentor. Feedback from these consultations was used to further
refine the questionnaire design. The formal questionnaire was administered from
April 1 to April 15, 2024, through both online and offline channels. A total of 473
questionnaires were distributed, and 444 valid responses were collected, yielding
an effective response rate of 93.9%. During the survey process, all respondents’
personal information was strictly protected. Participants signed informed consent
forms prior to completing the questionnaire, explicitly stating that their data
would be used solely for academic research and handled anonymously. All
questionnaire data were encrypted to prevent unauthorized access. Identifying
information, such as names and student numbers, was not linked to survey
responses, ensuring full privacy protection. All data processing and analysis were
conducted in accordance with relevant ethical research guidelines, ensuring
compliance with research ethics standards. Before training the BPNN model, the collected questionnaire data underwent
preprocessing. Quantitative data were standardized, and qualitative variables
were converted using one-hot encoding. The QS responses captured students’ self-
assessments and practical experiences in both music composition and
entrepreneurship education. These data enabled the BPNN to learn the individual
characteristics and needs of each student and to personalize instructional
strategies accordingly. For instance, if a student's responses indicated low

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

entrepreneurial awareness, the model could recommend increased exposure to
entrepreneurship-related learning materials and tailored instructional modules. The QS was administered through both online and offline channels, employing
a mixed sampling approach that combined convenience sampling and random
sampling methods. Among the 444 respondents, 143 were male (32.2%) and 301
were female (67.8%). Prior to formal deployment, a draft version of the questionnaire was developed
and reviewed by professional music educators and entrepreneurship instructors
to ensure conceptual alignment and clarity. Irrelevant or ambiguous items were
eliminated. Subsequently, the revised version was validated by subject-matter
experts in education and entrepreneurship to further refine the questionnaire’s
design. The finalized instrument includes twelve items of basic information, with
the full content presented in the appendix. Structurally, the questionnaire follows
a three-part format: an introductory statement, the main body, and a concluding
section. The introduction outlines the study’s objectives, the target participant
group, and the intended use of the data, thereby fostering understanding and
engagement. The main body is organized into three sections: (1) basic
demographic and academic information, (2) core competency assessment, and (3)
open-ended feedback. The core competency assessment is based on four primary
dimensions: foundational competence, professional competence, practical
competence, and extended competence. Each primary dimension is further divided
into three secondary indicators. The study conducted a comprehensive review of
relevant domestic and international literature, analyzing a total of 70 publications
on the integration of IEE with music education. Based on this review, 23 core
studies were selected, from which key variables related to entrepreneurial
competence were extracted. The concluding section thanks the participants and
affirms that all responses are anonymized and used solely for academic purposes
in accordance with ethical research guidelines. The questionnaire employs four
types of items: single-choice questions (for background information), graded
quantitative items (for evaluating achievements such as certifications and
competition awards), binary yes/no questions (for identifying participation in
entrepreneurial activities), and open-ended questions (for collecting suggestions
on integrating aesthetic education with entrepreneurship education). These open-
ended responses also serve as supplementary explanatory variables for
subsequent modeling. To ensure the BPNN model could effectively process the
data, a unified quantitative scoring mechanism was established. For instance, in
the “Patent Ownership” item, responses were encoded as 1 for “Yes” and 0 for
“No.” In the “Award Level” item, first, second, third prizes, and no award were
assigned scores of 3, 2, 1, and 0, respectively. Scores for secondary indicators
were calculated by aggregating item-level scores, and the resulting vectors were
used as input features for BPNN training. This scoring scheme ensures a balance
between interpretability and computational suitability. To assess the internal consistency of the QS, Cronbach’s alpha coefficient was
used—a standard and widely accepted method for measuring reliability in the
social sciences. A threshold of 0.7 is commonly accepted as the minimum for
adequate reliability [38]. The analysis results showed that all reliability
coefficients exceeded 0.7, indicating that the questionnaire possesses high
internal consistency and robust reliability. The detailed reliability analysis is
presented in Fig. 4: Indicator
α Coefficient
value
Background
0.852
Professional
ability
0.753
Practical
ability
0.776
Expanding
ability
0.721
Fig. 4 Reliability analysis of the QS
Statistical Product and Service Solutions (SPSS) 25.0 is a statistical analysis

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

software widely used across disciplines for data processing and interpretation. In
this study, SPSS 25.0 is employed to perform basic statistical computations such
as means, standard deviations, and correlation coefficients. It also facilitates
hypothesis testing, multiple regression analysis, and examination of relationships
among key variables to determine the influence of various factors on IEE. Moreover, SPSS’s reporting and visualization functions enhance the clarity and
communicability of empirical findings. In particular, the Kaiser-Meyer-Olkin (KMO)
measure is used to assess the sampling adequacy for principal component or factor
analysis. The KMO statistic ranges from 0 to 1, with higher values indicating
stronger inter-variable correlations, which are desirable for factor analysis. Typically, a KMO value above 0.5 is considered acceptable, whereas values below
0.5 suggest poor suitability, warranting alternative analytical methods. In the
present study, SPSS 25.0 is used to conduct a validity analysis of the questionnaire
data. The results show that all KMO values exceed 0.5, and the significance levels
are below 0.01, confirming statistical robustness. Additionally, the factor loadings
indicate that each variable contributes adequately, and the explanatory power of
each factor exceeds 60%, suggesting that each survey item is well-differentiated
and the overall structure satisfies psychometric criteria. The detailed validity
analysis results are presented in Fig. 5. Indicator
Question number
Factor loading values
The degree of variable
explanation
KMO
Bartlett's test of
significance
Background

0.782
73.23%
0.735
0.000

0.824

0.795
Professional ability

0.758
76.01%
0.771
0.000

0.833

0.802
Practical ability

0.776
74.03%
0.753
0.000

0.793

0.768
Expanding ability

0.813
70.08%
0.708
0.000

0.781

0.749
Fig. 5 Validity analysis of the QS
To construct a scientifically grounded and practically applicable evaluation
index system, a four-phase process was adopted: literature review, expert
interviews, pilot testing, and final revision.
1) Literature Review: An extensive review of domestic and international
literature was conducted, focusing on themes at the intersection of higher
education, IEE, and music-based aesthetic education. From this body of
research, core variables related to entrepreneurial competence were
extracted—such as academic performance, competition experience,
entrepreneurial engagement, and educational exposure.
2) Expert Consultation: Two rounds of expert interviews were carried out,
involving three university-level IEE instructors, two scholars in music
education, and one entrepreneurship mentor. These consultations provided
critical feedback on the relevance, structure, and wording of the
preliminary indicator framework. Based on this input, several items were
refined or reweighted to better align with the specificities of music-focused
educational contexts.
3) Pilot Testing: A pre-survey was conducted with 30 senior-year music
students. This test assessed item clarity, logical consistency, discriminatory

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

ability,
and
average
completion
time. Results
indicated
high
comprehensibility and operability. Feedback from this stage led to further
refinement, including the removal of redundant items and improvements to
question phrasing.
4) Finalization: The finalized evaluation index system comprises four first-
level indicators—foundational competence, professional competence,
practical competence, and extended competence—each containing three
second-level indicators, forming a total of twelve input variables for the
BPNN model. This index system integrates both theoretical constructs and
real-world educational observations, ensuring high reliability, validity, and
operational feasibility. The final structure of the evaluation index system is illustrated in Fig. 6. First-level
indicators
Secondary indicators
Options
Background
Status upon graduation
Master / Employed / Unemployed /
Entrepreneur
Social practice time
Less than 30 days / 30-60 days / 60-90
days / More than 90 days
Families with an entrepreneurial
background
1-2 years/3-4 years/more than 5 years/
None
Professional
ability
Get copyright
Yes/No
Get the certificate
Elementary/Intermediate/Advanced/
None
Attend competition
First Prize/Second Prize/Third Prize/Not
Winning/Not Participating
Practical ability
Entrepreneurial experience
Successful/Unsuccessful/None
Participate in entrepreneurship
training camp
Yes/No
Published J ournal Papers
Class A/Class B/Class C/Class D/None
Expanding
ability
Participate in entrepreneurial
societies
Succeeded/Unsuccessful/Not Attended
Entrepreneurship educated
Yes/No
Participate in entrepreneurial
programs
Yes/No
Options
1/2/0/3
2/4/6/8
3/4/5/0
6/0
3/6/10/0
8/6/4/2/0
8/6/0
5/0
10/8/4/2/0
3/2/0
5/0
5/0
Fig. 6 Evaluation indexes of music majors’ aesthetic course-oriented IEE
In Fig. 6, each first-level indicator is subdivided into three secondary
indicators. Each secondary indicator is associated with a set of questionnaire items,
and different responses are assigned corresponding scores. These scores are then
aggregated to form the input vectors for the neural network model.

### 4. Result Analysis of Tests and Suggestions

4.1 Result Analysis of Tests
According to the universal approximation theorem, a three-layer neural
network containing one hidden layer can approximate any continuous function on
a closed interval, making it sufficient for mapping an 𝑛-dimensional input to an 𝑚-
dimensional output with minimal training error. Therefore, this study adopts a
three-layer BPNN architecture consisting of an input layer, a hidden layer, and an
output layer. Given the twelve secondary indicators constructed in the evaluation
index system, the number of input layer neurons is set to 𝑛=12, and the number
of output layer neurons is set to 𝑚=1, reflecting a single predicted outcome. Determining the optimal number of hidden layer neurons is critical, as an
excessive number may result in overfitting and increased training time, whereas
too few can limit learning capacity. The empirical formula used to estimate the

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

hidden layer size is:
l =
n + m +a
(14)
Fig. 7 illustrates the relationship between the number of hidden neurons and
the training error.

0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
Error value
The number of neurons in the hidden layer
Training Error
Test Error
Fig. 7 The relationship between the number of neurons in the hidden layer and
the error
As shown in Fig. 7, when the number of hidden neurons is between 3 and 8,
the training error decreases steadily. However, beyond 6 neurons, a slight
increase in test error is observed. Based on a trade-off between model
generalization and fitting accuracy, the number of hidden neurons is set at 7. To
further validate this configuration, 5-fold cross-validation is employed to assess
model performance under different hidden neuron settings. The procedure
involves:
(1) Setting the number of hidden neurons from 2 to 12;
(2) Performing 5-fold cross-validation for each configuration;
(3) Calculating the average test error and standard deviation;
(4) Selecting the configuration with the lowest error and best stability. Fig. 8 Analysis of 5-fold cross validation results
As shown in Fig. 8, a configuration with 7 hidden neurons yields an average
test error of 0.029 and a standard deviation of 0.008, indicating excellent stability
and accuracy. Although increasing the neuron count beyond 7 slightly improves
training error, it results in higher test error variance, signaling potential
overfitting. Thus, selecting 7 neurons offers optimal performance and robustness. Next, the effect of different learning rates on training efficiency is analyzed. The experimental results are depicted in Fig. 9.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Training times
Error

Value
Categories
η=0.005
η=0.01
η=0.02
η=0.03
η=0.04
η=0.05
η=0.06
Fig. 9 Comparison of different learning rates
Based on the outcomes shown in Fig. 9 and the momentum-based error
optimization in Eq. (11), a learning rate of 0.01 is identified as the most effective,
providing a good balance between convergence speed and stability. Subsequently, the performance of six training functions is compared,
including:
1) Levenberg-Marquardt (LM)
2) Resilient Backpropagation (Rprop)
3) Scaled Conjugate Gradient (SCG)
4) One-step Secant (OSS)
5) Gradient Descent Method (GDM)
6) GDM with adaptive learning rate and momentum
Algorithms
Number of
training steps
Performance
Levenberg-
Marquardt
Algorithm

4.50
Rprop Algorithm

2.28
Scaled Conjugate
Algorithm

1.83
One Step Secant
Algorithm

1.58
Gradient Descent
Algorithm

2.13
Gradient descent
algorithm with
adaptive learning
rate + momentum
factor

2.15
Fig. 10 Comparison of training results from different algorithms
Fig. 10 reveals that the LM algorithm achieves the best performance in terms
of both convergence and training time. Therefore, this algorithm is selected for
subsequent model training. The momentum factor is set to 0.9 to prevent the
model from getting trapped in local minima. The BPNN model is implemented in MATLAB, and its performance is evaluated
using Mean Squared Error (MSE). Fig. 11 shows the fitting and regression results
for the training, validation, and overall datasets.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

a
b
c
50 55 60 65 70 75 80 85 90 95 100 105 110

Training: R=0.96236
Output
Target
Fit
γ=T
Data
50 55 60 65 70 75 80 85 90 95 100 105 110

Training: R=0.92574
Output
Target
Fit
γ=T
Data
50 55 60 65 70 75 80 85 90 95 100 105 110

Training: R=0.95039
Output
Target
Fit
γ=T
Data
Fig. 11 Fitting and regression performance of BPNN
(a) Training, (b) Validation, (c) Overall regression
In Fig. 11, the correlation coefficient during the training phase reaches R =
0.96236, during validation R = 0.92574, and for the overall model performance R
= 0.95039. As values of R approaching 1 indicate a strong fit, these results confirm
that the BPNN model exhibits excellent accuracy and generalization. These
findings validate the rationality of both the model structure and the empirical data
used in training. Following model training, the BPNN is tested using a randomly selected
dataset. The comparison between actual values and model-predicted outputs for
the proposed music-major aesthetic course-oriented IEE model is presented in Fig.
12. Output value
Data processing volume
Expected Value
True Value
Fig. 12 Comparison between actual and predicted network output values
As shown in Fig. 12, the predicted outputs closely align with the actual values,

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

with no significant deviations observed. This consistency highlights the model’s
high predictive reliability and the internal validity of the dataset. Notably, the
maximum relative error is only 1.64%, underscoring the model’s robust estimation
capability. Therefore, the trained BPNN yields predictions that are practically
indistinguishable from the true values. To further enhance the scientific rigor of model validation, the study employs
10-fold cross-validation to assess the BPNN’s generalization ability. In this
approach, the dataset is randomly divided into 10 equal parts. Each subset is used
once as the testing set, while the remaining nine serve as the training set. The
process is repeated ten times, and the final performance metrics are averaged
across all iterations. The results are presented in Fig. 13. Fig. 13 10-fold cross-validation results
To further examine potential overfitting during training, the learning curves
of both the training and validation sets are plotted, as shown in Fig. 14.

0.0
0.5
1.0
Loss
Epoch
Train_Loss
Validation_Loss
Fig. 14 Training and validation error convergence trends
As illustrated, the training and validation errors decrease in tandem over
successive iterations and ultimately converge to a stable state, with minimal
divergence. This trend suggests that no significant overfitting occurs during the
training process. The use of cross-validation, learning curve analysis, and multiple
error metrics provides comprehensive support for the model’s stability, reliability,
and generalization capacity. Compared to single-run error evaluations, this multi-
angle validation strategy offers stronger scientific rigor and interpretability. Each student’s evaluation score is derived from responses to twelve indicators,
with score levels reflecting the degree of entrepreneurial competence. Key
findings are summarized as follows:
(1) High-scoring students consistently demonstrate a strong professional
foundation in music. The data confirm that music majors exhibit well-developed
domain-specific knowledge.
(2) Among students scoring above 90, a substantial proportion have
participated in entrepreneurship competitions or attended intensive training
camps. This suggests elevated innovation consciousness and active engagement
in extracurricular learning.
(3) Most students scoring above 80 report involvement in social practice
activities, reflecting broad practical exposure and experience. In conclusion, the BPNN-based evaluation index system, tailored for aesthetic
course-oriented IEE among music majors, effectively captures individual
differences in competence. It serves as a scientifically grounded and practically
feasible auxiliary instructional tool, supporting educators in the systematic
integration and allocation of educational resources.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

4.2 Suggestions
Based on the analysis of the experimental results, the following four
recommendations are proposed to enhance the IEE system for college music
majors:
(1) Expand access to practical entrepreneurship competitions and AI-assisted
instruction systems. More practice-oriented entrepreneurship competitions and training programs
should be organized to foster students' innovative capabilities and entrepreneurial
experience. In particular, the application of AI-powered instructional systems
should be promoted within aesthetic courses to fully leverage their role in
personalized learning and skill development. Achieving this requires the
coordinated
involvement
of
multiple
stakeholders,
including
educators,
institutions, students, and industry partners. Through structured participation in
entrepreneurial activities, students can continuously acquire new knowledge and
enhance practical competencies. Well-designed competitions serve not only as
testing grounds for applied skills but also as platforms for evaluating students’
comprehensive quality. Institutions should enhance their support mechanisms by
forming full-time entrepreneurship advisory teams and partnering with local
enterprises to establish innovation and entrepreneurship incubation centers. In
addition, investment in educational resources—including the recruitment and
training of high-level faculty—will further strengthen the ecosystem supporting
IEE.
(2) Strengthen the theoretical foundation and applied orientation of
professional music education. There is a pressing need to enrich music majors’ theoretical knowledge while
integrating features of specialization, innovation, and interdisciplinarity into the
curriculum. Music education should be aligned with contemporary creative
industry demands, focusing on cultivating talent with both artistic expertise and
entrepreneurial capacity. To this end, a systematic talent development framework
should simulate enterprise-like work environments on campus. For instance,
music studios could be embedded into classroom teaching scenarios, and the
curriculum should be restructured to reflect market needs. Where conditions
permit,
individualized
mentorship—distinct
from
conventional
course
instruction—should be implemented. Mentors can offer targeted feedback on
students’ creative and performance work, guiding them through iterative
refinement. Moreover, reinforcing the practical application of musical knowledge
enhances the potential for customized and industry-relevant IEE. A school-
enterprise collaborative model may also be introduced, allowing students who
have completed core theoretical courses and earned sufficient credits to
undertake internships in partner companies, thereby facilitating the transfer of
classroom knowledge into real-world entrepreneurial practice.
(3) Promote scientific and structured innovation and entrepreneurship
training. IEE must be delivered through systematic and well-designed pedagogical
strategies, supported by macro-level policy frameworks. Government and
institutional support should be strengthened to establish favorable conditions for
entrepreneurship education. Students with strong academic foundations and
independent thinking abilities should be selected to participate in intensive
training programs, receiving expert guidance and professional mentoring. At the
same time, a vibrant cultural atmosphere that encourages innovation and
originality should be cultivated within the campus community. Establishing on-
campus demonstration zones equipped with advanced hardware and software
infrastructure can provide students with dedicated spaces for experimentation,
prototyping, and entrepreneurial exploration. These environments serve as
incubators for student-led innovation and help stimulate broader enthusiasm for
creative enterprise among the student body.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

### 5. Discussion

This study aims to advance IEE in Chinese music institutions by implementing
a BPNN-based AI-assisted teaching system to cultivate entrepreneurial spirit
among arts students. Drawing on the theoretical foundations of IEE and neural
network modeling, the study developed a BPNN framework comprising 12 input
neurons, 7 hidden neurons, and 1 output neuron. Empirical training and evaluation
of the model validated the effectiveness of the teaching system and confirmed the
scientific rigor of the BPNN-based entrepreneurship education assessment
framework. Results indicated that the BPNN-assisted system significantly
enhanced students’ entrepreneurial awareness and abilities, demonstrating its
practical value in music education. Comparative analyses of neural network fitting
and regression performance further supported the robustness and reliability of
the model and underlying data. For example, Yang (2020) proposed optimization
strategies for college art instruction combining theoretical models with AI-driven
algorithmic analysis, illustrating innovative applications of AI in evaluating course
effectiveness [39]. He and Sun (2021) introduced an AI-based teaching system that
achieved superior student learning outcomes compared with traditional
pedagogical approaches in art education [40]. Xu (2022) developed a neural
network–based evaluation model integrating ideological and political elements
into music education, enhancing instructional relevance and contextual
adaptability [41]. Similarly, Zheng et al. (2018) created an AI-assisted art
education framework capable of dynamically assessing teaching effectiveness and
supporting adaptive instruction [42]. This study differs from prior research in several ways. First, it not only
continues the application of AI in art education but also provides a replicable,
empirically validated system for assessing entrepreneurial competence in music
students. Second, the proposed BPNN-assisted teaching system enables dynamic,
personalized assessment and real-time feedback, forming a closed-loop structure
of “teaching effectiveness—competence development—system feedback.” This
approach promotes data-driven instructional decisions and optimizes educational
resource allocation. Furthermore, the assessment indicator system developed in
this study considers the multidimensional competencies necessary for music
entrepreneurship. These include students’ background, professional skills,
practical experience, and extended abilities. By incorporating these factors, the
system enhances the model’s adaptability to complex educational environments. In educational measurement theory, learner competence is regarded as a
multidimensional latent variable structure, characterized by high intercorrelation,
implicit hierarchical relationships, and dynamic developmental trajectories. This
is particularly pronounced in the evaluation of innovation and entrepreneurship
competencies. Traditional linear assessment models often assume that indicators
are independent and linearly additive. However, in practice—especially in arts
disciplines such as music—interactions among professional competence, aesthetic
expression, project awareness, and market judgment are typically nonlinear, with
potential “leaps” or “plateaus.” BPNN’s multilayer architecture and nonlinear
mapping capabilities effectively address these characteristics, improving
predictive accuracy and enhancing the interpretability of the assessment model. Despite the demonstrated effectiveness of the BPNN model in music education,
certain limitations remain. First, the study sample was restricted to music students;
future research could examine the system’s applicability in other arts disciplines,
including visual arts, dance, and theater. Second, while BPNN performs well with
complex educational data, it entails considerable computational complexity. Applying it to large-scale datasets may encounter performance bottlenecks. Future studies could explore more efficient algorithms to optimize BPNN or
integrate it with other AI methods to improve processing efficiency and real-time
feedback capabilities. Finally, this study offers insights for extending the system
to other disciplines. Although the BPNN model shows high applicability in music
education, adapting it to other fields may face challenges related to course content
differences, heterogeneity of student characteristics, and interdisciplinary

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

collaboration. Therefore, future work should investigate how to adjust the
assessment framework and model structure across different disciplinary contexts
to ensure generalizability and practical utility.

### 6. Conclusion

This study centers on university music majors and proposes the construction
and application of an auxiliary instructional system based on the BPNN to evaluate
and optimize the effectiveness of IEE. Questionnaire-derived data were
preprocessed, standardized, and used to train and test the BPNN model. The
model successfully captured differences in student characteristics and latent
educational needs during the entrepreneurial training process. The empirical
results indicate that the BPNN model demonstrates a reasonable degree of
predictive accuracy, achieving a maximum relative error of only 1.64% in
simulated scoring. When combined with cross-validation and multiple error metric
evaluations, the model exhibits a certain level of adaptability. However, the
generalization and robustness of the model remain subject to further validation,
particularly with larger and more heterogeneous samples. As such, the current
findings should be interpreted cautiously, as they are based on a specific sample
group and controlled simulation conditions and do not yet substantiate the
universal applicability of the proposed system. Despite these limitations, the study yields several important contributions. First, it represents a pioneering effort to integrate artificial neural network
technology into the evaluation of IEE for music majors, introducing a structured
modeling approach that offers preliminary insights for the development of
intelligent instructional evaluation systems. Second, by mining individual students’
traits and instructional needs, the model facilitates data-informed decisions for the
personalized allocation of educational resources. Third, the study constructs a
relatively comprehensive evaluation index system, supported by empirical data,
and implements systematic modeling to assess the instructional effectiveness of
IEE. Future research should focus on further optimizing the model’s architecture,
integrating multi-source data—including real-time learning behavior, interview
data, and instructional feedback—and expanding the sample size and diversity to
improve model robustness. In addition, combining quantitative modeling with
qualitative research methods would enable deeper analysis of students’ authentic
motivations and contextual factors influencing entrepreneurial behavior, thereby
enhancing the model’s interpretability and real-world applicability. Lastly, it is
essential to explore the adaptability and scalability of this BPNN-based IEE
evaluation framework across different disciplinary contexts, including other art-
focused and comprehensive universities, to assess its broader educational utility. Funding: This research received no external funding. Data Availability Statement
The datasets used and/or analyzed during the current study are available from the
corresponding
author
Juan
Xia
on
reasonable
request
via
e-mail
xiaxia0211@hbnu.edu.cn. Competing Interest
The authors declare no competing financial or non-financial interests. Author Contributions Declaration
Juan Xia: Conceptualization, methodology, software, validation, formal analysis,
investigation, resources, data curation, writing—original draft preparation, writing—review
and editing, visualization, supervision, project administration, funding acquisition

## ETHICS STATEMENT

The studies involving human participants were reviewed and approved by

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

Conservatory of music of Hubei Normal University Ethics Committee (Approval
Number: 2022.405842384). The participants provided their written informed
consent to participate in this study. All methods were performed in accordance with
relevant guidelines and regulations. References
[1] Crone, C. L., & Kallen, R. W., 2024. Measuring virtual embodiment: A
psychometric investigation of a standardised questionnaire for the
psychological sciences. CHB Reports, 14(1), pp. 100422.
[2] Wang, C., & Fu, B., 2023. A study on the efficiency of allocation and its
influencing factors on innovation and entrepreneurship education resources
in Chinese universities under the five-in-one model. INT J MANAG EDUC-
OXF, 21(1), pp. 100755.
[3] Dai, K., & Liu, Q., 2024. Leveraging artificial intelligence (AI) in English as a
foreign language (EFL) classes: Challenges and opportunities in the
spotlight. Computers in Human Behavior, 159, pp.108354.
[4] Yılmaz, Ö., 2024. Personalised learning and artificial intelligence in science
education: current state and future perspectives. Educational Technology
Quarterly, 2024(3), pp.255-274.
[5] Yang, Y., 2020. Exploration and Practice of Maker Education Mode in
Innovation and Entrepreneurship Education. Frontiers in Psychology, 11,
p.1626.
[6] Zhang, X., Yang, W., and Wang, Y., 2022. Research on the Application of
Artificial Intelligence in Music Education. Education Modernization, 37(6),
pp.112-114.
[7] Ma, X., Guan, Y., Mao, R., Zheng, S. and Wei, Q., 2021. Modeling of lead
removal by living Scenedesmus obliquus using backpropagation (BP) neural
network algorithm. Environmental Technology & Innovation, 22, pp.101410.
[8] Sari, I. M., and Yuliawan, R., 2020. The development of an artificial
intelligence-based
entrepreneurship
education
system. Journal
of
Entrepreneurship Education, 23(5), pp.1-8.
[9] Milić, T., Tomić, B., Marinković, S., & Jeremić, V., 2024. ESPRIT adventure: Assessing hybrid fuzzy-crisp rule-based AI method effectiveness in teaching
key performance indicators. INT J MANAG EDUC-OXF, 22(3), pp.101022.
[10]Zhu, S., Wang, Z., Zhuang, Y., Jiang, Y., Guo, M., Zhang, X., & Gao, Z., 2024. Exploring the impact of ChatGPT on art creation and collaboration: Benefits,
challenges and ethical implications. TIR, 14(1), pp.100138.
[11]Maiya, A. K., & Aithal, P. S. (2023). A review-based research topic
identification on how to improve the quality services of higher education
institutions in academic, administrative, and research areas. IJMTS, 8(3),
pp.103-153.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

[12]Rogoza, R., Żemojtel-Piotrowska, M., Kwiatkowska, M. M. and Kwiatkowska, K., 2018. The bright, the dark, and the blue face of narcissism: the Spectrum
of Narcissism in its relations to the metatraits of personality, self-esteem, and
the nomological network of shyness, loneliness, and empathy. Frontiers in
Psychology, pp.343.
[13]Tang, K. H. D., 2024. Implications of artificial intelligence for teaching and
learning. Acta Pedagogia Asiana, 3(2), pp.65-79.
[14]Alkan, A.,
2024. Artificial
intelligence: Its
role
and
potential
in
education. İnsan ve Toplum Bilimleri Araştırmaları Dergisi, 13(1), pp.483-497.
[15]Tashtoush, M. A., Wardat, Y., Ali, R. A. and Saleh, S., 2024. Artificial
intelligence in education: mathematics teachers’ perspectives, practices and
challenges. Iraqi Journal for Computer Science and Mathematics, 5(1), pp.20.
[16]Suryanarayana, K. S., Kandi, V. P., Pavani, G., Rao, A. S., Rout, S. and Krishna, T. S. R., 2024. Artificial intelligence enhanced digital learning for the
sustainability of education management system. The Journal of High
Technology Management Research, 35(2), pp.100495.
[17]Hameed, I., Zaman, U., Waris, I. and Shafique, O., 2021. A serial-mediation
model to link entrepreneurship education and green entrepreneurial behavior:
application of resource-based view and flow theory. International journal of
environmental research and public health, 18(2), pp. 550.
[18]Jin, Z., Goyal, S. B. and Rajawat, A. S., 2024. The informational role of artificial
intelligence in higher education in the New era. Procedia Computer
Science, 235, pp.1008-1023.
[19]Yan, C., Li, M., Liu, W. and Qi, M., 2020. Improved adaptive genetic algorithm
for the vehicle Insurance Fraud Identification Model based on a BP Neural
Network. Theoretical Computer Science, 817, pp.12-23.
[20]Yuan, C. H. and Wu, Y. J., 2020. Mobile instant messaging or face-to-face? Group interactions in cooperative simulations. Computers in Human
Behavior, 113, p.106508.
[21]Yılmaz, Ö., 2024. Personalised learning and artificial intelligence in science
education: current state and future perspectives. Educational Technology
Quarterly, 2024(3), pp.255-274.
[22]Wu, L., Zhou, J. and Li, Z., 2020. Applying of GA-BP neural network in the land
ecological security evaluation. IAENG International Journal of Computer
Science, 47(1), pp.11-18.
[23]Afeli, S. A. and Adunlin, G., 2022. Curriculum content for innovation and
entrepreneurship education in US pharmacy programs. Industry and Higher
Education, 36(1), pp.13-18.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

[24]Carpenter, A. and Wilson, R., 2022. A systematic review looking at the effect
of entrepreneurship education on higher education student. The International
Journal of Management Education, 20(2), pp.100541.
[25]Yang, H., Li, X., Qiang, W., Zhao, Y., Zhang, W. and Tang, C., 2021. A network
traffic forecasting method based on SA optimized ARIMA–BP neural
network. Computer Networks, 193, p.108102.
[26]Zhang, D. and Lou, S., 2021. The application research of neural network and
BP algorithm in stock price pattern classification and prediction. Future
Generation Computer Systems, 115, pp.872-879.
[27]Gu, P., Zhu, C. M., Wu, Y. Y. and Mura, A., 2020. Energy consumption
prediction model of SiCp/Al composite in grinding based on PSO-BP neural
network. In Solid
State
Phenomena, 305,
pp.
163-168. Trans
Tech
Publications Ltd.
[28]Choy, L. H. T., and Ho, W. K. O., 2023. The Use of Machine Learning in Real
Estate Research. Land, 12(4), pp.740.
[29]Elliott, C., Mantler, J. and Huggins, J., 2021. Exploring the gendered
entrepreneurial
identity
gap:
implications
for
entrepreneurship
education. International Journal of Gender and Entrepreneurship 13(1), pp.
50-74.
[30]Geng, P., Wang, J., Xu, X., Zhang, Y. and Qiu, S., 2020. SOC Prediction of
power lithium battery using BP neural network theory based on
keras. International Core Journal of Engineering, 6(1), pp.171-181.
[31]Xing, Z., Ma, G., Wang, L., Yang, L., Guo, X., & Chen, S., 2025. Towards visual
interaction: hand segmentation by combining 3D graph deep learning and
laser point cloud for intelligent rehabilitation. IEEE Internet of Things Journal.
[32]Zhang, W., Shankar, A., Antonidoss, A., 2020. Modern art education and
teaching based on artificial intelligence. Journal of Interconnection Networks,
22(Supp01), pp.2141005.
[33]Xing, Z., Meng, Z., Zheng, G., Ma, G., Yang, L., Guo, X.,... & Wu, H., 2025. Intelligent rehabilitation in an aging population: empowering human-machine
interaction for hand function rehabilitation through 3D deep learning and
point cloud. Frontiers in Computational Neuroscience, 19, pp. 1543643.
[34]Zhou, Y. and Zhou, H., 2022. Research on the quality evaluation of innovation
and
entrepreneurship
education
of
college
students
based
on
extenics. Procedia Computer Science, 199, pp.605-612.
[35]Ma, X., and Sun, C., 2021. Research on the Application of Artificial
Intelligence in Music Education. International Journal of Emerging
Technologies in Learning (iJET), 16(22), pp.191-204.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS

## ARTICLE IN PRESS

[36]Liu, Q., Huang, R., and Zhang, L., 2021. Learning analytics based on artificial
intelligence: research progress and application prospects. Library Hi Tech,
39(2), pp.287-301.
[37]Chen, L., Yang, X., Sun, C., Wang, Y., Xu, D. and Zhou, C., 2020. Feed intake
prediction model for group fish using the MEA-BP neural network in intensive
aquaculture. Information Processing in Agriculture, 7(2), pp.261-271.
[38]Li, R., 2020. Research on treatment of retaining wall foundation with
geosynthetics based on BP neural network. In Key Engineering Materials, 852,
pp. 220-229. Trans Tech Publications Ltd.
[39]Yang, R., 2020. Artificial intelligence-based strategies for improving the
teaching effect of art major courses in colleges. International Journal of
Emerging Technologies in Learning (iJET), 15(22), pp.146-160.
[40]He, C., and Sun, B., 2021. Application of artificial intelligence technology in
computer aided art teaching. Computer-Aided Design and Applications,
18(S4), pp.118-129.
[41]Xu. L., 2022. Ideological and Political Function Modeling of College Music
Education Based on Improved Neural Network. International Journal of e-
Collaboration (IJeC), 19(4), pp. 1-14.
[42]Zheng, W., Wu, Y. C. J. and Chen, L., 2018. Business intelligence for patient-
centeredness: a systematic review. Telematics and Informatics, 35(4), pp.665-
676.

## ACCEPTED MANUSCRIPT

## ARTICLE IN PRESS
