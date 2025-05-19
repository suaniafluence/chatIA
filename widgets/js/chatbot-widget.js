/**
 * Script principal du widget de chatbot IAfluence
 * Ce script gère l'interface utilisateur du chatbot et la communication avec le serveur
 */

class IAfluenceChatbot {
    /**
     * Configuration du chatbot
     * @type {Object}
     */
    #config = null;

    /**
     * État du chatbot (ouvert/fermé)
     * @type {boolean}
     */
    #isOpen = false;

    /**
     * Élément DOM du conteneur du chatbot
     * @type {HTMLElement}
     */
    #container = null;

    /**
     * Élément DOM du bouton du chatbot
     * @type {HTMLElement}
     */
    #button = null;

    /**
     * Élément DOM de la fenêtre du chatbot
     * @type {HTMLElement}
     */
    #window = null;

    /**
     * Élément DOM du conteneur des messages
     * @type {HTMLElement}
     */
    #messagesContainer = null;

    /**
     * Élément DOM du champ de saisie
     * @type {HTMLElement}
     */
    #inputField = null;

    /**
     * Historique de la conversation
     * @type {Array}
     */
    #conversationHistory = [];

    /**
     * ID de session unique
     * @type {string}
     */
    #sessionId = '';

    /**
     * Initialise le chatbot avec la configuration fournie
     * @param {Object} config - Configuration du chatbot
     */
    static init(config) {
        const chatbot = new IAfluenceChatbot(config);
        chatbot.render();
        return chatbot;
    }

    /**
     * Constructeur
     * @param {Object} config - Configuration du chatbot
     */
    constructor(config) {
        this.#config = config;
        this.#sessionId = this.#generateSessionId();
        this.#container = document.getElementById('iafluence-chatbot-container');

        // Vérification de la présence du conteneur
        if (!this.#container) {
            console.error('IAfluence Chatbot: Conteneur non trouvé');
            return;
        }

        // Récupération des options depuis les attributs data-*
        const position = this.#container.getAttribute('data-position') || config.options.position;
        const primaryColor = this.#container.getAttribute('data-primary-color') || config.options.primaryColor;
        const secondaryColor = this.#container.getAttribute('data-secondary-color') || config.options.secondaryColor;
        const chatbotName = this.#container.getAttribute('data-chatbot-name') || config.options.chatbotName;
        const welcomeMessage = this.#container.getAttribute('data-welcome-message') || config.options.welcomeMessage;
        const logoUrl = this.#container.getAttribute('data-logo-url') || config.options.logoUrl;
        const showBranding = this.#container.getAttribute('data-show-branding') === 'true' || config.options.showBranding;
        const autoOpen = this.#container.getAttribute('data-auto-open') === 'true' || config.options.autoOpen;
        const delayAutoOpen = parseInt(this.#container.getAttribute('data-delay-auto-open')) || config.options.delayAutoOpen;

        // Mise à jour de la configuration avec les valeurs des attributs
        this.#config.options = {
            ...config.options,
            position,
            primaryColor,
            secondaryColor,
            chatbotName,
            welcomeMessage,
            logoUrl,
            showBranding,
            autoOpen,
            delayAutoOpen
        };

        // Ouverture automatique si configurée
        if (autoOpen) {
            setTimeout(() => {
                this.open();
            }, delayAutoOpen);
        }
    }

