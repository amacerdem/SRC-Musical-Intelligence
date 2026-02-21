# survey-of-temporal-coding-of-sensory-information

fncom-19-1571109 June 28, 2025 Time: 19:3 # 1
TYPE Hypothesis and Theory
PUBLISHED 02 July 2025
DOI 10.3389/fncom.2025.1571109
OPEN ACCESS
EDITED BY
Mohammad Amin Kamaleddin,
University of Toronto, Canada
REVIEWED BY
Ehud Ahissar,
Weizmann Institute of Science, Israel
Tony Lindeberg,
KTH Royal Institute of Technology, Sweden
*CORRESPONDENCE
Peter Cariani
cariani@mac.com
RECEIVED 04 February 2025
ACCEPTED 04 June 2025
PUBLISHED 02 July 2025
CITATION
Cariani P and Baker JM (2025) Survey
of temporal coding of sensory information.
Front. Comput. Neurosci. 19:1571109.
doi: 10.3389/fncom.2025.1571109
COPYRIGHT
© 2025 Cariani and Baker. This is an
open-access article distributed under the
terms of the Creative Commons Attribution
License (CC BY). The use, distribution or
reproduction in other forums is permitted,
provided the original author(s) and the
copyright owner(s) are credited and that the
original publication in this journal is cited, in
accordance with accepted academic
practice. No use, distribution or reproduction
is permitted which does not comply with
these terms.
Survey of temporal coding of
sensory information
Peter Cariani1,2* and Janet M. Baker3
1Hearing Research Center, Boston University, Boston, MA, United States, 2Harvard Medical School,
Boston, MA, United States, 3Massachusetts Institute of Technology, Cambridge, MA, United States
Here we present evidence for the ubiquity of ﬁne spike timing and temporal
coding broadly observed across sensory systems and widely conserved
across diverse phyla, spanning invertebrates and vertebrates. A taxonomy
of basic neural coding types includes channel activation patterns, temporal
patterns of spikes, and patterns of spike latencies. Various examples and
types of combination temporal-channel codes are discussed, including
ﬁring sequence codes. Multiplexing of temporal codes and mixed channel-
temporal codes are considered. Neurophysiological and perceptual evidence
for temporal coding in many sensory modalities is surveyed: audition,
mechanoreception, electroreception, vision, gustation, olfaction, cutaneous
senses, proprioception, and the vestibular sense. Precise phase-locked, phase-
triggered, and spike latency codes can be found in many sensory systems.
Temporal resolutions on millisecond and submillisecond scales are common.
General correlation-based representations and operations are discussed. In
almost every modality, there is some role for temporal coding, often in surprising
places, such as color vision and taste. More investigations into temporal coding
are well-warranted.
KEYWORDS
multiplexing, phase-locking, neural coding, sensory coding, spike latency, perception
1 Introduction
“If everyone else is looking down, look up or in a diﬀerent direction. You will be
surprised at what you will ﬁnd.” Grote Reber, inscription at Green Bank Observatory, West
Virginia.
“Look where I am pointing, don’t bite my ﬁnger.” Warren McCulloch (Papert, 1965).
This is a survey of temporal codes with pointers to evidence for them in sensory
systems. Evidence for temporal coding of sensory distinctions can be found in nearly every
sensory modality. This paper surveys this body of evidence and attempts to bring it together
into a systematic, uniﬁed theoretical perspective. Temporal codes may well turn out to be
as fundamental as rate-based channel codes.
First, the paper takes up the problem of neural coding and outlines basic types
of temporal codes. The second half of the paper presents an overview of some of the
neurophysiological and psychological evidence that supports various possible roles for
temporal codes in major sensory modalities, updating and expanding three previous papers
on the subject (Cariani, 1995, 2001b; Cariani, 2004).
Frontiers in Computational Neuroscience 01 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 2
Cariani and Baker 10.3389/fncom.2025.1571109
2 The neural coding problem
Arguably, the speciﬁc nature of neural coding in the brain is
the most fundamental unsolved problem in neuroscience because
it determines how we think about neural systems, both natural
and artiﬁcial. The neural coding problem entails identifying which
speciﬁc aspects of neural activity convey those informational
distinctions on which brain functions depend (Uttal, 1972; Gerstner
et al., 1997; Rieke et al., 1997; Gerstner, 1999). How do collections
of spike trains at diﬀerent brain loci encode the various types of
information that brains handle?
Despite enormous advances, because we have yet to solve the
neural coding problem for most brain subsystems, neuroscience
is still in a phase similar to biology before the elucidation of
the genetic code. Without knowledge of the basic signals of the
system, what aspects of neural activity subserve what functions,
it is diﬃcult to understand how brains work in terms of speciﬁc
neurocompuational mechanisms, let alone how their informational
functions go awry or how such dysfunctions can be remedied.
There are two main approaches to neural coding. Neural
coding can be approached from a purely mathematical, Shannonian
information-theoretic perspective (how much information is
conveyed through some set of alternative signals through a
speciﬁed transmission channel, (MacKay and McCulloch, 1952;
Borst and Theunissen, 1999; Dimitrov et al., 2011) or from a
function-based perspective (what is the relation of a set of signals
to the informational functions of a system).
The information-theoretic approach often avoids speciﬁc
considerations of function, relying instead on general assumptions
involving optimally eﬃcient coding (Barlow, 1961; Barlow, 1995)
or optimal use of potentially available information by central
processors (MacKay and McCulloch, 1952; Siebert, 1970; Heinz
et al., 2001). Using such empirical and theoretical optimal use
estimates, informational capacities of temporal codies often exceed
those for rate-channel codes by an order of magnitude or more.
On its face, the eﬃcient coding principle does not comport with
neural populations that typically have high average spontaneous
ﬁring rates (e.g., >50 spikes/s), such as auditory and vestibular
nerves. Although the optimum central processor assumption is
useful in ruling out prospective codes that have insuﬃcient
informational capacity to account for perceptual acuities, once
adequacy has been established, higher transmission rates (e.g.,
MacKay and McCulloch, 1952) do not a priori favor one code
over another. This is because we often do not know what are the
primary operational measures, e.g., precision, accuracy, robustness,
reliability, fail-safe, damage-resistance/survivability, for which a
central processor might be optimized, as well as structural and
developmental constraints on its biological realization. When there
exists a surfeit of informational capacity, it is also relatively easy to
pool information in order to achieve higher levels of robustness and
reliability at the expense of high precision and accuracy.
In contrast, the function-based conception of neural coding
focuses on functional meaning in seeking to ﬁnd pervasive
correspondences with perception and behavior. Instead of
optimality of informational eﬃciency, in order to operate in a
robust manner in wide ranges of noisy and unpredictable contexts,
a good deal of redundancy and suboptimal pooling of information
is perhaps to be expected. Optimality of predictive accuracy under
a wide range of unpredictable and novel conditions is distinct from
eﬃcient neural coding.
In the spirit of Gregory Bateson (“The diﬀerence that makes
a diﬀerence”), distinctions are diﬀerences that make a diﬀerence
in terms of internal functional states and consequent behaviors.
In the functional view, the framework adopted here, the neural
coding problem involves identifying those systematic diﬀerences in
neural activity that subserve functional diﬀerences. Neural coding
is thus the problem of reverse-engineering the functional, “signals
of the system.”
The neural coding problem concerns both relations of stimuli
to neural activity (“encoding”, in what forms information available
to the system may take) and relations of neural activity to
behavior (“decoding, ” how the system uses this information to eﬀect
appropriate behaviors)(Shimazaki, 2025).
For several reasons this paper focuses on temporal coding of
sensory distinctions, i.e., how “sensory information” is encoded, as
opposed to those codes that support central neural representations
(e.g., in cognition, emotion, motivation, memory traces, and motor
programs). First, the speciﬁc nature of neural coding of speciﬁc
basic sensory and perceptual attributes is generally much better
understood than those codes involved in more central functional
states. Part of this is because sensory neural states and their
associated individual attributes tend to be simpler and more easily
identiﬁed than their more complex, multi-attribute and multi-
modal cognitive representations.
Whereas neural response patterns at stations near sensory
surfaces are mainly driven by external stimuli and hence
are more easily correlated with both stimulus structure and
associated perceptual attributes, more central distinctions can
involve other brain systems whose neural responses are contingent
on past history and current motivational, emotional, cognitive,
and mnemonic states. Second, large numbers of discriminable
stimulus states means that coding schemes can be tested with
high precision, and some assessment can be made of the
adequacy of a candidate code in accounting for perceptual acuities.
When experiments rely on 1-bit detections or discriminations
between or recognitions of small sets of stimuli, it can be
diﬃcult to determine whether some speciﬁc code or another
is being used by the brain for that task. Third, perceptual
invariances in which diﬀerent stimuli and stimulus conditions
evoke the same perceptual attributes aﬀord a means of testing
how well the general behavior of a particular neural code or
representation resembles that of the perceptual system it is
presumed to serve.
Neural candidate codes are those putative coding schemes
which cannot be ruled out of hand and for which there exist
plausible correlations with observed (here, sensory) functions.
Deﬁnitive establishment of a code requires positive demonstration
of a causal (in addition to a correlative) relationship between so-
coded neural states and speciﬁc sensory distinctions (Mountcastle,
1988; Mountcastle, 1993; Cariani, 1995, 1999; Jazayeri and Afraz,
2017; Panzeri et al., 2017).
Neuropsychological models that successfully predict perceptual
judgments for speciﬁc stimuli on the basis of observed or
biologically-realistic simulated neural responses can provide
positive demonstration that some speciﬁed code is used by some
nervous system for some particular functional end. Electrical
stimulation that produces speciﬁc patterns of neural activity and
Frontiers in Computational Neuroscience 02 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 3
Cariani and Baker 10.3389/fncom.2025.1571109
evoked percepts consistent with neural coding hypotheses provide
additional powerful evidence for those neural codes. Appropriately
temporally patterned electrical stimulation has been found to
produce percepts related to ﬂutter-vibration, auditory pitch and
speech perception (via cochlear implants), color, taste, and pain.
More recently, optical stimulation has been used in a similar
manner to test coding hypotheses, e.g., (Chong et al., 2020;
Bagur et al., 2025).
Although we are generally skeptical of automatic assumptions
of optimal eﬃciencies and ideal observers, information-theoretic
models are quite useful in ruling out candidate codes if they ﬁnd
that a prospective code lacks enough informational capacity to
account for the acuity or robustness of some perceptual capability
(Jacobs et al., 2009). These analyses can also be quite useful
in engineering contexts by suggesting new alternative coding
schemes that can yield superior precision, robustness, information
capacity, and eﬃciency in artiﬁcial devices (section “13 Design of
artiﬁcial systems”).
3 Temporal codes
3.1 What are temporal codes?
Temporal codes are those neural codes in which information
is carried by timings of receptor activations (Rucci et al., 2018).
Temporal codes are based on temporal patterns of neuronal
spiking responses rather than on which speciﬁc neurons or
neuronal populations are diﬀerentially activated (“channel” or
“rate-place” codes). Whereas temporal codes rely on temporal
relations between spikes, channel codes rely on activation proﬁles
amongst selective, tuned receptive elements. In the footsteps of
Johannes Mueller’s theory of speciﬁc nerve energies, channel coding
assumes that the particular neurons that “respond”, i.e., are most
excited in some way, encode the sensory quality that is perceived.
Following Helmholtz and Adrian, channel coding, speciﬁcally
rate-place coding, has been the dominant, default assumption
in neuroscience.
However, temporal coding has always constituted an alternative
to rate-place coding, with an early lineage in acoustics and auditory
theory. In the 19th century it runs from Seeboeck’s siren to
Rutherford’s “telephone theory” of audition, in the 20th it begins
with the temporal spike pattern theories of pitch of Troland
(1930) and Wever (1949) (Wever and Bray, 1937; Boring, 1942;
de Cheveigné, 2005). Notably, inspired by radio heterodyning,
Troland also proposed a temporal, “nerve current modulation”
theory of color (Troland, 1921, 1930), p. 200–202) in which
temporal patterns related to color would be multiplexed with those
encoding other visual attributes. Subsequent auditory models of
Jeﬀress (1948) and Licklider (1951a) 1959 combined temporal and
channel-coding principles. Interest in the function-oriented neural
coding problem has waxed and waned since, with peaks in the
1960’s (Mountcastle, 1967; Perkell and Bullock, 1968; Perkell, 1970),
early 1970’s (Uttal, 1972; Uttal, 1973), and the 1990’s (Wasserman,
1992; Carr, 1993b; Cariani, 1995; Covey et al., 1995; Theunissen
and Miller, 1995; Rieke et al., 1997; Lestienne, 1999; Cariani, 2001b;
Panzeri et al., 2009).
The temporal patterns that form the basis for temporal
codes can exist at the levels of spike trains of single neurons,
ensembles, subpopulations, or whole populations. The temporal
patterns can involve diﬀerences of characteristic time intervals
between spikes, as in interspike interval codes (e.g., 10 vs. 11 ms
intervals in auditory nerve ﬁbers), or in spike arrival times (e.g.,
relative sub-millisecond diﬀerences in spike latencies in auditory
and electroreceptive localizations). Temporal resolutions that
support sensory discriminations can range from sub-millisecond
timescales, as in electroreception and auditory pitch perception,
localization, and echolocation, to much longer timescales that
involve the encoding of longer durations associated with event
timings (Tucci et al., 2014; Akdogan et al., 2023; Howard, 2024).
The patterns can be simple, encoding a one-dimensional attribute,
(one or another interspike interval or relative latency) or complex,
encoding two or more attribute dimensions, (e.g., a series of
intervals, or multiplexed, interleaved intervals, or speciﬁc multi-
neuron volley patterns).
As with rate-channel codes, temporal codes can be dense
or sparse depending on what fraction of neurons are producing
temporally-coded patterns of spikes that are related to some
speciﬁc attribute (Kloppenburg and Nawrot, 2014). Temporal
codes can also be dense or sparse in time, depending on what
fractions of time contain spikes participating in a particular code.
Temporal codes that are sparse in time facilitate multiplexed,
interleaving of independent spike patterns. Temporal codes
at the levels of neural ensembles and populations can also
consist of temporal patterns whose spikes are distributed across
multiple neurons.
3.2 A taxonomy of neural codes
Taxonomies of diﬀerent basic types of neural codes have been
outlined and discussed in previous papers (Cariani, 1995; Cariani,
1999; Cariani, 2001b; Cariani, 2004). There are many ways to send
a message using arrays of channels each of which sends its own
train of pulses. A relatively economical taxonomy (Figure 1) divides
neural codes into channel codes, temporal pattern codes, and spike
latency codes. These are related to three independent aspects of any
signal: the channel over which it is sent, its internal structure (e.g.,
waveform), and its time-of-arrival.
Channel codes are those codes in which the respective identities
of the channels are crucial to the meaning of the message. The
channels are “labeled lines” such that if the labels are scrambled, so
is the message. Temporal pattern codes are those codes in which
messages are conveyed through diﬀerent temporal patternings
of spikes rather than through which particular channels are
involved, such that they do not require channel-speciﬁc labels
or connectivities. Spike latency codes are those codes in which
the absolute timing of spikes relative to some reference time
conveys messages.
The time-of-arrival (latency) of a signal is independent of
its internal structure (temporal pattern). Two signals arriving at
slightly diﬀerent times (relative latencies) can provide information
concerning the direction and range of objects in various modalities
(e.g., in binaural, somatic, olfactory localization; echolocation; and
electroreception). Following an onset of a response to an event
Frontiers in Computational Neuroscience 03 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 4
Cariani and Baker 10.3389/fncom.2025.1571109
FIGURE 1
A taxonomy of types of basic temporal codes. Sensory distinctions are conveyed through which neurons respond (channel codes), how they
respond with different temporal patterns of spikes (temporal pattern codes) and when they respond (spike latency codes). Combination codes that
use two or more types of response attributes lie on the edges. Multiple parallel, semi-independent codes for the same attribute lie in the center.
in one neural population, various other neural populations may
respond with characteristic delays, such that recurrent volleys of
spikes arriving at a given time after the onset response can indicate
that a particular population sensitive to a particular attribute
has been activated (e.g., later peaks in event-related-potentials
associated with diﬀerent stages of speech and language processing).
The relative latency of the incoming volley can thus indicate the
presence or absence of a speciﬁc feature.
3.2.1 Types of codes reﬂect universal neural
response properties
This tripartite distinction arises from near-universal properties
of neurons as simple integrate-to-threshold elements that are
driven by depolarizing input currents. These are:
(1) monotonically increasing average ﬁring rates with increased
excitatory depolarizing synaptic currents,
(2) phase-locking, i.e., spiking preferentially at times when
synaptic input currents increase or ﬂuctuate, and
(3) earlier ﬁring with increased synaptic currents, i.e., the ﬁrst spike
will be produced earlier with increasing input magnitude
The three properties related to excitation lead, respectively,
to rate-channel codes, phase-locked temporal pattern codes, and
spike latency codes (Figure 1). At the vertices of the triangle are
“pure” codes based on one response property (channel, temporal
pattern, timing), whereas at its edges are joint combination codes in
which two properties jointly determine a response pattern (which
temporal patterns or spike latencies in which channels), and in the
center are multiple independent codes (e.g., parallel coding using
multiple populations).
All three pure types of coding are possible whenever neural
inputs are excitatory, so it isn’t surprising when multiple types of
candidate codes are found in the same systems (as can be seen
in the auditory nerve, Figure 2). It then falls to neuroscientists to
determine which codes the system is actually using to realize its
various functions.
In addition, many neurons have characteristic recovery
times from transient, hyperpolarizing, inhibitory inputs in
which the latency of the ﬁrst spike after a hyperpolarizing
pulse is monotonically related to its magnitude (“anode break
excitation”). The timing of the second spike can be quite precise.
Thus an additional general mechanism that produces spike
timing precisions in sensory systems is rebound spike timing
from inhibition.
(4) rebound from inhibition
If a neuron is driven by an early excitatory wave of inputs
closely followed by an inhibitory one, then an onset triggered
spike can be followed by a second, precisely-timed anode-break
spike to produce a characteristic interspike interval related to the
Frontiers in Computational Neuroscience 04 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 5
Cariani and Baker 10.3389/fncom.2025.1571109
FIGURE 2
Temporal coding of pitch and timbre in the auditory nerve. Top(A) Stimulus waveform: Synthetic single-formant vowel, F0 = 80 Hz, F1 = 640 Hz,
60 dB SPL, 100×, Felis catus, dial anesthesia. (B) Post-stimulus time neurogram of 51 auditory nerve ﬁbers (ANFs). (C) Stimulus line spectrum.
(D) Average ﬁring rates vs. characteristic frequencies. (E) Stimulus autocorrelation function (ACF). 1/F0 = 12.5 ms = pitch period.
1/F1 = 1.6 ms = period of formant harmonic. (F) Population-interval distribution (PID), a.k.a. “summary autocorrelation,” the sum of all-order interval
distributions of all 51 individual ANFs, i.e., discarding all cochlear place (CF) information. Arrows indicate peaks related to pitch periods and to the
formant frequency. Bottom: Pitch and timbre phenomena predicted by the locations of major peaks in PIDs compiled from spike trains recorded
from 50 to 100 ANFs, on the order of 100,000 spikes/plot. First plots: Waveform, line spectrum, and ACF for an AM tone (fc = 640 Hz, fm = 160 Hz)
that produces a strong low pitch at its 160 Hz “missing fundamental.” Last plots: PIDs of synthetic two-formant vowels, showing characteristic
distributions of short intervals (0–5 ms). See (Cariani, 1999) for additional details.
magnitude of the onset transient. This mechanism can support
a non-phase locked interval code for the intensity transients: the
longer the recovery time from inhibition, the higher the intensity
of the transient.
3.2.2 More complex response properties
Of course, many neuronal types can have internal dynamics
that are more complex than simple integrate-and-ﬁre neurons,
and these can give rise to characteristic spike burst and interburst
patterns as well as single spike recovery times. Local networks of
neurons, especially if they contain both excitatory and inhibitory
elements, as in retinas and olfactory bulbs (Shepherd, 1990),
can produce stimulus-triggered characteristic spiking patterns
that need not be phase-locked to the stimulus in order to
encode diﬀerent stimulus attributes. Electrical conditioning of
single neurons with slow temporal patterns of non-electrical
stimulation can cause “assimilation of the rhythm” wherein
the neurons produce the conditioned pattern when they ﬁre
(Morrell, 1967; Thatcher and John, 1977). Oscillations are temporal
spiking patterns that can be produced both by single neurons
and local networks (Kopell et al., 2010a). Stimulus-triggered
oscillations in characteristic frequency bands can be found
throughout the brain (Ba¸ sar, 1992; Bullock, 1992; Buzsáki, 2006)
and potentially play essential functional roles in neural coding
(Shamir et al., 2009; Kopell et al., 2010b; Cariani and Baker, 2022;
Mignot et al., 2024).
Frontiers in Computational Neuroscience 05 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 6
Cariani and Baker 10.3389/fncom.2025.1571109
In many cases, electrical stimulation using recorded stimulus-
triggered temporal patterns can evoke the corresponding percept.
Examples of these types of temporal stimulation and response
patterns are illustrated in Figure 3 for gustation (Covey, 1980;
Di Lorenzo et al., 2009) and color vision (Festinger et al., 1971;
Young, 1977).
3.3 Channel-based codes
Temporal codes can be contrasted with channel codes in which
diﬀerent across-neuron patterns of activations convey distinctions.
For most of the history of neuroscience, following Helmholtz
(Helmholtz, 1885) and Adrian (Adrian, 1928), channel-coding
FIGURE 3
Temporal coding in visual and gustatory systems. (A) Responses of a single lateral geniculate neuron of an anesthetized macaque to constant
velocity drifting sinusoidal gratings. These correspond to temporal modulations of luminance of 16 and 32 Hz. Aligned period histograms and
all-order interspike interval distributions were compiled from 1233 spikes, 5897 intervals (16 Hz) and 495 spikes, 1102 intervals (32 Hz), showing
strong phase-locking to luminance modulations. Rate-based spatial frequency (temporal modulation) tuning curve (mean ± s.d.). Estimates of the
two temporal modulation frequencies 8 and 16 Hz made by ﬁnding the delay associated with the peak in the interval distributions had errors of 0.5
and 2%, respectively. Raw spike train data were provided courtesy of Przybyszewski et al. (2000). (B) Monochromatic ﬂicker stimuli that produce
subjective colors, the Prevost-Fechner-Benham Effect (Cohen and Gordon, 1949). Left: Rotating disk patterns that were used to study
ﬂicker-induced colors top to bottom, by Fechner, Helmholtz, Helmholtz, and Benham. Right. Glow tube monochromatic luminance patterns that
produce the corresponding colors (Festinger et al., 1971). Electrical stimulation using the same temporal patterns produce the same colored
phosphenes (Young, 1977). (C) Typical intrinsic whole-nerve chorda tympani temporal response patterns of different tastant classes in decerebrate
rats. The tastants were HCl (0.1M, sour), sucrose (0.5M, sweet), NaCl (0.1M, salty), and quinine (0.1M, bitter). From Covey (1980).
Frontiers in Computational Neuroscience 06 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 7
Cariani and Baker 10.3389/fncom.2025.1571109
has been the dominant, default assumption for conveying speciﬁc
informational contents in sensation and perception, cognition,
executive functions, emotion, memory, and motoric action.
Channel-coded neural representations are described as vectors in
which each dimension is associated with a speciﬁc neuron (or
ensemble or population) and its scalar value with some measure
of activation level.
The simplest channel codes are so-called “doorbell codes”
in which excitation of highly selective neurons indicates the
presence of one particular stimulus, such as a pheromone (one
stimulus/neuron). More common candidate channel codes are
referred to as “rate-place codes, ” in which diﬀerent levels of
activation are signiﬁed by diﬀerent average ﬁring rates, i.e., spike
counts averaged over tens to hundreds or more milliseconds, or
spiking probabilities, i.e., the probability of a spike occurring within
a given temporal window. A ﬁring rate proﬁle of a collection of
elements with diﬀerent selectivities can convey the relative presence
of a range of attributes.
A test of whether a given prospective neural code is a
channel code is to scramble channel identities/labels and to
determine whether this operation changes the functional meaning
of the pattern. In spatially-organized maps (e.g., cochleotopic,
retinotopic, somatotopic maps) the identity of an individual
neuron (which channel, which dimension in the vector) is
signiﬁed by its spatial “place” in the map). However, spatial
organization is not absolutely required, such that neurons spatially
dispersed within a population can be organized by their common
tunings. Here, “place” can refer to an element’s connectivity
position within a neural network (nervous system, brain, region,
population, ensemble).
Firing rates are not the only means of indicating channel
activations. Other biologically-plausible measures include relative
ﬁrst spike latency (the faster the response, the higher the
activation) and relative ﬁring order (earlier responders indicate
units with higher activations, subsequent responders indicate
lower activations).
3.4 Temporal pattern codes
Temporal pattern codes encode distinctions by means of
characteristic temporal patterns of spikes, i.e., how neurons
respond. In the sensory context, speciﬁc temporal patterns are
produced by speciﬁc stimulus attributes. Temporal patterning can
arise in two ways, through phase-locking to a stimulus or through
stimulus-triggered response patterns.
3.4.1 Phase-locked temporal pattern coding
What is “phase-locking”? In neuroscience, the term phase-
locking is used in several diﬀerent, though related, contexts.
Phase-locking can refer to time-locking of spikes to an external
stimulus (stimulus-locking). Unless otherwise noted, this is the
sense the term will be used in this paper in discussing sensory
coding. Most simply put, phase-locking here means that spike
timings are signiﬁcantly correlated with the waveform of the
incoming stimulus. In order to be phase-locked, spikes must occur
predominantly during one phase of a stimulating waveform, usually
either its positive or negative phase. They can be, but need not be,
“entrained” to the stimulus, i.e., one or more spikes produced for
each stimulus phase.
Phase-locking can also refer to temporal correlations between
neural activations at the levels of individual neurons, ensembles,
and whole populations. At the neuron level, these are correlations
between spike timings or ﬁring rate ﬂuctuations. At the ensemble
level, they may involve measures of multi-unit activity. At the
population level, they involve measures of the collective behavior
of the population, such as local ﬁeld potentials and gross potentials.
Interneural synchronies at any of these levels can involve spiking
and collective events that occur simultaneously (zero-lag) or
with some constant temporal oﬀset (lead or lag). Neural-neural
phase-locking on population-wide scales can involve temporally
correlated brain rhythms and oscillations, be they exogenous
(stimulus-locked), endogenous, triggered, or induced.
Phase-locking to motoric actions and their internal
representations constitutes yet another application of the general
concept. Muscle activations produce corollary discharges as well
as muscle and body movements that themselves produce spike
patterns in stretch receptors and proprioceptive aﬀerents. These are
phase-locked to the movements, especially onsets. These provide
both rate and temporal readouts of movements that can be used
in active sensing systems to improve tactile, haptic, and visual
perception (section “3.9 Temporal coding in active sensing”).
In these systems, on the encoding end, spike timing patterns in
primary sensory neurons are determined both by the structure of
the external stimulus and that of internally-generated movements
of sensory surfaces. On the decoding end, neural phase-locked loop
(PLL) mechanisms have been proposed to take into account the
temporal modulations induced by the movements so as to recover
the structure of the external stimulus (Ahissar et al., 2023).
Given the basic response properties of neurons, phase-locking
in these abovementioned senses is an almost inevitable, universal
process. Whenever depolarizing input synaptic currents from a
receptor or another neuron to a neuron ﬂuctuate, neurons ﬁre
preferentially when these currents are positive. The spikes are time-
locked to the positive phases (positive amplitude portions of the
waveform), i.e., they “phase-lock.” In the absence of signiﬁcant
currents, neurons may ﬁre stochastically, e.g., exhibiting Poisson-
like “spontaneous activity.” In most receptor systems, receptors
produce positive synaptic currents only when cilia are deﬂected
in one direction, such that alternating motions (e.g., vibrations,
aperiodic ﬂuctuations) produce half-wave rectiﬁed voltage and
current waveforms. As a consequence, spike timings are correlated
with the stimulus waveform as it has been ﬁltered through its
passage through sensory organs and receptors.
If sensory neurons phase-lock to the stimuli that excite them,
then the time structure of the stimulus waveform is impressed
on that of the produced spike trains. This in turn means
that any attributes closely associated with the time structure
of the stimulus waveform will have correlates in the resulting
patterns of spikes. This includes auditory and visual event onsets
and durations, event rhythmic patterns (musical rhythm, speech
prosodic rhythms), periodicity (auditory pitch, ﬂutter-vibration,
visual ﬂicker frequency), spectrum (auditory vowel quality, spectral
tilt/timbral brightness), onset dynamics (musical attack), and
modulation spectrum (consonantal distinctions, infrapitch). If a
feature is in the waveform, and within the frequency range of phase-
locking, it will have a phase-locked temporal pattern correlate in
Frontiers in Computational Neuroscience 07 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 8
Cariani and Baker 10.3389/fncom.2025.1571109
response spike trains. More succinctly, “if it’s in the waveform,
it’s in the spikes” somewhere, provided that there is at least some
phase-locking in the system.
Phase-locking eﬀectively encodes the time structure of periodic,
near-periodic, and aperiodic stimuli, and does not depend on
any particular waveform type (sinusoid, impulse, square wave,
noise), but it is limited in the frequencies it can track by the
low-pass ﬁltering imposed by sensory organs and receptors and
jitter introduced by synaptic transmission. In mammalian cochleae,
ﬁltering successively reduces the AC components of high frequency
pure tones, rolling oﬀ at a few thousand Hz, with synaptic
jitters on the order of 100 microseconds. The two factors reduce
usable phase-locking of mammalian auditory primary neurons to
somewhere between ∼3–8 kHz, depending on species (there is
debate about the upper limit in humans). In barn owls, phase-
locking exists up to ∼10 kHz (Koppl, 1997). Weakly electric ﬁsh
have special adaptations (electroreceptors, gap junction synapses,
coincidence detectors with many input lines) that reduce jitter,
enabling them to detect and produce electric signals with sub-
microsecond precisions (Carr et al., 1986; Heiligenberg, 1991; Carr,
1993b; Heiligenberg, 1994).
Phase-locking is found in nearly every sensory system, with
spiking patterns of many sensory neurons mainly reﬂecting the
ﬁne structure of the impinging stimulus itself (e.g., vibrations). In
active sensing systems there is also phase-locking to movements
of the animal and its sensory surfaces, such that spiking patterns
also reﬂect the temporal structure of those movements [e.g., gross
and ﬁne eye movements (Rucci et al., 2018), whisker movements,
sniﬃng cycles, bodily accelerations]. Temporal spiking patterns
related to the timings of movements can be used to separate
out those patterns that reﬂect properties of external objects from
those that reﬂect movements (see section “3.9 Temporal coding in
active sensing”).
In everyday life, very few stimuli, if any, are completely static.
In the case of vision, the eyes are in intermittent saccadic motions
and constant micro-motions such that the retina is constantly
producing short-time representations of images in the form of
spatial patterns of phase-locked spikes. When images are stabilized
on the retina, presumably phase-locking is abolished such that
neurons revert to Poisson-like spiking, and form perception rapidly
disappears (Ditchburn and Ginsborg, 1952; Coppola and Purves,
1996). This is highly suggestive that visual form perception critically
depends on phase-locking. See also discussion in section “9.1
Form vision.”
Phase-locked time structure is largely preserved when auditory
waveforms and visual images are inﬁnitely-peak-clipped, i.e.,
reducing waveforms and images to binary amplitudes (below
average values are set to 0, above-average values to 1). Remarkably,
speech intelligibility of inﬁnite-peak-clipped sounds is little aﬀected
(Licklider, 1951b) and images remain quite recognizable. Patterns
of acoustic discontinuities and visual contrasts (edges), not graded
amplitudes, are most important for perception of auditory qualities
and visual form. Phase-locking is arguably the simplest and
most eﬀective means of encoding patterns of temporal and
spatial edges.
Interspike interval codes are the simplest temporal pattern
codes. First-order interval codes consist of distributions of time
intervals between consecutive spikes, whereas all-order interval
codes instead count intervals between consecutive and non-
consecutive spikes. All-order distributions are equivalent to the
autocorrelation functions of spike trains. Interval sequences, such
as triplet codes consisting of sequences of two intervals (Lestienne,
1996; Lestienne and Tuckwell, 1998), can be described in terms
of triple autocorrelations (Yellott and Iverson, 1992). Longer
interval sequences can be described in terms of still higher order
autocorrelations (Victor and Conte, 1996).
Phase-locked interval codes can also indicate stimulus intensity
in the degree to which the activity of a population exhibits a
common time pattern. In the auditory nerve, the proportion of
spikes that are phase-locked vs. those “spontaneous” spikes that
occur at random phases increases monotonically with sound level
and its perceptual correlate, loudness (one expects an analogous
situation for contrast and phase-locking in retinal elements).
As a consequence, peak-to-mean ratios in population-interval
autocorrelation distributions at the level of the auditory nerve are
indicators of ratios of driven, correlated, phase-locked responses to
uncorrelated, spontaneous activity (Figure 2).
3.4.2 Stimulus-triggered temporal pattern coding
In addition to phase-locked temporal response patterns,
speciﬁc stimuli can trigger diﬀerent endogenous response patterns
in neurons. These characteristic responses need not have any
necessary correlation with the stimulus time structure beyond
the universal event-attributes of event onset, oﬀset, and duration.
Examples include temporal coding of taste and color (Figure 3)
that are further discussed in sections “9 Vision” and “10 Chemical
senses: gustation and olfaction.” Characteristic response patterns
can also come in the form of bursting patterns (burst length
and/or interburst intervals) and intrinsic oscillations of diﬀerent
frequencies or combinations of frequencies.
3.4.3 Spike correlation codes
Whereas the simplest temporal patterns can be interspike
intervals produced through phase-locking to periodic stimuli or
produced by triggered oscillations, more complex, speciﬁc patterns
of spikes in the form of spike volley codes or spike correlation codes
are also possible, e.g., (Fetz, 1997). Such correlation codes would
also encompass volley patterns consisting of sets of characteristic
spike latencies, making them varieties of spike latency coding. If the
volley patterns are independent of channel identities, then they are
purely temporal codes. If channel identities matter, then they are
combination channel-temporal pattern or channel-latency codes in
the taxonomy.
3.5 Spike latency codes
Spike latency codes rely on speciﬁc timings of spikes relative
to some internal reference time. First-spike latency codes can
encode the intensity of a stimulus onset or amplitude transient
with high fraction-of-a-millisecond precisions (Phillips, 1993;
Heil, 1997; Heil, 2004), which can be compared with coarser
estimates using information-theoretic counting window duration
methods (Kayser et al., 2010). Remarkably, ﬁrst spike jitters
for onsets at auditory cortical stations can be comparable
to those in primary auditory neurons, due presumably to
Frontiers in Computational Neuroscience 08 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 9
Cariani and Baker 10.3389/fncom.2025.1571109
repeated processing by neurons performing coincidence detection
operations on many independent inputs – jitter is preserved
or reduced by virtue of the Central Limit Theorem. Shorter
response latencies of individual neurons and narrower temporal
dispersions of spikes indicate higher change of amplitude
(contrast). Here the internal reference time may be the timing of
some threshold of onset-correlated spiking across a population.
In the retina, ﬁrst spike latencies can encode contrast, i.e.,
edges and contours (Gollisch and Meister, 2008; Gutig et al.,
2013). Ensemble- and population-wide oscillations can also serve
as reference times, with oscillatory phase oﬀsets (time delays,
relative latencies) encoding diﬀerent stimulus attributes in olfaction
and other modalities (Hopﬁeld, 1995; Masquelier et al., 2009).
Such phase-oﬀsets are widely observed in the hippocampal
coding of diﬀerent locations (places) in maze navigation tasks
(Skaggs et al., 1996).
Diﬀerent subpopulations of neurons can have diﬀerent
characteristic response times, such that peaks with diﬀerent
latencies in population-wide responses can indicate the degrees to
which diﬀerent subpopulations are activated. Some early theories
of color, noting the diﬀerent latencies of peaks in averaged
evoked responses to diﬀerent wavelengths of light, postulated
mechanisms of this sort.
Joint channel-temporal codes combine temporal patterns
and/or latencies with labeled lines. For example, in the auditory
nerve the appearance of interspike intervals associated with
a common frequency component across many channels can
encode the relative amplitude of that component relative to
others. A particular set of interspike intervals or burst patterns
appearing in some speciﬁc characteristic frequency channel, such
as those associated with some modulation frequency or event-onset
rhythms, can constitute an auditory interval-place representation
(Voigt et al., 1982). Similarly, relative spike latency can replace
ﬁring rate as an indicator of which channels are most highly
activated. Here the channel(s) with the shortest response latencies
serve as the best estimates of attribute values. Because average
ﬁring rates and shortest spike latencies often occur together, the
two codes can be diﬃcult to disambiguate as to which are causal
to function.
In phase-locked sensory systems, various localization functions
can be achieved by comparing the relative arrival times of similar
waveforms at diﬀerent body (receptor) surfaces, i.e., diﬀerent
channels. This strategy is seen for localization attributes in
many diﬀerent modalities: electroreception, audition, somatic,
olfaction, and gustation. In binocular vision, interocular delays
are interpreted as depth cues, as the Pulfrich Eﬀect illusion
suggests (Graham, 1966; Carr, 1993b). Perhaps the most widely
appreciated example is binaural localization in the horizontal
plane. For example, in human binaural localization diﬀerent
directions of sound sources in the horizontal plane produce
diﬀerences of sound arrival times between the two ears that
range up to roughly 500 microseconds. Due to phase-locking,
these time diﬀerences are faithfully preserved in spike trains of
the two auditory nerves, and through highly secure synapses
in those of spike trains produced by neurons in the anterior
cochlear nucleus. In eﬀect, a neural temporal cross-correlation
function is computed using delay lines and binaural coincidence
neurons in the auditory brainstem (Jeﬀress, 1948; Cariani, 2011).
The interaural delay channel in the binaural array that has
the highest number of coincidences, i.e., the highest ﬁring rate,
indicates the interaural delay and hence the direction in the
horizontal plane.
3.6 Firing sequence codes
Related to spike latency codes are ﬁring sequence codes in
which the temporal order of responses in diﬀerent channels
encodes some stimulus attribute. This is a joint channel-
time code by virtue of the necessity of labeling the channels,
but one in which the temporal dimension has ordinal values
rather than metrical ones Such codes have been proposed for
vision in light of experiments that strongly suggested short
neural processing windows for form vision (Thorpe, 1990;
Coppola and Purves, 1996).
A primary advantage of such codes is that they only require
one spike per channel, permitting rapid coding of images within
very short time windows (Van Rullen and Thorpe, 2001; Van Rullen
et al., 2005). The one-spike-per-neuron feature ameliorates the
many problems posed by the movement of the image relative to the
retina for computing spike rates over longer time windows of 50 ms
or more. To avoid confusion, note that the “interspike interval”
(“ISI”) code in Van Rullen and Thorpe (2001) is a mean interspike
interval measure, i.e., an alternative way of computing spike rate,
rather than a temporal code, as we use the concept here. Such ﬁring
sequence codes are also relatively insensitive to image degradations
(Delorme and Thorpe, 2001).
Order of ﬁring codes also potentially solve what is known as
the Hyperacuity Problem (Thorpe et al., 2004; Altes, 1989). Many
rate-place codes are plagued by this problem, where the acuity
of perceptual systems, as evidenced in controlled psychophysical
experiments and behavioral observations, is over an order of
magnitude ﬁner than the rate receptive ﬁelds of the most
selective neurons in the corresponding primary sensory neurons
(Rieke et al., 1997).
However, it is also often overlooked that phase-locked temporal
codes (pattern or latency) often have precisions that are orders
of magnitude better than their ﬁring rate counterparts that lead
to predictions of much smaller Weber fractions, e.g., in the
auditory nerve (Siebert, 1968; Heinz et al., 2001). Once spike
timing information enters the picture, this “hyperacuity problem”
goes away. Temporal coding also can solve analogous hyperacuity
problems in other systems, such as in visual representations of
space (Rucci et al., 2018), vernier actuity (Assa et al., 2025), and
haptic localization of objects using vibrissal systems (Knutsen et al.,
2006) Other mixed-time-place codes that use spatial patterns of
synchronous, phase-locked, temporally correlated spikes could also
operate on one-spike-per-channel constraints [cf. spike correlation
codes of Jacobs et al. (2009) and some temporal encoding
assumptions in Ahissar and Arieli (2012)].
On the belief that such synchronies are redundant with
respect to retinal rate-place proﬁles and sub-optimally reduce
rate-contrasts across neighboring receptive ﬁelds, some
workers eliminated synchronized spikes from consideration
(“decorrelation”) in attempts to improve rate-place codes
(Kuang et al., 2012). If one did this in the auditory nerve (Figure 2),
there would be almost nothing left.
Frontiers in Computational Neuroscience 09 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 10
Cariani and Baker 10.3389/fncom.2025.1571109
Firing sequence codes are perhaps best conceptualized in
terms of synﬁre chains (Abeles, 2009) in which spike timings and
interneural delays cause chains of coincidence elements to ﬁre.
Diﬀerent ﬁring orders activate diﬀerent sets of synﬁre chains. But
it is diﬃcult to imagine how visual images or auditory scenes or
olfactory mixtures could be robustly constructed from ensembles
of ﬁring sequences. How well do these representations fare in terms
of perceptual invariances (e.g., similar triangles of diﬀerent colors,
contrasts, positions, sizes)? How do they fare in terms of common
percepts in the face of other changing attributes? For example,
F0-pitches of musical notes are highly invariant with respect to
sound level, direction, attack, instrument timbre – one can play
the same note a bit louder, move around, play staccato or legato
notes, or even change instruments and the pitch remains the same.
But, because neurons are typically weakly sensitive to multiple
parameters, these manipulations will certainly change many ﬁring
orders of neurons in the auditory pathway.
The particular synﬁre chains that are activated by particular
stimulus conditions are intimately tied to particular channels
and transmission paths. Consequently, they encounter many
of the diﬃculties of rate-place and feature-detector-based
representations. Sequence codes have the merit of being invariant
under some time scale transformations, but the number of
alternative chains is quite high, making the dimensionality
of representations based on them many orders of magnitude
higher than the structure of their corresponding percepts and
perceptual scenes.
Dynamical system trajectories can be regarded in terms of ﬁring
times and sequences within whole neural populations. Their phase
spaces can consist of time-channel matrix of spike timings that
may have many of the same aforementioned diﬃculties as simpler
ﬁring sequences. For the sake of parsimony, some principle needs
to produce natural equivalence classes amongst the astronomical
number of trajectories observed within the phase space that map
easily to mental states and behaviors.
To our knowledge, no completely comprehensive theory of
the full space of possible spike codes has yet been proposed that
encompasses all of the codes discussed above as well as still others
yet to be proposed. We believe that such a synthesis is possible
and would be useful. Perhaps (Victor and Purpura, 1996) comes
closest. Such a systematic space would need to cover metrical
and non-metrical pattern codes, ordinal codes, combination codes,
sequence codes, as well as moments of distributions of coded
variables (e.g., means, variances, skewnesses, kurtoses of interval
or ﬁring rate distributions) and trajectories through dynamical
systems phase spaces (Mazor and Laurent, 2005). This is not to
mention high dimensional, often inscrutable, codes derived from
deep learning and convolutional neural networks (Mathis et al.,
2024). The expectation is that biological systems have found much
more elegant, simpler solutions.
3.7 Coding transformations and parallel
codes
Temporal and channel codes are not mutually exclusive
(Masuda and Aihara, 2007). They can exist at diﬀerent stages of
sensory pathways, with coding transformations occurring from
peripheral to central stations. The transformations can convert
temporal patterns to rate-place channel patterns, as in time-delay
neural networks. Central neural phase-locked loops were originally
proposed as mechanisms for converting spike latency-channel
representations to rate-channel representations (Ahissar, 1998;
Ahissar et al., 2000). Rate-place patterns can also be transformed to
temporal patterns, as in spike latency volley pattern codes, mixed
latency-place codes, order-of-ﬁring channel codes, and central
pattern generators. Evidence for rate-place coding at one stage in
sensory pathways does not rule out its conversion to some sort of
temporal code, e.g., spike latency or ﬁring order, at higher levels.
Temporal and channel codes can also exist as parallel, partially
redundant coding systems. For example, in thermoreception,
diﬀerent neural subpopulations are thought to respond to hot
and cold stimuli [section “11 Cutaneous sensations (pain, itch,
temperature)”]. High acuities may be achieved using temporally-
coded information and active-sensing central mechanisms, whereas
lower acuities may be found when sensory systems are forced to
rely solely on less precise spatial, channel-based codes (Gamzu and
Ahissar, 2001; Ahissar and Arieli, 2012).
Often ﬁrst spike latencies and ﬁring rates are highly correlated
making it diﬃcult to disambiguate which aspect of response spike
trains is causal to function. Finally, there can be joint, combination
temporal and spatial, channel proﬁle codes (Figure 1) in which
temporal patterns or relative spike latencies/ﬁring orders mark
which channels are most activated. Here temporal markers play
the role of ﬁring rates in diﬀerentiating channel activation patterns.
Two examples are a putative interval-channel code in the auditory
system (Voigt et al., 1982) and latency-place codes for somatic
localizations (von Békésy, 1967).
3.8 Multiplexing of temporally-coded
signals in the same channels
Contrary to what might have been expected 75 years ago, most
neurons in the brain have turned out to be not highly selective,
unitary feature detectors. The dogma of one feature-one neuron has
gradually eroded away, except in very specialized sensory domains.
Many cortical neurons respond to stimuli in multiple modalities
[e.g., visual and tactile information (Bieler et al., 2017)]. Even
cortical neurons within a single modality respond to changes in
multiple perceptual attributes within that modality, e.g., (Bizley and
Walker, 2010). It is hard to see how individual features get sorted
out at the cortical level. Neurons in supramodal areas often may
respond to multiple objects having diﬀerent sets of multi-modal
perceptual, cognitive, emotional, motivational, and action-related
attributes. The ubiquity of multi-valent “mixed selectivity” neurons
poses deep problems for theoretical neuroscience (Fusi et al., 2016).
It is possible that complex, central, multiplexed temporal codes
could solve some of these problems (Cariani and Baker, 2022;
Baker and Cariani, 2025).
A prime advantage of codes that do not require labeled lines
and consequently, highly speciﬁc connectivities and transmission
paths is that these coding schemes “liberate the signals from the
wires”, thereby enabling broadcast and selective reception strategies
for information integration (Cariani and Baker, 2022; Baker and
Cariani, 2025). Another advantage of temporal codes is that they
lend themselves to multiplexing of signals, i.e., multiple types of
pulse coded information can be sent along the same axonal lines
Frontiers in Computational Neuroscience 10 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 11
Cariani and Baker 10.3389/fncom.2025.1571109
at the same time. Multiplexing also relaxes the strict transmission
path constraints that channel codes appear to require. One spike
train can thereby convey “multiple meanings” (Chung et al., 1970;
Chung et al., 1974; Wasserman, 1992; Cariani, 2004).
In sensory systems the diﬀerent signals can be related to
diﬀerent independent attributes of a single object, event, situation
or body location. An example would be multiplexed coding
of the various cutaneous senses, such as vibration, pain, itch,
temperature, and pressure (Emmers, 1981; Woo et al., 2022). On
the motor side, diﬀerent multiplexed signals enable a single neuron
to independently control diﬀerent muscles (Bittner, 1968). Along
these lines, diﬀerential ﬁltering of temporal patterns of action
potentials at axonal branchpoints could provide an intraneural
mechanism for demultiplexing spike trains into independent
components (Raymond and Lettvin, 1978; Pratt, 1990).
Multiplexing in the time domain also potentially simpliﬁes
problems of scene analysis (perceptual organization, segmentation
and binding of attributes of multiple objects). Time-division,
frequency-division, code-division, and oscillatory phase
multiplexing of spike train signals are diﬀerent strategies for solving
these problems. More complex, multiplexed, multimodality, and
multiscale central codes, including temporally-organized “packets”
(Luczak et al., 2015) are also possible. We have discussed many
of these alternatives in greater depth elsewhere (Cariani, 2004;
Cariani and Baker, 2022; Baker and Cariani, 2025).
Many temporal codes are relatively sparse in time and
therefore only minimally interfere with one another. Some
temporal codes permit interleaving of spike patterns, whereas
for other interval codes interleaved spikes may alter the
encoded meanings of the pulse train signals. For example,
all-order interval codes are impervious to added or subtracted
spikes. These codes consist of time intervals between pairs of
both consecutive and non-consecutive spikes. Distributions
of all-order intervals are equivalent to autocorrelations of
spike trains (section “6.1 Basic auditory qualities”). The
neural code for pitch at the level of the auditory nerve
appears to be based on such autocorrelation-like interval
codes (section “6 Audition, ” Figure 2). In contrast, adding
or subtracting spikes for ﬁrst-order interspike interval codes,
i.e., intervals between only consecutive spikes, will change the
encodings and therefore the functional meanings of the spike
train messages.
Multiplexing in the time domain also potentially simpliﬁes
problems of scene analysis (perceptual organization, segmentation
and binding of attributes of multiple objects). Arguably some
means of multiplexing signals is needed for integrating (binding)
many diﬀerent types of information in cognitive representations
and memory traces of objects, events, situations, and internal
procedures. When multiple objects drive overlapping channels
(frequency channels in audition, spatial channels in vision)
temporal correlation structure can be used to separate them
(Cariani, 2004).
3.9 Temporal coding in active sensing
Active sensing involves use of bodily actions to reveal to the
senses the structure of objects and events in the environment.
A simple example is to sense the properties of an irregular
or smooth surface by running one’s ﬁnger over it. Here both
stimulus structure (surface characteristics) and movements of
sensory surfaces (what speed and pressure are used) determine
temporal spiking patterns in primary mechanoceptive neurons.
General theories of perception can be classiﬁed according
by their assumptions regarding the relation of incoming sensory
information to internal (cognitive, motivational, mnemonic, and
motoric) states (see (Ahissar et al., 2015) for a taxonomy of theories
from the active sensing perspective). Sensory systems that mainly
rely on bottom-up, environmentally determined information ﬂows
from sensory surfaces (e.g., auditory systems) are labeled “passive
mechanisms”, whereas those that function using both bottom-
up ﬂows and deliberate, self-generated actions (e.g., vibrissal
systems) are labeled “active mechanisms.” Modalities in which
active sensing plays critical roles can be seen as “closed-loop
convergence processes” (Saig et al., 2012; Ahissar and Assa, 2016) in
which “action-dependent perceptual invariances” can be achieved.
In this paper, our sense of “sensory coding” concerns what
information is available in peripheral spike activity patterns,
irrespective of whether they are produced by external stimuli
(objects, events) or self-generated motions. Both passive and active
sensing modalities depend on temporal coding in the form of
spatial and temporal patterns of spike timings.
In order to gain information about the surface, neural response
patterns related to the surface properties and not to the bodily
movement need to be separated. Central neural mechanisms
that demodulate (“decode”) the stimulus-movement mixture are
therefore needed. Feedback mechanisms in the form of neural
phase-locked loops have been proposed by Ahissar and co-
workers to carry out this role of taking into account the
contributions of bodily movements so as to recover stimulus
attributes (Ahissar et al., 2023).
Early on characteristic intrinsic low-frequency oscillatory
activity was discovered by Ahissar and Vaadia (1990) in
the somatosensory cortex of awake monkeys. These ﬁndings
subsequently led to models of active sensing in rat whisker systems
based on central oscillators and thalamic phase comparators. These
“compare cortical timing expectations with the actual input timing
and represent the diﬀerence by their population output rate”
(Ahissar et al., 1997).
By this proposed mechanism, diﬀerent spike latencies relative
to the timing of movements in sensory peripheries can be converted
to central ﬁring rate codes (Ahissar, 1998). Here diﬀerent whisking
phases correspond to spike timing diﬀerences, whereas whisking
frequencies correspond to time lags and interspike intervals
(instantaneous frequencies). Active coding models successfully
predict performance declines when whisking frequencies fall
outside the working frequency ranges of central oscillators
that support phase-locked loop mechanisms and latency-to-rate
conversions (Knutsen et al., 2006).
In taking account of the state of sensory organs, central
mechanisms can support perceptual invariances with respect to
actions, such as self-motions (Wallach et al., 2016) and sniﬃng
dynamics (Jordan et al., 2018). In these mechanisms, internal
induced oscillations can also support prediction and anticipation of
expected inputs on upcoming cycles with subsequent computation
of expectancy violations that can indicate changes in the
external world.
Frontiers in Computational Neuroscience 11 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 12
Cariani and Baker 10.3389/fncom.2025.1571109
4 What is encoded?
Diﬀerent sensory modalities convey diﬀerent types of
distinctions regarding the sensed-state of the body (intero-
reception) and the world external to it (extero-reception).
Intero-receptive modalities convey information related to the
bodily attributes of pain, irritation (itch), internal temperature,
digestive, circulatory, respiratory and immunological states, and
muscle fatigue, as well as body positions (proprioception, stretch
and position receptors), self-motion and orientation (vestibular).
Extero-receptive modalities in humans include auditory, visual,
tactile, vestibular, thermal, olfactory and gustatory distinctions
related respectively to patterns of external sounds, light, skin
contacts and vibrations, imposed motions, external temperature,
inhaled and ingested chemicals. Other animals also have additional
extero-receptive sense modalities such as magnetoreception
and electroreception.
Perception has strong modal structure and within it a
dimensional structure of diﬀerent attributes (Boring, 1942). Many
of the attributes of each modality have parallels with those of
other modalities, such that these parallels can be grouped into a
few categories:
1. basic sensory qualities , such as auditory pitch and timbre,
visual texture and color, taste, smell, sharp vs. dull tactile
sensations, salty vs. bitter vs sour taste, hot vs. cold, pain, and
itch, – “what sensations”?
2. intensity, such as loudness, pitch and timbral salience,
lightness (brightness), contrast, color saturation, as well as
tactile, thermal, and nocioceptive intensities – “how much”?
3. spatial forms, such as 2- and 3-D visual and tactile shapes –
“what shape, what object”?
4. temporal forms , such as auditory rhythmic patterns, and
temporal sequences (e.g., bird calls, speech streams, sequences
of changing qualities of all sorts) – “what temporal pattern of
events”?
5. directions of stimuli relative to body surfaces, such as apparent
directions of external objects and sources in visual, auditory,
olfactory, and electroreceptive spaces and apparent location of
stimuli contacting one’s body – “where”?
6. apparent distance (range) of external objects and sources in
visual, auditory, olfactory, and electroreceptive spaces, such
as is determined by visual parallax for depth perception and
auditory echolocation, as well as from prior knowledge of
object sizes and intensities as a function of distance – “how
far”?
7. apparent sizes of external objects – “how big?”
8. apparent motions of objects and sources– “how fast? where are
things headed?”
The dimensional structure coupled with common kinds of
attributes compels consideration of a neuro-phenomenological
isomorphism hypothesis vis-à-vis neural coding. Here each
modality has its own correlation structure of incoming sensory
ﬂuxes impinging on primary sensory surfaces, as well as its own
receptor types, proximal circuits, aﬀerent and eﬀerent pathways,
and thalamocortical organizations, albeit with many commonalities
across modalities.
A working hypothesis is that every independent perceptual
quality within each modality has a corresponding, independent
dimension of neural coding. The modal and dimensional structure
of perception falls out of 1) which aspects of the external world
to which receptors are sensitive, 2) the spatiotemporal correlation
structure of the incoming sensory ﬂuxes on receptor surfaces,
3) the nature of the neural codes that convey these correlation
patterns more centrally. The modal structure of perception
arises from diﬀerences in the patterns the sensory receptors
encode as well as the neural codes and processing operations
that are required for information given via that modality to
guide eﬀective action. The dimensional structure of perception
mirrors that of the correlation structures and neural codes in
each modality.
Where there are similarities between correlation structures and
neural codes, there will exist inter-modal parallels (e.g., similar
cross-correlation mechanisms for visual, auditory, and tactile
localizations (von Békésy, 1964b, 1967). In active sensing systems,
such as touch and vision, cross-modality similarities may also
arise from common central mechanisms for separating sensory
contributions of self-movements from those related to properties
of external objects (Ahissar et al., 2023).
5 Coding in speciﬁc sensory systems
In almost every sensory system there is some evidence
for the role of temporal discharge patterns for conveying
complex stimulus qualities in a host of human and animal
modalities: audition, vision, the vestibular sense, olfaction,
gustation, the cutaneous senses of mechanoreception (vibration,
pressure), nocioception (pain), thermoreception, proprioception
(body position and movement, muscle position and stretch
receptors, haptic perception), electroreception, visceral sensations,
magnetoreception, baroreception, and perhaps yet others waiting
to be discovered.
Often there is evidence for both temporal and rate-channel
coding. In such cases, the two can be diﬃcult to disambiguate,
i.e., to determine which type of information is causally related
to function. In the past, often, investigators stopped looking
for possible alternative, temporal codes once evidence for rate
coding and neuronal speciﬁcity were found. In part, this
occurred because, historically, concepts of rate codes and their
subsequent interpretations by the rest of the brain have been
more easily and universally understood, than those involving
temporal codes.
6 Audition
Audition is a general-purpose perceptual system used by
humans and animals to detect, discriminate, and recognize
sounds and to localize their sources in the external environment
so as to guide behavior. Its major functions involve hunting
prey, avoiding predators, navigation, intraspecies communications
(speech, animal vocalizations), and, in humans, self-modulation of
psychological states (music).
Frontiers in Computational Neuroscience 12 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 13
Cariani and Baker 10.3389/fncom.2025.1571109
Audition is a phase-locked sensory system par excellence. It
is a sense modality whose psychophysics and neurophysiology,
including temporal coding, have been intensively investigated. Its
literature is voluminous. Good places to start are (Schnupp et al.,
2011; Moore, 2013). [Moore, 2013, reference?]
Ubiquitous, abundant, and usable phase-locked temporal spike
patterns can be found at the ﬁrst stage of neural representation,
in the auditory nerve (Figure 2B). In humans usable spike timing
information is thought to existwhere they exist for periodicities
roughly up. Phase-locking rolls oﬀ at high frequencies, its upper
limit varying with species. In humans auditory percepts such
as octave matching and the existence region of musical tonality
(Cariani, 2019) suggest an upper limit of 4–8 kHz, depending on
the individual listener.
However, but like many other sensory systems, as one proceeds
up the pathway, spikes are more and more temporally sparse, jitters
accumulate, and spikes related to multiple kinds of information
intervene. Consequently phase-locking becomes progressively less
evident at cortical stations, where nevertheless phase-locking can
still be observed up to a few hundred Hz (Cariani, 1999; Cariani
and Micheyl, 2012), suﬃcient to cover human voice pitches,
low-frequency envelope periodicities, and event onset timings
in rhythms.
Temporal codes can be ﬁne or coarse depending on the
precision of spike timings. They can depend on timings of
individual spikes, potentially yielding submillisecond precisions, or
on temporal patterns of spike rates or spiking probabilities within
populations, with precisions in tens of milliseconds or more.
Whenever sounds are presented to the ear at moderate
to high sound levels, large swaths of the auditory nerve
phase-lock to periodicities in the acoustic stimuli, including
fundamental frequencies, individual frequency components, low
frequency envelopes of interacting components, as well as
aperiodic temporal patterns of acoustic transients and event-
onsets. Analogous phase-locked responses, albeit with diﬀerences
of frequency range and phase-locking precisions, can be found
in primary auditory neurons in mammals, birds, reptiles,
amphibians, ﬁsh, and insects. Spike timing plays a major
role in the coding of basic auditory attributes involved in
detecting, localizing, and recognizing sounds in the external
world, with humans reliably receiving speech, and listening
to music.
6.1 Basic auditory qualities
A substantial body of evidence exists for temporal
coding of basic auditory qualities of music, such as pitch,
consonance/roughness, timbre, note duration, and rhythm, and
those of speech, such as voice pitch, vowel and consonantal
distinctions, and speech rhythms.
Pitch. Pitch is a primary auditory attribute related to the
dominant repetition period (periodicity) of a periodic sound. This
is variously known as the “low” pitch at the fundamental F0, F0-
pitch, virtual pitch, and musical pitch (Cariani, 2019). It has a long
history and a rich set of precisely measured perceptual phenomena
that enable various neural coding hypotheses to be tested.
Both sinusoidal, pure tones and harmonic complexes of human
voices and tonal musical instruments produce strong pitches. The
strongest, most comprehensive, physiologically-grounded models
for both pure (Goldstein and Srulovicz, 1977; Heinz et al., 2001)
and complex tone pitches (Meddis et al., 1990; Meddis and
Hewitt, 1991; Cariani and Delgutte, 1996; Cariani, 1999) are
those that use phase-locked spike timing information in the form
of auditory nerve ﬁber (ANF) interspike interval distributions
(Figure 2). The latter models estimate the pitches that will be
heard from the most numerous all-order interspike intervals
present in the auditory nerve. This is a phase-locked temporal
pattern code. Due to phase-locking the time structure of the
neural spike trains are highly correlated with that of the stimulus.
For physiologically-resolved harmonics, spikes are phase-locked
to individual harmonics (“temporal ﬁne structure”), whereas for
pairs and groups of unresolved harmonics, spikes also phase-
lock to the lower-frequency envelopes (“modulations”) created by
beating harmonics. Interspike intervals created by phase-locking to
individual harmonics and to envelopes permit representations of
pitch for resolved and unresolved harmonics.
Because the all-order interval distributions are autocorrelations
of these spike trains, when they are added together, their
population-interval distribution (PID, 2F) resembles the stimulus
autocorrelation function (ACF , 2E), which carries the same
information as the stimulus power spectrum.
The population-wide interval distribution (PID) is therefore a
purely temporal code that does not depend on which characteristic
frequency channels produced which intervals, and as a general-
purpose neural autocorrelation-like representation, it conveys
information about both stimulus periodicity and spectrum.
As a result, the peaks in the neural PID indicate all the
periodicities in the stimulus waveform, suﬃcient to precisely
predict the dominant periodicity (the fundamental period 1/F0 and
its multiples, here 1/80 Hz = 12.5 ms) as well as other periodicities
(the period of the harmonic at the formant 1/640 Hz = 1.6 ms).
The precisions of estimates derived from a few thousand ANF spike
times produces F0-pitch estimates that have errors on the order of
half a percent in frequency, in the same ballpark as human listeners.
These models also predict a host of other pitch phenomena,
such as pitches of missing fundamentals, pitch equivalences
between stimuli with diﬀerent amplitude and phase spectra, pitch
invariance with respect to level, pitch shifts of inharmonic complex
tones, the dominance region for pitch, and spectral edge pitches
(not shown). The only pitch phenomena that are clearly not
predicted are subtle F0-pitch shifts of harmonic complexes with
one slightly mistuned individual harmonic (Dahlbom and Braasch,
2020) and not-so-subtle Zwicker pitches (Gockel and Carlyon,
2016), which are auditory afterimages that probably have a central
rather than peripheral origin.
Spectrum. Because the PID also temporally encodes spectral
information below ∼5 kHz, it also can serve as a representation
for vowel timbral space (Palmer, 1990). In so-called “double vowel”
experiments (Cariani and Delgutte, 1993), we found that we
could accurately identify single and double vowels by comparing
the correlations of neural PIDs with stimulus autocorrelations of
single-vowels (Cariani and Delgutte, 1993). The single-vowel PID
proﬁles are shown in the last plots of Figure 2 (Cariani, 1995).
Temporal coding also may explain how pitch and timbral
commonalities (e.g., diﬀerent instruments playing the same note,
the same instrument playing diﬀerent notes) can be extracted. By
simply by multiplying the summary autocorrelations of each of
Frontiers in Computational Neuroscience 13 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 14
Cariani and Baker 10.3389/fncom.2025.1571109
two conditions, their common peaks associated with either pitch
or spectrum reinforce each other (Cariani, 2001a). Time domain
representations and correlation-like processing operations can
simply auditory scene analysis, a.k.a. Gestaltist object formation,
segmentation and binding, Cherry’s “cocktail party problem”,
using the diﬀerent voice pitches of speakers to separate out
the diﬀerent voices (Cariani, 2004). Using correlations between
neural PIDs and stimulus autocorrelations and neural timing
nets, the single vowel constituents of concurrent double vowels
with the same and diﬀerent voice F0-pitches can be accurately
identiﬁed with patterns that resemble human performance
(Cariani, 2001c).
Loudness. Because the fraction of driven, correlated spiking
across the whole auditory nerve (vs. uncorrelated, spontaneous
activity) increases monotonically with sound level, degree of spike
correlation within a population is a potential neural correlate of
stimulus intensity (loudness). Here correlation index could be a
useful metric for testing this conjecture (Joris et al., 2006).
Musical tonality and rhythm. Other qualities important in
tonal music, such as octave similarity, roughness, consonance
(harmonicity, tonal fusion), musical interval ratios, and tonal
hierarchies may be explained in terms of autocorrelation-like
temporal codes based on interspike intervals (Cariani, 2019).
Here the fraction of intervals related to overlapping subharmonics
determine perceptual distances which form a tonality space (see
also (Leman and Carreras, 1997)). Although melodies are entirely
recognizable when transposed (multiplying all note F0-frequencies
by a constant ratio), this recognition breaks down for melodies
consisting of notes above ∼4 kHz, near the uppermost note on
the piano. For most listeners, octave equivalence also breaks down
at this frequency, which may be the upper limit of usable phase-
locking for within-CF-channel interval codes in most humans
(a few of whom can make octave equivalences at somewhat
higher frequencies).
Speech. Basic phonetic distinctions depend on quasi-
stationary spectral shapes in the case of vowels and transient
amplitude and frequency patterns in the case of consonants.
Vowel formant space is well represented in autocorrelation
functions and neural population-interval distributions of
the auditory nerve. Neural correlates of vowel category
boundaries of speciﬁc languages are presumably located at
higher levels of the auditory pathway. The neural coding of
consonantal distinctions, on the other hand, are much less
well understood because they involve spike patterns related
to acoustic contrasts and discontinuities (onsets, oﬀsets). This
makes them amenable to latency coding relative to population
onset responses.
Speech is highly redundant, with many diﬀerent kinds of
cues and representations, such that limited recognitions can be
achieved with reduced sets of these. Adequate, but suboptimal
levels of speech intelligibility can be achieved using information
in the modulation spectrum (Fogerty et al., 2023), i.e., low-
frequency ( <50 Hz) envelope ﬂuctuations of higher frequency
carriers (Ghitza et al., 2012). Temporal patterns related to slower
modulations are mostly the information that cochlear implant users
must rely on for consonant identiﬁcation and speech intelligibility.
Although the modulation spectrum appears suﬃcient for minimal
recognition of consonants (Chait et al., 2015; Teng et al., 2021),
reduced-channel vocoder experiments (Shamma and Lorenzi,
2013) suggest that although temporal ﬁne structure cues are more
resistant to noise, information related to either temporal ﬁne
structure or modulation envelopes can be used.
Neurons coarsely-rate-tuned to low frequency modulations of
higher frequency carriers are found throughout the auditory
pathway (Schreiner and Langner, 1988; Langner, 1992),
but a rule of thumb is that wherever there is such rate-
based modulation tuning (bandpass “modulation transfer
functions”) the neurons phase-lock to the envelope (modulation)
ﬂuctuations. The modulation spectrum also has correlates in
spike timings, and consequently in autocorrelation functions
in the form of longer time intervals ( >10–20 ms). Because
many neural subpopulations in the auditory pathway phase-
lock to these slower periodicities, there are also likely to be
temporal pattern coding correlates as well as those based
on latencies.
More centrally, oscillatory phase-locked loop mechanisms
similar to those proposed for somatosensory systems (sections
3.9 and 7) could potentially be triggered by onsets to enable
oscillatory phase-oﬀsets of spikes (spike latencies) to encode
envelopes (Ahissar et al., 2001; Ghitza, 2011).
Time-domain representations and analysis of speech
waveforms that emulate auditory phase-locked responses
have proven eﬀective. An acoustic processor for speech with
single sample temporal resolution, that directly phase-locks
to speech waveforms, demonstrated improved phonetic and
sub-phonetic detections and segmentations, based on acoustic
discontinuities (Baker et al., 1972; Baker et al., 1974; Baker, 1975).
When integrated with standard spectral features in the HEAR
acoustic processor, this time-domain processing improved test
performance of a state-of-the-art continuous natural language
speech recognition system on a standard corpus (Bahl et al., 1978;
Baker, 1979).
Interval-place (Ghitza, 1992) and purely temporal, non-place
representations (Ghitza, 1988) were explored as front-ends for
speech recognition research systems. The non-place Ensemble
Interval Histogram (EIH) representations are close to those
population-interval distributions described above for pitch, albeit
with some subtle diﬀerences that stem from their use of ﬁrst-order
rather than all-order intervals.
Rhythm. Because there are phase-locked responses to event
onsets at all levels of the auditory system, rhythms in music
(Nozaradan, 2014) and speech (Peelle and Davis, 2012; Peelle et al.,
2013) have direct phase-locked temporal pattern encodings.
This is all in keeping with the general conjecture that if it’s
in the waveform, periodic or not, it’s likely to be in the spikes.
Provided that amplitude, frequency, and phase ﬂuctuations lie
within the frequency limits of phase-locking, it is likely that
salient information will have direct correlates in the temporal
patterns of spiking.
6.2 Sound localization
Temporal coding in binaural localization and echolocation,
i.e., spatial hearing, is much more widely appreciated than its
role in representing other auditory qualities. Spatial hearing
includes estimating the direction (azimuth, altitude) of sound
Frontiers in Computational Neuroscience 14 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 15
Cariani and Baker 10.3389/fncom.2025.1571109
sources as well as their range (distance), size, and shape. It
also includes the perception of sound ﬁelds in natural and
architectural contexts such as concert halls, where time delays
associated with reverberations are important (Ando, 2009). Even
the psychophysical and neurophysiological literature addressing
timing issues for spatial hearing, including binaural localization
and bat and cetacean echolocation is rather large, but there are a
number of excellent overviews and computational models (Carr
et al., 2001; Grothe et al., 2010; Ming et al., 2021; Casseday and
Covey, 1995; Simmons et al., 2003; Simmons et al., 1993; Simmons
and Ferragamo, 1993; Durlach and Colburn, 1978; Colburn, 1996;
Simmons et al., 1996b; Ming et al., 2021).
Binaural sound localization. Humans can localize sound sources
in the horizontal plane with surprisingly high acuity. The two major
cues are interaural time diﬀerences (ITD’s) and interaural level
diﬀerences (ILD’s). When sounds propagate from some angle oﬀ
the listener’s midline, the sounds arrive at the two ears at slightly
diﬀerent times, the diﬀerence being the ITD. Maximum ITDs in
humans range from roughly 0–500 microseconds, depending on
head size, such that this cue is operant for pure tone frequencies
up to 1.5–2 kHz, above which ILD cues caused by acoustic
head shadows are more eﬀective. Lower frequency modulations
(envelopes) of higher frequency carriers can also use ITD cues. The
best jnd’s of 1–2 degrees azimuth correspond to interaural time
diﬀerences of 10–20 microseconds (Grothe et al., 2010), which are
comparable to time diﬀerences for best monaural pitch acuities
(0.1–0.2% for 1 kHz pure tones).
Classically, the Jeﬀress Model has been the mainstay of ITD-
based binaural localization computational mechanisms (Colburn,
1996; Cariani, 2011). It is a time-delay neural network consisting
of (1) phase-locked spike train inputs from corresponding
characteristic frequency regions in the two auditory nerves and
ventral cochlear nuclei, (2) axonal tapped delay lines with diﬀerent
lengths and conduction times that convey the spike trains to
(3) bipolar binaural neural coincidence detectors in the auditory
brainstem that ﬁre when spike from both left and right pathways
arrive at the same time, and (4) neural coincidence counters whose
ﬁring rates provide a rate-place proﬁle of ITDs.
Binaural localization in barn owls has been intensively studied
because of their impressive hunting skills in almost total darkness
(Grothe, 2018). They have excellent phase-locking limits (∼10 kHz)
that are about an octave above ours and neural coincidence
detectors that minimize jitter. By comparison, despite their much
smaller head size, barn owls have extremely good localization with
4 degree minimal audible angles (Krumm et al., 2019). There are
diﬀerences in binaural cross-correlation circuitries and topographic
organization of ITD maps between mammals and birds (Carr and
Konishi, 1990; Carr, 1993a; McAlpine and Grothe, 2003), such
that the bird binaural circuits better match the details of the
Jeﬀress Model than do those of mammals (Grothe, 2003; Grothe
et al., 2010). In recent decades, roles for precisely-timed inhibition
in sharpening coincidence detection have been incorporated into
binaural models in order to account for neuroanatomical and
neurophysiological diﬀerences between mammals, birds, and other
animals (Grothe et al., 2010; Ashida and Carr, 2011).
Those implementation details notwithstanding, there are
pervasive commonalities between time-delay cross-correlation
mechanisms that compute very ﬁne temporal disparities.
Across the animal kingdom analogous temporal operations
and mechanisms that measure time-of-arrival diﬀerences
exist in many diﬀerent modalities (Carr, 1993b): binaural
localization, echolocation, somatic localization, electroreception,
as well as gustatory and olfactory localization/lateralization
(von Békésy, 1964b,c; Bower, 1974; von Békésy, 1967). From
his interest in binaural and somatic localization based on
diﬀerent times-of-arrival at body locations, von Bekesy delivered
tastants to diﬀerent sides of the tongues of human subjects
who were able to discriminate temporal orders down to a
millisecond (von Békésy, 1964a,c). He carried out analogous
experiments with olfactory localizations using air puﬀs into the
two nostrils.
In binaural localization, the ridges on pinnae create spectral
notches that can serve as “pinna cues” for sound direction in
the vertical plane. Traditionally these cues have been assumed
to be coded by rate-place proﬁles, but because every spectral
feature has a corresponding time-domain correlate, these ridges
also produce low-frequency envelope modulations that in turn
produce phase-locked spike timing patterns in auditory nerves.
Thus localizations using pinna cues might also be temporally-coded
(Alves-Pinto et al., 2014).
Echolocation. Echolocation uses sounds emitted by a human
or animal and their echoes in order to determine the presence,
distance, and in some cases, shapes of external objects around them.
It is especially useful in dark environments where vision is highly
limited. The best echolocators are bats and cetaceans (Popper
and Fay, 1995; Surlykke et al., 2014; Ladegaard et al., 2019; Ming
et al., 2021) that form auditory images of the spaces and objects
around them.
For pragmatic reasons, much more is known about the
details of bat echolocation and its neuroanatomical and
neurophysiological substrates than those of cetaceans (Casseday
and Covey, 1995; Moss and Schnitzler, 1995; Covey, 2005).
Despite very diﬀerent environments and mediums, there are many
computational commonalities between them. Both systems are
capable of exploiting sub-microsecond temporal disparities.
The Spectrogram Correlation and Transformation (SCAT)
model of Simmons and co-workers can be applied to both bat and
cetacean echolocation (Simmons et al., 1996b; Ming et al., 2021).
What follows is a highly simpliﬁed summary of the signals and
signal processing computations.
Bats tend to use high frequency-swept chirps, whereas
cetaceans tend to use high-frequency pulsatile clicks. Both acoustic
bursts are very short. When a sound is emitted, if its echo copy is
heard after some time delay, then there is an object somewhere in
the direction of the sound source. The delay provides a readout of
the distance to the object that depends on the velocity of sound in
the medium (331 m/s in dry air or 1500 m/s in water).
The neural coding of both the vocalization and its echo
produces a precisely timed spike at each characteristic frequency
channel in the animal’s auditory nerve. In each channel, this
produces an interspike interval that encodes the echo-delay.
Depending on the shapes of objects, which are at diﬀerent
distances, diﬀerent frequency channels can have slightly diﬀerent
echo-delays (glints) and by comparing intervals across channels,
object variations in depth can be sensed. If the temporal cross-
correlations are integrated with built up binaural representations
then (2- and 3-D shape) contours can be inferred (Simmons, 1996;
Frontiers in Computational Neuroscience 15 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 16
Cariani and Baker 10.3389/fncom.2025.1571109
Simmons et al., 1996a). Narrow acoustic beams can act like
searchlights, thereby simplifying the problem of interfering echoes
(acoustic clutter).
7 Mechanoreception
Mechanoreception, mechanosensation, or the tactile sense
encompasses sensations related to mechanical movement of the
skin. Flutter-vibration is the sensation that is analogous to
auditory pitch, and like pitch, there is strong evidential basis for
phase-locked temporal pattern coding (Werner and Mountcastle,
1965; Mountcastle, 1967; Keidel, 1968; Mountcastle et al., 1969;
Mountcastle et al., 1990; Johnson and Hsiao, 1992; Harvey et al.,
2013). (Mountcastle, 1988) is an excellent starting point.
Humans can distinguish mechanical vibratory periodicities
over a wide range of frequencies, from 5 to 300 Hz and above,
depending on stimulating conditions (Talbot et al., 1968; Keidel,
1984; Morley et al., 1990). Flutter-vibration sensations can also be
elicited by diﬀerent frequencies of electrical microstimulation of
the hand, up to 1000 Hz (Mountcastle, 1993). This is consistent
with localizations on the skin and tongue based on down to 1 ms
diﬀerences in electrical pulse arrival times (von Békésy, 1967). He
carried out analogous experiments with non-electric olfactory and
gustatory localizations used air puﬀs into the two nostrils and
injected solutions of tastants onto the tongue, with comparable
results (von Békésy, 1964c; von Békésy, 1964a).
Two classes of sensory neurons that innervate mammalian
skin respond to vibratory stimuli. These are rapidly adapting
(RA) ﬁbers that innervate Meissner corpuscle end-organ receptors
that are sensitive to light touch and slip on the skin. RA ﬁbers
phase-lock in the 5–100 Hz range and those innervating Pacinian
corpuscle receptors, which phase-lock in the 30–1000 Hz range. An
alternative theory based on ratios of ﬁring rates of the two ﬁber
types was inconsistent with results of experiments using 30 and
150 Hz vibrotactile stimuli with diﬀerent amplitudes (Morley and
Rowe, 1990). Because of phase-locking, complex tactile sequences,
such as reading Braille, will have complex temporal pattern
correlates in spike trains (Morley et al., 1990). Roughness in
tactile perception would also presumably have similar correlates in
phase-locked time patterns, but see (Johnson and Hsiao, 1992) for
another view.
Mountcastle found that while ﬁrst-order intervals are
successively disrupted by accumulating jitter and intervening
spikes as one goes up the somatosensory pathway, phase-
locked all-order interval patterns of the vibratory stimulus were
maintained all the way up, from primary sensory ﬁbers to cortex
(Mountcastle, 1993). Thus, like the auditory coding of pitch, the
code for vibration pitch appears to be based on all-order intervals.
A recent study found evidence for millisecond-precision
temporal coding in macaque somatosensory cortex (S1) of
vibrotactile pitch for low frequencies (20–100 Hz) (Callier et al.,
2024). Other studies have found mixtures of rate and temporal
codes. Other studies of vibrotactile responses in rapidly-adapting
ﬁbers innervating glabrous skin of rats and mice found evidence
for both rate and temporal codes (Medlock et al., 2024). Recent
evidence in mice (Prsa et al., 2021; Lee et al., 2024) based
on probability of phase-locking supports a temporal code for
vibrotactile pitch (100–1900 Hz) at subcortical levels that is
transformed to a rate code at the thalamus. Another study in
S1 cortex in rats found rate and temporal codes for stimulus
location and random vibrational waveform patterns (Blanc and
Coq, 2007). Similar mixtures of multiplexed rate and temporal
codes have been proposed for perception of spatial edges on the
skin (Lankarany et al., 2019).
A great deal of work has been carried out on active sensing
in rodent vibrissal systems by Ahissar and Vaadia (1990) (see
section “3.9 Discussion”). They regard vibrissal systems as active
sensing systems par excellence. Early on they found evidence
for phase-locking and spike latency coding in the somatosensory
pathway, as well as units with oscillatory characteristics in
somatosensory cortex (Ahissar and Vaadia, 1990), spike latency-
to-ﬁring rate transformations (Ahissar et al., 2000), diﬀerent
sets of temporal codes for active and passive processes that
can also account for vibrissal hyperacuity (Szwed et al., 2003;
Knutsen and Ahissar, 2009).
Coding of sensory information gleaned by whiskers concerning
coarseness of surfaces is related to vibration roughness perception
in the skin (Arabzadeh et al., 2006), and here too, temporal codes
can convey information related to whisker deﬂections (Jones et al.,
2004; Jadhav et al., 2009). In the rat barrel cortex, ﬁrst spike latencies
may “form the basis for a fast robust population code” (Petersen
and Diamond, 2000; Petersen et al., 2002b, 2002a).
As with other modalities, these mechanoreceptive systems bear
structural and functional similarities to other sensory systems in
vertebrates and invertebrates. These similarities involve similar
types of receptors (It ¯o, 1992), phase-locked responses to temporal
onsets and patterns, e.g., as in insect cercal systems (Aldworth
et al., 2011), as well as common active sensing mechanisms
(Ahissar et al., 2023).
8 Electroreception
Weakly-electric ﬁsh, gymnotoform mormyrids such as
knifeﬁsh and elephantnose ﬁsh, generate weak alternating
sinusoidal electric ﬁelds for localizing prey and for intraspecies
communications (Bullock, 1982). By means of electroreceptors
that detect changes in electrical ﬁelds, and highly precise phase-
locking of spikes, they can sense subtle distortions in the ﬁelds
that are caused by other animals in their immediate vicinity. This
electroreceptive sense is useful in detecting prey in turbid water.
The distortions cause patterns of diﬀerent latencies in neural
spiking at diﬀerent places on their body surfaces that indicate the
direction of nearby prey.
These electroreceptive sensory systems can be regarded as
phase-locked spike latency codes that have similarities to both
binaural and somatic localization and echolocation. The latencies
can be regarded as relative delays or alternately as diﬀerent
phase or time oﬀsets in relation to sinusoidal electric ﬁelds
and electric pulses, respectively (Heiligenberg, 1989; Heiligenberg,
1991; Heiligenberg, 1994). The system thus resembles the temporal
auto-correlation and cross-correlation computations that are used
by other modalities (binaural hearing, echolocation, somatic,
gustatory, and olfactory localizations, (von Békésy, 1967; Carr and
Soares, 2002) in vertebrates and insects.
Frontiers in Computational Neuroscience 16 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 17
Cariani and Baker 10.3389/fncom.2025.1571109
Specialized receptors, gap junction electrical synapses, delay
lines, and neural coincidence detectors reduce spike timing jitters,
enabling the ﬁsh to detect sub-microsecond time diﬀerences (Carr
et al., 1986). Thus, in the electroreceptive system a latency-place
code appears to be converted to a channel code in which various
combinations of body points are represented. As with the Jeﬀress
delay-coincidence architectures, the output need not necessarily be
a rate-channel code at higher levels of the system. For example, the
next stage of processing could be a latency-place code rather than
another rate-channel code.
The ﬁsh also use their generated sinusoidal ﬁelds to
communicate with each other (Hopkins, 1988). The ﬁelds are
regular, very nearly sinusoidal, and typically have frequencies
of several hundred Hz. As with bats and cetaceans, to avoid
jamming, the ﬁsh adjust the signals they produce based on
sensed sub-millisecond timing diﬀerences (Baker et al., 2013).
And as in human speech and animal vocalizations, multiple
kinds of temporally-coded information are multiplexed together in
communications signals.
9 Vision
9.1 Form vision
Historically vision has largely been envisioned as a rate-
channel sensory modality in which time plays little or no role.
However, coming from the perspective of the auditory neurogram
and interspike interval distributions of Figure 2 and the visual
interspike interval distributions of Figure 3, it would appear
that the neural coding at its earliest stages in the retina, optic
nerve, and thalamus (lateral geniculate body, LGN) may be a
phase-locked spatiotemporal pattern code, with visual forms being
spatial patterns of near-synchronous, phase-locked spikes. In the
ﬁgure, the period and interval histograms show clear phase-locking
(spikes and intervals under the line) to the sinusoidal temporally
modulated constant velocity moving grating. Phase-locking can
also generate diﬀerent, but reliable ﬁrst spike latencies, if retinal
elements ﬁre at diﬀerent phases and relative times. Reliable relative
latencies in retinas and higher centers can encode contrasts with
high temporal precisions (Pollen et al., 1989; Bialek et al., 1991;
Reinagel and Reid, 2000; Gollisch and Meister, 2008; Baden et al.,
2011; Gutig et al., 2013). If spike response jitters of ∼1 ms or
less are present (Carney et al., 1995), then the unexpected vernier
acuities observed for high velocity moving targets may be explicable
in terms of phase-locked millisecond-precise spike timings. See
discussion of the hyperacuity problem above (section 4.6).
As in relational, correlation-based theories of visual form
(Kabrisky, 1967; Uttal, 1987, 1988) and texture (Uttal, 1975),
auto- and cross-correlation of spatial intervals and phase relations,
respectively, would enable representations of patterns of edges and
even points (dotted forms). Similar in many respects to temporal
correlation-based scanning models (Reitboeck et al., 1988; Pabst
et al., 1989; Reitboeck, 1989), lateral delay lines and coincidence
detectors would convert spatial intervals and phase-relations into
temporal, all-order interspike intervals, as in Figure 3A, and relative
spike time-of-arrival patterns that would encode phase relations.
For critical perspectives and debates on the role of eye movements
in vision, see (Ahissar and Arieli, 2012; Rucci et al., 2018; Rucci
et al., 2025), and (Gur, 2024).
This kind of spatiotemporal representation based on phase-
locking at its root would seem to be consistent with the necessity of
image motion or ﬂashed transients for form vision. Forms rapidly
disappear when images are stabilized (Ditchburn and Ginsborg,
1952), in as little as tens of milliseconds (Coppola and Purves,
1996). When images are well-stabilized, phase-locking should be
completely abolished. As with the order-of-ﬁring codes discussed
above (section 4.6), quick encoding of images would only require
one-spike-per-channel in only a fraction of channels (Gautrais and
Thorpe, 1998; Van Rullen et al., 2005). This is also consistent with
form-from-temporal-synchrony visual percepts, a.k.a. “illusions”
(Lee and Blake, 1999b,a; Blake and Lee, 2005), and the role
of interocular latency timing disparities, presumably reﬂected in
phase-locked spike times, that the visual system interprets as depth
cues in the Pulfrich Eﬀect (Graham, 1966; Lanska et al., 2015).
There are many parallels between auditory and visual
representations and Gestaltist grouping principles (Ando, 2009).
There is a perception of a visual ﬂicker stimulus at the “missing
fundamental” of harmonically-related ﬂicker components (e.g., one
can match a combination of 4, 5, and 6 Hz ﬂickers to a 1 Hz ﬂicker).
There is also a spatial frequency analog wherein gratings of 4 f, 5f,
and 6 f spatial frequencies can be matched to a grating with the
fundamental frequency f (de Valois and de Valois, 1990).
Historically, most theories of vision have been cast in terms
of rate-channel codes, receptive ﬁelds, and local feature detectors
rather than in terms of correlated patterns of spikes. Uncontrolled
eye movements and extra spikes complicate the detection of phase-
locked spikes. Under-controlled stimulus timing also complicates
detection of phase-locking. For example, due to uncertainties in
the ﬁeld phases of the monitor that was used to deliver the
moving gratings in Figure 3A, periodicities higher than ∼16 Hz
were smeared out in post-stimulus time (PST) histograms. Higher
frequency patterns were only clearly resolved in the all-order
interspike interval distributions shown. For the auditory interval
histograms of Figure 2, interval histograms were compiled for each
trial and then added together. If they look at interspike interval
distributions, most vision researchers examine only ﬁrst-order
intervals to compute ﬁring rates, in which periodicity patterns
can be obliterated by intervening spikes (e.g., bursts, mixtures of
phase-locked spikes with diﬀerent latencies or non-phase-locked
spikes). Standard vision theory has also not been helpful because it
assumes, often tacitly, that any phase-locked spikes due to motion
or transients is converted, via a layer of motion detectors, to rate-
place codes, after which, according to the theory, all ﬁne timing
related to phase-locking can then be ignored.
All the diﬃculties notwithstanding, there have been many
visual neurophysiologists who have looked hard for visual
information in ﬁne spike timing cues and their correlations
(Victor and Purpura, 1996). Temporal precisions of spikes
increase for changing (moving or ﬂuctuating) images, as opposed
to static ones (Mechler et al., 1998). Temporal codes appear
to be more stable (reliable, robust) than their rate-based
counterparts (Zhu et al., 2025) as well as being more eﬃcient
(Price and Gavornik, 2022).
There were earlier proposals for temporal coding (Reichardt,
1961), multiplexing (Chung et al., 1970; Wasserman, 1992) and
correlation-based theories of brain function (von der Malsburg,
Frontiers in Computational Neuroscience 17 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 18
Cariani and Baker 10.3389/fncom.2025.1571109
1994), but interest in these issues really blossomed in the 1990’s.
There is a sizable literature from that period concerning visual
codes and operations: synchronies (Singer, 1994b,a; Konig et al.,
1995; Singer, 1999), oscillations (Gray et al., 1989; Gray et al.,
1992), spike correlations (Mastronarde, 1989; Lestienne et al.,
1990; Abeles, 1994; Lestienne, 1996; Lestienne and Tuckwell, 1998;
Gerstein, 2004; Abeles, 2009), temporal coding (Bialek et al.,
1991; Egelhaaf and Borst, 1993; Gawne, 1999; Oram et al., 1999),
multiplexing (Richmond et al., 1989; Richmond et al., 1990;
McClurkin et al., 1991a; McClurkin et al., 1991b; McClurkin et al.,
1991c; Eskandar et al., 1992; Eskandar et al., 1992; McClurkin
et al., 1993; McClurkin and Optican, 1996; McClurkin et al., 1996),
and feature-binding (Eckhorn and Reitboeck, 1990; Eckhorn, 1991;
Singer and Gray, 1995; Gray, 1999).
However, it is not clear to us where the ﬁeld went and where
it currently stands, e.g., encoding of spatial frequencies in gamma
rhythms (Han et al., 2021) and distributed processing via temporal-
channel codes (Singer, 2009, 2018). It seems that these as well as
other fundamental questions involving the neural codes for basic
visual attributes such as form, texture, and color still remain to
be solved.
9.2 Visual texture
In the auditory system, pitches and timbres of resolved
harmonics are famously insensitive to diﬀerences in phase-spectra
(envelopes of unresolved harmonics are a diﬀerent matter). The
AM and QFM tones in Figure 2 are perceptually indistinguishable,
despite quite obvious diﬀerences in their waveforms. This is why an
inherently phase-insensitive autocorrelation-like all-order interval
code is necessary to account for auditory percepts.
Visual texture representations appear to be analogously
insensitive to phase – they cannot be pre-attentively distinguished
(Pabst et al., 1989). Their discrimination is dependent only on
spatial interval statistics as in spatial autocorrelations and not
on phase information, as in image cross-correlations (Kabrisky,
1967; Uttal, 1975, 1987, 1988). Autocorrelation representations
are sensitive to frequency content and disparities but insensitive
to phase disparities, whereas cross-correlations of waveforms are
highly sensitive to phase disparities (e.g., the AM vs. QFM
waveforms of Figure 2). If spatial intervals are converted to time
intervals in the visual system, as the scanning models do (Reitboeck
et al., 1988; Pabst et al., 1989; Reitboeck, 1989), then auditory timbre
and visual texture perception would have many coding similarities.
Roughness also has analogs in both auditory and visual textural
domains (Ando, 2009).
Information concerning visual textures can be found in spike
timings (Pollen et al., 1985; Victor and Conte, 1996). Characteristic
texture percepts can also be reliably induced by particular temporal
patterns of ﬂicker (Wilson, 1960; Fiorentini and MacKay, 1965;
Perkell and Bullock, 1968; Young et al., 1975; Richmond et al.,
1989). Retina and visual cortex contain many slow and fast
horizontal delay paths that generate two-dimensional standing
wave spatial patterns of excitations when rhythmic ﬂicker stimuli
are presented (Siegel and Read, 1993) that are perhaps not unlike
those created by spatiotemporal patterns of neural responses to
regular visual textures. Of related interest were rather striking
subjective responses that were sometimes evoked by ﬂashed
visual stimuli delivered at particular phases of alpha rhythms
(Walter, 1959; Hutchinson, 1991).
9.3 Color
Color may be a temporally-coded percept. These sensations
have been variously called ﬂicker colors, subjective colors, Prevost-
Fechner-Benham subjective colors, Fechner color, or pattern-
induced ﬂicker colors (PIFCs). In the early 19th century, the
perceptual phenomenon was discovered ﬁrst by a French monk
Benedict Prevost and then by the psycophysicist GustavFechner
that ﬂickering white light can induce diﬀerent color sensations. See
(Cohen and Gordon, 1949) for a detailed early history. Fechner
designed several black and white disks that, when rotated below the
ﬂicker fusion frequency limit, produced diﬀerent colors depending
on the relative durations of alternating black and white segments.
Figure 3B shows disks constructed and investigated by Fechner,
Helmholtz, and Benham, all of which produce a range of colors,
depending on the rotational speed of the disk. In Benham (1894)
created a top, called the artiﬁcial spectrum top, or Benham’s top,
which was sold as a toy (Benham, 1894, 1895).
As a historical note, in the early 1960’s a shuttering device, the
Butterﬁeld Color Encoder, was built for black-and-white (B&W)
television cameras that converted color images to B&W ﬂicker
patterns that could then be broadcast to B&W televisions whose
viewers then, in many cases unexpectedly, saw color images on their
B&W TV screens (Griﬃn, 1968; Sheppard, 1968).
Many years later Festinger, Allyn, and White, using glow tubes,
determined the temporal patterns that evoke particular colors,
Figure 3B (Festinger et al., 1971). All colors normally seen by
trichromat humans can be produced this way. The temporal
patterns have been Fourier-analyzed (Tritsch, 1992).
On its face, the Prevost-Fechner-Benham Eﬀect appears to
strongly suggest a neural code for color (Sheppard, 1968). Many
diﬀerent classes of retinal cells phase-lock to the coarse temporal
monochromatic ﬂicker patterns. If the central neural code for color
is a temporal pattern of spikes, then the central visual system
would interpret the ﬂicker patterns as color information. When
the eye is presented with a visual scene with diﬀerent mixtures
of wavelengths, diﬀerent activation latencies and lateral inhibitory
interactions might naturally produce these patterns.
There has been a good deal of debate over the years about
whether the ﬂicker patterns might have diﬀerential eﬀects on
diﬀerent classes of cones due to lateral inhibition or diﬀerent
temporal response properties, e.g., (von Campenhausen, 1969;
von Campenhausen et al., 1992), but these hypotheses are not
necessarily inconsistent with a temporal code for color, as they
might be the means by which the system encodes color information.
However rate-channel coding of speciﬁc subpopulations would
appear to be falsiﬁed by electrical stimulation experiments.
Electrical stimulation of the whole eye in human subjects using
the time patterns of Festinger et al. (1971) produced phosphene
ﬂashes of colors similar to those evoked by the glow tube (Young,
1977). Since electrical stimulation presumably excites all retinal
cells to ﬁre in the same temporal pattern, this is appears to be strong
evidence in favor of a central temporal code for color.
Frontiers in Computational Neuroscience 18 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 19
Cariani and Baker 10.3389/fncom.2025.1571109
There is some evidence for characteristic temporal patterns
in normal color vision. Such temporal patterns have been found
in optic nerve (Kozak and Reitboeck, 1974; Kozak et al., 1989),
lateral geniculate (Young and De Valois, 1977), and visual cortex
(Richmond et al., 1989; McClurkin et al., 1993). A model for
the representation of color using temporal encoding machines
(TEMs, section “13 Design of artiﬁcial systems”) to separate
multiple temporal spike pattern components has been proposed
(Lazar et al., 2015).
10 Chemical senses: gustation and
olfaction
Because phase-locking cannot track the vibratory frequencies
of molecules, phase-locked temporal pattern codes are ruled out.
However, stimulus-triggered temporal pattern codes, spike latency
codes, and mixed latency-channel codes are all still possible.
Because electrical stimulation of whole populations appears to
mimic chemical stimulation in the gustatory system, a temporal
pattern code appears most likely for gustation. On the other
hand, due to diﬀerences in latencies of its receptor and neuronal
responses as well as some channel speciﬁcities, spike latency
and latency-channel codes appear to be the most likely types
of temporal codes to be operant in olfaction. In both systems,
temporal and rate-place codes can coexist, both in the same neural
populations and in separate ones.
10.1 Gustation
Strong evidence exists in favor of temporal pattern codes for
taste in the gustatory pathways of vertebrates and arthropods (Katz,
2005; Glendinning et al., 2006; Hallock and Di Lorenzo, 2006;
Di Lorenzo et al., 2009; Ohla et al., 2019). Often both temporal
and rate codes are found together, sparking active discussions
and debates about temporal vs. rate coding vs. multiple codes in
speciﬁc neural populations (Spector and Travers, 2005; Wilson
et al., 2012; Jezzini et al., 2013; Reiter et al., 2015; Staszko et al., 2020;
Roper, 2022).
Through most of the history of modern neuroscience, following
( Adrian, 1928), it was assumed that taste buds (gustatory papillae)
responded only to speciﬁc tastant classes. Consequently, gustatory
sensations were thought to be determined entirely by ﬁring
rates in the primary neurons of the gustatory system, in the
chorda tympani. However, doubt was cast on these assumptions
when highly speciﬁc taste receptors were not found (Kimura and
Beidler, 1961; von Békésy, 1964c). Early and subsequent single-
unit neurophysiological experiments began to ﬁnd temporally
patterned responses.
Experiments with electrical stimulation of the tongue to
produce taste sensations began at the dawn of electrophysiology,
ﬁrst being “described by Sulzer, a few decades before Volta’s famous
experiments”(von Békésy, 1964c, i.e., ca. 1752–1754). von Békésy
(1964d) carried out a series of electrical stimulation at various
tongue locations and temporal frequencies and was able to elicit
sensations of what are thought to be the four primary taste classes:
sweet, sour, bitter, and salty.
In Covey (1980) Covey recorded whole chorda tympani
responses to four taste classes presented to decerebrate rats
(Figure 3C). When the tastants are presented, the animals, despite
the decerebration, elicit mouth gestures that are similar to those
of intact rats and that are characteristic of tasting sweet, sour,
salty, or bitter ﬂavors. Stimulation of the chorda tympani with the
same temporal patterns, but not with other patterns, elicited the
corresponding behavioral gestures. In the decade following, Patricia
DiLorenzo carefully replicated Covey’s experiments and carried out
similar ones in the nucleus of the solitary tract, the next station in
the ascending gustatory pathway.
In, Di Lorenzo and Hecht (1993) summarized the early
situation:
“In the study of the neural code for gustation in the central
nervous system, the temporal patterns of responses to taste are most
often ignored. Typical measures of taste responses account for the
overall amount of neural activity evoked by a tastant but do not
reﬂect the temporal arrangement of spikes during the response.
These measures would be adequate descriptors if the total number
of spikes associated with a given response were equally distributed
within the response interval; however, that is almost never the case.
Instead, most taste responses are characterized by variations in the
rate of ﬁring. The time course and magnitude of these variations
deﬁnes the temporal pattern of a response. Given numerous reports
that diﬀerent taste stimuli appear to evoke distinctive temporal
patterns of response in a number of taste-related neural structures
and that similar-tasting stimuli evoke similar temporal patterns of
response [15 citations ranging from 1957 to 1989, omitted here]
it is not surprising that several investigators have suggested that
this feature of the neural response may contain important, if not
essential, information about taste stimuli.”
For more than four decades now Patricia DiLorenzo and co-
workers have expanded this line of investigation into temporal
coding of gustation to deepen understanding of the neuroanatomy
and neurophysiology of gustatory systems and their functioning:
(Di Lorenzo and Schwartzbaum, 1982; Di Lorenzo, 1989, 2000;
Hallock and Di Lorenzo, 2006; Di Lorenzo et al., 2009;
Di Lorenzo, 2021).
10.2 Olfaction
Strong evidence exists for spatiotemporal, latency-channel
and ﬁring sequence codes in olfaction Chong and Rinberg,
2018; Chong et al., 2020; Haddad et al., 2010; Haddad et al.,
2013; Chong and Rinberg, 2018; Perl et al., 2020; Verhagen
et al., 2023; Chong et al., 2020). See (Wang et al., 2024;
Uchida et al., 2014) for excellent reviews.
Complex rate-coded temporal patterns have historically been
observed, and these have baﬄed olfactory neurophysiologists
(Lettvin and Gesteland, 1965; Gesteland et al., 1968). In part this
has been due to the complexity of the sense of smell, where the
dimensionality of the perceptual space has been a matter of dispute.
This is because there are on the order of 1000 diﬀerent receptor
types in the human olfactory system, such that assumptions of
channel coding of odor identity would require a similar number
of dimensions. Adding to the problem is the lack of any clear
low-dimensional structure to chemical odorant space (Haddad
Frontiers in Computational Neuroscience 19 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 20
Cariani and Baker 10.3389/fncom.2025.1571109
et al., 2008), unlike a cochleotopic frequency map in audition or
a spatial retinotopic map in vision. It is diﬃcult to identify what
the primaries of the space would be (Boring, 1942). Rather than
a trillion discriminable odor combinations that suggest a high-
dimensional space, the number of dimensions and distinctions may
be much smaller and more manageable (Meister, 2015). There
are some opponency relations, where pairs of odors can cancel
each other out. Still more challenging is the problem of stimulus
invariance with respect to intensity, here odorant concentration.
Some odorants elicit diﬀerent percepts at diﬀerent concentrations.
Finally, receptors in the olfactory bulb are constantly turning over
every few weeks, such that the system is constantly being rewired,
potentially complicating labeled line and channel-based coding and
network learning strategies.
A stable set of temporal codes might solve this problem of
coding constancy, and investigators have found temporal pattern
correlates of some odorant types in the past (Macrides and
Chorover, 1972; Macrides, 1977; Meredith and Moulton, 1978;
Meredith, 1981; Kauer, 1990; Kauer and White, 2001). Inspired
by diﬀerent latencies of response to odorants, (White and Kauer,
2001), Kauer, White, and co-workers developed an artiﬁcial nose
using synthetic DNA-based receptors and similar coding principles
(White et al., 2008).
There is also phase-locking to sniﬃng cycles (Mori and
Sakano, 2022; Macrides and Chorover, 1972 #7592), which though
not necessarily essential for coarse olfactory discriminations,
may nevertheless improve odor discrimination acuity. Similarly,
oscillations that emerge when engaging in active smelling (sniﬃng)
may have functional relations to neural coding (Freeman,
1975; Kauer, 1998; Dorries and Kauer, 2000; Kauer, 2002;
Kay et al., 2009).
Although the olfactory system has traditionally been regarded
as operating over relatively long timescales (hundreds of
milliseconds to seconds), rodents can make ﬁne odorant
discriminations and invariant recognitions despite rapid
ﬂuctuations of odorant concentrations on short timescales
(10–30 ms). These fast changes yield temporally-coded signatures
that could be used (1) for active sensing discounting of inhalation
dynamics so as to realize odor quality/identity invariance (Jordan
et al., 2018), (2) for gaining information about odor plumes and
the environment to facilitate tracking of odors and separating
out multiple odor plumes in natural environments (Ackels
et al., 2021), and/or (3) separating out temporal neural response
components related to odorant concentrations and their onset
dynamics from other later components that are invariant with
respect to odor quality and odorant identity (Lazar et al., 2023).
Robotic olfactory systems have been designed and constructed to
take advantage of fast olfactory processing and temporal coding
(Dennler et al., 2024).
The research group of Giles Laurent and former co-workers
has investigated temporal and correlation coding (Laurent et al.,
1996; Laurent, 1999; Wehr and Laurent, 1999; Friedrich and
Laurent, 2001; MacLeod and Laurent, 1996), temporal sequence
codes (Wehr and Laurent, 1996), spatiotemporal codes (Laurent
et al., 1998), oscillations (Perez-Orive et al., 2002), and dynamical
system trajectories (Laurent, 2002; Mazor and Laurent, 2005) in
the mushroom body of locusts. In an experiment to test the
functional role of population oscillations in the locust mushroom
body, they applied picrotoxin (Stopfer et al., 1997), which
abolishes the oscillations, and found that ﬁne, but not coarse,
odorant discriminations were impaired. One interpretation is that
oscillations facilitate better coding, but that they are not essential
for making more basic distinctions. Another would be to postulate
dual codes.
Optogenetic stimulation has been used eﬀectively to investigate
the relative contributions of temporal, spatial, and spatiotemporal
codes in the rat olfactory bulb (Haddad et al., 2013; Chong
and Rinberg, 2018; Chong et al., 2020). Using the optogenetic
technique, researchers have been able to independently drive
the rat olfactory bulb using recorded spatial and temporal
patterns of neural responses to natural and specially designed
odorants. They ﬁnd that particular coarse spatiotemporal patterns
of stimulation are most eﬀective in predicting perceptual judgments
of smell.
11 Cutaneous sensations (pain, itch,
temperature)
The cutaneous senses typically include tactile sensations
(touch, vibration, pressure), pain, itch, temperature, and
proprioception (body position, joint positions, muscle stretch).
Touch and vibration are covered in section “8 Electroreception”;
proprioception and the vestibular sense in section “13 Design of
artiﬁcial systems.”
The somatic senses of pain, itch, and temperature have
mainly been approached from labeled line and overlapping
neuronal populations. Ma (2010) provides a good review of
the neural coding problem as it pertains to these senses.
They note that “the activation of speciﬁc sensory ﬁbers is
suﬃcient to evoke a speciﬁc somatic sensation.” But inter-modality
interactions, e.g., pain and itch, hot and cold, and touch and
pain, are problematic for simple labeled line theories. In order
to explain these interactions “population coding” theories in
which there are separable neural populations that have some
cross-talk have been proposed (Ma, 2010). Perhaps counter
intuitively, diﬀerent separate populations may be responsible
for the sensations of hot and cold (Wang et al., 2018).
Rate-based multiplexing of neural responses in rat S1 to
itch and pain also are relevant to the cross-talk problem
(Woo et al., 2022).
Another review (Bokiniec et al., 2018) takes up similar
sensory crosstalk issues, but notes that there are proposed
codes that “combine specialized receptors with temporal coding
schemes.” Note that “temporal coding” in these contexts can mean
coarsely-scaled temporal successions of activations of diﬀerent
populations of neurons rather than temporal patterns of spikes.
Burst-pattern coding has been proposed for thermoreception,
but it is not clear how well it would explain such multimodal
cross-talk phenomena. See (Doetsch, 2000; Green, 2004;
Perl, 2007; Prescott et al., 2014) for discussions of non-temporal
labeled line, gate-control, channel-pattern codes, and cross-talk
population codes.
Despite its importance and extensive clinical data, the neural
codes that subserve sensations of itch and pain are still poorly
understood (Schmelz, 2015, 2021). It appears that primary
somatosensory nocioceptive aﬀerents are multimodal, such that
Frontiers in Computational Neuroscience 20 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 21
Cariani and Baker 10.3389/fncom.2025.1571109
they respond to both pain and itch provoking stimuli (Ikoma
et al., 2006; Hu et al., 2021). Diﬀerent ﬁring patterns have been
hypothesized to encode the diﬀerent sensations in the same
neurons: burst-like activity for itch vs. single action potentials for
pain (Sharif et al., 2020).
From a temporal coding perspective, by far the most
intriguing experiments are those reported by Emmers (1966b),a,
Emmers (1969, 1970, 1976, 1981). Recording in the thalamus,
he found separate temporal pattern codes for diﬀerent types of
thalamic neurons sensitive to touch, pressure, thermal, gustatory,
and pain stimuli (Emmers, 1981, p. 116). The spike patterns
had the form of onset bursts of a few spikes followed by
interspike intervals that were characteristic of the type of stimulus
driving the unit. Some units showed temporally multiplexed
and interleaved spike patterns. This work has largely been
ignored we think because the results sound too good to be
true, but these experiments really should be carefully replicated
by others and their results, negative or positive, should be
reported out.
12 Proprioception and movement
The proprioceptive system provides continuous feedback
information about body movements. Stretch receptors phase-lock
to both transient and periodic muscle movements, such that the
somatosensory system receives a temporal pattern readout of
all of the movements of muscles. Likewise vestibular aﬀerents
robustly phase-lock to acceleration transients (Curthoys et al.,
2017), again providing temporal pattern feedback information
for self- and externally-caused motion. In many cases, there also
will be similar time patterns accompanying the self motion, in
terms of changes in visual scenes correlated with head movements,
and changes in acoustic scenes correlated with vocalizations.
Given these commonalities of temporal structure in action and
perception, temporal patterns of perceived events can inform their
production. Likewise, temporal patternings used to produce a
sequence of actions (such as a rhythmic drum sequence) can inform
the perceptual detection and recognition of those patternings.
For time patterns of perception and action, what goes around,
comes around.
13 Design of artiﬁcial systems
Whereas science is primarily concerned with understanding
how the natural world works using empirical data and models,
engineering is ultimately focused on designing and constructing
artiﬁcial systems that can perform useful functions. The two
pursuits interact and mutually inform each other in the realms of
computational neuroscience (Rieke et al., 1997) and neuromorphic
engineering (Indiveri and Horiuchi, 2011; Indiveri et al., 2011;
Kudithipudi et al., 2025). Computational neuroscience involves
models of neuronal behavior and of how biological nervous
systems achieve informational functions that guide behavior.
Neuromorphic engineering involves the design and construction of
artiﬁcial devices using principles from neuroscience that have been
suggested by biological brains.
Despite their lack of many biophysical details, simpliﬁed
engineering-inspired models of neural information processing
can prove useful in considering putative coding and processing
schemes in the brain. They can clearly show how some particular
behavioral function might be achieved. Provided that their
simpliﬁcations retain essential aspects of biological neural signals,
elements, and architectures, these functional models can serve as
demonstrations of principles.
Aforementioned examples of how temporally-coded inputs and
putative subsequent signal processing can be used to realize various
speciﬁc behavioral functions for sound localization (Jeﬀress Model,
section “6.2 Sound localization”), pitch perception (Licklider
duplex and triplex models section “6.1 Basic auditory qualities”),
acoustic front ends (Baker’s HEAR and Ghitza’s Ensemble Interval
Histogram (EIH), section “6.1 Basic auditory qualities”), artiﬁcial
noses (section “10.2 Olfaction”), and active perception (phase-
locked loops, section ”3.9 Temporal coding in active sensing”).
Aside from brief discussions of central phase-locked loops
for active perception (sections ”3.9 Temporal coding in active
sensing”, “11 Cutaneous sensations (pain, itch, temperature), ” and
“10.2 Olfaction”), a full treatment of how temporal sensory codes
might be interpreted in central stations lies beyond the scope
of this paper. Elsewhere we have proposed that brains may use
multiplexed temporal codes and time-domain correlation-based
operations for a much wider range of functions than generally
envisioned, and have discussed the kinds of temporal processing
neural architectures that might handle such codes (Cariani and
Baker, 2022; Baker and Cariani, 2025).
Theories of how biological brains handle information can
also provide new principles for designing more powerful
and elegant artiﬁcial systems. Although most artiﬁcal signal
processing, pattern recognition systems, neural networks, and
robots have used channel-coded representational schemes, there
is no reason that artiﬁcial computing and robotic systems cannot
incorporate temporal coding as well. As observed in many sensory
systems, temporal coding can provide more precise and robust
representations of incoming sensory information than channel
codes. Temporal codes also obviate the need for windows and
their limitations. Early examples of temporal processing hardware
architectures include analog (Fukushima et al., 1970) and analog
VLSI implementations (Lazzaro and Mead, 1989; Mead, 1989;
Douglas et al., 1995).
Although most neural networks to date have assumed scalar
signals (artiﬁcial counterparts of ﬁring rates), integrating elements,
and sequences of coarse processing (time) steps, some neural
networks have been proposed that explicitly incorporate ﬁne
time bases and individual spiking events. Examples include time-
delay neural networks (TDNNs) (Tank and Hopﬁeld, 1987),
pulse-coded spiking neural networks (SNNs) (Gerstner, 1999;
Maas, 1999; Sejnowski, 1999; Y amazaki et al., 2022), synﬁre
chains and polychronous networks, and neural timing nets
(Cariani, 2001c, 2004).
A salient, widely recognized advantage of neural networks that
process pulses (electronic and numerical analogs of spikes) is that
they use much less power than comparable conventional multilayer
neural networks. Although most spiking networks in the past have
assumed pulse frequency modulation (PFM) encodings, i.e., rate-
channel codes, temporal codes could also be used more widely in
spiking neural networks of the future.
Frontiers in Computational Neuroscience 21 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 22
Cariani and Baker 10.3389/fncom.2025.1571109
Address-event representations (AERs) (Srivatsav et al., 2023),
event-based temporal coding and processing (Risi et al., 2020;
Assa et al., 2025) and time encoding machines (TEMs) (Lazar
and Pnevmatikakis, 2011; Lazar et al., 2015) import temporal
coding strategies into artiﬁcial, pulse-coded devices for general
computational signal processing (Indiveri and Horiuchi, 2011).
As in the Fukushima et al. (1970) artiﬁcial retina, events consist
of changes and their timings rather than static properties. These
kinds of representations appear to enable continuous signals to
be reconstructed from their pulse-coded event timings (Lazar and
Tóth, 2004; Adam et al., 2020). Direct incorporation of temporal
codes and time-domain operations into neural networks and other
pulse-coded systems thus promises to be a fertile avenue for
technological innovation in the future.
14 Conclusion
Evidence for temporal coding exists in virtually every sensory
system, often coexisting with rate-channel codes.
In many sensory systems, spike precisions are on the order of a
millisecond or less.
Temporal codes, as discussed here, can take the form of
either characteristic temporal patterns of spikes or of characteristic
patterns of spike response latencies.
The particular temporal spike patterns that are produced can
be produced extrinsically, through phase-locking in which the
stimulus impresses its time structure on response spike trains.
They can also be produced intrinsically, by the triggering
of neurons and local circuits. The patterns produced reﬂect the
internal organization of the neural circuits rather than the ﬁne time
structure of the stimulus.
First-spike latencies in response to onset events can
be quite precise.
Combinations of temporal and channel-based codes are possible.
A number of sense modalities may rely on cross-channel
patterns of ﬁrst-spike latencies.
Firing sequence codes are temporal codes that rely on spiking
order rather than metrical time relations.
Many auditory percepts related to stimulus qualities
can be modeled in terms of auto-correlation-like interspike
interval distributions.
Many auditory percepts related to localization may be explained
in terms of temporal cross-correlations (direction) and auto-
correlations (distance, echo-delay).
Early vision may turn out to rely on a phase-locked,
spatiotemporal pattern code.
Phase-locked temporal pattern codes can use autocorrelation
operations to represent the internal periodicities in stimulus
waveforms. They can use temporal cross-correlations to represent
diﬀerent times-of-arrival of stimuli at diﬀerent sensory surfaces and
to analyze phase relations.
Further investigations into temporal coding promise a fertile
ground for new scientiﬁc discoveries and technologies.
Data availability statement
The original contributions presented in this study are included
in this article/supplementary material, further inquiries can be
directed to the corresponding author.
Author contributions
PC: Conceptualization, Writing – original draft, Writing –
review and editing. JB: Conceptualization, Writing – original draft,
Writing – review and editing.
Funding
The author(s) declare that no ﬁnancial support was received for
the research and/or publication of this article.
Conﬂict of interest
The authors declare that the research was conducted in the
absence of any commercial or ﬁnancial relationships that could be
construed as a potential conﬂict of interest.
Generative AI statement
The authors declare that no Generative AI was used in the
creation of this manuscript.
Publisher’s note
All claims expressed in this article are solely those of the
authors and do not necessarily represent those of their aﬃliated
organizations, or those of the publisher, the editors and the
reviewers. Any product that may be evaluated in this article, or
claim that may be made by its manufacturer, is not guaranteed or
endorsed by the publisher.
References
Abeles, M. (1994). “Firing rates and well-timed events in the cerebral cortex, ” in
Models of neural networks II. Temporal aspects of coding and information processing in
biological systems, eds E. Doumany, J. L. van Hemmen, and K. Schulten (New York,
NY: Springer Verlag), 121–140.
Abeles, M. (2009). Synﬁre chains. Scholarpedia 4:1441. doi: 10.4249/scholarpedia.
1441
Ackels, T., Erskine, A., Dasgupta, D., Marin, A. C., Warner, T. P. A., Tootoonian,
S., et al. (2021). Fast odour dynamics are encoded in the olfactory system and guide
behaviour. Nature 593, 558–563. doi: 10.1038/s41586-021-03514-2
Adam, K., Scholeﬁeld, A., and Vetterli, M. (2020). Sampling and reconstruction of
bandlimited signals with multi-channel time encoding. IEEE Trans. Signal Process. 68,
1105–1119. doi: 10.1109/TSP.2020.2967182
Frontiers in Computational Neuroscience 22 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 23
Cariani and Baker 10.3389/fncom.2025.1571109
Adrian, E. D. (1928). The basis of sensation. London: Christophers.
Ahissar, E. (1998). Temporal-code to rate-code conversion by neuronal phase-
locked loops. Neural Comput. 10, 597–650. doi: 10.1162/089976698300017683
Ahissar, E., and Arieli, A. (2012). Seeing via miniature eye movements: A dynamic
hypothesis for vision. Front. Comput. Neurosci. 6:89. doi: 10.3389/fncom.2012.00089
Ahissar, E., and Assa, E. (2016). Perception as a closed-loop convergence process.
Elife 5:e12830. doi: 10.7554/eLife.12830
Ahissar, E., and Vaadia, E. (1990). Oscillatory activity of single units in a
somatosensory cortex of an awake monkey and their possible role in texture analysis.
Proc. Natl. Acad. Sci. U.S.A. 87, 8935–8939. doi: 10.1073/pnas.87.22.8935
Ahissar, E., Haidarliu, S., and Zacksenhouse, M. (1997). Decoding temporally
encoded sensory input by cortical oscillations and thalamic phase comparators. Proc.
Natl. Acad. Sci. U.S.A. 94, 11633–11638. doi: 10.1073/pnas.94.21.11633
Ahissar, E., Nagarajan, S., Ahissar, M., Protopapas, A., Mahncke, H., and Merzenich,
M. M. (2001). Speech comprehension is correlated with temporal response patterns
recorded from auditory cortex. Proc. Natl. Acad. Sci. U.S.A. 98, 13367–13372. doi:
10.1073/pnas.201400998
Ahissar, E., Nelinger, G., Assa, E., Karp, O., and Saraf-Sinik, I. (2023).
Thalamocortical loops as temporal demodulators across senses. Commun. Biol. 6:562.
doi: 10.1038/s42003-023-04881-4
Ahissar, E., Shinde, N., and Haidarliu, S. (2015). Systems neuroscience of touch.
Scholarpedia 10:32785. doi: 10.2991/978-94-6239-133-8_33
Ahissar, E., Sosnik, R., and Haidarliu, S. (2000). Transformation from temporal
to rate coding in a somatosensory thalamocortical pathway. Nature 406, 302–306.
doi: 10.1038/35018568
Akdogan, B., Wanar, A., Gersten, B. K., Gallistel, C. R., and Balsam, P. D. (2023).
Temporal encoding: Relative and absolute representations of time guide behavior.
J. Exp. Psychol. Anim. Learn. Cogn. 49, 46–61. doi: 10.1037/xan0000345
Aldworth, Z. N., Dimitrov, A. G., Cummins, G. I., Gedeon, T., and Miller, J. P.
(2011). Temporal encoding in a nervous system. PLoS Comput. Biol. 7:e1002041.
doi: 10.1371/journal.pcbi.1002041
Altes, R. A. (1989). Ubiquity of hyperacuity. J. Acoust. Soc. Am. 85, 943–952. doi:
10.1121/1.397566
Alves-Pinto, A., Palmer, A. R., and Lopez-Poveda, E. A. (2014). Perception
and coding of high-frequency spectral notches: Potential implications for sound
localization. Front. Neurosci. 8:112. doi: 10.3389/fnins.2014.00112
Ando, Y. (2009). Auditory and visual sensations. New York, NY: Springer.
Arabzadeh, E., Panzeri, S., and Diamond, M. E. (2006). Deciphering the spike
train of a sensory neuron: Counts and temporal patterns in the rat whisker pathway.
J. Neurosci. 26, 9216–9226. doi: 10.1523/JNEUROSCI.1491-06.2006
Ashida, G., and Carr, C. E. (2011). Sound localization: Jeﬀress and beyond. Curr.
Opin. Neurobiol. 21, 745–751. doi: 10.1016/j.conb.2011.05.008
Assa, E., Rivkind, A., Kreiserman, M., Khan, F. S., Khan, S., and Ahissar, E. (2025).
Temporal coding enables hyperacuity in event based vision. bioRxiv [Preprint] 26.
doi: 10.1101/2025.03.25.645190
Baden, T., Esposti, F., Nikolaev, A., and Lagnado, L. (2011). Spikes in retinal bipolar
cells phase-lock to visual stimuli with millisecond precision.Curr. Biol. 21, 1859–1869.
doi: 10.1016/j.cub.2011.09.042
Bagur, S., Bourg, J., Kempf, A., Tarpin, T., Bergaoui, K., Guo, Y., et al. (2025). A
spatial code for temporal information is necessary for eﬃcient sensory learning. Sci.
Adv. 11:eadr6214. doi: 10.1126/sciadv.adr6214
Bahl, L., Baker, J. K., Cohen, P. S., Jelinek, F., Lewis, B. L., and Mercer, R. L.
(1978). “Recognition of a continuously read natural corpus, ” inProceedings of the IEEE
ICASSP, (Tulsa, OK).
Baker, C. A., Kohashi, T., Lyons-Warren, A. M., Ma, X., and Carlson, B. A. (2013).
Multiplexed temporal coding of electric communication signals in mormyrid ﬁshes.
J. Exp. Biol. 216, 2365–2379. doi: 10.1242/jeb.082289
Baker, J. M. (1975). A new time-domain analysis of human speech and other complex
waveforms. Ph.D. thesis. Pittsburgh, PA: Carnegie Mellon University.
Baker, J. M. (1979). “Performance statistics of the HEAR acoustic processor, ” in
Proceedings of the IEEE ICASSP, (Washington, DC), 262–265.
Baker, J. M., and Cariani, P. (2025). Time-domain brain: Temporal mechanisms for
brain functions using time-delay nets, holographic processes, radio communications,
and emergent oscillatory sequences. Front. Comput. Neurosci. 19:1540532. doi: 10.
3389/fncom.2025.1540532
Baker, J. M., Baker, J. K., and Lettvin, J. Y. (1972). More visible speech.J. Acoust. Soc.
Am. 52:183.
Baker, J. M., Ramsey, R., Miller, M., Baker, J. K., and Cooper, C. (1974). Comparative
visual displays of time and frequency domain information in connected speech.
J. Acoust. Soc. Am. 55:412. doi: 10.1121/1.3437284
Barlow, H. B. (1961). “Possible principles underlying the transformation of sensory
messages, ” inSensory communication, ed. W. A. Rosenbluth (Cambridge, MA: MIT
Press), 217–234.
Barlow, H. B. (1995). “The neuron doctrine in perception, ” in The cognitive
neurosciences, ed. M. S. Gazzaniga (Cambridge, MA: MIT Press), 415–435.
Ba¸ sar, E. (1992). “Brain natural frequencies are causal factors for resonances and
induced rhythms, ” in Induced rythms of the brain , eds E. Ba?ar and T. H. Bullock
(Boston, MA: Birkhäuser), 425.
Benham, C. E. (1894). The artiﬁcial spectrum top. Nature 51:200.
Benham, C. E. (1895). The artiﬁcial spectrum top. Nature 2:321.
Bialek, W., Rieke, F., van Stevenink, R. R., and de Ruyter, W. (1991). Reading a
neural code. Science 252, 1854–1856. doi: 10.1126/science.2063199
Bieler, M., Sieben, K., Cichon, N., Schildt, S., Roder, B., and Hanganu-Opatz,
I. L. (2017). Rate and temporal coding convey multisensory information in primary
sensory cortices. eNeuro 4, 1–18. doi: 10.1523/ENEURO.0037-17.2017
Bittner, G. D. (1968). Diﬀerentiation of nerve terminals in the crayﬁsh opener
muscle and its functional signiﬁcance. J. Gen. Physiol. 51, 731–758. doi: 10.1085/jgp.
51.6.731
Bizley, J. K., and Walker, K. M. M. (2010). Sensitivity and selectivity of neurons
in the auditory cortex to the pitch, timbre, and location of sounds. Neuroscientist 16,
453–469. doi: 10.1177/1073858410371009
Blake, R., and Lee, S. H. (2005). The role of temporal structure in human vision.
Behav. Cogn. Neurosci. Rev. 4, 21–42. doi: 10.1177/1534582305276839
Blanc, J. L., and Coq, J. O. (2007). Coding processes involved in the cortical
representation of complex tactile stimuli. J. Physiol. Paris 101, 22–31. doi: 10.1016/j.
jphysparis.2007.10.004
Bokiniec, P., Zampieri, N., Lewin, G. R., and Poulet, J. F. (2018). The neural circuits
of thermal perception. Curr. Opin. Neurobiol. 52, 98–106. doi: 10.1016/j.conb.2018.
04.006
Boring, E. G. (1942). Sensation and perception in the history of experimental
psychology. New York, NY: Appleton-Century-Crofts.
Borst, A., and Theunissen, F. E. (1999). Information theory and neural coding. Nat.
Neurosci. 2, 947–957. doi: 10.1038/14731
Bower, T. G. R. (1974). “The evolution of sensory systems, ” in Perception: Essays
in Honor of James J. Gibson , eds R. B. MacLeod and H. Pick Jr. (Ithaca, NY: Cornell
University Press), 141–152.
Bullock, T. H. (1982). Electroception. Ann. Rev. Neurosci. 5, 121–170. doi: 10.1146/
annurev.ne.05.030182.001005
Bullock, T. H. (1992). “Introduction to induced rhythms: A widespread,
heterogeneous class of oscillations, ” in Induced rythms of the brain , ed. T. H. Bullock
(Boston, MA: Birkhäuser), 1–28.
Buzsáki, G. (2006). Rhythms of the brain. Oxford: Oxford University Press.
Callier, T., Gitchell, T., Harvey, M. A., and Bensmaia, S. J. (2024). Disentangling
temporal and rate codes in the primate somatosensory cortex. J. Neurosci.
44:e0036242024. doi: 10.1523/JNEUROSCI.0036-24.2024
Cariani, P. (1995). “As if time really mattered: Temporal strategies for neural
coding of sensory information, ” inCommunication and cognition –artiﬁcial intelligence
(CC-AI), Vol. 12, ed. K. Pribram (Hillsdale, NJ: Lawrence Erlbaum), 161–229.
Cariani, P. (1999). Temporal coding of periodicity pitch in the auditory system: An
overview. Neural Plast. 6, 147–172. doi: 10.1155/NP.1999.147
Cariani, P. (2001a). “Neural timing nets for auditory computation, ” in
Computational models of auditory function , eds S. Greenberg and M. Slaney
(Amsterdam: IOS Press), 235–249.
Cariani, P. (2001b). Temporal coding of sensory information in the brain. Acoust.
Sci. Tech. 22, 77–84. doi: 10.1250/ast.22.77
Cariani, P. (2001c). Neural timing nets. Neural Netw. 14, 737–753. doi: 10.1016/
S0893-6080(01)00056-9
Cariani, P. (2004). Temporal codes and computations for sensory representation
and scene analysis. IEEE Trans. Neural Netw. 15, 1100–1111. doi: 10.1109/TNN.2004.
833305
Cariani, P. (2011). Jeﬀress model. Scholarpedia 6:2920. doi: 10.4249/scholarpedia.
2920
Cariani, P. (2019). “Musical intervals, scales, and tunings: AUDITORY
representations and neural codes, ” in Foundations in music psychology: Theory
and research , eds P. J. Rentfrow and D. J. Levitin (Cambridge, MA: MIT Press),
149–218.
Cariani, P., and Baker, J. M. (2022). Time is of the essence: Neural codes,
synchronies, oscillations, architectures. Front. Comput. Neurosci. 16:898829. doi: 10.
3389/fncom.2022.898829
Cariani, P., and Delgutte, B. (1993). Interspike interval distributions of auditory
nerve ﬁbers in response to concurrent vowels with same and diﬀerent fundamental
frequencies. Assoc. Res. Otolaryngol. 16:373.
Cariani, P., and Delgutte, B. (1996). Neural correlates of the pitch of complex
tones. I. Pitch and pitch salience. II. Pitch shift, pitch ambiguity, phase-invariance,
pitch circularity, and the dominance region for pitch. J. Neurophysiol. 76, 1698–1734.
doi: 10.1152/jn.1996.76.3.1717
Frontiers in Computational Neuroscience 23 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 24
Cariani and Baker 10.3389/fncom.2025.1571109
Cariani, P., and Micheyl, C. (2012). “Towards a theory of information processing
in the auditory cortex, ” in Human auditory cortex: Springer handbook of auditory
research, eds D. Poeppel, T. Overath, and A. Popper (New York, NY: Springer),
351–390.
Carney, T., Silverstein, D. A., and Klein, S. A. (1995). Vernier acuity during image
rotation and translation: Visual performance limits. Vis. Res. 35, 1951–1964. doi:
10.1016/0042-6989(94)00288-W
Carr, C. E. (1993a). Organization of the nucleus magnocellularis and the nucleus
laminaris in the barn owl: Encdoding and measuring interaural time diﬀerences.
J. Comp. Neurol. 334, 337–355. doi: 10.1002/cne.903340302
Carr, C. E. (1993b). Processing of temporal information in the brain. Annu. Rev.
Neurosci. 16, 223–243. doi: 10.1146/annurev.ne.16.030193.001255
Carr, C. E., and Konishi, M. (1990). A circuit for detection of interaural time
diﬀerences in the brain stem of the barn owl. J. Neurosci. 10, 3227–3246. doi: 10.1523/
JNEUROSCI.10-10-03227.1990
Carr, C. E., and Soares, D. (2002). Evolutionary convergence and shared
computational principles in the auditory system. Brain Behav. Evol. 59, 294–311.
doi: 10.1159/000063565
Carr, C. E., Heiligenberg, W., and Rose, G. J. (1986). A time-comparison circuit
in the electric ﬁsh midbrain. I. Behavior and physiology. J. Neurosci. 6, 107–119.
doi: 10.1523/JNEUROSCI.06-05-01372.1986
Carr, C. E., Soares, D., Parameshwaran, S., and Perney, T. (2001). Evolution and
development of time coding systems.Curr. Opin. Neurobiol.11, 727–733. doi: 10.1016/
s0959-4388(01)00276-8
Casseday, J. H., and Covey, E. (1995). “Mechanisms for analysis of auditory temporal
patterns in the brainstem of echolocating bats, ” in Neural representation of temporal
patterns, eds E. Covey, H. L. Hawkins, and R. F. Port (New York, NY: Plenum), 25–51.
Chait, M., Greenberg, S., Arai, T., Simon, J. Z., and Poeppel, D. (2015). Multi-time
resolution analysis of speech: Evidence from psychophysics. Front. Neurosci. 9:214.
doi: 10.3389/fnins.2015.00214
Chong, E., and Rinberg, D. (2018). Behavioral readout of spatio-temporal codes in
olfaction. Curr. Opin. Neurobiol. 52, 18–24. doi: 10.1016/j.conb.2018.04.008
Chong, E., Moroni, M., Wilson, C., Shoham, S., Panzeri, S., and Rinberg, D.
(2020). Manipulating synthetic optogenetic odors reveals the coding logic of olfactory
perception. Science 368:aba2357. doi: 10.1126/science.aba2357
Chung, S. H., Lettvin, J. Y., and Raymond, S. A. (1974). Proceedings: The CLOOGE:
A simple device for interspike interval analysis. J. Physiol. 239, 63–66.
Chung, S. H., Raymond, S. A., and Lettvin, J. Y. (1970). Multiple meaning in single
visual units. Brain Behav. Evol. 3, 72–101. doi: 10.1159/000125464
Cohen, J., and Gordon, D. A. (1949). The prevost-Fechner-Benham subjective
colors. Psychol. Bull. 46, 97–136. doi: 10.1037/h0060841
Colburn, S. (1996). “Computational models of binaural processing, ” in Auditory
computation, eds H. Hawkins, T. McMullin, A. N. Popper, and R. R. Fay (New York,
NY: Springer Verlag).
Coppola, D., and Purves, D. (1996). The extraordinarily rapid disappearance of
entoptic images. Proc. Natl. Acad. Sci. U.S.A. 93, 8001–8004. doi: 10.1073/pnas.93.15.
8001
Covey, E. (1980). Temporal neural coding in gustation . Ph.D. thesis. Durham, NC:
Duke University.
Covey, E. (2005). Neurobiological specializations in echolocating bats. Anat. Rec.
A Discov. Mol. Cell. Evol. Biol. 287, 1103–1116. doi: 10.1002/ar.a.20254
Covey, E., Hawkins, H. L., and Port, R. F. (eds) (1995). Neural representation of
temporal patterns. New York, NY: Plenum Press.
Curthoys, I. S., MacDougall, H. G., Vidal, P. P., and de Waele, C. (2017). Sustained
and transient vestibular systems: A physiological basis for interpreting vestibular
function. Front. Neurol. 8:117. doi: 10.3389/fneur.2017.00117
Dahlbom, D. A., and Braasch, J. (2020). How to pick a peak: Pitch and peak shifting
in temporal models of pitch perception. J. Acoust. Soc. Am. 147:2713. doi: 10.1121/10.
0001134
de Cheveigné, A. (2005). “Pitch perception models, ” in Pitch neural coding and
perception, eds C. J. Plack, A. J. Oxenham, R. Fay, and A. N. Popper (New York, NY:
Springer), 169–233.
de Valois, R. L., and de Valois, K. K. (1990).Spatial vision. Oxford: Oxford University
Press.
Delorme, A., and Thorpe, S. J. (2001). Face identiﬁcation using one spike per neuron:
Resistance to image degradations. Neural Netw. 14, 795–803. doi: 10.1016/s0893-
6080(01)00049-1
Dennler, N., Drix, D., Warner, T. P. A., Rastogi, S., Casa, C. D., Ackels, T.,
et al. (2024). High-speed odor sensing using miniaturized electronic nose. Sci. Adv.
10:ead1764. doi: 10.1126/sciadv.adp1764
Di Lorenzo, P. M. (1989). Across unit patterns in the neural response to taste: Vector
space analysis. J. Neurophysiol. 62, 823–833. doi: 10.1152/jn.1989.62.4.823
Di Lorenzo, P. M. (2000). The neural code for taste in the brain stem: Response
proﬁles. Physiol Behav 69, 87–96. doi: 10.1016/s0031-9384(00)00191-8
Di Lorenzo, P. M. (2021). Taste: A scattered aﬀair. Curr. Biol. 31, R74–R76. doi:
10.1016/j.cub.2020.12.003
Di Lorenzo, P. M., and Hecht, G. S. (1993). Perceptual consequences of electrical
stimulation in the gustatory system. Behav. Neurosci. 107, 130–138.
Di Lorenzo, P. M., and Schwartzbaum, J. S. (1982). Coding of gustatory
information in the pontine parabrachial nuclei of the rabbit: Temporal patterns
of neural response. Brain Res. 251, 245–257. doi: 10.1016/0006-8993(82)
90742-9
Di Lorenzo, P. M., Leshchinskiy, S., Moroney, D. N., and Ozdoba, J. M. (2009).
Making time count: Functional evidence for temporal coding of taste sensation.Behav.
Neurosci. 123, 14–25. doi: 10.1037/a0014176
Dimitrov, A. G., Lazar, A. A., and Victor, J. D. (2011). Information theory in
neuroscience. J. Comput. Neurosci. 30, 1–5. doi: 10.1007/s10827-011-0314-3
Ditchburn, R. W., and Ginsborg, B. L. (1952). Vision with a stabilized retinal image.
Nature 170, 178–194. doi: 10.1038/170036a0
Doetsch, G. S. (2000). Patterns in the brain: Neuronal population coding in the
somatosensory system. Physiol. Behav. 69, 87–201. doi: 10.1016/s0031-9384(00)0
0201-8
Dorries, K. M., and Kauer, J. S. (2000). Relationships between odor-elicited
oscillations in the salamander olfactory epithelium and olfactory bulb.J. Neurophysiol.
83, 754–765. doi: 10.1152/jn.2000.83.2.754
Douglas, R., Mahowald, M., and Mead, C. (1995). Neuromorphic analogue VLSI.
Annu. Rev. Neurosci. 18, 255–281. doi: 10.1146/annurev.ne.18.030195.001351
Durlach, N. I., and Colburn, H. S. (1978). “Binaural phenomena, ” in Handbook of
perception, eds E. C. Carterette and M. P. Friedman (New York, NY: Academic Press).
Eckhorn, R. (1991). “Stimulus-speciﬁc synchronization in the visual cortex: Linking
of local features into global ﬁgures?” in Neuronal cooperativity, ed. J. Kruger (Berlin:
Springer-Verlag), 184–224.
Eckhorn, R., and Reitboeck, H. (1990). “Stimulus-speciﬁc synchronization in cat
visual cortex and its possible roles in visual pattern recognition, ” in Synergetics of
cognition, eds H. Haken and M. Stadler (Berlin: Springer-Verlag), 99–111.
Egelhaaf, M., and Borst, A. (1993). A look into the cockpit of the ﬂy: Visual
orientation, algorithms, and identiﬁed neurons. J. Neurosci. 13, 4563–4574. doi: 10.
1523/JNEUROSCI.13-11-04563.1993
Emmers, R. (1966a). Modulation of the thalamic relay of taste by stimulation of the
tongue with ice water. Exp. Neurol. 16, 50–56. doi: 10.1016/0014-4886(66)90085-9
Emmers, R. (1966b). Separate relays of tactile, pressure, thermal, and gustatory
modalities in the cat thalamus. Proc. Soc. Exp. Biol. Med. 121, 527–531. doi: 10.3181/
00379727-121-30821
Emmers, R. (1969). “Modality coding of lingual aﬀerents in the cat thalamus, ” in
Proceedings of the 3rd Symposium: Olfaction and taste, ed. C. Pfaﬀman (New York, NY:
Rockefeller University Press), 517–526.
Emmers, R. (1970). Modiﬁcations of sensory modality codes by stimuli of graded
intensity in the cat thalamus. Brain Res. 21, 91–104. doi: 10.1016/0006-8993(70)9
0023-5
Emmers, R. (1976). Thalamic mechanisms that process a temporal pulse code for
pain. Brain Res. 103, 425–441. doi: 10.1016/0006-8993(76)90442-x
Emmers, R. (1981). Pain: A spike-interval coded message in the brain. New York, NY:
Raven Press.
Eskandar, E. N., Optican, L. M., and Richmond, B. J. (1992). Role of inferior
temporal neurons in visual memory. II. Multiplying temporal waveforms related to
vision and memory. J. Neurophysiol. 68, 1296–1306. doi: 10.1152/jn.1992.68.4.1296
Festinger, L., Allyn, M. R., and White, C. W. (1971). The perception of color with
achromatic stimulation. Vision Res. 11, 591–612.
Fetz, E. E. (1997). Temporal coding in neural populations? Science 278, 1901–1902.
doi: 10.1126/science.278.5345.1901
Fiorentini, A., and MacKay, D. M. (1965). Temporal factors in pattern vision.Quart.
J. Exp. Psychol. 40, 282–291. doi: 10.1152/jn.1992.68.4.1277
Fogerty, D., Ahlstrom, J. B., and Dubno, J. R. (2023). Sentence recognition with
modulation-ﬁltered speech segments for younger and older adults: Eﬀects of hearing
impairment and cognition. J. Acoust. Soc. Am. 154, 3328–3343. doi: 10.1121/10.
0022445
Freeman, W. J. (1975). Mass action in the nervous system. New York, NY: Academic
Press.
Friedrich, R. W., and Laurent, G. (2001). Dynamic optimization of odor
representations by slow temporal patterning of mitral cell activity. Science 291, 889–
894. doi: 10.1126/science.291.5505.889
Fukushima, K., Y amaguchi, Y., Y asuda, M., and Nagata, S. (1970). An electronic
model of the retina. Proc. IEEE 58, 1950–1951. doi: 10.1109/PROC.1970.8066
Frontiers in Computational Neuroscience 24 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 25
Cariani and Baker 10.3389/fncom.2025.1571109
Fusi, S., Miller, E. K., and Rigotti, M. (2016). Why neurons mix: High dimensionality
for higher cognition.Curr. Opin. Neurobiol.37, 66–74. doi: 10.1016/j.conb.2016.01.010
Gamzu, E., and Ahissar, E. (2001). Importance of temporal cues for tactile spatial-
frequency discrimination. J. Neurosci. 21, 7416–7427. doi: 10.1523/JNEUROSCI.21-
18-07416.2001
Gautrais, J., and Thorpe, S. (1998). Rate coding versus temporal order coding: A
theoretical approach. Biosystems 48, 57–65. doi: 10.1016/s0303-2647(98)00050-1
Gawne, T. J. (1999). Temporal coding as a means of information transfer in the
primate visual system. Crit. Rev. Neurobiol. 13, 83–101. doi: 10.1615/critrevneurobiol.
v13.i1.40
Gerstein, G. L. (2004). Searching for signiﬁcance in spatio-temporal ﬁring patterns.
Acta Neurobiol. Exp. 64, 203–207. doi: 10.55782/ane-2004-1506
Gerstner, W. (1999). “Spiking neurons, ” in Pulsed neural networks , eds W. Maass
and C. M. Bishop (Cambridge, MA: MIT Press), xiii–xxvi.
Gerstner, W., Kreiter, A. K., Markram, H., and Herz, A. V. (1997). Neural codes:
Firing rates and beyond. Proc Natl Acad Sci U S A94, 12740–12741. doi: 10.1073/pnas.
94.24.12740
Gesteland, R. C., Lettvin, J. Y., Pitts, W. H., and Chung, S. H. (1968). “A code in
the nose, ” in Cybernetic problems in bionics , eds H. L. Oestereicher and D. R. Moore
(New York, NY: Gordon and Breach), 313–322.
Ghitza, O. (1988). Temporal non-place information in the auditory-nerve ﬁring
patterns as a front-end for speech recognition in a noisy environment. J. Phonetics
16, 109–123. doi: 10.1016/S0095-4470(19)30469-3
Ghitza, O. (1992). “Auditory nerve representation as a basis for speech processing, ”
in Advances in speech signal processing, eds S. Furui and M. M. Sondhi (New York, NY:
Marcel Dekker), 453–485.
Ghitza, O. (2011). Linking speech perception and neurophysiology: Speech
decoding guided by cascaded oscillators locked to the input rhythm. Front. Psychol.
2:130. doi: 10.3389/fpsyg.2011.00130
Ghitza, O., Giraud, A. L., and Poeppel, D. (2012). Neuronal oscillations and speech
perception: Critical-band temporal envelopes are the essence. Front. Hum. Neurosci.
6:340. doi: 10.3389/fnhum.2012.00340
Glendinning, J. I., Davis, A., and Rai, M. (2006). Temporal coding mediates
discrimination of “bitter” taste stimuli by an insect. J. Neurosci. 26, 8900–8908. doi:
10.1523/JNEUROSCI.2351-06.2006
Gockel, H. E., and Carlyon, R. P. (2016). On Zwicker tones and musical pitch in
the likely absence of phase locking corresponding to the pitch. J. Acoust. Soc. Am.
140:2257. doi: 10.1121/1.4963865
Goldstein, J. L., and Srulovicz, P. (1977). “Auditory-nerve spike intervals as an
adequate basis for aural frequency measurement, ” in Psychophysics and physiology of
hearing, eds E. F. Evans and J. P. Wilson (London: Academic Press), 337–347.
Gollisch, T., and Meister, M. (2008). Rapid neural coding in the retina with relative
spike latencies. Science 319, 1108–1111. doi: 10.1126/science.1149639
Graham, C. H. (1966). “Visual space perception, ” inVision and visual perception, ed.
C. H. Graham (New York, NY: John Wiley).
Gray, C. M. (1999). The temporal correlation hypothesis of visual feature
integration: Still alive and well. Neuron 31-47, 111–125. doi: 10.1016/s0896-6273(00)
80820-x
Gray, C. M., Engel, A. K., Konig, P., and Singer, W. (1992). Synchronization of
oscillatory neuronal responses in cat striate cortex: Temporal properties.Vis. Neurosci.
8, 337–347. doi: 10.1017/s0952523800005071
Gray, C. M., Konig, P., Engel, A. K., and Singer, W. (1989). Oscillatory responses in
cat visual cortex exhibit inter-columnar synchronization which reﬂects global stimulus
properties. Nature 338, 334–337. doi: 10.1038/338334a0
Green, B. G. (2004). Temperature perception and nocioception. J. Neurobiol. 61,
13–29. doi: 10.1002/neu.20081
Griﬃn, L. R. (1968). Color TV – That isn’t: Optical illusion creates color impression
in viewer’s mind. Pop. Sci. 5, 73–76.
Grothe, B. (2003). New roles for synaptic inhibition in sound localization. Nat. Rev.
Neurosci. 4, 1–11. doi: 10.1038/nrn1136
Grothe, B. (2018). How the barn owl computes auditory space. Trends Neurosci. 41,
115–117. doi: 10.1016/j.tins.2018.01.004
Grothe, B., Pecka, M., and McAlpine, D. (2010). Mechanisms of sound localization
in mammals. Physiol. Rev. 90, 983–1012. doi: 10.1152/physrev.00026.2009
Gur, M. (2024). Seeing on the ﬂy: Physiological and behavioral evidence show that
space-to-space representation and processing enable fast and eﬃcient performance by
the visual system. J. Vis. 24:11. doi: 10.1167/jov.24.11.11
Gutig, R., Gollisch, T., Sompolinsky, H., and Meister, M. (2013). Computing
complex visual features with retinal spike times. PLoS One 8:e53063. doi: 10.1371/
journal.pone.0053063
Haddad, R., Khan, R., Takahashi, Y. K., Mori, K., Harel, D., and Sobel, N. (2008). A
metric for odorant comparison. Nat. Methods 5, 425–429. doi: 10.1038/nmeth.1197
Haddad, R., Lanjuin, A., Madisen, L., Zeng, H., Murthy, V. N., and Uchida, N.
(2013). Olfactory cortical neurons read out a relative time code in the olfactory bulb.
Nat. Neurosci. 16, 949–957. doi: 10.1038/nn.3407
Haddad, R., Weiss, T., Khan, R., Nadler, B., Mandairon, N., Bensaﬁ, M., et al. (2010).
Global features of neural activity in the olfactory system form a parallel code that
predicts olfactory behavior and perception. J. Neurosci. 30, 9017–9026. doi: 10.1523/
JNEUROSCI.0398-10.2010
Hallock, R. M., and Di Lorenzo, P. M. (2006). Temporal coding in the gustatory
system. Neurosci. Biobehav. Rev. 30, 1145–1160. doi: 10.1016/j.neubiorev.2006.07.005
Han, C., Wang, T., Y ang, Y., Wu, Y., Li, Y., Dai, W., et al. (2021). Multiple gamma
rhythms carry distinct spatial frequency information in primary visual cortex. PLoS
Biol. 19:e3001466. doi: 10.1371/journal.pbio.3001466
Harvey, M. A., Saal, H. P., Dammann, J. F. III, and Bensmaia, S. J. (2013).
Multiplexing stimulus information through rate and temporal codes in primate
somatosensory cortex. PLoS Biol. 11:e1001558. doi: 10.1371/journal.pbio.1001558
Heil, P. (1997). Auditory cortical onset responses revisited. I. First-spike timing.
J. Neurophysiol. 77, 2616–2641. doi: 10.1152/jn.1997.77.5.2616
Heil, P. (2004). First-spike latency of auditory neurons revisited. Curr. Opin.
Neurobiol. 14, 461–467. doi: 10.1016/j.conb.2004.07.002
Heiligenberg, W. (1989). Coding and processing of electrosensory information in
gymnotiform ﬁsh. J. Exp. Biol. 146, 255–275. doi: 10.1242/jeb.146.1.255
Heiligenberg, W. (1994). “The coding and processing of temporal information in
the electrosensory system of the ﬁsh, ” in Temporal coding in the brain, eds G. Buzaki,
R. Llinas, W. Singer, A. Berthoz, and Y. Christen (Berlin: Springer-Verlag), 1–12.
Heiligenberg, W. F. (1991). Neural nets in electric ﬁsh. Cambridge, MA: MIT Press.
Heinz, M. G., Colburn, H. S., and Carney, L. H. (2001). Evaluating auditory
performance limits: I. One-parameter discrimination using a computational model
for the auditory nerve. Neural Comput. 13, 2273–2316. doi: 10.1162/0899766017505
4180
Helmholtz, H. V. (1885). On the Sensations of tone as a physiological basis for the
theory of music (1954 Reprint). New York, NY: Dover.
Hopﬁeld, J. J. (1995). Pattern recognition computation using action potential timing
for stimulus representation. Nature 376, 33–36. doi: 10.1038/376033a0
Hopkins, C. D. (1988). Neuroethology of electric communication. Ann. Rev.
Neurosci. 11, 497–535. doi: 10.1146/annurev.ne.11.030188.002433
Howard, M. W. (2024). “Memory for time, ” inOxford handbook of human memory,
eds M. J. Kahana and A. D. Wagner (Oxford: Oxford University Press), 436–456.
Hu, Y., Shan, W. Q., Wu, B., and Liu, T. (2021). New insight into the origins of itch
and pain: How are itch and pain signals coded and discriminated by primary sensory
neurons? Neurosci. Bull. 37, 575–578. doi: 10.1007/s12264-021-00643-6
Hutchinson, M. (1991). Megabrain. New York, NY: Ballantine.
Ikoma, A., Steinhoﬀ, M., Stander, S., Yosipovitch, G., and Schmelz, M. (2006). The
neurobiology of itch. Nat. Rev. Neurosci. 7, 535–547. doi: 10.1038/nrn1950
Indiveri, G., and Horiuchi, T. K. (2011). Frontiers in neuromorphic engineering.
Front. Neurosci. 5:118. doi: 10.3389/fnins.2011.00118
Indiveri, G., Linares-Barranco, B., Hamilton, T. J., van Schaik, A., Etienne-
Cummings, R., Delbruck, T., et al. (2011). Neuromorphic silicon neuron circuits.
Front. Neurosci. 5:73. doi: 10.3389/fnins.2011.00073
It¯o, F. (1992). Comparative aspects of mechanoreceptor systems . New York, NY:
Springer-Verlag.
Jacobs, A. L., Fridman, G., Douglas, R. M., Alam, N. M., Latham, P. E., Prusky, G. T.,
et al. (2009). Ruling out and ruling in neural codes. Proc. Natl. Acad. Sci. U.S.A. 106,
5936–5941. doi: 10.1073/pnas.0900573106
Jadhav, S. P., Wolfe, J., and Feldman, D. E. (2009). Sparse temporal coding of
elementary tactile features during active whisker sensation.Nat. Neurosci.12, 792–800.
doi: 10.1038/nn.2328
Jazayeri, M., and Afraz, A. (2017). Navigating the neural space in search of the neural
code. Neuron 93, 1003–1014. doi: 10.1016/j.neuron.2017.02.019
Jeﬀress, L. A. (1948). A place theory of sound localization. J. Comp. Physiol. Psychol.
41, 35–39. doi: 10.1037/h0061495
Jezzini, A., Mazzucato, L., La Camera, G., and Fontanini, A. (2013). Processing
of hedonic and chemosensory features of taste in medial prefrontal and
insular networks. J. Neurosci. 33, 18966–18978. doi: 10.1523/JNEUROSCI.2974-
13.2013
Johnson, K. O., and Hsiao, S. S. (1992). Neural mechanisms of tactual form and
texture perception. Annu. Rev. Neurosci. 15, 227–250. doi: 10.1146/annurev.ne.15.
030192.001303
Jones, L. M., Depireux, D. A., Simons, D. J., and Keller, A. (2004). Robust temporal
coding in the trigeminal system.Science 304, 1986–1989. doi: 10.1126/science.1097779
Jordan, R., Kollo, M., and Schaefer, A. T. (2018). Sniﬃng fast: Paradoxical eﬀects on
odor concentration discrimination at the levels of olfactory bulb output and behavior.
eNeuro 5, 1–18. doi: 10.1523/ENEURO.0148-18.2018
Frontiers in Computational Neuroscience 25 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 26
Cariani and Baker 10.3389/fncom.2025.1571109
Joris, P. X., Louage, D. H., Cardoen, L., and van der Heijden, M. (2006). Correlation
index: A new metric to quantify temporal coding. Hear. Res. 21, 19–30. doi: 10.1016/j.
heares.2006.03.010
Kabrisky, M. (1967). “A proposed model for visual information processing in the
brain, ” inModels for the perception of speech and visual forms , ed. W. Wathen-Dunn
(Cambridge, MA: MIT Press), 354–361.
Katz, D. B. (2005). The many ﬂavors of temporal coding in gustatory cortex. Chem
Senses 30, i80–i81. doi: 10.1093/chemse/bjh123
Kauer, J. S. (1990). “Temporal patterns of membrane potential in the olfactory
bulb observed with intracellular recording and voltage-dye imaging: Early
hyperpolarization, ” in Chemosensory information processing , ed. D. Schild (Berlin:
Springer Verlag), 305–313.
Kauer, J. S. (1998). Olfactory processing: A time and place for everything.Curr. Biol.
8, R282–R283. doi: 10.1016/s0960-9822(98)70173-3
Kauer, J. S. (2002). On the scents of smell in the salamander. Nature 417, 336–342.
doi: 10.1038/417336a
Kauer, J. S., and White, J. (2001). Imaging and coding in the olfactory system.Annu.
Rev. Neurosci. 24, 963–979. doi: 10.1146/annurev.neuro.24.1.963
Kay, L. M., Beshel, J., Brea, J., Martin, C., Rojas-Libano, D., and Kopell, N. (2009).
Olfactory oscillations: The what, how and what for. Trends Neurosci. 32, 207–214.
doi: 10.1016/j.tins.2008.11.008
Kayser, C., Logothetis, N. K., and Panzeri, S. (2010). Millisecond encoding precision
of auditory cortex neurons. Proc. Natl. Acad. Sci. U.S A. 107, 16976–16981. doi:
10.1073/pnas.1012656107
Keidel, W. (1984). “The sensory detection of vibrations, ” in Foundations of sensory
science, eds W. W. Dawson and J. M. Enoch (Berlin: Springer-Verlag), 465–512.
Keidel, W. D. (1968). “Electrophysiology of vibratory percpetion, ” in Contributions
to sensory physiology, ed. W. D. Neﬀ (New York, NY: Academic Press), 3.
Kimura, K., and Beidler, L. M. (1961). Microelectrode study of taste receptors of rat
and hamster. J. Cell. Comp. Physio.l 58, 131–139. doi: 10.1002/jcp.1030580204
Kloppenburg, P., and Nawrot, M. P. (2014). Neural coding: Sparse but on time.Curr.
Biol. 24, R957–R959. doi: 10.1016/j.cub.2014.08.041
Knutsen, P. M., and Ahissar, E. (2009). Orthogonal coding of object location.Trends
Neurosci. 32, 101–109. doi: 10.1016/j.tins.2008.10.002
Knutsen, P. M., Pietr, M., and Ahissar, E. (2006). Haptic object localization in the
vibrissal system: Behavior and performance. J. Neurosci. 26, 8451–8464. doi: 10.1523/
JNEUROSCI.1516-06.2006
Konig, P., Engel, A. K., Roelfsema, P. R., and Singer, W. (1995). How precise is
neuronal synchronization? Neural Comput. 7, 469–485. doi: 10.1162/neco.1995.7.3.
469
Kopell, N., Börgers, C., Pervouchine, D., Malerba, P., and Tort, A. B. (2010a).
“Gamma and theta rhythms in biophysical models of hippocampal circuits, ” in
Hippocampal microcircuits: A computational modeler’s resource book, ed. V. Cutsuridis
(New York, NY: Springer), 423–457.
Kopell, N., Kramer, M. A., Malerba, P., and Whittington, M. A. (2010b). Are
diﬀerent rhythms good for diﬀerent functions? Front. Hum. Neurosci. 4:187. doi:
10.3389/fnhum.2010.00187
Koppl, C. (1997). Phase locking to high frequencies in the auditory nerve and
cochlear nucleus magnocellularis of the barn owl, Tyto alba . J. Neurosci. 17, 3312–
3321. doi: 10.1523/JNEUROSCI.17-09-03312.1997
Kozak, W. M., and Reitboeck, H. J. (1974). Color-dependent distribution of spikes
in single optic tract ﬁbers of the cat. Vis. Res. 14, 405–419. doi: 10.1016/0042-6989(74)
90239-9
Kozak, W. M., Reitboeck, H. J., and Meno, F. (1989). “Subjective color sensations
elicited by moving patterns: Eﬀect of luminance, ” in Seeing contour and colour ,
eds J. J. Kulikowski and C. M. Dickenson (New York, NY: Pergamon Press),
294–310.
Krumm, B., Klump, G. M., Koppl, C., and Langemann, U. (2019). The barn owls’
minimum audible angle. PLoS One 14:e0220652. doi: 10.1371/journal.pone.0220652
Kuang, X., Poletti, M., Victor, J. D., and Rucci, M. (2012). Temporal encoding of
spatial information during active visual ﬁxation. Curr. Biol. 22, 510–514. doi: 10.1016/
j.cub.2012.01.050
Kudithipudi, D., Schuman, C., Vineyard, C. M., Pandit, T., Merkel, C., Kubendran,
R., et al. (2025). Neuromorphic computing at scale.Nature 637, 801–812. doi: 10.1038/
s41586-024-08253-8
Ladegaard, M., Mulsow, J., Houser, D. S., Jensen, F. H., Johnson, M., Madsen,
P. T., et al. (2019). Dolphin echolocation behaviour during active long-range target
approaches. J. Exp. Biol. 222:9217. doi: 10.1242/jeb.189217
Langner, G. (1992). Periodicity coding in the auditory system. Hear. Res. 60,
115–142. doi: 10.1016/0378-5955(92)90015-f
Lankarany, M., Al-Basha, D., Ratte, S., and Prescott, S. A. (2019). Diﬀerentially
synchronized spiking enables multiplexed neural coding. Proc. Natl. Acad. Sci. U.S.A.
116, 10097–10102. doi: 10.1073/pnas.1812171116
Lanska, D. J., Lanska, J. M., and Remler, B. F. (2015). Description and clinical
application of the Pulfrich eﬀect. Neurology 84, 2274–2278. doi: 10.1212/WNL.
0000000000001646
Laurent, G. (1999). A systems perspective on early olfactory coding. Science 286,
723–728. doi: 10.1126/science.286.5440.723
Laurent, G. (2002). Olfactory network dynamics and the coding of
multidimensional signals. Nat. Rev. Neurosci. 3, 884–895. doi: 10.1038/nrn964
Laurent, G., MacLeod, K., Stopfer, M., and Wehr, M. (1998). Spatiotemporal
structure of olfactory inputs to the mushroom bodies. Learn. Mem. 5, 124–132.
Laurent, G., Wehr, M., and Davidowitz, H. (1996). Temporal representations of
odors in an olfactory network. J. Neurosci. 16, 3837–3847. doi: 10.1523/JNEUROSCI.
16-12-03837.1996
Lazar, A. A., and Pnevmatikakis, E. A. (2011). Video time encoding machines. IEEE
Trans. Neural Netw. 22, 461–473. doi: 10.1109/TNN.2010.2103323
Lazar, A. A., and Tóth, L. T. (2004). Perfect recovery and sensitivity analysis of time
encoded bandlimited signals.IEEE Trans. Circ. Syst.51, 2060–2073. doi: 10.1109/TCSI.
2004.835026
Lazar, A. A., Liu, T., and Yeh, C. H. (2023). The functional logic of odor information
processing in the Drosophila antennal lobe. PLoS Comput. Biol. 19:e1011043. doi:
10.1371/journal.pcbi.1011043
Lazar, A. A., Slutskiy, Y. B., and Zhou, Y. (2015). Massively parallel neural circuits
for stereoscopic color vision: Encoding, decoding and identiﬁcation. Neural Netw. 63,
254–271. doi: 10.1016/j.neunet.2014.10.014
Lazzaro, J., and Mead, C. (1989). Silicon modeling of pitch perception. Proc. Nat.
Acad. Sci. U.S.A. 86, 9597–9601. doi: 10.1073/pnas.86.23.9597
Lee, K. S., Loutit, A. J., de Thomas Wagner, D., Sanders, M., Prsa, M., and Huber, D.
(2024). Transformation of neural coding for vibrotactile stimuli along the ascending
somatosensory pathway. Neuron 112:3343–3353.e3347. doi: 10.1016/j.neuron.2024.07.
005
Lee, S. H., and Blake, R. (1999a). Detection of temporal structure depends on spatial
structure. Vis. Res. 39, 3033–3048. doi: 10.1016/s0042-6989(98)00333-2
Lee, S. H., and Blake, R. (1999b). Visual form created solely from temporal structure.
Science 284, 1165–1168. doi: 10.1126/science.284.5417.1165
Leman, M., and Carreras, F. (1997). “Schema and gestalt: Testing the hypothesis of
psychoneural isomorphism by computer simulation, ” inMusic, gestalt, and computing,
ed. M. Leman (Berlin: Springer), 144–165.
Lestienne, R. (1996). Determination of the precision of spike timing in the visual
cortex of anaesthetised cats. Biol. Cybern. 74, 55–61. doi: 10.1007/BF00199137
Lestienne, R. (1999). Intrinsic and extrinsic neuronal mechanisms in temporal
coding: A further look at neuronal oscillations. Neural Plast. 6, 173–189. doi: 10.1155/
NP.1999.173
Lestienne, R., and Tuckwell, H. C. (1998). The signiﬁcance of precisely replicating
patterns in mammalian CNS spike trains. Neuroscience 82, 315–336. doi: 10.1016/
s0306-4522(97)00281-9
Lestienne, R., Gary-Bobo, E., Przybyslawski, J., Saillour, P., and Imbert, M. (1990).
Temporal correlations in modulated evoked responses in the visual cortical cells of the
cat. Biol. Cybern. 62, 425–440. doi: 10.1007/BF00197649
Lettvin, J. Y., and Gesteland, R. C. (1965). Speculations on smell. Cold Spring Harb.
Symp. Quant. Biol. 30, 217–225. doi: 10.1101/sqb.1965.030.01.024
Licklider, J. C. R. (1951a). A duplex theory of pitch perception. Experientia VII,
128–134. doi: 10.1007/BF02156143
Licklider, J. C. R. (1959). “Three auditory theories, ” in Psychology: A study of a
science. Study I. conceptual and systematic, ed. S. Koch (New York, NY: McGraw-Hill),
41–144.
Licklider, J. R. C. (1951b). “Basic correlates of the auditory stimulus, ” in Handbook
of experimental psychology, ed. S. S. Stevens (New York, NY: John Wiley and Sons Inc),
985–1039.
Luczak, A., McNaughton, B. L., and Harris, K. D. (2015). Packet-based
communication in the cortex. Nat. Rev. Neurosci. 16, 745–755. doi: 10.1038/nrn4026
Ma, Q. (2010). Labeled lines meet and talk: Population coding of somatic sensations.
J. Clin. Invest. 120, 3773–3778. doi: 10.1172/JCI43426
Maas, W. (1999). “Computing with spiking neurons, ” in Pulsed neural
networks, eds W. Maas and C. M. Bishop (Cambridge, MA: MIT Press),
xiii–xxvi.
MacKay, D. M., and McCulloch, W. S. (1952). The limiting information
capacity of a neuronal link. Bull. Math. Biophys. 14, 127–135. doi: 10.1007/BF024
77711
MacLeod, K., and Laurent, G. (1996). Distinct mechanisms for synchronization
and temporal patterning of odor-encoding neural assemblies. Science 274, 976–979.
doi: 10.1126/science.274.5289.976
Macrides, F. (1977). “Dynamic aspects of central olfactory processing, ” in Chemical
signals in vertebrates, eds D. M. Schwartze and M. M. Mozell (New York, NY: Plenum),
207–229.
Frontiers in Computational Neuroscience 26 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 27
Cariani and Baker 10.3389/fncom.2025.1571109
Macrides, F., and Chorover, S. L. (1972). Olfactory bulb units: Activity correlated
with inhalation cycles and odor quality. Science 175, 84–86. doi: 10.1126/science.175.
4017.84
Masquelier, T., Hugues, E., Deco, G., and Thorpe, S. J. (2009). Oscillations, phase-
of-ﬁring coding, and spike timing-dependent plasticity: An eﬃcient learning scheme.
J. Neurosci. 29, 13484–13493. doi: 10.1523/JNEUROSCI.2207-09.2009
Mastronarde, D. N. (1989). Correlated ﬁring of retinal ganglion cells. TINS 12,
75–80. doi: 10.1016/0166-2236(89)90140-9
Masuda, N., and Aihara, K. (2007). Dual coding hypotheses for neural information
representation. Math. Biosci. 207, 312–321. doi: 10.1016/j.mbs.2006.09.009
Mathis, M. W., Perez Rotondo, A., Chang, E. F., Tolias, A. S., and Mathis, A. (2024).
Decoding the brain: From neural representations to mechanistic models. Cell 187,
5814–5832. doi: 10.1016/j.cell.2024.08.051
Mazor, O., and Laurent, G. (2005). Transient dynamics versus ﬁxed points in odor
representations by locust antennal lobe projection neurons. Neuron 48, 661–673.
doi: 10.1016/j.neuron.2005.09.032
McAlpine, D., and Grothe, B. (2003). Sound localization and delay lines–do
mammals ﬁt the model? Trends Neurosci. 26, 347–350. doi: 10.1016/S0166-2236(03)
00140-1
McClurkin, J. W., and Optican, L. M. (1996). Primate striate and prestriate cortical
neurons during discrimination. I. simultaneous temporal encoding of information
about color and pattern. J. Neurophysiol. 75, 481–495. doi: 10.1152/jn.1996.75.1.481
McClurkin, J. W., Gawne, T. J., Optican, L. M., and Richmond, B. J. (1991a). Lateral
geniculate neurons in behaving primates. II. Encoding of visual information in the
temporal shape of the response. J. Neurophys. 66, 794–308. doi: 10.1152/jn.1991.66.3.
794
McClurkin, J. W., Gawne, T. J., Richmond, B. J., Optican, L. M., and Robinson,
D. L. (1991b). Lateral geniculate neurons in behaving primates. I. Responses to
two-dimensional stimuli. J. Neurophys. 66, 777–793. doi: 10.1152/jn.1991.66.3.777
McClurkin, J. W., Optican, L. M., Richmond, B. J., and Gawne, T. J. (1991c).
Concurrent processing and complexity of temporally encoded neuronal messages in
visual perception. Science 253, 675–677. doi: 10.1126/science.1908118
McClurkin, J. W., Zarbock, J. A., and Optican, L. M. (1993). Neurons in primate
visual cortex multiplex information about red/green, blue/yellow, and black/white
opponencies using temporal codes. Neurosci. Abstr. 19:1576.
McClurkin, J. W., Zarbock, J. A., and Optican, L. M. (1996). Primate striate and
prestriate cortical neurons during discrimination. II. Separable temporal codes for
color and pattern. J. Neurophysiol. 75, 496–507. doi: 10.1152/jn.1996.75.1.496
Mead, C. (1989). Analog VLSI and neural systems. Reading, MA: Addison-Wesley.
Mechler, F., Victor, J. D., Purpura, K. P., and Shapley, R. (1998). Robust temporal
coding of contrast by V1 neurons for transient but not for steady-state stimuli.
J. Neurosci. 18, 6583–6598. doi: 10.1523/JNEUROSCI.18-16-06583.1998
Meddis, R., and Hewitt, M. J. (1991). Virtual pitch and phase sensitivity of a
computer model of the auditory periphery. I. Pitch identiﬁcation II. Phase sensitivity.
J. Acoust. Soc. Am. 89, 2866–2894. doi: 10.1121/1.400725
Meddis, R., Hewitt, M. J., and Shackleton, T. (1990). Implementation details of a
computational model of the inner hair-cell/auditory-nerve synapse.J. Acoust. Soc. Am.
87, 1813–1818. doi: 10.1121/1.399379
Medlock, L., Al-Basha, D., Halawa, A., Dedek, C., Ratte, S., and Prescott, S. A.
(2024). Encoding of vibrotactile stimuli by mechanoreceptors in rodent glabrous skin.
J Neurosci 44, e1252242024. doi: 10.1523/JNEUROSCI.1252-24.2024
Meister, M. (2015). On the dimensionality of odor space. Elife 4:e07865. doi: 10.
7554/eLife.07865
Meredith, M. (1981). The analysis of response similarity in single neurons of the
goldﬁsh olfactory bulb using amino-acids as odor stimuli. Chem. Senses 6, 277–293.
doi: 10.1093/chemse/6.4.277
Meredith, M., and Moulton, D. G. (1978). Patterned response to odor in single
neurones of goldﬁsh olfactory bulb: Inﬂuence of odor quality and other stimulus
parameters. J. Gen Physiol. 71, 615–643. doi: 10.1085/jgp.71.6.615
Mignot, C., Weise, S., Podlesek, D., Leonhardt, G., Bensaﬁ, M., and Hummel, T.
(2024). What do brain oscillations tell about the human sense of smell? J. Neurosci.
Res. 102:e25335. doi: 10.1002/jnr.25335
Ming, C., Haro, S., Simmons, A. M., and Simmons, J. A. (2021). A comprehensive
computational model of animal biosonar signal processing. PLoS Comput. Biol.
17:e1008677. doi: 10.1371/journal.pcbi.1008677
Moore, B. C. J. (2013). An introduction to the psychology of hearing. Leiden: Brill.
Mori, K., and Sakano, H. (2022). Processing of odor information during the
respiratory cycle in mice. Front. Neural Circuits 16:861800. doi: 10.3389/fncir.2022.
861800
Morley, J. W., and Rowe, M. J. (1990). Perceived pitch of vibrotactile
stimuli: Eﬀects of vibration amplitude, and implications for vibration
frequency coding. J. Physiol. 431, 403–416. doi: 10.1113/jphysiol.1990.sp01
8336
Morley, J. W., Archer, J. S., Ferrington, D. G., Rowe, M. J., and Turman, A. B. (1990).
Neural coding of complex tactile vibration: Information processing in mammalian
auditory and tactile systems. New York, NY: Alan R. Liss, Inc, 127–140.
Morrell, F. (1967). “Electrical signs of sensory coding, ” in The neurosciences: A
study program, eds G. C. Quarton, T. Melnechuck, and F. O. Schmitt (New York, NY:
Rockefeller University Press), 452–469.
Moss, C. F., and Schnitzler, H.-U. (1995). “Behavioral studies of auditory
information processing, ” inHearing by bats, eds A. N. Popper and R. R. Fay (New York,
NY: Springer-Verlag), 87–145.
Mountcastle, V. (1967). “The problem of sensing and the neural coding of sensory
events, ” inThe neurosciences: A study program, eds G. C. Quarton, T. Melnechuk, and
F. O. Schmitt (New York, NY: Rockefeller University Press).
Mountcastle, V. (1993). Temporal order determinants in a somatosthetic frequency
discrimination: Sequential order coding. Ann. N. Y. Acad. Sci. 682, 151–170. doi:
10.1196/annals.1360.011
Mountcastle, V. B. (1988). The gordon wilson lecture. Representations and the
construction of reality. Trans. Am. Clin. Climatol. Assoc. 99, 70–90.
Mountcastle, V. B., Steinmetz, M. A., and Romo, R. (1990). Cortical neuronal
periodicities and frequency discrimination in the sense of ﬂutter. Cold Spring Harb.
Symp. Quant. Biol. 55, 861–872. doi: 10.1101/sqb.1990.055.01.081
Mountcastle, V. B., Talbot, W. H., Sakata, H., and Hyvärinen, J. (1969). Cortical
neuronal mechanisms in ﬂutter-vibration studied in unanesthetized monkeys.
Neuronal periodicity and frequency discrimination. J. Neurophysiol. 32, 452–485.
doi: 10.1152/jn.1969.32.3.452
Nozaradan, S. (2014). Exploring how musical rhythm entrains brain activity with
electroencephalogram frequency-tagging. Philos. Trans. R. Soc. Lond. B Biol. Sci.
369:20130393. doi: 10.1098/rstb.2013.0393
Ohla, K., Yoshida, R., Roper, S. D., Di Lorenzo, P. M., Victor, J. D., Boughter, J. D.,
et al. (2019). Recognizing taste: Coding patterns along the neural axis in mammals.
Chem. Senses 44, 237–247. doi: 10.1093/chemse/bjz013
Oram, M. W., Wiener, M. C., Lestienne, R., and Richmond, B. J. (1999). Stochastic
nature of precisely timed spike patterns in visual system neuronal responses.
J. Neurophysiol. 81, 3021–3033. doi: 10.1152/jn.1999.81.6.3021
Pabst, M., Reitboeck, H. J., and Eckhorn, R. (1989). “A model of preattentive
texture region deﬁnition based on texture analysis, ” in Models of brain
function, ed. R. M. J. Cotterill (Cambridge: Cambridge University Press),
137–150.
Palmer, A. R. (1990). The representation of the spectra and fundamental frequencies
of steady-state single- and double-vowel sounds in the temporal discharge patterns of
guinea pig cochlear-nerve ﬁbers. J. Acoust. Soc. Am. 88, 1412–1426. doi: 10.1121/1.
400329
Panzeri, S., Brunel, N., Logothetis, N. K., and Kayser, C. (2009). Sensory neural codes
using multiplexed time scales. Trends Neurosci. 33, 111–120. doi: 10.1016/j.tins.2009.
12.001
Panzeri, S., Harvey, C. D., Piasini, E., Latham, P. E., and Fellin, T. (2017).
Cracking the neural code for sensory perception by combining statistics,
intervention, and behavior. Neuron 93, 491–507. doi: 10.1016/j.neuron.2016.
12.036
Papert, S. (1965). “Introduction, ” in Embodiments of mind , ed. W. S. McCulloch
(Cambridge, MA: MIT Press), xiii–xx.
Peelle, J. E., and Davis, M. H. (2012). Neural oscillations carry speech rhythm
through to comprehension. Front. Psychol. 3:320. doi: 10.3389/fpsyg.2012.00320
Peelle, J. E., Gross, J., and Davis, M. H. (2013). Phase-locked responses to speech
in human auditory cortex are enhanced during comprehension. Cereb. Cortex 23,
1378–1387. doi: 10.1093/cercor/bhs118
Perez-Orive, J., Mazor, O., Turner, G. C., Cassenaer, S., Wilson, R. I., and Laurent,
G. (2002). Oscillations and sparsening of odor representations in the mushroom body.
Science 297, 359–365. doi: 10.1126/science.1070502
Perkell, D. H., and Bullock, T. H. (1968). Neurosci. Res. Program Bull. 6, 221–348.
Perkell, J. (1970). “Spike trains as carriers of information, ” in The neurosciences:
Second study program , eds F. O. Schmitt, G. C. Quarton, T. Melnechuk, and G.
Adelman (New York, NY: Rockefeller University Press), 587–604.
Perl, E. R. (2007). Ideas about pain, a historical view. Nat. Rev. Neurosci. 8, 71–80.
doi: 10.1038/nrn2042
Perl, O., Nahum, N., Belelovsky, K., and Haddad, R. (2020). The contribution of
temporal coding to odor coding and odor perception in humans. Elife 9:e49734.
doi: 10.7554/eLife.49734
Petersen, R. S., and Diamond, M. E. (2000). Spatial-temporal distribution of
whisker-evoked activity in rat somatosensory cortex and the coding of stimulus
location. J. Neurosci. 20, 6135–6143. doi: 10.1523/JNEUROSCI.20-16-06135.2000
Petersen, R. S., Panzeri, S., and Diamond, M. E. (2002a). Population coding
in somatosensory cortex. Curr. Opin. Neurobiol. 12, 441–447. doi: 10.1016/s0959-
4388(02)00338-0
Frontiers in Computational Neuroscience 27 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 28
Cariani and Baker 10.3389/fncom.2025.1571109
Petersen, R. S., Panzeri, S., and Diamond, M. E. (2002b). The role of individual spikes
and spike patterns in population coding of stimulus location in rat somatosensory
cortex. Biosystems 67, 187–193. doi: 10.1016/s0303-2647(02)00076-x
Phillips, D. P. (1993). Neural representation of stimulus times in the primary
auditory cortex. Ann. N. Y. Acad. Sci. 682, 104–118. doi: 10.1111/j.1749-6632.1993.
tb22963.x
Pollen, D. A., Foster, K. H., and Gaska, J. P. (1985). “Phase-dependent response
characteristics of visual cortical neurons, ” in Models of the visual cortex , eds D. Rose
and V. G. Dobson (Chichester, NY: John Wiley), 281–291. doi: 10.1523/JNEUROSCI.
08-08-02713.1988
Pollen, D. A., Gaska, J. P., and Jacobson, L. D. (1989). “Physiological constraints on
models of visual cortical function, ” in Models of brain function , ed. R. M. J. Cotterill
(Cambridge: Cambridge University Press), 115–136.
Popper, A. N., and Fay, R. R. (1995). Hearing by bats . New York, NY: Springer-
Verlag.
Pratt, G. (1990). Pulse computation. Ph.D. thesis. Cambridge, MA: M.I.T.
Prescott, S. A., Ma, Q., and De Koninck, Y. (2014). Normal and abnormal coding of
somatosensory stimuli causing pain. Nat. Neurosci. 17, 183–191. doi: 10.1038/nn.3629
Price, B. H., and Gavornik, J. P. (2022). Eﬃcient temporal coding in the early visual
system: Existing evidence and future directions. Front. Comput. Neurosci. 16:929348.
doi: 10.3389/fncom.2022.929348
Prsa, M., Kilicel, D., Nourizonoz, A., Lee, K. S., and Huber, D. (2021). A common
computational principle for vibrotactile pitch perception in mouse and human.
Nat.Commun. 12:5336. doi: 10.1038/s41467-021-25476-9
Przybyszewski, A., Gasa, J. P., Foote, W., and Pollen, D. A. (2000). Striate cortex
increases contrast gain in macaque LGN neurons. Vis. Neurosci. 17, 485–494. doi:
10.1017/s0952523800174012
Raymond, S. A., and Lettvin, J. Y. (1978). “Aftereﬀects of activity in peripheral axons
as a clue to nervous coding, ” inPhysiology and pathobiology of axons, ed. S. G. Waxman
(New York, NY: Raven Press).
Reichardt, W. (1961). “Autocorrelation, a principle for the evaluation of sensory
information by the central nervous system, ” in Sensory communication , ed. W. A.
Rosenblith (New York, NY: MIT Press/John Wiley), 303–317. doi: 10.1016/j.actpsy.
2009.06.006
Reinagel, P., and Reid, R. C. (2000). Temporal coding of visual information in the
thalamus. J. Neurosci.20, 5392–5400. doi: 10.1523/JNEUROSCI.20-14-05392.2000
Reitboeck, H. J. (1989). “Neural mechanisms of pattern recognition, ” in Sensory
processing in the mammalian brain, ed. J. S. Lund (Oxford: Oxford University Press),
307–330.
Reitboeck, H. J., Pabst, M., and Eckhorn, R. (1988). “Texture description in the time
domain, ” inComputer simulation in brain science , ed. R. M. J. Cotterill (Cambridge:
Cambridge University Press).
Reiter, S., Campillo Rodriguez, C., Sun, K., and Stopfer, M. (2015). Spatiotemporal
coding of individual chemicals by the gustatory system. J. Neurosci. 35, 12309–12321.
doi: 10.1523/JNEUROSCI.3802-14.2015
Richmond, B. J., Optican, L. M., and Gawne, T. J. (1989). “Neurons use multiple
messages encoded in temporally modulated spike trains to represent pictures, ” in
Seeing contour and colour , eds J. J. Kulikowski and C. M. Dickenson (New York, NY:
Pergamon Press), 705–713.
Richmond, B. J., Optican, L. M., and Spitzer, H. (1990). Temporal encoding of
two-dimensional patterns by single units in primate primary visual cortex. I. Stimulus-
response relations. J. Neurophysiol. 64, 351–369. doi: 10.1152/jn.1990.64.2.351
Rieke, F., Warland, D., de Ruyter van Steveninck, R., and Bialek, W. (1997). Spikes:
Exploring the neural code. Cambridge, MA: MIT Press.
Risi, N., Aimar, A., Donati, E., Solinas, S., and Indiveri, G. (2020). A spike-based
neuromorphic architecture of stereo vision. Front. Neurorobot. 14:568283. doi: 10.
3389/fnbot.2020.568283
Roper, S. D. (2022). Encoding taste: From receptors to perception. Handb. Exp.
Pharmacol. 275, 53–90. doi: 10.1007/164_2021_559
Rucci, M., Ahissar, E., and Burr, D. (2018). Temporal coding of visual space. Trends
Cogn. Sci. 22, 883–895. doi: 10.1016/j.tics.2018.07.009
Rucci, M., Ahissar, E., Burr, D. C., Kagan, I., Poletti, M., and Victor, J. D. (2025).
The visual system does not operate like a camera. J. Vis. 25:2. doi: 10.1167/jov.
25.3.2
Saig, A., Gordon, G., Assa, E., Arieli, A., and Ahissar, E. (2012). Motor-
sensory conﬂuence in tactile perception. J. Neurosci. 32, 14022–14032. doi: 10.1523/
JNEUROSCI.2432-12.2012
Schmelz, M. (2015). Neurophysiology and itch pathways. Handb. Exp. Pharmacol.
226, 39–55. doi: 10.1007/978-3-662-44605-8_3
Schmelz, M. (2021). How do neurons signal itch? Front. Med. (Lausanne) 8:643006.
doi: 10.3389/fmed.2021.643006
Schnupp, J., Nelken, I., and King, A. (2011). Auditory neuroscience: Making sense of
sound. Cambridge, MA: MIT Press.
Schreiner, C. E., and Langner, G. (1988). “Coding of temporal patterns in the central
auditory system, ” in Auditory function: Neurobiological bases of hearing , eds G. M.
Edelman, W. E. Gall, and W. M. Cowan (New York, NY: Wiley), 337–362.
Sejnowski, T. (1999). “Neural pulse coding, ” inPulsed neural networks, eds W. Maass
and C. M. Bishop (Cambridge, MA: MIT Press), xiii–xxvi.
Shamir, M., Ghitza, O., Epstein, S., and Kopell, N. (2009). Representation of time-
varying stimuli by a network exhibiting oscillations on a faster time scale. PLoS
Comput. Biol. 5:e1000370. doi: 10.1371/journal.pcbi.1000370
Shamma, S., and Lorenzi, C. (2013). On the balance of envelope and temporal ﬁne
structure in the encoding of speech in the early auditory system. J. Acoust. Soc. Am.
133, 2818–2833. doi: 10.1121/1.4795783
Sharif, B., Ase, A. R., Ribeiro-da-Silva, A., and Seguela, P. (2020). Diﬀerential coding
of itch and pain by a subpopulation of primary aﬀerent neurons. Neuron 94:e944.
doi: 10.1016/j.neuron.2020.03.021
Shepherd, G. M. (1990). “Olfactory bulb, ” in The synaptic organization of the brain,
ed. G. M. Shepherd (New York, NY: Oxford University Press), 133–169.
Sheppard, J. J. (1968). Human color perception: A critical study of the experimental
foundation. New York, NY: American Elsevier.
Shimazaki, H. (2025). Neural coding: Foundational concepts, statistical
formulations, and recent advances. Neurosci. Re.s 214, 75–80. doi: 10.1016/j.
neures.2025.03.001
Siebert, W. M. (1968). “Stimulus transformations in the peripheral auditory system, ”
in Recognizing patterns, eds P. A. Kollers and M. Eden (Cambridge, MA: MIT Press),
104–133.
Siebert, W. M. (1970). Frequency discrimination in the auditory system: Place or
periodicity mechanisms? Proc. IEEE 58, 723–730. doi: 10.1109/PROC.1970.7727
Siegel, R. M., and Read, H. L. (1993). Temporal processing in the visual brain. Ann.
N. Y. Acad. Sci. 682, 171–178. doi: 10.1111/j.1749-6632.1993.tb22967.x
Simmons, A. M., and Ferragamo, M. (1993). Periodicity extraction in the anuran
auditory nerve. J. Comp. Physiol. A 172, 57–69. doi: 10.1121/1.405693
Simmons, A. M., Reese, G., and Ferragamo, M. (1993). Periodicity extraction in the
anuran auditory nerve. II: Phase and temporal ﬁne structure. J. Acoust. Soc. Am. 93,
3374–3389. doi: 10.1121/1.405693
Simmons, J. A. (1996). “Formation of perceptual objects from the timing of neural
responses: Target-range images in bat sonar, ” in The mind-brain continuum , eds R.
Llinas and P. S. Churchland (Cambridge, MA: MIT Press), 219–250.
Simmons, J. A., Dear, S. P., Ferragamo, M. J., Haresign, T., and Fritz, J. (1996a).
Representation of perceptual dimensions of insect prey during terminal pursuit by
echolocating bats. Biol. Bull. 191, 109–121. doi: 10.2307/1543071
Simmons, J. A., Ferragamo, M. J., and Sanderson, M. I. (2003). Echo delay versus
spectral cues for temporal hyperacuity in the big brown bat, Eptesicus fuscus. J. Comp.
Physiol. A Neuroethol. Sens. Neural Behav. Physiol.189, 693–702. doi: 10.1007/s00359-
003-0444-9
Simmons, J. A., Saillant, P. A., Ferragamo, M. J., Haresign, T., Dear, S. P., Fritz, J.,
et al. (1996b). “Auditory computations for biosonar target imaging in bats, ” inAuditory
computation, eds H. Hawkins, T. McMullin, A. N. Popper, and R. R. Fay (New York,
NY: Springer Verlag), 401–468.
Singer, W. (1994a). “The role of synchrony in neocortical processing and synaptic
plasticity, ” inModels of neural networks II. Temporal aspects of coding and information
processing in biological systems, eds E. Doumany, J. L. van Hemmen, and K. Schulten
(New York, NY: Springer Verlag), 141–174.
Singer, W. (1994b). “Time as coding space in neocortical processing, ” in Temporal
coding in the brain, eds G. Buzsáki, R. Llinás, W. Singer, A. Berthoz, and Y. Christen
(Berlin: Springer-Verlag), 51–80.
Singer, W. (1999). Neuronal synchrony: A versatile code for the deﬁnition of
relations? Neuron 24, 111–125. doi: 10.1016/s0896-6273(00)80821-1
Singer, W. (2009). Distributed processing and temporal codes in neuronal networks.
Cogn. Neurodyn. 3, 189–196. doi: 10.1007/s11571-009-9087-z
Singer, W. (2018). Neuronal oscillations: Unavoidable and useful? Eur. J. Neurosci.
48, 2389–2398. doi: 10.1111/ejn.13796
Singer, W., and Gray, C. M. (1995). Visual feature integration and the temporal
correlation hypothesis. Annu. Rev. Neurosci. 18, 555–586. doi: 10.1146/annurev.ne.18.
030195.003011
Skaggs, W. E., McNaughton, B. L., Wilson, M. A., and Barnes, C. A. (1996).
Theta phase precession in hippocampal neuronal populations and the compression
of temporal sequences. Hippocampus 6, 149–172. doi: 10.1002/(SICI)1098-106319966:
2<149::AID-HIPO6<3.0.CO;2-K
Spector, A. C., and Travers, S. P. (2005). The representation of taste quality in the
mammalian nervous system. Behav. Cogn. Neurosci. Rev. 4, 143–191. doi: 10.1177/
1534582305280031
Srivatsav, R. M., Chakrabartty, S., and Thakur, C. S. (2023). Neuromorphic
computing with address-event-representation using time-to-event margin
propagation. IEEE J. Emerg. Select. Top. Circuits Syst. 13, 1114–1124.
doi: 10.1109/JETCAS.2023.3328916
Frontiers in Computational Neuroscience 28 frontiersin.org
fncom-19-1571109 June 28, 2025 Time: 19:3 # 29
Cariani and Baker 10.3389/fncom.2025.1571109
Staszko, S. M., Boughter, J. D. Jr., and Fletcher, M. L. (2020). Taste coding strategies
in insular cortex. Exp. Biol. Med. 245, 448–455. doi: 10.1177/1535370220909096
Stopfer, M., Bhagavan, S., Smith, B. H., and Laurent, G. (1997). Impaired odour
discrimination on desynchronization of odour-encoding neural assemblies. Nature
390, 70–74. doi: 10.1038/36335
Surlykke, A., Nachtigall, P. E., Fay, R. R., and Popper, A. N. (2014). Biosonar.
New York, NY: Springer.
Szwed, M., Bagdasarian, K., and Ahissar, E. (2003). Encoding of vibrissal active
touch. Neuron 40, 621–630. doi: 10.1016/s0896-6273(03)00671-8
Talbot, W. H., Darian-Smith, I., Kornhuber, H. H., and Mountcastle, V. B. (1968).
The sense of ﬂutter-vibration: Comparison of the human capacity with response
patterns of mechanoreceptive aﬀerents from the monkey hand. J. Neurophysiol. 31,
301–334. doi: 10.1152/jn.1968.31.2.301
Tank, D. W., and Hopﬁeld, J. J. (1987). Neural computation by concentrating
information in time. Proc. Natl. Acad. Sci. U.S.A. 84, 1896–1900. doi: 10.1073/pnas.
84.7.1896
Teng, X., Meng, Q., and Poeppel, D. (2021). Modulation spectra capture EEG
responses to speech signals and drive distinct temporal response functions. eNeuro
8, 1–15. doi: 10.1523/ENEURO.0399-20.2020
Thatcher, R. W., and John, E. R. (1977).Functional neuroscience, Vol. I. Foundations
of cognitive processes. Hillsdale, NJ: Lawrence Erlbaum.
Theunissen, F., and Miller, J. P. (1995). Temporal encoding in nervous systems: A
rigorous deﬁnition. J. Comput. Neurosci. 2, 149–162. doi: 10.1007/BF00961885
Thorpe, S. J. (1990). “Spike arrival times: A highly eﬃcient coding scheme for neural
networks, ” inParallel processing in neural systems, eds R. Eckmiller, G. Hartmann, and
G. Hauske (Amersterdam: Elsevier), 91–94.
Thorpe, S. J., Guyonneau, R., Guilbaud, N., Allegraud, J.-M., and VanRullen,
R. (2004). SpikeNet: Real time visual processing with one spike per neuron.
Neurocomputing 58-60, 857–864. doi: 10.1016/j.neucom.2004.01.138
Tritsch, M. F. (1992). Fourier analysis of the stimuli for pattern-induced colors. Vis.
Res. 32, 1461–1470. doi: 10.1016/0042-6989(92)90202-t
Troland, L. T. (1921). The enigma of color vision. Am. J Physiol. Opt. 2, 23–48.
Troland, L. T. (1930). The principles of psychphysiology: A survey of modern scientiﬁc
psychology, Vol. II. sensation. New York, NY: von Nostrand.
Tucci, V., Buhusi, C. V., Gallistel, R., and Meck, W. H. (2014). Towards an integrated
understanding of the biology of timing. Philos. Trans. R. Soc. Lond. B Biol. Sci.
369:20120470. doi: 10.1098/rstb.2012.0470
Uchida, N., Poo, C., and Haddad, R. (2014). Coding and transformations in the
olfactory system. Annu. Rev. Neurosci. 37, 363–385. doi: 10.1146/annurev-neuro-
071013-013941
Uttal, W. R. (1972). Sensory coding: Selected readings. Boston, MA: Little-Brown.
Uttal, W. R. (1973). The psychobiology of sensory coding. New York, NY: Harper and
Row.
Uttal, W. R. (1975). An autocorrelation theory of form detection . New York, NY:
Wiley.
Uttal, W. R. (1987). The perception of dotted forms . New York, NY: Lawrence
Erlbaum.
Uttal, W. R. (1988). On seeing forms. Hillsdale, NJ: Lawrence Erlbaum.
Van Rullen, R., and Thorpe, S. J. (2001). Rate coding versus temporal order coding:
What the retinal ganglion cells tell the visual cortex. Neural Comput. 13, 1255–1283.
doi: 10.1162/08997660152002852
Van Rullen, R., Guyonneau, R., and Thorpe, S. J. (2005). Spike times make sense.
Trends Neurosci. 28, 1–4. doi: 10.1016/j.tins.2004.10.010
Verhagen, J. V., Baker, K. L., Vasan, G., Pieribone, V. A., and Rolls, E. T. (2023).
Odor encoding by signals in the olfactory bulb. J. Neurophysiol. 129, 431–444. doi:
10.1152/jn.00449.2022
Victor, J. D., and Conte, M. M. (1996). The role of high-order phase correlations in
texture processing. Vis. Res. 36, 1615–1631. doi: 10.1016/0042-6989(95)00219-7
Victor, J. D., and Purpura, K. P. (1996). Nature and precision of temporal coding in
visual cortex: A metric-space analysis. J. Neurophysiol. 76, 1310–1326. doi: 10.1152/jn.
1996.76.2.1310
Voigt, H. F., Sachs, M. B., and Young, E. D. (1982). Representation of whispered
vowels in discharge patterns of auditory-nerve ﬁbers. Hear. Res. 8, 49–58. doi: 10.1016/
0378-5955(82)90033-8
von Békésy, G. (1964a). Duplexity theory of taste.Science 145, 834–835. doi: 10.1126/
science.145.3634.834
von Békésy, G. (1964b). Olfactory analogue to directional hearing. J. Appl. Physiol.
19, 369–373. doi: 10.1152/jappl.1964.19.3.369
von Békésy, G. (1964c). Rhythmical variations accompanying gustatory stimulation
observed by means of localization phenomena. J. Gen. Physiol. 47, 809–825. doi:
10.1085/jgp.47.5.809
von Békésy, G. (1964d). Sweetness produced electrically on the tongue and its
relation to taste theories. J. Appl. Physiol. 19, 1105–1113. doi: 10.1152/jappl.1964.19.
6.1105
von Békésy, G. (1967).Sensory Inhibition. Princeton, NJ: Princeton University Press.
von Campenhausen, C. (1969). The colors of Benham’s top under metameric
illuminations. Vis. Res. 9, 677–682. doi: 10.1016/0042-6989(69)90124-2
von Campenhausen, C., Hofstetter, K., Schramme, M. F., and Tritsch, M. F. (1992).
Color induction via non-opponent lateral interactions in the human retina. Vis. Res.
32, 913–923. doi: 10.1016/0042-6989(92)90034-g
von der Malsburg, C. (1994). “The correlation theory of brain function, ” inModels of
neural networks ii. temporal aspects of coding and information processing in biological
systems, eds E. Doumany, J. L. van Hemmen, and K. Schulten (New York, NY: Springer
Verlag), 95–119.
Wallach, A., Bagdasarian, K., and Ahissar, E. (2016). On-going computation of
whisking phase by mechanoreceptors. Nat. Neurosci. 19, 487–493. doi: 10.1038/nn.
4221
Walter, G. (1959). The living brain. New York, NY: Norton.
Wang, F., Belanger, E., Cote, S. L., Desrosiers, P., Prescott, S. A., Cote, D. C., et al.
(2018). Sensory aﬀerents use diﬀerent coding strategies for heat and cold. Cell Rep. 23,
2001–2013. doi: 10.1016/j.celrep.2018.04.065
Wang, P., Li, S., and Li, A. (2024). Odor representation and coding by the
mitral/tufted cells in the olfactory bulb. J Zhejiang Univ Sci B 25, 824–840. doi:
10.1631/jzus.B2400051
Wasserman, G. S. (1992). Isomorphism, task dependence, and the multiple meaning
theory of neural coding. Biol. Signals 1, 117–142. doi: 10.1159/000109318
Wehr, M., and Laurent, G. (1996). Odour encoding by temporal sequences of ﬁring
in oscillating neural assemblies. Nature 384, 162–166. doi: 10.1038/384162a0
Wehr, M., and Laurent, G. (1999). Relationship between aﬀerent and central
temporal patterns in the locust olfactory system.J. Neurosci. 19, 381–390. doi: 10.1523/
JNEUROSCI.19-01-00381.1999
Werner, G., and Mountcastle, V. B. (1965). Neural activity in mechanoreceptive
cutaneous aﬀerents: Stimulus-response relations, Weber functions, and information
transmission. J. Neurophysiol. 28, 359–397. doi: 10.1152/jn.1965.28.2.359
Wever, E. G. (1949). Theory of Hearing. New York, NY: Wiley.
Wever, E. G., and Bray, C. W. (1937). The perception of low tones and the
resonance-volley theory. J. Psychol. 3, 101–114. doi: 10.1080/00223980.1937.9917483
White, J., and Kauer, J. S. (2001). Exploring olfactory population coding using an
artiﬁcial olfactory system. Prog. Brain Res. 130, 191–203. doi: 10.1016/s0079-6123(01)
30013-4
White, J., Truesdell, K., Williams, L. B., Atkisson, M. S., and Kauer, J. S. (2008). Solid-
state, dye-labeled DNA detects volatile compounds in the vapor phase.PLoS Biol. 6:e9.
doi: 10.1371/journal.pbio.0060009
Wilson, D. M., Boughter, J. D. Jr., and Lemon, C. H. (2012). Bitter taste stimuli
induce diﬀerential neural codes in mouse brain. PLoS One 7:e41597. doi: 10.1371/
journal.pone.0041597
Wilson, J. P. (1960). Perceptual anomalies associated with a single contour. Nature
187:137. doi: 10.1038/187137a0
Woo, S., Kim, Y. R., Bak, M. S., Chung, G., Kim, S. J., and Kim, S. K. (2022).
Multiplexed representation of itch and pain and their interaction in the primary
somatosensory cortex. Exp. Neurobiol. 31, 324–331. doi: 10.5607/en22029
Y amazaki, K., Vo-Ho, V. K., Bulsara, D., and Le, N. (2022). Spiking neural networks
and their applications: A review. Brain Sci. 12:863. doi: 10.3390/brainsci12070863
Yellott, J. I., and Iverson, G. J. (1992). Uniqueness properties of higher-order
autocorrelation functions. J. Optic. Soc. Am. A 9, 388–404. doi: 10.1364/josaa.9.000388
Young, R. A. (1977). Some observations on temporal coding of color vision:
Psychophysical results. Vis. Res. 17, 957–965. doi: 10.1016/0042-6989(77)90071-2
Young, R. A., and De Valois, R. (1977). Temporal-chromatic interactions in monkey
visual system . Rockville, MD: Association for Research in Vision and Opthamology
(ARVO).
Young, R. S. L., Cole, R. E., Gambel, M., and Rayner, M. D. (1975). Subjective
patterns elicited by light ﬂicker. Vis. Res. 15, 1291–1293. doi: 10.1016/0042-6989(75)
90177-7
Zhu, H., He, F., Zolotavin, Pavlo, Patel, S., Tolias, A. S., et al. (2025).
Temporal coding carries mmore stable cortical visual representations
than ﬁring rate over time. bioRixiv [Preprint]. doi: 10.1101/2025.05.13.65
2528
Frontiers in Computational Neuroscience 29 frontiersin.org
