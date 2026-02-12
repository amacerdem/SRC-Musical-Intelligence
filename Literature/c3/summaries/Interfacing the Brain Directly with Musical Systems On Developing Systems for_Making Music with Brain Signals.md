See discussions, stats, and author profiles for this publication at: https://www.researchgate.net/publication/237350467
Interfacing the Brain Directly with Musical Systems: On Developing Systems for
Making Music with Brain Signals
Article  in  Leonardo · August 2005
DOI: 10.1162/0024094054762133
CITATIONS
70
READS
881
2 authors:
Eduardo Reck Miranda
University of Plymouth
348 PUBLICATIONS   4,654 CITATIONS   
SEE PROFILE
Andrew Brouse
McGill University
12 PUBLICATIONS   205 CITATIONS   
SEE PROFILE
All content following this page was uploaded by Eduardo Reck Miranda on 30 March 2014.
The user has requested enhancement of the downloaded file.


There is a growing number of researchers world-
wide working in the ﬁeld of Brain-Computer Interfacing
(BCI). Our work is unique, however, in that we are focused on
the development of BCI systems for musical applications and
we pay special attention to the development of generative mu-
sic techniques tailored for such systems. We might call such
systems Brain-Computer Music Interfaces (BCMIs). We should
clarify that the BCI research community understands a BCI
as a system that allows for the control of a machine by think-
ing about the task in question; e.g. controlling a robotic arm
by thinking explicitly about moving an arm. This is an ex-
tremely difﬁcult problem. The BCMI-Piano and the Inter-
Harmonium presented in this paper do not employ this type
of explicit control. We are not primarily interested in a system
that plays a melody by thinking the melody itself; rather, we
are furnishing our systems with artiﬁcial intelligence so that
they can perform their own interpretations of the meanings
of EEG patterns. Such machine interpretations may not always
be accurate or realistic, but this is the type of human-computer
interaction that we wish to address in our work.
To date, most efforts in BCI research have been aimed at
developing assistive technology to help disabled people com-
municate or control mechanical devices (such as wheelchairs
or prosthetic limbs). Comparatively little has been done to im-
plement BCI technology for musical applications.
MAKING MUSIC WITH BRAINWAVES
Human brainwaves were ﬁrst measured in 1924 by Hans Berger
[1,2]. Today, the electroencephalogram (EEG) has become
one of the most useful tools in the diagnosis of epilepsy and
other neurological disorders. The fact that a machine can read
signals from the brain has sparked the imaginations of scien-
tists, artists and researchers. Consequently, the EEG has made
its way into a myriad of applications.
In the early 1970s, Jacques Vidal took the ﬁrst tentative step
toward a BCI system. The results of
this work were published in 1973
[3]. Recently Vidal has revisited this
ﬁeld in his speculative article “Cy-
berspace Bionics” [4]. Many other
interesting attempts followed Vi-
dal’s work. In 1990, for example,
Jonathan Wolpaw and colleagues
developed a system to allow primitive control of a computer
cursor by individuals with severe motor deﬁcits. Users were
trained to use aspects of their 8–13 Hz alpha rhythm to move
the cursor in simple ways [5]. In 1998, Christoph Guger and
Gert Pfurtscheller presented a paper reporting an impressive
advance in BCI research: an EEG-based system for controlling
a prosthetic hand [6]. More recent reports on BCI research
have been published [7].
As early as 1934, a paper in the journal Brain reported a
method for listening to the EEG [8], but it is now generally ac-
cepted that it was composer Alvin Lucier who, in 1965, com-
©2005 ISAST
LEONARDO, Vol. 38, No. 4, pp. 331–336, 2005
331
G E N E R A L  A R T I C L E  
Interfacing the Brain Directly 
with Musical Systems: 
On Developing Systems for 
Making Music with Brain Signals
Eduardo Reck Miranda 
and Andrew Brouse
Eduardo Reck Miranda (composer, researcher, teacher), Computer Music Research,
School of Computing, Communications and Electronics, University of Plymouth, Drake
Circus, Plymouth, Devon PL4 8AA, U.K. E-mail: <eduardo.miranda@plymouth.ac.uk>.
Andrew Brouse (composer, researcher, teacher), Computer Music Research, School of
Computing, Communications and Electronics, University of Plymouth, Drake Circus, Ply-
mouth, Devon PL4 8AA, U.K. E-mail: <andrew.brouse@plymouth.ac.uk>.
A B S T R A C T
The authors discuss their work
on developing technology to
interface the brain directly with
music systems, a ﬁeld of
research generally known as
Brain-Computer Interfacing (BCI).
The paper gives a brief back-
ground of BCI in general and
surveys various attempts at
musical BCI, or Brain-Computer
Music Interface (BCMI)—
systems designed to make
music from brain signals, or
brainwaves. The authors present
a technical introduction to the
electroencephalogram (EEG),
which measures brainwaves
detected by electrodes placed
directly on the scalp. They
introduce approaches to the
design of BCI and BCMI systems
and present two case study
systems of their own design: 
the BCMI-Piano and the Inter-
Harmonium.
Fig. 1. Brainwaves can be detected by placing electrodes 
on the scalp. (© Eduardo Reck Miranda)


