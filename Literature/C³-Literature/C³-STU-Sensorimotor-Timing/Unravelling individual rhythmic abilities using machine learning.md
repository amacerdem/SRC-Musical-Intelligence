# Unravelling individual rhythmic abilities using machine learning

**Authors:** Simone Dalla Bella
**Year:** D:20
**Subject:** Scientific Reports, https://doi.org/10.1038/s41598-024-51257-7

---

Vol.:(0123456789)
Scientific Reports | (2024) 14:1135
| https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports
Unravelling individual rhythmic
abilities using machine learning
Simone Dalla Bella 1,2,3,4*, Stefan Janaqi 5, Charles‑Etienne Benoit 6, Nicolas Farrugia 7, Valentin Bégel 8, Laura Verga 9,10, Eleanor E. Harding 11 & Sonja A. Kotz 10,12*
Humans can easily extract the rhythm of a complex sound, like music, and move to its regular beat,
like in dance. These abilities are modulated by musical training and vary significantly in untrained
individuals. The causes of this variability are multidimensional and typically hard to grasp in single
tasks. To date we lack a comprehensive model capturing the rhythmic fingerprints of both musicians
and non-musicians. Here we harnessed machine learning to extract a parsimonious model of rhythmic
abilities, based on behavioral testing (with perceptual and motor tasks) of individuals with and
without formal musical training (n = 79). We demonstrate that variability in rhythmic abilities and their
link with formal and informal music experience can be successfully captured by profiles including a
minimal set of behavioral measures. These findings highlight that machine learning techniques can be
employed successfully to distill profiles of rhythmic abilities, and ultimately shed light on individual
variability and its relationship with both formal musical training and informal musical experiences. When speaking, playing a musical instrument, or walking in nature, we naturally coordinate our actions with
what we perceive. Music is an excellent model for studying this link between perception and action as listening to
music urges us to ­move1. Sometimes we can choose to deliberately align our movements to the beat of music like
we do when dancing. How can we explain this widespread tendency to move to music? Musical features like its
regular temporal structure (rhythmic complexity, syncopation), but also its pitch structure (harmonic complex-
ity) are particularly conducive to ­movement2,3. An explanation of this tight link between musical rhythm and
movement can lie in the structure and functioning of our ­brains1,4–6. Regions of the brain typically underpinning
motor control, such as the basal ganglia and cortical motor areas, are surprisingly engaged even when we merely
listen to a rhythmic sequence in the absence of motor ­movement4,5,7–9. Humans—musicians and non-musicians alike—are well equipped to extract temporal regularities from stimu-
lus sequences, both in the auditory and the visual modalities, and to align their movements to the most prominent
periodicity (e.g., the musical beat or pulse) by foot tapping, dancing, or walking (beat perception and synchro-
nization—BPS10–14; for a contribution of the vestibular system to perceptual–motor coupling see ­also15). The
majority in the general population can track the beat of music and move along with ­it14,16. Matching movements
to the beat is possible because the temporal dynamics of rhythm drives internal neurocognitive self-sustained
oscillations underpinning beat ­perception17–19. This underlying process, called entrainment, generates temporal
expectations which influence motor control and allows the alignment of movements to the anticipated beat times. BPS abilities are thought to be universal skills that can be refined by musical training. Musicians outperform
non-musicians in several BPS tasks. Musical training is found to improve the ability to extract the beat from a
musical sequence and parse its metrical structure, and to reproduce ­rhythms4,20–24. In addition, musicians display
more precise and accurate motor synchronization to the beat than non-musicians, as shown in finger tapping to
rhythmic sequences like a metronome or ­music25–29. OPEN
1International Laboratory for Brain, Music, and Sound Research (BRAMS), Montreal, Canada. 2Department of
Psychology, University of Montreal, Pavillon Marie‑Victorin, CP 6128 Succursale Centre‑Ville, Montréal, QC H3C
3J7, Canada. 3Centre for Research on Brain, Language and Music (CRBLM), Montreal, Canada. 4University of
Economics and Human Sciences in Warsaw, Warsaw, Poland. 5EuroMov Digital Health in Motion, IMT Mines
Ales and University of Montpellier, Ales and Montpellier, France. 6Inter‑University Laboratory of Human
Movement Biology, EA 7424, University Claude Bernard Lyon 1, 69 622 Villeurbanne, France. 7IMT Atlantique, Brest, France. 8Université Paris Cité, Paris, France. 9Comparative Bioacoustics Group, Max Planck Institute for
Psycholinguistics, Nijmegen, The Netherlands. 10Department of Neuropsychology & Psychopharmacology, Faculty of Psychology and Neuroscience, Maastricht University, P. O. 616, Maastricht  6200 MD, The
Netherlands. 11Department of Otorhinolaryngology/Head and Neck Surgery, University Medical Center Groningen, University of Groningen, Groningen, The Netherlands. 12Department of Neuropsychology, Max Planck Institute for
Human Cognitive and Brain Sciences, Leipzig, Germany. *email: simone.dalla.bella@umontreal.ca; sonja.kotz@
maastrichtuniversity.nl

Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
Particularly in the absence of musical training, individuals can differ significantly in BPS ­abilities14,16. A few
single-case studies on beat-deaf individuals or poor ­synchronizers16,30–32, using motor tasks (finger ­tapping33)
and/or beat perception tests (e.g., the Beat Alignment ­Test34), revealed that either beat perception, synchroniza-
tion, or both can be selectively impaired in neurotypical individuals. Both rhythm perception and production
are often impaired in beat-deaf ­individuals31,32. However, synchronization to the beat can be selectively impaired
in the presence of spared beat ­perception16. The reverse—poor perception with unimpaired synchronization to
the beat—is also ­observed30. These individual differences are further exacerbated by disease, such as neurode-
generative and neurodevelopmental disorders ­(Parkinson35,36, ­ADHD37, speech and language ­impairments38–42). Single-case evidence and studies of BPS in patient populations reveal intriguing dissociations between percep-
tion and production, and between beat-based and memory-based processes (see ­also43, for a recent study on a
larger sample of non-musicians). These effects of musical training and individual differences in non-musicians are typically examined by iso-
lated tests or limited sets of tasks, which often vary across experiments and are occasionally tested in small-sample
studies (i.e., single-case studies). This approach, albeit valuable, may provide an incomplete picture of differences
linked to musical training and a simplified characterization of individual differences. Rhythmic abilities reveal a
complex structure involving different dimensions (e.g., beat-based vs. memory-based ­processes43–47), compatible
with the idea that there may exist multiple rhythm ­intelligences48. This complexity and rich structure of rhythmic
abilities might not be easily captured with a few isolated tasks. There is a need of a more general, and at the same
time parsimonious, way to account for individual differences in rhythmic abilities. This approach would call for
multiple testing and modelling of both the differences resulting from musical training and the fluctuations of
BPS capacities in the general population. These dissociations between perception and production may translate
into single profiles that characterize individual differences in BPS abilities. We refer to the term “profile” as a
limited set of measures that can represent, in a succinct way, a given group (e.g., musicians vs. non-musicians,
or a clinical group), and can be illustrated graphically (e.g., using a directed graph, see below). Such profiles
might also serve as markers of developing or progressing impairment in clinical populations. However, the task
of identifying these profiles based on a few single cases and isolated methodologies is daunting. Even though
single-case evidence is informative and suggestive, its generalization is not warranted. A systematic investigation
in larger cohorts, relative to the performance of individuals with musical training, is still lacking. In sum, previous studies showed general differences in BPS abilities linked to musical training and mostly
quantified by a limited set of tests. Evidence from several single-case studies hinted at different rhythmic profiles. However, a general approach to individual differences in rhythmic abilities is still missing, which leaves several
questions unanswered. Which tasks or measures of BPS are the most sensitive to pick up differences due to musi-
cal training? Can we characterize an individual in terms of a given rhythmic profile (e.g., a signature of rhythmic
abilities)? What is the weight of perceptual and motor processes in defining these profiles? In the present study we aimed at characterizing rhythmic abilities in musicians and non-musicians, focus-
sing on beat-based processes, using a data science approach, namely by exploiting predictive modelling with
machine learning. Participants classified themselves as musicians (practicing their instrument during the last
year) or non-musicians. Non-musicians could not have received more than 7 years of formal musical training
(e.g., participation in structured lessons of an instrument or voice, coupled with at least 1 h of practice/week). The outcome of this approach is to define profiles of BPS abilities in musicians and non-musicians, and distill
out a parsimonious model capable of accounting for individual differences in both groups. Given the multidi-
mensionality of rhythmic abilities and to circumvent the limitations of previous studies, we submitted musicians
and non-musicians to a battery of tests assessing both perceptual and motor timing abilities (Battery for the
Assessment of Auditory Sensorimotor and Timing Abilities, BAASTA)49. The battery has been extensively used
in the past and has proven to sensitively detect individual differences in healthy and patient ­populations30,35,38,50,51. As multiple tests provide a wealth of information, we used dimensionality reduction techniques to pinpoint a
minimal set of tasks and measures that allow capturing variability in BPS abilities linked to musical training. Machine ­learning52,53, and graph theory served to operationalize individual differences in rhythmic abilities,
based on measures of BPS. We expected that both perceptual and motor measures would contribute to classify
musicians and non-musicians, and that musicians would display a stronger link between perceptual and motor
measures. This hypothesis is grounded in both behavioral and brain imaging evidence of a tighter coupling
between perceptual and motor systems as a result of extensive musical ­practice6,54,55. Musicians tend to activate
auditory and motor regions jointly when listening to ­sound4,56, or merely moving their ­hands57,58. An increased
sensorimotor association can be found after relatively little training while learning a musical ­instrument59,60,
a process which is likely involving the dorsolateral premotor ­cortex61. A second goal was to examine whether
the measures of rhythmic abilities, which could most successfully distinguish musicians from non-musicians,
would uncover subgroups in non-musicians, potentially reflecting some degree of informal musical experience. While musicians were expected to be quite homogeneous in their rhythmic abilities, non-musicians should
likely be less homogeneous in terms of their BPS abilities, and probably lie on a continuum, or cluster in groups. Individual differences found in single-case studies point towards different profiles, which might characterize
clusters of individuals in the general population. To test this possibility, we used unsupervised learning methods
(clustering) in non-musicians only. Results
Defining profiles of rhythmic abilities in musicians and non‑musicians
To define a profile of rhythmic abilities based on the results of the BAASTA tasks and classify musicians vs.
non-musicians, we processed data from 55 measures using Sparse Learning and Filtering algorithms (SLF)62,63. SLF aims at selecting a minimal set of variables obtained from the perceptual and motor tasks of BAASTA (Perc: Vol.:(0123456789)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
perceptual; M: motor) that capture the most relevant differences between musicians and non-musicians. This set
of measures was then entered in a model, aimed at classifying individuals as musicians or non-musicians based
on their rhythmic performance. The outcome model, including a limited set of measures, is parsimonious and
affords a significant gain in statistical power relative to a model that includes all the variables. We systematically
tested three classification models, by taking as input (1) the entire set of perceptual measures (7 out of 55; Model
Perc), (2) the entire set of motor measures (48 out of 55; Model Motor), and (3) the selected measures resulting
from Models Perc and Motor (Model PMI). Model PMI also included interactions between motor and perceptual
measures to test the hypothesis that the combination of perceptual and motor abilities is more relevant in defining
the rhythmic profile of musicians than of the one of non-musicians. The procedure and the selected variables are
illustrated in Fig. 1. Model Perc significantly accounted for 50% of the variance (F(73) = 14.4, p < 0.0001), model
Motor accounted for 84% of the variance (F(74) = 97.1, p < 0.0001), and finally model PMI accounted for 92%
of the variance (F(70) = 99.5, p < 0.0001), relative to the prediction of a model using the entire set of variables. Accuracy for the three models is shown in Fig. 1. We tested the capacity of the three models to discriminate between musicians and non-musicians by taking
the outcome of the models (value from 0 to 1, with 0 indicating non-musicians, and 1, musicians) using the
entire dataset (i.e., including the three phases of the classifier validation). Model PMI was superior compared
to the other two models in classifying musicians and non-musicians (Fig. 2a; Model × Group interaction, F(2,
154) = 3.8, p < 0.05; model Perc, t(66.9) = 5.2, p < 0.0001, d = 1.3; model Motor, t(64.3) = 6.2, p < 0.0001, d = 1.5;
model PMI, t(64.0) = 7.0, p < 0.0001, d = 1.8). Even though the distributions of the model PMI predictions were
partly overlapping (Fig. 2b), the model could classify musicians and non-musicians very successfully (Fig. 2c). Equation (1) below allowed the classification of musicians and non-musicians (prediction = ỹ) for model PMI. Model PMI, including two perceptual variables, two motor variables, and the four interactions yielded the
best classification results. The two perceptual variables come from two different tasks—the Beat Alignment Test
and Anisochrony detection with music—in which participants were asked to detect whether a metronome was
aligned to the beat of a musical excerpt presented at a slow tempo (P1—BAT_slow_Dprime; sensitivity index),
and whether there was a rhythmic irregularity—a shifted beat—in a short musical fragment (P2—Anisoc_det_
music_Thresh; threshold). The two motor measures come both from paced finger tapping tasks (Paced tapping
with tones, Paced tapping with music), and indicate synchronization accuracy (alignment of participants’ taps
to the beat) when participants tapped to a metronome presented at a slow tempo (M1—Paced_metro_750_Vec-
tor_dir) or to a musical excerpt (M2—Paced_music_ross_Vector_dir). To gain a better understanding of the
rhythmic signature of musicians and non-musicians, we examined the contribution to the classification of each
(1)
y = 0.49 + 0.05P1 −0.08P2 + 0.11M1 + 0.12M2 + 0.02P1M1 −0.005P1M2 −0.002P2M1 −0.007P2M2. Figure 1. Schema of the analysis pipeline using Sparse Learning and Filtering (SLF). Selected variables
for Model Perc: 3 variables from the Beat Alignment Test (BAT_slow_Dprime, BAT_med_Dprime, BAT_
fast_Dprime), 1 from Duration discrimination (Dur_discrim_Thresh), and 1 from Anisochrony detection
with music (Anisoc_det_music_Thresh). Model Motor: 2 variables from Paced tapping with tones (Paced_
metro_750_Vector_dir, Paced_metro_750_Vector_len), 1 from Paced tapping with music (Paced_music_
ross_Vector_dir), and 1 from Unpaced tapping (Unpaced_slow_CV). Model PMI included (a) two perceptual
measures, reflecting the ability to detect whether a metronome is aligned to the beat of music or not (P1—
BAT_slow_Dprime), or whether there is a rhythmic irregularity—a shifted beat—in a short musical fragment
(P2—Anisoc_det_music_Thresh), (b) two motor measures, indicating the alignment of participants’ taps with
the beat of a metronome (M1—Paced_metro_750_Vector_dir) and music (M2—Paced_music_ross_Vector_dir),
and (c) the four interactions between these measures (P1 × M1, P1 × M2, P2 × M1, P2 × M2). Accuracy is calculated
based on the Test phase of the classifier validation. Full description of the variables, and confusion matrices
for the three models at Train (60% of the dataset), Validation (20%) and Test (20%) phases are provided in
Supplementary Materials. Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
variable and interaction independently for each group. We calculated the correlation between each variable and
the prediction separately for musicians and non-musicians, leading to a measure of explained variance. With
this method we obtained two profiles characterizing musicians and non-musicians (Fig. 3a,b). The contribution
of each component (perceptual, motor, and their interaction) to the profiles of musicians and non-musicians
Figure 2. Classification performance of the three models. (a) Comparison of the Perc, Motor, and PMI
models predictions (0 = non-musicians; 1 = musicians). Error bars represent SEM. (b) Probability density for
musicians and non-musicians obtained with model PMI. (c) Scatter plot showing the individual predictions
based on model PMI. For simplicity, the predictions are presented as a projection of two composite scores
representing the linear portions of the prediction model, referring to the perceptual measures (perceptual
score = 0.05P1 − 0.08P2) and the motor measures (motor score = 0.11M1 + 0.12M2), without the interactions. Figure 3. Profiles of rhythmic abilities for musicians (a) and non-musicians (b) based on model PMI,
expressed as undirected graphs. The nodes’ size reflects the contribution of the variable to the definition of the
group (proportion of variance) and the edges’ widths to the contribution of the interactions. (c) Comparison
of the contribution of the model component (perceptual, motor, interaction) to the profiles of musicians and
non-musicians. P: perceptual; M: motor. Numbers refer to the specific variable (P1—BAT_slow_Dprime; P2—
Anisoc_det_music_Thresh; M1—Paced_metro_750_Vector_dir; M2—Paced_music_ross_Vector_dir). *p < 0.05. Vol.:(0123456789)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
is illustrated in Fig. 3c. The motor measures contributed to the profiles more than perceptual measures in both
musicians (χ2(1) = 20.8, p < 0.0001) and non-musicians (χ2(1) = 22.4, p < 0.0001). Differences between the two
profiles regarding the contribution of individual variables and interactions are apparent. Interactions between
perceptual and motor variables play a more important role in the definition of musicians’ profile than for non-
musicians (χ2(1) = 5.2, p < 0.05). The motor component may contribute more to the definition of non-musicians,
but this difference did not reach statistical significance (χ2(1) = 3.5, p = 0.11). These findings revealed that a minimal set of rhythmic measures and their interactions can successfully dif-
ferentiate musicians from non-musicians, as illustrated by undirected graphs. A limitation of this representation,
however, is that it does not reflect the sign of the relation, positive or negative, between the variable and the
predicted group. Moreover, one might wonder whether each component of the model can explain individual
variability within each group. To address this point, we examined the relation between each variable and inter-
action and the prediction, separately for each group (Fig. 4). Each component of the profile can explain differ-
ences within each group. The only exception was the interaction between P2 and M1, which just failed to reach
significance in explaining the variability for non-musicians. Notably the motor measures alone could explain
large portions of intra-group individual variability (63% for non-musicians and 46% for musicians). Moreover,
interactions between perceptual and motor variables could capture a significant amount of individual variabil-
ity in both groups. This further supports the inclusion of interactions in the PMI model. Also worth noting is
the sign of the relation between the components and the prediction. For both groups, improved performance
(i.e., an increase of P1, M1, or M2; a decrease of P2, indicating a lower detection threshold) was associated with
greater rhythmic abilities. When considering the interaction between perceptual and motor measures, opposite
relations with rhythmic abilities as reflected by the prediction of the PMI model (from 0 to 1) emerged. These
interactions were not only key in differentiating musicians from non-musicians (as shown in Fig. 3c), but also
played different roles in capturing individual differences within each group. Notably, a stronger interaction
between perceptual and motor measures, suggesting better performance in both dimensions (characterized by
Figure 4. Scatter graphs showing the relation between individual elements of the profiles of rhythmic abilities
(measures and their interactions) and the prediction of model PMI, separately for musicians and non-musicians. Explained variance for each group is reported (in bold when the regression was statistically significant).
**p < 0.01, *p < 0.05, ns not significant. Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
increasing positive values for P1 × M1 or M2, and negative values for P2 × M1 or M2, considering that lower P2
values—a perceptual threshold—signify better performance), was associated with enhanced prediction scores
exclusively among musicians. Profiles of rhythmic abilities for non‑musicians
An inspection of measures of rhythmic abilities in non-musicians revealed considerable variability in this group. Variance was larger in non-musicians than in musicians, as reflected by the PMI model (SD of the prediction from
PMI model for non-musicians = 0.24, for musicians = 0.14; Bartlett test for homogeneity of variance, χ2(1) = 9.6,
p < 0.01). To assess whether non-musicians’ rhythmic performance was homogeneous or rather different clus-
ters (and corresponding profiles) would emerge, we used model PMI to examine the distribution of rhythmic
skills in this group, linked with formal and informal musical experiences. This approach was both practical
and parsimonious as it was based on a limited set of variables (as compared to the full set) shown as sensitive
to large individual differences in rhythmic abilities linked to musical training (see below for further analyses
including the full dataset). Building on graph theory, we extracted two clusters from the non-musicians group
using modularity ­analysis64,65. This procedure led to the detection of two clusters (Subgroup 1, Subgroup 2) that
maximized modularity. Subgroup 1 included 20 participants (9 females, mean age = 24.1 years, SD = 4.7), and Subgroup 2 was formed
by 20 participants (10 females, mean age = 22.1 years, SD = 2.6). The two subgroups did not differ significantly in
terms of years of formal musical training (mean = 0.8 years, SD = 1.5, for Subgroup 1; mean = 1.8 years, SD = 2.4,
for Subgroup 2; t(31.8) = 1.6, p = 0.14, d = 0.5). However, Subgroup 2 showed more years of informal musical
activities (mean = 1.7 years, SD = 2.9, for Subgroup 1; mean = 5.0 years, SD = 4.3, for Subgroup 2; t(33.3) = 2.8,
p < 0.01, d = 1.0). By informal musical activities we referred to engaging in amateur play of one or more musical
instruments without the requirement of formal musical education. Once we uncovered the two clusters of non-musicians, we used the variables of model PMI to classify the two
subgroups (see Eq. 2 below). This new model could classify the two subgroups with an accuracy of 100% (in the
Test phase of the classifier validation; the confusion matrices at Train, Validation and Test phases are provided in
Supplementary Materials). The performance of the model is seen in Fig. 5. To avoid confusion with the coding
Figure 5. Classification performance of Model PMI for the two subgroups of non-musicians (− 1 = Subgroup 1;
1 = Subgroup 2). (a) Probability density for non-musicians in Subgroup 1 and Subgroup 2. (b) Scatter plot showing
the individual predictions based on the model. The predictions are presented as a projection of two composite
scores representing the linear portions of the prediction model, referring to the perceptual variables (perceptual
score = 0.76P1 + 0.15P2) and the motor variables (motor score =  0.53M1 − 0.07M2), without the interactions. Vol.:(0123456789)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
of musicians and non-musicians in the previous model, we indicated perfect classification for Subgroup 1 with
“− 1” and for Subgroup 2 with “+ 1”. We obtained profiles for the two subgroups of non-musicians by examining the contribution of each variable
and interaction to the classification of each group (in Fig. 6, panels a and b). The contribution to the profiles
of Subgroups 1 and 2 of each component (perceptual, motor, and their interaction) is presented in Fig. 6c. The
motor measures contributed to the profiles more than perceptual measures for both Subgroup 1 (χ2(1) = 32.1,
p < 0.0001) and Subgroup 2 (χ2(1) = 8.8, p < 0.01). There was a tendency toward a greater contribution of the motor
component in Subgroup 1 than in Subgroup 2 (χ2(1) = 3.2, p = 0.07). To test whether each component of the non-musicians’ subgroup profiles can explain individual variability
within each group, we examined the relation between each variable and interaction and the prediction separately
for each subgroup (Fig. 7). Only a few components of the profiles could explain the variability in each Subgroup, but in a rather specific
way. Notably, the two components P1 and M1, and their interaction, were the only ones that explained the
variability within the two subgroups. Variability within Subgroup 1 was strongly related with component P1,
explaining 68% of its variance, and with the interaction between component P1 and M1 (20%). Variability within
Subgroup 2 was mostly explained by component M1 (51% of the variance) and the interaction between M1 and
P1 (68%). Finally, as the two subgroups of non-musicians differed in terms of informal musical activities, we
tested whether variability in each of the two subgroups was related to this variable. Variability within Subgroup
1, indicated by the prediction of PMI model, was correlated with informal musical training (r = 0.48, p < 0.05). With increasing years of informal musical training, the prediction from the model for participants in Subgroup
1 became closer to 0, thus nearing the performance of Subgroup 2. This finding is consistent with the observa-
tion that Subgroup 2 displayed significantly more informal musical experiences than Subgroup 1 (see above). Finally, we ran an additional analysis to test whether some of the perceptual and motor measures included in
the PMI model were specifically correlated with informal musical training. Only M1 was positively correlated
with informal musical training (r(38) = 0.42, p < 0.05, Bonferroni-corrected), and the P1 correlation just failed
to reach significance (r(38) = 0.37, p = 0.08, Bonferroni-corrected). By design, the detection of two clusters among non-musicians and the extraction of the corresponding
profiles were based exclusively on the variables included in model PMI, which was highly successful in distin-
guishing musicians from non-musicians. This choice, albeit practical and parsimonious, might have biased the
search for profiles of rhythmic skills in non-musicians by focussing only on those capacities linked with musical
training. To test whether the clusters we identified were more representative of rhythmic abilities in general,
we extracted two clusters using a modularity analysis from the group of non-musicians using a subset of the
initial set of 55 variables representing 95% of the variance instead of taking only the variables from model PMI
(see Supplementary Materials). We detected two clusters of participants very comparable to those obtained in
the analysis based on model PMI, showing a large overlap (88%) between the classifications. Hence, the identi-
fied subgroups using the PMI model and based on a reduced set of profile measures seemed to effectively and
(2)
y = 0 + 0.76P1 + 0.15P2 + 0.53M1 −0.07M2 + 0.42P1M1 −0.04P1M2 −0.10P2M1 −0.00P2M2. Figure 6. Profiles of rhythmic abilities for non-musicians in Subgroup 1 (a) and Subgroup 2 (b) expressed
as undirected graphs. The nodes’ size reflects the contribution of the variable to the definition of the group
(proportion of variance) and the edges the contribution of the interactions. (c) Comparison of the contribution
of the model component (perceptual, motor, interaction) to the profiles of Subgroups 1 and 2. P: perceptual; M:
motor. Numbers refer to the specific variable (P1—BAT_slow_Dprime; P2—Anisoc_det_music_Thresh; M1—
Paced_metro_750_Vector_dir; M2—Paced_music_ross_Vector_dir). *marg. marginally significant, p = 0.07. Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
parsimoniously capture the individual differences in rhythmic abilities among non-musicians, as reflected by
their performance on BPS tasks. Discussion
We used machine learning techniques to characterize BPS abilities in musicians and non-musicians by selecting
a minimal set of perceptual and motor measures from a battery of rhythmic tests (BAASTA)49. We expected both
perceptual and motor measures to contribute to the classification of musicians and non-musicians. In keeping
with our hypothesis, a classification model (PMI) including small sets of perceptual and motor measures (4
variables overall) and their interactions was superior to models of perceptual and motor measures on their own. The final model of rhythmic abilities was very accurate in classifying musicians and non-musicians (almost 90%)
and allowed distilling separate profiles (undirected graphs) for the two groups. The final model included perceptual and motor measures derived from tasks which were shown to be affected
by musical training in prior work. The detection of the alignment between a metronome and musical beat (Beat
Alignement Test), and the perception of a rhythmic irregularity in an isochronous sequence (Anisochrony
detection) are typically enhanced by musical ­training66–68. Similarly, performance in paced tapping to rhythmic
stimuli (music and metronomes) is improved by musical ­training28,29,69 (for a review, ­see70). Interestingly, two of
the identified measures involved presenting the stimuli at a slow tempo (with an IOI of 750 ms), when detecting
a misalignment or tapping to an isochronous sequence, while the other two measures involved music fragments
presented at an average tempo (IOI of 600 ms). Whether stimulus processing at slow tempos plays a specific role
in defining rhythm profiles based on musical expertise is still unclear. For example, there is some evidence that
increased tempo might affect the tendency to anticipate the beat in paced finger tapping tasks (mean negative
­asynchrony71; but ­see70, for a discussion), an effect that seems to depend on musical training, at least at very
Figure 7. Scatter plots showing the relation between individual elements of the profiles of rhythmic abilities
(variables and interactions) and the prediction of model PMI, separately for non-musicians in Subgroups 1
and 2. Explained variance for each group is reported (in bold when the regression was statistically significant).
**p < 0.01, *p < 0.05, ns not significant. Vol.:(0123456789)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
slow ­tempos29. However, further research is needed to confirm the role of slow tempo in BPS when classifying
musicians and non-musicians. Motor measures played a more important role (explaining more variance) than perceptual measures for both
musicians and non-musicians. Interactions between perceptual and motor measures were stronger for musicians
than for non-musicians. Interestingly, the components of the profiles, albeit limited in number, could success-
fully capture individual variability within each group. An improvement in rhythm perception (better detection
of beat alignment or deviations from isochrony) or production (a less negative relative phase between taps and
the beat) increased the probability of being classified as musicians (with prediction scores closer to 1). The inter-
actions between perceptual and motor measures also explained a significant amount of variance within each
group. Notably, these interactions were differently linked to the performance of musicians and non-musicians
in rhythmic tasks as shown by opposite slopes relative to the model prediction in the two groups. In sum, it is
apparent that interactions between perceptual and motor measures play a critical role in defining a musician’s
rhythmic profile. Taking interactions into account both improves the classification of an individual as a musician
or a non-musician and can specifically account for intra-group variability. These findings are consistent with neuroimaging evidence of stronger coupling of auditory and motor sys-
tems resulting from extensive musical ­practice6,54. The effects of both short-term and long-term musical training
on brain plasticity have been widely documented and pertain to primary sensory and motor regions as well as
sensorimotor integration ­areas54,72–75. Auditory-motor associations can emerge as the result of little training
when learning a musical instrument (e.g., after training non-musicians to play an MRI-compatible cello)60 and
are thought to engage the dorsolateral premotor ­cortex61. The examination of the neuronal underpinnings of
auditory-motor integration when playing different musical instruments and ­singing76 revealed overlaps, for
example in dorsal premotor and supplementary motor cortices, thus pointing to shared mechanisms. A next
step in future research should be to link the profiles of rhythmic abilities identified herein through behavioral
measures with their brain substrates, to gain a better understanding of these individual differences. A second goal was to examine whether the profile measures which were successful in differentiating musi-
cians from non-musicians (from model PMI) could also reveal subgroups among non-musicians. This might
reflect varying degrees of informal musical experience in non-musicians. By applying modular clustering, an
unsupervised learning method, to the data extracted from non-musicians’ profiles, we identified two clusters. Again, motor measures contributed more than perceptual measures to both profiles, with a slight tendency to
contribute more to one of the two profiles (Subgroup 1). However, this general observation did not entirely reflect
the weight of the different tasks to capture variance within each group. For Subgroup 1, a single perceptual task
(detecting a misalignment between a metronome and the musical beat) unexpectedly accounted for the majority
of the variance, which contrasts with the initial impression given by the graph profiles. Similarly, for Subgroup
2, it was a motor task (finger tapping to a metronome) that captured most of the variance. This suggests that,
despite the overall dominance of motor measures in defining subgroup profiles, individual tasks may have a
disproportionate impact on the variance within each subgroup, thus providing a very parsimonious metric of
individual differences in the rhythmic domain. Generally, the interactions between perceptual and motor meas-
ures were less specific in capturing individual variability than when we compared musicians and non-musicians. Notably, the classification of similar subgroups among non-musicians was replicated when considering a much
larger set of perceptual and motor measures issued from BAASTA battery (and explaining most of the variance),
showing that the profiles obtained, in spite of the fact that they included a minimal set of variables based on the
comparison of musicians and non-musicians, could robustly capture individual differences in rhythmic abilities
among non-musicians. The two clusters of non-musicians differed in their informal musical activities. People belonging to the sub-
group displaying more years of informal musical activities, albeit being classified as non-musicians, received
less extreme prediction scores by the model (farther away from − 1) than the other group. Consistently, the
years of informal musical activities could also account for individual variability within one of the subgroups. Thus model PMI can capture subtle differences in rhythmic abilities linked to informal musical activities, such
as playing a musical instrument as an amateur musician would do. Notably, Western listeners, musicians, and
non-musicians alike, can acquire implicitly complex musical features (melody, harmony, rhythm)77–81 from
mere exposure to ­music82, shaping their ­perception77 and ­production83. This implicit knowledge paves the way
for non-musicians’ perception of the relations between musical events, thus creating expectations for upcoming
events that in turn, influence their ­processing84,85. Interestingly, informal music activities are likely to play an
important role earlier in life during music ­acquisition86. There is growing interest in the role of informal musical
activities, with evidence suggesting positive effects on both music and language development, auditory process-
ing, and vocabulary and grammar ­acquisition87–89. As informal musical activities are quite common, having a
model capable of capturing their effects on BPS may provide further insight into the relation between BPS and
developmental ­disorders37,38,41,42. Conclusions
The effects of musical training on beat perception and synchronization are well established. Yet, to date we are
missing a general approach to rhythmic abilities that can account for differences linked to musical training and
variability in non-musicians. Here we filled this gap by using machine learning ­techniques52,53 to extract a par-
simonious model of rhythmic abilities from a large set of perceptual and motor tasks (BAASTA)49. The obtained
profiles of rhythmic abilities, represented by undirected graphs, were based on a handful of perceptual and motor
measures. They were very successful in separating musicians and non-musicians, and could capture the variability
among non-musicians. Thus, using machine learning for the purpose of building a model of rhythmic abilities
was a very fruitful endeavor. Machine learning is progressively becoming an important element of the toolbox

Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
for research in cognitive science and ­neuroscience90–93 with applications in music research such as computational
music ­analysis94, and more recently in music ­cognition95. A similar approach based on machine learning and
graph theory as used to model individual differences in rhythmic abilities could be purposefully extended to
other music abilities such as pitch perception and production, or ­improvisation96. By exploiting machine learning, starting from a dataset derived from behavioral tests, we demonstrated that
the complexity of rhythmic abilities reflected by BPS ­tasks43, linked with formal musical training but also informal
musical experiences, can be captured by a minimal set of behavioral measures and their interaction. Detecting
profiles of rhythmic abilities and their link with formal and informal musical experiences is valuable to shed
light on the sources of individual variability in BPS (e.g., ­neuronal97; ­genetic98), and the link with more general
cognitive functioning. For example, rhythmic abilities and cognitive functions such as cognitive flexibility, inhibi-
tion, and working memory tend to covary in both healthy individuals and in populations with ­disorders37,38,99;
moreover, executive functions and rhythmic abilities are both enhanced by musical ­training100,101. A systematic
study of the relation between profiles of rhythmic abilities and cognitive functions is likely to advance our
understanding of the inter-dependence between rhythmic capacities and general cognitive functions, and the
underlying mechanisms. Finally, as individual differences in BPS are exacerbated in clinical populations, the
proposed model and the profiles of rhythmic abilities may serve for identifying markers of ­impairment102. One
of the advantages of this approach, owing to the model’s parsimony, is that profiles can be obtained via rapid
testing and screening of participants with a limited set of tasks (the Beat Alignment Test, anisochrony detection,
and finger tapping to a metronome and to music), that can be performed in about 15 min. This corresponds to
a gain in time over 80% relative to the full testing battery (lasting 2 h)49. Ultimately, detecting individual pro-
files of rhythmic abilities in patient populations may play a pivotal role in devising personalized rhythm-based
­interventions103,104. To further substantiate the profiles uncovered in this study, it would be beneficial to extend
the testing of the aforementioned measures to a broader sample, also encompassing clinical populations. Materials and methods
Participants
Seventy-nine adults (43 females, 35 right-handed, 4 left-handed and 2 ambidextrous) between 18 and 34 years
of age participated in the experiment. Thirty-nine (24 females; mean age = 24.3 years, SD = 2.5) were musi-
cians and 40 (19 females; mean age = 23.1, SD = 4.0) non-musicians. Musicians were German native speakers
recruited via a participant database at the Max Planck Institute for Human Cognitive and Brain Sciences in
Leipzig (Germany), and non-musicians were French speakers recruited in Montpellier (France). Participants
had to satisfy the following criteria to be assigned to one of the two groups: (1) they self-classified as musicians
or non-musicians, (2) they had practiced during the last year (musicians) or they did not practice during the last
year (non-musicians), and (3) did not receive more than 7 years of formal musical training to be considered as
non-musicians. A year of formal musical training was defined as a year during which the participant underwent
a structured lesson schema of any instrument or voice, either self-taught or by an instructor, and practiced an
average of at least 1 h per week. Musicians reported more years of formal musical training (mean = 7.5 years, SD = 2.5) than non-musicians (mean = 1.3 years, SD = 2.1; t(48.6) = 6.7, p < 0.0001, d = 1.9), and more years of
informal musical activities (13.1 years, SD = 4.4. vs. 3.4 years, SD = 4.1; t(76.4) = 10.2, p < 0.0001, d = 2.3). Informal
musical activities consisted of playing one or more musical instruments as an amateur without having received
formal musical training, which was the case for some non-musicians. The study was approved by the Ethics
Committee of the University of Leipzig and by the Euromov Ethics Committee. Informed consent was obtained
from all participants. All experiments were performed in accordance with relevant guidelines and regulations. Tests and procedure
We tested participants’ rhythmic abilities by submitting them to the Battery for the Assessment of Auditory and
Sensorimotor Timing Abilities (BAASTA)49. Measures of rhythmic abilities
BAASTA consists of a series of 4 perceptual tasks and 5 motor tasks. Perceptual tasks consisted in discriminating
single durations (Duration discrimination), detecting deviations from the beat in tone and musical sequences
(Anisochrony detection with tones, with music), or in saying whether a superimposed metronome was aligned
or not to a musical beat (Beat Alignment Test). Motor tasks involved finger tapping in the absence of stimulation
(Unpaced tapping), tapping to the beat of tone and music sequences (Paced tapping with tones, with music),
continuing tapping at the pace of a metronome (Synchronization–continuation), and adapting tapping to a
tempo change (Adaptive tapping). Participants were tested on all the tasks with a computer version of BAASTA. Auditory stimuli were delivered via headphones (Sennheiser HD201). Task order was fixed (Duration discrimi-
nation, Anisochrony detection with tones and music, BAT, for perceptual tasks; Unpaced tapping and Paced
tapping to tones and music, followed by Synchronization-continuation and Adaptive tapping, for motor tasks). The battery lasted approximately 2 h. In the Duration discrimination test, two tones (frequency = 1 kHz) were presented successively. The first tone
lasted 600 ms (standard duration), while the second lasted between 600 and 1000 ms (comparison duration). Participants judged whether the second tone lasted longer than the first. The goal of the Anisochrony detection
with tones task was to test the detection of a time shift in an isochronous tone sequence. Sequences of 5 tones
(1047 Hz, tone duration = 150 ms) were presented with a mean inter-onset interval (IOI) of 600 ms. Sequences
were isochronous (i.e., with a constant IOI) or not (with the 4th tone presented earlier than expected by up to
30% of the IOI). Participants judged whether the sequence was regular or not. The task was repeated using musi-
cal stimuli (Anisochrony detection with music) that consisted of an excerpt of two bars from Bach’s “Badinerie”

