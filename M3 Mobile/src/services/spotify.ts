/**
 * Spotify OAuth PKCE + Web API Service
 *
 * Uses expo-auth-session for PKCE flow (no client secret needed).
 * Returns data in MockTrack-compatible format so M³ pipeline works unchanged.
 */
import * as AuthSession from "expo-auth-session";
import * as WebBrowser from "expo-web-browser";
import AsyncStorage from "@react-native-async-storage/async-storage";
import type { NeuralFamily } from "../types/mind";
import type { MockTrack } from "./SpotifySimulator";

/* ── Config ─────────────────────────────────────────────────────────── */

const SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"; // Replace with your Spotify Developer App client ID

const SCOPES = [
  "user-read-recently-played",
  "user-top-read",
  "user-library-read",
  "user-read-currently-playing",
];

const discovery: AuthSession.DiscoveryDocument = {
  authorizationEndpoint: "https://accounts.spotify.com/authorize",
  tokenEndpoint: "https://accounts.spotify.com/api/token",
};

const STORAGE_KEYS = {
  accessToken: "spotify_access_token",
  refreshToken: "spotify_refresh_token",
  expiresAt: "spotify_expires_at",
};

const API_BASE = "https://api.spotify.com/v1";

/* ── Auth Helpers ───────────────────────────────────────────────────── */

WebBrowser.maybeCompleteAuthSession();

const redirectUri = AuthSession.makeRedirectUri({ scheme: "m3mind" });

export function getAuthRequest() {
  return new AuthSession.AuthRequest({
    clientId: SPOTIFY_CLIENT_ID,
    scopes: SCOPES,
    redirectUri,
    usePKCE: true,
    responseType: AuthSession.ResponseType.Code,
  });
}

/** Exchange authorization code for access + refresh tokens */
export async function exchangeCode(
  code: string,
  request: AuthSession.AuthRequest,
): Promise<{ accessToken: string; refreshToken: string; expiresAt: number }> {
  const result = await AuthSession.exchangeCodeAsync(
    {
      clientId: SPOTIFY_CLIENT_ID,
      code,
      redirectUri,
      extraParams: { code_verifier: request.codeVerifier! },
    },
    discovery,
  );

  const expiresAt = Date.now() + (result.expiresIn ?? 3600) * 1000;

  await AsyncStorage.multiSet([
    [STORAGE_KEYS.accessToken, result.accessToken],
    [STORAGE_KEYS.refreshToken, result.refreshToken ?? ""],
    [STORAGE_KEYS.expiresAt, String(expiresAt)],
  ]);

  return {
    accessToken: result.accessToken,
    refreshToken: result.refreshToken ?? "",
    expiresAt,
  };
}

/** Refresh the access token using the stored refresh token */
export async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = await AsyncStorage.getItem(STORAGE_KEYS.refreshToken);
  if (!refreshToken) return null;

  try {
    const result = await AuthSession.refreshAsync(
      { clientId: SPOTIFY_CLIENT_ID, refreshToken },
      discovery,
    );

    const expiresAt = Date.now() + (result.expiresIn ?? 3600) * 1000;

    await AsyncStorage.multiSet([
      [STORAGE_KEYS.accessToken, result.accessToken],
      [STORAGE_KEYS.expiresAt, String(expiresAt)],
    ]);

    if (result.refreshToken) {
      await AsyncStorage.setItem(STORAGE_KEYS.refreshToken, result.refreshToken);
    }

    return result.accessToken;
  } catch {
    return null;
  }
}

/** Get a valid access token (refreshing if expired) */
export async function getValidToken(): Promise<string | null> {
  const [token, expiresAtStr] = await AsyncStorage.multiGet([
    STORAGE_KEYS.accessToken,
    STORAGE_KEYS.expiresAt,
  ]);

  const accessToken = token[1];
  const expiresAt = Number(expiresAtStr[1] ?? 0);

  if (!accessToken) return null;

  // Refresh 60s before expiry
  if (Date.now() > expiresAt - 60_000) {
    return refreshAccessToken();
  }

  return accessToken;
}

