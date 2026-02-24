/* ── M³ Store — The Personal Musical Mind ─────────────────────────
 *  Persistent Zustand store managing M³ state, growth, and parameters.
 *  C³ = frozen physics. M³ = learnable individual weights.
 *  ──────────────────────────────────────────────────────────────── */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
  M3Mind,
  M3Milestone,
  M3Stage,
  M3Temperament,
  M3Tier,
  M3Parameters,
  M3TrackSignal,
  PresentationLayer,
} from "@/types/m3";
import { M3_STAGE_ORDER } from "@/types/m3";
import { M3_STAGES, M3_TEMPERAMENTS, getNextStage, getNextThreshold } from "@/data/m3-stages";

/* ── Parameter Initialization ────────────────────────────────────── */

/** Create a fresh parameter set with small random values + temperament bias */
function initParameters(temperament: M3Temperament): M3Parameters {
  const bias = M3_TEMPERAMENTS[temperament].paramBias;
  const rand = (n: number, scale: number) =>
    Array.from({ length: n }, () => (Math.random() * 0.1 - 0.05) * scale);

  return {
    beliefPriors:       rand(131, 1.0),
    precisionWeights:   rand(131, bias.precision),
    rewardWeights:      rand(131, bias.reward),
    predictionCoeffs:   rand(524, 1.0),
    attentionBiases:    rand(131, bias.attention),
    temporalPrefs:      rand(50,  bias.temporal),
    timbralMap:         rand(97,  bias.timbral),
    crossCorrelations:  rand(100, 1.0),
  };
}

/* ── Growth Engine ───────────────────────────────────────────────── */

/**
 * Compute how much a single listen contributes to M³ growth.
 * Signal strength: duration > repeat > skip (negative) > diversity
 */
function computeGrowthDelta(signal: M3TrackSignal): number {
  let delta = 0.01; // base per listen

  // Duration boost (longer = more signal)
  if (signal.duration > 180) delta += 0.005;
  if (signal.duration > 300) delta += 0.005;

  // Repeat = strong positive signal
  if (signal.isRepeat) delta += 0.003;

  // Skip = weak/negative signal
  if (signal.wasSkipped) delta -= 0.005;

  // High energy / high complexity = more engagement
  delta += signal.energy * 0.002;
  delta += signal.harmonicComplexity * 0.002;

  return Math.max(0.001, delta); // Always at least tiny growth
}

/**
 * Update M³ parameters based on a track signal.
 * Parameters shift slightly toward the track's characteristics.
 * This is the "convince the system" mechanism.
 */
function updateParameters(params: M3Parameters, signal: M3TrackSignal): M3Parameters {
  const lr = 0.02; // Learning rate — slow deliberate change
  const signalStrength = signal.wasSkipped ? 0.3 : signal.isRepeat ? 1.5 : 1.0;
  const rate = lr * signalStrength;

  // Shift reward weights based on valence/energy
  const newReward = params.rewardWeights.map((w, i) => {
    const nudge = (signal.valence * 0.5 + signal.energy * 0.5) * rate * (((i * 7 + 13) % 131) / 131);
    return w + nudge;
  });

  // Shift temporal prefs based on tempo
  const tempoNorm = signal.tempo / 200; // Normalize BPM to ~0-1
  const newTemporal = params.temporalPrefs.map((w, i) => {
    const nudge = (tempoNorm - 0.5) * rate * (((i * 3 + 7) % 50) / 50);
    return w + nudge;
  });

  // Shift timbral map based on brightness/acousticness
  const newTimbral = params.timbralMap.map((w, i) => {
    const nudge = (signal.timbralBrightness * 0.5 + (1 - signal.acousticness) * 0.5) * rate * (((i * 11 + 3) % 97) / 97);
    return w + nudge;
  });

  // Shift precision weights based on harmonic complexity
  const newPrecision = params.precisionWeights.map((w, i) => {
    const nudge = signal.harmonicComplexity * rate * 0.5 * (((i * 5 + 9) % 131) / 131);
    return w + nudge;
  });

  // Shift attention biases based on danceability
  const newAttention = params.attentionBiases.map((w, i) => {
    const nudge = (signal.danceability - 0.5) * rate * (((i * 13 + 1) % 131) / 131);
    return w + nudge;
  });

  return {
    ...params,
    rewardWeights: newReward,
    temporalPrefs: newTemporal,
    timbralMap: newTimbral,
    precisionWeights: newPrecision,
    attentionBiases: newAttention,
  };
}

