> **DEPRECATED** — This document describes the old AAC-only semantic space (v1.x).
> Superseded by [L³-BRAIN-SEMANTIC-SPACE.md](L³-BRAIN-SEMANTIC-SPACE.md) which covers
> the unified 104D L³ layer (8 groups α→θ) for the MusicalBrain. Retained for historical reference.

# L³ — Semantic Space for the AAC Model

> Musical Intelligence (MI) v1.2.0 — 2026-02-11
> The interpretation layer: giving meaning to autonomic computation.
> Scope: ARU-α2-AAC model only. Companion to L³-SRP-SEMANTIC-SPACE.md.
> Updated with deep research evidence + Swan Lake empirical validation (Section 9).

---

## 1. What Is L³ for AAC?

L³ for AAC provides the **semantic interpretation** of the 14D autonomic output.
Where the SRP L³ interprets dopaminergic reward, the AAC L³ interprets
physiological responses — what the body does when music moves you.

```
┌─────────────────────────────────────────────────────────────────┐
│                     L³ AAC SEMANTIC SPACE                        │
│                                                                  │
│  ┌─── Group α ── Computation Semantics (Level 1) ───────── 6D  │
│  │   Which pathways drive the ANS output?                       │
│  │                                                               │
│  ├─── Group β ── Neuroscience Semantics (Level 2) ────── 7D    │
│  │   Which ANS pathways? Sympathetic vs parasympathetic?         │
│  │                                                               │
│  ├─── Group γ ── Psychology Semantics (Level 3) ──────── 6D    │
│  │   Bodily awareness, arousal type, chill embodiment            │
│  │                                                               │
│  └─── Group δ ── Validation Semantics (Level 4) ──────── 7D    │
│      Direct physiological predictions, convergence with SRP      │
│                                                                  │
│  TOTAL L³: 26D interpretation for 14D computation                │
│  COMPLETE SEMANTIC FOOTPRINT: 14D + 26D = 40D                   │
└─────────────────────────────────────────────────────────────────┘
```

### AAC L³ vs SRP L³

| | SRP L³ | AAC L³ |
|---|--------|--------|
| Computation | 19D | 14D |
| L³ Interpretation | 45D | 26D |
| Ratio (interp/comp) | 2.37:1 | 1.86:1 |
| Focus | Brain regions, reward, aesthetics | ANS pathways, physiology, embodiment |
| Total | 64D | 40D |

AAC's L³ is smaller because its output dimensions are more directly
physiological — they already map closely to measurable quantities. SRP outputs
(wanting, liking, pleasure) are abstract psychological constructs that need
more interpretive layers to connect to observations.

---

## 2. Group α — Computation Semantics (6D)

These dimensions interpret WHAT the computation is doing at each frame —
which mechanisms and pathways drive the AAC output.

### α0: aed_contribution [0, 1]

**Formula**: Fraction of AAC dimensions driven primarily by AED mechanism
(aed_arousal, aed_expectancy, aed_dynamics, aed_onset_rate).

**What it reveals**: When high, the ANS response is driven by **emotional
arousal** — the body responds because the music is exciting. AED is the
primary mechanism (weight 1.0) for AAC, so α0 is typically dominant.

**Feeds from AAC**: E0 (aed_arousal), A0 (aed_arousal), A1 (aed_arousal),
A2 (aed_arousal), A3 (aed_arousal), A4 (aed_arousal), P0 (aed_arousal),
P2 (aed_onset_rate)

### α1: asa_contribution [0, 1]

**Formula**: Fraction of AAC dimensions driven primarily by ASA mechanism
(asa_segregation, asa_salience, asa_integration).

**What it reveals**: When high, the ANS response is driven by **auditory
scene organization** — the body responds because of how the sound is
structured (stream segregation, salience). High during complex, multi-
layered passages where scene analysis matters.

**Feeds from AAC**: E0 (asa_salience), A1 (asa_segregation), A3 (asa_salience),
P1 (asa_segregation), P2 (asa_salience)

### α2: cpd_contribution [0, 1]

**Formula**: Fraction of AAC dimensions driven primarily by CPD mechanism
(cpd_buildup, cpd_release).

**What it reveals**: When high, the ANS response is driven by **peak/chill
detection** — the body responds because a climactic moment is approaching
or occurring. CPD has weight 0.4 (tertiary), so α2 is typically subdominant.

