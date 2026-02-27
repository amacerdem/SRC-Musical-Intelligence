/* ── ResonanceEnvironment — Nebula backdrop + ambient particles ── */

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

/* ── Nebula backdrop sphere ─────────────────────────────────────── */

const nebulaVertex = `
varying vec3 vPos;
varying vec3 vNorm;
void main() {
  vPos = position;
  vNorm = normal;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const nebulaFragment = `
uniform float uTime;
varying vec3 vPos;
varying vec3 vNorm;

// Simple 3D noise
vec3 hash3(vec3 p) {
  p = vec3(dot(p, vec3(127.1, 311.7, 74.7)),
           dot(p, vec3(269.5, 183.3, 246.1)),
           dot(p, vec3(113.5, 271.9, 124.6)));
  return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
}

float noise3d(vec3 p) {
  vec3 i = floor(p);
  vec3 f = fract(p);
  vec3 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(dot(hash3(i + vec3(0,0,0)), f - vec3(0,0,0)),
                     dot(hash3(i + vec3(1,0,0)), f - vec3(1,0,0)), u.x),
                 mix(dot(hash3(i + vec3(0,1,0)), f - vec3(0,1,0)),
                     dot(hash3(i + vec3(1,1,0)), f - vec3(1,1,0)), u.x), u.y),
             mix(mix(dot(hash3(i + vec3(0,0,1)), f - vec3(0,0,1)),
                     dot(hash3(i + vec3(1,0,1)), f - vec3(1,0,1)), u.x),
                 mix(dot(hash3(i + vec3(0,1,1)), f - vec3(0,1,1)),
                     dot(hash3(i + vec3(1,1,1)), f - vec3(1,1,1)), u.x), u.y), u.z);
}

void main() {
  vec3 dir = normalize(vPos);

  // Base nebula colors
  vec3 deep = vec3(0.01, 0.005, 0.03);      // near black purple
  vec3 nebula1 = vec3(0.04, 0.01, 0.08);    // dark purple
  vec3 nebula2 = vec3(0.01, 0.02, 0.06);    // dark blue
  vec3 nebula3 = vec3(0.06, 0.01, 0.04);    // dark magenta

  float n1 = noise3d(dir * 2.0 + uTime * 0.015) * 0.5 + 0.5;
  float n2 = noise3d(dir * 3.5 - uTime * 0.01 + 100.0) * 0.5 + 0.5;
  float n3 = noise3d(dir * 1.5 + uTime * 0.008 + 200.0) * 0.5 + 0.5;

  vec3 col = deep;
  col = mix(col, nebula1, smoothstep(0.3, 0.7, n1) * 0.6);
  col = mix(col, nebula2, smoothstep(0.4, 0.8, n2) * 0.4);
  col = mix(col, nebula3, smoothstep(0.5, 0.9, n3) * 0.3);

  // Subtle star sparkle
  float star = pow(max(noise3d(dir * 60.0), 0.0), 20.0) * 0.8;
  col += vec3(star);

  // Fade toward horizon
  float horizon = smoothstep(-0.3, 0.5, dir.y);
  col *= 0.4 + horizon * 0.6;

  gl_FragColor = vec4(col, 1.0);
}
`;

function NebulaSphere() {
  const matRef = useRef<THREE.ShaderMaterial>(null);

  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
  }), []);

  useFrame((_, delta) => {
    if (matRef.current) {
      matRef.current.uniforms.uTime.value += delta;
    }
  });

  return (
    <mesh>
      <sphereGeometry args={[80, 32, 24]} />
      <shaderMaterial
        ref={matRef}
        vertexShader={nebulaVertex}
        fragmentShader={nebulaFragment}
        uniforms={uniforms}
        side={THREE.BackSide}
        depthWrite={false}
      />
    </mesh>
  );
}

/* ── Ambient drifting particles ─────────────────────────────────── */

function AmbientParticles() {
  const count = 2000;
  const meshRef = useRef<THREE.Points>(null);

  const [positions, velocities] = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const vel = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = 5 + Math.random() * 50;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.cos(phi) * 0.5;
      pos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
      vel[i * 3] = (Math.random() - 0.5) * 0.02;
      vel[i * 3 + 1] = (Math.random() - 0.5) * 0.01;
      vel[i * 3 + 2] = (Math.random() - 0.5) * 0.02;
    }
    return [pos, vel];
  }, []);

  const sizes = useMemo(() => {
    const s = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      s[i] = 0.02 + Math.random() * 0.06;
    }
    return s;
  }, []);

  useFrame((_, delta) => {
    if (!meshRef.current) return;
    const pos = meshRef.current.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < count; i++) {
      pos[i * 3] += velocities[i * 3] * delta * 10;
      pos[i * 3 + 1] += velocities[i * 3 + 1] * delta * 10;
      pos[i * 3 + 2] += velocities[i * 3 + 2] * delta * 10;

      // Soft respawn if too far
      const d = Math.sqrt(pos[i * 3] ** 2 + pos[i * 3 + 1] ** 2 + pos[i * 3 + 2] ** 2);
      if (d > 55) {
        const r = 5 + Math.random() * 15;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        pos[i * 3 + 1] = r * Math.cos(phi) * 0.4;
        pos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
      }
    }
    meshRef.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
        <bufferAttribute attach="attributes-size" args={[sizes, 1]} />
      </bufferGeometry>
      <pointsMaterial
        size={0.08}
        color="#8888cc"
        transparent
        opacity={0.35}
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

/* ── Ground reference rings ─────────────────────────────────────── */

function GroundRings() {
  const rings = [8, 14, 22];
  return (
    <group position={[0, -4, 0]} rotation={[-Math.PI / 2, 0, 0]}>
      {rings.map(r => (
        <mesh key={r}>
          <ringGeometry args={[r - 0.02, r + 0.02, 64]} />
          <meshBasicMaterial
            color="#4444aa"
            transparent
            opacity={0.04}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      ))}
    </group>
  );
}

/* ── Exported environment ───────────────────────────────────────── */

export function ResonanceEnvironment() {
  return (
    <>
      <NebulaSphere />
      <AmbientParticles />
      <GroundRings />
    </>
  );
}
