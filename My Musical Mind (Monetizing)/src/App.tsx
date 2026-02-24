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
import { Friends } from "@/pages/Friends";
import { ProfileView } from "@/pages/ProfileView";
import { ResonanceField } from "@/pages/ResonanceField";
import { Leaderboard } from "@/pages/Leaderboard";
import { Discover } from "@/pages/Discover";
import { InfoHub } from "@/pages/InfoHub";
import { M3Hub } from "@/pages/M3Hub";

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

          {/* App routes (with shell) */}
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
            <Route path="/discover" element={<Discover />} />
            <Route path="/friends" element={<Friends />} />
            <Route path="/friends/:userId" element={<ProfileView />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/info" element={<InfoHub />} />
            <Route path="/info/:id" element={<PersonaDetail />} />
          </Route>

          {/* Redirects for old routes */}
          <Route path="/arena" element={<Navigate to="/live" replace />} />
          <Route path="/listen" element={<Navigate to="/discover" replace />} />
          <Route path="/social/:userId" element={<Navigate to="/friends" replace />} />
          <Route path="/social" element={<Navigate to="/friends" replace />} />
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
