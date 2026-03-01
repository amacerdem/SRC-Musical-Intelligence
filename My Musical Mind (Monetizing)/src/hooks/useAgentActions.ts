/**
 * useAgentActions — Bridge between agent action events and player controls.
 *
 * When the LLM agent calls tools like play_track or control_playback,
 * the SSE stream emits "action" events. This hook dispatches those
 * actions to the appropriate player service (Spotify or demo mode).
 *
 * When Spotify is connected, searches Spotify's catalog and plays
 * full-length tracks via Spotify Connect. Falls back to MI catalog
 * when Spotify is not connected.
 */

import { useCallback, useRef } from "react";
import { SpotifyService } from "@/services/spotify";
import { miDataService, MIDataService } from "@/services/MIDataService";
import type { AgentAction } from "@/services/agent";
import type { MockTrack } from "@/services/SpotifySimulator";

export interface PlayerControls {
  isSpotifyConnected: boolean;
  setCurrentTrack: (t: MockTrack | null) => void;
  setIsPlaying: (p: boolean) => void;
  setProgressMs: (ms: number) => void;
  setDurationMs: (ms: number) => void;
  setQueueTracks?: (tracks: MockTrack[]) => void;
  syncPlaybackState: () => Promise<void>;
  handlePlayPause: () => Promise<void>;
  handleNext: () => Promise<void>;
  handlePrev: () => Promise<void>;
  handleShuffle: () => Promise<void>;
  handleRepeat: () => Promise<void>;
  handleVolume: (pct: number) => Promise<void>;
  volume: number;
}

/** Search Spotify and play the first result, updating UI with real track data */
async function spotifySearchAndPlay(
  trackName: string,
  artist: string | undefined,
  c: PlayerControls,
): Promise<boolean> {
  try {
    const query = artist ? `${trackName} ${artist}` : trackName;
    const results = await SpotifyService.searchTracks(query, 3);
    if (results.length === 0) return false;

    const hit = results[0];
    // Update UI immediately with Spotify data
    c.setCurrentTrack({
      id: hit.id,
      name: hit.name,
      artist: hit.artist,
      albumArt: hit.albumArt,
      durationSec: Math.round(hit.durationMs / 1000),
      dominantFamily: "Explorers",
      genre: "Unknown",
      features: {
        energy: 0.5, valence: 0.5, tempo: 120, danceability: 0.5,
        acousticness: 0.3, harmonicComplexity: 0.5, timbralBrightness: 0.5,
      },
    });
    c.setIsPlaying(true);
    c.setProgressMs(0);
    c.setDurationMs(hit.durationMs);

    // Play on Spotify
    await SpotifyService.playTrack(hit.uri);
    // Sync full state after a short delay
    setTimeout(() => c.syncPlaybackState(), 1000);
    return true;
  } catch {
    return false;
  }
}

