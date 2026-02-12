# Harmony Perception by Periodicity Detection

**Author:** Frieder Stolzenburg  
**Subject:**   
**Total Pages:** 33  
**Source File:** `a (14).pdf`

---

## Page 1

Harmony Perception by Periodicity Detection
Frieder Stolzenburgy
Harz University of Applied Sciences, Automation & Computer Sciences Department,
Friedrichstr. 57-59, 38855 Wernigerode, GERMANY
Abstract
The perception of consonance /dissonance of musical harmonies is strongly correlated with their
periodicity. This is shown in this article by consistently applying recent results from psychophysics
and neuroacoustics, namely that the just noticeable di erence between pitches for humans is about
1% for the musically important low frequency range and that periodicities of complex chords can be
detected in the human brain. Based thereon, the concepts of relative and logarithmic periodicity with
smoothing are introduced as powerful measures of harmoniousness. The presented results correlate
signiﬁcantly with empirical investigations on the perception of chords. Even for scales, plausible re-
sults are obtained. For example, all classical church modes appear in the front ranks of all theoretically
possible seven-tone scales.
Keywords: consonance /dissonance; harmony perception; periodicity; dyads, triads, chords, and scales
1 Introduction
Music perception and composition seem to be inﬂuenced not only by convention or culture, manifested
by musical styles or composers, but also by the neuroacoustics and psychophysics of tone perception
(Langner, 1997; Roederer, 2008). While studying the process of musical creativity including harmony
perception, several questions may arise, such as: What are the underlying principles of music perception?
How can the perceived consonance /dissonance of chords and scales be explained?
Numerous approaches tackle these questions, studying the consonance /dissonance of dyads and tri-
ads (Kameoka and Kuriyagawa, 1969; Hutchinson and Knopo , 1978, 1979; Cook and Fujisawa, 2006;
Johnson-Laird et al., 2012). For instance, the major triad (Figure 1(a)) is often associated with emotional
terms like pleasant ,strong , orbright , and, in contrast to this, the minor triad (Figure 1(b)) with terms
like sad,weak , ordark. Empirical studies reveal a clear preference ordering on the perceived conso-
nance /dissonance of common triads in Western music (see Figure 1), e.g. major minor (Roberts, 1986;
Johnson-Laird et al., 2012).
Early mathematical models relate musical intervals, i.e. the distance between two pitches, to simple
fractions by applying the fact that, in physical terms, an interval is the ratio between two sonic frequencies.
This helps to understand that human subjects rate harmonies, e.g. major and minor triads, di erently with
respect to their consonance. But since most common triads (cf. Figure 1) throughout are built from thirds,
thirds do not provide a direct explanation of the preference ordering. Newer explanations are based on the
notion of dissonance, roughness, instability, or tension (Helmholtz, 1863; Hutchinson and Knopo , 1978,
1979; Terhardt et al., 1982; Parncutt, 1989; Sethares, 2005; Cook and Fujisawa, 2006; Cook, 2009, 2012).
They correlate better with empirical results on harmony perception, but still can be improved.
Original paper appeared in Journal of Mathematics and Music , 9(3):215–238, 2015. DOI: 10.1080 /17459737.2015.1033024
yE-mail: fstolzenburg@hs-harz.de
1arXiv:1306.6458v6  [cs.SD]  20 Nov 2018

## Page 2

G
(a) major	4			6				4	
(b) minor					4	4 		6	
(c) diminished6		2			4			4	4
(d) augmented4		4	
(e) suspended6	6								
Figure 1: Common triads and their inversions. Figure 1(a)–(d) show all triads that can be built from major
and minor thirds, i.e., the distance between successive pairs of tones are three or four semitones, including
their inversions which are obtained by transposing the currently lowest tone by an octave, always with A4
as the lowest tone here. Figure 1(e) shows the suspended chord, built from perfect fourths (ﬁve semitones
apart). Its last inversion reveals this.
1.1 Aims
A theory of harmony perception should be as simple and explanatory as possible. This means on the one
hand, that it does not make too many assumptions, e.g. on implicit or explicit knowledge about diatonic
major scales from Western music theory, or use many mathematical parameters determining dissonance or
roughness curves. On the other hand, it should be applicable to musical harmonies in a broad sense: Tones
of a harmony may sound simultaneously as in chords, or consecutively and hence in context as in melodies
or scales. A harmony can thus simply be identiﬁed by a set of tones forming the respective interval, chord,
or scale. This article aims at and presents a fully computational (and hence falsiﬁable) model for musical
harmoniousness with high explanatory power for harmonies in this general, abstract sense.
A theory of harmony perception should furthermore also consider and incorporate the results from
neuroacoustics and psychophysics on auditory processing of musical tone sensations in the ear and the
brain. The frequency analysis in the inner ear can be compared with that of a ﬁlter bank with many
parallel channels. Periodicities of complex chords can be detected in the human brain, and information
concerning stimulus periodicities is still present in short-term memory (Langner, 1997; Lee et al., 2009).
Finally, the correlation between the consonance /dissonance predicted by the theory and the perceived
consonance /dissonance from empirical studies should be the highest possible. In order to make the theory
deﬁnitely non-circular, we therefore want to establish the relation between musical harmonies, i.e. com-
plex vibrations, and their perceived consonance /dissonance. Several empirical experiments on harmony
perception have been conducted (Malmberg, 1918; Roberts, 1986; Krumhansl, 1990; Johnson-Laird et al.,
2012; Temperley and Tan, 2013). For this, participants are asked to listen to and rate musical harmonies on
an ordinal scale with respect to their consonance /dissonance. We will use the results of these experiments,
which take intervals, chords, or scales as stimuli, to evaluate theories on harmony perception (in Section 4).
1.2 Main contribution
This article applies recent results from psychophysics and neuroacoustics consistently, obtaining a fully
computational theory of consonance /dissonance perception. We focus on periodicity detection, which can
be identiﬁed as a fundamental mechanism to music perception, and exploit in addition the fact that the
just noticeable di erence between pitches for humans is about 1% for the musically important low fre-
quency range (Zwicker et al., 1957; Roederer, 2008). This percentage is the only parameter of the present
approach. The concept of periodicity pitch has been studied for intervals many times in the literature (cf.
Roederer, 2008, and references therein). The idea in this article is to transfer this concept to chords and
also scales by considering relative periodicity, that is the approximated ratio of the period length of the
chord (its periodicity pitch) relative to the period length of its lowest tone component (without necessarily
applying octave equivalence), called harmonicity h in Stolzenburg (2009). In this article we will use the
term relative periodicity rather than harmonicity.
2

## Page 3

The hypothesis in this article is that the perceived consonance of a musical harmony decreases as the
relative periodicity hincreases. The corresponding analysis presented here (in Section 4) conﬁrms that it
does not matter much whether tones are presented consecutively (and hence in context) as in scales or
simultaneously as in chords. Periodicity detection seems to be an important mechanism for the perception
of all kinds of musical harmony: chords, scales, and probably also chord progressions. Listeners always
prefer simpler, i.e. shorter periodic patterns. The predictions of the presented periodicity-based method
with smoothing obtained for dyads and common triads on the one hand and diatonic scales, i.e. the clas-
sical church modes, on the other hand all show highest correlation with the empirical results (Schwartz
et al., 2003; Johnson-Laird et al., 2012; Temperley and Tan, 2013), not only with respect to the ranks, but
also with the ordinal values of the empirical ratings of musical consonance. For the latter, we consider
logarithmic periodicity , i.e. log2(h). As we will see, this logarithmic measure can plausibly be motivated
by the concrete topological organisation of the periodicity coding in the brain (cf. Section 2.6).
1.3 Overview of the rest of the article
The organisation of the article is straightforward. After this introductory section (Section 1), we brieﬂy
discuss existing theories on harmony perception (Section 2), which often make use of the notions con-
sonance and dissonance. In particular, we highlight the psychophysical basis of harmony perception by
reviewing recent results from neuroacoustics on periodicity detection in the brain (e.g. Langner, 1997).
Then, we deﬁne relative and logarithmic periodicity with smoothing in detail (Section 3). Applying these
measures of harmoniousness to common musical chords and also scales shows very high correlation with
empirical results (Section 4). We compare these results with those of other models of harmony perception
in our evaluation. Finally, we draw some conclusions (Section 5).
2 Theories of harmony perception
Since ancient times, the problem of explaining musical harmony perception attracted a lot of interest.
In what follows, we discuss some of them brieﬂy. But since there are numerous approaches addressing
the problem, the following list is by no means complete. We mainly concentrate on theories with a psy-
chophysical or neuroacoustical background and on those that provide a mathematical, i.e. computational
measure of consonance /dissonance that we can use in our evaluation of the di erent approaches (in Sec-
tion 4).
2.1 Overtones
A harmonic complex tone may consist of arbitrary sinusoidal tones, called partials , with harmonically
related frequencies. The frequency of the nth (harmonic) partial is fn=nf, where n1 and f=f1is
the frequency of the fundamental tone. The tones produced by real instruments, such as strings, tubes, or
the human voice, have harmonic or other overtones , where the nth overtone corresponds to the ( n+1)st
partial.
Overtones (cf. Figure 2) may explain the origin of the major triad and hence its high perceived con-
sonance. The major triad appears early in the sequence, namely partials 4, 5, 6 (root position) and – even
earlier – 3, 4, 5 (second inversion). But this does not hold for the minor chord. The partials 6, 7, 9 form a
minor chord, which is out of tune however, since the frequency ratio 7 =6 diers from the ratio 6 =5, which
is usually assumed for the minor third. The ﬁrst minor chord in tune appears only at the partials 10, 12, 15.
In contrast to the major triad, the partials forming the minor triad are not adjacent, and their ground tones
(B4 and G]5, respectively) are not octave equivalent (i.e., they do not have the same basic name) with the
fundamental tone E2 of the overtone series.
3

## Page 4

G1
	2
	3
	4
	5
4	6
	7
