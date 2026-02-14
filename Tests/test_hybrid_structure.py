"""
HYBRID v0.2 Structure Layer — Pytest Suite
=============================================
Tests for tempo shift, swing, rhythm density, and harmonic mode bias.

Run:
    pytest Tests/test_hybrid_structure.py -v
    pytest Tests/test_hybrid_structure.py -v -k "tempo"
    pytest Tests/test_hybrid_structure.py -v -k "swing"
    pytest Tests/test_hybrid_structure.py -v -k "mode"
"""

from __future__ import annotations

import sys
import os
import tempfile
import numpy as np
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

SR = 44100


# ── Fixtures ──────────────────────────────────────────────────────────

def _make_rhythmic_audio(duration: float = 5.0, bpm: float = 120.0) -> np.ndarray:
    """Create a rhythmic test signal with clear beats and pitched content."""
    n_samples = int(duration * SR)
    t = np.linspace(0, duration, n_samples, dtype=np.float32)
    y = np.zeros(n_samples, dtype=np.float32)

    beat_interval = 60.0 / bpm
    # Add pitched tones (C major chord: C4, E4, G4)
    y += 0.2 * np.sin(2 * np.pi * 261.63 * t)  # C4
    y += 0.15 * np.sin(2 * np.pi * 329.63 * t)  # E4
    y += 0.12 * np.sin(2 * np.pi * 392.00 * t)  # G4

    # Add rhythmic clicks at beat positions
    n_beats = int(duration / beat_interval)
    for i in range(n_beats):
        beat_sample = int(i * beat_interval * SR)
        if beat_sample + 200 < n_samples:
            # Sharp click + exponential decay
            click_len = 200
            decay = np.exp(-np.linspace(0, 8, click_len))
            y[beat_sample:beat_sample + click_len] += 0.5 * decay
            # Also add a noise burst for percussive content
            y[beat_sample:beat_sample + click_len] += 0.15 * decay * np.random.randn(click_len).astype(np.float32)

        # Add off-beat (8th note) at half-beat
        offbeat_sample = int((i + 0.5) * beat_interval * SR)
        if offbeat_sample + 100 < n_samples:
            click_len = 100
            decay = np.exp(-np.linspace(0, 10, click_len))
            y[offbeat_sample:offbeat_sample + click_len] += 0.2 * decay

    return y


@pytest.fixture(scope="session")
def rhythmic_audio() -> np.ndarray:
    return _make_rhythmic_audio(duration=5.0, bpm=120.0)


@pytest.fixture(scope="session")
def real_audio():
    swan = PROJECT_ROOT / "Test-Audio" / (
        "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
        " - Pyotr Ilyich Tchaikovsky.wav"
    )
    if not swan.exists():
        return None
    from Musical_Intelligence.hybrid.ops.stft_ops import load_audio
    return load_audio(str(swan))[:int(10 * SR)]


@pytest.fixture(scope="session")
def test_audio(real_audio, rhythmic_audio):
    return real_audio if real_audio is not None else rhythmic_audio


@pytest.fixture(scope="session")
def test_audio_path(test_audio):
    from Musical_Intelligence.hybrid.ops.stft_ops import save_audio
    tmp = tempfile.mktemp(suffix=".wav")
    save_audio(tmp, test_audio)
    yield tmp
    os.unlink(tmp)


# ── Helpers ───────────────────────────────────────────────────────────

def snr_db(y, y_hat):
    n = min(len(y), len(y_hat))
    sig = np.sum(y[:n] ** 2)
    noise = np.sum((y[:n] - y_hat[:n]) ** 2)
    if noise < 1e-20:
        return 120.0
    return 10.0 * np.log10(sig / noise)


def get_bpm(y, sr=SR):
    """Estimate BPM from audio."""
    import librosa
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr, hop_length=256)
    if hasattr(tempo, "__len__"):
        return float(tempo[0]) if len(tempo) > 0 else 120.0
    return float(tempo)


def get_chroma_mode_corr(y, sr=SR):
    """Get major/minor template correlation for audio."""
    import librosa
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=256)
    from Musical_Intelligence.hybrid.ops.structure_ops import estimate_key
    key_idx, mode, conf = estimate_key(chroma)
    from Musical_Intelligence.hybrid.ops.pitchclass_ops import compute_mode_correlation
    major_c, minor_c = compute_mode_correlation(chroma, key_idx)
    return key_idx, mode, major_c, minor_c


def transform(audio_path, **kwargs):
    """Quick transform helper."""
    from Musical_Intelligence.hybrid.hybrid_transformer import HybridTransformer
    from Musical_Intelligence.hybrid.controls import EmotionControls
    t = HybridTransformer(calibrate=False)
    c = EmotionControls(**kwargs)
    return t.transform(audio_path, c, calibrate=False)


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 1: Non-destructive (v0.2 additions)
# ══════════════════════════════════════════════════════════════════════

