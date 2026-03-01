import { PageShell } from '../../components/layout/PageShell'
import { AudioTimeline } from '../../components/audio/AudioTimeline'
import { R3GroupPanel } from '../../components/r3/R3GroupPanel'
import { R3_GROUPS } from '../../data/r3'
import { useR3Store } from '../../stores/r3Store'

export function R3Explorer() {
  const { r3Data, nFrames, r3Loading } = useR3Store()
  const totalDim = R3_GROUPS.reduce((s, g) => s + g.dim, 0)

  return (
    <PageShell title="R³ Features" subtitle="Early Perceptual Front-End — 97D spectral features across 9 groups">
      <div className="space-y-5 mt-4">
        {/* Audio sync timeline */}
        <AudioTimeline color="#60a5fa" />

        {/* Summary metrics */}
        <div className="grid grid-cols-5 gap-3">
          {[
            { label: 'Total Dimensions', value: `${totalDim}D`, sub: '9 groups' },
            { label: 'Stage 1 (Independent)', value: '7', sub: '71D' },
            { label: 'Stage 2 (Dependent)', value: '2', sub: '22D (G, H)' },
            { label: 'Frame Rate', value: '172.27 Hz', sub: '~5.8ms/frame' },
            {
              label: 'Loaded Frames',
              value: r3Loading ? '...' : nFrames > 0 ? nFrames.toLocaleString() : '\u2014',
              sub: r3Loading ? 'loading' : nFrames > 0 ? `${(nFrames / 172.27).toFixed(1)}s` : 'no experiment',
            },
          ].map((m) => (
            <div key={m.label} className="glass-card p-4">
              <div className="text-[10px] text-text-tertiary uppercase tracking-wider">{m.label}</div>
              <div className="text-xl font-semibold mono text-text-primary mt-1">{m.value}</div>
              <div className="text-[10px] text-text-tertiary">{m.sub}</div>
            </div>
          ))}
        </div>

        {/* Pipeline diagram */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">2-Stage DAG</div>
          <div className="flex items-center gap-3 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: '#22c55e' }} />
              <span className="text-text-secondary">Stage 1 (7 groups, independent)</span>
            </div>
            <span className="text-text-tertiary">{'\u2192'}</span>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: '#f59e0b' }} />
              <span className="text-text-secondary">Stage 2 (G{'\u2190'}energy, H{'\u2190'}pitch_chroma)</span>
            </div>
            <span className="text-text-tertiary">{'\u2192'}</span>
            <span className="text-text-secondary">H³ / C³</span>
          </div>
        </div>

        {/* Dimension bar */}
        <div className="glass-card p-4">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-2">Dimension Distribution</div>
          <div className="flex h-6 rounded-md overflow-hidden bg-white/3">
            {R3_GROUPS.map((g) => (
              <div
                key={g.id}
                className="flex items-center justify-center text-[9px] font-semibold mono text-white/90 transition-opacity"
                style={{
                  width: `${(g.dim / totalDim) * 100}%`,
                  backgroundColor: g.color,
                  opacity: 0.7,
                }}
                title={`${g.id}: ${g.name} [${g.dim}D]`}
              >
                {g.dim >= 5 && `${g.id}[${g.dim}]`}
              </div>
            ))}
          </div>
          <div className="flex flex-wrap gap-3 mt-2">
            {R3_GROUPS.map((g) => (
              <span key={g.id} className="flex items-center gap-1.5 text-[10px]">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: g.color }} />
                <span className="text-text-secondary">{g.id}: {g.name}</span>
                <span className="mono text-text-tertiary">{g.dim}D</span>
              </span>
            ))}
          </div>
        </div>

        {/* Group panels with dimension cards */}
        {R3_GROUPS.map((group) => (
          <R3GroupPanel
            key={group.id}
            group={group}
            data={r3Data}
          />
        ))}

        {/* Boundary spec */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">
            R³ Boundary Rules (FROZEN v1.0.0)
          </div>
          <div className="grid grid-cols-5 gap-3">
            {[
              { rule: '1', title: 'Frame Locality', desc: '\u00b12 frames (~11.6ms)' },
              { rule: '2', title: 'No Listener Model', desc: 'Signal only, no expectations' },
              { rule: '3', title: 'No Cross-Domain', desc: 'Single perceptual domain' },
              { rule: '4', title: 'No Prediction', desc: 'No future states/surprisal' },
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

        {/* Dissolved groups note */}
        <div className="glass-card p-5 opacity-60">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-2">Dissolved Groups</div>
          <div className="grid grid-cols-2 gap-4 text-xs text-text-tertiary">
            <div>
              <span className="text-text-secondary">Group E (Interactions, 24D)</span>
              <span className="mx-2">{'\u2192'}</span>
              C³ input layer (cross-domain products computed per model)
            </div>
            <div>
              <span className="text-text-secondary">Group I (Information, 7D)</span>
              <span className="mx-2">{'\u2192'}</span>
              4D {'\u2192'} C³, 1D {'\u2192'} H³, 2D removed (redundant)
            </div>
          </div>
        </div>
      </div>
    </PageShell>
  )
}
