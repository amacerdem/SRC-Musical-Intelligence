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
        if (c.isSpotifyConnected) {
          // Spotify mode: trigger sync after brief delay for playback to start
          try {
            await SpotifyService.play();
          } catch { /* best-effort */ }
          setTimeout(() => c.syncPlaybackState(), 500);
        } else {
          // Demo mode: find track in MI dataset and set as current
          const trackId = action.track_id ?? "";
          const catalogTrack = miDataService.findTrack(trackId);
          if (catalogTrack) {
            const mockTrack = MIDataService.toMockTrack(catalogTrack);
            c.setCurrentTrack(mockTrack);
            c.setIsPlaying(true);
            c.setProgressMs(0);
            c.setDurationMs(catalogTrack.duration_s * 1000);
          }
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

      case "get_now_playing":
        // No frontend action needed — agent gets context from tool result
        break;
    }
  }, []);

  return { handleAction };
}
