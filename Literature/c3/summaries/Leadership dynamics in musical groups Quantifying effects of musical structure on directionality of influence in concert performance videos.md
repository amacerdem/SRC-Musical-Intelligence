# Leadership dynamics in musical groups: Quantifying effects of musical structure on directionality of influence in concert performance videos

**Authors:** Sanket Rajeev Sabharwal, Matthew Breaden, Gualtiero Volpe, Antonio Camurri, Peter E. Keller
**Year:** D:20

---

## RESEARCH ARTICLE

Leadership dynamics in musical groups: Quantifying effects of musical structure on
directionality of influence in concert
performance videos
Sanket Rajeev SabharwalID1*, Matthew BreadenID2, Gualtiero VolpeID1, Antonio Camurri1, Peter E. KellerID2,3

### 1 DIBRIS, University of Genoa, Genoa, Italy, 2 MARCS Institute for Brain, Behaviour and Development, Western Sydney University, Penrith, Australia, 3 Center for Music in the Brain, Department of Clinical
Medicine, Aarhus University & The Royal Academy of Music Aarhus, Aarhus, Aalborg, Denmark
* sabharwalsanket@gmail.com
Abstract
Music ensemble performance provides an ecologically valid context for investigating lead-
ership dynamics in small group interactions. Musical texture, specifically the relative
salience of simultaneously sounding ensemble parts, is a feature that can potentially alter
leadership dynamics by introducing hierarchical relationships between individual parts. The present study extended previous work on quantifying interpersonal coupling in musi-
cal ensembles by examining the relationship between musical texture and leader-follower
relations, operationalised as directionality of influence between co-performers’ body
motion in concert video recordings. It was hypothesised that the directionality of influence,
indexed by Granger Causality, would be greater for ‘homophonic’ textures with a clear dis-
tinction between melody and accompaniment parts than for ‘polyphonic’ textures with less
distinction between melody and accompaniment. This hypothesis was tested by using
pose estimation algorithms to track instrumentalists’ body movements in a string quartet
and a clarinet quintet, and then applying Granger Causality analysis to their head motion
to estimate directional influence between instrumentalist pairs for sections of the pieces
that varied in texture. It was found that Granger Causality values were generally higher
(indicating greater directionality of influence) for homophonic than polyphonic textures. Furthermore, considering melody and accompaniment instrument roles revealed more
evidence for the melody instrument influencing accompanying instruments than vice
versa, plus a high degree of directionality among accompanying instruments, in homopho-
nic textures. These observed patterns of directional information flow in co-performer body
motion are consistent with changing leader-follower relations depending on hierarchical
relations between ensemble parts in terms of the relative salience of melodic material in
the musical texture. The finding that automatic pose estimation can detect modulations of
leadership dynamics in standard video recordings under naturalistic performance condi-
tions has implications for investigating interpersonal coordination in large-scale music

## PLOS ONE

PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
1 / 23
a1111111111
a1111111111
a1111111111
a1111111111
a1111111111

## OPEN ACCESS

Citation: Sabharwal SR, Breaden M, Volpe G, Camurri A, Keller PE (2024) Leadership dynamics
in musical groups: Quantifying effects of musical
structure on directionality of influence in concert
performance videos. PLoS ONE 19(4): e0300663.
https://doi.org/10.1371/journal.pone.0300663
Editor: Merryn D. Constable, Northumbria
University, UNITED KINGDOM
Received: June 15, 2023
Accepted: March 1, 2024
Published: April 3, 2024
Copyright: © 2024 Sabharwal et al. This is an open
access article distributed under the terms of the
Creative Commons Attribution License, which
permits unrestricted use, distribution, and
reproduction in any medium, provided the original
author and source are credited. Data Availability Statement: All relevant data
underpinning the results presented in this study,
except for the actual video recordings, are within
the manuscript and its Supporting information
files. Due to ethical considerations and the nature
of consent obtained, the video recordings used for
this research cannot be shared publicly or
distributed. Nevertheless, we have shared the
postural data extracted using Pose Estimation
algorithms on our github repository. The
experiments were performed with full consent for
research and analysis, but the consent does not

video datasets representing different cultural traditions, and for exploring nonverbal com-
munication in group activities more generally. Introduction
Interpersonal coordination and entrainment characterise a wide range of human interactions,
from spontaneous audience applauding to strategic play in team sports and artistically signifi-
cant collective displays in music and dance. Small ensembles of musicians provide a valuable
and practical setting for investigating these phenomena from a variety of perspectives, such as
biomechanical, computational, psychological, and neuroscientific [1–4]. Ensemble co-perform-
ers synchronise their body movements and sounds with high accuracy and flexibility to convey
musical structure and emotive information to one another and the audience. This synchronisa-
tion, achieved through rigorous rehearsal and a shared understanding of musical intent, is criti-
cal for the successful delivery of a performance and the realisation of a collective musical
expression [5–8]. The resulting musical communication is multimodal in the sense that visual
information can play a role in live and recorded performances, even though auditory informa-
tion is typically primary [9–12]. In live performances, the visual component not only facilitates
tighter synchronisation among performers but also enriches the interaction with the audience. In recorded performances, visual cues continue to play a role, as seen in the widespread appre-
ciation and engagement with music videos and live-recorded performances [13, 14]. In addition to body movements that directly trigger sounds, musicians produce movements
that are not technically required for sound production, such as head nods and torso swaying,
but contribute to regulating an individual’s performance while conveying musical structure,
expressive intentions, and underlying musical meaning to others [9, 15, 16]. These movements
may also constitute an embodiment of the musical intentions, where the physical gestures are
intertwined with the sound modulations to enhance the musical expression. In musical ensem-
bles, these ancillary movements, whether consciously intended or reflexive, serve as visual cues
that bolster communication and aid co-performers in synchronising their actions. Visual cues
become especially beneficial at points of heightened uncertainty (e.g., tempo changes or peri-
ods of silence) [17–19], complementing auditory information by providing continuous visual
feedback that co-performers can utilize to anticipate each other’s sounds [20], across multiple
timescales reflecting the hierarchical musical structure [21]. Coordination of sounds occurs on short timescales in the range of milliseconds, whereas
body sway and other movements align over more extended periods corresponding to higher
levels of musical structure, like phrases (i.e., organisational units perceived as coherent when
presented in isolation, analogous to sentences in speech) [21–23]. Previous work has demon-
strated that the coordination of ancillary body motion is systematically related to sound syn-
chrony and ensemble cohesion [7, 23–25], suggesting that visual and auditory information
provide parallel channels for musical communication [26]. Moreover, the coupling between
performers in body movements and sounds is not static but dynamic and changes over time
[27–29]. One aspect of interpersonal coupling that can vary is the degree to which it is sym-
metrical versus asymmetrical, in terms of the directionality of information exchange or influ-
ence among co-performers, which can reflect musical leadership relations [2, 4, 30, 31]. Here,
we use the term ‘leadership’ broadly to refer to a spectrum of relations spanning no leader (as
in bidirectional influence), a single leader and one or more followers, or multiple leaders and
followers.

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
2 / 23
extend to public distribution of the raw video data. For the sake of ethical considerations, all
identifiable characteristics within the video
recordings have been masked to maintain the
privacy and confidentiality of the participants. For
clarity, we’ve also provided the ethics approval
documents for the perusal of the editorial team. Funding: Funded studies: - Authors PEK and MB
were awarded grant number FT140101162 from
the Australian Research Council. URL: https://
dataportal.arc.gov.au/NCGP/Web/Grant/Grant/
FT140101162 - This work was supported through
grant number 824160, awarded as part of the
European Union’s Horizon 2020 (H2020) Research
and Innovation Program. The specific project was
the H2020 Future and Emerging Technologies
Proactive (FETPROACTIVE) ENtrainment and
Synchronization at Multiple TIME Scales in the
MENTal Foundations of Expressive Gesture
(EnTimeMent) Project. URL: https://cordis.europa.
eu/project/id/824160/it - The Center for Music in
the Brain received funding from the Danish
National Research Foundation, grant number
DNRF117. URL: https://dg.dk/en/ The funders had
no role in study design, data collection and
analysis, decision to publish, or preparation of the
manuscript. Competing interests: The authors have declared
that no competing interests exist. In many forms of collaborative joint action, individuals within small groups assume com-
plementary roles, such as leader or follower, observable in tasks ranging from lifting a bulky
item to collective dance [10, 32, 33]. In musical ensembles, explicit leadership roles can be
strategically assigned or dictated by convention (e.g., the first violinist in a string quartet),
whereas implicit roles can emerge spontaneously through constraints related to task struc-
ture or participant characteristics, including individual capabilities and personality [11, 31,
34–36]. Previous research has investigated leadership dynamics in musical ensembles using optical
motion capture systems to track co-performers’ body motion. Early studies with piano duos
demonstrated the sensitivity and reliability of this technique by showing that head movements
of designated leaders precede those of followers [10] and that sound synchrony is high to the
extent that the body sway motion of the pianist playing the melody part precedes motion of
the accompanying pianist [7]. Related work with larger ensembles has investigated the direc-
tionality of information flow in co-performers’ motion by assessing Granger Causality (GC). GC is a statistical hypothesis test used to determine if one time series can predict another. Spe-
cifically, it evaluates whether past values of one time series (e.g., Musician 1’s motion) provide
valuable information in predicting future values of another time series (e.g., Musician 2’s
motion) better than using the past values of the second time series alone. This method thereby
gives insights into potential causal relationships between the two time series [37]. A seminal study used GC to quantity information flow between the baton motion of con-
ductors and bow motion of members of an orchestral string section [2]. This study revealed
that the method was sufficiently sensitive to detect distinct levels of information flow for differ-
ent conductors and counteracting effects where increased conductor influence was associated
with decreased influence among instrumentalists. Additional evidence for the validity of using
GC measures to index ensemble coordination was provided by the finding that the quality of
performances was judged to be high to the extent that the conductor influenced the
instrumentalists. A subsequent study [38] measured GC between head movements of members of a string
quartet while introducing ‘perturbations’ in the form of alterations of rhythm and dynamics
(loudness) known only to the leader. Results indicated that the uni-directional influence of the
leader was reduced, and mutual influence among co-performers increased during periods fol-
lowing the perturbations, especially when playing sections where coordination was challenging
due to complex relations between parts in terms of rhythm, dynamics, or articulation. Consis-
tent with the notion that leadership is especially pertinent to coordination challenges, a study
focusing on head motion in duos consisting of a pianist and a clarinettist found greater direc-
tionality of coupling at the opening section of a piece and in a section characterised by rhyth-
mic uncertainty [34]. Leader-follower relations are thus changeable rather than fixed. Flexibility in leadership was demonstrated in a study showing that secretly assigned leaders in
a string quartet had a greater influence on followers’ body sway than vice versa and that assign-
ing different members as leaders resulted in changes to their relative predictive influence on
co-performers [27]. A positive correlation between the overall information flow and judg-
ments of performance quality was also found. This reinforces the validity of GC as a measure
of interdependencies in body motion and speaks to its relevance in gauging ensemble
cohesion. The findings of studies that applied GC analysis to ensemble motion capture data suggest
that leadership dynamics can be reliably quantified based on directional analysis of body
motion and can change flexibly in response to co-performers’ goals and musical structure. Musical texture is a structural aspect linked to variations in interpersonal coupling in ensemble
performance [27–29]. In music, ‘texture’ denotes the layering of instrumental parts and their

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
3 / 23

