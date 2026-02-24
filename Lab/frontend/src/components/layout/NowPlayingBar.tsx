import { useRef, useEffect, useCallback } from 'react';
import { useAudioStore } from '../../stores/audioStore';
import { audioStreamUrl } from '../../api/client';
import { colors, FRAME_RATE } from '../../design/tokens';

export default function NowPlayingBar() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const rafRef = useRef<number>(0);

  const {
    currentFile, duration, currentTime, isPlaying,
    setPlaying, setCurrentTime, setDuration,
    waveformEnvelope,
  } = useAudioStore();

  // Create audio element
  useEffect(() => {
    if (!currentFile) return;
    const audio = new Audio(audioStreamUrl(currentFile));
    audio.preload = 'auto';
    audioRef.current = audio;
    audio.addEventListener('loadedmetadata', () => setDuration(audio.duration));
    audio.addEventListener('ended', () => { setPlaying(false); setCurrentTime(0); });
    return () => { audio.pause(); audio.src = ''; audioRef.current = null; cancelAnimationFrame(rafRef.current); };
  }, [currentFile, setDuration, setPlaying, setCurrentTime]);

  const tick = useCallback(() => {
    const audio = audioRef.current;
    if (audio && !audio.paused) {
      setCurrentTime(audio.currentTime);
      rafRef.current = requestAnimationFrame(tick);
    }
  }, [setCurrentTime]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.play().catch(() => setPlaying(false));
      rafRef.current = requestAnimationFrame(tick);
    } else {
      audio.pause();
      cancelAnimationFrame(rafRef.current);
    }
  }, [isPlaying, tick, setPlaying]);

  const seek = (fraction: number) => {
    const audio = audioRef.current;
    if (!audio) return;
    const t = fraction * audio.duration;
    audio.currentTime = t;
    setCurrentTime(t);
  };

  const formatTime = (t: number) => {
    const m = Math.floor(t / 60);
    const s = Math.floor(t % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  if (!currentFile) return null;

  const progress = duration > 0 ? currentTime / duration : 0;
  const frame = Math.floor(currentTime * FRAME_RATE);

  return (
    <div className="now-playing-bar px-4 py-2">
      <div className="flex items-center gap-4 max-w-full">
        {/* Play / Pause */}
        <button
          onClick={() => setPlaying(!isPlaying)}
          className="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0 transition-colors"
          style={{
            background: isPlaying ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255,255,255,0.06)',
            color: isPlaying ? '#10b981' : 'var(--text-secondary)',
            border: '1px solid rgba(255,255,255,0.08)',
          }}
        >
          {isPlaying ? '\u275A\u275A' : '\u25B6'}
        </button>

        {/* File info */}
        <div className="flex flex-col min-w-0 flex-shrink-0" style={{ maxWidth: 180 }}>
          <span className="text-xs font-medium truncate">{currentFile}</span>
          <span className="font-data text-[10px]" style={{ color: 'var(--text-muted)' }}>
            {formatTime(currentTime)} / {formatTime(duration)}
          </span>
        </div>

        {/* Progress bar with mini waveform */}
        <div
          className="flex-1 h-6 relative cursor-pointer rounded-lg overflow-hidden"
          style={{ background: 'rgba(255,255,255,0.03)' }}
          onClick={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            seek((e.clientX - rect.left) / rect.width);
          }}
        >
          {/* Waveform background */}
          {waveformEnvelope && (
            <WaveMini data={waveformEnvelope} progress={progress} />
          )}

          {/* Progress overlay */}
          <div
            className="absolute inset-y-0 left-0"
            style={{
              width: `${progress * 100}%`,
              background: `${colors.r3}15`,
            }}
          />

          {/* Cursor line */}
          <div
            className="absolute top-0 bottom-0 w-px"
            style={{
              left: `${progress * 100}%`,
              background: colors.r3,
            }}
          />
        </div>

        {/* Frame counter */}
        <span className="font-data text-[10px] flex-shrink-0" style={{ color: 'var(--text-muted)', minWidth: 60, textAlign: 'right' }}>
          f{frame}
        </span>
      </div>
    </div>
  );
}

/** Tiny waveform rendered as inline SVG polyline */
function WaveMini({ data, progress }: { data: Float32Array; progress: number }) {
  const n = Math.min(data.length, 200);
  const step = Math.max(1, Math.floor(data.length / n));
  let points = '';
  for (let i = 0; i < n; i++) {
    const idx = i * step;
    const x = (i / n) * 100;
    const y = 50 - data[idx] * 48;
    points += `${x},${y} `;
  }

  return (
    <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
      <polyline
        points={points}
        fill="none"
        stroke="rgba(255,255,255,0.08)"
        strokeWidth="1"
        vectorEffect="non-scaling-stroke"
      />
    </svg>
  );
}
