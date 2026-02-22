# SDNPS E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid (E0, E1, E2)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:nps_value | [0, 1] | Neural Pitch Salience proxy (FFR magnitude). sigma(0.40*tonalness*autocorr + 0.30*(1-inharm) + 0.30*trist_balance). Cousineau 2015: NPS from brainstem phase-locking. |
| 1 | E1:stimulus_dependency | [0, 1] | Generalization limit — high for synthetic (simple spectra), low for natural (complex). sigma(0.50*(1-complexity)*E0 + 0.50*roughness_period). Cousineau 2015: r=0.34 synth, r=0.24 sax, r=-0.10 voice. |
| 2 | E2:roughness_corr | [0, 1] | Roughness correlation (stimulus-invariant r=-0.57). sigma(0.57*roughness_mean). Cousineau 2015: NPS-roughness holds across ALL timbres. |

---

## Design Rationale

Three features model stimulus-dependent neural pitch salience (Cousineau et al. 2015):

1. **NPS Value (E0)**: Tonalness (harmonic-to-noise ratio) times spectral autocorrelation captures brainstem phase-locking quality. (1-inharmonicity) and tristimulus balance add spectral simplicity. Higher values = clearer FFR = stronger NPS.

2. **Stimulus Dependency (E1)**: NPS validity degrades with spectral complexity. The (1-complexity)*E0 term gates NPS by how "synthetic" the signal is. Roughness periodicity captures stimulus regularity at 200ms. This maps the r=0.34→0.24→-0.10 degradation curve.

3. **Roughness Correlation (E2)**: The one truly invariant relationship: NPS ↔ roughness r=-0.57 across all timbres. Stored as sigmoid(0.57 * roughness_mean) for layer consistency.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 6, 14, 0) | roughness periodicity H6 L0 | Stimulus regularity at 200ms |
| (0, 3, 1, 2) | roughness mean H3 L2 | Context mean for invariant correlation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| 5 | inharmonicity | Spectral deviation from harmonic series |
| 14 | tonalness | Harmonic-to-noise ratio (FFR quality proxy) |
| 17 | spectral_autocorrelation | Harmonic periodicity |
| 18 | tristimulus1 | Fundamental energy |
| 19 | tristimulus2 | Mid-harmonic energy |
| 20 | tristimulus3 | High-harmonic energy |

---

## Scientific Foundation

- **Cousineau 2015**: NPS from brainstem FFR predicts consonance for synthetic (r=0.34, p<0.03) but NOT natural sounds (sax r=0.24, voice r=-0.10)
- **Bidelman 2013**: Subcortical NPS graded for consonance; r~0.9 NPS-consonance across studies
- **Fletcher 1934**: Inharmonicity as spectral deviation from ideal harmonic series

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sdnps/extraction.py`
