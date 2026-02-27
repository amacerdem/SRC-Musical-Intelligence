# Dissociation of Connectivity for Syntactic Irregularity and Perceptual Ambiguity in Musical Chord Stimuli

**Authors:** Chun Kee Chung
**Year:** D:20
**Subject:** Musical syntax has been studied mainly in terms of “syntactic irregularity” in harmonic/melodic sequences.

---

## ORIGINAL RESEARCH

published: 30 August 2021
doi: 10.3389/fnins.2021.693629
Edited by: Nicole Angenstein, Leibniz Institute for Neurobiology (LG), Germany
Reviewed by: Linshu Zhou, Shanghai Normal University, China
Yongjie Zhu, University of Helsinki, Finland
*Correspondence: Chun Kee Chung
chungc@snu.ac.kr
†Present address: Chan Hee Kim, Department of Physiology and Dental
Research Institute, Seoul National
University School of Dentistry, Seoul, South Korea
Specialty section: This article was submitted to
Auditory Cognitive Neuroscience,
a section of the journal
Frontiers in Neuroscience
Received: 13 April 2021
Accepted: 30 July 2021
Published: 30 August 2021
Citation: Kim CH, Jin SH, Kim JS, Kim Y, Yi SW and Chung CK (2021)
Dissociation of Connectivity for
Syntactic Irregularity and Perceptual
Ambiguity in Musical Chord Stimuli. Front. Neurosci. 15:693629.
doi: 10.3389/fnins.2021.693629
Dissociation of Connectivity for
Syntactic Irregularity and Perceptual
Ambiguity in Musical Chord Stimuli
Chan Hee Kim1,2†, Seung-Hyun Jin2, June Sic Kim2,3, Youn Kim4, Suk Won Yi5,6 and
Chun Kee Chung1,2,7,8*

### 1 Interdisciplinary Program in Neuroscience, College of Natural Science, Seoul National University, Seoul, South Korea,

### 2 Department of Neurosurgery, MEG Center, Seoul National University Hospital, Seoul, South Korea, 3 Research Institute of

Basic Sciences, Seoul National University, Seoul, South Korea, 4 Department of Music, School of Humanities, The University
of Hong Kong, Hong Kong, Hong Kong SAR China, 5 College of Music, Seoul National University, Seoul, South Korea,

### 6 Western Music Research Institute, Seoul National University, Seoul, South Korea, 7 Department of Brain and Cognitive

Science, College of Natural Science, Seoul National University, Seoul, South Korea, 8 Department of Neurosurgery, Seoul
National University Hospital, Seoul, South Korea
Musical syntax has been studied mainly in terms of “syntactic irregularity” in
harmonic/melodic sequences. However, “perceptual ambiguity” referring to the
uncertainty of judgment/classiﬁcation of presented stimuli can in addition be involved
in our musical stimuli using three different chord sequences. The present study
addresses how “syntactic irregularity” and “perceptual ambiguity” on musical syntax
are dissociated, in terms of effective connectivity between the bilateral inferior frontal
gyrus (IFGs) and superior temporal gyrus (STGs) by linearized time-delayed mutual
information (LTDMI). Three conditions were of ﬁve-chord sequences with endings of
dominant to tonic, dominant to submediant, and dominant to supertonic. The dominant
to supertonic is most irregular, compared with the regular dominant to tonic. The
dominant to submediant of the less irregular condition is the most ambiguous condition. In the LTDMI results, connectivity from the right to the left IFG (IFG-LTDMI) was enhanced
for the most irregular condition, whereas that from the right to the left STG (STG-LTDMI)
was enhanced for the most ambiguous condition (p = 0.024 in IFG-LTDMI, p < 0.001 in
STG-LTDMI, false discovery rate (FDR) corrected). Correct rate was negatively correlated
with STG-LTDMI, further reﬂecting perceptual ambiguity (p = 0.026). We found for the
ﬁrst time that syntactic irregularity and perceptual ambiguity coexist in chord stimulus
testing musical syntax and that the two processes are dissociated in interhemispheric
connectivities in the IFG and STG, respectively. Keywords: syntactic irregularity, perceptual ambiguity, effective connectivity, linearized time-delayed mutual
information, inferior frontal gyrus, superior temporal gyrus, magnetoencephalography
INTRODUCTION
Early right anterior negativity (ERAN) appearing with the negative peak at about 100–200 ms from
stimulus onset reﬂects the degree of expectation violations in chordal and melodic sequences; i.e.,
the more a chord and a melody are unexpected, and the more the peak amplitude of the ERAN
increases (Koelsch et al., 2000; Koelsch and Jentschke, 2010). The inferior frontal gyrus (IFG) is well
Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629

