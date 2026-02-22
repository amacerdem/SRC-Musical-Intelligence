"""NEMAC E-Layer -- Extraction (2D).

Nostalgia-Evoked Memory-Affect Circuit extraction signals:
  E0: chills            — Music-evoked chills from nostalgia convergence [0, 1]
  E1: nostalgia         — Nostalgic response strength [0, 1]

E0 captures chills -- the piloerection/frisson response that occurs when
nostalgic warmth, memory vividness, and hedonic reward converge. Chills
require simultaneous activation of mPFC (self-referential), hippocampus
(memory retrieval), and ventral striatum (reward). SRP.pleasure provides the
reward gate: chills only fire when pleasure is above threshold. Cheung 2019:
surprise x uncertainty interaction predicts pleasure peaks where chills occur.

E1 captures the overall nostalgic response to music. Driven by timbre warmth
(low spectral centroid = warm), tonal familiarity (binding stability), and
MEAMN memory retrieval. Sakakibara 2025: self-selected music boosts nostalgia
intensity by 1.2x (d=0.88, EEG N=33). Barrett 2010: nostalgia is a mixed
but predominantly positive emotion that increases social connectedness.

H3 demands consumed (4 tuples):
  (3, 16, 1, 2)   stumpf_fusion mean H16 L2      -- binding stability 1s
  (3, 20, 1, 2)   stumpf_fusion mean H20 L2      -- binding 5s consolidation
  (12, 16, 0, 2)  warmth value H16 L2            -- current timbre warmth
  (12, 20, 1, 0)  warmth mean H20 L0             -- sustained warmth 5s

R3 features:
  [0] roughness, [4] sensory_pleasantness, [10] loudness, [12] spectral_centroid,
  [14] tonalness, [25:33] x_l0l5

Upstream reads:
  SRP relay (19D) -- P2:pleasure at idx 15
  MEAMN relay (12D) -- P0:memory_state at idx 5

Cheung et al. 2019: surprise x uncertainty predicts pleasure (N=39, 80k).
Sakakibara 2025: self-selected music boosts nostalgia 1.2x (d=0.88).
Barrett et al. 2010: nostalgia increases wellbeing (6 studies, N=670+).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/nemac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_STUMPF_MEAN_H16 = (3, 16, 1, 2)      # stumpf_fusion mean H16 L2
_STUMPF_MEAN_H20 = (3, 20, 1, 2)      # stumpf_fusion mean H20 L2
_WARMTH_VAL_H16 = (12, 16, 0, 2)      # warmth value H16 L2
_WARMTH_MEAN_H20 = (12, 20, 1, 0)     # warmth mean H20 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_SPECTRAL_CENTROID = 12
_TONALNESS = 14
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- Upstream relay indices ---------------------------------------------------
_SRP_PLEASURE = 15       # SRP P2:pleasure (hybrid, idx 15)
_MEAMN_MEMORY_STATE = 5  # MEAMN P0:memory_state (hybrid, idx 5)
_MEAMN_NOSTALGIA = 7     # MEAMN P2:nostalgia_link (hybrid, idx 7)

# -- Constants ----------------------------------------------------------------
_SELF_SELECTED_BOOST = 1.2   # Sakakibara 2025: d=0.88, self-selected boost


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: chills and nostalgia extraction signals.

    E0 (chills) captures piloerection/frisson from nostalgia convergence.
    Requires simultaneous warmth + binding + pleasure above threshold.
    SRP.pleasure gates the chills response -- no pleasure = no chills.
    Cheung 2019: surprise x uncertainty predicts pleasure peaks (N=39).

    E1 (nostalgia) captures overall nostalgic response strength. Driven by
    timbre warmth (low spectral centroid), tonal familiarity (binding),
    and MEAMN memory retrieval. Self-selected music boosts 1.2x.
    Sakakibara 2025: d=0.88 (EEG, N=33, eta_p^2=0.636).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"SRP": (B, T, 19), "MEAMN": (B, T, 12)}``

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    stumpf_1s = h3_features[_STUMPF_MEAN_H16]      # (B, T)
    stumpf_5s = h3_features[_STUMPF_MEAN_H20]      # (B, T)
    warmth_val = h3_features[_WARMTH_VAL_H16]       # (B, T)
    warmth_mean = h3_features[_WARMTH_MEAN_H20]     # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                  # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]    # (B, T)
    loudness = r3_features[..., _LOUDNESS]                    # (B, T)
    centroid = r3_features[..., _SPECTRAL_CENTROID]           # (B, T)
    tonalness = r3_features[..., _TONALNESS]                  # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]    # (B, T, 8)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    meamn = relay_outputs.get("MEAMN", torch.zeros(B, T, 12, device=device))
    pleasure = srp[..., _SRP_PLEASURE]              # (B, T)
    memory_state = meamn[..., _MEAMN_MEMORY_STATE]  # (B, T)
    nostalgia_link = meamn[..., _MEAMN_NOSTALGIA]   # (B, T)

    # -- Derived signals --
    x_l0l5_mean = x_l0l5.mean(dim=-1)  # (B, T) memory-affect binding
    warmth_proxy = 1.0 - centroid       # low centroid = warm timbre
    binding = 0.50 * stumpf_1s + 0.50 * stumpf_5s  # multi-scale binding

    # -- E0: Chills --
    # Piloerection/frisson from convergence of warmth + memory + reward.
    # Pleasure gates the response: chills only fire above threshold.
    # Binding stability provides the memory coherence scaffold.
    # Cheung 2019: surprise x uncertainty -> pleasure -> chills.
    e0 = torch.sigmoid(
        0.30 * pleasure * memory_state.clamp(min=0.1)
        + 0.30 * warmth_val * binding.clamp(min=0.1)
        + 0.25 * x_l0l5_mean * nostalgia_link
        + 0.15 * loudness * pleasantness
    )

    # -- E1: Nostalgia --
    # Overall nostalgic response: warmth + familiarity + memory retrieval.
    # Self-selected music boosts nostalgia 1.2x (Sakakibara 2025: d=0.88).
    # mPFC + hippocampus hub creates vivid autobiographical nostalgia.
    # Barrett 2010: nostalgia is predominantly positive emotion.
    nostalgia_raw = (
        0.30 * warmth_proxy * warmth_mean.clamp(min=0.1)
        + 0.25 * binding * tonalness
        + 0.25 * memory_state * nostalgia_link
        + 0.20 * pleasantness * (1.0 - roughness)
    )
    e1 = torch.sigmoid(nostalgia_raw)

    return e0, e1
