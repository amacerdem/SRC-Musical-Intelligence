/**
 * Spotify OAuth + Web API Service (Browser)
 *
 * Auth flow delegates to Repetuare backend (server-side OAuth with client secret).
 * Tokens are stored in localStorage for direct Spotify API calls from the browser.
 * Returns data in MockTrack-compatible format so M³ pipeline works unchanged.
 */
import type { NeuralFamily } from "@/types/mind";
import type { MockTrack } from "./SpotifySimulator";

/* ── Config ─────────────────────────────────────────────────────────── */

const STORAGE_KEYS = {
  accessToken: "spotify_access_token",
  refreshToken: "spotify_refresh_token",
  expiresAt: "spotify_expires_at",
  preAuthPath: "spotify_pre_auth_path",
  preAuthUserName: "spotify_pre_auth_username",
} as const;

const API_BASE = "https://api.spotify.com/v1";

/* ── Auth Flow (via Repetuare backend) ─────────────────────────────── */

/**
 * Start the Spotify OAuth flow via backend.
 * Stores pre-auth context, then redirects to the backend login endpoint
 * which generates the Spotify authorization URL.
 */
export function startAuthFlow(meta?: { userName?: string; fromPath?: string; platform?: string }): void {
  // Store pre-auth context so callback can resume the flow
  if (meta?.userName) sessionStorage.setItem(STORAGE_KEYS.preAuthUserName, meta.userName);
  if (meta?.fromPath) sessionStorage.setItem(STORAGE_KEYS.preAuthPath, meta.fromPath);

  // Redirect to backend login — it generates the Spotify auth URL and redirects
  window.location.href = "/api/spotify/login";
}

/** Refresh the access token using the stored refresh token */
export async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = localStorage.getItem(STORAGE_KEYS.refreshToken);
  if (!refreshToken) return null;

  try {
    const res = await fetch("https://accounts.spotify.com/api/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: "8be4267057ac4bd69f18e63112a1a92f",
        grant_type: "refresh_token",
        refresh_token: refreshToken,
      }),
    });

    if (!res.ok) return null;

    const data = await res.json();
    const expiresAt = Date.now() + (data.expires_in ?? 3600) * 1000;

    localStorage.setItem(STORAGE_KEYS.accessToken, data.access_token);
    localStorage.setItem(STORAGE_KEYS.expiresAt, String(expiresAt));
    if (data.refresh_token) {
      localStorage.setItem(STORAGE_KEYS.refreshToken, data.refresh_token);
    }

    return data.access_token;
  } catch {
    return null;
  }
}

/** Get a valid access token (refreshing if expired) */
export async function getValidToken(): Promise<string | null> {
  const accessToken = localStorage.getItem(STORAGE_KEYS.accessToken);
  const expiresAt = Number(localStorage.getItem(STORAGE_KEYS.expiresAt) ?? 0);

  if (!accessToken) return null;

  // Refresh 60s before expiry
  if (Date.now() > expiresAt - 60_000) {
    return refreshAccessToken();
  }

  return accessToken;
}

/** Clear stored tokens (logout) */
export function clearTokens(): void {
  localStorage.removeItem(STORAGE_KEYS.accessToken);
  localStorage.removeItem(STORAGE_KEYS.refreshToken);
  localStorage.removeItem(STORAGE_KEYS.expiresAt);
}

/** Check if we have stored tokens */
export function isConnected(): boolean {
  return !!localStorage.getItem(STORAGE_KEYS.accessToken);
}

/* ── API Helpers ────────────────────────────────────────────────────── */

/**
 * Tracks endpoints that returned 401/403, suppressing repeated calls for 60s.
 * Key = path prefix (e.g. "/me/player"), value = timestamp when block expires.
 */
const _blockedEndpoints: Map<string, number> = new Map();
const BLOCK_TTL_MS = 60_000; // suppress retries for 60s

function endpointBlockKey(path: string): string {
  // Normalize: strip query params
  const base = path.split("?")[0];
  // These two endpoints use different scopes — don't group with /me/player
  if (base === "/me/player/recently-played") return base;
  if (base === "/me/player/currently-playing") return base;
  // Group playback-control endpoints (/me/player, /me/player/queue, etc.)
  if (base.startsWith("/me/player")) return "/me/player";
  if (base.startsWith("/me/playlists")) return "/me/playlists";
  return base;
}

async function apiFetch<T>(path: string): Promise<T> {
  const token = await getValidToken();
  if (!token) throw new Error("No valid Spotify token");

  // Check if this endpoint family is temporarily blocked
  const blockKey = endpointBlockKey(path);
  const blockedUntil = _blockedEndpoints.get(blockKey);
  if (blockedUntil && Date.now() < blockedUntil) {
    throw new Error(`Spotify API blocked (cached): ${blockKey}`);
  }

  const res = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    // Cache 401/403 to prevent polling spam
    if (res.status === 401 || res.status === 403) {
      _blockedEndpoints.set(blockKey, Date.now() + BLOCK_TTL_MS);
    }
    throw new Error(`Spotify API ${res.status}: ${path}`);
  }

  // Clear any previous block on success
  _blockedEndpoints.delete(blockKey);

  return res.json() as Promise<T>;
}