**Feeds from AAC**: P0 (cpd_buildup)

### α3: direct_read_contribution [0, 1]

**Formula**: Fraction of AAC dimensions driven primarily by direct H³ reads
(energy_level, velocity_signal, stability, tempo_signal, etc.).

**What it reveals**: When high, the ANS response is driven directly by
**acoustic features** bypassing mechanisms — raw energy, tempo, stability.
Typical during passages with strong dynamic or rhythmic character.

**Feeds from AAC**: E0 (energy_level), A0 (velocity, accel), A1 (tempo),
A3 (stability), A4 (stability, baseline), P1 (periodicity, tempo),
P2 (energy_accel), F0 (future_energy), F1 (future_energy)

### α4: computation_certainty [0, 1]

**Formula**: Mean distance from 0.5 across all 12 sigmoid-based AAC
dimensions (excluding the 2 tanh dimensions: f06_ans_response, ans_composite).

```
α4 = mean(|AAC_σ[i] - 0.5|) × 2   for all σ-activated dims
```

**What it reveals**: When high, the system makes **confident ANS predictions**
— outputs near 0 or 1. When low, the system is uncertain. High certainty
during musically clear moments (loud climax, soft calm). Low certainty during
transitions.

### α5: sympathetic_parasympathetic_balance [-1, 1]

**Formula**: `tanh(scr + respr - hr - bvp - temp + 0.5)`

**What it reveals**: Net balance between sympathetic activation (SCR↑, RespR↑)
and parasympathetic dominance (HR↓, BVP↓, Temp↓). Unique to AAC — SRP has
no equivalent because it models psychology, not physiology.

| Value | ANS State | Musical Context |
|-------|-----------|----------------|
| > 0.5 | Strong sympathetic | Exciting, crescendo, climax approach |
| ≈ 0 | **Co-activation** | Both branches active (chills!) |
| < -0.5 | Strong parasympathetic | Calm, resolved, post-climax |

**Critical at chills**: This should show paradoxical **near-zero** values at
chill moments because both branches co-activate (SCR↑ + HR↓ cancel in the
net balance).

**Validated by Berntson 2D autonomic space** (Berntson et al. 1991): Autonomic
control is NOT a single reciprocal axis. It is a 2D space with four quadrants:
reciprocal sympathetic, reciprocal parasympathetic, co-activation, and
co-inhibition. Music chills occupy the **co-activation quadrant** — this is
exactly what α5 ≈ 0 captures. Confirmed causally: Peng 2022 showed PEP shortening
(sympathetic, d=-0.45) + RSA increase (parasympathetic, d=+0.38) simultaneously.

---

## 3. Group β — Neuroscience Semantics (7D)

These dimensions map AAC outputs to ANS pathways and brain structures.
Level 2: "What would a physiologist measure?"

### β0: hypothalamus_activation [0, 1]

**Formula**: `σ(0.4 × f04_emotional_arousal + 0.3 × current_intensity + 0.3 × ans_composite_abs)`

**Neuroscience**: Hypothalamus — the master ANS control center. Integrates
emotional arousal signals from amygdala and insula, then drives sympathetic
and parasympathetic outputs via brainstem nuclei.

### β1: brainstem_sympathetic [0, 1]

**Formula**: `σ(0.4 × scr + 0.3 × respr + 0.3 × (1 - bvp))`

**Neuroscience**: Sympathetic chain activation via brainstem intermediolateral
column. Drives SCR (eccrine glands), respiratory rate increase, and
vasoconstriction (BVP decrease). Validated by **Peng 2022**: pre-ejection period
(PEP) shortening (d=-0.45) during emotional music is a pure sympathetic index
— shorter PEP = stronger sympathetic drive. β1 should correlate with PEP change.

### β2: brainstem_parasympathetic [0, 1]

**Formula**: `σ(0.5 × (1 - hr) + 0.3 × bvp + 0.2 × temp)`

**Neuroscience**: Vagal (parasympathetic) activation via nucleus ambiguus
and dorsal motor nucleus. The vagal brake: slows HR at peak emotional moments,
vasodilation (BVP increase), peripheral warming. Validated by **Peng 2022**:
respiratory sinus arrhythmia (RSA) increase (d=+0.38) during emotional music is
a pure parasympathetic index. The co-occurrence of PEP↓ (β1↑) and RSA↑ (β2↑)
is the cardiac co-activation that defines the chill state.

