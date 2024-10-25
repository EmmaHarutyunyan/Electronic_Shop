document.addEventListener("DOMContentLoaded", function () {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const chatbot = document.querySelector(".chatbot");
    const chatbox = document.querySelector(".chatbox");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendButton = document.querySelector(".chat-input span");

    chatbotToggler.addEventListener("click", function () {
        document.body.classList.toggle("show-chatbot");
    });

    sendButton.addEventListener("click", function () {
        const message = chatInput.value.trim();
        if (message) {
            addMessage("outgoing", message);
            chatInput.value = "";
            respondToUser(message);
        }
    });

    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });

    const buttons = document.querySelectorAll(".chat-btn");
    buttons.forEach((button) => {
        button.addEventListener("click", function () {
            const question = this.innerText;
            addMessage("outgoing", question);
            respondToUser(question);
        });
    });

    function addMessage(type, message) {
        const chat = document.createElement("li");
        chat.classList.add("chat", type);
        
        if (type === "incoming") {
            const imgTag = document.createElement("img");
            imgTag.src = "https://i.ibb.co/qWsG1cJ/image.png";
            imgTag.alt = "Chatbot avatar";
            imgTag.style.width = "40px";
            imgTag.style.height = "40px";
            chat.appendChild(imgTag);
        }
        
        const messageText = document.createElement("p");
        messageText.innerText = message;
        
        chat.appendChild(messageText);
        chatbox.appendChild(chat);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function respondToUser(input) {
        let response = "I'm not quite sure how to help with that.";
    
        if (input.toLowerCase() === "hi" || input.toLowerCase() === "hey") {
            response = "Hello! How can I assist you today?";
        } else if (input.toLowerCase() === "see products" || input.toLowerCase() === "what products do you have") {
            response = "Check out our fantastic range of products in the store!";
            setTimeout(() => {
                window.location.href = "/store/";
            }, 1000);
            return;
        } else if (input.toLowerCase() === "payment options") {
            response = "We accept major credit cards, PayPal, and more!";
        } else if (input.toLowerCase() === "delivery time") {
            response = "Our delivery typically takes 3 to 5 business days.";
        } else if (input.toLowerCase() === "store locations") {
            setTimeout(() => {
                window.open("https://www.google.com/maps/dir/40.2144573,44.5362326/yerevan+armenia/@40.2002374,44.5076775,14z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5!1m1!1s0x406aa2dab8fc8b5b:0x3d1479ae87da526a!2m2!1d44.515209!2d40.1872023?entry=ttu&g_ep=EgoyMDI0MDgyMC4xIKXMDSoASAFQAw%3D%3D", '_blank');
            }, 1000);
            return;
        } else if (input.toLowerCase() === "return policy") {
            response = "You can return items within 30 days for a full refund.";
        } else if (input.toLowerCase() === "customer support") {
            const email = "support@example.com";
            const subject = "Help Needed";
            const body = "I need assistance with...";
            const gmailLink = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(email)}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            
            setTimeout(() => {
                window.open(gmailLink, '_blank');
            }, 1000);
            return;
        } else if (input.toLowerCase() === "thanks") {
            response = "You're welcome! Let me know if you have any more questions.";
        } else {
            response = "I'm here to help! Please ask me anything.";
        }
    
        setTimeout(() => {
            addMessage("incoming", response);
        }, 1000);
    }
    
});
