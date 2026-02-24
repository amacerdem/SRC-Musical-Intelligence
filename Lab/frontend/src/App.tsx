import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ContextSidebar from './components/layout/ContextSidebar';
import TopBar from './components/layout/TopBar';
import NowPlayingBar from './components/layout/NowPlayingBar';
import DepthTransition from './components/layout/DepthTransition';
import DepthRouter from './components/depth/DepthRouter';
import PipelineModal from './components/depth/PipelineModal';
import Documentation from './pages/Documentation';

export default function App() {
  const [pipelineOpen, setPipelineOpen] = useState(false);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/docs" element={<Documentation />} />
        <Route
          path="*"
          element={
            <div className="flex h-screen w-screen" style={{ background: 'var(--bg)' }}>
              <ContextSidebar />
              <div className="flex-1 flex flex-col min-w-0" style={{ paddingBottom: 44 }}>
                <TopBar onRunPipeline={() => setPipelineOpen(true)} />
                <main className="flex-1 overflow-hidden">
                  <DepthTransition>
                    <DepthRouter />
                  </DepthTransition>
                </main>
              </div>
              <NowPlayingBar />
              <PipelineModal open={pipelineOpen} onClose={() => setPipelineOpen(false)} />
            </div>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