relationships, which can often manifest in terms of the relative saliency of parts and the intri-
cacy of their pitch and rhythmic relations [39]. Homophonic textures are characterised by a
strong vertical harmonic relationship between parts, with a clear distinction between melody
and accompaniment [34, 36, 38, 40]. In polyphonic music, by contrast, multiple instruments
or voices play different melodies at the same time, giving each musician some independence
and encouraging the listener to shift the focus of attention horizontally the flow of the multiple
melodies [31, 41–43]. A prior study by Sabharwal et al. [44] examined the effects of texture on interpersonal cou-
pling in small musical groups by analysing the body motion of instrumentalists in videoed
concert performances of ensemble pieces that contained homophonic and polyphonic sec-
tions. This study involved developing a computational framework and system for automatic
pose estimation (huSync) to analyse body motion in video recordings as an alternative to
marker-based motion capture methods, allowing concert performances to be studied conve-
niently in an ecological setting. The pose estimation-based system extracted full-body motion
data for each performer in a string quartet (consisting of two violins, viola, and cello) and a
clarinet quintet (a string quartet with added clarinettist). Then, phase relations between the
head motion trajectories were measured for all possible pairs of performers. Comparing the
results across textures revealed that phase coupling of co-performers’ head motion was gener-
ally stronger for polyphonic textures (where leadership is ambiguous) than for homophonic
textures (where there is a clear melodic leader). Ambiguous or changeable leadership in polyphonic textures thus encourages uniformly
high interpersonal coupling. In contrast, distinct leader-follower roles in homophonic textures
engender lower overall synchrony due to potential asymmetries in coupling. This interpreta-
tion is consistent with laboratory studies showing that dyadic coordination can be less precise
when leader-follower roles are designated than when they are not [45–47], possibly because
the lack of leadership assignment facilitates efficient mutual adaptation and anticipation [48]. However, our previous study did not include directional measures of interpersonal coupling. Therefore, whether the observed differences between homophonic and polyphonic textures
were attributable to different leadership dynamics remained to be determined. The present study addresses this question by examining the relationship between musical
texture and leader-follower roles based on assessment of the directionality of interpersonal
coupling between ensemble co-performers. To this end, we extended the huSync computa-
tional framework and pose estimation-based system for analysing body motion developed by
Sabharwal et al. [44] to compute GC measures between the head motion of pairs of instrumen-
talists in the videoed concert performances. Based on previous work [2, 38], it was assumed
that statistically significant GC tests, which can be computed in both directions within instru-
mentalist pairs, indicate the degree to which each performer exerts influence on the other per-
former within a pair. Our general hypothesis was that interpersonal coupling is more strongly
directional when a clear leadership hierarchy exists and, therefore, that GC tests will yield
more substantial evidence for directional coupling for homophonic than polyphonic textures. Furthermore, we expected that the role of the performer (melody vs. accompaniment) would
modulate the directionality of influence in homophonic textures. Specifically, we hypothesised
that GC tests would more often yield evidence that the performer playing the melody influ-
enced the other performers than vice versa. We did not have an a priori hypothesis about the
directionality of influence among accompanying players in homophonic textures. We
employed linear mixed-effects models (LMM), Analysis of Variance (ANOVA), and General-
ised Linear Mixed Model (GLMM) analyses to assess the effects of musical texture on GC val-
ues and the directionality of influence, with results corroborated across methods for
robustness and reliability.

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
4 / 23

Materials and methods
Dataset
The dataset consisted of videos of performances of two musical pieces featured in a concert
held in 2017 by the Omega Ensemble, a professional chamber music group from Australia. One piece was the Clarinet Quintet in B minor (Op. 115) written by Johannes Brahms
(referred to as Quintet), and the second piece was String Quartet No. 1 in A major written by
Alexander Borodin (referred to as Quartet). The Quartet is scored for violin 1, violin 2, viola,
and cello. The Quintet uses the same string instruments plus a clarinet. The duration of the
Quartet performance was 39 minutes and 13 seconds, while the duration of the Quintet perfor-
mance was 40 minutes and 38 seconds. Both pieces contain four movements with contrasting
musical characters and textural variations that enable the selection of equal numbers of homo-
phonic and polyphonic sections of similar duration. Approval of all ethical and experimental
procedures and protocols was granted by the Human Research Ethics Committee at Western
Sydney University (protocol number H10487) and performed in line with the Declaration of
Helsinki. Members of the Omega Ensemble were recruited in 2017. They provided written
informed consent to participate in the study in the knowledge that individual participants
would be identifiable because the data consisted of video recordings. A previous study using
these videos [44] demonstrated that they are suitable for investigating the effects of textural
variations on interpersonal coordination in musical ensemble performances from a natural
concert setting. However, while our earlier analysis focused on a global measure of interper-
sonal coupling (phase-locking values), the current study focuses specifically on the directional-
ity of coupling (Granger Causality). Videos of the performances were recorded using a Canon 1DX camera body and a Canon
EF 70–200 1:2.8 L zoom lens as QuickTime movies (. MOV) with dimensions 1920 × 1080 pix-
els at 25 frames per second. The full videos were split into parts based on textural annotations
(homophonic and polyphonic) that were made in ELAN [49] based on musicological analysis
of the published scores by author MB, which were checked by author PEK (both authors have
university qualifications in musicology). We operationally defined musical phrases as sections
of the pieces that were made up of coherent thematic material presented in a consistent tex-
ture. Alterations in both the thematic content and texture serve as phrase boundaries. Although the resulting phrase units are sometimes longer than those typically used in musico-
logical analysis, they provide more suitable units for investigating how structural change affects
the directionality of influence. For each phrase, textural categorisation, the total number of performing instruments, and
instrument roles (such as melody, counter melody, or harmonic accompaniment) were anno-
tated in different layers within the ELAN interface. Data from each layer of the annotated
ELAN file for each piece was extracted to extract video timecodes for each phrase and associ-
ated textural categorisation. The bar numbers from the score corresponding to each excerpt
are provided in S1 Table (For Quintet: Brahms, J. (1892). Clarinet Quintet, Op. 115. N. Sim-
rock.) and S2 Table (For Quartet: Borodin, A. (1884)). String Quartet No. 1. Hamburg: D. Rah-
ter.). Based on this information, phrases that had consistent texture and predominantly all
instruments playing throughout were selected for analysis. In Table 1, we present the selected
phrases used for analysis in our study, and Fig 1 illustrates the specific positioning of musi-
cians, arranged from left to right, along with appropriate labels. We made use of an equal num-
ber of homophonic and polyphonic phrases to have balanced textural classifications and
similar durations (ranging from 15 to 38 s).

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
5 / 23

Computational framework and procedure
The motion data of each performer in the video recordings were extracted through a custom-
ised processing pipeline. Our previous study [44] developed the huSync computational frame-
work utilised by this pipeline, which has been updated to include a new experimental and
analytical approach that addresses the current research questions about information flow
directionality. Fig 2 provides an overview of our approach, which includes four blocks, and is
based on a well-established system for analysing body movements and gestures that convey
expressiveness [50, 51]. The code and data pertinent to this study are openly accessible on
Github. The repository contains fully commented code and detailed instructions to facilitate
straightforward reproducibility. Additionally, the original huSync code is publicly accessible
on Github [44]. Our process was organised into a structured funnel of steps as follows: Table 1. Summary statistics for all texturally consistent phrases in the Quintet and Quartet and the subset selected for analysis based on matching phrase duration. Full Dataset Duration (s) and Count
Selected Phrases Duration (s) and Count
Piece
Texture
Min
Max
Med
Avg
Count
Min
Max
Med
Avg
Count
Brahms
Homophonic
15.03
38.20
19.74
21.57

16.16
38.20
21.60
23.74

Brahms
Polyphonic
15.49
33.08
23.10
23.53

15.49
27.55
20.16
21.11

Borodin
Homophonic
15.30
24.97
18.32
19.12

15.30
24.97
18.32
19.12

Borodin
Polyphonic
15.14
29.63
21.27
21.01

15.14
29.63
20.92
20.80

