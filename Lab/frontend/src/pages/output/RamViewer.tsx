import { PageShell } from '../../components/layout/PageShell'
import { HeatmapChart } from '../../components/charts/HeatmapChart'

const REGIONS = [
  { idx: 0, name: 'Primary Auditory Cortex', abbr: 'A1_HG', mni: '(48, -18, 8)', group: 'cortical', ba: '41' },
  { idx: 1, name: 'Superior Temporal Gyrus', abbr: 'STG', mni: '(58, -22, 4)', group: 'cortical', ba: '22' },
  { idx: 2, name: 'Superior Temporal Sulcus', abbr: 'STS', mni: '(54, -32, 4)', group: 'cortical', ba: '21' },
  { idx: 3, name: 'Inferior Frontal Gyrus', abbr: 'IFG', mni: '(48, 18, 8)', group: 'cortical', ba: '44' },
  { idx: 4, name: 'Dorsolateral Prefrontal', abbr: 'dlPFC', mni: '(42, 32, 30)', group: 'cortical', ba: '46' },
  { idx: 5, name: 'Ventromedial Prefrontal', abbr: 'vmPFC', mni: '(2, 46, -10)', group: 'cortical', ba: '10' },
  { idx: 6, name: 'Orbitofrontal Cortex', abbr: 'OFC', mni: '(28, 34, -16)', group: 'cortical', ba: '11' },
  { idx: 7, name: 'Anterior Cingulate', abbr: 'ACC', mni: '(2, 30, 28)', group: 'cortical', ba: '32' },
  { idx: 8, name: 'Supplementary Motor Area', abbr: 'SMA', mni: '(2, -2, 56)', group: 'cortical', ba: '6' },
  { idx: 9, name: 'Premotor Cortex', abbr: 'PMC', mni: '(46, 0, 48)', group: 'cortical', ba: '6' },
  { idx: 10, name: 'Angular Gyrus', abbr: 'AG', mni: '(48, -60, 30)', group: 'cortical', ba: '39' },
  { idx: 11, name: 'Temporal Pole', abbr: 'TP', mni: '(42, 12, -32)', group: 'cortical', ba: '38' },
  { idx: 12, name: 'Ventral Tegmental Area', abbr: 'VTA', mni: '(0, -16, -8)', group: 'subcortical' },
  { idx: 13, name: 'Nucleus Accumbens', abbr: 'NAcc', mni: '(10, 12, -8)', group: 'subcortical' },
  { idx: 14, name: 'Caudate Nucleus', abbr: 'caudate', mni: '(12, 10, 10)', group: 'subcortical' },
  { idx: 15, name: 'Amygdala', abbr: 'amygdala', mni: '(24, -4, -18)', group: 'subcortical' },
  { idx: 16, name: 'Hippocampus', abbr: 'hippocampus', mni: '(28, -22, -12)', group: 'subcortical' },
  { idx: 17, name: 'Putamen', abbr: 'putamen', mni: '(26, 4, 2)', group: 'subcortical' },
  { idx: 18, name: 'Thalamus (MGB)', abbr: 'MGB', mni: '(14, -24, -2)', group: 'subcortical' },
  { idx: 19, name: 'Hypothalamus', abbr: 'hypothalamus', mni: '(0, -4, -8)', group: 'subcortical' },
  { idx: 20, name: 'Insula', abbr: 'insula', mni: '(36, 16, 0)', group: 'subcortical' },
  { idx: 21, name: 'Inferior Colliculus', abbr: 'IC', mni: '(0, -34, -8)', group: 'brainstem' },
  { idx: 22, name: 'Auditory Nerve', abbr: 'AN', mni: '(8, -26, -24)', group: 'brainstem' },
  { idx: 23, name: 'Cochlear Nucleus', abbr: 'CN', mni: '(10, -38, -32)', group: 'brainstem' },
  { idx: 24, name: 'Superior Olivary Complex', abbr: 'SOC', mni: '(6, -34, -24)', group: 'brainstem' },
  { idx: 25, name: 'Periaqueductal Gray', abbr: 'PAG', mni: '(0, -30, -10)', group: 'brainstem' },
]

const GROUP_COLORS: Record<string, string> = {
  cortical: '#3b82f6',
  subcortical: '#f59e0b',
  brainstem: '#22c55e',
}

export function RamViewer() {
  const groups = ['cortical', 'subcortical', 'brainstem'] as const

  return (
    <PageShell title="Region Activation Map" subtitle="26 brain region activations \u2014 12 cortical + 9 subcortical + 5 brainstem">
      <div className="space-y-6 mt-4">
        {/* Summary */}
        <div className="flex gap-4">
          {groups.map((g) => {
            const count = REGIONS.filter((r) => r.group === g).length
            return (
              <div key={g} className="glass-card p-4 flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: GROUP_COLORS[g] }} />
                  <span className="text-xs text-text-tertiary uppercase tracking-wider">{g}</span>
                </div>
                <div className="text-xl font-semibold mono" style={{ color: GROUP_COLORS[g] }}>{count}</div>
              </div>
            )
          })}
        </div>

        {/* Heatmap placeholder — 26 regions × T frames */}
        <div className="glass-card p-5">
          <div className="text-xs text-text-tertiary uppercase tracking-wider mb-3">Region Activation Heatmap (26 × T)</div>
          <HeatmapChart
            data={null}
            rows={26}
            cols={100}
            rowLabels={REGIONS.map((r) => r.abbr)}
            colorScheme="plasma"
            height={260}
          />
          <div className="text-[10px] text-text-tertiary mt-2">
            Pipeline: \u03a3(relay_dim \u00d7 link_weight) \u2192 ReLU \u2192 z-normalize(T&gt;1) \u2192 sigmoid \u2192 [0,1]
          </div>
        </div>

        {/* Region table */}
        {groups.map((g) => (
          <div key={g}>
            <div className="section-divider mb-3"><span>{g}</span></div>
            <div className="glass-card overflow-hidden">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-border-subtle">
                    <th className="text-left px-4 py-2 text-text-tertiary font-medium w-8">#</th>
                    <th className="text-left px-4 py-2 text-text-tertiary font-medium w-16">Abbr</th>
                    <th className="text-left px-4 py-2 text-text-tertiary font-medium">Name</th>
                    <th className="text-left px-4 py-2 text-text-tertiary font-medium">MNI</th>
                    {'ba' in REGIONS[0] && (
                      <th className="text-left px-4 py-2 text-text-tertiary font-medium w-12">BA</th>
                    )}
                    <th className="text-right px-4 py-2 text-text-tertiary font-medium w-20">Trace</th>
                  </tr>
                </thead>
                <tbody>
                  {REGIONS.filter((r) => r.group === g).map((r) => (
                    <tr key={r.idx} className="border-b border-border-subtle/50 hover:bg-white/2">
                      <td className="px-4 py-2 mono text-text-tertiary">{r.idx}</td>
                      <td className="px-4 py-2 mono font-semibold" style={{ color: GROUP_COLORS[g] }}>{r.abbr}</td>
                      <td className="px-4 py-2 text-text-primary">{r.name}</td>
                      <td className="px-4 py-2 mono text-text-secondary">{r.mni}</td>
                      {'ba' in r && <td className="px-4 py-2 mono text-text-tertiary">{(r as { ba?: string }).ba ?? '\u2014'}</td>}
                      <td className="px-4 py-2 text-right text-text-tertiary italic">no data</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </PageShell>
  )
}