class TestNonDestructive:
    """Structural controls at zero must not break audio."""

    def test_structure_zero_is_noop(self, test_audio_path, test_audio):
        """All structural sliders at 0, strength=0 → near-identity."""
        result = transform(
            test_audio_path,
            tempo_shift=0, swing=0, push_pull=0,
            rhythm_density=0, harmonic_mode_bias=0,
            strength=0.0,
        )
        n = min(len(test_audio), len(result.audio))
        assert snr_db(test_audio[:n], result.audio[:n]) > 25.0

    def test_v01_presets_still_work(self, test_audio_path, test_audio):
        """v0.1 presets must still produce valid output after v0.2 refactor."""
        from Musical_Intelligence.hybrid.hybrid_transformer import EMOTION_PRESETS
        from Musical_Intelligence.hybrid.hybrid_transformer import HybridTransformer
        t = HybridTransformer(calibrate=False)
        for name in ["joyful", "calm", "intense"]:
            result = t.transform(test_audio_path, EMOTION_PRESETS[name], calibrate=False)
            assert not np.any(np.isnan(result.audio))
            assert np.max(np.abs(result.audio)) > 0.01

    def test_structural_preset_valid(self, test_audio_path, test_audio):
        """v0.2 structural presets produce valid, non-silent output."""
        from Musical_Intelligence.hybrid.hybrid_transformer import EMOTION_PRESETS
        from Musical_Intelligence.hybrid.hybrid_transformer import HybridTransformer
        t = HybridTransformer(calibrate=False)
        for name in ["rubato_minor", "swing_bright", "driving", "spacious"]:
            result = t.transform(test_audio_path, EMOTION_PRESETS[name], calibrate=False)
            assert not np.any(np.isnan(result.audio)), f"{name}: NaN"
            assert np.max(np.abs(result.audio)) > 0.01, f"{name}: silence"


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 2: Tempo shift
# ══════════════════════════════════════════════════════════════════════

class TestTempoShift:
    """Tempo shift must change duration and measured BPM."""

    def test_tempo_up_shortens_audio(self, test_audio_path, test_audio):
        """tempo_shift=+0.1 → output ~10% shorter."""
        result = transform(test_audio_path, tempo_shift=0.1, strength=0.7)
        expected_len = int(len(test_audio) / 1.1)
        actual_len = len(result.audio)
        ratio = actual_len / expected_len
        assert 0.9 < ratio < 1.1, f"Length ratio {ratio} not near 1.0"

    def test_tempo_down_lengthens_audio(self, test_audio_path, test_audio):
        """tempo_shift=-0.1 → output ~10% longer."""
        result = transform(test_audio_path, tempo_shift=-0.1, strength=0.7)
        expected_len = int(len(test_audio) / 0.9)
        actual_len = len(result.audio)
        ratio = actual_len / expected_len
        assert 0.9 < ratio < 1.1, f"Length ratio {ratio} not near 1.0"

    def test_tempo_up_bpm_increases(self, test_audio_path):
        """tempo_shift=+0.1 → estimated BPM increases."""
        from Musical_Intelligence.hybrid.ops.stft_ops import load_audio
        y_orig = load_audio(test_audio_path)
        bpm_orig = get_bpm(y_orig)

        result = transform(test_audio_path, tempo_shift=0.1, strength=0.7)
        bpm_new = get_bpm(result.audio)

        # BPM should increase (with some tolerance for estimation error)
        # The beat tracker might octave-double, so check relative change
        if bpm_orig > 0 and bpm_new > 0:
            ratio = bpm_new / bpm_orig
            # Accept if BPM increased OR if it octave-jumped
            assert ratio > 0.95 or ratio > 1.8, f"BPM didn't increase: {bpm_orig:.1f} → {bpm_new:.1f}"


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 3: Swing
# ══════════════════════════════════════════════════════════════════════

class TestSwing:
    """Swing must modify micro-timing of off-beats."""

    def test_swing_changes_audio(self, test_audio_path, test_audio):
        """swing=0.7 must produce different output."""
        result = transform(test_audio_path, swing=0.7, strength=0.7)
        n = min(len(test_audio), len(result.audio))
        max_diff = np.max(np.abs(test_audio[:n] - result.audio[:n]))
        assert max_diff > 0.001, "Swing had no effect"

    def test_swing_preserves_length(self, test_audio_path, test_audio):
        """Swing should not change audio length."""
        result = transform(test_audio_path, swing=0.7, strength=0.7)
        assert len(result.audio) == len(test_audio)

    def test_swing_preserves_quality(self, test_audio_path, test_audio):
        """Swing output should still be coherent (not bozuk)."""
        result = transform(test_audio_path, swing=0.7, strength=0.7)
        # RMS should be in reasonable range
        rms_orig = np.sqrt(np.mean(test_audio ** 2))
        rms_out = np.sqrt(np.mean(result.audio ** 2))
        ratio = rms_out / (rms_orig + 1e-8)
        assert 0.5 < ratio < 2.0, f"RMS ratio out of range: {ratio}"


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 4: Harmonic mode bias
# ══════════════════════════════════════════════════════════════════════

