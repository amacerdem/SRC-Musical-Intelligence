"""TempoState — STU belief, Phase 0.

observe(): Weighted combination of R³ rhythm features + HMCE context.
  R³: tempo_estimate, beat_strength, pulse_clarity, rhythmic_regularity.
  HMCE (v3.0): a1_encoding, stg_encoding, mtg_encoding — hierarchical
    temporal context encoding from auditory cortex (A1→STG→MTG).

  With HMCE:  70% R³ rhythm + 30% HMCE temporal context
  Without:    100% R³ rhythm (backward compatible)

predict(): H³-informed linear model.
  trend: h3[(onset_strength, H6, M18, L0)] — spectral_flux trend at beat
  period: h3[(onset_strength, H6, M14, L0)] — beat regularity
  context: perceived_consonance_{t-1} × 0.05

precision_obs: onset_regularity × salience_proxy / (H³ std + ε)
  HMCE enrichment: cross-signal agreement across 3 cortical levels
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

import torch
from torch import Tensor

from ..belief import Belief, Likelihood
from ..temporal_weights import TEMPO_HORIZONS
from ....ear.r3.registry.feature_map import R3FeatureMap

if TYPE_CHECKING:
    from ..relays.hmce_wrapper import HMCEOutput


class TempoState(Belief):
    """Tempo state — medium inertia belief (τ=0.7)."""

    name = "tempo_state"
    owner_unit = "STU"
    tau = 0.7
    baseline = 0.5
    phase = 0

    # H³ demands for predict()
    h3_predict_demands = (
        ("onset_strength", 6, 18, 0),  # onset trend at beat, L0
        ("onset_strength", 6, 14, 0),  # onset periodicity (beat regularity), L0
    )

    w_trend = 0.20
    w_period = 0.25
    context_weights = {"perceived_consonance": 0.05}

    # ── Multi-scale tempo prediction (v3.1) ─────────────────────
    # 6 horizons from micro to macro — no ultra (tempo is beat/phrase-level)
    multiscale_horizons = TEMPO_HORIZONS   # (5, 7, 10, 13, 18, 21)
    multiscale_feature = "onset_strength"  # R³ feature for H³ lookup
    T_char = 0.6                           # 600ms = beat period (~100 BPM)
    multiscale_alpha = 0.3                 # same decay rate as consonance

    def __init__(self, feature_map: R3FeatureMap) -> None:
        super().__init__(feature_map)
        self._idx_tempo = feature_map.resolve("tempo_estimate")
        self._idx_beat = feature_map.resolve("beat_strength")
        self._idx_pulse = feature_map.resolve("pulse_clarity")
        self._idx_regularity = feature_map.resolve("rhythmic_regularity")
        self._idx_onset = feature_map.resolve("onset_strength")
        self._idx_amplitude = feature_map.resolve("amplitude")

    # v3.0: HMCE blending weight (70% R³ / 30% HMCE context)
    _W_R3 = 0.70
    _W_HMCE = 0.30

    def observe(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
        *,
        hmce_out: Optional[HMCEOutput] = None,
    ) -> Likelihood:
        """Extract tempo observation from R³ rhythm features + HMCE context.

        HMCE mode (v3.0):
            value = 0.70×R³_rhythm + 0.30×HMCE_context
            HMCE context = hierarchical temporal encoding (A1→STG→MTG)
            precision boosted by cross-cortical agreement

        Fallback (no HMCE):
            Original R³ weighted average.
        """
        tempo = r3[..., self._idx_tempo]
        beat = r3[..., self._idx_beat]
        pulse = r3[..., self._idx_pulse]
        regularity = r3[..., self._idx_regularity]

        # R³ tempo state = weighted average of rhythmic indicators
        r3_value = (
            0.35 * tempo
            + 0.25 * beat
            + 0.25 * pulse
            + 0.15 * regularity
        ).clamp(0.0, 1.0)

        # HMCE enrichment: hierarchical temporal context (v3.0)
        if hmce_out is not None:
            # P-layer: regional encoding at 3 cortical levels
            # A1 = onset/beat (short), STG = phrase (medium), MTG = structure (long)
            hmce_context = (
                0.40 * hmce_out.a1_encoding
                + 0.35 * hmce_out.stg_encoding
                + 0.25 * hmce_out.mtg_encoding
            ).clamp(0.0, 1.0)

            value = (
                self._W_R3 * r3_value + self._W_HMCE * hmce_context
            ).clamp(0.0, 1.0)
        else:
            value = r3_value

        # Precision: onset regularity × amplitude (clear onsets = reliable)
        onset = r3[..., self._idx_onset]
        amplitude = r3[..., self._idx_amplitude]
        onset_regularity = regularity * onset  # proxy

        h3_std_key = (self._idx_onset, 6, 2, 0)  # M2=std, H6, L0
        h3_std = h3.get(h3_std_key, torch.tensor(0.1))
        if h3_std.dim() < 2:
            h3_std = torch.full_like(value, 0.1)

        precision = onset_regularity * amplitude / (h3_std + 1e-6)

        # HMCE precision boost: cross-cortical agreement
        if hmce_out is not None:
            hmce_stack = torch.stack([
                hmce_out.a1_encoding,
                hmce_out.stg_encoding,
                hmce_out.mtg_encoding,
            ], dim=-1)  # (B, T, 3)
            hmce_agreement = 1.0 / (hmce_stack.std(dim=-1) + 0.1)
            precision = precision + 0.3 * hmce_agreement

        precision = precision.clamp(0.01, 10.0)

        return Likelihood(value=value, precision=precision)
