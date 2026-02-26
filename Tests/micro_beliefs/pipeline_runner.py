"""MicroBeliefRunner — full R³→H³→C³ pipeline for micro-belief tests.

Initialises all extractors and mechanisms once (expensive ~5-10s),
then provides a fast ``run(audio, target_beliefs)`` method that returns
per-belief time-series tensors.

Usage::

    runner = MicroBeliefRunner()
    results = runner.run(audio_waveform, ["harmonic_stability", "interval_quality"])
    # results["harmonic_stability"]  →  (1, T) tensor
"""
from __future__ import annotations

import importlib
import pathlib
import sys
from typing import Any, Dict, List, Set, Tuple

import torch
import torchaudio
from torch import Tensor

# ── Constants ────────────────────────────────────────────────────────
SAMPLE_RATE = 44_100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")

_ROLE_TO_DEPTH = {
    "relay": 0,
    "encoder": 1,
    "associator": 2,
    "integrator": 3,
    "hub": 4,
}


# ── Collection helpers ───────────────────────────────────────────────

def _collect_mechanism_instances() -> List[Any]:
    """Auto-discover all mechanism instances from F1-F9."""
    from Musical_Intelligence.contracts.bases.nucleus import _NucleusBase

    instances: List[Any] = []
    for fn in _FUNCTION_IDS:
        mod_path = f"Musical_Intelligence.brain.functions.{fn}.mechanisms"
        try:
            mod = importlib.import_module(mod_path)
            for name in getattr(mod, "__all__", []):
                cls = getattr(mod, name, None)
                if cls is None:
                    continue
                try:
                    if isinstance(cls, type) and issubclass(cls, _NucleusBase):
                        instances.append(cls())
                except Exception:
                    continue
        except Exception:
            pkg_dir = (
                _PROJECT_ROOT
                / "Musical_Intelligence"
                / "brain"
                / "functions"
                / fn
                / "mechanisms"
            )
            if not pkg_dir.is_dir():
                continue
            for sub in sorted(pkg_dir.iterdir()):
                if not sub.is_dir() or sub.name.startswith(("_", ".")):
                    continue
                sub_mod_path = f"{mod_path}.{sub.name}"
                try:
                    sub_mod = importlib.import_module(sub_mod_path)
                except Exception:
                    continue
                for attr_name in dir(sub_mod):
                    attr = getattr(sub_mod, attr_name, None)
                    if attr is None:
                        continue
                    try:
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, _NucleusBase)
                            and attr is not _NucleusBase
                            and not attr_name.startswith("_")
                        ):
                            instances.append(attr())
                    except Exception:
                        continue
    return instances


def _collect_belief_instances() -> List[Any]:
    """Auto-discover all belief instances from F1-F9."""
    from Musical_Intelligence.contracts.bases.belief import _BeliefBase

    instances: List[Any] = []
    for fn in _FUNCTION_IDS:
        mod_path = f"Musical_Intelligence.brain.functions.{fn}.beliefs"
        try:
            mod = importlib.import_module(mod_path)
            for name in getattr(mod, "__all__", []):
                cls = getattr(mod, name, None)
                if cls is None:
                    continue
                try:
                    if isinstance(cls, type) and issubclass(cls, _BeliefBase):
                        instances.append(cls())
                except Exception:
                    continue
        except Exception:
            pkg_dir = (
                _PROJECT_ROOT
                / "Musical_Intelligence"
                / "brain"
                / "functions"
                / fn
                / "beliefs"
            )
            if not pkg_dir.is_dir():
                continue
            for sub in sorted(pkg_dir.iterdir()):
                if not sub.is_dir() or sub.name.startswith(("_", ".")):
                    continue
                sub_mod_path = f"{mod_path}.{sub.name}"
                try:
                    sub_mod = importlib.import_module(sub_mod_path)
                except Exception:
                    continue
                for attr_name in dir(sub_mod):
                    attr = getattr(sub_mod, attr_name, None)
                    if attr is None:
                        continue
                    try:
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, _BeliefBase)
                            and attr is not _BeliefBase
                            and not attr_name.startswith("_")
                        ):
                            instances.append(attr())
                    except Exception:
                        continue
    return instances


