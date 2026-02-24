import { PageShell } from '../components/layout/PageShell'
import { FUNCTIONS } from '../data/functions'

export function Overview() {
  return (
    <PageShell title="Overview" subtitle="MI Pipeline Experiment Dashboard">
      <div className="grid grid-cols-3 gap-4 mt-4">
        {/* Summary cards */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-1">R\u00b3 Features</div>
          <div className="text-2xl font-semibold mono">97D</div>
          <div className="text-xs text-text-secondary mt-1">9 groups &middot; FROZEN v1.0.0</div>
        </div>
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-1">H\u00b3 Morphology</div>
          <div className="text-2xl font-semibold mono">223,488</div>
          <div className="text-xs text-text-secondary mt-1">theoretical tuples &middot; 32 horizons</div>
        </div>
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-1">C\u00b3 Beliefs</div>
          <div className="text-2xl font-semibold mono">131</div>
          <div className="text-xs text-text-secondary mt-1">36 Core + 65 Appraisal + 30 Anticipation</div>
        </div>
      </div>

      {/* Function grid */}
      <h2 className="text-sm font-semibold text-text-secondary mt-8 mb-3">C\u00b3 Functions</h2>
      <div className="grid grid-cols-3 gap-3">
        {FUNCTIONS.map((fn) => (
          <a
            key={fn.id}
            href={`/brain/${fn.id}`}
            className="glass-card p-4 no-underline block"
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: fn.color }} />
              <span className="text-sm font-medium text-text-primary">
                F{fn.index} {fn.name}
              </span>
            </div>
            <div className="flex gap-2 mt-2">
              <span className="glass-badge badge-core">{fn.beliefCounts.core}C</span>
              <span className="glass-badge badge-appraisal">{fn.beliefCounts.appraisal}A</span>
              <span className="glass-badge badge-anticipation">{fn.beliefCounts.anticipation}N</span>
            </div>
            <div className="text-xs text-text-tertiary mt-2 mono">
              {fn.mechanismCount} mechanisms &middot; {fn.unit}
            </div>
          </a>
        ))}
      </div>
    </PageShell>
  )
}
