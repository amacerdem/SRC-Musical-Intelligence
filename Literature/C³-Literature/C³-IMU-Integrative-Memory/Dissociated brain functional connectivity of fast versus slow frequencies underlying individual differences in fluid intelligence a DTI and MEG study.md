# Dissociated brain functional connectivity of fast versus slow frequencies underlying individual differences in fluid intelligence: a DTI and MEG study

**Authors:** S. E. P. Bruzzone
**Year:** D:20
**Subject:** Scientific Reports, https://doi.org/10.1038/s41598-022-08521-5

---

Vol.:(0123456789)
Scientific Reports | (2022) 12:4746
| https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports
Dissociated brain functional
connectivity of fast versus slow
frequencies underlying individual
differences in fluid intelligence:
a DTI and MEG study
S. E. P. Bruzzone1,5, M. Lumaca1, E. Brattico1,4, P. Vuust1, M. L. Kringelbach1,2,3 &
L. Bonetti1,2,3*
Brain network analysis represents a powerful technique to gain insights into the connectivity profile
characterizing individuals with different levels of fluid intelligence (Gf). Several studies have used
diffusion tensor imaging (DTI) and slow-oscillatory resting-state fMRI (rs-fMRI) to examine the
anatomical and functional aspects of human brain networks that support intelligence. In this study, we
expand this line of research by investigating fast-oscillatory functional networks. We performed graph
theory analyses on resting-state magnetoencephalographic (MEG) signal, in addition to structural
brain networks from DTI data, comparing degree, modularity and segregation coefficient across
the brain of individuals with high versus average Gf scores. Our results show that high Gf individuals
have stronger degree and lower segregation coefficient than average Gf participants in a significantly
higher number of brain areas with regards to structural connectivity and to the slower frequency
bands of functional connectivity. The opposite result was observed for higher-frequency (gamma)
functional networks, with higher Gf individuals showing lower degree and higher segregation across
the brain. We suggest that gamma oscillations in more intelligent individuals might support higher
local processing in segregated subnetworks, while slower frequency bands would allow a more
effective information transfer between brain subnetworks, and stronger information integration. A fundamental characteristic of the human brain is the plethora of different cognitive abilities that allow us to
flexibly adapt to the ­environment1–3. Among these, intelligence has captured the attention of multiple research
­domains4–8. According to the classification by ­Cattell4, general intelligence (G) can be divided into fluid (Gf)
and crystallized (Gc) intelligence, which are present across the population with measurable inter-individual
­differences1,5. While Gc reflects the previously learned procedures and acquired knowledge, Gf relates to pro-
cesses such as abstract and logical reasoning and visuo-spatial problem-solving1,2,5, only minimally depending
on prior learning and ­acculturation4, and is relatively stable across the ­lifespan8. Typical tasks measuring Gf
correspond to figure analyses and classifications, mental manipulation of series of numbers and letters, and
visuo-spatial ­matrices4. The neural underpinnings of Gf have been extensively studied by means of different techniques for data
acquisition and analysis and various psychometric tests and ­tasks5,9–16. In this respect, one of the most accredited
theories on the neural basis of G is the Parieto-Frontal Integration Theory of intelligence (P-FIT)17,18. According
to this theory, cognitive performance arises from a hierarchical chain of subsequent brain processes. Here, incom-
ing sensory information from temporal and occipital areas is first elaborated in parietal regions and subsequently
integrated and abstracted in the frontal areas of the brain. Although the P-FIT theory is intriguing and well-posed, its approach tends to localise the main brain areas
involved in cognitive processes instead of directly considering the brain as a holistic dynamic network where the
OPEN
1Center for Music in the Brain, Department of Clinical Medicine, Aarhus University & The Royal Academy of Music
Aarhus, Aalborg, Denmark. 2Centre for Eudaimonia and Human Flourishing, Linacre College, University of Oxford, Oxford, UK. 3Department of Psychiatry, University of Oxford, Oxford, UK. 4Department of Education, Psychology, Communication, University of Bari Aldo Moro, Bari, Italy. 5Neurobiology Research Unit (NRU), Rigshospitalet, Copenhagen, Denmark. *email: leonardo.bonetti@clin.au.dk

Vol:.(1234567890)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
resolution of complex cognitive tasks relies on constant communication across the wholebrain. Indeed, recent
research supports the fact that the brain should be considered as a dynamic network and its properties studied
as ­such19,20. In this framework, an optimal efficiency of information flow would be favoured by a balanced ratio
between segregation (i.e., processing of information in local subnetworks) and integration (i.e., processing of
information linking different subnetworks through long-range connections)19,20. Coherently with this perspective and with the P-FIT theory, previous studies showed specific differences
of white matter structure and connectivity patterns in the brain of participants scoring higher in Gf tasks. In
particular, studies using diffusion tensor imaging (DTI) reported an association between greater white matter
integrity in the superior longitudinal fasciculus, an association tract connecting frontal, parietal, temporal and
occipital lobes, and greater Gf scores as measured with the Weschler Adult Scale of Intelligence (WAIS)21–24. In
addition, network analysis of DTI-derived structural connectivity using graph theory measures showed higher
global efficiency and shorter characteristic path length in participants with high versus average Gf ­scores24,25,
supporting the contribution of correctly balanced integration and segregation processing to Gf abilities. In accordance to the anatomical findings, a growing body of evidence based on ­lesion26–28 and functional
magnetic resonance imaging (fMRI) studies pointed at a close link between Gf and a specific subset of brain
regions behaving as hubs within the whole-brain ­network12,29,30. This set of dynamically interacting areas, involv-
ing bilateral temporal, parietal and frontal regions, forms what is also referred to as “multiple demand” (MD)
­network12,29,30 and provides an example of the need for signal integration across spatially segregated brain areas
in Gf. Along this line, former findings from electroencephalography (EEG) studies pointed toward an optimized
brain network configuration in individuals with greater Gf scores and a key role of the parietal and frontal  cor-
tices within such ­network31,32, coherently with both the P-FIT and the MD network theories. However, only a
limited number of studies explored the functional brain networks of Gf using graph theory and real-time neu-
rophysiological measurements such as EEG, while no study to date has used magnetoencephalography (MEG). Given the fast-scale dynamics of brain activity, investigating the brain networks underlying Gf with such meth-
ods would provide more accurate insights about the neurophysiological underpinnings of Gf. Moreover, little
is known about the relationship between functional connectivity in different frequency bands and individual
variation of Gf. Thus, in this study, we used for the first time MEG to explore the differences in the brain networks of high
versus average Gf individuals as emerging from fast-scale whole-brain functional connectivity. Based on resting-
state neural activity (rs-MEG), we computed functional connectivity within five main frequency bands (delta:
0.1–2 Hz, theta: 2–8 Hz alpha: 8–12 Hz, beta: 12–32 Hz, gamma: 32–75 Hz) and investigated the properties of the
fast-scale networks with graph theory measures. In line with previous research, we also explored the organization
of the anatomical networks based on DTI images. We hypothesized to observe a different network organiza-
tion in participants’ brains characterized by a high versus average Gf. With regards to structural connectivity,
according to previous ­literature22,24, we expected to detect a higher proportion of long-range connections as well
as a higher inter-subnetwork connectivity for the high versus average Gf group. Regarding the rs-MEG signal,
we hypothesized to observe different results across the five frequency bands. Specifically, since previous stud-
ies showed the importance of slow brain rhythms for long-range ­communications33–35, we expected to detect a
higher proportion of long-range and inter-subnetwork functional connections among slow bands in high versus
average Gf participants. Conversely, based on the established role of fast frequencies for local ­connectivity33,34,
we hypothesized to observe a higher level of intra-subnetworks communication among gamma band in high
versus average Gfs. Results
Experimental design. In this study, we aimed to characterize the neural correlates of fluid intelligence
by using graph theory measures on functional and structural connectivity. Specifically, we were interested in
measures indexing connectivity of each brain ROIs with the rest of the brain and returning an estimation of
the intra- and inter-subnetworks connectivity. Furthermore, we wished to investigate whether high versus aver-
age Gf participants presented different community structures. For these reasons, we mainly focused on degree,
modularity, and segregation coefficient. We acquired structural DTI using MRI and measured brain activity with MEG during 10 min of resting state
with eyes open. Next, we collected behavioural measures of intelligence using the Wechsler Adult Intelligence
Scale IV (WAIS-IV). The experimental procedures involved a total of 71 participants who gave their informed
consent, but two participants had to be excluded since they did not perform the WAIS-IV tests. Our 69 WAIS-
IV participants were divided into two groups based on their mean Gf and by considering at least one standard
deviation (std; standardized WAIS-IV std = 15) apart, so that the distinction between the two groups was psycho-
metrically meaningful, as suggested by previous literature on the ­topic36–39. The resulting groups were labelled
as high Gf (N = 38; mean Gf = 117.72 ± 4.66) and average Gf (N = 31; mean Gf = 102.98 ± 6.09). As expected, the
difference between the two groups was significant on a statistical level (t-test: p < 1.0e−07, t(55) = 11.08) (See
“Methods” for further background and statistical information on the two groups). Finally, since we had to discard
a few participants due to technical problems during the acquisition of DTI and MEG data, our final sample for
WAIS-IV and DTI analysis consisted of 67 participants, while the one for the WAIS-IV and MEG analysis of
66 participants. Data analysis overview. Based on the non-cerebellar parcels of the automated anatomical labelling (AAL)
brain parcellation, we constructed functional and structural connectivity matrices for each participant. The
structural connectivity matrix was created based on the probabilistic tractography computed across all the 90