https://doi.org/10.1371/journal.pone.0300663.t001
Fig 1. Images from the performance of the Quintet (Top Left) and the Quartet (Bottom Left), along with the outputs available with tracked key points
using a pose estimation algorithm (Top Right and Bottom Right). The arrangement of musicians from left to right are labelled as m1 to m4 (Quartet: m1—
violin1, m2—violin2, m3—viola, m4—cello) and m1 to m5 (Quintet: m1—violin1, m2—violin2, m3—viola, m4—cello, m5—clarinet).
https://doi.org/10.1371/journal.pone.0300663.g001

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
6 / 23

Fig 2. An illustration of the huSync computational framework and its system architecture as implemented in our study, showing the transition
from video input signals to statistical analyses. The accompanying images on the right delineate critical phases of the workflow and its intrinsic
procedures.
https://doi.org/10.1371/journal.pone.0300663.g002

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
7 / 23

### 1. After selecting videos based on our analysis criteria (see Table 1), we organised the record-

ings of the chosen phrases and readied them to be passed onto the second phase for feature
extraction (see Fig 2(A)).

### 2. We use AlphaPose [52], a multi-person pose estimation algorithm to extracted motion and

postural data from the chosen video recordings (see Fig 2(B)). The algorithm generates a
JSON file containing the trajectory information of body parts sampled at 30 fps, with the
nose key point serving as the best available representation of the head. We obtain kinematic
information as a position time-series data for further analysis using the nose key point. We
then used the data in the next step to quantify the directionality of influence among per-
formers. To ensure the data are stationary, we applied first-order differencing to the log-
transformed time series, a standard practice based on previous studies [53–55].

### 3. We employed the grangertest function from the lmtest package [56] in R Studio to evaluate

the directionality of information flow. The function measures the predictive relationship
between two time series (see Fig 2(C)). In our analysis, ‘X’ and ‘Y’ symbolise the time series
of movements for any two given performers, respectively, and ‘order’ denotes the number
of lags incorporated in the model (typically set to 1 by default). To illustrate, consider two
arbitrarily chosen performers labeled as J and K; we utilised the grangertest function to
investigate the extent to which the movement of performer J (X) predicts the movement of
performer K (Y), and vice versa (X! Y and Y! X). This method allowed us to assess the
presence of Granger causality within the pair’s interactions. It is important to note that our
measurements within the video frame’s coordinates offer a parallel to each performer’s
bodily movements due to the camera’s fixed orientation relative to the group. This means
that the horizontal axis of our video analysis closely matches the natural horizontal axis of
the performers’ body movements, thus serving as an approximate measure for lateral head
movements. If the p-value yielded by the Granger test was less than.05 (our criterion for
statistical significance), we rejected the null hypothesis and inferred a statistically significant
predictive relationship between the two time series in the specified direction. To account
for the delay between stimulus and response that is common in musical performances [27,
57], as well as in most behaviours, we performed GC tests for a lag of up to 1 second, setting
the order to 30 (equal to the sampling rate) to test for multiple lag-lengths, and examine the
nose key-point separately for each pair in both possible test directions (X! Y and Y! X). We extracted the GC values, including F and p values from each Granger test, and recorded
the binary numbers [0, 1] indicating the outcome of each test. A value of 1 indicates a statis-
tically significant predictive relationship (assumed to indicate influence or information
flow) between the performers in the tested direction, while 0 indicates the absence of a sig-
nificant predictive relationship in that direction. When GC tests in both directions were sta-
tistically significant for a given instrumentalist pair, a ‘1’ was coded for both directions. The
main analyses were based on the proportion of significant GC tests among pairs of musi-
cians for each phrase. Specifically, binary values indicating whether (1) or not (0) each
Granger test was significant were averaged across all pairs of performers (separately for
each test direction, X! Y and Y! X) for each phrase representing the two textures for
each piece. These proportion data were then passed onto the next step to analyse the direc-
tionality of influence among co-performers to address our research questions.

### 4. In this stage (see Fig 2(D)), we carried out several statistical analyses on the GC values we

obtained to address our hypothesis on the directionality of influence. We recorded results for
all possible pairs of instrumentalists for each musical phrase. Note that the aim of these analy-
ses was not to determine whether interaction is taking place at greater than chance levels

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
8 / 23

(given that expert ensembles were intentionally coordinating highly rehearsed performances
in a public concert setting), or whether GC can capture leader-follower relations in ensembles
(since this has been previously demonstrated in a number of studies). Our question instead
concerns the quality of interaction, specifically related to leadership relations, and whether
these relations vary across conditions in relative terms. The results for all pairs for the Quintet
can be found in S3 Table and those for the Quartet in S4 Table. In R, we conducted two pri-
mary statistical analyses [58, 59], one using a linear mixed-effects model (LMM) to test for
general effects of musical texture on GC values, followed by an Analysis of Variance
(ANOVA) to address directionality of influence effects related explicitly to melodic leader-
ship. Musical piece (Brahms Quintet and Borodin Quartet) was included as a random effect
in these analyses since we did not have hypotheses regarding the pieces (they comprised a
convenience sample that were on the ensemble’s program at the time of data collection), but
rather were interested effects that generalise beyond them. Shapiro-Wilk tests indicated that
proportion data were not normally distributed in some conditions, even following arcsine
transformation. Therefore, we report analyses on untransformed data (additional analyses
with arcsin-transformed data yielded similar results). However, given these violations of the
normality assumption, we also conducted binomial Generalised Linear Mixed Model
(GLMM) analyses on raw binary GC values to check whether equivalent effects are obtained. Obtaining consistent outcomes for the LMM and GLMM analyses would provide evidence
for the robustness and reliability of results. Such consistency was observed, and we only
report the LMM and ANOVA results in the article (because these tests are standard and facil-
itate comparison with other studies in the literature). Due to the large number of GC tests
run per musical excerpt (to assess exhaustive pairwise relations between instrumentalists), we
addressed the issue of potential false positives by correcting for multiple comparisons using
the Bonferroni method in supplementary analyses reported in S1 Appendix (see S1 Appen-
dix). The results were overall consistent with those reported here. Results
Fig 3 shows network plots of GC values representing statistically significant directional link-
ages for individual instrument pairings as a function of musical texture in the Quintet and
Quartet performances. Visual inspection of the plots reveals that connections are denser for
the Quintet than the Quartet. This effect was not of interest in the present study, since musical
piece was considered as a random effect in our analyses. Note that comparing the pieces would
be problematic and inconclusive because they vary on multiple confounding parameters (e.g.,
number of players, composer, tempi, key, and stylistic elements). Of note, it is also evident that there is a greater density of connections for homophonic than
polyphonic textures, consistent with our main hypothesis that interpersonal coupling would
generally exhibit higher directionality in homophonic textures with a clear melodic leader
compared to polyphonic textures with distributed or changing leadership roles. Evidence for
or against our additional specific hypothesis that the melody player would influence other
players more than vice versa in homophonic textures is less readily discernable from visual
inspection of these network plots alone since numerous connections exist not just between the
melody player and other instrumentalists, but also among these other players. This under-
scores the fact that our observations are grounded in a probabilistic framework, reflecting ten-
dencies not certainties. For example, while findings suggest a melody player often assumes a
leadership role, it does not rule out influential interactions from other ensemble members. Separate statistical analyses on the GC values were conducted to address each of the two
hypotheses.

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
9 / 23

General effect of musical texture
The hypothesis that interpersonal coupling would exhibit higher directionality in homophonic
textures than polyphonic textures was tested by examining the proportion of instrumentalist
pairs exhibiting statistically significant GC test values as a function of musical texture. The
results in Fig 4(A) revealed a higher proportion of significant GC values for homophonic
Fig 3. Directed network plots for ensemble GC values by instrument for each texture in Quintet and Quartet
musical pieces, representing the directionality of influence (DOI). Edge direction indicates DOI across all phrases. Homophonic textures have a clear melodic leader, while leadership is assumed to be distributed in polyphonic
textures. Each node represents an individual instrumentalist, and the yellow dot indicates the melody instruments
(which varied across the analysed phrases for the Quartet) in homophonic textures.
https://doi.org/10.1371/journal.pone.0300663.g003
Fig 4. (A—Left) Proportion of significant GC values for homophonic and polyphonic textures, averaged across the Quintet and
Quartet; (B—Right) Proportion of significant GC values for four categories of musical roles adopted by co-performers,
indicating the directionality of influence in the musical ensemble.
https://doi.org/10.1371/journal.pone.0300663.g004

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
10 / 23

