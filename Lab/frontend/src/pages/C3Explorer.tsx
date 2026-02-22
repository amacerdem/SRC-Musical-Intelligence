import { useState, useEffect, useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import HeatmapChart from '../components/charts/HeatmapChart';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { fetchBinary } from '../api/client';
import { colors, FRAME_RATE } from '../design/tokens';

const TABS = ['Beliefs', 'Relays', 'RAM', 'Neuro', 'Reward'];

const RELAY_INFO = [
  { name: 'BCH', unit: 'SPU', dim: 16, color: '#60a5fa' },
  { name: 'HMCE', unit: 'STU', dim: 18, color: '#a78bfa' },
  { name: 'SNEM', unit: 'ASU', dim: 12, color: '#f97316' },
  { name: 'MEAMN', unit: 'IMU', dim: 12, color: '#14b8a6' },
  { name: 'DAED', unit: 'RPU', dim: 8, color: '#eab308' },
  { name: 'MPG', unit: 'NDU', dim: 10, color: '#22c55e' },
  { name: 'SRP', unit: 'ARU', dim: 5, color: '#ef4444' },
  { name: 'PEOM', unit: 'MPU', dim: 3, color: '#ec4899' },
  { name: 'HTP', unit: 'PCU', dim: 9, color: '#6366f1' },
];

const RAM_REGIONS = [
  'A1_HG','STG','STS','IFG','AG','TP','dlPFC','vmPFC','OFC','Insula','ACC','SMA',
  'MGB','Caudate','Putamen','NAcc','Hippocampus','Amygdala','VTA','PAG','IC',
  'AN','CN','SOC','IC_bs','PAG_bs',
];

const NEURO_CHANNELS = [
  { name: 'Dopamine', short: 'DA', color: '#f59e0b' },
  { name: 'Norepinephrine', short: 'NE', color: '#ef4444' },
  { name: 'Opioid', short: 'OPI', color: '#a78bfa' },
  { name: 'Serotonin', short: '5HT', color: '#10b981' },
];

export default function C3Explorer() {
  const [activeTab, setActiveTab] = useState(0);
  const { currentExperimentId, r3Frames, rewardData, ramData } = usePipelineStore();
  const { currentFrame } = useAudioStore();

  // Relay data cache
  const [relayCache, setRelayCache] = useState<Record<string, { data: Float32Array; dim: number }>>({});
  // Beliefs data
  const [beliefsData, setBeliefsData] = useState<{ observed: Float32Array; names: string[]; nBeliefs: number } | null>(null);
  // Neuro data
  const [neuroData, setNeuroData] = useState<Float32Array | null>(null);

  // Load data when experiment changes
  useEffect(() => {
    if (!currentExperimentId) return;

    // Load beliefs
    fetchBinary(`/pipeline/results/${currentExperimentId}/c3/beliefs`)
      .then(({ data, headers }) => {
        const nFrames = parseInt(headers.get('X-N-Frames') || '0');
        const nBeliefs = parseInt(headers.get('X-N-Beliefs') || '0');
        const names = (headers.get('X-Belief-Names') || '').split(',');
        setBeliefsData({ observed: new Float32Array(data), names, nBeliefs });
      })
      .catch(() => setBeliefsData(null));

    // Load relays
    for (const relay of RELAY_INFO) {
      fetchBinary(`/pipeline/results/${currentExperimentId}/c3/relays/${relay.name.toLowerCase()}`)
        .then(({ data, headers }) => {
          const dim = parseInt(headers.get('X-N-Dims') || String(relay.dim));
          setRelayCache((prev) => ({ ...prev, [relay.name]: { data: new Float32Array(data), dim } }));
        })
        .catch(() => {});
    }

    // Load neuro
    fetchBinary(`/pipeline/results/${currentExperimentId}/c3/neuro`)
      .then(({ data }) => setNeuroData(new Float32Array(data)))
      .catch(() => setNeuroData(null));
  }, [currentExperimentId]);

  const hasData = currentExperimentId !== null;

  if (!hasData) {
    return (
      <div className="flex flex-col gap-4 p-4 h-full">
        <GlassPanel className="p-6 flex-1 flex items-center justify-center" glow="c3">
          <div className="text-center">
            <h2 className="text-lg font-semibold mb-2" style={{ color: colors.c3 }}>C³ Explorer</h2>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              Run a pipeline first to explore C³ cognitive outputs.
            </p>
            <p className="text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
              131 beliefs · 9 relays · 26 brain regions · 4 neuro channels
            </p>
          </div>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      {/* Audio */}
      <GlassPanel small className="p-3">
        <Waveform height={30} />
      </GlassPanel>

      {/* Tabs */}
      <div className="flex gap-1.5">
        {TABS.map((tab, i) => (
          <button
            key={tab}
            onClick={() => setActiveTab(i)}
            className="px-4 py-2 rounded-xl text-sm transition-colors"
            style={{
              background: activeTab === i ? `${colors.c3}15` : 'rgba(255,255,255,0.03)',
              color: activeTab === i ? colors.c3 : 'var(--text-muted)',
              border: `1px solid ${activeTab === i ? colors.c3 + '25' : 'rgba(255,255,255,0.05)'}`,
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === 0 && beliefsData && (
        <BeliefsTab data={beliefsData} nFrames={r3Frames} />
      )}

      {activeTab === 1 && (
        <RelaysTab relayCache={relayCache} nFrames={r3Frames} />
      )}

      {activeTab === 2 && ramData && (
        <RamTab data={ramData} nFrames={r3Frames} currentFrame={currentFrame} />
      )}

      {activeTab === 3 && neuroData && (
        <NeuroTab data={neuroData} nFrames={r3Frames} currentFrame={currentFrame} />
      )}

      {activeTab === 4 && rewardData && (
        <RewardTab data={rewardData} nFrames={r3Frames} currentFrame={currentFrame} />
      )}
    </div>
  );
}

// ── Beliefs Tab ──
function BeliefsTab({ data, nFrames }: { data: { observed: Float32Array; names: string[]; nBeliefs: number }; nFrames: number }) {
  const [expandedBelief, setExpandedBelief] = useState<number | null>(null);
  const { currentFrame } = useAudioStore();

  return (
    <div className="flex flex-col gap-2">
      <div className="text-xs px-1" style={{ color: 'var(--text-muted)' }}>
        {data.nBeliefs} beliefs · {nFrames} frames
      </div>
      {data.names.map((name, i) => {
        const isExpanded = expandedBelief === i;
        const curVal = currentFrame < nFrames ? data.observed[currentFrame * data.nBeliefs + i] : 0;
        return (
          <GlassPanel
            key={i}
            small
            className="p-3 cursor-pointer"
            onClick={() => setExpandedBelief(isExpanded ? null : i)}
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs" style={{ color: colors.c3 }}>
                [{i}] {name}
              </span>
              <span className="font-data text-xs">{curVal.toFixed(4)}</span>
            </div>
            <SignalTrace
              data={data.observed}
              nFeatures={data.nBeliefs}
              nFrames={nFrames}
              signals={[{ name, color: colors.c3, featureIndex: i }]}
              height={isExpanded ? 80 : 35}
            />
          </GlassPanel>
        );
      })}
    </div>
  );
}

// ── Relays Tab ──
function RelaysTab({ relayCache, nFrames }: { relayCache: Record<string, { data: Float32Array; dim: number }>; nFrames: number }) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
      {RELAY_INFO.map((relay) => {
        const cached = relayCache[relay.name];
        if (!cached) return (
          <GlassPanel key={relay.name} small className="p-3">
            <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{relay.name} — loading...</span>
          </GlassPanel>
        );

        const signals = Array.from({ length: cached.dim }, (_, j) => ({
          name: `${relay.name}[${j}]`,
          color: relay.color,
          featureIndex: j,
        }));

        return (
          <GlassPanel key={relay.name} small className="p-3">
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2 h-2 rounded-sm" style={{ background: relay.color }} />
              <span className="text-xs font-medium">{relay.name}</span>
              <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
                {relay.unit} · {cached.dim}D
              </span>
            </div>
            <SignalTrace
              data={cached.data}
              nFeatures={cached.dim}
              nFrames={nFrames}
              signals={signals}
              height={60}
            />
          </GlassPanel>
        );
      })}
    </div>
  );
}

// ── RAM Tab ──
function RamTab({ data, nFrames, currentFrame }: { data: Float32Array; nFrames: number; currentFrame: number }) {
  // RAM heatmap (26 × T)
  const nRegions = 26;

  // Current values
  const curValues = useMemo(() => {
    if (currentFrame >= nFrames) return null;
    const vals: number[] = [];
    for (let r = 0; r < nRegions; r++) {
      vals.push(data[currentFrame * nRegions + r]);
    }
    return vals;
  }, [data, currentFrame, nFrames]);

  return (
    <div className="flex flex-col gap-3">
      {/* Heatmap */}
      <GlassPanel className="p-3">
        <div className="text-sm font-medium mb-2" style={{ color: colors.c3 }}>
          Region Activation Map — 26 Regions × Time
        </div>
        <HeatmapChart
          data={data}
          nRows={nRegions}
          nCols={nFrames}
          height={300}
          rowLabels={RAM_REGIONS}
          colormap="magma"
          valueRange={[0, 1]}
        />
      </GlassPanel>

      {/* Current values */}
      {curValues && (
        <GlassPanel small className="p-3">
          <div className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>Activation at Frame {currentFrame}</div>
          <div className="grid grid-cols-4 gap-x-4 gap-y-1">
            {RAM_REGIONS.map((region, i) => (
              <div key={region} className="flex items-center justify-between">
                <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>{region}</span>
                <div className="flex items-center gap-1.5">
                  <div
                    className="w-12 h-1.5 rounded-full overflow-hidden"
                    style={{ background: 'rgba(255,255,255,0.06)' }}
                  >
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${(curValues[i] || 0) * 100}%`,
                        background: colors.c3,
                      }}
                    />
                  </div>
                  <span className="font-data text-xs w-10 text-right">{(curValues[i] || 0).toFixed(3)}</span>
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      )}
    </div>
  );
}

// ── Neuro Tab ──
function NeuroTab({ data, nFrames, currentFrame }: { data: Float32Array; nFrames: number; currentFrame: number }) {
  return (
    <div className="flex flex-col gap-3">
      {NEURO_CHANNELS.map((ch, i) => {
        const curVal = currentFrame < nFrames ? data[currentFrame * 4 + i] : 0;
        return (
          <GlassPanel key={ch.short} small className="p-3">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ background: ch.color }} />
                <span className="text-xs font-medium">{ch.name}</span>
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{ch.short}</span>
              </div>
              <span className="font-data text-xs">{curVal.toFixed(4)}</span>
            </div>
            <SignalTrace
              data={data}
              nFeatures={4}
              nFrames={nFrames}
              signals={[{ name: ch.short, color: ch.color, featureIndex: i }]}
              height={50}
            />
          </GlassPanel>
        );
      })}
    </div>
  );
}

// ── Reward Tab ──
function RewardTab({ data, nFrames, currentFrame }: { data: Float32Array; nFrames: number; currentFrame: number }) {
  const curVal = currentFrame < nFrames ? data[currentFrame] : 0;
  const mean = data.reduce((a, b) => a + b, 0) / data.length;
  const posPct = data.filter((v) => v > 0).length / data.length * 100;

  // Create a wrapper to make it work with SignalTrace (1 feature)
  return (
    <div className="flex flex-col gap-3">
      <GlassPanel className="p-4" glow="reward">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-medium" style={{ color: colors.reward }}>Reward Signal</span>
          <span className="font-data text-sm" style={{ color: curVal > 0 ? colors.c3 : colors.danger }}>
            {curVal > 0 ? '+' : ''}{curVal.toFixed(4)}
          </span>
        </div>
        <SignalTrace
          data={data}
          nFeatures={1}
          nFrames={nFrames}
          signals={[{ name: 'reward', color: colors.reward, featureIndex: 0 }]}
          height={120}
          yRange={[-0.2, 0.5]}
        />
      </GlassPanel>

      {/* Stats */}
      <div className="flex gap-3">
        <GlassPanel small className="flex-1 p-3">
          <div className="text-xs" style={{ color: 'var(--text-muted)' }}>Mean</div>
          <div className="font-data text-lg" style={{ color: mean > 0 ? colors.c3 : colors.danger }}>
            {mean > 0 ? '+' : ''}{mean.toFixed(4)}
          </div>
        </GlassPanel>
        <GlassPanel small className="flex-1 p-3">
          <div className="text-xs" style={{ color: 'var(--text-muted)' }}>Positive %</div>
          <div className="font-data text-lg" style={{ color: colors.reward }}>
            {posPct.toFixed(1)}%
          </div>
        </GlassPanel>
        <GlassPanel small className="flex-1 p-3">
          <div className="text-xs" style={{ color: 'var(--text-muted)' }}>Frames</div>
          <div className="font-data text-lg" style={{ color: 'var(--text-primary)' }}>
            {nFrames}
          </div>
        </GlassPanel>
      </div>
    </div>
  );
}
