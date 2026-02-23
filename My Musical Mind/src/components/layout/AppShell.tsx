import { Outlet } from "react-router-dom";
import { FloatingNav } from "./FloatingNav";
import { useSmoothScroll } from "@/hooks/useSmoothScroll";
import { MindOrganismCanvas } from "@/components/mind/MindOrganismCanvas";
import { useUserStore } from "@/stores/useUserStore";
import { personas } from "@/data/personas";
import { useMobile } from "@/hooks/useMediaQuery";

export function AppShell() {
  useSmoothScroll();
  const { mind } = useUserStore();
  const persona = mind ? personas.find((p) => p.id === mind.personaId) : null;
  const color = persona?.color ?? "#A855F7";
  const stage = mind?.stage ?? 1;
  const isMobile = useMobile();

  return (
    <div className="min-h-screen bg-black relative">
      {/* Persistent ambient organism background */}
      {!isMobile && (
        <div className="fixed inset-0 z-0 opacity-[0.06] pointer-events-none">
          <MindOrganismCanvas
            color={color}
            stage={stage as 1 | 2 | 3}
            intensity={0.15}
            breathRate={8}
            variant="ambient"
            className="w-full h-full"
            interactive={false}
          />
        </div>
      )}

      <main className="relative z-10 min-h-screen overflow-y-auto pb-24 px-4 sm:px-6 md:px-8 lg:px-12 xl:px-16 pt-16">
        <Outlet />
      </main>
      <FloatingNav />
    </div>
  );
}
