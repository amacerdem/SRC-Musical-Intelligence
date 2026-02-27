import { useState, useRef, useEffect } from 'react'
import { ChevronDown, Play, Loader2 } from 'lucide-react'
import { useLibraryStore, type AudioLibraryItem } from '../../stores/libraryStore'
import { usePipelineStore } from '../../stores/pipelineStore'

interface AudioPickerProps {
  beliefName?: string
  currentAudioName?: string
}

export function AudioPicker({ beliefName, currentAudioName }: AudioPickerProps) {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)
  const {
    items,
    fetchLibrary,
    getRecommendedForBelief,
    getMusicItems,
    getRelays,
    getMidiItems,
  } = useLibraryStore()
  const { runPipeline, runningExperiment } = usePipelineStore()
  const isRunning = runningExperiment !== null

  useEffect(() => {
    if (items.length === 0) fetchLibrary()
  }, [items.length, fetchLibrary])

  // Close on outside click
  useEffect(() => {
    if (!open) return
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [open])

  const handleSelect = (name: string) => {
    setOpen(false)
    if (name === currentAudioName || isRunning) return
    runPipeline(name)
  }

  const recommended = beliefName ? getRecommendedForBelief(beliefName) : []
  const musicItems = getMusicItems()
  const relays = getRelays()

  const displayName = currentAudioName
    ? items.find((i) => i.name === currentAudioName)?.displayName ?? currentAudioName
    : 'Select audio'

  return (
    <div ref={ref} className="relative" onClick={(e) => e.stopPropagation()}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 px-2 py-1 rounded-md text-[11px] mono
          bg-white/5 hover:bg-white/8 text-text-secondary transition-colors"
      >
        {isRunning && <Loader2 size={10} className="animate-spin" />}
        <span className="truncate max-w-[160px]">{displayName}</span>
        <ChevronDown size={10} />
      </button>

      {open && (
        <div
          className="absolute right-0 top-full mt-1 z-50 w-72 max-h-80 overflow-y-auto
            rounded-lg border border-border-subtle bg-bg-elevated shadow-xl"
        >
          {/* Recommended section */}
          {recommended.length > 0 && (
            <Section
              title="Recommended"
              items={recommended}
              onSelect={handleSelect}
              currentName={currentAudioName}
              running={isRunning}
            />
          )}

          {/* MIDI by relay */}
          {relays.map((relay) => {
            const relayItems = getMidiItems(relay)
            if (relayItems.length === 0) return null
            return (
              <Section
                key={relay}
                title={relay.toUpperCase()}
                items={relayItems}
                onSelect={handleSelect}
                currentName={currentAudioName}
                running={isRunning}
              />
            )
          })}

          {/* Music */}
          {musicItems.length > 0 && (
            <Section
              title="Music"
              items={musicItems}
              onSelect={handleSelect}
              currentName={currentAudioName}
              running={isRunning}
            />
          )}
        </div>
      )}
    </div>
  )
}

function Section({
  title,
  items,
  onSelect,
  currentName,
  running,
}: {
  title: string
  items: AudioLibraryItem[]
  onSelect: (name: string) => void
  currentName?: string
  running: boolean
}) {
  return (
    <div className="border-b border-border-subtle last:border-b-0">
      <div className="px-3 py-1.5 text-[9px] mono uppercase tracking-wider text-text-tertiary bg-white/[0.02]">
        {title} ({items.length})
      </div>
      {items.map((item) => {
        const isActive = item.name === currentName
        return (
          <button
            key={item.name}
            onClick={() => onSelect(item.name)}
            disabled={running}
            className={`w-full text-left px-3 py-1.5 text-[11px] flex items-center gap-2 transition-colors
              ${isActive ? 'bg-white/8 text-text-primary' : 'text-text-secondary hover:bg-white/4 hover:text-text-primary'}
              disabled:opacity-40`}
          >
            <Play size={8} className="shrink-0 opacity-40" />
            <span className="truncate flex-1">
              {item.displayName || item.filename}
            </span>
            {item.duration_s != null && (
              <span className="text-[9px] mono text-text-tertiary shrink-0">
                {item.duration_s.toFixed(1)}s
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
