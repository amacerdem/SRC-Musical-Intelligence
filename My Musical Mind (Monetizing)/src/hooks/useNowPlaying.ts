/* ── useNowPlaying — Current track state for Dashboard ────────────────
 *  Polls Spotify if connected; falls back to demo mode with MI dataset.
 *  Auto-starts demo when Spotify is not connected.
 *  ──────────────────────────────────────────────────────────────────── */

import { useState, useEffect, useCallback, useRef } from "react";
import { isConnected, getCurrentlyPlaying } from "@/services/spotify";
import { SpotifySimulator } from "@/services/SpotifySimulator";
import type { MockTrack } from "@/services/SpotifySimulator";

interface NowPlayingState {
  track: MockTrack | null;
  isPlaying: boolean;
  isDemo: boolean;
  toggleDemo: () => void;
}

export function useNowPlaying(): NowPlayingState {
  const [track, setTrack] = useState<MockTrack | null>(null);
  const [isDemo, setIsDemo] = useState(!isConnected());
  const demoTimerRef = useRef<ReturnType<typeof setInterval>>();
  const spotifyTimerRef = useRef<ReturnType<typeof setInterval>>();

  const toggleDemo = useCallback(() => {
    setIsDemo((prev) => {
      if (!prev) {
        // Turning demo ON — clear spotify polling
        setTrack(null);
      }
      return !prev;
    });
  }, []);

  // Spotify polling (real mode)
  useEffect(() => {
    if (isDemo || !isConnected()) return;

    let cancelled = false;

    const poll = async () => {
      try {
        const current = await getCurrentlyPlaying();
        if (!cancelled) setTrack(current);
      } catch {
        if (!cancelled) setTrack(null);
      }
    };

    poll();
    spotifyTimerRef.current = setInterval(poll, 10_000);

    return () => {
      cancelled = true;
      if (spotifyTimerRef.current) clearInterval(spotifyTimerRef.current);
    };
  }, [isDemo]);

  // Demo mode — load a mock track, cycle every 45s
  useEffect(() => {
    if (!isDemo) return;

    let cancelled = false;

    const loadTrack = async () => {
      try {
        const t = await SpotifySimulator.getCurrentTrack();
        if (!cancelled) setTrack(t);
      } catch {
        /* silent */
      }
    };

    loadTrack();
    demoTimerRef.current = setInterval(loadTrack, 45_000);

    return () => {
      cancelled = true;
      if (demoTimerRef.current) clearInterval(demoTimerRef.current);
    };
  }, [isDemo]);

  return {
    track,
    isPlaying: !!track,
    isDemo,
    toggleDemo,
  };
}
