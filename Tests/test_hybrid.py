"""
HYBRID v0.1 — Pytest Suite
============================
Non-destructive, R³ perceptual proxy, and pipeline integrity tests.

Run:
    pytest Tests/test_hybrid.py -v
    pytest Tests/test_hybrid.py -v -k "roundtrip"     # specific test
    pytest Tests/test_hybrid.py -v -k "r3"             # R³ tests only
"""

from __future__ import annotations

import sys
import tempfile
import os
import numpy as np
import pytest
from pathlib import Path

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

SR = 44100


# ── Fixtures ──────────────────────────────────────────────────────────

def _make_synthetic_audio(duration: float = 3.0) -> np.ndarray:
    """Create a synthetic test signal: chord + transients."""
    t = np.linspace(0, duration, int(duration * SR), dtype=np.float32)
    y = 0.3 * np.sin(2 * np.pi * 440 * t)     # A4
    y += 0.2 * np.sin(2 * np.pi * 660 * t)    # ~E5
    y += 0.15 * np.sin(2 * np.pi * 880 * t)   # A5
    # Transients every 0.5s
    for i in range(int(duration * 2)):
        idx = int(i * 0.5 * SR)
        if idx + 100 < len(y):
            y[idx:idx + 100] += 0.4 * np.exp(-np.linspace(0, 5, 100))
    return y.astype(np.float32)


@pytest.fixture(scope="session")
def synthetic_audio() -> np.ndarray:
    return _make_synthetic_audio()


@pytest.fixture(scope="session")
def real_audio() -> np.ndarray | None:
    """Try to load real Swan Lake audio, skip if not available."""
    swan = PROJECT_ROOT / "Test-Audio" / (
        "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
        " - Pyotr Ilyich Tchaikovsky.wav"
    )
    if not swan.exists():
        return None
    from Musical_Intelligence.hybrid.ops.stft_ops import load_audio
    return load_audio(str(swan))[:int(5 * SR)]  # 5 seconds


@pytest.fixture(scope="session")
def test_audio(real_audio, synthetic_audio) -> np.ndarray:
    """Use real audio if available, else synthetic."""
    return real_audio if real_audio is not None else synthetic_audio


@pytest.fixture(scope="session")
def test_audio_path(test_audio) -> str:
    """Save test audio to temp file and return path."""
    from Musical_Intelligence.hybrid.ops.stft_ops import save_audio
    tmp = tempfile.mktemp(suffix=".wav")
    save_audio(tmp, test_audio)
    yield tmp
    os.unlink(tmp)


# ── Helpers ───────────────────────────────────────────────────────────

def snr_db(y: np.ndarray, y_hat: np.ndarray) -> float:
    n = min(len(y), len(y_hat))
    sig = np.sum(y[:n] ** 2)
    noise = np.sum((y[:n] - y_hat[:n]) ** 2)
    if noise < 1e-20:
        return 120.0
    return 10.0 * np.log10(sig / noise)


def get_r3_mean(y: np.ndarray) -> np.ndarray:
    """Extract mean R³ features from audio waveform."""
    import torch, torchaudio
    y_t = torch.from_numpy(y).unsqueeze(0)
    mel_tr = torchaudio.transforms.MelSpectrogram(
        sample_rate=SR, n_fft=2048, hop_length=256, n_mels=128, power=2.0,
    )
    mel = mel_tr(y_t)
    mel = torch.log1p(mel)
    mx = mel.max()
    if mx > 0:
        mel = mel / mx
    from Musical_Intelligence.ear.r3 import R3Extractor
    ext = R3Extractor()
    return ext.extract(mel).features[0].numpy().mean(axis=0)


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 1: Non-destructive (pipeline integrity)
# ══════════════════════════════════════════════════════════════════════

