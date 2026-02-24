/* ── usePlaylistGenerator — Gene-Based Personalized Playlist ─────────
 *  Scores every track in the library against the user's 5 Mind Genes:
 *    40% — Gene→genre affinity
 *    30% — C³ profile cosine similarity
 *    20% — Audio feature matching
 *    10% — Diversity bonus (penalizes genre clustering)
 *  Returns top 12 tracks, shuffled within top tier.
 *  ──────────────────────────────────────────────────────────────── */

import { useMemo } from "react";
import { LIBRARY_TRACKS, type LibraryTrack } from "@/data/track-library";
import type { MindGenes, GeneName } from "@/types/m3";
import { GENE_NAMES } from "@/types/m3";

/* ── Genre Affinity Maps ─────────────────────────────────────── */

/** How much each gene "likes" each genre. Values 0-1. */
const GENE_GENRE_AFFINITY: Record<GeneName, Record<string, number>> = {
  entropy: {
    "IDM": 0.95, "Free Jazz": 0.9, "Noise": 0.85, "Glitch": 0.9,
    "Musique Concrète": 0.85, "Experimental": 0.8, "Art Rock": 0.75,
    "Progressive Rock": 0.7, "Jazz Fusion": 0.7, "Dark Ambient": 0.6,
    "Drum & Bass": 0.5, "Electronic": 0.5, "Psychedelic Rock": 0.6,
    "Post-Metal": 0.55,
  },
  resolution: {
    "Classical": 0.95, "Neo-Classical": 0.9, "Cinematic": 0.85,
    "Jazz": 0.8, "Smooth Jazz": 0.7, "Bossa Nova": 0.65,
    "Progressive Rock": 0.6, "Indian Classical": 0.75, "Jazz Fusion": 0.65,
    "Post-Rock": 0.5, "Ambient": 0.45,
  },
  tension: {
    "Progressive Metal": 0.9, "Post-Metal": 0.85, "Dark Ambient": 0.8,
    "Cinematic": 0.75, "Post-Rock": 0.7, "Trip-Hop": 0.65,
    "Psychedelic Rock": 0.7, "Free Jazz": 0.6, "Rock": 0.55,
    "Flamenco": 0.7, "Art Rock": 0.6, "Noise": 0.5,
  },
  resonance: {
    "Ambient": 0.9, "Singer-Songwriter": 0.9, "Indie Folk": 0.85,
    "Neo-Soul": 0.8, "Bossa Nova": 0.8, "Smooth Jazz": 0.75,
    "Lo-Fi Hip-Hop": 0.8, "R&B": 0.75, "Japanese Ambient": 0.85,
    "Classical": 0.6, "Post-Rock": 0.5, "Bluegrass": 0.65, "Funk": 0.5,
  },
  plasticity: {
    "Electronic": 0.85, "Progressive House": 0.9, "Synthwave": 0.8,
    "Drum & Bass": 0.85, "Trance": 0.8, "Funk": 0.85, "Afrobeat": 0.85,
    "Rock": 0.7, "Boom Bap": 0.75, "Trap": 0.7, "Bluegrass": 0.6,
    "Lo-Fi Hip-Hop": 0.55, "R&B": 0.6, "Flamenco": 0.65,
  },
};

/* ── Scoring Functions ───────────────────────────────────────── */

/** Gene-genre affinity score (0-1) */
function geneGenreScore(genes: MindGenes, genre: string): number {
  let score = 0;
  let totalWeight = 0;
  for (const g of GENE_NAMES) {
    const affinity = GENE_GENRE_AFFINITY[g][genre] ?? 0.3; // default 0.3 for unknown genres
    score += genes[g] * affinity;
    totalWeight += genes[g];
  }
  return totalWeight > 0 ? score / totalWeight : 0.3;
}

/** Cosine similarity between two 5D vectors */
function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0, magA = 0, magB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    magA += a[i] * a[i];
    magB += b[i] * b[i];
  }
  const mag = Math.sqrt(magA) * Math.sqrt(magB);
  return mag > 0 ? dot / mag : 0;
}

