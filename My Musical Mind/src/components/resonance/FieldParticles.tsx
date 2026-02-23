/* ── FieldParticles — Drifting dimension-colored particles ─────────── */

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { DIMENSIONS } from "@/data/resonance-simulation";

/* ── Pre-compute neg/pos RGB per dimension ──────────────────────── */

const DIM_NEG_RGB: [number, number, number][] = DIMENSIONS.map(d => {
  const c = new THREE.Color(d.negColor);
  return [c.r, c.g, c.b];
});

const DIM_POS_RGB: [number, number, number][] = DIMENSIONS.map(d => {
  const c = new THREE.Color(d.posColor);
  return [c.r, c.g, c.b];
});

const COUNT = 3000;

export function FieldParticles() {
  const pointsRef = useRef<THREE.Points>(null);
  const users = useResonanceStore(s => s.users);

  const [positions, colors, lifetimes, velocities] = useMemo(() => {
    const pos = new Float32Array(COUNT * 3);
    const col = new Float32Array(COUNT * 3);
    const life = new Float32Array(COUNT);
    const vel = new Float32Array(COUNT * 3);

    for (let i = 0; i < COUNT; i++) {
      // Random position in field volume
      const r = 3 + Math.random() * 28;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = (r * Math.cos(phi)) * 0.4;
      pos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);

      // Random dimension color (pick random dim, random polarity)
      const dimIdx = Math.floor(Math.random() * 5);
      const usePos = Math.random() > 0.5;
      const bc = usePos ? DIM_POS_RGB[dimIdx] : DIM_NEG_RGB[dimIdx];
      col[i * 3] = bc[0];
      col[i * 3 + 1] = bc[1];
      col[i * 3 + 2] = bc[2];

      // Random lifetime offset
      life[i] = Math.random() * 8;

      // Random velocity
      vel[i * 3] = (Math.random() - 0.5) * 0.3;
      vel[i * 3 + 1] = (Math.random() - 0.5) * 0.15;
      vel[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
    }

    return [pos, col, life, vel];
  }, []);

  useFrame((_, delta) => {
    if (!pointsRef.current) return;
    const geo = pointsRef.current.geometry;
    const posAttr = geo.attributes.position;
    const posArr = posAttr.array as Float32Array;

    for (let i = 0; i < COUNT; i++) {
      // Advance lifetime
      lifetimes[i] += delta;

      // Move
      posArr[i * 3] += velocities[i * 3] * delta;
      posArr[i * 3 + 1] += velocities[i * 3 + 1] * delta;
      posArr[i * 3 + 2] += velocities[i * 3 + 2] * delta;

      // Gentle attraction toward nearest user organism
      if (users.length > 0 && i % 4 === 0) {
        let nearDist = 999;
        let nearIdx = 0;
        const px = posArr[i * 3], py = posArr[i * 3 + 1], pz = posArr[i * 3 + 2];
        for (let u = 0; u < users.length; u++) {
          const dx = users[u].position[0] - px;
          const dy = users[u].position[1] - py;
          const dz = users[u].position[2] - pz;
          const d = dx * dx + dy * dy + dz * dz;
          if (d < nearDist) { nearDist = d; nearIdx = u; }
        }
        if (nearDist < 25) {
          const up = users[nearIdx].position;
          velocities[i * 3] += (up[0] - px) * 0.002;
          velocities[i * 3 + 1] += (up[1] - py) * 0.001;
          velocities[i * 3 + 2] += (up[2] - pz) * 0.002;

          // Color toward organism's dominant dimension polarity
          const psi = users[nearIdx].psi;
          let maxAbs = 0, maxDim = 0;
          for (let d = 0; d < 5; d++) {
            const a = Math.abs(psi[d]);
            if (a > maxAbs) { maxAbs = a; maxDim = d; }
          }
          const bc = psi[maxDim] >= 0 ? DIM_POS_RGB[maxDim] : DIM_NEG_RGB[maxDim];
          colors[i * 3] += (bc[0] - colors[i * 3]) * 0.01;
          colors[i * 3 + 1] += (bc[1] - colors[i * 3 + 1]) * 0.01;
          colors[i * 3 + 2] += (bc[2] - colors[i * 3 + 2]) * 0.01;
        }
      }

      // Damping
      velocities[i * 3] *= 0.998;
      velocities[i * 3 + 1] *= 0.998;
      velocities[i * 3 + 2] *= 0.998;

      // Respawn if too far or too old
      const d = Math.sqrt(posArr[i * 3] ** 2 + posArr[i * 3 + 1] ** 2 + posArr[i * 3 + 2] ** 2);
      if (d > 35 || lifetimes[i] > 8 + Math.random() * 4) {
        lifetimes[i] = 0;
        const r = 2 + Math.random() * 18;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        posArr[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        posArr[i * 3 + 1] = (r * Math.cos(phi)) * 0.35;
        posArr[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
        velocities[i * 3] = (Math.random() - 0.5) * 0.3;
        velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.15;
        velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
      }
    }

    posAttr.needsUpdate = true;
    geo.attributes.color.needsUpdate = true;
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
        <bufferAttribute attach="attributes-color" args={[colors, 3]} />
      </bufferGeometry>
      <pointsMaterial
        size={0.06}
        vertexColors
        transparent
        opacity={0.5}
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}