/** Clear stored tokens (logout) */
export async function clearTokens(): Promise<void> {
  await AsyncStorage.multiRemove(Object.values(STORAGE_KEYS));
}

/** Check if we have stored tokens */
export async function isConnected(): Promise<boolean> {
  const token = await AsyncStorage.getItem(STORAGE_KEYS.accessToken);
  return !!token;
}

/* ── API Helpers ────────────────────────────────────────────────────── */

async function apiFetch<T>(path: string): Promise<T> {
  const token = await getValidToken();
  if (!token) throw new Error("No valid Spotify token");

  const res = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    throw new Error(`Spotify API ${res.status}: ${path}`);
  }

  return res.json() as Promise<T>;
}

/* ── Spotify API Types (minimal) ────────────────────────────────────── */

interface SpotifyTrack {
  id: string;
  name: string;
  artists: { name: string }[];
  album: { images: { url: string }[] };
  duration_ms: number;
}

interface SpotifyAudioFeatures {
  id: string;
  energy: number;
  valence: number;
  tempo: number;
  danceability: number;
  acousticness: number;
  instrumentalness: number;
  speechiness: number;
}

/* ── Genre → NeuralFamily mapping ───────────────────────────────────── */

const GENRE_FAMILY_MAP: Record<string, NeuralFamily> = {
  electronic: "Kineticists",
  dance: "Kineticists",
  edm: "Kineticists",
  "drum and bass": "Kineticists",
  house: "Kineticists",
  techno: "Kineticists",
  classical: "Architects",
  jazz: "Architects",
  "art rock": "Architects",
  progressive: "Architects",
  ambient: "Alchemists",
  experimental: "Explorers",
  "avant-garde": "Explorers",
  idm: "Explorers",
  folk: "Anchors",
  "singer-songwriter": "Anchors",
  soul: "Anchors",
  "r&b": "Anchors",
  pop: "Anchors",
  rock: "Alchemists",
  metal: "Alchemists",
  "hip-hop": "Explorers",
  rap: "Explorers",
};

function guessFamily(genres: string[]): NeuralFamily {
  for (const g of genres) {
    const lower = g.toLowerCase();
    for (const [key, family] of Object.entries(GENRE_FAMILY_MAP)) {
      if (lower.includes(key)) return family;
    }
  }
  return "Explorers"; // default
}

function guessGenre(genres: string[]): string {
  return genres[0] ?? "Unknown";
}

/* ── Convert Spotify data → MockTrack ───────────────────────────────── */

function toMockTrack(
  track: SpotifyTrack,
  features: SpotifyAudioFeatures | null,
  artistGenres: string[],
): MockTrack {
  const f = features ?? {
    energy: 0.5,
    valence: 0.5,
    tempo: 120,
    danceability: 0.5,
    acousticness: 0.5,
    instrumentalness: 0.5,
    speechiness: 0.5,
  };

  return {
    id: track.id,
    name: track.name,
    artist: track.artists.map((a) => a.name).join(", "),
    albumArt: track.album.images[0]?.url ?? "",
    features: {
      energy: f.energy,
      valence: f.valence,
      tempo: f.tempo,
      danceability: f.danceability,
      acousticness: f.acousticness,
      harmonicComplexity:
        f.instrumentalness * 0.7 + (1 - f.speechiness) * 0.3,
      timbralBrightness: f.energy * 0.5 + (1 - f.acousticness) * 0.5,
    },
    dominantFamily: guessFamily(artistGenres),
    genre: guessGenre(artistGenres),
    durationSec: Math.round(track.duration_ms / 1000),
  };
}

/* ── Public API Methods ─────────────────────────────────────────────── */

