# Unknown

**Author:** Unknown  
**Subject:** N/A  
**Total Pages:** 12  
**Source File:** `Rus_Geometry.pdf`

---

## Page 1

Chapter 1 – The Five Components of Tonality
Analytical Expansion of Tymoczko’s A Geometry of Music
1TheFiveComponentsofTonal-
ity
Tymoczko defines tonality not as a historical stylistic
phenomenon, but as a combination of five indepen-
dently variable features, each of which can be measured,
manipulated, and analyzed both perceptually and math-
ematically.
1.1 Tonal Feature Vector
He introduces a tonal system as a five-dimensional
feature space:
Ttonal = (Cm,Ac,Hc,Mh,Ct)
•Cm: Conjunct melodic motion
•Ac: Acoustic consonance
•Hc: Harmonic consistency
•Mh: Limited macroharmony
•Ct: Centricity
1.2 Conjunct Melodic Motion ( Cm)
Definition: Preference for small melodic intervals,
enhancing continuity and voice separability.
Formula:
Smelody =1
nn−1/summationdisplay
i=1|pi+1−pi|
SmallerSmelodyvalues indicate more conjunct motion.
1.3 Acoustic Consonance ( Ac)
Definition: Preference for intervals with low beating
and roughness, associated with small integer ratios (2:1,
3:2, 5:4).
Model:
Ac∝/summationdisplay
i,jR(fi,fj)
WhereR(fi,fj)is a dissonance function between par-
tialsfiandfj.
1.4 Harmonic Consistency ( Hc)
Definition: The degree to which chords in a passage
share similar internal structure.
Metric:
Hc= 1−1
N2/summationdisplay
i,jdVL(Ci,Cj)
WheredVLmeasures voice-leading distance between
chords.1.5 Limited Macroharmony ( Mh)
Definition: The extent to which a passage restricts
pitch-class content over short spans.
Calculation:
Mh=1
|W|/summationdisplay
t∈W|PC(t)|
WithPC(t)the set of pitch classes active at time t.
1.6 Centricity ( Ct)
Definition: The emergence of a pitch-class as percep-
tual center based on frequency, resolution, and salience.
Centricity Function:
Ct(p) =w1f(p) +w2r(p) +w3s(p)
Where:
•f(p): Frequency of p
•r(p): Resolution role of p
•s(p): Structural salience of p
1.7 Overdetermination
Some harmonic constructs fulfill multiple tonal func-
tions. The C major triad (C–E–G):
•Has high consonance ( Ac)
•Allows efficient voice leading ( Cm)
•Fits within small pitch-class sets ( Mh)
•Functions as tonic ( Ct)
1.8 Tonal Profiles by Style
Tonal systems can be expressed as 5D vectors:
⃗T= (Cm,Ac,Hc,Mh,Ct)
Examples:
•Classical: (1,1,1,1,1)
•Romantic: (1,1,0.8,0.6,0.9)
•Modal jazz: (1,1,0.7,0.5,0.4)
•Atonal: (0.4,0.2,0.3,1,0)
1.9 Perceptual Simulation Framework
Tymoczko proposes an experiment: generate six se-
quences, progressively adding features.
1. Random chords
2. + Conjunct melodic motion
3. + Harmonic consistency
4. + Acoustic consonance
5. + Limited macroharmony
6. + Centricity
1

## Page 2

Listeners are expected to perceive increasing tonal
coherence across steps.
1.10 R3System Mapping
Table 1: Tonal features mapped to R3modules
Feature R3Module Application
Cm CRV Temporal Perceptual
Stability (TPS)
Ac OL / PR Spectral alignment,
overtone-locking
Hc RFM Field coherence, har-
monic flow
Mh RFM Pitch-class boundary
in local windows
Ct PR / CRV Phantom root, center
identification
2 Harmony and Voice Leading
Tymoczko expands the definition of harmony and voice-
leading by integrating distance metrics, geometric chord
spaces, and transformational equivalence classes.
2.1 Linear Pitch and Pitch-Class Space
Pitch is modeled using a logarithmic mapping of fre-
quency:
p= 69 + 12·log2/parenleftbiggf
440/parenrightbigg
Pitch classes are modeled in circular modular space:
Rmod 12
Intervals are directional and cyclic.
2.2Transformations: Transposition and Inver-
sion
Transposition:
Tx(p) =p+x
Inversion:
Ix,y(p) = (x+y)−p
Fixed Point:
f=x+y
2
These operations define symmetry-based transforma-
tion behavior.
2.3 Voice-Leading Distance
Given chords P= (p1,...,pn)andQ= (q1,...,qn):
d(P,Q) = min
σ∈Snn/summationdisplay
i=1|pi−qσ(i)|
Here,σis a permutation that minimizes motion.2.4 OPTIC Equivalence
OPTIC framework defines chordal identity under:
•Octave equivalence (O)
•Permutation of voices (P)
•Transposition (T)
•Inversion (I)
•Cardinality change (C)
2.5 Geometric Chord Spaces
Chords are positioned in spaces such as:
•R2/S2for dyads
•Möbius strip or torus for triads
•Rn/Snfor general chords
These topologies support smooth harmonic naviga-
tion.
2.6 Near-Identity Transformations
Chords are near-identical if:
dVL(C1,C2)≤ϵ
for perceptual threshold ϵ(e.g. 2 semitones total).
2.7 Perceptual and Structural Implications
Efficient voice-leading:
•Reduces cognitive load
•Supports continuity and recall
•Aligns with auditory stream formation
2.8 R3System Integration
Table 2: Chapter 2 concepts mapped to R3modules
Concept R3Module Application
Voice-leading
metricRFM∇Φresonance
field gradient
OPTIC identity
setPR Chord class equiv-
alence
Inversion/t.pos. RFM/PR Symmetry trans-
formations
Near-identity
filteringCRV Fusionandsimilar-
ity modeling
Directional
motionCRV Tonal flow vector
computation
2.9 Summary
Tymoczko redefines harmony and chord progression as
geometry-driven field navigation. The tools presented
here integrate naturally into R3’s resonance modeling
infrastructure.
2

