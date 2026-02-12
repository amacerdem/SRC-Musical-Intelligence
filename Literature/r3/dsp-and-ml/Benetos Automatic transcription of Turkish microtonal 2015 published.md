# Automatic transcription of Turkish microtonal music

**Author:** Unknown  
**Subject:** N/A  
**Total Pages:** 13  
**Source File:** `Benetos Automatic transcription of Turkish microtonal 2015 published.pdf`

---

## Page 1

Automatic transcription of Turkish microtonal music
Emmanouil Benetosa)
Centre for Digital Music, Queen Mary University of London, London E1 4NS, United Kingdom
Andr /C19eHolzapfel
Department of Computer Engineering, Bo /C21gazic¸i University, 34342 Bebek, Istanbul, Turkey
(Received 21 January 2015; revised 18 August 2015; accepted 24 August 2015; published online
14 October 2015)
Automatic music transcription, a central topic in music signal analysis, is typically limited to
equal-tempered music and evaluated on a quartertone tolerance level. A system is proposed to
automatically transcribe microtonal and heterophonic music as applied to the makam music of
Turkey. Speciﬁc traits of this music that deviate from properties targeted by current transcription
tools are discussed, and a collection of instrumental and vocal recordings is compiled, along with
aligned microtonal reference pitch annotations. An existing multi-pitch detection algorithm isadapted for transcribing music with 20 cent resolution, and a method for converting a multi-pitch
heterophonic output into a single melodic line is proposed. Evaluation metrics for transcribing
microtonal music are applied, which use various levels of tolerance for inaccuracies with respect tofrequency and time. Results show that the system is able to transcribe microtonal instrumental
music at 20 cent resolution with an F-measure of 56.7%, outperforming state-of-the-art methods for
the same task. Case studies on transcribed recordings are provided, to demonstrate the shortcomingsand the strengths of the proposed method.
VC2015 Acoustical Society of America .
[http://dx.doi.org/10.1121/1.4930187 ]
[TRM] Pages: 2118–2130
I. INTRODUCTION
Automatic music transcription (AMT) is deﬁned as the
process of converting an acoustic music signal into some
form of music notation. The problem may be divided intoseveral subtasks, including multiple-F0 estimation, onset/
offset detection, instrument identiﬁcation, and extraction of
rhythmic information ( Davy et al. , 2006 ). Applications of
AMT systems include transcribing audio from musical styles
where no score exists (e.g., music from oral traditions, jazz),
automatic search of musical information, interactive musicsystems (e.g., computer participation in live human perform-
ances), as well as computational musicology ( Klapuri and
Davy, 2006 ). While the problem of automatic pitch estima-
tion for monophonic (single voice) music is considered
solved ( de Cheveign /C19e, 2006 ), the creation of a system able to
transcribe multiple concurrent notes from multiple instru-ment sources with suitable accuracy remains open.
The vast majority of AMT systems target transcription
of 12-tone equal-tempered (12-TET) Eurogenetic
1music
and typically convert a recording into a piano-roll represen-
tation or a MIDI ﬁle [cf. Benetos et al. (2013b) for a recent
review of AMT systems]. Evaluation of AMT systems istypically performed using a quartertone (50 cent) tolerance,
as, for instance, in the MIREX Multiple-F0 Estimation and
Note Tracking Tasks ( MIREX, 2007 ;Bay et al. , 2009 ). To
the authors’ knowledge, no AMT systems have been
evaluated regarding their abilities to transcribe non-equal
tempered or microtonal music, even though there is a limitednumber of methods that can potentially support the transcrip-
tion of such music.
Related works on multiple-F0 estimation and poly-
phonic music transcription systems that could potentiallysupport non-equally tempered music include the systems ofFuentes et al. (2013) ,Benetos and Dixon (2013) , and
Kirchhoff et al. (2013) , which are based on spectrogram
factorization techniques and utilize the concept of shift-
invariance over a log-frequency representation in order to
support tuning deviations and frequency modulations. The
techniques employed include shift-invariant probabilisticlatent component analysis ( Fuentes et al. , 2013 ;Benetos and
Dixon, 2013 ) and non-negative matrix deconvolution
(Kirchhoff et al. , 2013 ). The method of Bunch and Godsill
(2011) is also able to detect multiple pitches with high reso-
lution, by decomposing linear frequency spectra using aPoisson point process and by estimating multiple pitches
using a sequential Markov chain Monte Carlo algorithm.
Other systems that support high-precision frequency estima-tion for polyphonic music include Dixon et al. (2012) , which
was proposed as a front-end for estimating harpsichord
temperament, and the method of Rigaud et al. (2013) , which
is able to detect multiple pitches for piano music, as well asinharmonicity and tuning parameters.
The value of a transcription that takes microtonal
aspects into account is illustrated by the history of transcrip-
tion in ethnomusicology. In the late 19th century Alexander
J. Ellis recognized the multitude of musical scales present inthe musical styles of the world, and proposed the cent scale
in order to accurately specify the frequency relations
between scale steps ( Stock, 2007 ). In the beginning of the
20th century, Abraham and von Hornbostel (1994) proposed
a)Electronic mail: emmanouil.benetos@qmul.ac.uk
2118 J. Acoust. Soc. Am. 138(4), October 2015 0001-4966/2015/138(4)/2118/13/$30.00 VC2015 Acoustical Society of America


## Page 2

