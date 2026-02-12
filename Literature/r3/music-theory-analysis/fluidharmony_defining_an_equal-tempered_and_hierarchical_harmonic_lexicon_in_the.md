# FluidHarmony: Defining an equal-tempered and hierarchical harmonic lexicon in the Fourier space

**Author:**   
**Subject:**   
**Total Pages:** 21  
**Source File:** `a (4).pdf`

---

## Page 1

Journal of New Music Research
ISSN: (Print) (Online) Journal homepage: www.tandfonline.com/journals/nnmr20
FluidHarmony: Deﬁning an equal-tempered and
hierarchical harmonic lexicon in the Fourier space
Gilberto Bernardes, Nádia Carvalho & Samuel Pereira
To cite this article: Gilberto Bernardes, Nádia Carvalho & Samuel Pereira (2022) FluidHarmony:
Deﬁning an equal-tempered and hierarchical harmonic lexicon in the Fourier space, Journal of
New Music Research, 51:2-3, 142-161, DOI: 10.1080/09298215.2023.2202641
To link to this article:  https://doi.org/10.1080/09298215.2023.2202641
© 2023 The Author(s). Published by Informa
UK Limited, trading as Taylor & Francis
Group
View supplementary material 
Published online: 16 Jun 2023.
Submit your article to this journal 
Article views: 829
View related articles 
View Crossmark data
Citing articles: 1 View citing articles 
Full Terms & Conditions of access and use can be found at
https://www.tandfonline.com/action/journalInformation?journalCode=nnmr20

## Page 2

