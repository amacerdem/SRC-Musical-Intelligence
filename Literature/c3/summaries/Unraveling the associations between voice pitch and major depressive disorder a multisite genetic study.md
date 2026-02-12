# Unraveling the associations between voice pitch and major depressive disorder: a multisite genetic study

**Authors:** Yazheng Di
**Year:** D:20
**Subject:** Molecular Psychiatry, doi:10.1038/s41380-024-02877-y

---

ARTICLE
OPEN
Unraveling the associations between voice pitch and major
depressive disorder: a multisite genetic study
Yazheng Di
1,2, Elior Rahmani3, Joel Mefford4, Jinhan Wang5, Vijay Ravi5, Aditya Gorla
6, Abeer Alwan5, Kenneth S. Kendler
7,8, Tingshao Zhu1,2✉and Jonathan Flint
9✉
© The Author(s) 2024
Major depressive disorder (MDD) often goes undiagnosed due to the absence of clear biomarkers. We sought to identify voice
biomarkers for MDD and separate biomarkers indicative of MDD predisposition from biomarkers reﬂecting current depressive
symptoms. Using a two-stage meta-analytic design to remove confounds, we tested the association between features representing
vocal pitch and MDD in a multisite case-control cohort study of Chinese women with recurrent depression. Sixteen features were
replicated in an independent cohort, with absolute association coefﬁcients (beta values) from the combined analysis ranging from
0.24 to 1.07, indicating moderate to large effects. The statistical signiﬁcance of these associations remained robust, with P values
ranging from 7.2 × 10–6 to 6.8 × 10–58. Eleven features were signiﬁcantly associated with current depressive symptoms. Using
genotype data, we found that this association was driven in part by a genetic correlation with MDD. Signiﬁcant voice features,
reﬂecting a slower pitch change and a lower pitch, achieved an AUC-ROC of 0.90 (sensitivity of 0.85 and speciﬁcity of 0.81) in MDD
classiﬁcation. Our results return vocal features to a more central position in clinical and research work on MDD. Molecular Psychiatry (2025) 30:2686–2695; https://doi.org/10.1038/s41380-024-02877-y
INTRODUCTION
Changes in human pitch and tone of speech have been noted as
an important sign of depression for over a century [1, 2]. Although
not contained in symptomatic criteria for major depressive
disorder (MDD) in DSM-III [3], DSM-IIIR [4], DSM-IV [5], or DSM-5
[6], they are found in 26 out of 28 detailed clinical descriptions of
melancholia published from 1880-1900 [1] and in 19 out of 21 of
such descriptions of depression published in the 20th century [2]. Given the current challenges in diagnosing MDD [2, 7, 8], where a
large proportion of cases (ranging from 50 to 90%) remain
untreated [9–11], the transformation of voice phenomena into
diagnostic biomarkers could aid in both clinical and research
arenas. Clinical observations describe the speech patterns of depressed
patients as slow, weak, low-pitched, and monotonous [1, 2, 12, 13]. These phenomena are typically quantiﬁed by increased pause
time, lower volume, lower pitch, and reduced pitch variability
[14–16]. Many studies have sought to develop features from pitch
as a biomarker for depression [17–26], but none have, to date,
achieved sufﬁcient accuracy and precision for clinical utility. The
large number of both vocal features and confounds [24, 25]
imposes a multi-testing burden that requires large sample sizes
which few studies have obtained [16]. Also, a critical distinction
between current mood and susceptibility to MDD on effects on
voice has never been addressed [27–29]. Furthermore, MDD is
likely heterogeneous [30, 31]: studies not accounting for this may
be underpowered [16]. Our study of the relationship between voice features and MDD
was designed to be well-powered, using thousands of subjects, to
be more robust to heterogeneity by analyzing cases with recurrent
depression of one sex only, and able to separate susceptibility to
MDD from the effect of current mood on voice features by using
genetic data. We used a large case-control study of MDD where
we could replicate ﬁndings in an independent sample, both from
China. Since, of the four groups of speech features (source,
spectral, prosodic, and formant features [16]), the association
between depression and a key component of prosody, pitch, has
repeatedly been observed [15, 16], our analysis was restricted to
examining pitch-related features. Our results return vocal features
to a more central position in clinical and research work on MDD. RESULTS
Subjects
We used recordings conducted as part of the CONVERGE [32]
(China, Oxford, and VCU Experimental Research on Genetic
Epidemiology) study (3968 cases and 4354 controls). CONVERGE
recruited only women with recurrent MDD from hospital settings
and compared them with matched controls with no history of
MDD, thus reducing heterogeneity in both genetic and vocal
Received: 3 June 2024 Revised: 3 December 2024 Accepted: 13 December 2024
Published online: 31 December 2024
1CAS Key Laboratory of Behavioral Science, Institute of Psychology, 100101 Beijing, China. 2Department of Psychology, University of Chinese Academy of Sciences, 100049
Beijing, China. 3Department of Computational Medicine, University of California Los Angeles, Los Angeles, CA, USA. 4Department of Neurology, University of California Los
Angeles, Los Angeles, CA, USA.
5Department of Electrical and Computer Engineering, University of California Los Angeles, Los Angeles, CA, USA.
6Bioinformatics
Interdepartmental Program, University of California Los Angeles, Los Angeles, CA, USA. 7Virginia Institute for Psychiatric and Behavioral Genetics, Richmond, VA, USA.
8Department of Psychiatry, Virginia Commonwealth University School of Medicine, Richmond, VA, USA. 9Department of Psychiatry and Biobehavioral Sciences, Brain Research
Institute, University of California Los Angeles, Los Angeles, CA, USA. ✉email: tszhu@psych.ac.cn; JFlint@mednet.ucla.edu
www.nature.com/mp
Molecular Psychiatry
1234567890();,:

signals [33, 34]. A summary of demographic data from cases and
controls is provided in Table S1; the relation of these to depression
is reported in earlier publications [31, 35–40]. All recordings,
obtained during diagnostic interviews, were listened to, and
segments that contained only the patient’s voice at an adequate
quality for the analyses (see the Method section in Supplementary
for details) were identiﬁed. In this study, a “segment” refers to the
longest continuous portion of an audio recording that contains
only
the
patient’s
voice,
uninterrupted
by
other
speakers. Segments are not split at pauses within the patient’s speech but
are instead deﬁned by changes in the speaker, ensuring that each
segment represents uninterrupted speech from the patient alone. It can be as short as a single word or as long as a complex
sentence or multiple sentences. This resulted in 364,929 voice
segments with a duration greater than two seconds from
7654 subjects. The selection of subjects for each component of
the study is shown in Fig. S1, which provides an overview of the
design of the project (Fig. S1a), and a PRISMA diagram to indicate
how many cases and controls were discarded at different stages
and pathways of analyses (Fig. S1b). Feature identiﬁcation
The perceptual attribute of pitch corresponds to the physical
measurement of fundamental frequency, or F0 [15]. Our interest in
prosodic features of speech, particularly pitch (hereafter referred
to as the F0) and change in pitch (ΔF0), led us to choose the
INTERSPEECH