Kim et al. Syntactic Irregularity and Perceptual Ambiguity
known as the generator of ERAN (Maess et al., 2001). The
bilateral IFGs play crucial roles in the processing of harmonic
expectation (Sammler et al., 2011), though the right IFG shows
hemispheric dominance in syntactic irregularity processing
(Koelsch et al., 2002). The ERAN is observed in both musicians
and non-musicians alike (Koelsch et al., 2000, 2001; Maess
et al., 2001), even though it is inﬂuenced by musical expertise
(Koelsch et al., 2002). In our previous magnetoencephalography (MEG) study on the
ERAN (Kim et al., 2011), using three diﬀerent stimuli, which
consisted of three levels of “regular” (dominant to tonic), “less
irregular” (dominant to submediant), and “irregular” (dominant
to supertonic) conditions on the conditional probability, the
ERAN was not observed in the less irregular condition but
in the irregular condition. In the present study, we reanalyzed
our previous MEG data on the ERAN, using linearized time-
delayed mutual information (LTDMI; see section “Materials and
Methods”). The LTDMI is an eﬀective connectivity measure
that can calculate information transmission between two time
series by giving time delays, which is an ideal measure to test
the hypothesis of the present study focusing on the veriﬁcation
of information transmission between speciﬁc brain regions
based on the time domain. Our hypothesis is ﬁrst that the
connectivity between the bilateral IFGs would be increased
with the “dominant to supertonic,” eliciting the largest ERAN. Secondly, we hypothesized that perceptual ambiguity could be
separately processed with syntactic irregularity. Through the
questionnaire after the experiment on the participants, we
conﬁrmed the report that they (66.6% of respondents) felt the
most uncertain when discriminating “dominant to submediant.”
The term “ambiguity” generally refers to uncertainty caused by
two or more plausible interpretations of an object (Tuggy, 1993; Kennedy, 2019). In the present study, perceptual ambiguity refers
to the uncertainty of judgment/classiﬁcation of presented stimuli. Therefore, the “dominant to submediant” of the less irregular
condition might elicit a neural response to perceptual ambiguity
in areas other than the IFG, instead of the ERAN. Additionally,
we tested whether the LTDMI reﬂecting perceptual ambiguity
would be correlated with correct rate (CR) in the behavioral
experiment, since the more ambiguous it is to distinguish the
conditions, and the lower CR will be. In terms of statistical learning, both musicians and non-
musicians alike who have been exposed to a system of Western
tonal music could react sensitively to conditional probability on
chord progression in the Bach Choral (Rohrmeier and Cross,
2008). Therefore, if the ability to detect perceptual ambiguity
is a basic musical ability, both musicians and non-musicians
can react to perceptual ambiguity, and like the ability to detect
syntactic irregularity reﬂected in ERAN.

## MATERIALS AND METHODS

Ethics Statement
In the present study, we used the same data sets of our
previous study (Kim et al., 2011) that was approved by the
Institutional Review Board of the Clinical Research Institute, Seoul National University Hospital (H-1001-020-306); but in
order to apply a novel hypothesis, the entire process was newly
analyzed based on the analysis procedure of Kim et al. (2011). We
reanalyzed the data set to apply novel hypotheses and analyses. All participants provided informed consent of written form prior
to the experiments. Participants
All 19 participants were women (mean age, 24.3 ± 3.0 years):
9 were musicians and 10 were non-musicians. Musicians
(nine piano majors and one violin major) majored in musical
instruments at the College of Music and received training from
the age of 5 for at least 15 years. Most of the non-musicians
had experience taking piano lessons, but they were not music
majors. Considering the diﬀerence in hemispheric dominance
of syntactic processing according to gender, only women were
recruited (Koelsch et al., 2003; Kim et al., 2011). They all had
normal hearing and were right-handed. Musical Stimuli
We used three diﬀerent conditions: T, SM, and ST (T = most
regular; SM = less regular; ST = most irregular; and see
also Figure 1A). The T was composed of “tonic–submediant–
supertonic–dominant–tonic.” The ending chord of “tonic” was
replaced with “submediant” and “supertonic” in the SM and ST,
respectively. The chords from the ﬁrst to fourth were the same
in all conditions. In each condition, the duration of a chord
was 600 ms. A chord sequence totaled 3,600 ms, including ﬁve
chords and a 600-ms resting period (Figure 1B). All conditions
transposed into 12 major keys, were randomly shuﬄed in
each session, and were recorded at 100 BPM using Cubase 5
(Steinberg Media Technologies, Hamburg, Germany) software. The intensity was normalized in each wave ﬁle (sampling rate
44.1 kHz; 16-bit; stereo; windows PCM) using Cool Edit Pro 2.1
(Syntrillium Software Corporation, Phoenix, AZ, United States). The piano timbre (Bösendorfer 290 Imperial grand) in each
chord was created by Grand 3 (Steinberg Media Technologies, Hamburg, Germany) software. Magnetoencephalography Recording
The whole experimental paradigm was composed of three
behavioral test sessions after six MEG recording sessions
(Figure 1B). Each MEG session included 100 sequences
consisting of 30 sequences per condition and 10 staccato
sequences. In individual staccato sequences, a staccato chord
of 37.5-ms duration was presented in the third, fourth, or ﬁfth
chord. The participants were asked to detect staccato chords and
to respond using a mouse. The response for staccato sequences
was excluded in the MEG data analysis. In each behavioral
session after MEG recording, 12 sequences per condition were
randomly presented. For the conditions of T, SM, and ST, all
participants were asked to identify each condition using the 1,
2, and 3 buttons on the keypad, respectively, instead of using
chord labels of T, SM, and ST. The participants were instructed
to distinguish between the three stimuli and to understand each
task of the MEG/behavioral experiment. This process was done
through training for a certain period of time before starting
Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629

