import { useStore } from "../store";
import R3SpectralPage from "../pages/R3SpectralPage";
import NucleusPage from "../pages/NucleusPage";
import BrainRegionsPage from "../pages/BrainRegionsPage";
import NeuroPage from "../pages/NeuroPage";
import PsiPage from "../pages/PsiPage";
import H3Page from "../pages/H3Page";
import EvidencePage from "../pages/EvidencePage";

export function TabContent() {
  const tab = useStore((s) => s.activeTab);

  return (
    <div style={{ flex: 1, minHeight: 0, overflow: "hidden" }}>
      {tab === "r3" && <R3SpectralPage />}
      {tab === "nucleus" && <NucleusPage />}
      {tab === "brain" && <BrainRegionsPage />}
      {tab === "neuro" && <NeuroPage />}
      {tab === "psi" && <PsiPage />}
      {tab === "h3" && <H3Page />}
      {tab === "evidence" && <EvidencePage />}
    </div>
  );
}
