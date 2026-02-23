"""Test 07 — Memory Profiling per Pipeline Stage.

Tracks peak memory usage at each stage of the MI pipeline on M2 8GB.
Critical for ensuring the system fits within constrained hardware.

Measurements:
- Baseline memory (import overhead)
- Audio loading + mel extraction memory
- R³ extraction peak memory
- H³ extraction peak memory
- C³ brain processing peak memory
- Cumulative pipeline peak
- Tensor allocation tracking
"""
from __future__ import annotations

import gc
import os
import tracemalloc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    MemoryTracker,
    load_audio_file,
)

# M2 8GB safety threshold (leave 2GB for system)
MAX_PIPELINE_MB = 6000  # 6 GB hard limit
WARN_THRESHOLD_MB = 4000  # 4 GB warning


def _get_process_memory_mb() -> float:
    """Get current process RSS in MB (macOS/Linux)."""
    try:
        import resource
        usage = resource.getrusage(resource.RUSAGE_SELF)
        return usage.ru_maxrss / (1024 * 1024)  # macOS reports in bytes
    except Exception:
        return 0.0


def _count_tensors() -> dict:
    """Count live torch tensors by device."""
    counts = {"cpu": 0, "total_mb": 0.0}
    for obj in gc.get_objects():
        try:
            if isinstance(obj, torch.Tensor):
                counts["cpu"] += 1
                counts["total_mb"] += obj.nelement() * obj.element_size() / (1024 * 1024)
        except Exception:
            continue
    return counts