6	8	
94	
104	
114	
12	
136	
146	
154	
16	
Figure 2: Harmonic partials (approximated) with respect to the fundamental tone E2.
Furthermore, a diminished triad is given by the partials 5, 6, 7. Therefore, it appears previous to the
minor triad in the overtone series, which is inconsistent with the empirical results. Nevertheless, the so
obtained diminished triad is also out of tune. The intervals correspond to di erent frequency ratios, namely
6=5 and 7=6, although the diminished triad is built from two (equal) minor thirds.
2.2 Frequency ratios
Already Pythagoras studied harmony perception, relating music and mathematics with each other. He
created a tuning system that minimised roughness for intervals of harmonic complexes and expressed
musical intervals as simple fractions, i.e. with small numerators and denominators. Also Euler (1739) (see
also Bailhache, 1997) spent some time with the problem and proposed the so-called gradus suavitatis
(degree of softness) as a measure of harmoniousness, considering the least common multiple (lcm) of
denominators and numerators of the frequency ratios fa1=b1;:::; ak=bkg(where all fractions ai=biare in
lowest terms) with respect to the lowest tone in the given harmony. If pm1
1:::pm`
`is the prime factorisation
ofn=lcm(a1;:::; ak)lcm(b1;:::; bk), then the gradus suavitatis is deﬁned by  (n)=1+P`
i=1mi(pi 1).
For instance, for the major second interval consisting of the frequency ratios f1=1;9=8g(including the root),
we have lcm(1 ;9)lcm(1;8)=72=2332and hence  (72)=1+31+22=8 as the value of the
gradus suavitatis.
Following somewhat the lines of Euler (1739), Stolzenburg (2012) considers, besides periodicity, the
complexity of the product lcm( a1;:::; ak)lcm(b1;:::; bk) with respect to prime factorisation. More pre-
cisely, it is the number of not necessarily distinct prime factors 
(cf. Hardy and Wright, 1979, p. 354), de-
ﬁned for natural numbers as follows: 
(1)=0,
(n)=1, ifnis a prime number, and 
(n)= 
(n1)+
(n2)
ifn=n1n2. For example, for the major second interval (see above), we have 
(72)= 
(2332)=3+2=5.
The function shares properties with the logarithm function (cf. last part of deﬁnition for composite num-
bers). The rationale behind this measure is to count the maximal number of times that the whole periodic
structure of the given chord can be decomposed in time intervals of equal length. Brefeld (2005) proposes
(a1:::akb1:::bk)1=(2k)as a measure of harmoniousness, i.e. the geometric average determined from
the numerators and denominators of the frequency ratios of all involved intervals. Both these measures
yield reasonable harmoniousness values in many cases.
Honingh and Bod (2005, 2011) investigate convexity of scales, by visualising them on the Euler lat-
tice, in which each point represents an integer power of prime factors, where also negative exponents are
allowed. Because of octave equivalence (which is adopted in that approach), the prime 2 is omitted. For
example, the frequency ratio 5 =3 (major sixth) can be written as 3 151and thus be visualised as point
( 1;1). Honingh and Bod (2005, 2011) consider periodicity blocks according to Fokker (1969) and ob-
serve that almost all traditional scales form (star-)convex subsets in this space. However, the star-convexity
property does not allow to rank harmonies, as done in this article, at least not in a direct manner, because
it is a multi-dimensional measure.
4

## Page 5

xyFigure 3: Dissonance or roughness curve with y= x=aexp(1 x=a)bandx=jf1=f0 1j(absolute
value of relative frequency deviation) following the lines of Hutchinson and Knopo (1978, 1979). ais
the interval for maximum roughness, and bis an index set to 2 to yield the standard curve.
2.3 Dissonance, roughness, and instability
Helmholtz (1863) explains the degree of consonance in terms of coincidence and proximity of overtones
and di erence tones. For instance, for the minor second (frequency ratio 16 =15), only very high, low-
energy overtones coincide, so it is weakly consonant. For the perfect ﬁfth (frequency ratio 3 =2), all its
most powerful overtones coincide, and only very weak ones are close enough to beat. The perfect ﬁfth is
therefore strongly consonant and only weakly dissonant. The theory of Helmholtz (1863) has already been
criticised convincingly by contemporaries such as R. H. Lotze, C. Stumpf, or E. Mach, but it has survived
with some modiﬁcations until today (e.g. Plomp and Levelt, 1965). Newer explanations are based on the
notion of dissonance orroughness (Kameoka and Kuriyagawa, 1969; Hutchinson and Knopo , 1978,
1979; Parncutt, 1989; Sethares, 2005). Other important explanations refer to tonal fusion (Stumpf, 1890)
or combination tones (Krueger, 1904).
In general, dissonance is understood as the opposite to consonance, meaning how well tones sound to-
gether. If two sine waves sound together, typical perceptions include pleasant beating (when the frequency
dierence is small), roughness (when the di erence grows larger), and separation into two tones (when
the frequency di erence increases even further) (Sethares, 2005, Figure 3.7). Based on these observations,
several mathematical functions for dissonance or roughness curves are proposed in the literature. Figure 3
shows one possibility according to Hutchinson and Knopo (1978, 1979) with two parameters aandb,
where ydenotes the sensory dissonance and xis the relative deviation between the two frequencies. In
order to ﬁnd out the dissonance among several tones, usually their overtone spectra are also taken into
account, summing up the single dissonance values.
Although these approaches correlate better with the empirical results on harmony perception, they do
not explain the low perceived consonance of the diminished or the augmented triad, which are built from
two minor or major thirds, respectively. Therefore, Cook and Fujisawa (2006) emphasise that harmony
is more than the summation of interval dissonance among tones and their upper partials, adopting the
argument from psychology that neighbouring intervals of equal size are unstable and produce a sense of
tonal instability ortension , that is resolved by pitch changes leading to unequal intervals (see also Cook,
2012). Lowering any tone in an augmented triad by one semitone leads to a major triad and raising to a
minor triad. Because of this, Cook and Fujisawa (2006) assume sound symbolism, where the major triad
is associated with social strength and the minor triad with social weakness.
Since overtone spectra vary largely among di erent instruments, it is di cult to determine the number
and amplitudes of overtones. This uncertainty makes the calculation of dissonance as sketched above a bit
vague. Maybe because of this, works based on dissonance and related notions focus on the consonance of
dyads and triads, whereas the analysis of more complex chords or even scales is less often studied.
5

## Page 6

2.4 Human speech and musical categories
Gill and Purves (2009) (see also Bowling and Purves, 2015) consider a more biological rationale, investi-
gating the relationship between musical modes and vocalisation. They examine the hypothesis that major
and minor scales elicit di erent a ective reactions because their spectra are similar to the spectra of voiced
speech segments. Their results reveal that spectra of intervals in major scales are more similar to the ones
found in excited speech, whereas spectra of particular intervals in minor scales are more similar to the
ones of subdued speech (Bowling et al., 2010). The observation, that the statistical structure of human
speech correlates with common musical categories, can also be applied to consonance rankings of dyads,
yielding plausible results (Schwartz et al., 2003). As a measure for comparing harmonies, the mean per-
centage similarity of the respective spectra is considered in this context. For an interval with frequency
ratio a=b, it is deﬁned as ( a+b 1)=(ab) (Gill and Purves, 2009, p. 2).
2.5 Periodicity-based approaches
The approaches discussed so far essentially take the frequency spectrum of a sound as their starting point.
Clearly, analysing the frequency spectrum is closely related to analysing the time domain (with respect to
periodicity). Fourier transformation allows us to translate between both mathematically. However, subjec-
tive pitch detection, i.e. the capability of the auditory system to identify the repetition rate of a complex
tone, only works for the lower but musically important frequency range up to about 1500 Hz (Plomp,
1967). A missing fundamental tone can be assigned to each interval. For this, the frequency components
of the given interval or chord are interpreted as (harmonic) overtones of a common fundamental frequency.
Note that the tone with the fundamental frequency, called the periodicity pitch of the interval, is not al-
ways present as an original tone component (and hence missing). Therefore, periodicity pitch and tone
pitch represent distinct dimensions of harmony perception.
Schouten (1938, 1940) introduces the notion of residue for periodicity pitch. Based on these works,
several periodicity-based approaches have been proposed (Licklider, 1951, 1962; Boomsliter and Creel,
1961; Terhardt et al., 1982; Beament, 2001). Licklider (1962) discusses possible neuronal mechanisms for
periodicity pitch, including autocorrelation and comb-ﬁltering, which has been proved correct by recent
results from neuroacoustics (see Section 2.6). Boomsliter and Creel (1961) explain musical phenomena
as relationships between long patterns of waves, using so-called frequency discs . Hofmann-Engl (2004,
2008) provides a more computational model, which determines the most probable missing fundamental
tone in the so-called sonance factor . Relative periodicity hpresented in this article (in Section 3) is also
based on periodicity detection. It is a fully computational model of consonance /dissonance, applicable to
harmonies in the broad sense, which shows high correlation with empirical ratings.
2.6 Neuronal models
Since musical harmony seems to be a phenomenon present in almost all human cultures, harmony percep-
tion must be somehow closely connected with the auditory processing of musical tone sensations in the ear
and in the brain. That periodicity can be detected in the brain has been well known for years. For example,
two pure tones forming a mistuned octave cause so-called second-order beats , although no exact octave
is present (Plomp, 1967; Roederer, 2008). But only recently has neuroacoustics found the mechanism for
being able to perceive periodicity, which lays the basis for the notion of relative periodicity hintroduced
in this article: Langner (1997) successfully conducted experiments on periodicity detection with animals
and humans. The resulting neuronal model (Langner, 1997, 2015) for the analysis of periodic signals is
sketched in Figure 4. It contains several stages, that we will explain next.
First, so-called trigger neurons in the ventral cochlear nucleus, well known as octopus cells in anatom-
ical terms, transfer signals without signiﬁcant delay. The period of the original signal and the neuronal
6

## Page 7

oscillator
neuronsintegrator
neuronstrigger
neuron
neuroncoincidenceinner ear
cochlea
orthogonal logarithmic
tonotopic pitch and periodicity map
cognitive
process
consonance/dissonance perceptionsoundFigure 4: Sketch of the neuronal model for the analysis of periodic signals (cf. Langner, 1997, Figure 3).
The arrows roughly denote the workﬂow of the auditory processing.
7

## Page 8

activity correspond, but the neuronal activity typically has the form of spike trains, i.e. a series of discrete
action potentials (Langner and Schreiner, 1988; Cariani, 1999; Tramo et al., 2001). The maximal ampli-
tude of these spikes is limited. This means, that some information on the waveform of the original signal
concerning the overtone spectrum and also the amplitudes, which contribute to the timbre and loudness of
the sound, is lost and hence in consequence the original signal is highly distorted by this.
Second, there are oscillator neurons , which are chopper neurons or stellate cells, with intrinsic oscilla-
tion showing regularly timed discharges in response to stimuli, not corresponding to the temporal structure
of the external signal. The oscillation intervals can be characterised as integer multiples nTof a base
period of T=0:4 ms with n2 for endothermic, i.e. warm-blooded animals (Langner, 1983; Schulze and
Langner, 1997; Bahmer and Langner, 2006). The external signal is synchronised with that of the oscillator
neurons, which limits signal resolution. Hence, frequencies and also intervals can only be distinguished
up to a certain precision.
Third, in the dorsal cochlear nucleus, periodic signals are transferred with (di erent) delays. Onset
latencies of so-called integrator neurons (fusiform cells, i.e. type IV cells, and giant cells in anatomical
terms) up to 120 ms have been observed (Langner and Schreiner, 1988). While oscillator neurons respond
with almost no delay, integrator neurons respond with a certain amount of delay. Both groups of neurons
are triggered and synchronised by trigger neurons (on-cells). When the delay corresponds to the signal
period, the delayed response and the non-delayed response to the next modulation wave coincide. All neu-
rons respond also to the harmonic overtones of their characteristic frequency (Langner, 1997). Therefore,
the missing fundamental tone and hence periodicity pitch can be detected in the brain. In the auditory
midbrain (inferior colliculus), coincidence neurons respond best whenever the delay is compensated by
the signal period.
The latter provides the basis for an autocorrelation mechanism by comb-ﬁltering, which includes phase
locking (Langner, 1983; Meddis and Hewitt, 1991; Lee et al., 2009). This means, phase di erences among
dierent signals can be neglected. Furthermore, runtime di erences between di erent spike trains in the
auditory system are nulliﬁed, thus facilitating the highest possible coincidence rate between two corre-
lated spike trains. The neurons in the midbrain inferior colliculus are capable of phase locking to stimulus
periodicities up to 1000 Hz, as Langner and Schreiner (1988) found out by experiments with cats. There
seems to be evidence that periodicity detection is possible for signiﬁcantly higher frequencies in some
cases (Langner, 1997, cf. Section 2.5). Pitch and timbre (i.e. frequency and periodicity) are mapped tem-
porally and also spatially and orthogonally to each other in the auditory midbrain and auditory cortex
as a result of a combined frequency-time analysis that is some kind of autocorrelation or comb-ﬁltering.
The neuronal periodicity maps in the inner cortex (of cat and gerbil) and cortex (of gerbil and human)
are organised along logarithmic axes in accordance with the frequency tuning of the respective neurons
(Langner and Schreiner, 1988; Schulze and Langner, 1997; Langner et al., 1997). In total, about 8 octaves
can be represented in each dimension.
Lee et al. (2009) (see also Lee et al., 2015) discovered that the phase-locking activity to the temporal
envelope is more accurate (i.e. sharper) in musicians than non-musicians, reporting experiments with two
intervals: The consonant interval (major sixth, tones with 99 and 166 Hz, approximate frequency ratio
5=3) shows the highest response in the brainstem at about 30.25 ms ˆ =99/3Hz, and the dissonant interval
(minor seventh, 93 and 166 Hz, frequency ratio 9 /5) at about 54.1 ms ˆ =93/5Hz. All this ﬁts very well with
periodicity-based approaches to harmony perception: The denominator of the approximate frequency ratio
(underlined above) is the relative period length with respect to the frequency of the lowest tone, as we shall
see later. In summary, the periodicity of a complex tone sensation can be detected by the auditory system
in the brain. In addition, it seems possible that the auditory system alters the spectrum of intervals making
them sound more consonant, i.e. obtaining simpler frequency ratios.
8

## Page 9

2.7 Autocorrelation and tonal fusion
All these results, which are also consistent with results from fMRI experiments on melody processing
in the auditory pathway (Patterson et al., 2002), indicate that periodicity detection in the brain may be
an important mechanism during music perception. Therefore, several approaches to harmony perception
(Ebeling, 2007, 2008; Foltyn, 2012) directly refer to Langner (1997). Ebeling (2007, 2008) (see also Ebel-
ing, 2014) develops a neuronal model of pulse chains in the auditory systems testing di erent pulse forms.
Applying autocorrelation functions, he derives the so-called generalised coincidence function by com-
puting the energy of the autocorrelation function. It provides a periodicity measure for arbitrary stimuli.
Intervals do not need to be given by ratios of positive integers, arbitrary vibration ratios can be handled. It
turns out that this mathematical model deﬁnes a measure that is in line with the degree of tonal fusion as
described by Stumpf (1883, 1890, 1898).
Stumpf (1883, 1890) assumes that listeners recognise whether one or more tones are present and how
similar or di erent they are. The perception of musical harmony arises then after tonal fusion, where
the sensation of several tones results into a single impression. From introspection and extensive hearing
experiments, in particular with musically not trained persons, he deduces a system of rules for the degree
of tonal fusion and illustrates it in a curve which shows the degree of fusion for all intervals over a range of
one octave (Stumpf, 1890, Section 19, p. 176). According to Stumpf (1898, Section 8), the fusion of two
tones is not changed when further tones are added. Nonetheless, musical harmony should be considered
holistically. It is more than the summation of interval consonance /dissonance. Already Cook and Fujisawa
(2006) applied this principle of gestalt psychology to triads (cf. Section 2.3). In this article, this idea is
developed even further and applied to arbitrarily complex harmonies. Relative and logarithmic periodicity,
which we introduce in detail in Section 3, always refer to the harmony as a whole.
Cariani (1999) reviews neurophysiological evidence for interspike interval-based representations for
pitch and timbre in the auditory nerve and cochlear nucleus (see also Tramo et al., 2001). Timings of dis-
charges in auditory nerve ﬁbres reﬂect the time structure of acoustic waveforms, such that the interspike
intervals (i.e. the period lengths) that are produced convey information concerning stimulus periodicities
that are still present in short-term memory. Common to these approaches is that they focus on the auto-
correlation function within one period of the given harmony, considering the interspike intervals between
both successive or non-successive spikes in a discharge pattern. This leads to histograms, called auto-
correlograms , which show high peaks for periods corresponding to the pitch. This procedure works well
for dyads, but for triads and more complex chords the correlation with empirical ratings is relatively low,
which has already been noticed by Ebeling (2007, Section 2.5.3).
McLachlan et al. (2013) conclude from experiments with common dyads and triads that the perception
of consonance /dissonance involves cognitive processes. According to the cognitive incongruence model
of dissonance, proposed by McLachlan et al. (2013), consonance /dissonance is learned to a certain extent
and is based on enculturation, i.e. the natural process of learning a particular culture. Nevertheless, also
in this model, periodicity plays a prominent role (McLachlan et al., 2013, Figure 10). So, consistent with
the results by Lee et al. (2009), a general tendency of musically trained persons toward higher dissonance
ratings is observed, as musicians become better able to use periodicity-based pitch mechanisms.
2.8 Cognitive and further theories
Cognitive science is the interdisciplinary scientiﬁc study of the mind and its processes. It includes research
on intelligence and behaviour, especially focusing on how information is represented, processed, and
transformed. There exists also a series of approaches on harmony perception following this paradigm,
in particular for more complex chords and scales. For instance, Johnson-Laird et al. (2012) propose a
cognitive dual-process theory , employing three basic principles for ranking triads, namely (in order of
decreasing priority) the use of diatonic scales, the central role of the major triad, and the construction of
9

## Page 10

chords out of thirds. These three principles of Western tonal music predict a trend in increasing dissonance.
Within each level of dissonance, roughness according to Hutchinson and Knopo (1978, 1979) can then
predict a detailed rank order.
Temperley and Tan (2013) investigate the emotional connotations of diatonic modes. In the respective
experiments, participants hear pairs of melodies, presented in di erent diatonic modes, and have to judge
which of the two melodies sounds happier. The resulting sequence Ionian MixolydianLydian
DorianAeolianPhrygian (in descending order of preference) is then explained by several principles:
familiarity , e.g. the major mode (Ionian) is the most common mode in classical and popular music, and
sharpness , i.e. the position of the scale relative to the tonic on the circle of ﬁfths. Both these cognitive
theories show high correlation with the empirical results with respect to their application domain, i.e.
chords in Western music and diatonic scales, respectively (cf. Section 4).
There are other, more or less purely mathematical explanations for the origin of chords and scales, e.g.
by group theory (Balzano, 1980; Carey and Clampitt, 1989), ignoring however the sensory psychophysical
basis. Therefore, we will not consider these approaches further here.
3 The periodicity-based method
3.1 Tunings
We now present the periodicity-based method and its rationales in detail, employing relative and logarith-
mic periodicity. We start with the notion of tuning, which we deﬁne with respect to a system of twelve
tones per octave, because in Western music an octave is usually divided into twelve semitones.
Deﬁnition 1. A strictly increasing function Tmapping integers (representing semitone numbers) to pos-
itive real numbers (representing frequencies) is called a tuning . A tuning is called a twelve-tone tuning if
it satisﬁesT(k+12)=2T(k) for every integer k. In this article we only deal with twelve-tone tunings,
so the term tuning will always mean twelve-tone tuning in the rest of this article.
Example 2. The frequencies for the kth semitone in equal temperament with twelve tones per octave
(12-TET) can be computed as fk=2k=12f, where fis the frequency of the ground tone. The respective
frequency ratios fk=fare shown in the third column of Table 1. The corresponding tuning function is
T(k)=2k=12f. The frequency values grow exponentially and not linearly, following the Weber-Fechner
lawin psychophysics, which says that, if the physical magnitude of stimuli grows exponentially, then the
perceived intensity grows only linearly.
In equal temperament and approximations thereof, all keys sound more or less equal. This is essential
for playing in di erent keys on one instrument and for modulation, i.e. changing from one key to another
within one piece of music. Since this seems to be the practice that is currently in use, at least in Western
music, we adopt the equal temperament with twelve tones as our reference system for tunings.
Remark 3. It is sometimes useful to associate a ratio function T0to a tuningT. The ratio functionT0is
a function from the integers to the positive real numbers deﬁned by T0(k)=T(k)=T(0). Since we assume
twelve-tone tuning, the ratio function consequently satisﬁes T0(k+12)=2T0(k).
In equal temperament in Example 2, the associated ratio function is T0(k)=2k=12, as displayed in
the third column of Table 1. The values of the ratio functions for four other tunings are also displayed
in Table 1.
10

## Page 11

Table 1: Table of frequency ratios for di erent tunings. Here, kdenotes the number of the semitone corre-
sponding to the given interval. In parentheses, the relative deviation of the respective frequency ratio from
equal temperament is shown. The maximal deviations dfor the rational tunings listed here are 1.0% (#1)
and 1.1% (#2).
Interval kEqual temperament Pythagorean Kirnberger III Rational tuning #1 Rational tuning #2
Unison 0 1.000 1 /1 (0.00%) 1 /1 (0.00%) 1 /1 (0.00%) 1 /1 (0.00%)
Minor second 1 1.059 256 /243 ( 0.56%) 25 /24 ( 1.68%) 16 /15 (0.68%) 16 /15 (0.68%)
Major second 2 1.122 9 /8 (0.23%) 9 /8 (0.23%) 9 /8 (0.23%) 9 /8 (0.23%)
Minor third 3 1.189 32 /27 ( 0.34%) 6 /5 (0.91%) 6 /5 (0.91%) 6 /5 (0.91%)
Major third 4 1.260 81 /64 (0.45%) 5 /4 ( 0.79%) 5 /4 ( 0.79%) 5 /4 ( 0.79%)
Perfect fourth 5 1.335 4 /3 ( 0.11%) 4 /3 ( 0.11%) 4 /3 ( 0.11%) 4 /3 ( 0.11%)
Tritone 6 1.414 729 /512 (0.68%) 45 /32 ( 0.56%) 17 /12 (0.17%) 7 /5 ( 1.01%)
Perfect ﬁfth 7 1.498 3 /2 (0.11%) 3 /2 (0.11%) 3 /2 (0.11%) 3 /2 (0.11%)
Minor sixth 8 1.587 128 /81 ( 0.45%) 25 /16 ( 1.57%) 8 /5 (0.79%) 8 /5 (0.79%)
Major sixth 9 1.682 27 /16 (0.34%) 5 /3 ( 0.90%) 5 /3 ( 0.90%) 5 /3 ( 0.90%)
Minor seventh 10 1.782 16 /9 ( 0.23%) 16 /9 ( 0.23%) 16 /9 ( 0.23%) 9 /5 (1.02%)
Major seventh 11 1.888 243 /128 (0.57%) 15 /8 ( 0.68%) 15 /8 ( 0.68%) 15 /8 ( 0.68%)
Octave 12 2.000 2 /1 (0.00%) 2 /1 (0.00%) 2 /1 (0.00%) 2 /1 (0.00%)
3.2 Approximating frequency ratios
One important feature of the periodicity-based method with smoothing is the use of integer frequency
ratios. In contrast to other approaches, however, we restrict attention only to integer ratios which di er
from the (possibly irrational) frequency ratios of the real physical signal (with possibly only quasi-periodic
time structure) up to about 1%. The underlying rationale for approximating the actual frequency ratios in
such a way is that human subjects can distinguish frequency di erences of pure tone components only up
to a certain resolution. It is about 0.7% at medium and high frequencies under optimal conditions; at low
frequencies, the relative just noticeable di erence increases and has a value of 3.6% at 100 Hz (Zwicker
and Fastl, 1999). Just intervals, i.e. with integer frequency ratios, rather than tempered, are considered best
in tune, but everything within a band of 1% or even more for more dissonant and ambiguous intervals,
e.g. the tritone, are acceptable to listeners (Hall and Hess, 1984). This also holds, in principle, if the
stimuli are pure sinusoids (V os, 1986, Experiment 2) and is in line with the results of Kopiez (2003)
that professional musicians are able to adapt to equal temperament but cannot really discriminate in their
performance between two tuning systems such as equal temperament and just intonation. In summary,
although there are also interindividual di erences and di erences between sinusoids and complex tones
as stimuli (Zwicker and Fastl, 1999), it seems to be reasonable to estimate the (relative) just noticeable
dierence by 1% for the musically important low frequency range, especially the tones in (accompanying)
chords (Zwicker et al., 1957; Roederer, 2008). The amount of mistuning required to distinguish between
a periodic tone and a tone with one mistuned partial is also in the range of 1% (Moore et al., 1985, 1986;
Hartmann, 1997, Figure 6.12).
Obviously, the frequency ratios in equal temperament are irrational numbers (except for the unison
and its octaves) but for computing (relative) periodicity (deﬁned in Deﬁnition 6) they must be integer
fractions, because otherwise no ﬁnite period length can be determined. Let us thus consider tunings with
integer frequency ratios. The oldest tuning with this property is probably the Pythagorean tuning , shown
in Table 1. Here, frequency relationships of all intervals have the form 2m3nfor some (possibly negative)
integers mandn, i.e. they are based on ﬁfths, strictly speaking, a stack of perfect ﬁfths (frequency ratio
3=2) applying octave equivalence. However, although large numbers appear in the numerators and denom-
inators of the fractions in Pythagorean tuning, the relative deviations with respect to equal temperament
11

## Page 12

xmin=(1 d)x;
xmax=(1+d)x;
al=bl=bxc=1;
ar=br=(bxc+1)=1;
a=b=[x]=1;
while (a=b<xminorxmax<a=b)do
x0=2x a=b;
if(x<a=b)then
ar=br=a=b;
k=b(x0bl al)=(ar x0br)c;
al=bl=(al+k ar)=(bl+k br);
else
al=bl=a=b;
k=b(ar x0br)=(x0bl al)c;
ar=br=(ar+k al)=(br+k bl);
end if
a=b=(al+ar)=(bl+br);
end while
Figure 5: Approximating real numbers xby fractions y=a=bwith maximal relative deviation d=jy=x 1j.
We use the ﬂoor function bxchere, which yields the largest integer less than or equal to x, and the rounding
function [ x], which rounds xto the nearest integer. The procedure enumerates e ciently, in contrast to
continued fraction expansion, every integer fraction y=a=bwith the property that there is no other
fraction with smaller numerator and denominator and smaller deviation dfrom ywith respect to x(cf.
Foriˇsek, 2007).
(shown in parentheses in Table 1) may be relatively high. For example, the tritone (semitone 6, frequency
ratio 729 /512) is still slightly mistuned (deviation 0.68%). On the other hand, the major third (semitone 4,
frequency ratio 81 =64, deviation 0.45%) is tuned more accurately than usually assumed in just intonation
(frequency ratio 5 =4, deviation -0.79%). Hence, the Pythagorean tuning is not in line with the results of
psychophysics mentioned above, that the just noticeable di erence of pitch perception is about 1%.
Let us therefore look for tunings, where the relative deviation dwith respect to equal temperament
is approximately 1% for each tone. In the literature, historical and modern tunings are listed, e.g. Kirn-
berger III (cf. Table 1). However, they are also only partially useful in this context, because they do not
take into account the fact on just noticeable di erences explicitly. In principle, this also holds for the adap-
tive tunings introduced by Sethares (2005), where simple integer ratios are used and scales are allowed to
vary. An adaptive tuning can be viewed as a generalised dynamic just intonation, which ﬁts well with mu-
sical practice, because the frequencies for one and the same pitch category may vary signiﬁcantly during
the performance of a piece of music, dependent on the musical harmonic context.
We therefore introduce the rational tuning now, which takes the fractions with smallest possible de-
nominators, such that the relative deviation with respect to equal temperament is just below a given per-
centage d. Frequency ratios fi=fcan be approximated by fractions algorithmically by employing the so-
called Stern-Brocot tree (Graham et al., 1994; Fori ˇsek, 2007). It induces an e ective procedure for approx-
imating numbers xby fractions y=a=bwith some precision, i.e. maximal relative deviation d=jy=x 1j.
The main idea is to perform a binary search between two bounds: al=bl(left) and ar=br(right). We start
with the two integer numbers that are nearest to x, e.g. 1=1 and 2=1, and repeat computing the so-called
mediant a=b=(al+ar)=(bl+br), until xis approximated with the desired precision. Figure 5 shows an
improved, e cient version of this procedure, following the lines of Fori ˇsek (2007).
12

## Page 13

0%0.2%0.4%0.6%0.8%1.0%1.2%1.4%1.6%1.8%2.0%d
k
01 2 3 4 5 6 7 8 9 10 11 121/1 2/13/24/35/3
5/47/4
6/57/5
8/59/57/6
8/7
10/713/7
9/815/810/9
16/9
17/917/10
19/1013/1114/1121/11
17/1219/1223/1214/1321/13
22/1323/1325/13
15/1419/14
25/1416/1517/15
19/1528/15
17/16
19/1621/16
23/1625/16
27/16Figure 6: Integer frequency ratios a=band their deviation dfrom the kth semitone in equal temperament
forb16 and d2%.
Table 1 shows two instances of the rational tuning, namely for d=1:0% (#1) (cf. Stolzenburg, 2009,
2010) and for d=1:1% (#2). They can be considered as special just-intonation systems, di ering only for
the tritone and the minor seventh. Although relative periodicity values may vary signiﬁcantly, if di erent
frequency ratios are used, taking e.g. 16 /9 instead of 9 /5 as the frequency ratio for the minor seventh, the
evaluation of the periodicity-based method with smoothing (see Section 4) shows that the results remain
relatively stable and correlate well with empirical ratings, provided that we employ the rational tunings #1
and #2, which implement that the just noticeable di erence of pitch perception is about 1%. If we adopt
the frequency ratios e.g. from Pythagorean tuning, which is not psychophysically motivated in this way,
the correlation with empirical ratings of harmonies decreases. Figure 6 shows possible integer frequency
ratios and their deviation from the nearest semitone in equal temperament.
The approximation procedure for frequency ratios can also be used to generate (equal tempera-
ment) tone scales by an interval, e.g. the perfect ﬁfth. In this case, we look for a tuning in equal tem-
perament with ntones per octave, such that the perfect ﬁfth in just intonation (frequency ratio 3 =2)
is approximated as good as possible. Therefore, we develop a fraction y=a=bwith 2a=b3=2,
where ais the number of the semitone representing the ﬁfth. Consequently we have to approximate
13

## Page 14

x=log2(3=2)0:585 by y. The corresponding sequence of mediants (between 0 =1 and 1=1) is
1=2;2=3;3=5;4=7;7=12;17=29;24=41;31=53; ::: It shows a=b=7=12 among others. Thus,
semitone a=7 gives the perfect ﬁfth in the tone scale with b=12 tones per octave with high precision.
Interestingly, only from this mediant on, the deviation of a=bwith respect to x(which is logarithmic with
respect to the relative frequency) is below 1%, namely  0:27%. Hence we obtain 12-TET (see Example 2)
by applying once again that the just noticeable di erence between pitches for humans is about 1%.
Note that, although we compute the frequency ratios for rational tunings by the approximation proce-
dure in Figure 5, this does not mean that the human auditory system somehow performs such a compu-
tation. We simply assume here, consistent with the results from psychophysics and neuroacoustics, that
the resolution of periodicity pitch in the brain is limited. The oscillator neurons in the brain with intrinsic
oscillation (cf. Section 2.6) provide evidence for this. Incidentally, the time constant 2 T=0:8 ms corre-
sponds to a frequency of 1250 Hz, which roughly coincides with the capability of the auditory system to
identify the repetition rate of a complex tone, namely up to about f=1500 Hz (cf. Section 2.5). Further-
more, the lowest frequency audible by humans is about 20 Hz. Its ratio with the border frequency fis only
slightly more than 1%. This percentage, corresponding to the above-mentioned just noticeable di erence,
is the only parameter of the presented approach on harmony perception.
3.3 Harmonies and measures of harmoniousness
We now deﬁne the notions harmony and measure of harmoniousness formally in a purely mathematical
way and give some examples.
Deﬁnition 4. Assume a ﬁnite non-empty set H=ff1;:::; fkgofkpositive real numbers fi>0 (where
1ik) that represent frequencies. Then His called a harmony and elements of Hare called tones .
Iffis the minimum of Hthen H=ff1=f;:::; fk=fgis called the set of frequency ratios of the harmony
H. The set of all harmonies H0with the same set of frequency ratios is called a class of harmonies and
denoted [ H]=fH0jH0=Hg. Furthermore, if all frequency ratios of a harmony are rational numbers then
we say that the harmony and the respective class of harmonies are rational ; otherwise we say that they are
irrational . Ameasure of harmoniousness His a function mapping harmonies to real numbers such that
any two harmonies with the same set of frequency ratios both map to the same real number. Consequently,
Hinduces a real-valued function on the set of harmony classes, which we also denote by H.
Example 5. Consider the harmonies in Table 2(a). The harmonies A0through A4represent A major triads
in various tuning systems, pitch standards and musical spacing. The harmony Ebelongs to the same
harmony class as A0and represents an E major triad in just intonation under the standard pitch. We see
that all harmonies but A3are rational. The harmonies A0,A1, and Ebelong to the same rational harmony
class [1=1;5=4;3=2]. It is important to note that all harmonies A0through A3are notated in the same way
in the usual musical notation.
In Section 2, we have mentioned several measures of harmoniousness, e.g. gradus suavitatis and rel-
ative periodicity. Table 2(b) shows their values for some harmonies. We will come back to this table and
explain it in more detail later, namely after the (formal) deﬁnition of relative periodicity (Deﬁnition 6).
3.4 Relative periodicity
We now introduce the concept of relative periodicity, at ﬁrst informally with an example: For this, we
further consider the harmony A0from Table 5(a), i.e. the A major triad in root position (cf. Figure 1(a))
and in just intonation. It consists of three tones with absolute frequencies f1=440 Hz (lowest tone),
f2=550 Hz (major third), and f3=660 Hz (perfect ﬁfth). For the sake of simplicity, we ignore possible
overtones and consider just the three pure tone components here. Figure 7(a)–(c) shows the sinusoids
14

## Page 15

Table 2: Example harmonies.
(a) Major triads in various tuning systems, pitch standards and musical spacing. As tunings we here
consider rational tuning (#1 or #2), the Pythagorean tuning, and twelve-tone equal temperament
(12-TET). Rational tunings #1 and #2 yield identical frequency values in the examples selected
here, so in the Tuning column we do not specify #1 or #2 after the word Rational tuning. Also note
that the four entries Rational tuning in the Tuning column could also be replaced by Just intonation.
Harmony Rationality Harmony class Tuning Pitch Spacing
A0f440;550;660g Rational [1 =1;5=4;3=2] Rational tuning Standard A4–C ]5–E5
A1f432;540;648g Rational [1 =1;5=4;3=2] Rational tuning Classical A4–C ]5–E5
A2f440;556:875;660g Rational [1 =1;81=64;3=2] Pythagorean Standard A4–C ]5–E5
A3f440;554:365;659:255g Irrational [1 =1;21=3;27=12] 12-TET Standard A4–C ]5–E5
A4f440;660;1100g Rational [1 =1;3=2;5=2] Rational tuning Standard A4–E5–C ]6
Ef660;825;990g Rational [1 =1;5=4;3=2] Rational tuning Standard E5–G ]5–B5
(b) Relative periodicity and gradus suavitatis. The gradus suavitatis can be derived from the prime
factorisation of the least common multiple (lcm) of the harmonic-series representation. The relative
periodicity of the respective harmony is simply its minimum.
Identiﬁer Harmonic series lcm Factorisation Gradus suavitatis Relative periodicity
A major triad f4;5;6g 60 2235 9 4
M2major second f8;9g 72 23328 8
M3major third f4;5g 20 225 7 4
T tritone f5;7g 35 57 11 5
for the three pure tone components and Figure 7(d) their superposition, i.e. the graph of the function
s(t)=sin(!1t)+sin(!2t)+sin(!3t), where!i=2fiis the respective angular frequency.
How can the periodicity of the signal s(t) in Figure 7(d) be determined? One possibility is to apply
continuous autocorrelation , i.e. the cross-correlation of a signal with itself. For the superposition of pe-
riodic functions s(t) over the reals, it is deﬁned as the continuous cross-correlation integral of s(t) with
itself, at lag , as follows:
()=lim
T!11
2TZ+T
 Ts(t)s(t ) dt=1
23X
i=1cos(!i)
The autocorrelation function reaches its peak at the origin. Other maxima indicate possible period lengths
of the original signal. Furthermore, possibly existing phase shifts are nulliﬁed, because we always obtain
a sum of pure cosines with the same frequencies as in the original signal as above. The respective graph
of() for the major triad example is shown in Figure 7(e). As one can see, it has a peak after four times
the period length of the lowest tone (cf. Figure 7(a)). This corresponds to the periodicity of the envelope
frequency, to which respective neurons in the inner cortex respond.
In general, overtones have to be taken into account in the computation of the autocorrelation function,
because real tones have them. In many approaches, complex tones are made up from sinusoidal partials
in this context. Their amplitudes vary e.g. as 1 =k, where kis the number of the partial, ranging from 1 to
10 or similar (Hutchinson and Knopo , 1978, 1979; Sethares, 2005; Ebeling, 2007, 2008), although the
number of partials can be higher in reality, if one looks at the spectra of musical instruments. In contrast
to this procedure, we calculate relative periodicity, abstracting from concrete overtone spectra, by simply
considering the frequency ratios of the involved tones. Figure 7(f) illustrates this by showing the periodic
patterns of the three tone components of the major triad as solid boxes one upon the other. As one can see,
15

## Page 16

(a)
(b)
(c)
(d)
(e)
(f)
Figure 7: Sinusoids of the major triad in root position (a)–(c), their superposition (d), and corresponding
autocorrelation function () in (e). Figure 7(f) shows the general periodicity structure of the chord, ab-
stracting from concrete overtone spectra and amplitudes. The solid boxes show the periodic patterns of the
three tone components one upon the other. The dashed lines therein indicate the greatest common period
of all tone components, called granularity by Stolzenburg (2012). Its frequency corresponds to their least
common overtone.
16

## Page 17

the period length of the chord is (only) four times the period length of the lowest tone for this example.
This ratio is the relative periodicity h. It only depends on the corresponding harmony class, which must
be rational, as already stated in Section 3.2.
For a harmony class [ a1=b1;:::; ak=bk] (where all fractions ai=biare in lowest terms, i.e. aiandbiare
coprime), the value of hcan be computed as lcm( b1;:::; bk), i.e., it is the least common multiple (lcm) of
the denominators of the frequency ratios. This can be seen as follows: Since the relative period length of
the lowest tone T1=f1=f1is 1, we have to ﬁnd the smallest integer number that is an integer multiple
of all relative period lengths Ti=f1=fi=bi=aifor 1<ik. Since after aiperiods of the ith tone, we
arrive at the integer bi,hcan be computed as the least common multiple of all bi. For the harmony class
[1=1;5=4;3=2] of A0e.g., we obtain a2T2=32=3=2=b2forT2=f1=f2=2=3. Together with b3=4,
ignoring b1=1, which is always irrelevant, we get h=lcm(1;2;4)=4 as expected. Let us now capture
the notion of relative periodicity formally.
Deﬁnition 6. Assume that H=ff1;:::; fkgis a rational harmony, fis the minimum of H, and fi=f=ai=bi
for 1ikand coprime positive integers aiandbi. Denote h=lcm(b1;:::; bk). Then his called relative
periodicity and the set Hharm=hH=fhai=bij1ikgis called the harmonic-series representation of
the rational harmony H.
Example 7. The set of frequency ratios for the harmonies A0,A1, and Efrom Table 5(a) is f1=1;5=4;3=2g.
Thus, as already mentioned, their relative periodicity is 4 and their harmonic-series representation is
f4;5;6g. The relative periodicity of A2is 64 and its harmonic-series representation is f64;81;96g.
Note that in all cases of Example 7, the relative periodicity is the minimal element of the harmonic-
series representation. It can easily be shown that this is not a coincidence but a consequence of Deﬁnition 6.
It always holds that h=min( Hharm). This equation may be used as an alternative way of deﬁning the key
concept: Relative periodicity can be deﬁned as the minimum of the harmonic-series representation of a
given rational harmony.
Interestingly, both relative periodicity and gradus suavitatis are functions of the harmonic-series rep-
resentation: While relative periodicity corresponds to its minimum, the gradus suavitatis depends on the
least common multiple of the harmonic-series representation (cf. Section 2.2). Thus, relative periodicity
only considers the lowest element in the harmonic-series representation, whereas Euler’s formula takes
into account more complex harmonic relations of all its elements. Some values of both measures of har-
moniousness are listed in Table 2(b). Note that on the one hand relative periodicity may not change for
harmonies of increasing complexity: For instance, relative periodicity is the same for the major triad in
root position and the major third (which is contained in the major triad) in just intonation (called AandM3
in Table 2(b)), while their gradus suavitatis values di er. On the other hand, both measures of harmonious-
ness produce di erent orderings: For example, relative periodicity predicts the preference tritone major
second (called TandM2in Table 2(b)) which corresponds to the empirical ranking (cf. Table 3), while it is
the other way round for the gradus suavitatis: We have h(T)=5<h(M2)=8, but  (M2)=8< (T)=11.
3.5 A hypothesis on harmony perception
The rationale behind employing relative periodicity as a measure of harmoniousness is given by the recent
results from neuroacoustics on periodicity detection in the brain, which we already reviewed in Sec-
tion 2.6. Clearly, di erent periodicity pitches must be mapped on di erent places on the periodicity map.
However, a general observation is that harmony perception is mostly independent of transposition, i.e.
pitch shifts. For instance, the perceived consonance /dissonance of an A major triad should be more or
less the same as that of one in B. This seems to be in accordance with the logarithmic organisation of the
neuronal periodicity map. There is no problem with the fact that periodicity detection in the brain is not
available for the high frequency range (cf. Section 2.5), because the fundamental tones (not necessarily
17

## Page 18

the overtones) of real musical harmonies usually are below this threshold, and this su ces to determine
periodicity.
In line with McLachlan et al. (2013), one may conclude that harmony perception requires in addition
some cognitive process or property ﬁlter (Licklider, 1962), conveying information concerning stimulus
periodicities in (short-term) memory. The latter is also required to explain harmony perception when
tones occur consecutively. Because of this, we do not consider absolute period length here, but relative
periodicity. As we shall see (in Section 4), this measure shows very high correlation with empirical ratings
of harmonies, especially higher than that of roughness (Hutchinson and Knopo , 1978, 1979) which only
regards the auditory processing in the ear and not the brain. This is in line with the result of Cousineau
et al. (2012) that the quality of roughness (induced by beating) constitutes an aesthetic dimension that is
distinct from that of dissonance.
It is a feature of the periodicity-based method with smoothing that the actual amplitudes of the tone
components in the given harmony are ignored. Harmonic overtone spectra are irrelevant for determining
relative periodicities, because the period length of a waveform of a complex tone with harmonic overtones
is identical with that of its fundamental tone. We always obtain h=1, since the frequencies of harmonic
overtones are integer multiples of the fundamental frequency. All frequency ratios [1 =1;2=1;3=1;:::] have
1 as denominator in this case. Therefore, relative periodicity his independent of concrete amplitudes and
also phase shifts of the pure tone components, i.e. tones with a plain sinusoidal waveform. Incidentally,
information on the waveform of the original signal is lost in the auditory processing, because neuronal
activity usually has the form of spike trains (Langner and Schreiner, 1988; Cariani, 1999; Tramo et al.,
2001). Information on phase is also lost because of the phase-locking mechanism in the brain (Langner
and Schreiner, 1988; Meddis and Hewitt, 1991; Lee et al., 2009). However, the information on periodicity
remains, which is consistent with the periodicity-based method proposed here.
Also from a more practical point of view, it seems plausible that harmony perception depends more on
periodicity than on loudness and timbre of the sound. It should not matter much whether a chord is played
e.g. on guitar, piano, or pipe organ. Of course, this argument only holds for tones with harmonic overtone
spectra. If we have inharmonic overtones in a complex tone such as in Indian, Thai, or Indonesian gong
orchestra, i.e. Gamelan music, or stretched or compressed timbres as considered by Sethares (2005), then
it holds h>1 for the relative periodicity value of a single tone, i.e., we have an inherently increased har-
monic complexity (Parncutt, 1989). Average listeners seem to prefer low or middle harmonic complexity,
e.g. baroque or classical style on the one hand and impressionism and jazz on the other hand, which of
course have to be analysed as complex cultural phenomena. In this context, Parncutt (1989, pp. 57-58)
speaks of optimal dissonance that gradually increased during the history in Western music.
We therefore set up the following hypothesis on harmony perception : The perceived consonance of
a harmony decreases as the relative periodicity hincreases. For the major triad in root position, we have
h=4 (cf. Example 7), which is quite low. Thus, the predicted consonance is high. This correlates very
well with empirical results. Relative periodicity gives us a powerful approach to the analysis of musical
harmony perception. We evaluate this hypothesis later at length (Section 4). But beforehand, we will state
some reﬁnement of relative periodicity.
3.6 Logarithmic periodicity and smoothing
Throughout the rest of this article, we consider relative periodicity has measure of harmoniousness and
also its base-2 logarithm log2(h), called logarithmic periodicity henceforth. The rationale for taking the
logarithm of relative periodicity is given again by the recent results from neuroacoustics on periodicity
detection in the brain, namely the logarithmic organisation of the neuronal periodicity map in the brain
(cf. Section 2.6). Since one octave corresponds to a frequency ratio of 2, we adopt the base-2 logarithm.
Obviously, as log2is an increasing function, logarithmic periodicity and relative periodicity lead to iden-
18

## Page 19

tical harmony rankings. This changes, however, if we apply the concept of smoothing (see Deﬁnition 9).
For this, harmonies must be given by sets of semitones, as follows.
Deﬁnition 8. Aset of semitones S =fs1;:::; sngis a set of (possibly negative) integer numbers, usually
containing 0. Such a set Smay be shifted byisemitones, deﬁned by Si=fs1 i;:::; sn ig. IfSis a set
of semitones andT0a ratio function, we write T0(S) forfT0(s1);:::;T0(sn)g.
Deﬁnition 9. LetT0be a ratio function, S=fs1;:::; snga set of nsemitones, andHa measure of harmo-
niousness. Then, the value of Hmay be smoothed , obtaining the (smoothed) measure of harmoniousness
Hby averaging over the shifted semitone sets of S, as follows:
H(S)=1
nX
i2SH(T0(Si))
Most comparisons with empirical rankings yield comparably favourable results, if (raw) relative peri-
odicity is employed, which can be computed without reference to any tuning system. However, in some
cases there is more than one integer fraction approximating a given frequency ratio with the required pre-
cision of about 1%. Therefore, for harmonies given as semitone sets, smoothing averages over several
related periodicity values. Only the tones of the given harmony are used as reference tones in the proce-
dure according to Deﬁnition 9, because otherwise the frequency ratios often deviate more than 1%. For
instance, for the perfect ﬁfth with the set of semitones S=f0;7gwe do not consider e.g. the shifted set
S10=f 10; 3gwhich corresponds to the frequency ratios f9=16;5=6gin rational tuning (#1 and #2). The
quotient of both frequency ratios is 40 =27, which not only deviates from the desired frequency ratio of
the perfect ﬁfth by more than 1% but also has an unnecessarily large denominator (that corresponds to its
relative periodicity).
Example 10. Let us consider the ﬁrst inversion of the diminished triad consisting of the tones A4, C5,
and F]5 (see Figure 1(c)). The corresponding set of semitones is S=S0=f0;3;9g, where the lowest
tone has the number 0 and is associated with the frequency ratio 1 =1 (unison). We use the corresponding
frequency ratios according to rational tuning #2, i.e. T0(S)=f1=1;6=5;5=3g. Hence, its relative periodicity
ish0=lcm(1;5;3)=15. In order to smooth and hence stabilise the calculated periodicity value, we have
to consider also the shifted sets of semitones S3=f 3;0;6gandS9=f 9; 6;0g. As a consequence of
Deﬁnition 1, for semitones associated with a negative number  n, we take the frequency ratio of semitone
12 nand halve it, i.e., we do not assume octave equivalence here. Therefore, we get the frequency
ratiosT0(S3)=f5=6;1=1;7=5gandT0(S9)=f3=5;7=10;1=1gwith relative periodicity values h3=5=6
lcm(6;1;5)=25 and h9=3=5lcm(5;10;1)=6, respectively. Their arithmetic average and hence the
smoothed relative periodicity is h=(15+25+6)=315:3. The smoothed logarithmic periodicity in this
case is log2(h)=(log2(15)+log2(25)+log2(6))=33:7.
Note that, as a side e ect of the procedure, for logarithmic periodicity we implicitly obtain the geo-
metric average over all hvalues instead of the arithmetic average. Because of the Weber-Fechner law and
the logarithmic mapping of frequencies on both the basilar membrane in the inner ear and the periodicity
map in the brain, this seems to be entirely appropriate.
Example 11. As a further example, we consider once again the major triad, but this time spread over more
than one octave, consisting of the tones C3 (lowest tone), E4 (major tenth), and G4 (perfect twelfth) with
corresponding numbers of semitones f0;16;19g. In contrast to other approaches, we do not project the
tones into one octave, but apply a factor 2 for each octave. Thus by Remark 3, the frequency ratio for the
major tenth with corresponding semitone number 16 is T0(16)=2T0(4)=25=4=5=2 in lowest terms.
The frequency ratios of the whole chord are f1=1;5=2;3=1g. Hence, h=lcm(1;2;1)=2 and log2(h)=1.
Smoothing does not change the results here.
19

## Page 20

Perceived consonance /dissonance certainly depends on overtones to a certain extent. Since concrete
amplitudes are neglected in the periodicity-based method, there are ambiguous cases where harmonic
overtones cannot be distinguished from extra tones coinciding with these overtones. This holds for Ex-
ample 11, because it contains the tones C3 and G4, which are more than an octave apart, namely n=19
semitones (perfect twelfth), with frequency ratio 3 =22=3=1. It cannot be distinguished from a complex
tone with C3 as fundamental tone and harmonic overtones, because its third partial corresponds to G4.
However, the waveforms normally di er here: In the former case the amplitudes of C3 and G4 may be
almost equal, whereas in the latter case the amplitude aof the overtone G4 may be signiﬁcantly lower
than that of C3. The superposition of both sinusoids can be stated roughly as sin( !t)+asin(3!t), where
!=2fwith f131 Hz (the frequency of C3), and tis the time. For 1=3a1=9, the higher tone
component G4 does not induce any additional local extrema in the waveform, which would correspond to
additional spikes in the neuronal activity. It seems that people tend to underestimate the number of pitches
in such chords (Dewitt and Crowder, 1987; McLachlan et al., 2013, p. 5). Nonetheless, even in such am-
biguous cases, the periodicity-based method yields meaningful results and high correlations to empirical
ratings of harmony perception for realistic chords (see Section 4.2).
Example 12. Let us now consider the minor triad in root position. From the respective frequency ratios in
rational tuning (#1 or #2) f1=1;6=5;3=2g, we easily can read o the relative periodicity h=lcm(1;5;2)=
10. Smoothing does not change the result here. Here it is important to note that pitch and periodicity
are orthogonal dimensions of harmony perception on the neuronal tonotopic map (cf. Section 2.6). If
we ignore this and identify tone pitch and periodicity pitch, we obtain e.g. for the A minor triad in root
position (cf. Figure 1(b)) the tone F2 as missing fundamental (with 1 =h=1=10 of the lowest frequency in
the harmony) that does not at all belong to the chord.
Example 13. Let us ﬁnally calculate the periodicity of the complete chromatic scale, i.e. the twelve
tones constituting Western music. For this, we compute the least common multiple of the denomina-
tors of all frequency ratios according to rational tuning #2 within one octave (cf. Table 1). We obtain
h=lcm(1;15;8;5;4;3;5;2;5;3;5;8)=120. Smoothing yields h168:2 and log2(h)7:4. Thus inter-
estingly, the (smoothed) logarithmic periodicity for the chromatic scale is just within the biological bound
of 8 octaves, which can be represented in the neuronal periodicity map (cf. Section 2.6).
4 Results and evaluation
Let us now apply the periodicity-based method and other theories on harmony perception to common
musical harmonies and correlate the obtained results with empirical results (Malmberg, 1918; Roberts,
1986; Schwartz et al., 2003; Johnson-Laird et al., 2012; Temperley and Tan, 2013). The corresponding
experiments are mostly conducted by (cognitive) psychologists, where the harmonies of interest are pre-
sented singly or in context. The listeners are required to judge the consonance /dissonance, using an ordinal
scale. All empirical and theoretical consonance values are either taken directly from the cited references
or calculated by computer programs according to the respective model on harmony perception. In par-
ticular, the smoothed periodicity values handlog2(h) are computed by a program, implemented by the
author of this article, written in the declarative programming language ECLiPSe Prolog (Apt and Wallace,
2007; Clocksin and Mellish, 2010). A table listing the computed harmoniousness values for all 2048 pos-
sible harmonies within one octave consisting of up to 12 semitones among other material is available at
http://artint.hs-harz.de/fstolzenburg/harmony/ , including a related technical report version
of this article (Stolzenburg, 2013).
In our analyses, we correlate the empirical and the theoretical ratings of harmonies. Since in most
cases only data on the ranking of harmonies is available, we mainly correlate rankings. Nevertheless,
correlating concrete numerical values yields additional interesting insights (see Section 4.2). For the sake
20

## Page 21

Table 3: Consonance rankings of dyads. The respective sets of semitones are given in braces, raw val-
ues of the respective measures in parentheses. The empirical rank is the average rank according to the
summary given by Schwartz et al. (2003, Figure 6). The roughness values are taken from Hutchinson
and Knopo (1978, Appendix). For computing the sonance factor (Hofmann-Engl, 2004, 2008), the Har-
mony Analyzer 3.2 applet software has been used, available at http://www.chameleongroup.org.
uk/software/piano.html . For these models, always C4 (middle C) is taken as the lowest tone. For
smoothed relative periodicity and percentage similarity (Gill and Purves, 2009), the frequency ratios from
rational tuning #2 are used.
Empirical Smoothed relative
Interval rank Roughness Sonance factor Similarity periodicity
Unisonf0;0g 1 2 (0.0019) 1-2 (1.000) 1-2 (100.00%) 1-2 (1.0)
Octavef0;12g 2 1 (0.0014) 1-2 (1.000) 1-2 (100.00%) 1-2 (1.0)
Perfect ﬁfthf0;7g 3 3 (0.0221) 3 (0.737) 3 (66.67%) 3 (2.0)
Perfect fourthf0;5g 4 4 (0.0451) 4 (0.701) 4 (50.00%) 4-5 (3.0)
Major thirdf0;4g 5 6 (0.0551) 5 (0.570) 6 (40.00%) 6 (4.0)
Major sixthf0;9g 6 5 (0.0477) 6 (0.526) 5 (46.67%) 4-5 (3.0)
Minor sixthf0;8g 7 7 (0.0843) 7 (0.520) 9 (30.00%) 7-8 (5.0)
Minor thirdf0;3g 8 10 (0.1109) 8 (0.495) 7 (33.33%) 7-8 (5.0)
Tritonef0;6g 9 8 (0.0930) 11 (0.327) 8 (31.43%) 9 (6.0)
Minor seventhf0;10g 10 9 (0.0998) 9 (0.449) 10 (28.89%) 10 (7.0)
Major secondf0;2g 11 12 (0.2690) 10 (0.393) 11 (22.22%) 12 (8.5)
Major seventhf0;11g 12 11 (0.2312) 12 (0.242) 12 (18.33%) 11 (8.0)
Minor secondf0;1g 13 13 (0.4886) 13 (0.183) 13 (12.50%) 13 (15.0)
Correlation r .967 .982 .977 .982
of simplicity and consistency, we always compute Pearson’s correlation coe cient r, which coincides
with Spearman’s rank correlation coe cient on rankings, provided that there are not too many bindings,
i.e. duplicate values. For determining the signiﬁcance of the results, we apply rp
n 2=p
1 r2tn 2,
i.e. we have n 2 degrees of freedom in Student’s tdistribution, where nis the number of corresponding
ranks or values. We always perform a one-sided test whether r0.
4.1 Dyads
Table 3 shows the perceived and computed consonance of dyads (intervals). The empirical rank is the
average ranking according to the summary given by Schwartz et al. (2003, Figure 6), which includes the
data by Malmberg (1918). Table 4 provides a more extensive list of approaches on harmony perception,
indicating the correlation of the rankings together with its signiﬁcance. As one can see, the correlations
of the empirical rating with the sonance factor and with smoothed relative and smoothed logarithmic
periodicity show the highest correlation ( r=:982).
However, for dyads, almost all correlations of the di erent approaches are highly statistically sig-
niﬁcant. Exceptions are complex tonalness (Parncutt, 1989, p. 140) and smoothed relative periodicity, if
Pythagorean tuning or Kirnberger III are employed, but neither of these tunings is psychophysically mo-
tivated by the just noticeable di erence of pitch perception of about 1% (cf. Section 3.2). In contrast to
this, smoothed relative and smoothed logarithmic periodicity employing one of the rational tunings from
Table 1 show high correlation.
If periodicity detection in the brain is an important mechanism for the perception of consonance, the
periodicity-based method with smoothing should show high correlation with neurophysiological data as
well, and in fact this holds: Bidelman and Krishnan (2009) found auditory nerve and brainstem correlates
of musical consonance and detected that brainstem responses to consonant intervals were more robust
and yielded stronger pitch salience than those to dissonant intervals. They compared perceptual consonant
21

## Page 22

Table 4: Correlations of several consonance rankings with empirical ranking for dyads. For percentage
similarity (Gill and Purves, 2009, Table 1), gradus suavitatis (Euler, 1739), consonance value (Brefeld,
2005), and the smoothed 
measure (Stolzenburg, 2012), the frequency ratios from rational tuning #2 (see
Table 1) are used.
Approach Correlation rSigniﬁcance p
Sonance factor (Hofmann-Engl, 2004, 2008) .982 .0000
Smoothed relative and smoothed logarithmic periodicity (rational tuning #2) .982 .0000
Consonance raw value (Foltyn, 2012, Figure 5) .978 .0000
Percentage similarity (Gill and Purves, 2009, Table 1) .977 .0000
Roughness (Hutchinson and Knopo , 1978, Appendix) .967 .0000
Smoothed gradus suavitatis (Euler, 1739) .941 .0000
Consonance value (Brefeld, 2005) .940 .0000
Pure tonalness (Parncutt, 1989, p. 140) .938 .0000
Smoothed relative and smoothed logarithmic periodicity (rational tuning #1) .936 .0000
Dissonance curve (Sethares, 2005, Figure 6.1) .905 .0000
Smoothed 
measure (Stolzenburg, 2012) .886 .0000
Generalised coincidence function (Ebeling, 2008, Figure 3B) .841 .0002
Smoothed relative periodicity (Pythagorean tuning) .817 .0003
Smoothed relative periodicity (Kirnberger III) .796 .0006
Complex tonalness (Parncutt, 1989, p. 140) .738 .0020
ratings of n=9 musical intervals and estimates of neural pitch salience derived from the respective
brainstem frequency-following responses. The correlation between the ranking of neural pitch salience
(see Bidelman and Krishnan, 2009, Figure 3) and smoothed relative or smoothed logarithmic periodicity
(with rational tuning #2) is r=:833, which is still signiﬁcant with p=:0027.
Last but not least, it should be noted that the so-called major proﬁle , investigated by Krumhansl (1990,
Figure 3.1), also corresponds quite well with the empirical consonance ranking. Here, an ascending or
descending major scale is presented to test persons. A probe tone comes next. The listener’s task is to rate
it as a completion of the scale context. The correlation in this case is r=:846, which is still signiﬁcant
with p=:0001.
4.2 Triads and more
Table 5 shows the perceived and computed consonance of common triads (cf. Figure 1). There are several
empirical studies on the perception of common triads (Roberts, 1986; Cook, 2009; Johnson-Laird et al.,
2012). But since the experiments conducted by Johnson-Laird et al. (2012, Experiment 1) are the most
comprehensive, because they examined all 55 possible three-note chords, we adopt this study as reference
for the empirical ranking here. Note that Johnson-Laird et al. (2012) designed the register of the pitch
classes in the chords, i.e. the spacing, so that the chords spread over about an octave and a half, in order
to make the chords comparable with those that occur in music. All the cited empirical studies on triads
are consistent with the following preference ordering on triads: major minorsuspendeddiminished
augmented, at least for chords in root position. However, the ordinal ratings of minor and suspended
chords do not di er very much. Again, the summary table (Table 6) reveals highest correlations with the
empirical ranking for smoothed relative and smoothed logarithmic periodicity, if the underlying tuning
is psychophysically motivated. Roughness (Hutchinson and Knopo , 1978, 1979) and the sonance factor
(Hofmann-Engl, 2004, 2008) yield relatively bad predictions of the perceived consonance of common
triads.
22

## Page 23

Table 5: Consonance rankings of common triads. The empirical rank is adopted from Johnson-Laird et al.
(2012, Experiment 1), where the tones are reduced to one octave in the theoretical analysis here. The
roughness values are taken from Hutchinson and Knopo (1979, Table 1), where again C4 (middle C)
is taken as the lowest tone. For smoothed relative periodicity and percentage similarity (Gill and Purves,
2009), the frequency ratios from rational tuning #2 are used. The dual-process theory (Johnson-Laird et al.,
2012, Figure 2) as a cognitive theory only provides ranks, not numerical raw values.
Empirical Smoothed Relative Dual
Chord class rank Roughness Instability Similarity periodicity process
Majorf0;4;7g 1 (1.667) 3 (0.1390) 1 (0.624) 1-2 (46.67%) 2 (4.0) 2
f0;3;8g 5 (2.889) 9 (0.1873) 5 (0.814) 8-9 (37.78%) 3 (5.0) 1
f0;5;9g 3 (2.741) 1 (0.1190) 4 (0.780) 5-6 (45.56%) 1 (3.0) 3
Minorf0;3;7g 2 (2.407) 4 (0.1479) 2 (0.744) 1-2 (46.67%) 4 (10.0) 4
f0;4;9g10 (3.593) 2 (0.1254) 3 (0.756) 5-6 (45.56%) 7 (12.0) 5
f0;5;8g 8 (3.481) 7 (0.1712) 6 (0.838) 8-9 (37.78%) 10 (15.0) 6
Suspendedf0;5;7g 7 (3.148) 11 (0.2280) 8 (1.175) 3-4 (46.30%) 5 (10.7) 7
f0;2;7g 6 (3.111) 13 (0.2490) 11 (1.219) 3-4 (46.30%) 9 (14.3) 9
f0;5;10g 4 (2.852) 6 (0.1549) 9 (1.190) 7 (42.96%) 6 (11.0) 8
Diminishedf0;3;6g12 (3.889) 12 (0.2303) 12 (1.431) 13 (32.70%) 12 (17.0) 12
f0;3;9g 9 (3.519) 10 (0.2024) 7 (1.114) 10-11 (37.14%) 11 (15.3) 10
f0;6;9g11 (3.667) 8 (0.1834) 10 (1.196) 10-11 (37.14%) 8 (13.3) 11
Augmentedf0;4;8g13 (5.259) 5 (0.1490) 13 (1.998) 12 (36.67%) 13 (20.3) 13
Correlation r .352 .698 .802 .846 .791
Table 6: Correlations of several consonance rankings with empirical ranking for triads. Only n=10 values
were available for pure tonalness (Parncutt, 1989, p. 140) and the consonance degree according to Foltyn
(2012, Figure 6), because suspended or diminished chords, respectively, are missing in these references.
Thus, we have only n 2=8 degrees of freedom in the calculation of the respective signiﬁcance values. For
some approaches (Helmholtz, 1863; Plomp and Levelt, 1965; Kameoka and Kuriyagawa, 1969; Sethares,
2005), the rankings are taken from Cook (2009, Table 1).
Approach Correlation rSigniﬁcance p
Smoothed relative periodicity (rational tuning #2) .846 .0001
Smoothed logarithmic periodicity (rational tuning #2) .831 .0002
Smoothed logarithmic periodicity (rational tuning #1) .813 .0004
Smoothed relative periodicity (rational tuning #1) .808 .0004
Percentage similarity (Gill and Purves, 2009) .802 .0005
Dual process (Johnson-Laird et al., 2012, Figure 2) .791 .0006
Consonance value (Brefeld, 2005) .755 .0014
Consonance degree (Foltyn, 2012, Figure 6) .826 .0016
Dissonance curve (Sethares, 2005) .723 .0026
Instability (Cook and Fujisawa, 2006, Table A2) .698 .0040
Smoothed gradus suavitatis (Euler, 1739) .690 .0045
Sensory dissonance (Kameoka and Kuriyagawa, 1969) .607 .0139
Tension (Cook and Fujisawa, 2006, Table A2) .599 .0153
Pure tonalness (Parncutt, 1989, p. 140) .675 .0162
Critical bandwidth (Plomp and Levelt, 1965) .570 .0210
Temporal dissonance (Helmholtz, 1863) .503 .0399
Relative prevalence of chord types (Eberlein, 1994, p. 421) .481 .0482
Sonance factor (Hofmann-Engl, 2004, 2008) .434 .0692
Roughness (Hutchinson and Knopo , 1979, Table 1) .352 .1193
23

## Page 24

Table 7: Consonance correlation for the complete list of triads in root position with spacing of chords as
given by Johnson-Laird et al. (2012, Figure 2, n=19). The ordinal rating and the numerical values of the
considered measures are given in parentheses. The correlation and signiﬁcance values written in parenthe-
ses refer to the ordinal rating, while the ones outside parentheses just compare the respective rankings. The
roughness values are taken from Johnson-Laird et al. (2012, Figure 2), who employ the implementation
available at http://www.uni-graz.at/richard.parncutt/computerprograms.html , based on the
research reported in Bigand et al. (1996). In all other cases, rational tuning #2 is used as the underlying
tuning for the respective frequency ratios.
Empirical Smoothed relative Smoothed logarithmic Dual
Chord # Semitones rank Roughness Similarity periodicity periodicity process
1a (major)f0;16;19g1 (1.667) 2 (0.0727) 1 (64.44%) 1 (2.0) 1 (1.000) 1
2af0;19;22g3 (2.481) 1 (0.0400) 5 (52.59%) 8-9 (12.3) 6-7 (3.133) 2
3af0;16;22g4-5 (2.630) 3 (0.0760) 9 (38.62%) 15-16 (19.0) 8 (3.271) 3
4af0;15;22g6 (2.926) 4 (0.0894) 8 (39.26%) 8-9 (12.3) 6-7 (3.133) 4
5a (minor)f0;15;19g2 (2.407) 5 (0.0972) 3-4 (55.56%) 4 (5.0) 4 (2.322) 5
6a (suspended) f0;7;14g7 (3.148) 6 (0.0983) 3-4 (55.56%) 6-7 (11.7) 5 (2.918) 6
7af0;19;23g8 (3.370) 7 (0.1060) 2 (56.67%) 2-3 (4.0) 2-3 (2.000) 7
8af0;16;23g4-5 (2.630) 8 (0.1097) 6 (52.22%) 2-3 (4.0) 2-3 (2.000) 8
9a (diminished)f0;15;18g11 (3.889) 16 (0.2214) 17 (28.57%) 13 (17.0) 14 (3.786) 9
10af0;11;14g13 (3.963) 9 (0.1390) 18 (28.33%) 10-11 (14.3) 12 (3.585) 10
11af0;18;22g15 (5.148) 12 (0.1746) 14 (30.05%) 15-16 (19.0) 11 (3.540) 11
12af0;17;23g12 (3.926) 13 (0.1867) 12 (34.37%) 6-7 (11.7) 10 (3.497) 12
13af0;14;17g9 (3.481) 14 (0.1902) 11 (36.11%) 5 (10.0) 9 (3.308) 13
14af0;15;26g10 (3.630) 17 (0.2485) 13 (33.52%) 12 (15.7) 15 (3.800) 14
15af0;11;18g14 (4.815) 18 (0.2639) 10 (36.90%) 17-18 (25.7) 17 (4.571) 15
16 (augmented)f0;16;20g16 (5.259) 10 (0.1607) 7 (41.67%) 10-11 (14.3) 13 (3.655) 16
17af0;15;23g17-18 (5.593) 11 (0.1727) 16 (28.89%) 17-18 (25.7) 18 (4.655) 17
18af0;20;23g19 (5.630) 15 (0.2164) 15 (29.44%) 14 (17.7) 16 (3.989) 18
19af0;14;25g17-18 (5.593) 19 (0.3042) 19 (19.93%) 19 (101.0) 19 (5.964) 19
Correlation r .761 (.746) .760 (.765) .713 (.548) .867 (.810) .916
Signiﬁcance p .0001 (.0001) .0001 (.0001) .0003 (.0075) .0000 (.0000) .0000
The data sets in Johnson-Laird et al. (2012) suggest further investigations. So Table 7 shows the anal-
ysis of all possible three-tone chords in root position (Johnson-Laird et al., 2012, Figure 2). As one can
see, the correlation between the empirical rating and the predictions of the dual-process theory is very
high ( r=:916). This also holds for smoothed logarithmic periodicity but not that much for smoothed
relative periodicity, in particular, if the correlation between the ordinal rating and the concrete smoothed
periodicity values are taken, which are shown in parentheses in Table 7 ( r=:810 versus r=:548). This
justiﬁes our preference for smoothed logarithmic as opposed to smoothed relative periodicity, because
the former notion is motivated more by neuroacoustical results, namely that the spatial structure of the
periodicity-pitch representation in the brain is organised as a logarithmic periodicity map. Johnson-Laird
et al. (2012, Experiment 2) also provide data for n=48 four-tone chords. A summary analysis is shown
in Table 8, indicating once again high correlation for several measures of harmoniousness, including log-
arithmic periodicity.
4.3 From chords to scales
In contrast to many other approaches, the periodicity-based method with smoothing can easily be applied
to scales and yields meaningful results (Stolzenburg, 2009).
24

## Page 25

Table 8: Correlations of several consonance rankings with ordinal values of empirical rating for n=48
selected four-note chords, spread over more than one octave (Johnson-Laird et al., 2012, Figure 3). For
the
measure (Stolzenburg, 2012), percentage similarity (Gill and Purves, 2009), and gradus suavitatis
(Euler, 1739), once again the frequency ratios from rational tuning #2 are used.
Approach Correlation rSigniﬁcance p
Dual process (Johnson-Laird et al., 2012, Figure 3) .895 .0000
Smoothed 
measure (Stolzenburg, 2012) .824 .0000
Smoothed gradus suavitatis (Euler, 1739) .785 .0000
Smoothed logarithmic periodicity (rational tuning #2) .758 .0000
Smoothed logarithmic periodicity (rational tuning #1) .754 .0000
Percentage similarity (Gill and Purves, 2009) .734 .0000
Smoothed relative periodicity (rational tuning #2) .567 .0000
Smoothed relative periodicity (rational tuning #1) .531 .0001
Roughness (Hutchinson and Knopo , 1978, 1979) .402 .0023
G4444
(a) pentachord					
(b) pentatonics					
(c) diatonic scale							
(d) blues scale		6	 4	 			6	
Figure 8: Harmonies (scales) with more than three tones.
Example 14. Figure 8(a) shows the pentachord Emaj7 =9 (with E4 as the lowest tone), classically built
from a stack of thirds, standard in jazz music. It is the highest ranked harmony with 5 out of 12 tones
(log2(h)4:234 with respect to rational tuning #1, log2(h)3:751 with respect to rational tuning
#2). Although in most cases this pentachord is most likely not heard in a bitonal manner, it may be
alternatively understood as the superposition of the major triads E and B, which are in a tonic-dominant
relationship according to classical harmony theory. As just said, it appears in the front rank of all harmonies
consisting of 5 out of 12 tones, which does not hold for a superposition of a random chord sequence.
Thus, also for chord progressions the periodicity-based method with smoothing yields meaningful results.
Nevertheless, this point has to be investigated further. All harmonies shown in Figure 8 have low, i.e. good
smoothed periodicity values, ranking among the top 5% in their tone multiplicity category with respect to
rational tuning #1. This holds for the pentatonics (5 tones, log2(h)5:302), the diatonic scale (7 tones,
log2(h)6:453), as well as the blues scale (8 tones, log2(h)7:600).
Temperley and Tan (2013) investigated the perceived consonance of diatonic scales. Table 9 lists all
classical church modes, i.e. the diatonic scale and its inversions. The cognitive model of the perception of
diatonic scales introduced by Temperley and Tan (2013) results in a 100% correlation with the empirical
data. Although the correlation for smoothed logarithmic periodicity obviously is not that good, it still
shows high correlation. Nonetheless, the major scale (Ionian, cf. Figure 8(c)) appears in the front rank of
462 possible scales with 7 out of 12 tones with respect to smoothed relative and smoothed logarithmic
periodicity. In addition, in contrast to more cognitive theories on harmony perception, the periodicity-
based method with smoothing introduced in this article does not presuppose any principles of tonal music,
e.g. the existence of diatonic scales or the common use of the major triad. They may be derived from
underlying, more primitive mechanisms, namely periodicity detection in the human (as well as animal)
brain.
Interestingly, with rational tuning #1 as basis, the results for scales (Table 9) are better for smoothed
logarithmic periodicity than with rational tuning #2 ( r=:964 versus r=:786). In the former case, the
25

## Page 26

Table 9: Rankings of common heptatonic scales (church modes), i.e. with 7 out of 12 tones. As empirical
rating, the overall preference for the classical church modes is adopted (Temperley and Tan, 2013, Fig-
ure 10). For the sonance factor (Hofmann-Engl, 2004, 2008), again C4 (middle C) is taken as the lowest
tone. For percentage similarity, the values are taken directly from Gill and Purves (2009, Table 3).
Smoothed Smoothed
Mode Semitones Empirical Sonance Similarity log. periodicity log. periodicity
rank factor (Rational tuning #1) (Rational tuning #2)
Ionianf0;2;4;5;7;9;11g1 (0.83) 4 (0.147) 3 (39.61%) 1 (6.453) 1 (5.701)
Mixolydianf0;2;4;5;7;9;10g2 (0.64) 1.5 (0.162) 6 (38.59%) 3 (6.607) 4 (5.998)
Lydianf0;2;4;6;7;9;11g3 (0.58) 1.5 (0.162) 5 (38.95%) 2 (6.584) 2 (5.830)
Dorianf0;2;3;5;7;9;10g4 (0.40) 3 (0.152) 2 (39.99%) 4 (6.615) 3 (5.863)
Aeolianf0;2;3;5;7;8;10g5 (0.34) 6 (0.138) 4 (39.34%) 5 (6.767) 7 (6.158)
Phrygianf0;1;3;5;7;8;10g6 (0.21) 7 (0.126) 1 (40.39%) 6 (6.778) 5 (6.023)
Locrianf0;1;3;5;6;8;10g7 5 (0.142) 7 (37.68%) 7 (6.790) 6 (6.033)
Correlation r .667 .036 .964 .786
Signiﬁcance p .0510 .4697 .0002 .0181
seven classical church modes even appear in the very front ranks of their tone multiplicity category. The
correlation of percentage similarity is low. But despite this, the diatonic scale and its inversions are among
the 50 heptatonic scales whose intervals conform most closely to a harmonic series out of 4 107examined
possibilities Gill and Purves (2009, Table 3), which is of course a meaningful result.
5 Discussion and conclusions
5.1 Summary
We have seen in this article that harmony perception can be explained well by considering the periodic
structure of harmonic sounds, which can be computed from the frequency ratios of the intervals in the
given harmony. The results presented show the highest correlation with empirical results and thus con-
tribute to the discussion of the consonance /dissonance of musical chords and scales. We conclude that
there is a strong neuroacoustical and psychophysical basis for harmony perception including chords and
scales.
5.2 Limitations of the approach
The periodicity-based method with smoothing, as presented in this article, clearly has limitations. First,
the available empirical studies on harmony perception used in this article (Schwartz et al., 2003; Johnson-
Laird et al., 2012; Temperley and Tan, 2013) in general take the average over all participants’ ratings.
Thus, individual di erences in perception are neglected, e.g. the inﬂuence of culture, familiarity, or mu-
sical training. However, some studies report that especially the number of years of musical training has
a signiﬁcant e ect on harmony perception, although periodicity detection remains an important factor
that is used to a di erent extent by musicians and non-musicians (Hall and Hess, 1984; Lee et al., 2009;
McLachlan et al., 2013).
Second, we do not consider in detail the context of a harmony in a musical piece during the periodicity-
based analyses with smoothing in this article. Therefore, Parncutt and Hair (2011) attempt to explain the
perception of musical harmonies as a holistic phenomenon, covering a broad spectrum, including the
conception of consonance /dissonance as pleasant /unpleasant, and the history in Western music and mu-
sic theory, emphasising that consonance /dissonance should be discussed along several dimensions such
26

## Page 27

as tense /relaxed, familiar /unfamiliar, and tonal /atonal. Nonetheless, periodicity may be used as one con-
stituent in explaining harmony perception, even with respect to the historical development of (Western)
music, by assuming di erent levels of harmonic complexity, changing over time (Parncutt, 1989, pp. 57-
58).
Third, in this article we adopt the equal temperament as a reference system for tunings, which is
the basis of Western music. However, non-Western scales, e.g. in Turkish classical music with Makam
melody types or tone scales of recordings of traditional Central African music (see http://music.
africamuseum.be/ and Moelants et al., 2009), do not seem to be based on equal temperament tunings.
Nevertheless, they can be analysed by the periodicity-based method with smoothing, predicting also rela-
tively good, i.e. low values of consonance for these scales (Stolzenburg, 2010). Lapp (2017) also studied
music from di erent cultures and epoques, including Turkish, Arabic, and Chinese music. He concludes
that for microtonal scales (smoothed logarithmic) periodicity as harmoniousness measure should be re-
stricted to smaller groups of tones, which he calls words , e.g. three consecutive tones. This point clearly
must be further investigated. The approaches by Gill and Purves (2009) and Honingh and Bod (2011) are
also applicable to non-Western music, too.
Relative and logarithmic periodicity of harmonies can be computed without reference to any tun-
ing by approximating frequency ratios within a band of d=1% employing the procedure from
Section 3.2 (see Deﬁnition 15 below). A re-implementation of the Prolog code (cf. Section 4) for
this generalized periodicity measure in GNU Octave (Eaton et al., 2017), which is largely compatible
with the scientiﬁc programming language Matlab (Higham and Higham, 2017), is available (also) at
http://artint.hs-harz.de/fstolzenburg/harmony/ .
Deﬁnition 15. LetH=ff1;:::; fngbe a harmony and Hk=ff1=fk;:::; fn=fkgfor 1kn. Then a
harmoniousness measure Hcan be smoothed for general harmonies, i.e. without reference to a tuning
system or semitone sets (in contrast to Deﬁnition 9), as follows:
eH(H)=1
nnX
k=1H(Hk)
IfHis relative or logarithmic periodicity, then each (real) frequency ratio Fin a harmony class Hkhas
to be made rational, and octave equivalence can be taken into account. For this, let F=2mF1for a
(possibly negative) integer msuch that 1F12, and F2be the rational approximation of F1(according
to Section 3.2) with some given maximal deviation d. Then the integer ratio F3=2mF2(in lowest terms)
shall be used instead of Fin the computation.
5.3 Future work
Future work should concentrate on even more exhaustive empirical experiments on harmony perception,
in order to improve the signiﬁcance of and conﬁdence in the statistical analyses, including more detailed
investigations of chord progressions, possibly employing di erent tunings and timbres, and taking into
account the historical development of Western music and beyond. Last but not least, the working of the
brain with respect to auditory processing still must be better understood (see e.g. Patterson et al., 2002).
In consequence, models of the brain that take temporal properties into account should be investigated, as
claimed also by Roederer (2008). For this, (artiﬁcial) neural networks that have this property (Cariani,
2001; Bahmer and Langner, 2006; Haykin, 2008; Stolzenburg and Ruh, 2009; V outsas et al., 2004) could
be considered further.
27

## Page 28

Acknowledgements
This article is a completely revised and extended version of previous work (Stolzenburg, 2009, 2010,
2012, 2014). I would like to thank Wolfgang Bibel, Peter A. Cariani, Norman D. Cook, Martin Ebeling,
Thomas Fiore, Adrian Foltyn, Sergey Gaponenko, Ludger J. Hofmann-Engl, Phil N. Johnson-Laird, Ger-
ald Langner, Andrew J. Milne, Florian Ruh, Tilla Schade, and Marek ˇZabka, as well as several anonymous
referees for helpful discussions, hints, and comments on this article or earlier versions thereof.
References
Apt, K. R. and Wallace, M. (2007). Constraint Logic Programming Using ECLiPSe . Cambridge Univer-
sity Press, Cambridge, UK.
Bahmer, A. and Langner, G. (2006). Oscillating neurons in the cochlear nucleus: I. Simulation results, II.
Experimental basis of a simulation paradigm. Biological Cybernetics , 95:371–392.
Bailhache, P. (1997). Music translated into mathematics: Leonhard Euler. In Problems of translation in
the 18th century , Nantes, France. Conference of the Center Franc ¸ois Vi `ete. Original in French. English
translation by Joe Monzo. Available from: http://www.tonalsoft.com/monzo/euler/euler-en.
aspx .
Balzano, G. J. (1980). The group-theoretic description of twelvefold and microtonal pitch systems. Com-
puter Music Journal , 4(4):66–84.
Beament, J. (2001). How we hear music: The relationship between music and the hearing mechanism .
The Boydell Press, Woodbridge, UK.
Bidelman, G. M. and Krishnan, A. (2009). Neural correlates of consonance, dissonance, and the hierarchy
of musical pitch in the human brainstem. The Journal of Neuroscience , 29(42):13165–13171.
Bigand, E., Parncutt, R., and Lerdahl, F. (1996). Perception of musical tension in short chord sequences:
The inﬂuence of harmonic function, sensory dissonance, horizontal motion, and musical training. Per-
ception and Psychophysics , 58(1):125–141.
Boomsliter, P. C. and Creel, W. (1961). The long pattern hypothesis in harmony and hearing. Journal of
Music Theory , 5(1):2–31.
Bowling, D. L., Gill, K. Z., Choi, J. D., Prinz, J., and Purves, D. (2010). Major and minor music compared
to excited and subdued speech. Journal of the Acoustical Society of America , 127(1):491–503.
Bowling, D. L. and Purves, D. (2015). A biological rationale for musical consonance. Proceedings of the
National Academy of Sciences , 112(36):11155–11160.
Brefeld, W. (2005). Zweiklang, Konsonanz, Dissonanz, Oktave, Quinte, Quarte und Terz. Online Publi-
cation. Available from: http://www.brefeld.homepage.t-online.de/konsonanz.html .
Cambouropolos, E., Tsougras, C., Mavromatis, P., and Pastiadis, K., editors (2012). Proceedings of 12th
International Conference on Music Perception and Cognition and 8th Triennial Conference of the Eu-
ropean Society for the Cognitive Sciences of Music , Thessaloniki, Greece.
Carey, N. and Clampitt, D. (1989). Aspects of well-formed scales. Music Theory Spectrum , 11(2):187–
206.
28

