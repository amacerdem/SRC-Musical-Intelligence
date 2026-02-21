"""C³ Brain — 96 cognitive nuclei organized into 12 cognitive functions (F1-F12).

The brain module transforms R³ spectral features and H³ temporal demands
into a ``BrainOutput`` containing four channels:
    tensor  (B, T, N_ext)   — cognitive processing output
    ram     (B, T, 26)      — Region Activation Map
    neuro   (B, T, 4)       — neurochemical state [DA, NE, OPI, 5HT]
    psi     (B, T, N_psi)   — Ψ³ cognitive interpretation
"""
