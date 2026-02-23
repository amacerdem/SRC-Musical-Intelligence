import type { Persona, NeuralFamily, FocusArtifact } from "@/types/mind";

// Helper to create starter artifacts
const createArtifact = (family: NeuralFamily, name: string, desc: string): FocusArtifact => ({
  id: `art_${name.toLowerCase().replace(/\s/g, '_')}`,
  name,
  description: desc,
  family,
  rarity: "Common",
  visualAssetUrl: "/artifacts/placeholder_prism.png", // Placeholder
  unlockCondition: "Granted upon awakening."
});

export const personas: Persona[] = [
  // ─── 1. ALCHEMISTS (Transformation) ──────────────────────────────
  {
    id: 1,
    name: "Dopamine Seeker",
    family: "Alchemists",
    tagline: "Lives for the drop",
    color: "#FF6B6B",
    axes: { entropyTolerance: 0.3, resolutionCraving: 0.9, monotonyTolerance: 0.15, salienceSensitivity: 0.9, tensionAppetite: 0.85 },
    description: "You chase the rush of synaptic transformation. The moment tension breaks into release—that is where you exist. Predictability is death; the drop is life.",
    strengths: ["Peak detection", "Anticipation modeling", "Reward sensitivity"],
    compatibleWith: [6, 7, 14, 18],
    famousMinds: ["Hans Zimmer", "Skrillex", "Tchaikovsky"],
    populationPct: 8.2,
    starterArtifact: createArtifact("Alchemists", "The Spike Crystal", "Glows brighter as musical tension increases.")
  },
  {
    id: 6,
    name: "Tension Architect",
    family: "Alchemists",
    tagline: "Building worlds before releasing them",
    color: "#6C5CE7",
    axes: { entropyTolerance: 0.5, resolutionCraving: 0.6, monotonyTolerance: 0.2, salienceSensitivity: 0.85, tensionAppetite: 0.95 },
    description: "You are the master of the build-up. While others crave the destination, you understand that the journey—the careful layering of dissonance and suspension—is the true alchemy.",
    strengths: ["Structural awareness", "Tension mapping", "Layered listening"],
    compatibleWith: [1, 7, 14, 18],
    famousMinds: ["Wagner", "Radiohead", "Nils Frahm"],
    populationPct: 5.3,
    starterArtifact: createArtifact("Alchemists", "The Suspension Bridge", "Visualizes the structural integrity of a buildup.")
  },
  {
    id: 7,
    name: "Contrast Addict",
    family: "Alchemists",
    tagline: "Silence before thunder",
    color: "#FF8A5C",
    axes: { entropyTolerance: 0.45, resolutionCraving: 0.8, monotonyTolerance: 0.1, salienceSensitivity: 0.9, tensionAppetite: 0.6 },
    description: "You live in the extremes. The whisper and the scream. You transmute silence into impact. For you, music without dynamic range is just flat noise.",
    strengths: ["Dynamic range sensitivity", "Contrast detection", "Impact response"],
    compatibleWith: [1, 6, 12, 18],
    famousMinds: ["Mahler", "Bjork", "Trent Reznor"],
    populationPct: 4.9,
    starterArtifact: createArtifact("Alchemists", "The Dynamic Scale", "Weighs the difference between the quietest and loudest moments.")
  },
  {
    id: 18,
    name: "Dramatic Arc",
    family: "Alchemists",
    tagline: "Every piece is a movie",
    color: "#DC2626",
    axes: { entropyTolerance: 0.5, resolutionCraving: 0.85, monotonyTolerance: 0.15, salienceSensitivity: 0.9, tensionAppetite: 0.85 },
    description: "You perceive music as a transformative narrative. You don't hear notes; you hear scenes, conflicts, and resolutions. You turn sound into cinema.",
    strengths: ["Narrative arc detection", "Climax prediction", "Dramatic sensitivity"],
    compatibleWith: [1, 5, 6, 8],
    famousMinds: ["John Williams", "Ennio Morricone", "Lisa Gerrard"],
    populationPct: 5.7,
    starterArtifact: createArtifact("Alchemists", "The Director's Lens", "Frames music as a cinematic sequence.")
  },

  // ─── 2. ARCHITECTS (Structure) ───────────────────────────────────
  {
    id: 2,
    name: "Harmonic Purist",
    family: "Architects",
    tagline: "Beauty in perfect intervals",
    color: "#4ECDC4",
    axes: { entropyTolerance: 0.2, resolutionCraving: 0.85, monotonyTolerance: 0.5, salienceSensitivity: 0.3, tensionAppetite: 0.2 },
    description: "Consonance is your sacred geometry. You see the mathematical perfection in every interval. Chaos disturbs you; you seek the crystalline truth of perfect resolution.",
    strengths: ["Harmonic analysis", "Voice leading sensitivity", "Tonal memory"],
    compatibleWith: [5, 9, 13, 20],
    famousMinds: ["Bach", "Debussy", "Jacob Collier"],
    populationPct: 5.1,
    starterArtifact: createArtifact("Architects", "The Crystal Metronome", "Pulses in perfect sync with harmonic resolution.")
  },
  {
    id: 4,
    name: "Minimal Zen",
    family: "Architects",
    tagline: "Less is everything",
    color: "#B8C6DB",
    axes: { entropyTolerance: 0.15, resolutionCraving: 0.3, monotonyTolerance: 0.9, salienceSensitivity: 0.1, tensionAppetite: 0.1 },
    description: "In structure and repetition, you find infinite depth. While complex minds seek chaos, your mind constructs cathedrals out of silence and subtle variation.",
    strengths: ["Micro-variation detection", "Sustained attention", "Meditative depth"],
    compatibleWith: [13, 15, 17, 22],
    famousMinds: ["Steve Reich", "Brian Eno", "Ryuichi Sakamoto"],
    populationPct: 4.7,
    starterArtifact: createArtifact("Architects", "The Still Water", "A sphere of water that ripples only with true novelty.")
  },
  {
    id: 5,
    name: "Resolution Junkie",
    family: "Architects",
    tagline: "The cadence is the drug",
    color: "#FFD93D",
    axes: { entropyTolerance: 0.25, resolutionCraving: 0.95, monotonyTolerance: 0.2, salienceSensitivity: 0.55, tensionAppetite: 0.5 },
    description: "You have an addiction to closure. The perfect V-I cadence isn't just a sound; it's a physiological relief. You build mental structures that demand completion.",
    strengths: ["Cadence sensitivity", "Harmonic expectation", "Closure detection"],
    compatibleWith: [1, 2, 8, 18],
    famousMinds: ["Beethoven", "Adele", "Chopin"],
    populationPct: 6.8,
    starterArtifact: createArtifact("Architects", "The Keystone", "Glows when a musical phrase is perfectly resolved.")
  },
  {
    id: 9,
    name: "Pattern Hunter",
    family: "Architects",
    tagline: "Every motif tells a story",
    color: "#00B894",
    axes: { entropyTolerance: 0.2, resolutionCraving: 0.75, monotonyTolerance: 0.25, salienceSensitivity: 0.5, tensionAppetite: 0.25 },
    description: "You decode the blueprints of sound. Recurring motifs, hidden symmetries, inversions—your mind maps the architecture of a piece in real-time.",
    strengths: ["Motif recognition", "Temporal pattern matching", "Structural memory"],
    compatibleWith: [2, 16, 20, 24],
    famousMinds: ["Bach", "Tool", "Ligeti"],
    populationPct: 3.8,
    starterArtifact: createArtifact("Architects", "The Fractal Compass", "Points to recurring patterns in the audio stream.")
  },
  {
    id: 20,
    name: "Precision Mind",
    family: "Architects",
    tagline: "Every note accounted for",
    color: "#60A5FA",
    axes: { entropyTolerance: 0.15, resolutionCraving: 0.8, monotonyTolerance: 0.2, salienceSensitivity: 0.5, tensionAppetite: 0.25 },
    description: "Accuracy is your aesthetic. You hear the grid behind the music. Every deviation in pitch or time stands out like a flare. You seek the perfect execution.",
    strengths: ["Pitch accuracy", "Timing precision", "Performance evaluation"],
    compatibleWith: [2, 9, 16, 24],
    famousMinds: ["Glenn Gould", "Wynton Marsalis", "Boulez"],
    populationPct: 3.5,
    starterArtifact: createArtifact("Architects", "The Laser Level", "Visualizes the deviation from perfect pitch and time.")
  },

  // ─── 3. EXPLORERS (Novelty) ──────────────────────────────────────
  {
    id: 3,
    name: "Chaos Explorer",
    family: "Explorers",
    tagline: "Order is overrated",
    color: "#FF4081",
    axes: { entropyTolerance: 0.92, resolutionCraving: 0.2, monotonyTolerance: 0.15, salienceSensitivity: 0.8, tensionAppetite: 0.85 },
    description: "You thrive in the entropy. Where others hear noise, you hear new potential. Glitches, dissonance, and broken structures are your native language.",
    strengths: ["Entropy processing", "Pattern-breaking detection", "Novel stimulus response"],
    compatibleWith: [10, 14, 21, 23],
    famousMinds: ["John Cage", "Aphex Twin", "Xenakis"],
    populationPct: 3.4,
    starterArtifact: createArtifact("Explorers", "The Glitch Prism", "Fractures sound into unexpected colors.")
  },
  {
    id: 10,
    name: "Sonic Nomad",
    family: "Explorers",
    tagline: "Never the same river twice",
    color: "#E17055",
    axes: { entropyTolerance: 0.85, resolutionCraving: 0.2, monotonyTolerance: 0.1, salienceSensitivity: 0.55, tensionAppetite: 0.7 },
    description: "A traveler of the sonic landscape. You refuse to settle in one genre or timbre. Your mind demands constant novelty; familiarity is stagnation.",
    strengths: ["Novelty detection", "Cross-genre adaptation", "Exploratory listening"],
    compatibleWith: [3, 19, 21, 23],
    famousMinds: ["David Bowie", "Flying Lotus", "Arca"],
    populationPct: 4.1,
    starterArtifact: createArtifact("Explorers", "The Compass of Nowhere", "always points to the most unfamiliar sound.")
  },
  {
    id: 19,
    name: "Curious Wanderer",
    family: "Explorers",
    tagline: "What happens if...?",
    color: "#34D399",
    axes: { entropyTolerance: 0.7, resolutionCraving: 0.3, monotonyTolerance: 0.4, salienceSensitivity: 0.5, tensionAppetite: 0.5 },
    description: "Your listening is a question, not an answer. You explore sound with innocent curiosity, unburdened by the need for predefined structures.",
    strengths: ["Exploratory attention", "Genre fluidity", "Open-mindedness"],
    compatibleWith: [3, 10, 23, 24],
    famousMinds: ["David Bowie", "Bjork", "Thom Yorke"],
    populationPct: 4.2,
    starterArtifact: createArtifact("Explorers", "The Open Door", "Resonates when you step out of your comfort zone.")
  },
  {
    id: 23,
    name: "Edge Runner",
    family: "Explorers",
    tagline: "The dissonance is the message",
    color: "#A3E635",
    axes: { entropyTolerance: 0.85, resolutionCraving: 0.15, monotonyTolerance: 0.15, salienceSensitivity: 0.6, tensionAppetite: 0.8 },
    description: "You live on the boundary of what is considered 'music'. You push your perception to the edge, finding beauty in the breakdown of the signal.",
    strengths: ["Dissonance processing", "Boundary exploration", "Avant-garde sensitivity"],
    compatibleWith: [3, 10, 14, 19],
    famousMinds: ["Penderecki", "Merzbow", "Autechre"],
    populationPct: 2.3,
    starterArtifact: createArtifact("Explorers", "The Noise Filter", "Inverts signal and noise.")
  },
  {
    id: 24,
    name: "Renaissance Mind",
    family: "Explorers",
    tagline: "All dimensions, fully alive",
    color: "#FBBF24",
    axes: { entropyTolerance: 0.7, resolutionCraving: 0.75, monotonyTolerance: 0.45, salienceSensitivity: 0.8, tensionAppetite: 0.7 },
    description: "A rare anomaly. You belong to no single family because you embody them all. You have high tolerance for chaos AND high craving for structure. A universal explorer.",
    strengths: ["Multi-dimensional balance", "Genre versatility", "Adaptive listening"],
    compatibleWith: [9, 12, 16, 19],
    famousMinds: ["Mozart", "Prince", "Kendrick Lamar"],
    populationPct: 1.9,
    starterArtifact: createArtifact("Explorers", "The Omni-Lens", "Allows you to see all dimensions simultaneously.")
  },

  // ─── 4. ANCHORS (Emotion/Memory) ─────────────────────────────────
  {
    id: 8,
    name: "Structural Romantic",
    family: "Anchors",
    tagline: "Grand narratives in sound",
    color: "#F8B500",
    axes: { entropyTolerance: 0.4, resolutionCraving: 0.8, monotonyTolerance: 0.45, salienceSensitivity: 0.75, tensionAppetite: 0.6 },
    description: "You feel the architecture of emotion. Music weaves a story that anchors your memories. For you, a melody is a thread to the past.",
    strengths: ["Narrative detection", "Long-form listening", "Emotional arc tracking"],
    compatibleWith: [5, 11, 18, 22],
    famousMinds: ["Schubert", "John Williams", "Joep Beving"],
    populationPct: 6.2,
    starterArtifact: createArtifact("Anchors", "The Memory Locket", "Stores the emotional imprint of a song.")
  },
  {
    id: 11,
    name: "Emotional Anchor",
    family: "Anchors",
    tagline: "Feeling is knowing",
    color: "#FDA7DF",
    axes: { entropyTolerance: 0.4, resolutionCraving: 0.7, monotonyTolerance: 0.5, salienceSensitivity: 0.55, tensionAppetite: 0.5 },
    description: "Your cognition is guided by the heart. You don't analyze music; you feel it resonate in your chest. Emotional truth is your only metric.",
    strengths: ["Emotional resonance", "Valence sensitivity", "Empathic listening"],
    compatibleWith: [5, 8, 15, 22],
    famousMinds: ["Chopin", "Billie Eilish", "Max Richter"],
    populationPct: 7.4,
    starterArtifact: createArtifact("Anchors", "The Heartbeat Sensor", "Syncs with the emotional pulse of the music.")
  },
  {
    id: 13,
    name: "Tonal Dreamer",
    family: "Anchors",
    tagline: "Floating in harmonic clouds",
    color: "#818CF8",
    axes: { entropyTolerance: 0.2, resolutionCraving: 0.4, monotonyTolerance: 0.75, salienceSensitivity: 0.2, tensionAppetite: 0.15 },
    description: "You drift in the textures and colors of sound. Gravity has no hold on you. You anchor yourself in the atmosphere rather than the beat.",
    strengths: ["Tonal immersion", "Overtone sensitivity", "Ambient processing"],
    compatibleWith: [4, 15, 17, 22],
    famousMinds: ["Debussy", "Sigur Ros", "Olafur Arnalds"],
    populationPct: 4.3,
    starterArtifact: createArtifact("Anchors", "The Cloud Jar", "Captures the texture of the atmosphere.")
  },
  {
    id: 15,
    name: "Quiet Observer",
    family: "Anchors",
    tagline: "Listening deeper than sound",
    color: "#94A3B8",
    axes: { entropyTolerance: 0.3, resolutionCraving: 0.5, monotonyTolerance: 0.6, salienceSensitivity: 0.15, tensionAppetite: 0.35 },
    description: "Silence speaks to you. You find your center in the spaces between notes. A deep, meditative listener who anchors the world in calm.",
    strengths: ["Micro-detail sensitivity", "Patient attention", "Depth perception"],
    compatibleWith: [4, 11, 13, 22],
    famousMinds: ["Erik Satie", "Nils Frahm", "Arvo Part"],
    populationPct: 4.5,
    starterArtifact: createArtifact("Anchors", "The Deep Ear", "Amplifies the quietest details.")
  },
  {
    id: 17,
    name: "Ambient Flow",
    family: "Anchors",
    tagline: "Texture over time",
    color: "#A78BFA",
    axes: { entropyTolerance: 0.25, resolutionCraving: 0.2, monotonyTolerance: 0.85, salienceSensitivity: 0.1, tensionAppetite: 0.1 },
    description: "You exist in a state of flow. Time dissolves into texture. You anchor yourself in the present moment, washed over by sound.",
    strengths: ["Textural awareness", "Temporal dissolution", "Environmental listening"],
    compatibleWith: [4, 13, 15, 22],
    famousMinds: ["Brian Eno", "Grouper", "Stars of the Lid"],
    populationPct: 3.9,
    starterArtifact: createArtifact("Anchors", "The Flow Stone", "Smooths out the passage of time.")
  },
  {
    id: 22,
    name: "Nostalgic Soul",
    family: "Anchors",
    tagline: "Memory is melody",
    color: "#F472B6",
    axes: { entropyTolerance: 0.2, resolutionCraving: 0.55, monotonyTolerance: 0.7, salienceSensitivity: 0.45, tensionAppetite: 0.2 },
    description: "Your mind is a library of the past on fire. Music is the key to unlocking forgotten times. You anchor your identity in the soundtrack of your history.",
    strengths: ["Musical memory", "Familiarity response", "Emotional attachment"],
    compatibleWith: [4, 8, 11, 13],
    famousMinds: ["Einaudi", "Norah Jones", "Yiruma"],
    populationPct: 5.8,
    starterArtifact: createArtifact("Anchors", "The Time Capsule", "Preserves the feeling of a moment forever.")
  },

  // ─── 5. KINETICISTS (Drive/Energy) ───────────────────────────────
  {
    id: 12,
    name: "Rhythmic Pulse",
    family: "Kineticists",
    tagline: "The beat is the brain",
    color: "#F97316",
    axes: { entropyTolerance: 0.45, resolutionCraving: 0.5, monotonyTolerance: 0.3, salienceSensitivity: 0.8, tensionAppetite: 0.55 },
    description: "You don't just hear rhythm; your neurons fire in sync with it. Movement, groove, and pulse are the fundamental languages of your mind.",
    strengths: ["Beat entrainment", "Polyrhythm processing", "Groove sensitivity"],
    compatibleWith: [7, 16, 21, 24],
    famousMinds: ["Questlove", "Steve Gadd", "J Dilla"],
    populationPct: 5.9,
    starterArtifact: createArtifact("Kineticists", "The Sync Core", "Locks your heartbeat to the BPM.")
  },
  {
    id: 14,
    name: "Dynamic Storm",
    family: "Kineticists",
    tagline: "Everything at once",
    color: "#EF4444",
    axes: { entropyTolerance: 0.85, resolutionCraving: 0.8, monotonyTolerance: 0.1, salienceSensitivity: 0.95, tensionAppetite: 0.9 },
    description: "A hurricane of cognition. You crave high energy, high density, high impact. Your mind creates order out of the eye of the storm.",
    strengths: ["Multi-dimensional processing", "High-bandwidth listening", "Peak experience"],
    compatibleWith: [1, 3, 6, 24],
    famousMinds: ["Stravinsky", "Meshuggah", "Hans Zimmer"],
    populationPct: 2.8,
    starterArtifact: createArtifact("Kineticists", "The Maelstrom Engine", "Converts chaos into power.")
  },
  {
    id: 16,
    name: "Groove Mechanic",
    family: "Kineticists",
    tagline: "Engineering the pocket",
    color: "#22D3EE",
    axes: { entropyTolerance: 0.45, resolutionCraving: 0.5, monotonyTolerance: 0.25, salienceSensitivity: 0.75, tensionAppetite: 0.3 },
    description: "You feel the micro-timing that makes a head nod. The Pocket. You understand the mechanics of motion and the subtle friction that creates groove.",
    strengths: ["Micro-timing sensitivity", "Groove detection", "Rhythmic precision"],
    compatibleWith: [9, 12, 20, 24],
    famousMinds: ["Herbie Hancock", "Daft Punk", "Anderson .Paak"],
    populationPct: 4.6,
    starterArtifact: createArtifact("Kineticists", "The Pocket Watch", "Measures the swing of the universe.")
  },
  {
    id: 21,
    name: "Raw Energy",
    family: "Kineticists",
    tagline: "Volume is a dimension",
    color: "#FB923C",
    axes: { entropyTolerance: 0.7, resolutionCraving: 0.25, monotonyTolerance: 0.2, salienceSensitivity: 0.85, tensionAppetite: 0.55 },
    description: "Subtlety is fine, but power is truth. You respond to the visceral impact of sound waves hitting the body. Music is a physical force.",
    strengths: ["Energy response", "Physical engagement", "Impact sensitivity"],
    compatibleWith: [3, 10, 12, 14],
    famousMinds: ["Jimi Hendrix", "Nine Inch Nails", "Sunn O)))"],
    populationPct: 3.6,
    starterArtifact: createArtifact("Kineticists", "The Amplifier", "Boosts the signal of reality.")
  }
];

export function getPersona(id: number): Persona {
  return personas.find((p) => p.id === id) ?? personas[0];
}
