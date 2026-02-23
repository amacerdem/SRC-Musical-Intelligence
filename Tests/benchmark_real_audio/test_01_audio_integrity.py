"""Test 01 — Audio Integrity & Mel Extraction.

Validates that all 7 test audio files load correctly, produce valid mel
spectrograms with expected shapes, and measures loading performance.

Checks:
- All files exist and are readable by torchaudio
- Waveform: mono, correct sample rate, no NaN/Inf
- Mel spectrogram: (1, 128, T), [0, 1] bounds, no NaN
- Loading time per file
- Frame count matches expected duration
"""
from __future__ import annotations

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    DEFAULT_EXCERPT_S,
    FRAME_RATE,
    N_MELS,
    Timer,
    load_audio_file,
)


@pytest.mark.benchmark
class TestAudioIntegrity:
    """Validate all 7 audio files load and produce valid mel spectrograms."""

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_file_loads_successfully(self, name: str) -> None:
        """Each audio file loads without error."""
        waveform, mel, duration = load_audio_file(name)
        assert waveform is not None
        assert mel is not None
        assert duration > 0

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_waveform_properties(self, name: str) -> None:
        """Waveform is mono, float32, no NaN/Inf."""
        waveform, _, duration = load_audio_file(name)

        assert waveform.ndim == 2, f"Expected 2D (1, N), got {waveform.ndim}D"
        assert waveform.shape[0] == 1, f"Expected mono, got {waveform.shape[0]} channels"
        assert waveform.dtype == torch.float32
        assert not torch.isnan(waveform).any(), "Waveform contains NaN"
        assert not torch.isinf(waveform).any(), "Waveform contains Inf"
        assert duration <= DEFAULT_EXCERPT_S + 0.1, \
            f"Excerpt should be ≤{DEFAULT_EXCERPT_S}s, got {duration:.1f}s"

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_mel_shape_and_bounds(self, name: str) -> None:
        """Mel spectrogram has correct shape and [0, 1] bounds."""
        _, mel, duration = load_audio_file(name)

        B, n_mels, T = mel.shape
        assert B == 1, f"Batch size should be 1, got {B}"
        assert n_mels == N_MELS, f"Expected {N_MELS} mel bins, got {n_mels}"

        # T should match duration approximately
        expected_T = int(duration * FRAME_RATE)
        assert abs(T - expected_T) <= 2, \
            f"Frame count mismatch: got {T}, expected ~{expected_T} ({duration:.1f}s)"

        # Bounds
        assert mel.min() >= 0.0, f"Mel min below 0: {mel.min():.4f}"
        assert mel.max() <= 1.0 + 1e-6, f"Mel max above 1: {mel.max():.4f}"
        assert not torch.isnan(mel).any(), "Mel contains NaN"

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_mel_not_silent(self, name: str) -> None:
        """Mel spectrogram has meaningful energy (not all zeros)."""
        _, mel, _ = load_audio_file(name)
        energy = mel.mean().item()
        assert energy > 0.01, f"Mel appears silent: mean energy {energy:.4f}"

    def test_loading_performance(self) -> None:
        """All 7 files load within acceptable time budget."""
        results = {}
        for name in AUDIO_CATALOG:
            with Timer() as t:
                load_audio_file(name)
            results[name] = t.elapsed_s

        print("\n╔══════════════════════════════════════════════════╗")
        print("║     Audio Loading Performance (30s excerpts)     ║")
        print("╠══════════════════════╦═══════════╦═══════════════╣")
        print("║ Track                ║ Time (s)  ║ Status        ║")
        print("╠══════════════════════╬═══════════╬═══════════════╣")
        for name, elapsed in results.items():
            status = "OK" if elapsed < 5.0 else "SLOW"
            print(f"║ {name:<20s} ║ {elapsed:>7.2f}   ║ {status:<13s} ║")
        print("╚══════════════════════╩═══════════╩═══════════════╝")

        total = sum(results.values())
        print(f"  Total: {total:.2f}s | Average: {total/len(results):.2f}s per file")

        # Each file should load in under 10s
        for name, elapsed in results.items():
            assert elapsed < 10.0, f"{name} loading took {elapsed:.1f}s (> 10s budget)"

    def test_full_duration_loads(self) -> None:
        """Shortest files (bach, duel) load at full duration without OOM."""
        for name in ["bach", "duel"]:
            waveform, mel, duration = load_audio_file(name, excerpt_s=None)
            assert mel.shape[2] > 0, f"{name} full duration produced no frames"
            print(f"  {name}: {duration:.1f}s → {mel.shape[2]} frames")

    def test_mp3_format_support(self) -> None:
        """MP3 format (yang.mp3) loads correctly alongside WAV files."""
        waveform, mel, duration = load_audio_file("yang")
        assert mel.shape[1] == N_MELS
        assert mel.shape[2] > 100, "MP3 produced too few frames"
