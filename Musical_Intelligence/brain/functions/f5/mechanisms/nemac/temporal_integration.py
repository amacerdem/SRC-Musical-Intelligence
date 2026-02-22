"""NEMAC M+W-Layer -- Temporal Integration (5D).

Nostalgia-Evoked Memory-Affect Circuit integration signals:
  M0: mpfc_activation     — mPFC (BA 8/9) self-referential activity [0, 1]
  M1: hippocampus_activ   — Hippocampal memory retrieval strength [0, 1]
  M2: memory_vividness    — Autobiographical memory vividness [0, 1]
  W0: nostalgia_intens    — Nostalgia intensity (warmth) [0, 1]
  W1: wellbeing_enhance   — Wellbeing enhancement from nostalgia [0, 1]

M0 captures mPFC (BA 8/9) activation for self-referential processing.
Janata 2009: dorsal mPFC parametrically tracks tonal space movement during
autobiographically salient songs (t(9)=5.784, p<0.0003). When music matches
familiar tonal schemas, mPFC increases BOLD signal proportionally.

M1 captures hippocampal activation for autobiographical memory retrieval.
The hippocampus binds disparate memory elements (place, emotion, people)
into coherent episodes. Music acts as an especially potent retrieval cue
because it simultaneously activates auditory, emotional, and motor traces.

M2 measures how vivid the retrieved autobiographical memory is. Vividness
depends on both the retrieval signal (hippocampus) and the emotional
intensity (nostalgia). Vivid memories drive stronger nostalgia and chills.

W0 measures nostalgia intensity -- the subjective warmth/longing feeling.
Self-selected music boosts this by 1.2x (Sakakibara 2025: d=0.88).
Barrett 2010: nostalgia is a mixed but predominantly positive emotion.

W1 captures wellbeing enhancement from nostalgia. Barrett 2010:
nostalgia increases social connectedness, self-continuity, and meaning
in life across 6 studies (N=670+). This is the therapeutic benefit.

H3 demands consumed (5 tuples):
  (0, 16, 0, 2)   roughness value H16 L2            -- dissonance
  (0, 20, 18, 0)  roughness trend H20 L0            -- dissonance trajectory
  (10, 16, 0, 2)  loudness value H16 L2             -- emotional intensity
  (4, 16, 0, 2)   sensory_pleasantness value H16 L2 -- hedonic signal
  (22, 16, 20, 2) entropy entropy H16 L2            -- predictability

R3 features:
  [0] roughness, [4] sensory_pleasantness, [10] loudness, [12] spectral_centroid,
  [22] distribution_entropy, [25:33] x_l0l5

Upstream reads:
  SRP relay (19D) -- P2:pleasure at idx 15
  MEAMN relay (12D) -- P0:memory_state at idx 5, P1:emotional_color at idx 6

Janata 2009: mPFC tracks tonal movement (fMRI, N=13).
Barrett et al. 2010: nostalgia increases wellbeing (6 studies, N=670+).
Sakakibara 2025: self-selected boost 1.2x (d=0.88).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/nemac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ROUGH_VAL_H16 = (0, 16, 0, 2)         # roughness value H16 L2
_ROUGH_TREND_H20 = (0, 20, 18, 0)      # roughness trend H20 L0
_LOUD_VAL_H16 = (10, 16, 0, 2)         # loudness value H16 L2
_PLEAS_VAL_H16 = (4, 16, 0, 2)         # sensory_pleasantness value H16 L2
_ENTROPY_ENT_H16 = (22, 16, 20, 2)     # entropy entropy H16 L2

# -- R3 feature indices -------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_SPECTRAL_CENTROID = 12
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- Upstream relay indices ---------------------------------------------------
_SRP_PLEASURE = 15         # SRP P2:pleasure (hybrid, idx 15)
_MEAMN_MEMORY_STATE = 5   # MEAMN P0:memory_state (hybrid, idx 5)
_MEAMN_EMOTION = 6        # MEAMN P1:emotional_color (hybrid, idx 6)

# -- Constants ----------------------------------------------------------------
_SELF_SELECTED_BOOST = 1.2   # Sakakibara 2025: d=0.88


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute M+W-layer: mPFC, hippocampus, vividness, nostalgia, wellbeing.

    M0 (mpfc_activation) captures self-referential mPFC (BA 8/9) BOLD signal.
    Tonal familiarity + pleasantness + low entropy (predictability) drive
    mPFC activation. Janata 2009: t(9)=5.784 for autobiographically salient.

    M1 (hippocampus_activ) captures hippocampal memory retrieval. Binding
    stability (from E-layer) + MEAMN memory state + emotional intensity.
    Hippocampus binds place + emotion + people into coherent episodes.

    M2 (memory_vividness) measures autobiographical memory vividness.
    Depends on retrieval strength (M1) + emotional nostalgia (E1).
    Vivid memories drive stronger nostalgia downstream.

    W0 (nostalgia_intens) measures nostalgia intensity (warmth/longing).
    Driven by E1 (nostalgia) + mPFC (M0) + memory color from MEAMN.
    Self-selected music boosts 1.2x (Sakakibara 2025: d=0.88).

    W1 (wellbeing_enhance) captures therapeutic wellbeing benefit.
    Barrett 2010: nostalgia increases social connectedness and meaning.
    Requires both nostalgia intensity + positive hedonic context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        relay_outputs: ``{"SRP": (B, T, 19), "MEAMN": (B, T, 12)}``

    Returns:
        ``(M0, M1, M2, W0, W1)`` each ``(B, T)``
    """
    e0, e1 = e

    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    rough_val = h3_features[_ROUGH_VAL_H16]         # (B, T)
    rough_trend = h3_features[_ROUGH_TREND_H20]     # (B, T)
    loud_val = h3_features[_LOUD_VAL_H16]           # (B, T)
    pleas_val = h3_features[_PLEAS_VAL_H16]         # (B, T)
    entropy_ent = h3_features[_ENTROPY_ENT_H16]     # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                  # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]    # (B, T)
    loudness = r3_features[..., _LOUDNESS]                    # (B, T)
    centroid = r3_features[..., _SPECTRAL_CENTROID]           # (B, T)
    entropy = r3_features[..., _ENTROPY]                      # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]    # (B, T, 8)
    x_l0l5_mean = x_l0l5.mean(dim=-1)                        # (B, T)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    meamn = relay_outputs.get("MEAMN", torch.zeros(B, T, 12, device=device))
    pleasure = srp[..., _SRP_PLEASURE]              # (B, T)
    memory_state = meamn[..., _MEAMN_MEMORY_STATE]  # (B, T)
    emotional_color = meamn[..., _MEAMN_EMOTION]    # (B, T)

    # -- Derived signals --
    warmth_proxy = 1.0 - centroid       # low centroid = warm timbre
    familiarity = 1.0 - entropy         # low entropy = predictable = familiar
    valence = pleas_val * (1.0 - rough_val)  # positive valence

    # -- M0: mPFC Activation --
    # Self-referential processing in dorsal mPFC (BA 8/9).
    # Tonal familiarity + pleasantness + low entropy drive mPFC.
    # Janata 2009: dorsal mPFC tracks tonal movement (t=5.784).
    m0 = torch.sigmoid(
        0.35 * familiarity * pleas_val.clamp(min=0.1)
        + 0.30 * memory_state * x_l0l5_mean
        + 0.20 * e1 * warmth_proxy
        + 0.15 * (1.0 - entropy_ent)
    )

    # -- M1: Hippocampus Activation --
    # Autobiographical memory retrieval via hippocampal binding.
    # Memory state (MEAMN) + binding quality + emotional intensity.
    # Hippocampus binds place + emotion + people into episodes.
    m1 = torch.sigmoid(
        0.35 * memory_state * e1.clamp(min=0.1)
        + 0.30 * x_l0l5_mean * loudness
        + 0.20 * emotional_color * loud_val
        + 0.15 * familiarity
    )

    # -- M2: Memory Vividness --
    # Autobiographical memory vividness. Depends on hippocampal
    # retrieval strength (M1) and emotional nostalgia (E1).
    # Vivid memories drive stronger nostalgia and chills downstream.
    m2 = torch.sigmoid(
        0.40 * m1 * e1.clamp(min=0.1)
        + 0.30 * emotional_color * memory_state
        + 0.30 * pleasantness * warmth_proxy
    )

    # -- W0: Nostalgia Intensity --
    # Subjective warmth/longing feeling. E1 (nostalgia) combined with
    # mPFC activation (self-referential) and MEAMN emotional color.
    # Self-selected music boosts 1.2x (Sakakibara 2025: d=0.88).
    # Dissonance trajectory: decreasing roughness = resolution = warmth.
    nostalgia_raw = (
        0.30 * e1 * m0.clamp(min=0.1)
        + 0.25 * emotional_color * memory_state
        + 0.25 * warmth_proxy * valence
        + 0.20 * (1.0 - rough_trend.abs())
    )
    w0 = torch.sigmoid(nostalgia_raw)

    # -- W1: Wellbeing Enhancement --
    # Therapeutic benefit: nostalgia increases social connectedness,
    # self-continuity, and meaning in life.
    # Barrett 2010: predominantly positive emotion (6 studies, N=670+).
    # Requires nostalgia intensity + positive hedonic context.
    w1 = torch.sigmoid(
        0.35 * w0 * pleasure.clamp(min=0.1)
        + 0.30 * m2 * m0
        + 0.20 * valence
        + 0.15 * e1
    )

    return m0, m1, m2, w0, w1
