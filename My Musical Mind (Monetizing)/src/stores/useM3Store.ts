/* ── M³ Store — Unified Personal Musical Mind ──────────────────────
 *  M³ growth IS persona evolution. Each learning session updates:
 *  - All 5 mind genes (Entropy, Resolution, Tension, Resonance, Plasticity)
 *  - Level progression (1-12, human growth stages)
 *  - Active persona derivation (from genes)
 *  - Type change detection (with animation trigger)
 *  ──────────────────────────────────────────────────────────────── */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
  M3Mind,
  M3Milestone,
  M3Stage,
  M3Tier,
  M3Parameters,
  M3TrackSignal,
  PresentationLayer,
  PersonaLevel,
  MindGenes,
  GeneName,
} from "@/types/m3";
import {
  LEVEL_THRESHOLDS,
  levelToStage,
  DEFAULT_GENES,
  GENE_NAMES,
  GENE_TO_TYPE,
  TYPE_TO_GENE,
  getDominantType,
} from "@/types/m3";
import type { NeuralFamily } from "@/types/mind";
import type { Persona } from "@/types/mind";
import { personas } from "@/data/personas";
import { M3_STAGES } from "@/data/m3-stages";
import { GENE_PARAM_BIASES } from "@/data/m3-stages";

/* ── Parameter Initialization ────────────────────────────────────── */

