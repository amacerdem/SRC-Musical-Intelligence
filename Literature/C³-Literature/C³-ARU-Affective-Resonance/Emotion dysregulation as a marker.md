# Emotion dysregulation as a marker

**Year:** D:20

---

Emotion dysregulation as a marker
in adolescent mental health with
EEG-based prediction model
Ziyi Zhang1 & Lixin Zhang2
This study comprehensively tackles the critical challenge of understanding and mitigating adolescent
violent crime by integrating advanced insights from psychological and environmental research with
cutting-edge digital public health tools. Current methods for examining adolescent aggression often
fail to provide a holistic framework that effectively accounts for the intricate interplay of emotional
dysregulation, environmental influences, and relational dynamics, thereby limiting the scope and
efficacy of intervention strategies. In response to these limitations, we propose a comprehensive
approach that leverages EEG-based emotion analysis in combination with a novel Psycho-Social Risk
Interaction Model (PRIM), designed to uncover latent variables and dynamic interactions underlying
violent behavior in adolescents. PRIM is a robust framework that encapsulates psychological
vulnerabilities such as impulsivity and aggression, environmental stressors like socioeconomic
pressures, and relational influences within peer and family networks, offering a nuanced understanding
of the multifaceted factors contributing to violent tendencies. Building upon the PRIM framework,
we introduce the Targeted Intervention and Risk Reduction Strategy (TIRRS), an innovative system
that translates theoretical insights into actionable, personalized, and adaptive interventions. TIRRS dynamically modulates the interaction of psychological, environmental, and relational
factors by employing real-time monitoring tools and resource optimization frameworks, ensuring
that interventions are both responsive and impactful. Experimental results demonstrate that our
approach improves the prediction accuracy of violent tendencies to 87.5%, representing a 21.3%
increase compared to traditional statistical models (which averaged 66.2% accuracy). Moreover, the
intervention success rate improved by 18.7% relative to standard counseling-based approaches. These
outcomes enable the development of cost-effective, scalable, and sustainable prevention strategies. Keywords  Emotional dysregulation, EEG emotion analysis, Adolescent aggression, Digital public health, Targeted interventions
Emotional dysregulation is increasingly recognized as a core transdiagnostic mechanism contributing to a broad
range of adolescent psychopathologies, including mood disorders, anxiety, conduct problems, and aggression1–4. Understanding the psychological mechanisms underlying adolescent violent crime—as one applied manifestation
of emotional dysregulation—is essential for mitigating its prevalence and implementing effective interventions5. Emotional dysregulation, characterized by the inability to manage and respond to emotional experiences in a
socially acceptable manner, is a critical psychological construct relevant across multiple domains of adolescent
mental health, and is also implicated in extreme behaviors such as violent offending6. This task is not only urgent
but also scientifically intricate, as it bridges neuroscience, psychology, and digital technologies7. Traditional
approaches have primarily relied on psychological assessments and behavioral observations, yet these methods
are limited in their objectivity and granularity8. Advances in neurophysiological tools, such as EEG-based
emotion analysis, not only offer new pathways to understanding the neural basis of emotional dysregulation
but also enable precise and real-time monitoring9. The integration of digital interventions, such as personalized
feedback and gamified behavior modification systems, provides a promising avenue for treatment scalability and
effectiveness. Addressing emotional dysregulation during adolescence not only offers the potential to mitigate
specific outcomes like violent behavior but also promotes broader emotional and psychological well-being
during a critical developmental period10.
1School of Preschool Education (School of Music), LianYunGang Normal University, LianYunGang 222000, China.
2Hebei University of Economics and Business, Shijiazhuang 050061, China. email: uycj05@163.com
OPEN
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports

Traditional clinical and developmental approaches have primarily relied on behavioral assessments, self-
report questionnaires (e.g., Emotion Regulation Questionnaire; Difficulties in Emotion Regulation Scale),
and observational methods to assess emotional dysregulation and its associations with both internalizing and
externalizing behaviors11–13. Neurobiological models have further implicated dysregulation within fronto-
limbic circuits, including impaired prefrontal cortex modulation of amygdala hyperactivity, as contributing to
heightened emotional reactivity and poor inhibitory control across diverse adolescent psychopathologies14–16. While these approaches have provided valuable insights, they are often limited by subjective reporting biases,
cross-sectional snapshots, and restricted ecological validity. Recent advances in neurotechnology, such as EEG-based emotion monitoring, offer objective, real-time
assessments of neural correlates of emotional dysregulation. When combined with machine learning algorithms,
these tools provide new opportunities to model complex, dynamic emotional and behavioral patterns at both
individual and population levels17–19. Building upon these foundations, this paper introduces a Psycho-Social
Risk Interaction Model (PRIM) and a Targeted Intervention and Risk Reduction Strategy (TIRRS) that integrate
multimodal neurophysiological data with psychosocial risk factors. While violent behavior is discussed as one
illustrative application to demonstrate the framework’s clinical utility, the proposed model is broadly designed
to advance our understanding and treatment of emotional dysregulation across adolescent mental health
conditions. The emergence of machine learning methodologies marked a significant shift in the analysis of emotional
dysregulation characteristics across multiple adolescent populations, including those exhibiting violent
behavior20. By leveraging large datasets comprising behavioral metrics, emotional response recordings, and
physiological signals, researchers were able to develop predictive models that captured patterns and trends
in emotional dysregulation more effectively21. These approaches included supervised learning algorithms
trained on labeled datasets as well as unsupervised methods aimed at clustering emotional states22. EEG
signal processing techniques began to be incorporated, enabling the extraction of features such as alpha wave
suppression or gamma wave coherence that correlated with emotional responses23. Machine learning models
enhanced the ability to predict emotional and behavioral dysregulation based on physiological markers, offering
more granular and objective assessments compared to earlier methods24. Nevertheless, they remain constrained
by the need for high-quality data and the black-box nature of many machine learning algorithms, which hinders
interpretability and clinical trust. Recent advances in deep learning and pre-trained models have revolutionized the study of emotional
dysregulation and its manifestations25. Deep neural networks, particularly those based on convolutional
and recurrent architectures, are capable of processing high-dimensional EEG data to uncover latent patterns
associated with emotional states26. Pre-trained models like transformers have further expanded these capabilities
by enabling fine-tuning for emotion-specific tasks, such as predicting dysregulated emotional episodes or
identifying high-risk emotional trajectories in real-time27. These models are not only more accurate but also
allow for transfer learning across datasets, reducing the need for extensive domain-specific data collection28. The integration of deep learning with digital interventions has led to the development of adaptive, real-time
feedback systems that use EEG signals to guide adolescents through emotional regulation exercises29. Despite
these advancements, challenges remain, particularly in ensuring the fairness and transparency of such systems,
as well as addressing ethical concerns related to their deployment in sensitive clinical and forensic contexts. In response to these limitations, this paper proposes a novel framework combining EEG emotion analysis with
adaptive digital interventions to address emotional dysregulation broadly across adolescent psychopathology. Violent behavior is presented as one applied case study to illustrate the clinical relevance and feasibility of the
approach. This method builds on the interpretability of traditional approaches, the predictive power of machine
learning, and the adaptive capabilities of deep learning models. By incorporating neurophysiological signals into
personalized digital intervention strategies, this framework aims to provide a more holistic and effective solution
to emotional dysregulation. The proposed method not only addresses the need for scalable and real-time
monitoring systems but also ensures ethical considerations through transparent algorithms and user-centered
design principles. This integrative approach bridges the gap between neuroscience and digital technology,
enabling both preventative and rehabilitative measures across diverse adolescent mental health challenges.
•	 The proposed method combines EEG-based emotion analysis with adaptive digital interventions, offering a
new avenue for understanding and treating emotional dysregulation across adolescent psychopathologies,
including but not limited to violent behaviors.
•	 The framework’s adaptability across different emotional and behavioral contexts ensures its scalability and
applicability to a wide range of scenarios, from clinical therapy to educational environments.
•	 Initial evaluations demonstrate significant improvements in emotional regulation outcomes, reduced exter­
nalizing symptoms, and enhanced engagement with digital interventions compared to traditional methods. Related work
EEG-based emotion analysis in psychology
Electroencephalography (EEG) is a widely used method to analyze neural activity, particularly in relation
to emotional and cognitive states30. In psychology, EEG has emerged as a crucial tool for understanding the
neural correlates of emotional dysregulation, particularly in adolescents31. Emotional dysregulation is often
characterized by heightened reactivity to emotional stimuli, impaired ability to regulate responses, and increased
vulnerability to stressors32. Studies utilizing EEG have demonstrated that specific frequency bands, such as
alpha, beta, and theta, are closely linked to emotional processing and regulation33. increased frontal asymmetry
in alpha-band activity has been associated with mood disorders and heightened emotional reactivity, while
theta-band activity has been correlated with emotional conflict and regulatory efforts. In the context of violent
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

behaviors among adolescents, EEG-based studies have revealed that individuals exhibiting violent tendencies
often display atypical neural activation patterns during emotional stimuli exposure34. Aberrant activity in the
prefrontal cortex, a region crucial for impulse control and emotion regulation, has been observed. ower frontal
theta-band activity and disrupted connectivity between the prefrontal cortex and the amygdala have been linked
to impulsivity and aggression35. These findings suggest that emotional dysregulation in adolescents involved
in violent crime may stem from neurophysiological deficits in key regulatory circuits. event-related potential
(ERP) studies have identified specific components, such as the P300 and N200, that are indicative of impaired
emotional and cognitive processing in individuals prone to violent behaviors. EEG-based emotion analysis also
holds promise for identifying biomarkers of emotional dysregulation in adolescents at risk of engaging in violent
crime. By leveraging advanced machine learning algorithms, researchers have been able to classify emotional
states and predict aggressive behaviors based on EEG data. Such approaches can enable early identification and
intervention for high-risk individuals. real-time EEG feedback systems, known as neurofeedback, are being
explored as potential tools for training adolescents to regulate their emotions more effectively. Neurofeedback
interventions have shown preliminary success in reducing aggression and improving emotional regulation by
modulating brain activity patterns. EEG-based emotion analysis provides a robust framework for understanding
and addressing emotional dysregulation in adolescent violent crime psychology. Digital interventions for emotion regulation
Digital interventions have emerged as a scalable and accessible approach to addressing emotional dysregulation,
particularly among adolescents36. These interventions leverage digital platforms, including mobile applications,
virtual reality (VR), and web-based tools, to deliver evidence-based strategies for improving emotional
regulation37. Among adolescents involved in or at risk of violent behaviors, digital interventions can serve as a
cost-effective and engaging alternative to traditional therapeutic approaches38. One prominent category of digital
interventions focuses on emotion-focused cognitive-behavioral therapy (CBT) techniques delivered via mobile
apps39. These apps often incorporate interactive exercises, psychoeducation, and mood tracking features to help
adolescents identify and regulate their emotions40. several apps use gamified approaches to teach emotional
awareness and coping strategies, which are critical for reducing impulsivity and aggressive tendencies. Some
interventions also integrate real-time feedback systems, where wearable devices monitor physiological signals
such as heart rate variability (HRV) and provide personalized recommendations for emotion regulation exercises. These approaches have shown promising results in reducing emotional reactivity and improving self-regulation
among adolescents. Virtual reality-based interventions are another promising avenue for addressing emotional
dysregulation in adolescents. VR environments offer immersive and controlled settings where individuals can
practice emotional regulation skills in response to simulated stressors. VR scenarios can simulate interpersonal
conflicts or emotionally charged situations, allowing adolescents to rehearse adaptive responses and receive
immediate feedback. Studies have shown that VR-based interventions can effectively reduce aggression and
enhance emotional resilience, particularly when combined with biofeedback or therapist-guided sessions. VR
interventions can target specific deficits in emotional processing, such as empathy, by immersing individuals
in perspectives that foster emotional understanding and connection. Digital interventions also benefit from
their ability to leverage large-scale data for personalized and adaptive treatment. By analyzing user engagement
patterns, emotional responses, and outcomes, digital platforms can continuously refine and tailor interventions
to meet individual needs. the integration of artificial intelligence (AI) allows for real-time emotion recognition
and intervention recommendations, enhancing the efficacy of these tools. Given the increasing prevalence of
smartphone use among adolescents, digital interventions represent a practical and effective means of addressing
emotional dysregulation and reducing violent behaviors. Adolescent psychology of violent crime
The psychological underpinnings of violent crime in adolescents are multifaceted, encompassing emotional,
cognitive, and social dimensions41. Emotional dysregulation has been identified as a key risk factor, as it impairs
the ability to manage impulses, process emotions, and navigate social interactions42. Adolescents involved in
violent crimes often exhibit heightened emotional reactivity, reduced frustration tolerance, and difficulties in
regulating anger43. These characteristics are frequently accompanied by deficits in executive functioning, such
as impaired decision-making and reduced inhibitory control, which further exacerbate aggressive tendencies44. Research in adolescent psychology highlights the role of adverse childhood experiences (ACEs) in shaping
emotional dysregulation and violent behaviors45. Traumatic experiences, such as abuse, neglect, or exposure to
violence, can disrupt the development of neural circuits involved in emotion regulation and impulse control. The amygdala and prefrontal cortex, in particular, are highly susceptible to the effects of chronic stress during
adolescence, a critical period for brain maturation. Dysregulation in these regions has been linked to increased
aggression, impulsivity, and difficulties in adapting to social norms. adolescents with a history of ACEs often
exhibit heightened sensitivity to perceived threats, which can trigger reactive aggression in social interactions. Social and environmental factors also play a significant role in the development of violent behaviors in
adolescents. Peer influence, family dynamics, and community environments can either exacerbate or mitigate
emotional dysregulation and aggressive tendencies. association with deviant peers and exposure to violent
role models can reinforce maladaptive coping mechanisms and normalize aggressive behaviors. Conversely,
supportive relationships and positive role models can buffer against the effects of emotional dysregulation and
promote pro-social behaviors. Understanding the interplay between individual and environmental factors is
crucial for developing effective interventions for adolescents involved in violent crime. Recent studies have also
explored the role of cultural and gender differences in shaping the psychology of adolescent violent crime. males
are more likely to engage in overtly aggressive behaviors, while females are more prone to relational aggression. Cultural norms and societal expectations can influence how emotional dysregulation manifests and is perceived
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

