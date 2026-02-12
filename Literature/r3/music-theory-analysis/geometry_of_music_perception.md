# Geometry of Music Perception

**Author:** Benjamin Himpel  
**Subject:**  Prevalent neuroscientific theories are combined with acoustic observations from various studies to create a consistent geometric model for music perception in order to rationalize, explain and predict psycho-acoustic phenomena. The space of all chords is shown to be a Whitney stratified space. Each stratum is a Riemannian manifold which naturally yields a geodesic distance across strata. The resulting metric is compatible with voice-leading satisfying the triangle inequality. The geometric model allows for rigorous studies of psychoacoustic quantities such as roughness and harmonicity as height functions. In order to show how to use the geometric framework in psychoacoustic studies, concepts for the perception of chord resolutions are introduced and analyzed.  
**Total Pages:** 34  
**Source File:** `a (6).pdf`

---

**Part 1 of 2** (Pages 1-20)

---

## Page 1

Citation: Himpel, B. Geometry of
Music Perception. Mathematics 2022 ,
10, 4793. https://doi.org/10.3390/
math10244793
Academic Editor: Luca Andrea
Ludovico
Received: 10 October 2022
Accepted: 8 December 2022
Published: 16 December 2022
Publisher’s Note: MDPI stays neutral
with regard to jurisdictional claims in
published maps and institutional afﬁl-
iations.
Copyright: © 2022 by the authors.
Licensee MDPI, Basel, Switzerland.
This article is an open access article
distributed under the terms and
conditions of the Creative Commons
Attribution (CC BY) license (https://
creativecommons.org/licenses/by/
4.0/).
mathematics
Article
Geometry of Music Perception
Benjamin Himpel
Department of Computer Science, Reutlingen University, 72762 Reutlingen, Germany;
benjamin.himpel@reutlingen-university.de
Abstract: Prevalent neuroscientiﬁc theories are combined with acoustic observations from various
studies to create a consistent geometric model for music perception in order to rationalize, explain
and predict psycho-acoustic phenomena. The space of all chords is shown to be a Whitney stratiﬁed
space. Each stratum is a Riemannian manifold which naturally yields a geodesic distance across strata.
The resulting metric is compatible with voice-leading satisfying the triangle inequality. The geometric
model allows for rigorous studies of psychoacoustic quantities such as roughness and harmonicity as
height functions. In order to show how to use the geometric framework in psychoacoustic studies,
concepts for the perception of chord resolutions are introduced and analyzed.
Keywords: music psychology; music theory; Riemanian geometry; Whitney stratiﬁcation; music
perception; voice leading; dissonance; transitional harmony; chord progression
MSC: 53Z05; 58A35; 57Z10; 35Q92; 92C20; 92B05
1. Introduction
Jacob Collier’s fascinating a cappella arrangement of “In The Bleak Midwinter” [ 1]
modulates from the key of E to the key of G half-sharp between the third and fourth verses.
This is by design, and he explains this choice in his own metaphorical language [ 2]. In
response to the question “Why does music theory sound good to our ears?” on Wired.com
Tech Support (on 26 May 2021), Jacob Collier answers “Music theory doesn’t really sound
like anything. It sounds like parchment. Music sounds like stuff though, and the truth is no
one knows. It’s a bit of a mystery.” [ 3]. This work addresses precisely the question of how to
geometrically model what music sounds like. We approach this question like a theoretical
physicist would: the world consists of physical objects goverened by differential equations.
1.1. Background
Music is based on a temporal sequence of pitched sounds. Over time, theorists
have analyzed patterns in musical works and described some classes of tones, sounds
and sequences thereof as pitches, chords (harmonies) and melodies/chord progressions,
respectively. The resulting theory is used in turn by composers to describe their musical
inceptions and allow musicians to reproduce them. The theory of harmonies is also used
by jazz musicians as a common basis for spontaneous musical creations.
There is a lot of research related to our differential-geometric approach to music
perception. However, music psychology and music theory remain practically distinct as it
was already noted by Carol Krumhansl in 1995 [ 4]. She empirically develops in [ 5] a tonal
hierarchy in speciﬁc musical contexts such as scales and tonal music. Frieder Stolzenberg [ 6]
presents a formal model for harmony perception based on periodicity detection which is
compatible with prior empirical results. Harrison and Pearce [ 7] reanalyse and formalize
consonance perception data from four previous major behavioral studies by way of a
computer model written in R. Their conclusion is that simultaneous consonance derives
in a large part from three phenomena: interference, periodicity/harmonicity, and cultural
familiarity. This suggests that chord pleasantness is a multi-dimensional phenomenon, and
Mathematics 2022 ,10, 4793. https://doi.org/10.3390/math10244793 https://www.mdpi.com/journal/mathematics

## Page 2

Mathematics 2022 ,10, 4793 2 of 34
experiment design in the study of pleasantness in chord perception is highly problematic.
They extend their ideas to introduce a new model for the analysis and generation of voice
leadings [ 8]. Marjieh et al. [ 9] provide a detailed analysis of the relationship between
consonance and timbre. A speculative account on the evolutional aspect of consonance
has been discussed in [ 10] with the conclusion that understanding evolutionary aspects
require elaborate cross-cultural and cross-species studies. Chan et al. [ 11] combine the
ideas of periodicity and roughness in the language of wave interferences in order to deﬁne
stationary subharmonic tension (essentially the ratio of a generalization of roughness to
different frequencies and periodicity) and use it to develop a new theory of transitional
harmony, also known as tension and release. Tonal expectations have been analyzed from
a sensoric and cognitive perspective in [ 12]. Dmitri Tymoczko [ 13,14] provides a geometric
model of musical chords. He also analyzed three different concepts of musical distance
and observed that they are in practise related [ 15]. Since our pitch perception is rather
forgiving and imprecise, pitch perception corresponds to a probability distribution and
therefore a smoothing should be applied to frequencies as in [ 16], which gives a rigorous
way of evaluating similarity of chords or more generally pitch collections using expectation
tensors. Differential geometry has also been used in mathematical musicology by way of
gauge theory with the aim of explaining tonal attraction [ 17,18]. Music was viewed as a
dynamical system in order to study tonal relationships [ 19] or musical performances [ 20].
On the level of audio signals, [ 21,22] use Hopf bifurcation control to study sound changes
in music. In [ 23,24], music theory for classical and jazz music is formalized by providing
a mathematical model for tonality, voice leading and chord progressions, which is very
different from the geometric and psychoacoustic approach presented in this paper but
could help in further developing it. Recent work by Wall et al. [ 25] analyzes voice leading
and harmony in the context of musical expectancy which is precisely the motivation for
our geometric model. Some very interesting vertical ideas on a scientiﬁc approach to music
can be found in [ 26], even though there are—strictly speaking—no new results in that
speciﬁc article: the brain’s exceptional ability for soft computing and pattern recognition
on incomplete or over-determined data is relevant for our model. Microtonal intervals
have been discussed in the context of harmony by [ 27,28]. Several results from cognitive
neuroscience studies in the context of music perception also need to be considered for a
geometric model [ 29–33]. A more conventional and more elaborate account on a scientiﬁc
approach to music can be found in [ 34]. William Sethares wrote a comprehensive analysis
on musical sounds based on roughness [35].
1.2. Aims
We hypothesize that there exists a simple underlying mathematical model and mecha-
nism which is responsible for the harmonic and melodic development in music, in particular
Western music. In order to study changes in sound and time, and since sound and time
are best modelled as continuous spaces, we need differential geometry in order to study
or construct musical trajectories on these spaces. Since the brain has not been understood
well enough, there is currently no way of rigorously proving the correctness of a geometric
model by deducing it from the way our brain processes music, even though there is a bit
of work in this direction [ 36,37]. Instead, the goal of this research project is to validate the
model by verifying its music theoretic implications. Our aim is to provide a framework
from a differential geometer’s point of view in the spirit of [ 14,38] which is ﬂexible enough
to allow for various existing and forthcoming approaches to studying perceptive aspects of
the space of notes and chords. In particular, this will remedy all the limitations of geometric
models mentioned in [ 5] (119ff.) by making the relations between notes and chords depend
on the context and the order. A focal point for this study is the cadence, “a melodic or
harmonic conﬁguration that creates a sense of resolution” [ 39] (pp. 105–106), which is
an important basis for a lot of modern western music and has a long history in human
evolution. It reduces tensions in chords, is related to falling ﬁfths and minimizes voice
leading distances. For us, it will serve as a guiding principle for the development of a