## Page 29

Cariani, P. A. (1999). Temporal coding of periodicity pitch in the auditory system: An overview. Neural
Plasticity , 6(4):147–172.
Cariani, P. A. (2001). Neural timing nets. Neural Networks , 14(6-7):737–753.
Clocksin, W. F. and Mellish, C. S. (2010). Programming in Prolog: Using the ISO Standard . Springer,
Berlin, Heidelberg, New York, 5th edition.
Cook, N. D. (2009). Harmony perception: Harmoniousness is more than the sum of interval consonance.
Music Perception , 27(1):25–41.
Cook, N. D. (2012). Harmony, Perspective, and Triadic Cognition . Cambridge University Press, Cam-
bridge, New York, Melbourne, Madrid, Cape Town.
Cook, N. D. and Fujisawa, T. X. (2006). The psychophysics of harmony perception: Harmony is a three-
tone phenomenon. Empirical Musicology Review , 1(2):1–21.
Cousineau, M., McDermott, J. H., and Peretz, I. (2012). The basis of musical consonance as revealed by
congenital amusia. Proceedings of the National Academy of Sciences , 109(48):19858–19863.
Dewitt, L. A. and Crowder, R. G. (1987). Tonal fusion of consonant musical intervals: The oomph in
Stumpf. Perception &Psychophysics , 41(1):73–84.
Eaton, J. W., Bateman, D., Hauberg, S., and Wehbring, R. (2017). GNU Octave – A High-Level Interactive
Language for Numerical Computations . Edition 4 for Octave version 4.2.1. Available from: http:
//www.octave.org/ .
Ebeling, M. (2007). Verschmelzung und neuronale Autokorrelation als Grundlage einer Konsonanztheo-
rie. Peter Lang, Frankfurt am Main, Berlin, Bern, Bruxelles, New York, Oxford, Wien.
Ebeling, M. (2008). Neuronal periodicity detection as a basis for the perception of consonance: A mathe-
matical model of tonal fusion. Journal of the Acoustical Society of America , 124(4):2320–2329.
Ebeling, M. (2014). Das Konzept von Konsonanz und Dissonanz vor dem Hintergrund von Erkennt-
nislehre und Neurowissenschaft. In Candoni, J.-F., Pesnel, S., and Schmidt, W. G. A., editors, Klang –
Ton – Musik , Z¨AK-Sonderheft 13. Felix Meiner.
Eberlein, R. (1994). Die Entstehung der tonalen Klangsyntax . Peter Lang, Frankfurt.
Euler, L. (1739). Tentamen novae theoria musicae ex certissimis harmoniae principiis dilucide expositae.
English translation by Charles S. Smith in June 1960.
Fokker, A. D. (1969). Unison vectors and periodicity blocks in the three-dimensional (3-5-7-)harmonic
lattice of notes. In Proceedings of Koninklijke Nederlandsche Akademie van Wetenschappen , pages
153–168, Amsterdam, Netherlands.
Foltyn, A. (2012). Neuroscientiﬁc measure of consonance. In Cambouropolos et al. (2012), pages 310–
316.
Foriˇsek, M. (2007). Approximating rational numbers by fractions. In Crescenzi, P., Prencipe, G., and
Pucci, G., editors, Fun with Algorithms – Proceedings of 4th International Conference , LNCS 4475,
pages 156–165, Castiglioncello, Italy. Springer.
Gill, K. Z. and Purves, D. (2009). A biological rationale for musical scales. PLoS ONE , 4(12):e8144.
29

