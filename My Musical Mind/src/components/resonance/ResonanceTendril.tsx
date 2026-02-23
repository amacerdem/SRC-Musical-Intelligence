/* ── ResonanceTendril — Glowing connection between resonant users ── */

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { useResonanceStore } from "@/stores/useResonanceStore";
import type { Connection } from "@/data/resonance-simulation";

/* ── Belief colors ──────────────────────────────────────────────── */

const BELIEF_COLORS = [
  new THREE.Color("#C084FC"), // consonance
  new THREE.Color("#F97316"), // tempo
  new THREE.Color("#84CC16"), // salience
  new THREE.Color("#38BDF8"), // familiarity
  new THREE.Color("#FBBF24"), // reward
];

/* ── Tendril shader ─────────────────────────────────────────────── */

const tendrilVertex = `
uniform float uTime;
uniform float uStrength;

attribute float aProgress;
varying float vProgress;
varying float vRadial;

void main() {
  vProgress = aProgress;
  vec3 pos = position;

  // Subtle wave displacement
  float wave = sin(aProgress * 6.283 + uTime * 2.0) * 0.03 * uStrength;
  pos += normal * wave;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
`;

const tendrilFragment = `
uniform float uTime;
uniform float uStrength;
uniform vec3 uColor;

varying float vProgress;

void main() {
  // Flowing pulse effect
  float flow = sin(vProgress * 12.566 - uTime * 3.0) * 0.5 + 0.5;
  flow = pow(flow, 3.0); // Sharpen peaks

  // Base glow
  float base = 0.15 * uStrength;
  float pulse = flow * 0.6 * uStrength;

  float alpha = base + pulse;

  // Fade at endpoints
  float endFade = smoothstep(0.0, 0.1, vProgress) * smoothstep(1.0, 0.9, vProgress);
  alpha *= endFade;

  gl_FragColor = vec4(uColor * (1.0 + pulse * 0.5), alpha);
}
`;

/* ── Component ──────────────────────────────────────────────────── */

interface Props {
  connection: Connection;
}

export function ResonanceTendril({ connection }: Props) {
  const meshRef = useRef<THREE.Mesh>(null);
  const matRef = useRef<THREE.ShaderMaterial>(null);
  const users = useResonanceStore(s => s.users);

  const color = useMemo(
    () => BELIEF_COLORS[connection.dominantBelief] ?? BELIEF_COLORS[0],
    [connection.dominantBelief],
  );

  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
    uStrength: { value: connection.strength },
    uColor: { value: color },
  }), []);

  // Pre-allocate curve objects
  const curve = useMemo(() => new THREE.CatmullRomCurve3([
    new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3(),
  ]), []);

  useFrame((_, delta) => {
    if (!meshRef.current || !matRef.current) return;

    const u = matRef.current.uniforms;
    u.uTime.value += delta;
    u.uStrength.value += (connection.strength - u.uStrength.value) * 0.1;
    u.uColor.value = BELIEF_COLORS[connection.dominantBelief] ?? BELIEF_COLORS[0];

    // Get user positions
    const userA = connection.userA === "self" ? null : users.find(u => u.id === connection.userA);
    const userB = connection.userB === "self" ? null : users.find(u => u.id === connection.userB);

    const posA = userA ? userA.position : [0, 0, 0];
    const posB = userB ? userB.position : [0, 0, 0];

    // Update curve control points
    const midX = (posA[0] + posB[0]) * 0.5;
    const midY = (posA[1] + posB[1]) * 0.5 + 1.0; // Arc upward
    const midZ = (posA[2] + posB[2]) * 0.5;

    curve.points[0].set(posA[0], posA[1], posA[2]);
    curve.points[1].set(midX, midY, midZ);
    curve.points[2].set(posB[0], posB[1], posB[2]);
    curve.updateArcLengths();

    // Rebuild geometry (lightweight for thin tubes)
    const tubeGeo = new THREE.TubeGeometry(
      curve,
      20,                                  // tubularSegments
      0.01 + connection.strength * 0.03,   // radius
      6,                                   // radialSegments
      false,
    );

    // Add progress attribute for flow animation
    const count = tubeGeo.attributes.position.count;
    const progressArr = new Float32Array(count);
    const posArr = tubeGeo.attributes.position.array;
    for (let i = 0; i < count; i++) {
      const p = new THREE.Vector3(posArr[i * 3], posArr[i * 3 + 1], posArr[i * 3 + 2]);
      // Approximate progress along curve
      const tA = curve.points[0];
      const tB = curve.points[2];
      const total = tA.distanceTo(tB) + 0.001;
      progressArr[i] = p.distanceTo(tA) / total;
    }
    tubeGeo.setAttribute("aProgress", new THREE.BufferAttribute(progressArr, 1));

    // Swap geometry
    if (meshRef.current.geometry) meshRef.current.geometry.dispose();
    meshRef.current.geometry = tubeGeo;
  });

  return (
    <mesh ref={meshRef}>
      <bufferGeometry />
      <shaderMaterial
        ref={matRef}
        vertexShader={tendrilVertex}
        fragmentShader={tendrilFragment}
        uniforms={uniforms}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}
