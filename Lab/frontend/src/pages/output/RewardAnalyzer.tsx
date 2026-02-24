import { PageShell } from '../../components/layout/PageShell'
import { AudioTimeline } from '../../components/audio/AudioTimeline'
import { RELAYS } from '../../data/relays'

const SRP = RELAYS.find((r) => r.name === 'SRP')!

const REWARD_FORMULA = [
  { name: 'surprise', weight: 1.5, color: '#f97316', desc: 'PE magnitude from precision engine' },
  { name: 'resolution', weight: 0.8, color: '#22c55e', desc: 'dissonance \u2192 consonance trend' },
  { name: 'exploration', weight: 0.5, color: '#3b82f6', desc: 'entropy/uncertainty novelty bonus' },
  { name: 'monotony', weight: -0.6, color: '#ef4444', desc: 'lack of change penalty' },
]

const NEURO_CHANNELS = [
  { name: 'DA', label: 'Dopamine', color: '#f59e0b', baseline: 0.5 },
  { name: 'NE', label: 'Norepinephrine', color: '#ef4444', baseline: 0.5 },
  { name: 'OPI', label: 'Opioid', color: '#a855f7', baseline: 0.5 },
  { name: '5HT', label: 'Serotonin', color: '#06b6d4', baseline: 0.5 },
]

export function RewardAnalyzer() {
  return (
    <PageShell title="Reward Analyzer" subtitle="SRP reward decomposition \u2014 wanting, liking, pleasure, tension-resolution dynamics">
      <div className="space-y-6 mt-4">
        {/* Audio sync timeline */}
        <AudioTimeline color="#f59e0b" />

        {/* P-Layer reward signals */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">P-Layer: Primary Reward Signals</div>
          <div className="grid grid-cols-3 gap-4">
            {['wanting', 'liking', 'pleasure'].map((signal, i) => (
              <div key={signal} className="glass-card p-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: ['#f59e0b', '#ec4899', '#a855f7'][i] }} />
                  <span className="text-sm font-medium text-text-primary capitalize">{signal}</span>
                  <span className="mono text-[10px] text-text-tertiary">P{i}</span>
                </div>
                <div className="text-xl font-semibold mono text-text-tertiary">\u2014</div>
                <div className="text-[10px] text-text-tertiary mt-1">awaiting experiment data</div>
              </div>
            ))}
          </div>
        </div>

        {/* Global Reward Formula */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">Global Reward Formula (v4.0)</div>
          <div className="mono text-sm text-text-secondary mb-4">
            R = \u03a3 salience \u00d7 ({REWARD_FORMULA.map((c, i) => (
              <span key={c.name}>
                {i > 0 && ' + '}
                <span style={{ color: c.color }}>{c.weight}\u00d7{c.name}</span>
              </span>
            ))}) \u00d7 fam_mod \u00d7 da_gain
          </div>
          <div className="grid grid-cols-2 gap-3">
            {REWARD_FORMULA.map((comp) => (
              <div key={comp.name} className="flex items-center gap-3">
                <span
                  className="w-8 h-5 rounded flex items-center justify-center mono text-[10px] font-bold"
                  style={{ backgroundColor: `${comp.color}20`, color: comp.color }}
                >
                  {comp.weight > 0 ? '+' : ''}{comp.weight}
                </span>
                <div>
                  <span className="text-xs text-text-primary">{comp.name}</span>
                  <span className="text-[10px] text-text-tertiary ml-2">{comp.desc}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Neurochemical channels */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">Neurochemical Channels (4D)</div>
          <div className="grid grid-cols-4 gap-3">
            {NEURO_CHANNELS.map((ch) => (
              <div key={ch.name} className="glass-card p-3">
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: ch.color }} />
                  <span className="mono text-xs font-semibold" style={{ color: ch.color }}>{ch.name}</span>
                </div>
                <div className="text-[10px] text-text-secondary">{ch.label}</div>
                <div className="mono text-[10px] text-text-tertiary mt-1">baseline: {ch.baseline}</div>
              </div>
            ))}
          </div>
        </div>

        {/* SRP dimension table */}
        <div className="glass-card p-5">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-xs text-text-tertiary uppercase tracking-wider">SRP Relay Dimensions</span>
            <span className="glass-chip">{SRP.outputDim}D</span>
          </div>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1">
            {SRP.dims.map((dim, i) => (
              <div key={i} className="flex items-center gap-2 py-0.5">
                <span className="mono text-[10px] text-text-tertiary w-5 text-right">{i}</span>
                <span className="mono text-xs text-text-secondary">{dim.name}</span>
                <span className="text-[9px] text-text-tertiary ml-auto">{dim.layer}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </PageShell>
  )
}
