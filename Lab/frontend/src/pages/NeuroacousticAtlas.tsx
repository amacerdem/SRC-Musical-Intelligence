import { useRef, useEffect, useCallback, useState } from 'react';
import { colors } from '../design/tokens';

// ══════════════════════════════════════════════════════════════════════
//  NEUROACOUSTIC ATLAS — Interactive System Architecture Diagram
//  Full data-flow visualization: Audio → R³ → H³ → C³ → Reward
// ══════════════════════════════════════════════════════════════════════

// ── Node Types ──

interface AtlasNode {
  id: string;
  label: string;
  sublabel?: string;
  x: number;
  y: number;
  w: number;
  h: number;
  color: string;
  category: 'source' | 'r3' | 'h3' | 'relay' | 'belief' | 'ram' | 'output' | 'meta';
  detail?: string;
  dims?: string;
}

interface AtlasEdge {
  from: string;
  to: string;
  color: string;
  label?: string;
  dashed?: boolean;
  width?: number;
}

interface Particle {
  edge: number;   // edge index
  t: number;      // 0..1 position along edge
  speed: number;
}

// ── Layout Constants ──
const W = 2200;
const H = 1400;

// Column X positions
const COL_SRC   = 80;
const COL_R3    = 320;
const COL_H3    = 620;
const COL_RELAY = 940;
const COL_BELIEF = 1260;
const COL_OUT   = 1580;
const COL_RAM   = 1850;

// ── Nodes ──

