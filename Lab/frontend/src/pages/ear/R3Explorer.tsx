import { useState } from 'react'
import { PageShell } from '../../components/layout/PageShell'
import { AudioTimeline } from '../../components/audio/AudioTimeline'
import { GlassChip } from '../../components/glass/GlassChip'
import { ChevronDown, ChevronRight } from 'lucide-react'

const R3_GROUPS = [
  {
    id: 'A', name: 'Consonance', range: [0, 7], dim: 7, stage: 1, color: '#f97316',
    domain: 'Psychoacoustic',
    features: [
      'roughness_total', 'roughness_avg', 'roughness_peak',
      'sethares_dissonance', 'pleasantness', 'helmholtz_consonance', 'stumpf_fusion',
    ],
  },
  {
    id: 'B', name: 'Energy', range: [7, 12], dim: 5, stage: 1, color: '#ef4444',
    domain: 'Spectral',
    features: ['amplitude', 'velocity_A', 'velocity_D', 'rms_energy', 'onset_strength'],
  },
  {
    id: 'C', name: 'Timbre', range: [12, 21], dim: 9, stage: 1, color: '#8b5cf6',
    domain: 'Spectral',
    features: [
      'spectral_centroid', 'spectral_bandwidth', 'brightness_kuttruff',
      'spectral_flatness', 'spectral_entropy', 'spectral_rolloff',
      'spectral_crest', 'spectral_contrast', 'spectral_irregularity',
    ],
  },
  {
    id: 'D', name: 'Change', range: [21, 25], dim: 4, stage: 1, color: '#22c55e',
    domain: 'Temporal',
    features: ['spectral_flux', 'centroid_delta', 'brightness_delta', 'distribution_concentration'],
  },
  {
    id: 'F', name: 'Pitch/Chroma', range: [25, 41], dim: 16, stage: 1, color: '#3b82f6',
    domain: 'Tonal',
    features: [
      'pitch_salience', 'pitch_confidence', 'pitch_class',
      'chroma_0', 'chroma_1', 'chroma_2', 'chroma_3', 'chroma_4', 'chroma_5',
      'chroma_6', 'chroma_7', 'chroma_8', 'chroma_9', 'chroma_10', 'chroma_11',
      'pitch_class_entropy',
    ],
  },
  {
    id: 'G', name: 'Rhythm/Groove', range: [41, 51], dim: 10, stage: 2, color: '#f59e0b',
    domain: 'Temporal', deps: 'energy',
    features: [
      'tempo_estimate', 'beat_strength', 'downbeat_strength', 'syncopation',
      'groove_consistency', 'micro_timing', 'rhythmic_complexity',
      'event_density', 'beat_phase', 'tempo_stability',
    ],
  },
  {
    id: 'H', name: 'Harmony', range: [51, 63], dim: 12, stage: 2, color: '#ec4899',
    domain: 'Tonal', deps: 'pitch_chroma',
    features: [
      'key_clarity', 'tonnetz_0', 'tonnetz_1', 'tonnetz_2',
      'tonnetz_3', 'tonnetz_4', 'tonnetz_5',
      'voice_leading_distance', 'harmonic_change',
      'tonal_stability', 'diatonicity', 'syntactic_irregularity',
    ],
  },
  {
    id: 'J', name: 'Timbre Extended', range: [63, 83], dim: 20, stage: 1, color: '#06b6d4',
    domain: 'Spectral',
    features: [
      'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5',
      'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10',
      'mfcc_11', 'mfcc_12', 'mfcc_13',
      'delta_mfcc_1', 'delta_mfcc_2', 'delta_mfcc_3',
      'delta_mfcc_4', 'delta_mfcc_5', 'delta_mfcc_6', 'delta_mfcc_7',
    ],
  },
  {
    id: 'K', name: 'Modulation', range: [83, 97], dim: 14, stage: 1, color: '#a855f7',
    domain: 'Psychoacoustic',
    features: [
      'am_rate', 'am_depth', 'am_regularity',
      'fm_rate', 'fm_depth', 'fm_regularity',
      'roughness_am', 'roughness_fm',
      'fluctuation_strength', 'vibrato_rate', 'vibrato_depth',
      'tremolo_rate', 'tremolo_depth', 'modulation_spectrum_centroid',
    ],
  },
] as const

const STAGE_COLORS: Record<number, string> = { 1: '#22c55e', 2: '#f59e0b' }

