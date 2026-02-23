/* ── Reward Aurora — Background hemisphere driven by reward trace ── */

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import type { AnalysisData } from "../hooks/useAnalysisData";
import { getFrameInterp, sampleTrace } from "../hooks/useAudioSync";

const vertexShader = `
varying vec3 vPosition;
varying vec3 vNormal;
void main() {
  vPosition = position;
  vNormal = normal;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const fragmentShader = `
uniform float uReward;
uniform float uTime;
varying vec3 vPosition;
varying vec3 vNormal;

void main() {
  vec3 posColor = vec3(0.984, 0.749, 0.141);  // #FBBF24
  vec3 negColor = vec3(0.30, 0.10, 0.15);
  vec3 neutralColor = vec3(0.02, 0.02, 0.04);

  float r = uReward;
  vec3 col = mix(negColor, posColor, smoothstep(-0.1, 0.2, r));
  col = mix(neutralColor, col, smoothstep(0.0, 0.05, abs(r)));

  // Aurora shimmer based on position + time
  float shimmer = sin(vPosition.y * 3.0 + uTime * 0.5) * 0.5 + 0.5;
  shimmer *= sin(vPosition.x * 2.0 + uTime * 0.3) * 0.5 + 0.5;

  float intensity = abs(r) * 1.5 * (0.6 + shimmer * 0.4);
  float fade = smoothstep(-0.3, 0.8, vPosition.y / 20.0);

  gl_FragColor = vec4(col * intensity * fade, intensity * fade * 0.3);
}
`;

interface Props {
  data: AnalysisData;
  currentTime: number;
  duration: number;
  tracePoints: number;
}

export function RewardAurora({ data, currentTime, duration, tracePoints }: Props) {
  const matRef = useRef<THREE.ShaderMaterial>(null);

  const uniforms = useMemo(() => ({
    uReward: { value: 0 },
    uTime: { value: 0 },
  }), []);

  useFrame((_, delta) => {
    if (!matRef.current) return;
    const { index, frac, nextIndex } = getFrameInterp(currentTime, duration, tracePoints);
    const reward = sampleTrace(data.beliefs.reward, index, frac, nextIndex);
    matRef.current.uniforms.uReward.value = reward;
    matRef.current.uniforms.uTime.value += delta;
  });

  return (
    <mesh>
      <sphereGeometry args={[22, 32, 16]} />
      <shaderMaterial
        ref={matRef}
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
        side={THREE.BackSide}
        transparent
        depthWrite={false}
      />
    </mesh>
  );
}