    /**
     * Génère un ID de session unique
     * @returns {string} ID de session
     */
    #generateSessionId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Crée et affiche l'interface du chatbot
     */
    render() {
        // Création du bouton
        this.#button = document.createElement('div');
        this.#button.className = 'iafluence-chatbot-button';
        this.#button.style.backgroundColor = this.#config.options.primaryColor;
        this.#button.innerHTML = `
            <div class="iafluence-chatbot-button-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${this.#config.options.secondaryColor}" width="24" height="24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
                </svg>
            </div>
        `;

        // Positionnement du bouton
        this.#button.classList.add(`iafluence-chatbot-button-${this.#config.options.position}`);

        // Création de la fenêtre du chatbot
        this.#window = document.createElement('div');
        this.#window.className = 'iafluence-chatbot-window';
        this.#window.classList.add(`iafluence-chatbot-window-${this.#config.options.position}`);
        this.#window.style.display = 'none';

        // En-tête de la fenêtre
        const header = document.createElement('div');
        header.className = 'iafluence-chatbot-header';
        header.style.backgroundColor = this.#config.options.primaryColor;
        header.style.color = this.#config.options.secondaryColor;

        // Logo dans l'en-tête
        let logoHtml = '';
        if (this.#config.options.logoUrl) {
            logoHtml = `<img src="${this.#config.options.logoUrl}" alt="Logo" class="iafluence-chatbot-logo">`;
        } else {
            logoHtml = `
                <div class="iafluence-chatbot-default-logo">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${this.#config.options.secondaryColor}" width="24" height="24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
                    </svg>
                </div>
            `;
        }

        header.innerHTML = `
            ${logoHtml}
            <div class="iafluence-chatbot-title">${this.#config.options.chatbotName}</div>
            <div class="iafluence-chatbot-close">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${this.#config.options.secondaryColor}" width="18" height="18">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
            </div>
        `;

        // Conteneur des messages
        this.#messagesContainer = document.createElement('div');
        this.#messagesContainer.className = 'iafluence-chatbot-messages';

        // Pied de page avec champ de saisie
        const footer = document.createElement('div');
        footer.className = 'iafluence-chatbot-footer';

        // Champ de saisie
        this.#inputField = document.createElement('input');
        this.#inputField.type = 'text';
        this.#inputField.className = 'iafluence-chatbot-input';
        this.#inputField.placeholder = 'Tapez votre message...';

        // Bouton d'envoi
        const sendButton = document.createElement('button');
        sendButton.className = 'iafluence-chatbot-send';
        sendButton.style.backgroundColor = this.#config.options.primaryColor;
        sendButton.style.color = this.#config.options.secondaryColor;
        sendButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${this.#config.options.secondaryColor}" width="18" height="18">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
        `;

        // Branding IAfluence
        let brandingHtml = '';
        if (this.#config.options.showBranding) {
            brandingHtml = `
                <div class="iafluence-chatbot-branding">
                    Propulsé par <a href="https://iafluence.fr" target="_blank" rel="noopener noreferrer">IAfluence</a>
                </div>
            `;
        }

        // Assemblage du pied de page
        footer.appendChild(this.#inputField);
        footer.appendChild(sendButton);
        if (brandingHtml) {
            const brandingElement = document.createElement('div');
            brandingElement.innerHTML = brandingHtml;
            footer.appendChild(brandingElement.firstElementChild);
        }

        // Assemblage de la fenêtre
        this.#window.appendChild(header);
        this.#window.appendChild(this.#messagesContainer);
        this.#window.appendChild(footer);

        // Ajout des éléments au conteneur
        this.#container.appendChild(this.#button);
        this.#container.appendChild(this.#window);

        // Ajout des écouteurs d'événements
        this.#addEventListeners();

        // Affichage du message de bienvenue
        this.#addMessage('bot', this.#config.options.welcomeMessage);
    }

    /**
     * Ajoute les écouteurs d'événements
     */
    #addEventListeners() {
        // Ouverture/fermeture du chatbot
        this.#button.addEventListener('click', () => {
            this.toggle();
        });

        // Fermeture du chatbot
        const closeButton = this.#window.querySelector('.iafluence-chatbot-close');
        closeButton.addEventListener('click', () => {
            this.close();
        });

        // Envoi de message par clic sur le bouton
        const sendButton = this.#window.querySelector('.iafluence-chatbot-send');
        sendButton.addEventListener('click', () => {
            this.#sendMessage();
        });

        // Envoi de message par appui sur Entrée
        this.#inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.#sendMessage();
            }
        });
    }

    /**
     * Ouvre la fenêtre du chatbot
     */
    open() {
        if (!this.#isOpen) {
            this.#window.style.display = 'flex';
            this.#isOpen = true;
            this.#inputField.focus();
        }
    }

    /**
     * Ferme la fenêtre du chatbot
     */
    close() {
        if (this.#isOpen) {
            this.#window.style.display = 'none';
            this.#isOpen = false;
        }
    }

    /**
     * Bascule l'état de la fenêtre du chatbot (ouvert/fermé)
     */
    toggle() {
        if (this.#isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    /**
     * Envoie un message au serveur
     */
    #sendMessage() {
        const message = this.#inputField.value.trim();
        if (!message) return;

        // Affichage du message de l'utilisateur
        this.#addMessage('user', message);
        this.#inputField.value = '';

        // Affichage d'un indicateur de chargement
        const loadingId = this.#addLoadingIndicator();

        // Envoi de la requête au serveur
        fetch(`${this.#config.serverUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                client_id: this.#config.clientId,
                session_id: this.#sessionId,
                message: message,
                conversation_history: this.#conversationHistory
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur de communication avec le serveur');
            }
            return response.json();
        })
        .then(data => {
            // Suppression de l'indicateur de chargement
            this.#removeLoadingIndicator(loadingId);
            
            // Affichage de la réponse du bot
            this.#addMessage('bot', data.response);
        })
        .catch(error => {
            // Suppression de l'indicateur de chargement
            this.#removeLoadingIndicator(loadingId);
            
            // Affichage d'un message d'erreur
            this.#addMessage('bot', 'Désolé, une erreur est survenue. Veuillez réessayer plus tard.');
            console.error('IAfluence Chatbot Error:', error);
        });
    }

