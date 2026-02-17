"""C3Kernel — single-pass phase scheduler for C³ v2.1.

Executes the belief cycle per frame:
  Phase 0:  BCH relay → observe sensory beliefs (consonance, tempo)
  Phase 1:  observe + predict + update salience (attentional gate)
  Phase 2a: predict all beliefs + observe familiarity (H³ macro stability)
          + multi-scale predict/observe for consonance (v2.0)
  Phase 2b: compute PE + precision for predictive beliefs
          + per-horizon PE + precision decomposition (v2.1)
  Phase 2c: update beliefs with Bayesian fusion
  Phase 3:  compute reward from multi-scale PEs with per-horizon π (v2.1)

Single pass.  No iteration.  No convergence loop.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

import torch
from torch import Tensor

from .belief import Belief, BeliefState, Likelihood
from .precision import PrecisionEngine
from .reward import RewardAggregator, RewardConfig
from .relays.bch_wrapper import BCHKernelWrapper
from .beliefs.consonance import PerceivedConsonance
from .beliefs.familiarity import FamiliarityState
from .beliefs.salience import SalienceState
from .beliefs.tempo import TempoState
from .beliefs.reward import RewardValence
from ...ear.r3.registry.feature_map import R3FeatureMap


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


# ======================================================================
# C3Kernel — the scheduler
# ======================================================================

class C3Kernel:
    """Minimal C³ belief-cycle kernel.

    v1.1 supports 5 active beliefs + BCH relay:
      Relay:   BCH (causal L0-only, 3 approved outputs)
      Active:  perceived_consonance, tempo_state, salience_state,
               familiarity_state, reward_valence

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

        # Relay wrapper — BCH in causal (L0-only) mode
        self._bch_wrapper = BCHKernelWrapper()

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

        # ── Phase 0: BCH relay + Sensory grounding ────────────────
        bch_out = self._bch_wrapper.compute(r3, h3)
        cons_likelihood = self._consonance.observe(r3, h3, bch_out=bch_out)
        tempo_likelihood = self._tempo.observe(r3, h3)

        # ── Phase 1: Salience (attentional gate) ──────────────────
        sal_likelihood = self._salience.observe(
            r3, h3, prev_pe_mean=self._prev_pe_mean,
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

        tempo_predicted = self._tempo.predict(self._beliefs_prev, h3)
        fam_predicted = self._familiarity.predict(self._beliefs_prev, h3)
        reward_predicted = self._reward_belief.predict(self._beliefs_prev, h3)

        # Familiarity observation (H³ macro stability)
        fam_likelihood = self._familiarity.observe(r3, h3)

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

        # ── Phase 3: Reward computation (v2.1: per-horizon precision) ──
        # Consonance uses multi-scale PE + per-horizon precision.
        # Tempo uses single-scale PE (will be upgraded later).
        if cons_ms_pe:
            # Uniform horizon weights for reward (all scales matter equally)
            n_h = len(cons_ms_pe)
            cons_reward_weights = {h: 1.0 / n_h for h in cons_ms_pe}

            reward_value = self._reward_agg.compute_multiscale(
                ms_pe_dict={"perceived_consonance": cons_ms_pe},
                ms_weights={"perceived_consonance": cons_reward_weights},
                ms_precision_dict={"perceived_consonance": cons_ms_precision},
                precision_pred_dict={
                    "perceived_consonance": cons_pi_pred,
                    "tempo_state": tempo_pi_pred,
                },
                salience=sal_posterior,
                familiarity=fam_posterior,
                single_pe_dict={"tempo_state": tempo_pe},
                single_precision_dict={"tempo_state": tempo_pi_pred},
            )
        else:
            # Fallback: single-scale reward (backward compat)
            reward_value = self._reward_agg.compute(
                {"perceived_consonance": cons_pe, "tempo_state": tempo_pe},
                {"perceived_consonance": cons_pi_pred,
                 "tempo_state": tempo_pi_pred},
                sal_posterior, fam_posterior,
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
        # PE carry-over: mean |PE| of sensory beliefs → salience Phase 1
        self._prev_pe_mean = (cons_pe.abs() + tempo_pe.abs()) / 2.0

        self._beliefs_prev = {
            "perceived_consonance": cons_posterior.detach(),
            "tempo_state": tempo_posterior.detach(),
            "salience_state": sal_posterior.detach(),
            "familiarity_state": fam_posterior.detach(),
            "reward_valence": reward_posterior.detach(),
        }
        self._frame_count += 1

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
            ms_pe={"perceived_consonance": cons_ms_pe} if cons_ms_pe else {},
            ms_precision_pred=(
                {"perceived_consonance": cons_ms_precision}
                if cons_ms_precision else {}
            ),
        )

    @staticmethod
    def _broadcast(t: Tensor, B: int, T: int, device: torch.device) -> Tensor:
        """Broadcast a scalar or small tensor to (B, T)."""
        if t.shape == (B, T):
            return t
        return t.expand(B, T).to(device)