posed the ﬁrst musical piece using the
EEG: Music for Solo Performer [9]. This was
a piece for percussion instruments made
to resonate by the performer’s EEG waves.
Later in the 1960s, Richard Teitelbaum
used the EEG (and other biological sig-
nals) to control electronic synthesizers
[10]. Then, in the early 1970s, David
Rosenboom began systematic research
into the potential of the EEG to generate
artworks, including music [11]. He devel-
oped EEG-based musical interfaces asso-
ciated with a number of compositional
and performance environments exploring
the hypothesis that it might be possible to
detect certain aspects of our musical ex-
perience in the EEG signal [12].
Since the 1970s, many other musicians
have experimented with EEG signals to
make music, but the ﬁeld has advanced
slowly. In 2003, one of the current authors,
Eduardo Miranda, and colleagues pub-
lished a paper in Computer Music Journal
[13] reporting on experiments and tech-
niques for enhancing the EEG signal and
training the computer to identify EEG pat-
terns associated with simple cognitive mu-
sical tasks.
THE ELECTROENCEPHALOGRAM
(EEG)
Neural activity generates electric ﬁelds
that can be recorded with electrodes at-
tached to the scalp (Fig. 1). The elec-
troencephalogram, or EEG, is the visual
plotting of this signal. In current usage,
the initials commonly refer to both the
method of measurement and the electric
ﬁelds themselves. These electric ﬁelds are
extremely faint, with amplitudes in the or-
der of only a few microvolts. These signals
must be greatly ampliﬁed in order to be
displayed and/or processed [14,15].
at one time is called a montage. Montages
fall into one of two categories: referential
or bipolar. In referential montages, the
reference for each electrode is in com-
mon with other electrodes; for exam-
ple, each electrode may be referenced 
to an electrode placed on the earlobe. 
An average reference means that each
electrode is compared to the average 
potential of every electrode. In bipolar
montages, each channel is composed of
two neighboring electrodes; for example,
channel 1 could be composed of Fp1-F3,
where Fp1 is the active electrode and F3
is the reference; channel 2 could then be
composed of Fp2-F4, where Fp2 is the ac-
tive electrode and F4 is the reference;
and so forth.
The EEG expresses the overall activity
of millions of neurons in the brain in
terms of charge movement, but the elec-
trodes can detect this only in the most su-
perﬁcial regions of the cerebral cortex.
The EEG is a difﬁcult signal to handle be-
cause it is ﬁltered by the meninges (the
membranes that separate the cortex from
the skull), the skull and the scalp before
it reaches the electrodes. Furthermore,
the signals arriving at the electrodes are
integrated sums of signals arising from
many possible sources, including artifacts
such as the heartbeat and eye blinks. This
signal needs to be further scrutinized
with signal processing and analysis tech-
niques in order to be of any use for our
research.
There are a number of approaches to
quantitative EEG analysis, such as power
spectrum, spectral centroid, Hjorth, event-
related potential (ERP) and correlation, to
cite but ﬁve. A brief nonmathematical 
introduction to EEG power spectrum,
spectral centroid and Hjorth analyses is
given below because of their relevance 
to the systems introduced in this paper.
We take note of discussions of other
analysis techniques and how they have
been used in the neuroscience of music
research [17–21].
The EEG is measured as the voltage
difference between two or more elec-
trodes on the surface of the scalp, one of
which is taken as a reference. There are
basically two conventions for positioning
the electrodes on the scalp: the 10-20 Elec-
trode Placement System (as recommended
by the International Federation of So-
cieties for EEG and Clinical Neuro-
physiology) and the Geodesic Sensor Net
(developed by a ﬁrm called Electric Ge-
odesics [16]). The former is more popu-
lar and is the convention adopted for the
systems described in this paper: It uses
electrodes placed at positions that are
measured at 10% and 20% of the head
circumference (Fig. 2). In this case, the
terminology for referring to the position
of the electrodes uses a key letter that in-
dicates a region on the scalp, and a num-
ber: F = frontal, Fp = frontopolar, C =
central, T = temporal, P = parietal, O =
occipital and A = auricular (the earlobe,
not shown in Fig. 2). Odd numbers indi-
cate electrodes on the left side of the
head and even numbers those on the
right side.
The set of electrodes being recorded
332
Miranda and Brouse, Interfacing the Brain with Musical Systems
G
Fp1
Fp2
F7
T3
T5
O1
O2
T6
T4
F8
F3
Fz
F4
C3
Cz
C4
P3
Pz
P4
Fig. 2. The standard 10-20
Electrode Placement System;
the electrodes are placed at
positions measured at 10% 
and 20% of the head circum-
ference. (© Eduardo Reck
Miranda)
Fig. 3. An example 
of Hjorth analysis. 
(© Eduardo Reck
Miranda) A raw EEG
signal is plotted at the top
(C:1) and its respective
Hjorth analysis is plotted
below: activity (C:2),
mobility (C:3) and 
complexity (C:4). 


