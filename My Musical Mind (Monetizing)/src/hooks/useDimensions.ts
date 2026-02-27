/* ── useDimensions — Tier-gated dimension access hook ─────────────
 *  Computes 6D/12D/24D dimension state from M³ belief parameters
 *  and gates access based on the user's subscription tier.
 *
 *  Free     → 6D  psychology only
 *  Basic    → 6D + 12D cognition
 *  Premium  → 6D + 12D + 24D neuroscience
 *  Ultimate → 6D + 12D + 24D + 131D research
 *  ──────────────────────────────────────────────────────────────── */

import { useMemo } from "react";
import { useM3Store } from "@/stores/useM3Store";
import type { DimensionLayer, DimensionProfile, DimensionState } from "@/types/dimensions";
import { TIER_DIMENSION_ACCESS } from "@/types/dimensions";
import {
  computeDimensions,
  arrayToProfile,
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  ALL_NEUROSCIENCE,
  PSYCHOLOGY_NAMES,
  PSYCHOLOGY_NAMES_TR,
  COGNITION_NAMES,
  NEUROSCIENCE_NAMES,
} from "@/data/dimensions";
import { getPersonaDimensions } from "@/data/persona-dimensions";

export interface UseDimensionsResult {
  /** Whether dimension data is available (M³ mind exists) */
  isAvailable: boolean;

  /** Current 6D profile computed from belief parameters */
  profile6D: DimensionProfile;

  /** Full dimension state (6D/12D/24D arrays) computed from beliefs */
  state: DimensionState;

  /** Which dimension layers the current tier can see */
  visibleLayers: DimensionLayer[];

  /** Check if a specific layer is visible at current tier */
  canSeeLayer: (layer: DimensionLayer) => boolean;

  /** The active persona's canonical 6D radar profile */
  personaProfile: DimensionProfile;

  /** Dimension names for the current locale */
  names: {
    psychology: string[];
    cognition: string[];
    neuroscience: string[];
  };

  /** The max dimension layer accessible at current tier */
  maxLayer: DimensionLayer;
}

export function useDimensions(locale: "en" | "tr" = "en"): UseDimensionsResult {
  const mind = useM3Store((s) => s.mind);

  const state = useMemo<DimensionState>(() => {
    if (!mind) {
      return {
        psychology: new Array(6).fill(0),
        cognition: new Array(12).fill(0),
        neuroscience: new Array(24).fill(0),
      };
    }
    // Compute from beliefPriors (131 values)
    return computeDimensions(mind.parameters.beliefPriors);
  }, [mind?.parameters.beliefPriors]);

  const profile6D = useMemo<DimensionProfile>(
    () => arrayToProfile(state.psychology),
    [state.psychology],
  );

  const tier = mind?.tier ?? "free";
  const visibleLayers = TIER_DIMENSION_ACCESS[tier] ?? ["psychology"];

  const canSeeLayer = (layer: DimensionLayer): boolean =>
    visibleLayers.includes(layer);

  const personaProfile = useMemo<DimensionProfile>(
    () => getPersonaDimensions(mind?.activePersonaId ?? 1),
    [mind?.activePersonaId],
  );

  const maxLayer: DimensionLayer =
    visibleLayers[visibleLayers.length - 1] ?? "psychology";

  const names = useMemo(() => ({
    psychology: locale === "tr" ? PSYCHOLOGY_NAMES_TR : PSYCHOLOGY_NAMES,
    cognition: COGNITION_NAMES,
    neuroscience: NEUROSCIENCE_NAMES,
  }), [locale]);

  return {
    isAvailable: mind !== null,
    profile6D,
    state,
    visibleLayers,
    canSeeLayer,
    personaProfile,
    names,
    maxLayer,
  };
}