Vol.:(0123456789)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
AAL regions of interest (ROIs) of the DTI images. The functional connectivity matrix was realized after recon-
structing the sources of the MEG brain signal,  by using the widely adopted solution named ­beamforming40
(see “Methods” for details) in AAL space. Then, we estimated functional connectivity by computing Pearson’s
correlations between the envelope of the timeseries of each pair of the 90 AAL brain areas. These correlations
have been computed across the whole duration of the MEG recording (approximately 10 min). Importantly, the
functional brain data was reconstructed in five different frequency bands (delta: 0.1–2 Hz, theta: 2–8 Hz alpha:
8–12 Hz, beta: 12–32 Hz, gamma: 32–75 Hz), returning a rather complete picture of the fast-scale information
flow in the brain during resting state. Next, we computed graph theoretical measures of the individual brain
structural and functional networks and compared them between the two groups of participants (high versus
average Gf). Specifically, we were interested in the brain organization in terms of ROIs degree, segregation in different
subnetworks (communities) and intra- and inter-subnetworks connectivity. Moreover, we aimed to detect how
the brains of high versus average Gf participants were organized in terms of structural connections and fast-scale
information flow during resting state. The overview of the analysis pipeline is illustrated in Fig. 1. Structural connectivity. After pre-processing the DTI data, matrices of structural connectivity were con-
structed for every participant using the output of the probabilistic tractography, which was normalized for the
size of the brain ROIs (see “Methods” for details). We constrained the structural matrices to the non-cerebellar
parcels of AAL parcellation (where each of the 90 regions represented a node of the brain network), resulting in
a 90 × 90 matrix. The structural connectivity averaged across participants is shown in Fig. 2A. Functional connectivity. Individual functional connectivity matrices were constructed based on the pre-
processed and source reconstructed MEG data, for each of the five frequency bands considered in the study:
delta, theta, alpha, beta and gamma. As done for the DTI data, the reconstructed neural signal was constrained
to the 90 non-cerebellar AAL parcellation. The resulting 90 × 90 matrix contained the information regarding the
correlations between the 90 AAL brain regions, where each region represented a node of the brain network. The
average functional connectivity across participants is shown in Fig. 2B, independently for each frequency band. Figure 1. Experimental design and analysis pipeline. (A) Participants were divided into two experimental
groups, namely average Gf and high Gf, based on their scoring to perceptual reasoning, working memory,
and speed processing indexed by WAIS-IV. (B) Diffusion-tensor imaging (DTI) data were collected and pre-
processed for both groups. Then, the white matter bundles were modelled using probabilistic tractography.
(C) For both groups, magnetoencephalographic (MEG) data were collected during a 10-min session of resting
state. The data were filtered to analyse five different frequency bands: 0.1–2 Hz (delta), 2–8 Hz (theta), 8–12 Hz
(alpha), 12–32 Hz (beta), 32–74 Hz (gamma). Next, they were source-reconstructed with the beamforming
algorithm. (D) Connectivity was computed for both DTI and MEG data for each subject. The connectivity
matrix for the DTI data was created by computing the probabilistic tractography based on AAL parcellation. The
connectivity matrix for MEG data was estimated by computing the Pearson’s correlations between the envelope
of each pair of brain areas timeseries. (E) Graph measures were used to investigate the structural and functional
brain networks of each group. Degree, modularity, and segregation coefficient provided the most insightful
results. Vol:.(1234567890)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
ROIs degree. We analysed the two types of connectivity using graph theory measures between participants
who scored high versus average in the WAIS-IV. First, we investigated whether the degree of the ROIs across the whole-brain differed among the two Gf
groups, after having verified that the variances of the two groups were not significantly different (p > 0.05). Par-
ticipants belonging to the high versus average Gf group showed significantly higher ROIs degree in both struc-
tural (p = 0.007) and functional networks for theta (p < 0.001), alpha (p < 0.001) and beta (p = 0.004) frequencies,
indicating an overall stronger level of connectivity between ROIs for the high Gf participants (Fig. 3). Remarkably,
the ROIs where this difference was mainly marked for structural connectivity and theta, alpha and beta frequency
bands were provided bilaterally by a widespread network involving frontal (postcentral gyrus, superior frontal
gyrus, postcentral gyrus, supplementary motor area), parietal (inferior and superior parietal lobule), occipital
regions (inferior, middle and superior occipital gyrus) and temporal (middle and superior temporal gyrus)
regions, as well as multiple subcortical areas (parahippocampal gyrus in the structural and in the functional,
hippocampus, cingulum, thalamus in the functional). Conversely, individuals with average Gf scores showed
greater ROIs degree across the whole-brain than the high Gf participants for the gamma frequency (p < 0.001). In this case, stronger degree centrality was observed in frontal, medio-temporal and subcortical areas, regions
that greatly overlap to those that were more central for high versus average Gf scores. A detailed list of the most
central regions and the correspondent degree coefficients in structural and functional brain networks in the two
experimental groups can be found in Table ST1. No significant difference was found for delta frequency band. Community structure and modularity. First, we estimated the community structure and modularity
(depicted in Fig. 5 and reported in Table ST2) using the modularity algorithm introduced by ­Newman41. This
procedure assumes that modularity can be expressed in terms of the eigenvectors of the characteristic matrix
for the network, which Newman named the modularity matrix. Such procedure allows to detect a community
structure of the brain network consisting of a subdivision of non-overlapping subnetworks of nodes (brain ROIs)
that maximizes the number of within-group connections and minimizes the number of between-group connec-
tions (Fig. 5B–F). Modularity refers to a statistic able to quantify the degree to which the network can be divided
Figure 2. Structural and functional whole-brain connectivity. (A) Structural connectivity computed from
DTI data. The circular connectogram and the connectivity matrix represent the connections between the 90
AAL nodes. The different connection strengths are represented by different colour shades. The whole-brain
figures depict the whole-brain connections, with stronger connections being thicker. Colourbars indicate the
normalized average number of streamlines connecting the brain areas. (B) Similarly, functional connectivity
computed from MEG data, for each of the five frequency bands analysed. Colourbars indicate the Pearson’s
correlations, showing the functional connectivity between brain areas. Vol.:(0123456789)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
Figure 3. Degree of connectivity. (A) Degree coefficients of structural and functional connectivity in
participants with high Gf. (B) Degree coefficients of structural and functional connectivity in participants with
average Gf. (C) Contrasts of the degree coefficients between the two groups. In the contrast, the red colour
indicates that high Gf individuals had stronger degree among a significantly higher number of ROIs, while blue
showed a stronger degree among a significantly higher number of ROIs for average Gf participants. This column
illustrates the ROIs whose degree coefficients were stronger than at least one standard deviation above the mean
across all ROIs. (D) Degree depicted for every brain ROI of high, average and high versus average Gf. Each
dot shows the degree of each of the 90 ROIs, independently for high and average Gf participants. Dashed lines
indicate the standard deviation with reference to zero, helping to identify whether the ROIs had a stronger or
weaker degree for high versus average Gf participants. Vol:.(1234567890)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
into clearly delineated subnetworks. Newman’s algorithm is widely adopted in network analysis of the brain and
returns results of demonstrably higher quality than competing methods. Also, it is very fast to ­compute41. Here, we computed the modularity of the brain networks at the group-level, independently for the two
experimental groups (high and average Gf). Then, using MCS we tested the modularity values of structural and
functional connectivity matrices (for the five frequency bands independently) against chance, to detect whether
the brain networks were more inclined to be divided into subnetworks (more divisible into subgroups) than
random configurations of the same original brain networks. The test was significant for both structural and
functional connectivity matrices (p < 0.001). Segregation coefficient. Then, we computed the segregation coefficient and compared it between the Gf
groups. This coefficient, ranging from zero to one, shows the level of connectivity of a ROI with the ROIs belong-
ing to the same community when tending to one, or to ROIs of other communities when tending to zero. Here,
we studied the ROIs segregation coefficient over the whole-brain in the high versus average Gf participants, after
having verified that the variances of the two groups were not significantly different (p > 0.05). The results showed
that high versus average Gfs presented higher ROIs segregation coefficient for both structural connectivity
(p < 0.001) and delta (p < 0.001), theta (p < 0.001) and alpha (p < 0.001) bands of the functional networks (Fig. 4). The ROIs with the strongest segregation coefficient in these frequencies were found bilaterally in parietal, tem-
poral, cingulate and subcortical areas (see Table ST3). Conversely, ROIs with the lowest segregation coefficient
were found in participants with average versus high Gf for the gamma frequency band (p = 0.003), mainly in
frontal, temporal and subcortical regions (Table ST3. No differences were found between the two groups for the
functional connectivity in beta frequency band. Modularity, density, characteristic path length, global and local efficiency. Modularity, density,
characteristic path length, global and local efficiency were not significantly different between the two groups,
neither in the structural nor in the functional networks (p > 0.002). Integration between structural and functional connectivity and Gf. We have carried on an analy-
sis to assess whether we could combine our two modalities (SC and FC) and study such combination in light of
the Gf differences. We computed structural and functional connectivity matrices and correlated them independently for each
participant and frequency band. Afterwards, we grouped the participants into our two experimental groups
(high and average Gf) and tested with an ANCOVA (considering age, sex, and education as covariates) whether
the two groups differed in terms of similarity between structural and functional connectivity. The ANCOVA
was not significant (p > 0.05). Discussion
In this study, we investigated the structural (DTI) and functional connectivity (rs-MEG) differences in individuals
with high versus average Gf scores. We found  a stronger degree for both structural connectivity and the slower
frequency bands of functional connectivity in high compared to average Gf individuals. On the contrary, gamma
band presented stronger degree of brain areas for average versus high Gf. Then, based on the estimation of the
community structure, we computed the segregation coefficient. Brain areas of high versus average Gfs presented
a different community structure and a lower segregation coefficient for structural connectivity and for the slower
frequency bands of functional connectivity, and a higher segregation coefficient for gamma band. Structural connectivity and Gf. After assessing that the computation of our structural and functional
connectivity matrices (illustrated in Fig. 2) returned results coherent with previous ­literature42–46, we investi-
gated them in relation to Gf. Our results for structural connectivity indicated that higher versus average Gf participants presented stronger
long-range and inter-subnetwork connectivity, as reflected by the smaller values of segregation coefficient. These
findings supported previous studies which reported associations between Gf and anatomical connectivity in
the brain. For example, FA measured in the superior longitudinal fasciculus was linked to greater scores in the
Weschler Adult Scale of Intelligence (WAIS) for the Gf ­tasks22. Since the superior longitudinal fasciculus is an
association tract that connects frontal, parietal, temporal and occipital lobes, our results support the perspective
that higher Gf individuals have stronger association and long-range connections. Moreover, Li and ­colleagues24
studied topological properties of the brain networks using graph theory in participants with high and general IQ
scores derived from the Chinese version of the WAIS test. Brain networks of high versus general IQ participants
had higher global efficiencies and shorter characteristic path length, which authors interpreted as a more efficient
parallel transfer of the information in the brain. Although we did not find significant differences in characteristic
path length or in global efficiency, our results about degree, modularity and segregation coefficient are overall
coherent with those by Li and colleagues. Furthermore, the IQ measures used by Li and ­colleagues24 involved not
only Gf, but also Gc tasks, suggesting that such topological measures may be more relevant when approaching
intelligence from a broader perspective. To summarize, on the one hand our work confirmed the main findings provided by previous studies, show-
ing that high versus low/average intelligent individuals have a different network organization, especially whit
regards to long-range connections. On the other hand, our study integrated previous research by highlighting
the specific role of degree, modularity, and segregation coefficient in characterizing the difference between high
versus average Gf people. Vol.:(0123456789)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
Figure 4. Segregation coefficient. (A) Segregation coefficient computed from structural and functional
connectivity in participants with high Gf. (B) Segregation coefficient computed from structural and functional
connectivity in participants with average Gf. (C) Contrasts related to the segregation coefficient between the two
groups. In the contrast, the red colour indicates that high versus average Gf individuals had a weaker segregation
coefficient among a significantly higher number of ROIs, meaning that they presented more inter-subnetwork
connections. Conversely, the blue colour showed that average versus high Gf individuals had a weaker
segregation coefficient among a significantly higher number of ROIs, meaning that they presented more inter-
subnetwork connections. (D) Segregation coefficient of high, average, and high versus average Gf participants. Here, each dot shows the segregation coefficient of each of the 90 ROIs, independently for high and average Gf
participants. Dashed lines indicate the standard deviation with reference to zero, helping to identify whether the
ROIs had a stronger or weaker segregation coefficient for high versus average Gf participants. Vol:.(1234567890)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
Functional connectivity. The main novelty of the current work consisted of investigating differences
between high versus average Gf in relation to five frequency bands emerging from the fast-scale connectivity
computed from rs-MEG. Indeed, differently from our work, previous studies on functional brain networks and intelligence focused on
brain ­lesion26–28 and fMRI. Taken together, they highlighted a subset of brain regions that arguably represented
key hubs for the functional substrate of human ­intelligence12,29,30, comprising bilateral temporal, parietal and
frontal regions of the brain, sometimes described as the MD ­network12,29,30. Furthermore, van den Heuvel and
­colleagues25 computed topological graph theoretical measures on fMRI data, reporting positive correlations
between intellectual performance and the global efficiency of functional brain networks. Finally, a few studies
connected Gf and functional brain networks using ­EEG31,32, suggesting that individuals with greater Gf scores
presented a more optimized brain network configuration. Although this research advanced our knowledge on the functional organization of the brain of intelligent
individuals, previous evidence on the fast-scale functional connectivity of the brain in relation to Gf remained
scarce. Furthermore, no studies used MEG nor showed differences among frequency bands when investigat-
ing the neural underpinning of Gf. Conversely, our research presented a different relationship between Gf and
functional organization of the brain networks when investigating a very fast frequency like gamma or slower
frequencies such as delta, theta, alpha, and beta. Indeed, our results suggested that the functional resting state
network in gamma frequency presented more intra-subnetwork connectivity and thus arguably more segregation
and less information flow across the whole-brain in high versus average Gf. Conversely, higher Gf individuals may
present a stronger integration between brain subnetworks and thus more long-range integration of information
among slower frequency bands. Such findings are coherent with previous literature proposing gamma band for local communication of brain
areas and short-distance information ­flow33,34 and slower rhythms such as alpha and theta for long-range func-
tional connections and communications between brain areas far away from each ­other33–35. In this perspective,
we argue that the investigation of the brain network configuration of fast and slow frequency bands is of great
importance to properly characterize and understand the neural substrate of Gf and integrate previous knowledge,
mainly derived from DTI and fMRI studies. Finally, our analyses returned a different organization of the brain subnetworks in high versus average Gf. As
expected, overall, these subnetworks grouped together brain regions within frontal and temporo-occipital lobes,
independently for the two hemispheres and coherently with previous ­literature42,43,46. Notably, the assignment
of the cingulate gyrus to a brain subnetwork differed between high and average Gf, highlighting the structural
and functional integration of such brain area within frontal subnetworks of the brain in high Gfs. Conversely, in
the average Gf the cingulate was segregated in an independent module for the structural connectivity and less
connected to the frontal subnetworks for the functional connectivity. Although these results do not represent
the focus of our work, they provide further evidence of the difference between the brain network organization
of high and average Gf and may be further explored by future investigations. Conclusions
Altogether, our findings point to a different whole-brain configuration of connectivity between individuals with
high versus average Gf. While our DTI findings confirm and support previous literature about structural con-
nectivity, the MEG results integrate previous knowledge on the brain network organization among slower and
faster frequency bands. Future studies are called to further investigate such phenomenon and provide additional
evidence about the brain mechanisms underlying integration and segregation of the information across brain
subnetworks and their relationship with Gf. Moreover, in our study, we reported network metrics independently derived from both structural and func-
tional connectivity. In addition, we carried out one correlational analysis which combined the two modalities
and investigated them in relation to Gf. Although this analysis did not return significant results, we believe that
more elaborated approaches might. Thus, future research is called for to conduct deeper investigations on how
the integration of structural and functional connectivity is reflected on high and average Gf individuals. For
instance, whole-brain computational modelling of functional connectivity might be performed based on the
structural connectivity and then compared between high versus average Gfs. Finally, while in our study we used solid and well-established metrics for computing functional connectivity
such as Pearson’s correlations of the envelope of the MEG signal, future research may use different measures of
connectivity (e.g. instantaneous phase, moving windows) to investigate the relationship between Gf and dynamic
measures of functional connectivity brain networks. Methods
Participants. We recruited a total of 71 healthy participants, 35 females and 36 males (aged 18–42, mean
age: 25.06 ± 4.11 years) of different nationalities. Two participants had to be excluded since they did not per-
form the WAIS-IV tests. Further, for the DTI data, two participants were excluded from the sample due to the
poor quality of the data, after the computation of the pre-processing pipeline. Thus, the final sample for DTI
consisted of 67 healthy volunteers (34 females, 33 males, mean age: 24.94 ± 4.05 years). Regarding MEG, three
participants were excluded because it was not possible to record their MEG resting state data. Thus, the final
sample for the MEG functional connectivity analyses consisted of 66 healthy volunteers (34 females, 32 males,
24.95 ± 4.24 years). Participants were recruited on a voluntary basis and compensated with vouchers. They were
healthy and not under any medication. Furthermore, they did not report any neurological or psychiatric prob-
lems occurred in their past. Vol.:(0123456789)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
All the experimental procedures were approved by the Ethics Committee of the Central Denmark Region (De
Videnskabsetiske Komitéer for Region Midtjylland) (Ref 1-10-72-411-17), in compliance with the declaration
of Helsinki—Ethical Principles for Medical Research. Moreover, informed consent has been obtained from all
participants before starting with the experimental procedures. Experimental design and overview of the analysis pipeline. In this study, we aimed to investigate
whether structural and fast-scale functional connectivity differed between participants characterized by high
and average levels of fluid intelligence (Gf). Participants underwent the acquisition of functional (magnetoencephalography, MEG) and structural (mag-
netic resonance imaging, MRI) data. We recorded resting-state neurophysiological activity throughout 10 min
of MEG recordings, during which participants were not engaged in any task and kept their eyes open. Regarding
MRI, we acquired T1-anatomical and diffusion-weighted (DTI) brain images. Independently for each partici-
pant, we reconstructed the sources of the MEG signal by combining the MEG with the structural T1 MRI data
in automated anatomical labelling (AAL)43–45,47 space and estimated the functional connectivity between each
pair of non-cerebellar brain areas of AAL. Similarly, we computed individual structural connectivity matrices
in AAL ­space42,46 based on the DTI images. After acquiring the neuro-functional and -structural data, we collected behavioural measures to estimate the
participants’ Gf along the following main scales of the fourth edition of the Wechsler Adult Intelligence Scale
(WAIS-IV)48: perceptual reasoning, working memory and speed processing. All the tests were carried out in
English, which was spoken fluently as a second language by the participants. Finally, as described in the following paragraphs, we used graph theory measures to analyse group differences
between high versus average Gf in both structural and functional brain networks. Participants’ Gf scores. The mean Gf score across the 69 (WAIS-IV subsample), 67 (WAIS-IV and DTI
subsample) or 66 (WAIS-IV and MEG subsample) participants was nearly identical (111.10 ± 9.09; 111.45 ± 9.13
and 110.76 ± 9.05, respectively). Thus, the following numerical information about the two Gf groups (Table 1)
that we have used in our experiment will be reported for the full sample of 69 participants who were admin-
istered the WAIS-IV. Indeed, our sample was divided in two groups based on their mean Gf and by consider-
ing at least one standard deviation (standardized WAIS-IV std = 15) apart, so that the distinction between the
two groups was psychometrically meaningful, as suggested by previous literature on the ­topic36–39. This pro-
cedure yielded two groups: the high Gf group (N = 38; mean Gf = 117.72 ± 4.66); the average Gf group (N = 31;
mean Gf = 102.98 ± 6.09). As conceivable, the difference between the two groups was also statistically significant
(p < 1.0e−07, t(55) = 11.08). Importantly, we controlled that the two groups were matched in terms of socio-eco-
nomical, demographic, and educational status. In both groups, participants were mainly of Danish nationality
and all of them came from a Western cultural country. The High Gf group comprised 15 females and 23 males
with an average age of 25.86 ± 4.89. The Average Gf group comprised 18 females and 13 males with an average
age of 24.00 ± 2.69. The age difference was not significant (p = 0.05). Furthermore, the mean of the education
years was 14.73 ± 4.25 for the high Gf and 14.56 ± 5.87 for the average Gf. Neither this difference was significant
(p = 0.37). MEG data acquisition. We acquired both MRI and MEG data at the Aarhus University Hospital (Den-
mark) in two independent sessions. MEG data were acquired with a 306-channel (204 planar gradiometers and
102 magnetometers) Elekta Neuroimag TRIUX system (Elekta Neuromag, Finland), with a sampling rate of

### 1000 Hz and an analog filter of 0.1–330 Hz. Prior to the measurements, the head shape and spatial coordinates

of each participant were digitalizaed with a 3D digitizer (Polhemus FastrakColchester, VT, USA). The head
localization was determined using four Head Position Indicator coils (cHPI) that were registered with respect to
three anatomical landmarks (fiducials), namely the nasion, left and right preauricular areas. The cHPI allowed
to continuously track the head position in respect to the MEG sensors and to correct for head movements. Fur-
thermore, the digitalization of the participants’ head provided the information for co-registering the functional
data recorded by the MEG with the anatomical data acquired with the MRI. MRI data acquisition. Whole-brain T1-weighted and diffusion-weighted images were acquired with a Sie-
mens Magnetom Skyra 3 T MRI scanner (20-channel head coils) located at Aarhus University Hospital, Den-
mark. T1 images were acquired with the following parameters: 1.0 × 1.0 × 1.0 mm voxel size (1.0 ­mm3); 256 × 256
reconstructed matrix size; 2.96 ms echo time (TE); 5000 ms repetition time (TR); 240 Hz/Px bandwidth. For
the reconstruction of the MEG functional data, each T1-weighted scan was co-registered to the standard brain
Table 1. Participants’ demographic data. Demographic data of the participants divided into the two
experimental groups. Age, Gf and years of education indicate means ± standard deviations. High Gf (n = 38)
Average Gf (n = 31)
Age
Gf
Years of
education
Handedness
Sex
Age
Gf
Years of
education
Handedness
Sex
25.86 ± 4.89
117.72 ± 4.66
14.73 ± 4.25
3 left-
handed

## 15F; 23 M

24.00 ± 2.69
102.98 ± 6.09 14.56 ± 5.87
1 left-
handed

## 18F; 13 M

Vol:.(1234567890)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
Figure 5. Inter and Intra-module connectivity in high versus average Gf. (A) Whole-brain structural and functional connectivity in
all participants. (B) Circular connectogram representing inter- (in gray) and intra-module (different colors) connections in high Gf
participants. (C) Brain modules and intra-module connections overlaid on a standard brain template, in individuals with high Gf. Different modules are represented by edges with different colors. (D) Inter-module connections in individuals with high Gf. Different
modules are represented by dots in different colors, while inter-module connections are represented by grey edges. (E) Circular
connectogram representing inter- (in gray) and intra-module (different colors) connections in average Gf participants. (F) Brain
modules and intra-module connections in individuals with average Gf. Different modules are represented by edges with different
colors. (G) Inter-module connections in individuals with average Gf. Different modules are represented by dots in different colors,
while inter-module connections are represented by grey edges. Vol.:(0123456789)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
template from the Montreal Neurological Institute (MNI) using an affine transformation. Next, it was referenced
to the MEG sensors space with the data about the head shape that was previously digitalized. Diffusion-weighted images were acquired using echo-planar imaging (EPI), with the following parameters:
2.0 × 2.0 × 2.0 mm voxel size (2.0mm3); 104 ms TE; 3300 ms TR; 100 × 100 × 72 matrix size; 221 volumes in ante-
rior–posterior (AP) direction; 1 volume in posterior-anterior (PA) direction; 2500 s/mm2 b-value; 29.41 Hz/Px
bandwidth. DTI data pre‑processing. We pre-processed the MRI diffusion data with the FMRIB’s Diffusion Toolbox
(FDT) toolbox in the FMRIB Software Library (FSL)49,50. First, we visually checked the data to assess the good
quality of the scans. After converting the files into nifti format, we created a reference volume (b0) based on the
first image of both the AP and PA files, which we used to correct for susceptibility-induced distortions resulting
in artefacts at the edge of the brain. Next, based on the corrected b0, we generated a brain mask that we applied
to correct for head motion and eddy currents. In particular, eddy currents refer currents generated in the MRI
machine because of the rapid change of the magnetic field direction during the acquisition (echo planar images
are acquired rapidly in different orientations). The pre-processed and corrected data were subsequently used for the estimation of the main white matter
tracts with probabilistic tractography. Tractography in AAL. We modelled the whole-brain structural connectivity with the FSL probabilistic
tractography for crossing ­fibres51,52, using the AAL parcellation in the MNI152 standard-space T1 weighted
average image. First, based on the pre-processed data and the corrected reference volume b0, we estimated the
fiber orientations of every voxel for each participant. Second, we created 90 seed masks—one for each AAL
region—with voxels sized 2 × 2 × 2mm. Using a Markov Chain Monte Carlo algorithm, we estimated the prob-
ability distribution of fibre direction at each brain voxel, with 1000 fibres (streamlines) per voxel. Whole-brain
tracts (structural connectivity between each pair of AAL brain regions) were estimated by considering the conti-
nuity between fibres of all the voxels contained in each AAL region and all the other AAL regions. Structural connectivity network. After the estimation of the probabilistic tractography, we have com-
puted a few normalization steps to obtain a final structural connectivity matrix, one for each participant. In our brain networks, the nodes were defined according to the AAL parcellation, with each non-cerebellar
AAL parcel representing a node of the network. The networks that we computed were undirected (i.e. a → b = b
→ a). However, the FSL probabilistic tractography estimates independently the two directions of the connec-
tivity between two nodes (i.e. a → b = b → a means the same, but are estimated with slightly different values). Thus, as previously ­done42, we averaged the two directions to obtain only one value of connectivity between
any pair of brain areas and thus a truly symmetric undirected connectivity matrix. Finally, we have normalized
each connection between AAL brain areas for the sizes of the same brain areas. This was done since larger AAL
parcels may present more connections simply because they are larger and not because they are actually more
densely connected. Thus, we have divided each connection between pairs of brain areas by the averaged size of
those brain areas (e.g. a ↔ b/((size of a + size of b)/2)). The resulting 90 × 90 matrix represented an undirected,
weighted brain structural network. MEG data pre‑processing. For the first pre-processing steps of the raw MEG data, we used ­MaxFilter53. These steps consisted in applying signal space separation (SSS) to attenuate interferences originated outside the
scalp, adjusting for head motion and down sampling the signal from 1000 to 250 Hz. Next, we converted the
data into the Statistical Parametric Mapping (SPM) format and further proceeded with the analyses using the
Oxford Centre for Human Brain Activity Software Library (OSL), a freely available toolbox that combines in-
house-built functions with existing tools from ­FSL49, ­SPM54 and ­Fieldtrip55 working in the Matlab environment
(MathWorks, Natick, Massachusetts, United States of America). The frequencies below 0.1 Hz, too low for being
originated by brain activity, were removed with a high-pass filter. In addition, we applied a notch filter to correct
for possible electric current-induced interferences and further down-sampled to 150 Hz. After visually inspect-
ing the data, we removed the parts of the signal that were altered by large artefacts. Then, we performed inde-
pendent-component analysis (ICA)56 to isolate and discard the artefacts generated by eyeblinks and heartbeat. Source reconstruction. The brain sources of the neural activity registered on the scalp by the MEG sen-
sors were estimated by using the OSL implementation of the beamforming algorithm. Specifically, the forward
solution was computed using an overlapping-spheres model in an 8-mm grid (comprising 3559 brain voxels). This solution represented a simplified geometric model of the MNI-co-registered anatomy of each participant,
fitting a sphere separately for each MEG ­sensor40. Then, we performed the inverse solution by using a beamform-
ing algorithm. Such procedure utilized a different set of weights sequentially applied to the source locations for
isolating the contribution of each source to the activity recorded by the MEG sensors at each time-point45,47. Our
beamforming computation was performed using both magnetometers and planar gradiometers. Importantly, the source reconstruction was computed for five different frequency bands that were estimated
after the ICA computation and subsequently reconstructed: delta: 0.1–2 Hz, theta: 2–8 Hz alpha: 8–12 Hz, beta:
12–32 Hz, gamma: 32–75 Hz. Functional connectivity network. After estimating the brain sources of the recorded MEG signal, we
have computed one functional connectivity matrix for each participant, similarly to what we did for the struc-

Vol:.(1234567890)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
tural connectivity based on the DTI data. First, the reconstructed functional data (3559 brain voxels) were con-
strained to the 90 non-cerebellar parcels defined by AAL. Next, we computed the envelope of the time-series
from each brain region using the Hilbert transform. Finally, we estimated the functional connections between
each pair of brain areas by computing Pearson’s correlations between the envelopes of the time-series of each
pair of AAL brain ­regions57. The correlations have been computed across the whole recording of MEG resting
state (approximately 10 min). ROIs degree of connectivity across the whole‑brain. The degree of connectivity describes how con-
nected a node is to the other nodes of the network and can provide information about the functional integra-
tion properties of the network. We computed the degree (d(n)) of node n (here, an AAL ROI) as the sum of the
weighted connections of that node to all other ­nodes20. This provided us with a value for each ROI indicating
its degree of connectivity, and thus its centrality within the whole-brain network. Note that we have used a
weighted measure of degree (i.e. we computed the strength of the connections and not only a binary measure
indicating whether the connections existed or not) to analyse connectivity without losing relevant information. Indeed, both structural and functional connectivity between two ROIs can be reliably described by a weighted
value which provides more information that the binary information telling whether they are connected or not. Since we were interested in the difference of ROIs degree among the whole-brain and not only considering
a few specific ROIs, we did not test the ROIs independently, but we compared the overall difference of ROIs
degree between high versus average Gf participants. Specifically, first we used the Bartlett test to assess whether
the variance within the two groups (high and average Gf) was not significantly different. Second, we computed
the difference between the median of the degree of each ROI for high versus average Gf and tested whether
such differences of medians were different from zero using MCS. If the ROIs degree among the whole-brain is
similar/equal between the two groups, its difference will be approximately zero, with some ROIs slightly above
zero and some others slightly below, by random chance. Conversely, if the degree is different between the two
groups in most of the ROIs, at the higher rate than chance level, then such result indicates a relevant difference
in terms of ROIs degree between the two groups. Thus, in our MCS, we tested whether the distribution of dif-
ferences between high versus average Gf ROIs degree was significantly different from zero. First, we computed
the number of ROIs whose difference degree was higher and lower than zero. Then we permuted the original
data across experimental groups and computed the difference between the median of ROIs degree for the two
permuted Gf groups and observed the distribution of the difference between the degrees with respect to zeros. We re-iterated this operation for 10,000 times, building a reference distribution of the difference between the
ROIs degree in the permuted scenarios. Finally, we compared the original distribution of differences between
high versus average Gf ROIs degree with the permuted distribution. Since we tested the original distribution
considering both tales of the permuted distribution (higher and lower than zero), the final MCS p-value was
obtained by dividing the MCS α level by two (0.05/2 = 0.025). Similarly, for the degree of functional connectivity,
we performed 10 statistical tests: one for each of the two tales of the reference distributions and for each of the
five frequency bands considered in the study. Thus, we corrected for multiple comparisons using the Bonferroni
correction, by dividing the MCS α level (0.05) by 10 (MCS p-value = 0.05/10 = 0.005). Modularity and community structure. Modularity is a value describing the segregation of a network
into discrete, non-overlapping clusters (modules) which optimize the network efficiency for specialized pro-
cessing. In other words, it quantifies the degree to which a network can be subdivided into clearly defined,
non-overlapping subnetworks. According to this definition, we computed the community structure by maxi-
mizing the intra-module connections within non-overlapping sub-modules of the network and minimizing the
inter-module connections. To calculate this measure, we used the undirected measure of modularity developed
by Newman implemented in the Brain Connectivity Toolbox (BCT)20, relying on the eigenvector ­solution41 and
returning a discrete value of modularity and the corresponding community structure, representing the division
of the AAL ROIs into distinct, non-overlapping subnetworks of the brain. While the community structure refers
to a subdivision of the brain networks into non-overlapping subnetworks (Fig. 5), the modularity it a statistic
able to quantify the degree to which the network can be divided into clearly delineated subnetworks. Newman’s
algorithm is widely adopted in network analysis of the brain and returned results of demonstrably higher quality
than competing methods and it is very fast to ­compute41. Here, we computed the modularity of the brain networks at the group-level, independently for the two experi-
mental groups (high and average Gf). Then, we tested whether the modularity of the structural and functional
brain data was significantly different by an equivalent network with connections placed randomly. To do so, we
performed an MCS. First, we computed the modularity of the original data, corresponding to the averaged con-
nectivity matrix (M) across participants. Second, we performed 1000 permutations of matrix M and extracted
the modularity for the permuted data. This procedure yielded a reference distribution of permuted modularity
values. Finally, we considered significant the original modularity value only if it was higher than the 99.9% of
the permuted modularity values. This procedure was computed independently for the structural and functional
data. A graphical depiction of the community structure for structural and functional brain networks is provided
in Fig. 5 and reported in detail in Table ST2. Segregation coefficient. Based on the previously computed community structure, we were interested to
observe whether the ROIs of high and average Gf participants differed in terms of connectivity within and
between the brain subnetworks. Specifically, we expected to find a tendency of high versus average Gf indi-
viduals to have more pronounced connectivity between brain subnetworks. Thus, we computed a ratio that we
referred to as “segregation coefficient”, which indicates whether an ROI is mainly connected to the other ROIs

Vol.:(0123456789)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/
of the same subnetwork or is more connected to ROIs in other subnetworks. The coefficient is computed by
dividing the degree of the ROI a with regards to the ROIs of the same subnetwork by the degree computed for
ROI a with regards to all other ROIs (so also the ones of other subnetworks of the brain). Therefore, the coef-
ficient values range between one and zero: the closer the coefficient to zero, the more the ROI has connections
outside the community, highlighting its relevance as connector hub. Conversely, the closer the value to one, the
greater the within-community degree, indicating that the ROI is mainly central within its own subnetwork. Note
that this coefficient is very similar to the participation coefficient which captures the distribution of a node’s
­connections58. Indeed, the participation coefficient approaches one when a node has equal connections to all
the subnetwork of a network. In our case, we used a slightly different measure (the segregation coefficient) since
we were simply interested in evaluating the ratio of the connections between the node and its subnetwork and
between the same node and every node of the brain network. To test the difference of the whole-brain distribution of the segregation coefficient between high versus aver-
age Gf individuals, we have performed an MCS analogous to the one described for the paragraph on the Degree
of connectivity. Global measures of the brain graph. Although our focus was on degree, modularity, and segregation
coefficient, we reported global measures of the brain graphs (structural and functional) to provide the readers
with complete information. Characteristic path length. The Characteristic path length represents the average shortest path length between
all pairs of nodes composing the network (e.g. the minimum number of connections to connect two nodes on
average), providing a good estimate of how easily information flows through the network (and therefore of the
integration of the network). Global and local efficiency. Local efficiency measures the average efficiency of integration within local clusters
(e.g. between the neighbours of a given node). Global efficiency is the inverse of the characteristic path length and
indicates how effectively the information flows across the network. Density. Density represents the ratio between the number of actual edges of the network and the number of all
possible edges of the network. Before computing density, the network was binarized by removing the weakest 1%
of spurious connections, according to the procedure reported in previous ­studies42,46. Each one of the measures described above (characteristic path length, global and local efficiency, and density)
were statistically compared between high versus average Gf groups by using analyses of covariance, where the
independent variables where the graph measures, the Gf group and sex the between-subject factors and the
covariates were age and years of education. In this case, we corrected for multiple comparisons by using Bonfer-
roni correction (i.e. dividing the α level of 0.05 by the total number of 24 comparisons (four measures × five fre-
quency band of the functional networks plus one structural connectivity network), resulting in 0.05/24 = 0.002). Integration between structural and functional connectivity and Gf. Finally, we have undertaken
an analysis to assess whether we could combine our two modalities (SC and FC) and study such combination in
light of the Gf differences. First, we computed structural and functional connectivity matrices independently for each participant and
frequency band. Then, we computed correlations between the structural connectivity matrix and the functional
connectivity ones, independently for each participant and frequency band. Afterwards, we grouped the par-
ticipants into our two experimental groups (high and average Gf) and tested with ANCOVA (considering age,
sex, and education as covariates) whether the two groups differed in terms of similarity between structural and
functional connectivity. Data availability
The codes are available at the following link: https://​github.​com/​leona​rdob92/​LBPD-1.​0.​git, while the multimodal
neuroimaging data from the experiment are available upon reasonable request. Received: 14 October 2021; Accepted: 9 March 2022
References

### 1. Ashton, M. C., Lee, K., Vernon, P. A. & Jang, K. L. Fluid intelligence, crystallized intelligence, and the openness/intellect factor. J. Res. Pers. https://​doi.​org/​10.​1006/​jrpe.​1999.​2276 (2000).

### 2. Barbey, A. K., Koenigs, M. & Grafman, J. Dorsolateral prefrontal contributions to human working memory. Cortex https://​doi.​

org/​10.​1016/j.​cortex.​2012.​05.​022 (2013).

### 3. Goldstein, S. & Naglieri, J. A. Handbook of executive functioning. Handb. Execut. Funct. https://​doi.​org/​10.​1007/​978-1-​4614-​8106-5

(2014).

### 4. Cattell, R. B. Theory of fluid and crystallized intelligence: A critical experiment. J. Educ. Psychol. https://​doi.​org/​10.​1037/​h0046​

743 (1963).

### 5. Gray, J. R., Chabris, C. F. & Braver, T. S. Neural mechanisms of general fluid intelligence. Nat. Neurosci. https://​doi.​org/​10.​1038/​

nn1014 (2003).

### 6. Gardner, H. & Hatch, T. Educational implications of the theory of multiple intelligences. Educ. Res. https://​doi.​org/​10.​3102/​00131​

## 89X01​80080​04 (1989). Vol:.(1234567890)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/

### 7. Clarke, A. M. & Sternberg, R. J. Beyond IQ: A triarchic theory of human intelligence. Br. J. Educ. Stud. https://​doi.​org/​10.​2307/​

31213​32 (1986).

### 8. Schneider, W., Niklas, F. & Schmiedeler, S. Intellectual development from early childhood to early adulthood: The impact of early

IQ differences on stability and change over time. Learn. Individ. Differ. https://​doi.​org/​10.​1016/j.​lindif.​2014.​02.​001 (2014).

### 9. Santarnecchi, E. et al. Network connectivity correlates of variability in fluid intelligence performance. Intelligence https://​doi.​org/​

10.​1016/j.​intell.​2017.​10.​002 (2017).

### 10. Criscuolo, A., Bonetti, L., Särkämö, T., Kliuchko, M. & Brattico, E. On the association between musical training, intelligence and

executive functions in adulthood. Front. Psychol. 10, 3389 (2019).

### 11. Bonetti, L. et al. Auditory sensory memory and working memory skills: Association between frontal MMN and performance

scores. Brain Res. 1700, 86–98 (2018).

### 12. Duncan, J., Assem, M. & Shashidhara, S. Integrated intelligence from distributed brain activity. Trends Cogn. Sci. https://​doi.​org/​

10.​1016/j.​tics.​2020.​06.​012 (2020).

### 13. Bonetti, L. & Costa, M. Intelligence and musical mode preference. Empir. Stud. Arts 34, 160–176 (2016).

### 14. Bonetti, L. & Costa, M. Musical mode and visual-spatial cross-modal associations in infants and adults. Music. Sci. 23, 50–68

(2019).

### 15. Bonetti, L. et al. Rapid encoding of musical tones discovered in whole-brain connectivity. Neuroimage https://​doi.​org/​10.​1016/j.​

neuro​image.​2021.​118735 (2021).

### 16. Sternberg, R. J. Handbook of Intelligence (Cambridge University Press, 2000).

### 17. Colom, R. et al. Gray matter correlates of fluid, crystallized, and spatial intelligence: Testing the P-FIT model. Intelligence https://​

doi.​org/​10.​1016/j.​intell.​2008.​07.​007 (2009).

### 18. Jung, R. E. & Haier, R. J. The parieto-frontal integration theory (P-FIT) of intelligence: Converging neuroimaging evidence. Behav. Brain Sci. https://​doi.​org/​10.​1017/​S0140​525X0​70011​85 (2007).

### 19. Deco, G., Tononi, G., Boly, M. & Kringelbach, M. L. Rethinking segregation and integration: Contributions of whole-brain model-

ling. Nat. Rev. Neurosci. https://​doi.​org/​10.​1038/​nrn39​63 (2015).

### 20. Rubinov, M. & Sporns, O. Complex network measures of brain connectivity: Uses and interpretations. Neuroimage https://​doi.​

org/​10.​1016/j.​neuro​image.​2009.​10.​003 (2010).

### 21. Basser, P. J. & Pierpaoli, C. Microstructural and physiological features of tissues elucidated by quantitative-diffusion-tensor MRI. J. Magn. Reson. https://​doi.​org/​10.​1016/j.​jmr.​2011.​09.​022 (2011).

### 22. Góngora, D., Vega-Hernández, M., Jahanshahi, M., Valdés-Sosa, P. A. & Bringas-Vega, M. L. Crystallized and fluid intelligence

are predicted by microstructure of specific white-matter tracts. Hum. Brain Mapp. https://​doi.​org/​10.​1002/​hbm.​24848 (2020).

### 23. Hidese, S. et al. Correlation between the wechsler adult intelligence scale-3rd edition metrics and brain structure in healthy

individuals: A whole-brain magnetic resonance imaging study. Front. Hum. Neurosci. https://​doi.​org/​10.​3389/​fnhum.​2020.​00211
(2020).

### 24. Li, Y. et al. Brain anatomical network and intelligence. PLoS Comput. Biol. https://​doi.​org/​10.​1371/​journ​al.​pcbi.​10003​95 (2009).

### 25. Van Den Heuvel, M. P., Stam, C. J., Kahn, R. S. & Hulshoff Pol, H. E. Efficiency of functional brain networks and intellectual

performance. J. Neurosci. https://​doi.​org/​10.​1523/​JNEUR​OSCI.​1443-​09.​2009 (2009).

### 26. Duncan, J., Burgess, P. & Emslie, H. Fluid intelligence after frontal lobe lesions. Neuropsychologia https://​doi.​org/​10.​1016/​0028-​

3932(94)​00124-8 (1995).

### 27. Roca, M. et al. Executive function and fluid intelligence after frontal lobe lesions. Brain https://​doi.​org/​10.​1093/​brain/​awp269

(2010).

### 28. Woolgar, A. et al. Fluid intelligence loss linked to restricted regions of damage within frontal and parietal cortex. Proc. Natl. Acad. Sci. USA. https://​doi.​org/​10.​1073/​pnas.​10079​28107 (2010).

### 29. Wen, T., Mitchell, D. J. & Duncan, J. Response of the multiple-demand network during simple stimulus discriminations. Neuroim-

age https://​doi.​org/​10.​1016/j.​neuro​image.​2018.​05.​019 (2018).

### 30. Assem, M., Glasser, M. F., Van Essen, D. C. & Duncan, J. A Domain-general cognitive core defined in multimodally parcellated

human cortex. Biorxiv https://​doi.​org/​10.​1101/​517599 (2019).

### 31. Langer, N. et al. Functional brain network efficiency predicts intelligence. Hum. Brain Mapp. https://​doi.​org/​10.​1002/​hbm.​21297

(2012).

### 32. Thatcher, R. W., Palmero-Soler, E., North, D. M. & Biver, C. J. Intelligence and EEG measures of information flow: Efficiency and

homeostatic neuroplasticity. Sci. Rep. https://​doi.​org/​10.​1038/​srep3​8890 (2016).

### 33. Von Stein, A. & Sarnthein, J. Different frequencies for different scales of cortical integration: From local gamma to long range

alpha/theta synchronization. Int. J. Psychophysiol. https://​doi.​org/​10.​1016/​S0167-​8760(00)​00172-0 (2000).

### 34. Donner, T. H. & Siegel, M. A framework for local cortical oscillation patterns. Trends Cogn. Sci. https://​doi.​org/​10.​1016/j.​tics.​2011.​

03.​007 (2011).

### 35. Mitra, A. et al. Human cortical-hippocampal dialogue in wake and slow-wave sleep. Proc. Natl. Acad. Sci. USA https://​doi.​org/​10.​

1073/​pnas.​16072​89113 (2016).

### 36. Groth-Marnat Publisher, G. & Wiley, J. Title: The Handbook of Psychological Assessment 4th edn. (Wliley, 2003).

### 37. Lezak, M. D., Howieson, D. B., Loring, D. W., Hannay, J. H. & Fischer, J. S. Neuropsychological Assessment (Oxford University Press,

2004).