Power Spectrum Analysis
Power spectrum analysis is based upon
techniques of Fourier analysis, such as
the Discrete Fourier Transform (DFT).
DFT, sometimes called the ﬁnite Fourier
transform, is a mathematical method
widely employed in signal processing and
related ﬁelds to analyze the frequencies
contained in the spectrum of a signal.
This is useful because the distribution 
of power in the spectrum of the EEG 
can reﬂect certain states of mind. For ex-
ample, a spectrum with salient low-fre-
quency components can be associated
with a state of drowsiness, whereas a spec-
trum with salient high-frequency com-
ponents could be associated with a state
of alertness. There are ﬁve commonly
recognized frequency bands or rhythms
of EEG activity, each with its speciﬁc as-
sociated mental states: delta, theta, alpha,
low beta and high beta. There is, however,
some controversy as to the exact fre-
quency boundaries of these bands and
about the mental states with which they
are associated.
Related to power spectrum analysis is
spectral centroid analysis, which calculates
the spectral “center of gravity” of the sig-
nal, that is, the midpoint of its energy dis-
tribution. Spectral centroid is a measure
of the average frequency weighted by am-
plitude, usually averaged over time.
Hjorth Analysis
Hjorth introduced an interesting method
for clinical EEG analysis [22] that meas-
ures three attributes of the signal: its ac-
tivity, mobility and complexity. Essentially,
through frequencies between two other
given frequencies.
Figure 3 shows an example of Hjorth
analysis. There is no clear agreement as
to what these measurements mean in
terms of mental states. It is common
sense to assume that the longer a subject
remains focused on a speciﬁc mental
task, the more stable the signal is, and
therefore the lower the variance of the
amplitude ﬂuctuation. However, this as-
sumption does not address the possible
effects of fatigue, habituation and bore-
dom, which we have not yet accounted
for in our research.
APPROACHES TO
BCI SYSTEM DESIGN
Generally speaking, a BCI is a system that
allows one to interact with a computing
device by means of signals emanating di-
rectly from the brain. There are two ba-
sic ways of tapping brain signals: invasive
and noninvasive. Whereas invasive meth-
ods require the placement of sensors con-
nected to the brain inside the skull,
noninvasive methods use sensors that can
read brain signals from outside the skull.
Invasive technology is becoming increas-
ingly sophisticated, but brain prosthetics
is not a viable option for this research.
The most viable noninvasive option for
tapping the brain for BCI is currently the
EEG.
It is possible to identify three cate-
gories of BCI systems:
1. User oriented: BCI systems in which
the computer adapts to the user.
Metaphorically speaking, these sys-
tems attempt to read the EEG of the
user in order to control a device.
For example, Anderson and Sijer-
cic [23] reported on the develop-
ment of a BCI that learns how 
to associate speciﬁc EEG patterns
this is a time-based signal analysis. This
method is interesting because it repre-
sents each time step (or window) using
only these three attributes and this is
done without conventional frequency
domain description (such as that of
DFT).
The signal is measured for successive
epochs (or windows) of one to several
seconds. Two of the attributes are ob-
tained from the ﬁrst and second time de-
rivatives of the amplitude ﬂuctuations in
the signal. The ﬁrst derivative is the rate
of change of the signal’s amplitude. At
peaks and troughs the ﬁrst derivative is
zero. At other points it will be positive or
negative depending on whether the am-
plitude is increasing or decreasing with
time. The steeper the slope of the wave
is, the greater the amplitude of the ﬁrst
derivative. The second derivative is de-
termined by taking the ﬁrst derivative of
the ﬁrst derivative of the signal. Peaks
and troughs in the ﬁrst derivative, which
correspond to points of greatest slope 
in the original signal, result in zero am-
plitude in the second derivative, and 
so forth.
Activity is the variance of the ampli-
tude ﬂuctuations in the epoch. Mobility
is calculated by taking the square root of
the variance of the ﬁrst derivative divided
by the variance of the primary signal.
Complexity is the ratio of the mobility of
the ﬁrst derivative of the signal to the mo-
bility of the signal itself. A sine wave has
a complexity of one.
There is one fact, however, that should
be borne in mind with Hjorth analysis: It
does not produce very clear results if the
input signal has more than one strong
band of frequencies in the power spec-
trum. This problem can be alleviated by
band-pass ﬁltering the signal beforehand,
but this may cause some loss of informa-
tion. A band-pass ﬁlter is a device that lets
Miranda and Brouse, Interfacing the Brain with Musical Systems
333
Braincap
Analysis
Music
Engine
Performance
EEG
Expression
MIDI
Fig. 4. The BCMI-Piano is composed 
of four modules. (© Eduardo Reck
Miranda)
Analysis
Music Engine
Frequency
band
Signal
complexity
Generative
rules
Tempo and
dynamics
EEG
MIDI
Fig. 5. Spectral information is used to activate generative music rules to compose 
music on the ﬂy, and the signal complexity is used to control the tempo of the music. 
(© Eduardo Reck Miranda)