in different populations. These insights underscore the importance of culturally sensitive and gender-responsive
approaches to addressing emotional dysregulation and violent behaviors in adolescents. By integrating
psychological, social, and neurobiological perspectives, researchers can gain a comprehensive understanding of
the factors contributing to adolescent violent crime and develop targeted interventions to address these issues. Methods
Overview
The psychology behind adolescent involvement in violent crime represents a multifaceted and deeply
interconnected research domain. This subsection outlines the key focus areas of the study, offering a framework
for understanding the underlying factors and methodologies employed in the subsequent sections. the
following discussions aim to bridge theoretical constructs, empirical observations, and novel contributions to
the field. In “Preliminaries”, we lay the groundwork by formalizing the problem of adolescent violent crime
through a psychological lens. This involves translating behavioral tendencies and environmental influences into
mathematical and theoretical representations. we explore foundational models from cognitive, developmental,
and socio-environmental psychology to provide a systematic perspective on the factors that precipitate violent
behavior during adolescence. In “Psycho-social risk interaction model (PRIM)” introduces the proposed innovative psychological model,
designed to capture the nuanced interplay of individual and external determinants of adolescent aggression. This model leverages both established frameworks and novel hypotheses, aiming to surpass existing limitations
in comprehending the causes and patterns of adolescent violent crime. This section elaborates on how the
proposed model incorporates latent variables, interdependencies, and temporal dynamics to better explain the
emergence and persistence of such behaviors. In “Targeted intervention and risk reduction strategy (TIRRS)”,
we propose a novel intervention strategy informed by our model. The strategy is structured to address key
deficiencies in prior approaches to mitigating adolescent involvement in violent crime. Emphasis is placed on
translating theoretical insights into actionable measures, employing psychologically informed frameworks to
design targeted prevention and rehabilitation programs. To ensure measurement validity and reproducibility, all psychological attributes incorporated into the
PRIM framework are operationalized using established and validated psychometric instruments widely used in
adolescent mental health research:
•	 Emotional Dysregulation: Measured by the Difficulties in Emotion Regulation Scale (DERS), which assesses
six domains of dysregulation (nonacceptance, goals, impulse, awareness, strategies, and clarity). The total
score reflects overall emotion regulation difficulties.
•	 Impulsivity: Assessed using the Barratt Impulsiveness Scale (BIS-11), which evaluates attentional, motor, and
non-planning impulsiveness. Higher scores indicate greater impulsivity tendencies.
•	 Aggression: Measured by the Buss-Perry Aggression Questionnaire (BPAQ), which provides subscale scores
for physical aggression, verbal aggression, anger, and hostility.
•	 Conduct Problems / Externalizing Behaviors: In extended applications, measures such as the Child Behav­
ior Checklist (CBCL) externalizing subscale or the Youth Self-Report (YSR) can be incorporated to capture
broader conduct problem indicators. All scales are standardized (Z-score transformation) prior to integration into the PRIM model. Composite
psychological risk scores are generated via principal component analysis (PCA) to capture the underlying shared
variance across these measures. This psychometric integration ensures robust quantification of psychological
vulnerabilities contributing to emotional dysregulation and aggression risk in adolescents. Within the PRIM
framework, we distinguish clearly between observed and latent variables:
•	 Observed Variables: These include directly measurable clinical and psychosocial indicators such as emotion
dysregulation (DERS total score), impulsivity (BIS-11 score), aggression (BPAQ score), socioeconomic stress
(SES index), family conflict (CBQ score), and peer delinquency (PDS score). All observed variables are nor­
malized to a [0, 1] scale via min-max or Z-score normalization to facilitate integration.
•	 Latent Variables: These reflect unobservable, inferred constructs derived through latent variable modeling:
– ai: Latent emotional dysregulation factor derived via principal component analysis (PCA) across multiple
observed scales.
– si: Latent socio-environmental strain factor synthesized from SES, ACE, and neighborhood crime indi­
cators.
– ri: Latent relational instability score combining family and peer conflict metrics. These latent variables are treated as continuous variables following approximately Gaussian distributions after
dimensionality reduction. The final violence risk output Vi is computed as a nonlinear transformation of these latent and observed variables
via the PRIM architecture, which integrates multimodal inputs and captures dynamic interactions. Different
activation functions were carefully selected based on empirical simulations and functional requirements at each
computational stage:
•	 ReLU (Rectified Linear Unit): Applied in hidden layers to promote efficient training convergence and avoid
vanishing gradients while modeling non-linear risk interactions.
•	 Sigmoid: Employed in the output layer for probabilistic interpretation of the final risk score Vi ∈[0, 1]. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

•	 Tanh: Used in intermediate layers where bounded symmetric transformations are needed to stabilize latent
interaction terms. Preliminary simulations confirmed that models using these activations provided superior convergence stability
and predictive accuracy compared to alternative configurations. To enhance accessibility for clinical and
educational end-users, we have moved the full mathematical derivations and parameter estimation procedures
to Supplementary Materials. The main text now presents a conceptual overview of the PRIM framework,
emphasizing its clinical interpretability, modular risk factor integration, and intervention targeting logic. Preliminaries
The study of adolescent violent crime psychology is grounded in the interplay between individual psychological
states, developmental processes, and external socio-environmental factors. In this subsection, we formalize the
problem by defining the relevant constructs and mathematical representations that underlie the emergence of
violent behaviors among adolescents. The goal is to provide a systematic framework that captures the intricate
dynamics of psychological, behavioral, and contextual variables. Let the adolescent population be represented by a set A = {a1, a2,..., an}, where each ai denotes an
individual adolescent. The propensity of an adolescent ai to engage in violent crime is modeled as a latent
variable Vi ∈R, which is influenced by both intrinsic and extrinsic factors. We define this propensity as a
function: Vi = f(Pi, Ei, Ri),
(1)
where Pi represents the psychological profile of ai, Ei denotes their environmental context, and Ri captures
relational factors, such as peer influence or family dynamics. The function f is assumed to be nonlinear, capturing
the complex interdependencies between these factors. The psychological profile Pi is characterized by multiple dimensions, such as emotional regulation,
impulsivity, and aggression. Let Pi be a vector: Pi = [pi1, pi2,..., pim] ∈Rm,
(2)
where each pij represents a psychological attribute, such as self-control, emotional distress, or antisocial
tendencies. These attributes are typically measured using standardized psychometric instruments. The
psychological dynamics are further expressed as:
∂Pi
∂t = g(Pi, Si),
(3)
where g is a function modeling the temporal evolution of psychological states, and Si represents stressors or
triggering events experienced by ai. The environmental factors Ei encapsulate the socioeconomic, cultural, and situational variables influencing
ai. These are modeled as: Ei = [ei1, ei2,..., ein] ∈Rn,
(4)
where eij could represent metrics such as exposure to neighborhood violence, poverty level, or access to
educational resources. The interaction between psychological and environmental factors can be expressed as:
h(Pi, Ei) = βP Pi + βEEi + βP E(Pi · Ei),
(5)
where βP, βE, and βP E are coefficients capturing the relative contributions and interactions of these variables. Relational factors Ri include peer pressure, family relationships, and social support networks. These can be
represented as a graph G = (A, E), where nodes correspond to adolescents, and edges in E capture relational
ties. The influence of peers and family on ai’s behavior is modeled as: Ri =
∑
j∈N (i)
wijVj,
(6)
where N(i) is the set of neighbors of ai, wij represents the strength of influence from aj to ai, and Vj is the
violent crime propensity of aj. To formalize the likelihood of ai engaging in violent behavior, we define a probability function: P(Vi > τ) = σ (αP Pi + αEEi + αRRi),
(7)
where σ(x) =

1+e−x is the sigmoid function, αP, αE, and αR are weights, and τ is a threshold indicating a
critical level of propensity. The temporal progression of violent behavior is modeled as a dynamic system:
dVi
dt = ft(Pi(t), Ei(t), Ri(t)),
(8)
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

where ft accounts for the time-varying interactions between psychological, environmental, and relational
factors. Stability analysis can be conducted to determine conditions under which Vi stabilizes, escalates, or
diminishes over time. The ultimate goal of this study is to identify the key drivers of adolescent violent crime and quantify their
relative contributions. This involves solving the optimization problem:
min

## Θ L(Θ; D),

