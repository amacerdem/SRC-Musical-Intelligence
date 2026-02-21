# behavior-relevant-periodized-neural-representation

Behavioral/Cognitive
Behavior-Relevant Periodized Neural Representation of
Acoustic But Not Tactile Rhythm in Humans
Cédric Lenoir,1
 Tomas Lenc,1,2 Rainer Polak,3,4 and
 Sylvie Nozaradan1,5,6
1Institute of Neuroscience (IONS), UCLouvain, Brussels 1200, Belgium, 2Basque Center on Cognition, Brain and Language (BCBL), Donostia-San
Sebastian 20009, Spain, 3RITMO Centre for Interdisciplinary Studies in Rhythm, Time and Motion, University of Oslo, Oslo 0318, Norway, 4Department
of Musicology, University of Oslo, Oslo 0318, Norway, 5MARCS Institute for Brain, Behaviour and Development, Western Sydney University, Sydney,
New South Wales 2751, Australia, and 6International Laboratory for Brain, Music and Sound Research (BRAMS), Montreal, Quebec H3C 3J7, Canada
Music makes people move. This human propensity to coordinate movement with musical rhythm requires multiscale temporal inte-
gration, allowing fast sensory events composing rhythmic input to be mapped onto slower, behavior-relevant, internal templates
such as periodic beats. Relatedly, beat perception has been shown to involve an enhanced representation of the beat periodicities
in neural activity. However, the extent to which this ability to move to the beat and the related “periodized” neural representation
are shared across the senses beyond audition remains unknown. Here, we addressed this question by recording separately the
electroencephalographic (EEG) responses and ﬁnger tapping to a rhythm conveyed either through acoustic or tactile inputs in
healthy volunteers of either sex. The EEG responses to the acoustic rhythm, spanning a low-frequency range (below 15 Hz), showed
enhanced representation of the perceived periodic beat, compatible with behavior. In contrast, the EEG responses to the tactile
rhythm, spanning a broader frequency range (up to 25 Hz), did not show signiﬁcant beat-related periodization and yielded less stable
tapping. Together, these ﬁndings suggest a preferential role of low-frequency neural activity in supporting neural representation of
the beat. Most importantly, we show that this neural representation, as well as the ability to move to the beat, is not systematically
shared across the senses. More generally, these results, highlighting multimodal differences in beat processing, reveal a process
of multiscale temporal integration that allows the auditory system to go beyond mere tracking of onset timing and to support
higher-level internal representation and motor entrainment to rhythm.
Key words: auditory; autocorrelation; beat; EEG; rhythm; tactile
Signiﬁcance Statement
Integrating fast sensory events composing music into slower temporal units is a cornerstone of beat perception. This study
shows that this ability relies critically on low-frequency brain activity, below the sensory event rate, in response to acoustic
rhythm. Conversely, brain responses elicited by the same tactile rhythm exhibit higher-frequency activity corresponding to
faithful tracking of the sensory event rate. Critically, the auditory-speci ﬁc slow ﬂuctuations feature an enhanced representa-
tion of the perceived periodic beat, compatible with behavior. This higher-level neural processing of rhythmic input could
thus re ﬂect internal representations of the beat that are not shared across senses, highlighting multimodal differences in
beat processing. These results pave the way to explore high-level multimodal perception and motor entrainment in humans.
Introduction
The propensity of humans to coordinate movement with musical
rhythm is attributed to a close coupling of the auditory and
motor systems ( Chen et al., 2008 ; Patel and Iversen, 2014 ;
Patel, 2024 ). This audiomotor coordination is thought to rely
on the auditory system ’s ability to integrate information at mul-
tiple timescales ( Teng et al., 2016 ). Such multiscale temporal
integration is arguably essential for human-speci ﬁc social inter-
actions such as music and dance ( Patel et al., 2005 ; Zatorre
et al., 2007 ) and speech ( Arnal et al., 2015b ; Norman-Haignere
Received April 2, 2025; revised July 22, 2025; accepted Sept. 9, 2025.
Author contributions: C.L. and S.N. designed research; C.L. performed research; C.L. and S.N. analyzed data;
C.L., T.L., R.P., and S.N. wrote the paper.
S.N. is supported by the ERC Starting Grant H2020 European Research Council, Grant/Award Number 801872.
The authors declare no competing ﬁnancial interests.
Correspondence should be addressed to Lenoir Cédric at cedric.lenoir@uclouvain.be.
https://doi.org/10.1523/JNEUROSCI.0664-25.2025
Copyright © 2025 Lenoir et al.
This is an open-access article distributed under the terms of theCreative Commons Attribution 4.0 International
license, which permits unrestricted use, distribution and reproduction in any medium provided that the original
work is properly attributed.
1–14  The Journal of Neuroscience, November 12, 2025  45(46):e0664252025
et al., 2022 ). Speci ﬁcally, this multiscale temporal sca ﬀolding is
crucial for organizing fast time intervals composing rhythmic
input into slower, behavior-relevant templates. Once mapped
onto the rhythmic input, these internal templates can be experi-
enced as periodic beats and can be used to guide motor coordi-
nation with others and the music ( Large and Snyder, 2009 ;
London, 2012; Bouwer and Honing, 2015 ).
Musical beat usually refers to an internal representation con-
sisting of recurring periods, or periodic pulses, mapped onto the
rhythmic input ( Bouwer and Honing, 2015 ; London et al., 2017 ;
Lenc et al., 2021). How this internal periodic template is mapped
onto complex sensory inputs such as music is far from trivial.
Indeed, the beat periodicities are often not prominent in the
physical structure of the input ( London, 2012 ; London et al.,
2017; Bouwer et al., 2018 ), thus pointing toward higher-level
neural processes underlying beat perception ( Nozaradan et al.,
2017a; Lenc et al., 2021 , 2025). Therefore, uncovering these pro-
cesses promises key insight into high-level perception and motor
entrainment in humans.
Recent studies captured human brain activity using electroen-
cephalography (EEG) in response to rhythmic inputs known to
yield the perception of a periodic beat. These studies revealed
that the neural representation of rhythmic inputs exhibit selec-
tively emphasized beat periodicities, regardless of their promi-
nence in the input ( Nozaradan et al., 2017a ; Lenc et al., 2020 ,
2023). Importantly, such “periodized” neural representation
seems functionally relevant, as the enhanced beat-related period-
icities in neural activity correspond to those preferentially
expressed through body movements ( Nozaradan et al., 2012 ,
2018; Lenc et al., 2018 ).
However, whether this neural representation of beat and the
ability to move to it are auditory-speci ﬁc or generalize beyond
audition remains unclear. Synchronization to rhythm is generally
recognized to be facilitated with audition, as compared with
vision or touch ( Repp and Penel, 2004 ; Hove et al., 2013 ;
Gilmore and Russo, 2021 ). Yet, recent studies have challenged
this view by showing synchronization performance close
to that typically found with audition when the rhythmic
input was tuned to match the sensitivity of the sensory modality
being compared with audition (e.g., with visual rhythms
conveyed through moving rather than static stimuli; Hove
et al., 2010 ).
Here, we addressed the question of cross-sensory commonal-
ities and speci ﬁcities in beat processing by separately recording
behavioral and EEG responses to an acoustic and tactile version
of the same rhythm. Since sounds and vibrations share similar
physical attributes (i.e., time –amplitude varying signals charac-
terized by their magnitude, frequency, period, and wavelength;
Dobie and Van Hemel, 2005 ) and often concomitantly occur in
musical contexts ( Merchel and Altinsoy, 2018 ; Reybrouck
et al., 2019 ), it could be hypothesized to ﬁnd enhanced neural
representation of the beat in response to both types of sensory
input (Schurmann et al., 2006 ; Rahman et al., 2020 ). Yet, recent
studies on sensorimotor synchronization with tactile versus
acoustic rhythms and corresponding EEG activity ( Brochard
et al., 2008 ; Tranchant et al., 2017 ;
Gilmore and Russo, 2021 )
showed di ﬀerences between these modalities. These di ﬀerences
could have been driven by the use of stimuli not speci ﬁcally
adjusted for the somatosensory system (e.g., body part and car-
rier frequency used for stimulation suboptimal to the mechano-
receptors’ sensitivity). Therefore, the current study aimed to
move a critical step forward by investigating beat processing
using stimuli ﬁne-tuned to match the sensitivity of each sense
while controlling for lower-level confounds using rhythms whose
physical structure does not feature prominent beat periodicities.
Materials and Methods
Participants
Forty-ﬁve healthy volunteers (32 women; mean age, 23.5 years; SD, 3.4)
took part in the study. All participants reported normal hearing, no alter-
ation of cutaneous sensitivity at the level of the ﬁngers, and no history or
presence of neurological or psychiatric disorders. Most of the partici-
pants reported having grown up in countries from a Western culture
(42 out of 45). They reported a range of musical training (mean, 1.6 years
of formal music training, e.g., music lessons; SD, 3.0; range, 0 –14 years),
with 8 of them self-identifying as “amateur musicians” while the other 37
participants deﬁned themselves as “nonmusicians.”
Participants were randomly assigned to one of the three groups cor-
responding to three di ﬀerent block orders, i.e., Group 1, ﬁrst tactile–sec-
ond acoustic –third tactile ( n = 15; mean age, 25.9 years; SD, 4.3; 12
women); Group 2, ﬁrst tactile –second tactile –third acoustic ( n = 15;
mean age, 25.4 years; SD, 2.3; 12 women); and Group 3, ﬁrst acoustic –
second tactile –third tactile ( n = 15; mean age, 24.7 years; SD, 3.4; 8
women). Participants provided written consent after being informed
about the experimental procedures. All procedures were approved by
the local ethical committee “Comité Hospitalo-facultaire de
l’UCLouvain” (protocol number B403201938913).
Rhythmic sequences
Participants were presented with 60 s rhythmic sequences in both sen-
sory modalities. The sequences were created in MATLAB 2020b
(MathWorks) by seamlessly looping 25 times a speci ﬁc 2.4 s rhythmic
pattern. The pattern was built by dividing 2.4 s into 12 equal intervals
of 200 ms, with 8 of these intervals being allocated a sensory event
kept identical across the eight occurrences. The location of these sensory
events on this regular interval grid yielded a speci ﬁc rhythmic pattern
corresponding to [xxxx.xxx..x.] (where “x” is a sensory event and dot rep-
resents an empty grid interval, each spanning 200 ms). The sensory
events corresponded to 150-ms-long sounds or vibrations (10 ms linear
ramp-up, 90 ms plateau, and 50 ms linear ramp-down), followed by a
50 ms gap (see Fig. 1A for a visualization of the sequential arrangement
of sensory events composing this speci ﬁc pattern).
This rhythmic pattern, used in a number of previous studies
(Nozaradan et al., 2016b , 2017a,b; Lenc et al., 2018 ;
Sauvé et al., 2022 ;
Sifuentes-Ortega et al., 2022 ), has been repeatedly shown to induce per-
ception of a periodic pulse (beat) at a rate generally converging across
Western participants toward a grouping of four underlying grid intervals
(4 × 200 ms). Moreover, signiﬁcant relative enhancement of neural activ-
ity at frequencies corresponding to the rate of this beat periodicity and
harmonics has been observed in the EEG in responses to this repeated
pattern ( Nozaradan et al., 2012 , 2018; Lenc et al., 2023 ). Importantly,
this speci ﬁc pattern can be considered weakly periodic at the rate of
this beat, since the groups of sensory events making up the rhythm are
arranged in a way that does not prominently cue the beat periodicity
(Povel and Essens, 1985 ; Patel et al., 2005 ; Grahn and Brett, 2007 ).
Using a weakly periodic rhythm is critical here, as it allows to control
for low-level sensory confounds, whereby the observed neural emphasis
on the beat periodicity could otherwise be trivially explained by neural
responses elicited by prominent physical features of the stimulus (see
below and Fig. 1B, for a quantiﬁcation of the prominence of the beat peri-
odicity in the stimulus modulation signal).
Acoustic inputs. Sound events consisted of pure sine waves at a fre-
quency of 300 Hz. This carrier frequency was used here based on previ-
ous work having shown that stimuli within this frequency range elicit
robust EEG responses ( Wunderlich and Cone-Wesson, 2001 ; Ross
et al., 2003 ; Nozaradan et al., 2015 , 2018; Lenc et al., 2018 ; Rahman
et al., 2020 ). Acoustic sequences were delivered binaurally, to ensure
comparability with e ﬀects obtained in previous studies investigating
beat processing using similar acoustic rhythm ( Nozaradan et al.,
2016b, 2017a,b; Lenc et al., 2018 ; Sauvé et al., 2022 ; Sifuentes-Ortega et
2  J. Neurosci., November 12, 2025  45(46):e0664252025 Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm
al., 2022). Sounds were presented at an intensity of 70 dB SPL using ﬂat
frequency response insert earphones (ER-2, Etymotic Research).
Tactile inputs. Vibration events consisted of 86 Hz sine waves at an
intensity corresponding to a peak-to-peak displacement magnitude of
230 µm. Previous works have shown that such tactile stimuli e ﬀectively
recruit the diﬀerent types of mechanosensitive receptors and elicit robust
EEG responses ( Muniak et al., 2007 ; Bensmaia, 2008 ; Rahman et al.,
2020). Tactile sequences were generated by an electromagnetically shielded
piezo-electric vibrotactile stimulator (VTS, Arsalis, UCLouvain) connected
to a 20-mm-diameter round–tipped probe. Tactile sequences were deliv-
ered unilaterally to all ﬁngertips in contact with the probe, which allowed
participants to perform the tapping task with the other hand similarly to
the acoustic condition while keeping tactile stimulus presentation identical
across EEG and tapping sessions. The speci ﬁc cutaneous region of the
ﬁngertips was chosen given its highest density of mechanoreceptors
(Johansson and Vallbo, 1979; Vallbo and Johansson, 1984; Corniani and
Saal, 2020) and for its distance to the ear canal which prevented any audi-
tory response through bone or soft tissue conduction ( Geal-Dor and
Sohmer, 2021). Moreover, during tactile stimulation, the likelihood of elic-
iting auditory response to sounds produced by the piezo-electric stimulator
was reduced by playing a uniformly distributed white noise through insert
earphones at individually adjusted maximal tolerable intensity (up to 80 dB
SPL). The masking white noise started 2 s before the onset of each tactile
trial and ended 0.5 s after its end.
Experimental design
The main experiment consisted of three blocks, one acoustic and two tac-
tile. The tactile condition was repeated because perceiving the beat in this
setting is unusual for normal-hearing individuals who are mostly
exposed to and rely on auditory input in rhythmic musical contexts in
everyday life. To mitigate the novelty of the situation and allow partici-
pants to familiarize themselves with the tactile condition, we repeated the
tactile block and counterbalanced the order of the blocks across partici-
pants. Each block was composed of an EEG session (12 trials), followed
by a tapping session (5 trials). A short break of a few seconds was
included between each trial and block to prevent sensory habituation
and fatigue.
During the EEG session, participants were asked to focus their atten-
tion on the tactile or acoustic rhythmic sequences and refrain from any
movement. During tactile stimulation of the ﬁngertips, the position of
the forearm and wrist was comfortably stabilized by means of a cushion.
To further encourage participants to focus on the temporal properties of
the stimuli, participants were also asked to detect transient changes of the
tempo that could possibly occur in the stimulus sequence and to report
the presence and number of such changes at the end of each sequence.
Tempo changes occurred in two nonconsecutive trials pseudorandomly
placed within the 12 EEG trials composing each block (with the exclusion
of the ﬁrst trial, which never contained a tempo change). Tempo changes
consisted of one pattern in which the underlying grid intervals were pro-
gressively lengthened (from 200 to 230 ms for the acoustic sequences and
from 200 to 250 ms for the tactile sequences) and then shortened back to
the initial 200 ms grid intervals following a cosine function across the 12
grid intervals spanning one repetition of the pattern. Within the 60 s
sequences containing the tempo change, up to three nonconsecutive
altered patterns were pseudorandomly positioned among the 25 repeti-
tions of the pattern, excluding the ﬁrst repetition. The altered EEG trials
were removed from further analyses.
During the tapping session, participants were asked to tap the perceived
beat along with the rhythmic sequences overﬁve successive trials, using the
index ﬁnger of their preferred hand. Finger tapping was recorded using a
custom-build response box (hereafter “tapping box ”; Institute of
Neurosciences, UCLouvain) containing a high-resistance switch able to
generate a trigger signal every time the ﬁngertip contacts the response
box and a force sensor continuously monitoring the normal force applied
to the box (with a constant response delay of 62.5 ms). The surface of the
tapping box contacted by the ﬁnger was rigid, providing somatosensory
and possibly auditory feedback. This feedback was reduced by using insert
earphones, which partially blocked the sound of each tap during the pre-
sentation of the acoustic stimulus and completely masked it with white
noise during tactile stimulation. Participants were asked to start tapping
as soon as possible after the rhythmic sequence started and continuously
tap the perceived beat along with the entire sequence as regularly as possi-
ble and as synchronized as possible with the sequence. Participants were
advised not to restrict spontaneous movements of other body parts if doing
so would help them perform the tapping task.
Familiarization phase
The main experiment was preceded by a familiarization phase in which
the participants were briefed on the concept of (1) beat, required for the
tapping task, and (2) tempo change, required for the detection task dur-
ing the EEG recording sessions.
During the ﬁrst part of the familiarization task, participants were
asked to press the space bar of a keyboard with the index ﬁnger of their
choice while listening successively to three tracks of electronic music in
which the beat was acoustically either very explicit or more ambiguous.
The instruction was to tap continuously along the track and as regularly
as possible in synchrony with the beat they perceived, as they would do if
Figure 1. Stimuli consist of a repeated rhythmic pattern where the beat periodicity is not prominent. A, Time domain representation of the stimuli (full signal in gray, sound envelope in
black). The 2.4 s rhythmic pattern was looped 25 times, yielding 60 s sequences for both sensory modalities (carrier frequency of 300 Hz and 86 Hz for aco ustic and tactile sequences, respec-
tively). B, Magnitude spectrum of stimulus envelope. Frequencies of interest were de ﬁned among the frequency of pattern repetition (1/2.4 s = 0.417 Hz) and harmonics. Harmonic frequencies
corresponding to the most consistently tapped periods were de ﬁned as beat-related frequencies in red (4 × 200 ms = 800 ms, i.e., 1.25 Hz and harmonics) and the remaining frequencies as
beat-unrelated frequencies in blue. Note that beat-related frequencies (de ﬁned as the most consistently tapped period of 800 ms, i.e., 1.25 Hz and harmonics) were overall of lower magnitude
than beat-unrelated frequencies in this rhythm.
Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm J. Neurosci., November 12, 2025  45(46):e0664252025  3
they were nodding the head or stepping along with the music tracks. A
plausible beat was indicated at the start of each music track by overlaid
periodic hand-claps sounds that gradually faded out as the track pro-
gressed. Participants were asked to initially synchronize their taps to
the clap sounds and keep tapping despite the cue was fading out (i.e.,
in a synchronization –continuation mode). Then, participants were pre-
sented with rhythmic sequences whose stimulus parameters were all
identical to those used during the main experiment, except for the
speciﬁc sequential arrangement of sensory events forming the repeated
rhythmic pattern. Namely, we used a weakly periodic rhythmic pattern
diﬀerent from the one used in the main experiment, corresponding
here to [xxx.xx..x.x.] (where x is a sensory event and dot an empty grid
interval). These either acoustic or tactile 60 s familiarization-speci ﬁc
rhythmic sequences were presented, while participants were encouraged
to tap along with the perceived beat as regularly as possible on the tap-
ping box, following the exact same instructions as in the main experi-
ment. Tactile sequences were delivered to the hand contralateral to the
hand chosen by the participant to perform the tapping task.
Participants were explicitly asked to relax and keep their ﬁngers still
on the stimulator while the sequences were played.
In the second part of the familiarization phase, participants were accus-
tomed with the detection of tempo changes as occurring in a few trials of
each block in the main experiment. To this aim, participants were asked
to detect tempo changes pseudorandomly inserted in the familiarization-
speciﬁc rhythmic sequences in the same fashion as in the main experiment.
EEG recording and processing
The EEG was recorded using 64 sintered Ag –AgCl electrodes placed on
the scalp according to the international 10/20 system (ActiveTwo,
Biosemi). Two additional electrodes were placed on the left and right
mastoids. The signal was referenced to the CMS (common mode sense)
electrode and digitized at a 1024 Hz sampling rate (with default
hardware low-pass ﬁltering at one- ﬁfth of the sampling rate). Electrode
oﬀsets were kept below 50 mV for all leads. The continuous EEG record-
ings were processed o ﬄ ine with Letswave6 ( https:/ /www.letswave.org/)
and custom scripts in MATLAB 2020b (MathWorks). The continuous
EEG signal was ﬁltered using a 0.1 Hz Butterworth zero-phase high –
pass ﬁlter (second order) to remove irrelevant slow ﬂuctuations and
then segmented into 60 s epochs relative to trial onset, thus encompass-
ing the total duration of stimulation in each trial. Channels containing
artifacts exceeding ± 200 mV or excessive noise were linearly interpo-
lated using the three closest channels (a maximum of three channels
were interpolated per participant in <7% of the total sample). After
rereferencing to the common average, artifacts due to eyeblinks, eye
movements, muscular activity, or heartbeat were removed using inde-
pendent component analysis (FastICA algorithm; Hyvarinen and Oja,
2000). A maximum of three independent components were removed
by participant. EEG responses recorded during acoustic stimulation
were analyzed at a frontocentral pool of electrodes (F1, FC1, C1, F2,
FC2, C2, Fz, FCz, Cz) rereferenced to the averaged mastoids which is a
standard reference to estimate cortical auditory responses ( Skoe and
Kraus, 2010; Nozaradan et al., 2016a , 2018; Mahajan et al., 2017 ). EEG
trials recorded during tactile stimuli were analyzed on a sensorimotor
pool of electrodes contralateral to the stimulated hand (C2, C4, C6,
T8, TP8, CP6, CP4, CP2, P2, P4, P6, P8) rereferenced to Fz electrode
which is a standard reference to estimate cortical somatosensory
responses ( Tobimatsu et al., 1999 ; Cruccu et al., 2008 ; Moungou et al.,
2016; Meinhold et al., 2022 ). EEG signals recorded during right-hand
stimulation were spatially ﬂipped over midline as if all participants
were stimulated on the left ﬁngertips. For each participant and condition,
time domain EEG signals were then averaged across trials to enhance the
signal-to-noise ratio of the neural response by attenuating the contribu-
tion of activities that were not time-locked to the stimulus ( Mouraux
et al., 2011 ; Nozaradan et al., 2011 , 2012).
Estimation of beat prominence in the brain responses: magnitude
spectrum-based analysis
For each participant and condition, the averaged time domain EEG
epochs were transformed in the frequency domain using a fast Fourier
transform (FFT), yielding frequency spectra ranging from 0 to 512 Hz
with a frequency resolution of 0.0167 Hz (1/60 s). A local baseline was
subtracted from each frequency bin in the resulting spectrum to mini-
mize the contribution of local variations of noise inherent to EEG record-
ings. The baseline was de ﬁned as the average magnitude measured at −2
to −5 and +2 to +5 frequency bins relative to each frequency bin
(Mouraux et al., 2011; Retter and Rossion, 2016). Spectra were then aver-
aged across all channels (average pool) and across modality-speci ﬁc
selections of channels (frontocentral pool for auditory and contralateral
parietal pool for somatosensory).
Identiﬁcation of the frequencies of interest
The frequencies at which the cortical responses were expected to be elic-
ited were determined based on the repetition rate of the rhythmic pat-
tern. Speci ﬁcally, the frequencies of interest constituted the pattern
repetition rate (0.417 Hz = 1/2.4 s) and harmonics, since this set of fre-
quencies captures any response that is reliably and consistently elicited
by the repeating rhythmic pattern (Lenc et al., 2025). This set of frequen-
cies was further validated using the temporal envelope of the 60 s
sequence stimuli as computed with Hilbert transform (function “hilbert”
as implemented in MATLAB 2020b). The resulting modulation signal
was then transformed in the frequency domain using an FFT, yielding
a frequency spectrum of the input envelope with a spectral resolution
of 0.0167 Hz ( Fig. 1 B; Nozaradan et al., 2016b , 2017a). The range of
included frequencies was adjusted for each modality, i.e., between 0
and 15 Hz for auditory responses and 0 and 25 Hz for somatosensory
responses (see below for the identi ﬁcation of the response bandwidth
for each modality). From the resulting set of harmonic frequencies, the
ﬁrst two frequencies were discarded from further analyses as they were
located within a frequency range (<1 Hz) typically featuring prominent
background noise in EEG spectra (due to the 1/f-like distribution of noise
over the spectrum), thus prone to unreliable measures (Cirelli et al., 2016;
Lenc et al., 2023 ). Moreover, the 12th frequency (i.e., 5 Hz) and its har-
monics were also dismissed, as their magnitude is expected to be driven
in major part by the shape of the individual 200 ms events composing the
rhythmic pattern (i.e., 1/0.2 s = 5 Hz and harmonics).
Estimation of the response frequency bandwidth for each modality
To determine the frequency range where the EEG responses for each
modality were distributed, we summed the magnitudes obtained from
the group-level averaged, baseline-corrected EEG spectra successively
over all harmonic frequencies from 0.417 Hz (i.e., 1/2.4 s) up to 30 Hz
(72 frequencies), separately for each modality. All harmonic frequencies
were taken into consideration, as the aim of this analysis was to quantify
the overall response to the rhythmic input irrespective of any higher-level
transformation. As shown in Figure 2, the curves of the summed magni-
tude as a function of frequency demonstrate a substantial gain in magni-
tude every 5 Hz. This prominent periodicity in the EEG signals re ﬂects
the responses to the recurring shortest interonset intervals making up
the rhythmic pattern (200 ms interonset or grid intervals, i.e., 5 Hz
rate). We then estimated the slope of each 5 Hz segment of the obtained
curves by ﬁ
tting a linear regression model. Finally, the response fre-
quency bandwidth was determined for each modality by identifying
the harmonic frequency at which the slope fell below an arbitrary thresh-
old of 0.01 (i.e., a gain in magnitude <0.05 mV over a range of 5 Hz). The
estimation of the response frequency bandwidth for the auditory modal-
ity was 0 –15 Hz, with most of the response concentrated below 5 Hz,
while the bandwidth of the somatosensory response was 0 –25 Hz. This
estimation was also con ﬁrmed by computing the derivative of the curve
and selecting the frequency at which the derivative was minimal and
tented toward zero. Only the frequencies of interest located within the
obtained response frequency bandwidths were further used to compute
the beat-related z-scores of the stimuli and the EEG responses for each
modality, respectively.
Z-scored signal-to-noise ratio (zSNR) measurements
To ensure that cross-modal di ﬀerences in magnitude at the frequencies
of interest were not driven by di ﬀerent quality of the signal, zSNR was
computed from the raw spectra (i.e., without baseline correction) to sta-
tistically test whether the response signi ﬁcantly stands out from
4  J. Neurosci., November 12, 2025  45(46):e0664252025 Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm
background noise in the recorded signal ( Liu-Shuang et al., 2014 ; Jonas
et al., 2016 ; Lochy et al., 2018 ; Volfart et al., 2020 ; Hagen et al., 2021 ).
First, the magnitudes at all frequency bins of interest and the respective
local noise at the surrounding bins ranging from−12 to −2 and +2 to +12
were extracted. The zSNR value was then obtained as [(average magni-
tude across frequencies of interest) − (average baseline magnitude)] /
(standard deviation of the baseline magnitude).
Measurement of relative prominence of the beat-related frequencies
The main goal of the current study was to assess, from the whole set of
frequencies of interest, the relative prominence of the frequencies consid-
ered as speci ﬁcally related to the beat versus the remaining frequencies
which are included in the stimulus envelope magnitude spectrum but
are unrelated to the beat periodicity. To this aim, the magnitude at
each of these frequencies of interest was ﬁrst standardized into z-scores
(Lenc et al., 2020 ). The obtained z-scores were then averaged separately
across beat-related frequencies (4 × 200 ms = 800 ms, i.e., 1.25 Hz and
harmonics) and beat-unrelated frequencies (i.e., the remaining frequen-
cies of interest). An average beat-related z-score higher than the corre-
sponding beat-related z-score calculated from the stimulus envelope
spectrum (acoustic rhythm z-score = −0.059; tactile rhythm z-score =
−0.051) would thus re ﬂect selectively enhanced beat periodicity in the
EEG compared with the input.
In addition, to assess whether the transformations observed in the
EEG responses to the acoustic rhythm could not be explained by
responses at the peripheral stages of sound processing, we also compared
the recorded EEG responses to responses simulated with a biologically
plausible model of peripheral auditory processing (hereafter cochlear
model; Lenc et al., 2018 , 2020). The cochlear model used to analyze
the acoustic stimuli consisted in an equivalent rectangular bandwidth
ﬁlter bank with 64 channels ( Patterson and Holdsworth, 1996), followed
by Meddis’ inner hair-cell model ( Meddis, 1986), as implemented in the
Auditory Toolbox for MATLAB ( Slaney, 1998 ). The output of the
cochlear model was subsequently transformed into the frequency
domain using FFT, and the obtained spectra were then averaged across
cochlear channels. The beat-related z-score was then computed as
described above (acoustic rhythm z-score from the model = −0.126,
i.e., showing even less emphasis of the beat periodicities as compared
with the envelope of the acoustic signal itself, as obtained with a
Hilbert transform).
Estimation of beat prominence in the brain responses:
autocorrelation-based analysis
A complementary approach was applied to analyze the prominence of
beat-related periodicities in brain responses using autocorrelation ( Lenc
et al., 2025
). This novel autocorrelation-based analysis aimed to
corroborate the results obtained with the magnitude spectrum-based anal-
ysis described above. Critical to the current study, the autocorrelation-
based approach has the advantage of providing an estimate of periodicity
that is invariant to the shape of the recurring signal. This is of major impor-
tance here, because diﬀerences in the brain responses elicited by the acous-
tic versus tactile sequences could be driven by characteristics unspeciﬁct o
any actual beat-related periodization of the input but rather by cross-modal
diﬀerences in the overall shape of the responses due to lower-level proper-
ties speciﬁc to each sensory modality. In other words, because the shape of
the response to single acoustic versus tactile events is expected to diﬀer, and
because these di ﬀerences would favor some frequencies in one modality
and not the other, it is crucial to control this using an analysis that is insen-
sitive to the response shape. As implemented here, the autocorrelation
function (ACF) was estimated from the complex spectrum after subtract-
ing an estimate of the 1/f-like noise and zeroing out frequency bins that did
not correspond to the frequencies of interest. This later step is justiﬁed by
the fact that the response was elicited by a stimulus consisting of a seam-
lessly looped rhythmic pattern and was therefore expected to elicit a
response that only contains energy at the exact frequency bins correspond-
ing to integer multiples of the rhythmic pattern repetition rate (Lenc et al.,
2025), i.e., within the set of beat-related and beat-unrelated frequencies
deﬁned above (see above, Identi ﬁcation of the frequencies of interest).
From this ACF, we extracted autocorrelation values at lags of interest cor-
responding to (1) beat periodicities (beat-related lags, 0.8 s and multiples
from which 2.4 s corresponding to the pattern duration was excluded)
and (2) control lags corresponding to periodicities where the beat was
not perceived despite being compatible with the temporal arrangement
of the sounds making up the rhythmic stimulus (beat-unrelated lags, 0.6,
1, 1.4, and 1.8 s and multiples). Overlapping beat-related and
beat-unrelated lags were excluded. After normalizing the autocorrelation
coeﬃ cients across the whole set of lags using z-scoring, the periodicity of
the response at the rate of the beat was quantiﬁed by averaging the coeﬃ -
cients across beat-related lags (for further methodological details, seeLenc
et al., 2025). An average beat-relatedz-score higher than the corresponding
beat-related z-score calculated from the stimulus envelope spectrum
(z-score =−0.409 for both acoustic and tactile rhythms) would thus reﬂect
selectively enhanced beat periodicity in the EEG compared with the input.
Tapping recording and analysis
The tap onsets generated by the tapping box were sent as analog triggers
to the EEG system and recorded at the same sampling rate as the EEG
signal (i.e., 1,024 Hz). The force signal continuously monitored by the
tapping box was digitalized at 44,100 Hz and recorded by means of an
audio interface (Fireface UC, RME). The time series of the continuous
force signal were downsampled to 1,024 Hz after having been low-pass
ﬁltered at 300 Hz (i.e., below the Nyquist frequency of the target
Figure 2. Modality-speciﬁc EEG frequency bandwidths. EEG responses show frequency bandwidths with lower cuto ﬀ for acoustic (0–15 Hz, in purple) than tactile (0 –25 Hz, in green) input.
The modality-speciﬁc bandwidths were determined based on the summed magnitudes over harmonic frequencies of the pattern repetition rate, measured from the group-level averaged EEG
magnitude spectrum, separately for each modality. Obtained summed magnitudes (gray curve) are superimposed with red dashed lines corresponding to linear functions ﬁtted to 5-Hz-long
segments across the spectra. The slopes of the ﬁtted lines show faster convergence toward zero for the auditory EEG responses, revealing the lower cuto ﬀ of their bandwidth. Note that most of
the auditory response is concentrated below 5 Hz.
Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm J. Neurosci., November 12, 2025  45(46):e0664252025  5
sampling rate) to avoid aliasing. Time series of tap onsets were converted
into a continuous time domain signal with duration corresponding to the
length of the stimulus sequence and sampled at 1,024 Hz. The value of
each sample corresponding to a tap onset time was set to 1 (i.e., a unit
impulse) and 0 otherwise.
Circular analysis of tapping
The period of the beat perceived by the participants was determined
based on an estimation of the periods that were most consistently tapped
across participants. This was achieved by computing the median intertap
interval (ITI) using the tap onset times (i.e., times at which the ﬁnger
contacted the tapping box) for each trial, block, and participant sepa-
rately. Because participants typically waited a few sensory events before
starting to tap along with the rhythmic input, the ﬁrst 2.4 s (i.e., temporal
window of the ﬁrst pattern presentation) was discarded.
To quantify the tapping performance of each participant, we then
evaluated the stability of tapping with respect to the beat period (i.e.,
period locking) by calculating a circular measure, namely, the mean vec-
tor length (Berens, 2009; Nozaradan et al., 2016a). This measure was cal-
culated by ﬁrst selecting, based on the median ITI of each participant, the
closest plausible beat period, i.e., the beat period most likely targeted by
the participant (with plausible beat periods corresponding here to any
integer multiple of the 200 ms grid interval that would ﬁt within the
2.4 s rhythmic pattern, thus yielding six plausible beat periods in total:
200, 400, 600, 800, 1,200, or 2,400 ms). The obtained target beat period
was then used to compute a time series of target beat positions, with
phase zero set in accordance with the ﬁrst tap of each trial.
The signed di ﬀerence between each tap and the closest target beat
position was then converted into an angle and mapped onto a unit circle.
The resulting unit vectors were then averaged across trials, and the length
of the mean vector served as an index of beat stability. This mean vector
length thus reﬂected the “consistency” of asynchronies between taps and
the corresponding beat positions, i.e., the strength of period locking
between the beat and the tapping response ( Rosenblum et al., 2001 ).
Finally, to compare the tapping stability between blocks and participants,
we obtained a single stability value per block and participant by ﬁrst sub-
tracting for each trial the angle of the mean vector from the unit vectors
corresponding to individual taps, then by collapsing the obtained values
across trials, and ﬁnally by recalculating the mean vector.
Magnitude spectrum-based analysis of tap onsets and tap force
As a complementary estimate of stability in tapping to the beat, single tri-
als of (1) time series of tap onsets and (2) continuous force signals as
recorded by the tapping box were also transformed in the frequency
domain using FFT. For each block and participant, and similarly to the
analysis described above for stimulus input and EEG responses, z-scores
of beat-related and beat-unrelated frequencies were then calculated from
the magnitude spectrum obtained for each trial and subsequently aver-
aged across trials. The frequency ranges of interest were de ﬁned as for
EEG responses using the changes in slopes of the 5 Hz chunks obtained
by successively summing the magnitude across harmonics of the pattern
duration as computed on the group-level averaged magnitude spectrum
for each type of signal (time series of tap onsets and tap force) and
modality. Tapping responses were mainly distributed between 0 and
10 Hz for both types of signals and both sensory modalities.
Autocorrelation-based analysis of tap onsets and tap force
The relative prominence of beat periodicities was also assessed in time
series of tap onsets and tap force using the novel implementation of
the frequency-tagging approach based on autocorrelation as described
above for EEG responses ( Lenc et al., 2025 ). Since tapping responses
are not expected to contain a prominent 1/ f-like noise component, the
ACF was estimated directly from the raw complex spectrum.
Head movements control
Unintentional periodic head movements of participants synchronized to
the perceived beat during the EEG recording may potentially enhance
beat-related periodicities in the obtained EEG responses. To rule out
such artifacts, we monitored head movements by means of a two-axes
accelerometer ( x for left-right, y for back-front) strapped on the EEG
cap at the vertex. Signals were acquired at a 1,024 Hz sampling rate.
The relative prominence of beat-related frequencies was estimated in
the accelerometer data in the same way as for tapping data.
Statistical analyses
The statistical analyses were conducted using JASP (JASP Team 2023,
Version 0.17.2). First, we veri ﬁed that the data followed a normal distri-
bution using Shapiro –Wilk tests. To assess if the order of blocks
inﬂuenced the diﬀerent measures obtained from EEG or tapping, we per-
formed mixed repeated-measures analyses of variance (RM-ANOVAs)
with “Group” as a between-subject factor (Group 1 acoustic –tactile–tac-
tile vs Group 2 tactile –acoustic–tactile vs Group 3 tactile –tactile–acous-
tic) and “Block” as a within-subject factor (acoustic block vs ﬁrst tactile
block vs second tactile block). For between-subject comparisons, homo-
geneity of variance was veri ﬁed using Levene’s test. Sphericity was tested
using Mauchly ’s test and F values were Greenhouse –Geisser corrected
when this assumption was violated. Post hoc comparisons were then per-
formed using t tests, with Holm correction for multiple comparisons. In
case of nonparametric testing, Friedman tests were performed with the
factor “Block,” with Conover ’s tests used for post hoc comparisons. In
addition to this frequentist analysis, we also calculated Bayes factors
(BF10) to quantify the probability of the data under di ﬀerent models
(Rouder et al., 2017 ; van den Bergh et al., 2020 ). Then, the inclusion
Bayes factor (BFincl) was estimated for each model’s predictor to quantify
the evidence in favor of including each of those predictors in the best
model.
Finally, to assess the periodization of the EEG responses with respect
to the input, we performed one-sample t tests between the beat-related
z-scores of the EEG and the beat-related z-scores of the stimuli for
each modality.
Code accessibility
The code for the autocorrelation-based approach analysis is available at
https://github.com/TomasLenc/acf_tools. Acoustic and tactile stimuli
are available upon request.
Results
Tapping data
Convergent beat periodicities across modalities revealed by
tapping
Median ITI indicated beat periodicities converging at 800 ms
(corresponding to the grouping of four 200 ms grid intervals,
i.e., three beats within each pattern repetition). Subject-level
median ITIs were not signi ﬁcantly diﬀerent between groups cor-
responding to di ﬀerent orders of block presentation (main e ﬀect
of group, F
(2,42) = 0.454; p = 0.638; ηp
2 = 0.021; RM-ANOVA).
Moreover, the median ITIs did not di ﬀer between blocks
(Fig. 3 A; main e ﬀect of block, F(1.3,54.73) = 2.412; p = 0.118;
ηp
2 = 0.054), and no signi ﬁcant Group × Block interaction was
observed ( F(2.6,54.73) = 0.573; p = 0.611; ηp
2 = 0.027). These results
were corroborated by a Bayesian RM-ANOVA which showed
that the null model better explained the data than any other
model including the Group and Block factors and their interac-
tion (all BF
10 ≤ 0.584).
Reduced beat periodicities in tapping to tactile versus acoustic
inputs
Beat tapping stability. The obtained beat tapping stability as esti-
mated with mean vector length yielded values deviating from a
normal distribution (Shapiro –Wilk test, p < 0.002), which jus-
tiﬁed further use of Friedman tests for comparison across blocks
and groups and Conover ’s tests for post hoc comparisons. The
Friedman test revealed a signi ﬁcant eﬀect of Group (correspond-
ing to di ﬀerent orders of block presentation; χ
2
(2) = 18.711;
p = 8.648 × 10−5; W = 0.208). Conover ’s post hoc comparisons
showed signiﬁcant diﬀerences between blocks ( Fig. 3B), namely,
6  J. Neurosci., November 12, 2025  45(46):e0664252025 Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm
with larger stability for the acoustic block as compared with the
ﬁrst tactile ( p = 1.218 × 10−4) and second tactile block ( p = 0.048)
and between the two tactile blocks ( p = 0.045). These results were
corroborated by a Bayesian RM-ANOVA which showed that
the model including the Block factor (evidence for Block e ﬀect
BF
incl = 7,403.78) better explained the data than the null model
or any model including the Group factor (all BF 10 ≤ 0.366).
Beat prominence in tap onsets time series. The mean z-scored
magnitudes at beat-related frequencies obtained using magni-
tude spectrum-based analysis corroborated the results obtained
above with mean vector length. Namely, the z-scored
values were not a ﬀected by the factor Group ( F
(2,42) = 0.168;
p = 0.846; ηp
2 = 0.008; RM-ANOVA). There was a signi ﬁcant
eﬀect of Block ( F(1.57,65.95) = 12.405; p = 1.057 × 10−4; ηp
2 = 0.228;
RM-ANOVA), and no signi ﬁcant Group × Block interaction
(F(3.14,65.95) = 0.360; p = 0.791; ηp
2 = 0.017). Post hoc comparisons
showed that beat-related frequencies were signi ﬁcantly more
prominent in the acoustic block as compared with the ﬁrst
(t(44) = 4.733; p = 2.663 × 10−5; Cohen ’s d = 0.450) and second
tactile blocks ( t(44) = 3.712; p =7 . 3 8 6×1 0−4; Cohen ’s d = 0.353;
paired t test), and the two tactile blocks were not signi ﬁcantly
diﬀerent from each other ( t(44) = −1.021; p = 0.310; Cohen ’s d =
−0.097; paired t test; Fig. 4 A). These results were corroborated
by a Bayesian RM-ANOVA, which showed that the best model
included only the Block factor (e ﬀect of Block BF
incl = 1,397.7)
and better explained the data than the null model or any models
including the Group factor (all BF
10 ≤ 0.379).
The results were further con ﬁrmed using beat-related
z-scored values obtained by the autocorrelation-based analysis
at beat-related lags ( Fig. 4 B). There was no signi ﬁcant
main e ﬀect of Group ( F(2,42) = 1.0; p = 0.376; ηp
2 = 0.045;
RM-ANOVA), a signi ﬁcant e ﬀect of Block ( F(1.49,62.43) = 7.487;
p = 0.003; ηp
2 = 0.151; RM-ANOVA), and no signi ﬁcant Group ’
Block interaction ( F(2.97,62.43) = 0.572; p = 0.634; ηp
2 = 0.027).
Post hoc comparisons showed that beat-related lags were signi ﬁ-
cantly more prominent in the acoustic block as compared with
the ﬁrst ( t
(44) = 3.721; p = 0.001; Cohen ’s d = 0.360) and second
tactile blocks ( t(44) = 2.781; p = 0.013; Cohen’s d = 0.269; paired t
test), and the two tactile blocks were not signi ﬁcantly di ﬀerent
from each other ( t(44) = −0.940; p = 0.350; Cohen ’s d = −0.091;
paired t test). The frequentist statistics were corroborated by a
Bayesian RM-ANOVA which showed that the best model
included only the Block factor (e ﬀect of Block BF
incl = 28.46)
and better explained the data than the null model or any models
including the Group factor (all BF
10 ≤ 0.551).
Beat prominence in force signal time series. Due to a technical
problem, the force signal was recorded in 36 participants out
of 45. Nevertheless, the analyses of beat prominence using the
force signal converged with those performed on tap onsets.
Mean z-scores obtained from the magnitude spectrum-based
analysis were not a ﬀected by the group order of the blocks
(F
(2,33) = 0.335; p = 0.718; ηp
2 = 0.020; RM-ANOVA). There was
a signi ﬁcant e ﬀect of Block ( F(1.68,55.43) = 11.768; p = 1.360 ×
10−4; ηp
2 = 0.263; RM-ANOVA) and no signi ﬁcant Group ×
Block interaction ( F(3.36,55.43) = 2.106; p = 0.103; ηp
2 = 0.113).
Post hoc comparisons showed that beat-related frequencies
were signiﬁcantly more prominent in the acoustic block as com-
pared with the ﬁrst tactile ( t
(44) = 2.070; p = 0.042; Cohen ’s
d = 0.399; paired t test) and second tactile blocks ( t(44) = 4.835;
p = 2.495 × 10−5; Cohen ’s d = 0.931; paired t test). As compared
with the analyses of onsets time series, the only noticeable di ﬀer-
ence was the signi ﬁcant decrease of beat-related z-scores in the
second versus ﬁrst tactile block ( t(44) = 2.765; p = 0.015; Cohen’s
d = 0.532; paired t test; Fig. 4C). The eﬀect of block was supported
by a Bayesian RM-ANOVA which showed that the best model
included only the Block factor (e ﬀect of Block BF
incl = 3,680.16)
and better explained the data than the null model or any models
including the Group factor (all BF
10 ≤ 0.216).
The results on force time series were con ﬁrmed using the
mean z-scored values obtained with the autocorrelation-based
analysis at beat-related lags ( Fig. 4D), also in line with the results
obtained from the autocorrelation-based analysis of tap onsets
(Fig. 4 B). There was no signi ﬁcant main e ﬀect of Group
(F(2,33) = 1.625; p = 0.212; ηp
2 = 0.073; RM-ANOVA), a signi ﬁcant
eﬀect of Block ( F(1.42,46.91) = 6.161; p = 0.009; ηp
2 = 0.157; RM-
ANOVA), and no signi ﬁcant Group ’ Block interaction
Figure 3. The tapping task reveals signiﬁcantly lower beat tapping stability in response to the tactile versus acoustic rhythm. A, Subject-level median ITIs (one dot per participant; error bars
indicate interquartile ranges) for each block condition. The tapped beat periods converged toward 800 ms across all blocks (4 × 200 ms grid interval, i.e., 3 beats per pattern repetition). One data
point ∼2.4 s in the three blocks is omitted from the plot for visualization purposes. B, Tapping stability (one dot per participant; horizontal lines indicate the median; left-shaded boxes indicate
interquartile ranges; ﬁtted distribution densities are displayed on the right, separately for each block). Tapping stability was signi ﬁcantly reduced in the tactile conditions as compared with the
acoustic condition (i.e., resultant vector length of the circular distribution of asynchronies between taps and beat positions closer to zero). Not e that both panels A and B depict each block,
irrespective of the order in which they were presented (given the absence of order eﬀect). Asterisks indicate signiﬁcant diﬀerences between blocks obtained from Conover’s post hoc comparisons
(*p < 0.05; ***p < 0.001).
Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm J. Neurosci., November 12, 2025  45(46):e0664252025  7
(F(2.84,46.91) = 0.27; p = 0.836; ηp
2 = 0.016). Post hoc comparisons
showed that beat-related lags were signi ﬁcantly more prominent
in the acoustic block as compared with the ﬁrst ( t(44) = 3.362;
p = 0.004; Cohen ’s d = 0.412) and second tactile blocks
(t(44) = 2.555; p = 0.026; Cohen ’s d = 0.313; paired t test), and
the two tactile blocks were not signi ﬁcantly di ﬀerent from each
other ( t(44) = −0.807; p = 0.422; Cohen ’s d = −0.099; paired
t test). These results were corroborated by a Bayesian
RM-ANOVA which showed that the best model included only
the Block factor (e ﬀect of Block BF
incl = 7.186) and better
explained the data than the null model or any models including
the Group factor (all BF
10 ≤ 0.750).
EEG responses
Reduced beat periodicities in brain responses to tactile versus
acoustic rhythms
The mean z-scored beat –related frequencies obtained using the
magnitude spectrum-based approach were not a ﬀected by the
group order of the blocks ( F(2,42) = 0.661; p = 0.522; ηp
2 = 0.031;
RM-ANOVA). There was a signi ﬁcant e ﬀect of the Block
(F(1.94,81.46) = 37.044; p = 5.85 × 10−12; ηp
2 = 0.469; RM-ANOVA)
and a signi ﬁcant Group × Block interaction ( F(3.88,81.46) = 3.769;
p = 0.008; ηp
2 = 0.152). Post hoc comparisons showed that
beat-related frequencies were signi ﬁcantly more prominent in
the acoustic block as compared with the ﬁrst ( t(44) = 8.240;
p = 6.008 × 10−12; Cohen ’s d = 1.648; paired t test) and second
tactile blocks ( t(44) = 6.274; p = 2.927 × 10−8; Cohen ’s d = 1.255;
paired t test) which were not signi ﬁcantly di ﬀerent from each
other ( t(44) = −1.966; p = 0.158; Cohen ’s d = −0.393; paired
t test; Fig. 5 A). These results were supported by a Bayesian
RM-ANOVA which showed that the model that better explained
the data included both Block and Group factors and
their interaction as compared with any other models
(BF
10 ≤ 0.575). There is decisive evidence for the e ﬀect of Block
(BFincl = 1.956 × 1010) followed by strong evidence for the Block
× Group interaction (BFincl = 10.991) and no evidence for includ-
ing the Group factor (BF incl = 0.158).
To assess the periodization of the input in the EEG responses,
one-sample t tests were performed between the beat-related
z-scores of the EEG responses and the corresponding stimulus,
Figure 4. Tapping data show greater prominence of the beat periodicity in response to acoustic versus tactile rhythm. Tap onsets and tapping force are depicted in A and B and C and D,
respectively. Magnitude spectrum-based and autocorrelation-based analyses are depicted in A and C and B and D, respectively. Note the signi ﬁcantly greater periodization of acoustic versus
tactile input (one dot per participant; colored horizontal lines indicate means; boxes show 95% conﬁdence intervals; gray lines for corresponding values from stimulus envelope). Asterisks indicate
signiﬁcant diﬀerences between blocks obtained from the pairwise post hoc comparisons ( *p < 0.05; **p < 0.01; ***p < 0.001).
8  J. Neurosci., November 12, 2025  45(46):e0664252025 Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm
separately for each modality. For the auditory modality, z-scored
magnitudes of beat-related frequencies in the EEG response were
signiﬁcantly larger than in the stimulus beat-relatedz-score calcu-
lated from the envelope spectrum ( t
(44) =6 . 9 0 7 ;p = 7.818 × 10−9;
Cohen’s d = 1.030; one-sided one –sample t test against stimulus
z-score of −0.059) and from the cochlear model ( t(44) =9 . 5 6 7 ;
p =1 . 2 8 3×1 0−12;C o h e n’s d = 1.426; one-sided one–sample t test
against stimulus z-score of −0.126). This was not the case in the
somatosensory modality (Tactile 1 block, t(44) = −5.258; p =1 . 0 0 ;
Cohen’s d = −0.784; and Tactile 2 block, t(44) = −0.815; p =0 . 7 9 0 ;
Cohen’s d = −0.121; one-sided one–sample t tests against stimulus
z-score of −0.051).
Reduced beat periodicities in brain responses to tactile versus
acoustic rhythms, corroborated with autocorrelation-based
analysis
Importantly, the results of beat prominence in the EEG as
obtained with the magnitude spectrum-based analysis were
conﬁrmed by the autocorrelation-based analysis ( Fig. 5 B). The
mean z-scored magnitudes at beat-related lags were not a ﬀected
by the group order of the blocks ( F
(2,42) = 2.263; p = 0.117; ηp
2 =
0.097; RM-ANOVA). There was a signi ﬁcant e ﬀect of Block
(F(1.81,76.05) = 12.464; p = 3.879 × 10−5; ηp
2 = 0.229; RM-ANOVA)
and a signi ﬁcant Group × Block interaction ( F(3.62,76.05) = 2.121;
p = 0.093; ηp
2 = 0.092). Post hoc comparisons showed that
beat-related lags were signi ﬁcantly more prominent in the
acoustic block as compared with the ﬁrst tactile ( t(44) = 4.626;
p = 4.02 × 10−5; Cohen’s d = 0.960; paired t test) and second tac-
tile ( t(44) = 3.940; p = 3.362 × 10−4 ; Cohen ’s d = 0.818; paired
t test) blocks which were close to be signi ﬁcantly di ﬀerent
from each other ( t(44) = −0.687; p = 0.494; Cohen ’s d = −0.143;
paired t test). These results were supported by a Bayesian
RM-ANOVA which showed that the model that better explained
the data included the Block factor as compared with any other
models (BF
10 ≤ 0.41). Indeed, there was decisive evidence for
the e ﬀect of block (BF incl =3,181.42), weak evidence for the
Block × Group interaction (BF incl = 1.091), and no evidence for
including the Group factor (BF incl = 0.376).
Similarly, as in the magnitude spectrum-based analysis, the
beat-related z-scores obtained using the autocorrelation-based
analysis showed a lack of periodization of the input in the EEG
response to the tactile rhythm as opposed to the acoustic rhythm.
Z-scored magnitudes of beat-related frequencies in the EEG
response to the acoustic rhythm were signi ﬁcantly larger than
in the stimulus z-scores obtained from the envelope spectrum
(t
(44) = 6.495; p = 3.156 × 10−8; Cohen ’s d = 0.968; one-sided
one–sample t test against stimulus z-score of −0.409) and from
the cochlear model ( t(44) = 6.76; p = 1.288 × 10−8; Cohen ’s
d = 1.008; one-sided one –sample t test against stimulus z-score
of −0.432). This was not the case for EEG responses to the tactile
rhythm (Tactile 1 block, t(44) = −0.004; p = 0.502; Cohen ’s
d = −6.544 × 10−4, and Tactile 2 block, t(44) = 0.848; p = 0.201;
Cohen’s d = 0.126; one-sided one–sample t tests against stimulus
z-score of −0.409).
Additional control analyses
To control for potential biases in our analyses, we conducted sev-
eral additional analyses.
Ruling out confounds with overall magnitude of the EEG responses
To ensure that any diﬀerences observed between conditions were
not trivially explained by di ﬀerences in the overall magnitude
of the responses irrespective of any beat-related periodization
of the input, zSNR were computed for each block by pooling
over magnitudes at all frequencies of interest (i.e., including all
frequencies tagged as beat-related and beat-unrelated, within
the response frequency bandwidth speci ﬁc to each modality).
The obtained zSNR values signi ﬁcantly deviated from a normal
distribution (Shapiro –Wilk test, p ≤ 0.029). The Friedman test
revealed a signi ﬁcant e ﬀect of block ( χ
2
(2) = 10.711; p = 0.005;
W = 0.119). Conover’s post hoc comparisons showed signi ﬁcant
diﬀerences between the acoustic and ﬁrst tactile blocks
Figure 5. EEG responses show greater prominence of the beat periodicity for acoustic versus tactile rhythm, in line with tapping responses. A, Magnitude spectrum-based analysis.
B, Autocorrelation-based analysis. Note the signi ﬁcantly reduced periodization for tactile versus acoustic inputs (cross-block and against-stimulus comparison). Horizontal lines represent mean s
and boxes indicate 95% conﬁdence intervals. Each dot represents a participant. The horizontal gray lines correspond to the stimuli z-scored magnitude at beat-related frequencies (A) or lags (B).
Asterisks indicate signi ﬁcant diﬀerences between blocks obtained from the post hoc pairwise comparisons ( ***p < 0.001). The octothorpes indicate signi ﬁcant diﬀerences obtained from the
one-sided one–sample t tests of the EEG z-scores against the stimulus z-scores (###p < 0.001).
Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm J. Neurosci., November 12, 2025  45(46):e0664252025  9
(p = 0.005) and no signi ﬁcant di ﬀerence between acoustic and
second tactile blocks nor between tactile blocks ( p = 0.153).
Therefore, the di ﬀerences in overall signal magnitude could not
directly explain the cross-modal di ﬀerences in beat-related peri-
odization observed in the EEG data.
Excluding contribution of unintentional head movement artifacts
in EEG responses
To rule out the possibility that beat-related periodization of the
input in the EEG was driven by artifacts related to unintentional
head movements of participants during the EEG recording, we
estimated the prominence of beat periodicities in the accelerom-
eter data (averaged across the two accelerometer axes) during
EEG recording using the magnitude spectrum-based analysis.
Due to a technical problem, accelerometer data were available
for 41 participants out of 45. We compared the obtained z-scored
magnitude of beat periodicities in the head movements to the
corresponding values from the stimulus. There was a signi ﬁcant
increase of beat periodicities in each block: acoustic ( t
(40) = 2.704;
p = 0.010; Cohen’s d = 0.420; one-sided one–sample t test against
stimulus z-score of −0.126), ﬁrst tactile ( t(40) = 3.306; p = 0.002;
Cohen’s d = 0.516; one-sided one –sample t test against stimulus
z-score of −0.051), and second tactile ( t(40) = 2.865; p =0 . 0 0 7 ;
Cohen’s d = 0.447; one-sided one –sample t test against stimulus
z-score of −0.051). However, there was no signiﬁcant main eﬀect
of Block ( F(1.65,62.69)= 0.255; p =0 . 7 3 3 ;ηp
2 =0 . 0 0 7 ; R M - A N O V A ) ,
Group ( F(2,38) =1 . 0 4 5 ;p =0 . 3 6 2 ;ηp
2 = 0.052; RM-ANOVA),
or Block × Group interaction ( F(3.3,62.69)=1 . 7 4 1 ; p =0 . 1 6 3 ;
ηp
2 = 0.084; RM-ANOVA). Therefore, the unintentional head
movements produced during EEG recordings were unlikely to
explain the cross-modal di ﬀerences in beat-related periodization
observed in the EEG.
Modality-speciﬁc versus common average montages for EEG
analyses
To ensure that the choices of the modality-speci ﬁc pools of EEG
channels and corresponding rereferencing did not bias the
results, the same magnitude spectrum-based analysis of beat
prominence in the EEG responses was performed on the signal
extracted from all EEG channels rereferenced to the common
average for both modalities. The results converged with the anal-
yses performed on signals obtained from modality-speci ﬁc mon-
tages. There was a signi ﬁcant main e ﬀect of Block ( F
(1.79,75.29) =
38.586; p = 1.299 × 10−12; ηp
2 = 0.479; RM-ANOVA), no signi ﬁ-
cant main e ﬀect of Group ( F(2,42) = 0.082; p = 0.921; ηp
2 = 0.004;
RM-ANOVA), and no signi ﬁcant Block × Group interaction
(F(3.58,75.29) = 0.198; p = 0.924; ηp
2 = 0.009; RM-ANOVA).
Discussion
The current study shows that mapping periodic beats onto an
acoustic rhythm is related to enhanced beat periodicities in the
neural representation of the rhythm. Moreover, this neural
enhancement of the beat selectively projects onto a low-
frequency range (under 15 Hz, mainly under 5 Hz). In contrast,
presenting the same rhythm through the somatosensory modal-
ity does not produce such periodic neural enhancement, despite
signiﬁcant and comparably robust neural responses to the tactile
rhythm. Importantly, this cross-sensory di ﬀerence converges
with diﬀerences in the ability to tap the beat along with the acous-
tic versus tactile rhythm.
In sum, internal representation of a rhythm that might be
experienced as a periodic beat seems preferentially supported
by periodized low-frequency neural activity. However, these
higher-level neural representations are not necessarily shared
across the senses. Such periodized low-frequency neural activity
may thus re ﬂect temporal integration across multiple timescales
beyond onset timing, a distinctive specialization of the auditory
system, that supports higher-level internal representation and
motor coordination with rhythm.
Periodized neural and behavioral representation of acoustic
versus tactile rhythm
Most studies that investigated rhythm perception and sensorimo-
tor synchronization across the senses have focused on instances
where synchronization was meant to be performed in a one-to-one
manner with the rhythmic input ( A m m i r a n t ee ta l . ,2 0 1 6;
Tranchant et al., 2017; Gilmore and Russo, 2021). In other words,
the goal was to synchronize each movement with the onset of each
sensory event. In contrast, moving to the perceived beat along with
the rhythm used here, where the beat is not prominently cued,
necessitates going beyond such a one-to-one mapping. Namely,
it requires an internal representation showing higher degree of
invariance with respect to the temporal structure of the rhythmic
input. Notably, this phenomenon is not a peculiarity of experimen-
tal design constraints or of speci ﬁc music genres but abounds in
music worldwide ( Butler, 2006 ; London, 2012 ; London et al.,
2017; Witek, 2017; Câmara and Danielsen, 2018).
In the current study, the neural responses to the acoustic—but
not tactile —rhythm show a speci ﬁc, behaviorally relevant,
enhancement of the beat period, for rhythmic inputs with a
weak prominence of that beat period. This result adds to the
growing evidence showing that this kind of neural enhancement
could reﬂect internal templates of periodic beats, beyond lower-
level sensory confounds (Tal et al., 2017; Nozaradan et al., 2017a;
Lenc et al., 2021 ).
Another important observation is that a vast majority of par-
ticipants spontaneously tap the beat at convergent periods,
whether the rhythm is acoustic or tactile. However, while the tap-
ping period is shared across sensory modalities, the stability in
tapping the beat period is signi ﬁcantly lower for tactile versus
acoustic rhythm. This lower tapping stability, together with the
lack of emphasis of the beat period in the EEG activity, suggests
a functional link between the two measures. Yet, neural and
behavioral observations o ﬀer a window onto di ﬀerent processes
recruited over very contrastive tasks —namely, experiencing a
rhythm while being instructed to stay still versus actively produc-
ing synchronized movements—which might diﬀerently aﬀect the
nature of the underlying internal representations emerging dur-
ing each of these tasks, respectively ( Su and Pöppel, 2012 ;
Manning and Schutz, 2013 ). Nonetheless, while plausibly linked,
these measures do not capture the underlying processes in a strict
one-to-one fashion, thus highlighting their complementarity in
understanding beat perception.
Low-frequency neural activity supports periodization of
acoustic but not tactile rhythm
In the current study, neural response to the acoustic rhythm selec-
tively projects onto the low-frequency range, mainly under 5 Hz. In
the time domain, this low-frequency activity manifests as slow
ﬂuctuations punctuated by more transient responses to each sen-
sory event onset (Fig. 5). This low-frequency activity could be a fea-
ture enabling the auditory system to integrate fast incoming events
into slower, behavior-relevant, temporal units, which is critical to
further coordinate body movement with rhythmic inputs.
Importantly, this observation is in line with the crucial role of delta
(<4 Hz) and theta (4 −8 Hz) band oscillations in subserving
10  J. Neurosci., November 12, 2025  45(46):e0664252025 Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm
multiscale temporal integration of temporally structured input
such as music and speech in humans ( Doelling et al., 2014; Arnal
et al., 2015a ; Teng et al., 2016 , 2018) and nonhuman primates
(Lakatos et al., 2005, 2016; Schroeder and Lakatos, 2009).
In contrast to the acoustic rhythm, the tactile rhythm elicits neu-
ral activity encompassing a wider frequency range, with responses
mainly concentrated at 5 Hz and harmonics up to 25 Hz (i.e., har-
monics of the 200 ms grid interval period). In the time domain, this
higher-frequency activity takes the form of short transient responses
faithfully tracking each sensory event onset and returning to the
baseline before the next onset occurs. Such a faster timescale is in
line with the preferential response bandwidth of 20 –30 Hz previ-
ously reported for somatosensory evoked responses ( Tobimatsu
et al., 1999 ; Vlaar et al., 2015 ; Ahn et al., 2016 ). More generally,
this faster response could re ﬂect a more discrete processing of
incoming tactile inputs (de Haan and Dijkerman, 2020), to the det-
riment of temporal integration over longer timescales.
Capturing neural activity compatible with primary auditory
and somatosensory cortices
The current study captured neural responses to rhythm with
topographical distributions indicative of di ﬀerent contributions
of cortical areas ( Fig. 6). More speci ﬁcally, the scalp topography
of the somatosensory response is qualitatively compatible with
activity originating from cortical generators with a dipole axis
tangential to the scalp and perpendicular to the central sulcus
in the hemisphere contralateral to the stimulated hand, i.e., pri-
mary somatosensory cortex (S1) generators ( Allison et al.,
1989; Moungou et al., 2016 ).
The frontocentral topographical distribution of the auditory
response is known to mainly re ﬂect activity originating from
bilateral Heschl ’s gyri, i.e., A1 generators ( Pantev et al., 1988 ;
Picton, 2011 ; Tan et al., 2016 ). However, such a topography
does not itself rule out substantial contributions of other median
brain regions ( Mouraux and Iannetti, 2009 ; Somervail et al.,
2021). Nevertheless, based on recent evidence for signiﬁcant neu-
ral enhancement of the beat period observed in the human
Heschl’s gyrus ( Nozaradan et al., 2017a ; Lenc et al., 2023 ), it
can be reasonably assumed that A1 is embedded into a brain net-
work enabling this higher-level temporal integration and ulti-
mately yielding beat-related periodization of rhythmic input.
Similarly, S1 is also embedded in a functional network which
comprises higher-order associative and motor areas such as the
cingulate cortex and supplementary motor area, as evidenced
by studies assessing temporal integration of tactile input in the
context of working memory tasks ( Harris et al., 2002 ;
Figure 6. EEG responses in the time (left) and frequency domains (right) show slowerﬂuctuations (lower-frequency) in response to the acoustic rhythm and more transient (higher-frequency)
responses to tactile rhythm. Grand-average EEG responses in the acoustic (rowA; frontocentral pool of electrodes referenced to the averaged mastoids), andﬁrst and second tactile blocks (rows B
and C, respectively; sensorimotor pool of electrodes contralateral to the stimulated hand referenced to Fz). The response time course is averaged across all repetitions of the rhythmic pattern
making up the stimulus sequences. Note that the auditory response time course shows transient responses to single sensory events composing the patte rn (in gray), embedded into slow
ﬂuctuations of the signal. In contrast, somatosensory responses do not exhibit such slow ﬂuctuations. On the right, the grand-average magnitude spectra show magnitude of the auditory
response located within 0 –15 Hz and mainly below 5 Hz, and magnitude of the somatosensory response spread over 0 –25 Hz (beat-related and beat-unrelated frequencies in red and
blue, respectively), in line with the estimated modality-speci ﬁc EEG response frequency bandwidths displayed in Figure 2 . Inserts show scalp topographies of the averaged magnitude at
beat-related and beat-unrelated frequencies within each modality-speci ﬁc frequency bandwidth.
Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm J. Neurosci., November 12, 2025  45(46):e0664252025  11
Numminen et al., 2004 ). Importantly, these studies revealed a
gradient of temporal integration from S1 to these higher-order
brain regions, with the latter speci ﬁcally engaged into slower,
suprasecond scales while the former would be crucial for retain-
ing information in the subsecond range. In the present study, the
somatosensory response to the tactile rhythm is compatible with
activity predominantly originating from S1, which might thus
explain the relative lack of temporal integration at longer time-
scales and associated reduced ability to move to the beat com-
pared with the auditory modality.
Multisensory redundancy in rhythm processing:
somatosensation as a special case?
When parameters of rhythmic stimuli are tuned to match the
sensitivity of the sensory modality, acoustic and visual rhythms
have been reported to elicit comparable synchronization perfor-
mances (Su and Pöppel, 2012 ; Gan et al., 2015 ). As shown here,
this is not the case for tactile rhythmic stimuli. In other words,
there seems to be a greater similarity in rhythm processing
between the auditory and visual modalities, as compared with
the somatosensory modality. This di ﬀerence could be partially
explained by the fact that both audition and vision share the
property of being possibly stimulated by external inputs from a
large distance from the body and from a remote region of the
peripersonal space ( Macaluso and Maravita, 2010 ; Canzoneri
et al., 2012 ). The auditory and visual modalities are thus more
likely stimulated concomitantly by a single external source of
rhythmic inputs, particularly when positioned at distance from
the body, leading to higher probability for redundancy between
the auditory and visual modalities in processing rhythmic inputs.
In contrast, the somatosensory modality requires closer prox-
imity with the stimuli for humans to perceive them. In addition,
and in contrast to audition and vision, somatosensation and asso-
ciated functions (such as body perception and ownership) are sup-
ported by several a ﬀerent subsystems (tactile, proprioceptive,
interoceptive, vestibular; de Haan and Dijkerman, 2020 )w h o s e
integration might thus be key to elicit higher-level perceptual expe-
rience such as the beat. Beat perception related to tactile input
could also be in ﬂuenced by the body part where the sensations
are perceived. The ribcage—a location often reported as being sen-
sitive to vibrations induced by sound (Merchel and Altinsoy, 2014)
—could represent an ecologically valid alternative to the ﬁngers
stimulated here yet coming with concurrent auditory activation
through bone conduction. Relatedly, it could be speculated that
loud low-frequency sounds and concomitantly produced vibra-
tions could constitute a functionally relevant input to this multien-
try system (Hove et al., 2020; Cameron et al., 2022). Future research
is also needed to clarify how individual experience (long-term
music practice or deafness) might tune the somatosensory system
toward multiscale temporal integration.
References
Ahn S, Kim K, Jun SC (2016) Steady-state somatosensory evoked potential for
brain-computer interface —present and future. Front Hum Neurosci 9:
716.
Allison T, McCarthy G, Wood CC, Darcey TM, Spencer DD, Williamson PD
(1989) Human cortical potentials evoked by stimulation of the median
nerve. I. Cytoarchitectonic areas generating short-latency activity.
J Neurophysiol 62:694 –710.
Ammirante P, Patel AD, Russo FA (2016) Synchronizing to auditory and tac-
tile metronomes: a test of the auditory-motor enhancement hypothesis.
Psychon Bull Rev 23:1882 –1890.
Arnal LH, Doelling KB, Poeppel D (2015a) Delta-beta coupled oscillations
underlie temporal prediction accuracy. Cereb Cortex 25:3077 –3085.
Arnal LH, Poeppel D, Giraud AL (2015b) Temporal coding in the auditory
cortex. Handb Clin Neurol 129:85 –98.
Bensmaia SJ (2008) Tactile intensity and population codes. Behav Brain Res
190:165–173.
Berens P (2009) Circstat: a MATLAB toolbox for circular statistics. J Stat
Softw 31:1–21.
Bouwer FL, Honing H (2015) Temporal attending and prediction in ﬂuence
the perception of metrical rhythm: evidence from reaction times and
ERPs. Front Psychol 6:1094.
Bouwer FL, Burgoyne JA, Odijk D, Honing H, Grahn JA (2018) What makes a
rhythm complex? the in ﬂuence of musical training and accent type on
beat perception. PLoS One 13:e0190322.
Brochard R, Touzalin P, Després O, Dufour A (2008) Evidence of beat percep-
tion via purely tactile stimulation. Brain Res 1223:59 –64.
Butler M (2006) Unlocking the groove: rhythm, meter, and musical design in
electronic dance music ( Iyer V ed ), Ed 2, pp 76. Bloomington: Indiana
University Press.
Câmara GS, Danielsen A (2018) Groove. In: The Oxford handbook of critical
concepts in music theory (Rehding A, Rings S, eds), pp 271 –294. Oxford
University Press (online edn).
Cameron DJ, Dotov D, Flaten E, Bosnyak D, Hove MJ, Trainor LJ (2022)
Undetectable very-low frequency sound increases dancing at a live con-
cert. Curr Biol 32:R1222 –R1223.
Canzoneri E, Magosso E, Serino A (2012) Dynamic sounds capture the
boundaries of peripersonal space representation in humans. PLoS One
7:e44306.
Chen JL, Penhune VB, Zatorre RJ (2008) Moving on time: brain network for
auditory-motor synchronization is modulated by rhythm complexity and
musical training. J Cogn Neurosci 20:226 –239.
Cirelli LK, Spinelli C, Nozaradan S, Trainor LJ (2016) Measuring neural
entrainment to beat and meter in infants: effects of music background.
Front Neurosci 10:229.
Corniani G, Saal HP (2020) Tactile innervation densities across the whole
body. J Neurophysiol 124:1229 –1240.
Cruccu G, Aminoff MJ, Curio G, Guerit JM, Kakigi R, Mauguiere F, Rossini
PM, Treede RD, Garcia-Larrea L (2008) Recommendations for the clinical
use of somatosensory-evoked potentials. Clin Neurophysiol 119:1705 –
1719.
de Haan EHF, Dijkerman HC (2020) Somatosensation in the brain: a theoret-
ical re-evaluation and a new model. Trends Cogn Sci 24:529 –541.
Dobie RA, Van Hemel SB (2005) Hearing loss: determining eligibility for social
security beneﬁts. Washington, DC: The National Academies Press.
Doelling KB, Arnal LH, Ghitza O, Poeppel D (2014) Acoustic landmarks
drive delta-theta oscillations to enable speech comprehension by facilitat-
ing perceptual parsing. Neuroimage 85:761 –768.
Gan L, Huang Y, Zhou L, Qian C, Wu X (2015) Synchronization to a bounc-
ing ball with a realistic motion trajectory. Sci Rep 5:11974.
Geal-Dor M, Sohmer H (2021) How is the cochlea activated in response to soft
tissue auditory stimulation in the occluded ear? Audiol Res 11:335–341.
Gilmore SA, Russo FA (2021) Neural and behavioral evidence for vibrotactile
beat perception and bimodal enhancement. J Cogn Neurosci 33:635 –650.
Grahn JA, Brett M (2007) Rhythm and beat perception in motor areas of the
brain. J Cogn Neurosci 19:893 –906.
Hagen S, Lochy A, Jacques C, Maillard L, Colnat-Coulbois S, Jonas J, Rossion B
(2021) Dissociated face- and word-selective intracerebral responses in the
human ventral occipito-temporal cortex. Brain Struct Funct 226:3031–3049.
Harris JA, Miniussi C, Harris IM, Diamond ME (2002) Transient storage of a
tactile memory trace in primary somatosensory cortex. J Neurosci 22:
8720–8725.
Hove MJ, Spivey MJ, Krumhansl CL (2010) Compatibility of motion facili-
tates visuomotor synchronization. J Exp Psychol Hum Percept Perform
36:1525–1534.
Hove MJ, Iversen JR, Zhang A, Repp BH (2013) Synchronization with com-
peting visual and auditory rhythms: bouncing ball meets metronome.
Psychol Res 77:388 –398.
Hove MJ, Martinez SA, Stupacher J (2020) Feel the bass: music presented to
tactile and auditory modalities increases aesthetic appreciation and body
movement. J Exp Psychol Gen 149:1137 –1147.
Hyvarinen A, Oja E (2000) Independent component analysis: algorithms and
applications. Neural Netw 13:411 –430.
Johansson RS, Vallbo AB (1979) Tactile sensibility in the human hand: rela-
tive and absolute densities of four types of mechanoreceptive units in gla-
brous skin. J Physiol (Lond) 286:283 –300.
12  J. Neurosci., November 12, 2025  45(46):e0664252025 Lenoir et al.
 Periodized Response to Acoustic versus Tactile Rhythm
Jonas J, Jacques C, Liu-Shuang J, Brissart H, Colnat-Coulbois S, Maillard L,
Rossion B (2016) A face-selective ventral occipito-temporal map of the
human brain with intracerebral potentials. Proc Natl Acad Sci U S A
113:E4088–E4097.
Lakatos P, Shah AS, Knuth KH, Ulbert I, Karmos G, Schroeder CE (2005) An
oscillatory hierarchy controlling neuronal excitability and stimulus pro-
cessing in the auditory cortex. J Neurophysiol 94:1904 –1911.
Lakatos P, Barczak A, Neymotin SA, McGinnis T, Ross D, Javitt DC,
O’Connell MN (2016) Global dynamics of selective attention and its
lapses in primary auditory cortex. Nat Neurosci 19:1707 –1717.
Large EW, Snyder JS (2009) Pulse and meter as neural resonance. Ann N Y
Acad Sci 1169:46 –57.
Lenc T, Keller PE, Varlet M, Nozaradan S (2018) Neural tracking of the musi-
cal beat is enhanced by low-frequency sounds. Proc Natl Acad Sci U S A
115:8221–8226.
Lenc T, Keller PE, Varlet M, Nozaradan S (2020) Neural and behavioral evi-
dence for frequency-selective context effects in rhythm processing in
humans. Cereb Cortex Commun 1:1 –15.
Lenc T, Merchant H, Keller PE, Honing H, Varlet M, Nozaradan S (2021)
Mapping between sound, brain and behaviour: four-level framework for
understanding rhythm processing in humans and non-human primates.
Phil Trans R Soc Lond Ser B Biol Sci 376:20200325.
Lenc T, Peter V, Hooper C, Keller PE, Burnham D, Nozaradan S (2023)
Infants show enhanced neural responses to musical meter frequencies
beyond low-level features. Dev Sci 26:e13353.
Lenc T, Lenoir C, Keller PE, Polak R, Mulders D, Nozaradan S (2025)
Measuring self-similarity in empirical signals to understand musical
beat perception. Eur J Neurosci 61:e16637.
Liu-Shuang J, Norcia AM, Rossion B (2014) An objective index of individual
face discrimination in the right occipito-temporal cortex by means of fast
periodic oddball stimulation. Neuropsychologia 52:57 –72.
Lochy A, Jacques C, Maillard L, Colnat-Coulbois S, Rossion B, Jonas J (2018)
Selective visual representation of letters and words in the left ventral
occipito-temporal cortex with intracerebral recordings. Proc Natl Acad
Sci U S A 115:E7595 –E7604.
London J (2012) Hearing in time: psychological aspects of musical meter . New
York: Oxford University Press.
London J, Polak R, Jacoby N (2017) Rhythm histograms and musical meter: a
corpus study of Malian percussion music. Psychon Bull Rev 24:474 –480.
Macaluso E, Maravita A (2010) The representation of space near the body
through touch and vision. Neuropsychologia 48:782 –795.
Mahajan Y, Peter V, Sharma M (2017) Effect of EEG referencing methods on
auditory mismatch negativity. Front Neurosci 11:560.
Manning F, Schutz M (2013) “Moving to the beat ” improves timing percep-
tion. Psychon Bull Rev 20:1133 –1139.
Meddis R (1986) Simulation of mechanical to neural transduction in the audi-
tory receptor. J Acoust Soc Am 79:702 –711.
Meinhold W, Nieves-Vazquez HA, Ueda J (2022) Prediction of single trial
somatosensory evoked potentials from mechanical stimulation intensity.
IEEE Int Conf Rehabil Robot 2022:1 –6.
Merchel S, Altinsoy M (2014) The in ﬂuence of vibrations on musical experi-
ence. J Audio Eng Soc 62:220 –234.
Merchel S, Altinsoy ME (2018) Auditory-Tactile experience of music. In:
Musical haptics (Papetti S, Saitis C, eds), pp 123 –148. Cham: Springer
International Publishing.
Moungou A, Thonnard JL, Mouraux A (2016) EEG frequency tagging to
explore the cortical activity related to the tactile exploration of natural tex-
tures. Sci Rep 6:20738.
Mouraux A, Iannetti GD (2009) Nociceptivelaser-evoked brain potentials do not
reﬂect nociceptive-speciﬁc neural activity. J Neurophysiol 101:3258–3269.
Mouraux A, Iannetti GD, Colon E, Nozaradan S, Legrain V, Plaghki L (2011)
Nociceptive steady-state evoked potentials elicited by rapid periodic ther-
mal stimulation of cutaneous nociceptors. J Neurosci 31:6079 –6087.
Muniak MA, Ray S, Hsiao SS, Dammann JF, Bensmaia SJ (2007) The neural cod-
ing of stimulus intensity: linking the population response of mechanorecep-
tive afferents with psychophysical behavior. J Neurosci 27:11687–11699.
Norman-Haignere SV, et al. (2022) Multiscale temporal integration organizes
hierarchical computation in human auditory cortex. Nat Hum Behav 6:
455–469.
Nozaradan S, Peretz I, Missal M, Mouraux A (2011) Tagging the neuronal
entrainment to beat and meter. J Neurosci 31:10234 –10240.
Nozaradan S, Peretz I, Mouraux A (2012) Selective neuronal entrainment to the
beat and meter embedded in a musical rhythm. J Neurosci 32:17572–17581.
Nozaradan S, Zerouali Y, Peretz I, Mouraux A (2015) Capturing with EEG the
neural entrainment and coupling underlying sensorimotor synchroniza-
tion to the beat. Cereb Cortex 25:736 –747.
Nozaradan S, Peretz I, Keller PE (2016a) Individual differences in rhythmic
cortical entrainment correlate with predictive behavior in sensorimotor
synchronization. Sci Rep 6:20612 –20612.
Nozaradan S, Schönwiesner M, Caron-Desrochers L, Lehmann A (2016b)
Enhanced brainstem and cortical encoding of sound during synchronized
movement. Neuroimage 142:231 –240.
Nozaradan S, Mouraux A, Jonas J, Colnat-Coulbois S, Rossion B, Maillard L
(2017a) Intracerebral evidence of rhythm transform in the human audi-
tory cortex. Brain Struct Funct 222:2389 –2404.
Nozaradan S, Schwartze M, Obermeier C, Kotz SA (2017b) Speciﬁc contribu-
tions of basal ganglia and cerebellum to the neural tracking of rhythm.
Cortex 95:156–168.
Nozaradan S, Keller PE, Rossion B, Mouraux A (2018) EEG frequency-
tagging and input-output comparison in rhythm perception. Brain
Topogr 31:153–160.
Numminen J, Schürmann M, Hiltunen J, Joensuu R, Jousmäki V, Koskinen
SK, Salmelin R, Hari R (2004) Cortical activation during a spatiotemporal
tactile comparison task. Neuroimage 22:815 –821.
Pantev C, Hoke M, Lehnertz K, Lütkenhöner B, Anogianakis G, Wittkowski
W (1988) Tonotopic organization of the human auditory cortex revealed
by transient auditory evoked magnetic ﬁelds. Electroencephalogr Clin
Neurophysiol 69:160–170.
Patel AD (2024) Beat-based dancing to music has evolutionary foundations in
advanced vocal learning. BMC Neurosci 25:65.
Patel AD, Iversen JR (2014) The evolutionary neuroscience of musical beat
perception: the action simulation for auditory prediction (ASAP) hypoth-
esis. Front Syst Neurosci 8:57.
Patel AD, Iversen JR, Chen Y, Repp BH (2005) The in ﬂuence of metricality
and modality on synchronization with a beat. Exp Brain Res 163:226 –
238.
Patterson RD, Holdsworth JL (1996) A functional model of neural
activity patterns and auditory images. Adv Speech Hear Lang Process 3:
547–563.
Picton TW (2011) Human auditory evoked potentials. San Diego: Plural Pub.
Povel D-J, Essens P (1985) Perception of temporal patterns. Music Percept 2:
411–440.
Rahman MS, Barnes KA, Crommett LE, Tommerdahl M, Yau JM (2020)
Auditory and tactile frequency representations are co-embedded in
modality-deﬁned cortical sensory systems. Neuroimage 215:116837.
Repp BH, Penel A (2004) Rhythmic movement is attracted more strongly to
auditory than to visual rhythms. Psychol Res 68:252 –270.
Retter TL, Rossion B (2016) Uncovering the neural magnitude and spatio-
temporal dynamics of natural image categorization in a fast visual stream.
Neuropsychologia 91:9–
28.
Reybrouck M, Podlipniak P, Welch D (2019) Music and noise: same or differ-
ent? What our body tells US. Front Psychol 10:1153.
Rosenblum M, Pikovsky A, Kurths J, Schäfer C, Tass PA (2001) Chapter 9
phase synchronization: from theory to data analysis. In: Handbook of bio-
logical physics (Moss F, Gielen S, eds), pp 279 –321. Amsterdam:
North-Holland.
Ross B, Draganova R, Picton TW, Pantev C (2003) Frequency speci ﬁcity of
40-Hz auditory steady-state responses. Hear Res 186:57 –68.
Rouder JN, Morey RD, Verhagen J, Swagman AR, Wagenmakers E-J (2017)
Bayesian analysis of factorial designs. Psychol Methods 22:304 –321.
Sauvé SA, Bolt ELW, Nozaradan S, Zendel BR (2022) Aging effects on neural
processing of rhythm and meter. Front Aging Neurosci 14:848608.
Schroeder CE, Lakatos P (2009) Low-frequency neuronal oscillations as
instruments of sensory selection. Trends Neurosci 32:9 –18.
Schurmann M, Caetano G, Hlushchuk Y, Jousmaki V, Hari R (2006) Touch
activates human auditory cortex. Neuroimage 30:1325 –1331.
Sifuentes-Ortega R, Lenc T, Nozaradan S, Peigneux P (2022) Partially pre-
served processing of musical rhythms in REM but Not in NREM sleep.
Cereb Cortex 32:1508 –1519.
Skoe E, Kraus N (2010) Auditory brain stem response to complex sounds: a
tutorial. Ear Hear 31:302 –324.
Slaney M (1998) Auditory toolbox (version 2). interval research corporation.
Tech Rep Navtradevcen 010:1 –52.
Somervail R, Bufacchi RJ, Salvatori C, Neary-Zajiczek L, Guo Y, Novembre G,
Iannetti GD (2021) Brain responses to surprising stimulus offsets:
phenomenology and functional signiﬁcance. Cereb Cortex 32:2231–2244.
Lenoir et al.  Periodized Response to Acoustic versus Tactile Rhythm J. Neurosci., November 12, 2025  45(46):e0664252025  13
Su Y-H, Pöppel E (2012) Body movement enhances the extraction of tempo-
ral structures in auditory sequences. Psychol Res 76:373 –382.
Tal I, Large EW, Rabinovitch E, Wei Y, Schroeder CE, Poeppel D, Zion
Golumbic E (2017) Neural entrainment to the beat: the “missing-pulse”
phenomenon. J Neurosci 37:6331 –6341.
Tan A, Hu L, Tu Y, Chen R, Hung YS, Zhang Z (2016) N1 magnitude of audi-
tory evoked potentials and spontaneous functional connectivity between
bilateral Heschl’s gyrus are coupled at interindividual level. Brain Connect
6:496–504.
Teng X, Tian X, Poeppel D (2016) Testing multi-scale processing in the audi-
tory system. Sci Rep 6:34390.
Teng X, Tian X, Doelling K, Poeppel D (2018) Theta band oscillations re ﬂect
more than entrainment: behavioral and neural evidence demonstrates an
active chunking process. Eur J Neurosci 48:2770 –2782.
Tobimatsu S, Zhang YM, Kato M (1999) Steady-state vibration somatosen-
sory evoked potentials: physiological characteristics and tuning function.
Clin Neurophysiol 110:1953 –1958.
Tranchant P, Shiell MM, Giordano M, Nadeau A, Peretz I, Zatorre RJ (2017)
Feeling the beat: bouncing synchronization to vibrotactile music in hear-
ing and early deaf people. Front Neurosci 11:507.
Vallbo AB, Johansson RS (1984) Properties of cutaneous mechanoreceptors
in the human hand related to touch sensation. Hum Neurobiol 3:3 –14.
van den Bergh D, et al. (2020) A tutorial on conducting and interpreting a
Bayesian ANOVA in JASP. L ’Année Psychologique 120:73 –96.
Vlaar MP, van der Helm FCT, Schouten AC (2015) Frequency domain char-
acterization of the somatosensory steady state response in electroenceph-
alography. IFAC-PapersOnLine 48:1391 –1396.
Volfart A, Jonas J, Maillard L, Colnat-Coulbois S, Rossion B (2020)
Neurophysiological evidence for crossmodal (face-name) person-identity
representation in the human left ventral temporal cortex. PLoS Biol 18:
e3000659.
Witek MAG (2017) Filling in: syncopation, pleasure and distributed embodi-
ment in groove. Music Anal 36:138 –160.
Wunderlich JL, Cone-Wesson BK (2001) Effects of stimulus frequency
and complexity on the mismatch negativity and other components
of the cortical auditory-evoked potential. J Acoust Soc Am 109:1526 –
1537.
Zatorre RJ, Chen JL, Penhune VB (2007) When the brain plays music:
auditory-motor interactions in music perception and production. Nat
Rev Neurosci 8:547 –558.
14  J. Neurosci., November 12, 2025  45(46):e0664252025 Lenoir et al.
 Periodized Response to Acoustic versus Tactile Rhythm
