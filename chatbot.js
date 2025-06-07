class Chatbot {
    constructor() {
        this.chatWindow = null;
        this.isOpen = false;
        this.projectData = null;
        this.loadProjectData();
        console.log('Chatbot constructor çalıştı');
        this.initializeChatbot();
    }

    initializeChatbot() {
        console.log('Chatbot initializeChatbot başlıyor');
        // Create chat window
        this.chatWindow = document.createElement('div');
        this.chatWindow.className = 'chat-window';
        this.chatWindow.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 400px;
            height: 500px;
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
            display: flex;
            flex-direction: column;
        `;

        // Create map container
        const mapContainer = document.createElement('div');
        mapContainer.className = 'map-container';
        mapContainer.style.cssText = `
            flex: 1;
            display: none;
            margin-top: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
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
        this.chatWindow.appendChild(mapContainer);
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
        console.log('Chatbot initializeChatbot bitti');

        // Bot ve kullanıcı mesajı için zorunlu stil ekle
        const style = document.createElement('style');
        style.innerHTML = `
        .bot-message {
            background: #000000 ;
            color: #000000  ;
            font-weight: 600  ;
            margin-right: auto;
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 15px;
            max-width: 80%;
            word-break: break-word;
        }
        .user-message {
            background: #2c3e50  ;
            color: #fff  ;
            margin-left: auto;
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 15px;
            max-width: 80%;
            word-break: break-word;
        }
        `;
        document.head.appendChild(style);
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        this.chatWindow.style.display = this.isOpen ? 'flex' : 'none';
        console.log('Chatbot penceresi açıldı mı:', this.isOpen);
    }

    addMessage(text, sender, html = null) {
        const messagesContainer = this.chatWindow.querySelector('.chat-messages');
        const messageDiv = document.createElement('div');
    
        if (sender === 'user') {
            messageDiv.style.cssText = `
                margin-left: auto  ;
                background: #2c3e50  ;
                color: white  ;
                margin-bottom: 10px  ;
                padding: 8px 12px  ;
                border-radius: 15px  ;
                max-width: 80%  ;
                font-weight: 500  ;
            `;
        } else {
            messageDiv.style.cssText = `
                margin-right: auto ;
                background: #ffffff;
                color: #000000  ;
                margin-bottom: 10px  ;
                padding: 8px 12px  ;
                border-radius: 15px  ;
                max-width: 80%  ;
                font-weight: 500  ;
            `;
        }
    
        if (html) {
            messageDiv.innerHTML = html;
        } else {
            messageDiv.textContent = text;
        }
    
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        console.log('addMessage:', sender, text);
    }
    
    

    async sendMessage(input) {
        const text = input.value.trim();
        if (text) {
            this.addMessage(text, 'user');
            input.value = '';
            console.log('Kullanıcı mesajı gönderdi:', text);
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
        } else {
            console.log('Boş mesaj gönderilmeye çalışıldı');
        }
    }

    async getBotResponse(text) {
        try {
            console.log('OpenAI API fetch başlıyor:', text);
            const response = await fetch('http://localhost:5001/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            console.log('OpenAI API cevabı:', data);
            return { response: data.answer };
        } catch (error) {
            console.error('OpenAI API fetch hatası:', error);
            return { response: 'Üzgünüm, şu anda yanıt veremiyorum.' };
        }
    }

    async loadProjectData() {
        try {
            const response = await fetch('project_data.json');
            this.projectData = await response.json();
            console.log('Proje verileri yüklendi:', this.projectData);
        } catch (error) {
            console.error('Proje verileri yüklenirken hata oluştu:', error);
        }
    }

    showMap(mapFile) {
        const mapContainer = this.chatWindow.querySelector('.map-container');
        mapContainer.style.display = 'block';
        mapContainer.innerHTML = `<iframe src="${mapFile}" style="width: 100%; height: 100%; border: none;"></iframe>`;
    }

    hideMap() {
        const mapContainer = this.chatWindow.querySelector('.map-container');
        mapContainer.style.display = 'none';
        mapContainer.innerHTML = '';
    }

    async handleUserMessage(message) {
        if (!this.projectData) {
            return "Üzgünüm, proje verileri henüz yüklenemedi. Lütfen daha sonra tekrar deneyin.";
        }

        const lowerMessage = message.toLowerCase();

        // Harita görselleştirmeleri hakkında bilgi
        if (lowerMessage.includes('harita göster') || lowerMessage.includes('haritayı aç')) {
            if (lowerMessage.includes('tüm') || lowerMessage.includes('hepsi')) {
                const allPointsMap = this.projectData.map_data.visualizations.tum_noktalar;
                this.showMap(allPointsMap.file);
                return `Tüm lokasyonları gösteren harita yükleniyor...`;
            }

            // Spesifik lokasyon türü için harita
            for (const [key, value] of Object.entries(this.projectData.map_data.locations)) {
                if (lowerMessage.includes(key.replace('_', ' ')) && value.visualization) {
                    this.showMap(value.visualization);
                    return `${value.description} haritası yükleniyor...`;
                }
            }

            // Genel İstanbul haritası
            if (lowerMessage.includes('istanbul')) {
                const istanbulMap = this.projectData.map_data.visualizations.istanbul_genel;
                this.showMap(istanbulMap.file);
                return `İstanbul genel haritası yükleniyor...`;
            }
        }

        // Haritayı kapat
        if (lowerMessage.includes('haritayı kapat') || lowerMessage.includes('haritayı gizle')) {
            this.hideMap();
            return "Harita kapatıldı.";
        }

        // Harita verileri hakkında bilgi
        if (lowerMessage.includes('harita') || lowerMessage.includes('konum') || lowerMessage.includes('yer')) {
            if (lowerMessage.includes('trafik')) {
                const trafficInfo = this.projectData.map_data.traffic_data;
                return `Trafik verilerimiz şunları içerir:\n` +
                       `- Yol verileri (${trafficInfo.yollar.size})\n` +
                       `- Yol tipleri, konumlar, uzunluklar ve trafik yoğunluğu bilgileri\n` +
                       `Detaylı bilgi için hangi tür trafik verisi hakkında bilgi almak istersiniz?`;
            }

            // Lokasyon türlerini listele
            if (lowerMessage.includes('nereler') || lowerMessage.includes('listele')) {
                const locations = Object.entries(this.projectData.map_data.locations)
                    .map(([key, value]) => `- ${key.replace('_', ' ')}: ${value.description} (${value.total_count || 'N/A'} kayıt)`)
                    .join('\n');
                return `Haritamızda şu lokasyon türleri bulunmaktadır:\n${locations}\n\nHarita görselleştirmelerini görmek için "harita göster [lokasyon adı]" yazabilirsiniz.`;
            }

            // Spesifik lokasyon türü hakkında bilgi
            for (const [key, value] of Object.entries(this.projectData.map_data.locations)) {
                if (lowerMessage.includes(key.replace('_', ' '))) {
                    return `${value.description}\n` +
                           `Toplam kayıt: ${value.total_count || 'N/A'}\n` +
                           `Özellikler: ${value.features.join(', ')}\n` +
                           `Veri kaynağı: ${value.data_source}\n\n` +
                           `Haritayı görmek için "harita göster ${key.replace('_', ' ')}" yazabilirsiniz.`;
                }
            }
        }

        // Mevcut kontroller devam ediyor...
        if (lowerMessage.includes('proje') || lowerMessage.includes('uygulama') || lowerMessage.includes('sistem')) {
            return `Bu proje "${this.projectData.project_name}" adında bir web uygulamasıdır. ${this.projectData.description}`;
        }

        // Özellikler hakkında bilgi
        if (lowerMessage.includes('özellik') || lowerMessage.includes('ne yapabilir')) {
            const features = this.projectData.features.map(f => 
                `- ${f.name}: ${f.description}`
            ).join('\n');
            return `Projemizin özellikleri:\n${features}`;
        }

        // Sayfalar hakkında bilgi
        if (lowerMessage.includes('sayfa') || lowerMessage.includes('bölüm')) {
            const pages = this.projectData.pages.map(p => 
                `- ${p.name}: ${p.description}`
            ).join('\n');
            return `Projemizin sayfaları:\n${pages}`;
        }

        // Spesifik özellik hakkında bilgi
        for (const feature of this.projectData.features) {
            if (lowerMessage.includes(feature.name.toLowerCase())) {
                return `${feature.name} özelliği: ${feature.description}`;
            }
        }

        // Spesifik sayfa hakkında bilgi
        for (const page of this.projectData.pages) {
            if (lowerMessage.includes(page.name.toLowerCase())) {
                return `${page.name} sayfası: ${page.description}`;
            }
        }

        return "Üzgünüm, bu konuda bilgim yok. Proje hakkında daha spesifik bir soru sorabilir misiniz?";
    }
}

// Initialize chatbot when document is loaded
console.log('DOMContentLoaded bekleniyor...');
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded tetiklendi, Chatbot başlatılıyor');
    
    // Chat widget'ı oluştur
    const chatWidget = document.createElement('div');
    chatWidget.className = 'chat-widget';
    chatWidget.innerHTML = `
        <button class="chat-button" style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #3498db, #2c3e50); color: white; border: none; cursor: pointer; box-shadow: 0 2px 8px rgba(44,62,80,0.18); font-size: 2rem; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-robot"></i><span class="fallback-robot" style="display:none;">🤖</span>
        </button>
    `;
    document.body.appendChild(chatWidget);

    // Font Awesome yüklenemezse fallback göster
    window.addEventListener('DOMContentLoaded', () => {
        const faRobot = document.querySelector('.chat-button i.fas.fa-robot');
        const fallback = document.querySelector('.chat-button .fallback-robot');
        if (faRobot && window.getComputedStyle(faRobot).fontFamily.indexOf('FontAwesome') === -1) {
            faRobot.style.display = 'none';
            if (fallback) fallback.style.display = 'inline';
        }
    });

    // Chatbot'u başlat
    const chatbot = new Chatbot();
    
    // Chat widget'a tıklama olayı ekle
    chatWidget.addEventListener('click', () => chatbot.toggleChat());
    console.log('chat-widget click event eklendi');
}); 