### β3: insula_interoception [0, 1]

**Formula**: `σ(0.3 × chills_intensity + 0.3 × f04_emotional_arousal + 0.2 × |ans_composite| + 0.2 × perceptual_arousal)`

**Neuroscience**: Anterior insula — interoceptive awareness hub (Craig 2009).
Bridges bodily sensations with conscious emotional experience. When high, the
listener is **aware** of their bodily response to music.

### β4: sympathetic_tone [0, 1]

**Formula**: `low_pass(brainstem_sympathetic, τ=1000ms)`

**Neuroscience**: Tonic sympathetic state — the sustained baseline of
sympathetic activation, smoothed over ~1s. Changes slowly. Reflects overall
arousal level rather than phasic responses.

### β5: vagal_tone [0, 1]

**Formula**: `low_pass(brainstem_parasympathetic, τ=1000ms)`

**Neuroscience**: Tonic vagal state — baseline parasympathetic activation.
High vagal tone = resting, relaxed. Drop in vagal tone precedes sympathetic
activation (Porges polyvagal theory). During chills: vagal brake ENGAGES
paradoxically (vagal tone INCREASES briefly, RSA d=+0.38 per Peng 2022).
This paradoxical vagal engagement is the hallmark of co-activation.

### β6: ans_coherence [0, 1]

**Formula**: `1 - std(z_score(scr), z_score(hr), z_score(respr), z_score(bvp), z_score(temp))`

**Neuroscience**: How synchronized are the ANS markers? Low coherence = markers
are responding independently (typical at rest). High coherence = all markers
moving together (typical during strong emotional events). At chills:
moderate-low coherence because SCR and HR move in OPPOSITE directions.

---

## 4. Group γ — Psychology Semantics (6D)

These dimensions map AAC outputs to subjective bodily experience.
Level 3: "What does the listener feel in their body?"

### γ0: bodily_awareness [0, 1]

**Formula**: `σ(0.4 × chills_intensity + 0.3 × |ans_composite| + 0.3 × current_intensity)`

**Psychology**: Interoceptive sensitivity — how much the listener notices
their body's response to music. High during peak moments when physical
sensations (goosebumps, heart racing, breath catching) become conscious.
Low during background listening.

### γ1: arousal_type [-1, 1]

**Formula**: `tanh(driving_signal - f04_emotional_arousal)`

**Psychology**: What drives the arousal — **rhythm** (positive) or **emotion**
(negative)?

| Value | Type | Example |
|-------|------|---------|
| > 0 | Rhythm-driven | Fast dance music, strong beat |
| ≈ 0 | Mixed | Emotional and rhythmic simultaneously |
| < 0 | Emotion-driven | Slow, harmonically rich passage |

### γ2: chill_embodiment [0, 1]

**Formula**: `σ(3.0 × (chills_intensity - 0.5))`

**Psychology**: The physical sensation of chills/frisson — goosebumps, spine
tingles, piloerection. Steep sigmoid with threshold: chills are binary-like
events with graded approach. Maps directly to Guhn 2007 physiological
chill criteria. Note: Mori & Iwanaga 2017 identified **two chill subtypes**:
"cold chills" (goosebumps, sympathetic-dominant) and "warm thrills" (tears,
lump in throat, parasympathetic-dominant). γ2 primarily captures cold chills;
warm thrills manifest more in β2 and β5.

### γ3: tempo_body_coupling [0, 1]

**Formula**: `σ(0.5 × driving_signal + 0.3 × perceptual_arousal + 0.2 × respr)`

**Psychology**: How strongly the musical beat drives physical responses —
breathing synchronized to beat, body swaying, head nodding. Related to groove
(Janata 2012) but from the autonomic perspective.

### γ4: emotional_intensity_aac [0, 1]

**Formula**: `σ(0.5 × f04_emotional_arousal + 0.3 × current_intensity + 0.2 × chills_intensity)`

**Psychology**: AAC's estimate of emotional intensity. Should correlate with
SRP's pleasure signal but captures the **bodily** rather than psychological
dimension. A listener might report low emotional awareness but still show
high AAC emotional intensity (implicit emotional processing).

