/* ── M3NowPlayingBar — Spotify-style player for M³ ──────────────── */

import { useRef, useEffect } from "react";
import { Play, Pause, SkipForward, SkipBack, Volume2, Square } from "lucide-react";
import { useM3AudioStore } from "@/stores/useM3AudioStore";

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${String(s).padStart(2, "0")}`;
}

interface Props {
  accentColor: string;
  onStop: () => void;
}

export function M3NowPlayingBar({ accentColor, onStop }: Props) {
  const playlist = useM3AudioStore((s) => s.playlist);
  const currentTrackIdx = useM3AudioStore((s) => s.currentTrackIdx);
  const isPlaying = useM3AudioStore((s) => s.isPlaying);

  const barRef = useRef<HTMLDivElement>(null);
  const timeRef = useRef<HTMLSpanElement>(null);
  const frameRef = useRef<number>(0);

  const track = playlist[currentTrackIdx];

  // 60fps progress bar via direct DOM
  useEffect(() => {
    let running = true;
    const tick = () => {
      if (!running) return;
      const state = useM3AudioStore.getState();
      const t = state.playlist[state.currentTrackIdx];
      if (t) {
        const progress = state.currentTime / t.durationSec;
        if (barRef.current) {
          barRef.current.style.width = `${Math.min(progress * 100, 100)}%`;
        }
        if (timeRef.current) {
          timeRef.current.textContent = `${formatTime(state.currentTime)} / ${formatTime(t.durationSec)}`;
        }
      }
      frameRef.current = requestAnimationFrame(tick);
    };
    frameRef.current = requestAnimationFrame(tick);
    return () => { running = false; cancelAnimationFrame(frameRef.current); };
  }, []);

  if (!track) return null;

  return (
    <div className="px-3 py-3">
      {/* Track info */}
      <div className="flex items-center gap-2.5 mb-2">
        {/* Equalizer / dot */}
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 relative overflow-hidden"
          style={{ background: `${accentColor}12`, border: `1px solid ${accentColor}18` }}
        >
          {isPlaying ? (
            <div className="flex items-end gap-[2px] h-3.5">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="w-[2.5px] rounded-full origin-bottom"
                  style={{
                    background: accentColor,
                    animation: "eq 0.8s ease-in-out infinite",
                    animationDelay: `${i * 0.15}s`,
                    height: "100%",
                  }}
                />
              ))}
            </div>
          ) : (
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: `${accentColor}50` }} />
          )}
        </div>

        <div className="flex-1 min-w-0">
          <p className="text-[11px] font-display font-medium text-slate-300 truncate">
            {track.name}
          </p>
          <p className="text-[9px] font-mono text-slate-600 truncate">
            {track.artist} · {track.genre}
          </p>
        </div>
      </div>

      {/* Progress bar */}
      <div className="flex items-center gap-2 mb-2.5">
        <div className="flex-1 h-[3px] rounded-full bg-white/[0.06] overflow-hidden">
          <div
            ref={barRef}
            className="h-full rounded-full transition-none"
            style={{
              background: accentColor,
              boxShadow: `0 0 8px ${accentColor}40`,
              width: "0%",
            }}
          />
        </div>
        <span
          ref={timeRef}
          className="text-[8px] font-mono text-slate-600 tabular-nums shrink-0 w-[68px] text-right"
        >
          0:00 / {formatTime(track.durationSec)}
        </span>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-center gap-2">
        <button
          onClick={() => useM3AudioStore.getState().prevTrack()}
          className="w-7 h-7 rounded-full flex items-center justify-center text-slate-500 hover:text-slate-300 transition-colors"
        >
          <SkipBack size={13} />
        </button>

        <button
          onClick={() => useM3AudioStore.getState().togglePlay()}
          className="w-9 h-9 rounded-full flex items-center justify-center transition-all"
          style={{
            background: `${accentColor}18`,
            border: `1px solid ${accentColor}28`,
          }}
        >
          {isPlaying ? (
            <Pause size={15} style={{ color: accentColor }} />
          ) : (
            <Play size={15} style={{ color: accentColor, marginLeft: 1 }} />
          )}
        </button>

        <button
          onClick={() => useM3AudioStore.getState().skipTrack()}
          className="w-7 h-7 rounded-full flex items-center justify-center text-slate-500 hover:text-slate-300 transition-colors"
        >
          <SkipForward size={13} />
        </button>

        <div className="w-px h-4 bg-white/5 mx-1" />

        <button
          onClick={onStop}
          className="w-6 h-6 rounded-full flex items-center justify-center text-slate-600 hover:text-red-400 transition-colors"
          title="Stop"
        >
          <Square size={10} />
        </button>

        <button
          className="w-6 h-6 rounded-full flex items-center justify-center text-slate-600 hover:text-slate-400 transition-colors"
          title="Volume"
        >
          <Volume2 size={11} />
        </button>
      </div>
    </div>
  );
}