## Page 3

Mathematics 2022 ,10, 4793 3 of 34
differential-geometric model. While we hope that this model generalizes to other kinds of
music because of its generalist approach, our focus will be on Western music. Note that
there are many approaches to analyzing and developing music based on machine learning.
For the time being, we will stay away from machine learning, even though we may later
use techniques from parameter optimization or artiﬁcal neural networks to narrow down
the model.
Despite numerous studies on music perception, there is a need for a holistic approach
by way of a common computational framework in order to study and compare various
psychoacoustic quantities such as tension, consonance and roughness in a given context.
In the spirit of theoretical physics, we make use of mathematical models, abstractions
and generalizations in order to create a geometric framework consistent with prevalent
neuroscientiﬁc theories and results. We show how to rationalize, explain and predict
psychoacoustic phenomena as well as disprove psychoacoustic theories using tools from
differential geometry. We will not be able to reach as far as explaining Jacob Collier’s
speciﬁc modulation to a half-key, but we will show why half-keys appear naturally from a
psychoacoustic point of view. We will describe how this simple yet powerful differential-
geometric model opens up new research directions.
1.3. Main Contribution
The problem with the abundance of competing approaches to dissonance and tension,
apart from the great number of different terminologies, is that they are related but not the
same, the neuronal processing behind the perception of music has not been understood and
the music theory does not yet have a satisfactory explanation based on existing approaches
to dissonance and tension. Our geometric model has been constructed in order for these ap-
proaches to be studied, compared, and combined. Despite numerous statistical evaluations
of models for dissonance and tension, none of these models can be used directly to com-
pose music or develop music further. The main contribution is therefore to present a new
approach to music perception by combining the above approaches to music cognition and
geometric modelling in a simple differential-geometric model which can be used together
with suitable concepts of consonance and tension to deduce the laws of music theory, lends
itself to further research and musical developments, as well as provide a ﬂexible framework
to relate the perception of music and music theory. This allows for systematically and
quantitatively studying the perception of music and music theory with or without just into-
nation or various equally or not equally tempered systems and describing new approaches
to composition and improvisation in the universal language of mathematics and with the
tools provided by geometric analysis. It is general enough and modular so that some or
all of the concrete sensoric functions presented here can be replaced with alternative ones.
A possible outcome is, that we are able to use certain gradient vectors of psychoacoustic
quality functions on the space of chords that explain which chord progressions sound good
(at which speed and why) and thereby provide an effective tool for composers.
1.4. Implications
Therefore, the aim is not to provide yet another bottom-up approach, but to follow a
top-down construction of a convenient model, which integrates roughness, consonance,
tension with voice leading in order to be useful for analysing music, composing music
and ultimately developing music further. In order to study time-dependent aspects of
music, we need to be able to consider derivatives of psychoacoustic functions on a space of
musical chords with a Riemannian structure. In particular, we want to associate musical
expectation to tension on the space of chords. Even though many of the underlying ideas
can be generalized, we restrict ourselves to Western music for reasons of accessibility and
convenience with an octave spanning 12 semitones.

## Page 4

Mathematics 2022 ,10, 4793 4 of 34
2. Foundations of Music Perception
In order to be able to construct a geometric framework which is consistent with the
prevalent neuroscientiﬁc theories, let us ﬁrst review and brieﬂy discuss the most relevant
results. Human evolution has optimized the ability of our sensory nervous system and
our brain to process signals efﬁciently in order to quickly and easily produce the most
useful interpretations and implications. Logarithmic perception of signals [ 40] and pattern
recognition [ 41] are at the heart of this optimized mechanism and also provide the basis
for music cognition. Signal detection theory provides a mathematical foundation for
constructing psychometric functions as models for music perception [ 42–45]. Those readers
who are not interested in the underlying mechanisms of music perception are welcome to
continue with the mathematical part in Section 3.
2.1. Neural Coding
Sensory organs such as eye, ears, skin, nose, and mouth collect various stimuli for
transduction, i.e., the conversion into an action potential, which is then transmitted to
the central nervous system [ 46] and processed by the neuronal network in the brain as
combination of spike trains [ 47]. Both sensation and perception are based on a physiological
process of recognizing patterns in the spike trains [48].
2.2. Logarithmic Perception of Signals
By the Weber–Fechner law [ 49] the perceived intensity pof a signal is logarithmic to
the stimulus intensity Sabove a minimal threshold S0:
p=klogS
S0
.
Varshney and Sun [ 40] gave a compelling argument, why this is due to an optimiza-
tion process in biological evolution where the relative error in information-processing is
minimized. Quantization in the brain due to limited resources forces a continuous input
signal to be perceived logarithmically. The Weber–Fechner law applies to the perception of
pressure, temperature, light, time, distance and—most importantly for us—to the frequency
and amplitude of sound waves.
2.3. Phase Locking
Synchronization and phase locking is a mechanism in the brain for organizing data,
recognizing patterns and soft computing. It has also been proposed and conﬁrmed by
Langner in the case of pitches [ 50,51]. Phase locking for multiple frequencies has been stud-
ied in [ 52]. These pattern recognition capabilities can be explained by human evolution [ 41].
In [53] (pp. 193–213), it is argued how pattern recognition has improved over millions of
years in order to allow for better predictions. It is even suggested that the current age of
digitalization adds another layer of neurons to recognize new patterns. Pattern recognition
is essential for living beings and humans in particular.
We immediately recognize shapes of objects and rhythmic repetitions of signals. Even
if we do not see something clearly, because it is too far away, we can predict the shape
within a context and thereby recognize the object. Pattern recognition in signals is based
on phase-phase synchronizations. This applies for simultaneously emitted signals such
as pictures and chords, but also for temporally adjacent patterns such as moving pictures
and chord progressions. Signal predictions and expectations are based on a continuation
of patterns. The more patterns diverge from the predicted patterns the more unexpected
a signal is. Arguably, our brain prefers signals where patterns can be detected. Again,
possible reasons for this can be found in evolution:
• Patterns allow us to predict events, and correctly predicting events allows us to evade
dangers or kill pray.

## Page 5