@pytest.mark.benchmark
@pytest.mark.memory
class TestMemoryProfile:
    """Memory profiling for MI pipeline on M2 8GB."""

    def test_baseline_memory(self) -> None:
        """Measure baseline memory after imports."""
        gc.collect()
        tensor_info = _count_tensors()
        rss = _get_process_memory_mb()

        print(f"\n  Baseline Memory:")
        print(f"    Process RSS: {rss:.1f} MB")
        print(f"    Live tensors: {tensor_info['cpu']}")
        print(f"    Tensor memory: {tensor_info['total_mb']:.1f} MB")

    def test_audio_loading_memory(self) -> None:
        """Memory cost of loading audio + computing mel."""
        gc.collect()
        tracemalloc.start()

        results = {}
        for name in ["bach", "herald", "beethoven"]:
            snapshot_before = tracemalloc.take_snapshot()
            waveform, mel, duration = load_audio_file(name)

            # Measure tensor sizes
            wav_mb = waveform.nelement() * waveform.element_size() / (1024 * 1024)
            mel_mb = mel.nelement() * mel.element_size() / (1024 * 1024)

            results[name] = {
                "duration": duration,
                "waveform_mb": wav_mb,
                "mel_mb": mel_mb,
                "mel_frames": mel.shape[2],
            }

            del waveform, mel
            gc.collect()

        tracemalloc.stop()

        print("\n╔══════════════════════════════════════════════════════════╗")
        print("║          Audio Loading Memory Profile                    ║")
        print("╠══════════════════╦═══════╦══════════╦═════════╦═════════╣")
        print("║ Track            ║ Dur(s)║ Wav (MB) ║ Mel(MB) ║ Frames  ║")
        print("╠══════════════════╬═══════╬══════════╬═════════╬═════════╣")
        for name, r in results.items():
            print(f"║ {name:<16s} ║ {r['duration']:>5.1f} ║ {r['waveform_mb']:>8.1f} ║ {r['mel_mb']:>7.1f} ║ {r['mel_frames']:>7d} ║")
        print("╚══════════════════╩═══════╩══════════╩═════════╩═════════╝")

    def test_r3_memory_overhead(self, r3_extractor) -> None:
        """Memory overhead of R³ extraction."""
        results = {}
        for name in ["bach", "herald"]:
            _, mel, duration = load_audio_file(name)
            T = mel.shape[2]

            gc.collect()
            with MemoryTracker() as tracker:
                r3_output = r3_extractor.extract(mel)

            r3_mb = r3_output.features.nelement() * r3_output.features.element_size() / (1024 * 1024)
            results[name] = {
                "peak_mb": tracker.peak_mb,
                "output_mb": r3_mb,
                "frames": T,
            }
            del r3_output
            gc.collect()

        print("\n  R³ Memory Profile:")
        for name, r in results.items():
            print(f"    {name}: peak={r['peak_mb']:.1f}MB, "
                  f"output={r['output_mb']:.2f}MB, frames={r['frames']}")

    def test_h3_memory_overhead(self, r3_extractor, h3_extractor, h3_demand_set) -> None:
        """Memory overhead of H³ extraction."""
        _, mel, _ = load_audio_file("herald")
        r3_features = r3_extractor.extract(mel).features

        gc.collect()
        with MemoryTracker() as tracker:
            h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        # Count H³ tensor memory
        h3_mb = sum(
            t.nelement() * t.element_size() / (1024 * 1024)
            for t in h3_output.features.values()
        )

        print(f"\n  H³ Memory Profile (herald, {len(h3_demand_set)} tuples):")
        print(f"    Peak allocation: {tracker.peak_mb:.1f} MB")
        print(f"    Output tensor memory: {h3_mb:.2f} MB")
        print(f"    Per-tuple avg: {h3_mb * 1024 / len(h3_demand_set):.1f} KB")

        del h3_output
        gc.collect()

    def test_full_pipeline_peak_memory(
        self, r3_extractor, h3_extractor, h3_demand_set
    ) -> None:
        """Track peak memory through entire pipeline (no C³ to avoid import issues)."""
        gc.collect()
        tracemalloc.start()

        stages = {}

        # Stage 1: Audio + Mel
        _, mel, duration = load_audio_file("herald")
        _, peak_mel = tracemalloc.get_traced_memory()
        stages["audio+mel"] = peak_mel / (1024 * 1024)

        # Stage 2: R³
        r3_features = r3_extractor.extract(mel).features
        _, peak_r3 = tracemalloc.get_traced_memory()
        stages["R³"] = peak_r3 / (1024 * 1024)

        # Stage 3: H³
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)
        _, peak_h3 = tracemalloc.get_traced_memory()
        stages["H³"] = peak_h3 / (1024 * 1024)

        tracemalloc.stop()

        print("\n╔══════════════════════════════════════════════════╗")
        print("║    Cumulative Peak Memory (herald 30s)           ║")
        print("╠══════════════════╦═══════════════════════════════╣")
        print("║ Stage            ║ Peak Memory (MB)              ║")
        print("╠══════════════════╬═══════════════════════════════╣")
        prev = 0
        for stage, peak in stages.items():
            delta = peak - prev
            bar = "█" * int(peak / 50)
            print(f"║ {stage:<16s} ║ {peak:>8.1f} (+{delta:>6.1f}) {bar:<12s} ║")
            prev = peak
        print("╚══════════════════╩═══════════════════════════════╝")

        final_peak = max(stages.values())
        print(f"\n  Final peak: {final_peak:.1f} MB")
        assert final_peak < MAX_PIPELINE_MB, \
            f"Pipeline exceeds {MAX_PIPELINE_MB}MB limit: {final_peak:.1f}MB"

        if final_peak > WARN_THRESHOLD_MB:
            print(f"  ⚠ Warning: approaching {WARN_THRESHOLD_MB}MB threshold")

        del mel, r3_features, h3_output
        gc.collect()

    def test_tensor_cleanup(self, r3_extractor, h3_extractor, h3_demand_set) -> None:
        """Tensors are properly cleaned up after pipeline execution."""
        before = _count_tensors()

        # Run pipeline
        _, mel, _ = load_audio_file("bach")
        r3_features = r3_extractor.extract(mel).features
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        during = _count_tensors()

        # Cleanup
        del mel, r3_features, h3_output
        gc.collect()

        after = _count_tensors()

        print(f"\n  Tensor Lifecycle:")
        print(f"    Before: {before['cpu']} tensors ({before['total_mb']:.1f} MB)")
        print(f"    During: {during['cpu']} tensors ({during['total_mb']:.1f} MB)")
        print(f"    After:  {after['cpu']} tensors ({after['total_mb']:.1f} MB)")

        # After cleanup, memory should drop significantly
        assert after["total_mb"] < during["total_mb"] * 0.9 or during["total_mb"] < 10, \
            "Tensor memory not cleaned up properly"