## Page 3

3 A Geometry of Chords
Tymoczko models harmony as movement through
chordal spaces structured by voice-leading distance and
transformational equivalence. Chords are geometric
objects; harmonic progressions trace paths over these
objects in a tonal field.
3.1 Ordered Pitch Collections
Chords are initially defined as ordered n-tuples:
P= (p1,p2,...,pn), pi∈R
with ascending order: p1≤p2≤···≤pn
3.2 Symmetric Quotient Spaces
To remove ordering redundancy:
Cn=Rn/Sn
Thistreatspermutationsofthesamenotesasequivalent,
forming a unique point in chord space.
3.3 Two-Note Chord Space
2-note chords form a triangle in R2/S2: - Hypotenuse
= unison - Voice-leading measured with Euclidean or
L1 norm
3.4 Three-Note Chord Space
Triads exist in Möbius strips or triangular toroidal
topologies depending on inversion and transposition
collapse.
dVL(Ci,Cj) =/summationdisplay
|pi−qi|
3.5 Voice-Leading Lattices
Chords form a network: - Nodes = chords - Edges =
minimal voice-leading transitions
3.6 Motion Types
Types of motion:
•Parallel: same direction
•Contrary: opposite directions
•Oblique: one voice static
3.7 Harmonic Consistency in Geometry
Voice-leading consistency:
dVL(Ci,Cj)≤ϵ
suggests harmonic similarity. Compact regions in chord
space produce tonal coherence.
3.8 Mars vs. Venus Metaphor
- Triads (Mars): regular, resolved, directionally sta-
ble - Sevenths (Venus): asymmetrical, chromatically
unstable
Each functions differently within harmonic flow fields.3.9 R3System Integration
Table 3: Chapter 3 features mapped to R3modules
Concept R3Module Application
Chordal geometry RFM Tonal resonance surface topology
Symmetric class-
ingPR Harmonic identity equivalence sets
Motion types CRV Perceptual continuity, fusion modeling
Lattice graphs RFM Harmonic path traversal in field topology
Triad/7th logic PR / CRV Fusion index variation across harmonic categories
3.10 Summary
Chordal geometry provides the foundation for under-
standing harmony as a spatially navigable field. These
models enable AI and cognitive systems to simulate
and generate tonal behavior with structural awareness.
4 Scales
Scales are not only collections of pitches but also metric
frameworks that define how distance and structure are
perceived in tonal music. Tymoczko models scales as
measurement devices that structure harmonic behavior,
melodic contour, and modulation potential.
4.1 Scale as Ruler
A scale allows musical distance to be measured by steps
rather than absolute frequency. For instance:
In C Major: C→G= 4steps (scale) ,7semitones (chromatic)
4.2 Scalar Transposition and Inversion
Scalar transposition: Motion within a scale’s struc-
ture.Interscalar transposition: Shifting material
between different scales.
In scalar inversion:
Ix,y(p) = (x+y)−p
mayresultinpitchesoutsidetheoriginalscale, requiring
reinterpretation.
4.3 Evenness and Scalar Construction
Evennessdescribeshowevenlyascaledividestheoctave.
Common scales:
•Diatonic: mixed whole/half steps – moderate even-
ness
•Whole-tone: only whole steps – high evenness
•Octatonic: alternating half-whole – symmetrical
Scales are generated using modular arithmetic over
pitch class space.
4.4 Constructing Common Scales
Examples of scale construction via interval cycles:
•Diatonic:W−W−H−W−W−W−H
•Whole-tone: step = 2 semitones
•Octatonic: alternating 1–2 or 2–1
These can be defined formally using modulo 12 arith-
metic and group actions.
3