### 38. Wechsler, D. Wechsler Memory Scale 3rd edn. (The Psychological Corporation, 1997).

### 39. Taylor, M. J. & Heaton, R. K. Sensitivity and specificity of WAIS-III/WMS-III domographically corrected factor scores in neu-

ropsychological assessment. J. Int. Neuropsychol. Soc. https://​doi.​org/​10.​1017/​s1355​61770​17771​07 (2001).

### 40. Hillebrand, A. & Barnes, G. R. Beamformer analysis of MEG data. Int. Rev. Neurobiol. https://​doi.​org/​10.​1016/​S0074-​7742(05)​

68006-3 (2005).

### 41. Newman, M. E. J. Modularity and community structure in networks. Proc. Natl. Acad. Sci. USA. https://​doi.​org/​10.​1073/​pnas.​

06016​02103 (2006).

### 42. Fernandes, H. M. et al. Disrupted brain structural connectivity in pediatric bipolar disorder with psychosis. Sci. Rep. https://​doi.​

org/​10.​1038/​s41598-​019-​50093-4 (2019).

### 43. Cabral, J. et al. Exploring mechanisms of spontaneous functional connectivity in MEG: How delayed network interactions lead to

structured amplitude envelopes of band-pass filtered oscillations. Neuroimage https://​doi.​org/​10.​1016/j.​neuro​image.​2013.​11.​047
(2014).