/** Create fresh parameters biased by the birth persona's dominant gene */
function initParameters(dominantGene: GeneName): M3Parameters {
  const bias = GENE_PARAM_BIASES[dominantGene];
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

/* ── Gene Engine ───────────────────────────────────────────────────── */

const GENE_DECAY = 0.995;
const GENE_LR = 0.02;

/** Calculate how much a track contributes to each gene */
function calculateGeneContribution(signal: M3TrackSignal): MindGenes {
  const { energy, valence, tempo, danceability, acousticness, harmonicComplexity } = signal;
  const tempoNorm = Math.min(1, tempo / 200);

  return {
    entropy:
      (1 - acousticness) * 0.25 + energy * 0.15 +
      danceability * 0.15 + Math.random() * 0.1 +
      (tempoNorm > 0.6 ? 0.15 : 0.05) + harmonicComplexity * 0.1,

    resolution:
      (1 - energy) * 0.25 + acousticness * 0.25 +
      harmonicComplexity * 0.2 +
      (1 - Math.abs(valence - 0.5) * 2) * 0.2 +
      (tempoNorm < 0.5 ? 0.1 : 0),

    tension:
      energy * 0.2 + (1 - valence) * 0.15 +
      Math.abs(energy - 0.5) * 2 * 0.25 +
      harmonicComplexity * 0.15 +
      (tempoNorm > 0.5 ? 0.15 : 0.05),

    resonance:
      valence * 0.15 + acousticness * 0.25 +
      (1 - energy) * 0.2 +
      (tempoNorm < 0.45 ? 0.2 : 0.1) + 0.05,

    plasticity:
      danceability * 0.3 + energy * 0.2 +
      (tempoNorm > 0.55 ? 0.2 : 0.1) +
      (1 - acousticness) * 0.1 +
      (1 - Math.abs(valence - 0.5) * 2) * 0.1,
  };
}

/** Update genes with EMA */
function updateGenes(current: MindGenes, contribution: MindGenes): MindGenes {
  const result: Record<string, number> = {};
  for (const g of GENE_NAMES) {
    result[g] = current[g] * GENE_DECAY + contribution[g] * GENE_LR;
  }
  return result as unknown as MindGenes;
}

/* ── Persona Derivation ──────────────────────────────────────────── */

/** Normalized Euclidean distance between two gene profiles [0,1] */
function geneDistance(a: MindGenes, b: MindGenes): number {
  let d = 0;
  for (const g of GENE_NAMES) {
    d += (a[g] - b[g]) ** 2;
  }
  return Math.sqrt(d) / Math.sqrt(5);
}

/** Derive the best-matching persona from genes (gene-to-gene matching) */
function derivePersona(genes: MindGenes): number {
  let bestId = 1;
  let bestScore = -Infinity;

  for (const p of personas) {
    // Direct gene-to-gene similarity
    const geneSim = 1 - geneDistance(genes, p.genes);

    // Family alignment bonus
    const dominantGene = TYPE_TO_GENE[p.family];
    const familyBonus = genes[dominantGene];

    const score = geneSim * 0.85 + familyBonus * 0.15;
    if (score > bestScore) {
      bestScore = score;
      bestId = p.id;
    }
  }
  return bestId;
}

/* ── Level / Stage Computation ───────────────────────────────────── */

function deriveLevel(totalListens: number): PersonaLevel {
  let level: PersonaLevel = 1;
  for (let l = 12; l >= 1; l--) {
    if (totalListens >= LEVEL_THRESHOLDS[l as PersonaLevel]) {
      level = l as PersonaLevel;
      break;
    }
  }
  return level;
}

function computeLevelProgress(totalListens: number, currentLevel: PersonaLevel): number {
  if (currentLevel >= 12) return 1;
  const nextLevel = (currentLevel + 1) as PersonaLevel;
  const currentThreshold = LEVEL_THRESHOLDS[currentLevel];
  const nextThreshold = LEVEL_THRESHOLDS[nextLevel];
  const range = nextThreshold - currentThreshold;
  return range > 0 ? Math.min(1, (totalListens - currentThreshold) / range) : 1;
}

/* ── Parameter Update ──────────────────────────────────────────── */

function updateParameters(params: M3Parameters, signal: M3TrackSignal): M3Parameters {
  const lr = 0.02;
  const signalStrength = signal.wasSkipped ? 0.3 : signal.isRepeat ? 1.5 : 1.0;
  const rate = lr * signalStrength;

  const newReward = params.rewardWeights.map((w, i) => {
    const nudge = (signal.valence * 0.5 + signal.energy * 0.5) * rate * (((i * 7 + 13) % 131) / 131);
    return w + nudge;
  });

  const tempoNorm = signal.tempo / 200;
  const newTemporal = params.temporalPrefs.map((w, i) => {
    const nudge = (tempoNorm - 0.5) * rate * (((i * 3 + 7) % 50) / 50);
    return w + nudge;
  });

  const newTimbral = params.timbralMap.map((w, i) => {
    const nudge = (signal.timbralBrightness * 0.5 + (1 - signal.acousticness) * 0.5) * rate * (((i * 11 + 3) % 97) / 97);
    return w + nudge;
  });

  const newPrecision = params.precisionWeights.map((w, i) => {
    const nudge = signal.harmonicComplexity * rate * 0.5 * (((i * 5 + 9) % 131) / 131);
    return w + nudge;
  });

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
  mind: M3Mind | null;
  milestones: M3Milestone[];
  preferredLayer: PresentationLayer;

  /** Birth M³ from a persona */
  birthM3: (persona: Persona, tier: M3Tier) => void;
  /** Learn from a track signal — updates all 5 genes, level, persona */
  learnFromListening: (signal: M3TrackSignal) => M3Milestone[];
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

      birthM3: (persona, tier) => {
        const now = new Date().toISOString();
        const isFree = tier === "free";
        const dominantGene = TYPE_TO_GENE[persona.family];

        // Use the persona's canonical gene profile as starting point
        const genes: MindGenes = { ...persona.genes };

        const params = initParameters(dominantGene);
        const stage: M3Stage = "embryo";
        const functions = M3_STAGES[stage].functions;

        const mind: M3Mind = {
          stage,
          level: 1,
          stageProgress: 0,
          totalListens: 0,
          totalMinutes: 0,
          genes,
          activePersonaId: persona.id,
          previousPersonaIds: [],
          parameters: params,
          activeFunctions: [...functions],
          tier,
          frozen: isFree,
          bornAt: now,
          lastUpdated: null,
        };

        const milestone: M3Milestone = {
          type: "birth",
          timestamp: now,
          stage: "embryo",
          level: 1,
          detail: `Born as ${persona.name} (${persona.family})`,
        };

        set({ mind, milestones: [milestone] });
      },

      learnFromListening: (signal) => {
        const { mind, milestones } = get();
        if (!mind || mind.frozen) return [];

        const now = new Date().toISOString();
        const newMilestones: M3Milestone[] = [];

        // 0. Detect old Mind Type BEFORE gene update
        const oldType = getDominantType(mind.genes);

        // 1. Update all 5 genes
        const contribution = calculateGeneContribution(signal);
        const newGenes = updateGenes(mind.genes, contribution);

        // 2. Detect Mind Type change
        const newType = getDominantType(newGenes);
        if (newType !== oldType) {
          newMilestones.push({
            type: "type_change",
            timestamp: now,
            fromType: oldType,
            toType: newType,
            detail: `Mind type shifted from ${oldType} to ${newType}`,
          });
        }

        // 3. Update M³ parameters
        const newParams = updateParameters(mind.parameters, signal);

        // 4. Increment listen count + minutes
        const newListens = mind.totalListens + 1;
        const newMinutes = mind.totalMinutes + Math.round(signal.duration / 60);

        // 5. Check level-up (1→12)
        const newLevel = deriveLevel(newListens);
        const leveledUp = newLevel > mind.level;
        if (leveledUp) {
          newMilestones.push({
            type: "level_up",
            timestamp: now,
            level: newLevel,
            detail: `Reached level ${newLevel}`,
          });
        }

        // 6. Derive stage from level
        const newStage = levelToStage(newLevel);
        const stageChanged = newStage !== mind.stage;
        if (stageChanged) {
          newMilestones.push({
            type: "stage_up",
            timestamp: now,
            stage: newStage,
            detail: `Evolved to ${newStage}`,
          });

          const prevFunctions = M3_STAGES[mind.stage].functions;
          const newFunctions = M3_STAGES[newStage].functions;
          const unlocked = newFunctions.filter(f => !prevFunctions.includes(f));
          for (const fn of unlocked) {
            newMilestones.push({
              type: "function_unlock",
              timestamp: now,
              detail: `F${fn} awakened`,
            });
          }
        }

        // 7. Derive active persona from genes
        const newPersonaId = derivePersona(newGenes);
        const personaShifted = newPersonaId !== mind.activePersonaId;
        if (personaShifted) {
          newMilestones.push({
            type: "persona_shift",
            timestamp: now,
            fromPersonaId: mind.activePersonaId,
            toPersonaId: newPersonaId,
            detail: `Persona shifted to ${personas.find(p => p.id === newPersonaId)?.name ?? "unknown"}`,
          });
        }

        // 8. Compute progress toward next level
        const newProgress = computeLevelProgress(newListens, newLevel);

        const updatedMind: M3Mind = {
          ...mind,
          genes: newGenes,
          parameters: newParams,
          totalListens: newListens,
          totalMinutes: newMinutes,
          level: newLevel,
          stage: newStage,
          activeFunctions: [...M3_STAGES[newStage].functions],
          activePersonaId: personaShifted ? newPersonaId : mind.activePersonaId,
          previousPersonaIds: personaShifted
            ? [...mind.previousPersonaIds, mind.activePersonaId]
            : mind.previousPersonaIds,
          stageProgress: newProgress,
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

        const updatedMind: M3Mind = { ...mind, tier, frozen: isFree };

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
      merge: (persisted, current) => {
        const p = persisted as Partial<M3StoreState>;
        if (p?.mind) {
          // Migrate stale familyAffinity → genes
          const m = p.mind as unknown as Record<string, unknown>;
          if (!m.genes && m.familyAffinity) {
            const fa = m.familyAffinity as Record<string, number>;
            m.genes = {
              entropy: fa.Explorers ?? 0.2,
              resolution: fa.Architects ?? 0.2,
              tension: fa.Alchemists ?? 0.2,
              resonance: fa.Anchors ?? 0.2,
              plasticity: fa.Kineticists ?? 0.2,
            };
            delete m.familyAffinity;
            delete m.axes;
          }
          if (!m.genes) {
            m.genes = { ...DEFAULT_GENES };
          }
          if (!m.previousPersonaIds) {
            m.previousPersonaIds = [];
          }
          // Migrate old stage names
          const stageMap: Record<string, string> = {
            seed: "embryo", sprout: "newborn", sapling: "infant",
            branch: "toddler", bloom: "child", canopy: "adolescent", ancient: "adult",
          };
          if (typeof m.stage === "string" && stageMap[m.stage]) {
            m.stage = stageMap[m.stage];
          }
        }
        return { ...(current as M3StoreState), ...p } as M3StoreState;
      },
    },
  ),
);
