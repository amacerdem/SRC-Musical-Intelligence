# Ultra Band Index

**Band**: Ultra
**Horizons**: H24-H31
**Duration**: 36,000ms - 981,000ms
**Frames**: 6,202-168,999
**Neural correlate**: Infra-slow oscillations (<0.1 Hz)
**Updated**: 2026-02-13

---

## Overview

The Ultra band covers the longest temporal horizons in the H3 system, spanning from 36 seconds to over 16 minutes. These horizons capture movement-level and piece-level musical structure. This is the sparsest band in the system -- only the MEM mechanism extends here (at H25), and only IMU actively consumes ultra-band horizons.

Ultra-band processing faces fundamental challenges: empirical research on temporal integration at these timescales is scarce, computational costs are substantial (H31 requires ~169K frames per buffer), and the reliability of statistical morphs degrades as window sizes grow far beyond the temporal structure of most musical events.

**Known limitation**: Long-form musical structure processing (multi-movement symphonies, opera acts, album-length works) remains an area of active research with limited empirical grounding.

---

## Quick Reference

| Horizon | Duration | Frames | Musical Scale | Mechanisms | Units |
|---------|----------|:------:|---------------|------------|-------|
| H24 | 36,000ms | 6,202 | ~36s (exposition) | -- | IMU |
| H25 | 60,000ms | 10,336 | 1 min | MEM | IMU |
| H26 | 120,000ms | 20,672 | 2 min | -- | IMU |
| H27 | 200,000ms | 34,453 | ~3.3 min | -- | IMU |
| H28 | 414,000ms | 71,319 | ~7 min | -- | IMU |
| H29 | 600,000ms | 103,359 | 10 min | -- | -- |
| H30 | 800,000ms | 137,812 | ~13 min | -- | -- |
| H31 | 981,000ms | 168,999 | ~16 min | -- | -- |

---

## Key Mechanisms

- **MEM** (Memory Encoding/Retrieval): H18, H20, H22, H25 -- only mechanism extending into ultra band
- **TMH** (Temporal Memory Hierarchy): H16, H18, H20, H22 -- terminates at macro/ultra boundary

Only MEM reaches into the ultra band, and only at a single horizon (H25 = 60s). This reflects the empirical reality: very little is known about how the brain integrates musical information over timescales beyond ~1 minute.

---

## Primary Unit Consumers

| Unit | Mechanisms Used | Horizon Range | Notes |
|------|----------------|:-------------:|-------|
| IMU | MEM | H25 | Only active consumer |
| -- | -- | H29-H31 | No current consumers |

The ultra band is the sparsest in the system. H29-H31 currently have no mechanism or unit assignments, serving as reserved capacity for future extensions.

---

## Morph Applicability

Only simple aggregates are meaningful at ultra timescales:

- **Meaningful**: M1 (mean), M18 (trend), M19 (stability)
- **Marginal**: M2 (std), M5 (range), M20 (entropy)
- **Not meaningful**: M8 (velocity), M9 (acceleration), M14 (periodicity), M16 (curvature), M22 (peaks)

At 36s+ windows, instantaneous dynamics (velocity, acceleration) and local structure (periodicity, curvature) are dominated by noise. Only broad statistical summaries and long-term trends provide signal.

---

## Sub-Documents

| File | Horizons | Description |
|------|----------|-------------|
| [H24-H28-Movement.md](H24-H28-Movement.md) | H24-H28 | Movement-level horizons |
| [H29-H31-Piece.md](H29-H31-Piece.md) | H29-H31 | Piece-level horizons |

## Cross-References

| Document | Location |
|----------|----------|
| Band overview | [../00-INDEX.md](../00-INDEX.md) |
| Section (H18-H23) | [../Macro/H18-H23-Section.md](../Macro/H18-H23-Section.md) |
| Horizon catalog | [../../Registry/HorizonCatalog.md](../../Registry/HorizonCatalog.md) |
| MEM mechanism | [../../../C³/Mechanisms/MEM.md](../../../C³/Mechanisms/MEM.md) |