notational methods to transcribe “exotic” melodies, includ-
ing a multitude of ways to describe microtonal inﬂections.Seeger (1958) suggested methods for accurately annotating
microtonal inﬂections with an accuracy of 20 cents, a value
close to the range of just noticeable differences in musicalintervals [see Houtsma (1968) , as cited by Thompson (2013 ,
p.124)].
In addition to microtonality, another aspect of music
that has been so far ignored in AMT systems is the phenom-
enon of heterophony . Heterophony, as deﬁned by Cooke
(2001) , is the simultaneous variation of a single melody by
several musicians. From a technical perspective, a hetero-
phonic performance could be considered as polyphonic
2due
to the presence of several instruments, but the underlyingconcept is a monophonic melody. While heterophony is
widely absent from European musical styles, it is often asso-
ciated with the music of the Arab world ( Racy, 2003 ) and
encountered in similar ways in the music of the Balkans,
Turkey, Iran, and other cultures of the near and Middle East.
Not restricted to geographical area, it has also been assigned,for instance, to Javanese Gamelan ( Anderson Sutton and
Vetter, 2006 ), Korean music ( Lee, 1980 ), and African
American congregational singing, to name but a few. It haseven been hypothesized as the origin of all music by Brown
(2007) , by interpreting polyphony as a later state of organi-
zation in pitch space. Because there is an apparent absenceof previously published microtonal or heterophonic AMT
approaches [see Bozkurt et al. (2014) ], presumably attrib-
uted to a cultural bias toward Eurogenetic music, a consider-ation of these wide-spread musical traits in an AMT system
seems timely. In general this would be advantageous for
accommodating newfound access to the diversity of musicalstyles.
In this work, a system for transcribing heterophonic and
microtonal music is proposed and applied to Turkish makammusic, following preliminary work presented by Benetos
and Holzapfel (2013) . A collection of instrumental and vocal
recordings has been compiled, along with detailed microto-nal reference pitch annotations for quantitative evaluation of
the system. The proposed method adapts a previously devel-
oped multi-pitch detection algorithm ( Benetos and Dixon,
2013 ) to address the speciﬁc challenges of Turkish makam
music and includes methods for converting a multi-pitch
heterophonic output into a single melodic line. Evaluationsare performed using various levels of tolerance for inaccura-
cies with respect to frequency and time. Results show that
the system is able to transcribe microtonal instrumentalmusic with 20-cent resolution. Case studies on transcribed
recordings are provided, in order to demonstrate the short-
comings and the strengths of the method.
An outline of the paper is as follows: In Sec. II, motiva-
tions for creating technologies for transcribing heterophonic
and microtonal music are given. Section IIIpresents the
instrumental and vocal music collections that were used for
experiments, along with the pitch annotation process. The
proposed system is described in Sec. IV. The employed eval-
uation metrics and results are presented in Sec. V. Finally,
the performance of the proposed system is discussed in Sec.
VI, followed by conclusions in Sec. VII.II. MOTIVATIONS
Until recently, AMT approaches were developed and
evaluated mainly in the context of Eurogenetic music. A dis-
advantage of such concentration is that AMT technology
may be inadequate when applied to many music stylesaround the world, whose characteristics are fundamentally
different from those of Eurogenetic music.
Regarding timbre as a ﬁrst property, the authors note
that polyphonic performances by piano and other
Eurogenetic instruments attract a lot of attention for the
development of AMT systems, while the consideration ofinstrumental timbres from other cultures represent rather an
exception ( Nesbit et al. , 2004 ). How a wider diversity of
instrumental timbres can be transcribed automatically andaccurately remains to be explored.
A second property of Eurogenetic music that limits the
musical diversity that AMT systems can handle is theassumption that pitch is distributed according to the 12-TETsystem. Most current AMT approaches aim to produce a
so-called “piano-roll” that speciﬁes which note of the equal-
tempered system is sounded at what time. Many music tradi-tions, however, make use of very different organization of
the tonal space, as for instance, the modal structures used in
Turkey, Iran, Iraq, and India.
Finally, AMT systems for Eurogenetic music have been
built on the assumption that music signals contain several dis-
tinct melody lines, or one melody line with a harmonic ac-companiment. However, several music traditions in the world
express melodies in a heterophonic way. That means that sev-
eral instruments play one basic melody with each instrumentinterpreting it slightly differently, according to the aesthetic
concepts of the music tradition. As far as the authors are
aware, heterophony, as a combination of apparent polyphonyat the signal level and monophony at the conceptual level has
so far never been approached systematically with a prior
AMT system.
The concentration of prior AMT systems on a limited
range of timbres, the equal-tempered system, and restriction
to either monophonic or polyphonic music, creates a distinctcultural bias towards Eurogenetic music. This motivates usto present a systematic study of an AMT system which
focuses on a music that challenges all three structural biases.
Turkish makam music was practiced at the Ottoman courtand in religious ceremonies during the times of the Ottoman
Empire, and continues to live on in today’s music practice in
modern Turkey in various forms. The melodies of this musicfollow the modal framework of the makam , which includes
the notion of a scale and rules for melodic progression.
While a comprehensive overview of the tonal and rhythmicconcepts of Turkish makam music is given in Bozkurt et al.
(2014) , some of the properties of this music that are of
particular relevance for the development of an AMT systemwill be emphasized.
(1) The Arel-Ezgi notation and tuning ( Arel, 1968 ) repre-
sents the ofﬁcial standard today. While intervals aredeﬁned using Pythagorean pitch ratios, they are quan-
tized to integer multiples of the Holderian-Mercator
comma, /C2522.64 cents ( Bozkurt et al. , 2014 ). As shown
J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel 2119

## Page 3

in Fig. 1, according to Arel-Ezgi notation the intervals of
1, 4, 5, 8, and 9 commas are used within a whole tone.
The whole tone interval, which is related to the fre-quency ratio 9/8 or 203.91 cents, is slightly sharp com-pared to 12-tone equal temperament (200 cents).Musical practice, however, tends to deviate from this
notation by using pitch classes systematically different
from those deﬁned by the accidentals. This theory-practice mismatch in respect to the underlying tuningsystem represents a challenge for an AMT system. It is,
however, important to point out that the Holderian-
Mercator comma deﬁnes the smallest pitch difference inTurkish music, further supporting a maximum resolutionof about 20 cents in frequency.
(2) Whereas the staff notation in a Eurogenetic context gen-
erally relates a certain pitch value to a speciﬁc funda-mental frequency, this is not the case for Turkish makam
music. Here, the musician may choose between one of
12 different transpositions, with the choice usually deter-mined by the type of instrument being played, or the pre-ferred vocal register of a singer.
(3) As a heterophonic music, a melody may be interpreted
by instruments in different octaves.
(4) The notated melodies are richly ornamented using a set
of idiosyncratic playing or singing techniques. Thesetechniques are not documented in written theory, but are
part of oral tradition and therefore only possible to grasp
by applying ethnographic approaches. According toinsights from ﬁeldwork by the second author, the com-mon practice is to add notes and embellishments duringa performance while at the same time maintaining the
onsets of the notes in a score. An illustrative example is
given in Fig. 2, where the notation of a short phrase in
makam Beyati is compared with the transcription of a
performance of the phrase as performed on the instru-
ment oud, a short-necked fretless lute. It is apparent that
the density of notes has increased, while the originallynotated onsets are maintained.(5) In Turkish makam music, a set of instrumental timbres is
encountered that is very characteristic for this music, andthat differs from timbres usually encountered inEurogenetic music. Further detail about the timbral qual-ities of these instruments is provided in Sec. III.
(6) Turkish makam music possesses no concept of func-
tional harmony, but is a music based on modes calledmakam . The modes deﬁne a scale and characteristics of
melodic progression. In the melodic progression, centralnotes of the mode are emphasized, and particular impor-tance has the ﬁnal note ( karar ) that concludes the pro-
gression and is usually referred to as the tonic in English
language.
While these traits clearly set Turkish makam music
apart from Eurogenetic music, Turkish makam music offersa relatively well-controlled environment for experimentswith AMT systems. This is because of the large collectionsof music recordings and associated notations that are avail-able from the work of the CompMusic project.
3These con-
trolled conditions signiﬁcantly facilitate the creation ofreference pitch annotations for music performances, which isnecessary for the quantitative evaluation of an AMT system.On the other hand, establishing an AMT system for thismusical style is an important ﬁrst step towards automatictranscription of microtonal and heterophonic music through-out the music traditions of the world.
III. MUSIC COLLECTION
Turkish makam music makes use of instrumental
timbres that clearly deﬁne the acoustic identity of this music.In Sec. III A an overview of the two instrumental timbres
that were chosen as representatives of this identity is given,and the recorded material used for acquiring timbral tem-plates is explained. Since the music collection used for theevaluation should cover a large variety, a set of instrumentalperformances and a set of vocal performances were com-
piled, which will be described in detail in Secs. III B and
III C. Only performances of pieces that are available in the
SymbTr collection ( Karaosmano /C21glu, 2012 ), which contains
microtonal notation for Turkish music in a machine-readableformat, were chosen. These annotations are a valuable start-ing point for the note-to-note alignment between notationand performance, which is needed for the evaluation of thesystem. The compilation of these reference transcriptionswill be detailed in Sec. III D.
FIG. 1. Visualization of the accidentals used in Turkish music. Only four of
the possible eight intermediate steps that divide a whole tone are used. The
size of the step is 1 Hc (Holderian-Mercator comma) /C2522:64 cents.
FIG. 2. Two representations of the
same melody, comparing the basic
form as found in a score with the tran-
scription of the same phrase as per-
formed on the oud.
2120 J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel

## Page 4