Vol.:(0123456789)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
orchestral suite for flute (BWV 1067) played with a piano timbre (inter-beat interval = 600 ms). To assess beat
perception, the Beat Alignment Test (BAT) used 72 stimuli based on 4 regular musical sequences, including 20
beats each (beat = quarter note). Two sequences were fragments from Bach’s “Badinerie”, and 2 from Rossini’s
“William Tell Overture”, both played with a piano timbre and played at three different tempos (with 450, 600,
and 750-ms inter-beat intervals—IBIs). From the 7th musical beat onward a metronome (i.e., triangle sound)
was superimposed onto the music, either aligned or non-aligned to the beat. When non-aligned, the metronome
was either phase shifted (with the sounds presented before or after the musical beats by 33% of the music IBI,
while keeping the tempo), or period shifted (with the tempo of the metronome changed by ± 10% of the IBI). Participants judged whether the metronome was aligned or not with the musical beat. These perceptual tasks
were implemented using Matlab software (version 7.6.0). In the first 3 tasks, there were three blocks of trials
and a maximum-likelihood adaptive ­procedure105 (MLP; MATLAB MLP ­toolbox106) was used to obtain per-
ceptual thresholds (for details, ­see49). All tasks were preceded by 4 examples and 4 practice trials with feedback. Responses in the perceptual tasks were provided verbally and entered by the Experimenter using the computer
keyboard by pressing one of two keys corresponding to a “yes” or “no” response. “Yes” indicated the situation
when the participant detected a duration difference, the presence of an anisochrony, or that a metronome was
misaligned with the musical beat. Motor rhythmic abilities were tested with finger tapping tasks. Participants responded by tapping with the
index finger of their dominant hand on a MIDI percussion pad. The purpose of the Unpaced tapping task was to
measure the participants’ preferred tapping rate, and its variability without a pacing stimulus. Participants were
asked to tap at their most natural rate for 60 s. In two additional unpaced conditions we asked participants to tap
as fast as possible, and as slow as possible, for 60 s. In the Paced tapping with tones task, we asked participants
to tap to a metronome sequence, formed by 60 isochronously presented piano tones (frequency = 1319 Hz) at 3
different tempos (600, 450 and 750-ms IOI). Similarly, in the Paced tapping with music task participants tapped to
the beat of two musical excerpts taken from Bach’s “Badinerie” and Rossini’s “William Tell Overture”. Each musi-
cal excerpt contained 64 quarter notes (IBI = 600 ms). Paced tapping trials were repeated twice for each stimulus
sequence and were preceded by one practice trial. To test the ability to continue tapping at the rate provided by a
metronome, in the Synchronization–continuation task participants synchronized with an isochronous sequence
of 10 tones (at 600, 450, and 750 ms IOI), and continued tapping at the same rate after the sequence stopped, for
a duration corresponding to 30 IOIs of the pacing stimulus. The task was repeated twice at each tempo and was
preceded by one practice trial. Finally, in the Adaptive tapping task, aimed to assess the ability to adapt to a tempo
change in a synchronization-continuation task, participants tapped to an isochronous sequence (10 tones). At
the end of the sequence (last 4 tones) the tempo either increased, decreased, or remained constant (40% of the
trials). The tempo changed by ± 30 or ± 75 ms. The task was to tap to the tones in the sequence, to adapt to the
tempo change, and to keep tapping at the new tempo after the stimulus stopped for a duration corresponding
to 10 IOIs. After each trial, participants judged whether they perceived a change in stimulus tempo (accelera-
tion, deceleration, or no change). The responses were communicated verbally and entered by the Experimenter. Trials were divided into 10 experimental blocks (6 trials × 10 blocks overall) and presented in random order. A
training block preceded the first experimental trial. In all the motor tasks, the performance was recorded via a
Roland SPD-6 MIDI percussion pad. Stimulus presentation and response recording was controlled by MAX-MSP
software (version 6.0). A MIDI response latency of 133 ms (Leipzig testing) and 100 ms (Montpellier testing)
was subtracted from the tapping data before further analysis. Analyses
BAASTA
For Duration discrimination, Anisochrony detection with tones and with music, we calculated mean thresholds
(percentage of the standard duration in the three task) across the three blocks or trials. We rejected the blocks
including more than 1/3 of False Alarms, when a difference in duration, or that the sequence beat was irregular,
was reported while there was no difference/no deviation from isochrony in the stimulus. In the BAT, we calcu-
lated the sensitivity index (dʹ) for the entire set of 72 stimuli, and separately for each or the 3 tempos (medium,
fast, and slow). dʹ was calculated based on the number of Hits (when a misaligned metronome was correctly
detected) and False Alarms (when a misalignment was erroneously reported). Motor data obtained from tapping tasks were pre-processed as follows (as in Refs.16,49). We discarded taps
leading to inter-tap intervals (ITIs) smaller than 100 ms (artifacts) and outlier taps were discarded. An outlier was
defined as a tap for which the ITI between the actual tap and the preceding tap was smaller than Q1–3 × Inter-
quartile range (IQR) or greater than Q3 + 3 × IQR, where Q1 is the first quartile and Q3 is the third quartile. We calculated the mean ITI (in ms) and motor variability (coefficient of variation of the ITI—CV ITI—namely,
the SD of the ITI/mean ITI) for Unpaced tapping (spontaneous, slow, and fast), Paced tapping, and for the
Synchronization-continuation tasks. Moreover, we analyzed synchronization in the Paced tapping task using
circular ­statistics107 (Circular Statistics Toolbox for ­Matlab108; for use in BAASTA ­see49). Tap times were coded
as unitary vectors with angles relative to the pacing event (tone or musical beat) on a 360° circular scale (cor-
responding to the IOI). The mean resultant vector R was calculated from the unit vectors corresponding to all
the taps in a sequence. We used two indexes of synchronization performance: the length of vector R (from 0
to 1) and its angle (θ or relative phase, in degrees). Vector length indicates whether the taps are systematically
occurring before or after the pacing stimuli (synchronization consistency); 1 refers to maximum consistency (no
variability), and 0, to a random distribution of angles around the circle (i.e., lack of synchronization). The angle of
vector R (θ or relative phase, in degrees) indicates synchronization accuracy, namely whether participants tapped
before (negative angle) or after (positive angle) the pacing event. Accuracy was calculated only if participants’
synchronization performance was above chance (null hypothesis = random distribution of data points around

Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
the circle), as assessed with the Rayleigh test for circular ­uniformity107,109. The null hypothesis is rejected when R
vector length is sufficiently large according to this test. Vector length data was submitted to a logit transformation
(e.g.40) before conducting further analyses. Additionally, for the Synchronization–continuation task, we calcu-
lated measures of central (or timekeeper) variance and motor variance based on Wing–Kristofferson’s ­model110. In both paced tapping and synchronization–continuation tasks, the results in the two trials were averaged and
submitted to further analyses. Finally, we analyzed the data from the Adaptive tapping task by first calculating an adaptation ­index111. To
do so, we fitted a regression line to obtain the slope of ITIs functions relative to the final sequence tempo; the
value of the slope corresponds to the adaptation index. When the value is 1, the adaptation is perfect; lower
and higher values than 1 indicate undercorrection and overcorrection, respectively. We calculated this index
separately for tempo acceleration (i.e., faster tempi with final sequence IOIs < 600 ms) and tempo deceleration
(slower tempi with final sequence IOIs > 600 ms). In addition, error correction was portioned into the two con-
tributors, phase correction and period ­correction112. Phase and period correction were estimated from the two
parameters alpha and beta of the fitted two-process model of error ­correction111. Finally, in the same task we
calculated the sensitivity index (dʹ) for detecting tempo changes based on the number of Hits (when a tempo
acceleration or deceleration was correctly detected) and False Alarms (when a tempo acceleration or deceleration
was reported while there was no change or the opposite change). The full list of the 55 variables (7 perceptual,
48 motor) obtained from BAASTA and used as input database for clustering and data modelling is provided in
Supplementary Materials. Definition of a model of rhythmic abilities (sparse learning and filtering)
The 55 variables from BAASTA collected from a group of 39 musicians and 40 non-musicians served as the start-
ing point to define a model of rhythmic abilities, for classifying the two groups. These variables formed a vector
x = (x1,..., xd) in our classification model. Given a set of pairs (xk, yk), k = 1,..., n, we looked for a relation
y = f (x) that fits the answers yk by f (xk); y takes value 1 for musicians and 0 for non-musicians. We denote by
Y the vector of all answers y. Finding this relation represents a supervised classification problem as the answers
yk are known. We addressed this problem using machine learning. One advantage of machine learning is that
it does not need a priori hypotheses. However, several methods (e.g., neural nets) behave like a “black box” and
do not provide any insight about the process and relations leading to successful classification. In this study, to
avoid this issue, we looked for an explicit linear relation (see Eq. 3). Here, b = (b1,..., bd) is the vector of regression coefficients and b0 is the intercept. By d we refer to the
dimension or number of variables. The symbol T represents the transpose of vector b. By y we refer to the
approximation of the known response y. This is a linear regression model. The classification follows the rule: An important issue of all statistical learning models is data dimensions ( d ). In our case, the dimension is
large ( d = 55 ) for a relatively limited sample size ( n = 79 ). For this reason, one of our goals was to uncover a
minimal set of measures capable of classifying musicians and non-musicians, assuming that some variables are
redundant and some variables may contribute more than others to classification. To this aim, we employed a
sparse learning and filtering (SLF) ­method62,113. This approach presents two advantages: (i) the selected variables
are easier to interpret; (ii) for a given number of observations, the statistical power of the prediction increases
with the reduction of the ­dimension114. SLF follows the principle of the lasso ­method115 by minimizing both
the regression error and the penalized sum of absolute values of coefficients (see Eq. 4). In the equation, L is the
number of observations that serve to learn the coefficients (b0, b); µ indicates the penalization factor. Recent methods in sparse learning have employed a proximal variant of the error function, which is smooth
and facilitates convergence when parameters are selected ­appropriately62,63,113. Notably, these proximal optimi-
zation methods have proven to be successful in supervised classification for big dimension data ( d ∼106)63,113. Sparse learning methods have the property to bring the coefficients bi to 0 by tuning the penalizing factor µ ≥0. The bigger the penalization µ, the more bi tends to converge to 0. The limit case µ = 0 turns to be the basic linear
regression and µ = ∞ puts all bi = 0 thus leading to the constant model y = b0 = 1
L
L
k=1yk. The optimal µ is
found by a trade-off between the classification error and the number of non-zero coefficients bi. We used a standard learning protocol (supervised classification) to assess the classification of musicians
and non-musicians. We divided the observations into three subsets stratified according to each class (i.e., with
balanced percentages of musicians and non-musicians), namely a Train set (60%), a Validation set (20%), and
a Test set (20%). The Train set is used to minimize E(b0, b, µ) (see Eq. 4) and served to select the variables. The
Validation set served as stopping criterion: when prediction errors on Train and Validation sets are approximately
equal, the training iterations are stopped. This prevents the model from overfitting the data, another well-known
issue of learning methods. The data in the Test set was used to assess the prediction behavior of the model for
(3)
y = b0 +
d
i=1bixi = b0 + bTx.
y > 0.5 →musicians
y ≤0.5 →non-musicians.
(4)
E(b0, b, µ) =
L
k=1
yk −b0 −bTxk



