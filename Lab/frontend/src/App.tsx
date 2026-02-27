import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AppLayout } from './components/layout/AppLayout'
import { Overview } from './pages/Overview'
import { R3Explorer } from './pages/ear/R3Explorer'
import { H3Explorer } from './pages/ear/H3Explorer'
import { FunctionPage } from './pages/brain/FunctionPage'
import { RewardAnalyzer } from './pages/output/RewardAnalyzer'
import { RamViewer } from './pages/output/RamViewer'
import { PipelineRunner } from './pages/tools/PipelineRunner'
import { NeuroacousticAtlas } from './pages/tools/NeuroacousticAtlas'
import { Library } from './pages/tools/Library'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Overview />} />
          <Route path="r3" element={<R3Explorer />} />
          <Route path="h3" element={<H3Explorer />} />
          <Route path="brain/:fId" element={<FunctionPage />} />
          <Route path="reward" element={<RewardAnalyzer />} />
          <Route path="ram" element={<RamViewer />} />
          <Route path="library" element={<Library />} />
          <Route path="pipeline" element={<PipelineRunner />} />
          <Route path="atlas" element={<NeuroacousticAtlas />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
