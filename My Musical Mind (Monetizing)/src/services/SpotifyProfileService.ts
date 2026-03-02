/**
 * Spotify → MI Profile Service
 *
 * After Spotify OAuth, calls the backend to fetch the user's listening
 * library and compute their MI profile (genes, dimensions, persona).
 */
import type { MindGenes, GeneName } from "@/types/m3";
import type { NeuralFamily } from "@/types/mind";
import { getValidToken } from "@/services/spotify";

/* ── Types ─────────────────────────────────────────────────────────── */

export interface SpotifyMITrack {
  id: string;
  title: string;
  artist: string;
  album_art: string;
  duration_s: number;
  genres: string[];
  signal: {
    energy: number;
    valence: number;
    tempo: number;
    danceability: number;
    acousticness: number;
    harmonicComplexity: number;
    timbralBrightness: number;
    duration: number;
  };
  genes: MindGenes;
  dominant_family: string;
  dominant_gene: string;
  dimensions_6d: number[];
  source: "spotify_audio_features" | "genre_heuristic";
}

export interface SpotifyMIProfile {
  spotify_user: {
    id: string;
    display_name: string;
    product: string;
  };
  stats: {
    total_tracks: number;
    total_minutes: number;
    unique_artists: number;
    unique_genres: number;
  };
  genes: MindGenes;
  dominant_family: NeuralFamily;
  dominant_gene: GeneName;
  persona_id: number;
  persona_name: string;
  dimensions_6d: number[];
  dimensions_12d: number[];
  dimensions_24d: number[];
  family_distribution: Record<string, number>;
  genre_distribution: Record<string, number>;
  tracks: SpotifyMITrack[];
  listening_diversity: {
    genre_entropy: number;
    artist_entropy: number;
    tempo_range: number;
    taste_shift: number;
  };
}

/* ── API ───────────────────────────────────────────────────────────── */

export async function fetchSpotifyMIProfile(): Promise<SpotifyMIProfile | null> {
  const token = await getValidToken();
  if (!token) return null;

  try {
    const res = await fetch("/api/spotify/profile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ access_token: token }),
    });

    if (!res.ok) {
      console.error("[SpotifyProfile] Backend error:", res.status);
      return null;
    }

    return (await res.json()) as SpotifyMIProfile;
  } catch (err) {
    console.error("[SpotifyProfile] Fetch failed:", err);
    return null;
  }
}
