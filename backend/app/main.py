"""
Point d'entrée principal de l'application FastAPI IAfluence
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.auth.router import router as auth_router
from app.clients.router import router as clients_router
from app.chatbots.router import router as chatbots_router
from app.conversations.router import router as conversations_router
from app.llm.router import router as llm_router
from app.widgets.router import router as widgets_router
from app.config import settings
from app.utils.db import init_db

# Création de l'application FastAPI
app = FastAPI(
    title="IAfluence API",
    description="API pour la gestion des chatbots IAfluence",
    version="1.0.0",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage des fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/widgets", StaticFiles(directory="widgets"), name="widgets")

# Inclusion des routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentification"])
app.include_router(clients_router, prefix="/api/clients", tags=["Clients"])
app.include_router(chatbots_router, prefix="/api/chatbots", tags=["Chatbots"])
app.include_router(conversations_router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(llm_router, prefix="/api/llm", tags=["LLM"])
app.include_router(widgets_router, prefix="/api/widgets", tags=["Widgets"])

@app.on_event("startup")
async def startup_db_client():
    """Initialisation de la connexion à la base de données au démarrage"""
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil de l'API"""
    return """
    <html>
        <head>
            <title>IAfluence API</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem;
                    line-height: 1.6;
                }
                h1 {
                    color: #4f46e5;
                }
                a {
                    color: #4f46e5;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .card {
                    background-color: #f9fafb;
                    border-radius: 8px;
                    padding: 1.5rem;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }
            </style>
        </head>
        <body>
            <h1>IAfluence API</h1>
            <div class="card">
                <h2>Documentation</h2>
                <p>Consultez la documentation interactive de l'API :</p>
                <ul>
                    <li><a href="/docs">Documentation Swagger</a></li>
                    <li><a href="/redoc">Documentation ReDoc</a></li>
                </ul>
            </div>
            <div class="card">
                <h2>Administration</h2>
                <p>Accédez à l'interface d'administration :</p>
                <ul>
                    <li><a href="/admin">Interface d'administration</a></li>
                </ul>
            </div>
            <div class="card">
                <h2>Statut</h2>
                <p>L'API est opérationnelle.</p>
            </div>
            <footer>
                <p>&copy; 2025 IAfluence. Tous droits réservés.</p>
            </footer>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Vérification de l'état de santé de l'API"""
    return {"status": "ok"}

@app.get("/preview")
async def preview(client_id: str):
    """Prévisualisation du chatbot pour un client donné"""
    # Cette route sera utilisée pour la prévisualisation du chatbot dans l'interface d'administration
    return HTMLResponse(content=f"""
    <html>
        <head>
            <title>Prévisualisation du chatbot</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/widgets/css/chatbot-widget.css">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: #f9fafb;
                }}
                .preview-container {{
                    width: 100%;
                    max-width: 400px;
                    height: 600px;
                    position: relative;
                    overflow: hidden;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                }}
            </style>
        </head>
        <body>
            <div class="preview-container">
                <div id="iafluence-chatbot-container" 
                    data-position="bottom-right"
                    data-primary-color="#4f46e5"
                    data-secondary-color="#ffffff"
                    data-chatbot-name="Assistant IA"
                    data-welcome-message="Bonjour ! Comment puis-je vous aider aujourd'hui ?"
                    data-logo-url=""
                    data-show-branding="true"
                    data-auto-open="true"
                    data-delay-auto-open="0"
                ></div>
            </div>
            <script>
                // Configuration du chatbot pour la prévisualisation
                var iafluenceConfig = {{
                    clientId: '{client_id}',
                    serverUrl: window.location.origin,
                    options: {{
                        position: 'bottom-right',
                        primaryColor: '#4f46e5',
                        secondaryColor: '#ffffff',
                        chatbotName: 'Assistant IA',
                        welcomeMessage: 'Bonjour ! Comment puis-je vous aider aujourd\\'hui ?',
                        logoUrl: '',
                        showBranding: true,
                        autoOpen: true,
                        delayAutoOpen: 0
                    }}
                }};
            </script>
            <script src="/widgets/js/chatbot-widget.js"></script>
            <script>
                // Initialisation du chatbot
                document.addEventListener('DOMContentLoaded', function() {{
                    if (window.IAfluenceChatbot) {{
                        window.IAfluenceChatbot.init(iafluenceConfig);
                    }}
                }});
            </script>
        </body>
    </html>
    """)