const NODES: AtlasNode[] = [
  // Source
  { id: 'audio', label: 'Audio', sublabel: 'WAV · 44.1kHz', x: COL_SRC, y: 200, w: 140, h: 50, color: '#ffffff', category: 'source', detail: 'Raw audio waveform input', dims: '(1, N)' },
  { id: 'stft', label: 'STFT', sublabel: 'Phase-preserve', x: COL_SRC, y: 310, w: 140, h: 50, color: '#94a3b8', category: 'source', detail: 'Short-Time Fourier Transform\nn_fft=2048, hop=256', dims: '(1, 1025, T)' },
  { id: 'mel', label: 'Mel Spec', sublabel: '128 bands · log1p', x: COL_SRC, y: 420, w: 140, h: 50, color: '#64748b', category: 'source', detail: 'Log-mel spectrogram\nsr=44100, hop=256, n_mels=128\nFrame rate: 172.27 Hz', dims: '(1, 128, T)' },

  // R³ Groups (9)
  { id: 'r3_A', label: 'A', sublabel: 'Consonance', x: COL_R3, y: 80,  w: 180, h: 42, color: '#60a5fa', category: 'r3', detail: 'Sethares roughness, Plomp-Levelt\nHelmholtz, Stumpf fusion\nSensory pleasantness', dims: '7D [0:7]' },
  { id: 'r3_B', label: 'B', sublabel: 'Energy', x: COL_R3, y: 135, w: 180, h: 42, color: '#f97316', category: 'r3', detail: 'RMS amplitude, loudness\nOnset strength, velocity', dims: '5D [7:12]' },
  { id: 'r3_C', label: 'C', sublabel: 'Timbre', x: COL_R3, y: 190, w: 180, h: 42, color: '#14b8a6', category: 'r3', detail: 'Warmth, sharpness, tonalness\nClarity, spectral smoothness\nTristimulus 1/2/3', dims: '9D [12:21]' },
  { id: 'r3_D', label: 'D', sublabel: 'Change', x: COL_R3, y: 245, w: 180, h: 42, color: '#eab308', category: 'r3', detail: 'Spectral flux\nDistribution entropy/flatness\nConcentration', dims: '4D [21:25]' },
  { id: 'r3_F', label: 'F', sublabel: 'Pitch / Chroma', x: COL_R3, y: 300, w: 180, h: 42, color: '#22c55e', category: 'r3', detail: '12-bin chroma (C→B)\nPitch height, class entropy\nPitch salience, inharmonicity', dims: '16D [25:41]' },
  { id: 'r3_G', label: 'G', sublabel: 'Rhythm', x: COL_R3, y: 355, w: 180, h: 42, color: '#ef4444', category: 'r3', detail: 'Tempo estimate, beat strength\nPulse clarity, syncopation\nGroove, event density', dims: '10D [41:51]' },
  { id: 'r3_H', label: 'H', sublabel: 'Harmony', x: COL_R3, y: 410, w: 180, h: 42, color: '#a78bfa', category: 'r3', detail: 'Key clarity, Tonnetz 5th/minor/major\nVoice leading, harmonic change\nTonal stability, diatonicity', dims: '12D [51:63]' },
  { id: 'r3_J', label: 'J', sublabel: 'Timbre Ext', x: COL_R3, y: 465, w: 180, h: 42, color: '#6366f1', category: 'r3', detail: 'MFCC 1-13\nSpectral contrast 1-7', dims: '20D [63:83]' },
  { id: 'r3_K', label: 'K', sublabel: 'Modulation', x: COL_R3, y: 520, w: 180, h: 42, color: '#ec4899', category: 'r3', detail: 'Modulation spectrum (0.5-16Hz)\nSharpness Zwicker\nFluctuation strength, alpha ratio', dims: '14D [83:97]' },

  // R³ output
  { id: 'r3_out', label: 'R³ Output', sublabel: '97D · [0,1] · Frozen', x: COL_R3, y: 610, w: 180, h: 50, color: colors.r3, category: 'r3', detail: 'Deterministic per-frame\nNo EMA/state, no cross-domain\n±2 frame context only', dims: '(B, T, 97)' },

  // H³ Engine
  { id: 'h3_engine', label: 'H³ Engine', sublabel: 'Temporal Morphology', x: COL_H3, y: 100, w: 200, h: 60, color: colors.h3, category: 'h3', detail: 'Demand-driven computation\nOnly requested 4-tuples computed\n97 × 32 × 24 × 3 = 223,488 theoretical', dims: 'Sparse dict' },
  { id: 'h3_micro', label: 'Micro', sublabel: 'H0-H7 · 5.8ms-250ms', x: COL_H3, y: 200, w: 200, h: 38, color: '#60a5fa', category: 'h3', detail: 'Sensory/sub-beat scale\nOnset, attack transients\n8 horizons', dims: 'H0-H7' },
  { id: 'h3_meso', label: 'Meso', sublabel: 'H8-H15 · 300ms-800ms', x: COL_H3, y: 252, w: 200, h: 38, color: '#a78bfa', category: 'h3', detail: 'Beat/phrase scale\nTempo, rhythmic patterns\n8 horizons', dims: 'H8-H15' },
  { id: 'h3_macro', label: 'Macro', sublabel: 'H16-H23 · 1s-25s', x: COL_H3, y: 304, w: 200, h: 38, color: '#f59e0b', category: 'h3', detail: 'Section/passage scale\nHarmonic progressions\n8 horizons', dims: 'H16-H23' },
  { id: 'h3_ultra', label: 'Ultra', sublabel: 'H24-H31 · 36s-981s', x: COL_H3, y: 356, w: 200, h: 38, color: '#ef4444', category: 'h3', detail: 'Movement/work scale\nLarge-scale form\n8 horizons', dims: 'H24-H31' },

  // Morphology types
  { id: 'h3_morph', label: '24 Morphologies', sublabel: 'M0-M23', x: COL_H3, y: 430, w: 200, h: 50, color: colors.h3 + 'cc', category: 'h3', detail: 'Level: value, mean, median, max\nDispersion: std, range, stability\nDynamics: velocity, acceleration, trend\nRhythm: periodicity, peaks\nInfo: entropy', dims: '24 types' },
  { id: 'h3_laws', label: '3 Laws', sublabel: 'L0 L1 L2', x: COL_H3, y: 510, w: 200, h: 50, color: colors.h3 + 'aa', category: 'h3', detail: 'L0 Memory: backward exp decay\nL1 Prediction: forward projection\nL2 Integration: bidirectional\nKernel: exp(-3|dt|/H)', dims: '3 perspectives' },

  // H³ output
  { id: 'h3_out', label: 'H³ Output', sublabel: '131 demanded tuples', x: COL_H3, y: 610, w: 200, h: 50, color: colors.h3, category: 'h3', detail: '4-tuple: (r3_idx, horizon, morph, law)\nAll L0-only for C³ kernel v4.0\nDemand-driven sparse computation', dims: '{tuple: (B,T)}' },

  // 9 Relays (Depth 0)
  { id: 'bch', label: 'BCH', sublabel: 'SPU · Consonance', x: COL_RELAY, y: 60,  w: 200, h: 42, color: '#60a5fa', category: 'relay', detail: 'Brainstem Consonance Hierarchy\nE4+M4+P4+F4 = 16D\n17 H³ L0 tuples\nhierarchy · consonance_signal · template_match', dims: '16D' },
  { id: 'hmce', label: 'HMCE', sublabel: 'STU · Context', x: COL_RELAY, y: 115, w: 200, h: 42, color: '#a78bfa', category: 'relay', detail: 'Hierarchical Musical Context Encoding\nE5+M2+P3+F3 = 18D (largest relay)\n18 H³ L0 tuples\na1/stg/mtg encoding · structure predict', dims: '18D' },
  { id: 'snem', label: 'SNEM', sublabel: 'ASU · Attention', x: COL_RELAY, y: 170, w: 200, h: 42, color: '#f97316', category: 'relay', detail: 'Sensory Novelty Expectation Model\nE3+M3+P3+F3 = 12D\n3 H³ L0 (degraded)\nbeat_locked · entrainment · selective_gain', dims: '12D' },
  { id: 'meamn', label: 'MEAMN', sublabel: 'IMU · Memory', x: COL_RELAY, y: 225, w: 200, h: 42, color: '#14b8a6', category: 'relay', detail: 'Music-Evoked Autobiographical Memory\nE3+M2+P3+F4 = 12D\n11 H³ L0 tuples\nmemory_state · emotional_color · nostalgia', dims: '12D' },
  { id: 'daed', label: 'DAED', sublabel: 'RPU · Reward', x: COL_RELAY, y: 280, w: 200, h: 42, color: '#eab308', category: 'relay', detail: 'Dopamine Anticipation-Experience Dissociation\nE4+M2+P2+F0 = 8D\n5 H³ L0, cross-relay (BCH+MEAMN)\nwanting/liking · caudate/nacc', dims: '8D' },
  { id: 'mpg', label: 'MPG', sublabel: 'NDU · Melodic', x: COL_RELAY, y: 335, w: 200, h: 42, color: '#22c55e', category: 'relay', detail: 'Melodic Pitch Gradient\nE4+M3+P2+F1 = 10D\n2 H³ L0 (degraded)\nonset · contour · phrase_boundary', dims: '10D' },
  { id: 'srp', label: 'SRP', sublabel: 'ARU · Pleasure', x: COL_RELAY, y: 390, w: 200, h: 42, color: '#ef4444', category: 'relay', detail: 'Subjective Reward & Pleasure\n5D output\n5 H³ L0 tuples\nwanting · liking · pleasure · tension · chills', dims: '5D' },
  { id: 'peom', label: 'PEOM', sublabel: 'MPU · Motor', x: COL_RELAY, y: 445, w: 200, h: 42, color: '#ec4899', category: 'relay', detail: 'Period Entrainment Oscillation Model\n3D output\n3 H³ L0 tuples\nperiod_lock · kinematics · velocity', dims: '3D' },
  { id: 'htp', label: 'HTP', sublabel: 'PCU · Prediction', x: COL_RELAY, y: 500, w: 200, h: 42, color: '#6366f1', category: 'relay', detail: 'Hierarchical Temporal Prediction\nE4+M3+P3+F2 = 12D\n9 H³ L0 tuples\nsensory_match · pitch/abstract prediction', dims: '12D' },

  // Belief system
  { id: 'beliefs_core', label: '36 Core', sublabel: 'Full Bayesian PE', x: COL_BELIEF, y: 80, w: 200, h: 50, color: '#10b981', category: 'belief', detail: 'Predict → Observe → PE → Update\nτ-weighted prior persistence\nPrecision: tanh(π/12) compression\nRing buffer PE history per-horizon', dims: '36 beliefs' },
  { id: 'beliefs_appraisal', label: '65 Appraisal', sublabel: 'Observe-only', x: COL_BELIEF, y: 150, w: 200, h: 50, color: '#3b82f6', category: 'belief', detail: 'Evaluative judgments\nNo prediction, no update\nDirect observation from upstream', dims: '65 beliefs' },
  { id: 'beliefs_anticipation', label: '30 Anticipation', sublabel: 'Forward predictions', x: COL_BELIEF, y: 220, w: 200, h: 50, color: '#f59e0b', category: 'belief', detail: 'F-layer forecast outputs\nFeed into Core predict()\nTrend + periodicity + context', dims: '30 beliefs' },

  // Functions F1-F9
  { id: 'f1', label: 'F1', sublabel: 'Sensory · 17', x: COL_BELIEF, y: 310, w: 92, h: 35, color: '#60a5fa', category: 'belief', detail: 'Sensory Processing\n5C + 7A + 5N = 17 beliefs\nharm_stability, pitch_prominence\ninterval_quality, consonance_trajectory', dims: '17' },
  { id: 'f2', label: 'F2', sublabel: 'Predict · 15', x: COL_BELIEF + 108, y: 310, w: 92, h: 35, color: '#a78bfa', category: 'belief', detail: 'Pattern Recognition & Prediction\n4C + 6A + 5N = 15 beliefs\nprediction_hierarchy, sequence_match', dims: '15' },
  { id: 'f3', label: 'F3', sublabel: 'Attention · 15', x: COL_BELIEF, y: 358, w: 92, h: 35, color: '#f97316', category: 'belief', detail: 'Attention & Salience\n4C + 7A + 4N = 15 beliefs\nbeat_entrainment, attention_capture', dims: '15' },
  { id: 'f4', label: 'F4', sublabel: 'Memory · 13', x: COL_BELIEF + 108, y: 358, w: 92, h: 35, color: '#14b8a6', category: 'belief', detail: 'Memory Systems\n4C + 7A + 2N = 13 beliefs\nautobio_retrieval, nostalgia', dims: '13' },
  { id: 'f5', label: 'F5', sublabel: 'Emotion · 14', x: COL_BELIEF, y: 406, w: 92, h: 35, color: '#ec4899', category: 'belief', detail: 'Emotion & Valence\n4C + 8A + 2N = 14 beliefs\nperceived_happy/sad, arousal', dims: '14' },
  { id: 'f6', label: 'F6', sublabel: 'Reward · 16', x: COL_BELIEF + 108, y: 406, w: 92, h: 35, color: '#eab308', category: 'belief', detail: 'Reward & Motivation\n5C + 7A + 4N = 16 beliefs\nwanting, liking, pleasure, PE, tension', dims: '16' },
  { id: 'f7', label: 'F7', sublabel: 'Motor · 17', x: COL_BELIEF, y: 454, w: 92, h: 35, color: '#ef4444', category: 'belief', detail: 'Motor & Timing\n4C + 9A + 4N = 17 beliefs\nperiod_entrainment, groove_quality', dims: '17' },
  { id: 'f8', label: 'F8', sublabel: 'Learning · 14', x: COL_BELIEF + 108, y: 454, w: 92, h: 35, color: '#22c55e', category: 'belief', detail: 'Learning & Plasticity\n4C + 8A + 2N = 14 beliefs\ntrained_timbre, expertise', dims: '14' },
  { id: 'f9', label: 'F9', sublabel: 'Social · 10', x: COL_BELIEF, y: 502, w: 200, h: 35, color: '#6366f1', category: 'belief', detail: 'Social Cognition\n2C + 6A + 2N = 10 beliefs\nneural_synchrony, social_coordination', dims: '10' },

  // Schedulers & Engines
  { id: 'salience', label: 'Salience', sublabel: '4-signal mix', x: COL_BELIEF, y: 570, w: 96, h: 42, color: '#f97316', category: 'output', detail: 'energy(R³ 0.25) + velocity(H³ 0.25)\n+ PE carry(0.15) + relay(0.35)\nSNEM selective_gain gate\n0.5×avg + 0.5×max', dims: '(B, T)' },
  { id: 'precision', label: 'Precision', sublabel: 'π engine', x: COL_BELIEF + 110, y: 570, w: 96, h: 42, color: '#a78bfa', category: 'output', detail: 'Per-belief π_obs and π_pred\ntanh(π_raw/12) compression\nRing buffer PE history\nBayesian gain = π_obs/(π_obs+π_pred)', dims: 'T×36×2' },

  // Familiarity & Reward
  { id: 'familiarity', label: 'Familiarity', sublabel: 'Recurrence v2.4', x: COL_OUT, y: 80, w: 180, h: 45, color: '#14b8a6', category: 'output', detail: 'M14 periodicity (50%)\n+ M2 std inverted (35%)\n+ tonal (15%)\nenergy gate, baseline=0.0', dims: '(B, T)' },
  { id: 'reward', label: 'Reward', sublabel: 'R = Σ sal × w × fam × DA', x: COL_OUT, y: 150, w: 180, h: 55, color: colors.reward, category: 'output', detail: 'Σ salience ×\n  (1.5×surprise\n  + 0.8×resolution\n  + 0.5×exploration\n  − 0.6×monotony)\n× fam_mod × da_gain', dims: '(B, T)' },

  // Neuro
  { id: 'neuro', label: 'Neuro', sublabel: 'DA · NE · OPI · 5HT', x: COL_OUT, y: 240, w: 180, h: 45, color: '#ef4444', category: 'output', detail: 'Dopamine: reward, surprise\nNorepinephrine: arousal, attention\nOpioid: pleasure, analgesia\nSerotonin: mood, tonal stability', dims: '(B, T, 4)' },

  // RAM
  { id: 'ram', label: 'RAM', sublabel: 'Region Activation Map', x: COL_OUT, y: 330, w: 180, h: 50, color: colors.c3, category: 'ram', detail: 'Σ(relay_dim × link_weight)\n→ ReLU → z-norm(T>1) → sigmoid\n26 brain regions · [0,1]\nSTG is convergence hub', dims: '(B, T, 26)' },

  // Brain region groups
  { id: 'ram_cortical', label: 'Cortical', sublabel: '12 regions', x: COL_RAM, y: 80, w: 160, h: 42, color: '#10b981', category: 'ram', detail: 'A1_HG, STG, STS, IFG, AG, TP\ndlPFC, vmPFC, OFC, Insula, ACC, SMA', dims: '12' },
  { id: 'ram_subcortical', label: 'Subcortical', sublabel: '9 regions', x: COL_RAM, y: 138, w: 160, h: 42, color: '#f59e0b', category: 'ram', detail: 'VTA, NAcc, Caudate, Amygdala\nHippocampus, Putamen, MGB\nHypothalamus, Insula', dims: '9' },
  { id: 'ram_brainstem', label: 'Brainstem', sublabel: '5 regions', x: COL_RAM, y: 196, w: 160, h: 42, color: '#ef4444', category: 'ram', detail: 'IC, AN, CN, SOC, PAG\nEarliest auditory processing', dims: '5' },

  // Psi output
  { id: 'psi', label: 'Ψ³', sublabel: 'Cognitive Interpretation', x: COL_OUT, y: 430, w: 180, h: 55, color: '#8b5cf6', category: 'output', detail: 'affect: valence, arousal, tension\nemotion: joy, sadness, awe\naesthetic: beauty, groove, flow\nbodily: chills, movement_urge\ncognitive: familiarity, absorption\ntemporal: anticipation, resolution', dims: '6 domains' },

  // Phase schedule
  { id: 'phase', label: 'Phase Schedule', sublabel: '0a→0b→0c→1→2a→2b→2c→3→RAM', x: COL_H3, y: 700, w: 540, h: 45, color: 'rgba(255,255,255,0.15)', category: 'meta', detail: '0a: 7 indep relays\n0b: HMCE+DAED cross\n0c: consonance+HTP, tempo+PEOM\n1: salience+SNEM+SRP+MPG\n2a: predict/observe, fam+MEAMN\n2b: PE+precision+HTP\n2c: update\n3: reward+SRP+MEAMN\n→ RAM → output', dims: '9 phases' },
];