compared to polyphonic textures, thus confirming the hypothesis. To further evaluate this
effect, we computed a LMM using the lme4 package in R [60], with texture as a fixed factor
and piece, part, phrase, and direction of the GC test (within each pair of instrumentalists) as
random effects. We included the piece as a random effect because our hypotheses were not
specific to the two particular musical works featured but rather representative of Western
chamber music in general. A likelihood-ratio test indicated that the full model with texture provided a better fit to the
data than a reduced model, including only the random effects (χ2(1) = 10.90, p <.001; Log
Likelihood = 17.20 (full) vs 11.80 (reduced), AIC = -20.40 vs -11.50, BIC = -3.10 vs 3.37). The
full model revealed a statistically significant effect of texture on GC values (Effect Estimate =
-0.248, SE = 0.070, t = -3.54, p = 0.001, 95% CI [-0.388, -0.107]), indicating that the directional-
ity of coupling was reliably higher in homophonic than polyphonic textures. Specific effects of musical roles
The second analysis tested the hypothesis that the instrument playing the melody would exert
greater influence on instrumentalists playing accompaniment material more than vice versa in
homophonic textures. For this analysis, we classified the GC test outcomes based on the musi-
cal roles of the instrumentalists, which included melody, accompanying (other), or mixed (in
polyphonic settings). We identified four categories of direction of influence, which can be seen
in Fig 4(B): (1) melody instrument influencing accompanying instruments (Melody on
Other), (2) accompanying instruments influencing the melody instrument (Other on Melody),
(3) accompanying instruments influencing other accompanying instruments (Other on
Other) in homophonic textures, and (4) mixed roles in polyphonic textures. GC values were
entered into a LMM with the direction of influence category as a fixed factor and piece, part,
and phrase as random effects. This full model provided a better fit to the data than a reduced
model with only random effects, as indicated by a likelihood-ratio test (χ2(3) = 15.50, p <.01; Log Likelihood = -1.06 (full) vs -8.82 (reduced), AIC = 18.10 vs 27.60, BIC = 37.90 vs 40.00). We conducted a follow-up ANOVA with three planned orthogonal contrasts to determine
the specific effects of the direction of influence. These contrasts compared homophonic leader-
ship categories combined (Melody on Other, Other on Melody, and Other on Other) versus
the mixed polyphonic category (which is equivalent to the analysis reported above, but with
different degrees of freedom), homophonic categories including a melody player (Melody on
Other and Other on Melody) versus the homophonic category without a melody player (Other
on Other), and the category reflecting melody instrument influence on other instruments
(Melody on Other) versus accompanying instrument influence on the melody instrument
(Other on Melody). This analysis indicated that GC values were significantly higher for homo-
phonic than polyphonic textures t(45.1) = 2.849, p =.0066, 95% CI [0.212, 1.235] and for mel-
ody instrument influence on others than for other instrument influence on the melody
instrument t(46.8) = 2.520, p =.015, 95% CI [0.027, 0.238]. This latter finding is consistent
with our specific hypothesis about musical role. In addition, we found that GC values for
homophonic pairings including a melody player were not significantly different from values
for homophonic pairings without a melody player t(46.8) = −1.039, p =.304, 95% CI [-0.278,
0.089]. This post-hoc finding was not hypothesised but is informative to the extent that it indi-
cates high directionality of influence among accompanying instrumentalists. Discussion
The present study investigated the effects of variations in musical texture on leadership
dynamics in musical ensembles by using pose estimation techniques and Granger Causality

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
11 / 23

(GC) measures to assess the directionality of interpersonal coupling between instrumentalists
in videos of concert performances by a string quartet and a clarinet quintet. Our main finding
was that the proportion of significant GC values, representing the directional influence of head
motion in pairs of co-performers, was higher for homophonic textures, where there is a clear
distinction between melody and accompanying parts, compared to polyphonic textures, where
melodic content is distributed across parts. This finding supports the general hypothesis that
the distinction between parts in homophonic textures is associated with leader-follower rela-
tions reflected in higher directionality in interpersonal coupling. Furthermore, our analyses
revealed that the melody instrument had a greater influence on other instruments than vice
versa in homophonic textures, consistent with the assumption that the melody player serves as
the leader. Our results extend our previous findings on non-directional coupling in the same
performances [44] and build on previous studies that used GC to assess leadership dynamics
in other ensemble settings [2, 17, 27, 38, 40, 61] by highlighting specific effects of musical tex-
ture as well as demonstrating the viability of quantifying leader-follower relations from pat-
terns of body motion extracted from naturalistic video recordings. Links between musical texture and leadership
Regarding the effects of musical texture, finding greater directionality in coupling for homo-
phonic textures, with information flowing from melody player to accompanying players more
than vice versa, sheds light on our previous result that phase coupling was generally weaker in
homophonic than polyphonic textures [44]. We previously argued that this finding could be
due to coupling being more evenly distributed across all performers in polyphonic textures,
whereas accompanying performers are mainly coupled to a single melodic leader in homopho-
nic textures. Present results are generally consistent with interpretation, though the finding of
directional influence among accompanying players in homophonic textures adds further
nuance to the picture. Overall, our present results suggest that coupling may be relaxed when leader-follower rela-
tions are demanded by musical structure. Such relaxation may enable leader-follower roles
characterised by asymmetries in the degree to which co-performers engage in temporal adap-
tation and anticipation. During rhythmic interpersonal coordination, temporal adaptation
processes keep interpersonal asynchronies in check by implementing reactive error correction
and anticipatory processes to enable the prediction of upcoming event timing [31, 62]. Previ-
ous work on leader-follower timing suggests that greater adaptation and anticipation is
observed in the follower than the leader at the level of instrumental movements [11, 36, 63,
64], and our results show that such asymmetries may generalise to ancillary body motion. Other movement features that could additionally have contributed to the present results
include higher complexity of motion or greater need for self-regulation in polyphonic textures,
similarly explored in studies probing effects of coordination challenges on ancillary motion [7,
34, 65]. While further investigation is necessary to confirm this using appropriate analytical
techniques, the importance of body motion cues indicates that musical communication might
engage coordination across multiple timescales and sensory modalities [30]. This engagement
could potentially share characteristics with the multimodal nature of diverse communicative
signals, as suggested by prior research [66, 67]. Questions remain about whether the effects of musical texture on leadership dynamics are
affected by other aspects of musical structure, such as phrase position. Our previous study
found that the effect of texture varied depending on position within the musical phrase. Cou-
pling was stronger for polyphonic than homophonic textures at the beginning and middle por-
tions of phrases but then decreased to similar levels at phrase endings. It was argued that

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
12 / 23

leader-follower relations were adopted at phrase endings in polyphonic textures due to coordi-
nation challenges at these points. The tempo tends to slow down at phrase endings and succes-
sive phrases can be separated by silent pauses of variable duration [31]. Previous research has
shown that the resulting uncertainty at phrase boundaries triggers increased communicative
behavior, such as eye gaze and larger amplitude motion [17, 34, 68]. Related work has shown
that leaders tend to make their timing more predictable by increasing the timing regularly
and/or the amplitude of their movements [6, 10, 45, 69]. These behavioural modifications are
instances of a more general phenomenon of coordination smoothers [70]. Based on these pre-
vious findings, direct influence from the melody player to accompanying players could
increase at phrase endings. However, we did not investigate the effects of phrase position in
the current study due to issues of time series length for reliable GC estimates (see Limitations
and future work). Nevertheless, future work could investigate such effects with experimental
manipulations applied over more extended musical sections (e.g., by using specially composed
pieces) where coordination challenges are systematically varied. Examining patterns of infor-
mation flow among accompanying players could be especially revealing in this context [71],
given our finding that such interpersonal dynamics are present and measurable. Another issue relevant to the mechanisms underlying the link between musical texture and
leadership is whether the hierarchical distinction between melody and accompanying parts in
homophonic textures automatically induces leader-follower relations. Previous work with piano
duos has shown melody lead in keystroke asynchronies and body sway [7, 10], but the degree to
which this emerges spontaneously or as a deliberate strategy still needs to be determined. The
finding that leader-follower relations are more consistent at the level of keystrokes than body
sway [7] suggests that the latter may serve strategic purposes or vary in order to display different
expressive intentions. Relatedly, it has been found that the perception of auditory leader-fol-
lower relations, specifically the temporal lag of sound in accompanying versus melody parts, is
susceptible to bottom-up effects of auditory streaming, indicating automatic processing [72],
while head motion is sensitive to leadership instructions, suggesting strategic use of communica-
tive ancillary movements [27]. In the present study, leadership was not explicitly instructed,
which suggests that co-performers negotiated leadership based on structural constraints in the
music. At the same time, the nature of such negotiation has proven difficult to pin down in labo-
ratory studies [73]. Analysing verbal communication between group members during rehearsals
in natural settings [74] is a promising future avenue to address such negotiation. Regardless of whether leader-follower relations emerge spontaneously or through expressed
intentions, attention plays a pivotal role in directing information flow. Ensemble performers,
when employing “prioritised integrative attending,” balance the distribution of attention
between their own parts and those of their co-performers, while also monitoring the overall
ensemble sound [39]. Despite one’s part presumably being the highest priority [75] in the case
of homophonic textures, accompanying players may allocate attentional resources dispropor-
tionally toward the melody part, as well as to parts played by other accompanying players. The
melody player, while also emphasising their own part, might be receptive to these dynamics. These attentional strategies, whether intentionally implemented or automatically emergent,
could influence interpersonal coupling directionally, given the established links between atten-
tion and sensory-motor coupling [31, 76, 77]. The bidirectional adjustments intrinsic to
ensemble settings further add to the complexity of these interactions. Benefits of studying natural coordination
Our study adds to the growing literature showing that body movement, including head
motion, provides an valid metric to investigate interpersonal coordination and leadership

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
13 / 23

dynamics in group settings [2, 27, 30]. Moreover, we demonstrate the potential of markerless
motion capture technology to analyse such leader-follower dynamics in videos of music
ensemble performances recorded during live concerts. Studying such performances is infor-
mative as they offer a naturalistic setting for musical communication. While this context
presents an ecologically valid representation of ensemble dynamics, it may not be the only
approach to investigating leadership in musical performances. Research on music and dance
underscores the influence of performing “in situ” on communication quality. Factors like
acoustics and audience presence can impact performers’ levels of motivation, attention, and
arousal [78–80]. The nonverbal communication of emotions is a specific aspect that may
benefit under these conditions, and the degree of enhancement may be reflected in increased
information flow. Evidence for this link is seen in a study that found greater information
flow in body sway when a trio were instructed to perform pieces with emotional expression
than without emotion [81]. Heightened expressive intensity may, therefore, be associated
with greater amplitude movements [82, 83] and the transmission of these cues between co-
performers. An additional advantage of using conventional video of ensemble performances is that it
widens the potential pool of materials for analysis. Video-based analysis allows perfor-
mances of other cultures to be studied when more specialised motion capture setups are not
feasible [1], and therefore has the potential to overcome the prevailing WEIRD (Western, Educated, Industrialised, Rich, and Democratic societies) focus of research in psychology
and neuroscience and subdisciplines such as music science [84]. A related practical benefit
is that video is relatively neutral regarding group size, notwithstanding the issue of occlu-
sion in large groups [44], and thus may help to accelerate the trend in the field to go beyond
dyadic coordination to study groups of three or more performers [85]. An advantage of this
upscaling, highlighted by the current results, is that it allowed us to examine the coupling
between instrumentalists playing accompanying parts and interactions between melody and
accompaniment. Our finding that the “other on other” influence was almost as strong as the
“melody on other” influence in homophonic textures is noteworthy to the extent it captures
the interaction between accompanying players. This finding suggests that to understand
musical group dynamics, it is important to consider the interconnected network of the
entire ensemble, in which subsets of performers function with some degree of independence
[86]. Such independence is consistent with claims that it is necessary to balance the integra-
tion and segregation of psychological representations of “self” and “other” in ensemble per-
formance [87–89], with the added nuance that there may be relatively high segregation
between melody and accompaniment players, but a high degree of integration among the
accompaniment players. A further benefit of the current approach is conceptual. The observed effects of musical tex-
ture on leadership dynamics were not the result of an explicit experimental manipulation, nor
were they post-hoc or data-driven findings. While these alternative approaches have particular
strengths, experimental methods can lack ecological validity and data-driven findings can be
challenging to interpret due to multiple possible contributing factors. Instead, our approach of
segmenting the videoed performances based on musicological analysis of musical structure
presents a middle ground that balances ecological naturalness and experimental control con-
siderations. This feature highlights the benefit of using ensemble music from notated tradi-
tions, where the score functions as a script that constrains the actions of each performer while
maintaining a degree of freedom for individual expression, as a domain to study the psycho-
logical dynamics of social interaction [3, 4].

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
14 / 23

