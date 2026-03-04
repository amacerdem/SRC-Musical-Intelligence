"""Ψ³ Cognitive Interpreter — maps C³ internals to experiential state.

Ψ³ is INSIDE C³ (TERMINOLOGY.md Section 16). It is a readout layer, not a
new neural computation. It maps tensor + ram + neuro → PsiState using
established neuro-cognitive correspondences.

Dimensions are organized into 6 cognitive domains:
    Affect:    valence, arousal, tension, dominance  (Laeng 2021 calibrated)
    Emotion:   joy, sadness, fear, awe, nostalgia, tenderness, serenity
    Aesthetic:  beauty, groove, flow, surprise, closure
    Bodily:    chills, movement_urge, breathing_change, tension_release
    Cognitive: familiarity, absorption, expectation, attention_focus
    Temporal:  anticipation, resolution, buildup, release
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from Musical_Intelligence.brain.neurochemicals import DA, NE, OPI, _5HT
from Musical_Intelligence.brain.regions import region_index
from Musical_Intelligence.contracts.dataclasses.brain_output import PsiState

if TYPE_CHECKING:
    from torch import Tensor


class PsiInterpreter:
    """Maps C³ internal outputs → Ψ³ cognitive state.

    Each mapping function uses published neuro-cognitive correspondences
    to derive experiential dimensions from the three C³ internal outputs.
    """

    def interpret(self, tensor: Tensor, ram: Tensor, neuro: Tensor) -> PsiState:
        """Compute Ψ³ cognitive state from C³ internals.

        Args:
            tensor: ``(B, T, N_ext)`` — external+hybrid dims from all nuclei.
            ram:    ``(B, T, 26)`` — Region Activation Map.
            neuro:  ``(B, T, 4)`` — neurochemical state [DA, NE, OPI, 5HT].

        Returns:
            PsiState with 6 cognitive domains.
        """
        affect = self._compute_affect(neuro, ram)
        emotion = self._compute_emotion(affect, ram)
        aesthetic = self._compute_aesthetic(tensor, neuro, ram)
        bodily = self._compute_bodily(ram, neuro)
        cognitive = self._compute_cognitive(ram, tensor)
        temporal = self._compute_temporal(tensor, neuro)

        return PsiState(
            affect=affect,
            emotion=emotion,
            aesthetic=aesthetic,
            bodily=bodily,
            cognitive=cognitive,
            temporal=temporal,
        )

    # ------------------------------------------------------------------
    # Domain mapping functions
    # ------------------------------------------------------------------

    def _compute_affect(self, neuro: Tensor, ram: Tensor) -> Tensor:
        """Core emotional coordinates: valence, arousal, tension, dominance.

        Mappings (Doya 2002, Russell 1980, Koelsch 2014, Laeng 2021):
            valence  = f(DA, OPI)     — cognitive reward evaluation (DA-dominant)
            arousal  = f(NE, OPI)     — sympathetic + hedonic-bodily activation
            tension  = f(amygdala, 5HT) — threat/salience detection
            dominance = f(dlPFC)      — executive control / agency

        Laeng 2021 dissociation: OPI blockade reduces physiological arousal
        (pupil dilation) but preserves cognitive valence judgments. This
        constrains the OPI weight: small for valence, larger for arousal.
        """
        B, T = neuro.shape[:2]
        device = neuro.device

        # Valence: cognitive goodness evaluation — DA-dominant
        # OPI contributes slightly (hedonic tone colors evaluation) but
        # cognitive valence persists under opioid blockade (Laeng 2021)
        valence = 0.9 * neuro[:, :, DA] + 0.1 * neuro[:, :, OPI]

        # Arousal: sympathetic activation (NE) + hedonic-bodily response (OPI)
        # OPI drives chills, piloerection, pupil dilation (Blood & Zatorre 2001)
        # Laeng 2021: opioid blockade reduces physiological arousal to music
        arousal = 0.7 * neuro[:, :, NE] + 0.3 * neuro[:, :, OPI]

        # Tension: amygdala activation + inverse serotonin
        amygdala_idx = region_index("amygdala")
        tension = 0.5 * ram[:, :, amygdala_idx] + 0.5 * (1.0 - neuro[:, :, _5HT])

        # Dominance: dlPFC activation (executive control)
        dlpfc_idx = region_index("dlPFC")
        dominance = ram[:, :, dlpfc_idx]

        return torch.stack([valence, arousal, tension, dominance], dim=-1).clamp(0, 1)

    def _compute_emotion(self, affect: Tensor, ram: Tensor) -> Tensor:
        """Categorical emotions from affect + RAM patterns (Koelsch 2014).

        7 emotions: joy, sadness, fear, awe, nostalgia, tenderness, serenity
        """
        valence = affect[:, :, 0]
        arousal = affect[:, :, 1]
        tension = affect[:, :, 2]

        nacc_idx = region_index("NAcc")
        hippocampus_idx = region_index("hippocampus")

        # Simple combinatorial mapping — calibrated against behavioral data
        joy = valence * arousal
        sadness = (1.0 - valence) * (1.0 - arousal)
        fear = tension * arousal
        awe = valence * arousal * ram[:, :, nacc_idx]
        nostalgia = valence * ram[:, :, hippocampus_idx]
        tenderness = valence * (1.0 - arousal) * (1.0 - tension)
        serenity = valence * (1.0 - tension) * (1.0 - arousal)

        return torch.stack(
            [joy, sadness, fear, awe, nostalgia, tenderness, serenity],
            dim=-1,
        ).clamp(0, 1)

    def _compute_aesthetic(self, tensor: Tensor, neuro: Tensor, ram: Tensor) -> Tensor:
        """Musical judgement: beauty, groove, flow, surprise, closure.

        Beauty and groove require tensor outputs from specific nuclei;
        at this stage (single BCH nucleus) we use proxies.
        """
        B, T = neuro.shape[:2]
        device = neuro.device

        putamen_idx = region_index("putamen")
        sma_idx = region_index("SMA")
        nacc_idx = region_index("NAcc")

        # Beauty: reward integration (NAcc + valence proxy)
        beauty = 0.5 * neuro[:, :, DA] + 0.5 * neuro[:, :, OPI]

        # Groove: motor areas + rhythm (Janata 2012)
        groove = 0.5 * ram[:, :, putamen_idx] + 0.5 * ram[:, :, sma_idx]

        # Flow: high engagement + low tension
        flow = ram[:, :, nacc_idx] * (1.0 - (1.0 - neuro[:, :, _5HT]) * 0.5)

        # Surprise: DA phasic bursts (Schultz 1997)
        surprise = torch.relu(neuro[:, :, DA] - 0.6)  # Above phasic threshold

        # Closure: inverse surprise (resolution)
        closure = 1.0 - surprise

        return torch.stack([beauty, groove, flow, surprise, closure], dim=-1).clamp(0, 1)

    def _compute_bodily(self, ram: Tensor, neuro: Tensor) -> Tensor:
        """Felt sensations: chills, movement_urge, breathing_change, tension_release.

        Chills: PAG + hypothalamus + OPI (Blood & Zatorre 2001)
        Movement: putamen + SMA (Grahn & Rowe 2009)
        """
        pag_idx = region_index("PAG")
        hypo_idx = region_index("hypothalamus")
        putamen_idx = region_index("putamen")
        sma_idx = region_index("SMA")

        chills = (
            0.3 * ram[:, :, pag_idx]
            + 0.3 * ram[:, :, hypo_idx]
            + 0.4 * neuro[:, :, OPI]
        )
        movement_urge = 0.5 * ram[:, :, putamen_idx] + 0.5 * ram[:, :, sma_idx]
        breathing_change = ram[:, :, hypo_idx]
        tension_release = neuro[:, :, OPI] * (1.0 - neuro[:, :, NE])

        return torch.stack(
            [chills, movement_urge, breathing_change, tension_release],
            dim=-1,
        ).clamp(0, 1)

    def _compute_cognitive(self, ram: Tensor, tensor: Tensor) -> Tensor:
        """Mental states: familiarity, absorption, expectation, attention_focus.

        Familiarity: hippocampus (Janata 2009)
        Absorption: insula + NAcc (Craig 2009)
        """
        hippocampus_idx = region_index("hippocampus")
        insula_idx = region_index("insula")
        nacc_idx = region_index("NAcc")
        dlpfc_idx = region_index("dlPFC")

        familiarity = ram[:, :, hippocampus_idx]
        absorption = 0.5 * ram[:, :, insula_idx] + 0.5 * ram[:, :, nacc_idx]
        # Expectation and attention are tensor-derived — proxy with RAM
        expectation = ram[:, :, dlpfc_idx]
        attention_focus = ram[:, :, dlpfc_idx]

        return torch.stack(
            [familiarity, absorption, expectation, attention_focus],
            dim=-1,
        ).clamp(0, 1)

    def _compute_temporal(self, tensor: Tensor, neuro: Tensor) -> Tensor:
        """Moment-in-time: anticipation, resolution, buildup, release.

        Anticipation: DA rising (Salimpoor 2011 — caudate peaks before pleasure)
        Resolution: DA stable + OPI (consummatory)
        """
        B, T = neuro.shape[:2]

        # Anticipation: DA above baseline but below phasic threshold
        anticipation = torch.relu(neuro[:, :, DA] - 0.5) * 2.0  # Scale to [0, 1]
        anticipation = anticipation.clamp(0, 1)

        # Resolution: OPI peak (consummatory pleasure)
        resolution = neuro[:, :, OPI]

        # Buildup: NE rising (arousal escalation)
        buildup = torch.relu(neuro[:, :, NE] - 0.5) * 2.0
        buildup = buildup.clamp(0, 1)

        # Release: inverse tension (5HT-mediated calm)
        release = neuro[:, :, _5HT]

        return torch.stack(
            [anticipation, resolution, buildup, release],
            dim=-1,
        ).clamp(0, 1)
