"""
Emotion control surface → R³ target deltas + operator configuration.

Maps 5 macro sliders (valence, arousal, tension, warmth, brightness)
+ 7 structural sliders (tempo_shift, rubato, swing, push_pull,
  rhythm_density, harmonic_mode_bias, harmonic_rhythm)
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

from dataclasses import dataclass


@dataclass
class EmotionControls:
    """
    5 macro emotion sliders + 7 structural sliders + global strength.

    Emotion sliders: -1.0 to +1.0
    Structural sliders: various ranges (see field comments)
    Strength: 0.0 (no effect) to 1.0 (full effect)
    """
    # ── v0.1: Timbral / affect sliders ──
    valence: float = 0.0      # Negative ↔ Positive emotional quality
    arousal: float = 0.0      # Low energy ↔ High energy / activation
    tension: float = 0.0      # Relaxed ↔ Tense / dissonant
    warmth: float = 0.0       # Cool ↔ Warm timbre
    brightness: float = 0.0   # Dark ↔ Bright timbre

    # ── v0.2: Structural sliders ──
    tempo_shift: float = 0.0          # -0.2 to +0.2 (relative BPM change)
    rubato: float = 0.0               # 0 to 1 (tempo variation amount)
    swing: float = 0.0                # -1 to +1 (off-beat shift; +1 = jazz swing)
    push_pull: float = 0.0            # -1 to +1 (ahead/behind beat micro-timing)
    rhythm_density: float = 0.0       # -1 to +1 (reduce ↔ increase event density)
    harmonic_mode_bias: float = 0.0   # -1 to +1 (minor ↔ major tilt)
    harmonic_rhythm: float = 0.0      # -1 to +1 (chord-change rate feel)

    # ── Global ──
    strength: float = 0.5     # Global effect intensity

    def __post_init__(self):
        for name in ("valence", "arousal", "tension", "warmth", "brightness",
                      "swing", "push_pull", "rhythm_density",
                      "harmonic_mode_bias", "harmonic_rhythm"):
            val = getattr(self, name)
            setattr(self, name, max(-1.0, min(1.0, float(val))))
        self.tempo_shift = max(-0.3, min(0.3, float(self.tempo_shift)))
        self.rubato = max(0.0, min(1.0, float(self.rubato)))
        self.strength = max(0.0, min(1.0, float(self.strength)))


# ── R³ target delta mapping ─────────────────────────────────────────────

R3_DELTA_MAP: dict[str, list[tuple[int, float]]] = {
    "valence": [
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
        (12, 0.12),   # warmth ↑
        (13, -0.08),  # sharpness ↓
        (15, -0.03),  # clarity ↓ (slightly)
        (122, -0.06), # sharpness_zwicker ↓
        (125, -0.04), # alpha_ratio ↓
    ],
    "brightness": [
        (12, -0.06),  # warmth ↓
        (13, 0.10),   # sharpness ↑
        (15, 0.08),   # clarity ↑
        (122, 0.08),  # sharpness_zwicker ↑
        (125, 0.04),  # alpha_ratio ↑
        (126, 0.04),  # hammarberg_index ↑
    ],
}


def controls_to_r3_delta(controls: EmotionControls) -> dict[int, float]:
    """Convert emotion controls to target R³ feature deltas."""
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
    """Configuration for all transform operators."""
    # ── v0.1: Timbral ──
    warmth_gain_db: float = 0.0
    brightness_gain_db: float = 0.0
    transient_mode: str = "none"
    transient_strength: float = 0.0
    harmonic_recipe: str = "none"
    harmonic_strength: float = 0.0

    # ── v0.2: Structural ──
    tempo_shift: float = 0.0
    rubato: float = 0.0
    swing: float = 0.0
    push_pull: float = 0.0
    rhythm_density: float = 0.0
    pitchclass_mode_bias: float = 0.0
    pitchclass_tension: float = 0.0

    # Global
    global_strength: float = 0.5


def controls_to_ops_config(controls: EmotionControls) -> OpsConfig:
    """
    Convert emotion controls to concrete operator parameters.
    Maps both timbral (v0.1) and structural (v0.2) controls.
    """
    cfg = OpsConfig(global_strength=controls.strength)
    s = controls.strength

    # ══════════════════════════════════════════════════════════════════
    # v0.1: TIMBRAL OPS
    # ══════════════════════════════════════════════════════════════════

    # Warmth / Brightness (spectral shelf)
    cfg.warmth_gain_db = controls.warmth * 4.0 * s
    cfg.brightness_gain_db = controls.brightness * 4.0 * s
    cfg.brightness_gain_db += controls.valence * 1.0 * s

    # Transient shaping
    if controls.arousal > 0.1:
        cfg.transient_mode = "intense"
        cfg.transient_strength = controls.arousal * s
    elif controls.arousal < -0.1:
        cfg.transient_mode = "calm"
        cfg.transient_strength = abs(controls.arousal) * s

    if controls.tension > 0.2:
        if cfg.transient_mode == "none":
            cfg.transient_mode = "intense"
        cfg.transient_strength += controls.tension * 0.3 * s

    # Harmonic density
    if controls.valence > 0.15:
        cfg.harmonic_recipe = "bright"
        cfg.harmonic_strength = controls.valence * s
    elif controls.valence < -0.15:
        cfg.harmonic_recipe = "dark"
        cfg.harmonic_strength = abs(controls.valence) * s

    if controls.tension > 0.3:
        cfg.harmonic_recipe = "tense"
        cfg.harmonic_strength = max(cfg.harmonic_strength, controls.tension * 0.7 * s)

    if controls.warmth > 0.3 and cfg.harmonic_recipe in ("none", "warm"):
        cfg.harmonic_recipe = "warm"
        cfg.harmonic_strength = max(cfg.harmonic_strength, controls.warmth * 0.5 * s)

    # ══════════════════════════════════════════════════════════════════
    # v0.2: STRUCTURAL OPS
    # ══════════════════════════════════════════════════════════════════

    # Direct structural sliders
    cfg.tempo_shift = controls.tempo_shift
    cfg.rubato = controls.rubato * s
    cfg.swing = controls.swing * s
    cfg.push_pull = controls.push_pull * s
    cfg.rhythm_density = controls.rhythm_density * s

    # Pitch-class reweighting
    cfg.pitchclass_mode_bias = controls.harmonic_mode_bias * s
    cfg.pitchclass_tension = 0.0

    # ── Cross-mapping: emotion sliders → structural params ──

    # Arousal → tempo shift (+), swing (+), rhythm density (+)
    if abs(controls.arousal) > 0.1:
        cfg.tempo_shift += controls.arousal * 0.03 * s    # subtle: max ±3% extra
        cfg.swing += controls.arousal * 0.15 * s          # slight swing with energy
        cfg.rhythm_density += controls.arousal * 0.3 * s  # density follows arousal

    # Tension → mode bias (minor), pitch-class tension, harmonic rhythm (+)
    if abs(controls.tension) > 0.1:
        cfg.pitchclass_mode_bias -= controls.tension * 0.3 * s  # tension → minor tilt
        cfg.pitchclass_tension += controls.tension * 0.5 * s    # direct tension pitch-class
        # Harmonic rhythm: tension = more chord changes
        # (applied as chroma novelty boost in transformer)

    # Valence → mode bias (major), reduce dissonant pitch-class gain
    if abs(controls.valence) > 0.1:
        cfg.pitchclass_mode_bias += controls.valence * 0.4 * s  # valence → major tilt
        cfg.pitchclass_tension -= controls.valence * 0.2 * s    # positive = less tense

    # Clamp structural params to safe ranges
    cfg.tempo_shift = max(-0.3, min(0.3, cfg.tempo_shift))
    cfg.rubato = max(0.0, min(1.0, cfg.rubato))
    cfg.swing = max(-1.0, min(1.0, cfg.swing))
    cfg.push_pull = max(-1.0, min(1.0, cfg.push_pull))
    cfg.rhythm_density = max(-1.0, min(1.0, cfg.rhythm_density))
    cfg.pitchclass_mode_bias = max(-1.0, min(1.0, cfg.pitchclass_mode_bias))
    cfg.pitchclass_tension = max(-1.0, min(1.0, cfg.pitchclass_tension))

    # Reduce harmonic doubles mix when pitch-class reweighting is active
    if abs(cfg.pitchclass_mode_bias) > 0.1 or abs(cfg.pitchclass_tension) > 0.1:
        cfg.harmonic_strength *= 0.5  # halve to avoid "chorus" on top of reweighting

    return cfg