Limitations and future work
While markerless motion analysis offers significant advantages, it also presents challenges, such
as alterations in frame resolution, occlusion, and lighting conditions. Comparatively, marker-
based systems yield less noisy data than their markerless counterparts despite their higher costs
and potential for causing participant discomfort. This quality disparity might narrow the scope
of research questions that can be effectively addressed using markerless techniques. However,
these techniques provide broader opportunities for studying group interaction, offsetting their
limitations to a certain extent. This trade-off is an important consideration in the choice
between selecting marker-based and markerless motion analysis methods. The huSync system, as currently designed, does not differentiate between lateral (side-to-
side) and vertical (up-down) head movements. It leverages input from a multi-person human
pose estimation (HPE) algorithm, and, based on the musicians’ arrangement within the scene,
it solely utilises position time series along the x-axis (horizontal). However, with advancements
in the HPE domain enabling data extraction in 3D space, there is potential for enhanced analy-
sis by capturing more nuanced motion trajectories of participants in multiple directions. Research findings indicate that different types of head motion play different functional roles in
ensemble music performance, exemplified by head nods being linked to timekeeping [34, 90]. Given this, it may be possible to enhance the performance analysis capabilities of future ver-
sions of HuSync by distinguishing between up-down and side-to-side head motion in relation
to ensemble dynamics. The current version of HuSync also does not account for the encoding
of emotional intent through head movements [91, 92]. Incorporating this aspect could provide
a more nuanced understanding of interpersonal coordination in ensemble settings. It should
nevertheless be acknowledged that, although we foreground head movements, they are not the
exclusive, nor necessarily the paramount, metric for synchronisation in ensemble contexts. While the current study and previous work demonstrate the capability of using GC with
body motion data in providing insights on ensemble leadership dynamics, the relationship of
these measures to the coordination of sounds warrants further attention. We did not include
measures of auditory communication via musical sounds in our analysis, and therefore our
measures focus exclusively on visual nonverbal communication exhibited by ancillary motion. Previous research has established close relations between ensemble coordination at the level of
sounds and body motion [6, 7, 23] and our previous work found correspondences between
overall synchrony and audio event density [44]. Although signal processing techniques exist
for separating sound sources from mixed recordings [93, 94], and recent work has assessed
ensemble synchrony directly from the overall group output using recurrence quantification
analysis [95], the types of recordings we analysed are not well-suited for these techniques. Sound source separation can be problematic to the extent that instrumental timbres are similar
(as is the case of the string sounds in our dataset). The recurrence-based technique has to date
been used to distinguish between coordinated and deliberately uncoordinated sections of a
musical piece (where the composer’s score instructs the performers to play at random in the
uncoordinated section), rather than subtle differences in coordination, let alone leader-fol-
lower relations. An alternative viable avenue for future work is to investigate how listeners and
observers perceive the directionality of effect, as has been done with overall measures of group
coordination [2, 27, 65]. Another issue to address relates to the fact that the present study focused on naturalistic
ensemble performance, and did not compare co-performers’ body motion to movement pat-
terns during solo performance. Previous research has highlighted the relevance of body move-
ments in solo performance for regulating performance and communicating musical structure
and expression [82, 96]. Incorporating a solo performance condition in future studies could

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
15 / 23

provide a baseline for understanding how these functions are fulfilled for different musical tex-
tures in ensemble settings [9, 97]. It also bears mention that we did not directly ascertain dis-
tinct leadership roles from the musicians but inferred them from the intrinsic musical
structure. This means that related patterns of body motion could be influenced by technical
demands related to coordination. A potential avenue for subsequent research is examining the
extent to which homophonic textures allow for more liberal head movements due to dimin-
ished synchronisation demands. A further limitation is that, for technical reasons (see Links between musical texture and
leadership), we did not address the potential effects of position within phrases on leadership
dynamics. GC assumes that time series data are stationary (i.e., free from the drift that makes
summary statistics vary over time). A standard method of dealing with potential non-statio-
narity, higher-order differencing [53, 55], can result in the loss of information regarding serial
dependencies and a reduction in sensitivity to directional information flow. Such losses may
be disproportionately impactful in short time series when introducing lags to maximise the
likelihood of capturing delays in information flow associated with leader-follower relations. Although it is justifiable to apply GC to short time series in contexts where there is no alterna-
tive, such as non-human animal communicative signalling, and when done in parallel with
complementary methods [98], in our view, the appropriateness of doing so for human musical
interaction requires further investigation. Ultimately, it will be beneficial to explore alternative
metrics and modelling techniques to capture dynamics of the strength and directionality of
coupling in musical groups [86, 99, 100]. Another limitation relates to sample size. Our study focuses on members of a professional
ensemble performing in two constellations, a string quartet and a clarinet quintet. It is there-
fore best considered a proof-of-principle case study that takes advantage of the availability of
data from a top international ensemble. This raises questions about the generality of findings
and, in particular, how the effects of musical texture on leadership dynamics might be affected
by factors such as the particular musical piece, as well as musical expertise and familiarity with
co-performers. Effects of musical piece were not analysed in the current study because the
quartet and quintet varied on a range of stylistic parameters beyond the number of performers
involved. Examining these factors systematically across a series of studies will be necessary to
disentangle their effects in future work. Regarding familiarity, a study of piano duos found that familiarity with a co-performer part
facilitates the coordination of ancillary head motion and body sway, however, not necessarily
instrument keystrokes [23]. Another study found that incongruent performance goals (con-
cerning tempo changes) were resolved with rehearsal via stylistic assimilation [73]. However,
that study did not resolve how leader-follower dynamics played a role in this process. There is
evidence that such relations may become less relevant with increasing familiarity. An analysis
of repeat performances by a string quartet [71] revealed that, as co-performers converged on a
common stylistic interpretation and their body sway became more similar across repeats, the
overall degree of information flow (assessed by GC) decreased, possibly because performers
came to rely on feedforward processes driven by internal models rather than actual feedback
[42, 89, 101]. Our findings suggest that in future work, it would be worthwhile to examine over-
all information flow and the specific directionality of information flow under such conditions
as a function of musical texture and performers’ roles as melody or accompanying players. Conclusion
Our study used automatic pose estimation and Granger Causality measures to investigate the
effects of musical texture on leadership dynamics reflected in instrumentalists’ head motion in

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
16 / 23

videos of live concert performances of ensemble music. Findings indicate that structural fea-
tures related to the hierarchical relationship between instrumental parts that vary in musical
salience influence the directionality of influence between co-performers’ head motion. We
observed greater directionality of influence in homophonic musical textures characterised by
distinct melody and accompaniment parts, with information flowing from the melody to
accompanying players, and among accompanying players, than for polyphonic textures with
less clear distinction. Musical texture thus not only influences the strength of interpersonal
coupling [44], but also its directionality. These results provide proof of principle that automatic pose estimation is sufficiently sensi-
tive to detect subtle modulations of interpersonal coupling and intricate leader-follower
dynamics in standard video recordings under naturalistic conditions. This extends work on
musical leadership to real-life contexts, and opens the door to future investigations of a wider
range of leadership phenomena. These include studying the dynamics of coupling directional-
ity among accompanying performers, examining different ensemble types and musical styles,
measuring motion from different body parts, and exploring the relationship between interper-
sonal coupling dynamics of body motion and both objective and subjective measures of the
coordination of musical sounds. While our findings are context-specific to musical performances, they offer potential
insights into the dynamics of leader-follower relationships in small-group interactions. To the
extent that musical ensembles operate as self-regulating teams aiming for a flawless perfor-
mance under systematically structured conditions governed by objective conventions and con-
straints (e.g., a musical score), they present an ideal opportunity to explore nonverbal
communication in group activities more generally [3]. Using video-based pose estimation to
analyse large publicly available datasets of real-world performances across cultures and group
sizes will maximise the potential use of music to study the communication dynamics of social
groups. Supporting information
S1 Appendix. Binomial Generalised Linear Mixed Model (GLMM) analyses and additional
analyses with Bonferroni correction.
(PDF)
S1 Table. Table for Brahms Quintet with bar numbers.
(PDF)
S2 Table. Table for Borodin Quartet with bar numbers.
(PDF)
S3 Table. Table for Granger Causality test results in Brahms Quintet.
(PDF)
S4 Table. Table for Granger Causality test results in Borodin Quartet.
(PDF)
Acknowledgments
The authors thank the members of the Omega Ensemble, especially Artistic Director and
Founder David Rowden. The authors also thank videographer Bruce Terry for making the
unprocessed video files available and Stephanie Laun for assistance with video annotation.

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
17 / 23

