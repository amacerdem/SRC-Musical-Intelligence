# novel-cyclic-homogeneous-oscillation-detection-met

Novel Cyclic Homogeneous1
Oscillation Detection Method for2
High Accuracy and Speciﬁc3
Characterization of Neural Dynamics4
Hohyun Cho1,2*, Markus Adamek 1,2, Jon T. Willie 1,2, Peter Brunner 1,2*5
*For correspondence:
hohyun@wustl.edu (HC);
pbrunner@wustl.edu (PB)
1Department of Neurosurgery, Washington University School of Medicine, St. Louis,6
MO, USA; 2National Center for Adaptive Neurotechnologies, St. Louis, MO, USA7
8
Abstract Detecting temporal and spectral features of neural oscillations is essential to9
understanding dynamic brain function. Traditionally, the presence and frequency of neural10
oscillations are determined by identifying peaks over 1/f noise within the power spectrum.11
However, this approach solely operates within the frequency domain and thus cannot adequately12
distinguish between the fundamental frequency of a non-sinusoidal oscillation and its harmonics.13
Non-sinusoidal signals generate harmonics, signiﬁcantly increasing the false-positive detection14
rate — a confounding factor in the analysis of neural oscillations. To overcome these limitations,15
we deﬁne the fundamental criteria that characterize a neural oscillation and introduce the Cyclic16
Homogeneous Oscillation (CHO) detection method that implements these criteria based on an17
auto-correlation approach that determines the oscillation’s periodicity and fundamental18
frequency. We evaluated CHO by verifying its performance on simulated sinusoidal and19
non-sinusoidal oscillatory bursts convolved with 1/f noise. Our results demonstrate that CHO20
outperforms conventional techniques in accurately detecting oscillations. Speciﬁcally, we21
determined the sensitivity and speciﬁcity of CHO as a function of signal-to-noise ratio (SNR). We22
further assessed CHO by testing it on electrocorticographic (ECoG, 8 subjects) and23
electroencephalographic (EEG, 7 subjects) signals recorded during the pre-stimulus period of an24
auditory reaction time task and on electrocorticographic signals (6 SEEG subjects and 6 ECoG25
subjects) collected during resting state. In the reaction time task, the CHO method detected26
auditory alpha and pre-motor beta oscillations in ECoG signals and occipital alpha and pre-motor27
beta oscillations in EEG signals. Moreover, CHO determined the fundamental frequency of28
hippocampal oscillations in the human hippocampus during the resting state (6 SEEG subjects).29
In summary, CHO demonstrates high precision and speciﬁcity in detecting neural oscillations in30
time and frequency domains. The method’s speciﬁcity enables the detailed study of31
non-sinusoidal characteristics of oscillations, such as the degree of asymmetry and waveform of32
an oscillation. Furthermore, CHO can be applied to identify how neural oscillations govern33
interactions throughout the brain and to determine oscillatory biomarkers that index abnormal34
brain function.35
36
Introduction37
Neural oscillations in the mammalian brain are thought to play an important role in coordinating38
neural activity across different brain regions, allowing for the integration of sensory information,39
1 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
the control of motor movements, and the maintenance of cognitive functions (Pfurtscheller and40
Da Silva, 1999; Caplan et al., 2003 ; Buzsaki and Draguhn, 2004 ; Jensen and Mazaheri, 2010 ; Gi-41
raud and Poeppel, 2012 ; Schalk, 2015 ; Fries, 2015 ). Detecting neural oscillations is important in42
neuroscience as it helps unravel the mysteries of brain function, understand brain disorders, in-43
vestigate cognitive processes, track neurodevelopment, develop brain-computer interfaces, and44
explore new therapeutic approaches. Thus, detecting and analyzing the “when”, the “where”, and45
the “what” of neural oscillations is an essential step in understanding the processes that govern46
neural oscillations.47
For example, detecting the onset and offset of a neural oscillation (i.e., the “when”) is necessary48
to understand the relationship between oscillatory power/phase and neural excitation, an essen-49
tial step in explaining an oscillation’s excitatory or inhibitory function ( Pfurtscheller and Da Silva,50
1999; Canolty et al., 2006; Klimesch et al., 2007; Haegens et al., 2011; de Pesters et al., 2016). Local-51
izing the brain area or layer that generates the oscillation (i.e., the “where”) provides neuroanatomi-52
cal relevance to cognitive and behavioral functions (Buzsaki and Draguhn, 2004; Miller et al., 2010).53
Lastly, determining the oscillation’s fundamental frequency (i.e., the “what”) indicates underlying54
brain states (Penﬁeld and Jasper, 1954; Buzsaki and Draguhn, 2004 ). Together, the “when”, the55
“where”, and the “what” can be seen as the fundamental pillars in investigating the role of oscilla-56
tions in interregional communication throughout the brain (Fries, 2015). These fundamental pillars57
can also provide insight into the functional purpose (i.e., the “why”), underlying mechanisms (i.e.,58
the “how”), and pathologies (i.e., the “whom”) of neural oscillations ( Buzsaki and Draguhn, 2004;59
Buzsaki, 2006).60
The detection of neural oscillations has historically been extensively studied in the frequency-61
(Wen and Liu, 2016 ; Donoghue et al., 2020 ; Ostlund et al., 2022 ), time- (Hughes et al., 2012 ; Gips62
et al., 2017), and time-frequency domains (Chen et al., 2011; Wilson et al., 2022; Neymotin et al.,63
2022). With the notable exception of Gips et al. 2017, these studies assume that neural oscillations64
are predominantly sinusoidal and stationary in their frequency. However, there is an increasing re-65
alization that neural oscillations are actually non-sinusoidal and exhibit spurious phase-amplitude66
coupling (Belluscio et al., 2012; Cole et al., 2017; Scheffer-Teixeira and Tort, 2016; Gips et al., 2017;67
Donoghue et al., 2022). A recent review paper on methodological issues in analyzing neural oscilla-68
tions (Donoghue et al., 2022) identiﬁed determining the fundamental frequency of non-sinusoidal69
neural oscillations as the most challenging problem in building an understanding of how neural os-70
cillations govern interactions throughout the brain.71
Fast Fourier Transform (FFT) is the most commonly used method to detect neural oscillations.72
The FFT separates a neural signal into sinusoidal components within canonical bands of the fre-73
quency spectrum (e.g., theta, alpha, beta). The components of these canonical bands are typically74
considered to be functionally independent and involved in different brain functions. However,75
when applied to non-sinusoidal neural signals, the FFT produces harmonic phase-locked compo-76
nents at multiples of the fundamental frequency. While the asymmetric nature of the fundamental77
oscillation can be of great physiological relevance (Mazaheri and Jensen, 2008 ; Cole et al., 2017;78
Donoghue et al., 2022 ), its harmonics are considered to be an artifact produced by the FFT that79
can confound the detection and physiological interpretation of neural oscillation ( Belluscio et al.,80
2012; Donoghue et al., 2022 ).81
An example of an unﬁltered electrocorticographic recording from auditory cortex (Figure 1 A)82
illustrates the non-sinusoidal nature of neural oscillations. The associated FFT-based power spec-83
trum ( Figure 1 B) exhibits multiple peaks over 1/f noise even though only one oscillatory signal is84
visibly present in the time domain signal. Whether the peaks over 1/f at 12 and 18 Hz, are har-85
monics of 6 Hz oscillations or independent oscillations remains unknown. This ambiguity affects86
the ability to accurately and eﬃciently identify neural oscillations and understand their role in cog-87
nition and behavior. For this illustrative example of non-sinusoidal neural oscillation, we used a88
phase-phase coupling analysis (Belluscio et al., 2012) to determine whether the exhibited 18 Hz89
beta oscillation is a harmonic of the 6 Hz theta oscillation. This analysis conﬁrmed that the beta os-90
2 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
cillation was indeed a harmonic of the theta oscillation (Figure 1E and F). In marked contrast, for a91
sinusoidal neural oscillation, a phase-phase coupling analysis could not fully ascertain whether the92
oscillations are phase-locked and thus are harmonics of each other (Figure 1 G-L). This ambiguity,93
combined with the exorbitant computational complexity of the entailed permutation test and the94
requirement to perform the analysis across all cross-frequency bands over all channels and trials95
render phase-phase coupling impracticable for determining the fundamental frequency of neural96
oscillations in real-time and, thus, the use in closed-loop neuromodulation applications.97
In this study, we aim to deﬁne the principle criteria that characterize a neural oscillation and to98
synthesize these criteria into a method that accurately determines the duration (“when”), location99
(“where”), and fundamental frequency (“what”) of non-sinusoidal neural oscillations. For this pur-100
pose, we introduce the Cyclic Homogeneous Oscillation (CHO) detection method to identify neural101
oscillations using an auto-correlation analysis to identify whether a neural oscillation is an inde-102
pendent oscillation or a harmonic of another oscillation. Auto-correlation is a statistical measure103
that assesses the degree of similarity between a time series and a delayed version of itself.104
Thus, auto-correlation can explain the periodicity of a signal without assuming that the signal105
is sinusoidal. Further, the peaks in the output of the auto-correlation function indicate the fun-106
damental frequency of the neural oscillation. As shown in Figure 2, irrespective of the shape of107
neural oscillation ( Figure 2A and C), the fundamental frequency can be determined from the pos-108
itive peak-to-peak intervals (see Figure 2 B and D). Despite auto-correlation being a well-known109
method to identify the fundamental frequency of a signal, its application to neural oscillations has110
been impeded by the requirement to accurately determine the onset and offset of the oscillation.111
To overcome this limitation, we combine the auto-correlation method with the Oscillation Event112
(OEvent) method (Neymotin et al., 2022) to determine the onset/offset of oscillations. In this ap-113
proach, OEvent determines bounding boxes in the time-frequency domain that mark the onset114
and offset of suspected oscillations. Each bounding box is generated by identifying a period of115
signiﬁcantly increased power from averaged power spectrum. To further improve OEvent, we re-116
placed the empirical threshold that identiﬁes bounding boxes in the time-frequency domain with117
a parametric threshold driven by an estimation of the underlying 1/f noise ( Donoghue et al., 2020),118
as shown in Figure 3A.119
Furthermore, we improved OEvent to reject any short-cycled oscillations that could represent120
evoked potentials (EP), event-related potentials (ERP), or spike activities, as shown in Figure 3B. In121
general, EPs or ERPs in neural signals generate less than two cycles of ﬂuctuations. Large-amplitude122
EPs, ERPs, and spike activities can result in spurious oscillatory power in the frequency domain123
(de Cheveigné and Nelken, 2019 ; Donoghue et al., 2020 , 2022).124
In the ﬁnal step, we determine the oscillation’s periodicity and fundamental frequency by iden-125
tifying positive peaks in the auto-correlation of the signal. As shown for a representative oscillation126
in Figure 3C, the center frequency of the highlighted bounding box is 24 Hz, but the periodicity of127
the underlying raw signal does not match the calculated fundamental frequency of 7 Hz. Conse-128
quently, this bounding box at 24 Hz will be rejected. Finally, we merge those remaining bounding129
boxes that neighbor each other in the frequency domain and overlap more than 75% ( Neymotin130
et al., 2022) in time.131
In summary, the presented CHO method identiﬁes neural oscillations that fulﬁll the following132
three criteria: 1) oscillations (peaks over 1/f noise) must be present in the time and frequency133
domains; 2) oscillations must exhibit at least two full cycles; and 3) oscillations must have auto-134
correlation. These criteria are supported by studies in the neuroscience literature ( Buzsaki and135
Draguhn, 2004; Niedermeyer and da Silva, 2005 ; Buzsaki, 2006; Cohen, 2014; de Cheveigné and136
Nelken, 2019; Donoghue et al., 2020, 2022). The synthesis of these criteria into the presented137
method allows us to detect and identify non-sinusoidal oscillations and their fundamental fre-138
quency. This is because criteria #1 (i.e., the presence of an oscillation) and #2 (i.e., the length of139
the oscillation) identify potential oscillations, which are then tested to be fundamental oscillations140
using an auto-correlation analysis using criteria #3 (i.e., the periodicity of an oscillation).141
3 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
0 0.5
0 2 4 6 8 10
0
0.2
0.4
0.6
0.8
1
Original0
0.35
0.7
0 0.5
0 2 4 6 8 10
0
0.2
0.4
0.6
0.8
1
0
0.35
0.7
A non-sinusoidal neural oscillation A sinusoidal neural oscillation
 φθ
 φβ
θ
β
Band passed signals and phase time series
 φθ
 φβ