Regression Error
+
µ
d
i=1
|bi|


Penalized coeﬃcients. Vol.:(0123456789)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/
new data. We used SLF in all the three models: Perc, based on the entire set of perceptual variables (7 out of 55); Motor, based on the entire set of motor variables (48 out of 55); PMI, based on the selected variables as an out-
come of models Perc and Motor. In Model PMI, we also included the interaction between perceptual and motor
variables selected for this model, as one of the goals of the study was to assess the relation between perceptual
and motor rhythmic abilities in musicians and non-musicians. Starting from model PMI, we derived profiles of rhythmic abilities for each group, expressed by undirected
graphs. The nodes in each graph indicated the variables selected by the model, and the edges represented their
interactions. We estimated the contribution of variables and interactions separately to the classification of musi-
cians and non-musicians. To do so we calculated the squared correlation coefficient between each variable or
interaction and the prediction, and expressed that as a percentage of the total explained variance in the group. We
used this classification procedure based on model PMI to classify musicians and non-musicians, and to classify
the two subgroups of non-musicians. Unsupervised learning (modular clustering)
To uncover clusters within the group of non-musicians we considered the participants as a collection of nodes
V, and link each couple of nodes to form the set of edges E. We thus obtained a network that can be easily repre-
sented mathematically by a similarity matrix S. The value of each entry S(v, w) is the similarity between individu-
als v and w. If x and y are the measures for these two individuals then, in our study, their similarity is given by
the correlation coefficient S(v, w) = corr(x, y). We processed these correlations using modularity ­analysis64,65. Modularity quantifies the degree to which a group can be subdivided into clearly delineated and non-overlapping
clusters. High modularity reflects strong within-cluster links and weaker links between clusters. We maximized
the well-known Newman’s modularity that measures the clustering quality versus a null model. The degree of
node v is defined by sv =
w∈VS(v, w) and M =
v∈Vsv is the sum of degrees. For a given partition g of the
node’s set V, the Modularity ( Q ) is defined as indicated in Eq. (5). Here, δ
g(v), g(w)
= 1 if g(v) = g(w) (that is, v and w are in the same cluster) and 0 otherwise. The null
model is given by the value svsw
2M that is the probability for a random edge to appear between v and w. Then, the
clustering algorithm searches for a partition g that maximizes Q
g
(Eq. 5). Modularity maximization led to
partition the group of non-musicians into two clusters, each including 20 participants (for a representation of
heat matrix showing that intra-cluster similarities are larger than inter-cluster similarities in the dataset, see
Supplementary Materials). Data availability
The dataset generated and analyzed during the current study are available from the corresponding authors on
reasonable request. Received: 6 May 2023; Accepted: 2 January 2024
References

