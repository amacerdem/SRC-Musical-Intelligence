# Construction of online classroom

**Year:** D:20

---

Construction of online classroom
instructional quality assessment
system of university music based
on BP neural network
Runze Ouyang
In view of the strong subjectivity of traditional instructional quality assessment methods and the
difficulty in quantifying nonlinear teaching elements, this article proposes an online classroom
assessment model of college music based on improved BP neural network (BPNN). The model
integrates multi-dimensional data such as the frequency of teacher-student interaction and the
utilization rate of teaching resources, and constructs a nonlinear mapping structure with double
hidden layers. At the same time, the optimization strategy of dynamic learning rate (initial value
0.01, attenuation coefficient 0.9) and momentum factor (coefficient 0.9) is adopted. After cleaning
and standardization, the real data is divided into training set and test set according to the ratio of
7: 3. Through cross-validation, the optimal number of hidden layer nodes is 25, and the normality of
error distribution is verified (p > 0.05). The experimental results show that the prediction accuracy of
this model reaches 95.2%(95% confidence interval is [93.7%, 96.4%]), which is 20.69% higher than
the traditional ID3 algorithm, and the mean absolute error (MAE) is reduced to 0.032. The model is
excellent in capturing complex indicators such as emotional interaction between teachers and students
and innovation of teaching content (F1 value is 0.93), and it has stable generalization ability for data
of different teaching platforms (standard deviation < 1.5). The dynamic learning rate strategy improves
the training efficiency by 37% and effectively avoids the local optimization problem. This study
confirms the effectiveness of neural network in education assessment and provides practical reference
for the digital transformation of music education. In the future, this achievement is expected to be
extended to interdisciplinary online teaching scenarios, thus promoting the development of education
in the direction of fairness and individuality. Keywords  Back propagation neural network, University music teaching, Online class, Instructional quality
assessment
With the popularization of tertiary education, people’s attention and understanding of education are gradually
improving1. More and more people realize that enhancing citizens’ education level and expanding access to
tertiary education not only elevates the cultural literacy of the public but also fuels the scientific and technological
progress of the nation2. Education stands as a vital component of life. As universities expand, both society
and academic institutions are increasingly attentive to the quality of students’ learning3. With the deepening
and evolution of music education reform in universities, novel challenges have surfaced in university music
classrooms, necessitating the formulation of a fresh set of classroom assessment criteria to provide guidance and
standardization4. Online classroom instructional assessment serves as a critical tool to advance students’ online
learning and enhance teachers’ online instruction proficiency. As an emerging teaching modality, online instruction ought to be anchored in an online instruction quality
assessment system. This ensures parity with offline teaching and drives the elevation of online instruction
standards. The rapid advancement and profound integration of information technology in tertiary education
and teaching have catalyzed the transformation and innovation of traditional classroom instructional models5. As a novel instructional approach, online instruction requires enhancement in teaching platform construction
and maintenance, elevation of teachers’ teaching proficiency, adaptation of students’ learning methodologies,
and assurance of instructional quality6. In recent years, the proliferation of online course platforms has been
Academy of Music, Dance and Fine Arts “Prof. Asen Diamandiev”, Staria Grad Plovdiv Center, Ul. “Todor
Samodumov” 2, 4000 Plovdiv, Bulgaria. email: 526629608@qq.com
OPEN
Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports

accompanied by a significant improvement in course quality. The accumulation of a vast amount of user data
during usage provides a certain degree of insight into the strengths and weaknesses of online courses7. In this
context, effective monitoring and reasonable assessment of the online classroom teaching phase, coupled with
the establishment of an online classroom instructional level assessment index system, assumes paramount
importance. With the rapid development of information technology, online teaching has become an important
part of college music education, but it also brings many new challenges. Online classroom generally lacks face-
to-face interaction, and the immediate feedback mechanism between teachers and students is weak, which
may lead to the decrease of students’ learning enthusiasm and the difficulty in ensuring instructional quality. Moreover, music teaching is practical and artistic, and traditional assessment methods are difficult to fully
reflect the teaching effect, so there are limitations in emotional expression and artistic creativity assessment. In
addition, the uneven distribution of teaching resources in different universities and teachers’ different levels of
network technology aggravate the complexity of online instructional quality assessment. In this context, online instructional quality assessment is particularly important. It can help teachers find
problems in time, improve teaching strategies and improve instructional efficiency. Scientific assessment
system can also provide decision-making basis for school administrators and promote the rational allocation
of educational resources. At the same time, the assessment results can be used as an important reference for
students to reflect on themselves and adjust their learning methods, which is helpful to improve their autonomous
learning ability. Therefore, building an efficient and intelligent online music classroom quality assessment system
is not only the key to meet the current challenges, but also the inevitable choice to promote the reform and
development of music education. BPNN, an adaptive feedforward learning network, plays a pivotal role in the domain of artificial intelligence8. In recent years, as a powerful machine learning model, BPNN has been widely used in many fields. In the
research of Shu et al.9, BPNN was used to evaluate the performance of private enterprises in China in a multi-
level dynamic fuzzy way. This shows that it has unique advantages in dealing with complex enterprise assessment
problems. Yan et al.10 demonstrated the application of BPNN in software quality assessment. By combining SCT
model with BPNN, the accuracy and reliability of assessment were improved. Zhang et al.11 further expanded
the application scope of BPNN, and applied it to the prediction of mechanical properties. Through the ATPSO-
BP neural network model, the prediction accuracy was improved. Ye et al.12 focused on the problem of speech
classification, and improved the classification performance through the BP neural network optimized by PSO. These studies show that BPNN has strong nonlinear fitting ability and adaptive learning ability, and can be
optimized according to the characteristics of different fields, thus playing an important role in solving various
complex problems. Combining different optimization algorithms and model structures, the performance of
BPNN can be further improved and it can be applied in the field of education. Based on an analysis of the
current state and distinctive characteristics of online music classroom instruction quality assessments, this
article constructs an assessment model for university music instruction, leveraging BPNN technology to usher
intelligence into the realm of music education. Musical instruction assessment represents the subjective conceptual assessment of the value of the studied
object in the realm of music education, grounded in factual observations. Divergent values will naturally yield
varying assessment outcomes13. Conducting an effective assessment of the musical instruction level stands as
a potent strategy adopted by educational institutions to holistically enhance the quality of music instruction14. In contrast to previous assessment frameworks, where the worth of each assessment metric was frequently
determined through simplistic mathematical computations to gauge a music instructor’s teaching efficacy15,
modern methods recognize the limitations of this approach. This is primarily because the correlation between
the input and output of the assessment system may not adhere to a straightforward linear pattern16. The
intricate nature of the teaching phase, encompassing both instruction and learning, renders the assessment of
instructional quality significantly more complex than assessing a tangible product17. The innovation of artificial
neural networks lies in their capability to model nonlinear processes, eliminating the necessity to comprehend
the underlying reasons for data generation18. This article introduces a mathematical model for assessing the level
of musical instruction, utilizing neural network theory. This model serves as a valuable reference for further
exploration into the development of musical instruction assessment systems. Theoretical basis
As an important component of higher education, the improvement of music instructional quality and management
level is increasingly receiving attention. In order to comprehensively and objectively evaluate the quality of music
teaching, various assessment methods and models emerge one after another. However, traditional assessment
methods are often limited by subjectivity and one-sidedness, making it difficult to accurately reflect the true
level of music teaching. Therefore, exploring a scientific, objective, and comprehensive method for assessing the
quality of music teaching is particularly important. The importance of music teaching assessment
The assessment of music instructional quality is the key link to improve the quality of music education. Through
the comprehensive assessment of music teaching, we can find out the problems and shortcomings in teaching
in time and provide strong support for teaching improvement. The assessment results can also be used as an
important basis for school management to formulate educational policies and optimize the allocation of teaching
resources. The assessment of music instructional quality is also of great significance for students’ individual
development, which can help students understand their own learning situation, adjust their learning strategies
and improve their learning effect. Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