## Page 30

Graham, R. L., Knuth, D. E., and Patashnik, O. (1994). Concrete Mathematics . Addison-Wesley, Reading,
MA, 2nd edition.
Hall, D. E. and Hess, J. T. (1984). Perception of musical interval tuning. Music Perception , 2(2):166–195.
Hardy, G. H. and Wright, E. M. (1979). An Introduction to the Theory of Numbers . Clarendon Press,
Oxford, England, 5th edition.
Hartmann, W. M. (1997). Signals, Sound, and Sensation . American Institute of Physics, Woodbury, NY .
Haykin, S. (2008). Neural Networks and Learning Machines . Prentice Hall, 3rd edition.
Helmholtz, H. L. F. v. (1863). Die Lehre von den Tonempﬁndungen als physiologische Grundlage f¨ ur die
Theorie der Musik . F. Vieweg, Braunschweig.
Higham, D. J. and Higham, N. J. (2017). MatLab Guide . Siam, Philadelphia, PA, 3rd edition. Available
from: http://bookstore.siam.org/ot150/ .
Hirata, K., Tzanetakis, G., and Yoshii, K., editors (2009). Proceedings of 10th International Society for
Music Information Retrieval Conference , Kobe, Japan.
Hofmann-Engl, L. J. (2004). Virtual pitch and its application to contemporary harmonic analysis.
Chameleon Group Online Publication. Available from: http://www.chameleongroup.org.uk/
research/virtual_analysis.html .
Hofmann-Engl, L. J. (2008). Virtual pitch and the classiﬁcation of chords in minor and major keys. In
Miyazaki, K., Hiraga, Y ., Adachi, M., Nakajima, Y ., and Tsuzaki, M., editors, Proceedings of 10th
International Conference on Music Perception and Cognition , Sapporo, Japan.
Honingh, A. and Bod, R. (2005). Convexity and the well-formedness of musical objects. Journal of New
Music Research , 34(3):293–303.
Honingh, A. and Bod, R. (2011). In search of universal properties of musical scales. Journal of New
Music Research , 40(1):81–89.
Hutchinson, W. and Knopo , L. (1978). The acoustic component of western consonance. Inter-
face/Journal of New Music Research , 7(1):1–29.
Hutchinson, W. and Knopo , L. (1979). The signiﬁcance of the acoustic component of consonance in
Western triad. Journal of Musicological Research , 3(1-2):5–22.
Johnson-Laird, P. N., Kang, O. E., and Leong, Y . C. (2012). On musical dissonance. Music Perception ,
30(1):19–35.
Kameoka, A. and Kuriyagawa, M. (1969). Consonance theory: I. Consonance of dyads, II. Consonance of
complex tones and its calculation method. Journal of the Acoustical Society of America , 45(6):1451–
1469.
Kopiez, R. (2003). Intonation of harmonic intervals: Adaptability of expert musicians to equal tempera-
ment and just intonation. Music Perception , 20(4):383–410.
Krueger, F. (1904). Di erenzt ¨one und Konsonanz. Zeitschrift f¨ ur Psychologie und Physiologie der Sin-
nesorgane , 36:205–275. Archiv f ¨ur die gesamte Psychologie.
30

