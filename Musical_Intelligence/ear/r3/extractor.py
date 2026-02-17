"""R3Extractor -- Orchestrates 97-D spectral feature extraction.

Auto-discovers all 9 spectral groups (A through K (excluding dissolved E and I)), registers them
into an R3FeatureRegistry, freezes index assignments, then executes
the 3-stage DAG pipeline to produce a dense (B, T, 97) R3 tensor.

Usage
-----
::

    extractor = R3Extractor()
    r3_output = extractor.extract(mel)
    # r3_output.features: (B, T, 97) in [0, 1]
    # r3_output.feature_names: tuple of 97 strings
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import torch
from torch import Tensor

from .pipeline.dag import DependencyDAG
from .pipeline.normalization import FeatureNormalizer
from .pipeline.stage_executor import StageExecutor
from .pipeline.warmup import WarmupManager
from .registry.auto_discovery import auto_discover_groups
from .registry.feature_map import R3FeatureMap
from .registry.feature_registry import R3FeatureRegistry


# ======================================================================
# R3Output
# ======================================================================

@dataclass(frozen=True)
class R3Output:
    """Immutable output of the R3 spectral extractor.

    Attributes:
        features:      ``(B, T, 97)`` tensor with all values in ``[0, 1]``.
        feature_names: Ordered tuple of 97 feature name strings.
        feature_map:   Frozen registry snapshot with group metadata.
    """

    features: Tensor
    feature_names: Tuple[str, ...]
    feature_map: R3FeatureMap


# ======================================================================
# R3Extractor
# ======================================================================

class R3Extractor:
    """Orchestrates all R3 spectral groups into a 97-D feature vector.

    On construction, the extractor:

    1. Auto-discovers all ``BaseSpectralGroup`` subclasses from
       ``ear/r3/groups/{a_consonance..k_modulation}/``.
    2. Registers them into an ``R3FeatureRegistry`` and freezes index
       assignments.
    3. Initialises the 2-stage ``DependencyDAG``, ``StageExecutor``,
       ``FeatureNormalizer``, and ``WarmupManager``.

    On ``extract(mel)``, it runs the full pipeline:

    1. Execute groups in DAG order → per-group ``(B, T, dim)`` tensors.
    2. Normalize each group's output (safety clamp to ``[0, 1]``).
    3. Concatenate to produce ``(B, T, 97)`` dense R3 vector.
    """

    def __init__(self) -> None:
        # 1. Auto-discover and register groups
        self._registry = R3FeatureRegistry()
        discovered = auto_discover_groups()

        if not discovered:
            raise RuntimeError(
                "R3Extractor: auto_discover_groups() returned no groups. "
                "Ensure ear/r3/groups/ contains valid BaseSpectralGroup "
                "subclasses."
            )

        # Register in canonical index order (A-K, sorted by INDEX_RANGE)
        for group in discovered:
            self._registry.register(group)

        # 2. Freeze → assign contiguous INDEX_RANGE per group
        self._feature_map = self._registry.freeze()

        # Build groups dict keyed by GROUP_NAME
        self._groups: Dict[str, object] = {
            g.GROUP_NAME: g for g in discovered
        }

        # 3. Initialise pipeline components
        self._dag = DependencyDAG()
        self._dag.validate()
        self._executor = StageExecutor()
        self._normalizer = FeatureNormalizer()
        self._warmup = WarmupManager()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def feature_map(self) -> R3FeatureMap:
        """Frozen registry snapshot with group metadata."""
        return self._feature_map

    @property
    def feature_names(self) -> Tuple[str, ...]:
        """Ordered tuple of 97 feature name strings."""
        return self._feature_map.feature_names

    @property
    def total_dim(self) -> int:
        """Total feature dimensionality (97)."""
        return self._feature_map.total_dim

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------

    @torch.no_grad()
    def extract(
        self,
        mel: Tensor,
        *,
        audio: Tensor | None = None,
        sr: int = 44100,
    ) -> R3Output:
        """Extract 97-D R3 spectral features from a mel spectrogram.

        Parameters
        ----------
        mel : Tensor
            Shape ``(B, 97, T)`` log-mel spectrogram (log1p normalised).
            Frame rate 172.27 Hz (sr=44100, hop_length=256).
        audio : Tensor, optional
            Shape ``(B, N_SAMPLES)`` raw waveform at *sr* Hz.  When
            provided, groups that override ``compute_from_audio()``
            (e.g. ConsonanceGroup) use it for real psychoacoustic
            computation instead of mel-based proxies.
        sr : int
            Sample rate in Hz (default 44100).

        Returns
        -------
        R3Output
            Frozen dataclass with:
            - ``features``: ``(B, T, 97)`` tensor, all values in ``[0, 1]``
            - ``feature_names``: tuple of 97 strings
            - ``feature_map``: frozen R3FeatureMap
        """
        B, N, T = mel.shape

        # 1. Execute all groups in DAG order
        group_outputs = self._executor.execute(
            mel, self._groups, self._dag, audio=audio, sr=sr,
        )

        # 2. Normalize each group's output (safety clamp)
        group_outputs = self._normalizer.normalize_all(group_outputs)

        # 3. Concatenate in index order to produce (B, T, 97)
        ordered_tensors = []
        for group_info in self._feature_map.groups:
            tensor = group_outputs[group_info.name]
            ordered_tensors.append(tensor)

        features = torch.cat(ordered_tensors, dim=-1)  # (B, T, 97)

        return R3Output(
            features=features,
            feature_names=self.feature_names,
            feature_map=self._feature_map,
        )

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"R3Extractor(groups={len(self._groups)}, "
            f"dim={self.total_dim})"
        )