Application of BPNN in music instructional quality assessment
BPNN is a multi-layer feedforward neural network based on error back propagation. It has strong self-learning,
self-organization and self-adaptability, and can deal with complex nonlinear problems. In the assessment of
music instructional quality, BPNN can automatically extract the key factors that affect the instructional quality
by training and learning a large number of teaching data, thus constructing an accurate assessment model. The application of BPNN in music instructional quality assessment includes the following steps:
(1) Data preparation: Collect data related to the quality of music teaching, including teachers’ teaching level,
students’ learning achievements and the allocation of teaching resources. These data should cover all aspects
of music teaching to ensure the comprehensiveness and accuracy of the assessment.
(2) Data preprocessing: cleaning, sorting and normalizing the collected data to eliminate the influence of
abnormal values and noise data on the assessment results. At the same time, the data is divided into training
set and test set, so as to train and verify the following model.
(3) Build a BPNN model: According to the characteristics of music teaching, design an appropriate neural
network structure, including input layer, hidden layer and output layer. The input layer is responsible for
receiving the pre-processed teaching data, the hidden layer performs nonlinear transformation on the data
through the activation function, and the output layer gives the final assessment result.
(4) Model training: BPNN is trained by using training set data. By constantly adjusting the network weights
and thresholds, the network can learn the inherent laws and characteristics in the data. Optimization algo­
rithms such as gradient descent method can be used to accelerate convergence and improve training efficien­
cy. In the model training, in order to ensure the best performance, the optimization parameters are finely
adjusted. The specific parameters are set as follows: the initial value of learning rate is set to 0.01, and it is
gradually reduced to 0.001 by dynamic adjustment. The maximum number of iterations is set to 1000, and
once the change of the loss function is less than the threshold (1e-5), it will be terminated early. The number of
hidden layer nodes is initially set to 20 according to the input feature dimension, and then optimized to 25 by
grid search. The momentum coefficient is set to 0.9 to enhance the convergence speed and stability. The com­
parative experiment shows that the parameter setting has a significant influence on the model performance. For example, if the learning rate is too high, it will easily lead to the model falling into local optimum; If the
learning rate is too low, the convergence speed of the model will decrease. Therefore, the above parameters
are optimized after many experiments.
(5) Model verification and optimization: the trained BPNN model is verified by using test set data. The perfor­
mance of the model is evaluated by calculating the accuracy and recall of the model. If the performance of the
model is not good, it can be optimized by adjusting parameters such as network structure and learning rate.
(6) Analysis and feedback of assessment results: Apply the trained BPNN model to the actual music instruc­
tional quality assessment. Through the analysis of the assessment results, we can find out the problems and
shortcomings in teaching in time and provide strong support for teaching improvement. At the same time,
the assessment results will be fed back to teachers and students to help them understand their teaching and
learning situation, so as to adjust teaching strategies and learning methods in time. In neural network, the input layer is responsible for receiving external data and transmitting it to the hidden
layer; The hidden layer extracts features and patterns from the data through complex calculation and nonlinear
transformation. The output layer converts the processing result of the hidden layer into the final assessment
result. This multi-level structure enables BPNN to process complex teaching data and realize accurate assessment
of music instructional quality. The advantages of BPNN in assessing the quality of music teaching
Compared to traditional music instructional quality assessment methods, BPNN based assessment methods
have the following advantages:
(1) Objectivity: BPNN evaluates data by automatically learning features and patterns, avoiding subjective
interference from human factors and making the assessment results more objective and accurate.
(2) Comprehensiveness: BPNN can handle multi-dimensional input data, thus comprehensively reflecting all
aspects of music teaching. This helps to identify potential problems and shortcomings in teaching, providing
a comprehensive perspective for teaching improvement.
(3) Adaptability: BPNN has strong adaptability and can automatically adjust model parameters with changes
in teaching data. This enables the assessment model to adapt to changes in different teaching environments
and student groups, maintaining the accuracy and effectiveness of the assessment. Methodology
Problems and needs of university music online classroom
With increasing attention being paid to music education in universities, the teaching reform in this field is
gaining momentum, leading to profound changes in the overall landscape of music classroom instruction. Whether it’s teaching objectives, content, processes, or methodologies, everything has undergone a
comprehensive renewal and restructuring. Due to the influence of factors like the network environment and
teachers’ proficiency in network technology on online instruction, their preparation for it becomes even more
critical than for offline classes. Only when instructors are well-versed in the platform’s operation and application
can they accomplish their teaching goals, devise contingency plans for potential online teaching emergencies,
and respond appropriately, thereby ensuring seamless online instruction19. Among various subjects, music
stands out as a unique discipline, and the university-level music course occupies a special place within it. When
Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