/* ── Store Interface ─────────────────────────────────────────────── */

interface M3StoreState {
  /* Core state */
  mind: M3Mind | null;
  milestones: M3Milestone[];
  preferredLayer: PresentationLayer;

  /* Actions */
  birthM3: (temperament: M3Temperament, tier: M3Tier) => void;
  feedListening: (signal: M3TrackSignal) => M3Milestone[];
  setTier: (tier: M3Tier) => void;
  setPreferredLayer: (layer: PresentationLayer) => void;
  resetM3: () => void;
}

const INITIAL_STATE = {
  mind: null as M3Mind | null,
  milestones: [] as M3Milestone[],
  preferredLayer: "surface" as PresentationLayer,
};

/* ── Store Implementation ────────────────────────────────────────── */

export const useM3Store = create<M3StoreState>()(
  persist(
    (set, get) => ({
      ...INITIAL_STATE,

      birthM3: (temperament, tier) => {
        const now = new Date().toISOString();
        const isFree = tier === "free";
        const params = initParameters(temperament);
        const stage: M3Stage = "seed";
        const functions = M3_STAGES[stage].functions;

        const mind: M3Mind = {
          stage,
          temperament,
          tier,
          bornAt: now,
          lastUpdated: null,
          totalListens: 0,
          parameters: params,
          activeFunctions: [...functions],
          stageProgress: 0,
          frozen: isFree,
        };

        const milestone: M3Milestone = {
          type: "birth",
          timestamp: now,
          stage: "seed",
          detail: `Born as ${temperament} — ${isFree ? "frozen (free tier)" : "growing"}`,
        };

        set({ mind, milestones: [milestone] });
      },

      feedListening: (signal) => {
        const { mind, milestones } = get();
        if (!mind || mind.frozen) return [];

        const now = new Date().toISOString();
        const newMilestones: M3Milestone[] = [];

        // Update parameters
        const updatedParams = updateParameters(mind.parameters, signal);
        const growthDelta = computeGrowthDelta(signal);
        const newListens = mind.totalListens + 1;

        // Compute stage progress
        const nextThreshold = getNextThreshold(mind.stage);
        const currentThreshold = M3_STAGES[mind.stage].threshold;
        const range = nextThreshold - currentThreshold;
        const newProgress = range > 0
          ? Math.min(1, (newListens - currentThreshold) / range)
          : 1;

        // Check stage transition
        let newStage = mind.stage;
        let newFunctions = [...mind.activeFunctions];
        let adjustedProgress = newProgress;

        if (newProgress >= 1) {
          const next = getNextStage(mind.stage);
          if (next) {
            newStage = next;
            newFunctions = [...M3_STAGES[next].functions];
            adjustedProgress = 0;

            newMilestones.push({
              type: "stage_up",
              timestamp: now,
              stage: next,
              detail: `Evolved to ${next}`,
            });

            // Check for newly unlocked functions
            const prevFunctions = M3_STAGES[mind.stage].functions;
            const unlocked = newFunctions.filter(f => !prevFunctions.includes(f));
            for (const fn of unlocked) {
              newMilestones.push({
                type: "function_unlock",
                timestamp: now,
                detail: `F${fn} awakened`,
              });
            }
          }
        }

        const updatedMind: M3Mind = {
          ...mind,
          parameters: updatedParams,
          totalListens: newListens,
          stage: newStage,
          activeFunctions: newFunctions,
          stageProgress: adjustedProgress,
          lastUpdated: now,
        };

        set({
          mind: updatedMind,
          milestones: [...milestones, ...newMilestones],
        });

        return newMilestones;
      },

      setTier: (tier) => {
        const { mind, milestones } = get();
        if (!mind) return;

        const wasFrozen = mind.frozen;
        const isFree = tier === "free";
        const now = new Date().toISOString();

        const updatedMind: M3Mind = {
          ...mind,
          tier,
          frozen: isFree,
        };

        const newMilestones = [...milestones];
        if (wasFrozen && !isFree) {
          newMilestones.push({
            type: "insight",
            timestamp: now,
            detail: `Upgraded to ${tier} — M³ unfrozen`,
          });
        }

        set({ mind: updatedMind, milestones: newMilestones });
      },

      setPreferredLayer: (layer) => set({ preferredLayer: layer }),

      resetM3: () => set(INITIAL_STATE),
    }),
    {
      name: "m3-mind-store",
      partialize: (state) => ({
        mind: state.mind,
        milestones: state.milestones,
        preferredLayer: state.preferredLayer,
      }),
    },
  ),
);
