import { useState } from 'react'
import { PageShell } from '../../components/layout/PageShell'
import { AudioTimeline } from '../../components/audio/AudioTimeline'
import { GlassChip } from '../../components/glass/GlassChip'
import { ChevronDown, ChevronRight } from 'lucide-react'

/* ── Morph catalogue ── */
const MORPH_FAMILIES = [
  {
    name: 'Distribution', color: '#3b82f6', morphs: [
      { id: 0, name: 'weighted_mean', signed: false },
      { id: 1, name: 'mean', signed: false },
      { id: 2, name: 'std', signed: false },
      { id: 3, name: 'median', signed: false },
      { id: 4, name: 'max', signed: false },
      { id: 5, name: 'range', signed: false },
      { id: 6, name: 'skewness', signed: true },
      { id: 7, name: 'kurtosis', signed: false },
    ],
  },
  {
    name: 'Dynamics', color: '#f97316', morphs: [
      { id: 8, name: 'velocity', signed: true },
      { id: 9, name: 'velocity_mean', signed: true },
      { id: 10, name: 'velocity_std', signed: false },
      { id: 11, name: 'acceleration', signed: true },
      { id: 12, name: 'acceleration_mean', signed: true },
      { id: 13, name: 'acceleration_std', signed: false },
      { id: 15, name: 'smoothness', signed: false },
      { id: 18, name: 'trend', signed: true },
      { id: 21, name: 'zero_crossings', signed: false },
    ],
  },
  {
    name: 'Rhythm', color: '#22c55e', morphs: [
      { id: 14, name: 'periodicity', signed: false },
      { id: 17, name: 'shape_period', signed: false },
      { id: 22, name: 'peaks', signed: false },
    ],
  },
  {
    name: 'Information', color: '#a855f7', morphs: [
      { id: 20, name: 'entropy', signed: false },
    ],
  },
  {
    name: 'Symmetry', color: '#ec4899', morphs: [
      { id: 16, name: 'curvature', signed: true },
      { id: 19, name: 'stability', signed: false },
      { id: 23, name: 'symmetry', signed: true },
    ],
  },
]

/* ── Horizon bands ── */
const HORIZON_BANDS = [
  { name: 'Micro', range: 'H0\u2013H7', frames: '1\u201316', time: '~6ms\u201393ms', color: '#3b82f6' },
  { name: 'Meso', range: 'H8\u2013H15', frames: '17\u2013256', time: '~100ms\u20131.5s', color: '#22c55e' },
  { name: 'Macro', range: 'H16\u2013H23', frames: '257\u20134096', time: '~1.5s\u201324s', color: '#f59e0b' },
  { name: 'Ultra', range: 'H24\u2013H31', frames: '4097\u201365536', time: '~24s\u2013380s', color: '#ef4444' },
]

/* ── Laws ── */
const LAWS = [
  { id: 0, name: 'L0: Memory', desc: 'Backward/causal window \u2014 only past frames', color: '#3b82f6' },
  { id: 1, name: 'L1: Forward', desc: 'Forward window \u2014 only future frames', color: '#22c55e' },
  { id: 2, name: 'L2: Integration', desc: 'Bidirectional window \u2014 centered on current frame', color: '#f59e0b' },
]

/* ── Demand counts per mechanism ── */
const DEMANDS = [
  { mech: 'BCH', fn: 'F1', type: 'Relay', demands: 48, dim: 16 },
  { mech: 'SRP', fn: 'F5', type: 'Relay', demands: 31, dim: 19 },
  { mech: 'PSCL', fn: 'F1', type: 'Encoder', demands: 20, dim: 16 },
  { mech: 'MEAMN', fn: 'F4', type: 'Relay', demands: 19, dim: 12 },
  { mech: 'CSG', fn: 'F1', type: 'Relay', demands: 18, dim: 12 },
  { mech: 'HTP', fn: 'F2', type: 'Relay', demands: 18, dim: 12 },
  { mech: 'HMCE', fn: 'F7', type: 'Relay', demands: 17, dim: 11 },
  { mech: 'DAED', fn: 'F6', type: 'Relay', demands: 16, dim: 8 },
  { mech: 'MPG', fn: 'F1', type: 'Relay', demands: 16, dim: 10 },
  { mech: 'PEOM', fn: 'F7', type: 'Relay', demands: 15, dim: 11 },
  { mech: 'SNEM', fn: 'F3', type: 'Relay', demands: 14, dim: 12 },
  { mech: 'PCCR', fn: 'F1', type: 'Assoc.', demands: 14, dim: 11 },
  { mech: 'MIAA', fn: 'F1', type: 'Relay', demands: 11, dim: 11 },
  { mech: 'SDED', fn: 'F1', type: 'Relay', demands: 9, dim: 10 },
]

