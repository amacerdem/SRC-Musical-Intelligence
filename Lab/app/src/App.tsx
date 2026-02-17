import { useEffect } from "react";
import { useStore } from "./store";
import { colors, fonts } from "./theme/tokens";
import { HeaderBar } from "./layout/HeaderBar";
import { AudioTransport } from "./layout/AudioTransport";
import { TabBar } from "./layout/TabBar";
import { TabContent } from "./layout/TabContent";

export function App() {
  const loadRegistry = useStore((s) => s.loadRegistry);
  const loadExperimentList = useStore((s) => s.loadExperimentList);

  useEffect(() => {
    loadRegistry();
    loadExperimentList();
  }, [loadRegistry, loadExperimentList]);

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        background: colors.bg.primary,
        fontFamily: fonts.ui,
        color: colors.text.primary,
        overflow: "hidden",
      }}
    >
      <HeaderBar />
      <AudioTransport />
      <TabBar />
      <TabContent />
    </div>
  );
}
