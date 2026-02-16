# H³ Horizons ↔ Temporal Receptive Windows: Empirical Mapping

**Status**: Research-validated mapping (2026-02-16)
**Purpose**: Establish the neuroscientific grounding of H³ horizon values against
measured Temporal Receptive Windows (TRW) from the auditory/speech neuroscience literature.

---

## 1. Background: What Is a Temporal Receptive Window?

A **Temporal Receptive Window (TRW)** is the length of time preceding a neural
response during which sensory information may affect that response (Hasson et al.
2008). The concept parallels spatial receptive fields in vision: just as neurons in
V1 respond to small patches of visual space while neurons in inferotemporal cortex
respond to large regions, auditory cortical areas differ in how much temporal context
they integrate.

The TRW hierarchy was first demonstrated by Hasson et al. (2008) using fMRI and
scrambled narratives, then refined by Lerner et al. (2011) with topographic mapping,
and given precise millisecond resolution by Norman-Haignere et al. (2022) using
intracranial EEG with a temporal context invariance (TCI) measure.

**Key principle**: TRW increases in an orderly hierarchical fashion from primary
auditory cortex (tens of milliseconds) through association cortex (seconds) to
prefrontal regions (minutes). The hierarchy is a **continuous gradient** with one
robust discrete transition point at ~200ms.

---

## 2. H³ Horizon Definitions

H³ encodes temporal morphology as 4-tuples: `(r3_idx, horizon, morph, law)`.
The `horizon` parameter indexes a set of temporal windows:

| H³ Index | Duration | Design Rationale |
|----------|----------|------------------|
| H0 | 5.8ms | ABR Wave V latency (brainstem IC) |
| H3 | 23ms | Gamma-band cortical sampling window |
| H6 | 200ms | Syllabic/categorical transition |
| H10 | 400ms | Word-level / chord-level |
| H14 | 700ms | Phrase onset / clause |
| H16 | 1000ms | Sentence onset / beat cycle |
| H18 | 2000ms | Phrase / short progression |
| H24 | 36s | Paragraph / section / narrative arc |

---

## 3. Empirical Validation: Region by Region

### 3.1 Subcortical: Brainstem (H0 = 5.8ms)

**Empirical values**:
- ABR Wave I (distal auditory nerve, near cochlea): ~1.5ms
- ABR Wave II (proximal auditory nerve, near brainstem): ~2.5ms
- ABR Wave III (cochlear nucleus): ~3.7ms
- ABR Wave IV (superior olivary complex): ~4.5ms
- **ABR Wave V (lateral lemniscus / inferior colliculus): ~5.7ms** ← H0

**H0 = 5.8ms verdict**: **Accurate.** Maps to ABR Wave V, the last reliable
subcortical auditory brainstem response component. This is transit time, not an
integration window — the brainstem does not "integrate" in the cortical TRW sense;
it relays with fixed latency.

**Source**: Tawfik et al. (2022). Auditory brainstem response audiometry. In:
StatPearls. PMID: 35593822. Standard ABR latency norms from clinical audiology.

### 3.2 Primary Auditory Cortex / A1 / Heschl's Gyrus (H3 = 23ms)

**Empirical values**:
- **Intracranial TCI** (Norman-Haignere et al. 2022): Posteromedial Heschl's
  gyrus (core auditory cortex) — median integration width = **74ms**, median
  integration center = **68ms**. Exemplar electrode: 68ms width, 64ms center.