## Page 31

Krumhansl, C. L. (1990). Cognitive Foundations of Musical Pitch , volume 17 of Oxford Psychology
Series . Oxford University Press, New York.
Langner, G. (1983). Evidence for neuronal periodicity detection in the auditory system of the Guinea
fowl: Implications for pitch analysis in the time domain. Experimental Brain Research , 52(3):333–355.
Langner, G. (1997). Temporal processing of pitch in the auditory system. Journal of New Music Research ,
26(2):116–132.
Langner, G. (2015). The Neural Code of Pitch and Harmony . Cambridge University Press, Cambridge,
UK.
Langner, G., Sams, M., Heil, P., and Schulze, H. (1997). Frequency and periodicity are represented in
orthogonal maps in the human auditory cortex: evidence from magnetoencephalography. Journal of
Comparative Physiology A , 181:665–676.
Langner, G. and Schreiner, C. E. (1988). Periodicity coding in the inferior colliculus of the cat: I. Neuronal
mechanisms, II. Topographical organization. Journal of Neurophysiology , 60(6):1799–1840.
Lapp, S. (2017). Modeling intonation in non-Western musical cultures. Bachelor thesis, Pennsylvania
State University, Department of Engineering Science and Mechanics and School of Music.
Lee, K. M., Skoe, E., Kraus, N., and Ashley, R. (2009). Selective subcortical enhancement of musical
intervals in musicians. The Journal of Neuroscience , 29(18):5832–5840.
Lee, K. M., Skoe, E., Kraus, N., and Ashley, R. (2015). Neural transformation of dissonant intervals in
the auditory brainstem. Music Perception , 32(5):445–459.
Licklider, J. C. R. (1951). A duplex theory of pitch perception. Experientia , 7(4):127–134.
Licklider, J. C. R. (1962). Periodicity pitch and related auditory process models. International Journal of
Audiology , 1(1):11–36.
Malmberg, C. F. (1918). The perception of consonance and dissonance. Psychological Monographs ,
25(2):93–133.
McLachlan, N., Marco, D., Light, M., and Wilson, S. (2013). Consonance and pitch. Journal of Experi-
mental Psychology: General .
Meddis, R. and Hewitt, M. J. (1991). Virtual pitch and phase sensivity of a computer model of the auditory
periphery: I. Pitch identiﬁcation, II. Phase sensivity. Journal of the Acoustical Society of America ,
89(6):2866–2894.
Moelants, D., Cornelis, O., and Leman, M. (2009). Exploring African tone scales. In Hirata et al. (2009),
pages 489–494.
Moore, B. C., Peters, R. W., and Glasberg, B. R. (1985). Thresholds for the detection of inharmonicity in
complex tones. Journal of the Acoustical Society of America , 77(5):1861–1867.
Moore, B. C., Peters, R. W., and Glasberg, B. R. (1986). Thresholds for hearing mistuned partials as
separate tones in harmonic complexes. Journal of the Acoustical Society of America , 80(2):479–483.
Parncutt, R. (1989). Harmony: A Psychoacoustical Approach . Springer, Berlin, Heidelberg, New York.
31

