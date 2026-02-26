/* ── M³ Observation Engine ──────────────────────────────────────────
 *  Generates observations following the "observe, don't judge" policy.
 *  M³ NEVER says "you are X". It describes its own state or reports data.
 *
 *  9 observation types, stage-gated by persona level:
 *   L2+ mood_landscape, L3+ daily_reflection, L5+ pattern_discovery,
 *   L5+ music_recommendation, L7+ predictive_insight, L7+ therapeutic,
 *   L9+ musical_counseling, L9+ cross_m3, L11+ meta_awareness
 *
 *  Each observation has all 3 layers: surface / narrative / deep.
 *  ──────────────────────────────────────────────────────────────────── */

import type { TFunction } from "i18next";
import type {
  M3Mind,
  M3Observation,
  PresentationLayer,
  ObservationType,
  PersonaLevel,
  MindGenes,
} from "../types/m3";
import { OBSERVATION_LEVEL_GATE, GENE_NAMES, GENE_TO_TYPE, getDominantType } from "../types/m3";
import { personas } from "./personas";

/* ── Helpers ───────────────────────────────────────────────────────── */

/** Mean absolute value of parameter array */
function paramMean(arr: number[]): number {
  if (arr.length === 0) return 0;
  return arr.reduce((s, v) => s + Math.abs(v), 0) / arr.length;
}

/** Pick a deterministic "mood" based on reward + timbral state */
function computeMood(mind: M3Mind): "calm" | "restless" | "bright" | "dark" | "searching" {
  const reward = paramMean(mind.parameters.rewardWeights);
  const timbral = paramMean(mind.parameters.timbralMap);
  const attention = paramMean(mind.parameters.attentionBiases);

  if (reward > 0.06 && timbral > 0.06) return "bright";
  if (reward < 0.03 && timbral < 0.03) return "dark";
  if (attention > 0.06) return "searching";
  if (reward > 0.04) return "calm";
  return "restless";
}

/** Dominant parameter shift direction */
function dominantShift(mind: M3Mind): "reward" | "temporal" | "timbral" | "precision" | "attention" {
  const groups = [
    { key: "reward" as const, val: paramMean(mind.parameters.rewardWeights) },
    { key: "temporal" as const, val: paramMean(mind.parameters.temporalPrefs) },
    { key: "timbral" as const, val: paramMean(mind.parameters.timbralMap) },
    { key: "precision" as const, val: paramMean(mind.parameters.precisionWeights) },
    { key: "attention" as const, val: paramMean(mind.parameters.attentionBiases) },
  ];
  groups.sort((a, b) => b.val - a.val);
  return groups[0].key;
}

/** Dominant Mind Type from genes */
function dominantFamily(genes: MindGenes): string {
  return getDominantType(genes);
}

/** Genes ranked descending (as Mind Types) */
function rankedFamilies(genes: MindGenes): { name: string; value: number }[] {
  return GENE_NAMES.map(g => ({ name: GENE_TO_TYPE[g], value: genes[g] }))
    .sort((a, b) => b.value - a.value);
}

/** Get active persona name */
function activePersonaName(mind: M3Mind): string {
  return personas.find(p => p.id === mind.activePersonaId)?.name ?? "Unknown";
}

/** Check if observation type is unlocked at given level */
function isUnlocked(type: ObservationType, level: PersonaLevel): boolean {
  return level >= OBSERVATION_LEVEL_GATE[type];
}

/* ── Observation Generators ────────────────────────────────────────── */

/** L2+ Mood Landscape — M³'s current emotional terrain */
function genMoodLandscape(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const mood = computeMood(mind);
  const family = dominantFamily(mind.genes);
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: `ml-mood-${mood}`,
      type: "mood_landscape",
      layer: "surface",
      text: t(`m3.obs.mood.surface.${mood}`),
      intensity: 0.8,
    });
  } else if (layer === "narrative") {
    const dom = dominantShift(mind);
    obs.push({
      id: `ml-trend-${dom}`,
      type: "mood_landscape",
      layer: "narrative",
      text: t(`m3.obs.mood.narrative.${dom}`, { family, listens: mind.totalListens }),
      belief: dom === "reward" ? "reward" : dom === "timbral" ? "consonance" : "salience",
      intensity: 0.7,
    });
  } else {
    const metrics = {
      reward: (paramMean(mind.parameters.rewardWeights) * 1000).toFixed(2),
      precision: (paramMean(mind.parameters.precisionWeights) * 1000).toFixed(2),
      timbral: (paramMean(mind.parameters.timbralMap) * 1000).toFixed(2),
    };
    obs.push({
      id: "ml-metrics",
      type: "mood_landscape",
      layer: "deep",
      text: t("m3.obs.mood.deep", metrics),
      intensity: 0.9,
    });
  }
  return obs;
}

