/**
 * Spotify OAuth PKCE + Web API Service (Browser)
 *
 * Uses standard browser redirect flow with PKCE (no client secret needed).
 * Returns data in MockTrack-compatible format so M³ pipeline works unchanged.
 */
import type { NeuralFamily } from "@/types/mind";
import type { MockTrack } from "./SpotifySimulator";

/* ── Config ─────────────────────────────────────────────────────────── */

const SPOTIFY_CLIENT_ID = "8be4267057ac4bd69f18e63112a1a92f";

const SCOPES = [
  "user-read-recently-played",
  "user-top-read",
  "user-library-read",
  "user-read-currently-playing",
].join(" ");

const REDIRECT_URI = "http://127.0.0.1:5174/callback";

const STORAGE_KEYS = {
  accessToken: "spotify_access_token",
  refreshToken: "spotify_refresh_token",
  expiresAt: "spotify_expires_at",
  codeVerifier: "spotify_code_verifier",
  oauthState: "spotify_oauth_state",
  preAuthPath: "spotify_pre_auth_path",
  preAuthUserName: "spotify_pre_auth_username",
  preAuthPlatform: "spotify_pre_auth_platform",
} as const;

const API_BASE = "https://api.spotify.com/v1";

/* ── PKCE Helpers ───────────────────────────────────────────────────── */

function generateRandomString(length: number): string {
  const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~";
  const values = crypto.getRandomValues(new Uint8Array(length));
  return Array.from(values, (v) => possible[v % possible.length]).join("");
}

async function sha256(plain: string): Promise<ArrayBuffer> {
  const encoder = new TextEncoder();
  return crypto.subtle.digest("SHA-256", encoder.encode(plain));
}

function base64urlEncode(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let str = "";
  for (const b of bytes) str += String.fromCharCode(b);
  return btoa(str).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

/* ── Auth Flow ──────────────────────────────────────────────────────── */

/**
 * Start the Spotify OAuth PKCE flow by redirecting to Spotify's authorize page.
 * Call this when the user taps the Spotify connect button.
 */
export async function startAuthFlow(meta?: { userName?: string; fromPath?: string; platform?: string }): Promise<void> {
  const codeVerifier = generateRandomString(128);
  const codeChallenge = base64urlEncode(await sha256(codeVerifier));
  const state = generateRandomString(32);

  // Store PKCE verifier + state for the callback
  sessionStorage.setItem(STORAGE_KEYS.codeVerifier, codeVerifier);
  sessionStorage.setItem(STORAGE_KEYS.oauthState, state);

  // Store pre-auth context so callback can resume the flow
  if (meta?.userName) sessionStorage.setItem(STORAGE_KEYS.preAuthUserName, meta.userName);
  if (meta?.fromPath) sessionStorage.setItem(STORAGE_KEYS.preAuthPath, meta.fromPath);
  if (meta?.platform) sessionStorage.setItem(STORAGE_KEYS.preAuthPlatform, meta.platform);

  const params = new URLSearchParams({
    client_id: SPOTIFY_CLIENT_ID,
    response_type: "code",
    redirect_uri: REDIRECT_URI,
    scope: SCOPES,
    state,
    code_challenge_method: "S256",
    code_challenge: codeChallenge,
  });

  window.location.href = `https://accounts.spotify.com/authorize?${params.toString()}`;
}

/**
 * Handle the OAuth callback. Call this from the /callback page.
 * Returns tokens + pre-auth context, or throws on error.
 */
export async function handleCallback(searchParams: URLSearchParams): Promise<{
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
  userName: string;
  fromPath: string;
  platform: string;
}> {
  const code = searchParams.get("code");
  const state = searchParams.get("state");
  const error = searchParams.get("error");

  if (error) throw new Error(`Spotify auth error: ${error}`);
  if (!code) throw new Error("No authorization code received");

  // Verify state
  const storedState = sessionStorage.getItem(STORAGE_KEYS.oauthState);
  if (state !== storedState) throw new Error("State mismatch — possible CSRF attack");

  const codeVerifier = sessionStorage.getItem(STORAGE_KEYS.codeVerifier);
  if (!codeVerifier) throw new Error("No code verifier found");

  // Exchange code for tokens
  const res = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: SPOTIFY_CLIENT_ID,
      grant_type: "authorization_code",
      code,
      redirect_uri: REDIRECT_URI,
      code_verifier: codeVerifier,
    }),
  });

  if (!res.ok) {
    const errBody = await res.text();
    throw new Error(`Token exchange failed: ${res.status} ${errBody}`);
  }

  const data = await res.json();
  const expiresAt = Date.now() + (data.expires_in ?? 3600) * 1000;

  // Persist tokens
  localStorage.setItem(STORAGE_KEYS.accessToken, data.access_token);
  localStorage.setItem(STORAGE_KEYS.refreshToken, data.refresh_token ?? "");
  localStorage.setItem(STORAGE_KEYS.expiresAt, String(expiresAt));

  // Retrieve pre-auth context
  const userName = sessionStorage.getItem(STORAGE_KEYS.preAuthUserName) ?? "";
  const fromPath = sessionStorage.getItem(STORAGE_KEYS.preAuthPath) ?? "/onboarding";
  const platform = sessionStorage.getItem(STORAGE_KEYS.preAuthPlatform) ?? "spotify";

  // Clean up session storage
  sessionStorage.removeItem(STORAGE_KEYS.codeVerifier);
  sessionStorage.removeItem(STORAGE_KEYS.oauthState);
  sessionStorage.removeItem(STORAGE_KEYS.preAuthUserName);
  sessionStorage.removeItem(STORAGE_KEYS.preAuthPath);
  sessionStorage.removeItem(STORAGE_KEYS.preAuthPlatform);

  return { accessToken: data.access_token, refreshToken: data.refresh_token ?? "", expiresAt, userName, fromPath, platform };
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
        client_id: SPOTIFY_CLIENT_ID,
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
  return "Explorers";
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
  const featuresData = await apiFetch<{
    audio_features: (SpotifyAudioFeatures | null)[];
  }>(`/audio-features?ids=${ids}`);

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
  startAuthFlow,
  handleCallback,
  refreshAccessToken,
  getValidToken,
  clearTokens,
  isConnected,
  getTopTracks,
  getRecentlyPlayed,
  getCurrentlyPlaying,
  getSavedTracks,
  getInitialBatch,
};

// Debug: expose to browser console
if (typeof window !== "undefined") {
  (window as any).SpotifyService = SpotifyService;
}