Author Contributions
Conceptualization: Sanket Rajeev Sabharwal, Gualtiero Volpe, Antonio Camurri, Peter E. Keller. Data curation: Sanket Rajeev Sabharwal, Matthew Breaden, Peter E. Keller. Formal analysis: Sanket Rajeev Sabharwal, Peter E. Keller. Funding acquisition: Gualtiero Volpe, Antonio Camurri, Peter E. Keller. Investigation: Sanket Rajeev Sabharwal, Peter E. Keller. Methodology: Sanket Rajeev Sabharwal, Peter E. Keller. Project administration: Sanket Rajeev Sabharwal, Gualtiero Volpe, Antonio Camurri, Peter
E. Keller. Resources: Sanket Rajeev Sabharwal, Peter E. Keller. Software: Sanket Rajeev Sabharwal, Peter E. Keller. Supervision: Gualtiero Volpe, Antonio Camurri, Peter E. Keller. Validation: Sanket Rajeev Sabharwal, Matthew Breaden, Antonio Camurri, Peter E. Keller. Visualization: Sanket Rajeev Sabharwal, Peter E. Keller. Writing – original draft: Sanket Rajeev Sabharwal, Peter E. Keller. Writing – review & editing: Sanket Rajeev Sabharwal, Matthew Breaden, Gualtiero Volpe, Antonio Camurri, Peter E. Keller. References
1. Clayton M., Jakubowski K., Eerola T., Keller P. E., Camurri A., Volpe G., et al. Interpersonal entrain-
ment in music performance. Music Perception 25 November 2020; 38 (2): 136–194. https://doi.org/10.
1525/mp.2020.38.2.136
2. D’Ausilio A., Badino L., Li Y., Tokay S., Craighero L., Canto R., et al. Leadership in orchestra emerges
from the causal relationships of movement kinematics. PLoS ONE, 7, e35757, 2012. https://doi.org/
10.1371/journal.pone.0035757 PMID: 22590511
3. D’Ausilio A., Novembre G., Fadiga L., & Keller P. E. What can music tell us about social interaction? Trends in Cognitive Sciences, Volume 19, Issue 3, 2015, Pages 111–114, ISSN 1364-6613. https://
doi.org/10.1016/j.tics.2015.01.005 PMID: 25641075
4. Volpe G., D’Ausilio A., Badino L., Camurri A., & Fadiga L. Measuring social interaction in music ensem-
bles. Philosophical Transactions of the Royal Society of London. Series B: Biological Sciences, 371
(1693), 2016. https://doi.org/10.1098/rstb.2015.0377 PMID: 27069054
5. Williamon A., & Davidson J. W. Exploring co-performer communication. Musicae Scientiae, 6(1), 53–
72, 2002. https://doi.org/10.1177/102986490200600103
6. Bishop L. Collaborative musical creativity: How ensembles coordinate spontaneity. Frontiers in Perfor-
mance Science, 9, 1285, 2018. https://doi.org/10.3389/fpsyg.2018.01285 PMID: 30087645
7. Keller P. E., & Appel M. Individual differences, auditory imagery, and the coordination of body move-
ments and sounds in musical ensembles. Music Perception, 28, 27–46, 2010. https://doi.org/10.1525/
mp.2010.28.1.27
8. Repp B. H., & Keller P. E. Adaptation to tempo changes in sensorimotor synchronisation: effects of
intention, attention, and awareness. The Quarterly Journal of Experimental Psychology. A, Human
Experimental Psychology, 57, 499–521, 2004. https://doi.org/10.1080/02724980343000369 PMID:

9. Davidson J. W. Bodily movement and facial actions in expressive musical performance by solo and
duo instrumentalists: Two distinctive case studies. Psychology of Music, 40(5), 595–633, 2012.
https://doi.org/10.1177/0305735612449896
10. Goebl W., & Palmer C. Synchronization of Timing and Motion Among Performing Musicians. Music
Perception, 26, 427–438, 2009. https://doi.org/10.1525/mp.2009.26.5.427

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
18 / 23

11. Timmers R., Endo S., Bradbury A., & Wing A. M. Synchronisation and leadership in string quartet per-
formance: a case study of auditory and visual cues [Original Research]. Frontiers in Psychology, 5,
2014. https://doi.org/10.3389/fpsyg.2014.00645 PMID: 25002856
12. Glowinski D., Dardard F., Gnecco G., Piana S., & Camurri A. Expressive non-verbal interaction in a
string quartet: an analysis through head movements. Journal on Multimodal User Interfaces, 9, 55–
68, 2013. https://doi.org/10.1007/s12193-014-0154-3
13. Ashley R. Musical performance as multimodal communication: drummers, musical collaborators, and
listeners. International Conference on Multimodal Interfaces and the Workshop on Machine Learning
for Multimodal Interaction (ICMI-MLMI’10). Association for Computing Machinery, New York, NY, USA, Article 14, 1.
14. Shoda H., Adachi M. & Umeda T. How live performance moves the human heart PloS one, 2016, 11.4:
e0154322. https://doi.org/10.1371/journal.pone.0154322 PMID: 27104377
15. Nusseck M., & Wanderley M. M. Music and Motion—How Music-Related Ancillary Body Movements
Contribute to the Experience of Music. Music Perception, 26(4), 335–353, 2009. https://doi.org/10.
1525/mp.2009.26.4.335
16. Demos A. P., Chaffin R., & Logan T. Musicians body sway embodies musical structure and expres-
sion: A recurrence-based approach. Musicae Scientiae, 22(2), 244–263, 2018. https://doi.org/10.
1177/1029864916685928
17. Bishop L., Cancino-Chaco´n C., & Goebl W. Eye gaze as a means of giving and seeking information
during musical interaction. Consciousness and Cognition, Volume 68, 2019, Pages 73–96, ISSN
1053-8100. https://doi.org/10.1016/j.concog.2019.01.002 PMID: 30660927
18. Ginsborg J., & Bennett D. Developing Familiarity in a New Duo: Rehearsal Talk and Performance
Cues. Front Psychol, 12, 590987, 2021. https://doi.org/10.3389/fpsyg.2021.590987 PMID:

19. Ginsborg J., & King E. Gestures and glances: The Effects of Familiarity and Expertise on Singers’ and
Pianists’ Bodily Movements in Ensemble Rehearsals. In King E. & Gritten A. (Eds.), New perspectives
on music and gesture (pp. 177–201). Surrey, UK: Ashgate Press. Retrieved from http://urn.fi/URN: NBN:fi:jyu-2009411255
20. Calabrese C., Lombardi M., Bollt E., De Lellis P., Bardy B. G., & di Bernardo M. Spontaneous Emer-
gence of Leadership Patterns Drives Synchronisation in Complex Human Networks. Scientific
Reports, 11(1), 18379, 2021. https://doi.org/10.1038/s41598-021-97656-y PMID: 34526559
21. Laroche J., Tomassini A., Volpe G., Camurri A., Fadiga L., & D’Ausilio A. Interpersonal sensorimotor
communication shapes intrapersonal coordination in a musical ensemble [Original Research]. Fron-
tiers in Human Neuroscience, 16, 2022. https://doi.org/10.3389/fnhum.2022.899676 PMID:

22. MacRitchie J., Varlet M., & Keller P. E. Embodied expression through entrainment and co-representa-
tion in musical ensemble performance. In Lesaffre M. Maes P. J., & Leman M. (Eds.), The Routledge
Companion to embodied music interaction (pp. 150–159). New York: Routledge, 2017.
23. Ragert M., Schroeder T., & Keller P. E. Knowing too little or too much: the effects of familiarity with a
co-performer’s part on interpersonal coordination in musical ensembles. Frontiers in Psychology, 4,
368, 2013. https://doi.org/10.3389/fpsyg.2013.00368 PMID: 23805116
24. Bishop L., & Goebl W. Communication for coordination: gesture kinematics and conventionality affect
synchronisation success in piano duos. Psychological Research 82, 1177–1194, 2018. https://doi.org/
10.1007/s00426-017-0893-3 PMID: 28733769
25. Keller P. E. Joint action in music performance. In Morganti F., Carassa A., & Riva G. (Eds.), Enacting
intersubjectivity: A cognitive and social perspective to the study of interactions (pp. 205–221). Amsterdam, Netherlands: IOS Press, 2008. Retrieved from https://pure.mpg.de/pubman/item/
item_723755_3
26. Davidson J. W. Movement and collaboration in musical performance. In Hallam S., Cross I., & Thaut
M. (Eds.), The Oxford handbook of music psychology (pp. 364–376). Oxford, UK: Oxford University
Press, 2009.
27. Chang A., Livingstone S. R., Bosnyak D. J., & Trainor L. J. Body sway reflects leadership in joint music
performance. Proceedings of the National Academy of Sciences of the United States of America, 114
(21), E4134–E4141, 2017. https://doi.org/10.1073/pnas.1617657114 PMID: 28484007
28. Eerola T., Jakubowski K., Moran N., Keller P. E., & Clayton M. Shared periodic performer movements
coordinate interactions in duo improvisations. Royal Society Open Science, 5(2), 171520, 2018.
https://doi.org/10.1098/rsos.171520 PMID: 29515867
29. Walton A. E., Richardson M. J., Langland-Hassan P., & Chemero A. Improvisation and the self-organi-
sation of multiple musical bodies. Frontiers in Psychology, 6, 313, 2015. https://doi.org/10.3389/fpsyg.

## 2015.00313 PMID: 25941499

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
19 / 23

30. Hilt P. M., Badino L., D’Ausilio A., Volpe G., Tokay S., Fadiga L., et al. Multi-layer adaptation of group
coordination in musical ensembles. Scientific Reports, 9(1), 5854, 2019. https://doi.org/10.1038/
s41598-019-42395-4 PMID: 30971783
31. Keller P. E. Ensemble performance: Interpersonal alignment of musical expression. In Fabian D., Tim-
mers R., & Schubert E. (Eds.), Expressiveness in music performance: Empirical approaches across
styles and cultures (pp. 260–282). Oxford, UK: Oxford University Press, 2014.
32. Chauvigne´ L. A. S., & Brown S. Role-Specific Brain Activations in Leaders and Followers During Joint
Action. Frontiers in Human Neuroscience, 12, 401, 2018. https://doi.org/10.3389/fnhum.2018.00401

