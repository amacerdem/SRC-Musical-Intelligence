/* ── MIDataService — Real MI Dataset Access Layer ────────────────────
 *  Loads catalog.json on init, lazy-loads per-track detail JSONs.
 *  Provides SpotifySimulator-compatible API + richer gene-based APIs.
 *  ──────────────────────────────────────────────────────────────────── */

import type {
  MICatalog,
  MICatalogTrack,
  MITrackDetail,
} from "@/types/mi-dataset";
import type { NeuralFamily } from "@/types/mind";
import type { M3TrackSignal, MindGenes } from "@/types/m3";
import { DEFAULT_GENES, GENE_NAMES, getDominantType, getDominantGene } from "@/types/m3";
import type { GeneName } from "@/types/m3";
import type { MockTrack } from "./SpotifySimulator";
import type {
  LibraryTrack,
  R3Profile,
  C3Profile,
  AudioFeatures,
} from "@/data/track-library";

const CATALOG_URL = "/data/mi-dataset/catalog.json";
const TRACK_URL = (id: string) => `/data/mi-dataset/tracks/${id}.json`;

/** Aggregate profile computed from the user's full listening history */
export interface MIAggregateProfile {
  genes: MindGenes;
  totalTracks: number;
  totalMinutes: number;
  dominantFamily: NeuralFamily;
  dominantGene: GeneName;
}

class MIDataService {
  private catalog: MICatalog | null = null;
  private trackCache = new Map<string, MITrackDetail>();
  private sessionOffset = 0;

  /* ── Init ─────────────────────────────────────────────────────── */

  async init(): Promise<void> {
    if (this.catalog) return;
    const res = await fetch(CATALOG_URL);
    this.catalog = (await res.json()) as MICatalog;
  }

  isReady(): boolean {
    return this.catalog !== null;
  }

  getCatalog(): MICatalog {
    if (!this.catalog) throw new Error("MIDataService not initialized");
    return this.catalog;
  }

  getAllTracks(): MICatalogTrack[] {
    return this.catalog?.tracks ?? [];
  }

  /* ── Per-track detail (lazy) ──────────────────────────────────── */

  async getTrackDetail(id: string): Promise<MITrackDetail> {
    const cached = this.trackCache.get(id);
    if (cached) return cached;
    const res = await fetch(TRACK_URL(id));
    const detail = (await res.json()) as MITrackDetail;
    this.trackCache.set(id, detail);
    return detail;
  }

  /* ── Aggregate Profile (deterministic) ───────────────────────── */

  /** Compute the user's TRUE gene profile from their full listening library.
   *  Duration-weighted average of all track genes → always the same result. */
  computeAggregateProfile(): MIAggregateProfile {
    const tracks = this.getAllTracks();
    if (tracks.length === 0) {
      return {
        genes: { ...DEFAULT_GENES },
        totalTracks: 0,
        totalMinutes: 0,
        dominantFamily: "Explorers" as NeuralFamily,
        dominantGene: "entropy" as GeneName,
      };
    }

    const totalDuration = tracks.reduce((s, t) => s + t.duration_s, 0);

    // Duration-weighted gene average across all tracks
    const genes: MindGenes = {
      entropy: 0, resolution: 0, tension: 0, resonance: 0, plasticity: 0,
    };
    for (const t of tracks) {
      const w = t.duration_s / totalDuration;
      for (const g of GENE_NAMES) {
        genes[g] += t.genes[g as keyof typeof t.genes] * w;
      }
    }

    return {
      genes,
      totalTracks: tracks.length,
      totalMinutes: Math.round(totalDuration / 60),
      dominantFamily: getDominantType(genes),
      dominantGene: getDominantGene(genes),
    };
  }

  /* ── SpotifySimulator-compatible API (deterministic) ─────────── */

  getCurrentTrack(): Promise<MockTrack> {
    const tracks = this.getAllTracks();
    if (tracks.length === 0) throw new Error("No tracks loaded");
    return Promise.resolve(MIDataService.toMockTrack(tracks[0]));
  }

  getRecentHistory(): MockTrack[] {
    const tracks = this.getAllTracks();
    return tracks.slice(0, 5).map(MIDataService.toMockTrack);
  }

  /** Return the next batch of tracks in catalog order (deterministic, sequential). */
  getListeningSession(): {
    track: MockTrack;
    listenedAt: string;
    wasSkipped: boolean;
  }[] {
    const tracks = this.getAllTracks();
    const count = 10;
    const now = Date.now();
    const start = this.sessionOffset % tracks.length;
    this.sessionOffset += count;

    const session: MICatalogTrack[] = [];
    for (let i = 0; i < count && i < tracks.length; i++) {
      session.push(tracks[(start + i) % tracks.length]);
    }

    return session.map((ct, i) => ({
      track: MIDataService.toMockTrack(ct),
      listenedAt: new Date(
        now - (count - i) * 4 * 60 * 1000
      ).toISOString(),
      wasSkipped: false,
    }));
  }

  getInitialBatch(): MockTrack[] {
    const tracks = this.getAllTracks();
    return tracks.slice(0, 20).map(MIDataService.toMockTrack);
  }

  /* ── Rich APIs ────────────────────────────────────────────────── */

  getTracksByFamily(family: NeuralFamily): MICatalogTrack[] {
    return this.getAllTracks().filter(
      (t) => t.dominant_family === family
    );
  }

  getTracksByCategory(cat: string): MICatalogTrack[] {
    return this.getAllTracks().filter((t) =>
      t.categories.includes(cat)
    );
  }