Kim et al. Syntactic Irregularity and Perceptual Ambiguity
FIGURE 1 | Musical stimuli and experimental paradigm. (A) Musical stimuli are composed of three different ﬁve-chord sequences. The three conditions are T, SM,
and ST, ending with dominant to tonic, dominant to submediant, and dominant to supertonic, respectively. (B) In the magnetoencephalography experiment (top), the
participants listened to the three conditions carefully and were asked to detect the staccato chord among chord sequences in the three conditions, and to click a
mouse (to check the level of attending the conditions). In the behavioral experiment (bottom), the participants discriminated the three conditions and responded by
using the 1, 2, and 3 buttons on the keypad.
the main experiment. The musical stimuli were presented at
the sound pressure level of 65 dB into MEG-compatible tubal
insert earphones (Tip-300, Nicolet, Madison, WI, United States)
using the STIM2 (Neuroscan, Charlotte, NC, United States)
system. The whole experiment took about 2 h. MEG signals were
recorded in a magnetically shielded room using a 306-channel
whole-head MEG System (Elekta NeuroMag VectorViewTM, Helsinki, Finland), with a sampling rate of 600.615 Hz using
0.1- to 200-Hz band-pass ﬁlter. Electrooculograms (EOGs) and
electrocardiograms (ECGs) were simultaneously recorded to later
remove ocular and cardiac noise. Magnetoencephalography Analysis
The environmental magnetic noise of raw MEG signals was
eliminated by the temporal Signal-Space Separation (tSSS)
algorithm in MaxFilter 2.1.13 (Elekta Neuromag Oy, Helsinki, Finland) (Taulu and Simola, 2006; Taulu and Hari, 2009). The 204 orthogonal planar gradiometer in 102 locations was
used in the further analysis procedure. Source analysis of four
regions of interest (ROIs) [bilateral IFGs and superior temporal
gyrus (STGs)] was performed using BESA 5.1.8.10 (MEGIS
Software GmbH, Gräfelﬁng, Germany). Multiple equivalent
current dipoles (ECDs) for the bilateral IFGs and STGs were ﬁt
on the generators of P2m and ERANm (as magnetic counterparts
of the P2 and ERAN, respectively), as estimated with the same
procedures as in our previous studies (Kim et al., 2011, 2014). After the ECDs of P2m were estimated in the peak latency of
180–190 ms for an average of all in-key chords, the ECDs of
ERANm were estimated in 140–220 ms for all ending chords
(mean of the tonic, submediant, and supertonic chords). The
ECDs were localized on the bilateral STGs involving auditory
cortices for the P2m and on the bilateral IFGs for the ERANm. The multiple dipoles were more than 80% of the goodness of
ﬁt (GOF). The estimated dipoles in the IFG were superior and
anterior to those in the STG (Maess et al., 2001; Kim et al., 2011,
2014). The x, y, and z in Talairach coordinates (millimeters) were
−45.1, −8.9, and 1.9 in the left STG; 43.1, −2.6, and 2 in the right
STG; −40.8, 18.5, and 15.6 in the left IFG; and 37.6, 21.2, and 15.1
in the right IFG, respectively (Supplementary Figure 1A). The
signal for ECDs was extracted in 400-ms epochs after the onset
of the ending chord using a 1- to 20-Hz band-pass ﬁlter for each
participant. The 400 ms was the time window involving the peak
latencies of P2m and ERANm in our previous studies (Kim et al.,
2011, 2014; Supplementary Figure 1B). Using the ECD signals of 400 ms in the multiple dipoles
of the bilateral IFGs and STGs, we estimated the information
ﬂows in 12 directional connections between the bilateral IFGs
and STGs for the three conditions. Eﬀective connectivity for
12 connections was calculated by LTDMI (Jin et al., 2010). The LTDMI is an information-theoretic measure of functional
coupling based on mutual information (MI) (Jin et al., 2011,
2012; Kim et al., 2020), which predicts information transmission
between two time series. Mutual information is deﬁned as the quantity of information
shared in two time series of X (n) and Y (n) (n = 1, 2,..., N), at N discrete points. The probability density function
Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629

Kim et al. Syntactic Irregularity and Perceptual Ambiguity
(PDF) of X (n) and Y (n) is p (X (n), κ) ≡p (X (n)) and
p (Y (n), κ) ≡p (Y (n)) with n = 1, 2,..., bin, respectively. The
MI is computed by p (X (n), Y (n)), the joint PDF between X (n)
and Y (n), as follows: MI = MIXY = MIYX = MI (X (n), Y (n))
= −
X
k
p (X (n), Y (n)) log p(X (n), Y(n))
p(X (n) )p(Y(n))
(1)
If X (n) and Y (n) are completely identical, the MI is maximum. However, if two time series are independent of each other, the
MI is zero. The directional information transmission between the
two time series can be calculated by time-delayed MI (TDMI): TDMIXY = TDMI (X (n), Y (n + τ))
= −
X
k
p (X (n), Y(n + τ)) log p(X (n), Y(n + τ))
p(X (n) )p(Y(n + τ))
TDMIYX = TDMI (Y (n), X (n + τ))
= −
X
k
p (Y (n), X (n + τ)) log p(Y (n), X(n + τ))
p(Y (n))p(X(n + τ))
(2)
Time-delayed MI can detect linear and non-linear correlations
between two time series. Since the data length used in the present
study (400-ms epoch) was insuﬃcient to reconstruct a reliable
PDF for general TDMI presented in Equation (2), we used
LTDMI as an eﬀective connectivity measure in this study. LTDMI
is adopted as follows: LTDMIXY = LTDMI (X (n), Y (n + τ))
= −1
2log
1−ρ2
X(n)Y(n+τ)

LTDMIYX = LTDMI (Y (n), X (n + τ))
= −1
2log
1−ρ2
Y(n)X(n+τ)

(3)
where,
ρX (n) Y(n + τ) and ρY (n) X(n + τ) are
a
cross-
correlation coeﬃcient. The τ of delay time was 120 ms. To
estimate the linearized information ﬂow between the time series,
each time series is assumed with the Gaussian distribution
function with zero mean, and variance σ2
X, σ2
Y, i.e., p (X) =

