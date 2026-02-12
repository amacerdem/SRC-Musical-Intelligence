# 

**Author:**   
**Subject:**   
**Total Pages:** 29  
**Source File:** `a (12).pdf`

---

## Page 1

Simultaneous Consonance in Music Perception and Composition
Peter M. C. Harrison
Queen Mary University of LondonMarcus T. Pearce
Queen Mary University of London and Aarhus University
Simultaneous consonance is a salient perceptual phenomenon corresponding to the perceived pleasant-
ness of simultaneously sounding musical tones. Various competing theories of consonance have beenproposed over the centuries, but recently a consensus has developed that simultaneous consonance isprimarily driven by harmonicity perception. Here we question this view, substantiating our argument bycritically reviewing historic consonance research from a broad variety of disciplines, reanalyzingconsonance perception data from 4 previous behavioral studies representing more than 500 participants,and modeling three Western musical corpora representing more than 100,000 compositions. We concludethat simultaneous consonance is a composite phenomenon that derives in large part from three phenom-ena: interference, periodicity/harmonicity, and cultural familiarity. We formalize this conclusion with acomputational model that predicts a musical chord’s simultaneous consonance from these three features,and release this model in an open-source R package, incon , alongside 15 other computational models also
evaluated in this paper. We hope that this package will facilitate further psychological and musicologicalresearch into simultaneous consonance.
Keywords: composition, consonance, dissonance, music, perception
Simultaneous consonance is a salient perceptual phenomenon
that arises from simultaneously sounding musical tones. Conso-nant tone combinations tend to be perceived as pleasant, stable,and positively valenced; dissonant combinations tend converselyto be perceived as unpleasant, unstable, and negatively valenced.The opposition between consonance and dissonance underlies
much of Western music (e.g., Dahlhaus, 1990 ;Hindemith, 1945 ;
Parncutt & Hair, 2011 ;Rameau, 1722 ;Schoenberg, 1978 ).
1
Many psychological explanations for simultaneous consonance
have been proposed over the centuries, including amplitude fluc-tuation ( Vassilakis, 2001 ), masking of neighboring partials ( Hu-
ron, 2001 ), cultural familiarity ( Johnson-Laird, Kang, & Leong,
2012 ), vocal similarity ( Bowling, Purves, & Gill, 2018 ), fusion of
chord tones ( Stumpf, 1890 ), combination tones ( Hindemith, 1945 ),
and spectral evenness ( Cook, 2009 ). Recently, however, a consen-
sus is developing that consonance primarily derives from a chord’sharmonicity ( Bidelman & Krishnan, 2009 ;Bowling & Purves,
2015 ;Cousineau, McDermott, & Peretz, 2012 ;Lots & Stone,
2008 ;McDermott, Lehr, & Oxenham, 2010 ;Stolzenburg, 2015 ),
with this effect potentially being moderated by musical exposure(McDermott et al., 2010 ;McDermott, Schultz, Undurraga, &
Godoy, 2016 ).
Here we question whether harmonicity is truly sufficient to
explain simultaneous consonance perception. First, we criticallyreview historic consonance research from a broad variety of dis-ciplines, including psychoacoustics, cognitive psychology, animalbehavior, computational musicology, and ethnomusicology. Sec-ond, we reanalyze consonance perception data from four previousstudies representing more than 500 participants ( Bowling et al.,
2018 ;Johnson-Laird et al., 2012 ;Lahdelma & Eerola, 2016 ;
Schwartz, Howe, & Purves, 2003 ). Third, we model chord prev-
alences in three large musical corpora representing more than100,000 compositions ( Broze & Shanahan, 2013 ;Burgoyne, 2011 ;
1By “Western music” we refer broadly to the musical traditions of
Europe and music derived from these traditions; by “Western listeners” werefer to listeners from these musical traditions.This article was published Online First December 23, 2019.
X
Peter M. C. Harrison, School of Electronic Engineering and Com-
puter Science, Queen Mary University of London; Marcus T. Pearce,School of Electronic Engineering and Computer Science, Queen MaryUniversity of London, and Center for Music in the Brain, Aarhus Univer-sity.
This paper was first posted as a preprint at https://doi.org/10.31234/osf
.io/6jsug . An early version was presented at the 2019 Society for Educa-
tion, Music and Psychology Research Graduate Conference. The authorsare very grateful to Daniel Bowling for contributing helpful advice and forsharing research materials. They would also like to thank Manuel Anglada-Tort, Emmanouil Benetos, and Matthew Purver for useful feedback andadvice regarding this project. Peter M. C. Harrison is supported by adoctoral studentship from the Engineering and Physical Sciences ResearchCouncil and Arts and Humanities Research Council Centre for DoctoralTraining in Media and Arts Technology (EP/L01632X/1).
This article has been published under the terms of the Creative Com-
mons Attribution License ( http://creativecommons.org/licenses/by/3.0/ ),
which permits unrestricted use, distribution, and reproduction in any me-dium, provided the original author and source are credited. Copyright forthis article is retained by the author(s). Author(s) grant(s) the AmericanPsychological Association the exclusive right to publish the article andidentify itself as the original publisher.
Correspondence concerning this article should be addressed to Peter M. C.
Harrison, School of Electronic Engineering and Computer Science, QueenMary University of London, Mile End Road, Bethnal Green, London E1 4NS,United Kingdom. E-mail: p.m.c.harrison@qmul.ac.ukPsychological Review
© 2019 The Author(s) 2020, Vol. 127, No. 2, 216–244
ISSN: 0033-295X http://dx.doi.org/10.1037/rev0000169
216

## Page 2

Viro, 2011 ). On the basis of these analyses, we estimate the degree
to which different psychological mechanisms contribute to conso-nance perception in Western listeners.
Computational modeling is a critical part of our approach. We
review the state of the art in consonance modeling, empiricallyevaluate 20 of these models, and use these models to test compet-ing theories of consonance. Our work results in two new conso-nance models: a corpus-based cultural familiarity model, and acomposite model of consonance perception that captures interfer-ence between partials, harmonicity, and cultural familiarity. Werelease these new models in an accompanying R package, incon ,
alongside new implementations of 14 other models from the lit-erature (see Software for details). In doing so, we hope to facilitate
future consonance research in both psychology and empiricalmusicology.
Musical Terminology
Western music is traditionally notated as collections of atomic
musical elements termed notes , which are organized along two
dimensions: pitch andtime. In performance, these notes are trans-
lated into physical sounds termed tones , whose pitch and timing
reflect the specifications in the musical score. Pitch is the psycho-logical correlate of a waveform’s oscillation frequency, with slowoscillations sounding “low” and fast oscillations sounding “high.”
Western listeners are particularly sensitive to pitch intervals , the
perceptual correlate of frequency ratios. Correspondingly, a keyprinciple in Western music is transposition invariance , the idea
that a musical object (e.g., a melody) retains its perceptual identitywhen its pitches are all shifted ( transposed ) by the same interval.
A particularly important interval is the octave , which approxi-
mates a 2:1 frequency ratio.
2Western listeners perceive a funda-
mental equivalence between pitches separated by octaves. Corre-spondingly, a pitch class is defined as an equivalence class of
pitches under octave transposition. The pitch-class interval be-
tween two pitch classes is then defined as the smallest possibleascending interval between two pitches belonging to the respectivepitch classes.
In Western music theory, a chord may be defined as a collection
of notes that are sounded simultaneously as tones. The lowest ofthese notes is termed the bass note . Chords may be termed based
on their size: For example, the terms dyad ,triad , and tetrad denote
chords comprising two, three, and four notes respectively. Chordsmay also be termed according to the representations of theirconstituent notes: (a) Pitch sets represent notes as absolute pitches;
(b)Pitch-class sets represent notes as pitch classes; and (c) Chord
types represent notes as intervals from the bass note.
This paper is about the simultaneous consonance of musical
chords. A collection of notes is said to be consonant if the notes
“sound well together,” and conversely dissonant if the notes
“sound poorly together.” In its broadest definitions, consonance isassociated with many different musical concepts, including dia-tonicism, centricism, stability, tension, similarity, and distance(Parncutt & Hair, 2011 ). For psychological studies, however, it is
often useful to provide a stricter operationalization of consonance,and so researchers commonly define consonance to their partici-pants as the pleasantness ,beauty ,o rattractiveness of a chord (e.g.,
Bowling & Purves, 2015 ;Bowling et al., 2018 ;Cousineau et al.,
2012 ;McDermott et al., 2010 ,2016 ).In this paper we use the term “simultaneous” to restrict consid-
eration to the notes within the chord, as opposed to sequentialrelationships between the chord and its musical context. Simulta-neous and sequential consonance are sometimes termed vertical
andhorizontal consonance respectively, by analogy with the phys-
ical layout of the Western musical score ( Parncutt & Hair, 2011 ).
These kinds of chordal consonance may also be distinguished from“melodic” consonance, which refers to the intervals of a melody.For the remainder of this paper, the term “consonance” will betaken to imply “simultaneous consonance” unless specified other-wise.
Consonance and dissonance are often treated as two ends of a
continuous scale, but some researchers treat the two as distinctphenomena (e.g., Parncutt & Hair, 2011 ). Under such formula-
tions, consonance is typically treated as the perceptual correlate ofharmonicity, and dissonance as the perceptual correlate of rough-ness (see Consonance Theories ). Here we avoid this approach, and
instead treat consonance and dissonance as antonyms.
Consonance Theories
Here we review current theories of consonance perception. We
pay particular attention to three classes of theories—periodicity/harmonicity, interference between partials, and culture—that weconsider to be particularly well-supported by the empirical litera-ture. We also discuss several related theories, including vocalsimilarity, fusion, and combination tones.
Periodicity/Harmonicity
Human vocalizations are characterized by repetitive structure
termed periodicity . This periodicity has several perceptual corre-
lates, of which the most prominent is pitch . Broadly speaking,
pitch corresponds to the waveform’s repetition rate, or fundamen-
tal frequency : Faster repetition corresponds to higher pitch.
Sound can be represented either in the time domain or in the
frequency domain. In the time domain, periodicity manifests asrepetitive waveform structure. In the frequency domain, periodic-ity manifests as harmonicity , a phenomenon where the sound’s
frequency components are all integer multiples of the fundamentalfrequency.
3These integer-multiple frequencies are termed har-
monics ; a sound comprising a full set of integer multiples is termed
aharmonic series . Each periodic sound constitutes a (possibly
incomplete) harmonic series rooted on its fundamental frequency;conversely, every harmonic series (incomplete or complete) isperiodic in its fundamental frequency. Harmonicity and periodicityare therefore essentially equivalent phenomena, and we will denoteboth by writing “periodicity/harmonicity.”
Humans rely on periodicity/harmonicity analysis to understand
the natural environment and to communicate with others (e.g.,Oxenham, 2018 ), but the precise mechanisms of this analysis
remain unclear. The primary extant theories are time-domain au-
tocorrelation theories and frequency-domain pattern-matching
theories ( de Cheveigné, 2005 ). Autocorrelation theories state that
2Note that in practice, however, the octave is often stretched slightly
beyond a 2:1 ratio (e.g. Rakowski, 1990 ).
3In particular, the fundamental frequency is equal to the greatest com-
mon divisor of the frequency components.217 SIMULTANEOUS CONSONANCE

## Page 3

listeners detect periodicity by computing the signal’s correlation
with a delayed version of itself as a function of delay time; peaksin the autocorrelation function correspond to potential fundamentalfrequencies ( Balaguer-Ballester, Denham, & Meddis, 2008 ;Bern-
stein & Oxenham, 2005 ;Cariani, 1999 ;Cariani & Delgutte, 1996 ;
de Cheveigné, 1998 ;Ebeling, 2008 ;Langner, 1997 ;Licklider,
1951 ;Meddis & Hewitt, 1991a ,1991b ;Meddis & O’Mard, 1997 ;
Slaney & Lyon, 1990 ;Wightman, 1973 ). Pattern-matching theo-
ries instead state that listeners infer fundamental frequencies bydetecting harmonic patterns in the frequency domain ( Bilsen, 1977 ;
Cohen, Grossberg, & Wyse, 1995 ;Duifhuis, Willems, & Sluyter,
1982 ;Goldstein, 1973 ;Shamma & Klein, 2000 ;Terhardt, 1974 ;
Terhardt, Stoll, & Seewann, 1982b ). Both of these explanations
have resisted definitive falsification, and it is possible that bothmechanisms contribute to periodicity/harmonicity detection ( de
Cheveigné, 2005 ).
The prototypically consonant intervals of Western music tend to
exhibit high periodicity/harmonicity. For example, octaves aretypically performed as complex tones that approximate 2:1 fre-quency ratios, where every cycle of the lower-frequency waveformapproximately coincides with a cycle of the higher-frequencywaveform. The combined waveform therefore repeats approxi-mately with a fundamental frequency equal to that of the lowesttone, which is as high a fundamental frequency as we could expectwhen combining two complex tones; we can therefore say that theoctave has maximal periodicity. In contrast, the dissonant tritonecannot be easily approximated by a simple frequency ratio, and soits fundamental frequency (approximate or otherwise) must bemuch lower than that of the lowest tone. We therefore say that thetritone has relatively low periodicity.
It has correspondingly been proposed that periodicity/harmonic-
ity determines consonance perception ( Bidelman & Heinz, 2011 ;
Boomsliter & Creel, 1961 ;Bowling & Purves, 2015 ;Bowling et
al., 2018 ;Cousineau et al., 2012 ;Ebeling, 2008 ;Heffernan &
Longtin, 2009 ;Lee, Skoe, Kraus, & Ashley, 2015 ;Lots & Stone,
2008 ;McDermott et al., 2010 ;Milne et al., 2016 ;Nordmark &
Fahlén, 1988 ;Patterson, 1986 ;Spagnolo, Ushakov, & Dubkov,
2013 ;Stolzenburg, 2015 ;Terhardt, 1974 ;Ushakov, Dubkov, &
Spagnolo, 2010 ).
4The nature of this potential relationship depends
in large part on the unresolved issue of whether listeners detectperiodicity/harmonicity using autocorrelation or pattern-matching(de Cheveigné, 2005 ), as well as other subtleties of auditory
processing such as masking ( Parncutt, 1989 ;Parncutt & Stras-
burger, 1994 ), octave invariance ( Harrison & Pearce, 2018 ;Milne
et al., 2016 ;Parncutt, 1988 ;Parncutt, Reisinger, Fuchs, & Kaiser,
2018 ), and nonlinear signal transformation ( Lee et al., 2015 ;Stol-
zenburg, 2017 ). It is also unclear precisely how consonance de-
velops from the results of periodicity/harmonicity detection; com-peting theories suggest that consonance is determined by theinferred fundamental frequency ( Boomsliter & Creel, 1961 ;Stol-
zenburg, 2015 ), the absolute degree of harmonic template fit at the
fundamental frequency ( Bowling et al., 2018 ;Gill & Purves, 2009 ;
Milne et al., 2016 ;Parncutt, 1989 ;Parncutt & Strasburger, 1994 ),
the degree of template fit at the fundamental frequency relative tothat at other candidate fundamental frequencies ( Parncutt, 1988 ;
Parncutt et al., 2018 ), or the degree of template fit as aggregated
over all candidate fundamental frequencies ( Harrison & Pearce,
2018 ). This variety of hypotheses is reflected in a diversity of
computational models of musical periodicity/harmonicity percep-tion ( Ebeling, 2008 ;Gill & Purves, 2009 ;Harrison & Pearce,
2018 ;Lartillot, Toiviainen, & Eerola, 2008 ;Milne et al., 2016 ;
Parncutt, 1988 ,1989 ;Parncutt & Strasburger, 1994 ;Spagnolo et
al., 2013 ;Stolzenburg, 2015 ). So far these models have only
received limited empirical comparison (e.g., Stolzenburg, 2015 ).
It is clear why periodicity/harmonicity should be salient to
human listeners: Periodicity/harmonicity detection is crucial forauditory scene analysis and for natural speech understanding (e.g.,Oxenham, 2018 ). It is less clear why periodicity/harmonicity
should be positively valenced, and hence associated with conso-nance. One possibility is that long-term exposure to vocal sounds(Schwartz et al., 2003 ) or Western music ( McDermott et al., 2016 )
induces familiarity with periodicity/harmonicity, in turn engender-ing liking through the mere exposure effect ( Zajonc, 2001 ). A
second possibility is that the ecological importance of interpretinghuman vocalizations creates a selective pressure to perceive thesevocalizations as attractive ( Bowling et al., 2018 ).
Interference Between Partials
Musical chords can typically be modeled as complex tones ,
superpositions of finite numbers of sinusoidal pure tones termed
partials . Each partial is characterized by a frequency and an
amplitude. It is argued that neighboring partials can interact toproduce interference effects, with these interference effects sub-
sequently being perceived as dissonance ( Dillon, 2013 ;Helmholtz,
1863 ;Hutchinson & Knopoff, 1978 ;Kameoka & Kuriyagawa,
1969a ,1969b ;Mashinter, 2006 ;Plomp & Levelt, 1965 ;Sethares,
1993 ;Vassilakis, 2001 ).
Pure-tone interference has two potential sources: beating and
masking . Beating develops from the following mathematical iden-
tity for the addition of two equal-amplitude sinusoids:
cos(2/H9266f
1t)/H11001cos(2/H9266f2t)/H110052cos(2/H9266f/H6126t) cos(/H9266/H9254t) (1)
where f1,f2are the frequencies of the original sinusoids ( f1/H11022f2),
f/H6126/H11005/H20849f1/H11001f2/H20850⁄2,/H9254/H11005 f1/H11002f2, and tdenotes time. For sufficiently
large frequency differences, listeners perceive the left hand side of
Equation 1 , corresponding to two separate pure tones at frequen-
cies f1,f2. For sufficiently small frequency differences, listeners
perceive the right hand side of Equation 1 , corresponding to a tone
of intermediate frequency f/H6126/H11005/H20849f1/H11001f2/H20850⁄2 modulated by a sinusoid
of frequency /H9254⁄2/H11005/H20849f1/H11002f2/H20850⁄2. This modulation is perceived as
amplitude fluctuation with frequency equal to the modulatingsinusoid’s zero-crossing rate, f
1/H11002f2. Slow amplitude fluctua -
tion (c. 0.1–5 Hz) is perceived as a not unpleasant oscillation inloudness, but fast amplitude fluctuation (c. 20–30 Hz) takes ona harsh quality described as roughness . This roughness is
thought to contribute to dissonance perception.
Masking describes situations where one sound obstructs the
perception of another sound (e.g., Patterson & Green, 2012 ;Scharf,
1971 ). Masking in general is a complex phenomenon, but the
mutual masking of pairs of pure tones can be approximated bystraightforward mathematical models ( Parncutt, 1989 ;Parncutt &
Strasburger, 1994 ;Terhardt, Stoll, & Seewann, 1982a ;Wang,
4Periodicity theories of consonance predating the 20th century can be
found in the work of Galileo Galilei, Gottfried Wilhelm Liebniz, LeonhardEuler, Theodor Lipps, and A. J. Polak ( Plomp & Levelt, 1965 ).218 HARRISON AND PEARCE

## Page 4

Shen, Guo, Tang, & Hamade, 2013 ). These models embody long-
established principles that masking increases with smaller fre-quency differences and with higher sound pressure level.
Beating and masking are both closely linked with the notion of
critical bands . The notion of critical bands comes from modeling
the cochlea as a series of overlapping bandpass filters , areas that
are preferentially excited by spectral components within a certainfrequency range ( Zwicker, Flottorp, & Stevens, 1957 ). Beating
typically only arises from spectral components localized to thesame critical band ( Daniel & Weber, 1997 ). The mutual masking
of pure tones approximates a linear function of the number ofcritical bands separating them (termed critical-band distance ),
with additional masking occurring from pure tones within the samecritical band that are unresolved by the auditory system ( Terhardt
et al., 1982a ).
Beating and masking effects are both considerably stronger
when two tones are presented diotically (to the same ear) ratherthan dichotically (to different ears; Buus, 1997 ;Grose, Buss, &
Hall, 2012 ). This indicates that these phenomena depend, in large
part, on physical interactions in the inner ear.
There is a long tradition of research relating beating to conso-
nance, mostly founded on the work of Helmholtz (1863 ;Aures,
1985a , cited in Daniel & Weber, 1997 ;Hutchinson & Knopoff,
1978 ;Kameoka & Kuriyagawa, 1969a ,1969b ;Mashinter, 2006 ;
Parncutt et al., 2018 ;Plomp & Levelt, 1965 ;Sethares, 1993 ;
Vassilakis, 2001 ).
5The general principle shared by this work is
that consonance develops from the accumulation of roughnessderiving from the beating of neighboring partials.
In contrast, the literature linking masking to consonance is
relatively sparse. Huron (2001 ,2002 ) suggests that masking in-
duces dissonance because it reflects a compromised sensitivity tothe auditory environment, with analogies in visual processing suchas occlusion or glare. Aures (1984 ; cited in Parncutt, 1989 ) and
Parncutt (1989 ;Parncutt & Strasburger, 1994 ) also state that
consonance reduces as a function of masking. Unfortunately, theseideas have yet to receive much empirical validation; a difficulty isthat beating and masking tend to happen in similar situations,making them difficult to disambiguate ( Huron, 2001 ).
The kind of beating that elicits dissonance is achieved by small,
but not too small, frequency differences between partials. Withvery small frequency differences, the beating becomes too slow toelicit dissonance ( Hutchinson & Knopoff, 1978 ;Kameoka & Kuri-
yagawa, 1969a ;Plomp & Levelt, 1965 ). The kind of masking that
elicits dissonance is presumably also maximized by small, but nottoo small, frequency differences between partials. For moderatelysmall frequency differences, the auditory system tries to resolvetwo partials, but finds it difficult on account of mutual masking,with this difficulty eliciting negative valence ( Huron, 2001 ,2002 ).
For very small frequency differences, the auditory system onlyperceives one partial, which becomes purer as the two acousticpartials converge on the same frequency.
Musical sonorities can often be treated as combinations of
harmonic complex tones , complex tones whose spectral frequen-
cies follow a harmonic series. The interference experienced by acombination of harmonic complex tones depends on the funda-mental frequencies of the complex tones. A particularly importantfactor is the ratio of these fundamental frequencies. Certain ratios,in particular the simple-integer ratios approximated by prototypi-cally consonant musical chords, tend to produce partials that eithercompletely coincide or are widely spaced, hence minimizing in-
terference.
Interference between partials also depends on pitch height. A
given frequency ratio occupies less critical-band distance as abso-lute frequency decreases, typically resulting in increased interfer-ence. This mechanism potentially explains why the same musicalinterval (e.g., the major third, 5:4) can sound consonant in highregisters and dissonant in low registers.
It is currently unusual to distinguish beating and masking the-
ories of consonance, as we have done above. Most previous worksolely discusses beating and its psychological correlate, roughness(e.g., Cousineau et al., 2012 ;McDermott et al., 2010 ,2016 ;
Parncutt & Hair, 2011 ;Parncutt et al., 2018 ;Terhardt, 1984 ).
However, we contend that the existing evidence does little todifferentiate beating and masking theories, and that it would bepremature to discard the latter in favor of the former. Moreover,we show later in this paper that computational models that addressbeating explicitly (e.g., Wang et al., 2013 ) seem to predict conso-
nance worse than generic models of interference between partials(e.g., Hutchinson & Knopoff, 1978 ;Sethares, 1993 ;Vassilakis,
2001 ). For now, therefore, it seems wise to contemplate both
beating and masking as potential contributors to consonance.
Culture
Consonance may also be determined by a listener’s cultural
background ( Arthurs, Beeston, & Timmers, 2018 ;Guernsey, 1928 ;
Johnson-Laird et al., 2012 ;Lundin, 1947 ;McDermott et al., 2016 ;
McLachlan, Marco, Light, & Wilson, 2013 ;Omigie, Dellacherie,
& Samson, 2017 ;Parncutt, 2006b ;Parncutt & Hair, 2011 ). Several
mechanisms for this effect are possible. Through the mere expo-sure effect ( Zajonc, 2001 ), exposure to common chords in a
musical style might induce familiarity and hence liking. Throughclassical conditioning, the co-occurrence of certain musical fea-tures (e.g., interference) with external features (e.g., the violentlyrics in death metal music, Olsen, Thompson, & Giblin, 2018 )
might also induce aesthetic responses to these musical features.
It remains unclear which musical features might become con-
sonant through familiarity. One possibility is that listeners becomefamiliar with acoustic phenomena such as periodicity/harmonicity(McDermott et al., 2016 ). A second possibility is that listeners
internalize Western tonal structures such as diatonic scales(Johnson-Laird et al., 2012 ). Alternatively, listeners might develop
a granular familiarity with specific musical chords ( McLachlan et
al., 2013 ).
Other Theories
Vocal similarity. Vocal similarity theories hold that conso-
nance derives from acoustic similarity to human vocalizations(e.g., Bowling & Purves, 2015 ;Bowling et al., 2018 ;Schwartz et
al., 2003 ). A key feature of human vocalizations is periodicity/
harmonicity, leading some researchers to operationalize vocal sim-ilarity as the latter ( Gill & Purves, 2009 ). In such cases, vocal
similarity theories may be considered a subset of periodicity/harmonicity theories. However, Bowling et al. (2018) additionally
5Earlier work in a similar line can be found in Sorge (1747) , cited in
Plomp and Levelt (1965) andSethares (2005) .219 SIMULTANEOUS CONSONANCE

## Page 5

operationalize vocal similarity as the absence of frequency inter-
vals smaller than 50 Hz, arguing that such intervals are rarelyfound in human vocalizations. Indeed, such intervals are nega-tively associated with consonance; however, this phenomenon canalso be explained by interference minimization. To our knowledge,no studies have shown that vocal similarity contributes to conso-nance through paths other than periodicity/harmonicity and inter-ference. We therefore do not evaluate vocal similarity separatelyfrom interference and periodicity/harmonicity.
Fusion. Stumpf (1890 ,1898 ) proposed that consonance de-
rives from fusion , the perceptual merging of multiple harmonic
complex tones. The substance of this hypothesis depends on theprecise definition of fusion. Some researchers have operationalizedfusion as perceptual indiscriminability , that is, an inability to
identify the constituent tones of a sonority ( DeWitt & Crowder,
1987 ;McLachlan et al., 2013 ). This was encouraged by Stumpf’s
early experiments investigating how often listeners erroneouslyjudged tone pairs as single tones ( DeWitt & Crowder, 1987 ;
Schneider, 1997 ). Subsequently, however, Stumpf wrote that fu-
sion should not be interpreted as indiscriminability but rather asthe formation of a coherent whole, with the sophisticated listenerbeing able to attend to individual chord components at will ( Sch-
neider, 1997 ). Stumpf later wrote that he was unsure whether
fusion truly caused consonance; instead, he suggested that fusionand consonance might both stem from harmonicity recognition(Plomp & Levelt, 1965 ;Schneider, 1997 ).
Following Stumpf, several subsequent studies have investigated
the relationship between fusion and consonance, but with mixedfindings. Guernsey (1928) andDeWitt and Crowder (1987) tested
fusion by playing participants different dyads and asking howmany tones these chords contained. In both studies, prototypicallyconsonant musical intervals (octaves, perfect fifths) were mostlikely to be confused for single tones, supporting a link betweenconsonance and fusion. McLachlan et al. (2013) instead tested
fusion with a pitch-matching task, where each trial cycled betweena target chord and a probe tone, and participants were instructed tomanipulate the probe tone until it matched a specified chord tone(lowest, middle, or highest). Pitch-matching accuracy increased forprototypically consonant chords, suggesting (contrary to Stumpf’sclaims) that consonance was inversely related to fusion. It is
difficult to conclude much about Stumpf’s claims from thesestudies, partly because different studies have yielded contradictoryresults, and partly because none of these studies tested for causal
effects of fusion on consonance, as opposed to consonance andfusion both being driven by a common factor of periodicity/harmonicity.
Combination tones. Combination tones are additional spec-
tral components introduced by nonlinear sound transmission in theear’s physical apparatus (e.g., Parncutt, 1989 ;Smoorenburg, 1972 ;
Wever, Bray, & Lawrence, 1940 ). For example, two pure tones of
frequencies f
1,f2:f1/H11021f2can elicit combination tones including
thesimple difference tone (f/H11005f2/H11002f1) and the cubic difference
tone (f/H110052f1/H11002f2;Parncutt, 1989 ;Smoorenburg, 1972 ).
Combination tones were once argued to be an important mech-
anism for pitch perception, reinforcing a complex tone’s funda-mental frequency and causing it to be perceived even when notacoustically present (e.g., Fletcher, 1924 ; see Parncutt, 1989 ).
Combination tones were also argued to have important implica-tions for music perception, explaining phenomena such as chordroots and perceptual consonance ( Hindemith, 1945 ;Krueger,
1910 ;Tartini, 1754 , cited in Parncutt, 1989 ). However, subsequent
research showed that the missing fundamental persisted even whenthe difference tone was removed by acoustic cancellation ( Schouten,
1938 , described in Plomp, 1965 ), and that, in any case, difference
tones are usually too quiet to be audible for typical speech andmusic listening ( Plomp, 1965 ). We therefore do not consider
combination tones further.
Loudness and sharpness. Aures (1985a ,1985b ) describes
four aspects of sensory consonance: tonalness ,roughness ,loud-
ness, and sharpness . Tonalness is a synonym for periodicity/
harmonicity, already discussed as an important potential con-tributor to consonance. Roughness is an aspect of interference,also an important potential contributor to consonance. Loudnessis the perceptual correlate of a sound’s energy content; sharp-ness describes the energy content of high spectral frequencies.Historically, loudness and sharpness have received little atten-tion in the study of musical consonance, perhaps because musictheorists and psychologists have primarily been interested in theconsonance of transposition-invariant and loudness-invariantstructures such as pitch-class sets, for which loudness andsharpness are undefined. We do not consider these phenomenafurther.
Evenness. The constituent notes of a musical chord can be
represented as points on a pitch line or apitch-class circle (e.g.,
Tymoczko, 2016 ). The evenness of the resulting distribution
can be characterized in various ways, including the differencein successive interval sizes ( Cook, 2009 ,2017 ;Cook & Fu-
jisawa, 2006 ), the difference between the largest and smallest
interval sizes ( Parncutt et al., 2018 ), and the standard deviation
of interval sizes ( Parncutt et al., 2018 ). In the case of Cook’s
(2009 ,2017 ,Cook & Fujisawa, 2006 ) models, each chord note
is expanded into a harmonic complex tone, and pitch distancesare computed between the resulting partials; in the other cases,pitch distances are computed between fundamental frequencies,presumably as inferred through periodicity/harmonicity detec-tion.
Evenness may contribute negatively to consonance. When a
chord contains multiple intervals of the same size, these inter-vals may become confusable and impede perceptual organiza-tion, hence decreasing consonance ( Cook, 2009 ,2017 ;Cook &
Fujisawa, 2006 ;Meyer, 1956 ). For example, a major triad in
pitch-class space contains the intervals of a major third, a minorthird, and a perfect fourth, and each note of the triad participatesin a unique pair of these intervals, one connecting it to the noteabove, and one connecting it to the note below. In contrast, anaugmented triad contains only intervals of a major third, and soeach note participates in an identical pair of intervals. Corre-spondingly, the individual notes of the augmented triad may beconsidered less distinctive than those of the major triad.
Evenness may also contribute positively, but indirectly, to con-
sonance. Spacing harmonics evenly on a critical-band scale typi-cally reduces interference, thereby increasing consonance (see,e.g., Huron & Sellmer, 1992 ;Plomp & Levelt, 1965 ). Evenness
also facilitates efficient voice leading, and therefore may contrib-ute positively to sequential consonance ( Parncutt et al., 2018
;
Tymoczko, 2011 ).
Evenness is an interesting potential contributor to consonance,
but so far it has received little empirical testing. We do not220 HARRISON AND PEARCE

## Page 6

consider it to be sufficiently well-supported to include in this
paper’s analyses, but we encourage future empirical research onthe topic.
Current Evidence
Evidence for disambiguating different theories of consonance
perception can be organized into three broad categories: stim-
ulus effects ,listener effects , and composition effects . We review
each of these categories in turn, and summarize our conclusionsinTable 1 .
Stimulus Effects
We begin by discussing stimulus effects , ways in which conso-
nance perception varies as a function of the stimulus.
Tone spectra. A chord’s consonance depends on the spectral
content of its tones. With harmonic tone spectra, peak consonanceis observed when the fundamental frequencies are related bysimple frequency ratios (e.g., Stolzenburg, 2015 ). With pure tone
spectra, these peaks at integer ratios disappear, at least for musi-cally untrained listeners ( Kaestner, 1909 ;Plomp & Levelt, 1965 ).
With inharmonic tone spectra, the peaks at integer ratios arereplaced by peaks at ratios determined by the inharmonic spectra(Geary, 1980 ;Pierce, 1966 ;Sethares, 2005 ).
6The consonance of
harmonic tone combinations can also be increased by selectivelydeleting harmonics responsible for interference ( Vos, 1986 ),though Nordmark and Fahlén (1988) report limited success with
this technique.
Interference theories clearly predict these effects of tone spectra
on consonance (for harmonic and pure tones, see Plomp & Levelt,
1965 ; for inharmonic tones, see Sethares, 1993 ,2005 ). In contrast,
neither periodicity/harmonicity nor cultural theories clearly predictthese phenomena. This suggests that interference does indeedcontribute toward consonance perception.
Pitch height. A given interval ratio typically appears less
consonant if it appears at low frequencies ( Plomp & Levelt, 1965 ).
Interference theories predict this phenomenon by relating conso-nance to pitch distance on a critical-bandwidth scale; a given ratiocorresponds to a smaller critical-bandwidth distance if it appears atlower frequencies ( Plomp & Levelt, 1965 ). In contrast, neither
periodicity/harmonicity nor cultural theories predict this sensitivityto pitch height.
Dichotic presentation. Interference between partials is thought
to take place primarily within the inner ear. Correspondingly, theinterference of a given pair of pure tones can be essentiallyeliminated by dichotic presentation, where each tone is presented to
a separate ear. Periodicity/harmonicity detection, meanwhile, isthought to be a central process that combines information fromboth ears ( Cramer & Huggins, 1958 ;Houtsma & Goldstein, 1972 ).
Correspondingly, the contribution of periodicity/harmonicity de-tection to consonance perception should be unaffected by dichoticpresentation.
Bidelman and Krishnan (2009) report consonance judgments for
dichotically presented pairs of complex tones. Broadly speaking,participants continued to differentiate prototypically consonantand dissonant intervals, suggesting that interference is insufficientto explain consonance. Unexpectedly, however, the tritone andperfect fourth received fairly similar consonance ratings. Thisfinding needs to be explored further.
Subsequent studies have investigated the effect of dichotic pre-
sentation on consonance judgments for pairs of pure tones ( Cous-
ineau et al., 2012 ;McDermott et al., 2010 ,2016 ). These studies
show that dichotic presentation reliably increases the consonanceof small pitch intervals, in particular major and minor seconds, aspredicted by interference theories. This would appear to supportinterference theories of consonance, though it is unclear whetherthese effects generalize to the complex tone spectra of real musicalinstruments.
Familiarity. McLachlan et al. (2013 , Experiment 2) trained
nonmusicians to perform a pitch-matching task on two-notechords. After training, participants judged chords from the trainingset as more consonant than novel chords. These results could beinterpreted as evidence that consonance is positively influenced byexposure, consistent with the mere exposure effect, and supportinga cultural theory of consonance. However, the generalizability ofthis effect has yet to be confirmed.
Chord structure. Western listeners consider certain chords
(e.g., the major triad) to be more consonant than others (e.g., theaugmented triad). It is possible to test competing theories ofconsonance by operationalizing the theories as computationalmodels and testing their ability to predict consonance judgments.
6Audio examples from Sethares (2005) are available at http://sethares
.engr.wisc.edu/html/soundexamples.html .Table 1
Summarized Evidence for the Mechanisms Underlying WesternConsonance Perception
Evidence InterferencePeriodicity/
harmonicity Culture
Stimulus effects
Tone spectra ✓
Pitch height ✓
Dichotic presentation ✠
Familiarity ( ✓)
Chord structure ( ✓)( ✓)( ✓)
¡This paper: Perceptual
analyses ✓✓ (✓)
Listener effects
Western listeners ( ✗) ✓
Congenital amusia ✓
Non-Western listeners ✓
Infants ( ✠)
Animals ( ✠)
Composition effects
Musical scales ✓
Manipulation of interference ✓✓
Chord spacing (Western music) ✓
Chord prevalences (Western
music) ( ✓)( ✓)
¡This paper: Corpus analyses ✓✓
Note . Each row identifies a section in Current Evidence .“✓” denotes
evidence that a mechanism contributes to Western consonance perception.“✗” denotes evidence that a mechanism is notrelevant to Western conso-
nance perception. “ ✠” denotes evidence that a mechanism is insufficient to
explain Western consonance perception. Parentheses indicate tentativeevidence; blank spaces indicate a lack of evidence.221 SIMULTANEOUS CONSONANCE

## Page 7

Unfortunately, studies using this approach have identified con-
flicting explanations for consonance:
1. Interference ( Hutchinson & Knopoff, 1978 );
2. Interference and additional unknown factors ( Vassilakis,
2001 );
3. Interference and cultural knowledge ( Johnson-Laird et
al., 2012 );
4. Periodicity/harmonicity ( Stolzenburg, 2015 );
5. Periodicity/harmonicity and interference ( Marin, Forde,
Gingras, & Stewart, 2015 );
6. Interference and sharpness ( Lahdelma & Eerola, 2016 );
7. Vocal similarity ( Bowling et al., 2018 ).
These contradictions may often be attributed to methodological
problems:
1. Different studies test different theories, and rarely test
more than two theories simultaneously.
2. Stimulus sets are often too small to support reliable
inferences.7
3.Stolzenburg (2015) evaluates models using pairwise cor-
relations, implicitly assuming that only one mechanism(e.g., periodicity/harmonicity, interference) determinesconsonance. Multiple regression would be necessary tocapture multiple simultaneous mechanisms.
4. The stimulus set of Marin et al. (2015) constitutes 12
dyads each transposed four times; the conditional depen-dencies between transpositions are not accounted for inthe linear regressions, inflating Type I error.
5.Johnson-Laird et al. (2012) do not report coefficients or
pvalues for their fitted regression models; they do report
hierarchical regression statistics, but these statistics donot test their primary research question, namely whetherinterference and cultural knowledge simultaneously con-
tribute to consonance.
6. The audio-based periodicity/harmonicity model used by
Lahdelma and Eerola (2016) fails when applied to com-
plex stimuli such as chords (see the Perceptual Analysessection).
These methodological problems and contradictory findings
make it difficult to generalize from this literature.
Listener Effects
We now discuss listener effects , ways in which consonance
perception varies as a function of the listener.
Western listeners. McDermott et al. (2010) tested competing
theories of consonance perception using an individual-differencesapproach. They constructed three psychometric measures, testing:(a)Interference preferences , operationalized by playing listeners
pure-tone dyads and subtracting preference ratings for dichoticpresentation (one tone in each ear) from ratings for diotic presen-tation (both tones in both ears); (b) Periodicity/harmonicity pref-
erences , operationalized by playing listeners subsets of a harmonic
complex tone and subtracting preference ratings for the originalversion from ratings for a version with perturbed harmonics; (c)Consonance preferences , operationalized by playing listeners 14
musical chords, and subtracting preference ratings for the globallyleast-preferred chords from the globally most-preferred chords.
Consonance preferences correlated with periodicity/harmonicity
preferences but not with interference preferences. This suggeststhat consonance may be driven by periodicity/harmonicity, notinterference. However, these findings must be considered prelim-inary given the limited construct validation of the three psycho-metric measures. Future work must examine whether these mea-sures generalize to a wider range of stimulus manipulations andresponse paradigms.
Congenital amusia. Congenital amusia is a lifelong cognitive
disorder characterized by difficulties in performing simple musicaltasks ( Ayotte, Peretz, & Hyde, 2002 ;Stewart, 2011 ). Using the
individual-differences tests of McDermott et al. (2010) (see the
Western listeners section), Cousineau et al. (2012) found that
amusics exhibited no aversion to traditionally dissonant chords,normal aversion to interference, and an inability to detect period-icity/harmonicity. Because the aversion to interference did nottransfer to dissonant chords, Cousineau et al. (2012) concluded
that interference is irrelevant to consonance perception. However,Marin et al. (2015) subsequently identified small but reliable
preferences for consonance in amusics, and showed with regres-sion analyses that these preferences were driven by interference,whereas nonamusic preferences were driven by both interferenceand periodicity/harmonicity. This discrepancy between Cousineau
et al. (2012) andMarin et al. (2015) needs further investigation.
Non-Western listeners. Cross-cultural research into conso-
nance perception has identified high similarity between the con-sonance judgments of Western and Japanese listeners ( Butler &
Daston, 1968 ), but low similarity between Western and Indian
listeners ( Maher, 1976 ), and between Westerners and native Ama-
zonians from the Tsimane’ society ( McDermott et al., 2016 ).
Exploring these differences further, McDermott et al. (2016) found
that Tsimane’ and Western listeners shared an aversion to inter-ference and an ability to perceive periodicity/harmonicity, but,unlike Western listeners, the Tsimane’ had no preference for
periodicity/harmonicity.
These results suggest that cultural exposure significantly affects
consonance perception. The results of McDermott et al. (2016)
additionally suggest that this effect of cultural exposure may bemediated by changes in preference for periodicity/harmonicity.
Infants. Consonance perception has been demonstrated in
toddlers ( Di Stefano et al., 2017 ), 6-month-old infants ( Crowder,
Reznick, & Rosenkrantz, 1991 ;Trainor & Heinmiller, 1998 ),
4-month-old infants ( Trainor, Tsang, & Cheung, 2002 ;Zentner &
7For example, Stolzenburg (2015 , Table 4) tabulates correlation coef-
ficients for 15 consonance models as evaluated on 12 dyads; the mediancorrelation of .939 has a 95% confidence interval spanning from .79 to .98,encompassing all but one of the reported coefficients.222 HARRISON AND PEARCE

## Page 8

Kagan, 1998 ), 2-month-old infants ( Trainor et al., 2002 ), and
newborn infants ( Masataka, 2006 ;Perani et al., 2010 ;Virtala,
Huotilainen, Partanen, Fellman, & Tervaniemi, 2013 ).Masataka
(2006) additionally found preserved consonance perception in
newborn infants with deaf parents. These results suggest thatconsonance perception does not solely depend on cultural ex-posure.
A related question is whether infants prefer consonance to
dissonance. Looking-time paradigms address this question, testingwhether infants preferentially look at consonant or dissonant soundsources ( Crowder et al., 1991 ;Masataka, 2006 ;Plantinga &
Trehub, 2014 ;Trainor & Heinmiller, 1998 ;Trainor et al., 2002 ;
Zentner & Kagan, 1998 ). With the exception of Plantinga and
Trehub (2014) , these studies each report detecting consonance
preferences in infants. However, Plantinga and Trehub (2014)
failed to replicate several of these results, and additionally questionthe validity of looking-time paradigms, noting that looking timesmay be confounded by features such as familiarity and compre-hensibility. These problems may partly be overcome by physicalplay-based paradigms (e.g., Di Stefano et al., 2017 ), but such
paradigms are unfortunately only applicable to older infants.
In conclusion, therefore, it seems that young infants perceive
some aspects of consonance, but it is unclear whether they preferconsonance to dissonance. These conclusions provide tentativeevidence that consonance perception is not solely cultural.
Animals. Animal studies could theoretically provide compel-
ling evidence for noncultural theories of consonance. If animalswere to display sensitivity or preference for consonance despitezero prior musical exposure, this would indicate that consonancecould not be fully explained by cultural learning.
Most studies of consonance perception in animals fall into
two categories: discrimination studies and preference studies
(see Toro & Crespo-Bojorque, 2017 for a review). Discrimina-
tion studies investigate whether animals can be taught to dis-criminate consonance from dissonance in unfamiliar sounds.Preference studies investigate whether animals prefer conso-nance to dissonance.
Discrimination studies have identified consonance discrimina-
tion in several nonhuman species, but methodological issues limitinterpretation of their findings. Experiment 5 of Hulse, Bernard,
and Braaten (1995) suggests that starlings may be able to discrim-
inate consonance from dissonance, but their stimulus set containsjust four chords. Experiment 2 of Izumi (2000) suggests that
Japanese monkeys may be able to discriminate consonance fromdissonance, but this study likewise relies on just four chords atdifferent transpositions. Watanabe, Uozumi, and Tanaka (2005)
claim to show consonance discrimination in Java sparrows, but thesparrows’ discriminations can also be explained by interval-sizejudgments.
8Conversely, studies of pigeons ( Brooks & Cook,
2010 ) and rats ( Crespo-Bojorque & Toro, 2015 ) have failed to
show evidence of consonance discrimination (but see also Borch-
grevink, 1975 ).9
Preference studies have identified consonance preferences in
several nonhuman animals. Using stimuli from a previous infantconsonance study ( Zentner & Kagan, 1998 ),Chiandetti and Val-
lortigara (2011) found that newly hatched domestic chicks spent
more time near consonant sound sources than dissonant soundsources. Sugimoto et al. (2010) gave an infant chimpanzee the
ability to select between consonant and dissonant two-part melo-dies, and found that the chimpanzee preferentially selected conso-
nant melodies. However, these studies have yet to be replicated,and both rely on borderline pvalues ( p/H11005.03). Other studies have
failed to demonstrate consonance preferences in Campbell’s mon-keys ( Koda et al., 2013 ) or cotton-top tamarins ( McDermott &
Hauser, 2004 ).
These animal studies provide an important alternative perspec-
tive on consonance perception. However, recurring problems withthese studies include small stimulus sets, small sample sizes, anda lack of replication studies. Future work should address theseproblems.
Composition Effects
Here we consider how compositional practice may provide
evidence for the psychological mechanisms underlying conso-nance perception.
Musical scales. Ascale divides an octave into a set of pitch
classes that can subsequently be used to generate musical material.Scales vary cross-culturally, but certain cross-cultural similaritiesbetween scales suggest common perceptual biases.
Gill and Purves (2009) argue that scale construction is biased
toward harmonicity maximization, and explain harmonicity max-imization as a preference for vocal-like sounds. They introduce acomputational model of harmonicity, which successfully recoversseveral important scales in Arabic, Chinese, Indian, and Westernmusic. However, they do not test competing consonance models,and admit that their results may also be explained by interferenceminimization.
Gamelan music and Thai classical music may help distin-
guish periodicity/harmonicity from interference. Both traditionsuse inharmonic scales whose structures seemingly reflect theinharmonic spectra of their percussion instruments ( Sethares,
2005 ). Sethares provides computational analyses relating these
scales to interference minimization; periodicity/harmonicity,meanwhile, offers no obvious explanation for these scales.
10
These findings suggest that interference contributes cross-culturally to consonance perception.
Manipulation of interference. Western listeners typically per-
ceive interference as unpleasant, but various other musical cultures
actively promote it. Interference is a key feature of the MiddleEastern mijwiz , an instrument comprising two blown pipes whose
relative tunings are manipulated to induce varying levels of inter-ference ( Vassilakis, 2005 ). Interference is also promoted in the
vocal practice of beat diaphony ,o rSchwebungsdiaphonie , where
two simultaneous voice parts sing in close intervals such as sec-onds. Beat diaphony can be found in various musical traditions,including music from Lithuania ( Ambrazevic ˇius, 2017 ;Vycˇiniene ˙,
8Zero of twelve of their consonant chords contain intervals smaller than
a minor third, whereas 15/16 of their dissonant chords contain suchintervals.
9Toro and Crespo-Bojorque (2017) also claim that consonance discrim-
ination has been demonstrated in black-capped chickadees, but we disagreein their interpretation of the cited evidence ( Hoeschele, Cook, Guillette,
Brooks, & Sturdy, 2012 ).
10It would be worth testing this formally, applying periodicity/harmo-
nicity consonance models (e.g. Harrison & Pearce, 2018 ) to the inharmonic
tone spectra of Gamelan and Thai classical music, and relating the resultsto scale structure.223 SIMULTANEOUS CONSONANCE

## Page 9

2002 ), Papua New Guinea ( Florian, 1981 ), and Bosnia ( Vassilakis,
2005 ). In contrast to Western listeners, individuals from these
traditions seem to perceive the resulting sonorities as consonant(Florian, 1981 ). These cross-cultural differences indicate that the
aesthetic valence of interference is, at least in part, culturallydetermined.
Chord spacing (Western music). In Western music, chords
seem to be spaced to minimize interference, most noticeably byavoiding small intervals in lower registers but permitting them inhigher registers ( Huron & Sellmer, 1992 ;McGowan, 2011 ;Plomp
& Levelt, 1965 ). Periodicity theories of consonance provide no
clear explanation for this phenomenon.
Chord prevalences (Western music). Many theorists have
argued that consonance played an integral role in determiningWestern compositional practice (e.g., Dahlhaus, 1990 ;Hindemith,
1945 ;Rameau, 1722 ). If so, it should be possible to test competing
theories of consonance by examining their ability to predict com-positional practice.
Huron (1991) analyzed prevalences of different intervals within
30 polyphonic keyboard works by J. S. Bach, and concluded thatthey reflected dual concerns of minimizing interference and min-imizing tonal fusion. Huron argued that interference was mini-mized on account of its negative aesthetic valence, whereas tonalfusion was minimized to maintain perceptual independence of thedifferent voices.
Parncutt et al. (2018) tabulated chord types in seven centuries of
vocal polyphony, and related their occurrence rates to severalformal models of diatonicity, interference, periodicity/harmonic-ity, and evenness. Most models correlated significantly with chordoccurrence rates, with fairly stable coefficient estimates acrosscenturies. These results suggest that multiple psychological mech-anisms contribute to consonance.
However, these findings must be treated as tentative, for the
following reasons: (a) The parameter estimates have low pre-cision due to the small sample sizes (12 dyads in Huron, 1991 ;
19 triads in Parncutt et al., 2018 )
11; (b) The pairwise correla-
tions reported in Parncutt et al. (2018) cannot capture effects of
multiple concurrent mechanisms (e.g., periodicity/harmonicityand interference).
Discussion
Table 1 summarizes the evidence contributed by these diverse
studies. We now use this evidence to reevaluate some claims in therecent literature.
Role of periodicity/harmonicity. Recent work has claimed
that consonance is primarily determined by periodicity/harmonic-ity, with the role of periodicity/harmonicity potentially moderatedby musical background ( Cousineau et al., 2012 ;McDermott et al.,
2010 ,2016 ). In our view, a significant contribution of periodicity/
harmonicity to consonance is indeed supported by the presentliterature, in particular by individual-differences research and con-genital amusia research (see Table 1 ). A moderating effect of
musical background also seems likely, on the basis of cross-cultural variation in music perception and composition. However,quantitative descriptions of these effects are missing: It is unclearwhat proportion of consonance may be explained by periodicity/harmonicity, and it is unclear how sensitive consonance is tocultural exposure.Role of interference. Recent work has also claimed that
consonance is independent of interference ( Bowling & Purves,
2015 ;Bowling et al., 2018 ;Cousineau et al., 2012 ;McDermott
et al., 2010 ,2016 ). In our view, the wider literature is incon-
sistent with this claim (see Table 1 ). The main evidence against
interference comes from the individual-differences study ofMcDermott et al. (2010) , but this evidence is counterbalanced
by several positive arguments for interference, including studiesof tone spectra, pitch height, chord voicing in Western music,scale tunings in Gamelan music and Thai classical music, andcross-cultural manipulation of interference for expressive ef-fect.
Role of culture. Cross-cultural studies of music perception
and composition make it clear that culture contributes to con-sonance perception (see Table 1 ). The mechanisms of this effect
remain unclear, however: Some argue that Western listenersinternalize codified conventions of Western harmony ( Johnson-
Laird et al., 2012 ), whereas others argue that Westerners simply
learn aesthetic preferences for periodicity/harmonicity ( McDer-
mott et al., 2016 ). These competing explanations have yet to be
tested.
Conclusions. We conclude that consonance perception in
Western listeners is likely to be driven by multiple psycholog-ical mechanisms, including interference, periodicity/harmonic-ity, and cultural background (see Table 1 ). This conclusion is at
odds with recent claims that interference does not contribute toconsonance perception ( Cousineau et al., 2012 ;McDermott et
al., 2010 ,2016 ). In the rest of this paper, we therefore examine
our proposition empirically, computationally modeling largedatasets of consonance judgments and music compositions.
Computational Models
We begin by reviewing prominent computational models of
consonance from the literature, organizing them by psychologicaltheory and by modeling approach (see Figure 1 ).
Periodicity/Harmonicity: Ratio Simplicity
Chords tend to be more periodic when their constituent tones are
related by simple frequency ratios. Ratio simplicity can thereforeprovide a proxy for periodicity/harmonicity. Previous research hasformalized ratio simplicity in various ways, with the resultingmeasures predicting the consonance of just-tuned chords fairlywell (e.g., Euler, 1739 ;Geer, Levelt, & Plomp, 1962 ;Levelt, Geer,
& Plomp, 1966 ;Schellenberg & Trehub, 1994 ).
12Unfortunately,
these measures generally fail to predict consonance for chords thatare not just-tuned. A particular problem is disproportionate sensi-tivity to small tuning deviations: For example, an octave stretchedby 0.001% still sounds consonant, despite corresponding to a verycomplex frequency ratio (200,002:100,000). However, Stolzen-
burg (2015) provides an effective solution to this by introducing a
preprocessing step where each note is adjusted to maximize ratiosimplicity with respect to the bass note. These adjustments are not
11For example, a correlation coefficient of r/H110050.5 with 19 triads has a
95% confidence interval of [0.06, 0.78].
12A chord is just-tuned when its pitches are drawn from a just-tuned
scale. A just-tuned scale is a scale tuned to maximize ratio simplicity.224 HARRISON AND PEARCE

## Page 10

permitted to change the interval size by more than 1.1%. Stolzen-
burg argues that such adjustments are reasonable given humanperceptual inaccuracies in pitch discrimination. Having expressedeach chord frequency as a fractional multiple of the bass fre-quency, ratio simplicity is then computed as the lowest commonmultiple of the fractions’ denominators. Stolzenburg terms thisexpression relative periodicity , and notes that, assuming harmonic
tones, relative periodicity corresponds to the chord’s overall
period length divided by the bass tone’s period length. Relativeperiodicity values are then postprocessed with logarithmictransformation and smoothing to produce the final model output(see Stolzenburg, 2015 for details).
Periodicity/Harmonicity: Spectral Pattern Matching
Spectral pattern-matching models of consonance follow directly
from spectral pattern-matching theories of pitch perception (seethe Consonance Theories section). These models operate in the
frequency domain, searching for spectral patterns characteristic of
periodic sounds.
Terhardt (1982) ;Parncutt (1988) .Terhardt (1982) andParn-
cutt (1988) both frame consonance in terms of chord-root percep-
tion. In Western music theory, the chord root is a pitch classsummarizing a chord’s tonal content, which (according to Terhardtand Parncutt) arises through pattern-matching processes of pitchperception. Consonance arises when a chord has a clear root;dissonance arises from root ambiguity.
Both Terhardt’s (1982) andParncutt’s (1988) models use har-
monic templates quantized to the Western 12-tone scale, with thetemplates represented as octave-invariant pitch class sets. Eachpitch class receives a numeric weight, quantifying how well thechord’s pitch classes align with a harmonic template rooted on thatpitch class. These weights preferentially reward coincidence withSimultaneous
consonancePeriodicity/
harmonicity
Interference
CultureRatio
simplicity
Spectral pattern
matching
Temporal
autocorrelationStolzenburg (2015)
Parncutt (1988)
Parncutt (1993)
Parncutt & Strasburger (1994)
Gill & Purves (2009)
Kameoka & Kuriyagawa (1969b)
Hutchinson & Knopoff (1978)Lartillot et al. (2008)
Harrison & Pearce (2018)
Boersma (1993)
Ebeling (2008)
Trulla et al. (2018)
Huron (1994)
Bowling et al. (2018)
Vassilakis (2001)
Weisser & Lartillot (2013)
Parncutt & Strasburger (1994)
Leman (2000)
Skovenborg (2002)
Wang et al. (2013)
Vencovský (2016)
Johnson-Laird et al. (2012)
This paperComplex
dyads
Pure
dyadsTerhardt 
(1982)
Parncutt
(1989)
Terhardt et al.
(1982a)
Milne
(2013)
Plomp & Levelt
(1965)
Sethares
(1993)
Parncutt (1989)
Terhardt et al.
(1982a)
Daniel & Weber
(1997)
Aures
(1985)Waveforms
StatisticsRules
Figure 1. Consonance models organized by psychological theory and modeling approach. Dashed borders
indicate models not evaluated in our empirical analyses. Arrows denote model revisions. See the online articlefor the color version of this figure.225 SIMULTANEOUS CONSONANCE

## Page 11

primary harmonics such as the octave, perfect fifth, and major
third.13The chord root is estimated as the pitch class with the
greatest weight; root ambiguity is then operationalized by dividingthe total weight by the maximum weight. According to Terhardtand Parncutt, root ambiguity should then negatively predict con-sonance.
Parncutt (1989) ;Parncutt and Strasburger (1994) .Parncutt’s
(1989) model constitutes a musical revision of Terhardt et al.’s
(1982a) pitch perception algorithm. Parncutt and Strasburger’s
(1994) model, in turn, represents a slightly updated version of
Parncutt’s (1989) model.
Like Parncutt’s (1988) model, Parncutt’s (1989) model formu-
lates consonance in terms of pattern-matching pitch perception. AsinParncutt (1988) , the algorithm works by sweeping a harmonic
template across an acoustic spectrum, seeking locations where thetemplate coincides well with the acoustic input; consonance iselicited when the location of best fit is unambiguous. However,Parncutt’s (1989) algorithm differs from Parncutt (1988) in several
important ways: (a) Chord notes are expanded into their impliedharmonics; (b) Psychoacoustic phenomena such as hearing thresh-olds, masking, and audibility saturation are explicitly modeled; (c)The pattern-matching process is no longer octave-invariant.
Parncutt (1989) proposes two derived measures for predicting
consonance: pure tonalness andcomplex tonalness .
14Pure tonal-
ness describes the extent to which the input spectral componentsare audible, after accounting for hearing thresholds and masking.Complex tonalness describes the audibility of the strongest virtualpitch percept. The former may be considered a interference model,the latter a periodicity/harmonicity model.
Parncutt and Strasburger (1994) describe an updated version of
Parncutt’s (1989) algorithm. The underlying principles are the
same, but certain psychoacoustic details differ, such as the calcu-lation of pure-tone audibility thresholds and the calculation ofpure-tone height. We evaluate this updated version here.
Parncutt (1993) presents a related algorithm for modeling the
perception of octave-spaced tones (also known as Shepard tones).Because octave-spaced tones are uncommon in Western music, wedo not evaluate the model here.
Gill and Purves (2009) .Gill and Purves (2009) present a
pattern-matching periodicity/harmonicity model which they applyto various two-note chords. They assume just tuning, which allowsthem to compute each chord’s fundamental frequency as the great-est common divisor of the two tones’ frequencies. They thenconstruct a hypothetical harmonic complex tone rooted on thisfundamental frequency, and calculate what proportion of thistone’s harmonics are contained within the spectrum of the originalchord. This proportion forms their periodicity/harmonicity mea-sure. This approach has been shown to generalize well to three-and four-note chords ( Bowling et al., 2018 ). However, the model’s
cognitive validity is limited by the fact that, unlike human listen-ers, it is very sensitive to small deviations from just tuning orharmonic tone spectra.
Peeters et al. (2011) ;Bogdanov et al. (2013) ;Lartillot et al.
(2008) .Several prominent audio analysis toolboxes—the Timbre
Toolbox ( Peeters et al., 2011 ), Essentia ( Bogdanov et al., 2013 ),
and MIRtoolbox ( Lartillot et al., 2008 )—contain inharmonicity
measures. Here we examine their relevance for consonance mod-
eling.The inharmonicity measure in the Timbre Toolbox ( Peeters et
al., 2011 ) initially seems relevant for consonance modeling, being
calculated by summing each partial’s deviation from harmonicity.However, the algorithm’s preprocessing stages are clearly de-signed for single tones rather than tone combinations. Each inputspectrum is preprocessed to a harmonic spectrum, slightly de-formed by optional stretching; this may be a reasonable approxi-mation for single tones, but it is inappropriate for tone combina-tions. We therefore do not consider this model further.
Essentia ( Bogdanov et al., 2013 ) contains an inharmonicity
measure defined similarly to the Timbre Toolbox ( Peeters et al.,
2011 ). As with the Timbre Toolbox, this feature is clearly intended
for single tones rather than tone combinations, and so we do notconsider it further.
MIRtoolbox ( Lartillot et al., 2008 ) contains a more flexible
inharmonicity measure. First, the fundamental frequency is esti-mated using autocorrelation and peak-picking; inharmonicity isthen estimated by applying a sawtooth filter to the spectrum, withtroughs corresponding to integer multiples of the fundamentalfrequency, and then integrating the result. This measure seemsmore likely to capture inharmonicity in musical chords, and indeedit has been recently used in consonance perception research ( Lah-
delma & Eerola, 2016 ). However, systematic validations of this
measure are lacking.
Milne (2013) ;Harrison and Pearce (2018) .Milne (2013)
presents a periodicity/harmonicity model that operates on pitch-class spectra (see also Milne et al., 2016 ). The model takes a
pitch-class set as input, and expands all tones to idealized har-monic spectra. These spectra are superposed additively, and thenblurred by convolution with a Gaussian distribution, mimickingperceptual uncertainty in pitch processing. The algorithm thensweeps a harmonic template over the combined spectrum, calcu-lating the cosine similarity between the template and the combinedspectrum as a function of the template’s fundamental frequency.The frequency eliciting the maximal cosine similarity is identifiedas the fundamental frequency, and the resulting cosine similarity istaken as the periodicity/harmonicity estimate.
Harrison and Pearce (2018) suggest that picking just one funda-
mental frequency may be inappropriate for larger chords, wherelisteners may instead infer several candidate fundamental frequencies.They therefore treat the cosine-similarity profile as a probabilitydistribution, and define periodicity/harmonicity as the Kullback-Leibler divergence to this distribution from a uniform distribution.The resulting measure can be interpreted as the information-theoreticuncertainty of the pitch-estimation process.
Periodicity/Harmonicity: Temporal Autocorrelation
Temporal autocorrelation models of consonance follow directly
from autocorrelation theories of pitch perception (see Consonance
Theories ). These models operate in the time domain, looking for
time lags at which the signal correlates with itself: High autocor-relation implies periodicity and hence consonance.
13The weights assigned to each harmonic differ between studies; Ter-
hardt (1982) used binary weights, but Parncutt (1988) introduced graduated
weights, which he updated in later work (see Parncutt, 2006a ).
14These measures were later termed pure and complex sonorousness by
Parncutt and Strasburger (1994) .226 HARRISON AND PEARCE

## Page 12

Boersma (1993) .Boersma’s (1993) autocorrelation algorithm
can be found in the popular phonetics software Praat. The algo-rithm tracks the fundamental frequency of an acoustic input overtime, and operationalizes periodicity as the harmonics-to-noise
ratio , the proportion of power contained within the signal’s peri-
odic component. Marin et al. (2015) found that this algorithm had
some power to predict the relative consonance of different dyads.However, the details of the algorithm lack psychological realism,having been designed to solve an engineering problem rather thanto simulate human perception. This limits the algorithm’s appeal asa consonance model.
Ebeling (2008) .Ebeling’s (2008) autocorrelation model esti-
mates the consonance of pure-tone intervals. Incoming pure tonesare represented as sequences of discrete pulses, reflecting the neuronalrate coding of the peripheral auditory system. These pulse sequencesare additively superposed to form a composite pulse sequence, forwhich the autocorrelation function is computed. The generalized
coincidence function is then computed by integrating the squared
autocorrelation function over a finite positive range of time lags.Applied to pure tones, the generalized coincidence function recoversthe traditional hierarchy of intervallic consonance, and mimics listen-ers in being tolerant to slight mistunings. Ebeling presents this as apositive result, but it is inconsistent with Plomp and Levelt’s (1965)
observation that, after accounting for musical training, pure tones donot exhibit the traditional hierarchy of intervallic consonance. Itremains unclear whether the model would successfully generalize tolarger chords or to complex tones.
Trulla, Stefano, and Giuliani (2018) .Trulla et al.’s (2018)
model uses recurrence quantification analysis to model the con-
sonance of pure-tone intervals. Recurrence quantification analysisperforms a similar function to autocorrelation analysis, identifyingtime lags at which waveform segments repeat themselves. Trulla et
al. (2018) use this technique to quantify the amount of repetition
within a waveform, and show that repetition is maximized bytraditionally consonant frequency ratios, such as the just-tunedperfect fifth (3:2). The algorithm constitutes an interesting newapproach to periodicity/harmonicity detection, but one that lacksmuch cognitive or neuroscientific backing. As with Ebeling
(2008) , it is also unclear how well the algorithm generalizes to
larger chords or to different tone spectra, and the validation suffersfrom the same problems described above for Ebeling’s model.
Summary. Autocorrelation is an important candidate mecha-
nism for consonance perception. However, autocorrelation conso-nance models have yet to be successfully generalized outsidesimple tone spectra and two-note intervals. We therefore do notevaluate these models in the present work, but we look forward tofuture research in this area (see, e.g., Tabas et al., 2017 ).
Interference: Complex Dyads
Complex-dyad models of interference search chords for com-
plex dyads known to elicit interference. These models are typicallyhand-computable, making them well-suited to quick consonanceestimation.
Huron (1994) .Huron (1994) presents a measure termed ag-
gregate dyadic consonance , which characterizes the consonance of
a pitch-class set by summing consonance ratings for each pitch-class interval present in the set. These consonance ratings arederived by aggregating perceptual data from previous literature.Huron (1994) originally used aggregate dyadic consonance to
quantify a scale’s ability to generate consonant intervals. Parncutt
et al. (2018) subsequently applied the model to musical chords,
and interpreted the output as an interference measure. The validityof this approach rests on the assumption that interference is addi-tively generated by pairwise interactions between spectral compo-nents; a similar assumption is made by pure-dyad interferencemodels (see the Interference: Pure Dyads section). A further as-sumption is that Huron’s dyadic consonance ratings solely reflectinterference, not (e.g.) periodicity/harmonicity; this assumption isarguably problematic, especially given recent claims that dyadicconsonance is driven by periodicity/harmonicity, not interference(McDermott et al., 2010 ;Stolzenburg, 2015 ).
Bowling et al. (2018) .Bowling et al. (2018) primarily explain
consonance in terms of periodicity/harmonicity, but also identifydissonance with chords containing pitches separated by less than50 Hz. They argue that such intervals are uncommon in humanvocalizations, and therefore elicit dissonance. We categorize thisproposed effect under interference, in line with Parncutt et al.’s
(2018) argument that these small intervals (in particular minor and
major seconds) are strongly associated with interference.
Interference: Pure Dyads
Pure-dyad interference models work by decomposing chords
into their pure-tone components, and accumulating interferencecontributions from each pair of pure tones.
Plomp and Levelt (1965) ;Kameoka and Kuriyagawa
(1969b) .Plomp and Levelt (1965) and Kameoka and Kuriya-
gawa (1969b) concurrently established an influential methodology
for consonance modeling: Use perceptual experiments to charac-terize the consonance of pure-tone dyads, and estimate the disso-nance of complex sonorities by summing contributions from eachpure dyad. However, their original models are rarely used today,having been supplanted by later work.
Hutchinson and Knopoff (1978) .Hutchinson and Knopoff
(1978) describe a pure-dyad interference model in the line of
Plomp and Levelt (1965) . Unlike Plomp and Levelt, Hutchinson
and Knopoff sum dissonance contributions over all harmonics,rather than just neighboring harmonics. The original model is notfully algebraic, relying on a graphically depicted mapping betweeninterval size and pure-dyad dissonance; a useful modification is thealgebraic approximation introduced by Bigand, Parncutt, and Le-
rdahl (1996) , which we adopt here (see also Mashinter, 2006 ).
Hutchinson and Knopoff (1978) only applied their model to
complex-tone dyads. They later applied their model to complex-tone triads ( Hutchinson & Knopoff, 1979 ), and for computational
efficiency introduced an approximation decomposing the interfer-ence of a triad into the contributions of its constituent complex-tone dyads (see previous discussion of Huron, 1994 ). With modern
computers, this approximation is unnecessary and hence rarelyused.
Sethares (1993) ;Vassilakis (2001) ;Weisser and Lartillot
(2013) .Several subsequent studies have preserved the general
methodology of Hutchinson and Knopoff (1978) while introducing
various technical changes. Sethares (1993) reformulated the equa-
tions linking pure-dyad consonance to interval size and pitchheight. Vassilakis (2001) andWeisser and Lartillot (2013) subse-
quently modified Sethares’s (1993) model, reformulating the rela-227 SIMULTANEOUS CONSONANCE

## Page 13

tionship between pure-dyad consonance and pure-tone amplitude.
These modifications generally seem principled, but the resultingmodels have received little systematic validation.
Parncutt (1989) ;Parncutt and Strasburger (1994) .As dis-
cussed above (see the Periodicity/Harmonicity: Spectral PatternMatching section), the pure tonalness measure of Parncutt (1989)
and the pure sonorousness measure of Parncutt and Strasburger
(1994) may be categorized as interference models. Unlike other
pure-dyad interference models, these models address masking, notbeating.
Interference: Waveforms
Dyadic models present a rather simplified account of interfer-
ence, and struggle to capture certain psychoacoustic phenomenasuch as effects of phase (e.g., Pressnitzer & McAdams, 1999 ) and
waveform envelope shape (e.g., Vencovský, 2016 ) on roughness.
The following models achieve a more detailed account of inter-ference by modeling the waveform directly.
Leman (2000) .Leman’s (2000) synchronization index model
measures beating energy within roughness-eliciting frequencyranges. The analysis begins with Immerseel and Martens’s (1992)
model of the peripheral auditory system, which simulates thefrequency response of the outer and middle ear, the frequencyanalysis of the cochlea, hair-cell transduction from mechanicalvibrations to neural impulses, and transmission by the auditorynerve. Particularly important is the half-wave rectification thattakes place in hair-cell transduction, which physically instantiatesbeating frequencies within the Fourier spectrum. Leman’s modelthen filters the neural transmissions according to their propensityto elicit roughness, and calculates the energy of the resultingspectrum as a roughness estimate. Leman illustrates model outputsfor several amplitude-modulated tones, and for two-note chordssynthesized with harmonic complex tones. The initial results seempromising, but we are unaware of any studies systematically fine-tuning or validating the model.
Skovenborg and Nielsen (2002) .Skovenborg and Nielsen’s
(2002) model is conceptually similar to Leman’s (2000) model.
The key differences are simulating the peripheral auditory systemusing the HUTear MATLAB toolbox ( Härmä & Palomäki, 1999 ),
rather than Immerseel and Martens’s (1992) model, and adopting
different definitions of roughness-eliciting frequency ranges. Theauthors provide some illustrations of the model’s application totwo-tone intervals of pure and complex tones. The model recoverssome established perceptual phenomena, such as the dissonanceelicited by small intervals, but also exhibits some undesirablebehavior, such as multiple consonance peaks for pure-tone inter-vals, and oversensitivity to slight mistunings for complex-toneintervals. We are unaware of further work developing this model.
Aures (1985c) ;Daniel and Weber (1997) ;Wang et al. (2013) .
Aures (1985c) describes a roughness model that has been succes-
sively developed by Daniel and Weber (1997) andWang et al.
(2013) . Here we describe the model as implemented in Wang et al.
(2013) . Like Leman (2000) andSkovenborg and Nielsen (2002) ,
the model begins by simulating the frequency response of the outerand middle ear, and the frequency analysis of the cochlea. UnlikeLeman (2000) andSkovenborg and Nielsen (2002) , the model does
not simulate hair-cell transduction or transmission by the auditorynerve. Instead, the model comprises the following steps: (a) Ex-tract the waveform envelope at each cochlear filter; (b) Filter the
waveform envelopes to retain the beating frequencies most asso-ciated with roughness; (c) For each filter, compute the modulation
index , summarizing beating magnitude as a proportion of the total
signal; (d) Multiply each filter’s modulation index by a phase
impact factor , capturing signal correlations between adjacent fil-
ters; high correlations yield higher roughness; (e) Multiply by aweighting factor identifying how different cochlear filters contrib-ute more to the perception of roughness; (f) Square the result andsum over cochlear filters.
Unlike the models of Leman (2000) and Skovenborg and
Nielsen (2002) , these three models are presented alongside objec-
tive perceptual validations. However, these validations are gener-ally restricted to relatively artificial and nonmusical stimuli.
Vencovský (2016) .Like Leman (2000) ;Skovenborg and
Nielsen (2002) , and Wang et al. (2013) ;Vencovský’s (2016)
model begins with a sophisticated model of the peripheral auditorysystem. The model of Meddis (2011) is used for the outer ear,
middle ear, inner hair cells, and auditory nerve; the model ofNobili, Vetešník, Turicchia, and Mammano (2003) is used for the
basilar membrane and cochlear fluid. The output is a neuronalsignal for each cochlear filter.
Roughness is then estimated from the neuronal signal’s enve-
lope, or beating pattern. Previous models estimate roughness fromthe amplitude of the beating pattern; Vencovský’s (2016) model
additionally accounts for the beating pattern’s shape. Consider asingle oscillation of the beating pattern; according to Vencovský’s
(2016) model, highest roughness is achieved when the difference
between minimal and maximal amplitudes is large, and when theprogression from minimal to maximal amplitudes (but not neces-sarily vice versa) is fast. Similar to previous models ( Daniel &
Weber, 1997 ;
Wang et al., 2013 ),Vencovský’s (2016) model also
normalizes roughness contributions by overall signal amplitudes,and decreases roughness when signals from adjacent cochlearchannels are uncorrelated.
Vencovský (2016) validates the model on perceptual data from
various types of artificial stimuli, including two-tone intervals ofharmonic complex tones, and finds that the model performs fairlywell. It is unclear how well the model generalizes to more complexmusical stimuli.
Culture
Cultural aspects of consonance perception have been empha-
sized by many researchers (see Consonance Theories ), but we are
only aware of one preexisting computational model instantiatingthese ideas: that of Johnson-Laird et al. (2012) .
Johnson-Laird et al. (2012) .Johnson-Laird et al. (2012) pro-
vide a rule-based model of consonance perception in Westernlisteners. The model comprises three rules, organized in decreasingorder of importance:
1. Chords consistent with a major scale are more consonant
than chords only consistent with a minor scale, which arein turn more consonant than chords not consistent witheither;
2. Chords are more consonant if they (a) contain a major
triad and (b) all chord notes are consistent with a majorscale containing that triad;228 HARRISON AND PEARCE

## Page 14

3. Chords are more consonant if they can be represented as
a series of pitch classes each separated by intervals of athird, optionally including one interval of a fifth.
Unlike most other consonance models, this model does not
return numeric scores, but instead ranks chords in order of theirconsonance. Ranking is achieved as follows: Apply the rules oneat a time, in decreasing order of importance, and stop when a ruleidentifies one chord as more consonant than the other. This pro-vides an estimate of cultural consonance.
Johnson-Laird et al. (2012) suggest that Western consonance
perception depends both on culture and on roughness. They cap-ture this idea with their dual-process model , which adds an extra
rule to the cultural consonance algorithm, applied only whenchords cannot be distinguished on the cultural consonance criteria.This rule predicts that chords are more consonant if they exhibitlower roughness. The authors operationalize roughness using themodel of Hutchinson and Knopoff (1978) .
The resulting model predicts chordal consonance rather effec-
tively ( Johnson-Laird et al., 2012 ;Stolzenburg, 2015 ). However, a
problem with this model is that the rules are hand-coded on thebasis of expert knowledge. The rules could represent culturalknowledge learned through exposure, but they could also explainpost hoc rationalizations of perceptual phenomena. This motivatesus to introduce an alternative corpus-based model, described be-low.
A corpus-based model of cultural familiarity. Here we in-
troduce a simple corpus-based model of cultural familiarity, rep-resenting the hypothesis that listeners become familiar with chordsin proportion to their frequency of occurrence in the listener’smusical culture, and that this familiarity positively influencesconsonance through the mere exposure effect ( Zajonc, 2001 ). We
simulate a Western listener’s musical exposure by tabulating theoccurrences of different chord types in the Billboard dataset ( Bur-
goyne, 2011 ), a large dataset of music from the U.S. charts. We
reason that this dataset should provide a reasonable first approxi-mation to the musical exposure of the average Western listener, butnote that this approach could easily be tailored to the specificmusical backgrounds of individual listeners. See the Method sec-tion for further details.
Perceptual Analyses
Here we reanalyze consonance perception data from four pre-
vious studies ( Bowling et al., 2018 ;Johnson-Laird et al., 2012 ;
Lahdelma & Eerola, 2016 ;Schwartz et al., 2003 ). These datasets
correspond to consonance judgments for Western musical chordsas made by listeners from Western musical cultures. We focus inparticular on the dataset from Bowling et al. (2018) , as it contains
considerably more chord types than previous datasets (see theMethod section for details). We make all these datasets availablein an accompanying R package, inconData .
Previous analyses of these datasets suffer from important limi-
tations. Several studies show that a dataset is consistent with theirproposed theory, but fail to test competing theories ( Bowling et al.,
2018 ;Schwartz et al., 2003 ). When competing theories are tested,
each theory is typically operationalized using just one computa-tional model ( Johnson-Laird et al., 2012 ;Lahdelma & Eerola,
2016 ), and the choice of model is fairly arbitrary, because fewcomparative model evaluations are available in the literature.
However, as we later show, models representing the same conso-nance theory can vary widely in performance. Furthermore, whenmultiple models are evaluated, parameter reliability is rarely con-sidered, encouraging inferences to be made from statistically in-significant differences ( Stolzenburg, 2015 ). Lastly, no studies si-
multaneously model contributions from periodicity/harmonicity,interference, and cultural familiarity, despite the implication fromthe empirical literature that all three phenomena may contribute toconsonance perception.
Here we address these problems. Our primary goal is to reeval-
uate competing theories of consonance perception; our secondarygoal is to facilitate future consonance research. Toward thesegoals, we compile 20 consonance models, 15 of which we imple-ment in this paper’s accompanying R package, and five of whichare available in publicly available audio analysis toolboxes (seeTable 2 ). We systematically evaluate these 20 models on our
perceptual data, providing future researchers an objective basis formodel selection. We then assess the evidence for a compositetheory of consonance perception, evaluating the extent to whichperiodicity/harmonicity, interference, and cultural familiarity si-multaneously contribute to consonance judgments. We include theresulting composite consonance model in the incon package.
For practical reasons, we do not try to evaluate every model in
the literature. In most cases, we only evaluate the latest publishedversion of a given model, and avoid models with limited ordiscouraging perceptual validations (e.g., Leman, 2000 ;Skoven-
borg & Nielsen, 2002 ). We also omit one model on the grounds of
its complexity ( Vencovský, 2016 ). See the Method section for
further details.
Evaluating Models Individually
We begin by evaluating each consonance model individually on
theBowling et al. (2018) dataset ( Figure 2A ). Our performance
metric is the partial correlation15between model predictions and
average consonance ratings, controlling for the number of notes ineach chord, with the latter treated as a categorical variable. Wecontrol for number of notes to account for a design-related con-found in Bowling et al. (2018) where stimulus presentation was
blocked by the number of notes in each chord, potentially allowingparticipants to recalibrate their response scales for each new num-ber of notes. We use predictive performance as an initial indicatorof a model’s cognitive validity and practical utility.
Competing theories of consonance. The three best-performing
models represent three different theories of consonance perception:interference ( r/H11005.77, 95% CI [.72, .81]), periodicity/harmonicity ( r/H11005
.72, 95% CI [.66, .77]), and cultural familiarity ( r/H11005.72, 95% CI [.66,
.77]). This similarity in performance is consistent with the idea thatthese three phenomena all contribute to consonance perception. Laterwe describe a regression analysis that provides a more principled testof this hypothesis.
Periodicity/harmonicity models. The most detailed periodic-
ity/harmonicity model tested is that of Parncutt and Strasburger
(1994) , which incorporates various psychoacoustic phenomena
including hearing thresholds, masking, and audibility saturation.
15All correlations in this paper are computed as Pearson correlation
coefficients, except where stated otherwise.229 SIMULTANEOUS CONSONANCE

## Page 15

However, this model’s performance ( r/H11005.56, 95% CI [.47, .63]) is
matched or beaten by four periodicity/harmonicity models withessentially no psychoacoustic modeling ( r/H11005.62, .65, .72, .72).
This suggests that these psychoacoustic details may be largelyirrelevant to the relationship between periodicity/harmonicity andconsonance.
Interference models. The interference models display an inter-
esting trend in performance: Since Hutchinson and Knopoff (1978) ,
performance has generally decreased, not increased. This is surpris-ing, because each successive model typically incorporates a moredetailed psychoacoustic understanding of the physics of amplitudefluctuation (exceptions are the complex-dyad models of Bowling et
al., 2018 , and Huron, 1994 , and the masking model of Parncutt &
Strasburger, 1994 ). This trend deserves to be explored further; an
interesting possibility is that amplitude-fluctuation models fail tocapture the potential contribution of masking to consonance (see theConsonance Theories section).
Cultural models. The new corpus-based consonance model
(r/H11005.72, 95% CI [.66, .77]) outperformed the rule-based conso-
nance model ( Johnson-Laird et al., 2012 ,r/H11005.63, 95% CI [.55,
.69]; 95% CI for the difference in correlations [.012, .017], afterZou, 2007 ).
16
Symbolic versus audio models. Many of the algorithms eval-
uated here take symbolic inputs, reducing each stimulus to a fewnumbers representing its constituent pitches. The other algorithmstake audio inputs, and therefore have access to the full spectralcontent of the stimulus. Given that consonance is sensitive to
spectral content, one might expect the audio algorithms to outper-form the symbolic algorithms. However, Figure 2A shows that this
is not the case: Generally speaking, the symbolic algorithms out-performed the audio algorithms. Particularly bad results were seenfor MIRtoolbox’s periodicity/harmonicity measure ( r/H11005.18, 95%
CI [.07, .29]) and Essentia’s interference measure ( r/H11005.19, 95% CI
[.08, .30]). Fairly good results were seen for MIRtoolbox’s inter-ference measure, which performed best using its default settings(original Sethares model; r/H11005.57, 95% CI [.49, .64]). Nonetheless,
this model was still outperformed by several simple symbolicmodels (e.g., Huron, 1994 ;Parncutt, 1988 ).
Wang et al.’s (2013) Model. The original model of Wang
et al. (2013) performed rather poorly ( r/H11005.17, 95% CI [.05,
.28]). This poor performance was surprising, given the sophis-ticated nature of the model and its position in a well-establishedmodeling tradition ( Aures, 1985c ;Daniel & Weber, 1997 ).
Experimenting with the model, we found its performance toimprove significantly upon disabling the “phase impact factors”component, whereby signal correlations between adjacent co-chlear filters increase roughness (resulting partial correlation:r/H11005.46, 95% CI [.37, .55]).
16All statistical comparisons of correlation coefficients reported in this
paper were conducted using the “cocor” package ( Diedenhofen & Musch,
2015 ).Table 2
Consonance Models Evaluated in the Present Work
Reference Original name Input Implementation
Periodicity/harmonicity
Gill and Purves (2009) Percentage similarity Symbolic incon (bowl18)
Harrison and Pearce (2018) Harmonicity Symbolic incon (har18)
Milne (2013) Harmonicity Symbolic incon (har18)
Parncutt (1988) Root ambiguity Symbolic incon (parn88)
Parncutt and Strasburger (1994) Complex sonorousness Symbolic incon (parn94)
Stolzenburg (2015) Smoothed relative periodicity Symbolic incon (stolz15)
Lartillot, Toiviainen, and Eerola (2008) Inharmonicity Audio MIRtoolbox
Interference
Bowling, Purves, and Gill (2018) Absolute frequency intervals Symbolic incon (bowl18)
Huron (1994) Aggregate dyadic consonance Symbolic incon
Hutchinson and Knopoff (1978) Dissonance Symbolic incon (dycon)
Parncutt and Strasburger (1994) Pure sonorousness Symbolic incon (parn94)
Sethares (1993) Dissonance Symbolic incon (dycon)
Vassilakis (2001) Roughness Symbolic incon (dycon)
Wang, Shen, Guo, Tang, and Hamade (2013) Roughness Symbolic incon (wang13)
Bogdanov et al. (2013) Dissonance Audio Essentia
Lartillot, Toiviainen, and Eerola (2008) Roughness (after Sethares) Audio MIRtoolbox
Lartillot, Toiviainen, and Eerola (2008) Roughness (after Vassilakis) Audio MIRtoolbox
Weisser and Lartillot (2013) Roughess (after Sethares) Audio MIRtoolbox
Culture
Johnson-Laird, Kang, and Leong (2012) Tonal dissonance Symbolic incon (jl12)
This paper Corpus dissonance Symbolic incon (corpdiss)
Note . “Reference” identifies the literature where the model or relevant software package was originally presented. “Original name” corresponds to the
name of the model (or corresponding psychological feature) in the reference literature. “Input” describes the input format for the model implementa tions
used in this paper. “Implementation” describes the software used for each model implementation, with “incon” referring to the incon package thataccompanies this paper, and “Essentia” and “MIRtoolbox” corresponding to the software presented in Bogdanov et al. (2013) andLartillot et al. (2008)
respectively. Terms in parentheses identify the low-level R packages that underpin the incon package, and that provide extended access to individua l
models.230 HARRISON AND PEARCE

## Page 16

A Composite Consonance Model
We constructed a linear regression model to test the hypothesis
that multiple psychological mechanisms contribute to consonanceperception. We fit this model to the Bowling et al. (2018)
dataset, using four features representing interference, periodic-ity/harmonicity, cultural familiarity, and number of notes. The first
three features corresponded to the three best-performing models inFigure 2A :Hutchinson and Knopoff’s (1978) roughness model,
Harrison and Pearce’s (2018) harmonicity model, and the new
cultural familiarity model. The fourth feature corresponded to thenumber of notes in the chord. All features were treated as contin-uous predictors.
The predictions of the resulting model are plotted in Figure 2B .
The predictions correlate rather well with the ground truth ( r/H11005
Wang et al. (2013, original)MIRtoolboxEssentiaMIRtoolbox (Vassilakis)Milne (2013)MIRtoolbox (Sethares, v2)Wang et al. (2013, new)Vassilakis (2001)Bowling et al. (2018)Parncutt & Strasburger (1994)Sethares (1993)MIRtoolbox (Sethares)Parncutt (1988)Johnson−Laird et al. (2012)Gill & Purves (2009)Parncutt & Strasburger (1994)Huron (1994)Stolzenburg (2015)This paperHarrison & Pearce (2018)Hutchinson & Knopoff (1978)
0.0 0.2 0.4 0.6 0.8
Partial correlation with consonance ratingsModelInput
Audio
Symbolic
Theory
InterferencePeriodicity/harmonicityCultureA r/g320.88
1234
1234
Predicted consonanceActual consonanceB
Number of notesCulturePeriodicity/harmonicityInterference
0.00 0.05 0.10 0.15 0.20
BetaPredictorC
Schwartz et al. (2003; 12 chords of size 2)Lahdelma & Eerola (2016; 15 chords of size 3−6)Exp 2. of Johnson−Laird et al.  (2012; 48 chords of size 4)Exp 1. of Johnson−Laird et al.  (2012; 55 chords of size 3)Bowling et al. (2018; 298 chords of size 2−4)
0.00 0.25 0.50 0.75 1.00
Correlation with consonance ratingsDatasetModel
Interference
Periodicity/harmonicity
Culture
CompositeComposite (without num. notes)D
Figure 2. Results of the perceptual analyses. All error bars denote 95% confidence intervals. (A) Partial
correlations between model outputs and average consonance ratings in the Bowling et al. (2018) dataset, after
controlling for number of notes. (B) Predictions of the composite model for the Bowling et al. (2018) dataset.
(C) Standardized regression coefficients for the composite model. (D) Evaluating the composite model acrossfive datasets from four studies ( Bowling et al., 2018 ;Johnson-Laird et al., 2012 ;Lahdelma & Eerola, 2016 ;
Schwartz et al., 2003 ). See the online article for the color version of this figure.231 SIMULTANEOUS CONSONANCE

## Page 17

.88, 95% CI [.85, .90]), significantly outperforming the individual
models in Figure 2A .
The resulting standardized regression coefficients are plotted in
Figure 2C , with signs equated for ease of comparison. All four
features contributed significantly and substantially to the model,each with broadly similar regression coefficients. As expected,interference was negatively related to consonance, whereas peri-odicity/harmonicity and cultural familiarity were positively relatedto consonance. Number of notes also contributed significantly,presumably reflecting participants recalibrating their responsescales for blocks with different numbers of notes.
This pattern of regression coefficients supports our proposition
that consonance is jointly determined by interference, periodicity/harmonicity, and cultural familiarity. Moreover, it implies that theeffect of cultural familiarity on consonance perception is not solelymediated by learned preferences for periodicity/harmonicity ( Mc-
Dermott et al., 2010 ,2016 ). However, the contribution of cultural
familiarity should be taken with caution: It might alternativelyreflect a noncultural contributor to consonance that is not capturedby our periodicity/harmonicity or interference models, but thatinfluences chord prevalences in music composition, and thereforecorrelates with our corpus-based cultural model. Future workcould test this possibility by modeling individual differences inconsonance perception as a function of the listener’s musicalbackground.
Generalizing to Different Datasets
A good predictive model of consonance should generalize out-
side the specific paradigm of Bowling et al. (2018) . We therefore
tested the new composite model on four additional datasets fromthe literature ( Johnson-Laird et al., 2012 ;Lahdelma & Eerola,
2016 ;Schwartz et al., 2003 ). These datasets are relatively small,
preventing model performance from being assessed with muchreliability; nonetheless, they provide a useful initial test of themodel’s generalizability. In each case, we assessed predictiveperformance by correlating model predictions with averaged con-sonance judgments for each stimulus, and benchmarked the com-posite model’s performance against that of its constituent submod-els. For datasets varying the number of notes in each chord, weevaluated the composite model twice: once in its original form, andonce removing the number of notes predictor, which we thoughtmight be a design-related artifact from Bowling et al. (2018) .
Johnson-Laird et al. (2012) provide two relevant datasets of
consonance judgments, one for three-note chords (Experiment 1,27 participants, 55 chords), and one for four-note chords (Exper-iment 2, 39 participants, 48 chords). Modeling these datasets, wefound a trend for the composite model to outperform the individualsubmodels ( Figure 2D ). This trend is less clear in the second
dataset, however, where interference performs particularly badlyand periodicity/harmonicity performs particularly well, almost ona par with the composite model.
17A possible explanation is the
fact that Johnson-Laird et al. (2012) purposefully undersampled
chords containing adjacent semitones, thereby restricting the vari-ation in interference.
Lahdelma and Eerola (2016) provide a dataset of consonance
judgments from 410 participants for 15 chords in various transpo-sitions, with the chords ranging in size from three to six notes. Astransposition information was missing from the published dataset,we averaged consonance judgments over transpositions before
computing the performance metrics. The composite model per-formed considerably worse ( r/H11005.63, 95% CI [.18, .87]) than the
submodels ( r/H11022.89). This implied that the number-of-notes pre-
dictor was sabotaging predictions, and indeed, removing this pre-dictor improved performance substantially ( r/H11005.97, 95% CI [.91,
.99]). This pattern of results is consistent with the hypothesis thatthe number of notes effect observed in the Bowling et al. (2018)
dataset was a design-related confound.
Schwartz et al. (2003) present data on the perceptual consonance
of two-note chords as compiled from seven historic studies ofconsonance perception. The composite model performs well here(r/H11005.87, 95% CI [.59, .96]), seemingly outperforming the sub-
models (.73 /H11021r/H11021.85), but the small dataset size limits the
statistical power of these comparisons.
In a subsequent exploratory analysis, we benchmarked the com-
posite model’s performance against the 10 best-performing modelsfrom Figure 2A . Model performance varied across datasets, and in
some cases individual models achieved higher correlation coeffi-cients than the composite model. However, no model significantlyoutperformed the composite model at a p/H11021.05 level in any given
dataset, even without correcting for multiple comparisons.
These evaluations provide qualified support for the composite
model’s generalizability across datasets. Predictive performance isgenerally good, with the composite model typically matching orimproving upon the performance of preexisting models. However,these inferences are constrained by the small dataset sizes ofprevious studies, which limit the precision of performance evalu-ations. A further limitation is that most previous studies do notmanipulate the number of notes in the chord, which makes itdifficult to test the generalizability of the number-of-notes effectobserved in the Bowling et al. (2018) dataset. These limitations
should be addressed in subsequent empirical work.
Recommendations for Model Selection
Figure 2A shows that consonance models representing similar
psychological theories can vary widely in performance. This high-lights the danger of testing psychological theories with singlecomputational models, especially when those models are relativelyunvalidated. For example, Lahdelma and Eerola (2016) found that
MIRtoolbox’s inharmonicity measure failed to predict consonancejudgments, and concluded that periodicity/harmonicity does notcontribute much to consonance. Our analyses replicate the lowpredictive power of MIRtoolbox’s inharmonicity measure (partialr/H11021.2), but they show that other periodicity/harmonicity measures
can predict consonance much better (partial r/H11022.7). If Lahdelma
and Eerola (2016) had selected a different periodicity/harmonicity
model, their conclusions might therefore have been very different.
Figure 2A provides useful information for model selection. All
else aside, models with higher predictive performance are likely tobe better instantiations of their respective psychological theories.Here we selected the three best-performing models in Figure 2A ,
which usefully represent three different consonance theories: in-terference, periodicity/harmonicity, and cultural familiarity. How-
17In conducting these analyses, we detected several apparent errors in
the roughness values reported by Johnson-Laird et al. (2012) . Here we use
roughness values as computed by our new incon package.232 HARRISON AND PEARCE

## Page 18

ever, several models reached similar levels of performance, and
should be retained as good candidates for consonance modeling.Stolzenburg’s (2015) model performed especially well on the
validation datasets, and should be considered a recommendedalternative to Harrison and Pearce’s (2018) periodicity/harmonic-
ity model. Likewise, if it is desirable for the model to be hand-computable, Huron’s (1994) model and Parncutt’s (1988) model
both perform remarkably well given their simplicity. When onlyaudio information is available, our results suggest that MIRtool-box’s roughness measure is the best candidate for estimatingconsonance. In contrast, none of the audio-based periodicity/har-monicity measures were able to predict consonance.
There are some applications, such as emotion research, music
information retrieval, or algorithmic music composition, where acomposite model of consonance may be more useful than modelsrepresenting individual consonance mechanisms. The compositemodel presented here would be well-suited for this role. However,the model would benefit from further tuning and validation, ideallyon datasets varying chord spacing, tone spectra, and the number ofnotes in the chord.
Corpus Analyses
We have argued that chord prevalences can provide a proxy for
a listener’s musical exposure, and therefore can be used to modelthe contribution of cultural familiarity to consonance perception.However, these chord prevalences may themselves be partly de-termined by noncultural aspects of consonance perception, such asperiodicity/harmonicity and interference.
A recent study by Parncutt et al. (2018) addressed these poten-
tial predictors of chord prevalences. The authors compiled a corpusof vocal polyphonic music spanning seven centuries of Westernmusic, and correlated chord prevalences in this corpus with fourfeatures: interference, periodicity/harmonicity, diatonicity, andevenness. They predicted that interference and periodicity/harmo-nicity should respectively be negatively and positively related tochord prevalence, on account of these features’ respective contri-butions to perceptual consonance. They predicted that diatonicchords—chords played within the Western diatonic scale—shouldbe more common, because the familiarity of the diatonic scaleinduces consonance in Western listeners. They also predicted thatchord prevalences should be higher for chords whose notes areapproximately evenly spaced, because even spacing is associatedwith efficient voice leading ( Tymoczko, 2011 ).
Parncutt and colleagues tested these hypotheses by counting
occurrences of 19 different three-note chord types in their dataset.They compiled a selection of formal models for each feature, andcorrelated model outputs with chord counts in their musical cor-pus, splitting the analysis by different musical periods. The ob-served correlations were generally consistent with the authors’predictions, supporting the notion that perceptual consonance con-tributes to Western chord prevalences.
Although a useful contribution, this study has several important
limitations. First, restricting consideration to just 19 chord typesresults in very imprecise parameter estimates. For example, acorrelation coefficient of r/H11005.5 has a 95% confidence interval
ranging from .06 to .78; it is difficult to draw reliable inferencesfrom such information. Second, pairwise correlations are unsuit-able for quantifying causal effects when the outcome variablepotentially depends on multiple predictor variables. Third, pair-
wise correlations can only capture linear relationships, and there-fore cannot test more complex relationships between chord usageand consonance, such as the proposition that chord usage is biasedtoward intermediate levels of consonance ( Lahdelma & Eerola,
2016 ). Fourth, the consonance models are simple note-counting
models, which often lack specificity to the feature being analyzed.For example, interference is modeled using the dyadic consonancemodel of Huron (1994) , but this model is built on dyadic conso-
nance judgments which have recently been attributed to periodic-ity/harmonicity, not interference ( McDermott et al., 2010 ;Stolzen-
burg, 2015 ).
Here we address these limitations, analyzing chord occurrences
in three large corpora spanning the last thousand years of Westernmusic: a corpus of classical scores ( Viro, 2011 ), a corpus of jazz
lead sheets ( Broze & Shanahan, 2013 ), and a corpus of harmonic
transcriptions of popular songs ( Burgoyne, 2011 ). Instead of re-
stricting consideration to 19 chord types, we tabulated prevalencesfor all 2,048 possible pitch-class chord types (see the Methodsection for further details). Instead of pairwise correlations, weconstructed polynomial regression models capable of capturingnonlinear effects of multiple simultaneous predictors. Instead ofsimple note-counting models, we used the best-performing conso-nance models from Figure 2A: Hutchinson and Knopoff’s (1978)
interference model, and Harrison and Pearce’s (2018) periodicity/
harmonicity model.
We were particularly interested in how interference and period-
icity/harmonicity contributed to chord prevalence. However, wealso controlled for the number of notes in the chord, reasoning thatthis feature is likely to have constrained chord usage on account ofpractical constraints (e.g., the number of instruments in an ensem-ble).
Analyzing interference and periodicity/harmonicity allows us to
revisit recent claims that consonance is primarily determined byperiodicity/harmonicity and not interference ( Cousineau et al.,
2012 ;McDermott et al., 2010 ,2016 ). If consonance is indeed
predicted primarily by periodicity/harmonicity, we would expectperiodicity/harmonicity to be an important predictor of Westernchord prevalences, and that interference should have little predic-tive power after controlling for periodicity/harmonicity. Con-versely, if consonance derives from both interference and period-icity/harmonicity, then we might expect both features to contributeto chord prevalences.
Compiling chord prevalences requires a decision about how to
categorize chords into chord types. Here we represented eachchord as a pitch-class chord type , defined as a pitch-class set
expressed relative to the bass pitch class. This representationcaptures the perceptual principles of octave invariance (the chordtype is unchanged when chord pitches are transposed by octaves,as long as they do not move below the bass note) and transpositioninvariance (the chord type is unchanged when all the chord’spitches are transposed by the same interval).
Hutchinson and Knopoff’s model requires knowledge of precise
pitch heights, which are not available in pitch-class chord typerepresentations. We therefore assigned pitch heights to each chordtype by applying the automatic chord voicing algorithm of Harri-
son and Pearce (2019 ; see the Method section for details).
Chord type prevalences could be operationalized in various
ways. Ideally, one might sum the temporal duration of each chord233 SIMULTANEOUS CONSONANCE

## Page 19

type over all of its occurrences, perhaps weighting compositions
by their popularity to achieve the best representation of a givenmusical style. However, chord durations and composition popu-larity were not available for our classical and jazz datasets. Wetherefore operationalized chord type prevalences as the total num-ber of occurrences of each chord type, excluding immediate rep-etitions of the same chord (see the Method section).
We constructed three orthogonal polynomial regression models
predicting log-transformed chord counts from interference, peri-odicity/harmonicity, and number of notes. The classical, jazz, andpopular corpora contributed 2,048, 118, and 157 data points re-spectively, corresponding to the unique chord types observed ineach corpus and their respective counts. Each corpus was assignedits own polynomial order by minimizing the Bayesian InformationCriterion for the fitted model; the classical, jazz, and populardatasets were thereby assigned third-order, first-order, and second-order polynomials respectively.
Figure 3A quantifies each predictor’s importance using model
reliance (Fisher, Rudin, & Dominici, 2018 , see the Method section
for details). Across the three genres, interference was consistentlythe most important predictor, explaining c. 20% to 50% of thevariance in chord prevalences. Periodicity/harmonicity was also animportant predictor for classical music, but not for popular or jazzmusic. Number of notes predicted chord prevalences in all threegenres, explaining about half as much variance as interference.
Figure 3B plots the marginal effects of each predictor, showing
how feature values map to predictions. Interference had a clearnegative effect on chord prevalence in all three genres, consistentwith the notion that interference evokes dissonance, causing it tobe disliked by listeners and avoided by composers. Periodicity/harmonicity had a clear positive effect on chord prevalence in theclassical dataset, consistent with the idea that periodicity/harmo-nicity evokes consonance and is therefore promoted by composers(Figure 3B ). The effect of periodicity/harmonicity was less strong
in the popular and jazz datasets, taking the form of a weak positiveeffect in the popular dataset and a weak negative effect in the jazzdataset.
Figure 3C summarizes the predictive performances of the three
regression models. Generally speaking, predictive performanceswere high, indicating that consonance and number of notes to-gether explain a large part of Western chord prevalences. How-ever, the strength of this relationship varied by musical style, withthe classical dataset exhibiting the strongest relationship and thejazz dataset the weakest relationship.
In sum, these results weigh against the claim that consonance is
primarily determined by periodicity/harmonicity and not interfer-ence ( Bowling & Purves, 2015 ;Bowling et al., 2018 ;McDermott
et al., 2010 ). Across musical genres, interference seems to have a
strong and reliable negative effect on chord prevalences. Period-icity/harmonicity also seems to influence chord prevalences, but itseffect is generally less strong, and the nature of its contributionseems to vary across musical genres.
Discussion
Recent research argues that consonance perception is driven not
by interference but by periodicity/harmonicity, with cultural dif-ferences in consonance perception being driven by learned pref-erences for the latter ( Cousineau et al., 2012 ;McDermott et al.,2010 ,2016 ). We reassessed this claim by reviewing a wide range
of historic literature, modeling perceptual data from four previousempirical studies, and conducting corpus analyses spanning athousand years of Western music composition. We concluded thatinterference contributes significantly to consonance perception inWestern listeners, and that cultural aspects of consonance percep-tion extend past learned preferences for periodicity/harmonicity.Instead, consonance perception in Western listeners seems to bejointly determined by interference, periodicity/harmonicity percep-tion, and learned familiarity with particular musical sonorities.
This multicomponent account of consonance is broadly consis-
tent with several previous claims in the literature. Terhardt (1974 ,
1984 ) has emphasized the role of roughness and harmonicity in
determining consonance, and Parncutt and colleagues have arguedthat consonance depends on roughness, harmonicity, and familiar-ity (Parncutt & Hair, 2011 ;Parncutt et al., 2018 ). Scientific pref-
erences for parsimony may have caused these multicomponentaccounts to be neglected in favor of single-component accounts,but our analyses demonstrate the necessity of the multicomponentapproach.
This consolidation of multiple psychological mechanisms
makes an interesting parallel with historic pitch perception re-search, where researchers strove to demonstrate whether pitchperception was driven by place coding or temporal coding (see de
Cheveigné, 2005 for a review). It proved difficult to falsify either
place coding or temporal coding theories, and many researchersnow believe that both mechanisms play a role in pitch perception(e.g., Bendor, Osmanski, & Wang, 2012 ;Moore & Ernst, 2012 ).
Like most existing consonance research, our analyses were
limited to Western listeners and composers, and therefore we canonly claim to have characterized consonance in Westerners. Pre-vious research has identified significant cross-cultural variation inconsonance perception ( Florian, 1981 ;Maher, 1976 ;McDermott
et al., 2016 ); we suggest that this cross-cultural variation might be
approximated by varying the regression coefficients in our com-posite consonance model. For example, listeners familiar with beatdiaphony seem to perceive interference as consonant, not dissonant(Florian, 1981 ); this would be reflected in a reversed regression
coefficient for interference. While the regression coefficientsmight vary cross-culturally, it seems plausible that the model’sunderlying predictors—interference, periodicity/harmonicity,familiarity—might recur cross-culturally, given the cross-cultural
perceptual salience of these features ( McDermott et al., 2016 ).
Our conclusions are not inconsistent with vocal-similarity the-
ories of consonance perception ( Bowling & Purves, 2015 ;Bowling
et al., 2018 ;Schwartz et al., 2003 ). According to these theories,
certain chords sound consonant because they particularly resemblehuman vocalizations. These theories usually emphasize periodic-ity/harmonicity as a salient feature of human vocalizations, butthey could also implicate interference as a feature avoided intypical vocalizations ( Bowling et al., 2018 ) but used to convey
distress in screams ( Arnal, Flinker, Kleinschmidt, Giraud, & Poep-
pel, 2015 ). It seems plausible that these mechanisms contribute a
universal bias to perceive periodicity/harmonicity as pleasant andinterference as unpleasant. Nonetheless, these biases must be sub-tle enough to allow cultural variation, if we are to account formusical cultures that lack preferences for periodicity/harmonicity(McDermott et al., 2016 ) or that consider interference to be pleas-
ant ( Florian, 1981 ).234 HARRISON AND PEARCE

## Page 20

Our analyses were limited by the computational models tested.
It would be interesting to develop existing models further, perhapsproducing a version of Bowling et al.’s (2018) periodicity/harmo-
nicity model that accepts arbitrary tunings, or a version of Parncuttand Strasburger’s (1994) model without discrete-pitch approxima-
tions. It would also be interesting to test certain models notevaluated here, such as Boersma’s (1993) model and Vencovský’s
(2016) model.A
B
C
Figure 3. Results of the corpus analyses. (A) Feature importance as assessed by model reliance ( Fisher et al.,
2018 ), with error bars indicating 95% confidence intervals (bias-corrected and accelerated bootstrap, 100,000
replicates, DiCiccio & Efron, 1996 ). (B) Marginal effects of each feature, calculated using z-scores for feature
values and for chord frequencies. The shaded areas describe 95% confidence intervals, and distributions offeature observations are plotted at the bottom of each panel. Distributions for the “number of notes” feature aresmoothed to avoid overplotting. (C) Predicted and actual chord-type frequencies, alongside correspondingPearson correlation coefficients. See the online article for the color version of this figure.235 SIMULTANEOUS CONSONANCE

## Page 21

Our perceptual analyses were limited by the available empirical
data. Future work should expand these datasets, with particularemphasis on varying voicing, tone spectra, and number of notes inthe chord. Such datasets would be essential for testing the gener-alizability of our models.
Our perceptual analyses marginalized over participants, producing
an average consonance rating for each chord. This approach neglectsindividual differences, which can provide an important complemen-tary perspective on consonance perception ( McDermott et al., 2010 ).
When suitable empirical datasets become available, it would be in-teresting to investigate how the regression weights in Figure 2C vary
between participants.
Our corpus analyses presented very broad approximations to mu-
sical genres, aggregating over a variety of musical styles and timeperiods. It would be interesting to apply these methods to morespecific musical styles, or indeed to individual composers. It wouldalso be interesting to investigate the evolution of consonance treat-ment over time. As we analyze music compositions dating furtherback in history, we should expect the chord distributions to reflectconsonance perception in historic listeners rather than modern listen-ers. Such analyses could potentially shed light on how consonanceperception has changed over time ( Parncutt et al., 2018 ).
Our three corpora were constructed in somewhat different ways.
The classical corpus was derived from published musical scores;the jazz corpus constitutes a collection of lead sheets; the popularcorpus comprises expert transcriptions of audio recordings. Thisheterogeneity is both an advantage, in that it tests the generaliz-ability of our findings to different transcription techniques, and adisadvantage, in that it reduces the validity of cross-genre com-parisons. Future work could benefit from corpora with both sty-listic diversity and consistent construction.
We hope that our work will facilitate future psychological
research into consonance. Our incon package makes it easy to testdiverse consonance models on new datasets, and it can be easilyextended to add new models. Our inconData package compiles theperceptual datasets analyzed here, making it easy to test newconsonance models on a variety of perceptual data.
This work should also have useful applications in computational
musicology and music information retrieval. Our composite con-sonance model provides a principled way to operationalize the netconsonance of a musical chord, while our model evaluationsprovide a principled way to operationalize individual consonancetheories. Our software provides a consistent and easy-to-use inter-face to these models, facilitating their application to new datasets.
Method
Models
The models evaluated in this paper are available from three
software sources: the incon package, MIRtoolbox,18and Essen-
tia.19Unless otherwise mentioned, all incon models represent
unaltered versions of their original algorithms as described in thecited literature, with the exception that all idealized harmonicspectra comprised exactly 11 harmonics (including the fundamen-tal frequency), with the ith harmonic having an amplitude of i
/H110021,
and assuming incoherence between tones for the purpose of am-
plitude summation. We clarify some further details below.Harrison and Pearce (2018) ;Milne (2013) .These algo-
rithms have three free parameters: the number of harmonics mod-eled in each complex tone, the harmonic roll-off rate ( /H9267), and the
standard deviation of the Gaussian smoothing distribution ( /H9268). We
set the number of harmonics to 11 (including the fundamentalfrequency), and set the other two parameters to the optimizedvalues in Milne and Holland (2016) : a roll-off of /H9267/H11005 0.75, and a
standard deviation of /H9268/H11005 6.83 cents.
Hutchinson and Knopoff (1978) .Our implementation is
based on Mashinter (2006) , whose description includes a paramet-
ric approximation for the relationship between interval size andpure-dyad dissonance (see also Bigand et al., 1996 ).
Sethares (1993) .Our implementation is primarily based on
Sethares (1993) , but we include a modification suggested in later
work ( Sethares, 2005 ;Weisser & Lartillot, 2013 ) where pure-dyad
consonance is weighted by the minimum amplitude of each pair ofpartials, not the product of their amplitudes.
Wang et al. (2013) .Our implementation of Wang et al.’s
(2013) algorithm takes symbolic input and expresses each input
tone as an idealized harmonic series. Time-domain analyses areconducted with a signal length o f 1 s and a sample rate of 44,000.
Frequency-domain analyses are conducted in the range 1–44,000Hz with a resolution of 1 Hz. An interactive demonstration of thealgorithm is available at http://shiny.pmcharrison.com/wang13 .
Essentia: Interference. We used Version 2.1 of Essentia. We
analyzed each audio file using the “essentia_streaming_extractor_music” feature extractor, and retained the mean estimated disso-nance for each file.
MIRtoolbox: Interference. We used Version 1.6.1 of MIR-
toolbox, and computed roughness using the “mirroughness” func-tion. The function was applied to a single window spanning theentire length of the stimulus.
We evaluated this model in several configurations (see Figure
2A):
1. “Sethares” denotes the default model configuration,
which implements the dissonance model of Sethares
(2005) , but with pure-tone dyad contributions being
weighted by the product of their amplitudes (see
Sethares, 1993 );
2. “Sethares, v2” denotes the “Min” option in MIRtoolbox,
where pure-tone dyad contributions are weighted by theminimum of their amplitudes, after Weisser and Lartillot
(2013) (see also Sethares, 2005 );
3. “Vassilakis” denotes MIRtoolbox’s implementation of
Vassilakis’s (2001) model.
Johnson-Laird et al. (2012) .Johnson-Laird et al.’s (2012)
algorithm may be separated into a cultural and an interferencecomponent, with the latter corresponding to Hutchinson and Knop-
off’s (1978) model. The cultural model assigns each chord to a
consonance category, where categories are ordered from consonantto dissonant, and chords within a category are considered to beequally consonant. In our implementation, these consonance cat-
18https://www.jyu.fi/hytk/fi/laitokset/mutku/en/research/materials/mirtoolbox .
19https://essentia.upf.edu .236 HARRISON AND PEARCE

## Page 22

egories are mapped to positive integers, such that higher integers
correspond to greater dissonance. These integers constitute thealgorithm’s outputs.
Corpus-based model of cultural familiarity. This model
estimates a listener’s unfamiliarity with a given chord type from itsrarity in a musical corpus. Here we use the Billboard dataset(Burgoyne, 2011 ), a corpus of popular songs sampled from the
Billboard magazine’s “Hot 100” chart in the period 1958–1991.This corpus is used as a first approximation to an average Westernlistener’s prior musical exposure. We represent each chord in thiscorpus as a pitch-class chord type , defined as the chord’s pitch-
class set expressed relative to the chord’s bass note. For example,a chord with MIDI note numbers {66, 69, 74} has a pitch-classchord type of {0, 3, 8}. We count how many times each of the2,048 possible pitch-class chord types occurs in the corpus, andadd 1 to the final count. Unfamiliarity is then estimated as thenegative natural logarithm of the chord type’s count.
Composite model. The composite model’s unstandardized re-
gression coefficients are provided to full precision in Table 3 .
Consonance is estimated by computing the four features listed inTable 3 , multiplying them by their respective coefficients, and
adding them to the intercept coefficient. Number of notes corre-sponds to the number of distinct pitch classes in the chord; inter-ference is computed using Hutchinson and Knopoff’s (1978) mod-
el; periodicity/harmonicity is computed using Harrison and
Pearce’s (2018) model; culture corresponds to the new corpus-
based cultural model.
It is unclear whether the effect of number of notes generalizes
outside the dataset of Bowling et al. (2018) (see the Perceptual
Analyses section). We therefore recommend setting the number ofnotes coefficient to zero when applying the model to new datasets.
Software
We release two top-level R packages along with this paper. The
first, incon, implements the symbolic consonance models evalu-ated in this paper (see Table 2 ).
20The second, inconData, compiles
the perceptual datasets that we analyzed.21Tutorials are available
alongside these packages.
The incon package depends on several low-level R packages that
we also release along with this paper, namely bowl18 ,corpdiss ,
dycon ,har18 ,hcorp ,hrep,jl12,parn88 ,parn94 ,stolz15 , and
wang13 . These packages provide detailed interfaces to individualconsonance models and tools for manipulating harmony representa-
tions.
Our software, analyses, and article were all created using the
programming language R ( R Core Team, 2017 ), and benefited in
particular from the following open-source packages: bookdown ,boot,
checkmate ,cocor ,cowplot ,dplyr ,ggplot2 ,glue,gtools ,hht,knitr,
jsonlite ,magrittr ,margins ,memoise ,numbers ,papaja ,phonTools ,
plyr,purrr ,Rdpack ,readr ,rmarkdown ,testthat ,tibble ,tidyr,usethis ,
withr , and zeallot . Our analysis code is freely available online.22
Perceptual Datasets
The following datasets are all included in our inconData Pack-
age.
Bowling et al. (2018) .This study collected consonance judg-
ments for all possible 12 two-note chord types, 66 three-note chordtypes, and 220 four-note chord types that can be formed from theWestern chromatic scale within a one-octave span of the bassnote.
23An advantage of this dataset is its systematic exploration of
the chromatic scale; a disadvantage is its restricted range of voic-ings.
Each chord tone was pitched as a just-tuned interval from the
bass note.
24This approach was presumably chosen because Bowl-
ing et al.’s (2018) periodicity/harmonicity model requires just
tuning, but it should be noted that just tuning itself is not com-monly adopted in Western music performance (e.g., Karrick, 1998 ;
Kopiez, 2003 ;Loosen, 1993 ). It should also be noted that tuning a
chord in this way does not ensure that the intervals betweennonbass notes are just-tuned, and certain chords can sound unusu-ally dissonant as a result compared with their equal-temperedequivalents.
Each chord type was assigned a bass note such that the chord’s
mean fundamental frequency would be equal to middle C, approx-imately 262 Hz. The resulting chords were played using the“Bosendorfer Studio Model” synthesized piano in the softwarepackage “Logic Pro 9.”
The participant group numbered 30 individuals. Of these, 15
were students at a Singapore music conservatory, each havingtaken weekly formal lessons in Western tonal music for an averageof 13 years ( SD/H110053.8). The remaining 15 participants were
recruited from the University of Vienna, and averaged less than ayear of weekly music lessons prior to the study ( SD/H110051.1).
Participants were played single chords, and asked to rate con-
sonance on a 4-point scale, where consonance was defined as “themusical pleasantness or attractiveness of a sound.” Participantswere free to listen to the same chord multiple times before givinga rating. Stimulus presentation was blocked by the number of notesin each chord, with stimulus presentation randomized withinblocks. This presents an unfortunate potential confound; if conso-
20https://github.com/pmcharrison/incon .
21https://github.com/pmcharrison/inconData .
22See https://github.com/pmcharrison/inconPaper for top-level source
code.
23As before, a chord type represents a chord as a set of intervals above
an unspecified bass note.
24Just tuning means expressing pitch intervals as small-integer fre-
quency ratios. In Bowling et al. (2018) , the eleven intervals in the octave
were expressed as the following frequency ratios: 16:15, 9:8, 6:5, 5:4, 4:3,7:5, 3:2, 8:5, 5:3, 9:5, 15:8, and 2:1.Table 3
Unstandardized Regression Coefficients for the CompositeConsonance Model
Term Coefficient
Intercept 0.628434666589357
Number of notes 0.422267698605598Interference /H110021.62001025973261
Periodicity/harmonicity 1.77992362857478Culture /H110020.0892234643584134
Note . These regression coefficients are presented to full precision for
the sake of exact reproducibility, but it would also be reasonable toround the coefficients to c. 3 significant figures. When generalizingoutside the dataset of Bowling et al. (2018) , we recommend setting the
number of notes coefficient to zero.237 SIMULTANEOUS CONSONANCE

## Page 23

nance differed systematically across chords containing different
numbers of notes, this may have caused participants to recalibratetheir scale usage across blocks.
Johnson-Laird et al. (2012) , Experiment 1. This experiment
collected consonance ratings for all 55 possible three-note pitch-
class chord types , where a pitch-class chord type is defined as a
chord’s pitch-class set expressed relative to the bass pitch class.These chords were voiced so that each chord spanned approxi-mately 1.5 octaves. All chords were played with synthesized pianousing the “Sibelius” software package.
The participant group numbered 27 individuals from the Prince-
ton University community. Some were nonmusicians, some weremusicians, but all were familiar with Western music.
Participants were played single chords, and asked to rate disso-
nance on a seven-point scale, where dissonance was defined as“unpleasantness.” Each chord was only played once, with presen-tation order randomized across participants.
Johnson-Laird et al. (2012) , Experiment 2. This experiment
collected consonance ratings for 43 four-note pitch-class chordtypes. The rationale for chord selection is detailed in Johnson-
Laird et al. (2012) ; particularly relevant is the decision to under-
sample chords containing three adjacent semitones, which mayhave mitigated contributions of interference to their results.
The participant group numbered 39 individuals from the Prince-
ton University community. All other aspects of the design wereequivalent to Experiment 1.
Lahdelma and Eerola (2016) .This experiment collected
consonance ratings for 15 different pitch chord types , where a
pitch chord type is defined as a chord’s pitch set expressed relativeto its bass pitch. These chords ranged in size from three to sixnotes. The full rationale for chord selection is detailed in Lahdelma
and Eerola (2016) , but the main principle was to select chords with
high consonance according to Huron’s (1994) dyadic consonance
model, and with varying levels of cultural familiarity according toTymoczko (2011) . Because Huron’s model primarily captures
interference (see the Computational Models section), this approachis likely to minimize between-stimulus variation in interference,potentially reducing the predictive power of interference modelswithin this dataset. All chords were played using the synthesized“Steinway D Concert Grand” piano in the software package “Able-ton Live 9” with the “Synthogy Ivory Grand Pianos II” plug-in.
The participant group was tested online, and numbered 418
individuals after quality-checking. These participants represented42 different nationalities, with 91.7% coming from Europe and theAmericas.
Each participant was played 30 stimuli comprising the 15 chord
types each at a “low” and a “high” transposition, with the precisetranspositions of these chord types randomly varying within anoctave for each transposition category. Unfortunately, precisetransposition information seems not to be preserved in the pub-lished response data. For the purpose of estimating interference,we therefore represented each chord type with a bass note of G4 (c.392 Hz), corresponding to the middle of the range of bass notesused in the original study.
Participants were instructed to rate each chord on five 5-point
scales; here we restrict consideration to the “consonance” scale.Curiously, “consonance” was defined as “How smooth do youthink the chord is,” with the scale’s extremes being termed “rough”and “smooth.” This definition resembles more a definition ofroughness than consonance, a potential problem for interpreting
the study’s results.
Schwartz et al. (2003) .This dataset provides consonance
ratings for the 12 two-note chord types in the octave, aggregatedover seven historic studies. Each study produced a rank ordering ofthese two-note chords; these rank orderings were then summarizedby taking the median rank for each chord.
Musical Corpora
Classical scores. The classical dataset was derived from the
Peachnote music corpus ( Viro, 2011 ).25This corpus compiles
more than 100,000 scores from the Petrucci Music Library(IMSLP, http://imslp.org ), spanning several hundred years of
Western art music (1198–2011). Each score was digitized usingoptical music recognition software. In the resulting dataset,each datum represents a distinct “vertical slice” of the score,with new slices occurring at new note onsets, and includingsustained notes sounded at previous onsets. We preprocessedthis dataset to a pitch-class chord-type representation, whereeach chord is represented as a pitch-class set expressed relativeto its bass pitch class. The resulting dataset numbered128,357,118 chords.
Jazz lead sheets. The jazz dataset was derived from the iRb
corpus ( Broze & Shanahan, 2013 ). The iRb corpus numbers 1,186
lead sheets for jazz compositions, where each lead sheet specifiesthe underlying chord sequence for a given composition. These leadsheets were compiled from an online forum for jazz musicians. Inthe original dataset, chords are represented as textual tokens, suchas “C7b9”; we translated all such tokens into a prototypical pitch-class chord-type representation, such as {0, 1, 4, 7, 10}. Thisprocess misses the improvisatory chord alterations that typicallyhappen during jazz performances, but nonetheless should providea reasonable first approximation to the performed music. Chordcounts were only incremented on chord changes, not chord repe-titions; section repeats were omitted. The resulting dataset num-bered 42,822 chords.
Popular transcriptions. The popular dataset was derived
from the McGill Billboard corpus ( Burgoyne, 2011 ), which
comprised chord sequences for 739 unique songs as transcribedby expert musicians. As with the iRb dataset, we translated allchord tokens into prototypical pitch-class chord-type represen-tations, omitting section repeats, and only incrementing chordcounts on each chord change. The resulting dataset numbered74,093 chords.
Corpus Analyses
We transformed each of our corpora to pitch-class chord type
representations, where each chord is represented as a pitch-classset relative to the chord’s bass note. We then counted occurrencesof pitch-class chord types in our three corpora.
For the purpose of applying Hutchinson and Knopoff’s (1978)
interference model, we assigned pitch heights to each chord typeusing the automatic chord voicing algorithm of Harrison and
Pearce (2019) . This model was originally designed for voicing
25In particular, we downloaded the “Exact 1-gram chord progressions”
file from http://www.peachnote.com/datasets.html on July 2nd, 2018.238 HARRISON AND PEARCE

## Page 24

chord sequences, but it can also be applied to individual chords. Its
purpose is to find an idiomatic assignment of pitch heights to pitchclasses that reflects the kind of psychoacoustic considerationsimplicitly followed by traditional Western composers (e.g., Huron,
2001 ). As applied here, the model minimized the following linear
combination of features:
8.653/H11003interference
/H110011.321/H11003|5/H11002number of notes |
/H110010.128/H11003|6 0/H11002mean pitch height |(2)
where “interference” refers to the raw output of Hutchinson and
Knopoff’s model, “number of notes” refers to the number ofunique pitches in the chord voicing, and “mean pitch height”corresponds to the mean of the chord’s pitches as expressed inMIDI note numbers.
26In other words, the model minimized the
chord’s interference while preferring chords containing (closeto) five discrete pitches with a mean pitch height close tomiddle C (c. 262 Hz). These model parameters correspond tothe optimal parameters that Harrison and Pearce (2019) derived
from a dataset of 370 chorale harmonizations by J. S. Bach, butwith the target number of notes changed from four to five.Chord voicings were restricted to the two octaves surroundingmiddle C, and were permitted to contain no more than five notesor the number of pitch classes in the chord type, whichever wasgreater.
We used polynomial regression to capture nonlinear relation-
ships between chord features and chord prevalences. We usedorthogonal polynomials, as computed by the R function “poly,”to avoid numerical instability, and we used the R package“margins” to compute marginal predictions for the resultingmodels.
Standardized regression coefficients become harder to inter-
pret as the polynomial degree increases. We instead assessedfeature importance using model reliance (Fisher et al., 2018 ), a
permutation-based metric commonly used for assessing featureimportance in random forest models ( Breiman, 2001 ). Model
reliance may calculated by computing two values: the model’soriginal predictive accuracy, and the model’s predictive accuracyafter randomly permuting the feature of interest (without refittingthe model). Model reliance is then defined as the difference inthese accuracies: The greater the difference, the more the modelrelies on the feature of interest. Here we used R
2as the perfor -
mance metric, and computed confidence intervals for our modelreliance estimates using bias-corrected accelerated bootstrappingwith 100,000 replicates ( DiCiccio & Efron, 1996 ).
26A frequency of fHz corresponds to a MIDI note number of
69/H1100112log2(f/440).
References
Ambrazevic ˇius, R. (2017). Dissonance/roughness and tonality perception
in Lithuanian traditional Schwebungsdiaphonie. Journal of Interdisci-
plinary Music Studies, 8, 39–53. http://dx.doi.org/10.4407/jims.2016.12
.002
Arnal, L. H., Flinker, A., Kleinschmidt, A., Giraud, A. L., & Poeppel, D.
(2015). Human screams occupy a privileged niche in the communicationsoundscape. Current Biology, 25, 2051–2056. http://dx.doi.org/10.1016/
j.cub.2015.06.043Arthurs, Y., Beeston, A. V., & Timmers, R. (2018). Perception of isolated
chords: Examining frequency of occurrence, instrumental timbre, acous-tic descriptors and musical training. Psychology of Music, 46, 662–681.
http://dx.doi.org/10.1177/0305735617720834
Aures, W. (1984). Berechnungsverfahren für den Wohlklang beliebiger
Schallsignale, ein Beitrag zur gehörbezogenen Schallanalyse [A proce-
dure for calculating the consonance of any sound, a contribution toauditory sound analysis] (PhD thesis). Technical University of Munich,Germany.
Aures, W. (1985a). Berechnungsverfahren für den sensorichen Wohlklang
beliebiger Schallsignale [A procedure for calculating the sensory con-sonance of any sound]. Acustica, 59, 130–141.
Aures, W. (1985b). Der sensorische Wohlklang als Funktion psychoakus-
tischer Empfindungsgrößen [Sensory consonance as a function of psy-choacoustic parameters]. Acta Acustica United with Acustica, 58, 282–
290.
Aures, W. (1985c). Ein Berechnungsverfahren der Rauhigkeit [A proce-
dure for calculating roughness]. Acustica, 58, 268–281.
Ayotte, J., Peretz, I., & Hyde, K. (2002). Congenital amusia: A group study
of adults afflicted with a music-specific disorder. Brain, 125, 238–251.
http://dx.doi.org/10.1093/brain/awf028
Balaguer-Ballester, E., Denham, S. L., & Meddis, R. (2008). A cascade
autocorrelation model of pitch perception. The Journal of the Acoustical
Society of America, 124, 2186–2195. http://dx.doi.org/10.1121/1
.2967829
Bendor, D., Osmanski, M. S., & Wang, X. (2012). Dual-pitch processing
mechanisms in primate auditory cortex. Journal of Neuroscience, 32,
16149–16161. http://dx.doi.org/10.1523/jneurosci.2563-12.2012
Bernstein, J. G. W., & Oxenham, A. J. (2005). An autocorrelation model
with place dependence to account for the effect of harmonic number onfundamental frequency discrimination. The Journal of the Acoustical
Society of America, 117, 3816–3831. http://dx.doi.org/10.1121/1
.1904268
Bidelman, G. M., & Heinz, M. G. (2011). Auditory-nerve responses predict
pitch attributes related to musical consonance-dissonance for normal andimpaired hearing. The Journal of the Acoustical Society of America, 130,
1488–1502. http://dx.doi.org/10.1121/1.3605559
Bidelman, G. M., & Krishnan, A. (2009). Neural correlates of consonance,
dissonance, and the hierarchy of musical pitch in the human brainstem.Journal of Neuroscience, 29, 13165–13171. http://dx.doi.org/10.1523/
JNEUROSCI.3900-09.2009
Bigand, E., Parncutt, R., & Lerdahl, F. (1996). Perception of musical
tension in short chord sequences: The influence of harmonic function,sensory dissonance, horizontal motion, and musical training. Perception
& Psychophysics, 58, 124–141. http://dx.doi.org/10.3758/BF032
05482
Bilsen, F. A. (1977). Pitch of noise signals: Evidence for a “central
spectrum.” The Journal of the Acoustical Society of America, 61, 150–
161. http://dx.doi.org/10.1121/1.381276
Boersma, P. (1993). Accurate short-term analysis of the fundamental
frequency and the harmonics-to-noise ratio of a sampled sound. Pro-
ceedings of the Institute of Phonetic Sciences, 17, 97–110.
Bogdanov, D., Wack, N., Gómez, E., Gulati, S., Herrera, P., Mayor, O. ,...
Serra, X. (2013). Essentia: An audio analysis library for music infor-
mation retrieval . In 14th International Society for Music Information
Retrieval Conference (ISMIR 2013), Curitiba, Brazil.
Boomsliter, P., & Creel, W. (1961). The long pattern hypothesis in har-
mony and hearing. Journal of Music Theory, 5, 2–31.
Borchgrevink, H. (1975). Musical consonance preference in man eluci-
dated by animal experiments (Norwegian). Tidsskrift for Den Norske
Laegeforening, 95, 356–358.
Bowling, D. L., & Purves, D. (2015). A biological rationale for musical
consonance. Proceedings of the National Academy of Sciences of the239 SIMULTANEOUS CONSONANCE

## Page 25

United States of America, 112, 11155–11160. http://dx.doi.org/10.1073/
pnas.1505768112
Bowling, D. L., Purves, D., & Gill, K. Z. (2018). Vocal similarity predicts
the relative attraction of musical chords. Proceedings of the National
Academy of Sciences of the United States of America, 115, 216–221.
http://dx.doi.org/10.1073/pnas.1713206115
Breiman, L. (2001). Random forests. Machine Learning, 45, 5–32.
Brooks, D. I., & Cook, R. G. (2010). Chord discrimination by pigeons.
Music Perception, 27, 183–196. http://dx.doi.org/10.1525/mp.2010.27.3
.183
Broze, Y., & Shanahan, D. (2013). Diachronic changes in jazz harmony: A
cognitive perspective. Music Perception, 31, 32–45. http://dx.doi.org/
10.1525/rep.2008.104.1.92
Burgoyne, J. A. (2011). Stochastic processes & database-driven musicol-
ogy(PhD thesis). McGill University, Montréal, Québec, Canada.
Butler, J. W., & Daston, P. G. (1968). Musical consonance as musical
preference: A cross-cultural study. The Journal of General Psychology,
79,129–142.
Buus, S. (1997). Auditory masking. In M. J. Crocker (Ed.), Encyclopedia
of acoustics (Vol. 3, pp. 1427–1445). Hoboken, NJ: Wiley. http://dx.doi
.org/10.1002/9780470172537.ch115
Cariani, P. A. (1999). Temporal coding of periodicity pitch in the auditory
system: An overview. Neural Plasticity, 6, 147–172.
Cariani, P. A., & Delgutte, B. (1996). Neural correlates of the pitch of
complex tones. I. Pitch and pitch salience. Journal of Neurophysiology,
76,1698–1716.
Chiandetti, C., & Vallortigara, G. (2011). Chicks like consonant music.
Psychological Science, 22, 1270–1273. http://dx.doi.org/10.1177/095
6797611418244
Cohen, M. A., Grossberg, S., & Wyse, L. L. (1995). A spectral network
model of pitch perception. The Journal of the Acoustical Society of
America, 98, 862–879. http://dx.doi.org/10.1121/1.413512
Cook, N. D. (2009). Harmony perception: Harmoniousness is more than
the sum of interval consonance. Music Perception, 27, 25–41. http://dx
.doi.org/10.1525/MP.2009.27.1.25
Cook, N. D. (2017). Calculation of the acoustical properties of triadic
harmonies. Journal of the Acoustical Society of America, 142, 3748–
3755. http://dx.doi.org/10.1121/1.5018342
Cook, N. D., & Fujisawa, T. (2006). The psychophysics of harmony
perception: Harmony is a three-tone phenomenon. Empirical Musicol-
ogy Review, 1, 106–126.
Cousineau, M., McDermott, J. H., & Peretz, I. (2012). The basis of musical
consonance as revealed by congenital amusia. Proceedings of the Na-
tional Academy of Sciences of the United States of America, 109,19858–19863. http://dx.doi.org/10.1073/pnas.1207989109
Cramer, E. M., & Huggins, W. H. (1958). Creation of pitch through
binaural interaction. The Journal of the Acoustical Society of America,
30,413–417. http://dx.doi.org/10.1121/1.1909628
Crespo-Bojorque, P., & Toro, J. M. (2015). The use of interval ratios in
consonance perception by rats ( Rattus norvegicus ) and humans ( Homo
sapiens ).Journal of Comparative Psychology, 129, 42–51. http://dx.doi
.org/10.1037/a0037991
Crowder, R. G., Reznick, J. S., & Rosenkrantz, S. L. (1991). Perception of
the major/minor distinction: V. Preferences among infants. Bulletin of
the Psychonomic Society, 29, 187–188. http://dx.doi.org/10.3758/
BF03335230
Dahlhaus, C. (1990). Studies on the origin of harmonic tonality . Princeton,
NJ: Princeton University Press.
Daniel, P., & Weber, R. (1997). Psychoacoustical roughness: Implemen-
tation of an optimized model. Acta Acustica United with Acustica, 83,
113–123.
de Cheveigné, A. (1998). Cancellation model of pitch perception. The
Journal of the Acoustical Society of America, 103, 1261–1271. http://
dx.doi.org/10.1121/1.423232de Cheveigné, A. (2005). Pitch perception models. In C. J. Plack & A. J.
Oxenham (Eds.), Pitch: Neural coding and perception (pp. 169–233).
New York, NY: Springer. http://dx.doi.org/10.1007/0-387-28958-5_6
DeWitt, L. A., & Crowder, R. G. (1987). Tonal fusion of consonant
musical intervals: The oomph in Stumpf. Perception and Psychophysics,
41,73–84.
DiCiccio, T. J., & Efron, B. (1996). Bootstrap confidence intervals. Sta-
tistical Science, 11, 189–212.
Diedenhofen, B., & Musch, J. (2015). cocor: A comprehensive solution for
the statistical comparison of correlations. PLoS ONE, 10, 4.http://dx
.doi.org/10.1371/journal.pone.0121945
Dillon, G. (2013). Calculating the dissonance of a chord according to
Helmholtz. European Physical Journal Plus, 128, 90.http://dx.doi.org/
10.1140/epjp/i2013-13090-4
Di Stefano, N., Focaroli, V., Giuliani, A., Formica, D., Taffoni, F., &
Keller, F. (2017). A new research method to test auditory preferences inyoung listeners: Results from a consonance versus dissonance percep-
tion study. Psychology of Music, 45, 699–712. http://dx.doi.org/10
.1177/0305735616681205
Duifhuis, H., Willems, L. F., & Sluyter, R. J. (1982). Measurement of pitch
in speech: An implementation of Goldstein’s theory of pitch perception.The Journal of the Acoustical Society of America, 71, 1568–1580.
http://dx.doi.org/10.1121/1.387811
Ebeling, M. (2008). Neuronal periodicity detection as a basis for the
perception of consonance: A mathematical model of tonal fusion. The
Journal of the Acoustical Society of America, 124, 2320–2329. http://
dx.doi.org/10.1121/1.2968688
Euler, L. (1739). Tentamen novae theoria musicae [An attempt at a new
theory of music]. Saint Petersburg, Russia: Academiae Scientiarum.
Fisher, A., Rudin, C., & Dominici, F. (2018). Model Class Reliance:
Variable importance measures for any machine learning model class,from the “Rashomon” perspective . Retrieved from https://arxiv.org/pdf/
1801.01489.pdf
Fletcher, H. (1924). The physical criterion for determining the pitch of a
musical tone. Physical Review, 23, 427–437. http://dx.doi.org/10.1103/
PhysRev.23.427
Florian, G. (1981). The two-part vocal style on Baluan Island Manus
Province, Papua New Guinea. Ethnomusicology, 25, 433–446.
Geary, J. M. (1980). Consonance and dissonance of pairs of inharmonic
sounds. The Journal of the Acoustical Society of America, 67, 1785–
1789. http://dx.doi.org/10.1121/1.384307
van de Geer, J. P., Levelt, W. J. M., & Plomp, R. (1962). The connotation
of musical consonance. Acta Psychologica, 20, 308–319. http://dx.doi
.org/10.1016/0001-6918(62)90028-8
Gill, K. Z., & Purves, D. (2009). A biological rationale for musical scales.
PLoS ONE, 4, 12.http://dx.doi.org/10.1371/journal.pone.0008144
Goldstein, J. L. (1973). An optimum processor theory for the central
formation of the pitch of complex tones.
The Journal of the Acoustical
Society of America, 54, 1496–1516. http://dx.doi.org/10.1121/1
.1914448
Grose, J. H., Buss, E., & Hall, J. W., III (2012). Binaural beat salience.
Hearing Research, 285, 40–45. http://dx.doi.org/10.1016/j.heares.2012
.01.012
Guernsey, M. (1928). The rôle of consonance and dissonance in music. The
American Journal of Psychology, 40, 173–204.
Härmä, A., & Palomäki, K. (1999). HUTear – a free Matlab toolbox for
modeling of human auditory system . Proceedings of the 1999 MATLAB
DSP Conference, Espoo, Finland. Retrieved from http://legacy.spa.aalto
.fi/software/HUTear/
Harrison, P. M. C., & Pearce, M. T. (2018). An energy-based generative
sequence model for testing sensory theories of Western harmony . Pro-
ceedings of the 19th International Society for Music Information Re-trieval Conference, Paris, France.240 HARRISON AND PEARCE

## Page 26

Harrison, P. M. C., & Pearce, M. T. (2019). A computational model for the
analysis and generation of chord voicings. PsyArXiv . Advance online
publication. http://dx.doi.org/10.31234/osf.io/wrgj7
Heffernan, B., & Longtin, A. (2009). Pulse-coupled neuron models as
investigative tools for musical consonance. Journal of Neuroscience
Methods, 183, 95–106. http://dx.doi.org/10.1016/j.jneumeth.2009.06
.041
Helmholtz, H. (1863). On the sensations of tone . New York, NY: Dover.
Hindemith, P. (1945). The craft of musical composition . New York, NY:
Associated Music Publishers.
Hoeschele, M., Cook, R. G., Guillette, L. M., Brooks, D. I., & Sturdy, C. B.
(2012). Black-capped chickadee (Poecile atricapillus) and human ( Homo
sapiens ) chord discrimination. Journal of Comparative Psychology, 126,
57–67. http://dx.doi.org/10.1037/a0024627
Houtsma, A. J. M., & Goldstein, J. L. (1972). The central origin of the pitch
of complex tones: Evidence from musical interval recognition. The
Journal of the Acoustical Society of America, 51, 520–529. http://dx.doi
.org/10.1121/1.1912873
Hulse, S. H., Bernard, D. J., & Braaten, R. F. (1995). Auditory discrimi-
nation of chord-based spectral structures by European starlings (Sturnusvulgaris). Journal of Experimental Psychology: General, 124, 409–423.
http://dx.doi.org/10.1037/0096-3445.124.4.409
Huron, D. (1991). Tonal consonance versus tonal fusion in polyphonic
sonorities. Music Perception, 9, 135–154.
Huron, D. (1994). Interval-class content in equally tempered pitch-class
sets: Common scales exhibit optimum tonal consonance. Music Percep-
tion, 11, 289–305. http://dx.doi.org/10.2307/40285624
Huron, D. (2001). Tone and voice: A derivation of the rules of voice-
leading from perceptual principles. Music Perception, 19, 1–64. http://
dx.doi.org/10.1525/mp.2001.19.1.1
Huron, D. (2002). A new theory of sensory dissonance: A role for perceived
numerosity . Presentation at the 7th International Conference for Music
Perception and Cognition (ICMPC-7), Sydney, Australia. Retrievedfrom https://csml.som.ohio-state.edu/Huron/Talks/Sydney.2002/Disson
ance/dissonance.abstract.html
Huron, D., & Sellmer, P. (1992). Critical bands and the spelling of vertical
sonorities. Music Perception, 10, 129–149.
Hutchinson, W., & Knopoff, L. (1978). The acoustic component of West-
ern consonance. Journal of New Music Research, 7, 1–29. http://dx.doi
.org/10.1080/09298217808570246
Hutchinson, W., & Knopoff, L. (1979). The significance of the acoustic
component of consonance in Western triads. Journal of Musicological
Research, 3, 5–22. http://dx.doi.org/10.1080/01411897908574504
Immerseel, L. V., & Martens, J. (1992). Pitch and voiced/unvoiced deter-
mination with an auditory model. The Journal of the Acoustical Society
of America, 91, 3511–3526.
Izumi, A. (2000). Japanese monkeys perceive sensory consonance of
chords. The Journal of the Acoustical Society of America, 108, 3073–
3078.
Johnson-Laird, P. N., Kang, O. E., & Leong, Y. C. (2012). On musical
dissonance. Music Perception, 30, 19–35.
Kaestner, G. (1909). Untersuchungen über den Gefühlseindruck unanalysi-
erter Zweiklänge [Investigation of the emotional impression of unana-lyzed dyads]. Psychologische Studien, 4, 473–504.
Kameoka, A., & Kuriyagawa, M. (1969a). Consonance theory part I:
Consonance of dyads. The Journal of the Acoustical Society of America,
45,
1451–1459. http://dx.doi.org/10.1121/1.1911623
Kameoka, A., & Kuriyagawa, M. (1969b). Consonance theory Part II:
Consonance of complex tones and its calculation method. The Journal of
the Acoustical Society of America, 45, 1460–1469. http://dx.doi.org/10
.1121/1.1911624
Karrick, B. (1998). An examination of the intonation tendencies of wind
instrumentalists based on their performance of selected harmonic musi-cal intervals. Journal of Research in Music Education, 46, 112–127.Koda, H., Nagumo, S., Basile, M., Olivier, M., Remeuf, K., Blois-Heulin,
C., & Lemasson, A. (2013). Validation of an auditory sensory reinforce-ment paradigm: Campbell’s monkeys (Cercopithecus campbelli) do notprefer consonant over dissonant sounds. Journal of Comparative Psy-
chology, 127, 265–271. http://dx.doi.org/10.1037/a0031237
Kopiez, R. (2003). Intonation of harmonic intervals: Adaptability of expert
musicians to equal temperament and just intonation. Music Perception,
20,383–410. http://dx.doi.org/10.1525/mp.2003.20.4.383
Krueger, F. (1910). Die Theorie der Konsonanz [The theory of conso-
nance]. Psychologische Studien, 5, 294–411.
Lahdelma, I., & Eerola, T. (2016). Mild dissonance preferred over conso-
nance in single chord perception. I-Perception .http://dx.doi.org/10
.1177/2041669516655812
Langner, G. (1997). Temporal processing of pitch in the auditory system.
Journal of New Music Research, 26, 116–132. http://dx.doi.org/10
.1080/09298219708570721
Lartillot, O., Toiviainen, P., & Eerola, T. (2008). A Matlab toolbox for
Music Information Retrieval. In C. Preisach, H. Burkhardt, L. Schmidt-Thieme, & R. Decker (Eds.), Data analysis, machine learning and
applications (pp. 261–268). Berlin, Germany: Springer.
Lee, K. M., Skoe, E., Kraus, N., & Ashley, R. (2015). Neural transforma-
tion of dissonant intervals in the auditory brainstem. Music Perception,
32,445–459. http://dx.doi.org/10.1525/MP.2015.32.5.445
Leman, M. (2000). Visualization and calculation of the roughness of
acoustical music signals using the Synchronization Index Model . Pro-
ceedings of the COSTG-6 Conference on Digital Audio Effects (DAFX-00), Verona, Italy.
Levelt, W. J. M., van de Geer, J. P., & Plomp, R. (1966). Triadic
comparisons of musical intervals. The British Journal of Mathematical
and Statistical Psychology, 19, 163–179.
Licklider, J. C. R. (1951). A duplex theory of pitch perception. Experientia,
7,128–134.
Loosen, F. (1993). Intonation of solo violin performance with reference to
equally tempered, Pythagorean, and just intonations. The Journal of the
Acoustical Society of America, 93, 525–539. http://dx.doi.org/10.1121/
1.405632
Lots, I. S., & Stone, L. (2008). Perception of musical consonance and
dissonance: An outcome of neural synchronization. Journal of the Royal
Society Interface, 5, 1429–1434. http://dx.doi.org/10.1098/rsif.2008
.0143
Lundin, R. W. (1947). Toward a cultural theory of consonance. The
Journal of Psychology, 23, 45–49. http://dx.doi.org/10.1080/00223980
.1947.9917318
Maher, T. F. (1976). “Need for resolution” ratings for harmonic musical
intervals: A comparison between Indians and Canadians. Journal of
Cross-Cultural Psychology, 7, 259–276.
Marin, M. M., Forde, W., Gingras, B., & Stewart, L. (2015). Affective
evaluation of simultaneous tone combinations in congenital amusia.Neuropsychologia, 78, 207–220. http://dx.doi.org/10.1016/j.neuropsy-
chologia.2015.10.004
Masataka, N. (2006). Preference for consonance over dissonance by hear-
ing newborns of deaf parents and of hearing parents. Developmental
Science, 9, 46–50. http://dx.doi.org/10.1111/j.1467-7687.2005.00462.x
Mashinter, K. (2006). Calculating sensory dissonance: Some discrepancies
arising from the models of Kameoka & Kuriyagawa, and Hutchinson &Knopoff. Empirical Musicology Review, 1, 65–84.
McDermott, J., & Hauser, M. (2004). Are consonant intervals music to
their ears? Spontaneous acoustic preferences in a nonhuman primate.Cognition, 94, B11–B21. http://dx.doi.org/10.1016/j.cognition.2004.04
.004
McDermott, J. H., Lehr, A. J., & Oxenham, A. J. (2010). Individual
differences reveal the basis of consonance. Current Biology, 20, 1035–
1041. http://dx.doi.org/10.1016/j.cub.2010.04.019241 SIMULTANEOUS CONSONANCE

## Page 27

McDermott, J. H., Schultz, A. F., Undurraga, E. A., & Godoy, R. A.
(2016). Indifference to dissonance in native Amazonians reveals culturalvariation in music perception. Nature, 535, 547–550. http://dx.doi.org/
10.1038/nature18635
McGowan, J. (2011). Psychoacoustic foundations of contextual harmonic
stability in jazz piano voicings. Journal of Jazz Studies, 7, 156–191.
McLachlan, N., Marco, D., Light, M., & Wilson, S. (2013). Consonance
and pitch. Journal of Experimental Psychology: General, 142, 1142–
1158. http://dx.doi.org/10.1037/a0030830
Meddis, R. (2011). MATLAB auditory periphery (MAP): Model technical
description . Retrieved from https://code.soundsoftware.ac.uk/projects/
map
Meddis, R., & Hewitt, M. J. (1991a). Virtual pitch and phase sensitivity of
a computer model of the auditory periphery. I: Pitch identification. The
Journal of the Acoustical Society of America, 89, 2866–2882. http://dx
.doi.org/10.1121/1.400725
Meddis, R., & Hewitt, M. J. (1991b). Virtual pitch and phase sensitivity of
a computer model of the auditory periphery. II: Phase sensitivity. The
Journal of the Acoustical Society of America, 89, 2883–2894. http://dx
.doi.org/10.1121/1.400726
Meddis, R., & O’Mard, L. (1997). A unitary model of pitch perception. The
Journal of the Acoustical Society of America, 102, 1811–1820. http://
dx.doi.org/10.1121/1.420088
Meyer, L. B. (1956). Emotion and meaning in music . Chicago, IL: The
University of Chicago Press.
Milne, A. J. (2013). A computational model of the cognition of tonality
(PhD thesis). The Open University, Milton Keynes, England.
Milne, A. J., & Holland, S. (2016). Empirically testing Tonnetz, voice-
leading, and spectral models of perceived triadic distance. Journal of
Mathematics and Music, 10, 59–85. http://dx.doi.org/10.1080/174
59737.2016.1152517
Milne, A. J., Laney, R., & Sharp, D. B. (2016). Testing a spectral model of
tonal affinity with microtonal melodies and inharmonic spectra. Musicae
Scientiae, 20, 465–494. http://dx.doi.org/10.1177/1029864915622682
Moore, B. C. J., & Ernst, S. M. A. (2012). Frequency difference limens at
high frequencies: Evidence for a transition from a temporal to a placecode. The Journal of the Acoustical Society of America, 132, 1542–1547.
http://dx.doi.org/10.1121/1.4739444
Nobili, R., Vetešník, A., Turicchia, L., & Mammano, F. (2003). Otoacous-
tic emissions from residual oscillations of the cochlear basilar membranein a human ear model. Journal of the Association for Research in
Otolaryngology, 4, 478–494.
Nordmark, J., & Fahlén, L. E. (1988). Beat theories of musical consonance.
STL-QPSR, 29, 111–122.
Olsen, K. N., Thompson, W. F., & Giblin, I. (2018). Listener expertise
enhances intelligibility of vocalizations in death metal music. Music
Perception, 35, 527–539. http://dx.doi.org/10.1525/MP.2018.35.5.527
Omigie, D., Dellacherie, D., & Samson, S. (2017). Effects of learning on
dissonance judgments. Journal of Interdisciplinary Music Studies, 8,
11–28. http://dx.doi.org/10.4407/jims.2016.12.001
Oxenham, A. J. (2018). How we hear: The perception and neural coding of
sound. Annual Review of Psychology, 69, 27–50. http://dx.doi.org/10
.1146/annurev-psych-122216-011635
Parncutt, R. (1988). Revision of Terhardt’s psychoacoustical model of the
root(s) of a musical chord. Music Perception, 6, 65–94.
Parncutt, R. (1989). Harmony: A psychoacoustical approach . Berlin, Ger-
many: Springer-Verlag.
Parncutt, R. (1993). Pitch properties of chords of octave-spaced tones.
Contemporary Music Review, 9, 35–50.
Parncutt, R. (2006a). Commentary on Cook & Fujisawa’s “The Psycho-
physics of Harmony Perception: Harmony is a Three-Tone Phenome-non.” Empirical Musicology Review, 1, 204–209.
Parncutt, R. (2006b). Commentary on Keith Mashinter’s “Calculating
sensory dissonance: Some discrepancies arising from the models ofKameoka & Kuriyagawa, and Hutchinson & Knopoff.” Empirical Mu-
sicology Review, 1, 201–203.
Parncutt, R., & Hair, G. (2011). Consonance and dissonance in music
theory and psychology: Disentangling dissonant dichotomies. Journal of
Interdisciplinary Music Studies, 5, 119–166. http://dx.doi.org/10.4407/
jims.2011.11.002
Parncutt, R., Reisinger, D., Fuchs, A., & Kaiser, F. (2018). Consonance
and prevalence of sonorities in Western polyphony: Roughness, harmo-nicity, familiarity, evenness, diatonicity. Journal of New Music Re-
search, 48, 1.http://dx.doi.org/10.1080/09298215.2018.1477804
Parncutt, R., & Strasburger, H. (1994). Applying psychoacoustics in com-
position: “Harmonic” progressions of “nonharmonic” sonorities. Per-
spectives of New Music, 32, 88–129.
Patterson, R. D. (1986). Spiral detection of periodicity and the spiral form
of musical scales. Psychology of Music, 14, 44–61. http://dx.doi.org/10
.1177/0305735686141004
Patterson, R. D., & Green, D. M. (2012). Auditory masking. In E. Cart-
erette (Ed.), Handbook of perception, volume IV: Hearing (pp. 337–
361). Amsterdam, the Netherlands: Elsevier.
Peeters, G., Giordano, B. L., Susini, P., Misdariis, N., Susini, P., &
McAdams, S. (2011). The Timbre Toolbox: Extracting audio descriptorsfrom musical signals. Journal of the Acoustical Society of America, 130,
2902–2916. http://dx.doi.org/10.1121/1.3642604
Perani, D., Cristina, M., Scifo, P., Spada, D., Andreolli, G., & Rovelli, R.
(2010). Functional specializations for music processing in the humannewborn brain. Proceedings of the National Academy of Sciences of the
United States of America, 107, 4758–4763. http://dx.doi.org/10.1073/
pnas.0909074107
Pierce, J. R. (1966). Attaining consonance in arbitrary scales. The Journal
of the Acoustical Society of America, 40, 249.
Plantinga, J., & Trehub, S. E. (2014). Revisiting the innate preference for
consonance. Journal of Experimental Psychology: Human Perception
and Performance, 40, 40–49. http://dx.doi.org/10.1037/a0033471
Plomp, R. (1965). Detectability threshold for combination tones. The
Journal of the Acoustical Society of America, 37, 1110–1123. http://dx
.doi.org/10.1121/1.1909532
Plomp, R., & Levelt, W. J. M. (1965). Tonal consonance and critical
bandwidth. The Journal of the Acoustical Society of America, 38, 548–
560. http://dx.doi.org/10.1121/1.1909741
Pressnitzer, D., & McAdams, S. (1999). Two phase effects in roughness
perception. Journal of the Acoustical Society of America, 105, 2773–
2782.
Rakowski, A. (1990). Intonation variants of musical intervals in isolation
and in musical contexts. Psychology of Music, 18, 60–72.
Rameau, J.-P. (1722). Treatise on harmony . Paris, France: Jean-Baptiste-
Christophe Ballard.
R Core Team. (2017). R: A language and environment for statistical
computing . Vienna, Austria: R Foundation for Statistical Computing.
Scharf, B. (1971). Fundamentals of auditory masking. Audiology, 10,
30–40.
Schellenberg, E. G., & Trehub, S. E. (1994). Frequency ratios and the
perception of tone patterns. Psychonomic Bulletin & Review, 1, 191–
201.
Schneider, A. (1997). “Verschmelzung,” tonal fusion, and consonance:
Carl Stumpf revisited. In M. Leman (Ed.), Music, gestalt, and comput-
ing: Studies in cognitive and systematic musicology (pp. 115–143).
Dordrecht, the Netherlands: Springer. http://dx.doi.org/10.1007/
BFb0034111
Schoenberg, A. (1978). Theory of harmony . Berkeley: University of Cal-
ifornia Press.
Schouten, J. F. (1938). The perception of subjective tones. Proceedings of
the Koninklijke Nederlandse Akademie van Wetenschappen, 41, 1086–
1093.242 HARRISON AND PEARCE

## Page 28

Schwartz, D. A., Howe, C. Q., & Purves, D. (2003). The statistical
structure of human speech sounds predicts musical universals. The
Journal of Neuroscience, 23, 7160–7168.
Sethares, W. A. (1993). Local consonance and the relationship between
timbre and scale. The Journal of the Acoustical Society of America, 94,
1218–1228.
Sethares, W. A. (2005). Tuning, timbre, spectrum, scale . London, UK:
Springer.
Shamma, S., & Klein, D. (2000). The case of the missing pitch templates:
How harmonic templates emerge in the early auditory system. The
Journal of the Acoustical Society of America, 107, 2631–2644. http://
dx.doi.org/10.1121/1.428649
Skovenborg, E., & Nielsen, S. H. (2002). Measuring sensory consonance
by auditory modelling. In Proceedings of the 5th International Confer-
ence on Digital Audio Effects (DAFX-02 ; pp. 251–256). Hamburg,
Germany.
Slaney, M., & Lyon, R. (1990). A perceptual pitch detector. In Interna-
tional conference on acoustics, speech, and signal processing (Vol. 1,
pp. 357–360). http://dx.doi.org/10.1109/ICASSP.1990.115684
Smoorenburg, G. F. (1972). Combination tones and their origin. The
Journal of the Acoustical Society of America, 52, 615–632. http://dx.doi
.org/10.1121/1.1913152
Sorge, G. A. (1747). Vorgemach der musicalischen Composition [Demon-
stration of music composition]. Lobenstein, Germany: Verlag des Au-toris.
Spagnolo, B., Ushakov, Y. V., & Dubkov, A. A. (2013). Harmony per-
ception and regularity of spike trains in a simple auditory model. AIP
Conference Proceedings (Vol. 1510, pp. 274–289). http://dx.doi.org/10
.1063/1.4776512
Stewart, L. (2011). Characterizing congenital amusia. Quarterly Journal of
Experimental Psychology, 64, 625–638. http://dx.doi.org/10.1080/
17470218.2011.552730
Stolzenburg, F. (2015). Harmony perception by periodicity detection.
Journal of Mathematics and Music, 9, 215–238. http://dx.doi.org/10
.1080/17459737.2015.1033024
Stolzenburg, F. (2017). Periodicity detection by neural transformation. In
E. Van Dyck (Ed.), Proceedings of the 25th Anniversary Conference of
the European Society for the Cognitive Sciences of Music (pp. 159–162).
Ghent, Belgium.
Stumpf, C. (1890). Tonpsychologie [Tone psychology]. Leipzig, Germany:
Verlag S. Hirzel.
Stumpf, C. (1898). Konsonanz und dissonanz [Consonance and disso-
nance]. Beiträge Zur Akustik Und Musikwissenschaft, 1, 1–108.
Sugimoto, T., Kobayashi, H., Nobuyoshi, N., Kiriyama, Y., Takeshita, H.,
Nakamura, T., & Hashiya, K. (2010). Preference for consonant musicover dissonant music by an infant chimpanzee. Primates, 51, 7–12.
http://dx.doi.org/10.1007/s10329-009-0160-3
Tabas, A., Andermann, M., Sebold, V., Riedel, H., Balaguer-Ballester, E.,
& Rupp, A. (2017). Early processing of consonance and dissonance in
human auditory cortex . Retrieved from http://arxiv.org/abs/1711.10991
Tartini, G. (1754). Trattato di musica secondo la vera scienza dell’armonia
[Treatise of music according to the true science of harmony]. Padova,Italy.
Terhardt, E. (1974). Pitch, consonance, and harmony. The Journal of the
Acoustical Society of America, 55, 1061–1069.
Terhardt, E. (1982). Die psychoakustischen Grundlagen der musikalischen
Akkordgrundtöne und deren algorithmische Bestimmung [The psycho-logical basis of musical chord root tones and their algorithmic determi-nation]. In C. Dahlhaus & M. Krause (Eds.), Tiefenstruktur . Berlin,
Germany: Technical University of Berlin.
Terhardt, E. (1984). The concept of musical consonance: A link between
music and psychoacoustics. Music Perception, 1, 276–295.
Terhardt, E., Stoll, G., & Seewann, M. (1982a). Algorithm for extraction of
pitch and pitch salience from complex tonal signals. The Journal of theAcoustical Society of America, 71, 679–688. http://dx.doi.org/10.1121/
1.387544
Terhardt, E., Stoll, G., & Seewann, M. (1982b). Pitch of complex signals
according to virtual-pitch theory: Tests, examples and predictions. The
Journal of the Acoustical Society of America, 71, 671–678. http://dx.doi
.org/10.1121/1.387543
Toro, J. M., & Crespo-Bojorque, P. (2017). Consonance processing in the
absence of relevant experience: Evidence from nonhuman animals.Comparative Cognition & Behavior Reviews, 12, 33–44. http://dx.doi
.org/10.3819/CCBR.2017.120004
Trainor, L. J., & Heinmiller, B. M. (1998). The development of evaluative
responses to music: Infants prefer to listen to consonance over disso-nance. Infant Behavior and Development, 21, 77–88. http://dx.doi.org/
10.1016/S0163-6383(98)90055-8
Trainor, L. J., Tsang, C. D., & Cheung, V. H. W. (2002). Preference for
sensory consonance in 2- and 4-month-old infants. Music Perception,
20,187–194.
Trulla, L. L., Stefano, N. D., & Giuliani, A. (2018). Computational ap-
proach to musical consonance and dissonance. Frontiers in Psychology,
9.http://dx.doi.org/10.3389/fpsyg.2018.00381
Tymoczko, D. (2011). A geometry of music . New York, NY: Oxford
University Press.
Tymoczko, D. (2016). In quest of musical vectors. In J. B. L. Smith, E.
Chew, & G. Assayag (Eds.), Mathemusical conversations (pp. 256–
282). London, UK: World Scientific.
Ushakov, Y. V., Dubkov, A. A., & Spagnolo, B. (2010). Spike train
statistics for consonant and dissonant musical accords in a simpleauditory sensory model. Physical Revie w E - Statistical, Nonlinear, and
Soft Matter Physics . Advance online publication. http://dx.doi.org/10
.1103/PhysRevE.81.041911
Vassilakis, P. N. (2001). Perceptual and physical properties of amplitude
fluctuation and their musical significance (PhD thesis). UCLA, Los
Angeles, CA.
Vassilakis, P. N. (2005). Auditory roughness as a means of musical
expression. In R. A. Kendall & R. H. Savage (Eds.), Selected reports in
ethnomusicology: Perspectives in systematic musicology (Vol. 12, pp.
119–144). Los Angeles: Department of Ethnomusicology, University ofCalifornia.
Vencovský, V. (2016). Roughness prediction based on a model of cochlear
hydrodynamics. Archives of Acoustics, 41, 189–201. http://dx.doi.org/
10.1515/aoa-2016-0019
Viro, V. (2011). Peachnote: Music score search and analysis platform. In
12th International Society for Music Information Retrieval Conference(ISMIR 2011; pp. 359–362).
Virtala, P., Huotilainen, M., Partanen, E., Fellman, V., & Tervaniemi, M.
(2013). Newborn infants’ auditory system is sensitive to Western musicchord categories. Frontiers in Psychology, 4, 492. http://dx.doi.org/10
.3389/fpsyg.2013.00492
Vos, J. (1986). Purity ratings of tempered fifths and major thirds. Music
Perception, 3, 221–257.
Vycˇiniene ˙, D. (2002). Lithuanian Schwebungsdiaphonie and its south and
east European parallels. The World of Music, 44, 55–57.
Wang, Y., Shen, G., Guo, H., Tang, X., & Hamade, T. (2013). Roughness
modelling based on human auditory perception for sound quality eval-uation of vehicle interior noise. Journal of Sound and Vibration, 332,
3893–3904. http://dx.doi.org/10.1016/j.jsv.2013.02.030
Watanabe, S., Uozumi, M., & Tanaka, N. (2005). Discrimination of con-
sonance and dissonance in Java sparrows. Behavioural Processes, 70,
203–208. http://dx.doi.org/10.1016/j.beproc.2005.06.001
Weisser, S., & Lartillot, O. (2013). Investigating non-Western musical
timbre: A need for joint approaches. In Proceedings of the Third Inter-
national Workshop on Folk Music Analysis (pp. 33–39). Amsterdam, the
Netherlands.243 SIMULTANEOUS CONSONANCE

## Page 29

Wever, E. G., Bray, C. W., & Lawrence, M. (1940). The origin of
combination tones. Journal of Experimental Psychology, 27, 217–226.
Wightman, F. L. (1973). The pattern-transformation model of pitch. The
Journal of the Acoustical Society of America, 54, 407–416. http://dx.doi
.org/10.1121/1.1913592
Zajonc, R. B. (2001). Mere exposure: A gateway to the subliminal. Current
Directions in Psychological Science, 10, 224–228.
Zentner, M. R., & Kagan, J. (1998). Infants’ perception of consonance and
dissonance in music. Infant Behavior and Development, 21, 483–492.
Zou, G. Y. (2007). Toward using confidence intervals to compare corre-
lations. Psychological Methods, 12, 399–413. http://dx.doi.org/10.1037/
1082-989X.12.4.399Zwicker, E., Flottorp, G., & Stevens, S. S. (1957). Critical band width in
loudness summation. The Journal of the Acoustical Society of America,
29,548–557. http://dx.doi.org/10.1121/1.1908963
Received January 21, 2019
Revision received June 13, 2019
Accepted September 2, 2019 /H18546244 HARRISON AND PEARCE