assessing music classroom instruction in universities, it’s essential to consider the subject’s distinct features at
this stage, emphasizing its individuality and establishing classroom assessment criteria tailored to the course’s
characteristics. Teaching assessment is a multifaceted and multilevel ongoing activity. Since assessment factors
are often qualitative and there’s no universal teaching assessment index system, different universities typically
have their own frameworks20. Owing to diverse assessment factors and levels, various universities commonly
adopt distinct assessment approaches. During the period of epidemic prevention and control, teachers can timely transmit the national policies,
prevention and control knowledge, typical deeds, mental health education and other contents to students in
online classroom teaching, forming a rich online course ideology education teaching resources. The diversified
assessment system must be student-centered and teacher-led, and advocate the cooperative relationship between
the testees and testers. In the assessment system, teachers are not only responsible for organizing and recording
assessment activities, but also guiding and helping students in the assessment process21. The teaching design of
online classroom should not only include the learning situation analysis, instructional objectives, instructional
content and time allocation, teaching difficulties and solutions, teaching material analysis, instructional methods
and other elements of traditional offline classroom teaching design, but also consider the teaching facilities or
teaching environment that online instruction needs to prepare in terms of time and cyberspace, and design a
relatively stable and easy-to-operate online instructional mode in advance. Classroom instructional assessment
is essential, but it is far from being able to comprehensively judge students’ studies22. Therefore, it is suggested
that teachers should assess students’ academic performance based on their engagement and achievements in
the music classroom. Simultaneously, they should leverage multimedia networks and other classroom and
extracurricular activities linked to music to promptly grasp students’ mastery and application of musical
concepts and techniques23. This approach enables teachers to identify students’ challenges during the learning
process and evaluate the intellectual and non-intellectual factors influencing their learning progress. The instructional effect can not be simply regarded as the result of teaching, but the teaching result is a
reflection of the instructional effect. The efficiency of online classroom teaching is mainly reflected in the activity
of teacher-student interaction, the number and satisfaction of teachers’ answering questions, and students’
participation in discussion, answering questions and homework tasks. Online teaching has broken through the
limitation of traditional offline teaching time and place. Teachers should attach importance to the advantages
of online instruction, lay stress on the cultivation of students’ autonomous learning ability, guide students to
actively participate in online learning, discussion, answering questions and homework tasks, and improve the
efficiency of online classroom teaching24. Teachers should make corresponding instructional plans according to
the actual situation of different platforms and classes, so as to realize teaching according to local conditions and
aptitude. At the same time, teachers should reasonably choose online classroom instructional mode according
to the different characteristics of online instruction before, during and after class, so as to improve classroom
instructional effect and students’ learning efficiency. Assessment model of university music instructional level based on BPNN
In the teaching stage, teachers can effectively assess students’ achievements at any time, such as in class discussion,
students’ homework and all aspects of classroom teaching, and at the same time, they should also consider
students’ extracurricular music learning. In the stage of music teaching, on the one hand, teachers should guide
students to set their own goals, and use this as a standard to test their music learning effectiveness. On the
other hand, students should learn self-reflection, self-improvement and self-perfection, and encourage them to
actively participate in the learning stage, so that the burden on teachers can be slightly reduced25. According to
the weight analysis, teachers should carefully design online interactive links, get the utmost out of efficient IT
methods to mobilize students’ enthusiasm, and use the functions of online instruction platform such as group
discussion, answering questions in class, barrage and so on to attract students to participate in the classroom,
and carry out effective teacher-student interaction, so that students can feel the sense of reality and gain in
online learning. As a teacher, we should adjust our teaching according to different assessment situations, so as to
improve the efficiency of classroom teaching and make assessment really serve teaching. Teachers should guide
students’ self-assessment, understand students’ learning stage and let students have their own development
goals. Teachers should also actively play the main role of students’ online instruction activities, guide and help
students to find faster learning ways by participating in discussions, answering questions and homework tasks,
and improve their autonomous learning ability. Instructional level assessment can comprehensively assess teachers’ ideological style, work ability, work
attitude and work performance, objectively reflect teachers’ teaching level, and provide a basis for rational
selection of teachers26. In instructional assessment, teachers or education authorities should participate, and
more importantly, students who are assessd should also make a reasonable assessment of their own learning. In
the neural network model of instructional level assessment. The data mining model structure of music online
classroom instructional assessment system is shown in Fig. 1. In reality, due to various subjective factors, the assessment lacks theoretical basis, so we also build a BPNN
model based on instructional level assessment according to the characteristics of BPNN, and make a quantitative
analysis of the instructional assessment results. The assessment model of music online classroom instructional
level based on BPNN is shown in Fig. 2. Music teachers in universities not only educate people with the beautiful articles in textbooks and the
humanistic ideas they contain, but also have a great influence on students by their own attitude of caring
about problems and ways and means of imparting knowledge. In the past, the assessment of a music course
in a university was often completed through specific quantitative tables to achieve the purpose of assessing the
classroom27. Considering this structured and valuable scale, we can enhance it by breaking down secondary
indicators to emphasize the emotional and cultural elements inherent in university-level music education28. This
Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

approach will further illuminate the qualitative attributes of the subject. In ensuring a comprehensive assessment
system for teachers’ instructional proficiency, it’s crucial to maintain a clear direction, adhering to the principle
of relevance and specificity. Through continuous learning and training, BPNN can discover its regularity from a large amount of
educational data with unknown patterns:
m = √x + y + R (10)
(1)
where m is the quantity of neurons in the hidden layer, x is the quantity of neurons in the output layer, and y is
the quantity of neurons in the input layer. The roughness calculation stage of the set X is:

## R−(X) = {U2, U3, U4, U5, U7}

(2)
Fig. 2. The assessment model of music online classroom instructional level based on BPNN. Fig. 1. Data mining model structure of music online classroom instructional assessment system. Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

## R−(X) = {U2, U4, U5} ̸= ∅

(3)
Therefore:
ρ (X) = 1 −|POSC (X)|
|R−(X)|
= 0.6
(4)
If X = {U2, U3}, it is not definable because:

## R−(X) = {U2, U3, U5, U7}

(5)
R−(X) = {x ∈U |R (x) ∩X ̸= ∅} ̸= ∅
(6)
R−(X) represents the lower approximation of the set X, that is, the set of all elements belonging to X; R−(X)
represents the upper approximation of the set X, that is, the set of all elements that may belong to X; ρ (X)
represents the roughness of set X, that is, the uncertainty of set X; POSC (X) represents the positive region of
the set X, that is, the set of all elements belonging to X. R (x) in formula (6) represents the rough set of element
x, that is, the set of all elements related to x. The assessment value of the teaching supervision group after listening to the class is used as the expected
output value29. Through the feedback information provided by classroom instructional assessment, teachers and
students can make clear the degree of realization of instructional objectives, whether the forms and methods
adopted in classroom instructional activities are conducive to promoting the realization of the prescribed
classroom instructional objectives, and accumulate information to provide the basis for how to achieve and
modify the instructional objectives more smoothly. The second is the assessment function. Through classroom
instructional assessment, we can understand the quality and level, advantages and disadvantages of music
teachers’ classroom teaching, so as to examine and identify teachers and students’ academic performance, ability
and development level. Weight adjustment formula with additional momentum factor:
∆W (t) = ηδX + α∆W (t −1)
(7)
where W is the weight matrix, X is the input vector, α is the momentum coefficient, usually α ∈(0, 1). The learning rate is:
∆w = −η ∂E
∂w 
(8)
To assess the level of music teaching in universities, we should not only fully consider the relativity and
comprehensiveness of teachers’ teaching, but also combine it with the school’s educational objectives. Let xi (t)
represent the input information at the time of t, and oj (t) represent the output information of j at the time of t, then the state of the neuron j is expressed as:
oj (t) = f
{[
n
∑
i=1
ωijxi (t −τij)
]
−Tj}
(9)
where τij is the synaptic delay, Tj is the threshold of the neuron, ωij is the weight of the neuron from i to j, and
f (·) is the transfer function. If τij is the unit time, then:
oj (t + 1) = f
{[
n
∑
i=1
ωijxi (t)
]
−Tj}
(10)
The subscripts of the input and output end indicate the diversity of the input and output methods of the neuron
model, which can get the utmost out of this property of the model to solve different problems according to
different needs. The input of the neuron at time t is represented by the following formula:
netj′ (t) =
n
∑
i=1
ωijxi (t)
(11)
For the above formula, the neuron is valid only when netj′ (t) > Tj. After simplification, the neuron model
can become:
oj = f (netj) = f (

## W T

j X)

