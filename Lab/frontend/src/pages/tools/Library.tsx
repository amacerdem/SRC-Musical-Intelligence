import { useEffect, useState } from 'react'
import { PageShell } from '../../components/layout/PageShell'
import { useLibraryStore, type AudioLibraryItem } from '../../stores/libraryStore'
import { usePipelineStore } from '../../stores/pipelineStore'
import { Play, Loader2, Music, TestTube2 } from 'lucide-react'

const RELAY_LABELS: Record<string, string> = {
  bch: 'BCH — Consonance',
  pscl: 'PSCL — Pitch Salience',
  pccr: 'PCCR — Pitch Class',
  sded: 'SDED — Spectral Dynamics',
  csg: 'CSG — Consonance Salience',
  mpg: 'MPG — Melodic Phrase',
  miaa: 'MIAA — Interval Analysis',
  stai: 'STAI — Stability Index',
}

function LibraryCard({
  item,
  onRun,
  running,
}: {
  item: AudioLibraryItem
  onRun: (name: string) => void
  running: boolean
}) {
  return (
    <div className="glass-card px-4 py-3 flex items-center gap-3 group">
      <div className="flex-1 min-w-0">
        <div className="text-sm text-text-primary truncate">
          {item.displayName || item.filename}
        </div>
        {item.description && (
          <div className="text-[11px] text-text-tertiary mt-0.5 line-clamp-1">
            {item.description}
          </div>
        )}
        <div className="flex items-center gap-3 mt-1">
          {item.relay && (
            <span className="text-[10px] mono text-text-tertiary uppercase">
              {item.relay}
            </span>
          )}
          {item.duration_s != null && (
            <span className="text-[10px] mono text-text-tertiary">
              {item.duration_s.toFixed(1)}s
            </span>
          )}
          <span className="text-[10px] mono text-text-tertiary uppercase">
            {item.format}
          </span>
        </div>
      </div>
      <button
        onClick={() => onRun(item.name)}
        disabled={running || !item.available}
        className="shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors
          bg-white/5 hover:bg-white/10 text-text-secondary hover:text-text-primary
          disabled:opacity-30 disabled:cursor-not-allowed"
      >
        {running ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
      </button>
    </div>
  )
}

export function Library() {
  const { items, loading, fetchLibrary, getRelays, getMusicItems, getMidiItems } =
    useLibraryStore()
  const { runPipeline, runningExperiment } = usePipelineStore()
  const [relayFilter, setRelayFilter] = useState<string | null>(null)

  useEffect(() => {
    if (items.length === 0) fetchLibrary()
  }, [items.length, fetchLibrary])

  const relays = getRelays()
  const musicItems = getMusicItems()
  const midiItems = getMidiItems(relayFilter ?? undefined)
  const isRunning = runningExperiment !== null

  const handleRun = (name: string) => {
    if (isRunning) return
    runPipeline(name)
  }

  return (
    <PageShell title="Library" subtitle="Audio sources for pipeline analysis">
      {/* Relay filter bar */}
      <div className="flex items-center gap-2 flex-wrap mt-4">
        <button
          onClick={() => setRelayFilter(null)}
          className={`px-3 py-1 rounded-full text-xs transition-colors ${
            relayFilter === null
              ? 'bg-white/10 text-text-primary'
              : 'bg-white/4 text-text-tertiary hover:text-text-secondary'
          }`}
        >
          All
        </button>
        {relays.map((r) => (
          <button
            key={r}
            onClick={() => setRelayFilter(relayFilter === r ? null : r)}
            className={`px-3 py-1 rounded-full text-xs mono uppercase transition-colors ${
              relayFilter === r
                ? 'bg-white/10 text-text-primary'
                : 'bg-white/4 text-text-tertiary hover:text-text-secondary'
            }`}
          >
            {r}
          </button>
        ))}
      </div>

      {loading && (
        <div className="flex items-center gap-2 mt-6 text-text-tertiary text-sm">
          <Loader2 size={16} className="animate-spin" /> Loading library...
        </div>
      )}

      {/* Music section — only show when no relay filter */}
      {!relayFilter && musicItems.length > 0 && (
        <div className="mt-6">
          <div className="flex items-center gap-2 mb-3">
            <Music size={14} className="text-text-tertiary" />
            <span className="text-xs text-text-tertiary uppercase tracking-wider font-semibold">
              Music ({musicItems.length})
            </span>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-2">
            {musicItems.map((item) => (
              <LibraryCard
                key={item.name}
                item={item}
                onRun={handleRun}
                running={isRunning}
              />
            ))}
          </div>
        </div>
      )}

      {/* MIDI test files */}
      {relayFilter ? (
        <div className="mt-6">
          <div className="flex items-center gap-2 mb-3">
            <TestTube2 size={14} className="text-text-tertiary" />
            <span className="text-xs text-text-tertiary uppercase tracking-wider font-semibold">
              {RELAY_LABELS[relayFilter] ?? relayFilter} ({midiItems.length})
            </span>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-2">
            {midiItems.map((item) => (
              <LibraryCard
                key={item.name}
                item={item}
                onRun={handleRun}
                running={isRunning}
              />
            ))}
          </div>
        </div>
      ) : (
        relays.map((relay) => {
          const relayItems = getMidiItems(relay)
          if (relayItems.length === 0) return null
          return (
            <div key={relay} className="mt-6">
              <div className="flex items-center gap-2 mb-3">
                <TestTube2 size={14} className="text-text-tertiary" />
                <span className="text-xs text-text-tertiary uppercase tracking-wider font-semibold">
                  {RELAY_LABELS[relay] ?? relay} ({relayItems.length})
                </span>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-2">
                {relayItems.map((item) => (
                  <LibraryCard
                    key={item.name}
                    item={item}
                    onRun={handleRun}
                    running={isRunning}
                  />
                ))}
              </div>
            </div>
          )
        })
      )}

      {!loading && items.length === 0 && (
        <div className="glass-card p-8 mt-6 text-center text-text-tertiary text-sm">
          No audio files found. Ensure the backend is running.
        </div>
      )}
    </PageShell>
  )
}
