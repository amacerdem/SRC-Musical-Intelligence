import { PageShell } from '../../components/layout/PageShell'

export function RamViewer() {
  return (
    <PageShell title="Region Activation Map" subtitle="26 brain region activations \u2014 12 cortical + 9 subcortical + 5 brainstem">
      <div className="glass-card p-6 mt-4">
        <p className="text-sm text-text-secondary">
          RAM viewer will display a (B, T, 26) activation heatmap with per-region traces.
          Regions receive weighted contributions from mechanism RegionLinks.
        </p>
      </div>
    </PageShell>
  )
}
