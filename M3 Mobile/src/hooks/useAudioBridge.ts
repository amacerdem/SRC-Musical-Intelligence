/* ── useAudioBridge — Connect AudioPlayer ↔ useM3AudioStore ────────────
 *  This hook bridges the imperative AudioPlayer singleton with the
 *  reactive Zustand store. It handles:
 *    - Playing/pausing/resuming audio when store state changes
 *    - Loading tracks via bundled asset require() map
 *    - Time updates from AudioPlayer → store
 *    - Viz param generation from AudioAnalyzerSim → store at ~30fps
 *    - Auto-skip to next track on track end
 *    - Cleanup on unmount or mode change to idle
 *
 *  Usage: Call useAudioBridge() in M3HubScreen (or any screen that
 *  manages audio playback).
 *  ──────────────────────────────────────────────────────────────── */

import { useEffect, useRef } from "react";
import { useM3AudioStore } from "../stores/useM3AudioStore";
import { audioPlayer } from "../services/AudioPlayer";
import { audioAnalyzerSim } from "../services/AudioAnalyzerSim";
import { resolveAudioAsset } from "../data/audio-assets";

export function useAudioBridge() {
  const mode = useM3AudioStore((s) => s.mode);
  const playlist = useM3AudioStore((s) => s.playlist);
  const currentTrackIdx = useM3AudioStore((s) => s.currentTrackIdx);
  const isPlaying = useM3AudioStore((s) => s.isPlaying);

  const prevTrackIdxRef = useRef(-1);
  const prevIsPlayingRef = useRef(false);
  const isLoadingRef = useRef(false);
  const vizIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Initialize audio on mount
  useEffect(() => {
    audioPlayer.initialize();

    return () => {
      audioPlayer.dispose();
      audioAnalyzerSim.clear();
      stopVizUpdates();
    };
  }, []);

  // Register time update callback
  useEffect(() => {
    const unsubTime = audioPlayer.onTimeUpdate((time) => {
      useM3AudioStore.getState().setCurrentTime(time);
    });

    const unsubEnded = audioPlayer.onEnded(() => {
      // Auto-skip to next track
      const state = useM3AudioStore.getState();
      if (state.playlist.length > 0) {
        state.skipTrack();
      }
    });

    return () => {
      unsubTime();
      unsubEnded();
    };
  }, []);

  // Handle track changes: load + play new track
  useEffect(() => {
    if (mode !== "playing" || playlist.length === 0) return;

    const track = playlist[currentTrackIdx];
    if (!track) return;

    // Only load if track actually changed
    if (currentTrackIdx === prevTrackIdxRef.current && prevIsPlayingRef.current) {
      return;
    }

    prevTrackIdxRef.current = currentTrackIdx;
    isLoadingRef.current = true;

    const loadAndPlay = async () => {
      try {
        // Resolve bundled asset
        const asset = resolveAudioAsset(track.audioFile);
        if (asset !== undefined) {
          await audioPlayer.playAsset(asset);
        } else {
          // Fallback: try URI
          await audioPlayer.play(track.audioFile);
        }

        // Set duration
        const dur = await audioPlayer.getDuration();
        useM3AudioStore.getState().setDuration(dur || track.durationSec);

        // Set track profile for viz simulation
        audioAnalyzerSim.setTrackProfile(track.r3Profile, track.c3Profile);

        // Start viz updates
        startVizUpdates();
      } catch (err) {
        console.warn("[AudioBridge] Error loading track:", err);
      } finally {
        isLoadingRef.current = false;
      }
    };

    loadAndPlay();
  }, [mode, currentTrackIdx, playlist]);

  // Handle play/pause toggle
  useEffect(() => {
    if (mode !== "playing" || isLoadingRef.current) return;

    // Skip the first render where we haven't loaded yet
    if (prevTrackIdxRef.current === -1) return;

    if (isPlaying && !prevIsPlayingRef.current) {
      audioPlayer.resume();
      startVizUpdates();
    } else if (!isPlaying && prevIsPlayingRef.current) {
      audioPlayer.pause();
      stopVizUpdates();
    }

    prevIsPlayingRef.current = isPlaying;
  }, [isPlaying, mode]);

  // Handle mode switch to idle — stop everything
  useEffect(() => {
    if (mode === "idle") {
      audioPlayer.stop();
      audioAnalyzerSim.clear();
      stopVizUpdates();
      prevTrackIdxRef.current = -1;
      prevIsPlayingRef.current = false;
    }
  }, [mode]);

  // Viz param update loop (~30fps)
  function startVizUpdates() {
    stopVizUpdates();
    vizIntervalRef.current = setInterval(() => {
      const params = audioAnalyzerSim.getParams();
      useM3AudioStore.getState().setVizParams(params);
    }, 33); // ~30fps
  }

  function stopVizUpdates() {
    if (vizIntervalRef.current) {
      clearInterval(vizIntervalRef.current);
      vizIntervalRef.current = null;
    }
  }
}