Computational
Paralinguistics
Evaluation
(COMPARE16) feature set [41, 42]. The primary application for
the feature set has been depression detection [24, 43–47] and it
captures typical temporal information and long-term information
either statically, through the use of utterance level statistics/
functionals, or dynamically, through frame-based delta (ΔF0)
coefﬁcients, reﬂecting differences between the adjacent vectors’
feature coefﬁcients [48, 49]. Its feature extraction process is well
documented [50], with standardized and well-referenced meth-
odologies that facilitate reproducibility and validation by other
researchers in many languages (including Chinese) [51–54]. The COMPARE16 feature set contains 83 F0/ΔF0-based features,
many of which are highly correlated (Fig. S2). Implementing a
feature selection process to remove redundancy (described in
Supplementary Methods), we extracted 30 voice features (Table S2,
their distributions are in Fig. S3 and Fig. S4), providing a
comprehensive characterization of the speaker’s prosodic pat-
terns, pitch, and intonation [41, 42] We calculated statistics and
functions based on the time series of F0, and its differential values,
namely pitch change speed (ΔF0). These statistics and functions
include mean values, quartiles, range, and regression coefﬁcients,
which capture pitch trends and dynamics in speech. A two-stage meta-analysis identiﬁes 20 features associated
with MDD
Our association analysis had to account for a number of potential
confounds. Not everyone in the study spoke the same language:
60% of the subjects spoke in standard Mandarin, whereas the rest
spoke either local languages or Mandarin with local accents. This
might not matter if language differences were randomized with
respect to case status, but uneven case/control ratios between
hospitals could confound the analysis. Similarly, the quality of the
recordings varied, potentially confounding the association testing. While we made every attempt to ensure that the location of
interviews was comparable (in outpatient departments) and that
the interviews were carried out in the same way by clinically
experienced interviewers that we had trained (Supplementary
Methods), these and other, unknown confounders might impact
the voice features. We dealt with these issues as follows. First, during the process
of identifying the patients’ voice segments, we annotated
background noise and language. The noise was categorized into
ﬁve levels, and a binary indicator tagged whether the subjects’
speech was in standard Mandarin or not. We included these
features as covariates in our analyses. Second, to account for differences between hospitals, we
implemented a two-stage meta-analysis, in which associations
were ﬁrst calculated at the hospital level, including demographic
features as covariates (Table S1), noise levels, and speech
indicators, and subsequently pooling results using a random-
effects model. We selected 27 hospitals with at least 100
individuals, yielding a total subject count of N = 5681 (Fig. S1). By analyzing cases and controls within each hospital ﬁrst and then
combining the results in a meta-analysis, we alleviated the risk of
site-speciﬁc confounders. We identiﬁed 20 features signiﬁcantly
associated with MDD at a 5% FDR threshold (Table 1; a description
of the vocal features is given in Table S2). All features were
standardized (to give a standard deviation of 1) before analysis so
that beta coefﬁcients can be compared and interpreted. Eighteen
features were signiﬁcant under a family-wise error rate control
using Bonferroni (P value < 0.0017), with 14 features showing
absolute β coefﬁcients greater than 0.3. The most signiﬁcantly
associated feature is a ΔF0 measure (interquartile range; β =

## –1.07, SE = 0.07, PFDR=1.1 × 10–49). To test the sensitivity of our results to differences between
cases and controls, we compared analyses with and without the
inclusion of 20 genetic principal components (PCs). The results of
this analysis are presented in Table S3, and a comparison of the
betas with and without adjusting for genetic PCs is presented in
Fig. S5. The correlation between betas in the two analyses was
r = 0.99, P = 8.7 × 10–28. These results demonstrate a high degree
of consistency in the estimated association effects, irrespective of
the adjustment for genetic PCs. There is no overall decrease in
signiﬁcance with the inclusion of the genetic covariates, implying
that cases and controls are overall adequately matched by
location, which implicitly also means matching by accent. Replication in an independent sample
We evaluated the 20 associated features in an independent
sample. The replication sample was collected six years after the
discovery CONVERGE data, using the same selection criteria and
interview protocol (described in Supplementary Methods). The
replication sample collected data from three new hospitals, and
one that was part of the CONVERGE sample. It used none of the
same interviewers and the participants did not overlap with the
discovery sample. A description of the sample is given in Table S4. While the replication sample is smaller than the discovery sample
(1084, Fig. S1), power to detect twelve of the features was greater
than 80% (Table 1). Again, we listened to all recordings, annotated
them for quality and accent, extracted prosodic features, analyzed
the association within each hospital, and combined results by
meta-analysis. As Table 1 shows, 14 features exceeded a
Bonferroni corrected threshold of 0.0025 (0.05/20) and 16
exceeded an FDR 5% threshold. We argue that this strong
replication ﬁnding in an independent sample, excludes systematic
bias in the way recordings were made, the way interviews were
conducted, and differences in accent among subjects and
differences between hospitals. Finally, we jointly analyzed the discovery and replication
samples by meta-analysis and show the results in Table 1. Eighteen features exceeded the Bonferroni corrected threshold
and all exceeded the 5% FDR threshold. The three most
signiﬁcantly associated features were ΔF0 interquartile range
ðβ ¼ 1:07; SE ¼ 0:07; PFDR ¼ 6:8 ´ 1058Þ, which measures the
range
between
the
25th
and
75th
percentile
of
pitch
change
speed
(ΔF0),
ΔF0
maximum
ðβ ¼ 0:97; SE ¼
0:07; PFDR ¼ 1:8 ´ 1048Þ, which measures the highest value of
pitch
change
speed,
and
time
with
F0>90th
percentile
ðβ ¼ 0:80; SE ¼ 0:06; PFDR ¼ 1:3 ´ 1044Þ, which measures the
amount of time the pitch stays above the 90th percentile of its
Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

Table 1. Associations between voice pitch features and major depressive disorder. Features
Statistical functionals
CONVERGE
Replication
Combined
Beta
P
P_FDR
Beta
P
P_FDR
Power
Beta
P
P_FDR
ΔF0_iqr1-3
Interquartile range (3rd–1st)
–1.07
3.5E–51
1.1E–49
–1.09
1.46E–07

–1.07
3.4E–59
6.7E–58
ΔF0_percentile99.0
Maximum (99th percentile)
–0.97
1.2E–43
1.8E–42
–0.97
5.35E–06

–0.97
1.8E–49
1.8E–48
F0_upleveltime90
Time with F0>90th percentile
–0.80
1.5E–41
1.5E–40
–0.78
5.37E–05
0.0001

–0.80
1.9E–45
1.3E–44
ΔF0_kurtosis
Kurtosis
0.87
1.5E–39
1.1E–38
0.83
2.69E–04
0.0005

0.86
6.4E–42
3.2E–41
ΔF0_rqmean
Root quadratic mean
–0.69
6.3E–31
3.8E–30
–0.76
2.99E–04
0.0005
0.99
–0.70
6.3E–34
2.1E–33
ΔF0_quartile3
3rd quartile
–0.78
5.4E–30
2.7E–29
–0.88
1.16E–05

0.98
–0.80
4.1E–35
1.6E–34
ΔF0_minPos
Position of the minimum
–0.60
3.3E–25
1.4E–24
–0.57
7.05E–07

0.96
–0.59
7.2E–31
2.0E–30
ΔF0_amean
Mean
0.43
5.8E–20
2.0E–19
0.56
5.85E–08

0.88
0.45
3.0E–26
7.4E–26
ΔF0_linregc1
Slope of linear regression
–0.39
6.0E–20
2.0E–19
–0.55
3.12E–03
0.0042
0.88
–0.41
8.7E–21
1.5E–20
F0_range
Range
0.57
1.0E–19
3.1E–19
0.48
2.35E–03
0.0034
0.88
0.55
3.7E–22
8.2E–22
ΔF0_maxPos
Position of the maximum
–0.55
1.8E–19
4.9E–19
–0.61
1.36E–03
0.0023
0.87
–0.56
5.4E–22
1.1E–21
ΔF0_qregc1
1st quadratic regression coefﬁcient
0.38
1.0E–17
2.6E–17
0.47
1.04E–04
0.0002
0.83
0.40
9.2E–22
1.7E–21
ΔF0_ﬂatness
Flatness
–0.43
5.5E–14
1.3E–13
–0.39
2.85E–05
0.0001
0.68
–0.42
6.6E–18
1.0E–17
F0_lpc2
2nd linear prediction coding coefﬁcient
0.33
1.3E–09
2.7E–09
0.41
2.22E–05
0.0001
0.44
0.34
6.0E–13
8.6E–13
F0_lpc4
4th linear prediction coding coefﬁcient
–0.28
4.9E–09
9.8E–09
–0.25
1.07E–01
0.1259
0.4
–0.27
2.7E–09
3.6E–09
F0_kurtosis
Kurtosis
0.23
1.1E–05
2.0E–05
0.30
1.81E–03
0.0028
0.19
0.24
3.6E–08
4.5E–08
F0_lpc0
0th linear prediction coding coefﬁcient
–0.29
9.0E–05
1.6E–04
–0.39
1.97E–02
0.0246
0.14
–0.30
6.1E–06
7.2E–06
ΔF0_risetime
Time with which ΔF0 is rising
–0.15
4.1E–04
6.9E–04
–0.25
1.39E–01
0.1539
0.1
–0.16
8.9E–05
9.9E–05
F0_ff0_maxSegLen
Maximum length of voiced segments with F0 > 0
0.19
6.3E–03
1.0E–02
0.12
2.69E–01
0.2837
0.05
0.19
3.2E–03
3.4E–03
F0_rqmean
Root quadratic mean
0.14
9.0E–03
1.3E–02
0.00
9.97E–01
0.9974
0.05
0.12
1.7E–02
1.7E–02
The table shows the names of the prosodic phenotypes, explained in Table S2. Beta values (Beta) P values (P) and FDR corrected (FDR) are from the logistic regression analysis. Beta coefﬁcients are derived from
analyses of normalized voice features (with standard deviation of 1). Results from the CONVERGE study and an independently collected replication are shown. The column headed ‘Power’ shows the power of the
replication study to detect the effect found in the discovery sample. The last three columns (‘Combined’) are results from a meta-analysis of CONVERGE and the Replication sample. Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

range. We found that there was no signiﬁcant heterogeneity in the
association effects between Mandarin speakers and non-Mandarin
speakers (Supplementary Results). Differences between case and control interviews do not
account for the associations
We considered next one additional potential confound: the
possible impact of the questions asked at interview. The interview
for cases is typically more than twice as long as for controls, as we
ask about past occurrences of depression and associated stressful
life events. Could the emotion associated with this questioning
alter speech in such a way as bias our ﬁndings? We conducted a
sensitivity analysis on responses to neutral questions to check if
the effects remained consistent across contexts. We selected two questions from the demographic section of the
interview based on their high response rates (Table S5) and neutral
nature. These questions (D2. A: “What is your date of birth?” and D10:
“How much do you weigh while wearing indoor clothing?”) were
chosen because they are unlikely to trigger emotional differences
between MDD cases and controls. We identiﬁed 533 subjects with
voice responses to question D2. A and 617 to question D10. The
average segment durations were 3.37 s (SD = 3.05), and 8.47 s
(SD = 2.69), respectively. For each question, we used the corre-
sponding segments to extract the 16 pitch features that were
associated with MDD in our main analysis. Using the two-stage
meta-analysis method again, we re-estimated their associations. Due to the small sample sizes, power to detect effects was low so
we used a one-sided binomial sign test to test consistency in the
direction of association effects between the two analyses. The estimated association effects in context-constrained analysis are
reported in Table S6. We found that for question D10, three out of 16
pitch features maintained signiﬁcant associations with MDD at
FDR < 0.05. Remarkably, 15 out of 16 features showed the same
direction of association effects, a fraction signiﬁcantly higher than
chance (Binomial P = 0.00026). For D2. A, despite the average duration
being only 3.37 s, three features achieved nominal signiﬁcance for
associations (uncorrected P < 0.05), and 12 out of 16 pitch features
showed
consistent
directions
of
association
effects
(Binomial
P = 0.038). In total, 12 out of 16 voice features showed consistent
directions of association effects across all four analyses. We conclude
that the ﬁndings from the main analyses are not biased by the context
of the interview. As a summary for these analyses, Fig. S6 shows the effect sizes
(beta coefﬁcients) and the 95% conﬁdence intervals for the
association between 16 voice F0/ΔF0 features and MDD in the
discovery (CONVERGE), replication and single segment analyses. Genetic correlations between pitch features and MDD
Cases for the CONVERGE study were identiﬁed as those who have
a history of recurrent MDD, and though all were ascertained
through hospitals, many were in remission. This raises the
important question as to what the association with voice features
represents: does it reﬂect their current low mood, compared to
controls, or does it reﬂect their history of MDD? We addressed this
question in the following way. To see if any voice features correlated with current mood, we
used a standard assessment of current mood for subjects, the
depressive symptom checklist (SCL) [55]. These data were only
available for the replication sample. The distributions of SCL scores
for cases and controls are presented in Fig. S7. Of the 16 pitch
features,

showed a signiﬁcant
association
with current
depressive symptoms, after FDR correction (Table 2). These results conﬁrm that most of the features we found to be
associated with MDD are correlated with current mood (the
relatively smaller sample for this analysis cannot exclude the
possibility that all features are thus associated). To examine
whether the association reﬂected a genetic effect common to
both variability in vocal features and susceptibility to MDD we
estimated the SNP-based heritability for each of the 16 pitch
features (this analysis was carried out with CONVERGE data, the
only group for which there are genetic data [32]). Results are
presented in Table 3. Four features were heritable at FDR < 0.05. We repeated the heritability analyses adjusting for more genetic
PCs to determine whether population structure might contribute
to the correlation and found that the heritability remained
signiﬁcant even after adjusting for as many as 60 genetic PCs
(Table S7). While we cannot rule out the possibility that all vocal
features are to some extent heritable (our sample size is too small
to conﬁdently detect heritabilities of less than 10%), Table 3 shows
that SNP-based heritability varies signiﬁcantly: the estimated
conﬁdence interval of the heritability for two, ΔF0_maxPos and
ΔF0_qregc1, lie outside those for ΔF0_iqr1-3. The low heritability
of these features indicates the genetic effects are unlikely to be
the only contributing factor to the association with MDD. We did
not ﬁnd any genome-wide signiﬁcant SNPs for these heritable
features (Supplementary Results), presumably owing to the
limited sample size. We estimated the genetic correlation with MDD for the four
features with evidence of heritability and found that three ΔF0
features had signiﬁcant genetic correlations (Table 3). They were: (1)
the interquartile range (IQR1-3), quantifying the variation of speed
in pitch change; (2) the kurtosis, signaling the extremity of speed in
pitch change; and (3) the maximum, representing the speed of the
fastest pitch change. There was no detectable genetic correlation
with MDD for one heritable feature, ΔF0_kurtosis. Again, while we
cannot exclude the possibility of some degree of genetic correlation
for this and other features, our results indicate that genetic effects
alone cannot explain the association with MDD for all features. The
vocal features index a composite of heritable and non-heritable
contributions to mood change. Associations between pitch features and MDD symptoms, risk
factors, and comorbidities
The deep set of phenotypes available in CONVERGE, which
includes MDD symptoms, environmental risk factors, comorbid
disease, and suicidality, permit us to explore other associations for
Table 2. Voice pitch features associated with SCL scores. Feature
Beta
SE
P
P_FDR
ΔF0_maxPos
–0.222
0.04
3.4E–08
5.5E–07
ΔF0_percentile99.0 *
–0.296
0.074
6.7E–05
5.3E–04
ΔF0_rqmean
–0.238
0.067
3.6E–04
0.001
ΔF0_quartile3
–0.286
0.081
3.9E–04
0.001
F0_upleveltime90
–0.246
0.066
1.9E–04
0.001
ΔF0_iqr1-3 *
–0.309
0.097
0.001
0.004
ΔF0_kurtosis *
0.225
0.081
0.005
0.01
F0_lpc2
0.118
0.042
0.005
0.01
ΔF0_amean
0.133
0.053
0.01
0.02
F0_kurtosis *
0.097
0.041
0.02
0.03
F0_range
0.128
0.057
0.02
0.03
ΔF0_ﬂatness
–0.116
0.056
0.04
0.05
ΔF0_qregc1
0.104
0.062
0.09
0.12
ΔF0_linregc1
–0.103
0.067
0.12
0.14
ΔF0_minPos
–0.13
0.086
0.13
0.14
F0_lpc0
–0.047
0.104
0.65
0.65
The associations between pitch features and SCL scores were estimated in
the replication sample using a two-stage meta-analysis. Asterisks indicate
heritable features, from Table 3. Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

the vocal features associated with MDD. For these exploratory
analyses we included all 30 voice features and tested association
with 33 traits (detailed in Table S8). The results of within-case two-
stage meta-analysis are shown in Table S8. We categorized the
traits into six classes (MDD symptoms, MDD clinical features,
suicidal features, co-morbid psychiatric disease, neuroticism and
stressful life events) as we were interested in determining the
effects on these categories.
110 associations are signiﬁcant at an uncorrected 5% signiﬁ-
cance threshold (where 50 are expected by chance). Surprisingly,
features assessing stressful life events showed the greatest
enrichment of low P values. After applying a Bonferroni correction
for the 990 tests (P < 0.05/990 = 5.1 × 10–5) six associations were
signiﬁcant, four for stressful life events, one for the personality trait
neuroticism, and one for premenstrual syndrome score. Two
features replicated (corrected threshold P < 0.05/6 = 0.008). Both
associations were between the total number of stressful life events
and ΔF0 features, including the IQR1-3 of ΔF0 (16 hospitals in
CONVERGE, total N = 2,064, β = - 0.21, SE = 0.03, uncorrected
P=1.9 × 10–11; four hospitals in the replication, total N = 295, β =
–0.20, SE = 0.07, uncorrected P = 0.0078) and maximum of ΔF0
(16 hospitals in CONVERGE, total N = 2064, β = –0.19, SE = 0.03,
uncorrected P = 6.5 × 10–10; four hospitals in the replication, total
N = 295, β = –0.20, SE = 0.08, uncorrected P = 0.0074). Classiﬁcation performance
If the voice features are to have any clinical utility, they must not
just be associated with MDD, but they must predict it accurately. We took advantage of access to our two independently collected
samples (discovery and replication), using the discovery group for
training data (n = 7654) and the replication sample (n = 1189) to
test the classiﬁcation performance. We compared the classiﬁcation performance of a full model against
a null model. The null model was a logistic regression (LR) model
trained on the covariates. We then trained a full model using the
covariates together with the identiﬁed voice features in discovery,
based on the same LR method. Table 4 illustrates these comparisons. Integrating voice data signiﬁcantly enhanced the predictive accuracy of
our models. Adding voice features to the LR model increased the AUC-
ROC from 0.70 to 0.83 and the accuracy from 0.63 to 0.76. We then tested whether the classiﬁcation results were robust to
different machine learning methods. We evaluated this on three
established methods suitable for our dataset, support vector
machine (SVM), extreme gradient boosting (XGBoost), and multi-
layer perceptron (MLP). Results improved prediction, with XGBoost
delivering an AUC of 0.90 (sensitivity of 0.85, and speciﬁcity of
0.81). Figure 1 plots the ROC curves for a null model (using
covariates only to classify depression) and the four models using
voice features. The precision-recall curve of these models are in
Fig. S8. DISCUSSION
We set out to ﬁnd voice pitch features associated with MDD. By
using a large and homogeneous case-control cohort, a two-stage
meta-analysis and an independent replication, we provide robust
evidence that certain pitch features distinguished MDD cases from
matched controls. The associated features were a slower change
in pitch and a particularly uneven distribution of these variations. Features measuring the variability and extremity of pitch change
speed were heritable and had genetic correlations with MDD,
which we interpret to mean that at least some of the association
between variation in pitch and susceptibility to depression is
genetic in origin. Classiﬁcation of those with and without
depression, based on vocal features, was achieved with an AUC
of 0.90, highlighting the potential use of these features as
biomarkers for MDD detection and secondary prevention. Establishing a robust, replicable association between voice
features and MDD is difﬁcult because of the numerous confounds
that could potentially introduce systematic differences between
cases and controls and thus corrupt our ﬁndings. We addressed
this concern by using a large, and as far as possible homogeneous
sample of depression. Our study used only women with recurrent
MDD in a population where many comorbid disorders, such as
smoking, alcohol, and drug abuse, are rare or practically non-
existent [32]. By adopting a two-stage meta-analysis to take into
account variation between hospitals, and using an independent
replication sample, our results are unlikely to be explained by
differences between hospitals, location, accent, quality of the
recording or the interview questions. Our ﬁndings support and extend previous studies which have
indicated potential links between pitch patterns and MDD, but
were limited by smaller sample sizes or more heterogeneous
cohorts [15, 16]. First, our large sample size provided adequate
Table 3. Heritable voice pitch features and their genetic correlation with MDD. Feature
SNP heritability
Genetic Correlation with MDD
h2

## 95% CI

P
P_FDR
rg

## 95% CI

P
P_FDR
ΔF0_iqr1-3
0.171
(0.071, 0.272)
0.0004
0.006
–0.45
(–0.77, –0.13)
0.03
0.04
F0_kurtosis
0.134
(0.035, 0.234)
0.004
0.03
–0.3
(–1.14, 0.54)
0.2
0.2
ΔF0_kurtosis
0.125
(0.025, 0.225)
0.007
0.03
0.55
(0.23, 0.88)
0.01
0.02
ΔF0_percentile99.0
0.121
(0.022, 0.221)
0.008
0.03
–0.7
(–1.28, –0.11)
4.2E–05
0.0002
ΔF0_ﬂatness
0.105
(0.007, 0.203)
0.02
0.05
F0_lpc2
0.093
(–0.005, 0.191)
0.03
0.08
ΔF0_rqmean
0.058
(–0.040, 0.157)
0.12
0.25
F0_upleveltime90
0.044
(–0.053, 0.141)
0.18
0.32
ΔF0_minPos
0.03
(–0.067, 0.128)
0.27
0.40
ΔF0_amean
0.024
(–0.073, 0.120)
0.31
0.40
ΔF0_quartile3
0.019
(–0.078, 0.116)
0.35
0.40
F0_lpc0
0.019
(–0.079, 0.116)
0.35
0.40
F0_range
0.001
(–0.096, 0.098)
0.49
0.49
ΔF0_linregc2
–0.004
(–0.101, 0.093)
0.47
0.49
ΔF0_qregc1
–0.028
(–0.124, 0.068)
0.28
0.40
ΔF0_maxPos
–0.065
(–0.160, 0.030)
0.09
0.21
Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

power to test several pitch features from a standardized features
set, providing more ﬁne-grained quantitative evidence for the
descriptions of the monotonous speech pattern in MDD than in
previous studies. Previous studies have found that depressed
people speak more slowly with lower pitch and decreased
variability [16, 25]. Here, our study showed MDD was negatively
associated with features measuring how fast pitch changes (the
maximum, the 3rd quartile, and the root quadratic mean of ΔF0, Table 1), indicating that the reduced rate of change in pitch is a
characteristic of voice in MDD patients. We also found that MDD
patients spend less time in their upper vocal range (Time with
F0>90th percentile, Table 1), afﬁrming the “low-pitched” pattern. Second, our results indicate that MDD’s pitch dynamics involve
more than reduced variability, showing a broader pitch range and
more extreme values (range and kurtosis of F0, Table 1). Our
analysis also revealed an uneven distribution of the speed with
which an MDD patient’s pitch changes, as shown by the negative
association between MDD and the ﬂatness of ΔF0 and the positive
association with the kurtosis of ΔF0 (Table 1). Overall, these
various features enrich our understanding of pitch dynamics,
demonstrating a pattern of slower change in pitch, yet with more
frequent occurrences of extreme values and pitch change speed. Third, our research examined the relationship between voice
features and the effects of current low mood, and the effects of
susceptibility to MDD. Some vocal features might be more
reﬂective of a person’s underlying propensity towards developing
MDD, while others could be more indicative of a current
depressive state. We found that some vocal features were indeed
heritable, but still correlated with changes in current mood:
individuals with an increased genetic risk of MDD may have a
smaller value of speed for the fastest pitch change, thus being
unable to speak as fast as those without depression. They may
show a narrower IQR of pitch change speeds and more frequently
occurring extreme changes of pitch (higher kurtosis). Shared
genetic effects exist between at least some ΔF0 features and MDD,
but while our low power to detect heritability and genetic
correlations raises the possibility that the other features may also
be associated in this way, our ﬁndings are consistent with vocal
features’ association with both current low mood and suscept-
ibility to MDD. We also found that two heritable voice features were associated
with the number of stressful life events. The reason for these
associations is unclear, but suggests the possibility that stressful
life events reveal a latent predisposition to depression [56, 57],
evidenced through a change in vocal features. It is interesting to consider physiological interpretations of our
ﬁndings. Possibly, changes in pitch could reﬂect tiredness, or the
psychomotor retardation that characterizes an episode of MDD.
0.0
0.2
0.4
0.6
0.8
1.0
False Positive Rate
0.0
0.2
0.4
0.6
0.8
1.0
True Positive Rate
LR-Covar (AUC = 0.70)
LR-(Voice+Covar) (AUC = 0.83)
SVM-(Voice+Covar) (AUC = 0.86)
MLP-(Voice+Covar) (AUC = 0.86)
XGBoost-(Voice+Covar) (AUC = 0.90)
Fig. 1
Receiver operating characteristic (ROC) curve. The ﬁgure shows the ROC for four models for predicting depression from voice
features, and a null model, a logistic regression model trained on demographic covariates only (LR-Covar). The full models are logistic
regression (LR), support vector machine (SVM), multi-layer perceptron (MLP), and extreme gradient boosting (XGBoost), trained on voice and
covariates (Covar+Voice). AUC: area under the curve. Table 4. Classiﬁcation performance using the identiﬁed voice pitch features. Model
Method
Feature
AUC-ROC
AUC-PR
Sensitivity
Speciﬁcity
F1 Score
Accuracy
NULL
LR
Demographic Covariates
0.70
0.62
0.75
0.53
0.63
0.62
FULL
LR
Demographic Covariates + Voice
0.83
0.77
0.81
0.70
0.73
0.75
SVM
Demographic Covariates + Voice
0.86
0.80
0.88
0.67
0.75
0.76
MLP
Demographic Covariates + Voice
0.85
0.80
0.86
0.69
0.75
0.76
XGBoost
Demographic Covariates + Voice
0.90
0.88
0.85
0.81
0.80
0.82
LR Logistic Regression, XGBoost Extreme Gradient Boosting, SVM Support Vector Machine, MLP Multi-layer Perceptron. Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

We do not have physiological assessments of our subjects that
characterize these features (all of our data are from interviews, and
therefore reﬂect the subjects’ perceptions) but it is worth pointing
out that at some level physiological and psychological contribu-
tions will be confounded. For example retardation of thought
(psychological) can result in a slowness of expression (motor
effect), so that in many cases the distinction may not be relevant. Could the features we identiﬁed provide clinically useful
predictions? A key aim of our research was to ﬁnd vocal
biomarkers that could take on this role. Applying XGBoost to
the independent test dataset we obtained an AUC-ROC of 0.90,
and a level of accuracy indicating that the features could be useful
in identifying cases of MDD. We applied three models for
classiﬁcation (SVM, XGBoost, and MLP) because relying on a
single model would not provide sufﬁcient evidence for the
robustness and generalizability of the voice features across
different machine learning approaches. SVM excels at handling
high-dimensional data and constructing optimal decision bound-
aries, but it assumes that the data is linearly separable in the
kernel-transformed feature space [58]. If the relationship between
the features and depression states is highly non-linear, SVM may
struggle to ﬁnd an optimal solution. In contrast, XGBoost [59], an
ensemble
of
decision
trees,
can
capture
complex
feature
interactions and handle non-linear relationships. However, it
may not be as effective as deep learning models like MLP in
capturing hierarchical representations of the data. MLP, with its
deep learning architecture, can learn intricate patterns and
hierarchical
representations,
but
it
is
prone
to
overﬁtting,
particularly when the dataset is small or the network is overly
complex [60]. By applying the voice features and geographical
covariates to all three models, we provide a robust justiﬁcation for
the usefulness and generalizability of the voice features in
depression classiﬁcation. Our results should be assessed with respect to several
limitations. First, we only recruited Han Chinese women with
recurrent MDD. Our results may not extrapolate to men, those
with single episode MDD, or to non-Chinese speakers. Second, our
analysis focused solely on pitch features, and future studies should
explore other feature types. Neural network-based approaches,
which can learn directly from raw audio signals, also hold promise
for detecting depression but face challenges in portability and
interpretability, particularly when addressing complex confound-
ing factors [61] (Supplementary Results). Third, although our
context-constrained analysis demonstrates that the signals we
found are persistent across speech content, we cannot separate
pitch differences due to word choice from pitch differences due to
emotional content without additional experiments directly con-
trolling the linguistic context. While we don’t know how far results will generalize outside the
female Chinese cohort, the ﬁndings reveal that vocal features can
be used to identify MDD cases with high accuracy and we expect
that with improvements, such as the inclusion of additional voice
features, even higher predictive accuracy may be obtainable. Our
hope is that these ﬁndings will further encourage efforts to assess
changes in the voice, long understood by experienced clinicians
to be a valuable sign, returning it to a more central position in
clinical and research work on MDD. METHODS
Participants
We used data from the CONVERGE [32] study, in which women with
recurrent MDD were recruited from 58 provincial mental health centers
and psychiatric departments of general medical hospitals in 45 cities and
23 provinces of China. Participants were aged between 30 and 60, with
two or more episodes of MDD that met the DSM-IV criteria [5], with the ﬁrst
episode occurring between ages 14–50. Cases were excluded if they had
pre-existing bipolar disorder, nonaffective psychosis, smoking/nicotine
dependence (alcohol and substance abuse were virtually absent in this
study, so it was not assessed), or mental retardation. Control subjects,
screened to exclude a history of MDD, were recruited from patients
undergoing minor surgical procedures at general hospitals and individuals
attending local community centers. The replication study [43] used the
same inclusion/exclusion criteria as CONVERGE, and recruited samples
from 20 different hospitals in China, with a ﬁnal sample size of 1189
(Fig. S1). This study was approved by Institutional Review Boards at UCLA, Bio-x Center, Shanghai Jiao Tong University (M16033), and local hospitals. All participants provided written informed consent. Data collection
All subjects went through a semi-structured interview using a computer-
ized assessment system as outlined previously [43] and described in
Supplementary Methods. Recordings for cases were obtained in outpatient
clinics. Controls were recorded in outpatient clinics and in community
health centers. Recordings were not standardized and varied in quality and
content. All participants provided DNA samples for genetic analysis. Details
of DNA sequencing and genotype imputation have been previously
reported [32] and described brieﬂy in Supplementary Methods. Covariates
The covariates were ﬁve demographic variables and two recording quality
variables. The demographic variables were age, education level, occupa-
tion, marital status, and social class. The recording quality referred to noise
level and accent. The noise level and accent label were determined
subjectively by the listeners during the process of identifying the patients’
voice segments. The noise was categorized into four levels: (1) No noise; (2)
Slight noise but the subject’s speech was clear; (3) Noise present but the
content of the subject’s speech could be clearly heard; (4) High noise levels
and unclear speech. Note that noise level 4 means that the speech,
although difﬁcult to understand, can still be comprehended with extra
effort. And samples were excluded during quality controls stage if the
speech is not able to comprehended at all. The accent was a binary label
that indicated whether the subjects’ speech was in standard Mandarin
or not. Voice data preprocessing
In total, 8322 subjects the subjects recruited in CONVERGE had interview
recordings (Fig. S1). To obtain the subjects’ utterances, a group of
undergraduates listened to the recordings to identify any voice segments
from the subjects with a duration >2 s. Audio samples were excluded
where the noise was so prominent that the content of the subject’s speech
could not be understood, which yielded 7654 subjects with available
segments. All segments from the same subject were concatenated in the
order in which they occur in the interview and down sampled to 8 kHz. Two postgraduate psychological students listened to all the segments to
ensure that no speech voice other than the subjects was included in the
segments and that no words were cut off mid-way. The preprocessing procedure in the replication study was the same as in
CONVERGE. Of the initially recruited 1301 participants (551 cases),
1189 subjects (including 490 cases) had available voice segments (Fig. S1). All segments from the same subject were concatenated into one, to extract
voice features for replicating the association between voice and MDD and
identifying the voice features associated with SCL (see distribution of the
audio segment length in Fig. S9). The speech segments in the replication
study were further annotated to indicate the speciﬁc question that
prompted each spoken response (Table S5). This additional level of data
analysis was introduced to better understand the relationship between the
interview content and the participants’ speech patterns. We additionally
extracted the same voice features on the non-concatenated segments
corresponding to a single question for a sensitivity analysis, which we
referred to as, the context-constrained analysis (described below). Voice features
We used the INTERSPEECH 2016 Computational Paralinguistics Evaluation
[41, 42]. Calculations were implemented in the openSMILE python package
v2.4.2 [62] and described in Supplementary Methods. Given that many of
the features were highly correlated (for example, the arithmetic and root-
quadratic mean of F0, as shown in Fig. S2), we removed redundant
features (described in Supplementary Methods), resulting in a set of 15 F0-
based features and 15 ΔF0-based features. We provide in Supplementary
Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

Table S2 technical deﬁnitions of the 30 features used, along with non-
technical explanations of what each feature measures. Two-stage meta-analysis
We used a two-stage meta-analytic framework to take into account
differences between hospitals. In the ﬁrst stage, for each hospital a linear
regression model was ﬁtted for each F0-related feature as the dependent
variable using MDD and covariates as the predictor variables. We applied
rank-based inverse normal transformation to the voice features. At stage 2,
beta coefﬁcients for MDD and standard errors from stage 1 were pooled
using random-effects meta-analysis [63], assuming that the true effect sizes
in different sites are not exactly the same but are drawn from a distribution
of effect sizes. P values were FDR-adjusted [64]. In the second stage, we
repeated the analyses in four hospitals with sample sizes ≥100 (N = 1084, Fig. S1). We performed the same procedure as in the two-stage meta-
analysis above. We combined results from both discovery and replication
cohorts using random-effects meta-analysis [63]. Heritability and genetic correlations
Heritability and genetic correlations were estimated on the 7654 subjects
in CONVERGE (Fig. S1). The SNP-based heritability used a generalized REML
(restricted maximum likelihood) method implemented in LDAK [65]. We
applied rank-based inverse normal transformation to the voice features
and incorporated the above covariates and 20 genetic PCs. P values were
FDR-adjusted. For heritable voice features, we estimated their genetic
correlation with MDD, adjusting for these same covariates and 20 genetic
PCs. The genetic correlation was calculated through a bivariate GREML
analysis implemented in GCTA [66, 67]. P values were FDR-adjusted based
on the number of heritable voice features. Associations between pitch features and current mood
To identify biomarkers for current mood, subjects in the replication cohort
were given a 16-item, self-administered questionnaire assessing the
severity of depression-related symptoms on a ﬁve-point distress scale
over the past 30 days (subscales for depression symptom checklist, SCL)
[55]. We used the same two-stage meta-analysis method to estimate the
association between the 16 voice features and SCL scores. All four hospitals
from the replication cohort with sample sizes ≥100 were selected
(N = 1084, Fig. S1). At stage 1, for each hospital, a linear regression model
was ﬁtted for each pitch feature as the dependent variable using SCL
scores and the covariates as the predictor variables. At stage 2, beta
coefﬁcients for SCL and standard errors from stage 1 were pooled using
random-effects meta-analyses [63]. SCL scores were standardized using
rank-based inverse normal transformation. P values were FDR-adjusted. Classiﬁcation model
We employed a logistic regression model using seven covariates (age,
education level, occupation, marital status, social class, noise level, and
accent) to establish a null model. Full models that incorporated both these
covariates and voice features were then developed. We included all 20
voice features identiﬁed as associated with MDD during the discovery
stage, including those not replicated. We used samples available in the
discovery group for training data (n = 7654). For the test data set we used
the replication sample (n = 1189). There was no re-estimation of weights in
the test sample. We compared the results of the full model with the null model based on
logistic regression. Then we tested the classiﬁcation performances using
SVM, XGBoost, and MLP as the classiﬁers. The performance of models was
evaluated across several metrics: accuracy, sensitivity, speciﬁcity, AUC-ROC, AUC-PR, and F1-score. To identify the best hyperparameters for each
model, a grid search with 5-folds cross-validation was employed on the
training dataset. The above process was implemented in python with
package scikit-learn [68] v1.2.2 and xgboost [59] v2.0.3. Associations between pitch features and MDD symptoms, risk
factors, and comorbidities
We examined the relationship between the 30 voice F0/ΔF0 features with
33 variables related to MDD, including eight risk factor variables, 11
comorbidity variables, seven symptoms, three variables about suicidality,
age of onset, number of MDD episodes, neuroticism, and premenstrual
syndrome score (summarized in Table S8). We again employed the two-
stage meta-analysis procedure. At stage 1, for each hospital, a multivariate
linear regression model was ﬁtted for each pitch feature as the dependent
variable using one of the above variables and covariates as the
independent variables. At stage 2, we used the Q statistics to measure
the heterogeneity of the pooled beta coefﬁcients and standard errors. If
the heterogeneity test is signiﬁcant (P < 0.05), we then used the random-
effects model for meta-analyses, otherwise we used ﬁxed-effects [64]. We
applied a Bonferroni correction to obtain a 5% signiﬁcance threshold. Due
to the high endorsement rates for certain variables within some hospitals,
the hospitals included in the meta-analysis varied depending on the
variable being analyzed (for example, if all cases from one hospital did not
have suicidal attempts, this hospital would be excluded for the analysis of
suicidal attempts at stage 1). We reported the number of hospitals and
sample size for each association along with the meta-results. Context-constrained analysis
We counted the total number of available voice segments for each question
in the replication cohort and selected the two most frequently answered
questions from the demographic section of the interview: D2. A (“What is
your date of birth?”) and D10 (“How much do you weigh while wearing
indoor clothing?”). For each question, we used the corresponding segments
to extract the 16 voice features that were associated with MDD in our
previous analysis. Finally, we re-assessed the associations between these
voice features and MDD through the two-stage meta-analysis method. The
limited voice duration and small sample size reduced power to detect a
signiﬁcant signal. We applied the one-sided binomial sign test to determine
whether the number of voice features demonstrating consistent directions
of association effects between the concatenated segments and the context-
constrained segments was greater than expected by chance (that is, a one-
sided test of whether this fraction is greater than 0.5).

## DATA AVAILABILITY

Site-level summary statistics necessary for generating the ﬁnal meta-analysis results,
as well as labels and model predictions required to reproduce the ROC and precision-
recall curves are available from the corresponding author upon reasonable request.

## CODE AVAILABILITY

Scripts to run the two-stage meta-analysis and classiﬁcation modeling are available
from the corresponding author upon reasonable request. REFERENCES

### 1. Kendler KS. The genealogy of major depression: symptoms and signs of mel-

ancholia from 1880 to 1900. Mol Psychiatry. 2017;22:1539–53.

### 2. Kendler KS. The phenomenology of major depression and the representativeness

and nature of DSM criteria. AJP. 2016;173:771–80.

### 3. American Psychiatric Association. Diagnostic and Statistical Manual of Mental

Disorders, Third Edition. Washington, D. C: American Psychiatric Association; 1980.

### 4. American Psychiatric Association. Diagnostic and Statistical Manual of Mental

Disorders, Revised Third Edition. Washington, D. C: American Psychiatric Asso-
ciation; 1987.

### 5. American Psychiatric Association. Diagnostic and statistical manual of mental

disorders, Fourth Edition. Washington, D. C: American Psychiatric Association;
1994.

### 6. American Psychiatric Association. Diagnostic and statistical manual of mental

disorders (DSM-5®). Washington, D. C: American Psychiatric Association; 2013.

### 7. Lux V, Kendler KS. Deconstructing major depression: a validation study of the

DSM-IV symptomatic criteria. Psychol Med. 2010;40:1679–90.

### 8. Hyman SE. Can neuroscience be integrated into the DSM-V? Nat Rev Neurosci.

2007;8:725–32.

### 9. Kessler RC, Berglund P, Demler O, Jin R, Koretz D, Merikangas KR, et al. The

epidemiology of major depressive disorder results from the national comorbidity
survey replication (NCS-R). JAMA. 2003;289:3095–105.

### 10. Lu J, Xu X, Huang Y, Li T, Ma C, Xu G, et al. Prevalence of depressive disorders and

treatment in China: a cross-sectional epidemiological study. Lancet Psychiatry.
2021;8:981–90.

### 11. Thornicroft G, Chatterji S, Evans-Lacko S, Gruber M, Sampson N, Aguilar-Gaxiola S,

et al. Undertreatment of people with major depressive disorder in 21 countries. Br J Psychiatry. 2017;210:119–24.

### 12. Guislain J Orales sur Les Phrénopathies, ou Traitê Thêorique Et Pratique Des

Maladies Mentales: Cours Donné A La Clinique Des Êtablissements D’Aliénés A
Gand. Vol. 1. Paris, & Bonn,: Gand; 1852. Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

### 13. Kraepelin E Manic-depressive insanity and paranoia. Edinburgh: E. & S. Living-

stone; 1921.

### 14. Sobin C Psychomotor Symptoms of Depression. A m J Psychiatry. 1997;15.

### 15. Cummins N, Scherer S, Krajewski J, Schnieder S, Epps J, Quatieri TF. A review of

depression and suicide risk assessment using speech analysis. Speech Commun.
2015;71:10–49.

### 16. Low DM, Bentley KH, Ghosh SS. Automated assessment of psychiatric disorders

using
speech: A
systematic
review. Laryngoscope
Investig
Otolaryngol.
2020;5:96–116.

### 17. Nilsonne Å. Acoustic analysis of speech variables during depression and after

improvement. Acta Psychiatr Scand. 1987;76:235–45.

### 18. Nilsonne Å. Speech characteristics as indicators of depressive illness. Acta Psy-

chiatr Scand. 1988;77:253–63.

### 19. Mundt JC, Snyder PJ, Cannizzaro MS, Chappie K, Geralts DS. Voice acoustic

measures of depression severity and treatment response collected via interactive
voice response (IVR) technology. J Neurolinguist. 2007;20:50–64.

### 20. Mundt JC, Vogel AP, Feltner DE, Lenderking WR. Vocal acoustic biomarkers of

depression severity and treatment response. Biol Psychiatry. 2012;72:580–7.

### 21. Kuny S, Stassen HH. Speaking behavior and voice sound characteristics in

depressive patients during recovery. J Psychiatr Res. 1993;27:289–307.

### 22. Cannizzaro M, Harel B, Reilly N, Chappell P, Snyder PJ. Voice acoustical mea-

surement of the severity of major depression. Brain Cogn. 2004;56:30–5.

### 23. Alpert M, Pouget ER, Silva RR. Reﬂections of depression in acoustic measures of

the patient’s speech. J Affect Disord. 2001;66:59–69.

### 24. Pan W, Flint J, Shenhav L, Liu T, Liu M, Hu B, et al. Re-examining the robustness of

voice features in predicting depression: Compared with baseline of confounders. Li Z, editor. PLoS ONE. 2019;14:e0218172.

### 25. Wang J, Zhang L, Liu T, Pan W, Hu B, Zhu T. Acoustic differences between healthy

and depressed people: a cross-situation study. BMC Psychiatry. 2019;19:300.

### 26. Schultebraucks K, Yadav V, Shalev AY, Bonanno GA, Galatzer-Levy IR. Deep

learning-based classiﬁcation of posttraumatic stress disorder and depression
following trauma utilizing visual and auditory markers of arousal and mood. Psychol Med. 2022;52:957–67.

### 27. Di Y, Wang J, Liu X, Zhu T. Combining polygenic risk score and voice features to

detect major depressive disorders. Front Genet. 2021;12:2451.

### 28. Flint J The genetic basis of major depressive disorder. Mol Psychiatry [Internet].

### 2023 Jan 26 [cited 2023 Jan 31]; Available from: https://www.nature.com/articles/

s41380-023-01957-9

### 29. Hasler G, Drevets WC, Manji HK, Charney DS. Discovering endophenotypes for

major depression. Neuropsychopharmacol. 2004;29:1765–81.

### 30. Kendler KS, Aggen SH, Neale MC. Evidence for multiple genetic factors under-

lying DSM-IV criteria for major depression. JAMA Psychiatry. 2013;70:599–607.

### 31. Peterson RE, Cai N, Dahl AW, Bigdeli TB, Edwards AC, Webb BT, et al. Molecular

genetic analysis subdivided by adversity exposure suggests etiologic hetero-
geneity in major depression. AJP. 2018;175:545–54.

### 32. CONVERGE consortium. Sparse whole-genome sequencing identiﬁes two loci for

major depressive disorder. Nature. 2015;523:588–91.

### 33. Andrianopoulos MV, Darrow KN, Chen J. Multimodal standardization of voice

among four multicultural populations: fundamental frequency and spectral
characteristics. J Voice. 2001;15:194–219.

### 34. Kendler KS, Gardner C, Neale M, Prescott C. Genetic risk factors for major

depression in men and women: similar or different heritabilities and same or
partly distinct genes? Psychol Med. 2001;31:605.

### 35. Tao M, Li Y, Xie D, Wang Z, Qiu J, Wu W, et al. Examining the relationship between

lifetime stressful life events and the onset of major depression in Chinese
women. J Affect Disord. 2011;135:95–9.

### 36. Gao J, Li Y, Cai Y, Chen J, Shen Y, Ni S, et al. Perceived parenting and risk for major

depression in Chinese women. Psychol Med. 2012;42:921–30.

### 37. Gan Z, Li Y, Xie D, Shao C, Yang F, Shen Y, et al. The impact of educational status

on the clinical features of major depressive disorder among Chinese women. J
Affect Disord. 2012;136:988–92.

### 38. Yang F, Li Y, Xie D, Shao C, Ren J, Wu W, et al. Age at onset of major depressive

disorder in Han Chinese women: Relationship with clinical features and family
history. J Affect Disord. 2011;135:89–94.

### 39. Shi J, Zhang Y, Liu F, Li Y, Wang J, Flint J, et al. Associations of educational

attainment, occupation, social class and major depressive disorder among Han
Chinese women. PLOS ONE. 2014;9:e86674.

### 40. Li Y, Shi S, Yang F, Gao J, Li Y, Tao M, et al. Patterns of co-morbidity with anxiety disorders

in Chinese women with recurrent major depression. Psychol Med. 2012;42:1239–48.

### 41. Schuller B, Steidl S, Batliner A, Hirschberg J, Burgoon JK, Baird A, et al. The INTER-

SPEECH 2016 Computational Paralinguistics Challenge: Deception, Sincerity &
Native Language. In: Interspeech 2016 [Internet]. ISCA; 2016 [cited 2023 Apr 19]. p.
2001–5. Available from: https://www.isca-speech.org/archive/interspeech_2016/
schuller16_interspeech.html

### 42. Weninger F, Eyben F, Schuller BW, Mortillaro M, Scherer KR On the Acoustics of

Emotion in Audio: What Speech, Music, and Sound have in Common. Front
Psychol
[Internet].

[cited

Dec
20];4. Available
from:
http://
journal.frontiersin.org/article/10.3389/fpsyg.2013.00292/abstract

### 43. Di Y, Wang J, Li W, Zhu T. Using i-vectors from voice features to identify major

depressive disorder. J Affect Disord. 2021;288:161–6.

### 44. Afshan A, Guo J, Park SJ, Ravi V, Flint J, Alwan A Effectiveness of Voice Quality

Features in Detecting Depression. Interspeech 2018 [Internet]. 2018 Sep [cited

### 2023 Apr 19]; Available from: https://par.nsf.gov/biblio/10098305-effectiveness-

voice-quality-features-detecting-depression

### 45. Alghowinem S, Goecke R, Epps J, Wagner M, Cohn J Cross-Cultural Depression

Recognition from Vocal Biomarkers. In: Interspeech 2016 [Internet]. ISCA; 2016
[cited 2023 May 23]. p. 1943–7. Available from: https://www.isca-speech.org/
archive/interspeech_2016/alghowinem16_interspeech.html

### 46. Quatieri TF, Malyska N Vocal-source biomarkers for depression: a link to psy-

chomotor activity. In: Interspeech 2012 [Internet]. ISCA; 2012 [cited 2022 Jul 7]. p.
1059–62. Available from: https://www.isca-speech.org/archive/interspeech_2012/
quatieri12_interspeech.html

### 47. Syed ZS, Schroeter J, Sidorov K, Marshall D Computational Paralinguistics: Automatic Assessment of Emotions, Mood and Behavioural State from Acoustics
of Speech. In: Interspeech 2018 [Internet]. ISCA; 2018 [cited 2023 Nov 27]. p.
511–5. Available from: https://www.isca-speech.org/archive/interspeech_2018/
syed18_interspeech.html

### 48. Schuller B, Batliner A, Steidl S, Seppi D. Recognising realistic emotions and affect

in speech: State of the art and lessons learnt from the ﬁrst challenge. Speech
Commun. 2011;53:1062–87.

### 49. Schuller B, Steidl S, Batliner A, Burkhardt F, Devillers L, Müller C, et al. Para-

linguistics in speech and language—State-of-the-art and the challenge. Comput
Speech Lang. 2013;27:4–39.

### 50. Eyben F Real-time speech and music classiﬁcation by large audio feature space

extraction. Springer; 2015.

### 51. Mao K, Wu Y, Chen J. A systematic review on automated clinical depression

diagnosis. npj Ment Health Res. 2023;20:1–17.

### 52. Xu S, Yang Z, Chakraborty D, Chua YHV, Tolomeo S, Winkler S, et al. Identifying

psychiatric manifestations in schizophrenia and depression from audio-visual
behavioural
indicators
through
a
machine-learning
approach. Schizophr.
2022;8:1–13.

### 53. Ringeval F, Schuller B, Valstar M, Cummins Ni, Cowie R, Tavabi L, et al. AVEC 2019

Workshop and Challenge: State-of-Mind, Detecting Depression with AI, and
Cross-Cultural Affect Recognition. arXiv:190711510 [cs, stat] [Internet]. 2019 Jul 10
[cited 2021 Jan 21]; Available from: http://arxiv.org/abs/1907.11510

### 54. Hansen L, Rocca R, Simonsen A, Olsen L, Parola A, Bliksted V, et al. Speech- and

text-based classiﬁcation of neuropsychiatric conditions in a multidiagnostic set-
ting. Nat Ment Health. 2023;1:971–81.

### 55. Derogatis LR. SCL-90: an outpatient psychiatric rating scale-preliminary report. Psychopharmacol Bull. 1973;9:13–28.

### 56. Kendler KS, Karkowski-Shuman L. Stressful life events and genetic liability to

major depression: genetic control of exposure to the environment? Psychol Med.
1997;27:539–47.

### 57. Kendler KS, Kessler RC, Walters EE, MacLean C, Neale MC, Heath AC, et al. Stressful

life events, genetic liability, and onset of an episode of major depression in
women. FOC. 2010;8:459–70.

### 58. Suthaharan S Support Vector Machine. In: Suthaharan S, editor. Machine Learning

Models and Algorithms for Big Data Classiﬁcation: Thinking with Examples for
Effective Learning [Internet]. Boston, MA: Springer US; 2016. p. 207–35. Available
from: https://doi.org/10.1007/978-1-4899-7641-3_9

### 59. Chen T, Guestrin C XGBoost: A Scalable Tree Boosting System. In: Proceedings of

the 22nd ACM SIGKDD International Conference on Knowledge Discovery and
Data Mining [Internet]. San Francisco California USA: ACM; 2016 [cited 2024 May
15]. p. 785–94. Available from: https://dl.acm.org/doi/10.1145/2939672.2939785

### 60. Glorot X, Bengio Y Understanding the difﬁculty of training deep feedforward

neural networks. In: Proceedings of the Thirteenth International Conference on
Artiﬁcial Intelligence and Statistics [Internet]. JMLR Workshop and Conference
Proceedings; 2010 [cited 2024 May 16]. p. 249–56. Available from: https://
proceedings.mlr.press/v9/glorot10a.html

### 61. Wang J, Ravi V, Flint J, Alwan A. Speechformer-CTC: sequential modeling of

depression detection with speech temporal classiﬁcation. Speech Commun.
2024;163:103106. Sep 1

### 62. Eyben F, Wöllmer M, Schuller B Opensmile: the munich versatile and fast open-

source audio feature extractor. In: Proceedings of the 18th ACM international
conference on Multimedia [Internet]. Firenze Italy: ACM; 2010 [cited 2023 May
24]. p. 1459–62. Available from: https://dl.acm.org/doi/10.1145/1873951.1874246

### 63. Viechtbauer W. Conducting Meta-Analyses in R with the metafor Package. J Stat

Softw. 2010;36:1–48. Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695

### 64. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful

approach to multiple testing. J R Stat Soc Ser B (Methodol). 1995;57:289–300.

### 65. Speed D, Cai N, Johnson MR, Nejentsev S, Balding DJ. Reevaluation of SNP her-

itability in complex human traits. Nat Genet. 2017;49:986–92.

### 66. Lee SH, Yang J, Goddard ME, Visscher PM, Wray NR. Estimation of pleiotropy between

complex diseases using single-nucleotide polymorphism-derived genomic relationships
and restricted maximum likelihood. Bioinformatics. 2012;28:2540–2.

### 67. Yang J, Lee SH, Goddard ME, Visscher PM. GCTA: a tool for genome-wide complex

trait analysis. Am J Hum Genet. 2011;88:76–82.

### 68. Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, et al. Scikit-

learn: machine learning in python. J Mach Learn Res. 2011;12:2825–30.

## AUTHOR CONTRIBUTIONS

Conceived and designed the study: JF, TZ, AA, ER; Analysed the data: YD, JM, JW, VR, AG. Wrote the paper: YD, KSK, JF. All authors contributed to the interpretation of data,
provided feedback on drafts, and approved the ﬁnal draft. FUNDING
This work was supported by R01-MH122596 from the National Institute of Mental
Health, 200176/A/15/Z from the Wellcome Trust, and a philanthropic donation from
Shirley and Walter Wang. The funding agencies and donors were not involved in the
conduct, analysis, or reporting of this work.

## COMPETING INTERESTS

The authors declare no competing interests.

## ETHICS APPROVAL AND CONSENT TO PARTICIPATE

This study was approved by Institutional Review Boards at UCLA, Bio-x Center, Shanghai Jiao Tong University (M16033), and local hospitals. All participants provided
written informed consent. All methods were performed in accordance with relevant
guidelines and regulations.

## ADDITIONAL INFORMATION

Supplementary information The online version contains supplementary material
available at https://doi.org/10.1038/s41380-024-02877-y. Correspondence and requests for materials should be addressed to Tingshao Zhu or
Jonathan Flint. Reprints and permission information is available at http://www.nature.com/
reprints
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims
in published maps and institutional afﬁliations. Open Access This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing,
adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative
Commons licence, and indicate if changes were made. The images or other third party
material in this article are included in the article’s Creative Commons licence, unless
indicated otherwise in a credit line to the material. If material is not included in the
article’s Creative Commons licence and your intended use is not permitted by statutory
regulation or exceeds the permitted use, you will need to obtain permission directly
from
the
copyright
holder. To
view
a
copy
of
this
licence,
visit
http://
creativecommons.org/licenses/by/4.0/.
© The Author(s) 2024
Y. Di et al. Molecular Psychiatry (2025) 30:2686 – 2695