√
2π σ2 exp (−x2/2σ2). The LTDMI values were averaged over
delay time. When the diﬀerence between LTDMIXY
and
LTDMIYX is positive, the information ﬂow between X and Y was
interpreted as “X to Y.”
Diﬀerences in the LTDMI values among the three conditions
of T, SM, and ST in 12 connections were tested by the two-way
repeated-measures analysis of variance (ANOVA). In all post hoc
analysis steps, the alpha levels for multiple comparisons were
adjusted by the Benjamin–Hochberg FDR correction (p < 0.05). Additionally, the group diﬀerence for the LTDMI values was
tested by the independent t-test (p < 0.05). In the MEG experiment, the mean CR for staccato chord
detection was calculated for each participant. In the behavioral
experiment, the diﬀerence between the three conditions for
the CR was determined by the one-way repeated-measures
for all conditions. Correlation analysis was performed to test the relationships
between the LTDMI value and CR for all conditions of all
participants (i.e., for the merged data set of three conditions of
18 participants). In the correlation analysis for the LTDMI value
and the CR, the correlation was tested using Spearman’s rank
correlation because the data were not normally distributed. The
correlation was calculated using the one-tailed test because the
ambiguous stimuli lead to slower and less accurate responses than
the easy stimuli (Sabri et al., 2006; Jastorﬀet al., 2009; Fleming
et al., 2010). The alpha level was adjusted by the FDR correction
for the multiple comparisons testing of the three conditions
(p < 0.05). The Greenhouse–Geisser correction was applied
because the sphericity of the data was violated via Mauchly’s
sphericity test. All statistical analyses were performed using SPSS
21.0 software (IBM, Armonk, NY, United States). RESULTS
Linearized Time-Delayed Mutual
Information Values for Three Conditions
The LTDMIs were calculated for 12 connections among four
ROIs of the bilateral IFGs and STGs for three conditions
of the T, SM, and ST in 19 participants. For the LTDMI
values, we performed a two-way repeated-measures ANOVA
with two factors of Condition and Connection. The ANOVA
(n = 19) showed a signiﬁcant main eﬀect of Condition [F(1.872,
404.247) = 3.108, p = 0.049] and a signiﬁcant interaction
of Condition × Connection [F(20.587, 404.247) = 2.555,
p = 0.0002], and a signiﬁcant eﬀect of Connection [F(1,
216) = 1.920, p = 0.038]. Post hoc one-way repeated-measures
ANOVAs with the Condition factor in 12 connections conﬁrmed
a connection reﬂecting the diﬀerence among the three conditions. The diﬀerence between the three conditions was revealed only in
two connections from the right to the left IFG [F(2, 36) = 6.526,
p = 0.024, and FDR corrected] and from the right to the left STG
[F(2, 36) = 12.373, p < 0.001, and FDR corrected] among 12
connections (Figures 2B, C; see also Supplementary Table 1). Hereafter, we use the term “IFG-LTDMI” to refer to the
LTDMI values from the right to the left IFG and the term “STG-
LTDMI” to refer to those from the right to the left STG. In
the two interhemispheric connections, the SM and ST of the
most ambiguous and irregular conditions showed the highest
STG-LTDMI and IFG-LTDMI, respectively. In a post hoc paired t-test, the IFG-LTDMI (MEAN[SD]
for IFG-LTDMI values of three conditions, T = 0.1584[0.1207], SM = 0.1563[0.1116], and ST = 0.2614[0.1186]) was higher for the
ST than for the T [t(18) = 3.091, p = 0.009, and FDR corrected]
and for the SM [t(18) = 3.223, p = 0.009, and FDR corrected],
while the IFG-LTDMI for the T and SM was not signiﬁcantly
diﬀerent [t(18) = 0.061, p = 0.952, and FDR corrected]. The
STG-LTDMI (MEAN[SD] for STG-LTDMI values of three
conditions, T = 0.2019[0.0919], SM = 0.2500[0.0843], and
ST = 0.1438[0.0541]) was higher for the SM than for the
Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629

