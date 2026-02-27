# © The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0

**Year:** D:20

---

RESEARCH
Open Access
© The Author(s) 2025. Open Access This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0
International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you
give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the
licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or
other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the
material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or
exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit ​h​t​t​p​:​/​/​c​r​e​a​t​i​
v​e​c​o​m​m​o​n​s​.​o​r​g​/​l​i​c​e​n​s​e​s​/​b​y​-​n​c​-​n​d​/​4​.​0​/. Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
https://doi.org/10.1186/s12984-025-01650-8
Journal of NeuroEngineering
and Rehabilitation
†Guozheng Wang and Xiaoxia Liu have contributed equally to this
work and share first authorship.
*Correspondence: Ying Gao
yigao@zju.edu.cn
Jun Liu
liujun@zju.edu.cn
Full list of author information is available at the end of the article
Abstract
Background  Tai Chi (TC) is recognized for enhancing balance and postural control. However, studies on its effects
on the central nervous system are limited and often involve static experiments despite the dynamic nature of TC. This study addressed that gap by examining cortical network activity during dynamic, multisensory conflict balance
tasks. We aimed to determine whether long-term TC practice leads to neuroplastic changes in brain connectivity that
improve sensory integration for postural control. Methods  Fifty-two young adult participants (long-term TC practitioners = 22; non-practitioners = 30) performed
balance tasks under sensory congruent and conflict conditions using a virtual reality headset with a rotating
supporting surface. EEG was performed, and generalized partial directed coherence was used to assess directed
functional connectivity in the mu rhythm (8–13 Hz) between predefined regions of interest (ROIs) in the cortex
implicated in sensory and motor integration. Graph-theoretic measures (in-strength and out-strength) indexed the
total incoming and outgoing connection strengths for each region. Statistical analysis used mixed-design ANOVAs
(Group × Condition) to compare balance and connectivity measures. Results  TC practitioners demonstrated significantly better postural stability under both sensory conditions, with a
reduced sway area. EEG analysis revealed that increased sensory conflict decreased the global efficiency of the visual
integration network but increased that of the somatosensory integration network. Furthermore, TC practitioners
demonstrated enhanced out-strength of the somatosensory cortex and lower out-strength of the right posterior
parietal cortex (PPC) compared to non-practitioners. Conclusions  Long-term TC practice is associated with quantifiable neuroplastic changes in mu-band cortical
effective connectivity, specifically enhanced information outflow from somatosensory reduce parietal influence
Cortical adaptations in Tai Chi practitioners
during sensory conflict: an EEG-based
effective connectivity analysis of postural
control
Guozheng Wang1,2,3†, Xiaoxia Liu3†, Yiming Cai2, Jian Wang3,4, Ying Gao3* and Jun Liu1,2*

Page 2 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
Background
Postural control is an essential requirement for static
and dynamic stability, integrating various sensory inputs
from the visual, vestibular, and somatosensory systems
to generate appropriate motor responses to maintain
postural stability [1, 2]. Efficient postural control during
most activities of daily living is important to prevent falls,
which may lead to injuries. Tai Chi (TC) is a traditional
Chinese martial art practiced worldwide for its health
benefits, particularly in improving balance and postural
control [3–5]. TC practice leads to substantial improvement in bal­
ance and proprioception, elements that form the basis
of postural control [6]. Trials have shown that TC
improves balance and prevents falls among older adults
and individuals with neurological diseases because it
involves slow and controlled movements [7, 8]. Li et al.
also reported that TC significantly improves balance and
reduces the risk of falls in older adults with a history of
falls [9]. While many studies have examined the peripheral
effects of TC, few studies have focused on central ner­
vous system effects. Recent electroencephalography
(EEG) studies have assessed the influence of TC on brain
activity [10]. EEG offers high temporal resolution suit­
able for capturing the rapid neural dynamics involved in
postural adjustments [11]. For example, enhanced alpha-
wave activity has been found in TC practitioners, reflect­
ing improvements in mental relaxation and reduced
stress [12]. Liu et al. reported improved cognitive func­
tion and cortical connectivity in TC practitioners com­
pared with that in non-practitioners [13]. However, most EEG-based TC studies have been con­
ducted under static conditions despite the dynamic
nature of TC. It is important to examine the cortical pro­
cessing of multisensory information under dynamic and
varied sensory input conditions. The prevailing static
research paradigm may overlook or misrepresent the
crucial neural adaptations that enable TC practitioners
to excel in dynamic balance tasks, thereby limiting the
translation of research findings into effective interven­
tions for real-world balance challenges. In recent years, there has been an increased focus on
understanding cortical and muscular connectivity dur­
ing balance control under sensory perturbations. Sen­
sory-conflict paradigms based on virtual reality (VR)
and moving platforms elicit substantial postural adjust­
ments and neural responses without significant bodily
movement interference. Multisensory conflicts, such as
inconsistencies between visual and vestibular or proprio­
ceptive information, challenge balance maintenance and
test sensory adjustment capabilities. Peterson and Fer­
ris (2019) conducted a study on group-level cortical and
muscular connectivity during perturbations in walking
and standing balance. Perturbations such as visual field
rotations and physical pulls were found to significantly
affect corticomuscular connectivity [14]. Our research
group has also conducted a series of experiments based
on brain network analysis under sensory conflict. We dis­
covered that sensory conflicts induced through virtual
reality and a rotating platform initially disrupt postural
stability [15, 16]; however, over time, individuals show
adaptation characterized by the dynamic reorganization
of brain networks. These findings underscore the brain’s
capacity for rapid adaptation and suggest that investi­
gating these dynamic reorganizational processes can
inform the design of targeted balance training programs
that specifically challenge and train these adaptive neural
mechanisms. Investigating brain function during such dynamic tasks
necessitates analytical approaches that can capture the
complex interplay within neural networks. Advances in
network neuroscience, computational approaches [17,
18], particularly methods for estimating directed effec­
tive connectivity from EEG, offer new perspectives on
cortical information interactions [19–21]. Effective con­
nectivity quantifies the directed influence one neural
population exerts over another, going beyond simple
correlations (often termed functional connectivity) to
infer information flow within brain networks. This shift
from describing what brain areas are active to how they
influence each other represents a fundamental advance­
ment, allowing for the formulation of more mechanistic
hypotheses about information processing in the brain,
especially during complex behaviors like postural adap­
tation. One powerful approach for estimating effec­
tive connectivity from EEG time-series is Multivariate
Autoregressive (MVAR) modeling. MVAR models cap­
ture the linear predictive relationships between multiple
signals simultaneously. From fitted MVAR models, met­
rics like Generalized Partial Directed Coherence (GPDC)
can be derived. Furthermore, graph theory provides a quantita­
tive framework for analyzing the topological proper­
ties of brain networks derived from connectivity data. Metrics such as node strength, specifically in-strength
and out-strength for directed networks, can character­
ize the functional roles of different brain regions [22].
regions. Our findings demonstrate central mechanisms by which TC practice may improve balance, providing
neuroengineering evidence for TC as a neuroplasticity-driven balance intervention. Keywords  Tai chi, Postural control, EEG, Cortical connectivity, Sensory integration

