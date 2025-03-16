document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("startTranslation");
    const statusMessage = document.getElementById("status");

    if (!startButton) {
        console.error("❌ Start button not found in popup.html!");
        return;
    }

    startButton.addEventListener("click", function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            if (tabs.length === 0) {
                console.error("❌ No active tab found.");
                updateStatus("❌ No active tab found", "red");
                return;
            }

            chrome.tabs.sendMessage(tabs[0].id, { action: "fetchVideoData" }, function (response) {
                if (!response || !response.success || !response.videoURL) {
                    console.error("❌ No video detected.");
                    updateStatus("❌ No video found", "red");
                } else {
                    console.log("✅ Video detected:", response.videoURL);
                    updateStatus("✅ Video detected! Sending to backend...", "green");

                    // Send video URL to backend
                    fetch("http://127.0.0.1:8000/translate/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ video_url: response.videoURL }),
                    })
                        .then(async res => {
                            if (!res.ok) {
                                throw new Error(`HTTP error! Status: ${res.status}`);
                            }
                            return res.json();
                        })
                        .then(data => {
                            console.log("✅ Backend Response:", data);
                            if (data.translation) {
                                updateStatus(`✅ Translation received!<br>${data.translation}`, "green");
                            } else {
                                updateStatus("❌ Error in translation!", "red");
                            }
                        })
                        .catch(error => {
                            console.error("❌ Backend request failed", error);
                            updateStatus("❌ Error connecting to backend!", "red");
                        });
                }
            });
        });
    });

    function updateStatus(message, color) {
        statusMessage.innerHTML = message;
        statusMessage.style.color = color;
    }
});