/** C³ profile similarity — cosine between gene-derived ideal and track's C³ */
function c3SimilarityScore(genes: MindGenes, track: LibraryTrack): number {
  // Derive an "ideal" C³ profile from genes
  const ideal = [
    genes.resonance * 0.6 + genes.resolution * 0.4,      // harmonicConsonance
    genes.plasticity * 0.5 + genes.tension * 0.3 + 0.2,   // rhythmicSync
    genes.resolution * 0.6 + (1 - genes.entropy) * 0.4,   // patternPredictability
    genes.resonance * 0.5 + genes.resolution * 0.3 + 0.2, // memoryRecognition
    genes.plasticity * 0.3 + genes.tension * 0.3 + genes.entropy * 0.2 + 0.2, // wanting
  ];
  const trackC3 = [
    track.c3Profile.harmonicConsonance,
    track.c3Profile.rhythmicSync,
    track.c3Profile.patternPredictability,
    track.c3Profile.memoryRecognition,
    track.c3Profile.wanting,
  ];
  return cosineSimilarity(ideal, trackC3);
}

/** Audio feature matching score — gene preferences mapped to features */
function featureMatchScore(genes: MindGenes, track: LibraryTrack): number {
  const f = track.audioFeatures;
  const tempoNorm = Math.min(1, f.tempo / 200);

  // Gene-derived preferences
  const energyPref = genes.plasticity * 0.4 + genes.tension * 0.4 + genes.entropy * 0.2;
  const valencePref = genes.resonance * 0.5 + genes.plasticity * 0.3 + (1 - genes.tension) * 0.2;
  const tempoPref = genes.plasticity * 0.4 + genes.entropy * 0.3 + genes.tension * 0.3;
  const acousticPref = genes.resonance * 0.4 + genes.resolution * 0.4 + (1 - genes.entropy) * 0.2;
  const complexPref = genes.resolution * 0.3 + genes.entropy * 0.4 + genes.tension * 0.3;

  // Score = 1 - average absolute distance
  const diffs = [
    Math.abs(f.energy - energyPref),
    Math.abs(f.valence - valencePref),
    Math.abs(tempoNorm - tempoPref),
    Math.abs(f.acousticness - acousticPref),
    Math.abs(f.harmonicComplexity - complexPref),
  ];
  return 1 - (diffs.reduce((a, b) => a + b, 0) / diffs.length);
}

/** Score a single track against user genes */
function scoreTrack(
  track: LibraryTrack,
  genes: MindGenes,
  genreCounts: Record<string, number>,
): number {
  const genreAffinity = geneGenreScore(genes, track.genre);
  const c3Sim = c3SimilarityScore(genes, track);
  const featureMatch = featureMatchScore(genes, track);

  // Diversity: penalize genres already selected
  const count = genreCounts[track.genre] ?? 0;
  const diversityBonus = 1 / (1 + count * 0.6);

  return (
    genreAffinity * 0.40 +
    c3Sim * 0.30 +
    featureMatch * 0.20 +
    diversityBonus * 0.10
  );
}

/* ── Generator ───────────────────────────────────────────────── */

/** Generate a personalized playlist of `count` tracks */
export function generateWeeklyPlaylist(
  allTracks: LibraryTrack[],
  genes: MindGenes,
  count = 12,
): LibraryTrack[] {
  const genreCounts: Record<string, number> = {};
  const selected: LibraryTrack[] = [];

  // Greedily pick top-scoring tracks one at a time (genre diversity built in)
  const remaining = [...allTracks];
  for (let i = 0; i < count && remaining.length > 0; i++) {
    let bestIdx = 0;
    let bestScore = -1;
    for (let j = 0; j < remaining.length; j++) {
      const s = scoreTrack(remaining[j], genes, genreCounts);
      if (s > bestScore) {
        bestScore = s;
        bestIdx = j;
      }
    }
    const pick = remaining.splice(bestIdx, 1)[0];
    selected.push(pick);
    genreCounts[pick.genre] = (genreCounts[pick.genre] ?? 0) + 1;
  }

  return selected;
}

/* ── React Hook ──────────────────────────────────────────────── */

export function usePlaylistGenerator(genes: MindGenes | undefined, count = 12) {
  return useMemo(() => {
    if (!genes) return [];
    return generateWeeklyPlaylist(LIBRARY_TRACKS, genes, count);
  }, [genes, count]);
}
