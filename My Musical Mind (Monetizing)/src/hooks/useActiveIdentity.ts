/* ── useActiveIdentity — Gene-derived identity for the current user ── */

import { useM3Store } from "@/stores/useM3Store";
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
 * Returns the current user's identity derived from their dominant Mind Gene.
 * Reactively updates when genes change (e.g. after training).
 */
export function useActiveIdentity(): ActiveIdentity {
  const genes = useM3Store((s) => s.mind?.genes);
  if (!genes) return FALLBACK;

  const gene = getDominantGene(genes);
  const family = getDominantType(genes);
  return {
    color: GENE_COLORS[gene],
    family,
    morphology: FAMILY_MORPHOLOGY[family] as FamilyMorphology,
    gene,
  };
}