    /**
     * Ajoute un message à la conversation
     * @param {string} sender - Expéditeur du message ('user' ou 'bot')
     * @param {string} content - Contenu du message
     * @returns {string} ID du message
     */
    #addMessage(sender, content) {
        const messageId = `msg-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
        const timestamp = new Date().toISOString();

        // Création de l'élément de message
        const messageElement = document.createElement('div');
        messageElement.className = `iafluence-chatbot-message iafluence-chatbot-message-${sender}`;
        messageElement.id = messageId;

        // Formatage du contenu avec prise en charge des liens et des sauts de ligne
        const formattedContent = this.#formatMessageContent(content);

        // Ajout du contenu au message
        messageElement.innerHTML = `
            <div class="iafluence-chatbot-message-content">${formattedContent}</div>
            <div class="iafluence-chatbot-message-time">${this.#formatTime(new Date())}</div>
        `;

        // Ajout du message au conteneur
        this.#messagesContainer.appendChild(messageElement);

        // Défilement vers le bas
        this.#scrollToBottom();

        // Ajout à l'historique de conversation
        this.#conversationHistory.push({
            id: messageId,
            sender: sender,
            content: content,
            timestamp: timestamp
        });

        return messageId;
    }

    /**
     * Formate le contenu du message (liens, sauts de ligne, etc.)
     * @param {string} content - Contenu brut du message
     * @returns {string} Contenu formaté en HTML
     */
    #formatMessageContent(content) {
        // Conversion des URLs en liens cliquables
        let formattedContent = content.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
        );
        
        // Conversion des sauts de ligne en balises <br>
        formattedContent = formattedContent.replace(/\n/g, '<br>');
        
        return formattedContent;
    }

    /**
     * Ajoute un indicateur de chargement
     * @returns {string} ID de l'indicateur
     */
    #addLoadingIndicator() {
        const loadingId = `loading-${Date.now()}`;
        
        // Création de l'élément de chargement
        const loadingElement = document.createElement('div');
        loadingElement.className = 'iafluence-chatbot-message iafluence-chatbot-message-bot';
        loadingElement.id = loadingId;
        
        // Ajout des points de chargement
        loadingElement.innerHTML = `
            <div class="iafluence-chatbot-loading">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        // Ajout de l'indicateur au conteneur
        this.#messagesContainer.appendChild(loadingElement);
        
        // Défilement vers le bas
        this.#scrollToBottom();
        
        return loadingId;
    }

    /**
     * Supprime l'indicateur de chargement
     * @param {string} loadingId - ID de l'indicateur à supprimer
     */
    #removeLoadingIndicator(loadingId) {
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    /**
     * Fait défiler la conversation vers le bas
     */
    #scrollToBottom() {
        this.#messagesContainer.scrollTop = this.#messagesContainer.scrollHeight;
    }

    /**
     * Formate l'heure pour l'affichage
     * @param {Date} date - Date à formater
     * @returns {string} Heure formatée (HH:MM)
     */
    #formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.get
(Content truncated due to size limit. Use line ranges to read in chunks)