/** L3+ Daily Reflection — snapshot of today's state */
function genDailyReflection(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const mood = computeMood(mind);
  const dom = dominantShift(mind);
  const persona = activePersonaName(mind);
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: `dr-${mood}`,
      type: "daily_reflection",
      layer: "surface",
      text: t(`m3.obs.reflection.surface.${mood}`),
      intensity: 0.6,
    });
  } else if (layer === "narrative") {
    obs.push({
      id: `dr-trend-${dom}`,
      type: "daily_reflection",
      layer: "narrative",
      text: t(`m3.obs.reflection.narrative`, {
        persona,
        listens: mind.totalListens,
        level: mind.level,
        dominant: t(`m3.param.${dom}`),
      }),
      belief: dom === "reward" ? "reward" : "salience",
      intensity: 0.6,
    });
  } else {
    const fnList = mind.activeFunctions.map(f => `F${f}`).join(", ");
    obs.push({
      id: "dr-deep",
      type: "daily_reflection",
      layer: "deep",
      text: t("m3.obs.reflection.deep", {
        active: fnList,
        total: 9,
        count: mind.activeFunctions.length,
        progress: (mind.stageProgress * 100).toFixed(1),
      }),
      intensity: 0.7,
    });
  }
  return obs;
}

/** L5+ Pattern Discovery — recurring behaviors */
function genPatternDiscovery(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const ranked = rankedFamilies(mind.genes);
  const top = ranked[0];
  const runner = ranked[1];
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: `pd-${top.name}`,
      type: "pattern_discovery",
      layer: "surface",
      text: t("m3.obs.pattern.surface", { family: t(`m3.family.${top.name}`) }),
      intensity: 0.7,
    });
  } else if (layer === "narrative") {
    obs.push({
      id: `pd-nar`,
      type: "pattern_discovery",
      layer: "narrative",
      text: t("m3.obs.pattern.narrative", {
        topFamily: t(`m3.family.${top.name}`),
        topPct: (top.value * 100).toFixed(0),
        runnerFamily: t(`m3.family.${runner.name}`),
        runnerPct: (runner.value * 100).toFixed(0),
      }),
      intensity: 0.7,
      functionSource: 4,
    });
  } else {
    const affinityStr = ranked.map(f => `${f.name}: ${(f.value * 100).toFixed(1)}%`).join(", ");
    obs.push({
      id: "pd-deep",
      type: "pattern_discovery",
      layer: "deep",
      text: t("m3.obs.pattern.deep", { affinity: affinityStr, listens: mind.totalListens }),
      intensity: 0.8,
      functionSource: 4,
    });
  }
  return obs;
}

/** L5+ Music Recommendation — growth-aligned suggestions */
function genMusicRecommendation(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const dom = dominantShift(mind);
  const family = dominantFamily(mind.genes);
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: `mr-${dom}`,
      type: "music_recommendation",
      layer: "surface",
      text: t(`m3.obs.recommend.surface.${dom}`),
      intensity: 0.6,
      functionSource: 6,
    });
  } else if (layer === "narrative") {
    obs.push({
      id: `mr-nar`,
      type: "music_recommendation",
      layer: "narrative",
      text: t("m3.obs.recommend.narrative", {
        family: t(`m3.family.${family}`),
        dominant: t(`m3.param.${dom}`),
      }),
      belief: "reward",
      intensity: 0.6,
      functionSource: 6,
    });
  } else {
    const genesStr = [
      `ENT=${mind.genes.entropy.toFixed(2)}`,
      `RES=${mind.genes.resolution.toFixed(2)}`,
      `TEN=${mind.genes.tension.toFixed(2)}`,
      `RSN=${mind.genes.resonance.toFixed(2)}`,
      `PLS=${mind.genes.plasticity.toFixed(2)}`,
    ].join(", ");
    obs.push({
      id: "mr-deep",
      type: "music_recommendation",
      layer: "deep",
      text: t("m3.obs.recommend.deep", { axes: genesStr }),
      intensity: 0.7,
      functionSource: 6,
    });
  }
  return obs;
}

