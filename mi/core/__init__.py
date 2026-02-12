"""MI Core — Infrastructure, constants, types, and base classes."""

from .constants import (
    SAMPLE_RATE,
    HOP_LENGTH,
    FRAME_RATE,
    N_MELS,
    R3_DIM,
    N_HORIZONS,
    N_MORPHS,
    N_LAWS,
    H3_TOTAL_DIM,
    HORIZON_FRAMES,
    MORPH_NAMES,
    LAW_NAMES,
    BETA_NACC,
    BETA_CAUDATE,
    h3_flat_index,
)
from .config import MIConfig, MI_CONFIG
from .types import (
    CochleaOutput,
    R3Output,
    H3Output,
    EarOutput,
    SemanticGroupOutput,
    L3Output,
    MIOutput,
)
from .base import (
    BaseSpectralGroup,
    BaseSemanticGroup,
)
from .registry import DemandAggregator

__all__ = [
    # Constants
    "SAMPLE_RATE", "HOP_LENGTH", "FRAME_RATE", "N_MELS", "R3_DIM",
    "N_HORIZONS", "N_MORPHS", "N_LAWS", "H3_TOTAL_DIM",
    "HORIZON_FRAMES", "MORPH_NAMES", "LAW_NAMES",
    "BETA_NACC", "BETA_CAUDATE",
    "h3_flat_index",
    # Config
    "MIConfig", "MI_CONFIG",
    # Types
    "CochleaOutput", "R3Output", "H3Output", "EarOutput",
    "SemanticGroupOutput", "L3Output", "MIOutput",
    # Base classes
    "BaseSpectralGroup", "BaseSemanticGroup",
    # Registry
    "DemandAggregator",
]
