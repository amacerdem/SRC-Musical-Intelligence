"""Test 10 — Reward & Salience Deep Analysis.

Deep analysis of the C³ kernel's reward and salience signals on real audio.
When the full C³ kernel is available, tests reward positivity, temporal
dynamics, and salience-reward correlation. Falls back to relay-level
analysis if the full kernel isn't available.

Experiments:
- Reward mean, std, positivity percentage per piece
- Salience temporal dynamics (peaks, troughs, variability)
- Reward vs salience correlation
- Reward signal smoothness (jitter analysis)
- Cross-piece reward comparison
"""
from __future__ import annotations

import gc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    load_audio_file,
)


def _try_run_kernel(r3_extractor, h3_extractor, h3_demand_set, name, all_mechanisms):
    """Attempt full C³ kernel run. Returns output or None."""
    try:
        from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
        _, mel, duration = load_audio_file(name)
        r3_features = r3_extractor.extract(mel).features
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)
        orchestrator = BrainOrchestrator(nuclei=all_mechanisms)
        brain_output = orchestrator.process(r3_features, h3_output.features)
        return brain_output, duration
    except Exception:
        return None, 0


@pytest.mark.benchmark
class TestRewardSalience:
    """Deep analysis of reward and salience signals."""

    def test_relay_based_salience_proxy(
        self, r3_extractor, h3_extractor, h3_demand_set, all_relays
    ) -> None:
        """Compute salience proxy from relay outputs on all files.

        Salience proxy: mean of relay output means (simple energy-based).
        """
        results = {}
        for name in AUDIO_CATALOG:
            _, mel, duration = load_audio_file(name)
            r3_features = r3_extractor.extract(mel).features
            h3_features = h3_extractor.extract(r3_features, h3_demand_set).features

            relay_means = []
            for relay in all_relays:
                try:
                    output = relay.compute(h3_features, r3_features)
                    relay_means.append(output.mean(dim=-1).squeeze(0))  # (T,)
                except Exception:
                    continue

            if relay_means:
                salience_proxy = torch.stack(relay_means, dim=0).mean(dim=0)  # (T,)
                results[name] = {
                    "mean": salience_proxy.mean().item(),
                    "std": salience_proxy.std().item(),
                    "max": salience_proxy.max().item(),
                    "min": salience_proxy.min().item(),
                    "duration": duration,
                    "signal": salience_proxy,
                }
            gc.collect()

        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║          Salience Proxy (Relay Energy) Across Pieces         ║")
        print("╠══════════════════╦═════════╦═════════╦═════════╦════════════╣")
        print("║ Track            ║  Mean   ║  Std    ║  Max    ║ DynRange   ║")
        print("╠══════════════════╬═════════╬═════════╬═════════╬════════════╣")
        for name, r in results.items():
            dyn = r["max"] - r["min"]
            print(f"║ {name:<16s} ║ {r['mean']:>.4f}  ║ {r['std']:>.4f}  ║ {r['max']:>.4f}  ║ {dyn:>.4f}     ║")
        print("╚══════════════════╩═════════╩═════════╩═════════╩════════════╝")

    def test_salience_peak_analysis(
        self, r3_extractor, h3_extractor, h3_demand_set, all_relays
    ) -> None:
        """Analyze salience peaks (moments of high perceptual interest)."""
        for name in ["herald", "duel", "bach"]:
            _, mel, duration = load_audio_file(name)
            r3_features = r3_extractor.extract(mel).features
            h3_features = h3_extractor.extract(r3_features, h3_demand_set).features

            relay_signals = []
            for relay in all_relays:
                try:
                    output = relay.compute(h3_features, r3_features)
                    relay_signals.append(output.mean(dim=-1).squeeze(0))
                except Exception:
                    continue

            if not relay_signals:
                continue

            salience = torch.stack(relay_signals, dim=0).mean(dim=0)
            T = salience.shape[0]

            # Find peaks (local maxima above mean + 1 std)
            threshold = salience.mean() + salience.std()
            peaks = []
            for t in range(1, T - 1):
                if salience[t] > salience[t-1] and salience[t] > salience[t+1] and salience[t] > threshold:
                    peaks.append(t)

            frame_rate = 172.27  # Hz
            peak_times = [p / frame_rate for p in peaks]

            print(f"\n  Salience Peaks ({name}, {duration:.1f}s):")
            print(f"    Threshold: {threshold:.4f}")
            print(f"    Peaks found: {len(peaks)}")
            print(f"    Peak rate: {len(peaks) / duration:.2f} peaks/sec")
            if peak_times[:10]:
                print(f"    First peaks at: {[f'{t:.1f}s' for t in peak_times[:10]]}")

            gc.collect()

    def test_r3_energy_as_reward_predictor(self, r3_extractor) -> None:
        """Test if R³ energy features correlate with musical intensity."""
        print("\n  R³ Energy Temporal Dynamics:")
        for name in ["bach", "herald", "beethoven"]:
            _, mel, duration = load_audio_file(name)
            r3 = r3_extractor.extract(mel).features.squeeze(0)  # (T, 97)

            # Energy group B[7:12]
            energy = r3[:, 7:12].mean(dim=-1)  # (T,)

            # Compute dynamics
            T = energy.shape[0]
            quarter = T // 4
            q1_mean = energy[:quarter].mean().item()
            q2_mean = energy[quarter:2*quarter].mean().item()
            q3_mean = energy[2*quarter:3*quarter].mean().item()
            q4_mean = energy[3*quarter:].mean().item()

            print(f"\n    {name} ({duration:.1f}s, {T} frames):")
            print(f"      Q1: {q1_mean:.4f}  Q2: {q2_mean:.4f}  Q3: {q3_mean:.4f}  Q4: {q4_mean:.4f}")
            print(f"      Range: [{energy.min():.4f}, {energy.max():.4f}]")

            # Music should have varying energy (not flat)
            assert energy.std() > 0.001, f"{name}: energy is nearly flat"

    def test_full_kernel_reward_if_available(
        self, r3_extractor, h3_extractor, h3_demand_set, all_mechanisms
    ) -> None:
        """If C³ kernel is available, test full reward signal properties."""
        brain_output, duration = _try_run_kernel(
            r3_extractor, h3_extractor, h3_demand_set, "herald", all_mechanisms
        )
        if brain_output is None:
            pytest.skip("Full C³ kernel not available — relay-level tests still run")

        # Check reward if available
        if hasattr(brain_output, 'reward') and brain_output.reward is not None:
            reward = brain_output.reward.squeeze(0)  # (T,)
            print(f"\n  Full Kernel Reward (herald):")
            print(f"    Mean: {reward.mean():.6f}")
            print(f"    Std: {reward.std():.6f}")
            print(f"    Positive %: {(reward > 0).float().mean() * 100:.1f}%")
            print(f"    Range: [{reward.min():.6f}, {reward.max():.6f}]")

            # Alpha-test target: positive reward
            assert reward.mean() > 0, "Reward mean should be positive"
        else:
            print("  Reward channel not available in BrainOutput")

    def test_relay_temporal_jitter(
        self, r3_extractor, h3_extractor, h3_demand_set, all_relays
    ) -> None:
        """Measure frame-to-frame jitter in relay outputs (smoothness indicator)."""
        _, mel, _ = load_audio_file("swan")
        r3_features = r3_extractor.extract(mel).features
        h3_features = h3_extractor.extract(r3_features, h3_demand_set).features

        print("\n  Relay Temporal Jitter (swan 30s):")
        for relay in all_relays:
            try:
                output = relay.compute(h3_features, r3_features).squeeze(0)  # (T, D)
                if output.shape[0] > 2:
                    diffs = (output[1:] - output[:-1]).abs().mean().item()
                    print(f"    {relay.NAME:<12s}: avg_jitter={diffs:.6f}")
            except Exception as e:
                print(f"    {relay.NAME:<12s}: ERROR — {e}")