## Page 4

4.5Modulation and Voice Leading Between
Scales
Efficient modulation depends on:
•Shared pitch classes
•Minimum voice-leading motion
•Centric alignment
Voice-leading between scales:
d(S1,S2) = min/summationdisplay
|pi−qi|
4.6 Interscalar Pathways
Progressions may move through different scalar fields:
C Major→A Minor→F Whole-Tone
These create modulation vectors in high-dimensional
harmonic space.
4.7Chromatic Modulation Over Scalar Con-
texts
Composers often layer chromatic material over scalar
frameworks. Example: Debussy and Reich apply non-
diatonic colors to modal or symmetrical scales.
4.8 Perceptual Implications
Scalar systems impact:
•Tonal predictability
•Memory retention
•Fusion strength
Higher evenness typically yields smoother cognitive
assimilation (CRV relevance).
4.9 R3System Integration
Table 4: Chapter 4 features mapped to R3modules
Concept R3Module Application
Scale structure RFM Scalar field as resonance geometry
Evenness metric RFM Spectral uniformity, balance in tonal field
Interscalar modu-
lationPR / CRV Phantom root drift and center shift
Chromatic over-
laysRFM Over-field layering and ambiguity modeling
Fusion and learn-
ingCRV Spectral–statistical congruence, TPS modulation
4.10 Summary
Scales serve as perceptual rulers and harmonic contain-
ers. Tymoczko’s framework allows us to model scalar
behavior dynamically across time, space, and transfor-
mation. R3uses this logic to map tonal flow and scalar
influence on perception and harmonic resonance.
5Macroharmony and Centricity
This chapter explores two high-level tonal features:
macroharmony and centricity. Tymoczko frames these
as essential, yet independently variable components of
tonal organization across time and style.5.1 Macroharmony Defined
Macroharmony refers to the total pitch-class collection
active in a span of time. It reflects the harmonic domain
within which motion occurs.
Formal definition:
Mh=1
|W|/summationdisplay
t∈W|PC(t)|
Where:
•W: time window
•PC(t): pitch-class set at time t
5.2 Macroharmonic Constraints
Tonal music tends to restrict |PC(t)|to 5–8 classes,
supporting scalar coherence. Atonal works often exceed
10.
5.3 Pitch-Class Circulation
Circulation measures the rate of change across pitch
classes. Low circulation = repetitive, scalar-like; high
= chromatic saturation.
5.4 Macroharmonic Consistency
Consistency refers to coherence in macroharmony across
time. Frequent changes suggest instability; slow evolu-
tion promotes centric perception.
5.5 Centricity Defined
Centricity refers to the emergence of a pitch-class as a
perceptual center or tonic.
Centricity function:
Ct(p) =w1f(p) +w2r(p) +w3s(p)
Where:
•f(p): frequency of pitch class p
•r(p): resolution likelihood
•s(p): structural salience (finality, metric position,
register)
5.6 Origins of Centricity
Centricity may emerge through:
•Statistical usage
•Melodic gravity
•Voice-leading asymmetry
•Harmonic resolution
5.7 Tonality Space
Tymoczko proposes a triangular tonal map:
•Diatonic-centric
•Chromatic-centric
•Acentric
Each point in this space reflects a different tonal
configuration.
4

## Page 5