// ── Edges ──

const EDGES: AtlasEdge[] = [
  // Source flow
  { from: 'audio', to: 'stft', color: '#ffffff40', width: 2 },
  { from: 'stft', to: 'mel', color: '#94a3b840', width: 2 },
  { from: 'mel', to: 'r3_A', color: '#60a5fa30' },
  { from: 'mel', to: 'r3_B', color: '#f9731630' },
  { from: 'mel', to: 'r3_C', color: '#14b8a630' },
  { from: 'mel', to: 'r3_D', color: '#eab30830' },
  { from: 'mel', to: 'r3_F', color: '#22c55e30' },
  { from: 'mel', to: 'r3_G', color: '#ef444430' },
  { from: 'mel', to: 'r3_H', color: '#a78bfa30' },
  { from: 'mel', to: 'r3_J', color: '#6366f130' },
  { from: 'mel', to: 'r3_K', color: '#ec489930' },

  // R³ → R³ output
  { from: 'r3_A', to: 'r3_out', color: '#60a5fa20' },
  { from: 'r3_B', to: 'r3_out', color: '#f9731620' },
  { from: 'r3_C', to: 'r3_out', color: '#14b8a620' },
  { from: 'r3_D', to: 'r3_out', color: '#eab30820' },
  { from: 'r3_F', to: 'r3_out', color: '#22c55e20' },
  { from: 'r3_G', to: 'r3_out', color: '#ef444420' },
  { from: 'r3_H', to: 'r3_out', color: '#a78bfa20' },
  { from: 'r3_J', to: 'r3_out', color: '#6366f120' },
  { from: 'r3_K', to: 'r3_out', color: '#ec489920' },

  // R³ → H³
  { from: 'r3_out', to: 'h3_engine', color: colors.r3 + '50', width: 3, label: '97D' },

  // H³ internal
  { from: 'h3_engine', to: 'h3_micro', color: '#60a5fa30' },
  { from: 'h3_engine', to: 'h3_meso', color: '#a78bfa30' },
  { from: 'h3_engine', to: 'h3_macro', color: '#f59e0b30' },
  { from: 'h3_engine', to: 'h3_ultra', color: '#ef444430' },

  // H³ → H³ output
  { from: 'h3_micro', to: 'h3_out', color: '#60a5fa18' },
  { from: 'h3_meso', to: 'h3_out', color: '#a78bfa18' },
  { from: 'h3_macro', to: 'h3_out', color: '#f59e0b18' },
  { from: 'h3_ultra', to: 'h3_out', color: '#ef444418' },
  { from: 'h3_morph', to: 'h3_out', color: colors.h3 + '20' },
  { from: 'h3_laws', to: 'h3_out', color: colors.h3 + '20' },

  // H³ → Relays (main data flow)
  { from: 'h3_out', to: 'bch', color: colors.h3 + '40', width: 2, label: '17 tuples' },
  { from: 'h3_out', to: 'hmce', color: colors.h3 + '40', width: 2, label: '18 tuples' },
  { from: 'h3_out', to: 'snem', color: colors.h3 + '30', label: '3' },
  { from: 'h3_out', to: 'meamn', color: colors.h3 + '40', label: '11' },
  { from: 'h3_out', to: 'daed', color: colors.h3 + '30', label: '5' },
  { from: 'h3_out', to: 'mpg', color: colors.h3 + '30', label: '2' },
  { from: 'h3_out', to: 'srp', color: colors.h3 + '30', label: '5' },
  { from: 'h3_out', to: 'peom', color: colors.h3 + '30', label: '3' },
  { from: 'h3_out', to: 'htp', color: colors.h3 + '40', label: '9' },

  // R³ direct to relays
  { from: 'r3_out', to: 'bch', color: colors.r3 + '20', dashed: true },
  { from: 'r3_out', to: 'snem', color: colors.r3 + '15', dashed: true },
  { from: 'r3_out', to: 'mpg', color: colors.r3 + '15', dashed: true },

  // Cross-relay
  { from: 'bch', to: 'daed', color: '#eab30825', dashed: true, label: 'cross' },
  { from: 'meamn', to: 'daed', color: '#eab30825', dashed: true, label: 'cross' },

  // Relays → Beliefs
  { from: 'bch', to: 'beliefs_core', color: '#10b98130' },
  { from: 'hmce', to: 'beliefs_core', color: '#10b98130' },
  { from: 'snem', to: 'beliefs_core', color: '#10b98130' },
  { from: 'meamn', to: 'beliefs_core', color: '#10b98130' },
  { from: 'srp', to: 'beliefs_core', color: '#10b98130' },
  { from: 'bch', to: 'beliefs_appraisal', color: '#3b82f625' },
  { from: 'hmce', to: 'beliefs_appraisal', color: '#3b82f625' },
  { from: 'daed', to: 'beliefs_appraisal', color: '#3b82f625' },
  { from: 'htp', to: 'beliefs_anticipation', color: '#f59e0b25' },
  { from: 'peom', to: 'beliefs_anticipation', color: '#f59e0b25' },
  { from: 'mpg', to: 'beliefs_anticipation', color: '#f59e0b25' },

  // Beliefs → Functions
  { from: 'beliefs_core', to: 'f1', color: '#10b98115' },
  { from: 'beliefs_core', to: 'f6', color: '#10b98115' },
  { from: 'beliefs_appraisal', to: 'f3', color: '#3b82f615' },
  { from: 'beliefs_appraisal', to: 'f5', color: '#3b82f615' },
  { from: 'beliefs_anticipation', to: 'f2', color: '#f59e0b15' },
  { from: 'beliefs_anticipation', to: 'f7', color: '#f59e0b15' },

  // Functions → Outputs
  { from: 'f3', to: 'salience', color: '#f9731625' },
  { from: 'f6', to: 'reward', color: '#f59e0b30', width: 2 },
  { from: 'salience', to: 'reward', color: '#f59e0b40', width: 2 },
  { from: 'precision', to: 'beliefs_core', color: '#a78bfa20', dashed: true },
  { from: 'familiarity', to: 'reward', color: '#14b8a630' },

  // RAM
  { from: 'bch', to: 'ram', color: '#10b98118' },
  { from: 'hmce', to: 'ram', color: '#10b98118' },
  { from: 'snem', to: 'ram', color: '#10b98118' },
  { from: 'meamn', to: 'ram', color: '#10b98118' },
  { from: 'srp', to: 'ram', color: '#10b98118' },
  { from: 'ram', to: 'ram_cortical', color: '#10b98130' },
  { from: 'ram', to: 'ram_subcortical', color: '#f59e0b30' },
  { from: 'ram', to: 'ram_brainstem', color: '#ef444430' },

  // Neuro
  { from: 'daed', to: 'neuro', color: '#ef444420' },
  { from: 'srp', to: 'neuro', color: '#ef444420' },

  // Psi
  { from: 'reward', to: 'psi', color: '#8b5cf630' },
  { from: 'neuro', to: 'psi', color: '#8b5cf625' },
  { from: 'ram', to: 'psi', color: '#8b5cf620', dashed: true },

  // SNEM → salience expanded
  { from: 'snem', to: 'salience', color: '#f9731630' },
  { from: 'srp', to: 'salience', color: '#ef444420', label: 'tension' },
  { from: 'mpg', to: 'salience', color: '#22c55e20' },

  // Familiarity sources
  { from: 'meamn', to: 'familiarity', color: '#14b8a625' },
  { from: 'mpg', to: 'familiarity', color: '#22c55e18', dashed: true },
];

