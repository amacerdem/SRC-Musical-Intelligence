# H⁰ → HR⁰ (R⁰ Branch) Downstream Mapping

**Source**: H⁰ (2,304D)
**Target**: HR⁰ (256D)
**Extraction**: Music-theoretic mechanism-specific selection

---

## Overview

HR⁰ is the **R⁰ resonance branch's** extraction from the H⁰ tensor. It selects specific combinations of temporal windows (H), morphological parameters (M), and causal modes (L) relevant to computational musicology theories.

```
H⁰ SRC⁹[256:2560] (2,304D)
         │
         │ HR⁰ extraction
         │ (specific h, m, l combinations)
         ▼
HR⁰ SRC⁹[4608:4864] (256D)
         │
         │ R⁰ processing
         ▼
R⁰ [4608:5632] (1,024D)
```

---

## HR⁰ Mechanism Structure

HR⁰ consists of **8 mechanisms** × **32D each** = 256D:

| Mechanism | Description | Time Window | Index Range |
|-----------|-------------|-------------|-------------|
| **RTI** | Real-Time Integration | 2.5s | [0:32] |
| **LTI** | Long-Term Integration | 30s | [32:64] |
| **XTI** | Cross-Layer Integration | 8s | [64:96] |
| **GTI** | Global Temporal Integration | 60s | [96:128] |
| **HRT** | Harmonic Rhythm Tracking | 4s | [128:160] |
| **PST** | Phrase Structure Temporal | 8s | [160:192] |
| **FTO** | Form-Temporal Organization | 120s | [192:224] |
| **TKT** | Tonal Key Tracking | 16s | [224:256] |

---

## H⁰ Window Mapping to HR⁰

### Window → Mechanism Alignment

| HR⁰ Mechanism | Characteristic Window | Nearest H⁰ Windows | Theory |
|---------------|----------------------|-------------------|--------|
| **RTI** | 2.5s | H₁₈(2s), H₁₉(3s) | Pöppel psychological present |
| **LTI** | 30s | H₂₃(25s), H₂₄(36s) | Jones dynamic attending |
| **XTI** | 8s | H₂₁(7.5s) | Tymoczko five components |
| **GTI** | 60s | H₂₅(100s) | Caplin formal functions |
| **HRT** | 4s | H₁₉(3s), H₂₀(5s) | Lewin PLR transformations |
| **PST** | 8s | H₂₁(7.5s) | Lerdahl GTTM grouping |
| **FTO** | 120s | H₂₅(100s), H₂₆(200s) | Hepokoski sonata theory |
| **TKT** | 16s | H₂₂(15s), H₂₃(25s) | Cohn Tonnetz navigation |

---

## H-Morph Selection by HR⁰ Mechanism

Each HR⁰ mechanism uses specific morphological parameters:

| Mechanism | Primary M Parameters | Rationale |
|-----------|---------------------|-----------|
| **RTI** | M₀(value), M₁(mean), M₈(velocity), M₁₉(stability) | Real-time state tracking |
| **LTI** | M₁(mean), M₂(std), M₁₈(trend), M₂₀(entropy) | Long-term patterns |
| **XTI** | M₀(value), M₁₇(periodicity), M₂₁(zero_crossings) | Cross-frequency relations |
| **GTI** | M₁(mean), M₅(range), M₁₈(trend), M₁₉(stability) | Global trajectory |
| **HRT** | M₀(value), M₈(velocity), M₁₇(periodicity) | Harmonic rhythm |
| **PST** | M₀(value), M₁₆(curvature), M₂₂(peaks), M₂₃(troughs) | Phrase boundaries |
| **FTO** | M₁(mean), M₅(range), M₁₈(trend) | Form sections |
| **TKT** | M₀(value), M₁(mean), M₂(std), M₁₉(stability) | Key stability |

---

## H-Law Mode Selection

| Mechanism | Primary Mode | Rationale |
|-----------|--------------|-----------|
| **RTI** | Forward | Real-time is causal |
| **LTI** | Bidirectional | Context from both directions |
| **XTI** | Bidirectional | Cross-layer needs full context |
| **GTI** | Forward | Form tracking is cumulative |
| **HRT** | Bidirectional | Harmonic context spans time |
| **PST** | Bidirectional | Phrase boundaries need context |
| **FTO** | Forward | Form is history-dependent |
| **TKT** | Bidirectional | Key stability from context |