### γ5: habituation_index [0, 1]

**Formula**: `1 - (current_ans_response / peak_ans_response_in_window)`

Where `peak_ans_response_in_window` is the maximum |ans_composite| in the
last 30s of frames.

**Psychology**: Are ANS responses habituating? The brain down-regulates ANS
responses to repeated stimuli (Sokolov 1963). After the first chill, the
same passage may produce weaker responses. High habituation = the listener
has "adapted" to the stimulus.

---

## 5. Group δ — Validation Semantics (7D)

These dimensions are **predictions about directly measurable quantities**.
Level 4: "What should we see in the lab?"

### δ0: predicted_scr [0, 1]

**Formula**: `scr` (direct mapping from A0)

**Target**: Skin conductance response measured via GSR electrodes on
index/middle finger or thenar eminence.

**Evidence**: Meta-pooled SCR effect d=0.85 (Fancourt 2020; note: Egermann 2013
d=2.5 is inflated context-specific value). Causal: Ferreri 2019 levodopa → SCR ↑
(p=0.033). AAC's SCR should match measured SCR trajectory with r ≈ 0.4-0.6.
SCR impulse response: τ_rise ≈ 1-2s, τ_decay ≈ 3-6s (Boucsein 2012).

### δ1: predicted_hr_deceleration [0, 1]

**Formula**: `1 - hr` (inverted from A1)

**Target**: Heart rate deceleration measured via ECG R-R intervals.
Note: This predicts DECELERATION, not raw HR. High = HR is decelerating.

**Evidence**: Meta-pooled HR effect d=1.0-1.5 (Fancourt 2020; note: Egermann 2013
d=6.0 is inflated context-specific value). HR response is **biphasic**: brief
acceleration (+2-5 BPM, ~0.5s, sympathetic) then sustained deceleration
(-3 to -8 BPM, 2-5s, vagal brake). At chill moments: deceleration phase
co-occurs with SCR increase (co-activation, Peng 2022).

### δ2: predicted_respr_change [0, 1]

**Formula**: `respr` (direct mapping from A2)

**Target**: Respiration rate measured via chest/abdominal band or nasal
thermistor.

### δ3: predicted_bvp_change [0, 1]

**Formula**: `1 - bvp` (inverted — predicts vasoconstriction)

**Target**: Blood Volume Pulse amplitude measured via photoplethysmography
(PPG) on fingertip or earlobe. Predicts amplitude DECREASE during arousal.

### δ4: predicted_piloerection [0, 1]

**Formula**: `σ(4.0 × (chills_intensity - 0.6))`

**Target**: Piloerection (goosebumps) measured via goosebump camera (Benedek
& Kaernbach 2011) or EMG on forearm.

**Evidence**: de Fleurian & Pearce 2021: goosebumps occur in ~50% of chill
episodes. Very steep threshold — essentially binary.

### δ5: predicted_chill_button [0, 1]

**Formula**: `σ(5.0 × (chills_intensity - 0.5))`

**Target**: Self-report chill button press. Tolerance: ±2s (broader than SRP's
±1s because bodily awareness has longer latency than psychological awareness).

### δ6: srp_aac_convergence [0, 1]

**Formula**: Requires SRP output. `σ(3.0 × (SRP.pleasure × chills_intensity - 0.3))`

**Target**: PASS/FAIL — when SRP predicts high pleasure, AAC should predict
high chills intensity. This is the **unified cascade validation**: the DA
release modeled by SRP causally drives the ANS response modeled by AAC. High
convergence confirms the cascade is intact; low convergence flags a broken link.

**Evidence**: The DA→ANS causal chain is established:
- Ferreri 2019: levodopa ↑ DA → SCR ↑ (p=0.033)
- Mas-Herrero 2021: TMS disrupts IFG → ↓ pleasure AND ↓ ANS (d=0.81)
- Salimpoor 2011: pleasure (SRP) correlates with ANS composite (AAC) at r=0.71

Convergence means both output facets of the single neural cascade are tracking
the same upstream musical event — the physiological downstream of dopaminergic
reward.

---

## 6. Cross-Level Mapping Matrix

### AAC → L³ Input Matrix

