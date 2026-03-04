"""Boundary condition tests — F9 extreme inputs.

Tests that all 10 F9 beliefs produce valid output for edge cases:
  - Near-silence (floor)
  - fff chromatic cluster (ceiling)
  - Single click (impulse)
  - Dense random (noise floor)
  - Very slow tempo (40bpm)
  - Very fast tempo (240bpm)
  - Extreme register (C1+C7)
  - Long duration (32 bars)
"""
from __future__ import annotations

import pathlib

import numpy as np
import torch
from scipy.io import wavfile

from Tests.micro_beliefs.assertions import assert_in_range

_SR = 44_100
_F9_AUDIO = (
    pathlib.Path(__file__).resolve().parent.parent.parent.parent
    / "Test-Audio" / "micro_beliefs" / "f9"
)

F9_ALL_BELIEFS = [
    # NSCP
    "neural_synchrony", "catchiness_pred",
    # SSRI
    "synchrony_reward", "social_bonding", "group_flow",
    "entrainment_quality", "social_prediction_error",
    "collective_pleasure_pred",
    # DDSMI
    "social_coordination", "resource_allocation",
]


def _load(group: str, name: str) -> torch.Tensor:
    """Load pre-generated F9 test audio as (1, N) float32 tensor."""
    wav_path = _F9_AUDIO / group / f"{name}.wav"
    sr, data = wavfile.read(str(wav_path))
    assert sr == _SR, f"Expected {_SR} Hz, got {sr}"
    audio = data.astype(np.float32) / 32767.0
    return torch.from_numpy(audio).unsqueeze(0)


class TestBoundaryNearSilence:
    """Near-silence: all beliefs should produce valid output near floor."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "01_near_silence")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"near_silence/{b}")


class TestBoundaryFffCluster:
    """fff chromatic cluster: max amplitude, all beliefs valid."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "02_fff_cluster")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"fff_cluster/{b}")


class TestBoundarySingleClick:
    """Single loud click: impulse response, all beliefs valid."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "03_single_click")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"single_click/{b}")


class TestBoundaryDenseRandom:
    """Dense random (16 notes/sec): no structure, all beliefs valid."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "04_dense_random_noise")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"dense_random/{b}")


class TestBoundaryVerySlowTempo:
    """Very slow 40bpm: all beliefs valid at ultra-macro scale."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "05_very_slow_40bpm")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"slow_40bpm/{b}")


class TestBoundaryVeryFastTempo:
    """Very fast 240bpm: all beliefs valid near motor limit."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "06_very_fast_240bpm")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"fast_240bpm/{b}")


class TestBoundaryExtremeRegister:
    """Extreme register (C1+C7): all beliefs valid at pitch extremes."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "07_extreme_register")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"extreme_register/{b}")


class TestBoundaryLongDuration:
    """Long duration (~32 bars): all beliefs valid, no accumulation errors."""

    def test_all_beliefs_valid(self, runner):
        audio = _load("boundary", "08_long_duration_32bar")
        results = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert_in_range(results[b], f"long_duration/{b}")