def _fix_processing_depths(nuclei: List[Any]) -> None:
    """Ensure PROCESSING_DEPTH matches the mechanism's ROLE."""
    for n in nuclei:
        role = getattr(n, "ROLE", "relay")
        min_depth = _ROLE_TO_DEPTH.get(role, 0)
        if n.PROCESSING_DEPTH < min_depth:
            n.PROCESSING_DEPTH = min_depth


# ── Pipeline runner ──────────────────────────────────────────────────

class MicroBeliefRunner:
    """Session-scoped pipeline runner for micro-belief tests."""

    def __init__(self) -> None:
        from Musical_Intelligence.ear.r3 import R3Extractor
        from Musical_Intelligence.ear.h3 import H3Extractor

        self.r3_extractor = R3Extractor()
        self.h3_extractor = H3Extractor()

        self.nuclei = _collect_mechanism_instances()
        _fix_processing_depths(self.nuclei)

        self._beliefs_by_name: Dict[str, Any] = {}
        for b in _collect_belief_instances():
            self._beliefs_by_name[b.NAME] = b

        # Full H³ demand set (union across all mechanisms)
        self.h3_demands: Set[Tuple[int, int, int, int]] = set()
        for m in self.nuclei:
            for spec in m.h3_demand:
                self.h3_demands.add(spec.as_tuple())

        # Mechanism name lookup
        self._mech_by_name: Dict[str, Any] = {
            m.NAME: m for m in self.nuclei
        }

        self._mel_transform = torchaudio.transforms.MelSpectrogram(
            sample_rate=SAMPLE_RATE,
            n_fft=N_FFT,
            hop_length=HOP_LENGTH,
            n_mels=N_MELS,
            power=2.0,
        )

    # ── Public API ───────────────────────────────────────────────────

    def audio_to_mel(self, waveform: Tensor) -> Tensor:
        """Convert ``(1, N)`` waveform to ``(1, 128, T)`` log-mel spectrogram."""
        mel = self._mel_transform(waveform)  # (1, 128, T)
        mel = torch.log1p(mel)
        mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
        return mel / mel_max

    def run(
        self,
        audio: Tensor,
        target_beliefs: list[str] | None = None,
    ) -> Dict[str, Tensor]:
        """Run full pipeline and return belief time-series.

        Args:
            audio: ``(1, N)`` waveform at 44100 Hz.
            target_beliefs: List of belief NAMEs to return.
                If ``None``, returns all 131 beliefs.

        Returns:
            Dict mapping belief NAME → ``(1, T)`` tensor.
        """
        from Musical_Intelligence.brain.executor import execute

        with torch.no_grad():
            mel = self.audio_to_mel(audio)
            r3_out = self.r3_extractor.extract(mel, audio=audio, sr=SAMPLE_RATE)
            r3_features = r3_out.features  # (1, T, 97)
            h3_out = self.h3_extractor.extract(r3_features, self.h3_demands)
            outputs, _ram, _neuro = execute(
                self.nuclei, h3_out.features, r3_features,
            )

        # Extract belief observations
        if target_beliefs is None:
            target_beliefs = list(self._beliefs_by_name.keys())

        results: Dict[str, Tensor] = {}
        for name in target_beliefs:
            belief = self._beliefs_by_name[name]
            mech_name = belief.MECHANISM
            if mech_name not in outputs:
                continue
            mech_output = outputs[mech_name]  # (1, T, D)
            results[name] = belief.observe(mech_output)  # (1, T)

        return results

    @property
    def belief_names(self) -> list[str]:
        """All available belief names."""
        return sorted(self._beliefs_by_name.keys())

    @property
    def mechanism_names(self) -> list[str]:
        """All available mechanism names."""
        return sorted(self._mech_by_name.keys())