from a subject with commands for
navigating a wheelchair.
2. Computer oriented: BCI systems in
which the user adapts to the com-
puter. These systems rely on the ca-
pacity of the users to learn to
control speciﬁc aspects of their
EEGs, affording them the ability to
exert some control over events in
their environments. Examples have
been shown where subjects learn
how to steer their EEG to select let-
ters for writing words on a com-
puter screen [24].
3. Mutually oriented: BCI systems that
combine the functionalities of both
categories; the user and computer
adapt to each other. The combined
use of mental task pattern classiﬁ-
cation and biofeedback-assisted on-
line learning allows the computer
and the user to adapt. Prototype sys-
tems to move a cursor on the com-
puter screen have been developed
in this fashion [25,26].
Until recently, those who have at-
tempted to employ EEG as part of a mu-
sic controller have done so by associating
certain EEG characteristics, such as the
power of the EEG alpha rhythms, with
speciﬁc musical actions. These are es-
sentially computer-oriented systems, as
they require users to learn to control
their EEGs in certain ways.
THE BCMI-PIANO
The BCMI-Piano falls into the category
of computer-oriented systems. The mo-
tivation for this system, however, departs
from a slightly different angle than do
other BCI systems. We aimed for a system
that would make music by “guessing”
two streams of control parameters. One
stream contains information about the
most prominent frequency band in the
signal and is used by the music engine to
compose the music. The other stream
contains information about the com-
plexity of the signal and is used by the
music engine to control the tempo of the
music (Fig. 5).
The core of the music engine module
is a set of generative music rules, each of
which produces a musical bar, or meas-
ure. A composition is then constructed
out of a sequence of musical bars (Fig. 6).
For each bar there are four possible gen-
erative rules, each of which is associated
with one of four EEG rhythms: theta, al-
pha, low beta, high beta. For example, 96
generative rules would be required to
compose a piece lasting for 24 bars. The
system works as follows: every time it has
to produce a bar, it checks the power
spectrum of the EEG at that moment and
activates one of the four generative rules
associated with the most prominent EEG
rhythm in the signal. The system is ini-
tialized with a reference tempo (e.g. 120
beats per minute) that is constantly mod-
ulated by the signal complexity analysis
(i.e. Hjorth analysis). A detailed expla-
nation of the generative rules is beyond
the scope of this paper.
THE INTERHARMONIUM
The InterHarmonium was conceived as
a networked live brainwave music per-
formance system [30]. The initial impe-
tus was to allow geographically separated
performers to simultaneously play musi-
cal compositions with their brainwaves.
As with the BCMI-Piano, the motivation
for this system springs from a source
other than prosthetic or therapeutically
oriented BCI systems. The InterHar-
monium was envisioned as a platform 
for artistic explorations into the topog-
raphies of computer networks as a
metaphor for our own central nervous
systems: Whereas the brain is formed of
billions of “networked” neurons, the In-
terHarmonium is formed of various net-
worked brains. Although it uses analysis
techniques similar to proper BCI systems,
the InterHarmonium would more ap-
propriately be considered a form of “au-
ditory display” [31], as it is attempting 
to present real-time brainwave activity 
in such a way as to make it intuitively 
and immediately comprehensible to lis-
teners. The fact that multiple networked
brains in different places can control mu-
sic in other, geographically separated 
locations is intrinsic to the InterHarmo-
what might be going on in the mind of
the subject rather than a system for ex-
plicit control of music by the subject.
Learning to steer the system by means of
biofeedback would be possible, but we
are still investigating whether this possi-
bility would produce effective control.
We acknowledge that the notion of
“guessing the mind” here is extremely
simplistic, but it is plausible: It is based
on the assumption that physiological in-
formation can be associated with speciﬁc
mental activities [27].
The system is programmed to look for
information in the EEG signal and match
the ﬁndings with assigned generative mu-
sical processes. For example, if the system
detects prominent alpha rhythms in the
EEG, then it will generate musical pas-
sages associated with the alpha rhythms.
These associations are predeﬁned and
they determine the different types of mu-
sic that are generated in association with
different mental states.
The system is composed of four main
modules (Fig. 4): braincap, analysis, music
engine and performance. The brain signals
are sensed with 7 pairs of gold EEG elec-
trodes on the scalp, roughly forming a
circle around the head (bipolar mon-
tage): G-Fz, F7-F3, T3-C3, O1-P3, O2-P4,
T4-C4, F8-F4. A discussion of the ration-
ale of this conﬁguration falls outside the
scope of this paper. It sufﬁces to say that
we are not looking for signals emanating
from speciﬁc cortical sites; rather, the
idea is to sense the EEG behavior over
the whole surface of the cortex. The elec-
trodes are plugged into a real-time biosig-
nal acquisition system manufactured by
g.Tec (Guger Technologies) [28].
The analysis module is programmed in
Matlab and Simulink [29]. It generates
334
Miranda and Brouse, Interfacing the Brain with Musical Systems
generative
rule 1(θ)
generative
rule 1(α)
generative
rule 1(β)
generative
rule 1(Β)
generative
rule 2(θ)
generative
rule 2(α)
generative
rule 2(β)
generative
rule 2(Β)
generative
rule 3(θ)
generative
rule 3(α)
generative
rule 3(β)
generative
rule 3(Β)
Begin
θ
β
α
etc.
etc.
Bar 1
Bar 2
Bar 3
α
Fig. 6. Each bar of a composition is produced by one of four possible generative rules,
according to the EEG rhythm of the subject. (© Eduardo Reck Miranda)


