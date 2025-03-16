console.log("✅ content.js loaded!");

// Function to get the video element and its source
function getVideoSource() {
    let videoElement = document.querySelector("video");

    if (!videoElement) {
        console.warn("❌ No video element found.");
        return null;
    }

    let videoSrc = videoElement.src || videoElement.currentSrc;

    if (!videoSrc) {
        // Check for <source> tags inside the <video> element
        let sourceElement = videoElement.querySelector("source");
        if (sourceElement) {
            videoSrc = sourceElement.src;
        }
    }

    if (!videoSrc) {
        console.warn("⚠️ Video element found, but no valid source detected.");
        return null;
    }

    console.log("✅ Video source detected:", videoSrc);
    return { videoElement, videoSrc };
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("📩 Message received in content.js:", request);

    if (request.action === "fetchVideoData") {
        let videoData = getVideoSource();

        if (!videoData) {
            sendResponse({ success: false, message: "No video found or unsupported format." });
            return;
        }

        console.log("🎥 Video detected:", videoData.videoSrc);

        sendResponse({
            success: true,
            videoURL: videoData.videoSrc
        });
    }

    return true; // Required for async sendResponse
});
