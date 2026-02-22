import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar';
import TopBar from './components/layout/TopBar';
import Dashboard from './pages/Dashboard';
import PipelineRunner from './pages/PipelineRunner';
import R3Explorer from './pages/R3Explorer';
import H3Explorer from './pages/H3Explorer';
import C3Explorer from './pages/C3Explorer';
import RewardAnalyzer from './pages/RewardAnalyzer';
import ExperimentCompare from './pages/ExperimentCompare';
import Documentation from './pages/Documentation';
import NeuroacousticAtlas from './pages/NeuroacousticAtlas';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen w-screen" style={{ background: 'var(--bg)' }}>
        {/* Sidebar */}
        <Sidebar />

        {/* Main content */}
        <div className="flex-1 flex flex-col min-w-0">
          <TopBar />
          <main className="flex-1 overflow-hidden">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/pipeline" element={<PipelineRunner />} />
              <Route path="/r3" element={<R3Explorer />} />
              <Route path="/h3" element={<H3Explorer />} />
              <Route path="/c3" element={<C3Explorer />} />
              <Route path="/reward" element={<RewardAnalyzer />} />
              <Route path="/compare" element={<ExperimentCompare />} />
              <Route path="/docs" element={<Documentation />} />
              <Route path="/atlas" element={<NeuroacousticAtlas />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
