import { SocialMetrics } from "@/types/mind";

export const InstagramSimulator = {
    /** 
     * Simulates sharing an artifact to Instagram Stories.
     * Returns a share ID.
     */
    shareToStory: (assetUrl: string): Promise<string> => {
        return new Promise((resolve) => {
            console.log(`[InstagramSimulator] Sharing ${assetUrl} to Stories...`);
            setTimeout(() => {
                const shareId = `share_${Date.now()}`;
                resolve(shareId);
            }, 1500); // Simulate upload time
        });
    },

    /**
     * Simulates polling for metrics on a shared story.
     * Values increase over time to simulate real engagement.
     */
    getMetrics: (shareId: string): Promise<SocialMetrics> => {
        return new Promise((resolve) => {
            // Simulate random engagement
            const baseLikes = Math.floor(Math.random() * 50) + 10;
            const baseViews = baseLikes * (Math.floor(Math.random() * 5) + 2);

            setTimeout(() => {
                resolve({
                    platform: 'instagram',
                    shareId,
                    views: baseViews,
                    likes: baseLikes,
                    comments: Math.floor(baseLikes / 10),
                    resonanceScore: baseLikes * 10 + baseViews // Simple formula
                });
            }, 800);
        });
    }
};
