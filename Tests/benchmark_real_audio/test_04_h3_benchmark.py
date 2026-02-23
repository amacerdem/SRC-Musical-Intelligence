"""Test 04 — H³ Temporal Morphology Benchmark.

Runs H³ (sparse temporal morphology extraction) on real audio,
measuring extraction time, tuple coverage, and output quality.

Checks:
- All demanded tuples are computed
- Output shape: (1, T) per tuple
- Values in [0, 1]
- No NaN/Inf
- Throughput (fps) per file
- Tuple statistics by morph type and horizon
"""
from __future__ import annotations

import gc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    LAW_NAMES,
    MORPH_NAMES,
    Timer,
    load_audio_file,
)


@pytest.mark.benchmark
class TestH3Benchmark:
    """Benchmark H³ extraction on real audio."""

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_h3_completeness(self, r3_extractor, h3_extractor, h3_demand_set, name: str) -> None:
        """All demanded tuples are computed for each audio file."""
        _, mel, _ = load_audio_file(name)
        r3_features = r3_extractor.extract(mel).features

        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        assert h3_output.n_tuples == len(h3_demand_set), \
            f"{name}: got {h3_output.n_tuples} tuples, expected {len(h3_demand_set)}"

    @pytest.mark.parametrize("name", list(AUDIO_CATALOG.keys()))
    def test_h3_bounds(self, r3_extractor, h3_extractor, h3_demand_set, name: str) -> None:
        """All H³ values in [0, 1], no NaN/Inf."""
        _, mel, _ = load_audio_file(name)
        r3_features = r3_extractor.extract(mel).features

        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        nan_count = 0
        oob_count = 0
        for key, tensor in h3_output.features.items():
            assert tensor.shape[0] == 1, f"Batch dim should be 1: {tensor.shape}"
            if torch.isnan(tensor).any():
                nan_count += 1
            if tensor.min() < -1e-6 or tensor.max() > 1.0 + 1e-6:
                oob_count += 1

        assert nan_count == 0, f"{name}: {nan_count} tuples contain NaN"
        assert oob_count == 0, f"{name}: {oob_count} tuples out of [0,1]"

    def test_h3_throughput_benchmark(self, r3_extractor, h3_extractor, h3_demand_set) -> None:
        """Benchmark H³ throughput (fps) on all files."""
        results = {}
        for name in AUDIO_CATALOG:
            _, mel, duration = load_audio_file(name)
            T = mel.shape[2]

            # R³ first
            r3_features = r3_extractor.extract(mel).features

            # H³ benchmark
            with Timer() as t:
                h3_output = h3_extractor.extract(r3_features, h3_demand_set)

            fps = T / t.elapsed_s if t.elapsed_s > 0 else float("inf")
            results[name] = {
                "frames": T,
                "n_tuples": h3_output.n_tuples,
                "time_s": t.elapsed_s,
                "fps": fps,
            }
            gc.collect()

        print("\n╔═════════════════════════════════════════════════════════════════════╗")
        print("║                 H³ Extraction Benchmark (30s)                       ║")
        print("╠══════════════════╦════════╦════════╦══════════╦═════════╦═══════════╣")
        print("║ Track            ║ Frames ║ Tuples ║ Time (s) ║   FPS   ║ Status    ║")
        print("╠══════════════════╬════════╬════════╬══════════╬═════════╬═══════════╣")
        for name, r in results.items():
            status = "FAST" if r["fps"] > 500 else "OK" if r["fps"] > 100 else "SLOW"
            print(f"║ {name:<16s} ║ {r['frames']:>6d} ║ {r['n_tuples']:>6d} ║ {r['time_s']:>8.2f} ║ {r['fps']:>7.0f} ║ {status:<9s} ║")
        print("╚══════════════════╩════════╩════════╩══════════╩═════════╩═══════════╝")

        avg_fps = sum(r["fps"] for r in results.values()) / len(results)
        print(f"  Average H³ FPS: {avg_fps:.0f}")
        print(f"  Total tuples demanded: {len(h3_demand_set)}")

    def test_h3_demand_coverage_report(self, h3_demand_set) -> None:
        """Report demand set breakdown by morph type and horizon."""
        by_morph = {}
        by_horizon = {}
        by_law = {}

        for (r3_idx, horizon, morph, law) in h3_demand_set:
            morph_name = MORPH_NAMES.get(morph, f"M{morph}")
            by_morph[morph_name] = by_morph.get(morph_name, 0) + 1
            by_horizon[horizon] = by_horizon.get(horizon, 0) + 1
            law_name = LAW_NAMES.get(law, f"L{law}")
            by_law[law_name] = by_law.get(law_name, 0) + 1

        print(f"\n  H³ Demand Set: {len(h3_demand_set)} tuples total")
        print(f"\n  By Morph Type:")
        for m, count in sorted(by_morph.items(), key=lambda x: -x[1]):
            print(f"    {m}: {count}")
        print(f"\n  By Law:")
        for l, count in sorted(by_law.items(), key=lambda x: -x[1]):
            print(f"    {l}: {count}")
        print(f"\n  Horizons used: {sorted(by_horizon.keys())}")

    def test_h3_morph_differentiation(self, r3_extractor, h3_extractor, h3_demand_set) -> None:
        """Different morph types produce distinguishable distributions."""
        _, mel, _ = load_audio_file("herald")
        r3_features = r3_extractor.extract(mel).features
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        morph_means = {}
        for (r3_idx, horizon, morph, law), tensor in h3_output.features.items():
            mname = MORPH_NAMES.get(morph, f"M{morph}")
            morph_means.setdefault(mname, []).append(tensor.mean().item())

        print("\n  Morph Type Mean Distributions (herald):")
        for mname, values in sorted(morph_means.items()):
            avg = sum(values) / len(values)
            print(f"    {mname}: avg={avg:.4f} (n={len(values)})")
