"""H3 bands sub-package -- four perceptual temporal bands.

Re-exports the four band metadata classes and provides a ``BANDS``
ordered mapping for programmatic lookup by name or index.

Band layout
-----------
=========  ========  ============  ==============  ==================
Band       Horizons  Duration      Frames          Neural correlate
=========  ========  ============  ==============  ==================
Micro      H0-H7    5.8ms-250ms   1-43            Gamma (30-100 Hz)
Meso       H8-H15   300ms-800ms   52-138          Beta-theta (4-30 Hz)
Macro      H16-H23  1s-25s        172-4,307       Delta-theta (1-4 Hz)
Ultra      H24-H31  36s-981s      6,202-168,999   Infra-slow (<0.1 Hz)
=========  ========  ============  ==============  ==================
"""

from __future__ import annotations

from .macro import MacroBand
from .meso import MesoBand
from .micro import MicroBand
from .ultra import UltraBand

__all__ = [
    "MicroBand",
    "MesoBand",
    "MacroBand",
    "UltraBand",
    "BANDS",
]

# Ordered mapping from band name to singleton instance.
BANDS: dict[str, MicroBand | MesoBand | MacroBand | UltraBand] = {
    "micro": MicroBand(),
    "meso":  MesoBand(),
    "macro": MacroBand(),
    "ultra": UltraBand(),
}