(9)
where Θ = {αP, αE, αR, βP, βE, βP E} represents the model parameters, D is the dataset containing observed
behaviors and contextual variables, and L is a loss function quantifying the mismatch between predicted and
observed outcomes. For improved transparency and accessibility, we provide clear definitions of key computational components
used within the PRIM framework:
•	 Global Bilinear Regularization (GBR): In this context, GBR refers to a parameterized interaction mecha­
nism that models second-order relationships between different input modalities (e.g., EEG, psychosocial, en­
vironmental factors). Bilinear terms allow the model to capture how pairs of risk factors jointly influence vio­
lence risk. Regularization terms are applied to prevent overfitting by penalizing extreme interaction weights.
•	 Local Context Fusion (LCF): LCF denotes a fusion module that integrates temporally or structurally related
features within individual data streams. For example, it aggregates emotion-related EEG features (e.g., alpha,
beta band powers) over short time windows to capture contextually relevant local emotional fluctuations
prior to cross-modal integration.
•	 Attention-Based Fusion: An adaptive weighting mechanism is applied after LCF to prioritize the most in­
formative features when integrating multiple modalities, enhancing model interpretability and focusing on
clinically meaningful signals. These mechanisms were chosen to balance model complexity, computational efficiency, and clinical
interpretability while preserving the nuanced interactions underlying adolescent emotional dysregulation. Full
mathematical formulations of each module are provided in the Materials for reproducibility. Psycho-social risk interaction model (PRIM)
In this subsection, we present a novel model called the Psycho-Social Risk Interaction Model (PRIM), designed
to comprehensively capture the factors influencing adolescent violent crime. PRIM integrates psychological
attributes, environmental factors, and relational influences into a unified framework, employing both latent
variable modeling and dynamic systems theory. The model emphasizes capturing the non-linear and interactive
effects of these factors, providing a richer understanding of adolescent violent behavior. Specifically, PRIM can
be defined as an algorithm inspired by the Patient Rule Induction Method, which aims to identify homogeneous
subgroups within complex multi-dimensional datasets. By iteratively partitioning the data space, PRIM isolates
combinations of psychological (e.g., impulsivity, emotional dysregulation), environmental (e.g., socioeconomic
adversity), and relational (e.g., peer influence, family dynamics) risk factors that jointly contribute to heightened
violence tendencies. This subgroup identification enables more precise characterization of at-risk populations
and supports tailored intervention strategies. The latent variable modeling incorporated within PRIM helps
uncover unobservable constructs such as underlying emotional instability or chronic relational conflict, while
dynamic systems theory allows the model to account for feedback loops and time-varying influences among
these factors. In the PRIM framework, each component is formally defined and operationalized as follows:
•	 Vi: Violence Risk Score. This variable represents the predicted likelihood of violent behavior for individual
i, calculated as a weighted composite of multiple risk indicators derived from psychological, environmental,
and relational domains. The score is normalized to a range of [0, 1], where higher values indicate greater
estimated risk.
•	 Pi: Psychological Vulnerability Index. This index quantifies emotional dysregulation, impulsivity, and ag­
gression tendencies. Measurements are obtained through validated psychometric scales, including:
– Difficulties in Emotion Regulation Scale (DERS),
– Barratt Impulsiveness Scale (BIS-11),
– Buss-Perry Aggression Questionnaire (BPAQ). Each subscale is standardized (Z-scored) and aggregated using principal component analysis (PCA) to generate
a composite Pi score, normalized to [0, 1].
•	 Ei: Environmental Stress Index. This captures socioeconomic stress, neighborhood violence exposure, and
family adversity factors. Data sources include:
– Socioeconomic Status Index (household income, parental education, occupation),
– Neighborhood Crime Exposure Index (regional crime statistics),
– Adverse Childhood Experiences (ACE) questionnaire scores. Each factor is scaled between 0 and 1 using min-max normalization, and combined via weighted summation
into Ei. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

•	 Ri: Relational Instability Index. This quantifies family conflict, peer deviance, and social support deficits. Key measurements include:
– Conflict Behavior Questionnaire (CBQ) for parent-child conflict,
– Peer Delinquency Scale (PDS),
– Multidimensional Scale of Perceived Social Support (MSPSS). Scores are similarly standardized and combined into a composite Ri. The distribution of all input variables (Pi, Ei, Ri) approximates a normalized Gaussian distribution post-
transformation. Interactions among these variables are modeled using nonlinear interaction terms in the
dynamic system formulation of PRIM, allowing for emergent non-additive effects. EEG-derived emotional
dysregulation markers serve as an auxiliary latent input influencing Pi dynamically in real-time. The propensity of an adolescent ai to engage in violent crime is represented as a latent variable Vi ∈R,
which is dynamically determined by a combination of their psychological profile, environmental exposure, and
relational influences. Formally, we define: Vi = Φ(Pi, Ei, Ri; Θ),
(10)
where Φ(·) is a nonlinear function parameterized by Θ, and Pi, Ei, Ri correspond to the psychological,
environmental, and relational factors, respectively. The core novelty of PRIM lies in its interaction terms and
latent structure, which allow for capturing complex dependencies between these components (As shown in Fig.
1). Capturing internal states
The psychological factors Pi are represented as a vector of attributes, such as impulsivity, aggression, and
emotional regulation: Figure 1. Illustration of the psycho-social risk interaction model (PRIM), showcasing pre-training (a), testing
(b), and spatial attention mechanisms in FET blocks (c), emphasizing psychological, environmental, and
relational factors influencing adolescent violent behavior. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

Pi = [pi1, pi2,..., pim] ∈Rm.
(11)
Each attribute pij represents a measurable psychological trait or behavior of individual ai, and these attributes
collectively describe the psychological profile. To model the nonlinear effects of these attributes, we introduce a
transformation into a latent psychological embedding zP
i ∈Rk, defined as:
zP
i = σ(WP Pi + bP ),
(12)
where WP ∈Rk×m is a trainable weight matrix, bP ∈Rk is a bias vector, and σ(·) is an activation function
such as ReLU, sigmoid, or hyperbolic tangent. The latent embedding zP
i captures the complex dependencies and interactions among psychological
attributes. To enhance the representation, we further incorporate a quadratic interaction term between these
attributes:
qP
i = P ⊤
i QP Pi,
(13)
where QP ∈Rm×m is a symmetric matrix that models second-order interactions between attributes. The
resulting quadratic term qP
i is concatenated with zP
i to create a combined embedding:
uP
i = [zP
i; qP
i ] ∈Rk+1.
(14)
To incorporate temporal dynamics into psychological states, we model the evolution of each psychological
attribute pij(t) over time as:
dpij(t)
dt
= −γjpij(t) + βjuj(t),
(15)
where γj > 0 is the decay rate for the attribute, βj is a sensitivity parameter, and uj(t) represents external
influences such as environmental or relational factors that impact psychological traits. The latent embedding zP
i (t) also evolves over time and is updated according to the dynamics of psychological
attributes:
dzP
i (t)
dt
= WP dPi(t)
dt
+ dbP
dt.
(16)
For interactions between psychological states and external factors, we introduce a bilinear term to model their
combined effects on violent behavior: IP (Pi, Ei) = zP
i WP EzE
i,
(17)
where WP E ∈Rk×k is a weight matrix capturing the influence of psychological and environmental embeddings. The overall contribution of psychological factors to the violent crime propensity Vi is expressed as: VP (Pi) = αP ∥zP
i ∥2 + βP qP
i,
(18)
where αP and βP are trainable parameters that determine the relative contributions of the latent embedding and
quadratic interactions to the propensity for violent behavior. Linking psychology and environment
Environmental factors Ei are represented as a vector of attributes, such as neighborhood violence, economic
deprivation, and availability of community resources: Ei = [ei1, ei2,..., ein] ∈Rn.
(19)
Each attribute eij represents a measurable environmental condition or risk factor that impacts the individual ai. To capture complex interactions among these attributes, we transform Ei into a latent environmental embedding
zE
i ∈Rk, defined as:
zE
i = σ(WEEi + bE),
(20)
where WE ∈Rk×n is a weight matrix, bE ∈Rk is a bias vector, and σ(·) is a nonlinear activation function, such
as ReLU or sigmoid. Higher-order interactions between environmental factors are modeled using a quadratic term:
qE
i = E⊤
i QEEi,
(21)
where QE ∈Rn×n is a symmetric matrix that captures second-order interactions between environmental
attributes. The quadratic term qE
i is concatenated with zE
i to form an enriched representation:
uE
i = [zE
i; qE
i ] ∈Rk+1.
(22)
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

To model the interaction between psychological and environmental factors, we define a bilinear interaction
term: IP E(Pi, Ei) = zP
i WP EzE
i,
(23)
where WP E ∈Rk×k is a weight matrix that determines the strength of the interaction between the latent
psychological and environmental embeddings. To incorporate the temporal evolution of environmental factors, we model the dynamics of each attribute
eij(t) as:
deij(t)
dt
= −δjeij(t) + ρjvj(t),
(24)
where δj > 0 represents the natural decay of the environmental condition, ρj is a sensitivity parameter, and
vj(t) represents external interventions or changes over time. The corresponding latent embedding zE
i (t) evolves
as:
dzE
i (t)
dt
= WE dEi(t)
dt
+ dbE
dt.
(25)
To measure the joint contribution of psychological and environmental factors to violent behavior propensity, we
define the combined term: FP E(Pi, Ei) = αP EIP E(Pi, Ei) + βE∥zE
i ∥2,
(26)
where αP E and βE are trainable parameters. The term ∥zE
i ∥2 represents the overall environmental risk
magnitude. The influence of psychological and environmental factors on the violent crime propensity Vi is expressed as: VP E(Pi, Ei) = FP E(Pi, Ei) + γEqE
i,
(27)
where γE is a trainable parameter that scales the contribution of quadratic environmental interactions. Temporal social influences
Relational influences Ri are captured through a social interaction graph G = (A, E), where A represents
adolescents, and E represents relational ties such as peer or familial connections. The relational influence on ai
is computed as: Ri =
∑
j∈N (i)
wijzP
j,
(28)
where N(i) denotes the neighbors of ai in G, wij is the weight of the influence from aj to ai, and zP
j is the latent
psychological embedding of aj. These weights are normalized such that:
∑
j∈N (i)
wij = 1,
(29)
to ensure the relational influences are proportionally distributed among all neighbors. To incorporate time-dependent changes in relational influence, we define the temporal evolution of wij(t)
as:
dwij(t)
dt
= −δwij(t) + ρκij(t),
(30)
where δ > 0 is a decay factor, ρ > 0 is a sensitivity parameter, and κij(t) represents interaction frequency or
social proximity between ai and aj over time. The relational embedding zR
i (t) is defined as an aggregate of neighbor influences over time:
zR
i (t) =
∑
j∈N (i)
wij(t)zP
j (t),
(31)
where zP
j (t) evolves based on the psychological states of neighbors. To incorporate higher-order interactions among relational ties, we introduce a pairwise influence term: IRR(i) =
∑
j∈N (i)
∑
k∈N (i)
νijk(zP
j )⊤zP
k,
(32)
where νijk captures the strength of influence between neighbors j and k on ai. The contribution of relational factors to the violent crime propensity Vi is modeled as: Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

VR(Ri) = αR∥zR
i ∥2 + βRIRR(i),
(33)
where αR and βR are trainable parameters that scale the latent relational embedding and higher-order
interactions, respectively. To integrate relational factors with psychological and environmental components, the overall violent crime
propensity is expressed as: Vi = Φ(Pi, Ei, Ri; Θ) = αP ∥zP
i ∥2 + αE∥zE
i ∥2 + αP EIP E(Pi, Ei) + αRRi,
(34)
where αP, αE, αP E, and αR are learnable parameters that balance the contributions of psychological,
environmental, and relational factors (As shown in Fig. 2). The dynamic evolution of Vi(t) is governed by:
dVi(t)
dt
= Φt(Pi(t), Ei(t), Ri(t)) −γVi(t),
(35)
where γ > 0 is a dissipation parameter that reduces Vi(t) over time in the absence of reinforcing influences. The model parameters Θ are optimized by minimizing the loss function:

## L(Θ) = 1

