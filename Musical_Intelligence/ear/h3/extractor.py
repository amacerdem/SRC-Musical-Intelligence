"""H3Extractor -- Orchestrates sparse temporal morphology extraction.

Given an R3 spectral tensor and a set of demanded 4-tuples, computes
only the requested temporal morph features using the 7-phase execution
pipeline.

Usage
-----
::

    extractor = H3Extractor()
    h3_output = extractor.extract(r3_tensor, demand)
    # h3_output.features: Dict[(r3_idx, horizon, morph, law)] -> (B, T)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Tuple

from torch import Tensor

from .demand.demand_tree import DemandTree
from .pipeline.executor import H3Executor
from .pipeline.warmup import WarmUpHandler


# ======================================================================
# H3Output
# ======================================================================

@dataclass(frozen=True)
class H3Output:
    """Immutable output of the H3 temporal extractor.

    Attributes:
        features: Sparse dictionary mapping each demanded 4-tuple
            ``(r3_idx, horizon, morph, law)`` to a ``(B, T)`` tensor
            with values in ``[0, 1]``.
        n_tuples: Number of demanded tuples that were computed.
    """

    features: Dict[Tuple[int, int, int, int], Tensor]
    n_tuples: int


# ======================================================================
# H3Extractor
# ======================================================================

class H3Extractor:
    """Orchestrates sparse temporal morphology extraction.

    The extractor wraps the ``H3Executor`` and ``DemandTree`` to
    provide a clean API for computing temporal morph features on demand.

    On ``extract(r3, demand)``:

    1. Build demand tree (group 4-tuples by horizon).
    2. Execute 7-phase pipeline via ``H3Executor``.
    3. Return sparse ``H3Output``.
    """

    def __init__(self) -> None:
        self._executor = H3Executor()
        self._warmup = WarmUpHandler()

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------

    def extract(
        self,
        r3: Tensor,
        demand: Set[Tuple[int, int, int, int]],
    ) -> H3Output:
        """Extract temporal morph features for the demanded tuples.

        Parameters
        ----------
        r3 : Tensor
            Shape ``(B, T, 97)`` R3 spectral feature tensor.
            All values should be in ``[0, 1]``.
        demand : set
            Set of 4-tuples ``(r3_idx, horizon, morph, law)``
            specifying which temporal features to compute.

        Returns
        -------
        H3Output
            Frozen dataclass with:
            - ``features``: dict mapping each 4-tuple to ``(B, T)``
            - ``n_tuples``: number of tuples computed
        """
        if not demand:
            return H3Output(features={}, n_tuples=0)

        # 1. Build demand tree (group by horizon)
        demand_tree = DemandTree.build(demand)

        # 2. Execute 7-phase pipeline
        results = self._executor.execute(r3, demand_tree)

        return H3Output(features=results, n_tuples=len(results))

    # ------------------------------------------------------------------
    # Warmup info
    # ------------------------------------------------------------------

    @property
    def warmup_handler(self) -> WarmUpHandler:
        """Access the warm-up handler for edge analysis."""
        return self._warmup

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return "H3Extractor()"
