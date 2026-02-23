"""Test 02 — R³ Full Extraction Benchmark.

Runs R³ (97-D spectral feature extraction) on all 7 real audio files,
measuring extraction time, throughput (fps), and validating output quality.

Checks:
- R³ output shape: (1, T, 97)
- All features in [0, 1]
- No NaN/Inf in outputs
- Per-file extraction time and fps
- 9 spectral groups produce non-zero output
- Feature names match 97 canonical names
"""
from __future__ import annotations

import gc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    R3_GROUPS,
    Timer,
    load_audio_file,
)



@pytest.mark.benchmark
class TestR3Benchmark:
    """Benchmark R³ extraction on real audio."""

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_r3_shape(self, r3_extractor, name: str) -> None:
        """R³ output has correct (1, T, 97) shape."""
        _, mel, _ = load_audio_file(name)
        r3_output = r3_extractor.extract(mel)
        B, T, D = r3_output.features.shape
        assert B == 1
        assert D == 97, f"Expected 97D, got {D}"
        assert T == mel.shape[2], f"T mismatch: R³={T}, mel={mel.shape[2]}"

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_r3_bounds(self, r3_extractor, name: str) -> None:
        """All R³ features in [0, 1], no NaN/Inf."""
        _, mel, _ = load_audio_file(name)
        features = r3_extractor.extract(mel).features

        assert not torch.isnan(features).any(), f"{name}: R³ contains NaN"
        assert not torch.isinf(features).any(), f"{name}: R³ contains Inf"
        assert features.min() >= -1e-6, f"{name}: R³ min={features.min():.6f}"
        assert features.max() <= 1.0 + 1e-6, f"{name}: R³ max={features.max():.6f}"

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_r3_groups_active(self, r3_extractor, name: str) -> None:
        """All 9 R³ groups produce non-zero features for real audio."""
        _, mel, _ = load_audio_file(name)
        features = r3_extractor.extract(mel).features  # (1, T, 97)

        inactive_groups = []
        for group_name, (start, end) in R3_GROUPS.items():
            group_slice = features[:, :, start:end]
            if group_slice.mean() < 1e-6:
                inactive_groups.append(group_name)

        assert len(inactive_groups) == 0, \
            f"{name}: Inactive R³ groups: {inactive_groups}"

    def test_r3_feature_names(self, r3_extractor) -> None:
        """R³ produces exactly 97 named features."""
        _, mel, _ = load_audio_file("bach")
        r3_output = r3_extractor.extract(mel)
        assert len(r3_output.feature_names) == 97, \
            f"Expected 97 names, got {len(r3_output.feature_names)}"

    def test_r3_throughput_benchmark(self, r3_extractor) -> None:
        """Benchmark R³ throughput (fps) on all files."""
        results = {}
        for name in AUDIO_CATALOG:
            _, mel, duration = load_audio_file(name)
            T = mel.shape[2]

            with Timer() as t:
                r3_output = r3_extractor.extract(mel)

            fps = T / t.elapsed_s if t.elapsed_s > 0 else float("inf")
            results[name] = {
                "frames": T,
                "duration_s": duration,
                "time_s": t.elapsed_s,
                "fps": fps,
            }
            gc.collect()

        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║              R³ Extraction Benchmark (30s)                  ║")
        print("╠══════════════════╦════════╦══════════╦═════════╦════════════╣")
        print("║ Track            ║ Frames ║ Time (s) ║  FPS    ║ Status     ║")
        print("╠══════════════════╬════════╬══════════╬═════════╬════════════╣")
        for name, r in results.items():
            status = "FAST" if r["fps"] > 10000 else "OK" if r["fps"] > 1000 else "SLOW"
            print(f"║ {name:<16s} ║ {r['frames']:>6d} ║ {r['time_s']:>8.3f} ║ {r['fps']:>7.0f} ║ {status:<10s} ║")
        print("╚══════════════════╩════════╩══════════╩═════════╩════════════╝")

        avg_fps = sum(r["fps"] for r in results.values()) / len(results)
        print(f"  Average FPS: {avg_fps:.0f}")

    def test_r3_temporal_variation(self, r3_extractor) -> None:
        """R³ features show temporal variation (not constant over time)."""
        _, mel, _ = load_audio_file("herald")
        features = r3_extractor.extract(mel).features  # (1, T, 97)

        # Compute std over time for each feature
        temporal_std = features.squeeze(0).std(dim=0)  # (97,)
        constant_features = (temporal_std < 1e-6).sum().item()
        assert constant_features < 10, \
            f"{constant_features}/97 features are temporally constant"
