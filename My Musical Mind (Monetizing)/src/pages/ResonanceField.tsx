/* ── ResonanceField — Full-screen immersive experience ────────────── */

import { useEffect } from "react";
import { motion } from "framer-motion";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { ResonanceCanvas } from "@/components/resonance/ResonanceCanvas";
import { ResonanceHUD } from "@/components/resonance/hud/ResonanceHUD";
import { EntranceSequence } from "@/components/resonance/hud/EntranceSequence";

export function ResonanceField() {
  const initialize = useResonanceStore(s => s.initialize);
  const cleanup = useResonanceStore(s => s.cleanup);
  const entranceComplete = useResonanceStore(s => s.entranceComplete);

  useEffect(() => {
    initialize();
    return () => cleanup();
  }, [initialize, cleanup]);

  return (
    <div className="fixed inset-0 bg-black overflow-hidden">
      {/* Cinematic entrance overlay */}
      <EntranceSequence />

      {/* 3D scene */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: entranceComplete ? 1 : 0.3 }}
        transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
        className="absolute inset-0"
      >
        <ResonanceCanvas />
      </motion.div>

      {/* HUD overlay */}
      <ResonanceHUD />

      {/* Cinematic vignette */}
      <div className="cinematic-vignette pointer-events-none" />
    </div>
  );
}
