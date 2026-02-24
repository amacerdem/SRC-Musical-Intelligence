/* ── M³ Tier Gating Hook ───────────────────────────────────────────
 *  Simple hook for feature-gating based on M³ tier and stage.
 *  Use in components to show/hide features and display upgrade CTAs.
 *  ──────────────────────────────────────────────────────────────── */

import { useM3Store } from "@/stores/useM3Store";
import { M3_STAGE_ORDER } from "@/types/m3";
import type { M3Stage, M3Tier, PresentationLayer } from "@/types/m3";

/** Numeric stage comparison */
function stageIndex(stage: M3Stage): number {
  return M3_STAGE_ORDER.indexOf(stage);
}

export function useM3Gate() {
  const mind = useM3Store((s) => s.mind);

  const tier: M3Tier = mind?.tier ?? "free";
  const stage: M3Stage = mind?.stage ?? "embryo";
  const isFrozen = mind?.frozen ?? true;
  const isAlive = mind !== null;

  return {
    /* Identity */
    isAlive,
    tier,
    stage,
    isFrozen,

    /* Growth */
    canGrow: isAlive && !isFrozen && tier !== "free",

    /* Presentation layers */
    canSeeLayer: (layer: PresentationLayer): boolean => {
      if (layer === "surface") return true;
      if (layer === "narrative") return tier !== "free";
      if (layer === "deep") return tier === "premium" || tier === "ultimate";
      return false;
    },

    /* Social features */
    canUseSocial: isAlive && stageIndex(stage) >= stageIndex("infant"),
    canUseDuoMind:
      isAlive &&
      (tier === "premium" || tier === "ultimate") &&
      stageIndex(stage) >= stageIndex("adolescent"),
    canUseEcho: isAlive && tier === "ultimate",
    canUseGarden:
      isAlive &&
      (tier === "premium" || tier === "ultimate") &&
      stageIndex(stage) >= stageIndex("toddler"),

    /* Recommendations */
    canGetRecommendations: isAlive && stageIndex(stage) >= stageIndex("toddler"),

    /* Therapeutic observations */
    canSeeTherapeutic: isAlive && stageIndex(stage) >= stageIndex("child"),

    /* Upgrade needed? */
    needsUpgrade: tier === "free",
    upgradeTarget: tier === "free" ? "basic" : tier === "basic" ? "premium" : tier === "premium" ? "ultimate" : null,
  };
}
