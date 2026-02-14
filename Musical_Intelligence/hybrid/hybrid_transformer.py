"""
HYBRID Transformer — main pipeline.

Transforms existing audio's emotional character through structural
manipulation (not just spectral filtering).

Pipeline:
  1. Load audio
  2. STFT → magnitude + phase (preserve phase!)
  3. HPSS → harmonic + percussive components
  4. Apply operators:
     a. Spectral: warmth/brightness shelf on harmonic magnitude
     b. Transient: onset-based shaping on percussive
     c. Harmonic density: pitch-shifted doubles on harmonic waveform
  5. Recombine components
  6. Safety: limiter + loudness normalize
  7. (Optional) R³ calibration: closed-loop strength adjustment
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from pathlib import Path

from Musical_Intelligence.hybrid.controls import (
    EmotionControls,
    OpsConfig,
    controls_to_ops_config,
    controls_to_r3_delta,
)
from Musical_Intelligence.hybrid.ops.stft_ops import (
    SR, N_FFT, HOP_LENGTH,
    load_audio, save_audio,
    stft_analyze, stft_synthesize,
    make_shelf_gain, soft_clip, loudness_normalize,
)
from Musical_Intelligence.hybrid.ops.hpss_ops import (
    hpss_stft, apply_spectral_transform_harmonic,
)
from Musical_Intelligence.hybrid.ops.transient_ops import (
    apply_transient_shaping_stft,
)
from Musical_Intelligence.hybrid.ops.harmonic_ops import (
    add_harmonic_doubles,
)


@dataclass
class TransformResult:
    """Result of a HYBRID transform."""
    audio: np.ndarray           # Transformed waveform
    sr: int                     # Sample rate
    controls: EmotionControls   # Applied controls
    ops_config: OpsConfig       # Derived operator config
    r3_deltas_target: dict      # Target R³ deltas
    calibration_result: object | None  # CalibrationResult if calibrated

    def save(self, path: str) -> None:
        """Save transformed audio to file."""
        save_audio(path, self.audio, self.sr)


class HybridTransformer:
    """
    Emotion-driven structural audio transformer.

    Usage:
        transformer = HybridTransformer()
        controls = EmotionControls(valence=0.5, arousal=0.3)
        result = transformer.transform("input.wav", controls)
        result.save("output.wav")
    """

    def __init__(self, sr: int = SR, calibrate: bool = True):
        self.sr = sr
        self.do_calibrate = calibrate

    def transform(
        self,
        input_path: str | Path,
        controls: EmotionControls,
        calibrate: bool | None = None,
    ) -> TransformResult:
        """
        Transform audio with emotion controls.

        Args:
            input_path: Path to input audio file
            controls:   Emotion control settings
            calibrate:  Override calibration (None = use default)

        Returns:
            TransformResult with transformed audio and diagnostics
        """
        do_cal = calibrate if calibrate is not None else self.do_calibrate

        # Load
        y_original = load_audio(str(input_path), sr=self.sr)
        ops_config = controls_to_ops_config(controls)
        r3_deltas = controls_to_r3_delta(controls)

        if do_cal and r3_deltas:
            # Calibrated mode: iterative strength adjustment
            from Musical_Intelligence.hybrid.calibration import calibrate as cal_fn

            def transform_fn(y: np.ndarray, strength: float) -> np.ndarray:
                scaled_controls = EmotionControls(
                    valence=controls.valence,
                    arousal=controls.arousal,
                    tension=controls.tension,
                    warmth=controls.warmth,
                    brightness=controls.brightness,
                    strength=strength,
                )
                return self._apply_transforms(y, scaled_controls)

            y_out, cal_result = cal_fn(
                y_original,
                target_deltas=r3_deltas,
                transform_fn=transform_fn,
                initial_strength=controls.strength,
                max_iterations=4,
                sr=self.sr,
            )
        else:
            y_out = self._apply_transforms(y_original, controls)
            cal_result = None

        # Final safety pass
        y_out = soft_clip(y_out)
        y_out = loudness_normalize(y_out, reference=y_original)

        return TransformResult(
            audio=y_out,
            sr=self.sr,
            controls=controls,
            ops_config=ops_config,
            r3_deltas_target=r3_deltas,
            calibration_result=cal_result,
        )

    def _apply_transforms(
        self,
        y: np.ndarray,
        controls: EmotionControls,
    ) -> np.ndarray:
        """
        Core transform pipeline (single pass, no calibration).

        Phase-preserving: all spectral modifications work on magnitude
        while keeping the original phase intact.
        """
        import librosa

        ops = controls_to_ops_config(controls)

        # ── Step 1: STFT (preserve phase) ──
        S = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)

        # ── Step 2: HPSS separation ──
        S_harm, S_perc = hpss_stft(S)

        # ── Step 3a: Spectral transforms on harmonic ──
        n_freq = S_harm.shape[0]

        # When both warmth and brightness are active, reduce cross-suppression
        # to avoid a mid-frequency scoop that kills sharpness/clarity
        both_active = abs(ops.warmth_gain_db) > 0.1 and abs(ops.brightness_gain_db) > 0.1
        cross_factor = 0.1 if both_active else 0.3

        if abs(ops.warmth_gain_db) > 0.1:
            # Warmth: low-shelf at ~800 Hz
            warmth_gain = make_shelf_gain(
                n_freq,
                cutoff_hz=800.0,
                low_gain=10 ** (ops.warmth_gain_db / 20.0),
                high_gain=10 ** (-ops.warmth_gain_db * cross_factor / 20.0),
                transition_hz=400.0,
            )
            S_harm = apply_spectral_transform_harmonic(
                S_harm, warmth_gain, strength=1.0
            )

        if abs(ops.brightness_gain_db) > 0.1:
            # Brightness: high-shelf at ~3000 Hz
            bright_gain = make_shelf_gain(
                n_freq,
                cutoff_hz=3000.0,
                low_gain=10 ** (-ops.brightness_gain_db * cross_factor / 20.0),
                high_gain=10 ** (ops.brightness_gain_db / 20.0),
                transition_hz=800.0,
            )
            S_harm = apply_spectral_transform_harmonic(
                S_harm, bright_gain, strength=1.0
            )

        # ── Step 3b: Transient shaping on percussive ──
        if ops.transient_mode != "none" and ops.transient_strength > 0.05:
            S_perc = apply_transient_shaping_stft(
                S_perc,
                mode=ops.transient_mode,
                strength=ops.transient_strength,
            )

        # ── Step 3c: Harmonic density augmentation ──
        S_enrichment = None
        if ops.harmonic_recipe != "none" and ops.harmonic_strength > 0.05:
            # Reconstruct harmonic waveform for pitch shifting
            y_harm = librosa.istft(S_harm, hop_length=HOP_LENGTH, length=len(y))

            # Add pitch-shifted doubles
            y_harm_enriched = add_harmonic_doubles(
                y_harm,
                recipe=ops.harmonic_recipe,
                strength=ops.harmonic_strength,
                sr=self.sr,
            )

            # Get the enrichment (new harmonics only) as STFT
            y_enrichment = y_harm_enriched - y_harm
            S_enrichment = librosa.stft(
                y_enrichment, n_fft=N_FFT, hop_length=HOP_LENGTH
            )

        # ── Step 4: Recombine ──
        S_out = S_harm + S_perc
        if S_enrichment is not None:
            # Match frame count
            n_frames = min(S_out.shape[1], S_enrichment.shape[1])
            S_out[:, :n_frames] += S_enrichment[:, :n_frames]

        # ── Step 5: Synthesize ──
        y_out = librosa.istft(S_out, hop_length=HOP_LENGTH, length=len(y))

        return y_out.astype(np.float32)

    def transform_batch(
        self,
        input_path: str | Path,
        presets: dict[str, EmotionControls],
        output_dir: str | Path,
        calibrate: bool | None = None,
    ) -> dict[str, TransformResult]:
        """
        Apply multiple emotion presets to the same audio.
        Useful for A/B comparison testing.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = {}
        for name, controls in presets.items():
            result = self.transform(input_path, controls, calibrate=calibrate)
            out_path = output_dir / f"{Path(input_path).stem}_{name}.wav"
            result.save(str(out_path))
            results[name] = result
            print(f"  [{name}] saved → {out_path}")

        return results


# ── Built-in presets ────────────────────────────────────────────────────

EMOTION_PRESETS: dict[str, EmotionControls] = {
    "joyful": EmotionControls(
        valence=0.7, arousal=0.4, tension=-0.2,
        warmth=0.2, brightness=0.3, strength=0.6,
    ),
    "melancholic": EmotionControls(
        valence=-0.5, arousal=-0.3, tension=0.1,
        warmth=0.3, brightness=-0.3, strength=0.6,
    ),
    "intense": EmotionControls(
        valence=0.0, arousal=0.8, tension=0.5,
        warmth=-0.1, brightness=0.2, strength=0.6,
    ),
    "calm": EmotionControls(
        valence=0.2, arousal=-0.7, tension=-0.4,
        warmth=0.4, brightness=-0.2, strength=0.6,
    ),
    "tense": EmotionControls(
        valence=-0.3, arousal=0.3, tension=0.8,
        warmth=-0.2, brightness=0.0, strength=0.6,
    ),
    "bright_warm": EmotionControls(
        valence=0.4, arousal=0.1, tension=-0.2,
        warmth=0.6, brightness=0.5, strength=0.5,
    ),
}