Mathematics 2022 ,10, 4793 5 of 34
• More abstractly, changes of patterns cause a rise of information, and we want to
minimize the information we need to process,
According to [ 54] processes of our working memory are accomplished by neural
operations involving phase-phase synchronization. We can think of working memory as
an echo of ﬁring neurons in our brain. Temporally adjacent sounds yield synchronized
ﬁrings, which not only allow us to detect a rhythm but enable us to detect pitches and
relate pitches to each other in chord progressions and melodies.
Quantifying phase synchronizations had been addressed by [ 55] which showed that
phase-locking values provide better estimation of oscillatory synchronization than spectral
coherence. There are other possible explanations for the relevance of simple ratios and
periodicity as described in Section 4.4 based on neural coding such as cross entropy and
minimizing sensoric quantities in the context of estimating distances and other measures.
At this point, phase-locking seems to be as good an explanation as any for all kinds of
sensatoric phenomena and pattern recognition, even though it will eventually be necessary
to conﬁrm this or ﬁnd better explanation for the signal expectation on the neuronal level. As
the mechanism for expectation will be similar for different signals, a geometric model will
help to reject explanations and ﬁnd suitable ones based on psychoacoustic observations.
An example of a popular loss function is cross-entropy which is minimized for the
training of artiﬁcial neural networks. Since we have a metric on each stratum we can
study any height function from a differential geometric point of view. For example we can
compute the differential or gradient of the dissonance function by way of which we can
ﬁnd the optimal direction in the space of chords to reduce dissonance as fast as possible.
Cross-entropy might be a good mathematical concept for the purpose of pattern
recognition, where we match information received with the information already stored in
the brain.
2.4. Audio Signals
A vibrating object causes surrounding air molecules to vibrate. As long as the kinetic
energy is sustained it spreads as a wave by way of a chain reaction. This sound wave
travels through the ear canal into the cochlea. Hair cells inside the cochlea convert the
wave into an electrical signal, which then travels along the auditory nerve into the brain.
The audio signal goes through various stages of existence from the moment of creation
to the perception in the brain. Due to a limited resolution of human perception frequency
and amplitude is quantized, and the brain logarithmically perceives patterns thereof as
certain sound features. These characteristics enable us to quickly recognize and describe
instruments, voices and other sounds. We want to distinguish three major stages of an
audio signal’s existence as shown in Figure 1:
1. The produced sound, e.g., the vibrating molecules in the air as they are stimulated by
a musical instrument or a loudspeaker.
2. The received sound, e.g., the vibrating microphone diaphragm or the hair cells in the
cochlea, at which point the sound wave is converted into an electric signal, before it
reaches the brain or different analog or digital recording devices.
3. The perceived sound, e.g., the interpretation by a person’s brain.
Figure 1. Three major stages of the audio signal’s existence.
2.5. Spectrum
The shape of an object is an important factor in the way it can vibrate [ 56]. It can be
modeled by differential equations involving the geometry of the object. There are several

## Page 6

Mathematics 2022 ,10, 4793 6 of 34
such possibilities known as eigenmodes, each of which moves at a ﬁxed frequency and
amplitude as long as the energy is sustained. These eigenmodes are called partials, and
the collection of all partials is known as the overtone spectrum of the audio signal. For
example, the partials of an ideal vibrating string of length Lﬁxed at both its ends are n/L
forn2N. In this case, the overtone spectrum is called the harmonic spectrum.
Pattern recognition and logarithmic signal perception seem instrumental for the qual-
itative analysis of sound and music: A musical instrument can play different notes, but
our brain detects the same spectral pattern which enables us to identify the sound as
coming from the same instrument. This sound quality is also known as timbre and the
process of merging several frequencies tonal fusion. Analogous mechanisms apply to voice
recognition. Depending on certain deviation patterns in the spectral pattern we can classify
and compare different members of the same instrument family (saxophone, clarinet, ﬂute,
string, trombone, etc.). It is also exactly this spectral pattern which allows us to recognize
the different tones that are played by various sources simultaneously and to determine
which instruments are playing which notes, depending on how much training we have.
2.6. Pitch Detection
Upper partials cannot be easily singled out, only a fundamental frequency can usually
be detected by humans. Sounds, where a fundamental frequency can be detected, are
called pitched sounds. The process in our brain that detects the pitch is phase locking. The
same mechanism is responsible for detecting a pitch in several octaves played together
and for detecting a pitch in a tone with a missing fundamental, which seems compatible
with autocorrelation [ 57]. Several pitched tones can be played together to produce a chord,
where each pitch can be detected.
Notice that different people might detect different fundamental frequencies depending
on the context. This can be seen by considering the ascending Shepard’s scale [ 58] con-
structed by a series of complex tones which is circular even though the pitch is perceived
as only moving upward.
2.7. Interference
Simultaneously emitted Soundwaves interfere with each other. The interference
between sine waves with slightly differing frequencies result in beatings which can be
computed explicitly. Arbitrary sound waves such as those from pitched tones can be
approximated by sums of sine waves. The various beatings between slightly different
sine wave summands combine to a quality called roughness. Sethares [ 35,59] uses the
Plomp–Levelt curves to provide a formula for measuring roughness and argues that this
sound quality is behind tuning and scales. In particular, he suggests that some aspects
of music theory can be transferred to compressed and stretched spectra, when played in
compressed and stretched scales. This has been conﬁrmed by recent results [9].
It has been shown by Hinrichsen [ 60] that the tuning of musical instruments such as
pianos based on minimizing Shannon entropy of tone spectra is compatible with aural
tuning and the Railsback curve. While the tuning of harmonic instruments approximating
twelve-tone equal temperament using coinciding partials will work, tuning inharmonic
instruments in the context of Western music is more challenging [61].
Overtone singing is also an interesting aspects of interference. Possibly, overtones are
sometimes not what you want to hear, maybe you want to stay away from them, because
they are an unwanted artefact.
2.8. Just-Noticeable Difference and Critical Bandwidth
The probability for detecting a pitch change between two succeeding tones can be
described rigorously using signal detection theory [ 42,45]. It is a collection of psychophys-
ical methods based on statistics for analyzing and determining how signals and noise
are perceived.

## Page 7

Mathematics 2022 ,10, 4793 7 of 34
The just-noticeable difference (JND) also known as difference limen is often described
as the minimal difference between two stimuli that can be noticed half of the time. Let
us adapt the concise deﬁnition and method of computation from psychometric function
analysis provided by [ 62] to pitch changes. Suppose a subject is presented two succeeding
tones as part of a pitch discrimination task. One of the tones is called the reference pitch
p, the other the comparison pitch c. Responses R1and R2correspond to the choices c<p
and c>p, respectively. There is no option c=p. A small set of tone pairs are repeated
a number of times (15 to 20), and the subject has to choose one of the two responses. A
psychometric function models the proportion of either R1orR2. For a ﬁxed reference pitch
pthe psychometric function for R2should be a monotonically increasing function in the
comparison pitch cwith values between 0 and 1, because for cmuch bigger than pthe
correct response R2should be obvious. We will assume for simplicity that the shape of the
curve ﬁtted to the data follows a cumulative Gaussian as in Figure 2, even though other
functions such as sigmoid, Weibull, logistic or Gumbel are also a possibility [ 63]. The point
of subjective equality (PSE) is the comparison pitch at which the two responses in this
discrimination task are equally likely, i.e., the median. Then, the JND is deﬁned to be half
its interquartile range, i.e.,
JND=c0.75 c0.25
2,
where c0.25and c0.75represent the comparison pitches, at which a change is detected with
probability 0.25 and 0.75, respectively.
c0.25 PSE c0.75
Comparison pitch c0.000.250.500.751.00Proportion of R2
Figure 2. Psychometric function with quartiles c0.25, PSE and c0.75.
Notice that when two tones are played in succession the JND is bigger than when the
two notes are played simultaneously. This is due to the interference discussed in Section 2.7.
Astonishingly, Section 7.2.2 of [ 64] states that the JND for two succeeding tones with a
pause (difference) is three times higher than the without a pause (modulation). Figure 7.2
in [65] shows that the just-noticeable frequency modulation is approximately 3 Hz below
500 Hz and 0.7% of the frequency above 500 Hz. Clearly, the JND depends on the observer
as well as other circumstances (noise) that might interfere with the perception of the signal.
The critical band is the frequency bandwidth within which the interference between
two tones is perceived as beats or roughness, not as two separate tones. The JND is a
lot smaller than the critical bandwidth. According to [ 66] “a critical band is 100 Hz wide
for center frequencies below 500 Hz, and 20% of the center frequency above 500 Hz”. A
comparison between the critical band and the JND can be seen in Figure 7.2 of [ 65] which
in turn is based on Figure 12 in [67].
In the context of periodicity , Stolzenburg [ 6] uses the JND of 1% and 1.1% or, equivalently ,
log2(1.01)12=0.0143551217.23 cent and log2(1.011)12=0.0157831218.94 cent.
In [16], a standard deviation of 3 cent has been used due to experimentally obtained frequency
difference limens of supposedly 3 cent [ 68], even though the value of 1% in [ 68] corresponds
to about 18 cent as we have just seen. Still, the fact that they used the standard deviation of 3
cent for the Gaussian smoothing is an interesting aspect that we will revisit in Section 4.4. It
will be necessary to design experiments and perform further studies along the lines of [ 69] to

