/**
 * useAgentActions — Bridge between agent action events and player controls.
 *
 * When the LLM agent calls tools like play_track or control_playback,
 * the SSE stream emits "action" events. This hook dispatches those
 * actions to the appropriate player service (Spotify or demo mode).
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

export function useAgentActions(controls: PlayerControls) {
  const controlsRef = useRef(controls);
  controlsRef.current = controls;

  const handleAction = useCallback(async (action: AgentAction) => {
    const c = controlsRef.current;

    switch (action.type) {
      case "play_track": {
        // Resolve track: try ID first, then fuzzy name/artist match
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
          c.setDurationMs(catalogTrack.duration_s * 1000);
        } else if (action.track_name) {
          // No catalog match — create mock from action data so UI still updates
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

        // Sync Spotify if connected
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

        // Build mock tracks from the action data
        const mockTracks: MockTrack[] = tracks.map((t) => {
          const catalogTrack = miDataService.findTrack(t.track_id);
          if (catalogTrack) return MIDataService.toMockTrack(catalogTrack);
          // Fallback: create minimal mock from action data
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

        // Set first track as current, rest as queue
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