Page 3 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
In-strength, the sum of weighted incoming connections
to a node, reflects the total influence received by that
region, potentially highlighting its role as an integra­
tion hub. Conversely, out-strength, the sum of weighted
outgoing connections from a node, reflects the total
influence exerted by that region on others, potentially
indicating its role as an information source or driver
within the network. Analyzing how these metrics change
under sensory conflict, and whether they differ between
TC practitioners and controls, can provide valuable
insights into the adaptive neural strategies associated
with TC training. This study specifically focuses on the mu rhythm
(8–13 Hz), an EEG oscillation originating predominantly
from the sensorimotor cortex [23]. The mu rhythm is
functionally relevant as it reflects the activation state
(desynchronization) or idling/inhibition state (synchroni­
zation) of sensorimotor areas. Its power and connectivity
are modulated during movement execution, preparation,
imagery, observation, and crucially, during tasks requir­
ing sensorimotor integration. Given that TC training
involves extensive refinement of sensorimotor control
and body awareness, we hypothesized that neuroplastic
adaptations induced by TC would be particularly evident
in the mu frequency band. Therefore, our a priori focus
on mu-band effective connectivity represents a hypothe­
sis-driven approach to investigate the specific sensorimo­
tor network changes potentially underlying TC’s postural
benefits. The primary aim of this study was to analyze corti­
cal-directed information interactions within the mu
frequency band in TC practitioners under sensory per­
turbations using effective brain network analysis via EEG
technology. Using advanced EEG techniques, we sought
to understand how TC practice influences the ability of
the brain to process and integrate sensory information
to maintain postural control. We hypothesized that: [1]
TC practitioners would exhibit superior postural stabil­
ity compared to controls, particularly under sensory
conflict; [2] Sensory conflict would modulate mu-band
effective connectivity networks in ways consistent with
sensory re-weighting; and [3] Compared to controls, TC
practitioners would demonstrate distinct patterns of mu-
band effective connectivity during sensory conflict, spe­
cifically showing evidence of enhanced somatosensory
processing (e.g., increased out-strength from somatosen­
sory regions), reflecting adaptive neural strategies devel­
oped through extensive training. Methods
Participants
The research included a total of 52 individuals, consist­
ing of 22 TC practitioners and 30 controls who were
matched in terms of age and sex. The TC practitioners
were national first-class athletes and national master ath­
letes with 6–15 years of TC experience. The TC practitio­
ners reported currently practicing Tai Chi for a minimum
of 30 min per session, at least three times per week, in
addition to their years of experience. The control group,
with no previous experience in TC practice, engaged in
general aerobic exercises, such as walking, at least three
times a week, with each session lasting 30 min or more. The inclusion criteria for the participants were: age
range of 18–35 years, good general health, normal or cor­
rected vision, and right hand and right leg dominance
confirmed through specific tests for hand and leg domi­
nance. For the TC practitioners, a minimum of 6 years
of TC practice was required. The following exclusion
criteria were applied: any sensory, neurological, muscu­
loskeletal, or cardiovascular disorders; recent surgery
involving the lower extremities or the dominant arm;
conditions such as motion sickness, dizziness, or ver­
tigo; psychological problems such as fear of falling, anxi­
ety, or depression; and a Montreal Cognitive Assessment
(MoCA) score of < 26. While Tai Chi is often practiced by
older adults, this study focused on young, highly experi­
enced practitioners to isolate the long-term neuroplastic
effects of extensive training itself, minimizing potential
confounds from age-related changes in neural struc­
ture, function, and postural control mechanisms. Direct
extrapolation of these specific findings to older popula­
tions requires caution. Participants were adequately informed of the research
protocols and gave signed permission before par­
ticipating. The Zhejiang University Psychological Sci­
ence Research Center Ethics Committee approved the
research (2024.011). Ethical considerations included
ensuring participant confidentiality, right to withdraw
from the study at any time, and adherence to the prin­
ciples of the Declaration of Helsinki. Initially, 22 TC practitioners and 30 non-practitioners
were recruited. However, EEG data were not collected
from three non-practitioners because of equipment mal­
function. Furthermore, excessive body movement during
the sessions resulted in significant EEG data contamina­
tion for three TC practitioners and four non-practitio­
ners. Consequently, the final analysis included center of
pressure (COP) data from all 22 TC athletes and 30 non­
athletes, while usable EEG data were available for 19 TC
practitioners and 23 non-practitioners only. Experimental design
This study examined the effect of TC training on pos­
ture control across multiple sensory conditions using
a rotating platform (All Controller, Nanjing, China) to
control actual motion and a virtual reality (VR) headset
(VIVE PRO 2, HTC Corporation, New Taipei, Taiwan)
to alter visual cues. Two balance disturbance conditions

Page 4 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
were set: “sensory congruent” and “sensory conflict.” The
“sensory congruent” condition aimed to present the par­
ticipants with natural multisensory information during a
clockwise rotation. The “sensory conflict” condition pro­
vided visual scenes expected during a counterclockwise
rotation while the participants were rotating clockwise
(Fig. 1). Upon entering the laboratory, the participants were
briefed on the experimental procedure and given a pre­
liminary trial to familiarize themselves with the process
(no data were collected). After the preliminary trial, the
participants were asked to remove their shoes and socks
and stand in the middle of the force plate with their feet
shoulder-width apart and their hands crossed over the
chest. They were then fitted with a VR headset that dis­
played a simulated laboratory environment created using
Unity3D. Throughout the experiment, the participants
were instructed to keep their eyes open and look straight
ahead (normal blinking was allowed), and the eye-track­
ing systems within the VR headset ensured no prolonged
intentional eye closure. Participants were required to
maintain their posture while keeping their feet in the
same position during the experiment. Once their stance was stable, participants were exposed
to the “sensory congruent” and “sensory conflict” bal­
ance disturbance conditions in random order, each last­
ing 36 s. Between these conditions, there were 5-minute
breaks during which participants sat with their eyes
closed to prevent any carryover effects. The “sensory
congruent” condition simulated natural rotation move­
ment in a stationary scene. Under this condition, the
rotating platform was set to rotate clockwise at 30°/s, and
the VR headset, following the internal sensors detecting
the participant’s movement, adjusted the scene to rotate
counterclockwise at the same rate of 30°/s relative to the
participant’s eyes. The entire rotation process lasted 36 s,
with the acceleration and deceleration phases completed
within 2 s, maintaining a steady clockwise speed of 30°/s
in the middle phase. This rotation speed was determined
in preliminary trials to sufficiently stimulate neural activ­
ity without significantly interfering with the EEG data. The rotation speed of 30°/s was chosen based on previous
studies investigating postural responses to platform rota­
tions and sensory conflicts and pilot testing, representing
a balance between inducing a measurable sensory con­
flict and postural challenge. The “sensory conflict” con­
dition aimed to provide participants with a visual scene
expected during a counterclockwise rotation while they
were rotating clockwise. In this condition, the rotating
platform also rotated clockwise at 30°/s; however, the VR
headset, in addition to following the participant’s move­
ment, added an extra counterclockwise rotation speed
twice that of the original, making the visual scene appear
to rotate clockwise at 30°/s relative to the participant’s
motion, as if they were rotating counterclockwise at
30°/s. This condition lasted 36  s, with acceleration and
deceleration phases within 2 s and a steady speed of 30°/s
in the middle phase. Data collection and preprocessing
The collection of COP data was conducted with a Wii
Balance Board manufactured by Nintendo in Kyoto, Japan. The balance board was positioned at the midpoint
of the rotating platform, and the data were sampled at
a rate of 100 Hz. Prior research has confirmed the pre­
cision and dependability of the Wii Balance Board in
measuring COP [24, 25]. EEG data were collected using
a 64-channel EEG cap (EE-225, ANT Neuro, Hengelo, The Netherlands). A conductive gel was applied on every
electrode after placement to prevent impedance from
exceeding 20 kΩ to promote good signal quality in the
recording. The COP signals were initially processed with a fourth-
order Butterworth low-pass filter with a cutoff frequency
of 20 Hz to eliminate high-frequency noise beyond this
threshold potentially due to equipment noise or other
non-postural dynamics not relevant for postural stabil­
ity. The sway area, which is a typical index of the overall
postural stability, was estimated for the processed COP
data. The sway area measure usually reflects overall pos­
tural stability and is achieved by estimating an ellipse for
the COP data in the anteroposterior and mediolateral
directions. The ellipse encloses 95% of the COP move­
ment area, thereby providing a quantitative measure of
the sway area [26]. The raw EEG data underwent several preprocessing
steps using custom scripts incorporating functions from
the EEGLAB toolbox (R2023b; ) running in MATLAB
(R2023b; The MathWorks, Inc., Natick, MA, USA) to
attenuate artifacts and isolate neural activity. The data
were band-pass filtered in the range of 2–48 Hz using a
Finite Impulse Response filter to attenuate very low- and
high-frequency noise. Although the recording environ­
ment included shielding, a 50  Hz notch filter (imple­
mented via the Cleanline plugin in EEGLAB) was applied
to remove any residual power line noise potentially intro­
duced by the VR system, rotating platform motors, or
other auxiliary equipment operating nearby [27]. Given that the experimental setup involving stand­
ing balance on a rotating platform within VR inevita­
bly induced movement artifacts, further cleaning was
performed using the Artifact Subspace Reconstruction
(ASR) method [28]. ASR is an automated, component-
based technique that effectively removes large and
transient artifacts, such as artifacts related to body move­
ments. We set the ASR threshold at 20 standard devia­
tions in this study. This specific threshold, in conjunction
with subsequent ICA, has demonstrated effectiveness