Kim et al. Syntactic Irregularity and Perceptual Ambiguity
FIGURE 2 | Difference in the linearized time-delayed mutual information (LTDMI) values for the three conditions. (A) Correct rate (CR) of SM is signiﬁcantly lower than
the CR of ST. The other pairs are not statistically signiﬁcant. *p < 0.05. (B) Difference between the conditions for LTDMI was revealed in only two interhemispheric
connections, which were termed “IFG-LTDMI” and “STG-LTDMI.” (C) The STG-LTDMIs were different between all pairs. In the IFG-LTDMI, the SM was higher in the
other conditions. *p < 0.05, **p < 0.01, and ***p < 0.001 (FDR corrected). Error bars denote 95% conﬁdence intervals. See also Supplementary Table 1. LTDMI,
linearized time-delayed mutual information; CR, correct rate; IFG, inferior frontal gyrus; STG, superior temporal gyrus; FDR, false discovery rate. T [t(18) = 2.691, p = 0.023, and FDR corrected] and the ST
[t(18) = 5.357, p = 0.0001, and FDR corrected], while it was
signiﬁcantly higher for the T than for the ST [t(18) = 2.259,
p = 0.037, and FDR corrected]. Behavioral Response
During the MEG experiment, participants were asked to listen
to each condition carefully and to detect the sequences including
a staccato chord in order to check the level of attending to
the condition (Figure 1B). All participants detected the staccato
chord with more than 95% including the number of missed
buttons. This indicates that the participants paid attention
to musical stimuli. After the MEG experiment, participants
performed a behavioral test discriminating among the three
conditions (Figure 1B). The mean CR (n = 18) was lower in
the SM (77.0%) than in the T (82.4%) and the ST (88.7%). The one-way repeated-measures ANOVA (n = 18, excluded
one outlier) showed a signiﬁcant main eﬀect of Condition
[F(2,34) = 4.799, p = 0.015]. In a post hoc analysis, the diﬀerence
between the CRs was signiﬁcant only between the SM and the
ST (Figure 2A). The SM was signiﬁcantly lower than the ST
[t(17) = −2.574, p = 0.020]. There were no signiﬁcant diﬀerences
in the pairs of T vs. SM [t(17) = 1.772, p = 0.094] and T vs. ST
[t(17) = −1.753, p = 0.098]. Additionally, in the questionnaire
after the experiment on the participants, of the total participants,
15 responded to the questionnaire; among them, 10 responded
“not certain” with the SM, while 13 responded “certain” for
the ST. Correlation Between the Linearized
Time-Delayed Mutual Information Values
and Correct Rate
To conﬁrm whether the STG-LTDMI reﬂected perceptual
ambiguity, and, if it was so, whether it was speciﬁc for the STG-
LTDMI among the IFG-LTDMI and the STG-LTDMI, we tested
the correlation between the LTDMI values of STG-LTDMI/IFG-
LTDMI and the behavioral response of CR. The correlation was
tested using the values for all conditions and participants (n = 57,
3 conditions × 19 participants). A signiﬁcant correlation with
the CR was observed not in the IFG-LTDMI but in the STG-
LTDMI (one-tailed Spearman’s rank correlation; STG-LTDMI, Spearman’s ρ =
−0.260, p = 0.026; IFG-LTDMI, Spearman’s
ρ = 0.064, and p = 0.319) (Figure 3). DISCUSSION
The IFG-LTDMI was enhanced for the ST of the most irregular
condition. The STG-LTDMI was enhanced for the SM of
the most ambiguous condition. The processing of syntactic
irregularity and perceptual ambiguity in the three conditions
was dissociated in the IFG-LTDMI, and the STG-LTDMI,
respectively. This implies that the brain interprets the three
conditions as both “from regular to irregular” and “from
ambiguous to unambiguous” conditions simultaneously. The highest IFG-LTDMI for the ST is a further extension
of the highest ERAN response elicited only for the most
irregular condition (ST) in our previous study (Kim et al.,
2011). The IFG-LTDMI in terms of eﬀective connectivity may
underlie the ERAN. Moreover, our data on IFG-LTDMI clearly
show how both hemispheres of IFG are closely related to
the processing of musical syntax. Also, it clearly shows what
kind of connection between these areas is interpreted from the
information introduced from the outside. Thus, the IFG-LTDMI
from the right to the left IFGs is one step forward from the
previous reports that the bilateral IFGs are the neural generators
of ERAN (Maess et al., 2001; Sammler et al., 2009; Kim et al.,
2011, 2014). Our data suggest that the left IFG and the right IFG
interrelate in the processing of musical syntax, and in terms of
eﬀective connectivity. The STG-LTDMI was the highest for the most ambiguous
SM. The patterns of STG-LTDMI between all conditions were
consistent with our hypotheses that the SM would be most
ambiguous. In a language study, acoustic–phonetic processing is
related to the STG (Callan et al., 2004). Auditory areas involving
Heschl’s gyrus are activated by ambiguous phonemes (Kilian-
Hutten et al., 2011). The STG is related to the processing
Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629

Kim et al. Syntactic Irregularity and Perceptual Ambiguity
FIGURE 3 | Correlation between correct rate (CR) and STG-LTDMI/IFG-LTDMI. The CR was only negatively correlated with the STG-LTDMI (n = 57, one-tailed
Spearman’s rank correlation, Spearman’s ρ = −0.260, and p = 0.026). However, for the IFG-LTDMI, a signiﬁcant correlation was not observed in both all
participants, and subgroups. Best-ﬁt trend lines for all participants (black solid line) are depicted in each graph. CR, correct rate; STG, superior temporal gyrus; LTDMI, linearized time-delayed mutual information; IFG, inferior frontal gyrus.
of pitch and melody (Patterson et al., 2002; Schneider et al.,
2005). The activity in the bilateral STGs is asymmetric in the
right hemisphere (Patterson et al., 2002; Warrier and Zatorre,
2004; Bidelman and Grall, 2014). The right STG is more
highly activated for deviant tones (Sabri et al., 2006) and is
more sensitive to pitch congruency (Nan and Friederici, 2013)
than the left STG. In contrast, the fundamental pitch in an
ambiguous tone is processed in the left STG, while spectral pitch
is processed in the right STG (Schneider et al., 2005). In a tone
interval discrimination task, the STG dissociates diﬃcult, and
easy tasks (Sabri et al., 2006). Unambiguous stimuli of speech
and ambiguous stimuli of speech like song diﬀerently activate
the STG (Tierney et al., 2013). As the aforementioned studies, we
interpret our ﬁndings in the bilateral STGs as indicating neural
substrates for the perception of ambiguities implied in musical
chord stimuli. In terms of voice leading, the ST of the most
irregular condition with a salient melodic line (Kim et al., 2014)
would be more distinguishable than other chords. However,
since the SM shares the same voice leading as the T, this might
have been another factor that could aﬀect perceptual ambiguity. The sensory novelty and frequency of occurrence of the ending
chords due to the distance between the two repeated chords
varying between the three conditions might be a confounding
factor aﬀecting perceptual ambiguity (Koelsch et al., 2007; Zhou
et al., 2019). Unlike the T of the major triad, also, the similar
sonic quality of the minor triad may cause perceptual ambiguity
between the SM and the ST. Therefore, the levels of perceptual
ambiguity reﬂected in interhemispheric connectivity between
the bilateral STG of STG-LTDMI might reﬂect the processes of
all factors that could be heard in the chord stimulus (see also
Supplementary Figure 2). In previous studies, the connection between the IFG and
STG is involved in the processing of syntax in music and
language (Sakai et al., 2002; Sammler et al., 2009; Friederici,
2011; Musso et al., 2015). Moreover, an fMRI study using a
real musical piece reported that the diﬀerent levels of syntactic
irregularity were reﬂected in functional connectivity between the
IFG and STG (Seger et al., 2013). In another fMRI study on
acoustic–phonetic processing, IFG–STG coupling is increased by
ambiguous acoustic signal (Leitman et al., 2010). However, our
data did not show the connection between the IFG and the STG
in either syntactic irregularity or perceptual ambiguity. Instead,
the connectivity was dissociated in IFG and STG. Furthermore,
the direction of eﬀective connectivity was from the right to
left hemisphere in both the IFG-LTDMI and STG-LTDMI. We
interpret dissociation of the IFG and STG in connectivity as
indicating the functional segregation related to syntax, and
ambiguity processing. Also, we interpret that the same direction
of information transmission in the bilateral IFGs and STGs as
indicating the diﬀerent roles of bilateral hemispheres in music
processing and indicating the IFG-LTDMI and STG-LTDMI
commonly based on the rightward asymmetry. Considering the STG-LTDMI, the SM is the most ambiguous
among the three conditions, and the ST is less ambiguous than
the T. The more ambiguous condition may be more diﬃcult
to discriminate than the less ambiguous condition. However,
although the CR was only signiﬁcantly diﬀerent between the SM
and the ST, the level of perceptual ambiguity was not perfectly
conﬁrmed in terms of behavioral results. Our data show that the
participants could discriminate among the three chord sequences
with reasonable accuracy (CRs for all conditions > 77%). We
infer that the CR was overall high (ceiling eﬀect), so perceptual
ambiguity was probably not reﬂected in the CR. Therefore, we
expected that the STG-LTDMI, an index reﬂecting perceptual
ambiguity, would be related to the CR because perceptual
ambiguity was involved in the CR, and the result was as expected. Most notable is that the signiﬁcant correlation was only observed
in the STG-LTDMI, not in the IFG-LTDMI. From these results,
it can be inferred that the processing of perceptually ambiguous
stimuli triggered the enhancement of connectivity in the STG-
LTDMI. The STG-LTDMI was the lowest for the ST. Which of the
factors made each condition sound more ambiguous and less
ambiguous cannot be clearly veriﬁed through the present results. Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629