| AAC Dimension | α (Comp) | β (Neuro) | γ (Psych) | δ (Valid) |
|--------------|----------|-----------|-----------|-----------|
| E0 f04_arousal | α0,α1 | β0,β3 | γ0,γ4 | — |
| E1 f06_ans_response | α5 | β0 | — | — |
| A0 scr | α0,α3 | β1 | γ0 | δ0 |
| A1 hr | α0,α3 | β2 | — | δ1 |
| A2 respr | α0 | β1 | γ3 | δ2 |
| A3 bvp | α0,α1,α3 | β1,β2 | — | δ3 |
| A4 temp | α0,α3 | β2 | — | — |
| I0 chills_intensity | — | β3 | γ0,γ2,γ4 | δ4,δ5,δ6 |
| I1 ans_composite | α5 | β0,β6 | γ0,γ5 | — |
| P0 current_intensity | α0,α2 | β0 | γ0,γ4 | — |
| P1 driving_signal | α1,α3 | — | γ1,γ3 | — |
| P2 perceptual_arousal | α0,α1,α3 | β3 | γ3 | — |
| F0 scr_pred_1s | α3 | — | — | — |
| F1 hr_pred_2s | α3 | — | — | — |

### Most Connected AAC Dimensions

| AAC Dim | L³ Connections | Role |
|---------|---------------|------|
| I0 chills_intensity | 8 | Core validation target — the chill signature |
| A0 scr | 5 | Primary sympathetic marker |
| E0 f04_arousal | 5 | Emotional arousal driver |
| I1 ans_composite | 5 | Multi-modal ANS integration |

---

## 7. Dimension Count Summary

```
┌──────────────────────────────────────────────────────────────┐
│                  AAC SEMANTIC FOOTPRINT                        │
│                                                                │
│  LEVEL 1 — Computation (AAC output)                           │
│    E: f04_emotional_arousal, f06_ans_response      2D         │
│    A: scr, hr, respr, bvp, temp                    5D         │
│    I: chills_intensity, ans_composite               2D         │
│    P: current_intensity, driving, perceptual        3D         │
│    F: scr_pred_1s, hr_pred_2s                       2D         │
│                                            ─────────          │
│                                 AAC Total: 14D                │
│                                                                │
│  L³ — INTERPRETATION                                          │
│                                                                │
│    Group α — Computation Semantics                             │
│      α0-α3: mechanism/pathway attribution          4D         │
│      α4: computation certainty                      1D         │
│      α5: sympathetic-parasympathetic balance        1D         │
│                                            ─────────          │
│                                  α Total:  6D                 │
│                                                                │
│    Group β — Neuroscience Semantics                            │
│      β0: hypothalamus activation                    1D         │
│      β1-β2: brainstem sympathetic/parasympathetic   2D         │
│      β3: insula interoception                       1D         │
│      β4-β5: tonic sympathetic/vagal tone            2D         │
│      β6: ANS coherence                              1D         │
│                                            ─────────          │
│                                  β Total:  7D                 │
│                                                                │
│    Group γ — Psychology Semantics                              │
│      γ0: bodily awareness                           1D         │
│      γ1: arousal type                               1D         │
│      γ2: chill embodiment                           1D         │
│      γ3: tempo-body coupling                        1D         │
│      γ4: emotional intensity (AAC)                  1D         │
│      γ5: habituation index                          1D         │
│                                            ─────────          │
│                                  γ Total:  6D                 │
│                                                                │
│    Group δ — Validation Semantics                              │
│      δ0-δ3: direct physiological predictions        4D         │
│      δ4-δ5: piloerection + chill button             2D         │
│      δ6: SRP-AAC convergence                        1D         │
│                                            ─────────          │
│                                  δ Total:  7D                 │
│                                                                │
│                                            ═════════          │
│                                  L³ Total: 26D                │
│                                                                │
│  ═══════════════════════════════════════════════════           │
│  COMPLETE AAC SEMANTIC FOOTPRINT: 14D + 26D = 40D             │
│  ═══════════════════════════════════════════════════           │
└──────────────────────────────────────────────────────────────┘
```

### Combined MI Semantic Footprint

```
SRP:   19D computation + 45D interpretation =  64D
AAC:   14D computation + 26D interpretation =  40D
                                               ────
                               Combined Total: 104D

With shared L³ dimensions deducted:
  δ6 srp_aac_convergence references SRP → counted once
  Shared Chill Test dimensions overlap with SRP δ11
                                               ────
                        Unique MI L³ footprint: ~100D
```

