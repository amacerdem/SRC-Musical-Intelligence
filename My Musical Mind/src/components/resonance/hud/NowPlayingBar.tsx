/* ── NowPlayingBar — Spotify-style play bar for self ─────────────── */

import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Play, Pause, SkipForward } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useResonanceStore, SELF_TRACKS } from "@/stores/useResonanceStore";

const ease = [0.22, 1, 0.36, 1] as const;
const ACCENT = "#A855F7";

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${String(s).padStart(2, "0")}`;
}

export function NowPlayingBar() {
  const { t } = useTranslation();
  const entranceComplete = useResonanceStore(s => s.entranceComplete);
  const isPlaying = useResonanceStore(s => s.isPlaying);
  const togglePlay = useResonanceStore(s => s.togglePlay);
  const skipTrack = useResonanceStore(s => s.skipTrack);
  const selfTrackIdx = useResonanceStore(s => s.selfTrackIdx);

  const barRef = useRef<HTMLDivElement>(null);
  const timeRef = useRef<HTMLSpanElement>(null);
  const frameRef = useRef<number>(0);

  const track = SELF_TRACKS[selfTrackIdx];

  // 60fps progress update via direct DOM
  useEffect(() => {
    let running = true;
    const tick = () => {
      if (!running) return;
      const state = useResonanceStore.getState();
      const progress = state.selfPlaybackTime / SELF_TRACKS[state.selfTrackIdx].duration;
      if (barRef.current) {
        barRef.current.style.width = `${Math.min(progress * 100, 100)}%`;
      }
      if (timeRef.current) {
        timeRef.current.textContent = `${formatTime(state.selfPlaybackTime)} / ${formatTime(SELF_TRACKS[state.selfTrackIdx].duration)}`;
      }
      frameRef.current = requestAnimationFrame(tick);
    };
    frameRef.current = requestAnimationFrame(tick);
    return () => { running = false; cancelAnimationFrame(frameRef.current); };
  }, []);

  if (!entranceComplete) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, filter: "blur(8px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      transition={{ duration: 0.8, ease, delay: 1.2 }}
      className="fixed bottom-6 left-[30%] -translate-x-1/2 z-[45] w-[340px] max-w-[calc(100vw-32px)]"
    >
      <div className="glass px-4 py-3 rounded-2xl">
        {/* Label */}
        <span className="text-[8px] font-display uppercase tracking-[0.25em] text-white/20 block mb-2">
          {isPlaying ? t("resonance.nowPlaying") : t("resonance.paused")}
        </span>

        {/* Track info + controls */}
        <div className="flex items-center gap-3">
          {/* Album art circle with equalizer */}
          <div
            className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 relative overflow-hidden"
            style={{ background: `${ACCENT}15`, border: `1px solid ${ACCENT}20` }}
          >
            {isPlaying ? (
              <div className="flex items-end gap-[2px] h-4">
                {[0.5, 1, 0.7].map((_, i) => (
                  <div
                    key={i}
                    className="w-[3px] rounded-full origin-bottom"
                    style={{
                      background: ACCENT,
                      animation: "eq 0.8s ease-in-out infinite",
                      animationDelay: `${i * 0.15}s`,
                      height: "100%",
                    }}
                  />
                ))}
              </div>
            ) : (
              <div className="w-3 h-3 rounded-full" style={{ background: `${ACCENT}60` }} />
            )}
          </div>

          {/* Title + artist */}
          <div className="flex-1 min-w-0">
            <div className="text-[12px] font-display font-medium text-slate-300 truncate">
              {track.title}
            </div>
            <div className="text-[10px] font-mono text-slate-600 truncate">
              {track.artist}
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-1.5 shrink-0">
            <button
              onClick={togglePlay}
              className="w-7 h-7 rounded-full flex items-center justify-center transition-colors"
              style={{ background: `${ACCENT}15`, border: `1px solid ${ACCENT}25` }}
            >
              {isPlaying ? (
                <Pause size={14} style={{ color: ACCENT }} />
              ) : (
                <Play size={14} style={{ color: ACCENT, marginLeft: 1 }} />
              )}
            </button>
            <button
              onClick={skipTrack}
              className="w-6 h-6 rounded-full flex items-center justify-center text-slate-600 hover:text-slate-400 transition-colors"
            >
              <SkipForward size={13} />
            </button>
          </div>
        </div>

        {/* Progress bar + time */}
        <div className="mt-2.5 flex items-center gap-2">
          <div className="flex-1 h-[3px] rounded-full bg-white/[0.06] overflow-hidden">
            <div
              ref={barRef}
              className="h-full rounded-full"
              style={{ background: ACCENT, boxShadow: `0 0 8px ${ACCENT}40`, width: "0%" }}
            />
          </div>
          <span
            ref={timeRef}
            className="text-[9px] font-mono text-slate-600 tabular-nums shrink-0 w-[72px] text-right"
          >
            0:00 / {formatTime(track.duration)}
          </span>
        </div>
      </div>
    </motion.div>
  );
}