## Page 32

Parncutt, R. and Hair, G. (2011). Consonance and dissonance in music theory and psychology: Disentan-
gling dissonant dichotomies. Journal of Interdisciplinary Music Studies , 5(2):119–166.
Patterson, R. D., Uppenkamp, S., Johnsrude, I. S., and Gri ths, T. D. (2002). The processing of temporal
pitch and melody information in auditory cortex. Neuron , 36(4):767–776.
Plomp, R. (1967). Beats of mistuned consonances. Journal of the Acoustical Society of America ,
42(2):462–474.
Plomp, R. and Levelt, W. J. M. (1965). Tonal consonance and critical bandwidth. Journal of the Acoustical
Society of America , 38(4):548–560.
Roberts, L. A. (1986). Consonant judgments of musical chords by musicians and untrained listeners.
Acustica , 62:163–171.
Roederer, J. G. (2008). The Physics and Psychophysics of Music: An Introduction . Springer, Berlin,
Heidelberg, New York, 4th edition.
Schouten, J. F. (1938). The perception of subjective tones. In Proceedings of Koninklijke Nederlandsche
Akademie van Wetenschappen 41 /10, pages 1086–1093, Amsterdam, Netherlands.
Schouten, J. F. (1940). The residue, a new component in subjective sound analysis. In Proceedings of
Koninklijke Nederlandsche Akademie van Wetenschappen 43 /3, pages 356–365, Amsterdam, Nether-
lands.
Schulze, H. and Langner, G. (1997). Periodicity coding in the primary auditory cortex of the mongo-
lian gerbil (merionesunguiculatus): two di erent coding strategies for pitch and rhythm? Journal of
Comparative Physiology A , 181:651–663.
Schwartz, D. A., Howe, C. Q., and Purves, D. (2003). The statistical structure of human speech sounds
predicts musical universals. The Journal of Neuroscience , 23(18):7160–7168.
Sethares, W. A. (2005). Tuning, Timbre, Spectrum, Scale . Springer, London, 2nd edition.
Stolzenburg, F. (2009). A periodicity-based theory for harmony perception and scales. In Hirata et al.
(2009), pages 87–92. Available from: http://ismir2009.ismir.net/proceedings/PS1-6.pdf .
Stolzenburg, F. (2010). A periodicity-based approach on harmony perception including non-western
scales. In Demorest, S. M., Morrison, S. J., and Campbell, P. S., editors, Proceedings of 11th Inter-
national Conference on Music Perception and Cognition , pages 683–687, Seattle, Washington, USA.
Available from: http://artint.hs-harz.de/fstolzenburg/papers/Sto10d.pdf .
Stolzenburg, F. (2012). Harmony perception by periodicity and granularity detection. In Cambouropolos
et al. (2012), pages 958–959. Available from: http://icmpc-escom2012.web.auth.gr/sites/
default/files/papers/958_Proc.pdf .
Stolzenburg, F. (2013). Harmony perception by periodicity detection. CoRR – Computing Research
Repository abs /1306.6458, Cornell University Library. Extended, revised, and corrected version 2018.
Available from: http://arxiv.org/abs/1306.6458 .
Stolzenburg, F. (2014). Harmony perception by periodicity detection. In Song, M. K., editor, Proceedings
of the ICMPC-APSCOM 2014 Joint Conference: 13th International Conference on Music Perception
and Cognition and 5th Conference of the Asian-Paciﬁc Society for the Cognitive Sciences of Music ,
pages 27–31, Seoul, South Korea. College of Music, Yonsei University. Available from: http://
artint.hs-harz.de/fstolzenburg/papers/Sto14.pdf .
32

