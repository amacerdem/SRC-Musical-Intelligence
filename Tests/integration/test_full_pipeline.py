"""Full end-to-end integration tests for the MI pipeline.

Pipeline stages: Audio (WAV) -> Cochlea (mel) -> R3 (97D) -> H3 (sparse) -> Brain C3 (1006D)

Tests include:
- Synthetic mel test (fast, no audio dependency)
- Swan Lake real-audio test (slow, marked @pytest.mark.slow)

Run with::

    pytest Tests/integration/test_full_pipeline.py -v
    pytest Tests/integration/test_full_pipeline.py -v -m slow    # slow tests only
    pytest Tests/integration/test_full_pipeline.py -v -m "not slow"  # skip slow
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root on sys.path
# ---------------------------------------------------------------------------
_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import numpy as np
import pytest
import torch

from Musical_Intelligence.ear import R3Extractor, H3Extractor
from Musical_Intelligence.brain import BrainOrchestrator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
EXPECTED_R3_DIM = 97
EXPECTED_BRAIN_DIM = 1006

SWAN_LAKE = (
    "Test-Audio/Swan Lake Suite, Op. 20a_ I. Scene "
    "_Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav"
)
SWAN_LAKE_PATH = Path(_PROJECT_ROOT) / SWAN_LAKE


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture(scope="module")
def r3_extractor() -> R3Extractor:
    return R3Extractor()


@pytest.fixture(scope="module")
def h3_extractor() -> H3Extractor:
    return H3Extractor()


@pytest.fixture(scope="module")
def brain() -> BrainOrchestrator:
    return BrainOrchestrator()


def _collect_brain_demand(brain: BrainOrchestrator) -> set:
    """Collect the full H3 demand set from all brain mechanisms and units."""
    demand = brain._mechanism_runner.h3_demand
    for unit in brain._units.values():
        demand |= unit.h3_demand
    return demand


# ======================================================================
# Test: Synthetic full pipeline
# ======================================================================

class TestFullPipelineSynthetic:
    """Full pipeline with synthetic mel input (T=200)."""

    def test_full_pipeline_synthetic(
        self,
        r3_extractor: R3Extractor,
        h3_extractor: H3Extractor,
        brain: BrainOrchestrator,
    ) -> None:
        """mel -> R3 -> H3 -> Brain produces (1, T, 1006) in [0, 1]."""
        B, T_mel = 1, 200
        gen = torch.Generator().manual_seed(42)
        mel = torch.rand(B, 128, T_mel, generator=gen)

        # ---- Stage 1: R3 extraction ----
        t0 = time.perf_counter()
        r3_out = r3_extractor.extract(mel)
        t_r3 = time.perf_counter() - t0

        r3_tensor = r3_out.features
        assert r3_tensor.shape[0] == B
        assert r3_tensor.shape[2] == EXPECTED_R3_DIM
        T = r3_tensor.shape[1]  # R3 may adjust T
        print(f"\n  R3: {r3_tensor.shape}  ({t_r3:.3f}s)")

        # ---- Stage 2: H3 extraction ----
        demand = _collect_brain_demand(brain)
        t0 = time.perf_counter()
        h3_out = h3_extractor.extract(r3_tensor, demand)
        t_h3 = time.perf_counter() - t0

        assert h3_out.n_tuples == len(demand), (
            f"H3 returned {h3_out.n_tuples} tuples, "
            f"expected {len(demand)}"
        )
        print(f"  H3: {h3_out.n_tuples} tuples  ({t_h3:.3f}s)")

        # ---- Stage 3: Brain forward ----
        t0 = time.perf_counter()
        brain_out = brain.forward(h3_out.features, r3_tensor)
        t_brain = time.perf_counter() - t0

        output = brain_out.tensor
        assert output.shape == (B, T, EXPECTED_BRAIN_DIM), (
            f"Brain output shape {output.shape} != "
            f"expected ({B}, {T}, {EXPECTED_BRAIN_DIM})"
        )
        assert output.min() >= 0.0, (
            f"Brain output min={output.min().item():.6f} < 0"
        )
        assert output.max() <= 1.0, (
            f"Brain output max={output.max().item():.6f} > 1"
        )
        print(f"  Brain: {output.shape}  ({t_brain:.3f}s)")
        print(f"  Total: {t_r3 + t_h3 + t_brain:.3f}s")


# ======================================================================
# Test: Swan Lake real-audio pipeline
# ======================================================================

class TestFullPipelineSwanLake:
    """Full pipeline with Swan Lake audio (real WAV, ~30s)."""

    @pytest.mark.slow
    def test_full_pipeline_swan_lake(
        self,
        r3_extractor: R3Extractor,
        h3_extractor: H3Extractor,
        brain: BrainOrchestrator,
    ) -> None:
        """Load Swan Lake WAV, compute mel, run full pipeline.

        Verifies final output shape (1, T, 1006) and value range [0, 1].
        Prints per-stage timing for performance monitoring.
        """
        import librosa

        if not SWAN_LAKE_PATH.exists():
            pytest.skip(
                f"Swan Lake audio not found at {SWAN_LAKE_PATH}. "
                f"Place the WAV file in Test-Audio/ to run this test."
            )

        # ---- Load audio (30 seconds) ----
        t0 = time.perf_counter()
        y, sr = librosa.load(str(SWAN_LAKE_PATH), sr=44100, duration=30.0)
        t_load = time.perf_counter() - t0
        print(f"\n  Load: {len(y)} samples @ {sr} Hz ({t_load:.3f}s)")

        # ---- Cochlea: mel spectrogram ----
        t0 = time.perf_counter()
        mel_np = librosa.feature.melspectrogram(
            y=y, sr=sr, n_fft=2048, hop_length=256, n_mels=128,
        )
        mel_np = np.log1p(mel_np)
        # Normalize to [0, 1]
        mel_max = mel_np.max()
        if mel_max > 0:
            mel_np = mel_np / mel_max
        mel = torch.from_numpy(mel_np).unsqueeze(0).float()  # (1, 128, T)
        t_mel = time.perf_counter() - t0
        print(f"  Cochlea: {mel.shape}  ({t_mel:.3f}s)")

        # ---- Stage 1: R3 ----
        t0 = time.perf_counter()
        r3_out = r3_extractor.extract(mel)
        t_r3 = time.perf_counter() - t0

        r3_tensor = r3_out.features
        B, T, D = r3_tensor.shape
        assert B == 1
        assert D == EXPECTED_R3_DIM
        print(f"  R3: {r3_tensor.shape}  ({t_r3:.3f}s)")

        # ---- Stage 2: H3 ----
        demand = _collect_brain_demand(brain)
        t0 = time.perf_counter()
        h3_out = h3_extractor.extract(r3_tensor, demand)
        t_h3 = time.perf_counter() - t0
        print(f"  H3: {h3_out.n_tuples} tuples  ({t_h3:.3f}s)")

        # ---- Stage 3: Brain ----
        t0 = time.perf_counter()
        brain_out = brain.forward(h3_out.features, r3_tensor)
        t_brain = time.perf_counter() - t0

        output = brain_out.tensor
        assert output.shape == (1, T, EXPECTED_BRAIN_DIM), (
            f"Brain output shape {output.shape} != "
            f"expected (1, {T}, {EXPECTED_BRAIN_DIM})"
        )
        assert output.min() >= 0.0, (
            f"Brain output min={output.min().item():.6f} < 0"
        )
        assert output.max() <= 1.0, (
            f"Brain output max={output.max().item():.6f} > 1"
        )
        print(f"  Brain: {output.shape}  ({t_brain:.3f}s)")

        total = t_load + t_mel + t_r3 + t_h3 + t_brain
        print(f"  ---")
        print(f"  Total: {total:.3f}s")
        print(f"  Throughput: {T / (t_r3 + t_h3 + t_brain):.0f} frames/s")
