import { useEffect, useState } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import { usePipelineStore } from '../stores/pipelineStore';
import { fetchJSON } from '../api/client';
import { colors } from '../design/tokens';

export default function ExperimentCompare() {
  const { experiments, setExperiments } = usePipelineStore();
  const [expA, setExpA] = useState<string>('');
  const [expB, setExpB] = useState<string>('');

  useEffect(() => {
    fetchJSON<any[]>('/experiments/list').then(setExperiments).catch(() => {});
  }, [setExperiments]);

  const metaA = experiments.find((e) => e.experiment_id === expA);
  const metaB = experiments.find((e) => e.experiment_id === expB);

  const metrics = ['reward_mean', 'reward_positive_pct', 'fps', 'duration', 'n_frames'];

  return (
    <div className="flex flex-col gap-4 p-4 h-full overflow-y-auto">
      {/* Selectors */}
      <div className="flex gap-4">
        <GlassPanel small className="flex-1 p-4">
          <label className="text-xs mb-2 block" style={{ color: 'var(--text-muted)' }}>Experiment A</label>
          <select
            className="w-full px-3 py-2 rounded-xl text-sm"
            style={{
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              color: 'var(--text-primary)',
            }}
            value={expA}
            onChange={(e) => setExpA(e.target.value)}
          >
            <option value="">Select...</option>
            {experiments.map((exp) => (
              <option key={exp.experiment_id} value={exp.experiment_id}>
                {exp.experiment_id} — {exp.audio_name}
              </option>
            ))}
          </select>
        </GlassPanel>

        <GlassPanel small className="flex-1 p-4">
          <label className="text-xs mb-2 block" style={{ color: 'var(--text-muted)' }}>Experiment B</label>
          <select
            className="w-full px-3 py-2 rounded-xl text-sm"
            style={{
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              color: 'var(--text-primary)',
            }}
            value={expB}
            onChange={(e) => setExpB(e.target.value)}
          >
            <option value="">Select...</option>
            {experiments.map((exp) => (
              <option key={exp.experiment_id} value={exp.experiment_id}>
                {exp.experiment_id} — {exp.audio_name}
              </option>
            ))}
          </select>
        </GlassPanel>
      </div>

      {/* Comparison table */}
      {metaA && metaB && (
        <GlassPanel className="p-4">
          <h3 className="text-sm font-medium mb-3">Comparison</h3>
          <table className="w-full text-sm">
            <thead>
              <tr style={{ color: 'var(--text-muted)' }}>
                <th className="text-left py-1 text-xs font-normal">Metric</th>
                <th className="text-right py-1 text-xs font-normal">A</th>
                <th className="text-right py-1 text-xs font-normal">B</th>
                <th className="text-right py-1 text-xs font-normal">Delta</th>
              </tr>
            </thead>
            <tbody>
              {metrics.map((metric) => {
                const valA = metaA[metric] ?? 0;
                const valB = metaB[metric] ?? 0;
                const delta = valB - valA;
                return (
                  <tr key={metric} style={{ borderTop: '1px solid rgba(255,255,255,0.04)' }}>
                    <td className="py-1.5 text-xs" style={{ color: 'var(--text-secondary)' }}>{metric}</td>
                    <td className="py-1.5 text-right font-data text-xs">{typeof valA === 'number' ? valA.toFixed(4) : valA}</td>
                    <td className="py-1.5 text-right font-data text-xs">{typeof valB === 'number' ? valB.toFixed(4) : valB}</td>
                    <td
                      className="py-1.5 text-right font-data text-xs"
                      style={{ color: delta > 0 ? colors.c3 : delta < 0 ? colors.danger : 'var(--text-muted)' }}
                    >
                      {delta > 0 ? '+' : ''}{typeof delta === 'number' ? delta.toFixed(4) : delta}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </GlassPanel>
      )}

      {/* Experiment list */}
      <GlassPanel className="p-4">
        <h3 className="text-sm font-medium mb-3">All Experiments ({experiments.length})</h3>
        {experiments.length === 0 ? (
          <p className="text-sm" style={{ color: 'var(--text-muted)' }}>No experiments yet. Run a pipeline first.</p>
        ) : (
          <div className="space-y-1.5">
            {experiments.map((exp) => (
              <div
                key={exp.experiment_id}
                className="flex items-center justify-between py-1.5 px-2 rounded-lg"
                style={{
                  background: (exp.experiment_id === expA || exp.experiment_id === expB)
                    ? 'rgba(255,255,255,0.04)' : 'transparent',
                }}
              >
                <div className="flex items-center gap-3">
                  <span className="font-data text-xs" style={{ color: 'var(--text-secondary)' }}>
                    {exp.experiment_id}
                  </span>
                  <span className="text-xs truncate" style={{ color: 'var(--text-muted)', maxWidth: 200 }}>
                    {exp.audio_name}
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="font-data text-xs" style={{ color: colors.reward }}>
                    r={exp.reward_mean?.toFixed(3)}
                  </span>
                  <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
                    {exp.fps}fps
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </GlassPanel>
    </div>
  );
}
