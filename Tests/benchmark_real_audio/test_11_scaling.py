"""Test 11 — Duration Scaling & Throughput.

Tests how the MI pipeline scales with audio duration on M2 8GB.
Uses Herald of the Change (5:01 full) at increasing excerpt lengths.

Experiments:
- 5s, 10s, 20s, 30s, 60s, 120s excerpts
- Per-stage timing (R³, H³) at each duration
- FPS stability across durations
- Memory scaling (linear? sublinear?)
- Maximum processable duration before OOM
"""
from __future__ import annotations

import gc
import tracemalloc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    Timer,
    load_audio_file,
)

# Test durations in seconds
SCALING_DURATIONS = [5, 10, 20, 30, 60, 120]


@pytest.mark.benchmark
@pytest.mark.slow
class TestScaling:
    """Duration scaling and throughput experiments."""

    def test_r3_scaling(self, r3_extractor) -> None:
        """R³ extraction time scales with audio duration."""
        results = {}
        for dur in SCALING_DURATIONS:
            try:
                _, mel, actual_dur = load_audio_file("herald", excerpt_s=dur)
                T = mel.shape[2]

                with Timer() as t:
                    r3_output = r3_extractor.extract(mel)

                fps = T / t.elapsed_s if t.elapsed_s > 0 else float("inf")
                results[dur] = {
                    "actual_dur": actual_dur,
                    "frames": T,
                    "time_s": t.elapsed_s,
                    "fps": fps,
                }
                del r3_output, mel
                gc.collect()
            except Exception as e:
                results[dur] = {"error": str(e)}
                break

        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║             R³ Duration Scaling (herald)                      ║")
        print("╠════════╦════════╦══════════╦═════════╦════════════════════════╣")
        print("║ Dur(s) ║ Frames ║ Time (s) ║   FPS   ║ Status                ║")
        print("╠════════╬════════╬══════════╬═════════╬════════════════════════╣")
        for dur, r in results.items():
            if "error" in r:
                print(f"║ {dur:>5d}  ║   —    ║    —     ║    —    ║ ERROR: {r['error'][:20]} ║")
            else:
                status = "OK" if r["fps"] > 1000 else "SLOW"
                print(f"║ {dur:>5d}  ║ {r['frames']:>6d} ║ {r['time_s']:>8.3f} ║ {r['fps']:>7.0f} ║ {status:<22s} ║")
        print("╚════════╩════════╩══════════╩═════════╩════════════════════════╝")

        # FPS should not degrade dramatically with duration
        if len(results) >= 3:
            fps_values = [r["fps"] for r in results.values() if "fps" in r]
            if fps_values:
                fps_ratio = min(fps_values) / max(fps_values)
                print(f"  FPS stability ratio: {fps_ratio:.2f} (1.0 = perfectly stable)")

    def test_h3_scaling(self, r3_extractor, h3_extractor, h3_demand_set) -> None:
        """H³ extraction time scales with audio duration."""
        results = {}
        for dur in SCALING_DURATIONS:
            try:
                _, mel, actual_dur = load_audio_file("herald", excerpt_s=dur)
                r3_features = r3_extractor.extract(mel).features

                with Timer() as t:
                    h3_output = h3_extractor.extract(r3_features, h3_demand_set)

                T = mel.shape[2]
                fps = T / t.elapsed_s if t.elapsed_s > 0 else float("inf")
                results[dur] = {
                    "frames": T,
                    "tuples": h3_output.n_tuples,
                    "time_s": t.elapsed_s,
                    "fps": fps,
                }
                del h3_output, r3_features, mel
                gc.collect()
            except Exception as e:
                results[dur] = {"error": str(e)}
                break

        print("\n╔═══════════════════════════════════════════════════════════════════╗")
        print("║                H³ Duration Scaling (herald)                       ║")
        print("╠════════╦════════╦════════╦══════════╦═════════╦═══════════════════╣")
        print("║ Dur(s) ║ Frames ║ Tuples ║ Time (s) ║   FPS   ║ Status            ║")
        print("╠════════╬════════╬════════╬══════════╬═════════╬═══════════════════╣")
        for dur, r in results.items():
            if "error" in r:
                print(f"║ {dur:>5d}  ║   —    ║   —    ║    —     ║    —    ║ OOM/ERR           ║")
            else:
                status = "OK" if r["fps"] > 100 else "SLOW"
                print(f"║ {dur:>5d}  ║ {r['frames']:>6d} ║ {r['tuples']:>6d} ║ {r['time_s']:>8.2f} ║ {r['fps']:>7.0f} ║ {status:<17s} ║")
        print("╚════════╩════════╩════════╩══════════╩═════════╩═══════════════════╝")

    def test_memory_scaling(self, r3_extractor, h3_extractor, h3_demand_set) -> None:
        """Track memory growth with increasing duration."""
        results = {}
        for dur in SCALING_DURATIONS:
            try:
                gc.collect()
                tracemalloc.start()

                _, mel, _ = load_audio_file("herald", excerpt_s=dur)
                r3_features = r3_extractor.extract(mel).features
                h3_output = h3_extractor.extract(r3_features, h3_demand_set)

                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                peak_mb = peak / (1024 * 1024)
                frames = mel.shape[2]
                mb_per_frame = peak_mb / frames if frames > 0 else 0

                results[dur] = {
                    "peak_mb": peak_mb,
                    "frames": frames,
                    "mb_per_frame": mb_per_frame,
                }

                del mel, r3_features, h3_output
                gc.collect()
            except Exception as e:
                if tracemalloc.is_tracing():
                    tracemalloc.stop()
                results[dur] = {"error": str(e)}
                break

        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║            Memory Scaling (herald, R³+H³)                     ║")
        print("╠════════╦════════╦═══════════╦═══════════════════════════════╣")
        print("║ Dur(s) ║ Frames ║ Peak (MB) ║ MB/frame                      ║")
        print("╠════════╬════════╬═══════════╬═══════════════════════════════╣")
        for dur, r in results.items():
            if "error" in r:
                print(f"║ {dur:>5d}  ║   —    ║    OOM    ║ (max duration exceeded)       ║")
            else:
                bar = "█" * int(r["peak_mb"] / 100)
                print(f"║ {dur:>5d}  ║ {r['frames']:>6d} ║ {r['peak_mb']:>8.1f}  ║ {r['mb_per_frame']:.4f} {bar:<18s}║")
        print("╚════════╩════════╩═══════════╩═══════════════════════════════╝")

        # Check memory stays under 6GB
        peaks = [r["peak_mb"] for r in results.values() if "peak_mb" in r]
        if peaks:
            max_peak = max(peaks)
            print(f"\n  Max peak memory: {max_peak:.1f} MB")
            assert max_peak < 6000, f"Memory exceeded 6GB: {max_peak:.1f}MB"

    def test_full_duration_capability(self, r3_extractor) -> None:
        """Test which files can be processed at full duration on M2 8GB."""
        # Ordered by duration (shortest first)
        test_order = [
            ("bach", "2:32"),
            ("duel", "2:37"),
            ("swan", "3:03"),
            ("herald", "5:01"),
            ("enigma", "6:29"),
            ("beethoven", "8:17"),
        ]

        print("\n  Full Duration Capability Test:")
        for name, expected_dur in test_order:
            try:
                gc.collect()
                with Timer() as t:
                    _, mel, duration = load_audio_file(name, excerpt_s=None)
                    r3_output = r3_extractor.extract(mel)

                T = mel.shape[2]
                fps = T / t.elapsed_s if t.elapsed_s > 0 else 0
                print(f"    ✓ {name:<12s} ({expected_dur}): {T:>6d} frames, "
                      f"{t.elapsed_s:.1f}s, {fps:.0f} fps")

                del mel, r3_output
                gc.collect()
            except Exception as e:
                print(f"    ✗ {name:<12s} ({expected_dur}): FAILED — {e}")
                break

    def test_throughput_consistency(self, r3_extractor) -> None:
        """FPS should be consistent across multiple runs of the same piece."""
        _, mel, _ = load_audio_file("bach")

        fps_values = []
        for _ in range(5):
            with Timer() as t:
                r3_extractor.extract(mel)
            fps = mel.shape[2] / t.elapsed_s if t.elapsed_s > 0 else 0
            fps_values.append(fps)

        avg = sum(fps_values) / len(fps_values)
        std = (sum((f - avg) ** 2 for f in fps_values) / len(fps_values)) ** 0.5
        cv = std / avg if avg > 0 else 0  # coefficient of variation

        print(f"\n  R³ Throughput Consistency (bach, 5 runs):")
        print(f"    Runs: {[f'{f:.0f}' for f in fps_values]}")
        print(f"    Mean: {avg:.0f} fps")
        print(f"    Std: {std:.0f} fps")
        print(f"    CV: {cv:.2%}")

        # CV should be < 30% for consistent performance
        assert cv < 0.30, f"Throughput too variable: CV={cv:.2%}"