### 44. Hindriks, R. et al. Role of white-matter pathways in coordinating alpha oscillations in resting visual cortex. Neuroimage https://​

doi.​org/​10.​1016/j.​neuro​image.​2014.​10.​057 (2015).

### 45. Brookes, M. J. et al. A multi-layer network approach to MEG connectivity analysis. Neuroimage https://​doi.​org/​10.​1016/j.​neuro​

image.​2016.​02.​045 (2016).

### 46. Jespersen, K. V. et al. Reduced structural connectivity in insomnia disorder. J. Sleep Res. https://​doi.​org/​10.​1111/​jsr.​12901 (2020).

### 47. Tzourio-Mazoyer, N. et al. Automated anatomical labeling of activations in SPM using a macroscopic anatomical parcellation of

the MNI MRI single-subject brain. Neuroimage https://​doi.​org/​10.​1006/​nimg.​2001.​0978 (2002).

### 48. Wechsler, D. WAIS-III Administration and Scoring Manual (The Psychological Corporation, 1997).

### 49. Smith, S. M. et al. Advances in functional and structural MR image analysis and implementation as FSL. Neuroimage https://​doi.​

org/​10.​1016/j.​neuro​image.​2004.​07.​051 (2004). Vol.:(0123456789)
Scientific Reports | (2022) 12:4746 |
https://doi.org/10.1038/s41598-022-08521-5
www.nature.com/scientificreports/