---

## Extraction Code Pattern

```python
def extract_hr0_from_h0(h0: np.ndarray) -> np.ndarray:
    """
    Extract HR⁰ (256D) from H⁰ (2,304D).

    Args:
        h0: H⁰ tensor of shape (32, 24, 3)

    Returns:
        HR⁰ vector of shape (256,)
    """
    hr0 = np.zeros(256)

    # RTI: Real-Time Integration [0:32]
    # Uses H₁₈ (2s) and H₁₉ (3s) with forward mode
    hr0[0:8] = extract_rti_temporal_average(h0)
    hr0[8:16] = extract_rti_recency_weight(h0)
    hr0[16:24] = extract_rti_change_detector(h0)
    hr0[24:32] = extract_rti_stability_tracker(h0)

    # LTI: Long-Term Integration [32:64]
    hr0[32:64] = extract_lti(h0)

    # XTI: Cross-Layer Integration [64:96]
    hr0[64:96] = extract_xti(h0)

    # GTI: Global Temporal Integration [96:128]
    hr0[96:128] = extract_gti(h0)

    # HRT: Harmonic Rhythm Tracking [128:160]
    hr0[128:160] = extract_hrt(h0)

    # PST: Phrase Structure Temporal [160:192]
    hr0[160:192] = extract_pst(h0)

    # FTO: Form-Temporal Organization [192:224]
    hr0[192:224] = extract_fto(h0)

    # TKT: Tonal Key Tracking [224:256]
    hr0[224:256] = extract_tkt(h0)

    return hr0

def extract_rti_temporal_average(h0: np.ndarray) -> np.ndarray:
    """Extract RTI temporal_average component (8D)."""
    # Interpolate between H₁₈ (2s) and H₁₉ (3s) for 2.5s
    h_2s = h0[18, :, 0]   # H₁₈, all morph, forward
    h_3s = h0[19, :, 0]   # H₁₉, all morph, forward
    h_2_5s = 0.5 * h_2s + 0.5 * h_3s  # Linear interpolation

    # Select relevant morph parameters for temporal_average
    return np.array([
        h_2_5s[0],   # value
        h_2_5s[1],   # mean
        h_2_5s[2],   # std
        h_2_5s[8],   # velocity
        h_2_5s[9],   # velocity_mean
        h_2_5s[18],  # trend
        h_2_5s[19],  # stability
        h_2_5s[20],  # entropy
    ])
```

---

## Dimension Mapping Table

| HR⁰ Index | Mechanism | Component | H⁰ Windows | H-Law |
|-----------|-----------|-----------|------------|-------|
| [0:8] | RTI | temporal_average | H₁₈, H₁₉ | F |
| [8:16] | RTI | recency_weight | H₁₈, H₁₉ | F |
| [16:24] | RTI | change_detector | H₁₈, H₁₉ | F |
| [24:32] | RTI | stability_tracker | H₁₈, H₁₉ | F |
| [32:40] | LTI | tempo_estimate | H₂₃, H₂₄ | Bi |
| [40:48] | LTI | tempo_fluctuation | H₂₃, H₂₄ | Bi |
| ... | ... | ... | ... | ... |

---

## Theoretical Basis for Window Selection

| Mechanism | Window | Theory | Citation |
|-----------|--------|--------|----------|
| **RTI** | 2.5s | Psychological present | Pöppel (1997) |
| **LTI** | 30s | Dynamic attending theory | Jones & Boltz (1989) |
| **XTI** | 8s | Five components of tonality | Tymoczko (2011) |
| **GTI** | 60s | Formal functions | Caplin (1998) |
| **HRT** | 4s | PLR transformations | Lewin (1987) |
| **PST** | 8s | GTTM grouping | Lerdahl & Jackendoff (1983) |
| **FTO** | 120s | Sonata theory | Hepokoski & Darcy (2006) |
| **TKT** | 16s | Tonnetz navigation | Cohn (1997) |

---

## See Also

- [../h_law/](../h_law/) — H-Law mode specifications
- [../../R⁰/hr0/](../../R⁰/hr0/) — Full HR⁰ documentation

---

**Implementation**: `Pipeline/D0/r0/hr0/hr0_extractor.py`