θ
β
Time-frequency map
Phase-phase coupling (1:m) Phase-phase coupling (1:m)
1:m phase locking value (R1:m)
1:m phase locking value (R1:m)
Permutation Original Permutationmm
n:m= 1:3
Original
Permutation
Original
Permutation
***
Theta : Beta = 1:3
Time-frequency map
0.3 0.6 0.9 1.2 1.5 
time (sec)
10
20
30
40
0.3 0.6 0.9 1.2 1.5 
time (sec)
10
20
30
40
Band passed signals and phase time series
100100
/uni03BCV
sec
/uni03BCV
sec 5 10 15 20 25 30 35 40
0
1
2
3
dB
Hz
θ
β
5 10 15 20 25 30 35 40-1
0
1
2
3
Power spectrum
Multi-gaussian fitting
1/f noisedB
Hz
θ
β
A HB G
C D I J
E F K L
1 1 N.SCoupling 1xBeta and 3xTheta
n:m= 1:3
Coupling 1xBeta and 3xTheta
Theta : Beta = 1:3
Figure 1. Examples of non-sinusoidal and sinusoidal neural oscillations recorded from the human
auditory cortex. Detecting the presence, onset/offset, and fundamental frequency of non-sinusoidal
oscillations is challenging. This is because the power spectrum of the non-sinusoidal theta-band oscillation
(A) exhibits multiple harmonic peaks in the alpha and beta bands (B). The peaks of these harmonics are also
exhibited in the time-frequency domain (C). To determine whether these peaks are independent oscillations
or harmonics of the fundamental frequency, we tested whether fundamental theta oscillation and potential
beta-band harmonic oscillations exhibit a 1:3 phase-locking (D-F), i.e., whether the beta-band oscillation is a
true 3rd harmonic of the fundamental theta-band oscillation. In our test, we found that the theta-band
oscillation was signiﬁcantly phase-locked to the beta-band oscillation with a 1:3 ratio in their frequencies (F).
This means that the tested theta- and beta-band oscillations are part of one single non-sinusoidal neural
oscillation. We applied the same statistical test to a more sinusoidal neural oscillation (G). Since this neural
oscillation more closely resembles a sinusoidal shape, it does not exhibit any prominent harmonic peaks in
the alpha and beta bands within the power spectrum (H) and time-frequency domain (I). Consequently, our
test found that the phase of the theta-band and beta-band oscillations were not phase-locked (J-L). Thus, this
statistical test suggests the absence of a harmonic structure.
To verify and validate CHO, we applied the above-presented principle criteria on simulated non-142
sinusoidal signals and human electrophysiological signals, including electrocorticographic (ECoG)143
signals recorded from the lateral brain surface, electroencephalographic signals (EEG) recorded144
from the scalp, and local ﬁeld potentials recorded from the hippocampus using stereo EEG (SEEG).145
We further validated our approach by comparing CHO to other commonly used methods.146
To determine the spectral accuracy in detecting the peak frequency of non-sinusoidal oscil-147
lations, we compared CHO to established methods, including the ﬁtting of oscillations using 1/f148
(FOOOF, also known as specparam, Donoghue et al. 2020 ), the OEvent method ( Neymotin et al.,149
2022), and the Spectral Parameterization Resolved in Time ( SPRiNT, Wilson et al. 2022 ) methods.150
Moreover, to determine the spectro-temporal accuracy in detecting both the peak frequency and151
the onset/offset of non-sinusoidal oscillations, we compared CHO with the OEvent method.152
The selection of FOOOF, SPRiNT, and OEvent is based on their fundamental approaches. To the153
best of our knowledge, FOOOF is the most representative method for detecting the peak frequency154
of neural oscillations. SPRiNT expands the FOOOF method into the time-frequency domain, and155
OEvent can determine the onset/offset of the detected oscillations.156
4 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
0 0.5 1.0 1.5
-200
-100
0
100
200
0 0.25 0.5 0.75 1.0
-1
-0.5
0
0.5
1
152 ms 307 ms
0 0.5 1.0 1.5
-200
-100
0
100
200
0 0.25 0.5 0.75 1.0
-1
-0.5
0
0.5
1
A non-sinusoidal neural oscillation A sinusoidal neural oscillation 
sec sec
sec sec
160 ms
335 ms
Auto-correlation
A
C
B
D
dB
Hz
6 Hz
dB
Hz
6 Hz
1000 ms / (307 - 152) ms ≈ 6 Hz 1000 ms / (335 - 160) ms ≈ 6 Hz
Amplitude in /uni03BCV
Time
lag
Figure 2. Using auto-correlation to determine the fundamental frequency of non-sinusoidal and
sinusoidal neural oscillations recorded from the human auditory cortex. (A) Temporal dynamics of
non-sinusoidal (left) and sinusoidal (right) neural oscillation and (B) their auto-correlation. The periodicity of
peaks in the auto-correlation reveals the fundamental frequency of the underlying oscillation. Asymmetry in
peaks and troughs of the auto-correlation is indicative of a non-sinusoidal oscillation.
Results157
The following sections describe the results of our study: The ﬁrst section presents simulation re-158
sults by comparing the accuracy of CHO with that of existing methods in detecting non-sinusoidal159
oscillations. The second section reports physiological results by comparing the accuracy of CHO160
with that of established methods in detecting oscillations within in-vivo recordings.161
Synthetic results162
To determine the speciﬁcity and sensitivity of CHO in detecting neural oscillations, we applied CHO163
to synthetic non-sinusoidal oscillatory bursts (2.5 cycles, 1–3 seconds long) convolved with 1/f noise,164
also known as pink noise, which has a power spectral density that is inversely proportional to the165
frequency of the signal. As shown in Figure 4, we generated 5s-long 1/f signals composed of166
pink noise and added non-sinusoidal oscillations of different lengths (one cycle, two-and-a-half167
cycles, 1s-duration, and 3s-duration). The rightmost panel of Figure 4A shows two examples of168
non-sinusoidal oscillations (two-and-a-half cycles and 2s-duration) along with their power spectra.169
As can be seen in Figure 4A, longer non-sinusoidal oscillations exhibit stronger harmonic peaks.170
Our results in Figure 4B-D demonstrate that CHO outperforms conventional techniques in speci-171
ﬁcity and accuracy for detecting the peak frequency of non-sinusoidal oscillations. High speciﬁcity172
depends on high true-negative and low false-positive rates. For conventional methods, we ex-173
pected harmonic oscillations to increase the false-positive rate and one-cycled oscillations to de-174
crease the true-negative rate. As expected, conventional methods detected harmonic and one-175
cycled oscillations as true oscillations. For example, the average speciﬁcity of SPRiNT was below176
0.3, which was signiﬁcantly lower than the robust speciﬁcity of CHO across the entire range of SNR.177
We also observed that CHO requires a higher SNR to detect the presence of oscillations. Sen-178
sitivity depends on the true-positive and the false-negative rates. We found existing methods to179
be overly sensitive in detecting the presence of oscillations. At the same time, this severely limits180
their speciﬁcity and, thus, their ability to accurately detect the presence and frequency of an oscil-181
lation. Based on our physiological datasets, we found the average SNR of oscillations in EEG and182
5 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
A. Remove 1/f noise in time-frequency map
Time-frequency map Flattened time-frequency map
B. Reject short cycles (< 2 cycles)
0.3 0.6 0.9 1.2 Time (sec) 
10
20
30
Hz
Initial bounding boxes above 1/f Bounding boxes (> 2 cycles)
C. Reject boxes with different periodicity with its autocorrelation
0.3 0.6 0.9 1.2 
10
20
30
0.3 0.6 0.9 1.2 
10
20
30
0.3 0.6 0.9 1.2 
10
20
30
Bounding boxes (> 2 cycles) Merged bounding boxes
The center frequency = 24 Hz
Frequency in raw signal = 7 Hz
Checking the center frequency equals to fre-
quency in raw signal (e.g. 24 Hz = 7 Hz ?)
0.5 sec
200 µV 
7 Hz
Merging survived bounding boxes
Figure 3. Procedural steps of CHO. (A) First, to identify periodic oscillations, CHO removes the underlying 1/f
aperiodic noise in the time-frequency space and generates initial bounding boxes of candidate oscillations.
(B) In the second step, CHO rejects bounding boxes that exhibit less than two oscillatory cycles. (C) In the ﬁnal
step, CHO limits the analysis to only those bounding boxes that exhibit the same frequency in the
time-frequency map and auto-correlation. Each remaining bounding box is characterized by onset/offset,
frequency range, center frequency, and number of cycles.
6 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
0
0.2
0.4
0.6
0.8
0
0.2
0.4
0.6
0.8
0
0.2
0.4
0.6
0.8
Spectral accuracy for detecting the fundamental frequency of non-sinusoidal oscillations
1/f noise Non-sinusoidal oscillations Simulation signals+ = Power spectrums
Simulation signal
1/f noise signal
dB
dB
Hz
Hz
5 10 20 30
5 10 20 30
+ =
Simulation examples
Spectro-temporal accuracy for detecting the fundamental frequency and onset/offset of non-sinusoidal oscillations
0
0.2
0.4
0.6
0.8
0
0.2
0.4
0.6
0.8
0
0.2
0.4
0.6
0.8
SPECIFICITY SENSITIVITY ACCURACY
SPECIFICITY SENSITIVITY ACCURACY
SNR (dB)
B C D
E F G
A
-24 -20 -16 -12 -8 -4 0  
-24 -20 -16 -12 -8 -4 0  
-24 -20 -16 -12 -8 -4 0  
CHO
OEvent
Fooof
SPRiNT
-24 -20 -16 -12 -8 -4 0  
SNR (dB)
-24 -20 -16 -12 -8 -4 0  -24 -20 -16 -12 -8 -4 0  
ECoG  EEG  
ECoG  EEG  
1.0 1.0 1.0
CHO
OEvent
Figure 4. Performance of CHO in detecting synthetic non-sinusoidal oscillations. (A) We evaluated CHO
by verifying its speciﬁcity, sensitivity, and accuracy in detecting the fundamental frequency of non-sinusoidal
oscillatory bursts (2.5 cycles, 1–3 seconds long) convolved with 1/f noise. (B-D) CHO outperformed existing
methods in detecting the fundamental frequency of non-sinusoidal oscillation (FOOOF: ﬁtting oscillations one
over f (Donoghue et al., 2020 ), OEvent ( Neymotin et al., 2022 ): Oscillation event detection method, and
SPRiNT (Wilson et al., 2022 ): Spectral Parameterization Resolved in Time) in speciﬁcity and accuracy, but not
in sensitivity. CHO exhibited fewer false-positive and more true-negative detections than existing methods.
(C) However, at SNR-levels of alpha oscillations found in EEG and ECoG recordings (i.e., -7 dB and -6 dB,
respectively), the sensitivity of CHO in detecting the peak frequency of non-sinusoidal oscillation is
comparable to that of SPRiNT. (D) This means that the overall accuracy of CHO was higher than that of
existing methods. (E-G) CHO outperformed existing methods in detecting the fundamental frequency and
onset/offset of non-sinusoidal oscillation. (F) Similar to the results shown in (C) CHO can effectively detect the
fundamental frequency and onset/offset for more than half of all oscillations at SNR-levels of alpha
oscillations found in EEG and ECoG recordings.
Figure 4—ﬁgure supplement 1. SNR Histograms of EEG and ECoG.
Figure 4—ﬁgure supplement 2. Synthetic sinusoidal oscillations.
7 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Delta (<3Hz) Theta (3-6Hz) Alpha (7-14Hz) Beta (15-30Hz) Low Gamma (31-40Hz)
FOOOF
CHO
Normalized Power
1
0
0.2
0.4
0.6
0.8
A
B
*
*
*
*
*
*
*
*
0 0.5 1 1.5
caudal middle frontal
inferior temporal
middle temporal
pars opercularis
pars triangularis
postcentral
precentral
superior temporal
supra marginal
0 0.5 1 1.5 0 0.5 1 1.5
*
*
*
*
*
*
0 0.5 1 1.5
*
*
*
*
*
*
*
*
*
0 0.5 1 1.5
occurence per sec
CHO
FOOOF
caudal middle frontal
inferior temporal
middle temporal
pars opercularis
pars triangularis
postcentral
precentral
superior temporal
supra marginal
Figure 5. Validation of CHO in detecting oscillations in ECoG signals. (A) We applied CHO and FOOOF to
determine the fundamental frequency of oscillations from ECoG signals recorded during the pre-stimulus
period of an auditory reaction time task. FOOOF detected oscillations primarily in the alpha- and beta-band
over STG and pre-motor area. In contrast, CHO also detected alpha-band oscillations primarily within STG,
and more focal beta-band oscillations over the pre-motor area, but not STG. (B) We investigated the
occurrence of each oscillation within deﬁned cerebral regions across eight ECoG subjects. The horizontal bars
and horizontal lines represent the median and median absolute deviation (MAD) of oscillations occurring
across the eight subjects. An asterisk (*) indicates statistically signiﬁcant differences in oscillation detection
between CHO and FOOOF (Wilcoxon rank-sum test, p<0.05 after Bonferroni correction).
Figure 5—ﬁgure supplement 1. ECoG results using FOOOF and CHO for all subjects.
ECoG to be -7 dB and -6 dB, respectively ( Figure 4—ﬁgure Supplement 1). When tested at these183
physiologically-motivated SNR levels, and found that the sensitivity of CHO is comparable to that184
of SPRiNT. Overall, when considering the accuracy combined with speciﬁcity and sensitivity, CHO185
outperformed all other methods in detecting the peak frequency of non-sinusoidal oscillations at186
the physiologically motivated SNR levels.187
In addition to determining the accuracy in detecting the presence of oscillations and determin-188
ing their peak frequency, we also determined the accuracy of all methods in detecting the onset189
and offset of oscillations. This comparison is limited to OEvent because FOOOF and SPRiNT meth-190
ods cannot determine the onset and offset of short oscillations. In this analysis, CHO outperformed191
the OEvent method in speciﬁcity but not sensitivity, as shown in Figure 4E-G. Speciﬁcally, we found192
performance trends similar to those in our previous simulation result (Figure 4 B-D). Thus, CHO193
outperforms conventional techniques in speciﬁcity for detecting both the peak frequency and on-194
set/offset of oscillations.195
Empirical results196
We further assessed CHO by testing it on electrophysiological signals recorded from human sub-197
jects. Speciﬁcally, we evaluated CHO on electrocorticographic (ECoG, x1–x8, 8 subjects) and elec-198
troencephalographic (EEG, y1–y7, 7 subjects) signals recorded during the pre-stimulus period of an199
auditory reaction time task. Furthermore, we also evaluated CHO on signals recorded during rest-200
ing state from cortical areas and hippocampus using ECoG (ze1–ze8, N=6) and stereo EEG (zs1–zs6,201
6 subjects).202
8 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
FOOOF
Normalized Power
1
0
0.2
0.4
0.6
0.8
Alpha entropy (MAX = 4.16)
 CHO = 3.82, FOOOF = 4.15