Kim et al. Syntactic Irregularity and Perceptual Ambiguity
However, it could be conﬁrmed that at least the SM, which was
likely to be confused with the other two conditions, was the
most ambiguous; and the ST, the most irregular condition with
a salient melodic line, was the most unambiguous. Syntactic
error of the ST is well recognized by both musicians and non-
musicians (Koelsch et al., 2000, 2001; Maess et al., 2001), and
it can be inferred that the fact that more than half of the
participants were non-musicians who were known to use chord
identiﬁcation strategies for melodic line (Sears et al., 2014) would
all have inﬂuenced the present ﬁndings. From the fact that
our ﬁndings were observed in the results including musicians
and non-musicians, we could presume that discriminating, and
perceiving the properties of chords could be a basic ability
implicitly acquired in musical experiences just as it could detect
syntactic violation (Koelsch et al., 2000). LIMITATION
Although our data suggest perceptual segregation of syntactic
irregularity and perceptual ambiguity in chord sequences, and
our data only focused on the four ROIs of the bilateral IFGs
and STGs based on our hypothesis. This syntactic irregularity
and perceptual ambiguity processes would be also examined in
terms of the whole-brain analysis including the four ROIs of
the bilateral IFGs and STGs on our hypothesis. Furthermore,
interhemispheric connectivity might be more clearly revealed
since the present study was only conducted on female
participants. Which hemisphere of bilateral hemispheres is more
dominant, or whether males can show diﬀerent information ﬂow
in the directional connections, should be discussed and compared
in future studies. Additionally, the main goal of the present study
was not to select the factors aﬀecting perceptual ambiguity and
to identify the weight of each but to suggest the neurocognitive
basis for the existence of perceptual ambiguity. Which of the
aforementioned factors is perceptually dominant would be also
addressed in future studies. CONCLUSION
To conclude, our ﬁndings demonstrate for the ﬁrst time through
neurobiological data that two processes, syntactic irregularity
and perceptual ambiguity, coexist at the level corresponding to
each condition in the musical stimuli of the chord sequence
testing syntactic irregularity. The connectivity from the left to
the right hemisphere in the IFG and the STG enhanced when the
levels of the two processes were high, respectively. These results
indicate that the two interhemispheric connectivities observed
simultaneously in the IFG and the STG are neural substrates
corresponding to the two processes.

## DATA AVAILABILITY STATEMENT

The raw data supporting the conclusions of this article will be
made available by the authors, without undue reservation.

## ETHICS STATEMENT

The studies involving human participants were reviewed and
approved by Institutional Review Board of the Clinical Research
Institute, Seoul National University Hospital (H-1001-020-
306). The patients/participants provided their written informed
consent to participate in this study. Written informed consent
was obtained from the individual(s) for the publication of any
potentially identiﬁable images or data included in this article.

## AUTHOR CONTRIBUTIONS

