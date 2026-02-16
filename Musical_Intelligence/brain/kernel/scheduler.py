"""C3Kernel — single-pass phase scheduler for C³ v1.0.

Executes the belief cycle per frame:
  Phase 0:  BCH relay → observe + update sensory beliefs (consonance, tempo)
  Phase 1:  observe + update salience (default 1.0 if not active)
  Phase 2a: predict all beliefs + observe familiarity (default 0.5)
  Phase 2b: compute PE + precision for predictive beliefs
  Phase 2c: update beliefs with Bayesian fusion
  Phase 3:  compute reward from PEs

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


# ======================================================================
# C3Kernel — the scheduler
# ======================================================================

class C3Kernel:
    """Minimal C³ belief-cycle kernel.

    v1.0 supports 3 active beliefs + 2 defaults + BCH relay:
      Relay:   BCH (causal L0-only, 3 approved outputs)
      Active:  perceived_consonance, tempo_state, reward_valence
      Default: salience_state=1.0, familiarity_state=0.5

    Usage:
        kernel = C3Kernel(feature_map)
        demands = kernel.h3_demands()  # collect for H³ extraction
        for t in range(T):
            output = kernel.tick(r3[:, t:t+1, :], h3_at_t)
    """

    def __init__(
        self,
        feature_map: R3FeatureMap,
        *,
        default_salience: float = 1.0,
        default_familiarity: float = 0.5,
    ) -> None:
        self._fm = feature_map

        # Relay wrapper — BCH in causal (L0-only) mode
        self._bch_wrapper = BCHKernelWrapper()

        # Instantiate beliefs
        self._consonance = PerceivedConsonance(feature_map)
        self._tempo = TempoState(feature_map)
        self._reward_belief = RewardValence(feature_map)

        # All beliefs in phase order
        self._beliefs: List[Belief] = [
            self._consonance,   # Phase 0
            self._tempo,        # Phase 0
            self._reward_belief, # Phase 3
        ]

        # Predictive beliefs (have PE — exclude reward)
        self._predictive: List[Belief] = [
            self._consonance,
            self._tempo,
        ]

        # Engines
        self._precision = PrecisionEngine()
        self._reward_agg = RewardAggregator()

        # Defaults for inactive beliefs
        self._default_salience = default_salience
        self._default_familiarity = default_familiarity

        # State: previous frame beliefs
        self._beliefs_prev: Dict[str, Tensor] = {}
        self._frame_count: int = 0

    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """Collect all H³ demands from beliefs and relays.

        Returns the union of:
          - Belief predict demands (with M2 std variants)
          - BCH L0 demands (deduped)
        """
        demands: Set[Tuple[int, int, int, int]] = set()

        # Belief predict demands + M2 std variants
        for belief in self._predictive:
            for feat_name, h, m, law in belief.h3_predict_demands:
                r3_idx = self._fm.resolve(feat_name)
                demands.add((r3_idx, h, m, law))
                demands.add((r3_idx, h, 2, law))  # M2=std for precision

        # BCH L0 demands (Rule 2: deduplication)
        demands |= self._bch_wrapper.h3_demands

        return demands

    def reset(self) -> None:
        """Reset all state for a new piece/session."""
        self._beliefs_prev.clear()
        self._precision.reset()
        self._frame_count = 0

    def tick(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> KernelOutput:
        """Execute one frame through the full belief cycle.

        Args:
            r3: R³ features, shape (B, T, 128).
            h3: H³ morphology dict, {(r3_idx, h, m, l): (B, T)}.

        Returns:
            KernelOutput with all belief posteriors, PEs, and reward.
        """
        B = r3.shape[0]
        T = r3.shape[1]
        device = r3.device

        # Default beliefs for inactive units
        salience = torch.full((B, T), self._default_salience, device=device)
        familiarity = torch.full((B, T), self._default_familiarity, device=device)

        # ── Phase 0: BCH relay + Sensory grounding ────────────────
        bch_out = self._bch_wrapper.compute(r3, h3)
        cons_likelihood = self._consonance.observe(r3, h3, bch_out=bch_out)
        tempo_likelihood = self._tempo.observe(r3, h3)

        # ── Phase 2a: Predict all beliefs (reads beliefs_{t-1}) ─────
        cons_predicted = self._consonance.predict(self._beliefs_prev, h3)
        tempo_predicted = self._tempo.predict(self._beliefs_prev, h3)
        reward_predicted = self._reward_belief.predict(self._beliefs_prev, h3)

        # Broadcast predictions to match observation shape
        cons_predicted = self._broadcast(cons_predicted, B, T, device)
        tempo_predicted = self._broadcast(tempo_predicted, B, T, device)
        reward_predicted = self._broadcast(reward_predicted, B, T, device)

        # ── Phase 2b: Compute PE + precision ────────────────────────
        cons_pe = cons_likelihood.value - cons_predicted
        tempo_pe = tempo_likelihood.value - tempo_predicted

        self._precision.record_pe("perceived_consonance", cons_pe)
        self._precision.record_pe("tempo_state", tempo_pe)

        cons_pi_pred = self._precision.estimate_precision_pred(
            "perceived_consonance", self._consonance.tau
        )
        tempo_pi_pred = self._precision.estimate_precision_pred(
            "tempo_state", self._tempo.tau
        )

        # ── Phase 2c: Update beliefs (Bayesian fusion) ──────────────
        cons_posterior = self._consonance.update(
            cons_likelihood, cons_predicted, cons_pi_pred
        )
        tempo_posterior = self._tempo.update(
            tempo_likelihood, tempo_predicted, tempo_pi_pred
        )

        # ── Phase 3: Reward computation ─────────────────────────────
        pe_dict = {
            "perceived_consonance": cons_pe,
            "tempo_state": tempo_pe,
        }
        pi_pred_dict = {
            "perceived_consonance": cons_pi_pred,
            "tempo_state": tempo_pi_pred,
        }

        reward_value = self._reward_agg.compute(
            pe_dict, pi_pred_dict, salience, familiarity,
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

        # ── Store beliefs for next frame ────────────────────────────
        self._beliefs_prev = {
            "perceived_consonance": cons_posterior.detach(),
            "tempo_state": tempo_posterior.detach(),
            "salience_state": salience.detach(),
            "familiarity_state": familiarity.detach(),
            "reward_valence": reward_posterior.detach(),
        }
        self._frame_count += 1

        # ── Assemble output ─────────────────────────────────────────
        return KernelOutput(
            beliefs={
                "perceived_consonance": cons_posterior,
                "tempo_state": tempo_posterior,
                "salience_state": salience,
                "familiarity_state": familiarity,
                "reward_valence": reward_posterior,
            },
            pe={
                "perceived_consonance": cons_pe,
                "tempo_state": tempo_pe,
                "reward_valence": reward_pe,
            },
            precision_obs={
                "perceived_consonance": cons_likelihood.precision,
                "tempo_state": tempo_likelihood.precision,
            },
            precision_pred={
                "perceived_consonance": cons_pi_pred,
                "tempo_state": tempo_pi_pred,
                "reward_valence": reward_pi_pred,
            },
            reward=reward_posterior,
        )

    @staticmethod
    def _broadcast(t: Tensor, B: int, T: int, device: torch.device) -> Tensor:
        """Broadcast a scalar or small tensor to (B, T)."""
        if t.shape == (B, T):
            return t
        return t.expand(B, T).to(device)