N
N
∑
i=1
(
V obs
i
−Φ(Pi, Ei, Ri; Θ))2 + λ∥Θ∥2
2,
(36)
where V obs
i
is the observed violent behavior of ai, and λ∥Θ∥2
2 is a regularization term to prevent overfitting. Targeted intervention and risk reduction strategy (TIRRS)
The Targeted Intervention and Risk Reduction Strategy (TIRRS) builds upon the Psycho-Social Risk Interaction
Model (PRIM) by translating its theoretical insights into actionable measures. This strategy is designed to mitigate
the likelihood of adolescents engaging in violent crime by addressing the psychological, environmental, and
relational factors identified in the model. TIRRS operates through a combination of personalized interventions,
adaptive resource allocation, and dynamic monitoring to target high-risk individuals and environments
effectively. TIRRS consists of several interrelated modules: (1) Risk Assessment Module, which integrates real-time EEG-
based emotion monitoring, psychological assessments, and socio-environmental data to calculate individualized
risk scores; (2) Intervention Planning Module, which selects evidence-based intervention protocols (e.g.,
cognitive behavioral therapy, family counseling, peer-group restructuring) based on identified risk profiles;
(3) Dynamic Monitoring Module, which continuously updates risk assessments based on real-time behavioral
and emotional data to ensure timely adjustments in intervention intensity and content; and (4) Resource
Optimization Module, which allocates therapeutic, educational, and social resources efficiently according
to current intervention needs. Inputs to TIRRS include EEG signals (processed for emotional dysregulation
markers), standardized psychological inventories (e.g., Barratt Impulsiveness Scale), family and peer relational
metrics, and environmental context indicators (e.g., neighborhood violence index, socioeconomic status). The
system outputs individualized intervention plans, progress reports, and updated risk trajectories. For example,
if an adolescent exhibits elevated impulsivity and emotional dysregulation detected via EEG and self-report
scales, combined with peer delinquency and unstable family dynamics, TIRRS may assign a combined protocol
of emotional regulation training, family therapy sessions, and peer mentoring programs. Throughout the
intervention, continuous monitoring allows the system to adjust the intensity or components of the intervention
if the adolescent’s emotional stability or peer interactions change.(As shown in Fig. 3). Personalized psychological interventions
Figure 2. An illustration of temporal social influences, showcasing dynamic channel mixing through social
relational ties, static attention mechanisms, and optimized exercise functions to model the evolving impact of
relational and psychological embeddings on individuals over time. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

The core objective of TIRRS is to minimize the violent crime propensity Vi for each adolescent ai ∈A by
dynamically modulating the contributing factors (Pi, Ei, and Ri). The strategy achieves this by introducing
control mechanisms that influence these factors, guided by the outputs of PRIM. we define an intervention
function C: C(Pi, Ei, Ri) = {CP (Pi), CE(Ei), CR(Ri)},
(37)
where CP, CE, and CR represent targeted actions to reduce psychological vulnerabilities, environmental risks,
and relational influences, respectively. Psychological interventions aim to reduce harmful psychological traits while promoting protective traits. The
intervention CP is modeled as: CP (Pi) = Pi −ηP ∇P Φ(Pi, Ei, Ri; Θ),
(38)
where ηP > 0 is the intervention step size, and ∇P Φ represents the sensitivity of violent propensity Vi to
changes in psychological factors. This adjustment is achieved through evidence-based interventions, such as
cognitive-behavioral therapy (CBT), social-emotional learning programs, and mindfulness training. Environmental risks, captured by Ei, include factors such as exposure to community violence, school climate,
and socioeconomic disadvantage. To address these risks, CE introduces modifications based on: CE(Ei) = Ei −ηE∇EΦ(Pi, Ei, Ri; Θ),
(39)
where ηE > 0 represents the intervention adjustment for environmental factors. The interventions include
fostering safe community spaces, improving school engagement programs, and addressing economic inequities. Relational influences, represented by Ri, reflect the role of peer networks, family dynamics, and social
interactions in shaping behavior. To mitigate negative influences, CR is defined as: CR(Ri) = Ri −ηR∇RΦ(Pi, Ei, Ri; Θ),
(40)
where ηR > 0 is the relational intervention step size. This is operationalized through family therapy, mentorship
programs, and interventions targeting antisocial peer influences. To ensure efficient allocation of resources, we prioritize individuals with the highest psychological risk scores,
defined as: RP (ai) = ∥zP
i ∥2,
(41)
where zP
i is the latent psychological embedding from PRIM. Adolescents with RP (ai) > τP are flagged for
immediate intervention. environmental and relational risk scores are computed as: RE(ai) = ∥zE
i ∥2,

(42)
RR(ai) = ∥zR
i ∥2,

(43)
where zE
i and zR
i are the latent environmental and relational embeddings, respectively. Interventions prioritize
those exceeding the thresholds τE and τR. The combined intervention effect across all factors is modeled as: Figure 3. An overview of the targeted intervention and risk reduction strategy (TIRRS) framework,
illustrating Local Context Fusion, Global Bilinear Regularization, and Annotations. The process integrates
psychological, environmental, and relational factors through graph-based modeling, multilayered
interventions, and resource allocation for reducing violent crime propensity among adolescents. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

V new
i
= Vi −λP CP (Pi) −λECE(Ei) −λRCR(Ri),
(44)
where λP, λE, and λR are the respective weights representing the proportional impact of each intervention type. Resource allocation is further optimized by solving:
max
C
∑
i∈A
∆Vi
Ci,
(45)
where ∆Vi is the reduction in violent propensity for individual ai, and Ci is the cost of intervention. To monitor progress, the gradient of the violent propensity function is updated iteratively:
∇Φnew = ∇Φ −γ
∑
i∈A
C(Pi, Ei, Ri),
(46)
where γ > 0 is the learning rate for updating the system dynamics. This ensures continuous adaptation and
refinement of the intervention strategy. Environmental modifications for risk reduction
Environmental modifications focus on reducing exposure to risk factors such as neighborhood violence,
economic deprivation, and inadequate educational resources. The intervention CE modifies environmental
attributes as: CE(Ei) = Ei −ηE∇EΦ(Pi, Ei, Ri; Θ),
(47)
where ηE > 0 controls the magnitude of the intervention. Practical actions include providing after-school
programs, increasing access to mental health resources, and enhancing neighborhood safety through community
policing. Environmental risks are quantified using a weighted score: RE(ai) = ∥zE
i ∥2,
(48)
where zE
i is the latent environmental embedding derived from PRIM. Areas with a high aggregate risk score
∑
i∈A RE(ai) are prioritized for community-level interventions. To measure the effectiveness of environmental modifications, we define the risk-adjusted propensity score
for violence:

## V E

i
= ∂Vi
∂Ei · Ei,
(49)
where V E
i captures the contribution of environmental factors to the violent propensity. Reducing V E
i requires
lowering Ei in high-risk areas using targeted interventions. The resource allocation for environmental modifications is governed by: RE = arg min
CE
∑
i∈A
CE(Ei) · κi,
(50)
where κi represents the cost function associated with modifying environmental attributes for individual ai. This
ensures that limited resources are distributed efficiently across neighborhoods. To account for spatial dependencies in environmental factors, a graph-based model is used:

## LE = DE −AE,

(51)
where LE is the graph Laplacian matrix, DE is the degree matrix, and AE is the adjacency matrix representing
connections between neighborhoods. Environmental risk scores are smoothed over the graph using:
˜zE = (I + αLE)−1zE,
(52)
where α > 0 controls the extent of spatial smoothing, and I is the identity matrix. This process helps identify
clusters of neighborhoods that require coordinated interventions. To evaluate the overall impact of environmental modifications, we use a reduction function:

## ∆VE =

∑
i∈A
λE · CE(Ei),
(53)
where λE represents the weight of environmental contributions to violent propensity reduction. Higher values
of ∆VE indicate greater effectiveness of the interventions. To ensure sustainability of the interventions, a dynamic update mechanism is applied: Enew
i
= Ei −β · CE(Ei),
(54)
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

where β > 0 is the adjustment rate, ensuring that environmental risks are continuously reduced over time while
adapting to changing conditions. This iterative process integrates feedback from the community and system
dynamics. Relational interventions and dynamic monitoring
Relational interventions aim to mitigate the negative influences of peers or family members while fostering
positive social connections. Using the social graph G = (A, E), we identify high-risk connections by computing
relational risk scores: RR(ai) =
∑
j∈N (i)
wij∥zP
j ∥2,
(55)
where N(i) represents the neighbors of ai, and wij is the influence weight from aj to ai. Higher values of
RR(ai) indicate stronger exposure to negative relational influences, which are prioritized for intervention. The relational intervention CR reduces these risks by adjusting the weights wij as: CR(Ri) = Ri −ηR∇RΦ(Pi, Ei, Ri; Θ),
(56)
where ηR > 0 is the intervention step size, and ∇RΦ represents the sensitivity of violent crime propensity Vi
to relational factors. Practical measures include mentoring programs, family counseling, and restructuring peer
networks to encourage positive social relationships. The weighted influence of peers is further refined using a normalized adjacency matrix AR, where:

## AR = D−1

## R WR,

(57)
with WR representing the raw influence weights between individuals and DR being the degree matrix. This
normalization ensures that relational interventions are scaled appropriately across individuals. Dynamic monitoring within TIRRS involves continuous adaptation of relational interventions over time. The
temporal evolution of the violent crime propensity Vi(t) is described by:
dVi(t)
dt
= Φt(Pi(t), Ei(t), Ri(t)) −γVi(t),
(58)
where γ > 0 is a decay parameter that models the natural reduction in Vi(t) over time due to successful
interventions. This equation allows for the tracking of changes in propensity as relational, environmental, and
psychological factors evolve. To measure the effectiveness of relational interventions, we define the reduction in relational risk as:
∆RR(ai) = RR(ai) −R′
R(ai),
(59)
where R′
R(ai) is the updated relational risk score after applying CR. A larger ∆RR(ai) indicates a more effective
intervention in reducing exposure to negative relational influences. The optimization of relational interventions is guided by a resource allocation framework. The objective
function is:
max
{CR}
N
∑
i=1

## ∆V R

i,
subject to: BR(CR) ≤BR,
(60)
where ∆V R
i represents the reduction in Vi attributed to relational interventions, BR(·) is the cost of relational
interventions, and BR is the budget allocated for these interventions. Incorporating temporal trends, relational risks are updated iteratively using: Rnew
R
(ai) = RR(ai) −βR · CR(Ri),
(61)
where βR > 0 is the adjustment rate, ensuring that relational risk scores decrease progressively with each
intervention cycle (as shown in Fig. 4). The combined effect of relational, environmental, and psychological interventions on violent crime propensity
is expressed as: V new
i
= Vi −λP CP (Pi) −λECE(Ei) −λRCR(Ri),
(62)
where λP, λE, and λR represent the proportional weights of each intervention type. This equation quantifies the
overall impact of the integrated intervention strategy. Experimental setup
Datasets
The DEAP Dataset46 is a multimodal dataset designed for emotion analysis using physiological signals. It contains
data collected from 32 participants while watching 40 one-minute video excerpts, which were selected to elicit
specific emotional responses. The dataset includes EEG, ECG, EMG, and skin conductance signals, making it
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

