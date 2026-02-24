import { useParams } from 'react-router-dom'
import { PageShell } from '../../components/layout/PageShell'
import { FUNCTIONS } from '../../data/functions'

export function FunctionPage() {
  const { fId } = useParams<{ fId: string }>()
  const fn = FUNCTIONS.find((f) => f.id === fId)

  if (!fn) {
    return (
      <PageShell title="Function Not Found">
        <p className="text-text-secondary text-sm mt-4">
          No function found for ID "{fId}". Valid IDs: f1\u2013f9.
        </p>
      </PageShell>
    )
  }

  const { beliefCounts: bc } = fn

  return (
    <PageShell
      title={`F${fn.index} ${fn.name}`}
      subtitle={fn.description}
      accent={fn.color}
    >
      {/* Belief count badges */}
      <div className="flex gap-2 mt-2 mb-6">
        <span className="glass-badge badge-core">{bc.core} Core</span>
        <span className="glass-badge badge-appraisal">{bc.appraisal} Appraisal</span>
        <span className="glass-badge badge-anticipation">{bc.anticipation} Anticipation</span>
        <span className="glass-chip">{fn.mechanismCount} mechanisms</span>
        {fn.relay && <span className="glass-chip">{fn.relay}</span>}
      </div>

      {/* Tab placeholder */}
      <div className="glass-tabs mb-6">
        <div className="glass-tab active">Beliefs ({bc.total})</div>
        <div className="glass-tab">Mechanisms ({fn.mechanismCount})</div>
        {fn.relay && <div className="glass-tab">Relay</div>}
      </div>

      {/* Content placeholder */}
      <div className="glass-card p-6" style={{ borderColor: `${fn.color}22` }}>
        <p className="text-sm text-text-secondary">
          Function page content for F{fn.index} {fn.name} ({fn.unit}).
          This will show {bc.total} beliefs, {fn.mechanismCount} mechanisms,
          and {fn.relay ?? 'no'} relay data.
        </p>
        <p className="text-xs text-text-tertiary mt-2 mono">
          Depth range: {fn.depthRange[0]}\u2013{fn.depthRange[1]}
        </p>
      </div>
    </PageShell>
  )
}