A. Timbral properties
Among the most widespread instruments for Turkish
makam music are the tanbur , a long-necked lute, and the
ney, an end-blown ﬂute (constructed from reed material).
The tanbur in its common form has seven strings, one bass
string and three courses of double strings plucked using a
plectrum made of tortoise shell. Melodies are played almost
exclusively on the lowest course of double strings, while the
other strings are plucked as a drone when the player wishesto give emphasis. Because of this playing technique, the
instrument can be considered to have a limited polyphonic
capacity. The length of the neck, the number of frets andtheir placement vary among instrument makers. Because the
frets are movable, players frequently change their positions
to adapt their tuning to, for instance, the tuning of anotherplayer. The main factor that inﬂuences the characteristic
sound of this instrument is its very thin resonating sound-
board, which does not have a sound hole. The open vibratingdrone strings ampliﬁed by the resonating soundboard lend a
very speciﬁc timbre to this instrument: the fourth harmonic
exceeds the energy of the second harmonic in the radiatedsound of the instrument, especially for forcefully plucked
notes ( Erkut et al. , 1999 ).
The ney has importance in court music ensembles as
well as in religious practice. It is an end-blown ﬂute, and as
such is strictly monophonic, with a length between 52 and
104 cm depending on which lowest pitch is desired. As
described in Sec. II, there are theoretically 12 transpositions
in Turkish music, and their names refer to the ney’s funda-mental pitches. There are variations in the positioning of the
ﬁnger holes depending on the instrument maker, just as there
are variations in the placement of frets on the tanbur.Additionally, natural deviation of the nodes of the reed stalk
from being equidistant result in a further source of variance.
The pitch of a single ﬁngering is strongly inﬂuenced byembouchure adjustments and angle of attack, enabling a
player to precisely adjust tuning. The basic tonal range of
the instrument is expanded by varying force and angle,reaching up to two and a half octaves. Notes in the higher
range in particular, demand greater effort by the player to
correct pitch to a desired one. Due to its construction as anend-blown ﬂute, including all variations in positioning the
instrument, the ney’s timbre always contains a very high
noise component.
Further instrumental timbres that are contained in
ensemble performances of Turkish makam music are the
kemence , a small ﬁddle played with a bow; the oud, a short
necked lute; and the kanun , a type of zither played by pluck-
ing the strings. While the kemence can be considered a
monophonic instrument, the oud and kanun can express
polyphony.
The AMT system introduced in this paper offers the
possibility to incorporate knowledge about the timbres of
instruments targeted for transcription. As described in more
detail in Sec. IV A, this knowledge is incorporated by learn-
ing typical magnitude spectra for pitches throughout the
range of an instrument. In order to learn these templates,
solo recordings of the target timbres are needed. To this end,pitches in approximately semitone intervals throughout the
whole range of the instruments were recorded from ney,
tanbur, kemence and kanun in a quiet environment using astudio quality portable recorder. In addition to these record-ings, three ney and four tanbur solo performances fromcommercially available recordings were included in order
to increase the timbral variety of the templates. In order to
evaluate the system for vocal performances, vocal timbretemplates were derived from solo recordings of those singersincluded in the collection of performances used for systemevaluation. From the recordings of singers and the solo
instrument performances, regions with relatively stable pitch
were identiﬁed manually throughout the vocal range of thesinger or instrument. All recordings of stable pitch regionswere then used to derive the spectral templates for oursystem as described in Sec. IV A.
Descriptive examples of the spectral content of these
template recordings are contrasted with a piano example inFig.3. In Fig. 3(a), the harmonic series for the piano has a
clear fundamental, and generally slowly decreasing ampli-
tudes towards higher harmonics, with the second harmonicat 220 Hz having a slightly smaller amplitude than the thirdharmonic. The tanbur is characterized by a very weak funda-mental (at 110 Hz), which is a phenomenon present through-out the range of the instrument, and not restricted to this
note. The strongest harmonics are the third to ﬁfth harmon-
ics, and the higher harmonics have less energy than for thepiano. Throughout the duration of the note, an increasingfocus on the frequency band between 300 and 1000 Hz canbe seen. The spectrogram of the ney in Fig. 3(c)displays its
noisy character caused by the type of excitation, as well
as the practical absence of harmonics beyond the fourth. Aharmonic series based on 220 Hz can be detected in thespectrogram. Even so, the actual perceived pitch seems to beabout 440 Hz.
B. Instrumental performances
The most common forms of makam instrumental com-
positions are the Pes¸revandSaz Semaisi forms. They share a
similar overall compositional structure, with one repeated
section ( Teslim ) interchanging with up to four sections
(Hane ) of new thematic material. Five solo performances for
each ney and tanbur were chosen, and six ensemble perform-ances that contain various instruments. Table Igives an
overview of the instrumental performances. Horizontal lines
in Table Idivide the collection amongst groups that repre-
sent different recordings of the same composition. The tonicfrequencies, obtained by manual annotation, demonstrate thedifferent tonal ranges of the instruments, as well as the diver-sity of chosen transpositions. The depicted number of notesis obtained from the SymbTr notations, and the notes are
edited as described in detail in Sec. III D. For ensemble per-
formances, the instruments are identiﬁed as kanun (k),kemence (f), ney (n), oud (o), percussion (p), and tanbur (t).
C. Vocal performances
Three renowned vocal performers of Turkish makam
music were chosen for vocal performances (see Table II),
J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel 2121

## Page 5

with most of the recordings chosen from the middle of the
20th century. All recordings contain the accompaniment byseveral instruments and can therefore be considered as heter-
ophonic performances. The choice of singers was inﬂuenced
by the availability of recorded vocal performances withoutinstrumental accompaniment, a necessary prerequisite in our
context, in order to obtain spectral templates per pitch for
the speciﬁc singers. Solo vocal improvisations ( gazel ),
Quran recitations and vocal teaching material were used to
this end. Commercially or publicly available solo performan-
ces could not be found for any of the recent popular singersof Turkish makam music. This led to the vocal collection
having an average recording quality that is inferior to the
average quality of the instrumental collection.D. Manual pitch annotation process
For evaluation purposes, it was a necessary step to spec-
ify the onset times of notes as well their (microtonal) pitchvalues. Considering the performance practice described inSec.II, where a high density of individual notes corresponds
to a lower density series of notes in the notated melody, note
offset times were not annotated. Machine-readable notationsfrom the SymbTr collection were used as a starting point toderive the desired reference annotations. The semi-automatic
approach that was followed had to take into account the
micro-tonality and elaboration of melodies that are describedin Sec. II. The SymbTr collection includes microtonal infor-
mation, but all currently available pitch and onset alignmentsoftware is restricted to the lower resolution of the 12-TET
system. For this reason, time alignment was performed using
standard tools in 12-TET resolution, and then microtonalinformation was re-established. However, the SymbTr nota-tions depict only the notes of the basic melody of a composi-tion, with embellishments in the performances not being
included. Hence, the objective of the transcription task is
to create a transcription of the basic melody played by allincluded instruments in the heterophony, rather than adescriptive transcription ( Seeger, 1958 ) of the detailed orna-
mentations present. The manual annotation process was con-
ducted by the two authors. The ﬁrst author holds a degree in
piano performance, and the second author has ﬁve years ofTABLE I. Collection of instrumental recordings used for transcription.
Form Makam Instr. Notes Tonic/Hz
1 Pes ¸rev Beyati Ensemble (k,f,n,o,p,t) 906 125
2 Pes ¸rev Beyati Ney 233 438
3 Saz S. Hicazkar Tanbur 706 1474 Pes ¸rev H €useyni Ensemble (n,p) 302 445
5 Pes ¸rev H €useyni Ensemble (k,f,n,p,t) 614 124
6 Saz S. Muhayyer Ney 560 4957 Saz S. Muhayyer Ensemble (k,f,n,t) 837 2948 Pes ¸rev Rast Tanbur 658 148
9 Pes ¸rev Rast Ney 673 392
10 Pes ¸rev Segah Ney 379 541
11 Pes ¸rev Segah Ensemble (k,f,n) 743 246
12 Saz S. Segah Ensemble (k,f,n,p,t) 339 31113 Saz S. Segah Tanbur 364 18614 Saz S. Us ¸s¸ak Tanbur 943 165
15 Saz S. Us ¸s¸ak Tanbur 784 162
16 Saz S. Us ¸s¸ak Ney 566 499
FIG. 3. Note spectrograms for three instruments. The sidebar values are in
dB, with 0 dB denoting the largest magnitude in the depicted power
spectrum.
TABLE II. Collection of vocal recordings used for transcription.
Singer Title (Makam) Notes Tonic/Hz
1 Bekir Sıdkı
SezginBekledim Yıllarca L ^akin Gelmedin
(H€uzzam)451 141
2 Bekir Sıdkı
SezginYandıkc ¸a Oldu S ^uz^an (Suzidil) 243 111
3 Kani Karaca Bir Nig ^ah Et Ne Olur Halime (Hicaz) 306 123
4 Kani Karaca €Ulfet Etsem Y ^ar ile A /C21gy^are Ne
(Hicaz-Uzzal)425 123
5 Saﬁye Ayla Vars in G €on€ul As¸kınla (Nis ¸aburek) 339 335
6 Saﬁye Ayla Bu Aks ¸am Ayıs ¸ı/C21g inda (Saba) 333 328
2122 J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel

## Page 6

practice of Turkish oud and took lessons from several mas-
ters of Turkish makam music.
As a ﬁrst step in compiling the reference annotations,
the SymbTr notations were manually edited in order to
reﬂect exactly the sequence of sections as chosen in the
performance. This is necessary because performers mayomit sections of a piece or their notated repetitions. In the
next step the (microtonal) SymbTr notation was converted to
standard MIDI, and the approach presented by Macrae and
Dixon (2010) was applied in order to get a rough estimate of
the temporal alignment between the recording and thenotes in a MIDI representation of the music. The resulting
pre-aligned MIDI ﬁle was then loaded into Sonic Visualiser
4
as a notation layer on top of the spectrogram of the record-
ing, and the timing of the alignment was corrected manually.
The manual alignment resulted in a list of notes with an
accurate temporal alignment and a frequency resolution of 1
semitone. Micro-tonal information was then recovered from
the edited SymbTr notations, obtaining a list of pitch valueswith 1 Hc resolution. The pitch values are normalized with
respect to the tonic ( karar ) of the piece, so that the tonic was
assigned a value of 0 cent. In Fig. 4an example of the pitch
annotation output is depicted. In this example, the ornamen-
tations resulting in additional notes between 135.5 and 137 s
(vertical lines caused from onsets of the kanun can be recog-
nized) were not annotated, resulting in an alignment of the
basic melody to this heterophonic ensemble performance.The annotation process resulted in reference annotations
containing a total of 11 704 notes, consisting of 2411 for
ney, 3455 for tanbur, 3741 for ensemble, and 2097 for vocalpieces. The annotations are available on the second author’s
website,
5while the audio recordings can be obtained by
using the provided identiﬁers.In order to compare a reference pitch annotation with
the output of the system for a given performance, the tonicfrequency from this performance is needed. As described in
Sec. II, this frequency depends on the chosen transposition
and on tuning inaccuracies. The tonic frequencies for all per-
formances were manually annotated. However, experiments
on automatic tonic frequency estimation ( Bozkurt, 2008 )
were conducted, and errors due to automatic estimation were
monitored.
IV. SYSTEM
The proposed system takes as input an audio recording
and information about the melodic mode (in this case, the
makam). Multi-pitch detection with 20 cent resolution is per-formed based on the systems of Benetos and Dixon (2013)
andBenetos et al. (2013a) , which were originally proposed
for transcribing Eurogenetic music [they ranked ﬁrst in the
MIREX 2013 Multiple F0 Estimation & Note Tracking pub-
lic evaluation (MIREX)]. The original systems’ abilities tosupport multi-pitch detection in a resolution ﬁner than a
semitone, which had not been exploited nor evaluated in
Benetos and Dixon (2013) , have been utilized. In addition, a
note template dictionary using instruments and vocal
performances from Turkish makam music is included inthe proposed system. Finally, in order to support the tran-
scription of heterophonic music, post-processing steps are
included that convert a multi-pitch output into a single
melodic line, and center the cent-scale output around
the detected tonic. A diagram of the proposed transcriptionsystem can be seen in Fig. 5.
A. Spectral template extraction
In dictionary-based transcription systems, spectral tem-
plates per pitch are typically extracted from isolated note
samples ( Dessein et al. , 2010 ). Since to the authors’ knowl-
edge such a database of isolated note samples for Turkishinstruments and vocals does not exist, recordings were
performed and appropriate available solo performances were
selected in order to obtain material from which to extract
spectral templates, as detailed in Sec. III A.
For the ney and tanbur solo performances, each note
segment is identiﬁed and manually labeled, and the probabil-
istic latent component analysis (PLCA) method ( Smaragdis
et al. , 2006 ) with one component was employed per segment
in order to extract a single spectral template per pitch. The
time/frequency representation used was produced by a
FIG. 4. Screenshot of an aligned sequence: the spectrogram for a short
phrase in recording 5, with the aligned note onsets. Four instruments inter-
pret the melody heterophonically: while the kanun ornaments strongly, the
other instruments play closer to the basic melody.
FIG. 5. Proposed transcription system diagram.
J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel 2123

## Page 7

constant-Q transform (CQT) with a spectral resolution of 60
bins/octave (corresponding to 20 cent resolution), with
27.5 Hz as the lowest bin, and a 20 ms time step ( Brown,
1991 ). Since in log-frequency representations like CQT
inter-harmonic spacings are consistent for all pitches, spec-
tral templates for missing pitches in the training set were
created by shifting the CQT spectra of neighboring pitches.
The same PLCA-based process was used for extracting
templates from the set of isolated notes for ney, tanbur,
kemence, and kanun. This resulted in an instrumental dic-
tionary consisting of 5 ney models (spanning notes 60–88 in
the MIDI scale), 5 tanbur models (spanning notes 39–72), 2
kanun models (spanning notes 53–88), and one kemence
model (spanning notes 56–88).
For creating vocal templates, a training dataset of six
solo voice recordings of Turkish makam music was used,
covering the singers listed in Table II. Given the non-stable
nature of the singing voice, a semi-supervised method was
employed in order to speed up the annotation/template
extraction process. A spectrogram of each recording was
displayed using Sonic Visualiser;4stable pitch areas were
manually annotated, and these annotated segments were con-
catenated to a new recording exclusively containing stable
pitches. The aforementioned recording was used as input to
the supervised PLCA algorithm, where the pitch activations
were ﬁxed (using the aforementioned user annotations) and
the dictionary was estimated. The resulting vocal templates
span MIDI notes 46 to 80.
B. Transcription model
For performing multi-pitch detection the model of
Benetos and Dixon (2013) , originally developed for compu-
tationally efﬁcient transcription of Eurogenetic music,
was employed and adapted. This model expands PLCA
techniques by supporting the use of multiple pre-extracted
templates per pitch and instrument source, as well as shift-
invariance over log-frequency; the latter is necessary for
performing multi-pitch detection at a frequency resolution
higher than the semitone scale, as in the present work.
The transcription model takes as input a normalized log-
frequency spectrogram Vx;t(xis the log-frequency index
andtis the time index) and approximates it as a bivariate
probability distribution Pðx;tÞ.Pðx;tÞis decomposed into a
series of log-frequency spectral templates per pitch, instru-
ment, and log-frequency shifting (which indicates deviation
from the 12-TET system), as well as probability distributions
for pitch activation, instrument contribution, and tuning.
The model is formulated as
Pðx;tÞ¼PðtÞX
p;f;sPðxjs;p;fÞPtðfjpÞPtðsjpÞPtðpÞ;(1)
where pdenotes pitch, sdenotes instrument source, and f
denotes log-frequency shifting. P(t) is equal to RxVx;t,
which is a known quantity. All factors in the right-hand side
of Eq. (1)are matrices (or tensors) containing values which
vary from 0 to 1, indexed by their respective integer random
variables. Pðxjs;p;fÞdenotes pre-extracted log-spectraltemplates per pitch pand source s, which are also pre-shifted
across log-frequency according to index f. The pre-shifting
operation is made in order to account for pitch deviations,without needing to formulate a convolutive model acrosslog-frequency, as was the case for Smaragdis (2009) .P
tðfjpÞ
is the time-varying log-frequency shifting distribution per
pitch, PtðsjpÞis the time-varying source contribution per
pitch, and ﬁnally, PtðpÞis the pitch activation, which is
essentially the resulting transcription. The shifting index fis
constrained to a semitone range with respect to an ideally
tuned pitch according to 12-TET; given the CQT resolution(20 cents), f2½1; :::;5/C138, with 3 indicating no deviation from
12-TET (this represents tuning values of /C040,/C020, 0, 20,
and 40 cents).
The unknown model parameters P
tðfjpÞ;PtðsjpÞ, and
PtðpÞare estimated using iterative update rules based on the
expectation-maximization (EM) algorithm ( Dempster et al. ,
1977 ). For the expectation step, an intermediate distribution
(i.e., the model posterior) is computed,
Ptp;f;sjx ðÞ ¼Pxjs;p;f ðÞ PtfjpðÞ PtsjpðÞ PtpðÞ
X
p;f;sPxjs;p;f ðÞ PtfjpðÞ PtsjpðÞ PtpðÞ:(2)
For the maximization step, the unknown model parame-
ters are updated using the posterior from Eq. (2):
PtfjpðÞ ¼X
x;sPtp;f;sjx ðÞ Vx;t
X
f;x;sPtp;f;sjx ðÞ Vx;t; (3)
PtsjpðÞ ¼X
x;fPtp;f;sjx ðÞ Vx;t
X
s;x;fPtp;f;sjx ðÞ Vx;t; (4)
PtpðÞ¼X
x;f;sPtp;f;sjx ðÞ Vx;t
X
p;x;f;sPtp;f;sjx ðÞ Vx;t: (5)
Equations (2)–(5)are iterated, with the number of itera-
tions set to 30. The various matrices are initialized with ran-dom values; from EM theory, convergence to a local
maximum is guaranteed ( Dempster et al. , 1977 ). The tem-
plates Pðxjs;p;fÞare kept ﬁxed using the pre-extracted and
pre-shifted spectral templates from Sec. IV A. The output of
the transcription model is a pitch activation matrix and a
pitch shifting tensor, which are, respectively, given by
Pðp;tÞ¼PðtÞP
tðpÞ; (6)
Pðf;p;tÞ¼PðtÞPtðpÞPtðfjpÞ: (7)
By stacking slices of Pðf;p;tÞfor all pitch values, a
time-pitch representation with 20 cent resolution can becreated,
2124 J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel

## Page 8

Pðf0;tÞ¼½ Pðf;plow ;tÞ/C1/C1/C1Pðf;phigh ;tÞ/C138; (8)
where f0denotes pitch in 20 cent resolution, with plow¼39
being the lowest MIDI-scale pitch value, and phigh¼88 the
highest pitch value considered. In Fig. 6the time-pitch repre-
sentation for a ney recording (piece no.2 from Table I) can
be seen.
C. Post-processing
The outputs of the transcription model of Sec. IV B are
non-binary and need to be converted into a list of noteevents, listing onset, offset, and pitch (the latter relative tothe tonic frequency). First, median ﬁltering is performedonP(p,t), which is subsequently thresholded (i.e., matrix
elements below a certain value are set to zero), and followedby minimum duration pruning (i.e., removing note eventswith durations less than 120 ms).
Since a signiﬁcant portion of the transcription dataset
consists of ensemble pieces where instruments (and in somecases, voice) are performing in octave unison, the hetero-phonic output of the multi-pitch detection algorithm needs tobe converted into a monophonic output that will be usable asa ﬁnal transcription. Thus, a simple “ensemble detector” iscreated by measuring the percentage of octave intervals inthe detected transcription. If the percentage is above 15%,the piece is considered an ensemble piece. Subsequently, foreach ensemble piece each octave interval is processed bymerging the note event of the higher note with that of thelower one.
In order to convert a detected note event into the cent
scale, information from the pitch shifting tensor Pðf;p;tÞis
used. For each detected event with pitch pand for each time
frame t, the value of pitch deviation fthat maximizes
Pðf;p;tÞis found,
^f
p;t¼arg max
fPðf;p;tÞ: (9)
The median of ^fp;tfor all time frames belonging to each note
event is selected as the tuning that best represents that note.Given the CQT resolution (60 bins/octave), the value in cent
scale for the lowest frequency bin of the detected pitch is
simply 20 ð^f/C01Þ, where ^fis the pitch shifting index
(f2½1;…;5/C138) of the detected note.
D. Tonic detection
Because of the unknown transposition of the perform-
ance, we need to determine the frequency of the tonic in Hz
in order to compare the automatic transcription with the ref-erence pitch annotations. To this end, the procedure
described by Bozkurt (2008) is applied. The method com-
putes a histogram of the detected pitch values and aligns it
with a template histogram for each makam using a cross-
correlation function. The peak value of the pitch histogramis then assigned to the tonic that is closest to the peak of the
tonic in the template, and all detected pitches are centered
on this value. Finally, after centering the detected noteevents by the tonic, note events that occur more than 1700
cents or less than /C0500 cents from the tonic are eliminated,
since such note ranges are rarely encountered in Turkish
makam music.
V. EVALUATION
A. Metrics
For assessing the performance of the proposed system in
terms of microtonal transcription, a set of metrics is pro-posed, by adapting the onset-based transcription metrics used
for the MIREX Note Tracking evaluations ( Bayet al. ,2 0 0 9 ).
In onset-based transcription evaluation of Eurogenetic music,
an automatically transcribed note is assumed to be correct if
its F0 deviates less than 50 cents from the annotated refer-ence pitch and its onset is within either a 50 or 100 ms toler-
ance from the ground truth onset.
For the proposed evaluations, an automatically tran-
scribed note is considered to be correct if its F0 is within a
620 cent tolerance around the annotated reference pitch and
its onset is within a 100 ms tolerance. The 620 cent and
6100 ms tolerance levels were considered as “fair margins
for an accurate transcription” by Seeger (1958) . The
FIG. 6. The time-pitch representation
Pðf0;tÞfor the ney piece No. 2 from
Table I.
J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel 2125

## Page 9