(12)
Classroom instructional level assessment index itself has a guiding role in teaching, that is, what indicators are
assessd, teachers will lay stress on what indicators30. Therefore, the establishment and selection of indicators
is extremely important. In China, there is no strict definition of assessment index system, which is generally
Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

formulated by the academic affairs department of the school. In order to supplement the training data, the data
with different labels are extracted separately, and each feature data is randomly extracted from the data set with
the same label to form a new data set, and these data are added to the original data. Result analysis and disussion
Experimental environment
In order to study the performance of the improved BP assessment model in music instructional quality
assessment, this section designs a comparative experiment. Table 1 shows the specific configurations of the
experimental environment, which ensure the stability of the experiment and the reproducibility of the results. First of all, a large number of teaching data are widely collected from online music courses in many
universities, including teaching videos, teaching PPT, student interaction records and after-class feedback. In order to ensure the quality and consistency of data, these data are carefully preprocessed, including data
cleaning, format conversion and standardization. After data preprocessing, the data set is divided into training set and test set, in which 70% of the data is used
to train the BP neural network model and the remaining 30% is used to test the performance of the model. In the
process of model training, the parameters of the model, such as learning rate, iteration times and the number of
hidden layer nodes, are constantly adjusted to find the best model configuration. In addition, in order to further improve the validity of the data and the training efficiency of the model,
the features are selected and optimized to ensure that the data input into the model can accurately reflect the
instructional quality of the online music classroom. Through these detailed data processing and model training
steps, it has laid a solid foundation for building a high-quality online music classroom instructional quality
assessment system. In order to evaluate the performance of BPNN more comprehensively, ID3 algorithm is chosen as the
comparison algorithm. As a classic decision tree algorithm, ID3 algorithm has a certain application foundation
in music instructional quality assessment. By comparing the performance of BPNN and ID3 algorithm in terms
of accuracy and mean absolute error (MAE), the advantages and disadvantages of BPNN can be evaluated more
objectively. Analysis of experimental results
The complexity of music classroom system elements in universities and the aesthetics with literary appreciation
as the main content require evaluators to have the idea of classroom integrity assessment on the basis of
differentiating and refining classroom elements. In the stage of implementing the quantitative table of music
classroom assessment in universities, we should not only have the idea of overall classroom assessment, but also
lay stress on the qualitative embodiment of teaching and learning in the teaching stage, and attach importance
to qualitative as well as quantitative. In the traditional instructional level assessment system, we often encounter
the problem that the assessment subject is too single and the assessment is always not comprehensive enough. In order to test the performance of the improved BP assessment model, a simulation experiment was carried
out on the platform of Matlab. Different algorithms are applied to predict the assessment results in the sample
data of music online classroom teaching test, and then compared with the actual results, and the comparison
results are shown in Fig. 3. When doing data analysis and processing, the samples involved often contain multiple variables, and more
variables will bring complexity to the analysis problem. Teachers should lay stress on the effectiveness of their
own teaching while developing and integrating teaching resources, constantly update and expand resources
according to the characteristics of majors, industries and frontier hotspots of disciplines, guide students to
actively use online instruction resources for learning, enrich students’ learning experience, and further improve
the efficiency of online classroom teaching. For different assessment objects, we should adopt an assessment index system with different contents. The
assessment algorithm in this article is compared with ID3 algorithm, and the result is shown in Fig. 4. The results showed that the prediction accuracy of this method was significantly higher than that of
traditional teaching assessment models, with an accuracy rate of over 95%, and the recognition accuracy of
key teaching elements reached 96.8%. The comprehensive logical analysis of the elements of music classroom
teaching in universities includes more than 30 different teaching variables, which is the basic basis for assessing
the quality of classroom teaching. From the perspective of information theory, in the information system of
classroom teaching activities, teachers act as carriers of information and continuously transmit knowledge,
language, ideological, and psychological information to students through an average of five different channels
and methods. At this stage of communication, the teaching level, teaching and research achievements, teaching
Category
Model/version
Processor
Intel Core i7
Memory

## 32GB DDR4

Storage

