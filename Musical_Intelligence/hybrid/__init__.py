"""
Musical Intelligence — HYBRID Module
=====================================
Emotion-driven structural audio transformation.

Transform existing audio's emotional character at a structural level
(harmony, transients, harmonic density) — not just spectral filtering.

Usage:
    from Musical_Intelligence.hybrid import HybridTransformer, EmotionControls

    transformer = HybridTransformer()
    controls = EmotionControls(valence=0.5, arousal=0.3)
    result = transformer.transform("input.wav", controls)
    result.save("output.wav")
"""

__all__ = ["HybridTransformer", "EmotionControls"]


def __getattr__(name: str):
    """Lazy imports — prevents crash during incremental development."""
    if name == "EmotionControls":
        from Musical_Intelligence.hybrid.controls import EmotionControls
        return EmotionControls
    if name == "HybridTransformer":
        from Musical_Intelligence.hybrid.hybrid_transformer import HybridTransformer
        return HybridTransformer
    raise AttributeError(f"module 'Musical_Intelligence.hybrid' has no attribute {name}")