Page 5 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
Fig. 1  Schematic diagram of the experimental setup and installation. The schematic diagram illustrates the experimental setup used to study the impact
of Tai Chi on postural control under sensory perturbation conditions. Participants stood barefoot on a Wii Balance Board placed in the center of a rotating
platform, with a virtual reality (VR) headset providing visual stimuli. Two conditions were tested: “sensory congruent” and “sensory conflict.” In the sensory
congruent condition, visual and actual rotational movements were aligned, whereas in the sensory conflict condition, the visual scene was counter-
rotated to create a mismatch between visual and proprioceptive inputs. Electroencephalographic (EEG) data were recorded using a 64-channel EEG cap,
and center of pressure (COP) data were collected to assess postural stability

Page 6 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
in handling artifacts during standing balance and walk­
ing tasks in previous studies [14, 29, 30]. Accordingly,
data points with a standard deviation over 20 times the
overall data standard deviation were regarded as artifacts
and removed, particularly in datasets most affected by
artifacts, a minimum of 75% of the original data dura­
tion was preserved across all participants. On average,
93.3% (mean) ± 4.4% (SD) of the data was retained follow­
ing ASR cleaning. This level of data cleaning was deemed
essential due to the unavoidable presence of motion-
related artifacts intrinsic to dynamic balance tasks per­
formed within VR. Following ASR, Independent Component Analysis
(ICA) using the extended Infomax algorithm was per­
formed to further refine the data. The sequential appli­
cation of ASR followed by ICA was chosen to leverage
their complementary strengths in artifact removal. ASR
effectively addresses the large-amplitude, non-stationary
artifacts (e.g., sudden movements, electrode pops) that
can severely disrupt EEG signals and potentially vio­
late the assumptions underlying ICA, thereby hindering
its decomposition quality. Relying solely on ICA might
fail to adequately remove these large-scale artifacts or
could lead to their influence contaminating the estima­
tion of other components. Conversely, attempting to use
ASR to remove all types of artifacts, including lower-
amplitude physiological ones like eye blinks or specific
muscle activities that ICA excels at identifying, could
necessitate overly aggressive thresholding and result in
excessive data loss. By first using ASR to clean the most
disruptive, high-variance artifacts, we create a dataset
more amenable to robust ICA decomposition. ICA can
then more effectively separate the remaining signal into
maximally independent components (ICs), allowing for
the precise identification and removal of residual physi­
ological artifacts (e.g., eye blinks, lateral eye movements,
tonic muscle activity) based on their characteristic spa­
tial topographies and temporal features. ICs classified by
ICLabel as having a high probability (> 0.8) of represent­
ing non-brain activity (muscle, eye, channel noise, etc.)
were subsequently removed from the data before further
analysis [31]. EEG source analysis
To estimate the neural activity originating from spe­
cific cortical regions rather than scalp electrodes, which
are affected by volume conduction, we performed EEG
source localization. Source space analysis was performed
in two stages: forward and inverse modeling. The ICBM-
152 brain template was used to generate a forward model
using the Boundary Element Method. This approach
has been proven to simulate the EEG signal propaga­
tion properties on the scalp with high accuracy; thus,
it provides sound underpinning for source reconstruc­
tion. In this study, the forward model was not generated
using participant magnetic resonance imaging (MRI)
data; instead, it was generated using a standardized
head model. This is based on the assumption that the
brain anatomy of all participants is similar to standard­
ized brain anatomical structures. Although this approach
does not account for anatomical differences among indi­
viduals, it is feasible and commonly used in cases where
individual MRI data are not available [32]. The inverse model computed in this experiment used
a well-known standardized low-resolution brain elec­
tromagnetic tomography (sLORETA) method [33].
sLORETA is a distributed source localization method
that provides smooth and physiologically plausible solu­
tions for EEG source imaging. It is used extensively
because it can provide zero-error localization in the pres­
ence of measurement and model errors under ideal con­
ditions [34]. The source reconstruction focused primarily on cor­
tical regions, as the synchronous activity of cortical
neurons is the predominant origin of EEG signals. The
reconstructed source activity time-series were averaged
within eight predefined Regions of Interest (ROIs) based
on the Brodmann atlas template mapped onto the ICBM-
152 standard brain [35]. These ROIs were selected a pri­
ori based on their known involvement in sensorimotor
control and visual processing (see Table 1). Directed functional connectivity computation
To investigate how TC practitioners integrate sensory
information under perturbation, we employed gener­
alized partial directed coherence (GPDC) to estimate
directed effective connectivity among the eight ROIs
within the mu frequency band (8–13 Hz). Effective con­
nectivity analysis was performed using the Source Infor­
mation Flow Toolbox (SIFT) (v1.0) implemented in
EEGLAB/MATLAB [36]. GPDC is a powerful method for
assessing directed functional connectivity [37]. It can dis­
criminate between direct and indirect interactions among
different structures. This feature makes it particularly
Table 1  Region of interest (ROI) definitions
ROI Abbreviation
Full Name
Included
Brodmann
Areas (BA)
LS1
Left Somatosensory Cortex
1, 2, 3
RS1
Right Somatosensory Cortex
1, 2, 3
LM1
Left Motor Cortex
4, 6
RM1
Right Motor Cortex
4, 6
LPPC
Left Posterior Parietal Cortex
5, 7
RPPC
Right Posterior Parietal Cortex
5, 7
LVC
Left Visual Cortex
17, 18, 19
RVC
Right Visual Cortex
17, 18, 19

