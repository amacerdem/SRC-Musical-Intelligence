/* ── useActiveIdentity — Persona-derived identity for the current user ── */

import { useM3Store } from "@/stores/useM3Store";
import { getPersona } from "@/data/personas";
import {
  getDominantGene,
  getDominantType,
  GENE_COLORS,
  FAMILY_MORPHOLOGY,
} from "@/types/m3";
import type { NeuralFamily, GeneName } from "@/types/m3";
import type { FamilyMorphology } from "@/canvas/mind-organism";

export interface ActiveIdentity {
  color: string;
  family: NeuralFamily;
  morphology: FamilyMorphology;
  gene: GeneName;
}

const FALLBACK: ActiveIdentity = {
  color: "#A855F7",
  family: "Alchemists",
  morphology: "volatile" as FamilyMorphology,
  gene: "tension",
};

/**
 * Returns the current user's identity derived from their active persona + genes.
 * Uses the persona's unique color (24 options) instead of the family color (5 options).
 * Reactively updates when genes or activePersonaId change (e.g. after training).
 */
export function useActiveIdentity(): ActiveIdentity {
  const genes = useM3Store((s) => s.mind?.genes);
  const activePersonaId = useM3Store((s) => s.mind?.activePersonaId);
  if (!genes) return FALLBACK;

  const gene = getDominantGene(genes);
  const family = getDominantType(genes);

  // Prefer persona-specific color over generic gene color
  const persona = activePersonaId ? getPersona(activePersonaId) : null;

  return {
    color: persona?.color ?? GENE_COLORS[gene],
    family,
    morphology: FAMILY_MORPHOLOGY[family] as FamilyMorphology,
    gene,
  };
}
