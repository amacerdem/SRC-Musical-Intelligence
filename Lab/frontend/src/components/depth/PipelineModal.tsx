import { useEffect, useState } from 'react';
import { useAudioStore } from '../../stores/audioStore';
import { usePipelineStore } from '../../stores/pipelineStore';
import { fetchJSON, fetchBinary, postJSON } from '../../api/client';
import { colors } from '../../design/tokens';

interface AudioFile {
  name: string;
  filename: string;
  duration: number;
  sample_rate: number;
  channels: number;
}

interface RunResponse {
  experiment_id: string;
  status: string;
  audio_name: string;
}

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function PipelineModal({ open, onClose }: Props) {
  const [audioFiles, setAudioFiles] = useState<AudioFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>('');
  const [excerptDuration, setExcerptDuration] = useState(30);
  const [useExcerpt, setUseExcerpt] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [log, setLog] = useState<string[]>([]);

  const { setCurrentFile, setDuration, setWaveformEnvelope, setSpectrogramData } = useAudioStore();
  const {
    isRunning, runPhase,
    setRunning, setRunPhase, setRunProgress,
    setCurrentExperimentId, setR3Data, setH3Data, setRewardData, setRamData,
    setExperiments, clearResults,
  } = usePipelineStore();

  useEffect(() => {
    if (open) {
      fetchJSON<AudioFile[]>('/audio/list').then(setAudioFiles).catch(() => {});
    }
  }, [open]);

  const addLog = (msg: string) => setLog((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);

  const runPipeline = async () => {
    if (!selectedFile) return;
    setRunning(true);
    setError(null);
    setLog([]);
    clearResults();
    addLog(`Starting pipeline on: ${selectedFile}`);
    setRunPhase('loading');
    setRunProgress(0);

    try {
      // Set audio
      setCurrentFile(selectedFile);
      const file = audioFiles.find((f) => f.filename === selectedFile);
      if (file) setDuration(file.duration);

      // Load waveform + spectrogram
      try {
        const { data } = await fetchBinary(`/audio/waveform/${encodeURIComponent(selectedFile)}`);
        setWaveformEnvelope(new Float32Array(data));
      } catch {}
      try {
        const { data, headers } = await fetchBinary(`/audio/spectrogram/${encodeURIComponent(selectedFile)}`);
        const nMels = parseInt(headers.get('X-N-Mels') || '128');
        const nFrames = parseInt(headers.get('X-N-Frames') || '0');
        setSpectrogramData(new Float32Array(data), nMels, nFrames);
      } catch {}

      addLog(`Config: excerpt=${useExcerpt ? excerptDuration + 's' : 'full'}`);
      const response = await postJSON<RunResponse>('/pipeline/run', {
        audio_name: selectedFile,
        excerpt_duration: useExcerpt ? excerptDuration : null,
      });

      addLog(`Pipeline complete! Experiment: ${response.experiment_id}`);
      setCurrentExperimentId(response.experiment_id);

      // Load R3
      const { data: r3Data, headers: r3Headers } = await fetchBinary(
        `/pipeline/results/${response.experiment_id}/r3`
      );
      const r3Frames = parseInt(r3Headers.get('X-N-Frames') || '0');
      const r3Names = (r3Headers.get('X-Feature-Names') || '').split(',');
      setR3Data(new Float32Array(r3Data), r3Names, r3Frames);
      addLog(`R\u00B3: ${r3Frames} frames \u00D7 97 features`);

      // Load H3
      try {
        const { data: h3TupleData, headers: h3Headers } = await fetchBinary(
          `/pipeline/results/${response.experiment_id}/h3`
        );
        const nTuples = parseInt(h3Headers.get('X-N-Tuples') || '0');
        const tupleBytes = nTuples * 4 * 4; // 4 ints per tuple, 4 bytes each
        const tuples = new Int32Array(h3TupleData.slice(0, tupleBytes));
        const values = new Float32Array(h3TupleData.slice(tupleBytes));
        setH3Data(tuples, values, nTuples);
        addLog(`H\u00B3: ${nTuples} tuples loaded`);
      } catch {
        addLog('H\u00B3 data not available');
      }

      // Load reward
      try {
        const { data: rewData } = await fetchBinary(
          `/pipeline/results/${response.experiment_id}/c3/reward`
        );
        setRewardData(new Float32Array(rewData));
        const rew = new Float32Array(rewData);
        addLog(`Reward: mean=${(rew.reduce((a, b) => a + b, 0) / rew.length).toFixed(4)}`);
      } catch {
        addLog('Reward not available');
      }

      // Load RAM
      try {
        const { data: ramBin } = await fetchBinary(
          `/pipeline/results/${response.experiment_id}/c3/ram`
        );
        setRamData(new Float32Array(ramBin));
        addLog('RAM: 26 regions loaded');
      } catch {}

      // Refresh experiments
      const exps = await fetchJSON<any[]>('/experiments/list');
      setExperiments(exps);

      setRunPhase('done');
      setRunProgress(1);
      addLog('All data loaded. Ready.');

      // Close modal after success
      setTimeout(onClose, 800);
    } catch (e: any) {
      setError(e.message || 'Pipeline failed');
      addLog(`ERROR: ${e.message}`);
      setRunPhase('error');
    } finally {
      setRunning(false);
    }
  };

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center"
      style={{ background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)' }}
      onClick={(e) => { if (e.target === e.currentTarget && !isRunning) onClose(); }}
    >
      <div
        className="glass-panel p-6 w-full max-w-lg"
        style={{ maxHeight: '80vh', overflow: 'auto' }}
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold" style={{ color: colors.c3 }}>Run Pipeline</h2>
          {!isRunning && (
            <button onClick={onClose} className="text-xs px-2 py-1 rounded-lg" style={{ color: 'var(--text-muted)' }}>
              Close
            </button>
          )}
        </div>

        {/* Audio selection */}
        <select
          className="w-full px-3 py-2 rounded-xl text-sm mb-3"
          style={{
            background: 'rgba(255,255,255,0.04)',
            border: '1px solid rgba(255,255,255,0.08)',
            color: 'var(--text-primary)',
          }}
          value={selectedFile}
          onChange={(e) => setSelectedFile(e.target.value)}
          disabled={isRunning}
        >
          <option value="">Select audio file...</option>
          {audioFiles.map((f) => (
            <option key={f.filename} value={f.filename}>
              {f.name} ({Math.floor(f.duration / 60)}:{String(Math.floor(f.duration % 60)).padStart(2, '0')})
            </option>
          ))}
        </select>

        {/* Excerpt */}
        <div className="flex items-center gap-3 mb-4">
          <label className="flex items-center gap-2 text-sm cursor-pointer">
            <input
              type="checkbox"
              checked={useExcerpt}
              onChange={(e) => setUseExcerpt(e.target.checked)}
              className="rounded"
              disabled={isRunning}
            />
            <span style={{ color: 'var(--text-secondary)' }}>Excerpt</span>
          </label>
          {useExcerpt && (
            <>
              <input
                type="number"
                value={excerptDuration}
                onChange={(e) => setExcerptDuration(Number(e.target.value))}
                className="w-16 px-2 py-1 rounded-lg text-sm font-data text-center"
                style={{
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  color: 'var(--text-primary)',
                }}
                min={5}
                max={600}
                disabled={isRunning}
              />
              <span className="text-xs" style={{ color: 'var(--text-muted)' }}>seconds</span>
            </>
          )}
        </div>

        {/* Run button */}
        <button
          onClick={runPipeline}
          disabled={!selectedFile || isRunning}
          className="w-full py-2.5 rounded-xl text-sm font-medium transition-all mb-4"
          style={{
            background: isRunning ? 'rgba(255,255,255,0.04)' : `${colors.c3}20`,
            color: isRunning ? 'var(--text-muted)' : colors.c3,
            border: `1px solid ${isRunning ? 'rgba(255,255,255,0.06)' : colors.c3 + '30'}`,
          }}
        >
          {isRunning ? `Running... (${runPhase})` : 'Run Pipeline'}
        </button>

        {error && (
          <div className="glass-panel-sm p-3 mb-3" style={{ borderColor: `${colors.danger}30` }}>
            <span className="text-sm" style={{ color: colors.danger }}>{error}</span>
          </div>
        )}

        {/* Console */}
        {log.length > 0 && (
          <div
            className="glass-panel-sm p-3 font-data text-xs space-y-0.5"
            style={{ color: 'var(--text-secondary)', maxHeight: 200, overflow: 'auto' }}
          >
            {log.map((line, i) => (
              <div key={i} style={{ color: line.includes('ERROR') ? colors.danger : undefined }}>
                {line}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
