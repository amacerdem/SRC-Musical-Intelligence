# H⁰ → HC⁰ (C⁰ Branch) Downstream Mapping

**Source**: H⁰ (2,304D)
**Target**: HC⁰ (512D)
**Extraction**: Mechanism-specific (h, m, l) selection

---

## Overview

HC⁰ is the **C⁰ cognitive branch's** extraction from the H⁰ tensor. It selects specific combinations of temporal windows (H), morphological parameters (M), and causal modes (L) relevant to neuroscientific mechanisms.

```
H⁰ SRC⁹[256:2560] (2,304D)
         │
         │ HC⁰ extraction
         │ (specific h, m, l combinations)
         ▼
HC⁰ SRC⁹[2560:3072] (512D)
         │
         │ C⁰ processing
         ▼
C⁰ [2560:4608] (2,048D)
```

---

## HC⁰ Mechanism Structure

HC⁰ consists of **16 mechanisms** organized in **4 functional layers**:

| Layer | Mechanisms | Dimension | Index Range |
|-------|------------|-----------|-------------|
| L1 Oscillatory | OSC, TGC, TIH, ATT | 128D | [0:128] |
| L2 Timing | NPL, PTM, ITM, GRV | 128D | [128:256] |
| L3 Memory | HRM, SGM, EFC, BND | 128D | [256:384] |
| L4 Affective | AED, ASA, CPD, C0P | 128D | [384:512] |

---

## H⁰ Window Selection by Mechanism

### Layer 1: Oscillatory

| Mechanism | H⁰ Windows | Primary Mode |
|-----------|------------|--------------|
| **OSC** | H₀(25ms), H₁(50ms), H₃(100ms), H₄(125ms), H₁₆(1000ms) | Bidirectional |
| **TGC** | H₄(125ms), H₇(250ms) | Bidirectional |
| **TIH** | H₁(50ms), H₈(300ms), H₁₇(1250ms), H₂₀(5000ms) | Forward |
| **ATT** | H₃(100ms) | Bidirectional |

### Layer 2: Timing

| Mechanism | H⁰ Windows | Primary Mode |
|-----------|------------|--------------|
| **NPL** | H₃(100ms) | Bidirectional |
| **PTM** | H₁₃(600ms) | Forward |
| **ITM** | H₁₆(1000ms) | Forward |
| **GRV** | H₁₁(500ms), H₁₅(800ms) | Bidirectional |

### Layer 3: Memory

| Mechanism | H⁰ Windows | Primary Mode |
|-----------|------------|--------------|
| **HRM** | H₁₄(730ms) | Forward + Backward |
| **SGM** | H₂₄(36s), H₂₈(414s), H₃₁(981s) | Forward |
| **EFC** | H₂(75ms) | Forward |
| **BND** | H₀(25ms), H₁(50ms), H₃(100ms) | Bidirectional |

### Layer 4: Affective

| Mechanism | H⁰ Windows | Primary Mode |
|-----------|------------|--------------|
| **AED** | H₆(200ms), H₁₆(1000ms) | Bidirectional |
| **ASA** | H₉(350ms) | Bidirectional |
| **CPD** | H₇(250ms), H₁₂(525ms), H₁₅(800ms) | Bidirectional |
| **C0P** | H₁₁(500ms) | Forward |

---

## H-Morph Selection by Mechanism

Each mechanism selects relevant morphological parameters:

| Mechanism | Primary M Parameters |
|-----------|---------------------|
| **OSC** | M₀(value), M₁(mean), M₂(std), M₁₇(periodicity) |
| **TGC** | M₀(value), M₁₆(curvature), M₁₇(periodicity) |
| **TIH** | M₀(value), M₁(mean), M₈(velocity), M₁₈(trend) |
| **ATT** | M₀(value), M₂(std), M₂₀(entropy) |
| **NPL** | M₀(value), M₁₇(periodicity), M₂₁(zero_crossings) |
| **PTM** | M₀(value), M₈(velocity), M₁₁(acceleration) |
| **ITM** | M₁(mean), M₂(std), M₁₉(stability) |
| **GRV** | M₀(value), M₁₇(periodicity), M₂₂(peaks) |
| **HRM** | M₀(value), M₁(mean), M₁₈(trend) |
| **SGM** | M₁(mean), M₅(range), M₁₈(trend) |
| **EFC** | M₀(value), M₈(velocity), M₁₅(smoothness) |
| **BND** | M₀(value), M₂(std), M₁₆(curvature) |
| **AED** | M₀(value), M₆(skew), M₈(velocity) |
| **ASA** | M₀(value), M₂(std), M₂₀(entropy) |
| **CPD** | M₀(value), M₄(max), M₈(velocity), M₁₈(trend) |
| **C0P** | M₁(mean), M₂(std), M₈(velocity) |

