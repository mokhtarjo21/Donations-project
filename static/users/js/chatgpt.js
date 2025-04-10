const chatContainer = document.getElementById("chat-messages");
const userInput = document.getElementById("chat-input");

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split("; ");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].split("=");
            if (cookie[0] === name) {
                cookieValue = decodeURIComponent(cookie[1]);
                break;
            }
        }
    }
    return cookieValue;
};

const csrfToken = getCookie('csrftoken');


userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    
    
    const message = userInput.value.trim();
    if (!message) return;
    
    appendMessage(message, "user");
    
    userInput.value = "";
    userInput.style.height = "auto";
    
    try {
        
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrfToken, 
            },
            body: JSON.stringify({ message: message }),
        });
        
        const data = await response.json();
        if (data.error) {
            appendMessage(`Error: ${data.error}`, "bot");
          
        } else {
            appendMessage(data.response, "bot");
           
        }
    } catch (error) {
        appendMessage(`Error: ${error.message}`, "bot");
     
    }
}

function appendMessage(message, isUser) {
    // const wrapper = document.createElement("div");
    
    const content = document.createElement("p");
    content.className = `alert ${isUser === 'user' ? 'alert-primary text-end' : 'alert-secondary text-start'}`;
    content.textContent = message;

    // wrapper.appendChild(content);
    chatContainer.appendChild(content);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}