5.8 Chromatic and Scalar Traditions
•Chromatic-centric : Brahms, Wagner, jazz
•Scalar-centric : Debussy, Messiaen, minimalism
Despitedifferentmechanisms, bothcanexhibitstrong
centricity.
5.9 R3System Integration
Table 5: Chapter 5 features mapped to R3modules
Concept R3Module Application
Macroharmony RFM Resonance field boundary shaping
Pitch-class circula-
tionCRV Temporal density, perceptual load
Macroharmonic
consistencyRFM Field coherence over time
Centricity func-
tionPR / CRV Phantom root location, center gravity
Tonality triangle RFM / PR Tonal vector classification
5.10 Summary
Macroharmony delimits the tonal space of a passage;
centricity provides gravitational pull. Tymoczko mod-
els both in terms of pitch-class usage, structural roles,
and perceptual weighting. Together, they inform the
dynamic behavior of tonal systems within the R3frame-
work.
6The Extended Common Prac-
tice
Tymoczko argues that tonality should not be confined
to a historical style period (e.g., 1600–1900). Instead,
it exists wherever the five tonal features co-occur in
meaningful ways. This defines the “Extended Common
Practice” (ECP).
6.1 Rethinking Tonal History
The five tonal features—conjunct motion, acoustic con-
sonance, harmonic consistency, macroharmony, and cen-
tricity—can exist in varied combinations across styles
and eras.
6.2 Medieval Counterpoint (2-Voice)
•Active features: Cm,Ac
•Minimal macroharmony
•No tonal centricity
6.3 Renaissance Triadic Texture
•Active:Cm,Ac,Hc
•3+1 voice leading
•Scalar macroharmony emerging
6.4 Classical Functional Tonality
•All five features active
•Strong tonic-dominant polarity
•High macroharmonic consistency6.5 Romantic Chromatic Expansion
•LargerMh(7–10 PC)
•Centricity preserved but more flexible
•Chromaticism via efficient voice-leading
6.6 20th Century Scalar Systems
•Modal and synthetic scales
•Non-functional centricity
•High evenness, stable Mh
6.7 Jazz as Structural Tonality
•Chromatic macroharmony
•Extended chords
•Scalar improvisation over functional forms
6.8 Tonal Feature Matrix
Table 6: Tonal features across historical styles
Style CmAcHcMhCt
Medieval ✓ ✓ – – –
Renaissance ✓ ✓ ✓ ∼✓∼✓
Classical ✓ ✓ ✓ ✓ ✓
Romantic ✓ ✓∼✓∼✓ ✓
20th Century ✓∼✓ ✓ ✓ ∼✓
Jazz ✓ ✓ ✓ ✓ ✓
6.9 R3System Integration
Table 7: Chapter 6 concepts mapped to R3modules
Concept R3Module Application
Feature mapping
across historyPR/CRV/RFM Tonal evolution by feature vector profile
Macroharmonic
expansionRFM Field curvature and entropy growth
Flexible centricity PR/CRV Phantom center shift, vector drift
Voice-leading
across stylesRFM Historical flow continuity modeling
Modal vs func-
tional overlayCRV Tonal ambiguity modeling
6.10 Summary
Tymoczko’s ECP redefines tonality as a combinatorial
system of structural features, not a style. The R3
system models how these features combine and evolve
across eras, styles, and cognitive representations.
7 Functional Harmony
Tymoczko reinterprets classical functional harmony
through the lens of geometric motion and voice-leading
efficiency. Rather than relying on abstract syntactic
rules, functional roles are modeled as spatial regions
and perceptual flows.
5

## Page 6

7.1Functional Syntax as Voice-Leading Pat-
terns
Traditional progressions such as:
I→vi→IV→ii→V→I
can be viewed as motion across functionally defined
zones:
•Tonic (T) : gravitational center
•Subdominant (S) : preparatory
•Dominant (D) : directional resolution
Each zone reflects clustering in chord space and ori-
entation toward tonal targets.
7.2 Voice-Leading Between Functions
Function zones are connected via minimal movement: -
I to V: two semitones (B–C, D–E) - ii to V: voice-leading
symmetry
Tymoczko models this as:
Functional Flow≈∇Φtonal
7.3 Modulation as Re-Centering
Modulation involves the reassignment of field centers:
ΦC
tonic→ΦG
tonic
Voice-leading provides the pathway, and shared har-
monies (e.g., pivot chords) act as connectors.
7.4 Sequences and Tonal Directionality
Chord sequences are cyclic, often based on:
I–vi–ii–V,IV–ii–vi–I
They preserve internal structure while shifting cen-
tricity. Tymoczko sees these as tonal spirals on the field
surface.
7.5 Geometric Functional Spaces
Each harmonic function exists as a zone in chord space:
- Tonic zone = low potential well - Dominant = high
gradient slope - Subdominant = pre-gradient field
These regions are mapped in the resonance landscape.
7.6 Comparison with Schenkerian Models
Tymoczko critiques Schenker’s abstraction:
•Lack of dynamic modeling
•Insufficient geometric precision
•Ignores real-time perceptual continuity
Instead, he proposes a vectorial model of function-
based tonal flow.
7.7 R3System Integration
7.8 Summary
Functional harmony is not fixed but dynamic: a system
of converging vectors in tonal field space. R3integrates
these zones as tonal attractors, with vector flow model-
ing continuity, modulation, and structural function.Table 8: Chapter 7 concepts mapped to R3modules
Concept R3Module Application
Function zones RFM Tonal field partitioning
Voice-leading
grammarRFM / CRV∇Φflow between regions
Modulation path-
waysPR / RFM Dynamic phantom root shift
Sequence struc-
turesCRV Cognitive reinforcement patterns
Schenker alterna-
tivesPR / CRV Real-time flow vs. hierarchy
8 Chromaticism
Tymoczko explores chromatic harmony as an expansion
and transformation of functional tonality. Chromati-
cism is framed not as the dissolution of tonality but as
its evolution via extended voice-leading and resonance
field complexity.
8.1 Wagner and Deferred Resolution
The Tristan chord is a hallmark of deferred tonal reso-
lution:
F−B−D#−G#
This sonority:
•Is not immediately resolvable
•Does not belong to any single functional zone
•Encourages tonal ambiguity and field curvature
8.2 Chromatic Sequences in Brahms
Brahms uses:
•Common-tone modulation
•Enharmonic reinterpretation
•Pivot chords leading to distantly related keys
Voice-leading remains smooth despite chromatic ex-
pansion.
8.3 Major Third Systems in Schubert
Schubert often modulates by major thirds:
C→A♭→E
These keys form a triangle in pitch-class space and
promote circular tonal movement. Tymoczko models
this as motion over a toroidal field.
8.4 Tonal Tesseract in Chopin
Chopin’s progressions exist in multiple harmonic dimen-
sions:
•Scalar
•Chromatic
•Functional
•Enharmonic
This produces a **4D resonance structure** — Ty-
moczko metaphorically calls it a tonal tesseract.
6