JOURNALOFNEWMUSICRESEARCH
2022,VOL.51,NOS.2–3,142–161https://doi.org/10.1080/09298215.2023.2202641
FluidHarmony: Defining an equal-tempered and hierarchical harmonic lexicon in
the Fourier space
Gilberto Bernardesa,b, Nádia Carvalhoa,band Samuel Pereiraa,b
aUniversityofPorto–FacultyofEngineering,Porto,Portugal;bINESCTEC,Porto,Portugal
ABSTRACT
FluidHarmony is an algorithmic method for defining a hierarchical harmonic lexicon in equal tem-
peraments. It utilizes an enharmonic weighted Fourier transform space to represent pitch class set(pcsets) relations. The method ranks pcsets based on user-defined constraints: the importance ofinterval classes (ICs) and a reference pcset. Evaluation of 5,184 Western musical pieces from the 16thto 20th centuries shows FluidHarmony captures 8% of the corpus’s harmony in its top pcsets. Thishighlights the role of ICs and a reference pcset in regulating harmony in Western tonal music whileenabling systematic approaches to define hierarchies and establish metrics beyond 12-TET.ARTICLE HISTORY
Received26October2021
Accepted5April2023
KEYWORDS
Harmony;discreteFouriertransform;pitchclasssets;
intervalclasses;lexicon
1. Introduction
W e s t e r na r tm u s i ci st y p i c a l l yt a u g h ta sas e to fp r i n c i -
ples emerging from the common-practice tonal musicperiod. These principles have been systematizred in thelargeplethoraofmusicaltreatises(Huron, 2016;Susanni
& Antokoletz, 2012), which define whatmusical objects
shouldbeadoptedand howtheyexistandrelateintime.
Typically,thejourneycommenceswiththestudyofmul-tiple constructs at different hierarchies, such as scales,intervals,andprototypicalchords.Oncetheseconstructsaremastered,functionalharmonyisstudied,whichulti-mately dictates pitch relations and harmonic motion.In what follows, we adopt a long-standing linguisticmetaphor (Swain, 1997) to refer to multiple constructs
and functional harmony as the lexicon
1and syntax of a
musicalgrammar,respectively.
Throughout the common practice period, roughly
from mid-seventeenth to late-nineteenth centuries, theWesterntonalmusiclexiconandsyntaxremainedrootedin the same fundamental principles (Aldwell et al.,
CONTACT GilbertoBernardes gba@fe.up.pt UniversityofPorto–FacultyofEngineering,RuaDr.RobertoFrias,4200-465Porto,Portugal;INESCTEC,
RuaDr.RobertoFrias,4200-465Porto,Portugal
Supplementaldataforthisarticlecanbeaccessedhere. https://doi.org/10.1080/09298215.2023.2202641
1Wewilloftenusethetermlexicon,awordpertainingtolinguistics,asametaphoricalmanifestationinmusic.Inlinguistics,lexiconisusedtodesc ribetheentire
set of words from a language to which meaning is attributed. A direct parallel in music can lead to the understanding of a harmonic lexicon as all possibl e
combinationsofpitch.However,withinthescopeofthisarticle,asinrelatedliterature,thetermisunderstoodasavariableandrelativelysmallg roupofpitch
classsetsthatestablishtheprimalharmonicmaterialtobeusedinagivencontext(e.g.,acompositionoramovement).
2It is certain that many of these new composition systems, such as integral serialism, have sought a highly democratic use of diﬀerent pitch classes and even
musicalelementssuchasrhythmordynamics.However,othercomposersofthe20thand21stcenturiesseekahierarchicaluseofpitches,whichreinfor cesthe
needtoproposeasystemthatassiststhecomposerindeﬁningthesehierarchies.2018; Rohrmeier & Pearce, 2018). In the twentieth cen-
tury, the fundamentals of the common practice havebeen criticised, disrupted, and expanded to a degreewithout historical precedent.
2Representative examples
are the emancipation of the dissonance (Parncutt &hair,2011;T e n n e y ,1988) and the rise of a myriad
of individual harmonic systems replacing the prevail-ing functional tonality (Persichetti, 1961) .T h er i s eo f
novelty as an aesthetic value impelled composers todesign new harmonic systems at an unprecedented rate.Thereupon, new harmonic treatises have been writtenby music composers and theorists. Notable examples
include Messiaen’s ( 1944)La technique de mon langage
musical, Schoenberg’s twelve-tone technique (Simms,
2000), Forte’s (1973) set theory, and Perle’s ( 1977)
twelve-tonetonality.
Equal-tempered divisions of the octave beyond the
traditional 12-tone equal temperament (TET) have also
been explored to a great extent. The 24-TET divisionhas been of interest to twentieth-century composers
©2023TheAuthor(s).PublishedbyInformaUKLimited,tradingasTaylor&FrancisGroup
ThisisanOpenAccessarticledistributedunderthetermsoftheCreativeCommonsAttributionLicense( http://creativecommons.org/licenses/by/4.0/ ),whichpermitsunrestricteduse,
distribution, and reproduction in any medium, provided the original work is properly cited. The terms on which this article has been published allow the posting of the AcceptedManuscriptinarepositorybytheauthor(s)orwiththeirconsent.

## Page 3

JOURNAL OF NEW MUSIC RESEARCH 143
such as Julián Carrillo, Ben Johnston, Harry Partch,
Horat¸iu Rădulescu, Karlheinz Stockhausen, James Ten-
ney,IvanWyschnegradsky,andLaMonteYoung(Anders&Miranda, 2010).Asthesemultipletuningsandsonori-
ties find their way into composition, a vast unchartedmusicalterritoryisavailabletocomposers.
C o m p u t a t i o nt o o l sp l a yav i t a lr o l ei nn a v i g a t i n gt h i s
unfamiliarlandscapeintwoprominentdirections.First,soundsynthesismethods,notablyinthedigitaldomain,fostertheauralexplorationofanytuningsystem.Second,the computer-aided algorithmic composition (CAAC)methodsupportsthedefinitionofhierarchicalharmonicconstructs.Existingsystemstypicallyaddressbothareas.Representative software includes Csound (Boulanger,2000),SuperCollider(McCartney, 2002),Max(Puckette,
2002),BachandCagelibrariesfortheM axen vironmen t(Ghisi & Agostini, 2017), Pure Data (Puckette, 1996),
OpenMusic and PWGL (Assayag et al., 1999;L a u r s o n
et al.,2009), JMSL (Didkovsky & Burk, 2001;P o l a n -
sky et al., 1990), Common Music (Taube, 1997), and
Strasheela(Anders&Miranda, 2010).
Comprehensivemusictheoriesbeyondthe12-TETare
challengingtomodelwiththeabovesystems;rather,theyfocus primarily on scales’ definition. Strasheela (Anders&M i r a n d a , 2010) is a notable exception, which applies
constraint programming to define higher-level pitch-related concepts such as chords and scales from user-defined relations between pitch, pitch classes, and chordorscaledegrees.Theformalisationoftheapproachtack-les the problem of defining equal-temperament higher-levelconstructssystematically.However,theuser-drivenparameterisation as heuristic constraints is arguablycomplex, defying the need for an automatic computa-tionalapproach.
In this paper, we propose FluidHarmony, a CAAC
method for defining a harmonic lexicon of pitch classsets(pcsets)inanyequal-tempereddivisionoftheoctave.The contributions of the proposed method can sup-port composers in (1) prescribing a harmonic lexiconof pcsets within a given composition context at multiplehierarchies(orcardinalities);(2)establishingaharmonic
hierarchyaccordingtotwouser-definedconstraintsreg-
ulating the interval content and the pcset region of thelexicon; (3) exploring a wide array of harmonic spacesin any number of p-tone subdivisions of the octave; (4)
guidingthecompositionprocessthroughprovidingauralfeedback as well as topological and mathematical hier-a r c h i c a lr e p r e s e n t a t i o n st h a te m e r g ef r o mt h eF o u r i e rrepresentationalspace.
FluidHarmony computes a lexicon of pcsets in an
equal-tempered, enharmonic Fourier space resultingfrom the discrete Fourier transform (DFT) of pcsets(Amiot,2016;L e w i n , 1959,2001;Q u i n n ,2006, 2007).Mathematically, this framework is similar to the appli-cation of the DFT on audio signals. However, the signalspace should be interpreted as the pitch class circle, andthesignalitselfastheweightsgiventothepitchclassesinaset(Yust, 2019).F o raco m p r ehensivepedagogyo nthe
application and interpretation of the DFT to pitch classdistribution, please refer to Amiot (2016 ), Noll (2019),
and Yust ( 2015b). The latter space has been shown to
capture and quantify musical theoretical principles withunforeseenaccuracyinvoice-leading(Tymoczko, 2008),
tonal regions modeling and subset structure (Bernardeset al.,2016,2017;Y u s t ,2015a, 2015b), and the study
of tuning systems (Amiot, 2016; Callender, 2007). Two
properties of the Fourier space relevant to our methodare the possibility of capturing interval class
3(IC) and
commonpitchclassrelationsfrommetricsintheFouriermagnitude and phase, respectively. Both magnitude andphase can be independently defined, fostering a methodwhere a pcset lexicon results from the intersection of areference set of pitch classes (or a vector defining the
importanceofeachpitchclass)withareferenceICvector
imposingtheimportanceofintervals.
Underlying our method lies an original contribution
thatenablesthealgebraicdefinitionofweightstoregulatethe importance of ICs in the Fourier magnitude space.Furthermore,apcsetintheweightedFourierspace, T(k),
exists in a limited space due to its L
2normalisation by
cardinality,allowingpcsetswithdifferentcardinalities(ormultiplehierarchies,suchasnotes,chords,andscales)toberepresentedandcompared(Bernardesetal., 2016).
After populating the weighted Fourier space with all
unique pcsets, within 1 ≤t≤pcardinality, where p∈
Z+standsasthenumberofequal-tempereddivisionsof
theoctave,aharmoniclexiconisdefinedasthecombina-tionoftwospatialconstraintstobemaximised:(1)pcsetmagnitude and (2) phase similarity to a reference pcsetR, as illustrated in Figure 1. Larger pcset magnitudes
indicategreatercompliancetotheuser-definedICdistri-bution. Phase (or cosine) similarity to a reference pcsetindicates greater compliance to a user-defined region.From the resulting harmonic lexicon and its underlying
(magnitudeandphase)metrics,weproposethreehierar-
chicalrepresentationsofpitchstructuresinspiredbytheconcept of event hierarchy by Bharucha ( 1984a,1984b)
– a cognitive pitch theory that aims at tackling somelimitations on the prevailing tonal pitch models withincognitive psychology (Krumhansl, 1979;L e r d a h l , 1988;
3The concept of IC, also known as unordered pitch-class interval, has been
coined within musical set theory (Forte, 1973) and extensively applied in
atonal music to denote the smallest (interval) distance in the pitch class
spacebetweentwounorderedpitchclasses.Forexample,theintervalclass
between pitch classes 0 and 7 is IC5 as 0 −7=−7≡−7(mod12)=5i s
smallerthan7 −0=7,yetitaccountsforboththecomplementaryintervals
ofperfectfourthandﬁfth.

## Page 4

144 G. BERNARDES ET AL.
Figure 1. Caption:Illustrationofapcsetlexicondeﬁnitioninﬁfth
Fourier coeﬃcient of Z12, particularly relevant for tonal music.
Allpitchclassesarerepresentedinthecirclealongwiththreetri-
ads,onebeingthereferencepcset R={0,4,7},highlightedbyan
orangedirectionalvector.Stablepcsetsoccupythedarkershadedareas, which result from two main constraints: (1) larger mag-nitude values – i.e. the area close to the circumference, and (2)
similarphasetoareferencepcset R.Pleasenotetheproximityof
thepcset {0,5,9}toR,asopposedtothepcset {1,5,8 }–thetrans-
positionof Rbyasemitone,whichinthecontextoftonalmusicisa
verydistanttriadto R.Furthermore,intheneighbourhoodof R,we
can ﬁnd its component pitch classes along with related diatonic(andconsonant)pitchclasses.
Longuet-Higgins, 1987;Shepard, 1982).4Ourthreehier-
archiesdefine(1)apcsetrankingdenotingtheharmonic
stabilityofeachpcsetinthelexicon;(2)atopologicalrep-resentation of the Fourier (phase) space exposing pitch
class retention between pcsets; and (3) a ‘well-formed’
andstratifiedspaceincludingpcsetsofmultiplecardinal-ities,followinganearlierproposalbyLerdahl( 2001).
We evaluate our research by conducting a systematic
assessment of the FluidHarmony method’s effectivenessin eliciting the lexica of a large corpus from Westernart music. Our expectation is that both constraints are
4A leading theory on tonal hierarchies is by Krumhansl ( 1979), which focus
oncyclicpropertiesofmusicalintervalswithintheoctave.Hertonalhierar-
chytheorydepictsthetonicasthemoststabletoneandtheﬁfthandthirdsconsonantmembersofthemajordiatonicsetasthenext-moststable.Theremainingtonesinthediatonicsetarelessstable,andnon-diatonicmem-
bers are deemed least stable. Despite its remarkable explanation of tonal
phenomena, Krumhansl’s (1979 ) theory fails to explain essential phenom-
ena from tonal music composition practice, such as temporal phenomena,
andevenlesswhenappliedtoatonaloranyequaltemperamentotherthan
the 12-TET. Please refer to Butler (1990 ) for a detailed critique of the tonal
hierarchy.fundamentaltothelexiconformationandtheFluidHar-
mony ranked lexica mirror the Western music practice.By validating the proposed method in regulated prac-tices, we aim to veridically assess how well the modelcaptures existing musical practices and foster the explo-ration of less systematized harmonic systems, namelytuningsystemsbeyond12-TET.
The remainder of this paper is structured as follows.
Section2reviews the musictheoretical value of the DFT
of pcsets by unpacking information from the Fouriermagnitude and phase. Section 3introduces the mathe-
maticaldefinitionofanICweightedFourierspace,wherea pcset’s magnitude informs its compliance to a user-defined IC distribution. Section 4details the definition
ofaharmoniclexiconasspatialconstraintsinaweightedFourierspace.Section 5proposesthreehierarchicalpitch
representations:arankedpitchstabilityhierarchy,atopo-logical common pitch class space, and a well-formedstratification space. Section 6presents the evaluation
of our FluidHarmony system in eliciting the harmonic
lexica of a large corpus of Western art music. Finally,
Section7presents the conclusions of our study, particu-
larlyunveilingthecompositionalimplicationsofourFlu-idHarmonymethod,pointingtowardsthefutureendeav-oursoftheresearch.
2. The discrete Fourier transform of
equal-tempered pitch class sets
From the allusion to the DFT within the context of
Lewin’sintervalfunctionorIFUNC–catalogingthetypeand number of directed pitch class intervals betweentwo pcsets (Lewin, 1959)–and the fundamental work of
Quinn (2004) on the study of the DFT magnitude for
musicanalysis,itcametobeknownthattheFourierspace
elicitsmanypropertiesofmusic-theoreticvalue.
T om a pap c s e ti n t ot h eF o u r i e rs p a c e ,w efi r s tc r e -
ate a pcset distribution, c(n),wh er en =p(p∈
Z+),i.e.
ad i s t r i b u t i o nw i t h nelements or the number of equal-
tempered divisions of the octave. The distribution c(n)
is then normalised to unit sum ( L2norm), ¯c(n).T h e
adoptionof L2normfostersametricalspacewheremulti-
pleharmonichierarchiesorpcsetsofanycardinalitycan
be interpreted and compared. Finally, we apply Eq. 1 tocomputeitsDFT, T(k),suchthat:
T(k)=N−1/summationdisplay
n=0¯c(n)e−j2πkn
N,k∈Z
with ¯c(n)=/braceleftBigg
c(n)
/bardblc(n)/bardbl,
c(n),if/bardblc(n)/bardbl>0
otherwise(1)

## Page 5

JOURNAL OF NEW MUSIC RESEARCH 145
Figure 2. Caption: Representations of the {0,3,6}pcset as a distribution in the pitch class space (left images) and the Fourier space
(rightimages).Examples(a)and(b)projectthesamepcsetin12-and7-TET.Dashed(red)linesindicatethe T(k)propertyasaconvex
combinationofpitchclasscomponents.
whereN=p, i.e., the number of elements of the pcset
distribution,and kisanintegernumbersetto1 ≤k≤p
2
forT(k),representingeachoftheDFTcoefficients.Inthe
Fourier space, ap
2-element complex vector correspond-
ingtothe1 ≤k≤p
2DFTcoefficientsisadopted.Thefirst
DFTcoefficient, T(0),exposingthecardinalityofapcset,
andallremainingsymmetricalcoefficientsareexcluded.5
Figure2shows the pcset distribution and the DFT of
the{0,3,6}triad in both Z12andZ7. To plot the mul-
tidimensional DFT of pcsets, we follow a visualisation
strategyadoptedinHarteetal.( 2006)andBernardesetal.
(2016),whichmapseachCartesian(realandimaginary)complexnumberpercoefficienttothe x-andy-axis.Fur-
t h e r m o r e ,e a c hc o e ffi c i e n tl o c a t i o nc a na l s ob ed e fi n e din vector magnitude and angle by converting them topolar coordinates. Typically, in related music theory lit-erature, the latter coordinate system is adopted (Amiot,2013,2016;Q u i n n , 2004;Y u s t , 2015a,2015b). Further-
more, relations among pcsets, typically computed andquantifiedbydistanceorsimilaritymetrics,areaddressed
5Whenperformingan N-pointDFTonapcsetdistribution,an Nseparatecom-
plexDFToutputisreturned.However,onlytheﬁrst N/2+1coeﬃcientsare
independent.Theremainingcoeﬃcients T(N/2+1)toT(N−1)areconju-
gatesymmetric,thusprovidenoadditionalinformationaboutthespectrum
ofthepcset(Shannon, 1949).ineachofthemagnitudeorphasespaces,whoseinterpre-
tationwedetailnextinSections 2.1and2.2,respectively .
2.1. Fourier magnitude of pitch class sets
The magnitude of pcsets in the Fourier space, i.e. their
size,hasbeenusedtostudytheshapeofapcsetdistribu-tion as it quantifies how a given Fourier coefficient is
N
k
periodic.InterpretationsofFouriermagnitudeshavepro-motedthestudyofpcsets’intervalcontentbasedontheirtransposition-invariantrepresentation(Amiot, 2016).
The pioneering work of Quinn ( 2004) interprets the
Fourier magnitudes of pcsets on a coefficient basis.Quinn (2004) identified for each Fourier coefficient
a prototypical pcset with maximal magnitude amongremainingpcsetsofthesamecardinality,referredtoasamaximally even (ME) set.
6Furthermore, based on these
6Please note that DFT has been used to generalize a method to ﬁnd per-
fectly balanced sets in a microtonal universe that divides the octave into
any kequal parts (Milne et al., 2015). The idea of perfectly balanced sets
appears in complementarity with perfectly even sets (Clough & Douthett,
1991).Essentially,ina12-toneequaltemperamentrepresentedaroundthe
periodiccircle,anysetofequidistantpitchclasses(e.g.,thenotesofawhole-
tonescale)isa perfectly even set.Ontheotherhand,anysetofpitchclasses
whosemeanpositionisthecentreofthecircleissaidtobea perfectly bal-
ancedset(e.g., thenotesofanoctatonicscalearea perfectly balanced and
unevenset).However,thesetwoscalesare periodicinthatwhentheyhave

## Page 6

146 G. BERNARDES ET AL.
Table 1.Interpretation of Fourier coeﬃcients’ magnitude T(1)
toT(6)forZ12. Maximal event (ME) sets and interval content
(IC) per DFT coeﬃcient are identiﬁed, i.e. prototype pcsets and
complementaryintervalswithmaximalmagnitude.Forenhanced
readability,pcsetprototypesarepresentedintheirprimeform(i.e.
transposedtobeginon0);however,pcsetprototypescanhaveup
toptranspositions.
T(k) MEset IC Harmonicquality
T(1) 0,1 IC1 chromaticity
T(2) 0,6 IC6 dyadicityor‘quartalquality’
T(3) 0,4,8 IC4 triadicityorhexatonicity
T(4) 0,3,6,9 IC3 octatonicity
T(5) 0,5 IC5 diatonicity
T(6) 0,2,4,6,8, 10 IC2 wholetone
pcsetprototypes,Quinn( 2004)establishesanassociation
between individual DFT coefficients and ICs: T(1)↔
IC1,T(2)↔IC6,T(3)↔IC4,T(4)↔IC3,T(5)↔
IC5, andT(6)↔IC2. For example, the pcset {0,3,6,9}
inZ12is 3-periodic; therefore, its magnitude in T(4)is
maximal.7A pcset with comparatively large T(4)canbe
associatedwiththeIC3(i.e.thecomplementaryintervals
ofaminorthirdandamajorsixth),suchas {0,1,3,6,9 },
which achieves the largest value in T(4)among pcsets
withcardinality t=5.
Amiot(2017 )hascriticisedthepreviousFouriercoef-
ficient interpretation in showing that it better relates tothe harmonic quality of a particular pcset, such as itslevelofdiatonicity,octatonicity,andwhole-toneness.Forexample,considerthesets A={0,4,5}andB={0,2,4}.
Converselytopcset B,pcsetAembedsaninstanceofIC5;
therefore, we expected a larger T(5).H o w ev e r ,th em a g -
nitude of pcset BinT(5),/bardblT
B(5)/bardbl2=4i sl a r g e rt h a n
/bardblTA(5)/bardbl2=2, asT(5)in many cases do not indicate
the ‘fifthyness’ of a pcset so much as its diatonicity, andBis a more characteristic diatonic subset than A.F o ra
greaterdiscussionontheinterpretationoftheseindivid-ual coefficients, please refer to Amiot ( 2017)a n dC a l -
lender (2007). Table 1summarises the correspondence
betweenFouriercoefficients T(k)withpcsetprototypes,
ICs,andharmonicqualitiesin
Z12.
Bernardes et al. ( 2016)b u i l du p o nt h eI Ci n t e r p r e t a -
tion of the DFT magnitude to propose a Z12Fourier-
w e i g h t e dT o n a lI n t e r v a lS p a c e .Aw e i g h t sv e c t o rr e g u -lates the importance of DFT coefficients to promote aspacereflectingthehierarchyofICswithinWesterntonal
been rotated at a speciﬁc angle, they exhibit the same notes as the origi-
nalposition(Milneetal., 2015).Itturnsoutthatina12-TET,thereareonly
two geometric patterns that are perfectly balanced ,uneven, and irreducibly
periodic—[C,Eb,E,Ab,A ],and[C,Db,E,F,G,Ab,B ].However,inamicrotonaluni-
verse,thepossibilityofﬁndingsetswiththesepropertiesis,intheverylimit,inﬁnite,whichisperfectlyinlinewiththemicrotonalfacetof FluidHarmony.
7Wecanﬁndthecoeﬃcientwhereagivenperiodicintervalexistsbydividingthenumberof p-tonesubdivisionsoftheoctavebytheperiod.Inthecurrent
pcsetexample,themaximalmagnitudein T(4)resultscanbecomputedas
12/3=4.music. For example, the DFT coefficients T(5)andT(3)
associatedwithIC5andIC4havelargerweightvaluesdue
to the fundamental importance of the intervals of per-fect fourth/perfect fifth and major third/minor sixth inWestern tonal harmony. This aspect is perfectly consis-tent with the results of Yust ( 2017), which point to the
preponderance of T(5),T(3)andT(2)in tonal music,
wherethecompositionalpracticelargelyfavoursIC5,IC4a n dI C 6 ,r e s p e c t i v e l y .W ec a no b s e r v e ,b o t hi nm a j o rand minor modes, a relation between DFT coefficientssuch asT(5)<T(3)<T(2), and specifically what the
author calls the ‘tonal index’: a DFT fingerprint to tonalpiecesinwhich T(2)+T(3)−T(5)≈0(Y ust,2017).In
Bernardes et al. ( 2016), weights were computed using
a brute-force approach to convey a ranking order ofdyads and triads consonance from empirical ratings. IntheTonalIntervalSpace,theFouriermagnitudeisinter-preted as the combination of all coefficients and quanti-fiesthepcset consonance as thedegreetowhich agivenpcsetrelatestotheIC-distributionweights.
2.2. Fourier phase of pitch class sets
ThephaseofpcsetsintheFourierspace,i.e.,theirdirec-
tion, captured music theorists’ attention as it modelsaspects of tonal music with unforeseen accuracy. Con-versely to the transpositional-invariant Fourier magni-tude,highlightingrelationsbetweentheintervalcontentof pcsets, Fourier phases are sensitive to pcset trans-position and have been used to study voice-leading(Tymoczko, 2010), tonal regions and hierarchical tonal
relations (Bernardes et al., 2016,2017), and tuning sys-
tems(Amiot, 2016;Callender, 2007).
Yust (2015b,2016) presents a geometric space adopt-
ing two-coefficient phases from the
Z12DFT of pcsets.
The resulting space is a Cartesian plane representa-tion of a torus (Amiot, 2016). The Fourier phase space
/angbracketleftT(5),T(3)/angbracketrighthas been adopted to describe music of the
nineteenth and twentieth centuries (Amiot, 2013;Y u s t ,
2015a,2015b,2016). Trajectories and distances in the
resulting /angbracketleftT(5),T(3)/angbracketrightFourier phase space reflect the
usual Riemannian (dual) Tonnetze structure and unveilsubsetstructure.
Bernardes et al. ( 2016) have shown that the Fourier
phasespacecapturesrelationsacrossmultipletonalpitchhierarchies as the angular distance between two givenT
1(k)andT2(k)vectors,suchthat:
T1(k)·T2(k)=/bardblT1(k)/bardbl/bardblT2(k)/bardblcosθ.( 2 )
Diatonic sets for each region of the 24 major and minortonalitiesorthecategorical(subdominantanddominant)harmonic functions per region exist as fuzzy clusters in

## Page 7

JOURNAL OF NEW MUSIC RESEARCH 147
Figure 3. VisualisationofthemagnitudeofIC1inthe Z12Fourierspace.Foreachcoeﬃcient k,therealandimaginarypartsoftheDFT
complexnumbersareprojectedintothe x-andy-axis,respectively.
the space. These distance relationships strive from com-
mon pitch class relations that are captured by smallerangulardistances.
3. An interval content-weighted Fourier space
We propose an algebraic method to compute weightsw(k)for distorting the magnitude of the Fourier space,
such that the magnitude of ICs in the Fourier space,/bardblT
IC(k)/bardbl, equates with a user-defined IC distribution,
I,w i t hp
2elements. For example, given an IC distri-
butionI={1,2,6,8,10,4 }inZ12(where each position
defines the relative importance of an IC), /bardblTIC1(k)/bardbl
and/bardblTIC5(k)/bardblmust be equal to 1 and 10, respectively.
Conversely to the brute-force approach proposed inBernardes et al. ( 2016)t ofi n da no p t i m a ls e to fw e i g h t s
w(k)that match empirical ratings of ICs’ consonance,
weproposeanalgebraicsolutionthatdrasticallyreducesthe computational complexity involved in finding the(exact) weights w(k)that match the user-defined IC
distribution, I.
Translating the relative importance of ICs within the
p-TET space into a set of Fourier weights w(k)is a
non-trivial problem due to the ‘loose’ links betweenFourier coefficients and ICs (as previously discussed inSection2.1).WhiletheassociationbetweenICsandDFT
coefficients, shown in Table 1, denotes maximal mag-
nitude for pcsets embedding the respective IC, it doesn o th o l di nm a n yc a s e sd u et ot h ec y c l i cr e p r e s e n t a -tion of the pitch classes in each coefficient. For exam-ple, a highly chromatic pcset cluster including all 12pitch classes has zero magnitude in T(1),t h eF o u r i e r
coefficient associated with IC1. Furthermore, all coef-
ficients, irrespective of their association to a given IC,
contribute to the magnitude of /bardblT(k)/bardbl.F i g u r e3 illus-
trates the latter case by denoting the magnitude of theIC1 for coefficients kin a
Z12non-weighted Fourier
space.
As q u a r em a t r i x , MIC,kwith sizep
2can express the
FouriermagnitudeofallICspercoefficient k.Forexam-
ple,Eq.3presentsthematrixM forthe Z12Fourierspace,
whereICsandFouriercoefficients kareexpressedasrows
andcolumns,respectively .
⎛
⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎝cosπ
12cosπ
6cosπ
4cos2π
6cos5π
12cosπ
2
cosπ
6cos2π
6cosπ
2cos2π
6cosπ
6cos(0)
cosπ
4cosπ
2cosπ
4cos(0)cosπ
4cosπ
2
cos2π
6cos2π
6cos(0)cos2π
6cos2π
6cos(0)
cos5π
12cosπ
6cosπ
4cos2π
6cosπ
12cosπ
2
cosπ
2cos(0)cosπ
2cos(0)cosπ
2cos(0)⎞
⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎠(3)

## Page 8

148 G. BERNARDES ET AL.
To regulate the importance of each IC in the baseline
Fouriermagnitudespace,wecomputetheweights walge-
braically as a linear system of matrix equations, suchthat:
w=M
−1I,( 4 )
whereIisauser-definedp
2-elementdistributiondenoting
therelativeimportanceofICs.Eq.5providesanexampleforcomputingtheweights w(k)fromtheICdistribution
I={1,2,6,8,10,4 }in
Z12.
⎛
⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎜⎝cosπ
12cosπ
6cosπ
4cos2π
6cos5π
12cosπ
2
cosπ
6cos2π
6cosπ
2cos2π
6cosπ
6cos(0)
cosπ
4cosπ
2cosπ
4cos(0)cosπ
4cosπ
2
cos2π
6cos2π
6cos(0)cos2π
6cos2π
6cos(0)
cos5π
12cosπ
6cosπ
4cos2π
6cosπ
12cosπ
2
cosπ
2cos(0)cosπ
2cos(0)cosπ
2cos(0)⎞
⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎟⎠−1
×⎛
⎜⎜⎜⎜⎜⎝.1
.2
.6
.8
1
.4⎞
⎟⎟⎟⎟⎟⎠=⎛
⎜⎜⎜⎜⎜⎝−.665
.069
.579
.231.608
.099⎞
⎟⎟⎟⎟⎟⎠(5)
The resulting weights w(k)define the amount of distor-
tion applied in each coefficient kto convey the degree
of importance of the user-defined IC distribution I.T h e
magnitude of a pcset in the weighted Fourier space Vis
computed as the weighted sum of the magnitude vector
values,suchthat:
V=M/summationdisplay
k=1w(k)/bardblT(k)/bardbl,( 6)
whereM=p
2isthenumberofnon-symmetricalFourier
coefficients for Zpandw(k)are weights that adjust the
space to convey a user-driven IC distribution. The mag-nitudeVofpcsetsindicatesthelevelofcompliancetothe
user-defined IC distribution. Larger magnitude Vval-
ues indicate greater compliance to the IC distribution I.
In other words, larger magnitude values will be subset-classvectorsoftheICdistribution–i.e.setsembeddedintheICdistribution,namelythoseICwithgreaterrelativeimportanceinthedistribution.4. Fluidharmony: A method for defining a
harmonic lexicon in the Fourier space as spatialconstraints
FluidHarmony is a CAAC method that adopts the pro-
posed weighted-Fourier space to define a lexicon ofpcsetsinp-TETspaces.Theresultinglexiconisregulated
bytwoconstraintsintheFourierspacetobemaximised:(1) the magnitude Vof theT(k)vectors to compute the
qualityofpcsetsincomplyingwithauser-definedICdis-tribution Iand(2)thephasedistancetoareferencepcset
T
R(k)asthecosinesimilaritywithan ygiven Ti(k)using
E q .7t od e fi n eh o ww e l lt h ep c s e te m b e d sar e f e r e n c eregion.
C=T
1(k)·T2(k)
/bardblT1(k)/bardbl/bardblT2(k)/bardbl(7)
Figure4shows the architecture of the method, namely
its processing modules (rectangular blocks), user inputparameters,andmethodoutput.Directionalarrowsindi-catethefluxofdataacrossthemultiplecomponents.Theinput of the method includes four user-defined param-eters: (1) a p-element IC distribution I,d e fi n i n gt h e
relative importance of ICs; (2) a reference pcset Rdefin-
ing a region the lexicon occupies within the ppossible
transpositions;
8(3) a list with all cardinalities 1 ≤t≤p
to be considered in the pcsets lexicon; (4) the balanceαbetween the Fourier magnitude Vand phase Ccon-
stra in tsasafloa ting-po in tval ueinthe0 ≤α≤1ra nge,
wherezeroandoneindicatethesoleadoptionofmagni-tudeandphase,respectively,andallrealvalueswithintheintervalindicatedifferentdegreesofimportancebetweentheconstraints.Thestrengthofdefiningaharmoniclex-icon as a constraint-generation problem in the Fourierspace lies in the flexible and integrated strategy to com-puteboththecompliancetoanICandpcsetspacesusingthe magnitude Vand phase Cinformation, respectively,
and the capability to balance their importance via the α
parameter.
Once the user-defined parameters are set, all pcsets
P
icombinationswithinthe1 ≤t≤puser-definedcardi-
nalities populate the Fourier space using Eq. 1. For eachpcsetT
i(k)intheFourierspace,wecomputeitsweighted
magnitude Vi(Eq.6)andthephasetothereferencepcset
TR(k)usingthecosinesimilarity Ci(Eq.2).Theweighted
combinationofthetwometricsabovedefinesthecompli-ance to the constraints as a harmonic stability indicatorH
i,suchthat:
Hi=α·Vi+(1−α)·Ci (8)
8The{0,2,4,5,7,9,11 }∈Z12isthepcsetthatdeﬁnestheregionofCmajor,
whose12possibletranspositionscorrespondtotheregionalspaceofthe12
majorkeyswithintonalmusic.Areferencepcsetdoesnotnecessarilyimplyatonalcentre,butratherthepcsetswhichareprivileged.

## Page 9

JOURNAL OF NEW MUSIC RESEARCH 149
Figure 4. TheFluidHarmonymethod’sarchitectureincludesinput,processingmodules(asrectangularblocks),andoutput.Thearrow’s
directionindicatesthedataﬂuxacrossthemultiplecomponentsofthemethod.
Finally, the FluidHarmony method outputs a ranked list
ofpcsetsPibydecreasing Hivalues.Thelargerthevalue,
thegreaterthecompliancetotheuser-definedharmonic
l e x i c o nc o n s t r a i n t s .T h eu s e rm a k e st h es u b j e c t i v ed e c i -
sionofthenumberofpcsetsinthelexicontobeadopted.
5. Eliciting harmonic event hierarchies and
pitch-proximity relations
BasedontheFluidHarmonymetricsunderlyingourhar-
moniclexiconmethod,weproposethreerepresentationsfor defining event hierarchies
9(an implicit pitch space):
(1) a pcset ranking denoting the harmonic event stabil-ity of each pcset in the lexicon; (2) a topological repre-sentation in Fourier (phase) space exposing pitch classretention between pcsets; and (3) a stratification spacewherepcsetsofmultiplecardinalitylevelsexposea‘well-formed’ structure as proposed by Deutsch and Feroe(1981)andLerdahl( 2001).
The stability of a harmonic event can be defined by
Hin Eq. 8 and create a hierarchy of pcsets in a given
harmonic context. The underlying assumption is thatpcsets that comply with the user-defined constraintswill be predominantly adopted in a composition, thusevoking higher stability due to their larger frequencyof occurrence (Bharucha, 1984b). Naturally, harmony is
one element within the many perceptual attributes ofthemusicalsurfaceelaborationthatconveydifferentsta-bility conditions. The interaction of harmonic contentwith remaining structural elements – such as rhythmic(e.g. duration), metrical strength, and pitch height–isfundamental to the perception of the stability and thehierarchicalformationofmusicalevents.
9Eventhierarchiesresultsfrommultiplestructuralconditions,whichinclude,
tociteafew,schematicinterpretationsagainstthemajor/minortonalhier-
archies and by the events’ metrical position and frequency of occurrence(Bharucha, 1984a,b).Table2shows the 14 highest ranked pcsets with
cardinality t=3s e q u e n t i a l l yl i s t e db yt h e i rd e c r e a s -
ing value of harmonic stability Hfor three user-
input parameter conditions. Left and middle data are
inZ12, where we explore Western music archetypes
for tonal diatonic structures. It adopts as a refer-ence pcset Rthe diatonic pitch collection of C major,
R={3,0,1,0,2,1,0,2,0,1,0,1 }with the C major triad
notes (i.e. C, E, and G) reinforced in terms of impor-
tanceorstability. Moreover, the IC distribution I=
{0,0,1,1,1,0 }derives from a major/minor triad pcset,
thus equally enforcing the complementary intervals ofm3/M6, M3/m6, and P4/P5, fundamental to the tonallexicon. The difference between the first two columnsreliesonthecontributionofeachconstraintbyadoptingα=.3 (left) and α=.7 (middle). It exposes the impor-
tance of the αparameter in the resulting harmonic lexi-
con.Largervaluesof αprivilegetheuser-definedICin I,
andsmallervaluesof αenforcethepitchclasscontentof
the reference pcset R.I nT a b l e 2,t h el e f td a t ap r i v i l e g e s
the retention of the reference pcset R;t h u s ,t h eu p p e r
ranking of pcsets is predominantly in the diatonic set ofCm a j o r .C o n v e r s e l y ,t h em i d d l ed a t ae n f o r c et h eI C s I,
thus exposing an ambiguous major/minor modes tonal
centreyetdenotingastrongemphasisontriadicharmony
withintheregionofC.
The rightmost data in Table 2is in the
Z7space.
It adopts as input parameters R={3,0,1,2,1,2 },I=
{0,1,1 },and α=.3.10Thedefinitionofareferencepcset
Rand IC distribution IforZ7follows some perceptual
experimentsdonebytheauthorsandhasbeenarbitrarilychosen, without relying on any existing set. Our ratio-nale aims to promote different levels of importance to
10Pleasenotethattheinputparameters RandIareindependent.Theycanbe
derivedfromanysource,suchasapcsetorperceptualratings,anddeﬁne
therelative importance ofpitchclassesin RandICsin I,thuscanassumeany
(integerorﬂoat)value.

## Page 10

150 G. BERNARDES ET AL.
Table 2.Harmonichierarchyforthreecollectionsoftriads(i.e.cardinality t=3)inthe Z12(leftandmiddledata)and Z7(rightdata),
whoserankingresultsfromtheharmonicstabilityindicator H.T heZ12lexicaadoptdiﬀerentvaluesof αinEq .8,enf or cingeitherthe
IC(α=.4)andthepitchclassretention( α=.7).Thelexicain Z12adopt R={3,0,1,0,2,1,0,2,0,1,0,1 }and I={0,0,1,1,1,0 }.The
Z7lexiconadopts R={3,0,1,2,1,2 }distributionand I={0,1,1}.Pleasenotethatsimilarpcsetsin Z12andZ7donotadoptthesame
tuning.
pcsetin Z12α=.3Harmonicstability
H pcsetin Z12α=.7Harmonicstability
H pcsetin Z7α=.3Harmonicstability
H
0,4,7 .680 0,4,7 .872 0,3,6 .618
0,4,9 .623 0,4,9 .864 0,3,4 .526
0,3,7 .574 0,3,7 .857 0,2,3 .513
0,5,9 .574 0,5,9 .857 0,2,6 .513
4,7,11 .574 4,7,11 .857 0,4,6 .513
0,4,8 .559 0,5,8 .854 0,2,4 .462
0,5,8 .544 2,7,11 .853 0,3,5 .462
2,7,11 .538 0,3,8 .850 2,3,6 .461
0,2,7 .538 2,7,10 .850 3,4,6 .446
0,7,9 .535 4,8,11 .850 0,1,3 .446
0,4,5 .532 1,4,9 .849 0,1,6 .423
0,4,11 .532 2,5,9 .849 0,5,6 .423
0,5,7 .529 1,4,8 .847 0,2,5 .404
0,7,11 .523 2,5,10 .847 1,3,6 .404
theset,havingthepitchclass0asastrongertonalcenter.
F u r t h e r m o r e ,w ea i m e da th a v i n gs o m ed e g r e eo fw e l l -formedness,namelysymmetry(Carey&Clampitt, 1989).
T h eI Cd i s t r i b u t i o na i m e dt oe n f o r c et h em o r ec o n s o -nant intervals, objectively assessed by Vassilakis’ ( 2001)
sensorydissonancemodel.
11
Figure5showstopologicalFourierphasespacesin Z12
(left image) and Z7(right image) for the 14 best-ranked
pcsets with cardinality t=3. We adopt the same input
parameters ( IandR)f r o mt h eh a r m o n i cs t a b i l i t yr a n k -
inginTable 2,anda α=.3inbothspaces.Toreducethe
high-dimensional Fourier phase distances of pcsets to a2-dimensionaltopology,weapplymultidimensionalscal-ing (MDS). This strategy has been largely conveyed bycognitivepsychologyresearchtovisualisepitchdistances(Miller,1989). To create an MDS representation from
pcsetsdistancesintheFourierphasespace,wefirstcom-
puteasquaredistancematrixbetweeneachpairofpcsets
using Eq. 2 solved for θ.Then,weapplyaclassicalMDS
algorithm (Torgerson, 1952) to create a 2-dimensional
projection, where the between-pcset distances are pre-servedwithminimaldistortion(orminimalstressusingtheMDSterminology).
In the
Z12space, the most striking property is the
emergence of fuzzy clusters where functional harmoniccategorieswithintheregionofCmajorcanbeobserved.Clustersareiden tifiedintheleftimageofFigure5 asSD
a n dDl a b e l s ,s t a n d i n gf o rs u b d o m i n a n ta n dd o m i n a n tfunctionalcategories,respectively.Theseclustersemergeprimarily from aggregating pcsets that share commonpitch classes, an information conveyed by the Fourier
11ThesensorydissonanceoftheIC1,IC2,andIC3in Z7equalto5.98,3.77,and
2.5,respectively.phaseinformation.Thetonicchord,labeledasT,isiden-tified in Figure 5and isolated from remaining clusters.
Note that some scale degrees of the tonic, dominant,a n ds u b d o m i n a n tc h o r dg r o u p s– (ˆ1,ˆ3),(ˆ7),a n d( ˆ4,ˆ6),
respectively – are naturally separated in T(3)andT(4)
DFTcoefficientspaces(Yust, 2019).Inpart,thisisdueto
thethirds-basedstructureinthesecoefficients,associatedwith hexatonicity and octatonicity harmonic qualities,and it points to a univocal relationship between coeffi-cientsT(3)andT(4), and the foundation of functional
syntax, often summarised as ii−V−I, i.e. subdominant-
dominant-tonic. Furthermore, by crossing the informa-tionwiththepcsetstability H,wecanusethesetopologies
toinferpossiblepathsacrosspcsetsinthespace,enforc-ingcommonpitchclasses(looselylinkedtovoice-leadingparsimony).
A similar rationale can be applied to less studied and
systematized spaces as the
Z7shown in the right image
of Figure 5. The composer should define clusters and
harmonic paths to establish lexical and syntactical rela-tionships within a work. For example, one of the promi-nent features in
Z7is the separation between pcsets
with ‘leading tone’ (in this context, the pitch class 6).Conversely to the leftmost pcsets, the rightmost pcsetse m b e d st h ep i t c hc l a s s6 .T h i sd i s t r i b u t i o ni ss i m i l a rt otheonefoundinthe
Z12universethroughthedominant
andsubdominantgroups.Inthiscontext,itisofcompo-sitional relevance to ask whether successive pendulumsbetween pcsets of the first group and pcsets of the sec-ondmightconstituteprototypicalharmonicprogressionsin
Z7– as it is usually the case in Z12.F u rt h e r m o r e ,t h e
topological representation of the space can quintessen-tially promote geometric-driven harmonic systems byapplyingconceptssuchasrotation,translation,andmor-phing. A video demonstration of harmonic sequences

## Page 11

JOURNAL OF NEW MUSIC RESEARCH 151
Figure 5. Multidimensional scaling reduction of the Fourier phase space exposing common pitch class relationships for the high-
est ranked 14 pcsets with cardinality t=3i nZ12andZ7on the left and right images, respectively. The left image adopts adopt
R={3,0,1,0,2,1,0,2,0,1,0,1} and I={0,0,1,1,1,0}.Therightimageadopts R={3,0,1,2,1,2 }and I={0,1,1}.Bothspacesadopt
α=.3.Intheleft Z12image,weidentifytheclustersforsubdominant(SD),dominant(D),andthetonicchord(T).Intheright Z7image,
adashedlinesplitspcsetsintotwogroupsbasedontheembeddingofthe‘leadingtone,’thepitchclass6.Pleasenotethatsimilarpcsets
inZ12andZ7donotadoptthesametuning.
definedinthe Z12andZ7topologicalspacesofFigure 5
can be found in the supplementary materials to this
article.
Inspired by the hierarchical pitch representation by
Lerdahl ( 1988),12Table3shows the most stable pitch
classesforpreviouslygivenuser-definedparametersfrom
FluidHarmony at different hierarchies (labeled as ‘lev-els’). Each level relates to a cardinality, and higher levelsdenote increasing cardinalities. It includes pitch con-figurations based on constructs from 12-TET West-ern art music, such as the total pitch collection, aregional set (typically including the notes of a scale),chords (triads and tetrads), a dyad, and a singlepitch.
Computationally, each pcset per level corresponds
t ot h em o s ts t a b l ep c s e tp e rc a r d i n a l i t y t(the stabil-
ity of pcsets is given by Hin Eq. 8). In other words,
the pcsets featured in Table 3result from computing
the pcsets with the highest Hf r o mt h es a m es e to fR
andIparameters for the multiple values of 1 ≤t≤p.
Conversely to existing pitch models (Krumhansl, 1979;
Longuet-Higgins, 1987;S h e p a r d , 1982), FluidHarmony
can define all levels of pitch description and establish
their hierarchical relations. The resulting representation
12The inspiration for the representation in Table 3is attributed to Lerdahl’s
(1988)TonalPitchSpace,whoserootscanbefoundinDeutschandFeroe
(1981).denotes a ‘well-formed’ basic space as proposed by Ler-
dahl(2001).13Well-formedrepresentations,denotingthe
basicspaceofsomeuser-definedconditions,areenforcedifsmallervaluesof αareadoptedtoprivilegetheregional
space,definedbythereferencepcset R,overtheICsI .
T h eb a s i cs p a c es h o w ni nT a b l e 3can be understood
asacontext-sensitivestratificationofa p-TETspace.Sta-
b i l i t yd e c r e a s e sa sw em o v ed o w nf r o ml e v e lai nt h espace.Eachleveliscumulative,aspitchclassespresentedat the most stable level are repeated at the lesser stablelevels. This cumulative property of the levels follows thetraditionofthereductionalspacepromotedbytheGen-erative Theory of Tonal Music (Lerdahl & Jackendoff,1996). While outside of the scope of this article, pursu-ingamathematicalframeworkfromtheproposedrepre-sentation can expand the music-theoretical and music-psychological discourse of Lerdahl’s ( 2001)t o n a lp i t c h
space theory beyond the 12-TET Western tonal context.Inthecontextofourproposal,ontheuseoftheFluidHar-mony method for assisting in the composition process,the levels can be either explicitly considered as a refer-ence pcset R, or as a guiding framework for guiding the
composerindefiningmicroandmacroharmonicobjects.
Note that in all of the examples provided in the cur-
rent section, the reference pcset Rtypically adopts a
large cardinality twithin the possible number of pitch
13The concept of well-formedness has a conﬂicting deﬁnition in the litera-
ture.Inthecontextofourwork,wefollowthedeﬁnitionproposedbyLer-
dahl (2001 ). For a comprehensive comparative discussion on the multiple
proposals,pleaserefertoNoll( 2010).

## Page 12

152 G. BERNARDES ET AL.
Table 3.Pitch class hierarchical space representation inspired
from Lerdahl (1988 ), where the embedding of the space across
hierarchies is highlighted. Each level is related to a cardinality t,
andallpossiblelevels(andcardinalities)arerepresented.Perlevel,
we notate the pcset with higher stability Hcomputed from the
FluidHarmonymethodwiththefollowingparameters.Therepre-sentation(a)isinZ12andadopts R={3,0,1,0,2,1,0,2,0,1,0,1}
andI={0,0,1,1,1,0 }.Therepresentation(b)isin
Z7andadopts
R={3,0,1,2,1,2 }and I={0,1,1}. Both spaces adopt α=.3.
Please note that similar pcsets in Z12andZ7do not adopt the
sametuning.
(a)
card tlevel
1a 0
2b 0 73c 0 4 7
4d 0 4 7 9
5e 0 2 4 7 96f 0 2 4 5 7 9
7g 0 2 4 5 7 91 1
8 h 0 2 45 789 1 19i 0 1 2 4 5 7 8 91 11 0 i 012 45 7891 01 1
11 j 0 1 2 4 5 6 7 8 9 10 11
1 2 j 01234567891 01 1
(b)card tlevel
1a 0
2b 0 3
3c 0 3 64d 0 2 3 6
5e 0 2 3 4 6
6f 0 2 3 4 5 67 g 0123456
classes from a collection p. This strategy follows a tradi-
tionalmodus operandi withinWestern(tonal)artmusic,
where harmonic structures tend to adopt a top-down
definition. For example, given a regional context (or a
key), we can define subsets that enforce stabilityfurther.
WhilethisstrategyisnotarequirementintheFluidHar-monymethod,itoffersgreatercontroloverthegeneratedharmonic lexicon. However, the definition of a refer-encepcsetinFluidHarmonycanexistateveryhierarchy,conveying different degrees of control over pitch classretentionfromthereferencepcset R.
6. Evaluation
This section details an objective computational assess-ment of our FluidHarmony method in predicting theharmoniclexiconinWesternartmusicalpiecesandhowit aligns with composition practice across multiple his-torical periods within the Western art music tradition.Specifically, we are assessing how well the constraints inFluidHarmonymodelharmonicpcsetperformonlexicamodellingforindividualcomposersandbetweengroup-ings of pre- and post-1900 composers. We assume theremainingspacestobeexplored,particularlyequaltem-peramentsbeyond12-tonesubdivisions,canbeformallydefinedfromthesameconstraints.
A representative sample of Western music can be
foundinthe TheYale–ClassicalArchivesCorpus (YCAC)
(White & Quinn, 2016), whose properties are described
in Section 6.1. Given the focus of the current study in
promoting CAAC for less systematized contemporarypractices, we expanded the YCAC with more represen-tativeexamplesacrossthetwentiethcentury.Toinfertheinput parameters of the FluidHarmony model, we com-pute statistics from each corpus’ file. Then, we define apcset ranking given the harmonic stability Hvaluefrom
FluidHarmony. Finally, we quantify the degree to whichthe proposed FluidHarmony ranking captures a pcsetsfrequency distribution of each file and bolster intuitiveobservations on our method from the large amounts ofanalyzeddata.
Furthermore, the implication and contribution of the
twofold constraints are studied on the corpus by infer-
ring the value of αi nE q .8t h a tb e s tp e r f o r m si no u r
method.Ourexpectancyisthatbothconstraintsarefun-
damental to the computation of a harmonic lexicon,namely in the common-practice period. However, it iscurrently unknown the degree to which each parametercontributestolexiconformation.
6.1. Corpus properties and annotations
The YCAC yields data from 8,713 MIDI files of
pieces or movements from Western European Classi-cal art music. The corpus was compiled from digitalmusical scores indexed in the crowd-sourced archiveclassicalarchives.com . Therefore, no systematic criteria
exist for the resulting collection, reflecting the prioritiesof a group of individuals committed to converting theirfavourite pieces into a digital format. Despite its unde-niable value for a systematic analysis of symbolic music,misrepresentations of the musical score have been iden-tifiedintheYCAC.AsDeClerq( 2016)notes,themisrep-
resentations derive mostly from the automatic detection
of scale degrees and local keys. However, they are usu-
ally ‘coherent’ with the underlying macroharmony. Asour evaluation tackles relations between local and largestructures inferred from the first, these misrepresenta-tionsmay have little influence on our results. White andQuinn (2016) highlight the higher representativeness of
‘theusualsuspects’–e.g.,Bach,Beethoven,Mozart–inthecorpus along with some composers from whom little tono information is available. To avoid any poor statisti-cal results that could bias the observation per composertowards particular musical examples, we excluded allcomposers in the YCAC with less than eight files from

## Page 13

JOURNAL OF NEW MUSIC RESEARCH 153
Figure 6. Number of ﬁles and slices per composer in the evaluation corpus. Slices are split into train slices (used to parameterise the
FluidHarmonymethod)andtheslicesadoptedfortestingthemethod.Composersarechronologicallyorderedinthe x-axis,providing
anoverviewofthedistributionofﬁlesandslicesacrossthetemporalspanofthecorpus.
ouranalysis.Moreover,weequallyexcludedmonophonic
MIDI files due to the inability to compute an input ICdistribution–afundamentalparametertoourmethod.Intotal,5,112filesfromtheYCACwereprocessed.
In the resulting corpus, the lack of twentieth cen-
tury composers was particularly noticeable. Due to thefocus on the application of the FluidHarmony methodinlesssystematizedharmonicsystemsoutsidetheWest-ern common-practice period, we expanded the corpuswith 72 new files from the following four representativetwentieth century composers: Olivier Messiaen, Arnold
Schoenberg,IgorStravinsky,andAntonWebern.Atotal
of 5,184 files were compiled in the corpus, whose distri-butionpercomposerisshowninFigure 6.Theextended
set of files was processed and annotated following theYCAC syntax and can be found in the supplementarymaterialtothisarticle.
Data and metadata annotations for each file in the
extended YCAC cover a variety of fields such as pitchand rhythmic content information of the musical sur-face,title(nameofthepiece),composer(lastname),dateof publication, and genre indicating the piece’s compo-sitional or formal type (e.g., symphony, character piece,opera, or mass.) For a comprehensive description ofavailable annotations, please refer to White and Quinn(2016).Fundamentaltoourevaluationisthecorpusdatarep-
resenting the pitch class information per ‘salami slice,’i.e. a segmented pcset each time a pitch is added or sub-tractedfromthemusicalsurface.
14Thecorpusincludesa
totalof7,582,130slices,whosedistributionpercomposerisshowninFigure 6.Giventheneedtoparameterisethe
DFT space by the input vectors RandI,w ec r e a t e da
threefold split of each file in the corpus and adopt 2 /3
ofthetotalnumberofsalamislicestocomputetheinputparameters and 1 /3t ot e s tt h em e t h o d – at y p i c a ls p l i t
within machine learning evaluation when adopting the
samedatasetfortrainingandtesting(Jamesetal., 2013).
The test slices are retrieved from the end of each file,
wheremodulationsarelesspronetooccur,thusminimis-ingpossiblemismatchesbetweentheparameterisationofRandthetestingpcsets.Fromthetotalnumberofslices,
5,054,753areusedforparameterisingtheDFTspace(i.e.definingRandI), and the remaining 2,527,376 for test-
ing the FluidHarmony method. Figure 6shows the split
betweenthenumberofslicesusedtocomputetheparam-etersandthenumberofslicesusedfortestingthemethodpercomposer.
14The salami slice segmentation can be computed from MIDI ﬁles by the
chordify()functionwithinthemusic21softwarepackage.

## Page 14

154 G. BERNARDES ET AL.
Figure 7. SalamislicesegmentationoftheﬁrsttwomeasuresofBach’sAria Meine Seufzer meine Tranen fromthe Achzen und erbarmlich
WeineninGminor,BWV13.Slicesarenumberedanddenotedbyverticalboundinglines.
The salami slice segmentation method offers access
to the musical surface without biases towards particular
constructs or assumptions, namely on what constitutesac h o r do rw h a ts t r u c t u r e ss h o u l db ep r i v i l e g e d .H o w -ever,thisequallymeansthat,forexample,pcsetsresultingfromprocessesofembellishmentandelaboration,suchaspassingnotes,neighbournotes,suspensions,andappog-giaturas, will create segments that do not comply withthe underlying harmonic lexicon. Figure 7exposes how
themethodcanintroduceinconsistenciesintheresultingevaluation.Forexample,theslicethreeinFigure 7results
inthenon-diatonicpcset {6,7}inthecontextofGminor,
as a result of the appoggiatura by step-wise motion in
the upper voice. While some research has experimentedwith ways to introduce equivalencies into the alphabetof chord types (White, 2013), the power and peculiar-
ity of the YCAC salami-sliced data should be noted andr e m a i n s ,t ot h eb e s to fo u rk n o w l e d g e ,t h em o s tr e l i -ablesegmentationstrategytoassessourmethodwithout
assumptions.
6.2. Computational methods
For each file in the corpus, we parsed its annotation
file and retrieved its entire collection of pcsets as salamislices. Per file, two distributions were computed fromt h efi r s t2 /3o ft h et o t a ln u m b e ro fs a l a m is l i c e s :a n
IC distribution and a 12-element pitch class histogram.
The resulting vectors are input to our FluidHarmony
method as parameters IandR,r e s p e c t i v e l y .T h et w o
remaininguser-definedattributes,cardinality tandmag-
nitude/phase balance αwere set to 1 ≤t≤12∈
Z12
and 0 ≤α≤1∈R, respectively. We instantiate Fluid-
Harmony with all unique pcset combinations Piwithin
Z12, i.e. all combinations of pitch classes in the range[0,11] ∈
Zwith pcsets of 1–12 elements or cardinali-
ties. A total of 4,095 unique pcsets combinations arecreated.
We ran the FluidHarmony method for each file in
thecorpusandcomputeditspcsetranking.Afrequencydistribution histogram for each file is created using theranked pcsets order as the distribution indexes (twoexamples are shown in Figure 9). Finally, we compute
aharmonic ranking index as the median index of the
frequency distribution histogram. The smaller the har-monic ranking index, the better the adopted lexicon ineachfilefitstheharmonicpcsetrankingfromFluidHar-mony.
Theharmonicrankingindexwascomputedforallval-
uesof0 ≤α≤1inEq.8wi th .05incrementvalues.For
eachvalueof α,wecalculatethemedianoftheharmonic
ranking index values for all files of a given composer inthe corpus. The results (per composer and for the entirecorpus)aimtoshowtherelativeimportanceofeachcon-straint in capturing the lexicon of existing Western artmusic.Thedatavalleyindicatesthebestperforming αin
providing the best alignment between the pcset rankinggenerated by the FluidHarmony method and the har-moniclexiconadoptedbythecomposers.Valleysat α=
0a n d α=1i n d i c a t et h a to n l yt h ep h a s eo rm a g n i t u d e ,
respectively, would be relevant to best capture the har-monic lexicon of the corpus files. A valley within limitsindicates that both constraints are relevant to computethelexiconandtheircontribution.
6.3. Results
Figure8showstheharmonicrankingindexaveragedper
composerusingvaluesof0 ≤α≤1inEq.8.Theresults
show a large agreement across the evaluated composers
in the global tendency of the data and the index of theirvalleys,indicatingthebestperforming α.Whencombin-
ingtheentirecorpus,shownasadashedlineinFigure 8,
thevalleyisfoundat α=.5.Thelattervalueexposesthe
bestperforming αfortheFluidHarmonymethodincap-
turingharmoniclexicaofWesternartmusicandprovidesan ‘agnostic’ indicator, or a default parameter value, toguide composers in the initial exploration of FluidHar-mony. Furthermore, it validates the importance of both

## Page 15

JOURNAL OF NEW MUSIC RESEARCH 155
Figure 8. Harmonicrankingmedianfor0 ≤α≤1valueswith.05stepdistancesinEq.8.Resultsareshownpercomposerandforthe
entirecorpus(dashedline).Thevalley α=.5indicatestheoptimumvaluetobalancebothconstraintsintheproposedmethod.Balance
(α)BetweentheFourierMagnitudeandPhaseConstraints.
constraints in capturing harmonic lexica from the cor-
pus.However,wemustnotetheasymmetryoftheresults
(considering the results for the entire corpus, the skew-nessis1.2).Itexposesanon-linearrelationshipbetween
theαrange values and the resulting implications in the
computedlexicon.Byadoptinglarger αvalues,thuspriv-
ilegingthemagnitude V,weremainclosertothelexicon
than privileging the phase Cby adopting smaller values
ofα.
Figure9showsthefrequencydistributionhistograms
fortwofilesinthecorpusbyJohannSebastianBach.Theyexpose a high (on the left image) and low (on the rightimage)performingharmonicrankingindexfortwocor-pus’filesfromBach.Theindexesareshowntogetherwiththe pcset on the y-axis. To enhance the figure’s read-
ability, we excluded all indexes from pcsets that werenot adopted in a given file. In these two examples, wecan observe the implications of the adopted segmenta-tionintheresults.Intherightimagedistribution,wecanverifythepredominanceofnon-diatonictonesinthelex-iconadoptedbythecomposerastheresultofverticalities
thatencompassmanyornaments.Theentirecollectionof
generatedplotsareavailableassupplementarymaterialtothisarticle.Asquaredboxaroundanindexonthe y-axis
identifiestheharmonicrankingindex Handprovidesan
intuitiveunderstatingoftheinformationcapturedbythisindex,namelytherelationbetweenthefrequencyvalues
on the histogram and its placement in the ranked and
indexedpcsets.
Descriptivestatisticsofharmonicrankingindexesfor
t h ee n t i r ea n a l y z e dc o r p u sa r es h o w ni nT a b l e 4.T h e
descriptive statistics include average and standard devi-ation (STD) of the corpus’ harmonic ranking indexesH. An averaged index of 52.7 ±110.1 out of the 4,095
unique indexes (or unique pcsets combinations) showsthatourFluidharmonymethodcancaptureintheupperpcset ranking the harmonic lexicon used by the com-p o s e r si nt h ec o r p u s .I no t h e rw o r d s ,t h ea d o p t e dp c s e tlexiconinthecorpusisprimarilycapturedinthe8%toppcsetsintheFluidHarmonyranking(weadopta86%asareferenceforcomputingtheprimarypcsetinformationcaptured by the ranked data in FluidHarmony). More-over,weshallconsiderthatinmostrankingsusinga
Z12
d i a t o n i cp i t c hs p a c e ,s u c ha st h o s ei n c l u d e di nt h ec o r -pus, the initial pcsets in the ranking typically comprisethe seven diatonic pitch classes and 21 dyads resultingfrom the combination of the prominent ICs in Iand
pitch classes in the reference pcset R.H o w e v e r ,w i t h i n
Western art music, a 3- or 4-voice texture is more com-monlyadopted(Huron, 2001),henceaharmonicranking
indexinthe[20-50]rangeismostlycapturing‘in-region’triads and tetrads. Moreover, while the test pcsets are

## Page 16

156 G. BERNARDES ET AL.
Figure 9. HistogramofpcsetsadoptedintwocompositionsbyBach: Fugueofthe Fantasy and Fugue inCminor,BWV906(leftimage)
andtheMinuetofthePartitano.5inGMajor,BWV829(rightimage).Theorderofpcsetsinthe y-axisresultsfromthepcsetranking
ofFluidHarmony(eachlabelindicatesthepcsetfollowedbyitsrankingindex).Indexentrieswithoutanypcsetand,intherightimage,
multipleentriesfromthemiddleofthehistogramhavebeenremovedforenhancedreadability.Thedistribution’sstatistics(medianand
IQR)equals3 ±6and193 ±558fortheleftandrightimages,respectively.
retrieved from the last part of each file where modula-
tions are less prone to occur, we must account for somedegreeofpcsetsthatarerepresentedtoalesserdegreein
R,p o s s i b l yp e n a l i s i n gt h er e s u l t sw i t hh i g h e rh a r m o n i c
rankingindexes H.Whileacknowledgingthisartifactin
o u re v a l u a t i o np r o c e d u r e ,p l e a s en o t et h a t Raccumu-
latesallinformationfromthefirst2/3slicesofeachpieceand enforces the pcsets with greater frequency, whicha r ee x p e c t e dt ob ei nt h ek e yo ft h ep i e c e .T h i sp o s s i -ble mismatch can equally have a greater penalty in later
historical composers, where modulations or displaced
t o n a lc e n t r e sa r em o r el i k e l yt oo c c u r .H o w e v e r ,c o m -posers after 1900 only account for 10% of the total testslices.

## Page 17

JOURNAL OF NEW MUSIC RESEARCH 157
Table 4.Descriptive statistics–average and standard deviation
(STD)–for the harmonic ranking index Hof the YCAC ﬁles under
analysis. The analysis presents statistics for the entire corpus
and for composers before and after 1900. We observe a gradual
increase in the harmonic ranking index in the period after 1900.
Allanalysisadoptathreefoldsplitperﬁle(2/3forparameterisation
and1/3fortesting).
Composers
before1900Composers
after1900 AllComposers
Files 4530 654 5184
Slices(param) 4547966 506787 5054753
Slices(test) 2273983 253393 2527376Average 40.1 140.2 52.7
STD 46.7 268.8 110.1
Table4also presents the statistics by grouping com-
posers before and after 1900. This split is defined in
the YCAC as ‘major’ and ‘minor’ composers, due totheirsmallerrepresentativenessinthecorpus,butequallysplits the corpus historically at the turn of the twentiethcentury. In the context of our work, this split provides abetter analysis of the harmonic ranking index Hin pri-
marilytonaldiatoniclexicabefore1900(40.1 ±46.7)and
more unsystematic approaches to harmony in the twen-tieth century (140.2 ±268.8). To better unpack this his-
toricallyincreaseintheindex H,weshowinFigure 10an
analysispercomposer.Ofnotetheincreasingtendencyofthe index across historical periods. This aligns with thehistorical perspective provided by multiple studies con-veyingtheappropriationofamoreextensivelexiconandthe gradual emancipation of dissonance (Tenney, 1988).
Of note are two twentieth century composers a notice-able higher harmonic ranking index H:Sc h o e n b e r ga n d
Webern. We strongly believe that the worse results byt h e s et w oc o m p o s e r sr e l a t et ot h e i ra d o p t i o no ft w e l v e -tone techniques–also known as dodecaphony. The latterapproach results in a (nearly) uniform reference pcsetR, thus failing to provide information about the regionthe pcsets should occupy in the Fourier space. In theseparticular cases, where either the IC distribution Iand
reference pcset Rresult in uniform distributions, Fluid-
Harmony constraints may be insufficient in defining apcsetlexicon.
7. Conclusions and future work
We have proposed FluidHarmony, a CAAC methodto systematically and intuitively explore the definitionof a harmonic lexicon, namely the less systematizedequaltempered pitch spaces with any psubdivisions of
the octave. In contrast to existing methods (Anders &Miranda, 2010), our method requires little
parameterisationbyleveragingtheFourierspaceinelic-iting control over the IC and pitch class retention of areference pcset as high-level concepts, intrinsic to thecompositionpracticewithinWesternartmusic.Theusercan control these properties with fine detail by decou-plingFouriermagnitudeandphaseinformation,respec-tively. Their contribution to a final ranking of pcsetsby harmonic stability can be defined by the user andexploreddynamically.
To control the compliance of pcsets to an arbitrarily
anduser-definedICdistribution,weproposedastrategyto assign weights to the coefficients of a Fourier spacealgebraically.Thestrategyisfundamentaltoourmethodin controlling the contribution of each IC to the magni-tudeofapcsetintheFourierspace,usedasanindicatorofthepcsetcompliancetotheuser-definedICdistribution.
The indicator of tonal stability Hand the metrics
underlyingitscomputationinFluidHarmony,namelytheFourier magnitude and phase information, have beenshowntoelicithierarchicalrepresentationsthatcanassistcomposersindefiningpcsetrelations.Theharmonicsta-bility indicator provides the most accessible hierarchythat ranks pcsets according to the user-defined con-
straints. The phase information conveyed by angular
distances between pcsets in the Fourier space allowsthe definition of a novel topology where common pitchclasses across sets are expressed as distances, using anMDS algorithm. In mirroring some properties of the
Z12Fourierspace,wherepcsetswithinsubdominantand
dominantharmoniccategoriesexistasfuzzyclusters,wespeculate the use of any p-TET phase space to extrap-
olate the possibility to establish pcset trajectories withsyntactic value or foster the exploration of geometric-dependent concepts, such as rotation, translation, andmorphing.Finally,arepresentationinspiredbyLerdahl’s(2001)tonalpitchspace,particularlyhisbasicspacewithi t sw e l l - f o r m e dp r o p e r t y ,i sc o n v e y e db yt h eF l u i d H a r -monymethod.
To evaluate our method, we conducted a systematic
analysis of a large corpus of 5,064 files (including move-ments and entire pieces) to assess how well the pro-posedFl uidH a rm o n ym eth odca p t ur esth epcsetlexico nof existing Western art music. Our corpus included themostrepresentedcomposers(witheightormorefiles)in
the YCAC (White & Quinn, 2016), which we extended
with 72 files by representative twentieth century com-
posers – made available in the supplementary materialstothisarticle.TheresultsprovideempiricalevidencethatFluidHarmony pcset ranking aligns well with the pcsetdistribution used by the composers in the corpus’ files.Ourmethodcanpredictmostofthecorpuspcsetsinthetop1.3%oftheFluidHarmonyranking.
While the FluidHamony method promotes the sys-
tematic definition of a harmonic lexicon from IC andpitchclassconstraints,itdoesnotassure optimalsurface
structure. The embodiment of the resulting lexicon in

## Page 18

158 G. BERNARDES ET AL.
Figure 10. Descriptivestatistics(median,IQR,whiskers,andoutliervalues)fortheharmonicrankingindexpercomposerinthecorpus
forα=.5.Composersinthe x-axisareorderedchronologicallyfromlefttoright.
musicalpracticerequiresaleapfromtheoreticalmusical
abstractionstosurfaceelaboration,suchasthedefinitionofpitchheight,rhythmic,andtimbreattributes.Thesur-faceelaborationcanheavilyimpacttheperceptualresultand the construction of harmonic coherence akin toevent and tonal hierarchies. In the spirit of CAAC tools,FluidHarmony fosters a methodology that precedes thecompositionpracticebyofferingoneapproachtothesys-tematic rationalisation of p- T E Tp i t c hs p a c e so nw h i c h
prescriptionscanbebased.
In the supplementary material to this article, we can
find manifestations of its many contributions. To pro-mote the creative appropriation and the scientific andartistic extension and reproducibility of our study, wesupplytwosoftwareimplementations,thetwentiethcen-
tury musical pieces included in the YCAC, our evalu-
ation data, and a video demonstration of the methodimplementationindefiningpcsetsequences.
In the supplementary material to this article, we pro-
videma terialstha tdemonstra tethecrea tivea pplica tionsandreproducibilityofourstudy.Specifically,weprovidetwo software implementations, the twentieth-centurym u s i c a lp i e c e si n c l u d e di nt h eY C A C ,o u re v a l u a t i o ndata, and a video demonstration of the method imple-mentation in defining pcset sequences. The FluidHar-monymethodhasbeenimplementedinthePythonlan-guage and Pure Data software environments to reacha broad audience acquainted with either code or visualprogrammingenvironments.
In the future, the most pressing issue to be pursued
isconductingcasestudiesandevaluationsprotocolsthatassessthecreativitysupportofFluidHarmonyincompo-s i tio n ,a sw e lla ss t u d yth eim p l ica tio n so fc o n tr o lv e r s u sa u t o n o m yw i t h i nt h ec r e a t i v ep r a c t i c ea n dt h ep o s s i b l eappropriationsofthemethodbypractitioners.WhiletheFluidHarmonymethodcanbeaccusedof‘universalising’or reducing creative freedom, we are actually aiming toallowgreaterexperimentationbyregulatedconstraints.
The further development of our work would bene-
fi tg r e a t l yf r o mt h ew i d e ra v a i l a b i l i t yo fn o n1 2 - T E Tsymbolic music datasets. However, the scarce numberof non 12-TET pieces available in the digital domainas symbolic representations in addition to the copyrightimpediments to make them publicly available, limitedourabilitytoevaluateourmethodbeyond12-TET.Suchanendeavourshallbepursuedinthelongtermfuture,as

## Page 19

JOURNAL OF NEW MUSIC RESEARCH 159
it can promote the systematic and empirical analysis of
twentieth-centuryWesternartmusic.
WeaimtoexpandfurthertheFluidHarmonymethod
towardsacomputationalcognitive-inspiredmodel,wherecontrolled experimental predictions about mental rep-resentations of musical structure, dependency relations,harmonic attraction, and tension in (unfamiliar) p-TET
p i t c hs p a c e s ,o t h e rt h a n1 2 - T E T ,c a nb et e s t e dw i t h o u tthe same reliance on symbolic datasets. Of interest arethe emerging qualities of the proposed hierarchies ineliciting syntactic relations by circular motions orbitingaroundthereferencepcset.Thehypothesisrelatedtohar-monicmotioninthehierarchiesproposed,namelythoserelatedtothetopologicalrepresentations,canleadtonewinsights into the mental processes regulating harmonicsyntax.
Our findings have a twofold impact at the theoreti-
cal and application levels on empirical musicology andmusic composition. First, we provide evidence that therelativeimportanceofICsandareferencepcsetarefun-
damental in regulating the harmonic lexicon in 12-TET
Western tonal music. The lexicon of Western art musicis largely captured by an even combination of these twoproperties. Second, the proposed weighted DFT spaceadopting the above elements as spatial constraints andthe detailed, quantifiable metrics and hierarchical rep-resentations of pitch in any number of equal-temperedoctave divisions expand the range of creative supportmethodsandtoolsavailabletocomposers.Toourknowl-edge,suchformalmethodshaveneverbeenproposedforp i t c hs pa c e sbey o n d1 2 - T E T ,a n dca npo t e n tiall yu nl oc kthe definition of harmonic lexicon and leverage novelcreativecompositionalstrategiesinlessstudiedandsys-tematizedpitchspaces.
Disclosure statement
Nopotentialconflictofinterestwasreportedbytheauthor(s).
Funding
This research has been funded by the Portuguese Foundation
for Science and Technology, Research and Technology [2021.
05132.BD and 2021.05059.BD] and by the Marie Curie StaffExchange (MCSE) project “An European and Ibero-American
approach for the digital collection, analysis and dissemina-
tion of folk music” (Grant Agreement 101086338) under theEuropean Union’s Horizon Europe research and innovation
programme.
ORCID
GilbertoBernardes http://orcid.org/0000-0003-3884-2687
NádiaCarvalho http://orcid.org/0000-0001-6882-5138
SamuelPereira http://orcid.org/0000-0003-2866-1081References
Aldwell, E., Schachter, C., & Cadwallader, A. C. ( 2018).Har-
mony&voiceleading (5thedition).Cengage.
Amiot, E. ( 2013). The torii of phases. In J. Yust, J. Wild,
&J .A .B u r g o y n e( E d s . ) ,Mathematics and computation in
music(Vol. 7937, pp. 1–18). Springer Berlin Heidelberg.
https://doi.org/10.1007/978-3-642-39357-0_1.
Amiot, E. ( 2016).Music through fourier space: Discrete fourier
transform in music theory . Computational Music Science.
SpringerInternationalPublishing.Imprint:Springer,Cham,1sted.2016edition.
Amiot, E. ( 2017). Interval content vs. Dft. In O. A. Agust´ın-
Aquino, E. Lluis-Puebla, & M. Montiel (Eds.), Mathemat-
ics and computation in music (Vol. 10527, pp. 151–166).
Springer International Publishing. https://doi.org/10.1007/
978-3-319-71827-9_12.
Anders,T .,&Miranda,E.R.( 2010).Acomputationalmodelfor
rule-basedmicrotonalmusictheoriesandcomposition. Per-
spectivesofNewMusic ,48(2),47–77. https://doi.org/10.1353/
pnm.2010.0009
Assayag, G., Rueda, C., Laurson, M., Agon, C., & Delerue,
O. (1999). Computer-assisted composition at ircam: From
patchwork to openmusic. Computer Music Journal ,23(3),
59–72.https://doi.org/10.1162/014892699559896
Bernardes, G., Cocharro, D., Caetano, M., Guedes, C.,
&D a v i e s ,M .E .( 2016). A multi-level tonal interval
space for modelling pitch relatedness and musical con-sonance. Journal of New Music Research ,45(4), 281–294.
https://doi.org/10.1080/09298215.2016.1182192
Bernardes,G.,Davies,M.E.P .,&Guedes,C.( 2017).Automatic
musical key estimation with adaptive mode bias. In 2017
IEEE International Conference on Acoustics, Speech and Sig-
nal Processing (ICASSP) , 316–320, New Orleans, LA. IEEE.
https://doi.org/10.1109/ICASSP.2017.7952169 .
Bharucha, J. ( 1984a). Anchoring effects in music: The reso-
lution of dissonance. Cognitive Psychology ,16(4), 485–518.
https://doi.org/10.1016/0010-0285(84)90018-5
B h a r u c h a ,J .J .( 1984b). Event hierarchies, tonal hierarchies,
and assimilation: A reply to deutsch and dowling. Jour-
nal of Experimental Psychology: General, 113(3), 421–425.
https://doi.org/10.1037/0096-3445.113.3.421
Boulanger, R. C. ed. ( 2000).T h eC s o u n db o o k :P e r s p e c t i v e s
in software synthesis, sound design, signal processing, and
programming .M
 ITPress.
B u t l e r ,D .( 1990). A study of event hierarchies in tonal
and post-tonal music. Psychology of Music ,18(1), 4–17.
https://doi.org/10.1177/0305735690181002
Callender, C. (2007). Continuous harmonic spaces. Journal
of Music Theory ,51(2), 277–332. https://doi.org/10.1215/
00222909-2009-004
Carey,N.,&Clampitt,D.( 1989).Aspectsofwell-formedscales.
Music Theory Spectrum ,11(2),187–206.
Clough, J., & Douthett, J. ( 1991).Maximally evensets. Journal
ofMusicTheory ,35(1/2),93. https://doi.org/10.2307/843811
DeClerq, T. ( 2016). Big data, big questions: A closer look
at the yale–classical archives corpus (C. 2015). Empirical
Musicology Review ,11(1), 59. https://doi.org/10.18061/emr.
v11i1.5274
Deutsch, D., & Feroe, J. ( 1981). The internal representation of
pitch sequences in tonal music. Psychological Review ,88(6),
503–522. https://doi.org/10.1037/0033-295X.88.6.503

## Page 20

160 G. BERNARDES ET AL.
Didkovsky, N., & Burk, P. L. ( 2001). Java music specification
language,anintroductionandoverview.InProceedingsofthe
InternationalComputerMusicConference ,H avana.
Forte, A. ( 1973).The structure of atonal music .Y al eU n i v e r s i ty
Press.
G h i s i ,D . ,&A g o s t i n i ,A .( 2017). Extending bach: A fam-
ily of libraries for real-time computerassisted composi-
tion in max. Journal of New Music Research ,46(1), 34–53.
https://doi.org/10.1080/09298215.2016.1236823
Harte, C., Sandler, M., & Gasser, M. ( 2006). Detecting har-
monic change in musical audio. In Proceedings of the 1st
ACM workshop on Audio and music computing multimedia-A M C M M‘ 0 6 , 21, Santa Barbara, California, USA. ACM
Press.https://doi.org/10.1145/1178723.1178727.
Huron, D. ( 2001). Tone and voice: A derivation of the rules of
voice-leading from perceptual principles. Music Perception ,
19(1),1–64. https://doi.org/10.1525/mp.2001.19.1.1
Huron,D.( 2016).Voiceleading:Thesciencebehindamusicalart
(1st ed.). The MIT Press. https://doi.org/10.7551/mitpress/
9780262034852.001.0001.
J a m e s ,G . ,W i t t e n ,D . ,H a s t i e ,T . ,&T i b s h i r a n i ,R .( 2013).An
introduction to statistical learning: With applications in R.
SpringerT extsinStatistics.Springer .
Krumhansl, C. L. ( 1979). The psychological representation of
musicalpitchinatonalcontext. CognitivePsychology ,11(3),
346–374. https://doi.org/10.1016/0010-0285(79)90016-1
Laurson, M., Kuuskankare, M., & Norilo, V. ( 2009). An
overview of pwgl, a visual programming environment formusic.ComputerMusicJournal ,33(1),19–31. https://doi.org/
10.1162/comj.2009.33.1.19
Lerdahl, F. ( 1988). Tonal pitch space. Music Perception ,5(3),
315–349. https://doi.org/10.2307/40285402
Lerdahl,F.( 2001).Tonalpitchspace .OxfordU niversityPress.
Lerdahl,F.,&Jackendoff,R.( 1996).Agenerativetheoryoftonal
music.MITPress.repr.edition.
Lewin, D. ( 1959). Re: intervallic relations between two col-
lections of notes. Jo
 urnal of Music Theory ,3(2), 298.
https://doi.org/10.2307/842856
Lewin,D.( 2001).Specialcasesoftheintervalfunctionbetween
pitch-classsetsxandy . JournalofMusicTheory ,45(1),1–29.
https://doi.org/10.2307/3090647
Longuet-Higgins,H.C.(1987). Mentalprocesses:studiesincog-
nitivescience .Number1inExplorationsincognitivescience.
MITPress.
McCartney, J. ( 2002). Rethinking the computer music lan-
guage:supercollider. ComputerMusicJournal ,26(4),61–68.
https://doi.org/10.1162/014892602320991383
Messiaen, O. ( 1944).T echniquedemonlangagemusical ,V ol.1.
AlphonseLeduc.
Miller,R.( 1989).Anintroductiontomultidimensionalscaling
for the study of musical perception. Bulletin of the Council
forResearchinMusicEducation ,102,60–73.
M i l n e ,A .J . ,B u l g e r ,D . ,H e r ff ,S .A . ,&S e t h a r e s ,W .A .( 2015).
Perfect balance: A novel principle for the constructiono fm u s i c a ls c a l e sa n dm e t e r s .I nT .C o l l i n s ,D .M e r e d i t h ,&A .V o l k( E d s . ) , Mathematics and computation in music
(Vol. 9110, pp. 97–108). Springer International Publishing.https://doi.org/10.1007/978-3-319-20603-5_9.
Noll, T. (2010). Two notions of well-formedness in the orga-
nization of musical pitch. Musicae Scientiae ,14(1 suppl),
95–113.https://doi.org/10.1177/10298649100140S106N o l l ,T .( 2019). Insiders’ choice: studying pitch class sets
through their discrete fourier transformations. In Inter-
national Conference on Mathematics and Computation inMusic,pages371–378.Springer.
Parncutt, R., & hair, g. ( 2011). Consonance and dissonance
in music theory and psychology: Disentangling dissonantdichotomies. JournalofInterdisciplinaryMusicStudies ,5(2),
119–166.
Perle, G. ( 1977).Twelve-tone tonality . University of California
Press.
Persichetti, V. ( 1961).Twentieth-century harmony .W .W .N o r -
ton.
Polansky, L., Burk, P., & Rosenboom, D. ( 1990). Hmsl
(Hierarchical music specification language): A theoret-ical overview. Perspectives of New Music ,28(2), 136.
https://doi.org/10.2307/833016
Puck
ette, M. ( 1996). Pure data: Another integrated com-
puter music environment. In Proceedings, Second Intercol-
lege Computer Music Concerts, pages 37–41, Tachikawa,Japan.
Puckette, M. ( 2002). Max at seventeen. Computer Music Jour-
nal,26(4), 31–43. https://doi.org/10.1162/014892602320
991356
Quinn, I. (2004). A unified theory of chord quality in equal
temperaments.Phd,U niversityofRochester .
Quinn,I.(2006).Generalequal-temperedharmony(Introduction
and part i). Perspectives of New Music ,44(2), 114–158.
https://doi.org/10.1353/pnm.2006.0010
Quinn, I. (2007). General equal-tempered harmony: Parts 2
and3.PerspectivesofNewMusic ,45(1),4–63. https://doi.org/
10.1353/pnm.2007.0016
Rohrmeier, M., & Pearce, M. ( 2018). Musical syntax i: The-
oretical perspectives. In R. Bader (Ed.), Springer hand-
book of systematic musicology (pp. 473–486). Springer
Berlin Heidelberg. https://doi.org/10.1007/978-3-662-550
04-5_25.
Shannon, C. ( 1949). Communication in the presence of noise.
ProceedingsoftheIRE ,37(1),10–21. https://doi.org/10.1109/
JRPROC.1949.232969
Shepard, R. N. ( 1982). Geometrical approximations to the
structure of musical pitch. Psychological Review ,89(4),
305–333. https://doi.org/10.1037/0033-295X.89.4.305
Simms, B. R. ( 2000).The atonal music of arnold schoenberg
1908–1923.OxfordUniversityPress. https://doi.org/10.1093/
acprof:oso/9780195128260.001.0001 .
Susanni, P., & Antokoletz, E. ( 2012).Music and twentieth-
centurytonality:Harmonicprogressionbasedonmodalityand
the interval cycles .N u m b e r1i nR o u t l e d g es t u d i e si nm u s i c
theory.Routledge,Taylor&FrancisGroup.
Swain,J.P.( 1997).Musicallanguages (1sted).Norton.
Taube, H. ( 1997). An introduction to common music. Com-
puter Music Journal ,21(1),
29. https://doi.org/10.2307/368
1213
T enney,J.( 1988).Ahistoryofconsonanceanddissonance .Excel-
siorMusicPublishingCompany.
Torgerson, W. S. ( 1952). Multidimensional scaling: I. Theory
andmethod. Psychometrika ,17(4),401–419. https://doi.org/
10.1007/BF02288916
Tymoczko,D.( 2008).Set-classsimilarity,voiceleading,andthe
fourier transform. Journal of Music Theory ,52(2), 251–272.
https://doi.org/10.1215/00222909-2009-017

## Page 21

JOURNAL OF NEW MUSIC RESEARCH 161
Tymoczko, D. ( 2010).Ageometryofmusic:Harmonyandcoun-
terpoint in the extended common practice. Oxford studies in
musictheory .OxfordU niversityPress.
Vassilakis, P. ( 2001) .A u d i t o r yr o u g h n e s se s t i m a t i o no fc o m -
plex spectra—roughness degrees and dissonance ratings ofharmonic intervals revisited. T h eJ o u r n a lo ft h eA c o u s t i c a l
SocietyofAmerica ,110(5),2755–2755.
White, C. W. (2013). An alphabet-reduction algorithm for
chordal n-grams. In D. Hutchison, T. Kanade, J. Kittler, J.
M. Kleinberg, F. Mattern, J. C. Mitchell, M. Naor, O. Nier-
strasz,C.PanduRangan,B.Steffen,M.Sudan,D .T erzopou-los, D. Tygar, M. Y. Vardi, G. Weikum, J. Yust, J. Wild,
&J .A .B u r g o y n e( E d s . ) , Mathematics and computation in
music(Vol.7937,pp.201–212).SpringerBerlinHeidelberg.
https://doi.org/10.1007/978-3-642-39357-0_16.
White, C. W., & Quinn, I. ( 2016). The yale-classical archives
corpus.Empirical Musicology Review ,11(1), 50. https://
doi.org/10.18061/emr.v11i1.4958Yust, J. (2015a).Applicationsofdfttothetheoryoftwentieth-
century harmony. In T. Collins, D. Meredith, & A.
Volk (Eds.), Mathematics and computation in music (Vol.
9110, pp. 207–218). Springer International Publishing.
https://doi.org/10.1007/978-3-319-20603-5_22.
Yust, J. (2015b). Schubert’s harmonic language and fourier
phase space. Journal of Music Theory ,59(1), 121–181.
https://doi.org/10.1215/00222909-2863409
Yust, J. (2016). Special collections. Journal of Music Theory ,
60(2),213–262. https://doi.org/10.1215/00222909-3651886
Yust, J. (2017). Probing questions about keys: Tonal distribu-
tions through the dft. In O. A. Agust´ınAquino, E. Lluis-
Puebla, & M. Montiel (Eds.), Mathematics and computation
in music(Vol. 10527, pp. 167–179). Springer International
Publishing. https://doi.org/10.1007/978-3-319-71827-9_13.
Yust, J. ( 2019). Stylistic information in pitch-class distri-
butions.Journal of New Music Research ,48(3), 217–231.
https://doi.org/10.1080/09298215.2019.1606833