nium design and central to its aesthetic
proposition.
Figure 7 illustrates the general struc-
ture of the system. In short, brain signals
are sensed, digitized and properly con-
verted to a suitable format to then be sent
over standard Internet Protocol networks
by the InterHarmonium servers; these
servers function as brainwave sources.
The InterHarmonium client computers
function as brainwave sinks, as well as
brainwave analysis and sound synthesis
nodes. The nodes can all have either all
the same or their own unique sets of soni-
ﬁcation rules.
The EEG was sensed using 4–8 elec-
trodes on the performer’s head with a
ground on one ear. The electrodes were
positioned on either one or both hemi-
spheres of the skull, roughly correspon-
ding to the frontal (Fp1, Fp2), temporal
(T3, T4), occipital (O1, O2) and parietal
(P3, P4) lobes. The earlobe electrode (A)
was used to improve common-mode noise
rejection. Differential measurements
were made between electrodes of the
same hemisphere. The electrodes were
plugged into a 16-channel Grass model
8-18 D analog EEG machine [32].
The ampliﬁed EEG signal from the
Grass machine was digitized using a Mark
of the Unicorn 828 8-channel A-D audio
interface [33]. Many current high-qual-
ity audio interfaces such as this have us-
able response down to 1 Hz or lower,
which is suitable for digitizing most EEG
signals. The software was implemented
in Max/MSP [34], using the Open-
SoundControl (OSC) protocol [35] to
format the data and the UDP protocol to
transport it over the Internet.
Brainwave analysis and sound synthe-
sis takes place at the client end. In con-
trast to the BCMI-Piano described above,
the InterHarmonium does not involve
any high-level compositional processes:
it soniﬁes the incoming EEG data ac-
cording to chosen parameters.
The sound synthesis process is inspired
by a well-known psychoacoustic phe-
nomenon known as the “missing funda-
mental.” Most musical instruments
produce a fundamental frequency plus
several higher tones, which are whole-
number multiples of the fundamental.
The beat frequencies between the suc-
cessive harmonics constitute subjective
tones that are at the same frequency as
the fundamental and therefore reinforce
the sense of pitch of the fundamen-
tal note being played. If the lower har-
monics are not produced because of poor
ﬁdelity or ﬁltering of the sound repro-
duction equipment, one still can hear 
ment-to-moment changes in relation-
ships between different channels of the
performer’s EEG.
DISCUSSION AND
CONCLUDING REMARKS
Our research work in this area owes a his-
torical debt to the pioneering work of
people such as David Rosenboom,
Richard Teitelbaum and Alvin Lucier,
but extends those earlier experiments
with new possibilities for much ﬁner
granularity of control over real-time mu-
sical processes.
The work presented in this paper is the
result of intense multidisciplinary re-
search, ranging from neuroscience and
medical engineering to music technol-
ogy and composition. While we have a
good understanding of the composi-
tional requirements of music as well as
the technical exigencies in the imple-
mentation of BCMI, we acknowledge
that our research so far has revealed only
the tip of a vast iceberg. There still re-
main a number of cumbersome problems
to be resolved before we can realize our
ultimate goal: an affordable, ﬂexible and
practically feasible BCMI for composi-
tion and performance with intelligent
real-time computer music systems.
Although powerful mathematical tools
for analyzing the EEG already exist, 
we still lack a good understanding of
their analytical semantics in relation to
the tone as having the pitch of the non-
existent fundamental because of the pres-
ence of these beat frequencies. This
“missing fundamental” effect plays an im-
portant role in sound reproduction by
preserving the sense of pitch (including
the perception of melody) when repro-
duced sound loses some of its lower fre-
quencies.
The vast majority of spectral energy in
the human EEG typically lies below 30 Hz
and thus largely below the range of nor-
mal human perception. The idea is that
if one can synthesize the corresponding
harmonic overtone structure of a given
subsonic frequency (such as the 8–13 Hz
alpha), then the psychoacoustic phe-
nomenon of the missing fundamental
will make the listener aware of that fre-
quency although he or she may not ac-
tually be able to hear it.
This was done by calculating the on-
going spectral centroid averaged over 
all brainwave signals and using that as 
the “fundamental” for the synthesized
sound (most likely a subsonic tone); 
then overtones or harmonic partials
—whole-number frequency multiples—
were calculated in the audible range. The
amplitude of the various partials was con-
trolled based on calculations derived
from relationships between the ongoing
brainwave signals. The harmonic center
of the fundamental was derived from the
spectral centroid and the shifting timbral
surface textures were based on the mo-
Miranda and Brouse, Interfacing the Brain with Musical Systems
335
InterHarmonium
Servers
EEG is digitized and
sent over the network
EEG
is received
from the
network
EEG
is processed
and analyzed
Audio is
synthesized
based on
audification rules
EEG
EEG
EEG
EEG
Analysis
Analysis
Audio
Audio
Internet
Fig. 7. The structure of the 
InterHarmonium system. 
(© Eduardo Reck Miranda)


