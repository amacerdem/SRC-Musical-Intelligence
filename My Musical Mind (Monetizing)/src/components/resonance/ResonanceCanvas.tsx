/* ── ResonanceCanvas — R3F Canvas + post-processing ─────────────── */

import { Suspense, useEffect, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { EffectComposer, Bloom, ChromaticAberration, Noise } from "@react-three/postprocessing";
import { BlendFunction } from "postprocessing";
import * as THREE from "three";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { ResonanceEnvironment } from "./ResonanceEnvironment";
import { UserOrganism } from "./UserOrganism";
import { ResonanceTendril } from "./ResonanceTendril";
import { FieldParticles } from "./FieldParticles";
import { CameraRig } from "./CameraRig";

/* ── Tick driver — runs inside R3F ──────────────────────────────── */

function SimulationTick() {
  const tick = useResonanceStore(s => s.tick);
  useFrame((_, delta) => {
    // Cap delta to avoid huge jumps on tab-switch
    tick(Math.min(delta, 0.1));
  });
  return null;
}

/* ── Scene content ──────────────────────────────────────────────── */

function SceneContent() {
  const users = useResonanceStore(s => s.users);
  const connections = useResonanceStore(s => s.connections);
  const selectedUserId = useResonanceStore(s => s.selectedUserId);

  return (
    <>
      <SimulationTick />
      <CameraRig />
      <ResonanceEnvironment />

      {/* User organisms */}
      {users.map(user => (
        <UserOrganism key={user.id} user={user} isSelected={user.id === selectedUserId} />
      ))}

      {/* Connections */}
      {connections.map(conn => (
        <ResonanceTendril key={conn.id} connection={conn} />
      ))}

      {/* Global particles */}
      <FieldParticles />

      {/* Post-processing */}
      <EffectComposer multisampling={0}>
        <Bloom
          luminanceThreshold={0.15}
          luminanceSmoothing={0.9}
          intensity={1.6}
          mipmapBlur
        />
        <ChromaticAberration
          offset={new THREE.Vector2(0.0012, 0.0012)}
          blendFunction={BlendFunction.NORMAL}
          radialModulation={false}
          modulationOffset={0}
        />
        <Noise
          premultiply
          blendFunction={BlendFunction.SOFT_LIGHT}
          opacity={0.025}
        />
      </EffectComposer>
    </>
  );
}

/* ── Canvas wrapper ─────────────────────────────────────────────── */

export function ResonanceCanvas() {
  return (
    <Canvas
      camera={{ position: [0, 6, 18], fov: 55, near: 0.1, far: 200 }}
      dpr={[1, 1.5]}
      gl={{
        antialias: true,
        alpha: false,
        powerPreference: "high-performance",
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 1.2,
      }}
      style={{ position: "absolute", inset: 0, background: "#000" }}
    >
      <fog attach="fog" args={["#000000", 25, 90]} />
      <ambientLight intensity={0.08} />
      <Suspense fallback={null}>
        <SceneContent />
      </Suspense>
    </Canvas>
  );
}
