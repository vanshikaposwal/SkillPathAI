document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatHistory = document.getElementById('chatHistory');
    const sendBtn = document.getElementById('sendBtn');

    if (!chatForm) return;

    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;

    chatForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;

        // Append user message
        appendMessage('user', msg);
        chatInput.value = '';
        sendBtn.disabled = true;

        // Typing indicator
        const typingEl = appendMessage('assistant', '<div class="spinner-grow spinner-grow-sm text-primary" role="status"></div> Thinking...', true);

        try {
            const res = await fetch('/api/ai/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ message: msg })
            });
            const data = await res.json();
            typingEl.remove();
            appendMessage('assistant', formatMarkdown(data.assistant_reply));
        } catch (e) {
            typingEl.remove();
            appendMessage('assistant', 'Sorry, I encountered an issue processing your question. Please try again.');
        } finally {
            sendBtn.disabled = false;
        }
    });

    function appendMessage(role, text, isTyping = false) {
        const div = document.createElement('div');
        div.className = `chat-msg ${role}`;
        div.innerHTML = text;
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return div;
    }

    function formatMarkdown(text) {
        if (!text) return '';
        // Simple client-side formatting for bullet points and bold
        let html = text
            .replace(/### (.*?)
/g, '<h6 class="fw-bold text-primary mt-2 mb-1">$1</h6>')
            .replace(/## (.*?)
/g, '<h5 class="fw-bold mt-2 mb-1">$1</h5>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/

/g, '<br><br>')
            .replace(/
- /g, '<br>• ');
        return html;
    }

    // Chip click handlers
    document.querySelectorAll('.prompt-chip').forEach(chip => {
        chip.addEventListener('click', function () {
            chatInput.value = this.innerText;
            chatForm.dispatchEvent(new Event('submit'));
        });
    });
});