### 1. Janata, P., Tomic, S. T. & Haberman, J. M. Sensorimotor coupling in music and the psychology of the groove. J. Exp. Psychol. Gen. 141, 54–75 (2012).

### 2. Matthews, T. E., Witek, M. A. G., Heggli, O. A., Penhune, V. B. & Vuust, P. The sensation of groove is affected by the interaction

of rhythmic and harmonic complexity. PLoS ONE 14, e0204539 (2019).

### 3. Witek, M. A. G., Clarke, E. F., Wallentin, M., Kringelbach, M. L. & Vuust, P. Syncopation, body-movement and pleasure in groove

music. PLoS ONE 9, e94446 (2014).

### 4. Chen, J. L., Penhune, V. B. & Zatorre, R. J. Listening to musical rhythms recruits motor regions of the brain. Cereb. Cortex 18,

2844–2854 (2008).

### 5. Grahn, J. A. & Brett, M. Rhythm and beat perception in motor areas of the brain. J. Cogn. Neurosci. 19, 893–906 (2007).

### 6. Zatorre, R. J., Chen, J. L. & Penhune, V. B. When the brain plays music: Auditory–motor interactions in music perception and

production. Nat. Rev. Neurosci. 8, 547–558 (2007).

### 7. Cannon, J. J. & Patel, A. D. How beat perception co-opts motor neurophysiology. Trends Cogn. Sci. 25, 137–150 (2021).

