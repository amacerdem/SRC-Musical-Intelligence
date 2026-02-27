# Directional hand movement can

**Year:** D:20

---

Directional hand movement can
be classified from insular cortex
SEEG signals using recurrent neural
networks and high-gamma band
features
Xiecheng Shao1,6, Ryan S. Chung1,2,3,6, Jonathon M. Cavaleri1, Roberto Martin Del Campo-Vera1, Miguel Parra1, Shivani Sundaram1, Selena Zhang1, Ashwitha Surabhi1, Ryan J. McGinn2,3,4, Charles Y. Liu1,2,3,4, Spencer S. Kellis1,2,3,4,5 &
Brian Lee1,2,3,4
Motor BCIs, with the help of Artificial Intelligence (AI) and machine learning, have shown promise in
decoding neural signals for restoring motor function. Structures beyond motor cortex have provided
additional sources for movement signals. New evidence points to the role of the insula in motor control,
specifically directional hand-movements. In this study, we applied AI and machine learning techniques
to decode directional hand-movements from high-gamma band (70–200 Hz) activity in the insular
cortex. Seven participants with medication-resistant epilepsy underwent stereo electroencephalographic
(SEEG) implantation of depth electrodes for seizure monitoring in the insula. SEEG data were sampled
throughout a cued motor task involving three conditions: left-hand movement, right-hand movement,
or no movement. Neural signal processing focused on high-gamma band activity. Demixed Principal
Component Analysis (dPCA) was used for dimension reduction (d = 10) and feature extraction from the time-
frequency analysis. For movement classification, we implemented a bidirectional Long Short-Term Memory
(LSTM) architecture with a single layer, utilizing the capacity to process temporal sequences in forward
and back directions for optimal decoding of movement direction. Our findings revealed robust directional-
specific high-gamma modulation within the insular cortex during motor execution. Temporal decomposition
through dPCA demonstrated distinct spatiotemporal patterns of high-gamma activity across movement
conditions. Subsequently, LSTM networks successfully decoded these condition-specific neural signatures,
achieving a classification accuracy of 72.6% ± 13.0% (mean ± SD), which significantly exceeded chance-level
performance of 33.3% (p < 0.0001, n = 16 sessions). Furthermore, we identified a strong negative correlation
between temporal distance of training-testing sessions and decoding performance (r = -0.868, p < 0.0001),
indicating temporal difference of the neural representations. Our study highlights the potential role of deep
brain structures, such as the insula, in conditional movement discrimination. We demonstrate that LSTM
networks and high-gamma band analysis can advance the understanding of neural mechanisms underlying
movement. These insights may pave the way for improvements in SEEG-based BCI. Keywords  SEEG, Insula, Insular cortex, BCI, AI, Neural networks
1Department of Neurological Surgery, Keck School of Medicine of USC, University of Southern California, 1200 N
State Street, Suite 3300, Los Angeles 90033, CA, USA. 2Keck School of Medicine of USC, University of Southern
California, Los Angeles, CA, USA. 3Department of Neurology, Keck School of Medicine of USC, University of
Southern California, Los Angeles, CA, USA. 4Department of Biology and Biological Engineering, California Institute
of Technology, Pasadena, CA, USA. 5Tianqiao and Chrissy Chen Brain-Machine Interface Center, Chen Institute
for Neuroscience, California Institute of Technology, Pasadena, CA, USA. 6Xiecheng Shao and Ryan S. Chung
contributed equally. email: rschung@usc.edu
OPEN
Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports

Traditionally, brain-computer interfaces (BCIs) have relied on neural recordings from cortical regions by
utilizing scalp-recorded electroencephalographic (EEG) activity1 or more invasive intracranial electrode arrays2. However, advancements in recording modalities like stereotactic electroencephalography (SEEG) have allowed
us to sample deeper cortical and subcortical structures with high spatial and temporal resolution3,4. SEEG
provides a novel opportunity to explore the utility of neural signals beyond the cortex in BCI5,6. SEEG, an intracranial recording modality used in the presurgical evaluation of epilepsy patients7, enables
for the sampling of local field potentials (LFPs) and analysis of high gamma-band neural activity (70–200 Hz)5,
a frequency range closely associated with pro-kinetic neural dynamics8,9. Indeed, gamma frequency band (30–

### 200 Hz) power modulations in cortical areas have been implicated in motor control in both humans and non-

human primates9–11. As such, the ability to record from deep cortical and subcortical brain regions with greater
resolution through SEEG enables further investigation into the distributed motor processing networks12, with
potential for integration into BCI systems. The incorporation of AI techniques to BCI has strengthened its progression13. Machine and deep learning
algorithms enable extraction and decoding of latent neural representations from SEEG signals (versus directly
from spike data), which can capture complex task-specific neural patterns14–16. Beyond motor decoding17, AI’s
application to SEEG signals expands to predicting seizure onset localization18,19 and speech20. These diverse
applications highlight the potential of SEEG as a rich source of neural signals for AI-driven decoding systems
that can improve patient care. Early work with motor BCI focused on decoding signals from primary motor cortex21,22. However, signals
in higher-order brain structures such as the posterior parietal cortex have also been used as a neural source
in motor BCI23,24. The success of utilizing structures beyond the motor cortex in motor BCI highlights that
motor processing signals may not be confined to primary motor regions. Rather, motor processing may involve
distributed networks spanning multiple brain areas. Therefore, deeper cortical structures may contribute
meaningful signals for motor BCIs. The IC, in particular, is a highly integrative region with involvement in multisensory processing, attentional
and working memory, motor association25,26, and the internal representation of gravitational acceleration27,28. Indeed, the neural representation of gravity optimizes movement execution by predicting the force required to
move vertically against gravity, thereby minimizing effort and improving motor performance29–31. Moreover,
the IC maintains extensive connectivity with motor-related areas including the putamen, supplementary motor
area, and primary motor cortex32,33, positioning it as a critical hub within the broader motor control network. Furthermore, IC is activated during both real28,34 and imagined35 directional movements making it a compelling
candidate for neural information in BCI applications that has been relatively unexplored. Murphy et al.
demonstrated that SEEG electrodes in the IC can record force-onset related signals, showing characteristic alpha-
band desynchronization during motor tasks and concluding that central sulcus and insular cortex may contain
neural signals that could be used for control of a grasp force BMI36. Similarly, Li et al. showed that SEEG can
detect neural activity from deep structures including white matter tracts, expanding the potential neural sources
for movement decoding37. Additional evidence for the IC’s motor relevance comes from IC’s enhanced activation
during motor imagery tasks38. The posterior insula is particularly involved in processing somatosensory and
spatial information39, while the anterior insula integrates multisensory inputs including proprioceptive signals
that convey limb position and movement direction40. This spatial and sensorimotor processing capacity suggests
that the IC may contain neural signatures that distinguish between different movement directions. In this study, we determined whether decoding algorithms could be used to decode simple directional
information (left vs. right) of hand movements from SEEG-recorded IC high-gamma band signals (70–200 Hz). We employed demixed Principal Component Analysis (dPCA) to extract spectrotemporal features relevant to
movement direction and state transitions within a left/right/nothing discrimination movement task. dPCA
allowed for isolation and quantification of variation attributable to certain task dimensions41. We then decoded
these dynamics through Long Short-Term Memory (LSTM) networks42 to predict the directional target. LSTMs were well-suited for capturing the complex time-varying neural patterns associated with intended
movements43, potentially unveiling a previously underappreciated role for the IC in motor processing through
SEEG recordings. We hypothesized that the IC is involved in encoding aspects of movement processing such as
directional information (left vs. right) and that AI-techniques could be utilized on SEEG recordings to decode
these aspects. Results
High-gamma band demonstrated superior classification performance
We evaluated the efficacy of various input features with LSTM to assess the impact of dPCA on the dataset. Multiple frequency ranges (alpha (8–13  Hz), beta (13–30  Hz), gamma (30–70  Hz), and high-gamma (70–

### 200  Hz)) were compared across participants. The analysis revealed that data within the high-gamma band

consistently exhibited the highest performance, with an average accuracy of 73% across all participants (Fig. 1),
which was significantly greater than 33% chance accuracy (paired t-test, N = 16 sessions, p < 0.0001, corrected
alpha: 0.00025). Further analysis was conducted to assess the impact of dPCA transformation on model accuracy. A significant improvement in performance was observed when using dPCA-transformed data compared to non-
transformed data across all patients (Fig. 1). To understand the insula’s contribution to movement decoding, we
compared classification performance across different brain regions where electrodes were present (Fig. 2). The
high-gamma band decoding performance in the insula outperformed the amygdala (mean: 53.8%, p < 0.001,
corrected alpha 0.00125), cingulate (mean: 59.3%, p < 0.001, corrected alpha: 0.00125), and hippocampus (mean:
61.6%, p < 0.001, corrected alpha: 0.00125). The frontal region, which included motor and premotor areas,
outperformed IC (mean: 76.3%, p < 0.001, corrected alpha: 0.00125). Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

dPCA result visualization and classifier models comparison
To understand why high-gamma band data after dPCA performs the best, we conducted a comprehensive analysis
of the high-gamma band (70–200 Hz) activity before and after dPCA. We first examined high-gamma PSD
across different movement conditions to identify potential frequency-specific neural signatures in the insular
region (Fig. 3). For each frequency bin within the high-gamma range (70–200 Hz), we observed overlapping
spectral power between left, right, and rest conditions, with no significant differences detected (Wilcoxon sign-
rank test: two-sided, p > 0.05, corrected alpha: 3.85e-4). We then visualized the first stimulus-dependent ( Xs)
dimension extracted by the dPCA algorithm, which served as input features for our LSTM decoder (Fig. 4). Initial analysis of the untransformed data revealed that conventional averaging across the entire high-gamma
band (70–200 Hz) failed to discriminate between the three experimental conditions. The average untransformed
signals showed overlap between left, right, and rest conditions, with nearly indistinguishable temporal patterns
and large trial-to-trial variability (Fig.  4C). After applying dPCA, the neural representations of movement
direction became markedly separated in the latent space (Fig. 4A). To evaluate the importance of temporal dynamics in decoding movement directions from neural data, we
conducted a systematic comparison between three classification approaches: our proposed LSTM network
architecture, Linear Discriminant Analysis (LDA), and Support Vector Machine (SVM). The dPCA-transformed
features were used across all three models, with temporal information preserved for LDA and SVM by
averaging time points for each principal component as a separate feature dimension. The results demonstrated a
performance advantage for the LSTM model (72.6%) (Fig. 5) over both LDA (mean accuracy: 55.4%, p < 0.001)
and SVM (mean accuracy: 56.1%, p < 0.001). Performance with limited training data and performance over time
We investigated the relationship between training data size and model performance using the dPCA + LSTM
model. Detailed instructions for training data selection can be found in the supplementary material. After
fitting the data with a linear function and a power law function, the analysis revealed a nonlinear correlation
(spearman correlation test: R2 = 0.653, p < 0.0001) between input data size and model accuracy with a power law
function model fit (power law function fit: ρ = 0.533, p < 0.0001). To contextualize these results, we compared
the performance of our model against a chance model using identical test datasets. The model consistently
outperformed the chance model across all data sizes (p < 0.001). No correlation was found between training
data size and model performance in the chance model (Fig. 6). To assess the model’s temporal generalizability,
we analyzed its performance across different task days for patients with multi-day recordings. Training and
Fig. 1. Accuracy comparison across different frequency bands and processing methods. Box plots show
classification accuracies for dPCA-processed data (green), non-dPCA processed data (yellow), and chance
level (purple) across four frequency bands: alpha, beta, gamma, and high-gamma. Each plot represents a
different frequency band, with accuracy on the y-axis ranging from 0 to 1.0. The dPCA method consistently
demonstrates higher median accuracy and smaller interquartile ranges compared to non-dPCA and chance,
with the most pronounced improvement visible in the high-gamma band. Whiskers extend to the minimum
and maximum values, excluding outliers. Significance levels: p₁ (dPCA vs. non-transformed), p₂ (dPCA vs.
chance), p₃ (non-transformed vs. chance); all p < 0.0001. Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

testing datasets were compiled from either the same day (difference = 0) or different days (difference > 0). The day
difference was calculated as the absolute difference between the training and testing day indices. A significant
linear correlation was observed between the day difference of training/testing datasets and model performance
(p < 0.0001). As the temporal gap between training and testing data increased, model performance decreased. This finding highlights the importance of temporal proximity in maintaining high levels of predictive accuracy
and suggests potential challenges in long-term generalizability of the model (Fig. 7). Discussion
Our findings demonstrate that recordings from deep cortical structures involved in motor network processing,
such as the IC, can be effectively utilized for brain-computer interface applications with the implementation
of AI techniques. Using dPCA + LSTM architecture, we achieved high classification accuracy (73% vs. 33%
chance level, p < 0.0001, N = 16 sessions) from SEEG signals in the insula. The dPCA transformation significantly
enhanced model performance across all patients. While the model demonstrated robust performance with
limited training data and showed a strong correlation between input data size and accuracy (p < 0.0001), the
temporal analysis revealed a significant decline in decoding accuracy as the interval between training and testing
days increased. Our findings demonstrated that high-gamma activity patterns in IC contain decodable information about
movement directionality, suggesting this region’s potential role in motor processing and as a novel target for BCI
applications. Given its extensive multimodal sensory input44 and role in sensorimotor integration45,46, the insula
may encode and communicate motor signals related to relative body positioning and action40,47–49. A recent
study has shown that the IC contains a somatotopically organized map of motor effectors, with effector-specific
connectivity to the primary motor cortex (M1), providing strong evidence for its direct involvement in motor
control rather than passive signal propagation50. Notably, human intracranial and neuroimaging studies have
demonstrated movement-related activity in the IC during both actual and imagined movements, implicating
it in initiating, modulating, and sustaining voluntary motor output35. Given its extensive interoceptive and
motivational inputs, the IC may serve as a bridge between internal drive states and motor execution, integrating
internal context with body positioning and action planning51. Furthermore, our cross-regional analysis
revealed a hierarchical pattern of movement decoding accuracy, with frontal regions demonstrating the highest
Fig. 2. Comparison of movement decoding accuracy between the insula and other brain regions. Box plots
illustrate classification accuracy distributions from LSTM models trained on intracranial EEG recordings
from different brain regions. (A) Amygdala vs. Insula: The insula showed significantly higher decoding
accuracy (mean = 0.742) compared to the amygdala (mean = 0.538, p < 0.001). (B) Cingulate vs. Insula: The insula demonstrated superior decoding performance (mean = 0.721) compared to the cingulate cortex
(mean = 0.593, p < 0.001), with some outliers visible in the insula distribution. (C) Frontal vs. Insula: The
frontal region exhibited higher mean accuracy (0.763) than the insula (0.687) (D) Hippocampus vs. Insula: The
insula achieved significantly higher decoding accuracy (mean = 0.742) than the hippocampus (mean = 0.616,
p < 0.001). Box plots display the median (horizontal line), interquartile range (box), and minimum/maximum
values within 1.5 times the interquartile range (whiskers). Statistical significance was assessed using Wilcoxon
rank-sum test (***p < 0.001). Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

performance followed by the insula, which significantly outperformed other examined deep cortical and
subcortical regions. This finding suggests that the IC may be involved in a part of a motor control network52. Although high-gamma signals in the frontal cortex yielded the strongest decoding performance in our dataset,
prior work suggests combining measurements from multiple motor-related areas—including deep structures
like the insula and basal ganglia—may enhance BCI accuracy. For example, one study demonstrated that
distributed SEEG decoding for both executed and imagined grasping tasks is impaired if any single region is
excluded, indicating that each recording site contributes unique information53. Another study uses sEEG and
found that more regions included in a classification task of hand movement task significantly improved the
classification accuracy54. The IC’s integration into motor networks is supported by robust anatomical connectivity studies. The IC
maintains strong connections with the basal ganglia, particularly the putamen, which is crucial for movement
initiation and motor learning33. Recent whole-brain connectivity mapping has shown that the anterior IC
exhibits preferential connectivity with motor-related areas, while maintaining its integration with limbic and
cognitive networks32. This anatomical organization positions the IC as a potential convergence zone where
motor commands can be integrated with contextual information about body state, spatial orientation, and
environmental demands. The IC’s contribution to motor control likely originates from its unique position as a sensorimotor integration
hub. The region receives convergent inputs from multiple sensory modalities, including proprioceptive,
vestibular, and visual signals that are crucial for movement planning and execution55. This multimodal integration
capacity allows the IC to compute body schema representations and spatial reference frames necessary for
accurate movement control56. Our successful decoding of directional information suggests that these integrated
sensorimotor representations contain movement-relevant signals that can be extracted for BCI applications,
even when the movements do not strongly engage the IC’s gravity-processing networks.
dPCA effectively identified and extracted discriminative features between different movement conditions,
capturing the underlying temporal dynamics of the neural responses. Previous studies have demonstrated the
utility of narrow-band analyses within the high-gamma range for movement decoding57–59. This frequency-
specific information demonstrates how dimensionality reduction techniques like dPCA can uncover previously
hidden neural representations. The LSTM architecture proved particularly advantageous for our neural decoding
task60–62. Its ability to maintain and utilize long-term dependencies in sequential data was crucial for capturing
the temporal evolution of movement-related neural signals60. dPCA identified the most relevant neural features,
while LSTM learned the complex temporal dependencies in these reduced-dimensional representations. Our longitudinal analysis revealed a significant degradation in decoding performance across recording
sessions on different days. This session-to-session variability has been documented in numerous BCI
studies14,63–65. Potential explanations include inherent source variability in neuronal firing rates, recording
Fig. 3. Normalized power spectral density (PSD) in the high-frequency band (70–200 Hz) is recorded from
the insula region during three different movement conditions: left movement (red), right movement (green),
and no movement (blue). Solid lines represent median values across all trials, all contacts in insula region,
and the shaded areas denote the interquartile range (IQR) for each condition. The data are normalized to
fixation phase for each trial each frequency bin prior to plot. The analysis reveals no differences in neural
representations between movement conditions within the insula. Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

electrode instability leading to shifts in recorded populations, and neuroplastic changes in neural circuits due to
learning-induced modifications or fluctuations in internal states65–67. We also demonstrated that IC high-gamma activity recorded through SEEG and decoded through AI
techniques may be suitable for motor BCI systems. Previous work has highlighted the potential for low gamma
(30–50 Hz) power changes in the motor cortex for accurate use in BCI11. As the full range of gamma band (up
to 200 Hz) has motor processing implications, it remains possible that higher gamma frequency bands could
be similarly used for BCI applications68. In addition, our study highlights the importance of understanding the
role of deep brain structures in movement processing and in BCI. A majority of BCI’s are based on the decoding
results of ECoG, which offers millimeter-spatial and millisecond-temporal resolution69. Yet, ECoG is limited
to cortical structures and does not sample activity from deeper structures such as the IC and basal ganglia. With the increased clinical utilization of SEEG for epilepsy monitoring, SEEG recordings may reveal how
deeper structures further define decoding for BCI17,70. As advances in technology and computation parallel our
understanding of the neurosciences, BCI’s integration with AI techniques may optimize performance, restoring
neural function to patients71. Several limitations should be considered. First, spatial sampling was determined by clinical necessity rather
than optimal coverage for movement decoding. Second, our participant population consisted exclusively of
patients with medically refractory epilepsy, which may affect the generalizability of our findings. Furthermore,
the classification-based dPCA + LSTM approach used in our current study limits the applicability of this method
to scenarios with clearly defined, discrete movement targets. Finally, our observation of declining decoder
performance with increasing temporal distance between training and testing sessions (r = -0.87, p < 0.0001)
suggests a significant practical limitation: the need for frequent recalibration of the decoding model, which
could be time consuming. In conclusion, SEEG signals from the insular cortex can be effectively decoded using advanced AI techniques.
dPCA successfully extracted movement-specific neural features from high-gamma band activity, while LSTM’s
ability to model temporal dependencies enabled accurate decoding of movement directions from these features,
achieving 73% accuracy in IC activity classification. This successful application of dimensionality reduction and
deep learning not only reveals complex neural dynamics but also establishes a framework for next-generation
BCIs in clinical settings. Future directions should focus on: (1) developing more sophisticated AI algorithms to
Fig. 4. Demixed Principal Component Analysis (dPCA) of neural population data. Left: Average trajectories
of different classes with(A)/without(C) dPCA transformation, shown with their respective confidence intervals
(shaded regions). Each line represents the mean trajectory of a distinct class across time. Right: Heatmap
showing the first dPCA dimension(B), or first feature(D) for individual trials (rows) across time (columns). Color intensity represents the magnitude of the transformed neural activity in the first demixed dimension,
with warmer colors (yellow) indicating higher values and cooler colors (dark blue) indicating lower values. The
consistency of patterns across trials within similar time periods after dPCA transformation suggests structured
temporal dynamics in the neural population. Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

Fig. 6. Performance vs. Input Data Size for Model and Chance predictions. Scatter plot shows accuracy (y-axis,
0 to 1) against training data size proportion of total training data (x-axis, 0.1 to 0.9). Blue dots represent model
performance, with a red trend line (correlation: 0.407, p < 0.001 using a linear function fit and a blue trend line
(correlation: 0.533, p < 0.001) showing positive correlation. Green dots represent chance performance, with a
flat green trend line (correlation: -0.0379, p-value: 7.718e-01) indicating no significant correlation. The model
consistently outperforms chance across all input data sizes, with accuracy improving as data size increases. Fig. 5. Model performance between a linear model (LDA), SVM (RBF kernel), and LSTM using dPCA
transformed data. LSTM shows best performance (mean = 0.726) significantly higher (Wilcoxon one-sided
sign rank test, p < 0.005) than LDA (mean = 0.554) and SVM (mean = 0.561). There is no significant difference
between performance of LDA and SVM (Wilcoxon two-sided sign rank test, p > 0.05). Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

improve decoding stability across different brain states and patient conditions, (2) understand how IC signals
could complement traditional motor areas for more robust BCIs, (3) creating automated AI systems that can
adapt to individual patient’s neural patterns for personalized BCI calibration, and (4) extending our dPCA-
LSTM framework to regression tasks capable of decoding continuous movement parameters such as velocity,
acceleration, and trajectory angle. Additionally, visual inspection of Fig.  4 suggests potential differences in
the neural separability of left versus right movement conditions in one participant. This observation raises
interesting questions about potential hemispheric asymmetries or directional biases in insular cortex movement
representations that should be explored in future studies with larger sample sizes designed specifically to examine
individual movement direction performance. Furthermore, studies using delayed reach tasks have shown that
subcortical regions such as the hippocampus and amygdala exhibit neural modulation during the preparatory
phase between cue presentation and movement onset72,73. These findings suggest that deep brain structures are
actively engaged in motor preparation processes, not solely execution. Although our analysis was time-aligned
to movement onset, this work highlights the possibility that the insula may also carry informative preparatory
signals during the cue-response interval, a direction that warrants future investigation. The integration of
advanced machine learning architectures with SEEG recordings can enable characterization of neural dynamics
in deep structures, such as the IC, revealing previously inaccessible aspects of deep brain function. Method
Participant recruitment
Seven participants (6 male, 1 female, aged 31–54 years, mean 39.7) with drug-resistant epilepsy underwent
SEEG electrode implantation with macro-electrodes (Ad-. Tech Medical Instrumentation Corporation, Oak Creek, WI, USA) in the IC as part of their seizure
localization surgery. Details on the locations of seizure onset are provided in Table 1. Informed consent was
obtained from all patients prior to participation in the study and all experiments were performed in accordance
with the guidelines (Study ID: HS-17-00544), which received approval from the Institutional Review Board
(IRB) at the University of Southern California (USC) Health Science Campus. The specific number and locations
of electrodes for each patient were clinically determined before study enrollment, based on evaluations from
magnetic resonance imaging (MRI), positron emission tomography (PET) scans, video-EEG monitoring, and
seizure semiology. Each case was reviewed by a team at the USC Comprehensive Epilepsy Center. 2 out of the 7
participants had bilateral depth electrodes implanted in the IC, while the 4 participants received unilateral depth
electrodes in the left hemisphere, opposite to their dominant hand. Fig. 7. Cross-day Performance using High Gamma Band. Scatter plot illustrates the relationship between
accuracy (y-axis, 0 to 1.0) and difference in days between training and testing (x-axis, 0 to 2.0). Blue dots
represent individual data points. The red line shows the negative linear correlation (correlation: -0.868,
p-value: 1.703e-07) with a 95% confidence interval (pink shaded area). A significant drop in performance is
observed between same-day (0.00) and 1 day difference (1.00) testing, as indicated by p0-1 < 0.0001. The plot
demonstrates a strong inverse relationship between temporal distance and model accuracy in the high gamma
band. Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

Electrodes and recording equipment
Neural signals were recorded using two types of SEEG depth electrodes: Spencer probes (8–10 platinum contacts,
4–5 mm spacing) and macro-micro electrodes (16 contacts total, 5 mm spacing), with only macro contacts
utilized for recording. Signals were acquired using NeuroPort Neural Signal Processor (Blackrock Microsystems, Salt Lake City, UT, USA) at 30,000 Hz sampling rate with 16-bit resolution and then down-sampled to 2,000 Hz. Signal processing included high-pass (0.3 Hz), low-pass (7,500 Hz), and anti-aliasing (500 Hz) filtering. The first
electrode type was the Spencer probe depth electrode, which featured platinum contacts measuring 2.29 mm in
length. Two variants of this electrode were used: the RD08R-SP05X-000, with 8 contacts spaced 4 mm apart,
and the RD10R-SP05X-000, with 10 contacts spaced 5 mm apart. The second type of electrode was the macro-
micro depth electrode, comprising 16 contacts, including 6 macro and 10 micro contacts. These electrodes had
platinum contacts with a diameter of 1.3 mm and a length of 1.57 mm (part number MM16C-SP05X-000)
and were spaced 5 mm apart. For this study, only recordings from the macro-type contacts were utilized. All
electrodes were supplied by Ad-Tech Medical Instrumentation Corporation, Oak Creek, WI, USA. Left/Right/Nothing discrimination task
The task consisted of six sequential components (Fig. 8): Inter-Trial Interval (1s), Fixation (1s), Cue1 (1s), Cue2
(0.5s), Delay (1s), and Response (max 5s). Participants positioned their right hand at screen center, maintained
fixation on a central dot during Fixation, and were presented with two target circles (left/right) during Cue

### 1. During Cue2, an arrow indicated movement direction (or cross for no movement). After a delay period

(Delay), participants moved their hand toward the indicated target during the Response phase. Each participant
completed 89–117 trials (mean 101.3 ± 9.6) with a total of 16 sessions. The task was implemented in MATLAB
using Psychophysics Toolbox74 and displayed on a touch-screen monitor. Behavioral data collection
Movement data was collected using dual accelerometers (ADXL335, Adafruit Industries, New York City, NY, USA). Performance metrics included delay time, trial time, response time, and success rate. Successful trials
required correct movement completion longer than 0.5 s and less than 5 s. Trial time was measured from ITI
start to Response end, while response time captured movement execution duration. The success rate reflected the
percentage of correctly executed trials within the time window. All metrics were computed using only successful
trials. If, after removing these outliers, the number of successful trials in the total trials was less than 50%, the
entire run was discarded. Data analysis
Data preprocessing
Neural signals underwent three sequential preprocessing stages to ensure data quality. First, we employed ZapLine
noise removal technique from `meegkit` Python package75 to eliminate 60 Hz line noise and its harmonics. For
re-referencing, to address the challenge of signal amplitude variations across SEEG contacts in both gray and
white matter, we developed a weighted electrode shaft re-referencing (wESR) method72,73 that utilized modified
Root Mean Square (RMS) values to scale each contact’s contribution to common noise calculation (Comparison
with other methods can be found in Supplementary Material Figure S1). Then, we implemented a high-pass filter
(300 Hz) and a thresholding technique (50uV) to identify and remove data containing high frequency signals. Only data chunks that passed this quality control step were included in the weight calculations. Response time alignment
Because the time for each movement onset could be different, dynamic time wrapping was used to shift the
timeframe of the start of response phase to the start of the participant’s movement using python package
affinewarp. ShiftWraping76. The accelerometer data during the Response phase was used for time alignment
during movement. The analysis window length was set at 2 s starting at the beginning of each response phase
after alignment. Patient ID
Insula Region
Age
Gender
Dominant Hand
Seizure onset zone

RI

Male
Right
R mesial temporal

## LI, RI

Male
Right
Right hippo head

LI

Female
Right
R basal temporal

RI

Male
Right
R hippo tail

LI

Male
Right
L Mesio temporal

RI

Male
Right
L posterior orbitofrontal

## LI, RI

Male
Right
L temporal
Table 1. Demographic information for the 7 participants included in the study. Given that participants were
right-handed, the analysis was confined to tasks performed with the right hand to minimize the confounding
influence of handedness. Of these participants, one was female, with ages of 42 years, and six were male, aged
between 31 and 54 years. It is also noted that none of the participants had a seizure onset zone located within
the Insula (RI: right insula, LI: left Insula). Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

Time-frequency representation calculation and data concatenation
Multi-taper taper analysis was used to calculate power spectral density (PSD) and time-frequency representation
(5 tapers, time-bandwidth product 3). Analysis window within response phase consists of overlapping moving
window with length of 0.35s, 0.0335s step size (90% overlap) was used, which makes for a total of 50 temporal
steps. Each frequency bin had a 2.86Hz resolution. Before we fed the data into the dPCA, we separated the time-
frequency representation for each bandwidth (alpha:8-13Hz, beta:13-30Hz, gamma:30-70Hz, high gamma:70-
200Hz). The data for all channels with the same bandwidth were concatenated into a large matrix, thus creating
a [Nchannels⋅Nfrequency, 50], where 50 is the number of temporal steps, and Nchannels⋅Nfrequency is the number of
features. The PSD data were normalized using the same frequency bin in the Fixation phase of the same trial.
dPCA
dPCA was used to separate the groups with different stimulus conditions. dPCA extracts different dimensions
with respect to each external variable41 and maximizes the variance across different groups while minimizing the
variance within the same group. To characterize how neural signals were modulated during different movement
conditions, we looked at the stimulus-dependent dimension (
−
Xst). We preserved the first 10 principal
components for each dimension based on the explained variance for the
−
Xst. We then fed
−
Xst into the LSTM
to train the neural network. To extract the transforming matrix for each dimension, we aimed at minimizing the
following loss function: Lφ = || Xφ −AqX ||
Where Aq = Fφ · Dφ, Fφ and Dφ are the encoder and decoder matrix. q indicate the matrix with leading
q singular values (rank). φ indicates the dimension of the data (time, stimulus, etc.). The minimization of
this equation can be solved as a reduced rank regression problem. In our case, Xφ will be calculated using
marginalization to decompose the original data X into independent part. During which the time dependent
dimension Xt is the average of the data across all conditions, stimulus dependent dimension Xst is the average
of the data not explained by Xt, for different stimulus. Xt = < X>s, Xst =< X −Xt >, After learning the Fφ, we will calculate the estimated
−
Xs using: Fig. 8. Temporal sequence of the left/right discrimination task paradigm. The trial begins with an inter-trial
interval (ITI) of 1s, followed by a fixation period (1s) where participants focus on a central dot. A target cue
(Cue 1) is then presented for 1s, indicating the required movement direction (left or right). After a holding
period (Cue 2, 0.5s), participants are prompted by a response cue to execute the instructed movement. Each
screen displays a black background with white stimuli to maintain consistent luminance throughout the task. The temporal progression flows from bottom to top, with precise timing intervals indicated for each phase of
the trial. Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

−
Xst = Fst · X
LSTM
We implemented a bidirectional LSTM neural network using PyTorch77 to decode movement directions
from time-frequency response. We used various input features with either raw time-frequency representation
(rawLSTM) or dPCA-transformed time-frequency representation data (dPCA + LSTM). We implemented a bidirectional LSTM neural network using PyTorch to decode movement directions from
time-frequency responses. The LSTM layer was configured with 50 hidden units, followed by a fully connected
layer (100 to 3 neurons) and softmax activation for probabilistic classification of movement directions (left,
right, no movement). Network training was performed individually for each session. Model parameters were
initialized using random_init in PyTorch’s Module class. Training utilized the Adam optimizer with a cross-
entropy loss function, employing a learning rate of 0.001 across 150 iterations. This iteration count was
empirically determined based on consistent loss convergence observed by iteration 150. For each participant, data were split using stratified sampling: 70% training, 30% testing. The training set
was further divided 80/20 for training/validation. The held-out test set was used exclusively for final evaluation. Model performance was evaluated using classification accuracy on the held-out test set (repeated 10 times for
robustness). To establish statistical significance, we computed chance-level performance by randomly permuting
class labels and comparing the resulting accuracies with the model’s true performance. This permutation testing
provided a robust baseline for assessing the decoder’s effectiveness. Training data method for training data size comparison
For the training data size analysis, we systematically varied the amount of training data by extracting N%
(ranging from 10 to 90% in 10% increments) of the original training set (70% of total data). For each training
data size condition, the selected training subset underwent a further 80/20 division into training and validation
sets following the same procedure as the standard training protocol. This approach allowed us to evaluate the
relationship between training data size and model performance while maintaining identical test conditions
across all comparisons. During each training iteration, we employed stochastic mini-batch training with 20% of
the available training data randomly sampled with replacement. Statistical analysis
We used Student’s t-tests to compare performance and evaluate the dependence of model performance on
architecture parameters, the addition of dPCA in preprocessing, time, and training dataset size. Significance
levels were reported after applying Benferroni correction. A Spearman Correlation Coefficient test was performed
between input size and model performance as well as between the difference in days between training/testing
datasets and model performance. To compare decoding performance across different brain regions, we applied
the dPCA + LSTM methodology using high-gamma band time-frequency data to all analyzed areas. Due to
the individualized nature of clinical SEEG implantation, each participant had unique electrode coverage. To
address this variability, we only included brain regions that were sampled in the majority of participants (n > 3). Furthermore, when comparing the insula to a specific region (e.g., amygdala), we only included participants
who had electrodes in both the insula and that comparison region, ensuring valid paired statistical comparisons. Data availability
The datasets generated and/or analyzed during the current study are not publicly available due to either the
prohibitively large size of the raw SEEG recordings and institutional restrictions regarding patient privacy. In
accordance with our IRB-approved protocol (HS-17-00544), participants did not provide explicit consent for the
public sharing of their neural data. However, derived data that support the findings of this study are available
from the corresponding author upon reasonable request and subject to appropriate data sharing agreements that
protect patient confidentiality. Received: 15 April 2025; Accepted: 4 August 2025
References

### 1. Wolpaw, J. R. & McFarland, D. J. Control of a two-dimensional movement signal by a noninvasive brain-computer interface in

humans. Proceedings of the National Academy of Sciences. 101 (51) 17849–17854. (2004). https://doi.org/10.1073/pnas.0403504101

### 2. Birbaumer, N. & Cohen, L. G. Brain–computer interfaces: communication and restoration of movement in paralysis. J. Physiol. 579

(Pt 3), 621–636. https://doi.org/10.1113/jphysiol.2006.125633 (2007).

### 3. Yamamoto, T. Recent advancement of technologies and the transition to new concepts in epilepsy surgery. Neurol. Med. Chir.

(Tokyo). 60 (12), 581–593. https://doi.org/10.2176/nmc.ra.2020-0197 (2020).

### 4. Youngerman, B. E., Khan, F. A. & McKhann, G. M. Stereoelectroencephalography in epilepsy, cognitive neurophysiology, and

psychiatric disease: safety, efficacy, and place in therapy. Neuropsychiatr Dis. Treat. 15, 1701–1716. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​2​1​4​7​/​N​D​T​.​S​
1​7​7​8​0​4​ (2019).

### 5. Herff, C., Krusienski, D. J. & Kubben, P. The potential of Stereotactic-EEG for Brain-Computer interfaces: current progress and

future directions. Front. Neurosci. 14 https://doi.org/10.3389/fnins.2020.00123 (2020).

### 6. Vadera, S., Marathe, A. R., Gonzalez-Martinez, J. & Taylor, D. M. Stereoelectroencephalography for continuous two-dimensional

cursor control in a brain-machine interface. Neurosurg. Focus. 34 (6), E3. https://doi.org/10.3171/2013.3. FOCUS1373 (2013).

### 7. Zumsteg, D. & Wieser, H. G. Presurgical evaluation: current role of invasive EEG. Epilepsia 41 (Suppl 3), S55–60. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​

0​.​1​1​1​1​/​j​.​1​5​2​8​-​1​1​5​7​.​2​0​0​0​.​t​b​0​1​5​3​5​.​x​ (2000).

### 8. Cassidy, M. et al. Movement-related changes in synchronization in the human basal ganglia. Brain 125 (Pt 6), 1235–1246. ​h​t​t​p​s​:​/​/​

d​o​i​.​o​r​g​/​1​0​.​1​0​9​3​/​b​r​a​i​n​/​a​w​f​1​3​5​ (2002). Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

### 9. Miller, K. J. et al. Spectral changes in cortical surface potentials during motor movement. J. Neurosci. 27 (9), 2424–2432. ​h​t​t​p​s​:​/​/​d​

o​i​.​o​r​g​/​1​0​.​1​5​2​3​/​J​N​E​U​R​O​S​C​I​.​3​8​8​6​-​0​6​.​2​0​0​7​ (2007).

### 10. Joundi, R. A., Jenkinson, N., Brittain, J. S., Aziz, T. Z. & Brown, P. Driving oscillatory activity in the human cortex enhances motor

performance. Curr. Biol. 22 (5), 403–407. https://doi.org/10.1016/j.cub.2012.01.024 (2012).

### 11. Engelhard, B., Ozeri, N., Israel, Z., Bergman, H. & Vaadia, E. Inducing γ oscillations and precise Spike synchrony by operant

conditioning via brain-machine interface. Neuron 77 (2), 361–375. https://doi.org/10.1016/j.neuron.2012.11.015 (2013).

### 12. Jensen, M. A. et al. A motor association area in the depths of the central sulcus. Nat. Neurosci. 26 (7), 1165–1169. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​

1​0​.​1​0​3​8​/​s​4​1​5​9​3​-​0​2​3​-​0​1​3​4​6​-​z​ (2023).

### 13. Zhang, X. et al. The combination of brain-computer interfaces and artificial intelligence: applications and challenges. Annals

Translational Med. 8 (11), 712–712. https://doi.org/10.21037/atm.2019.11.109 (2020).

### 14. Pandarinath, C. et al. Latent factors and dynamics in motor cortex and their application to Brain–Machine interfaces. J. Neurosci.

38 (44), 9390–9401. https://doi.org/10.1523/JNEUROSCI.1669-18.2018 (2018).

### 15. Churchland, M. M. et al. Neural population dynamics during reaching. Nature 487 (7405), 51–56. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​3​8​/​n​a​t​u​r​e​

1​1​1​2​9​ (2012).

### 16. Aghagolzadeh, M. & Truccolo, W. Inference and decoding of motor cortex Low-Dimensional dynamics via latent State-Space

models. IEEE Trans. Neural Syst. Rehabil. Eng. 24 (2), 272–282. https://doi.org/10.1109/TNSRE.2015.2470527 (2016).

### 17. Li, G. et al. A preliminary study towards prosthetic hand control using human stereo-electroencephalography (SEEG) signals. In: 8th

International IEEE/EMBS Conference on Neural Engineering (NER). 375–378. (2017). https://doi.org/10.1109/NER.2017.8008368

### 18. Johnson, G. W. et al. Localizing seizure onset zones in surgical epilepsy with neurostimulation deep learning. Published Online

September 23 https://doi.org/10.3171/2022.8. JNS221321 (2022).

### 19. Nieto Ramos, A. et al. Epileptic network identification: insights from dynamic mode decomposition of sEEG data. J. Neural Eng.

21 (4), 046061. https://doi.org/10.1088/1741-2552/ad705f (2024).

### 20. Wu, X., Wellington, S., Fu, Z. & Zhang, D. Speech decoding from stereo-electroencephalography (sEEG) signals using advanced

deep learning methods. J. Neural Eng. 21 (3), 036055. https://doi.org/10.1088/1741-2552/ad593a (2024).

### 21. Schwartz, A. B., Kettner, R. E. & Georgopoulos, A. P. Primate motor cortex and free arm movements to visual targets in three-

dimensional space. I. Relations between single cell discharge and direction of movement. J. Neurosci. 8 (8), 2913–2927. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​5​2​3​/​J​N​E​U​R​O​S​C​I​.​0​8​-​0​8​-​0​2​9​1​3​.​1​9​8​8​ (1988).

### 22. Kakei, S., Hoffman, D. S. & Strick, P. L. Muscle and movement representations in the primary motor cortex. Science 285 (5436),

2136–2139. https://doi.org/10.1126/science.285.5436.2136 (1999).

### 23. Musallam, S., Corneil, B. D., Greger, B., Scherberger, H. & Andersen, R. A. Cognitive control signals for neural prosthetics. Science

305 (5681), 258–262. https://doi.org/10.1126/science.1097938 (2004).

### 24. Mulliken, G. H., Musallam, S. & Andersen, R. A. Decoding trajectories from posterior parietal cortex ensembles. J. Neurosci. 28

(48), 12913–12926. https://doi.org/10.1523/JNEUROSCI.1463-08.2008 (2008).

### 25. Augustine, J. R. Circuitry and functional aspects of the insular lobe in primates including humans. Brain Res. Brain Res. Rev. 22 (3),

229–244. https://doi.org/10.1016/s0165-0173(96)00011-2 (1996).

### 26. Criaud, M. & Boulinguez, P. Have we been asking the right questions when assessing response Inhibition in go/no-go tasks with

fMRI? A meta-analysis and critical review. Neurosci. Biobehav Rev. 37 (1), 11–23. https://doi.org/10.1016/j.neubiorev.2012.11.003
(2013).

### 27. Indovina, I. et al. Representation of visual gravitational motion in the human vestibular cortex. Science 308 (5720), 416–419.

https://doi.org/10.1126/science.1107961 (2005).

### 28. Rousseau, C. et al. Direction-dependent activation of the insular cortex during vertical and horizontal hand movements. Neuroscience 325, 10–19. https://doi.org/10.1016/j.neuroscience.2016.03.039 (2016).

### 29. Berret, B. et al. The inactivation principle: mathematical solutions minimizing the absolute work and biological implications for

the planning of arm movements. PLoS Comput. Biol. 4 (10), e1000194. https://doi.org/10.1371/journal.pcbi.1000194 (2008).

### 30. White, O. et al. Altered gravity highlights central pattern generator mechanisms. J. Neurophysiol. 100 (5), 2819–2824. ​h​t​t​p​s​:​/​/​d​o​i​.​o​

r​g​/​1​0​.​1​1​5​2​/​j​n​.​9​0​4​3​6​.​2​0​0​8​ (2008).

### 31. Gaveau, J., Berret, B., Angelaki, D. E. & Papaxanthis, C. Direction-dependent arm kinematics reveal optimal integration of gravity

cues. Elife 5, e16394. https://doi.org/10.7554/eLife.16394 (2016).

### 32. Gehrlach, D. A. et al. A whole-brain connectivity map of mouse insular cortex. Wassum KM, Livneh Y, eds. eLife. 9 e55585. (2020).

https://doi.org/10.7554/eLife.55585

### 33. Cauda, F. et al. Functional connectivity of the Insula in the resting brain. Neuroimage 55 (1), 8–23. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​

i​m​a​g​e​.​2​0​1​0​.​1​1​.​0​4​9​ (2011).

### 34. Mutschler, I. et al. Functional organization of the human anterior insular cortex. Neurosci. Lett. 457 (2), 66–70. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​

1​0​1​6​/​j​.​n​e​u​l​e​t​.​2​0​0​9​.​0​3​.​1​0​1​ (2009).

### 35. Rousseau, C., Barbiero, M., Pozzo, T., Papaxanthis, C. & White, O. Actual and imagined movements reveal a dual role of the insular

cortex for motor control. Cereb. Cortex. 31 (5), 2586–2594. https://doi.org/10.1093/cercor/bhaa376 (2021).

### 36. Murphy, B. A., Miller, J. P., Gunalan, K. & Ajiboye, A. B. Contributions of subsurface cortical modulations to discrimination of

executed and imagined Grasp forces through stereoelectroencephalography. PLoS ONE. 11 (3), e0150359. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​7​1​
/​j​o​u​r​n​a​l​.​p​o​n​e​.​0​1​5​0​3​5​9​ (2016).

### 37. Li, G. et al. Detection of human white matter activation and evaluation of its function in movement decoding using stereo-

electroencephalography (SEEG). J. Neural Eng. 18 (4). https://doi.org/10.1088/1741-2552/ac160e (2021).

### 38. Caria, A. et al. Regulation of anterior insular cortex activity using real-time fMRI. Neuroimage 35 (3), 1238–1246. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​

1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​0​7​.​0​1​.​0​1​8​ (2007).

### 39. Chang, L. J., Yarkoni, T., Khaw, M. W. & Sanfey, A. G. Decoding the role of the Insula in human cognition: functional parcellation

and large-scale reverse inference. Cereb. Cortex. 23 (3), 739–749. https://doi.org/10.1093/cercor/bhs065 (2013).

### 40. Craig, A. D. B. How do you feel–now? The anterior Insula and human awareness. Nat. Rev. Neurosci. 10 (1), 59–70. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​

/​1​0​.​1​0​3​8​/​n​r​n​2​5​5​5​ (2009).

### 41. Kobak, D. et al. Demixed principal component analysis of neural population data. van Rossum MC, ed. eLife. 5 e10989. (2016).

https://doi.org/10.7554/eLife.10989

### 42. Staudemeyer, R. C. & Morris, E. R. Understanding LSTM -- a tutorial into long short-term memory recurrent neural networks. Published online September 12, 2019. Accessed October 23, (2024). http://arxiv.org/abs/1909.09586

### 43. Martín-Chinea, K. et al. Effect of time windows in LSTM networks for EEG-based BCIs. Cogn. Neurodyn. 17 (2), 385. ​h​t​t​p​s​:​/​/​d​o​i​.​

o​r​g​/​1​0​.​1​0​0​7​/​s​1​1​5​7​1​-​0​2​2​-​0​9​8​3​2​-​z​ (2022).

### 44. Averbeck, B. B. & Seo, M. The statistical neuroanatomy of frontal networks in the macaque. PLoS Comput. Biol. 4 (4), e1000050.

https://doi.org/10.1371/journal.pcbi.1000050 (2008).

### 45. Gogolla, N. The insular cortex. Curr. Biol. 27 (12), R580–R586. https://doi.org/10.1016/j.cub.2017.05.010 (2017).

### 46. Perri, R. L. et al. Awareness of perception and sensory–motor integration: erps from the anterior Insula. Brain Struct. Funct. 223

(8), 3577–3592. https://doi.org/10.1007/s00429-018-1709-y (2018).

### 47. Karnath, H. O. & Baier, B. Right Insula for our sense of limb ownership and self-awareness of actions. Brain Struct. Funct. 214

(5–6), 411–417. https://doi.org/10.1007/s00429-010-0250-4 (2010).

### 48. Critchley, H. D., Wiens, S., Rotshtein, P., Ohman, A. & Dolan, R. J. Neural systems supporting interoceptive awareness. Nat. Neurosci. 7 (2), 189–195. https://doi.org/10.1038/nn1176 (2004). Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

### 49. Kenzie, J. M. et al. Localization of impaired kinesthetic processing Post-stroke. Front. Hum. Neurosci. 10, 505. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​

3​8​9​/​f​n​h​u​m​.​2​0​1​6​.​0​0​5​0​5​ (2016).

### 50. Kerezoudis, P. et al. The human insula encodes somatotopic representation of motor execution with an effector-specific

connectomic map to primary motor cortex. bioRxiv. https://doi.org/10.1101/2025.05.19.653527

### 51. Tinaz, S. et al. Insula as the interface between body awareness and movement: A Neurofeedback-Guided kinesthetic motor

imagery study in parkinson’s disease. Front. Hum. Neurosci. 12 https://doi.org/10.3389/fnhum.2018.00496 (2018).

### 52. Bensmaia, S. J. & Miller, L. E. Restoring sensorimotor function through intracortical interfaces: progress and looming challenges. Nat. Rev. Neurosci. 15 (5), 313–325. https://doi.org/10.1038/nrn3724 (2014).

### 53. Ottenhoff, M. C. et al. Executed and imagined grasping movements can be decoded from lower dimensional representation of

distributed non-motor brain areas. Published Online July. 4 https://doi.org/10.1101/2022.07.04.498676 (2022).

### 54. Li, G. et al. Assessing differential representation of hand movements in multiple domains using stereo-electroencephalographic

recordings. NeuroImage 250, 118969. https://doi.org/10.1016/j.neuroimage.2022.118969 (2022).

### 55. Kurth, F., Zilles, K., Fox, P. T., Laird, A. R. & Eickhoff, S. B. A link between the systems: functional differentiation and integration

within the human Insula revealed by meta-analysis. Brain Struct. Funct. 214 (5–6), 519–534. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​0​7​/​s​0​0​4​2​9​-​0​1​0​-​0​
2​5​5​-​z​ (2010).

### 56. Craig, A. D. Interoception: the sense of the physiological condition of the body. Curr. Opin. Neurobiol. 13 (4), 500–505. ​h​t​t​p​s​:​/​/​d​o​

i​.​o​r​g​/​1​0​.​1​0​1​6​/​s​0​9​5​9​-​4​3​8​8​(​0​3​)​0​0​0​9​0​-​4​ (2003).

### 57. Wang, Z., Logothetis, N. K. & Liang, H. Decoding a bistable percept with integrated time–frequency representation of single-trial

local field potential. J. Neural Eng. 5 (4), 433. https://doi.org/10.1088/1741-2560/5/4/008 (2008).

### 58. Hammer, J. et al. Predominance of movement speed over direction in neuronal population signals of motor cortex: intracranial

EEG data and A simple explanatory model. Cereb. Cortex. 26 (6), 2863–2881. https://doi.org/10.1093/cercor/bhw033 (2016).

### 59. Miller, K. J., Hermes, D. & Staff, N. P. The current state of electrocorticography-based brain–computer interfaces. NeuroSurg. Focus.

49 (1), E2. https://doi.org/10.3171/2020.4. FOCUS20185 (2020).

### 60. Liu, F. et al. Deep learning for neural decoding in motor cortex. J. Neural Eng. 19 (5), 056021. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​8​8​/​1​7​4​1​-​2​5​5​2​/​

a​c​8​f​ b​5​ (2022).

### 61. Hosman, T. et al. BCI decoder performance comparison of an LSTM recurrent neural network and a Kalman filter in retrospective

simulation. In: 9th International IEEE/EMBS Conference on Neural Engineering (NER) 1066–1071. (2019). ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​1​0​9​
/​N​E​R​.​2​0​1​9​.​8​7​1​7​1​4​0​

### 62. Tortora, S., Ghidoni, S., Chisari, C., Micera, S. & Artoni, F. Deep learning-based BCI for gait decoding from EEG with LSTM

recurrent neural network. J. Neural Eng. 17 (4), 046011. https://doi.org/10.1088/1741-2552/ab9842 (2020).

### 63. Perge, J. A. et al. Intra-day signal instabilities affect decoding performance in an intracortical neural interface system. J. Neural Eng.

10 (3), 036004. https://doi.org/10.1088/1741-2560/10/3/036004 (2013).

### 64. Borra, D., Mondini, V., Magosso, E. & Müller-Putz, G. R. Decoding movement kinematics from EEG using an interpretable

convolutional neural network. Comput. Biol. Med. 165, 107323. https://doi.org/10.1016/j.compbiomed.2023.107323 (2023).

### 65. Degenhart, A. D. et al. Stabilization of a brain–computer interface via the alignment of low-dimensional spaces of neural activity. Nat. Biomed. Eng. 4 (7), 672–685. https://doi.org/10.1038/s41551-020-0542-9 (2020).

### 66. Lebedev, M. A. & Nicolelis, M. A. L. Brain-Machine interfaces: from basic science to neuroprostheses and neurorehabilitation. Physiol. Rev. 97 (2), 767–837. https://doi.org/10.1152/physrev.00027.2016 (2017).

### 67. Dabagia, M., Kording, K. P. & Dyer, E. L. Comparing high-dimensional neural recordings by aligning their low-dimensional latent

representations. Published online May 17, 2022. (Accessed October 23, 2024). http://arxiv.org/abs/2205.08413

### 68. Milekovic, T. et al. Volitional control of single-electrode high gamma local field potentials by people with paralysis. J. Neurophysiol.

121 (4), 1428–1450. https://doi.org/10.1152/jn.00131.2018 (2019).

### 69. Schalk, G. & Leuthardt, E. C. Brain-computer interfaces using electrocorticographic signals. IEEE Rev. Biomed. Eng. 4, 140–154.

https://doi.org/10.1109/RBME.2011.2172408 (2011).

### 70. Liu, D. et al. Intracranial brain-computer interface spelling using localized visual motion response. NeuroImage 258, 119363.

https://doi.org/10.1016/j.neuroimage.2022.119363 (2022).

### 71. Silva, G. A. A new frontier: the convergence of nanotechnology, brain machine interfaces, and artificial intelligence. Front. Neurosci. 12, 843. https://doi.org/10.3389/fnins.2018.00843 (2018).

### 72. Shao, X. et al. Beta-band desynchronization in the human hippocampus during movement preparation in a delayed reach task. Exp. Brain Res. 243 (7), 180. https://doi.org/10.1007/s00221-025-07124-6 (2025).

### 73. Sundaram, S. et al. Beta-band power modulation in the human amygdala during a delayed reach task. J. Clin. Neurosci. 135,

111151. https://doi.org/10.1016/j.jocn.2025.111151 (2025).

### 74. Psychtoolbox-3 - Overview. Accessed January 16. (2025). http://psychtoolbox.org/

### 75. De Cheveigné, A. & ZapLine A simple and effective method to remove power line artifacts. NeuroImage 207, 116356. ​h​t​t​p​s​:​/​/​d​o​i​.​

o​r​g​/​1​0​.​1​0​1​6​/​j​.​n​e​u​r​o​i​m​a​g​e​.​2​0​1​9​.​1​1​6​3​5​6​ (2020).

### 76. Williams, A. H. et al. Discovering precise temporal patterns in large-scale neural recordings through robust and interpretable time

warping. Neuron 105 (2), 246–259e8. https://doi.org/10.1016/j.neuron.2019.10.020 (2020).

### 77. Paszke, A. et al. PyTorch: an Imperative Style, High-Performance Deep Learning Library. Acknowledgements
We wish to acknowledge the generous support of the: NIH NINDS K23NS114190. Author contributions
X. S. and R. C. contributed equally. X. S., R. C., and J. C. wrote the main manuscript text. X. S. and R. C. prepared all
figures. X. S. performed the data analysis. All authors edited and reviewed the manuscript. S. S. and B. L. super­
vised the entire project. Declarations
Competing interests
The authors declare no competing interests. Additional information
Supplementary Information The online version contains supplementary material available at ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​3​8​/​s​4​1​5​9​8​-​0​2​5​-​1​4​8​0​5​-​3​.​
Correspondence and requests for materials should be addressed to R. S. C. Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/

Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:29993

| https://doi.org/10.1038/s41598-025-14805-3
www.nature.com/scientificreports/