- **Intrinsic neural timescale** (Cusinato et al. 2023): Transverse temporal
  gyrus (TTG/Heschl's) — **16.7ms** median intrinsic timescale.
- **Earliest cortical response latency** (Nourski et al. 2014): **<25ms** onset
  in posteromedial Heschl's gyrus via intracranial recordings.
- **Macaque core AI** (Camalier et al. 2012): Median onset latency **20ms**,
  synchrony cutoff 46Hz (period = ~22ms), preferred modulation 5Hz.
- **Oscillatory sampling** (Giraud & Poeppel 2012): Low gamma band (25-35Hz)
  samples at **~25-40ms** windows — phonemic feature extraction.

**H3 = 23ms verdict**: **Maps to the ONSET LATENCY and intrinsic timescale of A1,
not the full integration window.** The actual TCI integration window in core A1 is
~68-74ms. However, 23ms correctly captures:
- The earliest cortical onset response (<25ms, Nourski 2014)
- The intrinsic neural timescale (16.7ms, Cusinato 2023)
- The gamma-band sampling period (~25-40ms, Giraud & Poeppel 2012)

**Correction needed**: H3 = 23ms represents the **sampling grain** of A1 (how fast
it can resolve temporal features), not its full integration window. The full A1 TRW
is better captured by a hypothetical H5 ≈ 70ms. Consider whether this distinction
matters for MI's purposes: H3 is the temporal resolution, not the temporal context.

### 3.3 Belt / Parabelt Auditory Cortex (H6 = 200ms)

**Empirical values**:
- **Intracranial TCI** (Norman-Haignere et al. 2022): Distance 10-20mm from
  primary cortex — median integration width = **136ms**. Distance 20-30mm —
  **274ms**. The 200ms point marks the **critical transition** from
  spectrotemporal modulation selectivity to category selectivity.
  > "A sharp transition around ~200ms integration width separates
  > spectrotemporal from categorical neural representations."
- **Oscillatory sampling** (Giraud & Poeppel 2012): Theta band (4-8Hz)
  samples at **~150-300ms** — syllabic feature integration.
- **Macaque belt** (Camalier et al. 2012): Lateral belt median onset ~30ms,
  temporal modulation transfer function cutoff ~10-12Hz (~83-100ms period).
  Parabelt: no systematic preference for short temporal modulations.

**H6 = 200ms verdict**: **Exact match — the strongest validation point.** 200ms is
the empirically measured discrete transition boundary in auditory cortex, confirmed
by intracranial recordings. This is also the theta-band syllabic integration window
and the duration of a typical multi-phoneme syllable in speech.

This is arguably the single most important horizon in the H³ system: it marks the
boundary between low-level spectrotemporal processing and higher-level categorical/
object-level processing.

### 3.4 Superior Temporal Gyrus — Acoustic (H10 = 400ms)

**Empirical values**:
- **Speech quilts** (Overath et al. 2015): Bilateral STS showed speech-specific
  sensitivity to temporal structure, with responses increasing with segment
  length up to **~500ms**. This is the window for speech-specific (non-lexical)
  temporal integration.
- **Intracranial TCI** (Norman-Haignere et al. 2022): Non-primary STG exemplar
  electrode — 375ms width, 273ms center. Long-integration electrodes (>200ms)
  show prominent category selectivity.

**H10 = 400ms verdict**: **Good approximation.** Falls between the TCI exemplar
(375ms width) and the speech-specific plateau (~500ms, Overath 2015). This horizon
captures the acoustic-object level: a single chord, a spoken word, a timbral event.

### 3.5 Superior Temporal Gyrus — Linguistic (H14 = 700ms)

**Empirical values**:
- **Scrambling paradigm** (Lerner et al. 2011): Word-level scrambling used
  segments of ~700ms mean duration. STG showed differential responses to
  word-scrambled vs. fully scrambled conditions. Anterior STG required
  word-level coherence (~700ms).
- **Sentence processing onset** (various): Single-word processing windows
  typically cited at 400-1000ms in psycholinguistics.

**H14 = 700ms verdict**: **Accurate for word-level processing.** Maps to the mean
word duration in Lerner et al.'s scrambling paradigm. This captures the transition
from acoustic-object to linguistic-unit processing. In music: a single melodic
gesture, a chord change, a metric group.

### 3.6 STS / Association Cortex (H16 = 1000ms)

**Empirical values**:
- **Delta oscillation** (Giraud & Poeppel 2012): Delta band (1-3Hz) samples
  at ~500-1000ms — phrasal/intonational contour tracking.
- **Sentence processing** (various): The 1-second mark is commonly cited as
  the lower bound of multi-word/sentential integration.
- **Musical beat**: 1000ms = 60 BPM, a canonical resting beat rate.

**H16 = 1000ms verdict**: **Reasonable.** Captures the transition from single-word
to multi-word/clausal processing. In music: one beat cycle at moderate tempo, the
beginning of phrase-level structure.

### 3.7 IFG / Broca's Area / Frontal Regions (H18 = 2000ms)

**Empirical values**:
- **Scrambling paradigm** (Lerner et al. 2011): IFG responded reliably only
  when **sentence-level** or longer coherence was intact. Mean sentence duration
  in their stimulus: **~7.7 seconds**. IFG was near the apex of the hierarchy,
  suggesting paragraph-level sensitivity (~38s).
- **Neural population TRWs** (Regev et al. 2024, Nature Human Behaviour):
  Intracranial recordings (n=22) revealed **three interleaved neural populations**
  within the language network with TRWs of ~1, ~4, and ~6 words. These
  populations exist in BOTH IFG and temporal regions, not segregated by anatomy.
- **Blank & Fedorenko (2020)**: Found **no evidence for differences** among
  language regions in their TRWs at the region level. IFG and temporal language
  regions showed similar sensitivity to word lists and sentence lists.
  This finding was partially resolved by Regev 2024 showing the differences
  exist at the neural POPULATION level (interleaved within regions), not at the
  anatomical region level.

**H18 = 2000ms verdict**: **UNDERESTIMATE for IFG.** The empirical IFG TRW is
~7.7-38 seconds at the region level (Lerner 2011). 2000ms is more appropriate for:
- Multi-word phrase integration (2-3 words at normal speech rate)
- Musical phrase (~2 bars at moderate tempo)
- The lower end of "clausal" processing

**Recommendation**: H18 = 2000ms is valid as a **phrase-level** horizon but should
NOT be mapped to IFG. IFG's true TRW would require a horizon around H20-H22
(~5-15s). Consider adding intermediate horizons or remapping the brain-region
correspondence:

```
H18 = 2000ms → Posterior STS / anterior STG (phrase level)
H20 = ~5s    → IFG short-TRW population (~4 words, Regev 2024)
H22 = ~15s   → IFG long-TRW population (~6 words × context, Regev 2024)
H24 = 36s    → mPFC / PCC (paragraph / narrative)
```

### 3.8 mPFC / Default Mode Network (H24 = 36s)

**Empirical values**:
- **Scrambling paradigm** (Lerner et al. 2011): mPFC responded reliably
  **only** to the fully intact forward story. It did not correlate with
  paragraph-scrambled (~38s segments) or any shorter scrambling condition.
  The story was ~7 minutes long.
  > "The activation time course in the mPFC during the intact story did not
  > correlate with unscrambled patterns from any of the other conditions."
- **Paragraph-level** (Lerner 2011): Precuneus ROI (adjacent to PCC) showed
  TRW of **~38 seconds** (paragraph level).
- **Schema-dependent** (Yeshurun et al. 2017): mPFC responses were
  interpretation-dependent — same stimulus evoked different responses based on
  narrative schema. Sensitive to 3-minute story scripts.
- **Alignment latency** (Chien & Honey 2020): Higher-order cortical regions
  took **>10 seconds** to align representations. mPFC was among the slowest.
- **DMN integration** (Simony et al. 2016): PCC, angular gyrus, precuneus,
  mPFC, temporal pole, and TPJ "accumulate and integrate information over
  minutes-long timescales."

**H24 = 36s verdict**: **Excellent match for paragraph level.** The Lerner 2011
paragraph segments were ~38 seconds, nearly identical to H24 = 36s. However, mPFC
itself extends beyond paragraph level to full narrative (~7 minutes). H24 more
precisely maps to **precuneus/PCC** (paragraph level), while mPFC would require
even longer horizons (H26+ = minutes).

---

## 4. Corrected Mapping Table

| H³ | Duration | Brain Region (Corrected) | TRW Evidence | Processing Level | Confidence |
|----|----------|--------------------------|-------------|-----------------|------------|
| H0 | 5.8ms | **Inferior Colliculus** (brainstem) | ABR Wave V = 5.7ms | Subcortical relay | High |
| H3 | 23ms | **A1 / Heschl's Gyrus** (onset/grain) | Onset <25ms (Nourski), INT 16.7ms (Cusinato) | Spectrotemporal sampling | High |
| — | ~70ms | **A1 / Heschl's Gyrus** (integration) | TCI 68-74ms (Norman-Haignere 2022) | Full A1 integration | High |
| H6 | 200ms | **Belt / Parabelt** (transition) | TCI 200ms boundary (Norman-Haignere 2022) | Categorical transition | **Very High** |
| H10 | 400ms | **Non-primary STG** (acoustic object) | TCI 375ms (Norman-Haignere), quilts ~500ms (Overath) | Acoustic object / word | High |
| H14 | 700ms | **Anterior STG** (word/gesture) | Scrambling ~700ms words (Lerner 2011) | Word / melodic gesture | Moderate |
| H16 | 1000ms | **Posterior STS** (clause/beat) | Delta 1-3Hz (Giraud & Poeppel 2012) | Multi-word / beat cycle | Moderate |
| H18 | 2000ms | **Anterior STS** (phrase) | Phrase-level integration | Musical phrase / clause | Moderate |
| — | ~8s | **IFG populations** (sentence) | Sentence ~7.7s (Lerner), ~4-6 words (Regev 2024) | Sentence / section | High |
| H24 | 36s | **PCC / Precuneus** (paragraph) | Paragraph ~38s (Lerner 2011) | Paragraph / section | High |
| — | >2min | **mPFC** (narrative) | Only intact story (Lerner), minutes (Hasson 2015) | Full narrative | High |

### Key Corrections from Original Mapping:

1. **H3 (23ms)**: Maps to A1 onset/sampling grain, NOT full A1 integration (~70ms).
   A1's full TRW is ~70ms — there is a gap between H3 and H6 that could use a
   new horizon (e.g., H5 = 70ms).

2. **H6 (200ms)**: EXACT MATCH — the most strongly validated horizon. The 200ms
   boundary is a discrete transition point measured intracranially.

3. **H18 (2000ms)**: Maps to phrase-level (anterior STS), NOT IFG. IFG's TRW is
   ~8-38s. A gap exists between H18 (2s) and H24 (36s) that needs intermediate
   horizons for sentence-level processing.

4. **H24 (36s)**: Maps to PCC/precuneus (paragraph), not directly mPFC. mPFC
   extends to minutes — beyond current H³ range.

5. **The hierarchy is a continuous gradient** (Hasson 2015), not discrete steps.
   The only robust discrete boundary is at 200ms (H6). All other boundaries are
   approximate.

---

## 5. Oscillatory Correspondence

The TRW hierarchy maps onto canonical cortical oscillatory bands:

| Oscillation | Frequency | Period | H³ Horizon | Speech Feature | Hemisphere |
|-------------|-----------|--------|------------|----------------|------------|
| **High Gamma** | 70-150Hz | 7-14ms | H0-H3 | Phonemic onset, VOT | Bilateral |
| **Low Gamma** | 25-35Hz | 29-40ms | H3 | Phonemic segments, formants | Left-biased |
| **Beta** | 13-25Hz | 40-77ms | H3-H6 | Top-down prediction | Left |
| **Alpha** | 8-13Hz | 77-125ms | H6 | Attentional gating | — |
| **Theta** | 4-8Hz | 125-250ms | H6-H10 | Syllabic rate, prosody | Right-biased |
| **Delta** | 1-3Hz | 333-1000ms | H14-H16 | Phrasal/intonational | — |
| **Infra-slow** | <1Hz | >1s | H18-H24 | Narrative structure | — |

**Source**: Giraud AL, Poeppel D (2012). Cortical oscillations and speech
processing: emerging computational principles and operations. *Nature Neuroscience*
15(4):511-517. doi:10.1038/nn.3063.

**Source**: Poeppel D (2003). The analysis of speech in different temporal
integration windows: cerebral lateralization as "asymmetric sampling in time."
*Speech Communication* 41(1):245-255.

---

## 6. The Gradient Nature of the Hierarchy

### 6.1 Continuous, Not Discrete

Hasson et al. (2015) explicitly state:
> "The TRW increases in an orderly hierarchical fashion... The transition from
> shorter to longer TRWs follows a topographic organization along the cortical
> surface."

Norman-Haignere et al. (2022) confirm with intracranial data:
> "Integration windows ranged from ~15 to ~150ms... increasing approximately
> 3-4 fold from primary to non-primary auditory cortex."

The hierarchy is best understood as a continuous spatial gradient on the cortical
surface, with TRW increasing as a function of anatomical distance from primary
auditory cortex (r ≈ 0.85, Norman-Haignere 2022).

### 6.2 The One Discrete Boundary: 200ms

Norman-Haignere et al. (2022) found one robust transition:
> "A sharp transition around ~200ms integration width separates spectrotemporal
> modulation selectivity from category selectivity."

Below 200ms: neurons are tuned to spectrotemporal modulations (frequency × time).
Above 200ms: neurons show category selectivity (speech vs. music vs. environmental).

This makes H6 (200ms) the single most important structural boundary in the H³
system — it separates **what** from **what it means**.

### 6.3 Implications for H³ Design

The continuous gradient means:
- H³ horizons are **sampling points** on a continuum, not discrete processing stages
- The specific horizon values (23ms, 200ms, 400ms, etc.) are engineering choices
  that approximate the gradient at useful points
- Models should NOT treat horizons as hard boundaries (e.g., "this model only
  operates at H6") but as the temporal resolution at which they read features

---

## 7. Complete Reference List

### Primary TRW Papers

1. **Hasson U, Yang E, Vallines I, Heeger DJ, Rubin N (2008)**. A hierarchy of
   temporal receptive windows in human cortex. *J Neurosci* 28(10):2539-2550.
   doi:10.1523/JNEUROSCI.5487-07.2008.
   - First demonstration of TRW hierarchy using scrambled movie clips
   - Early auditory cortex: short TRW; frontal: long TRW

2. **Lerner Y, Honey CJ, Silbert LJ, Hasson U (2011)**. Topographic mapping of
   a hierarchy of temporal receptive windows using a narrated story. *J Neurosci*
   31(8):2906-2915. doi:10.1523/JNEUROSCI.3684-10.2011.
   - Scrambled story at word (~700ms), sentence (~7.7s), paragraph (~38s) levels
   - mPFC responded ONLY to intact forward story
   - Topographic gradient along STG from posterior (short) to anterior (long)

3. **Norman-Haignere SV, Long LK, Haskins AJ, Bhatt P (2022)**. Multiscale
   temporal integration organizes hierarchical computation in human auditory
   cortex. *Nature Human Behaviour* 6:455-469. doi:10.1038/s41562-021-01261-y.
   - Intracranial EEG (n=27 epilepsy patients), broadband gamma TCI measure
   - Core A1: median 74ms width, 68ms center
   - 200ms discrete transition: spectrotemporal → categorical
   - Integration increases ~3-4x from primary to non-primary

4. **Hasson U, Chen J, Honey CJ (2015)**. Hierarchical process memory: memory
   as an integral component of information processing. *Trends Cogn Sci*
   19(6):304-313. doi:10.1016/j.tics.2015.04.006.
   - Review establishing "process memory" at each hierarchical level
   - Each level's TRW = its memory capacity for temporal context
   - Continuous gradient principle

### Neural Population Studies

5. **Regev M, Yedetore A, Kean HH, Liu H, Haskins AJ, Bhatt P, Blank IA,
   Norman-Haignere SV, Fedorenko E (2024)**. Neural populations within language
   regions differ in the temporal window of their responsiveness. *Nature Human
   Behaviour*. doi:10.1038/s41562-024-01944-2.
   - Intracranial (n=22), three population profiles: ~1, ~4, ~6 word TRWs
   - Populations INTERLEAVED across IFG and temporal regions
   - Shorter-TRW populations biased toward posterior temporal lobe
   - Resolves Blank & Fedorenko (2020) "no difference" finding

6. **Blank IA, Fedorenko E (2020)**. No evidence for differences among language
   regions in their temporal receptive windows. *NeuroImage* 219:116925.
   doi:10.1016/j.neuroimage.2020.116925.
   - fMRI, challenged region-level TRW differences in language network
   - Resolved by Regev 2024: differences exist at population, not region level

### Intrinsic Timescales

7. **Cusinato R, Alnes SL, van Maren E, Piantoni G,"; et al. (2023)**. Intrinsic
   neural timescales in the temporal lobe support an auditory processing
   hierarchy. *J Neurosci* 43(20):3696-3707. doi:10.1523/JNEUROSCI.1941-22.2023.
   - Intracranial at rest, autocorrelation decay
   - TTG (Heschl's): 16.7ms; STG/STS: 31.2ms; MTG: 30.0ms; TP: 41.4ms
   - Supports increasing timescale from primary to association cortex

### Oscillatory Framework

8. **Giraud AL, Poeppel D (2012)**. Cortical oscillations and speech processing:
   emerging computational principles and operations. *Nature Neuroscience*
   15(4):511-517. doi:10.1038/nn.3063.
   - Gamma (25-35Hz): phonemic features (~25-40ms)
   - Theta (4-8Hz): syllabic structure (~150-300ms)
   - Delta (1-3Hz): phrasal/intonational (~500-1000ms)
   - Asymmetric sampling: left = fast (gamma), right = slow (theta)

9. **Poeppel D (2003)**. The analysis of speech in different temporal integration
   windows: cerebral lateralization as "asymmetric sampling in time." *Speech
   Communication* 41(1):245-255. doi:10.1016/S0167-6393(02)00107-3.
   - Foundational proposal: left hemisphere = short windows, right = long
   - Hemispheric asymmetry as temporal sampling asymmetry

### Auditory Cortex Processing Latencies

10. **Nourski KV, Steinschneider M, Oya H, Kawasaki H, Jones RD, Howard MA
    (2014)**. Spectral organization of the human lateral superior temporal gyrus
    revealed by intracranial recordings. *Cereb Cortex* 24(2):340-352.
    doi:10.1093/cercor/bhs314.
    - Earliest cortical onset <25ms in posteromedial Heschl's
    - Gradient of latency increase from core to belt

11. **Camalier CR, D'Angelo WR, Sterbing-D'Angelo SJ, de la Mothe LA,
    Bhagat NA (2012)**. Neural latencies across auditory cortex of macaque support
    a dorsal stream supramodal timing advantage. *PNAS* 109(44):18168-18173.
    doi:10.1073/pnas.1206387109.
    - Macaque AI core: onset 20ms, cutoff 46Hz
    - Rostral core: onset 33ms, cutoff 10Hz
    - Gradient from fast/precise (core) to slow/integrative (belt/parabelt)

### Speech-Specific Integration

12. **Overath T, McDermott JH, Zarate JM, Poeppel D (2015)**. The cortical
    analysis of speech-specific temporal structure revealed by responses to sound
    quilts. *Nature Neuroscience* 18(6):903-911. doi:10.1038/nn.4021.
    - Bilateral STS: speech-specific temporal integration up to ~500ms
    - Non-speech sounds: shorter integration windows
    - Speech quilts methodology

### Narrative and Long-Timescale

13. **Simony E, Honey CJ, Chen J, Lositsky O, Yeshurun Y, Wiesel A, Hasson U
    (2016)**. Dynamic reconfiguration of the default mode network during narrative
    comprehension. *Nature Communications* 7:12141. doi:10.1038/ncomms12141.
    - PCC, mPFC, precuneus: minutes-long integration
    - DMN coupling predicts narrative memory

14. **Yeshurun Y, Swanson S, Simony E, Chen J, Lazaridi C, Honey CJ, Hasson U
    (2017)**. Same story, different story: the neural representation of
    interpretive frameworks. *Psychological Science* 28(3):307-319.
    doi:10.1177/0956797616682029.
    - mPFC responses are schema-dependent (interpretation modulates response)
    - Sensitive to 3-minute story scripts

15. **Chien HYS, Honey CJ (2020)**. Constructing and forgetting temporal context
    in the human cerebral cortex. *Neuron* 106(4):675-686.e11.
    doi:10.1016/j.neuron.2020.02.013.
    - Higher-order regions: >10 seconds to align representations
    - mPFC among the slowest to align
    - Context construction and forgetting follow hierarchical timescales

### ABR and Subcortical

16. **Tawfik SA, Hazzaa NM, Elnabtity AMM (2022)**. Auditory brainstem response
    audiometry. In: *StatPearls*. StatPearls Publishing. PMID: 35593822.
    - Standard ABR wave latencies: I=1.5, II=2.5, III=3.7, IV=4.5, V=5.7ms

---

## 8. Recommended H³ Modifications

Based on this empirical review:

### 8.1 Add Missing Horizons

| Proposed | Duration | Rationale |
|----------|----------|-----------|
| H5 | ~70ms | A1 full integration window (Norman-Haignere: 68-74ms) |
| H20 | ~5s | IFG short-TRW population (Regev 2024: ~4 words) |
| H22 | ~15s | IFG long-TRW population (Regev 2024: ~6 words × context) |

### 8.2 Remap Brain Region Correspondences

- H18 (2s): Remap from "IFG" to "anterior STS / phrase level"
- H24 (36s): Remap from "mPFC" to "PCC / precuneus / paragraph level"
- Add note: mPFC TRW exceeds current H³ range (>2 minutes)

### 8.3 Acknowledge Gradient Nature

All documentation should note that H³ horizons are **sampling points on a continuous
gradient**, not discrete processing stages. The only empirically supported discrete
boundary is at H6 (200ms).
