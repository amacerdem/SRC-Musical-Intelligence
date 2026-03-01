import { Outlet, useLocation } from "react-router-dom";
import { FloatingNav } from "./FloatingNav";
import { MindChat } from "@/components/chat/MindChat";
import { useSmoothScroll } from "@/hooks/useSmoothScroll";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { useUserStore } from "@/stores/useUserStore";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { useMobile } from "@/hooks/useMediaQuery";

export function AppShell() {
  useSmoothScroll();
  const location = useLocation();
  const { mind } = useUserStore();
  const { color, morphology } = useActiveIdentity();
  const stage = mind?.stage ?? 1;
  const isMobile = useMobile();
  const isImmersive = location.pathname === "/live" || location.pathname === "/lab";

  return (
    <div className="min-h-screen bg-black relative">
      {/* Persistent ambient organism background (hidden on immersive pages) */}
      {!isMobile && !isImmersive && (
        <div className="fixed inset-0 z-0 opacity-[0.10] pointer-events-none">
          <MindOrganismCanvas
            color={color}
            stage={stage as 1 | 2 | 3}
            intensity={0.15}
            breathRate={8}
            variant="ambient"
            familyMorphology={morphology}
            className="w-full h-full"
            interactive={false}
          />
        </div>
      )}

      <main className={`relative z-10 min-h-screen ${isImmersive ? "" : `overflow-y-auto ${isMobile ? "pb-20" : "pb-24"} px-4 sm:px-6 md:px-8 lg:px-12 xl:px-16 pt-16`}`}
        style={isMobile && !isImmersive ? { paddingBottom: "calc(56px + env(safe-area-inset-bottom, 0px))" } : undefined}
      >
        <Outlet />
      </main>
      <FloatingNav />
      <MindChat />
    </div>
  );
}