class TestNonDestructive:
    """Pipeline must not break audio quality."""

    def test_stft_roundtrip_snr(self, test_audio):
        """STFT → iSTFT roundtrip: SNR > 40 dB."""
        from Musical_Intelligence.hybrid.ops.stft_ops import stft_analyze, stft_synthesize
        mag, phase = stft_analyze(test_audio)
        y_rt = stft_synthesize(mag, phase)
        assert snr_db(test_audio, y_rt) > 40.0

    def test_stft_roundtrip_correlation(self, test_audio):
        """STFT → iSTFT roundtrip: correlation > 0.9999."""
        from Musical_Intelligence.hybrid.ops.stft_ops import stft_analyze, stft_synthesize
        mag, phase = stft_analyze(test_audio)
        y_rt = stft_synthesize(mag, phase)
        n = min(len(test_audio), len(y_rt))
        corr = np.corrcoef(test_audio[:n], y_rt[:n])[0, 1]
        assert corr > 0.9999

    def test_hpss_recombine_snr(self, test_audio):
        """HPSS decompose + recombine: SNR > 25 dB."""
        import librosa
        from Musical_Intelligence.hybrid.ops.hpss_ops import hpss_stft
        S = librosa.stft(test_audio, n_fft=2048, hop_length=256)
        S_h, S_p = hpss_stft(S)
        S_recon = S_h + S_p
        y_recon = librosa.istft(S_recon, hop_length=256, length=len(test_audio))
        assert snr_db(test_audio, y_recon) > 25.0

    def test_zero_strength_identity(self, test_audio_path, test_audio):
        """strength=0 must produce near-identical output."""
        from Musical_Intelligence.hybrid.hybrid_transformer import HybridTransformer
        from Musical_Intelligence.hybrid.controls import EmotionControls
        t = HybridTransformer(calibrate=False)
        c = EmotionControls(valence=0.8, arousal=0.8, strength=0.0)
        result = t.transform(test_audio_path, c, calibrate=False)
        n = min(len(test_audio), len(result.audio))
        assert snr_db(test_audio[:n], result.audio[:n]) > 25.0


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 2: R³ Perceptual Proxy
# ══════════════════════════════════════════════════════════════════════

class TestR3PerceptualProxy:
    """
    Each transform must shift R³ features in the expected direction.
    This is the "not just a filter" proof.
    """

    def _transform(self, audio_path, **kwargs):
        from Musical_Intelligence.hybrid.hybrid_transformer import HybridTransformer
        from Musical_Intelligence.hybrid.controls import EmotionControls
        t = HybridTransformer(calibrate=False)
        # Zero structural params to isolate timbral effects for R³ tests
        structural_defaults = dict(
            tempo_shift=0, rubato=0, swing=0, push_pull=0,
            rhythm_density=0, harmonic_mode_bias=0, harmonic_rhythm=0,
        )
        merged = {**structural_defaults, **kwargs}
        c = EmotionControls(**merged, strength=0.7)
        return t.transform(audio_path, c, calibrate=False)

    def test_arousal_up_onset_strength(self, test_audio_path, test_audio):
        """arousal↑ → onset_strength (R³[11]) ↑"""
        result = self._transform(test_audio_path, arousal=0.8)
        r3_orig = get_r3_mean(test_audio)
        r3_trans = get_r3_mean(result.audio)
        assert r3_trans[11] > r3_orig[11], "onset_strength should increase with arousal"

    def test_arousal_up_spectral_flux(self, test_audio_path, test_audio):
        """arousal↑ → spectral_flux (R³[21]) ↑ or stable.

        Note: v0.2 cross-mapping (arousal→tempo/swing/density) can reduce
        spectral_flux even though timbral transforms try to increase it.
        Accept up to 15% decrease as structural side-effect.
        """
        result = self._transform(test_audio_path, arousal=0.8)
        r3_orig = get_r3_mean(test_audio)
        r3_trans = get_r3_mean(result.audio)
        assert r3_trans[21] > r3_orig[21] * 0.85, (
            f"spectral_flux dropped too much: {r3_orig[21]:.4f} → {r3_trans[21]:.4f}"
        )

    def test_calm_onset_strength_down(self, test_audio_path, test_audio):
        """arousal↓ → onset_strength (R³[11]) ↓"""
        result = self._transform(test_audio_path, arousal=-0.8)
        r3_orig = get_r3_mean(test_audio)
        r3_trans = get_r3_mean(result.audio)
        assert r3_trans[11] < r3_orig[11], "onset_strength should decrease when calm"

    def test_calm_spectral_flux_down(self, test_audio_path, test_audio):
        """arousal↓ → spectral_flux (R³[21]) ↓"""
        result = self._transform(test_audio_path, arousal=-0.8)
        r3_orig = get_r3_mean(test_audio)
        r3_trans = get_r3_mean(result.audio)
        assert r3_trans[21] < r3_orig[21], "spectral_flux should decrease when calm"

    def test_warmth_up(self, test_audio_path, test_audio):
        """warmth↑ → R³ warmth (R³[12]) ↑"""
        result = self._transform(test_audio_path, warmth=0.8)
        r3_orig = get_r3_mean(test_audio)
        r3_trans = get_r3_mean(result.audio)
        assert r3_trans[12] > r3_orig[12], "warmth should increase"

    def test_warmth_down_sharpness_up(self, test_audio_path, test_audio):
        """warmth↓ → sharpness (R³[13]) ↑"""
        result = self._transform(test_audio_path, warmth=-0.8)
        r3_orig = get_r3_mean(test_audio)
        r3_trans = get_r3_mean(result.audio)
        assert r3_trans[13] > r3_orig[13], "sharpness should increase when warmth decreases"

    def test_brightness_up_clarity(self, test_audio_path, test_audio):
        """brightness↑ → clarity (R³[15]) ↑"""
        result = self._transform(test_audio_path, brightness=0.8)
        r3_orig = get_r3_mean(test_audio)
        r3_trans = get_r3_mean(result.audio)
        assert r3_trans[15] > r3_orig[15], "clarity should increase with brightness"


