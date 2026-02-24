import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { PageShell } from '../components/layout/PageShell'
import { AudioTimeline } from '../components/audio/AudioTimeline'
import { FUNCTIONS } from '../data/functions'
import { BELIEFS } from '../data/beliefs'
import { MECHANISMS } from '../data/mechanisms'
import { RELAYS } from '../data/relays'
import { usePipelineStore } from '../stores/pipelineStore'
import { useC3Store } from '../stores/c3Store'
import { Brain, AudioWaveform, Clock, Award, MapPin, Layers, Play, Loader2, CheckCircle2, AlertCircle } from 'lucide-react'

export function Overview() {
  const totalBeliefs = BELIEFS.length
  const totalMechanisms = MECHANISMS.length
  const totalRelays = RELAYS.length
  const coreCount = BELIEFS.filter((b) => b.type === 'core').length

  const {
    audioCatalog,
    catalogLoading,
    experiments,
    currentExperiment,
    pipelineStatus,
    runningExperiment,
    fetchCatalog,
    fetchExperiments,
    runPipeline,
    selectExperiment,
  } = usePipelineStore()

  const beliefsLoading = useC3Store((s) => s.beliefsLoading)
  const nFrames = useC3Store((s) => s.nFrames)

  const [selectedAudio, setSelectedAudio] = useState('')
  const [excerptS, setExcerptS] = useState(0) // 0 = full

  // Fetch catalog and experiments on mount
  useEffect(() => {
    fetchCatalog()
    fetchExperiments()
  }, [fetchCatalog, fetchExperiments])

  // Auto-select first audio when catalog loads
  useEffect(() => {
    if (audioCatalog.length > 0 && !selectedAudio) {
      setSelectedAudio(audioCatalog[0].name)
    }
  }, [audioCatalog, selectedAudio])

  const isRunning = runningExperiment !== null

  const handleRun = () => {
    if (!selectedAudio || isRunning) return
    runPipeline(selectedAudio, excerptS > 0 ? excerptS : undefined)
  }

  return (
    <PageShell title="Overview" subtitle="MI Pipeline Experiment Dashboard">
      {/* Synced audio timeline */}
      <AudioTimeline className="mt-4" />

      {/* Pipeline Control Panel */}
      <div className="glass-card p-5 mt-4">
        <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">Pipeline Control</div>
        <div className="flex items-end gap-4">
          {/* Audio selector */}
          <div className="flex-1">
            <label className="text-xs text-text-secondary block mb-1">Audio Source</label>
            <select
              value={selectedAudio}
              onChange={(e) => setSelectedAudio(e.target.value)}
              disabled={isRunning}
              className="w-full bg-bg-secondary border border-white/10 rounded-lg px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-blue-500/50"
            >
              {catalogLoading && <option>Loading...</option>}
              {audioCatalog.map((a) => (
                <option key={a.name} value={a.name} disabled={!a.available}>
                  {a.name} {a.duration_s ? `(${a.duration_s.toFixed(1)}s)` : ''} {a.available ? '' : ' [missing]'}
                </option>
              ))}
            </select>
          </div>

          {/* Excerpt duration */}
          <div className="w-32">
            <label className="text-xs text-text-secondary block mb-1">Duration</label>
            <select
              value={excerptS}
              onChange={(e) => setExcerptS(Number(e.target.value))}
              disabled={isRunning}
              className="w-full bg-bg-secondary border border-white/10 rounded-lg px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-blue-500/50"
            >
              <option value={0}>Full</option>
              <option value={5}>5s</option>
              <option value={10}>10s</option>
              <option value={30}>30s</option>
              <option value={60}>60s</option>
            </select>
          </div>

          {/* Run button */}
          <button
            onClick={handleRun}
            disabled={isRunning || !selectedAudio}
            className="flex items-center gap-2 px-5 py-2 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/30 transition-colors disabled:opacity-40 disabled:cursor-not-allowed text-sm font-medium"
          >
            {isRunning ? <Loader2 size={16} className="animate-spin" /> : <Play size={16} />}
            {isRunning ? 'Running...' : 'Run Analysis'}
          </button>
        </div>

        {/* Progress bar */}
        {pipelineStatus && (
          <div className="mt-3">
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="text-text-secondary flex items-center gap-1.5">
                {pipelineStatus.status === 'done' && <CheckCircle2 size={12} className="text-emerald-400" />}
                {pipelineStatus.status === 'error' && <AlertCircle size={12} className="text-red-400" />}
                {pipelineStatus.status === 'running' && <Loader2 size={12} className="text-blue-400 animate-spin" />}
                {pipelineStatus.phase}
              </span>
              <span className="mono text-text-tertiary">
                {pipelineStatus.status === 'done' && `${pipelineStatus.fps.toFixed(0)} fps`}
                {pipelineStatus.status === 'running' && `${(pipelineStatus.progress * 100).toFixed(0)}%`}
                {pipelineStatus.status === 'error' && pipelineStatus.error}
              </span>
            </div>
            <div className="h-1 bg-white/5 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-300 ${
                  pipelineStatus.status === 'done' ? 'bg-emerald-500' :
                  pipelineStatus.status === 'error' ? 'bg-red-500' :
                  'bg-blue-500'
                }`}
                style={{ width: `${pipelineStatus.progress * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Experiment Selector */}
      {experiments.length > 0 && (
        <div className="glass-card p-5 mt-3">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">
            Experiments
            {beliefsLoading && <Loader2 size={10} className="inline-block ml-2 animate-spin" />}
            {currentExperiment && nFrames > 0 && (
              <span className="ml-2 text-emerald-400 normal-case">
                {nFrames} frames loaded
              </span>
            )}
          </div>
          <div className="flex flex-wrap gap-2">
            {experiments.map((exp) => (
              <button
                key={exp.experiment_id}
                onClick={() => selectExperiment(exp.experiment_id)}
                className={`px-3 py-1.5 rounded-lg text-xs mono transition-colors border ${
                  currentExperiment === exp.experiment_id
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                    : 'bg-white/5 text-text-secondary border-white/10 hover:bg-white/10'
                }`}
              >
                {exp.audio_name} ({exp.n_frames}f @ {exp.fps?.toFixed(0)}fps)
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Top metrics row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
        <MetricCard
          icon={<AudioWaveform size={18} />}
          label="R\u00b3 Features"
          value="97D"
          detail="9 groups \u00b7 FROZEN v1.0.0"
          color="#60a5fa"
        />
        <MetricCard
          icon={<Clock size={18} />}
          label="H\u00b3 Morphology"
          value="223,488"
          detail="theoretical tuples \u00b7 32 horizons"
          color="#a78bfa"
        />
        <MetricCard
          icon={<Brain size={18} />}
          label="C\u00b3 Beliefs"
          value={String(totalBeliefs)}
          detail={`${coreCount} Core + ${totalBeliefs - coreCount - 30} Appraisal + 30 Anticipation`}
          color="#34d399"
        />
        <MetricCard
          icon={<Layers size={18} />}
          label="Mechanisms"
          value={String(totalMechanisms)}
          detail={`${totalRelays} relays \u00b7 depth 0\u20135`}
          color="#f59e0b"
        />
      </div>

      {/* Pipeline architecture */}
      <div className="glass-card p-5 mt-6">
        <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">Pipeline Architecture</div>
        <div className="flex items-center gap-3 text-sm mono">
          <span className="px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
            Audio
          </span>
          <span className="text-text-tertiary">{'\u2192'}</span>
          <Link to="/r3" className="px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20 hover:bg-blue-500/15 transition-colors no-underline">
            R{'\u00b3'} (97D)
          </Link>
          <span className="text-text-tertiary">{'\u2192'}</span>
          <Link to="/h3" className="px-3 py-1.5 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20 hover:bg-purple-500/15 transition-colors no-underline">
            H{'\u00b3'} (277 tuples)
          </Link>
          <span className="text-text-tertiary">{'\u2192'}</span>
          <span className="px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            C{'\u00b3'} (131 beliefs)
          </span>
          <span className="text-text-tertiary">{'\u2192'}</span>
          <Link to="/ram" className="px-3 py-1.5 rounded-lg bg-teal-500/10 text-teal-400 border border-teal-500/20 hover:bg-teal-500/15 transition-colors no-underline">
            RAM (26D)
          </Link>
          <span className="text-text-tertiary">{'\u2192'}</span>
          <span className="px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
            {'\u03a8\u00b3'} (28D)
          </span>
        </div>
      </div>

      {/* Function grid */}
      <div className="flex items-center justify-between mt-8 mb-3">
        <h2 className="text-sm font-semibold text-text-secondary">C{'\u00b3'} Functions</h2>
        <span className="text-xs text-text-tertiary mono">9 functions {'\u00b7'} {totalBeliefs} beliefs {'\u00b7'} {totalMechanisms} mechanisms</span>
      </div>
      <div className="grid grid-cols-3 gap-3">
        {FUNCTIONS.map((fn) => (
          <Link
            key={fn.id}
            to={`/brain/${fn.id}`}
            className="glass-card p-4 no-underline block group"
          >
            <div className="flex items-center gap-2 mb-2">
              <span
                className="w-2.5 h-2.5 rounded-full transition-shadow group-hover:shadow-[0_0_8px]"
                style={{ backgroundColor: fn.color, ['--tw-shadow-color' as string]: fn.color }}
              />
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
              {fn.mechanismCount} mechanisms {'\u00b7'} {fn.unit}
              {fn.relay && <> {'\u00b7'} {fn.relay}</>}
            </div>
          </Link>
        ))}
      </div>

      {/* Quick links */}
      <div className="grid grid-cols-2 gap-3 mt-6">
        <Link to="/reward" className="glass-card p-4 flex items-center gap-3 no-underline hover:bg-white/[0.06] transition-colors">
          <Award size={20} className="text-amber-400" />
          <div>
            <div className="text-sm font-medium text-text-primary">Reward Analyzer</div>
            <div className="text-xs text-text-tertiary">SRP 19D {'\u00b7'} wanting/liking/pleasure</div>
          </div>
        </Link>
        <Link to="/ram" className="glass-card p-4 flex items-center gap-3 no-underline hover:bg-white/[0.06] transition-colors">
          <MapPin size={20} className="text-teal-400" />
          <div>
            <div className="text-sm font-medium text-text-primary">Region Activation Map</div>
            <div className="text-xs text-text-tertiary">26 regions {'\u00b7'} 12 cortical + 9 subcortical + 5 brainstem</div>
          </div>
        </Link>
      </div>
    </PageShell>
  )
}

function MetricCard({ icon, label, value, detail, color }: {
  icon: React.ReactNode; label: string; value: string; detail: string; color: string
}) {
  return (
    <div className="glass-card p-5">
      <div className="flex items-center gap-2 mb-2">
        <span style={{ color }}>{icon}</span>
        <span className="text-xs text-text-tertiary uppercase tracking-wider">{label}</span>
      </div>
      <div className="text-2xl font-semibold mono" style={{ color }}>{value}</div>
      <div className="text-xs text-text-secondary mt-1">{detail}</div>
    </div>
  )
}