### 50. Woolrich, M. W. et al. Bayesian analysis of neuroimaging data in FSL. Neuroimage https://​doi.​org/​10.​1016/j.​neuro​image.​2008.​10.​

055 (2009).

### 51. Behrens, T. E. J. et al. Characterization and propagation of uncertainty in diffusion-weighted MR imaging. Magn. Reson. Med.

https://​doi.​org/​10.​1002/​mrm.​10609 (2003).

### 52. Jbabdi, S., Sotiropoulos, S. N., Savio, A. M., Graña, M. & Behrens, T. E. J. Model-based analysis of multishell diffusion MR data

for tractography: How to get over fitting problems. Magn. Reson. Med. https://​doi.​org/​10.​1002/​mrm.​24204 (2012).

### 53. Taulu, S. & Simola, J. Spatiotemporal signal space separation method for rejecting nearby interference in MEG measurements. Phys. Med. Biol. https://​doi.​org/​10.​1088/​0031-​9155/​51/7/​008 (2006).

### 54. Penny, W., Friston, K., Ashburner, J., Kiebel, S. & Nichols, T. Statistical parametric mapping: The analysis of functional brain images. Stat. Paramet. Mapp. https://​doi.​org/​10.​1016/​B978-0-​12-​372560-​8.​X5000-1 (2007).