following onset-based Precision, Recall, and F-measure are
subsequently deﬁned:
Pons¼Ntp
Nsys;Rons¼Ntp
Nref;Fons¼2RonsPons
RonsþP ons;(10)
where Ntpis the number of correctly detected notes, Nsysthe
number of notes detected by the transcription system, andN
refthe number of reference notes. Duplicate notes are
considered as false positives. In all results, we display themetrics averaged across groups of recordings. It is important
to point out that notes in octave distance are not considered
as equal, since the differentiation of the octaves is importantfor a correct transcription of the melodic progression.
B. Results—Instrumental transcription
Two types of instrumental transcription evaluations
were performed. The ﬁrst tested the automatically detected
tonic produced by the system of Bozkurt (2008) . In the
second evaluation, a manually annotated tonic was used. Theproposed method was able to transcribe the entire 75 mininstrumental dataset in less than one hour, i.e., less than
real time. The instrumental transcription system included
templates from the ney, tanbur, kanun, and kemencedictionaries.
Results using manually annotated tonic are shown in
Table III, for the complete dataset as well as for individual
instrument families. Results using the automatically detectedtonic for the same dataset can be seen in Table IV. Using a
manually annotated tonic, the proposed system reachedF
ons¼56:75% with a 20 cent tolerance [preliminary experi-
ments in Benetos and Holzapfel (2013) reached 51.24%
using a smaller dictionary]. All instrument subsets exhibitedtranscription performance above 50%, with a best perform-ance of 58.5% being reached by the tanbur subset.
In order to demonstrate the robustness of the pitch-
activation threshold parameter, an ROC curve for recall-vs-precision is shown in Fig. 7, where the thresholded values
are varied from 1.0 to 10.0 [determined by the values inP(t)]. It can be seen that the system is fairly robust to thresh-
old changes, with the lowest values reached by Precision and
Recall being around 45%. From Fig. 7it is apparent that the
curve for tanbur reaches higher precision values than the neyand ensemble curves, which implies that the system detectsfewer spurious onsets for the tanbur. One reason for the
maximum possible precision being the lowest for the ensem-
ble pieces is due to a heterophonic performance practice. Inthe presence of several instruments, usually at least oneinstrument will strongly ornament the basic melody, whichadds additional notes to the automatic transcription. An
example of this process is given in Fig. 8, which shows the
same excerpt as Fig. 4, but visualizes the automatically tran-
scribed notes. The presence of ornamentations led to four
false positive detections (according to the reference pitch
annotation) between 135 and 138 s.
For comparing the proposed method with a recently
published transcription algorithm, the method of Vincent
et al. (2010) was employed. This method performs multi-
pitch detection using adaptive non-negative matrix factoriza-
tion and expresses an audio spectrogram as a series of
weighted narrowband harmonic spectra. To ensure a faircomparison with the proposed method, the output of the
aforementioned multi-pitch detection system (a list of note
onsets and corresponding pitches) is post-processed in thesame way as described in Sec. IV C, resulting in a list of
onsets and pitches in cent value centered by a tonic. Results
for the complete instrumental set using a manually annotated
tonic show that the Vincent et al. (2010) method reaches
F
ons¼38:52% with 20 cent tolerance and Fons¼49:84%
with 50 cent (i.e., semitone scale) tolerance, indicating that
the proposed method, which reached 56.75%, is more suita-
ble for the task of transcribing Turkish makam music, bothin a microtonal setting and using a semitone resolution (cf.
Table V).
Another comparison is carried out with respect to
monophonic transcription, using the benchmark YIN pitch
detection algorithm ( de Cheveign /C19e and Kawahara, 2002 ).
Since YIN returns a continuous series of pitch values with-out identifying onsets/offsets, an “oracle” approach was
employed, by using the ground truth (i.e., manually
derived) onsets and offsets as additional information. Thus,for each annotated note event (deﬁned by its ground truth
TABLE III. Instrumental transcription results using manually annotated
tonic.
Pons Rons Fons
Ney recordings 55.89% 54.71% 55.00%
Tanbur recordings 64.88% 53.41% 58.52%Ensemble recordings 51.44% 65.71% 57.06%All recordings 57.31% 57.74% 56.75%TABLE IV. Instrumental transcription results using automatically detected
tonic.
Pons Rons Fons
Ney recordings 53.22% 51.12% 51.91%
Tanbur recordings 44.51% 36.26% 39.91%Ensemble recordings 42.72% 54.24% 47.34%All recordings 47.22% 47.45% 46.73%
FIG. 7. ROC curves for recall-vs-precision using the instrumental dataset,
as pitch-activation threshold values are varied.
2126 J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel

## Page 10

onset-offset), its pitch is estimated by selecting computing
the median pitch returned from YIN for that segment; this
process is followed by the same post-processing steps
described in Sec. IV C, again returning a list of onsets and
pitches in cent value centered by a tonic. For the instrumen-
tal set, Fons¼51:71% (cf. Table V), while for the mono-
phonic recordings Fons¼55:41% (the latter compared to
56.60% for the proposed system).
Experiments on the robustness of the proposed method to
degradations of the audio input were also carried out, usingthe Audio Degradation Toolbox of Mauch and Ewert (2013) .
Pre-deﬁned “vinyl” degradations were used, which are rele-
vant for the collection selected for evaluation. The toolbox
adds impulse responses, LP surface crackle, wow-and-ﬂutterirregularities in playback speed, and pink noise. Using the
degraded audio recordings, transcription performance reached
46.42%, which shows that the proposed system is relativelyrobust to reduction in recording quality (cf. Table V).
As in our preliminary experiments ( Benetos and
Holzapfel, 2013 ), there is a performance drop (10% in terms
of F-measure) when the automatically detected tonic was
used compared to the manually supplied one. This is attrib-
uted to the fact that with a 20 cent F0 evaluation tolerance,even a slight tonic miscalculation might lead to a substantial
decrease in performance. Major tonic misdetections were
observed for instrumental recordings 3 and 5 (described inTable I), leading to F-measures close to zero for those cases.
The impact of F0 and onset time tolerance on F
onsis
shown in Table VI. With a 50 cent tolerance (corresponding
to a standard semitone-scale transcription tolerance) theF-measure reaches 66.95%. This indicates that the proposed
system is indeed successful at multi-pitch detection, and thata substantial part of the errors stems from detecting pitches
at a precise pitch resolution.
In order to demonstrate the need for using instrument-
speciﬁc templates for AMT, comparative experiments were
made using piano templates extracted from three piano models
taken from the MAPS database ( Emiya et al. , 2010 ). Using
the piano templates, the system reached F
ons¼53:28%, indi-
cating that a performance decrease occurs when templates are
applied that do not match the timbral properties of the sourceinstruments (cf. Table V). This best performance with piano
templates was obtained for the tanbur recordings (which might
be attributed to those instruments having similar excitation
and sound production); the ney recording performance wasclose to the average (53.4%), while the worst performance (of
51.2%) is observed for the ensemble recordings.
The impact of system sub-components can also be seen
by disabling the “ensemble detection” procedure, which
leads to an F-measure of 51.94% for the ensemble pieces,
corresponding to about 5% decrease in performance. Byremoving the minimum duration pruning process, thereported F-measure with manually annotated tonic is
54.54%, which is a performance decrease of about 2%.
Finally, by disabling the sub-component which deletes noteevents that occur more than 1700 cents or less than /C0500
cents from the tonic, system performance drops to 54.55%;
this decrease is more apparent for the ensemble pieces(which were performed in an octave unison, spanning awider note range), leading to an F-measure of 51.45%.
C. Results—singing transcription
For transcribing the vocal dataset, evaluations were also
performed using the automatically detected and manuallyannotated tonics. The dictionary used for transcribing vocals
consisted of a combination of vocal, ney, and tanbur
templates.
Results are shown in Table VII; as with the instrumental
dataset, there is a drop in performance (7% in terms of F
ons)
when using the automatically detected tonic. Performance isquite consistent across all recordings, with the best perform-
ance of F
ons¼72:2% achieved for recording No. 4 from
FIG. 8. (Color online) Excerpts from an ensemble transcription: Piece 5
from Table I, F-measure: 42.3%. The pitch axis is normalized to have the
tonic frequency at 0 cent. The log-frequency spectrogram is depicted, over-
laid with the automatic transcription as crosses, and the reference annotation
indicated by black rectangles, framed by white color for better visibility.
Width and height of the black rectangles are conﬁned to an allowed toler-
ance of 100 ms and 20 cents.
TABLE V. Instrumental transcription results using various system conﬁgu-
rations, compared with state-of-the-art approaches.
System Fons
Proposed method 56.75%
Proposed method—added “vinyl” degradation 46.42%Proposed method—using piano templates 53.28%(Vincent et al. , 2010 )—20 cent evaluation 38.52%
(Vincent et al. , 2010 )—50 cent evaluation 49.84%
YIN ( de Cheveign /C19e and Kawahara, 2002 ) 51.71%TABLE VI. Instrumental transcription results (in Fons) using different F0
and onset tolerance values.
F0 tolerance 10 cent 20 cent 30 cent 50 cent
Fons 38.90% 56.75% 62.68% 66.95%
Onset tolerance 50 ms 100 ms 150 ms 200 ms
Fons 42.75% 56.75% 60.66% 62.95%
TABLE VII. Singing transcription results using manually annotated and
automatically detected tonic.
Pons Rons Fons
Manually annotated 39.70% 44.71% 40.63%
Automatically detected 33.71% 36.53% 33.41%
J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel 2127