### 8. Kotz, S. A., Ravignani, A. & Fitch, W. T. The evolution of rhythm processing. Trends Cogn. Sci. 22, 896–910 (2018).

### 9. Nozaradan, S., Schwartze, M., Obermeier, C. & Kotz, S. A. Specific contributions of basal ganglia and cerebellum to the neural

tracking of rhythm. Cortex 95, 156–168 (2017).

### 10. Colley, I. D., Varlet, M., MacRitchie, J. & Keller, P. E. The influence of visual cues on temporal anticipation and movement

synchronization with musical sequences. Acta Psychol. 191, 190–200 (2018).

### 11. Damm, L., Varoqui, D., De Cock, V. C., Dalla Bella, S. & Bardy, B. Why do we move to the beat? A multi-scale approach, from

physical principles to brain dynamics. Neurosci. Biobehav. Rev. 112, 553–584 (2020).

### 12. Hove, M. J., Fairhurst, M. T., Kotz, S. A. & Keller, P. E. Synchronizing with auditory and visual rhythms: An fMRI assessment of

modality differences and modality appropriateness. NeuroImage 67, 313–321 (2013).

### 13. Patel, A. D. & Iversen, J. R. The evolutionary neuroscience of musical beat perception: The action simulation for auditory predic-

tion (ASAP) hypothesis. Front. Syst. Neurosci. 8, 57 (2014).