## Page 7

8.5 Schoenberg and Structural Chromaticism
Pre-serial Schoenberg maintains:
•Local centricity
•Scalar logic
•Maximal chromaticism through efficient voice-
leading
Chromatic saturation does not eliminate tonal space
— it densifies it.
8.6 Ambiguity and Tonal Vectors
Chromaticism enables field overlap:
ΦT1∩ΦT2̸=∅
Tonal direction becomes a function of convergence
rather than resolution.
8.7 Fusion and Field Curvature
Voice-leading complexity reduces fusion: - Overlapping
fields blur center perception - Listeners experience float-
ing tonal gravity - Resolution is asymptotic, not binary
8.8 R3System Integration
Table 9: Chapter 8 concepts mapped to R3modules
Concept R3Module Application
Tristan ambiguity PR / CRV Phantom root suppression, instability
Common-tone
shiftsRFM Field overlap and modulation bridges
Major third modu-
lationRFM Toroidal field traversal
Tonal tesseracts RFM / CRV Multidimensional fusion space
Voice-leading satu-
rationCRV Fusion breakdown and perceptual haze
8.9 Summary
Chromaticism is not a break with tonality but its spa-
tial extension. Tymoczko models chromatic harmony
as overlapping fields, increased entropy, and gradient
softening. In R3, these are captured via vector diffusion,
non-Euclidean flow, and center ambiguity.
9Scales in Twentieth-Century
Music
In this chapter, Tymoczko explores the resurgence and
transformation of scale-based music in the twentieth
century. Composers moved away from functional tonal-
ity while retaining scalar coherence, resulting in diverse
forms of modal, synthetic, and chromatically inflected
practices.
9.1 Scale-Based Composition Techniques
Tymoczko identifies three compositional strategies:
•Chord-first: Harmony determines the scalar en-
vironment.•Scale-first: A scale governs harmonic and melodic
material.
•Subsetmethod: Restrictedpitchmaterialdefines
structural identity.
9.2 Chord-First Composition
Examples:
•Debussy’s Fêtes: harmonic sonorities generate
modal context
•Michael Nyman: minimal triadic cycles yield emer-
gent scalar behavior
These pieces prioritize voice-leading over diatonic
logic.
9.3 Scale-First Composition
Composers begin with a scale, then derive harmony and
contour:
•Debussy : whole-tone, pentatonic scales
•Janáček : modal scales with chromatic coloration
•Shostakovich : modal themes with scalar devel-
opment
•Steve Reich : diatonic minimalism with additive
rhythms
9.4 Subset Technique
A limited pitch set defines the material identity of a
piece:
•Stravinsky’s octatonic blocks
•Miles Davis’s modal cells
•Reich’s motivic repetition
•The Beatles’ pentatonic riffs
Subset scales often serve both harmonic and timbral
purposes.
9.5 Chromatic Scalar Blending
Many works employ modal structures layered with chro-
matic alterations: - Debussy’s scalar color shifts - Re-
ich’s superimposed tonal centers - Jazz modal improvi-
sation with altered extensions
9.6 Fusion, Function, and Form
Scalar techniques can support:
•Tonal fusion (coherence)
•Functional illusion (voice-leading drive)
•Formal design (tessellated repetition, additive
buildup)
9.7 Cognitive Implications
Scale-based composition supports:
•Learnability and memory
•Predictability with local ambiguity
•Center formation via repetition and salience
These align with R3’s CRV metrics.
7

## Page 8

