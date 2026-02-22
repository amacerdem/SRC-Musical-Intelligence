# SNEM M-Layer — Temporal Integration (3D)

**Layer**: Mathematical Model (M)
**Indices**: [3:6]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:ssep_enhancement | [0, 1] | Raw SS-EP enhancement level. alpha*BeatSalience + beta*MeterSalience - gamma*Envelope. Nozaradan 2012: SS-EP magnitude at beat frequency exceeds acoustic energy. |
| 4 | M1:enhancement_index | [0, 1] | Normalized enhancement ratio. (SS-EP_beat - SS-EP_envelope) / (SS-EP_envelope + epsilon). Quantifies how much neural response exceeds passive encoding. |
| 5 | M2:beat_salience | [0, 1] | Perceptual beat salience. Gaussian around optimal ~2 Hz. Nozaradan 2012: optimal range for enhancement. Aparicio-Terres: 1.65 Hz > 2.85 Hz confirmed. |

---

## Design Rationale

1. **SS-EP Enhancement (M0)**: The core computational model — combines beat salience (alpha=1.0) and meter salience (beta=0.8) then subtracts the acoustic envelope (gamma=0.5). This difference represents the brain's active construction beyond passive tracking.

2. **Enhancement Index (M1)**: A normalized ratio that quantifies the magnitude of selective enhancement. High values mean the brain is strongly boosting beat-related signals above what the acoustic input provides.

3. **Beat Salience (M2)**: A Gaussian tuning curve centered at ~2 Hz that captures the optimal tempo for human beat perception. This reflects the well-established finding that entrainment is strongest at walking tempo (~120 BPM).

---

## Mathematical Formulation

```
SS-EP_enhancement(f) = alpha*BeatSalience(f) + beta*MeterSalience(f) - gamma*Envelope(f)

Parameters:
  alpha = 1.0 (beat salience weight)
  beta  = 0.8 (meter salience weight)
  gamma = 0.5 (envelope subtraction weight)

BeatSalience(f) = exp(-(f - f_beat)^2 / (2*sigma_beat^2))
MeterSalience(f) = Sum_i w_i * exp(-(f - f_meter_i)^2 / (2*sigma_meter^2))

Enhancement_Index = (SS-EP_beat - SS-EP_envelope) / (SS-EP_envelope + epsilon)
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 0, 0, 2) | spectral_flux value H0 L2 | Instantaneous onset 25ms |
| (10, 1, 1, 2) | spectral_flux mean H1 L2 | Mean onset 50ms |
| (10, 3, 0, 2) | spectral_flux value H3 L2 | Onset at alpha band 100ms |
| (10, 4, 14, 2) | spectral_flux periodicity H4 L2 | Beat periodicity at 125ms |
| (7, 3, 0, 2) | amplitude value H3 L2 | Beat amplitude at 100ms |
| (7, 3, 2, 2) | amplitude std H3 L2 | Amplitude variability 100ms |

---

## Scientific Foundation

- **Nozaradan 2012**: SS-EP magnitude at beat > envelope power (N=9, p<0.0001)
- **Aparicio-Terres et al.**: 1.65 Hz > 2.85 Hz for entrainment strength
- **Bridwell 2017**: r=0.65 MMN correlation, 4 Hz guitar → 8 Hz alpha entrainment

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/snem/temporal_integration.py`