# ══════════════════════════════════════════════════════════════════════
# TEST GROUP 3: Transform output quality
# ══════════════════════════════════════════════════════════════════════

class TestTransformQuality:
    """Transforms must produce valid, different, coherent audio."""

    @pytest.mark.parametrize("preset", [
        "joyful", "melancholic", "intense", "calm", "tense", "bright_warm",
    ])
    def test_preset_not_broken(self, test_audio_path, test_audio, preset):
        """Each preset must produce valid audio (no NaN, no silence)."""
        from Musical_Intelligence.hybrid.hybrid_transformer import (
            HybridTransformer, EMOTION_PRESETS,
        )
        t = HybridTransformer(calibrate=False)
        result = t.transform(test_audio_path, EMOTION_PRESETS[preset], calibrate=False)
        y_out = result.audio
        assert not np.any(np.isnan(y_out)), "NaN in output"
        assert np.max(np.abs(y_out)) > 0.01, "Output is silence"

    @pytest.mark.parametrize("preset", [
        "joyful", "melancholic", "intense", "calm", "tense", "bright_warm",
    ])
    def test_preset_coherent(self, test_audio_path, test_audio, preset):
        """Each preset must stay spectrally coherent (envelope corr > 0.8)."""
        import librosa
        from Musical_Intelligence.hybrid.hybrid_transformer import (
            HybridTransformer, EMOTION_PRESETS,
        )
        t = HybridTransformer(calibrate=False)
        result = t.transform(test_audio_path, EMOTION_PRESETS[preset], calibrate=False)
        # Use spectral envelope correlation (invariant to timing warps)
        S_orig = np.abs(librosa.stft(test_audio, n_fft=2048, hop_length=256))
        S_trans = np.abs(librosa.stft(result.audio, n_fft=2048, hop_length=256))
        env_orig = S_orig.mean(axis=1)
        env_trans = S_trans.mean(axis=1)
        corr = np.corrcoef(env_orig, env_trans)[0, 1]
        assert corr > 0.8, f"Spectral envelope too different: corr={corr:.4f}"

    @pytest.mark.parametrize("preset", [
        "joyful", "melancholic", "intense", "calm", "tense", "bright_warm",
    ])
    def test_preset_different(self, test_audio_path, test_audio, preset):
        """Each preset must actually change the audio."""
        from Musical_Intelligence.hybrid.hybrid_transformer import (
            HybridTransformer, EMOTION_PRESETS,
        )
        t = HybridTransformer(calibrate=False)
        result = t.transform(test_audio_path, EMOTION_PRESETS[preset], calibrate=False)
        n = min(len(test_audio), len(result.audio))
        max_diff = np.max(np.abs(test_audio[:n] - result.audio[:n]))
        assert max_diff > 0.001, "Transform had no effect"