### 55. Oostenveld, R., Fries, P., Maris, E. & Schoffelen, J. M. FieldTrip: Open source software for advanced analysis of MEG, EEG, and

invasive electrophysiological data. Comput. Intell. Neurosci. https://​doi.​org/​10.​1155/​2011/​156869 (2011).

### 56. Mantini, D. et al. A signal-processing pipeline for magnetoencephalography resting-state networks. Brain Connect. https://​doi.​

org/​10.​1089/​brain.​2011.​0001 (2011).

### 57. Brookes, M. J. et al. Investigating the electrophysiological basis of resting state networks using magnetoencephalography. Proc. Natl. Acad. Sci. USA https://​doi.​org/​10.​1073/​pnas.​11126​85108 (2011).

### 58. Power, J. D., Schlaggar, B. L., Lessov-Schlaggar, C. N. & Petersen, S. E. Evidence for hubs in human functional brain networks. Neuron https://​doi.​org/​10.​1016/j.​neuron.​2013.​07.​035 (2013). Acknowledgements
We thank Giulia Donati, Riccardo Proietti, Giulio Carraturo, Mick Holt and Holger Friis for their assistance in
the neuroscientific experiment. We also thank the psychologist Tina Birgitte Wisbech Carstensen for her help
with the administration of psychological tests and questionnaires, and Francesco Carlomagno for his sugges-
tions regarding the topic covered in the study. The Center for Music in the Brain (MIB) is funded by the Danish
National Research Foundation (Project Number DNRF117). LB is supported by Carlsberg Foundation (Grant
CF20-0239), Center for Music in the Brain, Linacre College of the University of Oxford, and Society for Education
and Music Psychology (SEMPRE’s 50th Anniversary Awards Scheme). MLK is supported by Center for Music in
the Brain, and Centre for Eudaimonia and Human Flourishing funded by the Pettit and Carlsberg Foundations. Additionally, we thank the Italian section of Mensa: The International High IQ Society for the economic support
provided to Francesco Carlomagno and the University of Bologna for the economic support provided to Giulia
Donati, Riccardo Proietti, Giulio Carraturo. Author contributions
L. B., S. E. P. B., E. B., M. L. K. and P. V. conceived the hypotheses and designed the study. L. B. and S. E. P. B. performed
pre-processing and statistical analysis. E. B., M. L. K., M. L., L. B. and P. V. provided essential help to interpret and
frame the results within the neuroscientific literature. L. B. and S. E. P. B. wrote the first draft of the manuscript
and prepared the figures. L. B., S. E. P. B., E. B., M. L., M. L. K. and P. V. edited and reviewed the manuscript. All the
authors contributed to and approved the final version of the manuscript. Competing interests
The authors declare no competing interests. Additional information
Supplementary Information The online version contains supplementary material available at https://​doi.​org/​
10.​1038/​s41598-​022-​08521-5. Correspondence and requests for materials should be addressed to L. B. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Open Access  This article is licensed under a Creative Commons Attribution 4.0 International
License, which permits use, sharing, adaptation, distribution and reproduction in any medium or
format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the
Creative Commons licence, and indicate if changes were made. The images or other third party material in this
article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the
material. If material is not included in the article’s Creative Commons licence and your intended use is not
permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from
the copyright holder. To view a copy of this licence, visit http://​creat​iveco​mmons.​org/​licen​ses/​by/4.​0/.
© The Author(s) 2022
