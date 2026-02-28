/* ── SpotifySimulator — Thin delegation to MIDataService ─────────────
 *  Preserves the same MockTrack interface & API surface so all
 *  consumers (M3Hub, useGamificationStore, SpotifyProfile) continue
 *  to work with zero import changes.
 *  ──────────────────────────────────────────────────────────────────── */

import type { NeuralFamily } from "@/types/mind";
import type { M3TrackSignal } from "@/types/m3";
import { miDataService } from "./MIDataService";

export interface MockTrack {
    id: string;
    name: string;
    artist: string;
    albumArt: string;
    features: {
        energy: number;
        valence: number;
        tempo: number;
        danceability: number;
        acousticness: number;
        harmonicComplexity: number;
        timbralBrightness: number;
    };
    dominantFamily: NeuralFamily;
    genre: string;
    durationSec: number;
}

/**
 * Convert a MockTrack to an M3TrackSignal for feeding M³.
 */
export function trackToM3Signal(track: MockTrack, opts?: { isRepeat?: boolean; wasSkipped?: boolean }): M3TrackSignal {
    return {
        energy: track.features.energy,
        valence: track.features.valence,
        tempo: track.features.tempo,
        danceability: track.features.danceability,
        acousticness: track.features.acousticness,
        harmonicComplexity: track.features.harmonicComplexity,
        timbralBrightness: track.features.timbralBrightness,
        duration: track.durationSec,
        isRepeat: opts?.isRepeat ?? false,
        wasSkipped: opts?.wasSkipped ?? false,
    };
}

export const SpotifySimulator = {
    /** Get a random track from the real MI dataset */
    getCurrentTrack: (): Promise<MockTrack> => miDataService.getCurrentTrack(),

    /** Get 5 random tracks from the real MI dataset */
    getRecentHistory: (): MockTrack[] => miDataService.getRecentHistory(),

    /** Get a listening session (5-10 tracks with timestamps) from real data */
    getListeningSession: () => miDataService.getListeningSession(),

    /** Get 15-20 tracks for temperament calculation at birth */
    getInitialBatch: (): MockTrack[] => miDataService.getInitialBatch(),
};
