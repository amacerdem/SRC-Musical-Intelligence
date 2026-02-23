import React, { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useGamificationStore } from "@/stores/useGamificationStore";
import { NeuralFamily } from "@/types/mind";

const FAMILY_COLORS: Record<NeuralFamily, string> = {
    Architects: "#22D3EE",   // Cyan
    Alchemists: "#A855F7",   // Purple
    Explorers: "#F472B6",    // Pink
    Anchors: "#FBBF24",      // Amber
    Kineticists: "#EF4444",  // Red
};

export const MindGardenView: React.FC = () => {
    const { mindGarden, syncMockSpotify } = useGamificationStore();

    // Auto-sync every few seconds for demo purposes
    useEffect(() => {
        const interval = setInterval(() => {
            // 10% chance to "hear" a new track in the background for the demo
            if (Math.random() > 0.9) {
                syncMockSpotify();
            }
        }, 3000);
        return () => clearInterval(interval);
    }, [syncMockSpotify]);

    return (
        <div className="relative w-full h-full bg-black/80 overflow-hidden rounded-3xl border border-white/10">
            {/* Background Ambience */}
            <div className={`absolute inset-0 opacity-20 bg-gradient-to-b from-black via-gray-900 to-${FAMILY_COLORS[mindGarden.dominantFamily || 'Architects'] || 'black'}`} />

            {/* Season Indicator */}
            <div className="absolute top-4 right-6 text-right z-20">
                <h2 className="text-4xl font-light text-white/90 tracking-tighter capitalize">{mindGarden.season}</h2>
                <p className="text-xs text-white/40 uppercase tracking-widest">Seeds Planted: {mindGarden.seedsPlanted}</p>
            </div>

            {/* The Garden Grid (Procedural) */}
            <div className="absolute inset-0 flex items-center justify-center">
                <div className="grid grid-cols-5 gap-4 p-8">
                    <AnimatePresence>
                        {mindGarden.recentTracks.map((track, idx) => (
                            <motion.div
                                key={`${track.id}-${idx}`}
                                initial={{ scale: 0, opacity: 0, y: 20 }}
                                animate={{ scale: 1, opacity: 1, y: 0 }}
                                exit={{ scale: 0, opacity: 0 }}
                                transition={{ type: "spring", stiffness: 200, damping: 20 }}
                                className="relative group"
                            >
                                {/* The Plant Node */}
                                <div
                                    className="w-12 h-12 rounded-full backdrop-blur-md border border-white/20 flex items-center justify-center shadow-[0_0_15px_rgba(0,0,0,0.5)]"
                                    style={{
                                        backgroundColor: `${FAMILY_COLORS[track.dominantFamily]}40`,
                                        boxShadow: `0 0 20px ${FAMILY_COLORS[track.dominantFamily]}60`
                                    }}
                                >
                                    <div className="w-3 h-3 bg-white rounded-full opacity-80" />
                                </div>

                                {/* Tooltip */}
                                <div className="absolute -top-12 left-1/2 -translate-x-1/2 w-32 bg-black/90 text-white text-[10px] p-2 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-30 border border-white/10">
                                    <p className="font-bold truncate">{track.name}</p>
                                    <p className="text-white/50">{track.dominantFamily}</p>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
};
