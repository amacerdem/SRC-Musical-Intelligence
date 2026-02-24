/* ── usePersonaOrganism — Derive organism config from persona + level + identity ── */

import { useMemo } from "react";
import type { Persona } from "@/types/mind";
import type { PersonaLevel, NeuralFamily } from "@/types/m3";
import { FAMILY_MORPHOLOGY, levelToOrganismStage } from "@/types/m3";
import { getLevelVisualConfig } from "@/data/persona-levels";
import type { FamilyMorphology } from "@/canvas/mind-organism";

export interface PersonaOrganismConfig {
  color: string;
  stage: 1 | 2 | 3;
  intensity: number;
  breathRate: number;
  familyMorphology: FamilyMorphology;
  tendrilCount: number;
  nucleiCount: number;
  bloomEnabled: boolean;
  chromaticEnabled: boolean;
  constellations: boolean;
  maxParticles: number;
}

/**
 * Derive organism rendering config from persona identity + M³ level.
 * When overrideColor / overrideFamily are provided (from useActiveIdentity),
 * those take precedence over persona's static values.
 */
export function usePersonaOrganism(
  persona: Persona | null,
  level: PersonaLevel,
  overrideColor?: string,
  overrideFamily?: NeuralFamily,
): PersonaOrganismConfig {
  return useMemo(() => {
    const family = overrideFamily ?? persona?.family ?? "Alchemists";
    const color = overrideColor ?? persona?.color ?? "#A855F7";
    const morphology = FAMILY_MORPHOLOGY[family] as FamilyMorphology;
    const levelConfig = getLevelVisualConfig(level);
    const organismStage = levelToOrganismStage(level);

    return {
      color,
      stage: organismStage,
      intensity: levelConfig.intensity,
      breathRate: levelConfig.breathRate,
      familyMorphology: morphology,
      tendrilCount: levelConfig.tendrilCount,
      nucleiCount: levelConfig.nucleiCount,
      bloomEnabled: levelConfig.bloomEnabled,
      chromaticEnabled: levelConfig.chromaticEnabled,
      constellations: organismStage >= 2,
      maxParticles: levelConfig.particleCap,
    };
  }, [persona, level, overrideColor, overrideFamily]);
}
