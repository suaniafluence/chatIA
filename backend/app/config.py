"""
Configuration de l'application IAfluence
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Paramètres de configuration de l'application
    """
    # Paramètres généraux
    APP_NAME: str = "IAfluence"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    API_PREFIX: str = "/api"
    
    # Paramètres de sécurité
    SECRET_KEY: str = os.getenv("SECRET_KEY", "iafluence_secret_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 heures
    
    # Paramètres CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "https://iafluence.fr",
        "https://admin.iafluence.fr",
    ]
    
    # Paramètres MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "iafluence")
    
    # Paramètres LLM
    DEFAULT_LLM: str = "gpt-4"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    
    # Paramètres email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@iafluence.fr")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "suan.tay@iafluence.fr")
    
    # Paramètres de quota
    DEFAULT_MONTHLY_QUOTA: int = 1000  # Nombre de requêtes par mois
    
    # Paramètres d'administration
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "suan.tay@iafluence.fr")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "motdepassefort")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance des paramètres
settings = Settings()