const TOTAL_DEMANDS = DEMANDS.reduce((s, d) => s + d.demands, 0)
const MAX_DEMANDS = Math.max(...DEMANDS.map((d) => d.demands))

type Section = 'morphs' | 'horizons' | 'demands'

export function H3Explorer() {
  const [section, setSection] = useState<Section>('morphs')
  const [expandedFamily, setExpandedFamily] = useState<string | null>(null)

  return (
    <PageShell title="H\u00b3 Morphology" subtitle="Multi-Scale Temporal Morphology Engine \u2014 32 horizons \u00d7 24 morphs \u00d7 3 laws">
      <div className="space-y-5 mt-4">
        {/* Audio sync timeline */}
        <AudioTimeline color="#a78bfa" />

        {/* Summary metrics */}
        <div className="grid grid-cols-5 gap-3">
          {[
            { label: 'Address Space', value: '223,488', sub: '97\u00d732\u00d724\u00d73' },
            { label: 'Active Demands', value: `${TOTAL_DEMANDS}`, sub: `${(TOTAL_DEMANDS / 223488 * 100).toFixed(2)}% occupancy` },
            { label: 'R\u00b3 Features', value: '97', sub: 'input indices' },
            { label: 'Horizons', value: '32', sub: 'H0\u2013H31' },
            { label: 'Morphs \u00d7 Laws', value: '24 \u00d7 3', sub: '72 operators' },
          ].map((m) => (
            <div key={m.label} className="glass-card p-4">
              <div className="text-[10px] text-text-tertiary uppercase tracking-wider">{m.label}</div>
              <div className="text-xl font-semibold mono text-text-primary mt-1">{m.value}</div>
              <div className="text-[10px] text-text-tertiary">{m.sub}</div>
            </div>
          ))}
        </div>

        {/* 4-Tuple format */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">4-Tuple Address Format</div>
          <div className="mono text-sm text-text-secondary">
            <span className="text-blue-400">(r3_idx</span>,{' '}
            <span className="text-green-400">horizon</span>,{' '}
            <span className="text-orange-400">morph</span>,{' '}
            <span className="text-purple-400">law</span>)
          </div>
          <div className="grid grid-cols-4 gap-4 mt-3 text-[10px]">
            <div><span className="text-blue-400 mono">r3_idx</span> <span className="text-text-tertiary">0\u201396 \u2014 which R\u00b3 feature</span></div>
            <div><span className="text-green-400 mono">horizon</span> <span className="text-text-tertiary">0\u201331 \u2014 temporal scale</span></div>
            <div><span className="text-orange-400 mono">morph</span> <span className="text-text-tertiary">0\u201323 \u2014 statistical operator</span></div>
            <div><span className="text-purple-400 mono">law</span> <span className="text-text-tertiary">0\u20132 \u2014 window direction</span></div>
          </div>
        </div>

        {/* Section tabs */}
        <div className="flex gap-1 text-sm">
          {([
            { id: 'morphs', label: 'Morph Catalogue (24)' },
            { id: 'horizons', label: 'Horizons & Laws' },
            { id: 'demands', label: `Demand Table (${TOTAL_DEMANDS})` },
          ] as { id: Section; label: string }[]).map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSection(tab.id)}
              className={`px-4 py-2 rounded-lg text-xs transition-colors ${
                section === tab.id
                  ? 'bg-white/8 text-text-primary'
                  : 'text-text-tertiary hover:text-text-secondary hover:bg-white/3'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Morph Catalogue */}
        {section === 'morphs' && (
          <div className="space-y-3">
            {MORPH_FAMILIES.map((family) => {
              const isExpanded = expandedFamily === family.name
              return (
                <div
                  key={family.name}
                  className={`glass-card cursor-pointer ${isExpanded ? 'ring-1 ring-white/8' : ''}`}
                  onClick={() => setExpandedFamily(isExpanded ? null : family.name)}
                >
                  <div className="flex items-center gap-3 px-5 py-3">
                    <span className="text-text-tertiary shrink-0">
                      {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                    </span>
                    <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: family.color }} />
                    <span className="text-sm font-medium text-text-primary">{family.name}</span>
                    <GlassChip label={`${family.morphs.length}`} color={family.color} />
                    <span className="flex-1" />
                    <span className="mono text-[10px] text-text-tertiary">
                      {family.morphs.map((m) => `M${m.id}`).join(', ')}
                    </span>
                  </div>
                  {isExpanded && (
                    <div className="border-t border-border-subtle px-5 py-3" onClick={(e) => e.stopPropagation()}>
                      <table className="w-full text-xs">
                        <thead>
                          <tr className="border-b border-border-subtle">
                            <th className="text-left py-1.5 text-text-tertiary font-medium w-12">M#</th>
                            <th className="text-left py-1.5 text-text-tertiary font-medium">Name</th>
                            <th className="text-left py-1.5 text-text-tertiary font-medium w-16">Signed</th>
                          </tr>
                        </thead>
                        <tbody>
                          {family.morphs.map((m) => (
                            <tr key={m.id} className="border-b border-border-subtle/50">
                              <td className="py-1 mono text-text-tertiary">M{m.id}</td>
                              <td className="py-1 mono text-text-secondary">{m.name}</td>
                              <td className="py-1">
                                {m.signed
                                  ? <span className="text-orange-400 text-[10px]">\u00b1</span>
                                  : <span className="text-text-tertiary text-[10px]">\u2265 0</span>
                                }
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )
            })}

            {/* M8 vs M18 distinction */}
            <div className="glass-card p-5 border-l-2 border-orange-500/30">
              <div className="text-xs text-text-tertiary uppercase tracking-wider mb-2">Critical Distinction: M8 vs M18</div>
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div>
                  <span className="mono text-orange-400">M8 velocity</span>
                  <p className="text-text-tertiary mt-1">Instantaneous rate: x(t) \u2212 x(t\u22121). Same value at all horizons. "What is the feature doing NOW?"</p>
                </div>
                <div>
                  <span className="mono text-orange-400">M18 trend</span>
                  <p className="text-text-tertiary mt-1">Scale-dependent: regression slope over W frames. Different at each horizon. "What is the overall direction at this scale?"</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Horizons & Laws */}
        {section === 'horizons' && (
          <div className="space-y-4">
            {/* Horizon bands */}
            <div className="glass-card p-5">
              <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">Horizon Bands (32 scales)</div>
              <div className="space-y-2">
                {HORIZON_BANDS.map((band) => (
                  <div key={band.name} className="flex items-center gap-4">
                    <span
                      className="w-16 text-center mono text-xs font-semibold py-1 rounded"
                      style={{ color: band.color, backgroundColor: `${band.color}15` }}
                    >
                      {band.name}
                    </span>
                    <span className="mono text-xs text-text-secondary w-20">{band.range}</span>
                    <span className="mono text-[10px] text-text-tertiary w-24">{band.frames} frames</span>
                    <span className="mono text-[10px] text-text-tertiary">{band.time}</span>
                    <span className="flex-1" />
                    <div className="w-32 h-2 rounded-full bg-white/5 overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: '100%', backgroundColor: band.color, opacity: 0.4 }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Representative horizons */}
            <div className="glass-card p-5">
              <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">Key Horizon Markers</div>
              <div className="flex items-center gap-2 text-[10px] flex-wrap">
                {[
                  { h: 0, t: '~6ms', label: 'sub-frame' },
                  { h: 3, t: '~100ms', label: 'syllable' },
                  { h: 8, t: '~500ms', label: 'beat' },
                  { h: 12, t: '~525ms', label: 'half-bar' },
                  { h: 16, t: '~1s', label: 'bar' },
                  { h: 20, t: '~5s', label: 'phrase' },
                  { h: 24, t: '~36s', label: 'section' },
                  { h: 31, t: '~380s', label: 'piece' },
                ].map((h) => (
                  <div key={h.h} className="glass-card px-3 py-2 text-center">
                    <div className="mono text-text-primary font-semibold">H{h.h}</div>
                    <div className="text-text-secondary">{h.t}</div>
                    <div className="text-text-tertiary">{h.label}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Laws */}
            <div className="glass-card p-5">
              <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">3 Temporal Laws</div>
              <div className="grid grid-cols-3 gap-4">
                {LAWS.map((law) => (
                  <div key={law.id} className="glass-card p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span
                        className="mono text-xs font-semibold px-2 py-0.5 rounded"
                        style={{ color: law.color, backgroundColor: `${law.color}15` }}
                      >
                        L{law.id}
                      </span>
                      <span className="text-sm text-text-primary">{law.name.split(': ')[1]}</span>
                    </div>
                    <div className="text-[10px] text-text-tertiary">{law.desc}</div>
                    {/* Visual arrow */}
                    <div className="mono text-xs text-text-tertiary mt-2 text-center">
                      {law.id === 0 && '\u25c0\u2500\u2500\u2500 t'}
                      {law.id === 1 && 't \u2500\u2500\u2500\u25b6'}
                      {law.id === 2 && '\u25c0\u2500\u2500 t \u2500\u2500\u25b6'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Demand Table */}
        {section === 'demands' && (
          <div className="space-y-4">
            <div className="glass-card overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-border-subtle">
                    <th className="text-left px-4 py-2 text-text-tertiary font-medium">Mechanism</th>
                    <th className="text-center px-4 py-2 text-text-tertiary font-medium w-12">Fn</th>
                    <th className="text-center px-4 py-2 text-text-tertiary font-medium w-16">Type</th>
                    <th className="text-right px-4 py-2 text-text-tertiary font-medium w-20">H\u00b3 Demands</th>
                    <th className="text-right px-4 py-2 text-text-tertiary font-medium w-16">Out Dim</th>
                    <th className="px-4 py-2 text-text-tertiary font-medium">Distribution</th>
                  </tr>
                </thead>
                <tbody>
                  {DEMANDS.map((d) => (
                    <tr key={d.mech} className="border-b border-border-subtle/50 hover:bg-white/2">
                      <td className="px-4 py-2 mono font-semibold text-text-primary">{d.mech}</td>
                      <td className="px-4 py-2 text-center text-text-secondary">{d.fn}</td>
                      <td className="px-4 py-2 text-center">
                        <span className={`text-[10px] ${d.type === 'Relay' ? 'text-orange-400' : d.type === 'Encoder' ? 'text-blue-400' : 'text-purple-400'}`}>
                          {d.type}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-right mono font-semibold text-text-primary">{d.demands}</td>
                      <td className="px-4 py-2 text-right mono text-text-tertiary">{d.dim}D</td>
                      <td className="px-4 py-2">
                        <div className="w-full h-3 rounded-full bg-white/5 overflow-hidden">
                          <div
                            className="h-full rounded-full"
                            style={{
                              width: `${(d.demands / MAX_DEMANDS) * 100}%`,
                              backgroundColor: d.type === 'Relay' ? '#f97316' : d.type === 'Encoder' ? '#3b82f6' : '#a855f7',
                              opacity: 0.6,
                            }}
                          />
                        </div>
                      </td>
                    </tr>
                  ))}
                  <tr className="border-t border-border-subtle bg-white/2">
                    <td className="px-4 py-2 font-semibold text-text-primary">TOTAL</td>
                    <td />
                    <td />
                    <td className="px-4 py-2 text-right mono font-bold text-text-primary">{TOTAL_DEMANDS}</td>
                    <td />
                    <td />
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Demand by type */}
            <div className="grid grid-cols-3 gap-3">
              {[
                { type: 'Relay', color: '#f97316' },
                { type: 'Encoder', color: '#3b82f6' },
                { type: 'Assoc.', color: '#a855f7' },
              ].map((t) => {
                const items = DEMANDS.filter((d) => d.type === t.type)
                const sum = items.reduce((s, d) => s + d.demands, 0)
                return (
                  <div key={t.type} className="glass-card p-4">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-2 h-2 rounded-full" style={{ backgroundColor: t.color }} />
                      <span className="text-xs text-text-primary">{t.type}</span>
                    </div>
                    <div className="text-lg font-semibold mono text-text-primary">{sum}</div>
                    <div className="text-[10px] text-text-tertiary">{items.length} mechanisms</div>
                  </div>
                )
              })}
            </div>

            {/* Occupancy note */}
            <div className="glass-card p-4 opacity-60">
              <div className="text-xs text-text-tertiary">
                <span className="mono text-text-secondary">{TOTAL_DEMANDS}</span> active tuples out of
                <span className="mono text-text-secondary"> 223,488</span> theoretical =
                <span className="mono text-text-secondary"> {(TOTAL_DEMANDS / 223488 * 100).toFixed(2)}%</span> occupancy.
                H\u00b3 is demand-driven: only tuples requested by C\u00b3 mechanisms are computed.
              </div>
            </div>
          </div>
        )}

        {/* Boundary rules */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">
            H\u00b3 Boundary Rules (FROZEN v1.0.0)
          </div>
          <div className="grid grid-cols-5 gap-3">
            {[
              { rule: '1', title: 'Window Locality', desc: 'Single sliding window only' },
              { rule: '2', title: 'Single Feature', desc: 'One R\u00b3 index per computation' },
              { rule: '3', title: 'No Listener Model', desc: 'Signal property, not expectation' },
              { rule: '4', title: 'No Accumulated State', desc: 'No EMA, baselines, counters' },
              { rule: '5', title: 'Deterministic', desc: 'No learned parameters' },
            ].map((r) => (
              <div key={r.rule} className="glass-card p-3">
                <div className="flex items-center gap-2 mb-1">
                  <span className="mono text-[10px] text-text-tertiary">R{r.rule}</span>
                  <span className="text-xs font-medium text-text-primary">{r.title}</span>
                </div>
                <div className="text-[10px] text-text-tertiary">{r.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </PageShell>
  )
}
