import { useEffect, useState } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import AudioPlayer from '../components/audio/AudioPlayer';
import Waveform from '../components/audio/Waveform';
import Spectrogram from '../components/audio/Spectrogram';
import { useAudioStore } from '../stores/audioStore';
import { fetchJSON, fetchBinary } from '../api/client';
import { colors, R3_GROUPS } from '../design/tokens';

interface AudioFile {
  name: string;
  filename: string;
  duration: number;
  sample_rate: number;
  channels: number;
}

export default function Dashboard() {
  const [audioFiles, setAudioFiles] = useState<AudioFile[]>([]);
  const [loading, setLoading] = useState(true);
  const { currentFile, setCurrentFile, setWaveformEnvelope, setSpectrogramData, setDuration } = useAudioStore();

  useEffect(() => {
    fetchJSON<AudioFile[]>('/audio/list')
      .then(setAudioFiles)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const selectFile = async (file: AudioFile) => {
    setCurrentFile(file.filename);
    setDuration(file.duration);

    // Load waveform envelope
    try {
      const { data } = await fetchBinary(`/audio/waveform/${encodeURIComponent(file.filename)}`);
      setWaveformEnvelope(new Float32Array(data));
    } catch (e) {
      console.error('Failed to load waveform:', e);
    }

    // Load spectrogram
    try {
      const { data, headers } = await fetchBinary(`/audio/spectrogram/${encodeURIComponent(file.filename)}`);
      const nMels = parseInt(headers.get('X-N-Mels') || '128');
      const nFrames = parseInt(headers.get('X-N-Frames') || '0');
      setSpectrogramData(new Float32Array(data), nMels, nFrames);
    } catch (e) {
      console.error('Failed to load spectrogram:', e);
    }
  };

  const formatDuration = (d: number) => {
    const m = Math.floor(d / 60);
    const s = Math.floor(d % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex flex-col gap-4 p-4 h-full overflow-y-auto">
      {/* Header metrics */}
      <div className="flex gap-3">
        {[
          { label: 'Audio Files', value: audioFiles.length.toString(), accent: colors.r3 },
          { label: 'Kernel', value: 'v4.0', accent: colors.c3 },
          { label: 'R³ Features', value: '97D', accent: colors.r3 },
          { label: 'C³ Beliefs', value: '131', accent: colors.c3 },
        ].map(({ label, value, accent }) => (
          <GlassPanel key={label} small className="flex-1 p-4">
            <div className="text-xs mb-1" style={{ color: 'var(--text-muted)' }}>{label}</div>
            <div className="text-xl font-semibold font-data" style={{ color: accent }}>{value}</div>
          </GlassPanel>
        ))}
      </div>

      {/* Audio player (if file selected) */}
      {currentFile && (
        <GlassPanel className="p-4" glow="r3">
          <div className="mb-3">
            <AudioPlayer />
          </div>
          <Waveform height={60} />
          <div className="mt-2">
            <Spectrogram height={100} />
          </div>
          <div className="flex items-center gap-2 mt-2">
            {R3_GROUPS.map((g) => (
              <span
                key={g.key}
                className="text-xs font-data px-1.5 py-0.5 rounded"
                style={{ background: `${colors[`group${g.key}` as keyof typeof colors]}20`, color: colors[`group${g.key}` as keyof typeof colors] }}
              >
                {g.key}
              </span>
            ))}
          </div>
        </GlassPanel>
      )}

      {/* Audio file grid */}
      <div>
        <h2 className="text-sm font-medium mb-3" style={{ color: 'var(--text-secondary)' }}>
          Test Audio Library
        </h2>
        {loading ? (
          <div className="text-sm" style={{ color: 'var(--text-muted)' }}>Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {audioFiles.map((file) => (
              <GlassPanel
                key={file.filename}
                small
                className="p-4 cursor-pointer"
                onClick={() => selectFile(file)}
                style={{
                  borderColor: currentFile === file.filename ? colors.r3 + '40' : undefined,
                }}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{file.name}</div>
                    <div className="flex items-center gap-3 mt-1.5">
                      <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
                        {formatDuration(file.duration)}
                      </span>
                      <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
                        {(file.sample_rate / 1000).toFixed(1)}kHz
                      </span>
                    </div>
                  </div>
                  {currentFile === file.filename && (
                    <span
                      className="w-2 h-2 rounded-full mt-1.5"
                      style={{ background: colors.c3 }}
                    />
                  )}
                </div>
              </GlassPanel>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
