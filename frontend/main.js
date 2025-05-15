const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

let chatHistory = [];

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    msgDiv.innerText = text;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function renderChat() {
    chatWindow.innerHTML = '';
    chatHistory.forEach(msg => appendMessage(msg.role, msg.text));
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    if (!query) return;
    chatHistory.push({ role: 'user', text: query });
    renderChat();
    userInput.value = '';
    try {
        // Adjust the backend URL as needed
        const res = await fetch('http://localhost:8000/generate-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        if (!res.ok) throw new Error('Server error');
        const data = await res.json();
        chatHistory.push({ role: 'bot', text: data.response });
        renderChat();
    } catch (err) {
        chatHistory.push({ role: 'bot', text: 'Error: Could not get response from backend.' });
        renderChat();
    }
});
