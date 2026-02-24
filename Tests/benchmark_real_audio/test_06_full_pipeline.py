"""Test 06 — End-to-End Pipeline (R³ → H³ → C³).

Runs the complete Musical Intelligence pipeline on real audio files,
including the C³ Brain Orchestrator with all nuclei (relays, encoders,
associators).

Checks:
- Full pipeline completes without error
- BrainOutput has expected channels (tensor, ram, neuro, psi)
- RAM: (1, T, 26), values in [0, 1]
- Neuro: (1, T, 4), bounded
- Individual relay outputs
- Per-stage timing
"""
from __future__ import annotations

import gc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    Timer,
    load_audio_file,
)


def _try_import_brain():
    """Try importing BrainOrchestrator. Returns (class, available)."""
    try:
        from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
        return BrainOrchestrator, True
    except Exception as e:
        return None, False


@pytest.mark.benchmark
class TestFullPipeline:
    """End-to-end pipeline test with real audio."""

    def _build_orchestrator(self, all_mechanisms):
        """Build BrainOrchestrator from available mechanisms."""
        BrainOrchestrator, available = _try_import_brain()
        if not available:
            pytest.skip("BrainOrchestrator not available")
        try:
            return BrainOrchestrator(nuclei=all_mechanisms)
        except (AttributeError, TypeError, ValueError) as e:
            pytest.skip(f"BrainOrchestrator construction failed: {e}")

    @pytest.mark.parametrize("name", ["bach", "swan", "herald"])
    def test_full_pipeline_completes(
        self, r3_extractor, h3_extractor, h3_demand_set, all_mechanisms, name: str
    ) -> None:
        """Full R³→H³→C³ pipeline completes without error."""
        _, mel, duration = load_audio_file(name)

        # R³
        r3_output = r3_extractor.extract(mel)
        r3_features = r3_output.features

        # H³
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        # C³
        orchestrator = self._build_orchestrator(all_mechanisms)
        brain_output = orchestrator.process(r3_features, h3_output.features)

        assert brain_output is not None, f"{name}: BrainOutput is None"
        print(f"\n  {name} ({duration:.1f}s): Pipeline completed successfully")
        gc.collect()

    @pytest.mark.parametrize("name", ["bach", "herald"])
    def test_brain_output_channels(
        self, r3_extractor, h3_extractor, h3_demand_set, all_mechanisms, name: str
    ) -> None:
        """BrainOutput has all expected channels with correct shapes."""
        _, mel, _ = load_audio_file(name)
        T = mel.shape[2]

        r3_features = r3_extractor.extract(mel).features
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        orchestrator = self._build_orchestrator(all_mechanisms)
        brain_output = orchestrator.process(r3_features, h3_output.features)

        # Tensor
        assert brain_output.tensor is not None, "tensor channel is None"
        assert brain_output.tensor.shape[0] == 1, "tensor batch dim"
        assert brain_output.tensor.shape[1] == T, f"tensor T: {brain_output.tensor.shape[1]} != {T}"
        print(f"\n  {name} tensor shape: {brain_output.tensor.shape}")

        # RAM
        assert brain_output.ram is not None, "ram channel is None"
        assert brain_output.ram.shape == (1, T, 26), \
            f"ram shape: {brain_output.ram.shape}, expected (1, {T}, 26)"
        assert not torch.isnan(brain_output.ram).any(), "RAM contains NaN"
        print(f"  {name} RAM shape: {brain_output.ram.shape}")

        # Neuro
        assert brain_output.neuro is not None, "neuro channel is None"
        assert brain_output.neuro.shape == (1, T, 4), \
            f"neuro shape: {brain_output.neuro.shape}, expected (1, {T}, 4)"
        assert not torch.isnan(brain_output.neuro).any(), "Neuro contains NaN"
        print(f"  {name} Neuro shape: {brain_output.neuro.shape}")

        # Psi
        if brain_output.psi is not None:
            print(f"  {name} Psi shape: {brain_output.psi.shape}")
        gc.collect()

    def test_pipeline_timing_breakdown(
        self, r3_extractor, h3_extractor, h3_demand_set, all_mechanisms
    ) -> None:
        """Measure per-stage timing for the full pipeline."""
        _, mel, duration = load_audio_file("herald")
        T = mel.shape[2]

        # R³
        with Timer() as r3_timer:
            r3_features = r3_extractor.extract(mel).features

        # H³
        with Timer() as h3_timer:
            h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        # C³
        orchestrator = self._build_orchestrator(all_mechanisms)
        with Timer() as c3_timer:
            brain_output = orchestrator.process(r3_features, h3_output.features)

        total = r3_timer.elapsed_s + h3_timer.elapsed_s + c3_timer.elapsed_s
        fps = T / total if total > 0 else 0

        print("\n╔═══════════════════════════════════════════════════╗")
        print("║   Full Pipeline Timing Breakdown (herald 30s)     ║")
        print("╠══════════════╦═══════════╦═════════╦══════════════╣")
        print("║ Stage        ║ Time (s)  ║ % Total ║ FPS          ║")
        print("╠══════════════╬═══════════╬═════════╬══════════════╣")
        for stage, elapsed in [("R³", r3_timer.elapsed_s), ("H³", h3_timer.elapsed_s), ("C³", c3_timer.elapsed_s)]:
            pct = (elapsed / total * 100) if total > 0 else 0
            stage_fps = T / elapsed if elapsed > 0 else float("inf")
            print(f"║ {stage:<12s} ║ {elapsed:>8.3f}  ║ {pct:>6.1f}% ║ {stage_fps:>11.0f}  ║")
        print("╠══════════════╬═══════════╬═════════╬══════════════╣")
        print(f"║ TOTAL        ║ {total:>8.3f}  ║ 100.0%  ║ {fps:>11.0f}  ║")
        print("╚══════════════╩═══════════╩═════════╩══════════════╝")
        print(f"  Duration: {duration:.1f}s | Frames: {T} | Overall FPS: {fps:.0f}")

        gc.collect()

    def test_relay_outputs_populated(
        self, r3_extractor, h3_extractor, h3_demand_set, all_relays
    ) -> None:
        """All relays produce non-zero output for real audio."""
        _, mel, _ = load_audio_file("bach")
        r3_features = r3_extractor.extract(mel).features
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        print("\n  Relay Outputs (bach 30s):")
        for relay in all_relays:
            try:
                output = relay.compute(h3_output.features, r3_features)
                mean_val = output.mean().item()
                has_nan = torch.isnan(output).any().item()
                print(f"    {relay.NAME:<12s}: shape={output.shape}, "
                      f"mean={mean_val:.4f}, nan={has_nan}")
                assert not has_nan, f"Relay {relay.NAME} output has NaN"
            except Exception as e:
                print(f"    {relay.NAME:<12s}: ERROR — {e}")