/** Get user's top tracks (short/medium/long term) */
export async function getTopTracks(
  timeRange: "short_term" | "medium_term" | "long_term" = "medium_term",
  limit = 50,
): Promise<MockTrack[]> {
  const data = await apiFetch<{ items: SpotifyTrack[] }>(
    `/me/top/tracks?time_range=${timeRange}&limit=${limit}`,
  );

  if (data.items.length === 0) return [];

  // Fetch audio features in batch
  const ids = data.items.map((t) => t.id).join(",");
  const featuresData = await apiFetch<{
    audio_features: (SpotifyAudioFeatures | null)[];
  }>(`/audio-features?ids=${ids}`);

  // Fetch top artists for genre info
  const artistData = await apiFetch<{
    items: { genres: string[] }[];
  }>(`/me/top/artists?time_range=${timeRange}&limit=20`);
  const topGenres = artistData.items.flatMap((a) => a.genres);

  return data.items.map((track, i) =>
    toMockTrack(track, featuresData.audio_features[i], topGenres),
  );
}

/** Get recently played tracks */
export async function getRecentlyPlayed(limit = 50): Promise<MockTrack[]> {
  const data = await apiFetch<{
    items: { track: SpotifyTrack; played_at: string }[];
  }>(`/me/player/recently-played?limit=${limit}`);

  if (data.items.length === 0) return [];

  const tracks = data.items.map((i) => i.track);
  const ids = tracks.map((t) => t.id).join(",");
  const featuresData = await apiFetch<{
    audio_features: (SpotifyAudioFeatures | null)[];
  }>(`/audio-features?ids=${ids}`);

  return tracks.map((track, i) =>
    toMockTrack(track, featuresData.audio_features[i], []),
  );
}

/** Get currently playing track */
export async function getCurrentlyPlaying(): Promise<MockTrack | null> {
  try {
    const data = await apiFetch<{
      is_playing: boolean;
      item: SpotifyTrack | null;
    }>("/me/player/currently-playing");

    if (!data.item) return null;

    const featuresData = await apiFetch<{
      audio_features: (SpotifyAudioFeatures | null)[];
    }>(`/audio-features?ids=${data.item.id}`);

    return toMockTrack(data.item, featuresData.audio_features[0], []);
  } catch {
    return null;
  }
}

/** Get user's saved/liked tracks */
export async function getSavedTracks(limit = 50): Promise<MockTrack[]> {
  const data = await apiFetch<{
    items: { track: SpotifyTrack }[];
  }>(`/me/tracks?limit=${limit}`);

  if (data.items.length === 0) return [];

  const tracks = data.items.map((i) => i.track);
  const ids = tracks.map((t) => t.id).join(",");
  const featuresData = await apiFetch<{
    audio_features: (SpotifyAudioFeatures | null)[];
  }>(`/audio-features?ids=${ids}`);

  return tracks.map((track, i) =>
    toMockTrack(track, featuresData.audio_features[i], []),
  );
}

/** Gather initial batch for onboarding (top tracks across all time ranges) */
export async function getInitialBatch(): Promise<MockTrack[]> {
  const [shortTerm, mediumTerm, longTerm] = await Promise.all([
    getTopTracks("short_term", 20),
    getTopTracks("medium_term", 20),
    getTopTracks("long_term", 20),
  ]);

  // Deduplicate by track id
  const seen = new Set<string>();
  const all: MockTrack[] = [];
  for (const track of [...shortTerm, ...mediumTerm, ...longTerm]) {
    if (!seen.has(track.id)) {
      seen.add(track.id);
      all.push(track);
    }
  }

  return all;
}

export const SpotifyService = {
  getAuthRequest,
  exchangeCode,
  refreshAccessToken,
  getValidToken,
  clearTokens,
  isConnected,
  getTopTracks,
  getRecentlyPlayed,
  getCurrentlyPlaying,
  getSavedTracks,
  getInitialBatch,
  redirectUri,
  discovery,
};