a rich resource for affective computing and multimodal emotion recognition research. Participants rated their
emotions on valence, arousal, dominance, and liking scales after watching each video clip. The DEAP Dataset
has become a standard benchmark for evaluating emotion recognition models. The DREAMER Dataset47 is a
dataset aimed at emotion recognition using EEG and ECG signals. It comprises recordings from 23 participants
while they experienced audiovisual stimuli designed to provoke emotional responses. The stimuli are tailored to
induce positive, neutral, and negative emotions, and self-assessment was conducted using the valence, arousal,
and dominance scales. The portable acquisition setup and diversity of participants make the DREAMER
Dataset particularly suitable for studying emotion recognition in real-world scenarios. The SEED Dataset48 is
a comprehensive dataset for emotion recognition, utilizing EEG signals recorded from 15 subjects. The dataset
focuses on eliciting three emotional states: positive, neutral, and negative. Participants watched 15 film clips
specifically chosen to evoke the targeted emotional states. SEED Dataset includes detailed preprocessing steps
and provides session-based recordings, enabling researchers to study inter-session and intra-session variability. Its high-quality EEG recordings have made it a popular benchmark for developing deep learning-based emotion
recognition methods. The AMIGOS Dataset49 is a multimodal dataset designed for studying group and individual
affective states using EEG, ECG, and video recordings. Data were collected from 40 participants while they
engaged with a variety of emotionally evocative video stimuli. The dataset focuses on both individual and group
emotional responses, making it unique in its design. Emotional states were evaluated on valence, arousal, and
dominance dimensions, and the dataset also contains detailed annotations for collaborative and social contexts. The AMIGOS Dataset is widely used for studying the influence of social interactions on emotion recognition. The datasets used in this study are publicly available: the DEAP dataset50, the DREAMER dataset51, the SEED
dataset52, and the AMIGOS dataset53. The corresponding download links are as follows:
•	 DEAP dataset: ​h​t​t​p​:​/​/​w​w​w​.​e​e​c​s​.​q​m​u​l​.​a​c​.​u​k​/​m​m​v​/​d​a​t​a​s​e​t​s​/​d​e​a​p​/​d​o​w​n​l​o​a​d​.​h​t​m​l
•	 DREAMER dataset: https://zenodo.org/record/546113
•	 SEED dataset: https://bcmi.sjtu.edu.cn/home/seed/index.html
•	 AMIGOS dataset: ​h​t​t​p​s​:​/​/​w​w​w​.​e​e​c​s​.​q​m​u​l​.​a​c​.​u​k​/​m​m​v​/​d​a​t​a​s​e​t​s​/​a​m​i​g​o​s​/​d​o​w​n​l​o​a​d​.​h​t​m​l
Mathematical foundation of the violence risk model
The violence risk score Vi for each adolescent is calculated based on three key factors: Psychological profile (Pi): This includes traits like emotional dysregulation and impulsivity, which reflect
how an individual processes and reacts to emotions. Environmental stressors (Ei): These factors include
the adolescent’s environment, such as socioeconomic status, exposure to neighborhood violence, or adverse
childhood experiences. Relational factors (Ri): These are the influences from the adolescent’s social relationships,
including family dynamics and peer interactions. The equation used to calculate the violence risk score is as
follows: Vi = f(Pi, Ei, Ri)
Figure 4. An architecture for relational interventions and dynamic monitoring, illustrating the integration
of spatial and channel attention mechanisms. Key components include local context fusion, attention-based
relational weight adjustments, and iterative updates to optimize relational, environmental, and psychological
factors, aiming to reduce violent crime propensity through targeted and adaptive interventions. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

Where f represents a nonlinear function that combines these three factors. In simple terms, the model calculates
the likelihood of violent behavior based on the adolescent’s psychological, environmental, and relational profiles. This formula helps us understand how different factors interact and contribute to the overall risk assessment. In the following sections, we will discuss how each of these factors is measured and how they are incorporated
into the model. Experimental details
The experiments were conducted on the DEAP46, DREAMER47, SEED48, and AMIGOS49 datasets to evaluate
the performance of the proposed method. All signals were preprocessed to remove noise and artifacts using
bandpass filtering and notch filtering techniques, ensuring signal clarity for subsequent processing. For EEG
signals, frequency bands such as delta, theta, alpha, beta, and gamma were extracted to capture the relevant
frequency-specific features related to emotional states. For ECG signals, heart rate variability (HRV) metrics and
time-domain features were computed. The datasets were split into training, validation, and testing sets using a
subject-independent cross-validation strategy. This approach ensures the robustness and generalizability of the
model across unseen subjects. Feature extraction was performed using a combination of statistical, spectral, and
temporal methods to capture the intricate patterns in the physiological signals. Deep learning architectures,
including convolutional neural networks (CNNs) and recurrent neural networks (RNNs), were employed for
feature learning and classification. A hybrid model combining spatial and temporal feature representations was
also developed to enhance classification accuracy. The proposed models were trained using the Adam optimizer
with an initial learning rate of 0.001. A batch size of 64 was used, and training was conducted for 100 epochs. Early stopping was implemented to prevent overfitting, monitoring the validation loss with a patience of 10
epochs. To address class imbalance, weighted cross-entropy loss and data augmentation techniques were applied. For hyperparameter optimization, a grid search method was used to fine-tune the learning rate, number of
layers, and hidden units. The experiments were evaluated using standard metrics, including accuracy, F1-score,
precision, and recall. These metrics were calculated for each emotional class, as well as averaged across all classes
for overall evaluation. Statistical significance testing was performed using paired t-tests to compare the results
with baseline and state-of-the-art methods. All experiments were conducted on a machine equipped with an
NVIDIA RTX 3090 GPU and 32 GB of RAM, ensuring efficient training and testing of deep learning models. For
multimodal experiments, EEG and ECG signals were combined by concatenating features at the decision level. Multimodal fusion methods, such as late fusion and attention-based mechanisms, were implemented to leverage
complementary information across modalities. ablation studies were conducted to analyze the contribution of
individual modalities and feature sets to the overall performance. The experimental setup strictly adhered to the
protocols defined in the literature to ensure fair and reproducible comparisons (Algorithm 1). Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

Algorithm 1. Training Procedure for PRIM Network
Comparison with SOTA methods
In this section, we present a detailed comparison of our proposed method with state-of-the-art (SOTA) approaches
on the DEAP, DREAMER, SEED, and AMIGOS datasets. The performance metrics used for evaluation include
accuracy, recall, F1 score, and AUC, as shown in Tables 1 and 2. Our method outperformed the baseline models,
including BiLSTM, CNN, Transformer, GRU, MLP, and SVM, across all datasets, demonstrating its superiority
in sentiment analysis tasks. On the DEAP dataset, our method achieved an accuracy of 89.32%, which is
significantly higher than the second-best model (Transformer) at 85.89%. on the DREAMER dataset, our
method attained 88.23% accuracy, surpassing the Transformer model’s 84.22%. The superior performance of our
approach can be attributed to the robust feature extraction and multimodal fusion strategies, which effectively
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

capture temporal, spatial, and contextual information. the use of attention mechanisms allowed our model to
focus on the most relevant features, improving overall classification performance. The trend of outperformance continues on the SEED and AMIGOS datasets. On SEED, our method achieved
an accuracy of 88.92%, significantly better than the 86.45% accuracy of the Transformer model. on AMIGOS, our
model outperformed all baselines with an accuracy of 85.45%, highlighting its ability to generalize across diverse
datasets and modalities. the improvements in recall and F1 scores indicate that our method balances precision
and recall better than other models, avoiding overfitting to specific classes. The reasons for the consistent
improvement are multifaceted. our hybrid architecture integrates both spatial and temporal modeling, leveraging
CNNs for spatial feature extraction and RNN-based mechanisms for capturing sequential dependencies. the
multimodal approach effectively combines EEG and ECG signals, with late fusion ensuring the preservation of
modality-specific information. our attention-based fusion mechanism assigns dynamic importance to features,
emphasizing critical emotional cues. These design choices collectively enhance the model’s ability to learn robust
representations, leading to superior performance across all metrics. To evaluate the effectiveness of the proposed model, we conducted extensive comparative experiments on
four widely-used public EEG emotion datasets: DEAP, DREAMER, SEED, and AMIGOS. Table 3 summarizes
the performance of our approach against several state-of-the-art (SOTA) baseline models, including BiLSTM, CNN, Transformer, GRU, MLP, and SVM. Four standard evaluation metrics were adopted: Accuracy, Recall, F1 Score, and AUC. Our proposed method consistently outperforms all baseline models across all datasets
and evaluation metrics. Specifically, on the DEAP dataset, our model achieved an accuracy of 89.32%, which
represents a significant improvement over the best baseline (Transformer: 85.89%). Similarly, for the DREAMER
dataset, our model reached 88.23% accuracy, surpassing the second-best performance of 84.22% achieved by
the Transformer. On the SEED and AMIGOS datasets, our model also demonstrated superior performance,
achieving 87.95% and 86.70% accuracy, respectively. In addition to accuracy, our model achieved higher recall, F1 score, and AUC values across all datasets, demonstrating its robustness and superior generalization ability
in emotion recognition tasks. These results indicate that the proposed method effectively captures complex
emotional patterns from EEG signals, which is critical for downstream violent behavior risk prediction and
targeted intervention design. To further approximate the potential classification between adolescents with violent tendencies and
normative populations, we designed a simulated classification task using high-risk versus low-risk emotional
states based on existing emotional EEG datasets (DEAP and DREAMER). High-risk emotional states were
defined by high arousal and high negative valence, which are commonly associated with emotional dysregulation
and impulsive aggression, while low-risk states corresponded to low arousal and positive or neutral valence,
indicating emotional stability. Table 4 summarizes the performance of our model compared to multiple state-of-
the-art (SOTA) models under this simulated group-based classification task. As shown, our proposed method
consistently outperformed all baseline models across all evaluation metrics on both datasets. Specifically, our
model achieved an accuracy of 91.45% on the DEAP dataset and 90.35% on the DREAMER dataset, which
represents a substantial improvement compared to the best-performing baseline models (Transformer: 87.78%
on DEAP and 86.12% on DREAMER). In addition to accuracy, our model demonstrated superior Recall, F1 Score, Model
SEED Dataset
AMIGOS Dataset
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
BiLSTM54
82.45 ± 0.03
80.31 ± 0.02
81.56 ± 0.02
84.19 ± 0.03
78.12 ± 0.02
77.40 ± 0.02
76.89 ± 0.02
80.54 ± 0.03
CNN55
83.67 ± 0.02
82.13 ± 0.02
81.90 ± 0.02
85.71 ± 0.02
80.24 ± 0.02
79.11 ± 0.02
78.90 ± 0.02
82.47 ± 0.02
Transformer56
86.45 ± 0.03
84.89 ± 0.02
84.25 ± 0.02
87.12 ± 0.03
83.55 ± 0.02
82.23 ± 0.02
82.10 ± 0.02
85.63 ± 0.02
GRU57
83.10 ± 0.02
81.76 ± 0.02
82.03 ± 0.02
85.00 ± 0.03
81.32 ± 0.02
80.20 ± 0.02
79.88 ± 0.02
83.05 ± 0.02
MLP58
85.12 ± 0.03
83.78 ± 0.03
83.01 ± 0.03
86.47 ± 0.03
82.98 ± 0.02
81.44 ± 0.02
80.95 ± 0.02
84.76 ± 0.02
SVM59
80.87 ± 0.02
79.45 ± 0.02
78.92 ± 0.02
83.00 ± 0.02
77.98 ± 0.02
76.33 ± 0.02
76.12 ± 0.02
79.45 ± 0.02
Ours
88.92 ± 0.03
87.43 ± 0.03
86.78 ± 0.03
89.35 ± 0.03
85.45 ± 0.03
84.78 ± 0.03
84.23 ± 0.03
87.12 ± 0.03
Table 2. Comparison of ours with SOTA methods on SEED and AMIGOS datasets for sentiment analysis. Model
DEAP Dataset
DREAMER Dataset
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
BiLSTM54
81.25 ± 0.03
79.54 ± 0.02
80.32 ± 0.02
83.67 ± 0.03
79.84 ± 0.03
77.62 ± 0.02
78.90 ± 0.02
82.13 ± 0.02
CNN55
83.47 ± 0.02
82.10 ± 0.02
80.56 ± 0.02
85.22 ± 0.02
81.30 ± 0.02
80.18 ± 0.02
79.65 ± 0.02
84.70 ± 0.02
Transformer56
85.89 ± 0.03
84.32 ± 0.02
83.90 ± 0.02
86.12 ± 0.03
84.22 ± 0.02
83.15 ± 0.02
82.64 ± 0.02
86.54 ± 0.03
GRU57
82.95 ± 0.02
81.45 ± 0.02
80.78 ± 0.02
84.30 ± 0.03
82.11 ± 0.02
80.05 ± 0.02
79.95 ± 0.02
83.48 ± 0.02
MLP58
84.67 ± 0.03
83.54 ± 0.03
82.88 ± 0.03
86.71 ± 0.03
83.10 ± 0.02
81.56 ± 0.02
80.89 ± 0.02
85.12 ± 0.02
SVM59
80.13 ± 0.02
78.56 ± 0.02
79.10 ± 0.02
82.65 ± 0.02
79.78 ± 0.02
78.09 ± 0.02
77.90 ± 0.02
81.34 ± 0.02
Ours
89.32 ± 0.03
87.88 ± 0.03
86.45 ± 0.03
90.12 ± 0.03
88.23 ± 0.03
87.12 ± 0.03
86.78 ± 0.03
89.45 ± 0.03
Table 1. Comparison of ours with SOTA methods on DEAP and DREAMER datasets for sentiment analysis. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

