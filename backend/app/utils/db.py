"""
Utilitaires pour la connexion à la base de données MongoDB
"""
import motor.motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.config import settings
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Client MongoDB asynchrone
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]

# Collections
clients_collection = db["clients"]
chatbots_collection = db["chatbots"]
conversations_collection = db["conversations"]
users_collection = db["users"]
llm_usage_collection = db["llm_usage"]

async def init_db():
    """
    Initialise la connexion à la base de données et crée les index nécessaires
    """
    try:
        # Vérification de la connexion
        await client.admin.command('ping')
        logger.info("Connexion à MongoDB établie avec succès")
        
        # Création des index
        await clients_collection.create_index("client_id", unique=True)
        await chatbots_collection.create_index("client_id")
        await conversations_collection.create_index([("client_id", 1), ("timestamp", -1)])
        await conversations_collection.create_index("session_id")
        await users_collection.create_index("email", unique=True)
        await llm_usage_collection.create_index([("client_id", 1), ("date", 1)])
        
        # Création de l'utilisateur admin par défaut s'il n'existe pas
        admin_exists = await users_collection.find_one({"email": settings.ADMIN_USERNAME})
        if not admin_exists:
            from app.auth.models import UserCreate
            from app.auth.service import create_user
            
            admin_user = UserCreate(
                email=settings.ADMIN_USERNAME,
                password=settings.ADMIN_PASSWORD,
                is_admin=True,
                full_name="Admin IAfluence"
            )
            await create_user(admin_user)
            logger.info(f"Utilisateur admin créé: {settings.ADMIN_USERNAME}")
            
    except ServerSelectionTimeoutError:
        logger.error("Impossible de se connecter à MongoDB")
        raise

def get_client_db(client_id: str):
    """
    Retourne une référence à la base de données spécifique d'un client
    
    Args:
        client_id: Identifiant unique du client
        
    Returns:
        Une référence à la base de données du client
    """
    return client[f"{settings.MONGODB_DB_NAME}_{client_id}"]

def get_sync_client():
    """
    Retourne un client MongoDB synchrone pour les opérations non-asynchrones
    
    Returns:
        Un client MongoDB synchrone
    """
    return MongoClient(settings.MONGODB_URL)
