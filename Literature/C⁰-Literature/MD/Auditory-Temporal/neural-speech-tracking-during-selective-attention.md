# neural-speech-tracking-during-selective-attention

Neural Speech Tracking during
Selective Attention: A Spatially
Realistic Audiovisual Study
Paz Har-shai Yahav, 1 Eshed Rabinovitch,1 Adi Korisky,1 Renana Vaknin Harel, 1
Martin Bliechner,2 and
 Elana Zion Golumbic 1
1The Gonda Center for Multidisciplinary Brain Research, Bar Ilan University, Ramat Gan,
5290002, Israel and 2Department of Psychology, Carl von Ossietzky Universität Oldenburg,
Germany
Abstract
Paying attention to a target talker in multitalker scenarios is associated with its more accurate neural
tracking relative to competing non-target speech. This “neural bias” to target speech has largely been
demonstrated in experimental setups where target and non-target speech are acoustically controlled
and interchangeable. However, in real-life situations this is rarely the case. For example, listeners often
look at the talker they are paying attention to while non-target speech is heard (but not seen) from
peripheral locations. To enhance the ecological-relevance of attention research, here we studied
whether neural bias toward target speech is observed in a spatially realistic audiovisual context and
how this is affected by switching the identity of the target talker. Group-level results show robust neural
bias toward target speech, an effect that persisted and generalized after switching the identity of the
target talker. In line with previous studies, this supports the utility of the speech-tracking approach for
studying speech processing and attention in spatially realistic settings. However, a more nuanced
picture emerges when inspecting data of individual participants. Although reliable neural speech
tracking could be established in most participants, this was not correlated with neural bias or with
behavioral performance, and >50% of participants showed similarly robust neural tracking of both
target and non-target speech. These results indicate that neural bias toward the target is not a
ubiquitous, or necessary, marker of selective attention (at least as measured from scalp-EEG), and
suggest that individuals diverge in their internal prioritization among concurrent speech, perhaps
reflecting different listening strategies or capabilities under realistic conditions.
Key words: EEG; selective attention; spatial; speech processing; TRF
Significance Statement
This work contributes to ongoing efforts to study the neural mechanisms involved in selective attention
to speech under ecologically relevant conditions, emulating the type of speech materials, multisensory
experience, and spatial realism of natural environments. Group-level results show that under these
more realistic conditions, the hallmark signature of selective attention —namely, the modulation of
sensory representation and its robustness to switches in target identity —is conserved, at least at
the group level. At the same time, results point to an underlying diversity among participants in
how that this modulation manifests, raising the possibility that differences in listening strategies,
motivation, or personal traits lead to differences in the way that individuals encode and process
competing stimuli, under ecological conditions.
Introduction
Effectively directing attention to a particular talker, and prioritizing its processing over
competing non-target speech, can be challenging. Selective attention to speech has
been associated at the neural level with enhanced neural tracking of target speech,
Received March 27, 2024; revised
March 13, 2025; accepted April 22,
2025.
The authors declare no competing
ﬁnancial interests.
Author contributions: P.H.-s.Y., A.K.,
M.B., and E.Z.G. designed research;
P.H.-s.Y. and R.V.H. performed
research; P.H.-s.Y., E.R., A.K., R.V.H.,
and E.Z.G. contributed unpublished
reagents/analytic tools; P.H.-s.Y., E.R.,
R.V.H., and E.Z.G. analyzed data;
P.H.-s.Y. and E.Z.G. wrote the paper.
This work was supported by Deutsche
Forschungsgemeinschaft (1591/2-1)
and Israel Ministry of Science
(3-16416).
Correspondence should be addressed
to Elana Zion Golumbic at elana.zion-
golumbic@biu.ac.il.
Copyright © 2025 Yahav et al.
This is an open-access article
distributed under the terms of the
Creative Commons Attribution 4.0
International license , which permits
unrestricted use, distribution and
reproduction in any medium provided
that the original work is properly
attributed.
Research Article: New Research
Cognition and Behavior
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 1 of 17
compared with non-target speech. This “neural bias ” for target speech has been demonstrated in numerous EEG and
MEG studies of selective attention to speech ( Kerlin et al., 2010 ; Ding et al., 2012 ; Zion Golumbic, et al., 2013b ;
O’Sullivan et al., 2015 ; Fiedler et al., 2019 ) and mirrors similar effects of selective attention in modulating sensory
responses to simpler stimuli ( Broadbent, 1958 ; Treisman, 1969 ; Hillyard et al., 1973 ; Näätänen et al., 1992 ). However,
to date, this effect has been mostly studied under conditions that do not fully capture the real-life challenge of attention
to speech. For example, the speech materials used in many studies are often comprised either of short, context-less utter-
ances (Brungart, 2001; Humes et al., 2017) or recordings of audiobooks that are highly edited and professionally rehearsed
and recorded (Fiedler et al., 2019; Fu et al., 2019), functioning more as “spoken texts” than as natural speech. In contrast,
natural speech is continuous, contextual, and produced on the ﬂy resulting in added disﬂuencies, pauses, and repetitions
(Agmon et al., 2023 ).
Another non-ecological aspect of many studies is that speech is presented only auditorily, often in a dichotic manner
where the audio from different talkers is presented to different ears ( Cherry, 1953 ; Bentin et al., 1995 ; Aydelott et al.,
2015; Brodbeck et al., 2020; Kaufman and Zion Golumbic, 2023; Makov et al., 2023). However, in many real-life situations,
listeners also look at the talker that they are paying attention to; hence, target speech is often audiovisual by nature and is
emitted from a central location relative to the listener. In contrast, other non-target talkers are —by default—heard but not
seen (unless listeners overtly move their head/eyes), and their audio emanates from peripheral spatial locations.
Accordingly, under spatially realistic audiovisual conditions, there are stark qualitative differences between the sensory
features of target and non-target speech, which likely assist listeners in focusing their attention appropriately ( Fleming
et al., 2021 ). Supporting this, it has been shown that having corresponding visual input of a talker facilitates speech pro-
cessing as well as selective attention ( Sumby and Pollack, 1954 ; Grant and Seitz, 2000 ; Schwartz et al., 2004 ; Ahmed et
al., 2023a,b; Haider et al., 2024; Karthik et al., 2024; Wikman et al., 2024) and also improves the precision of neural speech
tracking (Zion Golumbic et al., 2013a ; Crosse et al., 2015 ; Fu et al., 2019 ).
The current study is part of ongoing efforts to increase the ecological validity of selective attention research and to advance
our understanding of how the brain processes and prioritizes competing speech in the type of circumstances encountered in
real life (Freyman et al., 2001
; Ross et al., 2007; Tye-Mmurray et al., 2016; Shavit-Cohen and Zion Golumbic, 2019; Keidser et
al., 2020; Uhrig et al., 2022; Brown et al., 2023). We capitalize on the potential of the speech-tracking approach for gaining
insight into how the brain encodes and represents concurrent, continuous, and natural speech stimuli ( Ding et al., 2012 ;
Mesgarani and Chang, 2012; Zion Golumbic et al., 2013b ; Kaufman and Zion Golumbic, 2023 ). To our knowledge, only a
handful of previous studies have measured neural speech tracking in a spatially real audiovisual selective attention paradigm
(O’Sullivan et al., 2019; Wang et al., 2023). In one such study,O’Sullivan et al. (2019)found that it is possible to determine from
the neural signal whether a listener is paying attention to the talker they are looking at or if they are “eavesdropping” and
paying attention to a peripheral talker whom they cannot see. These results nicely demonstrate the dissimilarity of the neural
representation of audiovisual target speech and concurrent audio-only non-target speech. However, they leave open the
question of the degree to which the brain suppresses irrelevant speech and exhibits “neural bias” for preferential encoding
of target speech under spatially realistic audiovisual conditions.
There is a long-standing theoretical debate about how selective attention affects the neural representation of non-target
stimuli. One possibility is that non-target speech is attenuated at an early sensory level structuring ( Broadbent, 1958 ;
Treisman, 1960; Carlyon, 2004; Ding et al., 2018 ), and the degree to which non-target speech is represented/attenuated
is thought to re ﬂect the efﬁcacy of selective attention. Alternatively, target and non-target speech can be co-represented
at the sensory level, with selection occurring only at later stages (e.g., the level of linguistic/semantic processing; late-
selection; Deutsch and Deutsch, 1963; Murphy et al., 2013). As noted, numerous studies have demonstrated reliable “neu-
ral bias ” in the sensory representation of concurrent speech in dichotic listening paradigms, showing that the acoustic
envelope of target speech is tracked more precisely than non-target speech ( Kerlin et al., 2010 ; Zion Golumbic et al.,
2013b; O’Sullivan et al., 2015 ; Fuglsang et al., 2017 ; Fiedler et al., 2019 ; Har-Shai Yahav et al., 2024 ). However, although
this effect is robust when averaging across multiple participants, recently, Kaufman and Zion Golumbic (2023) showed
that this effect was driven by ∼30% of participants, whereas the majority of participants did not show reliable neural
bias but exhibited comparable neural representation for both target and non-target speech in bilateral auditory cortex.
This raised the possibility that suppression of non-target speech, at least at the sensory level, may not be a necessary
component of selective attention and that differences between individuals may re ﬂect different listening strategies or
capability for multiplexed listening. However, that study, like most previous work in the ﬁeld, used an auditory-only dicho-
tic listening design, which does not capture the spatial realism of real-life audiovisual contexts.
Here we sought to replicate and extend our previous work using a more ecologically valid spatially realistic audiovisual
design and to study the relative representation of target and non-target speech in the brain under these circumstances. We
simulated a common real-life situation in which individuals pay attention to a talker whom they can see (in this case, watch-
ing a video recording of a lecture) but also hear another talker off to the side, whom they cannot see and are asked to
ignore. We presented the audio of both target and non-target in a free- ﬁeld fashion, from their respective spatial locations,
rather than through earphones, to ensure realistic spatial propagation of the sound. Importantly, we used unedited record-
ings of actual lectures delivered by academics for the general public, to preserve the natural properties of the speech. In
addition, mid-way along the experiment we switched between the target and non-target talkers, to study how this affected
listeners and to test the generalizability of results across talkers and over time.
Research Article: New Research 2 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 2 of 17
We recorded participants neural activity using electroencephalography (EEG) and analyzed their neural tracking of tar-
get and non-target speech, focusing both on group averages, as is common in the ﬁeld, as well as on individual-level data
(Ding et al., 2012 ; Ding and Simon, 2012 ; Fuglsang et al., 2017 ; Rosenkranz et al., 2021 ; Kaufman and Zion Golumbic,
2023). We use data-driven statistics to determine the degree to which each talker is represented in the neural signal as
well as the “neural bias ” toward target speech. We also tested the reliability of results between the ﬁrst and second
half of the experiment, and tested if switching the identity of the target talker affected the pattern of neural tracking.
Materials and Methods
Participants
We collected data from 24 adult volunteers (16 female, 8 male), ranging in age between 19 and 34 ( M = 23.83,
SD = ±3.42). All participants were ﬂuent Hebrew speakers with self-reported normal hearing and no history of psychiatric
or neurological disorders. The study was approved by the IRB ethics board of Bar-Ilan University, and participants gave
their written informed consent prior to the experiment. Participants were either paid or received course credit for partic-
ipating in the experiment. Data from one participant was excluded from all analysis due to technical issues during EEG
recording, therefore all further analyses are reported for N = 23.
Speech stimuli
The stimuli consisted of two 20 min video recordings of a public lecture on popular science topics, one delivered by a
male talker and the other by a female talker. Each video recording included the lecturer as well as the slides accompanying
the talk. Both talkers gave their approval to use these materials for research purposes. Lecture videos were segmented
and edited using the software Filmora ( ﬁlmora.wondershare.net) and FFMPEG ( www.ffmpeg.org). Lectures were cut
into 63 segments ranging between 22 and 40 s each (lecture 1: M = 31.83, SD = ±4.2; lecture 2: M = 30.68, SD = 2.24).
The varied lengths were necessary to ensure that the segments did not cut off the lecture mid-sentence or mid-thought.
We equated the loudness of lecture segments using peak normalization, based on the average min and max dB across all
segments (separately for each talker). Then, to equate the perceived loudness of the two talkers (male and female), we
performed manual perceptual calibration, based on the feedback of ﬁve naive listeners. Loudness adjustment was per-
formed using the software FFMPEG and Audacity (version 3.2.1; www.audacityteam.org). Ultimately, the experiment
included 42 segments from the start and end of each lecture (21 each), and we discarded the content from the middle
of the lecture (see experimental procedure).
Experimental procedure
The experiment was programmed and presented to participants using the software OpenSesame ( Mathôt et al., 2012 ).
Participants were seated on a comfortable chair in a sound-attenuated booth and were instructed to keep as still as pos-
sible. Participants viewed a video lecture (target), presented segment-by-segment, on a computer monitor in front of them
with the lecture audio presented through a loudspeaker placed behind the monitor. They were instructed to pay attention
to the video and after every three segments, were asked three multiple-choice comprehension questions, regarding the
content of the recent segments (one question per segment, four possible answers). Participants received feedback
regarding the correctness of their responses and indicated via button press when they were ready to continue to the
next segment. In addition to the target lecture, audio from an additional non-target lecture was presented through a loud-
speaker placed on their left side ( Fig. 1A). Segments of non-target speech began 3 s after the onset of the target speech
and included a volume ramp-up of 2 s ( Fig. 1B). Both loudspeakers were placed at the same distance from participants ’
head (∼95 cm). We chose to present non-target speech only from the left side, rather than counterbalanced across both
sides, to ensure suf ﬁcient amount of data for TRF estimation, without doubling the experiment length.
In the middle of the experiment, the stimuli were switched: The lecture that had been the non-target became the target
lecture and was presented as a video in the second half, whereas the lecture that had been the target was presented as
audio-only from a loudspeaker on the left and was the non-target ( Fig. 1A). Importantly, different portions of each lecture
were presented in each half of the experiment. When a lecture was designated as the target, it started from the beginning
to ensure optimal comprehension and continued for 21 consecutive segments. When a lecture was designated as the
non-target (and presented only auditorily), the last 21 segments of the lecture were played, also in consecutive order.
In this way, segments from each lecture served both as target and non-target speech in different parts of the experiment
(thus sharing the talker-speciﬁc attributes and general topic), but none of the content was repeated. The order of the start-
ing lecture (male/female talker) was counterbalanced across participants, and participants were not informed in advance
about the switch. Audio from on-ear microphones and eye movements were also recorded during the experiment, but their
analysis is outside the scope of this study.
EEG data acquisition
EEG was recorded using a 64 Active Two system (BioSemi; sampling rate, 2,048 Hz) with Ag-AgCl electrodes, placed
according to the 10 –20 system. Two external electrodes were placed on the mastoids and served as reference channels.
Research Article: New Research 3 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 3 of 17
Electrooculographic (EOG) signals were simultaneously measured by four additional electrodes, located above and
beneath the right eye and on the external side of both eyes.
Behavioral data analysis
Behavioral data consisted of accuracy on the comprehension questions asked about each segment. These values were
averaged across trials, separately for each half of the experiment, and for each participant. We used a two-tailed paired t
test to evaluate whether accuracy rates differed signi ﬁcantly before and after the talker switch ( ﬁrst and second half).
EEG preprocessing and speech tracking
EEG preprocessing and analysis were performed using the Matlab-based FieldTrip toolbox ( Oostenveld et al., 2011), as
well as custom-written scripts. Raw data was ﬁrst rereferenced to the linked left and right mastoids and was bandpass
ﬁltered between 0.5 and 40 Hz (fourth-order zero-phase Butterworth ﬁlter). Data were then visually inspected and gross
artifacts (that were not eye movements) were removed. Independent component analysis (ICA) was performed to identify
and remove components associated with horizontal or vertical eye movements as well as heartbeats (identi ﬁed through
visual inspection). Any remaining noisy electrodes that exhibited either extreme high-frequency activity or low-frequency
drifts were replaced with the average of their neighbors using an interpolation procedure (ft_channelrepair function in the
FieldTrip toolbox). The clean data was then cut into trials, corresponding to portions of the experiment in which a
single segment of the lecture was presented. These were divided according to which half of the experiment they were
from—before and after switching the target talker ( ﬁrst and second half).
To estimate neural responses to the speech from the two simultaneous lectures, we performed speech-tracking anal-
ysis, using both an encoding and a decoding approach. We estimated multivariate linear Temporal Response Functions
Figure 1. Experimental setup. A, Two lectures were presented simultaneously, with one lecture (target talker) displayed on the screen and audio emitted
through the front loudspeaker. The other lecture (non-target talker) was played audio-only through the left loudspeaker. Participants were instru cted to
focus their attention on the lecture presented on the screen. Critically, in the middle of the experiment, the stimuli switched such that the lecture t hat
was played from the side and had been non-target in the ﬁrst half, was presented as a video in the second half, and became the target talker, whereas
the target talker from the ﬁrst half was presented in the second half from a loudspeaker on the side and became non-target. Participants answered com-
prehension questions regarding the target lecture after every three trials. B, Single trial illustration. Target speech began at trial onset, and non-target
speech began 3 s after onset and included a 2 s volume ramp-up.
Research Article: New Research 4 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 4 of 17
(TRFs) using the mTRF MATLAB toolbox ( Crosse et al., 2016 ), which constitutes a linear transfer function describing the
relationship between a particular feature of the stimuli (S) and the neural response (R) recorded when hearing it.
Here S was a matrix composed of the broadband envelopes of the two speech stimuli presented in each trial, and they
were treated as separate regressors in a single multivariate regression model. Envelopes were extracted using an equally
spaced ﬁlterbank between 100 and 10,000 Hz, with 20 frequency bands, based on Liberman ’s cochlear frequency map
(Liberman, 1982 ). The narrowband ﬁltered signals were summed across bands after taking the absolute value of the
Hilbert transform for each one, resulting in a broadband envelope signal. The R used here was the continuous cleaned
EEG data, bandpass ﬁltered again between 1 and 20 Hz (fourth-order zero-phase Butterworth ﬁlter), since the speech-
tracking response consists mostly of low-frequency modulations. S and R were aligned in time and downsampled to
100 Hz for computational ef ﬁciency. The ﬁve ﬁrst seconds of each trial were excluded from data analysis, due to the dif-
ferences in onset and ramp-up period ( Fig. 1B). In addition, the ﬁrst trial and the trial immediately after the talker switch
were omitted from data analysis, to avoid confounding effects associated with attentional ambiguity and adjustment to
the new target talker. This resulted in a total of 40 trials analyzed (20 per half), each ∼30 s long (see above).
Univariate and multivariate encoding and decoding models were optimized separately for each half of the experiment. In
the encoding approach, linear TRFs are estimated re ﬂecting the neural response at each electrode for each of the two
simultaneously presented stimuli, and the predictive power of the model reﬂects how it predicts the actual neural response
recorded. In the decoding approach, the neural data is used to reconstruct the envelope of each speech stimulus. TRF
predictive power values (encoding) and reconstruction accuracies (decoding) were assessed using a leave-one-out cross-
validation protocol. In each iteration, all trials except one were randomly selected to train the model (train set), which was
then used to predict either the neural response at each electrode (encoding) or the two speech envelopes (decoding) in the
left-out trial (test set). The predictive power of the encoding model is the Pearson ’s correlation (r value) between the actual
neural response in the left-out trial and the response predicted by the model. The decoding reconstruction accuracies is
calculated separately for the two speech stimuli presented in the left-out trial (target and non-target speech) and is the
Pearson’s correlation ( r value) between the reconstructed envelope of each and the actual envelope. The reported
TRFs, predictive power values, and reconstruction accuracies are the averages across all iterations.
Encoding TRFs were calculated over time lags ranging from −150 (pre-stimulus) to 450 ms, and the decoding analysis
used time lags of 0–400 ms, as is customary in similar analyses ( Crosse et al., 2016). To prevent overﬁtting of the model, a
ridge parameter was chosen as part of the cross-validation process (λ predictive power). This parameter signiﬁcantly inﬂu-
ences the shape and amplitude of the TRF and therefore, rather than choosing a different λ for each participant (which
would limit group-level analyses), a common λ value was selected for all participants, which yielded the highest average
predictive power, across all channels and participants (see also Har-shai Yahav et al., 2024; Kaufman and Zion Golumbic,
2023). For both the encoding and decoding models, this optimal value was λ = 1,000 a. Note that decoding results were
highly similar for λ’s that were optimized separately for each participant (data not shown).
EEG statistical analysis
Group-level statistics. The statistical signiﬁcance of the predictive power and reconstruction accuracy of the encoding
and decoding models were evaluated using permutation tests. For this, we repeated the encoding/decoding analysis pro-
cedure on shuf ﬂed S-R data where speech envelopes presented in one trial (S) were paired with the neural response
recorded in a different trial (mismatched R). This procedure was repeated 100 times, yielding a null distribution of predic-
tive power/reconstruction accuracy values that could be obtained by chance. The real data was then compared with this
null distribution and if it fell, within the top 5 percentile was considered statistically signi ﬁcant. To compare the speech-
tracking response across conditions, we conducted a 2 × 2 ANOVA a Bayesian factor analysis with repeated measures
to compare the predictive power and reconstruction accuracies obtained for target versus non-target speech, in each
half of the experiment (before vs after the target talker switch; JASP-Team, 2022; version 0.16.3; prior distribution param-
eters: Uniform Cauchy distribution with a scale parameter of r = 0.5, random effects r = 1, scale covariates r = 0.354).
To test the generalizability of the speech-tracking patterns between the two halves of the experiment, we also tested
how well decoders that were trained on data from one half of the experiment (either on target or non-target speech) could
be used to accurately predict the stimuli presented in the other half of the experiment based on the neural data.
Individual-level statistics. Statistical analysis of individual-level data focused only on reconstruction accuracies (decod-
ing approach), since this approach integrates responses across all electrodes, yielding a simpler metric for statistical anal-
ysis and avoiding multiple comparisons. We conducted a series of permutation tests to obtain data-driven statistics in
each individual participant, designed to address different questions, as illustrated in Figure 2.
First, we assessed whether the speech reconstruction accuracies obtained for both target and non-target speech were
signiﬁcantly better than those that could be obtained chance. To this end, we used S-R permutations, similar to those used
for group-level statistics, in which we shuf ﬂed the pairing between acoustic envelopes (S) and neural data responses (R;
Fig. 2A). Reconstruction values were assessed in 100 permutations of mismatched S-R combinations, yielding a null dis-
tribution from which we derived a personalized chance-level value for target and non-target speech, for each participant
(the top 5 percentile of the null distribution).
Research Article: New Research 5 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 5 of 17
Second, we assessed whether the difference in the reconstruction accuracy for the target and non-target talker could
reliably be attributed to their task relevance (referred to as the “Neural-Bias index ”). For this, we followed the procedure
introduced by Kaufman and Zion Golumbic (2023) to create an “attention-agnostic” null distribution of neural-bias indices
(Fig. 2B). Speciﬁcally, for each participant we created 100 permutations in which the two speech stimuli were randomly
relabeled so that the stimuli represented in each regressor was 50% target and 50% non-target. Multivariate decoders
were trained on this relabeled data and reconstruction accuracy values were estimated for each regressor, and difference
between them was used to create an attention-agnostic distribution of differences between reconstruction accuracies.
The real neural-bias index for each participant was normalized ( z-scored) relative to this null distribution, and participants
with a z-score >1.64 were considered as exhibiting a signi ﬁcance neural bias toward the target speech ( p < 0.05, one-
tailed). We chose this normalization continuous approach, rather than using a cutoff value, which allows us to present
the distribution of neural-bias values across participants. We note that the approach used here to assess differences in
speech tracking of target and non-target here differs from the auditory attention-decoding (AAD) approach used in similar
studies to identify which of two speech stimuli belongs to the target talker ( Mirkovic et al., 2015 ; O’Sullivan et al., 2015 ,
2019; Fuglsang et al., 2017 ; Teoh and Lalor, 2019 ). In those studies, a decoder trained only on target speech is used
to predict the envelope of non-target speech (and vice versa), which assesses the similarity/differences between the
decoders estimated for each stimulus. However, this approach is less appropriate in the current study, where we were
interested in assessing how accurately each speech stimulus is represented in the neural signal, even if the spatiotemporal
features of their decoders are different (see Extended Data Fig. 6-1 for a direct comparison of these approaches and dis-
cussion of their utility for different purposes).
The two analyses described above ( Fig. 2A,B) were performed using data from the entire experiment, as well as data
from each half of the experiment separately. We then performed a third permutation test to assess whether speech
Figure 2. Data-driven permutation tests for individual-level statistics. Three permutation tests were designed to assess statistical signi ﬁcance of different
results in individual participants. The black rectangles in all panels show the original data organization on the left and the relabeling for permutations test on
the right. A, S-R permutation test. In each permutation, the pairing between acoustic envelopes (S) and neural data responses (R) was shufﬂed across trials
such that speech envelopes presented in one trial (both target and non-target speech) were paired with the neural response (R) from in a different tria l. This
yields a null distribution of reconstruction accuracies that could be obtained by chance, to which the real data can be compared (right).
B, Attention-agnostic permutation test. In each permutation, the target and non-target speech stimuli were randomly relabeled to create attention-agnostic
regressors that contain 50% target speech and 50% non-target speech. The reconstruction accuracy for each regressor was estimated and the differenc e
between them is used to create a null distribution to which the neural-bias index can be compared (right). C, Order-agnostic permutation test. In each
permutation, trials were randomly relabeled and separated into two order-agnostic groups consisting of 50% trials from the ﬁrst half of the experiment
and 50% trials from the second half. The reconstruction accuracy for each group of trials was estimated, and the difference between them is used to create
a null distribution to which the real data from each half of the experiment can be compared (right).
Research Article: New Research 6 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 6 of 17
reconstruction accuracies and the Neural-Bias index differed signi ﬁcantly in the two halves of the experiment, i.e., before
versus after the talker switch. For this, we conducted an “order-agnostic” permutation test where trials were randomly
relabeled so that the data included in each regressor were 50% from the ﬁrst half of the experiment and 50% from the
second half ( Fig. 2 C). Multivariate decoders were trained on this relabeled data and reconstruction accuracy values
were estimated for each regressor, and this procedure was repeated 100 times, yielding a null distribution. A participant
was considered as showing a signiﬁcant difference in neural tracking of either the target or non-target talker, or different in
neural bias, if their real data fell in the top 5 percentile of the relevant null distribution.
Results
Behavioral data
Accuracy in answering comprehension questions about the content of the lecture was signi ﬁcantly above chance
(M = 0.845, SD = ±0.076; t(22) = 32.178, p <1 0−20). No signi ﬁcant differences in performance were observed between the
ﬁrst half (M = 0.846, SD = ±0.09) and second half (M = 0.856, SD = ±0.1) of the experiment (t(22) = −0.42, p = 0.68), as shown
in Figure 3.
Speech-tracking analysis
Group-level results
Figure 4 shows the results of the encoding approach. TRF models were estimated for target and non-target speech,
trained on data from the entire experiment and also separately on each half of the experiment (before and after talker
switch). As expected, the predictive power followed the common centro-frontal topography characteristic of auditory
responses in EEG ( Fig. 4 A) and was signi ﬁcant compared with a null distribution ( p < 0.01). The TRF for target speech
showed three prominent peaks —at 60, 110, and 170 ms —which is in line with previous studies and are thought to re ﬂect
a cascade of information ﬂow from the primary auditory cortex to associative and higher-order regions ( Brodbeck et al.,
2018b). The TRF for non-target speech was also robust but showed only a single positive peak, ∼70 ms, which likely
reﬂects its early sensory encoding, but not the two later peaks. Although the TRFs estimated for target and non-target
speech are not directly comparable (due to the many sensory differences between them, i.e., location, audiovisual vs audio
only), they did differ in the amount of variance they explained in the neural signal (predictive power of univariate models for
target vs non-target, averaged across all electrodes; F
(22) = 11.5, p = 0.003) and including both regressors in a multivariate
model explained signi ﬁcantly more of the variance in the neural signal than either univariate model alone ( t test between
average predictive power: multivariate vs target only: t = 2.97, p = 0.007; multivariate vs non-target only: t = 5.9, p <1 0−5;
Fig. 4B).
The TRFs estimated separately in the ﬁrst and second half of the experiment for target and non-target speech were
highly similar in their spatiotemporal properties, and no signi ﬁcant differences between them were found ( Fig. 4 C). An
ANOVA comparing the reconstruction accuracies for target versus non-target speech across both halves of the experi-
ment revealed a main effect of task relevance (target vs non-target: F
(1,22) = 28.3, p < 0.001) but no main effect of half
(F(1,22) = 0.12, p = 0.73) or interaction between the factors (half × talker: F(1,22) = 0.87, p = 0.87). These results were con-
ﬁrmed using a Bayesian ANOVA which indicated that the main effect of task relevance could be embraced with high con-
ﬁdence and explains most of the variance (BFinclusion = 317, p = 0.002) but there was no reliable difference between the two
halves or interaction (BF inclusion = 0.26 and BF inclusion = 0.27, respectively, both ps > 0.7).
Moreover, we found that decoders trained in one half of the experiment generalized well to the other half when tested on
stimuli that shared the same task relevance (role —target/non-target) but did not generalize well to stimuli that shared the
same talker identity but had different roles in the two halves of the experiment ( Fig. 5). Moreover, the modulation of recon-
struction accuracy by task relevance was preserved even in this cross-over analysis. This suggests that the decoders are
largely invariant to talker identity and primarily capture features related to the role of the talker in the given task and/or their
sensory properties (in this case, being presented audiovisually from a central location for the target speaker).
Figure 3. Behavioral results. Averaged accuracy rates across trials and participants, for multiple-choice comprehension questions, separately for the ﬁrst
(green) and second (yellow) half of the experiment. Error bars denote SEM across participants.
Research Article: New Research 7 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 7 of 17
Besides the speech-tracking analysis, we also conducted another group-level analysis of the data and inspected
whether the spectral makeup of the EEG signal, and particularly power in the alpha range (8 –12 Hz), differed between
the ﬁrst and second halves of the experiment. These results are shown in Extended Data Figure 4-1, as no signi ﬁcance
differences were found.
Individual-level results
Statistical analysis of speech tracking in individual participants was three tiered, assessing the signiﬁcance of: (1) recon-
struction accuracies for target and non-target speech, (2) the neural-bias index, and (3) differences between the two parts
of the experiment.
Figure 4. Neural bias: group-level results. A, TRF encoding models across all experimental trials, plotted from electrode “Fz,” separately for target and
non-target speech. Shaded highlights denote SEM across participants (top). Topographic distribution of the TRF main peaks, plotted separately for target
and non-target speech (bottom). B, Topographic distribution of predictive power values (Pearson’s r) of the encoding model, averaged across participants,
separately for multivariate (top) and univariate (bottom) analysis.C, TRF encoding models for the ﬁrst half (green) and second half (yellow) of the experiment,
plotted from electrode “Fz,” separately for target and non-target speech. Shaded highlights denote SEM across participants. D, Speech reconstruction
accuracies for the ﬁrst and second half of the experiment, for both target and non-target speech. Error bars denote SEM across participants. Extended
Data Figure 4-1 is supporting Figure 4.
Figure 5. Generalizability across talkers and time. Reconstruction accuracies for decoders trained on data from one half of the experiment (either on target
or non-target speech) and tested on data from the other half of the experiment, separately for same role decoders (e.g., train on target and test on targ et)
and for same talker identity decoders (e.g., train on male talker, test on male talker).
Research Article: New Research 8 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 8 of 17
Figure 6A (left panel) shows the reconstruction accuracies for target and non-target speech in individual participants,
relative to their personal chance-level value ( p = 0.05 cutoff, derived in a data-driven manner using S-R permutation).
All but one participant showed signi ﬁcant reconstruction accuracy of the target speech (22/23 participants —95%), and
most participants also showed higher than chance reconstruction for the non-target speech (18/23 participants —
78%). Moreover, reconstruction accuracies for target and non-target speech were positively correlated, across partici-
pants (Pearson’s r = 0.43, p = 0.038; Fig. 6A, right panel).
In Figure 6B, we compare the average reconstruction accuracy from each participant to their “Neural-Bias index,” which
reﬂects the difference in reconstruction accuracy for the target vs non-target speech (normalized relative“target-agnostic”
permutations of the data). When using a cutoff of z > 1.64 ( p < 0.05, one-tailed), only 10/23 participants (43%) showed a
signiﬁcant neural-bias index, and if we use a less conservative threshold of z >1 ( p < 0.15, one-tailed), this proportion
changes only slightly to 13/23 participants (56%). Interestingly, the reconstruction accuracies themselves and the neural-
bias index were not correlated with each other (Pearson ’s r = −0.017, p = 0.94), suggesting that these metrics are
independent.
We further tested whether performance on the behavioral tasks (answering comprehension questions) was correlated
with reconstruction accuracy of either speech stimuli or the neural-bias index; however, none of the brain –behavior cor-
relations were signi ﬁcance (target reconstruction accuracy vs behavior: r = 0.032, p = 0.88; non-target reconstruction
accuracy vs behavior: r = −0.088, p = 0.69; neural bias vs behavior: r = 0.14, p = 0.5; Fig. 6C).
Figures 7 and 8 depict the results of the same analyses shown in Figure 6 but conducted separately on data from each
half of the experiment. Here, speech reconstruction was signi ﬁcant in a fewer proportion of participants, with 17/23 (74%)
showing signiﬁcant reconstruction of target speech in both the ﬁrst and second half (although these were not necessarily
the same participants) and 10/23 (52%) or 12/23 (43%) participants showing signi ﬁcant reconstruction of non-target
speech in the ﬁrst and second half of the experiment, respectively ( Figs. 7 A, 8A). Reconstruction accuracy of target
and non-target speech were not signi ﬁcantly correlated in the ﬁrst half of the experiment (Pearson ’s r = 0.2, p = 0.33)
but were in the second half (Pearson ’s r = 0.4, p = 0.048).
Figure 6. Speech reconstruction and neural bias in individual participants—full experiment.A, Left, Bar graphs depicting reconstruction accuracy in individual
participants for target (black) and non-target (dark gray) speech. Horizontal light gray lines represent thep = 0.05 chance level, derived for each participant based
on data-driven S-R permutation. Asterisks indicate participants who also showed signi ﬁcant neural bias to target speech (see panel B). Right, Scatterplot
showing reconstruction accuracies for target and non-target speech across all participants. The red line represents the linear regressionﬁt between the two
variables, which was signi ﬁcant (Pearson’s r =0 . 4 3 ,p =0 . 0 3 8 ) .B, Scatterplot showing the average reconstruction accuracy and neural-bias index across
participants, which were not signi ﬁcantly correlated. Vertical dashed lines indicate the threshold for signi ﬁcant neural bias ( z = 1.64, one-tailed; p < 0.05).
C, Scatterplots showing the accuracy on behavioral task versus reconstruction accuracy of target speech (left), non-target speech (middle), and theneural-bias
index (right), across all participants. No signiﬁcant correlations were found. Extended DataFigure 6-1 is supporting Figure 6.
Research Article: New Research 9 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 9 of 17
When evaluating the neural-bias index of individual participants, we found that only 7/23 (30%) and 5/23 (21%) showed
signiﬁcantly better reconstruction accuracy for the target versus non-target speech ( z > 1.64, p < 0.05, one-tailed; ﬁrst and
second half, respectively). As observed for the full experiment, here too reconstruction accuracy was not correlated with
the neural-bias index in either half (ﬁrst half: r = −0.37, p = 0.08; second half: r = −0.026, p = 0.9; Figs. 7B, 8B), nor were any
brain–behavior correlations signiﬁcant (ﬁrst half: target reconstruction accuracy vs behavior: r = 0.095, p = 0.67; non-target
reconstruction accuracy vs behavior: r = 0.14, p = 0.54; neural bias vs behavior: r = −0.075, p = 0.73; Fig. 7C; second half:
target reconstruction accuracy vs behavior: r = 0.05, p = 0.83; non-target reconstruction accuracy vs behavior: r = −0.007,
p = 0.97; neural bias vs behavior: r = 0.1, p = 0.64; Fig. 8C).
Last, we compared the speech reconstruction accuracies and neural-bias indices obtained in each half of the experi-
ment but found that none of these measures were signi ﬁcantly correlated between the ﬁrst and second half of the exper-
iment (neural bias: Pearson ’s r = −0.005, p = 0.98, target speech: Pearson ’s r = 0.34, p = 0.11, non-target speech:
Pearson’s r = 0.17, p
= 0.44; Fig. 9 ). Only a handful of participants showed above-chance differences between the ﬁrst
and second half of the experiment in these metrics, relative to a distribution of order-agnostic permuted data ( Fig. 9 ,
red); however, these may represent false positives due to multiple comparisons.
Discussion
Here we studied the neural representation of target and non-target speech in a spatially realistic audiovisual setup, at
both the group-level and in individual participants. The group-level results are in line with results from previous two-talker
experiments that used less ecological paradigms (e.g., dichotic listening, scripted speech materials etc.), namely, that the
acoustic envelope of target speech is represented more robustly than that of non-target speech (Kerlin et al., 2010; Ding et
al., 2012; Mesgarani and Chang, 2012; Zion Golumbic et al., 2013b; O’Sullivan et al., 2015; Fuglsang et al., 2017; Brodbeck
et al., 2018b ; Fiedler et al., 2019 ; Niesen et al., 2019 ; Har-shai Yahav and Zion Golumbic, 2021 ; Kaufman and Zion
Golumbic, 2023 ; Straetmans et al., 2024 ). We also show that neural tracking is invariant to talker identity and does not
change signi ﬁcantly over the course of the experiment (in magnitude or spatiotemporal features of the decoder). This
Figure 7. Speech reconstruction and neural bias in individual participants—ﬁrst half of experiment. A, Left, Bar graphs depicting reconstruction accuracy in
individual participants for target (black) and non-target (dark gray) speech. Horizontal light gray lines represent the p = 0.05 chance level, derived for each
participant based on data-driven S-R permutation. Right, Scatterplot showing reconstruction accuracies for target and non-target speech across a ll par-
ticipants. B, Scatterplot showing the average reconstruction accuracy and neural-bias index across participants, which were not signi ﬁcantly correlated.
Vertical dashed lines indicate the threshold for signi ﬁcant neural bias ( z = 1.64, one-tailed; p < 0.05). C, Scatterplots showing the accuracy on behavioral
task versus reconstruction accuracy of target speech (left), non-target speech (middle), and the neural-bias index (right), across all participan ts. No sig-
niﬁcant correlations were found.
Research Article: New Research 10 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 10 of 17
supports the robustness of this measure for use in free-ﬁeld audiovisual contexts, laying the foundation to extend scientiﬁc
investigation of selective attention to more realistic environments ( Parsons, 2015; Risko et al., 2016 ; Brown et al., 2023 ;
Levy et al., 2024 ).
However, examination of individual-level results revealed that the neural bias observed at the group level is not seen
consistently in all, or even in most, listeners. Fewer than half of the participants showed signi ﬁcant neural bias for target
speech, whereas in most participants non-target speech could be reconstructed just as well as target speech from the
Figure 8. Speech reconstruction and neural bias in individual participants —second half of experiment. A, Left, Bar graphs depicting reconstruction accu-
racy in individual participants for target (black) and non-target (dark gray) speech. Horizontal light gray lines represent the p = 0.05 chance level, derived for
each participant based on data-driven S-R permutation. Right, Scatterplot showing reconstruction accuracies for target and non-target speech acr oss all
participants. The red line represents the linear regression ﬁt between the two variables, which was signi ﬁcant (Pearson’s r = 0.4, p = 0.048). B, Scatterplot
showing the average reconstruction accuracy and neural-bias index across participants, which were not signiﬁcantly correlated. Vertical dashed lines indi-
cate the threshold for signi ﬁcant neural bias (z = 1.64, one-tailed; p < 0.05). C, Scatterplots showing the accuracy on behavioral task versus reconstruction
accuracy of target speech (left), non-target speech (middle), and the neural-bias index (right), across all participants. No signiﬁcant correlations were found.
Figure 9. First versus second half of experiment. Scatterplots showing the neural-bias index (left), target speech (middle), and non-target speech recon-
struction accuracies (right) across all participants, in the ﬁrst versus second half of the experiment. No signi ﬁcant correlations were found for any of the
measures. Participants for whom signi ﬁcant difference were found between the two halves (based on an order-agnostic permutation test) are marked
in red.
Research Article: New Research 11 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 11 of 17
neural signal. Importantly, reconstruction accuracy and the neural-bias index were not correlated, indicating that variability
across participants cannot be trivially explained by poor speech tracking or low SNR. Moreover, neither the reconstruction
accuracy of target or non-target speech nor the neural-bias index were signiﬁcantly correlated with performance, suggest-
ing they carry limited behavioral consequences. These results are similar to those reported in a previous MEG study
(Kaufman and Zion Golumbic, 2023 ), which taken together lead us to suggest that although speech-tracking metrics
are useful for studying selective attention at the group level, they may fall short as “neural-markers of selective attention ”
at the individual level. Below we discuss the potential implications of these results for understanding the different strate-
gies listeners may employ to deal with concurrent speech in realistic multitalker contexts.
Group-level effects: highly robust and generalizable
The group-level TRFs, derived separately for target and non-target speech using an encoding approach, represent spa-
tiotemporal ﬁlters that capture the neural responses to each of the two concurrent talkers (Ding and Simon, 2012; Power et
al., 2012; Zion Golumbic et al., 2013b; Fuglsang et al., 2017; Fiedler et al., 2019; Kaufman and Zion Golumbic, 2023). They
share similar frontocentral topographical distribution, which is typical of auditory responses; however, they differ in their
time course. The TRF for target speech contains three prominent peaks —roughly at 60, 110, and 170 ms —which is in line
with previous studies and are thought to re ﬂect a cascade of information ﬂow from primary auditory cortex to associative
and higher-order regions ( Brodbeck et al., 2018b ; Chen et al., 2023 ). Conversely, the TRF for non-target speech showed
only a single positive peak, ∼70 ms, which likely reﬂects its early sensory encoding, but not the two later peaks. Past stud-
ies have reported mixed results regarding the temporal similarity of TRFs for target and non-target speech, some showing
similar time courses albeit with reduced amplitudes for non-target speech ( Kerlin et al., 2010 ; Ding et al., 2012 ; Zion
Golumbic et al., 2013b; O’Sullivan et al., 2015; Fiedler et al., 2019; Kaufman and Zion Golumbic, 2023) and others showing
that the later TRF peaks are not present for non-target speech ( Jaeger et al., 2020 ; Har-Shai Yahav et al., 2024 ). It is likely
that differences in spatiotemporal characteristics of TRFs for target and non-target speech are affected both by the spe-
ciﬁc perceptual attributes of the stimuli themselves (e.g., audiovisual vs audio presentation, their different spatial location
and consequent reverberation pattern) as well as by their task-related role (target vs non-target). In the spatially realistic
experimental design used here, these factors are inherently confounded, just as they are under real-life conditions in which
listeners look at the talker that they are trying to pay attention to. A previous study byO’sullivan et al. (2019) and reanalyzed
by Ahmed et al. (2023a) attempted to dissect the speci ﬁc contribution of selective attention versus audiovisual input by
including a condition in which participants watched video of a talker that they had to ignore and attended to a talker
who they could not see. However, it is not clear to what degree such a highly arti ﬁcial design (which is also extremely cog-
nitively demanding) is representative of the mechanisms that listeners use when processing speech under natural circum-
stances. Instead, here, rather than trying to assert whether the differences in TRF are due to “selective attention per se” or
to “perceptual differences,” we accept that in real life these often go together. We posit that as selective attention research
progresses to more ecologically valid contexts, these factors cannot (and perhaps need not!) be teased apart but rather
should be considered as making inherently joint contributions to behavior and neural responses. Arguably, in the aspira-
tion to empirically dissociate between “pure
” effects of perception and attention in ecological contexts may be inade-
quate, and we believe that one of the great challenges facing our ﬁeld today is to reconsider and rede ﬁne the
relationship between these constructs, if we strive to truly understand how the brain operates under real-life conditions
(Anderson, 2011; Risko et al., 2016 ; Schotter et al., 2025 ).
Regarding the comparison between theﬁrst and second half of the experiment, wefound similar TRFs and reconstruction
accuracies, both for target and for non-target speech. This indicates that listeners were highly effective at adapting their neural
encoding after the mid-way shift in the identity of the target talker and the topic of the lecture. It also demonstrates the robust-
ness of EEG-based speech-tracking measures and of the neural bias toward target speech when using roughly 10 min of data
(at least at the group level). When designi ng this study, we postulated that neural tracking and/or neural bias to the target
speech might be worse in the second half of the experiment, either due to fatigue ( Moore et al., 2017 ; Jaeger et al., 2020 )
or due to higher cognitive interference of the non-target talker who had previously been the target talker ( Johnsrude et al.,
2013; Har-Shai Yahav et al., 2024). The ﬁnding that here the switch did not carry a behavioral or neural processing cost is
testimony to the high adaptability andﬂexibility of the attentional system, which does not“get stuck” on processing previously
relevant features but updates its preferences according to changing task demands (Kiesel et al., 2010; Koch and Lawo, 2014;
Agmon et al., 2021; Kaufman and Zion Golumbic, 2023). This result is somewhat in contrast to some previousﬁndings show-
ing that speech processing was adversely affected by attention switching. For example, a recent study similar to ours (albeit
using auditory-only stimuli) found that a previously attended stream posed more of an interference to behavior task compared
with a consistently task-irrelevant stream (Orf et al., 2023). Other studies have also demonstrated reduced speech processing,
decreased intelligibility, and impaired recall of speciﬁc details, resulting from attention switching between talkers (Best et al.,
2008; Lin and Carlile, 2015; Getzmann et al., 2017; Teoh and Lalor, 2019; Uhrig et al., 2022). However, in those studies, the
switches occurred on a per-trial basis, which likely creates moreopportunities for confusion relative to the current study where
the target talker was switched only once. Admittedly, there is much yet to explore regarding attention switching between talk-
ers, particularly under ecological conditions where switches are contextual and ofteninitiated by the listener themselves. The
current ﬁndings contribute to these efforts by demonstrating that theneural representation of target and non-target speech is
invariant to talker identity and stabilizes nicely after a switch in a realistic audiovisual context.
Research Article: New Research 12 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 12 of 17
From group averages to individual-level responses
The vast majority of cognitive neuroscience research, and particularly when using EEG, relies on averaging results from
large samples of participants to obtain group-level results. This has traditionally been motivated by the noisy nature of
many EEG metrics, the variability across individuals, and the need to generalize results beyond a speci ﬁc sample ( Luck
et al., 2000 ; Makeig et al., 2004 ; Luck, 2014 ). However, increasingly, there is also a desire to derive reliable EEG-based
measures from the brains of individuals—to be used, for example, to explain variability in behavioral performance and cog-
nitive capabilities, as biomarkers for clinical symptoms, and to monitor the effectiveness of personalized interventions
(O’Sullivan et al., 2017 ; Bednar and Lalor, 2020 ; Hadley and Culling, 2022 ; Geirnaert et al., 2024 ). Deriving reliable
individual-level EEG-based metrics for speech processing and/or for attention has been particularly appealing, given their
potential utility for clinical, educational, and technological interventions. The development of speech-tracking methods
over the past decade has given hope that this metric will prove to be useful for individual-level assessments. Indeed, in
the domain of hearing and speech processing, several groups have demonstrated robust correlations between neural
speech-tracking metrics and speech intelligibility, for example, in children with dyslexia or in those with hearing impair-
ment (Keshavarzi et al., 2022; Xiu et al., 2022; Van Hirtum et al., 2023). In contexts that require selective attention to a target
talker, speech-tracking methods have also been successfully applied to distinguish between the neural representations of
target and non-target speech in individual participants and even on a per-trial basis (a classi ﬁcation-based approach that
can be effective, for example, for designing neuro-steering devices or hearing aids; Henshaw and Ferguson, 2013 ;
O’Sullivan et al., 2015; Kidd, 2017; Fallahnezhad et al., 2023; see Extended Data Fig. 6-1). However, to date fewer studies
have looked at the neural-bias index in individual participants, a metric that offers insights not only into the distinction
between target and non-target speech but into the modulation of their neural representations as a function of task rele-
vance, which is thought to be a signature of top-down selective attention ( Hillyard et al., 1973 ; Hansen and Hillyard,
1983; Woods et al., 1984 ; Bidet-Caulet et al., 2007 ; Manting et al., 2020 ).
The neural bias in reconstruction accuracies of target and non-target speech for individual participants is shown qual-
itatively in several previous papers, but statistical analyses focused mostly on the group level ( Ding et al., 2012 ; Ding and
Simon, 2012; Fuglsang et al., 2017 ; Rosenkranz et al., 2021 ). Kaufman and Zion Golumbic (2023) introduced the use of
attention-agnostic permutation tests to quantify and test the neural-bias index statistically in individual listeners.
Results from that MEG study are similar to those found here, whereby fewer than half of the participants ( ∼30% in that
study) exhibited signi ﬁcant modulation of speech tracking by selective attention, even when using a “permissive” statis-
tical threshold. The fact that group-level averages consistently show a robust difference between target and non-target
speech despite the underlying variability across participants is explained by the asymmetric distribution of the neural-bias
metric—since none of the participants show an “opposite” bias (i.e., more accurate reconstruction of non-target vs target
speech). This asymmetric distribution also lends further credibility to the neural-bias metric as reliably capturing the rel-
ative neural representation of the two speech stimuli.
How should we interpret the variability in neural bias across individuals? Here we ruled out several trivial explanations,
namely, that variability is due to poor EEG signal quality, poor speech-tracking abilities, or poor attention to the target —
since we show that the reconstruction accuracies for target and non-target speech are correlated with each other, but their
average is not correlated with the neural-bias index, nor is it correlated with accuracy in answering questions about the
content of target speech. Instead, we offer an alternative —admittedly speculative
—interpretation that emphasizes pos-
sible variability across individuals in their de facto allocation of processing resources among competing talkers. We know
from our subjective experience that paying attention solely to one target speech and shutting out other competing stimuli
can be extremely difﬁcult. There are numerous examples that both sensory and semantic properties of non-target speech
are encoded and processed, indicating that selective attention to one talker does not imply its exclusive representation
(Dupoux et al., 2003 ; Rivenez et al., 2006 ; Beaman et al., 2007 ; Parmentier et al., 2018 ; Vachon et al., 2019 ; Har-shai
Yahav and Zion Golumbic, 2021 ; Brown et al., 2023 ; Har-Shai Yahav et al., 2024 ). Moreover, the fact that individuals
can divide their attention reasonably well between two concurrent speech streams if asked to do so indicates that suf ﬁ-
cient perceptual cognitive resources may be available to listeners to apply a multiplexed listening strategy ( Vanthornhout
et al., 2019; Agmon et al., 2021; Kaufman and Zion Golumbic, 2023). Given that, it is reasonable to assume that even when
instructed to pay attention to only one talker, listeners may devote at least some resources to the competing non-target
talker as well—either voluntarily, as in divided attention, or involuntarily (Makov et al., 2023). This notion is in line with “load
theory of attention, ” which suggests that rather than attributing attentional selection of target stimuli/features to either
“early” or “late” stages of processing, attention should be viewed as the dynamic allocation of available cognitive
resources among competing stimuli. This allocation of resources among talkers re ﬂects their prioritization vis-à-vis their
relevance to the listener but can also vary as a function of perceptual load, task demands, and listener motivation/internal
state, which we propose may underlie some of the variability observed here between participants ( Lavie et al., 2004 ; Wild
et al., 2012 ; Gagné et al., 2017 ; Murphy et al., 2017 ; Peelle, 2018 ). Along these lines, the lack of a correlation between
neural bias and performance may suggest that the perceptual and cognitive demands of the current task, which emulates
those encountered in many real-life situations, left many listeners with suf ﬁcient available resources to corepresent both
talkers without behavioral costs. Clearly, this interpretation is speculative and the current data are insufﬁcient for testing its
plausibility; however, we offer it as a hypothesis for future studies aimed at better understanding individual differences in
prioritizing between target and non-target speech under realistic circumstances and whether this variability is explained by
Research Article: New Research 13 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 13 of 17
speciﬁc personal traits, by perceptual or cognitive load, or by other state-related factors (Beaman et al., 2007; Colﬂesh and
Conway, 2007; Forster and Lavie, 2008 ; Sörqvist and Rönnberg, 2014 ; Murphy et al., 2017 ; Lambez et al., 2020 ).
Another important point to note in this regard is that speech tracking, as quanti ﬁed here as the envelope-following
response measured using EEG, captures only a partial neural representation of the speech, primarily re ﬂecting encoding
of its acoustic properties in auditory (Ding et al., 2012; Mesgarani and Chang, 2012; Zion Golumbic et al., 2013b; Crosse et
al., 2016; Fiedler et al., 2019 ). Recent work that has attempted to separate between neural tracking of acoustic and lin-
guistic/semantic features of speech has suggested that selective attention primarily affects the latter ( Lachter et al.,
2004; Ding et al., 2018 ; Brodbeck et al., 2018a ), although this is not always the case ( Parmentier, 2008 ; Parmentier et
al., 2018 ; Vachon et al., 2019 ; Har-shai Yahav and Zion Golumbic, 2021 ). Moreover, studies that have looked at neural
speech tracking across different brain regions, using source-level MEG data or intracranial EEG (ECoG) recordings,
have shown a dissociation between the sensory cortical regions that corepresent concurrent speech versus higher-order
regions (e.g., anterior temporal cortex, as well as frontal and parietal regions) where attention selectivity was more prom-
inent (Zion Golumbic et al., 2013b ; Brodbeck et al., 2018a ,b; Har-shai Yahav and Zion Golumbic, 2021 ). Accordingly, it is
possible that if we were to use a more detailed characterization of the speech stimuli, had used a more complex non-linear
model, or had analyzed neural responses stemming from brain regions beyond auditory cortex, we might have found more
extensive evidence for neural bias in individual participants. While this is an important limitation to consider from a
basic-science perspective, the use of EEG in the current study and our focus on the acoustic envelope of speech have
critical applicational value. The motivation to derive personalized neural metrics of selective attention (as opposed to
group-based data) has a large practical component, such as providing tools for clinical/educational assessments and
interventions. As such, these would likely involve EEG recordings (which are substantially more accessible and affordable
than MEG) and—in the case of speech processing —would rely on analyzing speech features that are easy to derive (and
do not require a tedious annotation process; Agmon et al., 2023). In publishing this data set and emphasizing the variability
across individuals, we hope to provide a transparent account of the complexity of using EEG-based speech-tracking data,
as a “biomarker” of selective attention in individual listeners, and emphasize the need to systematically investigate the
factors underlying this variability (be them “cognitive” or “methodological” in nature).
Conclusion
In traditional cognitive neuroscience research, there is a desire to manipulate a speciﬁc construct (e.g., which stimulus is
the target) while controlling for all low-level sensory differences between stimuli. However, as we turn to studying neural
operations under increasingly ecological conditions, perfect control is less possible. In the case of selective attention, “tar-
getness” is often accompanied with speciﬁc sensory attributes, making targets inherently different than non-targets. Here
we studied one such case—where target speech is audiovisual and non-target speech is peripheral and auditory only. We
show that under these more realistic conditions, the hallmark signature of selective attention —
namely, the modulation of
sensory representation and its robustness to switches in target identity —is conserved, at least at the group level. At the
same time, our results also point to the underlying diversity among participants in how that this modulation manifests, to
the degree that in over half of the participants target and non-target speech were represented just as well (albeit in different
ways). These results emphasize that there is still much to explore regarding how the brain—or how different brains—treats
target and non-target speech when attempting to achieve selective attention. This work calls for more granular investiga-
tion of how factors such as task dif ﬁculty, perceptual load, listener motivation, and personal traits ultimately affect neural
encoding of competing stimuli, under ecological conditions.
References
Agmon G, Yahav PH-S, Ben-Shachar M, Zion Golumbic E (2021)
Attention to speech: mapping distributed and selective attention
systems. Cereb Cortex 32:3763 –3776.
Agmon G, Jaeger M, Tsarfaty R, Bleichner MG, Golumbic EZ (2023)
Um…,i t’s really difﬁcult to… um… speak ﬂuently”: neural tracking
of spontaneous speech. Neurobiol Lang 4:435 –454.
Ahmed F, Nidiffer AR, Lalor EC (2023a) The effect of gaze on EEG mea-
sures of multisensory integration in a cocktail party scenario. Front
Hum Neurosci 17:1283206.
Ahmed F, Nidiffer AR, O ’Sullivan AE, Zuk NJ, Lalor EC (2023b) The
integration of continuous audio and visual speech in a cocktail-
party environment depends on attention. Neuroimage 274:120143.
Anderson B (2011) There is no such thing as attention. Front Psychol
2:10181.
Aydelott J, Jamaluddin Z, Nixon Pearce S (2015) Semantic processing
of unattended speech in dichotic listening. J Acoust Soc Am
138:964–975.
Beaman CP, Bridges AM, Scott SK (2007) From dichotic listening to
the irrelevant sound effect: a behavioural and neuroimaging analy-
sis of the processing of unattended speech. Cortex 43:124 –134.
Bednar A, Lalor EC (2020) Where is the cocktail party? Decoding loca-
tions of attended and unattended moving sound sources using
EEG. Neuroimage 205:116283.
Bentin S, Kutas M, Hillyard SA (1995) Semantic processing and mem-
ory for attended and unattended words in dichotic listening: beha-
vioral and electrophysiological evidence. J Exp Psychol Hum
Percept Perform 21:54 –67.
Best V, Ozmeral EJ, Kopc ̌o N, Shinn-Cunningham BG (2008) Object
continuity enhances selective auditory attention. Proc Natl Acad
Sci U S A 105:13174 –13178.
Bidet-Caulet A, Fischer C, Besle J, Aguera PE, Giard MH, Bertrand O
(2007) Effects of selective attention on the electrophysiological
representation of concurrent sounds in the human auditory cortex.
J Neurosci 27:9252 –9261.
Research Article: New Research 14 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 14 of 17
Broadbent DE (1958) Perception and communication. London:
Pergamon Press.
Brodbeck C, Hong LE, Simon JZ (2018a) Rapid transformation from
auditory to linguistic representations of continuous speech. Curr
Biol 28:3976–3983.e5.
Brodbeck C, Presacco A, Simon JZ (2018b) Neural source dynamics of
brain responses to continuous stimuli: speech processing from
acoustics to comprehension. Neuroimage 172:162 –174.
Brodbeck C, Jiao A, Hong LE, Simon JZ (2020) Neural speech restora-
tion at the cocktail party: auditory cortex recovers masked speech
of both attended and ignored speakers (Malmierca MS, ed). PLoS
Biol 18:e3000883.
Brown A, Pinto D, Burgart K, Zvilichovsky Y, Zion-Golumbic E (2023)
Neurophysiological evidence for semantic processing of irrelevant
speech and own-name detection in a virtual café. J Neurosci
43:5045–5056.
Brungart DS (2001) Evaluation of speech intelligibility with the coordi-
nate response measure. J Acoust Soc Am 109:2276 –2279.
Carlyon RP (2004) How the brain separates sounds. Trends Cogn Sci
8:465–471.
Chen YP, Schmidt F, Keitel A, Rösch S, Hauswald A, Weisz N (2023)
Speech intelligibility changes the temporal evolution of neural
speech tracking. Neuroimage 268:119894.
Cherry EC (1953) Some experiments on the recognition of speech,
with one and with two ears. J Acoust Soc Am 25:975 –979.
Colﬂesh GJH, Conway ARA (2007) Individual differences in working
memory capacity and divided attention in dichotic listening.
Psychon Bull Rev 14:699 –703.
Crosse MJ, Butler JS, Lalor EC (2015) Congruent visual speech
enhances cortical entrainment to continuous auditory speech in
noise-free conditions. J Neurosci 35:14195 –14204.
Crosse MJ, Di Liberto GM, Bednar A, Lalor EC (2016) The multivariate
temporal response function (mTRF) toolbox: a MATLAB toolbox for
relating neural signals to continuous stimuli. Front Hum Neurosci
10:604.
Deutsch JA, Deutsch D (1963) Attention: some theoretical consider-
ations. Psychol Rev 70:80 –90.
Ding N, Simon JZ, Simon JZ (2012) Neural coding of continuous
speech in auditory cortex during monaural and dichotic listening.
J Neurophysiol 107:78 –89.
Ding N, Pan X, Luo C, Su N, Zhang W, Zhang J (2018) Attention is
required for knowledge-based sequential grouping: insights from
the integration of syllables into words. J Neurosci 38:1178 –1188.
Ding N, Simon JZ (2012) Emergence of neural encoding of auditory
objects while listening to competing speakers. Proc Natl Acad
Sci U S A 109:11854 –11859.
Dupoux E, Kouider S, Mehler J (2003) Lexical access without atten-
tion? Explorations using dichotic priming. J Exp Psychol Hum
Percept Perform 29:172 –184.
Fallahnezhad T, Pourbakht A, Toufan R (2023) The effect of computer-
based auditory training on speech-in-noise perception in adults: a
systematic review and meta-analysis. Indian J Otolaryngol Head
Neck Surg 75:4198 –4211.
Fiedler L, Wöstmann M, Herbst SK, Obleser J (2019) Late cortical
tracking of ignored speech facilitates neural selectivity in acousti-
cally challenging conditions. Neuroimage 186:33 –42.
Fleming JT, Maddox RK, Shinn-Cunningham BG (2021) Spatial align-
ment between faces and voices improves selective attention to
audio-visual speech. J Acoust Soc Am 150:3085 –3100.
Forster S, Lavie N (2008) Failures to ignore entirely irrelevant distrac-
tors: the role of load. J Exp Psychol Appl 14:73 –83.
Freyman RL, Balakrishnan U, Helfer KS (2001) Spatial release from
informational masking in speech recognition. J Acoust Soc Am
109:2112–2122.
Fu Z, Wu X, Chen J (2019) Congruent audiovisual speech enhances
auditory attention decoding with EEG. J Neural Eng 16:066033.
Fuglsang SA, Dau T, Hjortkjær J (2017) Noise-robust cortical tracking
of attended speech in real-world acoustic scenes. Neuroimage
156:435–444.
Gagné JP, Besser J, Lemke U (2017) Behavioral assessment of listen-
ing effort using a dual-task paradigm: a review. Trends Hear 21:1 –
25.
Geirnaert S, Zink R, Francart T, Bertrand A (2024) Fast, accurate, unsu-
pervised, and time-adaptive EEG-based auditory attention decod-
ing for neuro-steered hearing devices. In: Brain-computer interface
research (Guger C, Allison B, Rutkowski TM, Korostenskaja M,
eds), pp 29 –40. Cham: Springer.
Getzmann S, Jasny J, Falkenstein M (2017) Switching of auditory
attention in “cocktail-party” listening: ERP evidence of cueing
effects in younger and older adults. Brain Cogn 111:1 –12.
Grant KW, Seitz P-F (2000) The use of visible speech cues for improv-
ing auditory detection of spoken sentences. J Acoust Soc Am
108:1197–1208.
Hadley LV, Culling JF (2022) Timing of head turns to upcoming talkers
in triadic conversation: evidence for prediction of turn ends and
interruptions. Front Psychol 13:1061582.
Haider CL, Park H, Hauswald A, Weisz N (2024) Neural speech tracking
highlights the importance of visual speech in multi-speaker situa-
tions. J Cogn Neurosci 36:128 –142.
Hansen JC, Hillyard SA (1983) Selective attention to multidimensional
auditory stimuli. J Exp Psychol Hum Percept Perform 9:1 –19.
Har-Shai Yahav P, Sharaabi A, Zion Golumbic E (2024) The effect of
voice familiarity on attention to speech in a cocktail party scenario.
Cereb Cortex 34:bhad475.
Har-shai Yahav P, Zion Golumbic E (2021) Linguistic processing of
task-irrelevant speech at a cocktail party. Elife 10:e65096.
Henshaw H, Ferguson MA (2013) Ef ﬁcacy of individual computer-
based auditory training for people with hearing loss: a systematic
review of the evidence (Snyder J, ed). PLoS One 8:e62836.
Hillyard SA, Hink RF, Schwent VL, Picton TW (1973) Electrical signs of
selective attention in the human brain. Science 182:177 –180.
Humes LE, Kidd GR, Fogerty D (2017) Exploring use of the coordinate
response measure in a multitalker babble paradigm. J Speech
Lang Hear Res 60:741 –754.
Jaeger M, Mirkovic B, Bleichner MG, Debener S (2020) Decoding the
attended speaker from EEG using adaptive evaluation intervals
captures ﬂuctuations in attentional listening. Front Neurosci
14:510408.
JASP-Team (2022) JASP (version 0.16.3) [computer software].
Johnsrude IS, Mackey A, Hakyemez H, Alexander E, Trang HP,
Carlyon RP (2013) Swinging at a cocktail party: voice familiarity
aids speech perception in the presence of a competing voice.
Psychol Sci 24:1995 –2004.
Karthik G, Cao CZ, Demidenko MI, Jahn A, Stacey WC, Wasade VS,
Brang D (2024) Auditory cortex encodes lipreading information
through spatially distributed activity. Curr Biol 34:4021 –4032.e5.
Kaufman M, Zion Golumbic E (2023) Listening to two speakers: capac-
ity and tradeoffs in neural speech tracking during selective and dis-
tributed attention. Neuroimage 270:119984.
Keidser G, et al. (2020) The quest for ecological validity in hearing sci-
ence: what it is, why it matters, and how to advance it. Ear Hear
41:5S–19S.
Kerlin JR, Shahin AJ, Miller LM (2010) Attentional gain control of ongo-
ing cortical speech representations in a cocktail party. J Neurosci
30:620–628.
Keshavarzi M, Mandke K, Macfarlane A, Parvez L, Gabrielczyk F,
Wilson A, Flanagan S, Goswami U (2022) Decoding of speech
information using EEG in children with dyslexia: less accurate low-
frequency representations of speech, not “noisy” representations.
Brain Lang 235:105198.
Kidd G (2017) Enhancing auditory selective attention using a visually
guided hearing aid. J Speech Lang Hear Res 60:3027.
Kiesel A, Steinhauser M, Wendt M, Falkenstein M, Jost K, Philipp AM,
Koch I (2010) Control and interference in task switching –a review.
Psychol Bull 136:849 –874.
Koch I, Lawo V (2014) Exploring temporal dissipation of attention
settings in auditory task switching. Atten Percept Psychophys
76:73–80.
Research Article: New Research 15 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 15 of 17
Lachter J, Forster KI, Ruthruff E (2004) Forty-ﬁve years after broadbent
(1958): still no identi ﬁcation without attention. Psychol Rev
111:880–913.
Lambez B, Agmon G, Har-Shai Yahav P, Rassovsky Y, Zion Golumbic
E (2020) Paying attention to speech: the role of working memory
capacity and professional experience. Atten Percept Psychophys
82:3594–3605.
Lavie N, Hirst A, de Fockert JW, Viding E (2004) Load theory of selective
attention and cognitive control. J Exp Psychol Gen 133:339–354.
Levy O, Korisky A, Zvilichovsky Y, Golumbic EZ (2024) The neurophys-
iological costs of learning in a noisy classroom: an ecological vir-
tual reality study. J Cogn Neurosci 37:300 –316.
Liberman MC (1982) The cochlear frequency map for the cat: labeling
auditory-nerve ﬁbers of known characteristic frequency. J Acoust
Soc Am 72:1441 –1449.
Lin G, Carlile S (2015) Costs of switching auditory spatial attention in
following conversational turn-taking. Front Neurosci 9:136588.
Luck SJ, Woodman GF, Vogel EK (2000) Event-related potential stud-
ies of attention. Trends Cogn Sci 4:432 –440.
Luck SJ (2014) An introduction to the event-related potential tech-
nique, Ed 2. Cambridge: MIT press.
Makeig S, Debener S, Onton J, Delorme A (2004) Mining event-related
brain dynamics. Trends Cogn Sci 8:204 –210.
Makov S, Pinto D, Har-shai Yahav P, Miller LM, Zion Golumbic E (2023)
Unattended, distracting or irrelevant ”: theoretical implications of
terminological choices in auditory selective attention research.
Cognition 231:105313.
Manting CL, Andersen LM, Gulyas B, Ullén F, Lundqvist D (2020)
Attentional modulation of the auditory steady-state response
across the cortex. Neuroimage 217:116930.
Mathôt S, Schreij D, Theeuwes J (2012) OpenSesame: an open-
source, graphical experiment builder for the social sciences.
Behav Res Methods 44:314 –324.
Mesgarani N, Chang EF (2012) Selective cortical representation of
attended speaker in multi-talker speech perception. Nature
485:233–236.
Mirkovic B, Debener S, Jaeger M, De Vos M (2015) Decoding the
attended speech stream with multi-channel EEG: implications for
online, daily-life applications. J Neural Eng 12:046007.
Moore TM, Key AP, Thelen A, Hornsby BWY (2017) Neural mecha-
nisms of mental fatigue elicited by sustained auditory processing.
Neuropsychologia 106:371.
Murphy S, Fraenkel N, Dalton P (2013) Perceptual load does not mod-
ulate auditory distractor processing. Cognition 129:345 –355.
Murphy S, Spence C, Dalton P (2017) Auditory perceptual load: a
review. Hear Res 352:40 –48.
Näätänen R, Teder W, Alho K, Lavikainen J (1992) Auditory attention
and selective input modulation: a topographical ERP study.
Neuroreport 3:493–496.
Niesen M, Bourguignon M, Vander Ghinst M, Bertels J, Wens V,
Choufani G, Hassid S, Goldman S, De Tiège X (2019) Cortical pro-
cessing of hierarchical linguistic structures in adverse auditory sit-
uations. Front Neurosci 13.
Oostenveld R, Fries P, Maris E, Schoffelen J-M (2011) FieldTrip: open
source software for advanced analysis of MEG, EEG, and invasive
electrophysiological data. Comput Intell Neurosci 2011:1 –9.
Orf M, Wö M, Hannemann R, Obleser J (2023) Target enhancement but
not distractor suppression in auditory neural tracking during con-
tinuous speech. iScience 26:106849.
O’Sullivan AE, Lim CY, Lalor EC (2019) Look at me when I ’m talking to
you: selective attention at a multisensory cocktail party can be
decoded using stimulus reconstruction and alpha power modula-
tions. Eur J Neurosci 50:3282 –3295.
O
’Sullivan JA, Power AJ, Mesgarani N, Rajaram S, Foxe JJ,
Shinn-Cunningham BG, Slaney M, Shamma SA, Lalor EC (2015)
Attentional selection in a cocktail party environment can be
decoded from single-trial EEG. Cereb Cortex 25:1697 –1706.
O’Sullivan J, Chen Z, Herrero J, McKhann GM, Sheth SA, Mehta AD,
Mesgarani N (2017) Neural decoding of attentional selection in
multi-speaker environments without access to clean sources. J
Neural Eng 14:056001.
Parmentier FBR (2008) Towards a cognitive model of distraction by
auditory novelty: the role of involuntary attention capture and
semantic processing. Cognition 109:345 –362.
Parmentier FBR, Pacheco-Unguetti AP, Valero S (2018) Food words
distract the hungry: evidence of involuntary semantic processing
of task-irrelevant but biologically-relevant unexpected auditory
words. PLoS One 13:1 –17.
Parsons TD (2015) Virtual reality for enhanced ecological validity and
experimental control in the clinical, affective and social neurosci-
ences. Front Hum Neurosci 9:146520.
Peelle JE (2018) Listening effort: how the cognitive consequences of
acoustic challenge are re ﬂected in brain and behavior. Ear Hear
39:204–214.
Power AJ, Foxe JJ, Forde EJ, Reilly RB, Lalor EC (2012) At what time is
the cocktail party? A late locus of selective attention to natural
speech. Eur J Neurosci 35:1497 –1503.
Risko EF, Richardson DC, Kingstone A (2016) Breaking the fourth wall
of cognitive science. Curr Dir Psychol Sci 25:70 –74.
Rivenez M, Darwin CJ, Guillaume A (2006) Processing unattended
speech. J Acoust Soc Am 119:4027 –4040.
Rosenkranz M, Holtze B, Jaeger M, Debener S (2021) EEG-based
intersubject correlations re ﬂect selective attention in a competing
speaker scenario. Front Neurosci 15:685774.
Ross LA, Saint-Amour D, Leavitt VM, Molholm S, Javitt DC, Foxe JJ
(2007) Impaired multisensory processing in schizophrenia: de ﬁcits
in the visual enhancement of speech comprehension under noisy
environmental conditions. Schizophr Res 97:173 –183.
Schotter E, Payne B, Melcher D (2025) Characterizing the neural
underpinnings of attention in the real world via co-registration of
eye movements and EEG/MEG: an introduction to the special
issue. Atten Percept Psychophys 87:1 –4.
Schwartz JL, Berthommier F, Savariaux C (2004) Seeing to hear better:
evidence for early audio-visual interactions in speech identi ﬁca-
tion. Cognition 93:B69 –B78.
Shavit-Cohen K, Zion Golumbic E (2019) The dynamics of attention
shifts among concurrent speech in a naturalistic multi-speaker vir-
tual environment. Front Hum Neurosci 13:386.
Sörqvist P, Rönnberg J (2014) Individual differences in distractibility:
an update and a model. Psych J 3:42 –57.
Straetmans L, Adiloglu K, Debener S (2024) Neural speech tracking
and auditory attention decoding in everyday life. Front Hum
Neurosci 18:1483024.
Sumby WH, Pollack I (1954) Visual contribution to speech intelligibility
in noise. J Acoust Soc Am 26:212 –215.
Teoh ES, Lalor EC (2019) EEG decoding of the target speaker in a
cocktail party scenario: considerations regarding dynamic switch-
ing of talker location. J Neural Eng 16:036017.
Treisman AM (1960) Contextual cues in selective listening. Q J Exp
Psychol 12:242–248.
Treisman AM (1969) Strategies and models of selective attention.
Psychol Rev 76:282 –299.
Tye-Mmurray N, Spehar B, Myerson J, Hale S, Sommers M (2016)
Lipreading and audiovisual speech recognition across the adult
lifespan: implications for audiovisual integration. Psychol Aging
31:380–
389.
Uhrig S, Perkis A, Möller S, Svensson UP, Behne DM (2022) Effects of
spatial speech presentation on listener response strategy for
talker-identiﬁcation. Front Neurosci 15:730744.
Vachon F, Marsh JE, Labonté K (2019) The automaticity of semantic
processing revisited: auditory distraction by a categorical devia-
tion. J Exp Psychol Gen 149:1360 –1397.
Van Hirtum T, Somers B, Dieudonné B, Verschueren E, Wouters J,
Francart T (2023) Neural envelope tracking predicts speech intelli-
gibility and hearing aid bene ﬁt in children with hearing loss. Hear
Res 439:108893.
Vanthornhout J, Decruy L, Francart T (2019) Effect of task and atten-
tion on neural tracking of speech. Front Neurosci 13:977.
Research Article: New Research 16 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 16 of 17
Wang B, Xu X, Niu Y, Wu C, Wu X, Chen J (2023) EEG-based auditory
attention decoding with audiovisual speech for hearing-impaired
listeners. Cereb Cortex 33:10972 –10983.
Wikman P, Salmela V, Sjöblom E, Leminen M, Laine M, Alho K (2024)
Attention to audiovisual speech shapes neural processing through
feedback-feedforward loops between different nodes of the
speech network. PLoS Biol 22:e3002534.
Wild CJ, Yusuf A, Wilson DE, Peelle JE, Davis MH, Johnsrude IS (2012)
Effortful listening: the processing of degraded speech depends
critically on attention. J Neurosci 32:14010 –14021.
Woods DL, Hillyard SA, Hansen JC (1984) Event-related brain poten-
tials reveal similar attentional mechanisms during selective
listening and shadowing. J Exp Psychol Hum Percept Perform
10:761–777.
Xiu B, Paul BT, Chen JM, Le TN, Lin VY, Dimitrijevic A (2022)
Neural responses to naturalistic audiovisual speech are related to
listening demand in cochlear implant users. Front Hum Neurosci
16:1043499.
Zion Golumbic EM, Cogan GB, Schroeder CE, Poeppel D (2013a)
Visual input enhances selective speech envelope tracking in audi-
tory cortex at a “cocktail party”. J Neurosci 33:1417 –1426.
Zion Golumbic EM, et al. (2013b) Mechanisms underlying selective
neuronal tracking of attended speech at a “cocktail party ”.
Neuron 77:980–991.
Research Article: New Research 17 of 17
June 2025, 12(6). DOI: https://doi.org/10.1523/ENEURO.0132-24.2025. 17 of 17