## 1 TB SSD

Operat ing system
Windows 10 Professional
Programming environment
MATLAB R2022a
Table 1. Experimental environment. Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

style, and even their personality and emotions of teachers play a key role in directly determining the overall
quality of classroom teaching. The comparative analysis between the mean absolute error (MAE) of the assessment algorithm proposed in
this article and the ID3 algorithm is shown in Fig. 5, revealing a significant improvement in accuracy when using
the proposed method. In order to verify the reliability and stability of the prediction results of BPNN model, the
experimental results are further statistically analyzed. The specific method is to evaluate the performance of the
model by cross-validation method and calculate the confidence interval of the prediction results. Experiments
show that the prediction accuracy of the BPNN model is in the range of [93.7%, 96.4%], with an average of
95.2% and a standard deviation of 1.2% at 95% confidence level. In addition, with Shapiro–Wilk test, the normal
distribution of prediction error is verified (p > 0.05), which further supports the robustness of the results. Specifically, the error rate was significantly reduced by 20.69%, and compared to the 0.040 of the ID3 based
Fig. 5. Assessment of MAE comparison. Fig. 4. Comparison of assessment accuracy. Fig. 3. Comparison between predicted results and actual results. Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

model, our proposed method has a MAE of 0.032. The significant reduction of such errors emphasizes the higher
accuracy of assessing online music classroom teaching, which is crucial for ensuring the quality and effectiveness
of music education, especially in improving student learning outcomes, with an average increase of 15%, as
demonstrated by our empirical research results. The construction of an online music classroom instructional level assessment system, as described in this
article, not only enhances the monitoring capabilities of music teaching but also elevates the level of information
monitoring and summary abilities within the field. By utilizing advanced techniques like the BPNN, the system
can provide a more comprehensive and accurate assessment of teaching performance. This, in turn, enables
educators and administrators to make informed decisions regarding teaching strategies, resource allocation, and
areas for improvement. Furthermore, the enhanced monitoring level of music teaching facilitated by this system promotes a culture
of continuous improvement and excellence in education. By regularly assessing and adjusting teaching practices
based on objective data, educators can ensure that students receive the highest quality of music education
possible. Although the objectives of music education in universities are multifaceted, its humanistic aim stands out as
the foremost priority, reflecting the current consensus within the field of music instruction. Whether teachers
can integrate teaching materials and arrange instructional contents from the height of leading students’ spiritual
growth has become an important dynamic standard for classroom instructional assessment. The test results of
the instructional assessment model based on ID3 algorithm are shown in Fig. 6. The test results using the BPNN
instructional assessment model are shown in Fig. 7. It can be analyzed that the music instructional level assessment model based on BPNN is better than
ID3 algorithm in both accuracy and efficiency. Using BPNN to establish the assessment model of classroom
instructional level opens up a brand-new method for the reasonable assessment of classroom instructional level,
thus providing useful reference value for the research of instructional level assessment. Discussion
This study verifies the application effect of the improved BP assessment model in the assessment of music
classroom teaching in universities through experiments. The results show that the model is superior in both
prediction accuracy and error rate. Compared with the traditional ID3 algorithm, the model has higher accuracy
and lower error rate. This discovery is of great significance for improving the instructional quality monitoring
and assessment of music classes in universities. Fig. 7. Scatter plot of actual value and predicted value of BPNN. Fig. 6. Scatter plot of actual value and predicted value of ID3 algorithm. Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

