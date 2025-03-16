chrome.runtime.onInstalled.addListener(() => {
    console.log("🚀 AI Sign Language Translator installed!");
});

// Listen for browser action clicks (extension icon click)
chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["content.js"]
    });
});

// Handle messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "fetchVideoData") {
        console.log("📩 Fetching video data for:", message.videoUrl);

        // Process video data (placeholder for AI translation logic)
        sendResponse({ success: true, data: "Video data processed" });
    }
});