Beta entropy (MAX = 4.16)
 CHO = 4.05, FOOOF = 4.15
Delta (<3Hz) Theta (3-6Hz) Alpha (7-14Hz) Beta (15-30Hz) Low Gamma (31-40Hz)A
B
C
CHO
***
********************** *****
*****************************
0 0.5 1 1.5
FC5
FC3
FC1
FCz
FC2
FC4
FC6
C5
C3
C1
Cz
C2
C4
C6
CP5
CP3
CP1
CPz
CP2
CP4
CP6
Fp1
Fpz
Fp2
AF7
AF3
Afz
AF4
AF8
F7
F5
F3
F1
Fz
F2
F4
F6
F8
FT7
FT8
T7
T8
T9
T10
TP7
PT8
P7
P5
P3
P1
Pz
P2
P4
P6
P8
PO7
PO3
POz
PO4
PO8
O1
Oz
O2
Iz
*
***
**********************************************************
0 0.5 1 1.5 0 0.5 1 1.5
********************** ** ** ********************** ****************
0 0.5 1 1.5
*********************************** ************ *****************
0 0.5 1 1.5
occurence per sec
CHO
FOOOF
FC5
FC3
FC1
FCz
FC2
FC4
FC6
C5
C3
C1
Cz
C2
C4
C6
CP5
CP3
CP1
CPz
CP2
CP4
CP6
Fp1
Fpz
Fp2
AF7
AF3
Afz
AF4
AF8
F7
F5
F3
F1
Fz
F2
F4
F6
F8
FT7
FT8
T7
T8
T9
T10
TP7
PT8
P7
P5
P3
P1
Pz
P2
P4
P6
P8
PO7
PO3
POz
PO4
PO8
O1
Oz
O2
Iz
0 0.2 0.4 0.6
CHO
FOOOF
0 0.2 0.4 0.6
*
*
0 0.2 0.4 0.6
*
0 0.2 0.4 0.6 0 0.2 0.4 0.6
FC2-FC4
O1-O2
occurence per sec
Figure 6. Validation of CHO in detecting oscillations in EEG signals. (A) We applied CHO and FOOOF to
determine the fundamental frequency of oscillations from EEG signals recorded during the pre-stimulus
period of an auditory reaction time task. FOOOF primarily detected alpha-band oscillations over frontal/visual
areas and beta-band oscillations across all areas (with a focus on central areas). In contrast, CHO detected
alpha-band oscillations primarily within visual areas and detected more focal beta-band oscillations over the
pre-motor area, similar to the ECoG results shown in Figure 5. (B) We investigated the occurrence of each
oscillation within the EEG signals across seven subjects. An asterisk (*) indicates statistically signiﬁcant
differences in oscillation detection between CHO and FOOOF (Wilcoxon rank-sum test, p<0.05 after
Bonferroni correction). CHO exhibited lower entropy values of alpha and beta occurrence than FOOOF across
64 channels. (C) We compared the performance of FOOO and CHO in detecting oscillation across visual and
pre-motor-related EEG channels. CHO detected more alpha and beta oscillations in visual cortex than in
pre-motor cortex. FOOOF detected alpha and beta oscillations in visual cortex than in pre-motor cortex.
Figure 6—ﬁgure supplement 1. All EEG results using FOOOF and CHO.
9 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Electrocorticographic (ECoG) results203
In the auditory reaction time task, we expected to observe neural low-frequency oscillations during204
the pre-stimulus period within task-relevant areas, such as the auditory and motor cortex. As205
we expected, we found alpha and beta oscillations within these cortical areas. We compared the206
topographic distribution of the oscillations detected by FOOOF with those detected by CHO. As207
shown in Figure 5 A for one representative subject, FOOOF detected the presence of alpha, and208
beta oscillations within temporal and motor cortex. In contrast, while CHO also detected alpha209
oscillations in temporal and motor cortex, it only detected beta oscillations in motor cortex. We210
found this pattern to be consistent across subjects, as shown in Figure 5 B and Figure 5 —ﬁgure211
Supplement 1.212
We compared neural oscillation detection rates between CHO and FOOOF across eight ECoG213
subjects. We used FreeSurfer (Fischl, 2012 ) to determine the associated cerebral region for each214
ECoG location. Each subject performed approximately 400 trials of a simple auditory reaction-time215
task. We analyzed the neural oscillations during the 1.5-second-long pre-stimulus period within216
each trial. CHO and FOOOF demonstrated statistically comparable results in the theta and alpha217
bands despite CHO exhibiting smaller median occurrence rates than FOOOF across eight subjects.218
Notably, within the beta band, excluding speciﬁc regions such as precentral, pars opercularis, and219
caudal middle frontal areas, CHO’s beta oscillation detection rate was signiﬁcantly lower than that220
of FOOOF (Wilcoxon rank-sum test, p < 0.05 after Bonferroni correction). This suggests comparable221
detection rates between CHO and FOOOF in premotor and Broca’s areas, while the detection of222
beta oscillations by FOOOF in other regions, such as the temporal area, may represent harmonics223
of theta or alpha, as illustrated in Figure 5A and B. Furthermore, FOOOF exhibited a higher sensi-224
tivity in detecting delta, theta, and low gamma oscillations overall, although both CHO and FOOOF225
detected only a limited number of oscillations in these frequency bands.226
Electroencephalographic (EEG) results227
We expected that the EEG would exhibit similar results as seen in the ECoG results. Indeed, the EEG228
results mainly exhibit alpha and beta oscillations during the pre-stimulus periods of the auditory229
reaction time task, as shown in Figure 6. Speciﬁcally, FOOOF found alpha oscillations in mid-frontal230
and visual areas and beta oscillations throughout all areas of the scalp. In contrast, CHO found231
more focal visual alpha and pre-motor beta. Furthermore, the low gamma oscillations detected by232
CHO were also more focal than those detected by FOOOF. We found these results to be consistent233
across subjects (see Figure 6B, C and Figure 6—ﬁgure Supplement 1).234
We assessed the difference in neural oscillation detection performance between CHO and FOOOF235
across seven EEG subjects. We used EEG electrode locations according to the 10-10 electrode sys-236
tem (Nuwer, 2018) and assigned each electrode to the appropriate underlying cortex (e.g., O1 and237
O2 for the visual cortex). Each subject performed 200 trials of a simple auditory reaction-time238
task. We analyzed the neural oscillations during the 1.5-second-long pre-stimulus period. In the239
alpha band, CHO and FOOOF presented statistically comparable outcomes. However, CHO exhib-240
ited a greater alpha detection rate for the visual cortex than for the pre-motor cortex, as shown241
in Figure 6B and C. The entropy of CHO’s alpha oscillation occurrences (3.82) was lower than that242
of FOOOF (4.15), with a maximal entropy across 64 electrodes of 4.16. Furthermore, in the beta243
band, CHO’s entropy (4.05) was smaller than that of FOOOF (4.15). These ﬁndings suggest that244
CHO may offer a more region-speciﬁc oscillation detection than FOOOF. As illustrated in Figure 6C,245
CHO found fewer alpha oscillations in pre-motor cortex (FC2 and FC4) than in occipital cortex (O1246
and O2), while FOOOF found more beta oscillations occurrences in pre-motor cortex (FC2 and FC4)247
than in occipital cortex. However, FOOOF found more alpha and beta oscillations in visual cortex248
than in pre-motor cortex. Consistent with ECoG results, FOOOF demonstrated heightened sensi-249
tivity in detecting delta, theta, and low gamma oscillations. Nonetheless, both CHO and FOOOF250
identiﬁed only a limited number of oscillations in delta and theta frequency bands. Contrary to the251
ECoG results, FOOOF found more low gamma oscillations in EEG subjects than in ECoG subjects.252
10 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Onset and offset of neural oscillations253
So far, we have established that CHO can localize beta rhythms within pre-motor cortex in EEG and254
ECoG. Here, we are interested in determining the accuracy of the onset/offset detection of neural255
oscillations. For this purpose, we tested whether CHO, applied to signals recorded from auditory256
cortex during an auditory reaction-time task, can accurately detect the transition between resting257
and task periods. Speciﬁcally, we expected CHO to detect the offset times of neural oscillations258
after the stimulus onset (i.e., a beep tone that remained until a button was pressed). Based on the259
principle of event-related de-/synchronization (ERD/ERS, Pfurtscheller and Da Silva 1999), cortical260
neurons may be de-synchronized to process an auditory stimulus. As shown in Figure 7 , CHO261
successfully detected offset times of 7 Hz neural oscillations. During the pre-stimulus period, the262
distribution of the onset time remains uniform, reﬂecting the subject waiting for the stimulus. In263
contrast, after the stimulus onset, the distribution of onset times becomes Gaussian, reﬂecting264
the variable reaction time to the auditory stimulus. Of note, the detection of onset times peaks265
950 ms post-stimulus, which occurs signiﬁcantly later than the button press that happens 200 ms266
post-stimulus (Figure 7 B).267
Similar to the distribution of onset times, the distribution of offset times remained uniform268
throughout the pre-stimulus period. After stimulus onset, the distribution becomes Gaussian, with269
a peak of offset detections at 300 ms post-stimulus, or 200 ms post-response (i.e., the button press)270
(Figure 7C).271
In summary, this means that, on average, the detected 7 Hz oscillations de-synchronized 250 ms272
and synchronized 900 ms, post-stimulus, respectively.273
Stereoelectroencephalographic (SEEG) results274
We also investigated neural oscillations within the hippocampus. Speciﬁcally, we were interested in275
the frequency and duration of hippocampal oscillations, which are known to be non-sinusoidal and276
a hallmark of memory processing ( Buzsaki, 2006; Lundqvist et al., 2016 ). Using the CHO method,277
we plotted a representative example of detected hippocampal fast theta bursts ( Lega et al., 2012 ;278
Goyal et al., 2020), as shown in Figure 8. As expected, the non-sinusoidal alpha-band oscillations279
also resulted in harmonic oscillations in the beta band, which, while not clearly visible in the power280
spectrum (Figure 8 B), can be clearly seen in the time-frequency analysis (Figure 8 D and Figure 8E).281
In contrast to the ECoG and EEG results, the frequency of beta-band oscillations in the hippocam-282
pus exhibited a frequency close to the alpha-band (8–14 Hz). CHO found primarily alpha-band283
oscillations in the hippocampus (see Figure 8—ﬁgure Supplement 1). When comparing the consis-284
tency between CHO and FOOOF across hippocampal locations, CHO exhibits more speciﬁc results285
with less overlap between alpha and beta locations and almost no detection in the low-gamma286
band (30–40 Hz). For example, subject zs4 in Figure 8 —ﬁgure Supplement 1 shows alpha and287
beta locations mutually supplement each other when using CHO but not when using the FOOOF288
method. However, we did not ﬁnd a statistically signiﬁcant difference between CHO and FOOOF289
due to the small number of subjects and variable electrode locations within hippocampus across290
the six SEEG subjects.291
Frequency and duration of neural oscillations292
Here, we are interested in identifying the predominant frequency and duration of neural oscilla-293
tions for speciﬁc brain areas during the resting state. For this purpose, we ﬁrst determined the294
speciﬁc Brodmann area of each recording electrode using an intracranial electrode localization295
tool, Versatile Electrode Localization Framework (VERA, Adamek et al. 2022). Next, we investigated296
electrodes belonging to the primary auditory cortex (i.e., Brodmann areas 41 and 42), as shown in297
Figure 9A. We found that 7 and 11 Hz oscillations were the predominant neural oscillations for elec-298
trodes near the primary auditory cortex. The average duration of an 11 Hz oscillation was 450 ms.299
Next, our results for primary motor cortex (i.e., Brodmann area 4) showed that 7 Hz was the pre-300
dominant oscillation frequency in the motor cortex with 450 ms duration on average, as shown in301
11 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
-1500 -1000 -500 0 500 1000 1500
Time (ms)
5
10
15
20
25
30
35
40Frequency (Hz)
7 Hz
950 ms
-1500 -1000 -500 0 500 1000 1500
Time (ms)
300 ms
0
0.2
0.4
0.6
0.8
1
Normalized
A C D
High gamma activated ECoG 
locations for auditory beep stimuli
Frequency-onset time histograms for 
detected neural oscillations
Frequency-offset time histograms for 
detected neural oscillations
200 ms
Onset
Reaction
Offset
Reaction
Auditory
stimulus Button 
Press
0s 1s
B
Pre-stimulus Post-stimulus Pre-stimulus Post-stimulus
Pre-stimulus Post-stimulus
200 ms
-1500 -1000 -500 0 500 1000 1500
Time (ms)
-1500 -1000 -500 0 500 1000 1500
Figure 7. Application of CHO in determining the spatio-temporal characteristics of neural oscillations
in ECoG signals during a reaction-time task. (A) We selected those cortical locations (red) from all locations
(black) that exhibited a signiﬁcant broadband gamma response to an auditory stimulus in a reaction-time
task. (B) In this task, the subjects were asked to react as fast as possible with a button press to a salient
auditory stimulus. (C-D) Onset and offset times of detected neural oscillations. Fundamental oscillations were
centered around 7 Hz (left histogram). Onset and offset times during pre-stimulus period exhibited a uniform
distribution, indicating that 7 Hz oscillations randomly started and stopped during this period. A trough in the
onset and a peak in the offset of 7 Hz oscillations is visible from the histograms, indicating a general decrease
of the presence of neural oscillations immediately following the auditory stimulus. The subjects responded
with a button press within 200 ms of the auditory stimulus, on average. The prominent peak in the offset and
onset of oscillations at 300 ms and 950 ms post-stimulus, respectively, indicates a suspension of oscillations
in response to the auditory stimulus, and their reemergence after the execution of the button press behavior.
Figure 9B. We found that motor cortex exhibits more beta-band oscillations (around 500 ms dura-302
tion) than the auditory cortex. Next, Broca’s area exhibited characteristics similar to those of the303
motor cortex, however, with a predominant beta-band frequency of 17 Hz, which is lower than the304
22 or 24 Hz oscillations found in the motor cortex ( Figure 9C). Lastly, using SEEG electrodes, we305
investigated neural oscillations within the human hippocampus ( Figure 9D). This analysis showed306
that 8 Hz was the predominant oscillatory frequency in the hippocampus with a 450 ms duration307
on average. During the resting state, neural alpha- and beta-band oscillations within the hippocam-308
pus were shorter than in the motor cortex (p<0.05, Wilcoxon rank sum test, N=6).309
Discussion310
Our novel CHO method demonstrates high precision and speciﬁcity in detecting neural oscillations311
in time and frequency domains. The method’s speciﬁcity enables the detailed study of spatio-312
temporal dynamics of oscillations throughout the brain and the investigation of oscillatory biomark-313
ers that index functional brain areas.314
High speciﬁcity for detecting neural oscillations315
In our simulation study, CHO demonstrated high speciﬁcity in detecting both the peak and on-316
set/offset of neural oscillations in time and frequency domains. This high speciﬁcity directly results317
from the three criteria we established in this study. The ﬁrst criterion was that neural oscillations318
(peaks over 1/f noise) must be present in the time and frequency domain. The 1/f trend estimation319
served as a threshold to reject aperiodic oscillatory power in the neural signals (Donoghue et al.,320
2020).321
Next, the second condition was that oscillations must exhibit at least two complete cycles. This322
condition distinguishes periodic oscillations from evoked/event-related potentials (EP/ERP) and323
spike artifacts. EP/ERP have spectral characteristics that are similar to those of theta or alpha324
frequency oscillations. To discriminate EP/ERPs from genuine oscillations, we reject them if they325
don’t exhibit peaks over 1/f or if they have fewer than two cycles.326
12 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
1 2 3 4 5 6 7 8 9 
-400
0μV
400
7Hz 8Hz8Hz9Hz 10Hz
time
10
20
30
Hz
10
20
30
1 2 3 4 5 6 7 8 9 sec 
Hz
Superior View
0 10 20 30 40
Hz
0.5
1
1.5
2
A. Hippocampus contacts
B. Power spectrum
C. Detected hippocampal fast theta bursts
D. Initial bounding boxes
E. Final bounding boxes
0
Power specturm
1/f fitting
Figure 8. Application of CHO in determining the fundamental frequency and duration of hippocampal
oscillations in SEEG signals during resting state. (A) We recorded hippocampal oscillations from one
representative human subject implanted with SEEG electrodes within the left anterior hippocampus. (B)
Power spectrum (blue) and 1/f trend (red) for one electrode within the anterior-medial left hippocampus (red
dot in A). The power spectrum of a 10-second-long hippocampal signal indicates the presence of neural
activity over a 1/f trend across a wide frequency band up to 30 Hz. (C) In marked contrast to the relatively
unspeciﬁc results indicated by the power spectrum, CHO detected several distinct hippocampal fast theta
bursts. (D) This detection is based on ﬁrst denoising the power spectrum using 1/f ﬁtting (principle criterion
#1 of CHO), which yields initial bounding boxes that include short-cycled oscillations and harmonics. (E) The
auto-correlation step then successfully removes all short-cycled oscillations and harmonics, with only those
bounding boxes remaining that exhibit a fundamental frequency.
Figure 8—ﬁgure supplement 1. All results from six SEEG subjects using the FOOOF and CHO methods.
13 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
0 500 1000 1500 2000 2500 3000
Duration (ms)
5
10
15
20
25
30
35
40Frequency (Hz)11 Hz
450 ms
Detected neural oscillations on the primary 
auditory cortex (Brodmann area 41/42, N=6)A
0 500 1000 1500 2000 2500 3000
Duration (ms)
5
10
15
20
25
30
35
40Frequency (Hz)
7 Hz
450 ms
Detected neural oscillations on the primary 
motor coretex (Brodmann area 4, N=6)B
Detected neural oscillations on 
hippocampal contacts (N=6)
0 500 1000 1500 2000 2500 3000
Duration (ms)
5
10
15
20
25
30
35
40Frequency (Hz)
8 Hz
450 ms
DDetected neural oscillations on the Broca’s area 
(Brodmann area 44/45, N=6)
C
0 500 1000 1500 2000 2500 3000
Duration (ms)
5
10
15
20
25
30
35
40Frequency (Hz)
7 Hz
450 ms
0
0.2
0.4
0.6
0.8
1
Normalized
0
0.2
0.4
0.6
0.8
1
Normalized
0
0.2
0.4
0.6
0.8
1
Normalized
0
0.2
0.4
0.6
0.8
1
Normalized
ECoG ECoG
ECoG SEEG
Figure 9. Application of CHO in determining the fundamental frequency and duration of neural
oscillations in auditory cortex, motor cortex, Broca’s area, and hippocampus during resting state. This
ﬁgure presents the distribution of detected oscillations in a 2-dimensional frequency/duration histogram and
projected onto frequency and duration axes. The red line indicates the rejection line (less than two cycles). (A)
In primary auditory cortex (Brodmann area 41/42), the most dominant frequency and duration in the auditory
cortex was 11 Hz with 450 ms duration. (B) The primary motor cortex’s most dominant frequency was 7 Hz
with 450 ms duration, but more beta rhythms were detected with >500 ms duration than in auditory cortex.
(C) Broca’s area exhibits similar characteristics to that of motor cortex, but dominant beta-band oscillations
were found to be less present than in motor cortex. (D) Hippocampus primarily exhibits 8 Hz oscillations with
450 ms duration. 14 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
The third and ﬁnal condition is that oscillations should share the same periodicity as their auto-327
correlation. This is because positive peaks in the auto-correlation can identify the oscillation’s fun-328
damental frequency even if it is non-sinusoidal. The bounding boxes help us to identify possible329
onsets/offsets of neural oscillations. Moreover, calculating the auto-correlation of the raw signals330
within a bounding box provides the true periodic frequency of the raw signal. We then reject any331
bounding boxes for which the periodicity of the raw signal is not in alignment with the true periodic332
frequency revealed by the auto-correlation. This third condition is important in rejecting harmonic333
peaks over 1/f noise in the frequency domain. Furthermore, it is also effective in rejecting spurious334
oscillations, which are broadly generated by spike activities in the frequency domain (de Cheveigné335
and Nelken, 2019).336
To calculate the auto-correlation, we ﬁrst needed to determine the onset/offset of the potential337
oscillations. The ﬁrst and second criteria serve as a triage in ﬁnding the onset/offset of genuine338
oscillations. Thus, these three principle criteria were essential to reject aperiodic harmonic oscilla-339
tions and increase CHO’s speciﬁcity in detecting both the peak frequency and the onset/offset of340
non-sinusoidal oscillations. We also evaluated CHO on purely sinusoidal oscillations (see Figure 4—341
ﬁgure Supplement 2). The results of this analysis show that even in the absence of any asymmetry342
in the oscillations, CHO still outperforms existing methods in speciﬁcity. It further shows that the343
sensitivity increases with increasing SNR. Even though this analysis is based on synthetic sinusoidal344
oscillations, our results demonstrated that existing methods are susceptible to noise which results345
in the detection of spurious oscillations. However, as expected, both FOOOF and SPRiNT methods346
exhibited reasonable speciﬁcity when applied to sinusoidal signals.347
Focal localization of beta oscillations348
Beta oscillations occur within the 13–30 Hz band throughout various brain regions, including the349
motor cortex. In the motor cortex, beta oscillations are thought to be involved in motor plan-350
ning and execution. Studies have shown that beta oscillations increase and decrease in power351
during movement preparation and movement execution, respectively (Pfurtscheller and Da Silva,352
1999; Jenkinson and Brown, 2011; Doyle et al., 2005; Senkowski et al., 2006). In our empirical353
results based on the presented ECoG dataset, CHO found focal beta oscillations to occur within354
pre-motor and frontal cortex prior to the button response, as shown in Figure 5. These ﬁndings355
were consistent across subjects. Conventional methods found alpha and beta oscillations in the356
auditory cortex, while CHO found only select beta oscillations. This suggests that most of the beta357
oscillations detected by conventional methods within auditory cortex may be simply harmonics of358
the predominant asymmetric alpha oscillation. Along the same line, conventional methods found359
beta and low gamma oscillations in pre-motor and frontal areas, while CHO found predominantly360
beta oscillations. This suggests that low gamma oscillations detected by conventional methods are361
harmonics of beta oscillations.362
In the EEG results, CHO found focal visual alpha and motor beta oscillations, while the FOOOF363
found frontal and visual alpha and beta oscillations across broad scalp areas, as shown in Figure 6.364
In contrast to the ECoG results, neither CHO nor FOOOF auditory found alpha oscillations within the365
temporal areas. This is interesting as FOOOF exhibits a better sensitivity than CHO and suggests366
that auditory alpha rhythms may be diﬃcult to observe in EEG. Similar to the ECoG results, our367
analysis conﬁrmed that non-sinusoidal alpha and beta oscillations generate harmonic oscillations368
in both beta and low gamma in EEG. This shows that our CHO method, which has a high speciﬁcity,369
can detect focal motor beta oscillations.370
Harmonic oscillations in human hippocampus371
Recent studies suggest that the frequency range of hippocampal oscillations is wider than previ-372
ously assumed (<40 Hz in Cole and Voytek 2019, or 3–12 Hz in Li et al. 2022) and that it does not373
match the conventional frequency range of theta/alpha rhythms (Buzsaki, 2006 ). This realization374
stems from the recognition that neural oscillations are non-sinusoidal, and thus require a wide375
15 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
frequency band to be fully captured ( Cole and Voytek, 2019; Donoghue et al., 2022 ). Adopting a376
wider frequency band provides more frequency options in ﬁtting the non-sinusoidal shape of brain377
waves. The recognition of the need to expand the frequency band within oscillation analysis is not378
limited to the hippocampus. Our ECoG and EEG results show that harmonics can occur in any379
brain area and frequency band because neural oscillations are inherently non-sinusoidal. A recent380
study showed that the phase of wide-band oscillations could better predict neural ﬁring ( Davis381
et al., 2020).382
CHO can determine the fundamental frequency of non-sinusoidal oscillations when applied383
within a wide-band analysis, as shown in Figure 8E. Moreover, CHO provides onset/offset and the384
frequency range of an oscillation, allowing us to investigate non-sinusoidal features, such as the385
degree of asymmetry and amplitudes of trough/peak ( Cole and Voytek, 2019).386
Identifying onset/offset of neural oscillations and its application387
Although the frequency of neural oscillation has been extensively investigated, the onset/offset388
and duration of neural oscillations have remained elusive. Using CHO, the onset/offset, and du-389
ration of neural oscillations can be revealed, as shown in Figure 7 and Figure 9. Knowing the390
onset/offset and duration of a neural oscillation is essential for realizing closed-loop neuromod-391
ulation. This is because neuromodulation may be most eﬃcient when electrical stimulation is de-392
livered phase-locked to the underlying ongoing oscillation ( Chen et al., 2011 ; Cagnan et al., 2017 ,393
2019; Zanos et al., 2018 ; Shirinpour et al., 2020). For example, deep-brain stimulation in phase394
with ongoing oscillation can reduce the stimulation necessary to achieve the desired therapeutic395
effect (Cagnan et al., 2017, 2019). This improved eﬃciency in delivering the stimulation therapy re-396
duces power consumption and thus enhances the battery life of the implanted system ( Chen et al.,397
2011). Longer battery life means fewer battery changes (which require surgical procedures), or for398
rechargeable systems, fewer recharging sessions (which require the user’s attention). Realizing399
phase-locked neuromodulation requires detecting the duration of an ongoing oscillation with high400
speciﬁcity and delivering the electrical stimulation at a predicted oscillation phase. The detection401
and identiﬁcation with high speciﬁcity thus enable neuromodulation applications that depend on402
phase-locked electrical stimulation.403
Moreover, the temporal precision of CHO in detecting neural oscillations can improve the effec-404
tiveness of neurofeedback-based systems. For example, a neurofeedback system may provide tar-405
geted feedback on the magnitude of the user’s alpha oscillation to improve attention and in turn im-406
prove task performance. For this purpose, the system must detect the frequency, onset/offset, and407
duration of the user’s alpha oscillation with high speciﬁcity. High speciﬁcity requires distinguishing408
other oscillations and artifacts from true physiological alpha-band oscillations. The identiﬁcation409
of true neural oscillations with the high speciﬁcity of CHO thus enables targeted neurofeedback410
applications to enhance or restore task performance.411
Illuminating the when, where, what, why, how, and whom of neural oscillations412
In our study, we focused on the temporal dynamics (“when”), spatial distribution (“where”), and413
fundamental frequency (“what”) of neural oscillations. However, fully understanding the role of414
neural oscillations in cognition and behavior also requires investigating their underlying mecha-415
nisms (“how”), functional purpose (“why”), and pathologies (“whom”).416
Temporal Dynamics – the “when”417
CHO demonstrated high speciﬁcity in detecting the onset and offset of fundamental non-sinusoidal418
oscillations (see Figure 4E). Using CHO, our study revealed the temporal dynamics of oscillations419
within the temporal lobe in an auditory reaction-time task. We identiﬁed the onsets and offsets420
of 7 Hz oscillations and, thus, the boundaries in oscillatory activity between resting and task en-421
gagement. Our results show a rapid decrease in oscillatory activity for the duration of the auditory422
stimulus, followed by a rapid reemergence of the oscillatory activity following the cessation of the423
16 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
auditory stimulus (see Figure 7C and D). These results shed light on the temporal dynamics of neu-424
ral oscillatory activity in cognitive processes and how the brain adapts to environmental stimuli.425
Spatial Distribution – the “where”426
CHO revealed the spatial distribution of neural oscillations in EEG, SEEG, and ECoG recordings. The427
spatial distribution of fundamental neural oscillations, and their absence during task engagement,428
can reveal underlying shared functional organization. CHO can be applied to a wide range of neu-429
roimaging techniques such as EEG, MEG, ECoG, and SEEG to elucidate the involvement of different430
brain regions in various cognitive functions. For example, using CHO, our study found focal speciﬁc431
alpha oscillations over occipital (visual) cortex in EEG and focal beta oscillations over parietal (mo-432
tor) cortex in ECoG. These results demonstrate the utility of CHO in precisely mapping the spatial433
distribution of neural oscillations across the brain, and in revealing shared functional organization434
of brain networks.435
Fundamental Frequency – the “what”436
CHO revealed the fundamental frequencies of asymmetric neural oscillations recorded from the437
scalp, auditory cortex, motor cortex, Broca’s area, and hippocampus. Distinct brain states can be438
identiﬁed based on the fundamental frequency of their underlying neural oscillation. CHO showed439
high speciﬁcity in determining the fundamental frequency of synthetic non-sinusoidal oscillations440
(see Figure 4B). When applied to ECoG and SEEG signals, CHO revealed distinct fundamental fre-441
quencies of oscillations found within auditory cortex, motor cortex, Broca’s area, and hippocam-442
pus (see Figure 9). CHO can be applied in real time to detect the fundamental frequency and the443
onset/offset of neural oscillations. Characterizing neural oscillations in real time can make tran-444
sitions in brain states observable to the investigator. For example, investigators can characterize445
brain dynamics during wakefulness, sleep, or speciﬁc cognitive tasks by tracking changes in oscilla-446
tory activity during different behavioral states. This information provides insights into the brain’s447
adaptability and ﬂexibility in response to internal and external cues and could inform closed-loop448
neuromodulation.449
Underlying Mechanisms – the “how”450
Accurate detection of neural oscillations aids in deciphering the underlying mechanisms governing451
their generation and synchronization. In our study, we focused on determining the temporal dy-452
namics, spatial distribution, and fundamental frequency of neural oscillations. The results of our453
study, and more speciﬁcally the CHO method itself, provide a methodological foundation to sys-454
tematically study oscillatory connectivity and traveling oscillations throughout cortical layers and455
brain regions to create insights into unraveling the generating mechanism of neural oscillations.456
The information gained from such studies could create a better understanding of neural circuitry457
at the network level and could inform computational models that help reﬁne our knowledge of the458
complex mechanisms underlying brain function.459
Functional Purpose – the “why”460
Neural oscillation detection plays a crucial role in uncovering the functional signiﬁcance of oscilla-461
tory activity. In our study, CHO detected focal alpha oscillations over occipital (visual) cortex in EEG462
and focal beta oscillations over parietal (motor) cortex in ECoG during the pre-stimulus period of463
an auditory reaction-time task (see Figure 5 and Figure 6). The presence of these oscillations dur-464
ing the pre-stimulus period implicates visual-alpha and motor-beta oscillations in inhibition. We465
found the same inhibitory oscillatory phenomenon over the auditory cortex, however, with a fun-466
damental frequency of 7 Hz, indicating functional independence between inhibitory oscillations467
found in visual, motor, and auditory cortex (see Figure 7C and D). The approach presented in this468
study could be expanded to studying attention, memory, decision-making, and more by correlating469
neural oscillations with speciﬁc cognitive processes. Further, applying cross-frequency and phase-470
amplitude coupling analysis to oscillations detected by CHO could illuminate the role of neural471
17 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
oscillations in facilitating information processing and communication between brain regions.472
Pathologies – the “whom”473
Detecting and characterizing neural oscillations has signiﬁcant implications for the study of neu-474
rological and psychiatric disorders. For example, recent studies reported that patients affected475
by severe Parkinson’s disease exhibited more asymmetry between peak and trough amplitudes in476
beta oscillations (Cole et al., 2017; Jackson et al., 2019 ). The high speciﬁcity demonstrated by CHO477
in detecting asymmetric neural oscillations could beneﬁt the investigation of neural pathologies.478
Speciﬁcally, CHO could improve the quality of asymmetry measurements by providing onset/offset479
detection of the beta oscillations with high speciﬁcity. Abnormalities in neural oscillations are of-480
ten associated with various pathologies. Detecting and characterizing aberrant oscillatory patterns481
could lead to identifying biomarkers for speciﬁc disorders and insights into their underlying mech-482
anisms. These advancements could aid the development of targeted therapies and treatments for483
these conditions.484
Illuminating neural oscillations485
Overall, developing a reliable neural oscillation detection method is crucial for advancing our un-486
derstanding of brain function and cognition. The presented CHO method opens up new avenues487
of research by contributing to the investigation of temporal dynamics, spatial distribution, brain488
states, underlying mechanisms, functional purpose, and pathologies of neural oscillations. Ulti-489
mately, a comprehensive understanding of neural oscillations will deepen our knowledge of the490
brain’s complexity and pave the way for innovative approaches to treating neurological and psy-491
chiatric disorders.492
Limitations493
The results of this study show that our CHO method favors speciﬁcity over sensitivity when SNR494
is low. More speciﬁcally, CHO exhibited a low sensitivity due to the high false-negative rate in a495
low-SNR environment. This means that even though there are oscillations present in the recorded496
signals, CHO cannot detect them when they are drowned in noise. To investigate whether this is an497
issue in real-world applications, we determined the averaged SNR of alpha oscillations in EEG (-7 dB)498
and ECoG (-6 dB). Based on our evaluation of synthetic data, we found that at these physiologically-499
motivated SNR levels, CHO can detect 50–60% of all true oscillations. This sensitivity could be500
further improved by averaging across spatially correlated locations, e.g., within the hippocampus.501
One potential approach to reducing the dependency of sensitivity on SNR is to apply a wavelet502
transform in the estimation of the time-frequency map of the signal. Wavelet transform can better503
capture short cycles of oscillations. Currently, CHO uses a Hilbert transform method rather than504
Wavelet or short-time fast Fourier transform (STFFT) because it is easy to implement in MATLAB and505
provides better control over the spectral shape (i.e., better accuracy in detecting peak frequency506
of oscillations, Cohen 2014). Despite the theoretical advantages of wavelet over Hilbert transform,507
in developing our CHO method, we found no signiﬁcant differences when we used different ap-508
proaches to estimate the time-frequency map. This ﬁnding is further supported by a comparative509
study shown by Bruns in 2004. However, because our CHO method is modular, the FFT-based time-510
frequency analysis can be replaced with more sophisticated time-frequency estimation methods511
to improve the sensitivity of neural oscillation detection. Speciﬁcally, a state-space model ( Mat-512
suda and Komaki, 2017 ; Beck et al., 2022; Brady and Bardouille, 2022 ; He et al., 2023 ) or empirical513
mode decomposition (EMD, Fabus et al. 2022; Quinn et al. 2021) may improve the estimation of the514
auto-correlation of the harmonic structure underlying non-sinusoidal oscillations. Furthermore, a515
Gabor transform or matching pursuit-based approach may improve the onset/offset detection of516
short burst-like neural oscillations (Kuś et al., 2013 ; Morales and Bowers, 2022 ).517
Another avenue to improve the sensitivity of CHO is to modify the third criterion to better distin-518
guish neural oscillations from background noise. When we performed each detection step within519
18 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
CHO, as shown in Figure 3, we captured oscillations in a low-SNR situation. However, applying520
the third criterion rejected many possible bounding boxes. Thus, developing a better conceptual521
framework to reject harmonic peaks in the spectral domain may decrease the false-negative rate522
and, in turn, increase the sensitivity in low-SNR situations.523
Another limitation of this study is that it does not assess the harmonic structure of neural os-524
cillations. Thus, CHO cannot distinguish between oscillations that have the same fundamental fre-525
quency but differ in their non-sinusoidal properties. This limitation stems from the objective of this526
study, which is to identify the fundamental frequency of non-sinusoidal neural oscillations. Over-527
coming this limitation requires further studies to improve CHO to distinguish between different528
non-sinusoidal properties of pathological neural oscillations. The data that is necessary for these529
further studies could be obtained from the wide range of studies that have linked the harmonic530
structures in the neural oscillations to various cognitive functions (van Dijk et al., 2010; Schalk,531
2015; Mazaheri and Jensen, 2008 ) and neural disorders (Cole et al., 2017; Jackson et al., 2019 ; Hu532
et al., 2023). For example, Cole and Voytek 2019 showed that a harmonic structure of beta oscil-533
lations can explain the degree of Parkinson’s disease, and Hu et al. 2023 showed the number of534
harmonic peaks can localize the seizure onset zone.535
Conclusions536
Neural oscillations are thought to play an important role in coordinating neural activity across537
different brain regions, allowing for the integration of sensory information, the control of motor538
movements, and the maintenance of cognitive functions. Thus, better methods to detect and char-539
acterize neural oscillations, especially those that are asymmetric, can greatly impact neuroscience.540
In this study, we present Cyclic Homogeneous Oscillation (CHO) as a method to reveal the “when”,541
the “where”, and the “what” of neural oscillations. With this method, we overcome the confounding542
effect of detecting spurious oscillations that result from harmonics of the non-sinusoidal neural os-543
cillations (Donoghue et al., 2022). In our study, we demonstrate that solving this problem yields sci-544
entiﬁc insights into local beta oscillations in pre-motor areas, the onset/offset of oscillations in the545
time domain, and the fundamental frequency of hippocampal oscillations. These results demon-546
strate the potential for CHO to support closed-loop neuromodulation (brain-computer interfaces547
and neurofeedback) and neural oscillation detection systems to implement various neurological548
diagnostic and therapeutic systems and methods.549
Methods and Materials550
Electrophysiological data551
Eight human subjects implanted with ECoG electrodes (x1–x8, 4 females, average age = 41 ±14)552
participated in an auditory reaction time task at the Albany Medical Center in Albany, New York.553
The subjects were mentally and physically capable of participating in our study (average IQ = 96±18,554
range 75–120, Wechsler 1997). All subjects were patients with intractable epilepsy who underwent555
temporary placement of subdural electrode arrays to localize seizure foci before surgical resection.556
The implanted electrode grids were approved for human use (Ad-Tech Medical Corp., Racine,557
WI; and PMT Corp., Chanhassen, MN). The platinum-iridium electrodes were 4 mm in diameter558
(2.3 mm exposed), spaced 10 mm center-to-center, and embedded in silicone. The electrode grids559
were implanted in the left hemisphere for seven subjects (x1, x3, x6, and x7) and the right hemi-560
sphere for ﬁve subjects (x2, x4, x5, and x8). Following the placement of the subdural grids, each561
subject had postoperative anterior-posterior and lateral radiographs and computer tomography562
(CT) scans to verify grid location. These CT images, in conjunction with magnetic resonance imag-563
ing (MRI), were used to construct three-dimensional subject-speciﬁc cortical models and derive the564
electrode locations (Coon et al., 2016 ).565
A further seven healthy human subjects (y1–y7, all males, average age = 27 ±3.6) served as a566
control group for which we recorded EEG while performing the same auditory reaction time task.567
19 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
These subjects were ﬁtted with an elastic cap (Electro-cap International, Blom and Anneveldt 1982)568
with tin (Polich and Lawson, 1985) scalp electrodes in 64 positions according to the modiﬁed 10-20569
system (Acharya et al., 2016 ).570
In addition, six human subjects implanted with ECoG electrodes (ze1–ze6, 1 female, mean age571
46, range between 31 and 69) participated in resting state recording at the Albany Medical Center in572
Albany, New York. All six subjects had extensive electrode coverage over the lateral STG. Patients573
provided informed consent to participate in the study, and additional verbal consent was given574
prior to each testing session. The Institutional Review Board at Albany Medical Center approved575
the experimental protocol. Electrodes were comprised of platinum-iridium and spaced 3-10mm576
(PMT Corp., Chanhassen, MN).577
Lastly, six human subjects implanted with SEEG electrodes (zs1–zs6, three females, average578
age = 46±16.6) participated in resting state recordings at the Barnes Jewish Hospital in St. Louis,579
Missouri. All subjects were patients with intractable epilepsy who underwent temporary placement580
of subdural electrodes to localize seizure foci prior to surgical resection. All subjects provided581
informed consent for participating in the study, which was approved by the Institutional Review582
Board of Washington University School of Medicine in St. Louis.583
The implanted SEEG electrodes were approved for human use (Ad-Tech Medical Corp., Racine,584
WI; and PMT Corp., Chanhassen, MN). The platinum-iridium electrodes were 2 mm in length (0.8 mm585
diameter) and spaced 3.5–5 mm center-to-center. Following the placement of the stereo EEG elec-586
trodes, each subject had postoperative anterior-posterior and lateral radiographs and computer587
tomography (CT) scans to verify electrode location. These postoperative CT images, in conjunction588
with preoperative magnetic resonance imaging (MRI), were used to construct three-dimensional589
subject-speciﬁc cortical models and derive the electrode locations (Coon et al., 2016 ).590
Data collection591
We recorded EEG, ECoG, and SEEG signals from the subjects at their bedside using the general592
purpose Brain-Computer Interface (BCI2000) software ( Schalk et al., 2004), interfaced with eight593
16-channel g.USBamp biosignal acquisition devices (for EEG), one 256-channel g.HIamp biosignal594
acquisition device (g.tec., Graz, Austria, for ECoG), or one Nihon Kohden JE-120A long-term record-595
ing system (Nihon Kohden, Tokyo, Japan, for SEEG) to amplify, digitize (sampling rate 1,200 Hz for596
EEG and ECoG and 2,000 Hz for SEEG) and store the signals. To ensure safe clinical monitoring of597
ECoG signals during the experimental tasks, a connector split the cables connected to the patients598
into a subset connected to the clinical monitoring system and a subset connected to the ampliﬁers.599
Task600
The subjects performed an auditory reaction task, responding with a button press to a salient601
1 kHz tone. For their response, the subjects used their thumb contralateral to their ECoG implant.602
In total, the subjects performed between 134 and 580 trials. Throughout each trial, the subjects603
were ﬁrst required to ﬁxate and gaze at the screen in front of them. Next, a visual cue indicated604
the trial’s start, followed by a random 1–3 s pre-stimulus interval and, subsequently, the auditory605
stimulus. The stimulus was terminated by the subject’s button press or after a 2-s time out, after606
which the subject received feedback about his/her reaction time. This feedback motivated the607
subjects to respond as quickly as possible to the stimulus. We penalized subjects with a warning608
tone to prevent false starts if they responded too fast (i.e., less than 100 ms after stimulus onset).609
We excluded false-start trials from our analysis. We were interested in this task’s auditory and610
motor responses in this study. This required deﬁning the onset of these two responses. We time-611
locked our analysis of the auditory response to the onset of the auditory stimulus (as measured by612
the voltage between the sound port on the PC and the loudspeaker). For the motor response, we613
time-locked our analysis to the time when the push button was pressed. To ensure the temporal614
accuracy of these two onset markers, we sampled them simultaneously with the EEG/ECoG signals615
using dedicated inputs in our biosignal acquisition systems. We deﬁned baseline and task periods616
20 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
for the auditory and motor response. Speciﬁcally, we used the 0.5-s period prior to the stimulus617
onset as the baseline for the auditory response and the 1-s to 0.5-s period prior to the button press618
as the baseline for the motor response. Similarly, we used the 1-s period after stimulus onset as619
the task period for the auditory response and the period from 0.5-s before to 0.5-s after the button620
press as the task period for the motor task.621
Data pre-processing622
As our ampliﬁers acquired raw, unﬁltered EEG/ECoG/SEEG signals, we removed any offset from623
our signals using a 2nd-order Butterworth highpass ﬁlter at 0.05 Hz. Next, we removed any com-624
mon noise using a common median reference ﬁlter ( Liu et al., 2015). To create the common-mode625
reference, we excluded signals that exhibited an excessive 60 Hz line noise level (i.e., ten times626
the median absolute deviation). To improve the signal-to-noise ratio of our recordings and to re-627
duce the computational complexity of our subsequent analysis, we downsampled our signals from628
1200 Hz or 2000 Hz to 400 Hz or 500 Hz, respectively, using MATLABs “resample” function, which629
uses a polyphase antialiasing ﬁlter to resample the signal at the uniform sample rate.630
Phase-phase coupling631
To demonstrate phase-locking, as illustrated between theta and beta oscillations in Figure 1E and632
Figure 1 K, we utilized the n:m phase-phase coupling method described in Belluscio et al. 2012 .633
Speciﬁcally, we calculated the “mean radial distance”:𝑅𝑛∶𝑚 = ‖ 1
𝑁
∑𝑁
𝑗=1 𝑒𝑖Δ𝜙𝑛𝑚(𝑡𝑗 )‖, where 𝑗 indexes the634
samples in time, and 𝑁 represents the number of samples (epoch length in seconds × sampling635
frequency in Hz). 𝑅𝑛∶𝑚 equals 1 when Δ𝜙𝑛𝑚(𝑡𝑗) is constant for all time samples 𝑡𝑗, and 0 when Δ𝜙𝑛𝑚 is636
uniformly distributed. Of note, Δ𝜙𝑛𝑚(𝑡𝑗) equals 𝑛𝜙𝑓1 (𝑡𝑗) - 𝑚𝜙𝑓2 (𝑡𝑗), with 𝑓1 and 𝑓2 being two different637
frequency bands.638
A novel oscillation detection method639
We propose a novel method based on principle criteria to identify neural oscillations’ when, where,640
and what. The principle criteria are as follows: 1. Oscillations (peaks over 1/f noise) must be present641
in the time and frequency domain. 2. Oscillations must exhibit at least two full cycles. 3. The pe-642
riodicity of an oscillation is the fundamental frequency of the oscillation. The procedural steps643
of CHO adhere to these principle criteria, as shown in Figure 3 and Algorithm 1. First, we apply644
a time-frequency analysis to determine power changes for each frequency component over time.645
To measure the signiﬁcant spectral power increase over the time domain, we use the 1/f ﬁtting646
technique as the principal threshold. In other words, the proposed method only considers those647
oscillations that emerge above the underlying 1/f noise. Thus, any oscillation with smaller power648
than 1/f noise is not considered to be an oscillation. To accomplish this, we subtract the underly-649
ing 1/f noise within the time-frequency domain. Speciﬁcally, we divide the time domain into four650
periods and estimate the minimum 1/f aperiodic ﬁt across these periods (see Line 5 in Algorithm 1).651
After the subtraction of the underlying 1/f noise, we calculate the averaged power difference be-652
tween the signal and the 1/f noise (named sigma). If the spectral power exceeds two times sigma,653
we consider the oscillation to exhibit signiﬁcant power above the 1/f noise (see Line 12 in Algorithm654
1). Next, we cluster time points with signiﬁcant power over 1/f noise to generate initial bounding655
boxes as shown in Figure 3 A; this idea is adopted from a previous study ( Neymotin et al., 2022 )656
(see Lines 10–20 in Algorithm 1).657
Next, as the second principle criterion, we only consider those oscillations that exhibit at least658
two full cycles. This restriction allows CHO to distinguish oscillations from confounding event-659
related potentials (ERPs) or evoked potentials (EPs). In general, the frequency characteristics of660
those potentials often overlap with neural oscillations (e.g., theta power of ERPs and theta power661
of theta rhythm). However, ERPs or EPs never exhibit more than two cycles (see Line 23 in Algo-662
rithm 1). Therefore, we reject those bounding boxes that exhibit less than two cycles. An example663
is shown in Figure 3B.664
21 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Algorithm 1 CHO detection method
1: procedure CHO
2: Let 𝑥(𝑡) denote a signal at time point 𝑡 ∈ 𝑇 .
3: Remove 1/f noise in time-frequency map :
4: 𝑃 (𝑡, 𝑓) ← log power of 𝑥(𝑡) at frequency 𝑓 ∈ 𝐹
5: 𝑇1, ..., 𝑇𝑁 ∈ 𝑇 ← segment 𝑇 into 𝑁 windows
6: 𝑏𝑖, 𝑒𝑖 ← offset 𝑏 and exponent 𝑒 of 1/f ﬁtting from 𝑃 (𝑇𝑖∈𝑇 , 𝐹 )
7: 𝑡𝑚𝑖𝑛 ← 𝑎𝑟𝑔𝑚𝑖𝑛𝑖𝑏𝑖
8: 𝐿𝑚𝑖𝑛 ← 𝑏(𝑡𝑚𝑖𝑛) − 𝑙𝑜𝑔(𝐹 𝑒𝑚𝑖𝑛 )
9: 𝑃 ′(𝑡, 𝐹 ) ← 𝑃 (𝑡, 𝐹 ) − 𝐿𝑚𝑖𝑛
10: Generate initial bounding boxes:
11: 𝜎(𝑓 ) ← standard deviation of 𝑃 ′(𝑡, 𝑓) over 𝑡
12: 𝐶𝑘∈𝐾 ← cluster the data points in 𝑃 ′(𝑡, 𝑓) if 𝑃 ′(𝑡, 𝑓) > 2𝜎(𝑓 )
13: 𝐵𝑘∈𝐾 ← generate 𝐾 initial bounding boxes
14: 𝐵𝑘.𝑐𝑓 ← center frequency of the bounding box
15: 𝐵𝑘.𝑐𝑡 ← center time point of the bounding box
16: 𝐵𝑘.𝑝𝑜𝑤𝑒𝑟 ← peak power within the bounding box
17: 𝐵𝑘.𝑚𝑖𝑛𝑓 ← lower bound frequency of the bounding box
18: 𝐵𝑘.𝑚𝑎𝑥𝑓 ← upper bound frequency of the bounding box
19: 𝐵𝑘.𝑠𝑡𝑎𝑟𝑡 ← onset time of the bounding box
20: 𝐵𝑘.𝑠𝑡𝑜𝑝 ← offset time of the bounding box
21: Reject boxes have short cycles :
22: 𝐶𝑦𝑐𝑙𝑒 𝑘∈𝐾 ← 𝐵𝑘.𝑐𝑓 × (𝐵𝑘.𝑠𝑡𝑜𝑝 − 𝐵𝑘.𝑠𝑡𝑎𝑟𝑡)
23: 𝐵𝑚∈𝑀 ← reject 𝐵𝑘 if 𝐶𝑦𝑐𝑙𝑒 𝑘 < 2
24: Reject boxes if its periodicity of raw signal and center frequency are different :
25: 𝐴𝑚(𝑙) ← auto-correlation of the raw signal 𝑥(𝑡′), 𝑡′ ∈ 𝑇 ′,where 𝑇 ′ = 𝐵𝑚.𝑠𝑡𝑎𝑟𝑡, ..., 𝐵𝑚.𝑠𝑡𝑜𝑝
26: 𝑃 𝑝𝑒𝑎𝑘𝑠𝑚, 𝑁𝑝𝑒𝑎𝑘𝑠𝑚 ← Sets of positive and negative peaks in 𝐴𝑚(𝑙)
27: 𝑃 𝑖𝑛𝑡𝑒𝑟𝑣𝑎𝑙𝑚, 𝑁𝑖𝑛𝑡𝑒𝑟𝑣𝑎𝑙𝑚 ← Intervals of 𝑃 𝑒𝑎𝑘𝑠𝑚 and 𝑁𝑝𝑒𝑎𝑘𝑠 𝑚, respectively
28: 𝑃 𝑒𝑟𝑖𝑜𝑑𝑖𝑐𝑖𝑡𝑦𝑚 ← Periodicity (Hz) of 𝑃 𝑖𝑛𝑡𝑒𝑟𝑣𝑎𝑙𝑚
29: 𝑃 𝑠𝑖𝑚𝑖𝑙𝑎𝑟𝑖𝑡𝑦𝑚, 𝑁𝑠𝑖𝑚𝑖𝑙𝑎𝑟𝑖𝑡𝑦 𝑚 ← Similarity (%) of 𝑃 𝑖𝑛𝑡𝑒𝑟𝑣𝑎𝑙𝑚 and 𝑁𝑖𝑛𝑡𝑒𝑟𝑣𝑎𝑙 𝑚, respectively
30: 𝐵ℎ∈𝐻 ← Accept 𝐵𝑚 if 𝐵𝑚.𝑚𝑖𝑛𝑓 < 𝑃 𝑒𝑟𝑖𝑜𝑑𝑖𝑐𝑖𝑡𝑦 𝑚 < 𝐵 𝑚.𝑚𝑎𝑥𝑓 and 𝑃 𝑠𝑖𝑚𝑖𝑙𝑎𝑟𝑖𝑡𝑦𝑚 < 30%.
31: 𝐵𝑗∈𝐽 ← merge remained boxes if t’ overlaps > 75% each other
32: Return 𝐵𝑗∈𝐽
22 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Lastly, we calculate the periodicity of an oscillation using an autocorrelation analysis to deter-665
mine the fundamental frequency of the oscillation. Non-sinusoidal signals are known to exhibit666
harmonics in the frequency domain, signiﬁcantly increasing the false-positive detection rate —the667
confounding factor addressed by CHO’s third criterion. The power spectrum of the non-sinusoidal668
oscillations has additional harmonic peaks over 1/f noise, even though the periodicity of the signal669
does not match the harmonic peak frequency. Therefore, the positive peaks of the oscillation’s670
autocorrelation represent the oscillation’s periodicity and fundamental frequency (see Figure 2).671
As shown in Figure 3 C, the center frequency of the bounding box is 24 Hz, but the periodicity of672
the raw signal within the bounding box does not match 24 Hz. Consequently, this bounding box673
will be rejected (see Line 30 in Algorithm 1). Finally, the method merges those remaining bounding674
boxes that neighbor each other in the frequency domain and that overlap more than 75% in time675
(Neymotin et al., 2022 ).676
The MATLAB code that implements CHO and sample data is available on GitHub ( https://github.677
com/neurotechcenter/CHO).678
Tradeoffs in adjusting the hyper-parameters that govern the detection in CHO679
The ability of CHO to detect neural oscillations and determine their fundamental frequency is gov-680
erned by four principal hyper-parameters. Adjusting these parameters requires understanding681
their effect on the sensitivity and speciﬁcity in the detection of neural oscillations.682
The ﬁrst hyper-parameter is the number of time windows (N in Line 5 in Algorithm 1), that is683
used to estimate the 1/f noise. In our performance assessment of CHO, we used four windows,684
resulting in estimation periods of 250 ms in duration for each 1/f spectrum. A higher number of685
time windows results in smaller estimation periods and thus minimizes the likelihood of observing686
multiple neural oscillations within this time window, which otherwise could confound the 1/f esti-687
mation. However, a higher number of time windows and, thus, smaller time estimation periods688
may lead to unstable 1/f estimates.689
The second hyper-parameter deﬁnes the minimum number of cycles of a neural oscillation to690
be detected by CHO (see Line 23 in Algorithm 1). In our study, we speciﬁed this parameter to be two691
cycles. Increasing the number of cycles increases speciﬁcity, as it will reject spurious oscillations.692
However, increasing the number also reduces sensitivity as it will reject short oscillations.693
The third hyper-parameter is the signiﬁcance threshold that selects positive peaks within the694
auto-correlation of the signal. The magnitude of the peaks in the auto-correlation indicates the695
periodicity of the oscillations (see Line 26 in Algorithm 1). Referred to as “NumSTD,” this parameter696
denotes the number of standard errors that a positive peak has to exceed to be selected to be a697
true oscillation. For this study, we set the “NumSTD” value to 1. Increasing the “NumSTD” value698
increases speciﬁcity in the detection as it reduces the detection of spurious peaks in the auto-699
correlation. However, increasing the “NumSTD” value also decreases the sensitivity in the detection700
of neural oscillations with varying instantaneous oscillatory frequencies.701
The fourth hyper-parameter is the percentage of overlap between two bounding boxes that trig-702
ger their merger (see Line 31 in Algorithm 1). In our study, we set this parameter to 75% overlap. In-703
creasing this threshold yields more fragmentation in the detection of oscillations, while decreasing704
this threshold may reduce the accuracy in determining the onset and offset of neural oscillations.705
Validation on synthetic non-sinusoidal oscillations706
While empirical physiological signals are most appropriate for validating our method, they gen-707
erally lack the necessary ground truth to characterize neural oscillation with sinusoidal or non-708
sinusoidal properties. To overcome this limitation, we ﬁrst validated CHO on synthetic non-sinusoidal709
oscillatory bursts (2.5 cycles, 1–3 seconds long) convolved with 1/f noise to test the performance710
of the proposed method.711
As shown in Figure 4, we generated ﬁve second-long periods comprised of 1/f noise (i.e., pink712
noise). We added non-sinusoidal oscillations with different amplitudes and lengths. The ampli-713
23 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
tudes of non-sinusoidal oscillations vary between 5 and 20 microvolts, while the pink noise remains714
at 10 microvolts in amplitude. The signal-to-noise (SNR) was calculated by the snr() function in the715
Signal Processing Toolbox of MATLAB, which determines the signal-to-noise ratio in decibels of the716
non-sinusoidal burst by computing the ratio between summed squared magnitudes of the oscil-717
lation and the pink noise, respectively. We simulated ten iterations for each amplitude. For each718
iteration, we tested four different lengths of non-sinusoidal oscillations (one cycle, two-and-a-half719
cycles, one second, and three seconds long).720
We generated non-sinusoidal oscillations by introducing asymmetry between the trough and721
peak periods of sinusoidal waves. To generate this asymmetric nature of an oscillation, we applied722
a 9:1 ratio between trough and peak amplitudes, as shown in an example of Figure 4A. To smooth723
the onset and offset of the non-sinusoidal oscillations, we used Tukey (tapered cosine) window724
function with a 0.40 ratio for the taper section ( Bloomﬁeld, 2004). Of note, the smaller the Turkey725
ratio within the taper section, the higher the occurrence of high-frequency artifacts.726
To evaluate the performance of CHO, we calculated the speciﬁcity and sensitivity of CHO in727
detecting non-sinusoidal oscillations. High speciﬁcity depends on high true-negative and low false-728
positive detection rates. In contrast, high sensitivity depends on high true-positive and low false-729
negative detection rates. In this simulation, we expected harmonic oscillations to increase the false-730
positive detection rate, and one-cycled oscillations to decrease the true-negative detection rate731
within conventional methods. Thus, harmonic oscillations and one-cycled oscillations decrease732
the speciﬁcity, not sensitivity.733
For evaluating the performance of each method in determining the fundamental frequency of734
the oscillations, we deﬁned an accurate detection as one that exhibited a difference between the735
ground truth peak frequency and detected frequency of less than 1.5 Hz. Furthermore, to evaluate736
the performance of each method in detecting the onset/offset of the oscillations, we calculated the737
correlation between the envelope of the ground truth oscillation and the detected oscillation. We738
deﬁned those onset/offset detections as accurate if the correlation was positive and the p-value739
was smaller than 0.05.740
Acknowledgments741
This work was supported by the National Institutes of Health (NIH) grants R01-MH120194, R01-742
EB026439, U24-NS109103, U01-NS108916, U01-NS128612, P41-EB018783, the McDonnell Center743
for Systems Neuroscience and Fondazione Neurone.744
Authors’ Contributions745
Conceptualization: HC, PB. Methodology: HC, MA, JTW, PB. Data Curation: PB. Formal analysis: HC.746
Visualization: HC, MA. Funding acquisition: JTW, PB. Writing – original draft: HC, PB. Writing – review747
& editing: HC, MA, JTW, PB. All authors read and approved the ﬁnal version of the manuscript.748
Competing Interests749
One U.S. patent (Provisional Application Serial No.63/326,257) related to systems and methods750
for detection of neurophysiological signal oscillations described in this manuscript was ﬁled on751
March 31, 2022. The inventors/contributors of this patent involve some of the manuscript authors,752
including HC, MA, JTW, PB.753
Data Availability754
Datasets may be provided to interested researchers upon reasonable request to the correspond-755
ing author.756
24 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Code Availability757
The Matlab code and sample data used for CHO are available at https://github.com/neurotechcenter/758
CHO.759
References760
Acharya JN, Hani AJ, Cheek J, Thirumala P, Tsuchida TN. American clinical neurophysiology society guideline 2:761
guidelines for standard electrode position nomenclature. The Neurodiagnostic Journal. 2016; 56(4):245–252.762
doi: https://doi.org/10.1080/21646821.2016.1245558.763
Adamek M, Swift JR, Brunner P. VERA - A Versatile Electrode Localization Framework. Zenodo. 2022; (Version764
1.0.0) [Computer software]. doi: https://doi.org/10.5281/zenodo.7486842.765
Beck AM, He M, Gutierrez R, Purdon PL. An iterative search algorithm to identify oscillatory dynamics in neu-766
rophysiological time series. bioRxiv. 2022; p. 2022–10. doi: https://doi.org/10.1101/2022.10.30.514422.767
Belluscio MA, Mizuseki K, Schmidt R, Kempter R, Buzsáki G. Cross-frequency phase–phase coupling between768
theta and gamma oscillations in the hippocampus. Journal of Neuroscience. 2012; 32(2):423–435. doi:769
https://doi.org/10.1523/JNEUROSCI.4122-11.2012.770
Blom J, Anneveldt M. An electrode cap tested. Electroencephalography and Clinical Neurophysiology. 1982;771
54(5):591–594. doi: https://doi.org/10.1016/0013-4694(82)90046-3.772
Bloomﬁeld P. Fourier analysis of time series: an introduction. John Wiley & Sons; 2004.773
Brady B , Bardouille T. Periodic/Aperiodic parameterization of transient oscillations (PAPTO)–Implications for774
healthy ageing. NeuroImage. 2022; 251:118974. doi: https://doi.org/10.1016/j.neuroimage.2022.118974.775
Bruns A. Fourier-, Hilbert-and wavelet-based signal analysis: are they really different approaches? Journal of776
Neuroscience Methods. 2004; 137(2):321–332. doi: https://doi.org/10.1016/j.jneumeth.2004.03.002.777
Buzsaki G . Rhythms of the Brain. Oxford University Press; 2006. doi:778
https://doi.org/10.1093/acprof:oso/9780195301069.001.0001.779
Buzsaki G , Draguhn A. Neuronal oscillations in cortical networks. Science. 2004; 304(5679):1926–1929. doi:780
https://doi.org/10.1126/science.1099745.781
Cagnan H, Denison T, McIntyre C, Brown P. Emerging technologies for improved deep brain stimulation. Nature782
Biotechnology. 2019; 37(9):1024–1033. doi: https://doi.org/10.1038/s41587-019-0244-6.783
Cagnan H, Pedrosa D, Little S, Pogosyan A, Cheeran B, Aziz T, Green A, Fitzgerald J, Foltynie T, Limousin P,784
et al. Stimulating at the right time: phase-speciﬁc deep brain stimulation. Brain. 2017; 140(1):132–145. doi:785
https://doi.org/10.1093/brain/aww286.786
Canolty RT, Edwards E, Dalal SS, Soltani M, Nagarajan SS, Kirsch HE, Berger MS, Barbaro NM, Knight RT. High787
gamma power is phase-locked to theta oscillations in human neocortex. Science. 2006; 313(5793):1626–1628.788
doi: https://doi.org/10.1126/science.1128115.789
Caplan JB, Madsen JR, Schulze-Bonhage A, Aschenbrenner-Scheibe R, Newman EL, Kahana MJ. Human 𝜃 oscil-790
lations related to sensorimotor integration and spatial learning. Journal of Neuroscience. 2003; 23(11):4726–791
4736. doi: https://doi.org/10.1523/JNEUROSCI.23-11-04726.2003.792
Chen LL, Madhavan R, Rapoport BI, Anderson WS. Real-time brain oscillation detection and phase-locked793
stimulation using autoregressive spectral estimation and time-series forward prediction. IEEE Transactions794
on Biomedical Engineering. 2011; 60(3):753–762. doi: https://doi.org/10.1109/TBME.2011.2109715.795
de Cheveigné A , Nelken I. Filters: when, why, and how (not) to use them. Neuron. 2019; 102(2):280–293. doi:796
https://doi.org/10.1016/j.neuron.2019.02.039.797
Cohen MX . Analyzing neural time series data: theory and practice. MIT press; 2014. doi:798
https://doi.org/10.7551/mitpress/9609.001.0001.799
Cole S, Voytek B. Cycle-by-cycle analysis of neural oscillations. Journal of Neurophysiology. 2019; 122(2):849–800
861. doi: https://doi.org/10.1152/jn.00273.2019.801
25 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Cole SR , van der Meij R, Peterson EJ, de Hemptinne C, Starr PA, Voytek B. Nonsinusoidal beta oscillations802
reﬂect cortical pathophysiology in Parkinson’s disease. Journal of Neuroscience. 2017; 37(18):4830–4840.803
doi: https://doi.org/10.1523/JNEUROSCI.2208-16.2017.804
Coon WG , Gunduz A, Brunner P, Ritaccio AL, Pesaran B, Schalk G. Oscillatory phase modulates805
the timing of neuronal activations and resulting behavior. NeuroImage. 2016; 133:294–301. doi:806
https://doi.org/10.1016/j.neuroimage.2016.02.080.807
Davis ZW , Muller L, Martinez-Trujillo J, Sejnowski T, Reynolds JH. Spontaneous travelling cortical waves gate808
perception in behaving primates. Nature. 2020; 587(7834):432–436. doi: https://doi.org/10.1038/s41586-809
020-2802-y.810
van Dijk H, van der Werf J, Mazaheri A, Medendorp WP, Jensen O. Modulations in oscillatory activity with811
amplitude asymmetry can produce cognitively relevant event-related responses. Proceedings of the National812
Academy of Sciences. 2010; 107(2):900–905. doi: https://doi.org/10.1073/pnas.0908821107.813
Donoghue T, Haller M, Peterson EJ, Varma P, Sebastian P, Gao R, Noto T, Lara AH, Wallis JD, Knight RT, et al.814
Parameterizing neural power spectra into periodic and aperiodic components. Nature Neuroscience. 2020;815
23(12):1655–1665. doi: https://doi.org/10.1038/s41593-020-00744-x.816
Donoghue T, Schaworonkow N, Voytek B. Methodological considerations for studying neural oscillations. Eu-817
ropean Journal of Neuroscience. 2022; 55(11-12):3502–3527. doi: https://doi.org/10.1111/ejn.15361.818
Doyle LM, Yarrow K, Brown P. Lateralization of event-related beta desynchronization in the EEG819
during pre-cued reaction time tasks. Clinical Neurophysiology. 2005; 116(8):1879–1888. doi:820
https://doi.org/10.1016/j.clinph.2005.03.017.821
Fabus MS, Woolrich MW, Warnaby CW, Quinn AJ. Understanding harmonic structures through822
instantaneous frequency. IEEE Open Journal of Signal Processing. 2022; 3:320–334. doi:823
https://doi.org/10.1109/OJSP.2022.3198012.824
Fischl B. FreeSurfer. Neuroimage. 2012; 62(2):774–781. doi: https://doi.org/10.1016/j.neuroimage.2012.01.021.825
Fries P. Rhythms for cognition: communication through coherence. Neuron. 2015; 88(1):220–235. doi:826
https://doi.org/10.1016/j.neuron.2015.09.034.827
Gips B, Bahramisharif A, Lowet E, Roberts MJ, de Weerd P, Jensen O, van der Eerden J. Discovering recur-828
ring patterns in electrophysiological recordings. Journal of Neuroscience Methods. 2017; 275:66–79. doi:829
https://doi.org/10.1016/j.jneumeth.2016.11.001.830
Giraud AL, Poeppel D. Cortical oscillations and speech processing: emerging computational principles and831
operations. Nature Neuroscience. 2012; 15(4):511–517. doi: https://doi.org/10.1016/j.tics.2012.05.003.832
Goyal A, Miller J, Qasim SE, Watrous AJ, Zhang H, Stein JM, Inman CS, Gross RE, Willie JT, Lega B, et al. Func-833
tionally distinct high and low theta oscillations in the human hippocampus. Nature communications. 2020;834
11(1):2469. doi: https://doi.org/10.1038/s41467-020-15670-6.835
Haegens S, Nácher V, Luna R, Romo R, Jensen O. 𝛼-Oscillations in the monkey sensorimotor network836
inﬂuence discrimination performance by rhythmical inhibition of neuronal spiking. Proceedings of837
the National Academy of Sciences of the United States of America. 2011; 108(48):19377–19382. doi:838
https://doi.org/10.1073/pnas.1117190108.839
He M, Das P, Hotan G, Purdon PL. Switching state-space modeling of neural signal dynamics. PLoS Computa-840
tional Biology. 2023; 19(8):e1011395. doi: https://doi.org/10.1371/journal.pcbi.1011395.841
Hu L, Ye L, Ye H, Liu X, Xiong K, Zhang Y, Zheng Z, Jiang H, Chen C, Wang Z, et al. Harmonic patterns embedding842
ictal EEG signals in focal epilepsy: a new insight into the epileptogenic zone. medRxiv. 2023; p. 2023–12. doi:843
https://doi.org/10.1101/2023.12.20.23300274.844
Hughes AM, Whitten TA, Caplan JB, Dickson CT. BOSC: A better oscillation detection method, extracts both845
sustained and transient rhythms from rat hippocampal recordings. Hippocampus. 2012; 22(6):1417–1428.846
doi: https://doi.org/10.1002/hipo.20979.847
Jackson N, Cole SR, Voytek B, Swann NC. Characteristics of waveform shape in Parkinson’s disease detected848
with scalp electroencephalography. eNeuro. 2019; 6(3). doi: https://doi.org/10.1523/ENEURO.0151-19.2019.849
26 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Jenkinson N, Brown P. New insights into the relationship between dopamine, beta oscillations and motor850
function. Trends in Neurosciences. 2011; 34(12):611–618. doi: https://doi.org/10.1016/j.tins.2011.09.003.851
Jensen O, Mazaheri A. Shaping functional architecture by oscillatory alpha activity: gating by inhibition. Fron-852
tiers in Human Neuroscience. 2010; 4:186. doi: https://doi.org/10.3389/fnhum.2010.00186.853
Klimesch W, Sauseng P, Hanslmayr S. EEG alpha oscillations: the inhibition–timing hypothesis. Brain research854
reviews. 2007; 53(1):63–88. doi: https://doi.org/10.1016/j.brainresrev.2006.06.003.855
Kuś R, Różański PT, Durka PJ. Multivariate matching pursuit in optimal Gabor dictionaries: theory and856
software with interface for EEG/MEG via Svarog. Biomedical engineering online. 2013; 12(1):1–28. doi:857
https://doi.org/10.1186/1475-925X-12-94.858
Lega BC, Jacobs J, Kahana M. Human hippocampal theta oscillations and the formation of episodic memories.859
Hippocampus. 2012; 22(4):748–761. doi: https://doi.org/10.1002/hipo.20937.860
Li J, Cao D, Dimakopoulos V, Shi W, Yu S, Fan L, Stieglitz L, Imbach L, Sarnthein J, Jiang T. Anterior–posterior861
hippocampal dynamics support working memory processing. Journal of Neuroscience. 2022; 42(3):443–453.862
doi: https://doi.org/10.1523/JNEUROSCI.1287-21.2021.863
Liu Y, Coon WG, de Pesters A, Brunner P, Schalk G. The Effects of Spatial Filtering and Artifacts on Electrocor-864
ticographic Signals. Journal of Neural Engineering. 2015; 12(5):056008. doi: https://doi.org/10.1088/1741-865
2560/12/5/056008.866
Lundqvist M, Rose J, Herman P, Brincat SL, Buschman TJ, Miller EK. Gamma and beta bursts underlie working867
memory. Neuron. 2016; 90(1):152–164. doi: https://doi.org/10.1016/j.neuron.2016.02.028.868
Matsuda T, Komaki F. Time series decomposition into oscillation components and phase estimation. Neural869
Computation. 2017; 29(2):332–367. doi: https://doi.org/10.1162/NECO_a_00916.870
Mazaheri A, Jensen O. Asymmetric amplitude modulations of brain oscillations generate slow evoked re-871
sponses. Journal of Neuroscience. 2008; 28(31):7781–7787. doi: https://doi.org/10.1523/JNEUROSCI.1631-872
08.2008.873
Miller KJ, Schalk G, Fetz EE, Den Nijs M, Ojemann JG, Rao RP. Cortical activity during motor execution, motor874
imagery, and imagery-based online feedback. Proceedings of the National Academy of Sciences of the United875
States of America. 2010; 107(9):4430–4435. doi: https://doi.org/10.1073/pnas.0913697107.876
Morales S, Bowers ME. Time-frequency analysis methods and their application in developmental EEG data.877
Developmental cognitive neuroscience. 2022; 54:101067. doi: https://doi.org/10.1016/j.dcn.2022.101067.878
Neymotin SA, Tal I, Barczak A, O’Connell MN, McGinnis T, Markowitz N, Espinal E, Griﬃth E, Anwar H, Dura-879
Bernal S, Schroeder CE, Lytton WW, Jones SR, Bickel S, Lakatos P. Detecting Spontaneous Neural Oscillation880
Events in Primate Auditory Cortex. eNeuro. 2022; 9(4). doi: https://doi.org/10.1523/ENEURO.0281-21.2022.881
Niedermeyer E, da Silva FL. Electroencephalography: basic principles, clinical applications, and related ﬁelds.882
Lippincott Williams & Wilkins; 2005. doi: https://doi.org/10.1093/med/9780190228484.001.0001.883
Nuwer MR. 10-10 electrode system for EEG recording. Clinical neurophysiology: oﬃcial jour-884
nal of the International Federation of Clinical Neurophysiology. 2018; 129(5):1103–1103. doi:885
https://doi.org/10.1016/j.clinph.2018.01.065.886
Ostlund B , Donoghue T, Anaya B, Gunther KE, Karalunas SL, Voytek B, Pérez-Edgar KE. Spectral parame-887
terization for studying neurodevelopment: How and why. Developmental Cognitive Neuroscience. 2022;888
54:101073. doi: https://doi.org/10.1016/j.dcn.2022.101073.889
Penﬁeld W , Jasper H. Epilepsy and the functional anatomy of the human brain. Little, Brown & Co.; 1954. doi:890
https://doi.org/10.1126/science.119.3097.645.b.891
de Pesters A, Coon WG, Brunner P, Gunduz A, Ritaccio AL, Brunet N, De Weerd P, Roberts M, Oosten-892
veld R, Fries P, et al. Alpha power indexes task-related networks on large and small scales: a mul-893
timodal ECoG study in humans and a non-human primate. NeuroImage. 2016; 134:122–131. doi:894
https://doi.org/10.1016/j.neuroimage.2016.03.074.895
Pfurtscheller G, Da Silva FL. Event-related EEG/MEG synchronization and desynchronization: basic principles.896
Clinical Neurophysiology. 1999; 110(11):1842–1857. doi: https://doi.org/10.1016/s1388-2457(99)00141-8.897
27 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Polich J, Lawson D. Event-related potential paradigms using tin electrodes. The American Journal of EEG898
Technology. 1985; 25(3):187–192. doi: https://doi.org/10.1080/00029238.1985.11080171.899
Quinn AJ, Lopes-dos Santos V, Huang N, Liang WK, Juan CH, Yeh JR, Nobre AC, Dupret D, Woolrich MW. Within-900
cycle instantaneous frequency proﬁles report oscillatory waveform dynamics. Journal of neurophysiology.901
2021; 126(4):1190–1208. doi: https://doi.org/10.1152/jn.00201.2021.902
Schalk G, McFarland DJ, Hinterberger T, Birbaumer N, Wolpaw JR. BCI2000: a general purpose brain-903
computer interface (BCI) system. IEEE Transactions on Biomedical Engineering. 2004; 51(6):1034–1043. doi:904
https://doi.org/10.1109/TBME.2004.827072.905
Schalk G . A general framework for dynamic cortical function: the function-through-biased-oscillations (FBO)906
hypothesis. Frontiers in Human Neuroscience. 2015; 9:352. doi: https://doi.org/10.3389/fnhum.2015.00352.907
Scheffer-Teixeira R, Tort AB. On cross-frequency phase-phase coupling between theta and gamma oscillations908
in the hippocampus. eLife. 2016; 5:e20515. doi: https://doi.org/10.7554/eLife.20515.909
Senkowski D, Molholm S, Gomez-Ramirez M, Foxe JJ. Oscillatory beta activity predicts response speed during a910
multisensory audiovisual reaction time task: a high-density electrical mapping study. Cerebral Cortex. 2006;911
16(11):1556–1565. doi: https://doi.org/10.1093/cercor/bhj091.912
Shirinpour S, Alekseichuk I, Mantell K, Opitz A. Experimental evaluation of methods for real-time EEG913
phase-speciﬁc transcranial magnetic stimulation. Journal of Neural Engineering. 2020; 17(4):046002. doi:914
https://doi.org/10.1088/1741-2552/ab9dba.915
Wechsler D. Wais-III, Wechsler Adult Intelligence Scale. San Antonio, TX: Psychological Corporation; 1997. doi:916
https://doi.org/10.1037/t49755-000.917
Wen H , Liu Z. Separating fractal and oscillatory components in the power spectrum of neurophysiological918
signal. Brain Topography. 2016; 29:13–26. doi: https://doi.org/10.1007/s10548-015-0448-0.919
Wilson LE, da Silva Castanheira J, Baillet S. Time-resolved parameterization of aperiodic and periodic brain920
activity. eLife. 2022; 11:e77348. doi: https://doi.org/10.7554/eLife.77348.921
Zanos S, Rembado I, Chen D, Fetz EE. Phase-locked stimulation during cortical beta oscillations pro-922
duces bidirectional synaptic plasticity in awake monkeys. Current Biology. 2018; 28(16):2515–2526. doi:923
https://doi.org/10.1016/j.cub.2018.07.009.924
28 of 28
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
-40 -30 -20 -10 0 10
SNR (dB)
5
10
15
20
25
30
35
40Frequency (Hz)
10 Hz
-7 db
0
0.2
0.4
0.6
0.8
1
Normalized
-40 -30 -20 -10 0 10
SNR (dB)
5
10
15
20
25
30
35
40Frequency (Hz)
7 Hz
-6 db
0
0.2
0.4
0.6
0.8
1
Normalized
A BDetected neural oscillations in EEG Detected neural oscillations in ECoG
Figure 4—ﬁgure supplement 1. SNR Histograms of EEG (A) and ECoG (B).
925
 Spectral accuracy for detecting the peak frequency of sinusoidal oscillations
CHO
OEvent
Fooof
SPRiNT
0
0.2
0.4
0.6
0.8
0
0.2
0.4
0.6
0.8
0
0.2
0.4
0.6
0.8
SPECIFICITY SENSITIVITY ACCURACYA B C
-24 -20 -16 -12 -8 -4 0  
SNR (dB)
-24 -20 -16 -12 -8 -4 0  -24 -20 -16 -12 -8 -4 0  
ECoG  EEG  
Figure 4—ﬁgure supplement 2. Synthetic sinusoidal oscillations.
926
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Delta (<3Hz) Theta (3-6Hz) Alpha (7-14Hz) Beta (15-30Hz) Gamma (31-40Hz)
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
Normalized Power
X1FOOOFCHO
X2FOOOFCHO
X3FOOOFCHO
X4FOOOFCHO
X5FOOOFCHO
X6FOOOFCHO
X7
FOOOFCHO
X8FOOOFCHO
Figure 5—ﬁgure supplement 1. ECoG results using FOOOF and CHO for all subjects.
927
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Delta Theta Alpha Beta Gamma
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
Normalized Power
y1
FOOOFCHO
y2FOOOFCHO
y3
FOOOFCHO
y4FOOOFCHO
y5FOOOFCHO
y6FOOOFCHO
y7
FOOOFCHO
Figure 6—ﬁgure supplement 1. Results from seven EEG subjects using the FOOOF and CHO
methods.
928
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
Delta Theta Alpha Beta Gamma
0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1
Normalized Power
Anterior
Posterior
Right Left
zs1
FOOOFCHO
zs2
FOOOFCHO
zs3
FOOOFCHO
zs4
FOOOFCHO
zs5
FOOOFCHO
zs6
FOOOFCHO
Figure 8—ﬁgure supplement 1. All results from six SEEG subjects using the FOOOF and CHO
methods.
929
.CC-BY 4.0 International licenseavailable under a
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made 
The copyright holder for this preprintthis version posted March 23, 2024. ; https://doi.org/10.1101/2023.10.04.560843doi: bioRxiv preprint 
