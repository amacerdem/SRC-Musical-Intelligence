import { useEffect } from "react";
import { useStore } from "./store";
import { colors, fonts, sizes } from "./theme/tokens";
import { HeaderBar } from "./layout/HeaderBar";
import { AudioTransport } from "./layout/AudioTransport";
import { NavigationTree } from "./layout/NavigationTree";
import { MainGrid } from "./layout/MainGrid";
import { DetailDrawer } from "./layout/DetailDrawer";

export function App() {
  const loadRegistry = useStore((s) => s.loadRegistry);
  const loadExperimentList = useStore((s) => s.loadExperimentList);
  const drawerOpen = useStore((s) => s.detailDrawerOpen);

  useEffect(() => {
    loadRegistry();
    loadExperimentList();
  }, [loadRegistry, loadExperimentList]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "grid",
        gridTemplateRows: `${sizes.headerHeight}px ${sizes.transportHeight}px 1fr ${drawerOpen ? sizes.drawerHeight : 32}px`,
        gridTemplateColumns: `${sizes.sidebarWidth}px 1fr`,
        gridTemplateAreas: `
          "header    header"
          "transport transport"
          "sidebar   main"
          "drawer    drawer"
        `,
        background: colors.bg.primary,
        fontFamily: fonts.ui,
        color: colors.text.primary,
        overflow: "hidden",
      }}
    >
      <div style={{ gridArea: "header" }}>
        <HeaderBar />
      </div>
      <div style={{ gridArea: "transport" }}>
        <AudioTransport />
      </div>
      <div style={{ gridArea: "sidebar" }}>
        <NavigationTree />
      </div>
      <div style={{ gridArea: "main", overflow: "auto" }}>
        <MainGrid />
      </div>
      <div style={{ gridArea: "drawer" }}>
        <DetailDrawer />
      </div>
    </div>
  );
}