musical cognition. However, continual
progress in the ﬁeld of cognitive neuro-
science [36] is improving this scenario
substantially. Once these issues are bet-
ter understood we will be able to pro-
gram our devices to recognize patterns
of cognitive activity in the brainwaves and
activate appropriate musical algorithms
associated with such patterns. Prelimi-
nary work in this regard has been re-
ported in a recent paper [37].
Other aspects that need to be devel-
oped include the nonergonomic nature
of the electrode technology for sensing
the EEG, which can be uncomfort-
able and awkward to wear. There are cer-
tainly possibilities for innovations in 
the hardware design of EEG capture de-
vices. In his original 1973 paper, Jacques
Vidal suggested putting miniature pre-
ampliﬁers right at the site of the elec-
trode. Inexpensive auto-scanning/auto-
negotiating wireless chips are now avail-
able and could be placed on the head
along with small preampliﬁers and mi-
croprocessors. It would thus be possible
to build a wearable EEG sensor device
with built-in ampliﬁers, signal processing
and wireless data transmission [38].
References and Notes
1. H. Berger, “Über Das Elektrenkephalogramm Des
Menschen,” Archiv für Psychiatrie und Nervenkrank-
heiten 87 (1929) pp. 527–570.
2. H. Berger, “On the Electroencephalogram of
Man,” The Fourteen Original Reports on the Human Elec-
troencephalogram, Electroencephalography and Clinical
Neurophysiology, Supplement No. 28 (Amsterdam: El-
sevier, 1969).
3. J.J. Vidal (1973), “Toward Direct Brain-Computer
Communication,” in L.J. Mullins, ed., Annual Review
of Biophysics and Bioengineering (Palo Alto, CA: An-
nual Reviews, 1993) pp. 157–180.
4. J.J. Vidal, “Cyberspace Bionics” <http://www.
cs.ucla.edu/~vidal/bionics.html>. Accessed 17 June
2004.
5. J. Wolpaw et al., “An EEG-Based Brain-Computer
Interface for Cursor Control,” Electroencephalography
and Clinical Neurophysiology 78, No. 3, 252–259 (1991).
6. C. Guger and G. Pfurtscheller, “EEG-Based Brain-
Computer Interface (BCI) Running in Real-Time un-
der Windows,” Electroencephalography and Clinical
Neurophysiology (Proceedings of 9th European Congress of
Clinical Neurophysiology) 106, Supplement 1, 91–100
(1998).
7. For recent reports on BCI research please refer to
the special issue of IEEE Transactions on Biomedical
Engineering 51 (June 2004).
on Rehabilitation Engineering 20, No. 5, 214–216
(1999).
27. H. Petsche and S.C. Etlinger, EEG and Thinking
(Vienna: Austrian Academy of Sciences, 1998).
28. g.tec—Guger Technologies <http://www.gtec.
at/>. Accessed 18 June 2004.
29. The MathWorks <http://www.mathworks.com/>.
Accessed 18 June 2004.
30. A. Brouse, “The Interharmonium: An Investiga-
tion into Networked Musical Applications and
Brainwaves,” M.A. dissertation (McGill University,
2001).
31. G. Kramer, ed., Auditory Display: Soniﬁcation, Au-
diﬁcation, and Auditory Interfaces (Reading, MA: Ad-
dison-Wesley, 1994).
32. Grass-Telefactor <http://www.grass-telefactor.
com/>. Accessed 7 July 2004.
33. See <http://www.motu.com/>. Accessed 7 July
2004.
34.
See <http://www.cycling74.com/products/
maxmsp.html>. Accessed 6 July 2004.
35. Open Sound Control <http://www.cnmat.
berkeley.edu/OpenSoundControl/>. Accessed 7 July
2004.
36. I. Peretz and R.J. Zatorre, The Cognitive Neuro-
science of Music (Oxford, U.K.: Oxford Univ. Press,
2003).
37. E.R. Miranda, S. Roberts and M. Stokes, “On Gen-
erating EEG for Controlling Musical Systems,” Bio-
medizinische Technik 49, No. 1, 75–76 (2004).
38. It is worth mentioning that there are a few com-
mercially available EEG systems that can be used by
artists and musicians; for example, the IBVA system
and WaveRider. Although these systems have some
limitations, they are a good starting point for those
wanting to experiment with the concepts presented
in this paper. Please see IBVA Technology <http://
www.ibva.com/> (accessed 17 June 2004) and Mind-
Peak <http://www.mindpeak.com/> (accessed 14
February 2005).
Manuscript received 1 October 2004.
Eduardo Reck Miranda is the head of com-
puter music research at the University of Ply-
mouth, U.K. He has authored a number of
papers and books in the ﬁeld of computer mu-
sic. He has made contributions in the ﬁelds of
speech synthesis, evolutionary music and cog-
nitive neural modeling. His latest album CD,
Mother Tongue, was released by Sargasso,
London.
Andrew Brouse is a composer and researcher.
He has lectured on music technology at McGill
University and computation arts at Concor-
dia University in Montreal, Canada. Cur-
rently he is studying for a Ph.D. in the ﬁeld
of Brain-Computer Music Interface at the Uni-
versity of Plymouth, U.K.
8. E. Adrian and B. Matthews, “The Berger Rhythm:
Potential Changes from the Occipital Lobes in Man,”
Brain 57, No. 4, 355–385 (1934).
9. A. Lucier, “Statement On: Music for Solo Per-
former,” in D. Rosenboom, ed., Biofeedback and the
Arts: Results of Early Experiments (Vancouver, Canada:
Aesthetic Research Centre of Canada, 1976).
10. R. Teitelbaum, “In Tune: Some Early Experi-
ments in Biofeedback Music (1966–1974),” in D.
Rosenboom [9].
11. D. Rosenboom, Extended Musical Interface with the
Human Nervous System, Leonardo Monograph Series
No. 1 (Berkeley, CA: International Society for the
Arts, Sciences and Technology, 1990).
12. D. Rosenboom, “The Performing Brain,” Com-
puter Music Journal 14, No. 1, 48–65 (1990).
13. E.R. Miranda et al., “On Harnessing the Elec-
troencephalogram for the Musical Braincap,” Com-
puter Music Journal 27, No. 2, 80–102 (2003).
14. E. Niedermeyer and F.H. Lopes da Silva, eds., 
Electroencephalography, 2nd Ed. (Munich, Germany:
Urban and Schwartzenberg, 1987).
15. K.E. Misulis, Essentials of Clinical Neurophysiology
(Boston, MA: Butterworth-Heinemann, 1997).
16. Electrical Geodesics, Inc. <http://www.egi.com/>.
Accessed 21 June 2004.
17. M. Besson and F. Faita, “An Event-Related Po-
tential (ERP) Study of Musical Expectancy: Com-
parison of Musicians with Non-Musicians,” Journal of
Experimental Psychology: Human Perception and Perfor-
mance 21 (1995) pp. 1278–1296.
18. P. Janata and H. Petsche, “Spectral Analysis of the
EEG as a Tool for Evaluating Expectancy Violations
of Musical Contexts,” Musical Perception 10, No. 3,
281–304 (1993).
19. S. Koelsch, E. Schroger and T.C. Gunter, “Music
Matters: Preattentive Musicality of the Human
Brain,” Psychophysiology 39 (2002) pp. 38–48.
20. R. Näätänen, “The Role of Attention in Auditory
Information Processing as Revealed by Event-Related
Potentials and Other Brain Measures of Cognitive
Function,” Behavioral and Brain Sciences 13 (1990) pp.
201–288.
21. M. Tervaniemi, “Pre-Attentive Processing of Mu-
sical Information in the Human Brain,” Journal of
New Music Research 28, No. 3, 237–245 (1999).
22. B. Hjorth, “EEG Analysis Based on Time Series
Properties,” Electroencephalography and Clinical Neu-
rophysiology 29 (1970) pp. 306–310.
23. C. Anderson and Z. Sijercic, “Classiﬁcation of
EEG Signals from Four Subjects during Five Mental
Tasks,” in Solving Engineering Problems with Neural Net-
works: Proceedings of the Conference on Engineering Ap-
plications in Neural Networks (EANN’96) (Turku,
Finland: Systems Engineering Association, 1996) pp.
507–514.
24. N. Birbaumer et al., “A Spelling Device for the
Paralysed,” Nature 398 (1999) pp. 297–298.
25. B.O. Peters, G. Pfurtscheller and H. Flyvberg,
“Prompt Recognition of Brain States by Their EEG
Signals,” Theory in Biosciences 116 (1997) pp. 290–301.
26. W.D. Penny et al., “EEG-Based Communication:
A Pattern Recognition Approach,” IEEE Transactions
336
Miranda and Brouse, Interfacing the Brain with Musical Systems
