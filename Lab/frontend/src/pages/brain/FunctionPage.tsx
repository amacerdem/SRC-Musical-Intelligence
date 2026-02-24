import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { PageShell } from '../../components/layout/PageShell'
import { GlassTabs } from '../../components/glass/GlassTabs'
import { FunctionHeader } from '../../components/c3/FunctionHeader'
import { BeliefGrid } from '../../components/c3/BeliefGrid'
import { MechanismCard } from '../../components/c3/MechanismCard'
import { RelayPanel } from '../../components/c3/RelayPanel'
import { AudioTimeline } from '../../components/audio/AudioTimeline'
import { useFunctionData } from '../../hooks/useFunctionData'
import { BELIEFS } from '../../data/beliefs'

export function FunctionPage() {
  const { fId } = useParams<{ fId: string }>()
  const { fn, beliefs, mechanisms, relay } = useFunctionData(fId ?? '')
  const [activeTab, setActiveTab] = useState('beliefs')

  if (!fn) {
    return (
      <PageShell title="Function Not Found">
        <p className="text-text-secondary text-sm mt-4">
          No function found for ID "{fId}". Valid IDs: f1–f9.
        </p>
      </PageShell>
    )
  }

  const tabs = [
    { key: 'beliefs', label: 'Beliefs', count: fn.beliefCounts.total },
    { key: 'mechanisms', label: 'Mechanisms', count: mechanisms.length },
    ...(relay ? [{ key: 'relay', label: 'Relay' }] : []),
  ]

  return (
    <PageShell title="" subtitle="">
      <div className="space-y-6">
        {/* Header */}
        <FunctionHeader fn={fn} mechanismCount={mechanisms.length} />

        {/* Audio timeline strip */}
        <AudioTimeline color={fn.color} />

        {/* Tabs */}
        <GlassTabs
          tabs={tabs}
          active={activeTab}
          onChange={setActiveTab}
          accent={fn.color}
        />

        {/* Tab content */}
        {activeTab === 'beliefs' && (
          <BeliefGrid
            beliefs={beliefs.beliefs}
            data={beliefs.data}
            color={fn.color}
            counts={fn.beliefCounts}
          />
        )}

        {activeTab === 'mechanisms' && (
          <div className="space-y-2">
            {mechanisms.map((m) => (
              <MechanismCard
                key={m.name}
                mechanism={m}
                linkedBeliefs={BELIEFS.filter(
                  (b) => b.mechanism === m.name && b.functionId === fn.id,
                )}
                color={fn.color}
              />
            ))}
            {mechanisms.length === 0 && (
              <div className="glass-card p-6 text-center text-text-tertiary text-sm">
                F{fn.index} is a pure belief layer with zero mechanisms.
                <br />
                Beliefs source from cross-function mechanisms.
              </div>
            )}
          </div>
        )}

        {activeTab === 'relay' && relay && (
          <RelayPanel relay={relay} color={fn.color} />
        )}
      </div>
    </PageShell>
  )
}