## Page 11

Table IIand the worst performance of Fons¼21:2% for
recording No. 1 (which suffers from poor recording quality).
When using only vocal templates, system performance
reaches Fons¼34:8%, while when using only the instru-
mental templates an F-measure of 39.5% is achieved. Thisindicates that the instrumental templates contribute more tosystem performance than the templates extracted from thevocal training set, although including the vocal templatesleads to an improvement over using only the instrumentaltemplates. For comparison, using the multi-pitch detectionmethod of Vincent et al. (2010) as in Sec. VB, with 20 cent
tolerance yields F
ons¼22:8%, while 50 cent tolerance gives
Fons¼36:6%.
In general, these results indicate the challenge of
transcribing mixtures of vocal and instrumental music, inparticular, in cases of historic recordings. However, theresults are promising, and indicate that the proposed systemcan successfully derive transcriptions from vocal and instru-mental ensembles, which can serve as a basis for ﬁxingtranscription errors in a user-informed step. Detailed discus-sion on the instrumental and vocal systems will be made inSec.VI.
VI. DISCUSSION
The results obtained from the proposed AMT system indi-
cate lower performance for vocal pieces compared to resultsfor instrumental recordings. As pointed out in Sec. III C,t h e
recording quality of the vocal recordings is generally lowerthan the quality of most instrumental performances, which isreﬂected in a higher noise level and the absence of high-frequency information due to low-quality analog-to-digitalconversion. In order to assess the impact of the low recordingquality, an informal experiment was carried out, in which sixnew vocal recordings were chosen for transcription. Since forthose recordings no time-aligned reference pitch annotationsexist, a qualitative evaluation was performed by an aural com-parison of an original vocal recording with a synthesizer play-back of a transcription of the recording. This experiment didnot indicate a clear improvement of vocal transcription for thenewer recordings.
An insight can be obtained into what was identiﬁed as
the main reason for the low transcription performance forvocal pieces by comparing the depicted spectrograms inFigs. 9(a)and9(b). The instrumental example in Fig. 9(a)is
characterized by pitch that remains relatively stable for theduration of a note, and by note onsets that can be identiﬁedby locating changes in pitch. However, the vocal example inFig.9(b)is completely different. Here, the pitch of the voice
is clearly distinguishable but characterized by a widevibrato. For instance, in the downward movement starting atabout 170 s, the notation contains a progression through sub-sequent notes of the H €uzzam-makam scale, which appears in
the singing voice with a vibrato of the almost constant rangeof ﬁve semitones. Such characteristics are typical of Turkishvocal performances, and it seems hard to imagine a methodbased purely on signal processing that could correctly inter-pret such a performance in terms of the underlying impliednote sequence. It is an open question whether this difﬁcultyof transcribing vocal performances is unique to this form of
music, or if AMT systems would exhibit similar perform-ance deﬁcits for other styles of music as well. Based on our
own observations of musical practice in Turkey, instrumen-
tal music education more frequently explains ornamentationsin terms of notes than in vocal education, where teacherstend to teach ornamentations such as the vibrato in Fig. 9(b)
purely in terms of performance demonstrations.
One aspect important to point out is that the system
performance values displayed in Sec. Vcontain an over-
pessimistic bias. As explained in Sec. II, Turkish makam
music practice deviates from the pitch values implied by
notation, due to a mismatch between theory and practice.However, our reference annotations contain pitch valuesthat are following the most common theoretical framework
to explain the tonal concepts of Turkish makam music,
while the performances contain pitches that will deviatefrom the theoretical values at least for some cases. Forinstance, the step from the tonic to the fourth note in makam
Segah is usually notated as a perfect fourth. However,
within performances this interval tends to be larger becausethe tonic is typically played (by instruments) at a lowerpitch. For piece 10 in Table I, a clear increase of this inter-
val compared to the annotated one is observed. For this
piece, correcting this interval from 500 to 530 cents changesthe F-measure from 30.6% to 39.7%, a substantial improve-ment. Similar phenomena are very likely to occur for other
pieces, but a systematic evaluation would require manual
correction of all individual pitch values in our referenceannotations.
FIG. 9. (Color online) Excerpts from transcriptions. Axes and symbols fol-
low the principle of Fig. 8.
2128 J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel

## Page 12

