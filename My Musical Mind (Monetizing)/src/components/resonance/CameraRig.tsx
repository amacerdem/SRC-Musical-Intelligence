/* ── CameraRig — Smooth follow + orbit controls ─────────────────── */

import { useRef, useEffect } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { useResonanceStore } from "@/stores/useResonanceStore";

export function CameraRig() {
  const controlsRef = useRef<any>(null);
  const cameraMode = useResonanceStore(s => s.cameraMode);
  const selectedUserId = useResonanceStore(s => s.selectedUserId);
  const users = useResonanceStore(s => s.users);
  const targetLookAt = useRef(new THREE.Vector3(0, 0, 0));
  const targetPosition = useRef(new THREE.Vector3(0, 6, 18));
  const autoRotateAngle = useRef(0);

  useFrame((state, delta) => {
    if (!controlsRef.current) return;
    const controls = controlsRef.current;

    if (cameraMode === "self") {
      // Gentle auto-rotation around origin
      autoRotateAngle.current += delta * 0.08;
      const r = 18;
      const y = 6;
      targetPosition.current.set(
        Math.sin(autoRotateAngle.current) * r,
        y + Math.sin(autoRotateAngle.current * 0.3) * 1.5,
        Math.cos(autoRotateAngle.current) * r,
      );
      targetLookAt.current.set(0, 0, 0);

      // Smooth camera movement
      state.camera.position.lerp(targetPosition.current, 0.02);
      controls.target.lerp(targetLookAt.current, 0.02);

    } else if (cameraMode === "selected" && selectedUserId) {
      const user = users.find(u => u.id === selectedUserId);
      if (user) {
        const [ux, uy, uz] = user.position;
        targetLookAt.current.set(ux, uy, uz);

        // Position camera between origin and selected user, offset up and back
        const midX = ux * 0.6;
        const midZ = uz * 0.6;
        const dist = Math.sqrt(ux * ux + uz * uz);
        const offsetDist = Math.max(dist * 0.8, 8);
        const angle = Math.atan2(ux, uz);
        targetPosition.current.set(
          midX + Math.sin(angle + 0.4) * offsetDist * 0.3,
          uy + 4,
          midZ + Math.cos(angle + 0.4) * offsetDist * 0.3,
        );

        state.camera.position.lerp(targetPosition.current, 0.03);
        controls.target.lerp(targetLookAt.current, 0.03);
      }
    }
    // "free" mode: orbit controls handle it

    controls.update();
  });

  return (
    <OrbitControls
      ref={controlsRef}
      enableDamping
      dampingFactor={0.08}
      minDistance={3}
      maxDistance={50}
      maxPolarAngle={Math.PI * 0.8}
      minPolarAngle={Math.PI * 0.1}
      enablePan={cameraMode === "free"}
      enableZoom
      enableRotate={cameraMode === "free"}
      makeDefault
    />
  );
}
