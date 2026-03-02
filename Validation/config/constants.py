"""MI system constants shared across all validation modules."""
from __future__ import annotations

# ── Audio ──
SAMPLE_RATE: int = 44100
HOP_LENGTH: int = 256
N_MELS: int = 128
N_FFT: int = 2048
FRAME_RATE: float = SAMPLE_RATE / HOP_LENGTH  # 172.265625 Hz

# ── R³ ──
R3_DIM: int = 97
R3_GROUPS = {
    "A": (0, 7),     # consonance (7D)
    "B": (7, 12),    # energy (5D)
    "C": (12, 21),   # timbre (9D)
    "D": (21, 25),   # change (4D)
    "F": (25, 41),   # pitch (16D)
    "G": (41, 51),   # rhythm (10D)
    "H": (51, 63),   # harmony (12D)
    "J": (63, 83),   # timbre_ext (20D)
    "K": (83, 97),   # modulation (14D)
}

# ── H³ ──
H3_HORIZONS: int = 32
H3_MORPHS: int = 24
H3_LAWS: int = 3

# ── C³ ──
NUM_BELIEFS: int = 131
NUM_CORE_BELIEFS: int = 36
NUM_APPRAISAL_BELIEFS: int = 65
NUM_ANTICIPATION_BELIEFS: int = 30
NUM_FUNCTIONS: int = 9
NUM_REGIONS: int = 26
NUM_NEUROCHEMICALS: int = 4

# ── Neurochemical channels ──
DA: int = 0   # dopamine
NE: int = 1   # norepinephrine
OPI: int = 2  # opioid
_5HT: int = 3  # serotonin

NEURO_NAMES = ("DA", "NE", "OPI", "5HT")
NEURO_BASELINE: float = 0.5

# ── Dimension tiers ──
DIM_PSYCHOLOGY: int = 6
DIM_COGNITION: int = 12
DIM_NEUROSCIENCE: int = 24

# ── Ψ³ domains ──
PSI_DOMAINS = {
    "affect": 4,
    "emotion": 7,
    "aesthetic": 5,
    "bodily": 4,
    "cognitive": 4,
    "temporal": 4,
}

# ── Region groups ──
CORTICAL_REGIONS = list(range(0, 12))
SUBCORTICAL_REGIONS = list(range(12, 21))
BRAINSTEM_REGIONS = list(range(21, 26))

REGION_NAMES = (
    # Cortical (0-11)
    "A1_HG", "STG", "STS", "IFG", "dlPFC", "vmPFC",
    "OFC", "ACC", "SMA", "PMC", "AG", "TP",
    # Subcortical (12-20)
    "VTA", "NAcc", "caudate", "amygdala", "hippocampus",
    "putamen", "MGB", "hypothalamus", "insula",
    # Brainstem (21-25)
    "IC", "AN", "CN", "SOC", "PAG",
)

# ── MNI152 coordinates for all 26 regions ──
MNI_COORDINATES = {
    "A1_HG": (48, -18, 8),
    "STG": (58, -22, 4),
    "STS": (52, -28, -4),
    "IFG": (-48, 18, 20),
    "dlPFC": (-42, 36, 24),
    "vmPFC": (2, 46, -12),
    "OFC": (30, 34, -14),
    "ACC": (2, 30, 24),
    "SMA": (-4, -6, 58),
    "PMC": (-38, -20, 54),
    "AG": (-46, -64, 30),
    "TP": (48, 12, -28),
    "VTA": (2, -16, -12),
    "NAcc": (10, 12, -6),
    "caudate": (12, 10, 10),
    "amygdala": (-22, -4, -18),
    "hippocampus": (-28, -20, -12),
    "putamen": (-24, 4, 2),
    "MGB": (14, -24, -4),
    "hypothalamus": (2, -4, -10),
    "insula": (-36, 14, 2),
    "IC": (0, -34, -6),
    "AN": (0, -40, -30),
    "CN": (6, -38, -24),
    "SOC": (8, -36, -20),
    "PAG": (0, -30, -10),
}