// ── Category labels ──
const SECTION_LABELS = [
  { x: COL_SRC + 70, y: 160, label: 'SOURCE', color: '#ffffff30' },
  { x: COL_R3 + 90, y: 40, label: 'R³ SPECTRAL', color: colors.r3 + '60' },
  { x: COL_H3 + 100, y: 60, label: 'H³ TEMPORAL', color: colors.h3 + '60' },
  { x: COL_RELAY + 100, y: 25, label: 'C³ RELAYS (Depth 0)', color: colors.c3 + '60' },
  { x: COL_BELIEF + 100, y: 48, label: 'C³ BELIEFS (131)', color: colors.c3 + '60' },
  { x: COL_OUT + 90, y: 48, label: 'OUTPUT', color: colors.reward + '60' },
  { x: COL_RAM + 80, y: 48, label: 'RAM REGIONS', color: colors.c3 + '60' },
];

export default function NeuroacousticAtlas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredNode, setHoveredNode] = useState<AtlasNode | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const [camera, setCamera] = useState({ x: 0, y: 0, zoom: 0.72 });
  const isDragging = useRef(false);
  const dragStart = useRef({ x: 0, y: 0, cx: 0, cy: 0 });
  const particlesRef = useRef<Particle[]>([]);
  const timeRef = useRef(0);

  // Initialize particles
  useEffect(() => {
    const particles: Particle[] = [];
    for (let i = 0; i < EDGES.length; i++) {
      const edge = EDGES[i];
      if (edge.width && edge.width >= 2) {
        // More particles on major edges
        for (let j = 0; j < 3; j++) {
          particles.push({ edge: i, t: Math.random(), speed: 0.001 + Math.random() * 0.002 });
        }
      } else if (!edge.dashed) {
        particles.push({ edge: i, t: Math.random(), speed: 0.0008 + Math.random() * 0.0015 });
      }
    }
    particlesRef.current = particles;
  }, []);

  const getNodeById = useCallback((id: string) => NODES.find(n => n.id === id), []);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const dpr = window.devicePixelRatio || 1;
    const cw = container.clientWidth;
    const ch = container.clientHeight;
    canvas.width = cw * dpr;
    canvas.height = ch * dpr;
    canvas.style.width = `${cw}px`;
    canvas.style.height = `${ch}px`;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.scale(dpr, dpr);

    const { x: cx, y: cy, zoom } = camera;
    timeRef.current += 1;

    // Clear
    ctx.fillStyle = '#0a0a0f';
    ctx.fillRect(0, 0, cw, ch);

    // Subtle grid
    ctx.save();
    ctx.translate(cx, cy);
    ctx.scale(zoom, zoom);

    const gridSize = 100;
    ctx.strokeStyle = 'rgba(255,255,255,0.015)';
    ctx.lineWidth = 0.5;
    for (let gx = 0; gx < W; gx += gridSize) {
      ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke();
    }
    for (let gy = 0; gy < H; gy += gridSize) {
      ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke();
    }

    // Section labels
    for (const sl of SECTION_LABELS) {
      ctx.font = '600 10px Inter, sans-serif';
      ctx.fillStyle = sl.color;
      ctx.textAlign = 'center';
      ctx.letterSpacing = '2px';
      ctx.fillText(sl.label.toUpperCase(), sl.x, sl.y);
    }

    // Edges
    for (const edge of EDGES) {
      const from = getNodeById(edge.from);
      const to = getNodeById(edge.to);
      if (!from || !to) continue;

      const x1 = from.x + from.w;
      const y1 = from.y + from.h / 2;
      const x2 = to.x;
      const y2 = to.y + to.h / 2;

      ctx.strokeStyle = edge.color;
      ctx.lineWidth = edge.width || 1;

      if (edge.dashed) {
        ctx.setLineDash([4, 4]);
      } else {
        ctx.setLineDash([]);
      }

      // Bezier curve
      const cpx = (x1 + x2) / 2;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.bezierCurveTo(cpx, y1, cpx, y2, x2, y2);
      ctx.stroke();

      // Edge label
      if (edge.label) {
        const mx = (x1 + x2) / 2;
        const my = (y1 + y2) / 2 - 6;
        ctx.font = '8px JetBrains Mono, monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.textAlign = 'center';
        ctx.fillText(edge.label, mx, my);
      }
    }
    ctx.setLineDash([]);

    // Particles
    for (const particle of particlesRef.current) {
      particle.t += particle.speed;
      if (particle.t > 1) particle.t -= 1;

      const edge = EDGES[particle.edge];
      const from = getNodeById(edge.from);
      const to = getNodeById(edge.to);
      if (!from || !to) continue;

      const x1 = from.x + from.w;
      const y1 = from.y + from.h / 2;
      const x2 = to.x;
      const y2 = to.y + to.h / 2;

      const t = particle.t;
      const cpx = (x1 + x2) / 2;
      // Bezier interpolation
      const mt = 1 - t;
      const px = mt*mt*mt*x1 + 3*mt*mt*t*cpx + 3*mt*t*t*cpx + t*t*t*x2;
      const py = mt*mt*mt*y1 + 3*mt*mt*t*y1 + 3*mt*t*t*y2 + t*t*t*y2;

      const particleColor = edge.color.substring(0, 7);
      ctx.fillStyle = particleColor + 'cc';
      ctx.beginPath();
      ctx.arc(px, py, 2, 0, Math.PI * 2);
      ctx.fill();

      // Glow
      ctx.fillStyle = particleColor + '30';
      ctx.beginPath();
      ctx.arc(px, py, 6, 0, Math.PI * 2);
      ctx.fill();
    }

    // Nodes
    const isHovered = (node: AtlasNode) => hoveredNode?.id === node.id;

    // Hovered node connections
    const hoveredConnections = new Set<string>();
    if (hoveredNode) {
      for (const edge of EDGES) {
        if (edge.from === hoveredNode.id || edge.to === hoveredNode.id) {
          hoveredConnections.add(edge.from);
          hoveredConnections.add(edge.to);
        }
      }
    }

    for (const node of NODES) {
      const hovered = isHovered(node);
      const connected = hoveredNode ? hoveredConnections.has(node.id) : false;
      const dimmed = hoveredNode && !connected && !hovered;

      // Node background
      ctx.fillStyle = dimmed
        ? 'rgba(255,255,255,0.015)'
        : hovered
          ? 'rgba(255,255,255,0.12)'
          : 'rgba(255,255,255,0.04)';
      ctx.strokeStyle = dimmed
        ? 'rgba(255,255,255,0.03)'
        : hovered
          ? node.color
          : connected
            ? node.color + '60'
            : 'rgba(255,255,255,0.06)';
      ctx.lineWidth = hovered ? 1.5 : 0.8;

      // Rounded rect
      const r = 10;
      ctx.beginPath();
      ctx.moveTo(node.x + r, node.y);
      ctx.lineTo(node.x + node.w - r, node.y);
      ctx.quadraticCurveTo(node.x + node.w, node.y, node.x + node.w, node.y + r);
      ctx.lineTo(node.x + node.w, node.y + node.h - r);
      ctx.quadraticCurveTo(node.x + node.w, node.y + node.h, node.x + node.w - r, node.y + node.h);
      ctx.lineTo(node.x + r, node.y + node.h);
      ctx.quadraticCurveTo(node.x, node.y + node.h, node.x, node.y + node.h - r);
      ctx.lineTo(node.x, node.y + r);
      ctx.quadraticCurveTo(node.x, node.y, node.x + r, node.y);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Glow for hovered
      if (hovered) {
        ctx.shadowColor = node.color;
        ctx.shadowBlur = 20;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // Label
      const alpha = dimmed ? '40' : 'e0';
      ctx.font = '600 11px Inter, sans-serif';
      ctx.fillStyle = node.color + alpha;
      ctx.textAlign = 'left';
      ctx.fillText(node.label, node.x + 10, node.y + 18);

      // Sublabel
      if (node.sublabel) {
        ctx.font = '400 9px Inter, sans-serif';
        ctx.fillStyle = dimmed ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.4)';
        ctx.fillText(node.sublabel, node.x + 10, node.y + 32);
      }

      // Dims badge
      if (node.dims && !dimmed) {
        ctx.font = '400 8px JetBrains Mono, monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.25)';
        ctx.textAlign = 'right';
        ctx.fillText(node.dims, node.x + node.w - 8, node.y + 18);
      }
    }

    // Highlight edges for hovered node
    if (hoveredNode) {
      for (const edge of EDGES) {
        if (edge.from !== hoveredNode.id && edge.to !== hoveredNode.id) continue;
        const from = getNodeById(edge.from);
        const to = getNodeById(edge.to);
        if (!from || !to) continue;

        const x1 = from.x + from.w;
        const y1 = from.y + from.h / 2;
        const x2 = to.x;
        const y2 = to.y + to.h / 2;

        const highlightColor = edge.from === hoveredNode.id
          ? hoveredNode.color + '80'
          : (getNodeById(edge.from)?.color || '#ffffff') + '80';

        ctx.strokeStyle = highlightColor;
        ctx.lineWidth = 2.5;
        ctx.setLineDash(edge.dashed ? [6, 4] : []);

        const cpx = (x1 + x2) / 2;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.bezierCurveTo(cpx, y1, cpx, y2, x2, y2);
        ctx.stroke();

        // Arrow head
        const arrowSize = 6;
        const angle = Math.atan2(y2 - (y1 + y2) / 2, x2 - cpx);
        ctx.fillStyle = highlightColor;
        ctx.beginPath();
        ctx.moveTo(x2, y2);
        ctx.lineTo(x2 - arrowSize * Math.cos(angle - 0.4), y2 - arrowSize * Math.sin(angle - 0.4));
        ctx.lineTo(x2 - arrowSize * Math.cos(angle + 0.4), y2 - arrowSize * Math.sin(angle + 0.4));
        ctx.closePath();
        ctx.fill();
      }
      ctx.setLineDash([]);
    }

    ctx.restore();
  }, [camera, hoveredNode, getNodeById]);

  // Animation loop
  useEffect(() => {
    let raf: number;
    const loop = () => { draw(); raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [draw]);

  // Hit test
  const hitTest = useCallback((mx: number, my: number): AtlasNode | null => {
    const { x: cx, y: cy, zoom } = camera;
    const wx = (mx - cx) / zoom;
    const wy = (my - cy) / zoom;
    for (let i = NODES.length - 1; i >= 0; i--) {
      const n = NODES[i];
      if (wx >= n.x && wx <= n.x + n.w && wy >= n.y && wy <= n.y + n.h) {
        return n;
      }
    }
    return null;
  }, [camera]);

  // Mouse events
  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    if (isDragging.current) {
      setCamera(prev => ({
        ...prev,
        x: dragStart.current.cx + (e.clientX - dragStart.current.x),
        y: dragStart.current.cy + (e.clientY - dragStart.current.y),
      }));
      return;
    }

    const node = hitTest(mx, my);
    setHoveredNode(node);
    setTooltipPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  }, [hitTest]);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    isDragging.current = true;
    dragStart.current = { x: e.clientX, y: e.clientY, cx: camera.x, cy: camera.y };
  }, [camera]);

  const handleMouseUp = useCallback(() => {
    isDragging.current = false;
  }, []);

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const rect = e.currentTarget.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    const factor = e.deltaY > 0 ? 0.92 : 1.08;
    setCamera(prev => {
      const newZoom = Math.max(0.3, Math.min(2, prev.zoom * factor));
      // Zoom toward cursor
      const wx = (mx - prev.x) / prev.zoom;
      const wy = (my - prev.y) / prev.zoom;
      return {
        zoom: newZoom,
        x: mx - wx * newZoom,
        y: my - wy * newZoom,
      };
    });
  }, []);

  // Reset view
  const resetView = useCallback(() => {
    setCamera({ x: 20, y: 20, zoom: 0.72 });
  }, []);

  return (
    <div className="flex flex-col h-full overflow-hidden" style={{ background: '#0a0a0f' }}>
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2" style={{ background: 'rgba(255,255,255,0.02)' }}>
        <div className="flex items-center gap-3">
          <h2 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
            Neuroacoustic Atlas
          </h2>
          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
            Interactive system architecture · Pan: drag · Zoom: scroll
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={resetView}
            className="px-3 py-1 rounded-lg text-xs"
            style={{ background: 'rgba(255,255,255,0.04)', color: 'var(--text-secondary)', border: '1px solid rgba(255,255,255,0.06)' }}
          >
            Reset View
          </button>
          <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
            {Math.round(camera.zoom * 100)}%
          </span>
          {/* Legend */}
          <div className="flex items-center gap-3 ml-4">
            {[
              { label: 'R³', color: colors.r3 },
              { label: 'H³', color: colors.h3 },
              { label: 'C³', color: colors.c3 },
              { label: 'Reward', color: colors.reward },
            ].map(l => (
              <span key={l.label} className="flex items-center gap-1 text-xs">
                <span className="w-2 h-2 rounded-sm" style={{ background: l.color }} />
                <span style={{ color: l.color }}>{l.label}</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Canvas */}
      <div
        ref={containerRef}
        className="flex-1 relative"
        style={{ cursor: isDragging.current ? 'grabbing' : 'grab' }}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        <canvas ref={canvasRef} className="absolute inset-0" />

        {/* Tooltip */}
        {hoveredNode && (
          <div
            className="glass-panel-sm absolute pointer-events-none p-3"
            style={{
              left: Math.min(tooltipPos.x + 16, (containerRef.current?.clientWidth || 800) - 280),
              top: Math.min(tooltipPos.y + 16, (containerRef.current?.clientHeight || 600) - 200),
              maxWidth: 260,
              zIndex: 100,
              borderColor: hoveredNode.color + '40',
            }}
          >
            <div className="flex items-center gap-2 mb-1.5">
              <span className="w-2 h-2 rounded-sm" style={{ background: hoveredNode.color }} />
              <span className="text-sm font-semibold" style={{ color: hoveredNode.color }}>
                {hoveredNode.label}
              </span>
              {hoveredNode.dims && (
                <span className="font-data text-xs ml-auto" style={{ color: 'var(--text-muted)' }}>
                  {hoveredNode.dims}
                </span>
              )}
            </div>
            {hoveredNode.sublabel && (
              <div className="text-xs mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                {hoveredNode.sublabel}
              </div>
            )}
            {hoveredNode.detail && (
              <pre className="text-xs font-data whitespace-pre-wrap" style={{ color: 'var(--text-muted)', lineHeight: 1.5 }}>
                {hoveredNode.detail}
              </pre>
            )}
            {/* Connection count */}
            <div className="mt-2 pt-1.5 text-xs" style={{ borderTop: '1px solid rgba(255,255,255,0.06)', color: 'var(--text-muted)' }}>
              {EDGES.filter(e => e.from === hoveredNode.id).length} outgoing ·{' '}
              {EDGES.filter(e => e.to === hoveredNode.id).length} incoming
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
