import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AnimatePresence } from "framer-motion";
import { AppShell } from "@/components/layout/AppShell";
import { useUserStore } from "@/stores/useUserStore";

/* Pages */
import { Landing } from "@/pages/Landing";
import { Onboarding } from "@/pages/Onboarding";
import { MindReveal } from "@/pages/MindReveal";
import { Dashboard } from "@/pages/Dashboard";
import { PersonaDetail } from "@/pages/PersonaDetail";
import { ExploreAE } from "@/pages/ExploreAE";
import { ResonanceField } from "@/pages/ResonanceField";
import { InfoHub } from "@/pages/InfoHub";
import { M3Hub } from "@/pages/M3Hub";
import { Callback } from "@/pages/Callback";

export default function App() {
  const { hasCompletedOnboarding } = useUserStore();

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

          {/* App routes (with shell) — 4 main pages */}
          <Route element={<AppShell />}>
            <Route
              path="/m3"
              element={
                hasCompletedOnboarding ? <M3Hub /> : <Navigate to="/" />
              }
            />
            <Route
              path="/dashboard"
              element={
                hasCompletedOnboarding ? <Dashboard /> : <Navigate to="/" />
              }
            />
            <Route path="/live" element={<ResonanceField />} />
            <Route path="/info" element={<InfoHub />} />
            <Route path="/info/:id" element={<PersonaDetail />} />
          </Route>

          {/* Redirects for removed/old routes */}
          <Route path="/discover" element={<Navigate to="/dashboard" replace />} />
          <Route path="/friends" element={<Navigate to="/dashboard" replace />} />
          <Route path="/friends/:userId" element={<Navigate to="/dashboard" replace />} />
          <Route path="/leaderboard" element={<Navigate to="/dashboard" replace />} />
          <Route path="/arena" element={<Navigate to="/live" replace />} />
          <Route path="/listen" element={<Navigate to="/dashboard" replace />} />
          <Route path="/social/:userId" element={<Navigate to="/dashboard" replace />} />
          <Route path="/social" element={<Navigate to="/dashboard" replace />} />
          <Route path="/personas/:id" element={<Navigate to="/info" replace />} />
          <Route path="/personas" element={<Navigate to="/info" replace />} />
          <Route path="/explorer" element={<Navigate to="/dashboard" replace />} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AnimatePresence>
    </BrowserRouter>
  );
}
