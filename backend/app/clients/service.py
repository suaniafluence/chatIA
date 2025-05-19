"""
Services d'authentification
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from app.config import settings
from app.utils.db import users_collection
from app.auth.models import UserCreate, UserInDB, User, TokenData

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration de l'authentification OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe en clair correspond à un mot de passe haché
    
    Args:
        plain_password: Mot de passe en clair
        hashed_password: Mot de passe haché
        
    Returns:
        True si les mots de passe correspondent, False sinon
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Génère un hash sécurisé pour un mot de passe
    
    Args:
        password: Mot de passe en clair
        
    Returns:
        Hash du mot de passe
    """
    return pwd_context.hash(password)

async def get_user(email: str) -> Optional[UserInDB]:
    """
    Récupère un utilisateur par son email
    
    Args:
        email: Email de l'utilisateur
        
    Returns:
        L'utilisateur s'il existe, None sinon
    """
    user_data = await users_collection.find_one({"email": email})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        return UserInDB(**user_data)
    return None

async def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authentifie un utilisateur
    
    Args:
        email: Email de l'utilisateur
        password: Mot de passe en clair
        
    Returns:
        L'utilisateur si l'authentification réussit, None sinon
    """
    user = await get_user(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    # Conversion de UserInDB en User (sans le mot de passe haché)
    return User(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_admin=user.is_admin,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT
    
    Args:
        data: Données à encoder dans le token
        expires_delta: Durée de validité du token
        
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Récupère l'utilisateur courant à partir du token JWT
    
    Args:
        token: Token JWT
        
    Returns:
        L'utilisateur courant
        
    Raises:
        HTTPException: Si le token est invalide ou l'utilisateur n'existe pas
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, is_admin=payload.get("is_admin", False))
    except JWTError:
        raise credentials_exception
    
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    
    # Conversion de UserInDB en User (sans le mot de passe haché)
    return User(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_admin=user.is_admin,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Vérifie que l'utilisateur courant est actif
    
    Args:
        current_user: Utilisateur courant
        
    Returns:
        L'utilisateur courant s'il est actif
        
    Raises:
        HTTPException: Si l'utilisateur est inactif
    """
    # Dans une version future, on pourrait ajouter un champ is_active
    return current_user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Vérifie que l'utilisateur courant est un administrateur
    
    Args:
        current_user: Utilisateur courant
        
    Returns:
        L'utilisateur courant s'il est administrateur
        
    Raises:
        HTTPException: Si l'utilisateur n'est pas administrateur
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits d'administrateur requis"
        )
    return current_user

async def create_user(user_create: UserCreate) -> User:
    """
    Crée un nouvel utilisateur
    
    Args:
        user_create: Données pour la création de l'utilisateur
        
    Returns:
        L'utilisateur créé
        
    Raises:
        HTTPException: Si l'email est déjà utilisé
    """
    # Vérification que l'email n'est pas déjà utilisé
    existing_user = await users_collection.find_one({"email": user_create.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé"
        )
    
    # Création de l'utilisateur
    now = datetime.utcnow()
    user_data = {
        "email": user_create.email,
        "full_name": user_create.full_name,
        "hashed_password": get_password_hash(user_create.password),
        "is_admin": user_create.is_admin,
        "created_at": now,
        "updated_at": now
    }
    
    result = await users_collection.insert_one(user_data)
    user_data["id"] = str(result.inserted_id)
    
    # Conversion en User (sans le mot de passe haché)
    return User(
        id=user_data["id"],
        email=user_data["email"],
        full_name=user_data["full_name"],
        is_admin=user_data["is_admin"],
        created_at=user_data["created_at"],
        updated_at=user_data["updated_at"]
    )
