"""
BaseSpectralGroup -- Abstract base class for R3 spectral feature groups.

R3 computes 49 spectral features per frame, organised into 5 groups:

    Group A  -- Consonance     (7D)   [0:7]    Plomp-Levelt, Stumpf, etc.
    Group B  -- Energy         (5D)   [7:12]   Loudness, amplitude, onsets
    Group C  -- Timbre         (9D)   [12:21]  Warmth, brightness, tristimulus
    Group D  -- Change         (4D)   [21:25]  Spectral flux, novelty
    Group E  -- Interactions   (24D)  [25:49]  Cross-domain products

Each group is implemented as a BaseSpectralGroup subclass.  The group reads
the mel spectrogram and produces its slice of the R3 vector.  The R3
pipeline collects all groups and concatenates their outputs.

The DOMAIN attribute indicates what perceptual domain the group operates in.
INDEX_RANGE defines the half-open interval [start, end) in the 49-D vector.

This ABC is structurally compatible with the mi (v2) BaseSpectralGroup but
adds DOMAIN metadata and stronger validation for the mi_beta architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from torch import Tensor


class BaseSpectralGroup(ABC):
    """Abstract base class for R3 spectral feature groups.

    Each subclass computes a contiguous slice of the 49-D R3 feature vector
    from the mel spectrogram.
    """

    # ═══════════════════════════════════════════════════════════════════
    # CLASS CONSTANTS — override in every subclass
    # ═══════════════════════════════════════════════════════════════════

    GROUP_NAME: str = ""
    """Canonical group name (e.g. "consonance", "energy", "timbre")."""

    DOMAIN: str = ""
    """Perceptual domain this group covers.  One of:
    "psychoacoustic", "energetic", "timbral", "temporal", "cross_domain"."""

    OUTPUT_DIM: int = 0
    """Number of features this group produces."""

    INDEX_RANGE: Tuple[int, int] = (0, 0)
    """Half-open interval [start, end) in the 49-D R3 vector.
    end - start MUST equal OUTPUT_DIM."""

    # ═══════════════════════════════════════════════════════════════════
    # ABSTRACT MEMBERS
    # ═══════════════════════════════════════════════════════════════════

    @abstractmethod
    def compute(self, mel: Tensor) -> Tensor:
        """Compute spectral features from the mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram (log1p normalised).

        Returns:
            (B, T, OUTPUT_DIM) spectral features for this group.
            Values should be in [0, 1] unless the feature has a natural
            signed range (documented in feature_names).
        """

    @property
    @abstractmethod
    def feature_names(self) -> List[str]:
        """Ordered names of each output dimension.

        len(feature_names) MUST equal OUTPUT_DIM.
        Names follow snake_case convention (e.g. "stumpf_fusion").
        """

    # ═══════════════════════════════════════════════════════════════════
    # COMPUTED HELPERS
    # ═══════════════════════════════════════════════════════════════════

    @property
    def start_index(self) -> int:
        """Start index in the R3 vector (inclusive)."""
        return self.INDEX_RANGE[0]

    @property
    def end_index(self) -> int:
        """End index in the R3 vector (exclusive)."""
        return self.INDEX_RANGE[1]

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).
        """
        errors: list[str] = []

        if not self.GROUP_NAME:
            errors.append("GROUP_NAME must be non-empty")
        if self.OUTPUT_DIM <= 0:
            errors.append(f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}")

        start, end = self.INDEX_RANGE
        if end - start != self.OUTPUT_DIM:
            errors.append(
                f"INDEX_RANGE [{start}:{end}] span ({end - start}) "
                f"!= OUTPUT_DIM ({self.OUTPUT_DIM})"
            )

        try:
            names = self.feature_names
            if len(names) != self.OUTPUT_DIM:
                errors.append(
                    f"feature_names has {len(names)} entries, "
                    f"expected {self.OUTPUT_DIM}"
                )
        except NotImplementedError:
            pass

        return errors

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"group={self.GROUP_NAME!r}, "
            f"domain={self.DOMAIN!r}, "
            f"dim={self.OUTPUT_DIM}, "
            f"range=[{self.INDEX_RANGE[0]}:{self.INDEX_RANGE[1]}])"
        )