## Page 33

Stolzenburg, F. and Ruh, F. (2009). Neural networks and continuous time. In Schmid, U., Ragni, M., and
Knau , M., editors, Proceedings of KI 2009 Workshop Complex Cognition , pages 25–36, Paderborn.
Extended version available at CoRR – Computing Research Repository arxiv.org /abs/1606.04466, Cor-
nell University Library, 2016. Available from: http://arxiv.org/abs/1606.04466 .
Stumpf, C. (1883). Tonpsychologie , volume 1. S. Hirzel, Leipzig.
Stumpf, C. (1890). Tonpsychologie , volume 2. S. Hirzel, Leipzig.
Stumpf, C. (1898). Neueres ¨uber Tonverschmelzung. Beitr¨ age zur Akustik und Musikwissenschaft , 2:1–
24. Available from: http://vlp.uni-regensburg.de/library/data/lit38512 .
Temperley, D. and Tan, D. (2013). Emotional connotations of diatonic modes. Music Perception ,
30(3):237–257.
Terhardt, E., Stoll, G., and Seewann, M. (1982). Algorithm for extraction of pitch and pitch salience from
complex tonal signals. Journal of the Acoustical Society of America , 71(3):679–688.
Tramo, M. J., Cariani, P. A., Delgutte, B., and Braida, L. D. (2001). Neurobiological foundations for the
theory of harmony in western tonal music. Annals of the New York Academy of Sciences , 930:92–116.
V os, J. (1986). Purity ratings of tempered ﬁfths and major thirds. Music Perception , 3(3):221–258.
V outsas, K., Langner, G., Adamy, J., and Ochsen, M. (2004). A brain-like neural network for periodicity
analysis. IEEE Transactions on Systems, Man, and Cybernetics, Part B: Cybernetics , 35(1):12–22.
Zwicker, E. and Fastl, H. (1999). Psychoacoustics: Facts and Models . Springer, Heidelberg, New York,
2nd edition.
Zwicker, E., Flottorp, G., and Stevens, S. S. (1957). Critical band width in loudness summation. Journal
of the Acoustical Society of America , 29(5):548–557.
33