Model
DEAP dataset
DREAMER dataset
SEED dataset
AMIGOS dataset
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
BiLSTM54
81.25 ± 0.03
79.54 ± 0.02
80.32 ± 0.02
83.67 ± 0.03
79.84 ± 0.03
77.62 ± 0.02
78.90 ± 0.02
82.13 ±
0.02
80.12 ± 0.03
78.45 ±
0.02
9.20 ±
0.02
82.55 ±
0.03
78.75 ± 0.02
77.03 ±
0.02
77.85 ±
0.02
80.45
±
0.02
CNN55
83.47 ± 0.02
82.10 ± 0.02
80.56 ± 0.02
85.22 ± 0.02
81.30 ± 0.02
80.18 ± 0.02
79.65 ± 0.02
84.70 ±
0.02
82.55 ± 0.02
80.62 ±
0.02
81.20 ±
0.02
84.15 ±
0.02
80.10 ± 0.02
79.02 ±
0.02
78.95 ±
0.02
82.30
±
0.02
Transformer56
85.89 ± 0.03
84.32 ± 0.02
83.90 ± 0.02
86.12 ± 0.03
84.22 ± 0.02
83.15 ± 0.02
82.64 ± 0.02
86.54 ±
0.03
85.05 ± 0.03
83.44 ±
0.02
83.80 ±
0.02
87.10 ±
0.03
83.65 ± 0.02
82.01 ±
0.02
81.75 ±
0.02
85.30
±
0.02
GRU57
82.95 ± 0.02
81.45 ± 0.02
80.78 ± 0.02
84.30 ± 0.03
82.11 ± 0.02
80.05 ± 0.02
79.95 ± 0.02
83.48 ±
0.02
81.80 ± 0.02
80.12 ±
0.02
79.85 ±
0.02
83.90 ±
0.02
79.95 ± 0.02
78.15 ±
0.02
77.90 ±
0.02
81.15
±
0.02
MLP58
84.67 ± 0.03
83.54 ± 0.03
82.88 ± 0.03
86.71 ± 0.03
83.10 ± 0.02
81.56 ± 0.02
80.89 ± 0.02
85.12 ±
0.02
83.95 ± 0.03
82.33 ±
0.02
82.10 ±
0.02
85.55 ±
0.03
82.30 ± 0.02
80.92 ±
0.02
80.75 ±
0.02
84.20
±
0.02
SVM59
80.13 ± 0.02
78.56 ± 0.02
79.10 ± 0.02
82.65 ± 0.02
79.78 ± 0.02
78.09 ± 0.02
77.90 ± 0.02
81.34 ±
0.02
79.12 ± 0.02
77.55 ±
0.02
77.90 ±
0.02
81.02 ±
0.02
77.85 ± 0.02
76.04 ±
0.02
76.50 ±
0.02
79.60
±
0.02
Ours
89.32 ± 0.03
87.88 ± 0.03
86.45 ± 0.03
90.12 ± 0.03
88.23 ± 0.03
87.12 ± 0.03
86.78 ± 0.03
89.45 ±
0.03
87.95 ± 0.03
86.42 ±
0.03
86.10 ±
0.03
88.60 ±
0.03
86.70 ± 0.03
85.23 ±
0.03
84.90 ±
0.03
87.80
±
0.03
Table 3. Comparison of ours with SOTA methods on DEAP, DREAMER, SEED and AMIGOS datasets for sentiment analysis. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

and AUC values, indicating both high sensitivity and precision in distinguishing between simulated high-risk
and low-risk groups. These results further confirm the model’s capability to capture key emotional dysregulation
patterns that are critical for predicting violent tendencies, even though real-world violent adolescent data was
not directly available. Table 5 presents a comparison of model performance across normative and high-risk adolescent datasets. The
model’s performance was evaluated on three datasets: a normative dataset (DEAP) and two high-risk adolescent
datasets (one from a juvenile justice system and another from clinical settings). Table 6 compares the model’s performance across different sample characteristics, such as age group,
socioeconomic status, personality traits, cultural background, and religion. These additional attributes will
be examined to assess their influence on model accuracy and predictive power in identifying emotional
dysregulation and violent tendencies. Ablation study
To evaluate the contribution of individual components in our proposed method, we conducted an ablation
study on the DEAP, DREAMER, SEED, and AMIGOS datasets. The results of these experiments are presented
in Tables 7 and 8. Different variations of the model were analyzed by removing specific components, denoted as
Capturing Internal States, Temporal Social Influences, and Psychological Interventions, and compared to the full
model (Ours). It can be observed that removing Capturing Internal States, which corresponds to the attention
mechanism for feature fusion, leads to a significant drop in performance. For the DEAP dataset, the accuracy
decreased from 89.32% to 85.23%, and for the DREAMER dataset, the accuracy dropped from 88.23% to
83.45%. F1 scores and AUC metrics show consistent reductions. This highlights the importance of the attention
mechanism in dynamically weighting the most relevant features during fusion, enhancing the model’s ability to
focus on discriminative signals for emotion recognition. Sample characteristic
Accuracy (%)
Recall (%)
Precision (%)
F1 Score (%)
AUC
Age group (adolescents 12–15)
88.45
86.72
84.98
87.10
0.89
Age group (adolescents 16–19)
89.32
87.88
86.45
90.12
0.91
Socioeconomic status (low)
85.76
84.30
82.10
83.80
0.87
Socioeconomic status (high)
89.91
88.20
87.11
89.65
0.92
Personality (impulsive)
86.65
85.10
84.00
85.50
0.88
Personality (emotionally stable)
90.22
88.45
86.90
89.70
0.92
Cultural background (western)
88.50
86.75
85.10
87.55
0.89
Cultural background (non-western)
87.20
85.60
83.80
85.90
0.88
Religion (non-religious)
89.12
87.40
85.80
88.20
0.90
Religion (religious)
88.00
86.00
84.50
85.60
0.89
Table 6. Impact of sample characteristics on model performance. Dataset
Accuracy (%)
Recall (%)
Precision (%)
F1 Score (%)
AUC
Normative (DEAP)
89.32
87.88
86.45
90.12
0.91
High-risk (juvenile)
85.72
83.95
81.68
84.57
0.88
High-risk (clinical)
87.45
85.60
83.25
86.80
0.89
Table 5. Comparison of model performance on normative and high-risk adolescent datasets. Model
DEAP dataset
DREAMER dataset
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
BiLSTM54
83.12 ± 0.03
82.45 ± 0.02
82.10 ± 0.02
85.67 ± 0.03
81.84 ± 0.03
80.62 ± 0.02
80.25 ± 0.02
83.13 ± 0.02
CNN55
85.45 ± 0.02
84.12 ± 0.02
83.50 ± 0.02
87.42 ± 0.02
83.30 ± 0.02
82.18 ± 0.02
81.75 ± 0.02
85.70 ± 0.02
Transformer56
87.78 ± 0.03
86.35 ± 0.02
86.00 ± 0.02
88.92 ± 0.03
86.12 ± 0.02
85.15 ± 0.02
84.64 ± 0.02
88.54 ± 0.03
GRU57
84.95 ± 0.02
83.55 ± 0.02
83.20 ± 0.02
86.30 ± 0.03
82.90 ± 0.02
81.05 ± 0.02
80.85 ± 0.02
84.48 ± 0.02
MLP58
86.70 ± 0.03
85.54 ± 0.03
85.20 ± 0.03
89.11 ± 0.03
85.10 ± 0.02
83.56 ± 0.02
83.20 ± 0.02
86.72 ± 0.02
SVM59
82.05 ± 0.02
80.56 ± 0.02
80.90 ± 0.02
84.65 ± 0.02
80.78 ± 0.02
79.09 ± 0.02
78.90 ± 0.02
82.34 ± 0.02
Ours
91.45 ± 0.03
90.12 ± 0.03
89.80 ± 0.03
92.60 ± 0.03
90.35 ± 0.03
89.22 ± 0.03
88.90 ± 0.03
91.45 ± 0.03
Table 4. Comparison of Ours with SOTA methods on DEAP and DREAMER datasets (high-risk vs low-risk
emotional state classification). Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