### 14. Tranchant, P., Vuvan, D. T. & Peretz, I. Keeping the beat: A large sample study of bouncing and clapping to music. PLoS ONE

11, e0160178 (2016).

### 15. Todd, N. P. & Lee, C. S. The sensory–motor theory of rhythm and beat induction 20 years on: A new synthesis and future per-

spectives. Front. Hum. Neurosci. 9, 444 (2015).

### 16. Sowiński, J. & Dalla Bella, S. Poor synchronization to the beat may result from deficient auditory–motor mapping. Neuropsy-

chologia 51, 1952–1963 (2013).
(5)
Q
g
=

2M
v,w∈V
S(v, w) −svsw
2M

δ
g(v), g(w). Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/

### 17. Fujioka, T., Trainor, L. J., Large, E. W. & Ross, B. Internalized timing of isochronous sounds is represented in neuromagnetic

beta oscillations. J. Neurosci. 32, 1791–1802 (2012).

### 18. Large, E. W. & Jones, M. R. The dynamics of attending: How people track time-varying events. Psychol. Rev. 106, 119–159 (1999).

### 19. Nozaradan, S., Peretz, I., Missal, M. & Mouraux, A. Tagging the neuronal entrainment to beat and meter. J. Neurosci. 31,

10234–10240 (2011).

### 20. Drake, C. & Botte, M. C. Tempo sensitivity in auditory sequences: Evidence for a multiple-look model. Percept. Psychophys. 54,

277–286 (1993).

### 21. Grahn, J. A. & Rowe, J. B. Feeling the beat: Premotor and striatal interactions in musicians and nonmusicians during beat

perception. J. Neurosci. 29, 7540–7548 (2009).

### 22. Kincaid, A. E., Duncan, S. & Scott, S. A. Assessment of fine motor skill in musicians and nonmusicians: Differences in timing

versus sequence accuracy in a bimanual fingering task. Percept. Mot. Skills 95, 245–257 (2002).

### 23. Nave-Blodgett, J. E., Snyder, J. S. & Hannon, E. E. Hierarchical beat perception develops throughout childhood and adolescence

and is enhanced in those with musical training. J. Exp. Psychol. Gen. 150, 314–339 (2021).

### 24. Smith, J. Reproduction and representation of musical rhythms: The effects of musical skill. In The Acquisition of Symbolic Skills

(eds Rogers, D. & Sloboda, J. A.) 273–282 (Springer, 1983).

### 25. Aschersleben, G. Temporal control of movements in sensorimotor synchronization. Brain Cogn. 48, 66–79 (2002).

