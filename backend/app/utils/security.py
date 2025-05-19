"""
Utilitaires pour la sécurité
"""
import secrets
import string
import hashlib
import re
from typing import Optional

def generate_random_string(length: int = 32) -> str:
    """
    Génère une chaîne aléatoire sécurisée
    
    Args:
        length: Longueur de la chaîne à générer
        
    Returns:
        Chaîne aléatoire
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_client_id(name: str) -> str:
    """
    Génère un identifiant client à partir d'un nom
    
    Args:
        name: Nom du client
        
    Returns:
        Identifiant client
    """
    # Conversion en minuscules
    name = name.lower()
    
    # Suppression des caractères spéciaux et remplacement des espaces par des tirets
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'\s+', '-', name)
    
    # Ajout d'un suffixe aléatoire pour éviter les collisions
    suffix = generate_random_string(6).lower()
    
    return f"{name}-{suffix}"

def hash_password(password: str) -> str:
    """
    Hache un mot de passe avec SHA-256
    
    Args:
        password: Mot de passe en clair
        
    Returns:
        Hash du mot de passe
    """
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """
    Valide une adresse email
    
    Args:
        email: Adresse email à valider
        
    Returns:
        True si l'adresse email est valide, False sinon
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_input(input_str: Optional[str]) -> Optional[str]:
    """
    Nettoie une chaîne d'entrée pour éviter les injections
    
    Args:
        input_str: Chaîne à nettoyer
        
    Returns:
        Chaîne nettoyée
    """
    if input_str is None:
        return None
    
    # Suppression des caractères potentiellement dangereux
    return re.sub(r'[<>&\'"]', '', input_str)