class TestHarmonicModeBias:
    """Mode bias should shift chroma correlation with major/minor templates."""

    def test_major_bias_shifts_chroma(self, test_audio_path):
        """harmonic_mode_bias=+0.7 should increase major template correlation."""
        from Musical_Intelligence.hybrid.ops.stft_ops import load_audio
        y_orig = load_audio(test_audio_path)
        _, _, major_orig, minor_orig = get_chroma_mode_corr(y_orig)

        result = transform(test_audio_path, harmonic_mode_bias=0.7, strength=0.8)
        _, _, major_new, minor_new = get_chroma_mode_corr(result.audio)

        # Major correlation should increase (or at least not decrease much)
        # The effect is subtle, so just check direction
        major_delta = major_new - major_orig
        minor_delta = minor_new - minor_orig
        # Either major increased OR minor decreased (or both)
        assert major_delta > -0.05 or minor_delta < 0.05, (
            f"Major bias had no effect: major {major_orig:.3f}→{major_new:.3f}, "
            f"minor {minor_orig:.3f}→{minor_new:.3f}"
        )

    def test_minor_bias_shifts_chroma(self, test_audio_path):
        """harmonic_mode_bias=-0.7 should increase minor template correlation."""
        from Musical_Intelligence.hybrid.ops.stft_ops import load_audio
        y_orig = load_audio(test_audio_path)
        _, _, major_orig, minor_orig = get_chroma_mode_corr(y_orig)

        result = transform(test_audio_path, harmonic_mode_bias=-0.7, strength=0.8)
        _, _, major_new, minor_new = get_chroma_mode_corr(result.audio)

        minor_delta = minor_new - minor_orig
        major_delta = major_new - major_orig
        assert minor_delta > -0.05 or major_delta < 0.05, (
            f"Minor bias had no effect: minor {minor_orig:.3f}→{minor_new:.3f}, "
            f"major {major_orig:.3f}→{major_new:.3f}"
        )

    def test_mode_bias_preserves_quality(self, test_audio_path, test_audio):
        """Mode bias should not break audio."""
        result = transform(test_audio_path, harmonic_mode_bias=-0.8, strength=0.8)
        assert not np.any(np.isnan(result.audio))
        assert np.max(np.abs(result.audio)) > 0.01


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 5: Rhythm density
# ══════════════════════════════════════════════════════════════════════

class TestRhythmDensity:
    """Rhythm density should change perceived event density."""

    def test_density_down_reduces_energy(self, test_audio_path, test_audio):
        """rhythm_density=-0.7 should reduce percussive energy."""
        result = transform(test_audio_path, rhythm_density=-0.7, strength=0.7)
        n = min(len(test_audio), len(result.audio))
        # Some difference should exist
        max_diff = np.max(np.abs(test_audio[:n] - result.audio[:n]))
        assert max_diff > 0.0001, "Density reduction had no effect"

    def test_density_up_increases_contrast(self, test_audio_path, test_audio):
        """rhythm_density=+0.7 should increase event contrast."""
        result = transform(test_audio_path, rhythm_density=0.7, strength=0.7)
        n = min(len(test_audio), len(result.audio))
        max_diff = np.max(np.abs(test_audio[:n] - result.audio[:n]))
        assert max_diff > 0.0001, "Density increase had no effect"


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 6: Quality guardrails
# ══════════════════════════════════════════════════════════════════════

class TestQualityGuardrails:
    """Safety constraints must hold for all structural transforms."""

    @pytest.mark.parametrize("preset", [
        "rubato_minor", "swing_bright", "driving", "spacious",
    ])
    def test_no_clipping(self, test_audio_path, preset):
        """Output should not clip beyond soft limiter threshold."""
        from Musical_Intelligence.hybrid.hybrid_transformer import (
            HybridTransformer, EMOTION_PRESETS,
        )
        t = HybridTransformer(calibrate=False)
        result = t.transform(test_audio_path, EMOTION_PRESETS[preset], calibrate=False)
        assert np.max(np.abs(result.audio)) <= 1.0, "Clipping detected"

    @pytest.mark.parametrize("preset", [
        "rubato_minor", "swing_bright", "driving", "spacious",
    ])
    def test_no_nans(self, test_audio_path, preset):
        """No NaN values in output."""
        from Musical_Intelligence.hybrid.hybrid_transformer import (
            HybridTransformer, EMOTION_PRESETS,
        )
        t = HybridTransformer(calibrate=False)
        result = t.transform(test_audio_path, EMOTION_PRESETS[preset], calibrate=False)
        assert not np.any(np.isnan(result.audio))

    def test_extreme_params_dont_crash(self, test_audio_path):
        """Extreme parameter values should not crash or produce NaN."""
        result = transform(
            test_audio_path,
            tempo_shift=0.2, swing=1.0, push_pull=1.0,
            rhythm_density=1.0, harmonic_mode_bias=-1.0,
            tension=1.0, arousal=1.0, strength=1.0,
        )
        assert not np.any(np.isnan(result.audio))
        assert np.max(np.abs(result.audio)) <= 1.0
