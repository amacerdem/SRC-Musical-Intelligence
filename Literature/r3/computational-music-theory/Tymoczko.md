# Unknown

**Author:** Unknown  
**Subject:** N/A  
**Total Pages:** 2  
**Source File:** `Tymoczko.pdf`

---

## Page 1

Chapter 1 – The Five Components of Tonality
Deep Expansion of Tymoczko’s A Geometry of Music
1 Conceptual Framing
Tymoczko deﬁnes tonality as a perceptual and struc-
tural ﬁeld, not conﬁned to the common-practice era. It
emerges from ﬁve interrelated features, each measurable
and variably active across musical traditions.
2 Tonal Feature Vector Space
Let
Ttonal = (Cm, Ac, Hc, Mh, Ct)
Where:
•Cm: Conjunct melodic motion
•Ac: Acoustic consonance
•Hc: Harmonic consistency
•Mh: Limited macroharmony
•Ct: Centricity
Each component can be modeled, measured, and
interpreted both perceptually and mathematically.
3 Conjunct Melodic Motion ( Cm)
Cognitive Basis
Smallmelodicintervalsenhancestreamcoherence(Breg-
man, 1990) and align with expectations in tonal syntax.
Formula
Smelody =1
nn−1/summationdisplay
i=1|pi+1−pi|
Lower values of Smelodyindicate higher conjunctness.
4 Acoustic Consonance ( Ac)
Psychoacoustic Foundations
Preference for simple frequency ratios: octave (2:1),
ﬁfth (3:2), major third (5:4), etc. Supported by beating,
roughness, and fusion models.
Dissonance Integral
Ac∝/summationdisplay
i,jR(fi, fj)
Where R(fi, fj)is a roughness or dissonance function
between partials fiandfj.5 Harmonic Consistency ( Hc)
Deﬁnition
Consistency across chord progressions in interval struc-
ture or scale membership.
Voice-Leading Distance
Hc= 1−1
N2/summationdisplay
i,jdVL(Ci, Cj)
Where dVLis a measure of minimum voice-leading
movement.
6 Limited Macroharmony ( Mh)
Concept
Temporal limitation on pitch-class variety within a win-
dowW.
Calculation
Mh=1
|W|/summationdisplay
t∈W|PC(t)|
Where PC(t)is the pitch-class content at time t.
Thresholds
Tonal: 5–8 pitch classes
Chromatic: 10–12 pitch classes
7 Centricity ( Ct)
Components
Ct(p) =w1f(p) +w2r(p) +w3s(p)
•f(p): frequency of pitch class p
•r(p): resolution behavior
•s(p): metric and registral salience
Center Instability
Atonal or chromatic music may cause Ctvalues to
ﬂuctuate, leading to unstable or multiple centers.
1

## Page 2

8 Overdetermined Structures
Certain harmonic entities (e.g., major triad) satisfy
multiple tonal features simultaneously:
•High acoustic consonance
•Enables conjunct melodic movement
•Belongs to diatonic macroharmony
•Creates centricity in closure positions
9 Tonal Style Vectors
Each musical style or piece can be encoded as a feature
vector:
/vectorT= (Cm, Ac, Hc, Mh, Ct)
•Classical: (1, 1, 1, 1, 1)
•Romantic: (1, 1, 0.8, 0.6, 0.9)
•Modal jazz: (1, 1, 0.7, 0.5, 0.4)
•Atonal: (0.4, 0.2, 0.3, 1, 0)
This space allows for clustering, comparison, and
computational learning models.
10 Perceptual Testing Protocol
Tymoczko proposes an empirical paradigm for tonal
perception using constraint layers:
1. A: Random chords
2. B: Add conjunct motion
3. C: Add harmonic consistency
4. D: Add acoustic consonance
5. E: Limit macroharmony
6. F: Add centricity
Hypothesis: tonal perception increases monotonically
with added constraints.
11 R3System Integration
Table 1: Mapping tonal features to R3modules
Feature R3Module Functional Applica-
tion
Cm CRV Temporal Percep-
tual Stability (TPS),
melodic grouping
Ac OL / PR Consonance prediction,
overtone-locking align-
ment
Hc RFM Chordal ﬁeld unifor-
mity and topographic
coherence
Mh RFM Macroharmonic con-
ﬁnement in tonal
maps
Ct PR / CRV Phantom root tracking,
cognitive anchoring
2

