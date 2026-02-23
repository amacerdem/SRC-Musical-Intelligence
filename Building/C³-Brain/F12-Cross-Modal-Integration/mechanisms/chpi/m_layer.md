# CHPI — Temporal Integration

**Model**: Cross-Modal Harmonic Predictive Integration
**Unit**: PCU
**Function**: F12 Cross-Modal Integration
**Tier**: beta
**Layer**: M — Temporal Integration
**Dimensions**: 0D (not defined)

---

## Dimensions

CHPI does not define an M-layer. The model uses a 3-layer structure (E + P + F) with 11D total output:
- E-layer: 4D (extraction of cross-modal harmonic features)
- P-layer: 3D (cognitive present state)
- F-layer: 4D (future harmonic predictions)

The temporal integration that would typically occupy an M-layer is instead distributed across the H3 demands consumed by the E-layer (multi-scale windows from 25ms gamma through 1s beat timescale) and the P-layer (present-moment tonal context and convergence state). This design choice reflects that CHPI's cross-modal harmonic prediction operates primarily through feed-forward extraction and present-state monitoring rather than through dedicated mathematical transformation of temporal dynamics.

---

## H3 Demands

No H3 demands are assigned to this layer. All 20 H3 tuples are consumed by the E-layer (14 tuples) and P-layer (6 tuples).

---

## Computation

No computation is performed at this layer.

---

## Dependencies

No dependencies at this layer.