## PMID: 30349467

33. Sebanz N., Bekkering H., & Knoblich G. Joint Action: Bodies and Minds Moving Together. Trends in
Cognitive Sciences, 10(2), 70–76, 2006. https://doi.org/10.1016/j.tics.2005.12.009 PMID: 16406326
34. Bishop L., Cancino-Chaco´n C., & Goebl W. Moving to communicate, moving to interact: Patterns of
body motion in musical duo performance. Music Perception 1 September 2019; 37 (1): 1–25. https://
doi.org/10.1525/mp.2019.37.1.1
35. Davidson J. W., & Good J. M. M. Social and musical coordination between members of a string quar-
tet: An exploratory study. Psychology of Music, 30, 186–201, 2002. https://doi.org/10.1177/

36. Wing A. M., Endo S., Bradbury A., & Vorberg D. Optimal feedback correction in string quartet synchro-
nisation. Journal of the Royal Society, Interface, 11, 20131125, 2014. https://doi.org/10.1098/rsif.

## 2013.1125 PMID: 24478285

37. Granger C. W. J. Investigating Causal Relations by Econometric Models and Cross-Spectral Methods. Econometrica, 37(3), 424–438, 1969. https://doi.org/10.2307/1912791
38. Badino L., D’Ausilio A., Glowinski D., Camurri A., & Fadiga L. Sensorimotor communication in profes-
sional quartets. Neuropsychologia, Volume 55, 2014, Pages 98–104, ISSN 0028-3932 https://doi.org/
10.1016/j.neuropsychologia.2013.11.012 PMID: 24333167
39. Keller P. E. Attentional resource allocation in musical ensemble performance. Psychology of Music,
29, 20–38, 2001. https://doi.org/10.1177/0305735601291003
40. Glowinski D., Mancini M., Cowie R., Camurri A., Chiorri C., & Doherty C. The Movements Made by
Performers in a Skilled Quartet: A Distinctive Pattern, and the Function That It Serves. Frontiers in Psy-
chology, 4, 841, 2013. https://doi.org/10.3389/fpsyg.2013.00841 PMID: 24312065
41. Goodman E. Ensemble performance. In Rink J. (Ed.), Musical performance: A guide to understanding
(pp. 153–167). Cambridge, UK: Cambridge University Press, 2002.
42. Keller P. E., Novembre G., & Loehr J. Musical ensemble performance: Representing self, other and
joint action outcomes. In Obhi S. S. & Cross E. S. (Eds.), Shared representations: Sensorimotor foun-
dations of social life (pp. 280–310). Cambridge, UK: Cambridge University Press, 2016.
43. Varni G., Volpe G., & Camurri A. A System for Real-Time Multimodal Analysis of Nonverbal Affective
Social Interaction in User-Centric Media IEEE Transactions on Multimedia, 12, 576–590, 2010.
https://doi.org/10.1109/TMM.2010.2052592
44. Sabharwal S. R., Varlet M., Breaden M., Volpe G., Camurri A., & Keller P. E. huSync—A model and
system for the measure of synchronisation in small groups: A case study on musical joint action. IEEE
Access, 1–1, 2022. https://doi.org/10.1109/ACCESS.2022.3202959
45. Novembre G., Varlet M., Muawiyath S., Stevens C. J., & Keller P. E. The E-music box: an empirical
method for exploring the universal capacity for musical production and for social interaction through
music. Royal Society Open Science, 2(11), 150286, 2015. https://doi.org/10.1098/rsos.150286 PMID:

46. Noy L., Dekel E., & Alon U. The mirror game as a paradigm for studying the dynamics of two people
improvising motion together. Proceedings of the National Academy of Sciences of the United States of
America, 108, 20947–20952, 2011. https://doi.org/10.1073/pnas.1108155108 PMID: 22160696
47. Varlet M., Nozaradan S., Nijhuis P., & Keller P. E. Neural tracking and integration of ‘self’ and ‘other’ in
improvised interpersonal coordination. Neuroimage, 206, 116303, 2020. https://doi.org/10.1016/j.
neuroimage.2019.116303 PMID: 31654761
48. Keller P. E., Novembre G., & Hove M. J. Rhythm in joint action: Psychological and neurophysiological
mechanisms for real-time interpersonal coordination. Philosophical Transactions of the Royal Society
of London. Series B: Biological Sciences, 369 (1658), 20130394, 2014. https://doi.org/10.1098/rstb.

## 2013.0394 PMID: 25385772

49. ELAN. ELAN (Version 6.3) [Computer Software]. Nijmegen: Max Planck Institute for Psycholinguistics, The Language Archive, 2022. Retrieved from https://archive.mpi.nl/tla/elan
50. Camurri A., Mazzarino B., Ricchetti M., Timmers R., & Volpe G. Multimodal Analysis of Expressive
Gesture in Music and Dance Performances. In: Camurri A., Volpe G. (eds) Gesture-Based

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
20 / 23

Communication in Human-Computer Interaction. GW 2003. Lecture Notes in Computer Science(), vol

### 2915. Springer, Berlin, Heidelberg, 2004.

51. Camurri A., Volpe G., Piana S., Mancini M., Niewiadomski R., Ferrari N., et al. The Dancer in the Eye: Towards a Multi-Layered Computational Framework of Qualities in Movement. In Proceedings of the
3rd International Symposium on Movement and Computing (MOCO’16). Association for Computing
Machinery, New York, NY, USA, Article 6, 1–7.
52. Fang H. S., Xie S., Tai Y. W., & Lu C. Rmpe: Regional multi-person pose estimation. In Proceedings of
the IEEE international conference on computer vision (pp. 2334–2343), 2017.
53. Freeman J. R. (1983). Granger Causality and the Times Series Analysis of Political Relationships. American Journal of Political Science, 27(2), 327–358. https://doi.org/10.2307/2111021
54. Zbilut J. P., & Webber C. L. (1992). Embeddings and Delays as Derived from Quantification of
Recurrence Plots. Physics Letters A, 171(3), 199–203. https://doi.org/10.1016/0375-9601(92)
90426-M
55. Zhou Y., Kang Z., Zhang L., & Spanos C. Causal Analysis for Non-Stationary Time Series in Sensor-
Rich Smart Buildings. In Proceedings of the 2013 IEEE International Conference on Automation Sci-
ence and Engineering (pp. 593–598).
56. Zeileis A., & Hothorn T. Diagnostic Checking in Regression Relationships. R News, 2(3), 7–10, 2002.
https://journal.r-project.org/articles/RN-2002-018/RN-2002-018.pdf
57. Meals C. D. The Question of Lag: An Exploration of the Relationship Between Conductor Gesture and
Sonic Response in Instrumental Ensembles. Frontiers in Psychology, 11, 2020. https://doi.org/10.
3389/fpsyg.2020.573030 PMID: 33362639
58. Brown V. A. An introduction to linear mixed-effects modeling in R. Advances in Methods and Practices
in Psychological Science. 2021; 4(1). https://doi.org/10.1177/2515245920960351
59. Harrison X. A., Donaldson L., Correa-Cano M. E., Evans J., Fisher D. N., Goodwin C. E. D., et al. A
Brief Introduction to Mixed Effects Modelling and Multi-Model Inference in Ecology. PeerJ, 6, e4794,
2018. https://doi.org/10.7717/peerj.4794 PMID: 29844961
60. Bates D., Ma¨chler M., Bolker B., & Walker S. Fitting linear mixed-effects models using lme4. Journal of
Statistical Software, 67(1), 1–48, 2015. https://doi.org/10.18637/jss.v067.i01
61. Glowinski D., Badino L., Ausilio A., Camurri A., & Fadiga L. Analysis of leadership in a string quartet. Third International Workshop on Social Behaviour in Music at ACM ICMI 2012, 2012. Retrieved from
http://www.infomus.org/Events/SBM2012/papers/2.pdf
62.
van der Steen M. C., & Keller P. E. The ADaptation and Anticipation Model (ADAM) of sensorimotor
synchronisation. Frontiers in Human Neuroscience, 7, 253, 2013. https://doi.org/10.3389/fnhum.

## 2013.00253 PMID: 23772211

63. Heggli O. A., Cabral J., Konvalinka I., Vuust P., & Kringelbach M. L. A Kuramoto model of self-other
integration across interpersonal synchronisation strategies. PLOS Computational Biology, 15(10),
e1007422, 2019. https://doi.org/10.1371/journal.pcbi.1007422 PMID: 31618261
64. Konvalinka I., Bauer M., Stahlhut C., Hansen L. K., Roepstorff A., & Frith C. D. Frontal alpha oscilla-
tions distinguish leaders from followers: multivariate decoding of mutually interacting brains. Neuro-
Image, Volume 94, 2014, Pages 79–88, ISSN 1053-8119. https://doi.org/10.1016/j.neuroimage.2014.

## 03.003 PMID: 24631790

65. Jakubowski K., Eerola T., Blackwood Ximenes A., Ma W. K., Clayton M., & Keller P. E. Multimodal per-
ception of interpersonal synchrony: Evidence from global and continuous ratings of improvised musical
duo performances. Psychomusicology: Music, Mind, and Brain, 30(4), 159–177, 2020. https://doi.org/
10.1037/pmu0000264
66. Alviar C., Dale R., Dewitt A., & Kello C. Multimodal coordination of sound and movement in music and
speech. Discourse Processes, 57(8), 682–702, 2020. https://doi.org/10.1080/0163853X.2020.

