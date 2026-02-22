# MSPBA S-Layer — Extraction (3D)

**Layer**: Syntactic Processing (S)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | S0:musical_syntax | [0, 1] | mERAN response strength. IFG (BA 44) + right homologue activation. f25 = sigma(0.35 * pred_error.mean * x_l0l5.mean * roughness). Violation + coupling + dissonance = mERAN. Maess et al. 2001: mERAN localized in BA 44 (p=0.005, MEG, N=28). |
| 1 | S1:harm_prediction | [0, 1] | Harmonic prediction strength. BA 45 (pars triangularis) context accumulation. f26 = sigma(0.30 * harmony.mean * (1-entropy) * stumpf_fusion). Context + regularity + fusion = expectation. Patel 2003: SSIRH shared syntactic resources. |
| 2 | S2:broca_activation | [0, 1] | Domain-general Broca's activation. BA 44 syntactic processing load. f27 = sigma(0.35 * struct_expect.mean * familiarity.mean * (1-sethares)). Tachibana et al. 2024: bilateral BA 45 for musical syntax production (fNIRS, N=20). |

---

## Design Rationale

1. **Musical Syntax (S0)**: Tracks the mERAN (music-specific early right anterior negativity) response -- the neural signature of harmonic syntax violation. Uses prediction error multiplied by energy-consonance coupling (x_l0l5) and roughness. The multiplicative chain ensures that all three factors (surprise, coupling disruption, dissonance) must co-occur for a strong mERAN signal. Primary basis: Maess et al. 2001 MEG source localization.

2. **Harmonic Prediction (S1)**: Measures the strength of harmonic expectation based on accumulated context. Uses harmony context (from Brain pathway) multiplied by regularity (1-entropy) and tonal fusion (stumpf). High values mean the listener has built a strong harmonic expectation framework. Violation against strong context produces larger mERAN (2:1 ratio, position 5 vs position 3).

3. **Broca's Activation (S2)**: The domain-general syntactic processing load in Broca's area (BA 44). Uses structural expectation, familiarity, and consonance. This signal is shared between musical and linguistic syntax processing per the SSIRH (Patel 2003). Tachibana et al. 2024 confirmed bilateral BA 45 activation during improvisation.

---

## H3 Dependencies (S-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 10, 0, 2) | roughness value H10 L2 | Current dissonance at chord level |
| (0, 14, 1, 0) | roughness mean H14 L0 | Average dissonance over progression |
| (1, 10, 0, 2) | sethares_dissonance value H10 L2 | Current beating dissonance |
| (1, 14, 8, 0) | sethares_dissonance velocity H14 L0 | Rate of dissonance change |
| (3, 10, 0, 2) | stumpf_fusion value H10 L2 | Current tonal fusion |
| (3, 14, 1, 2) | stumpf_fusion mean H14 L2 | Fusion stability over progression |
| (5, 10, 0, 2) | inharmonicity value H10 L2 | Current harmonic deviation |
| (22, 10, 0, 2) | entropy value H10 L2 | Current harmonic unpredictability |
| (10, 10, 0, 2) | loudness value H10 L2 | Attention gating |
| (11, 10, 0, 2) | onset_strength value H10 L2 | Chord onset detection |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | S0: harmonic tension / violation |
| [1] | sethares_dissonance | S2: chord dissonance (Neapolitan signature) |
| [2] | helmholtz_kang | S1: harmonic template matching |
| [3] | stumpf_fusion | S1: tonal fusion (inverse violation) |
| [4] | sensory_pleasantness | S1: chord consonance quality |
| [5] | inharmonicity | S0: spectral deviation |
| [6] | harmonic_deviation | S0: partial misalignment |
| [10] | loudness | S0: attention gating |
| [11] | onset_strength | S0: chord onset salience |
| [22] | entropy | S0+S1: harmonic unpredictability |
| [23] | spectral_flux | S0: spectral change rate |
| [25:33] | x_l0l5 | S0: pitch-dissonance coupling (ERAN basis) |
| [33:41] | x_l4l5 | S0: temporal violation detection |
| [41:49] | x_l5l7 | S1: harmonic structure analysis |

---

## Scientific Foundation

- **Maess et al. 2001**: mERAN localized in BA 44 and right homologue, ~200ms latency (MEG, N=28, p=0.005)
- **Koelsch et al. 2000/2001**: ERAN for Neapolitan chord violations in non-musicians (EEG, p<0.001)
- **Patel 2003**: Shared Syntactic Integration Resource Hypothesis -- music + language share IFG resources (review)
- **Tachibana et al. 2024**: Bilateral BA 45 activation during guitar improvisation (fNIRS, N=20)
- **Kim et al. 2021**: IFG connectivity enhanced for syntactic irregularity (MEG, N=19, F=6.53, p=0.024)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mspba/extraction.py`
