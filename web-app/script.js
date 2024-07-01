document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') {
        return;
    }
    appendMessage('user', userInput);
    document.getElementById('user-input').value = '';

    fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); 
        if (data && data.length > 0) {
            data.forEach(msg => appendMessage('bot', msg.text));
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
