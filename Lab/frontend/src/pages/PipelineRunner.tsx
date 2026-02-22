import { useEffect, useState } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import { useAudioStore } from '../stores/audioStore';
import { usePipelineStore } from '../stores/pipelineStore';
import { fetchJSON, fetchBinary, postJSON } from '../api/client';
import { colors } from '../design/tokens';

interface AudioFile {
  name: string;
  filename: string;
  duration: number;
}

interface RunResponse {
  experiment_id: string;
  status: string;
  audio_name: string;
}

export default function PipelineRunner() {
  const [audioFiles, setAudioFiles] = useState<AudioFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>('');
  const [excerptDuration, setExcerptDuration] = useState<number>(30);
  const [useExcerpt, setUseExcerpt] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [log, setLog] = useState<string[]>([]);

  const {
    isRunning, runPhase, runProgress,
    setRunning, setRunPhase, setRunProgress,
    setCurrentExperimentId, setR3Data, setRewardData, setRamData,
    setExperiments,
  } = usePipelineStore();

  useEffect(() => {
    fetchJSON<AudioFile[]>('/audio/list').then(setAudioFiles);
    fetchJSON<any[]>('/experiments/list').then(setExperiments);
  }, [setExperiments]);

  const addLog = (msg: string) => setLog((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);

  const runPipeline = async () => {
    if (!selectedFile) return;
    setRunning(true);
    setError(null);
    setLog([]);
    addLog(`Starting pipeline on: ${selectedFile}`);
    setRunPhase('loading');
    setRunProgress(0);

    try {
      addLog(`Config: excerpt=${useExcerpt ? excerptDuration + 's' : 'full'}`);
      const response = await postJSON<RunResponse>('/pipeline/run', {
        audio_name: selectedFile,
        excerpt_duration: useExcerpt ? excerptDuration : null,
      });

      addLog(`Pipeline complete! Experiment: ${response.experiment_id}`);
      setCurrentExperimentId(response.experiment_id);

      // Load R³ results
      addLog('Loading R³ features...');
      const { data: r3Data, headers: r3Headers } = await fetchBinary(
        `/pipeline/results/${response.experiment_id}/r3`
      );
      const r3Frames = parseInt(r3Headers.get('X-N-Frames') || '0');
      const r3Names = (r3Headers.get('X-Feature-Names') || '').split(',');
      setR3Data(new Float32Array(r3Data), r3Names, r3Frames);
      addLog(`R³: ${r3Frames} frames × 97 features loaded`);

      // Load reward
      try {
        const { data: rewData } = await fetchBinary(
          `/pipeline/results/${response.experiment_id}/c3/reward`
        );
        setRewardData(new Float32Array(rewData));
        const reward = new Float32Array(rewData);
        const mean = reward.reduce((a, b) => a + b, 0) / reward.length;
        addLog(`Reward: mean=${mean.toFixed(4)}`);
      } catch {
        addLog('Reward data not available');
      }

      // Load RAM
      try {
        const { data: ramDataBin } = await fetchBinary(
          `/pipeline/results/${response.experiment_id}/c3/ram`
        );
        setRamData(new Float32Array(ramDataBin));
        addLog('RAM: 26 regions loaded');
      } catch {
        addLog('RAM data not available');
      }

      // Refresh experiments list
      const exps = await fetchJSON<any[]>('/experiments/list');
      setExperiments(exps);

      // Load summary
      const summary = await fetchJSON<any>(`/pipeline/results/${response.experiment_id}/summary`);
      addLog(`FPS: ${summary.fps} | Duration: ${summary.duration}s | Reward: ${summary.reward_mean?.toFixed(4)}`);

      setRunPhase('done');
      setRunProgress(1);
    } catch (e: any) {
      setError(e.message || 'Pipeline failed');
      addLog(`ERROR: ${e.message}`);
      setRunPhase('error');
    } finally {
      setRunning(false);
    }
  };

  const phases = [
    { key: 'audio', label: 'Audio', color: 'var(--text-secondary)' },
    { key: 'mel', label: 'Mel', color: 'var(--text-secondary)' },
    { key: 'r3', label: 'R³', color: colors.r3 },
    { key: 'h3', label: 'H³', color: colors.h3 },
    { key: 'c3', label: 'C³', color: colors.c3 },
    { key: 'saving', label: 'Save', color: colors.reward },
    { key: 'done', label: 'Done', color: '#10b981' },
  ];

  return (
    <div className="flex flex-col gap-4 p-4 h-full overflow-y-auto">
      {/* Config panel */}
      <div className="flex gap-4">
        <GlassPanel className="flex-1 p-5">
          <h3 className="text-sm font-medium mb-3">Audio Selection</h3>
          <select
            className="w-full px-3 py-2 rounded-xl text-sm"
            style={{
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              color: 'var(--text-primary)',
            }}
            value={selectedFile}
            onChange={(e) => setSelectedFile(e.target.value)}
          >
            <option value="">Select audio file...</option>
            {audioFiles.map((f) => (
              <option key={f.filename} value={f.filename}>
                {f.name} ({Math.floor(f.duration / 60)}:{String(Math.floor(f.duration % 60)).padStart(2, '0')})
              </option>
            ))}
          </select>

          <div className="flex items-center gap-3 mt-3">
            <label className="flex items-center gap-2 text-sm cursor-pointer">
              <input
                type="checkbox"
                checked={useExcerpt}
                onChange={(e) => setUseExcerpt(e.target.checked)}
                className="rounded"
              />
              <span style={{ color: 'var(--text-secondary)' }}>Excerpt</span>
            </label>
            {useExcerpt && (
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
              />
            )}
            {useExcerpt && (
              <span className="text-xs" style={{ color: 'var(--text-muted)' }}>seconds</span>
            )}
          </div>

          <button
            onClick={runPipeline}
            disabled={!selectedFile || isRunning}
            className="mt-4 w-full py-2.5 rounded-xl text-sm font-medium transition-all"
            style={{
              background: isRunning ? 'rgba(255,255,255,0.04)' : `${colors.c3}20`,
              color: isRunning ? 'var(--text-muted)' : colors.c3,
              border: `1px solid ${isRunning ? 'rgba(255,255,255,0.06)' : colors.c3 + '30'}`,
            }}
          >
            {isRunning ? 'Running...' : 'Run Pipeline'}
          </button>
        </GlassPanel>

        {/* Phase indicator */}
        <GlassPanel className="p-5" style={{ width: 300 }}>
          <h3 className="text-sm font-medium mb-3">Pipeline Phase</h3>
          <div className="flex flex-col gap-2">
            {phases.map((p) => (
              <div key={p.key} className="flex items-center gap-2">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{
                    background: runPhase === p.key ? p.color : 'rgba(255,255,255,0.08)',
                    boxShadow: runPhase === p.key ? `0 0 8px ${p.color}40` : 'none',
                  }}
                />
                <span
                  className="text-xs font-data"
                  style={{ color: runPhase === p.key ? p.color : 'var(--text-muted)' }}
                >
                  {p.label}
                </span>
              </div>
            ))}
          </div>
        </GlassPanel>
      </div>

      {/* Error */}
      {error && (
        <GlassPanel small className="p-3" style={{ borderColor: `${colors.danger}30` }}>
          <span className="text-sm" style={{ color: colors.danger }}>{error}</span>
        </GlassPanel>
      )}

      {/* Console log */}
      <GlassPanel className="flex-1 p-4 overflow-y-auto" style={{ minHeight: 200 }}>
        <h3 className="text-xs font-medium mb-2" style={{ color: 'var(--text-muted)' }}>Console</h3>
        <div className="font-data text-xs space-y-0.5" style={{ color: 'var(--text-secondary)' }}>
          {log.length === 0 ? (
            <span style={{ color: 'var(--text-muted)' }}>Waiting for pipeline run...</span>
          ) : (
            log.map((line, i) => (
              <div key={i} style={{ color: line.includes('ERROR') ? colors.danger : undefined }}>
                {line}
              </div>
            ))
          )}
        </div>
      </GlassPanel>

      {/* Past experiments */}
      <GlassPanel small className="p-4">
        <h3 className="text-xs font-medium mb-2" style={{ color: 'var(--text-muted)' }}>
          Experiments ({usePipelineStore.getState().experiments.length})
        </h3>
        <div className="space-y-1">
          {usePipelineStore.getState().experiments.slice(0, 5).map((exp) => (
            <div key={exp.experiment_id} className="flex items-center justify-between text-xs">
              <span className="font-data" style={{ color: 'var(--text-secondary)' }}>
                {exp.experiment_id}
              </span>
              <span className="font-data" style={{ color: colors.reward }}>
                r={exp.reward_mean?.toFixed(3)}
              </span>
            </div>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}