export function R3Explorer() {
  const [expanded, setExpanded] = useState<string | null>(null)
  const totalDim = R3_GROUPS.reduce((s, g) => s + g.dim, 0)

  return (
    <PageShell title="R\u00b3 Features" subtitle="Early Perceptual Front-End \u2014 97D spectral features across 9 groups">
      <div className="space-y-5 mt-4">
        {/* Audio sync timeline */}
        <AudioTimeline color="#60a5fa" />

        {/* Summary metrics */}
        <div className="grid grid-cols-4 gap-3">
          {[
            { label: 'Total Dimensions', value: `${totalDim}D`, sub: '9 groups' },
            { label: 'Stage 1 (Independent)', value: '7', sub: '71D' },
            { label: 'Stage 2 (Dependent)', value: '2', sub: '22D' },
            { label: 'Frame Rate', value: '172.27 Hz', sub: '5.8ms/frame' },
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
            <span className="text-text-tertiary">\u2192</span>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: '#f59e0b' }} />
              <span className="text-text-secondary">Stage 2 (G\u2190energy, H\u2190pitch_chroma)</span>
            </div>
            <span className="text-text-tertiary">\u2192</span>
            <span className="text-text-secondary">H\u00b3 / C\u00b3</span>
          </div>
        </div>

        {/* Dimension bar */}
        <div className="glass-card p-4">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-2">Dimension Distribution</div>
          <div className="flex h-6 rounded-md overflow-hidden bg-white/3">
            {R3_GROUPS.map((g) => (
              <div
                key={g.id}
                className="flex items-center justify-center text-[9px] font-semibold mono text-white/90 cursor-pointer hover:opacity-100 transition-opacity"
                style={{
                  width: `${(g.dim / totalDim) * 100}%`,
                  backgroundColor: g.color,
                  opacity: expanded === g.id ? 1 : 0.7,
                }}
                title={`${g.id}: ${g.name} [${g.dim}D]`}
                onClick={() => setExpanded(expanded === g.id ? null : g.id)}
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

        {/* Group panels */}
        {R3_GROUPS.map((group) => {
          const isExpanded = expanded === group.id
          return (
            <div
              key={group.id}
              className={`glass-card cursor-pointer ${isExpanded ? 'ring-1 ring-white/8' : ''}`}
              onClick={() => setExpanded(isExpanded ? null : group.id)}
            >
              {/* Header */}
              <div className="flex items-center gap-3 px-5 py-3">
                <span className="text-text-tertiary shrink-0">
                  {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                </span>
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: group.color }} />
                <span className="mono text-sm font-semibold" style={{ color: group.color }}>
                  {group.id}
                </span>
                <span className="text-sm text-text-primary">{group.name}</span>
                <GlassChip label={`${group.dim}D`} color={group.color} />
                <span className="mono text-[10px] text-text-tertiary">[{group.range[0]}:{group.range[1]})</span>
                <span className="flex-1" />
                <span
                  className="mono text-[10px] px-1.5 py-0.5 rounded"
                  style={{
                    color: STAGE_COLORS[group.stage],
                    backgroundColor: `${STAGE_COLORS[group.stage]}15`,
                  }}
                >
                  S{group.stage}
                </span>
                <span className="text-[10px] text-text-tertiary">{group.domain}</span>
              </div>

              {/* Expanded detail */}
              {isExpanded && (
                <div className="border-t border-border-subtle px-5 py-4 space-y-3" onClick={(e) => e.stopPropagation()}>
                  {'deps' in group && (
                    <div className="text-xs text-text-tertiary">
                      Depends on: <span className="mono text-text-secondary">{group.deps}</span>
                    </div>
                  )}
                  <div className="grid grid-cols-2 gap-x-6 gap-y-1">
                    {group.features.map((feat, i) => (
                      <div key={feat} className="flex items-center gap-2 py-0.5">
                        <span className="mono text-[10px] text-text-tertiary w-6 text-right">
                          {group.range[0] + i}
                        </span>
                        <span className="mono text-xs text-text-secondary">{feat}</span>
                        <span className="flex-1" />
                        <span className="text-[9px] text-text-tertiary italic">no data</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )
        })}

        {/* Boundary spec */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">
            R\u00b3 Boundary Rules (FROZEN v1.0.0)
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
              <span className="mx-2">\u2192</span>
              C\u00b3 input layer (cross-domain products computed per model)
            </div>
            <div>
              <span className="text-text-secondary">Group I (Information, 7D)</span>
              <span className="mx-2">\u2192</span>
              4D \u2192 C\u00b3, 1D \u2192 H\u00b3, 2D removed (redundant)
            </div>
          </div>
        </div>
      </div>
    </PageShell>
  )
}
