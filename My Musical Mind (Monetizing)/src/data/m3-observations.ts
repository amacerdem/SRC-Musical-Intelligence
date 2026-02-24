/* ── M³ Observation Engine ──────────────────────────────────────────
 *  Generates observations following the "observe, don't judge" policy.
 *  M³ NEVER says "you are X". It describes its own state or reports data.
 *  Three layers: Surface (mood), Narrative (trends), Deep (metrics).
 *  ──────────────────────────────────────────────────────────────────── */

import type { TFunction } from "i18next";
import type { M3Mind, M3Observation, PresentationLayer } from "@/types/m3";
import { M3_STAGES } from "@/data/m3-stages";

/* ── Helpers ───────────────────────────────────────────────────────── */

/** Compute a summary metric from parameter array (mean absolute value) */
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

/** Compute dominant parameter shift direction */
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

/* ── Surface Layer ─────────────────────────────────────────────────── */

function generateSurface(mind: M3Mind, t: TFunction): M3Observation[] {
  const mood = computeMood(mind);
  const stage = mind.stage;
  const obs: M3Observation[] = [];

  // Primary mood observation
  obs.push({
    id: `s-mood-${mood}`,
    layer: "surface",
    text: t(`m3.observations.surface.mood.${mood}`),
    intensity: 0.8,
  });

  // Stage-specific observation
  if (stage === "seed") {
    obs.push({
      id: "s-seed",
      layer: "surface",
      text: t("m3.observations.surface.seed"),
      intensity: 0.5,
    });
  } else if (stage === "sprout") {
    obs.push({
      id: "s-sprout",
      layer: "surface",
      text: t("m3.observations.surface.sprout"),
      intensity: 0.6,
    });
  } else {
    const dom = dominantShift(mind);
    obs.push({
      id: `s-shift-${dom}`,
      layer: "surface",
      text: t(`m3.observations.surface.shift.${dom}`),
      intensity: 0.7,
    });
  }

  return obs;
}

/* ── Narrative Layer ───────────────────────────────────────────────── */

function generateNarrative(mind: M3Mind, t: TFunction): M3Observation[] {
  const obs: M3Observation[] = [];
  const dom = dominantShift(mind);
  const mood = computeMood(mind);
  const activeFns = mind.activeFunctions;

  // Trend observation
  obs.push({
    id: `n-trend-${dom}`,
    layer: "narrative",
    text: t(`m3.observations.narrative.trend.${dom}`, {
      listens: mind.totalListens,
      stage: t(`m3.stage.${mind.stage}`),
    }),
    belief: dom === "reward" ? "reward" : dom === "timbral" ? "consonance" : dom === "temporal" ? "tempo" : "salience",
    intensity: 0.7,
  });

  // Mood-context narrative
  obs.push({
    id: `n-mood-${mood}`,
    layer: "narrative",
    text: t(`m3.observations.narrative.mood.${mood}`),
    intensity: 0.6,
  });

  // Function-specific narrative (only for active functions)
  if (activeFns.includes(2)) {
    // F2 Prediction active — note prediction accuracy
    const predMean = paramMean(mind.parameters.predictionCoeffs);
    obs.push({
      id: "n-prediction",
      layer: "narrative",
      text: t("m3.observations.narrative.prediction", {
        accuracy: (predMean * 1000).toFixed(1),
      }),
      functionSource: 2,
      intensity: 0.5,
    });
  }

  if (activeFns.includes(4)) {
    // F4 Memory active
    obs.push({
      id: "n-memory",
      layer: "narrative",
      text: t("m3.observations.narrative.memory", {
        listens: mind.totalListens,
      }),
      functionSource: 4,
      intensity: 0.5,
    });
  }

  if (activeFns.includes(6)) {
    // F6 Reward active
    const rewardMean = paramMean(mind.parameters.rewardWeights);
    obs.push({
      id: "n-reward",
      layer: "narrative",
      text: t("m3.observations.narrative.reward", {
        intensity: (rewardMean * 100).toFixed(0),
      }),
      belief: "reward",
      functionSource: 6,
      intensity: rewardMean * 10,
    });
  }

  return obs;
}

/* ── Deep Layer ────────────────────────────────────────────────────── */

function generateDeep(mind: M3Mind, t: TFunction): M3Observation[] {
  const obs: M3Observation[] = [];

  // Parameter means
  const metrics = {
    reward: paramMean(mind.parameters.rewardWeights),
    precision: paramMean(mind.parameters.precisionWeights),
    temporal: paramMean(mind.parameters.temporalPrefs),
    timbral: paramMean(mind.parameters.timbralMap),
    attention: paramMean(mind.parameters.attentionBiases),
    prediction: paramMean(mind.parameters.predictionCoeffs),
    beliefPrior: paramMean(mind.parameters.beliefPriors),
    crossCorr: paramMean(mind.parameters.crossCorrelations),
  };

  // Technical summary
  obs.push({
    id: "d-metrics",
    layer: "deep",
    text: t("m3.observations.deep.metrics", {
      reward: (metrics.reward * 1000).toFixed(2),
      precision: (metrics.precision * 1000).toFixed(2),
      temporal: (metrics.temporal * 1000).toFixed(2),
      timbral: (metrics.timbral * 1000).toFixed(2),
      attention: (metrics.attention * 1000).toFixed(2),
    }),
    intensity: 0.9,
  });

  // Active functions report
  const fnList = mind.activeFunctions.map(f => `F${f}`).join(", ");
  obs.push({
    id: "d-functions",
    layer: "deep",
    text: t("m3.observations.deep.functions", {
      active: fnList,
      total: 9,
      count: mind.activeFunctions.length,
    }),
    intensity: 0.7,
  });

  // Stage progression
  const stageDef = M3_STAGES[mind.stage];
  obs.push({
    id: "d-stage",
    layer: "deep",
    text: t("m3.observations.deep.stage", {
      stage: mind.stage,
      progress: (mind.stageProgress * 100).toFixed(1),
      organism: stageDef.organismStage,
      listens: mind.totalListens,
    }),
    intensity: 0.6,
  });

  // Prediction coefficients (if F2 active)
  if (mind.activeFunctions.includes(2)) {
    obs.push({
      id: "d-prediction",
      layer: "deep",
      text: t("m3.observations.deep.prediction", {
        mean: (metrics.prediction * 1000).toFixed(3),
        beliefPrior: (metrics.beliefPrior * 1000).toFixed(3),
      }),
      functionSource: 2,
      intensity: 0.5,
    });
  }

  return obs;
}

/* ── Public API ────────────────────────────────────────────────────── */

/**
 * Generate observations for the given M³ mind at the requested layer.
 * Observations follow the language policy: observe, never judge.
 */
export function generateObservations(
  mind: M3Mind,
  layer: PresentationLayer,
  t: TFunction,
): M3Observation[] {
  switch (layer) {
    case "surface": return generateSurface(mind, t);
    case "narrative": return generateNarrative(mind, t);
    case "deep": return generateDeep(mind, t);
  }
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
    layer: "surface",
    text: t(`m3.observations.surface.mood.${mood}`),
    intensity: 0.8,
  };
}