VII. CONCLUSIONS
In this paper, a system for transcribing microtonal
makam music of Turkey is proposed, based on spectrogram
factorization models relying on pre-extracted spectral tem-
plates per pitch. A collection of instrumental and vocalrecordings was compiled and annotated, and evaluation met-
rics suitable for microtonal transcription were proposed.
Results show that the system is able to transcribe both instru-mental and vocal recordings with variable accuracy rangingfrom approximately 40% to 60% for 20 cent resolution,
depending on several factors. Results are substantially better
using manually determined tonic values as compared with anautomatic method. We also observed a discrepancy between
music theory and practice, as observed through the reference
pitch annotations that followed a theoretical framework. Thecode for the proposed system is available online.
6
A logical extension of this work is to combine acoustic
models with music language models suitable for microtonaland heterophonic music, in order to both improve transcrip-
tion performance and quantify the gap between theory and
practice in Turkish makam music. Finally, following work inBenetos and Dixon (2013) , another suggested extension is to
annotate the various sound states observed in typical Turkish
makam music instruments (such as attack, sustain, decay),
which the authors believe will result in a more robust andaccurate AMT system for microtonal music.
ACKNOWLEDGMENTS
The authors would like to thank Baris ¸ Bozkurt for his
advice and for providing us with software tools, as well asRobert Reigle and Simon Dixon for proofreading. E.B. was
supported by a Royal Academy of Engineering Research
Fellowship (RF/128) and by a City University LondonResearch Fellowship. A.H. was supported by a Marie Curie
Intra European Fellowship (Grant No. PIEF-GA-2012-
328379).
1Term used to avoid the misleading dichotomy of Western and non-
Western music, proposed by Reigle (2013) .
2The term “polyphony” in the context of AMT does not necessarily refer to
a polyphonic style of composition. It rather refers to music signals that
contain either several instruments, or one instrument that is capable ofplaying several individual melodic voices at the same time, such as the
piano. On the other hand, “monophonic” refers to signals that contain one
instrument that is capable of playing at most one note at a time (e.g., flute).
The two terms are used with this technical interpretation in the paper.
3http://compmusic.upf.edu (Last viewed August 6, 2015).
4http://www.sonicvisualiser.org/ (Last viewed August 6, 2015).
5Please follow the links provided at http://www.rhythmos.org/
Datasets.html (Last viewed August 6, 2015) in order to obtain the annota-
tions as two archives. Lists that identify all performances using their
MusicBrainz ID (musicbrainz.org) or a YouTube-link if no ID is available,are included.
6Code for proposed system: https://code.soundsoftware.ac.uk/projects/
automatic-transcription-of-turkish-makam-music (Last viewed August 6,
2015).
Abraham, O., and von Hornbostel, E. M. ( 1994 ). “Suggested methods for
the transcription of exotic music,” Ethnomusicology 38, 425–456 [origi-
nally published in German in 1909: “Vorschl €age f €ur die Transkription
exotischer Melodien”].
Anderson Sutton, R., and Vetter, R. R. ( 2006 ). “Flexing the frame in
Javanese gamelan music: Playfulness in a performance of LadrangPangkur,” in Analytic Studies in World Music , edited by M. Tenzer
(Oxford University Press, Oxford, UK), Chap. 7, pp. 237–272.
Arel, H. S. ( 1968 ).T€urk Musikisi Nazariyat i (The Theory of Turkish Music )
(H€usn€utabiat matbaas i, Istanbul, Turkey), Vol. 2.
Bay, M., Ehmann, A. F., and Downie, J. S. ( 2009 ). “Evaluation of multiple-
F0 estimation and tracking systems,” in International Society for Music
Information Retrieval Conference , Kobe, Japan, pp. 315–320.
Benetos, E., Cherla, S., and Weyde, T. ( 2013a ). “An efﬁcient shift-
invariant model for polyphonic music transcription,” in 6th International
Workshop on Machine Learning and Music , Prague, Czech Republic,
pp. 7–10.
Benetos, E., and Dixon, S. ( 2013 ). “Multiple-instrument polyphonic music
transcription using a temporally-constrained shift-invariant model,”J. Acoust. Soc. Am. 133, 1727–1741.
Benetos, E., Dixon, S., Giannoulis, D., Kirchhoff, H., and Klapuri, A.
(2013b ). “Automatic music transcription: Challenges and future
directions,” J. Intell. Inf. Syst. 41, 407–434.
Benetos, E., and Holzapfel, A. ( 2013 ). “Automatic transcription of Turkish
makam music,” in International Society for Music Information Retrieval
Conference , Curitiba, Brazil, pp. 355–360.
Bozkurt, B. ( 2008 ). “An automatic pitch analysis method for Turkish
maqam music,” J. New Mus. Res. 37, 1–13.
Bozkurt, B., Ayangil, R., and Holzapfel, A. ( 2014 ). “Computational analysis
of makam music in Turkey: Review of state-of-the-art and challenges,”J. New Mus. Res. 43, 3–23.
Brown, J. C. ( 1991 ). “Calculation of a constant Q spectral transform,”
J. Acoust. Soc. Am. 89, 425–434.
Brown, S. ( 2007 ). “Contagious heterophony: A new theory about the origins
of music,” Musicae Scientiae 11
, 3–26.
Bunch, P., and Godsill, S. ( 2011 ). “Point process MCMC for sequential
music transcription,” in International Conference on Acoustical Speech
and Signal Processing , Prague, Czech Republic, pp. 5936–5939.
Cooke, P. ( 2001 ). “Heterophony,” Oxford Music Online, Grove Music
Online, http://grovemusic.com/ (Last accessed August 6, 2015).
Davy, M., Godsill, S., and Idier, J. ( 2006 ). “Bayesian analysis of western
tonal music,” J. Acoust. Soc. Am. 119, 2498–2517.
de Cheveign /C19e, A. ( 2006 ). “Multiple F0 estimation,” in Computational
Auditory Scene Analysis, Algorithms and Applications , edited by D. L.
Wang and G. J. Brown (IEEE Press/Wiley, New York), pp. 45–79.
de Cheveign /C19e, A., and Kawahara, H. ( 2002 ). “YIN, a fundamental fre-
quency estimator for speech and music,” J. Acoust. Soc. Am. 111,
1917–1930.
Dempster, A. P., Laird, N. M., and Rubin, D. B. ( 1977 ). “Maximum likeli-
hood from incomplete data via the EM algorithm,” J. R. Stat. Soc. 39,
1–38.
Dessein, A., Cont, A., and Lemaitre, G. ( 2010 ). “Real-time polyphonic
music transcription with non-negative matrix factorization and beta-divergence,” in International Society for Music Information Retrieval
Conference , Utrecht, Netherlands, pp. 489–494.
Dixon, S., Mauch, M., and Tidhar, D. ( 2012 ). “Estimation of harpsichord
inharmonicity and temperament from musical recordings,” J. Acoust. Soc.
Am. 131, 878–887.
Emiya, V., Badeau, R., and David, B. ( 2010 ). “Multipitch estimation of
piano sounds using a new probabilistic spectral smoothness principle,”IEEE Trans. Audio, Speech Lang. Proc. 18, 1643–1654.
Erkut, C., Tolonen, T., Karjalainen, M., and V €alim€aki, V. ( 1999 ). “Acoustic
analysis of Tanbur, a Turkish long-necked lute,” in International
Congress on Sound and Vibration (IIAV ), pp. 345–352.
Fuentes, B., Badeau, R., and Richard, G. ( 2013 ). “Harmonic adaptive latent
component analysis of audio and application to music transcription,”IEEE Trans. Audio Speech Lang. Proc. 21, 1854–1866.
Houtsma, A. ( 1968 ). “Discrimination of frequency ratios,” J. Acoust. Soc.
Am. 44, 383.
Karaosmano /C21glu, K. ( 2012 ). “A Turkish Makam music symbolic database for
music information retrieval: Symbtr,” in International Society for Music
Information Retrieval Conference , Porto, Portugal, pp. 223–228.
Kirchhoff, H., Dixon, S., and Klapuri, A. ( 2013 ). “Missing template estima-
tion for user-assisted music transcription,” in International Conference on
Acoustical Speech and Signal Processing , Vancouver, Canada, 26–30.
Klapuri, A., and Davy, M. ( 2006 ).Signal Processing Methods for Music
Transcription (Springer-Verlag, New York).
Lee, K. ( 1980 ). “Certain experiences in Korean music,” in Musics of Many
Cultures: An Introduction , edited by E. May (University of California
Press, Oakland, CA), pp. 32–47.
J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel 2129

## Page 13

Macrae, R., and Dixon, S. ( 2010 ). “Accurate real-time windowed time
warping,” in International Society for Music Information Retrieval
Conference , Utrecht, Netherlands, pp. 423–428.
Mauch, M., and Ewert, S. ( 2013 ). “The audio degradation toolbox and its
application to robustness evaluation,” in International Society for Music
Information Retrieval Conference , Curitiba, Brazil, pp. 83–88.
MIREX ( 2007 ). “Music Information Retrieval Evaluation eXchange
(MIREX),” http://music-ir.org/mirexwiki/ (Last accessed August 6, 2015).
N e s b i t ,A . ,H o l l e n b e r g ,L . ,a n dS e n y a r d ,A .( 2004). “Towards automatic tran-
scription of Australian aboriginal music,” in Proceedings of the 5th
International Conference on Music Information Retrieval , Barcelona, Spain.
Racy, A. J. ( 2003 ).Making Music in the Arab World: The Culture and
Artistry of Tarab (Cambridge University Press, Cambridge, UK), Chap.
Heterophony, pp. 80–96.
Rigaud, F., David, B., and Daudet, L. ( 2013 ). “A parametric model and esti-
mation techniques for the inharmonicity and tuning of the piano,”
J. Acoust. Soc. Am. 133, 3107–3118.Reigle, R. ( 2013 ). (personal communication).
Seeger, C. ( 1958 ). “Prescriptive and descriptive music-writing,” Music
Quart. 64, 184–195.
Smaragdis, P. ( 2009 ). “Relative-pitch tracking of multiple arbitary sounds,”
J. Acoust. Soc. Am. 125, 3406–3413.
Smaragdis, P., Raj, B., and Shashanka, M. ( 2006 ). “A probabilistic
latent variable model for acoustic modeling,” in Advances in
Models for Acoustic Processing Workshop (NIPS’06 ), Whistler,
Canada.
Stock, J. P. J. ( 2007 ). “Alexander j. Ellis and his place in the history of eth-
nomusicology,” Ethnomusicology 51, 306–325.
Thompson, W. F. ( 2013 ). “Intervals and scales,” in The Psychology of
Music , edited by D. Deutsch (Elsevier, Amsterdam, the Netherlands),
Chap. 4.
Vincent, E., Bertin, N., and Badeau, R. ( 2010 ). “Adaptive harmonic spectral
decomposition for multiple pitch estimation,” IEEE Trans. Audio Speech
Lang. Process. 18, 528–537.
2130 J. Acoust. Soc. Am. 138(4), October 2015 Emmanouil Benetos and Andr /C19e Holzapfel