Table 10: Chapter 9 concepts mapped to R3modules
Concept R3Module Application
Chord-first strat-
egyRFM / PR Field emergence from harmonic selection
Scale-first strategy RFM Field pre-configuration and constraint
Subset scalar de-
signCRV Perceptual focus and identity anchoring
Chromatic col-
orationRFM / CRV Spectral variation, ambiguity control
Scalar learnability CRV Temporal stability and tonal prediction
9.8 R3System Integration
9.9 Summary
Twentieth-century scale use reflects a rebalancing of
tonality: away from function, toward field logic. Ty-
moczko’s model reveals how scalar systems serve har-
monic, formal, and perceptual goals. R3supports this
viaconstraintmodeling, vectorfieldanalysis, andscalar-
centered cognition.
10 Jazz
Tymoczko presents jazz as a modern synthesis of scalar,
functional, and chromatic harmonic systems. Jazz har-
mony blends extended chord vocabularies, modal envi-
ronments, and real-time voice-leading logic.
10.1 10.1 Jazz Harmony Fundamentals
Jazz uses:
•Extended tertian harmony (7ths, 9ths, 13ths)
•Quartal voicings and modal harmony
•Modal scales: Dorian, Mixolydian, Lydian, etc.
These structures define harmonic regions rather than
strict progressions.
10.2 10.2 Chord Extensions and Alterations
Extended dominant chords:
G7→G7(b9, #9, #11, b13)
These imply altered scales and voice-leading strate-
gies, not just vertical color.
10.3 10.3 Quartal Harmony
Fourth-based voicings:
•Introduce harmonic ambiguity
•Emphasize openness and modal flavor
•Are core to McCoy Tyner and Herbie Hancock’s
sound
10.4 10.4 Tritone Substitution
Functional inversion:
G7→D♭7
This substitutes dominant chords a tritone apart by
exploiting their common internal tritone interval (B–F).10.5 10.5 Modal Scalar Systems
Improvisers apply scales over chords:
•Dorian over minor 7
•Mixolydian over dominant 7
•Lydian over major 7
•Altered scale over V7alt
Modes define horizontal continuity across static har-
mony.
10.6 10.6 Polytonality and Playing Out
Techniques for harmonic expansion:
•Polytonality : simultaneous overlapping keys
•Playing out : intentional dissonance for expressive
tension
Thesearemodeledasvectorialdeparturesandreturns
in tonal field space.
10.7 10.7 Functional Reinterpretation
In jazz:
•Functional identity is flexible
•Rhythm, timbre, and gesture support perceived
centricity
•Fusion depends on contour and convergence, not
syntax
10.8 10.8 R3System Integration
Table 11: Chapter 10 concepts mapped to R3modules
Concept R3Module Application
Extended chords RFM / PR Resonance field diversity, root ambiguity
Quartal harmony RFM Alternative topologies in chord space
Tritone substitu-
tionPR / RFM Field inversion and symmetrical flipping
Modal scalar sys-
temsRFM / CRV Scalar containment, modal field logic
"Playing out" tech-
niqueCRV Cognitive vector excursion from center
10.9 10.9 Summary
Jazz demonstrates that harmonic logic can be fluid,
emergent, and multimodal. Tymoczko frames jazz as a
multidimensionalfieldpractice. TheR3systemcaptures
its complex resonance patterns, dynamic centricity, and
chromatic mobility.
Appendix A — Measuring Voice-
Leading Size
Tymoczko introduces precise ways to quantify the dis-
tance between chords by computing the total voice-
leading size, using either continuous pitch spaces or
discrete approximations.
A.1 Ordered Chords as Vectors
Each chord is modeled as a vector of nreal numbers:
P= (p1,p2,...,pn), pi∈R
8

## Page 9

where each pirepresents a voice, ordered by pitch or
voice identity.
A.2 Permutation Matching
To compare unordered chords, all permutations are
considered:
d(P,Q) = min
σ∈Snn/summationdisplay
i=1|pi−qσ(i)|
Here,σis a permutation in the symmetric group Sn,
reassigning voices optimally.
A.3 Norm Definitions
L1 norm (taxicab):
dL1(P,Q) =n/summationdisplay
i=1|pi−qi|
L2 norm (Euclidean):
dL2(P,Q) =/radicaltp/radicalvertex/radicalvertex/radicalbtn/summationdisplay
i=1(pi−qi)2
Each norm defines a unique geometry and impacts
how proximity is interpreted in chord space.
A.4 Musical Implications
- Small voice-leading distances imply smoother transi-
tions. - Near-identity chords have small d(P,Q)values.
- Norms affect field curvature in tonal geometry.
A.5 R3System Integration
Table 12: Appendix A concepts in R3modules
Concept R3Module Application
Voice-leading met-
ricRFM Geometric resonance mapping
Permutational
matchingRFM Chordal equivalence within field
L1 / L2 proximity CRV Fusion similarity scaling
Vector continuity RFM / CRV Field flow and tonal directionality
A.6 Summary
Voice-leading distance is central to modeling harmonic
movement in R3. Tymoczko’s metrics provide the foun-
dation for calculating tonal vectors, harmonic fields,
and perceptual fusion zones.
Appendix B — Chord Geometry:
A More Technical Look
This appendix formalizes the geometric spaces under-
lying Tymoczko’s theory of chords. It focuses on
pitch-class vectors, symmetric quotient spaces, and the
construction of continuous and discrete topologies for
chordal analysis.B.1 Chord Space Definition
LetP= (p1,...,pn)∈Rnbe an ordered chord. Ty-
moczko considers the quotient space:
Rn/Sn
whereSnis the symmetric group acting by permuting
coordinates. This eliminates ordering redundancy and
focuses on content.
B.2 Compactification and Octave Modulo
To model pitch-class space:
Rmod 12
is used to fold the infinite pitch axis into a 12-tone
circle. When extended to ndimensions:
(Rmod 12)n/Sn
yields a compactified, symmetric, multi-dimensional
torus.
B.3 Simplicial and Lattice Structures
The fundamental domain becomes a simplicial region,
e.g., a triangle for 3-note chords. This space tiles under
transposition and inversion.
- Discrete models = tonal lattice graphs - Continuous
models = topological manifolds
B.4 Example Structures
•R2/S2= right triangle (2-note chords)
•T3/S3= Möbius strip, tetrahedral surface (triads)
•Higher dimensions yield complex manifolds for 4+
voice chords
B.5 Topological Properties
Chord space is: - Connected - Compact (under modulo)
- Non-orientable (in some projections) - Traversable via
continuous voice-leading paths
B.6 R3System Integration
Table 13: Appendix B concepts in R3modules
Concept R3Module Application
Chord space quo-
tientRFM / PR Topological field construction
Octave wrapping RFM Toroidal resonance domains
Symmetric simpli-
ficationPR Class identity under permutation
Path continuity CRV Tonal directionality, fusion potential
B.7 Summary
Chord geometry converts harmonic logic into spatial
topology. R3leverages these spaces to model voice-
leading flow, resonance curvature, and harmonic iden-
tity without symbolic dependency.
9

## Page 10

Appendix C — Discrete Voice-
Leading Lattices
Tymoczko proposes a model of harmonic motion based
on discrete voice-leading networks. These lattices pro-
vide a graph-theoretic view of chord transitions, en-
abling topological modeling of tonal proximity and
functional continuity.
C.1 Lattice Construction
Each chord (typically a triad) is a node in a graph.
Edges represent minimal voice-leading transitions: -
Typically, one note moves by a semitone - Graph is
undirected unless functional motion is encoded
C.2 Example: Triadic Lattice
For major and minor triads: - Each triad connects
to neighbors via minimal motion (e.g., C major to E
minor) - The graph resembles a **triadic Tonnetz**,
extended in multiple dimensions
C.3 Path Metrics and Tonal Distance
Graph-theoretic distance:
dgraph(C1,C2) =Minimum number of edges between
This acts as a discrete approximation to voice-leading
size and is closely related to perceptual similarity.
C.4 Cycles and Functional Motion
Lattices can encode: - Cadential cycles (e.g., ii–V–I)
- Modulatory loops (e.g., circle of fifths) - Sequences
(transposable harmonic paths)
C.5 Tonal Field Navigation
Voice-leading lattices allow: - Algorithmic generation
of smooth progressions - Perceptual modeling of direc-
tion and closure - Embedding of harmonic identities in
spatial layout
C.6 R3System Integration
Table 14: Appendix C concepts in R3modules
Concept R3Module Application
Chord graph net-
workRFM Tonal pathfinding in harmonic field
Graph distance
metricCRV Similarity and fusion modeling
Cycle topology RFM / PR Cadential and modulatory recurrence
Edge constraints RFM Efficient harmonic connectivity
C.7 Summary
Discrete voice-leading lattices offer a scalable and com-
putationally tractable model of harmonic motion. In
R3, they support field-based traversal, functional path
analysis, and perceptual continuity simulations.Appendix D — The Interscalar
Interval Matrix
This appendix introduces a tool to compare pitch-class
collections (scales) using a matrix that records the
interval content between every pair of elements in two
distinct scalar sets.
D.1 Definitions
Let:
S1={s1,s2,...,sn}, S 2={t1,t2,...,tm}
Eachsi,tj∈Z12. The interval function is:
I(si,tj) = (tj−si) mod 12
D.2 Example: C Major →Octatonic
Let:
S1={0,2,4,5,7,9,11}(C Major)
S2={0,1,3,5,6,8,10}(Octatonic)
Table 15: Interscalar Interval Matrix
0 1 3 5 6 8 10
00 1 3 5 6 8 10
210 11 1 3 4 6 8
48 9 11 1 2 4 6
57 8 10 0 1 3 5
75 6 8 10 11 1 3
93 4 6 8 9 11 1
111 2 4 6 7 9 11
D.3 Interpretations
- Frequent repetitions →shared interval content - Clus-
ters→congruent scalar motion - Sparse matrices →
frictional modulation
D.4 Scalar Fusion Index
Fusion potential defined by:
F(S1,S2) =Number of common intervals
n·m
HighFimplies scalar congruence and smooth modu-
lation potential.
D.5 Applications
Use cases include:
•Predicting scalar modulation smoothness
•Modeling tonal center blending
•Supporting scale-to-scale transitions in R3
10

## Page 11

Table 16: Appendix D concepts in R3modules
Concept R3Module Application
Interscalar matrix RFM Interval overlap and modulation mapping
Fusion index CRV Cognitive similarity of scalar fields
Modulation ten-
sionPR / CRV Transition complexity estimation
Pitch-class density RFM Field curvature in scalar transitions
D.6 R3System Integration
D.7 Summary
The interscalar interval matrix quantifies scalar congru-
ence. In R3, it supports modeling of resonance bridges,
voice-leading efficiency, and cognitive smoothness in
scalar modulation.
Appendix E — Scale, Macrohar-
mony, andLerdahl’s“BasicSpace”
This appendix compares Tymoczko’s field-based model
of tonality with Fred Lerdahl’s “Basic Space” from
*Tonal Pitch Space* (2001). While both are concerned
with perceptual stability and tonal centering, their
methodologies differ significantly.
E.1 Lerdahl’s Basic Space
Lerdahl models tonal space as hierarchical zones of
stability, based on:
•Scale degrees (diatonic hierarchy)
•Chord membership (triadic functions)
•Regional relationships (key area proximity)
Each pitch is assigned a stability value within a given
context.
E.2 Tymoczko’s Resonance Fields
In contrast, Tymoczko defines tonality geometrically:
Φ(p) =Resonance potential of pitch p
Tonal centers arise not from syntactic rules but from ge-
ometric regularity and efficient voice-leading flow across
chord space.
E.3 Macroharmony as Field Constraint
Macroharmony defines the boundary of active pitch-
classes in a passage. Tymoczko treats it as the "size" of
the tonal field:
Mh=|Active pitch-class set |
SmallerMhvalues→stronger centricity; larger Mh
→modal or ambiguous regions.
E.4 Differences in Tension Modeling
Lerdahl models tension as deviation from a referential
tonic.Tymoczko models tension as distance from a tonal
center within a spatial field:
T(p) =∥p−ct∥
wherectis the perceptual center and pis the current
pitch or chord.
E.5 Dynamic vs. Hierarchical Models
•Lerdahl→static tree of priorities
•Tymoczko →dynamic surface of gravitational pull
•R3→hybrid: geometric with perceptual weight-
ings
E.6 R3System Integration
Table 17: Appendix E concepts in R3modules
Concept R3Module Application
Tonaltensionmod-
elingCRV Dynamic vector pull toward center
Macroharmony
constraintRFM Field size and tonal density control
Tonal hierarchy vs
fieldPR / RFM Phantom root vs spatial center duality
Cognitive weight-
ingCRV Temporal perceptual stability (TPS)
E.7 Summary
While Lerdahl’s Basic Space is rooted in symbolic hier-
archy, Tymoczko’s geometry enables flexible, dynamic
tonal modeling. R3benefits from both: geometric con-
tinuity and perceptual force metrics to guide tonal flow
and structural clarity.
Appendix F — Study Problems
and Activities
This appendix provides a set of conceptual and analyti-
cal exercises for engaging with the geometrical models
presented in the book. It is designed for students, the-
orists, and musicians seeking to explore tonal space
through computation, drawing, and listening.
F.1 Voice-Leading Exercises
1.Calculate the voice-leading size (L1 norm) between
the following chord pairs:
•(C, E, G) and (D, F#, A)
•(E, G, B) and (G, B, D)
2. Repeat using L2 norm.
3.Identify the permutation that minimizes total mo-
tion.
F.2 Chord Geometry Visualization
1. Draw R2/S2for 2-note chords.
2. Mark major and minor thirds on your plot.
3.Extend to R3/S3by projecting triads in triangle
form.
11

## Page 12

F.3 Scalar Construction Tasks
1.Generate scales using the circle-of-fifths method
(e.g., diatonic).
2.Plot pitch-class distributions on the 12-point circle.
3.Compare scalar evenness of diatonic vs whole-tone.
F.4 Interscalar Analysis
1. Construct interscalar interval matrices between:
•C major and C melodic minor
•C major and octatonic
2. Count the number of shared intervals.
3. Evaluate modulation friction.
F.5 Tonal Field Navigation
1.Choose 5 chords and draw a minimal voice-leading
path between them.
2. Label path direction and pitch movement.
3. Identify any cadential or cyclical behavior.
F.6 Listening and Application Tasks
1.Choose a short piece by Debussy, Reich, or Schoen-
berg.
2.Map scalar regions, macroharmony, and centricity
over time.
3. Sketch a tonal flow diagram for the excerpt.
F.7 Suggested Software and Tools
•Mathematica or Python for interval matrix com-
putation
•Music21 for symbolic analysis and pitch-class data
•Graphviz or TikZ for lattice and graph drawing
•Sonic Visualiser for spectro-temporal overlays
F.8 Summary
These activities provide a hands-on approach to Ty-
moczko’s geometric model of tonality. By calculating,
drawing, and listening, users can internalize the topo-
logical and perceptual principles of tonal space.
12