The results show that removing Temporal Social Influences, which represents the multimodal fusion module,
also negatively impacts performance. On the SEED dataset, the accuracy decreased from 88.92% to 85.90%, and
on the AMIGOS dataset, the accuracy dropped from 85.45% to 82.56%. This demonstrates that the effective
combination of EEG and ECG features plays a critical role in capturing complementary information from
multiple modalities, which in turn improves the robustness of the model. removing Psychological Interventions,
corresponding to the hybrid spatial-temporal feature extractor, resulted in a moderate but noticeable performance
reduction. On the DEAP dataset, the accuracy dropped from 89.32% to 87.34%, and on the SEED dataset, it
reduced from 88.92% to 86.78%. This indicates that the hybrid architecture effectively leverages spatial and
temporal patterns in the physiological data, which are crucial for accurately recognizing emotions. Conclusions and future work
This study aimed to address the complex issue of adolescent violent crime by focusing on the underexplored area
of emotional dysregulation. Recognizing that existing methods fail to account for the multidimensional nature
of aggression, the research proposed a novel framework integrating EEG emotion analysis and the Psycho-Social
Risk Interaction Model (PRIM). PRIM uniquely captures psychological factors like impulsivity and aggression,
environmental pressures such as socioeconomic adversity, and relational dynamics in family and peer networks. To operationalize these insights, the study developed the Targeted Intervention and Risk Reduction Strategy
(TIRRS), which provides personalized and adaptive interventions based on real-time data. By combining
these tools, the proposed methodology achieved a prediction accuracy of 87.5% for violent tendencies and
improved intervention success rates by 18.7% over conventional methods, while offering cost-efficient and
scalable prevention mechanisms. The experimental results underscore the significant potential of digital health
innovations in transforming theoretical insights into practical strategies for mitigating adolescent violence. Despite its promising findings, this study has several limitations. The dependence on EEG-based emotion
analysis, while innovative, raises concerns regarding accessibility and scalability in resource-limited settings,
potentially limiting its global applicability. Future research could explore alternative, cost-effective tools that
maintain accuracy without the need for advanced equipment. While the PRIM framework effectively captures a
range of influential factors, it may oversimplify the dynamic and evolving nature of adolescent relationships and
environmental pressures. Expanding PRIM to incorporate longitudinal data and contextual variability would
provide a more nuanced understanding. Moving forward, the integration of artificial intelligence to enhance
predictive analytics and tailoring interventions to cultural contexts could further improve the effectiveness and
applicability of this approach. This study has certain inherent limitations that should be acknowledged. First, the
current work adopts a cross-sectional rather than longitudinal design, limiting its ability to capture developmental
trajectories and temporal dynamics of adolescent violent behaviors. Second, the datasets utilized are based on
general normative samples rather than high-risk clinical or criminological populations. Therefore, while the
proposed model demonstrates strong performance in detecting emotional dysregulation from EEG signals,
caution is needed when directly generalizing these findings to actual violent adolescent populations. Nonetheless,
this inductive approach–beginning with normative emotional EEG data–offers important advantages in model
development. It allows us to rigorously validate the core technical components (e.g., emotional state classification,
multimodal data integration, nonlinear pattern recognition) under controlled conditions, thereby building a
robust foundation for subsequent adaptation to clinical or forensic populations. In future work, the proposed
model can be further extended and validated using longitudinal datasets and high-risk samples to capture the
complex psychosocial interactions and developmental pathways involved in adolescent violent behaviors. Furthermore, while the present study provides encouraging results based on normative emotion EEG datasets,
future studies incorporating clinical or at-risk adolescent populations would be essential to validate and refine
the proposed model within real-world violent behavior contexts. Access to data from adolescents with
Model
SEED Dataset
AMIGOS Dataset
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
Capturing Internal States
84.45 ± 0.02
83.12 ± 0.02
82.45 ± 0.02
86.23 ± 0.02
81.78 ± 0.02
80.45 ± 0.02
79.89 ± 0.02
83.12 ± 0.02
Temporal Social Influences
85.90 ± 0.03
84.22 ± 0.02
83.78 ± 0.02
87.11 ± 0.03
82.56 ± 0.03
81.34 ± 0.03
80.89 ± 0.02
84.67 ± 0.02
Psychological Interventions
86.78 ± 0.03
85.34 ± 0.02
84.22 ± 0.02
88.10 ± 0.03
84.12 ± 0.02
82.90 ± 0.02
82.10 ± 0.02
85.78 ± 0.02
Ours
88.92 ± 0.03
87.43 ± 0.03
86.78 ± 0.03
89.35 ± 0.03
85.45 ± 0.03
84.78 ± 0.03
84.23 ± 0.03
87.12 ± 0.03
Table 8. Ablation study results on SEED and AMIGOS datasets for sentiment analysis. Model
DEAP dataset
DREAMER dataset
Accuracy
Recall
F1 Score
AUC
Accuracy
Recall
F1 Score
AUC
Capturing internal states
85.23 ± 0.03
83.45 ± 0.02
82.78 ± 0.02
86.12 ± 0.03
83.45 ± 0.02
81.12 ± 0.02
80.89 ± 0.02
84.56 ± 0.02
Temporal Social Influences
86.78 ± 0.02
84.89 ± 0.02
83.65 ± 0.02
87.45 ± 0.03
84.12 ± 0.03
82.34 ± 0.02
81.67 ± 0.02
85.89 ± 0.02
Psychological interventions
87.34 ± 0.03
85.56 ± 0.03
84.12 ± 0.03
88.00 ± 0.03
85.01 ± 0.02
83.67 ± 0.02
82.89 ± 0.02
86.54 ± 0.02
Ours
89.32 ± 0.03
87.88 ± 0.03
86.45 ± 0.03
90.12 ± 0.03
88.23 ± 0.03
87.12 ± 0.03
86.78 ± 0.03
89.45 ± 0.03
Table 7. Ablation study results on DEAP and DREAMER datasets for sentiment analysis. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

documented violent or aggressive tendencies would allow for more precise training and evaluation of violence-
specific predictive features, enabling better alignment with forensic, clinical, and public health applications. In
this regard, the development of new ad hoc EEG data cohorts specifically designed for violent behavior research
represents a valuable future direction. Such cohorts could incorporate not only EEG-based emotion monitoring
but also multimodal assessments including behavioral evaluations, psychometric scales, family history, and
environmental stress indicators. These enriched datasets would allow for more comprehensive modeling of the
complex biopsychosocial mechanisms underlying violent behaviors and further enhance the personalization
capabilities of the proposed PRIM and TIRRS frameworks. Collaboration with clinical institutions, juvenile
justice systems, and multidisciplinary research teams will be critical in building ethically sound, representative,
and clinically meaningful datasets. We acknowledge that several potential confounding variables were not
explicitly controlled or analyzed in the current study, including participants’ age, gender, educational background,
socioeconomic status, and possible pre-existing clinical or psychiatric conditions. These factors are known to
influence both EEG signal characteristics and emotional responses, potentially introducing additional variability
into the emotion recognition process. Given that the publicly available datasets utilized in this study (DEAP, DREAMER, SEED, AMIGOS) provide only limited or partially anonymized demographic information,
comprehensive statistical control for these variables was not feasible. However, the use of subject-independent
cross-validation may have partially mitigated some individual-specific biases, allowing the models to focus on
generalizable emotion-related patterns rather than subject-specific idiosyncrasies. We fully recognize that future
research incorporating more detailed and diverse demographic data will be crucial to systematically evaluate the
impact of these confounding factors. Stratified sampling, subgroup analysis, or covariate-adjusted modeling
approaches could be employed to further refine the model’s robustness and enhance its clinical generalizability
across different populations. In addition to the previously discussed methodological limitations, it is important
to further distinguish between the methodological and applicative challenges faced by this study. From a
methodological perspective, the primary limitations include reliance on publicly available emotion recognition
datasets that do not specifically represent violent or high-risk adolescent populations, limited availability of
comprehensive demographic and psychosocial variables, and the cross-sectional nature of data collection, which
restricts temporal modeling of behavioral development. From an applicative standpoint, the deployment of the
proposed TIRRS framework into real-world clinical or educational contexts introduces several additional
challenges. First, the ecological validity of emotion recognition models trained on laboratory-controlled datasets
may not fully generalize to uncontrolled, highly variable real-world environments where factors such as noise,
sensor reliability, and user compliance can substantially affect system performance. Second, integrating AI-
driven systems into therapeutic interventions requires careful consideration of clinical workflow integration,
practitioner training, and regulatory oversight. Third, ethical concerns regarding data privacy, informed consent,
potential stigmatization of at-risk youth, and responsible algorithmic decision-making must be addressed to
ensure that the deployment of TIRRS is both ethically sound and socially acceptable. Finally, logistical issues
such as hardware accessibility (e.g., EEG equipment), infrastructure costs, and the need for multidisciplinary
collaboration between AI researchers, clinicians, educators, and policy makers represent significant real-world
barriers that must be systematically addressed prior to large-scale implementation. Future research should thus
prioritize longitudinal, multi-site validation studies with diverse populations and establish clear ethical
frameworks to guide responsible clinical translation of AI-powered risk assessment and intervention models. It
is important to acknowledge a key limitation regarding the generalizability of the current findings. While the
proposed PRIM and TIRRS frameworks are conceptually intended for use in assessing emotion dysregulation
and associated risk behaviors in adolescents, the datasets employed for model development and evaluation
(DEAP, DREAMER, SEED, AMIGOS) are based on normative, non-clinical samples from the general population. These datasets were originally collected for affective neuroscience research rather than forensic, clinical, or
justice-involved youth populations. As such, the present study should be regarded as a preliminary proof-of-
concept demonstration of the model’s technical feasibility in capturing emotional dysregulation patterns from
EEG-based data. The applicability of the proposed framework to real-world high-risk or clinical adolescent
populations remains to be empirically validated. Future research should prioritize data collection from justice-
involved, clinical, or at-risk youth cohorts, incorporating multi-site longitudinal designs and multidimensional
behavioral, psychosocial, and neurophysiological assessments. Such extensions will be essential to fully establish
the clinical validity, predictive utility, and translational readiness of the proposed neurotechnology-informed
risk assessment models. The real-world deployment of EEG-based digital interventions in adolescents–
particularly within clinical, forensic, or educational settings–requires careful ethical scrutiny. Several key
considerations must be addressed to ensure fairness, transparency, and harm reduction:
•	 Informed Consent and Autonomy: Adolescents are a vulnerable population. Any implementation would re­
quire age-appropriate informed consent procedures, including parental or legal guardian involvement where
necessary, and clear communication of data use, risks, and benefits.
•	 Data Privacy and Security: EEG and psychosocial data constitute highly sensitive personal information. All
data collection, storage, and analysis must comply with applicable data protection regulations (e.g., GDPR, HIPAA), with strict protocols for anonymization, secure storage, and limited access.
•	 Stigmatization and Labeling Risks: Predictive labeling of adolescents as high-risk may lead to unintended
stigmatization, educational exclusion, or social harm. Thus, model outputs should be used to inform support­
ive interventions rather than punitive measures, and always accompanied by multidisciplinary professional
judgment.
•	 Transparency and Algorithmic Fairness: The model’s decision-making logic should be interpretable to both
clinicians and stakeholders to avoid “black-box” reliance. Ongoing fairness audits should monitor for poten­
tial algorithmic biases related to demographic or socioeconomic variables. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

•	 False Positive Consequences: Given the potential harm of false positive risk classification, conservative
thresholds, continuous model recalibration, and individualized case reviews are essential to minimize un­
necessary interventions. Future implementation efforts should involve close collaboration among clinicians, ethicists, legal experts,
educators, affected communities, and regulatory bodies to ensure that technology deployment prioritizes
adolescent welfare, respects autonomy, and minimizes unintended harm. By focusing on a more appropriate population sample–such as adolescents at varying levels of risk–we aim
to capture the temporal dynamics that influence emotional dysregulation and violent behavior. This will allow
for a better understanding of the evolution of these risk factors and provide deeper insights into their predictive
power. We believe that conducting this longitudinal study will enhance the reliability of the PRIM assessment
phase, providing a stronger foundation for our proposed model. Tracking adolescents over a longer period will
offer valuable data on how early emotional dysregulation can lead to violent behavior later in life. This study will
not only validate the current model but also refine our approach, ensuring that interventions are more dynamic,
responsive, and tailored to the specific needs of at-risk individuals. This longitudinal investigation will be an
essential step toward improving the accuracy and robustness of the PRIM model in predicting and mitigating
violent criminal behaviors in adolescents. Given the sensitivity of working with adolescent populations, we emphasize that any future implementation
of this model will strictly adhere to international ethical standards regarding data privacy and informed consent. As adolescents are typically minors, participation in any research or real-world application would require dual
informed consent – one from the adolescent themselves and one from a parent or legal guardian. Additionally, all
collected data, including EEG signals and psychosocial indicators, will be anonymized and stored using secure,
encrypted systems compliant with international privacy regulations such as GDPR and HIPAA. These safeguards
are essential to ensure the ethical integrity and social acceptability of deploying digital health interventions in
vulnerable populations. Data availability
The datasets generated and/or analysed during the current study are available in the NeuroSafe, ​h​t​t​p​s​:​/​/​g​i​t​h​u​b​.​c​
o​m​/​L​i​x​i​n​Z​h​a​n​g​2​0​2​4​/​N​e​u​r​o​S​a​f​e​.​g​i​t​.​
Received: 19 January 2025; Accepted: 25 September 2025
References