### 26. Baer, L. H., Thibodeau, J. L. N., Gralnick, T. M., Li, K. Z. H. & Penhune, V. B. The role of musical training in emergent and

event-based timing. Front. Hum. Neurosci. 7, 191 (2013).

### 27. Franĕk, M., Mates, J., Radil, T., Beck, K. & Pöppel, E. Finger tapping in musicians and nonmusicians. Int. J. Psychophysiol. 11,

277–279 (1991).

### 28. Repp, B. H. Sensorimotor synchronization and perception of timing: Effects of music training and task experience. Hum. Mov. Sci. 29, 200–213 (2010).

### 29. Repp, B. H. & Doggett, R. Tapping to a very slow beat: A comparison of musicians and nonmusicians. Music Percept. 24, 367–376

(2007).

### 30. Bégel, V. et al. ‘Lost in time’ but still moving to the beat. Neuropsychologia 94, 129–138 (2017).

### 31. Palmer, C., Lidji, P. & Peretz, I. Losing the beat: Deficits in temporal coordination. Philos. Trans. R. Soc. Lond. B Biol. Sci. 369,

20130405 (2014).

### 32. Phillips-Silver, J. et al. Born to dance but beat deaf: A new form of congenital amusia. Neuropsychologia 49, 961–969 (2011).

### 33. Repp, B. H. Sensorimotor synchronization: A review of the tapping literature. Psychon. Bull. Rev. 12, 969–992 (2005).

### 34. Iversen, J. R., & Patel, A. D. The Beat Alignment Test (BAT): Surveying beat processing abilities in the general population. In: Miyazaki K, et al., editors. Proceedings of the 10th International Conference on Music Perception & Cognition (ICMPC10), Sapporo, Japan, 25-29 August 2008. Adelaide: Causal Productions (465-468) (2008).

### 35. Benoit, C.-E. et al. Musically cued gait-training improves both perceptual and motor timing in Parkinson’s disease. Front. Hum. Neurosci. 8, 494 (2014).

### 36. Grahn, J. A. & Brett, M. Impairment of beat-based rhythm discrimination in Parkinson’s disease. Cortex 45, 54–61 (2009).

### 37. Puyjarinet, F., Bégel, V., Lopez, R., Dellacherie, D. & Dalla Bella, S. Children and adults with attention-deficit/hyperactivity

disorder cannot move to the beat. Sci. Rep. 7, 11550 (2017).

### 38. Bégel, V. et al. Rhythm as an independent determinant of developmental dyslexia. Dev. Psychol. 58, 339–358 (2022).

### 39. Corriveau, K. H. & Goswami, U. Rhythmic motor entrainment in children with speech and language impairments: Tapping to

the beat. Cortex 45, 119–130 (2009).

### 40. Falk, S., Müller, T. & Dalla Bella, S. Non-verbal sensorimotor timing deficits in children and adolescents who stutter. Front. Psychol. 6, 847 (2015).

### 41. Ladányi, E., Persici, V., Fiveash, A., Tillmann, B. & Gordon, R. L. Is atypical rhythm a risk factor for developmental speech and

language disorders? Wiley Interdiscip. Rev. Cogn. Sci. 11, e1528 (2020).

### 42. Lense, M. D., Ladányi, E., Rabinowitch, T.-C., Trainor, L. & Gordon, R. Rhythm and timing as vulnerabilities in neurodevelop-

mental disorders. Philos. Trans. R. Soc. Lond. B Biol. Sci. 376, 20200327 (2021).

### 43. Fiveash, A., Dalla Bella, S., Bigand, E., Gordon, R. L. & Tillmann, B. You got rhythm, or more: The multidimensionality of

rhythmic abilities. Attent. Percept. Psychophys. 84, 1370–1392 (2022).

### 44. Bonacina, S., Krizman, J., White-Schwoch, T., Nicol, T. & Kraus, N. How rhythmic skills relate and develop in school-age children. Glob. Pediatr. Health 6, 2333794X19852045 (2019).

### 45. Bouwer, F. L., Honing, H. & Slagter, H. A. Beat-based and memory-based temporal expectations in rhythm: Similar perceptual

effects, different underlying mechanisms. J. Cogn. Neurosci. 32, 1221–1241 (2020).

### 46. Kasdan, A. V. et al. Identifying a brain network for musical rhythm: A functional neuroimaging meta-analysis and systematic

review. Neurosci. Biobehav. Rev. 136, 104588 (2022).

### 47. Tierney, A. & Kraus, N. Evidence for multiple rhythmic skills. PLoS ONE 10, e0136645 (2015).

### 48. Kraus, N. Of Sound Mind (MIT Press, 2021).

### 49. Dalla Bella, S. et al. BAASTA: Battery for the assessment of auditory sensorimotor and timing abilities. Behav. Res. Methods 49,

1128–1145 (2017).

### 50. Puyjarinet, F. et al. At-home training with a rhythmic video game for improving orofacial, manual, and gait abilities in Parkinson’s

disease: A pilot study. Front. Neurosci. 16, 874032 (2022).

### 51. Verga, L., Schwartze, M., Stapert, S., Winkens, I. & Kotz, S. A. Dysfunctional timing in traumatic brain injury patients: Co-

occurrence of cognitive, motor, and perceptual deficits. Front. Psychol. 12, 731898 (2021).

### 52. Hastie, T., Tibshirani, R. & Friedman, J. The Elements of Statistical Learning (Springer, 2009).

### 53. Jones, N. Computer science: The learning machines. Nature 505, 146–148 (2014).

### 54. Herholz, S. C. & Zatorre, R. J. Musical training as a framework for brain plasticity: Behavior, function, and structure. Neuron

76, 486–502 (2012).
55.	 van Vugt, F. T. & Tillmann, B. Thresholds of auditory–motor coupling measured with a simple task in musicians and non-
musicians: Was the sound simultaneous to the key press? PLoS ONE 9, e87176 (2014).

### 56. Lahav, A., Boulanger, A., Schlaug, G. & Saltzman, E. The power of listening: Auditory–motor interactions in musical training. Ann. N. Y. Acad. Sci. 1060, 189–194 (2005).

### 57. Lotze, M. et al. Activation of cortical and cerebellar motor areas during executed and imagined hand movements: An fMRI

study. J. Cogn. Neurosci. 11, 491–501 (1999).

### 58. Lotze, M., Scheler, G., Tan, H.-R. M., Braun, C. & Birbaumer, N. The musician’s brain: Functional imaging of amateurs and

professionals during performance and imagery. NeuroImage 20, 1817–1829 (2003).

### 59. Lega, C., Stephan, M. A., Zatorre, R. J. & Penhune, V. Testing the role of dorsal premotor cortex in auditory-motor association

learning using transcranical magnetic stimulation (TMS). PLoS ONE 11, e0163380 (2016).

### 60. Wollman, I., Penhune, V., Segado, M., Carpentier, T. & Zatorre, R. J. Neural network retuning and neural predictors of learning

success associated with cello training. Proc. Natl. Acad. Sci. U. S. A. 115, E6056–E6064 (2018).

### 61. Chen, J. L., Rae, C. & Watkins, K. E. Learning to play a melody: An fMRI study examining the formation of auditory-motor

associations. NeuroImage 59, 1200–1208 (2012). Vol.:(0123456789)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/

### 62. Combettes, P. L. & Pesquet, J.-C. A Douglas–Rachford splitting approach to nonsmooth convex variational signal recovery. IEEE

J. Sel. Top. Signal Process. 1, 564–574 (2007).

### 63. Jiu, M. et al. Sparse hierarchical interaction learning with epigraphical projection. Preprint at http://​arxiv.​org/​abs/​1705.​07817

(2021).

### 64. Newman, M. E. J. Modularity and community structure in networks. Proc. Natl. Acad. Sci. U. S. A. 103, 8577–8582 (2006).

### 65. Rubinov, M. & Sporns, O. Complex network measures of brain connectivity: Uses and interpretations. NeuroImage 52, 1059–1069

(2010).

### 66. Ehrlé, N. & Samson, S. Auditory discrimination of anisochrony: Influence of the tempo and musical backgrounds of listeners. Brain Cogn. 58, 133–147 (2005).

### 67. Hsu, P., Ready, E. A. & Grahn, J. A. The effects of Parkinson’s disease, music training, and dance training on beat perception and

production abilities. PLoS ONE 17, e0264587 (2022).

### 68. Spiech, C., Endestad, T., Laeng, B., Danielsen, A. & Haghish, E. F. Beat alignment ability is associated with formal musical train-

ing not current music playing. Front. Psychol. 14, 1034561 (2023).

### 69. Krause, V., Schnitzler, A. & Pollok, B. Functional network interactions during sensorimotor synchronization in musicians and

non-musicians. NeuroImage 52, 245–251 (2010).

### 70. Repp, B. H. & Su, Y.-H. Sensorimotor synchronization: A review of recent research (2006–2012). Psychon. Bull. Rev. 20, 403–452

(2013).

### 71. Repp, B. H. Metrical subdivision results in subjective slowing of the beat. Music Percept. 26, 19–39 (2008).

### 72. Dalla Bella, S. Music and brain plasticity. In The Oxford Handbook of Music Psychology (eds Hallam, S. et al.) 325–342 (Oxford

University Press, 2016).

### 73. Merrett, D. L., Peretz, I. & Wilson, S. J. Moderating variables of music training-induced neuroplasticity: A review and discussion. Front. Psychol. 4, 606 (2013).

### 74. Strait, D. L. & Kraus, N. Biological impact of auditory expertise across the life span: Musicians as a model of auditory learning. Hear. Res. 308, 109–121 (2014).

### 75. Wan, C. Y. & Schlaug, G. Music making as a tool for promoting brain plasticity across the life span. Neuroscientist 16, 566–577

