import { useRef, useEffect, useCallback } from 'react';
import { useAudioStore } from '../../stores/audioStore';
import { audioStreamUrl } from '../../api/client';

/**
 * Audio playback engine — manages Web Audio API context, provides
 * play/pause/seek and drives the global currentTime for cursor sync.
 */
export default function AudioPlayer() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const rafRef = useRef<number>(0);

  const {
    currentFile,
    isPlaying,
    setPlaying,
    setCurrentTime,
    setDuration,
  } = useAudioStore();

  // Create/update audio element when file changes
  useEffect(() => {
    if (!currentFile) return;

    const audio = new Audio(audioStreamUrl(currentFile));
    audio.preload = 'auto';
    audioRef.current = audio;

    audio.addEventListener('loadedmetadata', () => {
      setDuration(audio.duration);
    });

    audio.addEventListener('ended', () => {
      setPlaying(false);
      setCurrentTime(0);
    });

    return () => {
      audio.pause();
      audio.src = '';
      audioRef.current = null;
      cancelAnimationFrame(rafRef.current);
    };
  }, [currentFile, setDuration, setPlaying, setCurrentTime]);

  // Animation loop for cursor sync
  const tick = useCallback(() => {
    const audio = audioRef.current;
    if (audio && !audio.paused) {
      setCurrentTime(audio.currentTime);
      rafRef.current = requestAnimationFrame(tick);
    }
  }, [setCurrentTime]);

  // Play/pause sync
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

  const togglePlay = () => {
    if (!currentFile) return;
    setPlaying(!isPlaying);
  };

  const seek = (fraction: number) => {
    const audio = audioRef.current;
    if (!audio) return;
    const t = fraction * audio.duration;
    audio.currentTime = t;
    setCurrentTime(t);
  };

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={togglePlay}
        className="w-8 h-8 rounded-lg flex items-center justify-center text-sm transition-colors"
        style={{
          background: isPlaying ? 'rgba(16, 185, 129, 0.15)' : 'rgba(255,255,255,0.06)',
          color: isPlaying ? '#10b981' : 'var(--text-secondary)',
          border: '1px solid rgba(255,255,255,0.08)',
        }}
        disabled={!currentFile}
      >
        {isPlaying ? '❚❚' : '▶'}
      </button>

      {/* Seek bar */}
      <div
        className="flex-1 h-1.5 rounded-full cursor-pointer relative"
        style={{ background: 'rgba(255,255,255,0.06)', minWidth: 100 }}
        onClick={(e) => {
          const rect = e.currentTarget.getBoundingClientRect();
          seek((e.clientX - rect.left) / rect.width);
        }}
      >
        <div
          className="absolute inset-y-0 left-0 rounded-full"
          style={{
            width: `${(useAudioStore.getState().currentTime / Math.max(useAudioStore.getState().duration, 0.01)) * 100}%`,
            background: 'var(--r3)',
            transition: 'width 50ms linear',
          }}
        />
      </div>
    </div>
  );
}
