# MSR — Temporal Integration

**Model**: Musician Sensorimotor Reorganization
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | plv_high_freq | Raw PLV at 40-60 Hz. Continuous estimate of phase-locking value in the high-gamma range. Musicians: 0.40-0.44; nonmusicians: 0.28-0.31. Directly derived from f04 (E-layer). L. Zhang 2015: ascending trains PLV d = 1.04, descending trains PLV d = 1.13. |
| 4 | p2_amplitude | Normalized P2 amplitude. Tracks the vertex P2 potential at 155-180ms post-stimulus. Lower values indicate more efficient (trained) processing. Musicians: 1.46-3.29 uV; nonmusicians: 4.65-5.91 uV. L. Zhang 2015: P2 mean peak d = 1.16. |
| 5 | efficiency_index | PLV-P2 balance. Combined index: alpha * PLV - beta * P2 (normalized). Higher values indicate more efficient sensorimotor processing. Alpha=1.0 (PLV weight), beta=0.5 (P2 weight). Directly derived from f06 (E-layer). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 4 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 125ms — theta oscillation |
| 1 | 25 | 16 | M1 (mean) | L2 (bidi) | Mean coupling over 1s — long-term PLV baseline |
| 2 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s — beat-level PLV |
| 3 | 8 | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms — P2 amplitude input |
| 4 | 8 | 3 | M2 (std) | L2 (bidi) | Loudness variability 100ms — P2 modulation |

---

## Computation

The M-layer integrates the E-layer features into continuous mathematical estimates of the PLV/P2 system state:

1. **PLV high-frequency** (idx 3): Directly inherits from f04. Represents the continuous estimate of 40-60 Hz phase-locking strength. Uses additional coupling periodicity at theta (125ms) and beat (1s) horizons to track PLV stability across time scales. The PLV range [0.28, 0.44] from Zhang 2015 maps to [0, 1] via sigmoid.

2. **P2 amplitude** (idx 4): Computed from loudness features at 100ms horizon. Loudness value and variability at 100ms capture the stimulus properties that drive the P2 vertex response. Higher loudness variability maps to higher P2 (novel/unpredictable stimuli). The inverse relationship with training is implicit in the model — more predictable processing yields lower P2.

3. **Efficiency index** (idx 5): Directly inherits from f06. Represents the net PLV-P2 balance using alpha=1.0 (PLV weight) and beta=0.5 (P2 weight). This asymmetric weighting reflects that bottom-up enhancement (PLV) contributes more to overall efficiency than top-down suppression (P2 reduction).

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f04, f06 | PLV and efficiency features feed mathematical integration |
| R³ [8] | loudness | Perceptual intensity for P2 amplitude computation |
| R³ [25:33] | x_l0l5 | Motor-auditory coupling for long-term PLV baseline |
| H³ | 5 tuples (see above) | Theta/beat-scale periodicity and loudness dynamics |