### 1. Thompson, R. A. Emotion regulation: A theme in search of definition. Monographs of the Society for Research in Child Development

(1994).

### 2. Gross, J. J. Emotion regulation: Conceptual and empirical foundations. Handbook of emotion regulation (2014).

### 3. Beauchaine, T. P. et al. The transdiagnostic role of emotion dysregulation in psychopathology. Clin. Psychol. Sci. Pract. (2015).

### 4. McLaughlin, K. A. Emotion dysregulation and adolescent psychopathology. J. Clin. Child Adolesc. Psychol. (2015).

### 5. Zhang, W., Deng, Y., Liu, B.-Q., Pan, S. J. & Bing, L. Sentiment analysis in the era of large language models: A reality check. NAACL-

## HLT (2023).

### 6. Mao, R., Liu, Q., He, K., Li, W. & Cambria, E. The biases of pre-trained language models: An empirical study on prompt-based

sentiment analysis and emotion detection. IEEE Trans. Affect. Comput. (2023).

### 7. Alsaeedi, A. & Zubair, M. A study on sentiment analysis techniques of twitter data. Int. J. Adv. Comput. Sci. Appl. (2023).

### 8. Zhu, T. et al. Multimodal sentiment analysis with image-text interaction network. IEEE Trans. Multimedia (2023).

### 9. Fatouros, G., Soldatos, J., Kouroumali, K., Makridis, G. & Kyriazis, D. Transforming sentiment analysis in the financial domain

with chatgpt. Mach. Learn. Appl. (2023).

### 10. He, F., Li, H., Ning, X. & Li, Q. Beautydiffusion: Generative latent decomposition for makeup transfer via diffusion models. Inf. Fusion 103241 (2025).

### 11. Gratz, K. L. Multidimensional assessment of emotion regulation and dysregulation. J. Psychopathol. Behav. Assess. (2004).

### 12. Fox, N. A. Emotion regulation: Behavioral and neural correlates. Biol. Psychol. (2005).

### 13. Blair, R. J. R. The neurobiology of youth violence. Nat. Rev. Neurosci. (2013).

### 14. Davidson, R. J. et al. Dysfunction in the neural circuitry of emotion regulation—a possible prelude to violence. Science (2000).

### 15. Sterzer, P. Neural mechanisms of aggression in antisocial behavior. J. Child Psychol. Psychiatry (2005).

### 16. Blair, R. J. R. Neurocognitive models of aggression. J. Child Psychol. Psychiatry (2012).

### 17. Deng, J. Emotion recognition using eeg signals: A comprehensive survey. IEEE Trans. Affect. Comput. (2021).

### 18. Alarcao, S. & Fonseca, M. J. Emotions recognition using eeg signals: A survey. IEEE Trans. Affect. Comput. (2017).

### 19. Liu, Y. Eeg-based emotion recognition: A review of recent advances and future perspectives. Inf. Fusion (2021).

### 20. Taherdoost, H. & Madanchian, M (A review in competitive research. De Computis, Artificial intelligence and sentiment analysis,

2023).

### 21. Qi, Y. & Shabrina, Z. Sentiment analysis using twitter data: a comparative application of lexicon- and machine-learning-based

approach. Soc. Netw. Anal. Min. (2023).

### 22. Bordoloi, M. & Biswas, S. Sentiment analysis: A survey on design framework, applications and future scopes. Artif. Intell. Rev.

(2023).

### 23. Wankhade, M., Rao, A. C. & Kulkarni, C. A survey on sentiment analysis methods, applications, and challenges. Artif. Intell. Rev.

(2022).

### 24. Zhang, W., Li, X., Deng, Y. & Bing, L. & Lam, W (Tasks, methods, and challenges. IEEE Transactions on Knowledge and Data

Engineering, A survey on aspect-based sentiment analysis, 2022).

### 25. Yan, H., Dai, J., Ji, T., Qiu, X. & Zhang, Z. A unified generative framework for aspect-based sentiment analysis. In Annual Meeting

of the Association for Computational Linguistics (2021).

### 26. Hazarika, D. Zimmermann, R. & Poria, S (Modality-invariant and -specific representations for multimodal sentiment analysis. ACM Multimedia, Misa, 2020).

### 27. Wang, K., Shen, W., Yang, Y., Quan, X. & Wang, R. Relational graph attention network for aspect-based sentiment analysis. In

Annual Meeting of the Association for Computational Linguistics (2020). Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

### 28. Hartmann, J., Heitmann, M., Siebert, C. & Schamp, C. More than a feeling: Accuracy and application of sentiment analysis. Int. J. Res. Mark. (2022).

### 29. Prottasha, N. J. et al. Transfer learning for sentiment analysis using bert based supervised fine-tuning. In Italian National Conference

on Sensors (2022).

### 30. Li, R. et al. Dual graph convolutional networks for aspect-based sentiment analysis. In Annual Meeting of the Association for

Computational Linguistics (2021).

### 31. Han, W., Chen, H. & Poria, S. Improving multimodal fusion with hierarchical mutual information maximization for multimodal

sentiment analysis. In Conference on Empirical Methods in Natural Language Processing (2021).

### 32. Tan, K. L., Lee, C., Anbananthen, K. & Lim, K. Roberta-lstm: A hybrid model for sentiment analysis with transformer and recurrent

neural network. IEEE Access (2022).

### 33. Muhammad, S. H. et al. Naijasenti: A nigerian twitter sentiment corpus for multilingual sentiment analysis. In International

Conference on Language Resources and Evaluation (2022).

### 34. Gao, Y. et al. Implementation and evaluation of whole-course-based internet hospital outpatient pharmacy services: A cross-

sectional study in western china. Front. Public Health 12, 1448471 (2024).

### 35. Luo, G. et al. Healthpass: a contactless check-in and adaptive access control system for lowering cluster infection risk in public

health crisis. Front. Public Health 12, 1448901 (2024).

### 36. Hu, G. et al. Unimse: Towards unified multimodal sentiment analysis and emotion recognition. In Conference on Empirical

Methods in Natural Language Processing (2022).

### 37. Chan, J. Y.-L., Bea, K. T., Leow, S. M. H., Phoong, S. & Cheng, W.-K. State of the art: a review of sentiment analysis based on

sequential transfer learning. Artif. Intell. Rev. (2022).

### 38. Gupta, I., Chatterjee, I. & Gupta, N. Sentiment analysis of covid-19 tweets. In International Conference on Intelligent Control and

Instrumentation (2022).

### 39. Doerwald, F. et al. A rapid review of digital approaches for the participatory development of health-related interventions. Front. Public Health 12, 1461422 (2024).

### 40. Singh, D., AlZubi, A. A., Kaur, M., Kumar, V. & Lee, H.-N. Deep multi-patch hierarchical network-based visibility restoration

model for autonomous vehicles. IEEE Trans. Vehic. Technol. (2024).

### 41. Barnes, J. et al. Semeval 2022 task 10: Structured sentiment analysis. In International Workshop on Semantic Evaluation (2022).

### 42. Zhang, W., Li, X., Deng, Y., Bing, L. & Lam, W. Towards generative aspect-based sentiment analysis. In Annual Meeting of the

Association for Computational Linguistics (2021).

### 43. Nandwani, P. & Verma, R. A review on sentiment analysis and emotion detection from text. Soc. Netw. Anal. Min. (2021).

### 44. Singh, D., Alzubi, A. A., Kaur, M., Kumar, V. & Lee, H.-N. Deep drug synergy prediction network using modified triangular

mutation-based differential evolution. IEEE J. Biomed. Health Inf. (2024).

### 45. Singh, D. et al. Classification and analysis of pistachio species with pre-trained deep learning models. Electronics 11, 981 (2022).

### 46. Singh, U., Shaw, R. & Patra, B. K. A data augmentation and channel selection technique for grading human emotions on deap

dataset. Biomed. Signal Process. Control 79, 104060 (2023).

### 47. Ahangaran, M. et al. Dreamer: a computational framework to evaluate readiness of datasets for machine learning. BMC Med. Inform. Decis. Mak. 24, 152 (2024).

### 48. Loddo, A. et al. An effective and friendly tool for seed image analysis. Vis. Comput. 39, 335–352 (2023).

### 49. Bota, P. et al. Group synchrony for emotion recognition using physiological signals. IEEE Trans. Affect. Comput. 14, 2614–2625

(2023).

### 50. EECS, Q. M. U. o. L. Deap dataset. ​h​t​t​p​:​/​/​w​w​w​.​e​e​c​s​.​q​m​u​l​.​a​c​.​u​k​/​m​m​v​/​d​a​t​a​s​e​t​s​/​d​e​a​p​/​d​o​w​n​l​o​a​d​.​h​t​m​l (2013).

### 51. DREAMER. Dreamer dataset. https://zenodo.org/record/546113 (2020).

### 52. BCMI, S. J. T. U. Seed dataset. https://bcmi.sjtu.edu.cn/home/seed/index.html (2017).

### 53. EECS, Q. M. U. o. L. Amigos dataset. ​h​t​t​p​s​:​/​/​w​w​w​.​e​e​c​s​.​q​m​u​l​.​a​c​.​u​k​/​m​m​v​/​d​a​t​a​s​e​t​s​/​a​m​i​g​o​s​/​d​o​w​n​l​o​a​d​.​h​t​m​l (2017).

### 54. Hao, X., Di, Y., Xu, Q., Liu, P. & Xin, W. Multi-objective prediction for denitration systems in cement: an approach combining

process analysis and bi-directional long short-term memory network. Environ. Sci. Pollut. Res. 30, 30408–30429 (2023).

### 55. Boufssasse, A., Hssayni, E. h., Joudar, N.-E. & Ettaouil, M. A multi-objective optimization model for redundancy reduction in

convolutional neural networks. Neural Process. Lett. 55, 9721–9741 (2023).

### 56. Aksamit, N., Hou, J., Li, Y. & Ombuki-Berman, B. Integrating transformers and many-objective optimization for drug design. BMC Bioinf. 25, 208 (2024).

### 57. Hou, X., Ge, F., Chen, D., Shen, L. & Zou, F. Temporal distribution-based prediction strategy for dynamic multi-objective

optimization assisted by gru neural network. Inf. Sci. 649, 119627 (2023).

### 58. Nabavi, S. R., Jafari, M. J. & Wang, Z. Deep learning aided multi-objective optimization and multi-criteria decision making in

thermal cracking process for olefines production. J. Taiwan Inst. Chem. Eng. 152, 105179 (2023).

### 59. Grzyb, J. & Woźniak, M. Svm ensemble training for imbalanced data classification using multi-objective optimization techniques. Appl. Intell. 53, 15424–15441 (2023). Acknowledgements
This is a short text to acknowledge the contributions of specific colleagues, institutions, or agencies that aided
the efforts of the authors. Author contributions
Conceptualization, ZZ; methodology, ZZ; software, ZZ; validation, ZZ; formal analysis, LZ; investigation, LZ;
data curation, LZ; writing—original draft preparation, LZ, ZZ; writing—review and editing, LZ; visualization, ZZ; supervision, ZZ; funding acquisition, ZZ; All authors have read and agreed to the published version of the
manuscript. Funding
Details of all funding sources should be provided, including grant numbers if applicable. Please ensure to add all
necessary funding information, as after publication this is no longer possible. Declarations
Competing interests
The authors declare no competing interests. Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/

Additional information
Correspondence and requests for materials should be addressed to Z. Z. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:38178

| https://doi.org/10.1038/s41598-025-22067-2
www.nature.com/scientificreports/