## Page 8

Mathematics 2022 ,10, 4793 8 of 34
collect data for periodicity discrimination in the light of pitch and roughness correlations for
tones within chords and between different chords, determine the best model and describe the
dependency on noise [ 43,44,70], which is beyond the scope of this work. Due to a lack of such
a study, we will assume that cultural familiarity lets us associate slightly mistuned pitches
with an ideal pitch and thereby detect and use the implied pitch for the perception of music.
2.9. Music Perception
Let us deﬁne music to be a temporal sequence of pitched sounds created by a formal
system. Formal systems obey a set of rules for sound and rhythm, which are ultimately
based on physics and mathematics respectively. Different cultures developed and are
continuing to develop a variety of systems and scales besides the ones used in Western
music [ 71], for example Gamelan music [ 35,72], Arabic music [ 73,74], Turkish music [ 75] and
classical Indian music [ 76]. In Western music, there are major subsystems such as classical
and jazz music. Enculturation is an important factor in the listener’s musical expectation
and perception [ 77,78], but we want to focus on a speciﬁc prevalent and in some way
universal aspect of music, namely, pitch [ 79,80]. While the space of received sounds lends
itself to a mathematical model, e.g., by using the frequencies and amplitudes computed
by Fourier analysis, the spaces of produced and perceived sounds can be compared to it.
Given a good microphone connected to some recording device and a good understanding of
particle physics the space of produced sounds should be more or less the same as the space
of received sounds. Our brain transforms sound waves of music by applying additional
ﬁlters and perceiving pitch, timbre and loudness. There is also a short term memory effect
in the brain, which we hypothesize to be responsible for the sense of resolution in certain
chord progressions.
The perception of every person is different and can change via training or degradation.
Sound and music are therefore very subjective and can be compared to food, in the sense
that the chemical content of food corresponds to the Fourier decomposition of a sound,
food can be analysed using chemistry just like we can analyse sound using Fourier analysis
or harmony theory, different tastes can be analyzed using signal detection theory and
can be described using various characteristics such as spiciness, sweetness, sourness,
temperature, etc., just like sounds can be characterized as warm, loud, sweet, rough, etc.,
via a psychoacoustic analysis. In addition there is an after-taste to food, which might
inﬂuence the characteristics of food-to-come, just like chord progressions need to be viewed
within a musical context.
Chords are also called harmonies and play a key role in Western music. These can
sound consonant or dissonant, and the change in this characteristic is an important aspect
of musical pieces. Composers build up tension and resolve it subsequently by way of
cadences. Notice that it clearly is not only a question of how consonant or dissonant chords
sound in a chord progression: the precise way or direction of chord movement is important.
It is this kind of aspect in music, that we want to illuminate by geometrically modeling
the perception of chords. To this end, we revisit the geometric model of chords [ 13] with a
focus on music perception.
2.10. Mathematics and Music
While sound seems to be well-understood by physics and mathematical structures
can be found at every point in music, neither one gives a deep understanding by providing
a general principle of how music is perceived by humans. On the other hand, music
itself is in reality a mathematical concept based on the brain’s perception of sound, put
into action in a creative and aesthetically pleasing way: Any kind of scale has been de-
veloped mathematically to be compatible with some acoustic observations, rhythm is a
time-dependent structure governed by elementary mathematics. Western music theory is a
formal system consisting of an assortment of rules that have been deduced from various
psychoacoustic preferences. An account of the major aspects surrounding mathematics

## Page 9

Mathematics 2022 ,10, 4793 9 of 34
and music can be found in [ 81]. We want to emphasize the difference between two types of
mathematical structures:
The ﬁrst kind consists of superimposed formal systems in order to give music more
structure and to make it more interesting. It starts with simple structures such as note
lengths and bars to organize rhythm. Other examples include composition procedures
such as the fugue characterized by imitation and counterpoint as well as various special
techniques such as Kanon, Krebs, Umkehrung. Then, there is the twelve-tone technique
invented by Arnold Schoenberg [ 82]. For some of these structures we assume a twelve-tone
equal temperament, which is itself a mathematical structure superimposed on pitched
sounds, not accidentally but deliberately based on a second type of mathematical structure.
This second kind is more subtle, originally due to an evolutionary process and a
preference for patterns but ultimately caused by psycho-physical mechanisms such as
phase locking. It captures the structure inherent in music. It covers temporal structures
such as rhythmic repetitions. Most Western instruments have approximately a harmonic
overtone spectrum. Guided by the simultaneous or sequential perception of intervals
and chords humans developed scales, instruments and music theory. Already Pythagoras
discovered that simple rational relationships between fundamental frequencies correlate
with pleasant sounding intervals. The twelve tones in an octave are also the result of simple
rational relationships between frequencies, even though the two physical psychoacoustic
qualities harmonicity/periodicity and roughness/interference have been shown to be
fundamentally different [ 9,35]. Music theory is a formal system which captures more
subtle perceptional aspects in Western music. It developed over centuries by the efforts of
countless musicians and theorists, mainly however due to observed perceptive qualities of
chord progressions.
Concise models of physical observations can be formulated in the universal language
of mathematics, whose powerful tools allow us to deduce complex facts from simple ones.
Therefore, the goal is to ﬁnd a simple way of modeling sounds in the context of music
perception, from which we can for example deduce good sounding chord progressions
independent of functional harmony, create a music theory in other less common music
systems as well as ultimately explain the established Western music theory of harmonies.
3. Riemannian Geometry of Chords
Tymoczko [ 13] viewed the space of chords with nnotes as an orbifold [ 83]. In [ 84],
the orbifold of chords had been generalized from a topological point of view, while we
focus on the geometry. We argue that it is a Riemannian orbifold [ 85] and show that the
space of chordsCwith an arbitrary numbers of notes is a Whitney stratiﬁed space [ 86]
endowed with a metric given by the geodesic distance. The metric provides voice leading
distance across different strata. Chord progressions can formally be viewed as sections of
the (trivial)C-bundle over the real line. While our motivation is its use for Western music
with its twelve-tone equal temperament, it can readily be adopted to other music. For
simplicity, the geometric model represents the chords that can be played using a single
instrument which can produce musical tones at any frequency (like a violin) but cannot
duplicate notes (like a piano).
Pitches and frequencies can formally be identiﬁed with integers via B3= 1,C4=0,
C]4=1, etc. Therefore unit distance corresponds to a pitch distance of 100 Cent, which
is compatible with the musician’s perception of distance between musical tones. The
identiﬁcation between frequency and pitch numbers is given by the function
pitch : R!R,
f7!12log2(f/f0),
where f0=261.626 Hzcorresponds to pitch(f0) = 0=C4. Chords can then be identi-
ﬁed with integer tuples (p1,. . .,pn)2Zn. Instead, we will identify chords with tuples
(p1, . . . , pn)2Rnfor the following reasons:

## Page 10