---

## 8. Implementation Notes

### Compute Order

L³ AAC dimensions are computed AFTER AAC model output:

```
AAC 14D (Level 1)
  │
  ├──► Group α (6D) — needs AAC outputs only
  ├──► Group β (7D) — needs AAC outputs + α5
  ├──► Group γ (6D) — needs AAC outputs + some β
  └──► Group δ (7D) — needs AAC + γ2 + SRP (for δ6)
```

**Cross-model dependency**: δ6 (srp_aac_convergence) requires SRP.pleasure.
This means AAC L³ δ-group must be computed after SRP completes. Since SRP
and AAC share the same EAR, this is naturally satisfied: EAR → mechanisms →
SRP → AAC → L³ SRP → L³ AAC.

### State Requirements

| Dimension | State Required | Reason |
|-----------|---------------|--------|
| β4 sympathetic_tone | Low-pass buffer (~172 frames) | 1s smoothing |
| β5 vagal_tone | Low-pass buffer (~172 frames) | 1s smoothing |
| γ5 habituation_index | 30s sliding window (~5168 frames) | Peak tracking |

### File Structure

```
mi/
├── language/
│   ├── aac/
│   │   ├── __init__.py    ← AACSemantics orchestrator: AAC → 26D
│   │   └── alpha.py       ← Group α: computation semantics (6D)
│   │   (β, γ, δ groups → future implementation)
│   └── srp/               ← (existing SRP L³)
```

---

## 9. Empirical Validation — Swan Lake (First Run)

> Tchaikovsky: Swan Lake Suite, Op. 20a — Scene (Swan Theme). Moderato
> Duration: 182.6s | 31,456 frames | 172.27 Hz

### 9.1 Raw AAC Output Summary

| Dimension | Mean | Std | Min | Max | Interpretation |
|-----------|------|-----|-----|-----|----------------|
| f04_emotional_arousal | 0.605 | 0.028 | 0.518 | 0.696 | Moderate-high baseline arousal throughout |
| f06_ans_response | 0.086 | 0.778 | -1.0 | 1.0 | Full range — highly dynamic |
| **scr** | **0.542** | **0.275** | **0.000** | **1.000** | Full sympathetic range — silent=0, climax=1 |
| hr | 0.576 | 0.027 | 0.306 | 0.626 | **Very stable** — parasympathetic tonus maintained |
| respr | 0.547 | 0.175 | 0.002 | 1.000 | Follows arousal, wide range |
| bvp | 0.593 | 0.013 | 0.557 | 0.625 | Near-constant (slowest ANS marker) |
| temp | 0.673 | 0.010 | 0.643 | 0.699 | Nearly flat (expected: slowest response) |
| **chills_intensity** | **0.496** | **0.108** | **0.190** | **0.773** | CI peaks in climax region |
| ans_composite | 0.429 | 0.065 | 0.222 | 0.585 | Moderate activation throughout |
| current_intensity | 0.594 | 0.039 | 0.480 | 0.700 | Tracks loudness curve |
| **driving_signal** | **0.863** | **0.041** | **0.293** | **0.902** | **Very high — strong vals rhythm** |
| perceptual_arousal | 0.538 | 0.286 | 0.000 | 1.000 | Full range |
| scr_pred_1s | 0.557 | 0.053 | 0.421 | 0.787 | SCR anticipation active |
| hr_pred_2s | 0.409 | 0.067 | 0.213 | 0.579 | HR deceleration forecast |

### 9.2 SRP-AAC Cascade Observations

**Corresponding SRP values** (same audio, same pipeline run):
- SRP pleasure: mean=0.756, max=0.940 — high pleasure throughout
- SRP wanting: mean=0.356, wanting->liking lag visible
- SRP prediction_error: -0.999 to 1.000 — full range
- SRP harmonic_tension: 0.010 to 1.000 — full range

#### Observation 1: SCR-HR Inverse Correlation (Co-Activation)

SCR (sympathetic) and HR (parasympathetic) show **inverse movement** during
emotional peaks. This matches the Peng 2022 co-activation finding exactly:

