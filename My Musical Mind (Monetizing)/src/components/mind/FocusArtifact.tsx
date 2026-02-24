import React from "react";
import { motion } from "framer-motion";
import { FocusArtifact } from "@/types/mind";

interface FocusArtifactProps {
    artifact: FocusArtifact;
    size?: "sm" | "md" | "lg";
    isLocked?: boolean;
}

const FAMILY_COLORS = {
    Architects: "cyan",
    Alchemists: "purple",
    Explorers: "magenta",
    Anchors: "amber",
    Kineticists: "red",
};

export const FocusArtifactView: React.FC<FocusArtifactProps> = ({ artifact, size = "md", isLocked }) => {
    const sizeClass = size === "sm" ? "w-16 h-16" : size === "md" ? "w-32 h-32" : "w-64 h-64";
    const glowColor = FAMILY_COLORS[artifact.family] || "white";

    return (
        <motion.div
            className={`relative ${sizeClass} flex items-center justify-center`}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.05 }}
        >
            {/* Halo Effect */}
            <motion.div
                className={`absolute inset-0 rounded-full blur-xl opacity-40 bg-${glowColor}-500`}
                animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.3, 0.6, 0.3],
                }}
                transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
            />

            {/* Artifact Container */}
            <div className={`relative z-10 w-full h-full rounded-xl overflow-hidden border border-${glowColor}-400/30 bg-black/40 backdrop-blur-md shadow-2xl`}>
                {/* Mock 3D Object (Image) */}
                <motion.img
                    src={artifact.visualAssetUrl}
                    alt={artifact.name}
                    className={`w-full h-full object-cover ${isLocked ? "grayscale blur-sm opacity-50" : ""}`}
                    animate={{
                        y: [0, -5, 0],
                        rotate: [0, 2, -2, 0],
                    }}
                    transition={{
                        duration: 6,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                />

                {/* Holo Overlay */}
                {!isLocked && (
                    <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/10 to-transparent opacity-30 pointer-events-none mix-blend-overlay" />
                )}
            </div>

            {/* Label (if huge) */}
            {size === "lg" && (
                <div className="absolute -bottom-12 text-center w-full">
                    <h3 className="text-xl font-bold tracking-widest text-white uppercase">{artifact.name}</h3>
                    <p className="text-xs text-white/50">{artifact.rarity} Relic</p>
                </div>
            )}
        </motion.div>
    );
};
