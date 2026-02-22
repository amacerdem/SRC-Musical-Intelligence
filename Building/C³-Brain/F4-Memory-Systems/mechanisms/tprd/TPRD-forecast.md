# TPRD F-Layer — Forecast (3D)

**Model**: Tonotopy-Pitch Representation Dissociation (IMU-β8)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:pitch_percept_fc | [0, 1] | Pitch percept prediction (50-200ms ahead). Based on pitch salience trajectory using brainstem horizon H3 (23.2ms). Predicts whether pitch clarity will strengthen or weaken. Uses _predict_future() with perceptual circuit pitch salience and H3 window. Tabas 2019: POR latency difference up to 36ms between consonant and dissonant dyads (MEG, N=37). |
| 8 | F1:tonotopic_adpt_fc | [0, 1] | Tonotopic adaptation prediction (200-700ms ahead). Based on harmony trajectory using H14 (700ms) horizon features. Predicts tonotopic map adaptation — how spectral encoding will shift as harmonic context evolves. Uses _predict_future() with mnemonic circuit harmony signal and H14 window. Briley 2013: adaptation paradigm revealed tonotopic vs pitch organization. |
| 9 | F2:dissociation_fc | [0, 1] | Dissociation evolution forecast (0.5-2s ahead). Based on structural expectation trajectory using H18 (2s) horizon features. Predicts how the tonotopy-pitch divergence will evolve. Uses _predict_future() with mnemonic circuit structure signal and H18 window. Cheung 2019: uncertainty-surprise interaction in auditory cortex modulates processing. |

---

## Design Rationale

1. **Pitch Percept Forecast (F0)**: Projects pitch percept strength 50-200ms ahead. This short-horizon prediction operates at the brainstem processing timescale, leveraging the fast pitch extraction chain (H0 -> H3 -> H6). Motivated by Tabas 2019 showing that consonant combinations are decoded faster (up to 36ms) in anterolateral HG, meaning pitch processing speed itself carries predictive information about the upcoming stimulus.

2. **Tonotopic Adaptation Forecast (F1)**: Projects tonotopic map state 200-700ms ahead. This medium-horizon prediction tracks adaptation of spectral encoding over harmonic progression timescales. As harmonic context changes (chord progressions, key changes), the tonotopic map load shifts. Uses H14 (700ms) trend features from the mnemonic circuit's harmony signal, aligned with the adaptation paradigm used by Briley 2013 to reveal tonotopic organization.

3. **Dissociation Forecast (F2)**: Projects the evolution of tonotopic-pitch divergence 0.5-2s ahead. This longer-horizon prediction captures how the balance between spectral and pitch processing will shift at the phrase level. Uses H18 (2s) horizon features from the mnemonic circuit's structural expectation signal. Supported by Cheung 2019 showing that uncertainty and surprise jointly predict auditory cortex activity in hippocampus and auditory cortex.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 18, 19, 0) | sensory_pleasantness stability H18 L0 | Consonance stability over phrase for dissociation forecast |
| (7, 6, 8, 0) | amplitude velocity H6 L0 | Energy change rate at beat level for tonotopic adaptation |
| (0, 14, 1, 0) | roughness mean H14 L0 | Average tonotopic load over progression |
| (5, 14, 1, 0) | inharmonicity mean H14 L0 | Average conflict over progression |
| (14, 6, 1, 0) | tonalness mean H6 L0 | Beat-level pitch clarity for pitch forecast |
| (17, 6, 14, 0) | spectral_autocorrelation periodicity H6 L0 | Beat-level harmonic periodicity for pitch trajectory |
| (22, 6, 0, 0) | entropy value H6 L0 | Spectral complexity at beat level |
| (22, 14, 1, 0) | entropy mean H14 L0 | Average complexity over progression |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F1: tonotopic trajectory input |
| [5] | inharmonicity | F2: conflict trajectory for dissociation |
| [14] | tonalness | F0: pitch clarity trajectory |
| [17] | spectral_autocorrelation | F0: harmonic periodicity trajectory |
| [22] | entropy | F1+F2: complexity trajectory |

---

## Brain Regions

| Region | Coordinates (Talairach) | Evidence | Function |
|--------|-------------------------|----------|----------|
| Anterolateral HG | L: -49.1, -21.2, 17.2 / R: 42.9, -5.5, 17.6 | Direct (EEG, Briley 2013 N=8; MEG, Tabas 2019 N=37) | Pitch prediction — consonance decoded faster in alHG |
| Bilateral STG | Bilateral (iEEG coverage) | Direct (iEEG, Bellier 2023 N=29) | Anterior-posterior organization — sustained (anterior) vs onset (posterior) |
| Heschl's Gyrus (medial) | L: -41.9, -18.8, 15.8 / R: 44.2, -13.4, 13.4 | Direct (EEG, Briley 2013 N=8) | Tonotopic adaptation prediction |

---

## Scientific Foundation

- **Tabas et al. (2019)**: POR latency difference up to 36ms for dissonant vs consonant dyads; consonance processing in alHG; model R2>0.90 (MEG, N=37)
- **Cheung et al. (2019)**: Uncertainty and surprise jointly predict auditory cortex, amygdala, hippocampus activity (fMRI, N=39)
- **Bellier et al. (2023)**: Anterior-posterior STG organization with sustained (anterior) vs onset (posterior) responses; R-STG dominance for music (iEEG, N=29, 2668 electrodes)
- **Briley et al. (2013)**: Adaptation paradigm revealed tonotopic vs pitch organization gradient (EEG, N=8-15)
- **Bidelman (2013)**: Brainstem FFR encodes consonance hierarchy — subcortical pitch processing supports fast pitch prediction (review)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/tprd/forecast.py`
