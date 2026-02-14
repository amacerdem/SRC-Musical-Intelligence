"""
Emotion control surface → R³ target deltas + operator configuration.

Maps 5 macro sliders (valence, arousal, tension, warmth, brightness)
to concrete R³ feature targets and transform operator parameters.

R³ Feature Index Reference (128D):
  A: Consonance      [0:7]   roughness, sethares_dissonance, helmholtz_kang,
                              stumpf_fusion, sensory_pleasantness, inharmonicity,
                              harmonic_deviation
  B: Energy           [7:12]  amplitude, velocity_A, acceleration_A, loudness,
                              onset_strength
  C: Timbre          [12:21]  warmth, sharpness, tonalness, clarity,
                              spectral_smoothness, spectral_autocorrelation,
                              tristimulus1, tristimulus2, tristimulus3
  D: Change          [21:25]  spectral_flux, distribution_entropy,
                              distribution_flatness, distribution_concentration
  F: Pitch & Chroma  [49:65]  chroma_C..chroma_B, pitch_height,
                              pitch_class_entropy, pitch_salience, inharmonicity_index
  G: Rhythm & Groove [65:75]  tempo_estimate, beat_strength, pulse_clarity, ...
                              event_density, tempo_stability, rhythmic_regularity
  H: Harmony         [75:87]  key_clarity, tonnetz(6), voice_leading_distance,
                              harmonic_change, tonal_stability, diatonicity,
                              syntactic_irregularity
  I: Information     [87:94]  melodic_entropy, harmonic_entropy, ...,
                              spectral_surprise, information_rate
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmotionControls:
    """
    5 macro emotion sliders + global strength.

    All sliders range from -1.0 to +1.0.
    Strength ranges from 0.0 (no effect) to 1.0 (full effect).
    """
    valence: float = 0.0      # Negative ↔ Positive emotional quality
    arousal: float = 0.0      # Low energy ↔ High energy / activation
    tension: float = 0.0      # Relaxed ↔ Tense / dissonant
    warmth: float = 0.0       # Cool ↔ Warm timbre
    brightness: float = 0.0   # Dark ↔ Bright timbre
    strength: float = 0.5     # Global effect intensity

    def __post_init__(self):
        for name in ("valence", "arousal", "tension", "warmth", "brightness"):
            val = getattr(self, name)
            setattr(self, name, max(-1.0, min(1.0, float(val))))
        self.strength = max(0.0, min(1.0, float(self.strength)))


# ── R³ target delta mapping ─────────────────────────────────────────────
# Each entry: (r3_index, delta_per_unit_slider)
# delta_per_unit_slider = how much R³ feature should change when slider = +1.0
# Negative delta_per_unit_slider means the feature should DECREASE when slider increases.

R3_DELTA_MAP: dict[str, list[tuple[int, float]]] = {
    "valence": [
        # Positive valence → more consonant, more pleasant
        (0, -0.08),   # roughness ↓
        (1, -0.08),   # sethares_dissonance ↓
        (3,  0.06),   # stumpf_fusion ↑
        (4,  0.10),   # sensory_pleasantness ↑
        (12, 0.04),   # warmth ↑ (slightly)
        (14, 0.05),   # tonalness ↑
        (75, 0.06),   # key_clarity ↑
        (84, 0.06),   # tonal_stability ↑
        (85, 0.04),   # diatonicity ↑
    ],
    "arousal": [
        # High arousal → more energy, more transients, more flux
        (7,  0.08),   # amplitude ↑
        (8,  0.06),   # velocity_A ↑
        (10, 0.08),   # loudness ↑
        (11, 0.10),   # onset_strength ↑
        (21, 0.10),   # spectral_flux ↑
        (72, 0.06),   # event_density ↑
        (90, 0.04),   # spectral_surprise ↑
        (91, 0.04),   # information_rate ↑
    ],
    "tension": [
        # High tension → more dissonant, more entropy, less stable
        (0,  0.10),   # roughness ↑
        (1,  0.10),   # sethares_dissonance ↑
        (5,  0.06),   # inharmonicity ↑
        (6,  0.04),   # harmonic_deviation ↑
        (22, 0.06),   # distribution_entropy ↑
        (84, -0.06),  # tonal_stability ↓
        (86, 0.06),   # syntactic_irregularity ↑
        (87, 0.04),   # melodic_entropy ↑
        (88, 0.04),   # harmonic_entropy ↑
        (93, 0.04),   # tonal_ambiguity ↑
    ],
    "warmth": [
        # Warm → more low/mid energy, less sharp
        (12, 0.12),   # warmth ↑
        (13, -0.08),  # sharpness ↓
        (15, -0.03),  # clarity ↓ (slightly)
        (122, -0.06), # sharpness_zwicker ↓
        (125, -0.04), # alpha_ratio ↓ (less high-freq energy)
    ],
    "brightness": [
        # Bright → more high-freq energy, more clarity
        (12, -0.06),  # warmth ↓
        (13, 0.10),   # sharpness ↑
        (15, 0.08),   # clarity ↑
        (122, 0.08),  # sharpness_zwicker ↑
        (125, 0.04),  # alpha_ratio ↑
        (126, 0.04),  # hammarberg_index ↑
    ],
}


def controls_to_r3_delta(controls: EmotionControls) -> dict[int, float]:
    """
    Convert emotion controls to target R³ feature deltas.

    Returns:
        Dict mapping R³ feature index → target delta value.
        Positive = increase, negative = decrease.
    """
    deltas: dict[int, float] = {}
    strength = controls.strength

    for slider_name, mappings in R3_DELTA_MAP.items():
        slider_value = getattr(controls, slider_name)
        if abs(slider_value) < 0.01:
            continue

        for r3_idx, delta_per_unit in mappings:
            delta = slider_value * delta_per_unit * strength
            deltas[r3_idx] = deltas.get(r3_idx, 0.0) + delta

    return deltas


# ── Operator configuration ──────────────────────────────────────────────

@dataclass
class OpsConfig:
    """Configuration for transform operators, derived from emotion controls."""
    # Spectral (applied to harmonic STFT)
    warmth_gain_db: float = 0.0       # Low-shelf boost/cut
    brightness_gain_db: float = 0.0   # High-shelf boost/cut

    # Transient shaping (applied to percussive STFT)
    transient_mode: str = "none"      # 'intense', 'calm', or 'none'
    transient_strength: float = 0.0

    # Harmonic density (applied to harmonic waveform)
    harmonic_recipe: str = "none"     # Key from HARMONIC_RECIPES or 'none'
    harmonic_strength: float = 0.0

    # Global
    global_strength: float = 0.5


def controls_to_ops_config(controls: EmotionControls) -> OpsConfig:
    """
    Convert emotion controls to concrete operator parameters.
    This is where the "art" lives — mapping emotional intent to DSP operations.
    """
    cfg = OpsConfig(global_strength=controls.strength)

    # ── Warmth / Brightness (spectral shelf) ──
    # These directly map to frequency shelves on harmonic component
    cfg.warmth_gain_db = controls.warmth * 4.0 * controls.strength      # max ±4 dB
    cfg.brightness_gain_db = controls.brightness * 4.0 * controls.strength  # max ±4 dB

    # Also add cross-effects:
    # Positive valence → slightly brighter
    cfg.brightness_gain_db += controls.valence * 1.0 * controls.strength

    # ── Transient shaping ──
    # Arousal drives transient mode
    if controls.arousal > 0.1:
        cfg.transient_mode = "intense"
        cfg.transient_strength = controls.arousal * controls.strength
    elif controls.arousal < -0.1:
        cfg.transient_mode = "calm"
        cfg.transient_strength = abs(controls.arousal) * controls.strength

    # Tension also adds slight intensity
    if controls.tension > 0.2:
        if cfg.transient_mode == "none":
            cfg.transient_mode = "intense"
        cfg.transient_strength += controls.tension * 0.3 * controls.strength

    # ── Harmonic density ──
    # Valence drives harmonic recipe
    if controls.valence > 0.15:
        cfg.harmonic_recipe = "bright"
        cfg.harmonic_strength = controls.valence * controls.strength
    elif controls.valence < -0.15:
        cfg.harmonic_recipe = "dark"
        cfg.harmonic_strength = abs(controls.valence) * controls.strength

    # Tension overrides with tense intervals
    if controls.tension > 0.3:
        cfg.harmonic_recipe = "tense"
        cfg.harmonic_strength = max(cfg.harmonic_strength,
                                    controls.tension * 0.7 * controls.strength)

    # Warmth adds sub-octave
    if controls.warmth > 0.3 and cfg.harmonic_recipe in ("none", "warm"):
        cfg.harmonic_recipe = "warm"
        cfg.harmonic_strength = max(cfg.harmonic_strength,
                                    controls.warmth * 0.5 * controls.strength)

    return cfg