/** PUT/POST helper for player control endpoints (no JSON body expected back) */
async function apiCommand(path: string, method: "PUT" | "POST" = "PUT"): Promise<void> {
  const token = await getValidToken();
  if (!token) throw new Error("No valid Spotify token");

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: { Authorization: `Bearer ${token}` },
  });

  // 204 No Content is the expected success for player endpoints
  if (!res.ok && res.status !== 204) {
    throw new Error(`Spotify API ${res.status}: ${path}`);
  }
}

/**
 * Try to fetch audio features; returns null array on 403 (deprecated endpoint).
 * Caches the 403 result so subsequent calls skip the network request entirely.
 */
let _audioFeaturesBlocked = false;
async function fetchAudioFeatures(ids: string): Promise<(SpotifyAudioFeatures | null)[]> {
  if (_audioFeaturesBlocked) return ids.split(",").map(() => null);
  try {
    const data = await apiFetch<{ audio_features: (SpotifyAudioFeatures | null)[] }>(
      `/audio-features?ids=${ids}`,
    );
    return data.audio_features;
  } catch {
    _audioFeaturesBlocked = true;
    return ids.split(",").map(() => null);
  }
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

interface SpotifyArtist {
  id: string;
  name: string;
  genres: string[];
  images: { url: string }[];
  followers: { total: number };
  popularity: number;
}

export interface SpotifyUserProfile {
  id: string;
  display_name: string;
  images: { url: string }[];
  followers: { total: number };
  product: string; // "free" | "premium" etc.
  country: string;
}

export interface SpotifyArtistInfo {
  id: string;
  name: string;
  image: string;
  genres: string[];
  followers: number;
  popularity: number;
  family: NeuralFamily;
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
    if (!g) continue;
    const lower = g.toLowerCase();
    for (const [key, family] of Object.entries(GENRE_FAMILY_MAP)) {
      if (lower.includes(key)) return family;
    }
  }
  return "Explorers";
}

