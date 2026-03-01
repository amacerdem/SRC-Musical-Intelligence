import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { AppShell } from "@/components/layout/AppShell";
import { useUserStore } from "@/stores/useUserStore";
import { miDataService } from "@/services/MIDataService";
import { initLibraryTracks } from "@/data/track-library";
import { initListeningData } from "@/data/mock-listening";
import { initRecommendedTracks } from "@/data/mock-tracks";

/* Pages */
import { Landing } from "@/pages/Landing";
import { Onboarding } from "@/pages/Onboarding";
import { MindReveal } from "@/pages/MindReveal";
import { Dashboard } from "@/pages/Dashboard";
import { PersonaDetail } from "@/pages/PersonaDetail";
import { ExploreAE } from "@/pages/ExploreAE";
import { ResonanceField } from "@/pages/ResonanceField";
import { M3Hub } from "@/pages/M3Hub";
import { Callback } from "@/pages/Callback";
import { LibraryAuth } from "@/pages/LibraryAuth";

import { Lab } from "@/pages/Lab";
import { Listen } from "@/pages/Listen";

export default function App() {
  const { hasCompletedOnboarding } = useUserStore();
  const [dataReady, setDataReady] = useState(false);

  useEffect(() => {
    miDataService.init().then(() => {
      initLibraryTracks();
      initListeningData();
      initRecommendedTracks();
      setDataReady(true);
    });
  }, []);

  if (!dataReady) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white/60 text-sm animate-pulse">Loading MI data...</div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <AnimatePresence mode="wait">
        <Routes>
          {/* Public routes (no shell) */}
          <Route path="/" element={<Landing />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/reveal" element={<MindReveal />} />
          <Route path="/explore-ae" element={<ExploreAE />} />
          <Route path="/callback" element={<Callback />} />
          <Route path="/library" element={<LibraryAuth />} />

          {/* App routes (with shell) — 6 main pages */}
          <Route element={<AppShell />}>
            <Route
              path="/listen"
              element={
                hasCompletedOnboarding ? <Listen /> : <Navigate to="/" />
              }
            />
            <Route
              path="/my-mind"
              element={
                hasCompletedOnboarding ? <Dashboard /> : <Navigate to="/" />
              }
            />
            <Route
              path="/lab"
              element={
                hasCompletedOnboarding ? <Lab /> : <Navigate to="/" />
              }
            />
            <Route
              path="/m3"
              element={
                hasCompletedOnboarding ? <M3Hub /> : <Navigate to="/" />
              }
            />
            <Route path="/live" element={<ResonanceField />} />
            <Route path="/info" element={<PersonaDetail />} />
            <Route path="/info/:id" element={<PersonaDetail />} />
          </Route>

          {/* Redirects for removed/old routes */}
          <Route path="/dashboard" element={<Navigate to="/my-mind" replace />} />
          <Route path="/discover" element={<Navigate to="/my-mind" replace />} />
          <Route path="/friends" element={<Navigate to="/my-mind" replace />} />
          <Route path="/friends/:userId" element={<Navigate to="/my-mind" replace />} />
          <Route path="/leaderboard" element={<Navigate to="/my-mind" replace />} />
          <Route path="/arena" element={<Navigate to="/live" replace />} />
          {/* /listen is now a real route — no redirect needed */}
          <Route path="/social/:userId" element={<Navigate to="/my-mind" replace />} />
          <Route path="/social" element={<Navigate to="/my-mind" replace />} />
          <Route path="/personas/:id" element={<Navigate to="/info" replace />} />
          <Route path="/personas" element={<Navigate to="/info" replace />} />
          <Route path="/explorer" element={<Navigate to="/my-mind" replace />} />
          <Route path="/spotify" element={<Navigate to="/my-mind" replace />} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AnimatePresence>
    </BrowserRouter>
  );
}
