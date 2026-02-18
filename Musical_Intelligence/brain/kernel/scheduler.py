"""C3Kernel — single-pass phase scheduler for C³ v3.1.

Executes the belief cycle per frame:
  Phase 0a: Independent relays (BCH, SNEM, MMP, MPG)
  Phase 0b: Dependent relays with cross-inputs:
              HMCE (+SNEM beat_locked_activity → A1 gain)
              DAED (+BCH consonance_signal → wanting, +MMP familiarity → liking)
          + observe sensory beliefs (consonance, tempo)
  Phase 1:  observe + predict + update salience (attentional gate)
          + multi-feature H³ velocity, mean+max mixing (v2.5)
  Phase 2a: predict all beliefs + observe familiarity (H³ macro stability)
          + multi-scale predict/observe for consonance (v2.0, 8 horizons)
          + multi-scale predict/observe for tempo (v3.1, 6 horizons)
  Phase 2b: compute PE + precision for predictive beliefs
          + per-horizon PE + precision decomposition (v2.1)
  Phase 2c: update beliefs with Bayesian fusion
  Phase 3:  compute reward from multi-scale PEs with per-horizon π (v2.1)
          + horizon activation gating — data-readiness weights (v2.2)
          + surprise-dominant reward weights (v2.5)
          + DAED DA modulation — wanting/liking gain on reward (v3.0)

v3.1: Multi-scale tempo prediction.
  Tempo gets 6-horizon prediction (H5-H21) using onset_strength.
  Per-horizon PE + precision feed into multiscale reward.
  Uniform weights (no ultra horizons → no activation gating needed).

v3.0 Wave 2: Cross-relay pathways + DAED→reward.
  Phase 0 splits into 0a (independent) + 0b (dependent):
    P1: BCH consonance_signal → DAED wanting amplification
    P3: SNEM beat_locked_activity → HMCE A1 encoding gain
    P7: MMP familiarity_level → DAED liking amplification
  DAED → reward: DA gain = 1 + 0.25×(0.6×wanting + 0.4×liking)
  Relay→belief wiring (Wave 1):
    BCH→consonance, HMCE→tempo, SNEM+MPG→salience, MMP→familiarity

Single pass.  No iteration.  No convergence loop.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import torch
from torch import Tensor

from .belief import Belief, BeliefState, Likelihood
from .precision import PrecisionEngine
from .reward import RewardAggregator, RewardConfig
from .relays.bch_wrapper import BCHKernelWrapper
from .relays.hmce_wrapper import HMCEKernelWrapper
from .relays.snem_wrapper import SNEMKernelWrapper
from .relays.mmp_wrapper import MMPKernelWrapper
from .relays.daed_wrapper import DAEDKernelWrapper
from .relays.mpg_wrapper import MPGKernelWrapper
from .relays.base_wrapper import RelayKernelWrapper
from .beliefs.consonance import PerceivedConsonance
from .beliefs.familiarity import FamiliarityState
from .beliefs.salience import SalienceState
from .beliefs.tempo import TempoState
from .beliefs.reward import RewardValence
from ...ear.h3.constants.horizons import FRAME_RATE
from ...ear.r3.registry.feature_map import R3FeatureMap
from .ram import assemble_ram
from .temporal_weights import activated_reward_weights


# ======================================================================
# KernelOutput — what the scheduler produces per frame
# ======================================================================

@dataclass
class KernelOutput:
    """Output of one C³ kernel tick."""
    beliefs: Dict[str, Tensor]           # belief_name → (B, T) posterior
    pe: Dict[str, Tensor]                # belief_name → (B, T) prediction error
    precision_obs: Dict[str, Tensor]     # belief_name → (B, T)
    precision_pred: Dict[str, Tensor]    # belief_name → scalar
    reward: Tensor                        # (B, T) reward_valence
    # v2.0: per-horizon PE decomposition for multi-scale beliefs
    ms_pe: Dict[str, Dict[int, Tensor]] = field(default_factory=dict)
    # v2.1: per-horizon precision for multi-scale beliefs
    ms_precision_pred: Dict[str, Dict[int, Tensor]] = field(default_factory=dict)
    # v3.0: relay wrapper outputs (populated but not yet consumed by beliefs)
    relay_outputs: Dict[str, Any] = field(default_factory=dict)
    # v3.1: Region Activation Map — (B, T, 26) brain region activations
    ram: Optional[Tensor] = None


# ======================================================================
# C3Kernel — the scheduler
# ======================================================================

class C3Kernel:
    """C³ belief-cycle kernel with relay integration.

    v3.0 supports 5 active beliefs + 6 relay wrappers:
      Relays:  BCH (SPU, 3D), HMCE (STU, 6D), SNEM (ASU, 6D),
               MMP (IMU, 6D), DAED (RPU, 4D), MPG (NDU, 3D)
      Active:  perceived_consonance, tempo_state, salience_state,
               familiarity_state, reward_valence

    Wave 2: Cross-relay pathways + DAED→reward modulation:
      Phase 0a: BCH, SNEM, MMP, MPG (independent)
      Phase 0b: HMCE(+SNEM), DAED(+BCH,+MMP) (dependent)
      Relay→belief: BCH→consonance, HMCE→tempo, SNEM+MPG→salience, MMP→familiarity
      DAED→reward: DA gain on reward_valence

    Usage:
        kernel = C3Kernel(feature_map)
        demands = kernel.h3_demands()  # collect for H³ extraction
        for t in range(T):
            output = kernel.tick(r3[:, t:t+1, :], h3_at_t)
    """

    def __init__(
        self,
        feature_map: R3FeatureMap,
    ) -> None:
        self._fm = feature_map

        # Relay wrappers — all in causal (L0-only) mode
        self._bch_wrapper = BCHKernelWrapper()
        self._hmce_wrapper = HMCEKernelWrapper()
        self._snem_wrapper = SNEMKernelWrapper()
        self._mmp_wrapper = MMPKernelWrapper()
        self._daed_wrapper = DAEDKernelWrapper()
        self._mpg_wrapper = MPGKernelWrapper()

        # All relay wrappers (excluding BCH which has its own path)
        self._relay_wrappers: List[RelayKernelWrapper] = [
            self._hmce_wrapper,
            self._snem_wrapper,
            self._mmp_wrapper,
            self._daed_wrapper,
            self._mpg_wrapper,
        ]

        # Instantiate beliefs
        self._consonance = PerceivedConsonance(feature_map)
        self._tempo = TempoState(feature_map)
        self._salience = SalienceState(feature_map)
        self._familiarity = FamiliarityState(feature_map)
        self._reward_belief = RewardValence(feature_map)

        # All beliefs in phase order
        self._beliefs: List[Belief] = [
            self._consonance,    # Phase 0
            self._tempo,         # Phase 0
            self._salience,      # Phase 1
            self._familiarity,   # Phase 2a
            self._reward_belief, # Phase 3
        ]

        # Predictive beliefs (have PE — exclude reward)
        self._predictive: List[Belief] = [
            self._consonance,
            self._tempo,
            self._salience,
            self._familiarity,
        ]

        # Engines
        self._precision = PrecisionEngine()
        self._reward_agg = RewardAggregator()

        # State: previous frame beliefs + PE carry-over for salience
        self._beliefs_prev: Dict[str, Tensor] = {}
        self._prev_pe_mean: Optional[Tensor] = None
        self._frame_count: int = 0

    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """Collect all H³ demands from beliefs and relays.

        Returns the union of:
          - Belief predict demands (with M2 std variants)
          - Multi-scale demands (M0/M18/M2 per horizon, v2.0)
          - BCH L0 demands (deduped)
          - v3.0: 5 relay wrapper L0 demands (HMCE, SNEM, MMP, DAED, MPG)
        """
        demands: Set[Tuple[int, int, int, int]] = set()

        # Belief predict demands + M2 std variants
        for belief in self._predictive:
            for feat_name, h, m, law in belief.h3_predict_demands:
                r3_idx = self._fm.resolve(feat_name)
                demands.add((r3_idx, h, m, law))
                demands.add((r3_idx, h, 2, law))  # M2=std for precision

        # Belief observe demands (stability for familiarity, velocity for salience)
        for belief in self._predictive:
            for feat_name, h, m, law in belief.h3_observe_demands:
                r3_idx = self._fm.resolve(feat_name)
                demands.add((r3_idx, h, m, law))

        # Multi-scale demands (v2.0): M0, M18, M2 per horizon
        for belief in self._predictive:
            for feat_name, h, m, law in belief.multiscale_h3_demands():
                r3_idx = self._fm.resolve(feat_name)
                demands.add((r3_idx, h, m, law))

        # BCH L0 demands (Rule 2: deduplication)
        demands |= self._bch_wrapper.h3_demands

        # v3.0: Relay wrapper L0 demands (auto-deduped via set union)
        for wrapper in self._relay_wrappers:
            demands |= wrapper.h3_demands

        return demands

    def reset(self) -> None:
        """Reset all state for a new piece/session."""
        self._beliefs_prev.clear()
        self._prev_pe_mean = None
        self._precision.reset()
        self._frame_count = 0

    def tick(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> KernelOutput:
        """Execute one frame through the full belief cycle.

        Args:
            r3: R³ features, shape (B, T, 97).
            h3: H³ morphology dict, {(r3_idx, h, m, l): (B, T)}.

        Returns:
            KernelOutput with all belief posteriors, PEs, and reward.
        """
        B = r3.shape[0]
        T = r3.shape[1]
        device = r3.device

        # ── Phase 0a: Independent relays ──────────────────────────────
        bch_out = self._bch_wrapper.compute(r3, h3)
        snem_out = self._snem_wrapper.compute(r3, h3)
        mmp_out = self._mmp_wrapper.compute(r3, h3)
        mpg_out = self._mpg_wrapper.compute(r3, h3)

        # ── Phase 0b: Dependent relays (cross-inputs from 0a) ────────
        # P3: SNEM beat_locked_activity → HMCE A1 encoding gain
        snem_beat = snem_out.beat_locked_activity if snem_out is not None else None
        hmce_out = self._hmce_wrapper.compute(r3, h3, snem_beat=snem_beat)

        # P1+P7: BCH consonance + MMP familiarity → DAED wanting/liking
        bch_cons = bch_out.consonance_signal if bch_out is not None else None
        mmp_fam = mmp_out.familiarity_level if mmp_out is not None else None
        daed_out = self._daed_wrapper.compute(
            r3, h3, bch_consonance=bch_cons, mmp_familiarity=mmp_fam,
        )

        relay_outputs: Dict[str, Any] = {
            "BCH": bch_out,
            "HMCE": hmce_out,
            "SNEM": snem_out,
            "MMP": mmp_out,
            "DAED": daed_out,
            "MPG": mpg_out,
        }

        # ── Phase 0c: Sensory grounding ──────────────────────────────
        cons_likelihood = self._consonance.observe(r3, h3, bch_out=bch_out)
        tempo_likelihood = self._tempo.observe(r3, h3, hmce_out=hmce_out)

        # ── Phase 1: Salience (attentional gate) ──────────────────
        sal_likelihood = self._salience.observe(
            r3, h3,
            prev_pe_mean=self._prev_pe_mean,
            snem_out=snem_out,
            mpg_out=mpg_out,
        )
        sal_predicted = self._salience.predict(self._beliefs_prev, h3)
        sal_predicted = self._broadcast(sal_predicted, B, T, device)
        sal_pe = sal_likelihood.value - sal_predicted
        self._precision.record_pe("salience_state", sal_pe)
        sal_pi_pred = self._precision.estimate_precision_pred(
            "salience_state", self._salience.tau,
        )
        sal_posterior = self._salience.update(
            sal_likelihood, sal_predicted, sal_pi_pred,
        )

        # ── Phase 2a: Predict + Observe familiarity ─────────────────

        # Multi-scale predict/observe for consonance (v2.0)
        cons_ms_predicted = self._consonance.predict_multiscale(
            self._beliefs_prev, h3,
        )
        cons_ms_observed = self._consonance.observe_multiscale(h3)

        # Aggregated prediction for single-belief update
        if cons_ms_predicted:
            cons_predicted = self._consonance.aggregate_prediction(
                cons_ms_predicted,
            )
        else:
            # Fallback to single-scale if multiscale not available
            cons_predicted = self._consonance.predict(self._beliefs_prev, h3)

        # Multi-scale predict/observe for tempo (v3.1)
        tempo_ms_predicted = self._tempo.predict_multiscale(
            self._beliefs_prev, h3,
        )
        tempo_ms_observed = self._tempo.observe_multiscale(h3)

        # Aggregated prediction for single-belief update
        if tempo_ms_predicted:
            tempo_predicted = self._tempo.aggregate_prediction(
                tempo_ms_predicted,
            )
        else:
            tempo_predicted = self._tempo.predict(self._beliefs_prev, h3)

        fam_predicted = self._familiarity.predict(self._beliefs_prev, h3)
        reward_predicted = self._reward_belief.predict(self._beliefs_prev, h3)

        # Familiarity observation (H³ macro stability + MMP recognition)
        fam_likelihood = self._familiarity.observe(r3, h3, mmp_out=mmp_out)

        # Broadcast predictions to match observation shape
        cons_predicted = self._broadcast(cons_predicted, B, T, device)
        tempo_predicted = self._broadcast(tempo_predicted, B, T, device)
        fam_predicted = self._broadcast(fam_predicted, B, T, device)
        reward_predicted = self._broadcast(reward_predicted, B, T, device)

        # ── Phase 2b: Compute PE + precision ────────────────────────

        # Per-horizon PE decomposition for consonance (v2.0)
        cons_ms_pe: Dict[int, Tensor] = {}
        for h in cons_ms_predicted:
            obs_h = cons_ms_observed.get(h)
            pred_h = cons_ms_predicted[h]
            if obs_h is not None and obs_h.dim() >= 2:
                pred_h_bc = self._broadcast(pred_h, B, T, device)
                obs_h_bc = self._broadcast(obs_h, B, T, device)
                cons_ms_pe[h] = obs_h_bc - pred_h_bc

        # Per-horizon precision for consonance (v2.1)
        cons_ms_precision: Dict[int, Tensor] = {}
        for h, pe_h in cons_ms_pe.items():
            self._precision.record_pe_multiscale(
                "perceived_consonance", h, pe_h,
            )
            cons_ms_precision[h] = (
                self._precision.estimate_precision_pred_multiscale(
                    "perceived_consonance", h, self._consonance.tau,
                )
            )

        # Per-horizon PE decomposition for tempo (v3.1)
        tempo_ms_pe: Dict[int, Tensor] = {}
        for h in tempo_ms_predicted:
            obs_h = tempo_ms_observed.get(h)
            pred_h = tempo_ms_predicted[h]
            if obs_h is not None and obs_h.dim() >= 2:
                pred_h_bc = self._broadcast(pred_h, B, T, device)
                obs_h_bc = self._broadcast(obs_h, B, T, device)
                tempo_ms_pe[h] = obs_h_bc - pred_h_bc

        # Per-horizon precision for tempo (v3.1)
        tempo_ms_precision: Dict[int, Tensor] = {}
        for h, pe_h in tempo_ms_pe.items():
            self._precision.record_pe_multiscale(
                "tempo_state", h, pe_h,
            )
            tempo_ms_precision[h] = (
                self._precision.estimate_precision_pred_multiscale(
                    "tempo_state", h, self._tempo.tau,
                )
            )

        # Single-scale PE (BCH obs vs aggregated pred) — for belief update
        cons_pe = cons_likelihood.value - cons_predicted
        tempo_pe = tempo_likelihood.value - tempo_predicted
        fam_pe = fam_likelihood.value - fam_predicted

        self._precision.record_pe("perceived_consonance", cons_pe)
        self._precision.record_pe("tempo_state", tempo_pe)
        self._precision.record_pe("familiarity_state", fam_pe)

        cons_pi_pred = self._precision.estimate_precision_pred(
            "perceived_consonance", self._consonance.tau
        )
        tempo_pi_pred = self._precision.estimate_precision_pred(
            "tempo_state", self._tempo.tau
        )
        fam_pi_pred = self._precision.estimate_precision_pred(
            "familiarity_state", self._familiarity.tau
        )

        # ── Phase 2c: Update beliefs (Bayesian fusion) ──────────────
        cons_posterior = self._consonance.update(
            cons_likelihood, cons_predicted, cons_pi_pred
        )
        tempo_posterior = self._tempo.update(
            tempo_likelihood, tempo_predicted, tempo_pi_pred
        )
        fam_posterior = self._familiarity.update(
            fam_likelihood, fam_predicted, fam_pi_pred
        )

        # ── Phase 3: Reward computation (v3.1: dual multiscale) ────────
        # Consonance: 8-horizon with activation gating (ultra horizons suppressed).
        # Tempo: 6-horizon with uniform weights (no ultra → no gating needed).
        if cons_ms_pe or tempo_ms_pe:
            # Consonance: horizon activation gating (v2.2)
            elapsed_s = self._frame_count / FRAME_RATE
            ms_pe_dict: Dict[str, Dict[int, Tensor]] = {}
            ms_weights: Dict[str, Dict[int, float]] = {}
            ms_prec: Dict[str, Dict[int, Tensor]] = {}

            if cons_ms_pe:
                cons_reward_weights = activated_reward_weights(
                    elapsed_s, tuple(cons_ms_pe.keys()),
                )
                ms_pe_dict["perceived_consonance"] = cons_ms_pe
                ms_weights["perceived_consonance"] = cons_reward_weights
                ms_prec["perceived_consonance"] = cons_ms_precision

            # Tempo: uniform weights (all 6 horizons fill within seconds)
            if tempo_ms_pe:
                n_h = len(tempo_ms_pe)
                tempo_reward_weights = {h: 1.0 / n_h for h in tempo_ms_pe}
                ms_pe_dict["tempo_state"] = tempo_ms_pe
                ms_weights["tempo_state"] = tempo_reward_weights
                ms_prec["tempo_state"] = tempo_ms_precision

            # Single-scale fallback for beliefs not yet on multiscale
            single_pe: Optional[Dict[str, Tensor]] = None
            single_prec: Optional[Dict[str, Tensor]] = None
            if not tempo_ms_pe:
                single_pe = {"tempo_state": tempo_pe}
                single_prec = {"tempo_state": tempo_pi_pred}

            reward_value = self._reward_agg.compute_multiscale(
                ms_pe_dict=ms_pe_dict,
                ms_weights=ms_weights,
                ms_precision_dict=ms_prec,
                precision_pred_dict={
                    "perceived_consonance": cons_pi_pred,
                    "tempo_state": tempo_pi_pred,
                },
                salience=sal_posterior,
                familiarity=fam_posterior,
                single_pe_dict=single_pe,
                single_precision_dict=single_prec,
                daed_out=daed_out,
            )
        else:
            # Fallback: single-scale reward (backward compat)
            reward_value = self._reward_agg.compute(
                {"perceived_consonance": cons_pe, "tempo_state": tempo_pe},
                {"perceived_consonance": cons_pi_pred,
                 "tempo_state": tempo_pi_pred},
                sal_posterior, fam_posterior,
                daed_out=daed_out,
            )

        # Update reward belief with aggregated reward
        reward_likelihood = Likelihood(
            value=reward_value,
            precision=torch.tensor(1.0, device=device),
        )
        reward_pi_pred = self._precision.estimate_precision_pred(
            "reward_valence", self._reward_belief.tau
        )
        reward_posterior = self._reward_belief.update(
            reward_likelihood, reward_predicted, reward_pi_pred,
        )

        # Reward PE (for tracking only)
        reward_pe = reward_value - reward_predicted

        # ── Store state for next frame ──────────────────────────────
        # PE carry-over: mean |PE| of predictive beliefs → salience Phase 1
        # v2.5: include fam_pe — structural boundary surprises boost attention
        self._prev_pe_mean = (
            cons_pe.abs() + tempo_pe.abs() + fam_pe.abs()
        ) / 3.0

        self._beliefs_prev = {
            "perceived_consonance": cons_posterior.detach(),
            "tempo_state": tempo_posterior.detach(),
            "salience_state": sal_posterior.detach(),
            "familiarity_state": fam_posterior.detach(),
            "reward_valence": reward_posterior.detach(),
        }
        self._frame_count += 1

        # ── Region Activation Map (v3.1) ─────────────────────────────
        ram = assemble_ram(relay_outputs, B, T, device)

        # ── Assemble output ─────────────────────────────────────────
        return KernelOutput(
            beliefs={
                "perceived_consonance": cons_posterior,
                "tempo_state": tempo_posterior,
                "salience_state": sal_posterior,
                "familiarity_state": fam_posterior,
                "reward_valence": reward_posterior,
            },
            pe={
                "perceived_consonance": cons_pe,
                "tempo_state": tempo_pe,
                "salience_state": sal_pe,
                "familiarity_state": fam_pe,
                "reward_valence": reward_pe,
            },
            precision_obs={
                "perceived_consonance": cons_likelihood.precision,
                "tempo_state": tempo_likelihood.precision,
                "salience_state": sal_likelihood.precision,
                "familiarity_state": fam_likelihood.precision,
            },
            precision_pred={
                "perceived_consonance": cons_pi_pred,
                "tempo_state": tempo_pi_pred,
                "salience_state": sal_pi_pred,
                "familiarity_state": fam_pi_pred,
                "reward_valence": reward_pi_pred,
            },
            reward=reward_posterior,
            ms_pe={
                **({"perceived_consonance": cons_ms_pe} if cons_ms_pe else {}),
                **({"tempo_state": tempo_ms_pe} if tempo_ms_pe else {}),
            },
            ms_precision_pred={
                **({"perceived_consonance": cons_ms_precision} if cons_ms_precision else {}),
                **({"tempo_state": tempo_ms_precision} if tempo_ms_precision else {}),
            },
            relay_outputs=relay_outputs,
            ram=ram,
        )

    @staticmethod
    def _broadcast(t: Tensor, B: int, T: int, device: torch.device) -> Tensor:
        """Broadcast a scalar or small tensor to (B, T)."""
        if t.shape == (B, T):
            return t
        return t.expand(B, T).to(device)