function guessGenre(genres: string[]): string {
  return genres.find((g) => !!g) ?? "Unknown";
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
      harmonicComplexity: f.instrumentalness * 0.7 + (1 - f.speechiness) * 0.3,
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

  const ids = data.items.map((t) => t.id).join(",");
  const [features, artistData] = await Promise.all([
    fetchAudioFeatures(ids),
    apiFetch<{ items: { genres: string[] }[] }>(
      `/me/top/artists?time_range=${timeRange}&limit=20`,
    ),
  ]);
  const topGenres = artistData.items.flatMap((a) => a.genres ?? []).filter(Boolean);

  return data.items.map((track, i) =>
    toMockTrack(track, features[i], topGenres),
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
  const features = await fetchAudioFeatures(ids);

  return tracks.map((track, i) =>
    toMockTrack(track, features[i], []),
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

    const features = await fetchAudioFeatures(data.item.id);
    return toMockTrack(data.item, features[0], []);
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
  const features = await fetchAudioFeatures(ids);

  return tracks.map((track, i) =>
    toMockTrack(track, features[i], []),
  );
}

/** Gather initial batch for onboarding (top tracks across all time ranges) */
export async function getInitialBatch(): Promise<MockTrack[]> {
  const [shortTerm, mediumTerm, longTerm] = await Promise.all([
    getTopTracks("short_term", 20),
    getTopTracks("medium_term", 20),
    getTopTracks("long_term", 20),
  ]);

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

/* ── Playback State ────────────────────────────────────────────────── */

export interface PlaybackState {
  is_playing: boolean;
  progress_ms: number;
  duration_ms: number;
  shuffle_state: boolean;
  repeat_state: "off" | "track" | "context";
  track: MockTrack | null;
}

/** Get full playback state (currently playing + progress + controls) */
export async function getPlaybackState(): Promise<PlaybackState | null> {
  try {
    const data = await apiFetch<{
      is_playing: boolean;
      progress_ms: number;
      item: SpotifyTrack | null;
      shuffle_state: boolean;
      repeat_state: "off" | "track" | "context";
    }>("/me/player");

    if (!data || !data.item) return null;

    const features = await fetchAudioFeatures(data.item.id);
    return {
      is_playing: data.is_playing,
      progress_ms: data.progress_ms ?? 0,
      duration_ms: data.item.duration_ms,
      shuffle_state: data.shuffle_state ?? false,
      repeat_state: data.repeat_state ?? "off",
      track: toMockTrack(data.item, features[0], []),
    };
  } catch {
    return null;
  }
}

/* ── Player Controls ──────────────────────────────────────────────── */

/** Resume / start playback */
export async function play(): Promise<void> {
  await apiCommand("/me/player/play");
}

/** Pause playback */
export async function pause(): Promise<void> {
  await apiCommand("/me/player/pause");
}

/** Skip to next track */
export async function skipToNext(): Promise<void> {
  await apiCommand("/me/player/next", "POST");
}

/** Skip to previous track */
export async function skipToPrevious(): Promise<void> {
  await apiCommand("/me/player/previous", "POST");
}

/** Toggle shuffle */
export async function setShuffle(state: boolean): Promise<void> {
  await apiCommand(`/me/player/shuffle?state=${state}`);
}

/** Set repeat mode */
export async function setRepeat(state: "off" | "track" | "context"): Promise<void> {
  await apiCommand(`/me/player/repeat?state=${state}`);
}

/** Set volume (0–100) */
export async function setVolume(percent: number): Promise<void> {
  await apiCommand(`/me/player/volume?volume_percent=${Math.round(percent)}`);
}

/** Seek to position in current track */
export async function seekTo(positionMs: number): Promise<void> {
  await apiCommand(`/me/player/seek?position_ms=${Math.round(positionMs)}`);
}

/* ── Additional Data Endpoints ────────────────────────────────────── */

/** Get user's Spotify profile */
export async function getUserProfile(): Promise<SpotifyUserProfile | null> {
  try {
    return await apiFetch<SpotifyUserProfile>("/me");
  } catch {
    return null;
  }
}

/** Get user's top artists */
export async function getTopArtists(
  timeRange: "short_term" | "medium_term" | "long_term" = "medium_term",
  limit = 20,
): Promise<SpotifyArtistInfo[]> {
  try {
    const data = await apiFetch<{ items: SpotifyArtist[] }>(
      `/me/top/artists?time_range=${timeRange}&limit=${limit}`,
    );
    return data.items.map((a) => ({
      id: a.id,
      name: a.name,
      image: a.images[0]?.url ?? "",
      genres: a.genres ?? [],
      followers: a.followers?.total ?? 0,
      popularity: a.popularity ?? 0,
      family: guessFamily(a.genres ?? []),
    }));
  } catch {
    return [];
  }
}

/** Get user's playlists */
export interface SpotifyPlaylistInfo {
  id: string;
  name: string;
  image: string;
  trackCount: number;
  owner: string;
  isPublic: boolean;
}

export async function getUserPlaylists(limit = 20): Promise<SpotifyPlaylistInfo[]> {
  try {
    const data = await apiFetch<{
      items: {
        id: string;
        name: string;
        images: { url: string }[];
        tracks: { total: number };
        owner: { display_name: string };
        public: boolean;
      }[];
    }>(`/me/playlists?limit=${limit}`);
    return data.items.map((p) => ({
      id: p.id,
      name: p.name,
      image: p.images[0]?.url ?? "",
      trackCount: p.tracks.total,
      owner: p.owner.display_name,
      isPublic: p.public ?? false,
    }));
  } catch {
    return [];
  }
}

/** Get the user's playback queue */
export async function getQueue(): Promise<{ currentTrack: MockTrack | null; queue: MockTrack[] }> {
  try {
    const data = await apiFetch<{
      currently_playing: SpotifyTrack | null;
      queue: SpotifyTrack[];
    }>("/me/player/queue");
    const allTracks = [data.currently_playing, ...data.queue].filter(Boolean) as SpotifyTrack[];
    const ids = allTracks.map((t) => t.id).join(",");
    const features = ids ? await fetchAudioFeatures(ids) : [];
    const current = data.currently_playing
      ? toMockTrack(data.currently_playing, features[0] ?? null, [])
      : null;
    const queue = data.queue.map((t, i) =>
      toMockTrack(t, features[i + (data.currently_playing ? 1 : 0)] ?? null, []),
    );
    return { currentTrack: current, queue };
  } catch {
    return { currentTrack: null, queue: [] };
  }
}

export const SpotifyService = {
  startAuthFlow,
  refreshAccessToken,
  getValidToken,
  clearTokens,
  isConnected,
  getTopTracks,
  getRecentlyPlayed,
  getCurrentlyPlaying,
  getSavedTracks,
  getInitialBatch,
  getPlaybackState,
  play,
  pause,
  skipToNext,
  skipToPrevious,
  setShuffle,
  setRepeat,
  setVolume,
  seekTo,
  getUserProfile,
  getTopArtists,
  getUserPlaylists,
  getQueue,
};

// Debug: expose to browser console
if (typeof window !== "undefined") {
  (window as any).SpotifyService = SpotifyService;
}
