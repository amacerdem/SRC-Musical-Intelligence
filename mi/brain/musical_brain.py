"""
MusicalBrain — Unified Musical Cognition (26D)

One brain. Internal pathways that share state. Like the real brain.

Pipeline:
  H³ features (4-tuple) + R³ direct → shared_state (4D)
                                     → reward_pathway (9D)   [reads shared_state]
                                     → affect_pathway (6D)   [reads shared_state + R³]
                                     → autonomic_pathway (5D) [reads shared + reward + affect]
                                     → integration (2D)      [reads reward + affect]

Total: 26D per frame. Zero learned parameters. Every dimension has a citation.

Replaces:
  SRP (19D) + AAC (14D) + VMM (12D) = 45D across 3 separate models
  AED + CPD + C0P + ASA = 120D mechanism layer

Scientific basis:
  Reward: Salimpoor 2011 (β₁=0.84, β₂=0.71), Blood & Zatorre 2001, Berridge 2003
  Affect: Fritz 2009 (F(2,39)=15.48), Koelsch 2006 (t=5.1), Mitterschiffthaler 2007
  Autonomic: de Fleurian & Pearce 2021 (k=116, d=0.85), Ferreri 2019, Peng 2022
  Shared: Yang 2025, Ding 2025, Fong 2020, Kim 2021, Sachs 2025
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import torch
from torch import Tensor

from ..core.constants import (
    BETA_NACC,
    BETA_CAUDATE,
    R3_CONSONANCE,
    MORPH_SCALE,
    N_LAWS,
)


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT TYPE
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class BrainOutput:
    """Output of the unified Musical Brain."""
    tensor: Tensor                                  # (B, T, 26)
    dimension_names: Tuple[str, ...]                # 26 names
    pathway_ranges: Dict[str, Tuple[int, int]]      # {"shared": (0,4), ...}

    def get_pathway(self, name: str) -> Tensor:
        """Extract a pathway slice by name."""
        s, e = self.pathway_ranges[name]
        return self.tensor[..., s:e]

    def get_dim(self, name: str) -> Tensor:
        """Extract a single dimension by name."""
        idx = self.dimension_names.index(name)
        return self.tensor[..., idx]


# ═══════════════════════════════════════════════════════════════════════
# MUSICAL BRAIN
# ═══════════════════════════════════════════════════════════════════════

# Valence pathway weights — Mitterschiffthaler 2007: equal contribution
_ALPHA_H = 0.50
_ALPHA_S = 0.50


class MusicalBrain:
    """Unified Musical Brain — one integrated system with dissociable pathways.

    Internal pathways (NOT separate models):
      - Shared State (4D): arousal, prediction error, harmonic context, momentum
      - Reward (9D): VTA → Caudate DA (wanting) + NAcc DA (liking) [Salimpoor 2011]
      - Affect (6D): Mode → Valence → Happy/Sad pathways [Fritz 2009, Koelsch 2006]
      - Autonomic (5D): ANS readout of brain state [de Fleurian & Pearce 2021]
      - Integration (2D): beauty, emotional arc

    Pathways are NOT independent. Autonomic receives arousal FROM shared state,
    da_nacc FROM reward, valence FROM affect. Like the real brain.
    """

    NAME = "Brain"
    OUTPUT_DIM = 26

    DIMENSION_NAMES: Tuple[str, ...] = (
        # Shared State [0:4]
        "arousal", "prediction_error", "harmonic_context", "emotional_momentum",
        # Reward Pathway [4:13]
        "da_caudate", "da_nacc", "opioid_proxy",
        "wanting", "liking", "pleasure",
        "tension", "prediction_match", "reward_forecast",
        # Affect Pathway [13:19]
        "f03_valence", "mode_signal", "consonance_valence",
        "happy_pathway", "sad_pathway", "emotion_certainty",
        # Autonomic Pathway [19:24]
        "scr", "hr", "respr", "chills_intensity", "ans_composite",
        # Integration [24:26]
        "beauty", "emotional_arc",
    )

    PATHWAY_RANGES: Dict[str, Tuple[int, int]] = {
        "shared": (0, 4),
        "reward": (4, 13),
        "affect": (13, 19),
        "autonomic": (19, 24),
        "integration": (24, 26),
    }

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """All H³ 4-tuples needed by the brain (union of all pathways).

        24 unique tuples across 8 R³ features, 6 horizons, 10 morphs, 3 laws.
        Every tuple has a scientific citation in the computation below.

        Returns:
            List of (r3_idx, horizon, morph, law) 4-tuples
        """
        # Deduplicated union from all pathways.
        # Organized by horizon for H³ extraction efficiency.
        demand = set()

        # ── H9 (350ms) — fast ANS + arousal ────────────────────────
        demand |= {
            (10, 9, 4, 2),    # loudness max — arousal: peak energy [Yang 2025]
            (8,  9, 8, 2),    # velocity_A velocity — arousal: rate [Ding 2025]
            (11, 9, 11, 2),   # onset_strength accel — arousal: transient [Scherer 2013]
        }

        # ── H16 (1s) — bar-level dynamics ───────────────────────────
        demand |= {
            (14, 16, 14, 2),  # tonalness periodicity — tempo signal [de Fleurian 2021]
            (8,  16, 8, 2),   # velocity_A velocity — bar dynamics [Fancourt 2020]
        }

        # ── H18 (2s) — phrase-level consummatory ────────────────────
        demand |= {
            (3,  18, 0, 2),   # stumpf_fusion value — consonance now [Salimpoor 2011]
            (3,  18, 14, 2),  # stumpf_fusion periodicity — harmonic regularity
            (3,  18, 15, 2),  # stumpf_fusion smoothness — sustained consonance [Blood 2001]
            (3,  18, 2, 2),   # stumpf_fusion std — prediction error [Fong 2020]
            (10, 18, 4, 2),   # loudness max — peak loudness [Salimpoor 2011]
            (10, 18, 18, 0),  # loudness trend — energy trajectory [Sachs 2025]
            (8,  18, 8, 0),   # velocity_A velocity — dynamics rate [Zatorre 2013]
            (14, 18, 14, 2),  # tonalness periodicity — tonal regularity [Blood 2001]
        }

        # ── H19 (3s) — phrase harmonic context + ANS baseline ───────
        demand |= {
            (3,  19, 14, 2),  # stumpf_fusion periodicity — harmonic context [Kim 2021]
            (3,  19, 2, 2),   # stumpf_fusion std — mode ambiguity [Fritz 2009]
            (4,  19, 1, 2),   # sensory_pleasantness mean — pleasantness [Koelsch 2006]
            (10, 19, 1, 2),   # loudness mean — arousal baseline [Mitterschiffthaler 2007]
            (10, 19, 19, 2),  # loudness stability — ANS baseline [Peng 2022]
            (7,  19, 4, 2),   # amplitude max — energy context [Fancourt 2020]
        }

        # ── H20 (5s) — phrase-level anticipation ────────────────────
        demand |= {
            (10, 20, 4, 1),   # loudness max predict — anticipation [Salimpoor 2011]
            (4,  20, 0, 2),   # sensory_pleasantness value — happy pathway [Koelsch 2006]
        }

        # ── H22 (15s) — Salimpoor window + section stability ───────
        demand |= {
            (10, 22, 4, 1),   # loudness max predict — Salimpoor 15s [Salimpoor 2011]
            (3,  22, 19, 2),  # stumpf_fusion stability — mode stability [Fritz 2009]
            (12, 22, 19, 2),  # warmth stability — timbral stability [Brattico 2011]
        }

        return sorted(demand)

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> BrainOutput:
        """Compute the unified 26D brain output.

        Data flow:
          1. Read all H³ demands + R³ direct features
          2. Shared state (4D) — available to all pathways
          3. Reward pathway (9D) — uses shared
          4. Affect pathway (6D) — uses shared + R³ direct
          5. Autonomic pathway (5D) — uses shared + reward + affect
          6. Integration (2D) — uses reward + affect

        Args:
            h3_features: {(r3_idx, h, m, l): (B, T)} per-R³-feature temporals
            r3_features: (B, T, 49) R³ spectral features (for affect mode detection)

        Returns:
            BrainOutput with (B, T, 26) tensor
        """
        # ─── HELPER: scaled H³ read ────────────────────────────────
        sample = next(iter(h3_features.values()))
        B, T = sample.shape
        device, dtype = sample.device, sample.dtype
        zero = torch.zeros(B, T, device=device, dtype=dtype)

        def g(r3_idx: int, h: int, m: int, l: int) -> Tensor:
            """Get H³ value with per-morph scaling."""
            val = h3_features.get((r3_idx, h, m, l))
            if val is None:
                return zero
            gain, bias = MORPH_SCALE[m]
            return gain * (val - bias)

        # ═══════════════════════════════════════════════════════════
        # H³ NAMED READS (organized by horizon)
        # ═══════════════════════════════════════════════════════════

        # H9 (350ms) — fast response
        loud_max_h9       = g(10, 9,  4,  2)   # loudness max
        vel_A_h9          = g(8,  9,  8,  2)   # velocity_A velocity
        onset_accel_h9    = g(11, 9,  11, 2)   # onset acceleration

        # H16 (1s) — bar-level
        tempo_signal      = g(14, 16, 14, 2)   # tonalness periodicity
        vel_A_h16         = g(8,  16, 8,  2)   # velocity_A velocity

        # H18 (2s) — phrase consummatory
        consonance_mean   = g(3,  18, 0,  2)   # stumpf weighted mean
        consonance_period = g(3,  18, 14, 2)   # stumpf periodicity
        consonance_smooth = g(3,  18, 15, 2)   # stumpf smoothness
        consonance_std    = g(3,  18, 2,  2)   # stumpf std
        loudness_max      = g(10, 18, 4,  2)   # loudness max
        loudness_trend    = g(10, 18, 18, 0)   # loudness trend
        velocity_A_vel    = g(8,  18, 8,  0)   # velocity_A velocity
        tonalness_period  = g(14, 18, 14, 2)   # tonalness periodicity

        # H19 (3s) — phrase context + baseline
        cons_period_h19   = g(3,  19, 14, 2)   # stumpf periodicity
        cons_ambiguity    = g(3,  19, 2,  2)   # stumpf std (ambiguity)
        pleas_mean_h19    = g(4,  19, 1,  2)   # pleasantness mean
        loud_mean_h19     = g(10, 19, 1,  2)   # loudness mean
        loud_stab_h19     = g(10, 19, 19, 2)   # loudness stability
        amp_max_h19       = g(7,  19, 4,  2)   # amplitude max

        # H20 (5s) — anticipation
        loud_max_5s       = g(10, 20, 4,  1)   # loudness max predict
        pleas_val_h20     = g(4,  20, 0,  2)   # pleasantness value

        # H22 (15s) — Salimpoor window + section stability
        loud_max_15s      = g(10, 22, 4,  1)   # loudness max predict
        cons_stab_15s     = g(3,  22, 19, 2)   # consonance stability
        warmth_stab_h22   = g(12, 22, 19, 2)   # warmth stability

        # R³ DIRECT — instantaneous spectral features (per-frame, no H³ smoothing)
        r3 = r3_features
        consonance_level = r3[..., R3_CONSONANCE[0]:R3_CONSONANCE[1]].mean(dim=-1)
        stumpf_r3        = r3[..., 3]    # stumpf_fusion: consonance quality (σ=0.15)
        pleasant_r3      = r3[..., 4]    # sensory_pleasantness: hedonic quality (σ=0.19)
        amplitude_r3     = r3[..., 7]    # amplitude: current energy (σ=0.24)
        warmth_r3        = r3[..., 12]   # warmth
        brightness       = r3[..., 15]   # clarity
        tristimulus1     = r3[..., 18]   # tristimulus1

        # ═══════════════════════════════════════════════════════════
        # SHARED STATE (4D) — computed FIRST, available to all
        # ═══════════════════════════════════════════════════════════

        # D0: arousal — current energy-based activation [Yang 2025]
        # g() outputs ~[-3,+3]; coefficients sum to 1.0 → input in [-3,+3]
        arousal = torch.sigmoid(
            0.50 * loud_max_h9
            + 0.30 * vel_A_h9
            + 0.20 * onset_accel_h9
        )

        # D1: prediction_error — expectation violation [Fong 2020]
        prediction_error = torch.tanh(
            0.60 * consonance_std - 0.40 * cons_stab_15s
        )

        # D2: harmonic_context — current harmonic quality [Kim 2021]
        harmonic_context = torch.sigmoid(
            0.60 * cons_period_h19
            + 0.40 * pleas_mean_h19
        )

        # D3: emotional_momentum — carry-forward trajectory [Sachs 2025]
        emotional_momentum = torch.tanh(0.80 * loudness_trend)

        # ═══════════════════════════════════════════════════════════
        # REWARD PATHWAY (9D) — striatal dopamine dynamics
        # ═══════════════════════════════════════════════════════════

        # D4: da_caudate — anticipatory DA ramp [Salimpoor 2011, r=0.71]
        # Three factors:
        #   future_reward: HOW REWARDING the future will be (absolute level)
        #   gap_gate: tanh-gated positive gap (future > present, diminishing returns)
        #   engagement: music must be present
        # Key insight: Salimpoor found caudate correlates with anticipated REWARD
        # MAGNITUDE — anticipating a climax (ff) produces more DA than anticipating
        # a moderate passage (mf), even if the gap is similar.
        gap_15s = loud_max_15s - loudness_max    # Salimpoor 15s window
        gap_5s  = loud_max_5s - loudness_max     # 5s phrase gap
        engagement = torch.sigmoid(2.0 * loudness_max)
        # How rewarding will the future sound? (absolute level, not gap)
        future_reward = torch.sigmoid(
            0.50 * loud_max_5s + 0.50 * loud_max_15s
        )
        # Positive gap gate with diminishing returns (tanh prevents clamp saturation)
        positive_gap = 0.50 * torch.relu(gap_5s) + 0.50 * torch.relu(gap_15s)
        gap_gate = torch.tanh(2.0 * positive_gap)   # 0 at gap=0, ~0.96 at gap≥1
        da_caudate = future_reward * gap_gate * engagement

        # D5: da_nacc — consummatory DA burst [Salimpoor 2011, r=0.84]
        # PRESENT-focused: individual R³ features (not group means — too flat).
        # Berridge 2003 wanting/liking dissociation:
        #   da_caudate (wanting): H³ FUTURE-oriented (predict law, 5s/15s ahead)
        #   da_nacc (liking): R³ PRESENT-focused (instantaneous sensory beauty)
        # R³ values in [0,1]; max total input ≈ ±3.25 → sigmoid [0.04, 0.96]
        da_nacc = torch.sigmoid(
            3.0 * (pleasant_r3 - 0.5)     # sensory pleasantness NOW [Salimpoor 2011]
            + 2.0 * (stumpf_r3 - 0.5)     # consonance quality NOW [Blood 2001]
            + 1.5 * (amplitude_r3 - 0.5)  # energy level NOW [Zatorre 2013]
        )

        # D6: opioid_proxy — sustained hedonic tone [Blood & Zatorre 2001]
        opioid_proxy = torch.sigmoid(
            0.40 * consonance_mean
            + 0.30 * consonance_smooth
            + 0.30 * tonalness_period
        )

        # D7: wanting — [Berridge 2003]
        wanting = (BETA_CAUDATE * da_caudate).clamp(0, 1)

        # D8: liking — [Berridge 2003]
        liking = (BETA_NACC * da_nacc).clamp(0, 1)

        # D9: pleasure — geometric mean: peaks when BOTH DA signals high
        # [Salimpoor 2011 dual-peak: need wanting AND liking convergence]
        pleasure = (da_nacc * da_caudate).sqrt()

        # D10: tension — uses shared harmonic_context [Huron 2006 ITPRA]
        tension = torch.sigmoid(
            -2.0 * (harmonic_context - 0.5)   # dissonance → tension
            + 0.30 * velocity_A_vel            # dynamics energy
            + 0.50 * emotional_momentum        # momentum contribution
        )

        # D11: prediction_match — [Huron 2006 ITPRA]
        prediction_match = torch.tanh(
            consonance_period - consonance_std
        )

        # D12: reward_forecast — [Howe 2013 ramping DA]
        # emotional_momentum is tanh-capped [-1,+1], safe from onset transients
        reward_forecast = torch.sigmoid(
            2.0 * (da_caudate - 0.5)        # anticipation signal [-1,+1]
            + 1.0 * emotional_momentum      # energy trajectory [-1,+1]
        )

        # ═══════════════════════════════════════════════════════════
        # AFFECT PATHWAY (6D) — valence/mode circuits
        # ═══════════════════════════════════════════════════════════

        # D14: mode_signal — major/minor detection [Fritz 2009, F(2,39)=15.48]
        # R³ values in [0,1]; H³ coefficient reduced to avoid saturation
        mode_signal = torch.sigmoid(
            3.0 * (consonance_level - 0.50)
            + 2.0 * (brightness - 0.40)
            + 1.5 * (warmth_r3 - 0.50)
            + 0.20 * cons_period_h19
        )

        # D15: consonance_valence — [Koelsch 2006, consonant→VS t=5.1]
        consonance_valence = torch.sigmoid(
            2.5 * (consonance_level - 0.48)
            + 1.5 * (tristimulus1 - 0.60)
            + 0.20 * pleas_mean_h19
            - 0.10 * cons_ambiguity
        )

        # D16: happy_pathway — [Mitterschiffthaler 2007: happy→striatum]
        happy_pathway = torch.sigmoid(
            1.5 * (consonance_valence - 0.5)
            + 1.5 * (mode_signal - 0.5)
            + 0.20 * pleas_val_h20
        )

        # D17: sad_pathway — [Mitterschiffthaler 2007: sad→limbic]
        sad_pathway = torch.sigmoid(
            1.5 * (0.5 - consonance_valence)
            + 1.5 * (0.5 - mode_signal)
            + 0.20 * loud_mean_h19
        )

        # D13: f03_valence — bipolar [Russell 1980 circumplex]
        f03_valence = torch.tanh(
            _ALPHA_H * happy_pathway - _ALPHA_S * sad_pathway
        )

        # D18: emotion_certainty — [Brattico 2011]
        emotion_certainty = torch.sigmoid(
            0.5 * cons_stab_15s
            + 0.5 * warmth_stab_h22
            - 0.5 * cons_ambiguity
        )

        # ═══════════════════════════════════════════════════════════
        # AUTONOMIC PATHWAY (5D) — ANS READOUT of brain state
        # COUPLED with reward: pleasure/da_caudate drive SCR, HR, chills
        # [Salimpoor 2011: DA release ↔ SCR + chills, de Fleurian 2021]
        # ═══════════════════════════════════════════════════════════

        # D19: scr — skin conductance [de Fleurian & Pearce 2021, d=0.85]
        # Reward delivery (pleasure) is the primary SCR driver [Salimpoor 2011]
        scr = torch.sigmoid(
            2.5 * (arousal - 0.5)       # energy activation
            + 2.0 * (pleasure - 0.3)    # reward delivery → SCR spike
            + 0.20 * onset_accel_h9     # transient startle
        )

        # D20: hr — heart rate [Thayer 2009, Salimpoor 2011]
        # Anticipation → HR deceleration (orienting response)
        # High arousal → vagal withdrawal → HR decrease
        hr = torch.sigmoid(
            -2.5 * (arousal - 0.5)      # vagal withdrawal
            - 1.5 * (da_caudate - 0.3)  # anticipation → HR deceleration
            + 0.30 * tempo_signal       # tempo entrainment
            + 0.20 * loud_stab_h19      # stability baseline
        )

        # D21: respr — respiration [Fancourt 2020]
        respr = torch.sigmoid(
            2.5 * (arousal - 0.5)       # high arousal → fast breathing
            + 1.0 * (pleasure - 0.3)    # reward → respiratory change
            + 0.30 * vel_A_h16          # dynamics
        )

        # D22: chills_intensity — [Sloboda 1991, Guhn 2007, Salimpoor 2011]
        # Chills = pleasure × physiological gate. Multiplicative ensures
        # sharp peaks ONLY when reward delivery AND arousal co-occur.
        chills_gate = torch.sigmoid(
            3.0 * (arousal - 0.5)                   # need activation
            + 2.0 * torch.abs(prediction_error)     # unexpectedness amplifies
        )
        chills_intensity = pleasure * chills_gate

        # D23: ans_composite — [Peng 2022 co-activation model]
        ans_composite = torch.tanh(
            0.30 * scr
            + 0.30 * (1.0 - hr)
            + 0.20 * respr
            + 0.10 * pleasure             # reward coupling
            + 0.10 * torch.abs(f03_valence)
        )

        # ═══════════════════════════════════════════════════════════
        # INTEGRATION (2D) — cross-pathway synthesis
        # ═══════════════════════════════════════════════════════════

        # D24: beauty — [Blood & Zatorre 2001: opioid × liking]
        beauty = opioid_proxy * liking

        # D25: emotional_arc — [Sachs 2025: trajectory summary]
        emotional_arc = torch.sigmoid(
            1.5 * emotional_momentum         # [-1,+1] → [-1.5,+1.5]
            + 1.0 * (pleasure - 0.3)         # center around typical
            + 1.0 * f03_valence              # [-1,+1] → [-1,+1]
        )

        # ═══════════════════════════════════════════════════════════
        # ASSEMBLE OUTPUT (B, T, 26)
        # ═══════════════════════════════════════════════════════════

        output = torch.stack([
            # Shared State [0:4]
            arousal, prediction_error, harmonic_context, emotional_momentum,
            # Reward Pathway [4:13]
            da_caudate, da_nacc, opioid_proxy,
            wanting, liking, pleasure,
            tension, prediction_match, reward_forecast,
            # Affect Pathway [13:19]
            f03_valence, mode_signal, consonance_valence,
            happy_pathway, sad_pathway, emotion_certainty,
            # Autonomic Pathway [19:24]
            scr, hr, respr, chills_intensity, ans_composite,
            # Integration [24:26]
            beauty, emotional_arc,
        ], dim=-1)

        return BrainOutput(
            tensor=output,
            dimension_names=self.DIMENSION_NAMES,
            pathway_ranges=self.PATHWAY_RANGES,
        )