CK and CC conceived the study and wrote the manuscript. SJ
and JK contributed to analytic tools. YK and SY contributed to
music-theoretical background. CK analyzed the data. All authors
discussed the results and reviewed the manuscript. FUNDING
This research was supported by Samsung Research Funding
& Incubation Center for Future Technology (SRFC-IT1902-
08, Decoding Inner Music Using Electrocorticography), and
the
Technology
Innovation
Program
(Alchemist
Project)
(20012355, Fully implantable closed loop Brain to X for voice
communication) funded by the Ministry of Trade, Industry and
Energy (MOTIE, South Korea). The funders had no role in
study design, data collection and analysis, decision to publish,
or preparation of the manuscript. ACKNOWLEDGMENTS
We would like to thank Ji Hyang Nam for the technical support
in MEG acquisition.

## SUPPLEMENTARY MATERIAL

The Supplementary Material for this article can be found
online
at:
https://www.frontiersin.org/articles/10.3389/fnins.
2021.693629/full#supplementary-material
REFERENCES
Bidelman, G. M.,
and
Grall, J.
(2014). Functional
organization
for
musical
consonance
and
tonal
pitch
hierarchy
in
human
auditory
cortex. Neuroimage
101,
204–214.
doi:
10.1016/j.neuroimage.2014.
07.005
Callan, D. E., Jones, J. A., Callan, A. M., and Akahane-Yamada, R. (2004). Phonetic perceptual identiﬁcation by native- and second-language speakers
diﬀerentially
activates
brain
regions
involved
with
acoustic
phonetic
processing
and
those
involved
with
articulatory-auditory/orosensory
internal models. Neuroimage 22, 1182–1194. doi: 10.1016/j.neuroimage.2004.
03.006
Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629

