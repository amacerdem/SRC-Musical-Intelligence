# L³ Groups — Delta (Validation Semantics)

**Version**: 2.1.0
**Symbol**: δ
**Level**: 4
**Dimensions**: 12 (fixed)
**Phase**: 1 (Independent, Stateless)
**Output Range**: [0, 1]
**Code**: `mi_beta/language/groups/delta.py` (112 lines)
**Updated**: 2026-02-13

---

## Overview

Delta answers the question: **HOW to test empirically?**

Delta maps Brain dimensions to measurable physiological, neural, and behavioral signals. Every delta dimension is a **testable prediction** — it represents what a specific laboratory measurement should show given the current Brain state. Delta is the primary bridge between MI's computational output and empirical validation.

**Audience**: Experimenters, physiologists, neuroscience validation teams.

---

## Design Principle

Every delta dimension corresponds to a real-world measurement with known effect sizes and established methodologies. The mapping is designed so that MI's output can be directly correlated against:

- Skin conductance response (SCR) waveforms
- Heart rate variability (HRV) traces
- Pupillometry recordings
- fMRI BOLD signals at specific MNI coordinates
- EEG spectral power in specified bands
- Behavioral auction/rating data

---

## 4 Subcategories

| Subcategory | Dim | Indices | Measurement Modality |
|-------------|:---:|:-------:|---------------------|
| Physiological | 4 | 0--3 | SCR, HR, pupil, piloerection |
| Neural | 3 | 4--6 | fMRI BOLD, EEG alpha |
| Behavioral | 2 | 7--8 | WTP auction, button-press rating |
| Temporal Constraints | 3 | 9--11 | Phase ordering, latency, refractory |

---

## Dimension Table

### Physiological (4D)

| Local Index | Name | Range | Formula | Citation | Effect Size |
|:-----------:|------|:-----:|---------|----------|:-----------:|
| 0 | `skin_conductance` | [0,1] | `scr` (passthrough) | de Fleurian & Pearce 2021 | d=0.85 |
| 1 | `heart_rate` | [0,1] | `hr` (passthrough) | Thayer et al. 2009 | -- |
| 2 | `pupil_diameter` | [0,1] | `arousal * |prediction_error|` | Laeng et al. 2012 | -- |
| 3 | `piloerection` | [0,1] | `chills_intensity` (passthrough) | Sloboda 1991 | -- |

### Neural (3D)

| Local Index | Name | Range | Formula | Citation | Effect Size |
|:-----------:|------|:-----:|---------|----------|:-----------:|
| 4 | `fmri_nacc_bold` | [0,1] | `da_nacc` (passthrough) | Salimpoor et al. 2011 | r=0.84 |
| 5 | `fmri_caudate_bold` | [0,1] | `da_caudate` (passthrough) | Salimpoor et al. 2011 | r=0.71 |
| 6 | `eeg_frontal_alpha` | [0,1] | `1 - pleasure` | Sammler et al. 2007 | -- |

### Behavioral (2D)

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 7 | `willingness_to_pay` | [0,1] | `pleasure` (proxy) | Salimpoor et al. 2013 |
| 8 | `button_press_rating` | [0,1] | `pleasure` (proxy) | Schubert 2004 |

### Temporal Constraints (3D)

| Local Index | Name | Range | Formula | Citation |
|:-----------:|------|:-----:|---------|----------|
| 9 | `wanting_leads_liking` | [0,1] | `sigmoid(da_caudate - da_nacc)` | Salimpoor et al. 2011 |
| 10 | `rpe_latency` | [0,1] | `|prediction_error|` | Fong et al. 2020 |
| 11 | `refractory_state` | [0,1] | `1 - chills_intensity` | Grewe et al. 2009 |

---

## Formulas

### Physiological (4D)

```python
# SCR: direct skin conductance response passthrough
skin_conductance = scr

# HR: direct heart rate passthrough
heart_rate = hr

# Pupil dilation: arousal-weighted prediction error magnitude
pupil_diameter = arousal * abs(prediction_error)

# Piloerection: chills intensity as goosebump probability
piloerection = chills_intensity
```

### Neural (3D)

```python
# fMRI NAcc BOLD: NAcc dopamine signal as BOLD proxy (r=0.84 with actual BOLD)
fmri_nacc_bold = da_nacc

# fMRI Caudate BOLD: Caudate dopamine signal (r=0.71 with actual BOLD)
fmri_caudate_bold = da_caudate

# EEG frontal alpha suppression: pleasure inversely predicts alpha power
eeg_frontal_alpha = 1.0 - pleasure
```

