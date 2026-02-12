"""MI-Beta Core -- Infrastructure, constants, types, registry, and assembly."""

from .config import MIBetaConfig, MI_BETA_CONFIG
from .constants import (
    # Audio
    SAMPLE_RATE,
    HOP_LENGTH,
    FRAME_RATE,
    FRAME_DURATION_MS,
    N_FFT,
    N_MELS,
    # R3
    R3_DIM,
    R3_CONSONANCE,
    R3_ENERGY,
    R3_TIMBRE,
    R3_CHANGE,
    R3_INTERACTIONS,
    # H3
    N_HORIZONS,
    N_MORPHS,
    N_LAWS,
    H3_TOTAL_DIM,
    HORIZON_MS,
    HORIZON_FRAMES,
    ATTENTION_DECAY,
    MORPH_NAMES,
    LAW_NAMES,
    MORPH_SCALE,
    # Neuroscience
    BETA_NACC,
    BETA_CAUDATE,
    CIRCUIT_NAMES,
    # Helpers
    h3_flat_index,
    scale_h3_value,
    # mi_beta extensions
    MECHANISM_DIM,
    UNIT_EXECUTION_ORDER,
    ALL_UNIT_NAMES,
    MODEL_TIERS,
    CIRCUITS,
    N_CIRCUITS,
)
from .types import (
    # Ear
    CochleaOutput,
    R3Output,
    H3Output,
    EarOutput,
    # Brain
    ModelOutput,
    UnitOutput,
    BrainOutput,
    # Language
    SemanticGroupOutput,
    L3Output,
    # Pipeline
    MIBetaOutput,
)
from .registry import ModelRegistry
from .demand_aggregator import DemandAggregator
from .space_assembler import SpaceAssembler, SpaceLayout
from .dimension_map import DimensionMap

__all__ = [
    # Config
    "MIBetaConfig", "MI_BETA_CONFIG",
    # Constants - Audio
    "SAMPLE_RATE", "HOP_LENGTH", "FRAME_RATE", "FRAME_DURATION_MS",
    "N_FFT", "N_MELS",
    # Constants - R3
    "R3_DIM", "R3_CONSONANCE", "R3_ENERGY", "R3_TIMBRE",
    "R3_CHANGE", "R3_INTERACTIONS",
    # Constants - H3
    "N_HORIZONS", "N_MORPHS", "N_LAWS", "H3_TOTAL_DIM",
    "HORIZON_MS", "HORIZON_FRAMES", "ATTENTION_DECAY",
    "MORPH_NAMES", "LAW_NAMES", "MORPH_SCALE",
    # Constants - Neuroscience
    "BETA_NACC", "BETA_CAUDATE", "CIRCUIT_NAMES",
    # Constants - Helpers
    "h3_flat_index", "scale_h3_value",
    # Constants - mi_beta extensions
    "MECHANISM_DIM", "UNIT_EXECUTION_ORDER", "ALL_UNIT_NAMES",
    "MODEL_TIERS", "CIRCUITS", "N_CIRCUITS",
    # Types - Ear
    "CochleaOutput", "R3Output", "H3Output", "EarOutput",
    # Types - Brain
    "ModelOutput", "UnitOutput", "BrainOutput",
    # Types - Language
    "SemanticGroupOutput", "L3Output",
    # Types - Pipeline
    "MIBetaOutput",
    # Registry
    "ModelRegistry",
    # Demand
    "DemandAggregator",
    # Space
    "SpaceAssembler", "SpaceLayout",
    # Dimensions
    "DimensionMap",
]
