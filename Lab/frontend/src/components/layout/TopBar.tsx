import { useAudioStore } from '../../stores/audioStore';

export default function TopBar() {
  const { currentFile, duration, currentTime, isPlaying } = useAudioStore();

  const formatTime = (t: number) => {
    const m = Math.floor(t / 60);
    const s = Math.floor(t % 60);
    const ms = Math.floor((t % 1) * 100);
    return `${m}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(2, '0')}`;
  };

  return (
    <header
      className="glass-panel-sm flex items-center justify-between px-5 py-3"
      style={{ borderRadius: '0 0 16px 16px' }}
    >
      <div className="flex items-center gap-4">
        {currentFile ? (
          <>
            <span className="text-sm font-medium truncate" style={{ maxWidth: 300 }}>
              {currentFile}
            </span>
            <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
              {formatTime(duration)}
            </span>
          </>
        ) : (
          <span className="text-sm" style={{ color: 'var(--text-muted)' }}>
            No audio selected
          </span>
        )}
      </div>

      <div className="flex items-center gap-4">
        {currentFile && (
          <div className="flex items-center gap-2">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: isPlaying ? '#10b981' : 'var(--text-muted)' }}
            />
            <span className="font-data text-xs" style={{ color: 'var(--text-secondary)' }}>
              {formatTime(currentTime)}
            </span>
          </div>
        )}
      </div>
    </header>
  );
}
