/* ── Audio synchronization for visualization ─────────────────────── */

import { useState, useEffect, useRef, useCallback } from "react";

export function useAudioSync(src: string, duration: number) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    const audio = new Audio(src);
    audio.preload = "auto";
    audioRef.current = audio;

    const onTimeUpdate = () => setCurrentTime(audio.currentTime);
    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);
    const onEnded = () => { setIsPlaying(false); setCurrentTime(0); };

    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);
    audio.addEventListener("ended", onEnded);

    return () => {
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
      audio.removeEventListener("ended", onEnded);
      audio.pause();
    };
  }, [src]);

  const togglePlay = useCallback(() => {
    const a = audioRef.current;
    if (!a) return;
    if (a.paused) a.play().catch(() => {});
    else a.pause();
  }, []);

  const seek = useCallback((t: number) => {
    const a = audioRef.current;
    if (!a) return;
    a.currentTime = t;
    setCurrentTime(t);
  }, []);

  return { currentTime, isPlaying, togglePlay, seek, audioRef };
}

/** Convert audio currentTime → trace index with fractional interpolation */
export function getFrameInterp(currentTime: number, duration: number, tracePoints: number) {
  const progress = Math.max(0, Math.min(1, currentTime / Math.max(0.01, duration))) * (tracePoints - 1);
  const i = Math.floor(progress);
  const frac = progress - i;
  return { index: i, frac, nextIndex: Math.min(i + 1, tracePoints - 1) };
}

/** Interpolate a value from a trace array at the current time */
export function sampleTrace(trace: number[], index: number, frac: number, nextIndex: number): number {
  return trace[index] * (1 - frac) + trace[nextIndex] * frac;
}
