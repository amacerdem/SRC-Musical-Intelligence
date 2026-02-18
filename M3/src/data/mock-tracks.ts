export interface Track {
  id: string;
  title: string;
  artist: string;
  genre: string;
  match?: number;
  duration: string;
  plays?: number;
  isLive?: boolean;
  creator?: string;
}

export const recommendedTracks: Track[] = [
  { id: "r1", title: "Neural Overdrive", artist: "SynthMind", genre: "Electronic", match: 94, duration: "3:42" },
  { id: "r2", title: "Deep Resonance", artist: "Harmonic Lab", genre: "Ambient", match: 91, duration: "5:18" },
  { id: "r3", title: "Entropy Garden", artist: "Kai", genre: "Post-Rock", match: 88, duration: "4:55" },
  { id: "r4", title: "Cognitive Drift", artist: "Max Richter", genre: "Neo-Classical", match: 85, duration: "6:02" },
  { id: "r5", title: "Tension Architecture", artist: "Nils Frahm", genre: "Minimal", match: 82, duration: "4:33" },
  { id: "r6", title: "Midnight Signal", artist: "Aphex Twin", genre: "IDM", match: 79, duration: "3:21" },
];

export const topPerformances: Track[] = [
  { id: "t1", title: "Neural Drift", artist: "Luna x Max", genre: "Live Duo", plays: 4200, isLive: true, duration: "12:30" },
  { id: "t2", title: "Entropy Garden", artist: "Kai", genre: "Solo", plays: 3800, duration: "8:15" },
  { id: "t3", title: "Deep State", artist: "Echo", genre: "Solo", plays: 3200, duration: "6:40" },
  { id: "t4", title: "Harmonic Pulse", artist: "Yuki", genre: "Live Solo", plays: 2900, isLive: true, duration: "10:05" },
  { id: "t5", title: "Midnight Architecture", artist: "Max", genre: "Solo", plays: 2400, duration: "7:22" },
];

export interface FriendActivity {
  id: string;
  userId: string;
  userName: string;
  action: "listening" | "composed" | "performing";
  trackTitle: string;
  timeAgo: string;
}

export const friendActivity: FriendActivity[] = [
  { id: "fa1", userId: "u1", userName: "Luna", action: "performing", trackTitle: "Neural Drift", timeAgo: "Live now" },
  { id: "fa2", userId: "u2", userName: "Max", action: "composed", trackTitle: "Midnight Architecture", timeAgo: "2h ago" },
  { id: "fa3", userId: "u3", userName: "Kai", action: "listening", trackTitle: "Entropy Garden", timeAgo: "4h ago" },
  { id: "fa4", userId: "u4", userName: "Yuki", action: "performing", trackTitle: "Harmonic Pulse", timeAgo: "Live now" },
  { id: "fa5", userId: "u5", userName: "Echo", action: "listening", trackTitle: "Deep State", timeAgo: "6h ago" },
];
