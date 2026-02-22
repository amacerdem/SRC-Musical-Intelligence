# IACM P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [6:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:p3a_capture | [0, 1] | Attention-gated P3a. sigma(...+0.5*approx_entropy_val). Combines M-layer attention capture with approximate entropy to produce the real-time "inharmonic event captured attention" signal. Basinski 2025: P3a amplitude d=-1.37. |
| 7 | P1:spectral_encoding | [0, 1] | Oscillatory spectral encoding state. sigma(...+0.5*flatness_entropy). High-gamma oscillatory encoding of spectral content in STG. Foo 2016: ECoG STG gamma for spectral encoding. |

---

## Design Rationale

1. **P3a Capture (P0)**: The summary "present-moment" signal for involuntary attention capture. This is the primary IACM output that the kernel scheduler reads as the attention capture state. It feeds the Core belief `attention_capture` and reflects the P3a ERP component elicited by inharmonic spectral events.

2. **Spectral Encoding (P1)**: Oscillatory spectral encoding in superior temporal gyrus. This reflects the high-gamma activity observed in ECoG studies when the auditory cortex actively encodes spectral content. Higher values indicate stronger cortical engagement with the spectral structure of the current sound.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `p3a_capture` | P0 [6] | Core belief observation: attention_capture |
| `spectral_encoding` | P1 [7] | Spectral encoding state for precision engine |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (16, 3, 20, 2) | spectral_flatness entropy H3 L2 | Spectral entropy for encoding state (reused from E-layer) |
| (5, 3, 0, 2) | periodicity value H3 L2 | Periodicity at 100ms for capture gating |
| (5, 3, 2, 2) | periodicity std H3 L2 | Periodicity variability 100ms for scene complexity |

---

## Scientific Foundation

- **Basinski 2025**: P3a amplitude d=-1.37, involuntary attention to inharmonic events (EEG, N=35)
- **Foo 2016**: ECoG STG high-gamma oscillatory encoding of spectral content
- **Koelsch 1999**: P3a in musical context reflects involuntary attention switching
- **Alain 2007**: ORN as index of auditory scene segregation

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/iacm/cognitive_present.py`