### Behavioral (2D)

```python
# Willingness-to-pay: Salimpoor 2013 auction paradigm proxy
willingness_to_pay = pleasure

# Continuous button-press rating: Schubert 2004 paradigm proxy
button_press_rating = pleasure
```

### Temporal Constraints (3D)

```python
# Wanting-leads-liking: sigmoid of Caudate-NAcc difference
# >0.5 = Caudate (wanting) leads; <0.5 = NAcc (liking) leads
wanting_leads_liking = sigmoid(da_caudate - da_nacc)

# RPE latency: magnitude of prediction error as timing proxy
rpe_latency = abs(prediction_error)

# Refractory state: inter-chill cooldown period
refractory_state = 1.0 - chills_intensity
```

---

## Code Mapping

| Doc Concept | Code Variable | Location |
|-------------|---------------|----------|
| SCR | `scr = _safe_get_dim(brain_output, "scr")` | delta.py:74 |
| HR | `hr = _safe_get_dim(brain_output, "hr")` | delta.py:75 |
| Arousal | `arousal = _safe_get_dim(brain_output, "arousal")` | delta.py:76 |
| Prediction error | `pred_error = _safe_get_dim(brain_output, "prediction_error", default=0.0)` | delta.py:77 |
| Pupil | `pupil = (arousal * pred_error.abs()).unsqueeze(-1)` | delta.py:78 |
| Piloerection | `piloerection = _safe_get_dim(brain_output, "chills_intensity")` | delta.py:79 |
| fMRI NAcc | `fmri_nacc = _safe_get_dim(brain_output, "da_nacc")` | delta.py:82 |
| fMRI Caudate | `fmri_caudate = _safe_get_dim(brain_output, "da_caudate")` | delta.py:83 |
| Pleasure | `pleasure = _safe_get_dim(brain_output, "pleasure")` | delta.py:84 |
| EEG alpha | `eeg_alpha = (1.0 - pleasure)` | delta.py:85 |
| WTP | `wtp = pleasure` | delta.py:88 |
| Wanting leads | `wanting_leads = torch.sigmoid(da_caudate - da_nacc)` | delta.py:94 |
| RPE latency | `rpe_latency = pred_error.abs()` | delta.py:95 |
| Refractory | `refractory = (1.0 - chills)` | delta.py:97 |
| OUTPUT_DIM | `OUTPUT_DIM = 12` (class constant) | delta.py:57 |

---

## Validation Paradigms

Each delta dimension maps to a specific experimental paradigm:

| Dimension | Paradigm | Expected Correlation |
|-----------|----------|---------------------|
| `skin_conductance` | SCR electrodes during music listening | r > 0.6 |
| `heart_rate` | ECG during music listening | Directional match |
| `pupil_diameter` | Eye-tracking during music listening | r > 0.4 |
| `piloerection` | Goosebump camera / self-report | Temporal alignment |
| `fmri_nacc_bold` | fMRI ROI at MNI NAcc coordinates | r = 0.84 (Salimpoor) |
| `fmri_caudate_bold` | fMRI ROI at MNI Caudate coordinates | r = 0.71 (Salimpoor) |
| `eeg_frontal_alpha` | EEG Fz/F3/F4 alpha power (8-12 Hz) | Inverse correlation with pleasure |
| `willingness_to_pay` | Auction paradigm (Salimpoor 2013) | r > 0.5 |
| `button_press_rating` | Continuous rating dial (Schubert 2004) | r > 0.5 |

---

## Design Notes

- **Fixed 12D**: Always outputs exactly 12 dimensions
- **Testable predictions**: Every dimension is designed to be correlated against laboratory data
- **Effect sizes documented**: Where available, expected effect sizes from literature are noted
- **Proxy mappings**: Some dimensions (WTP, button_press) use pleasure as a proxy
- **All outputs clamped**: Final tensor passes through `.clamp(0, 1)`

---

## Parent / See Also

- **Parent**: [Independent/00-INDEX.md](00-INDEX.md)
- **Epistemology**: [Epistemology/Validation.md](../../Epistemology/Validation.md) — Level 4 theory
- **Registry**: [Registry/DimensionCatalog.md](../../Registry/DimensionCatalog.md) — global indices
- **Validation**: [Validation/BenchmarkPlan.md](../../Validation/BenchmarkPlan.md) — delta vs physiology benchmark plan
- **Code**: `mi_beta/language/groups/delta.py`