From the comparison between the predicted results and the actual results, we can see that the BP assessment
model can predict the assessment results of music classroom teaching more accurately. This advantage is mainly
due to the strong learning and generalization ability of BPNN, which can effectively capture the nonlinear
relationship in teaching assessment, thus providing more accurate prediction in the complex and changeable
classroom teaching environment. By comparing the accuracy of ID3 algorithm and BPNN teaching assessment model, it is found that BPNN
model has higher accuracy. This shows that BPNN has stronger processing ability when dealing with teaching
assessment data with multiple variables and complex relationships. This is especially important for music teaching
in universities, because music teaching involves many factors, including teachers’ teaching level, teaching style,
teaching content and students’ feedback, which all affect the final instructional quality. By comparing the MAE of the two algorithms, it is found that the error rate of BPNN model is obviously
lower than that of ID3 algorithm. This further proves the superiority of BPNN model in music classroom
teaching assessment. Reducing the error rate is very important to ensure the objectivity and fairness of teaching
assessment, which helps to reflect the teaching level of teachers and the learning effect of students more accurately. In addition, this study also emphasizes the importance of combining qualitative and quantitative assessment. In the assessment of music classroom in universities, we should not only pay attention to quantifiable indicators,
such as students’ test scores and teachers’ class hours, but also pay attention to those factors that are difficult
to quantify, such as teachers’ teaching style, classroom atmosphere and students’ learning attitude. This
comprehensive assessment method can reflect the instructional quality of music classroom more comprehensively
and provide more valuable feedback for improving teaching. The reason why BPNN model can surpass ID3 algorithm in prediction accuracy and error rate is mainly due
to its strong self-learning and adaptive ability. BPNN can continuously optimize the network weight through the
back propagation algorithm, so as to capture the complex patterns and relationships in the data more accurately. In addition, the multi-layer structure of BPNN enables it to handle higher-dimensional data, which further
improves its performance in the task of assessing the quality of music classroom teaching. It is worth noting that although this study has verified the effectiveness of BPNN model in music teaching
assessment, other factors should be considered in practical application. For example, the differences of music
teaching ideas, teaching resources and student groups in different universities may affect the results of teaching
assessment. Therefore, when applying the BPNN model, it needs to be adjusted and optimized according to the
specific situation. To sum up, this study verified the superiority of BP assessment model in the assessment of music classroom
teaching in universities through experiments, and provided a new perspective and method for improving
instructional quality. Although some achievements have been made in this study, there are still some limitations. First of all, there may be potential bias in the data set, because the data mainly comes from specific universities,
which may affect the generalization ability of the model. Secondly, the results of this study may not be fully
applicable to all educational environments, because there may be differences in teaching models and resource
allocation in different schools and regions. Therefore, in the future research, we will focus on collecting more
diverse data and explore how to improve the generalization performance of the model. Conclusions
With the ongoing evolution and expansion of music teaching reforms in universities, novel challenges have
arisen within music classrooms, necessitating the development of updated classroom assessment criteria to
ensure standardization and guide practice. Online classroom instruction assessment plays a critical role in
enhancing students’ online learning experiences and elevating teachers’ online instruction proficiency. The integration of modern technologies in refining the assessment phase of music education and forging
an intelligent music instruction assessment model is crucial for realizing smart music teaching practices. Instructional assessment provides invaluable insights and a solid scientific foundation for elevating teaching and
instruction standards, with a robust assessment system serving as a pivotal backbone for educational success. Our findings demonstrate that, compared to the instructional assessment model based on the ID3 algorithm,
our method reduces error by a significant 20.69%. The establishment of an online music classroom instruction
level assessment system has the potential to significantly enhance the monitoring capabilities of music education,
improving information tracking and summarization within the field. The music instruction assessment model leveraging BPNN proves superior to the ID3 algorithm in terms of
both precision and efficiency. Through these assessment outcomes, university music educators can gain a deeper
understanding of their students’ realities, identify prevalent issues in teaching, and subsequently reflect on and
refine their instructional strategies and methods. In conclusion, this article introduces the application of BPNN in assessing online music classroom instruction
levels, addressing the nonlinear complexities of assessment and effectively overcoming the limitations inherent
in traditional assessment techniques. The utilization of BPNN in constructing the classroom instruction level
assessment model paves the way for a novel approach in objectively assessing classroom instruction quality,
offering valuable insights for future research in instruction level assessment. Data availability
The datasets used and/or analyzed during the current study are available from the corresponding author Runze
Ouyang on reasonable request via e-mail 526,629,608@qq.com. Received: 1 November 2024; Accepted: 14 April 2025
Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

References

### 1. Groenier, M., Brummer, L. & Bunting, B. P. Reliability of observational assessment methods for outcome-based assessment of

surgical skill: Systematic review and meta-analyses. J. Surg. Educ. 77(1), 189–201 (2020).

### 2. Huang, W. Simulation of English instructional quality assessment model based on gaussian process machine learning. J. Intell. Fuzzy Syst. 40(2), 2373–2383 (2021).

### 3. Wanderley, C. Oral cultures and multilingualism in a world of big digital data: The case of Portuguese speaking countries. Educ. Inf. 34(3), 239–254 (2018).

### 4. Zhang, Y. Interactive intelligent teaching and automatic composition scoring system based on linear regression machine learning

algorithm. J. Intell. Fuzzy Syst. 40(2), 2069–2081 (2021).

### 5. Qian, R., Sengan, S. & Juneja, S. English language teaching based on big data analytics in augmentative and alternative

communication system. Int. J. Speech Technol. 25(2), 409–420 (2022).

### 6. Yu, H. Online instructional quality assessment based on emotion recognition and improved AprioriTid algorithm. J. Intell. Fuzzy

Syst. 40(5), 1–11 (2020).

### 7. Lu, C., He, B. & Zhang, R. Assessment of English interpretation instructional quality based on GA optimized RBF neural network. J. Intell. Fuzzy Syst. 40(2), 3185–3192 (2021).

### 8. Coral, M. A. & Bernuy, A. E. Challenges in the digital transformation processes in higher education institutions and universities. Int. J. Inform. Technol. Syst. Approach (IJITSA) 15(1), 1–14 (2022).

### 9. Shu, Y. & Xu, G. H. Retraction Note: Multi-level Dynamic Fuzzy Evaluation and BP Neural Network Method for Performance

Evaluation of Chinese Private Enterprises. Wireless Pers. Commun. 128(1), 749–749 (2023).

### 10. Yan, B. et al. A Case Study for Software Quality Evaluation Based on SCT Model With BP Neural Network. IEEE Access 8, 56403–

56414 (2020).

### 11. Zhang, J., Gao, P. & Fang, F. An ATPSO-BP neural network modeling and its application in mechanical property prediction. Comput. Mater. Sci. 163, 262–266 (2019).