Kim et al. Syntactic Irregularity and Perceptual Ambiguity
Fleming, S. M., Thomas, C. L., and Dolan, R. J. (2010). Overcoming status quo
bias in the human brain. Proc. Natl. Acad. Sci. U. S. A. 107, 6005–6009. doi:
10.1073/pnas.0910380107
Friederici, A. D. (2011). The brain basis of language processing: from structure to
function. Physiol. Rev. 91, 1357–1392. Jastorﬀ, J., Kourtzi, Z., and Giese, M. A. (2009). Visual learning shapes the
processing of complex movement stimuli in the human brain. J. Neurosci. 29,
14026–14038. doi: 10.1523/JNEUROSCI.3070-09.2009
Jin, S. H., Lin, P., and Hallett, M. (2010). Linear and nonlinear information
ﬂow based on time-delayed mutual information method and its application to
corticomuscular interaction. Clin. Neurophysiol. 121, 392–401. doi: 10.1016/j.
clinph.2009.09.033
Jin, S. H., Lin, P., and Hallett, M. (2012). Reorganization of brain functional small-
world networks during ﬁnger movements. Hum. Brain Mapp. 33, 861–872.
doi: 10.1002/hbm.21253
Jin, S. H., Seol, J., Kim, J. S., and Chung, C. K. (2011). How reliable are the
functional connectivity networks of MEG in resting states? J. Neurophysiol. 106,
2888–2895. doi: 10.1152/jn.00335.2011
Kennedy, C. (2019). “8 Ambiguity and vagueness: an overview,” in Semantics-
Lexical Structures and Adjectives, eds C. Maienborn, K. von Heusinger, and P. Portner (Chicago, IL: Department of Linguistics, University of Chicago), 236. Kilian-Hutten, N., Valente, G., Vroomen, J., and Formisano, E. (2011). Auditory
cortex encodes the perceptual interpretation of ambiguous sound. J. Neurosci.
31, 1715–1720. doi: 10.1523/JNEUROSCI.4572-10.2011
Kim, C. H., Lee, S., Kim, J. S., Seol, J., Yi, S. W., and Chung, C. K. (2014). Melody
eﬀects on ERANm elicited by harmonic irregularity in musical syntax. Brain
Res. 1560, 36–45. doi: 10.1016/j.brainres.2014.02.045
Kim, C. H., Seol, J., Jin, S. H., Kim, J. S., Kim, Y., Yi, S. W., et al. (2020). Increased
fronto-temporal connectivity by modiﬁed melody in real music. PLoS One
15:e0235770. doi: 10.1371/journal.pone.0235770
Kim, S. G., Kim, J. S., and Chung, C. K. (2011). The eﬀect of conditional probability
of chord progression on brain response: an MEG study. PLoS One 6:e17337.
doi: 10.1371/journal.pone.0017337
Koelsch, S., and Jentschke, S. (2010). Diﬀerences in electric brain responses to
melodies and chords. J. Cogn. Neurosci. 22, 2251–2262. doi: 10.1162/jocn.2009. Koelsch, S., Gunter, T. C., Schroger, E., Tervaniemi, M., Sammler, D., and
Friederici, A. D. (2001). Diﬀerentiating ERAN and MMN: an ERP study. Neuroreport 12, 1385–1389. Koelsch, S., Gunter, T., Friederici, A. D., and Schröger, E. (2000). Brain
indices of music processing:“nonmusicians” are musical. J. Cogn. Neurosci. 12,
520–541. Koelsch, S., Jentschke, S., Sammler, D., and Mietchen, D. (2007). Untangling
syntactic and sensory processing: an ERP study of music perception. Psychophysiology 44, 476–490. doi: 10.1111/j.1469-8986.2007.00517.x
Koelsch, S., Maess, B., Grossmann, T., and Friederici, A. D. (2003). Electric
brain responses reveal gender diﬀerences in music processing. Neuroreport 14,
709–713. doi: 10.1097/01.wnr.0000065762.60383.67
Koelsch, S., Schmidt, B. H., and Kansok, J. (2002). Eﬀects of musical expertise
on the early right anterior negativity: an event-related brain potential study. Psychophysiology 39, 657–663. Leitman, D. I., Wolf, D. H., Ragland, J. D., Laukka, P., Loughead, J., Valdez, J. N., et al. (2010). “It’s not what you say, but how you say it”: a reciprocal
temporo-frontal network for aﬀective prosody. Front. Hum. Neurosci. 4:19.
doi: 10.3389/fnhum.2010.00019
Maess, B., Koelsch, S., Gunter, T. C., and Friederici, A. D. (2001). Musical syntax
is processed in Broca’s area: an MEG study. Nat. Neurosci. 4, 540–545. doi:
10.1038/87502
Musso, M., Weiller, C., Horn, A., Glauche, V., Umarova, R., Hennig, J., et al. (2015). A single dual-stream framework for syntactic computations in music and
language. Neuroimage 117, 267–283. doi: 10.1016/j.neuroimage.2015.05.020
Nan, Y., and Friederici, A. D. (2013). Diﬀerential roles of right temporal
cortex
and
Broca’s
area
in
pitch
processing:
evidence
from
music
and Mandarin. Hum. Brain Mapp. 34, 2045–2054. doi: 10.1002/hbm. Patterson, R. D., Uppenkamp, S., Johnsrude, I. S., and Griﬃths, T. D. (2002). The processing of temporal pitch and melody information in auditory cortex. Neuron 36, 767–776. Rohrmeier, M. A., and Cross, I. (2008). Statistical Properties of Tonal Harmony in
Bach’s Chorales. Sapporo: ICMPC. Sabri, M., Liebenthal, E., Waldron, E. J., Medler, D. A., and Binder, J. R. (2006). Attentional modulation in the detection of irrelevant deviance: a simultaneous
ERP/fMRI study. J. Cogn. Neurosci. 18, 689–700. doi: 10.1162/jocn.2006.18.
5.689
Sakai, K. L., Noguchi, Y., Takeuchi, T., and Watanabe, E. (2002). Selective priming
of syntactic processing by event-related transcranial magnetic stimulation of
Broca’s area. Neuron 35, 1177–1182. Sammler, D., Koelsch, S., and Friederici, A. D. (2011). Are left fronto-temporal
brain areas a prerequisite for normal music-syntactic processing? Cortex 47,
659–673. doi: 10.1016/j.cortex.2010.04.007
Sammler, D., Koelsch, S., Ball, T., Brandt, A., Elger, C. E., Friederici, A. D., et al.
(2009). Overlap of musical and linguistic syntax processing: intracranial ERP
evidence. Ann. N. Y. Acad. Sci. 1169, 494–498. doi: 10.1111/j.1749-6632.2009.
04792.x
Schneider, P., Sluming, V., Roberts, N., Scherg, M., Goebel, R., Specht, H. J., et al.
(2005). Structural and functional asymmetry of lateral Heschl’s gyrus reﬂects
pitch perception preference. Nat. Neurosci. 8, 1241–1247. doi: 10.1038/nn1530
Sears, D., Caplin, W. E., and McAdams, S. (2014). Perceiving the classical cadence. Music Percept. Interdiscipl. J. 31, 397–417. doi: 10.1525/mp.2014.31.5.397
Seger, C. A., Spiering, B. J., Sares, A. G., Quraini, S. I., Alpeter, C., David, J., et al.
(2013). Corticostriatal contributions to musical expectancy perception. J. Cogn. Neurosci. 25, 1062–1077. doi: 10.1162/jocn_a_00371
Taulu, S., and Hari, R. (2009). Removal of magnetoencephalographic artifacts with
temporal signal-space separation: demonstration with single-trial auditory-
evoked responses. Hum. Brain Mapp. 30, 1524–1534. doi: 10.1002/hbm.20627
Taulu, S., and Simola, J. (2006). Spatiotemporal signal space separation method
for rejecting nearby interference in MEG measurements. Phys. Med. Biol. 51,
1759–1768. doi: 10.1088/0031-9155/51/7/008
Tierney, A., Dick, F., Deutsch, D., and Sereno, M. (2013). Speech versus song:
multiple pitch-sensitive areas revealed by a naturally occurring musical illusion. Cereb Cortex 23, 249–254. doi: 10.1093/cercor/bhs003
Tuggy, D. (1993). Ambiguity, polysemy, and vagueness. Cogn. Linguist. (Includes
Cogn. Linguist. Bibliogr.) 4, 273–290. Warrier, C. M., and Zatorre, R. J. (2004). Right temporal cortex is critical for
utilization of melodic contextual cues in a pitch constancy task. Brain 127(Pt
7), 1616–1625. doi: 10.1093/brain/awh183
Zhou, L., Liu, F., Jiang, J., Jiang, H., and Jiang, C. (2019). Abnormal
neural responses to harmonic syntactic structures in congenital amusia. Psychophysiology 56:e13394. Conﬂict of Interest: The authors declare that the research was conducted in the
absence of any commercial or ﬁnancial relationships that could be construed as a
potential conﬂict of interest. Publisher’s Note: All claims expressed in this article are solely those of the authors
and do not necessarily represent those of their aﬃliated organizations, or those of
the publisher, the editors and the reviewers. Any product that may be evaluated in
this article, or claim that may be made by its manufacturer, is not guaranteed or
endorsed by the publisher. Copyright © 2021 Kim, Jin, Kim, Kim, Yi and Chung. This is an open-access article
distributed under the terms of the Creative Commons Attribution License (CC BY). The use, distribution or reproduction in other forums is permitted, provided the
original author(s) and the copyright owner(s) are credited and that the original
publication in this journal is cited, in accordance with accepted academic practice. No
use, distribution or reproduction is permitted which does not comply with these terms. Frontiers in Neuroscience | www.frontiersin.org

August 2021 | Volume 15 | Article 693629