(2010).

### 76. Segado, M., Hollinger, A., Thibodeau, J., Penhune, V. & Zatorre, R. J. Partially overlapping brain networks for singing and cello

playing. Front. Neurosci. 12, 351 (2018).

### 77. Bigand, E. & Poulin-Charronnat, B. Are we ‘experienced listeners’? A review of the musical capacities that do not depend on

formal musical training. Cognition 100, 100–130 (2006).

### 78. Terry, J., Stevens, C. J., Weidemann, G. & Tillmann, B. Implicit learning of between-group intervals in auditory temporal struc-

tures. Attent. Percept. Psychophys. 78, 1728–1743 (2016).

### 79. Tillmann, B., Stevens, C. & Keller, P. E. Learning of timing patterns and the development of temporal expectations. Psychol. Res.

75, 243–258 (2011).

### 80. Tillmann, B. Implicit investigations of tonal knowledge in nonmusician listeners. Ann. N. Y. Acad. Sci. 1060, 100–110 (2005).

### 81. Tillmann, B., Bharucha, J. J. & Bigand, E. Implicit learning of tonality: A self-organizing approach. Psychol. Rev. 107, 885–913

(2000).

### 82. Rohrmeier, M. & Rebuschat, P. Implicit learning and acquisition of music. Top. Cogn. Sci. 4, 525–553 (2012).

### 83. Weiss, M. W. & Peretz, I. Improvisation is a novel tool to study musicality. Sci. Rep. 12, 12595 (2022).

### 84. Jones, M. R., Moynihan, H., MacKenzie, N. & Puente, J. Temporal aspects of stimulus-driven attending in dynamic arrays. Psychol. Sci. 13, 313–319 (2002).

### 85. Selchenkova, T., Jones, M. R. & Tillmann, B. The influence of temporal regularities on the implicit learning of pitch structures. Q. J. Exp. Psychol. 67, 2360–2380 (2014).

### 86. Hannon, E. E. & Trainor, L. J. Music acquisition: Effects of enculturation and formal training on development. Trends Cogn. Sci.

11, 466–472 (2007).

### 87. Politimou, N., Dalla Bella, S., Farrugia, N. & Franco, F. Born to speak and sing: Musical Predictors of language development in

pre-schoolers. Front. Psychol. 10, 948 (2019).

### 88. Putkinen, V., Tervaniemi, M. & Huotilainen, M. Informal musical activities are linked to auditory discrimination and attention

in 2-3-year-old children: An event-related potential study. Eur. J. Neurosci. 37, 654–661 (2013).

### 89. Williams, K. E., Barrett, M. S., Welch, G. F., Abad, V. & Broughton, M. Associations between early shared music activities in the

home and later child outcomes: Findings from the Longitudinal Study of Australian Children. Early Child. Res. Q. 31, 113–124
(2015).

### 90. Aglinskas, A., Hartshorne, J. K. & Anzellotti, S. Contrastive machine learning reveals the structure of neuroanatomical variation

within autism. Science 376, 1070–1074 (2022).

### 91. Richards, B. A. et al. A deep learning framework for neuroscience. Nat. Neurosci. 22, 1761–1770 (2019).

### 92. Shen, X., Houser, T., Smith, D. V. & Murty, V. P. Machine-learning as a validated tool to characterize individual differences in

free recall of naturalistic events. Psychon. Bull. Rev. 30(1), 308–16 (2023).

### 93. Yarkoni, T. & Westfall, J. Choosing prediction over explanation in psychology: Lessons from machine learning. Perspect. Psychol. Sci. 12, 1100–1122 (2017).

### 94. Agres, K. R. et al. Music, computing, and health: A roadmap for the current and future roles of music technology for health care

and well-being. Music Sci. 4, 2059204321997709 (2021).

### 95. Vempala, N. N. & Russo, F. A. Modeling music emotion judgments using machine learning methods. Front. Psychol. 8, 2239

(2017).

### 96. Farrugia, N., Lamouroux, A., Rocher, C., Bouvet, J. & Lioi, G. Beta and theta oscillations correlate with subjective time during

musical improvisation in ecological and controlled settings: A single subject study. Front. Neurosci. 15, 6723 (2021).

### 97. Tierney, A., White-Schwoch, T., MacLean, J. & Kraus, N. Individual differences in rhythm skills: Links with neural consistency

and linguistic ability. J. Cogn. Neurosci. 29, 855–868 (2017).

### 98. Niarchou, M. et al. Genome-wide association study of musical beat synchronization demonstrates high polygenicity. Nat. Hum. Behav. 6, 1292–1309 (2022).

### 99. Tierney, A. T. & Kraus, N. The ability to tap to a beat relates to cognitive, linguistic, and perceptual skills. Brain Lang. 124,

225–231 (2013).

### 100. Bailey, J. A. & Penhune, V. B. Rhythm synchronization performance and auditory working memory in early- and late-trained

musicians. Exp. Brain Res. 204, 91–101 (2010).

### 101. Zuk, J., Benjamin, C., Kenyon, A. & Gaab, N. Behavioral and neural correlates of executive functioning in musicians and non-

musicians. PLoS ONE 9, e99868 (2014).

### 102. Robinaugh, D. J., Hoekstra, R. H. A., Toner, E. R. & Borsboom, D. The network approach to psychopathology: A review of the

literature 2008–2018 and an agenda for future research. Psychol. Med. 50, 353–366 (2020).

### 103. Dalla Bella, S., Dotov, D., Bardy, B. & Cochen de Cock, V. Individualization of music-based rhythmic auditory cueing in Par-

kinson’s disease. Ann. N. Y. Acad. Sci. 1423, 308–317 (2018).

### 104. Dalla Bella, S. The use of rhythm in rehabilitation for patients with movement disorders. In Music and the Aging Brain (eds

Cuddy, L. L. et al.) 383–406 (Academic Press, 2020). Vol:.(1234567890)
Scientific Reports | (2024) 14:1135 |
https://doi.org/10.1038/s41598-024-51257-7
www.nature.com/scientificreports/

### 105. Green, D. M. A maximum-likelihood method for estimating thresholds in a yes-no task. J. Acoust. Soc. Am. 93, 2096–2105

(1993).

### 106. Grassi, M. & Soranzo, A. MLP: A MATLAB toolbox for rapid and reliable auditory threshold estimation. Behav. Res. Methods

41, 20–28 (2009).

### 107. Fisher, N. I. Statistical Analysis of Circular Data (Cambridge University Press, 1993).

### 108. Berens, P. CircStat: A MATLAB toolbox for circular statistics. J. Stat. Softw. 31, 1–21 (2009).

### 109. Wilkie, D. Rayleigh test for randomness of circular data. J. R. Stat. Soc. Ser. C Appl. Stat. 32, 311–312 (1983).

### 110. Wing, A. M. & Kristofferson, A. B. Response delays and the timing of discrete motor responses. Percept. Psychophys. 14, 5–12

(1973).

### 111. Schwartze, M., Keller, P. E., Patel, A. D. & Kotz, S. A. The impact of basal ganglia lesions on sensorimotor synchronization,

spontaneous motor tempo, and the detection of tempo changes. Behav. Brain Res. 216, 685–691 (2011).

### 112. Repp, B. H. & Keller, P. E. Adaptation to tempo changes in sensorimotor synchronization: Effects of intention, attention, and

awareness. Q. J. Exp. Psychol. 57, 499–521 (2004).

### 113. Jiu, M., Pustelnik, N., Chebre, M., Janaqv, S. & Ricoux, P. Multiclass SVM with graph path coding regularization for face clas-

sification. In 2016 IEEE 26th Int. Workshop Mach. Learn. Signal Process. MLSP 1–6. (2016).

### 114. Faul, F., Erdfelder, E., Buchner, A. & Lang, A.-G. Statistical power analyses using G*Power 3.1: Tests for correlation and regres-

sion analyses. Behav. Res. Methods 41, 1149–1160 (2009).

### 115. Tibshirani, R. Regression shrinkage and selection via the lasso: A retrospective. J. R. Stat. Soc. Ser. B 73, 273–282 (2011). Acknowledgements
This research was funded by the European Community’s Seventh Framework Programme (EBRAMUS Project, FP7 Initial Training Network, Grant Agreement No. 238157) and by FEDER funds (Languedoc-Roussillon
Region, BAASTA-FEDER project) to SDB and SAK; by Canada Research Chair program funding to SDB (CRC
in music auditory-motor skill learning and new technologies), and by international mobility funds from IMT
Mines Alès to S. J. Author contributions
S. D. B., S. J. and S. A. K.: conception of the study, writing of a first draft of the manuscript; C. E. B., V. B., L. V., E. A. H.:
recruitment and data collection; S. D. B., S. J., N. F., C. E. B.: data analysis and modelling; all authors contributed to
edit the final version of the manuscript. Competing interests
SDB and CEB are on the board of the BeatHealth company dedicated to the design and commercialization of
technological tools for assessing rhythm capacities (e.g. BAASTA), and implementing rhythm-based interven-
tions. Other authors declare no competing interests. Additional information
Supplementary Information The online version contains supplementary material available at https://​doi.​org/​
10.​1038/​s41598-​024-​51257-7. Correspondence and requests for materials should be addressed to S. D. B. or S. A. K. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Open Access  This article is licensed under a Creative Commons Attribution 4.0 International
License, which permits use, sharing, adaptation, distribution and reproduction in any medium or
format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the
Creative Commons licence, and indicate if changes were made. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the
material. If material is not included in the article’s Creative Commons licence and your intended use is not
permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from
the copyright holder. To view a copy of this licence, visit http://​creat​iveco​mmons.​org/​licen​ses/​by/4.​0/.
© The Author(s) 2024
