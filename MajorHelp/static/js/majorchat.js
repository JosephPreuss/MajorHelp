document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatWindow = document.getElementById("chat-window");

    // Connect to default channel on load
    connectToChannel("general");

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault(); // ⛔ Prevent the page from reloading

        const message = chatInput.value.trim();
        if (message !== "") {
            // Send through WebSocket
            if (window.chatSocket && window.chatSocket.readyState === WebSocket.OPEN) {
                window.chatSocket.send(JSON.stringify({ message: message }));
            }
            chatInput.value = "";
        }
    });

    function appendMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message");
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function connectToChannel(channelName) {
        if (window.chatSocket) {
            window.chatSocket.close();
        }

        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const chatSocket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${channelName}/`);
        window.chatSocket = chatSocket;

        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            appendMessage(data.username, data.message);
        };

        chatSocket.onclose = function (e) {
            console.error("Chat socket closed unexpectedly");
        };

        chatSocket.onerror = function (e) {
            console.error("WebSocket error:", e);
        };
    }

    // Allow channel switching
    const channelButtons = document.querySelectorAll(".channel");
    channelButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            document.querySelector(".channel.active")?.classList.remove("active");
            btn.classList.add("active");
            const channel = btn.getAttribute("data-channel");
            connectToChannel(channel);
        });
    });
});
