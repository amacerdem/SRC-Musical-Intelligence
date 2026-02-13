# C³ Mechanisms — Index

## Overview

Mechanisms are shared 30D sub-computations used by multiple models across cognitive units. Each mechanism is a `BaseMechanism` subclass that reads H3 temporal features and R3 spectral features and produces a fixed `(B, T, 30)` output tensor. The 30D output is split into 3x10D sub-sections, each corresponding to a distinct temporal horizon.

Mechanisms are computed once by the `MechanismRunner` and cached — if multiple models reference the same mechanism, it is shared rather than recomputed.

## Mechanism Catalogue

| NAME | Full Name | Circuit | Horizons | Models Using It |
|------|-----------|---------|----------|-----------------|
| AED | Affective Entrainment Dynamics | Mesolimbic | H6, H16 | SRP, AAC, VMM, PUPF, MAD, CLAM, TAR, DAP, CMAT, NEMAC, DAED, RPEM, MORMR, MCCN, MEAMR, LDAC, ICEM, WMED |
| CPD | Chills & Peak Detection | Mesolimbic | H9, H16, H18 | SRP, AAC, PUPF, MAD, DAED, RPEM |
| C0P | Cognitive Projection | Mesolimbic | H18, H19, H20 | SRP, VMM, MORMR, IUCP, ICEM, UDP |
| PPC | Pitch Processing Chain | Perceptual | H0, H3, H6 | BCH, PSCL, PCCR, SDNPS, ESME, SDED, SPH, HTP, PSH, PWUP, TPRD, SDD |
| TPC | Timbre Processing Chain | Perceptual | H6, H12, H16 | STAI, TSCP, MIAA, TPIO, IGFE, HTP, PSH |
| BEP | Beat Entrainment Processing | Sensorimotor | H6, H9, H11 | HMCE, AMSC, AMSS, MDNS, NEWMD, EDTA, ETAM, HGSIC, TMRM, OMS, MPFS, MTNE, PTGMP, PEOM, MSR, GSSM, NSCP, DDSMI, SPMC, STC, VRMSME, ASAP, CTBB, CMAPCC, RASN, IOTMS |
| TMH | Temporal Memory Hierarchy | Sensorimotor | H16, H18, H20, H22 | HMCE, AMSC, HGSIC, TMRM, MEAMN, PMIM, MCCN, CDMR |
| MEM | Memory Encoding / Retrieval | Mnemonic | H18, H20, H22, H25 | MEAMN, PNH, MMP, HCMC, OII, CDEM, CSSL, DMMS, RIRI, VRIAP, CMAPCC, RASN, PMIM, MSPBA (via SYN), NEMAC, WMED, MEAMR, SLEE, HTP, PSH |
| SYN | Syntactic Processing | Mnemonic | H12, H16, H18 | MSPBA |
| ASA | Auditory Scene Analysis | Salience | H3, H6, H9 | SNEM, IACM, CSG, SDl, STANM, BARM, AACM, PWSM, DGTP, AAC, MPG, CDMR, ONI, EDNR, DSP, SDD, SDDP, ECT, SLEE, SSPS, MAA |

## Circuit Grouping

### Mesolimbic (reward & pleasure)
- **AED** — Affective Entrainment Dynamics (H6, H16)
- **CPD** — Chills & Peak Detection (H9, H16, H18)
- **C0P** — Cognitive Projection (H18, H19, H20)

### Perceptual (hearing & pattern)
- **PPC** — Pitch Processing Chain (H0, H3, H6)
- **TPC** — Timbre Processing Chain (H6, H12, H16)

### Sensorimotor (rhythm & movement)
- **BEP** — Beat Entrainment Processing (H6, H9, H11)
- **TMH** — Temporal Memory Hierarchy (H16, H18, H20, H22)

### Mnemonic (memory & familiarity)
- **MEM** — Memory Encoding / Retrieval (H18, H20, H22, H25)
- **SYN** — Syntactic Processing (H12, H16, H18)

### Salience (attention & novelty)
- **ASA** — Auditory Scene Analysis (H3, H6, H9)

## Architecture

```
BaseMechanism (ABC)
    ├── NAME, FULL_NAME, OUTPUT_DIM=30, HORIZONS
    ├── h3_demand -> Set[(r3_idx, horizon, morph, law)]
    └── compute(h3_features, r3_features) -> (B, T, 30)

MechanismRunner
    ├── Scans ModelRegistry for MECHANISM_NAMES
    ├── Instantiates each needed mechanism once
    ├── run() computes all, caches outputs
    └── get(name) returns cached (B, T, 30) tensor
```

## Code Reference

- Base class: `mi_beta/contracts/base_mechanism.py`
- Implementations: `mi_beta/brain/mechanisms/{name}.py`
- Runner: `mi_beta/brain/mechanisms/__init__.py`
