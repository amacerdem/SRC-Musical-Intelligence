import { PageShell } from '../../components/layout/PageShell'

export function NeuroacousticAtlas() {
  return (
    <PageShell title="Neuroacoustic Atlas" subtitle="Interactive 3D brain atlas with MNI152 coordinates">
      <div className="glass-card p-6 mt-4">
        <p className="text-sm text-text-secondary">
          Atlas visualization \u2014 26 brain regions mapped in MNI152 space
          with functional role descriptions and relay connectivity.
        </p>
      </div>
    </PageShell>
  )
}