Mathematics 2022 ,10, 4793 10 of 34
• There are usually minor pitch adjustments to make chords sound “better”.
• The fundamental frequency f0can assume different values.
• Quarter tones are entirely legitimate.
• There are other tuning systems.
• In particular, not even the piano is tuned using twelve-tone-equal temperament but
their stretched tuning follows the Railsback curve [60,87].
• We assume that instruments play pitches and that the perceived pitch is most relevant
for our purpose. We do not include the overtone spectrum with all its amplitudes.
When it becomes necessary it can easily be introduced.
Since chord notes are played simultaneously, the order of pitches piin a chord is
irrelevant. For example, the dominant seventh chord (0, 4, 7, 11) needs to be identiﬁed with
(4, 0, 7, 11).
Lemma 1. LetSnbe the ﬁnite symmetric group of all bijective functions f1,. . .,ng!f 1,. . .,ng.
1. The permutation
s: Rn!Rn
(p1, . . . , pn)7!(ps(1), . . . , ps(n)).
is a left action on Rn.
2. The relation
˜c1'˜c2:,9 s2Sn:s(˜c1) = ˜c2for˜cj2Rn
is an equivalence relation on Rn.
Proof. Bijective functions of ﬁnite sets form a group.
1. We compute that
s2(s1(p1, . . . , pn)) = s2(ps1(1), . . . , ps1(n)) = ( ps2(s1(1)), . . . , ps2(s1(n)))
(p(s2s1)(1), . . . , p(s2s1)(n)) = ( s2s1)(p1, . . . , pn).
Therefore Snacts on Rnfrom the left.
2. Clearly, the relation is reﬂexive since ˜c1=˜c1. If˜c1'˜c2, we have s(˜c1) = ˜c2for some
s2Sn. Since Snis a group we have ˜c2=s 1(˜c1). Therefore ˜c2'˜c1, and symmetry is
satisﬁed. If ˜c1'˜c2and ˜c2'˜c3, then s1(˜c1) = ˜c2and s2(˜c2) = ˜c3for some s1,s22Sn.
Therefore (s2s1)(˜c1) = ˜c2and ˜c1˜'˜c2so that the relation is transitive.
Then the quotient by the symmetric group action is given by Rn/Sn:=Rn/', and
its elements are written as [p1,. . .,pn]. This space Rn/Snis known as the n–the symmetric
power of Rand is an example of an orbifold [ 83], a generalization of a manifold which is
locally a quotient of a differentiable manifold by a ﬁnite group action. We can also identify
notes with the same name but in different octaves before we consider the quotient by Sn.
Then, we get the toroidal orbifold (R/12Z)n/Snconsidered by Tymoczko [ 13,14] in order
to study efﬁcient voice leading. From a mathematical point of view, this orbifold does
not behave differently from Rn/Sn, but this model is not suitable for music perception.
More importantly for us, Theorem 1 shows that it is a Riemannian orbifold [ 85,88–90] and
a Riemannian orbit space [91–94].
Deﬁnition 1. A Riemannian orbifold is a metric space which is locally isometric to orbit spaces
of isometric actions of ﬁnite groups on Riemannian manifolds. A Riemannian orbit space is the
quotient of a Riemannian manifold by a proper and isometric Lie group action.
Proposition 1. Consider the Lpmetric on Euclidean space Rn. Then, the symmetric group Snacts
onRnby isometries.

## Page 11