```
Climax region (130-160s):
  SCR → max (sympathetic activation)
  HR  → drops toward 0.3 (parasympathetic engagement)

  α5 (sympathetic-parasympathetic balance) → near zero at peaks
  = Berntson co-activation quadrant
```

#### Observation 2: CI Peaks Align with Climax

Chills intensity maximum (0.773) occurs in the known climax region
(130-160s), where the orchestra reaches full fortissimo with
the swan theme in augmentation. The CI formula decomposes as:

```
At CI peak:
  0.35 * SCR_peak  ≈ 0.35 * 0.85 = 0.298  (37.8%)
  0.40 * (1 - HR)  ≈ 0.40 * 0.70 = 0.280  (35.6%)
  0.25 * RespR     ≈ 0.25 * 0.78 = 0.195  (24.8%)
  ----- CI ≈ 0.773

  → All three ANS branches contribute, no single marker dominates
  → Consistent with Salimpoor 2009 multi-marker chills definition
```

#### Observation 3: Driving Signal Dominance

driving_signal (mean=0.863) is the highest AAC dimension. Swan Lake's
strong rhythmic structure (vals meter + orchestral attacks) drives
continuous tempo-body coupling. This matches Janata 2012: respiration
entrains to beat in metrically regular music (r=0.3-0.5).

#### Observation 4: ANS Marker Response Speed

| Marker | Std | Response | Neuroscience |
|--------|-----|----------|--------------|
| SCR | 0.275 | Fastest phasic | Eccrine glands, 1-2s latency |
| RespR | 0.175 | Fast | Respiratory center, <1s |
| HR | 0.027 | **Very slow** | Vagal brake, sustained |
| BVP | 0.013 | Slowest phasic | Vascular smooth muscle |
| Temp | 0.010 | Near-constant | Thermoregulation, minutes |

The temporal response hierarchy (SCR > RespR >> HR >> BVP > Temp) matches
known ANS physiology exactly. This validates the model's temporal dynamics
without any tuning — the structure emerges from the mechanism weights alone.

#### Observation 5: SRP Pleasure <-> AAC CI Correlation

SRP pleasure (normalized) and AAC chills_intensity (normalized) show
strong temporal correlation. Both track the same upstream musical events
through different pathways:

```
SRP path: prediction error -> DA release -> wanting -> pleasure
AAC path: DA release -> hypothalamus -> ANS cascade -> CI
                                    |
                                    +--- Ferreri 2019: DA causally drives ANS
```

### 9.3 Musical Structure Alignment

| Time | Musical Section | SRP Says | AAC Says |
|------|----------------|----------|----------|
| 0-5s | Intro | Low PE, low wanting | Low SCR, driving_signal drops |
| 5-30s | Opening Tremolo | Rising tension, PE volatile | SCR pulses, HR stable |
| 30-60s | Swan Theme (Oboe) | pleasure rises, wanting builds | emotional_arousal rises, HR begins drop |
| 60-95s | Development | tension fluctuates, PE peaks | SCR variable, driving_signal high |
| 95-130s | Buildup | wanting peak, DA ramps | SCR climbing, HR descending |
| **130-160s** | **Climax** | **pleasure max (0.94), liking peak** | **CI peak (0.773), SCR max, HR min** |
| 160-183s | Resolution | tension resolves, PE calms | SCR decays, HR recovers, CI drops |

The two models tell a **coherent narrative**: SRP describes the reward
psychology (wanting builds, pleasure peaks, liking follows), while AAC
describes the bodily response (sympathetic activates, vagal brake engages,
chills occur). They converge at the climax — the same moment that
maximizes pleasure also maximizes CI.

### 9.4 Cascade Visualization

See: `Lab/Experiments/Cascade/` for the 7-panel cascade visualization
showing all dimensions synchronized with audio waveform and musical moments.

Script: `Lab/visualize_cascade.py` — generates publication-quality
SRP-AAC unified cascade plots for any audio file.

---

*Related: [L³-SRP-SEMANTIC-SPACE.md](L³-SRP-SEMANTIC-SPACE.md) — SRP interpretation (sibling)*
*Related: [07-AAC-DATA-FLOW.md](../General/07-AAC-DATA-FLOW.md) — AAC pipeline trace*
*Back to: [00-INDEX.md](../General/00-INDEX.md) — Navigation hub*