### 12. Ye, H. W. & Wen, X. J. Classification of speech based on bp neural network optimized by PSO. J. Comput. (Taiwan) 29(4), 269–276

(2018).

### 13. Li, X. Characteristics and rules of university English education based on cognitive process simulation. Cogn. Syst. Res. 57(10),

11–19 (2019).

### 14. Goodrich, A. Counterpoint in the music classroom: Creating an environment of resilience with peer mentoring and LGBTQIA+

students. Int. J. Music. Educ. 38(4), 582–592. https://doi.org/10.1177/0255761420949373 (2020).

### 15. Zhu, Q. Research on an online teaching platform for university music course based on internet of things technology. Int. J. Inf. Commun. Technol. 23(1), 1–14 (2023).

### 16. Palazón, J. & Giráldez, A. QR codes for instrumental performance in the music classroom. Int. J. Music. Educ. 36(3), 447–459

(2018).

### 17. Richerme, L. K. Equity via relations of equality: Bridging the classroom-society divide. Int. J. Music. Educ. 39(4), 492–503. ​h​t​t​p​s​:​/​/​

d​o​i​.​o​r​g​/​1​0​.​1​1​7​7​/​0​2​5​5​7​6​1​4​2​1​1​0​0​5​8​9​9​ (2021).

### 18. Cagirgan, G. The opinions of the preservice music teachers regarding the teaching of orchestra and chamber music courses during

distance education process. Cypriot J. Educ. Sci. 16(3), 1088–1096. https://doi.org/10.18844/cjes.v16i3.5827 (2021).

### 19. Daradkeh, M. Organizational adoption of sentiment analytics in social media networks: Insights from a systematic literature

review. Int. J. Inform. Technol. Syst. Approach (IJITSA) 15(2), 1–29 (2022).

### 20. Jiang, H. & Cheong, K. W. Developing teaching strategies for rural school pupils’ concentration in the distance music classroom. Educ. Inf. Technol. 29, 5903–5920. https://doi.org/10.1007/s10639-023-12056-1 (2024).

### 21. Zhang, P., Thilak, K. D. & Ravi, R. V. Big data analytics and augmentative and alternative communication in EFL teaching. Int. J. Speech Technol. 25(2), 315–329 (2022).

### 22. Wang, Y. A comprehensive assessment system of instructional quality based on big data architecture. Int. J. Cont. Eng. Educ. Life

Long Learn. 30(2), 176–189 (2020).

### 23. Wen, M. Interactive online classes in music education: The impact of online technologies on the level of creative thinking of

students. Curr. Psychol. 43, 13619–13629. https://doi.org/10.1007/s12144-023-05411-5 (2024).

### 24. Boettger, R. K. & Ishizaki, S. Introduction to the special issue: Data-driven approaches to research and teaching in professional and

technical communication. IEEE Trans. Profess. Commun. 61(4), 352–355 (2018).

### 25. Khussainova, G. A., Akparova, G. & Chsherbotayeva, N. Professional innovation policy in the system of higher music education in

the republic of kazakhstan. Eur. Online J. Nat. Soc. Sci. 7, 202–213 (2018).

### 26. Tejada, J., Thayer, T. & Arenas, M. In-service music teaching performance of Chilean generalist teachers: a mixed methods

exploratory study. Didacticae 7(7), 30–56 (2020).

### 27. Potter, J. Preservice elementary teachers and music in the elementary classroom. Update: Appl. Res. Music Educ. 41(1), 16–23

(2022).

### 28. Zhou, W. & Kim, Y. Innovative music education: An empirical assessment of ChatGPT-4’s impact on student learning experiences. Educ. Inf. Technol. https://doi.org/10.1007/s10639-024-12705-z (2024).

### 29. Cantabella, M., Martínez-Espaa, R. & Ayuso, B. Analysis of student behavior in learning management systems through a Big Data

framework. Future Gener. Comput. Syst. 90(8), 262–272 (2019).

### 30. Kumbhar, V. S. Impact of outcome-based education in Indian universities. Solid State Technol. 63(6), 16938–16943 (2020). Acknowledgements
Henan Higher Education Teaching Reform Research and Practice Project: The Dilemma and Countermeasures
of Online Quality Courses Construction in Henan Higher Vocational universities(2021SJGLX903)
Author contributions
Runze Ouyang: Conceptualization, methodology, software, validation, formal analysis, investigation, resources,
data curation, writing—original draft preparation, writing—review and editing, visualization, supervision, pro­
ject administration, funding acquisition. Declarations
Competing interests
The authors declare no competing interests. Ethical approval
The studies involving human participants were reviewed and approved by Academy of Music, Dance and Fine
Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/

Arts"Prof. Asen Diamandiev” Ethics Committee (Approval Number: 2022.6521000). The participants provided
their written informed consent to participate in this study. All methods were performed in accordance with
relevant guidelines and regulations. Additional information
Correspondence and requests for materials should be addressed to R. O. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:14250

| https://doi.org/10.1038/s41598-025-98556-1
www.nature.com/scientificreports/