Mathematics 2022 ,10, 4793 11 of 34
Proof. Let(p1,. . .,pn),(q1,. . .,qn)2Rn. Then, we obtain for any s2Snby commutativity
of the sum
d((p1, . . . , pn),(q1, . . . , qn)) =n
å
k=1(qp
k pp
k)1/p=n
å
k=1(qp
s(k) pp
s(k))1/p
=d((ps(1), . . . , ps(n)),(qs(1), . . . , qs(n))).
This yields the following.
Theorem 1. The quotient space Sn:=Rn/Snis a Riemannian orbifold and a Riemannian
orbit space.
In order to study chord progressions it is necessary to consider chords of varying size.
We need to construct a metric space of chords with an arbitrary number of tones that is
useful for describing music. The metric should provide a sensible voice leading distance, in
particular for chord progressions of the form [0, 3]![0, 3, 4 ]or[0, 3]![0, 3, 3 ]. Multiple
same pitches as well as transitions between chords with a different number of tones can
be dealt with by considering multiple same pitches in a chord only once, just like a piano
plays chords. For example, [0, 0, 4, 7, 11 ]is identiﬁed with [0, 4, 7, 11 ].
Proposition 2. Consider the set of chords
S:= ¥[
k=1Sk!
.
The relation
[p1,p2, . . . , pk][p1,p2, . . . , pk 1]:,[p1,p2, . . . , pk]'[p1,p1,p2, . . . , pk 1]
for all k =2, . . . , n is an equivalence relation on S.
Proof. This is an immediate consequence of 'being an equivalence relation.
This allows us to deﬁne the space of all chords.
Deﬁnition 2. LetC:=S/the space of all chords and Cn:=(Sn
k=1Sk)/the space of chords
with at most npitches. Let Un:=f(p1,. . .,pn)Rnjpi6=pjfor i6=jg. Let p:Rn!C nbe
the quotient map (p1, . . . , pn)7![p1, . . . , pn].
Remark 1. Notice thatCnnCn 1is the set of chords with exactly n different pitches.
Example 1. The spaceC2is the Euclidean plane as shown in Figure 3, where the points are identiﬁed
with their mirror image when reﬂected across the diagonal, essentially equivalent to the lower (or
the upper) triangle of the plane. C1consists of the singular points with respect to this reﬂection and
is the boundary ofC2.

## Page 12

Mathematics 2022 ,10, 4793 12 of 34
11
[1, 2]
[2, 1]
[p] = [ p,p]2C 1
Figure 3. The spaceC2.
Lemma 2. The Stabilizer S pof the action of S nonRnis trivial for each p 2Un.
Proof. The Stabilizer Spof action of SnonRnis given byfs2Snjs(p) =pg. Ifs6=1then
s(i) =jfor some i6=j. Then, pi6=ps(j)and therefore s(p)6=p. Therefore Spis trivial for
each p2Un.
Proposition 3.CnnCn 1is a Riemannian manifold of dimension n. The space of chords Cis the
disjoint union ofCnnCn=1
C=¥G
n=1(CnnCn=1).
Proof. Due to Lemma 2 we have [˜c1][˜c2],˜c1'˜c2for˜c1,˜c22Un. Therefore,
p:Un!C nnCn 1is a canonical bijection, and CnnCn 1inherits the Riemannian metric
from Rn.
Remark 2. The family of chords fCngn2Nis an example of a ﬁltration
C1C 2. . .C n. . .
By Proposition 3 the ﬁltration fCkgk=1,...,nofCis an inﬁnite-dimensional stratiﬁcation, and
CknCk 1are the strata of dimensions k.
Remark 3. The Riemannian metric gnprovides a normkvknfor every v2TpSn. Furthermore,
the Riemannian metric gnmakes the orbifoldSninto a metric space using the geodesic distance
deﬁned by
d(p,q):=inf(Zb
akr0(t)pk1/p
ndtr:[a,b]!S npiecewise smooth ,
r(a) =p,r(b) =q)
for p ,q2S n.
Proposition 4. The distance onSncan be computed via
dn(p,q) =min
s2Sn˜dn(p,s(q))
where ˜d is an Lp–metric on Rn.
Proof. In Euclidean space, the geodesic distance is given by the Lp–metric. Let p,q2S n.
Consider two representatives (p1,. . .,pn),(q1,. . .,qn)2Unofpand qwith pi<pi+1
und qi<qi+1. Then, tqi+ (1 t)pi<tqi+1+ (1 t)pi+1fort2[0, 1]which implies

## Page 13

Mathematics 2022 ,10, 4793 13 of 34
t(q1,. . .,qn) + ( 1 t)(p1,. . .,pn)2Un. Therefore Unis convex. Since Unis a fundamental
domain for Un/Sn, the distance on Un/Snis equal to the Euclidean distance in Un. Since
the canonical projection Un! S nnS n 1is an isometric bijection, it follows that for
p,q2S nnSn 1we have dn(p,q) = min s2Sn˜dn(p,s(q)). Since the closure of SnnSn 1is
also convex the same formula holds for all p,q2S n.
Chord progressions in Snwith a small distance dncorrespond to efﬁcient voice leading.
The metric dnonSnclearly yields a metric on each stratum CnnCn 1. Finding a suitable
distance on all ofCis problematic. We can deﬁne the following functions dnand dandCn
andC, respectively:
dn(c1,c2):=min
˜cj2cjdn(˜c1,˜c2)and d(c1,c2):=min
n2Ndn(c1,c2).
For example, we compute
d3([0, 1, 7 ],[0, 6, 7 ]) = 5,
d4([0, 1, 7 ],[0, 6, 7 ]) = d4([0, 1, 7, 7 ],[0, 0, 6, 7 ]) = 2.
Even if this is considered to be suitable for determining efﬁcient voice leading, the
following shows that this is not a metric on Cn.
Proposition 5. The functions d nand d onCnandCdo not satisfy the triangle inequality.
Proof. Since we have
d([0],[0, 1]) + d([0, 1],[0, 1, 2 ]) = 1+1<3=d([0],[0, 1, 2 ]), (1)
(see Figure 4) this generalization does not satisfy the triangle inequality. The same holds
fordn.
Since the aim is to do differential geometry on Cthe following result is important.
See [ 86] for a detailed treatment of stratiﬁed spaces from a geometric analysis point of view.
Theorem 2. For each n2N, the ﬁltrationfCkgk2Nis a Whitney stratiﬁcation of C.
Proof. We show that Whitney’s condition Bis satisﬁed. Consider the strata X:=CknCk 1
and Y:=ClnCl 1fork>land embed them in some RNvia a map i:Ck!RN. Let
x1,. . .and y1,. . .be sequences of points in Xand Y, respectively, both converging to the
same point y2Y, such that the sequence of secant lines Libetween xiand yiconverges to
a line LRNin real projective space RPNand the sequence of tangent planes TitoXat
the points xiconverges to a k–dimensional plane TofRNin the Grassmannian Gr(k,RN)
asitends to inﬁnity. The points x1,. . .uniquely lift to a sequence ˜x1,. . .inRk. Let ˜ybe the
lift of YtoRkso that ˜x1,. . .converges to ˜y. Choose the lift ˜YRkofYsuch that ˜y2˜Y.
Then, y1,. . .uniquely lifts to a sequence ˜y1,. . .of points in ˜Ythat converge to ˜y. Each
tangent plane Tipulls back to the only plane in Rk2Gr(k,Rk). The secant lines between
(iq) 1(xi)and(iq) 1(yi)converge to a line ˜LinRPkwhich is contained in Rk. This
implies that its push-forward L=d(iq)˜y˜Lis contained in d(iq)˜yRk=T.
Since every stratum of Cis a metric space and a Riemannian manifold, and the notion
of piecewise smooth paths makes sense in C, we can deﬁne the geodesic distance on C
as follows.
Deﬁnition 3. We call a continuous path r:[a,b]!C piecewise smooth, if there exists a partition
a=x1<. . .xN=bof[a,b]such that rrestricted to (xi,xi+1)is a smooth path inCninCni 1for

## Page 14

Mathematics 2022 ,10, 4793 14 of 34
some ni2N. Let r:[a,b]!C be a piecewise smooth path, then we deﬁne kr0(t)k:=kr0(t)knif
r(t)2C nnCn 1. The geodesic distance on Cis
d(p,q):=inf(Zb
akr0(t)pk1/pdtr:[a,b]!C piecewise smooth ,
r(a) =p,r(b) =q)
for p ,q2C.
Theorem 3. The function d is a metric on C. It can be computed via
d(p,q) =inf(
n 1
å
i=1di(xi,xi+1)jxi2C inCi 1)
Proof. Clearly, d(p,p) =0. Since every stratum is a metric space and we have only a ﬁnite
number of strata, we obtain d(p,q)>0forp6=qand d(p,q) =d(q,p). The concatenation
of any piecewise smooth path from ptoqand from qtorinCis a piecewise smooth path
from ptor, so that the triangle inequality holds. Therefore, the function dis a metric.
Letri:[a,b]!C be a sequence of piecewise smooth paths with ri(a) = pand
ri(b) = qwith a partition a=x1<. . .xN=bof[a,b]such that rrestricted to (xi,xi+1)
is a smooth path in CninCni 1for some ni2Nwhose length converges to d(p,q). Since
CninCni 1is convex, this implies
d(p,q) =N 1
å
i=1dni(xi,xi+1).
Furthermore, we can assume that ni>ni 1because of this convexity.
The metric onCcan be considered as a voice leading distance for music theory.
Example 2. Let us compute the distance between [0]and[0, 1, 2 ]. It can be computed by minimizing
the concatenation of geodesic paths within C3nC2andC2nC1, and we obtain
d([0],[0, 1, 2 ]) = min
p0(d2([0],[0,p]) + d3([0,p],[0, 1, 2 ])) = min
p0(jpj+jp 1j+jp 2j)
=1+0+1=2
In particular, we conﬁrm together with d([0],[0, 1]) = 1andd([0, 1],[0, 1, 2 ]) = 1that the triangle
inequality has not been violated as it was in Equation (1). See Figure 4.
[0, 1, 2 ]
[0, 1]
[0] C1
C2
Figure 4. The stratumC3.
In summary , Theorems 1–3 show that Cis a well-behaved differential-geometric space:
1.Cis a metric space,
2.Cis a Whitney stratiﬁed space, and

## Page 15

Mathematics 2022 ,10, 4793 15 of 34
3. each stratum of Cis a Riemannian manifold.
This provides a rich structure for quantitative studies of psychoacoustic models with
a voice leading distance on all of C. The Riemannian metric allows us to study the shape of
melodies and chord progressions by differentiating psychoacoustic functions and comput-
ing directional derivatives of paths in C. This model is universal in the sense that it allows
note and chord progressions in any musical system.
4. Sound Perception of Chords
We relate psychometric functions to psychoacoustic height functions on C. Contour
plots of psychoacoustic functions on Cprovide us with insightful visualizations of different
models for consonance such as roughness and periodicity. Timbre and loudness are also
important perceptive quantities, which can be addressed later. The Riemannian structure
onCallows us to study the shape of melodies and chord progressions as paths in Cand the
perception thereof by differentiating psychoacoustic lifts of the paths in Cin Section 5.
4.1. Psychoacoustic Functions on the Space of Chords
While the space of musical chords can be modelled geometrically, independently of
the listener, and a music score can be viewed as a sequence of points or a path in this
space, sound perception varies and corresponds to different psychoacoustic functions on
this space: dissonance, musical expectation, sense of resolution, root of chord, interfer-
ence/roughness, all of which depend on both player and listener. Usually, these functions
are real-valued on the space of chords (with a given spectrum/timbre) and quantify the
individual sensation. This kind of a function turns out to be an example for an important
mathematical tool in geometry, analysis and optimization known as a height function on a
surface, manifold or more generally a Whitney stratiﬁed space. Since the psychoacoustic
function varies with the listener and noise it is natural to analyze them using psychometric
functions introduced in Section 2.8.
Assuming that the JND for pitch discrimination is the same for every reference pitch,
let us give a different perspective on the psychometric function from Figure 2. Consider
the Gaußian distribution fm,sgiven by given by
fm,s(x) =1
sp
2pe 1
2(x m
s)2
.
with mean m=PSE and standard deviation s=JND/ 0.674490 , as well as the Heaviside
step function
f(x):=(
0 if <0
1 if0.
Then the function in Figure 2 is equal to the convolution ffm,sgiven by
(ffm,s)(p):=Z
f(x)fm,s(p x)dx.
Consider now a task which is slightly different from the one presented in Section 2.8:
For a given reference pitch pa subject has to say, whether a tone with pitch chas the same
pitch as por not. Let us reformulate the task using random variables. Let Xp,cbe the random
variable which is 1(yes) when a comparison pitch cis perceived as the reference pitch p
and 0(no) otherwise. We can go one step further and consider the continuous random
variable Xpwhich equals cwhen pis perceived as c. Then, the probability distribution of
Xpis given by the normal distribution fm,swith sand mas above. For our purpose let us
assume that PSE is equal to p.
Again, we can view the probability distribution fm,sas a convolution of fm,swith
point mass at 0 or, equivalently, as a convolution of f0,swith point mass at m=p. We
observe that fm,s(c) =0.5forc=pJND . Now that we have set up the notation, we can

## Page 16

Mathematics 2022 ,10, 4793 16 of 34
ask which pitch we expect to hear when a tone with pitch pis played. Clearly, it should be
p, and we can conﬁrm this by computing the expectation value of Xp:
E(Xp) =Z¥
 ¥P(Xp=c)c dc=Z¥
pfm,s(c)(c+ (2p c))dc=1
22p=p.
We will use this as a basis for modeling psychoacoustic functions as an expectation value
of certain random variables associated to psychometric functions. In [ 16], this viewpoint has
been used in order to model perceived distance between pairs of pitch collections, where the
perceived dissimilarity was reformulated as a metric between expectation tensors.
As we will see in Section 4.4, consonance of dyads and chords is likely to be determined
by certain nearby pitches with low periodicity which in turn is due to the phase locking and
pattern recognition principle described in Section 2.3. Let us therefore discuss the following
multi-variate scenario. Given a ﬁxed set of NpitchesP=fp1,. . .,pNgwith pi<pi+1and
JND<jpi+1 pij<2JND , a subject has to choose one pitch from Pwhich is equal or
closest to a given pitch c. Let XP,cbe the random variable which equals piif a perceived
pitch cis closest to pi. Clearly, we expect a smoothed version of a step function for the
expectation value E(XP,c)as a function of pwhere the steps are located at (pi+pi+1)/2.
One might be tempted to use the convolution of the step function with of fm,sas above, but
by doing so we have neglected the subtle interplay of the random variables and possible
dependencies. If we interpret E(XP,c)as
E(XP,c) =E0
@N_
i=10
@Xpi,c^^
j6=iXpj,c1
A1
A,
we take into account the knowledge that cis not perceived as pjforj6=i, but we neglect
terms of the form Xpi,c^Xpj,corXp1,c^. . .^XpN,c. If we assume that Xpi,cand Xpj,care
independent random variables for i6=jwe can apply the product formula for independent
random variables.
Under the premise that common chord progressions in music theory and their psy-
choacoustic properties ﬁnd their justiﬁcation in certain sound qualities, the chord model C
together with its sound qualities given by certain height functions on Cis not only inter-
esting for the music theorist and psychoacoustic analyst, but can become a powerful tool
in the hands of composers and computer programs emulating composers because of its
conceptual simplicity and quantitative control. Even though Ccould theoretically extend
to include the whole overtone spectrum, we hypothesize that different spectra will simply
change the psychoacoustic height functions, as long as the spectra consistently have almost
the same pattern.
Since there are instruments that do not produce a harmonic series in overtones, it
will be interesting to analyse how music and music theory changes for these instruments.
A change in the interference scheme due to a different overtone spectrum will promote
different note systems. This can be observed in history and other cultures because of
the construction of different scales for instruments, which do not produce a harmonic
series. Possibly, the relationship of periodicity/harmonicity and consonance needs to be
re-evaluated: Is it due to the almost harmonic spectrum of the notes produced by most
musical instruments, is it connected to the way human beings interpret periodicity of
chords, or are there other more basic concepts at work such as logarithmic perception and
pattern recognition? However, if it depends on our interpretation of chords, is this due to
enculturation or our physical and chemical processing of sound?
In summary, height functions based on mathematical quantitative models for psychoa-
coustic quantities on the space of chords allow for rigorous studies on music perception.
Once the correctness of mathematical models has been conﬁrmed they will yield new
music theories. In our work we focus on the psychoacoustic concepts of consonance and
tension/release in music. From a psychometric point of view it will be necessary to conduct

## Page 17

Mathematics 2022 ,10, 4793 17 of 34
further studies regarding these psychoacoustic quantities. We will see that experiments
must be carefully designed as in [ 9] due to the fortunate (from a Western musical point of
view) and at the same time the undesirable (from a scientiﬁc point of view) correlations
between roughness and periodicity.
4.2. Consonance
Consonance is a psychoacoustic quality of perceived chords considered to be an impor-
tant factor in Western music with the usual twelve-tone equal temperament system. Two or
more musical tones are considered consonant/dissonant, if they sound pleasant/unpleasant
together, and there are a variety of explanations for this phenomenon [ 95]. The most impor-
tant ones go back to roughness (interference) by Helmholtz [ 96] and tonal fusion (neural
periodicity) by Stumpf [ 97,98]. The discussion in [ 7] carefully analyses various different
psychoacoustic interpretations, evaluates data from previous studies, provides a code for
several computational models and shows their correlation with consonance ratings. They
conclude that consonance depends on interference/roughness, periodicity/harmonicity,
and cultural familiarity. While the ﬁrst two are based on physically justiﬁable phenomena
independent of the individual, cultural familiarity is different for every person by way of
musical expertise and cultural conditioning in the following ways:
1. Musical training actively and systematically changes your perception. In particular, it
allows to better differentiate how consonant chords sound.
2. The cultural context passively changes your perception by repetition. In particular, it
determines how consonant chords sound. E.g. certain jazz chords sound dissonant
to people who are unfamiliar with the jazz idiom, while they sound pleasant to
jazz musicians.
Tension, a concept of horizontal harmony between consecutive chords, had also been
linked to dissonance [ 99], but [ 100] suggests that tension is less subjective to cultural
familiarity and musical expertise than consonance, pleasantness and harmoniousness of
chords. A recent study [ 101] determined that roughness inﬂuences automatic responses in
a simple cognitive task while harmonicity did not. Furthermore, [ 11] argues that tension
is independent of harmonicity because it has been shown in [ 102] that it is possible for
a more consonant chord to resolve into a more dissonant chord. Even though we expect
tension to be related to harmonicity, it is apparently fundamentally different from the
vertical quality of consonance and should be reﬂected in the model accordingly. The
difﬁculty in this discussion surrounding consonance and tension is that in reality they are a
conglomeration of different psycho-acoustic phenomena. Furthermore, the terminology
might be misleading: Horizontal harmony needs to be viewed in musical context, therefore
we will call it the resolve instead of tension.
Dichotic presentation (different ears for different tones) of chords preserves harmonic-
ity and reduces roughness [ 103], therefore roughness cannot be responsible for the psycho-
logical effect of consonance for chord resolutions, even though roughness and consonance
are highly correlated during diotic presentations (same ear for all tones) and will increase
the respective effects. The difference of harmonicity and roughness has also been studied
in [36]. It is legitimate to say that interference plays a role for the construction of scales,
tuning and the quantiﬁcation of sensory dissonance [ 35], but we hypothesize that there
is a fundamental mechanism in the brain that is responsible for the effect of consonance
and tension (for a given scale) in the context of chord resolutions and for the way Western
music has developed. In particular, such a mechanism should in principal not depend
on how badly in tune the notes of a chord sound as long as the chord is approximately
correct, and it should not depend on whether the chord tones are presented diotically or
dichoticaly. Therefore, we can ignore roughness and beatings for the purpose of studying
the mechanism behind chord resolutions. Nevertheless, roughness will strengthen the
effect harmonicity has on the listener and will play a role for more subtle variations and
ﬁne-tuning of ideal chord progressions.

## Page 18

Mathematics 2022 ,10, 4793 18 of 34
From a neurophysiological point of view, we hypothesize that roughness, harmonicity
and the resolve all ﬁnd their neural coding origin in the same phase locking principle:
• Roughness is based on the interference of sine waves and can be perceived even
during dichotic presentation of dyads. It is usually determined using a spectral
analysis which will be reviewed brieﬂy in Section 4.3, but it can also be modeled by
the synchronization index model using the degree of phase locking to a particular
frequency within the neural pattern [104] and [35] (Appendix G).
• Harmonicity can be modeled via periodicity [ 6], which is based on phase locking of
perceived pitches and will be discussed in Sections 4.4 and 4.5.
• The resolve has not been studied much with respect to the phase locking principle, but
we hypothesize that it depends on the interplay between the working memory and
harmonicity. Not only has harmonicity been successfully computed via neural period-
icity, but working memory has also been linked to phase-phase synchronization [ 54].
Some ideas are developed in Section 5.1.
In summary, the three physically justiﬁable phenomena roughness, harmonicity and
resolve are correlated, and their respective psycho-acoustic effects on the listener are
ampliﬁed by this correlation and by cultural familiarity. These mechanisms are often
presented as explanations of consonance, even though they address different issues within
the perception of music. The aim of the following sections is therefore to deﬁne, distinguish
and elaborate upon the individual psycho-acoustic phenomena related to consonance in
the context ofC.
4.3. Roughness
Nineteenth-century physicist Herman von Helmholtz [ 96] was the ﬁrst to notice a
relation between the harmonic series and the pleasantness of chords, based on which he
proposed a theory of consonance and dissonance. In short, he argued, that each tone played
by a musical instrument consists of a series of partials determined by the harmonic series:
The fewer partials the spectra share, the more dissonant they should be. The interaction
between sound waves is called interference, and the interference between two different
but similar sine waves create beatings within and roughness outside a critical bandwidth
of frequency.
While Western music is usually based on twelve-tone equal temperament, this speciﬁc
tuning is really a compromise for musical instruments whose pitches are ﬁxed. The pitches
of notes for more ﬂexible instruments such as the violin or the saxophone are usually
adjusted slightly in order to produce chords with minimal or the right amount of roughness.
Even pianos are not tuned using twelve-tone-equal temperament but their stretched tuning
follows the Railsback curve [ 87]. Sethares [ 35] describes how roughness between complex
notes can be computed based on the interference between their partials. He argues that
this is one of the main reasons for having a twelve-tone equal temperament system, and
that it is a useful tool for tuning and intonating instruments. However, while roughness
might be behind tuning, and you want to mostly reduce roughness, it is simply an acoustic
artifact that you need to take into account in order to have exactly the correct amount
of roughness, just like some coinciding partials whose audibility you want to control. A
graph of roughness for dyads can be seen in Figure 5 (adapted from [ 105]). The roughness
function ﬁts very well into our geometric framework. A contour graph of roughness for
triads can be seen in Figure 6.21 of [ 35]. One small issue is the fact that the model is not
differentiable at its local minima. A possible remedy is the modeling approach by [ 104]. Its
roughness graph of a harmonic tone complex can be seen in [ 104] (Figure 4). It remains to
be seen how deep we have to dive into other aspects such as cochlear hydrodynamics [ 106]
in order to improve the roughness model for further studies on music perception.

## Page 19

Mathematics 2022 ,10, 4793 19 of 34
1/1 2/1 3/2 4/3 5/3 5/4 7/4 6/5 7/5 8/5 9/5
frequency ratiosensory dissonance
Figure 5. Sensory dissonance for dyads in terms of their frequency ratio.
It will be interesting to study roughness together with the geometric model Cto
compute and visualize entropy and determine ideal tunings. For details, formulas and
graphs of roughness we refer to [ 35]. More importantly for us we need to study roughness
in combination with harmonicity, because both types of consonance are relevant for music
in their own way, but their speciﬁc psycho-acoustic effects independently of each other are
not clear yet.
4.4. Harmonicity of Dyads
In order to create a suitable harmonicity height function p:C ! Ron musical
chords, we will focus on the harmonicity model determined by relative (logarithmic)
periodicity as presented by Stolzenburg [ 6]. His explanations based on the neuronal model
by Langner [ 50,51] using phase locking are convincing, even if probabilistic implications of
the psychometric functions apart from the JND have not been included and other aspects
such as roughness and cultural familiarity clearly alter the perception of chords. In short,
if the ratio of two pitch frequencies f1and f2with f2f1is given by f2/f1=p/qwith
gcd(p,q) = 1, then the periodicity for this dyad is q. In other words, the period of the
sound wave for this dyad equals qperiods of the ﬁrst (lower) note.
Since the above periodicity qwill change a lot for small changes of the ratio f2/f1=p/q,
our brain will pick the smallest qwithin a JND for harmonicity through phase locking as
discussed in Section 2.8. It is chosen to be 1% and 1.1% in [ 6] based on related results
by [64,67,68,107–113]. As we have seen in Section 2.8 this corresponds to approximately
18 cent.
A naive model for periodicity is therefore given by a step function with a JND of
18 cent for periodicity as shown in Figure 6, but we need to keep in mind that depending on
the listener, the loudness and distracting noise the JND might vary. Furthermore, in order
to compute JND for harmonicity of simultaneously played tones we need to design a new
experiment, where we can analyze the effects of roughness and harmonicity separately.
Notice however, that by incorporating probabilistic aspects via Gaussian smoothing
after ﬁrst constructing a step function resembling the periodicity based on [ 6] we commit a
conceptual error, which we are not able correct in this work but which is hopefully small
enough to still provide useful results. The perceived periodicity of a chord is determined
by the period that is the best ﬁt for the given spike train induced by the audio signal. The
brain either chooses the smallest period it can detect or it detects a mixture of periodicities
as an average. It is also possible that different periods are detected at different times within
a small time interval due to small variations in the spike sequence or in the pitch. Spike
trains with low periodicities are more likely to be detected than spike trains with high
periodicities. In order to create a better model we need take into account these probabilistic
issues already within the phase locking stage and make use of probabilistic tools such as
cross entropy and coherence in the time domain along the lines of [55].
Let us consider a dyad in 12-tone equal temperament as discussed in Section 3. If the
lower note is ﬁxed, a dyad spanning at most one octave is determined by the number of
separating semitones i2f0,. . ., 12g. Its frequencies fiwithin a JND of 1.1%, its relative
periodicies Liand its logarithm are given in Table 1.

## Page 20

Mathematics 2022 ,10, 4793 20 of 34
Table 1. Frequencies and periodicites relative to pitch 0.
i 0 1 2 3 4 5 6 7 8 9 10 11 12
fi 116
159
86
55
44
37
53
28
55
39
515
82
1
Li 1 15 8 5 4 3 5 2 5 3 5 8 1
log2(Li)0 3.91 3 2.32 2 1.58 2.32 1 2.32 1.58 2.32 3 0
Observe that the concept of voice leading is also related to the periodicity of an
octave being 1. It allows the player to change the voicing of a chord without changing the
psychological effect of its sound by much. Certainly, periodicities can be computed for
all intervals as a function fpfor all dyads [0,p], where p2[0, 12]. Its graph is shown in
Figure 6, where the JND is 18 cent. Notice that the step functions has jumps very close to
some of the integers.
0 2 4 6 8 10 120123456
Figure 6. Logarithmic periodicities of dyads spanning at most one octave.
As we have discussed above, in order to obtain a smooth height function on the space
of chords in the spirit of psychometric functions we can consider the convolution with a
Gaussian. A standard deviation of s=JND/ 0.674490 which we discussed in Section 4 to
be the correct value in the context of psychometric functions seems much too big. When
applied to the step function the resulting graph can be seen in Figure 7.
0 2 4 6 8 10 120123456
Figure 7. Logarithmic periodicities smoothed by a Gaussian with standard deviation of
s=JND/0.67449026.69 cent.
In order to keep the appropriate maxima and minima of the step function a standard
deviation of s=JND/ 3=6cent seems better. The result is shown in Figure 8. There
are a few reasons why this smaller sis more appropriate. First of all, [ 16] suggests a