  getRecommendations(
    userGenes: MindGenes,
    count: number
  ): MICatalogTrack[] {
    const tracks = this.getAllTracks();
    const scored = tracks.map((t) => ({
      track: t,
      score: recommendationScore(t, userGenes),
    }));
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, count).map((s) => s.track);
  }

  /** Find catalog track by id */
  findTrack(id: string): MICatalogTrack | undefined {
    return this.getAllTracks().find((t) => t.id === id);
  }

  /* ── Static Adapters ──────────────────────────────────────────── */

  static toMockTrack(ct: MICatalogTrack): MockTrack {
    return {
      id: ct.id,
      name: ct.title,
      artist: ct.artist,
      albumArt: "",
      features: {
        energy: ct.signal.energy,
        valence: ct.signal.valence,
        tempo: ct.signal.tempo,
        danceability: ct.signal.danceability,
        acousticness: ct.signal.acousticness,
        harmonicComplexity: ct.signal.harmonicComplexity,
        timbralBrightness: ct.signal.timbralBrightness,
      },
      dominantFamily: ct.dominant_family as NeuralFamily,
      genre: ct.categories[0] ?? "Unknown",
      durationSec: ct.duration_s,
    };
  }

  static toM3Signal(
    ct: MICatalogTrack,
    opts?: { isRepeat?: boolean; wasSkipped?: boolean }
  ): M3TrackSignal {
    return {
      energy: ct.signal.energy,
      valence: ct.signal.valence,
      tempo: ct.signal.tempo,
      danceability: ct.signal.danceability,
      acousticness: ct.signal.acousticness,
      harmonicComplexity: ct.signal.harmonicComplexity,
      timbralBrightness: ct.signal.timbralBrightness,
      duration: ct.signal.duration,
      isRepeat: opts?.isRepeat ?? false,
      wasSkipped: opts?.wasSkipped ?? false,
    };
  }

  static toLibraryTrack(ct: MICatalogTrack): LibraryTrack {
    const s = ct.signal;
    const g = ct.genes;

    const audioFeatures: AudioFeatures = {
      energy: s.energy,
      valence: s.valence,
      tempo: s.tempo,
      danceability: s.danceability,
      acousticness: s.acousticness,
      harmonicComplexity: s.harmonicComplexity,
      timbralBrightness: s.timbralBrightness,
    };

    const r3Profile: R3Profile = {
      roughness: 1 - s.acousticness,
      spectralFlux: s.energy * 0.6 + s.harmonicComplexity * 0.4,
      loudness: s.energy,
      keyClarity:
        s.acousticness * 0.5 + (1 - s.harmonicComplexity) * 0.5,
      onsetStrength: s.danceability * 0.6 + s.energy * 0.4,
      melodicClarity:
        s.acousticness * 0.4 +
        (1 - s.timbralBrightness) * 0.3 +
        s.harmonicComplexity * 0.3,
      brightness: s.timbralBrightness,
      tempoStability: s.danceability * 0.7 + (1 - s.energy) * 0.3,
      tonalness:
        s.acousticness * 0.5 + (1 - s.timbralBrightness) * 0.5,
      grooveStrength: s.danceability * 0.7 + s.energy * 0.3,
    };

    const c3Profile: C3Profile = {
      harmonicConsonance: g.resolution * 0.6 + g.resonance * 0.4,
      rhythmicSync:
        g.plasticity * 0.5 + g.entropy * 0.3 + 0.2,
      patternPredictability:
        g.resolution * 0.6 + (1 - g.entropy) * 0.4,
      memoryRecognition:
        g.resonance * 0.5 + g.resolution * 0.3 + 0.2,
      wanting:
        g.plasticity * 0.3 +
        g.tension * 0.3 +
        g.entropy * 0.2 +
        0.2,
    };

    return {
      id: ct.id,
      name: ct.title,
      artist: ct.artist,
      genre: ct.categories[0] ?? "Unknown",
      bpm: Math.round(s.tempo),
      key: "?",
      mode: "minor",
      durationSec: ct.duration_s,
      dominantFamily: ct.dominant_family as NeuralFamily,
      audioFeatures,
      r3Profile,
      c3Profile,
      audioFile: "",
    };
  }
}

/* ── Helpers ─────────────────────────────────────────────────────── */

function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0,
    magA = 0,
    magB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    magA += a[i] * a[i];
    magB += b[i] * b[i];
  }
  const denom = Math.sqrt(magA) * Math.sqrt(magB);
  return denom === 0 ? 0 : dot / denom;
}

function recommendationScore(
  track: MICatalogTrack,
  userGenes: MindGenes
): number {
  const tg = track.genes;
  const geneVec = [
    tg.entropy,
    tg.resolution,
    tg.tension,
    tg.resonance,
    tg.plasticity,
  ];
  const userVec = [
    userGenes.entropy,
    userGenes.resolution,
    userGenes.tension,
    userGenes.resonance,
    userGenes.plasticity,
  ];

  // 50% gene cosine similarity
  const geneSim = cosineSimilarity(geneVec, userVec);

  // 30% complementary — tracks that exercise the user's weakest gene
  let weakest: keyof MindGenes = "entropy";
  let weakVal = Infinity;
  for (const g of GENE_NAMES) {
    if (userGenes[g] < weakVal) {
      weakVal = userGenes[g];
      weakest = g;
    }
  }
  const complementary = tg[weakest];

  // 20% diversity bonus — different dominant family
  const familyBonus =
    track.dominant_family !== getDominantType(userGenes) ? 0.3 : 0.0;

  return geneSim * 0.5 + complementary * 0.3 + familyBonus * 0.2;
}

export { MIDataService };
export const miDataService = new MIDataService();
