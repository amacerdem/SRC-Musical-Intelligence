"""
HYBRID Transformer v0.2 — main pipeline.

Transforms existing audio's emotional character through both
timbral AND structural manipulation.

Pipeline:
  1. Load audio
  2. STFT / HPSS split (phase-preserving foundation)
  3. STRUCTURE EXTRACT: beat grid + onset env + chroma + novelty
  4. TIMING WARPS: tempo shift (phase vocoder on STFT), then micro-timing
  5. RHYTHM DENSITY: transient-aware density control on percussive
  6. HARMONIC FUNCTION: pitch-class reweighting on harmonic
  7. TIMBRAL: warmth/brightness shelf, transient shaping (v0.1)
  8. HARMONIC DOUBLES: pitch-shifted overtone enrichment (v0.1)
  9. Recombine + safety (gain clamp, limiter, loudness match)
  10. Optional closed-loop R³ calibration
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
from Musical_Intelligence.hybrid.ops.structure_ops import (
    extract_score_proxy, ScoreProxy,
)
from Musical_Intelligence.hybrid.ops.timing_ops import (
    apply_tempo_shift_stft, apply_rubato, apply_microtiming,
    apply_rhythm_density,
)
from Musical_Intelligence.hybrid.ops.pitchclass_ops import (
    apply_pitchclass_reweighting,
)


@dataclass
class TransformResult:
    """Result of a HYBRID transform."""
    audio: np.ndarray
    sr: int
    controls: EmotionControls
    ops_config: OpsConfig
    r3_deltas_target: dict
    score_proxy: ScoreProxy | None
    calibration_result: object | None

    def save(self, path: str) -> None:
        save_audio(path, self.audio, self.sr)


class HybridTransformer:
    """
    Emotion-driven structural audio transformer (v0.2).

    Usage:
        transformer = HybridTransformer()
        controls = EmotionControls(valence=0.5, arousal=0.3, swing=0.6)
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
        """Transform audio with emotion + structural controls."""
        do_cal = calibrate if calibrate is not None else self.do_calibrate

        y_original = load_audio(str(input_path), sr=self.sr)
        ops_config = controls_to_ops_config(controls)
        r3_deltas = controls_to_r3_delta(controls)

        if do_cal and r3_deltas:
            from Musical_Intelligence.hybrid.calibration import calibrate as cal_fn

            def transform_fn(y: np.ndarray, strength: float) -> np.ndarray:
                scaled = EmotionControls(
                    valence=controls.valence, arousal=controls.arousal,
                    tension=controls.tension, warmth=controls.warmth,
                    brightness=controls.brightness,
                    tempo_shift=controls.tempo_shift, rubato=controls.rubato,
                    swing=controls.swing, push_pull=controls.push_pull,
                    rhythm_density=controls.rhythm_density,
                    harmonic_mode_bias=controls.harmonic_mode_bias,
                    harmonic_rhythm=controls.harmonic_rhythm,
                    strength=strength,
                )
                return self._apply_transforms(y, scaled)[0]

            y_out, cal_result = cal_fn(
                y_original, target_deltas=r3_deltas,
                transform_fn=transform_fn,
                initial_strength=controls.strength,
                max_iterations=4, sr=self.sr,
            )
            score = None
        else:
            y_out, score = self._apply_transforms(y_original, controls)
            cal_result = None

        # Final safety
        y_out = soft_clip(y_out)
        y_out = loudness_normalize(y_out, reference=y_original)

        return TransformResult(
            audio=y_out, sr=self.sr, controls=controls,
            ops_config=ops_config, r3_deltas_target=r3_deltas,
            score_proxy=score, calibration_result=cal_result,
        )

    def _apply_transforms(
        self,
        y: np.ndarray,
        controls: EmotionControls,
    ) -> tuple[np.ndarray, ScoreProxy | None]:
        """
        Core transform pipeline (single pass, no calibration).
        Returns (y_transformed, score_proxy).
        """
        import librosa

        ops = controls_to_ops_config(controls)
        has_structure = (
            abs(ops.tempo_shift) > 0.005
            or ops.rubato > 0.01
            or abs(ops.swing) > 0.01
            or abs(ops.push_pull) > 0.01
            or abs(ops.rhythm_density) > 0.05
            or abs(ops.pitchclass_mode_bias) > 0.01
            or abs(ops.pitchclass_tension) > 0.01
        )

        # ── Step 1: STFT (preserve phase) ──
        S = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)

        # ── Step 2: HPSS separation ──
        S_harm, S_perc = hpss_stft(S)

        # ── Step 3: Score proxy extraction ──
        score = None
        if has_structure:
            y_perc_temp = librosa.istft(S_perc, hop_length=HOP_LENGTH, length=len(y))
            score = extract_score_proxy(y, self.sr, y_percussive=y_perc_temp)

        # ── Step 4: TIMING WARPS ──

        # 4a: Global tempo shift (phase vocoder on STFT — preserves pitch)
        if abs(ops.tempo_shift) > 0.005:
            S_harm = apply_tempo_shift_stft(S_harm, ops.tempo_shift, HOP_LENGTH)
            S_perc = apply_tempo_shift_stft(S_perc, ops.tempo_shift, HOP_LENGTH)

        # ── Step 5: PITCH-CLASS REWEIGHTING on harmonic ──
        if score and (abs(ops.pitchclass_mode_bias) > 0.01
                      or abs(ops.pitchclass_tension) > 0.01):
            S_harm = apply_pitchclass_reweighting(
                S_harm,
                key_idx=score.key_idx,
                mode_bias=ops.pitchclass_mode_bias,
                tension=ops.pitchclass_tension,
                strength=1.0,
                n_fft=N_FFT,
                sr=self.sr,
            )

        # ── Step 6: RHYTHM DENSITY on percussive ──
        if abs(ops.rhythm_density) > 0.05:
            S_perc = apply_rhythm_density(
                S_perc,
                density=ops.rhythm_density,
                hop_length=HOP_LENGTH,
                sr=self.sr,
            )

        # ── Step 7: TIMBRAL OPS (v0.1) ──

        n_freq = S_harm.shape[0]
        both_active = abs(ops.warmth_gain_db) > 0.1 and abs(ops.brightness_gain_db) > 0.1
        cross_factor = 0.1 if both_active else 0.3

        if abs(ops.warmth_gain_db) > 0.1:
            warmth_gain = make_shelf_gain(
                n_freq, cutoff_hz=800.0,
                low_gain=10 ** (ops.warmth_gain_db / 20.0),
                high_gain=10 ** (-ops.warmth_gain_db * cross_factor / 20.0),
                transition_hz=400.0,
            )
            S_harm = apply_spectral_transform_harmonic(S_harm, warmth_gain, strength=1.0)

        if abs(ops.brightness_gain_db) > 0.1:
            bright_gain = make_shelf_gain(
                n_freq, cutoff_hz=3000.0,
                low_gain=10 ** (-ops.brightness_gain_db * cross_factor / 20.0),
                high_gain=10 ** (ops.brightness_gain_db / 20.0),
                transition_hz=800.0,
            )
            S_harm = apply_spectral_transform_harmonic(S_harm, bright_gain, strength=1.0)

        # Transient shaping on percussive
        if ops.transient_mode != "none" and ops.transient_strength > 0.05:
            S_perc = apply_transient_shaping_stft(
                S_perc, mode=ops.transient_mode, strength=ops.transient_strength,
            )

        # ── Step 8: iSTFT both components ──
        # Estimate output length based on tempo shift
        if abs(ops.tempo_shift) > 0.005:
            rate = 1.0 + np.clip(ops.tempo_shift, -0.3, 0.3)
            target_len = int(len(y) / rate)
        else:
            target_len = len(y)

        y_harm = librosa.istft(S_harm, hop_length=HOP_LENGTH, length=target_len)
        y_perc = librosa.istft(S_perc, hop_length=HOP_LENGTH, length=target_len)

        # ── Step 8b: MICRO-TIMING warps (waveform domain) ──
        if score and (abs(ops.swing) > 0.01 or abs(ops.push_pull) > 0.01):
            # Adjust beat times for tempo change
            beat_times = score.beat_times.copy()
            if abs(ops.tempo_shift) > 0.005:
                rate = 1.0 + np.clip(ops.tempo_shift, -0.3, 0.3)
                beat_times = beat_times / rate

            # Filter beat times to output duration
            max_t = target_len / self.sr
            beat_times = beat_times[beat_times < max_t]

            if len(beat_times) >= 2:
                y_harm = apply_microtiming(
                    y_harm, self.sr, beat_times, ops.swing, ops.push_pull,
                )
                y_perc = apply_microtiming(
                    y_perc, self.sr, beat_times, ops.swing, ops.push_pull,
                )

        # Rubato (waveform domain)
        if score and ops.rubato > 0.01:
            beat_times = score.beat_times.copy()
            if abs(ops.tempo_shift) > 0.005:
                rate = 1.0 + np.clip(ops.tempo_shift, -0.3, 0.3)
                beat_times = beat_times / rate
            max_t = target_len / self.sr
            beat_times = beat_times[beat_times < max_t]
            if len(beat_times) >= 2:
                y_harm = apply_rubato(y_harm, self.sr, beat_times, ops.rubato)
                y_perc = apply_rubato(y_perc, self.sr, beat_times, ops.rubato)

        # ── Step 9: HARMONIC DOUBLES (v0.1, waveform domain) ──
        S_enrichment = None
        if ops.harmonic_recipe != "none" and ops.harmonic_strength > 0.05:
            y_harm_enriched = add_harmonic_doubles(
                y_harm, recipe=ops.harmonic_recipe,
                strength=ops.harmonic_strength, sr=self.sr,
            )
            y_enrichment = y_harm_enriched - y_harm
            S_enrichment = librosa.stft(y_enrichment, n_fft=N_FFT, hop_length=HOP_LENGTH)

        # ── Step 10: Recombine ──
        y_out = y_harm + y_perc
        if S_enrichment is not None:
            y_enrich = librosa.istft(
                S_enrichment, hop_length=HOP_LENGTH, length=len(y_out),
            )
            y_out = y_out + y_enrich

        return y_out.astype(np.float32), score

    def transform_batch(
        self,
        input_path: str | Path,
        presets: dict[str, EmotionControls],
        output_dir: str | Path,
        calibrate: bool | None = None,
    ) -> dict[str, TransformResult]:
        """Apply multiple presets to the same audio."""
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
    # v0.1 timbral presets
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
    # v0.2 structural presets
    "rubato_minor": EmotionControls(
        valence=-0.3, tension=0.3, warmth=0.2,
        rubato=0.7, harmonic_mode_bias=-0.6, strength=0.6,
    ),
    "swing_bright": EmotionControls(
        valence=0.3, arousal=0.3, brightness=0.3,
        swing=0.7, strength=0.6,
    ),
    "driving": EmotionControls(
        arousal=0.6, tension=0.2,
        tempo_shift=0.08, rhythm_density=0.5, push_pull=0.3, strength=0.6,
    ),
    "spacious": EmotionControls(
        valence=0.1, arousal=-0.5, tension=-0.3,
        warmth=0.3, rubato=0.5,
        rhythm_density=-0.5, harmonic_mode_bias=0.3, strength=0.6,
    ),
}
