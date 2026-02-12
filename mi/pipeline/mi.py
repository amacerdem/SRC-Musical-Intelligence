"""
MIPipeline — Full audio → output orchestrator.

Data flow:
  audio → cochlea → R³(49D) → H³(4-tuple) → MusicalBrain(26D) → L³(104D)

One brain. One pipeline. Per-R³-feature H³ tracking.
"""

from __future__ import annotations

from typing import Optional

from torch import Tensor

from ..core.config import MIConfig, MI_CONFIG
from ..core.types import MIOutput, EarOutput
from ..core.registry import DemandAggregator

from ..ear.cochlea import audio_to_mel
from ..ear.r3 import R3Extractor
from ..ear.h3 import H3Extractor

from ..brain.musical_brain import MusicalBrain, BrainOutput
from ..language.brain import BrainSemantics


class MIPipeline:
    """Full MI pipeline: audio → unified brain output + semantics."""

    def __init__(self, config: MIConfig = MI_CONFIG) -> None:
        self.config = config

        # EAR
        self.r3_extractor = R3Extractor(config)
        self.h3_extractor = H3Extractor(config)

        # BRAIN
        self.brain = MusicalBrain()

        # LANGUAGE
        self.semantics = BrainSemantics()

        # H³ demand: compute once, reuse
        self._demand = DemandAggregator.from_brain(self.brain)

    def process(
        self,
        waveform: Tensor,
        return_ear: bool = False,
        return_semantics: bool = True,
    ) -> MIOutput:
        """Process audio through the full pipeline.

        Args:
            waveform: (B, samples) or (samples,) audio tensor
            return_ear: if True, include EAR outputs in result
            return_semantics: if True, compute L³ semantic layer (104D)

        Returns:
            MIOutput with brain (26D) and optionally semantics (104D)
        """
        # ─── EAR ─────────────────────────────────────────────────
        cochlea = audio_to_mel(waveform, self.config)
        r3 = self.r3_extractor.extract(cochlea.mel)
        h3 = self.h3_extractor.extract(r3.features, self._demand)

        ear_output = EarOutput(cochlea=cochlea, r3=r3, h3=h3) if return_ear else None

        # ─── BRAIN ───────────────────────────────────────────────
        brain_output = self.brain.compute(h3.features, r3.features)

        # ─── LANGUAGE ────────────────────────────────────────────
        l3_output = self.semantics.compute(brain_output) if return_semantics else None

        return MIOutput(
            brain=brain_output,
            semantics=l3_output,
            ear=ear_output,
        )

    def reset(self) -> None:
        """Reset stateful components. Call between audio files."""
        self.semantics.reset()