/** L7+ Predictive Insight — anticipating future preferences */
function genPredictiveInsight(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const predMean = paramMean(mind.parameters.predictionCoeffs);
  const dom = dominantShift(mind);
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: "pi-surface",
      type: "predictive_insight",
      layer: "surface",
      text: t(`m3.obs.predict.surface.${dom}`),
      intensity: 0.6,
      functionSource: 2,
      neuroChem: "DA",
    });
  } else if (layer === "narrative") {
    obs.push({
      id: "pi-nar",
      type: "predictive_insight",
      layer: "narrative",
      text: t("m3.obs.predict.narrative", {
        persona: activePersonaName(mind),
        dominant: t(`m3.param.${dom}`),
        level: mind.level,
      }),
      belief: "reward",
      intensity: 0.7,
      functionSource: 2,
      neuroChem: "DA",
    });
  } else {
    obs.push({
      id: "pi-deep",
      type: "predictive_insight",
      layer: "deep",
      text: t("m3.obs.predict.deep", {
        predMean: (predMean * 1000).toFixed(3),
        coeffCount: mind.parameters.predictionCoeffs.length,
      }),
      intensity: 0.8,
      functionSource: 2,
    });
  }
  return obs;
}

/** L7+ Therapeutic Observation — emotional trend analysis */
function genTherapeuticObservation(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const mood = computeMood(mind);
  const family = dominantFamily(mind.genes);
  const rewardMean = paramMean(mind.parameters.rewardWeights);
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: `to-${mood}`,
      type: "therapeutic_observation",
      layer: "surface",
      text: t(`m3.obs.therapeutic.surface.${mood}`),
      intensity: 0.7,
      neuroChem: mood === "dark" ? "5HT" : mood === "bright" ? "OPI" : "NE",
    });
  } else if (layer === "narrative") {
    obs.push({
      id: "to-nar",
      type: "therapeutic_observation",
      layer: "narrative",
      text: t("m3.obs.therapeutic.narrative", {
        mood,
        family: t(`m3.family.${family}`),
        minutes: mind.totalMinutes,
      }),
      intensity: 0.7,
      functionSource: 5,
      neuroChem: "OPI",
    });
  } else {
    obs.push({
      id: "to-deep",
      type: "therapeutic_observation",
      layer: "deep",
      text: t("m3.obs.therapeutic.deep", {
        rewardMean: (rewardMean * 1000).toFixed(3),
        attentionMean: (paramMean(mind.parameters.attentionBiases) * 1000).toFixed(3),
        temporalMean: (paramMean(mind.parameters.temporalPrefs) * 1000).toFixed(3),
      }),
      intensity: 0.8,
      functionSource: 5,
    });
  }
  return obs;
}

/** L9+ Musical Counseling — growth/exploration guidance */
function genMusicalCounseling(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const ranked = rankedFamilies(mind.genes);
  const weakest = ranked[ranked.length - 1];
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: `mc-${weakest.name}`,
      type: "musical_counseling",
      layer: "surface",
      text: t("m3.obs.counseling.surface", { family: t(`m3.family.${weakest.name}`) }),
      intensity: 0.6,
      functionSource: 8,
    });
  } else if (layer === "narrative") {
    obs.push({
      id: "mc-nar",
      type: "musical_counseling",
      layer: "narrative",
      text: t("m3.obs.counseling.narrative", {
        weakFamily: t(`m3.family.${weakest.name}`),
        weakPct: (weakest.value * 100).toFixed(0),
        strongFamily: t(`m3.family.${ranked[0].name}`),
        strongPct: (ranked[0].value * 100).toFixed(0),
      }),
      intensity: 0.7,
      functionSource: 8,
    });
  } else {
    const affinityStr = ranked.map(f => `${f.name}: ${(f.value * 100).toFixed(1)}%`).join(", ");
    obs.push({
      id: "mc-deep",
      type: "musical_counseling",
      layer: "deep",
      text: t("m3.obs.counseling.deep", { affinity: affinityStr, level: mind.level }),
      intensity: 0.8,
      functionSource: 8,
    });
  }
  return obs;
}

/** L9+ Cross-M³ Insight — comparing with other minds */
function genCrossM3Insight(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const persona = activePersonaName(mind);
  const family = dominantFamily(mind.genes);
  const pop = personas.find(p => p.id === mind.activePersonaId)?.populationPct ?? 5;
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: "cx-surface",
      type: "cross_m3_insight",
      layer: "surface",
      text: t("m3.obs.cross.surface", { persona, pct: pop.toFixed(1) }),
      intensity: 0.5,
      functionSource: 9,
    });
  } else if (layer === "narrative") {
    obs.push({
      id: "cx-nar",
      type: "cross_m3_insight",
      layer: "narrative",
      text: t("m3.obs.cross.narrative", {
        persona,
        family: t(`m3.family.${family}`),
        level: mind.level,
        pct: pop.toFixed(1),
      }),
      intensity: 0.6,
      functionSource: 9,
    });
  } else {
    obs.push({
      id: "cx-deep",
      type: "cross_m3_insight",
      layer: "deep",
      text: t("m3.obs.cross.deep", {
        personaId: mind.activePersonaId,
        previousCount: mind.previousPersonaIds.length,
        totalListens: mind.totalListens,
      }),
      intensity: 0.7,
      functionSource: 9,
    });
  }
  return obs;
}

