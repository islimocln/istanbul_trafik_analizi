class Chatbot {
    constructor() {
        this.chatWindow = null;
        this.isOpen = false;
        this.messages = [];
        this.initializeChatbot();
    }

    initializeChatbot() {
        // Create chat window
        this.chatWindow = document.createElement('div');
        this.chatWindow.className = 'chat-window';
        this.chatWindow.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 300px;
            height: 400px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: none;
            flex-direction: column;
            z-index: 1000;
        `;

        // Create chat header
        const header = document.createElement('div');
        header.className = 'chat-header';
        header.style.cssText = `
            padding: 10px;
            background: #2c3e50;
            color: white;
            border-radius: 10px 10px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        `;
        header.innerHTML = `
            <span>İstanbul Rehberi Asistanı</span>
            <button class="close-btn" style="background: none; border: none; color: white; cursor: pointer;">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Create chat messages container
        const messagesContainer = document.createElement('div');
        messagesContainer.className = 'chat-messages';
        messagesContainer.style.cssText = `
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        `;

        // Create chat input
        const inputContainer = document.createElement('div');
        inputContainer.className = 'chat-input';
        inputContainer.style.cssText = `
            padding: 10px;
            border-top: 1px solid #eee;
            display: flex;
        `;
        inputContainer.innerHTML = `
            <input type="text" placeholder="Mesajınızı yazın..." style="flex: 1; padding: 5px; border: 1px solid #ddd; border-radius: 5px; margin-right: 5px;">
            <button class="send-btn" style="background: #2c3e50; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">
                <i class="fas fa-paper-plane"></i>
            </button>
        `;

        // Append elements
        this.chatWindow.appendChild(header);
        this.chatWindow.appendChild(messagesContainer);
        this.chatWindow.appendChild(inputContainer);
        document.body.appendChild(this.chatWindow);

        // Add event listeners
        const closeBtn = header.querySelector('.close-btn');
        const sendBtn = inputContainer.querySelector('.send-btn');
        const input = inputContainer.querySelector('input');

        closeBtn.addEventListener('click', () => this.toggleChat());
        sendBtn.addEventListener('click', () => this.sendMessage(input));
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage(input);
            }
        });

        // Add initial message
        this.addMessage('Merhaba! Size nasıl yardımcı olabilirim?', 'bot');
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        this.chatWindow.style.display = this.isOpen ? 'flex' : 'none';
    }

    addMessage(text, sender, html = null) {
        const messagesContainer = this.chatWindow.querySelector('.chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 15px;
            max-width: 80%;
            ${sender === 'user' ? 'margin-left: auto; background: #2c3e50; color: white;' : 'margin-right: auto; background: #f0f0f0;'}
        `;
        if (html) {
            messageDiv.innerHTML = html;
        } else {
            messageDiv.textContent = text;
        }
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async sendMessage(input) {
        const text = input.value.trim();
        if (text) {
            this.addMessage(text, 'user');
            input.value = '';

            // Simulate bot response
            const { response, html } = await this.getBotResponse(text);
            setTimeout(() => {
                this.addMessage(response, 'bot', html);
                // Add event listeners for navigation buttons
                const navBtns = document.querySelectorAll('.chat-nav-btn');
                navBtns.forEach(btn => {
                    btn.addEventListener('click', () => {
                        window.location.href = btn.dataset.href;
                    });
                });
            }, 500);
        }
    }

    async getBotResponse(text) {
        const lowerText = text.toLowerCase();
        // Navigation helpers
        const navBtn = (label, href) => `<button class='chat-nav-btn' data-href='${href}' style='margin-top:8px; background:#2c3e50; color:white; border:none; border-radius:5px; padding:5px 12px; cursor:pointer;'>${label}</button>`;

        if (lowerText.includes('merhaba') || lowerText.includes('selam')) {
            return { response: 'Merhaba! Size nasıl yardımcı olabilirim?' };
        }
        if (lowerText.includes('eczane')) {
            return {
                response: 'Size en yakın eczaneleri haritada gösterebilirim. Harita sayfasına gitmek ister misiniz?',
                html: `Size en yakın eczaneleri haritada gösterebilirim.<br>${navBtn('Haritaya Git', 'map.html')}`
            };
        }
        if (lowerText.includes('benzin') || lowerText.includes('petrol')) {
            return {
                response: 'En yakın benzin istasyonlarını haritada gösterebilirim. Harita sayfasına gitmek ister misiniz?',
                html: `En yakın benzin istasyonlarını haritada gösterebilirim.<br>${navBtn('Haritaya Git', 'map.html')}`
            };
        }
        if (lowerText.includes('otel')) {
            return {
                response: 'Oteller sayfasında en iyi otelleri ve değerlendirmeleri bulabilirsiniz. Oteller sayfasına gitmek ister misiniz?',
                html: `Oteller sayfasında en iyi otelleri ve değerlendirmeleri bulabilirsiniz.<br>${navBtn('Otellere Git', 'hotels.html')}`
            };
        }
        if (lowerText.includes('harita')) {
            return {
                response: 'Harita sayfasına yönlendirebilirim.',
                html: `Harita sayfasına yönlendirebilirim.<br>${navBtn('Haritaya Git', 'map.html')}`
            };
        }
        if (lowerText.includes('ana sayfa') || lowerText.includes('anasayfa') || lowerText.includes('başlangıç')) {
            return {
                response: 'Ana sayfaya yönlendirebilirim.',
                html: `Ana sayfaya yönlendirebilirim.<br>${navBtn('Ana Sayfa', 'index.html')}`
            };
        }
        if (lowerText.includes('yardım')) {
            return {
                response: 'Size yardımcı olabileceğim başlıca konular: eczane, benzin istasyonu, otel, harita, ana sayfa. Hangi konuda bilgi almak istersiniz?',
                html: `Size yardımcı olabileceğim başlıca konular:<ul><li>Eczane</li><li>Benzin İstasyonu</li><li>Otel</li><li>Harita</li><li>Ana Sayfa</li></ul>`
            };
        }
        if (lowerText.includes('teşekkür')) {
            return { response: 'Rica ederim! Başka bir konuda yardıma ihtiyacınız var mı?' };
        }
        return { response: 'Üzgünüm, bu konuda size yardımcı olamıyorum. Başka bir soru sorabilir misiniz?' };
    }
}

// Initialize chatbot when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    const chatbot = new Chatbot();
    
    // Add click event to chat widget
    const chatWidget = document.querySelector('.chat-widget');
    if (chatWidget) {
        chatWidget.addEventListener('click', () => chatbot.toggleChat());
    }
}); 