67. Kello C. T., Dalla Bella S., Mede B., & Balasubramaniam R. Hierarchical temporal structure in music,
speech and animal vocalisations: jazz is like a conversation, humpbacks sing like hermit thrushes. J R
Soc Interface, 14(135), 2017. https://doi.org/10.1098/rsif.2017.0231 PMID: 29021158
68. Kawase S. Gazing behaviour and coordination during piano duo performance. Attention, Perception,
& Psychophysics, 76(2), 527–540, 2014. https://doi.org/10.3758/s13414-013-0568-0 PMID:

69. Novembre G., Mitsopoulos Z., & Keller P. E. Empathic perspective taking promotes interpersonal coor-
dination through music. Scientific Reports, 9(1), 12255, 2019. https://doi.org/10.1038/s41598-019-

## 48556-9 PMID: 31439866

70. Vesper C., Butterfill S., Knoblich G., & Sebanz N. A minimal architecture for joint action. Neural Net-
works, 23, 998–1003, 2010. https://doi.org/10.1016/j.neunet.2010.06.002 PMID: 20598504

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
21 / 23

71. Wood E. A., Chang A., Bosnyak D., Klein L., Baraku E., Dotov D. et al. Creating a shared musical inter-
pretation: Changes in coordination dynamics while learning unfamiliar music together. Annals of the
New York Academy of Sciences, 1516(1), 106–113, 2022. https://doi.org/10.1111/nyas.14858 PMID:

72. Ragert M., Fairhurst M. T., & Keller P. E. Segregation and integration of auditory streams when listen-
ing to multi-part music. PLoS ONE, 9, e84085, 2014. https://doi.org/10.1371/journal.pone.0084085

## PMID: 24475030

73. MacRitchie J., Herff S. A., Procopio A., & Keller P. E. Negotiating between individual and joint goals in
ensemble musical performance. Quarterly Journal of Experimental Psychology, 71(7), 1535–1551,
2018. https://doi.org/10.1080/17470218.2017.1339098 PMID: 28585902
74. Pennill N., & Timmers R. Patterns of verbal interaction in newly formed music ensembles [Original
Research]. Frontiers in Psychology, 13, 2022. https://doi.org/10.3389/fpsyg.2022.987775 PMID:

75. Keller P. E., & Burnham D. K. Musical meter in attention to multi-part rhythm. Music Perception, 22,
629–661, 2005. https://doi.org/10.1525/mp.2005.22.4.629
76. Coey C. A., Varlet M., & Richardson M. J. Coordination dynamics in a socially situated nervous sys-
tem. Frontiers in Human Neuroscience, 6, 164–164, 2012. https://doi.org/10.3389/fnhum.2012.00164

## PMID: 22701413

77. Harry B. B., Margulies D. S., Falkiewicz M., & Keller P. E. Brain networks for temporal adaptation,
anticipation, and sensory-motor integration in rhythmic human behaviour. Neuropsychologia, Volume
183, 2023, 108524, ISSN 0028-3932. https://doi.org/10.1016/j.neuropsychologia.2023.108524 PMID:

78. Lee H., & Orgs G. Experiencing art in social settings. In Skov M. & Nadal M. (Eds.), The Routledge
international handbook of Neuroaesthetics (pp. 448–460). New York, USA: Routledge, 2022.
79. Moelants D., Demey M., Grachten M., Wu C.-F., & Leman M. The Influence of an Audience on Per-
formers: A Comparison Between Rehearsal and Concert Using Audio, Video and Movement Data. Journal of New Music Research, 41(1), 67–78, 2012. https://doi.org/10.1080/09298215.2011.

80. Wald-Fuhrmann M., Egermann H., Czepiel A., O’Neill K., Weining C., Meier D. et al. Music Listening in
Classical Concerts: Theory, Literature Review, and Research Program [Review]. Frontiers in Psychol-
ogy, 12, 2021. https://doi.org/10.3389/fpsyg.2021.638783 PMID: 33986708
81. Chang A., Kragness H. E., Livingstone S. R., Bosnyak D. J., & Trainor L. J. Body sway reflects joint
emotional expression in music ensemble performance. Scientific Reports, 9(1), 205, 2019. https://doi.
org/10.1038/s41598-018-36358-4 PMID: 30659220
82. Davidson J. W., & Broughton M. C. Bodily mediated coordination, collaboration, and communication in
music performance. In Hallam S., Cross I., & Thaut M. (Eds.), The Oxford handbook of music psychol-
ogy (pp. 573–595). Oxford, UK: Oxford University Press, 2016.
83. Sevdalis V., & Keller P. E. Perceiving performer identity and intended expression intensity in point-light
displays of dance. Psychological Research, 75, 423–434, 2011. https://doi.org/10.1007/s00426-010-

## 0312-5 PMID: 20981438

84. Jacoby N., Margulis E. H., Clayton M., Hannon E., Honing H., Iversen J., et al. Cross-Cultural Work in
Music Cognition: Challenges, Insights, and Recommendations. Music Perception, 37(3), 185–195,
2020. https://doi.org/10.1525/mp.2020.37.3.185 PMID: 36936548
85. Dotov D., Delasanta L., Cameron D. J., Large E. W., & Trainor L. Collective dynamics support group
drumming, reduce variability and stabilise tempo drift. Elife, 11, e74816, 2022. https://doi.org/10.7554/
eLife.74816 PMID: 36317963
86. Demos A. P. & Palmer C. Social and nonlinear dynamics unite: Musical group synchrony. Trends in
Cognitive Sciences, 2023. https://doi.org/10.1016/j.tics.2023.05.005 PMID: 37277276
87. Heggli O. A., Konvalinka I., Kringelbach M. L., & Vuust P. A metastable attractor model of self-other
integration (MEAMSO) in rhythmic synchronisation. Philosophical Transactions of the Royal Society of
London. Series B: Biological Sciences, 376 (1835), 20200332, 2021. https://doi.org/10.1098/rstb.

## 2020.0332 PMID: 34420393

88. Liebermann-Jordanidis H., Novembre G., Koch I., & Keller P. E. Simultaneous self-other integra-
tion and segregation support real-time interpersonal coordination in a musical joint action task. Acta Psychologica, 218, 103348, 2021. https://doi.org/10.1016/j.actpsy.2021.103348 PMID:

89. Novembre G., Sammler D., & Keller P. E. Neural alpha oscillations index the balance between self-
other integration and segregation in real-time joint action. Neuropsychologia, 89, 414–425, 2016.
https://doi.org/10.1016/j.neuropsychologia.2016.07.027 PMID: 27449708

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
22 / 23

90. Palmer C., Spidle F., Koopmans E., & Schubert P. Ears, heads, and eyes: When singers synchronise
Quarterly journal of experimental psychology, 2006, 72(9), 2272–2287. https://doi.org/10.1177/

91. Thompson W. F., & Russo F. A. Facing the Music. Psychological Science, 18(9), 756–757. 2007.
https://doi.org/10.1111/j.1467-9280.2007.01973.x PMID: 17760767
92. Livingstone SR & Palmer C. Head movements encode emotions during speech and song. Emotion.

### 2016 Apr; 16(3):365–80. Epub 2015 Oct 26. https://doi.org/10.1037/emo0000106 PMID: 26501928

93. Girin L., Gannot S., & Li X. Audio source separation into the wild. In Alameda-Pineda X. Ricci E., &
Sebe N. (Eds.), Multimodal behaviour analysis in the wild (pp. 53–78). Cambridge, USA: Academic
Press, 2019.
94. Pardo B., Liutkus A., Duan Z., & Richard G. Applying source separation to music. In Audio Source Sep-
aration and Speech Enhancement (pp. 345–376). NewYork, USA: Wiley, 2018.
95. Proksch S., Reeves M., Spivey M., & Balasubramaniam R. Coordination dynamics of multi-agent inter-
action in a musical ensemble. Scientific Reports, 12(1), 421, 2022. https://doi.org/10.1038/s41598-

## 021-04463-6 PMID: 35013620

96. Buck B., MacRitchie J., & Bailey N. J. The interpretive shaping of embodied musical structure in piano
performance. Empirical Musicology Review, 8(2), 92–119. https://doi.org/10.18061/emr.v8i2.3929
97. Glowinski D, Riolfo A, Shirole K, Torres-Eliard K, Chiorri C, & Grandjean D. Is he playing solo or within
an ensemble? How the context, visual information, and expertise may impact upon the perception of
musical expressivity. Perception, 43(8), 825–828. https://doi.org/10.1068/p7787 PMID: 25549513
98. Anichini M., de Reus K., Hersh T. A., Valente D., Salazar-Casals A., Berry C., et al. Measuring rhythms
of vocal interactions: a proof of principle in harbour seal pups. Philosophical Transactions of the Royal
Society B: Biological Sciences, 378 (1875), 20210477, 2023. https://doi.org/10.1098/rstb.2021.0477

## PMID: 36871583

99. Hudson D., Wiltshire T. J., & Atzmueller M. multiSyncPy: A Python package for assessing multivariate
coordination dynamics. Behavior Research Methods, 55(2), 932–962, 2023. https://doi.org/10.3758/
s13428-022-01855-y PMID: 35513768
100. Richardson M. J., Garcia R. L., Frank T. D., Gergor M., & Marsh K. L. Measuring group synchrony: a
cluster-phase method for analyzing multivariate movement time-series. Frontiers in physiology, 3,
405, 2012. https://doi.org/10.3389/fphys.2012.00405 PMID: 23091463
101. Mu¨ller V., Ohstro¨m K.-R. P., & Lindenberger U. Interactive brains, social minds: Neural and physiologi-
cal mechanisms of interpersonal action coordination. Neuroscience and Biobehavioral Reviews, 128,
661–677, 2021. https://doi.org/10.1016/j.neubiorev.2021.07.017 PMID: 34273378

## PLOS ONE

Leadership dynamics and influence in music performances
PLOS ONE | https://doi.org/10.1371/journal.pone.0300663
April 3, 2024
23 / 23
