# BARM E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:regularization_tendency | [0, 1] | Bias toward isochrony. f10 = sigma(0.35*(1-BAT)*groove_mean + 0.35*tempo_periodicity). Rathcke 2024: individuals with low BAT regularize rhythms toward isochrony (ER>19, N=87). |
| 1 | E1:beat_alignment | [0, 1] | Individual beat-alignment ability. f11 = sigma(0.40*beat_periodicity_1s + 0.30*onset_periodicity_1s). Grahn & Brett 2007: beat perception accuracy varies with motor system integrity (fMRI, N=27). |
| 2 | E2:sync_benefit | [0, 1] | Movement synchronization enhancement. f12 = sigma(...+0.30*coupling_period_1s + 0.30*(1-f11)*motor_mean). Hoddinott & Grahn 2024: movement benefit scales inversely with alignment ability (7T RSA). |

---

## Design Rationale

1. **Regularization Tendency (E0)**: Tracks the perceptual system's bias toward isochronous (equally-spaced) beat interpretation. Low beat-ability individuals show stronger regularization — they "fill in" regularity where none exists. Uses tempo periodicity at 500ms horizon (H8) to detect rhythmic regularity in the signal.

2. **Beat Alignment (E1)**: Measures how accurately the listener aligns internal beat representation with external rhythmic events. Uses H3 periodicity at 1s horizon for both spectral_flux and onset_strength — the two primary onset-detection channels. This is the core individual-difference variable (BAT score proxy).

3. **Sync Benefit (E2)**: Captures the movement-synchronization advantage. Lower-ability individuals (1-f11) paradoxically show greater motor enhancement when synchronizing — their motor system compensates for weaker perceptual alignment. Uses motor-auditory coupling features (x_l0l5) at 1s horizon.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (21, 8, 14, 0) | spectral_change periodicity H8 L0 | Tempo periodicity at 500ms — regularization signal |
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | Beat periodicity at 1s — main beat alignment |
| (11, 16, 14, 2) | onset_strength periodicity H16 L2 | Onset periodicity at 1s — confirms beat alignment |
| (25, 16, 14, 2) | x_l0l5[0] periodicity H16 L2 | Motor-auditory coupling periodicity 1s — sync benefit |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | E0: groove mean for regularization |
| [10] | spectral_flux | E1: onset detection for beat alignment |
| [11] | onset_strength | E1: event boundary detection |
| [21] | spectral_change | E0: tempo periodicity source |
| [22] | energy_change | E2: energy envelope for motor coupling |
| [25:33] | x_l0l5 | E2: motor-auditory coupling features |

---

## Scientific Foundation

- **Rathcke et al. 2024**: Regularization tendency scales inversely with BAT (ER>19, N=87, behavioral)
- **Grahn & Brett 2007**: Beat perception recruits SMA + basal ganglia, individual differences in motor system (fMRI, N=27)
- **Hoddinott & Grahn 2024**: 7T RSA reveals movement benefit for low-ability perceivers
- **Niarchou et al. 2022**: GWAS heritability h²=0.13-0.16 for beat synchronization (N=606k)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/barm/extraction.py`