---

## Extraction Code Pattern

```python
def extract_hc0_from_h0(h0: np.ndarray) -> np.ndarray:
    """
    Extract HC⁰ (512D) from H⁰ (2,304D).

    Args:
        h0: H⁰ tensor of shape (32, 24, 3)

    Returns:
        HC⁰ vector of shape (512,)
    """
    hc0 = np.zeros(512)

    # Layer 1: Oscillatory [0:128]
    hc0[0:32] = extract_osc(h0)    # OSC: gamma, beta, alpha, theta, delta
    hc0[32:64] = extract_tgc(h0)   # TGC: coupling, phase, nesting
    hc0[64:96] = extract_tih(h0)   # TIH: micro, meso, macro, global
    hc0[96:128] = extract_att(h0)  # ATT: alpha suppression

    # Layer 2: Timing [128:256]
    hc0[128:160] = extract_npl(h0)  # NPL: phase-locking
    hc0[160:192] = extract_ptm(h0)  # PTM: beat anticipation
    hc0[192:224] = extract_itm(h0)  # ITM: interval timing
    hc0[224:256] = extract_grv(h0)  # GRV: groove/motor

    # Layer 3: Memory [256:384]
    hc0[256:288] = extract_hrm(h0)  # HRM: hippocampal replay
    hc0[288:320] = extract_sgm(h0)  # SGM: striatal gradient
    hc0[320:352] = extract_efc(h0)  # EFC: efference copy
    hc0[352:384] = extract_bnd(h0)  # BND: binding

    # Layer 4: Affective [384:512]
    hc0[384:416] = extract_aed(h0)  # AED: affective entrainment
    hc0[416:448] = extract_asa(h0)  # ASA: auditory stream
    hc0[448:480] = extract_cpd(h0)  # CPD: chills/peak
    hc0[480:512] = extract_c0p(h0)  # C0P: C⁰ projection

    return hc0

def extract_osc(h0: np.ndarray) -> np.ndarray:
    """Extract OSC mechanism from H⁰."""
    osc = np.zeros(32)

    # Gamma band from H₀ (25ms)
    osc[0:8] = h0[0, :8, 2]  # value, mean, std... with bidirectional mode

    # Beta band from H₁ (50ms)
    osc[8:16] = h0[1, :8, 2]

    # Alpha band from H₃ (100ms)
    osc[16:24] = h0[3, :8, 2]

    # Theta band from H₄ (125ms)
    osc[24:32] = h0[4, :8, 2]

    return osc
```

---

## Dimension Mapping Table

| HC⁰ Index | Mechanism | H⁰ Window | H-Morph | H-Law |
|-----------|-----------|-----------|---------|-------|
| [0:8] | OSC-γ | H₀ (25ms) | M₀-M₇ | Bi |
| [8:16] | OSC-β | H₁ (50ms) | M₀-M₇ | Bi |
| [16:24] | OSC-α | H₃ (100ms) | M₀-M₇ | Bi |
| [24:32] | OSC-θ | H₄ (125ms) | M₀-M₇ | Bi |
| ... | ... | ... | ... | ... |

---

## See Also

- [../h_law/forward/forward-mechanisms.md](../h_law/forward/forward-mechanisms.md)
- [../h_law/bidirectional/bidirectional-mechanisms.md](../h_law/bidirectional/bidirectional-mechanisms.md)
- [../../C⁰/HC⁰ Mechanisms/](../../C⁰/HC⁰ Mechanisms/) — Full HC⁰ documentation

---

**Implementation**: `Pipeline/D0/c0/hc0/hc0_extractor.py`