/** L11+ Meta Awareness — M³ commenting on its own changes */
function genMetaAwareness(mind: M3Mind, layer: PresentationLayer, t: TFunction): M3Observation[] {
  const shifts = mind.previousPersonaIds.length;
  const family = dominantFamily(mind.genes);
  const obs: M3Observation[] = [];

  if (layer === "surface") {
    obs.push({
      id: "ma-surface",
      type: "meta_awareness",
      layer: "surface",
      text: t("m3.obs.meta.surface", { level: mind.level, shifts }),
      intensity: 0.9,
      functionSource: 8,
    });
  } else if (layer === "narrative") {
    obs.push({
      id: "ma-nar",
      type: "meta_awareness",
      layer: "narrative",
      text: t("m3.obs.meta.narrative", {
        persona: activePersonaName(mind),
        family: t(`m3.family.${family}`),
        level: mind.level,
        shifts,
        listens: mind.totalListens,
        minutes: mind.totalMinutes,
      }),
      intensity: 0.9,
      functionSource: 8,
    });
  } else {
    const ranked = rankedFamilies(mind.genes);
    const affinityStr = ranked.map(f => `${f.name}: ${(f.value * 100).toFixed(1)}%`).join(", ");
    const genesStr = [
      `ENT=${mind.genes.entropy.toFixed(3)}`,
      `RES=${mind.genes.resolution.toFixed(3)}`,
      `TEN=${mind.genes.tension.toFixed(3)}`,
      `RSN=${mind.genes.resonance.toFixed(3)}`,
      `PLS=${mind.genes.plasticity.toFixed(3)}`,
    ].join(", ");
    obs.push({
      id: "ma-deep",
      type: "meta_awareness",
      layer: "deep",
      text: t("m3.obs.meta.deep", { affinity: affinityStr, axes: genesStr, level: mind.level }),
      intensity: 1.0,
      functionSource: 8,
    });
  }
  return obs;
}

/* ── Generator Registry ───────────────────────────────────────────── */

type ObsGenerator = (mind: M3Mind, layer: PresentationLayer, t: TFunction) => M3Observation[];

const GENERATORS: Record<ObservationType, ObsGenerator> = {
  mood_landscape: genMoodLandscape,
  daily_reflection: genDailyReflection,
  pattern_discovery: genPatternDiscovery,
  music_recommendation: genMusicRecommendation,
  predictive_insight: genPredictiveInsight,
  therapeutic_observation: genTherapeuticObservation,
  musical_counseling: genMusicalCounseling,
  cross_m3_insight: genCrossM3Insight,
  meta_awareness: genMetaAwareness,
};

/* ── Public API ────────────────────────────────────────────────────── */

/**
 * Generate ALL unlocked observations for the given M³ mind at the requested layer.
 * Observations are stage-gated by persona level.
 */
export function generateObservations(
  mind: M3Mind,
  layer: PresentationLayer,
  t: TFunction,
): M3Observation[] {
  const obs: M3Observation[] = [];

  for (const [type, gen] of Object.entries(GENERATORS)) {
    if (isUnlocked(type as ObservationType, mind.level)) {
      obs.push(...gen(mind, layer, t));
    }
  }

  return obs;
}

/**
 * Generate observations for a specific type only (if unlocked).
 */
export function generateObservationsByType(
  mind: M3Mind,
  type: ObservationType,
  layer: PresentationLayer,
  t: TFunction,
): M3Observation[] {
  if (!isUnlocked(type, mind.level)) return [];
  return GENERATORS[type](mind, layer, t);
}

/**
 * Get all unlocked observation types for the mind's current level.
 */
export function getUnlockedObservationTypes(level: PersonaLevel): ObservationType[] {
  return (Object.entries(OBSERVATION_LEVEL_GATE) as [ObservationType, PersonaLevel][])
    .filter(([, minLevel]) => level >= minLevel)
    .map(([type]) => type);
}

/**
 * Get the primary (most important) observation for a quick summary.
 */
export function getPrimaryObservation(
  mind: M3Mind,
  t: TFunction,
): M3Observation {
  const mood = computeMood(mind);
  return {
    id: `primary-${mood}`,
    type: "mood_landscape",
    layer: "surface",
    text: t(`m3.obs.mood.surface.${mood}`),
    intensity: 0.8,
  };
}
