"""BaseSpectralGroup -- Abstract Base Class for R3 spectral feature groups.

Each subclass computes a contiguous slice of the R3 feature vector from the
mel spectrogram. The current v1 architecture defines 5 groups (A-E) producing
49 features; the v2 architecture (Phase 6) extends to 11 groups (A-K)
producing 128 features.

Groups are organized in a 3-stage DAG:

    Stage 1: Independent groups (compute from mel only)
    Stage 2: Groups depending on Stage 1 outputs
    Stage 3: Groups depending on Stage 1 + Stage 2 outputs

Current groups (v1):

    A  consonance        psychoacoustic   7D   [0:7]
    B  energy            energetic        5D   [7:12]
    C  timbre            timbral          9D   [12:21]
    D  change            temporal         4D   [21:25]
    E  interactions      cross_domain     24D  [25:49]
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from torch import Tensor


class BaseSpectralGroup(ABC):
    """Abstract base class for R3 spectral feature groups.

    Each subclass computes a contiguous slice of the R3 feature vector
    from the mel spectrogram.

    Class Constants (must override in every subclass):
        GROUP_NAME:   Canonical group name (e.g. ``"consonance"``,
                      ``"energy"``). Must be non-empty and unique across all
                      registered groups.
        DOMAIN:       Perceptual domain: ``"psychoacoustic"``,
                      ``"energetic"``, ``"timbral"``, ``"temporal"``,
                      ``"cross_domain"``, or Phase 6 additions.
        OUTPUT_DIM:   Number of features this group produces. Must be > 0.
        INDEX_RANGE:  Half-open interval ``[start, end)`` in the R3 vector.
                      ``end - start`` MUST equal ``OUTPUT_DIM``.
        STAGE:        Computation stage in the 3-stage DAG (1, 2, or 3).
                      Stage 1 groups compute from mel only; Stage 2-3 groups
                      depend on outputs from earlier stages.
        DEPENDENCIES: Tuple of group names this group depends on. Empty for
                      Stage 1 groups.
    """

    # ------------------------------------------------------------------
    # Class constants -- override in every subclass
    # ------------------------------------------------------------------

    GROUP_NAME: str = ""
    DOMAIN: str = ""
    OUTPUT_DIM: int = 0
    INDEX_RANGE: Tuple[int, int] = (0, 0)
    STAGE: int = 1
    DEPENDENCIES: Tuple[str, ...] = ()

    # ------------------------------------------------------------------
    # Abstract members
    # ------------------------------------------------------------------

    @abstractmethod
    def compute(self, mel: Tensor) -> Tensor:
        """Compute spectral features from the mel spectrogram.

        This is the primary compute method for Stage 1 groups. Stage 2-3
        groups should also implement ``compute_with_deps()``.

        Args:
            mel: ``(B, N_MELS, T)`` log-mel spectrogram (log1p normalised).
                ``N_MELS`` = 128, frame rate 172.27 Hz
                (sr=44100, hop_length=256).

        Returns:
            ``(B, T, OUTPUT_DIM)`` spectral features for this group.
            Values should be in ``[0, 1]`` unless the feature has a natural
            signed range (documented in ``feature_names``).
        """

    def compute_with_deps(
        self,
        mel: Tensor,
        deps: Dict[str, Tensor],
    ) -> Tensor:
        """Compute spectral features with access to dependent group outputs.

        Override this for Stage 2-3 groups that depend on other group outputs.
        Default implementation falls back to ``compute(mel)``.

        Args:
            mel: ``(B, N_MELS, T)`` log-mel spectrogram.
            deps: Dict mapping ``GROUP_NAME`` to ``(B, T, dim)`` tensors
                from previously computed groups. Only groups declared in
                ``DEPENDENCIES`` are guaranteed present.

        Returns:
            ``(B, T, OUTPUT_DIM)`` spectral features.
        """
        return self.compute(mel)

    def compute_from_audio(
        self,
        mel: Tensor,
        audio: Tensor,
        sr: int = 44100,
    ) -> Tensor | None:
        """Compute spectral features with access to raw audio waveform.

        Override this for groups that need raw audio (e.g. psychoacoustic
        consonance models requiring STFT peak picking).  Return ``None``
        to fall back to ``compute(mel)``.

        Args:
            mel:   ``(B, N_MELS, T)`` log-mel spectrogram.
            audio: ``(B, N_SAMPLES)`` raw waveform at *sr* Hz.
            sr:    Sample rate in Hz (default 44100).

        Returns:
            ``(B, T, OUTPUT_DIM)`` spectral features, or ``None`` to
            indicate fallback to mel-only computation.
        """
        return None

    @property
    @abstractmethod
    def feature_names(self) -> Tuple[str, ...]:
        """Ordered names of each output dimension.

        ``len(feature_names)`` MUST equal ``OUTPUT_DIM``.
        Names follow ``snake_case`` convention (e.g. ``"stumpf_fusion"``).
        Names must be unique across all groups.

        Returns:
            Tuple of feature name strings.
        """

    # ------------------------------------------------------------------
    # Computed helpers
    # ------------------------------------------------------------------

    @property
    def start_index(self) -> int:
        """Start index in the R3 vector (inclusive)."""
        return self.INDEX_RANGE[0]

    @property
    def end_index(self) -> int:
        """End index in the R3 vector (exclusive)."""
        return self.INDEX_RANGE[1]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).

        Checks:
            1. ``GROUP_NAME`` is non-empty.
            2. ``OUTPUT_DIM`` is positive.
            3. ``INDEX_RANGE`` span matches ``OUTPUT_DIM``.
            4. ``feature_names`` length matches ``OUTPUT_DIM``.
            5. ``STAGE`` is in {1, 2, 3}.
            6. ``DEPENDENCIES`` is empty for Stage 1 groups.
        """
        errors: list[str] = []

        # 1. GROUP_NAME non-empty
        if not self.GROUP_NAME:
            errors.append("GROUP_NAME must be non-empty")

        # 2. OUTPUT_DIM > 0
        if self.OUTPUT_DIM <= 0:
            errors.append(
                f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}"
            )

        # 3. INDEX_RANGE span matches OUTPUT_DIM
        start, end = self.INDEX_RANGE
        if end - start != self.OUTPUT_DIM:
            errors.append(
                f"INDEX_RANGE [{start}:{end}] span ({end - start}) "
                f"!= OUTPUT_DIM ({self.OUTPUT_DIM})"
            )

        # 4. feature_names length matches OUTPUT_DIM
        try:
            names = self.feature_names
            if len(names) != self.OUTPUT_DIM:
                errors.append(
                    f"feature_names has {len(names)} entries, "
                    f"expected {self.OUTPUT_DIM}"
                )
        except NotImplementedError:
            pass  # feature_names not yet implemented in subclass

        # 5. STAGE in {1, 2, 3}
        if self.STAGE not in (1, 2, 3):
            errors.append(
                f"STAGE must be 1, 2, or 3, got {self.STAGE}"
            )

        # 6. DEPENDENCIES must be empty for Stage 1
        if self.STAGE == 1 and self.DEPENDENCIES:
            errors.append(
                f"Stage 1 group must have empty DEPENDENCIES, "
                f"got {self.DEPENDENCIES!r}"
            )

        return errors

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"group={self.GROUP_NAME!r}, "
            f"domain={self.DOMAIN!r}, "
            f"dim={self.OUTPUT_DIM}, "
            f"range=[{self.INDEX_RANGE[0]}:{self.INDEX_RANGE[1]}], "
            f"stage={self.STAGE})"
        )
