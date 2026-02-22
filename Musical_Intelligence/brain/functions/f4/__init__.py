"""F4 — Memory Systems.

15 mechanism models (all IMU — Integrative Memory Unit), 163D total output.
13 beliefs: 4 Core + 7 Appraisal + 2 Anticipation.

Depth-ordered pipeline:
    Depth 0 (alpha):   MEAMN(12D,relay) | PNH(11D) | MMP(12D)
    Depth 1 (beta):    RASN(11D) | PMIM(11D) | OII(10D) | HCMC(11D) | RIRI(10D) | MSPBA(11D)
    Depth 2 (beta/γ):  VRIAP(10D) | TPRD(10D) | CMAPCC(10D) | DMMS(10D) | CSSL(10D) | CDEM(10D)

MEAMN relay wrapper already in kernel v4.0 (Phase 0a).
Mechanism models run in Phase 2 (after F1-F3).
"""
