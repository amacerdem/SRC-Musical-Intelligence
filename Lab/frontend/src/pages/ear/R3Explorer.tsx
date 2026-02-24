import { PageShell } from '../../components/layout/PageShell'

export function R3Explorer() {
  return (
    <PageShell title="R\u00b3 Features" subtitle="Early Perceptual Front-End \u2014 97D spectral features across 9 groups">
      <div className="glass-card p-6 mt-4">
        <p className="text-sm text-text-secondary">
          R\u00b3 feature explorer will display 97 dimensions organized by group:
          A[0:7], B[7:12], C[12:21], D[21:25], F[25:41], G[41:51], H[51:63], J[63:83], K[83:97]
        </p>
      </div>
    </PageShell>
  )
}