export function useAgentActions(controls: PlayerControls) {
  const controlsRef = useRef(controls);
  controlsRef.current = controls;

  const handleAction = useCallback(async (action: AgentAction) => {
    const c = controlsRef.current;

    switch (action.type) {
      case "play_track": {
        // ── Spotify path: search & play full-length track ──
        if (c.isSpotifyConnected && action.track_name) {
          const played = await spotifySearchAndPlay(action.track_name, action.artist, c);
          if (played) break;
          // If Spotify search failed, fall through to MI catalog
        }

        // ── MI catalog fallback ──
        const trackId = action.track_id ?? "";
        let catalogTrack = trackId ? miDataService.findTrack(trackId) : undefined;
        if (!catalogTrack) {
          catalogTrack = miDataService.findTrackFuzzy(action.track_name, action.artist);
        }

        if (catalogTrack) {
          const mockTrack = MIDataService.toMockTrack(catalogTrack);
          c.setCurrentTrack(mockTrack);
          c.setIsPlaying(true);
          c.setProgressMs(0);
          c.setDurationMs(Math.max(catalogTrack.duration_s, 180) * 1000);
        } else if (action.track_name) {
          c.setCurrentTrack({
            id: trackId || `agent_${Date.now()}`,
            name: action.track_name,
            artist: action.artist ?? "Unknown",
            albumArt: "",
            durationSec: 240,
            dominantFamily: "Explorers",
            genre: "Unknown",
            features: {
              energy: 0.5, valence: 0.5, tempo: 120, danceability: 0.5,
              acousticness: 0.3, harmonicComplexity: 0.5, timbralBrightness: 0.5,
            },
          });
          c.setIsPlaying(true);
          c.setProgressMs(0);
          c.setDurationMs(240_000);
        }

        if (c.isSpotifyConnected) {
          try { await SpotifyService.play(); } catch { /* best-effort */ }
          setTimeout(() => c.syncPlaybackState(), 500);
        }
        break;
      }

      case "control_playback": {
        switch (action.command) {
          case "pause":
            c.setIsPlaying(false);
            if (c.isSpotifyConnected) {
              try { await SpotifyService.pause(); } catch { /* best-effort */ }
            }
            break;
          case "resume":
            await c.handlePlayPause();
            break;
          case "next":
            await c.handleNext();
            break;
          case "previous":
            await c.handlePrev();
            break;
          case "volume_up":
            await c.handleVolume(Math.min(100, c.volume + 20));
            break;
          case "volume_down":
            await c.handleVolume(Math.max(0, c.volume - 20));
            break;
          case "shuffle_toggle":
            await c.handleShuffle();
            break;
          case "repeat_cycle":
            await c.handleRepeat();
            break;
        }
        break;
      }

      case "queue_tracks": {
        const tracks = action.tracks ?? [];
        if (tracks.length === 0) break;

        // ── Spotify path: search each track, play first, queue rest ──
        if (c.isSpotifyConnected) {
          try {
            const resolved: { uri: string; name: string; artist: string; albumArt: string; durationMs: number; id: string }[] = [];
            for (const t of tracks) {
              const query = t.artist ? `${t.track_name} ${t.artist}` : t.track_name;
              const results = await SpotifyService.searchTracks(query, 1);
              if (results.length > 0) resolved.push(results[0]);
            }

            if (resolved.length > 0) {
              const [first, ...rest] = resolved;
              // Play first track
              c.setCurrentTrack({
                id: first.id,
                name: first.name,
                artist: first.artist,
                albumArt: first.albumArt,
                durationSec: Math.round(first.durationMs / 1000),
                dominantFamily: "Explorers",
                genre: "Unknown",
                features: {
                  energy: 0.5, valence: 0.5, tempo: 120, danceability: 0.5,
                  acousticness: 0.3, harmonicComplexity: 0.5, timbralBrightness: 0.5,
                },
              });
              c.setIsPlaying(true);
              c.setProgressMs(0);
              c.setDurationMs(first.durationMs);
              await SpotifyService.playTrack(first.uri);

              // Queue rest in Spotify
              for (const r of rest) {
                try { await SpotifyService.addToQueue(r.uri); } catch { /* best-effort */ }
              }

              // Also populate UI queue for visual display
              if (c.setQueueTracks) {
                c.setQueueTracks(rest.map((r) => ({
                  id: r.id,
                  name: r.name,
                  artist: r.artist,
                  albumArt: r.albumArt,
                  durationSec: Math.round(r.durationMs / 1000),
                  dominantFamily: "Explorers" as const,
                  genre: "Unknown",
                  features: {
                    energy: 0.5, valence: 0.5, tempo: 120, danceability: 0.5,
                    acousticness: 0.3, harmonicComplexity: 0.5, timbralBrightness: 0.5,
                  },
                })));
              }

              setTimeout(() => c.syncPlaybackState(), 1000);
              break;
            }
          } catch { /* fall through to MI catalog */ }
        }

        // ── MI catalog fallback ──
        const mockTracks: MockTrack[] = tracks.map((t) => {
          const catalogTrack = miDataService.findTrack(t.track_id);
          if (catalogTrack) return MIDataService.toMockTrack(catalogTrack);
          return {
            id: t.track_id,
            name: t.track_name,
            artist: t.artist,
            albumArt: "",
            durationSec: 240,
            dominantFamily: (t.dominant_family ?? "Explorers") as MockTrack["dominantFamily"],
            genre: "Unknown",
            features: {
              energy: 0.5, valence: 0.5, tempo: 120, danceability: 0.5,
              acousticness: 0.3, harmonicComplexity: 0.5, timbralBrightness: 0.5,
            },
          };
        });

        const [first, ...rest] = mockTracks;
        c.setCurrentTrack(first);
        c.setIsPlaying(true);
        c.setProgressMs(0);
        c.setDurationMs(first.durationSec * 1000);
        if (c.setQueueTracks) c.setQueueTracks(rest);

        if (c.isSpotifyConnected) {
          try { await SpotifyService.play(); } catch { /* best-effort */ }
          setTimeout(() => c.syncPlaybackState(), 500);
        }
        break;
      }

      case "get_now_playing":
        // No frontend action needed — agent gets context from tool result
        break;
    }
  }, []);

  return { handleAction };
}