Page 7 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
well suited for analyzing complex brain network dynam­
ics in the context of sensorimotor integration. The computation of GPDC involves the following steps. First, a multivariable autoregressive (MVAR) model is
fitted to preprocessed EEG data. The optimal model
order ‘p’ was determined individually for each dataset
by minimizing the Akaike Information Criterion (AIC)
over a range of plausible orders (1 to 30). AIC balances
model goodness-of-fit (likelihood) against model com­
plexity (number of parameters), providing a standard
criterion for model selection [38]. The median optimal
order across participants was found to be p = 20, and this
order was used consistently for all subsequent MVAR
model fitting. The MVAR model was used to provide a
frequency-domain representation of directed connectiv­
ity, which was applied to analyze the interactions within
specific frequency bands. This study focused on the fre­
quency band of the mu rhythm (8–13  Hz) because of
its critical role in sensorimotor integration. The GPDC
values for all the pairs of signal channels were then cal­
culated to provide a directed connectivity matrix repre­
senting the causal dependencies of the various channels
within the EEG network. The validity of the fitted MVAR model for each partici­
pant’s data was assessed using standard diagnostic tests
implemented in SIFT: [1] Model Consistency [2], Model
Stability, and [3] Residual Whiteness. To assess consis­
tency, data simulation using the model was performed
and then the Euclidean norm was calculated between
the correlation matrix of the real and simulated data
[39]. The statistic is measured on a scale of 0 to 100%,
where greater percentages indicate a greater correlation
between the model and the structure of the data. Stabil­
ity was confirmed by analyzing the logarithm of the high­
est eigenvalue in the coefficient matrix of the model. A
negative number indicates the stability of the model. In
addition, the whiteness of the residuals was evaluated
using an autocorrelation function test in conjunction
with confidence intervals [40]. The result is represented
as a numerical number ranging from zero to one, indi­
cating the probability that the residuals exhibit a white
noise pattern. A high value suggests that the residuals
are free of correlation structures that are not captured
by the model, thus increasing the confidence in the mod­
el’s accuracy. These validation steps confirmed that our
model provided a robust representation of the underlying
EEG data, ensuring a reliable and meaningful interpreta­
tion of the GPDC results. Based on the GPDC-derived directed connectivity
matrix, we further analyzed both the global and local
network characteristics. The global efficiency of the net­
work was computed to assess the extent to which infor­
mation was exchanged across the brain network. Given
the potential independent roles of visual integration and
sensorimotor integration, we divided the global effi­
ciency calculation into three networks: the overall net­
work, visual integration network (comprising four nodes: LPPC, RPPC, LVC, RVC), and sensory-motor integration
network (comprising six nodes: LS1, RS1, LM1, RM1,

## LPPC, RPPC). For local network properties, we calculated the strength
of each node, which was further divided into in-strength
and out-strength. In-strength, the sum of weighted
incoming connections to a node, reflects the total influ­
ence received by that region. Out-strength, the sum of
weighted outgoing connections from a node, reflects the
total influence exerted by that region on others. Statistical analysis
We used a 2 (Group: TC, Control) × 2 (Condition: Congruent, Conflict) mixed-design analysis of vari­
ance (ANOVA) to assess the impact of TC training
(between-subject factor) and sensory information con­
gruence (within-subject factor) on sway area, global effi­
ciency, clustering coefficient, and the in-strength and
out-strength of the cortical nodes. These metrics were
calculated for the entire brain network, sensory-motor
integration cortex, and visual integration cortex to assess
overall and regional brain network efficiency and cluster­
ing, as well as local cortical interactions. For each ANOVA, we reported the F-statistic, p-value,
and partial eta-squared (η²) as a measure of effect size. Partial eta-squared (ηp2) values are interpreted with con­
ventional thresholds of 0.01, 0.06, and 0.14 representing
small, medium, and large effects, respectively. Signifi­
cant main effects and interactions were further explored
using post hoc pairwise comparisons with Bonferroni
correction to account for multiple testing. A p-value of
< 0.05 was considered statistically significant. All statis­
tical analyses were performed using. Statistical results
are reported consistently with two decimal places for
F-values and effect sizes, and three decimal places for
p-values. Results
Analysis of COP
To examine the effects of long-term TC training
(between-subject factor) and sensory information con­
gruence (within-subject factor) on the sway area (an indi­
cator of postural stability), we conducted a mixed-design
ANOVA. The ANOVA revealed significant main effects of
Group (F(1,50) = 13.77, p < 0.001, ηp2 = 0.22) and Condi­
tion (F(1,50) = 26.48, p < 0.001, ηp2 = 0.35). The Group ×
Condition interaction was not significant (F(1,50) = 0.11,
p = 0.738, ηp2 = 0.002). Specifically, the TC group exhib­
ited significantly smaller sway areas overall compared to
the Control group. Independently, the sensory conflict

Page 8 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
condition resulted in significantly larger sway areas com­
pared to the congruent condition across both groups
(Fig. 2). EEG model validation
To confirm the adequacy of the multivariate autoregres­
sive (MVAR) models that form the basis of our gener­
alized partial directed coherence (GPDC) analysis, we
quantified three standard validation metrics: (i) percent
consistency, (ii) residual whiteness probability (RWP),
and (iii) stability index. Percent consistency expresses the proportion of the
empirical cross-spectra that the model can reproduce;
values > 80% are generally interpreted as “good”. RWP is
the fraction of model windows in which the Ljung–Box
portmanteau test fails to reject the null hypothesis of
white residuals at α = 0.05 and ≥ 0.95 as ideal. The stability
index is the maximum modulus of the MVAR compan­
ion-matrix eigenvalues; negative values indicate that all
poles lie inside the unit circle, i.e., a stationary and hence
stable solution. Table 2 summarises the group means ± SD. All condi­
tions exhibited high consistency (92–95%), confirming
that the selected model order captured the bulk of tem­
poral dependencies. The residual-whiteness probability
averaged 0.916 ± 0.024. Although marginally below the
ideal 0.95 threshold, a probability above 90% is generally
considered acceptable in MVAR modeling. The stabil­
ity index was negative for every subject (range − 0.38 to
− 0.12), satisfying the requirement that all eigenvalues lie
inside the unit circle. Overall, these metrics demonstrate that the fitted
MVAR models are stable, internally consistent, and free
of substantial residual structure. The moderate (< 8%)
departure from perfect whiteness is well within the range
reported in previous EEG studies that adopted the same
criteria and therefore does not compromise the reliability
of the subsequent GPDC estimates. Global network metrics of directed brain network analysis
We utilized GPDCderived from the validated MVAR
models to estimate the directed brain networks between
eight predefined cortical regions of interest (ROIs, see
Table 2  Model fitting results (n = 38)
Group
Control
Tai Chi
Sensory
Congruent
Conflict
Congruent
Conflict
Residual Whiteness
Likelihood
0.93 (0.031)
0.92 (0.033)
0.91 (0.036)
0.91
(0.039)
Stability Index
-0.23 (0.038)
-0.20 (0.079)
-0.23 (0.037)
-2.2
(0.0275)
Consistency (%)
95 (2.3)
94 (5.2)
93 (4.3)
92 (5.1)
Values are presented as Mean (SD)
Fig. 2  Geometric sway measures. The figure displays geometric sway measures divided into left and right panels, representing sensory congruent and
sensory conflict conditions, respectively. Each panel compares the center of pressure (COP) sway trajectories of Tai Chi practitioners and non-practitioners. The trajectories shown are from a representative participant whose sway areas closely approximate the average sway areas across all participants. The
95% ellipse profile illustrates the sway area under each condition

Page 9 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
Fig. 3 (See legend on next page.)

Page 10 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
Methods 2.4 for definitions) under four conditions: TC
practitioners with sensory congruence, TC practitioners
with sensory conflict, control group with sensory congru­
ence, and control group with sensory conflict. Figure 3A
visualizes the average connectivity networks. Mixed-design ANOVAs were performed on global
network metrics (Fig.  3B). For global efficiency of the
entire brain network (Eglob) and the clustering coeffi­
cient (Clum - analysis not shown as original results were
non-significant), no significant main effects of Group or
Condition, nor any significant interactions were found
(all p > 0.050). For the sensory-motor integration cortex, there was
a significant main effect of sensory information con­
gruence on global efficiency (F [1, 40] = 10.32, p = 0.003,
ηp2 = 0.21), indicating that global efficiency within this
subnetwork was significantly higher during sensory con­
flict compared to the congruent condition. However,
the main effect of TC training was not significant, (F
[1, 40] = 0.11, p = 0.742, ηp2 = 0.00), and the interaction
effect was also non-significant (F [1, 40] = 0.01, p = 0.919,
ηp2 = 0.00). For the global efficiency of the visual integration net­
work (Eglobvc), a significant main effect of Condition
was found (F [1, 40] = 37.64, p < 0.001, ηp2 = 0.48), with
lower efficiency observed in the conflict condition com­
pared to the congruent condition across both groups. The
main effect of Group was not significant (F [1, 40] = 0.75,
p = 0.392,ηp2 = 0.02), and the Group × Condition interac­
tion approached significance (F [1, 40] = 3.00, p = 0.091,
ηp2 = 0.07). Local network metrics of directed brain network analysis
Mixed-design ANOVAs were used to analyze the in-
strength and out-strength for each of the eight cortical
ROIs. For in-strength, the ANOVAs revealed no signifi­
cant main effects of Group or Condition, nor any signifi­
cant Group × Condition interactions for any of the eight
ROIs (all p > 0.05). For out-strength (Fig. 4), the analysis revealed several
significant effects. Significant main effects of Condition
were found for the out-strength of LVC (F [1, 40] = 31.3
6,p < 0.001,ηp2 = 0.44) and RVC (F [1, 40] = 52.06,p < 0.00
1,ηp2 = 0.57). In both visual cortical regions, out-strength
was significantly lower in the conflict condition com­
pared to the congruent condition across both groups. The magnitude of this reduction appeared somewhat
larger in the right hemisphere (ηp2 = 0.57) compared to
the left hemisphere (ηp2=0.44), although this asymmetry
was not directly tested. For RS1, significant main effects were found for both
Condition (F [1, 40] = 5.47, p = 0.024, ηp² = 0.12) and
Group (F [1, 40] = 7.78, p = 0.008, ηp² = 0.16). The inter­
action was not significant (F [1, 40] = 0.22, p = 0.64, ηp² =
0.005). Both the conflict condition and Tai Chi training
led to an increase in RS1 out-strength. For RPPC, a significant main effect of Group was found
(F [1, 40] = 11.39, p = 0.002, ηp² = 0.22), indicating that Tai
Chi training significantly reduced RPPC out-strength,
compared to the Control group. Neither the Condition
nor the Interaction effects were significant (all p > 0.05). Discussion
This study investigated the effects of long-term TC train­
ing on underlying cortical mu-band effective connectivity
dynamics and postural control during sensory perturba­
tion. Using EEG effective connectivity analysis, we sought
to understand how long-term TC training influences the
ability of the brain to integrate sensory information to
maintain balance. The key statistically significant findings
were (Table  3): [1] TC practitioners exhibited superior
postural stability (reduced sway area) compared to con­
trols under both conditions; [2] Sensory conflict induced
changes in network efficiency across both groups,
decreasing efficiency in the visual integration network
while increasing efficiency in the sensorimotor integra­
tion network; [3] TC practitioners showed significantly
increased the out-strength of the right primary somato­
sensory cortex (S1) and decreased that of the right pos­
terior parietal cortex (PPC). These results provide novel
insights into the potential neuroplastic adaptations asso­
ciated with long-term TC practice that may contribute
to enhanced postural control, particularly in challenging
sensory environments.
(See figure on previous page.)
Fig. 3  Group-level µ-band connectivity and graph-metric summary. (A) Directed-connectivity heat-maps. Each 8 × 8 matrix shows the grand-average
GPDC value (row → column information flow) for the four experimental conditions: Control-Congruent, Control-Conflict, Tai Chi-Congruent and Tai
Chi-Conflict (upper-left, lower-left, upper-right, lower-right, respectively). Abbreviations—LM1: left motor cortex; RM1: right motor cortex; LS1: left so­
matosensory cortex; RS1: right somatosensory cortex; LPPC/RPPC: left/right posterior parietal cortex; LVC/RVC: left/right visual cortex. Colour follows a
power-normalised “turbo” scale (γ = 0.5): deep blue = weakest, red = strongest; connections below the group-wise 50 th percentile are masked white. Exact
MNI coordinates of all ROIs are provided in Methods 2.4 and Table 1. (B) Graph-theoretical indices. Dual-axis box-and-whisker plots illustrate (i) whole-
brain global efficiency (Eglob), (ii) whole-brain clustering coefficient (Clu), (iii) global efficiency of the sensorimotor-integration sub-network (Eglobmc;
comprising six nodes: LS1, RS1, LM1, RM1, LPPC, RPPC), and (iv) global efficiency of the visual-integration sub-network (Eglobvc). B; comprising four nodes: LPPC, RPPC, LVC, RVCox centre = median; hinges = 25 / 75 th percentiles; whiskers = 1.5 × IQR. + indicates a significant main effect of Condition; * indicates
a significant main effect of Group (two-way mixed ANOVA with Holm–Bonferroni correction). One, two and three symbols denote p < 0.05, p < 0.01 and
p < 0.001, respectively

Page 11 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
Effects on sway areas and postural control
Our study revealed that TC practitioners demonstrated
significantly better postural stability than did non-practi­
tioners under both sensory congruent and conflict condi­
tions. These findings underscore the effectiveness of TC
in enhancing balance and stability even when sensory
inputs are incongruent. These findings are consistent
with those of earlier studies that have shown the benefits
of TC in improving balance and reducing the risk of falls. For instance, Li et al. showed that TC practitioners had a
much better balance ability and lower rate of falling than
did controls [9]. Similarly, Wayne et al. concluded that
TC improved postural control and stability in an older
cohort [41]. While previous studies have primarily focused on
static conditions, our study uniquely demonstrates the
efficacy of TC under dynamic and challenging sensory
perturbations. This further underlines the robustness of
TC as an intervention for improving balance in complex
environments. Fig. 4  Out-strength of cortical nodes under the sensory congruent and conflict conditions. The box plots illustrates the out-strength values for eight
cortical nodes under sensory congruent (Cong) and sensory conflict (Incong) conditions for Tai Chi practitioners (TC) and the control group (CT). The
cortical nodes are defined in Table 1. Each subplot is a dual-axis box plot showing the out-strength distribution under the specified conditions. Plus
symbols (+) denote significant main effects of Condition; Asterisks (*) denote significant main effects of Group. Single symbols: p < 0.05; double symbols:
p < 0.01; triple symbols: p < 0.001

Page 12 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
Cortical network efficiency changes and sensory
Re-weighting
The analysis of global network efficiency revealed signifi­
cant effects of the sensory condition across both groups
(Table  3; Fig.  4). Our results further showed a clear
decrease in the global efficiency of the visual information
integration network under sensory conflict. This decrease
indicates that the brain relies less on visual input when it
is unreliable, and compensates by using more somatosen­
sory information for stabilization. This adaptive mecha­
nism is supported by the findings of previous studies
showing that conflicting sensory inputs lead to decreased
reliance on visual information and increased dependence
on somatosensory stimuli [42]. In contrast, the global efficiency of the somatosensory
information integration networks increased under sen­
sory conflict. This enhancement indicates that the brain
compensates for the increased processing of somatosen­
sory information, thereby enhancing effective postural
control despite the incongruence generated by visual
inputs. Previous studies have shown that the brain can
dynamically shift processing resources to utilize the most
reliable sensory modality under conditions of sensory
interference [43]. Our findings provide network-level evi­
dence for such re-weighting occurring within the mu fre­
quency band during sensory conflict, affecting both TC
practitioners and controls. Directed connectivity: enhanced somatosensory outflow in
Tai Chi practitioner
The application of GPDC in the current study provides a
fine-grained understanding of directed information inter­
actions within the brain with respect to postural con­
trol during sensory perturbations. We distinguished the
sources and destinations of in-strength and out-strength
from different cortical nodes by analyzing the values of
these parameters. Our results showed that chronic TC
training changed the out-strength of the somatosensory
cortices. The key finding differentiating the groups was the
significantly higher µband outstrength from the right
somatosensory cortex (RS1) in TC practitioners com­
pared with controls, along with an overall increase in
RS1 outstrength during the conflict condition across
both groups. Recalling that out-strength reflects the total
weighted directed influence a region exerts on the net­
work, this suggests that long-term TC training enhances
the effective outflow of processed somatosensory infor­
mation from these primary sensory regions to down­
stream areas potentially involved in postural control and
motor planning, particularly within the mu frequency
band linked to sensorimotor processing. This result sup­
ports those of previous studies suggesting that good
somatosensory integration is important for balance and
stability, particularly in difficult conditions [44, 45]. In contrast, Tai Chi training was associated with a sig­
nificant reduction in µ band out‑strength from the right
posterior parietal cortex (RPPC). Given the RPPC’s role
in multisensory integration and attentional re‑allocation,
this decrease might reflect a more efficient reliance on
proprioceptive cues, with less need for parietal‑medi­
ated compensatory processes when visual information is
unreliable [46]. Together, the heightened RS1 outstrength
and reduced RPPC outstrength may represent comple­
mentary neural adaptations whereby TC practitioners
prioritize accurate somatosensory inflow while stream­
lining parietal processing. Previous studies have suggested that TC practice
enhances sensory reweighting capabilities, particularly
increasing reliance on proprioceptive input [47, 48]. Our
findings provide a potential neural correlate for this phe­
nomenon at the level of cortical effective connectivity
within the mu frequency band. The increased somato­
sensory out-strength in TC practitioners suggests a more
Table 3  Summary of key statistical findings from 2 × 2 mixed ANOVAs
Dependent Variable
Main Effect: Group
(TC vs. CT)
Main Effect: Condition
(Conflict vs. Cong)
Interaction
Group × Condition
Behavioral
Sway Area
F(1, 50) = 13.77, p < 0.001, ηp² = 0.22 *
F(1, 50) = 26.48, p < 0.001, ηp² = 0.35 *
F(1, 50) = 0.11, p = 0.738, ηp² = 0.00
EEG Network Metrics (µ-band)
EglobSMC
F(1, 40) = 0.11, p = 0.742, ηp² = 0.00
F(1, 40) = 10.32, p = 0.003, ηp² = 0.21 *
F(1, 40) = 0.01, p = 0.919, ηp² = 0.00
EglobVC
F(1, 40) = 0.75, p = 0.392, ηp² = 0.02
F(1, 40) = 37.64, p < 0.001, ηp² = 0.48 *
F(1, 40) = 3.00, p = 0.091, ηp² = 0.07
Out-Strength
LVC
F(1, 40) = 0.01, p = 0.910, ηp² = 0.00
F(1, 40) = 31.36, p < 0.001, ηp² = 0.44 *
F(1, 40) = 2.16, p = 0.150, ηp² = 0.05
RVC
F(1, 40) = 0.70, p = 0.407, ηp² = 0.02
F(1, 40) = 52.06, p < 0.001, ηp² = 0.57 *
F(1, 40) = 0.79, p = 0.379, ηp² = 0.02
RS1
F(1, 40) = 7.78, p = 0.008, ηp² = 0.16 *
F(1, 40) = 5.47, p = 0.024, ηp² = 0.12 *
F(1, 40) = 0.22, p = 0.640, ηp² = 0.01
RPPC
F(1, 40) = 11.39, p = 0.002, ηp² = 0.22 *
All p > 0.05
All p > 0.05

## LM1, RM1, LPPC, LS1

All p > 0.05
All p > 0.05
All p > 0.05
In-Strength (all ROIs)
All p > 0.05
All p > 0.05
All p > 0.05
*** p < 0.01; Eglobsmc = Global Efficiency Sensorimotor Network; Eglobvc = Global Efficiency Visual Network; LVC/RVC = Left/Right Visual Cortex; LS1/RS1 = Left/Right
Somatosensory Cortex

Page 13 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
robust or efficient channeling of relevant sensory infor­
mation within the cortical network, facilitating adaptive
postural responses. Limitations and future research directions
Although our study provides significant insights into the
effects of long-term TC training on cortical connectiv­
ity and postural control under sensory perturbation, it
is important to acknowledge some limitations that may
influence the interpretation and generalizability of our
findings. First, the study focused exclusively on young, healthy,
highly experienced TC practitioners. While this allowed
us to isolate the effects of extensive training while mini­
mizing age-related confounds, it limits the direct gener­
alizability of these specific findings to older adults, who
represent a primary population for TC balance interven­
tions. The patterns of cortical adaptation might differ
in older individuals due to age-related changes in brain
structure, function, and baseline postural control mecha­
nisms. Future research should specifically investigate mu-
band and other frequency band connectivity adaptations
in middle-aged and older TC practitioners, potentially
using longitudinal designs to track changes with training
initiation. Second, we used a highly controlled VR and rotating
platform setup to create one specific type of sensory con­
flict (continuous yaw rotation mismatch). This is a some­
what artificial scenario compared to everyday balance
challenges, which can involve translational perturbations,
slips, trips, uneven surfaces, or cognitive distractions. The ecological validity of our findings is thus limited –
they apply to a sustained visual-vestibular conflict. It
would be erroneous to assume the same neural adjust­
ments happen for, say, a sudden push or a vestibular
loss scenario. Moreover, our perturbation was relatively
short-term; we don’t know how sustained exposure (min­
utes rather than seconds) would influence connectivity
(maybe some habituation occurs). Third, this study focused solely on cortical dynamics
recorded via EEG. The absence of concurrent electro­
myography (EMG) recordings prevented the analysis of
corticomuscular coherence (CMC) or directed cortico­
muscular connectivity. CMC provides insights into the
direct functional coupling between the motor cortex and
active muscles during postural tasks. Investigating how
TC practice modulates CMC, particularly in lower limb
muscles crucial for balance, would complement the cur­
rent findings on cortico-cortical interactions and provide
a more complete picture of the neuromuscular adapta­
tions. Future studies integrating simultaneous EEG and
EMG are warranted. Fourth, the use of a standard head model for EEG
source localization rather than individual MRI data may
have introduced inaccuracies in identifying the exact
neural sources of the observed EEG signals. Individual
anatomical differences can influence the precision of
source localization, and future studies should consider
incorporating personalized head models to improve
accuracy. Finally, although the sample size was relatively small,
it was adequate for detecting significant effects. Larger
sample sizes would increase the generalizability of the
findings and provide greater statistical power for detect­
ing subtle effects. Additionally, the cross-sectional design
limits causal inferences; longitudinal studies tracking
individuals as they undertake TC training would be nec­
essary to definitively establish that the observed differ­
ences in brain connectivity are caused by the practice
itself. Future research should aim to address these limitations
by studying older populations, employing more varied
and ecologically valid paradigms, analyzing multiple fre­
quency bands and corticomuscular coupling, utilizing
individual head models, and incorporating longitudinal
designs. Conclusions
This study demonstrated that long-term TC practice
enhanced postural stability and reorganized corti­
cal connectivity under sensory perturbation. Crucially,
this behavioral advantage was accompanied by specific,
quantifiable differences in mu-band (8–13  Hz) cortical
effective connectivity patterns compared to non-prac­
ticing controls. While sensory conflict induced adap­
tive changes in network efficiency (decreased visual,
increased sensorimotor) across both groups, TC practi­
tioners exhibited significantly greater information out­
flow from the right somatosensory cortex (RS1) and,
simultaneously, reduced outflow from the right pos­
terior parietal cortex (RPPC). These complementary
adaptations suggest that extensive TC training may fos­
ter neuroplastic changes that amplify the utilization of
somatosensory information while streamlining parietal
integration processes for postural control. The enhanced
somatosensory out-strength observed in TC practitio­
ners provides a potential neural substrate underlying
their superior balance performance in challenging envi­
ronments. These results elucidate possible neural mech­
anisms contributing to the well-documented balance
benefits of TC and highlight its potential as an interven­
tion that may promote beneficial central neuroplasticity. Abbreviations
ANOVA
Analysis of variance
ASR
Artifact subspace reconstruction
COP
Center of pressure
EEG
Electroencephalography
MVAR
Multivariate autoregression
GPDC
Generalized partial directed coherence

Page 14 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120
MRI
Magnetic resonance imaging
ROIs
Regions of interest
sLORETA
Standardized low-resolution brain electromagnetic tomography
TC
Tai chi
VR
Virtual reality
Acknowledgements
The authors would like to thank the participants for supporting our study and
the students for helping with data collection. Author contributions
GZW: Writing–original draft, Writing–review & editing, Conceptualization, Data curation, Methodology, and Visualization. XXL: Writing–original draft, Writing–review & editing, Software, Methodology, Formal analysis, and
Visualization. YMC: Writing–review & editing, Investigation, and Data curation. JW: Writing–review & editing and Resources. YG: Writing–review & editing, Conceptualization, Investigation, Methodology, and Resources. JL: Writing–
review & editing, Conceptualization, Investigation, Methodology, Supervision, Project. Funding
This research was funded by the Zhejiang Provincial Medical and Health
Science Research Fund Committee, grant number WKJ-ZJ-2334. Funding
was also provided by the National Defense Foundation Strengthening
Program Technology Field Fund Project of China (2021-JCJQ-JJ-1029) and
the Key Research and Development Program of Zhejiang Province (Grant No.
2025C01135). Data availability
The datasets used and/or analyzed during the current study available from the
corresponding author on reasonable request. Declarations
Ethics approval and consent to participate
The study was approved by the Ethics Committee of Zhejiang University
Psychological Science Research Center (2024.011). The study procedures were
thoroughly explained to all individuals, and written informed consent was
obtained prior to participation. Consent for publication
Not applicable. Competing interests
The authors declare no competing interests. Author details
1Taizhou Key Laboratory of Medical Devices and Advanced Materials, Taizhou Institute of Zhejiang University, Taizhou 318000, China
2Key Laboratory for Biomedical Engineering of Ministry of Education, College of Biomedical Engineering & Instrument Science, Zhejiang
University, 866 Yuhangtang Road, Hangzhou 310058, China
3Department of Sports Science, College of Education, Zhejiang University, Hangzhou 310058, China
4Center for Psychological Science, Zhejiang University, Hangzhou
310058, China
Received: 26 August 2024 / Accepted: 13 May 2025
References
1. Kandel ER, Schwartz JH, Jessell TM, Siegelbaum S, Hudspeth AJ, Mack S. Principles of neural science: McGraw-hill New York 2000.
2. Horak FB. Postural orientation and equilibrium: what do we need to
know about neural control of balance to prevent falls? Age Ageing.
2006;35(suppl2):ii7–11.
3. Li F. Transforming traditional Tai Ji Quan techniques into integrative move­
ment therapy—Tai Ji Quan: moving for better balance. J Sport Health Sci.
2014;3(1):9–15.
4. Wayne PM, Kaptchuk TJ. Challenges inherent to T’ai Chi research: part II—
defining the intervention and optimal study design. J Altern Complement
Med. 2008;14(2):191–7.
5. Wang C, Schmid CH, Rones R, Kalish R, Yinh J, Goldenberg DL, et al. A ran­
domized trial of Tai Chi for fibromyalgia. New Engl J Med. 2010;363(8):743–54.
6. Hu X, Lai Z, Wang L. Effects of Taichi exercise on knee and ankle proprio­
ception among individuals with knee osteoarthritis. Res Sports Med.
2020;28(2):268–78.
7. Courel-Ibáñez J, Buendía-Romero Á, Pallarés JG, García-Conesa S, Martínez-
Cava A, Izquierdo M. Impact of tailored multicomponent exercise for prevent­
ing weakness and falls on nursing home residents’ functional capacity. J Am
Med Dir Assoc. 2022;23(1):98–104. e3.
8. Li G, Huang P, Cui S-S, Tan Y-Y, He Y-C, Shen X, et al. Mechanisms of motor
symptom improvement by long-term Tai Chi training in Parkinson’s disease
patients. Translational Neurodegeneration. 2022;11(1):6.
9. Li F, Harmer P, Fitzgerald K, Eckstrom E, Akers L, Chou L-S, et al. Effectiveness of
a therapeutic Tai Ji Quan intervention vs a multimodal exercise intervention
to prevent falls among older adults at high risk of falling: a randomized clini­
cal trial. JAMA Intern Med. 2018;178(10):1301–10.

### 10. He T, Hu Z. Effects of Tai Chi Chuan on cortical sources of EEG rhythms in

the resting state in elderly individuals: a cross-sectional study. NeuroReport.
2022;33(4):180.

### 11. Hua A, Wang G, Bai J, Hao Z, Liu J, Meng J, et al. Nonlinear dynamics of

postural control system under visual-vestibular habituation balance practice:
evidence from EEG, EMG and center of pressure signals. Front Hum Neurosci.
2024;18:1371648.

### 12. Wei GX, Xu T, Fan FM, Dong HM, Zuo XN. Can Taichi reshape the brain?? A

brain? morphometry study. PLoS ONE. 2013;8(4):e61038.

### 13. Lu X, Siu KC, Fu SN, Hui-Chan CWY, Tsang WWN. Effects of Tai Chi training on

postural control and cognitive performance while dual tasking– a random­
ized clinical trial. J Complement Integr Med. 2016;13(2):181–7.

### 14. Peterson SM, Ferris DP. Group-level cortical and muscular connectiv­

ity during perturbations to walking and standing balance. NeuroImage.
2019;198:93–103.

### 15. Wang G, Yang Y, Wang J, Hao Z, Luo X, Liu J. Dynamic changes of brain net­

works during standing balance control under visual conflict. Front Neurosci-
Switz. 2022;16.

### 16. Wang G, Yang Y, Dong K, Hua A, Wang J, Liu J. Multisensory conflict impairs

Cortico-Muscular network connectivity and postural stability: insights from
partial directed coherence analysis. Neurosci Bull. 2024;40(1):79–89.

### 17. Li L, Zhang M, Chen Y, Wang K, Zhou G, Huang Q. TAGL: Temporal-Guided

adaptive graph learning network for coordinated movement classification. IEEE Trans Industr Inf. 2024;20(11):12554–64.

### 18. Wang X, Li W, Song R, Ao D, Hu H, Li L. Corticomuscular coupling altera­

tions during elbow isometric contraction correlated with clinical scores:
an fNIRS-sEMG study in stroke survivors. IEEE Trans Neural Syst Rehabil Eng.
2025;33:696–704.

### 19. Dong K, Zhang D, Wei Q, Wang G, Chen X, Zhang L et al. An integrated infor­

mation theory index using multichannel EEG for evaluating various States of
consciousness under anesthesia. Comput Biol Med. 2023;153.

### 20. Liu J, Dong K, Sun Y, Kakkos I, Huang F, Wang G, et al. Progress of brain

network studies on anesthesia and consciousness: framework and clinical
applications. Engineering. 2021;20:77–95.

### 21. Friston KJ. Functional and effective connectivity: a review. Brain Connect.

2011;1(1):13–36.

### 22. Fallani FDV, Costa LF, Rodriguez FA, Astolfi L, Vecchiato G, Toppi J et al. A

graph-theoretical approach in brain functional networks. Possible implica­
tions in EEG studies. Nonlinear Biomedical Phys. 2010;4(S1).

### 23. Sabate M, Llanos C, Enriquez E, Rodriguez M. Mu rhythm, visual processing

and motor control. Clin Neurophysiol. 2012;123(3):550–7.

### 24. Huurnink A, Fransz DP, Kingma I, van Dieën JH. Comparison of a laboratory

grade force platform with a Nintendo Wii balance board on measure­
ment of postural control in single-leg stance balance tasks. J Biomech.
2013;46(7):1392–5.

### 25. Leach JM, Mancini M, Peterka RJ, Hayes TL, Horak FB. Validating and calibrat­

ing the Nintendo Wii balance board to derive reliable center of pressure
measures. Sensors-Basel. 2014;14(10):18244–67.

### 26. Paillard T, Noe F. Techniques and methods for testing the postural function in

healthy and pathological subjects. Biomed Res Int. 2015;2015.

### 27. Delorme A, Makeig S. EEGLAB: an open source toolbox for analysis of single-

trial EEG dynamics including independent component analysis. J Neurosci
Methods. 2004;134(1):9–21. Page 15 of 15
Wang et al. Journal of NeuroEngineering and Rehabilitation (2025) 22:120

### 28. Chang CY, Hsu SH, Pion-Tonachini L, Jung TP. Evaluation of artifact subspace

reconstruction for automatic artifact components removal in Multi-Channel
EEG recordings. IEEE Trans Biomed Eng. 2020;67(4):1114–21.

### 29. Shenoy Handiru V, Alivar A, Hoxha A, Saleh S, Suviseshamuthu ES, Yue GH,

et al. Graph-theoretical analysis of EEG functional connectivity during bal­
ance perturbation in traumatic brain injury: A pilot study. Hum Brain Mapp.
2021;42(14):4427–47.

### 30. Artoni F, Fanciullacci C, Bertolucci F, Panarese A, Makeig S, Micera S, et al. Unidirectional brain to muscle connectivity reveals motor cortex control of
leg muscles during stereotyped walking. NeuroImage. 2017;159:403–16.

### 31. Pion-Tonachini L, Kreutz-Delgado K, Makeig S. ICLabel: an automated electro­

encephalographic independent component classifier, dataset, and website. NeuroImage. 2019;198:181–97.

### 32. Huang Y, Parra LC, Haufe S. The new York Head—A precise standardized

volume conductor model for EEG source localization and tES targeting. NeuroImage. 2016;140:150–62.

### 33. Pascual-Marqui RD. Standardized low-resolution brain electromagnetic

tomography (sLORETA): technical details. Methods Find Exp Clin Pharmacol.
2002;24:5–12. Suppl D(Suppl D).

### 34. Grech R, Cassar T, Muscat J, Camilleri KP, Vanrumste B. Review on solving

the inverse problem in EEG source analysis. J Neuroeng Rehabilitation.
2008;5(1):25.

### 35. Zilles K, Amunts K. Centenary of Brodmann’s map—conception and fate. Nat

Rev Neurosci. 2010;11(2):139–45.

### 36. Delorme A, Mullen T, Kothe C, Acar ZA, Makeig S. EEGLAB, SIFT, NFT, BCILAB,

and ERICA: new tools for advanced EEG processing. Comput Intell Neurosci.
2011;2011:1687–5265.

### 37. Baccala LA, Sameshima K, Takahashi DY, editors. Generalized partial directed

coherence. 2007 15th International conference on digital signal processing

### 2007. Ieee.

### 38. Akaike H. Citation Classic - a new look at the Statistical-Model identification. Cc/Eng Tech Appl Sci. 1981;51:22.

### 39. Ding MZ, Bressler SL, Yang WM, Liang HL. Short-window spectral analysis

of cortical event-related potentials by adaptive multivariate autoregressive
modeling: data preprocessing, model validation, and variability assessment. Biol Cybern. 2000;83(1):35–45.

### 40. Taylor R. New introduction to multiple time series analysis. Int J Forecast.

2007;23(1):153.

### 41. Wayne PM, Gow BJ, Costa MD, Peng C-K, Lipsitz LA, Hausdorff JM, et al. Complexity-based measures inform effects of Tai Chi training on standing
postural control: cross-sectional and randomized trial studies. PLoS ONE.
2014;9(12):e114731.

### 42. Domingos C, Pêgo J, Santos N. Effects of physical activity on brain func­

tion and structure in older adults: A systematic review. Behav Brain Res.
2021;402:113061.

### 43. Taubert M, Draganski B, Anwander A, Müller K, Horstmann A, Villringer

A, et al. Dynamic properties of human brain structure: learning-related
changes in cortical areas and associated fiber connections. J Neurosci.
2010;30(35):11670–7.

### 44. Song Q, Zhang X, Mao M, Sun W, Zhang C, Chen Y, et al. Relationship of

proprioception, cutaneous sensitivity, and muscle strength with the balance
control among older adults. Ournal Sport Health Sci. 2021;10(5):585–93.

### 45. Fetsch CR, Pouget A, DeAngelis GC, Angelaki DE. Neural correlates of

reliability-based cue weighting during multisensory integration. Nat Neuro­
sci. 2011;15(1):146–54.

### 46. Tsang WW, Wong VS, Fu SN, Hui-Chan CW. Tai Chi improves standing balance

control under reduced or conflicting sensory conditions. Archives Phys Med
Rehabilitation. 2004;85(1):129–37.

### 47. Tsang WW, Hui-Chan CW. Standing balance after vestibular stimulation in Tai

Chi–practicing and nonpracticing healthy older adults. Archives Phys Med
Rehabilitation. 2006;87(4):546–53.

### 48. Cui J, Hao Z, Tian H, Yang Y, Wang J, Lin X. The effects of Tai Chi on standing

balance control in older adults May be attributed to the improvement of
sensory reweighting and complexity rather than reduced sway velocity or
amplitude. Front Aging Neurosci. 2024;16:1330063. Publisher’s note
Springer Nature remains neutral with regard to jurisdictional claims in
published maps and institutional affiliations.
